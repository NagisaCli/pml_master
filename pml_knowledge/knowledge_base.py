"""
PML Knowledge Base
===================
Loads, indexes, and retrieves paper mill equipment and PML syntax knowledge.
Acts as the Agent's "long-term memory" for E3D PML syntax, paper mill modeling
patterns, and industrial equipment specifications.
"""

import json
import math
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

#: The skill directory is the single source of truth for modeling knowledge.
#: It is read both by humans/LLMs (as Markdown) and by this loader, so there is
#: no second copy of the rules that can drift out of step with the first. The
#: previous ``pml_knowledge/corpus/`` duplicated the rules and had gone stale --
#: it still described a bottom-face datum and a SUSPEND/RESUME prologue, both of
#: which are wrong and are now recorded as failures F-1 and F-2 in
#: ``skill/workflows/diagnosing-failures.md``.
SKILL_ROOT = Path(__file__).resolve().parent.parent / "skill"
KNOWLEDGE_CORPUS_DIR = SKILL_ROOT


class PMLKnowledgeBase:
    """Paper mill PML knowledge base — stores equipment specs, syntax, and patterns."""

    def __init__(self, corpus_dir: Optional[Path] = None):
        self.corpus_dir = corpus_dir or KNOWLEDGE_CORPUS_DIR
        self.documents: Dict[str, str] = {}       # filename -> markdown text
        self.index: Dict[str, List[Tuple[str, int]]] = {}  # keyword -> [(file, line)]
        self._load_corpus()

    # -- Loading ------------------------------------------------------

    def _load_corpus(self):
        """Load every .md document under the skill corpus, recursively."""
        if not self.corpus_dir.exists():
            print(f"[KB] Knowledge base directory not found: {self.corpus_dir}")
            return
        # Recursive: the skill corpus is organised into knowledge/, workflows/,
        # equipment/ and projects/ subdirectories. Document ids keep the
        # subdirectory ("knowledge/iron-rules") so that files sharing a stem --
        # every section has a README.md -- do not overwrite one another.
        for md_file in sorted(self.corpus_dir.rglob("*.md")):
            doc_id = md_file.relative_to(self.corpus_dir).with_suffix("").as_posix()
            text = md_file.read_text(encoding="utf-8")
            self.documents[doc_id] = text
            self._index_document(doc_id, text)
        print(f"[KB] Loaded {len(self.documents)} knowledge documents: "
              f"{list(self.documents.keys())}")

    def _index_document(self, doc_id: str, text: str):
        """Build keyword inverted index."""
        lines = text.split("\n")
        for lineno, line in enumerate(lines):
            keywords = set()
            # Headings
            if line.startswith("##") or line.startswith("#"):
                keywords.add(line.strip("# ").strip().lower())
            # PML keywords in backticks
            for match in re.finditer(r"`([A-Z_][A-Z_0-9]*)`", line):
                keywords.add(match.group(1).lower())
            # Capitalized words
            for word in re.findall(r'\b[A-Z][A-Z_0-9]{2,}\b', line):
                keywords.add(word.lower())
            for kw in keywords:
                self.index.setdefault(kw, []).append((doc_id, lineno))

    # -- Retrieval ----------------------------------------------------

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Full-text search the knowledge base, return most relevant chunks."""
        query_lower = query.lower()

        import re
        query_words = set(re.findall(r'\b[a-z][a-z0-9_]{1,}\b', query_lower))

        # 1) Keyword match scoring.
        #
        # Term frequency is normalised by document length.  Raw counts make
        # relevance a proxy for size: an append-only project log accumulates
        # ordinary words until it outranks the short, canonical reference on
        # that reference's own subject.  jk-pump-build.md reached 46 uses of
        # "centre" against iron-rules.md's 18 purely by being 2.2x longer, and
        # started winning datum queries that the Iron Rules must own.
        #
        # Dividing by a length factor keeps a document competitive on the
        # terms it is actually about, while the heading and index bonuses --
        # which are evidence of aboutness rather than of mere length -- are
        # scaled by the same factor so they are not swamped in a long file.
        # sqrt damps the correction so a thorough document is not punished for
        # being thorough; it is the classic tf-idf length-normalisation trick.
        lengths = {d: max(len(t), 1) for d, t in self.documents.items()}
        median_length = sorted(lengths.values())[len(lengths) // 2] \
            if lengths else 1

        scores: Dict[str, float] = {}
        for doc_id, text in self.documents.items():
            text_lower = text.lower()
            norm = max(math.sqrt(lengths[doc_id] / median_length), 1.0)
            score = 0.0
            for word in query_words:
                if len(word) < 2:
                    continue
                count = text_lower.count(word)
                score += count * 3 / norm
                for line in text.split('\n'):
                    if line.startswith('#') and word in line.lower():
                        score += 50 / norm
                if word in self.index:
                    for (d, _) in self.index[word]:
                        if d == doc_id:
                            score += 30 / norm
            if score > 0:
                scores[doc_id] = score

        # Route high-level construction questions to the purpose-built maps.
        # Plain term frequency tends to rank iron-rules.md first because it is
        # intentionally repetitive; that is useful for safety questions but
        # slow when the user is asking "which element should represent this
        # shape?" or supplying a native export for a syntax study.
        # The boost must PROMOTE the routed document, not merely add a fixed
        # bonus.  Keyword score is raw term frequency over the whole document
        # and therefore grows without bound as a project log accumulates
        # entries, while a flat "+750" stays constant.  The long-running
        # jk-pump-build log had already reached ~1065 on this query against
        # the spatial map's ~282 and was outranking it on sheer length; the
        # flat bonus was one project entry away from being overtaken.
        # Routing is an intent decision, so lift the target clear of the
        # current leader instead of betting on a magic constant.
        def route_to(doc_id: str, margin: float = 1.25) -> None:
            if doc_id not in self.documents:
                return
            leader = max(scores.values(), default=0.0)
            scores[doc_id] = max(scores.get(doc_id, 0.0),
                                 leader * margin + 1.0)

        spatial_terms = {
            "shape", "spatial", "intent", "construct", "construction",
            "selection", "choose",
        }
        if query_words & spatial_terms:
            route_to("knowledge/pml-spatial-lookup")

        native_study = (
            {"native", "export"} <= query_words
            or {"syntax", "experiment"} <= query_words
            or {"syntax", "study"} <= query_words
        )
        if native_study:
            route_to("workflows/learning-from-native-exports")

        # Element-position datum semantics are safety rules, not project-log
        # anecdotes. Long project histories naturally repeat "primitive",
        # "position", "datum" and "centre" as failures accumulate; route a
        # direct datum query back to the canonical Iron Rules unless the user
        # explicitly asked for the spatial selector or native-study workflow.
        datum_safety = ("datum" in query_words
                        or {"primitive", "position"} <= query_words)
        if datum_safety and not native_study and not (query_words & spatial_terms):
            route_to("knowledge/iron-rules")

        # 2) Extract matching chunks
        results = []
        for doc_id in sorted(scores, key=scores.get, reverse=True)[:top_k]:
            text = self.documents[doc_id]
            best_chunk, best_score = self._best_chunk(text, query_words)
            results.append({
                "source": doc_id,
                "relevance": scores[doc_id],
                "chunk": best_chunk,
                "full_doc_title": text.split("\n")[0] if text else doc_id,
            })

        return results

    def _best_chunk(self, text: str, query_words: set) -> Tuple[str, int]:
        """Find the contiguous paragraph containing the most query words."""
        lines = text.split("\n")
        best_score = 0
        best_chunk = ""
        window = 20

        for start in range(0, len(lines), 5):
            chunk = "\n".join(lines[start:start + window])
            chunk_lower = chunk.lower()
            score = sum(1 for w in query_words if w in chunk_lower)
            if "```" in chunk:
                score += 5
            if score > best_score:
                best_score = score
                best_chunk = chunk

        if not best_chunk:
            best_chunk = "\n".join(lines[:30])
        return best_chunk[:2000], best_score

    def get_document(self, doc_id: str) -> Optional[str]:
        """Get full document by ID."""
        return self.documents.get(doc_id)

    def list_all_topics(self) -> List[str]:
        """List all knowledge topics."""
        topics = []
        for doc_id, text in self.documents.items():
            for line in text.split("\n"):
                if line.startswith("## "):
                    topics.append(f"{doc_id}: {line.strip('#').strip()}")
        return topics

    # -- Project-specific knowledge -----------------------------------

    @staticmethod
    def get_project_evar_mapping() -> Dict[str, str]:
        """Return the project environment variable mapping."""
        return {
            "ACP000": "\\AvevaCatalogue\\acp000",
            "APSPIC": "\\AvevaPlantSample\\apspic",
            "APSISO": "\\AvevaPlantSample\\apsiso",
            "AMS000": "\\AvevaMarineSample\\ams000",
            "AMSDIA": "\\AvevaMarineSample\\amsdia",
            "AMSDWG": "\\AvevaMarineSample\\amsdwg",
        }

    @staticmethod
    def get_element_type_list() -> List[str]:
        """Return list of common E3D element types."""
        return [
            "WORLD", "SITE", "ZONE", "FRMWRK", "EQUIPMENT", "VESSEL",
            "PUMP", "NOZZLE", "PIPE", "SCTN", "BRAN", "BEND", "TEE",
            "REDUCER", "VALVE", "FLANGE", "GASKET", "BOLTSET",
            "GENSEC", "PANEL", "BRACE", "STAIR", "LADDER", "HANDRAIL",
            "CABLE", "TRAY", "PLATFORM", "ANCHOR",
        ]

    @staticmethod
    def get_paper_mill_equipment_types() -> Dict[str, str]:
        """Return paper mill equipment type mapping."""
        return {
            "PULPER": "Hydrapulper — high-consistency stock slushing tank",
            "REFINER": "Disc refiner — fiber fibrillation and cutting",
            "CLEANER": "Centrifugal cleaner — heavy contaminant removal",
            "SCREEN": "Pressure screen — fiber fractionation and debris removal",
            "DIGESTER": "Continuous digester — kraft/sulfite chemical pulping vessel",
            "BLOW_TANK": "Blow tank — receives cooked pulp from digester",
            "WASHER": "Vacuum drum washer — pulp washing and black liquor extraction",
            "BLEACH_TOWER": "Bleaching tower — pulp brightness improvement stages",
            "EVAPORATOR": "Falling film evaporator — black liquor concentration",
            "RECOVERY_BOILER": "Chemical recovery boiler — burns black liquor, recovers chemicals",
            "LIME_KILN": "Rotary lime kiln — regenerates CaO from CaCO3",
            "CAUSTICIZER": "Causticizing plant — converts green liquor to white liquor",
            "HEADBOX": "Hydraulic headbox — uniform pulp jet onto forming wire",
            "BREAST_ROLL": "Breast roll — wire section first turning roll",
            "COUCH_ROLL": "Couch roll — wire section final extraction roll",
            "PRESS_ROLL": "Press roll — mechanical web dewatering nip",
            "DRYER_CYLINDER": "Steam-heated dryer cylinder — thermal web drying",
            "CALENDER_ROLL": "Calender roll — surface finish and thickness control",
            "REEL_DRUM": "Reel drum — continuous winding onto parent reel spool",
            "STOCK_CHEST": "Stock chest — pulp slurry intermediate storage",
            "WHITE_WATER_SILO": "White water silo — process water recirculation tank",
            "CLARIFIER": "Circular clarifier — wastewater primary sedimentation",
        }
