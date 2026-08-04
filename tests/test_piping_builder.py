"""Regression tests for the evidence-gated PIPE / BRANCH generator."""

from __future__ import annotations

import pytest

from wsb.piping_builder import (
    BranchSpec,
    ElbowSpec,
    NativeCatalogueComponentSpec,
    PipeSpec,
    PipingBuilder,
    VerticalReducerSpec,
    build_pipe,
)
from wsb.pml_builder import PMLValidationError, validate_pml


def _straight_branch(**changes) -> BranchSpec:
    values = {
        "name": "/CODEX-P100/B1",
        "head": (0.0, 0.0, 0.0),
        "tail": (4000.0, 0.0, 0.0),
        "head_direction": "E",
        "tail_direction": "W",
        "head_bore": 100.0,
        "tail_bore": 100.0,
        "tube_component": "/A3B/PA100",
    }
    values.update(changes)
    return BranchSpec(**values)


def test_builds_user_confirmed_implicit_straight_tube_form():
    macro = build_pipe(
        PipeSpec(
            name="/CODEX-P100",
            specification="/A3B",
            bore=100.0,
            temperature_c=50.0,
            branches=(_straight_branch(),),
        )
    )

    assert macro == (
        "NEW PIPE /CODEX-P100\n"
        "BORE 100mm\n"
        "TEMP 50degC\n"
        "PRES 0pascal\n"
        "TPRESS 0pascal\n"
        "PSPE SPECIFICATION /A3B\n"
        "NEW BRANCH /CODEX-P100/B1\n"
        "HPOS E 0mm N 0mm U 0mm\n"
        "TPOS E 4000mm N 0mm U 0mm\n"
        "HDIR E\n"
        "TDIR W\n"
        "LHEA true\n"
        "LTAI true\n"
        "HBOR 100mm\n"
        "TBOR 100mm\n"
        "HCON OPEN\n"
        "TCON OPEN\n"
        "TEMP 50degC\n"
        "PRES 0pascal\n"
        "TPRESS 0pascal\n"
        "HSTU SPCOMPONENT /A3B/PA100\n"
        "PSPE SPECIFICATION /A3B\n"
        "END\n"
        "END\n"
    )
    assert validate_pml(macro) == []


def test_builds_user_confirmed_slope_reference_on_pipe_and_branch():
    branch = _straight_branch(
        head=(0.0, 0.0, 100.0),
        tail=(10000.0, 0.0, 0.0),
        head_direction="E 0.5729 D",
        tail_direction="W 0.5729 U",
        slope_ref="/1in100",
        tube_component="/A1A/PA100",
    )
    macro = build_pipe(
        PipeSpec(
            name="/CODEX-P100",
            specification="/A1A",
            bore=100.0,
            slope_ref="/1in100",
            branches=(branch,),
        )
    )

    assert macro.count("SLOREF SLOELE /1in100") == 2
    assert "HDIR E 0.5729 D" in macro
    assert "TDIR W 0.5729 U" in macro


def test_builder_counts_multiple_pipes_and_branches():
    pipe1 = PipeSpec(
        name="/P1",
        specification="/A3B",
        branches=(_straight_branch(name="/P1/B1"),),
    )
    pipe2 = PipeSpec(
        name="/P2",
        specification="/A3B",
        branches=(
            _straight_branch(name="/P2/B1"),
            _straight_branch(name="/P2/B2", head=(0, 1000, 0), tail=(4000, 1000, 0)),
        ),
    )
    builder = PipingBuilder().extend((pipe1, pipe2))

    macro = builder.build()

    assert builder.pipe_count == 2
    assert builder.branch_count == 3
    assert macro.count("NEW PIPE ") == 2
    assert macro.count("NEW BRANCH ") == 3


@pytest.mark.parametrize(
    ("change", "message"),
    (
        ({"head_bore": 0}, "HBOR"),
        ({"tail_bore": -80}, "TBOR"),
        ({"head_direction": "SIDEWAYS"}, "HDIR"),
        ({"tube_component": "A3B/PA100"}, "HSTU"),
        ({"tail": (0.0, 0.0, 0.0)}, "must differ"),
    ),
)
def test_rejects_physically_or_syntactically_invalid_branch(change, message):
    with pytest.raises(PMLValidationError, match=message):
        _straight_branch(**change)


def test_rejects_branch_slope_that_disagrees_with_pipe():
    branch = _straight_branch(name="/P1/B1", slope_ref="/1in100")
    with pytest.raises(PMLValidationError, match="differs"):
        PipeSpec(
            name="/P1",
            specification="/A3B",
            slope_ref="/1in200",
            branches=(branch,),
        )


def test_rejects_branch_named_outside_its_pipe():
    with pytest.raises(PMLValidationError, match="beneath its PIPE"):
        PipeSpec(
            name="/P1",
            specification="/A3B",
            branches=(_straight_branch(name="/P2/B1"),),
        )


def test_builds_user_confirmed_elbow_arrive2_leave1_contract():
    elbow = ElbowSpec(
        position=(0, 0, 2000),
        component="/A3B/EA100",
        leave_tube="/A3B/PA100",
        bore=100,
    )
    branch = _straight_branch(
        name="/P1/B1",
        tail=(-4000, 0, 2000),
        head_direction="U",
        tail_direction="E",
        components=(elbow,),
    )
    macro = build_pipe(
        PipeSpec(name="/P1", specification="/A3B", branches=(branch,))
    )

    start = macro.index("NEW ELBOW")
    component = macro[start : macro.index("END", start)]
    assert component.splitlines() == [
        "NEW ELBOW",
        "POS E 0mm N 0mm U 2000mm",
        "ORI Y IS D AND Z IS N",
        "BUIL false",
        "SHOP true",
        "SPRE SPCOMPONENT /A3B/EA100",
        "LSTU SPCOMPONENT /A3B/PA100",
        "ARRI 2",
        "LEAV 1",
        "ORIF true",
        "POSF true",
    ]


def test_builds_user_confirmed_vertical_reducer_axes():
    reducer = VerticalReducerSpec(
        position=(0, 0, 1500),
        component="/A3B/RC100X80",
        leave_tube="/A3B/PA80",
        head_bore=100,
        tail_bore=80,
    )
    branch = _straight_branch(
        name="/P1/B1",
        head=(0, 0, 3000),
        tail=(0, 0, 0),
        head_direction="D",
        tail_direction="U",
        tail_bore=80,
        components=(reducer,),
    )
    macro = build_pipe(
        PipeSpec(name="/P1", specification="/A3B", branches=(branch,))
    )

    assert "NEW REDUCER\nPOS E 0mm N 0mm U 1500mm" in macro
    assert "ORI Y IS N AND Z IS E" in macro
    assert "SPRE SPCOMPONENT /A3B/RC100X80" in macro
    assert "LSTU SPCOMPONENT /A3B/PA80" in macro


def test_rejects_component_bore_mismatch():
    elbow = ElbowSpec(
        position=(0, 0, 2000),
        component="/A3B/EA80",
        leave_tube="/A3B/PA80",
        bore=80,
    )
    with pytest.raises(PMLValidationError, match="must match"):
        _straight_branch(components=(elbow,))


def test_rejects_multi_component_route_until_certified():
    elbow = ElbowSpec(
        position=(0, 0, 2000),
        component="/A3B/EA100",
        leave_tube="/A3B/PA100",
        bore=100,
    )
    with pytest.raises(PMLValidationError, match="one verified"):
        _straight_branch(components=(elbow, elbow))


def test_native_stress_component_can_copy_multiple_catalogue_blocks_explicitly():
    flange = NativeCatalogueComponentSpec(
        element_type="FLANGE",
        position=(0, 0, 0),
        orientation="Y is E and Z is U",
        spref="/A3B/FO100",
        lstu="/A3B/PA100",
        attributes=(("ARRI", "2"), ("LEAV", "1"), ("RLOC", "2")),
    )
    valve = NativeCatalogueComponentSpec(
        element_type="VALVE",
        name="/STRESS-V1",
        position=(0, 0, 300),
        orientation="Y is E and Z is U",
        spref="/A3B/VG100",
        lstu="/A3B/PA100",
    )
    branch = _straight_branch(components=(flange, valve))
    macro = build_pipe(
        PipeSpec(name="/CODEX-P100", specification="/A3B", branches=(branch,))
    )

    assert "NEW FLANGE" in macro
    assert "RLOC 2" in macro
    assert "NEW VALVE /STRESS-V1" in macro
    assert validate_pml(macro) == []
