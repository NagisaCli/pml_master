-- ====================================================================
-- 203-PU-011 - BROWN STOCK DD WASHER RETURN FILTRATE PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 203-PU-011
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /203_PU_011
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_011_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 17685.0 N 170.0 U 25.0

NEW SUBE /203_PU_011_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 18015.0 N -595.4 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 18015.0 N -595.4 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 18015.0 N -595.4 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 17355.0 N -595.4 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 17355.0 N -595.4 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 17355.0 N -595.4 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 18015.0 N 935.4 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 18015.0 N 935.4 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 18015.0 N 935.4 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 17355.0 N 935.4 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 17355.0 N 935.4 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 17355.0 N 935.4 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 18015.0 N 170.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 18015.0 N 170.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 18015.0 N 170.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 17355.0 N 170.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 17355.0 N 170.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 17355.0 N 170.0 U 58.1

NEW SUBE /203_PU_011_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 60.8
YLEN 1410.4
ZLEN 57.0
POS E 17867.4 N 135.6 U 78.5

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 60.8
YLEN 1410.4
ZLEN 57.0
POS E 17502.6 N 135.6 U 78.5

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 17685.0 N -414.8 U 69.4

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 17685.0 N 170.0 U 69.4

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 17685.0 N 754.8 U 69.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 92.7
POS E 17821.8 N 593.4 U 96.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 92.7
POS E 17548.2 N 593.4 U 96.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 92.7
POS E 17821.8 N 761.8 U 96.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 92.7
POS E 17548.2 N 761.8 U 96.4

NEW SUBE /203_PU_011_CASING
-- Reference Value: Filtrate-service volute back-pull-out rear plate
NEW CYLI
DIAM 238.9
HEIG 46.2
ORI Z IS N AND Y IS U
POS E 17685.0 N 540.6 U 278.5

-- Reference Value: Filtrate-service volute radially split casing envelope
NEW CYLI
DIAM 271.5
HEIG 184.9
ORI Z IS N AND Y IS U
POS E 17685.0 N 656.1 U 278.5

-- Reference Value: casing split flange
NEW CYLI
DIAM 285.0
HEIG 11.6
ORI Z IS N AND Y IS U
POS E 17685.0 N 742.8 U 278.5

-- Reference Value: Filtrate-service volute tapered impeller-eye cover
NEW CONE
DTOP 162.9
DBOT 266.0
HEIG 99.1
ORI Z IS N AND Y IS U
POS E 17685.0 N 798.1 U 278.5

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 168.3
HEIG 15.9
ORI Z IS N AND Y IS U
POS E 17685.0 N 839.8 U 278.5

-- Reference Value: Filtrate-service volute circumferentially distributed axial casing rib 1/2
NEW CYLI
DIAM 11.0
HEIG 125.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 656.1 U 416.2

-- Reference Value: Filtrate-service volute circumferentially distributed axial casing rib 2/2
NEW CYLI
DIAM 11.0
HEIG 125.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 656.1 U 140.7

NEW SUBE /203_PU_011_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 17547.2 N 752.8 U 278.5

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 17547.2 N 750.1 U 278.5

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 17547.2 N 755.7 U 278.5

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 17587.6 N 752.8 U 375.9

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 17587.6 N 750.1 U 375.9

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 17587.6 N 755.7 U 375.9

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 17685.0 N 752.8 U 416.2

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 17685.0 N 750.1 U 416.2

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 17685.0 N 755.7 U 416.2

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 17782.4 N 752.8 U 375.9

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 17782.4 N 750.1 U 375.9

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 17782.4 N 755.7 U 375.9

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 17822.8 N 752.8 U 278.5

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 17822.8 N 750.1 U 278.5

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 17822.8 N 755.7 U 278.5

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 17782.4 N 752.8 U 181.0

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 17782.4 N 750.1 U 181.0

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 17782.4 N 755.7 U 181.0

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 17685.0 N 752.8 U 140.7

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 17685.0 N 750.1 U 140.7

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 17685.0 N 755.7 U 140.7

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 17587.6 N 752.8 U 181.0

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 17587.6 N 750.1 U 181.0

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 17587.6 N 755.7 U 181.0

NEW SUBE /203_PU_011_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 62.4
HEIG 68.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 345.4 U 278.5

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 71.9
HEIG 68.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 414.2 U 278.5

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 81.4
HEIG 68.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 483.0 U 278.5

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 59.7
DBOT 86.9
HEIG 33.0
ORI Z IS N AND Y IS U
POS E 17685.0 N 500.9 U 278.5

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 58.6
YLEN 144.5
ZLEN 130.7
POS E 17685.0 N 424.6 U 172.4

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 17685.0 N 426.6 U 329.2

NEW SUBE /203_PU_011_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction N
NEW NOZZLE /203_PU_011_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 17685.0 N 1054.1 U 278.5
ORI P1 IS N
HEIG 206.4
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_011_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 17685.0 N 682.6 U 417.8

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /203_PU_011_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 17685.0 N 682.6 U 564.2
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_011_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 25.7
HEIG 240.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 190.6 U 278.5

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 55.3
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 17685.0 N 92.7 U 278.5

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 55.3
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 17685.0 N 288.5 U 278.5

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 65.2
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 17685.0 N 190.6 U 278.5

-- Reference Value: tapered coupling guard
NEW CONE
DTOP 130.3
DBOT 112.1
HEIG 240.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 190.6 U 278.5

-- Reference Value: coupling-guard clamp band 1
NEW CYLI
DIAM 136.2
HEIG 10.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 75.7 U 278.5

-- Reference Value: coupling-guard clamp band 2
NEW CYLI
DIAM 136.2
HEIG 10.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 305.6 U 278.5

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 80.8
YLEN 28.9
ZLEN 106.3
POS E 17685.0 N 113.6 U 160.2

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 80.8
YLEN 28.9
ZLEN 106.3
POS E 17685.0 N 267.7 U 160.2

NEW SUBE /203_PU_011_DRIVER
-- Reference Value: IEC standard ribbed motor TEFC motor fan cowl
NEW CYLI
DIAM 258.7
HEIG 99.1
ORI Z IS N AND Y IS U
POS E 17685.0 N -540.7 U 278.5

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 281.2
DBOT 253.1
HEIG 44.6
ORI Z IS N AND Y IS U
POS E 17685.0 N -513.5 U 278.5

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile MEDIUM_FILTRATE_PUMP_CORE
NEW CYLI
DIAM 281.2
HEIG 516.5
ORI Z IS N AND Y IS U
POS E 17685.0 N -260.7 U 278.5

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 202.5
DBOT 281.2
HEIG 72.7
ORI Z IS N AND Y IS U
POS E 17685.0 N 33.9 U 278.5

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 106.9
HEIG 16.0
ORI Z IS N AND Y IS U
POS E 17685.0 N 62.2 U 278.5

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 50.6
HEIG 9.5
ORI Z IS S AND Y IS U
POS E 17685.0 N -585.5 U 278.5

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 189.7
YLEN 7.0
ZLEN 5.1
POS E 17685.0 N -586.7 U 203.5

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 189.7
POS E 17760.0 N -586.7 U 278.5

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 229.9
YLEN 7.0
ZLEN 5.1
POS E 17685.0 N -586.7 U 241.0

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 229.9
POS E 17722.5 N -586.7 U 278.5

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 241.8
YLEN 7.0
ZLEN 5.1
POS E 17685.0 N -586.7 U 278.5

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 241.8
POS E 17685.0 N -586.7 U 278.5

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 229.9
YLEN 7.0
ZLEN 5.1
POS E 17685.0 N -586.7 U 315.9

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 229.9
POS E 17647.5 N -586.7 U 278.5

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 189.7
YLEN 7.0
ZLEN 5.1
POS E 17685.0 N -586.7 U 353.4

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 189.7
POS E 17610.0 N -586.7 U 278.5

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 92.5
ZLEN 18.9
POS E 17852.2 N -411.9 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 72.1
ZLEN 83.1
POS E 17828.1 N -411.9 U 167.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 92.5
ZLEN 18.9
POS E 17517.8 N -411.9 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 72.1
ZLEN 83.1
POS E 17541.9 N -411.9 U 167.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 92.5
ZLEN 18.9
POS E 17852.2 N -108.1 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 72.1
ZLEN 83.1
POS E 17828.1 N -108.1 U 167.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 92.5
ZLEN 18.9
POS E 17517.8 N -108.1 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 72.1
ZLEN 83.1
POS E 17541.9 N -108.1 U 167.4

-- Reference Value: 360-degree motor cooling rib 1/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17685.0 N -260.7 U 422.5

-- Reference Value: 360-degree motor cooling rib 2/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17747.5 N -260.7 U 408.2

-- Reference Value: 360-degree motor cooling rib 3/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17797.6 N -260.7 U 368.2

-- Reference Value: 360-degree motor cooling rib 4/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17825.4 N -260.7 U 310.5

-- Reference Value: 360-degree motor cooling rib 5/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17825.4 N -260.7 U 246.4

-- Reference Value: 360-degree motor cooling rib 6/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17797.6 N -260.7 U 188.7

-- Reference Value: 360-degree motor cooling rib 7/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17747.5 N -260.7 U 148.7

-- Reference Value: 360-degree motor cooling rib 8/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17685.0 N -260.7 U 134.5

-- Reference Value: 360-degree motor cooling rib 9/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17622.5 N -260.7 U 148.7

-- Reference Value: 360-degree motor cooling rib 10/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17572.4 N -260.7 U 188.7

-- Reference Value: 360-degree motor cooling rib 11/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17544.6 N -260.7 U 246.4

-- Reference Value: 360-degree motor cooling rib 12/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17544.6 N -260.7 U 310.5

-- Reference Value: 360-degree motor cooling rib 13/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17572.4 N -260.7 U 368.2

-- Reference Value: 360-degree motor cooling rib 14/14
NEW CYLI
DIAM 15.5
HEIG 454.5
ORI Z IS N AND Y IS U
POS E 17622.5 N -260.7 U 408.2

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 191.5
YLEN 158.5
ZLEN 68.6
POS E 17685.0 N -286.4 U 464.5

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 199.2
YLEN 164.9
ZLEN 8.2
POS E 17685.0 N -286.4 U 502.9

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.5
ORI Z IS U AND Y IS N
POS E 17753.9 N -346.7 U 509.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.5
ORI Z IS U AND Y IS N
POS E 17616.1 N -346.7 U 509.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.5
ORI Z IS U AND Y IS N
POS E 17753.9 N -226.2 U 509.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.5
ORI Z IS U AND Y IS N
POS E 17616.1 N -226.2 U 509.3

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 20.4
HEIG 8.3
ORI Z IS W AND Y IS U
POS E 17585.1 N -286.4 U 461.0

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 15.1
HEIG 9.8
ORI Z IS W AND Y IS U
POS E 17576.0 N -286.4 U 461.0

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 16.0
YLEN 50.7
ZLEN 48.0
POS E 17685.0 N -141.1 U 443.1

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.5
HEIG 27.1
ORI Z IS W AND Y IS U
POS E 17685.0 N -141.1 U 456.5

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 8.2
YLEN 105.7
ZLEN 41.1
POS E 17827.6 N -220.4 U 295.3

NEW SUBE /203_PU_011_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 17867.4 N -411.9 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 17867.4 N -411.9 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 17867.4 N -411.9 U 152.4

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 17502.6 N -411.9 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 17502.6 N -411.9 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 17502.6 N -411.9 U 152.4

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 17867.4 N -108.1 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 17867.4 N -108.1 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 17867.4 N -108.1 U 152.4

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 17502.6 N -108.1 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 17502.6 N -108.1 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 17502.6 N -108.1 U 152.4

NEW SUBE /203_PU_011_SERVICE_DETAILS
-- Reference Value: filtrate-pump side inspection boss
NEW CYLI
DIAM 48.9
HEIG 10.0
ORI Z IS W AND Y IS U
POS E 17544.3 N 682.6 U 245.9

-- Reference Value: filtrate casing vent plug
NEW CYLI
DIAM 18.0
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 17630.7 N 682.6 U 389.6


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 138 primitives.
