"""Loopback-only HTTP gateway for the isolated E3D live bridge."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hmac
import json
import os
from pathlib import Path
import threading
import time
from typing import Any

from .apply import (
    ApplyAuthorizationRequest,
    ApplyResultRequest,
    PendingChangeRegistry,
)
from .assistant import ReadOnlyAssistant
from .audit import AuditLog
from .openai_backend import (
    ASSISTANT_PROVIDERS,
    DEFAULT_OPENAI_MODEL,
    DEFAULT_TOKEN_RHYTHM_MODEL,
    OpenAIBackendConfig,
    OpenAIBackendError,
    OpenAICompatibleChatConfig,
    OpenAICompatibleChatPreviewAssistant,
    OpenAIPreviewAssistant,
    PROVIDER_OPENAI_RESPONSES,
    PROVIDER_TOKEN_RHYTHM_CHAT,
)
from .preview import ChangePreviewRequest
from .protocol import (
    PROTOCOL_VERSION,
    ProtocolError,
    ScopeKey,
    SelectionEnvelope,
    _require_exact_keys,
    _require_mapping,
    _require_positive_int,
    _require_string,
)
from .session import (
    ACCESS_MODES,
    ACCESS_MODE_CONTROLLED_WRITE,
    LiveSession,
    default_session_file,
    default_session_root,
    remove_session_file,
    write_session_file,
)


DEFAULT_PORT = 48731
MAX_REQUEST_BYTES = 1_048_576
TOKEN_HEADER = "X-E3D-Live-Token"


class AuthenticationError(PermissionError):
    """Raised when a request does not carry the active bridge token."""


@dataclass(frozen=True)
class GatewayConfig:
    session: LiveSession
    max_request_bytes: int = MAX_REQUEST_BYTES
    openai_model: str = DEFAULT_OPENAI_MODEL
    audit_log: AuditLog | None = None


class BridgeService:
    """Scope and authentication gate in front of the assistant backend."""

    def __init__(self, config: GatewayConfig, assistant: Any | None = None):
        self.config = config
        self.assistant = assistant or ReadOnlyAssistant()
        self._selection_assistant = ReadOnlyAssistant()
        self._assistant_lock = threading.Lock()
        self._assistant_generation = 0
        self._changes = PendingChangeRegistry()
        self._audit = config.audit_log or AuditLog(None)
        self._metrics_lock = threading.Lock()
        self._preview_execution_lock = threading.Lock()
        self._preview_cache_lock = threading.Lock()
        self._preview_cache: dict[str, tuple[str, dict[str, Any]]] = {}
        self._accepted_selection_count = 0
        self._accepted_preview_count = 0
        self._accepted_authorization_count = 0
        self._accepted_apply_result_count = 0
        self._last_request_id: str | None = None
        self._last_preview_request_id: str | None = None

    def health(self) -> dict[str, Any]:
        with self._assistant_lock:
            assistant = self.assistant
            active_change_set_count = self._changes.active_count()
        with self._metrics_lock:
            return {
                "status": "ok",
                "mode": self.config.session.access_mode,
                "protocol_version": PROTOCOL_VERSION,
                "bridge_session_id": self.config.session.bridge_session_id,
                "target_process_id": self.config.session.target_process_id,
                "scope": self.config.session.scope.to_dict(),
                "assistant_backend": assistant.backend_name,
                "assistant_model": assistant.model_name,
                "assistant_endpoint_origin": getattr(
                    assistant, "endpoint_origin", None
                ),
                "accepted_selection_count": self._accepted_selection_count,
                "accepted_preview_count": self._accepted_preview_count,
                "accepted_authorization_count": self._accepted_authorization_count,
                "accepted_apply_result_count": self._accepted_apply_result_count,
                "active_change_set_count": active_change_set_count,
                "last_request_id": self._last_request_id,
                "last_preview_request_id": self._last_preview_request_id,
            }

    def process_selection(self, payload: Any, token: str) -> dict[str, Any]:
        if not hmac.compare_digest(token or "", self.config.session.token):
            raise AuthenticationError("invalid bridge token")

        envelope = SelectionEnvelope.from_mapping(payload)
        if envelope.bridge_session_id != self.config.session.bridge_session_id:
            raise ProtocolError("bridge_session_id does not match the active gateway")
        if envelope.process_id != self.config.session.target_process_id:
            raise ProtocolError("process_id does not match the target E3D process")
        self.config.session.scope.assert_matches(envelope.scope)
        response = self._selection_assistant.analyse(envelope).to_dict()
        with self._metrics_lock:
            self._accepted_selection_count += 1
            self._last_request_id = envelope.request_id
        self._audit.append(
            "selection.accepted",
            request_id=envelope.request_id,
            process_id=envelope.process_id,
            scope=envelope.scope.to_dict(),
            target_element=envelope.selection.full_name,
        )
        return response

    def process_preview(self, payload: Any, token: str) -> dict[str, Any]:
        if not hmac.compare_digest(token or "", self.config.session.token):
            raise AuthenticationError("invalid bridge token")

        request = ChangePreviewRequest.from_mapping(payload)
        envelope = request.envelope
        if envelope.bridge_session_id != self.config.session.bridge_session_id:
            raise ProtocolError("bridge_session_id does not match the active gateway")
        if envelope.process_id != self.config.session.target_process_id:
            raise ProtocolError("process_id does not match the target E3D process")
        self.config.session.scope.assert_matches(envelope.scope)

        fingerprint = sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        # One E3D process has one operator-driven preview lane. Serialising this
        # section makes duplicate request IDs truly idempotent under concurrency
        # and prevents two external calls from registering different ChangeSets.
        with self._preview_execution_lock:
            return self._process_preview_once(request, fingerprint)

    def _process_preview_once(
        self,
        request: ChangePreviewRequest,
        fingerprint: str,
    ) -> dict[str, Any]:
        envelope = request.envelope
        with self._preview_cache_lock:
            cached = self._preview_cache.get(envelope.request_id)
            if cached is not None:
                if cached[0] != fingerprint:
                    raise ProtocolError(
                        "request_id was reused with a different preview payload"
                    )
                return json.loads(json.dumps(cached[1]))

        with self._assistant_lock:
            assistant = self.assistant
            assistant_generation = self._assistant_generation
        preview = assistant.preview(request)
        with self._assistant_lock:
            if assistant_generation != self._assistant_generation:
                raise ProtocolError(
                    "assistant provider changed while the preview was in progress"
                )
            record = (
                self._changes.register(request, preview)
                if self.config.session.write_enabled
                else None
            )
            response = preview.to_response(
                request=request,
                backend=assistant.backend_name,
                model=assistant.model_name,
                change_set_id=record.change_set_id if record else None,
                expires_at_utc=record.expires_at_utc if record else None,
                write_enabled=self.config.session.write_enabled,
            )
            with self._preview_cache_lock:
                if len(self._preview_cache) >= 128:
                    oldest_request_id = next(iter(self._preview_cache))
                    del self._preview_cache[oldest_request_id]
                self._preview_cache[envelope.request_id] = (fingerprint, response)
            with self._metrics_lock:
                self._accepted_preview_count += 1
                self._last_preview_request_id = envelope.request_id
        self._audit.append(
            "preview.accepted",
            request_id=envelope.request_id,
            process_id=envelope.process_id,
            scope=envelope.scope.to_dict(),
            target_element=envelope.selection.full_name,
            change_set_id=record.change_set_id if record else None,
            operation_count=len(preview.operations),
            backend=assistant.backend_name,
            model=assistant.model_name,
        )
        return response

    def configure_assistant(self, payload: Any, token: str) -> dict[str, Any]:
        if not hmac.compare_digest(token or "", self.config.session.token):
            raise AuthenticationError("invalid bridge token")
        data = _require_mapping(payload, "message")
        _require_exact_keys(
            data,
            "message",
            {
                "protocol_version",
                "message_type",
                "bridge_session_id",
                "process_id",
                "scope",
                "provider",
                "model",
                "api_key",
            },
        )
        if data.get("protocol_version") != PROTOCOL_VERSION:
            raise ProtocolError("configure message protocol_version is incompatible")
        if data.get("message_type") != "configure_assistant":
            raise ProtocolError("message_type must be 'configure_assistant'")
        bridge_session_id = _require_string(
            data.get("bridge_session_id"), "bridge_session_id", max_length=128
        )
        process_id = _require_positive_int(data.get("process_id"), "process_id")
        scope = ScopeKey.from_mapping(data.get("scope"))
        self._assert_bound_session(bridge_session_id, process_id, scope)
        api_key = _require_string(data.get("api_key"), "api_key", max_length=512)
        provider = _require_string(data.get("provider"), "provider", max_length=64)
        if provider not in ASSISTANT_PROVIDERS:
            raise ProtocolError("provider is unsupported")
        model = _require_string(
            data.get("model"), "model", max_length=128, allow_empty=True
        )
        try:
            if provider == PROVIDER_OPENAI_RESPONSES:
                assistant = OpenAIPreviewAssistant(
                    OpenAIBackendConfig.from_api_key(
                        api_key, model=model or self.config.openai_model
                    )
                )
            elif provider == PROVIDER_TOKEN_RHYTHM_CHAT:
                assistant = OpenAICompatibleChatPreviewAssistant(
                    OpenAICompatibleChatConfig.from_api_key(
                        api_key, model=model or DEFAULT_TOKEN_RHYTHM_MODEL
                    )
                )
            else:  # pragma: no cover - guarded by ASSISTANT_PROVIDERS
                raise ProtocolError("provider is unsupported")
        except OpenAIBackendError as exc:
            raise ProtocolError(str(exc)) from exc
        with self._assistant_lock:
            self.assistant = assistant
            self._assistant_generation += 1
            # Provider changes revoke previews produced by the prior backend.
            self._changes = PendingChangeRegistry()
            with self._preview_cache_lock:
                self._preview_cache.clear()
        self._audit.append(
            "assistant.configured",
            process_id=process_id,
            scope=scope.to_dict(),
            backend=assistant.backend_name,
            model=assistant.model_name,
            endpoint_origin=getattr(assistant, "endpoint_origin", None),
        )
        return {
            "protocol_version": PROTOCOL_VERSION,
            "status": "configured",
            "backend": assistant.backend_name,
            "model": assistant.model_name,
            "endpoint_origin": getattr(assistant, "endpoint_origin", None),
            "access_mode": self.config.session.access_mode,
            "api_key_persistence": "memory_only",
        }

    def configure_openai(self, payload: Any, token: str) -> dict[str, Any]:
        """Accept the phase-3 official OpenAI message during rolling upgrades."""
        if not hmac.compare_digest(token or "", self.config.session.token):
            raise AuthenticationError("invalid bridge token")
        data = _require_mapping(payload, "message")
        _require_exact_keys(
            data,
            "message",
            {
                "protocol_version",
                "message_type",
                "bridge_session_id",
                "process_id",
                "scope",
                "api_key",
            },
        )
        upgraded = dict(data)
        upgraded["message_type"] = "configure_assistant"
        upgraded["provider"] = PROVIDER_OPENAI_RESPONSES
        upgraded["model"] = self.config.openai_model
        return self.configure_assistant(upgraded, token)

    def process_authorization(self, payload: Any, token: str) -> dict[str, Any]:
        if not self.config.session.write_enabled:
            raise ProtocolError("the active gateway session is read-only")
        if not hmac.compare_digest(token or "", self.config.session.token):
            raise AuthenticationError("invalid bridge token")
        request = ApplyAuthorizationRequest.from_mapping(payload)
        self._assert_bound_session(
            request.session.bridge_session_id,
            request.session.process_id,
            request.session.scope,
        )
        with self._assistant_lock:
            response = self._changes.authorize(request)
        with self._metrics_lock:
            self._accepted_authorization_count += 1
        self._audit.append(
            "apply.authorized",
            request_id=request.request_id,
            process_id=request.session.process_id,
            scope=request.session.scope.to_dict(),
            target_element=request.target_element,
            change_set_id=request.change_set_id,
            authorization_id=response["authorization_id"],
            operation_count=len(response["operations"]),
            persist_requested=request.persist_requested,
        )
        return response

    def process_apply_result(self, payload: Any, token: str) -> dict[str, Any]:
        if not hmac.compare_digest(token or "", self.config.session.token):
            raise AuthenticationError("invalid bridge token")
        request = ApplyResultRequest.from_mapping(payload)
        self._assert_bound_session(
            request.session.bridge_session_id,
            request.session.process_id,
            request.session.scope,
        )
        with self._assistant_lock:
            response = self._changes.record_result(request)
        with self._metrics_lock:
            self._accepted_apply_result_count += 1
        self._audit.append(
            "apply.result",
            request_id=request.request_id,
            process_id=request.session.process_id,
            scope=request.session.scope.to_dict(),
            target_element=request.target_element,
            change_set_id=request.change_set_id,
            authorization_id=request.authorization_id,
            execution_status=request.status,
            persistence=request.persistence,
            operation_count=len(request.operation_results),
        )
        return response

    def _assert_bound_session(
        self, bridge_session_id: str, process_id: int, scope: ScopeKey
    ) -> None:
        if bridge_session_id != self.config.session.bridge_session_id:
            raise ProtocolError("bridge_session_id does not match the active gateway")
        if process_id != self.config.session.target_process_id:
            raise ProtocolError("process_id does not match the target E3D process")
        self.config.session.scope.assert_matches(scope)


class BridgeRequestHandler(BaseHTTPRequestHandler):
    """HTTP adapter; the server injects ``service`` before serving."""

    service: BridgeService
    server_version = "E3DLiveBridge/0.3"

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path != "/health":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        if self.client_address[0] not in {"127.0.0.1", "::1"}:
            self._send_json(HTTPStatus.FORBIDDEN, {"error": "loopback clients only"})
            return
        token = self.headers.get(TOKEN_HEADER, "")
        if not hmac.compare_digest(token or "", self.service.config.session.token):
            self._send_json(HTTPStatus.UNAUTHORIZED, {"error": "invalid bridge token"})
            return
        try:
            health = self.service.health()
        except Exception:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "internal gateway failure"},
            )
            return
        self._send_json(HTTPStatus.OK, health)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path not in {
            "/v1/selection",
            "/v1/preview",
            "/v1/configure/assistant",
            "/v1/configure/openai",
            "/v1/apply/authorize",
            "/v1/apply/result",
        }:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        if self.client_address[0] not in {"127.0.0.1", "::1"}:
            self._send_json(HTTPStatus.FORBIDDEN, {"error": "loopback clients only"})
            return
        if self.headers.get_content_type() != "application/json":
            self._send_json(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                {"error": "Content-Type must be application/json"},
            )
            return

        try:
            content_length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid Content-Length"})
            return
        if content_length <= 0 or content_length > self.service.config.max_request_bytes:
            self._send_json(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                {"error": "request body is empty or too large"},
            )
            return

        try:
            body = self.rfile.read(content_length)
            payload = json.loads(body.decode("utf-8"))
            token = self.headers.get(TOKEN_HEADER, "")
            if self.path == "/v1/selection":
                response = self.service.process_selection(payload, token)
            elif self.path == "/v1/preview":
                response = self.service.process_preview(payload, token)
            elif self.path == "/v1/configure/assistant":
                response = self.service.configure_assistant(payload, token)
            elif self.path == "/v1/configure/openai":
                response = self.service.configure_openai(payload, token)
            elif self.path == "/v1/apply/authorize":
                response = self.service.process_authorization(payload, token)
            else:
                response = self.service.process_apply_result(payload, token)
        except AuthenticationError as exc:
            self._send_json(HTTPStatus.UNAUTHORIZED, {"error": str(exc)})
            return
        except (ProtocolError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        except OpenAIBackendError as exc:
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": str(exc)})
            return
        except Exception:
            # Keep unexpected failures inside the request thread and do not
            # reflect provider bodies, credentials, or project data.
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "internal gateway failure"},
            )
            return

        self._send_json(HTTPStatus.OK, response)

    def _send_json(self, status: HTTPStatus, payload: Any) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def create_server(
    service: BridgeService,
    *,
    host: str = "127.0.0.1",
    port: int = DEFAULT_PORT,
) -> ThreadingHTTPServer:
    if host not in {"127.0.0.1", "::1"}:
        raise ValueError("the live bridge may bind only to a loopback address")

    handler = type(
        "ConfiguredBridgeRequestHandler",
        (BridgeRequestHandler,),
        {"service": service},
    )
    server = ThreadingHTTPServer((host, port), handler)
    server.daemon_threads = True
    return server


def start_target_process_watchdog(
    server: ThreadingHTTPServer,
    target_process_id: int,
    *,
    poll_seconds: float = 1.0,
) -> threading.Thread:
    """Stop the gateway when the exact target process exits.

    Windows keeps a handle to the original process object, so a later PID reuse
    cannot keep a stale gateway alive. The polling fallback is used only on
    non-Windows development hosts.
    """
    if target_process_id <= 0 or poll_seconds <= 0:
        raise ValueError("watchdog inputs must be positive")

    if os.name == "nt":
        import ctypes
        from ctypes import wintypes

        synchronize = 0x00100000
        wait_object_0 = 0x00000000
        infinite = 0xFFFFFFFF
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel32.WaitForSingleObject.restype = wintypes.DWORD
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL
        process_handle = kernel32.OpenProcess(
            synchronize, False, target_process_id
        )
        if not process_handle:
            error_code = ctypes.get_last_error()
            raise RuntimeError(
                f"cannot monitor target E3D PID {target_process_id} "
                f"(Windows error {error_code})"
            )

        def watch() -> None:
            try:
                if kernel32.WaitForSingleObject(process_handle, infinite) == wait_object_0:
                    server.shutdown()
            finally:
                kernel32.CloseHandle(process_handle)

    else:
        try:
            os.kill(target_process_id, 0)
        except OSError as exc:
            raise RuntimeError(
                f"cannot monitor target process {target_process_id}"
            ) from exc

        def watch() -> None:
            while True:
                time.sleep(poll_seconds)
                try:
                    os.kill(target_process_id, 0)
                except OSError:
                    server.shutdown()
                    return

    thread = threading.Thread(
        target=watch,
        name=f"e3d-target-watchdog-{target_process_id}",
        daemon=True,
    )
    thread.start()
    return thread


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Start the PID- and scope-bound E3D live gateway."
    )
    parser.add_argument("--project-code", required=True)
    parser.add_argument("--mdb", required=True)
    parser.add_argument("--module", default="DESIGN")
    parser.add_argument("--target-e3d-pid", required=True, type=int)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument(
        "--assistant-backend",
        choices=("local", "openai"),
        default="local",
    )
    parser.add_argument("--openai-model")
    parser.add_argument(
        "--access-mode",
        choices=tuple(sorted(ACCESS_MODES)),
        default=ACCESS_MODE_CONTROLLED_WRITE,
    )
    parser.add_argument(
        "--allow-external-ai",
        action="store_true",
        help="Explicitly allow scoped selection data to be sent to OpenAI.",
    )
    parser.add_argument(
        "--session-root",
        type=Path,
        default=default_session_root(),
        help="Directory for PID-specific ephemeral Add-in session files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    if args.target_e3d_pid <= 0:
        raise SystemExit("--target-e3d-pid must be a positive integer")
    scope = ScopeKey.create(args.project_code, args.mdb, args.module)
    gateway_url = f"http://127.0.0.1:{args.port}/"
    live_session = LiveSession.create(
        scope,
        gateway_url,
        args.target_e3d_pid,
        access_mode=args.access_mode,
    )
    assistant: Any = ReadOnlyAssistant()
    if args.assistant_backend == "openai":
        if not args.allow_external_ai:
            raise SystemExit(
                "--assistant-backend openai requires --allow-external-ai"
            )
        assistant = OpenAIPreviewAssistant(
            OpenAIBackendConfig.from_environment(
                model=args.openai_model or DEFAULT_OPENAI_MODEL
            )
        )
    session_file = default_session_file(args.target_e3d_pid, args.session_root)
    audit_path = (
        args.session_root.parent
        / "audit"
        / scope.partition_id
        / f"{live_session.bridge_session_id}.jsonl"
    )
    service = BridgeService(
        GatewayConfig(
            session=live_session,
            openai_model=args.openai_model or DEFAULT_OPENAI_MODEL,
            audit_log=AuditLog(audit_path),
        ),
        assistant=assistant,
    )
    server = create_server(service, port=args.port)

    try:
        start_target_process_watchdog(server, args.target_e3d_pid)
    except RuntimeError as exc:
        server.server_close()
        raise SystemExit(str(exc)) from exc

    write_session_file(live_session, session_file)
    print(
        f"E3D live bridge started in {live_session.access_mode.upper()} mode\n"
        f"  endpoint: {gateway_url}\n"
        f"  scope:    {scope.project_code}/{scope.mdb}/{scope.module}\n"
        f"  E3D PID:  {live_session.target_process_id}\n"
        f"  backend:  {assistant.backend_name}"
        f"{f' / {assistant.model_name}' if assistant.model_name else ''}\n"
        f"  session:  {live_session.bridge_session_id}\n"
        f"  config:   {session_file.expanduser().resolve()}"
    )
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        print("\nE3D live bridge stopping")
    finally:
        server.server_close()
        remove_session_file(live_session, session_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
