"""Local validity and geometry-property tests for PML-STUDY-SCREW-001."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

from wsb.pml_builder import validate_pml


ROOT = Path(__file__).parents[1]
STUDY = ROOT / "Projects/E3D_Syntax_Lab/experiments/PML-STUDY-SCREW-001"
CANDIDATE = STUDY / "candidate/01_refined_screw_set.pml"


def _builder():
    spec = importlib.util.spec_from_file_location(
        "screw_study_builder", STUDY / "build_candidates.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_candidate_is_frozen():
    assert CANDIDATE.is_file()
    assert hashlib.sha256(CANDIDATE.read_bytes()).hexdigest().upper() == (
        "4EC02396EBD54D7F42E957A5091F9895246B521B64AD23EAE7363CED677D0923"
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
    assert len(blocks) == 56
    by_sube = {}
    for block in blocks:
        by_sube.setdefault(block["sube"], []).append(block)
    assert len(by_sube["/CODEX_SCREW_001_HEX_BOLT"]) == 21
    assert len(by_sube["/CODEX_SCREW_001_BUTTON_SCREW"]) == 16
    assert len(by_sube["/CODEX_SCREW_001_SQUARE_BOLT"]) == 19
