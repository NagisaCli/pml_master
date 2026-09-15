"""Append-only, secret-free audit receipts for one isolated live session."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import threading
from typing import Any


class AuditLog:
    def __init__(self, path: Path | None) -> None:
        self.path = path.expanduser().resolve() if path is not None else None
        self._lock = threading.Lock()

    def append(self, event: str, **fields: Any) -> None:
        if self.path is None:
            return
        record = {
            "timestamp_utc": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "event": event,
            **fields,
        }
        encoded = json.dumps(record, sort_keys=True, ensure_ascii=True)
        # Tokens and API keys are never accepted as fields by callers. This
        # final guard prevents accidental bearer-token persistence.
        lowered = encoded.lower()
        if "api_key" in lowered or "authorization: bearer" in lowered or '"token"' in lowered:
            raise ValueError("audit record contains a forbidden secret field")
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(encoded + "\n")
