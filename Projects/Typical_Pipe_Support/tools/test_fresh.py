import pytest
from build_fresh import SOURCE,fresh_script,verify_fresh

def test_full_load_has_no_r1_dependencies():
    source=SOURCE.read_text(encoding="utf-8-sig")
    assert verify_fresh(fresh_script(source),source)["requires_existing_R1"] is False

def test_missing_frame_creation_is_rejected():
    source=SOURCE.read_text(encoding="utf-8-sig")
    script=fresh_script(source).replace("NEW FRMW /TPS_R2_FRAME", "/TPS_R2_FRAME")
    with pytest.raises(AssertionError,match="Uncreated model dependency"):
        verify_fresh(script,source)

def test_old_frame_selection_is_rejected():
    source=SOURCE.read_text(encoding="utf-8-sig")
    script=fresh_script(source).replace("NEW FRMW /TPS_R2_FRAME", "/TPS_R1_FRAME")
    with pytest.raises(AssertionError): verify_fresh(script,source)
