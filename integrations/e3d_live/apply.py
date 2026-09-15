"""One-time authorization protocol for controlled E3D writes.

The gateway never mutates E3D. It holds short-lived, scope-bound ChangeSets and
authorizes the x86 Add-in to execute an exact operation list after the operator
confirms it in the E3D window.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import threading
from typing import Any, Callable, Mapping
import uuid

from .preview import ChangePreview, ChangePreviewRequest, PreviewOperation
from .protocol import (
    PROTOCOL_VERSION,
    SOURCE_E3D_CAF_ADDIN,
    ProtocolError,
    ScopeKey,
    _require_exact_keys,
    _require_mapping,
    _require_positive_int,
    _require_string,
)


MESSAGE_APPLY_AUTHORIZATION_REQUEST = "apply_authorization_request"
MESSAGE_APPLY_RESULT = "apply_result"
CHANGE_SET_TTL_SECONDS = 300
MAX_PENDING_CHANGE_SETS = 128
APPLY_RESULT_STATUSES = frozenset(
    {"applied", "applied_not_persisted", "rejected", "stale", "rolled_back", "failed"}
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class SessionReference:
    bridge_session_id: str
    process_id: int
    source: str
    addin_version: str
    scope: ScopeKey

    @classmethod
    def from_mapping(cls, value: Any) -> "SessionReference":
        data = _require_mapping(value, "session")
        _require_exact_keys(
            data,
            "session",
            {"bridge_session_id", "process_id", "source", "addin_version", "scope"},
        )
        source = _require_string(data.get("source"), "session.source", max_length=64)
        if source != SOURCE_E3D_CAF_ADDIN:
            raise ProtocolError(f"session.source must be {SOURCE_E3D_CAF_ADDIN!r}")
        return cls(
            bridge_session_id=_require_string(
                data.get("bridge_session_id"),
                "session.bridge_session_id",
                max_length=128,
            ),
            process_id=_require_positive_int(data.get("process_id"), "session.process_id"),
            source=source,
            addin_version=_require_string(
                data.get("addin_version"), "session.addin_version", max_length=32
            ),
            scope=ScopeKey.from_mapping(data.get("scope"), "session.scope"),
        )


def _parse_base_message(
    value: Any, *, message_type: str, additional_keys: set[str]
) -> tuple[Mapping[str, Any], str, str, SessionReference]:
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
        }
        | additional_keys,
    )
    if data.get("protocol_version") != PROTOCOL_VERSION:
        raise ProtocolError("apply message protocol_version is incompatible")
    if data.get("message_type") != message_type:
        raise ProtocolError(f"message_type must be {message_type!r}")
    return (
        data,
        _require_string(data.get("request_id"), "request_id", max_length=128),
        _require_string(data.get("timestamp_utc"), "timestamp_utc", max_length=64),
        SessionReference.from_mapping(data.get("session")),
    )


def _require_string_array(value: Any, field_name: str, *, max_items: int = 16) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ProtocolError(f"{field_name} must be an array")
    if not value or len(value) > max_items:
        raise ProtocolError(f"{field_name} must contain 1 to {max_items} items")
    return tuple(
        _require_string(item, f"{field_name}[{index}]", max_length=128)
        for index, item in enumerate(value)
    )


@dataclass(frozen=True)
class ApplyAuthorizationRequest:
    request_id: str
    timestamp_utc: str
    session: SessionReference
    change_set_id: str
    target_element: str
    operation_ids: tuple[str, ...]
    persist_requested: bool

    @classmethod
    def from_mapping(cls, value: Any) -> "ApplyAuthorizationRequest":
        data, request_id, timestamp_utc, session = _parse_base_message(
            value,
            message_type=MESSAGE_APPLY_AUTHORIZATION_REQUEST,
            additional_keys={
                "change_set_id",
                "target_element",
                "operation_ids",
                "persist_requested",
            },
        )
        persist_requested = data.get("persist_requested")
        if not isinstance(persist_requested, bool):
            raise ProtocolError("persist_requested must be a boolean")
        return cls(
            request_id=request_id,
            timestamp_utc=timestamp_utc,
            session=session,
            change_set_id=_require_string(
                data.get("change_set_id"), "change_set_id", max_length=128
            ),
            target_element=_require_string(
                data.get("target_element"), "target_element", max_length=1024
            ),
            operation_ids=_require_string_array(
                data.get("operation_ids"), "operation_ids"
            ),
            persist_requested=persist_requested,
        )


@dataclass(frozen=True)
class ApplyOperationResult:
    operation_id: str
    attribute: str
    before_value: str
    requested_value: str
    after_value: str
    status: str

    @classmethod
    def from_mapping(cls, value: Any, index: int) -> "ApplyOperationResult":
        field_name = f"operation_results[{index}]"
        data = _require_mapping(value, field_name)
        _require_exact_keys(
            data,
            field_name,
            {
                "operation_id",
                "attribute",
                "before_value",
                "requested_value",
                "after_value",
                "status",
            },
        )
        status = _require_string(data.get("status"), f"{field_name}.status", max_length=32)
        if status not in {"applied", "failed", "rolled_back"}:
            raise ProtocolError(f"{field_name}.status is unsupported")
        return cls(
            operation_id=_require_string(
                data.get("operation_id"), f"{field_name}.operation_id", max_length=128
            ),
            attribute=_require_string(
                data.get("attribute"), f"{field_name}.attribute", max_length=64
            ).upper(),
            before_value=_require_string(
                data.get("before_value"),
                f"{field_name}.before_value",
                max_length=4096,
                allow_empty=True,
            ),
            requested_value=_require_string(
                data.get("requested_value"),
                f"{field_name}.requested_value",
                max_length=4096,
            ),
            after_value=_require_string(
                data.get("after_value"),
                f"{field_name}.after_value",
                max_length=4096,
                allow_empty=True,
            ),
            status=status,
        )


@dataclass(frozen=True)
class ApplyResultRequest:
    request_id: str
    timestamp_utc: str
    session: SessionReference
    authorization_id: str
    change_set_id: str
    target_element: str
    status: str
    persistence: str
    message: str
    operation_results: tuple[ApplyOperationResult, ...]

    @classmethod
    def from_mapping(cls, value: Any) -> "ApplyResultRequest":
        data, request_id, timestamp_utc, session = _parse_base_message(
            value,
            message_type=MESSAGE_APPLY_RESULT,
            additional_keys={
                "authorization_id",
                "change_set_id",
                "target_element",
                "status",
                "persistence",
                "message",
                "operation_results",
            },
        )
        status = _require_string(data.get("status"), "status", max_length=32)
        if status not in APPLY_RESULT_STATUSES:
            raise ProtocolError("apply result status is unsupported")
        raw_results = data.get("operation_results")
        if not isinstance(raw_results, list) or len(raw_results) > 16:
            raise ProtocolError("operation_results must be an array of at most 16 items")
        return cls(
            request_id=request_id,
            timestamp_utc=timestamp_utc,
            session=session,
            authorization_id=_require_string(
                data.get("authorization_id"), "authorization_id", max_length=128
            ),
            change_set_id=_require_string(
                data.get("change_set_id"), "change_set_id", max_length=128
            ),
            target_element=_require_string(
                data.get("target_element"), "target_element", max_length=1024
            ),
            status=status,
            persistence=_require_string(
                data.get("persistence"), "persistence", max_length=64
            ),
            message=_require_string(
                data.get("message"), "message", max_length=1000, allow_empty=True
            ),
            operation_results=tuple(
                ApplyOperationResult.from_mapping(item, index)
                for index, item in enumerate(raw_results)
            ),
        )


@dataclass
class PendingChangeSet:
    change_set_id: str
    bridge_session_id: str
    process_id: int
    scope: ScopeKey
    target_element: str
    operations: tuple[PreviewOperation, ...]
    created_at: datetime
    expires_at: datetime
    authorization_request_id: str | None = None
    authorization_id: str | None = None
    authorization_response: dict[str, Any] | None = None
    result_request_id: str | None = None
    result_signature: tuple[Any, ...] | None = None
    result_response: dict[str, Any] | None = None

    @property
    def expires_at_utc(self) -> str:
        return _iso_utc(self.expires_at)


class PendingChangeRegistry:
    """Thread-safe, bounded registry for preview/apply hand-off."""

    def __init__(
        self,
        *,
        ttl_seconds: int = CHANGE_SET_TTL_SECONDS,
        max_records: int = MAX_PENDING_CHANGE_SETS,
        clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        if ttl_seconds <= 0 or max_records <= 0:
            raise ValueError("registry limits must be positive")
        self._ttl_seconds = ttl_seconds
        self._max_records = max_records
        self._clock = clock
        self._lock = threading.Lock()
        self._records: dict[str, PendingChangeSet] = {}

    def register(
        self, request: ChangePreviewRequest, preview: ChangePreview
    ) -> PendingChangeSet | None:
        if not preview.operations:
            return None
        now = self._clock()
        record = PendingChangeSet(
            change_set_id=str(uuid.uuid4()),
            bridge_session_id=request.envelope.bridge_session_id,
            process_id=request.envelope.process_id,
            scope=request.envelope.scope,
            target_element=request.envelope.selection.full_name,
            operations=preview.operations,
            created_at=now,
            expires_at=now + timedelta(seconds=self._ttl_seconds),
        )
        with self._lock:
            self._purge_locked(now)
            if len(self._records) >= self._max_records:
                oldest = min(self._records.values(), key=lambda item: item.created_at)
                del self._records[oldest.change_set_id]
            self._records[record.change_set_id] = record
        return record

    def authorize(self, request: ApplyAuthorizationRequest) -> dict[str, Any]:
        now = self._clock()
        with self._lock:
            self._purge_locked(now)
            record = self._records.get(request.change_set_id)
            if record is None:
                raise ProtocolError("change_set_id is unknown or expired")
            self._assert_session(record, request.session)
            if request.target_element != record.target_element:
                raise ProtocolError("target_element does not match the ChangeSet")
            expected_ids = tuple(operation.operation_id for operation in record.operations)
            if request.operation_ids != expected_ids:
                raise ProtocolError("operation_ids do not match the ChangeSet")
            if record.result_response is not None:
                raise ProtocolError("the ChangeSet already has a terminal result")
            if record.authorization_response is None:
                record.authorization_request_id = request.request_id
                record.authorization_id = str(uuid.uuid4())
                record.authorization_response = {
                    "protocol_version": PROTOCOL_VERSION,
                    "request_id": request.request_id,
                    "status": "authorized",
                    "authorization_id": record.authorization_id,
                    "change_set_id": record.change_set_id,
                    "expires_at_utc": record.expires_at_utc,
                    "scope": record.scope.to_dict(),
                    "target_element": record.target_element,
                    "persist_requested": request.persist_requested,
                    "operations": [operation.to_dict() for operation in record.operations],
                }
            else:
                if request.request_id != record.authorization_request_id:
                    raise ProtocolError(
                        "the ChangeSet already has a different authorization request"
                    )
                if record.authorization_response["persist_requested"] != request.persist_requested:
                    raise ProtocolError("authorization retry changed persist_requested")
            return dict(record.authorization_response)

    def record_result(self, request: ApplyResultRequest) -> dict[str, Any]:
        now = self._clock()
        with self._lock:
            record = self._records.get(request.change_set_id)
            if record is None:
                raise ProtocolError("change_set_id is unknown")
            self._assert_session(record, request.session)
            if request.authorization_id != record.authorization_id:
                raise ProtocolError("authorization_id does not match the ChangeSet")
            if request.target_element != record.target_element:
                raise ProtocolError("target_element does not match the ChangeSet")
            expected_ids = tuple(operation.operation_id for operation in record.operations)
            actual_ids = tuple(result.operation_id for result in request.operation_results)
            if actual_ids != expected_ids[: len(actual_ids)]:
                raise ProtocolError(
                    "operation result IDs must be an ordered ChangeSet prefix"
                )
            self._validate_result(record, request)
            signature = self._result_signature(request)
            if record.result_response is not None:
                if request.request_id != record.result_request_id:
                    raise ProtocolError("the ChangeSet already has a different terminal result")
                if signature != record.result_signature:
                    raise ProtocolError(
                        "result request_id was reused with a different payload"
                    )
                return dict(record.result_response)
            record.result_request_id = request.request_id
            record.result_signature = signature
            record.result_response = {
                "protocol_version": PROTOCOL_VERSION,
                "request_id": request.request_id,
                "status": "recorded",
                "change_set_id": record.change_set_id,
                "authorization_id": record.authorization_id,
                "execution_status": request.status,
                "persistence": request.persistence,
                "recorded_at_utc": _iso_utc(now),
            }
            return dict(record.result_response)

    @staticmethod
    def _validate_result(
        record: PendingChangeSet, request: ApplyResultRequest
    ) -> None:
        expected = record.operations
        results = request.operation_results
        for index, result in enumerate(results):
            operation = expected[index]
            if result.attribute != operation.attribute:
                raise ProtocolError("operation result attribute does not match the ChangeSet")
            if result.before_value != operation.expected_current_value:
                raise ProtocolError("operation result before_value does not match the ChangeSet")
            if result.requested_value != operation.proposed_value:
                raise ProtocolError(
                    "operation result requested_value does not match the ChangeSet"
                )

        persist_requested = bool(
            record.authorization_response
            and record.authorization_response["persist_requested"]
        )
        if request.status == "applied":
            expected_persistence = "save_work" if persist_requested else "in_memory"
            if len(results) != len(expected) or any(
                result.status != "applied" for result in results
            ):
                raise ProtocolError("an applied result must verify every operation")
            if request.persistence != expected_persistence:
                raise ProtocolError("applied result persistence is inconsistent")
        elif request.status == "applied_not_persisted":
            if not persist_requested:
                raise ProtocolError("applied_not_persisted requires Save Work approval")
            if len(results) != len(expected) or any(
                result.status != "applied" for result in results
            ):
                raise ProtocolError(
                    "applied_not_persisted must verify every in-memory operation"
                )
            if request.persistence != "in_memory":
                raise ProtocolError("applied_not_persisted must remain in memory")
        elif request.status in {"rolled_back", "failed"}:
            if request.persistence != "none":
                raise ProtocolError("failed or rolled-back results cannot be persistent")
            if any(result.status != request.status for result in results):
                raise ProtocolError("operation result status is inconsistent")
        elif request.status in {"rejected", "stale"}:
            if results or request.persistence != "none":
                raise ProtocolError("rejected or stale results cannot contain changes")

    @staticmethod
    def _result_signature(request: ApplyResultRequest) -> tuple[Any, ...]:
        return (
            request.authorization_id,
            request.change_set_id,
            request.target_element,
            request.status,
            request.persistence,
            request.message,
            tuple(
                (
                    result.operation_id,
                    result.attribute,
                    result.before_value,
                    result.requested_value,
                    result.after_value,
                    result.status,
                )
                for result in request.operation_results
            ),
        )

    def active_count(self) -> int:
        with self._lock:
            self._purge_locked(self._clock())
            return len(self._records)

    @staticmethod
    def _assert_session(record: PendingChangeSet, session: SessionReference) -> None:
        if session.bridge_session_id != record.bridge_session_id:
            raise ProtocolError("bridge_session_id does not match the ChangeSet")
        if session.process_id != record.process_id:
            raise ProtocolError("process_id does not match the ChangeSet")
        record.scope.assert_matches(session.scope)

    def _purge_locked(self, now: datetime) -> None:
        expired = [
            change_set_id
            for change_set_id, record in self._records.items()
            if record.expires_at <= now and record.result_response is None
        ]
        for change_set_id in expired:
            del self._records[change_set_id]
