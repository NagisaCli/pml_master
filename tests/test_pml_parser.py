"""
Regression tests for the shared macro parser.

The parser is the one thing every numeric verifier depends on, so its failure
mode matters as much as its results. IR-11f: a verifier that parses nothing
reports nothing, and a silent check is indistinguishable from a passing one.
"""

from __future__ import annotations

import pytest

from wsb.pml_parser import (
    bounds_of,
    equipment_name_to_element,
    lowest_point,
    parse_labelled,
    parse_nozzles,
    parse_plan_direction,
    parse_primitives,
)


def _macro(body: str) -> str:
    return "NEW EQUI /205_PU_004\n" + body


def test_attribute_order_does_not_change_the_parse():
    """
    IR-11f: the parse must not depend on emission order.

    The previous pump parser matched a fixed six-line block, so reordering an
    attribute made it silently match nothing. Both orders below describe the
    same cylinder and must parse identically.
    """
    canonical = _macro(
        "NEW CYLI\nDIAM 500\nHEIG 300\nORI Z IS U AND Y IS N\n"
        "POS E 10 N 20 U 100\n"
    )
    reordered = _macro(
        "NEW CYLI\nHEIG 300\nDIAM 500\nORI Z IS U AND Y IS N\n"
        "POS E 10 N 20 U 100\n"
    )
    first = parse_primitives(canonical, "205-PU-004", simple_tag=True)
    second = parse_primitives(reordered, "205-PU-004", simple_tag=True)
    assert first == second
    assert len(first) == 1
    assert first[0]["diam"] == 500.0
    assert first[0]["heig"] == 300.0


def test_labelled_parse_survives_attribute_reordering():
    """The same guarantee for label-introduced detail features."""
    for body in (
        "-- cast motor foot mounting pad\nNEW BOX\n"
        "XLEN 100\nYLEN 200\nZLEN 50\nPOS E 0 N 0 U 25\n",
        "-- cast motor foot mounting pad\nNEW BOX\n"
        "ZLEN 50\nYLEN 200\nXLEN 100\nPOS E 0 N 0 U 25\n",
    ):
        found = parse_labelled(_macro(body), "cast motor foot mounting pad", "BOX")
        assert len(found) == 1, f"label parse went silent for:\n{body}"
        assert found[0]["xlen"] == 100.0
        assert found[0]["zlen"] == 50.0


def test_grouping_elements_are_never_treated_as_geometry():
    """A SUBE owns a position but occupies no space."""
    script = _macro(
        "NEW SUBE /205_PU_004_CASING\nPOS E 0 N 0 U 0\n"
        "NEW CYLI\nDIAM 400\nHEIG 200\nORI Z IS U AND Y IS N\n"
        "POS E 0 N 0 U 500\n"
    )
    prims = parse_primitives(script, "205-PU-004", simple_tag=True)
    assert [p["kind"] for p in prims] == ["CYLI"]


def test_primitives_of_other_equipment_are_excluded():
    """Membership follows the tree: an EQUI closes the previous one."""
    script = (
        "NEW EQUI /205_PU_004\n"
        "NEW CYLI\nDIAM 400\nHEIG 200\nORI Z IS U AND Y IS N\n"
        "POS E 0 N 0 U 100\n"
        "NEW EQUI /205_PU_009\n"
        "NEW CYLI\nDIAM 999\nHEIG 999\nORI Z IS U AND Y IS N\n"
        "POS E 0 N 0 U 100\n"
    )
    prims = parse_primitives(script, "205-PU-004", simple_tag=True)
    assert len(prims) == 1
    assert prims[0]["diam"] == 400.0


def test_dish_spans_from_its_rim_plane_not_a_centre():
    """
    IR-1: a DISH is positioned by its flat rim, every other primitive by its
    centre. Getting this wrong moves a head by half its height.
    """
    dish_up = {
        "kind": "DISH", "axis": "U", "east": 0.0, "north": 0.0, "up": 1000.0,
        "diam": 2000.0, "heig": 400.0,
    }
    # Rim at U 1000, body rising to 1400: the lowest point is the rim itself.
    assert lowest_point(dish_up) == pytest.approx(1000.0)
    assert bounds_of(dish_up)[5] == pytest.approx(1400.0)

    cyli = dict(dish_up, kind="CYLI")
    # A CYLI at the same POS is centred there, so it hangs 200 below.
    assert lowest_point(cyli) == pytest.approx(800.0)


def test_horizontal_cylinder_is_bounded_by_its_radius():
    prim = {
        "kind": "CYLI", "axis": "E", "east": 0.0, "north": 0.0, "up": 500.0,
        "diam": 300.0, "heig": 1000.0,
    }
    e_min, e_max, n_min, n_max, u_min, u_max = bounds_of(prim)
    assert (e_min, e_max) == pytest.approx((-500.0, 500.0))   # along the axis
    assert (n_min, n_max) == pytest.approx((-150.0, 150.0))   # radius
    assert (u_min, u_max) == pytest.approx((350.0, 650.0))    # radius


def test_rotated_box_is_bounded_by_its_enclosing_extent():
    """A BOX rotated in plan must report a conservative, larger footprint."""
    square = {
        "kind": "BOX", "axis": "U", "east": 0.0, "north": 0.0, "up": 0.0,
        "xlen": 100.0, "ylen": 100.0, "zlen": 10.0, "plan_rotation_deg": 45.0,
    }
    e_min, e_max, *_ = bounds_of(square)
    assert e_max == pytest.approx(100.0 * (2 ** 0.5) / 2.0)
    assert e_min == pytest.approx(-e_max)


def test_equipment_names_collapse_runs_of_punctuation():
    assert equipment_name_to_element("205-PU-004") == "205_PU_004"
    assert equipment_name_to_element("PUMP A -- B") == "PUMP_A_B"


def test_malformed_plan_bearing_raises_rather_than_defaulting():
    """
    A bad bearing must not quietly resolve to 0 deg, which would place a
    rotated BOX on the wrong axis and still verify clean.
    """
    assert parse_plan_direction("E") == 0.0
    assert parse_plan_direction("N 30 W") == pytest.approx(120.0)
    for bad in ("N 30 Q", "N 95 W", "sideways"):
        with pytest.raises(ValueError):
            parse_plan_direction(bad)


def test_nozzles_are_parsed_with_face_and_binding():
    script = _macro(
        "NEW NOZZLE /205_PU_004_SUCTION_NOZZLE\n"
        "CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY\n"
        "HEIG 250\nORI P1 IS E\nPOS E 100 N 0 U 700\nEND\n"
    )
    nozzles = parse_nozzles(script, "205_PU_004")
    assert len(nozzles) == 1
    assert nozzles[0]["axis"] == "E"
    assert nozzles[0]["face"] == (100.0, 0.0, 700.0)
    assert nozzles[0]["catref"].endswith("AAZFBB0YY")
