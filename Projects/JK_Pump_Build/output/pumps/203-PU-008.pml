-- ====================================================================
-- 203-PU-008 - BLOW TANK DILUTION PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 203-PU-008
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:27

NEW EQUI /203_PU_008
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_008_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 852.0
YLEN 2136.0
ZLEN 50.0
POS E 13971.0 N 14110.0 U 25.0

NEW SUBE /203_PU_008_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.0
HEIG 23.0
ORI Z IS U AND Y IS N
POS E 14341.6 N 13159.5 U 52.8

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.6
HEIG 3.7
ORI Z IS U AND Y IS N
POS E 14341.6 N 13159.5 U 51.9

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.3
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 14341.6 N 13159.5 U 59.0

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.0
HEIG 23.0
ORI Z IS U AND Y IS N
POS E 13600.4 N 13159.5 U 52.8

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.6
HEIG 3.7
ORI Z IS U AND Y IS N
POS E 13600.4 N 13159.5 U 51.9

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.3
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 13600.4 N 13159.5 U 59.0

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.0
HEIG 23.0
ORI Z IS U AND Y IS N
POS E 14341.6 N 15060.5 U 52.8

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.6
HEIG 3.7
ORI Z IS U AND Y IS N
POS E 14341.6 N 15060.5 U 51.9

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.3
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 14341.6 N 15060.5 U 59.0

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.0
HEIG 23.0
ORI Z IS U AND Y IS N
POS E 13600.4 N 15060.5 U 52.8

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.6
HEIG 3.7
ORI Z IS U AND Y IS N
POS E 13600.4 N 15060.5 U 51.9

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.3
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 13600.4 N 15060.5 U 59.0

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.0
HEIG 23.0
ORI Z IS U AND Y IS N
POS E 14341.6 N 14110.0 U 52.8

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.6
HEIG 3.7
ORI Z IS U AND Y IS N
POS E 14341.6 N 14110.0 U 51.9

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.3
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 14341.6 N 14110.0 U 59.0

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.0
HEIG 23.0
ORI Z IS U AND Y IS N
POS E 13600.4 N 14110.0 U 52.8

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.6
HEIG 3.7
ORI Z IS U AND Y IS N
POS E 13600.4 N 14110.0 U 51.9

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.3
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 13600.4 N 14110.0 U 59.0

-- Reference Value: baseplate anchor fastener A7: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.0
HEIG 23.0
ORI Z IS U AND Y IS N
POS E 13971.0 N 13159.5 U 52.8

-- Reference Value: baseplate anchor fastener A7: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.6
HEIG 3.7
ORI Z IS U AND Y IS N
POS E 13971.0 N 13159.5 U 51.9

-- Reference Value: baseplate anchor fastener A7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.3
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 13971.0 N 13159.5 U 59.0

-- Reference Value: baseplate anchor fastener A8: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.0
HEIG 23.0
ORI Z IS U AND Y IS N
POS E 13971.0 N 15060.5 U 52.8

-- Reference Value: baseplate anchor fastener A8: solid washer under filled shank Reference Value
NEW CYLI
DIAM 36.6
HEIG 3.7
ORI Z IS U AND Y IS N
POS E 13971.0 N 15060.5 U 51.9

-- Reference Value: baseplate anchor fastener A8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 29.3
HEIG 10.6
ORI Z IS U AND Y IS N
POS E 13971.0 N 15060.5 U 59.0

NEW SUBE /203_PU_008_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 68.2
YLEN 1751.5
ZLEN 63.9
POS E 14175.5 N 14067.3 U 82.0

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 68.2
YLEN 1751.5
ZLEN 63.9
POS E 13766.5 N 14067.3 U 82.0

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 613.4
YLEN 49.1
ZLEN 43.5
POS E 13971.0 N 13383.8 U 71.7

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 613.4
YLEN 49.1
ZLEN 43.5
POS E 13971.0 N 13867.9 U 71.7

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 613.4
YLEN 49.1
ZLEN 43.5
POS E 13971.0 N 14352.1 U 71.7

-- Reference Value: skid cross-member 4
NEW BOX
XLEN 613.4
YLEN 49.1
ZLEN 43.5
POS E 13971.0 N 14836.2 U 71.7

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 110.8
YLEN 160.2
ZLEN 105.8
POS E 14124.4 N 14671.6 U 102.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 110.8
YLEN 160.2
ZLEN 105.8
POS E 13817.6 N 14671.6 U 102.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 110.8
YLEN 160.2
ZLEN 105.8
POS E 14124.4 N 14893.8 U 102.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 110.8
YLEN 160.2
ZLEN 105.8
POS E 13817.6 N 14893.8 U 102.9

NEW SUBE /203_PU_008_CASING
-- Reference Value: General process volute back-pull-out rear plate
NEW CYLI
DIAM 296.3
HEIG 52.3
ORI Z IS N AND Y IS U
POS E 13971.0 N 14597.5 U 324.1

-- Reference Value: General process volute radially split casing envelope
NEW CYLI
DIAM 336.7
HEIG 261.4
ORI Z IS N AND Y IS U
POS E 13971.0 N 14754.4 U 324.1

-- Reference Value: casing split flange
NEW CYLI
DIAM 362.0
HEIG 15.3
ORI Z IS N AND Y IS U
POS E 13971.0 N 14877.5 U 324.1

-- Reference Value: General process volute tapered impeller-eye cover
NEW CONE
DTOP 191.9
DBOT 330.0
HEIG 122.0
ORI Z IS N AND Y IS U
POS E 13971.0 N 14946.1 U 324.1

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 202.0
HEIG 19.5
ORI Z IS N AND Y IS U
POS E 13971.0 N 14997.4 U 324.1

-- Reference Value: General process volute circumferentially distributed axial casing rib 1/3
NEW CYLI
DIAM 13.5
HEIG 177.8
ORI Z IS N AND Y IS U
POS E 13971.0 N 14754.4 U 494.9

-- Reference Value: General process volute circumferentially distributed axial casing rib 2/3
NEW CYLI
DIAM 13.5
HEIG 177.8
ORI Z IS N AND Y IS U
POS E 14118.9 N 14754.4 U 238.7

-- Reference Value: General process volute circumferentially distributed axial casing rib 3/3
NEW CYLI
DIAM 13.5
HEIG 177.8
ORI Z IS N AND Y IS U
POS E 13823.1 N 14754.4 U 238.7

NEW SUBE /203_PU_008_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 13798.0 N 14890.0 U 324.1

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 13798.0 N 14886.8 U 324.1

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 13798.0 N 14892.8 U 324.1

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 13821.2 N 14890.0 U 410.6

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 13821.2 N 14886.8 U 410.6

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 13821.2 N 14892.8 U 410.6

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 13884.5 N 14890.0 U 473.9

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 13884.5 N 14886.8 U 473.9

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 13884.5 N 14892.8 U 473.9

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 13971.0 N 14890.0 U 497.1

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 13971.0 N 14886.8 U 497.1

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 13971.0 N 14892.8 U 497.1

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 14057.5 N 14890.0 U 473.9

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 14057.5 N 14886.8 U 473.9

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 14057.5 N 14892.8 U 473.9

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 14120.8 N 14890.0 U 410.6

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 14120.8 N 14886.8 U 410.6

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 14120.8 N 14892.8 U 410.6

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 14144.0 N 14890.0 U 324.1

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 14144.0 N 14886.8 U 324.1

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 14144.0 N 14892.8 U 324.1

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 14120.8 N 14890.0 U 237.6

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 14120.8 N 14886.8 U 237.6

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 14120.8 N 14892.8 U 237.6

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 14057.5 N 14890.0 U 174.3

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 14057.5 N 14886.8 U 174.3

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 14057.5 N 14892.8 U 174.3

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 13971.0 N 14890.0 U 151.1

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 13971.0 N 14886.8 U 151.1

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 13971.0 N 14892.8 U 151.1

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 13884.5 N 14890.0 U 174.3

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 13884.5 N 14886.8 U 174.3

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 13884.5 N 14892.8 U 174.3

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.2
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 13821.2 N 14890.0 U 237.6

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 31.8
HEIG 3.3
ORI Z IS N AND Y IS U
POS E 13821.2 N 14886.8 U 237.6

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 8.8
ORI Z IS N AND Y IS U
POS E 13821.2 N 14892.8 U 237.6

NEW SUBE /203_PU_008_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 77.4
HEIG 64.1
ORI Z IS N AND Y IS U
POS E 13971.0 N 14347.1 U 324.1

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 89.2
HEIG 64.1
ORI Z IS N AND Y IS U
POS E 13971.0 N 14411.2 U 324.1

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 101.0
HEIG 64.1
ORI Z IS N AND Y IS U
POS E 13971.0 N 14475.3 U 324.1

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 112.8
HEIG 64.1
ORI Z IS N AND Y IS U
POS E 13971.0 N 14539.3 U 324.1

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 74.1
DBOT 107.7
HEIG 43.6
ORI Z IS N AND Y IS U
POS E 13971.0 N 14549.6 U 324.1

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 81.2
YLEN 179.4
ZLEN 153.8
POS E 13971.0 N 14456.0 U 190.8

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 13971.0 N 14458.6 U 390.5

NEW SUBE /203_PU_008_SUCTION
-- Reference Value: suction DN100; POS is flange face, contractual direction N
NEW NOZZLE /203_PU_008_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 13971.0 N 15257.1 U 324.1
ORI P1 IS N
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_008_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 13971.0 N 14789.2 U 496.1

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /203_PU_008_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 13971.0 N 14789.2 U 645.8
ORI P1 IS U
HEIG 153.4
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_008_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 31.5
HEIG 299.0
ORI Z IS N AND Y IS U
POS E 13971.0 N 14165.5 U 324.1

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 67.8
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 13971.0 N 14038.5 U 324.1

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 67.8
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 13971.0 N 14292.6 U 324.1

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 80.0
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 13971.0 N 14165.5 U 324.1

-- Reference Value: fabricated rectangular coupling guard
NEW BOX
XLEN 147.0
YLEN 299.0
ZLEN 124.6
POS E 13971.0 N 14165.5 U 324.1

-- Reference Value: boxed guard top reinforcing seam
NEW BOX
XLEN 8.8
YLEN 245.2
ZLEN 8.8
POS E 13971.0 N 14165.5 U 391.2

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 99.1
YLEN 35.9
ZLEN 130.3
POS E 13971.0 N 14069.8 U 179.1

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 99.1
YLEN 35.9
ZLEN 130.3
POS E 13971.0 N 14261.2 U 179.1

NEW SUBE /203_PU_008_DRIVER
-- Reference Value: Heavy-duty high-torque motor TEFC motor fan cowl
NEW CYLI
DIAM 354.4
HEIG 123.2
ORI Z IS N AND Y IS U
POS E 13971.0 N 13197.6 U 324.1

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 361.6
DBOT 325.4
HEIG 55.4
ORI Z IS N AND Y IS U
POS E 13971.0 N 13231.5 U 324.1

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile LARGE_PROCESS_PUMP_CORE
NEW CYLI
DIAM 361.6
HEIG 685.7
ORI Z IS N AND Y IS U
POS E 13971.0 N 13567.6 U 324.1

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 260.4
DBOT 361.6
HEIG 105.6
ORI Z IS N AND Y IS U
POS E 13971.0 N 13963.2 U 324.1

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 137.4
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 13971.0 N 14007.0 U 324.1

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 65.1
HEIG 12.2
ORI Z IS S AND Y IS U
POS E 13971.0 N 13142.1 U 324.1

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 244.0
YLEN 9.0
ZLEN 6.5
POS E 13971.0 N 13140.5 U 227.7

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 6.5
YLEN 9.0
ZLEN 244.0
POS E 14067.4 N 13140.5 U 324.1

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 295.7
YLEN 9.0
ZLEN 6.5
POS E 13971.0 N 13140.5 U 275.9

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 6.5
YLEN 9.0
ZLEN 295.7
POS E 14019.2 N 13140.5 U 324.1

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 311.0
YLEN 9.0
ZLEN 6.5
POS E 13971.0 N 13140.5 U 324.1

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 6.5
YLEN 9.0
ZLEN 311.0
POS E 13971.0 N 13140.5 U 324.1

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 295.7
YLEN 9.0
ZLEN 6.5
POS E 13971.0 N 13140.5 U 372.3

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 6.5
YLEN 9.0
ZLEN 295.7
POS E 13922.8 N 13140.5 U 324.1

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 244.0
YLEN 9.0
ZLEN 6.5
POS E 13971.0 N 13140.5 U 420.5

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 6.5
YLEN 9.0
ZLEN 244.0
POS E 13874.6 N 13140.5 U 324.1

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 122.7
YLEN 123.2
ZLEN 23.1
POS E 14158.4 N 13373.6 U 125.5

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 51.5
YLEN 96.1
ZLEN 71.0
POS E 14131.4 N 13373.6 U 172.5

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 122.7
YLEN 123.2
ZLEN 23.1
POS E 13783.6 N 13373.6 U 125.5

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 51.5
YLEN 96.1
ZLEN 71.0
POS E 13810.6 N 13373.6 U 172.5

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 122.7
YLEN 123.2
ZLEN 23.1
POS E 14158.4 N 13778.4 U 125.5

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 51.5
YLEN 96.1
ZLEN 71.0
POS E 14131.4 N 13778.4 U 172.5

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 122.7
YLEN 123.2
ZLEN 23.1
POS E 13783.6 N 13778.4 U 125.5

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 51.5
YLEN 96.1
ZLEN 71.0
POS E 13810.6 N 13778.4 U 172.5

-- Reference Value: 360-degree motor cooling rib 1/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13971.0 N 13567.6 U 509.3

-- Reference Value: 360-degree motor cooling rib 2/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 14034.3 N 13567.6 U 498.1

-- Reference Value: 360-degree motor cooling rib 3/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 14090.0 N 13567.6 U 466.0

-- Reference Value: 360-degree motor cooling rib 4/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 14131.4 N 13567.6 U 416.7

-- Reference Value: 360-degree motor cooling rib 5/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 14153.4 N 13567.6 U 356.3

-- Reference Value: 360-degree motor cooling rib 6/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 14153.4 N 13567.6 U 292.0

-- Reference Value: 360-degree motor cooling rib 7/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 14131.4 N 13567.6 U 231.5

-- Reference Value: 360-degree motor cooling rib 8/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 14090.0 N 13567.6 U 182.3

-- Reference Value: 360-degree motor cooling rib 9/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 14034.3 N 13567.6 U 150.1

-- Reference Value: 360-degree motor cooling rib 10/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13971.0 N 13567.6 U 139.0

-- Reference Value: 360-degree motor cooling rib 11/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13907.7 N 13567.6 U 150.1

-- Reference Value: 360-degree motor cooling rib 12/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13852.0 N 13567.6 U 182.3

-- Reference Value: 360-degree motor cooling rib 13/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13810.6 N 13567.6 U 231.5

-- Reference Value: 360-degree motor cooling rib 14/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13788.6 N 13567.6 U 292.0

-- Reference Value: 360-degree motor cooling rib 15/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13788.6 N 13567.6 U 356.3

-- Reference Value: 360-degree motor cooling rib 16/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13810.6 N 13567.6 U 416.7

-- Reference Value: 360-degree motor cooling rib 17/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13852.0 N 13567.6 U 466.0

-- Reference Value: 360-degree motor cooling rib 18/18
NEW CYLI
DIAM 19.9
HEIG 603.4
ORI Z IS N AND Y IS U
POS E 13907.7 N 13567.6 U 498.1

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 1/2
NEW CYLI
DIAM 381.5
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 13971.0 N 13453.3 U 324.1

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 2/2
NEW CYLI
DIAM 381.5
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 13971.0 N 13681.8 U 324.1

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 235.2
YLEN 246.4
ZLEN 96.7
POS E 13971.0 N 13540.8 U 567.6

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 244.6
YLEN 256.3
ZLEN 11.6
POS E 13971.0 N 13540.8 U 621.8

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.6
HEIG 6.4
ORI Z IS U AND Y IS N
POS E 14055.7 N 13447.2 U 630.8

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.6
HEIG 6.4
ORI Z IS U AND Y IS N
POS E 13886.3 N 13447.2 U 630.8

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.6
HEIG 6.4
ORI Z IS U AND Y IS N
POS E 14055.7 N 13634.4 U 630.8

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 13.6
HEIG 6.4
ORI Z IS U AND Y IS N
POS E 13886.3 N 13634.4 U 630.8

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 28.7
HEIG 11.7
ORI Z IS W AND Y IS U
POS E 13847.6 N 13540.8 U 562.8

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 21.3
HEIG 13.8
ORI Z IS W AND Y IS U
POS E 13834.8 N 13540.8 U 562.8

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 17.9
YLEN 78.9
ZLEN 58.0
POS E 13971.0 N 13734.4 U 533.9

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 24.2
HEIG 30.4
ORI Z IS W AND Y IS U
POS E 13971.0 N 13734.4 U 550.2

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 9.0
YLEN 140.8
ZLEN 50.5
POS E 14153.8 N 13628.8 U 345.8

NEW SUBE /203_PU_008_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.9
HEIG 24.2
ORI Z IS U AND Y IS N
POS E 14175.5 N 13373.6 U 149.1

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 38.5
HEIG 3.9
ORI Z IS U AND Y IS N
POS E 14175.5 N 13373.6 U 139.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 30.8
HEIG 11.1
ORI Z IS U AND Y IS N
POS E 14175.5 N 13373.6 U 166.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.9
HEIG 24.2
ORI Z IS U AND Y IS N
POS E 13766.5 N 13373.6 U 149.1

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 38.5
HEIG 3.9
ORI Z IS U AND Y IS N
POS E 13766.5 N 13373.6 U 139.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 30.8
HEIG 11.1
ORI Z IS U AND Y IS N
POS E 13766.5 N 13373.6 U 166.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.9
HEIG 24.2
ORI Z IS U AND Y IS N
POS E 14175.5 N 13778.4 U 149.1

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 38.5
HEIG 3.9
ORI Z IS U AND Y IS N
POS E 14175.5 N 13778.4 U 139.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 30.8
HEIG 11.1
ORI Z IS U AND Y IS N
POS E 14175.5 N 13778.4 U 166.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 17.9
HEIG 24.2
ORI Z IS U AND Y IS N
POS E 13766.5 N 13778.4 U 149.1

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 38.5
HEIG 3.9
ORI Z IS U AND Y IS N
POS E 13766.5 N 13778.4 U 139.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 30.8
HEIG 11.1
ORI Z IS U AND Y IS N
POS E 13766.5 N 13778.4 U 166.7

NEW SUBE /203_PU_008_SERVICE_DETAILS
-- Reference Value: dilution-pump vent/flush boss
NEW CYLI
DIAM 22.0
HEIG 17.6
ORI Z IS U AND Y IS N
POS E 13910.4 N 14754.4 U 474.3


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 163 primitives.
