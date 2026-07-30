-- ====================================================================
-- JUNK TRAP-2
-- ====================================================================
-- Scope: One independent equipment model
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Equipment bottom centre / foundation bearing plane
-- Generated: 2026-07-30 03:18:47
-- Execution: Select a writable ZONE, then $M <this file>


-- ====================================================================
-- JUNK TRAP-2
-- ====================================================================
-- Bottom centre: E 33635.0  N 15965.0  U -300.0
-- Main dimensions: OD 1770 mm; shell 1800 mm; hopper 550 mm
-- Overall height: 2942.5 mm

NEW EQUI /JUNK_TRAP_2
POS E 0.0 N 0.0 U 0.0
NEW SUBE /JUNK_TRAP_2_SUPPORT
-- Support leg 1
NEW BOX
XLEN 180.0
YLEN 180.0
ZLEN 700.0
POS E 34254.5 N 16584.5 U 50.0

-- Support leg 1 foot plate
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 25.0
POS E 34254.5 N 16584.5 U -287.5

-- Junk-trap support leg 1 non-shrink grout pad
NEW BOX
XLEN 380.0
YLEN 380.0
ZLEN 12.0
ORI Z IS U AND X IS E 45 N
POS E 34254.5 N 16584.5 U -294.0

-- Junk-trap support leg 1 radial base gusset
NEW BOX
XLEN 165.0
YLEN 35.0
ZLEN 150.0
ORI Z IS U AND X IS E 45 N
POS E 34254.5 N 16584.5 U -225.0

-- Junk-trap support leg 1 tangential base gusset
NEW BOX
XLEN 35.0
YLEN 165.0
ZLEN 150.0
ORI Z IS U AND X IS E 45 N
POS E 34254.5 N 16584.5 U -225.0

-- Junk-trap support leg 1 anchor stud 1
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 16728.7 U -268.5

-- Junk-trap support leg 1 anchor clamp washer plate 1
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS E 45 N
POS E 34254.5 N 16728.7 U -270.0

-- Junk-trap support leg 1 anchor washer 1
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 16728.7 U -272.5

-- Junk-trap support leg 1 anchor nut 1
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 16728.7 U -261.0

-- Junk-trap support leg 1 anchor stud 2
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 34110.3 N 16584.5 U -268.5

-- Junk-trap support leg 1 anchor clamp washer plate 2
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS E 45 N
POS E 34110.3 N 16584.5 U -270.0

-- Junk-trap support leg 1 anchor washer 2
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 34110.3 N 16584.5 U -272.5

-- Junk-trap support leg 1 anchor nut 2
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 34110.3 N 16584.5 U -261.0

-- Junk-trap support leg 1 anchor stud 3
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 16440.3 U -268.5

-- Junk-trap support leg 1 anchor clamp washer plate 3
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS E 45 N
POS E 34254.5 N 16440.3 U -270.0

-- Junk-trap support leg 1 anchor washer 3
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 16440.3 U -272.5

-- Junk-trap support leg 1 anchor nut 3
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 16440.3 U -261.0

-- Junk-trap support leg 1 anchor stud 4
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 34398.7 N 16584.5 U -268.5

-- Junk-trap support leg 1 anchor clamp washer plate 4
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS E 45 N
POS E 34398.7 N 16584.5 U -270.0

-- Junk-trap support leg 1 anchor washer 4
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 34398.7 N 16584.5 U -272.5

-- Junk-trap support leg 1 anchor nut 4
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 34398.7 N 16584.5 U -261.0

-- Junk-trap support leg 1 top load-spreader plate
NEW BOX
XLEN 360.0
YLEN 360.0
ZLEN 40.0
ORI Z IS U AND X IS E 45 N
POS E 34254.5 N 16584.5 U 400.0

-- Junk-trap support leg 1 radial top gusset web
NEW BOX
XLEN 440.0
YLEN 35.0
ZLEN 320.0
ORI Z IS U AND X IS E 45 N
POS E 34254.5 N 16584.5 U 250.0

-- Junk-trap support leg 1 tangential top gusset web
NEW BOX
XLEN 35.0
YLEN 440.0
ZLEN 320.0
ORI Z IS U AND X IS E 45 N
POS E 34254.5 N 16584.5 U 250.0

-- Support leg 2
NEW BOX
XLEN 180.0
YLEN 180.0
ZLEN 700.0
POS E 33015.5 N 16584.5 U 50.0

-- Support leg 2 foot plate
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 25.0
POS E 33015.5 N 16584.5 U -287.5

-- Junk-trap support leg 2 non-shrink grout pad
NEW BOX
XLEN 380.0
YLEN 380.0
ZLEN 12.0
ORI Z IS U AND X IS N 45 W
POS E 33015.5 N 16584.5 U -294.0

-- Junk-trap support leg 2 radial base gusset
NEW BOX
XLEN 165.0
YLEN 35.0
ZLEN 150.0
ORI Z IS U AND X IS N 45 W
POS E 33015.5 N 16584.5 U -225.0

-- Junk-trap support leg 2 tangential base gusset
NEW BOX
XLEN 35.0
YLEN 165.0
ZLEN 150.0
ORI Z IS U AND X IS N 45 W
POS E 33015.5 N 16584.5 U -225.0

-- Junk-trap support leg 2 anchor stud 1
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 32871.3 N 16584.5 U -268.5

-- Junk-trap support leg 2 anchor clamp washer plate 1
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS N 45 W
POS E 32871.3 N 16584.5 U -270.0

-- Junk-trap support leg 2 anchor washer 1
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 32871.3 N 16584.5 U -272.5

-- Junk-trap support leg 2 anchor nut 1
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 32871.3 N 16584.5 U -261.0

-- Junk-trap support leg 2 anchor stud 2
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 16440.3 U -268.5

-- Junk-trap support leg 2 anchor clamp washer plate 2
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS N 45 W
POS E 33015.5 N 16440.3 U -270.0

-- Junk-trap support leg 2 anchor washer 2
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 16440.3 U -272.5

-- Junk-trap support leg 2 anchor nut 2
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 16440.3 U -261.0

-- Junk-trap support leg 2 anchor stud 3
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 33159.7 N 16584.5 U -268.5

-- Junk-trap support leg 2 anchor clamp washer plate 3
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS N 45 W
POS E 33159.7 N 16584.5 U -270.0

-- Junk-trap support leg 2 anchor washer 3
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 33159.7 N 16584.5 U -272.5

-- Junk-trap support leg 2 anchor nut 3
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 33159.7 N 16584.5 U -261.0

-- Junk-trap support leg 2 anchor stud 4
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 16728.7 U -268.5

-- Junk-trap support leg 2 anchor clamp washer plate 4
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS N 45 W
POS E 33015.5 N 16728.7 U -270.0

-- Junk-trap support leg 2 anchor washer 4
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 16728.7 U -272.5

-- Junk-trap support leg 2 anchor nut 4
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 16728.7 U -261.0

-- Junk-trap support leg 2 top load-spreader plate
NEW BOX
XLEN 360.0
YLEN 360.0
ZLEN 40.0
ORI Z IS U AND X IS N 45 W
POS E 33015.5 N 16584.5 U 400.0

-- Junk-trap support leg 2 radial top gusset web
NEW BOX
XLEN 440.0
YLEN 35.0
ZLEN 320.0
ORI Z IS U AND X IS N 45 W
POS E 33015.5 N 16584.5 U 250.0

-- Junk-trap support leg 2 tangential top gusset web
NEW BOX
XLEN 35.0
YLEN 440.0
ZLEN 320.0
ORI Z IS U AND X IS N 45 W
POS E 33015.5 N 16584.5 U 250.0

-- Support leg 3
NEW BOX
XLEN 180.0
YLEN 180.0
ZLEN 700.0
POS E 33015.5 N 15345.5 U 50.0

-- Support leg 3 foot plate
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 25.0
POS E 33015.5 N 15345.5 U -287.5

-- Junk-trap support leg 3 non-shrink grout pad
NEW BOX
XLEN 380.0
YLEN 380.0
ZLEN 12.0
ORI Z IS U AND X IS W 45 S
POS E 33015.5 N 15345.5 U -294.0

-- Junk-trap support leg 3 radial base gusset
NEW BOX
XLEN 165.0
YLEN 35.0
ZLEN 150.0
ORI Z IS U AND X IS W 45 S
POS E 33015.5 N 15345.5 U -225.0

-- Junk-trap support leg 3 tangential base gusset
NEW BOX
XLEN 35.0
YLEN 165.0
ZLEN 150.0
ORI Z IS U AND X IS W 45 S
POS E 33015.5 N 15345.5 U -225.0

-- Junk-trap support leg 3 anchor stud 1
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 15201.3 U -268.5

-- Junk-trap support leg 3 anchor clamp washer plate 1
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS W 45 S
POS E 33015.5 N 15201.3 U -270.0

-- Junk-trap support leg 3 anchor washer 1
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 15201.3 U -272.5

-- Junk-trap support leg 3 anchor nut 1
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 15201.3 U -261.0

-- Junk-trap support leg 3 anchor stud 2
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 33159.7 N 15345.5 U -268.5

-- Junk-trap support leg 3 anchor clamp washer plate 2
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS W 45 S
POS E 33159.7 N 15345.5 U -270.0

-- Junk-trap support leg 3 anchor washer 2
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 33159.7 N 15345.5 U -272.5

-- Junk-trap support leg 3 anchor nut 2
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 33159.7 N 15345.5 U -261.0

-- Junk-trap support leg 3 anchor stud 3
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 15489.7 U -268.5

-- Junk-trap support leg 3 anchor clamp washer plate 3
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS W 45 S
POS E 33015.5 N 15489.7 U -270.0

-- Junk-trap support leg 3 anchor washer 3
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 15489.7 U -272.5

-- Junk-trap support leg 3 anchor nut 3
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 33015.5 N 15489.7 U -261.0

-- Junk-trap support leg 3 anchor stud 4
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 32871.3 N 15345.5 U -268.5

-- Junk-trap support leg 3 anchor clamp washer plate 4
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS W 45 S
POS E 32871.3 N 15345.5 U -270.0

-- Junk-trap support leg 3 anchor washer 4
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 32871.3 N 15345.5 U -272.5

-- Junk-trap support leg 3 anchor nut 4
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 32871.3 N 15345.5 U -261.0

-- Junk-trap support leg 3 top load-spreader plate
NEW BOX
XLEN 360.0
YLEN 360.0
ZLEN 40.0
ORI Z IS U AND X IS W 45 S
POS E 33015.5 N 15345.5 U 400.0

-- Junk-trap support leg 3 radial top gusset web
NEW BOX
XLEN 440.0
YLEN 35.0
ZLEN 320.0
ORI Z IS U AND X IS W 45 S
POS E 33015.5 N 15345.5 U 250.0

-- Junk-trap support leg 3 tangential top gusset web
NEW BOX
XLEN 35.0
YLEN 440.0
ZLEN 320.0
ORI Z IS U AND X IS W 45 S
POS E 33015.5 N 15345.5 U 250.0

-- Support leg 4
NEW BOX
XLEN 180.0
YLEN 180.0
ZLEN 700.0
POS E 34254.5 N 15345.5 U 50.0

-- Support leg 4 foot plate
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 25.0
POS E 34254.5 N 15345.5 U -287.5

-- Junk-trap support leg 4 non-shrink grout pad
NEW BOX
XLEN 380.0
YLEN 380.0
ZLEN 12.0
ORI Z IS U AND X IS S 45 E
POS E 34254.5 N 15345.5 U -294.0

-- Junk-trap support leg 4 radial base gusset
NEW BOX
XLEN 165.0
YLEN 35.0
ZLEN 150.0
ORI Z IS U AND X IS S 45 E
POS E 34254.5 N 15345.5 U -225.0

-- Junk-trap support leg 4 tangential base gusset
NEW BOX
XLEN 35.0
YLEN 165.0
ZLEN 150.0
ORI Z IS U AND X IS S 45 E
POS E 34254.5 N 15345.5 U -225.0

-- Junk-trap support leg 4 anchor stud 1
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 34398.7 N 15345.5 U -268.5

-- Junk-trap support leg 4 anchor clamp washer plate 1
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS S 45 E
POS E 34398.7 N 15345.5 U -270.0

-- Junk-trap support leg 4 anchor washer 1
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 34398.7 N 15345.5 U -272.5

-- Junk-trap support leg 4 anchor nut 1
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 34398.7 N 15345.5 U -261.0

-- Junk-trap support leg 4 anchor stud 2
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 15489.7 U -268.5

-- Junk-trap support leg 4 anchor clamp washer plate 2
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS S 45 E
POS E 34254.5 N 15489.7 U -270.0

-- Junk-trap support leg 4 anchor washer 2
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 15489.7 U -272.5

-- Junk-trap support leg 4 anchor nut 2
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 15489.7 U -261.0

-- Junk-trap support leg 4 anchor stud 3
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 34110.3 N 15345.5 U -268.5

-- Junk-trap support leg 4 anchor clamp washer plate 3
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS S 45 E
POS E 34110.3 N 15345.5 U -270.0

-- Junk-trap support leg 4 anchor washer 3
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 34110.3 N 15345.5 U -272.5

-- Junk-trap support leg 4 anchor nut 3
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 34110.3 N 15345.5 U -261.0

-- Junk-trap support leg 4 anchor stud 4
NEW CYLI
DIAM 24.0
HEIG 63.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 15201.3 U -268.5

-- Junk-trap support leg 4 anchor clamp washer plate 4
NEW BOX
XLEN 75.0
YLEN 75.0
ZLEN 10.0
ORI Z IS U AND X IS S 45 E
POS E 34254.5 N 15201.3 U -270.0

-- Junk-trap support leg 4 anchor washer 4
NEW CYLI
DIAM 48.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 15201.3 U -272.5

-- Junk-trap support leg 4 anchor nut 4
NEW CYLI
DIAM 42.0
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 34254.5 N 15201.3 U -261.0

-- Junk-trap support leg 4 top load-spreader plate
NEW BOX
XLEN 360.0
YLEN 360.0
ZLEN 40.0
ORI Z IS U AND X IS S 45 E
POS E 34254.5 N 15345.5 U 400.0

-- Junk-trap support leg 4 radial top gusset web
NEW BOX
XLEN 440.0
YLEN 35.0
ZLEN 320.0
ORI Z IS U AND X IS S 45 E
POS E 34254.5 N 15345.5 U 250.0

-- Junk-trap support leg 4 tangential top gusset web
NEW BOX
XLEN 35.0
YLEN 440.0
ZLEN 320.0
ORI Z IS U AND X IS S 45 E
POS E 34254.5 N 15345.5 U 250.0

NEW SUBE /JUNK_TRAP_2_SHELL
-- Heavy-reject conical hopper
NEW CONE
DTOP 1770.0
DBOT 300.0
HEIG 550.0
ORI Z IS U AND Y IS N
POS E 33635.0 N 15965.0 U 125.0

-- Junk-trap pressure shell
NEW CYLI
DIAM 1770.0
HEIG 1800.0
ORI Z IS U AND Y IS N
POS E 33635.0 N 15965.0 U 1300.0

-- Dished top closure
NEW DISH
DIAM 1770.0
HEIG 442.5
RADIUS 1770.0
ORI Z IS U AND Y IS N
POS E 33635.0 N 15965.0 U 2200.0

NEW SUBE /JUNK_TRAP_2_N1
-- N1 native NOZZLE placeholder — DN300 chip-circulation inlet
NEW NOZZLE /JUNK_TRAP_2_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 34790.0 N 15965.0 U 800.0
ORI P1 IS E
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /JUNK_TRAP_2_N2
-- N2 native NOZZLE placeholder — DN300 circulation outlet
NEW NOZZLE /JUNK_TRAP_2_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 32480.0 N 15965.0 U 1200.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /JUNK_TRAP_2_N3
-- N3 native NOZZLE placeholder — DN200 flush-water connection
NEW NOZZLE /JUNK_TRAP_2_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 33635.0 N 17120.0 U 1650.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /JUNK_TRAP_2_N4
-- N4 native NOZZLE placeholder — DN200 equalizing / vent connection
NEW NOZZLE /JUNK_TRAP_2_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 33635.0 N 14810.0 U 1950.0
ORI P1 IS S
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /JUNK_TRAP_2_N5
-- N5 native NOZZLE placeholder — DN300 bottom heavy-reject discharge
NEW NOZZLE /JUNK_TRAP_2_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 33635.0 N 15965.0 U -300.0
ORI P1 IS D
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /JUNK_TRAP_2_DETAIL
-- JUNK TRAP-2 east lifting lug plate
NEW BOX
XLEN 140.0
YLEN 260.0
ZLEN 300.0
POS E 34590.0 N 15965.0 U 1820.0

-- JUNK TRAP-2 east lifting-lug pin envelope
NEW CYLI
DIAM 70.0
HEIG 180.0
ORI Z IS N AND Y IS U
POS E 34590.0 N 15965.0 U 1820.0

-- JUNK TRAP-2 west lifting lug plate
NEW BOX
XLEN 140.0
YLEN 260.0
ZLEN 300.0
POS E 32680.0 N 15965.0 U 1820.0

-- JUNK TRAP-2 west lifting-lug pin envelope
NEW CYLI
DIAM 70.0
HEIG 180.0
ORI Z IS N AND Y IS U
POS E 32680.0 N 15965.0 U 1820.0

-- JUNK TRAP-2 north lifting lug plate
NEW BOX
XLEN 260.0
YLEN 140.0
ZLEN 300.0
POS E 33635.0 N 16920.0 U 1820.0

-- JUNK TRAP-2 north lifting-lug pin envelope
NEW CYLI
DIAM 70.0
HEIG 180.0
ORI Z IS E AND Y IS U
POS E 33635.0 N 16920.0 U 1820.0

-- JUNK TRAP-2 south lifting lug plate
NEW BOX
XLEN 260.0
YLEN 140.0
ZLEN 300.0
POS E 33635.0 N 15010.0 U 1820.0

-- JUNK TRAP-2 south lifting-lug pin envelope
NEW CYLI
DIAM 70.0
HEIG 180.0
ORI Z IS E AND Y IS U
POS E 33635.0 N 15010.0 U 1820.0

-- JUNK TRAP-2 engraved equipment nameplate
NEW BOX
XLEN 500.0
YLEN 24.0
ZLEN 320.0
POS E 33635.0 N 15068.0 U 1600.0

-- JUNK TRAP-2 nameplate screw 1
NEW CYLI
DIAM 18.0
HEIG 18.0
ORI Z IS S AND Y IS U
POS E 33425.0 N 15068.0 U 1475.0

-- JUNK TRAP-2 nameplate screw 2
NEW CYLI
DIAM 18.0
HEIG 18.0
ORI Z IS S AND Y IS U
POS E 33845.0 N 15068.0 U 1475.0

-- JUNK TRAP-2 nameplate screw 3
NEW CYLI
DIAM 18.0
HEIG 18.0
ORI Z IS S AND Y IS U
POS E 33425.0 N 15068.0 U 1725.0

-- JUNK TRAP-2 nameplate screw 4
NEW CYLI
DIAM 18.0
HEIG 18.0
ORI Z IS S AND Y IS U
POS E 33845.0 N 15068.0 U 1725.0

-- JUNK TRAP-2 grounding lug
NEW BOX
XLEN 160.0
YLEN 80.0
ZLEN 120.0
POS E 34600.0 N 15965.0 U 520.0

-- JUNK TRAP-2 grounding-lug bolt
NEW CYLI
DIAM 24.0
HEIG 100.0
ORI Z IS N AND Y IS U
POS E 34600.0 N 15965.0 U 520.0


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 5 of 5 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 114 primitives.
