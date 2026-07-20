"""
E3D Agent 记忆系统
=================
持久化存储：错误日志、用户反馈、建模决策、经验教训。
这些记忆会在后续 Agent 会话中被重新加载和参考。
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
    记忆存储 — JSON 持久化。
    存储类型：
      - error:    建模/执行错误（人工处理）
      - feedback: 用户反馈/修正
      - pattern:  成功/失败的建模模式
      - decision: 设计决策记录
      - lesson:   经验教训
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or MEMORY_DB_PATH
        self._entries: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        self._load()

    # ── 核心操作 ─────────────────────────────

    def add(self, entry_type: str, content: Dict[str, Any]):
        """添加一条记忆。"""
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
        """记录错误（待人工处理）。"""
        return self.add("error", {
            "module": module,
            "error": error_text,
            "context": context or {},
            "resolved": False,
        })

    def add_feedback(self, user_message: str, related_to: str = ""):
        """记录用户反馈。"""
        return self.add("feedback", {
            "message": user_message,
            "related_to": related_to,
            "action_taken": "",
        })

    def add_pattern(self, name: str, description: str, pml_code: str, success: bool):
        """记录一个建模模式（方法论）。"""
        return self.add("pattern", {
            "name": name,
            "description": description,
            "pml_code": pml_code,
            "success": success,
            "usage_count": 0,
        })

    def add_lesson(self, topic: str, lesson: str, pml_example: str = ""):
        """记录经验教训。"""
        return self.add("lesson", {
            "topic": topic,
            "lesson": lesson,
            "pml_example": pml_example,
        })

    # ── 查询 ─────────────────────────────────

    def query(self, type: Optional[str] = None, keyword: str = "",
              limit: int = 20) -> List[Dict]:
        """查询记忆，支持类型过滤和关键词搜索。"""
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
        """获取所有未解决的错误。"""
        return [e for e in self._entries
                if e["type"] == "error" and not e.get("resolved", False)]

    def mark_resolved(self, entry_id: str, resolution: str = ""):
        """标记错误为已解决。"""
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
        """返回记忆统计。"""
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
        """搜索相似的错误记录（帮助诊断）。"""
        return self.query(type="error", keyword=error_substring, limit=5)

    # ── 持久化 ─────────────────────────────

    def _save(self):
        """原子写入，避免进程中断时留下损坏的 JSON 文件。"""
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
                    raise ValueError("记忆库根节点必须是列表")
                self._entries = entries
            except (json.JSONDecodeError, OSError, ValueError) as exc:
                # 保留故障现场，防止下一次写入覆盖可恢复的数据。
                backup = self.db_path.with_suffix(
                    self.db_path.suffix + f".corrupt.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                try:
                    os.replace(self.db_path, backup)
                except OSError:
                    pass
                print(f"[Memory] 记忆库无法读取，已新建空库: {exc}")
                self._entries = []

    def _trim(self):
        """裁剪到最大条目数。"""
        if len(self._entries) > MAX_MEMORY_ENTRIES:
            self._entries = self._entries[-MAX_MEMORY_ENTRIES:]

    def clear(self):
        """清空记忆。"""
        self._entries = []
        self._save()

    def export_to_markdown(self) -> str:
        """导出为可读的 Markdown 报告。"""
        lines = ["# E3D Agent 记忆报告", f"生成时间: {datetime.now().isoformat()}", ""]
        lines.append(f"总计: {len(self._entries)} 条记录\n")

        sections = {
            "error": "## 错误记录（待人工处理）",
            "feedback": "## 用户反馈",
            "pattern": "## 建模模式",
            "lesson": "## 经验教训",
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
