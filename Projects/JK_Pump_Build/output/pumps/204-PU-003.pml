-- ====================================================================
-- 204-PU-003 - PRIMARY SCREEN FEED PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 204-PU-003
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /204_PU_003
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_003_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 857.0
YLEN 2129.0
ZLEN 50.0
POS E 20162.0 N -8768.0 U 25.0

NEW SUBE /204_PU_003_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.1
HEIG 23.1
ORI Z IS U AND Y IS N
POS E 20534.8 N -9715.4 U 52.8

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.9
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 20534.8 N -9715.4 U 51.9

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.5
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 20534.8 N -9715.4 U 59.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.1
HEIG 23.1
ORI Z IS U AND Y IS N
POS E 19789.2 N -9715.4 U 52.8

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.9
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 19789.2 N -9715.4 U 51.9

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.5
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 19789.2 N -9715.4 U 59.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.1
HEIG 23.1
ORI Z IS U AND Y IS N
POS E 20534.8 N -7820.6 U 52.8

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.9
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 20534.8 N -7820.6 U 51.9

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.5
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 20534.8 N -7820.6 U 59.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.1
HEIG 23.1
ORI Z IS U AND Y IS N
POS E 19789.2 N -7820.6 U 52.8

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.9
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 19789.2 N -7820.6 U 51.9

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.5
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 19789.2 N -7820.6 U 59.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.1
HEIG 23.1
ORI Z IS U AND Y IS N
POS E 20534.8 N -8768.0 U 52.8

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.9
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 20534.8 N -8768.0 U 51.9

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.5
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 20534.8 N -8768.0 U 59.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.1
HEIG 23.1
ORI Z IS U AND Y IS N
POS E 19789.2 N -8768.0 U 52.8

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.9
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 19789.2 N -8768.0 U 51.9

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.5
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 19789.2 N -8768.0 U 59.1

-- Reference Value: baseplate anchor fastener A7: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.1
HEIG 23.1
ORI Z IS U AND Y IS N
POS E 20162.0 N -9715.4 U 52.8

-- Reference Value: baseplate anchor fastener A7: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.9
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 20162.0 N -9715.4 U 51.9

-- Reference Value: baseplate anchor fastener A7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.5
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 20162.0 N -9715.4 U 59.1

-- Reference Value: baseplate anchor fastener A8: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.1
HEIG 23.1
ORI Z IS U AND Y IS N
POS E 20162.0 N -7820.6 U 52.8

-- Reference Value: baseplate anchor fastener A8: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.9
HEIG 3.8
ORI Z IS U AND Y IS N
POS E 20162.0 N -7820.6 U 51.9

-- Reference Value: baseplate anchor fastener A8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.5
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 20162.0 N -7820.6 U 59.1

NEW SUBE /204_PU_003_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 68.6
YLEN 1745.8
ZLEN 64.3
POS E 20367.7 N -8810.6 U 82.1

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 68.6
YLEN 1745.8
ZLEN 64.3
POS E 19956.3 N -8810.6 U 82.1

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 617.0
YLEN 49.4
ZLEN 43.7
POS E 20162.0 N -9491.9 U 71.9

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 617.0
YLEN 49.4
ZLEN 43.7
POS E 20162.0 N -9009.3 U 71.9

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 617.0
YLEN 49.4
ZLEN 43.7
POS E 20162.0 N -8526.7 U 71.9

-- Reference Value: skid cross-member 4
NEW BOX
XLEN 617.0
YLEN 49.4
ZLEN 43.7
POS E 20162.0 N -8044.1 U 71.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 111.4
YLEN 159.7
ZLEN 106.3
POS E 20316.3 N -8189.6 U 103.2

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 111.4
YLEN 159.7
ZLEN 106.3
POS E 20007.7 N -8189.6 U 103.2

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 111.4
YLEN 159.7
ZLEN 106.3
POS E 20316.3 N -7955.1 U 103.2

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 111.4
YLEN 159.7
ZLEN 106.3
POS E 20007.7 N -7955.1 U 103.2

NEW SUBE /204_PU_003_CASING
-- Reference Value: Stock/screen-feed open-impeller volute back-pull-out rear plate
NEW CYLI
DIAM 312.4
HEIG 46.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -8272.4 U 333.8

-- Reference Value: Stock/screen-feed open-impeller volute radially split casing envelope
NEW CYLI
DIAM 355.0
HEIG 294.3
ORI Z IS N AND Y IS U
POS E 20162.0 N -8102.2 U 333.8

-- Reference Value: casing split flange
NEW CYLI
DIAM 390.5
HEIG 16.1
ORI Z IS N AND Y IS U
POS E 20162.0 N -7963.1 U 333.8

-- Reference Value: Stock/screen-feed open-impeller volute tapered impeller-eye cover
NEW CONE
DTOP 220.1
DBOT 347.9
HEIG 119.6
ORI Z IS N AND Y IS U
POS E 20162.0 N -7895.3 U 333.8

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 230.7
HEIG 19.1
ORI Z IS N AND Y IS U
POS E 20162.0 N -7845.1 U 333.8

-- Reference Value: Stock/screen-feed open-impeller volute circumferentially distributed axial casing rib 1/5
NEW CYLI
DIAM 14.2
HEIG 200.1
ORI Z IS N AND Y IS U
POS E 20162.0 N -8102.2 U 513.8

-- Reference Value: Stock/screen-feed open-impeller volute circumferentially distributed axial casing rib 2/5
NEW CYLI
DIAM 14.2
HEIG 200.1
ORI Z IS N AND Y IS U
POS E 20333.2 N -8102.2 U 389.4

-- Reference Value: Stock/screen-feed open-impeller volute circumferentially distributed axial casing rib 3/5
NEW CYLI
DIAM 14.2
HEIG 200.1
ORI Z IS N AND Y IS U
POS E 20267.8 N -8102.2 U 188.1

-- Reference Value: Stock/screen-feed open-impeller volute circumferentially distributed axial casing rib 4/5
NEW CYLI
DIAM 14.2
HEIG 200.1
ORI Z IS N AND Y IS U
POS E 20056.2 N -8102.2 U 188.1

-- Reference Value: Stock/screen-feed open-impeller volute circumferentially distributed axial casing rib 5/5
NEW CYLI
DIAM 14.2
HEIG 200.1
ORI Z IS N AND Y IS U
POS E 19990.8 N -8102.2 U 389.4

NEW SUBE /204_PU_003_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 19977.4 N -7949.9 U 333.8

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 19977.4 N -7953.3 U 333.8

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 19977.4 N -7946.9 U 333.8

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 19995.7 N -7949.9 U 413.9

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 19995.7 N -7953.3 U 413.9

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 19995.7 N -7946.9 U 413.9

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20046.9 N -7949.9 U 478.1

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20046.9 N -7953.3 U 478.1

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20046.9 N -7946.9 U 478.1

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20120.9 N -7949.9 U 513.8

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20120.9 N -7953.3 U 513.8

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20120.9 N -7946.9 U 513.8

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20203.1 N -7949.9 U 513.8

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20203.1 N -7953.3 U 513.8

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20203.1 N -7946.9 U 513.8

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20277.1 N -7949.9 U 478.1

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20277.1 N -7953.3 U 478.1

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20277.1 N -7946.9 U 478.1

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20328.3 N -7949.9 U 413.9

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20328.3 N -7953.3 U 413.9

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20328.3 N -7946.9 U 413.9

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20346.6 N -7949.9 U 333.8

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20346.6 N -7953.3 U 333.8

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20346.6 N -7946.9 U 333.8

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20328.3 N -7949.9 U 253.7

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20328.3 N -7953.3 U 253.7

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20328.3 N -7946.9 U 253.7

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20277.1 N -7949.9 U 189.5

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20277.1 N -7953.3 U 189.5

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20277.1 N -7946.9 U 189.5

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20203.1 N -7949.9 U 153.8

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20203.1 N -7953.3 U 153.8

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20203.1 N -7946.9 U 153.8

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20120.9 N -7949.9 U 153.8

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20120.9 N -7953.3 U 153.8

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20120.9 N -7946.9 U 153.8

-- Reference Value: casing split-line bolt C13: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 20046.9 N -7949.9 U 189.5

-- Reference Value: casing split-line bolt C13: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 20046.9 N -7953.3 U 189.5

-- Reference Value: casing split-line bolt C13: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 20046.9 N -7946.9 U 189.5

-- Reference Value: casing split-line bolt C14: flange-penetrating stud Reference Value
NEW CYLI
DIAM 16.0
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 19995.7 N -7949.9 U 253.7

-- Reference Value: casing split-line bolt C14: flange-face washer Reference Value
NEW CYLI
DIAM 33.5
HEIG 3.5
ORI Z IS N AND Y IS U
POS E 19995.7 N -7953.3 U 253.7

-- Reference Value: casing split-line bolt C14: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.3
ORI Z IS N AND Y IS U
POS E 19995.7 N -7946.9 U 253.7

NEW SUBE /204_PU_003_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 81.6
HEIG 51.1
ORI Z IS N AND Y IS U
POS E 20162.0 N -8525.3 U 333.8

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 94.1
HEIG 51.1
ORI Z IS N AND Y IS U
POS E 20162.0 N -8474.2 U 333.8

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 106.5
HEIG 51.1
ORI Z IS N AND Y IS U
POS E 20162.0 N -8423.1 U 333.8

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 118.9
HEIG 51.1
ORI Z IS N AND Y IS U
POS E 20162.0 N -8372.0 U 333.8

-- Reference Value: stepped bearing bracket section 5
NEW CYLI
DIAM 131.3
HEIG 51.1
ORI Z IS N AND Y IS U
POS E 20162.0 N -8320.9 U 333.8

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 78.1
DBOT 113.6
HEIG 46.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -8318.4 U 333.8

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 94.6
YLEN 178.8
ZLEN 153.9
POS E 20162.0 N -8410.3 U 191.2

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 20162.0 N -8407.8 U 409.5

NEW SUBE /204_PU_003_SUCTION
-- Reference Value: suction DN100; POS is flange face, contractual direction N
NEW NOZZLE /204_PU_003_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 20162.0 N -7585.5 U 333.8
ORI P1 IS N
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_003_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 20162.0 N -8065.4 U 514.9

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /204_PU_003_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 20162.0 N -8065.4 U 665.5
ORI P1 IS U
HEIG 154.3
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_003_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 32.9
HEIG 298.1
ORI Z IS N AND Y IS U
POS E 20162.0 N -8699.9 U 333.8

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 70.8
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -8826.4 U 333.8

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 70.8
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -8573.3 U 333.8

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 83.5
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -8699.9 U 333.8

-- Reference Value: fabricated rectangular coupling guard
NEW BOX
XLEN 153.5
YLEN 298.1
ZLEN 130.1
POS E 20162.0 N -8699.9 U 333.8

-- Reference Value: boxed guard top reinforcing seam
NEW BOX
XLEN 9.2
YLEN 244.4
ZLEN 9.2
POS E 20162.0 N -8699.9 U 403.9

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 103.4
YLEN 35.8
ZLEN 136.1
POS E 20162.0 N -8795.3 U 182.3

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 103.4
YLEN 35.8
ZLEN 136.1
POS E 20162.0 N -8604.5 U 182.3

NEW SUBE /204_PU_003_DRIVER
-- Reference Value: Heavy-duty high-torque motor TEFC motor fan cowl
NEW CYLI
DIAM 370.0
HEIG 126.4
ORI Z IS N AND Y IS U
POS E 20162.0 N -9688.4 U 333.8

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 377.6
DBOT 339.8
HEIG 56.9
ORI Z IS N AND Y IS U
POS E 20162.0 N -9653.7 U 333.8

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile LARGE_STOCK_PUMP_CORE
NEW CYLI
DIAM 377.6
HEIG 703.4
ORI Z IS N AND Y IS U
POS E 20162.0 N -9308.9 U 333.8

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 271.9
DBOT 377.6
HEIG 108.3
ORI Z IS N AND Y IS U
POS E 20162.0 N -8903.1 U 333.8

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 143.5
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -8857.9 U 333.8

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 68.0
HEIG 12.7
ORI Z IS S AND Y IS U
POS E 20162.0 N -9745.2 U 333.8

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 254.8
YLEN 9.4
ZLEN 6.8
POS E 20162.0 N -9746.9 U 233.1

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 6.8
YLEN 9.4
ZLEN 254.8
POS E 20262.7 N -9746.9 U 333.8

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 308.7
YLEN 9.4
ZLEN 6.8
POS E 20162.0 N -9746.9 U 283.5

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 6.8
YLEN 9.4
ZLEN 308.7
POS E 20212.3 N -9746.9 U 333.8

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 324.7
YLEN 9.4
ZLEN 6.8
POS E 20162.0 N -9746.9 U 333.8

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 6.8
YLEN 9.4
ZLEN 324.7
POS E 20162.0 N -9746.9 U 333.8

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 308.7
YLEN 9.4
ZLEN 6.8
POS E 20162.0 N -9746.9 U 384.1

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 6.8
YLEN 9.4
ZLEN 308.7
POS E 20111.7 N -9746.9 U 333.8

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 254.8
YLEN 9.4
ZLEN 6.8
POS E 20162.0 N -9746.9 U 434.5

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 6.8
YLEN 9.4
ZLEN 254.8
POS E 20061.3 N -9746.9 U 333.8

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 123.4
YLEN 126.4
ZLEN 24.1
POS E 20350.5 N -9507.9 U 126.3

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 51.8
YLEN 98.6
ZLEN 68.6
POS E 20323.4 N -9507.9 U 172.7

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 123.4
YLEN 126.4
ZLEN 24.1
POS E 19973.5 N -9507.9 U 126.3

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 51.8
YLEN 98.6
ZLEN 68.6
POS E 20000.6 N -9507.9 U 172.7

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 123.4
YLEN 126.4
ZLEN 24.1
POS E 20350.5 N -9092.6 U 126.3

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 51.8
YLEN 98.6
ZLEN 68.6
POS E 20323.4 N -9092.6 U 172.7

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 123.4
YLEN 126.4
ZLEN 24.1
POS E 19973.5 N -9092.6 U 126.3

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 51.8
YLEN 98.6
ZLEN 68.6
POS E 20000.6 N -9092.6 U 172.7

-- Reference Value: 360-degree motor cooling rib 1/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -9308.9 U 527.2

-- Reference Value: 360-degree motor cooling rib 2/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20221.8 N -9308.9 U 517.7

-- Reference Value: 360-degree motor cooling rib 3/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20275.7 N -9308.9 U 490.2

-- Reference Value: 360-degree motor cooling rib 4/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20318.4 N -9308.9 U 447.4

-- Reference Value: 360-degree motor cooling rib 5/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20345.9 N -9308.9 U 393.5

-- Reference Value: 360-degree motor cooling rib 6/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20355.4 N -9308.9 U 333.8

-- Reference Value: 360-degree motor cooling rib 7/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20345.9 N -9308.9 U 274.0

-- Reference Value: 360-degree motor cooling rib 8/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20318.4 N -9308.9 U 220.1

-- Reference Value: 360-degree motor cooling rib 9/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20275.7 N -9308.9 U 177.4

-- Reference Value: 360-degree motor cooling rib 10/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20221.8 N -9308.9 U 149.9

-- Reference Value: 360-degree motor cooling rib 11/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -9308.9 U 140.4

-- Reference Value: 360-degree motor cooling rib 12/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20102.2 N -9308.9 U 149.9

-- Reference Value: 360-degree motor cooling rib 13/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20048.3 N -9308.9 U 177.4

-- Reference Value: 360-degree motor cooling rib 14/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20005.6 N -9308.9 U 220.1

-- Reference Value: 360-degree motor cooling rib 15/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 19978.1 N -9308.9 U 274.0

-- Reference Value: 360-degree motor cooling rib 16/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 19968.6 N -9308.9 U 333.8

-- Reference Value: 360-degree motor cooling rib 17/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 19978.1 N -9308.9 U 393.5

-- Reference Value: 360-degree motor cooling rib 18/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20005.6 N -9308.9 U 447.4

-- Reference Value: 360-degree motor cooling rib 19/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20048.3 N -9308.9 U 490.2

-- Reference Value: 360-degree motor cooling rib 20/20
NEW CYLI
DIAM 20.8
HEIG 619.0
ORI Z IS N AND Y IS U
POS E 20102.2 N -9308.9 U 517.7

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 1/2
NEW CYLI
DIAM 398.3
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -9426.1 U 333.8

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 2/2
NEW CYLI
DIAM 398.3
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 20162.0 N -9191.7 U 333.8

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 236.5
YLEN 252.8
ZLEN 101.0
POS E 20162.0 N -9336.4 U 588.0

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 246.0
YLEN 262.9
ZLEN 12.0
POS E 20162.0 N -9336.4 U 644.5

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.7
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 20247.2 N -9432.4 U 653.8

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.7
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 20076.8 N -9432.4 U 653.8

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.7
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 20247.2 N -9240.3 U 653.8

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.7
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 20076.8 N -9240.3 U 653.8

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 30.0
HEIG 12.2
ORI Z IS W AND Y IS U
POS E 20037.6 N -9336.4 U 583.0

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 22.2
HEIG 14.4
ORI Z IS W AND Y IS U
POS E 20024.3 N -9336.4 U 583.0

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 18.0
YLEN 80.9
ZLEN 58.0
POS E 20162.0 N -9137.8 U 551.6

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 24.3
HEIG 30.6
ORI Z IS W AND Y IS U
POS E 20162.0 N -9137.8 U 567.8

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 9.0
YLEN 144.4
ZLEN 52.7
POS E 20352.8 N -9246.1 U 356.5

NEW SUBE /204_PU_003_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 18.0
HEIG 24.3
ORI Z IS U AND Y IS N
POS E 20367.7 N -9507.9 U 150.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 38.7
HEIG 4.0
ORI Z IS U AND Y IS N
POS E 20367.7 N -9507.9 U 140.4

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 31.0
HEIG 11.2
ORI Z IS U AND Y IS N
POS E 20367.7 N -9507.9 U 168.3

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 18.0
HEIG 24.3
ORI Z IS U AND Y IS N
POS E 19956.3 N -9507.9 U 150.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 38.7
HEIG 4.0
ORI Z IS U AND Y IS N
POS E 19956.3 N -9507.9 U 140.4

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 31.0
HEIG 11.2
ORI Z IS U AND Y IS N
POS E 19956.3 N -9507.9 U 168.3

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 18.0
HEIG 24.3
ORI Z IS U AND Y IS N
POS E 20367.7 N -9092.6 U 150.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 38.7
HEIG 4.0
ORI Z IS U AND Y IS N
POS E 20367.7 N -9092.6 U 140.4

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 31.0
HEIG 11.2
ORI Z IS U AND Y IS N
POS E 20367.7 N -9092.6 U 168.3

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 18.0
HEIG 24.3
ORI Z IS U AND Y IS N
POS E 19956.3 N -9092.6 U 150.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 38.7
HEIG 4.0
ORI Z IS U AND Y IS N
POS E 19956.3 N -9092.6 U 140.4

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 31.0
HEIG 11.2
ORI Z IS U AND Y IS N
POS E 19956.3 N -9092.6 U 168.3

NEW SUBE /204_PU_003_SERVICE_DETAILS
-- Reference Value: stock-duty casing clean-out cover
NEW CYLI
DIAM 106.5
HEIG 12.0
ORI Z IS W AND Y IS U
POS E 19978.5 N -8065.4 U 333.8

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS W AND Y IS U
POS E 19968.6 N -8065.4 U 306.1

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS W AND Y IS U
POS E 19968.6 N -8065.4 U 361.5

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS W AND Y IS U
POS E 19968.6 N -8093.1 U 333.8

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS W AND Y IS U
POS E 19968.6 N -8037.7 U 333.8


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 178 primitives.
