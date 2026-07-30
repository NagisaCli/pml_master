-- ====================================================================
-- 205-PU-049 - D1 WASHER WIRE WASH PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 205-PU-049
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis N from driver to casing; suction N; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:29

NEW EQUI /205_PU_049
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_049_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 49674.0 N 14294.0 U 25.0

NEW SUBE /205_PU_049_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 50004.0 N 13528.6 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 50004.0 N 13528.6 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 50004.0 N 13528.6 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 49344.0 N 13528.6 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 49344.0 N 13528.6 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 49344.0 N 13528.6 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 50004.0 N 15059.4 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 50004.0 N 15059.4 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 50004.0 N 15059.4 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 49344.0 N 15059.4 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 49344.0 N 15059.4 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 49344.0 N 15059.4 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 50004.0 N 14294.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 50004.0 N 14294.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 50004.0 N 14294.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 49344.0 N 14294.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 49344.0 N 14294.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 49344.0 N 14294.0 U 58.1

NEW SUBE /205_PU_049_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 60.8
YLEN 1410.4
ZLEN 57.0
POS E 49856.4 N 14259.6 U 78.5

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 60.8
YLEN 1410.4
ZLEN 57.0
POS E 49491.6 N 14259.6 U 78.5

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 49674.0 N 13709.2 U 69.4

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 49674.0 N 14294.0 U 69.4

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 547.2
YLEN 43.8
ZLEN 38.8
POS E 49674.0 N 14878.8 U 69.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 105.0
POS E 49810.8 N 14748.6 U 102.5

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 105.0
POS E 49537.2 N 14748.6 U 102.5

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 105.0
POS E 49810.8 N 14910.0 U 102.5

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 98.8
YLEN 129.0
ZLEN 105.0
POS E 49537.2 N 14910.0 U 102.5

NEW SUBE /205_PU_049_CASING
-- Reference Value: Wire-wash clean-water volute back-pull-out rear plate
NEW CYLI
DIAM 223.6
HEIG 47.5
ORI Z IS N AND Y IS U
POS E 49674.0 N 14699.6 U 282.0

-- Reference Value: Wire-wash clean-water volute radially split casing envelope
NEW CYLI
DIAM 254.1
HEIG 174.1
ORI Z IS N AND Y IS U
POS E 49674.0 N 14810.3 U 282.0

-- Reference Value: casing split flange
NEW CYLI
DIAM 264.3
HEIG 11.1
ORI Z IS N AND Y IS U
POS E 49674.0 N 14891.8 U 282.0

-- Reference Value: Wire-wash clean-water volute tapered impeller-eye cover
NEW CONE
DTOP 137.2
DBOT 249.1
HEIG 94.9
ORI Z IS N AND Y IS U
POS E 49674.0 N 14944.8 U 282.0

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 147.4
HEIG 15.2
ORI Z IS N AND Y IS U
POS E 49674.0 N 14984.7 U 282.0

-- Reference Value: Wire-wash clean-water volute circumferentially distributed axial casing rib 1/2
NEW CYLI
DIAM 11.0
HEIG 118.4
ORI Z IS N AND Y IS U
POS E 49674.0 N 14810.3 U 411.1

-- Reference Value: Wire-wash clean-water volute circumferentially distributed axial casing rib 2/2
NEW CYLI
DIAM 11.0
HEIG 118.4
ORI Z IS N AND Y IS U
POS E 49674.0 N 14810.3 U 153.0

NEW SUBE /205_PU_049_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49545.7 N 14901.6 U 282.0

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 49545.7 N 14898.9 U 282.0

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 49545.7 N 14904.5 U 282.0

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49583.2 N 14901.6 U 372.8

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 49583.2 N 14898.9 U 372.8

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 49583.2 N 14904.5 U 372.8

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49674.0 N 14901.6 U 410.4

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 49674.0 N 14898.9 U 410.4

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 49674.0 N 14904.5 U 410.4

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49764.8 N 14901.6 U 372.8

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 49764.8 N 14898.9 U 372.8

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 49764.8 N 14904.5 U 372.8

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49802.3 N 14901.6 U 282.0

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 49802.3 N 14898.9 U 282.0

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 49802.3 N 14904.5 U 282.0

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49764.8 N 14901.6 U 191.3

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 49764.8 N 14898.9 U 191.3

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 49764.8 N 14904.5 U 191.3

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49674.0 N 14901.6 U 153.7

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 49674.0 N 14898.9 U 153.7

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 49674.0 N 14904.5 U 153.7

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49583.2 N 14901.6 U 191.3

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS N AND Y IS U
POS E 49583.2 N 14898.9 U 191.3

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS N AND Y IS U
POS E 49583.2 N 14904.5 U 191.3

NEW SUBE /205_PU_049_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 58.5
HEIG 51.6
ORI Z IS N AND Y IS U
POS E 49674.0 N 14495.2 U 282.0

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 67.3
HEIG 51.6
ORI Z IS N AND Y IS U
POS E 49674.0 N 14546.8 U 282.0

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 76.2
HEIG 51.6
ORI Z IS N AND Y IS U
POS E 49674.0 N 14598.4 U 282.0

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 85.1
HEIG 51.6
ORI Z IS N AND Y IS U
POS E 49674.0 N 14650.0 U 282.0

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 55.9
DBOT 81.3
HEIG 31.6
ORI Z IS N AND Y IS U
POS E 49674.0 N 14660.0 U 282.0

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 61.3
YLEN 144.5
ZLEN 132.5
POS E 49674.0 N 14583.0 U 173.2

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 49674.0 N 14585.0 U 334.6

NEW SUBE /205_PU_049_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction N
NEW NOZZLE /205_PU_049_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 49674.0 N 15198.7 U 282.0
ORI P1 IS N
HEIG 206.4
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_049_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 49674.0 N 14834.1 U 412.7

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /205_PU_049_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 49674.0 N 14834.1 U 559.1
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_049_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 26.3
HEIG 240.8
ORI Z IS N AND Y IS U
POS E 49674.0 N 14349.0 U 282.0

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 56.4
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 49674.0 N 14251.1 U 282.0

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 56.4
HEIG 45.0
ORI Z IS N AND Y IS U
POS E 49674.0 N 14446.9 U 282.0

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 66.6
HEIG 28.0
ORI Z IS N AND Y IS U
POS E 49674.0 N 14349.0 U 282.0

-- Reference Value: full rounded coupling guard
NEW CYLI
DIAM 133.0
HEIG 240.8
ORI Z IS N AND Y IS U
POS E 49674.0 N 14349.0 U 282.0

-- Reference Value: coupling-guard clamp band 1
NEW CYLI
DIAM 139.0
HEIG 10.8
ORI Z IS N AND Y IS U
POS E 49674.0 N 14234.1 U 282.0

-- Reference Value: coupling-guard clamp band 2
NEW CYLI
DIAM 139.0
HEIG 10.8
ORI Z IS N AND Y IS U
POS E 49674.0 N 14464.0 U 282.0

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 82.5
YLEN 28.9
ZLEN 108.5
POS E 49674.0 N 14272.0 U 161.3

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 82.5
YLEN 28.9
ZLEN 108.5
POS E 49674.0 N 14426.1 U 161.3

NEW SUBE /205_PU_049_DRIVER
-- Reference Value: Compact high-speed motor TEFC motor fan cowl
NEW CYLI
DIAM 251.2
HEIG 131.3
ORI Z IS N AND Y IS U
POS E 49674.0 N 13565.0 U 282.0

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 273.0
DBOT 245.7
HEIG 59.1
ORI Z IS N AND Y IS U
POS E 49674.0 N 13601.1 U 282.0

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile MEDIUM_WIRE_WASH_PUMP_CORE
NEW CYLI
DIAM 273.0
HEIG 569.1
ORI Z IS N AND Y IS U
POS E 49674.0 N 13878.4 U 282.0

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 196.6
DBOT 273.0
HEIG 65.6
ORI Z IS N AND Y IS U
POS E 49674.0 N 14195.8 U 282.0

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 103.8
HEIG 14.4
ORI Z IS N AND Y IS U
POS E 49674.0 N 14221.4 U 282.0

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 49.1
HEIG 9.2
ORI Z IS S AND Y IS U
POS E 49674.0 N 13504.0 U 282.0

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 184.2
YLEN 6.8
ZLEN 5.0
POS E 49674.0 N 13502.8 U 209.2

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 5.0
YLEN 6.8
ZLEN 184.2
POS E 49746.8 N 13502.8 U 282.0

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 223.2
YLEN 6.8
ZLEN 5.0
POS E 49674.0 N 13502.8 U 245.6

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 5.0
YLEN 6.8
ZLEN 223.2
POS E 49710.4 N 13502.8 U 282.0

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 234.8
YLEN 6.8
ZLEN 5.0
POS E 49674.0 N 13502.8 U 282.0

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 5.0
YLEN 6.8
ZLEN 234.8
POS E 49674.0 N 13502.8 U 282.0

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 223.2
YLEN 6.8
ZLEN 5.0
POS E 49674.0 N 13502.8 U 318.4

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 5.0
YLEN 6.8
ZLEN 223.2
POS E 49637.6 N 13502.8 U 282.0

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 184.2
YLEN 6.8
ZLEN 5.0
POS E 49674.0 N 13502.8 U 354.8

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 5.0
YLEN 6.8
ZLEN 184.2
POS E 49601.2 N 13502.8 U 282.0

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 102.1
ZLEN 19.3
POS E 49841.2 N 13696.3 U 116.6

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 79.6
ZLEN 94.3
POS E 49817.1 N 13696.3 U 173.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 102.1
ZLEN 19.3
POS E 49506.8 N 13696.3 U 116.6

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 79.6
ZLEN 94.3
POS E 49530.9 N 13696.3 U 173.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 102.1
ZLEN 19.3
POS E 49841.2 N 14031.7 U 116.6

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 79.6
ZLEN 94.3
POS E 49817.1 N 14031.7 U 173.4

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 109.4
YLEN 102.1
ZLEN 19.3
POS E 49506.8 N 14031.7 U 116.6

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.0
YLEN 79.6
ZLEN 94.3
POS E 49530.9 N 14031.7 U 173.4

-- Reference Value: 360-degree motor cooling rib 1/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49674.0 N 13878.4 U 421.9

-- Reference Value: 360-degree motor cooling rib 2/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49721.8 N 13878.4 U 413.4

-- Reference Value: 360-degree motor cooling rib 3/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49763.9 N 13878.4 U 389.1

-- Reference Value: 360-degree motor cooling rib 4/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49795.1 N 13878.4 U 351.9

-- Reference Value: 360-degree motor cooling rib 5/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49811.7 N 13878.4 U 306.3

-- Reference Value: 360-degree motor cooling rib 6/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49811.7 N 13878.4 U 257.7

-- Reference Value: 360-degree motor cooling rib 7/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49795.1 N 13878.4 U 212.1

-- Reference Value: 360-degree motor cooling rib 8/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49763.9 N 13878.4 U 174.9

-- Reference Value: 360-degree motor cooling rib 9/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49721.8 N 13878.4 U 150.6

-- Reference Value: 360-degree motor cooling rib 10/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49674.0 N 13878.4 U 142.2

-- Reference Value: 360-degree motor cooling rib 11/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49626.2 N 13878.4 U 150.6

-- Reference Value: 360-degree motor cooling rib 12/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49584.1 N 13878.4 U 174.9

-- Reference Value: 360-degree motor cooling rib 13/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49552.9 N 13878.4 U 212.1

-- Reference Value: 360-degree motor cooling rib 14/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49536.3 N 13878.4 U 257.7

-- Reference Value: 360-degree motor cooling rib 15/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49536.3 N 13878.4 U 306.3

-- Reference Value: 360-degree motor cooling rib 16/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49552.9 N 13878.4 U 351.9

-- Reference Value: 360-degree motor cooling rib 17/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49584.1 N 13878.4 U 389.1

-- Reference Value: 360-degree motor cooling rib 18/18
NEW CYLI
DIAM 15.0
HEIG 500.8
ORI Z IS N AND Y IS U
POS E 49626.2 N 13878.4 U 413.4

-- Reference Value: compact high-speed motor end-frame collar 1
NEW CYLI
DIAM 282.6
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49674.0 N 13657.8 U 282.0

-- Reference Value: compact high-speed motor end-frame collar 2
NEW CYLI
DIAM 282.6
HEIG 14.0
ORI Z IS N AND Y IS U
POS E 49674.0 N 14090.3 U 282.0

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 159.6
YLEN 145.9
ZLEN 63.0
POS E 49674.0 N 13834.8 U 460.9

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 166.0
YLEN 151.7
ZLEN 7.6
POS E 49674.0 N 13834.8 U 496.2

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 49731.5 N 13779.4 U 502.0

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 49616.5 N 13779.4 U 502.0

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 49731.5 N 13890.3 U 502.0

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 9.9
HEIG 4.2
ORI Z IS U AND Y IS N
POS E 49616.5 N 13890.3 U 502.0

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 18.7
HEIG 7.6
ORI Z IS W AND Y IS U
POS E 49590.4 N 13834.8 U 457.7

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 13.9
HEIG 9.0
ORI Z IS W AND Y IS U
POS E 49582.1 N 13834.8 U 457.7

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 16.0
YLEN 46.7
ZLEN 49.0
POS E 49674.0 N 13995.3 U 443.1

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.5
HEIG 27.1
ORI Z IS W AND Y IS U
POS E 49674.0 N 13995.3 U 456.8

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 8.2
YLEN 116.7
ZLEN 42.0
POS E 49812.5 N 13907.8 U 298.4

NEW SUBE /205_PU_049_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 49856.4 N 13696.3 U 137.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 49856.4 N 13696.3 U 128.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 49856.4 N 13696.3 U 152.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 49491.6 N 13696.3 U 137.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 49491.6 N 13696.3 U 128.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 49491.6 N 13696.3 U 152.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 49856.4 N 14031.7 U 137.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 49856.4 N 14031.7 U 128.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 49856.4 N 14031.7 U 152.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 49491.6 N 14031.7 U 137.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 49491.6 N 14031.7 U 128.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 49491.6 N 14031.7 U 152.7

NEW SUBE /205_PU_049_SERVICE_DETAILS
-- Reference Value: compact pressure tapping boss
NEW CYLI
DIAM 16.0
HEIG 14.4
ORI Z IS U AND Y IS N
POS E 49674.0 N 14834.1 U 406.1


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 144 primitives.
