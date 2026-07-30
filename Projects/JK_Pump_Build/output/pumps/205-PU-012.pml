-- ====================================================================
-- 205-PU-012 - D0 STAGE DILUTION PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 205-PU-012
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /205_PU_012
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_012_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 1245.0
YLEN 2701.0
ZLEN 50.0
POS E 33065.0 N 13825.0 U 25.0

NEW SUBE /205_PU_012_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 24.0
HEIG 32.4
ORI Z IS U AND Y IS N
POS E 33606.6 N 12623.1 U 54.0

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 51.6
HEIG 5.3
ORI Z IS U AND Y IS N
POS E 33606.6 N 12623.1 U 52.6

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 41.3
HEIG 14.9
ORI Z IS U AND Y IS N
POS E 33606.6 N 12623.1 U 62.7

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 24.0
HEIG 32.4
ORI Z IS U AND Y IS N
POS E 32523.4 N 12623.1 U 54.0

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 51.6
HEIG 5.3
ORI Z IS U AND Y IS N
POS E 32523.4 N 12623.1 U 52.6

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 41.3
HEIG 14.9
ORI Z IS U AND Y IS N
POS E 32523.4 N 12623.1 U 62.7

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 24.0
HEIG 32.4
ORI Z IS U AND Y IS N
POS E 33606.6 N 15026.9 U 54.0

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 51.6
HEIG 5.3
ORI Z IS U AND Y IS N
POS E 33606.6 N 15026.9 U 52.6

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 41.3
HEIG 14.9
ORI Z IS U AND Y IS N
POS E 33606.6 N 15026.9 U 62.7

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 24.0
HEIG 32.4
ORI Z IS U AND Y IS N
POS E 32523.4 N 15026.9 U 54.0

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 51.6
HEIG 5.3
ORI Z IS U AND Y IS N
POS E 32523.4 N 15026.9 U 52.6

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 41.3
HEIG 14.9
ORI Z IS U AND Y IS N
POS E 32523.4 N 15026.9 U 62.7

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 24.0
HEIG 32.4
ORI Z IS U AND Y IS N
POS E 33606.6 N 13825.0 U 54.0

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 51.6
HEIG 5.3
ORI Z IS U AND Y IS N
POS E 33606.6 N 13825.0 U 52.6

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 41.3
HEIG 14.9
ORI Z IS U AND Y IS N
POS E 33606.6 N 13825.0 U 62.7

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 24.0
HEIG 32.4
ORI Z IS U AND Y IS N
POS E 32523.4 N 13825.0 U 54.0

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 51.6
HEIG 5.3
ORI Z IS U AND Y IS N
POS E 32523.4 N 13825.0 U 52.6

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 41.3
HEIG 14.9
ORI Z IS U AND Y IS N
POS E 32523.4 N 13825.0 U 62.7

-- Reference Value: baseplate anchor fastener A7: exposed threaded shank Reference Value
NEW CYLI
DIAM 24.0
HEIG 32.4
ORI Z IS U AND Y IS N
POS E 33065.0 N 12623.1 U 54.0

-- Reference Value: baseplate anchor fastener A7: solid washer under filled shank Reference Value
NEW CYLI
DIAM 51.6
HEIG 5.3
ORI Z IS U AND Y IS N
POS E 33065.0 N 12623.1 U 52.6

-- Reference Value: baseplate anchor fastener A7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 41.3
HEIG 14.9
ORI Z IS U AND Y IS N
POS E 33065.0 N 12623.1 U 62.7

-- Reference Value: baseplate anchor fastener A8: exposed threaded shank Reference Value
NEW CYLI
DIAM 24.0
HEIG 32.4
ORI Z IS U AND Y IS N
POS E 33065.0 N 15026.9 U 54.0

-- Reference Value: baseplate anchor fastener A8: solid washer under filled shank Reference Value
NEW CYLI
DIAM 51.6
HEIG 5.3
ORI Z IS U AND Y IS N
POS E 33065.0 N 15026.9 U 52.6

-- Reference Value: baseplate anchor fastener A8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 41.3
HEIG 14.9
ORI Z IS U AND Y IS N
POS E 33065.0 N 15026.9 U 62.7

NEW SUBE /205_PU_012_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 99.6
YLEN 2214.8
ZLEN 90.0
POS E 33363.8 N 13771.0 U 95.0

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 99.6
YLEN 2214.8
ZLEN 90.0
POS E 32766.2 N 13771.0 U 95.0

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 896.4
YLEN 71.7
ZLEN 61.2
POS E 33065.0 N 12906.7 U 80.6

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 896.4
YLEN 71.7
ZLEN 61.2
POS E 33065.0 N 13518.9 U 80.6

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 896.4
YLEN 71.7
ZLEN 61.2
POS E 33065.0 N 14131.1 U 80.6

-- Reference Value: skid cross-member 4
NEW BOX
XLEN 896.4
YLEN 71.7
ZLEN 61.2
POS E 33065.0 N 14743.3 U 80.6

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 161.8
YLEN 202.6
ZLEN 144.5
POS E 33289.1 N 14567.1 U 122.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 161.8
YLEN 202.6
ZLEN 144.5
POS E 32840.9 N 14567.1 U 122.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 161.8
YLEN 202.6
ZLEN 144.5
POS E 33289.1 N 14859.2 U 122.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 161.8
YLEN 202.6
ZLEN 144.5
POS E 32840.9 N 14859.2 U 122.3

NEW SUBE /205_PU_012_CASING
-- Reference Value: General process volute back-pull-out rear plate
NEW CYLI
DIAM 449.6
HEIG 68.7
ORI Z IS N AND Y IS U
POS E 33065.0 N 14469.8 U 450.0

-- Reference Value: General process volute radially split casing envelope
NEW CYLI
DIAM 510.9
HEIG 343.6
ORI Z IS N AND Y IS U
POS E 33065.0 N 14675.9 U 450.0

-- Reference Value: casing split flange
NEW CYLI
DIAM 549.3
HEIG 20.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 14837.7 U 450.0

-- Reference Value: General process volute tapered impeller-eye cover
NEW CONE
DTOP 291.2
DBOT 500.7
HEIG 160.3
ORI Z IS N AND Y IS U
POS E 33065.0 N 14927.9 U 450.0

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 306.6
HEIG 22.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 14997.0 U 450.0

-- Reference Value: General process volute circumferentially distributed axial casing rib 1/4
NEW CYLI
DIAM 20.4
HEIG 233.6
ORI Z IS N AND Y IS U
POS E 33065.0 N 14675.9 U 709.2

-- Reference Value: General process volute circumferentially distributed axial casing rib 2/4
NEW CYLI
DIAM 20.4
HEIG 233.6
ORI Z IS N AND Y IS U
POS E 33324.2 N 14675.9 U 450.0

-- Reference Value: General process volute circumferentially distributed axial casing rib 3/4
NEW CYLI
DIAM 20.4
HEIG 233.6
ORI Z IS N AND Y IS U
POS E 33065.0 N 14675.9 U 190.8

-- Reference Value: General process volute circumferentially distributed axial casing rib 4/4
NEW CYLI
DIAM 20.4
HEIG 233.6
ORI Z IS N AND Y IS U
POS E 32805.8 N 14675.9 U 450.0

NEW SUBE /205_PU_012_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 32802.5 N 14855.2 U 450.0

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 32802.5 N 14850.2 U 450.0

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 32802.5 N 14859.4 U 450.0

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 32822.5 N 14855.2 U 550.5

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 32822.5 N 14850.2 U 550.5

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 32822.5 N 14859.4 U 550.5

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 32879.4 N 14855.2 U 635.6

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 32879.4 N 14850.2 U 635.6

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 32879.4 N 14859.4 U 635.6

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 32964.5 N 14855.2 U 692.5

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 32964.5 N 14850.2 U 692.5

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 32964.5 N 14859.4 U 692.5

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 33065.0 N 14855.2 U 712.5

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 33065.0 N 14850.2 U 712.5

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 33065.0 N 14859.4 U 712.5

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 33165.5 N 14855.2 U 692.5

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 33165.5 N 14850.2 U 692.5

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 33165.5 N 14859.4 U 692.5

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 33250.6 N 14855.2 U 635.6

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 33250.6 N 14850.2 U 635.6

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 33250.6 N 14859.4 U 635.6

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 33307.5 N 14855.2 U 550.5

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 33307.5 N 14850.2 U 550.5

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 33307.5 N 14859.4 U 550.5

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 33327.5 N 14855.2 U 450.0

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 33327.5 N 14850.2 U 450.0

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 33327.5 N 14859.4 U 450.0

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 33307.5 N 14855.2 U 349.5

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 33307.5 N 14850.2 U 349.5

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 33307.5 N 14859.4 U 349.5

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 33250.6 N 14855.2 U 264.4

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 33250.6 N 14850.2 U 264.4

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 33250.6 N 14859.4 U 264.4

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 33165.5 N 14855.2 U 207.5

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 33165.5 N 14850.2 U 207.5

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 33165.5 N 14859.4 U 207.5

-- Reference Value: casing split-line bolt C13: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 33065.0 N 14855.2 U 187.5

-- Reference Value: casing split-line bolt C13: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 33065.0 N 14850.2 U 187.5

-- Reference Value: casing split-line bolt C13: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 33065.0 N 14859.4 U 187.5

-- Reference Value: casing split-line bolt C14: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 32964.5 N 14855.2 U 207.5

-- Reference Value: casing split-line bolt C14: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 32964.5 N 14850.2 U 207.5

-- Reference Value: casing split-line bolt C14: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 32964.5 N 14859.4 U 207.5

-- Reference Value: casing split-line bolt C15: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 32879.4 N 14855.2 U 264.4

-- Reference Value: casing split-line bolt C15: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 32879.4 N 14850.2 U 264.4

-- Reference Value: casing split-line bolt C15: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 32879.4 N 14859.4 U 264.4

-- Reference Value: casing split-line bolt C16: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.0
HEIG 21.8
ORI Z IS N AND Y IS U
POS E 32822.5 N 14855.2 U 349.5

-- Reference Value: casing split-line bolt C16: flange-face washer Reference Value
NEW CYLI
DIAM 48.3
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 32822.5 N 14850.2 U 349.5

-- Reference Value: casing split-line bolt C16: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.5
HEIG 13.3
ORI Z IS N AND Y IS U
POS E 32822.5 N 14859.4 U 349.5

NEW SUBE /205_PU_012_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 117.5
HEIG 64.8
ORI Z IS N AND Y IS U
POS E 33065.0 N 14143.7 U 450.0

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 135.4
HEIG 64.8
ORI Z IS N AND Y IS U
POS E 33065.0 N 14208.5 U 450.0

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 153.3
HEIG 64.8
ORI Z IS N AND Y IS U
POS E 33065.0 N 14273.4 U 450.0

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 171.2
HEIG 64.8
ORI Z IS N AND Y IS U
POS E 33065.0 N 14338.2 U 450.0

-- Reference Value: stepped bearing bracket section 5
NEW CYLI
DIAM 189.1
HEIG 64.8
ORI Z IS N AND Y IS U
POS E 33065.0 N 14403.0 U 450.0

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 112.4
DBOT 163.5
HEIG 55.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 14407.9 U 450.0

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 136.1
YLEN 226.9
ZLEN 215.5
POS E 33065.0 N 14289.6 U 247.7

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 22.7
HEIG 20.4
ORI Z IS U AND Y IS N
POS E 33065.0 N 14292.8 U 554.7

NEW SUBE /205_PU_012_SUCTION
-- Reference Value: suction DN150; POS is flange face, contractual direction N
NEW NOZZLE /205_PU_012_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 33065.0 N 15258.0 U 450.0
ORI P1 IS N
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_012_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 135.0
HEIG 28.0
ORI Z IS U AND Y IS N
POS E 33065.0 N 14721.7 U 709.7

-- Reference Value: discharge DN100; POS is flange face, contractual direction U
NEW NOZZLE /205_PU_012_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 33065.0 N 14721.7 U 929.6
ORI P1 IS U
HEIG 224.1
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_012_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 36.0
HEIG 378.1
ORI Z IS N AND Y IS U
POS E 33065.0 N 13922.2 U 450.0

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 77.4
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 13755.7 U 450.0

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 77.4
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 14088.8 U 450.0

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 91.3
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 13922.2 U 450.0

-- Reference Value: fabricated rectangular coupling guard
NEW BOX
XLEN 202.4
YLEN 378.1
ZLEN 171.6
POS E 33065.0 N 13922.2 U 450.0

-- Reference Value: boxed guard top reinforcing seam
NEW BOX
XLEN 12.1
YLEN 310.1
ZLEN 12.1
POS E 33065.0 N 13922.2 U 542.4

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 136.4
YLEN 45.4
ZLEN 200.0
POS E 33065.0 N 13801.2 U 240.0

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 136.4
YLEN 45.4
ZLEN 200.0
POS E 33065.0 N 14043.2 U 240.0

NEW SUBE /205_PU_012_DRIVER
-- Reference Value: Heavy-duty high-torque motor TEFC motor fan cowl
NEW CYLI
DIAM 522.5
HEIG 163.4
ORI Z IS N AND Y IS U
POS E 33065.0 N 12648.0 U 450.0

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 533.2
DBOT 479.9
HEIG 73.5
ORI Z IS N AND Y IS U
POS E 33065.0 N 12692.9 U 450.0

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile D0_DILUTION_XL
NEW CYLI
DIAM 533.2
HEIG 909.2
ORI Z IS N AND Y IS U
POS E 33065.0 N 13138.5 U 450.0

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 383.9
DBOT 533.2
HEIG 140.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 13663.2 U 450.0

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 202.6
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 13724.2 U 450.0

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 96.0
HEIG 16.2
ORI Z IS S AND Y IS U
POS E 33065.0 N 12574.4 U 450.0

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 359.8
YLEN 12.0
ZLEN 9.0
POS E 33065.0 N 12572.3 U 307.8

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 9.0
YLEN 12.0
ZLEN 359.8
POS E 33207.2 N 12572.3 U 450.0

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 436.0
YLEN 12.0
ZLEN 9.0
POS E 33065.0 N 12572.3 U 378.9

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 9.0
YLEN 12.0
ZLEN 436.0
POS E 33136.1 N 12572.3 U 450.0

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 458.6
YLEN 12.0
ZLEN 9.0
POS E 33065.0 N 12572.3 U 450.0

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 9.0
YLEN 12.0
ZLEN 458.6
POS E 33065.0 N 12572.3 U 450.0

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 436.0
YLEN 12.0
ZLEN 9.0
POS E 33065.0 N 12572.3 U 521.1

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 9.0
YLEN 12.0
ZLEN 436.0
POS E 32993.9 N 12572.3 U 450.0

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 359.8
YLEN 12.0
ZLEN 9.0
POS E 33065.0 N 12572.3 U 592.2

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 9.0
YLEN 12.0
ZLEN 359.8
POS E 32922.8 N 12572.3 U 450.0

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 179.3
YLEN 163.4
ZLEN 28.0
POS E 33338.9 N 12881.4 U 154.0

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 75.3
YLEN 127.4
ZLEN 108.8
POS E 33299.5 N 12881.4 U 222.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 179.3
YLEN 163.4
ZLEN 28.0
POS E 32791.1 N 12881.4 U 154.0

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 75.3
YLEN 127.4
ZLEN 108.8
POS E 32830.5 N 12881.4 U 222.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 179.3
YLEN 163.4
ZLEN 28.0
POS E 33338.9 N 13418.1 U 154.0

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 75.3
YLEN 127.4
ZLEN 108.8
POS E 33299.5 N 13418.1 U 222.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 179.3
YLEN 163.4
ZLEN 28.0
POS E 32791.1 N 13418.1 U 154.0

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 75.3
YLEN 127.4
ZLEN 108.8
POS E 32830.5 N 13418.1 U 222.4

-- Reference Value: 360-degree motor cooling rib 1/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33065.0 N 13138.5 U 722.3

-- Reference Value: 360-degree motor cooling rib 2/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33141.7 N 13138.5 U 711.3

-- Reference Value: 360-degree motor cooling rib 3/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33212.2 N 13138.5 U 679.1

-- Reference Value: 360-degree motor cooling rib 4/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33270.8 N 13138.5 U 628.3

-- Reference Value: 360-degree motor cooling rib 5/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33312.7 N 13138.5 U 563.1

-- Reference Value: 360-degree motor cooling rib 6/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33334.5 N 13138.5 U 488.8

-- Reference Value: 360-degree motor cooling rib 7/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33334.5 N 13138.5 U 411.2

-- Reference Value: 360-degree motor cooling rib 8/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33312.7 N 13138.5 U 336.9

-- Reference Value: 360-degree motor cooling rib 9/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33270.8 N 13138.5 U 271.7

-- Reference Value: 360-degree motor cooling rib 10/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33212.2 N 13138.5 U 220.9

-- Reference Value: 360-degree motor cooling rib 11/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33141.7 N 13138.5 U 188.7

-- Reference Value: 360-degree motor cooling rib 12/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 33065.0 N 13138.5 U 177.7

-- Reference Value: 360-degree motor cooling rib 13/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32988.3 N 13138.5 U 188.7

-- Reference Value: 360-degree motor cooling rib 14/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32917.8 N 13138.5 U 220.9

-- Reference Value: 360-degree motor cooling rib 15/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32859.2 N 13138.5 U 271.7

-- Reference Value: 360-degree motor cooling rib 16/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32817.3 N 13138.5 U 336.9

-- Reference Value: 360-degree motor cooling rib 17/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32795.5 N 13138.5 U 411.2

-- Reference Value: 360-degree motor cooling rib 18/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32795.5 N 13138.5 U 488.8

-- Reference Value: 360-degree motor cooling rib 19/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32817.3 N 13138.5 U 563.1

-- Reference Value: 360-degree motor cooling rib 20/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32859.2 N 13138.5 U 628.3

-- Reference Value: 360-degree motor cooling rib 21/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32917.8 N 13138.5 U 679.1

-- Reference Value: 360-degree motor cooling rib 22/22
NEW CYLI
DIAM 26.0
HEIG 800.1
ORI Z IS N AND Y IS U
POS E 32988.3 N 13138.5 U 711.3

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 1/2
NEW CYLI
DIAM 562.5
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 12987.0 U 450.0

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 2/2
NEW CYLI
DIAM 562.5
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 13290.1 U 450.0

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 343.6
YLEN 326.7
ZLEN 142.6
POS E 33065.0 N 13103.1 U 806.6

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 357.4
YLEN 339.8
ZLEN 12.0
POS E 33065.0 N 13103.1 U 883.9

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.5
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 33188.7 N 12978.9 U 893.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.5
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 32941.3 N 12978.9 U 893.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.5
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 33188.7 N 13227.2 U 893.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.5
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 32941.3 N 13227.2 U 893.2

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 32.4
HEIG 13.2
ORI Z IS W AND Y IS U
POS E 32886.6 N 13103.1 U 799.5

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 24.0
HEIG 15.6
ORI Z IS W AND Y IS U
POS E 32872.2 N 13103.1 U 799.5

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 22.0
YLEN 104.5
ZLEN 58.0
POS E 33065.0 N 13359.8 U 745.6

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 29.7
HEIG 37.4
ORI Z IS W AND Y IS U
POS E 33065.0 N 13359.8 U 761.8

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 9.0
YLEN 186.7
ZLEN 74.4
POS E 33333.6 N 13219.8 U 482.0

NEW SUBE /205_PU_012_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 33363.8 N 12881.4 U 181.5

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 33363.8 N 12881.4 U 170.2

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 33363.8 N 12881.4 U 201.2

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 32766.2 N 12881.4 U 181.5

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 32766.2 N 12881.4 U 170.2

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 32766.2 N 12881.4 U 201.2

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 33363.8 N 13418.1 U 181.5

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 33363.8 N 13418.1 U 170.2

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 33363.8 N 13418.1 U 201.2

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 32766.2 N 13418.1 U 181.5

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 32766.2 N 13418.1 U 170.2

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 32766.2 N 13418.1 U 201.2

NEW SUBE /205_PU_012_SERVICE_DETAILS
-- Reference Value: dilution-pump vent/flush boss
NEW CYLI
DIAM 26.0
HEIG 20.8
ORI Z IS U AND Y IS N
POS E 32973.0 N 14675.9 U 675.0


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 181 primitives.
