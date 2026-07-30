-- ====================================================================
-- 205-PU-060 - SCRUBBER CIRCULATION PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 205-PU-060
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis E from driver to casing; suction E; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:29

NEW EQUI /205_PU_060
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_060_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 1720.0
YLEN 760.0
ZLEN 50.0
POS E 46154.0 N -10854.0 U 25.0

NEW SUBE /205_PU_060_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 45388.6 N -11184.0 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 45388.6 N -11184.0 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 45388.6 N -11184.0 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 45388.6 N -10524.0 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 45388.6 N -10524.0 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 45388.6 N -10524.0 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 46919.4 N -11184.0 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 46919.4 N -11184.0 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 46919.4 N -11184.0 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 46919.4 N -10524.0 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 46919.4 N -10524.0 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 46919.4 N -10524.0 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 46154.0 N -11184.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 46154.0 N -11184.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 46154.0 N -11184.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 46154.0 N -10524.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 46154.0 N -10524.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 46154.0 N -10524.0 U 58.1

NEW SUBE /205_PU_060_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 1410.4
YLEN 60.8
ZLEN 57.0
POS E 46119.6 N -11036.4 U 78.5

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 1410.4
YLEN 60.8
ZLEN 57.0
POS E 46119.6 N -10671.6 U 78.5

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 45569.2 N -10854.0 U 69.4

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 46154.0 N -10854.0 U 69.4

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 46738.8 N -10854.0 U 69.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.0
YLEN 98.8
ZLEN 96.6
POS E 46602.8 N -10990.8 U 98.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.0
YLEN 98.8
ZLEN 96.6
POS E 46602.8 N -10717.2 U 98.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.0
YLEN 98.8
ZLEN 96.6
POS E 46781.7 N -10990.8 U 98.3

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 129.0
YLEN 98.8
ZLEN 96.6
POS E 46781.7 N -10717.2 U 98.3

NEW SUBE /205_PU_060_CASING
-- Reference Value: Chemical/scrubber circulation volute back-pull-out rear plate
NEW CYLI
DIAM 254.1
HEIG 49.1
ORI Z IS E AND Y IS U
POS E 46546.6 N -10854.0 U 291.0

-- Reference Value: Chemical/scrubber circulation volute radially split casing envelope
NEW CYLI
DIAM 288.8
HEIG 203.5
ORI Z IS E AND Y IS U
POS E 46673.0 N -10854.0 U 291.0

-- Reference Value: casing split flange
NEW CYLI
DIAM 311.9
HEIG 12.3
ORI Z IS E AND Y IS U
POS E 46768.6 N -10854.0 U 291.0

-- Reference Value: Chemical/scrubber circulation volute tapered impeller-eye cover
NEW CONE
DTOP 156.0
DBOT 283.0
HEIG 98.2
ORI Z IS E AND Y IS U
POS E 46823.8 N -10854.0 U 291.0

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 167.5
HEIG 15.7
ORI Z IS E AND Y IS U
POS E 46865.1 N -10854.0 U 291.0

-- Reference Value: Chemical/scrubber circulation volute circumferentially distributed axial casing rib 1/4
NEW CYLI
DIAM 11.6
HEIG 138.4
ORI Z IS E AND Y IS U
POS E 46673.0 N -10854.0 U 437.4

-- Reference Value: Chemical/scrubber circulation volute circumferentially distributed axial casing rib 2/4
NEW CYLI
DIAM 11.6
HEIG 138.4
ORI Z IS E AND Y IS U
POS E 46673.0 N -11000.5 U 291.0

-- Reference Value: Chemical/scrubber circulation volute circumferentially distributed axial casing rib 3/4
NEW CYLI
DIAM 11.6
HEIG 138.4
ORI Z IS E AND Y IS U
POS E 46673.0 N -10854.0 U 144.5

-- Reference Value: Chemical/scrubber circulation volute circumferentially distributed axial casing rib 4/4
NEW CYLI
DIAM 11.6
HEIG 138.4
ORI Z IS E AND Y IS U
POS E 46673.0 N -10707.5 U 291.0

-- Reference Value: chemical-duty seal collar 1
NEW CYLI
DIAM 104.0
HEIG 12.3
ORI Z IS E AND Y IS U
POS E 46515.9 N -10854.0 U 291.0

-- Reference Value: chemical-duty seal collar 2
NEW CYLI
DIAM 114.1
HEIG 12.3
ORI Z IS E AND Y IS U
POS E 46503.7 N -10854.0 U 291.0

NEW SUBE /205_PU_060_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10705.3 U 291.0

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10705.3 U 291.0

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10705.3 U 291.0

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10725.2 U 365.3

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10725.2 U 365.3

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10725.2 U 365.3

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10779.6 U 419.8

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10779.6 U 419.8

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10779.6 U 419.8

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10854.0 U 439.7

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10854.0 U 439.7

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10854.0 U 439.7

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10928.4 U 419.8

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10928.4 U 419.8

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10928.4 U 419.8

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10982.8 U 365.3

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10982.8 U 365.3

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10982.8 U 365.3

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -11002.7 U 291.0

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -11002.7 U 291.0

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -11002.7 U 291.0

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10982.8 U 216.6

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10982.8 U 216.6

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10982.8 U 216.6

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10928.4 U 162.2

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10928.4 U 162.2

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10928.4 U 162.2

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10854.0 U 142.2

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10854.0 U 142.2

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10854.0 U 142.2

-- Reference Value: casing split-line bolt C11: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10779.6 U 162.2

-- Reference Value: casing split-line bolt C11: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10779.6 U 162.2

-- Reference Value: casing split-line bolt C11: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10779.6 U 162.2

-- Reference Value: casing split-line bolt C12: flange-penetrating stud Reference Value
NEW CYLI
DIAM 14.0
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 46778.9 N -10725.2 U 216.6

-- Reference Value: casing split-line bolt C12: flange-face washer Reference Value
NEW CYLI
DIAM 29.4
HEIG 3.1
ORI Z IS E AND Y IS U
POS E 46776.3 N -10725.2 U 216.6

-- Reference Value: casing split-line bolt C12: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 24.1
HEIG 8.1
ORI Z IS E AND Y IS U
POS E 46781.9 N -10725.2 U 216.6

NEW SUBE /205_PU_060_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 66.4
HEIG 51.6
ORI Z IS E AND Y IS U
POS E 46341.5 N -10854.0 U 291.0

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 76.5
HEIG 51.6
ORI Z IS E AND Y IS U
POS E 46393.1 N -10854.0 U 291.0

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 86.6
HEIG 51.6
ORI Z IS E AND Y IS U
POS E 46444.7 N -10854.0 U 291.0

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 96.7
HEIG 51.6
ORI Z IS E AND Y IS U
POS E 46496.3 N -10854.0 U 291.0

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 63.5
DBOT 92.4
HEIG 35.1
ORI Z IS E AND Y IS U
POS E 46504.5 N -10854.0 U 291.0

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 144.5
YLEN 69.7
ZLEN 135.6
POS E 46429.2 N -10854.0 U 174.8

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 46431.3 N -10854.0 U 349.3

NEW SUBE /205_PU_060_SUCTION
-- Reference Value: suction DN80; POS is flange face, contractual direction E
NEW NOZZLE /205_PU_060_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 47079.4 N -10854.0 U 291.0
ORI P1 IS E
HEIG 206.4
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_060_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 108.0
HEIG 24.0
ORI Z IS U AND Y IS N
POS E 46697.5 N -10854.0 U 439.0

-- Reference Value: discharge DN80; POS is flange face, contractual direction U
NEW NOZZLE /205_PU_060_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 46697.5 N -10854.0 U 585.4
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_060_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 27.6
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 46195.3 N -10854.0 U 291.0

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 59.3
HEIG 45.0
ORI Z IS E AND Y IS U
POS E 46097.4 N -10854.0 U 291.0

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 59.3
HEIG 45.0
ORI Z IS E AND Y IS U
POS E 46293.2 N -10854.0 U 291.0

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 70.0
HEIG 28.0
ORI Z IS E AND Y IS U
POS E 46195.3 N -10854.0 U 291.0

-- Reference Value: ventilated guard cage rail 1
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 46195.3 N -10798.1 U 291.0

-- Reference Value: ventilated guard cage rail 2
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 46195.3 N -10814.5 U 330.5

-- Reference Value: ventilated guard cage rail 3
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 46195.3 N -10854.0 U 346.9

-- Reference Value: ventilated guard cage rail 4
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 46195.3 N -10893.5 U 330.5

-- Reference Value: ventilated guard cage rail 5
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 46195.3 N -10909.9 U 291.0

-- Reference Value: ventilated guard cage rail 6
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 46195.3 N -10893.5 U 251.4

-- Reference Value: ventilated guard cage rail 7
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 46195.3 N -10854.0 U 235.0

-- Reference Value: ventilated guard cage rail 8
NEW CYLI
DIAM 10.5
HEIG 240.8
ORI Z IS E AND Y IS U
POS E 46195.3 N -10814.5 U 251.4

-- Reference Value: ventilated guard end horizontal brace 1
NEW BOX
XLEN 10.8
YLEN 114.6
ZLEN 10.5
POS E 46080.3 N -10854.0 U 291.0

-- Reference Value: ventilated guard end vertical brace 1
NEW BOX
XLEN 10.8
YLEN 10.5
ZLEN 114.6
POS E 46080.3 N -10854.0 U 291.0

-- Reference Value: ventilated guard end horizontal brace 2
NEW BOX
XLEN 10.8
YLEN 114.6
ZLEN 10.5
POS E 46310.3 N -10854.0 U 291.0

-- Reference Value: ventilated guard end vertical brace 2
NEW BOX
XLEN 10.8
YLEN 10.5
ZLEN 114.6
POS E 46310.3 N -10854.0 U 291.0

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 28.9
YLEN 86.7
ZLEN 114.1
POS E 46118.2 N -10854.0 U 164.0

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 28.9
YLEN 86.7
ZLEN 114.1
POS E 46272.3 N -10854.0 U 164.0

NEW SUBE /205_PU_060_DRIVER
-- Reference Value: Chemical-duty sealed motor TEFC motor fan cowl
NEW CYLI
DIAM 274.2
HEIG 112.3
ORI Z IS E AND Y IS U
POS E 45429.3 N -10854.0 U 291.0

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 298.0
DBOT 268.2
HEIG 50.5
ORI Z IS E AND Y IS U
POS E 45460.1 N -10854.0 U 291.0

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile MATCHED_SCRUBBER_CIRCULATION_CORE
NEW CYLI
DIAM 298.0
HEIG 529.7
ORI Z IS E AND Y IS U
POS E 45718.8 N -10854.0 U 291.0

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 214.6
DBOT 298.0
HEIG 91.2
ORI Z IS E AND Y IS U
POS E 46029.3 N -10854.0 U 291.0

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 113.2
HEIG 18.0
ORI Z IS E AND Y IS U
POS E 46065.9 N -10854.0 U 291.0

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 53.6
HEIG 10.1
ORI Z IS W AND Y IS U
POS E 45378.1 N -10854.0 U 291.0

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 7.5
YLEN 201.1
ZLEN 5.4
POS E 45376.8 N -10854.0 U 211.5

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 7.5
YLEN 5.4
ZLEN 201.1
POS E 45376.8 N -10933.4 U 291.0

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 7.5
YLEN 243.7
ZLEN 5.4
POS E 45376.8 N -10854.0 U 251.2

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 7.5
YLEN 5.4
ZLEN 243.7
POS E 45376.8 N -10893.7 U 291.0

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 7.5
YLEN 256.3
ZLEN 5.4
POS E 45376.8 N -10854.0 U 291.0

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 7.5
YLEN 5.4
ZLEN 256.3
POS E 45376.8 N -10854.0 U 291.0

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 7.5
YLEN 243.7
ZLEN 5.4
POS E 45376.8 N -10854.0 U 330.7

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 7.5
YLEN 5.4
ZLEN 243.7
POS E 45376.8 N -10814.3 U 291.0

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 7.5
YLEN 201.1
ZLEN 5.4
POS E 45376.8 N -10854.0 U 370.4

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 7.5
YLEN 5.4
ZLEN 201.1
POS E 45376.8 N -10774.6 U 291.0

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 98.2
YLEN 109.4
ZLEN 20.2
POS E 45562.6 N -11021.2 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.6
YLEN 46.0
ZLEN 79.3
POS E 45562.6 N -10997.1 U 166.9

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 98.2
YLEN 109.4
ZLEN 20.2
POS E 45562.6 N -10686.8 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.6
YLEN 46.0
ZLEN 79.3
POS E 45562.6 N -10710.9 U 166.9

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 98.2
YLEN 109.4
ZLEN 20.2
POS E 45885.4 N -11021.2 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.6
YLEN 46.0
ZLEN 79.3
POS E 45885.4 N -10997.1 U 166.9

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 98.2
YLEN 109.4
ZLEN 20.2
POS E 45885.4 N -10686.8 U 117.1

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 76.6
YLEN 46.0
ZLEN 79.3
POS E 45885.4 N -10710.9 U 166.9

-- Reference Value: 360-degree motor cooling rib 1/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10854.0 U 443.6

-- Reference Value: 360-degree motor cooling rib 2/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10906.2 U 434.4

-- Reference Value: 360-degree motor cooling rib 3/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10952.1 U 407.9

-- Reference Value: 360-degree motor cooling rib 4/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10986.2 U 367.3

-- Reference Value: 360-degree motor cooling rib 5/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -11004.3 U 317.5

-- Reference Value: 360-degree motor cooling rib 6/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -11004.3 U 264.5

-- Reference Value: 360-degree motor cooling rib 7/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10986.2 U 214.7

-- Reference Value: 360-degree motor cooling rib 8/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10952.1 U 174.1

-- Reference Value: 360-degree motor cooling rib 9/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10906.2 U 147.5

-- Reference Value: 360-degree motor cooling rib 10/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10854.0 U 138.3

-- Reference Value: 360-degree motor cooling rib 11/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10801.8 U 147.5

-- Reference Value: 360-degree motor cooling rib 12/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10755.9 U 174.1

-- Reference Value: 360-degree motor cooling rib 13/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10721.8 U 214.7

-- Reference Value: 360-degree motor cooling rib 14/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10703.7 U 264.5

-- Reference Value: 360-degree motor cooling rib 15/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10703.7 U 317.5

-- Reference Value: 360-degree motor cooling rib 16/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10721.8 U 367.3

-- Reference Value: 360-degree motor cooling rib 17/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10755.9 U 407.9

-- Reference Value: 360-degree motor cooling rib 18/18
NEW CYLI
DIAM 16.4
HEIG 466.1
ORI Z IS E AND Y IS U
POS E 45718.8 N -10801.8 U 434.4

-- Reference Value: chemical-duty sealed drive-end collar
NEW CYLI
DIAM 226.5
HEIG 14.0
ORI Z IS E AND Y IS U
POS E 45976.7 N -10854.0 U 291.0

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 175.4
YLEN 191.5
ZLEN 88.3
POS E 45695.9 N -10854.0 U 495.9

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 182.5
YLEN 199.2
ZLEN 10.6
POS E 45695.9 N -10854.0 U 545.4

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 5.8
ORI Z IS U AND Y IS N
POS E 45629.3 N -10922.9 U 553.6

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 5.8
ORI Z IS U AND Y IS N
POS E 45629.3 N -10785.1 U 553.6

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 5.8
ORI Z IS U AND Y IS N
POS E 45762.6 N -10922.9 U 553.6

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.1
HEIG 5.8
ORI Z IS U AND Y IS N
POS E 45762.6 N -10785.1 U 553.6

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 26.2
HEIG 10.7
ORI Z IS N AND Y IS U
POS E 45695.9 N -10752.9 U 491.5

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 19.4
HEIG 12.6
ORI Z IS N AND Y IS U
POS E 45695.9 N -10741.2 U 491.5

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 56.1
YLEN 16.0
ZLEN 51.5
POS E 45850.3 N -10854.0 U 465.7

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.5
HEIG 27.1
ORI Z IS N AND Y IS U
POS E 45850.3 N -10854.0 U 480.1

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 112.3
YLEN 8.2
ZLEN 44.1
POS E 45766.1 N -11005.0 U 308.8

NEW SUBE /205_PU_060_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 45562.6 N -11036.4 U 138.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 45562.6 N -11036.4 U 129.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 45562.6 N -11036.4 U 153.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 45562.6 N -10671.6 U 138.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 45562.6 N -10671.6 U 129.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 45562.6 N -10671.6 U 153.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 45885.4 N -11036.4 U 138.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 45885.4 N -11036.4 U 129.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 45885.4 N -11036.4 U 153.7

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 45885.4 N -10671.6 U 138.0

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 45885.4 N -10671.6 U 129.0

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 45885.4 N -10671.6 U 153.7

NEW SUBE /205_PU_060_SERVICE_DETAILS
-- Reference Value: scrubber-pump seal-flush manifold
NEW CYLI
DIAM 18.0
HEIG 126.3
ORI Z IS E AND Y IS U
POS E 46613.3 N -10767.4 U 348.7

-- Reference Value: scrubber-pump seal splash shield
NEW BOX
XLEN 119.3
YLEN 167.5
ZLEN 13.0
POS E 46564.2 N -10854.0 U 169.7


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 169 primitives.
