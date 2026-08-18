"""
Whole-assembly reconstruction.
==============================

A drawing is not one pump.  It is a pump *set*: the machine, its
baseplate, the suction and discharge pipework, elbows, reducers, flanges,
bolting and supports.  Earlier stages reduced each drawing to a single
revolved body, which threw all of that away.

This module takes the opposite approach.  It makes no assumption about
what a pump looks like.  Instead it:

1. removes annotation (the dimension rectangle and its witness lines);
2. finds every closed region in the remaining linework;
3. gives each region a solid of its own, revolved about the local axis
   of symmetry when it has one and extruded when it does not;
4. keeps whatever is left as open profile detail.

The result is that a suction elbow becomes an elbow, a valve becomes a
valve, and a bolt head becomes a bolt head - because each is a distinct
closed region in the drawing, not because the code knows what those
things are.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from .contours import Contour, ShapeKind, detect_contours
from .profile import strip_annotation
from .source import RawCadEntity

__all__ = ["Region", "AssemblyModel", "decompose"]

#: Regions smaller than this in both directions are drawing detail
#: (hatch ticks, weld symbols) rather than modellable geometry.
MIN_REGION_MM = 14.0

#: A region is treated as a body of revolution when its own linework is
#: symmetric about its centre to within this fraction of its width.
SYMMETRY_TOL = 0.12


@dataclass
class Region:
    """One closed region of the drawing: a single physical part."""

    bounds: Tuple[float, float, float, float]
    handles: List[str] = field(default_factory=list)
    #: Silhouette as (axis position, half-width) pairs, measured from the
    #: region's own linework.  This is what gets revolved or extruded.
    profile: List[Tuple[float, float]] = field(default_factory=list)
    #: "v" when the part's axis runs up the drawing, "h" when across.
    axis: str = "v"
    revolve: bool = True
    kind: str = "part"
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


@dataclass
class AssemblyModel:
    """Every part the drawing contains."""

    regions: List[Region] = field(default_factory=list)
    outline: Optional[Tuple[float, float, float, float]] = None
    annotation_handles: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    @property
    def bounds(self) -> Optional[Tuple[float, float, float, float]]:
        if not self.regions:
            return None
        return (
            min(r.bounds[0] for r in self.regions),
            min(r.bounds[1] for r in self.regions),
            max(r.bounds[2] for r in self.regions),
            max(r.bounds[3] for r in self.regions),
        )


def _local_profile(
    entities: Sequence[RawCadEntity],
    bounds: Tuple[float, float, float, float],
    axis: str,
    *,
    samples: int = 40,
) -> List[Tuple[float, float]]:
    """Silhouette of the linework inside ``bounds``.

    Returns (position along the axis, half-width) pairs.  Measuring the
    part's own outline keeps its tapers and steps instead of flattening
    it to a bounding box.
    """
    x0, y0, x1, y1 = bounds
    vertical = axis == "v"
    lo, hi = (y0, y1) if vertical else (x0, x1)
    if hi - lo <= 1e-6:
        return []
    centre = ((x0 + x1) / 2.0) if vertical else ((y0 + y1) / 2.0)

    profile: List[Tuple[float, float]] = []
    for index in range(samples + 1):
        level = lo + (hi - lo) * index / samples
        best = 0.0
        for entity in entities:
            if vertical:
                a, b = entity.start.y, entity.end.y
                pa, pb = entity.start.x, entity.end.x
            else:
                a, b = entity.start.x, entity.end.x
                pa, pb = entity.start.y, entity.end.y
            low, high = (a, b) if a <= b else (b, a)
            if level < low - 1e-9 or level > high + 1e-9:
                continue
            if abs(b - a) < 1e-9:
                candidates = (pa, pb)
            else:
                t = (level - a) / (b - a)
                candidates = (pa + t * (pb - pa),)
            for value in candidates:
                best = max(best, abs(value - centre))
        profile.append((level - lo, best))
    return profile


def _is_symmetric(
    entities: Sequence[RawCadEntity],
    bounds: Tuple[float, float, float, float],
    axis: str,
) -> bool:
    """Does the part's linework mirror about its own centreline?

    A body of revolution drawn in section is symmetric; a bracket, foot or
    elbow is not.  Deciding this from the drawing avoids revolving things
    that are not round.
    """
    x0, y0, x1, y1 = bounds
    vertical = axis == "v"
    centre = ((x0 + x1) / 2.0) if vertical else ((y0 + y1) / 2.0)
    width = (x1 - x0) if vertical else (y1 - y0)
    if width <= 1e-6:
        return False

    left = right = 0
    for entity in entities:
        for point in (entity.start, entity.end):
            value = point.x if vertical else point.y
            if value < centre - width * 0.05:
                left += 1
            elif value > centre + width * 0.05:
                right += 1
    if left + right == 0:
        return False
    balance = abs(left - right) / float(left + right)
    return balance <= SYMMETRY_TOL * 3.0


def _entities_within(
    entities: Sequence[RawCadEntity],
    bounds: Tuple[float, float, float, float],
    *,
    slack: float = 1.0,
) -> List[RawCadEntity]:
    x0, y0, x1, y1 = bounds
    inside: List[RawCadEntity] = []
    for entity in entities:
        ex0 = min(entity.start.x, entity.end.x)
        ex1 = max(entity.start.x, entity.end.x)
        ey0 = min(entity.start.y, entity.end.y)
        ey1 = max(entity.start.y, entity.end.y)
        if (
            ex0 >= x0 - slack
            and ex1 <= x1 + slack
            and ey0 >= y0 - slack
            and ey1 <= y1 + slack
        ):
            inside.append(entity)
    return inside


def decompose(
    entities: Sequence[RawCadEntity],
    outline: Optional[Tuple[float, float, float, float]],
) -> AssemblyModel:
    """Break a drawing into every part it contains."""
    model = AssemblyModel(outline=outline)

    machine = list(entities)
    if outline is not None:
        machine = strip_annotation(entities, outline)
        removed = len(entities) - len(machine)
        if removed:
            model.notes.append(
                f"removed {removed} annotation segment(s) lying on the "
                f"dimension rectangle"
            )

    if not machine:
        model.notes.append("no machine linework after annotation removal")
        return model

    contours, _ = detect_contours(machine)

    # Open profiles carry most of the assembly.  A mechanical drawing
    # closes a contour only where the draughtsman happened to; a half
    # section, a bracket seen edge-on and an elbow's two flanks are all
    # open, and taking only closed contours discarded them - which is why
    # a 440-line drawing produced eight parts.
    candidates = [
        c
        for c in contours
        if max(c.size) >= MIN_REGION_MM
        and (c.closed or (min(c.size) >= MIN_REGION_MM * 0.5))
    ]

    for contour in candidates:
        width, height = contour.size
        if max(width, height) < MIN_REGION_MM:
            continue
        axis = "v" if height >= width else "h"
        inside = _entities_within(machine, contour.bounds)
        if not inside:
            inside = [
                e for e in machine if e.handle in set(contour.handles)
            ]
        profile = _local_profile(inside, contour.bounds, axis)
        revolve = contour.kind is ShapeKind.CIRCLE or _is_symmetric(
            inside, contour.bounds, axis
        )
        model.regions.append(
            Region(
                bounds=contour.bounds,
                handles=list(contour.handles),
                profile=profile,
                axis=axis,
                revolve=revolve,
                kind=(
                    "disc"
                    if contour.kind is ShapeKind.CIRCLE
                    else ("region" if contour.closed else "profile")
                ),
                detail=(
                    f"{'closed' if contour.closed else 'open'} "
                    f"{contour.kind.value} {width:.0f}x{height:.0f}, "
                    f"{'revolved' if revolve else 'extruded'} about its "
                    f"{'vertical' if axis == 'v' else 'horizontal'} axis"
                ),
            )
        )

    model.regions = _pair_mirrored_flanks(model.regions)
    model.regions.sort(key=lambda r: r.area, reverse=True)
    model.notes.append(
        f"{len(model.regions)} part(s) modelled from {len(machine)} machine segments"
    )
    return model


def _pair_mirrored_flanks(regions: List[Region]) -> List[Region]:
    """Fuse the two sides of a body drawn in section into one part.

    A cylinder seen from the side is drawn as two parallel flanks.  Taken
    separately they become two thin solids standing apart at the body's
    own diameter - which is exactly the "scattered parts" failure: a
    column 415 mm across appeared as two cylinders 415 mm apart instead
    of one cylinder 415 mm in diameter.

    Two regions pair when they occupy the same band along the machine
    axis, have similar extent, and sit on opposite sides of the midline
    between them.
    """
    used: set = set()
    fused: List[Region] = []

    for i, first in enumerate(regions):
        if i in used:
            continue
        partner: Optional[int] = None
        for j in range(i + 1, len(regions)):
            if j in used:
                continue
            second = regions[j]
            if first.axis != second.axis:
                continue
            vertical = first.axis == "v"
            # Extent along the part's own axis must match.
            a_lo, a_hi = (
                (first.bounds[1], first.bounds[3])
                if vertical
                else (first.bounds[0], first.bounds[2])
            )
            b_lo, b_hi = (
                (second.bounds[1], second.bounds[3])
                if vertical
                else (second.bounds[0], second.bounds[2])
            )
            length = a_hi - a_lo
            if length <= 1e-6:
                continue
            if abs((b_hi - b_lo) - length) > length * 0.12:
                continue
            overlap = min(a_hi, b_hi) - max(a_lo, b_lo)
            if overlap < length * 0.8:
                continue
            # Must be thin and separated across the axis.
            a_w = first.size[0] if vertical else first.size[1]
            b_w = second.size[0] if vertical else second.size[1]
            a_c = (
                (first.bounds[0] + first.bounds[2]) / 2.0
                if vertical
                else (first.bounds[1] + first.bounds[3]) / 2.0
            )
            b_c = (
                (second.bounds[0] + second.bounds[2]) / 2.0
                if vertical
                else (second.bounds[1] + second.bounds[3]) / 2.0
            )
            gap = abs(a_c - b_c)
            if gap < max(a_w, b_w) * 1.2:
                continue
            if abs(a_w - b_w) > max(a_w, b_w) * 0.5:
                continue
            partner = j
            break

        if partner is None:
            fused.append(first)
            continue

        second = regions[partner]
        used.add(partner)
        merged = (
            min(first.bounds[0], second.bounds[0]),
            min(first.bounds[1], second.bounds[1]),
            max(first.bounds[2], second.bounds[2]),
            max(first.bounds[3], second.bounds[3]),
        )
        width = (
            merged[2] - merged[0] if first.axis == "v" else merged[3] - merged[1]
        )
        length = (
            merged[3] - merged[1] if first.axis == "v" else merged[2] - merged[0]
        )
        fused.append(
            Region(
                bounds=merged,
                handles=list(first.handles) + list(second.handles),
                profile=[(0.0, width / 2.0), (length, width / 2.0)],
                axis=first.axis,
                revolve=True,
                kind="body",
                detail=(
                    f"body {width:.0f} dia x {length:.0f} long, fused from the "
                    f"two flanks it is drawn with in section"
                ),
            )
        )

    return fused
