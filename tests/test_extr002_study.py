"""Local validity and geometry-property tests for PML-STUDY-EXTR-002."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

from wsb.pml_builder import validate_pml


ROOT = Path(__file__).parents[1]
STUDY = ROOT / "Projects/E3D_Syntax_Lab/experiments/PML-STUDY-EXTR-002"
CANDIDATE = STUDY / "candidate/01_bolted_channel_frame.pml"


def _builder():
    spec = importlib.util.spec_from_file_location(
        "extr002_builder", STUDY / "build_candidates.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_candidate_is_frozen():
    assert CANDIDATE.is_file()
    assert hashlib.sha256(CANDIDATE.read_bytes()).hexdigest().upper() == (
        "70CE42874B505A4B739FEBB3C456CB4107DC2901659AC5DE670AA4F5BECB4094"
    )


def test_candidate_is_isolated_and_pml1_clean():
    text = CANDIDATE.read_text(encoding="utf-8")
    assert text.count("NEW EQUIPMENT") == 1
    assert "NEW SITE" not in text
    assert "NEW PIPE" not in text
    assert validate_pml(text) == []


def test_candidate_geometry_properties():
    builder = _builder()
    text = CANDIDATE.read_text(encoding="utf-8")
    assert builder.verify_geometry(text) == []
    blocks = builder.parse_blocks(text)
    assert len(blocks) == 32
    by_sube = {}
    for block in blocks:
        by_sube.setdefault(block["sube"], []).append(block)
    assert len(by_sube["/CODEX_EXTR_002_BASE"]) == 1
    assert len(by_sube["/CODEX_EXTR_002_RAIL"]) == 1
    assert len(by_sube["/CODEX_EXTR_002_PEDESTAL"]) == 2
    for cleat in ("NE", "NW", "SE", "SW"):
        assert len(by_sube[f"/CODEX_EXTR_002_CLEAT_{cleat}"]) == 1
    for bolt in ("NE1", "NE2", "NW1", "NW2", "SE1", "SE2", "SW1", "SW2"):
        assert len(by_sube[f"/CODEX_EXTR_002_BOLT_{bolt}"]) == 3
