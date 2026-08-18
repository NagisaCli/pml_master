"""Tests for pumpcad geometry building, PML emission and validation."""

from __future__ import annotations

import pytest

from pumpcad.audit import validate
from pumpcad.build import (
    BASEPLATE_THICKNESS,
    build_pump,
    render_pml,
    snap_to_catalogue_dn,
)
from pumpcad.semantic import ViewType, build_semantic_model
from pumpcad.source import CadPoint, PumpRecord, RawCadEntity
from wsb.pml_builder import validate_pml


def _line(x1: float, y1: float, x2: float, y2: float, handle: str = "H") -> RawCadEntity:
    return RawCadEntity(
        kind="Line", start=CadPoint(x1, y1), end=CadPoint(x2, y2), handle=handle
    )


def _rect(x0: float, y0: float, x1: float, y1: float, tag: str = "r") -> list[RawCadEntity]:
    return [
        _line(x0, y0, x1, y0, f"{tag}b"),
        _line(x1, y0, x1, y1, f"{tag}r"),
        _line(x1, y1, x0, y1, f"{tag}t"),
        _line(x0, y1, x0, y0, f"{tag}l"),
    ]


def _record(
    *,
    tag: str = "TEST-PU-001",
    length: float = 1720.0,
    width: float = 760.0,
    inlet: str = "E",
    outlet: str = "U",
    entities: list[RawCadEntity] | None = None,
    location: tuple[float, float, float] = (10000.0, 20000.0, 0.0),
) -> PumpRecord:
    return PumpRecord(
        tag=tag,
        name="TEST PUMP",
        source_path=f"{tag}.json",
        location_e_n_u=location,
        length_mm=length,
        width_mm=width,
        inlet_orientation=inlet,
        outlet_orientation=outlet,
        dn_input_mm=150.0,
        dn_output_mm=100.0,
        specification="ANSI-NOZZLES",
        generic_type="150lb Ansi Flanges",
        reference_top_view=None,
        entities=entities or [],
    )


def _plan_record(**kwargs) -> PumpRecord:
    entities = (
        _rect(0, 0, 1720, 760, "plate")
        + _rect(200, 180, 700, 580, "motor")
        + _rect(1200, 280, 1500, 480, "casing")
    )
    return _record(entities=entities, **kwargs)


class TestCatalogueSnapping:
    def test_exact_size_is_kept_without_a_note(self) -> None:
        dn, note = snap_to_catalogue_dn(150.0)
        assert dn == 150
        assert note == ""

    def test_odd_bore_snaps_and_reports(self) -> None:
        """Metadata carries measured bores, not catalogue sizes."""
        dn, note = snap_to_catalogue_dn(173.0)
        assert dn in (150, 200)
        assert note, "a substituted bore must be reported, never silent"

    def test_rejects_non_positive_bore(self) -> None:
        with pytest.raises(ValueError):
            snap_to_catalogue_dn(0.0)


class TestPlacement:
    def test_baseplate_underside_sits_on_the_metadata_datum(self) -> None:
        record = _plan_record(location=(5000.0, 6000.0, 100.0))
        build = build_pump(record, build_semantic_model(record))
        plate = build.solids[0]
        assert plate.position[0] == pytest.approx(5000.0)
        assert plate.position[1] == pytest.approx(6000.0)
        # POS is the centre, so the underside is half a thickness lower.
        assert plate.position[2] - BASEPLATE_THICKNESS / 2.0 == pytest.approx(100.0)

    def test_north_facing_pump_swaps_plate_extents(self) -> None:
        record = _plan_record(inlet="N")
        build = build_pump(record, build_semantic_model(record))
        plate = build.solids[0]
        assert plate.xlen == pytest.approx(760.0)
        assert plate.ylen == pytest.approx(1720.0)


class TestPlanReconstruction:
    def test_driver_and_casing_are_separated_along_the_axis(self) -> None:
        """Regression: nested detail contours once put the casing on the motor.

        A motor is drawn with its terminal box inside its own outline; taking
        the two largest contours by area picked that inner rectangle as the
        casing, leaving both bodies 92 mm apart on a 1720 mm plate.
        """
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        bodies = build.solids[1:]
        assert len(bodies) >= 2
        eastings = sorted(s.position[0] for s in bodies)
        assert eastings[-1] - eastings[0] > 500.0

    def test_footprint_matches_the_cad_outline(self) -> None:
        record = _plan_record()
        model = build_semantic_model(record)
        build = build_pump(record, model)
        bounds = build.top_view_bounds()
        assert bounds is not None
        assert bounds[2] - bounds[0] == pytest.approx(1720.0, abs=1.0)
        assert bounds[3] - bounds[1] == pytest.approx(760.0, abs=1.0)

    def test_body_footprints_come_from_the_cad_contours(self) -> None:
        """The driver's drawn footprint must survive into the model.

        It is emitted as a cylinder lying along the machine axis, so the
        footprint is checked by projection rather than by BOX extents.
        """
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        motor = next(s for s in build.solids if "Motor [" in s.label)
        x0, y0, x1, y1 = motor.top_view_bounds()
        assert x1 - x0 == pytest.approx(500.0, abs=1.0)
        assert y1 - y0 == pytest.approx(400.0, abs=1.0)

    def test_rotating_parts_share_one_shaft_centreline(self) -> None:
        """Regression: every body used to stand on the plate at its own
        height, so a horizontal pump read as boxes lying on the ground."""
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        train = [
            s
            for s in build.solids
            if s.primitive == "CYLI"
            and s.axis not in ("U", "D")
            and any(
                key in s.label
                for key in ("Motor", "Coupling", "BearingHousing", "PumpCasing")
            )
            and "branch" not in s.label
            and "flange" not in s.label
            and "gland" not in s.label
        ]
        assert len(train) >= 2
        elevations = {round(s.position[2], 3) for s in train}
        assert len(elevations) == 1, f"shaft train is not concentric: {elevations}"

    def test_driver_lies_along_the_machine_axis(self) -> None:
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        motor = next(s for s in build.solids if "Motor [" in s.label)
        assert motor.primitive == "CYLI"
        assert motor.axis == build.placement.layout_axis

    def test_nothing_sinks_below_the_baseplate(self) -> None:
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        plate = build.solids[0]
        underside = plate.position[2] - plate.zlen / 2.0
        for solid in build.solids:
            if solid.primitive == "BOX":
                half = solid.zlen / 2.0
            elif solid.axis in ("U", "D"):
                half = solid.height / 2.0
            else:
                half = max(solid.diameter, solid.dtop, solid.dbot) / 2.0
            assert solid.position[2] - half >= underside - 1.0, (
                f"{solid.label!r} dips below the baseplate"
            )

    def test_driver_carries_mechanical_detail(self) -> None:
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        labels = " ".join(s.label for s in build.solids)
        assert "cooling rib" in labels
        assert "terminal box" in labels
        assert "foot" in labels

    def test_nozzles_stand_alone_without_extra_primitives(self) -> None:
        """Client rule: a nozzle is just the nozzle.  The catalogue NOZZLE
        element draws its own flange and barrel, so no neck/flange solids
        may be added beside it."""
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        labels = " ".join(s.label for s in build.solids)
        assert len(build.nozzles) == 2
        assert "branch neck" not in labels
        assert "raised-face flange" not in labels

    def test_baseplate_has_anchor_bolts(self) -> None:
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        bolts = [s for s in build.solids if "anchor bolt" in s.label]
        assert len(bolts) == 8  # four positions, shank + head each


class TestUnknownViewFallback:
    """A file with no declared view and unexplained geometry below its
    outline must refuse to guess, and still produce a bounded pump from
    metadata rather than a rotated elevation."""

    def _ambiguous_record(self) -> PumpRecord:
        entities = (
            _rect(0, 0, 2000, 1050, "env")
            + _rect(400, 0, 450, -350, "pedestal_left")
            + _rect(900, 0, 950, -350, "pedestal_right")
        )
        return _record(length=2000.0, width=1050.0, entities=entities)

    def test_ambiguous_view_is_unknown(self) -> None:
        model = build_semantic_model(self._ambiguous_record())
        assert model.view is ViewType.UNKNOWN
        assert model.components == []
        assert any("refusing to guess" in w for w in model.warnings)

    def test_baseplate_always_uses_the_metadata_pair(self) -> None:
        """The old elevation reading stood a 1720 mm pump on a 1720 mm deep
        plate; with an unresolved view the metadata pair is still the plan
        and nothing can silently turn one of its figures into a height."""
        build = build_pump(
            self._ambiguous_record(),
            build_semantic_model(self._ambiguous_record()),
        )
        plate = build.solids[0]
        assert plate.xlen == pytest.approx(2000.0, abs=1.0)
        assert plate.ylen == pytest.approx(1050.0, abs=1.0)

    def test_fallback_still_builds_a_horizontal_body(self) -> None:
        build = build_pump(
            self._ambiguous_record(),
            build_semantic_model(self._ambiguous_record()),
        )
        assert len(build.solids) > 2
        assert any("volute barrel" in s.label for s in build.solids)


class TestPmlEmission:
    def test_emitted_pml_passes_project_validation(self) -> None:
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        script = render_pml(build, generated="2026-08-12 00:00:00")
        assert validate_pml(script) == []

    def test_exactly_one_equi_per_file(self) -> None:
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        script = render_pml(build, generated="2026-08-12 00:00:00")
        assert script.count("NEW EQUI") == 1

    def test_nozzle_binds_catref_before_position(self) -> None:
        """An unbound NOZZLE draws nothing, so CATR must come first."""
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        script = render_pml(build, generated="2026-08-12 00:00:00")
        lines = script.splitlines()
        nozzle_at = next(i for i, l in enumerate(lines) if l.startswith("NEW NOZZLE"))
        catr_at = next(
            i for i, l in enumerate(lines[nozzle_at:], nozzle_at) if l.startswith("CATR")
        )
        pos_at = next(
            i for i, l in enumerate(lines[nozzle_at:], nozzle_at) if l.startswith("POS")
        )
        assert catr_at < pos_at

    def test_comments_use_the_pml1_token(self) -> None:
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        script = render_pml(build, generated="2026-08-12 00:00:00")
        for line in script.splitlines():
            if line and not line[0].isalpha():
                assert line.startswith("--"), f"unexpected comment syntax: {line!r}"

    def test_cad_handles_are_recorded_for_traceability(self) -> None:
        record = _plan_record()
        build = build_pump(record, build_semantic_model(record))
        script = render_pml(build, generated="2026-08-12 00:00:00")
        assert "-- CAD handles:" in script


class TestValidation:
    def test_clean_plan_pump_passes(self) -> None:
        record = _plan_record()
        model = build_semantic_model(record)
        result = validate(record, model, build_pump(record, model))
        assert result.passed, [c for c in result.failures]

    def test_pump_without_geometry_is_flagged_not_crashed(self) -> None:
        record = _record()
        model = build_semantic_model(record)
        build = build_pump(record, model)
        result = validate(record, model, build)
        assert not result.passed
        assert any(
            "CAD top-view evidence" in name for name, _, _ in result.failures
        )
        # It still produces a usable metadata-only model.
        assert build.solids
