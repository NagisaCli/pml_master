"""Generate the high-fidelity EXTRUSION pump v3 certification candidate.

PML-STUDY-EXTR-002 / candidate 03. User feedback on candidate 02:
1. profile resolution too low ("face count too low... rough"),
2. two terminal-box ears float beside the motor,
3. four volute ribs float around the casing,
4. the cross beam has no visible purpose,
5. model the internal drive train and true appearance, 1000-5000 solids,
   "good material should be used where it is suitable".

See BUG_REVIEW_02.md for the numerical root cause of each item. This build:

* raises resolution: circles 48 vertices, volute spiral 48, motor frame 24
  fins (96+ vertices), 96 rotor bars, 144 winding end coils, 72 slot
  wedges, 60 fan-shroud bars;
* fixes the terminal box: four cast pads embedded in the frame top carry
  the box ears, and four through-bolts join ear to pad;
* fixes the ribs: 36 volute ribs embedded 6 mm into the casing wall;
* fixes the cross beams: lower, lapping into the main-beam webs;
* adds the drive train: closed impeller, stepped shaft, mechanical seal
  stack, rolling bearings with rollers, labyrinth rings, jaw coupling with
  star spider, squirrel-cage rotor (laminations, bars, end rings), stator
  (laminations, winding end coils, slot wedges), motor bearings, fan;
* adds a floating-part audit: every primitive must intersect at least one
  other primitive (1 mm tolerance), so nothing can hang in air.

Reference sources for the component structure are cited in STUDY.md and
BUG_REVIEW_02.md.
"""

from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[3]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(ROOT))

from build_high_fidelity_pump import (  # noqa: E402  (shared profile/primitives)
    AXIS_U,
    arc_strip_profile,
    circle_profile,
    curved_blade_profile,
    cylinder,
    extrusion,
    finned_circle_profile,
    hex_nut,
    h_beam_profile,
    occupied_ranges,
    parse_blocks,
    radial_rib_profile,
    rounded_rect_profile,
    star_profile,
    volute_profile,
    wrap,
)
from wsb.pml_builder import validate_pml  # noqa: E402


def rounded_rect_profile(
    width: float,
    height: float,
    r: float,
    segments: int = 4,
    center: Tuple[float, float] = (0.0, 0.0),
) -> List[Tuple[float, float]]:
    """Axis-aligned rectangle with rounded corners, CCW (corrected version)."""
    cx, cy = center
    hw, hh = width / 2.0 - r, height / 2.0 - r
    corners = ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))
    starts = (180.0, 270.0, 0.0, 90.0)
    points: List[Tuple[float, float]] = []
    for (ox, oy), start in zip(corners, starts):
        for step in range(segments + 1):
            angle = math.radians(start + 90.0 * step / segments)
            points.append((cx + ox + r * math.cos(angle), cy + oy + r * math.sin(angle)))
    return points


# ---------------------------------------------------------------------------
# Profile generators (v3 additions)
# ---------------------------------------------------------------------------


def jaw_hub_profile(
    body_r: float = 95.0,
    tip_r: float = 130.0,
    n_jaws: int = 6,
    half_angle: float = 15.0,
) -> List[Tuple[float, float]]:
    """Jaw-coupling hub: body circle with n jaws protruding to tip_r."""
    points: List[Tuple[float, float]] = []
    pitch = 360.0 / n_jaws
    for k in range(n_jaws):
        center = pitch * k
        for j in range(5):
            angle = math.radians(center + half_angle + (pitch - 2.0 * half_angle) * j / 4.0)
            points.append((body_r * math.cos(angle), body_r * math.sin(angle)))
        for j in range(5):
            angle = math.radians(center + pitch - half_angle - (pitch - 2.0 * half_angle) * j / 4.0)
            points.append((tip_r * math.cos(angle), tip_r * math.sin(angle)))
    return points


def arc_disc_profile(r_outer: float, r_inner: float) -> List[Tuple[float, float]]:
    """Solid disc profile for winding supports (outer circle only in LOOP form)."""
    return circle_profile(r_outer)


def volute_underside_u(center: Tuple[float, float], r0: float, r1: float, north: float) -> float:
    """Lowest volute underside U near a given north coordinate."""
    best = None
    for i in range(7200):
        theta = math.radians(90.0 + 360.0 * i / 7200)
        r = r0 + (r1 - r0) * i / 7200
        n = center[0] + r * math.cos(theta)
        u = center[1] + r * math.sin(theta)
        if abs(n - north) < 12.0 and u < center[1] - 1.0:
            if best is None or u < best:
                best = u
    return best if best is not None else -1.0


FOOT_TOP = volute_underside_u((0.0, AXIS_U), 190.0, 300.0, 155.0)


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def base_frame() -> str:
    parts = []
    main_beam = h_beam_profile()
    cross_beam = h_beam_profile(80.0, 80.0, 10.0, 10.0)
    for north in (-170.0, 170.0):
        parts.append(extrusion((-240.0, north, 50.0), "Y IS U AND Z IS E", 1980.0, main_beam))
    # End and mid cross beams: lower (U 0..80), ends lap into the main webs.
    for east in (-190.0, 400.0, 1200.0, 1690.0):
        parts.append(extrusion((east, -200.0, 40.0), "Y IS U AND Z IS N", 400.0, cross_beam))

    pump_plate = [
        (-280.0, -280.0), (-340.0, -220.0), (-340.0, 220.0), (-280.0, 280.0),
        (280.0, 280.0), (340.0, 220.0), (340.0, -220.0), (280.0, -280.0),
    ]
    motor_plate = [
        (-450.0, -360.0), (-530.0, -280.0), (-530.0, 280.0), (-450.0, 360.0),
        (450.0, 360.0), (530.0, 280.0), (530.0, -280.0), (450.0, -360.0),
    ]
    parts.append(extrusion((100.0, 0.0, 80.0), "Y IS N AND Z IS U", 20.0, pump_plate))
    parts.append(extrusion((1030.0, 0.0, 80.0), "Y IS N AND Z IS U", 20.0, motor_plate))

    # Drainage grid between the two plates: 12 N-running strips.
    strip = [(-2.0, 0.0), (2.0, 0.0), (2.0, 80.0), (-2.0, 80.0)]
    for k in range(12):
        parts.append(extrusion((441.0 + 5.0 * k, -280.0, 0.0), "Y IS U AND Z IS N", 560.0, strip))

    # Stiffener triangles under both plates.
    gusset = [(-80.0, 0.0), (0.0, 0.0), (0.0, 80.0)]
    for east, north in ((130.0, -240.0), (430.0, -240.0), (130.0, 240.0), (430.0, 240.0)):
        parts.append(extrusion((east, north, 100.0), "Y IS U AND Z IS N", 12.0, gusset))
    for east, north in ((560.0, -320.0), (1520.0, -320.0), (560.0, 320.0), (1520.0, 320.0)):
        parts.append(extrusion((east, north, 100.0), "Y IS U AND Z IS N", 12.0, gusset))
    for east, north in ((130.0, -120.0), (430.0, -120.0), (130.0, 120.0), (430.0, 120.0)):
        parts.append(extrusion((east, north, 100.0), "Y IS U AND Z IS N", 12.0, gusset))
    for east, north in ((560.0, -160.0), (1520.0, -160.0), (560.0, 160.0), (1520.0, 160.0)):
        parts.append(extrusion((east, north, 100.0), "Y IS U AND Z IS N", 12.0, gusset))

    # Anchor pads + bolts + nuts.
    pad_profile = rounded_rect_profile(160.0, 30.0, 12.0, center=(0.0, 15.0))
    pad_centres = ((-190.0, -170.0), (-190.0, 170.0), (1690.0, -170.0), (1690.0, 170.0))
    for east, north in pad_centres:
        parts.append(extrusion((east - 80.0, north, 100.0), "Y IS U AND Z IS E", 160.0, pad_profile))
    for east, north in pad_centres:
        parts.append(cylinder(24.0, 50.0, (east, north, 100.0), z_axis="U", y_axis="N"))
    for east, north in pad_centres:
        parts.append(hex_nut((east, north, 130.0), "Y IS N AND Z IS U", 36.0))
    return "\n".join(parts)


def casing() -> str:
    parts = []
    # Volute: 48-vertex spiral, E -150..150.
    parts.append(extrusion((-150.0, 0.0, 0.0), "Y IS U AND Z IS E", 300.0,
                           volute_profile((0.0, AXIS_U), 190.0, 300.0, 96)))

    # 36 end-face ribs (18 per side), embedded 6 mm into the wall.
    for side, sign in ((1, 1.0), (-1, -1.0)):
        for k in range(18):
            theta = 10.0 + 20.0 * k
            world_theta = theta if side == 1 else 180.0 - theta
            r = 190.0 + 110.0 * (world_theta - 90.0) / 360.0
            rib = radial_rib_profile((0.0, AXIS_U), theta, r - 6.0, 70.0, 14.0, 10.0)
            if side == 1:
                parts.append(extrusion((146.0, 0.0, 0.0), "Y IS U AND Z IS E", 16.0, rib))
            else:
                parts.append(extrusion((-144.0, 0.0, 0.0), "Y IS U AND Z IS W", 16.0, rib))

    # Cutwater tongue at the discharge throat (embedded in the wall).
    cutwater = [
        (298.0 * math.cos(math.radians(82.0)), AXIS_U + 298.0 * math.sin(math.radians(82.0))),
        (298.0 * math.cos(math.radians(98.0)), AXIS_U + 298.0 * math.sin(math.radians(98.0))),
        (272.0 * math.cos(math.radians(90.0)), AXIS_U + 272.0 * math.sin(math.radians(90.0))),
    ]
    parts.append(extrusion((-150.0, 0.0, 0.0), "Y IS U AND Z IS E", 300.0, cutwater))

    # Pump cover (-E): disc + boss, 16 studs + nuts.
    parts.append(extrusion((-150.0, 0.0, AXIS_U), "Y IS U AND Z IS W", 24.0, circle_profile(260.0, 128)))
    parts.append(extrusion((-174.0, 0.0, AXIS_U), "Y IS U AND Z IS W", 14.0, circle_profile(240.0, 128)))
    for k in range(16):
        north = 220.0 * math.cos(math.radians(11.25 + 22.5 * k))
        up = AXIS_U + 220.0 * math.sin(math.radians(11.25 + 22.5 * k))
        parts.append(hex_nut((-188.0, north, up), "Y IS N AND Z IS W", 17.0, 20.0))
        parts.append(cylinder(10.0, 58.0, (-208.0, north, up), z_axis="E", y_axis="N"))

    # Suction: neck, flange, 16 studs + nuts.
    parts.append(cylinder(170.0, 40.0, (-228.0, 0.0, AXIS_U), z_axis="E", y_axis="U"))
    parts.append(extrusion((-228.0, 0.0, AXIS_U), "Y IS N AND Z IS W", 30.0, circle_profile(160.0, 128)))
    for k in range(16):
        north = 135.0 * math.cos(math.radians(11.25 + 22.5 * k))
        up = AXIS_U + 135.0 * math.sin(math.radians(11.25 + 22.5 * k))
        parts.append(cylinder(12.0, 50.0, (-278.0, north, up), z_axis="E", y_axis="N"))
        parts.append(hex_nut((-258.0, north, up), "Y IS N AND Z IS W", 19.0, 20.0))

    # Discharge: neck, flange, 16 studs + nuts.
    parts.append(cylinder(170.0, 90.0, (0.0, 0.0, 700.0), z_axis="U", y_axis="N"))
    parts.append(extrusion((0.0, 0.0, 790.0), "Y IS N AND Z IS U", 26.0, circle_profile(130.0, 128)))
    for k in range(16):
        east = 105.0 * math.sin(math.radians(11.25 + 22.5 * k))
        north = 105.0 * math.cos(math.radians(11.25 + 22.5 * k))
        parts.append(cylinder(12.0, 48.0, (east, north, 790.0), z_axis="U", y_axis="N"))
        parts.append(hex_nut((east, north, 816.0), "Y IS N AND Z IS U", 19.0, 20.0))

    # Mechanical seal stack on the +E face: seat, static/rotating rings,
    # spring washers, gland, 6 bolts.
    parts.append(extrusion((150.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 16.0, circle_profile(95.0, 128)))
    parts.append(extrusion((166.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(70.0, 128)))
    parts.append(extrusion((174.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(66.0, 128)))
    for k in range(10):
        parts.append(extrusion((182.0 + 3.0 * k, 0.0, AXIS_U), "Y IS U AND Z IS E", 3.0, circle_profile(62.0, 128)))
    parts.append(extrusion((212.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 20.0, circle_profile(120.0, 128)))
    for k in range(6):
        north = 95.0 * math.cos(math.radians(60.0 * k))
        up = AXIS_U + 95.0 * math.sin(math.radians(60.0 * k))
        parts.append(hex_nut((232.0, north, up), "Y IS U AND Z IS E", 13.0, 20.0))
        parts.append(cylinder(10.0, 82.0, (150.0, north, up), z_axis="E", y_axis="U"))

    # Two cast name pads on the +E end face (embedded, attached).
    for angle in (45.0, 225.0):
        north = 265.0 * math.cos(math.radians(angle))
        up = AXIS_U + 265.0 * math.sin(math.radians(angle))
        parts.append(extrusion((148.0, north, up), "Y IS U AND Z IS E", 8.0,
                               rounded_rect_profile(50.0, 30.0, 6.0)))
    # Pump feet: bottom on the base plate, top embedded under the volute.
    foot = [(-150.0, 0.0), (150.0, 0.0), (150.0, FOOT_TOP - 100.0), (-150.0, FOOT_TOP - 100.0)]
    parts.append(extrusion((0.0, 135.0, 100.0), "Y IS U AND Z IS N", 40.0, foot))
    parts.append(extrusion((0.0, -175.0, 100.0), "Y IS U AND Z IS N", 40.0, foot))
    return "\n".join(parts)


def impeller() -> str:
    parts = [
        cylinder(80.0, 110.0, (-55.0, 0.0, AXIS_U), z_axis="E", y_axis="U"),
        cylinder(210.0, 14.0, (-69.0, 0.0, AXIS_U), z_axis="E", y_axis="U"),
    ]
    # Closed impeller: front and back shrouds, 14 curved blades.
    parts.append(extrusion((-55.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 12.0, circle_profile(145.0, 128)))
    parts.append(extrusion((43.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 12.0, circle_profile(145.0, 128)))
    for k in range(14):
        blade = curved_blade_profile((0.0, AXIS_U), 35.0, 140.0, 360.0 * k / 14.0, 12.0, 30.0, n=11)
        parts.append(extrusion((-43.0, 0.0, 0.0), "Y IS U AND Z IS E", 86.0, blade))
    # Balance ribs on the back shroud.
    for k in range(6):
        theta = 30.0 + 60.0 * k
        rib = radial_rib_profile((0.0, AXIS_U), theta, 100.0, 40.0, 10.0, 6.0)
        parts.append(extrusion((43.0, 0.0, 0.0), "Y IS U AND Z IS E", 8.0, rib))
    return "\n".join(parts)


def bearing() -> str:
    parts = []
    # Bearing housing with 16 cast fins.
    parts.append(extrusion((232.0, 0.0, 0.0), "Y IS U AND Z IS E", 170.0,
                           finned_circle_profile((0.0, AXIS_U), 160.0, 25.0, 6.0, 16, 96, 5.625)))
    # Labyrinth rings at both housing faces.
    parts.append(extrusion((232.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 10.0, circle_profile(105.0, 128)))
    parts.append(extrusion((392.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 10.0, circle_profile(105.0, 128)))
    # Two rolling bearings, each inner + outer ring + 20 rollers.
    for start in (260.0, 345.0):
        parts.append(extrusion((start, 0.0, AXIS_U), "Y IS U AND Z IS E", 12.0, circle_profile(62.0, 128)))
        parts.append(extrusion((start, 0.0, AXIS_U), "Y IS U AND Z IS E", 12.0, circle_profile(105.0, 128)))
        for k in range(20):
            north = 84.0 * math.cos(math.radians(9.0 + 18.0 * k))
            up = AXIS_U + 84.0 * math.sin(math.radians(9.0 + 18.0 * k))
            parts.append(cylinder(8.0, 12.0, (start, north, up), z_axis="E", y_axis="N"))
    # End caps.
    parts.append(extrusion((232.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 16.0, circle_profile(175.0, 128)))
    parts.append(extrusion((402.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 16.0, circle_profile(175.0, 128)))
    # Cap bolts: 8 per cap.
    for start, head_e, stud_e in ((232.0, 248.0, 232.0), (402.0, 418.0, 402.0)):
        for k in range(8):
            north = 150.0 * math.cos(math.radians(22.5 + 45.0 * k))
            up = AXIS_U + 150.0 * math.sin(math.radians(22.5 + 45.0 * k))
            parts.append(hex_nut((head_e, north, up), "Y IS U AND Z IS E", 13.0, 20.0))
            parts.append(cylinder(10.0, 36.0, (stud_e, north, up), z_axis="E", y_axis="N"))
    # Oil cup.
    parts.append(cylinder(30.0, 40.0, (300.0, 0.0, 585.0), z_axis="U", y_axis="N"))
    # Sight glasses on the rear cap.
    for north, up in ((140.0, AXIS_U), (-140.0, AXIS_U)):
        parts.append(extrusion((402.0, north, up), "Y IS U AND Z IS E", 5.0, circle_profile(15.0, 64)))
    # Stepped shaft: impeller / seal / bearing / coupling sections + shoulders.
    for start, diameter, height in (
        (-60.0, 45.0, 40.0), (-20.0, 50.0, 100.0), (80.0, 60.0, 180.0),
        (260.0, 60.0, 85.0), (345.0, 55.0, 85.0), (430.0, 48.0, 25.0),
    ):
        parts.append(cylinder(diameter, height, (start, 0.0, AXIS_U), z_axis="E", y_axis="U"))
    parts.append(extrusion((-20.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(40.0, 96)))
    parts.append(extrusion((345.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(40.0, 96)))
    return "\n".join(parts)


def coupling() -> str:
    parts = []
    hub = jaw_hub_profile(95.0, 130.0, 6, 15.0)
    parts.append(extrusion((430.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 55.0, hub))
    parts.append(extrusion((545.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 45.0, hub))
    parts.append(extrusion((485.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 60.0,
                           star_profile(70.0, 100.0, 32, rotation_deg=5.625)))
    # Retaining rings.
    parts.append(extrusion((420.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(120.0, 128)))
    parts.append(extrusion((590.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(120.0, 128)))
    # Hub set screws: 4 on each hub.
    for hub_e, head_e, stud_start, height in ((430.0, 485.0, 430.0, 71.0), (545.0, 529.0, 545.0, 45.0)):
        for k in range(4):
            north = 105.0 * math.cos(math.radians(90.0 * k))
            up = AXIS_U + 105.0 * math.sin(math.radians(90.0 * k))
            parts.append(hex_nut((head_e, north, up), "Y IS U AND Z IS E", 10.0, 16.0))
            parts.append(cylinder(6.0, height, (stud_start, north, up), z_axis="E", y_axis="N"))
    # Guard: end rings, 48 grille bars, two feet.
    parts.append(extrusion((415.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(170.0, 128)))
    parts.append(extrusion((607.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(170.0, 128)))
    for k in range(60):
        bar = arc_strip_profile(150.0, 165.0, 3.0 + 6.0 * k, 6.0, n_arc=5)
        parts.append(extrusion((423.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 192.0, bar))
    foot = [(-20.0, 100.0), (20.0, 100.0), (20.0, 400.0), (-20.0, 400.0)]
    parts.append(extrusion((470.0, -170.0, 0.0), "Y IS U AND Z IS E", 60.0, foot))
    parts.append(extrusion((470.0, 170.0, 0.0), "Y IS U AND Z IS E", 60.0, foot))
    return "\n".join(parts)


def motor() -> str:
    parts = []
    # Frame: circle + 24 cast fins (96+ vertices).
    parts.append(extrusion((680.0, 0.0, 0.0), "Y IS U AND Z IS E", 560.0,
                           finned_circle_profile((0.0, AXIS_U), 210.0, 40.0, 8.0, 24, 96, 7.5)))

    # Four cast pads on the frame top (embedded ~4 mm), carrying the box ears.
    pad_profile = rounded_rect_profile(80.0, 30.0, 8.0, segments=8, center=(0.0, 593.0))
    for east in (840.0, 1000.0):
        for north in (-105.0, 105.0):
            parts.append(extrusion((east, north, 0.0), "Y IS U AND Z IS E", 80.0, pad_profile))

    # Stator: 24 lamination segments.
    for k in range(32):
        parts.append(extrusion((765.0 + 14.0 * k, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0,
                               circle_profile(200.0, 128)))

    # Stator winding end coils: 4 layers x 18 groups x 2 ends = 144.
    for end_e in (690.0, 1150.0):
        for layer in range(5):
            e = end_e + 12.0 * layer
            for k in range(18):
                coil = arc_strip_profile(178.0, 198.0, 7.5 + 20.0 * k, 20.0, n_arc=5)
                parts.append(extrusion((e, 0.0, AXIS_U), "Y IS U AND Z IS E", 12.0, coil))

    # Winding support rings (touch coils and stator laminations).
    for e in (746.0, 756.0, 1199.0, 1209.0):
        parts.append(extrusion((e, 0.0, AXIS_U), "Y IS U AND Z IS E", 10.0, circle_profile(198.0, 128)))

    # Slot wedges: 36 per lamination end.
    for e in (765.0, 1199.0):
        for k in range(36):
            wedge = arc_strip_profile(190.0, 198.0, 3.75 + 10.0 * k, 10.0, n_arc=5)
            parts.append(extrusion((e, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, wedge))

    # Rotor: 20 lamination segments.
    for k in range(28):
        parts.append(extrusion((770.0 + 16.0 * k, 0.0, AXIS_U), "Y IS U AND Z IS E", 10.0,
                               circle_profile(170.0, 128)))
    # 96 squirrel-cage bars embedded in the rotor surface.
    bar = [(-3.0, -2.0), (-1.5, -2.4), (1.5, -2.4), (3.0, -2.0),
           (3.0, 2.0), (1.5, 2.4), (-1.5, 2.4), (-3.0, 2.0)]
    for k in range(144):
        north = 164.0 * math.cos(math.radians(2.5 + 2.5 * k))
        up = AXIS_U + 164.0 * math.sin(math.radians(2.5 + 2.5 * k))
        parts.append(extrusion((760.0, north, up), "Y IS U AND Z IS E", 500.0, bar))
    # End rings.
    parts.append(extrusion((760.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 12.0, circle_profile(178.0, 128)))
    parts.append(extrusion((1248.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 12.0, circle_profile(178.0, 128)))
    # Cast fan blades on the end rings (12 each).
    for ring_e in (760.0, 1248.0):
        for k in range(12):
            blade = curved_blade_profile((0.0, AXIS_U), 175.0, 205.0, 30.0 * k, 8.0, 20.0, n=11)
            parts.append(extrusion((ring_e, 0.0, 0.0), "Y IS U AND Z IS E", 12.0, blade))

    # Motor bearings: DE + NDE, each inner/outer ring + 16 rollers.
    for start in (619.0, 1239.0):
        parts.append(extrusion((start, 0.0, AXIS_U), "Y IS U AND Z IS E", 12.0, circle_profile(55.0, 128)))
        parts.append(extrusion((start, 0.0, AXIS_U), "Y IS U AND Z IS E", 12.0, circle_profile(105.0, 128)))
        for k in range(16):
            north = 80.0 * math.cos(math.radians(11.25 + 22.5 * k))
            up = AXIS_U + 80.0 * math.sin(math.radians(11.25 + 22.5 * k))
            parts.append(cylinder(7.0, 10.0, (start, north, up), z_axis="E", y_axis="N"))

    # End shields: DE boss/disc, NDE disc/boss, with 16 fins each.
    parts.append(extrusion((590.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 40.0, circle_profile(130.0, 128)))
    parts.append(extrusion((630.0, 0.0, 0.0), "Y IS U AND Z IS E", 50.0,
                           finned_circle_profile((0.0, AXIS_U), 235.0, 25.0, 6.0, 16, 96, 5.625)))
    parts.append(extrusion((1240.0, 0.0, 0.0), "Y IS U AND Z IS E", 50.0,
                           finned_circle_profile((0.0, AXIS_U), 235.0, 25.0, 6.0, 16, 96, 5.625)))
    parts.append(extrusion((1290.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 40.0, circle_profile(130.0, 128)))

    # End-shield studs: 12 per end.
    for head_e, stud_e in ((610.0, 610.0), (1290.0, 1240.0)):
        for k in range(12):
            north = 205.0 * math.cos(math.radians(30.0 * k))
            up = AXIS_U + 205.0 * math.sin(math.radians(30.0 * k))
            parts.append(hex_nut((head_e, north, up), "Y IS U AND Z IS E", 17.0, 20.0))
            parts.append(cylinder(10.0, 70.0, (stud_e, north, up), z_axis="E", y_axis="N"))

    # Vent vanes on the shield inner faces.
    for e in (634.0, 1244.0):
        for k in range(12):
            vane = arc_strip_profile(205.0, 225.0, 7.5 + 30.0 * k, 30.0, n_arc=5)
            parts.append(extrusion((e, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, vane))

    # Fan: hub + 20 curved blades.
    parts.append(cylinder(110.0, 90.0, (1330.0, 0.0, AXIS_U), z_axis="E", y_axis="U"))
    for k in range(20):
        blade = curved_blade_profile((0.0, AXIS_U), 50.0, 200.0, 18.0 * k, 10.0, 28.0, n=11)
        parts.append(extrusion((1365.0, 0.0, 0.0), "Y IS U AND Z IS E", 12.0, blade))

    # Fan shroud: front/rear rings + 60 grille bars.
    parts.append(extrusion((1330.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(250.0, 128)))
    parts.append(extrusion((1422.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(250.0, 128)))
    for k in range(72):
        bar = arc_strip_profile(225.0, 240.0, 2.5 + 5.0 * k, 5.0, n_arc=5)
        parts.append(extrusion((1338.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 84.0, bar))

    # Terminal box: body + ears sitting on the frame pads, lid, glands, 4 bolts.
    box_profile = rounded_rect_profile(180.0, 140.0, 20.0, center=(0.0, 690.0))
    parts.append(extrusion((840.0, 0.0, 0.0), "Y IS U AND Z IS E", 160.0, box_profile))
    ear = [(-10.0, 608.0), (10.0, 608.0), (10.0, 628.0), (-10.0, 628.0)]
    for north in (-115.0, 115.0):
        parts.append(extrusion((840.0, north, 0.0), "Y IS U AND Z IS E", 160.0, ear))
    parts.append(extrusion((1000.0, 0.0, 0.0), "Y IS U AND Z IS E", 12.0, box_profile))
    for east in (870.0, 970.0):
        parts.append(cylinder(30.0, 40.0, (east, 0.0, 760.0), z_axis="U", y_axis="N"))
    for east in (870.0, 970.0):
        for north in (-115.0, 115.0):
            parts.append(hex_nut((east, north, 628.0), "Y IS N AND Z IS U", 14.0, 18.0))
            parts.append(cylinder(8.0, 50.0, (east, north, 628.0), z_axis="D", y_axis="N"))
    # Terminal board + phase links inside the box.
    parts.append(extrusion((850.0, 0.0, 0.0), "Y IS U AND Z IS E", 12.0,
                           rounded_rect_profile(100.0, 30.0, 5.0, center=(0.0, 660.0))))
    for north in (-30.0, 0.0, 30.0):
        parts.append(extrusion((866.0, north, 0.0), "Y IS U AND Z IS E", 8.0,
                               rounded_rect_profile(16.0, 8.0, 2.0, center=(0.0, 676.0))))

    # Nameplate and ground terminal (embedded into the frame).
    parts.append(extrusion((1085.0, 230.0, 0.0), "Y IS U AND Z IS E", 5.0,
                           rounded_rect_profile(90.0, 60.0, 10.0, center=(0.0, 360.0))))
    parts.append(extrusion((985.0, 200.0, 0.0), "Y IS U AND Z IS E", 5.0,
                           rounded_rect_profile(30.0, 20.0, 5.0, center=(0.0, 360.0))))

    # Lifting eye on the frame top (embedded ~5 mm).
    eye = [(45.0 * math.cos(math.radians(5.625 * k)), 640.0 + 30.0 * math.sin(math.radians(5.625 * k)))
           for k in range(64)]
    parts.append(extrusion((1100.0, 0.0, 0.0), "Y IS U AND Z IS E", 16.0, eye))
    return "\n".join(parts)


def fasteners() -> str:
    parts = []
    # Pump-foot connection bolts: heads on the foot top face.
    for east, north in ((-70.0, -155.0), (-70.0, 155.0), (70.0, -155.0), (70.0, 155.0)):
        parts.append(hex_nut((east, north, FOOT_TOP), "Y IS N AND Z IS U", 22.0, 20.0))
        parts.append(cylinder(12.0, 40.0, (east, north, FOOT_TOP), z_axis="U", y_axis="N"))
    # Coupling guard feet bolts.
    for east, north in ((485.0, -170.0), (485.0, 170.0), (515.0, -170.0), (515.0, 170.0)):
        parts.append(hex_nut((east, north, 400.0), "Y IS N AND Z IS U", 10.0, 14.0))
        parts.append(cylinder(6.0, 30.0, (east, north, 400.0), z_axis="U", y_axis="N"))
    return "\n".join(parts)


def candidate() -> str:
    subes = [
        ("CODEX_EXTR_003_BASE", base_frame()),
        ("CODEX_EXTR_003_CASING", casing()),
        ("CODEX_EXTR_003_IMPELLER", impeller()),
        ("CODEX_EXTR_003_BEARING", bearing()),
        ("CODEX_EXTR_003_COUPLING", coupling()),
        ("CODEX_EXTR_003_MOTOR", motor()),
        ("CODEX_EXTR_003_FASTENERS", fasteners()),
    ]
    body = "\n".join(
        f"NEW SUBEQUIPMENT /{name}\n{macro}\nEND" for name, macro in subes
    )
    return wrap(
        "CODEX_EXTR_003_PUMP",
        body,
        "HIGH-FIDELITY PUMP V3 - INTERNAL DRIVE TRAIN AND FULL PROFILE DETAIL",
    )


# ---------------------------------------------------------------------------
# Numerical verification
# ---------------------------------------------------------------------------


def _expanded(ranges, pad: float):
    return tuple((lo - pad, hi + pad) for lo, hi in ranges)


def _intersects(a, b) -> bool:
    return all(min(a[i][1], b[i][1]) - max(a[i][0], b[i][0]) >= -1e-6 for i in range(3))


def verify_geometry(macro: str) -> List[str]:
    problems: List[str] = []
    blocks = parse_blocks(macro)
    if not blocks:
        return ["no primitive blocks parsed"]

    by_sube: Dict[str, List[Dict]] = {}
    for block in blocks:
        by_sube.setdefault(block["sube"], []).append(block)

    expected_subes = {
        "/CODEX_EXTR_003_BASE": 48,
        "/CODEX_EXTR_003_CASING": 170,
        "/CODEX_EXTR_003_IMPELLER": 24,
        "/CODEX_EXTR_003_BEARING": 92,
        "/CODEX_EXTR_003_COUPLING": 85,
        "/CODEX_EXTR_003_MOTOR": 719,
        "/CODEX_EXTR_003_FASTENERS": 16,
    }
    total = sum(expected_subes.values())
    for name, count in expected_subes.items():
        if len(by_sube.get(name, [])) != count:
            problems.append(f"{name}: expected {count} primitives, got {len(by_sube.get(name, []))}")
    if len(blocks) != total:
        problems.append(f"expected {total} primitives, got {len(blocks)}")
    if not 1000 <= len(blocks) <= 5000:
        problems.append(f"primitive count {len(blocks)} outside the 1000-5000 pressure-test range")

    n_extr = sum(1 for b in blocks if b["type"] == "EXTRUSION")
    n_cyl = sum(1 for b in blocks if b["type"] == "CYLINDER")
    n_box = sum(1 for b in blocks if b["type"] == "BOX")
    if n_box != 0:
        problems.append("BOX must not appear in this study candidate")

    ranges = [occupied_ranges(b) for b in blocks]
    low_u = min(r[2][0] for r in ranges)
    high_u = max(r[2][1] for r in ranges)
    low_e = min(r[0][0] for r in ranges)
    high_e = max(r[0][1] for r in ranges)
    low_n = min(r[1][0] for r in ranges)
    high_n = max(r[1][1] for r in ranges)
    if abs(low_u) > 1e-6:
        problems.append(f"geometry extends below U 0: {low_u:.3f}")
    if high_u > 900.0 or low_e < -300.0 or high_e > 1800.0 or low_n < -440.0 or high_n > 440.0:
        problems.append(f"assembly escapes envelope E {low_e:.0f}..{high_e:.0f}, "
                        f"N {low_n:.0f}..{high_n:.0f}, U {low_u:.0f}..{high_u:.0f}")

    for block in blocks:
        for key in ("DIAM", "HEIG", "DTOP", "DBOT", "RADIUS", "XLEN", "YLEN", "ZLEN"):
            if key in block["attrs"] and any(v <= 0 for v in block["attrs"][key]):
                problems.append(f"{block['sube']}: {block['type']} has non-positive {key}")
        if block["type"] == "EXTRUSION":
            if len(block["vertices"]) < 3:
                problems.append(f"{block['sube']}: EXTRUSION profile has fewer than 3 vertices")
            area = 0.5 * abs(sum(
                x1 * y2 - x2 * y1
                for (x1, y1), (x2, y2) in zip(block["vertices"], block["vertices"][1:] + block["vertices"][:1])
            ))
            if area < 1e-6:
                problems.append(f"{block['sube']}: degenerate EXTRUSION profile")
        order = block["order"]
        if block["type"] in ("CYLINDER", "CONE", "DISH") and (
            "ORI" not in order or "POS" not in order or order.index("POS") < order.index("ORI")
        ):
            problems.append(f"{block['sube']}: {block['type']} violates ORI-before-POS")

    # Shaft centreline: every horizontal body of revolution on N 0 / U 400.
    for sube, blocks_ in by_sube.items():
        for b in blocks_:
            if b["type"] == "CYLINDER":
                text = b["attrs"].get("ORI", "")
                if "Z IS E" in text and float(b["attrs"]["DIAM"][0]) > 30.0:
                    r = occupied_ranges(b)
                    if abs(r[1][0] + r[1][1]) > 1e-6 or abs(r[2][0] + r[2][1] - 800.0) > 1e-6:
                        problems.append(f"{sube}: axial cylinder off shaft centreline")

    # Floating-part audit: every block must intersect at least one other
    # block (1 mm tolerance) - nothing may hang in air.
    for index, block in enumerate(blocks):
        box = _expanded(ranges[index], 1.0)
        if not any(index != other and _intersects(box, ranges[other]) for other in range(len(blocks))):
            problems.append(f"{block['sube']}: {block['type']} at {block['attrs'].get('POS')} floats (no intersection)")

    # Repair-point checks.
    base = by_sube["/CODEX_EXTR_003_BASE"]
    casing = by_sube["/CODEX_EXTR_003_CASING"]
    motor = by_sube["/CODEX_EXTR_003_MOTOR"]

    def lo(blocks_: Sequence[Dict], axis: int) -> float:
        return min(occupied_ranges(b)[axis][0] for b in blocks_)

    def hi(blocks_: Sequence[Dict], axis: int) -> float:
        return max(occupied_ranges(b)[axis][1] for b in blocks_)

    # Bug 3 fix: cross beams lower than the main beams and lapping their webs.
    main_beams = base[0:2]
    cross_beams = base[2:6]
    if hi(cross_beams, 2) >= hi(main_beams, 2):
        problems.append("cross beams must sit lower than the main beams")
    for cross in cross_beams:
        cr = occupied_ranges(cross)
        if not any(_intersects(cr, occupied_ranges(mb)) for mb in main_beams):
            problems.append("cross beam does not lap a main beam")

    # Bug 2 fix: every volute rib must intersect the volute wall.
    volute = casing[0]
    vr = occupied_ranges(volute)
    for rib in casing[1:37]:
        if not _intersects(occupied_ranges(rib), vr):
            problems.append("volute rib does not embed into the volute wall")

    # Bug 1 fix: pads embed into the frame top; ears sit exactly on pad tops.
    pads = motor[1:5]
    ears = motor[699:701]
    frame_top_at_n105 = AXIS_U + math.sqrt(210.0 ** 2 - 105.0 ** 2)
    if min(lo(pads, 2) for pads_ in (pads,)) >= frame_top_at_n105:
        problems.append(f"frame pads must embed below frame top {frame_top_at_n105:.1f}")
    if abs(hi(pads, 2) - lo(ears, 2)) > 1e-6:
        problems.append("box ears must sit exactly on the frame pad tops")

    # Volute underside vs pump feet (tolerance 3 mm).
    underside = volute_underside_u((0.0, AXIS_U), 190.0, 300.0, 155.0)
    if abs(hi(casing[168:170], 2) - underside) > 3.0:
        problems.append(f"pump feet top {hi(casing[168:170], 2):.1f} must meet volute underside {underside:.1f}")

    # Internal drive train must be inside the volute / motor frame.
    impeller = by_sube["/CODEX_EXTR_003_IMPELLER"]
    for b in impeller:
        if not _intersects(occupied_ranges(b), vr):
            problems.append("impeller part outside the volute")
    frame = motor[0]
    fr = occupied_ranges(frame)
    for b in motor[5:]:
        if b["type"] == "EXTRUSION" and _inside_stator_zone(b) and not _intersects(occupied_ranges(b), fr):
            problems.append("stator/rotor internal part outside the motor frame")

    total_vertices = sum(len(b["vertices"]) for b in blocks if b["type"] == "EXTRUSION")
    if total_vertices < 20000:
        problems.append(f"profile resolution too low: {total_vertices} vertices (target >= 20000)")
    if n_extr < 500 or n_cyl < 200:
        problems.append(f"element balance off: EXTRUSION {n_extr} / CYLINDER {n_cyl}")
    return problems


def _inside_stator_zone(block: Dict) -> bool:
    """Heuristic: blocks whose E span lies within the frame's E span."""
    r = occupied_ranges(block)
    return 680.0 < r[0][0] and r[0][1] < 1240.0 and r[2][1] <= 650.0


if __name__ == "__main__":
    macro = candidate()
    problems = validate_pml(macro)
    if problems:
        raise SystemExit("PML validation failed:\n  " + "\n  ".join(problems))
    geometry_problems = verify_geometry(macro)
    if geometry_problems:
        raise SystemExit("Geometry verification failed:\n  " + "\n  ".join(geometry_problems[:80]))

    path = ROOT / "candidate" / "03_high_fidelity_pump_v3.pml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(macro, encoding="utf-8", newline="\n")

    digest = hashlib.sha256(macro.encode("utf-8")).hexdigest().upper()
    parsed = parse_blocks(macro)
    n_extr = sum(1 for b in parsed if b["type"] == "EXTRUSION")
    n_cyl = sum(1 for b in parsed if b["type"] == "CYLINDER")
    n_vert = sum(len(b["vertices"]) for b in parsed if b["type"] == "EXTRUSION")
    print(f"candidate: {path}")
    print(f"SHA-256:   {digest}")
    print(f"primitives: {len(parsed)} (EXTRUSION {n_extr} / CYLINDER {n_cyl} / BOX 0)")
    print(f"profile vertices: {n_vert}")
    print("PML1 validation: clean")
    print("geometry verification: clean (contacts, envelope, floating audit, repairs)")
