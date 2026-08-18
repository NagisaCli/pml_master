"""
Semantic interpretation of pump CAD linework.
=============================================

Turns detected contours into a ``PumpSemanticModel``: named physical
components with a confidence and a stated reason, each traceable back to
the CAD handles that produced it.

Two facts about this data set drive the design:

1. Every drawing in the export is a **top view** of a horizontal pump.
   The JSON carries this explicitly (``reference_top_view``), and the
   client re-confirmed it on 2026-08-13: the plan view is the strict
   modelling reference.  An outline that is taller than it is wide is
   therefore a North/South pump seen from above, not an elevation.
2. Curves arrive pre-tessellated, so circles are recovered geometrically
   rather than read from the file.

Nothing here fabricates a component.  When the evidence is weak the
candidate is recorded with LOW confidence, or skipped with a reason.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence, Tuple

from .contours import Contour, ShapeKind, detect_contours, find_outline_rectangle
from .source import (
    CLIENT_LONGITUDINAL_AXIS,
    CadPoint,
    PumpRecord,
    SkippedEntity,
)

__all__ = [
    "ViewType",
    "Confidence",
    "ComponentKind",
    "Component",
    "PumpSemanticModel",
    "classify_view",
    "build_semantic_model",
]


class ViewType(str, Enum):
    """Which projection the drawing represents."""

    PLAN = "plan"
    ELEVATION = "elevation"
    UNKNOWN = "unknown"


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ComponentKind(str, Enum):
    BASEPLATE = "BasePlate"
    PUMP_CASING = "PumpCasing"
    MOTOR = "Motor"
    BEARING_HOUSING = "BearingHousing"
    COUPLING = "Coupling"
    COUPLING_GUARD = "CouplingGuard"
    SUCTION = "Suction"
    DISCHARGE = "Discharge"
    SUPPORT = "Support"
    COLUMN = "Column"
    AUXILIARY = "Auxiliary"


@dataclass
class Component:
    """One inferred physical component.

    ``bounds`` and ``centre`` are in the **source CAD coordinate space**;
    the transform stage converts them.  Keeping them in source space means
    the reconstruction can always be checked against the original file.
    """

    kind: ComponentKind
    bounds: Tuple[float, float, float, float]
    confidence: Confidence
    reason: str
    handles: List[str] = field(default_factory=list)
    radius: Optional[float] = None
    is_circular: bool = False
    #: Ordered radii when the feature is a stepped concentric stack.
    radii: List[float] = field(default_factory=list)
    #: Axis a body of revolution turns about: "z", "x", "y", or None.
    round_axis: Optional[str] = None
    #: Drawn outline points for a closed polygon silhouette (CAD space).
    points: List[Tuple[float, float]] = field(default_factory=list)

    @property
    def centre(self) -> Tuple[float, float]:
        x0, y0, x1, y1 = self.bounds
        return ((x0 + x1) / 2.0, (y0 + y1) / 2.0)

    @property
    def size(self) -> Tuple[float, float]:
        x0, y0, x1, y1 = self.bounds
        return (x1 - x0, y1 - y0)


@dataclass
class PumpSemanticModel:
    """The intermediate representation between CAD and 3-D geometry."""

    tag: str
    name: str
    source_json: str
    view: ViewType
    view_reason: str
    # Outline of the drawn envelope, in source CAD space.
    outline: Optional[Tuple[float, float, float, float]]
    # The drawing's long axis: "x" or "y" in CAD space.
    long_axis: str
    #: Bounds of *all* linework, which may exceed the dimensioned outline
    #: where a nozzle or pedestal is drawn outside it.
    cad_extent: Optional[Tuple[float, float, float, float]] = None
    components: List[Component] = field(default_factory=list)
    #: Every interpretable feature recovered from the linework, kept so the
    #: audit can show what the drawing contained versus what was modelled.
    features: List[object] = field(default_factory=list)
    skipped: List[SkippedEntity] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)

    def of_kind(self, kind: ComponentKind) -> List[Component]:
        return [c for c in self.components if c.kind is kind]

    def first(self, kind: ComponentKind) -> Optional[Component]:
        found = self.of_kind(kind)
        return found[0] if found else None

    @property
    def outline_size(self) -> Optional[Tuple[float, float]]:
        if self.outline is None:
            return None
        x0, y0, x1, y1 = self.outline
        return (x1 - x0, y1 - y0)


def classify_view(record: PumpRecord, outline: Optional[Tuple[float, float, float, float]]) -> Tuple[ViewType, str]:
    """Decide whether a drawing is a plan or an elevation.

    The JSON's own ``reference_top_view`` field is authoritative for this
    data set: every geometry-bearing file declares a top view and must be
    reconstructed as one.  The geometric aspect-ratio heuristic that
    treated tall outlines as elevations is gone - a North/South pump's
    plan outline is legitimately taller than it is wide.

    The old geometric test survives only as a last-resort fallback for
    files whose declared view field is absent; in that case a drawing
    whose geometry hangs below its outline is conservatively treated as
    unknown rather than silently rotated into the ground.
    """
    declared = (record.reference_top_view or "").strip().lower()
    if declared and declared != "no reference":
        if outline is None:
            return (
                ViewType.PLAN,
                f"declared top view {record.reference_top_view!r}; "
                f"outline will be recovered separately",
            )
        width = outline[2] - outline[0]
        height = outline[3] - outline[1]
        if width <= 0 or height <= 0:
            return ViewType.UNKNOWN, "degenerate outline"
        return (
            ViewType.PLAN,
            f"declared top view {record.reference_top_view!r} governs; "
            f"outline {width:.0f}x{height:.0f} is the baseplate seen from "
            f"above (long side = pump axis, short side = transverse)",
        )

    if outline is None:
        return ViewType.UNKNOWN, "no outline recovered"

    width = outline[2] - outline[0]
    height = outline[3] - outline[1]
    if width <= 0 or height <= 0:
        return ViewType.UNKNOWN, "degenerate outline"

    below = 0.0
    for entity in record.entities:
        for point in (entity.start, entity.end):
            if point.y < outline[1]:
                below = max(below, outline[1] - point.y)

    if below > height * 0.12:
        return (
            ViewType.UNKNOWN,
            f"no declared view and geometry extends {below:.0f} mm below "
            f"the {width:.0f}x{height:.0f} outline; refusing to guess",
        )

    return (
        ViewType.PLAN,
        f"no declared view; outline {width:.0f}x{height:.0f} contains the "
        f"geometry, consistent with a baseplate seen from above",
    )


def _inside(inner: Tuple[float, float, float, float], outer: Tuple[float, float, float, float], slack: float = 5.0) -> bool:
    return (
        inner[0] >= outer[0] - slack
        and inner[1] >= outer[1] - slack
        and inner[2] <= outer[2] + slack
        and inner[3] <= outer[3] + slack
    )


def _classify_plan_components(
    contours: Sequence[Contour],
    outline: Tuple[float, float, float, float],
    long_axis: str,
) -> Tuple[List[Component], List[str]]:
    """Interpret a true plan view of a horizontal pump.

    Layout evidence: the driver sits at one end of the baseplate and the
    casing at the other, with the coupling between them on a shared
    centreline.  Sizes are taken from the contours themselves, never from
    a template.
    """
    components: List[Component] = []
    warnings: List[str] = []

    x0, y0, x1, y1 = outline
    plate_w, plate_h = x1 - x0, y1 - y0
    plate_area = plate_w * plate_h

    components.append(
        Component(
            kind=ComponentKind.BASEPLATE,
            bounds=outline,
            confidence=Confidence.HIGH,
            reason=(
                f"dimensioned outline rectangle {plate_w:.0f}x{plate_h:.0f} "
                f"enclosing all pump geometry"
            ),
        )
    )

    axis_index = 0 if long_axis == "x" else 1
    centre_cross = (y0 + y1) / 2.0 if long_axis == "x" else (x0 + x1) / 2.0

    # Candidate bodies: closed contours meaningfully smaller than the plate
    # but large enough to be a real component.
    bodies: List[Contour] = []
    for contour in contours:
        if not contour.closed:
            continue
        area = contour.area
        if area <= 0 or area >= plate_area * 0.92:
            continue
        if area < plate_area * 0.01:
            continue
        if not _inside(contour.bounds, outline, slack=plate_h * 0.35):
            continue
        bodies.append(contour)

    if not bodies:
        warnings.append(
            "no interior closed contours found; only the baseplate outline "
            "could be reconstructed from this drawing"
        )
        return components, warnings

    bodies.sort(key=lambda c: c.area, reverse=True)

    # Drop contours nested inside a larger body.  A motor is drawn with its
    # terminal box and end-shield detail inside its own outline, and those
    # inner rectangles are not separate machines - taking them as such put
    # the "casing" on top of the motor instead of at the wet end.
    outermost: List[Contour] = []
    for contour in bodies:
        if any(_inside(contour.bounds, kept.bounds, slack=1.0) for kept in outermost):
            continue
        outermost.append(contour)
    bodies = outermost

    # The two largest bodies straddling the centreline are the driver and
    # the casing.  Which is which follows from position along the axis, and
    # is confirmed downstream by the nozzle metadata.
    def along(contour: Contour) -> float:
        return contour.centroid.x if axis_index == 0 else contour.centroid.y

    ranked = bodies[:2] if len(bodies) >= 2 else bodies
    ranked.sort(key=along)

    if len(ranked) == 2:
        first, second = ranked
        components.append(
            Component(
                kind=ComponentKind.MOTOR,
                bounds=first.bounds,
                confidence=Confidence.HIGH,
                reason=(
                    f"largest closed contour {first.size[0]:.0f}x{first.size[1]:.0f} "
                    f"at the driver end of the baseplate, centred on the shaft axis"
                ),
                handles=list(first.handles),
            )
        )
        components.append(
            Component(
                kind=ComponentKind.PUMP_CASING,
                bounds=second.bounds,
                confidence=Confidence.HIGH,
                reason=(
                    f"closed contour {second.size[0]:.0f}x{second.size[1]:.0f} "
                    f"at the wet end opposite the driver"
                ),
                handles=list(second.handles),
                is_circular=second.kind is ShapeKind.CIRCLE,
                radius=second.radius,
            )
        )
    else:
        only = ranked[0]
        components.append(
            Component(
                kind=ComponentKind.MOTOR,
                bounds=only.bounds,
                confidence=Confidence.MEDIUM,
                reason=(
                    f"single large closed contour {only.size[0]:.0f}x"
                    f"{only.size[1]:.0f}; driver/casing split not resolvable"
                ),
                handles=list(only.handles),
            )
        )

    # Remaining bodies between the driver and casing are coupling-related;
    # circles on the shaft axis are shaft/coupling features.
    for contour in bodies[2:]:
        cross = contour.centroid.y if axis_index == 0 else contour.centroid.x
        on_axis = abs(cross - centre_cross) < plate_h * 0.2
        if contour.kind is ShapeKind.CIRCLE and on_axis:
            components.append(
                Component(
                    kind=ComponentKind.COUPLING,
                    bounds=contour.bounds,
                    confidence=Confidence.MEDIUM,
                    reason=(
                        f"circle r={contour.radius:.0f} on the shaft centreline "
                        f"between driver and casing"
                    ),
                    handles=list(contour.handles),
                    is_circular=True,
                    radius=contour.radius,
                )
            )
        elif on_axis:
            components.append(
                Component(
                    kind=ComponentKind.COUPLING_GUARD,
                    bounds=contour.bounds,
                    confidence=Confidence.LOW,
                    reason=(
                        f"small closed contour {contour.size[0]:.0f}x"
                        f"{contour.size[1]:.0f} on the shaft centreline"
                    ),
                    handles=list(contour.handles),
                )
            )
        else:
            components.append(
                Component(
                    kind=ComponentKind.AUXILIARY,
                    bounds=contour.bounds,
                    confidence=Confidence.LOW,
                    reason="closed contour off the shaft centreline",
                    handles=list(contour.handles),
                )
            )

    return components, warnings


def _merge_height_bands(
    contours: Sequence[Contour], *, overlap: float = 0.6
) -> List[Tuple[float, float, float, float, List[str]]]:
    """Merge contours that occupy the same height band into one body.

    On an elevation a single component is routinely drawn as two mirrored
    half profiles, plus separate detail strokes.  Anything sharing a
    height band belongs to the same physical body, so the bands are
    merged and the widest extent across the band becomes its diameter.

    Returns ``(min_x, min_y, max_x, max_y, handles)`` per merged body.
    """
    bands: List[Tuple[float, float, float, float, List[str]]] = []
    for contour in sorted(contours, key=lambda c: c.bounds[1]):
        x0, y0, x1, y1 = contour.bounds
        height = y1 - y0
        placed = False
        for index, (bx0, by0, bx1, by1, handles) in enumerate(bands):
            band_height = by1 - by0
            shared = min(y1, by1) - max(y0, by0)
            if shared <= 0:
                continue
            # Same band when the vertical overlap dominates the smaller body.
            if shared >= min(height, band_height) * overlap:
                bands[index] = (
                    min(bx0, x0),
                    min(by0, y0),
                    max(bx1, x1),
                    max(by1, y1),
                    handles + contour.handles,
                )
                placed = True
                break
        if not placed:
            bands.append((x0, y0, x1, y1, list(contour.handles)))
    return bands


def _classify_elevation_components(
    contours: Sequence[Contour],
    outline: Tuple[float, float, float, float],
) -> Tuple[List[Component], List[str]]:
    """Interpret an elevation of a (usually vertical) pump.

    Here the outline's vertical extent is a **height**.  Components stack
    along it: motor at the top, then coupling/lantern, then the bearing or
    column, then the casing at the bottom.  The horizontal extent gives the
    diameters, which is what constrains the plan footprint.
    """
    components: List[Component] = []
    warnings: List[str] = []

    x0, y0, x1, y1 = outline
    span_x, span_y = x1 - x0, y1 - y0
    outline_area = span_x * span_y

    # A vertical pump is a body of revolution drawn symmetrically about its
    # centreline, so its outline is frequently split into two open half
    # profiles that never close.  Rejecting open paths would discard the
    # motor on most of these drawings, so profiles are accepted on their
    # own merit: a meaningful extent in both directions, inside the
    # envelope, and not a thin annotation stroke.
    min_span = min(span_x, span_y) * 0.06
    bodies: List[Contour] = []
    for contour in contours:
        width, height = contour.size
        if contour.closed:
            if not (outline_area * 0.004 < contour.area < outline_area * 0.9):
                continue
        else:
            # Open profiles must still describe a real body.
            if width < min_span or height < min_span:
                continue
            if width > span_x * 0.98 and height > span_y * 0.98:
                continue  # the envelope itself, drawn open
            if contour.path_length < min_span * 2.0:
                continue
        bodies.append(contour)

    if not bodies:
        warnings.append(
            "elevation contains no usable interior contours; only the "
            "envelope height and width are usable"
        )
        return components, warnings

    bodies = _merge_height_bands(bodies)
    bodies.sort(key=lambda band: band[3], reverse=True)

    # Height bands, from the top of the drawing downwards.
    for index, (bx0, by0, bx1, by1, handles) in enumerate(bodies):
        cy = (by0 + by1) / 2.0
        height_fraction = (cy - y0) / span_y if span_y else 0.0
        width, height = bx1 - bx0, by1 - by0

        if height_fraction > 0.72:
            kind = ComponentKind.MOTOR
            confidence = Confidence.HIGH if index == 0 else Confidence.MEDIUM
            reason = (
                f"contour {width:.0f}x{height:.0f} in the top quarter of the "
                f"elevation, the driver position on a vertical pump"
            )
        elif height_fraction > 0.45:
            kind = ComponentKind.COLUMN
            confidence = Confidence.MEDIUM
            reason = (
                f"contour {width:.0f}x{height:.0f} in the mid-height band "
                f"between driver and casing"
            )
        elif height_fraction > 0.18:
            kind = ComponentKind.BEARING_HOUSING
            confidence = Confidence.MEDIUM
            reason = (
                f"contour {width:.0f}x{height:.0f} below the column and above "
                f"the wet end"
            )
        else:
            kind = ComponentKind.PUMP_CASING
            confidence = Confidence.HIGH
            reason = (
                f"largest low-level contour {width:.0f}x{height:.0f}, the wet "
                f"end at the bottom of a vertical pump"
            )

        components.append(
            Component(
                kind=kind,
                bounds=(bx0, by0, bx1, by1),
                confidence=confidence,
                reason=reason,
                handles=handles,
                is_circular=True,
                radius=width / 2.0,
            )
        )

    return components, warnings


def build_semantic_model(record: PumpRecord) -> PumpSemanticModel:
    """Build the intermediate model for one pump.

    Never raises for geometry reasons: a pump with no usable CAD evidence
    yields a model with no components and an explanatory warning, so the
    batch can continue and the audit can explain the gap.
    """
    model = PumpSemanticModel(
        tag=record.tag,
        name=record.name,
        source_json=record.source_path,
        view=ViewType.UNKNOWN,
        view_reason="",
        outline=None,
        long_axis="x",
        skipped=list(record.skipped),
    )

    if not record.has_geometry:
        model.view_reason = "no CAD geometry in this file"
        model.warnings.append(
            "no shape-reference geometry; the pump must fall back to "
            "metadata-driven geometry"
        )
        return model

    contours, stats = detect_contours(record.entities)
    model.stats = dict(stats)
    model.cad_extent = record.bounds

    outline = find_outline_rectangle(
        record.entities, expect=(record.length_mm, record.width_mm)
    )
    if outline is None:
        outline = find_outline_rectangle(record.entities)
    model.outline = outline

    view, reason = classify_view(record, outline)
    model.view = view
    model.view_reason = reason

    if outline is None:
        model.warnings.append(
            "no dimensioned outline rectangle could be recovered; component "
            "classification was not attempted"
        )
        return model

    span_x = outline[2] - outline[0]
    span_y = outline[3] - outline[1]
    model.long_axis = "x" if span_x >= span_y else "y"

    # Recover the drawn topology - concentric stacks, rail-pair cylinders,
    # profiles - before naming anything.  Classifying raw contours instead
    # discards most of the linework and yields a two-box pump.
    from .assembly import assemble_elevation, assemble_plan
    from .features import extract_features

    features = extract_features(contours, outline=outline)
    model.features = list(features)
    model.stats["features"] = len(features)

    if view is ViewType.PLAN:
        layout_axis = CLIENT_LONGITUDINAL_AXIS.get(
            record.tag, record.inlet_orientation or "E"
        ).upper()
        parts, warnings = assemble_plan(
            features,
            outline,
            model.long_axis,
            layout_axis,
            is_mc=("MC PUMP" in record.name.upper()),
        )
    elif view is ViewType.ELEVATION:
        parts, warnings = assemble_elevation(features, outline)
    else:
        parts, warnings = [], [
            f"view could not be resolved ({model.view_reason}); "
            f"component classification was skipped and the pump falls back "
            f"to metadata-proportioned geometry"
        ]

    for part in parts:
        model.components.append(
            Component(
                kind=part.kind,
                bounds=part.bounds,
                confidence=part.confidence,
                reason=part.reason,
                handles=part.handles,
                is_circular=part.round_axis is not None,
                radius=part.radius,
                radii=list(part.radii),
                round_axis=part.round_axis,
                points=list(part.points),
            )
        )
    model.warnings.extend(warnings)
    return model
