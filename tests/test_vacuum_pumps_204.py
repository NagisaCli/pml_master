"""
Test suite for 204-PU-401 and 204-PU-402 Vacuum Pump PML1 macros
================================================================
Verifies syntax, Iron Rules, primitive counts, and nozzle definitions.
"""

from pathlib import Path
import re
import pytest

from wsb.pml_builder import validate_pml
from wsb.pml_parser import parse_primitives

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

@pytest.mark.parametrize("tag", ["204_PU_401", "204_PU_402"])
def test_vacuum_pump_204_pml(tag):
    macro_file = OUTPUT_DIR / f"{tag}.pml"
    assert macro_file.is_file(), f"Macro file {macro_file} does not exist"

    text = macro_file.read_text(encoding="utf-8")
    
    # 1. PML1 syntax and Iron Rule validation
    errors = validate_pml(text)
    assert not errors, f"Syntax validation failed for {tag}: {errors}"

    # 2. Check equipment declaration
    assert f"NEW EQUI /{tag}" in text

    # 3. Check Sub-equipments and Nozzle names
    expected_subes = [
        f"{tag}_BASE_SKID",
        f"{tag}_PUMP_CASING",
        f"{tag}_INTERCONNECT",
        f"{tag}_AUX_UNIT",
        f"{tag}_STOOL",
        f"{tag}_MOTOR",
        f"{tag}_N1",
        f"{tag}_N2",
        f"{tag}_N3",
        f"{tag}_N4",
    ]
    for sube in expected_subes:
        assert f"NEW SUBE /{sube}" in text, f"Missing SUBE /{sube}"

    # 4. Check nozzle declarations with unique names
    assert f"NEW NOZZLE /{tag}_N1_NOZZ" in text
    assert f"NEW NOZZLE /{tag}_N2_NOZZ" in text
    assert f"NEW NOZZLE /{tag}_N3_NOZZ" in text
    assert f"NEW NOZZLE /{tag}_N4_NOZZ" in text

    # 5. Check nozzle orientations
    assert "ORI P1 IS U" in text  # N1 and N3 point UP
    assert "ORI P1 IS W" in text  # N2 and N4 point WEST

    # 6. Parse primitives count and extents
    prims = parse_primitives(text, tag, with_bounds=True)
    assert len(prims) == 74, f"Expected 74 primitives, got {len(prims)}"

    min_e = min(p["bounds"][0] for p in prims if p.get("bounds"))
    max_e = max(p["bounds"][1] for p in prims if p.get("bounds"))
    min_u = min(p["bounds"][4] for p in prims if p.get("bounds"))

    assert abs(min_u - 0.0) < 1.0, f"Expected base at U 0.0, got {min_u}"
    assert abs(max_e - 1977.0) < 1.0, f"Expected length 1977.0 mm, got {max_e}"
