-- ====================================================================
-- MAIN CONDENSATE TANK
-- ====================================================================
-- Scope: One independent equipment model
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Equipment bottom centre / foundation bearing plane
-- Generated: 2026-07-30 03:18:48
-- Execution: Select a writable ZONE, then $M <this file>


-- ====================================================================
-- MAIN CONDENSATE TANK
-- ====================================================================
-- Bottom centre: E 28497.0  N 27796.0  U -300.0
-- Main dimensions: Horizontal envelope 3400 × 2017 mm; straight barrel 2391.5 mm
-- Overall height: 2717.0 mm
-- Listed capacity: 8 m3

NEW EQUI /MAIN_CONDENSATE_TANK
POS E 0.0 N 0.0 U 0.0
NEW SUBE /MAIN_CONDENSATE_TANK_SHELL
-- Horizontal condensate receiver shell
NEW CYLI
DIAM 2017.0
HEIG 2391.5
ORI Z IS N AND Y IS U
POS E 28497.0 N 27796.0 U 1208.5

-- North 2:1 elliptical head envelope
NEW DISH
DIAM 2017.0
HEIG 504.2
RADIUS 2017.0
ORI Z IS N AND Y IS U
POS E 28497.0 N 28991.8 U 1208.5

-- South 2:1 elliptical head envelope
NEW DISH
DIAM 2017.0
HEIG 504.2
RADIUS 2017.0
ORI Z IS S AND Y IS U
POS E 28497.0 N 26600.2 U 1208.5

NEW SUBE /MAIN_CONDENSATE_TANK_SUPPORT
-- Saddle support 1
NEW BOX
XLEN 1700.0
YLEN 400.0
ZLEN 500.0
POS E 28497.0 N 27146.0 U -50.0

-- Saddle support 1 vessel wear/load-spreader plate
NEW BOX
XLEN 1800.0
YLEN 500.0
ZLEN 40.0
POS E 28497.0 N 27146.0 U 200.0

-- Saddle support 1 sole plate and grout interface
NEW BOX
XLEN 1800.0
YLEN 500.0
ZLEN 20.0
POS E 28497.0 N 27146.0 U -290.0

-- Condensate saddle 1 anchor stud 1
NEW CYLI
DIAM 24.0
HEIG 70.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 27296.0 U -265.0

-- Condensate saddle 1 anchor washer 1
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 27296.0 U -277.5

-- Condensate saddle 1 anchor nut 1
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 27296.0 U -266.0

-- Condensate saddle 1 anchor stud 2
NEW CYLI
DIAM 24.0
HEIG 70.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 27296.0 U -265.0

-- Condensate saddle 1 anchor washer 2
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 27296.0 U -277.5

-- Condensate saddle 1 anchor nut 2
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 27296.0 U -266.0

-- Condensate saddle 1 anchor stud 3
NEW CYLI
DIAM 24.0
HEIG 70.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 26996.0 U -265.0

-- Condensate saddle 1 anchor washer 3
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 26996.0 U -277.5

-- Condensate saddle 1 anchor nut 3
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 26996.0 U -266.0

-- Condensate saddle 1 anchor stud 4
NEW CYLI
DIAM 24.0
HEIG 70.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 26996.0 U -265.0

-- Condensate saddle 1 anchor washer 4
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 26996.0 U -277.5

-- Condensate saddle 1 anchor nut 4
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 26996.0 U -266.0

-- Saddle support 2
NEW BOX
XLEN 1700.0
YLEN 400.0
ZLEN 500.0
POS E 28497.0 N 28446.0 U -50.0

-- Saddle support 2 vessel wear/load-spreader plate
NEW BOX
XLEN 1800.0
YLEN 500.0
ZLEN 40.0
POS E 28497.0 N 28446.0 U 200.0

-- Saddle support 2 sole plate and grout interface
NEW BOX
XLEN 1800.0
YLEN 500.0
ZLEN 20.0
POS E 28497.0 N 28446.0 U -290.0

-- Condensate saddle 2 anchor stud 1
NEW CYLI
DIAM 24.0
HEIG 70.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 28596.0 U -265.0

-- Condensate saddle 2 anchor washer 1
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 28596.0 U -277.5

-- Condensate saddle 2 anchor nut 1
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 28596.0 U -266.0

-- Condensate saddle 2 anchor stud 2
NEW CYLI
DIAM 24.0
HEIG 70.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 28596.0 U -265.0

-- Condensate saddle 2 anchor washer 2
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 28596.0 U -277.5

-- Condensate saddle 2 anchor nut 2
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 28596.0 U -266.0

-- Condensate saddle 2 anchor stud 3
NEW CYLI
DIAM 24.0
HEIG 70.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 28296.0 U -265.0

-- Condensate saddle 2 anchor washer 3
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 28296.0 U -277.5

-- Condensate saddle 2 anchor nut 3
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 27797.0 N 28296.0 U -266.0

-- Condensate saddle 2 anchor stud 4
NEW CYLI
DIAM 24.0
HEIG 70.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 28296.0 U -265.0

-- Condensate saddle 2 anchor washer 4
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 28296.0 U -277.5

-- Condensate saddle 2 anchor nut 4
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 29197.0 N 28296.0 U -266.0

NEW SUBE /MAIN_CONDENSATE_TANK_N1
-- N1 native NOZZLE placeholder — DN200 condensate inlet
NEW NOZZLE /MAIN_CONDENSATE_TANK_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 28497.0 N 29766.0 U 1208.5
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /MAIN_CONDENSATE_TANK_N2
-- N2 native NOZZLE placeholder — DN200 condensate outlet
NEW NOZZLE /MAIN_CONDENSATE_TANK_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 28497.0 N 25826.0 U 1208.5
ORI P1 IS S
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /MAIN_CONDENSATE_TANK_N3
-- N3 native NOZZLE placeholder — DN150 level / overflow connection
NEW NOZZLE /MAIN_CONDENSATE_TANK_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 29725.5 N 27796.0 U 1208.5
ORI P1 IS E
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /MAIN_CONDENSATE_TANK_M1
-- M1 native NOZZLE placeholder — DN500 inspection manway
NEW NOZZLE /MAIN_CONDENSATE_TANK_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB011
POS E 27118.5 N 27796.0 U 1208.5
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /MAIN_CONDENSATE_TANK_N4
-- N4 native NOZZLE placeholder — DN150 high-point vent
NEW NOZZLE /MAIN_CONDENSATE_TANK_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 28497.0 N 27796.0 U 2417.0
ORI P1 IS U
HEIG 280.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /MAIN_CONDENSATE_TANK_DETAIL
-- Condensate receiver lifting pad 1
NEW BOX
XLEN 260.0
YLEN 140.0
ZLEN 120.0
POS E 28497.0 N 27146.0 U 2277.0

-- Condensate receiver lifting-pin envelope 1
NEW CYLI
DIAM 60.0
HEIG 180.0
ORI Z IS E AND Y IS U
POS E 28497.0 N 27146.0 U 2277.0

-- Condensate receiver lifting pad 2
NEW BOX
XLEN 260.0
YLEN 140.0
ZLEN 120.0
POS E 28497.0 N 28446.0 U 2277.0

-- Condensate receiver lifting-pin envelope 2
NEW CYLI
DIAM 60.0
HEIG 180.0
ORI Z IS E AND Y IS U
POS E 28497.0 N 28446.0 U 2277.0

-- Condensate receiver nameplate
NEW BOX
XLEN 24.0
YLEN 500.0
ZLEN 300.0
POS E 29517.5 N 27796.0 U 1208.5

-- Condensate receiver nameplate screw 1
NEW CYLI
DIAM 18.0
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 29517.5 N 27586.0 U 1088.5

-- Condensate receiver nameplate screw 2
NEW CYLI
DIAM 18.0
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 29517.5 N 28006.0 U 1088.5

-- Condensate receiver nameplate screw 3
NEW CYLI
DIAM 18.0
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 29517.5 N 27586.0 U 1328.5

-- Condensate receiver nameplate screw 4
NEW CYLI
DIAM 18.0
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 29517.5 N 28006.0 U 1328.5

-- Condensate receiver grounding lug
NEW BOX
XLEN 120.0
YLEN 160.0
ZLEN 80.0
POS E 29565.5 N 27796.0 U 320.0

-- Condensate receiver grounding-lug bolt
NEW CYLI
DIAM 24.0
HEIG 100.0
ORI Z IS N AND Y IS U
POS E 29565.5 N 27796.0 U 320.0


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 5 of 5 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 44 primitives.
