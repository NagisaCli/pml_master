"""Generate the high-fidelity EXTRUSION pump certification candidate.

PML-STUDY-EXTR-002 / candidate 02. The user rejected candidate 01 as too
ordinary ("too ordinary, not enough detail, and it did not make full use of the EXTRUSION capability") and asked for
a physically detailed pump with no primitive-count ceiling. This candidate
answers with one end-suction centrifugal pump whose irregular solids are
built from EXTRUSION profiles wherever a custom section exists:

* volute casing - a true spiral profile, one EXTRUSION
* motor frame - a circle plus 12 cast cooling fins, one EXTRUSION
* impeller and fan blades - curved profile bands, one EXTRUSION per blade
* coupling elastomer - a 16-tooth star profile, one EXTRUSION
* fan shroud grille - 12 arc-strip bars
* base frame - H-section beams and corner-cut plates
* hex nuts, octagonal flanges, rounded anchor pads, nameplate

CYLINDER is used only where a body of revolution is the true form: shaft,
necks, studs, bosses, fan hub. No BOX is needed anywhere.

Every element form is individually VERIFIED in E3D Design Mk3.1.11.0
(EXTRUSION via PML-STUDY-EXTR-001/01-04; CYLINDER via production macros).
The assembly itself is new and awaits a user E3D verdict.
"""

from __future__ import annotations

import hashlib
import math
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[3]
sys.path.insert(0, str(REPO_ROOT))

from wsb.extrusion_builder import build_extrusion
from wsb.pml_builder import validate_pml


# ---------------------------------------------------------------------------
# Study-wide Reference Values (not client data)
# ---------------------------------------------------------------------------

AXIS_U = 400.0       # shaft centreline height above the base underside
BASE_TOP = 100.0     # top of the H-section base frame


def fmt(value: float) -> str:
    if abs(value) < 1e-9:
        value = 0.0
    return f"{value:.6f}".rstrip("0").rstrip(".") or "0"


# ---------------------------------------------------------------------------
# Profile generators
# ---------------------------------------------------------------------------


def circle_profile(radius: float, n: int = 24, center: Tuple[float, float] = (0.0, 0.0)) -> List[Tuple[float, float]]:
    return [
        (center[0] + radius * math.cos(2 * math.pi * i / n),
         center[1] + radius * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ]


def polygon_profile(radius: float, n: int, rotation_deg: float = 0.0, center: Tuple[float, float] = (0.0, 0.0)) -> List[Tuple[float, float]]:
    return [
        (center[0] + radius * math.cos(math.radians(rotation_deg + 360.0 * i / n)),
         center[1] + radius * math.sin(math.radians(rotation_deg + 360.0 * i / n)))
        for i in range(n)
    ]


def hex_profile(across_flats: float, center: Tuple[float, float] = (0.0, 0.0)) -> List[Tuple[float, float]]:
    radius = across_flats / math.sqrt(3.0)
    return polygon_profile(radius, 6, rotation_deg=30.0, center=center)


def rounded_rect_profile(width: float, height: float, r: float, segments: int = 4, center: Tuple[float, float] = (0.0, 0.0)) -> List[Tuple[float, float]]:
    """Axis-aligned rectangle with rounded corners, CCW from top-left."""
    cx, cy = center
    hw, hh = width / 2.0 - r, height / 2.0 - r
    corners = (
        (-hw, -hh),  # bottom-left
        (hw, -hh),   # bottom-right
        (hw, hh),    # top-right
        (-hw, hh),   # top-left
    )
    points: List[Tuple[float, float]] = []
    for index, (ox, oy) in enumerate(corners):
        start = math.pi / 2.0 * index
        for step in range(segments + 1):
            angle = start + math.pi / 2.0 * step / segments
            points.append((cx + ox + r * math.cos(angle), cy + oy + r * math.sin(angle)))
    return points


def h_beam_profile(flange: float = 120.0, height: float = 100.0, web: float = 12.0, flange_t: float = 14.0) -> List[Tuple[float, float]]:
    """H-section, local X across the flange, local Y along the web."""
    hw, hh = flange / 2.0, height / 2.0
    hw2, hh2 = web / 2.0, hh - flange_t
    return [
        (-hw, -hh), (hw, -hh), (hw, -hh + flange_t),
        (hw2, -hh + flange_t), (hw2, hh - flange_t),
        (hw, hh - flange_t), (hw, hh), (-hw, hh),
        (-hw, hh - flange_t), (-hw2, hh - flange_t),
        (-hw2, -hh + flange_t), (-hw, -hh + flange_t),
    ]


def volute_profile(center: Tuple[float, float], r0: float, r1: float, n: int = 18) -> List[Tuple[float, float]]:
    """Archimedean spiral + radial return slit, start at +U (top).

    The solid is a real volute outline: one full turn from r0 to r1 with the
    discharge throat at the top and a radial cutwater slit closing the loop.
    """
    cx, cy = center
    points = []
    for i in range(n + 1):
        theta = math.radians(90.0 + 360.0 * i / n)
        r = r0 + (r1 - r0) * i / n
        points.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
    return points


def finned_circle_profile(
    center: Tuple[float, float],
    radius: float,
    fin_height: float,
    fin_width_deg: float,
    n_fins: int,
    n_circle: int,
    fin_offset_deg: float,
) -> List[Tuple[float, float]]:
    """Circle with radial cooling fins merged into one LOOP."""
    cx, cy = center
    angles = sorted({360.0 * i / n_circle for i in range(n_circle)} |
                    {fin_offset_deg + 360.0 * k / n_fins + d for k in range(n_fins)
                     for d in (-fin_width_deg / 2.0, fin_width_deg / 2.0)})
    fin_edges = {fin_offset_deg + 360.0 * k / n_fins + d for k in range(n_fins)
                 for d in (-fin_width_deg / 2.0, fin_width_deg / 2.0)}
    points = []
    for angle in angles:
        theta = math.radians(angle)
        r = radius + fin_height if angle in fin_edges else radius
        points.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
    return points


def star_profile(root_radius: float, tip_radius: float, n_teeth: int, rotation_deg: float = 0.0) -> List[Tuple[float, float]]:
    points = []
    for i in range(n_teeth * 2):
        radius = tip_radius if i % 2 == 0 else root_radius
        angle = math.radians(rotation_deg + 360.0 * i / (n_teeth * 2))
        points.append((radius * math.cos(angle), radius * math.sin(angle)))
    return points


def arc_strip_profile(r_inner: float, r_outer: float, center_deg: float, span_deg: float, n_arc: int = 2) -> List[Tuple[float, float]]:
    """Radial strip following an arc: inner edge, outer edge, back."""
    points = []
    for i in range(n_arc + 1):
        angle = math.radians(center_deg - span_deg / 2.0 + span_deg * i / n_arc)
        points.append((r_inner * math.cos(angle), r_inner * math.sin(angle)))
    for i in range(n_arc + 1):
        angle = math.radians(center_deg + span_deg / 2.0 - span_deg * i / n_arc)
        points.append((r_outer * math.cos(angle), r_outer * math.sin(angle)))
    return points


def curved_blade_profile(
    center: Tuple[float, float],
    r_inner: float,
    r_outer: float,
    angle_deg: float,
    sweep_in_deg: float,
    sweep_out_deg: float,
    n: int = 5,
) -> List[Tuple[float, float]]:
    """Curved band between a swept back edge and a swept front edge."""
    cx, cy = center
    points = []
    for i in range(n + 1):
        t = i / n
        r = r_inner + (r_outer - r_inner) * t
        theta = math.radians(angle_deg + sweep_in_deg * t)
        points.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
    for i in range(n + 1):
        t = i / n
        r = r_outer - (r_outer - r_inner) * t
        theta = math.radians(angle_deg + sweep_out_deg * t)
        points.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
    return points


def radial_rib_profile(center: Tuple[float, float], theta_deg: float, r_inner: float, length: float, inner_half: float, outer_half: float) -> List[Tuple[float, float]]:
    """Trapezoid rib sitting on a circle at theta, pointing outward."""
    cx, cy = center
    theta = math.radians(theta_deg)
    di = math.atan2(inner_half, r_inner)
    do = math.atan2(outer_half, r_inner + length)
    points = (
        (cx + r_inner * math.cos(theta + di), cy + r_inner * math.sin(theta + di)),
        (cx + (r_inner + length) * math.cos(theta + do), cy + (r_inner + length) * math.sin(theta + do)),
        (cx + (r_inner + length) * math.cos(theta - do), cy + (r_inner + length) * math.sin(theta - do)),
        (cx + r_inner * math.cos(theta - di), cy + r_inner * math.sin(theta - di)),
    )
    return list(points)


# ---------------------------------------------------------------------------
# Primitive helpers
# ---------------------------------------------------------------------------


def extrusion(
    position: Tuple[float, float, float],
    orientation: str,
    height: float,
    profile: Sequence[Tuple[float, float]],
    level: Optional[Tuple[int, int]] = None,
) -> str:
    return build_extrusion(position, orientation, height, profile, level=level).rstrip()


def cylinder(
    diameter: float,
    height: float,
    start: Tuple[float, float, float],
    z_axis: str = "U",
    y_axis: str = "N",
) -> str:
    """Solid cylinder. ``start`` is the negative-end face along z_axis."""
    east, north, up = start
    axis = {"E": 0, "W": 0, "N": 1, "S": 1, "U": 2, "D": 2}[z_axis]
    centre = [east, north, up]
    if z_axis in ("E", "N", "U"):
        centre[axis] += height / 2.0
    else:
        centre[axis] -= height / 2.0
    return "\n".join(
        (
            "NEW CYLINDER",
            f"DIAM {fmt(diameter)}mm",
            f"HEIG {fmt(height)}mm",
            f"ORI Y IS {y_axis} AND Z IS {z_axis}",
            f"POS E {fmt(centre[0])}mm N {fmt(centre[1])}mm U {fmt(centre[2])}mm",
            "END",
        )
    )


def hex_nut(
    position: Tuple[float, float, float],
    orientation: str,
    across_flats: float,
    height: float = 20.0,
) -> str:
    return extrusion(position, orientation, height, hex_profile(across_flats), level=(5, 10))


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def base_frame() -> str:
    profile = h_beam_profile()
    parts = []
    for north in (-170.0, 170.0):
        parts.append(extrusion((-220.0, north, 50.0), "Y IS U AND Z IS E", 1900.0, profile))
    for east in (150.0, 900.0, 1450.0):
        parts.append(extrusion((east, -170.0, 50.0), "Y IS U AND Z IS N", 340.0, profile))

    pump_plate = [
        (-300.0, -200.0), (-250.0, -250.0), (250.0, -250.0), (300.0, -200.0),
        (300.0, 200.0), (250.0, 250.0), (-250.0, 250.0), (-300.0, 200.0),
    ]
    motor_plate = [
        (-460.0, -260.0), (-400.0, -320.0), (400.0, -320.0), (460.0, -260.0),
        (460.0, 260.0), (400.0, 320.0), (-400.0, 320.0), (-460.0, 260.0),
    ]
    parts.append(extrusion((120.0, 0.0, 80.0), "Y IS N AND Z IS U", 20.0, pump_plate))
    parts.append(extrusion((1020.0, 0.0, 80.0), "Y IS N AND Z IS U", 20.0, motor_plate))

    pad_profile = rounded_rect_profile(160.0, 30.0, 12.0, center=(0.0, 15.0))
    pad_centres = ((-180.0, -170.0), (-180.0, 170.0), (1670.0, -170.0), (1670.0, 170.0))
    for east, north in pad_centres:
        parts.append(extrusion((east - 80.0, north, 100.0), "Y IS U AND Z IS E", 160.0, pad_profile))
    for east, north in pad_centres:
        parts.append(cylinder(24.0, 50.0, (east, north, 100.0), z_axis="U", y_axis="N"))
    for east, north in pad_centres:
        parts.append(hex_nut((east, north, 130.0), "Y IS N AND Z IS U", 36.0))

    gusset = [(-80.0, 0.0), (0.0, 0.0), (0.0, 80.0)]
    for east, north in ((130.0, -240.0), (210.0, -240.0), (130.0, 240.0), (210.0, 240.0)):
        parts.append(extrusion((east, north, 100.0), "Y IS U AND Z IS N", 12.0, gusset))
    for east, north in ((730.0, -300.0), (810.0, -300.0), (730.0, 300.0), (810.0, 300.0)):
        parts.append(extrusion((east, north, 100.0), "Y IS U AND Z IS N", 12.0, gusset))
    return "\n".join(parts)


def casing() -> str:
    parts = []
    # Volute body: one spiral EXTRUSION, profile end plane at E -130.
    parts.append(extrusion((-130.0, 0.0, 0.0), "Y IS U AND Z IS E", 260.0,
                           volute_profile((0.0, AXIS_U), 190.0, 280.0, 18)))

    # Suction side (-E): neck, octagonal flange, 8 studs + nuts. The flange
    # profile plane sits on the neck face (E -160) and sweeps toward -E.
    parts.append(cylinder(190.0, 30.0, (-160.0, 0.0, AXIS_U), z_axis="E", y_axis="U"))
    flange_profile = polygon_profile(130.0, 8, rotation_deg=22.5)
    parts.append(extrusion((-160.0, 0.0, AXIS_U), "Y IS N AND Z IS W", 28.0, flange_profile))
    for k in range(8):
        north = 105.0 * math.cos(math.radians(22.5 + 45.0 * k))
        up = AXIS_U + 105.0 * math.sin(math.radians(22.5 + 45.0 * k))
        parts.append(cylinder(14.0, 48.0, (-208.0, north, up), z_axis="E", y_axis="N"))
    for k in range(8):
        north = 105.0 * math.cos(math.radians(22.5 + 45.0 * k))
        up = AXIS_U + 105.0 * math.sin(math.radians(22.5 + 45.0 * k))
        parts.append(hex_nut((-188.0, north, up), "Y IS N AND Z IS W", 24.0))

    # Discharge side (+U): neck, octagonal flange, 8 studs + nuts.
    parts.append(cylinder(150.0, 80.0, (0.0, 0.0, 680.0), z_axis="U", y_axis="N"))
    discharge_profile = polygon_profile(110.0, 8, rotation_deg=22.5)
    parts.append(extrusion((0.0, 0.0, 760.0), "Y IS N AND Z IS U", 24.0, discharge_profile))
    for k in range(8):
        east = 88.0 * math.sin(math.radians(22.5 + 45.0 * k))
        north = 88.0 * math.cos(math.radians(22.5 + 45.0 * k))
        parts.append(cylinder(12.0, 44.0, (east, north, 760.0), z_axis="U", y_axis="N"))
    for k in range(8):
        east = 88.0 * math.sin(math.radians(22.5 + 45.0 * k))
        north = 88.0 * math.cos(math.radians(22.5 + 45.0 * k))
        parts.append(hex_nut((east, north, 784.0), "Y IS N AND Z IS U", 19.0))

    # Seal gland on the +E volute face + boss for the bearing housing.
    parts.append(extrusion((130.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 24.0,
                           rounded_rect_profile(190.0, 190.0, 25.0)))
    parts.append(cylinder(110.0, 30.0, (154.0, 0.0, AXIS_U), z_axis="E", y_axis="U"))

    # Pump feet: bottom face on the base plate, top face under the volute.
    foot_profile = [(-150.0, 0.0), (150.0, 0.0), (150.0, 105.0), (-150.0, 105.0)]
    parts.append(extrusion((0.0, 135.0, 100.0), "Y IS U AND Z IS N", 40.0, foot_profile))
    parts.append(extrusion((0.0, -175.0, 100.0), "Y IS U AND Z IS N", 40.0, foot_profile))

    # Radial ribs on the +E volute face.
    for theta in (30.0, 150.0, 210.0, 330.0):
        r = 190.0 + 90.0 * theta / 360.0
        parts.append(extrusion((130.0, 0.0, 0.0), "Y IS U AND Z IS E", 10.0,
                               radial_rib_profile((0.0, AXIS_U), theta, r, 55.0, 12.0, 8.0)))
    return "\n".join(parts)


def impeller() -> str:
    parts = [
        cylinder(90.0, 100.0, (-50.0, 0.0, AXIS_U), z_axis="E", y_axis="U"),
        cylinder(210.0, 20.0, (-70.0, 0.0, AXIS_U), z_axis="E", y_axis="U"),
    ]
    for k in range(6):
        blade = curved_blade_profile((0.0, AXIS_U), 50.0, 135.0, 60.0 * k, 15.0, 35.0)
        parts.append(extrusion((-50.0, 0.0, 0.0), "Y IS U AND Z IS E", 100.0, blade))
    return "\n".join(parts)


def bearing() -> str:
    parts = [
        extrusion((150.0, 0.0, 0.0), "Y IS U AND Z IS E", 150.0,
                  finned_circle_profile((0.0, AXIS_U), 150.0, 25.0, 8.0, 8, 16, 22.5)),
    ]
    foot_profile = [(-45.0, 0.0), (45.0, 0.0), (30.0, 125.0), (-30.0, 125.0)]
    parts.append(extrusion((190.0, 110.0, 100.0), "Y IS U AND Z IS N", 40.0, foot_profile))
    parts.append(extrusion((190.0, -150.0, 100.0), "Y IS U AND Z IS N", 40.0, foot_profile))
    cap_profile = polygon_profile(165.0, 8, rotation_deg=22.5)
    parts.append(extrusion((154.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 20.0, cap_profile))
    parts.append(extrusion((300.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 20.0, cap_profile))
    parts.append(cylinder(55.0, 710.0, (-60.0, 0.0, AXIS_U), z_axis="E", y_axis="U"))
    return "\n".join(parts)


def coupling() -> str:
    hub = polygon_profile(85.0, 6, rotation_deg=30.0)
    elastomer = star_profile(55.0, 75.0, 16, rotation_deg=11.25)
    parts = [
        extrusion((320.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 60.0, hub),
        extrusion((380.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 90.0, elastomer),
        extrusion((470.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 40.0, hub),
    ]
    shroud = [
        (-180.0, 100.0), (-130.0, 100.0), (-130.0, 290.0), (-140.0, 610.0),
        (140.0, 610.0), (130.0, 290.0), (130.0, 100.0), (180.0, 100.0),
    ]
    parts.append(extrusion((320.0, 0.0, 0.0), "Y IS U AND Z IS E", 240.0, shroud))
    return "\n".join(parts)


def motor() -> str:
    parts = []
    # Frame: circle + 12 cast fins in one profile.
    parts.append(extrusion((600.0, 0.0, 0.0), "Y IS U AND Z IS E", 560.0,
                           finned_circle_profile((0.0, AXIS_U), 210.0, 35.0, 12.0, 12, 24, 7.5)))

    # DE end: boss + disc.
    parts.append(extrusion((510.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 40.0, circle_profile(130.0)))
    parts.append(extrusion((550.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 50.0, circle_profile(235.0)))
    # NDE end: disc + boss.
    parts.append(extrusion((1160.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 50.0, circle_profile(235.0)))
    parts.append(extrusion((1210.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 40.0, circle_profile(130.0)))

    # Feet: four trapezoids whose tops follow the frame underside at N +-160.
    foot_profile = [(-80.0, 0.0), (80.0, 0.0), (60.0, 164.0), (-60.0, 164.0)]
    for east in (770.0, 1030.0):
        parts.append(extrusion((east, 150.0, 100.0), "Y IS U AND Z IS N", 20.0, foot_profile))
        parts.append(extrusion((east, -170.0, 100.0), "Y IS U AND Z IS N", 20.0, foot_profile))

    # End-cover studs: 6 per end, seated on the disc outer faces.
    stud_angles = [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]
    for angle in stud_angles:
        north = 205.0 * math.cos(math.radians(angle))
        up = AXIS_U + 205.0 * math.sin(math.radians(angle))
        parts.append(hex_nut((550.0, north, up), "Y IS U AND Z IS E", 17.0, 20.0))
        parts.append(cylinder(10.0, 70.0, (550.0, north, up), z_axis="E", y_axis="U"))
    for angle in stud_angles:
        north = 205.0 * math.cos(math.radians(angle))
        up = AXIS_U + 205.0 * math.sin(math.radians(angle))
        parts.append(hex_nut((1230.0, north, up), "Y IS U AND Z IS E", 17.0, 20.0))
        parts.append(cylinder(10.0, 70.0, (1180.0, north, up), z_axis="E", y_axis="U"))

    # Terminal box: body, lid, two cable glands, two mounting ears.
    box_profile = rounded_rect_profile(170.0, 130.0, 20.0, center=(0.0, 655.0))
    parts.append(extrusion((830.0, 0.0, 0.0), "Y IS U AND Z IS E", 160.0, box_profile))
    parts.append(extrusion((990.0, 0.0, 0.0), "Y IS U AND Z IS E", 10.0, box_profile))
    ear_profile = [(-10.0, 590.0), (10.0, 590.0), (10.0, 610.0), (-10.0, 610.0)]
    for north in (-100.0, 100.0):
        parts.append(extrusion((830.0, north, 0.0), "Y IS U AND Z IS E", 160.0, ear_profile))
    for east in (870.0, 950.0):
        parts.append(cylinder(28.0, 40.0, (east, 0.0, 720.0), z_axis="U", y_axis="N"))

    # Fan: hub, 8 curved blades.
    parts.append(cylinder(110.0, 90.0, (1250.0, 0.0, AXIS_U), z_axis="E", y_axis="U"))
    for k in range(8):
        blade = curved_blade_profile((0.0, AXIS_U), 60.0, 195.0, 45.0 * k, 10.0, 28.0)
        parts.append(extrusion((1300.0, 0.0, 0.0), "Y IS U AND Z IS E", 10.0, blade))

    # Shroud: front ring, 12 grille bars, rear disc.
    parts.append(extrusion((1270.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(240.0)))
    for k in range(12):
        bar = arc_strip_profile(213.0, 227.0, 7.5 + 30.0 * k, 26.0)
        parts.append(extrusion((1278.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 88.0, bar))
    parts.append(extrusion((1358.0, 0.0, AXIS_U), "Y IS U AND Z IS E", 8.0, circle_profile(240.0)))

    # Nameplate embedded into the fin envelope.
    parts.append(extrusion((1060.0, 248.0, 0.0), "Y IS U AND Z IS E", 5.0,
                           rounded_rect_profile(100.0, 60.0, 10.0, center=(0.0, 368.0))))
    return "\n".join(parts)


def fasteners() -> str:
    parts = []
    # Pump-foot connection bolts: heads on the foot top face.
    for east, north in ((-70.0, 155.0), (70.0, 155.0), (-70.0, -155.0), (70.0, -155.0)):
        parts.append(hex_nut((east, north, 224.0), "Y IS N AND Z IS U", 22.0, 20.0))
        parts.append(cylinder(12.0, 40.0, (east, north, 224.0), z_axis="U", y_axis="N"))
    # Gland bolts: 4 seated on the gland outer face.
    for angle in (45.0, 135.0, 225.0, 315.0):
        north = 75.0 * math.cos(math.radians(angle))
        up = AXIS_U + 75.0 * math.sin(math.radians(angle))
        parts.append(hex_nut((154.0, north, up), "Y IS U AND Z IS E", 13.0, 20.0))
        parts.append(cylinder(10.0, 44.0, (130.0, north, up), z_axis="E", y_axis="U"))
    # Bearing end-cap bolts: 4 per cap.
    for angle in (45.0, 135.0, 225.0, 315.0):
        north = 140.0 * math.cos(math.radians(angle))
        up = AXIS_U + 140.0 * math.sin(math.radians(angle))
        parts.append(hex_nut((174.0, north, up), "Y IS U AND Z IS E", 13.0, 20.0))
        parts.append(cylinder(10.0, 40.0, (154.0, north, up), z_axis="E", y_axis="U"))
    for angle in (45.0, 135.0, 225.0, 315.0):
        north = 140.0 * math.cos(math.radians(angle))
        up = AXIS_U + 140.0 * math.sin(math.radians(angle))
        parts.append(hex_nut((320.0, north, up), "Y IS U AND Z IS E", 13.0, 20.0))
        parts.append(cylinder(10.0, 40.0, (300.0, north, up), z_axis="E", y_axis="U"))
    return "\n".join(parts)


def wrap(name: str, body: str, description: str) -> str:
    return "\n".join(
        (
            "$S-  -- Synonym translation OFF",
            "ONERROR GOLABEL /ERROR3",
            "INPUT BEGIN",
            f"NEW EQUIPMENT /{name}",
            "POS E 0mm N 0mm U 0mm",
            f"DESC '{description}'",
            body.rstrip(),
            "END",
            f"INPUT END EQUIPMENT /{name}",
            "INPUT FINISH",
            "LABEL /ERROR3",
            "handle ANY",
            "$S+",
            "RETURN ERROR",
            "endhandle",
            "$S+  -- Synonym translation ON",
            "",
        )
    )


def candidate() -> str:
    subes = [
        ("CODEX_EXTR_002_BASE", base_frame()),
        ("CODEX_EXTR_002_CASING", casing()),
        ("CODEX_EXTR_002_IMPELLER", impeller()),
        ("CODEX_EXTR_002_BEARING", bearing()),
        ("CODEX_EXTR_002_COUPLING", coupling()),
        ("CODEX_EXTR_002_MOTOR", motor()),
        ("CODEX_EXTR_002_FASTENERS", fasteners()),
    ]
    body = "\n".join(
        f"NEW SUBEQUIPMENT /{name}\n{macro}\nEND" for name, macro in subes
    )
    return wrap(
        "CODEX_EXTR_002_PUMP",
        body,
        "HIGH-FIDELITY END-SUCTION PUMP - EXTRUSION PROFILE STUDY",
    )


# ---------------------------------------------------------------------------
# Numerical verification
# ---------------------------------------------------------------------------

_NEW = re.compile(r"^NEW\s+(CYLINDER|CONE|DISH|BOX|EXTRUSION)\b", re.I)
_SUBE = re.compile(r"^NEW\s+SUBEQUIPMENT\s+(/\S+)", re.I)
_ATTR = re.compile(r"^(DIAM|HEIG|DTOP|DBOT|RADIUS|XLEN|YLEN|ZLEN|POS|ORI|LEVE)\s+(.*)$", re.I)
_ORI = re.compile(r"^Y\s+IS\s+([ENWSUD])\s+AND\s+Z\s+IS\s+([ENWSUD])$", re.I)

_VECTORS = {
    "E": (1.0, 0.0, 0.0),
    "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0),
    "S": (0.0, -1.0, 0.0),
    "U": (0.0, 0.0, 1.0),
    "D": (0.0, 0.0, -1.0),
}


def _numbers(text: str) -> List[float]:
    return [float(m) for m in re.findall(r"[-+]?\d+(?:\.\d+)?", text)]


def _cross(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def parse_blocks(macro: str) -> List[Dict]:
    blocks: List[Dict] = []
    sube: Optional[str] = None
    block: Optional[Dict] = None
    depth = 0
    for raw in macro.splitlines():
        line = raw.strip()
        sube_match = _SUBE.match(line)
        if sube_match:
            sube = sube_match.group(1)
            continue
        new_match = _NEW.match(line)
        if new_match:
            block = {"type": new_match.group(1).upper(), "sube": sube, "attrs": {}, "vertices": [], "order": []}
            if block["type"] == "EXTRUSION":
                depth = 0
            continue
        if block is None:
            continue
        if line == "END":
            if block["type"] == "EXTRUSION":
                if depth == 0:
                    blocks.append(block)
                    block = None
                elif depth == 1:
                    depth = 0
                else:
                    depth = 1
            else:
                blocks.append(block)
                block = None
            continue
        if line.startswith("NEW LOOP"):
            depth = 1
            continue
        if line.startswith("NEW VERTEX"):
            depth = 2
            continue
        if block["type"] == "EXTRUSION" and depth > 0:
            if depth == 2:
                east, north, _ = _numbers(line)
                block["vertices"].append((east, north))
            continue
        attr_match = _ATTR.match(line)
        if attr_match and not line.startswith("NEW "):
            key = attr_match.group(1).upper()
            if key == "ORI":
                block["attrs"][key] = attr_match.group(2).strip()
            else:
                block["attrs"][key] = _numbers(attr_match.group(2))
            block["order"].append(key)
    return blocks


def _pos(block: Dict) -> Tuple[float, float, float]:
    e, n, u = block["attrs"].get("POS", [0.0, 0.0, 0.0])
    return float(e), float(n), float(u)


def _orientation(block: Dict) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    text = block["attrs"].get("ORI")
    match = _ORI.fullmatch(" ".join(text.upper().split()))
    if not match:
        raise AssertionError(f"unparseable ORI {text!r}")
    y_axis, z_axis = match.groups()
    return _VECTORS[y_axis], _VECTORS[z_axis]


def occupied_ranges(block: Dict) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
    pos = _pos(block)
    kind = block["type"]
    attrs = block["attrs"]

    if kind in ("CYLINDER", "CONE"):
        height = float(attrs["HEIG"][0])
        half = height / 2.0
        zv = _orientation(block)[1]
        ranges = [(p - half, p + half) if zv[axis] else (p, p) for axis, p in enumerate(pos)]
        return tuple(ranges)  # type: ignore[return-value]

    if kind == "BOX":
        half = (float(attrs["XLEN"][0]) / 2.0, float(attrs["YLEN"][0]) / 2.0, float(attrs["ZLEN"][0]) / 2.0)
        return tuple((pos[axis] - half[axis], pos[axis] + half[axis]) for axis in range(3))  # type: ignore[return-value]

    if kind == "DISH":
        height = float(attrs["HEIG"][0])
        zv = _orientation(block)[1]
        ranges = []
        for axis, p in enumerate(pos):
            if zv[axis] == 1.0:
                ranges.append((p, p + height))
            elif zv[axis] == -1.0:
                ranges.append((p - height, p))
            else:
                ranges.append((p, p))
        return tuple(ranges)  # type: ignore[return-value]

    if kind == "EXTRUSION":
        height = float(attrs["HEIG"][0])
        yv, zv = _orientation(block)
        xv = _cross(yv, zv)
        xs = [vertex[0] for vertex in block["vertices"]]
        ys = [vertex[1] for vertex in block["vertices"]]
        extents = ((xv, (min(xs), max(xs))), (yv, (min(ys), max(ys))), (zv, (0.0, height)))
        ranges = []
        for axis in range(3):
            lo = hi = pos[axis]
            for vector, (a, b) in extents:
                if vector[axis] == 1.0:
                    lo += a
                    hi += b
                elif vector[axis] == -1.0:
                    lo += -b
                    hi += -a
            ranges.append((lo, hi))
        return tuple(ranges)  # type: ignore[return-value]

    raise AssertionError(f"unhandled primitive {kind}")


def _area(vertices: Sequence[Tuple[float, float]]) -> float:
    return abs(
        0.5
        * sum(
            x1 * y2 - x2 * y1
            for (x1, y1), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1])
        )
    )


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


def verify_geometry(macro: str) -> List[str]:
    problems: List[str] = []
    blocks = parse_blocks(macro)
    if not blocks:
        return ["no primitive blocks parsed"]

    by_sube: Dict[str, List[Dict]] = {}
    for block in blocks:
        by_sube.setdefault(block["sube"], []).append(block)

    expected_subes = {
        "/CODEX_EXTR_002_BASE": 27,
        "/CODEX_EXTR_002_CASING": 45,
        "/CODEX_EXTR_002_IMPELLER": 8,
        "/CODEX_EXTR_002_BEARING": 6,
        "/CODEX_EXTR_002_COUPLING": 4,
        "/CODEX_EXTR_002_MOTOR": 63,
        "/CODEX_EXTR_002_FASTENERS": 32,
    }
    for name, count in expected_subes.items():
        if len(by_sube.get(name, [])) != count:
            problems.append(f"{name}: expected {count} primitives, got {len(by_sube.get(name, []))}")

    if len(blocks) != 185:
        problems.append(f"expected 185 primitives, got {len(blocks)}")
    if sum(1 for b in blocks if b["type"] == "EXTRUSION") != 128:
        problems.append(f"expected 128 EXTRUSION, got {sum(1 for b in blocks if b['type'] == 'EXTRUSION')}")
    if sum(1 for b in blocks if b["type"] == "CYLINDER") != 57:
        problems.append(f"expected 57 CYLINDER, got {sum(1 for b in blocks if b['type'] == 'CYLINDER')}")
    if sum(1 for b in blocks if b["type"] == "BOX") != 0:
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
    if high_u > 860.0 or low_e < -260.0 or high_e > 1800.0 or low_n < -430.0 or high_n > 430.0:
        problems.append(f"assembly escapes its envelope E {low_e:.0f}..{high_e:.0f}, "
                        f"N {low_n:.0f}..{high_n:.0f}, U {low_u:.0f}..{high_u:.0f}")

    for block in blocks:
        for key in ("DIAM", "HEIG", "DTOP", "DBOT", "RADIUS", "XLEN", "YLEN", "ZLEN"):
            if key in block["attrs"] and any(v <= 0 for v in block["attrs"][key]):
                problems.append(f"{block['sube']}: {block['type']} has non-positive {key}")
        if block["type"] == "EXTRUSION":
            if len(block["vertices"]) < 3 or _area(block["vertices"]) < 1e-6:
                problems.append(f"{block['sube']}: degenerate EXTRUSION profile")
        order = block["order"]
        if block["type"] in ("CYLINDER", "CONE", "DISH") and (
            "ORI" not in order or "POS" not in order or order.index("POS") < order.index("ORI")
        ):
            problems.append(f"{block['sube']}: {block['type']} violates ORI-before-POS")

    def lo(blocks_: Sequence[Dict], axis: int) -> float:
        return min(occupied_ranges(b)[axis][0] for b in blocks_)

    def hi(blocks_: Sequence[Dict], axis: int) -> float:
        return max(occupied_ranges(b)[axis][1] for b in blocks_)

    base = by_sube["/CODEX_EXTR_002_BASE"]
    casing = by_sube["/CODEX_EXTR_002_CASING"]
    bearing = by_sube["/CODEX_EXTR_002_BEARING"]
    coupling = by_sube["/CODEX_EXTR_002_COUPLING"]
    motor = by_sube["/CODEX_EXTR_002_MOTOR"]

    # Shaft centreline: every axial body of revolution sits on N 0, U 400.
    for sube, blocks_ in by_sube.items():
        for b in blocks_:
            if b["type"] == "CYLINDER":
                y, z = _orientation(b)
                if z == (1.0, 0.0, 0.0) and float(b["attrs"]["DIAM"][0]) > 40.0:
                    r = occupied_ranges(b)
                    if abs(r[1][0] + r[1][1]) > 1e-6 or abs(r[2][0] + r[2][1] - 800.0) > 1e-6:
                        problems.append(f"{sube}: axial cylinder not on shaft centreline N 0 U 400")

    # Base frame: top at U 100 carries everything.
    if hi(base, 2) < 100.0:
        problems.append("base frame top must be at least U 100")
    for label, blocks_ in (
        ("pump feet", casing[39:41]),
        ("bearing feet", bearing[1:3]),
        ("motor feet", motor[5:9]),
        ("shroud", coupling[3:4]),
    ):
        if abs(lo(blocks_, 2) - 100.0) > 1e-6:
            problems.append(f"{label} must sit on the base top U 100")

    # Volute underside vs pump feet (tolerance 3 mm).
    underside = volute_underside_u((0.0, AXIS_U), 190.0, 280.0, 155.0)
    if abs(hi(casing[39:41], 2) - underside) > 3.0:
        problems.append(f"pump feet top {hi(casing[39:41], 2):.1f} must meet volute underside {underside:.1f}")

    # Suction chain contacts.
    neck = casing[1]
    if hi([neck], 0) != -130.0 or lo([neck], 0) != -160.0:
        problems.append("suction neck must span E -160..-130")
    if hi(casing[2:3], 0) != -160.0 or lo(casing[2:3], 0) != -188.0:
        problems.append("suction flange must span E -188..-160")

    # Discharge chain contacts.
    if hi(casing[19:20], 2) != 760.0 or lo(casing[19:20], 2) != 680.0:
        problems.append("discharge neck must span U 680..760")
    if hi(casing[20:21], 2) != 784.0 or lo(casing[20:21], 2) != 760.0:
        problems.append("discharge flange must span U 760..784")

    # Gland and bearing chain.
    if hi(casing[37:38], 0) != 154.0 or lo(casing[37:38], 0) != 130.0:
        problems.append("seal gland must span E 130..154")
    if hi(bearing[0:1], 0) != 300.0 or lo(bearing[0:1], 0) != 150.0:
        problems.append("bearing housing must span E 150..300")
    if hi(bearing[4:5], 0) != 320.0 or lo(bearing[4:5], 0) != 300.0:
        problems.append("bearing +E cap must span E 300..320")

    # Coupling chain contacts.
    chain = (
        (coupling[0], 320.0, 380.0, "pump hub"),
        (coupling[1], 380.0, 470.0, "elastomer"),
        (coupling[2], 470.0, 510.0, "motor hub"),
    )
    for block, a, b, label in chain:
        r = occupied_ranges(block)
        if abs(r[0][0] - a) > 1e-6 or abs(r[0][1] - b) > 1e-6:
            problems.append(f"{label} must span E {a}..{b}")
    motor_de_boss = motor[1]
    motor_de_disc = motor[2]
    motor_frame = motor[0]
    for block, a, b, label in (
        (motor_de_boss, 510.0, 550.0, "motor DE boss"),
        (motor_de_disc, 550.0, 600.0, "motor DE disc"),
        (motor_frame, 600.0, 1160.0, "motor frame"),
    ):
        r = occupied_ranges(block)
        if abs(r[0][0] - a) > 1e-6 or abs(r[0][1] - b) > 1e-6:
            problems.append(f"{label} must span E {a}..{b}")

    # Motor feet tops meet the frame underside at N 160 (tolerance 2 mm).
    if abs(hi(motor[5:9], 2) - 264.0) > 2.0:
        problems.append(f"motor feet tops must meet frame underside 264, got {hi(motor[5:9], 2):.1f}")

    # Shroud covers the coupling.
    shroud = coupling[3]
    sr = occupied_ranges(shroud)
    if sr[0][0] != 320.0 or sr[0][1] != 560.0 or sr[2][1] < 510.0:
        problems.append("shroud must cover the coupling E 320..560, U to 610")

    return problems


if __name__ == "__main__":
    macro = candidate()
    problems = validate_pml(macro)
    if problems:
        raise SystemExit("PML validation failed:\n  " + "\n  ".join(problems))
    geometry_problems = verify_geometry(macro)
    if geometry_problems:
        raise SystemExit("Geometry verification failed:\n  " + "\n  ".join(geometry_problems))

    path = ROOT / "candidate" / "02_high_fidelity_pump.pml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(macro, encoding="utf-8", newline="\n")

    digest = hashlib.sha256(macro.encode("utf-8")).hexdigest().upper()
    count = len(parse_blocks(macro))
    print(f"candidate: {path}")
    print(f"SHA-256:   {digest}")
    print(f"primitives: {count} (EXTRUSION {sum(1 for b in parse_blocks(macro) if b['type'] == 'EXTRUSION')} / "
          f"CYLINDER {sum(1 for b in parse_blocks(macro) if b['type'] == 'CYLINDER')} / BOX 0)")
    print("PML1 validation: clean")
    print("geometry verification: clean (contacts, bounds, axis, lowest point)")
