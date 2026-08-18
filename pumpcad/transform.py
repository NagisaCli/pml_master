"""
The one place coordinates change frame.
=======================================

Three spaces, kept explicitly separate:

``CAD``
    Raw millimetres as exported from the drawing.  A large negative
    quadrant; the drawing's own frame.  Y is "up the paper", which is a
    *height* on an elevation and a *depth* on a plan.

``LOCAL``
    The pump's own frame.  Origin at the centre of the baseplate
    underside - the datum ``Pump_details.xlsx`` uses - with +X along the
    pump's long axis from driver to casing, +Y to the left of that, and
    +Z up.

``WORLD``
    E/N/U plant millimetres, as written into the PML.

The chain is always::

    CAD --lift--> LOCAL --orient--> --translate--> WORLD

``lift`` is where the plan/elevation distinction is resolved, and it is
the only place a CAD Y coordinate is allowed to become either a depth or
a height.  Orientation and translation never inspect the drawing again.

Angle convention: ``rotation_deg`` is counter-clockwise, in degrees, in
the plan (E/N) plane, measured from +E.  E3D's ORI keywords are emitted
from the resulting cardinal axis, never by scattering sign flips through
the geometry code.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

from .semantic import ViewType

__all__ = [
    "AXIS_VECTOR",
    "OPPOSITE_AXIS",
    "Placement",
    "axis_to_rotation",
    "rotation_to_axis",
    "cad_to_local",
    "local_to_world",
    "world_size",
    "LocalGeometry",
    "ori_clause",
    "extrusion_axes",
    "extrusion_plan_bounds",
    "CARDINAL_3D",
]

# Plan-plane unit vectors in (E, N).  Matches wsb.pump_builder._AXIS_VECTOR
# so the new pipeline places pumps exactly as JK_Pump_Build does.
AXIS_VECTOR = {
    "E": (1.0, 0.0),
    "W": (-1.0, 0.0),
    "N": (0.0, 1.0),
    "S": (0.0, -1.0),
}

OPPOSITE_AXIS = {"E": "W", "W": "E", "N": "S", "S": "N", "U": "D", "D": "U"}

_AXIS_ROTATION = {"E": 0.0, "N": 90.0, "W": 180.0, "S": 270.0}

# Full 3-D cardinal basis used by EXTRUSION emitters and their verifiers.
CARDINAL_3D = {
    "E": (1.0, 0.0, 0.0),
    "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0),
    "S": (0.0, -1.0, 0.0),
    "U": (0.0, 0.0, 1.0),
    "D": (0.0, 0.0, -1.0),
}


def axis_to_rotation(axis: str) -> float:
    """Cardinal axis -> counter-clockwise degrees from +E."""
    key = axis.upper()
    if key not in _AXIS_ROTATION:
        raise ValueError(f"not a plan-plane cardinal axis: {axis!r}")
    return _AXIS_ROTATION[key]


def rotation_to_axis(rotation_deg: float) -> str:
    """Counter-clockwise degrees from +E -> nearest cardinal axis."""
    angle = rotation_deg % 360.0
    best = min(_AXIS_ROTATION.items(), key=lambda kv: min(
        abs(angle - kv[1]), 360.0 - abs(angle - kv[1])
    ))
    return best[0]


@dataclass(frozen=True)
class Placement:
    """Everything needed to put a pump into the plant.

    ``origin`` is the contractual datum from ``Pump_details.xlsx``: the
    geometric centre of the **baseplate underside**.
    """

    origin: Tuple[float, float, float]
    layout_axis: str

    @property
    def rotation_deg(self) -> float:
        return axis_to_rotation(self.layout_axis)

    @property
    def forward(self) -> Tuple[float, float]:
        """Unit vector, driver -> casing, in the plan plane."""
        return AXIS_VECTOR[self.layout_axis.upper()]

    @property
    def left(self) -> Tuple[float, float]:
        """Unit vector 90 deg counter-clockwise from ``forward``."""
        fx, fy = self.forward
        return (-fy, fx)


@dataclass(frozen=True)
class LocalGeometry:
    """A component expressed in the pump's own frame.

    ``along`` runs driver -> casing, ``across`` is transverse, ``up`` is
    height above the baseplate underside.  Sizes are full extents.
    """

    along: float
    across: float
    up: float
    length: float
    width: float
    height: float

    @property
    def centre(self) -> Tuple[float, float, float]:
        return (self.along, self.across, self.up)


def cad_to_local(
    bounds: Tuple[float, float, float, float],
    *,
    outline: Tuple[float, float, float, float],
    view: ViewType,
    long_axis: str,
    height: Optional[float] = None,
    base_elevation: float = 0.0,
) -> LocalGeometry:
    """Lift a CAD-space box into the pump's local frame.

    This is the only function that interprets what a CAD Y coordinate
    *means*, and it does so from ``view``:

    * ``PLAN`` - the drawing is the footprint.  CAD X/Y map to the local
      along/across axes, and ``height`` must be supplied by engineering
      reasoning because the drawing says nothing about it.
    * ``ELEVATION`` - the drawing is a side view.  The CAD axis along the
      outline's long direction is a **height**; the other is a diameter,
      which sets both local along and across for a body of revolution.

    Never call this with ``ViewType.UNKNOWN``; a pump with no view has no
    CAD geometry to lift.
    """
    ox0, oy0, ox1, oy1 = outline
    bx0, by0, bx1, by1 = bounds
    span_x = bx1 - bx0
    span_y = by1 - by0

    if view is ViewType.PLAN:
        # Footprint drawing: X/Y are both plan dimensions.
        plate_cx = (ox0 + ox1) / 2.0
        plate_cy = (oy0 + oy1) / 2.0
        cx = (bx0 + bx1) / 2.0
        cy = (by0 + by1) / 2.0
        if long_axis == "x":
            along, across = cx - plate_cx, cy - plate_cy
            length, width = span_x, span_y
        else:
            along, across = cy - plate_cy, -(cx - plate_cx)
            length, width = span_y, span_x
        tall = height if height is not None else min(length, width)
        return LocalGeometry(
            along=along,
            across=across,
            up=base_elevation + tall / 2.0,
            length=length,
            width=width,
            height=tall,
        )

    if view is ViewType.ELEVATION:
        # Side view: the outline's long direction is the vertical one.
        vertical_is_y = (oy1 - oy0) >= (ox1 - ox0)
        if vertical_is_y:
            elevation_span = span_y
            diameter = span_x
            bottom = by0 - oy0
            lateral = ((bx0 + bx1) / 2.0) - ((ox0 + ox1) / 2.0)
        else:
            elevation_span = span_x
            diameter = span_y
            bottom = bx0 - ox0
            lateral = ((by0 + by1) / 2.0) - ((oy0 + oy1) / 2.0)
        return LocalGeometry(
            along=lateral,
            across=0.0,
            up=base_elevation + bottom + elevation_span / 2.0,
            length=diameter,
            width=diameter,
            height=elevation_span,
        )

    raise ValueError("cannot lift geometry for an unknown view type")


def local_to_world(
    local: Tuple[float, float, float], placement: Placement
) -> Tuple[float, float, float]:
    """Rotate by the pump's orientation, then translate to its datum.

    ``local`` is ``(along, across, up)``.  Rotation happens in the plan
    plane only; ``up`` is never rotated.
    """
    along, across, up = local
    fx, fy = placement.forward
    lx, ly = placement.left
    east = placement.origin[0] + along * fx + across * lx
    north = placement.origin[1] + along * fy + across * ly
    return (east, north, placement.origin[2] + up)


def world_size(
    length: float, width: float, placement: Placement
) -> Tuple[float, float]:
    """Map a local (length, width) onto world (XLEN, YLEN).

    Matches ``PumpSpec.world_baseplate_dimensions``: an E/W pump keeps
    length on X, an N/S pump swaps them.  Only right-angle orientations
    occur in this data set, so no shear can arise.
    """
    if placement.layout_axis.upper() in ("E", "W"):
        return (length, width)
    return (width, length)


def ori_clause(axis: str) -> str:
    """E3D ORI clause aiming a primitive's Z along ``axis``.

    Written once here so no other module hand-rolls an ORI string.
    """
    key = axis.upper()
    if key == "U":
        return "ORI Z IS U AND Y IS N"
    if key == "D":
        return "ORI Z IS D AND Y IS N"
    if key in ("E", "W", "N", "S"):
        return f"ORI Z IS {key} AND Y IS U"
    raise ValueError(f"unsupported orientation axis: {axis!r}")


def extrusion_axes(orientation: str) -> Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
    Tuple[float, float, float],
]:
    """Local X/Y/Z basis vectors for an ``ORI Y IS .. AND Z IS ..`` clause.

    EXTRUSION's LOOP lives in its local XY plane and sweeps HEIG along local
    +Z, so callers need all three axes to project a solid back onto E/N.
    """
    parts = " ".join(orientation.upper().split()).split()
    if (
        len(parts) == 7
        and parts[0] == "Y"
        and parts[1] == "IS"
        and parts[3] == "AND"
        and parts[4] == "Z"
        and parts[5] == "IS"
    ):
        y_axis, z_axis = parts[2], parts[6]
    else:
        raise ValueError(f"malformed EXTRUSION orientation: {orientation!r}")
    if y_axis not in CARDINAL_3D or z_axis not in CARDINAL_3D:
        raise ValueError(f"non-cardinal EXTRUSION orientation: {orientation!r}")
    y_vec = CARDINAL_3D[y_axis]
    z_vec = CARDINAL_3D[z_axis]
    x_vec = (
        y_vec[1] * z_vec[2] - y_vec[2] * z_vec[1],
        y_vec[2] * z_vec[0] - y_vec[0] * z_vec[2],
        y_vec[0] * z_vec[1] - y_vec[1] * z_vec[0],
    )
    if all(abs(v) < 1e-9 for v in x_vec):
        raise ValueError(f"degenerate EXTRUSION orientation: {orientation!r}")
    return x_vec, y_vec, z_vec


def extrusion_plan_bounds(
    position: Tuple[float, float, float],
    orientation: str,
    height: float,
    vertices: Sequence[Tuple[float, float]],
) -> Tuple[float, float, float, float]:
    """E/N bounding box of an EXTRUSION's plan projection."""
    x_axis, y_axis, z_axis = extrusion_axes(orientation)
    east_points: List[float] = []
    north_points: List[float] = []
    for x, y in vertices:
        for depth in (0.0, height):
            east = position[0] + x * x_axis[0] + y * y_axis[0] + depth * z_axis[0]
            north = position[1] + x * x_axis[1] + y * y_axis[1] + depth * z_axis[1]
            east_points.append(east)
            north_points.append(north)
    return (
        min(east_points),
        min(north_points),
        max(east_points),
        max(north_points),
    )
