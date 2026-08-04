from __future__ import annotations

import pytest

from wsb.extrusion_builder import ExtrusionBuilder, ExtrusionSpec, build_extrusion
from wsb.pml_builder import PMLValidationError, validate_pml


HEX = (
    (0.0, 0.0),
    (0.0, 20.0),
    (-17.32, 30.0),
    (-34.64, 20.0),
    (-34.64, 0.0),
    (-17.32, -10.0),
    (0.0, 0.0),
)


def test_builds_native_full_name_extrusion_hierarchy():
    macro = build_extrusion(
        (300.0, -1264.99, -348.0),
        "Y IS S AND Z IS U",
        20.0,
        HEX,
        level=(5, 10),
    )
    assert macro.startswith(
        "NEW EXTRUSION\n"
        "POS E 300mm N -1264.99mm U -348mm\n"
        "ORI Y IS S AND Z IS U\n"
        "LEVE 5 10\n"
        "HEIG 20mm\n\n"
        "NEW LOOP\n"
    )
    assert macro.count("NEW VERTEX") == 6
    assert macro.splitlines().count("END") == 8
    assert validate_pml(macro) == []


def test_hex_profile_math_matches_native_regular_hex():
    spec = ExtrusionSpec((0, 0, 0), "Y IS S AND Z IS U", 20, HEX)
    assert spec.profile_bounds == pytest.approx((-34.64, 0.0, -10.0, 30.0))
    assert spec.profile_area == pytest.approx(1039.2)


def test_rejects_zero_area_and_parallel_axes():
    with pytest.raises(PMLValidationError, match="non-zero"):
        ExtrusionSpec((0, 0, 0), "Y IS S AND Z IS U", 10, ((0, 0), (1, 0), (2, 0)))
    with pytest.raises(PMLValidationError, match="orthogonal"):
        ExtrusionSpec((0, 0, 0), "Y IS U AND Z IS D", 10, ((0, 0), (1, 0), (0, 1)))
