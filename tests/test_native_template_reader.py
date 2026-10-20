"""Native template ownership and spatial validation regression properties."""

import math

import pytest

from wsb.pml_builder import validate_pml
from wsb.pml_parser import native_orientation_basis, parse_native_tree


def test_nested_negative_and_profile_keep_their_actual_owner():
    text = """NEW EQUIPMENT /TEST
POS E 0mm N 0mm U 0mm
NEW SUBEQUIPMENT /TEST_DRIVER
NEW CONE
ORI Y IS U AND Z IS E
POS E 10mm N 0mm U 300mm
NEW NCONE
HEIG 20mm
END
END
NEW EXTRUSION
HEIG 10mm
NEW LOOP
NEW VERTEX
END
NEW VERTEX
POS W 10mm N 5mm U 0mm
END
END
END
END
END
"""
    root = parse_native_tree(text)[0]
    cone, extrusion = root.children[0].children
    assert cone.children[0].kind == "NCONE"
    assert cone.get("POS") == "E 10mm N 0mm U 300mm"
    vertices = extrusion.children[0].children
    assert vertices[0].get("POS") is None
    assert vertices[1].get("POS") == "W 10mm N 5mm U 0mm"
    assert [node.kind for node in root.walk()].count("VERTEX") == 2


@pytest.mark.parametrize("text", ["NEW BOX\n", "END\n", "POS E 0mm\n", "-- Empty\n"])
def test_native_reader_fails_loudly_on_unbalanced_or_empty_input(text):
    with pytest.raises(ValueError):
        parse_native_tree(text)


def test_motor_fin_quadrant_is_an_orthonormal_right_handed_frame():
    axes = native_orientation_basis("Y IS E AND Z IS N 80 D")
    assert axes["Z"] == pytest.approx((0, math.cos(math.radians(80)), -math.sin(math.radians(80))))
    for axis in "XYZ":
        assert sum(x * x for x in axes[axis]) == pytest.approx(1)
    for a, b in (("X", "Y"), ("Y", "Z"), ("Z", "X")):
        assert sum(x * y for x, y in zip(axes[a], axes[b])) == pytest.approx(0)
    x, y = axes["X"], axes["Y"]
    assert (x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0]) == pytest.approx(axes["Z"])


@pytest.mark.parametrize("orientation", ["Y IS E AND Z IS E", "Y IS E AND Z IS N 91 D", "Y IS E AND Z IS N 10 S"])
def test_native_orientation_rejects_invalid_frames(orientation):
    with pytest.raises(ValueError):
        native_orientation_basis(orientation)


def test_native_validation_is_opt_in_and_preserves_order_and_nozzle_rules():
    script = "NEW BOX\nORI Y IS E AND Z IS N 80 D\nPOS E 0mm N 0mm U 300mm\nEND\n"
    assert validate_pml(script)
    assert not validate_pml(script, native_templates=True)
    reversed_order = script.replace("ORI Y IS E AND Z IS N 80 D\nPOS E 0mm N 0mm U 300mm", "POS E 0mm N 0mm U 300mm\nORI Y IS E AND Z IS N 80 D")
    assert any("before ORI" in p for p in validate_pml(reversed_order, native_templates=True))
    bad_nozzle = "NEW NOZZLE /N\nPOS E 0mm N 0mm U 0mm\nORI Y IS E AND Z IS U\nEND\n"
    assert validate_pml(bad_nozzle, native_templates=True)
