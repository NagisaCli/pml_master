-- ====================================================================
-- 205-PU-032 - EOP WASHER WIRE WASH PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 205-PU-032
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:29

NEW EQUI /205_PU_032
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_032_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 765.0
YLEN 1671.0
ZLEN 50.0
POS E 39418.0 N 14294.0 U 25.0

NEW SUBE /205_PU_032_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.3
HEIG 20.7
ORI Z IS U AND Y IS N
POS E 39750.5 N 13550.4 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.9
HEIG 3.4
ORI Z IS U AND Y IS N
POS E 39750.5 N 13550.4 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.3
HEIG 9.5
ORI Z IS U AND Y IS N
POS E 39750.5 N 13550.4 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.3
HEIG 20.7
ORI Z IS U AND Y IS N
POS E 39085.5 N 13550.4 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.9
HEIG 3.4
ORI Z IS U AND Y IS N
POS E 39085.5 N 13550.4 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.3
HEIG 9.5
ORI Z IS U AND Y IS N
POS E 39085.5 N 13550.4 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.3
HEIG 20.7
ORI Z IS U AND Y IS N
POS E 39750.5 N 15037.6 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.9
HEIG 3.4
ORI Z IS U AND Y IS N
POS E 39750.5 N 15037.6 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.3
HEIG 9.5
ORI Z IS U AND Y IS N
POS E 39750.5 N 15037.6 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.3
HEIG 20.7
ORI Z IS U AND Y IS N
POS E 39085.5 N 15037.6 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.9
HEIG 3.4
ORI Z IS U AND Y IS N
POS E 39085.5 N 15037.6 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.3
HEIG 9.5
ORI Z IS U AND Y IS N
POS E 39085.5 N 15037.6 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.3
HEIG 20.7
ORI Z IS U AND Y IS N
POS E 39750.5 N 14294.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.9
HEIG 3.4
ORI Z IS U AND Y IS N
POS E 39750.5 N 14294.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.3
HEIG 9.5
ORI Z IS U AND Y IS N
POS E 39750.5 N 14294.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.3
HEIG 20.7
ORI Z IS U AND Y IS N
POS E 39085.5 N 14294.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.9
HEIG 3.4
ORI Z IS U AND Y IS N
POS E 39085.5 N 14294.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.3
HEIG 9.5
ORI Z IS U AND Y IS N
POS E 39085.5 N 14294.0 U 58.1

NEW SUBE /205_PU_032_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 61.2
YLEN 1370.2
ZLEN 57.4
POS E 39601.6 N 14260.6 U 78.7

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 61.2
YLEN 1370.2
ZLEN 57.4
POS E 39234.4 N 14260.6 U 78.7

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 550.8
YLEN 44.1
ZLEN 39.0
POS E 39418.0 N 13725.9 U 69.5

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 550.8
YLEN 44.1
ZLEN 39.0
POS E 39418.0 N 14294.0 U 69.5

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 550.8
YLEN 44.1
ZLEN 39.0
POS E 39418.0 N 14862.1 U 69.5

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 99.5
YLEN 125.3
ZLEN 105.6
POS E 39555.7 N 14735.7 U 102.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 99.5
YLEN 125.3
ZLEN 105.6
POS E 39280.3 N 14735.7 U 102.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 99.5
YLEN 125.3
ZLEN 105.6
POS E 39555.7 N 14892.5 U 102.8

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 99.5
YLEN 125.3
ZLEN 105.6
POS E 39280.3 N 14892.5 U 102.8

NEW SUBE /205_PU_032_CASING
-- Reference Value: Wire-wash clean-water volute back-pull-out rear plate
NEW CYLI
DIAM 225.1
HEIG 46.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14688.0 U 283.6

-- Reference Value: Wire-wash clean-water volute radially split casing envelope
NEW CYLI
DIAM 255.8
HEIG 169.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14795.6 U 283.6

-- Reference Value: casing split flange
NEW CYLI
DIAM 266.0
HEIG 10.8
ORI Z IS N AND Y IS U
POS E 39418.0 N 14874.8 U 283.6

-- Reference Value: Wire-wash clean-water volute tapered impeller-eye cover
NEW CONE
DTOP 138.1
DBOT 250.7
HEIG 92.2
ORI Z IS N AND Y IS U
POS E 39418.0 N 14926.3 U 283.6

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 148.4
HEIG 14.8
ORI Z IS N AND Y IS U
POS E 39418.0 N 14965.0 U 283.6

-- Reference Value: Wire-wash clean-water volute circumferentially distributed axial casing rib 1/2
NEW CYLI
DIAM 11.0
HEIG 115.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 14795.6 U 413.4

-- Reference Value: Wire-wash clean-water volute circumferentially distributed axial casing rib 2/2
NEW CYLI
DIAM 11.0
HEIG 115.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 14795.6 U 153.7

NEW SUBE /205_PU_032_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39288.8 N 14884.4 U 283.6

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 39288.8 N 14881.7 U 283.6

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 39288.8 N 14887.3 U 283.6

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39326.7 N 14884.4 U 374.9

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 39326.7 N 14881.7 U 374.9

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 39326.7 N 14887.3 U 374.9

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 14884.4 U 412.7

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14881.7 U 412.7

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14887.3 U 412.7

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39509.3 N 14884.4 U 374.9

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 39509.3 N 14881.7 U 374.9

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 39509.3 N 14887.3 U 374.9

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39547.2 N 14884.4 U 283.6

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 39547.2 N 14881.7 U 283.6

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 39547.2 N 14887.3 U 283.6

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39509.3 N 14884.4 U 192.2

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 39509.3 N 14881.7 U 192.2

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 39509.3 N 14887.3 U 192.2

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 14884.4 U 154.4

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14881.7 U 154.4

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14887.3 U 154.4

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39326.7 N 14884.4 U 192.2

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 39326.7 N 14881.7 U 192.2

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 39326.7 N 14887.3 U 192.2

NEW SUBE /205_PU_032_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 58.8
HEIG 50.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14489.5 U 283.6

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 67.8
HEIG 50.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14539.6 U 283.6

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 76.7
HEIG 50.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14589.8 U 283.6

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 85.7
HEIG 50.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 14639.9 U 283.6

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 56.3
DBOT 81.9
HEIG 30.7
ORI Z IS N AND Y IS U
POS E 39418.0 N 14649.6 U 283.6

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 61.7
YLEN 140.4
ZLEN 133.3
POS E 39418.0 N 14574.7 U 174.0

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 39418.0 N 14576.7 U 336.4

NEW SUBE /205_PU_032_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction N
NEW NOZZLE /205_PU_032_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 39418.0 N 15172.9 U 283.6
ORI P1 IS N
HEIG 200.5
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_032_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 39418.0 N 14818.7 U 415.1

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /205_PU_032_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 39418.0 N 14818.7 U 561.5
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_032_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 26.4
HEIG 233.9
ORI Z IS N AND Y IS U
POS E 39418.0 N 14347.5 U 283.6

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 56.8
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 14253.0 U 283.6

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 56.8
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 14441.9 U 283.6

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 67.0
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 14347.5 U 283.6

-- Reference Value: full rounded coupling guard
NEW CYLI
DIAM 133.9
HEIG 233.9
ORI Z IS N AND Y IS U
POS E 39418.0 N 14347.5 U 283.6

-- Reference Value: coupling-guard clamp band 1
NEW CYLI
DIAM 139.9
HEIG 10.5
ORI Z IS N AND Y IS U
POS E 39418.0 N 14235.8 U 283.6

-- Reference Value: coupling-guard clamp band 2
NEW CYLI
DIAM 139.9
HEIG 10.5
ORI Z IS N AND Y IS U
POS E 39418.0 N 14459.2 U 283.6

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 83.0
YLEN 28.1
ZLEN 109.2
POS E 39418.0 N 14272.6 U 162.0

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 83.0
YLEN 28.1
ZLEN 109.2
POS E 39418.0 N 14422.3 U 162.0

NEW SUBE /205_PU_032_DRIVER
-- Reference Value: Compact high-speed motor TEFC motor fan cowl
NEW CYLI
DIAM 252.9
HEIG 127.5
ORI Z IS N AND Y IS U
POS E 39418.0 N 13585.8 U 283.6

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 274.8
DBOT 247.4
HEIG 57.4
ORI Z IS N AND Y IS U
POS E 39418.0 N 13620.8 U 283.6

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile WIRE_WASH_CORE_UNCONFIRMED
NEW CYLI
DIAM 274.8
HEIG 552.9
ORI Z IS N AND Y IS U
POS E 39418.0 N 13890.3 U 283.6

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 197.9
DBOT 274.8
HEIG 63.8
ORI Z IS N AND Y IS U
POS E 39418.0 N 14198.6 U 283.6

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 104.4
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 14223.5 U 283.6

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 49.5
HEIG 9.3
ORI Z IS S AND Y IS U
POS E 39418.0 N 13526.6 U 283.6

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 185.5
YLEN 6.9
ZLEN 5.0
POS E 39418.0 N 13525.4 U 210.3

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 5.0
YLEN 6.9
ZLEN 185.5
POS E 39491.3 N 13525.4 U 283.6

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 224.7
YLEN 6.9
ZLEN 5.0
POS E 39418.0 N 13525.4 U 246.9

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 5.0
YLEN 6.9
ZLEN 224.7
POS E 39454.6 N 13525.4 U 283.6

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 236.4
YLEN 6.9
ZLEN 5.0
POS E 39418.0 N 13525.4 U 283.6

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 5.0
YLEN 6.9
ZLEN 236.4
POS E 39418.0 N 13525.4 U 283.6

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 224.7
YLEN 6.9
ZLEN 5.0
POS E 39418.0 N 13525.4 U 320.2

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 5.0
YLEN 6.9
ZLEN 224.7
POS E 39381.4 N 13525.4 U 283.6

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 185.5
YLEN 6.9
ZLEN 5.0
POS E 39418.0 N 13525.4 U 356.8

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 5.0
YLEN 6.9
ZLEN 185.5
POS E 39344.7 N 13525.4 U 283.6

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 110.2
YLEN 99.2
ZLEN 19.4
POS E 39586.3 N 13713.3 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.3
YLEN 77.4
ZLEN 95.0
POS E 39562.1 N 13713.3 U 174.2

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 110.2
YLEN 99.2
ZLEN 19.4
POS E 39249.7 N 13713.3 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.3
YLEN 77.4
ZLEN 95.0
POS E 39273.9 N 13713.3 U 174.2

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 110.2
YLEN 99.2
ZLEN 19.4
POS E 39586.3 N 14039.2 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.3
YLEN 77.4
ZLEN 95.0
POS E 39562.1 N 14039.2 U 174.2

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 110.2
YLEN 99.2
ZLEN 19.4
POS E 39249.7 N 14039.2 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.3
YLEN 77.4
ZLEN 95.0
POS E 39273.9 N 14039.2 U 174.2

-- Reference Value: 360-degree motor cooling rib 1/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39418.0 N 13890.3 U 424.3

-- Reference Value: 360-degree motor cooling rib 2/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39466.1 N 13890.3 U 415.8

-- Reference Value: 360-degree motor cooling rib 3/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39508.5 N 13890.3 U 391.4

-- Reference Value: 360-degree motor cooling rib 4/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39539.9 N 13890.3 U 353.9

-- Reference Value: 360-degree motor cooling rib 5/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39556.6 N 13890.3 U 308.0

-- Reference Value: 360-degree motor cooling rib 6/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39556.6 N 13890.3 U 259.1

-- Reference Value: 360-degree motor cooling rib 7/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39539.9 N 13890.3 U 213.2

-- Reference Value: 360-degree motor cooling rib 8/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39508.5 N 13890.3 U 175.7

-- Reference Value: 360-degree motor cooling rib 9/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39466.1 N 13890.3 U 151.3

-- Reference Value: 360-degree motor cooling rib 10/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39418.0 N 13890.3 U 142.8

-- Reference Value: 360-degree motor cooling rib 11/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39369.9 N 13890.3 U 151.3

-- Reference Value: 360-degree motor cooling rib 12/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39327.5 N 13890.3 U 175.7

-- Reference Value: 360-degree motor cooling rib 13/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39296.1 N 13890.3 U 213.2

-- Reference Value: 360-degree motor cooling rib 14/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39279.4 N 13890.3 U 259.1

-- Reference Value: 360-degree motor cooling rib 15/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39279.4 N 13890.3 U 308.0

-- Reference Value: 360-degree motor cooling rib 16/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39296.1 N 13890.3 U 353.9

-- Reference Value: 360-degree motor cooling rib 17/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39327.5 N 13890.3 U 391.4

-- Reference Value: 360-degree motor cooling rib 18/18
NEW CYLI
DIAM 15.1
HEIG 486.6
ORI Z IS N AND Y IS U
POS E 39369.9 N 13890.3 U 415.8

-- Reference Value: compact high-speed motor end-frame collar 1
NEW CYLI
DIAM 284.5
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 13676.1 U 283.6

-- Reference Value: compact high-speed motor end-frame collar 2
NEW CYLI
DIAM 284.5
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 14096.3 U 283.6

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 160.6
YLEN 141.7
ZLEN 63.4
POS E 39418.0 N 13847.9 U 463.6

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 167.1
YLEN 147.4
ZLEN 7.6
POS E 39418.0 N 13847.9 U 499.1

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 39475.8 N 13794.1 U 505.0

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 39360.2 N 13794.1 U 505.0

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 39475.8 N 13901.8 U 505.0

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 39360.2 N 13901.8 U 505.0

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 18.8
HEIG 7.7
ORI Z IS W AND Y IS U
POS E 39333.8 N 13847.9 U 460.4

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 14.0
HEIG 9.1
ORI Z IS W AND Y IS U
POS E 39325.5 N 13847.9 U 460.4

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 16.1
YLEN 45.3
ZLEN 49.3
POS E 39418.0 N 14003.8 U 445.6

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.7
HEIG 27.3
ORI Z IS W AND Y IS U
POS E 39418.0 N 14003.8 U 459.5

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 8.3
YLEN 113.4
ZLEN 42.3
POS E 39557.4 N 13918.8 U 300.0

NEW SUBE /205_PU_032_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.1
HEIG 21.7
ORI Z IS U AND Y IS N
POS E 39601.6 N 13713.3 U 137.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.5
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 39601.6 N 13713.3 U 128.5

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.6
HEIG 10.0
ORI Z IS U AND Y IS N
POS E 39601.6 N 13713.3 U 153.4

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.1
HEIG 21.7
ORI Z IS U AND Y IS N
POS E 39234.4 N 13713.3 U 137.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.5
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 39234.4 N 13713.3 U 128.5

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.6
HEIG 10.0
ORI Z IS U AND Y IS N
POS E 39234.4 N 13713.3 U 153.4

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.1
HEIG 21.7
ORI Z IS U AND Y IS N
POS E 39601.6 N 14039.2 U 137.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.5
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 39601.6 N 14039.2 U 128.5

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.6
HEIG 10.0
ORI Z IS U AND Y IS N
POS E 39601.6 N 14039.2 U 153.4

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.1
HEIG 21.7
ORI Z IS U AND Y IS N
POS E 39234.4 N 14039.2 U 137.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.5
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 39234.4 N 14039.2 U 128.5

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.6
HEIG 10.0
ORI Z IS U AND Y IS N
POS E 39234.4 N 14039.2 U 153.4

NEW SUBE /205_PU_032_SERVICE_DETAILS
-- Reference Value: compact pressure tapping boss
NEW CYLI
DIAM 16.0
HEIG 14.4
ORI Z IS U AND Y IS N
POS E 39418.0 N 14818.7 U 408.4


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 144 primitives.
