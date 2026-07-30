-- ====================================================================
-- 205-PU-046 - D1 WASHER FRONT DILUTION PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 205-PU-046
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:29

NEW EQUI /205_PU_046
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_046_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 45221.0 N 14294.0 U 25.0

NEW SUBE /205_PU_046_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 45551.0 N 13528.6 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 45551.0 N 13528.6 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 45551.0 N 13528.6 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 44891.0 N 13528.6 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 44891.0 N 13528.6 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 44891.0 N 13528.6 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 45551.0 N 15059.4 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 45551.0 N 15059.4 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 45551.0 N 15059.4 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 44891.0 N 15059.4 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 44891.0 N 15059.4 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 44891.0 N 15059.4 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 45551.0 N 14294.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 45551.0 N 14294.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 45551.0 N 14294.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 44891.0 N 14294.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 44891.0 N 14294.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 44891.0 N 14294.0 U 58.1

NEW SUBE /205_PU_046_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 60.8
YLEN 1410.4
ZLEN 57.0
POS E 45403.4 N 14259.6 U 78.5

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 60.8
YLEN 1410.4
ZLEN 57.0
POS E 45038.6 N 14259.6 U 78.5

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 45221.0 N 13709.2 U 69.4

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 45221.0 N 14294.0 U 69.4

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 45221.0 N 14878.8 U 69.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 90.5
POS E 45357.8 N 14725.9 U 95.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 90.5
POS E 45084.2 N 14725.9 U 95.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 90.5
POS E 45357.8 N 14897.8 U 95.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 90.5
POS E 45084.2 N 14897.8 U 95.3

NEW SUBE /205_PU_046_CASING
-- Reference Value: General process volute back-pull-out rear plate
NEW CYLI
DIAM 249.1
HEIG 40.5
ORI Z IS N AND Y IS U
POS E 45221.0 N 14668.5 U 282.0

-- Reference Value: General process volute radially split casing envelope
NEW CYLI
DIAM 283.0
HEIG 202.3
ORI Z IS N AND Y IS U
POS E 45221.0 N 14789.9 U 282.0

-- Reference Value: casing split flange
NEW CYLI
DIAM 304.3
HEIG 11.8
ORI Z IS N AND Y IS U
POS E 45221.0 N 14885.1 U 282.0

-- Reference Value: General process volute tapered impeller-eye cover
NEW CONE
DTOP 161.3
DBOT 277.4
HEIG 94.4
ORI Z IS N AND Y IS U
POS E 45221.0 N 14938.2 U 282.0

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 169.8
HEIG 15.1
ORI Z IS N AND Y IS U
POS E 45221.0 N 14977.9 U 282.0

-- Reference Value: General process volute circumferentially distributed axial casing rib 1/2
NEW CYLI
DIAM 11.3
HEIG 137.5
ORI Z IS N AND Y IS U
POS E 45221.0 N 14789.9 U 425.6

-- Reference Value: General process volute circumferentially distributed axial casing rib 2/2
NEW CYLI
DIAM 11.3
HEIG 137.5
ORI Z IS N AND Y IS U
POS E 45221.0 N 14789.9 U 138.5

NEW SUBE /205_PU_046_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45075.6 N 14895.2 U 282.0

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45075.6 N 14892.6 U 282.0

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45075.6 N 14898.2 U 282.0

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45103.4 N 14895.2 U 367.5

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45103.4 N 14892.6 U 367.5

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45103.4 N 14898.2 U 367.5

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45176.1 N 14895.2 U 420.3

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45176.1 N 14892.6 U 420.3

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45176.1 N 14898.2 U 420.3

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45265.9 N 14895.2 U 420.3

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45265.9 N 14892.6 U 420.3

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45265.9 N 14898.2 U 420.3

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45338.6 N 14895.2 U 367.5

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45338.6 N 14892.6 U 367.5

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45338.6 N 14898.2 U 367.5

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45366.4 N 14895.2 U 282.0

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45366.4 N 14892.6 U 282.0

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45366.4 N 14898.2 U 282.0

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45338.6 N 14895.2 U 196.6

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45338.6 N 14892.6 U 196.6

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45338.6 N 14898.2 U 196.6

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45265.9 N 14895.2 U 143.7

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45265.9 N 14892.6 U 143.7

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45265.9 N 14898.2 U 143.7

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45176.1 N 14895.2 U 143.7

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45176.1 N 14892.6 U 143.7

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45176.1 N 14898.2 U 143.7

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 45103.4 N 14895.2 U 196.6

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 45103.4 N 14892.6 U 196.6

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 45103.4 N 14898.2 U 196.6

NEW SUBE /205_PU_046_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 65.1
HEIG 68.8
ORI Z IS N AND Y IS U
POS E 45221.0 N 14476.3 U 282.0

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 75.0
HEIG 68.8
ORI Z IS N AND Y IS U
POS E 45221.0 N 14545.1 U 282.0

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 84.9
HEIG 68.8
ORI Z IS N AND Y IS U
POS E 45221.0 N 14613.9 U 282.0

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 62.3
DBOT 90.6
HEIG 33.7
ORI Z IS N AND Y IS U
POS E 45221.0 N 14631.5 U 282.0

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 61.1
YLEN 144.5
ZLEN 132.6
POS E 45221.0 N 14555.4 U 173.3

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 45221.0 N 14557.5 U 334.5

NEW SUBE /205_PU_046_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction N
NEW NOZZLE /205_PU_046_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 45221.0 N 15191.8 U 282.0
ORI P1 IS N
HEIG 206.4
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_046_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 45221.0 N 14816.9 U 427.1

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /205_PU_046_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 45221.0 N 14816.9 U 573.5
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_046_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 26.3
HEIG 240.8
ORI Z IS N AND Y IS U
POS E 45221.0 N 14321.5 U 282.0

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 56.4
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 45221.0 N 14223.6 U 282.0

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 56.4
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 45221.0 N 14419.4 U 282.0

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 66.6
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 45221.0 N 14321.5 U 282.0

-- Reference Value: tapered coupling guard
NEW CONE
DTOP 133.0
DBOT 114.4
HEIG 240.8
ORI Z IS N AND Y IS U
POS E 45221.0 N 14321.5 U 282.0

-- Reference Value: coupling-guard clamp band 1
NEW CYLI
DIAM 139.0
HEIG 10.8
ORI Z IS N AND Y IS U
POS E 45221.0 N 14206.5 U 282.0

-- Reference Value: coupling-guard clamp band 2
NEW CYLI
DIAM 139.0
HEIG 10.8
ORI Z IS N AND Y IS U
POS E 45221.0 N 14436.5 U 282.0

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 82.5
YLEN 28.9
ZLEN 108.5
POS E 45221.0 N 14244.5 U 161.3

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 82.5
YLEN 28.9
ZLEN 108.5
POS E 45221.0 N 14398.6 U 161.3

NEW SUBE /205_PU_046_DRIVER
-- Reference Value: IEC standard ribbed motor TEFC motor fan cowl
NEW CYLI
DIAM 264.1
HEIG 101.1
ORI Z IS N AND Y IS U
POS E 45221.0 N 13577.4 U 282.0

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 287.0
DBOT 258.3
HEIG 45.5
ORI Z IS N AND Y IS U
POS E 45221.0 N 13605.3 U 282.0

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile D1_FRONT_DILUTION_COMPACT
NEW CYLI
DIAM 287.0
HEIG 527.3
ORI Z IS N AND Y IS U
POS E 45221.0 N 13863.3 U 282.0

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 206.7
DBOT 287.0
HEIG 74.2
ORI Z IS N AND Y IS U
POS E 45221.0 N 14164.0 U 282.0

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 109.1
HEIG 16.3
ORI Z IS N AND Y IS U
POS E 45221.0 N 14193.0 U 282.0

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 51.7
HEIG 9.7
ORI Z IS S AND Y IS U
POS E 45221.0 N 13531.7 U 282.0

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 193.7
YLEN 7.2
ZLEN 5.2
POS E 45221.0 N 13530.5 U 205.5

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 5.2
YLEN 7.2
ZLEN 193.7
POS E 45297.5 N 13530.5 U 282.0

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 234.7
YLEN 7.2
ZLEN 5.2
POS E 45221.0 N 13530.5 U 243.8

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 5.2
YLEN 7.2
ZLEN 234.7
POS E 45259.3 N 13530.5 U 282.0

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 246.9
YLEN 7.2
ZLEN 5.2
POS E 45221.0 N 13530.5 U 282.0

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 5.2
YLEN 7.2
ZLEN 246.9
POS E 45221.0 N 13530.5 U 282.0

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 234.7
YLEN 7.2
ZLEN 5.2
POS E 45221.0 N 13530.5 U 320.3

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 5.2
YLEN 7.2
ZLEN 234.7
POS E 45182.7 N 13530.5 U 282.0

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 193.7
YLEN 7.2
ZLEN 5.2
POS E 45221.0 N 13530.5 U 358.6

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 5.2
YLEN 7.2
ZLEN 193.7
POS E 45144.5 N 13530.5 U 282.0

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 94.4
ZLEN 19.3
POS E 45388.2 N 13708.9 U 116.6

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 73.6
ZLEN 80.8
POS E 45364.1 N 13708.9 U 166.7

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 94.4
ZLEN 19.3
POS E 45053.8 N 13708.9 U 116.6

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 73.6
ZLEN 80.8
POS E 45077.9 N 13708.9 U 166.7

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 94.4
ZLEN 19.3
POS E 45388.2 N 14019.1 U 116.6

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 73.6
ZLEN 80.8
POS E 45364.1 N 14019.1 U 166.7

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 94.4
ZLEN 19.3
POS E 45053.8 N 14019.1 U 116.6

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 73.6
ZLEN 80.8
POS E 45077.9 N 14019.1 U 166.7

-- Reference Value: 360-degree motor cooling rib 1/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45221.0 N 13863.3 U 429.0

-- Reference Value: 360-degree motor cooling rib 2/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45284.8 N 13863.3 U 414.5

-- Reference Value: 360-degree motor cooling rib 3/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45335.9 N 13863.3 U 373.7

-- Reference Value: 360-degree motor cooling rib 4/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45364.3 N 13863.3 U 314.7

-- Reference Value: 360-degree motor cooling rib 5/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45364.3 N 13863.3 U 249.3

-- Reference Value: 360-degree motor cooling rib 6/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45335.9 N 13863.3 U 190.4

-- Reference Value: 360-degree motor cooling rib 7/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45284.8 N 13863.3 U 149.6

-- Reference Value: 360-degree motor cooling rib 8/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45221.0 N 13863.3 U 135.0

-- Reference Value: 360-degree motor cooling rib 9/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45157.2 N 13863.3 U 149.6

-- Reference Value: 360-degree motor cooling rib 10/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45106.1 N 13863.3 U 190.4

-- Reference Value: 360-degree motor cooling rib 11/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45077.7 N 13863.3 U 249.3

-- Reference Value: 360-degree motor cooling rib 12/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45077.7 N 13863.3 U 314.7

-- Reference Value: 360-degree motor cooling rib 13/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45106.1 N 13863.3 U 373.7

-- Reference Value: 360-degree motor cooling rib 14/14
NEW CYLI
DIAM 15.8
HEIG 464.0
ORI Z IS N AND Y IS U
POS E 45157.2 N 13863.3 U 414.5

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 191.5
YLEN 161.8
ZLEN 70.0
POS E 45221.0 N 13837.0 U 471.9

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 199.2
YLEN 168.3
ZLEN 8.4
POS E 45221.0 N 13837.0 U 511.1

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 45289.9 N 13775.5 U 517.6

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 45152.1 N 13775.5 U 517.6

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 45289.9 N 13898.5 U 517.6

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 4.6
ORI Z IS U AND Y IS N
POS E 45152.1 N 13898.5 U 517.6

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 20.8
HEIG 8.5
ORI Z IS W AND Y IS U
POS E 45121.0 N 13837.0 U 468.4

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 15.4
HEIG 10.0
ORI Z IS W AND Y IS U
POS E 45111.8 N 13837.0 U 468.4

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 16.0
YLEN 51.8
ZLEN 49.0
POS E 45221.0 N 13985.4 U 450.1

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.5
HEIG 27.1
ORI Z IS W AND Y IS U
POS E 45221.0 N 13985.4 U 463.8

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 8.2
YLEN 107.9
ZLEN 42.0
POS E 45366.5 N 13904.5 U 299.3

NEW SUBE /205_PU_046_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 45403.4 N 13708.9 U 137.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 45403.4 N 13708.9 U 128.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 45403.4 N 13708.9 U 152.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 45038.6 N 13708.9 U 137.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 45038.6 N 13708.9 U 128.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 45038.6 N 13708.9 U 152.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 45403.4 N 14019.1 U 137.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 45403.4 N 14019.1 U 128.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 45403.4 N 14019.1 U 152.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 45038.6 N 14019.1 U 137.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 45038.6 N 14019.1 U 128.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 45038.6 N 14019.1 U 152.7

NEW SUBE /205_PU_046_SERVICE_DETAILS
-- Reference Value: dilution-pump vent/flush boss
NEW CYLI
DIAM 22.0
HEIG 17.6
ORI Z IS U AND Y IS N
POS E 45170.1 N 14789.9 U 409.7


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 143 primitives.
