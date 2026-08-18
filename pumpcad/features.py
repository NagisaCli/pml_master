"""
Feature extraction: the drawn topology, not just the envelope.
=============================================================

Contour detection recovers *shapes*; this module recovers what those
shapes mean together.  Three structures carry most of the topology in
these drawings and each needs its own recogniser:

``concentric stacks``
    Circles sharing a centre are one stepped feature - a volute with its
    flange, a hub with its boss - not several unrelated discs.

``parallel rails``
    Two parallel lines with nothing between them are a cylinder seen from
    the side: a shaft, a column, a spool.  Their separation is the
    diameter and their overlap is the length.  Reading them as two thin
    plates instead of one cylinder is the single biggest fidelity loss in
    a naive reconstruction.

``profile bands``
    Contours occupying the same span along the machine axis belong to one
    body, and their combined extent is its true silhouette.

Everything here is measured from the linework.  Where a group cannot be
interpreted it is left for the caller to record as unclassified rather
than being forced into a shape.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .contours import Contour, ShapeKind

__all__ = [
    "FeatureKind",
    "Feature",
    "extract_features",
    "find_concentric_stacks",
    "find_parallel_rails",
]

#: Two circle centres closer than this are the same axis.
CONCENTRIC_TOL = 6.0

#: Rails must be parallel to within this angle (degrees).
RAIL_ANGLE_TOL = 1.0

#: A rail pair's separation must be at least this, else it is a hairline.
MIN_RAIL_SEPARATION = 12.0

#: Rails must overlap along their shared direction by this fraction.
MIN_RAIL_OVERLAP = 0.55


class FeatureKind(str, Enum):
    """What a group of contours physically is."""

    DISC_STACK = "disc_stack"      # concentric circles: volute, flange, hub
    CYLINDER = "cylinder"          # parallel rails: shaft, column, spool
    PRISM = "prism"                # a closed rectangular body
    PROFILE = "profile"            # a closed non-circular silhouette
    PLATE = "plate"                # thin closed rectangle: flange face, foot
    UNCLASSIFIED = "unclassified"


@dataclass
class Feature:
    """One physically meaningful feature recovered from the linework."""

    kind: FeatureKind
    bounds: Tuple[float, float, float, float]
    handles: List[str] = field(default_factory=list)
    #: For DISC_STACK / CYLINDER: the ordered radii or the single radius.
    radii: List[float] = field(default_factory=list)
    centre: Optional[Tuple[float, float]] = None
    #: For CYLINDER: "x" or "y", the direction the cylinder runs.
    axis: Optional[str] = None
    #: Ordered outline points for closed generic contours (rectangles,
    #: polygons, octagonal flanges); empty for fitted circles and rail
    #: pairs, which carry their exact centre/radius instead.
    points: List[Tuple[float, float]] = field(default_factory=list)
    detail: str = ""

    @property
    def size(self) -> Tuple[float, float]:
        x0, y0, x1, y1 = self.bounds
        return (x1 - x0, y1 - y0)

    @property
    def centroid(self) -> Tuple[float, float]:
        x0, y0, x1, y1 = self.bounds
        return ((x0 + x1) / 2.0, (y0 + y1) / 2.0)

    @property
    def area(self) -> float:
        width, height = self.size
        return width * height


def find_concentric_stacks(
    contours: Sequence[Contour], *, tol: float = CONCENTRIC_TOL
) -> Tuple[List[Feature], set]:
    """Group circles sharing a centre into stepped disc features.

    A pump casing in plan is drawn as the volute circle, the flange circle
    and often a hub circle, all on one axis.  Emitting three separate
    cylinders of arbitrary height loses the step; emitting one stack keeps
    it.
    """
    circles = [
        c
        for c in contours
        if c.kind is ShapeKind.CIRCLE and c.centre is not None and c.radius
    ]
    used: set = set()
    features: List[Feature] = []

    groups: List[List[Contour]] = []
    for circle in sorted(circles, key=lambda c: c.radius or 0.0, reverse=True):
        placed = False
        for group in groups:
            head = group[0]
            assert head.centre is not None and circle.centre is not None
            if head.centre.distance_to(circle.centre) <= tol:
                group.append(circle)
                placed = True
                break
        if not placed:
            groups.append([circle])

    for group in groups:
        radii = sorted((c.radius or 0.0) for c in group)
        head = group[0]
        assert head.centre is not None
        handles: List[str] = []
        for circle in group:
            handles.extend(circle.handles)
            used.update(circle.handles)
        cx, cy = head.centre.x, head.centre.y
        outer = radii[-1]
        features.append(
            Feature(
                kind=FeatureKind.DISC_STACK,
                bounds=(cx - outer, cy - outer, cx + outer, cy + outer),
                handles=handles,
                radii=radii,
                centre=(cx, cy),
                detail=(
                    f"{len(radii)} concentric circle(s) on one axis, radii "
                    + ", ".join(f"{r:.0f}" for r in radii)
                ),
            )
        )
    return features, used


def _segment_of(contour: Contour) -> Optional[Tuple[float, float, float, float]]:
    """Reduce a straight 2-point contour to (x0, y0, x1, y1)."""
    if len(contour.points) != 2:
        return None
    a, b = contour.points
    return (a.x, a.y, b.x, b.y)


def find_parallel_rails(
    contours: Sequence[Contour],
    *,
    exclude: Optional[set] = None,
) -> Tuple[List[Feature], set]:
    """Pair axis-aligned rails into cylinders seen from the side.

    Only pairs with nothing drawn between them are accepted, so the two
    flanks of a shaft become one cylinder while the two sides of a large
    hollow body do not get collapsed.
    """
    exclude = exclude or set()
    used: set = set()
    features: List[Feature] = []

    horizontal: List[Tuple[float, float, float, Contour]] = []  # y, x0, x1
    vertical: List[Tuple[float, float, float, Contour]] = []  # x, y0, y1

    for contour in contours:
        if contour.closed or any(h in exclude for h in contour.handles):
            continue
        segment = _segment_of(contour)
        if segment is None:
            continue
        x0, y0, x1, y1 = segment
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        if length < MIN_RAIL_SEPARATION:
            continue
        angle = math.degrees(math.atan2(abs(dy), abs(dx)))
        if angle <= RAIL_ANGLE_TOL:
            horizontal.append(((y0 + y1) / 2.0, min(x0, x1), max(x0, x1), contour))
        elif angle >= 90.0 - RAIL_ANGLE_TOL:
            vertical.append(((x0 + x1) / 2.0, min(y0, y1), max(y0, y1), contour))

    def pair(
        rails: List[Tuple[float, float, float, Contour]], axis: str
    ) -> None:
        taken: set = set()
        ordered = sorted(rails, key=lambda r: r[0])
        for i, (pos_a, lo_a, hi_a, contour_a) in enumerate(ordered):
            if i in taken:
                continue
            best: Optional[Tuple[int, float]] = None
            for j in range(i + 1, len(ordered)):
                if j in taken:
                    continue
                pos_b, lo_b, hi_b, _ = ordered[j]
                separation = abs(pos_b - pos_a)
                if separation < MIN_RAIL_SEPARATION:
                    continue
                overlap = min(hi_a, hi_b) - max(lo_a, lo_b)
                shorter = min(hi_a - lo_a, hi_b - lo_b)
                if shorter <= 0 or overlap < shorter * MIN_RAIL_OVERLAP:
                    continue
                # Nearest qualifying partner wins: a shaft pairs with its own
                # far flank, not with a distant unrelated line.
                if best is None or separation < best[1]:
                    best = (j, separation)
            if best is None:
                continue
            j, separation = best
            pos_b, lo_b, hi_b, contour_b = ordered[j]
            taken.add(i)
            taken.add(j)
            lo = max(lo_a, lo_b)
            hi = min(hi_a, hi_b)
            handles = list(contour_a.handles) + list(contour_b.handles)
            used.update(handles)
            centre_pos = (pos_a + pos_b) / 2.0
            if axis == "x":
                bounds = (lo, centre_pos - separation / 2.0, hi, centre_pos + separation / 2.0)
            else:
                bounds = (centre_pos - separation / 2.0, lo, centre_pos + separation / 2.0, hi)
            features.append(
                Feature(
                    kind=FeatureKind.CYLINDER,
                    bounds=bounds,
                    handles=handles,
                    radii=[separation / 2.0],
                    axis=axis,
                    centre=(
                        (lo + hi) / 2.0 if axis == "x" else centre_pos,
                        centre_pos if axis == "x" else (lo + hi) / 2.0,
                    ),
                    detail=(
                        f"parallel rail pair {separation:.0f} mm apart running "
                        f"{hi - lo:.0f} mm along {axis}, a cylindrical body "
                        f"seen from the side"
                    ),
                )
            )

    pair(horizontal, "x")
    pair(vertical, "y")
    return features, used


def extract_features(
    contours: Sequence[Contour],
    *,
    outline: Optional[Tuple[float, float, float, float]] = None,
) -> List[Feature]:
    """Recover every interpretable feature from a pump's contours.

    Order matters: concentric stacks and rail pairs claim their contours
    first, because those interpretations are strictly more informative
    than treating the same linework as loose shapes.
    """
    features: List[Feature] = []
    claimed: set = set()

    # Identify the outline first so it is excluded from every later pass:
    # its own two sides otherwise pair with each other into a "cylinder"
    # the width of the whole drawing.  Contours are excluded by identity
    # rather than by handle, because handles are only unique per drawing
    # and a shared handle would silently drop unrelated geometry.
    outline_ids: set = set()
    if outline is not None:
        for contour in contours:
            if _matches(contour.bounds, outline, tol=2.5):
                outline_ids.add(id(contour))

    considered = [c for c in contours if id(c) not in outline_ids]

    stacks, used = find_concentric_stacks(considered)
    features.extend(stacks)
    claimed |= used

    rails, used = find_parallel_rails(considered, exclude=claimed)
    features.extend(rails)
    claimed |= used

    for contour in considered:
        if contour.handles and all(handle in claimed for handle in contour.handles):
            continue
        width, height = contour.size
        if width <= 0.5 and height <= 0.5:
            continue

        if contour.closed:
            thin = min(width, height) < max(width, height) * 0.12
            kind = FeatureKind.PLATE if thin else (
                FeatureKind.PRISM
                if contour.kind is ShapeKind.RECTANGLE
                else FeatureKind.PROFILE
            )
            detail = (
                f"closed {contour.kind.value} {width:.0f}x{height:.0f}"
                + (" (thin - a flange face, foot or rib)" if thin else "")
            )
        else:
            kind = FeatureKind.UNCLASSIFIED
            detail = (
                f"open path {width:.0f}x{height:.0f}, "
                f"{len(contour.points)} vertices"
            )

        features.append(
            Feature(
                kind=kind,
                bounds=contour.bounds,
                handles=list(contour.handles),
                radii=[contour.radius] if contour.radius else [],
                centre=(contour.centroid.x, contour.centroid.y),
                points=(
                    [(point.x, point.y) for point in contour.points]
                    if contour.closed and _plausible_polygon(contour)
                    else []
                ),
                detail=detail,
            )
        )
        claimed.update(contour.handles)

    features.sort(key=lambda f: f.area, reverse=True)
    return features


def _matches(
    a: Tuple[float, float, float, float],
    b: Tuple[float, float, float, float],
    *,
    tol: float,
) -> bool:
    return all(abs(a[i] - b[i]) <= tol for i in range(4))


def _plausible_polygon(contour: Contour) -> bool:
    """A closed contour only becomes an EXTRUSION LOOP when its shape can
    have come from a real part rather than a chance bridge of two strokes."""
    width, height = contour.size
    if min(width, height) < 8.0:
        return False
    if min(width, height) < max(width, height) * 0.20:
        return False
    bbox_area = width * height
    if bbox_area <= 0 or contour.area < bbox_area * 0.15:
        return False
    return True
