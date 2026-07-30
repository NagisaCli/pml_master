-- ====================================================================
-- 205-PU-054 - D1 STAGE MC PUMP (205-PU-054/MC PUMP)
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 205-PU-054
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:29

NEW EQUI /205_PU_054
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_054_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 1046.0
YLEN 2000.0
ZLEN 50.0
POS E 48852.0 N 4714.0 U 25.0

NEW SUBE /205_PU_054_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.9
HEIG 28.2
ORI Z IS U AND Y IS N
POS E 49307.0 N 3824.0 U 53.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.0
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 49307.0 N 3824.0 U 52.3

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.0
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 49307.0 N 3824.0 U 61.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.9
HEIG 28.2
ORI Z IS U AND Y IS N
POS E 48397.0 N 3824.0 U 53.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.0
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 48397.0 N 3824.0 U 52.3

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.0
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 48397.0 N 3824.0 U 61.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.9
HEIG 28.2
ORI Z IS U AND Y IS N
POS E 49307.0 N 5604.0 U 53.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.0
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 49307.0 N 5604.0 U 52.3

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.0
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 49307.0 N 5604.0 U 61.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.9
HEIG 28.2
ORI Z IS U AND Y IS N
POS E 48397.0 N 5604.0 U 53.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.0
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 48397.0 N 5604.0 U 52.3

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.0
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 48397.0 N 5604.0 U 61.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.9
HEIG 28.2
ORI Z IS U AND Y IS N
POS E 49307.0 N 4714.0 U 53.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.0
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 49307.0 N 4714.0 U 52.3

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.0
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 49307.0 N 4714.0 U 61.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.9
HEIG 28.2
ORI Z IS U AND Y IS N
POS E 48397.0 N 4714.0 U 53.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.0
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 48397.0 N 4714.0 U 52.3

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.0
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 48397.0 N 4714.0 U 61.1

-- Reference Value: baseplate anchor fastener A7: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.9
HEIG 28.2
ORI Z IS U AND Y IS N
POS E 48852.0 N 3824.0 U 53.5

-- Reference Value: baseplate anchor fastener A7: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.0
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 48852.0 N 3824.0 U 52.3

-- Reference Value: baseplate anchor fastener A7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.0
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 48852.0 N 3824.0 U 61.1

-- Reference Value: baseplate anchor fastener A8: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.9
HEIG 28.2
ORI Z IS U AND Y IS N
POS E 48852.0 N 5604.0 U 53.5

-- Reference Value: baseplate anchor fastener A8: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.0
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 48852.0 N 5604.0 U 52.3

-- Reference Value: baseplate anchor fastener A8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.0
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 48852.0 N 5604.0 U 61.1

NEW SUBE /205_PU_054_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 83.7
YLEN 1640.0
ZLEN 78.5
POS E 49103.0 N 4674.0 U 89.2

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 83.7
YLEN 1640.0
ZLEN 78.5
POS E 48601.0 N 4674.0 U 89.2

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 753.1
YLEN 60.2
ZLEN 53.3
POS E 48852.0 N 4034.0 U 76.7

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 753.1
YLEN 60.2
ZLEN 53.3
POS E 48852.0 N 4487.3 U 76.7

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 753.1
YLEN 60.2
ZLEN 53.3
POS E 48852.0 N 4940.7 U 76.7

-- Reference Value: skid cross-member 4
NEW BOX
XLEN 753.1
YLEN 60.2
ZLEN 53.3
POS E 48852.0 N 5394.0 U 76.7

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 136.0
YLEN 150.0
ZLEN 83.3
POS E 49040.3 N 4986.4 U 91.6

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 136.0
YLEN 150.0
ZLEN 83.3
POS E 48663.7 N 4986.4 U 91.6

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 136.0
YLEN 150.0
ZLEN 83.3
POS E 49040.3 N 5310.8 U 91.6

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 136.0
YLEN 150.0
ZLEN 83.3
POS E 48663.7 N 5310.8 U 91.6

NEW SUBE /205_PU_054_CASING
-- Reference Value: Medium-consistency fluidizer volute back-pull-out rear plate
NEW CYLI
DIAM 457.3
HEIG 76.3
ORI Z IS N AND Y IS U
POS E 48852.0 N 4878.3 U 393.1

-- Reference Value: Medium-consistency fluidizer volute radially split casing envelope
NEW CYLI
DIAM 519.7
HEIG 368.9
ORI Z IS N AND Y IS U
POS E 48852.0 N 5100.9 U 393.1

-- Reference Value: casing split flange
NEW CYLI
DIAM 571.6
HEIG 20.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 5275.4 U 393.1

-- Reference Value: Medium-consistency fluidizer volute tapered impeller-eye cover
NEW CONE
DTOP 249.4
DBOT 509.3
HEIG 190.8
ORI Z IS N AND Y IS U
POS E 48852.0 N 5380.8 U 393.1

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 270.2
HEIG 22.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 5465.2 U 393.1

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 1/6
NEW CYLI
DIAM 20.8
HEIG 250.8
ORI Z IS N AND Y IS U
POS E 48852.0 N 5100.9 U 656.7

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 2/6
NEW CYLI
DIAM 20.8
HEIG 250.8
ORI Z IS N AND Y IS U
POS E 49080.3 N 5100.9 U 524.9

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 3/6
NEW CYLI
DIAM 20.8
HEIG 250.8
ORI Z IS N AND Y IS U
POS E 49080.3 N 5100.9 U 261.3

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 4/6
NEW CYLI
DIAM 20.8
HEIG 250.8
ORI Z IS N AND Y IS U
POS E 48852.0 N 5100.9 U 129.5

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 5/6
NEW CYLI
DIAM 20.8
HEIG 250.8
ORI Z IS N AND Y IS U
POS E 48623.7 N 5100.9 U 261.3

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 6/6
NEW CYLI
DIAM 20.8
HEIG 250.8
ORI Z IS N AND Y IS U
POS E 48623.7 N 5100.9 U 524.9

-- Reference Value: MC fluidizer nose sleeve
NEW CYLI
DIAM 228.6
HEIG 42.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 5455.2 U 393.1

NEW SUBE /205_PU_054_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48581.8 N 5293.0 U 393.1

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48581.8 N 5287.9 U 393.1

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48581.8 N 5297.3 U 393.1

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48602.3 N 5293.0 U 496.5

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48602.3 N 5287.9 U 496.5

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48602.3 N 5297.3 U 496.5

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48660.9 N 5293.0 U 584.2

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48660.9 N 5287.9 U 584.2

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48660.9 N 5297.3 U 584.2

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48748.6 N 5293.0 U 642.7

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48748.6 N 5287.9 U 642.7

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48748.6 N 5297.3 U 642.7

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48852.0 N 5293.0 U 663.3

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48852.0 N 5287.9 U 663.3

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48852.0 N 5297.3 U 663.3

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48955.4 N 5293.0 U 642.7

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48955.4 N 5287.9 U 642.7

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48955.4 N 5297.3 U 642.7

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 49043.1 N 5293.0 U 584.2

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 49043.1 N 5287.9 U 584.2

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 49043.1 N 5297.3 U 584.2

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 49101.7 N 5293.0 U 496.5

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 49101.7 N 5287.9 U 496.5

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 49101.7 N 5297.3 U 496.5

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 49122.2 N 5293.0 U 393.1

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 49122.2 N 5287.9 U 393.1

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 49122.2 N 5297.3 U 393.1

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 49101.7 N 5293.0 U 289.7

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 49101.7 N 5287.9 U 289.7

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 49101.7 N 5297.3 U 289.7

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 49043.1 N 5293.0 U 202.0

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 49043.1 N 5287.9 U 202.0

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 49043.1 N 5297.3 U 202.0

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48955.4 N 5293.0 U 143.4

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48955.4 N 5287.9 U 143.4

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48955.4 N 5297.3 U 143.4

-- Reference Value: casing split-line bolt C13: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48852.0 N 5293.0 U 122.9

-- Reference Value: casing split-line bolt C13: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48852.0 N 5287.9 U 122.9

-- Reference Value: casing split-line bolt C13: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48852.0 N 5297.3 U 122.9

-- Reference Value: casing split-line bolt C14: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48748.6 N 5293.0 U 143.4

-- Reference Value: casing split-line bolt C14: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48748.6 N 5287.9 U 143.4

-- Reference Value: casing split-line bolt C14: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48748.6 N 5297.3 U 143.4

-- Reference Value: casing split-line bolt C15: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48660.9 N 5293.0 U 202.0

-- Reference Value: casing split-line bolt C15: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48660.9 N 5287.9 U 202.0

-- Reference Value: casing split-line bolt C15: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48660.9 N 5297.3 U 202.0

-- Reference Value: casing split-line bolt C16: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.4
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 48602.3 N 5293.0 U 289.7

-- Reference Value: casing split-line bolt C16: flange-face washer Reference Value
NEW CYLI
DIAM 49.1
HEIG 5.1
ORI Z IS N AND Y IS U
POS E 48602.3 N 5287.9 U 289.7

-- Reference Value: casing split-line bolt C16: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.2
HEIG 13.6
ORI Z IS N AND Y IS U
POS E 48602.3 N 5297.3 U 289.7

NEW SUBE /205_PU_054_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 119.5
HEIG 30.3
ORI Z IS N AND Y IS U
POS E 48852.0 N 4703.7 U 393.1

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 137.7
HEIG 30.3
ORI Z IS N AND Y IS U
POS E 48852.0 N 4734.0 U 393.1

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 155.9
HEIG 30.3
ORI Z IS N AND Y IS U
POS E 48852.0 N 4764.3 U 393.1

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 174.1
HEIG 30.3
ORI Z IS N AND Y IS U
POS E 48852.0 N 4794.7 U 393.1

-- Reference Value: stepped bearing bracket section 5
NEW CYLI
DIAM 192.3
HEIG 30.3
ORI Z IS N AND Y IS U
POS E 48852.0 N 4825.0 U 393.1

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 114.3
DBOT 166.3
HEIG 55.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 4812.7 U 393.1

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 138.4
YLEN 106.2
ZLEN 168.5
POS E 48852.0 N 4771.9 U 212.7

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 23.1
HEIG 20.8
ORI Z IS U AND Y IS N
POS E 48852.0 N 4773.4 U 499.6

NEW SUBE /205_PU_054_SUCTION
-- Reference Value: suction DN200; POS is flange face, contractual direction N
NEW NOZZLE /205_PU_054_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 48852.0 N 5756.2 U 393.1
ORI P1 IS N
HEIG 280.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_054_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 202.5
HEIG 42.0
ORI Z IS U AND Y IS N
POS E 48852.0 N 5158.2 U 659.2

-- Reference Value: discharge DN150; POS is flange face, contractual direction U
NEW NOZZLE /205_PU_054_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 48852.0 N 5158.2 U 841.2
ORI P1 IS U
HEIG 188.3
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_054_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 36.0
HEIG 140.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 4618.5 U 393.1

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 77.4
HEIG 35.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 4566.0 U 393.1

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 77.4
HEIG 35.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 4671.0 U 393.1

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 91.3
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 4618.5 U 393.1

-- Reference Value: fabricated rectangular coupling guard
NEW BOX
XLEN 185.0
YLEN 140.0
ZLEN 156.9
POS E 48852.0 N 4618.5 U 393.1

-- Reference Value: boxed guard top reinforcing seam
NEW BOX
XLEN 11.1
YLEN 114.8
ZLEN 11.1
POS E 48852.0 N 4618.5 U 477.6

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 124.7
YLEN 24.0
ZLEN 164.1
POS E 48852.0 N 4573.7 U 210.5

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 124.7
YLEN 24.0
ZLEN 164.1
POS E 48852.0 N 4663.3 U 210.5

NEW SUBE /205_PU_054_DRIVER
-- Reference Value: MC-pump main drive TEFC motor fan cowl
NEW CYLI
DIAM 413.9
HEIG 112.3
ORI Z IS N AND Y IS U
POS E 48852.0 N 3855.7 U 393.1

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 449.9
DBOT 404.9
HEIG 50.6
ORI Z IS N AND Y IS U
POS E 48852.0 N 3886.6 U 393.1

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile D1_MC_DUAL_AUX
NEW CYLI
DIAM 449.9
HEIG 578.2
ORI Z IS N AND Y IS U
POS E 48852.0 N 4169.5 U 393.1

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 323.9
DBOT 449.9
HEIG 89.9
ORI Z IS N AND Y IS U
POS E 48852.0 N 4503.6 U 393.1

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 171.0
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 4539.5 U 393.1

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 81.0
HEIG 15.2
ORI Z IS S AND Y IS U
POS E 48852.0 N 3807.1 U 393.1

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 303.6
YLEN 11.2
ZLEN 8.1
POS E 48852.0 N 3805.1 U 273.1

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 8.1
YLEN 11.2
ZLEN 303.6
POS E 48971.9 N 3805.1 U 393.1

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 367.8
YLEN 11.2
ZLEN 8.1
POS E 48852.0 N 3805.1 U 333.1

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 8.1
YLEN 11.2
ZLEN 367.8
POS E 48912.0 N 3805.1 U 393.1

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 386.9
YLEN 11.2
ZLEN 8.1
POS E 48852.0 N 3805.1 U 393.1

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 8.1
YLEN 11.2
ZLEN 386.9
POS E 48852.0 N 3805.1 U 393.1

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 367.8
YLEN 11.2
ZLEN 8.1
POS E 48852.0 N 3805.1 U 453.1

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 8.1
YLEN 11.2
ZLEN 367.8
POS E 48792.0 N 3805.1 U 393.1

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 303.6
YLEN 11.2
ZLEN 8.1
POS E 48852.0 N 3805.1 U 513.0

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 8.1
YLEN 11.2
ZLEN 303.6
POS E 48732.1 N 3805.1 U 393.1

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 150.6
YLEN 104.9
ZLEN 28.0
POS E 49082.1 N 4001.7 U 142.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 63.3
YLEN 81.8
ZLEN 89.8
POS E 49049.0 N 4001.7 U 201.3

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 150.6
YLEN 104.9
ZLEN 28.0
POS E 48621.9 N 4001.7 U 142.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 63.3
YLEN 81.8
ZLEN 89.8
POS E 48655.0 N 4001.7 U 201.3

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 150.6
YLEN 104.9
ZLEN 28.0
POS E 49082.1 N 4346.3 U 142.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 63.3
YLEN 81.8
ZLEN 89.8
POS E 49049.0 N 4346.3 U 201.3

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 150.6
YLEN 104.9
ZLEN 28.0
POS E 48621.9 N 4346.3 U 142.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 63.3
YLEN 81.8
ZLEN 89.8
POS E 48655.0 N 4346.3 U 201.3

-- Reference Value: 360-degree motor cooling rib 1/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48852.0 N 4169.5 U 623.5

-- Reference Value: 360-degree motor cooling rib 2/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48916.9 N 4169.5 U 614.1

-- Reference Value: 360-degree motor cooling rib 3/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48976.6 N 4169.5 U 586.9

-- Reference Value: 360-degree motor cooling rib 4/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 49026.1 N 4169.5 U 544.0

-- Reference Value: 360-degree motor cooling rib 5/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 49061.6 N 4169.5 U 488.8

-- Reference Value: 360-degree motor cooling rib 6/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 49080.0 N 4169.5 U 425.9

-- Reference Value: 360-degree motor cooling rib 7/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 49080.0 N 4169.5 U 360.3

-- Reference Value: 360-degree motor cooling rib 8/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 49061.6 N 4169.5 U 297.4

-- Reference Value: 360-degree motor cooling rib 9/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 49026.1 N 4169.5 U 242.2

-- Reference Value: 360-degree motor cooling rib 10/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48976.6 N 4169.5 U 199.3

-- Reference Value: 360-degree motor cooling rib 11/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48916.9 N 4169.5 U 172.0

-- Reference Value: 360-degree motor cooling rib 12/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48852.0 N 4169.5 U 162.7

-- Reference Value: 360-degree motor cooling rib 13/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48787.1 N 4169.5 U 172.0

-- Reference Value: 360-degree motor cooling rib 14/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48727.4 N 4169.5 U 199.3

-- Reference Value: 360-degree motor cooling rib 15/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48677.9 N 4169.5 U 242.2

-- Reference Value: 360-degree motor cooling rib 16/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48642.4 N 4169.5 U 297.4

-- Reference Value: 360-degree motor cooling rib 17/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48624.0 N 4169.5 U 360.3

-- Reference Value: 360-degree motor cooling rib 18/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48624.0 N 4169.5 U 425.9

-- Reference Value: 360-degree motor cooling rib 19/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48642.4 N 4169.5 U 488.8

-- Reference Value: 360-degree motor cooling rib 20/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48677.9 N 4169.5 U 544.0

-- Reference Value: 360-degree motor cooling rib 21/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48727.4 N 4169.5 U 586.9

-- Reference Value: 360-degree motor cooling rib 22/22
NEW CYLI
DIAM 24.7
HEIG 508.8
ORI Z IS N AND Y IS U
POS E 48787.1 N 4169.5 U 614.1

-- Reference Value: MC-pump main drive stator reinforcing band 1/3
NEW CYLI
DIAM 474.6
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 4024.9 U 393.1

-- Reference Value: MC-pump main drive stator reinforcing band 2/3
NEW CYLI
DIAM 474.6
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 4169.5 U 393.1

-- Reference Value: MC-pump main drive stator reinforcing band 3/3
NEW CYLI
DIAM 474.6
HEIG 18.0
ORI Z IS N AND Y IS U
POS E 48852.0 N 4314.1 U 393.1

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 282.4
YLEN 202.2
ZLEN 116.4
POS E 48852.0 N 4144.0 U 694.1

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 293.7
YLEN 210.3
ZLEN 12.0
POS E 48852.0 N 4144.0 U 758.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.3
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 48953.7 N 4067.2 U 767.6

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.3
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 48750.3 N 4067.2 U 767.6

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.3
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 48953.7 N 4220.9 U 767.6

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.3
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 48750.3 N 4220.9 U 767.6

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 32.4
HEIG 13.2
ORI Z IS W AND Y IS U
POS E 48704.2 N 4144.0 U 688.2

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 24.0
HEIG 15.6
ORI Z IS W AND Y IS U
POS E 48689.8 N 4144.0 U 688.2

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 22.0
YLEN 64.7
ZLEN 58.0
POS E 48852.0 N 4308.8 U 647.0

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 29.7
HEIG 37.3
ORI Z IS W AND Y IS U
POS E 48852.0 N 4308.8 U 663.3

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 9.0
YLEN 119.8
ZLEN 63.5
POS E 49078.9 N 4218.9 U 420.1

NEW SUBE /205_PU_054_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 49103.0 N 4001.7 U 169.9

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 49103.0 N 4001.7 U 158.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 49103.0 N 4001.7 U 189.6

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 48601.0 N 4001.7 U 169.9

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 48601.0 N 4001.7 U 158.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 48601.0 N 4001.7 U 189.6

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 49103.0 N 4346.3 U 169.9

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 49103.0 N 4346.3 U 158.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 49103.0 N 4346.3 U 189.6

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 48601.0 N 4346.3 U 169.9

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 48601.0 N 4346.3 U 158.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 48601.0 N 4346.3 U 189.6

NEW SUBE /205_PU_054_SERVICE_DETAILS
NEW SUBE /205_PU_054_MC_AUXILIARY
-- Reference Value: MC integrated air separator; structure based on project top view and official MC-pump separation descriptions
NEW CYLI
DIAM 167.4
HEIG 313.8
ORI Z IS U AND Y IS N
POS E 48527.7 N 5014.0 U 285.4

-- Reference Value: MC separator top reducer
NEW CONE
DTOP 103.8
DBOT 167.4
HEIG 50.2
ORI Z IS U AND Y IS N
POS E 48527.7 N 5014.0 U 467.4

-- Reference Value: MC separator degassing outlet
NEW CYLI
DIAM 36.8
HEIG 47.1
ORI Z IS U AND Y IS N
POS E 48527.7 N 5014.0 U 516.0

-- Reference Value: MC degassing connection line
NEW CYLI
DIAM 47.1
HEIG 178.8
ORI Z IS W AND Y IS U
POS E 48617.1 N 5158.2 U 507.4

-- Reference Value: MC separator auxiliary motor barrel
NEW CYLI
DIAM 167.4
HEIG 316.8
ORI Z IS N AND Y IS U
POS E 48527.7 N 4322.8 U 232.2

-- Reference Value: MC auxiliary motor fan cover
NEW CYLI
DIAM 150.6
HEIG 79.2
ORI Z IS N AND Y IS U
POS E 48527.7 N 4133.6 U 232.2

-- Reference Value: MC auxiliary motor drive-end bell
NEW CONE
DTOP 110.5
DBOT 167.4
HEIG 52.8
ORI Z IS N AND Y IS U
POS E 48527.7 N 4490.0 U 232.2

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 1/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48527.7 N 4322.8 U 318.1

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 2/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48578.2 N 4322.8 U 301.7

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 3/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48609.4 N 4322.8 U 258.8

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 4/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48609.4 N 4322.8 U 205.7

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 5/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48578.2 N 4322.8 U 162.7

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 6/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48527.7 N 4322.8 U 146.3

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 7/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48477.3 N 4322.8 U 162.7

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 8/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48446.1 N 4322.8 U 205.7

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 9/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48446.1 N 4322.8 U 258.8

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 10/10
NEW CYLI
DIAM 10.0
HEIG 272.4
ORI Z IS N AND Y IS U
POS E 48477.3 N 4322.8 U 301.7

-- Reference Value: MC auxiliary-motor terminal box
NEW BOX
XLEN 66.9
YLEN 88.0
ZLEN 28.5
POS E 48527.7 N 4314.0 U 340.2

-- Reference Value: MC auxiliary motor foot
NEW BOX
XLEN 120.5
YLEN 79.2
ZLEN 20.1
POS E 48527.7 N 4217.2 U 138.5

-- Reference Value: MC auxiliary motor foot
NEW BOX
XLEN 120.5
YLEN 79.2
ZLEN 20.1
POS E 48527.7 N 4410.8 U 138.5

-- Reference Value: enlarged MC separation/control side package matched to the tag-specific top view
NEW BOX
XLEN 240.6
YLEN 360.0
ZLEN 170.0
POS E 49176.3 N 5194.0 U 213.4

-- Reference Value: MC side-package access lid
NEW BOX
XLEN 247.8
YLEN 370.8
ZLEN 13.6
POS E 49176.3 N 5194.0 U 305.2

-- Reference Value: MC side-package lid fastener
NEW CYLI
DIAM 14.3
HEIG 8.8
ORI Z IS U AND Y IS N
POS E 49262.9 N 5057.2 U 316.5

-- Reference Value: MC side-package lid fastener
NEW CYLI
DIAM 14.3
HEIG 8.8
ORI Z IS U AND Y IS N
POS E 49089.7 N 5057.2 U 316.5

-- Reference Value: MC side-package lid fastener
NEW CYLI
DIAM 14.3
HEIG 8.8
ORI Z IS U AND Y IS N
POS E 49262.9 N 5330.8 U 316.5

-- Reference Value: MC side-package lid fastener
NEW CYLI
DIAM 14.3
HEIG 8.8
ORI Z IS U AND Y IS N
POS E 49089.7 N 5330.8 U 316.5

-- Reference Value: D1 MC orthogonal auxiliary-drive barrel matched to 205-PU-054 top-view arrangement
NEW CYLI
DIAM 136.0
HEIG 282.4
ORI Z IS E AND Y IS U
POS E 49233.8 N 5074.0 U 211.4

-- Reference Value: D1 orthogonal auxiliary-drive pedestal
NEW BOX
XLEN 67.8
YLEN 70.7
ZLEN 18.0
POS E 49092.6 N 5074.0 U 137.4


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 212 primitives.
