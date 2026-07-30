-- ====================================================================
-- 205-PU-038 - EOP STAGE MC PUMP (205-PU-038/MC PUMP)
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 205-PU-038
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis W from driver to casing; suction S; discharge W
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:29

NEW EQUI /205_PU_038
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_038_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 2000.0
YLEN 1051.0
ZLEN 50.0
POS E 43119.0 N 5016.0 U 25.0

NEW SUBE /205_PU_038_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 44009.0 N 5473.2 U 53.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 44009.0 N 5473.2 U 52.3

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 44009.0 N 5473.2 U 61.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 44009.0 N 4558.8 U 53.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 44009.0 N 4558.8 U 52.3

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 44009.0 N 4558.8 U 61.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 42229.0 N 5473.2 U 53.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 42229.0 N 5473.2 U 52.3

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 42229.0 N 5473.2 U 61.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 42229.0 N 4558.8 U 53.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 42229.0 N 4558.8 U 52.3

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 42229.0 N 4558.8 U 61.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 43119.0 N 5473.2 U 53.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 43119.0 N 5473.2 U 52.3

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 43119.0 N 5473.2 U 61.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 43119.0 N 4558.8 U 53.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 43119.0 N 4558.8 U 52.3

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 43119.0 N 4558.8 U 61.1

-- Reference Value: baseplate anchor fastener A7: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 44009.0 N 5016.0 U 53.5

-- Reference Value: baseplate anchor fastener A7: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 44009.0 N 5016.0 U 52.3

-- Reference Value: baseplate anchor fastener A7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 44009.0 N 5016.0 U 61.1

-- Reference Value: baseplate anchor fastener A8: exposed threaded shank Reference Value
NEW CYLI
DIAM 21.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 42229.0 N 5016.0 U 53.5

-- Reference Value: baseplate anchor fastener A8: solid washer under filled shank Reference Value
NEW CYLI
DIAM 45.2
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 42229.0 N 5016.0 U 52.3

-- Reference Value: baseplate anchor fastener A8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 36.2
HEIG 13.0
ORI Z IS U AND Y IS N
POS E 42229.0 N 5016.0 U 61.1

NEW SUBE /205_PU_038_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 1640.0
YLEN 84.1
ZLEN 78.8
POS E 43159.0 N 5268.2 U 89.4

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 1640.0
YLEN 84.1
ZLEN 78.8
POS E 43159.0 N 4763.8 U 89.4

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 60.5
YLEN 756.7
ZLEN 53.6
POS E 43799.0 N 5016.0 U 76.8

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 60.5
YLEN 756.7
ZLEN 53.6
POS E 43345.7 N 5016.0 U 76.8

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 60.5
YLEN 756.7
ZLEN 53.6
POS E 42892.3 N 5016.0 U 76.8

-- Reference Value: skid cross-member 4
NEW BOX
XLEN 60.5
YLEN 756.7
ZLEN 53.6
POS E 42439.0 N 5016.0 U 76.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 150.0
YLEN 136.6
ZLEN 83.7
POS E 42851.4 N 5205.2 U 91.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 150.0
YLEN 136.6
ZLEN 83.7
POS E 42851.4 N 4826.8 U 91.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 150.0
YLEN 136.6
ZLEN 83.7
POS E 42530.1 N 5205.2 U 91.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 150.0
YLEN 136.6
ZLEN 83.7
POS E 42530.1 N 4826.8 U 91.8

NEW SUBE /205_PU_038_CASING
-- Reference Value: Medium-consistency fluidizer volute back-pull-out rear plate
NEW CYLI
DIAM 455.2
HEIG 75.6
ORI Z IS W AND Y IS U
POS E 42958.5 N 5016.0 U 392.3

-- Reference Value: Medium-consistency fluidizer volute radially split casing envelope
NEW CYLI
DIAM 517.3
HEIG 365.4
ORI Z IS W AND Y IS U
POS E 42738.0 N 5016.0 U 392.3

-- Reference Value: casing split flange
NEW CYLI
DIAM 569.0
HEIG 20.0
ORI Z IS W AND Y IS U
POS E 42565.3 N 5016.0 U 392.3

-- Reference Value: Medium-consistency fluidizer volute tapered impeller-eye cover
NEW CONE
DTOP 248.3
DBOT 507.0
HEIG 189.0
ORI Z IS W AND Y IS U
POS E 42460.8 N 5016.0 U 392.3

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 269.0
HEIG 22.0
ORI Z IS W AND Y IS U
POS E 42377.3 N 5016.0 U 392.3

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 1/5
NEW CYLI
DIAM 20.7
HEIG 248.5
ORI Z IS W AND Y IS U
POS E 42738.0 N 5016.0 U 654.7

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 2/5
NEW CYLI
DIAM 20.7
HEIG 248.5
ORI Z IS W AND Y IS U
POS E 42738.0 N 5265.5 U 473.4

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 3/5
NEW CYLI
DIAM 20.7
HEIG 248.5
ORI Z IS W AND Y IS U
POS E 42738.0 N 5170.2 U 180.0

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 4/5
NEW CYLI
DIAM 20.7
HEIG 248.5
ORI Z IS W AND Y IS U
POS E 42738.0 N 4861.8 U 180.0

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 5/5
NEW CYLI
DIAM 20.7
HEIG 248.5
ORI Z IS W AND Y IS U
POS E 42738.0 N 4766.5 U 473.4

-- Reference Value: MC fluidizer nose sleeve
NEW CYLI
DIAM 227.6
HEIG 41.6
ORI Z IS W AND Y IS U
POS E 42387.1 N 5016.0 U 392.3

NEW SUBE /205_PU_038_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 4747.0 U 392.3

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 4747.0 U 392.3

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 4747.0 U 392.3

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 4773.6 U 509.0

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 4773.6 U 509.0

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 4773.6 U 509.0

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 4848.3 U 602.6

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 4848.3 U 602.6

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 4848.3 U 602.6

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 4956.1 U 654.6

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 4956.1 U 654.6

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 4956.1 U 654.6

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 5075.9 U 654.6

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 5075.9 U 654.6

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 5075.9 U 654.6

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 5183.7 U 602.6

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 5183.7 U 602.6

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 5183.7 U 602.6

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 5258.4 U 509.0

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 5258.4 U 509.0

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 5258.4 U 509.0

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 5285.0 U 392.3

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 5285.0 U 392.3

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 5285.0 U 392.3

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 5258.4 U 275.6

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 5258.4 U 275.6

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 5258.4 U 275.6

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 5183.7 U 182.0

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 5183.7 U 182.0

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 5183.7 U 182.0

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 5075.9 U 130.1

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 5075.9 U 130.1

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 5075.9 U 130.1

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 4956.1 U 130.1

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 4956.1 U 130.1

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 4956.1 U 130.1

-- Reference Value: casing split-line bolt C13: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 4848.3 U 182.0

-- Reference Value: casing split-line bolt C13: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 4848.3 U 182.0

-- Reference Value: casing split-line bolt C13: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 4848.3 U 182.0

-- Reference Value: casing split-line bolt C14: flange-penetrating stud Reference Value
NEW CYLI
DIAM 23.3
HEIG 22.1
ORI Z IS W AND Y IS U
POS E 42547.8 N 4773.6 U 275.6

-- Reference Value: casing split-line bolt C14: flange-face washer Reference Value
NEW CYLI
DIAM 48.9
HEIG 5.1
ORI Z IS W AND Y IS U
POS E 42552.8 N 4773.6 U 275.6

-- Reference Value: casing split-line bolt C14: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 40.0
HEIG 13.5
ORI Z IS W AND Y IS U
POS E 42543.5 N 4773.6 U 275.6

NEW SUBE /205_PU_038_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 119.0
HEIG 30.3
ORI Z IS W AND Y IS U
POS E 43132.8 N 5016.0 U 392.3

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 137.1
HEIG 30.3
ORI Z IS W AND Y IS U
POS E 43102.5 N 5016.0 U 392.3

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 155.2
HEIG 30.3
ORI Z IS W AND Y IS U
POS E 43072.2 N 5016.0 U 392.3

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 173.3
HEIG 30.3
ORI Z IS W AND Y IS U
POS E 43041.8 N 5016.0 U 392.3

-- Reference Value: stepped bearing bracket section 5
NEW CYLI
DIAM 191.4
HEIG 30.3
ORI Z IS W AND Y IS U
POS E 43011.5 N 5016.0 U 392.3

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 113.8
DBOT 165.5
HEIG 55.0
ORI Z IS W AND Y IS U
POS E 43023.8 N 5016.0 U 392.3

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 106.2
YLEN 137.8
ZLEN 167.8
POS E 43064.6 N 5016.0 U 212.7

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 23.0
HEIG 20.7
ORI Z IS U AND Y IS N
POS E 43063.1 N 5016.0 U 498.3

NEW SUBE /205_PU_038_SUCTION
-- Reference Value: suction DN200; POS is flange face, contractual direction S
NEW NOZZLE /205_PU_038_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 42681.3 N 4477.3 U 392.3
ORI P1 IS S
HEIG 280.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_038_DISCHARGE
-- Reference Value: discharge DN150; POS is flange face, contractual direction W
NEW NOZZLE /205_PU_038_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 42177.2 N 5016.0 U 392.3
ORI P1 IS W
HEIG 189.2
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_038_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 36.0
HEIG 140.0
ORI Z IS W AND Y IS U
POS E 43218.0 N 5016.0 U 392.3

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 77.4
HEIG 35.0
ORI Z IS W AND Y IS U
POS E 43270.5 N 5016.0 U 392.3

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 77.4
HEIG 35.0
ORI Z IS W AND Y IS U
POS E 43165.5 N 5016.0 U 392.3

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 91.3
HEIG 28.0
ORI Z IS W AND Y IS U
POS E 43218.0 N 5016.0 U 392.3

-- Reference Value: fabricated rectangular coupling guard
NEW BOX
XLEN 140.0
YLEN 184.2
ZLEN 156.2
POS E 43218.0 N 5016.0 U 392.3

-- Reference Value: boxed guard top reinforcing seam
NEW BOX
XLEN 114.8
YLEN 11.0
ZLEN 11.0
POS E 43218.0 N 5016.0 U 476.4

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 24.0
YLEN 124.2
ZLEN 163.4
POS E 43262.8 N 5016.0 U 210.5

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 24.0
YLEN 124.2
ZLEN 163.4
POS E 43173.2 N 5016.0 U 210.5

NEW SUBE /205_PU_038_DRIVER
-- Reference Value: MC-pump main drive TEFC motor fan cowl
NEW CYLI
DIAM 412.1
HEIG 111.3
ORI Z IS W AND Y IS U
POS E 43974.3 N 5016.0 U 392.3

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 447.9
DBOT 403.1
HEIG 50.1
ORI Z IS W AND Y IS U
POS E 43943.7 N 5016.0 U 392.3

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile EOP_MC_LARGE_SEPARATOR
NEW CYLI
DIAM 447.9
HEIG 572.8
ORI Z IS W AND Y IS U
POS E 43663.5 N 5016.0 U 392.3

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 322.5
DBOT 447.9
HEIG 89.0
ORI Z IS W AND Y IS U
POS E 43332.5 N 5016.0 U 392.3

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 170.2
HEIG 18.0
ORI Z IS W AND Y IS U
POS E 43297.0 N 5016.0 U 392.3

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 80.6
HEIG 15.1
ORI Z IS E AND Y IS U
POS E 44022.4 N 5016.0 U 392.3

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 11.2
YLEN 302.2
ZLEN 8.1
POS E 44024.4 N 5016.0 U 272.9

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 11.2
YLEN 8.1
ZLEN 302.2
POS E 44024.4 N 5135.4 U 392.3

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 11.2
YLEN 366.2
ZLEN 8.1
POS E 44024.4 N 5016.0 U 332.6

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 11.2
YLEN 8.1
ZLEN 366.2
POS E 44024.4 N 5075.7 U 392.3

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 11.2
YLEN 385.2
ZLEN 8.1
POS E 44024.4 N 5016.0 U 392.3

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 11.2
YLEN 8.1
ZLEN 385.2
POS E 44024.4 N 5016.0 U 392.3

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 11.2
YLEN 366.2
ZLEN 8.1
POS E 44024.4 N 5016.0 U 452.0

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 11.2
YLEN 8.1
ZLEN 366.2
POS E 44024.4 N 4956.3 U 392.3

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 11.2
YLEN 302.2
ZLEN 8.1
POS E 44024.4 N 5016.0 U 511.7

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 11.2
YLEN 8.1
ZLEN 302.2
POS E 44024.4 N 4896.6 U 392.3

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 103.9
YLEN 151.3
ZLEN 28.0
POS E 43829.7 N 5247.2 U 142.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 81.0
YLEN 63.6
ZLEN 90.9
POS E 43829.7 N 5213.9 U 202.3

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 103.9
YLEN 151.3
ZLEN 28.0
POS E 43829.7 N 4784.8 U 142.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 81.0
YLEN 63.6
ZLEN 90.9
POS E 43829.7 N 4818.1 U 202.3

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 103.9
YLEN 151.3
ZLEN 28.0
POS E 43488.3 N 5247.2 U 142.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 81.0
YLEN 63.6
ZLEN 90.9
POS E 43488.3 N 5213.9 U 202.3

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 103.9
YLEN 151.3
ZLEN 28.0
POS E 43488.3 N 4784.8 U 142.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 81.0
YLEN 63.6
ZLEN 90.9
POS E 43488.3 N 4818.1 U 202.3

-- Reference Value: 360-degree motor cooling rib 1/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5016.0 U 621.7

-- Reference Value: 360-degree motor cooling rib 2/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5086.9 U 610.5

-- Reference Value: 360-degree motor cooling rib 3/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5150.8 U 577.9

-- Reference Value: 360-degree motor cooling rib 4/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5201.6 U 527.1

-- Reference Value: 360-degree motor cooling rib 5/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5234.2 U 463.2

-- Reference Value: 360-degree motor cooling rib 6/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5245.4 U 392.3

-- Reference Value: 360-degree motor cooling rib 7/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5234.2 U 321.4

-- Reference Value: 360-degree motor cooling rib 8/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5201.6 U 257.5

-- Reference Value: 360-degree motor cooling rib 9/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5150.8 U 206.7

-- Reference Value: 360-degree motor cooling rib 10/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5086.9 U 174.2

-- Reference Value: 360-degree motor cooling rib 11/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 5016.0 U 162.9

-- Reference Value: 360-degree motor cooling rib 12/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 4945.1 U 174.2

-- Reference Value: 360-degree motor cooling rib 13/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 4881.2 U 206.7

-- Reference Value: 360-degree motor cooling rib 14/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 4830.4 U 257.5

-- Reference Value: 360-degree motor cooling rib 15/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 4797.8 U 321.4

-- Reference Value: 360-degree motor cooling rib 16/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 4786.6 U 392.3

-- Reference Value: 360-degree motor cooling rib 17/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 4797.8 U 463.2

-- Reference Value: 360-degree motor cooling rib 18/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 4830.4 U 527.1

-- Reference Value: 360-degree motor cooling rib 19/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 4881.2 U 577.9

-- Reference Value: 360-degree motor cooling rib 20/20
NEW CYLI
DIAM 24.6
HEIG 504.1
ORI Z IS W AND Y IS U
POS E 43663.5 N 4945.1 U 610.5

-- Reference Value: MC-pump main drive stator reinforcing band 1/3
NEW CYLI
DIAM 472.6
HEIG 18.0
ORI Z IS W AND Y IS U
POS E 43806.7 N 5016.0 U 392.3

-- Reference Value: MC-pump main drive stator reinforcing band 2/3
NEW CYLI
DIAM 472.6
HEIG 18.0
ORI Z IS W AND Y IS U
POS E 43663.5 N 5016.0 U 392.3

-- Reference Value: MC-pump main drive stator reinforcing band 3/3
NEW CYLI
DIAM 472.6
HEIG 18.0
ORI Z IS W AND Y IS U
POS E 43520.2 N 5016.0 U 392.3

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 200.3
YLEN 283.8
ZLEN 115.9
POS E 43688.7 N 5016.0 U 692.0

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 208.4
YLEN 295.1
ZLEN 12.0
POS E 43688.7 N 5016.0 U 755.9

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.4
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 43764.8 N 5118.2 U 765.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.4
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 43764.8 N 4913.8 U 765.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.4
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 43612.6 N 5118.2 U 765.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 16.4
HEIG 6.6
ORI Z IS U AND Y IS N
POS E 43612.6 N 4913.8 U 765.2

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 32.4
HEIG 13.2
ORI Z IS S AND Y IS U
POS E 43688.7 N 4867.5 U 686.2

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 24.0
HEIG 15.6
ORI Z IS S AND Y IS U
POS E 43688.7 N 4853.1 U 686.2

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 64.1
YLEN 22.0
ZLEN 58.0
POS E 43525.4 N 5016.0 U 645.3

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 29.7
HEIG 37.4
ORI Z IS S AND Y IS U
POS E 43525.4 N 5016.0 U 661.5

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 118.7
YLEN 9.0
ZLEN 63.2
POS E 43614.5 N 5242.0 U 419.2

NEW SUBE /205_PU_038_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 43829.7 N 5268.2 U 170.3

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 43829.7 N 5268.2 U 159.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 43829.7 N 5268.2 U 190.0

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 43829.7 N 4763.8 U 170.3

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 43829.7 N 4763.8 U 159.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 43829.7 N 4763.8 U 190.0

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 43488.3 N 5268.2 U 170.3

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 43488.3 N 5268.2 U 159.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 43488.3 N 5268.2 U 190.0

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 20.0
HEIG 27.0
ORI Z IS U AND Y IS N
POS E 43488.3 N 4763.8 U 170.3

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 43.0
HEIG 4.4
ORI Z IS U AND Y IS N
POS E 43488.3 N 4763.8 U 159.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 34.4
HEIG 12.4
ORI Z IS U AND Y IS N
POS E 43488.3 N 4763.8 U 190.0

NEW SUBE /205_PU_038_SERVICE_DETAILS
NEW SUBE /205_PU_038_MC_AUXILIARY
-- Reference Value: MC integrated air separator; structure based on project top view and official MC-pump separation descriptions
NEW CYLI
DIAM 191.7
HEIG 359.4
ORI Z IS U AND Y IS N
POS E 42639.0 N 4690.2 U 308.5

-- Reference Value: MC separator top reducer
NEW CONE
DTOP 118.9
DBOT 191.7
HEIG 57.5
ORI Z IS U AND Y IS N
POS E 42639.0 N 4690.2 U 517.0

-- Reference Value: MC separator degassing outlet
NEW CYLI
DIAM 42.2
HEIG 53.9
ORI Z IS U AND Y IS N
POS E 42639.0 N 4690.2 U 572.7

-- Reference Value: MC degassing connection line
NEW CYLI
DIAM 47.3
HEIG 181.0
ORI Z IS S AND Y IS U
POS E 42681.3 N 4780.7 U 506.1

-- Reference Value: MC separator auxiliary motor barrel
NEW CYLI
DIAM 168.2
HEIG 316.8
ORI Z IS W AND Y IS U
POS E 43430.2 N 4690.2 U 233.1

-- Reference Value: MC auxiliary motor fan cover
NEW CYLI
DIAM 151.3
HEIG 79.2
ORI Z IS W AND Y IS U
POS E 43619.4 N 4690.2 U 233.1

-- Reference Value: MC auxiliary motor drive-end bell
NEW CONE
DTOP 111.0
DBOT 168.2
HEIG 52.8
ORI Z IS W AND Y IS U
POS E 43263.0 N 4690.2 U 233.1

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 1/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4690.2 U 319.4

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 2/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4740.9 U 302.9

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 3/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4772.3 U 259.8

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 4/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4772.3 U 206.4

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 5/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4740.9 U 163.3

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 6/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4690.2 U 146.8

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 7/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4639.5 U 163.3

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 8/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4608.1 U 206.4

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 9/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4608.1 U 259.8

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 10/10
NEW CYLI
DIAM 10.1
HEIG 272.4
ORI Z IS W AND Y IS U
POS E 43430.2 N 4639.5 U 302.9

-- Reference Value: MC auxiliary-motor terminal box
NEW BOX
XLEN 88.0
YLEN 67.3
ZLEN 28.6
POS E 43439.0 N 4690.2 U 341.5

-- Reference Value: MC auxiliary motor foot
NEW BOX
XLEN 79.2
YLEN 121.1
ZLEN 20.2
POS E 43535.8 N 4690.2 U 138.9

-- Reference Value: MC auxiliary motor foot
NEW BOX
XLEN 79.2
YLEN 121.1
ZLEN 20.2
POS E 43342.2 N 4690.2 U 138.9

-- Reference Value: enlarged MC separation/control side package matched to the tag-specific top view
NEW BOX
XLEN 360.0
YLEN 241.7
ZLEN 170.0
POS E 42499.0 N 5341.8 U 213.8

-- Reference Value: MC side-package access lid
NEW BOX
XLEN 370.8
YLEN 249.0
ZLEN 13.6
POS E 42499.0 N 5341.8 U 305.6

-- Reference Value: MC side-package lid fastener
NEW CYLI
DIAM 14.4
HEIG 8.8
ORI Z IS U AND Y IS N
POS E 42635.8 N 5428.8 U 316.8

-- Reference Value: MC side-package lid fastener
NEW CYLI
DIAM 14.4
HEIG 8.8
ORI Z IS U AND Y IS N
POS E 42635.8 N 5254.8 U 316.8

-- Reference Value: MC side-package lid fastener
NEW CYLI
DIAM 14.4
HEIG 8.8
ORI Z IS U AND Y IS N
POS E 42362.2 N 5428.8 U 316.8

-- Reference Value: MC side-package lid fastener
NEW CYLI
DIAM 14.4
HEIG 8.8
ORI Z IS U AND Y IS N
POS E 42362.2 N 5254.8 U 316.8


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 200 primitives.
