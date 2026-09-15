"""Ephemeral session-file handling shared by the gateway and E3D Add-in."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import secrets
import uuid

from .protocol import PROTOCOL_VERSION, ScopeKey


ACCESS_MODE_READ_ONLY = "read_only"
ACCESS_MODE_CONTROLLED_WRITE = "controlled_write"
ACCESS_MODES = frozenset({ACCESS_MODE_READ_ONLY, ACCESS_MODE_CONTROLLED_WRITE})


def default_session_root() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    if base:
        return Path(base) / "E3DLiveBridge" / "sessions"
    return Path.home() / ".e3d_live_bridge" / "sessions"


def default_session_file(target_process_id: int, root: Path | None = None) -> Path:
    if isinstance(target_process_id, bool) or target_process_id <= 0:
        raise ValueError("target_process_id must be a positive integer")
    session_root = root if root is not None else default_session_root()
    return session_root / f"{target_process_id}.json"


@dataclass(frozen=True)
class LiveSession:
    bridge_session_id: str
    token: str
    gateway_url: str
    scope: ScopeKey
    target_process_id: int
    access_mode: str = ACCESS_MODE_READ_ONLY

    @classmethod
    def create(
        cls,
        scope: ScopeKey,
        gateway_url: str,
        target_process_id: int,
        *,
        access_mode: str = ACCESS_MODE_READ_ONLY,
    ) -> "LiveSession":
        if isinstance(target_process_id, bool) or target_process_id <= 0:
            raise ValueError("target_process_id must be a positive integer")
        if access_mode not in ACCESS_MODES:
            raise ValueError(f"unsupported access_mode {access_mode!r}")
        return cls(
            bridge_session_id=str(uuid.uuid4()),
            token=secrets.token_urlsafe(32),
            gateway_url=gateway_url,
            scope=scope,
            target_process_id=target_process_id,
            access_mode=access_mode,
        )

    @property
    def write_enabled(self) -> bool:
        return self.access_mode == ACCESS_MODE_CONTROLLED_WRITE

    def to_dict(self) -> dict[str, object]:
        return {
            "protocol_version": PROTOCOL_VERSION,
            "bridge_session_id": self.bridge_session_id,
            "token": self.token,
            "gateway_url": self.gateway_url,
            "target_process_id": self.target_process_id,
            "scope": self.scope.to_dict(),
            "access_mode": self.access_mode,
            "write_enabled": self.write_enabled,
        }


def write_session_file(session: LiveSession, path: Path) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(session.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    try:
        os.chmod(temporary, 0o600)
    except OSError:
        pass
    temporary.replace(path)


def remove_session_file(session: LiveSession, path: Path) -> None:
    path = path.expanduser().resolve()
    try:
        current = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return
    if (
        current.get("bridge_session_id") == session.bridge_session_id
        and current.get("target_process_id") == session.target_process_id
    ):
        path.unlink(missing_ok=True)
