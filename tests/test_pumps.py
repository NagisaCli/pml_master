"""Regression tests for the independent JK pump macros."""

from __future__ import annotations

import hashlib
import re
from functools import lru_cache

from wsb.projects import resolve_project
from wsb.pump_builder import (
    derive_detail_profile,
    derive_pump_geometry,
    verify_pump,
)
from wsb.pump_generate import generate_pumps


_IMMUTABLE_PROJECT_DATA = {
    "203-PU-008": ((13971, 14110, 0), 2136, 852, "N", "U", "N"),
    "203-PU-009": ((16137, 14089, 0), 2129, 857, "N", "U", "N"),
    "203-PU-011": ((17685, 170, 0), 1720, 760, "N", "U", "N"),
    "203-PU-020": ((17095, 5685, 0), 926, 760, "W", "U", "W"),
    "203-PU-026": ((13809, 358, 0), 1720, 760, "S", "U", "S"),
    "203-PU-031": ((15108, 175, 0), 1353, 631, "S", "U", "S"),
    "204-PU-003": ((20162, -8768, 0), 2129, 857, "N", "U", "N"),
    "204-PU-008": ((20000, 19210, 0), 1720, 760, "E", "U", "E"),
    "204-PU-006": ((20000, 17410, 0), 1725, 760, "E", "U", "E"),
    "204-PU-015": ((22512, 14092, 0), 2135, 863, "N", "U", "N"),
    "204-PU-016": ((28213, 14089, 0), 2129, 857, "N", "U", "N"),
    "204-PU-017": ((25814, 14294, 0), 1720, 760, "N", "U", "N"),
    "204-PU-023": ((28520, 415, 0), 1725, 760, "N", "U", "N"),
    "205-PU-004": ((30441, -10580, 0), 1725, 760, "E", "U", "E"),
    "205-PU-012": ((33065, 13825, 0), 2701, 1245, "N", "U", "N"),
    "205-PU-013": ((31566, 14294, 0), 1720, 760, "N", "U", "N"),
    "205-PU-018": ((35723, 5019, 0), 2022, 1051, "S", "W", "W"),
    "205-PU-024": ((41518, 660, 0), 1720, 760, "S", "U", "S"),
    "205-PU-027": ((42218, -8620, 0), 2135, 857, "N", "U", "N"),
    "205-PU-030": ((40868, 14089, 0), 2129, 863, "N", "U", "N"),
    "205-PU-031": ((37916, 14089, 0), 2129, 857, "N", "U", "N"),
    "205-PU-032": ((39418, 14294, 0), 1671, 765, "N", "U", "N"),
    "205-PU-038": ((43119, 5016, 0), 2000, 1051, "S", "W", "W"),
    "205-PU-046": ((45221, 14294, 0), 1720, 760, "N", "U", "N"),
    "205-PU-047": ((46620, 14089, 0), 2129, 863, "N", "U", "N"),
    "205-PU-048": ((48221, 14089, 0), 2129, 863, "N", "U", "N"),
    "205-PU-049": ((49674, 14294, 0), 1720, 760, "N", "U", "N"),
    "205-PU-054": ((48852, 4714, 0), 2000, 1046, "N", "U", "N"),
    "205-PU-060": ((46154, -10854, 0), 1720, 760, "E", "U", "E"),
    "205-PU-061": ((46154, -8256, 0), 1720, 760, "E", "U", "E"),
}

_PRE_FASTENER_FIX_NON_TARGET_SHA256 = (
    "a5fce5959232cda68bb343c5fd4a52a5f0c75b4027f9caa4e28734ec8d2dc57c"
)


def _canonical_non_target_geometry(script: str) -> str:
    """Exclude only the two user-authorized fastener SUBEs from a macro."""
    kept = []
    skipping = False
    for line in script.splitlines():
        if re.match(
            r"^NEW SUBE /.*_(?:BASE_FASTENERS|CASING_FASTENERS)\s*$",
            line,
        ):
            skipping = True
            continue
        if skipping and re.match(r"^NEW (?:SUBE|NOZZ|EQUI)\b", line):
            skipping = False
        if not skipping and line.strip() and not line.lstrip().startswith("--"):
            kept.append(line.rstrip())
    return "\n".join(kept)


def _section_cylinders(script: str, section_name: str):
    block = re.search(
        rf"(?ms)^NEW SUBE /{re.escape(section_name)}\n"
        r"(.*?)(?=^NEW (?:SUBE|NOZZ|EQUI)\b|\Z)",
        script,
    )
    assert block, section_name
    pattern = re.compile(
        r"(?ms)^-- (?P<label>[^\n]+)\n"
        r"NEW CYLI\n"
        r"DIAM (?P<diam>-?[\d.]+)\n"
        r"HEIG (?P<height>-?[\d.]+)\n"
        r"ORI [^\n]+\n"
        r"POS E (?P<east>-?[\d.]+) N (?P<north>-?[\d.]+) "
        r"U (?P<up>-?[\d.]+)$"
    )
    return [
        {
            "label": match.group("label"),
            "diam": float(match.group("diam")),
            "height": float(match.group("height")),
            "east": float(match.group("east")),
            "north": float(match.group("north")),
            "up": float(match.group("up")),
        }
        for match in pattern.finditer(block.group(1))
    ]


@lru_cache(maxsize=1)
def _result():
    project = resolve_project("JK_Pump_Build")
    return generate_pumps(project=project)


def test_all_30_pumps_validate_independently():
    result = _result()
    assert len(result.pumps) == 30
    assert result.verified
    for pump in result.pumps:
        assert verify_pump(pump.spec, pump.macro) == []


def test_each_macro_has_one_equi_and_two_native_nozzles():
    result = _result()
    for pump in result.pumps:
        equis = re.findall(r"^NEW EQUI /(.+)$", pump.macro, re.MULTILINE)
        nozzles = re.findall(r"^NEW NOZZLE /(.+)$", pump.macro, re.MULTILINE)
        assert equis == [pump.spec.safe_tag]
        assert len(nozzles) == 2
        assert all(name.startswith(pump.spec.safe_tag + "_") for name in nozzles)


def test_client_confirmed_coordinates_and_thickness_are_applied():
    result = _result()
    by_tag = {pump.spec.tag: pump.spec for pump in result.pumps}
    assert by_tag["205-PU-046"].position == (45221, 14294, 0)
    assert by_tag["205-PU-061"].position == (46154, -8256, 0)
    assert {pump.baseplate_thickness for pump in by_tag.values()} == {50.0}


def test_high_detail_pass_cannot_change_any_contractual_project_parameter():
    result = _result()
    actual = {
        pump.spec.tag: (
            pump.spec.position,
            pump.spec.length,
            pump.spec.width,
            pump.spec.suction_axis,
            pump.spec.discharge_axis,
            pump.spec.layout_axis,
        )
        for pump in result.pumps
    }
    assert actual == _IMMUTABLE_PROJECT_DATA
    assert {pump.spec.baseplate_thickness for pump in result.pumps} == {50.0}


def test_corrected_motor_envelopes_are_realistically_proportioned():
    """Keep the user-corrected drivers substantial without changing project data."""
    result = _result()
    for pump in result.pumps:
        spec = pump.spec
        geometry = derive_pump_geometry(spec)
        if spec.is_mc:
            assert geometry.motor_length >= spec.length * 0.325
            assert geometry.motor_height >= spec.width * 0.40
        else:
            assert geometry.motor_length >= spec.length * 0.375
            assert geometry.motor_height >= spec.width * 0.43
        assert geometry.motor_width == spec.width * 0.60


def test_motor_coupling_bearing_and_casing_do_not_interpenetrate():
    result = _result()
    for pump in result.pumps:
        spec, geometry = pump.spec, pump.geometry
        motor_front = geometry.motor_centre_l + geometry.motor_length / 2.0
        casing_rear = geometry.casing_centre_l - geometry.casing_length / 2.0
        motor_to_casing_gap = casing_rear - motor_front
        bearing_length = min(
            max(55.0, motor_to_casing_gap) * 0.52,
            spec.length * 0.12,
        )
        bearing_start = casing_rear - bearing_length
        assert motor_front < bearing_start < casing_rear
        assert abs(
            (bearing_start - motor_front) - geometry.coupling_length
        ) <= 1e-6


def test_high_detail_models_have_realistic_subsystems_and_fasteners():
    result = _result()
    signatures = set()
    for pump in result.pumps:
        profile = derive_detail_profile(pump.spec, pump.geometry)
        signatures.add(profile.signature)
        minimum = 145 if pump.spec.is_mc else 105
        assert pump.primitive_count >= minimum
        assert "_BASE_FASTENERS" in pump.macro
        assert "_CASING_FASTENERS" in pump.macro
        assert "_BEARING_FRAME" in pump.macro
        assert "_DRIVER_FASTENERS" in pump.macro
        assert "cap/hex-head envelope" in pump.macro
        assert "terminal-box lid screw head" in pump.macro
        assert "finned IEC TEFC motor stator barrel" in pump.macro
        assert {
            "ROUND": "full rounded coupling guard",
            "TAPERED": "tapered coupling guard",
            "BOXED": "fabricated rectangular coupling guard",
            "VENTED_CAGE": "ventilated guard cage rail",
        }[profile.guard_style.name] in pump.macro
        assert pump.macro.count("360-degree motor cooling rib ") == (
            profile.motor_fin_count
        )
        assert "open fan-grille horizontal bar" in pump.macro
        assert "open fan-grille vertical bar" in pump.macro
        assert "motor fan grille face" not in pump.macro
        assert "cast motor foot mounting pad" in pump.macro
        assert "barrel-connected motor foot web" in pump.macro
        assert pump.macro.count("baseplate anchor fastener") == (
            profile.anchor_bolt_count * 3
        )
        assert pump.macro.count("casing split-line bolt") == (
            profile.casing_bolt_count * 3
        )

    # Service families must create material alternatives, while genuinely
    # matched drawings are allowed to retain the same construction.
    assert len(signatures) >= 12


def test_only_authorized_fastener_sections_changed_from_loaded_model():
    canonical = _canonical_non_target_geometry(_result().combined_macro)
    assert hashlib.sha256(canonical.encode("utf-8")).hexdigest() == (
        _PRE_FASTENER_FIX_NON_TARGET_SHA256
    )


def test_base_anchors_and_casing_flange_fasteners_are_physically_seated():
    for pump in _result().pumps:
        spec = pump.spec
        base = _section_cylinders(
            pump.macro,
            f"{spec.safe_tag}_BASE_FASTENERS",
        )
        assert len(base) % 3 == 0
        plate_top = spec.position[2] + spec.baseplate_thickness
        for index in range(0, len(base), 3):
            shank, washer, head = base[index : index + 3]
            shank_bottom = shank["up"] - shank["height"] / 2.0
            shank_top = shank["up"] + shank["height"] / 2.0
            washer_bottom = washer["up"] - washer["height"] / 2.0
            washer_top = washer["up"] + washer["height"] / 2.0
            head_bottom = head["up"] - head["height"] / 2.0
            head_top = head["up"] + head["height"] / 2.0
            assert abs(washer_bottom - plate_top) <= 0.11
            assert abs(head_bottom - washer_top) <= 0.11
            assert abs(shank_top - head_top) <= 0.11
            assert spec.position[2] <= shank_bottom < plate_top

        casing = _section_cylinders(
            pump.macro,
            f"{spec.safe_tag}_CASING_FASTENERS",
        )
        assert len(casing) % 3 == 0
        geometry = pump.geometry
        profile = derive_detail_profile(spec, geometry)
        rear_l = geometry.casing_centre_l - geometry.casing_length / 2.0
        rear_fraction, body_fraction, flange_ratio = {
            "PROCESS_VOLUTE": (0.12, 0.60, 1.075),
            "FILTRATE_VOLUTE": (0.14, 0.56, 1.050),
            "STOCK_VOLUTE": (0.10, 0.64, 1.100),
            "HIGH_HEAD_VOLUTE": (0.16, 0.58, 1.065),
            "CLEAN_WATER_VOLUTE": (0.15, 0.55, 1.040),
            "ABRASIVE_VOLUTE": (0.10, 0.65, 1.120),
            "CHEMICAL_VOLUTE": (0.14, 0.58, 1.080),
            "MC_FLUIDIZER": (0.12, 0.58, 1.100),
        }[profile.casing_style.name]
        split_l = rear_l + geometry.casing_length * (
            rear_fraction + body_fraction
        )
        forward = {
            "E": (1.0, 0.0),
            "W": (-1.0, 0.0),
            "N": (0.0, 1.0),
            "S": (0.0, -1.0),
        }[spec.layout_axis]
        cross = (-forward[1], forward[0])
        cover_root_r = geometry.casing_diameter * 0.98 / 2.0
        flange_outer_r = geometry.casing_diameter * flange_ratio / 2.0
        expected_circle_r = (cover_root_r + flange_outer_r) / 2.0

        def local_geometry(cylinder):
            east = cylinder["east"] - spec.position[0]
            north = cylinder["north"] - spec.position[1]
            centre_l = east * forward[0] + north * forward[1]
            centre_t = east * cross[0] + north * cross[1]
            radial = (
                centre_t**2
                + (cylinder["up"] - spec.position[2] - geometry.shaft_u) ** 2
            ) ** 0.5
            half = cylinder["height"] / 2.0
            return centre_l - half, centre_l + half, radial

        for index in range(0, len(casing), 3):
            shank, washer, head = casing[index : index + 3]
            shank_min, shank_max, shank_r = local_geometry(shank)
            washer_min, washer_max, washer_r = local_geometry(washer)
            head_min, head_max, head_r = local_geometry(head)
            assert abs(washer_min - split_l) <= 0.11
            assert abs(head_min - washer_max) <= 0.11
            assert abs(shank_max - head_max) <= 0.11
            assert shank_min < split_l
            for radius in (shank_r, washer_r, head_r):
                assert cover_root_r <= radius <= flange_outer_r
                assert abs(radius - expected_circle_r) <= 0.11


def test_evidence_based_profiles_are_diverse_without_fake_unique_models():
    result = _result()
    by_tag = {pump.spec.tag: pump for pump in result.pumps}
    core_profiles = {
        (
            pump.spec.appearance.motor_style,
            pump.spec.appearance.casing_style,
            pump.spec.appearance.guard_style,
            pump.spec.appearance.fin_count,
            pump.spec.appearance.casing_bolt_count,
            pump.spec.appearance.casing_rib_count,
            pump.spec.appearance.bearing_sections,
            pump.spec.appearance.mc_variant,
        )
        for pump in result.pumps
    }
    assert 10 <= len(core_profiles) < 30
    assert (
        by_tag["205-PU-060"].spec.appearance
        == by_tag["205-PU-061"].spec.appearance
    )
    assert (
        by_tag["203-PU-026"].spec.appearance
        == by_tag["205-PU-024"].spec.appearance
    )
    assert {
        pump.spec.appearance.terminal_mount_side for pump in result.pumps
    } == {0}


def test_tag_specific_top_view_features_change_actual_geometry():
    result = _result()
    by_tag = {pump.spec.tag: pump for pump in result.pumps}
    assert "205-PU-027 stock-casing lateral branch" in by_tag["205-PU-027"].macro
    assert (
        "enlarged MC separation/control side package"
        not in by_tag["205-PU-018"].macro
    )
    assert (
        "enlarged MC separation/control side package"
        in by_tag["205-PU-038"].macro
    )
    assert (
        "D1 MC orthogonal auxiliary-drive barrel"
        in by_tag["205-PU-054"].macro
    )
    for tag in ("203-PU-020", "205-PU-004"):
        assert by_tag[tag].spec.top_view is None
        assert "NO_VIEW" in by_tag[tag].spec.appearance.mc_variant


def test_service_classification_covers_all_supplied_process_uses():
    result = _result()
    assert {pump.spec.duty.name for pump in result.pumps} == {
        "DILUTION",
        "FILTRATE",
        "SCREEN_FEED",
        "BOOSTER",
        "WIRE_WASH",
        "WASHER_FEED",
        "MEDIUM_CONSISTENCY",
        "SCRUBBER_CIRCULATION",
    }


def test_motor_is_opposite_the_suction_end():
    result = _result()
    direction = {
        "E": (1.0, 0.0),
        "W": (-1.0, 0.0),
        "N": (0.0, 1.0),
        "S": (0.0, -1.0),
    }
    for pump in result.pumps:
        spec = pump.spec
        forward = direction[spec.layout_axis]
        motor_world = (
            spec.position[0] + forward[0] * pump.geometry.motor_centre_l,
            spec.position[1] + forward[1] * pump.geometry.motor_centre_l,
        )
        signed = (
            (motor_world[0] - spec.position[0]) * forward[0]
            + (motor_world[1] - spec.position[1]) * forward[1]
        )
        assert signed < 0, f"{spec.tag}: motor is not opposite suction"


def _nozzle_position_and_direction(macro: str, name: str):
    block = re.search(
        rf"(?ms)^NEW NOZZLE /{re.escape(name)}\n(.*?)(?=^NEW |\Z)",
        macro,
    )
    assert block, name
    position = re.search(
        r"^POS E (-?[\d.]+) N (-?[\d.]+) U (-?[\d.]+)$",
        block.group(1),
        re.MULTILINE,
    )
    orientation = re.search(
        r"^ORI P1 IS ([ENSWUD])$", block.group(1), re.MULTILINE
    )
    assert position and orientation
    return tuple(float(value) for value in position.groups()), orientation.group(1)


def test_205_018_and_205_038_special_layout_is_east_west_and_coplanar():
    result = _result()
    by_tag = {pump.spec.tag: pump for pump in result.pumps}
    for tag in ("205-PU-018", "205-PU-038"):
        pump = by_tag[tag]
        spec = pump.spec
        assert spec.layout_axis == "W"
        assert spec.suction_axis == "S"
        assert spec.discharge_axis == "W"
        assert spec.world_baseplate_dimensions == (
            spec.length,
            spec.width,
            50.0,
        )

        suction, suction_direction = _nozzle_position_and_direction(
            pump.macro, f"{spec.safe_tag}_SUCTION_NOZZLE"
        )
        discharge, discharge_direction = _nozzle_position_and_direction(
            pump.macro, f"{spec.safe_tag}_DISCHARGE_NOZZLE"
        )
        assert suction_direction == "S"
        assert discharge_direction == "W"
        assert suction[2] == discharge[2]
        assert suction[1] < spec.position[1]
        assert discharge[0] < spec.position[0]

        # Local positive points west from the east-side driver to the west casing.
        driver_east = (
            spec.position[0] - pump.geometry.motor_centre_l
        )
        casing_west = (
            spec.position[0] - pump.geometry.casing_centre_l
        )
        assert driver_east > spec.position[0]
        assert casing_west < spec.position[0]


def test_other_28_pumps_keep_suction_defined_longitudinal_layout():
    result = _result()
    specials = {"205-PU-018", "205-PU-038"}
    ordinary = [pump.spec for pump in result.pumps if pump.spec.tag not in specials]
    assert len(ordinary) == 28
    assert all(spec.layout_axis == spec.suction_axis for spec in ordinary)


def test_generation_writes_individual_files_and_one_click_combined_macro(tmp_path):
    project = resolve_project("JK_Pump_Build")
    result = generate_pumps(project=project, output_dir=tmp_path)
    files = sorted((tmp_path / "pumps").glob("*.pml"))
    assert len(files) == 30
    assert {path.stem for path in files} == {
        pump.spec.tag for pump in result.pumps
    }
    assert result.combined_macro_path == (
        tmp_path / "JK_Pump_Build_All_Pumps.pml"
    )
    assert result.combined_macro_path.is_file()
    assert result.combined_problems == []
    assert re.findall(
        r"^NEW EQUI /(.+)$", result.combined_macro, re.MULTILINE
    ) == [pump.spec.safe_tag for pump in result.pumps]
    assert len(
        re.findall(r"^NEW NOZZLE /(.+)$", result.combined_macro, re.MULTILINE)
    ) == 60
    assert len(
        re.findall(
            r"^CATR SPCOMPONENT /(.+)$",
            result.combined_macro,
            re.MULTILINE,
        )
    ) == 60
    assert result.verification_report_path.is_file()
    assert result.uncertainty_report_path.is_file()
    assert all(
        "\r" not in path.read_text(encoding="utf-8")
        for path in [*files, result.combined_macro_path]
    )


def test_filtered_generation_does_not_overwrite_formal_combined_macro(tmp_path):
    project = resolve_project("JK_Pump_Build")
    full = generate_pumps(project=project, output_dir=tmp_path)
    combined_path = full.combined_macro_path
    assert combined_path is not None
    original = combined_path.read_bytes()

    subset = generate_pumps(
        pumps=[full.pumps[0].spec],
        project=project,
        output_dir=tmp_path,
    )
    assert subset.combined_macro_path is None
    assert combined_path.read_bytes() == original
