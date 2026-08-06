"""Local validity and geometry-property tests for pump v3 (pressure test)."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

from wsb.pml_builder import validate_pml


ROOT = Path(__file__).parents[1]
STUDY = ROOT / "Projects/E3D_Syntax_Lab/experiments/PML-STUDY-EXTR-002"
CANDIDATE = STUDY / "candidate/03_high_fidelity_pump_v3.pml"


def _builder():
    spec = importlib.util.spec_from_file_location(
        "extr002_pump_v3_builder", STUDY / "build_high_fidelity_pump_v3.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_candidate_is_frozen():
    assert CANDIDATE.is_file()
    assert hashlib.sha256(CANDIDATE.read_bytes()).hexdigest().upper() == (
        "1086C7E167FBC162F7F27F20EC459C9B674B698C72539D4B90796EFC5EBDD8A3"
    )


def test_candidate_is_isolated_and_pml1_clean():
    text = CANDIDATE.read_text(encoding="utf-8")
    assert text.count("NEW EQUIPMENT") == 1
    assert "NEW SITE" not in text
    assert "NEW PIPE" not in text
    assert "NEW BOX" not in text
    assert validate_pml(text) == []


def test_candidate_geometry_properties():
    builder = _builder()
    text = CANDIDATE.read_text(encoding="utf-8")
    assert builder.verify_geometry(text) == []
    blocks = builder.parse_blocks(text)
    assert len(blocks) == 1154
    assert sum(1 for b in blocks if b["type"] == "EXTRUSION") == 950
    assert sum(1 for b in blocks if b["type"] == "CYLINDER") == 204
    total_vertices = sum(len(b["vertices"]) for b in blocks if b["type"] == "EXTRUSION")
    assert total_vertices >= 20000
    by_sube = {}
    for block in blocks:
        by_sube.setdefault(block["sube"], []).append(block)
    assert len(by_sube["/CODEX_EXTR_003_BASE"]) == 48
    assert len(by_sube["/CODEX_EXTR_003_CASING"]) == 170
    assert len(by_sube["/CODEX_EXTR_003_IMPELLER"]) == 24
    assert len(by_sube["/CODEX_EXTR_003_BEARING"]) == 92
    assert len(by_sube["/CODEX_EXTR_003_COUPLING"]) == 85
    assert len(by_sube["/CODEX_EXTR_003_MOTOR"]) == 719
    assert len(by_sube["/CODEX_EXTR_003_FASTENERS"]) == 16
