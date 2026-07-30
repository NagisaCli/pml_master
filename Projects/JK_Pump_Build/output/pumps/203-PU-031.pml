-- ====================================================================
-- 203-PU-031 - OXYGEN REACTOR TOP SPOOLING BOOSTER PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 203-PU-031
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis S from driver to casing; suction S; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /203_PU_031
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_031_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 631.0
YLEN 1353.0
ZLEN 50.0
POS E 15108.0 N 175.0 U 25.0

NEW SUBE /203_PU_031_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 14.0
HEIG 18.9
ORI Z IS U AND Y IS N
POS E 14842.5 N 777.1 U 52.3

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 30.1
HEIG 3.1
ORI Z IS U AND Y IS N
POS E 14842.5 N 777.1 U 51.5

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.7
ORI Z IS U AND Y IS N
POS E 14842.5 N 777.1 U 57.4

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 14.0
HEIG 18.9
ORI Z IS U AND Y IS N
POS E 15373.5 N 777.1 U 52.3

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 30.1
HEIG 3.1
ORI Z IS U AND Y IS N
POS E 15373.5 N 777.1 U 51.5

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.7
ORI Z IS U AND Y IS N
POS E 15373.5 N 777.1 U 57.4

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 14.0
HEIG 18.9
ORI Z IS U AND Y IS N
POS E 14842.5 N -427.1 U 52.3

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 30.1
HEIG 3.1
ORI Z IS U AND Y IS N
POS E 14842.5 N -427.1 U 51.5

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.7
ORI Z IS U AND Y IS N
POS E 14842.5 N -427.1 U 57.4

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 14.0
HEIG 18.9
ORI Z IS U AND Y IS N
POS E 15373.5 N -427.1 U 52.3

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 30.1
HEIG 3.1
ORI Z IS U AND Y IS N
POS E 15373.5 N -427.1 U 51.5

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.7
ORI Z IS U AND Y IS N
POS E 15373.5 N -427.1 U 57.4

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 14.0
HEIG 18.9
ORI Z IS U AND Y IS N
POS E 14842.5 N 175.0 U 52.3

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 30.1
HEIG 3.1
ORI Z IS U AND Y IS N
POS E 14842.5 N 175.0 U 51.5

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.7
ORI Z IS U AND Y IS N
POS E 14842.5 N 175.0 U 57.4

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 14.0
HEIG 18.9
ORI Z IS U AND Y IS N
POS E 15373.5 N 175.0 U 52.3

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 30.1
HEIG 3.1
ORI Z IS U AND Y IS N
POS E 15373.5 N 175.0 U 51.5

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.7
ORI Z IS U AND Y IS N
POS E 15373.5 N 175.0 U 57.4

NEW SUBE /203_PU_031_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 55.0
YLEN 1109.5
ZLEN 48.0
POS E 14956.6 N 202.1 U 74.0

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 55.0
YLEN 1109.5
ZLEN 48.0
POS E 15259.4 N 202.1 U 74.0

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 454.3
YLEN 39.6
ZLEN 32.6
POS E 15108.0 N 635.0 U 66.3

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 454.3
YLEN 39.6
ZLEN 32.6
POS E 15108.0 N 175.0 U 66.3

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 454.3
YLEN 39.6
ZLEN 32.6
POS E 15108.0 N -285.0 U 66.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 82.0
YLEN 101.5
ZLEN 73.9
POS E 14994.4 N -177.2 U 86.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 82.0
YLEN 101.5
ZLEN 73.9
POS E 15221.6 N -177.2 U 86.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 82.0
YLEN 101.5
ZLEN 73.9
POS E 14994.4 N -304.2 U 86.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 82.0
YLEN 101.5
ZLEN 73.9
POS E 15221.6 N -304.2 U 86.9

NEW SUBE /203_PU_031_CASING
-- Reference Value: Booster/high-head volute back-pull-out rear plate
NEW CYLI
DIAM 202.4
HEIG 39.8
ORI Z IS S AND Y IS U
POS E 15108.0 N -139.9 U 238.9

-- Reference Value: Booster/high-head volute radially split casing envelope
NEW CYLI
DIAM 230.0
HEIG 144.4
ORI Z IS S AND Y IS U
POS E 15108.0 N -232.0 U 238.9

-- Reference Value: casing split flange
NEW CYLI
DIAM 244.9
HEIG 10.0
ORI Z IS S AND Y IS U
POS E 15108.0 N -299.2 U 238.9

-- Reference Value: Booster/high-head volute tapered impeller-eye cover
NEW CONE
DTOP 105.8
DBOT 225.4
HEIG 64.7
ORI Z IS S AND Y IS U
POS E 15108.0 N -336.5 U 238.9

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 115.0
HEIG 10.4
ORI Z IS S AND Y IS U
POS E 15108.0 N -363.7 U 238.9

-- Reference Value: Booster/high-head volute circumferentially distributed axial casing rib 1/3
NEW CYLI
DIAM 11.0
HEIG 98.2
ORI Z IS S AND Y IS U
POS E 15108.0 N -232.0 U 355.9

-- Reference Value: Booster/high-head volute circumferentially distributed axial casing rib 2/3
NEW CYLI
DIAM 11.0
HEIG 98.2
ORI Z IS S AND Y IS U
POS E 15006.7 N -232.0 U 180.4

-- Reference Value: Booster/high-head volute circumferentially distributed axial casing rib 3/3
NEW CYLI
DIAM 11.0
HEIG 98.2
ORI Z IS S AND Y IS U
POS E 15209.3 N -232.0 U 180.4

-- Reference Value: high-head casing reinforcement band 1
NEW CYLI
DIAM 238.0
HEIG 8.0
ORI Z IS S AND Y IS U
POS E 15108.0 N -201.3 U 238.9

-- Reference Value: high-head casing reinforcement band 2
NEW CYLI
DIAM 238.0
HEIG 8.0
ORI Z IS S AND Y IS U
POS E 15108.0 N -267.7 U 238.9

NEW SUBE /203_PU_031_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 15225.6 N -308.4 U 238.9

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 15225.6 N -305.7 U 238.9

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 15225.6 N -311.3 U 238.9

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 15191.1 N -308.4 U 322.0

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 15191.1 N -305.7 U 322.0

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 15191.1 N -311.3 U 322.0

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 15108.0 N -308.4 U 356.5

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 15108.0 N -305.7 U 356.5

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 15108.0 N -311.3 U 356.5

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 15024.9 N -308.4 U 322.0

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 15024.9 N -305.7 U 322.0

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 15024.9 N -311.3 U 322.0

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 14990.4 N -308.4 U 238.9

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 14990.4 N -305.7 U 238.9

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 14990.4 N -311.3 U 238.9

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 15024.9 N -308.4 U 155.7

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 15024.9 N -305.7 U 155.7

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 15024.9 N -311.3 U 155.7

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 15108.0 N -308.4 U 121.3

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 15108.0 N -305.7 U 121.3

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 15108.0 N -311.3 U 121.3

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 15191.1 N -308.4 U 155.7

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 15191.1 N -305.7 U 155.7

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 15191.1 N -311.3 U 155.7

NEW SUBE /203_PU_031_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 52.9
HEIG 40.6
ORI Z IS S AND Y IS U
POS E 15108.0 N 22.1 U 238.9

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 61.0
HEIG 40.6
ORI Z IS S AND Y IS U
POS E 15108.0 N -18.5 U 238.9

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 69.0
HEIG 40.6
ORI Z IS S AND Y IS U
POS E 15108.0 N -59.1 U 238.9

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 77.1
HEIG 40.6
ORI Z IS S AND Y IS U
POS E 15108.0 N -99.7 U 238.9

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 50.6
DBOT 73.6
HEIG 24.9
ORI Z IS S AND Y IS U
POS E 15108.0 N -107.5 U 238.9

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 55.5
YLEN 113.7
ZLEN 102.3
POS E 15108.0 N -46.9 U 149.2

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 15108.0 N -48.5 U 287.4

NEW SUBE /203_PU_031_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction S
NEW NOZZLE /203_PU_031_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 15108.0 N -531.3 U 238.9
ORI P1 IS S
HEIG 162.4
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_031_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 15108.0 N -244.4 U 357.5

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /203_PU_031_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 15108.0 N -244.4 U 503.9
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_031_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 21.1
HEIG 189.4
ORI Z IS S AND Y IS U
POS E 15108.0 N 137.1 U 238.9

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 45.4
HEIG 45.0
ORI Z IS S AND Y IS U
POS E 15108.0 N 209.3 U 238.9

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 45.4
HEIG 45.0
ORI Z IS S AND Y IS U
POS E 15108.0 N 64.9 U 238.9

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 53.6
HEIG 28.0
ORI Z IS S AND Y IS U
POS E 15108.0 N 137.1 U 238.9

-- Reference Value: tapered coupling guard
NEW CONE
DTOP 110.0
DBOT 94.6
HEIG 189.4
ORI Z IS S AND Y IS U
POS E 15108.0 N 137.1 U 238.9

-- Reference Value: coupling-guard clamp band 1
NEW CYLI
DIAM 114.9
HEIG 8.5
ORI Z IS S AND Y IS U
POS E 15108.0 N 227.6 U 238.9

-- Reference Value: coupling-guard clamp band 2
NEW CYLI
DIAM 114.9
HEIG 8.5
ORI Z IS S AND Y IS U
POS E 15108.0 N 46.7 U 238.9

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 68.2
YLEN 24.0
ZLEN 85.9
POS E 15108.0 N 197.7 U 140.9

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 68.2
YLEN 24.0
ZLEN 85.9
POS E 15108.0 N 76.5 U 140.9

NEW SUBE /203_PU_031_DRIVER
-- Reference Value: Compact high-speed motor TEFC motor fan cowl
NEW CYLI
DIAM 202.2
HEIG 101.3
ORI Z IS S AND Y IS U
POS E 15108.0 N 744.0 U 238.9

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 219.8
DBOT 197.8
HEIG 45.6
ORI Z IS S AND Y IS U
POS E 15108.0 N 716.2 U 238.9

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile O2_TOP_SPOOL_BOOSTER
NEW CYLI
DIAM 219.8
HEIG 439.2
ORI Z IS S AND Y IS U
POS E 15108.0 N 502.1 U 238.9

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 158.2
DBOT 219.8
HEIG 50.7
ORI Z IS S AND Y IS U
POS E 15108.0 N 257.2 U 238.9

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 83.5
HEIG 11.1
ORI Z IS S AND Y IS U
POS E 15108.0 N 237.4 U 238.9

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 39.6
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 15108.0 N 790.6 U 238.9

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 148.3
YLEN 6.0
ZLEN 5.0
POS E 15108.0 N 791.7 U 180.3

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 5.0
YLEN 6.0
ZLEN 148.3
POS E 15049.4 N 791.7 U 238.9

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 179.7
YLEN 6.0
ZLEN 5.0
POS E 15108.0 N 791.7 U 209.6

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 5.0
YLEN 6.0
ZLEN 179.7
POS E 15078.7 N 791.7 U 238.9

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 189.0
YLEN 6.0
ZLEN 5.0
POS E 15108.0 N 791.7 U 238.9

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 5.0
YLEN 6.0
ZLEN 189.0
POS E 15108.0 N 791.7 U 238.9

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 179.7
YLEN 6.0
ZLEN 5.0
POS E 15108.0 N 791.7 U 268.2

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 5.0
YLEN 6.0
ZLEN 179.7
POS E 15137.3 N 791.7 U 238.9

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 148.3
YLEN 6.0
ZLEN 5.0
POS E 15108.0 N 791.7 U 297.5

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 5.0
YLEN 6.0
ZLEN 148.3
POS E 15166.6 N 791.7 U 238.9

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 90.9
YLEN 78.8
ZLEN 16.0
POS E 14969.2 N 642.7 U 106.0

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 38.2
YLEN 61.5
ZLEN 81.8
POS E 14989.2 N 642.7 U 154.9

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 90.9
YLEN 78.8
ZLEN 16.0
POS E 15246.8 N 642.7 U 106.0

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 38.2
YLEN 61.5
ZLEN 81.8
POS E 15226.8 N 642.7 U 154.9

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 90.9
YLEN 78.8
ZLEN 16.0
POS E 14969.2 N 383.8 U 106.0

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 38.2
YLEN 61.5
ZLEN 81.8
POS E 14989.2 N 383.8 U 154.9

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 90.9
YLEN 78.8
ZLEN 16.0
POS E 15246.8 N 383.8 U 106.0

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 38.2
YLEN 61.5
ZLEN 81.8
POS E 15226.8 N 383.8 U 154.9

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15108.0 N 502.1 U 351.4

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15064.9 N 502.1 U 342.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15028.4 N 502.1 U 318.4

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15004.0 N 502.1 U 281.9

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 14995.5 N 502.1 U 238.9

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15004.0 N 502.1 U 195.8

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15028.4 N 502.1 U 159.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15064.9 N 502.1 U 134.9

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15108.0 N 502.1 U 126.3

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15151.1 N 502.1 U 134.9

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15187.6 N 502.1 U 159.3

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15212.0 N 502.1 U 195.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15220.5 N 502.1 U 238.9

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15212.0 N 502.1 U 281.9

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15187.6 N 502.1 U 318.4

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 12.1
HEIG 386.5
ORI Z IS S AND Y IS U
POS E 15151.1 N 502.1 U 342.8

-- Reference Value: compact high-speed motor end-frame collar 1
NEW CYLI
DIAM 227.4
HEIG 12.3
ORI Z IS S AND Y IS U
POS E 15108.0 N 671.7 U 238.9

-- Reference Value: compact high-speed motor end-frame collar 2
NEW CYLI
DIAM 227.4
HEIG 12.3
ORI Z IS S AND Y IS U
POS E 15108.0 N 337.8 U 238.9

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 132.5
YLEN 112.6
ZLEN 50.7
POS E 15108.0 N 535.8 U 382.8

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 137.8
YLEN 117.1
ZLEN 6.1
POS E 15108.0 N 535.8 U 411.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 15060.3 N 578.5 U 415.9

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 15155.7 N 578.5 U 415.9

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 15060.3 N 493.0 U 415.9

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 15155.7 N 493.0 U 415.9

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 16.2
HEIG 6.6
ORI Z IS E AND Y IS U
POS E 15177.6 N 535.8 U 380.3

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 12.0
HEIG 7.8
ORI Z IS E AND Y IS U
POS E 15184.8 N 535.8 U 380.3

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 13.3
YLEN 36.0
ZLEN 39.4
POS E 15108.0 N 411.9 U 368.5

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 17.9
HEIG 22.5
ORI Z IS E AND Y IS U
POS E 15108.0 N 411.9 U 379.5

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 6.8
YLEN 90.1
ZLEN 33.8
POS E 14996.1 N 479.5 U 252.1

NEW SUBE /203_PU_031_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 13.3
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 14956.6 N 642.7 U 123.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 28.5
HEIG 3.0
ORI Z IS U AND Y IS N
POS E 14956.6 N 642.7 U 115.5

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 22.8
HEIG 8.2
ORI Z IS U AND Y IS N
POS E 14956.6 N 642.7 U 136.1

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 13.3
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 15259.4 N 642.7 U 123.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 28.5
HEIG 3.0
ORI Z IS U AND Y IS N
POS E 15259.4 N 642.7 U 115.5

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 22.8
HEIG 8.2
ORI Z IS U AND Y IS N
POS E 15259.4 N 642.7 U 136.1

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 13.3
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 14956.6 N 383.8 U 123.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 28.5
HEIG 3.0
ORI Z IS U AND Y IS N
POS E 14956.6 N 383.8 U 115.5

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 22.8
HEIG 8.2
ORI Z IS U AND Y IS N
POS E 14956.6 N 383.8 U 136.1

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 13.3
HEIG 18.0
ORI Z IS U AND Y IS N
POS E 15259.4 N 383.8 U 123.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 28.5
HEIG 3.0
ORI Z IS U AND Y IS N
POS E 15259.4 N 383.8 U 115.5

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 22.8
HEIG 8.2
ORI Z IS U AND Y IS N
POS E 15259.4 N 383.8 U 136.1

NEW SUBE /203_PU_031_SERVICE_DETAILS
-- Reference Value: compact pressure tapping boss
NEW CYLI
DIAM 16.0
HEIG 14.4
ORI Z IS U AND Y IS N
POS E 15108.0 N -244.4 U 351.9

-- Reference Value: booster bearing cooling rib
NEW BOX
XLEN 9.0
YLEN 79.7
ZLEN 12.0
POS E 15062.0 N -174.7 U 307.9

-- Reference Value: booster bearing cooling rib
NEW BOX
XLEN 9.0
YLEN 79.7
ZLEN 12.0
POS E 15154.0 N -174.7 U 307.9


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 147 primitives.
