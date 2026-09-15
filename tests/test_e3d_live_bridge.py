from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
import types
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from integrations.e3d_live.gateway import (
    BridgeService,
    GatewayConfig,
    create_server,
    start_target_process_watchdog,
)
from integrations.e3d_live.apply import PendingChangeRegistry
from integrations.e3d_live.audit import AuditLog
from integrations.e3d_live.openai_backend import (
    DEFAULT_TOKEN_RHYTHM_MODEL,
    TOKEN_RHYTHM_BASE_URL,
    OpenAIBackendConfig,
    OpenAIBackendError,
    OpenAICompatibleChatConfig,
    OpenAICompatibleChatPreviewAssistant,
    OpenAIPreviewAssistant,
)
from integrations.e3d_live.preview import (
    PREVIEW_ATTRIBUTE_ALLOWLIST,
    ChangePreview,
    ChangePreviewRequest,
    openai_output_schema,
)
from integrations.e3d_live.protocol import (
    ATTRIBUTE_ALLOWLIST,
    PROTOCOL_VERSION,
    ProtocolError,
    ScopeKey,
)
from integrations.e3d_live.session import (
    ACCESS_MODE_CONTROLLED_WRITE,
    LiveSession,
    default_session_file,
    remove_session_file,
    write_session_file,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_ROOT = REPO_ROOT / "integrations" / "e3d_live"


def _payload(session: LiveSession, *, scope: ScopeKey | None = None) -> dict:
    selected_scope = scope or session.scope
    return {
        "protocol_version": PROTOCOL_VERSION,
        "message_type": "selection_snapshot",
        "request_id": "request-1",
        "timestamp_utc": "2026-08-20T12:00:00Z",
        "session": {
            "bridge_session_id": session.bridge_session_id,
            "process_id": session.target_process_id,
            "source": "e3d-caf-addin",
            "addin_version": "0.1.0",
            "scope": selected_scope.to_dict(),
        },
        "selection": {
            "full_name": "/P1501B/BASE/STAY01",
            "element_type": "PYRAMID",
            "owner_full_name": "/P1501B/BASE",
            "attributes": {
                "HEIG": "37mm",
                "POS": "E 0 N 0 U -236",
            },
        },
    }


def _preview_payload(session: LiveSession, instruction: str = "Set height to 45mm") -> dict:
    payload = _payload(session)
    payload["message_type"] = "change_preview_request"
    payload["instruction"] = instruction
    return payload


def _valid_preview_mapping(session: LiveSession) -> dict:
    return {
        "summary": "One typed height change is proposed.",
        "observations": ["The captured HEIG is 37mm."],
        "warnings": ["Preview only; verify geometry before execution."],
        "operations": [
            {
                "operation_id": "op-1",
                "operation_type": "set_attribute",
                "target_element": "/P1501B/BASE/STAY01",
                "attribute": "HEIG",
                "expected_current_value": "37mm",
                "proposed_value": "45mm",
                "reason": "Requested by the operator.",
            }
        ],
    }


def _session() -> LiveSession:
    return LiveSession(
        bridge_session_id="bridge-session-1",
        token="test-token",
        gateway_url="http://127.0.0.1:48731/",
        scope=ScopeKey.create("APS", "/ALL", "DESIGN"),
        target_process_id=4100,
    )


def _write_session() -> LiveSession:
    return LiveSession(
        bridge_session_id="bridge-session-write-1",
        token="write-test-token",
        gateway_url="http://127.0.0.1:48731/",
        scope=ScopeKey.create("APS", "/ALL", "DESIGN"),
        target_process_id=4100,
        access_mode=ACCESS_MODE_CONTROLLED_WRITE,
    )


class _DeterministicPreviewAssistant:
    backend_name = "deterministic_test"
    model_name = "test-model"

    def preview(self, request: ChangePreviewRequest) -> ChangePreview:
        return ChangePreview.from_mapping(
            _valid_preview_mapping(_write_session()),
            request=request,
        )


def test_scope_normalisation_and_partitioning_are_deterministic() -> None:
    first = ScopeKey.create("aps", "/all", "design")
    second = ScopeKey.create("APS", "ALL", "DESIGN")
    unrelated = ScopeKey.create("ACP", "ALL", "DESIGN")

    assert first == second
    assert first.partition_id == second.partition_id
    assert first.partition_id != unrelated.partition_id


def test_read_only_service_accepts_only_the_bound_scope_and_session() -> None:
    session = _session()
    service = BridgeService(GatewayConfig(session=session))

    response = service.process_selection(_payload(session), session.token)
    assert response["status"] == "read_only"
    assert response["changes"] == []
    assert response["persistence"] == "none"
    assert service.health()["accepted_selection_count"] == 1
    assert service.health()["last_request_id"] == "request-1"

    with pytest.raises(ProtocolError, match="scope mismatch"):
        service.process_selection(
            _payload(session, scope=ScopeKey.create("ACP", "ALL", "DESIGN")),
            session.token,
        )

    wrong_session = _payload(session)
    wrong_session["session"]["bridge_session_id"] = "old-session"
    with pytest.raises(ProtocolError, match="bridge_session_id"):
        service.process_selection(wrong_session, session.token)

    wrong_process = _payload(session)
    wrong_process["session"]["process_id"] = 4200
    with pytest.raises(ProtocolError, match="target E3D process"):
        service.process_selection(wrong_process, session.token)


def test_protocol_rejects_unsolicited_context_and_non_allowlisted_attributes() -> None:
    session = _session()
    service = BridgeService(GatewayConfig(session=session))

    polluted = _payload(session)
    polluted["project_context"] = {"source": "another-module"}
    with pytest.raises(ProtocolError, match="unsupported fields"):
        service.process_selection(polluted, session.token)

    non_allowlisted = _payload(session)
    non_allowlisted["selection"]["attributes"]["FOREIGN_CONTEXT"] = "blocked"
    with pytest.raises(ProtocolError, match="not in the bridge allowlist"):
        service.process_selection(non_allowlisted, session.token)


def test_local_change_preview_is_typed_non_executable_and_empty() -> None:
    session = _session()
    service = BridgeService(GatewayConfig(session=session))

    response = service.process_preview(_preview_payload(session), session.token)
    assert response["status"] == "preview_ready"
    assert response["mode"] == "preview_only"
    assert response["change_set"]["executable"] is False
    assert response["change_set"]["requires_user_approval"] is True
    assert response["change_set"]["operations"] == []
    assert response["changes"] == []
    assert response["persistence"] == "not_applied"
    assert service.health()["accepted_preview_count"] == 1


def test_change_preview_rejects_cross_element_and_stale_preconditions() -> None:
    session = _session()
    request = ChangePreviewRequest.from_mapping(_preview_payload(session))

    cross_element = _valid_preview_mapping(session)
    cross_element["operations"][0]["target_element"] = "/OTHER"
    with pytest.raises(ProtocolError, match="selected element"):
        ChangePreview.from_mapping(cross_element, request=request)

    stale = _valid_preview_mapping(session)
    stale["operations"][0]["expected_current_value"] = "38mm"
    with pytest.raises(ProtocolError, match="captured snapshot"):
        ChangePreview.from_mapping(stale, request=request)

    unsafe_attribute = _valid_preview_mapping(session)
    unsafe_attribute["operations"][0]["attribute"] = "CATR"
    with pytest.raises(ProtocolError, match="execution-allowlisted"):
        ChangePreview.from_mapping(unsafe_attribute, request=request)


def test_openai_backend_uses_structured_stateless_output_and_local_validation() -> None:
    session = _session()
    captured: dict = {}

    def fake_sender(config: OpenAIBackendConfig, payload: dict) -> dict:
        captured.update(payload)
        return {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {
                            "type": "output_text",
                            "text": json.dumps(_valid_preview_mapping(session)),
                        }
                    ],
                }
            ]
        }

    assistant = OpenAIPreviewAssistant(
        OpenAIBackendConfig(api_key="not-sent-in-test", model="explicit-test-model"),
        sender=fake_sender,
    )
    service = BridgeService(GatewayConfig(session=session), assistant=assistant)
    response = service.process_preview(_preview_payload(session), session.token)

    assert captured["store"] is False
    assert captured["text"]["format"]["type"] == "json_schema"
    assert captured["text"]["format"]["strict"] is True
    assert session.token not in json.dumps(captured)
    assert session.bridge_session_id not in json.dumps(captured)
    assert response["backend"] == {
        "kind": "openai_responses",
        "model": "explicit-test-model",
    }
    assert len(response["change_set"]["operations"]) == 1
    assert response["change_set"]["executable"] is False
    assert response["changes"] == []


def test_openai_backend_rejects_unvalidated_model_output() -> None:
    session = _session()

    def fake_sender(config: OpenAIBackendConfig, payload: dict) -> dict:
        invalid = _valid_preview_mapping(session)
        invalid["operations"][0]["target_element"] = "/FOREIGN/PROJECT/ELEMENT"
        return {"output_text": json.dumps(invalid)}

    assistant = OpenAIPreviewAssistant(
        OpenAIBackendConfig(api_key="not-sent-in-test", model="explicit-test-model"),
        sender=fake_sender,
    )
    service = BridgeService(GatewayConfig(session=session), assistant=assistant)
    with pytest.raises(OpenAIBackendError, match="local validation"):
        service.process_preview(_preview_payload(session), session.token)


def test_loopback_http_contract_requires_token_and_returns_no_changes() -> None:
    session = _session()
    service = BridgeService(GatewayConfig(session=session))
    server = create_server(service, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    try:
        unauthorized_health = Request(
            f"http://127.0.0.1:{port}/health",
            method="GET",
        )
        with pytest.raises(HTTPError) as health_error:
            urlopen(unauthorized_health, timeout=2)
        assert health_error.value.code == 401

        authorized_health = Request(
            f"http://127.0.0.1:{port}/health",
            method="GET",
            headers={"X-E3D-Live-Token": session.token},
        )
        with urlopen(authorized_health, timeout=2) as response:
            health = json.loads(response.read().decode("utf-8"))
        assert health["bridge_session_id"] == session.bridge_session_id

        body = json.dumps(_payload(session)).encode("utf-8")
        request = Request(
            f"http://127.0.0.1:{port}/v1/selection",
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-E3D-Live-Token": session.token,
            },
        )
        with urlopen(request, timeout=2) as response:
            result = json.loads(response.read().decode("utf-8"))
        assert result["status"] == "read_only"
        assert result["changes"] == []

        preview_request = Request(
            f"http://127.0.0.1:{port}/v1/preview",
            data=json.dumps(_preview_payload(session)).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-E3D-Live-Token": session.token,
            },
        )
        with urlopen(preview_request, timeout=2) as response:
            preview = json.loads(response.read().decode("utf-8"))
        assert preview["mode"] == "preview_only"
        assert preview["change_set"]["executable"] is False
        assert preview["changes"] == []

        configuration_payload = {
            "protocol_version": PROTOCOL_VERSION,
            "message_type": "configure_assistant",
            "bridge_session_id": session.bridge_session_id,
            "process_id": session.target_process_id,
            "scope": session.scope.to_dict(),
            "provider": "token_rhythm_chat",
            "model": "",
            "api_key": "sk-http-test",
        }
        configure_request = Request(
            f"http://127.0.0.1:{port}/v1/configure/assistant",
            data=json.dumps(configuration_payload).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-E3D-Live-Token": session.token,
            },
        )
        with urlopen(configure_request, timeout=2) as response:
            configured = json.loads(response.read().decode("utf-8"))
        assert configured["backend"] == "token_rhythm_chat"
        assert configured["model"] == DEFAULT_TOKEN_RHYTHM_MODEL
        assert "sk-http-test" not in json.dumps(configured)

        unauthorized = Request(
            f"http://127.0.0.1:{port}/v1/selection",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with pytest.raises(HTTPError) as error:
            urlopen(unauthorized, timeout=2)
        assert error.value.code == 401
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_target_process_watchdog_notifies_gateway_when_original_process_exits() -> None:
    class FakeServer:
        def __init__(self) -> None:
            self.shutdown_called = threading.Event()

        def shutdown(self) -> None:
            self.shutdown_called.set()

    child = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(0.2)"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    fake_server = FakeServer()
    watchdog = start_target_process_watchdog(fake_server, child.pid)
    child.wait(timeout=3)
    assert fake_server.shutdown_called.wait(timeout=3)
    watchdog.join(timeout=3)
    assert not watchdog.is_alive()


def test_unexpected_request_failure_is_sanitized_and_server_stays_healthy() -> None:
    session = _session()

    class FailingAssistant:
        backend_name = "failing_test"
        model_name = "test-model"

        def preview(self, request: ChangePreviewRequest) -> ChangePreview:
            raise RuntimeError("sensitive-internal-detail")

    service = BridgeService(
        GatewayConfig(session=session), assistant=FailingAssistant()
    )
    server = create_server(service, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    try:
        request = Request(
            f"http://127.0.0.1:{port}/v1/preview",
            data=json.dumps(_preview_payload(session)).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-E3D-Live-Token": session.token,
            },
        )
        with pytest.raises(HTTPError) as failure:
            urlopen(request, timeout=2)
        assert failure.value.code == 500
        body = failure.value.read().decode("utf-8")
        assert "internal gateway failure" in body
        assert "sensitive-internal-detail" not in body

        health_request = Request(
            f"http://127.0.0.1:{port}/health",
            headers={"X-E3D-Live-Token": session.token},
        )
        with urlopen(health_request, timeout=2) as response:
            assert json.loads(response.read().decode("utf-8"))["status"] == "ok"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_session_file_is_ephemeral_and_owner_checked(tmp_path: Path) -> None:
    path = tmp_path / "session.json"
    session = _session()
    write_session_file(session, path)
    written = json.loads(path.read_text(encoding="utf-8"))
    assert written["scope"] == session.scope.to_dict()
    assert written["target_process_id"] == session.target_process_id
    assert written["access_mode"] == "read_only"
    assert written["write_enabled"] is False

    other = LiveSession(
        bridge_session_id=session.bridge_session_id,
        token="other-token",
        gateway_url=session.gateway_url,
        scope=session.scope,
        target_process_id=4200,
    )
    remove_session_file(other, path)
    assert path.exists()
    remove_session_file(session, path)
    assert not path.exists()


def test_default_session_files_are_partitioned_by_e3d_process(tmp_path: Path) -> None:
    first = default_session_file(4100, tmp_path)
    second = default_session_file(4200, tmp_path)
    assert first == tmp_path / "4100.json"
    assert second == tmp_path / "4200.json"
    assert first != second


def test_python_bridge_has_no_cross_project_imports() -> None:
    python_sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in MODULE_ROOT.glob("*.py")
    )
    forbidden = (
        "from agent",
        "import agent",
        "from memory",
        "import memory",
        "from wsb",
        "import wsb",
        "Projects/",
        "Projects\\",
    )
    for pattern in forbidden:
        assert pattern not in python_sources


def test_caf_addin_source_confines_controlled_writes_to_the_executor() -> None:
    addin_sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (MODULE_ROOT / "addin").glob("*.cs")
    )
    for forbidden_call in (
        "element.Create(",
        "element.Delete(",
        ".CreateAfter(",
        ".CreateBefore(",
    ):
        assert forbidden_call not in addin_sources
    executor = (MODULE_ROOT / "addin" / "ControlledChangeExecutor.cs").read_text(
        encoding="utf-8"
    )
    non_executor_sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (MODULE_ROOT / "addin").glob("*.cs")
        if path.name != "ControlledChangeExecutor.cs"
    )
    assert ".SetAttribute(" in executor
    assert ".SetAttribute(" not in non_executor_sources
    assert "StartTransaction(" in executor
    assert "EndTransaction()" in executor
    assert "AbortTransaction()" in executor
    assert "GetAsString(" in executor
    assert "MDB.CurrentMDB.SaveWork(" in executor
    assert "authorization.PersistRequested" in executor
    assert "AttributeAllowlist" in addin_sources
    assert "CurrentElement.CurrentElementChanged" in addin_sources
    assert 'Process.GetCurrentProcess().Id.ToString() + ".json"' in addin_sources
    assert "E3D_LIVE_SESSION_FILE" not in addin_sources
    assert "window.Show();" in addin_sources
    assert 'Text = "Preview Changes"' in addin_sources
    assert "PostPreview" in addin_sources
    assert 'Text = "Apply Verified ChangeSet"' in addin_sources
    assert "MessageBox.Show(" in addin_sources
    assert "MessageBoxDefaultButton.Button2" in addin_sources
    assert "UseSystemPasswordChar = true" in addin_sources


def test_attribute_allowlist_is_identical_across_both_processes_and_schema() -> None:
    builder_source = (MODULE_ROOT / "addin" / "SelectionSnapshotBuilder.cs").read_text(
        encoding="utf-8"
    )
    initializer = builder_source.split("AttributeAllowlist", 1)[1].split("};", 1)[0]
    csharp_allowlist = set(re.findall(r'"([A-Z]+)"', initializer))

    schema = json.loads((MODULE_ROOT / "protocol.schema.json").read_text(encoding="utf-8"))
    schema_allowlist = set(
        schema["properties"]["selection"]["properties"]["attributes"][
            "propertyNames"
        ]["enum"]
    )
    assert csharp_allowlist == ATTRIBUTE_ALLOWLIST
    assert schema_allowlist == ATTRIBUTE_ALLOWLIST


def test_preview_allowlist_is_identical_across_runtime_and_contracts() -> None:
    response_schema = json.loads(
        (MODULE_ROOT / "preview-response.schema.json").read_text(encoding="utf-8")
    )
    response_allowlist = set(
        response_schema["$defs"]["operation"]["properties"]["attribute"]["enum"]
    )
    structured_allowlist = set(
        openai_output_schema()["properties"]["operations"]["items"]["properties"][
            "attribute"
        ]["enum"]
    )
    control_schema = json.loads(
        (MODULE_ROOT / "control-protocol.schema.json").read_text(encoding="utf-8")
    )
    result_allowlist = set(
        control_schema["$defs"]["operationResult"]["properties"]["attribute"]["enum"]
    )
    assert response_allowlist == PREVIEW_ATTRIBUTE_ALLOWLIST
    assert structured_allowlist == PREVIEW_ATTRIBUTE_ALLOWLIST
    assert result_allowlist == PREVIEW_ATTRIBUTE_ALLOWLIST
    assert {
        "configureAssistant",
        "configureAssistantResponse",
        "authorizeRequest",
        "authorizeResponse",
        "applyResultRequest",
        "applyResultReceipt",
    }.issubset(control_schema["$defs"])


def test_experiment_launchers_keep_configuration_process_local() -> None:
    deployment = MODULE_ROOT / "deployment"
    launcher = (deployment / "start_test_e3d.ps1").read_text(encoding="utf-8")
    gateway_launcher = (deployment / "start_target_gateway.ps1").read_text(
        encoding="utf-8"
    )

    assert "Start-Process" in launcher
    assert "-WindowStyle Normal" in launcher
    assert "$previousAddinsPath" in launcher
    assert "$previousSessionRoot" in launcher
    assert "SetEnvironmentVariable" not in launcher
    assert "setx" not in launcher.lower()
    assert "Get-Process -Id $TargetE3dPid" in gateway_launcher
    assert "ProcessName, 'des'" in gateway_launcher
    assert "-AllowExternalAI" in gateway_launcher
    assert "--allow-external-ai" in gateway_launcher


def test_deployment_uses_caf_assembly_name_and_copies_dll_beside_xml() -> None:
    deployment_source = (
        MODULE_ROOT / "deployment" / "prepare_deployment.ps1"
    ).read_text(encoding="utf-8")

    assert "Copy-Item -LiteralPath $addinPath -Destination $deployedDll" in deployment_source
    assert "$node.InnerText = $addinAssemblyName" in deployment_source
    assert "$node.InnerText = $addinBasePath" not in deployment_source


def _authorize_payload(
    session: LiveSession, preview_response: dict, *, persist: bool = False
) -> dict:
    change_set = preview_response["change_set"]
    return {
        "protocol_version": PROTOCOL_VERSION,
        "message_type": "apply_authorization_request",
        "request_id": "authorize-1",
        "timestamp_utc": "2026-08-20T12:01:00Z",
        "session": _payload(session)["session"],
        "change_set_id": change_set["change_set_id"],
        "target_element": change_set["target_element"],
        "operation_ids": [item["operation_id"] for item in change_set["operations"]],
        "persist_requested": persist,
    }


def _result_payload(session: LiveSession, authorization: dict) -> dict:
    operation = authorization["operations"][0]
    return {
        "protocol_version": PROTOCOL_VERSION,
        "message_type": "apply_result",
        "request_id": "result-1",
        "timestamp_utc": "2026-08-20T12:02:00Z",
        "session": _payload(session)["session"],
        "authorization_id": authorization["authorization_id"],
        "change_set_id": authorization["change_set_id"],
        "target_element": authorization["target_element"],
        "status": "applied",
        "persistence": "in_memory",
        "message": "verified",
        "operation_results": [
            {
                "operation_id": operation["operation_id"],
                "attribute": operation["attribute"],
                "before_value": operation["expected_current_value"],
                "requested_value": operation["proposed_value"],
                "after_value": operation["proposed_value"],
                "status": "applied",
            }
        ],
    }


def test_controlled_write_preview_authorization_and_result_are_one_scoped_chain() -> None:
    session = _write_session()
    service = BridgeService(
        GatewayConfig(session=session), assistant=_DeterministicPreviewAssistant()
    )

    preview = service.process_preview(_preview_payload(session), session.token)
    assert preview["mode"] == "controlled_write"
    assert preview["change_set"]["executable"] is True
    assert preview["change_set"]["change_set_id"]
    assert preview["persistence"] == "not_applied"

    authorization_payload = _authorize_payload(session, preview)
    authorization = service.process_authorization(
        authorization_payload, session.token
    )
    assert authorization["status"] == "authorized"
    assert authorization["target_element"] == "/P1501B/BASE/STAY01"
    assert authorization["operations"] == preview["change_set"]["operations"]

    duplicate = service.process_authorization(authorization_payload, session.token)
    assert duplicate == authorization

    result_payload = _result_payload(session, authorization)
    receipt = service.process_apply_result(result_payload, session.token)
    assert receipt["status"] == "recorded"
    assert receipt["execution_status"] == "applied"
    assert service.process_apply_result(result_payload, session.token) == receipt

    health = service.health()
    assert health["accepted_preview_count"] == 1
    assert health["accepted_authorization_count"] == 2
    assert health["accepted_apply_result_count"] == 2


def test_controlled_write_rejects_scope_pid_target_and_operation_drift() -> None:
    session = _write_session()
    service = BridgeService(
        GatewayConfig(session=session), assistant=_DeterministicPreviewAssistant()
    )
    preview = service.process_preview(_preview_payload(session), session.token)

    wrong_pid = _authorize_payload(session, preview)
    wrong_pid["session"]["process_id"] = 9999
    with pytest.raises(ProtocolError, match="target E3D process"):
        service.process_authorization(wrong_pid, session.token)

    wrong_target = _authorize_payload(session, preview)
    wrong_target["target_element"] = "/OTHER"
    with pytest.raises(ProtocolError, match="target_element"):
        service.process_authorization(wrong_target, session.token)

    wrong_operations = _authorize_payload(session, preview)
    wrong_operations["operation_ids"] = ["other-operation"]
    with pytest.raises(ProtocolError, match="operation_ids"):
        service.process_authorization(wrong_operations, session.token)

    wrong_scope = _authorize_payload(session, preview)
    wrong_scope["session"]["scope"]["project_code"] = "ACP"
    with pytest.raises(ProtocolError, match="scope mismatch"):
        service.process_authorization(wrong_scope, session.token)


def test_authorization_retry_requires_the_original_request_id() -> None:
    session = _write_session()
    service = BridgeService(
        GatewayConfig(session=session), assistant=_DeterministicPreviewAssistant()
    )
    preview = service.process_preview(_preview_payload(session), session.token)
    authorization_payload = _authorize_payload(session, preview)
    service.process_authorization(authorization_payload, session.token)

    different_retry = json.loads(json.dumps(authorization_payload))
    different_retry["request_id"] = "authorize-different"
    with pytest.raises(ProtocolError, match="different authorization request"):
        service.process_authorization(different_retry, session.token)


def test_partial_rollback_receipt_is_recorded_but_false_applied_receipt_is_rejected() -> None:
    session = _write_session()

    class TwoOperationAssistant:
        backend_name = "two_operation_test"
        model_name = "test-model"

        def preview(self, request: ChangePreviewRequest) -> ChangePreview:
            mapping = _valid_preview_mapping(session)
            mapping["operations"].append(
                {
                    "operation_id": "op-2",
                    "operation_type": "set_attribute",
                    "target_element": "/P1501B/BASE/STAY01",
                    "attribute": "DESC",
                    "expected_current_value": "OLD",
                    "proposed_value": "NEW",
                    "reason": "Requested by the operator.",
                }
            )
            return ChangePreview.from_mapping(mapping, request=request)

    payload = _preview_payload(session)
    payload["selection"]["attributes"]["DESC"] = "OLD"
    service = BridgeService(
        GatewayConfig(session=session), assistant=TwoOperationAssistant()
    )
    preview = service.process_preview(payload, session.token)
    authorization = service.process_authorization(
        _authorize_payload(session, preview), session.token
    )

    rolled_back = _result_payload(session, authorization)
    rolled_back["status"] = "rolled_back"
    rolled_back["persistence"] = "none"
    rolled_back["operation_results"][0]["status"] = "rolled_back"
    receipt = service.process_apply_result(rolled_back, session.token)
    assert receipt["execution_status"] == "rolled_back"

    other_service = BridgeService(
        GatewayConfig(session=session), assistant=_DeterministicPreviewAssistant()
    )
    other_preview = other_service.process_preview(
        _preview_payload(session), session.token
    )
    other_authorization = other_service.process_authorization(
        _authorize_payload(session, other_preview), session.token
    )
    false_applied = _result_payload(session, other_authorization)
    false_applied["operation_results"] = []
    with pytest.raises(ProtocolError, match="verify every operation"):
        other_service.process_apply_result(false_applied, session.token)


def test_terminal_result_retry_rejects_payload_drift() -> None:
    session = _write_session()
    service = BridgeService(
        GatewayConfig(session=session), assistant=_DeterministicPreviewAssistant()
    )
    preview = service.process_preview(_preview_payload(session), session.token)
    authorization = service.process_authorization(
        _authorize_payload(session, preview), session.token
    )
    result = _result_payload(session, authorization)
    service.process_apply_result(result, session.token)

    drifted = json.loads(json.dumps(result))
    drifted["message"] = "different terminal payload"
    with pytest.raises(ProtocolError, match="reused with a different payload"):
        service.process_apply_result(drifted, session.token)


def test_expired_change_set_cannot_be_authorized() -> None:
    session = _write_session()
    now = [datetime(2026, 8, 20, 12, 0, tzinfo=timezone.utc)]
    service = BridgeService(
        GatewayConfig(session=session), assistant=_DeterministicPreviewAssistant()
    )
    service._changes = PendingChangeRegistry(  # noqa: SLF001 - injected test clock
        ttl_seconds=1, clock=lambda: now[0]
    )
    preview = service.process_preview(_preview_payload(session), session.token)
    now[0] += timedelta(seconds=2)
    with pytest.raises(ProtocolError, match="unknown or expired"):
        service.process_authorization(
            _authorize_payload(session, preview), session.token
        )


def test_preview_request_id_is_idempotent_and_conflicts_fail_closed() -> None:
    session = _write_session()
    calls = 0

    def fake_sender(config: OpenAIBackendConfig, payload: dict) -> dict:
        nonlocal calls
        calls += 1
        return {"output_text": json.dumps(_valid_preview_mapping(session))}

    assistant = OpenAIPreviewAssistant(
        OpenAIBackendConfig(api_key="not-sent-in-test", model="test-model"),
        sender=fake_sender,
    )
    service = BridgeService(GatewayConfig(session=session), assistant=assistant)
    payload = _preview_payload(session)
    first = service.process_preview(payload, session.token)
    second = service.process_preview(payload, session.token)
    assert second == first
    assert calls == 1
    assert service.health()["accepted_preview_count"] == 1

    conflict = _preview_payload(session, instruction="Set height to 46mm")
    with pytest.raises(ProtocolError, match="request_id was reused"):
        service.process_preview(conflict, session.token)


def test_parallel_duplicate_preview_makes_one_external_call_and_one_change_set() -> None:
    session = _write_session()
    calls = 0
    calls_lock = threading.Lock()

    def slow_sender(config: OpenAIBackendConfig, payload: dict) -> dict:
        nonlocal calls
        with calls_lock:
            calls += 1
        time.sleep(0.05)
        return {"output_text": json.dumps(_valid_preview_mapping(session))}

    service = BridgeService(
        GatewayConfig(session=session),
        assistant=OpenAIPreviewAssistant(
            OpenAIBackendConfig(api_key="not-sent-in-test", model="test-model"),
            sender=slow_sender,
        ),
    )
    payload = _preview_payload(session)
    with ThreadPoolExecutor(max_workers=12) as pool:
        responses = list(
            pool.map(
                lambda _: service.process_preview(payload, session.token),
                range(40),
            )
        )

    assert calls == 1
    assert all(response == responses[0] for response in responses)
    assert service.health()["accepted_preview_count"] == 1
    assert service.health()["active_change_set_count"] == 1


def test_api_key_configuration_is_memory_only_and_secret_free_in_audit(tmp_path: Path) -> None:
    session = _write_session()
    audit_path = tmp_path / "audit.jsonl"
    service = BridgeService(
        GatewayConfig(session=session, audit_log=AuditLog(audit_path))
    )
    api_key = "sk-test-secret-never-log"
    response = service.configure_assistant(
        {
            "protocol_version": PROTOCOL_VERSION,
            "message_type": "configure_assistant",
            "bridge_session_id": session.bridge_session_id,
            "process_id": session.target_process_id,
            "scope": session.scope.to_dict(),
            "provider": "token_rhythm_chat",
            "model": "",
            "api_key": api_key,
        },
        session.token,
    )
    assert response["status"] == "configured"
    assert response["api_key_persistence"] == "memory_only"
    assert response["model"] == DEFAULT_TOKEN_RHYTHM_MODEL
    assert response["endpoint_origin"] == "https://tokenrhythm.studio"
    assert service.health()["assistant_backend"] == "token_rhythm_chat"
    assert api_key not in audit_path.read_text(encoding="utf-8")


def test_token_rhythm_chat_adapter_uses_model_messages_and_local_validation() -> None:
    session = _write_session()
    captured: dict = {}

    def fake_sender(config: OpenAICompatibleChatConfig, payload: dict) -> dict:
        captured["config"] = config
        captured["payload"] = payload
        return {
            "choices": [
                {"message": {"role": "assistant", "content": json.dumps(
                    _valid_preview_mapping(session)
                )}}
            ]
        }

    assistant = OpenAICompatibleChatPreviewAssistant(
        OpenAICompatibleChatConfig.from_api_key("sk-test", model="glm-5.2"),
        sender=fake_sender,
    )
    preview = assistant.preview(ChangePreviewRequest.from_mapping(_preview_payload(session)))

    assert preview.operations[0].attribute == "HEIG"
    assert captured["config"].base_url == TOKEN_RHYTHM_BASE_URL
    assert captured["payload"]["model"] == "glm-5.2"
    assert captured["payload"]["stream"] is False
    assert [item["role"] for item in captured["payload"]["messages"]] == [
        "system",
        "user",
    ]
    wire_text = json.dumps(captured["payload"], sort_keys=True)
    assert session.token not in wire_text
    assert session.bridge_session_id not in wire_text


def test_token_rhythm_adapter_constructs_the_pinned_sdk_client_and_chat_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _write_session()
    captured: dict = {}

    class FakeResponse:
        def model_dump(self, *, mode: str) -> dict:
            assert mode == "json"
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": json.dumps(_valid_preview_mapping(session)),
                        }
                    }
                ]
            }

    class FakeCompletions:
        def create(self, **payload: object) -> FakeResponse:
            captured["payload"] = payload
            return FakeResponse()

    class FakeOpenAI:
        def __init__(self, **kwargs: object) -> None:
            captured["client"] = kwargs
            self.chat = types.SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setitem(sys.modules, "openai", types.SimpleNamespace(OpenAI=FakeOpenAI))
    assistant = OpenAICompatibleChatPreviewAssistant(
        OpenAICompatibleChatConfig.from_api_key("sk-sdk-test")
    )
    preview = assistant.preview(
        ChangePreviewRequest.from_mapping(_preview_payload(session))
    )

    assert preview.operations[0].proposed_value == "45mm"
    assert captured["client"] == {
        "api_key": "sk-sdk-test",
        "base_url": TOKEN_RHYTHM_BASE_URL,
        "timeout": 60.0,
        "max_retries": 3,
    }
    assert captured["payload"]["model"] == DEFAULT_TOKEN_RHYTHM_MODEL
    assert captured["payload"]["stream"] is False


def test_provider_failure_cannot_reflect_the_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _write_session()
    api_key = "unit-test-key-never-log"

    class FailingCompletions:
        def create(self, **payload: object) -> object:
            raise RuntimeError("provider reflected " + api_key)

    class FakeOpenAI:
        def __init__(self, **kwargs: object) -> None:
            self.chat = types.SimpleNamespace(completions=FailingCompletions())

    monkeypatch.setitem(sys.modules, "openai", types.SimpleNamespace(OpenAI=FakeOpenAI))
    assistant = OpenAICompatibleChatPreviewAssistant(
        OpenAICompatibleChatConfig.from_api_key(api_key)
    )
    with pytest.raises(OpenAIBackendError) as failure:
        assistant.preview(ChangePreviewRequest.from_mapping(_preview_payload(session)))
    assert api_key not in str(failure.value)
    assert "[REDACTED]" in str(failure.value)


def test_token_rhythm_profile_rejects_placeholders_and_endpoint_drift() -> None:
    with pytest.raises(OpenAIBackendError, match="placeholder"):
        OpenAICompatibleChatConfig.from_api_key("sk-test", model="MODEL_ID")
    with pytest.raises(OpenAIBackendError, match="API key"):
        OpenAICompatibleChatConfig.from_api_key("YOUR_API_KEY")
    with pytest.raises(OpenAIBackendError, match="unexpected base URL"):
        OpenAICompatibleChatConfig.from_api_key(
            "sk-test", base_url="https://unrelated.example/v1"
        )
    with pytest.raises(OpenAIBackendError, match="clean HTTPS"):
        OpenAICompatibleChatConfig.from_api_key(
            "sk-test", base_url="http://tokenrhythm.studio/v1"
        )


def test_provider_reconfiguration_revokes_an_in_flight_preview() -> None:
    session = _write_session()
    started = threading.Event()
    release = threading.Event()

    def slow_sender(config: OpenAIBackendConfig, payload: dict) -> dict:
        started.set()
        assert release.wait(timeout=2)
        return {"output_text": json.dumps(_valid_preview_mapping(session))}

    service = BridgeService(
        GatewayConfig(session=session),
        assistant=OpenAIPreviewAssistant(
            OpenAIBackendConfig(api_key="sk-old", model="old-model"),
            sender=slow_sender,
        ),
    )
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(
            service.process_preview, _preview_payload(session), session.token
        )
        assert started.wait(timeout=2)
        service.configure_assistant(
            {
                "protocol_version": PROTOCOL_VERSION,
                "message_type": "configure_assistant",
                "bridge_session_id": session.bridge_session_id,
                "process_id": session.target_process_id,
                "scope": session.scope.to_dict(),
                "provider": "token_rhythm_chat",
                "model": "",
                "api_key": "sk-new",
            },
            session.token,
        )
        release.set()
        with pytest.raises(ProtocolError, match="provider changed"):
            pending.result(timeout=2)
    assert service.health()["active_change_set_count"] == 0


def test_legacy_configure_openai_endpoint_remains_official_provider_compatible() -> None:
    session = _write_session()
    service = BridgeService(GatewayConfig(session=session))
    response = service.configure_openai(
        {
            "protocol_version": PROTOCOL_VERSION,
            "message_type": "configure_openai",
            "bridge_session_id": session.bridge_session_id,
            "process_id": session.target_process_id,
            "scope": session.scope.to_dict(),
            "api_key": "sk-test",
        },
        session.token,
    )
    assert response["backend"] == "openai_responses"
    assert response["model"] == "gpt-5.4-2026-03-05"


def test_parallel_selection_ingress_is_thread_safe() -> None:
    session = _write_session()
    service = BridgeService(GatewayConfig(session=session))

    def send(index: int) -> str:
        payload = _payload(session)
        payload["request_id"] = f"parallel-{index}"
        return service.process_selection(payload, session.token)["status"]

    with ThreadPoolExecutor(max_workers=12) as pool:
        statuses = list(pool.map(send, range(100)))
    assert statuses == ["read_only"] * 100
    assert service.health()["accepted_selection_count"] == 100


def test_phase3_runtime_is_pinned_and_provider_profiles_are_visible_in_e3d_ui() -> None:
    requirements = (MODULE_ROOT / "requirements.txt").read_text(encoding="utf-8")
    launcher = (
        MODULE_ROOT / "deployment" / "start_target_gateway.ps1"
    ).read_text(encoding="utf-8")
    control = (MODULE_ROOT / "addin" / "E3DLiveBridgeControl.cs").read_text(
        encoding="utf-8"
    )
    backend = (MODULE_ROOT / "openai_backend.py").read_text(encoding="utf-8")

    assert "openai==3.3.1" in requirements
    assert "gpt-5.4-2026-03-05" in launcher
    assert "gpt-5.4-2026-03-05" in backend
    assert 'providerCombo.Items.Add("Token Rhythm (Chat Completions)")' in control
    assert 'Text = "https://tokenrhythm.studio/v1"' in control
    assert 'Text = "deepseek-v4-flash"' in control
    assert "UseSystemPasswordChar = true" in control
    assert 'Text = "Configure AI"' in control


def test_robustness_guards_are_present_in_gateway_and_addin_boundaries() -> None:
    gateway = (MODULE_ROOT / "gateway.py").read_text(encoding="utf-8")
    bridge_configuration = (
        MODULE_ROOT / "addin" / "BridgeConfiguration.cs"
    ).read_text(encoding="utf-8")
    addin = (MODULE_ROOT / "addin" / "E3DLiveBridgeAddin.cs").read_text(
        encoding="utf-8"
    )

    assert "_preview_execution_lock" in gateway
    assert "start_target_process_watchdog" in gateway
    assert "WaitForSingleObject" in gateway
    assert 'HTTPStatus.UNAUTHORIZED, {"error": "invalid bridge token"}' in gateway
    assert 'String.Equals(gatewayUri.Host, "127.0.0.1"' in bridge_configuration
    assert 'String.Equals(gatewayUri.AbsolutePath, "/"' in bridge_configuration
    assert "CaptureCurrentSelection(true);" in addin
