-- ====================================================================
-- 204-SE-010 - TERTIARY SCREEN (Tertiary Pressure Screen) - HORIZONTAL LAYOUT
-- ====================================================================
-- Project: CTE-2026-JK (Screening & Washing Area 204)
-- Equipment Tag: 204-SE-010
-- Equipment Name: TERTIARY SCREEN
-- Orientation: Horizontal machine (Horizontal Layout), axis along North (N)
-- Source Drawing: C:\Users\A\Desktop\Fight\Layout\CTE-2026-JK-00-GEN-Rev2(newest).dwg
-- Units: mm
-- Datum: Equipment origin (E 0, N 0, U 0) at South base ring foundation contact
-- Shaft / Cylinder Centerline: E 0.0, U 240.0
-- CAD Plant Coordinates: E 1241403.3, N -240603.4, U 0.0
-- Execution: In AVEVA E3D Command Window, navigate to active ZONE and type: $M <filename>.pml

NEW EQUI /204_SE_010
POS E 0.0 N 0.0 U 0.0
-- --------------------------------------------------------------------
-- SUBEQUIPMENT 1: SUPPORT SKID & BASE CRADLE
-- --------------------------------------------------------------------
NEW SUBE /204_SE_010_SUPPORT
-- Project Data: South end cover / base ring flange (DIAM 479.5 x 37.7 mm, N 0..37.7)
NEW CYLI
DIAM 479.5
HEIG 37.7
ORI Z IS N AND Y IS U
POS E 0.0 N 18.9 U 240.0

-- Reference Value: Base skid longitudinal channel rail (West side)
NEW BOX
XLEN 80.0
YLEN 1497.8
ZLEN 60.0
POS E -350.0 N 1099.0 U 30.0

-- Reference Value: Base skid longitudinal channel rail (East side)
NEW BOX
XLEN 80.0
YLEN 1497.8
ZLEN 60.0
POS E 350.0 N 1099.0 U 30.0

-- Reference Value: Base skid transverse cross member (South)
NEW BOX
XLEN 700.0
YLEN 100.0
ZLEN 60.0
POS E 0.0 N 400.0 U 30.0

-- Reference Value: Base skid transverse cross member (Middle)
NEW BOX
XLEN 700.0
YLEN 100.0
ZLEN 60.0
POS E 0.0 N 1000.0 U 30.0

-- Reference Value: Base skid transverse cross member (North)
NEW BOX
XLEN 700.0
YLEN 100.0
ZLEN 60.0
POS E 0.0 N 1750.0 U 30.0

-- Reference Value: Main body support cradle saddle
NEW BOX
XLEN 360.0
YLEN 80.0
ZLEN 147.5
POS E 0.0 N 400.0 U 133.8

-- Reference Value: Drive column support pedestal
NEW BOX
XLEN 160.0
YLEN 80.0
ZLEN 188.4
POS E 0.0 N 1000.0 U 154.2

-- --------------------------------------------------------------------
-- SUBEQUIPMENT 2: SCREEN BODY & HEAD
-- --------------------------------------------------------------------
NEW SUBE /204_SE_010_BODY
-- Project Data: Main cylindrical screen basket body (DIAM 414.9 x 511.8 mm, N 37.7..549.5)
NEW CYLI
DIAM 414.9
HEIG 511.8
ORI Z IS N AND Y IS U
POS E 0.0 N 293.6 U 240.0

-- Project Data: Screen body middle split flange (DIAM 450.0 x 21.6 mm, N 549.5..571.1)
NEW CYLI
DIAM 450.0
HEIG 21.6
ORI Z IS N AND Y IS U
POS E 0.0 N 560.3 U 240.0

-- Project Data: Conical head reducer (DBOT 296.3 -> DTOP 253.2 x 97.0 mm, N 571.1..668.1)
NEW CONE
DTOP 253.2
DBOT 296.3
HEIG 97.0
ORI Z IS N AND Y IS U
POS E 0.0 N 619.6 U 240.0

-- --------------------------------------------------------------------
-- SUBEQUIPMENT 3: DRIVE COLUMN & INSPECTION PORT
-- --------------------------------------------------------------------
NEW SUBE /204_SE_010_DRIVE
-- Project Data: Drive column shaft housing (DIAM 183.2 x 635.8 mm, N 668.1..1303.8)
NEW CYLI
DIAM 183.2
HEIG 635.8
ORI Z IS N AND Y IS U
POS E 0.0 N 986.0 U 240.0

-- Project Data: Inspection port collar facing Up (DIAM 150.9 x 25.0 mm at N 1099.1)
NEW CYLI
DIAM 150.9
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 0.0 N 1099.1 U 344.1

-- Reference Value: Inspection window protective grille disc
NEW CYLI
DIAM 135.0
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 0.0 N 1099.1 U 354.1

-- Project Data: Motor stool transition cone (DBOT 183.2 -> DTOP 301.7 x 48.5 mm, N 1303.8..1352.3)
NEW CONE
DTOP 301.7
DBOT 183.2
HEIG 48.5
ORI Z IS N AND Y IS U
POS E 0.0 N 1328.0 U 240.0

-- --------------------------------------------------------------------
-- SUBEQUIPMENT 4: DRIVE MOTOR
-- --------------------------------------------------------------------
NEW SUBE /204_SE_010_MOTOR
-- Reference Value: Motor mounting D-flange (DIAM 350.0 x 22.7 mm, N 1352.3..1375.0)
NEW CYLI
DIAM 350.0
HEIG 22.7
ORI Z IS N AND Y IS U
POS E 0.0 N 1363.6 U 240.0

-- Project Data: Motor stator frame cylinder (DIAM 301.7 x 327.5 mm, N 1375.0..1702.5)
NEW CYLI
DIAM 301.7
HEIG 327.5
ORI Z IS N AND Y IS U
POS E 0.0 N 1538.8 U 240.0

-- Reference Value: Motor terminal box on East side
NEW BOX
XLEN 70.0
YLEN 140.0
ZLEN 130.0
POS E 185.0 N 1540.0 U 240.0

-- Project Data: Motor upper bearing end shield (DIAM 301.7 x 37.7 mm, N 1702.5..1740.2)
NEW CYLI
DIAM 301.7
HEIG 37.7
ORI Z IS N AND Y IS U
POS E 0.0 N 1721.3 U 240.0

-- Project Data: Motor fan cowl chamfered cover (DBOT 301.7 -> DTOP 220.9 x 43.1 mm, N 1740.2..1783.3)
NEW CONE
DTOP 220.9
DBOT 301.7
HEIG 43.1
ORI Z IS N AND Y IS U
POS E 0.0 N 1761.8 U 240.0

-- Project Data: Motor fan cover end disc (DIAM 220.9 x 4.0 mm, N 1783.3..1787.3)
NEW CYLI
DIAM 220.9
HEIG 4.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1785.3 U 240.0

-- --------------------------------------------------------------------
-- NOZZLES (One SUBE per nozzle, CATR first inline, flange-face POS)
-- --------------------------------------------------------------------
NEW SUBE /204_SE_010_N1
-- Project Data: N1 - Tangential Feed Inlet (DN100 / 4in 150lb, East, N 444.5)
NEW NOZZLE /204_SE_010_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 401.4 N 444.5 U 240.0
ORI P1 IS E
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_SE_010_N2
-- Project Data: N2 - Accept Outlet (DN100 / 4in 150lb, East, N 272.1)
NEW NOZZLE /204_SE_010_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 401.4 N 272.1 U 240.0
ORI P1 IS E
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_SE_010_N3
-- Project Data: N3 - Reject Outlet (DN80 / 3in 150lb, East, N 102.4)
NEW NOZZLE /204_SE_010_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 401.4 N 102.4 U 240.0
ORI P1 IS E
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_SE_010_N4
-- Project Data: N4 - Dilution / Flush Water Inlet (DN80 / 3in 150lb, West, N 471.4)
NEW NOZZLE /204_SE_010_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E -282.9 N 471.4 U 240.0
ORI P1 IS W
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 4 of 4 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 21 primitives.
