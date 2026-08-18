"""Tests for pumpcad view classification and component inference.

The view type is the single most consequential decision in the pipeline.
The JSON export declares its own view (``reference_top_view``), and the
client confirmed on 2026-08-13 that every supplied drawing is a top view:
a North/South pump's plan outline is legitimately taller than it is wide.
The geometric aspect-ratio heuristic that treated those as elevations was
the defect behind a full batch of vertical-pump misreads, and these tests
pin the corrected behaviour.
"""

from __future__ import annotations

import pytest

from pumpcad.semantic import (
    ComponentKind,
    Confidence,
    ViewType,
    build_semantic_model,
    classify_view,
)
from pumpcad.source import CadPoint, PumpRecord, RawCadEntity


def _line(x1: float, y1: float, x2: float, y2: float, handle: str = "H") -> RawCadEntity:
    return RawCadEntity(
        kind="Line", start=CadPoint(x1, y1), end=CadPoint(x2, y2), handle=handle
    )


def _record(
    tag: str = "TEST-PU-001",
    *,
    length: float = 1720.0,
    width: float = 760.0,
    entities: list[RawCadEntity] | None = None,
    reference_top_view: str | None = None,
) -> PumpRecord:
    return PumpRecord(
        tag=tag,
        name="TEST PUMP",
        source_path=f"{tag}.json",
        location_e_n_u=(1000.0, 2000.0, 0.0),
        length_mm=length,
        width_mm=width,
        inlet_orientation="E",
        outlet_orientation="U",
        dn_input_mm=150.0,
        dn_output_mm=100.0,
        specification="ANSI-NOZZLES",
        generic_type="150lb Ansi Flanges",
        reference_top_view=reference_top_view,
        entities=entities or [],
    )


def _outline_entities(
    x0: float, y0: float, x1: float, y1: float, tag: str = "o"
) -> list[RawCadEntity]:
    """A closed rectangle.  Handles are unique per rectangle, as in real
    exports, so contour claiming behaves the way it does on real data."""
    return [
        _line(x0, y0, x1, y0, f"{tag}b"),
        _line(x1, y0, x1, y1, f"{tag}r"),
        _line(x1, y1, x0, y1, f"{tag}t"),
        _line(x0, y1, x0, y0, f"{tag}l"),
    ]


class TestViewClassification:
    def test_declared_top_view_wins_over_a_tall_outline(self) -> None:
        """A 760x1720 outline with a declared top view is a N/S plan."""
        record = _record(reference_top_view="Top View - TEST-PU-001")
        view, reason = classify_view(record, (0.0, 0.0, 760.0, 1720.0))
        assert view is ViewType.PLAN
        assert "declared top view" in reason

    def test_undeclared_tall_outline_still_parses_as_a_plan(self) -> None:
        """Without a declared view the geometry itself is read as a plan;
        aspect ratio alone is no longer allowed to rotate a pump on end."""
        record = _record(entities=_outline_entities(0, 0, 760, 1720))
        view, reason = classify_view(record, (0.0, 0.0, 760.0, 1720.0))
        assert view is ViewType.PLAN

    def test_wide_contained_outline_is_a_plan(self) -> None:
        record = _record(entities=_outline_entities(0, 0, 1720, 760))
        view, _ = classify_view(record, (0.0, 0.0, 1720.0, 760.0))
        assert view is ViewType.PLAN

    def test_undeclared_outline_with_geometry_below_is_unknown(self) -> None:
        """Without a declared view and with unexplained geometry below the
        outline, the pipeline refuses to guess instead of rotating it."""
        entities = _outline_entities(0, 0, 2000, 1050, "env") + [
            _line(400, 0, 400, -350, "pedestal_left"),
            _line(900, 0, 900, -350, "pedestal_right"),
            _line(400, -350, 900, -350, "sole_plate"),
        ]
        record = _record(length=2000.0, width=1050.0, entities=entities)
        view, reason = classify_view(record, (0.0, 0.0, 2000.0, 1050.0))
        assert view is ViewType.UNKNOWN
        assert "refusing to guess" in reason

    def test_missing_outline_is_unknown(self) -> None:
        view, reason = classify_view(_record(), None)
        assert view is ViewType.UNKNOWN
        assert "no outline" in reason


class TestSemanticModel:
    def test_pump_without_geometry_degrades_safely(self) -> None:
        """203-PU-020 and 205-PU-004 carry no CAD evidence at all."""
        model = build_semantic_model(_record())
        assert model.view is ViewType.UNKNOWN
        assert model.components == []
        assert model.warnings
        assert "no shape-reference geometry" in model.warnings[0]

    def test_plan_view_yields_baseplate_and_bodies(self) -> None:
        entities = _outline_entities(0, 0, 1720, 760, "plate")
        # Driver at the left end, casing at the right, on a shared centreline.
        entities += _outline_entities(200, 180, 700, 580, "motor")
        entities += _outline_entities(1100, 250, 1500, 510, "casing")
        model = build_semantic_model(
            _record(length=1720.0, width=760.0, entities=entities)
        )
        assert model.view is ViewType.PLAN
        # The outline is recovered as the pump's envelope.  It is not a
        # CAD-derived *component*: the baseplate is contractual, built from
        # Pump_details.xlsx in the build stage, so the semantic model
        # deliberately leaves it out.
        assert model.outline_size == pytest.approx((1720.0, 760.0))
        motor = model.first(ComponentKind.MOTOR)
        casing = model.first(ComponentKind.PUMP_CASING)
        assert motor is not None and casing is not None
        # The driver is the one nearer the origin along the long axis.
        assert motor.centre[0] < casing.centre[0]

    def test_components_carry_traceable_handles(self) -> None:
        entities = _outline_entities(0, 0, 1720, 760, "plate")
        entities += _outline_entities(200, 180, 700, 580, "motor")
        entities += _outline_entities(1100, 250, 1500, 510, "casing")
        model = build_semantic_model(
            _record(length=1720.0, width=760.0, entities=entities)
        )
        motor = model.first(ComponentKind.MOTOR)
        assert motor is not None
        assert motor.handles, "components must be traceable to source CAD handles"

    def test_every_component_states_a_reason(self) -> None:
        entities = _outline_entities(0, 0, 1720, 760, "plate")
        entities += _outline_entities(200, 180, 700, 580, "motor")
        model = build_semantic_model(
            _record(length=1720.0, width=760.0, entities=entities)
        )
        assert model.components
        for component in model.components:
            assert component.reason.strip(), f"{component.kind} has no reason"
