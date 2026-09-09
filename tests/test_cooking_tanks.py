from __future__ import annotations

import hashlib
import math
import re

import pytest

from wsb.composite_builder import (
    build_combined_macro,
    build_equipment_macro,
    validate_equipment_model,
    verify_equipment_macro,
)
from wsb.composite_generate import generate_composite_project
from wsb.pml_builder import NOZZLE_BORE_COMPONENTS, PMLBuilder, validate_pml
from wsb.projects import resolve_project


PROJECT = resolve_project("JK_Cooking_Tank_Build")
MODELS = tuple(PROJECT.tanks())


def test_register_has_all_fifteen_workbook_rows() -> None:
    assert len(MODELS) == 15
    assert len({model.name for model in MODELS}) == 15
    assert all(model.position[2] == -300.0 for model in MODELS)


def test_every_resolved_model_obeys_local_envelope() -> None:
    for model in MODELS:
        validate_equipment_model(model)
        assert min(p.bounds()[4] for p in model.primitives) == 0.0
        assert max(p.bounds()[5] for p in model.primitives) <= model.overall_height


def test_individual_macros_are_pml1_and_numerically_verified() -> None:
    for model in MODELS:
        macro = build_equipment_macro(model)
        assert validate_pml(macro) == []
        assert verify_equipment_macro(model, macro) == []
        assert macro.count("NEW EQUI /") == 1
        assert "SUSPEND" not in macro
        assert "RESUME" not in macro
        assert "END EQUI" not in macro


def test_combined_macro_has_one_independent_equi_per_model() -> None:
    macro = build_combined_macro(MODELS, PROJECT.name)
    assert validate_pml(macro) == []
    assert macro.count("NEW EQUI /") == len(MODELS)
    for model in MODELS:
        assert verify_equipment_macro(model, macro) == []


def test_capacity_tank_height_formula_is_exact() -> None:
    model = next(m for m in MODELS if m.name == "BLEACH_HOT_WATER_TANK")
    diameter = 5020.0
    expected_shell = 100.0e9 / (math.pi * diameter**2 / 4.0)
    shell = next(
        primitive
        for primitive in model.primitives
        if primitive.label == "Capacity cylinder"
    )
    assert shell.height == expected_shell
    assert model.overall_height == 20.0 + expected_shell + diameter * 0.15


def test_blow_tank_profile_preserves_authoritative_top_to_bottom_string() -> None:
    for name in ("BLOW_TANK_1", "BLOW_TANK_2"):
        model = next(m for m in MODELS if m.name == name)
        body = [p for p in model.primitives if p.role == "body"]
        assert [(p.kind, p.height) for p in body] == [
            ("CYLI", 2508.0),
            ("CONE", 2944.0),
            ("CYLI", 8753.0),
            ("CONE", 5898.0),
        ]
        assert [(p.d_bottom, p.d_top) for p in body if p.kind == "CONE"] == [
            (7300.0, 3876.0),
            (555.0, 7300.0),
        ]
        assert sum(p.height for p in body) == 20103.0
        assert body[-1].bounds()[4] == 1848.0
        assert body[-1].bounds()[5] == 7746.0
        assert body[0].bounds()[5] == 21951.0
        assert model.overall_height == 21951.0
        assert model.position[2] + model.overall_height == 21651.0

        legs = [
            p
            for p in model.primitives
            if re.fullmatch(r"Blow-tank support leg \d", p.label)
        ]
        assert len(legs) == 4
        assert all(leg.bounds()[4] == 0.0 for leg in legs)
        assert all(leg.bounds()[5] == 7746.0 for leg in legs)


def test_main_condensate_plan_envelope_is_3400_by_2017() -> None:
    model = next(m for m in MODELS if m.name == "MAIN_CONDENSATE_TANK")
    envelope = model.body_envelope
    assert envelope[1] - envelope[0] == 2017.0
    assert envelope[3] - envelope[2] == 3400.0


def test_accumulator_top_dish_pos_is_shell_tangent_plane() -> None:
    """Regression for the HEIG/2 flying-head fault seen in the user's E3D."""
    model = next(m for m in MODELS if m.name == "ACCUMULATOR_TANK")
    top_head = next(
        p
        for p in model.primitives
        if p.kind == "DISH" and p.axis == "U"
    )
    macro = build_equipment_macro(model)
    block = re.search(
        rf"-- {re.escape(top_head.label)}\nNEW DISH\n"
        rf"DIAM [^\n]+\nHEIG [^\n]+\nRADIUS [^\n]+\n"
        rf"ORI [^\n]+\nPOS E [^ ]+ N [^ ]+ U (-?[\d.]+)",
        macro,
    )
    assert block is not None
    emitted_u = float(block.group(1))
    assert emitted_u == pytest.approx(
        top_head.point[2] + model.position[2], abs=0.1
    )
    shell = next(
        p for p in model.primitives if p.label == "Accumulator cylindrical shell"
    )
    assert shell.bounds()[5] == pytest.approx(top_head.bounds()[4])


def test_every_placeholder_is_one_catalogue_backed_native_nozzle() -> None:
    """No nozzle SUBE may regress to a neck/flange stack of primitives."""
    for model in MODELS:
        assert len(model.native_nozzles) == len(model.nozzle_groups)
        assert all(nozzle.dn in NOZZLE_BORE_COMPONENTS for nozzle in model.native_nozzles)
        assert not any(p.group in model.nozzle_groups for p in model.primitives)
        macro = build_equipment_macro(model)
        assert macro.count("NEW NOZZLE /") == len(model.native_nozzles)
        for nozzle in model.native_nozzles:
            start = macro.index(f"NEW NOZZLE /{model.name}_{nozzle.name}_NOZZ")
            end = macro.index("\nEND", start)
            block = macro[start:end]
            assert block.index("CATR SPCOMPONENT ") < block.index("\nPOS ")
            assert block.index("\nPOS ") < block.index("\nORI P1 IS ")
            assert block.index("\nORI P1 IS ") < block.index("\nHEIG ")


def test_ladders_have_varied_bearings_base_shoes_and_supported_blow_tank_height() -> None:
    bearings = set()
    ladder_models = set()
    for model in MODELS:
        rails = [p for p in model.primitives if "ladder rail" in p.label]
        if not rails:
            continue
        ladder_models.add(model.name)
        match = re.search(r"\b([EWNS])\b", rails[0].label)
        assert match is not None
        bearings.add(match.group(1))
        shoes = [p for p in model.primitives if "ladder base shoe" in p.label]
        assert len(shoes) == 2
        assert all(shoe.bounds()[4] == 0.0 for shoe in shoes)
        assert len(
            [p for p in model.primitives if "connected ladder bracket" in p.label]
        ) >= 4
    assert bearings == {"E", "W", "N", "S"}
    assert ladder_models == {
        "BLEACH_HOT_WATER_TANK",
        "BLOW_TANK_1",
        "BLOW_TANK_2",
        "WARM_WATER_TANK",
        "BROWN_HOT_WATER_TANK",
        "ACCUMULATOR_TANK",
        "W_L_SERVICE_TANK_1",
        "W_L_SERVICE_TANK_2",
        "B_L_TANK",
    }

    for name in ("BLOW_TANK_1", "BLOW_TANK_2"):
        model = next(item for item in MODELS if item.name == name)
        rails = [p for p in model.primitives if "ladder rail" in p.label]
        assert max(rail.bounds()[5] for rail in rails) == pytest.approx(16499.0)
        crossbars = [
            p for p in model.primitives if "ladder-to-leg crossbar" in p.label
        ]
        legs = [
            p
            for p in model.primitives
            if re.fullmatch(r"Blow-tank support leg \d", p.label)
        ]
        assert len(crossbars) >= 2
        for crossbar in crossbars:
            cb = crossbar.bounds()
            assert any(
                cb[0] <= leg.bounds()[1]
                and cb[1] >= leg.bounds()[0]
                and cb[2] <= leg.bounds()[3]
                and cb[3] >= leg.bounds()[2]
                and cb[4] <= leg.bounds()[5]
                and cb[5] >= leg.bounds()[4]
                for leg in legs
            )


def test_blow_tanks_have_ground_mounted_vertical_bottom_entry_agitators() -> None:
    for name in ("BLOW_TANK_1", "BLOW_TANK_2"):
        model = next(item for item in MODELS if item.name == name)
        internal = [p for p in model.primitives if p.group == "INTERNALS"]
        labels = [p.label for p in internal]
        assert not any("side-entry" in label for label in labels)
        shaft = next(
            p
            for p in internal
            if "internal vertical bottom-entry agitator shaft" in p.label
        )
        assert shaft.axis == "U"
        assert shaft.point[0:2] == (0.0, 0.0)
        assert shaft.bounds()[4] < 1848.0 < shaft.bounds()[5]
        assert sum("agitator impeller hub" in label for label in labels) == 2
        assert sum("agitator east-west blade pair" in label for label in labels) == 2
        assert sum("agitator north-south blade pair" in label for label in labels) == 2
        motor = next(p for p in internal if "vertical agitator motor" in p.label)
        gearbox = next(p for p in internal if "agitator gearbox" in p.label)
        housing = next(
            p for p in internal if "packing-box and bearing housing" in p.label
        )
        baseplate = next(
            p for p in internal if "agitator ground baseplate" in p.label
        )
        grout = next(p for p in internal if "agitator non-shrink grout" in p.label)
        assert all(p.point[0:2] == (0.0, 0.0) for p in (motor, gearbox, housing))
        assert grout.bounds()[4] == 0.0
        assert baseplate.bounds()[4] == grout.bounds()[5]
        assert housing.bounds()[5] == 1848.0
        assert sum("agitator ground anchor stud" in label for label in labels) == 4
        assert sum("agitator ground anchor nut" in label for label in labels) == 4


def test_blow_tank_nozzles_keep_their_relative_body_locations() -> None:
    expected_u = {
        "N1": 20610.0,
        "N2": 20110.0,
        "N3": 15110.0,
        "N4": 10310.0,
        "M1": 9310.0,
        "N5": 1848.0,
    }
    for name in ("BLOW_TANK_1", "BLOW_TANK_2"):
        model = next(item for item in MODELS if item.name == name)
        assert {
            nozzle.name: nozzle.face[2] for nozzle in model.native_nozzles
        } == expected_u


def test_r5_scope_freeze_keeps_non_blow_macros_byte_identical_to_r4() -> None:
    expected_hashes = {
        "BLEACH_HOT_WATER_TANK": "fee9685eece1936bd36f95461adacf86a6723f87c610b9cdafad2c4a1a687ffa",
        "WARM_WATER_TANK": "7aea87d1290672dadc01bf7ef35f36b070f9f5baa7ba3c770ff2b7008a54f9e2",
        "BROWN_HOT_WATER_TANK": "ed45993618d81de65c1b2e67e20238aa15e3526f6fb73e930b47a4e0465c4012",
        "JUNK_TRAP_1": "6d0f6274df8e7da57b919e464388aaa2da2441bd8675c3c33a630a73fca36094",
        "JUNK_TRAP_2": "806d5215ba5cf5978a2856308b69157068ce533a7ee7ae17295a70c70e87c6bb",
        "ACCUMULATOR_TANK": "f4ada0d4650fc86ff1d5a15e71f5004bc3e98aa7f4023dac8db92903c76c35ca",
        "ACCUMULATOR_TANK_AID_1": "afb481971830bc367a70f55105f6cc6060967028d87ae47432ab1a40a6f4ea8a",
        "ACCUMULATOR_TANK_AID_2": "af0412f8d6469daac12cbeb627147bbee975bce60eeb5dff0299fc7db89f3724",
        "W_L_SERVICE_TANK_1": "ca7f7a5dc68737e2f75a2de7c1fe56bd8697400db7ca91346c86cae4cacca639",
        "W_L_SERVICE_TANK_2": "2f74d33b60bc579ea00ed0267fb749e069ca2d154fb841ed18bb21287ce1cf56",
        "MAIN_CONDENSATE_TANK": "223e806aa128e2147e05bbf1472dc4785d9d50272af36e816043cf3c8480db94",
        "SPENT_LIQUOR_TANK": "7a7b4800951c674a3bc17fd6596cd87ce56c1521236e8603b1a41790110c0053",
        "B_L_TANK": "6e9e6e2bf4f52d8fd87f01a8c7fc9d2ff873d18c29c75c7471d30b6cff6bb12b",
    }
    for model in MODELS:
        if model.name.startswith("BLOW_TANK_"):
            continue
        macro = build_equipment_macro(model)
        normalized = "\n".join(
            "-- Generated:<normalized>"
            if line.startswith("-- Generated:")
            else line
            for line in macro.splitlines()
        )
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        assert digest == expected_hashes[model.name]


def test_supports_and_anchor_bolts_have_physical_connection_parts() -> None:
    for model in MODELS:
        assert any("nameplate screw" in p.label for p in model.primitives)
        assert any("anchor nut" in p.label for p in model.primitives)

    for name in ("BLOW_TANK_1", "BLOW_TANK_2", "JUNK_TRAP_1", "JUNK_TRAP_2"):
        model = next(item for item in MODELS if item.name == name)
        labels = [p.label for p in model.primitives]
        assert sum("top load-spreader plate" in label for label in labels) == 4
        assert sum("base gusset" in label for label in labels) >= 8
        assert (
            sum(
                "support leg" in label and "non-shrink grout pad" in label
                for label in labels
            )
            == 4
        )
        assert sum("anchor clamp washer plate" in label for label in labels) == 16

    chassis_tanks = [
        model
        for model in MODELS
        if any("bottom base chassis plate" in p.label for p in model.primitives)
    ]
    assert len(chassis_tanks) == 10
    for model in chassis_tanks:
        chassis = next(
            p
            for p in model.primitives
            if "bottom base chassis plate" in p.label
        )
        assert chassis.height == 20.0
        assert chassis.bounds()[4] == 0.0
        assert chassis.bounds()[5] == 20.0
        # All support chair brackets and webs removed on chassis tanks:
        assert not any("anchor chair web" in p.label for p in model.primitives)
        assert not any("anchor clamp plate" in p.label for p in model.primitives)
        stud_count = sum("anchor stud" in p.label for p in model.primitives)
        nut_count = sum("anchor nut" in p.label for p in model.primitives)
        washer_count = sum("anchor washer" in p.label for p in model.primitives)
        assert stud_count == nut_count == washer_count


def test_rotated_box_pml_uses_verified_plan_bearing_before_position() -> None:
    builder = PMLBuilder()
    for angle in (30.0, 120.0, 210.0, 300.0):
        builder.box(
            240.0,
            90.0,
            20.0,
            (1000.0, 1000.0, 26.0),
            plan_rotation_deg=angle,
        )
    macro = builder.build()
    expected_directions = (
        "ORI Z IS U AND X IS E 30 N",
        "ORI Z IS U AND X IS N 30 W",
        "ORI Z IS U AND X IS W 30 S",
        "ORI Z IS U AND X IS S 30 E",
    )
    assert all(direction in macro for direction in expected_directions)
    for block in macro.split("NEW BOX")[1:]:
        assert block.index("ORI Z IS U AND X IS") < block.index("POS E ")

    bad = "\n".join(
        (
            "NEW BOX",
            "XLEN 240",
            "YLEN 90",
            "ZLEN 20",
            "POS E 1000 N 1000 U 26",
            "ORI Z IS U AND X IS E 30 N",
        )
    )
    assert any("before ORI" in problem for problem in validate_pml(bad))


def test_ten_tanks_have_elevated_chassis_and_five_tanks_retain_supports() -> None:
    EXCLUDED_5 = {
        "MAIN_CONDENSATE_TANK",
        "BLOW_TANK_1",
        "BLOW_TANK_2",
        "JUNK_TRAP_1",
        "JUNK_TRAP_2",
    }
    for model in MODELS:
        if model.name in EXCLUDED_5:
            assert not any(
                "bottom base chassis plate" in p.label for p in model.primitives
            )
            if "CONDENSATE" in model.name:
                assert any("Saddle support" in p.label for p in model.primitives)
            else:
                assert any("support leg" in p.label for p in model.primitives)
        else:
            chassis = next(
                p
                for p in model.primitives
                if "bottom base chassis plate" in p.label
            )
            shell_radius = (
                model.primitives[1].cross_diameter / 2.0
            )
            assert chassis.diameter == (shell_radius + 150.0) * 2.0
            assert chassis.height == 20.0
            assert model.body_envelope[4] == 20.0  # body elevated by 20mm
            assert min(p.bounds()[4] for p in model.primitives) == 0.0


def test_generation_writes_fifteen_macros_and_combined_file(tmp_path) -> None:
    result = generate_composite_project(PROJECT, MODELS, output_dir=tmp_path)
    assert result.verified
    assert len(result.macro_paths) == 15
    assert result.combined_path is not None and result.combined_path.is_file()
    assert result.report_path is not None and result.report_path.is_file()
    assert all(path.is_file() for path in result.macro_paths)


def test_base_anchor_nuts_are_hexagonal_extrusions() -> None:
    for model in MODELS:
        anchor_nuts = [p for p in model.primitives if "anchor nut" in p.label]
        assert len(anchor_nuts) > 0, f"{model.name} has no anchor nuts"
        for nut in anchor_nuts:
            assert nut.kind == "EXTRUSION", f"{nut.label} is not EXTRUSION"
            assert len(nut.vertices) == 6, f"{nut.label} does not have 6 hex vertices"
            assert nut.height > 0.0, f"{nut.label} height <= 0"
        macro = build_equipment_macro(model)
        assert "NEW EXTRUSION" in macro
        assert "NEW LOOP" in macro
        assert "NEW VERTEX" in macro


def test_vertical_access_ladders_have_safety_cages() -> None:
    tanks_with_ladders = [
        model for model in MODELS
        if any("ladder rail" in p.label for p in model.primitives)
    ]
    assert len(tanks_with_ladders) == 9  # 9 vertical tanks have ladders
    for model in tanks_with_ladders:
        hoops = [p for p in model.primitives if "ladder safety cage hoop" in p.label]
        vertical_bars = [p for p in model.primitives if "ladder cage vertical bar" in p.label]
        weld_clips = [p for p in model.primitives if "hoop weld clip" in p.label]
        weld_collars = [p for p in model.primitives if "ladder cage weld collar" in p.label]
        weld_caps = [p for p in model.primitives if "ladder cage bar top weld cap" in p.label]
        bracket_pads = [p for p in model.primitives if "bracket shell weld pad" in p.label]

        assert len(hoops) >= 2, f"{model.name} ladder lacks safety cage hoops"
        assert len(vertical_bars) == 7, f"{model.name} ladder does not have 7 vertical cage bars"
        assert len(weld_clips) == len(hoops) * 2, f"{model.name} missing hoop weld clips"
        assert len(weld_collars) == len(hoops) * 7, f"{model.name} missing weld collars"
        assert len(weld_caps) == 7, f"{model.name} missing bar top weld caps"
        assert len(bracket_pads) >= 4, f"{model.name} missing bracket shell weld pads"

        for hoop in hoops:
            assert hoop.kind == "EXTRUSION"
            assert len(hoop.vertices) >= 36, f"{hoop.label} vertices < 36 for smooth arc"
        for bar in vertical_bars:
            assert bar.kind == "CYLI"
            assert bar.diameter == 20.0


def test_tanks_have_appropriate_stiffeners_and_reinforcements() -> None:
    for model in MODELS:
        if model.name.startswith("BLOW_TANK_"):
            stiffeners = [p for p in model.primitives if "stiffener ring" in p.label]
            assert len(stiffeners) == 3, f"{model.name} missing blow-tank stiffener rings"
        elif "WATER_TANK" in model.name or "SERVICE_TANK" in model.name or "B_L_TANK" in model.name:
            stiffeners = [p for p in model.primitives if "stiffening ring" in p.label or "roof curb" in p.label]
            assert len(stiffeners) >= 2, f"{model.name} missing shell stiffeners / roof curb"
        elif "ACCUMULATOR" in model.name:
            stiffeners = [p for p in model.primitives if "stiffener" in p.label or "stiffening ring" in p.label]
            assert len(stiffeners) >= 2, f"{model.name} missing accumulator stiffeners"
        elif "CONDENSATE" in model.name:
            stiffeners = [p for p in model.primitives if "stiffener gusset" in p.label]
            assert len(stiffeners) == 4, f"{model.name} missing saddle stiffener gussets"
        elif "JUNK_TRAP" in model.name:
            stiffeners = [p for p in model.primitives if "cone transition stiffener ring" in p.label]
            assert len(stiffeners) == 1, f"{model.name} missing junk trap cone stiffener"

