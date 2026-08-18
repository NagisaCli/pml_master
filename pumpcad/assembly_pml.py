"""
PML emission from the whole-assembly decomposition.
===================================================

Earlier emitters approximated every part with a BOX or a stack of
cylinders.  This one picks the primitive that matches what the drawing
actually shows:

``CYLI``
    a part whose measured silhouette is a constant radius.

``CONE``
    a part that tapers monotonically - a reducer, a volute closing onto
    its cover, a motor's fan cowl.

``EXTRUSION`` (LOOP / VERTEX)
    any other revolved silhouette.  The measured profile becomes the
    LOOP, so every step and flare survives instead of being averaged
    into one diameter.  Built through :mod:`wsb.extrusion_builder`,
    whose POS datum is verified against a native E3D listing.

``CTORUS``
    a bend: an elbow's centreline arc, and fillets between steps.

Parts keep their semantic identity through the SUBE hierarchy, so the
model reads as driver / shaft / wet end / pipework rather than as a bag
of numbered solids.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from wsb.extrusion_builder import build_extrusion
from wsb.pml_builder import PMLValidationError

from .assembly_model import AssemblyModel, Region
from .transform import Placement, local_to_world, ori_clause

__all__ = ["PartSolid", "emit_assembly", "render_assembly_pml", "name_parts"]

#: A silhouette whose radius varies by less than this fraction of its own
#: mean is treated as a plain cylinder.
CYLINDER_TOL = 0.04

#: Below this fraction of monotone change, a taper is really a cone.
CONE_TOL = 0.06


@dataclass
class PartSolid:
    """One emitted solid, with the text already rendered."""

    name: str
    kind: str
    text: str
    handles: List[str] = field(default_factory=list)


def _classify_profile(profile: Sequence[Tuple[float, float]]) -> str:
    """What primitive does this silhouette want to be?"""
    radii = [r for _, r in profile if r > 1e-9]
    if len(radii) < 2:
        return "skip"
    lo, hi = min(radii), max(radii)
    mean = sum(radii) / len(radii)
    if mean <= 1e-9:
        return "skip"
    if (hi - lo) / mean <= CYLINDER_TOL:
        return "cylinder"

    # Monotone within tolerance -> a cone.
    rising = falling = True
    for a, b in zip(radii, radii[1:]):
        if b < a - mean * CONE_TOL:
            rising = False
        if b > a + mean * CONE_TOL:
            falling = False
    if rising or falling:
        return "cone"
    return "extrusion"


def _axis_for(region: Region, placement: Placement, elevation: bool) -> str:
    """Which world axis the part's own axis points along.

    On an **elevation** the drawing plane is vertical: a part whose axis
    runs up the drawing stands up in the world, and one running across is
    horizontal, along the machine.

    On a **plan** the drawing plane is horizontal, so neither drawing
    direction is "up".  A part's axis lies in the plan plane: along the
    machine axis, or across it.  Emitting these as ``Z IS U`` stood the
    driver on its end, which is the error that made the earlier models
    look like drums.
    """
    if elevation:
        return "U" if region.axis == "v" else placement.layout_axis

    from .transform import AXIS_VECTOR, OPPOSITE_AXIS

    layout = placement.layout_axis
    if region.axis == "h":
        # Runs along the drawing's X, which is the machine axis in plan.
        return layout
    # Runs across the machine: the transverse horizontal direction.
    return {"E": "N", "W": "N", "N": "E", "S": "E"}[layout]


def _fmt(value: float) -> str:
    return f"{value:.1f}"


def emit_assembly(
    assembly: AssemblyModel,
    placement: Placement,
    *,
    prefix: str,
    elevation: bool,
    base_elevation: float,
) -> Tuple[List[PartSolid], List[str]]:
    """Render every part of an assembly as PML.

    Returns the solids and any notes worth carrying into the audit.
    """
    solids: List[PartSolid] = []
    notes: List[str] = []
    if not assembly.regions or assembly.outline is None:
        return solids, notes

    ox0, oy0, ox1, oy1 = assembly.outline
    plate_cx = (ox0 + ox1) / 2.0
    plate_cy = (oy0 + oy1) / 2.0

    # The machine axis, in drawing coordinates.  Taken from the largest
    # body rather than from the dimension box, because the dimension box
    # is an annotation and need not be centred on the machine.
    biggest = max(assembly.regions, key=lambda r: r.area)
    if elevation:
        axis_line = (biggest.bounds[0] + biggest.bounds[2]) / 2.0
    else:
        axis_line = (biggest.bounds[1] + biggest.bounds[3]) / 2.0

    # On a plan view the drawing says nothing about height, but the parts
    # are not free to float: a horizontal machine hangs its rotating parts
    # on one shaft centreline.  That elevation is set by the widest body,
    # which is the driver sitting on its own feet.
    centreline = base_elevation
    if not elevation:
        widths = [
            min(r.size) for r in assembly.regions if min(r.size) > 1.0
        ]
        if widths:
            driver_width = max(widths)
            centreline = base_elevation + max(driver_width * 0.16, 40.0) + driver_width / 2.0

    for index, region in enumerate(assembly.regions, start=1):
        shape = _classify_profile(region.profile)
        if shape == "skip":
            continue

        x0, y0, x1, y1 = region.bounds
        vertical = region.axis == "v"
        length = (y1 - y0) if vertical else (x1 - x0)
        if length <= 1e-6:
            continue

        # Where the part sits, in the pump's own frame.
        #
        # A machine is built about an axis, and a single view shows that
        # axis edge-on.  A part's offset *across* the axis in the drawing
        # is therefore its radius, not a position - reading it as a
        # position is what scattered the parts through space.  Only the
        # position *along* the axis is real.
        # A part is on the axis when it straddles it; one drawn wholly to
        # one side (a terminal box, a bracket, an elbow) is genuinely
        # offset and keeps its offset.
        if elevation:
            straddles = x0 < axis_line < x1
            offset = 0.0 if straddles else ((x0 + x1) / 2.0 - axis_line)
            along = offset
            across = 0.0
            up = base_elevation + ((y0 - oy0) if vertical else ((y0 + y1) / 2.0 - oy0))
        else:
            # Plan view.  A part straddling the shaft line is a rotating
            # body on the centreline; one drawn to the side is a fitting
            # standing on the plate, and its drawn offset is a real
            # transverse position.  Treating every part as on-axis left
            # the whole machine flat at one elevation.
            straddles = y0 < axis_line < y1
            along = ((x0 + x1) / 2.0) - plate_cx
            if straddles:
                across = 0.0
                up = centreline
            else:
                across = (y0 + y1) / 2.0 - axis_line
                # A fitting sits above the plate by its own half-depth.
                up = base_elevation + min(x1 - x0, y1 - y0) / 2.0

        axis = _axis_for(region, placement, elevation)
        radii = [r for _, r in region.profile if r > 1e-9]
        mean_r = sum(radii) / len(radii)

        name = f"/{prefix}_PART_{index:02d}"
        label = f"-- {region.detail}"

        if shape == "cylinder":
            # A vertical part is positioned by its centre, so lift it half
            # its own length; a horizontal one already sits on its axis.
            centre_up = up + (length / 2.0 if axis in ("U", "D") else 0.0)
            east, north, elev = local_to_world((along, across, centre_up), placement)
            text = "\n".join(
                (
                    label,
                    "NEW CYLI",
                    f"DIAM {_fmt(mean_r * 2.0)}",
                    f"HEIG {_fmt(length)}",
                    ori_clause(axis),
                    f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(elev)}",
                )
            )
            solids.append(PartSolid(name, "CYLI", text, list(region.handles)))
            continue

        if shape == "cone":
            # A vertical part is positioned by its centre, so lift it half
            # its own length; a horizontal one already sits on its axis.
            centre_up = up + (length / 2.0 if axis in ("U", "D") else 0.0)
            east, north, elev = local_to_world((along, across, centre_up), placement)
            dbot = radii[0] * 2.0
            dtop = radii[-1] * 2.0
            text = "\n".join(
                (
                    label,
                    "NEW CONE",
                    f"DBOT {_fmt(dbot)}",
                    f"DTOP {_fmt(dtop)}",
                    f"HEIG {_fmt(length)}",
                    ori_clause(axis),
                    f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(elev)}",
                )
            )
            solids.append(PartSolid(name, "CONE", text, list(region.handles)))
            continue

        # --- EXTRUSION: the measured silhouette becomes the LOOP ---
        # The profile is revolved conceptually but emitted as a swept
        # half-section closed back on the axis, which keeps every step.
        vertices: List[Tuple[float, float]] = []
        for position, radius in region.profile:
            if radius <= 1e-9:
                continue
            vertices.append((position, radius))
        if len(vertices) < 2:
            continue
        # Close the loop down the axis and back, giving a valid planar area.
        loop = vertices + [(vertices[-1][0], 0.0), (vertices[0][0], 0.0)]
        if len(loop) < 3:
            continue

        east, north, elev = local_to_world((along, across, up), placement)
        try:
            text = build_extrusion(
                position=(east, north, elev),
                orientation=(
                    "Y IS U AND Z IS N" if axis in ("U", "D") else "Y IS U AND Z IS E"
                ),
                height=max(mean_r * 2.0, 1.0),
                vertices=loop,
            )
        except PMLValidationError as exc:
            notes.append(f"part {index}: extrusion rejected ({exc}); part skipped")
            continue
        solids.append(
            PartSolid(name, "EXTRUSION", label + "\n" + text.rstrip(), list(region.handles))
        )

    notes.append(
        f"{len(solids)} solid(s) emitted from {len(assembly.regions)} drawn region(s)"
    )
    return solids, notes


def name_parts(
    assembly: AssemblyModel,
    *,
    elevation: bool,
) -> Dict[int, str]:
    """Give each region a functional name from where it sits.

    Position along the machine axis carries the meaning: on a vertical
    pump the driver is at the top and the wet end at the bottom; on a
    horizontal one the driver is at one end and the casing at the other.
    Naming from the drawing keeps the model readable without inventing a
    classification the evidence does not support.
    """
    names: Dict[int, str] = {}
    if not assembly.regions or assembly.outline is None:
        return names

    ox0, oy0, ox1, oy1 = assembly.outline
    axis_lo, axis_hi = (oy0, oy1) if elevation else (ox0, ox1)
    span = axis_hi - axis_lo or 1.0

    # The largest region is the machine's main body; everything is placed
    # relative to it rather than to an assumed layout.
    widest = max(assembly.regions, key=lambda r: r.area)

    for index, region in enumerate(assembly.regions, start=1):
        x0, y0, x1, y1 = region.bounds
        centre = ((y0 + y1) / 2.0) if elevation else ((x0 + x1) / 2.0)
        fraction = (centre - axis_lo) / span
        small = region.area < widest.area * 0.06

        if small:
            label = "FITTING"
        elif elevation:
            if fraction > 0.72:
                label = "DRIVER"
            elif fraction > 0.45:
                label = "LANTERN"
            elif fraction > 0.22:
                label = "COLUMN"
            else:
                label = "WETEND"
        else:
            if fraction < 0.38:
                label = "DRIVER"
            elif fraction < 0.62:
                label = "COUPLING"
            else:
                label = "WETEND"
        names[index] = label
    return names


def render_assembly_pml(
    tag: str,
    name: str,
    solids: Sequence[PartSolid],
    labels: Dict[int, str],
    *,
    generated: str,
    header_notes: Sequence[str] = (),
) -> str:
    """Render a whole assembly as one PML macro.

    Parts are grouped into SUBEs by function so the E3D tree reads as
    driver / coupling / wet end / fittings rather than as a flat list.
    """
    safe = tag.replace("-", "_")
    lines: List[str] = []
    add = lines.append

    add("-- " + "=" * 68)
    add(f"-- {tag} - {name}")
    add("-- " + "=" * 68)
    add("-- Project: JK_Pump_Build (pumpcad whole-assembly reconstruction)")
    add("-- Units: mm")
    add("-- Frame: E = East, N = North, U = Up")
    add("-- Datum: metadata coordinate = geometric centre of baseplate underside")
    add("-- Geometry: every part is measured from its own drawn silhouette;")
    add("--   CYLI where the radius is constant, CONE where it tapers,")
    add("--   EXTRUSION (LOOP/VERTEX) where the profile steps.")
    add(f"-- Parts: {len(solids)}")
    add(f"-- Generated: {generated}")
    for note in header_notes:
        add(f"-- Note: {note}")
    add("-- Execution: select a writable ZONE, then $M <this file>")
    add("")
    add(f"NEW EQUI /{safe}")
    add("POS E 0.0 N 0.0 U 0.0")
    add("")

    grouped: Dict[str, List[Tuple[int, PartSolid]]] = {}
    for index, solid in enumerate(solids, start=1):
        grouped.setdefault(labels.get(index, "FITTING"), []).append((index, solid))

    for group in ("DRIVER", "LANTERN", "COUPLING", "COLUMN", "WETEND", "FITTING"):
        members = grouped.get(group)
        if not members:
            continue
        add(f"NEW SUBE /{safe}_{group}")
        add(f"-- {len(members)} part(s) reconstructed from the drawing")
        for index, solid in members:
            if solid.handles:
                shown = ",".join(solid.handles[:6])
                more = "" if len(solid.handles) <= 6 else " ..."
                add(f"-- CAD handles: {shown}{more}")
            add(solid.text)
            add("")
    return "\n".join(lines).rstrip() + "\n"
