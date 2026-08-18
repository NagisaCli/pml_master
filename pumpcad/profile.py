"""
Revolution profiles from elevation linework.
============================================

A vertical pump is a body of revolution.  Its elevation therefore *is*
the profile: the distance from the machine centreline to the outermost
line, sampled up the drawing, gives radius against height.  Revolving
that curve reproduces every taper, step and flare the draughtsman drew.

This replaces the earlier approach of reducing each component to a
bounding box and extruding it, which discarded exactly the curve detail
that makes a pump look like a pump.

Two classes of linework must be removed first or they dominate the
silhouette:

``dimension rectangle``
    The dimensioned outline is an annotation.  On 205-PU-013 it made the
    profile a flat 380 mm at every height - a featureless drum.

``leader and witness lines``
    Long thin strokes running to dimension text, outside the machine.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple

from .source import RawCadEntity

__all__ = [
    "ProfilePoint",
    "RevolutionProfile",
    "strip_annotation",
    "extract_profile",
]


@dataclass(frozen=True)
class ProfilePoint:
    """One sample of the silhouette: ``radius`` at ``height``."""

    height: float
    radius: float


@dataclass
class RevolutionProfile:
    """A pump's silhouette as radius against height, in millimetres.

    ``points`` runs from the bottom of the machine upwards.  Heights are
    relative to the lowest drawn geometry, so the profile can be planted
    on a baseplate without further arithmetic.
    """

    points: List[ProfilePoint] = field(default_factory=list)
    centreline: float = 0.0
    source_height: float = 0.0
    handles: List[str] = field(default_factory=list)

    @property
    def height(self) -> float:
        return self.points[-1].height - self.points[0].height if self.points else 0.0

    @property
    def max_radius(self) -> float:
        return max((p.radius for p in self.points), default=0.0)

    def simplified(self, tolerance: float = 4.0) -> "RevolutionProfile":
        """Drop samples that lie on the straight line between neighbours.

        Keeps every corner - the steps and tapers that define the shape -
        while removing redundant collinear samples.
        """
        if len(self.points) < 3:
            return self
        kept = [self.points[0]]
        for previous, current, following in zip(
            self.points, self.points[1:], self.points[2:]
        ):
            span = following.height - previous.height
            if abs(span) < 1e-9:
                continue
            t = (current.height - previous.height) / span
            interpolated = previous.radius + t * (following.radius - previous.radius)
            if abs(current.radius - interpolated) > tolerance:
                kept.append(current)
        kept.append(self.points[-1])
        return RevolutionProfile(
            points=kept,
            centreline=self.centreline,
            source_height=self.source_height,
            handles=list(self.handles),
        )


def strip_annotation(
    entities: Sequence[RawCadEntity],
    outline: Tuple[float, float, float, float],
    *,
    tol: float = 2.0,
) -> List[RawCadEntity]:
    """Remove the dimension rectangle and its witness lines.

    A segment is annotation when it lies along an outline edge.  Keeping
    it makes the revolved profile a featureless drum the width of the
    dimension, which is what went wrong before.
    """
    x0, y0, x1, y1 = outline
    kept: List[RawCadEntity] = []
    for entity in entities:
        on_left = abs(entity.start.x - x0) < tol and abs(entity.end.x - x0) < tol
        on_right = abs(entity.start.x - x1) < tol and abs(entity.end.x - x1) < tol
        on_bottom = abs(entity.start.y - y0) < tol and abs(entity.end.y - y0) < tol
        on_top = abs(entity.start.y - y1) < tol and abs(entity.end.y - y1) < tol
        if on_left or on_right or on_bottom or on_top:
            continue
        kept.append(entity)
    return kept


def _span_at(entity: RawCadEntity, level: float, *, vertical: bool) -> List[float]:
    """Where ``entity`` crosses ``level``, in the transverse direction."""
    if vertical:
        a, b = entity.start.y, entity.end.y
        pa, pb = entity.start.x, entity.end.x
    else:
        a, b = entity.start.x, entity.end.x
        pa, pb = entity.start.y, entity.end.y

    low, high = (a, b) if a <= b else (b, a)
    if level < low - 1e-9 or level > high + 1e-9:
        return []
    if abs(b - a) < 1e-9:
        # The segment lies in this level: both ends count.
        return [pa, pb]
    t = (level - a) / (b - a)
    return [pa + t * (pb - pa)]


def extract_profile(
    entities: Sequence[RawCadEntity],
    outline: Tuple[float, float, float, float],
    *,
    samples: int = 96,
    vertical: bool = True,
) -> Optional[RevolutionProfile]:
    """Measure the silhouette of an elevation as radius against height.

    ``vertical`` selects which drawing axis is the machine axis: ``True``
    for a pump drawn standing up (the usual case), ``False`` for one
    drawn lying down.

    Returns ``None`` when the linework cannot support a profile.
    """
    machine = strip_annotation(entities, outline)
    if not machine:
        return None

    if vertical:
        axis_values = [v for e in machine for v in (e.start.y, e.end.y)]
        cross_values = [v for e in machine for v in (e.start.x, e.end.x)]
    else:
        axis_values = [v for e in machine for v in (e.start.x, e.end.x)]
        cross_values = [v for e in machine for v in (e.start.y, e.end.y)]

    low, high = min(axis_values), max(axis_values)
    if high - low <= 1e-6:
        return None

    # The centreline is where the machine is symmetric, which is the
    # midpoint of its own geometry rather than of the dimension box.
    centreline = (min(cross_values) + max(cross_values)) / 2.0

    points: List[ProfilePoint] = []
    for index in range(samples + 1):
        level = low + (high - low) * index / samples
        radius = 0.0
        for entity in machine:
            for position in _span_at(entity, level, vertical=vertical):
                radius = max(radius, abs(position - centreline))
        points.append(ProfilePoint(height=level - low, radius=radius))

    # A profile of nothing but zeros carries no shape.
    if max(p.radius for p in points) <= 1e-6:
        return None

    return RevolutionProfile(
        points=points,
        centreline=centreline,
        source_height=high - low,
        handles=[e.handle for e in machine],
    )
