-- Macro: Candidate 02 - Rectangular Platform Handrail (6000x4000mm)
-- Study: PML-STUDY-HANDRA-001 (AVEVA E3D Design)
-- Hierarchy: STRU -> FRMWORK -> HANDRA
-- ----------------------------------------------------------------

NEW STRU /CODEX_HR_RECT_02_STRU
NEW FRMWORK /CODEX_HR_RECT_02_FRMWORK

NEW HANDRA /CODEX_HANDRA_RECT_02
POS E 0mm N 0mm U 1000mm
RAILHE 1250mm 750mm
POSTSP 1200mm
TANGOF 300mm
SHOWKP true
BRAD 150mm
FIRE 0
BUIL false
SHOP false

NEW RPATH

NEW POINTR
POS E 0mm N 0mm U 0mm
FRAD 150mm
END
NEW POINTR
POS E 6000mm N 0mm U 0mm
FRAD 150mm
END
NEW POINTR
POS E 6000mm N 4000mm U 0mm
FRAD 150mm
END
NEW POINTR
POS E 0mm N 4000mm U 0mm
FRAD 150mm
END
NEW POINTR
POS E 0mm N 0mm U 0mm
FRAD 150mm
END
END
END

END
END
