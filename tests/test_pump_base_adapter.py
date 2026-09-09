"""Regression coverage for the /P1501B-BASE per-pump adapter."""

from __future__ import annotations

import hashlib
import math
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "Projects" / "JK_Pump_Build" / "tools"
sys.path.insert(0, str(TOOLS))

from base_deform import (ANCHOR_INDICES, LOWER_GUSSET_INDICES,  # noqa: E402
                         OUTER_STAY_INDICES,
                         REF_MOTOR_BOTTOM, REF_MOTOR_RADIUS,
                         REF_MOTOR_SUPPORT_TOP, REF_PLATE_T,
                         REF_PLATE_UNDER, REF_PUMP_BOTTOM,
                         REF_PUMP_RADIUS, REF_PUMP_SUPPORT_TOP,
                         SADDLE_GUSSET_INDICES, SOLE_PLATE_INDICES,
                         SOURCE, WASHER_INDICES, orientation_basis,
                         parse_reference, profile_centre, rotate_ori)
from build_pumps import build_pump                            # noqa: E402
from check_base_shape import check as check_base_shape        # noqa: E402
from check_macro_text import check as check_emitted_macro     # noqa: E402
from extract_project_data import load_all                     # noqa: E402
from verify_pumps import bounds, verify                        # noqa: E402

REFERENCE_SHA256 = "d8c17257e318162fc4bbdc901c82ea2c2811e7e3775da860c5f7a770ec9101af"


@lru_cache(maxsize=1)
def _sources():
    return load_all()


@lru_cache(maxsize=1)
def _models():
    sources = _sources()
    return tuple(build_pump(tag, sources) for tag in sorted(sources["location"]))


def test_preserved_base_reference_bytes_are_the_user_supplied_master():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == REFERENCE_SHA256


def test_every_pump_has_exactly_the_reference_43_members_and_no_duplicate_plate():
    expected = Counter({"BOX": 11, "PYRAMID": 12,
                        "EXTRUSION": 10, "CYLINDER": 10})
    for model in _models():
        base = [member for member in model.primitives if member.sube == "BASE"]
        assert len(base) == 43, model.tag
        assert Counter(member.kind for member in base) == expected, model.tag
        assert not any(member.sube == "BASEPLATE" for member in model.primitives), model.tag


def test_all_reference_members_preserve_local_axes_dimensions_and_profiles():
    reference = parse_reference()
    for model in _models():
        assert check_base_shape(model, reference) == [], model.tag


def test_default_oriented_members_rotate_with_each_pump_direction():
    reference = parse_reference()
    default_indices = {element.index for element in reference if element.ori is None}
    by_direction = {}
    for model in _models():
        by_direction.setdefault(model.facts["wet_end"], model)
    assert set(by_direction) == {"N", "S", "E", "W"}
    for direction, model in by_direction.items():
        for member in (item for item in model.primitives if item.sube == "BASE"):
            index = int(member.note.split("element ", 1)[1].split(":", 1)[0])
            if index in default_indices:
                assert member.ori == rotate_ori(None, direction)


def test_every_offset_pyramid_leans_toward_the_machine_centreline():
    for model in _models():
        wet = model.facts["wet_end"]
        along = {"N": (0.0, 1.0), "S": (0.0, -1.0),
                 "E": (1.0, 0.0), "W": (-1.0, 0.0)}[wet]
        across = (along[1], -along[0])
        plate_e, plate_n = model.facts["plate_centre"]
        for member in (item for item in model.primitives
                       if item.sube == "BASE" and item.kind == "PYRAMID"):
            xoff = member.attrs.get("XOFF", 0.0)
            yoff = member.attrs.get("YOFF", 0.0)
            if abs(xoff) + abs(yoff) < 0.001:
                continue
            basis = orientation_basis(member.ori)
            top_e = member.east + basis["X"][0] * xoff + basis["Y"][0] * yoff
            top_n = member.north + basis["X"][1] * xoff + basis["Y"][1] * yoff
            base_offset = ((member.east - plate_e) * across[0]
                           + (member.north - plate_n) * across[1])
            top_offset = ((top_e - plate_e) * across[0]
                          + (top_n - plate_n) * across[1])
            assert abs(top_offset) <= abs(base_offset) + 0.01, (
                model.tag, member.note, base_offset, top_offset)


def test_every_hex_head_is_coaxial_with_one_anchor_shaft():
    for model in _models():
        washers = [item for item in model.primitives
                   if item.sube == "BASE" and item.kind == "EXTRUSION"]
        unused_bolts = [item for item in model.primitives
                        if item.sube == "BASE" and item.kind == "CYLINDER"]
        assert len(washers) == len(unused_bolts) == 10, model.tag
        for washer in washers:
            local_x, local_y = profile_centre(washer.profile or [])
            basis = orientation_basis(washer.ori)
            centre = (
                washer.east + basis["X"][0] * local_x
                + basis["Y"][0] * local_y,
                washer.north + basis["X"][1] * local_x
                + basis["Y"][1] * local_y,
            )
            bolt = min(unused_bolts, key=lambda item: math.hypot(
                item.east - centre[0], item.north - centre[1]))
            assert math.hypot(bolt.east - centre[0],
                              bolt.north - centre[1]) < 0.001, (
                                  model.tag, washer.note, bolt.note)
            unused_bolts.remove(bolt)


def test_structural_members_form_one_load_path_to_the_skid_without_hardware():
    tolerance = 0.6
    for model in _models():
        placed = {
            int(member.note.split("element ", 1)[1].split(":", 1)[0]): member
            for member in model.primitives if member.sube == "BASE"
        }
        structure = {index: placed[index] for index in range(1, 20)}
        structure.update({index: placed[index] for index in range(40, 44)})
        adjacency = {index: set() for index in structure}
        indices = sorted(structure)
        for offset, first in enumerate(indices):
            first_bounds = bounds(structure[first])
            for second in indices[offset + 1:]:
                second_bounds = bounds(structure[second])
                touches = all(
                    min(first_bounds[axis][1], second_bounds[axis][1])
                    >= max(first_bounds[axis][0], second_bounds[axis][0])
                    - tolerance
                    for axis in range(3))
                if touches:
                    adjacency[first].add(second)
                    adjacency[second].add(first)
        connected = set()
        pending = [2, 40, 41, 42, 43]
        while pending:
            index = pending.pop()
            if index in connected:
                continue
            connected.add(index)
            pending.extend(adjacency[index] - connected)
        assert connected == set(structure), (
            model.tag, sorted(set(structure) - connected))


def test_adaptive_bearing_faces_and_fixed_hardware_thicknesses():
    reference = {element.index: element for element in parse_reference()}
    reference_anchor = reference[min(ANCHOR_INDICES)]
    reference_anchor_bottom = (
        reference_anchor.pos["up"] - reference_anchor.attrs["HEIG"] / 2)
    for model in _models():
        placed = {
            int(member.note.split("element ", 1)[1].split(":", 1)[0]): member
            for member in model.primitives if member.sube == "BASE"
        }
        scale = model.facts["plate"][2] / REF_PLATE_T
        sole_tops = {}
        for index in SOLE_PLATE_INDICES:
            low, high = bounds(placed[index])[2]
            assert abs(low - model.facts["plate_top"]) < 0.01, (
                model.tag, index, low)
            station = placed[index].note.rsplit("(", 1)[-1].split(" station", 1)[0]
            sole_tops[station] = max(sole_tops.get(station, -math.inf), high)
        for index in LOWER_GUSSET_INDICES:
            station = placed[index].note.rsplit("(", 1)[-1].split(" station", 1)[0]
            assert abs(bounds(placed[index])[2][0] - sole_tops[station]) < 0.01, (
                model.tag, index)
            pad_index = 1 if station == "pump" else 13
            pad_bottom = bounds(placed[pad_index])[2][0]
            assert abs(bounds(placed[index])[2][1] - pad_bottom) < 0.01, (
                           model.tag, index)
            assert abs(placed[index].up
                       - (sole_tops[station] + pad_bottom) / 2) < 0.01, (
                           model.tag, index, "PYRAMID POS is not its centre")
        for index in OUTER_STAY_INDICES:
            station = placed[index].note.rsplit("(", 1)[-1].split(" station", 1)[0]
            assert abs(bounds(placed[index])[2][0] - sole_tops[station]) < 0.01, (
                model.tag, index)
            assert abs(placed[index].up
                       - (sole_tops[station] + bounds(placed[index])[2][1]) / 2
                       ) < 0.01, (
                           model.tag, index, "PYRAMID POS is not its centre")
        mounting_pad_top = bounds(placed[1])[2][1]
        for index in SADDLE_GUSSET_INDICES:
            assert abs(bounds(placed[index])[2][0] - mounting_pad_top) < 0.01, (
                model.tag, index)

        unused_anchors = [placed[index] for index in sorted(ANCHOR_INDICES)]
        expected_anchor_bottom = (
            model.facts["plate_under"]
            + (reference_anchor_bottom - REF_PLATE_UNDER) * scale)
        for index in sorted(WASHER_INDICES):
            washer = placed[index]
            station = washer.note.rsplit("(", 1)[-1].split(" station", 1)[0]
            washer_low, washer_high = bounds(washer)[2]
            assert abs(washer_low - sole_tops[station]) < 0.01, (
                model.tag, index)
            assert abs(washer.attrs["HEIG"]
                       - reference[index].attrs["HEIG"] * scale) < 0.01, (
                           model.tag, index)
            local_x, local_y = profile_centre(washer.profile or [])
            basis = orientation_basis(washer.ori)
            centre = (washer.east + basis["X"][0] * local_x
                      + basis["Y"][0] * local_y,
                      washer.north + basis["X"][1] * local_x
                      + basis["Y"][1] * local_y)
            anchor = min(unused_anchors, key=lambda item: math.hypot(
                item.east - centre[0], item.north - centre[1]))
            anchor_low, anchor_high = bounds(anchor)[2]
            assert abs(anchor_low - expected_anchor_bottom) < 0.01, (
                model.tag, index)
            assert abs(anchor_high - washer_high) < 0.01, (model.tag, index)
            unused_anchors.remove(anchor)


def test_rounded_emitted_macro_keeps_all_hex_heads_on_anchor_axes(tmp_path):
    path = tmp_path / "all_pumps.pml"
    path.write_text("\n".join(model.to_pml() for model in _models()),
                    encoding="utf-8")
    assert check_emitted_macro(path) == []


def test_station_tops_preserve_reference_machine_overlap():
    for model in _models():
        base = [member for member in model.primitives if member.sube == "BASE"]
        relations = (
            ("pump", "CASING", REF_PUMP_BOTTOM, REF_PUMP_SUPPORT_TOP,
             REF_PUMP_RADIUS),
            ("motor", "DRIVER", REF_MOTOR_BOTTOM, REF_MOTOR_SUPPORT_TOP,
             REF_MOTOR_RADIUS),
        )
        for station, sube, ref_bottom, ref_top, ref_radius in relations:
            barrels = [member for member in model.primitives
                       if member.sube == sube and member.kind == "CYLINDER"]
            if not barrels:
                continue
            barrel = next(
                (member for member in barrels if "volute barrel" in member.note),
                max(barrels, key=lambda member: member.attrs.get("HEIG", 0)))
            machine_bottom = bounds(barrel)[2][0]
            radius = barrel.attrs["DIAM"] / 2
            expected = machine_bottom + (ref_top - ref_bottom) * radius / ref_radius
            actual = max(bounds(member)[2][1] for member in base
                         if f"({station} station)" in member.note)
            assert abs(actual - expected) < 0.01, model.tag


def test_full_numeric_verifier_accepts_every_adapted_pump():
    sources = _sources()
    for model in _models():
        assert verify(model, sources) == [], model.tag
