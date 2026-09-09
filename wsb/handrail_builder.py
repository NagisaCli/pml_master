"""
Structural Handrail Builder
===========================
Emits AVEVA E3D PML structural handrail (``HANDRA``) and route path (``RPATH``)
geometry commands according to native E3D data listings (PML-STUDY-HANDRA-001).

Supports:
- Parameterized rail heights (dual-rail top/intermediate heights: ``RAILHE``)
- Post spacing (``POSTSP``), tangent offset (``TANGOF``), kickplate flag (``SHOWKP``)
- Bend radius (``BRAD``) and route point fillet radius (``FRAD``)
- Circular arc interpolation using intermediate ``CURVE`` points with ``CURTYP THRU``
- Start and end path tangent direction vectors (``DRNS`` / ``DRNE``)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple

from .pml_builder import PMLValidationError, validate_pml

Point3D = Tuple[float, float, float]


def _fmt(value: float, decimals: int = 2) -> str:
    """Format coordinate with finite bounds and clean trailing decimals."""
    if not math.isfinite(value):
        raise PMLValidationError(f"Handrail coordinate must be finite, got {value!r}")
    if abs(value) < 1e-9:
        value = 0.0
    rounded = round(value, decimals)
    if abs(rounded - round(rounded)) < 1e-9:
        return str(int(round(rounded)))
    return f"{rounded:.{decimals}f}".rstrip("0").rstrip(".") or "0"


def _fmt_pos(e: float, n: float, u: float) -> str:
    """Emit formatted E3D POS string with quadrant letters."""
    parts: List[str] = []
    if e >= 0:
        parts.append(f"E {_fmt(e)}mm")
    else:
        parts.append(f"W {_fmt(-e)}mm")

    if n >= 0:
        parts.append(f"N {_fmt(n)}mm")
    else:
        parts.append(f"S {_fmt(-n)}mm")

    if u >= 0:
        parts.append(f"U {_fmt(u)}mm")
    else:
        parts.append(f"D {_fmt(-u)}mm")

    return " ".join(parts)


@dataclass(frozen=True)
class RoutePoint:
    """A control vertex in a handrail route path."""

    position: Optional[Point3D] = None
    fillet_radius: float = 100.0

    def __post_init__(self) -> None:
        if self.fillet_radius < 0:
            raise PMLValidationError(f"Fillet radius must be non-negative, got {self.fillet_radius}")
        if self.position is not None:
            for coord in self.position:
                if not math.isfinite(coord):
                    raise PMLValidationError(f"RoutePoint coordinate must be finite, got {coord!r}")


@dataclass(frozen=True)
class RouteCurve:
    """An arc interpolation point in a handrail route path."""

    position: Point3D
    curve_type: str = "THRU"

    def __post_init__(self) -> None:
        for coord in self.position:
            if not math.isfinite(coord):
                raise PMLValidationError(f"RouteCurve coordinate must be finite, got {coord!r}")
        if self.curve_type.upper() not in {"THRU", "RAD"}:
            raise PMLValidationError(f"Unsupported CURTYP {self.curve_type!r}; expected 'THRU' or 'RAD'")


@dataclass
class HandrailSpec:
    """Specification for an E3D structural HANDRA element."""

    name: Optional[str] = None
    position: Point3D = (0.0, 0.0, 0.0)
    top_rail_height: float = 1250.0
    mid_rail_height: float = 750.0
    post_spacing: float = 1000.0
    tangent_offset: float = 300.0
    show_kickplate: bool = True
    bend_radius: float = 100.0
    fire_rating: int = 0
    built: bool = False
    shop: bool = False
    start_direction: Optional[str] = None
    end_direction: Optional[str] = None
    path_items: Sequence[RoutePoint | RouteCurve] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.top_rail_height <= 0 or self.mid_rail_height <= 0:
            raise PMLValidationError("Rail heights must be positive")
        if self.top_rail_height <= self.mid_rail_height:
            raise PMLValidationError("Top rail height must be greater than mid rail height")
        if self.post_spacing <= 0:
            raise PMLValidationError("Post spacing must be positive")
        if len(self.path_items) < 2:
            raise PMLValidationError("Route path must have at least 2 points")


class HandrailBuilder:
    """Builder for generating AVEVA E3D PML1 structural HANDRA blocks."""

    def build(self, spec: HandrailSpec) -> str:
        lines: List[str] = []
        
        # HANDRA header
        name_clause = f" /{spec.name.strip().lstrip('/')}" if spec.name else ""
        lines.append(f"NEW HANDRA{name_clause}")
        lines.append(f"POS {_fmt_pos(*spec.position)}")
        lines.append(f"RAILHE {_fmt(spec.top_rail_height)}mm {_fmt(spec.mid_rail_height)}mm")
        lines.append(f"POSTSP {_fmt(spec.post_spacing)}mm")
        lines.append(f"TANGOF {_fmt(spec.tangent_offset)}mm")
        lines.append(f"SHOWKP {'true' if spec.show_kickplate else 'false'}")
        lines.append(f"BRAD {_fmt(spec.bend_radius)}mm")
        lines.append(f"FIRE {spec.fire_rating}")
        lines.append(f"BUIL {'true' if spec.built else 'false'}")
        lines.append(f"SHOP {'true' if spec.shop else 'false'}")
        lines.append("")

        # RPATH container
        lines.append("NEW RPATH")
        if spec.start_direction:
            lines.append(f"DRNS {spec.start_direction}")
        if spec.end_direction:
            lines.append(f"DRNE {spec.end_direction}")
        lines.append("")

        # Path items
        for item in spec.path_items:
            if isinstance(item, RoutePoint):
                lines.append("NEW POINTR")
                if item.position is not None:
                    lines.append(f"POS {_fmt_pos(*item.position)}")
                if item.fillet_radius > 0:
                    lines.append(f"FRAD {_fmt(item.fillet_radius)}mm")
                lines.append("END")
            elif isinstance(item, RouteCurve):
                lines.append("NEW CURVE")
                lines.append(f"POS {_fmt_pos(*item.position)}")
                lines.append(f"CURTYP {item.curve_type.upper()}")
                lines.append("END")

        lines.append("END")  # closes RPATH
        lines.append("END")  # closes HANDRA

        macro = "\n".join(lines) + "\n"
        errors = validate_pml(macro)
        if errors:
            raise PMLValidationError("Generated HANDRA macro failed PML validation: " + "; ".join(errors))
        return macro


def build_circular_handrail(
    center_local: Tuple[float, float],
    radius: float,
    *,
    elevation: float = 0.0,
    name: Optional[str] = None,
    position: Point3D = (0.0, 0.0, 0.0),
    top_rail_height: float = 1250.0,
    mid_rail_height: float = 750.0,
    post_spacing: float = 1000.0,
    tangent_offset: float = 300.0,
    fillet_radius: float = 100.0,
    start_direction: str = "E 22.5 N",
    end_direction: str = "E 22.5 S",
) -> str:
    """
    Build a 4-quadrant circular structural handrail using native 8-point discretization
    (4 vertices with POINTR + 4 mid-arc through points with CURVE CURTYP THRU).
    """
    if radius <= 0:
        raise PMLValidationError(f"Circular handrail radius must be positive, got {radius}")

    ec, nc = center_local
    s45 = math.sin(math.pi / 4.0)  # ~0.70710678

    # 8 points around the circle in local coordinates (starting at -90 deg South):
    # theta = -90 (start): (0, 0) relative to (ec, nc - radius)
    # theta = -45: (ec + radius * s45, nc - radius * s45)
    # theta = 0 (East): (ec + radius, nc)
    # theta = 45: (ec + radius * s45, nc + radius * s45)
    # theta = 90 (North): (ec, nc + radius)
    # theta = 135: (ec - radius * s45, nc + radius * s45)
    # theta = 180 (West): (ec - radius, nc)
    # theta = 225: (ec - radius * s45, nc - radius * s45)
    # theta = 270 (end): (0, 0)

    path_items: List[RoutePoint | RouteCurve] = [
        RoutePoint(position=None, fillet_radius=fillet_radius),
        RouteCurve(position=(ec + radius * s45, nc - radius * s45, elevation), curve_type="THRU"),
        RoutePoint(position=(ec + radius, nc, elevation), fillet_radius=fillet_radius),
        RouteCurve(position=(ec + radius * s45, nc + radius * s45, elevation), curve_type="THRU"),
        RoutePoint(position=(ec, nc + radius, elevation), fillet_radius=fillet_radius),
        RouteCurve(position=(ec - radius * s45, nc + radius * s45, elevation), curve_type="THRU"),
        RoutePoint(position=(ec - radius, nc, elevation), fillet_radius=fillet_radius),
        RouteCurve(position=(ec - radius * s45, nc - radius * s45, elevation), curve_type="THRU"),
        RoutePoint(position=None, fillet_radius=fillet_radius),
    ]

    spec = HandrailSpec(
        name=name,
        position=position,
        top_rail_height=top_rail_height,
        mid_rail_height=mid_rail_height,
        post_spacing=post_spacing,
        tangent_offset=tangent_offset,
        show_kickplate=True,
        bend_radius=fillet_radius,
        start_direction=start_direction,
        end_direction=end_direction,
        path_items=path_items,
    )
    return HandrailBuilder().build(spec)


def build_polyline_handrail(
    points: Sequence[Point3D | Tuple[float, float]],
    *,
    name: Optional[str] = None,
    position: Point3D = (0.0, 0.0, 0.0),
    top_rail_height: float = 1250.0,
    mid_rail_height: float = 750.0,
    post_spacing: float = 1000.0,
    tangent_offset: float = 300.0,
    fillet_radius: float = 100.0,
    show_kickplate: bool = True,
    start_direction: Optional[str] = None,
    end_direction: Optional[str] = None,
) -> str:
    """
    Build a multi-segment polygonal/linear structural handrail through ordered 3D points.
    """
    if len(points) < 2:
        raise PMLValidationError(f"Polyline handrail requires at least 2 points, got {len(points)}")

    path_items: List[RoutePoint] = []
    for pt in points:
        if len(pt) == 2:
            pt_3d = (float(pt[0]), float(pt[1]), 0.0)
        else:
            pt_3d = (float(pt[0]), float(pt[1]), float(pt[2]))
        path_items.append(RoutePoint(position=pt_3d, fillet_radius=fillet_radius))

    spec = HandrailSpec(
        name=name,
        position=position,
        top_rail_height=top_rail_height,
        mid_rail_height=mid_rail_height,
        post_spacing=post_spacing,
        tangent_offset=tangent_offset,
        show_kickplate=show_kickplate,
        bend_radius=fillet_radius,
        start_direction=start_direction,
        end_direction=end_direction,
        path_items=path_items,
    )
    return HandrailBuilder().build(spec)


def build_rectangular_handrail(
    length_e: float,
    width_n: float,
    *,
    origin: Point3D = (0.0, 0.0, 0.0),
    elevation: float = 0.0,
    name: Optional[str] = None,
    top_rail_height: float = 1250.0,
    mid_rail_height: float = 750.0,
    post_spacing: float = 1000.0,
    tangent_offset: float = 300.0,
    fillet_radius: float = 100.0,
    show_kickplate: bool = True,
) -> str:
    """
    Build a closed 4-sided rectangular perimeter handrail (e.g. for platforms / mezzanines).
    """
    if length_e <= 0 or width_n <= 0:
        raise PMLValidationError(f"Rectangular handrail length and width must be positive: got {length_e}x{width_n}")

    points: List[Point3D] = [
        (0.0, 0.0, elevation),
        (length_e, 0.0, elevation),
        (length_e, width_n, elevation),
        (0.0, width_n, elevation),
        (0.0, 0.0, elevation),
    ]
    return build_polyline_handrail(
        points,
        name=name,
        position=origin,
        top_rail_height=top_rail_height,
        mid_rail_height=mid_rail_height,
        post_spacing=post_spacing,
        tangent_offset=tangent_offset,
        fillet_radius=fillet_radius,
        show_kickplate=show_kickplate,
    )


def build_arc_handrail(
    center_local: Tuple[float, float],
    radius: float,
    start_angle_deg: float,
    sweep_angle_deg: float,
    *,
    segments: int = 4,
    elevation: float = 0.0,
    name: Optional[str] = None,
    position: Point3D = (0.0, 0.0, 0.0),
    top_rail_height: float = 1250.0,
    mid_rail_height: float = 750.0,
    post_spacing: float = 1000.0,
    tangent_offset: float = 300.0,
    fillet_radius: float = 100.0,
    show_kickplate: bool = True,
) -> str:
    """
    Build an open or closed arc structural handrail with parameterized angle sweep.
    Uses intermediate CURVE elements with CURTYP THRU between vertices.
    """
    if radius <= 0:
        raise PMLValidationError(f"Arc handrail radius must be positive, got {radius}")
    if segments < 1:
        raise PMLValidationError(f"Arc handrail segments must be >= 1, got {segments}")

    ec, nc = center_local
    d_theta = math.radians(sweep_angle_deg) / segments
    theta_0 = math.radians(start_angle_deg)

    path_items: List[RoutePoint | RouteCurve] = []
    
    # First point
    x0 = ec + radius * math.cos(theta_0)
    y0 = nc + radius * math.sin(theta_0)
    path_items.append(RoutePoint(position=(x0, y0, elevation), fillet_radius=fillet_radius))

    for i in range(segments):
        theta_mid = theta_0 + (i + 0.5) * d_theta
        theta_end = theta_0 + (i + 1.0) * d_theta

        x_mid = ec + radius * math.cos(theta_mid)
        y_mid = nc + radius * math.sin(theta_mid)

        x_end = ec + radius * math.cos(theta_end)
        y_end = nc + radius * math.sin(theta_end)

        # Midpoint curve
        path_items.append(RouteCurve(position=(x_mid, y_mid, elevation), curve_type="THRU"))
        # End vertex
        path_items.append(RoutePoint(position=(x_end, y_end, elevation), fillet_radius=fillet_radius))

    spec = HandrailSpec(
        name=name,
        position=position,
        top_rail_height=top_rail_height,
        mid_rail_height=mid_rail_height,
        post_spacing=post_spacing,
        tangent_offset=tangent_offset,
        show_kickplate=show_kickplate,
        bend_radius=fillet_radius,
        path_items=path_items,
    )
    return HandrailBuilder().build(spec)


def build_tank_top_handrail(
    center_local: Tuple[float, float],
    radius: float,
    *,
    ladder_distance: Optional[float] = None,
    ladder_half_width: float = 240.0,
    ladder_azimuth_deg: float = 180.0,
    elevation: float = 0.0,
    name: Optional[str] = None,
    position: Point3D = (0.0, 0.0, 0.0),
    top_rail_height: float = 1100.0,
    mid_rail_height: float = 550.0,
    post_spacing: float = 1000.0,
    tangent_offset: float = 300.0,
    fillet_radius: float = 100.0,
    show_kickplate: bool = True,
) -> str:
    """
    Build a circular tank-top structural handrail connected directly and outward
    to the extended handrail stringers of a vertical access ladder.
    """
    if radius <= 0:
        raise PMLValidationError(f"Tank top handrail radius must be positive, got {radius}")

    ec, nc = center_local

    if ladder_distance is None:
        ladder_distance = radius + 300.0

    # Ladder stringer points (at azimuth 180 deg / West)
    p_stringer_south = (ec - ladder_distance, nc - ladder_half_width)
    p_stringer_north = (ec - ladder_distance, nc + ladder_half_width)

    # Rim intersection points on circle at y = +/- ladder_half_width
    x_rim_offset = -math.sqrt(max(0.0, radius**2 - ladder_half_width**2))
    p_rim_south = (ec + x_rim_offset, nc - ladder_half_width)
    p_rim_north = (ec + x_rim_offset, nc + ladder_half_width)

    theta_south_deg = math.degrees(math.atan2(-ladder_half_width, x_rim_offset))
    theta_north_deg = math.degrees(math.atan2(+ladder_half_width, x_rim_offset))

    sweep = 360.0 - 2.0 * abs(theta_north_deg - 180.0)
    d_theta = sweep / 4.0

    a1 = theta_south_deg + d_theta * 0.5
    a2 = theta_south_deg + d_theta
    a3 = theta_south_deg + d_theta * 1.5
    a4 = theta_south_deg + d_theta * 2.0
    a5 = theta_south_deg + d_theta * 2.5
    a6 = theta_south_deg + d_theta * 3.0
    a7 = theta_south_deg + d_theta * 3.5

    path_items: List[RoutePoint | RouteCurve] = [
        # 1. South ladder stringer connection point
        RoutePoint(position=(p_stringer_south[0], p_stringer_south[1], elevation), fillet_radius=fillet_radius),
        # 2. South rim transition corner
        RoutePoint(position=(p_rim_south[0], p_rim_south[1], elevation), fillet_radius=fillet_radius),
        # 3. Quadrant 4 curve
        RouteCurve(position=(ec + radius * math.cos(math.radians(a1)), nc + radius * math.sin(math.radians(a1)), elevation), curve_type="THRU"),
        RoutePoint(position=(ec + radius * math.cos(math.radians(a2)), nc + radius * math.sin(math.radians(a2)), elevation), fillet_radius=fillet_radius),
        # 4. East (0 deg) curve
        RouteCurve(position=(ec + radius * math.cos(math.radians(a3)), nc + radius * math.sin(math.radians(a3)), elevation), curve_type="THRU"),
        RoutePoint(position=(ec + radius, nc, elevation), fillet_radius=fillet_radius),
        # 5. Quadrant 1 curve
        RouteCurve(position=(ec + radius * math.cos(math.radians(a5)), nc + radius * math.sin(math.radians(a5)), elevation), curve_type="THRU"),
        RoutePoint(position=(ec + radius * math.cos(math.radians(a6)), nc + radius * math.sin(math.radians(a6)), elevation), fillet_radius=fillet_radius),
        # 6. North rim transition corner
        RouteCurve(position=(ec + radius * math.cos(math.radians(a7)), nc + radius * math.sin(math.radians(a7)), elevation), curve_type="THRU"),
        RoutePoint(position=(p_rim_north[0], p_rim_north[1], elevation), fillet_radius=fillet_radius),
        # 7. North ladder stringer connection point
        RoutePoint(position=(p_stringer_north[0], p_stringer_north[1], elevation), fillet_radius=fillet_radius),
    ]

    spec = HandrailSpec(
        name=name,
        position=position,
        top_rail_height=top_rail_height,
        mid_rail_height=mid_rail_height,
        post_spacing=post_spacing,
        tangent_offset=tangent_offset,
        show_kickplate=show_kickplate,
        bend_radius=fillet_radius,
        start_direction="E",
        end_direction="W",
        path_items=path_items,
    )
    return HandrailBuilder().build(spec)


__all__ = [
    "HandrailBuilder",
    "HandrailSpec",
    "RouteCurve",
    "RoutePoint",
    "build_arc_handrail",
    "build_circular_handrail",
    "build_polyline_handrail",
    "build_rectangular_handrail",
    "build_tank_top_handrail",
]

