"""Isolated OpenAI and OpenAI-compatible preview backends.

Both adapters produce a typed preview only. Their output is parsed and then
revalidated by :mod:`preview` before any ChangeSet can reach the E3D Add-in.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any, Callable
from urllib.parse import urlsplit

from .preview import ChangePreview, ChangePreviewRequest, openai_output_schema
from .protocol import ProtocolError


ISOLATED_API_KEY_ENV = "E3D_LIVE_OPENAI_API_KEY"
DEFAULT_OPENAI_MODEL = "gpt-5.4-2026-03-05"
TOKEN_RHYTHM_BASE_URL = "https://tokenrhythm.studio/v1"
DEFAULT_TOKEN_RHYTHM_MODEL = "deepseek-v4-flash"
PROVIDER_OPENAI_RESPONSES = "openai_responses"
PROVIDER_TOKEN_RHYTHM_CHAT = "token_rhythm_chat"
ASSISTANT_PROVIDERS = frozenset(
    {PROVIDER_OPENAI_RESPONSES, PROVIDER_TOKEN_RHYTHM_CHAT}
)
MAX_RESPONSE_BYTES = 1_048_576


class OpenAIBackendError(RuntimeError):
    """Raised when an explicitly enabled external preview request fails."""


def _clean_api_key(api_key: str) -> str:
    cleaned = (api_key or "").strip()
    if not cleaned or cleaned in {"YOUR_API_KEY", "sk_xxx"}:
        raise OpenAIBackendError("an API key is required")
    if len(cleaned) > 512:
        raise OpenAIBackendError("the API key exceeds the local size limit")
    return cleaned


def _clean_model(model: str, *, default: str) -> str:
    cleaned = (model or "").strip() or default
    if cleaned == "MODEL_ID":
        raise OpenAIBackendError("MODEL_ID is a placeholder, not a model name")
    if len(cleaned) > 128 or any(character.isspace() for character in cleaned):
        raise OpenAIBackendError("the model ID is invalid")
    return cleaned


def _clean_base_url(base_url: str) -> str:
    cleaned = (base_url or "").strip().rstrip("/")
    parts = urlsplit(cleaned)
    if (
        parts.scheme != "https"
        or parts.username is not None
        or parts.password is not None
        or parts.query
        or parts.fragment
    ):
        raise OpenAIBackendError("the compatible API base URL must be a clean HTTPS URL")
    if cleaned != TOKEN_RHYTHM_BASE_URL:
        raise OpenAIBackendError("the selected provider profile has an unexpected base URL")
    return cleaned


def _safe_failure(prefix: str, exc: Exception, api_key: str) -> OpenAIBackendError:
    # SDK exceptions should not contain request headers. Redact defensively in
    # case an upstream service reflects credentials in a response message.
    detail = str(exc).replace(api_key, "[REDACTED]")[:1000]
    return OpenAIBackendError(f"{prefix} ({type(exc).__name__}): {detail}")


def _bounded_mapping(value: Any, provider_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise OpenAIBackendError(f"{provider_name} response must be a JSON object")
    encoded_size = len(json.dumps(value, separators=(",", ":")).encode("utf-8"))
    if encoded_size > MAX_RESPONSE_BYTES:
        raise OpenAIBackendError(f"{provider_name} response exceeds the local size limit")
    return value


@dataclass(frozen=True)
class OpenAIBackendConfig:
    api_key: str
    model: str = DEFAULT_OPENAI_MODEL
    timeout_seconds: float = 60.0
    max_retries: int = 3

    @classmethod
    def from_environment(
        cls, *, model: str = DEFAULT_OPENAI_MODEL
    ) -> "OpenAIBackendConfig":
        api_key = os.environ.get(ISOLATED_API_KEY_ENV, "").strip()
        if not api_key:
            raise OpenAIBackendError(
                f"{ISOLATED_API_KEY_ENV} is required for the OpenAI backend"
            )
        return cls.from_api_key(api_key, model=model)

    @classmethod
    def from_api_key(
        cls, api_key: str, *, model: str = DEFAULT_OPENAI_MODEL
    ) -> "OpenAIBackendConfig":
        return cls(
            api_key=_clean_api_key(api_key),
            model=_clean_model(model, default=DEFAULT_OPENAI_MODEL),
        )


@dataclass(frozen=True)
class OpenAICompatibleChatConfig:
    api_key: str
    model: str = DEFAULT_TOKEN_RHYTHM_MODEL
    base_url: str = TOKEN_RHYTHM_BASE_URL
    timeout_seconds: float = 60.0
    max_retries: int = 3

    @classmethod
    def from_api_key(
        cls,
        api_key: str,
        *,
        model: str = DEFAULT_TOKEN_RHYTHM_MODEL,
        base_url: str = TOKEN_RHYTHM_BASE_URL,
    ) -> "OpenAICompatibleChatConfig":
        return cls(
            api_key=_clean_api_key(api_key),
            model=_clean_model(model, default=DEFAULT_TOKEN_RHYTHM_MODEL),
            base_url=_clean_base_url(base_url),
        )

    @property
    def endpoint_origin(self) -> str:
        parts = urlsplit(self.base_url)
        return f"{parts.scheme}://{parts.netloc}"


def _post_responses(
    config: OpenAIBackendConfig, payload: dict[str, Any]
) -> dict[str, Any]:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise OpenAIBackendError(
            "the pinned OpenAI SDK is not installed; run install_runtime.ps1"
        ) from exc

    try:
        client = OpenAI(
            api_key=config.api_key,
            timeout=config.timeout_seconds,
            max_retries=config.max_retries,
        )
        value = client.responses.create(**payload).model_dump(mode="json")
    except Exception as exc:
        raise _safe_failure("OpenAI Responses request failed", exc, config.api_key) from exc
    return _bounded_mapping(value, "OpenAI")


def _post_chat_completions(
    config: OpenAICompatibleChatConfig, payload: dict[str, Any]
) -> dict[str, Any]:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise OpenAIBackendError(
            "the pinned OpenAI SDK is not installed; run install_runtime.ps1"
        ) from exc

    try:
        client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout_seconds,
            max_retries=config.max_retries,
        )
        value = client.chat.completions.create(**payload).model_dump(mode="json")
    except Exception as exc:
        raise _safe_failure(
            "OpenAI-compatible Chat Completions request failed", exc, config.api_key
        ) from exc
    return _bounded_mapping(value, "OpenAI-compatible")


def _extract_responses_output_text(response: dict[str, Any]) -> str:
    direct = response.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct
    for item in response.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                text = content.get("text")
                if isinstance(text, str) and text.strip():
                    return text
    raise OpenAIBackendError("OpenAI response did not contain output_text")


def _extract_chat_output_text(response: dict[str, Any]) -> str:
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) != 1:
        raise OpenAIBackendError(
            "OpenAI-compatible response must contain exactly one choice"
        )
    choice = choices[0]
    message = choice.get("message") if isinstance(choice, dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, str) or not content.strip():
        raise OpenAIBackendError(
            "OpenAI-compatible response did not contain message content"
        )
    return content


def _external_input(request: ChangePreviewRequest) -> dict[str, Any]:
    return {
        "scope": request.envelope.scope.to_dict(),
        "instruction": request.instruction,
        "selection": request.envelope.selection.to_dict(),
    }


PREVIEW_INSTRUCTIONS = (
    "Produce a preview-only AVEVA E3D attribute change proposal. "
    "Use only the supplied selection snapshot and instruction. "
    "Do not invent project facts. Return no operations when evidence is insufficient. "
    "Every operation must preserve the exact target and expected current value from "
    "the snapshot. Only attributes permitted by the supplied schema may be proposed. "
    "The operator and E3D Add-in independently revalidate every operation before "
    "execution."
)


def _validated_preview(
    text: str, *, request: ChangePreviewRequest, provider_name: str
) -> ChangePreview:
    try:
        output = json.loads(text)
    except json.JSONDecodeError as exc:
        raise OpenAIBackendError(
            f"{provider_name} structured output was not valid JSON"
        ) from exc
    try:
        return ChangePreview.from_mapping(output, request=request)
    except ProtocolError as exc:
        raise OpenAIBackendError(
            f"{provider_name} preview failed local validation: {exc}"
        ) from exc


class OpenAIPreviewAssistant:
    backend_name = PROVIDER_OPENAI_RESPONSES
    endpoint_origin = "https://api.openai.com"

    def __init__(
        self,
        config: OpenAIBackendConfig,
        *,
        sender: Callable[
            [OpenAIBackendConfig, dict[str, Any]], dict[str, Any]
        ] = _post_responses,
    ) -> None:
        self.config = config
        self._sender = sender

    @property
    def model_name(self) -> str:
        return self.config.model

    def preview(self, request: ChangePreviewRequest) -> ChangePreview:
        payload = {
            "model": self.config.model,
            "store": False,
            "max_output_tokens": 3000,
            "instructions": PREVIEW_INSTRUCTIONS,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": json.dumps(_external_input(request), sort_keys=True),
                        }
                    ],
                }
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "e3d_change_preview",
                    "strict": True,
                    "schema": openai_output_schema(),
                }
            },
        }
        response = self._sender(self.config, payload)
        return _validated_preview(
            _extract_responses_output_text(response),
            request=request,
            provider_name="OpenAI",
        )


class OpenAICompatibleChatPreviewAssistant:
    backend_name = PROVIDER_TOKEN_RHYTHM_CHAT

    def __init__(
        self,
        config: OpenAICompatibleChatConfig,
        *,
        sender: Callable[
            [OpenAICompatibleChatConfig, dict[str, Any]], dict[str, Any]
        ] = _post_chat_completions,
    ) -> None:
        self.config = config
        self._sender = sender

    @property
    def model_name(self) -> str:
        return self.config.model

    @property
    def endpoint_origin(self) -> str:
        return self.config.endpoint_origin

    def preview(self, request: ChangePreviewRequest) -> ChangePreview:
        schema = json.dumps(openai_output_schema(), sort_keys=True)
        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        PREVIEW_INSTRUCTIONS
                        + " Return exactly one JSON object and no markdown. JSON schema: "
                        + schema
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(_external_input(request), sort_keys=True),
                },
            ],
            "max_tokens": 3000,
            "stream": False,
        }
        response = self._sender(self.config, payload)
        return _validated_preview(
            _extract_chat_output_text(response),
            request=request,
            provider_name="OpenAI-compatible",
        )
