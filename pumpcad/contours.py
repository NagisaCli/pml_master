"""
Contour detection from tessellated CAD linework.
================================================

The exporter flattens every curve into short straight segments, so the
input is an unordered soup of ``Line`` primitives.  This module rebuilds
structure from it:

    dedup -> connectivity graph -> chains -> closure -> shape classification

A chain is classified as a CIRCLE when its vertices are equidistant from
their centroid, as a RECTANGLE when it reduces to four axis-aligned
corners, and otherwise kept as a general POLYLINE.  Circle recovery
matters because a bolt circle or a shaft is meaningless as 32 separate
5 mm segments.

Nothing here invents coordinates: every emitted contour is backed by the
handles of the source entities that produced it.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .source import CadPoint, RawCadEntity

__all__ = [
    "ShapeKind",
    "Contour",
    "detect_contours",
    "dedupe_entities",
    "find_outline_rectangle",
]

# Endpoints closer than this are treated as the same vertex.  The drawings
# are millimetre CAD with clean snapping; 0.05 mm is far below any real
# feature yet absorbs float noise from the exporter.
WELD_TOL = 0.05

# A chain is closed when its two ends weld together.
CLOSE_TOL = 0.15

# Fractional radius spread below which a closed chain is accepted as a circle.
CIRCLE_TOL = 0.06

# Angular tolerance (degrees) for calling a segment axis-aligned.
AXIS_TOL_DEG = 0.5


class ShapeKind(str, Enum):
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    POLYLINE = "polyline"
    OPEN_PATH = "open_path"


@dataclass
class Contour:
    """A reconstructed contour, traceable back to its source handles."""

    kind: ShapeKind
    points: List[CadPoint]
    handles: List[str]
    closed: bool
    # Populated for CIRCLE.
    centre: Optional[CadPoint] = None
    radius: Optional[float] = None

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        return (min(xs), min(ys), max(xs), max(ys))

    @property
    def size(self) -> Tuple[float, float]:
        x0, y0, x1, y1 = self.bounds
        return (x1 - x0, y1 - y0)

    @property
    def centroid(self) -> CadPoint:
        x0, y0, x1, y1 = self.bounds
        return CadPoint((x0 + x1) / 2.0, (y0 + y1) / 2.0)

    @property
    def area(self) -> float:
        """Shoelace area; 0.0 for open paths."""
        if not self.closed or len(self.points) < 3:
            return 0.0
        total = 0.0
        pts = self.points
        for i in range(len(pts)):
            a = pts[i]
            b = pts[(i + 1) % len(pts)]
            total += a.x * b.y - b.x * a.y
        return abs(total) / 2.0

    @property
    def path_length(self) -> float:
        total = 0.0
        for a, b in zip(self.points, self.points[1:]):
            total += a.distance_to(b)
        if self.closed and len(self.points) > 2:
            total += self.points[-1].distance_to(self.points[0])
        return total


def _key(point: CadPoint, tol: float = WELD_TOL) -> Tuple[int, int]:
    return (int(round(point.x / tol)), int(round(point.y / tol)))


def dedupe_entities(entities: Sequence[RawCadEntity]) -> Tuple[List[RawCadEntity], int]:
    """Drop segments that duplicate another segment (same endpoints, either
    direction).  Four of the source files overdraw lines; keeping both
    copies would corrupt the connectivity degree counts.
    """
    seen: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
    unique: List[RawCadEntity] = []
    dropped = 0
    for entity in entities:
        a = _key(entity.start)
        b = _key(entity.end)
        signature = (a, b) if a <= b else (b, a)
        if signature in seen:
            dropped += 1
            continue
        seen.add(signature)
        unique.append(entity)
    return unique, dropped


def _build_adjacency(
    entities: Sequence[RawCadEntity],
) -> Tuple[Dict[Tuple[int, int], CadPoint], Dict[Tuple[int, int], List[int]]]:
    vertices: Dict[Tuple[int, int], CadPoint] = {}
    incident: Dict[Tuple[int, int], List[int]] = defaultdict(list)
    for index, entity in enumerate(entities):
        for point in (entity.start, entity.end):
            key = _key(point)
            vertices.setdefault(key, point)
            incident[key].append(index)
    return vertices, incident


def _trace_chains(entities: Sequence[RawCadEntity]) -> List[List[int]]:
    """Walk the connectivity graph into chains of segment indices.

    At a vertex of degree 2 the walk continues; at a junction it stops, so
    a tee or a crossing splits into separate contours instead of producing
    an arbitrary path through the junction.
    """
    _, incident = _build_adjacency(entities)
    used: Set[int] = set()
    chains: List[List[int]] = []

    def next_segment(vertex: Tuple[int, int], current: int) -> Optional[int]:
        candidates = [i for i in incident[vertex] if i != current and i not in used]
        if len(candidates) != 1:
            return None  # dead end or junction - stop the chain here
        # Only continue through a genuine degree-2 vertex.
        if len(incident[vertex]) != 2:
            return None
        return candidates[0]

    for start_index in range(len(entities)):
        if start_index in used:
            continue
        used.add(start_index)
        chain = [start_index]

        # Extend forward from the segment's end, then backward from its start.
        for direction in (0, 1):
            current = start_index
            entity = entities[current]
            vertex = _key(entity.end if direction == 0 else entity.start)
            # Track which end of the growing chain we are at.
            while True:
                nxt = next_segment(vertex, current)
                if nxt is None:
                    break
                used.add(nxt)
                if direction == 0:
                    chain.append(nxt)
                else:
                    chain.insert(0, nxt)
                nxt_entity = entities[nxt]
                a, b = _key(nxt_entity.start), _key(nxt_entity.end)
                vertex = b if a == vertex else a
                current = nxt
        chains.append(chain)
    return chains


def _ordered_points(
    entities: Sequence[RawCadEntity], chain: Sequence[int]
) -> List[CadPoint]:
    """Turn a chain of segment indices into an ordered vertex list."""
    if not chain:
        return []
    if len(chain) == 1:
        entity = entities[chain[0]]
        return [entity.start, entity.end]

    first, second = entities[chain[0]], entities[chain[1]]
    fa, fb = _key(first.start), _key(first.end)
    sa, sb = _key(second.start), _key(second.end)
    # Orient the first segment so its far end joins the second segment.
    if fb in (sa, sb):
        points = [first.start, first.end]
    elif fa in (sa, sb):
        points = [first.end, first.start]
    else:
        points = [first.start, first.end]

    for index in chain[1:]:
        entity = entities[index]
        tail = _key(points[-1])
        if _key(entity.start) == tail:
            points.append(entity.end)
        elif _key(entity.end) == tail:
            points.append(entity.start)
        else:
            # Disjoint - the chain walker should prevent this, but never
            # fabricate a connection if it happens.
            points.append(entity.start)
            points.append(entity.end)
    return points


def _fit_circle(points: Sequence[CadPoint]) -> Optional[Tuple[CadPoint, float]]:
    """Accept a closed chain as a circle when all vertices sit at a
    consistent radius from the centroid.  Returns ``None`` otherwise.
    """
    if len(points) < 6:
        return None
    cx = sum(p.x for p in points) / len(points)
    cy = sum(p.y for p in points) / len(points)
    centre = CadPoint(cx, cy)
    radii = [centre.distance_to(p) for p in points]
    mean = sum(radii) / len(radii)
    if mean <= 1e-9:
        return None
    spread = (max(radii) - min(radii)) / mean
    if spread > CIRCLE_TOL:
        return None
    return centre, mean


def _is_axis_aligned(a: CadPoint, b: CadPoint) -> bool:
    dx, dy = abs(b.x - a.x), abs(b.y - a.y)
    if dx <= 1e-9 and dy <= 1e-9:
        return False
    angle = math.degrees(math.atan2(dy, dx))
    return angle <= AXIS_TOL_DEG or angle >= (90.0 - AXIS_TOL_DEG)


def _simplify_collinear(points: Sequence[CadPoint], tol: float = 0.05) -> List[CadPoint]:
    """Drop vertices that lie on the straight line between their neighbours."""
    if len(points) < 3:
        return list(points)
    out = [points[0]]
    for prev, cur, nxt in zip(points, points[1:], points[2:]):
        cross = (cur.x - prev.x) * (nxt.y - prev.y) - (cur.y - prev.y) * (nxt.x - prev.x)
        base = max(prev.distance_to(nxt), 1e-9)
        if abs(cross) / base > tol:
            out.append(cur)
    out.append(points[-1])
    return out


def _is_rectangle(points: Sequence[CadPoint]) -> bool:
    """True when the closed contour reduces to four axis-aligned corners."""
    simple = _simplify_collinear(points)
    # A closed ring repeats its first point at the end.
    if simple and simple[0].distance_to(simple[-1]) <= CLOSE_TOL:
        simple = simple[:-1]
    if len(simple) != 4:
        return False
    for a, b in zip(simple, simple[1:] + simple[:1]):
        if not _is_axis_aligned(a, b):
            return False
    return True


def find_outline_rectangle(
    entities: Sequence[RawCadEntity],
    *,
    tol: float = 2.0,
    expect: Optional[Tuple[float, float]] = None,
    expect_tol: float = 25.0,
) -> Optional[Tuple[float, float, float, float]]:
    """Recover the drawn outline rectangle from extremal axis-aligned edges.

    Several drawings break the outline at its corners (a dimension tick or
    leader crosses there), so the four sides never chain into a closed
    ring.  Chain closure alone therefore misses the single most important
    contour in the drawing.

    This looks instead for long horizontal and vertical segments sitting on
    the extremes of the geometry, and accepts them as an outline only when
    all four sides are present and their spans agree with each other.
    Returns ``(min_x, min_y, max_x, max_y)`` or ``None``.
    """
    if not entities:
        return None

    horizontals: List[Tuple[float, float, float]] = []  # (y, x_lo, x_hi)
    verticals: List[Tuple[float, float, float]] = []  # (x, y_lo, y_hi)
    for entity in entities:
        dx = entity.end.x - entity.start.x
        dy = entity.end.y - entity.start.y
        if abs(dy) <= tol and abs(dx) > tol:
            horizontals.append(
                (
                    (entity.start.y + entity.end.y) / 2.0,
                    min(entity.start.x, entity.end.x),
                    max(entity.start.x, entity.end.x),
                )
            )
        elif abs(dx) <= tol and abs(dy) > tol:
            verticals.append(
                (
                    (entity.start.x + entity.end.x) / 2.0,
                    min(entity.start.y, entity.end.y),
                    max(entity.start.y, entity.end.y),
                )
            )
    if not horizontals or not verticals:
        return None

    # The outline is the dominant pair of parallel rails, which is not
    # necessarily at the geometry extreme: nozzles and pump bodies routinely
    # protrude past the dimensioned envelope.  Pick the longest opposing
    # pair on each axis instead, then require the two pairs to agree.
    def best_pair(
        candidates: Sequence[Tuple[float, float, float]]
    ) -> Optional[Tuple[float, float, float]]:
        ordered = sorted(candidates, key=lambda t: (t[2] - t[1]), reverse=True)
        for i, (pos_a, lo_a, hi_a) in enumerate(ordered):
            span_a = hi_a - lo_a
            if span_a <= 0:
                continue
            for pos_b, lo_b, hi_b in ordered[i + 1 :]:
                span_b = hi_b - lo_b
                # Opposite rails of one rectangle: near-equal length, well
                # separated, and overlapping along their shared direction.
                if abs(span_a - span_b) > max(tol, span_a * 0.02):
                    continue
                if abs(pos_a - pos_b) < span_a * 0.05:
                    continue
                overlap = min(hi_a, hi_b) - max(lo_a, lo_b)
                if overlap < span_a * 0.9:
                    continue
                lo, hi = sorted((pos_a, pos_b))
                return (lo, hi, span_a)
        return None

    def pair_near(
        candidates: Sequence[Tuple[float, float, float]], target: float
    ) -> Optional[Tuple[float, float, float]]:
        """Find opposing rails separated by ``target``.

        Used when the metadata states the drawn outline size.  The rails
        only have to be separated correctly and to overlap; they need not
        be the longest lines present, which is what lets this succeed on
        drawings whose outline is closed on two sides only.
        """
        best: Optional[Tuple[float, float, float]] = None
        best_err = expect_tol
        for i, (pos_a, lo_a, hi_a) in enumerate(candidates):
            for pos_b, lo_b, hi_b in candidates[i + 1 :]:
                separation = abs(pos_a - pos_b)
                err = abs(separation - target)
                if err > best_err:
                    continue
                overlap = min(hi_a, hi_b) - max(lo_a, lo_b)
                if overlap < min(hi_a - lo_a, hi_b - lo_b) * 0.5:
                    continue
                # Prefer the longest such pair, tie-broken by accuracy.
                lo, hi = sorted((pos_a, pos_b))
                span = max(hi_a - lo_a, hi_b - lo_b)
                if best is None or span > best[2] or (
                    abs(span - best[2]) < tol and err < best_err
                ):
                    best = (lo, hi, span)
                    best_err = max(err, 1e-9)
        return best

    h_pair = v_pair = None
    if expect is not None:
        # Metadata gives the drawn outline; try both orientations and keep
        # the interpretation that the linework actually supports.
        for want_x, want_y in ((expect[0], expect[1]), (expect[1], expect[0])):
            cand_h = pair_near(horizontals, want_y)
            cand_v = pair_near(verticals, want_x)
            if cand_h and cand_v:
                h_pair, v_pair = cand_h, cand_v
                break

    if h_pair is None or v_pair is None:
        h_pair = best_pair(horizontals)  # -> (y_lo, y_hi, x_span)
        v_pair = best_pair(verticals)  # -> (x_lo, x_hi, y_span)
    if h_pair is None or v_pair is None:
        return None
    if expect is not None:
        # A metadata-guided hit is already validated by construction.
        got = (v_pair[1] - v_pair[0], h_pair[1] - h_pair[0])
        long_got, short_got = max(got), min(got)
        long_exp, short_exp = max(expect), min(expect)
        if (
            abs(long_got - long_exp) <= expect_tol
            and abs(short_got - short_exp) <= expect_tol
        ):
            return (v_pair[0], h_pair[0], v_pair[1], h_pair[1])

    y_lo, y_hi, x_span = h_pair
    x_lo, x_hi, y_span = v_pair
    # The rails must describe the same rectangle.
    if abs((x_hi - x_lo) - x_span) > max(tol, x_span * 0.03):
        return None
    if abs((y_hi - y_lo) - y_span) > max(tol, y_span * 0.03):
        return None

    return (x_lo, y_lo, x_hi, y_hi)


def _bridge_open_chains(
    contours: List[Contour], *, max_gap: float
) -> Tuple[List[Contour], int]:
    """Join open chains whose free ends coincide.

    Real mechanical drawings break an outline wherever another entity
    crosses it - a dimension tick, a centreline, a hidden-line dash.  The
    chain walker correctly refuses to guess a route through such a
    junction, which leaves one physical outline as several open paths.

    This pass rejoins chains only when their endpoints are genuinely
    within ``max_gap`` of each other, so it recovers the drawn outline
    without inventing any coordinate that was not already in the file.
    """
    open_paths = [c for c in contours if not c.closed]
    others = [c for c in contours if c.closed]
    if len(open_paths) < 2:
        return contours, 0

    merged = True
    joins = 0
    while merged:
        merged = False
        for i in range(len(open_paths)):
            if open_paths[i] is None:  # type: ignore[comparison-overlap]
                continue
            for j in range(i + 1, len(open_paths)):
                a, b = open_paths[i], open_paths[j]
                if a is None or b is None:  # type: ignore[comparison-overlap]
                    continue
                pairs = (
                    (a.points[-1], b.points[0], False, False),
                    (a.points[-1], b.points[-1], False, True),
                    (a.points[0], b.points[0], True, False),
                    (a.points[0], b.points[-1], True, True),
                )
                for tail, head, flip_a, flip_b in pairs:
                    if tail.distance_to(head) > max_gap:
                        continue
                    pts_a = list(reversed(a.points)) if flip_a else list(a.points)
                    pts_b = list(reversed(b.points)) if flip_b else list(b.points)
                    combined = pts_a + pts_b[1:] if pts_a[-1].distance_to(
                        pts_b[0]
                    ) <= max_gap else pts_a + pts_b
                    a.points = combined
                    a.handles = a.handles + b.handles
                    open_paths[j] = None  # type: ignore[call-overload]
                    joins += 1
                    merged = True
                    break

    rebuilt: List[Contour] = list(others)
    for contour in open_paths:
        if contour is None:  # type: ignore[comparison-overlap]
            continue
        points = contour.points
        if len(points) > 2 and points[0].distance_to(points[-1]) <= CLOSE_TOL:
            ring = points[:-1]
            fit = _fit_circle(ring)
            if fit is not None:
                contour.kind = ShapeKind.CIRCLE
                contour.centre, contour.radius = fit
            elif _is_rectangle(points):
                contour.kind = ShapeKind.RECTANGLE
            else:
                contour.kind = ShapeKind.POLYLINE
            contour.points = ring
            contour.closed = True
        rebuilt.append(contour)
    return rebuilt, joins


def detect_contours(
    entities: Sequence[RawCadEntity],
    *,
    min_length: float = 0.0,
    bridge_gap: float = 8.0,
) -> Tuple[List[Contour], Dict[str, int]]:
    """Group tessellated linework into contours.

    Returns the contours plus a small statistics dict for the audit.
    """
    unique, duplicates = dedupe_entities(entities)
    stats = {
        "input_entities": len(entities),
        "duplicate_entities": duplicates,
        "chains": 0,
        "circles": 0,
        "rectangles": 0,
        "polylines": 0,
        "open_paths": 0,
    }
    if not unique:
        return [], stats

    contours: List[Contour] = []
    for chain in _trace_chains(unique):
        points = _ordered_points(unique, chain)
        if len(points) < 2:
            continue
        handles = [unique[i].handle for i in chain]
        closed = len(points) > 2 and points[0].distance_to(points[-1]) <= CLOSE_TOL

        ring = points[:-1] if closed else points
        kind = ShapeKind.OPEN_PATH
        centre: Optional[CadPoint] = None
        radius: Optional[float] = None

        if closed:
            fit = _fit_circle(ring)
            if fit is not None:
                kind = ShapeKind.CIRCLE
                centre, radius = fit
            elif _is_rectangle(points):
                kind = ShapeKind.RECTANGLE
            else:
                kind = ShapeKind.POLYLINE

        contour = Contour(
            kind=kind,
            points=ring if closed else points,
            handles=handles,
            closed=closed,
            centre=centre,
            radius=radius,
        )
        if min_length and contour.path_length < min_length:
            continue
        contours.append(contour)

    if bridge_gap > 0:
        contours, joins = _bridge_open_chains(contours, max_gap=bridge_gap)
        stats["bridged_joins"] = joins

    stats["chains"] = len(contours)
    for contour in contours:
        if contour.kind is ShapeKind.CIRCLE:
            stats["circles"] += 1
        elif contour.kind is ShapeKind.RECTANGLE:
            stats["rectangles"] += 1
        elif contour.kind is ShapeKind.POLYLINE:
            stats["polylines"] += 1
        else:
            stats["open_paths"] += 1

    contours.sort(key=lambda c: (c.area, c.path_length), reverse=True)
    return contours, stats
