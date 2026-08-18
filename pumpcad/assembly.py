"""
Feature -> component assembly.
==============================

Turns the extracted features into named pump components arranged along
the machine axis.  This is where a pump stops being a bag of shapes and
becomes a driver, a coupling, a shaft, a casing and their fittings.

The rule throughout: a component's silhouette in the drawing plane is
taken verbatim from the feature that evidences it.  Only the third
dimension is reasoned about, and for a body of revolution even that is
derived (a cylinder's unseen dimension equals its seen diameter).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from .features import Feature, FeatureKind
from .semantic import ComponentKind, Confidence, ViewType

__all__ = ["AssembledPart", "assemble_plan", "assemble_elevation"]


@dataclass
class AssembledPart:
    """A component ready to become a 3-D solid.

    ``bounds`` is the silhouette in the drawing plane, in CAD space.
    ``round_axis`` names the axis a body of revolution turns about, or
    ``None`` for a prismatic body.
    """

    kind: ComponentKind
    bounds: Tuple[float, float, float, float]
    confidence: Confidence
    reason: str
    handles: List[str] = field(default_factory=list)
    round_axis: Optional[str] = None
    radius: Optional[float] = None
    #: Ordered radii for a stepped disc feature.
    radii: List[float] = field(default_factory=list)
    #: Drawn outline points for a closed polygon feature, when the part is
    #: a single contour rather than a merged band.
    points: List[Tuple[float, float]] = field(default_factory=list)

    @property
    def size(self) -> Tuple[float, float]:
        x0, y0, x1, y1 = self.bounds
        return (x1 - x0, y1 - y0)

    @property
    def centroid(self) -> Tuple[float, float]:
        x0, y0, x1, y1 = self.bounds
        return ((x0 + x1) / 2.0, (y0 + y1) / 2.0)


#: Features smaller than this in both directions are drawing detail
#: (weld ticks, hatch stubs) rather than modellable geometry.
MIN_FEATURE_MM = 22.0


def _inside(
    inner: Tuple[float, float, float, float],
    outer: Tuple[float, float, float, float],
    slack: float = 5.0,
) -> bool:
    """Whether one bounds box sits within another, with optional slack."""
    return (
        inner[0] >= outer[0] - slack
        and inner[1] >= outer[1] - slack
        and inner[2] <= outer[2] + slack
        and inner[3] <= outer[3] + slack
    )


def _significant(feature: Feature) -> bool:
    width, height = feature.size
    if feature.kind is FeatureKind.UNCLASSIFIED:
        # An open path needs real extent in both directions to be a body.
        return min(width, height) >= MIN_FEATURE_MM
    return max(width, height) >= MIN_FEATURE_MM


def _merge_overlapping(
    features: Sequence[Feature], *, axis: int, tol: float
) -> List[Tuple[Tuple[float, float, float, float], List[str], List[Feature]]]:
    """Merge features whose extent along ``axis`` coincides.

    A motor drawn as a body plus two fin bands plus a terminal box is one
    component; merging by shared span along the machine axis recovers
    that without hard-coding what a motor looks like.
    """
    bands: List[Tuple[List[float], List[str], List[Feature]]] = []
    for feature in sorted(features, key=lambda f: f.bounds[axis]):
        lo, hi = feature.bounds[axis], feature.bounds[axis + 2]
        placed = False
        for band in bands:
            blo, bhi = band[0][0], band[0][1]
            overlap = min(hi, bhi) - max(lo, blo)
            if overlap > min(hi - lo, bhi - blo) * tol:
                band[0][0] = min(blo, lo)
                band[0][1] = max(bhi, hi)
                band[1].extend(feature.handles)
                band[2].append(feature)
                placed = True
                break
        if not placed:
            bands.append(([lo, hi], list(feature.handles), [feature]))

    merged: List[Tuple[Tuple[float, float, float, float], List[str], List[Feature]]] = []
    for _, handles, members in bands:
        xs0 = min(f.bounds[0] for f in members)
        ys0 = min(f.bounds[1] for f in members)
        xs1 = max(f.bounds[2] for f in members)
        ys1 = max(f.bounds[3] for f in members)
        merged.append(((xs0, ys0, xs1, ys1), handles, members))
    return merged


def _near_wet_end(
    feature: Feature,
    wet_edge: float,
    axis: int,
    axis_span: float,
) -> bool:
    """Whether a feature sits in the outer half of the plate toward the wet end."""
    centre = feature.centroid[axis]
    return abs(centre - wet_edge) < axis_span * 0.50


def assemble_plan(
    features: Sequence[Feature],
    outline: Tuple[float, float, float, float],
    long_axis: str,
    layout_axis: str,
    is_mc: bool = False,
) -> Tuple[List[AssembledPart], List[str]]:
    """Assemble a horizontal pump seen from above.

    Layout along the machine axis, driver end first:
    motor -> bearing/adapter -> shaft -> coupling -> casing -> nozzle.
    Position along that axis is the primary evidence for identity, anchored
    by the contractual layout axis (driver -> casing), which names the wet
    end unambiguously even when both ends of the drawing carry large bodies.
    """
    parts: List[AssembledPart] = []
    warnings: List[str] = []

    axis = 0 if long_axis == "x" else 1
    cross = 1 - axis
    ox0, oy0, ox1, oy1 = outline
    axis_lo = outline[axis]
    axis_hi = outline[axis + 2]
    axis_span = axis_hi - axis_lo
    plate_cross = (outline[cross] + outline[cross + 2]) / 2.0
    cross_span = outline[cross + 2] - outline[cross]

    # +along (driver -> casing) maps onto the drawing's own axis: E -> +X,
    # W -> -X, N -> +Y, S -> -Y.  The wet end is the corresponding end of
    # the outline and the driver end is its opposite.
    axis_sign = {
        "E": (1.0, 0.0),
        "W": (-1.0, 0.0),
        "N": (0.0, 1.0),
        "S": (0.0, -1.0),
    }.get((layout_axis or "E").upper(), (1.0, 0.0))
    wet_sign = axis_sign[1] if long_axis == "y" else axis_sign[0]
    wet_edge = axis_hi if wet_sign > 0 else axis_lo
    driver_end = axis_lo if wet_sign > 0 else axis_hi

    # Attached pipework is legitimately drawn beyond the baseplate (long
    # suction elbows, drain runs), but it belongs to the piping discipline,
    # not to the pump equipment.  Including it made one pump's "motor" band
    # swallow 2 m of suction line and one pump's casing a pipe elbow.  Only
    # linework inside the dimensioned outline takes part in the assembly;
    # nozzle reach is measured separately from the full CAD extent.
    usable = [
        f
        for f in features
        if _significant(f) and _inside(f.bounds, outline, slack=6.0)
    ]
    if not usable:
        warnings.append("no features large enough to model")
        return parts, warnings

    # The casing is the compact round feature of real size at one end of the
    # plate.  A concentric disc stack is the strongest evidence, but several
    # drawings give the volute as open linework and leave only the small
    # top-discharge bore as a closed circle; those pumps get their casing
    # from the largest compact body at an end instead.  The minimum radius
    # keeps a DN150 discharge bore (r ~ 73) from being mistaken for the
    # whole casing.
    # The compact MC fluidizer is drawn smaller than a conventional volute,
    # so its acceptance floor is lower; a full-size separator vessel beside
    # it is excluded separately below.
    min_casing_radius = (
        max(40.0, cross_span * 0.06)
        if is_mc
        else max(60.0, cross_span * 0.10)
    )
    discs = [
        f
        for f in usable
        if f.kind is FeatureKind.DISC_STACK
        and max(f.radii or [0.0]) >= min_casing_radius
        and _near_wet_end(f, wet_edge, axis, axis_span)
    ]
    casing = max(discs, key=lambda f: max(f.radii or [0.0]), default=None)

    # The shaft is the rail pair running along the machine axis.
    # The shaft is the rail pair on the machine centreline whose diameter is
    # small relative to the plate: a long thin cylinder, not a body.
    rails = [
        f
        for f in usable
        if f.kind is FeatureKind.CYLINDER
        and f.axis == long_axis
        and abs(f.centroid[cross] - plate_cross) < cross_span * 0.2
        and f.size[cross] < cross_span * 0.45
    ]
    shaft = max(rails, key=lambda f: f.size[axis], default=None)

    consumed = set()
    if casing is not None:
        consumed.update(casing.handles)
    if shaft is not None:
        consumed.update(shaft.handles)

    # Everything else is grouped by its span along the machine axis.  A
    # feature running nearly the whole plate is the machine's own outline
    # profile, not a component, and would merge every band into one.
    remaining = [
        f
        for f in usable
        if not (set(f.handles) & consumed)
        and (f.bounds[axis + 2] - f.bounds[axis]) <= axis_span * 0.78
    ]
    # A driver is drawn as its body plus fin bands, terminal box and fan
    # cowl, all sharing the same span along the machine axis.  Merging on
    # that shared span rebuilds the one machine without hard-coding what a
    # motor looks like; a low threshold here leaves it in pieces.  Bands
    # whose cross extent nearly spans the plate belong to the machine's own
    # outline rather than to one component, and are kept separate so they
    # cannot inflate the driver envelope.
    remaining = [
        f
        for f in remaining
        if (f.bounds[cross + 2] - f.bounds[cross]) < cross_span * 0.88
    ]
    bands = _merge_overlapping(remaining, axis=axis, tol=0.30)
    # Post-merge guard: a band that now spans nearly the whole machine is
    # the machine's own side profile, not one component (204-PU-003 draws
    # full-height flanks that chained every section into a single blob).
    bands = [
        band
        for band in bands
        if (band[0][axis + 2] - band[0][axis]) <= axis_span * 0.88
        and (band[0][cross + 2] - band[0][cross]) < cross_span * 0.88
    ]

    for bounds, handles, members in bands:
        centre = (bounds[axis] + bounds[axis + 2]) / 2.0
        extent = bounds[axis + 2] - bounds[axis]
        cross_extent = bounds[cross + 2] - bounds[cross]
        # Distance from the driver end, normalised over the plate.
        position = abs(centre - driver_end) / axis_span if axis_span else 0.0

        if cross_extent < cross_span * 0.14 and extent < axis_span * 0.12:
            kind = ComponentKind.AUXILIARY
            confidence = Confidence.LOW
            reason = f"small fitting {bounds[2]-bounds[0]:.0f}x{bounds[3]-bounds[1]:.0f}"
        elif position < 0.42 and cross_extent > cross_span * 0.35:
            kind = ComponentKind.MOTOR
            confidence = Confidence.HIGH
            reason = (
                f"large body {extent:.0f} mm along the machine axis at the "
                f"driver end, spanning {cross_extent:.0f} mm across the "
                f"baseplate ({len(members)} drawn feature(s) merged)"
            )
        elif position < 0.62:
            kind = ComponentKind.BEARING_HOUSING
            confidence = Confidence.MEDIUM
            reason = (
                f"body {extent:.0f}x{cross_extent:.0f} between the driver and "
                f"the coupling, the bearing/adapter position"
            )
        elif position < 0.80:
            kind = ComponentKind.COUPLING_GUARD
            confidence = Confidence.MEDIUM
            reason = (
                f"body {extent:.0f}x{cross_extent:.0f} spanning the gap between "
                f"driver and wet end, the coupling guard position"
            )
        else:
            kind = ComponentKind.AUXILIARY
            confidence = Confidence.LOW
            reason = (
                f"body {extent:.0f}x{cross_extent:.0f} at the wet end, outboard "
                f"of the casing"
            )

        parts.append(
            AssembledPart(
                kind=kind,
                bounds=bounds,
                confidence=confidence,
                reason=reason,
                handles=handles,
                points=(
                    list(members[0].points)
                    if len(members) == 1
                    else []
                ),
            )
        )

    # A pump has one driver.  Bands that all read as "motor" are the body,
    # its fin sections and its fan cowl drawn separately, so they are
    # consolidated into a single machine rather than emitted as three
    # motors each with its own fins and feet.
    for unique_kind, description in (
        (ComponentKind.MOTOR, "body, fin bands, cowl"),
        (ComponentKind.BEARING_HOUSING, "housing sections"),
    ):
        group = [p for p in parts if p.kind is unique_kind]
        if len(group) <= 1:
            continue
        merged_bounds = (
            min(p.bounds[0] for p in group),
            min(p.bounds[1] for p in group),
            max(p.bounds[2] for p in group),
            max(p.bounds[3] for p in group),
        )
        merged_handles: List[str] = []
        for part in group:
            merged_handles.extend(part.handles)
        parts = [p for p in parts if p.kind is not unique_kind]
        span = merged_bounds[axis + 2] - merged_bounds[axis]
        across = merged_bounds[cross + 2] - merged_bounds[cross]
        parts.insert(
            0,
            AssembledPart(
                kind=unique_kind,
                bounds=merged_bounds,
                confidence=Confidence.HIGH,
                reason=(
                    f"{unique_kind.value} assembly {span:.0f} mm along the "
                    f"machine axis x {across:.0f} mm across, consolidated from "
                    f"{len(group)} drawn sections ({description})"
                ),
                handles=merged_handles,
            ),
        )

    if not any(part.kind is ComponentKind.MOTOR for part in parts):
        # Some drawings give the driver only as a full-height machine flank
        # pair with no closed motor outline (203-PU-008).  The flank width
        # is drawn evidence of the motor diameter; the axial length is not
        # dimensioned, so it is inferred as the driver-end third and the
        # component is reported at LOW confidence rather than silently
        # dropped.
        flanks = [
            feature
            for feature in usable
            if (feature.bounds[axis + 2] - feature.bounds[axis]) > axis_span * 0.75
            and (feature.bounds[cross + 2] - feature.bounds[cross])
            < cross_span * 0.55
        ]
        if flanks:
            flank = max(
                flanks, key=lambda f: f.bounds[cross + 2] - f.bounds[cross]
            )
            across = flank.bounds[cross + 2] - flank.bounds[cross]
            length = axis_span * 0.36
            if wet_sign > 0:
                along_lo, along_hi = axis_lo, axis_lo + length
            else:
                along_lo, along_hi = axis_hi - length, axis_hi
            cross_lo = plate_cross - across / 2.0
            cross_hi = plate_cross + across / 2.0
            if axis == 0:
                bounds = (along_lo, cross_lo, along_hi, cross_hi)
            else:
                bounds = (cross_lo, along_lo, cross_hi, along_hi)
            parts.insert(
                0,
                AssembledPart(
                    kind=ComponentKind.MOTOR,
                    bounds=bounds,
                    confidence=Confidence.LOW,
                    reason=(
                        f"motor width {across:.0f} mm measured from the "
                        f"full-height machine flank pair; axial length "
                        f"{length:.0f} mm is an inferred Reference Value "
                        f"(no closed driver outline is drawn)"
                    ),
                    handles=list(flank.handles),
                ),
            )

    if shaft is not None:
        parts.append(
            AssembledPart(
                kind=ComponentKind.COUPLING,
                bounds=shaft.bounds,
                confidence=Confidence.HIGH,
                reason=(
                    f"shaft/coupling: {shaft.detail}; drawn on the machine "
                    f"centreline between driver and casing"
                ),
                handles=shaft.handles,
                round_axis=long_axis,
                radius=(shaft.radii[0] if shaft.radii else None),
            )
        )

    if casing is not None:
        parts.append(
            AssembledPart(
                kind=ComponentKind.PUMP_CASING,
                bounds=casing.bounds,
                confidence=Confidence.HIGH,
                reason=(
                    f"volute: {casing.detail}; the only large round feature in "
                    f"the plan, at the wet end"
                ),
                handles=casing.handles,
                round_axis="z",
                radius=max(casing.radii),
                radii=list(casing.radii),
            )
        )
    else:
        # No concentric circle group: the wet end is drawn with open
        # linework.  The largest compact body in the outer half toward the
        # wet end is the casing envelope.  "Compact" excludes the slivers
        # that a pure furthest-body rule once promoted (340x16), and the
        # wet-end anchor keeps the driver from being picked on pumps whose
        # wet end has no round feature at all.
        candidates = []
        for part in parts:
            if part.kind not in (
                ComponentKind.AUXILIARY,
                ComponentKind.COUPLING_GUARD,
            ):
                continue
            extent = part.bounds[axis + 2] - part.bounds[axis]
            cross_extent = part.bounds[cross + 2] - part.bounds[cross]
            if min(extent, cross_extent) < axis_span * 0.08:
                continue
            if min(extent, cross_extent) < max(extent, cross_extent) * 0.25:
                continue
            centre = (part.bounds[axis] + part.bounds[axis + 2]) / 2.0
            if abs(centre - wet_edge) < axis_span * 0.30:
                candidates.append(part)
        if candidates:
            # Prefer the roundest compact body; a 652x210 cover plate is
            # not a volute when a 232x210 body is also present.  On MC pumps
            # the outboard separator vessel is deliberately skipped (it is
            # bigger than the casing itself and classified as auxiliary).
            compact = []
            for part in candidates:
                if is_mc and part.size[cross] > cross_span * 0.50:
                    continue
                compact.append(part)
            casing_part = max(
                compact or candidates,
                # The volute is the *large* wet-end envelope; preferring
                # roundness over size crowned the small top-discharge boss
                # (334x172) as the casing while the drawn 652x210 volute
                # band sat beside it as "auxiliary" - the exact "twisted
                # main body" failure the client flagged.
                key=lambda p: p.size[0] * p.size[1],
            )
            extent = casing_part.bounds[axis + 2] - casing_part.bounds[axis]
            cross_extent = casing_part.bounds[cross + 2] - casing_part.bounds[cross]
            parts.remove(casing_part)
            parts.append(
                AssembledPart(
                    kind=ComponentKind.PUMP_CASING,
                    bounds=casing_part.bounds,
                    confidence=Confidence.MEDIUM,
                    reason=(
                        f"compact body {extent:.0f}x{cross_extent:.0f} at the "
                        f"wet end; no concentric circle group was drawn, so the "
                        f"volute envelope is taken from the largest compact "
                        f"wet-end body"
                    ),
                    handles=list(casing_part.handles),
                    points=list(casing_part.points),
                )
            )
        else:
            warnings.append(
                "no concentric circle group or compact wet-end body found; "
                "the casing could not be identified from this plan"
            )

    return parts, warnings


def assemble_elevation(
    features: Sequence[Feature],
    outline: Tuple[float, float, float, float],
) -> Tuple[List[AssembledPart], List[str]]:
    """Assemble a vertical pump seen from the side.

    Components stack along the drawing's vertical axis.  Nearly every
    body here is a solid of revolution, so a feature's horizontal extent
    is a diameter and its vertical extent is a true measured height.
    """
    parts: List[AssembledPart] = []
    warnings: List[str] = []

    ox0, oy0, ox1, oy1 = outline
    vertical_is_y = (oy1 - oy0) >= (ox1 - ox0)
    v = 1 if vertical_is_y else 0  # index of the vertical axis
    h = 1 - v
    v_lo, v_hi = outline[v], outline[v + 2]
    v_span = v_hi - v_lo
    centreline = (outline[h] + outline[h + 2]) / 2.0

    usable = [f for f in features if _significant(f)]
    if not usable:
        warnings.append("no features large enough to model")
        return parts, warnings

    # A vertical pump is often drawn with a full-height side profile down
    # each flank.  Those describe the whole machine's silhouette rather than
    # any one component, and merging on them chains every band into a single
    # blob - which collapsed several pumps to two solids.
    spanning = [
        f for f in usable if (f.bounds[v + 2] - f.bounds[v]) > v_span * 0.85
    ]
    stacked = [f for f in usable if f not in spanning]
    if not stacked:
        stacked = usable
        warnings.append(
            "every feature spans the full height; the pump could not be "
            "resolved into stacked components"
        )

    # Require a strong shared span before merging: on an elevation the
    # components are stacked, so a low threshold chains the whole machine
    # into one band through incidental overlaps at the joints.
    bands = _merge_overlapping(stacked, axis=v, tol=0.75)
    bands.sort(key=lambda b: b[0][v], reverse=True)

    # Height fractions must be measured against the machine's own extent,
    # not the dimensioned outline: the drawn envelope usually includes
    # clearance above and below, which shifts every band's fraction and
    # mislabels the shaft as part of the driver.
    machine_lo = min(b[0][v] for b in bands)
    machine_hi = max(b[0][v + 2] for b in bands)
    machine_span = machine_hi - machine_lo or v_span or 1.0

    # A slender body on the centreline is a shaft, whatever height it sits
    # at; diameter relative to the widest body is what identifies it.
    widest = max((b[0][h + 2] - b[0][h]) for b in bands) or 1.0

    for bounds, handles, members in bands:
        low = bounds[v] - v_lo
        high = bounds[v + 2] - v_lo
        centre = (bounds[v] + bounds[v + 2]) / 2.0
        fraction = (centre - machine_lo) / machine_span
        height = high - low
        diameter = bounds[h + 2] - bounds[h]

        if (
            diameter < widest * 0.30
            and height > diameter * 1.4
            and abs(((bounds[h] + bounds[h + 2]) / 2.0) - centreline)
            < widest * 0.2
        ):
            parts.append(
                AssembledPart(
                    kind=ComponentKind.COUPLING,
                    bounds=bounds,
                    confidence=Confidence.HIGH,
                    reason=(
                        f"slender body {diameter:.0f} dia x {height:.0f} high on "
                        f"the machine centreline - the shaft/coupling spool"
                    ),
                    handles=handles,
                    round_axis="z",
                    radius=diameter / 2.0,
                )
            )
            continue

        if fraction > 0.74:
            kind = ComponentKind.MOTOR
            confidence = Confidence.HIGH
            reason = (
                f"body {diameter:.0f} dia x {height:.0f} high in the top "
                f"quarter of the elevation - the driver on a vertical pump "
                f"({len(members)} drawn feature(s) merged)"
            )
        elif fraction > 0.52:
            kind = ComponentKind.COUPLING_GUARD
            confidence = Confidence.MEDIUM
            reason = (
                f"body {diameter:.0f} dia x {height:.0f} high below the driver "
                f"- the lantern/coupling housing"
            )
        elif fraction > 0.30:
            kind = ComponentKind.COLUMN
            confidence = Confidence.MEDIUM
            reason = (
                f"body {diameter:.0f} dia x {height:.0f} high spanning the "
                f"mid-height - the column/support barrel"
            )
        elif fraction > 0.14:
            kind = ComponentKind.BEARING_HOUSING
            confidence = Confidence.MEDIUM
            reason = (
                f"body {diameter:.0f} dia x {height:.0f} high above the wet end "
                f"- the bearing/stuffing box position"
            )
        else:
            kind = ComponentKind.PUMP_CASING
            confidence = Confidence.HIGH
            reason = (
                f"body {diameter:.0f} dia x {height:.0f} high at the bottom of "
                f"the elevation - the wet end"
            )

        parts.append(
            AssembledPart(
                kind=kind,
                bounds=bounds,
                confidence=confidence,
                reason=reason,
                handles=handles,
                round_axis="z",
                radius=diameter / 2.0,
            )
        )

    return parts, warnings
