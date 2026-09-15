"""Reject the user-observed unsupported framework orientation attribute."""
import pytest
from wsb.pml_builder import validate_pml

@pytest.mark.parametrize("kind", ["FRMW", "FRMWORK", "FRAMEWORK"])
def test_reject_framework_orientation(kind):
    errors=validate_pml(f"NEW {kind} /F\nORI Y IS N AND Z IS U\n")
    assert any("FRMWORK does not have attribute ORI" in e for e in errors)

def test_allow_orientation_on_child_geometry():
    assert not validate_pml("NEW FRMW /F\nNEW BOX\nXLEN 10\nYLEN 10\nZLEN 10\nORI Z IS U AND X IS E\nPOS E 0 N 0 U 0\n")

def test_reselect_known_framework():
    errors=validate_pml("NEW FRMW /F\nNEW SCTN /S\n/F\nORI Y IS N AND Z IS U\n")
    assert any("FRMWORK does not have attribute ORI" in e for e in errors)

def test_comment_and_other_owner_do_not_trigger():
    assert not validate_pml("NEW FRMW /F\n-- ORI Y IS N AND Z IS U\n/OTHER\nORI Y IS N AND Z IS U\n")
