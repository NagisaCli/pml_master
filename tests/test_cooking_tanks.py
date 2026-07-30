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
    assert model.overall_height == expected_shell + diameter * 0.15


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
        "BLEACH_HOT_WATER_TANK": "2c421878b2ca2bcfacafdd3113fbe03091c796b575963f3f3aaa631f9a705dbe",
        "WARM_WATER_TANK": "3225d1fff3fdaad92ceba68894be4dfb3ac0e4702bfaa816b87ecae2727b9b9e",
        "BROWN_HOT_WATER_TANK": "8ec9d27a75004bae9516451434e9b0427daac8fd3242d7d02b1204fbea9e3b32",
        "JUNK_TRAP_1": "bd7c4e2c20c63097609b5207bb724d669ead420f19c264f03e6c81daa62a279f",
        "JUNK_TRAP_2": "13580042f39aeb2292ff4e61b0320aaabdbf23a32e02237f3af398cb9dac0a4c",
        "ACCUMULATOR_TANK": "4208e0d68a802aeff3b5e6e914b0637a7a5703ef6783927887a2dd04b02b5cc3",
        "ACCUMULATOR_TANK_AID_1": "a43dbcb46a1f9cd43e27fcd1720a5703ecb92057c0417f4cb5cbda2697917131",
        "ACCUMULATOR_TANK_AID_2": "608bc9ad71f69eff1ab7260c29a6f63c2dcff4a8735f06c4fb92fbe3ba9156b4",
        "W_L_SERVICE_TANK_1": "aedca83d6aaa3c09bf63f6e3a542f4ce946e002623f6c388a45d3b91ae25b7d9",
        "W_L_SERVICE_TANK_2": "b00d51c5592940897ebd590dbdb23f2d6845db89ca2047c1a835a3d68c64f55e",
        "MAIN_CONDENSATE_TANK": "67d06efa8212022d12f44022a031bedc7de6f446085d20eaf5d4b2d16bfcc4d2",
        "SPENT_LIQUOR_TANK": "8971478c3e9ac2e37ce465987e0a8f7040dcfcdd5c0961d230ad89bb3b911d0f",
        "B_L_TANK": "1ff5d3b18fda190a98fb010e2384a69674b74a6ffc05d4991bc63c75e06ca9a6",
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

    ground_or_skirt = [
        model
        for model in MODELS
        if any("anchor chair web" in p.label for p in model.primitives)
    ]
    assert len(ground_or_skirt) == 10
    for model in ground_or_skirt:
        clamp_count = sum("anchor clamp plate" in p.label for p in model.primitives)
        chair_count = sum("anchor chair web" in p.label for p in model.primitives)
        stud_count = sum("anchor stud" in p.label for p in model.primitives)
        assert clamp_count == chair_count == stud_count


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


def test_perimeter_anchor_plates_are_radial_and_tangent_to_the_shell() -> None:
    off_axis_count = 0
    for model in MODELS:
        clamps = [
            p for p in model.primitives if "anchor clamp plate" in p.label
        ]
        if not clamps:
            continue
        macro = build_equipment_macro(model)
        for clamp in clamps:
            centre_radius = math.hypot(clamp.point[0], clamp.point[1])
            expected_angle = (
                math.degrees(math.atan2(clamp.point[1], clamp.point[0])) % 360.0
            )
            assert clamp.plan_rotation_deg == pytest.approx(expected_angle)
            assert clamp.xlen == pytest.approx(240.0)
            assert clamp.ylen == pytest.approx(90.0)

            index = clamp.label.rsplit(" ", 1)[-1]
            stud = next(
                p
                for p in model.primitives
                if p.label.endswith(f"anchor stud {index}")
            )
            stud_radius = math.hypot(stud.point[0], stud.point[1])
            shell_radius = stud_radius - 150.0
            assert centre_radius - clamp.xlen / 2.0 < shell_radius
            assert centre_radius + clamp.xlen / 2.0 > stud_radius

            if not math.isclose(
                expected_angle % 90.0, 0.0, abs_tol=1e-9
            ):
                off_axis_count += 1
                start = macro.index(f"-- {clamp.label}")
                block = macro[start : macro.index("\n\n", start)]
                assert "ORI Z IS U AND X IS " in block
                assert block.index("ORI Z IS U AND X IS ") < block.index(
                    "POS E "
                )
    assert off_axis_count > 0


def test_generation_writes_fifteen_macros_and_combined_file(tmp_path) -> None:
    result = generate_composite_project(PROJECT, MODELS, output_dir=tmp_path)
    assert result.verified
    assert len(result.macro_paths) == 15
    assert result.combined_path is not None and result.combined_path.is_file()
    assert result.report_path is not None and result.report_path.is_file()
    assert all(path.is_file() for path in result.macro_paths)
