-- ====================================================================
-- 204-PU-008 - SAND SEPARATOR FEED PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 204-PU-008
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis E from driver to casing; suction E; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /204_PU_008
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_008_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 1720.0
YLEN 760.0
ZLEN 50.0
POS E 20000.0 N 19210.0 U 25.0

NEW SUBE /204_PU_008_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 19234.6 N 18880.0 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 19234.6 N 18880.0 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 19234.6 N 18880.0 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 19234.6 N 19540.0 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 19234.6 N 19540.0 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 19234.6 N 19540.0 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 20765.4 N 18880.0 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 20765.4 N 18880.0 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 20765.4 N 18880.0 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 20765.4 N 19540.0 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 20765.4 N 19540.0 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 20765.4 N 19540.0 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 20000.0 N 18880.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 20000.0 N 18880.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 20000.0 N 18880.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 20000.0 N 19540.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 20000.0 N 19540.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 20000.0 N 19540.0 U 58.1

NEW SUBE /204_PU_008_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 1410.4
YLEN 60.8
ZLEN 57.0
POS E 19965.6 N 19027.6 U 78.5

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 1410.4
YLEN 60.8
ZLEN 57.0
POS E 19965.6 N 19392.4 U 78.5

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 19415.2 N 19210.0 U 69.4

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 20000.0 N 19210.0 U 69.4

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 20584.8 N 19210.0 U 69.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.0
YLEN 98.8
ZLEN 87.9
POS E 20450.4 N 19073.2 U 93.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.0
YLEN 98.8
ZLEN 87.9
POS E 20450.4 N 19346.8 U 93.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.0
YLEN 98.8
ZLEN 87.9
POS E 20632.8 N 19073.2 U 93.9

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.0
YLEN 98.8
ZLEN 87.9
POS E 20632.8 N 19346.8 U 93.9

NEW SUBE /204_PU_008_CASING
-- Reference Value: Abrasive-service lined volute back-pull-out rear plate
NEW CYLI
DIAM 269.4
HEIG 35.8
ORI Z IS E AND Y IS U
POS E 20386.0 N 19210.0 U 291.0

-- Reference Value: Abrasive-service lined volute radially split casing envelope
NEW CYLI
DIAM 306.1
HEIG 232.5
ORI Z IS E AND Y IS U
POS E 20520.1 N 19210.0 U 291.0

-- Reference Value: casing split flange
NEW CYLI
DIAM 342.9
HEIG 12.5
ORI Z IS E AND Y IS U
POS E 20630.1 N 19210.0 U 291.0

-- Reference Value: Abrasive-service lined volute tapered impeller-eye cover
NEW CONE
DTOP 183.7
DBOT 300.0
HEIG 89.4
ORI Z IS E AND Y IS U
POS E 20681.1 N 19210.0 U 291.0

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 199.0
HEIG 14.3
ORI Z IS E AND Y IS U
POS E 20718.7 N 19210.0 U 291.0

-- Reference Value: Abrasive-service lined volute circumferentially distributed axial casing rib 1/5
NEW CYLI
DIAM 12.2
HEIG 158.1
ORI Z IS E AND Y IS U
POS E 20520.1 N 19210.0 U 446.2

-- Reference Value: Abrasive-service lined volute circumferentially distributed axial casing rib 2/5
NEW CYLI
DIAM 12.2
HEIG 158.1
ORI Z IS E AND Y IS U
POS E 20520.1 N 19062.3 U 338.9

-- Reference Value: Abrasive-service lined volute circumferentially distributed axial casing rib 3/5
NEW CYLI
DIAM 12.2
HEIG 158.1
ORI Z IS E AND Y IS U
POS E 20520.1 N 19118.7 U 165.3

-- Reference Value: Abrasive-service lined volute circumferentially distributed axial casing rib 4/5
NEW CYLI
DIAM 12.2
HEIG 158.1
ORI Z IS E AND Y IS U
POS E 20520.1 N 19301.3 U 165.3

-- Reference Value: Abrasive-service lined volute circumferentially distributed axial casing rib 5/5
NEW CYLI
DIAM 12.2
HEIG 158.1
ORI Z IS E AND Y IS U
POS E 20520.1 N 19357.7 U 338.9

-- Reference Value: abrasive-service replaceable liner cover
NEW CYLI
DIAM 347.5
HEIG 16.1
ORI Z IS E AND Y IS U
POS E 20623.5 N 19210.0 U 291.0

NEW SUBE /204_PU_008_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19370.7 U 291.0

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19370.7 U 291.0

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19370.7 U 291.0

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19349.2 U 371.3

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19349.2 U 371.3

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19349.2 U 371.3

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19290.4 U 430.1

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19290.4 U 430.1

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19290.4 U 430.1

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19210.0 U 451.7

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19210.0 U 451.7

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19210.0 U 451.7

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19129.6 U 430.1

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19129.6 U 430.1

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19129.6 U 430.1

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19070.8 U 371.3

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19070.8 U 371.3

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19070.8 U 371.3

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19049.3 U 291.0

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19049.3 U 291.0

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19049.3 U 291.0

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19070.8 U 210.6

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19070.8 U 210.6

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19070.8 U 210.6

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19129.6 U 151.8

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19129.6 U 151.8

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19129.6 U 151.8

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19210.0 U 130.2

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19210.0 U 130.2

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19210.0 U 130.2

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19290.4 U 151.8

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19290.4 U 151.8

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19290.4 U 151.8

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20640.6 N 19349.2 U 210.6

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20637.9 N 19349.2 U 210.6

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20643.5 N 19349.2 U 210.6

NEW SUBE /204_PU_008_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 70.4
HEIG 51.6
ORI Z IS E AND Y IS U
POS E 20187.5 N 19210.0 U 291.0

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 81.1
HEIG 51.6
ORI Z IS E AND Y IS U
POS E 20239.1 N 19210.0 U 291.0

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 91.8
HEIG 51.6
ORI Z IS E AND Y IS U
POS E 20290.7 N 19210.0 U 291.0

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 102.6
HEIG 51.6
ORI Z IS E AND Y IS U
POS E 20342.3 N 19210.0 U 291.0

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 67.3
DBOT 98.0
HEIG 35.8
ORI Z IS E AND Y IS U
POS E 20350.2 N 19210.0 U 291.0

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 144.5
YLEN 73.8
ZLEN 132.7
POS E 20275.2 N 19210.0 U 173.3

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 20277.3 N 19210.0 U 352.2

NEW SUBE /204_PU_008_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction E
NEW NOZZLE /204_PU_008_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 20932.2 N 19210.0 U 291.0
ORI P1 IS E
HEIG 206.4
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_008_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 20547.0 N 19210.0 U 447.6

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /204_PU_008_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 20547.0 N 19210.0 U 594.0
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_008_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 27.6
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 20041.3 N 19210.0 U 291.0

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 59.3
HEIG 45.0
ORI Z IS E AND Y IS U
POS E 19943.4 N 19210.0 U 291.0

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 59.3
HEIG 45.0
ORI Z IS E AND Y IS U
POS E 20139.2 N 19210.0 U 291.0

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 70.0
HEIG 28.0
ORI Z IS E AND Y IS U
POS E 20041.3 N 19210.0 U 291.0

-- Reference Value: ventilated guard cage rail 1
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 20041.3 N 19265.9 U 291.0

-- Reference Value: ventilated guard cage rail 2
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 20041.3 N 19249.5 U 330.5

-- Reference Value: ventilated guard cage rail 3
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 20041.3 N 19210.0 U 346.9

-- Reference Value: ventilated guard cage rail 4
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 20041.3 N 19170.5 U 330.5

-- Reference Value: ventilated guard cage rail 5
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 20041.3 N 19154.1 U 291.0

-- Reference Value: ventilated guard cage rail 6
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 20041.3 N 19170.5 U 251.4

-- Reference Value: ventilated guard cage rail 7
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 20041.3 N 19210.0 U 235.0

-- Reference Value: ventilated guard cage rail 8
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 20041.3 N 19249.5 U 251.4

-- Reference Value: ventilated guard end horizontal brace 1
NEW BOX
XLEN 10.8
YLEN 114.6
ZLEN 10.5
POS E 19926.3 N 19210.0 U 291.0

-- Reference Value: ventilated guard end vertical brace 1
NEW BOX
XLEN 10.8
YLEN 10.5
ZLEN 114.6
POS E 19926.3 N 19210.0 U 291.0

-- Reference Value: ventilated guard end horizontal brace 2
NEW BOX
XLEN 10.8
YLEN 114.6
ZLEN 10.5
POS E 20156.3 N 19210.0 U 291.0

-- Reference Value: ventilated guard end vertical brace 2
NEW BOX
XLEN 10.8
YLEN 10.5
ZLEN 114.6
POS E 20156.3 N 19210.0 U 291.0

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 28.9
YLEN 86.7
ZLEN 114.1
POS E 19964.2 N 19210.0 U 164.0

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 28.9
YLEN 86.7
ZLEN 114.1
POS E 20118.3 N 19210.0 U 164.0

NEW SUBE /204_PU_008_DRIVER
-- Reference Value: Heavy-duty high-torque motor TEFC motor fan cowl
NEW CYLI
DIAM 310.1
HEIG 98.2
ORI Z IS E AND Y IS U
POS E 19268.2 N 19210.0 U 291.0

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 316.4
DBOT 284.8
HEIG 44.2
ORI Z IS E AND Y IS U
POS E 19295.3 N 19210.0 U 291.0

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile SAND_SEPARATOR_ABRASIVE
NEW CYLI
DIAM 316.4
HEIG 546.8
ORI Z IS E AND Y IS U
POS E 19563.3 N 19210.0 U 291.0

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 227.8
DBOT 316.4
HEIG 84.2
ORI Z IS E AND Y IS U
POS E 19878.8 N 19210.0 U 291.0

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 120.2
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 19911.9 N 19210.0 U 291.0

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 57.0
HEIG 10.7
ORI Z IS W AND Y IS U
POS E 19224.5 N 19210.0 U 291.0

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 7.9
YLEN 213.5
ZLEN 5.7
POS E 19223.1 N 19210.0 U 206.6

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 7.9
YLEN 5.7
ZLEN 213.5
POS E 19223.1 N 19125.6 U 291.0

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 7.9
YLEN 258.7
ZLEN 5.7
POS E 19223.1 N 19210.0 U 248.8

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 7.9
YLEN 5.7
ZLEN 258.7
POS E 19223.1 N 19167.8 U 291.0

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 7.9
YLEN 272.1
ZLEN 5.7
POS E 19223.1 N 19210.0 U 291.0

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 7.9
YLEN 5.7
ZLEN 272.1
POS E 19223.1 N 19210.0 U 291.0

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 7.9
YLEN 258.7
ZLEN 5.7
POS E 19223.1 N 19210.0 U 333.1

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 7.9
YLEN 5.7
ZLEN 258.7
POS E 19223.1 N 19252.2 U 291.0

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 7.9
YLEN 213.5
ZLEN 5.7
POS E 19223.1 N 19210.0 U 375.3

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 7.9
YLEN 5.7
ZLEN 213.5
POS E 19223.1 N 19294.4 U 291.0

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 98.2
YLEN 109.4
ZLEN 20.2
POS E 19408.6 N 19042.8 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.6
YLEN 46.0
ZLEN 64.7
POS E 19408.6 N 19066.9 U 159.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 98.2
YLEN 109.4
ZLEN 20.2
POS E 19408.6 N 19377.2 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.6
YLEN 46.0
ZLEN 64.7
POS E 19408.6 N 19353.1 U 159.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 98.2
YLEN 109.4
ZLEN 20.2
POS E 19731.4 N 19042.8 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.6
YLEN 46.0
ZLEN 64.7
POS E 19731.4 N 19066.9 U 159.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 98.2
YLEN 109.4
ZLEN 20.2
POS E 19731.4 N 19377.2 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.6
YLEN 46.0
ZLEN 64.7
POS E 19731.4 N 19353.1 U 159.6

-- Reference Value: 360-degree motor cooling rib 1/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19210.0 U 453.0

-- Reference Value: 360-degree motor cooling rib 2/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19154.6 U 443.2

-- Reference Value: 360-degree motor cooling rib 3/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19105.8 U 415.1

-- Reference Value: 360-degree motor cooling rib 4/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19069.7 U 372.0

-- Reference Value: 360-degree motor cooling rib 5/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19050.4 U 319.1

-- Reference Value: 360-degree motor cooling rib 6/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19050.4 U 262.8

-- Reference Value: 360-degree motor cooling rib 7/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19069.7 U 209.9

-- Reference Value: 360-degree motor cooling rib 8/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19105.8 U 166.8

-- Reference Value: 360-degree motor cooling rib 9/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19154.6 U 138.7

-- Reference Value: 360-degree motor cooling rib 10/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19210.0 U 128.9

-- Reference Value: 360-degree motor cooling rib 11/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19265.4 U 138.7

-- Reference Value: 360-degree motor cooling rib 12/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19314.2 U 166.8

-- Reference Value: 360-degree motor cooling rib 13/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19350.3 U 209.9

-- Reference Value: 360-degree motor cooling rib 14/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19369.6 U 262.8

-- Reference Value: 360-degree motor cooling rib 15/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19369.6 U 319.1

-- Reference Value: 360-degree motor cooling rib 16/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19350.3 U 372.0

-- Reference Value: 360-degree motor cooling rib 17/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19314.2 U 415.1

-- Reference Value: 360-degree motor cooling rib 18/18
NEW CYLI
DIAM 17.4
HEIG 481.2
ORI Z IS E AND Y IS U
POS E 19563.3 N 19265.4 U 443.2

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 1/2
NEW CYLI
DIAM 333.8
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 19472.1 N 19210.0 U 291.0

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 2/2
NEW CYLI
DIAM 333.8
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 19654.4 N 19210.0 U 291.0

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 196.5
YLEN 209.8
ZLEN 84.6
POS E 19541.9 N 19210.0 U 504.0

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 204.4
YLEN 218.2
ZLEN 10.2
POS E 19541.9 N 19210.0 U 551.4

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 12.1
HEIG 5.6
ORI Z IS U AND Y IS N
POS E 19467.3 N 19134.5 U 559.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 12.1
HEIG 5.6
ORI Z IS U AND Y IS N
POS E 19467.3 N 19285.5 U 559.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 12.1
HEIG 5.6
ORI Z IS U AND Y IS N
POS E 19616.6 N 19134.5 U 559.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 12.1
HEIG 5.6
ORI Z IS U AND Y IS N
POS E 19616.6 N 19285.5 U 559.3

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 25.1
HEIG 10.2
ORI Z IS N AND Y IS U
POS E 19541.9 N 19320.0 U 499.8

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 18.6
HEIG 12.1
ORI Z IS N AND Y IS U
POS E 19541.9 N 19331.2 U 499.8

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 62.9
YLEN 16.0
ZLEN 51.5
POS E 19696.3 N 19210.0 U 474.9

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.5
HEIG 27.1
ORI Z IS N AND Y IS U
POS E 19696.3 N 19210.0 U 489.3

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 112.3
YLEN 8.2
ZLEN 44.1
POS E 19612.1 N 19049.8 U 309.9

NEW SUBE /204_PU_008_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 19408.6 N 19027.6 U 138.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 19408.6 N 19027.6 U 129.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 19408.6 N 19027.6 U 153.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 19408.6 N 19392.4 U 138.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 19408.6 N 19392.4 U 129.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 19408.6 N 19392.4 U 153.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 19731.4 N 19027.6 U 138.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 19731.4 N 19027.6 U 129.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 19731.4 N 19027.6 U 153.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 19731.4 N 19392.4 U 138.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 19731.4 N 19392.4 U 129.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 19731.4 N 19392.4 U 153.7

NEW SUBE /204_PU_008_SERVICE_DETAILS
-- Reference Value: stock-duty casing clean-out cover
NEW CYLI
DIAM 91.8
HEIG 12.0
ORI Z IS N AND Y IS U
POS E 20547.0 N 19369.1 U 291.0

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS N AND Y IS U
POS E 20547.0 N 19379.0 U 267.1

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS N AND Y IS U
POS E 20547.0 N 19379.0 U 314.8

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS N AND Y IS U
POS E 20523.1 N 19379.0 U 291.0

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS N AND Y IS U
POS E 20570.8 N 19379.0 U 291.0


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 173 primitives.
