-- ====================================================================
-- 204-PU-015 - PRESSURE SCREEN REJECTION DILUTION PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 204-PU-015
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /204_PU_015
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_015_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 863.0
YLEN 2135.0
ZLEN 50.0
POS E 22512.0 N 14092.0 U 25.0

NEW SUBE /204_PU_015_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.3
HEIG 23.3
ORI Z IS U AND Y IS N
POS E 22887.4 N 13141.9 U 52.8

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 37.1
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 22887.4 N 13141.9 U 51.9

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.7
HEIG 10.7
ORI Z IS U AND Y IS N
POS E 22887.4 N 13141.9 U 59.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.3
HEIG 23.3
ORI Z IS U AND Y IS N
POS E 22136.6 N 13141.9 U 52.8

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 37.1
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 22136.6 N 13141.9 U 51.9

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.7
HEIG 10.7
ORI Z IS U AND Y IS N
POS E 22136.6 N 13141.9 U 59.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.3
HEIG 23.3
ORI Z IS U AND Y IS N
POS E 22887.4 N 15042.1 U 52.8

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 37.1
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 22887.4 N 15042.1 U 51.9

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.7
HEIG 10.7
ORI Z IS U AND Y IS N
POS E 22887.4 N 15042.1 U 59.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.3
HEIG 23.3
ORI Z IS U AND Y IS N
POS E 22136.6 N 15042.1 U 52.8

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 37.1
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 22136.6 N 15042.1 U 51.9

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.7
HEIG 10.7
ORI Z IS U AND Y IS N
POS E 22136.6 N 15042.1 U 59.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.3
HEIG 23.3
ORI Z IS U AND Y IS N
POS E 22887.4 N 14092.0 U 52.8

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 37.1
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 22887.4 N 14092.0 U 51.9

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.7
HEIG 10.7
ORI Z IS U AND Y IS N
POS E 22887.4 N 14092.0 U 59.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.3
HEIG 23.3
ORI Z IS U AND Y IS N
POS E 22136.6 N 14092.0 U 52.8

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 37.1
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 22136.6 N 14092.0 U 51.9

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.7
HEIG 10.7
ORI Z IS U AND Y IS N
POS E 22136.6 N 14092.0 U 59.1

-- Reference Value: baseplate anchor fastener A7: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.3
HEIG 23.3
ORI Z IS U AND Y IS N
POS E 22512.0 N 13141.9 U 52.8

-- Reference Value: baseplate anchor fastener A7: solid washer under filled shank Reference Value
NEW CYLI
DIAM 37.1
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 22512.0 N 13141.9 U 51.9

-- Reference Value: baseplate anchor fastener A7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.7
HEIG 10.7
ORI Z IS U AND Y IS N
POS E 22512.0 N 13141.9 U 59.1

-- Reference Value: baseplate anchor fastener A8: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.3
HEIG 23.3
ORI Z IS U AND Y IS N
POS E 22512.0 N 15042.1 U 52.8

-- Reference Value: baseplate anchor fastener A8: solid washer under filled shank Reference Value
NEW CYLI
DIAM 37.1
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 22512.0 N 15042.1 U 51.9

-- Reference Value: baseplate anchor fastener A8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.7
HEIG 10.7
ORI Z IS U AND Y IS N
POS E 22512.0 N 15042.1 U 59.1

NEW SUBE /204_PU_015_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 69.0
YLEN 1750.7
ZLEN 64.7
POS E 22719.1 N 14049.3 U 82.4

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 69.0
YLEN 1750.7
ZLEN 64.7
POS E 22304.9 N 14049.3 U 82.4

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 621.4
YLEN 49.7
ZLEN 44.0
POS E 22512.0 N 13366.1 U 72.0

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 621.4
YLEN 49.7
ZLEN 44.0
POS E 22512.0 N 13850.0 U 72.0

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 621.4
YLEN 49.7
ZLEN 44.0
POS E 22512.0 N 14334.0 U 72.0

-- Reference Value: skid cross-member 4
NEW BOX
XLEN 621.4
YLEN 49.7
ZLEN 44.0
POS E 22512.0 N 14817.9 U 72.0

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 112.2
YLEN 160.1
ZLEN 107.1
POS E 22667.3 N 14653.3 U 103.6

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 112.2
YLEN 160.1
ZLEN 107.1
POS E 22356.7 N 14653.3 U 103.6

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 112.2
YLEN 160.1
ZLEN 107.1
POS E 22667.3 N 14875.5 U 103.6

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 112.2
YLEN 160.1
ZLEN 107.1
POS E 22356.7 N 14875.5 U 103.6

NEW SUBE /204_PU_015_CASING
-- Reference Value: General process volute back-pull-out rear plate
NEW CYLI
DIAM 300.1
HEIG 52.3
ORI Z IS N AND Y IS U
POS E 22512.0 N 14579.3 U 327.7

-- Reference Value: General process volute radially split casing envelope
NEW CYLI
DIAM 341.1
HEIG 261.3
ORI Z IS N AND Y IS U
POS E 22512.0 N 14736.1 U 327.7

-- Reference Value: casing split flange
NEW CYLI
DIAM 366.6
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 22512.0 N 14859.1 U 327.7

-- Reference Value: General process volute tapered impeller-eye cover
NEW CONE
DTOP 194.4
DBOT 334.2
HEIG 122.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 14927.7 U 327.7

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 204.6
HEIG 19.5
ORI Z IS N AND Y IS U
POS E 22512.0 N 14978.9 U 327.7

-- Reference Value: General process volute circumferentially distributed axial casing rib 1/3
NEW CYLI
DIAM 13.6
HEIG 177.7
ORI Z IS N AND Y IS U
POS E 22512.0 N 14736.1 U 500.7

-- Reference Value: General process volute circumferentially distributed axial casing rib 2/3
NEW CYLI
DIAM 13.6
HEIG 177.7
ORI Z IS N AND Y IS U
POS E 22661.8 N 14736.1 U 241.2

-- Reference Value: General process volute circumferentially distributed axial casing rib 3/3
NEW CYLI
DIAM 13.6
HEIG 177.7
ORI Z IS N AND Y IS U
POS E 22362.2 N 14736.1 U 241.2

NEW SUBE /204_PU_015_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22336.8 N 14871.7 U 327.7

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22336.8 N 14868.4 U 327.7

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22336.8 N 14874.6 U 327.7

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22360.3 N 14871.7 U 415.3

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22360.3 N 14868.4 U 415.3

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22360.3 N 14874.6 U 415.3

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22424.4 N 14871.7 U 479.4

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22424.4 N 14868.4 U 479.4

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22424.4 N 14874.6 U 479.4

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22512.0 N 14871.7 U 502.9

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22512.0 N 14868.4 U 502.9

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22512.0 N 14874.6 U 502.9

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22599.6 N 14871.7 U 479.4

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22599.6 N 14868.4 U 479.4

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22599.6 N 14874.6 U 479.4

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22663.7 N 14871.7 U 415.3

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22663.7 N 14868.4 U 415.3

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22663.7 N 14874.6 U 415.3

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22687.2 N 14871.7 U 327.7

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22687.2 N 14868.4 U 327.7

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22687.2 N 14874.6 U 327.7

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22663.7 N 14871.7 U 240.1

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22663.7 N 14868.4 U 240.1

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22663.7 N 14874.6 U 240.1

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22599.6 N 14871.7 U 175.9

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22599.6 N 14868.4 U 175.9

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22599.6 N 14874.6 U 175.9

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22512.0 N 14871.7 U 152.5

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22512.0 N 14868.4 U 152.5

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22512.0 N 14874.6 U 152.5

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22424.4 N 14871.7 U 175.9

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22424.4 N 14868.4 U 175.9

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22424.4 N 14874.6 U 175.9

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.3
HEIG 14.6
ORI Z IS N AND Y IS U
POS E 22360.3 N 14871.7 U 240.1

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 32.2
HEIG 3.4
ORI Z IS N AND Y IS U
POS E 22360.3 N 14868.4 U 240.1

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.4
HEIG 8.9
ORI Z IS N AND Y IS U
POS E 22360.3 N 14874.6 U 240.1

NEW SUBE /204_PU_015_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 78.4
HEIG 64.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 14329.0 U 327.7

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 90.4
HEIG 64.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 14393.0 U 327.7

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 102.3
HEIG 64.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 14457.1 U 327.7

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 114.3
HEIG 64.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 14521.1 U 327.7

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 75.0
DBOT 109.1
HEIG 43.6
ORI Z IS N AND Y IS U
POS E 22512.0 N 14531.4 U 327.7

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 82.3
YLEN 179.3
ZLEN 155.8
POS E 22512.0 N 14437.9 U 192.6

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 22512.0 N 14440.4 U 394.8

NEW SUBE /204_PU_015_SUCTION
-- Reference Value: suction DN100; POS is flange face, contractual direction N
NEW NOZZLE /204_PU_015_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 22512.0 N 15238.7 U 327.7
ORI P1 IS N
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_015_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 22512.0 N 14770.9 U 501.8

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /204_PU_015_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 22512.0 N 14770.9 U 653.5
ORI P1 IS U
HEIG 155.3
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_015_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 31.9
HEIG 298.9
ORI Z IS N AND Y IS U
POS E 22512.0 N 14147.5 U 327.7

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 68.7
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 14020.6 U 327.7

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 68.7
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 14274.5 U 327.7

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 81.0
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 14147.5 U 327.7

-- Reference Value: fabricated rectangular coupling guard
NEW BOX
XLEN 148.9
YLEN 298.9
ZLEN 126.2
POS E 22512.0 N 14147.5 U 327.7

-- Reference Value: boxed guard top reinforcing seam
NEW BOX
XLEN 8.9
YLEN 245.1
ZLEN 8.9
POS E 22512.0 N 14147.5 U 395.6

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 100.3
YLEN 35.9
ZLEN 132.0
POS E 22512.0 N 14051.9 U 180.7

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 100.3
YLEN 35.9
ZLEN 132.0
POS E 22512.0 N 14243.2 U 180.7

NEW SUBE /204_PU_015_DRIVER
-- Reference Value: Heavy-duty high-torque motor TEFC motor fan cowl
NEW CYLI
DIAM 358.9
HEIG 123.1
ORI Z IS N AND Y IS U
POS E 22512.0 N 13180.0 U 327.7

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 366.3
DBOT 329.6
HEIG 55.4
ORI Z IS N AND Y IS U
POS E 22512.0 N 13213.9 U 327.7

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile LARGE_PROCESS_PUMP_CORE
NEW CYLI
DIAM 366.3
HEIG 685.4
ORI Z IS N AND Y IS U
POS E 22512.0 N 13549.8 U 327.7

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 263.7
DBOT 366.3
HEIG 105.6
ORI Z IS N AND Y IS U
POS E 22512.0 N 13945.3 U 327.7

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 139.2
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 13989.1 U 327.7

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 65.9
HEIG 12.4
ORI Z IS S AND Y IS U
POS E 22512.0 N 13124.6 U 327.7

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 247.1
YLEN 9.2
ZLEN 6.6
POS E 22512.0 N 13123.0 U 230.0

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 6.6
YLEN 9.2
ZLEN 247.1
POS E 22609.6 N 13123.0 U 327.7

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 299.5
YLEN 9.2
ZLEN 6.6
POS E 22512.0 N 13123.0 U 278.8

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 6.6
YLEN 9.2
ZLEN 299.5
POS E 22560.8 N 13123.0 U 327.7

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 315.0
YLEN 9.2
ZLEN 6.6
POS E 22512.0 N 13123.0 U 327.7

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 6.6
YLEN 9.2
ZLEN 315.0
POS E 22512.0 N 13123.0 U 327.7

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 299.5
YLEN 9.2
ZLEN 6.6
POS E 22512.0 N 13123.0 U 376.5

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 6.6
YLEN 9.2
ZLEN 299.5
POS E 22463.2 N 13123.0 U 327.7

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 247.1
YLEN 9.2
ZLEN 6.6
POS E 22512.0 N 13123.0 U 425.3

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 6.6
YLEN 9.2
ZLEN 247.1
POS E 22414.4 N 13123.0 U 327.7

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 124.3
YLEN 123.1
ZLEN 23.4
POS E 22701.9 N 13355.9 U 126.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 52.2
YLEN 96.1
ZLEN 71.9
POS E 22674.5 N 13355.9 U 174.1

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 124.3
YLEN 123.1
ZLEN 23.4
POS E 22322.1 N 13355.9 U 126.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 52.2
YLEN 96.1
ZLEN 71.9
POS E 22349.5 N 13355.9 U 174.1

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 124.3
YLEN 123.1
ZLEN 23.4
POS E 22701.9 N 13760.6 U 126.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 52.2
YLEN 96.1
ZLEN 71.9
POS E 22674.5 N 13760.6 U 174.1

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 124.3
YLEN 123.1
ZLEN 23.4
POS E 22322.1 N 13760.6 U 126.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 52.2
YLEN 96.1
ZLEN 71.9
POS E 22349.5 N 13760.6 U 174.1

-- Reference Value: 360-degree motor cooling rib 1/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22512.0 N 13549.8 U 515.2

-- Reference Value: 360-degree motor cooling rib 2/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22576.2 N 13549.8 U 503.9

-- Reference Value: 360-degree motor cooling rib 3/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22632.6 N 13549.8 U 471.4

-- Reference Value: 360-degree motor cooling rib 4/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22674.4 N 13549.8 U 421.5

-- Reference Value: 360-degree motor cooling rib 5/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22696.7 N 13549.8 U 360.2

-- Reference Value: 360-degree motor cooling rib 6/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22696.7 N 13549.8 U 295.1

-- Reference Value: 360-degree motor cooling rib 7/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22674.4 N 13549.8 U 233.9

-- Reference Value: 360-degree motor cooling rib 8/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22632.6 N 13549.8 U 184.0

-- Reference Value: 360-degree motor cooling rib 9/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22576.2 N 13549.8 U 151.4

-- Reference Value: 360-degree motor cooling rib 10/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22512.0 N 13549.8 U 140.1

-- Reference Value: 360-degree motor cooling rib 11/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22447.8 N 13549.8 U 151.4

-- Reference Value: 360-degree motor cooling rib 12/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22391.4 N 13549.8 U 184.0

-- Reference Value: 360-degree motor cooling rib 13/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22349.6 N 13549.8 U 233.9

-- Reference Value: 360-degree motor cooling rib 14/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22327.3 N 13549.8 U 295.1

-- Reference Value: 360-degree motor cooling rib 15/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22327.3 N 13549.8 U 360.2

-- Reference Value: 360-degree motor cooling rib 16/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22349.6 N 13549.8 U 421.5

-- Reference Value: 360-degree motor cooling rib 17/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22391.4 N 13549.8 U 471.4

-- Reference Value: 360-degree motor cooling rib 18/18
NEW CYLI
DIAM 20.1
HEIG 603.2
ORI Z IS N AND Y IS U
POS E 22447.8 N 13549.8 U 503.9

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 1/2
NEW CYLI
DIAM 386.4
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 13435.6 U 327.7

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 2/2
NEW CYLI
DIAM 386.4
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 13664.0 U 327.7

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 238.2
YLEN 246.3
ZLEN 98.0
POS E 22512.0 N 13523.1 U 574.3

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 247.7
YLEN 256.1
ZLEN 11.8
POS E 22512.0 N 13523.1 U 629.1

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.8
HEIG 6.5
ORI Z IS U AND Y IS N
POS E 22597.7 N 13429.5 U 638.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.8
HEIG 6.5
ORI Z IS U AND Y IS N
POS E 22426.3 N 13429.5 U 638.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.8
HEIG 6.5
ORI Z IS U AND Y IS N
POS E 22597.7 N 13616.7 U 638.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.8
HEIG 6.5
ORI Z IS U AND Y IS N
POS E 22426.3 N 13616.7 U 638.2

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 29.1
HEIG 11.9
ORI Z IS W AND Y IS U
POS E 22387.0 N 13523.1 U 569.4

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 21.6
HEIG 14.0
ORI Z IS W AND Y IS U
POS E 22374.0 N 13523.1 U 569.4

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 18.1
YLEN 78.8
ZLEN 58.0
POS E 22512.0 N 13716.6 U 539.8

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 24.5
HEIG 30.8
ORI Z IS W AND Y IS U
POS E 22512.0 N 13716.6 U 556.0

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 9.0
YLEN 140.7
ZLEN 51.1
POS E 22697.1 N 13611.0 U 349.6

NEW SUBE /204_PU_015_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 18.1
HEIG 24.5
ORI Z IS U AND Y IS N
POS E 22719.1 N 13355.9 U 150.4

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 39.0
HEIG 4.0
ORI Z IS U AND Y IS N
POS E 22719.1 N 13355.9 U 140.1

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 31.2
HEIG 11.2
ORI Z IS U AND Y IS N
POS E 22719.1 N 13355.9 U 168.2

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 18.1
HEIG 24.5
ORI Z IS U AND Y IS N
POS E 22304.9 N 13355.9 U 150.4

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 39.0
HEIG 4.0
ORI Z IS U AND Y IS N
POS E 22304.9 N 13355.9 U 140.1

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 31.2
HEIG 11.2
ORI Z IS U AND Y IS N
POS E 22304.9 N 13355.9 U 168.2

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 18.1
HEIG 24.5
ORI Z IS U AND Y IS N
POS E 22719.1 N 13760.6 U 150.4

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 39.0
HEIG 4.0
ORI Z IS U AND Y IS N
POS E 22719.1 N 13760.6 U 140.1

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 31.2
HEIG 11.2
ORI Z IS U AND Y IS N
POS E 22719.1 N 13760.6 U 168.2

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 18.1
HEIG 24.5
ORI Z IS U AND Y IS N
POS E 22304.9 N 13760.6 U 150.4

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 39.0
HEIG 4.0
ORI Z IS U AND Y IS N
POS E 22304.9 N 13760.6 U 140.1

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 31.2
HEIG 11.2
ORI Z IS U AND Y IS N
POS E 22304.9 N 13760.6 U 168.2

NEW SUBE /204_PU_015_SERVICE_DETAILS
-- Reference Value: dilution-pump vent/flush boss
NEW CYLI
DIAM 22.0
HEIG 17.6
ORI Z IS U AND Y IS N
POS E 22450.6 N 14736.1 U 479.7


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 163 primitives.
