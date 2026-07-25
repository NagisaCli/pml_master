"""
E3D Agent Memory System
========================
Persistent storage: error logs, user feedback, modeling decisions, lessons learned.
Memories are reloaded and referenced in subsequent Agent sessions.
"""

import json
import os
import tempfile
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

from ..config import MEMORY_DB_PATH, MAX_MEMORY_ENTRIES


class MemoryStore:
    """
    Memory store — JSON persistence.

    Entry types:
      - error:    Modeling/execution errors (pending manual review)
      - feedback: User feedback/corrections
      - pattern:  Successful/failed modeling patterns
      - decision: Design decision records
      - lesson:   Lessons learned
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or MEMORY_DB_PATH
        self._entries: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        self._load()

    # -- Core Operations ----------------------------------------------

    def add(self, entry_type: str, content: Dict[str, Any]):
        """Add a memory entry."""
        with self._lock:
            record = {
                "id": f"{entry_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                "type": entry_type,
                "timestamp": datetime.now().isoformat(),
                **content,
            }
            self._entries.append(record)
            self._trim()
            self._save()
        return record["id"]

    def add_error(self, module: str, error_text: str, context: Dict = None):
        """Record an error (pending manual review)."""
        return self.add("error", {
            "module": module,
            "error": error_text,
            "context": context or {},
            "resolved": False,
        })

    def add_feedback(self, user_message: str, related_to: str = ""):
        """Record user feedback."""
        return self.add("feedback", {
            "message": user_message,
            "related_to": related_to,
            "action_taken": "",
        })

    def add_pattern(self, name: str, description: str, pml_code: str, success: bool):
        """Record a modeling pattern (methodology)."""
        return self.add("pattern", {
            "name": name,
            "description": description,
            "pml_code": pml_code,
            "success": success,
            "usage_count": 0,
        })

    def add_lesson(self, topic: str, lesson: str, pml_example: str = ""):
        """Record a lesson learned."""
        return self.add("lesson", {
            "topic": topic,
            "lesson": lesson,
            "pml_example": pml_example,
        })

    # -- Query --------------------------------------------------------

    def query(self, type: Optional[str] = None, keyword: str = "",
              limit: int = 20) -> List[Dict]:
        """Query memories with optional type filter and keyword search."""
        results = self._entries
        if type:
            results = [e for e in results if e["type"] == type]
        if keyword:
            kw_lower = keyword.lower()
            results = [
                e for e in results
                if kw_lower in json.dumps(e, ensure_ascii=False).lower()
            ]
        return results[-limit:]

    def get_unresolved_errors(self) -> List[Dict]:
        """Get all unresolved errors."""
        return [e for e in self._entries
                if e["type"] == "error" and not e.get("resolved", False)]

    def mark_resolved(self, entry_id: str, resolution: str = ""):
        """Mark an error as resolved."""
        with self._lock:
            for entry in self._entries:
                if entry["id"] == entry_id and entry["type"] == "error":
                    entry["resolved"] = True
                    entry["resolved_at"] = datetime.now().isoformat()
                    entry["resolution"] = resolution
                    self._save()
                    return True
        return False

    def get_stats(self) -> Dict:
        """Return memory statistics."""
        types = {}
        for e in self._entries:
            t = e["type"]
            types[t] = types.get(t, 0) + 1
        return {
            "total": len(self._entries),
            "by_type": types,
            "unresolved_errors": len(self.get_unresolved_errors()),
        }

    def search_similar_errors(self, error_substring: str) -> List[Dict]:
        """Search for similar error records (diagnostic aid)."""
        return self.query(type="error", keyword=error_substring, limit=5)

    # -- Persistence --------------------------------------------------

    def _save(self):
        """Atomic write to avoid corrupt JSON on process interruption."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{self.db_path.stem}_", suffix=".tmp", dir=self.db_path.parent,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self._entries, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_name, self.db_path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)

    def _load(self):
        if self.db_path.exists():
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    entries = json.load(f)
                if not isinstance(entries, list):
                    raise ValueError("Memory root must be a list")
                self._entries = entries
            except (json.JSONDecodeError, OSError, ValueError) as exc:
                backup = self.db_path.with_suffix(
                    self.db_path.suffix + f".corrupt.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                try:
                    os.replace(self.db_path, backup)
                except OSError:
                    pass
                print(f"[Memory] Database unreadable, created new empty store: {exc}")
                self._entries = []

    def _trim(self):
        """Trim to max entry count."""
        if len(self._entries) > MAX_MEMORY_ENTRIES:
            self._entries = self._entries[-MAX_MEMORY_ENTRIES:]

    def clear(self):
        """Clear all memories."""
        self._entries = []
        self._save()

    def export_to_markdown(self) -> str:
        """Export as readable Markdown report."""
        lines = ["# E3D Paper Mill Agent Memory Report",
                 f"Generated: {datetime.now().isoformat()}", ""]
        lines.append(f"Total: {len(self._entries)} records\n")

        sections = {
            "error": "## Errors (Pending Manual Review)",
            "feedback": "## User Feedback",
            "pattern": "## Modeling Patterns",
            "lesson": "## Lessons Learned",
        }

        for etype, header in sections.items():
            entries = [e for e in self._entries if e["type"] == etype]
            if not entries:
                continue
            lines.append(header)
            for e in entries[-10:]:
                lines.append(f"- **{e.get('id', '')}** ({e.get('timestamp', '')})")
                for k, v in e.items():
                    if k not in ("id", "type", "timestamp"):
                        lines.append(f"  - {k}: {v}")
                lines.append("")

        return "\n".join(lines)
