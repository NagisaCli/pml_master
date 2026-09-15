"""
Property tests for the 203-TA-024 GA rebuild (Projects/JK-Tank_Build).

The tool resolves GA drawing 203-TA-024-GA-001 into an EquipmentModel, emits
the EQUI in the END-closed native form and splices it into the R9 listing.
These tests pin the drawing dimensions, the datum rules (IR-4/IR-6/IR-8) and
the byte-preservation of everything else in the baseline.
"""

from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "Projects" / "JK-Tank_Build" / "tools"
sys.path.insert(0, str(TOOLS))

import reactor_203_ta_024_ga as tool  # noqa: E402

from wsb.composite_builder import (  # noqa: E402
    validate_equipment_model,
    verify_equipment_macro,
)
from wsb.pml_builder import validate_pml  # noqa: E402
from wsb.pml_parser import parse_nozzles, parse_primitives  # noqa: E402


@lru_cache(maxsize=1)
def _generated():
    return tool.generate(write=False)


def _model():
    return _generated()[0]


def _macro():
    return _generated()[1]


def _listing():
    return _generated()[2]


# -- resolved model ---------------------------------------------------------


def test_model_validates_and_counts():
    model = _model()
    validate_equipment_model(model)
    counts = tool.group_counts(model)
    assert counts == {"SUPPORT": 60, "SHELL": 4, "ACCESS": 141}
    assert model.primitive_count == 205
    assert model.nozzle_count == 11
    assert model.position == (12005.0, -3752.0, 0.0)


def test_drawing_dimensions_drive_the_body():
    model = _model()
    body = [p for p in model.primitives if p.role == "body"]
    assert [p.kind for p in body] == ["CYLI", "CONE", "CYLI", "DISH"]
    spool, cone, shell, head = body
    assert (cone.d_bottom, cone.d_top) == (450.0, 2000.0)
    assert cone.bounds()[4:] == (1200.0, 4000.0)          # cone tangent 4000
    assert shell.diameter == 2000.0 and shell.height == 15600.0
    assert shell.bounds()[4:] == (4000.0, 19600.0)        # head tangent 19600
    assert head.height == 700.0 and head.bounds()[5] == 20300.0   # overall H
    assert model.body_envelope == (-1000.0, 1000.0, -1000.0, 1000.0, 300.0, 20300.0)


def test_bottom_datum_and_extent():
    model = _model()
    bounds = [p.bounds() for p in model.primitives]
    assert min(b[4] for b in bounds) == 0.0                # IR-6: nothing below
    assert max(b[5] for b in bounds) == tool.STRINGER_TOP_U
    assert model.overall_height == tool.STRINGER_TOP_U


@pytest.mark.parametrize(
    "mark, wall_radius, axis",
    [("N2", 1000.0, "W"), ("N3", 1000.0, "E"), ("N4", 1000.0, "E"),
     ("N5", 1000.0, "W"), ("N6", 1000.0, "W"), ("N10", 225.0, "W"),
     ("M1", 1000.0, "S")],
)
def test_side_nozzles_penetrate_the_wall_by_100(mark, wall_radius, axis):
    nozzle = next(n for n in _model().native_nozzles if n.name == mark)
    e, n, _u = nozzle.face
    face_radius = math.hypot(e, n)
    assert nozzle.axis == axis
    assert face_radius - nozzle.height == pytest.approx(wall_radius - 100.0)


def test_vertical_nozzles_root_inside_the_heads():
    model = _model()
    by_name = {n.name: n for n in model.native_nozzles}
    top = by_name["N1"]
    assert top.axis == "U" and top.face[2] - top.height == 20300.0 - 100.0
    bottom = by_name["N9"]
    assert bottom.axis == "D" and bottom.face == (0.0, 0.0, 0.0)
    assert bottom.face[2] + bottom.height == tool.SPOOL_BASE + 100.0
    for mark in ("N7", "N8"):
        inst = by_name[mark]
        assert inst.axis == "U"
        assert math.hypot(inst.face[0], inst.face[1]) == pytest.approx(400.0)
        assert inst.face[2] == 20530.0


def test_nozzle_schedule_matches_the_drawing_list():
    dn = {n.name: n.dn for n in _model().native_nozzles}
    assert dn == {"N1": 300, "N2": 100, "N3": 50, "N4": 25, "N5": 80, "N6": 80,
                  "N7": 50, "N8": 80, "N9": 300, "N10": 150, "M1": 600}


def test_legs_are_sheared_prisms_from_base_plate_to_cap():
    legs = [p for p in _model().primitives if p.kind == "PYRAMID" and p.xbot == 200.0]
    assert len(legs) == 4
    for leg in legs:
        assert leg.xoff == -450.0 and leg.yoff == 0.0
        b = leg.bounds()
        assert b[4] == 25.0 and b[5] == 4400.0
        centre_r = math.hypot(leg.point[0], leg.point[1])
        assert centre_r == pytest.approx(1375.0)
        # Local X must point radially outward so the -450 offset splays inward.
        radial_deg = math.degrees(math.atan2(leg.point[1], leg.point[0])) % 360.0
        assert leg.plan_rotation_deg == pytest.approx(radial_deg)


def test_anchor_bolts_sit_on_the_base_plates():
    prims = _model().primitives
    studs = [p for p in prims if p.kind == "CYLI" and p.diameter == 30.0]
    nuts = [p for p in prims if p.label.startswith("Hex nut")]
    assert len(studs) == 16 and len(nuts) == 16
    for stud in studs:
        assert stud.bounds()[4] == 0.0 and stud.bounds()[5] == 79.0
    for nut in nuts:
        assert nut.bounds()[4] == 25.0 and nut.bounds()[5] == 49.0


def test_cage_hoops_clear_the_landings():
    hoops = tool.hoop_elevations()
    assert len(hoops) == 11
    for u in hoops:
        for floor, _span in tool.LANDINGS:
            assert not (floor <= u <= floor + 1000.0)
    assert 6000.0 not in hoops and 13200.0 not in hoops


def test_ladder_clears_the_legs():
    """The stringers sit between the 90 and 135 deg legs, not on one."""
    assert tool.LADDER_BEARING not in tool.LEG_BEARINGS
    assert min(abs(tool.LADDER_BEARING - b) for b in tool.LEG_BEARINGS) >= 22.5


# -- emitted macro ----------------------------------------------------------


def test_macro_verifies_numerically_and_validates():
    model, macro, _listing = _generated()
    assert validate_pml(macro) == []
    assert verify_equipment_macro(model, macro) == []
    assert len(parse_primitives(macro, tool.NAME)) == 205
    assert len(parse_nozzles(macro, tool.NAME)) == 11


def test_macro_keeps_the_baseline_equi_frame():
    macro = _macro()
    assert "NEW EQUI /203_TA_024\nPOS E 51267.0 N 58841.0 U -300.0\nFUNC '001024'" in macro
    assert macro.count("NEW SUBE /203_TA_024_") == 14      # SUPPORT, SHELL, 11 nozzles, ACCESS
    assert macro.count("CATR SPCOMPONENT /150lb_Ansi_Flanged/") == 11


def test_structure_block_is_native_form():
    macro = _macro()
    assert "NEW STRUCTURE /203_TA_024_STRU\nPOS E 51267mm N 58841mm U 0mm" in macro
    assert "NEW FRMWORK /203_TA_024_FRMWORK" in macro
    assert macro.count("NEW HANDRA /203_TA_024_") == 5
    assert "NEW HANDRA /203_TA_024_TOP_HANDRAIL\nPOS E 12005mm S 3752mm U 19350mm" in macro
    assert macro.count("RAILHE 1100mm 550mm") == 5


def test_top_handrail_ties_into_the_stringers():
    spec = tool.top_rail_spec()
    first = spec.path_items[0].position
    last = spec.path_items[-1].position
    for pt, y in ((first, -240.0), (last, 240.0)):
        e, n = tool.ladder_to_local(1250.0, y)
        assert pt[0] == pytest.approx(e) and pt[1] == pytest.approx(n)
    assert spec.start_direction and spec.end_direction
    # Local elevation of the rail is the floor top; HANDRA POS carries the
    # EQUI's D 300 so the world elevation matches the EQUI-local primitives.
    assert spec.position[2] == 19650.0 - 300.0


def test_cage_hoop_attaches_seamlessly_to_stringers():
    """Assert each hoop profile starts and ends at the ladder stringers with 0 gap."""
    profile = tool.hoop_profile()
    str_b = tool.ladder_to_local(tool.STRINGER_X, tool.STRINGER_Y)
    assert profile[0][0] == pytest.approx(str_b[0]) and profile[0][1] == pytest.approx(str_b[1])
    str_a = tool.ladder_to_local(tool.STRINGER_X, -tool.STRINGER_Y)
    mid_idx = len(profile) // 2 - 1
    assert profile[mid_idx][0] == pytest.approx(str_a[0]) and profile[mid_idx][1] == pytest.approx(str_a[1])


def test_top_handrail_parallel_radial_arms():
    """Assert the top handrail return arms run parallel along y = +-240 mm (pure radial)."""
    spec = tool.top_rail_spec()
    assert spec.start_direction == "S 67.5 E"
    assert spec.end_direction == "N 67.5 W"


# -- spliced listing --------------------------------------------------------


def test_listing_preserves_everything_else():
    baseline = tool.read_baseline().split("\n")
    listing = _listing().split("\n")
    s, e = baseline.index("NEW EQUIPMENT /203_TA_024"), baseline.index("NEW EQUIPMENT /203_TA_029")
    s2, e2 = listing.index("NEW EQUI /203_TA_024"), listing.index("NEW EQUIPMENT /203_TA_029")
    assert baseline[:s] == listing[:s2]
    ob = baseline.index("OLD NOZZLE /203_TA_024_N1_NOZZ")
    oe = baseline.index("OLD NOZZLE /203_TA_024_M1_NOZZ") + 3
    nb = listing.index("OLD NOZZLE /203_TA_024_N1_NOZZ")
    ne = listing.index("OLD NOZZLE /203_TA_024_M1_NOZZ") + 3
    assert baseline[e:ob] == listing[e2:nb]
    assert baseline[oe:] == listing[ne:]
    assert (oe - ob, ne - nb) == (18, 33)                  # 6 -> 11 rebinding entries
    assert not any(line.startswith("--") for line in listing[s2:e2])


def test_written_outputs_match_the_generator():
    macro = tool.OUTPUT_MACRO.read_text(encoding="utf-8")
    generated = _macro()
    strip = lambda text: "\n".join(l for l in text.split("\n") if not l.startswith("-- Generated:"))
    assert strip(macro) == strip(generated)
    raw = tool.OUTPUT_LISTING.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf") and b"\r\n" in raw
    assert raw[3:].decode("utf-8").replace("\r\n", "\n") == _listing()
