"""Local validity and geometry-property tests for the high-fidelity pump."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

from wsb.pml_builder import validate_pml


ROOT = Path(__file__).parents[1]
STUDY = ROOT / "Projects/E3D_Syntax_Lab/experiments/PML-STUDY-EXTR-002"
CANDIDATE = STUDY / "candidate/02_high_fidelity_pump.pml"


def _builder():
    spec = importlib.util.spec_from_file_location(
        "extr002_pump_builder", STUDY / "build_high_fidelity_pump.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_candidate_is_frozen():
    assert CANDIDATE.is_file()
    assert hashlib.sha256(CANDIDATE.read_bytes()).hexdigest().upper() == (
        "341D2E565A99E4BADEE951D790434FBC555E4FC943B9047A19F2517E0AF1B8F9"
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
    assert len(blocks) == 185
    assert sum(1 for b in blocks if b["type"] == "EXTRUSION") == 128
    assert sum(1 for b in blocks if b["type"] == "CYLINDER") == 57
    by_sube = {}
    for block in blocks:
        by_sube.setdefault(block["sube"], []).append(block)
    assert len(by_sube["/CODEX_EXTR_002_BASE"]) == 27
    assert len(by_sube["/CODEX_EXTR_002_CASING"]) == 45
    assert len(by_sube["/CODEX_EXTR_002_IMPELLER"]) == 8
    assert len(by_sube["/CODEX_EXTR_002_BEARING"]) == 6
    assert len(by_sube["/CODEX_EXTR_002_COUPLING"]) == 4
    assert len(by_sube["/CODEX_EXTR_002_MOTOR"]) == 63
    assert len(by_sube["/CODEX_EXTR_002_FASTENERS"]) == 32
