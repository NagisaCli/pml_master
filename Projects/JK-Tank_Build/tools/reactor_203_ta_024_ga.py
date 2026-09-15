"""
203-TA-024 1st Oxygen Reactor, rebuilt from GA drawing 203-TA-024-GA-001 Rev A.

The drawing (2024-06-07, N.T.S., "for 3D modeling only") supersedes the
legacy ``equipment_data.py`` TankSpec for this item. This tool resolves it
into an :class:`~wsb.composite_schema.EquipmentModel`, emits the EQUI in the
END-closed native listing form the WSB_TA baseline uses, adds the access
handrails as a STRU/FRMWORK/HANDRA block, splices both into the R9 baseline
and writes the review report.

Frames
------
* **Drawing bearings**: 0 deg = plant North, clockwise (90 = E, 180 = S,
  270 = W). This is the reading of the drawing's top view and is a
  Reference assumption recorded in the report.
* **Builder bearings**: East towards North, as ``PMLBuilder`` expects.
  ``math_angle = 90 - drawing_bearing``.
* **Equipment-local**: origin at the vessel bottom centre (bottom outlet
  flange face, drawing elevation 0). ``BOTTOM_CENTRE`` places it in the EQUI
  frame; the EQUI itself keeps the baseline's owner-relative POS.
* **Ladder frame**: x radial outward along the ladder bearing, y tangential
  (counter-clockwise), used for every ladder, cage, floor and rail point and
  rotated into E/N once.

Datums (IR-4): CYLI/CONE by base-face centre in the spec (the builder moves
them to the geometric centre), DISH by rim plane, BOX/PYRAMID by geometric
centre, EXTRUSION by profile end plane, NOZZLE by flange face.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

BASE = Path(__file__).resolve().parent.parent          # Projects/JK-Tank_Build
REPO_ROOT = BASE.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from wsb.composite_builder import (  # noqa: E402
    emit_equipment,
    validate_equipment_model,
    verify_equipment_macro,
)
from wsb.composite_schema import (  # noqa: E402
    EquipmentModel,
    NativeNozzleSpec,
    ParameterRecord,
    PrimitiveSpec,
    ReferenceValue,
    SourceRecord,
)
from wsb.handrail_builder import (  # noqa: E402
    HandrailBuilder,
    HandrailSpec,
    RouteCurve,
    RoutePoint,
)
from wsb.pml_builder import (  # noqa: E402
    PMLBuilder,
    _plan_direction,
    nozzle_component_path,
    validate_pml,
)
from wsb.pml_parser import parse_nozzles, parse_primitives  # noqa: E402

Point = Tuple[float, float, float]

# ---------------------------------------------------------------------------
# Identity and baseline continuation
# ---------------------------------------------------------------------------

REVISION_DATE = "20260911"
NAME = "203_TA_024"
DISPLAY_NAME = "203-TA-024 1st Oxygen Reactor"
DRAWING = "203-TA-024-GA-001 Rev A (2024-06-07, N.T.S.)"

BASELINE = BASE / "output" / "WSB_TA_relocate_20260902.txt"
OUTPUT_MACRO = BASE / "output" / f"203_TA_024_GA_{REVISION_DATE}.pml"
OUTPUT_LISTING = BASE / "output" / f"WSB_TA_203_TA_024_GA_{REVISION_DATE}.txt"
OUTPUT_REPORT = BASE / "output" / f"203_TA_024_GA_{REVISION_DATE}_report.md"

#: The EQUI's owner-relative POS in the R9 baseline (``POS E 51267mm N 58841mm
#: D 300mm``). Reproduced exactly or the whole reactor moves.
EQUI_POSITION: Point = (51267.0, 58841.0, -300.0)
#: Vessel bottom centre in the EQUI frame, unchanged from the baseline.
BOTTOM_CENTRE: Point = (12005.0, -3752.0, 0.0)
#: Attribute lines every EQUI/SUBE in the native export carries.
NATIVE_ATTRIBUTES = (
    "FUNC '001024'",
    "BUIL false",
    "DSCO unset",
    "PTSP unset",
    "INSC unset",
)
NEXT_EQUIPMENT = "203_TA_029"
STRU_NAME = f"{NAME}_STRU"
FRMWORK_NAME = f"{NAME}_FRMWORK"

# ---------------------------------------------------------------------------
# Drawing data (KEY DIMENSIONS / PROCESS DATA, mm)
# ---------------------------------------------------------------------------

OVERALL_HEIGHT = 20300.0
SHELL_OD = 2000.0
HEAD_HEIGHT = 700.0
SHELL_HEIGHT = 15600.0
CONE_SECTION_HEIGHT = 4000.0
EL_TOP_NOZZLE = 20300.0
EL_TOP_TANGENT = 19600.0
EL_CONE_TANGENT = 4000.0
EL_BOTTOM_OUTLET = 0.0
VOLUME_M3 = 49.0
TEMPERATURE_C = 91.0
RETENTION_MIN = 20.0
CONSISTENCY_PCT = 11.0

SHELL_R = SHELL_OD / 2.0
WALL_PENETRATION = 100.0       # nozzle root inside the wall (IR-8)

# ---------------------------------------------------------------------------
# Reference Values (not on the drawing - basis recorded in the report)
# ---------------------------------------------------------------------------

SPOOL_D = 450.0                # lower transition spool, DN300 outlet + wall
SPOOL_BASE = 300.0             # bottom outlet nozzle (HEIG 400) roots at 400
SPOOL_HEIGHT = 900.0           # spool 300..1200, cone 1200..4000
CONE_BASE = SPOOL_BASE + SPOOL_HEIGHT
CONE_HEIGHT = EL_CONE_TANGENT - CONE_BASE
HEAD_RADIUS = SHELL_OD          # project DISH form (JK-Tank_Build R1..R9)

LEG_BEARINGS = (45.0, 135.0, 225.0, 315.0)
LEG_SIZE = 200.0
LEG_BASE_U = 25.0               # on the base plate
LEG_TOP_U = 4400.0
LEG_BASE_R = 1600.0
LEG_TOP_R = 1150.0
BASE_PLATE = (400.0, 400.0, 25.0)
CAP_PLATE = (300.0, 300.0, 20.0)
CAP_PLATE_R = 1100.0
GUSSET = (250.0, 16.0, 400.0)
GUSSET_R = 1125.0
BOLT_OFFSET = 140.0
STUD_D = 30.0
STUD_LENGTH = 79.0              # plate 25 + nut 24 + 1 d projection
NUT_AF = 46.0
NUT_HEIGHT = 24.0
TIE_U = 2200.0
TIE_SECTION = (80.0, 120.0)     # width (radial), depth (vertical)
TIE_END_SETBACK = 100.0         # ends at the leg face
BRACE_SIZE = 60.0
BRACE_LOW_U = 300.0
BRACE_END_SETBACK = 150.0

LADDER_BEARING = 112.5          # between the 90 and 135 deg legs, clear of both
STRINGER_D = 42.4
STRINGER_X = 1250.0
STRINGER_Y = 240.0
STRINGER_BASE_U = 16.0          # on the shoe
STRINGER_TOP_U = 20750.0        # 1150 above the top floor (safety extension)
SHOE = (120.0, 120.0, 16.0)
RUNG = (25.0, 480.0, 25.0)
RUNG_FIRST_U = 300.0
RUNG_LAST_U = 19500.0
RUNG_PITCH = 300.0
STANDOFF_PAD = (14.0, 100.0, 100.0)   # radial thickness, width, height
STANDOFF_ARM = 30.0
STANDOFF_EMBED = 5.0
CONE_STANDOFF_U = (2400.0, 3600.0)
SHELL_STANDOFF_U = tuple(float(u) for u in range(4800, 19201, 2400))
HOOP_FLAT_HEIGHT = 50.0
HOOP_FLAT_THICK = 6.0
HOOP_STRAIGHT_X = (1250.0, 1550.0)    # legs from the rung line back
HOOP_R = 350.0
HOOP_FIRST_U = 2400.0
HOOP_LAST_U = 19200.0
HOOP_PITCH = 1200.0
LANDING_CLEAR_ABOVE = 1000.0          # no hoop within [L, L + 1000]
STRAP_SECTION = (6.0, 30.0)
STRAP_ANGLES = (0.0, 45.0, 80.0, -45.0)   # about the hoop arc centre
STRAP_LOW_U = HOOP_FIRST_U - HOOP_FLAT_HEIGHT / 2.0
STRAP_HIGH_U = HOOP_LAST_U + HOOP_FLAT_HEIGHT / 2.0
FLOOR_R = (1000.0, 1800.0)
TOP_FLOOR_U = EL_TOP_TANGENT
TOP_FLOOR_THICK = 50.0
TOP_FLOOR_GAP_HALF = 17.0             # deg each side of the ladder axis
FLOOR_BRACKET = (780.0, 12.0, 250.0)
FLOOR_BRACKET_R = 1400.0
FLOOR_BRACKET_BEARINGS = tuple(float(b) for b in range(0, 360, 45))
LANDING_THICK = 40.0
LANDING_BRACKET = (780.0, 12.0, 200.0)
#: (floor elevation, angular span) - all on the -y side of the ladder,
#: starting at the top-floor gap edge. The 12500 landing is sized to reach
#: the manway; the others are exit landings for the caged ladder.
LANDINGS = ((5900.0, 37.0), (9200.0, 37.0), (12500.0, 74.0), (15900.0, 37.0))
LANDING_START = -17.0
ARC_STEP_DEG = 3.0

RAIL_TOP = 1100.0
RAIL_MID = 550.0
RAIL_R = FLOOR_R[1] - 60.0
RAIL_LINK_R = 1250.0                  # gap-edge point level with the stringers
LANDING_RAIL_NEAR_R = 1560.0          # opening between shell and this post
LANDING_RAIL_FAR_R = FLOOR_R[0] + 60.0

MANWAY_DN = 600
MANWAY_U = 13300.0
MANWAY_HEIG = 450.0

# ---------------------------------------------------------------------------
# Frame helpers
# ---------------------------------------------------------------------------


def math_angle(bearing_deg: float) -> float:
    """Drawing bearing (N = 0, clockwise) to builder bearing (E = 0, CCW)."""
    return (90.0 - bearing_deg) % 360.0


def _snap(value: float) -> float:
    """Kill the -0.0 that cardinal bearings leave behind."""
    return 0.0 if abs(value) < 1e-9 else value


def radial(bearing_deg: float, r: float) -> Tuple[float, float]:
    """Plan point at radius ``r`` on a drawing bearing."""
    a = math.radians(bearing_deg)
    return _snap(r * math.sin(a)), _snap(r * math.cos(a))


def rotate(x: float, y: float, deg: float) -> Tuple[float, float]:
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return _snap(c * x - s * y), _snap(s * x + c * y)


LADDER_ANGLE = math_angle(LADDER_BEARING)   # -22.5 deg -> 337.5


def ladder_to_local(x: float, y: float) -> Tuple[float, float]:
    """Ladder frame (x radial, y tangential CCW) to equipment-local E/N."""
    return rotate(x, y, LADDER_ANGLE)


def polar(angle_deg: float, r: float) -> Tuple[float, float]:
    a = math.radians(angle_deg)
    return r * math.cos(a), r * math.sin(a)


def arc_points(r: float, start_deg: float, end_deg: float, step: float = ARC_STEP_DEG):
    """Points along an arc from start to end (either direction), both ends included."""
    sweep = end_deg - start_deg
    count = max(1, int(math.ceil(abs(sweep) / step)))
    return [polar(start_deg + sweep * k / count, r) for k in range(count + 1)]


def cone_radius(u: float) -> float:
    """Outer radius of the lower cone at elevation ``u``."""
    t = (u - CONE_BASE) / CONE_HEIGHT
    return SPOOL_D / 2.0 + (SHELL_R - SPOOL_D / 2.0) * t


def leg_radius(u: float) -> float:
    """Leg centreline radius at elevation ``u`` (linear splay)."""
    t = (u - LEG_BASE_U) / (LEG_TOP_U - LEG_BASE_U)
    return LEG_BASE_R + (LEG_TOP_R - LEG_BASE_R) * t


# ---------------------------------------------------------------------------
# Body
# ---------------------------------------------------------------------------


def build_shell() -> List[PrimitiveSpec]:
    g = "SHELL"
    return [
        PrimitiveSpec.cyli(
            g, SPOOL_D, SPOOL_HEIGHT, (0.0, 0.0, SPOOL_BASE),
            "Lower transition spool D450 (Reference)", role="body",
        ),
        PrimitiveSpec.cone(
            g, SPOOL_D, SHELL_OD, CONE_HEIGHT, (0.0, 0.0, CONE_BASE),
            "Bottom cone 1200..4000 (drawing: cone + lower transition 4000)",
            role="body",
        ),
        PrimitiveSpec.cyli(
            g, SHELL_OD, SHELL_HEIGHT, (0.0, 0.0, EL_CONE_TANGENT),
            "Straight shell OD 2000 x 15600 (4000..19600)", role="body",
        ),
        PrimitiveSpec.dish(
            g, SHELL_OD, HEAD_HEIGHT, (0.0, 0.0, EL_TOP_TANGENT),
            "Top head, rim 19600, apex 20300", radius=HEAD_RADIUS, role="body",
        ),
    ]


BODY_ENVELOPE = (-SHELL_R, SHELL_R, -SHELL_R, SHELL_R, SPOOL_BASE, OVERALL_HEIGHT)

# ---------------------------------------------------------------------------
# Support: four splayed legs, ties, X-bracing, anchor bolts
# ---------------------------------------------------------------------------


def build_support() -> List[PrimitiveSpec]:
    g = "SUPPORT"
    out: List[PrimitiveSpec] = []
    leg_height = LEG_TOP_U - LEG_BASE_U
    for bearing in LEG_BEARINGS:
        a = math_angle(bearing)
        tag = f"leg {bearing:g} deg"
        cx, cy = radial(bearing, (LEG_BASE_R + LEG_TOP_R) / 2.0)
        out.append(PrimitiveSpec.pyramid(
            g, LEG_SIZE, LEG_SIZE, LEG_SIZE, LEG_SIZE, leg_height,
            (cx, cy, (LEG_BASE_U + LEG_TOP_U) / 2.0),
            f"Support {tag}: 200x200 sheared prism, base r1600 -> top r1150",
            xoff=LEG_TOP_R - LEG_BASE_R, plan_rotation_deg=a, role="support",
        ))
        px, py = radial(bearing, CAP_PLATE_R)
        out.append(PrimitiveSpec.box(
            g, *CAP_PLATE, (px, py, LEG_TOP_U + CAP_PLATE[2] / 2.0),
            f"Cap plate {tag}", plan_rotation_deg=a, role="support",
        ))
        gx, gy = radial(bearing, GUSSET_R)
        out.append(PrimitiveSpec.box(
            g, *GUSSET, (gx, gy, LEG_TOP_U - GUSSET[2] / 2.0),
            f"Gusset {tag}", plan_rotation_deg=a, role="support",
        ))
        bx, by = radial(bearing, LEG_BASE_R)
        out.append(PrimitiveSpec.box(
            g, *BASE_PLATE, (bx, by, BASE_PLATE[2] / 2.0),
            f"Base plate {tag}", plan_rotation_deg=a, role="support",
        ))
        for i, (ox, oy) in enumerate(
            ((BOLT_OFFSET, BOLT_OFFSET), (-BOLT_OFFSET, BOLT_OFFSET),
             (-BOLT_OFFSET, -BOLT_OFFSET), (BOLT_OFFSET, -BOLT_OFFSET)), 1
        ):
            dx, dy = rotate(ox, oy, a)
            out.append(PrimitiveSpec.cyli(
                g, STUD_D, STUD_LENGTH, (bx + dx, by + dy, 0.0),
                f"Anchor stud M30 {tag} #{i}", role="hardware",
            ))
            out.append(PrimitiveSpec.hex_nut(
                g, (bx + dx, by + dy, BASE_PLATE[2]), NUT_AF, NUT_HEIGHT,
                f"Hex nut M30 {tag} #{i}", rotation_deg=a,
            ))

    # Horizontal ties between adjacent legs, on the bay bisectors.
    tie_leg_r = leg_radius(TIE_U)
    chord_half = tie_leg_r * math.sin(math.radians(45.0))
    tie_length = 2.0 * (chord_half - TIE_END_SETBACK)
    for bisector in (0.0, 90.0, 180.0, 270.0):
        a = math_angle(bisector)
        tx, ty = radial(bisector, tie_leg_r * math.cos(math.radians(45.0)))
        out.append(PrimitiveSpec.box(
            g, tie_length, TIE_SECTION[0], TIE_SECTION[1], (tx, ty, TIE_U),
            f"Horizontal tie, bay bisector {bisector:g} deg",
            plan_rotation_deg=a - 90.0, role="support",
        ))

    # X-bracing in every bay between the base and the tie level. Local X is
    # the chord direction, local Y the bay bisector (radial outward).
    low_leg_r = leg_radius(BRACE_LOW_U)
    low_half = low_leg_r * math.sin(math.radians(45.0))
    low_mid_r = low_leg_r * math.cos(math.radians(45.0))
    high_half = chord_half
    high_mid_r = tie_leg_r * math.cos(math.radians(45.0))
    s_low = low_half - BRACE_END_SETBACK
    s_high = high_half - BRACE_END_SETBACK
    for bisector in (0.0, 90.0, 180.0, 270.0):
        a = math_angle(bisector)
        for sign, tag in ((1.0, "rising"), (-1.0, "falling")):
            s0, s1 = -sign * s_low, sign * s_high
            r0, r1 = low_mid_r, high_mid_r
            centre_s, centre_r = (s0 + s1) / 2.0, (r0 + r1) / 2.0
            ex, ey = rotate(centre_s, centre_r, a - 90.0)
            out.append(PrimitiveSpec.pyramid(
                g, BRACE_SIZE, BRACE_SIZE, BRACE_SIZE, BRACE_SIZE,
                TIE_U - BRACE_LOW_U,
                (ex, ey, (BRACE_LOW_U + TIE_U) / 2.0),
                f"Diagonal brace ({tag}), bay bisector {bisector:g} deg",
                xoff=s1 - s0, yoff=r1 - r0, plan_rotation_deg=a - 90.0,
                role="support",
            ))
    return out


# ---------------------------------------------------------------------------
# Access: caged ladder, standoffs, top floor, landings
# ---------------------------------------------------------------------------


def hoop_elevations() -> List[float]:
    hoops = []
    u = HOOP_FIRST_U
    while u <= HOOP_LAST_U + 1e-6:
        blocked = any(L <= u <= L + LANDING_CLEAR_ABOVE for L, _span in LANDINGS)
        if not blocked:
            hoops.append(u)
        u += HOOP_PITCH
    return hoops


def hoop_profile() -> List[Tuple[float, float]]:
    """Flared D-shaped flat-bar ring starting directly at the ladder stringers (y = +-240)."""
    x_str = STRINGER_X
    y_str = STRINGER_Y
    x_flare0 = x_str + 30.0
    x_flare1 = 1390.0
    x_arc_c = 1550.0
    r_out = HOOP_R + HOOP_FLAT_THICK / 2.0
    r_in = HOOP_R - HOOP_FLAT_THICK / 2.0

    # Outer boundary (starts at Stringer B at y = +240, ends at Stringer A at y = -240):
    pts = [(x_str, y_str), (x_flare0, y_str), (x_flare1, r_out), (x_arc_c, r_out)]
    pts += [(x_arc_c + px, py) for px, py in arc_points(r_out, 90.0, -90.0)][1:-1]
    pts += [(x_arc_c, -r_out), (x_flare1, -r_out), (x_flare0, -y_str), (x_str, -y_str)]

    # Inner boundary (offset by thickness 6mm):
    y_str_in = y_str - HOOP_FLAT_THICK
    y_flare1_in = r_out - HOOP_FLAT_THICK
    pts += [(x_str, -y_str_in), (x_flare0, -y_str_in), (x_flare1, -y_flare1_in), (x_arc_c, -r_in)]
    pts += [(x_arc_c + px, py) for px, py in arc_points(r_in, -90.0, 90.0)][1:-1]
    pts += [(x_arc_c, r_in), (x_flare1, y_flare1_in), (x_flare0, y_str_in), (x_str, y_str_in)]
    return [ladder_to_local(x, y) for x, y in pts]


def top_floor_profile() -> List[Tuple[float, float]]:
    """Annulus sector r 1000..1800 with rectangular ladder channel along y = +-240."""
    r_in, r_out = FLOOR_R
    y_open = STRINGER_Y
    x_in = math.sqrt(r_in * r_in - y_open * y_open)
    x_out = math.sqrt(r_out * r_out - y_open * y_open)
    ang_in = math.degrees(math.atan2(y_open, x_in))
    ang_out = math.degrees(math.atan2(y_open, x_out))

    outer = arc_points(r_out, ang_out, 360.0 - ang_out)
    edge_a = [(x_out, -y_open), (x_in, -y_open)]
    inner = arc_points(r_in, 360.0 - ang_in, ang_in)
    edge_b = [(x_in, y_open), (x_out, y_open)]
    return [ladder_to_local(x, y) for x, y in outer + edge_a + inner + edge_b]


def ring_sector_profile(start_deg: float, end_deg: float) -> List[Tuple[float, float]]:
    """Annulus sector r 1000..1800 between two ladder-frame angles."""
    r_in, r_out = FLOOR_R
    outer = arc_points(r_out, start_deg, end_deg)
    inner = arc_points(r_in, end_deg, start_deg)
    return [ladder_to_local(x, y) for x, y in outer + inner]


def landing_sector(span_deg: float) -> Tuple[float, float]:
    """Ladder-frame start/end angles of a landing (on the -y side)."""
    return LANDING_START, LANDING_START - span_deg


def build_access() -> List[PrimitiveSpec]:
    g = "ACCESS"
    out: List[PrimitiveSpec] = []
    a = LADDER_ANGLE

    for side, y in (("A", -STRINGER_Y), ("B", STRINGER_Y)):
        ex, ey = ladder_to_local(STRINGER_X, y)
        out.append(PrimitiveSpec.cyli(
            g, STRINGER_D, STRINGER_TOP_U - STRINGER_BASE_U,
            (ex, ey, STRINGER_BASE_U), f"Ladder stringer {side} CHS 42.4",
        ))
        out.append(PrimitiveSpec.box(
            g, *SHOE, (ex, ey, SHOE[2] / 2.0), f"Ladder shoe {side}",
            plan_rotation_deg=a,
        ))

    rx, ry = ladder_to_local(STRINGER_X, 0.0)
    u = RUNG_FIRST_U
    n = 1
    while u <= RUNG_LAST_U + 1e-6:
        out.append(PrimitiveSpec.box(
            g, *RUNG, (rx, ry, u), f"Rung {n} at U {u:g}", plan_rotation_deg=a,
        ))
        u += RUNG_PITCH
        n += 1

    def standoff(u: float, surface_x: float, tag: str) -> None:
        pad_x = surface_x + STANDOFF_PAD[0] / 2.0 - STANDOFF_EMBED
        arm_start = pad_x + STANDOFF_PAD[0] / 2.0
        arm_end = STRINGER_X + 2.0
        for side, y in (("A", -STRINGER_Y), ("B", STRINGER_Y)):
            px, py = ladder_to_local(pad_x, y)
            out.append(PrimitiveSpec.box(
                g, *STANDOFF_PAD, (px, py, u),
                f"Standoff pad {tag} {side}", plan_rotation_deg=a,
            ))
            mx, my = ladder_to_local((arm_start + arm_end) / 2.0, y)
            out.append(PrimitiveSpec.box(
                g, arm_end - arm_start, STANDOFF_ARM, STANDOFF_ARM, (mx, my, u),
                f"Standoff arm {tag} {side}", plan_rotation_deg=a,
            ))

    for u in CONE_STANDOFF_U:
        rc = cone_radius(u)
        standoff(u, math.sqrt(rc * rc - STRINGER_Y * STRINGER_Y), f"to cone U {u:g}")
    shell_surface_x = math.sqrt(SHELL_R * SHELL_R - STRINGER_Y * STRINGER_Y)
    for u in SHELL_STANDOFF_U:
        standoff(u, shell_surface_x, f"to shell U {u:g}")

    profile = hoop_profile()
    for u in hoop_elevations():
        out.append(PrimitiveSpec.extrusion(
            g, (0.0, 0.0, u - HOOP_FLAT_HEIGHT / 2.0), HOOP_FLAT_HEIGHT, profile,
            f"Cage hoop flat bar 50x6 at U {u:g}",
        ))

    strap_r = HOOP_R + HOOP_FLAT_THICK / 2.0 + STRAP_SECTION[0] / 2.0
    for theta in STRAP_ANGLES:
        sx = HOOP_STRAIGHT_X[1] + strap_r * math.cos(math.radians(theta))
        sy = strap_r * math.sin(math.radians(theta))
        ex, ey = ladder_to_local(sx, sy)
        out.append(PrimitiveSpec.box(
            g, STRAP_SECTION[0], STRAP_SECTION[1], STRAP_HIGH_U - STRAP_LOW_U,
            (ex, ey, (STRAP_LOW_U + STRAP_HIGH_U) / 2.0),
            f"Cage vertical strap at {theta:g} deg", plan_rotation_deg=a + theta,
        ))

    out.append(PrimitiveSpec.extrusion(
        g, (0.0, 0.0, TOP_FLOOR_U), TOP_FLOOR_THICK,
        top_floor_profile(),
        "Top platform floor ring r1000..1800 with ladder opening",
    ))
    for bearing in FLOOR_BRACKET_BEARINGS:
        bx, by = radial(bearing, FLOOR_BRACKET_R)
        out.append(PrimitiveSpec.box(
            g, *FLOOR_BRACKET, (bx, by, TOP_FLOOR_U - FLOOR_BRACKET[2] / 2.0),
            f"Top floor bracket {bearing:g} deg",
            plan_rotation_deg=math_angle(bearing),
        ))

    for L, span in LANDINGS:
        start, end = landing_sector(span)
        out.append(PrimitiveSpec.extrusion(
            g, (0.0, 0.0, L), LANDING_THICK, ring_sector_profile(start, end),
            f"Access landing at U {L:g}, span {span:g} deg",
        ))
        for k in (1, 3):
            theta = start - span * k / 4.0
            bx, by = ladder_to_local(*polar(theta, FLOOR_BRACKET_R))
            out.append(PrimitiveSpec.box(
                g, *LANDING_BRACKET, (bx, by, L - LANDING_BRACKET[2] / 2.0),
                f"Landing bracket U {L:g} #{(k + 1) // 2}",
                plan_rotation_deg=a + theta,
            ))
    return out


# ---------------------------------------------------------------------------
# Nozzles (From P&ID list on the drawing)
# ---------------------------------------------------------------------------


def _side_face(bearing: float, u: float, heig: float, wall_r: float = SHELL_R) -> Point:
    x, y = radial(bearing, wall_r - WALL_PENETRATION + heig)
    return (x, y, u)


HEAD_INSTRUMENT_R = 400.0
HEAD_INSTRUMENT_FACE_U = 20530.0
HEAD_INSTRUMENT_HEIG = 400.0

NOZZLES: Tuple[Tuple[str, str, int, float, str, Point], ...] = (
    # group, P&ID tag / service, DN, HEIG, axis, face (local)
    ("N1", "Top outlet to 2nd stage (DN as per line; Reference DN300)", 300,
     500.0, "U", (0.0, 0.0, OVERALL_HEIGHT + 400.0)),
    ("N2", "BF8-131 top/upper shell 270 deg", 100, 300.0, "W",
     _side_face(270.0, 19100.0, 300.0)),
    ("N3", "CH2-122 upper shell 90 deg", 50, 250.0, "E",
     _side_face(90.0, 17600.0, 250.0)),
    ("N4", "BK19-125 mid shell 90 deg", 25, 250.0, "E",
     _side_face(90.0, 12300.0, 250.0)),
    ("N5", "PIS-3524 instrument connection, upper shell 270 deg (Reference DN80)",
     80, 300.0, "W", _side_face(270.0, 15900.0, 300.0)),
    ("N6", "PD-3523 instrument connection, lower shell 270 deg (Reference DN80)",
     80, 300.0, "W", _side_face(270.0, 5300.0, 300.0)),
    ("N7", "TI-3535 temperature indicator, top head (Reference DN50)", 50,
     HEAD_INSTRUMENT_HEIG, "U",
     (*radial(315.0, HEAD_INSTRUMENT_R), HEAD_INSTRUMENT_FACE_U)),
    ("N8", "PI-3536 pressure indicator, top head (Reference DN80)", 80,
     HEAD_INSTRUMENT_HEIG, "U",
     (*radial(45.0, HEAD_INSTRUMENT_R), HEAD_INSTRUMENT_FACE_U)),
    ("N9", "Bottom outlet to Oxygen Mixer, bottom centre (table DN300)", 300,
     400.0, "D", (0.0, 0.0, EL_BOTTOM_OUTLET)),
    ("N10", "Bottom auxiliary, lower section side (as per P&ID)", 150, 300.0,
     "W", _side_face(270.0, 750.0, 300.0, wall_r=SPOOL_D / 2.0)),
    ("M1", "Manway (Reference DN600), shell 180 deg", MANWAY_DN, MANWAY_HEIG,
     "S", _side_face(180.0, MANWAY_U, MANWAY_HEIG)),
)


def build_nozzles() -> List[NativeNozzleSpec]:
    return [
        NativeNozzleSpec(group=g, name=g, dn=dn, height=h, face=face, axis=axis,
                         label=f"{g}: {label}")
        for g, label, dn, h, axis, face in NOZZLES
    ]


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

SOURCES = (
    SourceRecord("GA drawing", f"{DRAWING}, sheet 1 of 1 - key dimensions, "
                 "process data, nozzle/instrument list, elevation and top view"),
    SourceRecord("Baseline", "output/WSB_TA_relocate_20260902.txt (R9) - EQUI "
                 "position, attribute lines, element naming"),
    SourceRecord("Project convention", "skill/projects/jk-project-wsb.md - "
                 "anchor bolts, caged ladder, standoffs, structural HANDRA"),
)

PARAMETERS = (
    ParameterRecord("Overall height H", "20300 mm", "GA key dimensions"),
    ParameterRecord("Shell OD", "2000 mm", "GA key dimensions"),
    ParameterRecord("Top head height", "700 mm", "GA key dimensions"),
    ParameterRecord("Straight shell height", "15600 mm", "GA key dimensions"),
    ParameterRecord("Bottom cone & lower transition height", "4000 mm",
                    "GA key dimensions"),
    ParameterRecord("Top nozzle centreline elevation", "20300 mm", "GA key dimensions"),
    ParameterRecord("Top head to shell tangent elevation", "19600 mm",
                    "GA key dimensions"),
    ParameterRecord("Shell to cone tangent elevation", "4000 mm", "GA key dimensions"),
    ParameterRecord("Bottom outlet centreline elevation", "0 mm", "GA key dimensions"),
    ParameterRecord("Volume", "49 m3", "GA process data"),
    ParameterRecord("Temperature", "91 degC", "GA process data"),
    ParameterRecord("Retention", "20 min", "GA process data"),
    ParameterRecord("Consistency", "11 %", "GA process data"),
    ParameterRecord("EQUI position", "E 51267 N 58841 D 300 (owner-relative)",
                    "R9 baseline, unchanged"),
    ParameterRecord("Bottom centre (EQUI frame)", "E 12005 S 3752 U 0",
                    "R9 baseline, unchanged"),
)

REFERENCE_VALUES = (
    ReferenceValue("Bearing convention", "drawing 0 deg = plant North, clockwise",
                   "Top view reads as a compass rose; nozzle list gives 0/90/180/270"),
    ReferenceValue("Lower transition spool", "D450 x 900 (300..1200), cone 1200..4000",
                   "Drawing lumps cone and transition into 4000 mm; split scaled from the N.T.S. elevation"),
    ReferenceValue("Top head form", "DISH HEIG 700, RADIUS 2000",
                   "Project DISH convention (R1..R9); drawing gives height only"),
    ReferenceValue("N1 top outlet size", "DN300",
                   "Drawing: 'size as per line'; taken equal to the bottom outlet"),
    ReferenceValue("Bottom outlet size", "DN300",
                   "Nozzle list DN300; elevation label reads DN150 - conflict, table taken"),
    ReferenceValue("N2/N3/N4/N5/N6 elevations", "19100 / 17600 / 12300 / 15900 / 5300",
                   "Scaled from the N.T.S. elevation between tangents 4000 and 19600"),
    ReferenceValue("Instrument nozzle sizes", "PIS DN80, PD DN80, TI DN50, PI DN80",
                   "Not on drawing; typical instrument connections"),
    ReferenceValue("Head instrument positions", "r 400 at 45 and 315 deg, face U 20530",
                   "Drawing shows both on the top head, no offsets"),
    ReferenceValue("Manway", "DN600 at 180 deg, U 13300",
                   "Drawing shows a manway ~60 % up the shell, no size"),
    ReferenceValue("Support legs", "4 x 200x200 at 45/135/225/315, base r1600, top r1150, ties at 2200, X-bracing",
                   "Drawing shows 4 splayed legs with ties and diagonals, no sections"),
    ReferenceValue("Anchor bolts", "4 x M30 per base plate 400x400x25",
                   "Project convention (R5 hex bolts)"),
    ReferenceValue("Ladder", "bearing 112.5 deg, stringers CHS 42.4 at r1250, rungs @300, cage hoops @1200",
                   "Drawing shows ladder at ~135 deg; moved off the 135 deg leg"),
    ReferenceValue("Landings", "U 5900 / 9200 / 12500 / 15900, r1000..1800",
                   "'Access platform (typ.)' on drawing, elevations not dimensioned"),
    ReferenceValue("Top platform", "ring r1000..1800 at U 19600, rail RAILHE 1100/550",
                   "Circular top platform with handrail on drawing, no dimensions"),
)

NOTES = (
    "Insulation / cladding shown on the drawing is not modelled (bare OD 2000).",
    "Every nozzle is catalogue-bound inline (CATR before POS/ORI); the trailing "
    "OLD/CATR rebinding pass of the native listing is regenerated to match.",
    "Handrails are structural HANDRA under STRU/FRMWORK, peer to the EQUI, as accepted in R8.",
)

OUTSTANDING = (
    "Bottom outlet: elevation label says DN150, nozzle list says DN300 - DN300 modelled, confirm.",
    "Top outlet DN 'as per line' - DN300 assumed, confirm against the 2nd stage line.",
    "Instrument connection sizes (PIS-3524, PD-3523, TI-3535, PI-3536) are Reference Values.",
    "Nozzle elevations not dimensioned on the drawing are scaled from the N.T.S. view.",
    "Bearing convention (0 deg = North, clockwise) to be confirmed against the plant north arrow.",
    "Diagonal braces are sheared prisms (PYRAMID) - the only verified form for an inclined member.",
    "Ladder safety gate at the top exit is not modelled.",
)


def build_model() -> EquipmentModel:
    primitives = build_support() + build_shell() + build_access()
    nozzles = build_nozzles()
    return EquipmentModel(
        name=NAME,
        display_name=DISPLAY_NAME,
        area="WSB",
        position=BOTTOM_CENTRE,
        overall_height=STRINGER_TOP_U,
        main_dimensions=(
            f"OD {SHELL_OD:g} x H {OVERALL_HEIGHT:g} (vessel), "
            f"{STRINGER_TOP_U:g} to ladder stringer top"
        ),
        primitives=tuple(primitives),
        body_envelope=BODY_ENVELOPE,
        capacity_m3=VOLUME_M3,
        nozzle_groups=tuple(n.group for n in nozzles),
        native_nozzles=tuple(nozzles),
        parameters=PARAMETERS,
        reference_values=REFERENCE_VALUES,
        sources=SOURCES,
        notes=NOTES,
        outstanding=OUTSTANDING,
    )


# ---------------------------------------------------------------------------
# Handrails (STRU / FRMWORK / HANDRA)
# ---------------------------------------------------------------------------


def _fmt_mm(value: float) -> str:
    r = round(value, 2)
    if abs(r - round(r)) < 1e-6:
        return f"{int(round(r))}mm"
    return f"{r:.2f}".rstrip("0").rstrip(".") + "mm"


def native_pos(e: float, n: float, u: float) -> str:
    return "POS " + " ".join((
        f"E {_fmt_mm(e)}" if e >= 0 else f"W {_fmt_mm(-e)}",
        f"N {_fmt_mm(n)}" if n >= 0 else f"S {_fmt_mm(-n)}",
        f"U {_fmt_mm(u)}" if u >= 0 else f"D {_fmt_mm(-u)}",
    ))


def _direction_of(p0: Tuple[float, float], p1: Tuple[float, float]) -> str:
    return _plan_direction(math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0])))


def _handrail_position(local_u: float) -> Point:
    """HANDRA POS relative to the STRU: tank axis at the floor top, world elevation."""
    return (BOTTOM_CENTRE[0], BOTTOM_CENTRE[1], local_u + EQUI_POSITION[2])


def _spec(name: str, floor_top_u: float, ladder_pts: Sequence[Tuple[str, Tuple[float, float]]]) -> HandrailSpec:
    """Build a HandrailSpec from (kind, ladder-frame point) pairs."""
    items: List[RoutePoint | RouteCurve] = []
    xy: List[Tuple[float, float]] = []
    for kind, (x, y) in ladder_pts:
        e, n = ladder_to_local(x, y)
        xy.append((e, n))
        if kind == "P":
            items.append(RoutePoint(position=(e, n, 0.0)))
        else:
            items.append(RouteCurve(position=(e, n, 0.0)))
    return HandrailSpec(
        name=name,
        position=_handrail_position(floor_top_u),
        top_rail_height=RAIL_TOP,
        mid_rail_height=RAIL_MID,
        start_direction=_direction_of(xy[0], xy[1]),
        end_direction=_direction_of(xy[-2], xy[-1]),
        path_items=tuple(items),
    )


def top_rail_spec() -> HandrailSpec:
    x_str = STRINGER_X
    y_str = STRINGER_Y
    x_rim = math.sqrt(RAIL_R * RAIL_R - y_str * y_str)
    theta_rim = math.degrees(math.atan2(y_str, x_rim))
    sweep = 360.0 - 2.0 * theta_rim
    segments = 4
    pts: List[Tuple[str, Tuple[float, float]]] = [
        ("P", (x_str, -y_str)),
        ("P", (x_rim, -y_str)),
    ]
    for k in range(segments):
        a0 = -theta_rim - sweep * k / segments
        a1 = -theta_rim - sweep * (k + 1) / segments
        amid = (a0 + a1) / 2.0
        px_mid, py_mid = polar(amid, RAIL_R)
        px1, py1 = polar(a1, RAIL_R)
        pts.append(("C", (px_mid, py_mid)))
        if k < segments - 1:
            pts.append(("P", (px1, py1)))
    pts += [
        ("P", (x_rim, y_str)),
        ("P", (x_str, y_str)),
    ]
    return _spec(f"{NAME}_TOP_HANDRAIL", TOP_FLOOR_U + TOP_FLOOR_THICK, pts)


def landing_rail_spec(index: int, floor_u: float, span: float) -> HandrailSpec:
    start, end = landing_sector(span)
    pts: List[Tuple[str, Tuple[float, float]]] = [
        ("P", polar(end, LANDING_RAIL_FAR_R)),
        ("P", polar(end, RAIL_R)),
        ("C", polar((start + end) / 2.0, RAIL_R)),
        ("P", polar(start, RAIL_R)),
        ("P", polar(start, LANDING_RAIL_NEAR_R)),
    ]
    return _spec(f"{NAME}_LANDING{index}_HANDRAIL", floor_u + LANDING_THICK, pts)


def handrail_specs() -> List[HandrailSpec]:
    specs = [top_rail_spec()]
    for i, (L, span) in enumerate(LANDINGS, 1):
        specs.append(landing_rail_spec(i, L, span))
    return specs


def build_structure_block() -> str:
    builder = HandrailBuilder()
    lines = [
        f"NEW STRUCTURE /{STRU_NAME}",
        native_pos(EQUI_POSITION[0], EQUI_POSITION[1], 0.0),
        "BUIL false",
        "PDNAME unset",
        "",
        f"NEW FRMWORK /{FRMWORK_NAME}",
        "BUIL false",
        "SHOP false",
        "GRADE 0",
        "FIRE 0",
        "PTSP unset",
        "INSC unset",
        "PDNAME unset",
        "",
    ]
    for spec in handrail_specs():
        lines.append(builder.build(spec).rstrip("\n"))
    lines += ["END", "END"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Emission
# ---------------------------------------------------------------------------


def build_equipment_block(model: EquipmentModel) -> str:
    """END-closed EQUI block in the EQUI frame, verified against the model."""
    validate_equipment_model(model)
    builder = PMLBuilder(model.name, close_elements=True)
    emit_equipment(
        model,
        builder,
        equi_position=EQUI_POSITION,
        equi_attributes=NATIVE_ATTRIBUTES,
        sube_attributes=NATIVE_ATTRIBUTES,
    )
    script = builder.build()
    problems = verify_equipment_macro(model, script)
    if problems:
        raise ValueError("Numerical verification failed:\n  " + "\n  ".join(problems))
    return script


def build_macro(model: EquipmentModel, equipment_block: str, structure_block: str) -> str:
    """Standalone macro: header, EQUI block, STRU block, footer."""
    header = [
        f"-- Macro: {OUTPUT_MACRO.name}",
        f"-- Purpose: /{NAME} {DISPLAY_NAME} rebuilt from {DRAWING}",
        "-- Frame: EQUI POS is owner-relative to ZONE /WSB_TA (R9 baseline form);",
        f"--        primitives are in the EQUI frame, bottom centre E {BOTTOM_CENTRE[0]:g} "
        f"S {-BOTTOM_CENTRE[1]:g} U 0.",
        "-- Load: make ZONE /WSB_TA the current element, DELETE EQUI /203_TA_024 and",
        "--       STRU /203_TA_024_STRU if they exist, then $M <this file>.",
        f"-- Generated: {date.today().isoformat()} by tools/reactor_203_ta_024_ga.py",
        "",
    ]
    footer = [
        "",
        f"-- End of macro - 1 equipment, {model.primitive_count} primitives, "
        f"{model.nozzle_count} nozzles, {len(handrail_specs())} handrails.",
    ]
    text = "\n".join(header) + equipment_block.rstrip("\n") + "\n\n" + structure_block + "\n".join(footer) + "\n"
    problems = validate_pml(text)
    if problems:
        raise ValueError("PML validation failed:\n  " + "\n  ".join(problems))
    return text


def catref_rebinding(model: EquipmentModel) -> List[str]:
    """Trailing OLD/CATR entries in the native listing's own shape."""
    lines: List[str] = []
    for nozzle in model.native_nozzles:
        lines += [
            f"OLD NOZZLE /{NAME}_{nozzle.name}_NOZZ",
            f"CATR SPCOMPONENT {nozzle_component_path(nozzle.dn)}",
            "",
        ]
    return lines


def splice_listing(baseline: str, equipment_block: str, structure_block: str, model: EquipmentModel) -> str:
    """
    Replace the old /203_TA_024 EQUI block and its trailing CATR rebinding in
    the baseline listing. Everything else is preserved byte-for-byte.
    """
    lines = baseline.split("\n")
    start = lines.index(f"NEW EQUIPMENT /{NAME}")
    end = lines.index(f"NEW EQUIPMENT /{NEXT_EQUIPMENT}")
    if not (start < end):
        raise ValueError("Baseline EQUI blocks out of order")
    new_block: List[str] = []
    for line in (equipment_block.rstrip("\n") + "\n" + structure_block).split("\n"):
        if line.startswith("--"):
            continue                      # generator commentary, not listing data
        if line == "" and (not new_block or new_block[-1] == ""):
            continue                      # native listings use single blank lines
        new_block.append(line)
    while new_block and new_block[-1] == "":
        new_block.pop()
    lines[start:end] = new_block

    old_first = lines.index(f"OLD NOZZLE /{NAME}_N1_NOZZ")
    old_last = lines.index(f"OLD NOZZLE /{NAME}_M1_NOZZ")
    if not (old_first < old_last and lines[old_last + 2] == ""):
        raise ValueError("Unexpected trailing CATR block shape")
    lines[old_first:old_last + 3] = catref_rebinding(model)
    return "\n".join(lines)


def read_baseline() -> str:
    raw = BASELINE.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("Baseline is expected to carry a UTF-8 BOM")
    return raw[3:].decode("utf-8").replace("\r\n", "\n")


def write_listing(path: Path, text: str) -> None:
    path.write_bytes(b"\xef\xbb\xbf" + text.replace("\n", "\r\n").encode("utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def group_counts(model: EquipmentModel) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for p in model.primitives:
        counts[p.group] = counts.get(p.group, 0) + 1
    return counts


def build_report(model: EquipmentModel, macro_path: Path, listing_path: Path,
                 parsed_primitives: int, parsed_nozzles: int) -> str:
    counts = group_counts(model)
    lines = [
        f"# {DISPLAY_NAME} - GA rebuild {REVISION_DATE}",
        "",
        f"Source: {DRAWING}. Baseline: `{BASELINE.name}` (R9).",
        "",
        "## Deliverables",
        "",
        f"- `{macro_path.name}` - standalone EQUI + STRU macro (SHA-256 `{sha256(macro_path)}`)",
        f"- `{listing_path.name}` - R9 listing with /{NAME} replaced (SHA-256 `{sha256(listing_path)}`)",
        "",
        "## Model summary",
        "",
        f"- Primitives: {model.primitive_count} "
        + ", ".join(f"{g} {n}" for g, n in counts.items()),
        f"- Native nozzles: {model.nozzle_count} (all catalogue-bound)",
        f"- Handrails: {len(handrail_specs())} structural HANDRA under /{STRU_NAME}",
        f"- Re-parsed from the emitted EQUI: {parsed_primitives} primitives, {parsed_nozzles} nozzles (IR-11f)",
        f"- Overall vessel height {OVERALL_HEIGHT:g}; model reaches {model.overall_height:g} (ladder stringer top)",
        "",
        "## Drawing data",
        "",
        "| Parameter | Value | Source |",
        "|---|---|---|",
    ]
    lines += [f"| {p.name} | {p.value} | {p.source} |" for p in model.parameters]
    lines += [
        "",
        "## Nozzle list (From P&ID)",
        "",
        "| Mark | Service | DN | Axis | Face (local E, N, U) | HEIG |",
        "|---|---|---|---|---|---|",
    ]
    for n in model.native_nozzles:
        e, nn, u = n.face
        lines.append(
            f"| {n.name} | {n.label.split(': ', 1)[1]} | {n.dn} | {n.axis} | "
            f"{e:.1f}, {nn:.1f}, {u:.1f} | {n.height:g} |"
        )
    lines += ["", "## Reference Values", "", "| Parameter | Value | Basis |", "|---|---|---|"]
    lines += [f"| {r.parameter} | {r.value} | {r.basis} |" for r in model.reference_values]
    lines += ["", "## Notes", ""] + [f"- {n}" for n in model.notes]
    lines += ["", "## Outstanding", ""] + [f"- {o}" for o in model.outstanding]
    lines += [
        "",
        "## Load instructions",
        "",
        "1. In E3D Design, open ZONE /WSB_TA (or the full listing file).",
        f"2. Full listing: input `{listing_path.name}` as the WSB_TA data listing (replaces the R9 file).",
        f"3. Standalone: `DELETE EQUI /{NAME}` and `DELETE STRU /{STRU_NAME}` if present, make ZONE /WSB_TA the CE, then `$M {macro_path.name}`.",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def generate(write: bool = True) -> Tuple[EquipmentModel, str, str]:
    model = build_model()
    equipment_block = build_equipment_block(model)
    structure_block = build_structure_block()
    macro = build_macro(model, equipment_block, structure_block)
    listing = splice_listing(read_baseline(), equipment_block, structure_block, model)

    parsed_primitives = len(parse_primitives(macro, NAME))
    parsed_nozzles = len(parse_nozzles(macro, NAME))
    if parsed_primitives != model.primitive_count or parsed_nozzles != model.nozzle_count:
        raise ValueError(
            f"Re-parse mismatch: {parsed_primitives}/{model.primitive_count} primitives, "
            f"{parsed_nozzles}/{model.nozzle_count} nozzles"
        )

    if write:
        OUTPUT_MACRO.write_text(macro, encoding="utf-8", newline="\n")
        write_listing(OUTPUT_LISTING, listing)
        OUTPUT_REPORT.write_text(
            build_report(model, OUTPUT_MACRO, OUTPUT_LISTING, parsed_primitives, parsed_nozzles),
            encoding="utf-8", newline="\n",
        )
    return model, macro, listing


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="build and verify without writing")
    args = parser.parse_args(argv)
    model, macro, listing = generate(write=not args.check)
    counts = group_counts(model)
    print(f"{DISPLAY_NAME}: {model.primitive_count} primitives "
          + ", ".join(f"{g} {n}" for g, n in counts.items())
          + f"; {model.nozzle_count} nozzles; {len(handrail_specs())} handrails")
    print(f"macro {len(macro.splitlines())} lines; listing {len(listing.splitlines())} lines")
    if not args.check:
        for path in (OUTPUT_MACRO, OUTPUT_LISTING, OUTPUT_REPORT):
            print(f"wrote {path.relative_to(BASE)}  sha256 {sha256(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
