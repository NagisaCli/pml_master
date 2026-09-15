import pytest
from rebuild_r3 import BASE,EQ,build_r3,verify_r3,labelled
from wsb.pml_parser import parse_primitives

@pytest.fixture
def candidate():
    base=BASE.read_text(encoding="ascii")
    return base,build_r3(base)

def test_complete_reconstruction(candidate):
    base,script=candidate
    check=verify_r3(script,base)
    assert check["negative_bores"]==12

def test_positive_extrusion_survives_negative_children(candidate):
    _,script=candidate
    p,block=labelled(script,"UPPER_MOUNT_PLATE")
    assert block.count("NEW NCYLINDER")==4
    assert p["kind"]=="EXTRUSION" and p["heig"]==16
    assert len(p["vertices"])==8
    assert p["orientation"]=="Y IS U AND Z IS N"
    assert p["up"]==-75

def test_cut_end_outside_node_is_rejected(candidate):
    base,script=candidate
    script=script.replace("POSS E 0 N 80 U -452.444658", "POSS E 0 N 16 U -470")
    assert script!=candidate[1]
    with pytest.raises(AssertionError): verify_r3(script,base)

def test_negative_as_sube_child_is_rejected(candidate):
    base,script=candidate
    script=script.replace("NEW NCYLINDER", "END\nNEW NCYLINDER",1)
    with pytest.raises(AssertionError): verify_r3(script,base)

def test_uncut_washer_is_rejected(candidate):
    base,script=candidate
    _,block=labelled(script,"WASHER_1")
    changed=script.replace(block,block.replace("NAPPFLAG 2","NAPPFLAG 0",1),1)
    with pytest.raises(AssertionError): verify_r3(changed,base)

def test_missing_geometry_cannot_pass(candidate):
    base,_=candidate
    with pytest.raises(AssertionError): verify_r3("",base)

def test_wrong_owner_frame_bore_is_rejected(candidate):
    base,script=candidate
    _,block=labelled(script,"WASHER_1")
    changed=script.replace(block,block.replace("POS E 0.000000 N 0.000000 U 0.000000", "POS E 0.000000 N 17.500000 U 0.000000",1),1)
    assert changed!=script
    with pytest.raises(AssertionError): verify_r3(changed,base)
