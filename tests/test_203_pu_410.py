"""
Verification test suite for 203-PU-409 and 203-PU-410.

Verifies:
- PML1 syntax and Iron Rules
- Equipment and SUBEQUIPMENT hierarchy balance
- Baseplate envelope (516 x 1278 x 50 mm) and zero foundation penetration
- Piecewise adapted 43-member /P1501B-BASE support structure
- Catalogue NOZZLE placeholders and orientations (Suction North, Discharge Up)
- Driver dual-cone construction with 36 axial cooling ribs
"""

from pathlib import Path
import re
import pytest

from wsb.pml_builder import validate_pml
from wsb.pml_parser import parse_native_tree

REPO = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO / "output"
PROJECT_OUTPUT_DIR = REPO / "Projects" / "JK_Pump_Build" / "output"

PUMP_TAGS = [
    ("203-PU-409", "203_PU_409", "BS DD Drum Wash Pump"),
    ("203-PU-410", "203_PU_410", "BS DD Return Filtrate Pump"),
]


@pytest.mark.parametrize("tag,element,duty", PUMP_TAGS)
def test_individual_pump_files_and_syntax(tag: str, element: str, duty: str):
    file1 = OUTPUT_DIR / f"{element}.pml"
    file2 = PROJECT_OUTPUT_DIR / f"{element}.pml"
    assert file1.is_file(), f"{file1} does not exist"
    assert file2.is_file(), f"{file2} does not exist"

    text1 = file1.read_text(encoding="utf-8")
    text2 = file2.read_text(encoding="utf-8")
    assert text1 == text2

    # 1. Syntax and Iron Rule Validation
    findings = validate_pml(text1, native_templates=True)
    assert not findings, f"PML validation findings for {element}: {findings}"

    # 2. Tree parsing and hierarchy balance
    roots = parse_native_tree(text1)
    assert len(roots) == 1
    equi = roots[0]
    assert equi.kind == "EQUIPMENT"
    assert equi.name == f"/{element}"

    sube_names = [child.name for child in equi.children if child.kind == "SUBEQUIPMENT"]
    expected_subes = [
        f"/{element}_CASING",
        f"/{element}_DRIVER",
        f"/{element}_DRIVE_SHAFT",
        f"/{element}_BASE",
        f"/{element}_SUCTION",
        f"/{element}_DISCHARGE",
    ]
    assert set(sube_names) == set(expected_subes)

    # 3. Baseplate envelope and zero foundation penetration
    assert re.search(r"NEW BOX[\s\S]*?XLEN\s+106\.24mm[\s\S]*?YLEN\s+1278mm[\s\S]*?POS\s+W\s+204\.88mm\s+N\s+0mm\s+U\s+41\.67mm", text1) is not None
    assert re.search(r"NEW BOX[\s\S]*?XLEN\s+106\.24mm[\s\S]*?YLEN\s+1278mm[\s\S]*?POS\s+E\s+204\.88mm\s+N\s+0mm\s+U\s+41\.67mm", text1) is not None

    for pos_match in re.finditer(r"POS\s+(?:[EW]\s+[\d.]+mm\s+)?(?:[NS]\s+[\d.]+mm\s+)?([UD])\s+([\d.]+)mm", text1):
        direction, val_str = pos_match.group(1), pos_match.group(2)
        val = float(val_str)
        if direction == "D":
            assert val == 0.0, f"Element found below foundation datum: D {val}mm"

    # 4. Nozzles: catalogue binding, positions, orientations
    nozzles = [node for node in equi.walk() if node.kind == "NOZZLE"]
    assert len(nozzles) == 2
    nozzle_map = {n.name: n for n in nozzles}

    suction = nozzle_map[f"/{element}_SUCTION_NOZZLE"]
    assert suction.get("CATR") == "SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN"
    assert suction.get("ORI") == "P1 IS N"
    assert "E 0mm" in suction.get("POS", "")
    assert "N 639mm" in suction.get("POS", "")

    discharge = nozzle_map[f"/{element}_DISCHARGE_NOZZLE"]
    assert discharge.get("CATR") == "SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL"
    assert discharge.get("ORI") == "P1 IS U"
    assert "E 0mm" in discharge.get("POS", "")
    assert "N 400mm" in discharge.get("POS", "")

    # 5. Base structure 43-member inventory
    base_sube = next(c for c in equi.children if c.name == f"/{element}_BASE")
    assert len(base_sube.children) == 43
    counts = {}
    for node in base_sube.children:
        counts[node.kind] = counts.get(node.kind, 0) + 1
    assert counts.get("BOX") == 11
    assert counts.get("PYRAMID") == 12
    assert counts.get("CYLINDER") == 10
    assert counts.get("EXTRUSION") == 10

    # 6. Driver motor construction
    driver_sube = next(c for c in equi.children if c.name == f"/{element}_DRIVER")
    cones = [c for c in driver_sube.children if c.kind == "CONE"]
    assert len(cones) == 2
    assert cones[0].get("DTOP") == "260.25mm" and cones[0].get("DBOT") == "173.5mm"
    assert cones[1].get("DTOP") == "173.5mm" and cones[1].get("DBOT") == "260.25mm"

    cooling_ribs = [c for c in driver_sube.children if c.kind == "CYLINDER" and c.get("DIAM") == "12mm"]
    assert len(cooling_ribs) == 36
    for rib in cooling_ribs:
        assert rib.get("ORI") == "Z IS N AND Y IS U"


def test_combined_review_macro():
    combined_file = OUTPUT_DIR / "JK_Pump_Build_203_PU_409_410.pml"
    assert combined_file.is_file()
    text = combined_file.read_text(encoding="utf-8")
    findings = validate_pml(text, native_templates=True)
    assert not findings, f"Combined macro validation findings: {findings}"

    roots = parse_native_tree(text)
    assert len(roots) == 2
    names = [r.name for r in roots]
    assert names == ["/203_PU_409", "/203_PU_410"]
