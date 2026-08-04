"""Regression guards for the first native PIPE syntax study."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path

from wsb.piping_builder import (
    BranchSpec,
    ElbowSpec,
    PipeSpec,
    PipingBuilder,
    VerticalReducerSpec,
)
from wsb.pml_builder import validate_pml


REPO_ROOT = Path(__file__).resolve().parent.parent
LAB = REPO_ROOT / "Projects" / "E3D_Syntax_Lab"
NATIVE = LAB / "imports" / "2026-07-30_pipe_native.txt"
CANDIDATES = (
    LAB / "experiments" / "PML-STUDY-PIPE-001" / "candidate"
)
RESULTS = LAB / "experiments" / "PML-STUDY-PIPE-001" / "results"
NATIVE_SHA256 = (
    "a2e80b00c9b009f56260925b72fefe4e0508006bfdc9be374f983b9db5437a77"
)


def _lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _pipe_candidates() -> list[Path]:
    """Return numbered PIPE study macros, excluding standalone DRAWING tests."""
    return sorted(path for path in CANDIDATES.glob("*.pml") if path.stem[:1].isdigit())


def test_native_pipe_evidence_is_preserved_byte_for_byte():
    assert NATIVE.is_file()
    digest = hashlib.sha256(NATIVE.read_bytes()).hexdigest()
    assert digest == NATIVE_SHA256


def test_round2_user_evidence_is_preserved_byte_for_byte():
    expected = {
        "06_elbow_arrive2_leave1_pass.png": (
            "46146b0146769a668e95578f4480b30193a1063acc31ab1c67685ea31c7df901"
        ),
        "07_reducer_vertical_native_axes_pass.png": (
            "be303abbe66e4f2c82115964a0951fcf4f3a4a12c844fcd045fef72cec59f597"
        ),
    }
    for name, digest in expected.items():
        path = RESULTS / name
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest


def test_cluster_crash_sir_is_preserved_byte_for_byte():
    expected = {
        "SIR-20260730-184519-collections-addin-crash.txt": (
            "4abb9671646f22efbcec507734a7f4ebd211c5c0125b000f0d821d02cb487cc3"
        ),
        "SIR-20260730-185650-delete-crash.txt": (
            "13b35f12689c3118183151a60dc45119dea5594b13553de15a421d5ae6a86def"
        ),
    }
    for name, digest in expected.items():
        path = RESULTS / name
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest


def test_documented_native_pipe_inventory_matches_evidence():
    counts = Counter()
    for line in _lines(NATIVE):
        match = re.match(r"^NEW\s+(\S+)", line)
        if match:
            counts[match.group(1).upper()] += 1

    expected = {
        "SITE": 3,
        "ZONE": 4,
        "PIPE": 84,
        "BRANCH": 166,
        "ELBOW": 354,
        "TEE": 103,
        "FLANGE": 155,
        "GASKET": 170,
        "VALVE": 74,
        "REDUCER": 24,
    }
    for element, count in expected.items():
        assert counts[element] == count, (
            f"native evidence inventory changed for {element}: "
            f"{counts[element]} != {count}"
        )


def test_native_piping_components_are_consistently_pos_then_ori():
    current_type = None
    pose: list[str] = []
    checked = 0

    def close_block() -> None:
        nonlocal checked
        if current_type and "POS" in pose and "ORI" in pose:
            assert pose.index("POS") < pose.index("ORI"), (
                f"native NEW {current_type} contains ORI before POS"
            )
            checked += 1

    for raw in _lines(NATIVE):
        line = raw.strip()
        new = re.match(r"^NEW\s+(\S+)", line)
        if new:
            close_block()
            current_type = new.group(1).upper()
            pose = []
        elif line == "END":
            close_block()
            current_type = None
            pose = []
        elif current_type:
            verb = re.match(r"^(POS|ORI)\b", line)
            if verb:
                pose.append(verb.group(1))
    close_block()

    assert checked == 1013


def test_all_pipe_candidates_pass_the_general_pml_validator():
    candidates = _pipe_candidates()
    assert [p.name for p in candidates] == [
        "01_pipe_core.pml",
        "02_pose_pos_then_ori.pml",
        "03_pose_ori_then_pos.pml",
        "04_tee_branch_refs.pml",
        "05_slope_1in100.pml",
        "06_elbow_arrive2_leave1.pml",
        "07_reducer_vertical_native_axes.pml",
        "08_balanced_pipe_cluster.pml",
        "09_cluster_core_straight_slope.pml",
        "10_cluster_components_elbow_reducer.pml",
        "11_high_density_all_components.pml",
        "13_tee_gasket_query_kit.pml",
        "14_advanced_inline_families.pml",
        "15_advanced_pose_families.pml",
        "16_connection_first_network.pml",
        "17_cap_fire_spec.pml",
    ]
    for candidate in candidates:
        problems = validate_pml(candidate.read_text(encoding="utf-8"))
        assert not problems, f"{candidate.name}:\n" + "\n".join(problems)


def test_candidate_input_blocks_are_balanced():
    for candidate in _pipe_candidates():
        lines = _lines(candidate)
        new_count = sum(bool(re.match(r"^NEW\s+", line)) for line in lines)
        end_count = sum(line == "END" for line in lines)
        assert new_count == end_count, (
            f"{candidate.name}: {new_count} NEW blocks but {end_count} END lines"
        )
        assert lines.count("INPUT BEGIN") == 1
        assert lines.count("INPUT FINISH") == 1


def test_pose_pair_reverses_only_the_elbow_pose_contract():
    def elbow_pose(name: str) -> list[str]:
        lines = _lines(CANDIDATES / name)
        start = lines.index("NEW ELBOW")
        end = lines.index("END", start)
        return [
            line
            for line in lines[start + 1 : end]
            if line.startswith(("POS ", "ORI "))
        ]

    assert elbow_pose("02_pose_pos_then_ori.pml") == [
        "POS E 0mm N 0mm U 2000mm",
        "ORI Y is D and Z is N",
    ]
    assert elbow_pose("03_pose_ori_then_pos.pml") == [
        "ORI Y is D and Z is N",
        "POS E 0mm N 0mm U 2000mm",
    ]


def test_round2_elbow_restores_native_arrive_leave():
    text = (CANDIDATES / "06_elbow_arrive2_leave1.pml").read_text(
        encoding="utf-8"
    )
    assert "SPRE SPCOMPONENT /A3B/EA100" in text
    assert re.search(r"(?m)^ARRI 2$", text)
    assert re.search(r"(?m)^LEAV 1$", text)


def test_round2_reducer_uses_native_vertical_axes():
    text = (CANDIDATES / "07_reducer_vertical_native_axes.pml").read_text(
        encoding="utf-8"
    )
    assert "SPRE SPCOMPONENT /A3B/RC100X80" in text
    assert "ORI Y is N and Z is E" in text


def test_candidate08_matches_shared_builder_and_balances_verified_forms():
    pipes = (
        PipeSpec(
            name="/CODEX-P08-01-HEADER",
            specification="/A3B",
            bore=100,
            temperature_c=50,
            branches=(
                BranchSpec(
                    name="/CODEX-P08-01-HEADER/B1",
                    head=(0, 0, 0),
                    tail=(12000, 0, 0),
                    head_direction="E",
                    tail_direction="W",
                    head_bore=100,
                    tail_bore=100,
                    tube_component="/A3B/PA100",
                ),
            ),
        ),
        PipeSpec(
            name="/CODEX-P08-02-SLOPE",
            specification="/A1A",
            bore=100,
            temperature_c=50,
            slope_ref="/1in100",
            branches=(
                BranchSpec(
                    name="/CODEX-P08-02-SLOPE/B1",
                    head=(0, 2500, 100),
                    tail=(10000, 2500, 0),
                    head_direction="E 0.5729 D",
                    tail_direction="W 0.5729 U",
                    head_bore=100,
                    tail_bore=100,
                    tube_component="/A1A/PA100",
                    slope_ref="/1in100",
                ),
            ),
        ),
        PipeSpec(
            name="/CODEX-P08-03-ELBOW",
            specification="/A3B",
            bore=100,
            temperature_c=50,
            branches=(
                BranchSpec(
                    name="/CODEX-P08-03-ELBOW/B1",
                    head=(0, 5000, 0),
                    tail=(-4000, 5000, 2000),
                    head_direction="U",
                    tail_direction="E",
                    head_bore=100,
                    tail_bore=100,
                    tube_component="/A3B/PA100",
                    components=(
                        ElbowSpec(
                            position=(0, 5000, 2000),
                            component="/A3B/EA100",
                            leave_tube="/A3B/PA100",
                            bore=100,
                        ),
                    ),
                ),
            ),
        ),
        PipeSpec(
            name="/CODEX-P08-04-REDUCER",
            specification="/A3B",
            bore=100,
            temperature_c=50,
            branches=(
                BranchSpec(
                    name="/CODEX-P08-04-REDUCER/B1",
                    head=(4000, 7500, 3000),
                    tail=(4000, 7500, 0),
                    head_direction="D",
                    tail_direction="U",
                    head_bore=100,
                    tail_bore=80,
                    tube_component="/A3B/PA100",
                    components=(
                        VerticalReducerSpec(
                            position=(4000, 7500, 1500),
                            component="/A3B/RC100X80",
                            leave_tube="/A3B/PA80",
                            head_bore=100,
                            tail_bore=80,
                        ),
                    ),
                ),
            ),
        ),
    )
    generated = PipingBuilder().extend(pipes).build()
    candidate = (CANDIDATES / "08_balanced_pipe_cluster.pml").read_text(
        encoding="utf-8"
    )
    start = candidate.index("NEW PIPE /CODEX-P08")
    end = candidate.index("\nEND\nEND\n\nINPUT END SITE /CODEX-PIPE-LAB08")
    embedded = candidate[start:end].rstrip() + "\n"

    assert embedded == generated
    assert generated.count("NEW PIPE ") == 4
    assert generated.count("NEW BRANCH ") == 4
    assert generated.count("SLOREF SLOELE /1in100") == 2
    assert generated.count("NEW ELBOW") == 1
    assert generated.count("NEW REDUCER") == 1


def test_crash_isolation_candidates_split_core_and_component_forms():
    core = (CANDIDATES / "09_cluster_core_straight_slope.pml").read_text(
        encoding="utf-8"
    )
    components = (
        CANDIDATES / "10_cluster_components_elbow_reducer.pml"
    ).read_text(encoding="utf-8")

    assert core.count("NEW PIPE ") == 2
    assert core.count("NEW BRANCH ") == 2
    assert core.count("SLOREF SLOELE /1in100") == 2
    assert "NEW ELBOW" not in core
    assert "NEW REDUCER" not in core

    assert components.count("NEW PIPE ") == 2
    assert components.count("NEW BRANCH ") == 2
    assert components.count("NEW ELBOW") == 1
    assert components.count("NEW REDUCER") == 1
    assert "SLOREF SLOELE" not in components


def test_candidate11_is_a_high_density_all_component_stress_output():
    path = CANDIDATES / "11_high_density_all_components.pml"
    text = path.read_text(encoding="utf-8")
    assert validate_pml(text) == []
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "f655678400cd5ea69aa346996aaae72aa13a10766496ff0a539183efc7a339ff"
    )
    assert text.count("NEW PIPE ") == 16
    assert text.count("NEW BRANCH ") == 16
    assert text.count("NEW FLANGE") == 12
    assert text.count("NEW GASKET") == 12
    assert text.count("NEW VALVE") == 16
    assert text.count("NEW INSTRUMENT ") == 12
    assert text.count("NEW ELBOW") == 16
    assert text.count("NEW TEE") == 16
    assert text.count("NEW REDUCER") == 12
    assert text.count("NEW OLET") == 12
    assert text.count("NEW COUPLING") == 16
    assert text.count("NEW BEND") == 12
    assert text.count("NEW FILTER") == 12
    assert text.count("NEW CLOSURE") == 16
    assert text.count("NEW WELD") == 12
    assert text.count("NEW CAP") == 4
    assert text.count("SLOREF SLOELE /1in100") == 12


def test_tee_gasket_query_error_evidence_is_preserved_byte_for_byte():
    path = RESULTS / "evidence/2026-08-04_tee_gasket_query_error.txt"
    assert path.is_file()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "f044f47a258f9002650447cd8c8eacfc2dde505278d276eebceef99ff24a233f"
    )


def test_tee_gasket_query_success_evidence_is_preserved_byte_for_byte():
    path = RESULTS / "evidence/2026-08-04_tee_gasket_query_success.txt"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "Cref /CODEX-Q13-TEE/B2" in text
    assert "Spref /A3B/GC20" in text
    assert "Height 0mm" in text


def test_candidate09_att_evidence_is_preserved_byte_for_byte():
    path = RESULTS / "evidence/2026-08-04_candidate09_att.txt"
    assert path.is_file()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "2b7a9dd70a20ba447b2ce03d6fb3659029ad2e0e206f935f770b4b9453bb1ab2"
    )


def test_advanced_candidates_are_native_slices_with_isolated_names():
    fourteen = (CANDIDATES / "14_advanced_inline_families.pml").read_text(
        encoding="utf-8"
    )
    for pipe in (
        "/CODEX-QFILTER",
        "/CODEX-QCLOSURE",
        "/CODEX-QFBLIND",
        "/CODEX-QCOUPLING",
        "/CODEX-QWELD",
    ):
        assert f"NEW PIPE {pipe}" in fourteen
    assert "/FIRE/" not in fourteen
    assert "/100-B-" not in fourteen
    assert "SPECIFICATION SPECIFICATION" not in fourteen

    fifteen = (CANDIDATES / "15_advanced_pose_families.pml").read_text(
        encoding="utf-8"
    )
    for pipe in ("/CODEX-QBEND", "/CODEX-QOLET", "/CODEX-QPTAPPING"):
        assert f"NEW PIPE {pipe}" in fifteen
    assert "/FIRE/" not in fifteen
    assert "/General-Tappings/TAPPING-200mm" in fifteen
    assert "SPECIFICATION SPECIFICATION" not in fifteen

    seventeen = (CANDIDATES / "17_cap_fire_spec.pml").read_text(
        encoding="utf-8"
    )
    assert "/FIRE/CAP-6" in seventeen
    assert "SPECIFICATION SPECIFICATION" not in seventeen


def test_connection_first_network_keeps_only_internal_references():
    text = (CANDIDATES / "16_connection_first_network.pml").read_text(
        encoding="utf-8"
    )
    assert "NEW PIPE /CODEX-Q16-NET" in text
    assert "NEW BRANCH /CODEX-Q16-NET/B1" in text
    assert "NEW BRANCH /CODEX-Q16-NET/B2" in text
    assert "NEW BRANCH /CODEX-Q16-NET/B3" in text
    assert "HREF OLET 1 of BRANCH /CODEX-Q16-NET/B1" in text
    assert "TREF OLET 2 of BRANCH /CODEX-Q16-NET/B1" in text
    assert "HREF TEE 2 of BRANCH /CODEX-Q16-NET/B1" in text
    assert "/CODEX-Q16-NETA" not in text
    assert "/CODEX-Q16-NETB" not in text
    assert "TREF NOZZLE" not in text
    assert "OLD VALVE /V100" not in text
    assert "OLD VALVE /V101" not in text


def test_tee_gasket_query_pack_points_to_self_contained_kit():
    path = LAB / "experiments/PML-STUDY-PIPE-001/queries/12_query_tee_gasket.mac"
    text = path.read_text(encoding="utf-8")
    commands = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("--")
    ]
    assert commands == []
    assert "13_tee_gasket_query_kit.pml" in text


def test_tee_gasket_query_kit_is_self_contained_and_valid():
    path = CANDIDATES / "13_tee_gasket_query_kit.pml"
    text = path.read_text(encoding="utf-8")
    assert validate_pml(text) == []
    assert "NEW SITE /CODEX-PIPE-LAB13" in text
    assert "SPRE SPCOMPONENT /A1A/TA150" in text
    assert "SPRE SPCOMPONENT /A3B/GC20" in text
    assert "OLD TEE 1 of BRANCH /CODEX-Q13-TEE/B1" in text
    assert "CREF BRANCH /CODEX-Q13-TEE/B2 TAIL" in text
    assert "TREF TEE 1 of BRANCH /CODEX-Q13-TEE/B1" in text
    assert "OLD GASKET 1 of BRANCH /CODEX-Q13-GASKET/B1" in text
    commands = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("--")
    ]
    assert commands.count("Q ATT") == 2
    # Queries run inside the INPUT transaction while the SITE is current, so
    # no post-INPUT world-navigation paths are attempted.
    assert not any("CODEX-PIPE-LAB13/" in command for command in commands)
    assert not any(command.startswith("ONERROR") for command in commands)
    assert "Q NAME ANSWER" not in [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("--")
    ]
