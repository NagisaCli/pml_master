"""Regression coverage for the 2026-08-20 r9 motor/drive rebuild."""

from __future__ import annotations

import hashlib
import math
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "Projects" / "JK_Pump_Build"
TOOLS = PROJECT / "tools"
sys.path.insert(0, str(TOOLS))

from build_pumps import build_pump                              # noqa: E402
from extract_project_data import load_all                       # noqa: E402

CSV = PROJECT / "imports" / "2026-08-19_engine_shaft_measurements_updated.csv"
CSV_SHA256 = "c3e8b5cd96cb0e76bbedaae15f87202bd110696b8fcbf4834b1b639fe29c141e"
MISSING_DONORS = {
    "203-PU-020": "203-PU-031",
    "203-PU-026": "205-PU-024",
    "205-PU-004": "204-PU-006",
}


@lru_cache(maxsize=1)
def _sources():
    return load_all()


@lru_cache(maxsize=1)
def _models():
    sources = _sources()
    return {tag: build_pump(tag, sources)
            for tag in sorted(sources["location"])}


def test_archived_measurement_csv_is_the_supplied_source():
    assert hashlib.sha256(CSV.read_bytes()).hexdigest() == CSV_SHA256


def test_missing_rows_use_traceable_deterministic_reference_families():
    sources = _sources()
    assert set(sources["location"]) - set(sources["engine"]) == set(MISSING_DONORS)
    for tag, donor in MISSING_DONORS.items():
        model = _models()[tag]
        assert model.facts["engine_source"] == f"DERIVED from {donor}"
        assert any(donor in item for item in model.reference_values)
        assert 0.5 <= model.facts["shaft_fit_scale"] <= 1.5


def test_driver_uses_measured_cones_and_never_the_old_dish_end_bells():
    for tag, model in _models().items():
        driver = [item for item in model.primitives if item.sube == "DRIVER"]
        assert driver, tag
        assert not any(item.kind == "DISH" for item in driver), tag
        for cone in (item for item in driver if item.kind == "CONE"):
            assert cone.attrs["DBOT"] > 0
            assert cone.attrs["DTOP"] > 0
            assert cone.attrs["HEIG"] > 0
            assert f"Z is {model.facts['wet_end']}" in cone.ori


def test_motor_parts_close_exactly_inside_the_resolved_total_envelope():
    for tag, model in _models().items():
        segments = model.facts["motor_segments"]
        assert math.isclose(sum(item["length"] for item in segments),
                            model.facts["motor_effective_total"], abs_tol=0.05), tag
        assert math.isclose(segments[0]["start"],
                            model.facts["motor_axis_span"][0], abs_tol=0.01), tag
        assert math.isclose(segments[-1]["end"],
                            model.facts["motor_axis_span"][1], abs_tol=0.01), tag
        for first, second in zip(segments, segments[1:]):
            assert math.isclose(first["end"], second["start"],
                                abs_tol=0.01), (tag, first["role"], second["role"])


def test_every_motor_has_two_similar_cones_with_small_faces_outward():
    for tag, model in _models().items():
        segments = model.facts["motor_segments"]
        cones = [item for item in segments if item["kind"] == "CONE"]
        main = next(item for item in segments
                    if item["role"] == "main stator barrel")
        assert len(cones) == 2, tag
        rear, front = cones
        target = main["DIAM"] * (2.0 / 3.0)
        assert math.isclose(rear["DBOT"], target, abs_tol=0.01), tag
        assert math.isclose(rear["DTOP"], main["DIAM"], abs_tol=0.01), tag
        assert math.isclose(front["DBOT"], main["DIAM"], abs_tol=0.01), tag
        assert math.isclose(front["DTOP"], target, abs_tol=0.01), tag
        assert math.isclose(rear["length"], front["length"], abs_tol=0.01), tag
        assert segments[0]["kind"] == "CONE", tag
        assert segments[0]["role"] == "rear frustum", tag
        assert segments[-1]["kind"] == "CONE", tag
        assert segments[-1]["role"] == "front frustum", tag
        assert not any(item["role"] == "rear small barrel" for item in segments), tag


def test_205_pu_012_keeps_long_envelope_with_a_cone_as_the_tail():
    model = _models()["205-PU-012"]
    main = next(item for item in model.facts["motor_segments"]
                if item["role"] == "main stator barrel")
    assert math.isclose(main["length"], 1126.8, abs_tol=0.01)
    assert math.isclose(model.facts["motor_effective_total"], 1277.8,
                        abs_tol=0.01)
    assert model.facts["motor_effective_total"] > model.facts["motor_source_total"]


def test_non_mc_drive_is_exactly_two_cylinders_then_one_pump_side_cone():
    sources = _sources()
    for tag, model in _models().items():
        drive = [item for item in model.primitives if item.sube == "DRIVE_SHAFT"]
        if model.facts["is_mc"]:
            assert drive == [], tag
            assert "close-coupled" in model.facts["shaft"]
            continue
        assert [item.kind for item in drive] == ["CYLINDER", "CYLINDER", "CONE"], tag
        assert not any(item.sube == "COUPLING" for item in model.primitives), tag
        engine = model.facts["engine_record"]
        assert math.isclose(drive[0].attrs["DIAM"], engine["shaft_cyl1_D_mm"]), tag
        assert math.isclose(drive[1].attrs["DIAM"], engine["shaft_cyl2_D_mm"]), tag
        assert math.isclose(drive[2].attrs["DBOT"],
                            engine["shaft_frust3_D_min_mm"]), tag
        assert math.isclose(drive[2].attrs["DTOP"],
                            engine["shaft_frust3_D_max_mm"]), tag


def test_drive_axial_fit_preserves_ratios_and_closes_both_interfaces():
    for tag, model in _models().items():
        if model.facts["is_mc"]:
            continue
        segments = model.facts["drive_segments"]
        scale = model.facts["shaft_fit_scale"]
        assert 0.5 <= scale <= 1.5, tag
        for item in segments:
            assert math.isclose(item["length"] / item["source_length"], scale,
                                rel_tol=0, abs_tol=1e-9), (tag, item["role"])
        for first, second in zip(segments, segments[1:]):
            assert math.isclose(first["end"], second["start"], abs_tol=0.01), tag
        assert math.isclose(segments[0]["start"],
                            model.facts["motor_axis_span"][1], abs_tol=0.01), tag
        casing_centre = model.facts["casing_centre"]
        plate_centre = model.facts["plate_centre"]
        wet = {"N": (0.0, 1.0), "S": (0.0, -1.0),
               "E": (1.0, 0.0), "W": (-1.0, 0.0)}[model.facts["wet_end"]]
        casing_along = ((casing_centre[0] - plate_centre[0]) * wet[0]
                        + (casing_centre[1] - plate_centre[1]) * wet[1])
        casing_back = casing_along - model.facts["casing"][1] / 2
        assert casing_back - 0.01 <= segments[-1]["end"] <= casing_along + 0.01, tag
