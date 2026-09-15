"""Typed, non-executable change previews for the E3D live bridge."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from .protocol import (
    PROTOCOL_VERSION,
    ProtocolError,
    SelectionEnvelope,
    _require_exact_keys,
    _require_mapping,
    _require_string,
)


MESSAGE_CHANGE_PREVIEW_REQUEST = "change_preview_request"
MAX_INSTRUCTION_LENGTH = 4000
MAX_PREVIEW_ITEMS = 16
MAX_PREVIEW_TEXT = 1000
EXECUTABLE_ATTRIBUTE_ALLOWLIST = frozenset(
    {
        "DESC",
        "XLEN",
        "YLEN",
        "ZLEN",
        "HEIG",
        "DIAM",
        "DTOP",
        "DBOT",
    }
)
PREVIEW_ATTRIBUTE_ALLOWLIST = EXECUTABLE_ATTRIBUTE_ALLOWLIST
_NUMERIC_VALUE_RE = re.compile(
    r"^(?P<value>(?:0|[1-9][0-9]*)(?:\.[0-9]+)?)\s*(?P<unit>mm|m)?$",
    re.IGNORECASE,
)
_NUMERIC_ATTRIBUTES = EXECUTABLE_ATTRIBUTE_ALLOWLIST - {"DESC"}


def _validate_proposed_value(attribute: str, value: str, field: str) -> str:
    if attribute == "DESC":
        if len(value) > 256:
            raise ProtocolError(f"{field} exceeds 256 characters for DESC")
        if any(ord(character) < 32 for character in value):
            raise ProtocolError(f"{field} contains control characters")
        return value

    if attribute in _NUMERIC_ATTRIBUTES:
        match = _NUMERIC_VALUE_RE.fullmatch(value)
        if match is None:
            raise ProtocolError(
                f"{field} must be a positive number optionally followed by mm or m"
            )
        magnitude = float(match.group("value"))
        if match.group("unit") and match.group("unit").lower() == "m":
            magnitude *= 1000.0
        if magnitude <= 0.0 or magnitude > 100_000_000.0:
            raise ProtocolError(f"{field} is outside the executable numeric range")
        return value

    raise ProtocolError(f"{field} has no executable value validator")


def _require_string_list(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ProtocolError(f"{field} must be an array")
    if len(value) > MAX_PREVIEW_ITEMS:
        raise ProtocolError(f"{field} exceeds the {MAX_PREVIEW_ITEMS}-item limit")
    return tuple(
        _require_string(item, f"{field}[{index}]", max_length=MAX_PREVIEW_TEXT)
        for index, item in enumerate(value)
    )


@dataclass(frozen=True)
class ChangePreviewRequest:
    envelope: SelectionEnvelope
    instruction: str

    @classmethod
    def from_mapping(cls, value: Any) -> "ChangePreviewRequest":
        data = _require_mapping(value, "message")
        _require_exact_keys(
            data,
            "message",
            {
                "protocol_version",
                "message_type",
                "request_id",
                "timestamp_utc",
                "session",
                "selection",
                "instruction",
            },
        )
        if data.get("message_type") != MESSAGE_CHANGE_PREVIEW_REQUEST:
            raise ProtocolError("message_type must be 'change_preview_request'")

        selection_message = {
            key: data[key]
            for key in (
                "protocol_version",
                "request_id",
                "timestamp_utc",
                "session",
                "selection",
            )
        }
        selection_message["message_type"] = "selection_snapshot"
        return cls(
            envelope=SelectionEnvelope.from_mapping(selection_message),
            instruction=_require_string(
                data.get("instruction"),
                "instruction",
                max_length=MAX_INSTRUCTION_LENGTH,
            ),
        )


@dataclass(frozen=True)
class PreviewOperation:
    operation_id: str
    operation_type: str
    target_element: str
    attribute: str
    expected_current_value: str
    proposed_value: str
    reason: str

    @classmethod
    def from_mapping(
        cls,
        value: Any,
        *,
        request: ChangePreviewRequest,
        index: int,
    ) -> "PreviewOperation":
        field = f"operations[{index}]"
        data = _require_mapping(value, field)
        _require_exact_keys(
            data,
            field,
            {
                "operation_id",
                "operation_type",
                "target_element",
                "attribute",
                "expected_current_value",
                "proposed_value",
                "reason",
            },
        )
        operation_type = _require_string(
            data.get("operation_type"), f"{field}.operation_type", max_length=32
        )
        if operation_type != "set_attribute":
            raise ProtocolError(f"{field}.operation_type must be 'set_attribute'")

        target = _require_string(
            data.get("target_element"), f"{field}.target_element", max_length=1024
        )
        if target != request.envelope.selection.full_name:
            raise ProtocolError(f"{field}.target_element must equal the selected element")

        attribute = _require_string(
            data.get("attribute"), f"{field}.attribute", max_length=64
        ).upper()
        if attribute not in EXECUTABLE_ATTRIBUTE_ALLOWLIST:
            raise ProtocolError(f"{field}.attribute is not execution-allowlisted")

        expected = _require_string(
            data.get("expected_current_value"),
            f"{field}.expected_current_value",
            max_length=4096,
            allow_empty=True,
        )
        captured = request.envelope.selection.attributes.get(attribute)
        if captured is None:
            raise ProtocolError(f"{field}.attribute was not captured in the snapshot")
        if expected != captured:
            raise ProtocolError(
                f"{field}.expected_current_value does not match the captured snapshot"
            )

        proposed = _require_string(
            data.get("proposed_value"),
            f"{field}.proposed_value",
            max_length=4096,
        )
        proposed = _validate_proposed_value(
            attribute, proposed, f"{field}.proposed_value"
        )
        if proposed == expected:
            raise ProtocolError(f"{field}.proposed_value must change the current value")

        return cls(
            operation_id=_require_string(
                data.get("operation_id"), f"{field}.operation_id", max_length=64
            ),
            operation_type=operation_type,
            target_element=target,
            attribute=attribute,
            expected_current_value=expected,
            proposed_value=proposed,
            reason=_require_string(
                data.get("reason"), f"{field}.reason", max_length=MAX_PREVIEW_TEXT
            ),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type,
            "target_element": self.target_element,
            "attribute": self.attribute,
            "expected_current_value": self.expected_current_value,
            "proposed_value": self.proposed_value,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ChangePreview:
    summary: str
    observations: tuple[str, ...]
    warnings: tuple[str, ...]
    operations: tuple[PreviewOperation, ...]

    @classmethod
    def from_mapping(
        cls, value: Any, *, request: ChangePreviewRequest
    ) -> "ChangePreview":
        data = _require_mapping(value, "preview")
        _require_exact_keys(
            data,
            "preview",
            {"summary", "observations", "warnings", "operations"},
        )
        raw_operations = data.get("operations")
        if not isinstance(raw_operations, list):
            raise ProtocolError("preview.operations must be an array")
        if len(raw_operations) > MAX_PREVIEW_ITEMS:
            raise ProtocolError(
                f"preview.operations exceeds the {MAX_PREVIEW_ITEMS}-operation limit"
            )
        operations = tuple(
            PreviewOperation.from_mapping(item, request=request, index=index)
            for index, item in enumerate(raw_operations)
        )
        operation_ids = [operation.operation_id for operation in operations]
        attributes = [operation.attribute for operation in operations]
        if len(set(operation_ids)) != len(operation_ids):
            raise ProtocolError("preview.operations contains duplicate operation_id values")
        if len(set(attributes)) != len(attributes):
            raise ProtocolError("preview.operations contains duplicate attributes")

        return cls(
            summary=_require_string(
                data.get("summary"), "preview.summary", max_length=MAX_PREVIEW_TEXT
            ),
            observations=_require_string_list(
                data.get("observations"), "preview.observations"
            ),
            warnings=_require_string_list(data.get("warnings"), "preview.warnings"),
            operations=operations,
        )

    def to_response(
        self,
        *,
        request: ChangePreviewRequest,
        backend: str,
        model: str | None = None,
        change_set_id: str | None = None,
        expires_at_utc: str | None = None,
        write_enabled: bool = False,
    ) -> dict[str, Any]:
        executable = bool(write_enabled and change_set_id and self.operations)
        return {
            "protocol_version": PROTOCOL_VERSION,
            "request_id": request.envelope.request_id,
            "status": "preview_ready",
            "mode": "controlled_write" if write_enabled else "preview_only",
            "backend": {"kind": backend, "model": model},
            "analysis": {
                "summary": self.summary,
                "observations": list(self.observations),
                "warnings": list(self.warnings),
            },
            "change_set": {
                "schema_version": "2.0",
                "change_set_id": change_set_id,
                "status": "proposal",
                "executable": executable,
                "requires_user_approval": True,
                "expires_at_utc": expires_at_utc,
                "scope": request.envelope.scope.to_dict(),
                "target_element": request.envelope.selection.full_name,
                "operations": [operation.to_dict() for operation in self.operations],
            },
            "changes": [],
            "persistence": "not_applied",
        }


def local_preview(request: ChangePreviewRequest) -> ChangePreview:
    selected = request.envelope.selection
    return ChangePreview(
        summary=(
            f"Preview request captured for {selected.element_type} "
            f"{selected.full_name}; no external AI backend is enabled."
        ),
        observations=(
            f"{len(selected.attributes)} allowlisted attributes are available.",
            f"Instruction: {request.instruction}",
        ),
        warnings=(
            "No AI proposal was generated in local-only mode.",
            "No operation can execute until the operator previews and confirms it.",
        ),
        operations=(),
    )


def openai_output_schema() -> dict[str, Any]:
    operation = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "operation_id",
            "operation_type",
            "target_element",
            "attribute",
            "expected_current_value",
            "proposed_value",
            "reason",
        ],
        "properties": {
            "operation_id": {"type": "string", "minLength": 1, "maxLength": 64},
            "operation_type": {"const": "set_attribute"},
            "target_element": {"type": "string", "minLength": 1, "maxLength": 1024},
            "attribute": {"enum": sorted(PREVIEW_ATTRIBUTE_ALLOWLIST)},
            "expected_current_value": {"type": "string", "maxLength": 4096},
            "proposed_value": {"type": "string", "minLength": 1, "maxLength": 4096},
            "reason": {"type": "string", "minLength": 1, "maxLength": MAX_PREVIEW_TEXT},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["summary", "observations", "warnings", "operations"],
        "properties": {
            "summary": {"type": "string", "minLength": 1, "maxLength": MAX_PREVIEW_TEXT},
            "observations": {
                "type": "array",
                "maxItems": MAX_PREVIEW_ITEMS,
                "items": {"type": "string", "minLength": 1, "maxLength": MAX_PREVIEW_TEXT},
            },
            "warnings": {
                "type": "array",
                "maxItems": MAX_PREVIEW_ITEMS,
                "items": {"type": "string", "minLength": 1, "maxLength": MAX_PREVIEW_TEXT},
            },
            "operations": {
                "type": "array",
                "maxItems": MAX_PREVIEW_ITEMS,
                "items": operation,
            },
        },
    }
