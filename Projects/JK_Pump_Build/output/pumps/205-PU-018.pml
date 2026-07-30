-- ====================================================================
-- 205-PU-018 - D0 STAGE MC PUMP (205-PU-018/MC PUMP)
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 205-PU-018
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis W from driver to casing; suction S; discharge W
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /205_PU_018
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_018_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 2022.0
YLEN 1051.0
ZLEN 50.0
POS E 35723.0 N 5019.0 U 25.0

NEW SUBE /205_PU_018_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 36622.8 N 5476.2 U 53.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 36622.8 N 5476.2 U 52.3

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 36622.8 N 5476.2 U 61.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 36622.8 N 4561.8 U 53.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 36622.8 N 4561.8 U 52.3

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 36622.8 N 4561.8 U 61.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 34823.2 N 5476.2 U 53.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 34823.2 N 5476.2 U 52.3

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 34823.2 N 5476.2 U 61.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 34823.2 N 4561.8 U 53.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 34823.2 N 4561.8 U 52.3

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 34823.2 N 4561.8 U 61.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 35723.0 N 5476.2 U 53.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 35723.0 N 5476.2 U 52.3

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 35723.0 N 5476.2 U 61.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 35723.0 N 4561.8 U 53.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 35723.0 N 4561.8 U 52.3

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 35723.0 N 4561.8 U 61.1

-- Reference Value: baseplate anchor fastener A7: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 36622.8 N 5019.0 U 53.5

-- Reference Value: baseplate anchor fastener A7: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 36622.8 N 5019.0 U 52.3

-- Reference Value: baseplate anchor fastener A7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 36622.8 N 5019.0 U 61.1

-- Reference Value: baseplate anchor fastener A8: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 34823.2 N 5019.0 U 53.5

-- Reference Value: baseplate anchor fastener A8: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 34823.2 N 5019.0 U 52.3

-- Reference Value: baseplate anchor fastener A8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 34823.2 N 5019.0 U 61.1

NEW SUBE /205_PU_018_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 1658.0
YLEN 84.1
ZLEN 78.8
POS E 35763.4 N 5271.2 U 89.4

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 1658.0
YLEN 84.1
ZLEN 78.8
POS E 35763.4 N 4766.8 U 89.4

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 60.5
YLEN 756.7
ZLEN 53.6
POS E 36410.5 N 5019.0 U 76.8

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 60.5
YLEN 756.7
ZLEN 53.6
POS E 35952.2 N 5019.0 U 76.8

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 60.5
YLEN 756.7
ZLEN 53.6
POS E 35493.8 N 5019.0 U 76.8

-- Reference Value: skid cross-member 4
NEW BOX
XLEN 60.5
YLEN 756.7
ZLEN 53.6
POS E 35035.5 N 5019.0 U 76.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 151.7
YLEN 136.6
ZLEN 83.7
POS E 35457.4 N 5208.2 U 91.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 151.7
YLEN 136.6
ZLEN 83.7
POS E 35457.4 N 4829.8 U 91.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 151.7
YLEN 136.6
ZLEN 83.7
POS E 35135.7 N 5208.2 U 91.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 151.7
YLEN 136.6
ZLEN 83.7
POS E 35135.7 N 4829.8 U 91.8

NEW SUBE /205_PU_018_CASING
-- Reference Value: Medium-consistency fluidizer volute back-pull-out rear plate
NEW CYLI
DIAM 451.0
HEIG 75.7
ORI Z IS W AND Y IS U
POS E 35564.7 N 5019.0 U 389.9

-- Reference Value: Medium-consistency fluidizer volute radially split casing envelope
NEW CYLI
DIAM 512.5
HEIG 365.9
ORI Z IS W AND Y IS U
POS E 35343.9 N 5019.0 U 389.9

-- Reference Value: casing split flange
NEW CYLI
DIAM 563.7
HEIG 20.0
ORI Z IS W AND Y IS U
POS E 35170.9 N 5019.0 U 389.9

-- Reference Value: Medium-consistency fluidizer volute tapered impeller-eye cover
NEW CONE
DTOP 246.0
DBOT 502.2
HEIG 189.3
ORI Z IS W AND Y IS U
POS E 35066.3 N 5019.0 U 389.9

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 266.5
HEIG 22.0
ORI Z IS W AND Y IS U
POS E 34982.7 N 5019.0 U 389.9

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 1/5
NEW CYLI
DIAM 20.5
HEIG 248.8
ORI Z IS W AND Y IS U
POS E 35343.9 N 5019.0 U 649.8

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 2/5
NEW CYLI
DIAM 20.5
HEIG 248.8
ORI Z IS W AND Y IS U
POS E 35343.9 N 5266.2 U 470.2

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 3/5
NEW CYLI
DIAM 20.5
HEIG 248.8
ORI Z IS W AND Y IS U
POS E 35343.9 N 5171.8 U 179.6

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 4/5
NEW CYLI
DIAM 20.5
HEIG 248.8
ORI Z IS W AND Y IS U
POS E 35343.9 N 4866.2 U 179.6

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 5/5
NEW CYLI
DIAM 20.5
HEIG 248.8
ORI Z IS W AND Y IS U
POS E 35343.9 N 4771.8 U 470.2

-- Reference Value: MC fluidizer nose sleeve
NEW CYLI
DIAM 225.5
HEIG 41.6
ORI Z IS W AND Y IS U
POS E 34992.5 N 5019.0 U 389.9

NEW SUBE /205_PU_018_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 4752.5 U 389.9

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 4752.5 U 389.9

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 4752.5 U 389.9

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 4778.9 U 505.5

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 4778.9 U 505.5

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 4778.9 U 505.5

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 4852.9 U 598.2

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 4852.9 U 598.2

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 4852.9 U 598.2

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 4959.7 U 649.7

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 4959.7 U 649.7

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 4959.7 U 649.7

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 5078.3 U 649.7

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 5078.3 U 649.7

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 5078.3 U 649.7

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 5185.1 U 598.2

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 5185.1 U 598.2

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 5185.1 U 598.2

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 5259.1 U 505.5

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 5259.1 U 505.5

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 5259.1 U 505.5

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 5285.5 U 389.9

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 5285.5 U 389.9

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 5285.5 U 389.9

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 5259.1 U 274.3

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 5259.1 U 274.3

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 5259.1 U 274.3

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 5185.1 U 181.5

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 5185.1 U 181.5

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 5185.1 U 181.5

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 5078.3 U 130.1

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 5078.3 U 130.1

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 5078.3 U 130.1

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 4959.7 U 130.1

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 4959.7 U 130.1

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 4959.7 U 130.1

-- Reference Value: casing split-line bolt C13: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 4852.9 U 181.5

-- Reference Value: casing split-line bolt C13: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 4852.9 U 181.5

-- Reference Value: casing split-line bolt C13: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 4852.9 U 181.5

-- Reference Value: casing split-line bolt C14: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.1
HEIG 21.9
ORI Z IS W AND Y IS U
POS E 35153.4 N 4778.9 U 274.3

-- Reference Value: casing split-line bolt C14: flange-face washer Reference Value
NEW CYLI
DIAM 48.4
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 35158.4 N 4778.9 U 274.3

-- Reference Value: casing split-line bolt C14: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 39.7
HEIG 13.4
ORI Z IS W AND Y IS U
POS E 35149.2 N 4778.9 U 274.3

NEW SUBE /205_PU_018_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 117.9
HEIG 30.7
ORI Z IS W AND Y IS U
POS E 35740.5 N 5019.0 U 389.9

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 135.8
HEIG 30.7
ORI Z IS W AND Y IS U
POS E 35709.9 N 5019.0 U 389.9

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 153.7
HEIG 30.7
ORI Z IS W AND Y IS U
POS E 35679.2 N 5019.0 U 389.9

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 171.7
HEIG 30.7
ORI Z IS W AND Y IS U
POS E 35648.5 N 5019.0 U 389.9

-- Reference Value: stepped bearing bracket section 5
NEW CYLI
DIAM 189.6
HEIG 30.7
ORI Z IS W AND Y IS U
POS E 35617.9 N 5019.0 U 389.9

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 112.7
DBOT 164.0
HEIG 55.0
ORI Z IS W AND Y IS U
POS E 35630.0 N 5019.0 U 389.9

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 107.3
YLEN 136.5
ZLEN 166.3
POS E 35671.5 N 5019.0 U 212.0

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 22.8
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 35670.0 N 5019.0 U 494.9

NEW SUBE /205_PU_018_SUCTION
-- Reference Value: suction DN200; POS is flange face, contractual direction S
NEW NOZZLE /205_PU_018_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 35287.1 N 4479.7 U 389.9
ORI P1 IS S
HEIG 283.1
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_018_DISCHARGE
-- Reference Value: discharge DN150; POS is flange face, contractual direction W
NEW NOZZLE /205_PU_018_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 34782.5 N 5019.0 U 389.9
ORI P1 IS W
HEIG 189.2
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_018_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 36.0
HEIG 141.5
ORI Z IS W AND Y IS U
POS E 35826.6 N 5019.0 U 389.9

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 77.4
HEIG 35.4
ORI Z IS W AND Y IS U
POS E 35879.7 N 5019.0 U 389.9

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 77.4
HEIG 35.4
ORI Z IS W AND Y IS U
POS E 35773.6 N 5019.0 U 389.9

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 91.3
HEIG 28.0
ORI Z IS W AND Y IS U
POS E 35826.6 N 5019.0 U 389.9

-- Reference Value: ventilated guard cage rail 1
NEW CYLI
DIAM 14.9
HEIG 141.5
ORI Z IS W AND Y IS U
POS E 35826.6 N 4939.6 U 389.9

-- Reference Value: ventilated guard cage rail 2
NEW CYLI
DIAM 14.9
HEIG 141.5
ORI Z IS W AND Y IS U
POS E 35826.6 N 4962.9 U 446.0

-- Reference Value: ventilated guard cage rail 3
NEW CYLI
DIAM 14.9
HEIG 141.5
ORI Z IS W AND Y IS U
POS E 35826.6 N 5019.0 U 469.3

-- Reference Value: ventilated guard cage rail 4
NEW CYLI
DIAM 14.9
HEIG 141.5
ORI Z IS W AND Y IS U
POS E 35826.6 N 5075.1 U 446.0

-- Reference Value: ventilated guard cage rail 5
NEW CYLI
DIAM 14.9
HEIG 141.5
ORI Z IS W AND Y IS U
POS E 35826.6 N 5098.4 U 389.9

-- Reference Value: ventilated guard cage rail 6
NEW CYLI
DIAM 14.9
HEIG 141.5
ORI Z IS W AND Y IS U
POS E 35826.6 N 5075.1 U 333.8

-- Reference Value: ventilated guard cage rail 7
NEW CYLI
DIAM 14.9
HEIG 141.5
ORI Z IS W AND Y IS U
POS E 35826.6 N 5019.0 U 310.5

-- Reference Value: ventilated guard cage rail 8
NEW CYLI
DIAM 14.9
HEIG 141.5
ORI Z IS W AND Y IS U
POS E 35826.6 N 4962.9 U 333.8

-- Reference Value: ventilated guard end horizontal brace 1
NEW BOX
XLEN 6.4
YLEN 162.7
ZLEN 14.9
POS E 35894.2 N 5019.0 U 389.9

-- Reference Value: ventilated guard end vertical brace 1
NEW BOX
XLEN 6.4
YLEN 14.9
ZLEN 162.7
POS E 35894.2 N 5019.0 U 389.9

-- Reference Value: ventilated guard end horizontal brace 2
NEW BOX
XLEN 6.4
YLEN 162.7
ZLEN 14.9
POS E 35759.0 N 5019.0 U 389.9

-- Reference Value: ventilated guard end vertical brace 2
NEW BOX
XLEN 6.4
YLEN 14.9
ZLEN 162.7
POS E 35759.0 N 5019.0 U 389.9

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 24.0
YLEN 123.0
ZLEN 161.9
POS E 35871.9 N 5019.0 U 209.8

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 24.0
YLEN 123.0
ZLEN 161.9
POS E 35781.3 N 5019.0 U 209.8

NEW SUBE /205_PU_018_DRIVER
-- Reference Value: MC-pump main drive TEFC motor fan cowl
NEW CYLI
DIAM 408.3
HEIG 111.5
ORI Z IS W AND Y IS U
POS E 36584.8 N 5019.0 U 389.9

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 443.8
DBOT 399.4
HEIG 50.2
ORI Z IS W AND Y IS U
POS E 36554.1 N 5019.0 U 389.9

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile D0_MC_SIDE_SUCTION
NEW CYLI
DIAM 443.8
HEIG 573.7
ORI Z IS W AND Y IS U
POS E 36273.4 N 5019.0 U 389.9

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 319.5
DBOT 443.8
HEIG 89.2
ORI Z IS W AND Y IS U
POS E 35942.0 N 5019.0 U 389.9

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 168.7
HEIG 18.0
ORI Z IS W AND Y IS U
POS E 35906.4 N 5019.0 U 389.9

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 79.9
HEIG 15.0
ORI Z IS E AND Y IS U
POS E 36633.0 N 5019.0 U 389.9

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 11.1
YLEN 299.5
ZLEN 8.0
POS E 36634.9 N 5019.0 U 271.6

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 11.1
YLEN 8.0
ZLEN 299.5
POS E 36634.9 N 5137.3 U 389.9

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 11.1
YLEN 362.9
ZLEN 8.0
POS E 36634.9 N 5019.0 U 330.7

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 11.1
YLEN 8.0
ZLEN 362.9
POS E 36634.9 N 5078.2 U 389.9

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 11.1
YLEN 381.7
ZLEN 8.0
POS E 36634.9 N 5019.0 U 389.9

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 11.1
YLEN 8.0
ZLEN 381.7
POS E 36634.9 N 5019.0 U 389.9

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 11.1
YLEN 362.9
ZLEN 8.0
POS E 36634.9 N 5019.0 U 449.1

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 11.1
YLEN 8.0
ZLEN 362.9
POS E 36634.9 N 4959.8 U 389.9

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 11.1
YLEN 299.5
ZLEN 8.0
POS E 36634.9 N 5019.0 U 508.2

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 11.1
YLEN 8.0
ZLEN 299.5
POS E 36634.9 N 4900.7 U 389.9

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 104.0
YLEN 151.3
ZLEN 28.0
POS E 36439.8 N 5250.2 U 142.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 81.1
YLEN 63.6
ZLEN 91.5
POS E 36439.8 N 5216.9 U 202.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 104.0
YLEN 151.3
ZLEN 28.0
POS E 36439.8 N 4787.8 U 142.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 81.1
YLEN 63.6
ZLEN 91.5
POS E 36439.8 N 4821.1 U 202.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 104.0
YLEN 151.3
ZLEN 28.0
POS E 36098.0 N 5250.2 U 142.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 81.1
YLEN 63.6
ZLEN 91.5
POS E 36098.0 N 5216.9 U 202.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 104.0
YLEN 151.3
ZLEN 28.0
POS E 36098.0 N 4787.8 U 142.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 81.1
YLEN 63.6
ZLEN 91.5
POS E 36098.0 N 4821.1 U 202.6

-- Reference Value: 360-degree motor cooling rib 1/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5019.0 U 617.2

-- Reference Value: 360-degree motor cooling rib 2/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5089.2 U 606.0

-- Reference Value: 360-degree motor cooling rib 3/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5152.6 U 573.8

-- Reference Value: 360-degree motor cooling rib 4/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5202.9 U 523.5

-- Reference Value: 360-degree motor cooling rib 5/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5235.2 U 460.1

-- Reference Value: 360-degree motor cooling rib 6/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5246.3 U 389.9

-- Reference Value: 360-degree motor cooling rib 7/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5235.2 U 319.7

-- Reference Value: 360-degree motor cooling rib 8/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5202.9 U 256.3

-- Reference Value: 360-degree motor cooling rib 9/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5152.6 U 206.0

-- Reference Value: 360-degree motor cooling rib 10/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5089.2 U 173.7

-- Reference Value: 360-degree motor cooling rib 11/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 5019.0 U 162.6

-- Reference Value: 360-degree motor cooling rib 12/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 4948.8 U 173.7

-- Reference Value: 360-degree motor cooling rib 13/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 4885.4 U 206.0

-- Reference Value: 360-degree motor cooling rib 14/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 4835.1 U 256.3

-- Reference Value: 360-degree motor cooling rib 15/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 4802.8 U 319.7

-- Reference Value: 360-degree motor cooling rib 16/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 4791.7 U 389.9

-- Reference Value: 360-degree motor cooling rib 17/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 4802.8 U 460.1

-- Reference Value: 360-degree motor cooling rib 18/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 4835.1 U 523.5

-- Reference Value: 360-degree motor cooling rib 19/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 4885.4 U 573.8

-- Reference Value: 360-degree motor cooling rib 20/20
NEW CYLI
DIAM 24.4
HEIG 504.8
ORI Z IS W AND Y IS U
POS E 36273.4 N 4948.8 U 606.0

-- Reference Value: MC-pump main drive stator reinforcing band 1/3
NEW CYLI
DIAM 468.2
HEIG 18.0
ORI Z IS W AND Y IS U
POS E 36416.8 N 5019.0 U 389.9

-- Reference Value: MC-pump main drive stator reinforcing band 2/3
NEW CYLI
DIAM 468.2
HEIG 18.0
ORI Z IS W AND Y IS U
POS E 36273.4 N 5019.0 U 389.9

-- Reference Value: MC-pump main drive stator reinforcing band 3/3
NEW CYLI
DIAM 468.2
HEIG 18.0
ORI Z IS W AND Y IS U
POS E 36130.0 N 5019.0 U 389.9

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 200.6
YLEN 283.8
ZLEN 114.9
POS E 36298.7 N 5019.0 U 686.8

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 208.7
YLEN 295.1
ZLEN 12.0
POS E 36298.7 N 5019.0 U 750.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.4
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 36374.9 N 5121.2 U 759.5

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.4
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 36374.9 N 4916.8 U 759.5

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.4
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 36222.4 N 5121.2 U 759.5

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.4
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 36222.4 N 4916.8 U 759.5

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 32.4
HEIG 13.2
ORI Z IS S AND Y IS U
POS E 36298.7 N 4870.5 U 681.1

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 24.0
HEIG 15.6
ORI Z IS S AND Y IS U
POS E 36298.7 N 4856.1 U 681.1

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 64.2
YLEN 22.0
ZLEN 58.0
POS E 36135.2 N 5019.0 U 640.8

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 29.7
HEIG 37.4
ORI Z IS S AND Y IS U
POS E 36135.2 N 5019.0 U 657.0

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 118.9
YLEN 9.0
ZLEN 62.7
POS E 36224.4 N 5242.9 U 416.5

NEW SUBE /205_PU_018_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 36439.8 N 5271.2 U 170.3

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 36439.8 N 5271.2 U 159.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 36439.8 N 5271.2 U 190.0

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 36439.8 N 4766.8 U 170.3

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 36439.8 N 4766.8 U 159.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 36439.8 N 4766.8 U 190.0

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 36098.0 N 5271.2 U 170.3

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 36098.0 N 5271.2 U 159.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 36098.0 N 5271.2 U 190.0

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 36098.0 N 4766.8 U 170.3

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 36098.0 N 4766.8 U 159.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 36098.0 N 4766.8 U 190.0

NEW SUBE /205_PU_018_SERVICE_DETAILS
NEW SUBE /205_PU_018_MC_AUXILIARY
-- Reference Value: MC integrated air separator; structure based on project top view and official MC-pump separation descriptions
NEW CYLI
DIAM 168.2
HEIG 315.3
ORI Z IS U AND Y IS N
POS E 35642.1 N 4693.2 U 286.5

-- Reference Value: MC separator top reducer
NEW CONE
DTOP 104.3
DBOT 168.2
HEIG 50.4
ORI Z IS U AND Y IS N
POS E 35642.1 N 4693.2 U 469.3

-- Reference Value: MC separator degassing outlet
NEW CYLI
DIAM 37.0
HEIG 47.3
ORI Z IS U AND Y IS N
POS E 35642.1 N 4693.2 U 518.2

-- Reference Value: MC degassing connection line
NEW CYLI
DIAM 47.3
HEIG 182.3
ORI Z IS S AND Y IS U
POS E 35287.1 N 4784.3 U 502.6

-- Reference Value: MC separator auxiliary motor barrel
NEW CYLI
DIAM 168.2
HEIG 320.3
ORI Z IS W AND Y IS U
POS E 36118.5 N 4693.2 U 233.1

-- Reference Value: MC auxiliary motor fan cover
NEW CYLI
DIAM 151.3
HEIG 80.1
ORI Z IS W AND Y IS U
POS E 36309.8 N 4693.2 U 233.1

-- Reference Value: MC auxiliary motor drive-end bell
NEW CONE
DTOP 111.0
DBOT 168.2
HEIG 53.4
ORI Z IS W AND Y IS U
POS E 35949.5 N 4693.2 U 233.1

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 1/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4693.2 U 319.4

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 2/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4743.9 U 302.9

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 3/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4775.3 U 259.8

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 4/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4775.3 U 206.4

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 5/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4743.9 U 163.3

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 6/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4693.2 U 146.8

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 7/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4642.5 U 163.3

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 8/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4611.1 U 206.4

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 9/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4611.1 U 259.8

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 10/10
NEW CYLI
DIAM 10.1
HEIG 275.4
ORI Z IS W AND Y IS U
POS E 36118.5 N 4642.5 U 302.9

-- Reference Value: MC auxiliary-motor terminal box
NEW BOX
XLEN 89.0
YLEN 67.3
ZLEN 28.6
POS E 36127.4 N 4693.2 U 341.5

-- Reference Value: MC auxiliary motor foot
NEW BOX
XLEN 80.1
YLEN 121.1
ZLEN 20.2
POS E 36225.3 N 4693.2 U 138.9

-- Reference Value: MC auxiliary motor foot
NEW BOX
XLEN 80.1
YLEN 121.1
ZLEN 20.2
POS E 36029.5 N 4693.2 U 138.9


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 204 primitives.
