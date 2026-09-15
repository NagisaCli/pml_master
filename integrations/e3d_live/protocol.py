"""Versioned, project-scoped protocol for the E3D live bridge.

This module deliberately depends only on the Python standard library and other
modules inside ``integrations.e3d_live``.  It must not import the repository's
global agent, memory, project data, or geometry generators.  Project-specific
knowledge is attached later through an explicit, scope-checked adapter.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import re
from typing import Any, Mapping


PROTOCOL_VERSION = "2.0"
MESSAGE_SELECTION_SNAPSHOT = "selection_snapshot"
SOURCE_E3D_CAF_ADDIN = "e3d-caf-addin"
MAX_ATTRIBUTES = 64
MAX_ATTRIBUTE_NAME = 64
MAX_ATTRIBUTE_VALUE = 4096
MAX_ELEMENT_NAME = 1024

_SCOPE_PART_RE = re.compile(r"^[A-Z0-9_.-]{1,64}$")
ATTRIBUTE_ALLOWLIST = frozenset(
    {
        "NAME",
        "DESC",
        "POS",
        "ORI",
        "XLEN",
        "YLEN",
        "ZLEN",
        "HEIG",
        "DIAM",
        "DTOP",
        "DBOT",
        "CATR",
        "BORD",
        "PRES",
        "TEMP",
    }
)


class ProtocolError(ValueError):
    """Raised when a bridge message is invalid or crosses a scope boundary."""


def _require_mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ProtocolError(f"{field} must be an object")
    return value


def _require_exact_keys(
    value: Mapping[str, Any], field: str, allowed: set[str]
) -> None:
    keys = set(value)
    unexpected = keys - allowed
    missing = allowed - keys
    if unexpected:
        raise ProtocolError(f"{field} contains unsupported fields: {sorted(unexpected)!r}")
    if missing:
        raise ProtocolError(f"{field} is missing required fields: {sorted(missing)!r}")


def _require_string(
    value: Any,
    field: str,
    *,
    max_length: int = 256,
    allow_empty: bool = False,
) -> str:
    if not isinstance(value, str):
        raise ProtocolError(f"{field} must be a string")
    text = value.strip()
    if not allow_empty and not text:
        raise ProtocolError(f"{field} must not be empty")
    if len(text) > max_length:
        raise ProtocolError(f"{field} exceeds {max_length} characters")
    return text


def _require_positive_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ProtocolError(f"{field} must be a positive integer")
    return value


def _normalise_scope_part(value: Any, field: str) -> str:
    text = _require_string(value, field, max_length=65)
    text = text.lstrip("/").upper()
    if not _SCOPE_PART_RE.fullmatch(text):
        raise ProtocolError(
            f"{field} must contain only A-Z, 0-9, underscore, dot, or hyphen"
        )
    return text


@dataclass(frozen=True)
class ScopeKey:
    """The hard isolation boundary for one live E3D gateway process."""

    project_code: str
    mdb: str
    module: str

    @classmethod
    def create(cls, project_code: str, mdb: str, module: str = "DESIGN") -> "ScopeKey":
        return cls(
            project_code=_normalise_scope_part(project_code, "project_code"),
            mdb=_normalise_scope_part(mdb, "mdb"),
            module=_normalise_scope_part(module, "module"),
        )

    @classmethod
    def from_mapping(cls, value: Any, field: str = "scope") -> "ScopeKey":
        data = _require_mapping(value, field)
        _require_exact_keys(data, field, {"project_code", "mdb", "module"})
        return cls.create(
            project_code=data.get("project_code"),
            mdb=data.get("mdb"),
            module=data.get("module"),
        )

    @property
    def partition_id(self) -> str:
        raw = f"{self.project_code}|{self.mdb}|{self.module}".encode("utf-8")
        return sha256(raw).hexdigest()[:16]

    def to_dict(self) -> dict[str, str]:
        return {
            "project_code": self.project_code,
            "mdb": self.mdb,
            "module": self.module,
        }

    def assert_matches(self, other: "ScopeKey") -> None:
        if self != other:
            raise ProtocolError(
                "scope mismatch: gateway is bound to "
                f"{self.project_code}/{self.mdb}/{self.module}, received "
                f"{other.project_code}/{other.mdb}/{other.module}"
            )


@dataclass(frozen=True)
class SelectionSnapshot:
    full_name: str
    element_type: str
    owner_full_name: str
    attributes: Mapping[str, str]

    @classmethod
    def from_mapping(cls, value: Any) -> "SelectionSnapshot":
        data = _require_mapping(value, "selection")
        _require_exact_keys(
            data,
            "selection",
            {"full_name", "element_type", "owner_full_name", "attributes"},
        )
        raw_attributes = _require_mapping(data.get("attributes"), "selection.attributes")
        if len(raw_attributes) > MAX_ATTRIBUTES:
            raise ProtocolError(
                f"selection.attributes exceeds the {MAX_ATTRIBUTES}-attribute limit"
            )

        attributes: dict[str, str] = {}
        for raw_name, raw_value in raw_attributes.items():
            name = _require_string(
                raw_name,
                "selection.attributes key",
                max_length=MAX_ATTRIBUTE_NAME,
            ).upper()
            if name not in ATTRIBUTE_ALLOWLIST:
                raise ProtocolError(
                    f"selection.attributes.{name} is not in the bridge allowlist"
                )
            value_text = _require_string(
                raw_value,
                f"selection.attributes.{name}",
                max_length=MAX_ATTRIBUTE_VALUE,
                allow_empty=True,
            )
            attributes[name] = value_text

        return cls(
            full_name=_require_string(
                data.get("full_name"), "selection.full_name", max_length=MAX_ELEMENT_NAME
            ),
            element_type=_require_string(
                data.get("element_type"), "selection.element_type", max_length=64
            ).upper(),
            owner_full_name=_require_string(
                data.get("owner_full_name", ""),
                "selection.owner_full_name",
                max_length=MAX_ELEMENT_NAME,
                allow_empty=True,
            ),
            attributes=attributes,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "full_name": self.full_name,
            "element_type": self.element_type,
            "owner_full_name": self.owner_full_name,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True)
class SelectionEnvelope:
    request_id: str
    timestamp_utc: str
    bridge_session_id: str
    process_id: int
    source: str
    addin_version: str
    scope: ScopeKey
    selection: SelectionSnapshot

    @classmethod
    def from_mapping(cls, value: Any) -> "SelectionEnvelope":
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
            },
        )
        if data.get("protocol_version") != PROTOCOL_VERSION:
            raise ProtocolError(
                f"unsupported protocol_version {data.get('protocol_version')!r}; "
                f"expected {PROTOCOL_VERSION!r}"
            )
        if data.get("message_type") != MESSAGE_SELECTION_SNAPSHOT:
            raise ProtocolError("message_type must be 'selection_snapshot'")

        session = _require_mapping(data.get("session"), "session")
        _require_exact_keys(
            session,
            "session",
            {"bridge_session_id", "process_id", "source", "addin_version", "scope"},
        )
        source = _require_string(session.get("source"), "session.source", max_length=64)
        if source != SOURCE_E3D_CAF_ADDIN:
            raise ProtocolError(f"session.source must be {SOURCE_E3D_CAF_ADDIN!r}")
        return cls(
            request_id=_require_string(
                data.get("request_id"), "request_id", max_length=128
            ),
            timestamp_utc=_require_string(
                data.get("timestamp_utc"), "timestamp_utc", max_length=64
            ),
            bridge_session_id=_require_string(
                session.get("bridge_session_id"),
                "session.bridge_session_id",
                max_length=128,
            ),
            process_id=_require_positive_int(session.get("process_id"), "session.process_id"),
            source=source,
            addin_version=_require_string(
                session.get("addin_version"), "session.addin_version", max_length=32
            ),
            scope=ScopeKey.from_mapping(session.get("scope"), "session.scope"),
            selection=SelectionSnapshot.from_mapping(data.get("selection")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol_version": PROTOCOL_VERSION,
            "message_type": MESSAGE_SELECTION_SNAPSHOT,
            "request_id": self.request_id,
            "timestamp_utc": self.timestamp_utc,
            "session": {
                "bridge_session_id": self.bridge_session_id,
                "process_id": self.process_id,
                "source": self.source,
                "addin_version": self.addin_version,
                "scope": self.scope.to_dict(),
            },
            "selection": self.selection.to_dict(),
        }


@dataclass(frozen=True)
class GatewayResponse:
    request_id: str
    status: str
    message: str
    scope: ScopeKey

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol_version": PROTOCOL_VERSION,
            "request_id": self.request_id,
            "status": self.status,
            "message": self.message,
            "scope": self.scope.to_dict(),
            "changes": [],
            "persistence": "none",
        }
