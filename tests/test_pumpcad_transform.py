"""Tests for the pumpcad coordinate transform chain.

The transform is deliberately the only place frames change, so these
tests pin the conventions the rest of the pipeline relies on.
"""

from __future__ import annotations

import pytest

from pumpcad.semantic import ViewType
from pumpcad.transform import (
    Placement,
    axis_to_rotation,
    cad_to_local,
    local_to_world,
    ori_clause,
    rotation_to_axis,
    world_size,
)


class TestAngleConvention:
    @pytest.mark.parametrize(
        ("axis", "degrees"),
        [("E", 0.0), ("N", 90.0), ("W", 180.0), ("S", 270.0)],
    )
    def test_axis_to_rotation_is_counter_clockwise_from_east(
        self, axis: str, degrees: float
    ) -> None:
        assert axis_to_rotation(axis) == degrees

    @pytest.mark.parametrize("axis", ["E", "N", "W", "S"])
    def test_rotation_round_trips(self, axis: str) -> None:
        assert rotation_to_axis(axis_to_rotation(axis)) == axis

    def test_rejects_vertical_axis(self) -> None:
        with pytest.raises(ValueError):
            axis_to_rotation("U")


class TestPlacement:
    def test_forward_and_left_are_orthogonal(self) -> None:
        for axis in ("E", "N", "W", "S"):
            placement = Placement(origin=(0.0, 0.0, 0.0), layout_axis=axis)
            fx, fy = placement.forward
            lx, ly = placement.left
            assert fx * lx + fy * ly == pytest.approx(0.0)

    def test_left_is_counter_clockwise_of_forward(self) -> None:
        placement = Placement(origin=(0.0, 0.0, 0.0), layout_axis="E")
        assert placement.forward == (1.0, 0.0)
        assert placement.left == (0.0, 1.0)


class TestLocalToWorld:
    def test_origin_maps_to_the_datum(self) -> None:
        placement = Placement(origin=(1000.0, 2000.0, 50.0), layout_axis="E")
        assert local_to_world((0.0, 0.0, 0.0), placement) == pytest.approx(
            (1000.0, 2000.0, 50.0)
        )

    def test_east_pump_puts_along_on_east(self) -> None:
        placement = Placement(origin=(0.0, 0.0, 0.0), layout_axis="E")
        assert local_to_world((500.0, 0.0, 0.0), placement) == pytest.approx(
            (500.0, 0.0, 0.0)
        )

    def test_north_pump_rotates_along_onto_north(self) -> None:
        placement = Placement(origin=(0.0, 0.0, 0.0), layout_axis="N")
        east, north, up = local_to_world((500.0, 0.0, 0.0), placement)
        assert (east, north, up) == pytest.approx((0.0, 500.0, 0.0))

    def test_height_is_never_rotated(self) -> None:
        for axis in ("E", "N", "W", "S"):
            placement = Placement(origin=(0.0, 0.0, 10.0), layout_axis=axis)
            assert local_to_world((0.0, 0.0, 300.0), placement)[2] == pytest.approx(310.0)

    def test_world_size_swaps_for_north_south(self) -> None:
        east = Placement(origin=(0.0, 0.0, 0.0), layout_axis="E")
        north = Placement(origin=(0.0, 0.0, 0.0), layout_axis="N")
        assert world_size(1720.0, 760.0, east) == (1720.0, 760.0)
        assert world_size(1720.0, 760.0, north) == (760.0, 1720.0)


class TestCadToLocal:
    OUTLINE = (0.0, 0.0, 1720.0, 760.0)

    def test_plan_centre_body_sits_at_the_local_origin(self) -> None:
        local = cad_to_local(
            (760.0, 280.0, 960.0, 480.0),
            outline=self.OUTLINE,
            view=ViewType.PLAN,
            long_axis="x",
            height=400.0,
        )
        assert local.along == pytest.approx(0.0)
        assert local.across == pytest.approx(0.0)
        assert local.length == pytest.approx(200.0)
        assert local.width == pytest.approx(200.0)

    def test_plan_preserves_the_footprint(self) -> None:
        """A plan view's XY extents must survive the lift unchanged."""
        local = cad_to_local(
            (200.0, 180.0, 700.0, 580.0),
            outline=self.OUTLINE,
            view=ViewType.PLAN,
            long_axis="x",
            height=500.0,
        )
        assert local.length == pytest.approx(500.0)
        assert local.width == pytest.approx(400.0)

    def test_elevation_turns_vertical_span_into_height(self) -> None:
        """On an elevation the tall CAD axis is a height, not a depth."""
        local = cad_to_local(
            (280.0, 100.0, 480.0, 900.0),
            outline=(0.0, 0.0, 760.0, 1720.0),
            view=ViewType.ELEVATION,
            long_axis="y",
        )
        assert local.height == pytest.approx(800.0)
        # The horizontal span becomes a diameter in both plan directions.
        assert local.length == pytest.approx(200.0)
        assert local.width == pytest.approx(200.0)

    def test_elevation_height_is_measured_from_the_outline_base(self) -> None:
        local = cad_to_local(
            (280.0, 100.0, 480.0, 900.0),
            outline=(0.0, 0.0, 760.0, 1720.0),
            view=ViewType.ELEVATION,
            long_axis="y",
        )
        # Body spans 100..900 above the outline base, so its centre is 500.
        assert local.up == pytest.approx(500.0)

    def test_unknown_view_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            cad_to_local(
                (0.0, 0.0, 10.0, 10.0),
                outline=self.OUTLINE,
                view=ViewType.UNKNOWN,
                long_axis="x",
            )


class TestOriClause:
    def test_vertical_axes(self) -> None:
        assert ori_clause("U") == "ORI Z IS U AND Y IS N"
        assert ori_clause("D") == "ORI Z IS D AND Y IS N"

    def test_horizontal_axes(self) -> None:
        assert ori_clause("E") == "ORI Z IS E AND Y IS U"
        assert ori_clause("N") == "ORI Z IS N AND Y IS U"

    def test_rejects_nonsense(self) -> None:
        with pytest.raises(ValueError):
            ori_clause("X")
