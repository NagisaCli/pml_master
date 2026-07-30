-- ====================================================================
-- 204-PU-023 - POST OXYGEN DD WASHER RETURN FILTRATE PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 204-PU-023
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /204_PU_023
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_023_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1725.0
ZLEN 50.0
POS E 28520.0 N 415.0 U 25.0

NEW SUBE /204_PU_023_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 28850.0 N -352.6 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 28850.0 N -352.6 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 28850.0 N -352.6 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 28190.0 N -352.6 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 28190.0 N -352.6 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 28190.0 N -352.6 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 28850.0 N 1182.6 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 28850.0 N 1182.6 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 28850.0 N 1182.6 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 28190.0 N 1182.6 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 28190.0 N 1182.6 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 28190.0 N 1182.6 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 28850.0 N 415.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 28850.0 N 415.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 28850.0 N 415.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 28190.0 N 415.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 28190.0 N 415.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 28190.0 N 415.0 U 58.1

NEW SUBE /204_PU_023_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 60.8
YLEN 1414.5
ZLEN 57.0
POS E 28702.4 N 380.5 U 78.5

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 60.8
YLEN 1414.5
ZLEN 57.0
POS E 28337.6 N 380.5 U 78.5

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 28520.0 N -171.5 U 69.4

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 28520.0 N 415.0 U 69.4

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 28520.0 N 1001.5 U 69.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.4
ZLEN 92.7
POS E 28656.8 N 839.6 U 96.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.4
ZLEN 92.7
POS E 28383.2 N 839.6 U 96.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.4
ZLEN 92.7
POS E 28656.8 N 1008.5 U 96.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.4
ZLEN 92.7
POS E 28383.2 N 1008.5 U 96.4

NEW SUBE /204_PU_023_CASING
-- Reference Value: Filtrate-service volute back-pull-out rear plate
NEW CYLI
DIAM 238.9
HEIG 46.4
ORI Z IS N AND Y IS U
POS E 28520.0 N 786.6 U 278.5

-- Reference Value: Filtrate-service volute radially split casing envelope
NEW CYLI
DIAM 271.5
HEIG 185.5
ORI Z IS N AND Y IS U
POS E 28520.0 N 902.6 U 278.5

-- Reference Value: casing split flange
NEW CYLI
DIAM 285.0
HEIG 11.6
ORI Z IS N AND Y IS U
POS E 28520.0 N 989.5 U 278.5

-- Reference Value: Filtrate-service volute tapered impeller-eye cover
NEW CONE
DTOP 162.9
DBOT 266.0
HEIG 99.4
ORI Z IS N AND Y IS U
POS E 28520.0 N 1045.0 U 278.5

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 168.3
HEIG 15.9
ORI Z IS N AND Y IS U
POS E 28520.0 N 1086.7 U 278.5

-- Reference Value: Filtrate-service volute circumferentially distributed axial casing rib 1/2
NEW CYLI
DIAM 11.0
HEIG 126.1
ORI Z IS N AND Y IS U
POS E 28520.0 N 902.6 U 416.2

-- Reference Value: Filtrate-service volute circumferentially distributed axial casing rib 2/2
NEW CYLI
DIAM 11.0
HEIG 126.1
ORI Z IS N AND Y IS U
POS E 28520.0 N 902.6 U 140.7

NEW SUBE /204_PU_023_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 28382.2 N 999.5 U 278.5

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 28382.2 N 996.8 U 278.5

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 28382.2 N 1002.4 U 278.5

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 28422.6 N 999.5 U 375.9

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 28422.6 N 996.8 U 375.9

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 28422.6 N 1002.4 U 375.9

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 999.5 U 416.2

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 28520.0 N 996.8 U 416.2

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 28520.0 N 1002.4 U 416.2

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 28617.4 N 999.5 U 375.9

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 28617.4 N 996.8 U 375.9

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 28617.4 N 1002.4 U 375.9

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 28657.8 N 999.5 U 278.5

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 28657.8 N 996.8 U 278.5

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 28657.8 N 1002.4 U 278.5

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 28617.4 N 999.5 U 181.0

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 28617.4 N 996.8 U 181.0

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 28617.4 N 1002.4 U 181.0

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 999.5 U 140.7

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 28520.0 N 996.8 U 140.7

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 28520.0 N 1002.4 U 140.7

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 28422.6 N 999.5 U 181.0

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 28422.6 N 996.8 U 181.0

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 28422.6 N 1002.4 U 181.0

NEW SUBE /204_PU_023_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 62.4
HEIG 69.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 590.9 U 278.5

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 71.9
HEIG 69.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 659.9 U 278.5

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 81.4
HEIG 69.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 728.9 U 278.5

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 59.7
DBOT 86.9
HEIG 33.1
ORI Z IS N AND Y IS U
POS E 28520.0 N 746.9 U 278.5

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 58.6
YLEN 144.9
ZLEN 130.7
POS E 28520.0 N 670.3 U 172.4

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 28520.0 N 672.4 U 329.2

NEW SUBE /204_PU_023_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction N
NEW NOZZLE /204_PU_023_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 28520.0 N 1301.6 U 278.5
ORI P1 IS N
HEIG 207.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_023_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 28520.0 N 929.0 U 417.8

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /204_PU_023_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 28520.0 N 929.0 U 564.2
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_023_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 25.7
HEIG 241.5
ORI Z IS N AND Y IS U
POS E 28520.0 N 435.7 U 278.5

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 55.3
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 337.4 U 278.5

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 55.3
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 533.9 U 278.5

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 65.2
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 435.7 U 278.5

-- Reference Value: tapered coupling guard
NEW CONE
DTOP 130.3
DBOT 112.1
HEIG 241.5
ORI Z IS N AND Y IS U
POS E 28520.0 N 435.7 U 278.5

-- Reference Value: coupling-guard clamp band 1
NEW CYLI
DIAM 136.2
HEIG 10.9
ORI Z IS N AND Y IS U
POS E 28520.0 N 320.4 U 278.5

-- Reference Value: coupling-guard clamp band 2
NEW CYLI
DIAM 136.2
HEIG 10.9
ORI Z IS N AND Y IS U
POS E 28520.0 N 551.0 U 278.5

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 80.8
YLEN 29.0
ZLEN 106.3
POS E 28520.0 N 358.4 U 160.2

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 80.8
YLEN 29.0
ZLEN 106.3
POS E 28520.0 N 513.0 U 160.2

NEW SUBE /204_PU_023_DRIVER
-- Reference Value: IEC standard ribbed motor TEFC motor fan cowl
NEW CYLI
DIAM 258.7
HEIG 99.4
ORI Z IS N AND Y IS U
POS E 28520.0 N -297.8 U 278.5

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 281.2
DBOT 253.1
HEIG 44.7
ORI Z IS N AND Y IS U
POS E 28520.0 N -270.4 U 278.5

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile MEDIUM_FILTRATE_PUMP_CORE
NEW CYLI
DIAM 281.2
HEIG 518.0
ORI Z IS N AND Y IS U
POS E 28520.0 N -16.9 U 278.5

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 202.5
DBOT 281.2
HEIG 72.9
ORI Z IS N AND Y IS U
POS E 28520.0 N 278.5 U 278.5

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 106.9
HEIG 16.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 306.9 U 278.5

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 50.6
HEIG 9.5
ORI Z IS S AND Y IS U
POS E 28520.0 N -342.7 U 278.5

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 189.7
YLEN 7.0
ZLEN 5.1
POS E 28520.0 N -343.9 U 203.5

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 189.7
POS E 28595.0 N -343.9 U 278.5

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 229.9
YLEN 7.0
ZLEN 5.1
POS E 28520.0 N -343.9 U 241.0

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 229.9
POS E 28557.5 N -343.9 U 278.5

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 241.8
YLEN 7.0
ZLEN 5.1
POS E 28520.0 N -343.9 U 278.5

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 241.8
POS E 28520.0 N -343.9 U 278.5

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 229.9
YLEN 7.0
ZLEN 5.1
POS E 28520.0 N -343.9 U 315.9

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 229.9
POS E 28482.5 N -343.9 U 278.5

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 189.7
YLEN 7.0
ZLEN 5.1
POS E 28520.0 N -343.9 U 353.4

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 5.1
YLEN 7.0
ZLEN 189.7
POS E 28445.0 N -343.9 U 278.5

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 92.7
ZLEN 18.9
POS E 28687.2 N -168.6 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 72.3
ZLEN 83.1
POS E 28663.1 N -168.6 U 167.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 92.7
ZLEN 18.9
POS E 28352.8 N -168.6 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 72.3
ZLEN 83.1
POS E 28376.9 N -168.6 U 167.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 92.7
ZLEN 18.9
POS E 28687.2 N 136.1 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 72.3
ZLEN 83.1
POS E 28663.1 N 136.1 U 167.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 92.7
ZLEN 18.9
POS E 28352.8 N 136.1 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 72.3
ZLEN 83.1
POS E 28376.9 N 136.1 U 167.4

-- Reference Value: 360-degree motor cooling rib 1/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28520.0 N -16.9 U 422.5

-- Reference Value: 360-degree motor cooling rib 2/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28582.5 N -16.9 U 408.2

-- Reference Value: 360-degree motor cooling rib 3/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28632.6 N -16.9 U 368.2

-- Reference Value: 360-degree motor cooling rib 4/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28660.4 N -16.9 U 310.5

-- Reference Value: 360-degree motor cooling rib 5/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28660.4 N -16.9 U 246.4

-- Reference Value: 360-degree motor cooling rib 6/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28632.6 N -16.9 U 188.7

-- Reference Value: 360-degree motor cooling rib 7/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28582.5 N -16.9 U 148.7

-- Reference Value: 360-degree motor cooling rib 8/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28520.0 N -16.9 U 134.5

-- Reference Value: 360-degree motor cooling rib 9/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28457.5 N -16.9 U 148.7

-- Reference Value: 360-degree motor cooling rib 10/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28407.4 N -16.9 U 188.7

-- Reference Value: 360-degree motor cooling rib 11/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28379.6 N -16.9 U 246.4

-- Reference Value: 360-degree motor cooling rib 12/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28379.6 N -16.9 U 310.5

-- Reference Value: 360-degree motor cooling rib 13/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28407.4 N -16.9 U 368.2

-- Reference Value: 360-degree motor cooling rib 14/14
NEW CYLI
DIAM 15.5
HEIG 455.8
ORI Z IS N AND Y IS U
POS E 28457.5 N -16.9 U 408.2

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 191.5
YLEN 159.0
ZLEN 68.6
POS E 28520.0 N -42.7 U 464.5

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 199.2
YLEN 165.3
ZLEN 8.2
POS E 28520.0 N -42.7 U 502.9

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.5
ORI Z IS U AND Y IS N
POS E 28588.9 N -103.2 U 509.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.5
ORI Z IS U AND Y IS N
POS E 28451.1 N -103.2 U 509.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.5
ORI Z IS U AND Y IS N
POS E 28588.9 N 17.7 U 509.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.5
ORI Z IS U AND Y IS N
POS E 28451.1 N 17.7 U 509.3

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 20.4
HEIG 8.3
ORI Z IS W AND Y IS U
POS E 28420.1 N -42.7 U 461.0

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 15.1
HEIG 9.8
ORI Z IS W AND Y IS U
POS E 28411.0 N -42.7 U 461.0

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 16.0
YLEN 50.9
ZLEN 48.0
POS E 28520.0 N 103.0 U 443.1

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.5
HEIG 27.1
ORI Z IS W AND Y IS U
POS E 28520.0 N 103.0 U 456.5

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 8.2
YLEN 106.0
ZLEN 41.1
POS E 28662.6 N 23.5 U 295.3

NEW SUBE /204_PU_023_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 28702.4 N -168.6 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 28702.4 N -168.6 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 28702.4 N -168.6 U 152.4

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 28337.6 N -168.6 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 28337.6 N -168.6 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 28337.6 N -168.6 U 152.4

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 28702.4 N 136.1 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 28702.4 N 136.1 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 28702.4 N 136.1 U 152.4

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 28337.6 N 136.1 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 28337.6 N 136.1 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 28337.6 N 136.1 U 152.4

NEW SUBE /204_PU_023_SERVICE_DETAILS
-- Reference Value: filtrate-pump side inspection boss
NEW CYLI
DIAM 48.9
HEIG 10.0
ORI Z IS W AND Y IS U
POS E 28379.3 N 929.0 U 245.9

-- Reference Value: filtrate casing vent plug
NEW CYLI
DIAM 18.0
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 28465.7 N 929.0 U 389.6


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 138 primitives.
