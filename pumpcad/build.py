"""
Semantic model -> 3-D solids -> E3D PML.
========================================

Z geometry is the one place engineering reasoning is allowed to supply
what the drawing does not contain, and it is bounded by rule: a solid's
XY extents always come from the CAD evidence, and only its height may be
reasoned about.  For elevations the reverse holds - the height is
measured and the diameter is the evidence - so in both cases every
number written here traces to something in the source file.

PML conventions (hierarchy, ORI-before-POS, CATR binding, ``--``
comments, absolute ``POS E/N/U``) follow JK_Pump_Build exactly, so the
output drops into the same workflow.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from wsb.pml_builder import (
    NOZZLE_BORE_COMPONENTS,
    NOZZLE_MAX_CATALOGUE_DN,
    nozzle_component_path,
)

from .semantic import (
    Component,
    ComponentKind,
    Confidence,
    PumpSemanticModel,
    ViewType,
)
from .source import CLIENT_LONGITUDINAL_AXIS, PumpRecord
from .transform import (
    AXIS_VECTOR,
    CARDINAL_3D,
    OPPOSITE_AXIS,
    Placement,
    cad_to_local,
    local_to_world,
    ori_clause,
    world_size,
)

__all__ = [
    "BASEPLATE_THICKNESS",
    "Solid",
    "PumpBuild",
    "build_pump",
    "render_pml",
    "snap_to_catalogue_dn",
]

#: Baseplate thickness (mm).  Matches the JK_Pump_Build convention, where
#: the Excel coordinate is the underside and the plate top is +thickness.
BASEPLATE_THICKNESS = 50.0

#: Catalogue nozzle projection from the connection point to the flange
#: face, kept in one place because the emitted HEIG must equal the
#: face standoff or the nozzle reads as a stub.
NOZZLE_PROJECTION = 150.0

#: Height a plan-view body is given when the drawing cannot say.  Applied
#: as a fraction of the body's own footprint so a large motor is taller
#: than a small one, rather than every pump sharing one canned height.
_PLAN_HEIGHT_FACTOR: Dict[ComponentKind, float] = {
    ComponentKind.MOTOR: 1.05,
    ComponentKind.PUMP_CASING: 1.10,
    ComponentKind.COUPLING: 0.85,
    ComponentKind.COUPLING_GUARD: 0.95,
    ComponentKind.BEARING_HOUSING: 0.90,
    ComponentKind.AUXILIARY: 0.70,
}


def snap_to_catalogue_dn(nominal_mm: float) -> Tuple[int, str]:
    """Snap a metadata bore to the nearest available catalogue DN.

    The workbook carries measured bores (539, 216, 151 mm ...) which are
    not catalogue sizes.  A nozzle must bind to a real SPCO, so the bore
    is snapped to the nearest one the catalogue actually carries and the
    substitution is reported, never applied silently.
    """
    if nominal_mm <= 0:
        raise ValueError(f"nozzle bore must be positive, got {nominal_mm}")
    sizes = sorted(NOZZLE_BORE_COMPONENTS)
    best = min(sizes, key=lambda dn: abs(dn - nominal_mm))
    if abs(best - nominal_mm) <= 0.5:
        return best, ""
    note = (
        f"metadata bore {nominal_mm:.0f} mm snapped to catalogue DN{best} "
        f"(nearest available in {NOZZLE_BORE_COMPONENTS[best]!r}; "
        f"catalogue max is DN{NOZZLE_MAX_CATALOGUE_DN})"
    )
    return best, note


@dataclass
class Solid:
    """One E3D primitive, already in world coordinates."""

    primitive: str  # "BOX", "CYLI" or "CONE"
    label: str
    position: Tuple[float, float, float]
    # BOX
    xlen: float = 0.0
    ylen: float = 0.0
    zlen: float = 0.0
    # CYLI / CONE
    diameter: float = 0.0
    height: float = 0.0
    axis: str = "U"
    # CONE only: DTOP/DBOT, as the reference pump uses for tapers.
    dtop: float = 0.0
    dbot: float = 0.0
    source_handles: List[str] = field(default_factory=list)
    # EXTRUSION only: local LOOP vertices and the full ORI clause.
    vertices: List[Tuple[float, float]] = field(default_factory=list)
    orientation: str = ""
    # SUBE group the solid belongs to (one SUBE per major assembly, not one
    # per primitive).
    group: str = "BODY"

    def top_view_bounds(self) -> Tuple[float, float, float, float]:
        """Footprint this solid projects onto the E/N plane."""
        east, north, _ = self.position
        if self.primitive == "EXTRUSION":
            from .transform import extrusion_plan_bounds

            return extrusion_plan_bounds(
                self.position, self.orientation, self.height, self.vertices
            )
        if self.primitive == "BOX":
            half_x, half_y = self.xlen / 2.0, self.ylen / 2.0
        else:
            width = (
                max(self.dtop, self.dbot)
                if self.primitive == "CONE"
                else self.diameter
            )
            if self.axis in ("U", "D"):
                half_x = half_y = width / 2.0
            elif self.axis in ("E", "W"):
                half_x, half_y = self.height / 2.0, width / 2.0
            else:
                half_x, half_y = width / 2.0, self.height / 2.0
        return (east - half_x, north - half_y, east + half_x, north + half_y)


@dataclass
class Nozzle:
    """A catalogue-bound nozzle."""

    label: str
    role: str  # "SUCTION" or "DISCHARGE"
    dn: int
    catref: str
    face: Tuple[float, float, float]
    axis: str
    height: float
    note: str = ""
    group: str = ""


@dataclass
class PumpBuild:
    """The buildable result for one pump."""

    tag: str
    name: str
    safe_tag: str
    placement: Placement
    view: ViewType
    solids: List[Solid] = field(default_factory=list)
    nozzles: List[Nozzle] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def top_view_bounds(self) -> Optional[Tuple[float, float, float, float]]:
        boxes = [s.top_view_bounds() for s in self.solids]
        if not boxes:
            return None
        return (
            min(b[0] for b in boxes),
            min(b[1] for b in boxes),
            max(b[2] for b in boxes),
            max(b[3] for b in boxes),
        )


def _layout_axis(record: PumpRecord) -> str:
    """Driver -> casing direction, from the contractual suction direction.

    Mirrors ``PumpSpec.layout_axis``.  A vertical pump's suction is still
    a plan-plane direction; only the discharge points up.  The two special
    East-West MC pumps override the suction-derived axis per client
    confirmation (driver East, casing West).
    """
    override = CLIENT_LONGITUDINAL_AXIS.get(record.tag)
    if override:
        return override.upper()
    axis = (record.inlet_orientation or "E").upper()
    if axis not in ("E", "W", "N", "S"):
        return "E"
    return axis


def _baseplate_solid(
    record: PumpRecord, model: PumpSemanticModel, placement: Placement
) -> Tuple[Solid, List[str]]:
    """The baseplate, sized from metadata and checked against the CAD.

    ``Pump_details.xlsx`` is authoritative for baseplate size (section
    18), so the plate is always built from metadata.  The CAD outline is
    compared against it and any disagreement is recorded rather than
    being allowed to distort the plate.
    """
    notes: List[str] = []
    length, width = record.length_mm, record.width_mm

    outline = model.outline_size
    if outline is not None and model.view is ViewType.PLAN:
        long_cad, short_cad = max(outline), min(outline)
        long_meta, short_meta = max(length, width), min(length, width)
        delta = abs(long_cad - long_meta) + abs(short_cad - short_meta)
        if delta > 25.0:
            notes.append(
                f"baseplate: CAD outline {long_cad:.0f}x{short_cad:.0f} differs "
                f"from metadata {long_meta:.0f}x{short_meta:.0f} by {delta:.0f} mm; "
                f"metadata retained as the authoritative size"
            )
    elif model.view is ViewType.ELEVATION and outline is not None:
        # On an elevation the metadata pair describes the *drawn* outline, so
        # one of its two numbers is a height, not a plan dimension.  Using it
        # as YLEN would stand a 1720 mm tall pump on a 1720 mm deep plate.
        # The plan extent is the drawing's horizontal span; the depth is not
        # dimensioned at all, so the footprint is taken as square on it.
        plan_span = min(outline)
        length = width = plan_span
        notes.append(
            f"baseplate: drawing is an elevation, so the metadata pair "
            f"{max(record.length_mm, record.width_mm):.0f}x"
            f"{min(record.length_mm, record.width_mm):.0f} is an outline in "
            f"which the larger figure is a height, not a plan depth; the plate "
            f"is built {plan_span:.0f}x{plan_span:.0f} from the drawn "
            f"horizontal span, and the height is carried by the bodies"
        )

    xlen, ylen = world_size(length, width, placement)
    east, north, up = placement.origin
    return (
        Solid(
            primitive="BOX",
            label="contractual rectangular baseplate; POS is its geometric "
            "centre and the metadata coordinate is its underside centre",
            position=(east, north, up + BASEPLATE_THICKNESS / 2.0),
            xlen=xlen,
            ylen=ylen,
            zlen=BASEPLATE_THICKNESS,
        ),
        notes,
    )


def _shaft_elevation(model: PumpSemanticModel) -> float:
    """Elevation of the machine centreline above the baseplate underside.

    A horizontal pump has exactly one shaft axis, and every rotating part
    - driver, coupling, bearing housing, impeller - turns about it.  The
    plan view cannot show that height, so it is derived: the driver is the
    tallest body, it is a cylinder lying on its side, and it clears the
    plate on its own feet.  That fixes the centreline at roughly half the
    driver's drawn width above the plate top.

    Getting this wrong is what makes a pump look like a pile of boxes on
    the floor rather than a machine.
    """
    widths = [
        min(component.size)
        for component in model.components
        if component.kind
        in (ComponentKind.MOTOR, ComponentKind.BEARING_HOUSING)
        and min(component.size) > 1.0
    ]
    if not widths:
        return BASEPLATE_THICKNESS + 250.0
    driver_width = max(widths)
    # Foot height keeps the driver body off the plate; a shallow fraction
    # of its own diameter is the usual proportion on a skid-mounted set.
    foot = max(driver_width * 0.16, 40.0)
    return BASEPLATE_THICKNESS + foot + driver_width / 2.0


def _plan_body_solids(
    model: PumpSemanticModel, placement: Placement, centreline: float
) -> List[Solid]:
    """Build a horizontal pump from a true plan view.

    The XY footprint of every part is taken verbatim from its CAD contour.
    What the plan cannot show - the third dimension - is resolved by one
    engineering fact rather than per-part guesswork: **all rotating parts
    share a single shaft centreline**.  Bodies are therefore hung on that
    centreline as cylinders lying along the machine axis, and only the
    parts that genuinely sit on the plate (feet, pedestals, baseplate
    fittings) are grounded.
    """
    solids: List[Solid] = []
    assert model.outline is not None

    plate_top = BASEPLATE_THICKNESS
    axis = placement.layout_axis

    for component in model.components:
        if component.kind is ComponentKind.BASEPLATE:
            continue
        label = (
            f"{component.kind.value} [{component.confidence.value}]: "
            f"{component.reason}"
        )
        handles = list(component.handles)
        local = cad_to_local(
            component.bounds,
            outline=model.outline,
            view=ViewType.PLAN,
            long_axis=model.long_axis,
            height=0.0,
            base_elevation=0.0,
        )
        # ``length`` runs along the machine axis, ``width`` across it.
        along_extent = local.length
        across_extent = local.width

        # --- shaft / coupling spool: a cylinder on the centreline ---
        if component.round_axis in ("x", "y") and component.radius:
            solids.extend(
                _shaft_train(
                    component,
                    local,
                    placement,
                    centreline,
                    label,
                    handles,
                )
            )
            continue

        # --- volute: circle, polygon or merged band, all handled inside ---
        if component.kind is ComponentKind.PUMP_CASING:
            solids.extend(
                _volute(
                    component,
                    local,
                    placement,
                    centreline,
                    plate_top,
                    label,
                    handles,
                    model,
                )
            )
            continue

        # --- driver and other bodies straddling the centreline ---
        if component.kind is ComponentKind.MOTOR:
            solids.extend(
                _driver(
                    local, placement, centreline, plate_top, label, handles, axis
                )
            )
            continue

        if component.kind is ComponentKind.BEARING_HOUSING:
            # A bearing/adapter housing is a cylinder on the shaft axis,
            # carried by a pedestal down to the plate.
            solids.append(
                Solid(
                    primitive="CYLI",
                    label=label,
                    position=local_to_world(
                        (local.along, local.across, centreline), placement
                    ),
                    diameter=across_extent,
                    height=along_extent,
                    axis=axis,
                    source_handles=handles,
                )
            )
            solids.extend(
                _support_assembly(
                    local.along,
                    local.across,
                    along_extent * 0.80,
                    across_extent * 0.62,
                    plate_top,
                    max(centreline - across_extent * 0.45, plate_top + 25.0),
                    placement,
                    "Bearing housing pedestal",
                )
            )
            continue

        if component.kind is ComponentKind.COUPLING_GUARD:
            # The guard is a box enclosing the coupling, sitting on the
            # centreline with its own end plates, rather than on the floor.
            guard_w = across_extent
            xlen, ylen = world_size(along_extent, across_extent, placement)
            solids.append(
                Solid(
                    primitive="BOX",
                    label=label,
                    position=local_to_world(
                        (local.along, local.across, centreline), placement
                    ),
                    xlen=xlen,
                    ylen=ylen,
                    zlen=guard_w,
                    source_handles=handles,
                )
            )
            end_d = across_extent * 0.92
            end_t = max(across_extent * 0.08, 6.0)
            for sign in (-1.0, 1.0):
                solids.append(
                    Solid(
                        primitive="CYLI",
                        label="Coupling guard end plate",
                        position=local_to_world(
                            (
                                local.along
                                + sign * (along_extent / 2.0 - end_t / 2.0),
                                local.across,
                                centreline,
                            ),
                            placement,
                        ),
                        diameter=end_d,
                        height=end_t,
                        axis=axis,
                    )
                )
            continue

        # --- everything else: a fitting standing on the plate ---
        height = max(min(along_extent, across_extent) * 0.8, 60.0)
        if component.points and len(component.points) >= 3:
            try:
                solids.append(
                    _polygon_body(
                        component.points,
                        model,
                        placement,
                        plate_top,
                        height,
                        label,
                        handles,
                    )
                )
                continue
            except ValueError:
                pass
        xlen, ylen = world_size(along_extent, across_extent, placement)
        solids.append(
            Solid(
                primitive="BOX",
                label=label,
                position=local_to_world(
                    (local.along, local.across, plate_top + height / 2.0), placement
                ),
                xlen=xlen,
                ylen=ylen,
                zlen=height,
                source_handles=handles,
            )
        )
    return solids


def _shaft_train(
    component,
    local,
    placement: Placement,
    centreline: float,
    label: str,
    handles: List[str],
) -> List[Solid]:
    """The shaft and its two coupling hubs.

    A coupling is not one cylinder: it is a shaft with a hub at each end,
    which is what makes the gap between driver and pump read correctly.
    """
    axis = placement.layout_axis
    shaft_d = (component.radius or 30.0) * 2.0
    span = max(local.length, local.width)
    solids = [
        Solid(
            primitive="CYLI",
            label=label,
            position=local_to_world(
                (local.along, local.across, centreline), placement
            ),
            diameter=shaft_d,
            height=span,
            axis=axis,
            source_handles=handles,
        )
    ]
    # Hubs at each end, sized off the shaft rather than invented.
    hub_d = shaft_d * 1.75
    hub_len = span * 0.22
    for sign in (-1.0, 1.0):
        offset = sign * (span / 2.0 - hub_len / 2.0)
        solids.append(
            Solid(
                primitive="CYLI",
                label=f"Coupling hub (d={hub_d:.0f}) on the shaft centreline",
                position=local_to_world(
                    (local.along + offset, local.across, centreline), placement
                ),
                diameter=hub_d,
                height=hub_len,
                axis=axis,
            )
        )
    return solids


def _volute(
    component,
    local,
    placement: Placement,
    centreline: float,
    plate_top: float,
    label: str,
    handles: List[str],
    model: PumpSemanticModel,
) -> List[Solid]:
    """The wet end: volute barrel, suction cover, split flange and its foot.

    The plan drawing gives the volute's true silhouette, and that silhouette
    is reproduced with the primitive it actually deserves:

    * a closed polygon outline (an octagonal flange, a rounded arc body)
      becomes a vertical EXTRUSION of that exact polygon;
    * a concentric disc stack becomes a vertical cylinder, whose plan is the
      drawn circle exactly;
    * a merged open band falls back to a barrel cylinder on the shaft axis
      whose plan equals the drawn rectangle.
    """
    axis = placement.layout_axis
    solids: List[Solid] = []

    across = local.width
    along = local.length
    diameter = max(across, 60.0)

    if component.points and len(component.points) >= 3:
        # A closed polygon silhouette: EXTRUSION keeps every vertex, so the
        # plan is the drawn octagon/diamond/arc exactly rather than a circle
        # or box standing in for it.
        body_height = max(diameter * 0.62, 70.0)
        solids.append(
            _polygon_body(
                component.points,
                model,
                placement,
                centreline - body_height / 2.0,
                body_height,
                label,
                handles,
            )
        )
        solids.extend(
            _casing_train(
                local,
                placement,
                centreline,
                plate_top,
                diameter,
                diameter * 0.45,
                max(model.outline_size) / 2.0,
            )
        )
        return solids

    if component.round_axis == "z":
        # Concentric disc stack: a vertical cylinder of revolution about the
        # drawn circle, so its plan is that circle and nothing else.
        body_height = max(diameter * 0.62, 70.0)
        solids.append(
            Solid(
                primitive="CYLI",
                label=label,
                position=local_to_world(
                    (local.along, local.across, centreline), placement
                ),
                diameter=diameter,
                height=body_height,
                axis="U",
                source_handles=handles,
            )
        )
        # Top split flange and its vertical bolt ring: a larger concentric
        # disc, exactly the second ring the drawing shows.
        flange_d = diameter * 1.10
        flange_t = max(diameter * 0.055, 16.0)
        flange_up = centreline + body_height / 2.0 + flange_t / 2.0
        solids.append(
            Solid(
                primitive="CYLI",
                label="casing split flange at the cover joint",
                position=local_to_world(
                    (local.along, local.across, flange_up), placement
                ),
                diameter=flange_d,
                height=flange_t,
                axis="U",
            )
        )
        bolt_d = _clamp_value(diameter * 0.045, 12.0, 22.0)
        bolt_radius = flange_d / 2.0 - bolt_d * 0.9
        bolt_count = 8 if diameter < 260.0 else 12
        for index in range(bolt_count):
            angle = 2.0 * math.pi * index / bolt_count
            bolt_pos = local_to_world(
                (
                    local.along + bolt_radius * math.cos(angle),
                    local.across + bolt_radius * math.sin(angle),
                    centreline + body_height / 2.0 + flange_t,
                ),
                placement,
            )
            shank_len = flange_t + bolt_d * 1.6
            solids.append(
                Solid(
                    primitive="CYLI",
                    label=(
                        f"Reference Value: casing flange bolt "
                        f"{index + 1}/{bolt_count}"
                    ),
                    position=(
                        bolt_pos[0],
                        bolt_pos[1],
                        bolt_pos[2] - shank_len / 2.0,
                    ),
                    diameter=bolt_d,
                    height=shank_len,
                    axis="U",
                )
            )
            solids.append(
                _hex_fastener(
                    centre=(
                        bolt_pos[0],
                        bolt_pos[1],
                        bolt_pos[2] + bolt_d * 0.4,
                    ),
                    axis="U",
                    across_flats=bolt_d * 1.7,
                    thickness=bolt_d * 0.8,
                    label=(
                        f"Reference Value: casing flange hex nut "
                        f"{index + 1}/{bolt_count}"
                    ),
                    group="CASING",
                )
            )
        solids.extend(
            _casing_train(
                local,
                placement,
                centreline,
                plate_top,
                diameter,
                body_height,
                max(model.outline_size) / 2.0,
            )
        )
        return solids

    # Merged open band: a barrel cylinder on the shaft axis whose plan
    # equals the drawn rectangle verbatim.
    body_len = max(along, diameter * 0.35)
    solids.append(
        Solid(
            primitive="CYLI",
            label=label,
            position=local_to_world(
                (local.along, local.across, centreline), placement
            ),
            diameter=diameter,
            height=body_len,
            axis=axis,
            source_handles=handles,
        )
    )
    solids.extend(
        _casing_train(
            local,
            placement,
            centreline,
            plate_top,
            diameter,
            body_len,
            max(model.outline_size) / 2.0,
        )
    )
    return solids


def _casing_train(
    local,
    placement: Placement,
    centreline: float,
    plate_top: float,
    diameter: float,
    body_len: float,
    plate_half: float,
) -> List[Solid]:
    """Cover, shaft boss, flank ribs and foot shared by every casing form."""
    axis = placement.layout_axis
    solids: List[Solid] = []

    cover_d = diameter * 0.62
    cover_len = min(body_len * 0.30, diameter * 0.45)
    # The cover must stay on the machine: it closes toward the suction end
    # but can never reach past the plate (or the drawn extent) and start
    # floating as an out-of-drawing spout.
    available = max(
        plate_half - 10.0 - (local.along + body_len / 2.0), 0.0
    )
    cover_len = min(cover_len, available)
    if cover_len > 20.0:
        solids.append(
            Solid(
                primitive="CONE",
                label="volute closing onto the suction cover",
                position=local_to_world(
                    (
                        local.along + body_len / 2.0 + cover_len / 2.0,
                        local.across,
                        centreline,
                    ),
                    placement,
                ),
                dtop=cover_d,
                dbot=diameter,
                height=cover_len,
                axis=axis,
            )
        )

    boss_d = diameter * 0.42
    boss_len = body_len * 0.18
    solids.append(
        Solid(
            primitive="CYLI",
            label="casing shaft boss toward the bearing frame",
            position=local_to_world(
                (
                    local.along - body_len / 2.0 - boss_len / 2.0,
                    local.across,
                    centreline,
                ),
                placement,
            ),
            diameter=boss_d,
            height=boss_len,
            axis=axis,
        )
    )

    # Axial casting ribs as rods on the barrel flanks, lying on the shaft
    # axis like the real part rather than standing up as plates.
    rib_d = _clamp_value(diameter * 0.045, 9.0, 18.0)
    rib_len = body_len * 0.52
    for sign in (-1.0, 1.0):
        solids.append(
            Solid(
                primitive="CYLI",
                label="Reference Value: axial casing rib",
                position=local_to_world(
                    (
                        local.along,
                        local.across + sign * (diameter / 2.0 + rib_d * 0.4),
                        centreline,
                    ),
                    placement,
                ),
                diameter=rib_d,
                height=rib_len,
                axis=axis,
            )
        )

    solids.extend(
        _support_assembly(
            local.along,
            local.across,
            body_len * 0.50,
            diameter * 0.62,
            plate_top,
            max(centreline - diameter * 0.48, plate_top + 25.0),
            placement,
            "Casing support",
        )
    )
    return solids


def _polygon_body(
    points: Sequence[Tuple[float, float]],
    model: PumpSemanticModel,
    placement: Placement,
    bottom_up: float,
    height: float,
    label: str,
    handles: List[str],
) -> Solid:
    """A vertical EXTRUSION whose LOOP is a drawn polygon, plan-exact."""
    outline = model.outline
    if outline is None:
        raise ValueError("polygon body needs a recovered outline")
    ox0, oy0, ox1, oy1 = outline
    plate_cx = (ox0 + ox1) / 2.0
    plate_cy = (oy0 + oy1) / 2.0

    world_points: List[Tuple[float, float]] = []
    for x, y in points:
        if model.long_axis == "x":
            along, across = x - plate_cx, y - plate_cy
        else:
            along, across = y - plate_cy, -(x - plate_cx)
        east, north, _ = local_to_world((along, across, 0.0), placement)
        world_points.append((east, north))

    east0 = sum(point[0] for point in world_points) / len(world_points)
    north0 = sum(point[1] for point in world_points) / len(world_points)
    loop = [
        (point[0] - east0, point[1] - north0) for point in world_points
    ]
    if loop and loop[0] != loop[-1]:
        loop.append(loop[0])
    return Solid(
        primitive="EXTRUSION",
        label=label,
        position=(east0, north0, bottom_up),
        height=height,
        vertices=loop,
        orientation="Y IS N AND Z IS U",
        source_handles=handles,
        group="CASING",
    )


def _clamp_value(value: float, low: float, high: float) -> float:
    """Clamp a dimension; used to bound Reference-Value detail sizes."""
    return max(low, min(high, value))


def _casing_top(casing: Solid) -> float:
    """Crown elevation of a casing body, whatever primitive represents it."""
    if casing.primitive == "EXTRUSION":
        # POS is the profile end plane and HEIG sweeps upward for Z IS U.
        return casing.position[2] + casing.height
    if casing.axis in ("U", "D"):
        return casing.position[2] + casing.height / 2.0
    return casing.position[2] + casing.diameter / 2.0


def _hex_vertices(across_flats: float) -> List[Tuple[float, float]]:
    """Six LOOP vertices of a regular hexagon, centred on the origin."""
    radius = across_flats / math.sqrt(3.0)
    return [
        (
            radius * math.cos(math.radians(30.0 + index * 60.0)),
            radius * math.sin(math.radians(30.0 + index * 60.0)),
        )
        for index in range(6)
    ]


def _hex_fastener(
    centre: Tuple[float, float, float],
    axis: str,
    across_flats: float,
    thickness: float,
    label: str,
    group: str = "BASEPLATE",
) -> Solid:
    """A hexagonal nut/head as a native EXTRUSION.

    The hexagon is the profile, swept along the fastener's own axis, so the
    solid is a true hex prism rather than a cylinder pretending to be one.
    POS is the profile end plane (the back face) and HEIG runs toward the
    fastener axis, matching the verified EXTRUSION datum.
    """
    key = axis.upper()
    if key not in CARDINAL_3D:
        raise ValueError(f"unsupported fastener axis: {axis!r}")
    if key in ("U", "D"):
        orientation = f"Y IS N AND Z IS {key}"
    else:
        orientation = f"Y IS U AND Z IS {key}"
    zx, zy, zz = CARDINAL_3D[key]
    position = (
        centre[0] - zx * thickness / 2.0,
        centre[1] - zy * thickness / 2.0,
        centre[2] - zz * thickness / 2.0,
    )
    return Solid(
        primitive="EXTRUSION",
        label=label,
        position=position,
        height=thickness,
        vertices=_hex_vertices(across_flats),
        orientation=orientation,
        group=group,
    )


def _gusset(
    along: float,
    across: float,
    bottom_up: float,
    length: float,
    height: float,
    thickness: float,
    placement: Placement,
    label: str,
) -> Solid:
    """A triangular stiffener plate, as a flat EXTRUSION in the machine's
    vertical plane (shaft axis x up), swept through the plate thickness."""
    axis = placement.layout_axis
    # Local X must point along +machine axis and local Y straight up, so the
    # triangle LOOP lies in the axis/up plane; the sweep then crosses the
    # machine transversely, which is the plate thickness.
    z_axis = {"E": "S", "W": "N", "N": "E", "S": "W"}[axis]
    orientation = f"Y IS U AND Z IS {z_axis}"
    centre = local_to_world((along, across, bottom_up), placement)
    zx, zy, zz = CARDINAL_3D[z_axis]
    position = (
        centre[0] - zx * thickness / 2.0,
        centre[1] - zy * thickness / 2.0,
        centre[2] - zz * thickness / 2.0,
    )
    return Solid(
        primitive="EXTRUSION",
        label=label,
        position=position,
        height=thickness,
        vertices=[
            (0.0, 0.0),
            (length, 0.0),
            (length * 0.55, height),
        ],
        orientation=orientation,
        group="SUPPORT",
    )


def _support_assembly(
    along: float,
    across: float,
    foot_len: float,
    foot_w: float,
    plate_top: float,
    bearing_top: float,
    placement: Placement,
    label_prefix: str,
) -> List[Solid]:
    """A real fabricated support: sole plate, pedestal, two triangular
    gussets and two hold-downs with hex nuts, all bearing on the plate."""
    solids: List[Solid] = []
    sole_t = max(foot_w * 0.12, 10.0)
    pedestal_h = max(bearing_top - plate_top - sole_t, 20.0)

    sole_x, sole_y = world_size(foot_len * 1.15, foot_w * 1.15, placement)
    solids.append(
        Solid(
            primitive="BOX",
            label=f"{label_prefix}: sole plate on the baseplate",
            position=local_to_world(
                (along, across, plate_top + sole_t / 2.0), placement
            ),
            xlen=sole_x,
            ylen=sole_y,
            zlen=sole_t,
        )
    )
    ped_x, ped_y = world_size(foot_len * 0.58, foot_w * 0.58, placement)
    solids.append(
        Solid(
            primitive="BOX",
            label=f"{label_prefix}: pedestal web",
            position=local_to_world(
                (along, across, plate_top + sole_t + pedestal_h / 2.0),
                placement,
            ),
            xlen=ped_x,
            ylen=ped_y,
            zlen=pedestal_h,
        )
    )
    for sign in (-1.0, 1.0):
        solids.append(
            _gusset(
                along - foot_len * 0.30,
                across + sign * foot_w * 0.30,
                plate_top + sole_t,
                foot_len * 0.60,
                pedestal_h * 0.88,
                foot_w * 0.10,
                placement,
                f"{label_prefix}: triangular stiffener gusset",
            )
        )

    bolt_d = max(foot_w * 0.065, 12.0)
    for sign in (-1.0, 1.0):
        bolt_pos = local_to_world(
            (along + sign * foot_len * 0.36, across, 0.0), placement
        )
        shank_top = plate_top + sole_t
        solids.append(
            Solid(
                primitive="CYLI",
                label=f"{label_prefix}: hold-down bolt shank",
                position=(
                    bolt_pos[0],
                    bolt_pos[1],
                    plate_top + (shank_top - plate_top) / 2.0,
                ),
                diameter=bolt_d,
                height=shank_top - plate_top + bolt_d,
                axis="U",
            )
        )
        solids.append(
            _hex_fastener(
                centre=(bolt_pos[0], bolt_pos[1], shank_top + bolt_d * 0.4),
                axis="U",
                across_flats=bolt_d * 1.7,
                thickness=bolt_d * 0.8,
                label=f"{label_prefix}: hold-down hex nut",
                group="SUPPORT",
            )
        )
    return solids


def _driver(
    local,
    placement: Placement,
    centreline: float,
    plate_top: float,
    label: str,
    handles: List[str],
    axis: str,
) -> List[Solid]:
    """The driver: barrel, end bells, 360-degree cooling fins, terminal
    box, feet and hold-downs.

    The barrel is a cylinder lying along the machine axis whose plan
    footprint equals the drawn motor contour verbatim.  Every added detail
    is a bounded Reference Value scaled from that measured envelope; the
    full-circumference fin array follows the client's standing correction
    that a few top-side strips are not an acceptable motor.
    """
    body_len = local.length
    body_d = local.width
    solids: List[Solid] = [
        Solid(
            primitive="CYLI",
            label=label,
            position=local_to_world(
                (local.along, local.across, centreline), placement
            ),
            diameter=body_d,
            height=body_len,
            axis=axis,
            source_handles=handles,
        )
    ]

    # End bells at both ends of the stator.
    bell_d = body_d * 1.08
    bell_len = body_len * 0.06
    for sign in (-1.0, 1.0):
        solids.append(
            Solid(
                primitive="CYLI",
                label="Motor end bell",
                position=local_to_world(
                    (
                        local.along + sign * (body_len / 2.0 - bell_len / 2.0),
                        local.across,
                        centreline,
                    ),
                    placement,
                ),
                diameter=bell_d,
                height=bell_len,
                axis=axis,
            )
        )

    # Axial cooling ribs around the complete 360-degree stator: thin rods
    # lying on the shaft axis at equal angles, the same construction the
    # client accepted for the r14 motors.  A plate that only stands up at
    # the top of the barrel is not a fin; a full circumference is.
    fin_count = 10 + int(round(body_d / 70.0))
    fin_count = max(10, min(fin_count, 16))
    fin_len = body_len * 0.72
    fin_t = _clamp_value(body_d * 0.028, 7.0, 16.0)
    fin_radius = body_d / 2.0 + fin_t / 2.0
    for index in range(fin_count):
        angle = 2.0 * math.pi * index / fin_count
        solids.append(
            Solid(
                primitive="CYLI",
                label=(
                    f"Reference Value: 360-degree motor cooling rib "
                    f"{index + 1}/{fin_count}"
                ),
                position=local_to_world(
                    (
                        local.along,
                        local.across + fin_radius * math.cos(angle),
                        centreline + fin_radius * math.sin(angle),
                    ),
                    placement,
                ),
                diameter=fin_t,
                height=fin_len,
                axis=axis,
            )
        )

    # Terminal box on top of the driver, with its cable gland and a lifting
    # lug beside it.
    box_h = body_d * 0.22
    box_len = body_len * 0.30
    box_w = body_d * 0.40
    box_x, box_y = world_size(box_len, box_w, placement)
    solids.append(
        Solid(
            primitive="BOX",
            label="Motor terminal box",
            position=local_to_world(
                (
                    local.along,
                    local.across,
                    centreline + body_d / 2.0 + box_h / 2.0,
                ),
                placement,
            ),
            xlen=box_x,
            ylen=box_y,
            zlen=box_h,
        )
    )
    gland_d = box_h * 0.34
    gland_len = body_d * 0.22
    solids.append(
        Solid(
            primitive="CYLI",
            label="Motor cable gland",
            position=local_to_world(
                (
                    local.along,
                    local.across + box_w / 2.0 + gland_len / 2.0,
                    centreline + body_d / 2.0 + box_h / 2.0,
                ),
                placement,
            ),
            diameter=gland_d,
            height=gland_len,
            axis="E" if placement.layout_axis in ("N", "S") else "N",
        )
    )
    lug_x, lug_y = world_size(body_d * 0.12, body_d * 0.07, placement)
    solids.append(
        Solid(
            primitive="BOX",
            label="Reference Value: motor lifting lug",
            position=local_to_world(
                (
                    local.along - body_len * 0.28,
                    local.across,
                    centreline + body_d / 2.0 + box_h * 0.55,
                ),
                placement,
            ),
            xlen=lug_x,
            ylen=lug_y,
            zlen=body_d * 0.10,
        )
    )
    # Nameplate on the barrel flank.
    plate_x, plate_y = world_size(body_len * 0.18, body_d * 0.13, placement)
    solids.append(
        Solid(
            primitive="BOX",
            label="Reference Value: motor nameplate",
            position=local_to_world(
                (
                    local.along + body_len * 0.12,
                    local.across - body_d / 2.0 - 2.0,
                    centreline,
                ),
                placement,
            ),
            xlen=plate_x,
            ylen=plate_y,
            zlen=6.0,
        )
    )

    # Fan grille: a thin end disc plus radial bars at the non-drive end.
    grille_d = body_d * 1.10
    grille_t = 8.0
    solids.append(
        Solid(
            primitive="CYLI",
            label="Motor fan cowl disc",
            position=local_to_world(
                (
                    local.along - body_len / 2.0 - grille_t / 2.0,
                    local.across,
                    centreline,
                ),
                placement,
            ),
            diameter=grille_d,
            height=grille_t,
            axis=axis,
        )
    )
    bar_x, bar_y = world_size(grille_t * 1.2, grille_d * 0.46, placement)
    for side in (-1.0, 1.0):
        solids.append(
            Solid(
                primitive="BOX",
                label="Motor fan grille bar",
                position=local_to_world(
                    (
                        local.along - body_len / 2.0 - grille_t / 2.0,
                        local.across + side * grille_d * 0.23,
                        centreline,
                    ),
                    placement,
                ),
                xlen=bar_x,
                ylen=bar_y,
                zlen=grille_t * 0.8,
            )
        )

    # Two fabricated feet under the driver, each a sole plate + pedestal +
    # gussets + hold-downs rather than a bare pad.
    for sign in (-1.0, 1.0):
        foot_pos = local.along + sign * body_len * 0.32
        solids.extend(
            _support_assembly(
                foot_pos,
                local.across,
                body_len * 0.17,
                body_d * 0.95,
                plate_top,
                max(centreline - body_d * 0.45, plate_top + 25.0),
                placement,
                "Motor foot",
            )
        )
    return solids


def _elevation_body_solids(
    model: PumpSemanticModel, placement: Placement
) -> List[Solid]:
    """Build bodies from an elevation.

    Here the drawing measures the height directly and the horizontal span
    is a diameter, so these bodies are emitted as cylinders of revolution
    about the vertical pump axis.  This is the case the CAD constrains
    *better* than a plan view would.
    """
    solids: List[Solid] = []
    assert model.outline is not None

    # Elevations are measured from the outline base, but several drawings
    # put real geometry *below* their own dimension line - an MC pump's
    # pedestal is drawn under the machine envelope.  Those parts would then
    # be given negative elevations and sink through the baseplate, so the
    # datum is shifted down to the lowest drawn component.
    vertical_is_y = (model.outline[3] - model.outline[1]) >= (
        model.outline[2] - model.outline[0]
    )
    v = 1 if vertical_is_y else 0
    lowest = min(
        (
            component.bounds[v]
            for component in model.components
            if component.kind is not ComponentKind.BASEPLATE
        ),
        default=model.outline[v],
    )
    underhang = max(model.outline[v] - lowest, 0.0)

    for component in model.components:
        if component.kind is ComponentKind.BASEPLATE:
            continue
        local = cad_to_local(
            component.bounds,
            outline=model.outline,
            view=ViewType.ELEVATION,
            long_axis=model.long_axis,
            base_elevation=BASEPLATE_THICKNESS + underhang,
        )
        position = local_to_world(local.centre, placement)
        # An elevation measures the height directly and the horizontal span
        # is a diameter, so these are true bodies of revolution: both the
        # profile and the size come from the drawing, nothing is inferred.
        solids.append(
            Solid(
                primitive="CYLI",
                label=(
                    f"{component.kind.value} [{component.confidence.value}]: "
                    f"{component.reason}"
                ),
                position=position,
                diameter=local.length,
                height=local.height,
                axis="U",
                source_handles=list(component.handles),
            )
        )
    return solids


def _plan_reach(
    model: PumpSemanticModel, placement: Placement, direction: str
) -> Optional[Tuple[float, float]]:
    """World point where the linework stops in ``direction``.

    Only meaningful for a plan view, where the drawing shows the branch
    in the plane it projects onto.  Returns ``None`` when the drawing
    cannot say, so the caller keeps its fallback.
    """
    if model.view is not ViewType.PLAN or model.outline is None:
        return None
    extent = getattr(model, "cad_extent", None)
    if extent is None:
        return None

    ox0, oy0, ox1, oy1 = model.outline
    plate_cx, plate_cy = (ox0 + ox1) / 2.0, (oy0 + oy1) / 2.0
    ex0, ey0, ex1, ey1 = extent
    if model.long_axis == "x":
        forward_far, forward_near = ex1 - plate_cx, plate_cx - ex0
        cross_far, cross_near = ey1 - plate_cy, plate_cy - ey0
    else:
        forward_far, forward_near = ey1 - plate_cy, plate_cy - ey0
        cross_far, cross_near = plate_cx - ex0, ex1 - plate_cx

    layout = placement.layout_axis
    if direction == layout:
        along, across = forward_far, 0.0
    elif direction == OPPOSITE_AXIS[layout]:
        along, across = -forward_near, 0.0
    else:
        left = placement.left
        vx, vy = AXIS_VECTOR[direction]
        along = 0.0
        across = cross_far if (vx * left[0] + vy * left[1]) > 0 else -cross_near
    east, north, _ = local_to_world((along, across, 0.0), placement)
    return (east, north)


def _nozzles(
    record: PumpRecord,
    model: PumpSemanticModel,
    placement: Placement,
    solids: Sequence[Solid],
    centreline: float,
) -> Tuple[List[Nozzle], List[str]]:
    """Create the suction and discharge nozzles.

    Identity and nominal size come from metadata (authoritative); the
    attachment point is the pump's own machine: horizontal nozzles sit on
    the shaft centreline and vertical ones on the casing crown, so a nozzle
    can never fall to the baseplate datum.
    """
    nozzles: List[Nozzle] = []
    notes: List[str] = []

    casing = next(
        (
            solid
            for solid in solids
            if solid.label.startswith("PumpCasing")
            and solid.primitive == "CYLI"
        ),
        None,
    )
    casing_top = _casing_top(casing) if casing is not None else centreline + 150.0
    casing_east, casing_north = (
        casing.position[:2] if casing is not None else placement.origin[:2]
    )
    origin = placement.origin

    for role, bore, axis in (
        ("SUCTION", record.dn_input_mm, record.inlet_orientation),
        ("DISCHARGE", record.dn_output_mm, record.outlet_orientation),
    ):
        if bore <= 0:
            notes.append(f"{role.lower()}: no bore in metadata; nozzle omitted")
            continue
        direction = (axis or "").upper()
        if direction not in ("E", "W", "N", "S", "U", "D"):
            notes.append(
                f"{role.lower()}: unusable direction {axis!r} in metadata; "
                f"nozzle omitted"
            )
            continue
        try:
            dn, note = snap_to_catalogue_dn(bore)
        except ValueError as exc:
            notes.append(f"{role.lower()}: {exc}; nozzle omitted")
            continue
        if note:
            notes.append(f"{role.lower()}: {note}")

        if direction in ("U", "D"):
            sign = 1.0 if direction == "U" else -1.0
            face = (
                casing_east,
                casing_north,
                casing_top + sign * NOZZLE_PROJECTION,
            )
        else:
            from .transform import AXIS_VECTOR

            vx, vy = AXIS_VECTOR[direction]
            # How far the branch reaches is *drawn*, so measure it rather
            # than assume a standoff.  A fixed 150 mm offset once put the
            # flange 43 mm outside the drawn silhouette.  The drawn reach is
            # capped at the plate edge plus a nozzle-scale projection: a
            # long suction elbow beyond the plate is attached pipework, not
            # part of the nozzle, and chasing it to its far end would leave
            # the flange floating metres from the casing (204-PU-003).
            layout = placement.layout_axis
            plate_half = (
                record.length_mm / 2.0
                if direction in (layout, OPPOSITE_AXIS[layout])
                else record.width_mm / 2.0
            )
            projection = max(dn * 0.35, 60.0)
            flange_t = max(dn * 0.16, 20.0)
            limit = _plan_reach(model, placement, direction)
            if limit is not None:
                drawn = abs(
                    (limit[0] - origin[0]) * vx
                    + (limit[1] - origin[1]) * vy
                )
                # Seat the flange face so its outer edge lands on the drawn
                # extent (leaving the flange thickness inboard), but never
                # beyond the plate edge plus the projection.
                use = min(drawn, plate_half + projection)
            else:
                use = plate_half + projection
            face = (
                origin[0] + vx * (use - flange_t),
                origin[1] + vy * (use - flange_t),
                centreline,
            )

        nozzles.append(
            Nozzle(
                label=(
                    f"{role.lower()} DN{dn}; POS is the flange face, "
                    f"contractual direction {direction}"
                ),
                role=role,
                dn=dn,
                catref=nozzle_component_path(dn),
                face=face,
                axis=direction,
                height=NOZZLE_PROJECTION,
            )
        )

    return nozzles, notes


def build_pump(record: PumpRecord, model: PumpSemanticModel) -> PumpBuild:
    """Assemble one pump.  Never raises for data reasons."""
    placement = Placement(
        origin=record.location_e_n_u, layout_axis=_layout_axis(record)
    )
    build = PumpBuild(
        tag=record.tag,
        name=record.name,
        safe_tag=record.tag.replace("-", "_"),
        placement=placement,
        view=model.view,
    )
    build.warnings.extend(model.warnings)

    plate, notes = _baseplate_solid(record, model, placement)
    build.solids.append(plate)
    build.notes.extend(notes)

    # The shaft centreline must clear the suction flange's own radius: a
    # DN600 end-suction pump cannot have its centreline at DN150 height or
    # the flange sinks through the foundation.
    centreline = (
        _shaft_elevation(model)
        if model.components
        else BASEPLATE_THICKNESS
        + max(record.width_mm * 0.16, 40.0)
        + record.width_mm * 0.27
    )
    suction_flange_d = max(record.dn_input_mm * 1.9, 0.0)
    centreline = max(
        centreline,
        BASEPLATE_THICKNESS + suction_flange_d / 2.0 + 30.0,
    )

    if model.outline is not None and model.components:
        if model.view is ViewType.PLAN:
            build.solids.extend(
                _plan_body_solids(model, placement, centreline)
            )
        elif model.view is ViewType.ELEVATION:
            build.solids.extend(_elevation_body_solids(model, placement))
    else:
        build.solids.extend(
            _metadata_fallback_solids(record, placement, centreline)
        )
        build.warnings.append(
            "no CAD top view in this file; pump body geometry is a "
            "metadata-proportioned Reference Value and remains UNCONFIRMED"
        )

    nozzles, nozzle_notes = _nozzles(
        record, model, placement, build.solids, centreline
    )
    build.nozzles.extend(nozzles)
    build.notes.extend(nozzle_notes)

    # Anchor bolts fixing the baseplate to its foundation.
    build.solids.extend(_anchor_bolts(build.solids[0], placement))

    # Assign every solid to its major-assembly SUBE group after the whole
    # solid list exists, so builders never have to track grouping while
    # they emit geometry.
    for solid in build.solids:
        solid.group = _group_for(solid.label)
    return build


def _metadata_fallback_solids(
    record: PumpRecord, placement: Placement, centreline: float
) -> List[Solid]:
    """A bounded horizontal body when a file carries no top view at all.

    Used only for 203-PU-020 and 205-PU-004.  Every dimension here is a
    Reference Value scaled from the contractual baseplate, and the audit
    keeps the pump flagged UNCONFIRMED until vendor data or a top view
    arrives.
    """
    axis = placement.layout_axis
    plate_top = BASEPLATE_THICKNESS
    length, width = record.length_mm, record.width_mm

    motor_len = length * 0.42
    motor_d = width * 0.52
    casing_len = length * 0.30
    casing_d = width * 0.46
    solids: List[Solid] = []

    # Driver at the end opposite the casing.
    motor_along = -length / 2.0 + motor_len / 2.0 + length * 0.06
    solids.append(
        Solid(
            primitive="CYLI",
            label="UNCONFIRMED: motor barrel (metadata-proportioned)",
            position=local_to_world(
                (motor_along, 0.0, centreline), placement
            ),
            diameter=motor_d,
            height=motor_len,
            axis=axis,
        )
    )
    for sign in (-1.0, 1.0):
        solids.extend(
            _support_assembly(
                motor_along + sign * motor_len * 0.30,
                0.0,
                motor_len * 0.17,
                motor_d * 0.95,
                plate_top,
                max(centreline - motor_d * 0.45, plate_top + 25.0),
                placement,
                "UNCONFIRMED: motor foot",
            )
        )

    # Coupling between driver and casing.
    coupling_len = length * 0.12
    coupling_along = casing_len / 2.0 + coupling_len / 2.0 + length * 0.02
    solids.append(
        Solid(
            primitive="CYLI",
            label="UNCONFIRMED: coupling (metadata-proportioned)",
            position=local_to_world(
                (coupling_along, 0.0, centreline), placement
            ),
            diameter=motor_d * 0.36,
            height=coupling_len,
            axis=axis,
        )
    )
    solids.append(
        Solid(
            primitive="BOX",
            label="UNCONFIRMED: coupling guard (metadata-proportioned)",
            position=local_to_world(
                (coupling_along, 0.0, centreline), placement
            ),
            xlen=world_size(coupling_len, motor_d * 0.46, placement)[0],
            ylen=world_size(coupling_len, motor_d * 0.46, placement)[1],
            zlen=motor_d * 0.46,
        )
    )

    # Volute at the wet end, with its foot.
    casing_along = length / 2.0 - casing_len / 2.0 - length * 0.04
    solids.append(
        Solid(
            primitive="CYLI",
            label="UNCONFIRMED: volute barrel (metadata-proportioned)",
            position=local_to_world(
                (casing_along, 0.0, centreline), placement
            ),
            diameter=casing_d,
            height=casing_len,
            axis=axis,
        )
    )
    solids.append(
        Solid(
            primitive="CONE",
            label="UNCONFIRMED: suction cover (metadata-proportioned)",
            position=local_to_world(
                (
                    casing_along + casing_len / 2.0 + casing_len * 0.16,
                    0.0,
                    centreline,
                ),
                placement,
            ),
            dtop=casing_d * 0.62,
            dbot=casing_d,
            height=casing_len * 0.32,
            axis=axis,
        )
    )
    solids.extend(
        _support_assembly(
            casing_along,
            0.0,
            casing_len * 0.50,
            casing_d * 0.62,
            plate_top,
            max(centreline - casing_d * 0.48, plate_top + 25.0),
            placement,
            "UNCONFIRMED: casing foot",
        )
    )
    return solids


def _group_for(label: str, role: str = "") -> str:
    """Major-assembly SUBE for one solid, from its construction label."""
    text = label.lower()
    if role:
        return role
    if "branch neck" in text or "raised-face flange" in text:
        return "SUCTION" if "suction" in text else "DISCHARGE"
    if "contractual rectangular baseplate" in text or "anchor bolt" in text:
        return "BASEPLATE"
    if (
        "sole plate" in text
        or "pedestal web" in text
        or "stiffener gusset" in text
        or "hold-down" in text
        or "casing support" in text
        or "motor foot" in text
        or "bearing housing pedestal" in text
        or "unconfirmed: motor foot" in text
        or "unconfirmed: casing foot" in text
    ):
        return "SUPPORT"
    if (
        "pumpcasing" in text
        or "casing split flange" in text
        or "casing flange bolt" in text
        or "casing flange hex nut" in text
        or "casing shaft boss" in text
        or "volute" in text
        or "suction cover" in text
        or "axial casing rib" in text
        or "unconfirmed: volute barrel" in text
    ):
        return "CASING"
    if "bearing" in text:
        return "BEARING"
    if (
        "coupling" in text
        or "shaft" in text
        or " hub" in text
    ):
        return "COUPLING"
    if (
        "motor" in text
        or "cooling rib" in text
        or "terminal box" in text
        or "cable gland" in text
        or "lifting lug" in text
        or "nameplate" in text
        or "fan" in text
        or "end bell" in text
        or "hold-down" in text
        or "unconfirmed: motor barrel" in text
    ):
        return "DRIVER"
    return "AUXILIARY"


def _anchor_bolts(plate: Solid, placement: Placement) -> List[Solid]:
    """Foundation bolts at the four corners of the baseplate."""
    if plate.primitive != "BOX":
        return []
    east, north, up = plate.position
    inset_x = plate.xlen / 2.0 - min(plate.xlen * 0.06, 90.0)
    inset_y = plate.ylen / 2.0 - min(plate.ylen * 0.10, 90.0)
    shank = max(min(plate.xlen, plate.ylen) * 0.03, 20.0)
    across_flats = shank * 1.7
    nut_t = shank * 0.8
    top = up + plate.zlen / 2.0

    bolts: List[Solid] = []
    for index, (dx, dy) in enumerate(
        ((-1, -1), (-1, 1), (1, -1), (1, 1)), start=1
    ):
        x = east + dx * inset_x
        y = north + dy * inset_y
        bolts.append(
            Solid(
                primitive="CYLI",
                label=f"Baseplate anchor bolt A{index}: exposed shank",
                position=(x, y, top + shank * 0.75),
                diameter=shank,
                height=shank * 1.5,
                axis="U",
            )
        )
        bolts.append(
            _hex_fastener(
                centre=(x, y, top + shank * 1.5 + nut_t / 2.0),
                axis="U",
                across_flats=across_flats,
                thickness=nut_t,
                label=f"Baseplate anchor bolt A{index}: hex nut",
                group="BASEPLATE",
            )
        )
    return bolts


def _fmt(value: float) -> str:
    return f"{value:.1f}"


def render_pml(build: PumpBuild, *, generated: str) -> str:
    """Render one pump as a PML1 macro.

    Follows the JK_Pump_Build layout exactly: a banner, exactly one EQUI,
    SUBE groups, ORI before POS, and CATR bound before the nozzle's
    position.
    """
    lines: List[str] = []
    add = lines.append

    add("-- " + "=" * 68)
    add(f"-- {build.tag} - {build.name}")
    add("-- " + "=" * 68)
    add("-- Project: JK_Pump_Build (pumpcad reconstruction)")
    add(f"-- Equipment: {build.tag}")
    add("-- Units: mm")
    add("-- Frame: E = East, N = North, U = Up")
    add("-- Datum: metadata coordinate = geometric centre of baseplate underside")
    add(f"-- Source view: {build.view.value}")
    add(f"-- Layout axis: {build.placement.layout_axis} (driver -> casing)")
    add("-- Hierarchy: Exactly one EQUI in this file")
    add("-- Execution: Select a writable ZONE, then $M <this file>")
    add(f"-- Generated: {generated}")
    for note in build.notes:
        add(f"-- Note: {note}")
    for warning in build.warnings:
        add(f"-- Warning: {warning}")
    add("")
    add(f"NEW EQUI /{build.safe_tag}")
    add("POS E 0.0 N 0.0 U 0.0")

    # One SUBE per major assembly, not one per primitive: the tree stays
    # readable and a piping or structural designer can take hold of a whole
    # driver, casing or connection instead of a single box.
    group_order = (
        "BASEPLATE",
        "SUPPORT",
        "CASING",
        "BEARING",
        "COUPLING",
        "DRIVER",
        "AUXILIARY",
        "SUCTION",
        "DISCHARGE",
    )
    grouped: Dict[str, List[Solid]] = {}
    for solid in build.solids:
        grouped.setdefault(solid.group or "BODY", []).append(solid)

    for group in group_order:
        members = grouped.get(group)
        group_nozzles = [
            nozzle for nozzle in build.nozzles if nozzle.role == group
        ]
        if not members and not group_nozzles:
            continue
        add(f"NEW SUBE /{build.safe_tag}_{group}")
        add(
            f"-- {len(members or [])} part(s), "
            f"{len(group_nozzles)} nozzle(s)"
        )
        for solid in members or []:
            _append_solid(add, solid)
        # A connection is one SUBE: the modelled neck and raised-face flange
        # plus the catalogue NOZZLE itself, so selecting the SUBE selects the
        # whole connection and no duplicate SUBE name is ever emitted.
        for nozzle in group_nozzles:
            add(f"-- {nozzle.label}")
            add(f"NEW NOZZLE /{build.safe_tag}_{nozzle.role}_NOZZLE")
            add(f"CATR SPCOMPONENT {nozzle.catref}")
            east, north, up = nozzle.face
            add(f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(up)}")
            add(f"ORI P1 IS {nozzle.axis}")
            add(f"HEIG {_fmt(nozzle.height)}")
            add("TEMP -100000")
            add("PRES 0")
            add("TPRESS 0")
            add("DUTY unset")
            add("END")
            add("")

    return "\n".join(lines).rstrip() + "\n"


def _append_solid(add, solid: Solid) -> None:
    """Append one solid's PML1 block (ORI before POS for primitives)."""
    add(f"-- {solid.label}")
    if solid.source_handles:
        shown = ",".join(solid.source_handles[:6])
        more = "" if len(solid.source_handles) <= 6 else " ..."
        add(f"-- CAD handles: {shown}{more}")
    if solid.primitive == "BOX":
        add("NEW BOX")
        add(f"XLEN {_fmt(solid.xlen)}")
        add(f"YLEN {_fmt(solid.ylen)}")
        add(f"ZLEN {_fmt(solid.zlen)}")
        east, north, up = solid.position
        add(f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(up)}")
        add("")
    elif solid.primitive == "CONE":
        add("NEW CONE")
        add(f"DTOP {_fmt(solid.dtop)}")
        add(f"DBOT {_fmt(solid.dbot)}")
        add(f"HEIG {_fmt(solid.height)}")
        add(ori_clause(solid.axis))
        east, north, up = solid.position
        add(f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(up)}")
        add("")
    elif solid.primitive == "EXTRUSION":
        from wsb.extrusion_builder import build_extrusion

        add(
            build_extrusion(
                solid.position,
                solid.orientation,
                solid.height,
                solid.vertices,
            ).rstrip()
        )
        add("")
    else:
        add("NEW CYLI")
        add(f"DIAM {_fmt(solid.diameter)}")
        add(f"HEIG {_fmt(solid.height)}")
        add(ori_clause(solid.axis))
        east, north, up = solid.position
        add(f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(up)}")
        add("")
