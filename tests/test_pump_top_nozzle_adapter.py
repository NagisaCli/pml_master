"""Regression coverage for the 2026-08-20 r12 top-nozzle width branches."""

from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "Projects" / "JK_Pump_Build" / "tools"
sys.path.insert(0, str(TOOLS))

from build_pumps import build_pump                              # noqa: E402
from check_top_nozzle_non_target_unchanged import main as delta_check  # noqa: E402
from extract_project_data import load_all                       # noqa: E402
from verify_pumps import bounds, verify                          # noqa: E402

PREFIX = "top discharge casing connection"
BRIDGE_PREFIX = "top discharge casing offset bridge"


@lru_cache(maxsize=1)
def _sources():
    return load_all()


@lru_cache(maxsize=1)
def _models():
    sources = _sources()
    return {tag: build_pump(tag, sources)
            for tag in sorted(sources["location"])}


def _top_nozzle(model):
    return next((item for item in model.primitives
                 if item.kind == "NOZZLE" and item.ori.endswith(" U")), None)


def _parts(model):
    return sorted((item for item in model.primitives
                   if item.note.startswith(PREFIX)),
                  key=lambda item: bounds(item)[2][0])


def test_every_up_nozzle_uses_the_required_width_branch():
    top_count = 0
    overwidth_count = 0
    direct_count = 0
    for tag, model in _models().items():
        nozzle = _top_nozzle(model)
        parts = _parts(model)
        if nozzle is None:
            assert parts == [], tag
            continue
        top_count += 1
        records = model.facts.get("top_nozzle_connections", [])
        assert len(records) == 1, tag
        record = records[0]
        crown = model.facts["shaft_u"] + model.facts["casing"][0] / 2
        root_u = nozzle.up - nozzle.attrs["HEIG"]
        if record["overwidth"]:
            overwidth_count += 1
            assert parts, tag
            assert all(item.sube == "CASING" for item in parts), tag
            assert all(math.isclose(item.east, nozzle.east, abs_tol=0.01)
                       and math.isclose(item.north, nozzle.north, abs_tol=0.01)
                       for item in parts), tag
            spans = [bounds(item)[2] for item in parts]
            assert spans[0][0] < crown
            assert spans[0][1] > crown
            assert math.isclose(root_u, spans[-1][1], abs_tol=0.01), tag
            for first, second in zip(spans, spans[1:]):
                assert math.isclose(first[1], second[0], abs_tol=0.01), tag
        else:
            direct_count += 1
            assert parts == [], tag
            assert root_u < crown
            external_ratio = (nozzle.up - crown) / nozzle.attrs["HEIG"]
            assert external_ratio >= 0.70 - 0.001, tag
            assert math.isclose(external_ratio, record["external_ratio"],
                                abs_tol=0.001), tag
        assert root_u < nozzle.up
    assert top_count == 28
    assert overwidth_count == 14
    assert direct_count == 14


def test_overwidth_nozzles_use_socket_cone_without_an_extra_neck():
    overwidth = 0
    direct = 0
    for tag, model in _models().items():
        records = model.facts.get("top_nozzle_connections", [])
        if not records:
            continue
        assert len(records) == 1, tag
        record = records[0]
        parts = _parts(model)
        if record["overwidth"]:
            overwidth += 1
            assert [item.kind for item in parts] == ["CYLINDER", "CONE"], tag
            socket, reducer = parts
            assert socket.attrs["DIAM"] <= record["casing_width"], tag
            assert math.isclose(socket.attrs["DIAM"], reducer.attrs["DBOT"], abs_tol=0.01)
            assert math.isclose(reducer.attrs["DTOP"], record["nozzle_diameter"],
                                abs_tol=0.01)
        else:
            direct += 1
            assert parts == [], tag
    assert overwidth == 14
    assert direct == 14


def test_only_205_pu_054_needs_an_offset_solid_casing_bridge():
    bridged = []
    for tag, model in _models().items():
        bridges = [item for item in model.primitives
                   if item.note.startswith(BRIDGE_PREFIX)]
        if bridges:
            bridged.append(tag)
            assert len(bridges) == 1
            assert bridges[0].kind == "CYLINDER"
            assert bridges[0].sube == "CASING"
    assert bridged == ["205-PU-054"]


def test_r12_models_pass_the_independent_relational_verifier():
    sources = _sources()
    for tag, model in _models().items():
        assert verify(model, sources) == [], tag


def test_r9_geometry_is_unchanged_except_top_nozzle_heig_and_added_connectors():
    assert delta_check() == 0
