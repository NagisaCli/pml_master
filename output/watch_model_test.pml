-- ============================================================
-- E3D Agent model test: simplified wristwatch
-- Units: mm
-- PREREQUISITE: in E3D Model Explorer, select an existing writable
-- ZONE as CE before running this macro. This macro does NOT create a
-- SITE or ZONE, avoiding an invalid owner hierarchy.
-- ============================================================

-- Case: 45 mm diameter × 12 mm high
NEW EQUI /WATCH_CASE_001
DESC 'Simplified wristwatch case'
NEW CYLI
DIAM 45
HEIG 12

-- Dial: 39 mm diameter × 2 mm high, placed on top of the case
NEW EQUI /WATCH_DIAL_001
DESC 'Watch dial'
POS E 0 N 0 U 12
NEW CYLI
DIAM 39
HEIG 2

-- North strap: 22 mm wide × 80 mm long × 3 mm thick
NEW EQUI /WATCH_STRAP_N_001
DESC 'North strap segment'
POS E 0 N 62.5 U 4
NEW BOX
XLEN 22
YLEN 80
ZLEN 3

-- South strap: 22 mm wide × 80 mm long × 3 mm thick
NEW EQUI /WATCH_STRAP_S_001
DESC 'South strap segment'
POS E 0 N -62.5 U 4
NEW BOX
XLEN 22
YLEN 80
ZLEN 3

-- Crown: 6 mm diameter × 8 mm high
NEW EQUI /WATCH_CROWN_001
DESC 'Watch crown'
POS E 25.5 N 0 U 4
NEW CYLI
DIAM 6
HEIG 8

-- End of macro.
