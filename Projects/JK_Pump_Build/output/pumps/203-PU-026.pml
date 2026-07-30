-- ====================================================================
-- 203-PU-026 - OXIDISED WL BOOSTER PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 203-PU-026
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis S from driver to casing; suction S; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /203_PU_026
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_026_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 13809.0 N 358.0 U 25.0

NEW SUBE /203_PU_026_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 13479.0 N 1123.4 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 13479.0 N 1123.4 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 13479.0 N 1123.4 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 14139.0 N 1123.4 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 14139.0 N 1123.4 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 14139.0 N 1123.4 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 13479.0 N -407.4 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 13479.0 N -407.4 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 13479.0 N -407.4 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 14139.0 N -407.4 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 14139.0 N -407.4 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 14139.0 N -407.4 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 13479.0 N 358.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 13479.0 N 358.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 13479.0 N 358.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 14139.0 N 358.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 14139.0 N 358.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 14139.0 N 358.0 U 58.1

NEW SUBE /203_PU_026_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 60.8
YLEN 1410.4
ZLEN 57.0
POS E 13626.6 N 392.4 U 78.5

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 60.8
YLEN 1410.4
ZLEN 57.0
POS E 13991.4 N 392.4 U 78.5

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 13809.0 N 942.8 U 69.4

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 13809.0 N 358.0 U 69.4

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 13809.0 N -226.8 U 69.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 104.2
POS E 13672.2 N -98.2 U 102.1

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 104.2
POS E 13945.8 N -98.2 U 102.1

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 104.2
POS E 13672.2 N -263.1 U 102.1

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 104.2
POS E 13945.8 N -263.1 U 102.1

NEW SUBE /203_PU_026_CASING
-- Reference Value: Booster/high-head volute back-pull-out rear plate
NEW CYLI
DIAM 231.3
HEIG 51.7
ORI Z IS S AND Y IS U
POS E 13809.0 N -49.7 U 285.6

-- Reference Value: Booster/high-head volute radially split casing envelope
NEW CYLI
DIAM 262.8
HEIG 187.5
ORI Z IS S AND Y IS U
POS E 13809.0 N -169.4 U 285.6

-- Reference Value: casing split flange
NEW CYLI
DIAM 279.9
HEIG 11.3
ORI Z IS S AND Y IS U
POS E 13809.0 N -257.5 U 285.6

-- Reference Value: Booster/high-head volute tapered impeller-eye cover
NEW CONE
DTOP 120.9
DBOT 257.6
HEIG 84.1
ORI Z IS S AND Y IS U
POS E 13809.0 N -305.2 U 285.6

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 131.4
HEIG 13.5
ORI Z IS S AND Y IS U
POS E 13809.0 N -340.5 U 285.6

-- Reference Value: Booster/high-head volute circumferentially distributed axial casing rib 1/3
NEW CYLI
DIAM 11.0
HEIG 127.5
ORI Z IS S AND Y IS U
POS E 13809.0 N -169.4 U 419.0

-- Reference Value: Booster/high-head volute circumferentially distributed axial casing rib 2/3
NEW CYLI
DIAM 11.0
HEIG 127.5
ORI Z IS S AND Y IS U
POS E 13693.5 N -169.4 U 218.9

-- Reference Value: Booster/high-head volute circumferentially distributed axial casing rib 3/3
NEW CYLI
DIAM 11.0
HEIG 127.5
ORI Z IS S AND Y IS U
POS E 13924.5 N -169.4 U 218.9

-- Reference Value: high-head casing reinforcement band 1
NEW CYLI
DIAM 272.0
HEIG 8.4
ORI Z IS S AND Y IS U
POS E 13809.0 N -128.6 U 285.6

-- Reference Value: high-head casing reinforcement band 2
NEW CYLI
DIAM 272.0
HEIG 8.4
ORI Z IS S AND Y IS U
POS E 13809.0 N -214.8 U 285.6

NEW SUBE /203_PU_026_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13943.4 N -267.3 U 285.6

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13943.4 N -264.7 U 285.6

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13943.4 N -270.3 U 285.6

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13917.7 N -267.3 U 364.6

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13917.7 N -264.7 U 364.6

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13917.7 N -270.3 U 364.6

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13850.5 N -267.3 U 413.4

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13850.5 N -264.7 U 413.4

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13850.5 N -270.3 U 413.4

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13767.5 N -267.3 U 413.4

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13767.5 N -264.7 U 413.4

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13767.5 N -270.3 U 413.4

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13700.3 N -267.3 U 364.6

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13700.3 N -264.7 U 364.6

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13700.3 N -270.3 U 364.6

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13674.6 N -267.3 U 285.6

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13674.6 N -264.7 U 285.6

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13674.6 N -270.3 U 285.6

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13700.3 N -267.3 U 206.6

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13700.3 N -264.7 U 206.6

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13700.3 N -270.3 U 206.6

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13767.5 N -267.3 U 157.8

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13767.5 N -264.7 U 157.8

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13767.5 N -270.3 U 157.8

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13850.5 N -267.3 U 157.8

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13850.5 N -264.7 U 157.8

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13850.5 N -270.3 U 157.8

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13917.7 N -267.3 U 206.6

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS S AND Y IS U
POS E 13917.7 N -264.7 U 206.6

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS S AND Y IS U
POS E 13917.7 N -270.3 U 206.6

NEW SUBE /203_PU_026_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 60.4
HEIG 41.3
ORI Z IS S AND Y IS U
POS E 13809.0 N 161.9 U 285.6

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 69.6
HEIG 41.3
ORI Z IS S AND Y IS U
POS E 13809.0 N 120.6 U 285.6

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 78.8
HEIG 41.3
ORI Z IS S AND Y IS U
POS E 13809.0 N 79.4 U 285.6

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 88.0
HEIG 41.3
ORI Z IS S AND Y IS U
POS E 13809.0 N 38.1 U 285.6

-- Reference Value: stepped bearing bracket section 5
NEW CYLI
DIAM 97.2
HEIG 41.3
ORI Z IS S AND Y IS U
POS E 13809.0 N -3.2 U 285.6

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 57.8
DBOT 84.1
HEIG 32.3
ORI Z IS S AND Y IS U
POS E 13809.0 N -7.7 U 285.6

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 70.0
YLEN 144.5
ZLEN 130.0
POS E 13809.0 N 69.0 U 172.0

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 13809.0 N 67.0 U 344.2

NEW SUBE /203_PU_026_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction S
NEW NOZZLE /203_PU_026_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 13809.0 N -553.6 U 285.6
ORI P1 IS S
HEIG 206.4
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_026_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 13809.0 N -185.5 U 420.6

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /203_PU_026_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 13809.0 N -185.5 U 567.0
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_026_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 26.8
HEIG 240.8
ORI Z IS S AND Y IS U
POS E 13809.0 N 303.0 U 285.6

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 57.6
HEIG 45.0
ORI Z IS S AND Y IS U
POS E 13809.0 N 400.9 U 285.6

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 57.6
HEIG 45.0
ORI Z IS S AND Y IS U
POS E 13809.0 N 205.1 U 285.6

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 68.0
HEIG 28.0
ORI Z IS S AND Y IS U
POS E 13809.0 N 303.0 U 285.6

-- Reference Value: full rounded coupling guard
NEW CYLI
DIAM 135.7
HEIG 240.8
ORI Z IS S AND Y IS U
POS E 13809.0 N 303.0 U 285.6

-- Reference Value: coupling-guard clamp band 1
NEW CYLI
DIAM 141.8
HEIG 10.8
ORI Z IS S AND Y IS U
POS E 13809.0 N 417.9 U 285.6

-- Reference Value: coupling-guard clamp band 2
NEW CYLI
DIAM 141.8
HEIG 10.8
ORI Z IS S AND Y IS U
POS E 13809.0 N 188.0 U 285.6

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 84.2
YLEN 28.9
ZLEN 110.7
POS E 13809.0 N 380.0 U 162.4

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 84.2
YLEN 28.9
ZLEN 110.7
POS E 13809.0 N 225.9 U 162.4

NEW SUBE /203_PU_026_DRIVER
-- Reference Value: Compact high-speed motor TEFC motor fan cowl
NEW CYLI
DIAM 256.3
HEIG 131.3
ORI Z IS S AND Y IS U
POS E 13809.0 N 1087.0 U 285.6

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 278.6
DBOT 250.8
HEIG 59.1
ORI Z IS S AND Y IS U
POS E 13809.0 N 1050.9 U 285.6

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile MEDIUM_BOOSTER_PUMP_CORE
NEW CYLI
DIAM 278.6
HEIG 569.1
ORI Z IS S AND Y IS U
POS E 13809.0 N 773.6 U 285.6

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 200.6
DBOT 278.6
HEIG 65.6
ORI Z IS S AND Y IS U
POS E 13809.0 N 456.2 U 285.6

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 105.9
HEIG 14.4
ORI Z IS S AND Y IS U
POS E 13809.0 N 430.6 U 285.6

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 50.2
HEIG 9.4
ORI Z IS N AND Y IS U
POS E 13809.0 N 1147.9 U 285.6

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 188.0
YLEN 7.0
ZLEN 5.0
POS E 13809.0 N 1149.2 U 211.3

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 5.0
YLEN 7.0
ZLEN 188.0
POS E 13734.7 N 1149.2 U 285.6

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 227.8
YLEN 7.0
ZLEN 5.0
POS E 13809.0 N 1149.2 U 248.5

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 5.0
YLEN 7.0
ZLEN 227.8
POS E 13771.9 N 1149.2 U 285.6

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 239.6
YLEN 7.0
ZLEN 5.0
POS E 13809.0 N 1149.2 U 285.6

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 5.0
YLEN 7.0
ZLEN 239.6
POS E 13809.0 N 1149.2 U 285.6

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 227.8
YLEN 7.0
ZLEN 5.0
POS E 13809.0 N 1149.2 U 322.7

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 5.0
YLEN 7.0
ZLEN 227.8
POS E 13846.1 N 1149.2 U 285.6

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 188.0
YLEN 7.0
ZLEN 5.0
POS E 13809.0 N 1149.2 U 359.9

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 5.0
YLEN 7.0
ZLEN 188.0
POS E 13883.3 N 1149.2 U 285.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 102.1
ZLEN 19.6
POS E 13641.8 N 955.7 U 116.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 79.6
ZLEN 91.9
POS E 13665.9 N 955.7 U 172.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 102.1
ZLEN 19.6
POS E 13976.2 N 955.7 U 116.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 79.6
ZLEN 91.9
POS E 13952.1 N 955.7 U 172.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 102.1
ZLEN 19.6
POS E 13641.8 N 620.3 U 116.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 79.6
ZLEN 91.9
POS E 13665.9 N 620.3 U 172.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 102.1
ZLEN 19.6
POS E 13976.2 N 620.3 U 116.8

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 79.6
ZLEN 91.9
POS E 13952.1 N 620.3 U 172.6

-- Reference Value: 360-degree motor cooling rib 1/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13809.0 N 773.6 U 428.3

-- Reference Value: 360-degree motor cooling rib 2/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13760.2 N 773.6 U 419.7

-- Reference Value: 360-degree motor cooling rib 3/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13717.3 N 773.6 U 394.9

-- Reference Value: 360-degree motor cooling rib 4/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13685.4 N 773.6 U 356.9

-- Reference Value: 360-degree motor cooling rib 5/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13668.5 N 773.6 U 310.4

-- Reference Value: 360-degree motor cooling rib 6/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13668.5 N 773.6 U 260.8

-- Reference Value: 360-degree motor cooling rib 7/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13685.4 N 773.6 U 214.3

-- Reference Value: 360-degree motor cooling rib 8/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13717.3 N 773.6 U 176.3

-- Reference Value: 360-degree motor cooling rib 9/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13760.2 N 773.6 U 151.5

-- Reference Value: 360-degree motor cooling rib 10/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13809.0 N 773.6 U 142.9

-- Reference Value: 360-degree motor cooling rib 11/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13857.8 N 773.6 U 151.5

-- Reference Value: 360-degree motor cooling rib 12/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13900.7 N 773.6 U 176.3

-- Reference Value: 360-degree motor cooling rib 13/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13932.6 N 773.6 U 214.3

-- Reference Value: 360-degree motor cooling rib 14/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13949.5 N 773.6 U 260.8

-- Reference Value: 360-degree motor cooling rib 15/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13949.5 N 773.6 U 310.4

-- Reference Value: 360-degree motor cooling rib 16/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13932.6 N 773.6 U 356.9

-- Reference Value: 360-degree motor cooling rib 17/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13900.7 N 773.6 U 394.9

-- Reference Value: 360-degree motor cooling rib 18/18
NEW CYLI
DIAM 15.3
HEIG 500.8
ORI Z IS S AND Y IS U
POS E 13857.8 N 773.6 U 419.7

-- Reference Value: compact high-speed motor end-frame collar 1
NEW CYLI
DIAM 288.4
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13809.0 N 994.2 U 285.6

-- Reference Value: compact high-speed motor end-frame collar 2
NEW CYLI
DIAM 288.4
HEIG 14.0
ORI Z IS S AND Y IS U
POS E 13809.0 N 561.7 U 285.6

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 159.6
YLEN 145.9
ZLEN 64.3
POS E 13809.0 N 817.2 U 468.1

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 166.0
YLEN 151.7
ZLEN 7.7
POS E 13809.0 N 817.2 U 504.1

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 13751.5 N 872.6 U 510.1

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 13866.5 N 872.6 U 510.1

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 13751.5 N 761.7 U 510.1

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 13866.5 N 761.7 U 510.1

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 19.1
HEIG 7.8
ORI Z IS E AND Y IS U
POS E 13892.7 N 817.2 U 464.9

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 14.1
HEIG 9.2
ORI Z IS E AND Y IS U
POS E 13901.2 N 817.2 U 464.9

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 16.0
YLEN 46.7
ZLEN 50.0
POS E 13809.0 N 656.7 U 449.9

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.5
HEIG 27.1
ORI Z IS E AND Y IS U
POS E 13809.0 N 656.7 U 463.9

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 8.2
YLEN 116.7
ZLEN 42.9
POS E 13667.7 N 744.2 U 302.3

NEW SUBE /203_PU_026_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 13626.6 N 955.7 U 137.4

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 13626.6 N 955.7 U 128.4

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 13626.6 N 955.7 U 153.1

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 13991.4 N 955.7 U 137.4

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 13991.4 N 955.7 U 128.4

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 13991.4 N 955.7 U 153.1

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 13626.6 N 620.3 U 137.4

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 13626.6 N 620.3 U 128.4

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 13626.6 N 620.3 U 153.1

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 13991.4 N 620.3 U 137.4

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 13991.4 N 620.3 U 128.4

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 13991.4 N 620.3 U 153.1

NEW SUBE /203_PU_026_SERVICE_DETAILS
-- Reference Value: compact pressure tapping boss
NEW CYLI
DIAM 16.0
HEIG 14.4
ORI Z IS U AND Y IS N
POS E 13809.0 N -185.5 U 413.7

-- Reference Value: booster bearing cooling rib
NEW BOX
XLEN 9.2
YLEN 103.5
ZLEN 13.1
POS E 13756.4 N -95.0 U 364.4

-- Reference Value: booster bearing cooling rib
NEW BOX
XLEN 9.2
YLEN 103.5
ZLEN 13.1
POS E 13861.6 N -95.0 U 364.4


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 156 primitives.
