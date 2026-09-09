"""Regression tests for PML-STUDY-HANDRA-001 (Native Structural Handrail Study)."""

from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path

import pytest

from wsb.handrail_builder import (
    HandrailBuilder,
    HandrailSpec,
    RouteCurve,
    RoutePoint,
    build_circular_handrail,
)
from wsb.pml_builder import PMLValidationError, validate_pml

REPO_ROOT = Path(__file__).resolve().parent.parent
LAB = REPO_ROOT / "Projects" / "E3D_Syntax_Lab"
NATIVE_IMPORT = LAB / "imports" / "2026-08-31_handra_native.txt"
STUDY_DIR = LAB / "experiments" / "PML-STUDY-HANDRA-001"
NATIVE_SOURCE = STUDY_DIR / "source" / "2026-08-31_handra_native.txt"
CANDIDATE_01 = STUDY_DIR / "candidate" / "01_circular_handra_trial.pml"

NATIVE_SHA256 = "76efb61dd2b7ab95517c297a089a2ea6616bbd4265b8f1b5c42aba8de0a43f93"


def test_native_handra_evidence_preserved_byte_for_byte():
    """Verify that both import and experiment source files match the exact SHA-256 hash."""
    assert NATIVE_IMPORT.is_file(), f"Missing import evidence: {NATIVE_IMPORT}"
    assert NATIVE_SOURCE.is_file(), f"Missing source evidence: {NATIVE_SOURCE}"

    import_hash = hashlib.sha256(NATIVE_IMPORT.read_bytes()).hexdigest()
    source_hash = hashlib.sha256(NATIVE_SOURCE.read_bytes()).hexdigest()

    assert import_hash == NATIVE_SHA256
    assert source_hash == NATIVE_SHA256


def test_candidate_01_macro_validates_cleanly():
    """Verify candidate trial macro has no PML2 or syntax violations."""
    assert CANDIDATE_01.is_file()
    content = CANDIDATE_01.read_text(encoding="utf-8")
    errors = validate_pml(content)
    assert errors == [], f"Candidate 01 validation errors: {errors}"


def test_native_geometry_mathematical_derivation():
    """Verify the 8-point discretization matches the circle R=2910 centered at (0, 2910)."""
    radius = 2910.0
    ec, nc = 0.0, 2910.0
    s45 = math.sin(math.pi / 4.0)

    # Check 45-degree midpoint curve coordinates
    expected_curve_1_e = ec + radius * s45  # 2057.6807
    expected_curve_1_n = nc - radius * s45  # 852.3193

    assert round(expected_curve_1_e, 2) == 2057.68
    assert round(expected_curve_1_n, 2) == 852.32

    # Check 135-degree midpoint curve coordinates
    expected_curve_3_e = ec - radius * s45  # -2057.6807
    expected_curve_3_n = nc + radius * s45  # 4967.6807

    assert round(abs(expected_curve_3_e), 2) == 2057.68
    assert round(expected_curve_3_n, 2) == 4967.68


def test_build_circular_handrail_produces_native_specimen_geometry():
    """Verify build_circular_handrail reproduces native listing elements."""
    macro = build_circular_handrail(
        center_local=(0.0, 2910.0),
        radius=2910.0,
        position=(34999.64, -1251.49, 15320.0),
        top_rail_height=1250.0,
        mid_rail_height=750.0,
        post_spacing=1000.0,
        tangent_offset=300.0,
        fillet_radius=100.0,
    )

    assert "NEW HANDRA" in macro
    assert "RAILHE 1250mm 750mm" in macro
    assert "POSTSP 1000mm" in macro
    assert "TANGOF 300mm" in macro
    assert "SHOWKP true" in macro
    assert "BRAD 100mm" in macro
    assert "NEW RPATH" in macro
    assert "DRNS E 22.5 N" in macro
    assert "DRNE E 22.5 S" in macro
    assert "CURTYP THRU" in macro

    # Check coordinate occurrences
    assert "E 2057.68mm N 852.32mm" in macro
    assert "E 2910mm N 2910mm" in macro
    assert "E 2057.68mm N 4967.68mm" in macro
    assert "E 0mm N 5820mm" in macro
    assert "W 2057.68mm N 4967.68mm" in macro
    assert "W 2910mm N 2910mm" in macro
    assert "W 2057.68mm N 852.32mm" in macro

    errors = validate_pml(macro)
    assert errors == []


def test_handrail_builder_validation_guards():
    """Verify that illegal handrail parameters raise PMLValidationError."""
    # Top rail <= mid rail
    with pytest.raises(PMLValidationError, match="Top rail height must be greater"):
        HandrailSpec(
            top_rail_height=500.0,
            mid_rail_height=750.0,
            path_items=(RoutePoint(), RoutePoint()),
        )

    # Post spacing <= 0
    with pytest.raises(PMLValidationError, match="Post spacing must be positive"):
        HandrailSpec(
            post_spacing=-10.0,
            path_items=(RoutePoint(), RoutePoint()),
        )

    # Less than 2 path points
    with pytest.raises(PMLValidationError, match="at least 2 points"):
        HandrailSpec(
            path_items=(RoutePoint(),),
        )

    # Invalid curve type
    with pytest.raises(PMLValidationError, match="Unsupported CURTYP"):
        RouteCurve(position=(0.0, 0.0, 0.0), curve_type="INVALID")


def test_all_candidates_validate_cleanly():
    """Verify all 4 generated candidate macros pass validate_pml without errors."""
    for candidate in sorted((STUDY_DIR / "candidate").glob("*.pml")):
        content = candidate.read_text(encoding="utf-8")
        errors = validate_pml(content)
        assert errors == [], f"Validation errors in {candidate.name}: {errors}"


def test_rectangular_handrail_builder():
    """Verify build_rectangular_handrail produces a closed 4-corner loop."""
    from wsb.handrail_builder import build_rectangular_handrail

    macro = build_rectangular_handrail(
        length_e=5000.0,
        width_n=3000.0,
        elevation=500.0,
        name="RECT_HR",
    )
    assert "NEW HANDRA /RECT_HR" in macro
    assert "POS E 5000mm N 0mm U 500mm" in macro
    assert "POS E 5000mm N 3000mm U 500mm" in macro
    assert "POS E 0mm N 3000mm U 500mm" in macro
    assert validate_pml(macro) == []


def test_arc_handrail_builder():
    """Verify build_arc_handrail produces parametric multi-segment curves."""
    from wsb.handrail_builder import build_arc_handrail

    macro = build_arc_handrail(
        center_local=(0.0, 0.0),
        radius=1500.0,
        start_angle_deg=0.0,
        sweep_angle_deg=180.0,
        segments=2,
    )
    assert "NEW HANDRA" in macro
    assert "CURTYP THRU" in macro
    assert validate_pml(macro) == []


def test_user_rendered_screenshot_evidence_preserved():
    """Verify user E3D rendered screenshot evidence is preserved in results."""
    user_png = STUDY_DIR / "results" / "2026-08-31_circular_handra_e3d_rendered.png"
    assert user_png.is_file(), f"Missing user E3D rendering evidence: {user_png}"
    digest = hashlib.sha256(user_png.read_bytes()).hexdigest()
    assert digest == "6483d9fc45d5677ca5164a478d827afc26333a42f93a61a74212dd23dc96ab9b"


def test_pml_builder_fluent_handrail_methods():
    """Verify PMLBuilder.circular_handrail and rectangular_handrail methods."""
    from wsb.pml_builder import PMLBuilder

    builder = PMLBuilder()
    builder.equi("203_TA_001")
    builder.sube("203_TA_001_TOP_HANDRAIL")
    builder.circular_handrail(
        center_local=(0.0, 0.0),
        radius=3000.0,
        elevation=12000.0,
        name="TA_001_ROOF_HR",
    )
    builder.rectangular_handrail(
        length_e=4000.0,
        width_n=2500.0,
        elevation=6000.0,
        name="TA_001_PLAT_HR",
    )
    macro = builder.build()

    assert "NEW HANDRA /TA_001_ROOF_HR" in macro
    assert "NEW HANDRA /TA_001_PLAT_HR" in macro
    assert "CURTYP THRU" in macro
    assert validate_pml(macro) == []


def test_tank_top_handrail_ladder_connection():
    """Verify build_tank_top_handrail connects outward directly to vertical ladder handrail stringers."""
    from wsb.handrail_builder import build_tank_top_handrail

    macro = build_tank_top_handrail(
        center_local=(0.0, 0.0),
        radius=4850.0,
        ladder_distance=5150.0,
        ladder_half_width=240.0,
        name="TA_056_LADDER_HR",
    )
    assert "NEW HANDRA /TA_056_LADDER_HR" in macro
    assert "DRNS E" in macro
    assert "DRNE W" in macro
    assert "POS W 5150mm S 240mm U 0mm" in macro
    assert "POS W 5150mm N 240mm U 0mm" in macro
    assert "CURTYP THRU" in macro
    assert validate_pml(macro) == []


