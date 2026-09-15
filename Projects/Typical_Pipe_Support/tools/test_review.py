"""Geometric rejection tests for the review candidate, including frame mistakes."""
import pytest
from build_review import SOURCE, build, verify, extent, only, build_resume, PROJECT

@pytest.fixture
def candidate():
    source=SOURCE.read_text(encoding="utf-8-sig")
    return source,build(source)

def test_candidate_passes(candidate):
    source,script=candidate
    assert verify(script,source)["hex_heads"]==6

def test_rotated_hex_bounds(candidate):
    _,script=candidate
    head=only(script,"HEX_HEAD_1")[0]
    assert extent(head)[2:4] == (19,31)
    assert extent(head)[4:6] == (45,75)

def test_floating_head_is_rejected(candidate):
    source,script=candidate
    changed=script.replace("POS E -45 N 19 U 60", "POS E -45 N 21 U 60",1)
    assert changed != script
    with pytest.raises(AssertionError): verify(changed,source)

def test_gusset_penetrating_angle_is_rejected(candidate):
    source,script=candidate
    start=script.index("-- UPPER_GUSSET ")
    changed=script[:start]+script[start:].replace("POS E 0.0 N 0.0 U 0.0","POS E -4.0 N 0.0 U 0.0",1)
    assert changed != script
    with pytest.raises(AssertionError): verify(changed,source)

def test_empty_geometry_is_rejected(candidate):
    source,_=candidate
    with pytest.raises(AssertionError): verify("",source)

def test_wall_datum_violation_is_rejected(candidate):
    source,script=candidate
    changed=script.replace("POS E 0.0 N 8.0 U -75.0","POS E 0.0 N 7.0 U -75.0",1)
    assert changed != script
    with pytest.raises(AssertionError): verify(changed,source)

def test_only_the_failed_framework_header_changed(candidate):
    _,script=candidate
    before=(PROJECT/"archive/R1_before_FRMW_fix/Typical_Pipe_Support_R1.pml").read_text(encoding="ascii")
    assert script == before.replace("NEW FRMW /TPS_R1_FRAME\nORI Y IS N AND Z IS U\nPOS E 0 N 0 U 0\n", "NEW FRMW /TPS_R1_FRAME\n",1)

def test_resume_starts_at_existing_framework(candidate):
    _,script=candidate
    resume=build_resume(script)
    commands=[line for line in resume.splitlines() if line and not line.startswith("--")]
    assert commands[:2] == ["/TPS_R1_FRAME","NEW SCTN /TPS_R1_BEAM"]
    assert resume.endswith(script[script.index("NEW SCTN /TPS_R1_BEAM\n"):])
    assert not any(line.startswith(("DELETE ","NEW ZONE ","NEW STRU ","NEW FRMW ")) for line in commands)
