-- ====================================================================
-- 204-PU-006 - SECONDARY SCREEN FEED PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 204-PU-006
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis E from driver to casing; suction E; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /204_PU_006
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_006_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 1725.0
YLEN 760.0
ZLEN 50.0
POS E 20000.0 N 17410.0 U 25.0

NEW SUBE /204_PU_006_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 19232.4 N 17080.0 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 19232.4 N 17080.0 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 19232.4 N 17080.0 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 19232.4 N 17740.0 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 19232.4 N 17740.0 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 19232.4 N 17740.0 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 20767.6 N 17080.0 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 20767.6 N 17080.0 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 20767.6 N 17080.0 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 20767.6 N 17740.0 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 20767.6 N 17740.0 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 20767.6 N 17740.0 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 20000.0 N 17080.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 20000.0 N 17080.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 20000.0 N 17080.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 20000.0 N 17740.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 20000.0 N 17740.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 20000.0 N 17740.0 U 58.1

NEW SUBE /204_PU_006_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 1414.5
YLEN 60.8
ZLEN 57.0
POS E 19965.5 N 17227.6 U 78.5

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 1414.5
YLEN 60.8
ZLEN 57.0
POS E 19965.5 N 17592.4 U 78.5

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 19413.5 N 17410.0 U 69.4

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 20000.0 N 17410.0 U 69.4

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 20586.5 N 17410.0 U 69.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.4
YLEN 98.8
ZLEN 92.6
POS E 20447.4 N 17273.2 U 96.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.4
YLEN 98.8
ZLEN 92.6
POS E 20447.4 N 17546.8 U 96.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.4
YLEN 98.8
ZLEN 92.6
POS E 20628.7 N 17273.2 U 96.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.4
YLEN 98.8
ZLEN 92.6
POS E 20628.7 N 17546.8 U 96.3

NEW SUBE /204_PU_006_CASING
-- Reference Value: Stock/screen-feed open-impeller volute back-pull-out rear plate
NEW CYLI
DIAM 264.3
HEIG 35.5
ORI Z IS E AND Y IS U
POS E 20383.5 N 17410.0 U 292.7

-- Reference Value: Stock/screen-feed open-impeller volute radially split casing envelope
NEW CYLI
DIAM 300.4
HEIG 227.4
ORI Z IS E AND Y IS U
POS E 20514.9 N 17410.0 U 292.7

-- Reference Value: casing split flange
NEW CYLI
DIAM 330.4
HEIG 12.4
ORI Z IS E AND Y IS U
POS E 20622.4 N 17410.0 U 292.7

-- Reference Value: Stock/screen-feed open-impeller volute tapered impeller-eye cover
NEW CONE
DTOP 186.2
DBOT 294.3
HEIG 92.4
ORI Z IS E AND Y IS U
POS E 20674.9 N 17410.0 U 292.7

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 195.2
HEIG 14.8
ORI Z IS E AND Y IS U
POS E 20713.7 N 17410.0 U 292.7

-- Reference Value: Stock/screen-feed open-impeller volute circumferentially distributed axial casing rib 1/4
NEW CYLI
DIAM 12.0
HEIG 154.6
ORI Z IS E AND Y IS U
POS E 20514.9 N 17410.0 U 445.1

-- Reference Value: Stock/screen-feed open-impeller volute circumferentially distributed axial casing rib 2/4
NEW CYLI
DIAM 12.0
HEIG 154.6
ORI Z IS E AND Y IS U
POS E 20514.9 N 17257.7 U 292.7

-- Reference Value: Stock/screen-feed open-impeller volute circumferentially distributed axial casing rib 3/4
NEW CYLI
DIAM 12.0
HEIG 154.6
ORI Z IS E AND Y IS U
POS E 20514.9 N 17410.0 U 140.4

-- Reference Value: Stock/screen-feed open-impeller volute circumferentially distributed axial casing rib 4/4
NEW CYLI
DIAM 12.0
HEIG 154.6
ORI Z IS E AND Y IS U
POS E 20514.9 N 17562.3 U 292.7

NEW SUBE /204_PU_006_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17566.2 U 292.7

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17566.2 U 292.7

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17566.2 U 292.7

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17545.3 U 370.8

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17545.3 U 370.8

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17545.3 U 370.8

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17488.1 U 428.0

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17488.1 U 428.0

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17488.1 U 428.0

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17410.0 U 448.9

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17410.0 U 448.9

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17410.0 U 448.9

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17331.9 U 428.0

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17331.9 U 428.0

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17331.9 U 428.0

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17274.7 U 370.8

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17274.7 U 370.8

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17274.7 U 370.8

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17253.8 U 292.7

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17253.8 U 292.7

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17253.8 U 292.7

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17274.7 U 214.7

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17274.7 U 214.7

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17274.7 U 214.7

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17331.9 U 157.5

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17331.9 U 157.5

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17331.9 U 157.5

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17410.0 U 136.6

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17410.0 U 136.6

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17410.0 U 136.6

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17488.1 U 157.5

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17488.1 U 157.5

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17488.1 U 157.5

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 20632.9 N 17545.3 U 214.7

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 20630.2 N 17545.3 U 214.7

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 20635.8 N 17545.3 U 214.7

NEW SUBE /204_PU_006_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 69.1
HEIG 51.8
ORI Z IS E AND Y IS U
POS E 20184.6 N 17410.0 U 292.7

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 79.6
HEIG 51.8
ORI Z IS E AND Y IS U
POS E 20236.3 N 17410.0 U 292.7

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 90.1
HEIG 51.8
ORI Z IS E AND Y IS U
POS E 20288.1 N 17410.0 U 292.7

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 100.6
HEIG 51.8
ORI Z IS E AND Y IS U
POS E 20339.8 N 17410.0 U 292.7

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 66.1
DBOT 96.1
HEIG 35.5
ORI Z IS E AND Y IS U
POS E 20347.9 N 17410.0 U 292.7

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 144.9
YLEN 72.4
ZLEN 135.4
POS E 20272.5 N 17410.0 U 174.7

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 20274.6 N 17410.0 U 353.1

NEW SUBE /204_PU_006_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction E
NEW NOZZLE /204_PU_006_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 20928.0 N 17410.0 U 292.7
ORI P1 IS E
HEIG 207.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_006_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 20543.4 N 17410.0 U 446.5

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /204_PU_006_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 20543.4 N 17410.0 U 592.9
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_006_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 27.9
HEIG 241.5
ORI Z IS E AND Y IS U
POS E 20038.0 N 17410.0 U 292.7

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 59.9
HEIG 45.0
ORI Z IS E AND Y IS U
POS E 19939.7 N 17410.0 U 292.7

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 59.9
HEIG 45.0
ORI Z IS E AND Y IS U
POS E 20136.2 N 17410.0 U 292.7

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 70.7
HEIG 28.0
ORI Z IS E AND Y IS U
POS E 20038.0 N 17410.0 U 292.7

-- Reference Value: tapered coupling guard
NEW CONE
DTOP 141.2
DBOT 121.4
HEIG 241.5
ORI Z IS E AND Y IS U
POS E 20038.0 N 17410.0 U 292.7

-- Reference Value: coupling-guard clamp band 1
NEW CYLI
DIAM 147.5
HEIG 10.9
ORI Z IS E AND Y IS U
POS E 19922.6 N 17410.0 U 292.7

-- Reference Value: coupling-guard clamp band 2
NEW CYLI
DIAM 147.5
HEIG 10.9
ORI Z IS E AND Y IS U
POS E 20153.3 N 17410.0 U 292.7

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 29.0
YLEN 87.5
ZLEN 115.2
POS E 19960.7 N 17410.0 U 164.6

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 29.0
YLEN 87.5
ZLEN 115.2
POS E 20115.2 N 17410.0 U 164.6

NEW SUBE /204_PU_006_DRIVER
-- Reference Value: Heavy-duty high-torque motor TEFC motor fan cowl
NEW CYLI
DIAM 313.1
HEIG 97.6
ORI Z IS E AND Y IS U
POS E 19269.1 N 17410.0 U 292.7

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 319.5
DBOT 287.5
HEIG 43.9
ORI Z IS E AND Y IS U
POS E 19295.9 N 17410.0 U 292.7

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile SECONDARY_SCREEN
NEW CYLI
DIAM 319.5
HEIG 543.0
ORI Z IS E AND Y IS U
POS E 19562.1 N 17410.0 U 292.7

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 230.0
DBOT 319.5
HEIG 83.6
ORI Z IS E AND Y IS U
POS E 19875.4 N 17410.0 U 292.7

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 121.4
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 19908.2 N 17410.0 U 292.7

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 57.5
HEIG 10.8
ORI Z IS W AND Y IS U
POS E 19225.7 N 17410.0 U 292.7

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 8.0
YLEN 215.6
ZLEN 5.8
POS E 19224.3 N 17410.0 U 207.6

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 8.0
YLEN 5.8
ZLEN 215.6
POS E 19224.3 N 17324.8 U 292.7

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 8.0
YLEN 261.2
ZLEN 5.8
POS E 19224.3 N 17410.0 U 250.2

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 8.0
YLEN 5.8
ZLEN 261.2
POS E 19224.3 N 17367.4 U 292.7

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 8.0
YLEN 274.8
ZLEN 5.8
POS E 19224.3 N 17410.0 U 292.7

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 8.0
YLEN 5.8
ZLEN 274.8
POS E 19224.3 N 17410.0 U 292.7

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 8.0
YLEN 261.2
ZLEN 5.8
POS E 19224.3 N 17410.0 U 335.3

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 8.0
YLEN 5.8
ZLEN 261.2
POS E 19224.3 N 17452.6 U 292.7

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 8.0
YLEN 215.6
ZLEN 5.8
POS E 19224.3 N 17410.0 U 377.9

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 8.0
YLEN 5.8
ZLEN 215.6
POS E 19224.3 N 17495.2 U 292.7

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 97.6
YLEN 109.4
ZLEN 20.4
POS E 19408.5 N 17242.8 U 117.2

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.1
YLEN 46.0
ZLEN 64.0
POS E 19408.5 N 17266.9 U 159.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 97.6
YLEN 109.4
ZLEN 20.4
POS E 19408.5 N 17577.2 U 117.2

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.1
YLEN 46.0
ZLEN 64.0
POS E 19408.5 N 17553.1 U 159.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 97.6
YLEN 109.4
ZLEN 20.4
POS E 19729.0 N 17242.8 U 117.2

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.1
YLEN 46.0
ZLEN 64.0
POS E 19729.0 N 17266.9 U 159.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 97.6
YLEN 109.4
ZLEN 20.4
POS E 19729.0 N 17577.2 U 117.2

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.1
YLEN 46.0
ZLEN 64.0
POS E 19729.0 N 17553.1 U 159.4

-- Reference Value: 360-degree motor cooling rib 1/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17410.0 U 456.3

-- Reference Value: 360-degree motor cooling rib 2/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17354.0 U 446.5

-- Reference Value: 360-degree motor cooling rib 3/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17304.8 U 418.1

-- Reference Value: 360-degree motor cooling rib 4/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17268.3 U 374.5

-- Reference Value: 360-degree motor cooling rib 5/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17248.9 U 321.2

-- Reference Value: 360-degree motor cooling rib 6/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17248.9 U 264.3

-- Reference Value: 360-degree motor cooling rib 7/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17268.3 U 210.9

-- Reference Value: 360-degree motor cooling rib 8/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17304.8 U 167.4

-- Reference Value: 360-degree motor cooling rib 9/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17354.0 U 139.0

-- Reference Value: 360-degree motor cooling rib 10/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17410.0 U 129.1

-- Reference Value: 360-degree motor cooling rib 11/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17466.0 U 139.0

-- Reference Value: 360-degree motor cooling rib 12/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17515.2 U 167.4

-- Reference Value: 360-degree motor cooling rib 13/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17551.7 U 210.9

-- Reference Value: 360-degree motor cooling rib 14/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17571.1 U 264.3

-- Reference Value: 360-degree motor cooling rib 15/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17571.1 U 321.2

-- Reference Value: 360-degree motor cooling rib 16/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17551.7 U 374.5

-- Reference Value: 360-degree motor cooling rib 17/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17515.2 U 418.1

-- Reference Value: 360-degree motor cooling rib 18/18
NEW CYLI
DIAM 17.6
HEIG 477.9
ORI Z IS E AND Y IS U
POS E 19562.1 N 17466.0 U 446.5

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 1/2
NEW CYLI
DIAM 337.1
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 19471.6 N 17410.0 U 292.7

-- Reference Value: Heavy-duty high-torque motor stator reinforcing band 2/2
NEW CYLI
DIAM 337.1
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 19652.6 N 17410.0 U 292.7

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 195.1
YLEN 209.8
ZLEN 85.4
POS E 19540.9 N 17410.0 U 507.9

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 202.9
YLEN 218.2
ZLEN 10.3
POS E 19540.9 N 17410.0 U 555.7

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 12.1
HEIG 5.6
ORI Z IS U AND Y IS N
POS E 19466.7 N 17334.5 U 563.7

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 12.1
HEIG 5.6
ORI Z IS U AND Y IS N
POS E 19466.7 N 17485.5 U 563.7

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 12.1
HEIG 5.6
ORI Z IS U AND Y IS N
POS E 19615.0 N 17334.5 U 563.7

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 12.1
HEIG 5.6
ORI Z IS U AND Y IS N
POS E 19615.0 N 17485.5 U 563.7

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 25.4
HEIG 10.3
ORI Z IS N AND Y IS U
POS E 19540.9 N 17520.0 U 503.6

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 18.8
HEIG 12.2
ORI Z IS N AND Y IS U
POS E 19540.9 N 17531.3 U 503.6

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 62.4
YLEN 16.0
ZLEN 52.0
POS E 19694.2 N 17410.0 U 478.5

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.5
HEIG 27.1
ORI Z IS N AND Y IS U
POS E 19694.2 N 17410.0 U 493.1

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 111.5
YLEN 8.2
ZLEN 44.6
POS E 19610.6 N 17248.3 U 311.9

NEW SUBE /204_PU_006_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 19408.5 N 17227.6 U 138.2

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 19408.5 N 17227.6 U 129.2

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 19408.5 N 17227.6 U 153.9

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 19408.5 N 17592.4 U 138.2

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 19408.5 N 17592.4 U 129.2

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 19408.5 N 17592.4 U 153.9

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 19729.0 N 17227.6 U 138.2

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 19729.0 N 17227.6 U 129.2

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 19729.0 N 17227.6 U 153.9

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 19729.0 N 17592.4 U 138.2

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 19729.0 N 17592.4 U 129.2

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 19729.0 N 17592.4 U 153.9

NEW SUBE /204_PU_006_SERVICE_DETAILS
-- Reference Value: stock-duty casing clean-out cover
NEW CYLI
DIAM 90.1
HEIG 12.0
ORI Z IS N AND Y IS U
POS E 20543.4 N 17566.2 U 292.7

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS N AND Y IS U
POS E 20543.4 N 17576.1 U 269.3

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS N AND Y IS U
POS E 20543.4 N 17576.1 U 316.2

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS N AND Y IS U
POS E 20519.9 N 17576.1 U 292.7

-- Reference Value: clean-out cover bolt head
NEW CYLI
DIAM 13.6
HEIG 7.8
ORI Z IS N AND Y IS U
POS E 20566.8 N 17576.1 U 292.7


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 162 primitives.
