-- Macro: Candidate 04 - Sloped Stair / Ramp Handrail with Landings
-- Study: PML-STUDY-HANDRA-001 (AVEVA E3D Design)
-- Hierarchy: STRU -> FRMWORK -> HANDRA
-- ----------------------------------------------------------------

NEW STRU /CODEX_HR_SLOPED_04_STRU
NEW FRMWORK /CODEX_HR_SLOPED_04_FRMWORK

NEW HANDRA /CODEX_HANDRA_SLOPED_04
POS E 0mm N 0mm U 0mm
RAILHE 1250mm 750mm
POSTSP 1000mm
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
POS E 1500mm N 0mm U 0mm
FRAD 150mm
END
NEW POINTR
POS E 4500mm N 0mm U 1500mm
FRAD 150mm
END
NEW POINTR
POS E 6000mm N 0mm U 1500mm
FRAD 150mm
END
END
END

END
END
