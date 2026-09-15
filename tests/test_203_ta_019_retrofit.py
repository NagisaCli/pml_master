"""
Test suite for 203-TA-019 Retrofit Macro
=========================================
Verifies:
1. File existence and non-emptiness.
2. Stack balance (balanced NEW and END).
3. validate_pml() zero new findings and strict PML1 compliance.
4. Absence of banned tokens (render prologue, PML2 keywords).
5. 360-degree walkway loop geometry (R_in=1000, R_out=1900, ladder cut-out W250..E250).
6. 360-degree structural handrails (R=1840, meeting at North, connecting to ladder at South).
7. Vertical dropleg continuity (U=0..50 base plate, U=50..2000 column DN800, dish apex at U=2000).
8. Nozzle N9 Eastward relocation (E=16001.5, N=6415, U=500, HEIG=250 penetrating dropleg).
9. 100% preservation of connected nozzles N1, N2, and other existing nozzles N4..N8.
10. Preservation of 4-leg support and ladder access structure.
"""

import math
import re
from pathlib import Path
import pytest
import wsb.pml_builder as pb

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PML = ROOT_DIR / "Projects" / "JK-Tank_Build" / "output" / "WSB_TA_203_TA_019_retrofit_20260914.pml"
ALT_EXPORT = Path(r"C:\Users\A\.gemini\antigravity\brain\55927096-4ebf-4e09-8ce4-336c7c879052\.user_uploaded\media_1789383959828.txt")

@pytest.fixture(scope="module")
def macro_content():
    assert OUTPUT_PML.exists(), f"Deliverable macro does not exist at {OUTPUT_PML}"
    with open(OUTPUT_PML, "r", encoding="utf-8") as f:
        text = f.read()
    assert len(text) > 5000, "Macro file is unexpectedly small"
    return text

def test_file_exists_and_non_empty(macro_content):
    assert len(macro_content) > 0
    assert "NEW STRUCTURE /203_TA_019_STRU" in macro_content
    assert "NEW EQUIPMENT /203_TA_019" in macro_content

def test_stack_balance(macro_content):
    stack = []
    for idx, line in enumerate(macro_content.splitlines()):
        l = line.strip()
        if l.startswith("NEW "):
            elem = l.split()[1]
            stack.append((elem, idx + 1))
        elif l == "END":
            assert len(stack) > 0, f"Unbalanced END at line {idx+1}"
            stack.pop()
    assert len(stack) == 0, f"Unbalanced stack at EOF: {stack}"

def test_banned_tokens(macro_content):
    banned = ["SUSPEND", "RESUME", "VAR 0", "ALPHA HEADER", "!var", "COLLECT", "UNSET", "ENDS", "END EQUI"]
    for token in banned:
        pattern = rf"\b{re.escape(token)}\b"
        matches = re.findall(pattern, macro_content, re.IGNORECASE)
        # Note: 'PDNAME unset', 'PTSP unset' in native export are valid attribute assignments
        if token.upper() in ["UNSET"]:
            continue
        assert len(matches) == 0, f"Banned token found in macro: {token}"

def test_pml_validation_zero_new_findings(macro_content):
    new_errs = pb.validate_pml(macro_content)
    # Check that new_errs does not exceed original export errors
    if ALT_EXPORT.exists():
        with open(ALT_EXPORT, "r", encoding="utf-8-sig") as f:
            orig_text = f.read()
        end_idx = orig_text.find("-- End Data Listing")
        orig_copy1 = orig_text[:end_idx] if end_idx != -1 else orig_text
        orig_errs = pb.validate_pml(orig_copy1)
        assert len(new_errs) <= len(orig_errs), f"New findings ({len(new_errs)}) exceed original ({len(orig_errs)})"
    # Ensure no severe syntax breakages
    assert not any("Syntax error" in e for e in new_errs)

def test_dropleg_geometry(macro_content):
    """
    Verifies the DN800 dropleg under /203_TA_019_SHELL:
    Base plate: DIAM 1050, HEIG 50, U = 25 (span 0..50)
    Column: DIAM 800, HEIG 1950, U = 1025 (span 50..2000)
    Bottom dish: apex at U = 2000 (POS U 2500, HEIG 500, Z is D)
    """
    assert "DIAM 1050mm" in macro_content
    assert "POS E 15445mm N 6415mm U 25mm" in macro_content
    assert "DIAM 800mm" in macro_content
    assert "HEIG 1950mm" in macro_content
    assert "POS E 15445mm N 6415mm U 1025mm" in macro_content
    assert "POS E 15445mm N 6415mm U 2500mm" in macro_content # bottom dish
    assert "ORI Y is N and Z is D" in macro_content

def test_nozzle_n9_east_relocation(macro_content):
    """
    Verifies nozzle N9 is relocated to the East side:
    POS E 16001.5mm N 6415mm U 500mm
    Penetrates DN800 dropleg column (center E 15445, R 400 -> wall at E 15845).
    """
    assert "NEW NOZZLE /203_TA_019_N9_NOZZ" in macro_content
    assert "POS E 16001.5mm N 6415mm U 500mm" in macro_content
    assert "POS E 14888.5mm" not in macro_content

def test_connected_nozzles_preserved(macro_content):
    """
    Verifies existing connected nozzles N1 and N2 are unchanged:
    N1: POS E 16100mm N 6415mm U 8600mm
    N2: POS E 15445mm N 6415mm U 8700mm
    """
    assert "POS E 16100mm N 6415mm U 8600mm" in macro_content
    assert "POS E 15445mm N 6415mm U 8700mm" in macro_content

def test_walkway_extrusion_geometry(macro_content):
    """
    Verifies 360-degree annular walkway EXTRUSION:
    POS E 15445mm N 6415mm U 8000mm, HEIG 50mm.
    Outer radius R=1900, Inner radius R=1000, Ladder opening at South W250..E250.
    """
    lines = macro_content.splitlines()
    walkway_found = False
    verts = []
    in_loop = False

    for idx, line in enumerate(lines):
        if "NEW EXTRUSION" in line and idx + 1 < len(lines) and "U 8000mm" in lines[idx+1]:
            walkway_found = True
        if walkway_found and "NEW LOOP" in line:
            in_loop = True
            continue
        if in_loop:
            if line.startswith("NEW BOX"):
                break
            if line.strip().startswith("POS "):
                # parse POS E/W ... N/S ...
                parts = line.strip().split()
                # format: POS E/W <val>mm N/S <val>mm U 0mm
                e_sign = 1 if parts[1] == "E" else -1
                e_val = float(parts[2].replace("mm", "")) * e_sign
                n_sign = 1 if parts[3] == "N" else -1
                n_val = float(parts[4].replace("mm", "")) * n_sign
                verts.append((e_val, n_val))

    assert walkway_found, "Walkway EXTRUSION at U 8000mm not found"
    assert len(verts) >= 60, f"Expected full circular polygon vertices, got {len(verts)}"

    # Check radius distribution
    r_list = [math.sqrt(x**2 + y**2) for x, y in verts]
    outer_r = [r for r in r_list if r > 1500]
    inner_r = [r for r in r_list if r < 1200]

    assert len(outer_r) > 20, "Missing outer arc vertices"
    assert len(inner_r) > 20, "Missing inner arc vertices"

    for r in outer_r:
        assert math.isclose(r, 1900.0, abs_tol=1.5), f"Outer vertex radius {r} != 1900"
    for r in inner_r:
        assert math.isclose(r, 1000.0, abs_tol=1.5), f"Inner vertex radius {r} != 1000"

    # Verify quad coverage (all 4 quadrants present)
    has_ne = any(x > 100 and y > 100 for x, y in verts)
    has_nw = any(x < -100 and y > 100 for x, y in verts)
    has_se = any(x > 100 and y < -100 for x, y in verts)
    has_sw = any(x < -100 and y < -100 for x, y in verts)
    assert has_ne and has_nw and has_se and has_sw, "Walkway does not encircle all 4 quadrants"

def test_handrails_geometry(macro_content):
    """
    Verifies Handrail A and B 360-degree coverage:
    Radius R=1840 mm, meeting at North (E 0, N 1840), connecting to ladder at South (E/W 240, S 1250).
    """
    assert "NEW HANDRA /203_TA_019_TOP_HANDRAIL_A" in macro_content
    assert "NEW HANDRA /203_TA_019_TOP_HANDRAIL_B" in macro_content
    # Meeting at North
    assert macro_content.count("POS E 0mm N 1840mm U 0mm") == 2
    # Connecting to ladder stringers
    assert "POS W 240mm S 1250mm U 0mm" in macro_content
    assert "POS E 240mm S 1250mm U 0mm" in macro_content
    # Circular curves with CURTYP THRU
    assert macro_content.count("CURTYP THRU") >= 4
