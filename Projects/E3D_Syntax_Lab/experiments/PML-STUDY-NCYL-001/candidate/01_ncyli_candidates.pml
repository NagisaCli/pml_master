$S-  -- Synonym translation OFF
-- ----------------------------------------------------------------
-- NCYLI candidate test - negative cylinder hole forms
-- Date : 05 Aug 2026
-- Load with the same INPUT data-listing path as JK_Pump_Build r3.
-- Four vertical plates (BOX 20 x 200 x 300, centre U 150) at E 0 /
-- 4000 / 8000 / 12000. Each carries one NCYLINDER with NAPPFLAG 2.
--
-- Expected observations (plate N face is the big 200 x 300 face):
--   C1 plate at E 0     : NCYLINDER POS E 0 N 0 U 250, ORI Z is E,
--                         DIAM 60, HEIG 400 (r3 form, world POS/ORI)
--   C2 plate at E 4000  : NCYLINDER no POS, no ORI (inherits owner),
--                         DIAM 60, HEIG 400
--   C3 plate at E 8000  : NCYLINDER POS E 0 N 0 U 0, ORI Z is E,
--                         DIAM 60, HEIG 400 (zero/local POS probe)
--   C4 plate at E 12000 : standalone NCYLINDER at SUBE level (not a
--                         child of the BOX), world POS/ORI
--
-- A correct horizontal hole (axis E) shows a clear 60 mm circle on the
-- plate N face. A correct vertical hole (axis U) shows a 60 mm circle
-- on the plate E face (side).
-- ----------------------------------------------------------------

ONERROR GOLABEL /ERROR3

INPUT BEGIN
NEW ZONE /CODEX_NCYL_TEST
DUNION 2

NEW EQUIPMENT /CODEX_NCYL_TEST
FUNC '025024'
BUIL false
DSCO unset
PTSP unset
INSC unset

NEW SUBEQUIPMENT /CODEX_NCYL_TEST_C1
FUNC '025024'
BUIL false
DSCO unset
PTSP unset
INSC unset

NEW BOX
POS E 0mm N 0mm U 150mm
XLEN 20mm
YLEN 200mm
ZLEN 300mm

NEW NCYLINDER
POS E 0mm N 0mm U 250mm
ORI Y is U and Z is E
DIAM 60mm
HEIG 400mm
NAPPFLAG 2
END
END
END
NEW SUBEQUIPMENT /CODEX_NCYL_TEST_C2
FUNC '025024'
BUIL false
DSCO unset
PTSP unset
INSC unset

NEW BOX
POS E 4000mm N 0mm U 150mm
XLEN 20mm
YLEN 200mm
ZLEN 300mm

NEW NCYLINDER
DIAM 60mm
HEIG 400mm
NAPPFLAG 2
END
END
END
NEW SUBEQUIPMENT /CODEX_NCYL_TEST_C3
FUNC '025024'
BUIL false
DSCO unset
PTSP unset
INSC unset

NEW BOX
POS E 8000mm N 0mm U 150mm
XLEN 20mm
YLEN 200mm
ZLEN 300mm

NEW NCYLINDER
POS E 0mm N 0mm U 0mm
ORI Y is U and Z is E
DIAM 60mm
HEIG 400mm
NAPPFLAG 2
END
END
END
NEW SUBEQUIPMENT /CODEX_NCYL_TEST_C4
FUNC '025024'
BUIL false
DSCO unset
PTSP unset
INSC unset

NEW BOX
POS E 12000mm N 0mm U 150mm
XLEN 20mm
YLEN 200mm
ZLEN 300mm
END
NEW NCYLINDER
POS E 12000mm N 0mm U 250mm
ORI Y is U and Z is E
DIAM 60mm
HEIG 400mm
NAPPFLAG 2
END
END
END
END
INPUT END  ZONE /CODEX_NCYL_TEST
INPUT FINISH
-- Switch synonyms back on if an error occurs.
LABEL /ERROR3
handle ANY
$S+
RETURN ERROR
endhandle

-- End candidate test
$S+  -- Synonym translation ON
-- ----------------------------------------------------------------
