"""Tests for topology recovery: concentric stacks, rail cylinders, bands.

These recognisers are what separate a faithful reconstruction from a
two-box approximation. A naive pass over the same linework consumed 40%
of the entities and produced 2-3 solids per pump; recovering the drawn
topology raises that to ~92% and 9-13 solids.
"""

from __future__ import annotations

import math

import pytest

from pumpcad.contours import detect_contours
from pumpcad.features import (
    FeatureKind,
    extract_features,
    find_concentric_stacks,
    find_parallel_rails,
)
from pumpcad.source import CadPoint, RawCadEntity


def _line(x1: float, y1: float, x2: float, y2: float, handle: str) -> RawCadEntity:
    return RawCadEntity(
        kind="Line", start=CadPoint(x1, y1), end=CadPoint(x2, y2), handle=handle
    )


def _rect(x0: float, y0: float, x1: float, y1: float, tag: str) -> list[RawCadEntity]:
    return [
        _line(x0, y0, x1, y0, f"{tag}b"),
        _line(x1, y0, x1, y1, f"{tag}r"),
        _line(x1, y1, x0, y1, f"{tag}t"),
        _line(x0, y1, x0, y0, f"{tag}l"),
    ]


def _circle(
    cx: float, cy: float, radius: float, tag: str, segments: int = 24
) -> list[RawCadEntity]:
    pts = [
        CadPoint(
            cx + radius * math.cos(2 * math.pi * i / segments),
            cy + radius * math.sin(2 * math.pi * i / segments),
        )
        for i in range(segments)
    ]
    return [
        RawCadEntity(
            kind="Line", start=pts[i], end=pts[(i + 1) % segments], handle=f"{tag}{i}"
        )
        for i in range(segments)
    ]


class TestConcentricStacks:
    def test_concentric_circles_become_one_stepped_feature(self) -> None:
        """A volute, its flange and its hub are one part, not three discs."""
        contours, _ = detect_contours(
            _circle(500, 400, 93, "outer") + _circle(500, 400, 73, "inner")
        )
        stacks, used = find_concentric_stacks(contours)
        assert len(stacks) == 1
        stack = stacks[0]
        assert stack.kind is FeatureKind.DISC_STACK
        assert len(stack.radii) == 2
        assert stack.radii[0] < stack.radii[1]
        assert used

    def test_separated_circles_stay_separate(self) -> None:
        contours, _ = detect_contours(
            _circle(200, 400, 80, "a") + _circle(1200, 400, 80, "b")
        )
        stacks, _ = find_concentric_stacks(contours)
        assert len(stacks) == 2

    def test_stack_bounds_use_the_outer_radius(self) -> None:
        contours, _ = detect_contours(
            _circle(500, 400, 93, "outer") + _circle(500, 400, 40, "inner")
        )
        stack = find_concentric_stacks(contours)[0][0]
        width, height = stack.size
        assert width == pytest.approx(186.0, abs=4.0)
        assert height == pytest.approx(186.0, abs=4.0)


class TestParallelRails:
    def test_rail_pair_becomes_a_cylinder(self) -> None:
        """Two parallel lines with a gap are a shaft seen from the side.

        Reading them as two thin plates is the largest single fidelity
        loss in a naive reconstruction.
        """
        contours, _ = detect_contours(
            [
                _line(1186, 313, 1396, 313, "shaft_lower"),
                _line(1186, 447, 1396, 447, "shaft_upper"),
            ]
        )
        rails, used = find_parallel_rails(contours)
        assert len(rails) == 1
        rail = rails[0]
        assert rail.kind is FeatureKind.CYLINDER
        assert rail.axis == "x"
        assert rail.radii[0] == pytest.approx(67.0, abs=1.0)
        assert rail.size[0] == pytest.approx(210.0, abs=1.0)
        assert used

    def test_vertical_rail_pair_is_detected(self) -> None:
        contours, _ = detect_contours(
            [
                _line(350, 850, 350, 1180, "col_left"),
                _line(458, 850, 458, 1180, "col_right"),
            ]
        )
        rails, _ = find_parallel_rails(contours)
        assert len(rails) == 1
        assert rails[0].axis == "y"

    def test_non_overlapping_lines_do_not_pair(self) -> None:
        contours, _ = detect_contours(
            [
                _line(0, 100, 200, 100, "a"),
                _line(900, 300, 1100, 300, "b"),
            ]
        )
        assert find_parallel_rails(contours)[0] == []

    def test_hairline_gap_is_not_a_cylinder(self) -> None:
        contours, _ = detect_contours(
            [
                _line(0, 100, 400, 100, "a"),
                _line(0, 102, 400, 102, "b"),
            ]
        )
        assert find_parallel_rails(contours)[0] == []


class TestExtractFeatures:
    def test_outline_is_not_reported_as_a_component(self) -> None:
        """The dimensioned envelope is an annotation, not a body.

        It is frequently drawn open; letting it through makes it span the
        whole drawing and swallow every other feature.
        """
        outline = (0.0, 0.0, 1720.0, 760.0)
        entities = _rect(0, 0, 1720, 760, "outline") + _rect(200, 180, 700, 580, "motor")
        contours, _ = detect_contours(entities)
        features = extract_features(contours, outline=outline)
        for feature in features:
            width, height = feature.size
            assert not (
                width == pytest.approx(1720.0, abs=3.0)
                and height == pytest.approx(760.0, abs=3.0)
            ), "the outline leaked into the feature list"

    def test_a_real_plan_layout_yields_several_features(self) -> None:
        outline = (0.0, 0.0, 1720.0, 760.0)
        entities = (
            _rect(0, 0, 1720, 760, "outline")
            + _rect(313, 140, 776, 620, "motor")
            + _circle(1571, 380, 93, "volute")
            + _circle(1571, 380, 73, "flange")
            + [
                _line(1186, 313, 1396, 313, "shaft_lo"),
                _line(1186, 447, 1396, 447, "shaft_hi"),
            ]
        )
        contours, _ = detect_contours(entities)
        features = extract_features(contours, outline=outline)
        kinds = {f.kind for f in features}
        assert FeatureKind.DISC_STACK in kinds
        assert FeatureKind.CYLINDER in kinds
        assert len(features) >= 3

    def test_features_remain_traceable(self) -> None:
        outline = (0.0, 0.0, 1720.0, 760.0)
        contours, _ = detect_contours(
            _rect(0, 0, 1720, 760, "outline") + _rect(200, 180, 700, 580, "motor")
        )
        for feature in extract_features(contours, outline=outline):
            assert feature.handles, f"{feature.kind} lost its source handles"

    def test_empty_input_is_safe(self) -> None:
        assert extract_features([], outline=None) == []
