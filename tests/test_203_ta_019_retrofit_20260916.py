import math
import re
from pathlib import Path
import pytest
import wsb.pml_builder as pb

ROOT_DIR = Path(__file__).resolve().parents[1]
COMBINED_PML = ROOT_DIR / "Projects" / "JK-Tank_Build" / "output" / "WSB_TA_203_TA_019_retrofit_20260916.pml"
STRU_PML = ROOT_DIR / "Projects" / "JK-Tank_Build" / "output" / "WSB_TA_203_TA_019_STRU_20260916.pml"
EQUI_PML = ROOT_DIR / "Projects" / "JK-Tank_Build" / "output" / "WSB_TA_203_TA_019_EQUI_20260916.pml"
DOWNLOADS_FILE = Path(r"C:\Users\A\Downloads\yes.txt")

E_TANK = 15445.0
N_TANK = 6415.0
R_TANK = 1000.0

@pytest.fixture(scope="module")
def combined_content():
    assert COMBINED_PML.exists(), f"File {COMBINED_PML} does not exist"
    with open(COMBINED_PML, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture(scope="module")
def downloads_content():
    assert DOWNLOADS_FILE.exists(), f"File {DOWNLOADS_FILE} does not exist"
    with open(DOWNLOADS_FILE, "r", encoding="utf-8") as f:
        return f.read()

def check_stack_balance(text, name="Macro"):
    stack = []
    for idx, l in enumerate(text.splitlines()):
        line = l.strip()
        if line.startswith("NEW "):
            elem = line.split()[1]
            stack.append((elem, idx + 1))
        elif line == "END":
            assert len(stack) > 0, f"{name}: Extra END at line {idx+1}"
            stack.pop()
    assert len(stack) == 0, f"{name}: Stack not balanced at EOF: {stack}"

def test_stack_balance_all(combined_content, downloads_content):
    check_stack_balance(combined_content, "Combined")
    check_stack_balance(downloads_content, "Downloads")
    with open(STRU_PML, "r", encoding="utf-8") as f:
        check_stack_balance(f.read(), "STRU")
    with open(EQUI_PML, "r", encoding="utf-8") as f:
        check_stack_balance(f.read(), "EQUI")

def test_banned_tokens(combined_content):
    banned = ["SUSPEND", "RESUME", "VAR 0", "ALPHA HEADER", "!var", "COLLECT", "ENDS", "END EQUI"]
    for token in banned:
        assert not re.search(rf"\b{re.escape(token)}\b", combined_content, re.IGNORECASE)

def test_pml_validation(combined_content):
    errs = pb.validate_pml(combined_content)
    assert not any("Syntax error" in e for e in errs)
    with open(STRU_PML, "r", encoding="utf-8") as f:
        stru_errs = pb.validate_pml(f.read())
        assert len(stru_errs) == 0

def test_ladder_proximity_to_cylinder(combined_content):
    def get_pos(name):
        m = re.search(rf"NEW\s+[A-Z0-9_-]+\s+{re.escape(name)}[\s\S]*?POS\s+E\s+([\d\.]+)mm\s+N\s+([\d\.]+)mm\s+U\s+([\d\.]+)mm", combined_content)
        assert m, f"{name} not found"
        e, n, u = float(m.group(1)), float(m.group(2)), float(m.group(3))
        r = math.hypot(e - E_TANK, n - N_TANK)
        return e, n, u, r

    _, _, _, ra = get_pos("/JK203_TA019_R2_F2_STILE_A")
    _, _, _, rb = get_pos("/JK203_TA019_R2_F2_STILE_B")
    assert 65.0 <= ra - R_TANK <= 75.0, f"Stile A distance {ra - R_TANK} mm out of range"
    assert 65.0 <= rb - R_TANK <= 75.0, f"Stile B distance {rb - R_TANK} mm out of range"

    for i in range(1, 9):
        _, _, _, rr = get_pos(f"/JK203_TA019_R2_F2_RUNG_{i:02d}")
        assert 19.0 <= rr - R_TANK <= 22.0, f"Rung {i} distance {rr - R_TANK} mm out of range"

def test_middle_platform_handrail_enclosure(combined_content):
    assert "POS E 608.57mm N 1305.08mm U 0mm" in combined_content
    assert combined_content.count("POS E 225.27mm N 1422.27mm U 0mm") >= 2
    assert "/JK203_TA019_R2_TOP_SLOT_RETURN_A" not in combined_content
    assert "/JK203_TA019_R2_TOP_SLOT_RETURN_B" not in combined_content

def test_preservation_of_all_other_equipment(combined_content):
    assert "NEW SUBEQUIPMENT /Copy-of-203_TA_019_SUPPORT" in combined_content
    assert "NEW BOX /JK203_TA019_S1_PEDESTAL" in combined_content
    assert "NEW SUBEQUIPMENT /Copy-of-203_TA_019_SHELL" in combined_content
    assert "NEW SUBEQUIPMENT /Copy-of-203_TA_019_N2" in combined_content
    assert "NEW SUBEQUIPMENT /Copy-of-203_TA_019_N1" in combined_content
    assert "NEW NOZZLE /Copy-of-203_TA_019_N1_NOZZ" in combined_content
    assert "NEW NOZZLE /Copy-of-203_TA_019_N9_NOZZ" in combined_content
    assert "NEW SUBEQUIPMENT /JK203_TA019_R2_MANWAY_ID600" in combined_content
    assert "NEW CYLINDER /JK203_TA019_F1_STILE_A" in combined_content
    assert "NEW BOX /JK203_TA019_F1_RUNG_01" in combined_content
