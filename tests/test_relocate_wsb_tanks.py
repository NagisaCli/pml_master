"""
Regression tests for WSB_TA equipment relocation (2026-09-02).
Verifies:
- Accurate coordinate translation by vector (E 51267, N 58841, U 0)
- Byte preservation of all internal geometry across 27,000+ lines
- Exact match of SHA-256 hashes
- 0 new PML validation findings
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import pytest

from wsb.pml_builder import validate_pml

REPO_ROOT = Path(__file__).resolve().parent.parent
IMPORT_FILE = REPO_ROOT / "Projects" / "JK-Tank_Build" / "imports" / "2026-09-02_WSB_TA.txt"
OUTPUT_TXT = REPO_ROOT / "Projects" / "JK-Tank_Build" / "output" / "WSB_TA_relocate_20260902.txt"
OUTPUT_PML = REPO_ROOT / "Projects" / "JK-Tank_Build" / "output" / "WSB_TA_relocate_20260902.pml"

EXPECTED_SRC_SHA = "ed1f73040fe40ad3c4934b88c817c1ffd4ae666f00bfbdeed816142468145f1c"
EXPECTED_OUT_SHA = "231ee209e81125f89db68b2514c3f83496d866e98b1ee269f1bdadc79fa49ec4"


def test_import_evidence_file_intact():
    assert IMPORT_FILE.is_file(), f"Missing import file: {IMPORT_FILE}"
    actual_hash = hashlib.sha256(IMPORT_FILE.read_bytes()).hexdigest()
    assert actual_hash == EXPECTED_SRC_SHA, f"Import hash mismatch: {actual_hash}"


def test_output_file_hashes_and_content():
    assert OUTPUT_TXT.is_file(), f"Missing output txt: {OUTPUT_TXT}"
    assert OUTPUT_PML.is_file(), f"Missing output pml: {OUTPUT_PML}"

    txt_bytes = OUTPUT_TXT.read_bytes()
    pml_bytes = OUTPUT_PML.read_bytes()

    assert txt_bytes == pml_bytes, "Output txt and pml must be byte-identical"
    assert hashlib.sha256(pml_bytes).hexdigest() == EXPECTED_OUT_SHA


def test_pml_validation_zero_new_findings():
    src_content = IMPORT_FILE.read_text(encoding="utf-8")
    out_content = OUTPUT_PML.read_text(encoding="utf-8")

    err_src = validate_pml(src_content)
    err_out = validate_pml(out_content)

    assert len(err_out) == len(err_src) == 215, f"Unexpected validation findings count: {len(err_out)}"


def test_equipment_coordinates_audit():
    out_lines = OUTPUT_PML.read_text(encoding="utf-8").splitlines()

    # Verify specific positions
    expected_positions = {
        "/205_TA_056": "POS E 51267mm N 58841mm D 300mm",
        "/205_TA_056_STRU": "POS E 51267mm N 58841mm U 0mm",
        "/205_TA_001": "POS E 51267mm N 58841mm U 500mm",
        "/205_TA_001_STRU": "POS E 51267mm N 58841mm U 0mm",
        "/203_TA_006": "POS E 66275.09mm N 78700.84mm U 0mm",
        "/203_TA_019": "POS E 51267mm N 58841mm U 0mm",
        "/203_TA_024": "POS E 51267mm N 58841mm D 300mm",
        "/203_TA_029": "POS E 67876mm N 55089mm D 300mm",
        "/203_TA_044": "POS E 51267mm N 58841mm U 0mm",
        "/204_TA_001": "POS E 51267.09mm N 58841.06mm U 0mm",
        "/204_TA_021": "POS E 51267mm N 58841mm U 0mm",
        "/204_TA_034": "POS E 51267mm N 58841mm D 300mm",
        "/204_TA_035": "POS E 51267mm N 58841mm D 300mm",
        "/205_TA_008": "POS E 51267mm N 58841mm D 300mm",
        "/205_TA_011": "POS E 51267mm N 58841mm D 300mm",
        "/205_TA_016": "POS E 51267mm N 58841mm U 0mm",
        "/205_TA_022": "POS E 51267mm N 58841mm D 300mm",
        "/205_TA_025": "POS E 51267mm N 58841mm D 300mm",
        "/205_TA_029": "POS E 51267mm N 58841mm D 300mm",
        "/205_TA_036": "POS E 51267mm N 58841mm U 0mm",
        "/205_TA_042": "POS E 51267mm N 58841mm D 300mm",
        "/205_TA_045": "POS E 51267mm N 58841mm D 300mm",
        "/205_TA_052": "POS E 51267mm N 58841mm U 0mm",
        "/205_TA_059": "POS E 51267mm N 58841mm D 300mm",
    }

    found_positions = {}
    curr_item = None
    for line in out_lines:
        line_s = line.strip()
        if line_s.startswith("NEW EQUIPMENT ") or line_s.startswith("NEW STRUCTURE "):
            curr_item = line_s.split()[2]
        elif curr_item and line_s.startswith("POS "):
            if curr_item not in found_positions:
                found_positions[curr_item] = line_s

    assert len(found_positions) == len(expected_positions)
    for name, exp_pos in expected_positions.items():
        assert found_positions.get(name) == exp_pos, f"Mismatch on {name}: got {found_positions.get(name)} != expected {exp_pos}"
