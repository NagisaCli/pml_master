-- =================================================================
-- E3D Agent detailed model test: 41 mm diver-style wristwatch
-- Units: mm. Select an existing writable ZONE as CE before running.
-- No SITE or ZONE is created by this macro.
-- =================================================================

-- Case stack: Ø41 × 11.3 overall (case, back, bezel, dial, crystal)
NEW EQUI /WATCH_DV_CASE_001
DESC '41 mm stainless-steel middle case'
NEW CYLI
DIAM 41
HEIG 8

NEW EQUI /WATCH_DV_BACK_001
DESC 'Screw case back'
POS E 0 N 0 U -1.5
NEW CYLI
DIAM 38
HEIG 1.5

NEW EQUI /WATCH_DV_BEZEL_001
DESC 'Rotating diver bezel'
POS E 0 N 0 U 8
NEW CYLI
DIAM 41.8
HEIG 2.0

NEW EQUI /WATCH_DV_DIAL_001
DESC 'Black dial'
POS E 0 N 0 U 10
NEW CYLI
DIAM 35.5
HEIG 0.5

NEW EQUI /WATCH_DV_CRYSTAL_001
DESC 'Sapphire crystal'
POS E 0 N 0 U 10.5
NEW CYLI
DIAM 35.0
HEIG 0.8

-- Crown and two crown guards, on the three-o-clock side
NEW EQUI /WATCH_DV_CROWN_001
DESC 'Screw-down crown'
POS E 23.5 N 0 U 4
NEW CYLI
DIAM 6.5
HEIG 3.5

NEW EQUI /WATCH_DV_CROWN_GUARD_N_001
DESC 'Upper crown guard'
POS E 20.5 N 5 U 3
NEW BOX
XLEN 5
YLEN 4
ZLEN 5

NEW EQUI /WATCH_DV_CROWN_GUARD_S_001
DESC 'Lower crown guard'
POS E 20.5 N -5 U 3
NEW BOX
XLEN 5
YLEN 4
ZLEN 5

-- Four lugs: 48.8 mm lug-to-lug and 20 mm strap width
NEW EQUI /WATCH_DV_LUG_NE_001
DESC 'North-east lug'
POS E 7 N 22.5 U 2
NEW BOX
XLEN 6
YLEN 8
ZLEN 5

NEW EQUI /WATCH_DV_LUG_NW_001
DESC 'North-west lug'
POS E -7 N 22.5 U 2
NEW BOX
XLEN 6
YLEN 8
ZLEN 5

NEW EQUI /WATCH_DV_LUG_SE_001
DESC 'South-east lug'
POS E 7 N -22.5 U 2
NEW BOX
XLEN 6
YLEN 8
ZLEN 5

NEW EQUI /WATCH_DV_LUG_SW_001
DESC 'South-west lug'
POS E -7 N -22.5 U 2
NEW BOX
XLEN 6
YLEN 8
ZLEN 5

-- Three-link bracelet, six articulated visual segments
NEW EQUI /WATCH_DV_BRACELET_N1_001
DESC 'North bracelet link 1'
POS E 0 N 34 U 2
NEW BOX
XLEN 20
YLEN 18
ZLEN 3

NEW EQUI /WATCH_DV_BRACELET_N2_001
DESC 'North bracelet link 2'
POS E 0 N 53 U 2
NEW BOX
XLEN 20
YLEN 18
ZLEN 3

NEW EQUI /WATCH_DV_BRACELET_N3_001
DESC 'North bracelet link 3'
POS E 0 N 72 U 2
NEW BOX
XLEN 20
YLEN 18
ZLEN 3

NEW EQUI /WATCH_DV_BRACELET_S1_001
DESC 'South bracelet link 1'
POS E 0 N -34 U 2
NEW BOX
XLEN 20
YLEN 18
ZLEN 3

NEW EQUI /WATCH_DV_BRACELET_S2_001
DESC 'South bracelet link 2'
POS E 0 N -53 U 2
NEW BOX
XLEN 20
YLEN 18
ZLEN 3

NEW EQUI /WATCH_DV_BRACELET_S3_001
DESC 'South bracelet link 3'
POS E 0 N -72 U 2
NEW BOX
XLEN 20
YLEN 18
ZLEN 3

-- Dial markers: rectangular cardinal indices and eight round indices
NEW EQUI /WATCH_DV_INDEX_12_001
DESC 'Twelve o-clock index'
POS E 0 N 14 U 11.3
NEW BOX
XLEN 4
YLEN 2
ZLEN 0.6

NEW EQUI /WATCH_DV_INDEX_3_001
DESC 'Three o-clock index'
POS E 14 N 0 U 11.3
NEW BOX
XLEN 2
YLEN 4
ZLEN 0.6

NEW EQUI /WATCH_DV_INDEX_6_001
DESC 'Six o-clock index'
POS E 0 N -14 U 11.3
NEW BOX
XLEN 4
YLEN 2
ZLEN 0.6

NEW EQUI /WATCH_DV_INDEX_9_001
DESC 'Nine o-clock index'
POS E -14 N 0 U 11.3
NEW BOX
XLEN 2
YLEN 4
ZLEN 0.6

NEW EQUI /WATCH_DV_INDEX_1_001
DESC 'One o-clock luminous index'
POS E 7 N 12 U 11.3
NEW CYLI
DIAM 2
HEIG 0.6

NEW EQUI /WATCH_DV_INDEX_2_001
DESC 'Two o-clock luminous index'
POS E 12 N 7 U 11.3
NEW CYLI
DIAM 2
HEIG 0.6

NEW EQUI /WATCH_DV_INDEX_4_001
DESC 'Four o-clock luminous index'
POS E 12 N -7 U 11.3
NEW CYLI
DIAM 2
HEIG 0.6

NEW EQUI /WATCH_DV_INDEX_5_001
DESC 'Five o-clock luminous index'
POS E 7 N -12 U 11.3
NEW CYLI
DIAM 2
HEIG 0.6

NEW EQUI /WATCH_DV_INDEX_7_001
DESC 'Seven o-clock luminous index'
POS E -7 N -12 U 11.3
NEW CYLI
DIAM 2
HEIG 0.6

NEW EQUI /WATCH_DV_INDEX_8_001
DESC 'Eight o-clock luminous index'
POS E -12 N -7 U 11.3
NEW CYLI
DIAM 2
HEIG 0.6

NEW EQUI /WATCH_DV_INDEX_10_001
DESC 'Ten o-clock luminous index'
POS E -12 N 7 U 11.3
NEW CYLI
DIAM 2
HEIG 0.6

NEW EQUI /WATCH_DV_INDEX_11_001
DESC 'Eleven o-clock luminous index'
POS E -7 N 12 U 11.3
NEW CYLI
DIAM 2
HEIG 0.6

-- Hands, shown as raised rectangular primitives at ten past ten
NEW EQUI /WATCH_DV_HAND_HOUR_001
DESC 'Hour hand'
POS E 0 N 4 U 11.9
NEW BOX
XLEN 3.0
YLEN 10
ZLEN 0.5

NEW EQUI /WATCH_DV_HAND_MINUTE_001
DESC 'Minute hand'
POS E 5.5 N 0 U 12.0
NEW BOX
XLEN 15
YLEN 2.0
ZLEN 0.4

NEW EQUI /WATCH_DV_HAND_SECOND_001
DESC 'Second hand'
POS E 0 N -7 U 12.1
NEW BOX
XLEN 0.8
YLEN 18
ZLEN 0.25

-- Date aperture at four-thirty, modelled as a recessed visual block
NEW EQUI /WATCH_DV_DATE_001
DESC 'Date aperture at four-thirty'
POS E 9 N -9 U 11.3
NEW BOX
XLEN 5
YLEN 3
ZLEN 0.3

-- End of detailed watch macro.
