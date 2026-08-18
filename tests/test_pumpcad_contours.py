"""Tests for the pumpcad CAD parsing and contour-detection stage."""

from __future__ import annotations

import math

import pytest

from pumpcad.contours import (
    ShapeKind,
    dedupe_entities,
    detect_contours,
    find_outline_rectangle,
)
from pumpcad.source import CadPoint, RawCadEntity


def _line(x1: float, y1: float, x2: float, y2: float, handle: str = "H") -> RawCadEntity:
    return RawCadEntity(
        kind="Line",
        start=CadPoint(x1, y1),
        end=CadPoint(x2, y2),
        handle=handle,
    )


def _rect(x0: float, y0: float, x1: float, y1: float) -> list[RawCadEntity]:
    return [
        _line(x0, y0, x1, y0, "b"),
        _line(x1, y0, x1, y1, "r"),
        _line(x1, y1, x0, y1, "t"),
        _line(x0, y1, x0, y0, "l"),
    ]


def _polygonised_circle(
    cx: float, cy: float, radius: float, segments: int = 24
) -> list[RawCadEntity]:
    """A circle tessellated into straight segments, as the exporter emits."""
    points = [
        CadPoint(
            cx + radius * math.cos(2 * math.pi * i / segments),
            cy + radius * math.sin(2 * math.pi * i / segments),
        )
        for i in range(segments)
    ]
    return [
        RawCadEntity(
            kind="Line",
            start=points[i],
            end=points[(i + 1) % segments],
            handle=f"c{i}",
        )
        for i in range(segments)
    ]


class TestDedupe:
    def test_drops_reversed_duplicate(self) -> None:
        entities = [_line(0, 0, 100, 0, "a"), _line(100, 0, 0, 0, "b")]
        unique, dropped = dedupe_entities(entities)
        assert len(unique) == 1
        assert dropped == 1

    def test_keeps_distinct_segments(self) -> None:
        entities = [_line(0, 0, 100, 0, "a"), _line(0, 50, 100, 50, "b")]
        unique, dropped = dedupe_entities(entities)
        assert len(unique) == 2
        assert dropped == 0


class TestContourDetection:
    def test_closed_rectangle_is_recognised(self) -> None:
        contours, stats = detect_contours(_rect(0, 0, 400, 200))
        assert stats["rectangles"] == 1
        rect = contours[0]
        assert rect.kind is ShapeKind.RECTANGLE
        assert rect.closed
        assert rect.size == pytest.approx((400.0, 200.0))
        assert rect.area == pytest.approx(80000.0)

    def test_tessellated_circle_is_recovered(self) -> None:
        """The exporter emits no Circle entities, only polygonised lines."""
        contours, stats = detect_contours(_polygonised_circle(10.0, 20.0, 50.0))
        assert stats["circles"] == 1
        circle = contours[0]
        assert circle.kind is ShapeKind.CIRCLE
        assert circle.centre is not None and circle.radius is not None
        assert circle.centre.x == pytest.approx(10.0, abs=0.5)
        assert circle.centre.y == pytest.approx(20.0, abs=0.5)
        # A polygon inscribes the circle, so the fitted radius is slightly under.
        assert circle.radius == pytest.approx(50.0, rel=0.02)

    def test_open_path_stays_open(self) -> None:
        contours, stats = detect_contours([_line(0, 0, 100, 0), _line(100, 0, 100, 80)])
        assert stats["open_paths"] == 1
        assert not contours[0].closed

    def test_broken_corner_is_bridged(self) -> None:
        """A rectangle split at a corner must still close.

        Real drawings break outlines wherever a dimension tick crosses.
        """
        entities = [
            _line(0, 0, 400, 0, "b"),
            _line(400, 0, 400, 200, "r"),
            _line(400, 200, 0, 200, "t"),
            _line(0, 200, 0, 100, "l1"),
            _line(0, 100, 0, 0, "l2"),
        ]
        contours, _ = detect_contours(entities)
        closed = [c for c in contours if c.closed]
        assert len(closed) == 1
        assert closed[0].size == pytest.approx((400.0, 200.0))

    def test_empty_input_is_safe(self) -> None:
        contours, stats = detect_contours([])
        assert contours == []
        assert stats["input_entities"] == 0


class TestOutlineRectangle:
    def test_finds_plain_rectangle(self) -> None:
        assert find_outline_rectangle(_rect(0, 0, 1720, 760)) == pytest.approx(
            (0.0, 0.0, 1720.0, 760.0)
        )

    def test_ignores_protruding_nozzle(self) -> None:
        """The outline is the dimensioned envelope, not the bounding box.

        204-PU-006 has a nozzle projecting 140 mm past its outline.
        """
        entities = _rect(0, 0, 1725, 760) + [
            _line(1725, 380, 1865, 380, "nozzle"),
            _line(1865, 330, 1865, 430, "nozzle_face"),
        ]
        box = find_outline_rectangle(entities)
        assert box is not None
        assert box[2] - box[0] == pytest.approx(1725.0)
        assert box[3] - box[1] == pytest.approx(760.0)

    def test_metadata_guided_recovery_of_open_outline(self) -> None:
        """Two rails plus metadata are enough when the outline is not closed.

        Several drawings only draw the outline's long sides.
        """
        entities = [
            _line(0, 10, 0, 2140, "left"),
            _line(857, 10, 857, 2140, "right"),
            _line(200, 0, 572, 0, "bottom_stub"),
            _line(300, 2129, 640, 2129, "top_stub"),
        ]
        box = find_outline_rectangle(entities, expect=(2129.0, 857.0))
        assert box is not None
        assert box[2] - box[0] == pytest.approx(857.0, abs=1.0)

    def test_returns_none_without_an_outline(self) -> None:
        assert find_outline_rectangle([_line(0, 0, 100, 0)]) is None
