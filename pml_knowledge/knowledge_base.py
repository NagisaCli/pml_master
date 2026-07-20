"""
PML 知识库模块
==============
负责加载、索引和检索 PML 文档知识。
作为 Agent 的"长期记忆"，存储 E3D PML 语法、建模模式、最佳实践。
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

KNOWLEDGE_CORPUS_DIR = Path(__file__).parent / "corpus"


class PMLKnowledgeBase:
    """PML 知识库 — 存储 PML 语法、建模模式、项目约定。"""

    def __init__(self, corpus_dir: Optional[Path] = None):
        self.corpus_dir = corpus_dir or KNOWLEDGE_CORPUS_DIR
        self.documents: Dict[str, str] = {}    # filename -> markdown text
        self.index: Dict[str, List[Tuple[str, int]]] = {}  # keyword -> [(file, line)]
        self._load_corpus()

    # ── 加载 ──────────────────────────────────

    def _load_corpus(self):
        """加载 corpus/ 下所有 .md 文档。"""
        if not self.corpus_dir.exists():
            print(f"[KB] 知识库目录不存在: {self.corpus_dir}")
            return
        for md_file in sorted(self.corpus_dir.glob("*.md")):
            text = md_file.read_text(encoding="utf-8")
            self.documents[md_file.stem] = text
            self._index_document(md_file.stem, text)
        print(f"[KB] 已加载 {len(self.documents)} 个知识文档: {list(self.documents.keys())}")

    def _index_document(self, doc_id: str, text: str):
        """建立关键词倒排索引。"""
        lines = text.split("\n")
        for lineno, line in enumerate(lines):
            # 提取标题和重要关键词
            keywords = set()
            # 标题
            if line.startswith("##") or line.startswith("#"):
                keywords.add(line.strip("# #").strip().lower())
            # 代码块中定义的关键字 (NEW, NAME, POSITION 等)
            for match in re.finditer(r"`([A-Z_][A-Z_0-9]*)`", line):
                keywords.add(match.group(1).lower())
            # 普通词
            for word in re.findall(r'\b[A-Z][A-Z_0-9]{2,}\b', line):
                keywords.add(word.lower())
            for kw in keywords:
                self.index.setdefault(kw, []).append((doc_id, lineno))

    # ── 检索 ──────────────────────────────────

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """全文搜索知识库，返回最相关的文档片段。"""
        query_lower = query.lower()

        # 支持中英文关键词提取
        import re
        # English words
        query_words = set(re.findall(r'\b[a-z][a-z0-9_]{1,}\b', query_lower))
        # Chinese characters / bigrams
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', query_lower)
        for c in chinese_chars:
            # 添加整体和二元分词
            query_words.add(c)
            for i in range(len(c) - 1):
                query_words.add(c[i:i+2])

        # 1) 关键词匹配得分
        scores: Dict[str, float] = {}
        for doc_id, text in self.documents.items():
            text_lower = text.lower()
            score = 0
            for word in query_words:
                if len(word) < 2:
                    continue
                # 全文命中
                count = text_lower.count(word)
                score += count * 3  # 权重提升
                # 标题命中加权
                for line in text.split('\n'):
                    if line.startswith('#') and word in line.lower():
                        score += 50
                # 代码块和关键词索引命中
                if word in self.index:
                    for (d, _) in self.index[word]:
                        if d == doc_id:
                            score += 30
            if score > 0:
                scores[doc_id] = score

        # 2) 提取命中片段
        results = []
        for doc_id in sorted(scores, key=scores.get, reverse=True)[:top_k]:
            text = self.documents[doc_id]
            # 找到最相关的段落（包含最多查询词的连续行块）
            best_chunk, best_score = self._best_chunk(text, query_words)
            results.append({
                "source": doc_id,
                "relevance": scores[doc_id],
                "chunk": best_chunk,
                "full_doc_title": text.split("\n")[0] if text else doc_id,
            })

        return results

    def _best_chunk(self, text: str, query_words: set) -> Tuple[str, int]:
        """找到包含最多查询词的连续段落（最多 30 行）。"""
        lines = text.split("\n")
        best_score = 0
        best_chunk = ""
        window = 20

        for start in range(0, len(lines), 5):
            chunk = "\n".join(lines[start:start + window])
            chunk_lower = chunk.lower()
            score = sum(1 for w in query_words if w in chunk_lower)
            # 优先包含代码块的段落
            if "```" in chunk:
                score += 5
            if score > best_score:
                best_score = score
                best_chunk = chunk

        if not best_chunk:
            best_chunk = "\n".join(lines[:30])  # fallback: 开头
        return best_chunk[:2000], best_score

    def get_document(self, doc_id: str) -> Optional[str]:
        """按文档 ID 获取完整文档。"""
        return self.documents.get(doc_id)

    def list_all_topics(self) -> List[str]:
        """列出所有知识主题。"""
        topics = []
        for doc_id, text in self.documents.items():
            for line in text.split("\n"):
                if line.startswith("## "):
                    topics.append(f"{doc_id}: {line.strip('#').strip()}")
        return topics


    # ── 项目特定知识（从现有项目配置提取）──

    @staticmethod
    def get_project_evar_mapping() -> Dict[str, str]:
        """返回项目环境变量映射（从 evars*.bat 提取）。"""
        return {
            "ACP000": "\\AvevaCatalogue\\acp000",
            "APSPIC": "\\AvevaPlantSample\\apspic",
            "APSISO": "\\AvevaPlantSample\\apsiso",
            "AMS000": "\\AvevaMarineSample\\ams000",
            "AMSDIA": "\\AvevaMarineSample\\amsdia",
            "AMSDWG": "\\AvevaMarineSample\\amsdwg",
            "CPL000": "\\cpl\\cpl000",
            "PSL000": "\\psl\\psl000",
        }

    @staticmethod
    def get_element_type_list() -> List[str]:
        """返回 E3D 常用元素类型列表。"""
        return [
            "WORLD", "SITE", "ZONE", "FRMWRK", "EQUIPMENT", "VESSEL",
            "PUMP", "NOZZLE", "PIPE", "SCTN", "BRAN", "BEND", "TEE",
            "REDUCER", "VALVE", "FLANGE", "GASKET", "BOLTSET",
            "GENSEC", "PANEL", "BRACE", "STAIR", "LADDER", "HANDRAIL",
            "CABLE", "TRAY", "PLATFORM", "ANCHOR",
        ]

    @staticmethod
    def get_pml_function_ref() -> Dict[str, str]:
        """返回常用 PML 函数/方法参考。"""
        return {
            "NEW": "CREATE 创建新元素",
            "COLLECT": "Q QUERY 数据库查询",
            "DBREF": "获取数据库引用",
            "MEMBER": "获取子元素列表",
            "BELOW": "获取所有后代元素",
            "ATTACH": "附加分支",
            "CONNECT": "连接元素",
            "ALIGN": "对齐到目标",
            "JOIN": "连接到管口",
            "WRITE": "写入文件",
            "REPORT": "生成报告",
            "DotNetCall": "调用 .NET 方法",
            "DotNetLoad": "加载 .NET 程序集",
        }
