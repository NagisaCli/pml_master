-- ====================================================================
-- 203-PU-020 - OXYGEN STAGE FEED MC PUMP
-- ====================================================================
-- Project: JK_Pump_Build
-- Equipment: 203-PU-020
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: Excel/client coordinate = geometric centre of baseplate underside
-- Orientation: Main axis W from driver to casing; suction W; discharge U
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
-- Generated: 2026-07-29 22:54:28

NEW EQUI /203_PU_020
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_020_BASEPLATE
-- PROJECT DATA: contractual rectangular baseplate; POS is its geometric centre and the coordinate is its underside centre
NEW BOX
XLEN 926.0
YLEN 760.0
ZLEN 50.0
POS E 17095.0 N 5685.0 U 25.0

NEW SUBE /203_PU_020_BASE_FASTENERS
-- Reference Value: baseplate anchor fastener A1: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 17503.0 N 6015.0 U 52.5

-- Reference Value: baseplate anchor fastener A1: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 17503.0 N 6015.0 U 51.7

-- Reference Value: baseplate anchor fastener A1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 17503.0 N 6015.0 U 58.1

-- Reference Value: baseplate anchor fastener A2: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 17503.0 N 5355.0 U 52.5

-- Reference Value: baseplate anchor fastener A2: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 17503.0 N 5355.0 U 51.7

-- Reference Value: baseplate anchor fastener A2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 17503.0 N 5355.0 U 58.1

-- Reference Value: baseplate anchor fastener A3: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 16687.0 N 6015.0 U 52.5

-- Reference Value: baseplate anchor fastener A3: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 16687.0 N 6015.0 U 51.7

-- Reference Value: baseplate anchor fastener A3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 16687.0 N 6015.0 U 58.1

-- Reference Value: baseplate anchor fastener A4: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 16687.0 N 5355.0 U 52.5

-- Reference Value: baseplate anchor fastener A4: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 16687.0 N 5355.0 U 51.7

-- Reference Value: baseplate anchor fastener A4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 16687.0 N 5355.0 U 58.1

-- Reference Value: baseplate anchor fastener A5: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 17095.0 N 6015.0 U 52.5

-- Reference Value: baseplate anchor fastener A5: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 17095.0 N 6015.0 U 51.7

-- Reference Value: baseplate anchor fastener A5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 17095.0 N 6015.0 U 58.1

-- Reference Value: baseplate anchor fastener A6: exposed threaded shank Reference Value
NEW CYLI
DIAM 15.2
HEIG 20.5
ORI Z IS U AND Y IS N
POS E 17095.0 N 5355.0 U 52.5

-- Reference Value: baseplate anchor fastener A6: solid washer under filled shank Reference Value
NEW CYLI
DIAM 32.7
HEIG 3.3
ORI Z IS U AND Y IS N
POS E 17095.0 N 5355.0 U 51.7

-- Reference Value: baseplate anchor fastener A6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.1
HEIG 9.4
ORI Z IS U AND Y IS N
POS E 17095.0 N 5355.0 U 58.1

NEW SUBE /203_PU_020_SUPPORT_FRAME
-- Reference Value: welded longitudinal skid rail -1
NEW BOX
XLEN 759.3
YLEN 60.8
ZLEN 57.0
POS E 17113.5 N 5867.4 U 78.5

-- Reference Value: welded longitudinal skid rail +1
NEW BOX
XLEN 759.3
YLEN 60.8
ZLEN 57.0
POS E 17113.5 N 5502.6 U 78.5

-- Reference Value: skid cross-member 1
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 17409.8 N 5685.0 U 69.4

-- Reference Value: skid cross-member 2
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 17095.0 N 5685.0 U 69.4

-- Reference Value: skid cross-member 3
NEW BOX
XLEN 43.8
YLEN 547.2
ZLEN 38.8
POS E 16780.2 N 5685.0 U 69.4

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 69.5
YLEN 98.8
ZLEN 57.0
POS E 16935.7 N 5821.8 U 78.5

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 69.5
YLEN 98.8
ZLEN 57.0
POS E 16935.7 N 5548.2 U 78.5

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 69.5
YLEN 98.8
ZLEN 57.0
POS E 16799.6 N 5821.8 U 78.5

-- Reference Value: integrally supported casing foot
NEW BOX
XLEN 69.5
YLEN 98.8
ZLEN 57.0
POS E 16799.6 N 5548.2 U 78.5

NEW SUBE /203_PU_020_CASING
-- Reference Value: Medium-consistency fluidizer volute back-pull-out rear plate
NEW CYLI
DIAM 301.5
HEIG 32.0
ORI Z IS W AND Y IS U
POS E 16981.0 N 5685.0 U 278.3

-- Reference Value: Medium-consistency fluidizer volute radially split casing envelope
NEW CYLI
DIAM 342.6
HEIG 154.7
ORI Z IS W AND Y IS U
POS E 16887.7 N 5685.0 U 278.3

-- Reference Value: casing split flange
NEW CYLI
DIAM 376.9
HEIG 10.0
ORI Z IS W AND Y IS U
POS E 16815.3 N 5685.0 U 278.3

-- Reference Value: Medium-consistency fluidizer volute tapered impeller-eye cover
NEW CONE
DTOP 164.5
DBOT 335.8
HEIG 80.0
ORI Z IS W AND Y IS U
POS E 16770.3 N 5685.0 U 278.3

-- Reference Value: suction-cover wear-ring boss
NEW CYLI
DIAM 178.2
HEIG 12.8
ORI Z IS W AND Y IS U
POS E 16736.7 N 5685.0 U 278.3

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 1/4
NEW CYLI
DIAM 13.7
HEIG 105.2
ORI Z IS W AND Y IS U
POS E 16887.7 N 5685.0 U 452.1

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 2/4
NEW CYLI
DIAM 13.7
HEIG 105.2
ORI Z IS W AND Y IS U
POS E 16887.7 N 5858.8 U 278.3

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 3/4
NEW CYLI
DIAM 13.7
HEIG 105.2
ORI Z IS W AND Y IS U
POS E 16887.7 N 5685.0 U 104.5

-- Reference Value: Medium-consistency fluidizer volute circumferentially distributed axial casing rib 4/4
NEW CYLI
DIAM 13.7
HEIG 105.2
ORI Z IS W AND Y IS U
POS E 16887.7 N 5511.2 U 278.3

-- Reference Value: MC fluidizer nose sleeve
NEW CYLI
DIAM 150.7
HEIG 18.0
ORI Z IS W AND Y IS U
POS E 16739.3 N 5685.0 U 278.3

NEW SUBE /203_PU_020_CASING_FASTENERS
-- Reference Value: casing split-line bolt C1: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5506.8 U 278.3

-- Reference Value: casing split-line bolt C1: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5506.8 U 278.3

-- Reference Value: casing split-line bolt C1: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5506.8 U 278.3

-- Reference Value: casing split-line bolt C2: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5540.9 U 383.0

-- Reference Value: casing split-line bolt C2: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5540.9 U 383.0

-- Reference Value: casing split-line bolt C2: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5540.9 U 383.0

-- Reference Value: casing split-line bolt C3: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5629.9 U 447.7

-- Reference Value: casing split-line bolt C3: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5629.9 U 447.7

-- Reference Value: casing split-line bolt C3: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5629.9 U 447.7

-- Reference Value: casing split-line bolt C4: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5740.1 U 447.7

-- Reference Value: casing split-line bolt C4: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5740.1 U 447.7

-- Reference Value: casing split-line bolt C4: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5740.1 U 447.7

-- Reference Value: casing split-line bolt C5: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5829.1 U 383.0

-- Reference Value: casing split-line bolt C5: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5829.1 U 383.0

-- Reference Value: casing split-line bolt C5: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5829.1 U 383.0

-- Reference Value: casing split-line bolt C6: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5863.2 U 278.3

-- Reference Value: casing split-line bolt C6: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5863.2 U 278.3

-- Reference Value: casing split-line bolt C6: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5863.2 U 278.3

-- Reference Value: casing split-line bolt C7: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5829.1 U 173.6

-- Reference Value: casing split-line bolt C7: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5829.1 U 173.6

-- Reference Value: casing split-line bolt C7: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5829.1 U 173.6

-- Reference Value: casing split-line bolt C8: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5740.1 U 108.9

-- Reference Value: casing split-line bolt C8: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5740.1 U 108.9

-- Reference Value: casing split-line bolt C8: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5740.1 U 108.9

-- Reference Value: casing split-line bolt C9: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5629.9 U 108.9

-- Reference Value: casing split-line bolt C9: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5629.9 U 108.9

-- Reference Value: casing split-line bolt C9: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5629.9 U 108.9

-- Reference Value: casing split-line bolt C10: flange-penetrating stud Reference Value
NEW CYLI
DIAM 15.4
HEIG 14.6
ORI Z IS W AND Y IS U
POS E 16805.3 N 5540.9 U 173.6

-- Reference Value: casing split-line bolt C10: flange-face washer Reference Value
NEW CYLI
DIAM 32.4
HEIG 3.4
ORI Z IS W AND Y IS U
POS E 16808.6 N 5540.9 U 173.6

-- Reference Value: casing split-line bolt C10: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 26.5
HEIG 8.9
ORI Z IS W AND Y IS U
POS E 16802.5 N 5540.9 U 173.6

NEW SUBE /203_PU_020_BEARING_FRAME
-- Reference Value: stepped bearing bracket section 1
NEW CYLI
DIAM 78.8
HEIG 17.6
ORI Z IS W AND Y IS U
POS E 17058.4 N 5685.0 U 278.3

-- Reference Value: stepped bearing bracket section 2
NEW CYLI
DIAM 90.8
HEIG 17.6
ORI Z IS W AND Y IS U
POS E 17040.9 N 5685.0 U 278.3

-- Reference Value: stepped bearing bracket section 3
NEW CYLI
DIAM 102.8
HEIG 17.6
ORI Z IS W AND Y IS U
POS E 17023.3 N 5685.0 U 278.3

-- Reference Value: stepped bearing bracket section 4
NEW CYLI
DIAM 114.8
HEIG 17.6
ORI Z IS W AND Y IS U
POS E 17005.8 N 5685.0 U 278.3

-- Reference Value: mechanical-seal/gland housing
NEW CONE
DTOP 75.4
DBOT 109.6
HEIG 26.7
ORI Z IS W AND Y IS U
POS E 17010.3 N 5685.0 U 278.3

-- Reference Value: bearing-frame pedestal
NEW BOX
XLEN 49.2
YLEN 82.6
ZLEN 113.9
POS E 17028.6 N 5685.0 U 164.0

-- Reference Value: bearing grease/oil fill cap
NEW CYLI
DIAM 20.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 17027.9 N 5685.0 U 345.7

NEW SUBE /203_PU_020_SUCTION
-- Reference Value: suction DN150; POS is flange face, contractual direction W
NEW NOZZLE /203_PU_020_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 16580.3 N 5685.0 U 278.3
ORI P1 IS W
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_020_DISCHARGE
-- Reference Value: integrally cast discharge-neck boss
NEW CYLI
DIAM 135.0
HEIG 28.0
ORI Z IS U AND Y IS N
POS E 16863.7 N 5685.0 U 453.8

-- Reference Value: discharge DN100; POS is flange face, contractual direction U
NEW NOZZLE /203_PU_020_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 16863.7 N 5685.0 U 599.6
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_020_COUPLING
-- Reference Value: exposed common shaft between driver and pump
NEW CYLI
DIAM 25.7
HEIG 64.8
ORI Z IS W AND Y IS U
POS E 17099.6 N 5685.0 U 278.3

-- Reference Value: motor-side flexible-coupling hub
NEW CYLI
DIAM 55.2
HEIG 16.2
ORI Z IS W AND Y IS U
POS E 17123.9 N 5685.0 U 278.3

-- Reference Value: pump-side flexible-coupling hub
NEW CYLI
DIAM 55.2
HEIG 16.2
ORI Z IS W AND Y IS U
POS E 17075.3 N 5685.0 U 278.3

-- Reference Value: elastomeric flexible-coupling element
NEW CYLI
DIAM 65.2
HEIG 28.0
ORI Z IS W AND Y IS U
POS E 17099.6 N 5685.0 U 278.3

-- Reference Value: ventilated guard cage rail 1
NEW CYLI
DIAM 10.0
HEIG 64.8
ORI Z IS W AND Y IS U
POS E 17099.6 N 5632.9 U 278.3

-- Reference Value: ventilated guard cage rail 2
NEW CYLI
DIAM 10.0
HEIG 64.8
ORI Z IS W AND Y IS U
POS E 17099.6 N 5648.2 U 315.1

-- Reference Value: ventilated guard cage rail 3
NEW CYLI
DIAM 10.0
HEIG 64.8
ORI Z IS W AND Y IS U
POS E 17099.6 N 5685.0 U 330.4

-- Reference Value: ventilated guard cage rail 4
NEW CYLI
DIAM 10.0
HEIG 64.8
ORI Z IS W AND Y IS U
POS E 17099.6 N 5721.8 U 315.1

-- Reference Value: ventilated guard cage rail 5
NEW CYLI
DIAM 10.0
HEIG 64.8
ORI Z IS W AND Y IS U
POS E 17099.6 N 5737.1 U 278.3

-- Reference Value: ventilated guard cage rail 6
NEW CYLI
DIAM 10.0
HEIG 64.8
ORI Z IS W AND Y IS U
POS E 17099.6 N 5721.8 U 241.5

-- Reference Value: ventilated guard cage rail 7
NEW CYLI
DIAM 10.0
HEIG 64.8
ORI Z IS W AND Y IS U
POS E 17099.6 N 5685.0 U 226.2

-- Reference Value: ventilated guard cage rail 8
NEW CYLI
DIAM 10.0
HEIG 64.8
ORI Z IS W AND Y IS U
POS E 17099.6 N 5648.2 U 241.5

-- Reference Value: ventilated guard end horizontal brace 1
NEW BOX
XLEN 5.0
YLEN 106.8
ZLEN 10.0
POS E 17129.5 N 5685.0 U 278.3

-- Reference Value: ventilated guard end vertical brace 1
NEW BOX
XLEN 5.0
YLEN 10.0
ZLEN 106.8
POS E 17129.5 N 5685.0 U 278.3

-- Reference Value: ventilated guard end horizontal brace 2
NEW BOX
XLEN 5.0
YLEN 106.8
ZLEN 10.0
POS E 17069.7 N 5685.0 U 278.3

-- Reference Value: ventilated guard end vertical brace 2
NEW BOX
XLEN 5.0
YLEN 10.0
ZLEN 106.8
POS E 17069.7 N 5685.0 U 278.3

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 24.0
YLEN 80.7
ZLEN 106.2
POS E 17120.4 N 5685.0 U 160.1

-- Reference Value: coupling-guard support foot
NEW BOX
XLEN 24.0
YLEN 80.7
ZLEN 106.2
POS E 17078.9 N 5685.0 U 160.1

NEW SUBE /203_PU_020_DRIVER
-- Reference Value: MC-pump main drive TEFC motor fan cowl
NEW CYLI
DIAM 267.9
HEIG 63.9
ORI Z IS W AND Y IS U
POS E 17526.1 N 5685.0 U 278.3

-- Reference Value: motor non-drive end bell
NEW CONE
DTOP 291.2
DBOT 262.1
HEIG 28.8
ORI Z IS W AND Y IS U
POS E 17508.5 N 5685.0 U 278.3

-- Reference Value: finned IEC TEFC motor stator barrel; tag profile O2_MC_COMPACT
NEW CYLI
DIAM 291.2
HEIG 328.8
ORI Z IS W AND Y IS U
POS E 17347.6 N 5685.0 U 278.3

-- Reference Value: motor drive-end bell
NEW CONE
DTOP 209.7
DBOT 291.2
HEIG 51.1
ORI Z IS W AND Y IS U
POS E 17157.6 N 5685.0 U 278.3

-- Reference Value: motor drive-end bearing cap
NEW CYLI
DIAM 110.7
HEIG 11.2
ORI Z IS W AND Y IS U
POS E 17137.7 N 5685.0 U 278.3

-- Reference Value: motor fan grille central hub
NEW CYLI
DIAM 52.4
HEIG 9.8
ORI Z IS E AND Y IS U
POS E 17553.1 N 5685.0 U 278.3

-- Reference Value: open fan-grille horizontal bar 1
NEW BOX
XLEN 7.3
YLEN 196.5
ZLEN 5.2
POS E 17554.4 N 5685.0 U 200.7

-- Reference Value: open fan-grille vertical bar 1
NEW BOX
XLEN 7.3
YLEN 5.2
ZLEN 196.5
POS E 17554.4 N 5762.6 U 278.3

-- Reference Value: open fan-grille horizontal bar 2
NEW BOX
XLEN 7.3
YLEN 238.1
ZLEN 5.2
POS E 17554.4 N 5685.0 U 239.5

-- Reference Value: open fan-grille vertical bar 2
NEW BOX
XLEN 7.3
YLEN 5.2
ZLEN 238.1
POS E 17554.4 N 5723.8 U 278.3

-- Reference Value: open fan-grille horizontal bar 3
NEW BOX
XLEN 7.3
YLEN 250.4
ZLEN 5.2
POS E 17554.4 N 5685.0 U 278.3

-- Reference Value: open fan-grille vertical bar 3
NEW BOX
XLEN 7.3
YLEN 5.2
ZLEN 250.4
POS E 17554.4 N 5685.0 U 278.3

-- Reference Value: open fan-grille horizontal bar 4
NEW BOX
XLEN 7.3
YLEN 238.1
ZLEN 5.2
POS E 17554.4 N 5685.0 U 317.1

-- Reference Value: open fan-grille vertical bar 4
NEW BOX
XLEN 7.3
YLEN 5.2
ZLEN 238.1
POS E 17554.4 N 5646.2 U 278.3

-- Reference Value: open fan-grille horizontal bar 5
NEW BOX
XLEN 7.3
YLEN 196.5
ZLEN 5.2
POS E 17554.4 N 5685.0 U 355.9

-- Reference Value: open fan-grille vertical bar 5
NEW BOX
XLEN 7.3
YLEN 5.2
ZLEN 196.5
POS E 17554.4 N 5607.4 U 278.3

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 59.6
YLEN 109.4
ZLEN 18.8
POS E 17443.0 N 5852.2 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.5
YLEN 46.0
ZLEN 73.8
POS E 17443.0 N 5828.1 U 162.8

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 59.6
YLEN 109.4
ZLEN 18.8
POS E 17443.0 N 5517.8 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.5
YLEN 46.0
ZLEN 73.8
POS E 17443.0 N 5541.9 U 162.8

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 59.6
YLEN 109.4
ZLEN 18.8
POS E 17247.0 N 5852.2 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.5
YLEN 46.0
ZLEN 73.8
POS E 17247.0 N 5828.1 U 162.8

-- Reference Value: cast motor foot mounting pad
NEW BOX
XLEN 59.6
YLEN 109.4
ZLEN 18.8
POS E 17247.0 N 5517.8 U 116.4

-- Reference Value: barrel-connected motor foot web
NEW BOX
XLEN 46.5
YLEN 46.0
ZLEN 73.8
POS E 17247.0 N 5541.9 U 162.8

-- Reference Value: 360-degree motor cooling rib 1/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5685.0 U 427.4

-- Reference Value: 360-degree motor cooling rib 2/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5749.7 U 412.7

-- Reference Value: 360-degree motor cooling rib 3/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5801.6 U 371.3

-- Reference Value: 360-degree motor cooling rib 4/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5830.4 U 311.5

-- Reference Value: 360-degree motor cooling rib 5/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5830.4 U 245.1

-- Reference Value: 360-degree motor cooling rib 6/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5801.6 U 185.3

-- Reference Value: 360-degree motor cooling rib 7/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5749.7 U 143.9

-- Reference Value: 360-degree motor cooling rib 8/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5685.0 U 129.2

-- Reference Value: 360-degree motor cooling rib 9/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5620.3 U 143.9

-- Reference Value: 360-degree motor cooling rib 10/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5568.4 U 185.3

-- Reference Value: 360-degree motor cooling rib 11/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5539.6 U 245.1

-- Reference Value: 360-degree motor cooling rib 12/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5539.6 U 311.5

-- Reference Value: 360-degree motor cooling rib 13/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5568.4 U 371.3

-- Reference Value: 360-degree motor cooling rib 14/14
NEW CYLI
DIAM 16.0
HEIG 289.4
ORI Z IS W AND Y IS U
POS E 17347.6 N 5620.3 U 412.7

-- Reference Value: MC-pump main drive stator reinforcing band 1/3
NEW CYLI
DIAM 307.2
HEIG 11.5
ORI Z IS W AND Y IS U
POS E 17429.8 N 5685.0 U 278.3

-- Reference Value: MC-pump main drive stator reinforcing band 2/3
NEW CYLI
DIAM 307.2
HEIG 11.5
ORI Z IS W AND Y IS U
POS E 17347.6 N 5685.0 U 278.3

-- Reference Value: MC-pump main drive stator reinforcing band 3/3
NEW CYLI
DIAM 307.2
HEIG 11.5
ORI Z IS W AND Y IS U
POS E 17265.4 N 5685.0 U 278.3

-- Reference Value: cast motor terminal box
NEW BOX
XLEN 115.0
YLEN 205.2
ZLEN 75.4
POS E 17362.1 N 5685.0 U 473.1

-- Reference Value: terminal-box gasketed lid
NEW BOX
XLEN 119.6
YLEN 213.4
ZLEN 9.0
POS E 17362.1 N 5685.0 U 515.3

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.9
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 17405.8 N 5758.9 U 522.4

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.9
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 17405.8 N 5611.1 U 522.4

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.9
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 17318.4 N 5758.9 U 522.4

-- Reference Value: terminal-box lid screw head
NEW CYLI
DIAM 11.9
HEIG 5.0
ORI Z IS U AND Y IS N
POS E 17318.4 N 5611.1 U 522.4

-- Reference Value: motor terminal cable gland body
NEW CYLI
DIAM 22.4
HEIG 9.1
ORI Z IS S AND Y IS U
POS E 17362.1 N 5577.8 U 469.4

-- Reference Value: motor terminal cable gland compression nut
NEW CYLI
DIAM 16.6
HEIG 10.8
ORI Z IS S AND Y IS U
POS E 17362.1 N 5567.9 U 469.4

-- Reference Value: motor lifting lug plate
NEW BOX
XLEN 36.8
YLEN 16.0
ZLEN 48.0
POS E 17268.3 N 5685.0 U 447.9

-- Reference Value: filled lifting-lug pin envelope
NEW CYLI
DIAM 21.5
HEIG 27.1
ORI Z IS S AND Y IS U
POS E 17268.3 N 5685.0 U 461.3

-- Reference Value: motor rating/nameplate
NEW BOX
XLEN 68.2
YLEN 8.2
ZLEN 41.1
POS E 17319.5 N 5832.6 U 295.8

NEW SUBE /203_PU_020_DRIVER_FASTENERS
-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 17443.0 N 5867.4 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 17443.0 N 5867.4 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 17443.0 N 5867.4 U 152.3

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 17443.0 N 5502.6 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 17443.0 N 5502.6 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 17443.0 N 5502.6 U 152.3

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 17247.0 N 5867.4 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 17247.0 N 5867.4 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 17247.0 N 5867.4 U 152.3

-- Reference Value: motor hold-down fastener: exposed threaded shank Reference Value
NEW CYLI
DIAM 16.0
HEIG 21.5
ORI Z IS U AND Y IS N
POS E 17247.0 N 5502.6 U 136.6

-- Reference Value: motor hold-down fastener: solid washer under filled shank Reference Value
NEW CYLI
DIAM 34.3
HEIG 3.5
ORI Z IS U AND Y IS N
POS E 17247.0 N 5502.6 U 127.6

-- Reference Value: motor hold-down fastener: cap/hex-head envelope Reference Value
NEW CYLI
DIAM 27.5
HEIG 9.9
ORI Z IS U AND Y IS N
POS E 17247.0 N 5502.6 U 152.3

NEW SUBE /203_PU_020_SERVICE_DETAILS
NEW SUBE /203_PU_020_MC_AUXILIARY
-- Reference Value: MC integrated air separator; structure based on project top view and official MC-pump separation descriptions
NEW CYLI
DIAM 121.6
HEIG 228.0
ORI Z IS U AND Y IS N
POS E 17076.5 N 5449.4 U 221.0

-- Reference Value: MC separator top reducer
NEW CONE
DTOP 75.4
DBOT 121.6
HEIG 36.5
ORI Z IS U AND Y IS N
POS E 17076.5 N 5449.4 U 353.2

-- Reference Value: MC separator degassing outlet
NEW CYLI
DIAM 30.0
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 17076.5 N 5449.4 U 388.6

-- Reference Value: MC degassing connection line
NEW CYLI
DIAM 35.0
HEIG 139.7
ORI Z IS S AND Y IS U
POS E 16863.7 N 5519.2 U 353.7

-- Reference Value: MC separator auxiliary motor barrel
NEW CYLI
DIAM 121.6
HEIG 120.0
ORI Z IS W AND Y IS U
POS E 17276.9 N 5449.4 U 182.4

-- Reference Value: MC auxiliary motor fan cover
NEW CYLI
DIAM 109.4
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 17348.5 N 5449.4 U 182.4

-- Reference Value: MC auxiliary motor drive-end bell
NEW CONE
DTOP 80.3
DBOT 121.6
HEIG 20.0
ORI Z IS W AND Y IS U
POS E 17213.5 N 5449.4 U 182.4

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 1/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5449.4 U 244.8

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 2/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5486.1 U 232.9

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 3/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5508.8 U 201.7

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 4/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5508.8 U 163.1

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 5/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5486.1 U 131.9

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 6/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5449.4 U 120.0

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 7/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5412.7 U 131.9

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 8/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5390.0 U 163.1

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 9/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5390.0 U 201.7

-- Reference Value: 360-degree MC auxiliary-motor cooling rib 10/10
NEW CYLI
DIAM 7.3
HEIG 103.2
ORI Z IS W AND Y IS U
POS E 17276.9 N 5412.7 U 232.9

-- Reference Value: MC auxiliary-motor terminal box
NEW BOX
XLEN 33.3
YLEN 48.6
ZLEN 20.7
POS E 17280.2 N 5449.4 U 260.8

-- Reference Value: MC auxiliary motor foot
NEW BOX
XLEN 30.0
YLEN 87.6
ZLEN 18.0
POS E 17316.9 N 5449.4 U 116.0

-- Reference Value: MC auxiliary motor foot
NEW BOX
XLEN 30.0
YLEN 87.6
ZLEN 18.0
POS E 17243.5 N 5449.4 U 116.0


-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 2 of 2 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 178 primitives.
