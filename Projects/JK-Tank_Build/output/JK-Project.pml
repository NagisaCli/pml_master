-- ====================================================================
-- PULP MILL - WASHING, SCREENING & BLEACHING (WSB) AREA
-- ====================================================================
-- Project: JK-Project
-- Scope: 22 tank-type equipment items
-- Units: mm
-- Frame: E = East, N = North, U = Up (elevation)
-- Datum: Each tank is positioned by its BOTTOM CENTRE POINT
-- Source: Projects/JK-Project/ equipment list + drawings
-- Generated: 2026-07-25 07:10:45
-- Execution: Select a writable ZONE in E3D, then $M <this file>


-- ====================================================================
-- 203-TA-006  BROWN STOCK WASHER FILTRATE TANK
-- ====================================================================
-- Area:        203 - Brown Stock / O2 Stage
-- Bottom centre (installation coordinate): E 15000.0  N 19860.0  U 0.0
-- Shell:       DN5600 x 9200 high
-- Closure:     Conical roof / Flat bottom
-- Support:     Ground / slab bearing
-- Volume:      197 m3

NEW EQUI /203_TA_006
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_TA_006_SHELL
-- Flat bottom plate
NEW CYLI
DIAM 5600.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 10.0

-- Shell: DN5600 x 9200
NEW CYLI
DIAM 5600.0
HEIG 9200.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 4600.0

-- Roof curb / compression ring
NEW CYLI
DIAM 5800.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 9075.0

-- Conical roof, 700 rise
NEW CONE
DTOP 300.0
DBOT 5600.0
HEIG 700.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 9550.0

-- Roof apex cap
NEW CYLI
DIAM 400.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 9930.0

NEW SUBE /203_TA_006_N1
-- N1  DN400  EL +7820  -  Stock / filtrate feed inlet
-- N1 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 15000.0 N 22675.0 U 7820.0

-- N1  DN400  EL +7820  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /203_TA_006_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 15000.0 N 23010.0 U 7820.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_006_N2
-- N2  DN400  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 15000.0 N 17045.0 U 400.0

-- N2  DN400  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /203_TA_006_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 15000.0 N 16710.0 U 400.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_006_N3
-- N3  DN200  EL +8648  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 12185.0 N 19860.0 U 8648.0

-- N3  DN200  EL +8648  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /203_TA_006_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 11950.0 N 19860.0 U 8648.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_006_N4
-- N4  DN150  EL +9200  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 16120.0 N 19860.0 U 9635.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /203_TA_006_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 16120.0 N 19860.0 U 9820.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_006_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /203_TA_006_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 17950.0 N 19860.0 U 250.0
ORI P1 IS E
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_006_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 15000.0 N 22675.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /203_TA_006_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 15000.0 N 23010.0 U 1200.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_006_ACCESS
-- Stiffening ring 1 of 2
NEW CYLI
DIAM 5840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 3166.7

-- Stiffening ring 2 of 2
NEW CYLI
DIAM 5840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 6233.3

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 8900.0
ORI Z IS U AND Y IS N
POS E 12200.0 N 20160.0 U 4750.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 8900.0
ORI Z IS U AND Y IS N
POS E 12200.0 N 19560.0 U 4750.0

-- Ladder safety cage required over the 8900 run (2 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
NEW SUBE /203_TA_006_INTERNALS
-- Agitator mounting pedestal on roof
NEW CYLI
DIAM 672.0
HEIG 400.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 10100.0

-- Agitator mounting flange
NEW CYLI
DIAM 872.0
HEIG 40.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 10320.0

-- Agitator gearbox
NEW BOX
XLEN 1200.0
YLEN 900.0
ZLEN 700.0
POS E 15000.0 N 19860.0 U 10690.0

-- Agitator drive motor
NEW CYLI
DIAM 700.0
HEIG 900.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 11490.0

-- Agitator shaft
NEW CYLI
DIAM 180.0
HEIG 8520.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 5640.0

-- Impeller hub, DN1960 swept
NEW CYLI
DIAM 324.0
HEIG 150.0
ORI Z IS U AND Y IS N
POS E 15000.0 N 19860.0 U 1731.0

-- Impeller blade E
NEW BOX
XLEN 890.0
YLEN 120.0
ZLEN 150.0
POS E 15535.0 N 19860.0 U 1731.0

-- Impeller blade N
NEW BOX
XLEN 120.0
YLEN 890.0
ZLEN 150.0
POS E 15000.0 N 20395.0 U 1731.0

-- Impeller blade W
NEW BOX
XLEN 890.0
YLEN 120.0
ZLEN 150.0
POS E 14465.0 N 19860.0 U 1731.0

-- Impeller blade S
NEW BOX
XLEN 120.0
YLEN 890.0
ZLEN 150.0
POS E 15000.0 N 19325.0 U 1731.0


-- ====================================================================
-- 203-TA-019  OXYGEN STAGE FEED TANK
-- ====================================================================
-- Area:        203 - Brown Stock / O2 Stage
-- Bottom centre (installation coordinate): E 15445.0  N 6415.0  U 0.0
-- Shell:       DN2000 x 8500 high
-- Closure:     Dished head / Dished bottom
-- Support:     Skirt support
-- Volume:      13 m3

NEW EQUI /203_TA_019
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_TA_019_SUPPORT
-- Skirt support, 1500 high to shell tangent
NEW CYLI
DIAM 2000.0
HEIG 1500.0
ORI Z IS U AND Y IS N
POS E 15445.0 N 6415.0 U 750.0

-- Skirt base ring
NEW CYLI
DIAM 2300.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 15445.0 N 6415.0 U 15.0

-- Skirt access opening, DN600
NEW CYLI
DIAM 600.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 15445.0 N 7395.0 U 450.0

-- Skirt vent E
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS E AND Y IS U
POS E 16425.0 N 6415.0 U 1300.0

-- Skirt vent W
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS W AND Y IS U
POS E 14465.0 N 6415.0 U 1300.0

NEW SUBE /203_TA_019_SHELL
-- Dished bottom head, 500 rise
NEW DISH
DIAM 2000.0
HEIG 500.0
RADIUS 2000.0
ORI Z IS D AND Y IS N
POS E 15445.0 N 6415.0 U 1250.0

-- Shell: DN2000 x 8500
NEW CYLI
DIAM 2000.0
HEIG 8500.0
ORI Z IS U AND Y IS N
POS E 15445.0 N 6415.0 U 5750.0

-- Dished top head, 500 rise
NEW DISH
DIAM 2000.0
HEIG 500.0
RADIUS 2000.0
ORI Z IS U AND Y IS N
POS E 15445.0 N 6415.0 U 10250.0

NEW SUBE /203_TA_019_N1
-- N1  DN200  EL +7800  -  Brown stock feed inlet
-- N1 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 15445.0 N 7430.0 U 9300.0

-- N1  DN200  EL +7800  90 deg  -  Brown stock feed inlet
NEW NOZZLE /203_TA_019_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 15445.0 N 7665.0 U 9300.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_019_N2
-- N2  DN800  EL +0  -  DN800 bottom outlet to MC pump
-- N2 reinforcing pad
NEW CYLI
DIAM 1020.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 15445.0 N 6415.0 U 15.0

-- N2  DN800  bottom nozzle  -  DN800 bottom outlet to MC pump
NEW NOZZLE /203_TA_019_N2_NOZZ
-- No catalogue component at DN800 (largest is DN600) - left unbound, will not render
POS E 15445.0 N 6415.0 U 0.0
HEIG 550.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_019_N3
-- N3  DN100  EL +6500  -  Level transmitter LS-3492 connection
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 16460.0 N 6415.0 U 8000.0

-- N3  DN100  EL +6500  0 deg  -  Level transmitter LS-3492 connection
NEW NOZZLE /203_TA_019_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 16645.0 N 6415.0 U 8000.0
ORI P1 IS E
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_019_N4
-- N4  DN100  EL +3000  -  Level control LIC-3493 connection
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 14430.0 N 6415.0 U 4500.0

-- N4  DN100  EL +3000  180 deg  -  Level control LIC-3493 connection
NEW NOZZLE /203_TA_019_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 14245.0 N 6415.0 U 4500.0
ORI P1 IS W
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_019_N5
-- N5  DN150  EL +8500  -  Vent
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 15845.0 N 6415.0 U 10315.0

-- N5  DN150  roof nozzle  -  Vent
NEW NOZZLE /203_TA_019_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 15845.0 N 6415.0 U 10500.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_019_M1
-- M1  DN500  EL +1800  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 14430.0 N 6415.0 U 3300.0

-- M1  DN500  EL +1800  135 deg  -  Manway
NEW NOZZLE /203_TA_019_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB011
POS E 14095.0 N 6415.0 U 3300.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_019_ACCESS
-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 9700.0
ORI Z IS U AND Y IS N
POS E 14445.0 N 6715.0 U 5150.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 9700.0
ORI Z IS U AND Y IS N
POS E 14445.0 N 6115.0 U 5150.0

-- Ladder safety cage required over the 9700 run (3 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 203-TA-024  1st OXYGEN REACTOR
-- ====================================================================
-- Area:        203 - Brown Stock / O2 Stage
-- Bottom centre (installation coordinate): E 12005.0  N -3752.0  U 0.0
-- Shell:       DN2000 x 20300 high
-- Closure:     Dished head / Conical bottom
-- Support:     Skirt support
-- Volume:      49 m3

NEW EQUI /203_TA_024
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_TA_024_SUPPORT
-- Skirt support, 2000 high to shell tangent
NEW CYLI
DIAM 2000.0
HEIG 2000.0
ORI Z IS U AND Y IS N
POS E 12005.0 N -3752.0 U 1000.0

-- Skirt base ring
NEW CYLI
DIAM 2300.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 12005.0 N -3752.0 U 15.0

-- Skirt access opening, DN600
NEW CYLI
DIAM 600.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 12005.0 N -2772.0 U 450.0

-- Skirt vent E
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS E AND Y IS U
POS E 12985.0 N -3752.0 U 1800.0

-- Skirt vent W
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS W AND Y IS U
POS E 11025.0 N -3752.0 U 1800.0

NEW SUBE /203_TA_024_SHELL
-- Conical bottom, 1800 high, DN300 outlet
NEW CONE
DTOP 2000.0
DBOT 300.0
HEIG 1800.0
ORI Z IS U AND Y IS N
POS E 12005.0 N -3752.0 U 1100.0

-- Shell: DN2000 x 20300
NEW CYLI
DIAM 2000.0
HEIG 20300.0
ORI Z IS U AND Y IS N
POS E 12005.0 N -3752.0 U 12150.0

-- Dished top head, 500 rise
NEW DISH
DIAM 2000.0
HEIG 500.0
RADIUS 2000.0
ORI Z IS U AND Y IS N
POS E 12005.0 N -3752.0 U 22550.0

NEW SUBE /203_TA_024_N1
-- N1  DN300  EL +600  -  MC pulp feed inlet (bottom, upflow)
-- N1 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 12005.0 N -2737.0 U 2600.0

-- N1  DN300  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /203_TA_024_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 12005.0 N -2502.0 U 2600.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_024_N2
-- N2  DN300  EL +19488  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 12005.0 N -4767.0 U 21488.0

-- N2  DN300  EL +19488  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /203_TA_024_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 12005.0 N -5002.0 U 21488.0
ORI P1 IS S
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_024_N3
-- N3  DN100  EL +6090  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 13020.0 N -3752.0 U 8090.0

-- N3  DN100  EL +6090  0 deg  -  Chemical injection / sample point
NEW NOZZLE /203_TA_024_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 13205.0 N -3752.0 U 8090.0
ORI P1 IS E
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_024_N4
-- N4  DN100  EL +12180  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 10990.0 N -3752.0 U 14180.0

-- N4  DN100  EL +12180  180 deg  -  Sample point
NEW NOZZLE /203_TA_024_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 10805.0 N -3752.0 U 14180.0
ORI P1 IS W
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_024_N5
-- N5  DN150  EL +20300  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 12405.0 N -3752.0 U 22615.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /203_TA_024_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 12405.0 N -3752.0 U 22800.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_024_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 10990.0 N -3752.0 U 3500.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /203_TA_024_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 10655.0 N -3752.0 U 3500.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_024_ACCESS
-- Stiffening ring 1 of 4
NEW CYLI
DIAM 2240.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 12005.0 N -3752.0 U 6160.0

-- Stiffening ring 2 of 4
NEW CYLI
DIAM 2240.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 12005.0 N -3752.0 U 10220.0

-- Stiffening ring 3 of 4
NEW CYLI
DIAM 2240.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 12005.0 N -3752.0 U 14280.0

-- Stiffening ring 4 of 4
NEW CYLI
DIAM 2240.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 12005.0 N -3752.0 U 18340.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 22000.0
ORI Z IS U AND Y IS N
POS E 11005.0 N -3452.0 U 11300.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 22000.0
ORI Z IS U AND Y IS N
POS E 11005.0 N -4052.0 U 11300.0

-- Ladder safety cage required over the 22000 run (7 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
-- Access platform required at EL +6000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +12000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +18000 (Reference Value - extent and support to be set by steel design)

-- ====================================================================
-- 203-TA-029  2nd OXYGEN REACTOR
-- ====================================================================
-- Area:        203 - Brown Stock / O2 Stage
-- Bottom centre (installation coordinate): E 16609.0  N -3752.0  U 0.0
-- Shell:       DN2600 x 23500 high
-- Closure:     Dished head / Conical bottom
-- Support:     Skirt support
-- Volume:      97 m3

NEW EQUI /203_TA_029
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_TA_029_SUPPORT
-- Skirt support, 2000 high to shell tangent
NEW CYLI
DIAM 2600.0
HEIG 2000.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 1000.0

-- Skirt base ring
NEW CYLI
DIAM 2900.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 15.0

-- Skirt access opening, DN600
NEW CYLI
DIAM 600.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 16609.0 N -2472.0 U 450.0

-- Skirt vent E
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS E AND Y IS U
POS E 17889.0 N -3752.0 U 1800.0

-- Skirt vent W
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS W AND Y IS U
POS E 15329.0 N -3752.0 U 1800.0

NEW SUBE /203_TA_029_SHELL
-- Conical bottom, 2200 high, DN300 outlet
NEW CONE
DTOP 2600.0
DBOT 300.0
HEIG 2200.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 1100.0

-- Shell: DN2600 x 23500
NEW CYLI
DIAM 2600.0
HEIG 23500.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 13750.0

-- Dished top head, 650 rise
NEW DISH
DIAM 2600.0
HEIG 650.0
RADIUS 2600.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 25825.0

NEW SUBE /203_TA_029_N1
-- N1  DN300  EL +600  -  MC pulp feed inlet (bottom, upflow)
-- N1 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 16609.0 N -2437.0 U 2600.0

-- N1  DN300  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /203_TA_029_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 16609.0 N -2202.0 U 2600.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_029_N2
-- N2  DN300  EL +22560  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 16609.0 N -5067.0 U 24560.0

-- N2  DN300  EL +22560  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /203_TA_029_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 16609.0 N -5302.0 U 24560.0
ORI P1 IS S
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_029_N3
-- N3  DN100  EL +7050  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 17924.0 N -3752.0 U 9050.0

-- N3  DN100  EL +7050  0 deg  -  Chemical injection / sample point
NEW NOZZLE /203_TA_029_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 18109.0 N -3752.0 U 9050.0
ORI P1 IS E
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_029_N4
-- N4  DN100  EL +14100  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 15294.0 N -3752.0 U 16100.0

-- N4  DN100  EL +14100  180 deg  -  Sample point
NEW NOZZLE /203_TA_029_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 15109.0 N -3752.0 U 16100.0
ORI P1 IS W
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_029_N5
-- N5  DN150  EL +23500  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 17129.0 N -3752.0 U 25905.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /203_TA_029_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 17129.0 N -3752.0 U 26090.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_029_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 15294.0 N -3752.0 U 3500.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /203_TA_029_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 14959.0 N -3752.0 U 3500.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_029_ACCESS
-- Stiffening ring 1 of 5
NEW CYLI
DIAM 2840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 6016.7

-- Stiffening ring 2 of 5
NEW CYLI
DIAM 2840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 9933.3

-- Stiffening ring 3 of 5
NEW CYLI
DIAM 2840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 13850.0

-- Stiffening ring 4 of 5
NEW CYLI
DIAM 2840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 17766.7

-- Stiffening ring 5 of 5
NEW CYLI
DIAM 2840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 16609.0 N -3752.0 U 21683.3

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 25200.0
ORI Z IS U AND Y IS N
POS E 15309.0 N -3452.0 U 12900.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 25200.0
ORI Z IS U AND Y IS N
POS E 15309.0 N -4052.0 U 12900.0

-- Ladder safety cage required over the 25200 run (8 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
-- Access platform required at EL +6000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +12000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +18000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +22000 (Reference Value - extent and support to be set by steel design)

-- ====================================================================
-- 203-TA-044  INSTRUMENT AIR RECEIVER
-- ====================================================================
-- Area:        203 - Brown Stock / O2 Stage
-- Bottom centre (installation coordinate): E 11601.0  N 3981.0  U 0.0
-- Shell:       DN800 x 2500 high
-- Closure:     Dished head / Dished bottom
-- Support:     Support legs

NEW EQUI /203_TA_044
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_TA_044_SUPPORT
-- 4 support legs on a 800 bolt circle
-- Support base plate at foundation bearing plane
NEW CYLI
DIAM 1000.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 11601.0 N 3981.0 U 12.5

-- Leg 1
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 600.0
POS E 11742.4 N 4122.4 U 300.0

-- Leg 1 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 11742.4 N 4122.4 U 12.5

-- Leg 1 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 11722.6 N 4102.6 U 450.0

-- Leg 2
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 600.0
POS E 11459.6 N 4122.4 U 300.0

-- Leg 2 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 11459.6 N 4122.4 U 12.5

-- Leg 2 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 11479.4 N 4102.6 U 450.0

-- Leg 3
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 600.0
POS E 11459.6 N 3839.6 U 300.0

-- Leg 3 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 11459.6 N 3839.6 U 12.5

-- Leg 3 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 11479.4 N 3859.4 U 450.0

-- Leg 4
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 600.0
POS E 11742.4 N 3839.6 U 300.0

-- Leg 4 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 11742.4 N 3839.6 U 12.5

-- Leg 4 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 11722.6 N 3859.4 U 450.0

NEW SUBE /203_TA_044_SHELL
-- Dished bottom head, 200 rise
NEW DISH
DIAM 800.0
HEIG 200.0
RADIUS 800.0
ORI Z IS D AND Y IS N
POS E 11601.0 N 3981.0 U 500.0

-- Shell: DN800 x 2500
NEW CYLI
DIAM 800.0
HEIG 2500.0
ORI Z IS U AND Y IS N
POS E 11601.0 N 3981.0 U 1850.0

-- Dished top head, 200 rise
NEW DISH
DIAM 800.0
HEIG 200.0
RADIUS 800.0
ORI Z IS U AND Y IS N
POS E 11601.0 N 3981.0 U 3200.0

NEW SUBE /203_TA_044_N1
-- N1  DN80  EL +2200  -  Compressed air inlet
-- N1  DN80  EL +2200  90 deg  -  Compressed air inlet
NEW NOZZLE /203_TA_044_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 11601.0 N 4531.0 U 2800.0
ORI P1 IS N
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_044_N2
-- N2  DN80  EL +500  -  Air outlet to distribution header
-- N2  DN80  EL +500  270 deg  -  Air outlet to distribution header
NEW NOZZLE /203_TA_044_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 11601.0 N 3431.0 U 1100.0
ORI P1 IS S
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_044_N3
-- N3  DN25  EL +0  -  Condensate drain / auto trap
-- N3  DN25  bottom nozzle  -  Condensate drain / auto trap
NEW NOZZLE /203_TA_044_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0FF
POS E 11601.0 N 3981.0 U 0.0
ORI P1 IS U
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_044_N4
-- N4  DN50  EL +2500  -  Safety relief valve
-- N4  DN50  roof nozzle  -  Safety relief valve
NEW NOZZLE /203_TA_044_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0JJ
POS E 11761.0 N 3981.0 U 3370.0
ORI P1 IS U
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_TA_044_ACCESS

-- ====================================================================
-- 204-TA-001  OXYGEN STAGE BLOW TANK
-- ====================================================================
-- Area:        204 - Screening & Washing
-- Bottom centre (installation coordinate): E 21008.0  N -4151.0  U 0.0
-- Shell:       DN3200 x 13000 high
-- Closure:     Conical roof / Conical bottom
-- Support:     Skirt support
-- Volume:      64 m3

NEW EQUI /204_TA_001
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_TA_001_SUPPORT
-- Skirt support, 1500 high to shell tangent
NEW CYLI
DIAM 3200.0
HEIG 1500.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 750.0

-- Skirt base ring
NEW CYLI
DIAM 3500.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 15.0

-- Skirt access opening, DN600
NEW CYLI
DIAM 600.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 21008.0 N -2571.0 U 450.0

-- Skirt vent E
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS E AND Y IS U
POS E 22588.0 N -4151.0 U 1300.0

-- Skirt vent W
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS W AND Y IS U
POS E 19428.0 N -4151.0 U 1300.0

NEW SUBE /204_TA_001_SHELL
-- Conical bottom, 2000 high, DN400 outlet
NEW CONE
DTOP 3200.0
DBOT 400.0
HEIG 2000.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 1000.0

-- Shell: DN3200 x 13000
NEW CYLI
DIAM 3200.0
HEIG 13000.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 8000.0

-- Roof curb / compression ring
NEW CYLI
DIAM 3400.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 14375.0

-- Conical roof, 900 rise
NEW CONE
DTOP 300.0
DBOT 3200.0
HEIG 900.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 14950.0

-- Roof apex cap
NEW CYLI
DIAM 400.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 15430.0

NEW SUBE /204_TA_001_N1
-- N1  DN400  EL +11500  -  Blow line inlet from O2 reactor
-- N1 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 21008.0 N -2536.0 U 13000.0

-- N1  DN400  EL +11500  90 deg  -  Blow line inlet from O2 reactor
NEW NOZZLE /204_TA_001_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 21008.0 N -2201.0 U 13000.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_001_N2
-- N2  DN400  EL +0  -  Bottom cone outlet to pump
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 15.0

-- N2  DN400  bottom nozzle  -  Bottom cone outlet to pump
NEW NOZZLE /204_TA_001_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 21008.0 N -4151.0 U 0.0
ORI P1 IS U
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_001_N3
-- N3  DN600  EL +13000  -  Steam / vapour relief to cyclone
-- N3 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 21648.0 N -4151.0 U 15055.0

-- N3  DN600  roof nozzle  -  Steam / vapour relief to cyclone
NEW NOZZLE /204_TA_001_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 21648.0 N -4151.0 U 15390.0
ORI P1 IS U
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_001_N4
-- N4  DN200  EL +6000  -  Dilution filtrate
-- N4 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 19393.0 N -4151.0 U 7500.0

-- N4  DN200  EL +6000  180 deg  -  Dilution filtrate
NEW NOZZLE /204_TA_001_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 19158.0 N -4151.0 U 7500.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_001_M1
-- M1  DN600  EL +2000  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 19393.0 N -4151.0 U 3500.0

-- M1  DN600  EL +2000  135 deg  -  Manway
NEW NOZZLE /204_TA_001_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 19058.0 N -4151.0 U 3500.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_001_ACCESS
-- Stiffening ring 1 of 3
NEW CYLI
DIAM 3440.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 4850.0

-- Stiffening ring 2 of 3
NEW CYLI
DIAM 3440.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 8100.0

-- Stiffening ring 3 of 3
NEW CYLI
DIAM 3440.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 21008.0 N -4151.0 U 11350.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 14200.0
ORI Z IS U AND Y IS N
POS E 19408.0 N -3851.0 U 7400.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 14200.0
ORI Z IS U AND Y IS N
POS E 19408.0 N -4451.0 U 7400.0

-- Ladder safety cage required over the 14200 run (4 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
NEW SUBE /204_TA_001_INTERNALS
-- Side-entry agitator mounting nozzle
NEW CYLI
DIAM 500.0
HEIG 350.0
ORI Z IS S AND Y IS U
POS E 21008.0 N -5876.0 U 3060.0

-- Side-entry agitator mounting flange
NEW CYLI
DIAM 620.0
HEIG 40.0
ORI Z IS S AND Y IS U
POS E 21008.0 N -6031.0 U 3060.0

-- Side-entry agitator gearbox
NEW CYLI
DIAM 700.0
HEIG 600.0
ORI Z IS S AND Y IS U
POS E 21008.0 N -6351.0 U 3060.0

-- Side-entry agitator drive motor
NEW CYLI
DIAM 550.0
HEIG 900.0
ORI Z IS S AND Y IS U
POS E 21008.0 N -7101.0 U 3060.0

-- Side-entry agitator shaft
NEW CYLI
DIAM 180.0
HEIG 960.0
ORI Z IS S AND Y IS U
POS E 21008.0 N -5221.0 U 3060.0

-- Side-entry agitator propeller, DN640
NEW CYLI
DIAM 640.0
HEIG 120.0
ORI Z IS S AND Y IS U
POS E 21008.0 N -4801.0 U 3060.0


-- ====================================================================
-- 204-TA-021  POST O2 WASHER DROPLEG
-- ====================================================================
-- Area:        204 - Screening & Washing
-- Bottom centre (installation coordinate): E 23650.0  N 6000.0  U 0.0
-- Shell:       DN710 x 12000 high
-- Closure:     Flat roof / Conical bottom
-- Support:     Support legs

NEW EQUI /204_TA_021
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_TA_021_SUPPORT
-- 4 support legs on a 710 bolt circle
-- Support base plate at foundation bearing plane
NEW CYLI
DIAM 910.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 23650.0 N 6000.0 U 12.5

-- Leg 1
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 23759.6 N 6109.6 U 250.0

-- Leg 1 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 23759.6 N 6109.6 U 12.5

-- Leg 1 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 23744.3 N 6094.3 U 350.0

-- Leg 2
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 23540.4 N 6109.6 U 250.0

-- Leg 2 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 23540.4 N 6109.6 U 12.5

-- Leg 2 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 23555.7 N 6094.3 U 350.0

-- Leg 3
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 23540.4 N 5890.4 U 250.0

-- Leg 3 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 23540.4 N 5890.4 U 12.5

-- Leg 3 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 23555.7 N 5905.7 U 350.0

-- Leg 4
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 23759.6 N 5890.4 U 250.0

-- Leg 4 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 23759.6 N 5890.4 U 12.5

-- Leg 4 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 23744.3 N 5905.7 U 350.0

NEW SUBE /204_TA_021_SHELL
-- Conical bottom, 900 high, DN300 outlet
NEW CONE
DTOP 710.0
DBOT 300.0
HEIG 900.0
ORI Z IS U AND Y IS N
POS E 23650.0 N 6000.0 U 450.0

-- Shell: DN710 x 12000
NEW CYLI
DIAM 710.0
HEIG 12000.0
ORI Z IS U AND Y IS N
POS E 23650.0 N 6000.0 U 6500.0

-- Flat roof plate
NEW CYLI
DIAM 710.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 23650.0 N 6000.0 U 12512.5

-- Roof rim angle
NEW CYLI
DIAM 910.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 23650.0 N 6000.0 U 12375.0

NEW SUBE /204_TA_021_N1
-- N1  DN400  EL +11640  -  Filtrate inlet from washer vat
-- N1 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 23650.0 N 6370.0 U 12140.0

-- N1  DN400  EL +11640  90 deg  -  Filtrate inlet from washer vat
NEW NOZZLE /204_TA_021_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 23650.0 N 6705.0 U 12140.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_021_N2
-- N2  DN400  EL +300  -  Seal pot / filtrate outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 23650.0 N 5630.0 U 800.0

-- N2  DN400  EL +300  270 deg  -  Seal pot / filtrate outlet
NEW NOZZLE /204_TA_021_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 23650.0 N 5295.0 U 800.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_021_N3
-- N3  DN150  EL +12000  -  Vacuum / air separation vent
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 23792.0 N 6000.0 U 12515.0

-- N3  DN150  roof nozzle  -  Vacuum / air separation vent
NEW NOZZLE /204_TA_021_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 23792.0 N 6000.0 U 12700.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_021_ACCESS
-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 12200.0
ORI Z IS U AND Y IS N
POS E 23295.0 N 6300.0 U 6400.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 12200.0
ORI Z IS U AND Y IS N
POS E 23295.0 N 5700.0 U 6400.0

-- Ladder safety cage required over the 12200 run (4 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 204-TA-034  SCREEN DILUTION TANK
-- ====================================================================
-- Area:        204 - Screening & Washing
-- Bottom centre (installation coordinate): E 22512.0  N 21358.0  U 0.0
-- Shell:       DN2300 x 7600 high
-- Closure:     Conical roof / Flat bottom
-- Support:     Ground / slab bearing
-- Volume:      29 m3

NEW EQUI /204_TA_034
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_TA_034_SHELL
-- Flat bottom plate
NEW CYLI
DIAM 2300.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 22512.0 N 21358.0 U 10.0

-- Shell: DN2300 x 7600
NEW CYLI
DIAM 2300.0
HEIG 7600.0
ORI Z IS U AND Y IS N
POS E 22512.0 N 21358.0 U 3800.0

-- Roof curb / compression ring
NEW CYLI
DIAM 2500.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 22512.0 N 21358.0 U 7475.0

-- Conical roof, 350 rise
NEW CONE
DTOP 230.0
DBOT 2300.0
HEIG 350.0
ORI Z IS U AND Y IS N
POS E 22512.0 N 21358.0 U 7775.0

-- Roof apex cap
NEW CYLI
DIAM 330.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 22512.0 N 21358.0 U 7980.0

NEW SUBE /204_TA_034_N1
-- N1  DN250  EL +6460  -  Stock / filtrate feed inlet
-- N1 reinforcing pad
NEW CYLI
DIAM 470.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 22523.0 U 6460.0

-- N1  DN250  EL +6460  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /204_TA_034_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0VV
POS E 22512.0 N 22758.0 U 6460.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_034_N2
-- N2  DN300  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 22512.0 N 20193.0 U 400.0

-- N2  DN300  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /204_TA_034_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 22512.0 N 19958.0 U 400.0
ORI P1 IS S
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_034_N3
-- N3  DN200  EL +7144  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 21347.0 N 21358.0 U 7144.0

-- N3  DN200  EL +7144  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /204_TA_034_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 21112.0 N 21358.0 U 7144.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_034_N4
-- N4  DN150  EL +7600  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 22972.0 N 21358.0 U 7825.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /204_TA_034_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 22972.0 N 21358.0 U 8010.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_034_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /204_TA_034_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 23812.0 N 21358.0 U 250.0
ORI P1 IS E
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_034_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 22523.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /204_TA_034_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 22512.0 N 22858.0 U 1200.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_034_ACCESS
-- Stiffening ring 1 of 1
NEW CYLI
DIAM 2540.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 22512.0 N 21358.0 U 3900.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 7300.0
ORI Z IS U AND Y IS N
POS E 21362.0 N 21658.0 U 3950.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 7300.0
ORI Z IS U AND Y IS N
POS E 21362.0 N 21058.0 U 3950.0

-- Ladder safety cage required over the 7300 run (2 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 204-TA-035  POST OXYGEN FILTRATE TANK
-- ====================================================================
-- Area:        204 - Screening & Washing
-- Bottom centre (installation coordinate): E 27013.0  N 19860.0  U 0.0
-- Shell:       DN5600 x 7600 high
-- Closure:     Conical roof / Flat bottom
-- Support:     Ground / slab bearing
-- Volume:      158 m3

NEW EQUI /204_TA_035
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_TA_035_SHELL
-- Flat bottom plate
NEW CYLI
DIAM 5600.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 10.0

-- Shell: DN5600 x 7600
NEW CYLI
DIAM 5600.0
HEIG 7600.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 3800.0

-- Roof curb / compression ring
NEW CYLI
DIAM 5800.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 7475.0

-- Conical roof, 700 rise
NEW CONE
DTOP 300.0
DBOT 5600.0
HEIG 700.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 7950.0

-- Roof apex cap
NEW CYLI
DIAM 400.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 8330.0

NEW SUBE /204_TA_035_N1
-- N1  DN300  EL +5500  -  DN300 filtrate inlet
-- N1 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 27013.0 N 22675.0 U 5500.0

-- N1  DN300  EL +5500  90 deg  -  DN300 filtrate inlet
NEW NOZZLE /204_TA_035_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 27013.0 N 22910.0 U 5500.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_035_N2
-- N2  DN400  EL +400  -  Filtrate pump suction
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 27013.0 N 17045.0 U 400.0

-- N2  DN400  EL +400  270 deg  -  Filtrate pump suction
NEW NOZZLE /204_TA_035_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 27013.0 N 16710.0 U 400.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_035_N3
-- N3  DN300  EL +7100  -  Overflow
-- N3 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 24198.0 N 19860.0 U 7100.0

-- N3  DN300  EL +7100  180 deg  -  Overflow
NEW NOZZLE /204_TA_035_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 23963.0 N 19860.0 U 7100.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_035_N4
-- N4  DN200  EL +7600  -  Vent
-- N4 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 28133.0 N 19860.0 U 8035.0

-- N4  DN200  roof nozzle  -  Vent
NEW NOZZLE /204_TA_035_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 28133.0 N 19860.0 U 8270.0
ORI P1 IS U
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_035_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /204_TA_035_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 29963.0 N 19860.0 U 250.0
ORI P1 IS E
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_035_M1
-- M1  DN600  EL +1200  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 27013.0 N 22675.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Manway
NEW NOZZLE /204_TA_035_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 27013.0 N 23010.0 U 1200.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_TA_035_ACCESS
-- Stiffening ring 1 of 2
NEW CYLI
DIAM 5840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 2633.3

-- Stiffening ring 2 of 2
NEW CYLI
DIAM 5840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 5166.7

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 7300.0
ORI Z IS U AND Y IS N
POS E 24213.0 N 20160.0 U 3950.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 7300.0
ORI Z IS U AND Y IS N
POS E 24213.0 N 19560.0 U 3950.0

-- Ladder safety cage required over the 7300 run (2 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
NEW SUBE /204_TA_035_INTERNALS
-- Agitator mounting pedestal on roof
NEW CYLI
DIAM 672.0
HEIG 400.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 8500.0

-- Agitator mounting flange
NEW CYLI
DIAM 872.0
HEIG 40.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 8720.0

-- Agitator gearbox
NEW BOX
XLEN 1200.0
YLEN 900.0
ZLEN 700.0
POS E 27013.0 N 19860.0 U 9090.0

-- Agitator drive motor
NEW CYLI
DIAM 700.0
HEIG 900.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 9890.0

-- Agitator shaft
NEW CYLI
DIAM 180.0
HEIG 7160.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 4720.0

-- Impeller hub, DN1960 swept
NEW CYLI
DIAM 324.0
HEIG 150.0
ORI Z IS U AND Y IS N
POS E 27013.0 N 19860.0 U 1443.0

-- Impeller blade E
NEW BOX
XLEN 890.0
YLEN 120.0
ZLEN 150.0
POS E 27548.0 N 19860.0 U 1443.0

-- Impeller blade N
NEW BOX
XLEN 120.0
YLEN 890.0
ZLEN 150.0
POS E 27013.0 N 20395.0 U 1443.0

-- Impeller blade W
NEW BOX
XLEN 890.0
YLEN 120.0
ZLEN 150.0
POS E 26478.0 N 19860.0 U 1443.0

-- Impeller blade S
NEW BOX
XLEN 120.0
YLEN 890.0
ZLEN 150.0
POS E 27013.0 N 19325.0 U 1443.0


-- ====================================================================
-- 205-TA-001  UNBLEACHED PULP STORAGE TOWER
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 26863.0  N -11601.0  U 0.0
-- Shell:       DN9000 x 26400 high, outer envelope DN10800
-- Closure:     Conical roof / Dished bottom
-- Support:     Ground / slab bearing
-- Volume:      1000 m3

NEW EQUI /205_TA_001
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_001_SHELL
-- Bottom plate on slab (dished head has no clearance below grade)
NEW CYLI
DIAM 9000.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 10.0

-- Shell: DN9000 x 26400
NEW CYLI
DIAM 9000.0
HEIG 26400.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 13200.0

-- Roof curb / compression ring
NEW CYLI
DIAM 9200.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 26275.0

-- Conical roof, 1800 rise
NEW CONE
DTOP 300.0
DBOT 9000.0
HEIG 1800.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 27300.0

-- Roof apex cap
NEW CYLI
DIAM 400.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 28230.0

-- Outer shell / insulation envelope DN10800 (annulus 900 radial)
NEW CYLI
DIAM 10800.0
HEIG 26400.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 13200.0

NEW SUBE /205_TA_001_N1
-- N1  DN400  EL +24000  -  MC pulp feed inlet (top)
-- N1 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 26863.0 N -6186.0 U 24000.0

-- N1  DN400  EL +24000  90 deg  -  MC pulp feed inlet (top)
NEW NOZZLE /205_TA_001_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 26863.0 N -5851.0 U 24000.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_001_N2
-- N2  DN500  EL +500  -  Bottom discharge to drop leg
-- N2 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 26863.0 N -17016.0 U 500.0

-- N2  DN500  EL +500  270 deg  -  Bottom discharge to drop leg
NEW NOZZLE /205_TA_001_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB011
POS E 26863.0 N -17351.0 U 500.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_001_N3
-- N3  DN200  EL +3000  -  Dilution water ring - lower
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 32278.0 N -11601.0 U 3000.0

-- N3  DN200  EL +3000  0 deg  -  Dilution water ring - lower
NEW NOZZLE /205_TA_001_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 32513.0 N -11601.0 U 3000.0
ORI P1 IS E
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_001_N4
-- N4  DN200  EL +3000  -  Dilution water ring - upper
-- N4 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 21448.0 N -11601.0 U 3000.0

-- N4  DN200  EL +3000  180 deg  -  Dilution water ring - upper
NEW NOZZLE /205_TA_001_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 21213.0 N -11601.0 U 3000.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_001_N5
-- N5  DN300  EL +26400  -  Vent
-- N5 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 28663.0 N -11601.0 U 27495.0

-- N5  DN300  roof nozzle  -  Vent
NEW NOZZLE /205_TA_001_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 28663.0 N -11601.0 U 27730.0
ORI P1 IS U
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_001_M1
-- M1  DN600  EL +1500  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 21448.0 N -11601.0 U 1500.0

-- M1  DN600  EL +1500  135 deg  -  Manway
NEW NOZZLE /205_TA_001_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 21113.0 N -11601.0 U 1500.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_001_ACCESS
-- Stiffening ring 1 of 6
NEW CYLI
DIAM 11040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 3871.4

-- Stiffening ring 2 of 6
NEW CYLI
DIAM 11040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 7642.9

-- Stiffening ring 3 of 6
NEW CYLI
DIAM 11040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 11414.3

-- Stiffening ring 4 of 6
NEW CYLI
DIAM 11040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 15185.7

-- Stiffening ring 5 of 6
NEW CYLI
DIAM 11040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 18957.1

-- Stiffening ring 6 of 6
NEW CYLI
DIAM 11040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 22728.6

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 26100.0
ORI Z IS U AND Y IS N
POS E 21463.0 N -11301.0 U 13350.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 26100.0
ORI Z IS U AND Y IS N
POS E 21463.0 N -11901.0 U 13350.0

-- Ladder safety cage required over the 26100 run (8 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
-- Access platform required at EL +8000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +16000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +24000 (Reference Value - extent and support to be set by steel design)
NEW SUBE /205_TA_001_INTERNALS
-- Discharge scraper drive head (at floor centre)
NEW CYLI
DIAM 1400.0
HEIG 700.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 350.0

-- Discharge scraper hub
NEW CYLI
DIAM 900.0
HEIG 400.0
ORI Z IS U AND Y IS N
POS E 26863.0 N -11601.0 U 900.0

-- Discharge scraper sweep arm E
NEW BOX
XLEN 3240.0
YLEN 250.0
ZLEN 250.0
POS E 28933.0 N -11601.0 U 825.0

-- Discharge scraper sweep arm N
NEW BOX
XLEN 250.0
YLEN 3240.0
ZLEN 250.0
POS E 26863.0 N -9531.0 U 825.0

-- Discharge scraper sweep arm W
NEW BOX
XLEN 3240.0
YLEN 250.0
ZLEN 250.0
POS E 24793.0 N -11601.0 U 825.0

-- Discharge scraper sweep arm S
NEW BOX
XLEN 250.0
YLEN 3240.0
ZLEN 250.0
POS E 26863.0 N -13671.0 U 825.0


-- ====================================================================
-- 205-TA-008  D0 TOWER
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 34016.0  N -4501.0  U 0.0
-- Shell:       DN2600 x 18600 high
-- Closure:     Flat roof / Conical bottom
-- Support:     Skirt support
-- Volume:      65 m3

NEW EQUI /205_TA_008
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_008_SUPPORT
-- Skirt support, 2500 high to shell tangent
NEW CYLI
DIAM 2600.0
HEIG 2500.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 1250.0

-- Skirt base ring
NEW CYLI
DIAM 2900.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 15.0

-- Skirt access opening, DN600
NEW CYLI
DIAM 600.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 34016.0 N -3221.0 U 450.0

-- Skirt vent E
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS E AND Y IS U
POS E 35296.0 N -4501.0 U 2300.0

-- Skirt vent W
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS W AND Y IS U
POS E 32736.0 N -4501.0 U 2300.0

NEW SUBE /205_TA_008_SHELL
-- Conical bottom, 3000 high, DN300 outlet
NEW CONE
DTOP 2600.0
DBOT 300.0
HEIG 3000.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 1500.0

-- Shell: DN2600 x 18600
NEW CYLI
DIAM 2600.0
HEIG 18600.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 11800.0

-- Flat roof plate
NEW CYLI
DIAM 2600.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 21112.5

-- Roof rim angle
NEW CYLI
DIAM 2800.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 20975.0

NEW SUBE /205_TA_008_N1
-- N1  DN300  EL +600  -  MC pulp feed inlet (bottom, upflow)
-- N1 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 34016.0 N -3186.0 U 3100.0

-- N1  DN300  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /205_TA_008_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 34016.0 N -2951.0 U 3100.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_008_N2
-- N2  DN300  EL +17856  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 34016.0 N -5816.0 U 20356.0

-- N2  DN300  EL +17856  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /205_TA_008_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 34016.0 N -6051.0 U 20356.0
ORI P1 IS S
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_008_N3
-- N3  DN100  EL +5580  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 35331.0 N -4501.0 U 8080.0

-- N3  DN100  EL +5580  0 deg  -  Chemical injection / sample point
NEW NOZZLE /205_TA_008_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 35516.0 N -4501.0 U 8080.0
ORI P1 IS E
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_008_N4
-- N4  DN100  EL +11160  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 32701.0 N -4501.0 U 13660.0

-- N4  DN100  EL +11160  180 deg  -  Sample point
NEW NOZZLE /205_TA_008_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 32516.0 N -4501.0 U 13660.0
ORI P1 IS W
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_008_N5
-- N5  DN150  EL +18600  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 34536.0 N -4501.0 U 21115.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /205_TA_008_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 34536.0 N -4501.0 U 21300.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_008_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 32701.0 N -4501.0 U 4000.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_008_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 32366.0 N -4501.0 U 4000.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_008_ACCESS
-- Stiffening ring 1 of 4
NEW CYLI
DIAM 2840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 6320.0

-- Stiffening ring 2 of 4
NEW CYLI
DIAM 2840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 10040.0

-- Stiffening ring 3 of 4
NEW CYLI
DIAM 2840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 13760.0

-- Stiffening ring 4 of 4
NEW CYLI
DIAM 2840.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 34016.0 N -4501.0 U 17480.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 20800.0
ORI Z IS U AND Y IS N
POS E 32716.0 N -4201.0 U 10700.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 20800.0
ORI Z IS U AND Y IS N
POS E 32716.0 N -4801.0 U 10700.0

-- Ladder safety cage required over the 20800 run (6 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
-- Access platform required at EL +6000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +12000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +17000 (Reference Value - extent and support to be set by steel design)

-- ====================================================================
-- 205-TA-011  D0 FILTRATE TANK
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 33067.0  N 19057.0  U 0.0
-- Shell:       DN4000 x 5300 high
-- Closure:     Conical roof / Flat bottom
-- Support:     Ground / slab bearing
-- Volume:      63 m3

NEW EQUI /205_TA_011
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_011_SHELL
-- Flat bottom plate
NEW CYLI
DIAM 4000.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 33067.0 N 19057.0 U 10.0

-- Shell: DN4000 x 5300
NEW CYLI
DIAM 4000.0
HEIG 5300.0
ORI Z IS U AND Y IS N
POS E 33067.0 N 19057.0 U 2650.0

-- Roof curb / compression ring
NEW CYLI
DIAM 4200.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 33067.0 N 19057.0 U 5175.0

-- Conical roof, 500 rise
NEW CONE
DTOP 300.0
DBOT 4000.0
HEIG 500.0
ORI Z IS U AND Y IS N
POS E 33067.0 N 19057.0 U 5550.0

-- Roof apex cap
NEW CYLI
DIAM 400.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 33067.0 N 19057.0 U 5830.0

NEW SUBE /205_TA_011_N1
-- N1  DN300  EL +4505  -  Stock / filtrate feed inlet
-- N1 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 33067.0 N 21072.0 U 4505.0

-- N1  DN300  EL +4505  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /205_TA_011_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 33067.0 N 21307.0 U 4505.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_011_N2
-- N2  DN350  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 570.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 33067.0 N 17042.0 U 400.0

-- N2  DN350  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /205_TA_011_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0XX
POS E 33067.0 N 16707.0 U 400.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_011_N3
-- N3  DN200  EL +4982  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 31052.0 N 19057.0 U 4982.0

-- N3  DN200  EL +4982  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /205_TA_011_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 30817.0 N 19057.0 U 4982.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_011_N4
-- N4  DN150  EL +5300  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 33867.0 N 19057.0 U 5615.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /205_TA_011_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 33867.0 N 19057.0 U 5800.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_011_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /205_TA_011_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 35217.0 N 19057.0 U 250.0
ORI P1 IS E
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_011_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 33067.0 N 21072.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_011_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 33067.0 N 21407.0 U 1200.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_011_ACCESS
-- Stiffening ring 1 of 1
NEW CYLI
DIAM 4240.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 33067.0 N 19057.0 U 2750.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 5000.0
ORI Z IS U AND Y IS N
POS E 31067.0 N 19357.0 U 2800.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 5000.0
ORI Z IS U AND Y IS N
POS E 31067.0 N 18757.0 U 2800.0

-- Ladder safety cage required over the 5000 run (1 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 205-TA-016  D0 WASHER DROPLEG
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 33833.0  N 6000.0  U 0.0
-- Shell:       DN1050 x 12000 high
-- Closure:     Flat roof / Conical bottom
-- Support:     Support legs

NEW EQUI /205_TA_016
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_016_SUPPORT
-- 4 support legs on a 1050 bolt circle
-- Support base plate at foundation bearing plane
NEW CYLI
DIAM 1250.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 33833.0 N 6000.0 U 12.5

-- Leg 1
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 34062.8 N 6229.8 U 250.0

-- Leg 1 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 34062.8 N 6229.8 U 12.5

-- Leg 1 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 34030.6 N 6197.6 U 350.0

-- Leg 2
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 33603.2 N 6229.8 U 250.0

-- Leg 2 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 33603.2 N 6229.8 U 12.5

-- Leg 2 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 33635.4 N 6197.6 U 350.0

-- Leg 3
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 33603.2 N 5770.2 U 250.0

-- Leg 3 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 33603.2 N 5770.2 U 12.5

-- Leg 3 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 33635.4 N 5802.4 U 350.0

-- Leg 4
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 34062.8 N 5770.2 U 250.0

-- Leg 4 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 34062.8 N 5770.2 U 12.5

-- Leg 4 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 34030.6 N 5802.4 U 350.0

NEW SUBE /205_TA_016_SHELL
-- Conical bottom, 1200 high, DN400 outlet
NEW CONE
DTOP 1050.0
DBOT 400.0
HEIG 1200.0
ORI Z IS U AND Y IS N
POS E 33833.0 N 6000.0 U 600.0

-- Shell: DN1050 x 12000
NEW CYLI
DIAM 1050.0
HEIG 12000.0
ORI Z IS U AND Y IS N
POS E 33833.0 N 6000.0 U 6500.0

-- Flat roof plate
NEW CYLI
DIAM 1050.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 33833.0 N 6000.0 U 12512.5

-- Roof rim angle
NEW CYLI
DIAM 1250.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 33833.0 N 6000.0 U 12375.0

NEW SUBE /205_TA_016_N1
-- N1  DN400  EL +11640  -  Filtrate inlet from washer vat
-- N1 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 33833.0 N 6540.0 U 12140.0

-- N1  DN400  EL +11640  90 deg  -  Filtrate inlet from washer vat
NEW NOZZLE /205_TA_016_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 33833.0 N 6875.0 U 12140.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_016_N2
-- N2  DN400  EL +300  -  Seal pot / filtrate outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 33833.0 N 5460.0 U 800.0

-- N2  DN400  EL +300  270 deg  -  Seal pot / filtrate outlet
NEW NOZZLE /205_TA_016_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 33833.0 N 5125.0 U 800.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_016_N3
-- N3  DN150  EL +12000  -  Vacuum / air separation vent
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 34043.0 N 6000.0 U 12515.0

-- N3  DN150  roof nozzle  -  Vacuum / air separation vent
NEW NOZZLE /205_TA_016_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 34043.0 N 6000.0 U 12700.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_016_ACCESS
-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 12200.0
ORI Z IS U AND Y IS N
POS E 33308.0 N 6300.0 U 6400.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 12200.0
ORI Z IS U AND Y IS N
POS E 33308.0 N 5700.0 U 6400.0

-- Ladder safety cage required over the 12200 run (4 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 205-TA-022  EOP REACTOR
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 38469.0  N -4401.0  U 0.0
-- Shell:       DN2800 x 22000 high
-- Closure:     Dished head / Conical bottom
-- Support:     Skirt support

NEW EQUI /205_TA_022
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_022_SUPPORT
-- Skirt support, 2500 high to shell tangent
NEW CYLI
DIAM 2800.0
HEIG 2500.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 1250.0

-- Skirt base ring
NEW CYLI
DIAM 3100.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 15.0

-- Skirt access opening, DN600
NEW CYLI
DIAM 600.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 38469.0 N -3021.0 U 450.0

-- Skirt vent E
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS E AND Y IS U
POS E 39849.0 N -4401.0 U 2300.0

-- Skirt vent W
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS W AND Y IS U
POS E 37089.0 N -4401.0 U 2300.0

NEW SUBE /205_TA_022_SHELL
-- Conical bottom, 2400 high, DN300 outlet
NEW CONE
DTOP 2800.0
DBOT 300.0
HEIG 2400.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 1300.0

-- Shell: DN2800 x 22000
NEW CYLI
DIAM 2800.0
HEIG 22000.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 13500.0

-- Dished top head, 700 rise
NEW DISH
DIAM 2800.0
HEIG 700.0
RADIUS 2800.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 24850.0

NEW SUBE /205_TA_022_N1
-- N1  DN300  EL +600  -  MC pulp feed inlet (bottom, upflow)
-- N1 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 38469.0 N -2986.0 U 3100.0

-- N1  DN300  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /205_TA_022_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 38469.0 N -2751.0 U 3100.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_022_N2
-- N2  DN300  EL +21120  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 38469.0 N -5816.0 U 23620.0

-- N2  DN300  EL +21120  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /205_TA_022_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 38469.0 N -6051.0 U 23620.0
ORI P1 IS S
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_022_N3
-- N3  DN100  EL +6600  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 39884.0 N -4401.0 U 9100.0

-- N3  DN100  EL +6600  0 deg  -  Chemical injection / sample point
NEW NOZZLE /205_TA_022_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 40069.0 N -4401.0 U 9100.0
ORI P1 IS E
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_022_N4
-- N4  DN100  EL +13200  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 37054.0 N -4401.0 U 15700.0

-- N4  DN100  EL +13200  180 deg  -  Sample point
NEW NOZZLE /205_TA_022_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 36869.0 N -4401.0 U 15700.0
ORI P1 IS W
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_022_N5
-- N5  DN150  EL +22000  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 39029.0 N -4401.0 U 24935.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /205_TA_022_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 39029.0 N -4401.0 U 25120.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_022_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 37054.0 N -4401.0 U 4000.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_022_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 36719.0 N -4401.0 U 4000.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_022_ACCESS
-- Stiffening ring 1 of 5
NEW CYLI
DIAM 3040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 6266.7

-- Stiffening ring 2 of 5
NEW CYLI
DIAM 3040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 9933.3

-- Stiffening ring 3 of 5
NEW CYLI
DIAM 3040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 13600.0

-- Stiffening ring 4 of 5
NEW CYLI
DIAM 3040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 17266.7

-- Stiffening ring 5 of 5
NEW CYLI
DIAM 3040.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 38469.0 N -4401.0 U 20933.3

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 24200.0
ORI Z IS U AND Y IS N
POS E 37069.0 N -4101.0 U 12400.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 24200.0
ORI Z IS U AND Y IS N
POS E 37069.0 N -4701.0 U 12400.0

-- Ladder safety cage required over the 24200 run (8 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
-- Access platform required at EL +6000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +12000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +18000 (Reference Value - extent and support to be set by steel design)

-- ====================================================================
-- 205-TA-025  EOP BLOW TANK
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 43067.0  N -4501.0  U 0.0
-- Shell:       DN3200 x 13000 high
-- Closure:     Conical roof / Conical bottom
-- Support:     Skirt support

NEW EQUI /205_TA_025
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_025_SUPPORT
-- Skirt support, 1500 high to shell tangent
NEW CYLI
DIAM 3200.0
HEIG 1500.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 750.0

-- Skirt base ring
NEW CYLI
DIAM 3500.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 15.0

-- Skirt access opening, DN600
NEW CYLI
DIAM 600.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 43067.0 N -2921.0 U 450.0

-- Skirt vent E
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS E AND Y IS U
POS E 44647.0 N -4501.0 U 1300.0

-- Skirt vent W
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS W AND Y IS U
POS E 41487.0 N -4501.0 U 1300.0

NEW SUBE /205_TA_025_SHELL
-- Conical bottom, 2000 high, DN400 outlet
NEW CONE
DTOP 3200.0
DBOT 400.0
HEIG 2000.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 1000.0

-- Shell: DN3200 x 13000
NEW CYLI
DIAM 3200.0
HEIG 13000.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 8000.0

-- Roof curb / compression ring
NEW CYLI
DIAM 3400.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 14375.0

-- Conical roof, 900 rise
NEW CONE
DTOP 300.0
DBOT 3200.0
HEIG 900.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 14950.0

-- Roof apex cap
NEW CYLI
DIAM 400.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 15430.0

NEW SUBE /205_TA_025_N1
-- N1  DN400  EL +11500  -  Blow line inlet from EOP reactor
-- N1 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 43067.0 N -2886.0 U 13000.0

-- N1  DN400  EL +11500  90 deg  -  Blow line inlet from EOP reactor
NEW NOZZLE /205_TA_025_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 43067.0 N -2551.0 U 13000.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_025_N2
-- N2  DN400  EL +0  -  Bottom cone outlet to pump
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 15.0

-- N2  DN400  bottom nozzle  -  Bottom cone outlet to pump
NEW NOZZLE /205_TA_025_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 43067.0 N -4501.0 U 0.0
ORI P1 IS U
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_025_N3
-- N3  DN600  EL +13000  -  Vapour relief
-- N3 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 43707.0 N -4501.0 U 15055.0

-- N3  DN600  roof nozzle  -  Vapour relief
NEW NOZZLE /205_TA_025_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 43707.0 N -4501.0 U 15390.0
ORI P1 IS U
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_025_N4
-- N4  DN200  EL +6000  -  Dilution filtrate
-- N4 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 41452.0 N -4501.0 U 7500.0

-- N4  DN200  EL +6000  180 deg  -  Dilution filtrate
NEW NOZZLE /205_TA_025_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 41217.0 N -4501.0 U 7500.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_025_M1
-- M1  DN600  EL +2000  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 41452.0 N -4501.0 U 3500.0

-- M1  DN600  EL +2000  135 deg  -  Manway
NEW NOZZLE /205_TA_025_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 41117.0 N -4501.0 U 3500.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_025_ACCESS
-- Stiffening ring 1 of 3
NEW CYLI
DIAM 3440.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 4850.0

-- Stiffening ring 2 of 3
NEW CYLI
DIAM 3440.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 8100.0

-- Stiffening ring 3 of 3
NEW CYLI
DIAM 3440.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 43067.0 N -4501.0 U 11350.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 14200.0
ORI Z IS U AND Y IS N
POS E 41467.0 N -4201.0 U 7400.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 14200.0
ORI Z IS U AND Y IS N
POS E 41467.0 N -4801.0 U 7400.0

-- Ladder safety cage required over the 14200 run (4 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 205-TA-029  EOP FILTRATE TANK
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 39418.0  N 19057.0  U 0.0
-- Shell:       DN3570 x 5300 high
-- Closure:     Conical roof / Flat bottom
-- Support:     Ground / slab bearing

NEW EQUI /205_TA_029
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_029_SHELL
-- Flat bottom plate
NEW CYLI
DIAM 3570.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 39418.0 N 19057.0 U 10.0

-- Shell: DN3570 x 5300
NEW CYLI
DIAM 3570.0
HEIG 5300.0
ORI Z IS U AND Y IS N
POS E 39418.0 N 19057.0 U 2650.0

-- Roof curb / compression ring
NEW CYLI
DIAM 3770.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 39418.0 N 19057.0 U 5175.0

-- Conical roof, 450 rise
NEW CONE
DTOP 300.0
DBOT 3570.0
HEIG 450.0
ORI Z IS U AND Y IS N
POS E 39418.0 N 19057.0 U 5525.0

-- Roof apex cap
NEW CYLI
DIAM 400.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 39418.0 N 19057.0 U 5780.0

NEW SUBE /205_TA_029_N1
-- N1  DN300  EL +4505  -  Stock / filtrate feed inlet
-- N1 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 20857.0 U 4505.0

-- N1  DN300  EL +4505  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /205_TA_029_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 39418.0 N 21092.0 U 4505.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_029_N2
-- N2  DN350  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 570.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 39418.0 N 17257.0 U 400.0

-- N2  DN350  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /205_TA_029_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0XX
POS E 39418.0 N 16922.0 U 400.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_029_N3
-- N3  DN200  EL +4982  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 37618.0 N 19057.0 U 4982.0

-- N3  DN200  EL +4982  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /205_TA_029_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 37383.0 N 19057.0 U 4982.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_029_N4
-- N4  DN150  EL +5300  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 40132.0 N 19057.0 U 5585.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /205_TA_029_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 40132.0 N 19057.0 U 5770.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_029_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /205_TA_029_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 41353.0 N 19057.0 U 250.0
ORI P1 IS E
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_029_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 20857.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_029_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 39418.0 N 21192.0 U 1200.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_029_ACCESS
-- Stiffening ring 1 of 1
NEW CYLI
DIAM 3810.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 39418.0 N 19057.0 U 2750.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 5000.0
ORI Z IS U AND Y IS N
POS E 37633.0 N 19357.0 U 2800.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 5000.0
ORI Z IS U AND Y IS N
POS E 37633.0 N 18757.0 U 2800.0

-- Ladder safety cage required over the 5000 run (1 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 205-TA-036  EOP WASHER DROPLEG
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 41833.0  N 6000.0  U 0.0
-- Shell:       DN1050 x 12000 high
-- Closure:     Flat roof / Conical bottom
-- Support:     Support legs

NEW EQUI /205_TA_036
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_036_SUPPORT
-- 4 support legs on a 1050 bolt circle
-- Support base plate at foundation bearing plane
NEW CYLI
DIAM 1250.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 41833.0 N 6000.0 U 12.5

-- Leg 1
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 42062.8 N 6229.8 U 250.0

-- Leg 1 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 42062.8 N 6229.8 U 12.5

-- Leg 1 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 42030.6 N 6197.6 U 350.0

-- Leg 2
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 41603.2 N 6229.8 U 250.0

-- Leg 2 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 41603.2 N 6229.8 U 12.5

-- Leg 2 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 41635.4 N 6197.6 U 350.0

-- Leg 3
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 41603.2 N 5770.2 U 250.0

-- Leg 3 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 41603.2 N 5770.2 U 12.5

-- Leg 3 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 41635.4 N 5802.4 U 350.0

-- Leg 4
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 42062.8 N 5770.2 U 250.0

-- Leg 4 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 42062.8 N 5770.2 U 12.5

-- Leg 4 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 42030.6 N 5802.4 U 350.0

NEW SUBE /205_TA_036_SHELL
-- Conical bottom, 1200 high, DN400 outlet
NEW CONE
DTOP 1050.0
DBOT 400.0
HEIG 1200.0
ORI Z IS U AND Y IS N
POS E 41833.0 N 6000.0 U 600.0

-- Shell: DN1050 x 12000
NEW CYLI
DIAM 1050.0
HEIG 12000.0
ORI Z IS U AND Y IS N
POS E 41833.0 N 6000.0 U 6500.0

-- Flat roof plate
NEW CYLI
DIAM 1050.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 41833.0 N 6000.0 U 12512.5

-- Roof rim angle
NEW CYLI
DIAM 1250.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 41833.0 N 6000.0 U 12375.0

NEW SUBE /205_TA_036_N1
-- N1  DN400  EL +11640  -  Filtrate inlet from washer vat
-- N1 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 41833.0 N 6540.0 U 12140.0

-- N1  DN400  EL +11640  90 deg  -  Filtrate inlet from washer vat
NEW NOZZLE /205_TA_036_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 41833.0 N 6875.0 U 12140.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_036_N2
-- N2  DN400  EL +300  -  Seal pot / filtrate outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 41833.0 N 5460.0 U 800.0

-- N2  DN400  EL +300  270 deg  -  Seal pot / filtrate outlet
NEW NOZZLE /205_TA_036_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 41833.0 N 5125.0 U 800.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_036_N3
-- N3  DN150  EL +12000  -  Vacuum / air separation vent
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 42043.0 N 6000.0 U 12515.0

-- N3  DN150  roof nozzle  -  Vacuum / air separation vent
NEW NOZZLE /205_TA_036_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 42043.0 N 6000.0 U 12700.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_036_ACCESS
-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 12200.0
ORI Z IS U AND Y IS N
POS E 41308.0 N 6300.0 U 6400.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 12200.0
ORI Z IS U AND Y IS N
POS E 41308.0 N 5700.0 U 6400.0

-- Ladder safety cage required over the 12200 run (4 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 205-TA-042  D1 TOWER
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 49380.0  N -5003.0  U 0.0
-- Shell:       DN3650 x 20000 high
-- Closure:     Flat roof / Conical bottom
-- Support:     Skirt support

NEW EQUI /205_TA_042
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_042_SUPPORT
-- Skirt support, 2500 high to shell tangent
NEW CYLI
DIAM 3650.0
HEIG 2500.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 1250.0

-- Skirt base ring
NEW CYLI
DIAM 3950.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 15.0

-- Skirt access opening, DN600
NEW CYLI
DIAM 600.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 49380.0 N -3198.0 U 450.0

-- Skirt vent E
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS E AND Y IS U
POS E 51185.0 N -5003.0 U 2300.0

-- Skirt vent W
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS W AND Y IS U
POS E 47575.0 N -5003.0 U 2300.0

NEW SUBE /205_TA_042_SHELL
-- Conical bottom, 3500 high, DN350 outlet
NEW CONE
DTOP 3650.0
DBOT 350.0
HEIG 3500.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 1750.0

-- Shell: DN3650 x 20000
NEW CYLI
DIAM 3650.0
HEIG 20000.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 12500.0

-- Flat roof plate
NEW CYLI
DIAM 3650.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 22512.5

-- Roof rim angle
NEW CYLI
DIAM 3850.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 22375.0

NEW SUBE /205_TA_042_N1
-- N1  DN350  EL +600  -  MC pulp feed inlet (bottom, upflow)
-- N1 reinforcing pad
NEW CYLI
DIAM 570.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 49380.0 N -3163.0 U 3100.0

-- N1  DN350  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /205_TA_042_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0XX
POS E 49380.0 N -2828.0 U 3100.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_042_N2
-- N2  DN350  EL +19200  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 570.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 49380.0 N -6843.0 U 21700.0

-- N2  DN350  EL +19200  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /205_TA_042_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0XX
POS E 49380.0 N -7178.0 U 21700.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_042_N3
-- N3  DN100  EL +6000  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 51220.0 N -5003.0 U 8500.0

-- N3  DN100  EL +6000  0 deg  -  Chemical injection / sample point
NEW NOZZLE /205_TA_042_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 51405.0 N -5003.0 U 8500.0
ORI P1 IS E
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_042_N4
-- N4  DN100  EL +12000  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 47540.0 N -5003.0 U 14500.0

-- N4  DN100  EL +12000  180 deg  -  Sample point
NEW NOZZLE /205_TA_042_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 47355.0 N -5003.0 U 14500.0
ORI P1 IS W
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_042_N5
-- N5  DN150  EL +20000  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 50110.0 N -5003.0 U 22515.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /205_TA_042_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 50110.0 N -5003.0 U 22700.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_042_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 47540.0 N -5003.0 U 4000.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_042_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 47205.0 N -5003.0 U 4000.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_042_ACCESS
-- Stiffening ring 1 of 4
NEW CYLI
DIAM 3890.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 6600.0

-- Stiffening ring 2 of 4
NEW CYLI
DIAM 3890.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 10600.0

-- Stiffening ring 3 of 4
NEW CYLI
DIAM 3890.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 14600.0

-- Stiffening ring 4 of 4
NEW CYLI
DIAM 3890.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 49380.0 N -5003.0 U 18600.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 22200.0
ORI Z IS U AND Y IS N
POS E 47555.0 N -4703.0 U 11400.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 22200.0
ORI Z IS U AND Y IS N
POS E 47555.0 N -5303.0 U 11400.0

-- Ladder safety cage required over the 22200 run (7 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
-- Access platform required at EL +6000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +12000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +18000 (Reference Value - extent and support to be set by steel design)

-- ====================================================================
-- 205-TA-045  D1 FILTRATE TANK
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 47423.0  N 19057.0  U 0.0
-- Shell:       DN3500 x 5300 high
-- Closure:     Conical roof / Flat bottom
-- Support:     Ground / slab bearing

NEW EQUI /205_TA_045
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_045_SHELL
-- Flat bottom plate
NEW CYLI
DIAM 3500.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 47423.0 N 19057.0 U 10.0

-- Shell: DN3500 x 5300
NEW CYLI
DIAM 3500.0
HEIG 5300.0
ORI Z IS U AND Y IS N
POS E 47423.0 N 19057.0 U 2650.0

-- Roof curb / compression ring
NEW CYLI
DIAM 3700.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 47423.0 N 19057.0 U 5175.0

-- Conical roof, 450 rise
NEW CONE
DTOP 300.0
DBOT 3500.0
HEIG 450.0
ORI Z IS U AND Y IS N
POS E 47423.0 N 19057.0 U 5525.0

-- Roof apex cap
NEW CYLI
DIAM 400.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 47423.0 N 19057.0 U 5780.0

NEW SUBE /205_TA_045_N1
-- N1  DN300  EL +4505  -  Stock / filtrate feed inlet
-- N1 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 47423.0 N 20822.0 U 4505.0

-- N1  DN300  EL +4505  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /205_TA_045_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 47423.0 N 21057.0 U 4505.0
ORI P1 IS N
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_045_N2
-- N2  DN350  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 570.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 47423.0 N 17292.0 U 400.0

-- N2  DN350  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /205_TA_045_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0XX
POS E 47423.0 N 16957.0 U 400.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_045_N3
-- N3  DN200  EL +4982  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 45658.0 N 19057.0 U 4982.0

-- N3  DN200  EL +4982  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /205_TA_045_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 45423.0 N 19057.0 U 4982.0
ORI P1 IS W
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_045_N4
-- N4  DN150  EL +5300  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 48123.0 N 19057.0 U 5585.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /205_TA_045_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 48123.0 N 19057.0 U 5770.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_045_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /205_TA_045_N5_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 49323.0 N 19057.0 U 250.0
ORI P1 IS E
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_045_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 47423.0 N 20822.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_045_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 47423.0 N 21157.0 U 1200.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_045_ACCESS
-- Stiffening ring 1 of 1
NEW CYLI
DIAM 3740.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 47423.0 N 19057.0 U 2750.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 5000.0
ORI Z IS U AND Y IS N
POS E 45673.0 N 19357.0 U 2800.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 5000.0
ORI Z IS U AND Y IS N
POS E 45673.0 N 18757.0 U 2800.0

-- Ladder safety cage required over the 5000 run (1 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 205-TA-052  D1 WASHER DROPLEG
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 49838.0  N 6000.0  U 0.0
-- Shell:       DN1050 x 12000 high
-- Closure:     Flat roof / Conical bottom
-- Support:     Support legs

NEW EQUI /205_TA_052
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_052_SUPPORT
-- 4 support legs on a 1050 bolt circle
-- Support base plate at foundation bearing plane
NEW CYLI
DIAM 1250.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 49838.0 N 6000.0 U 12.5

-- Leg 1
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 50067.8 N 6229.8 U 250.0

-- Leg 1 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 50067.8 N 6229.8 U 12.5

-- Leg 1 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 50035.6 N 6197.6 U 350.0

-- Leg 2
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 49608.2 N 6229.8 U 250.0

-- Leg 2 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 49608.2 N 6229.8 U 12.5

-- Leg 2 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 49640.4 N 6197.6 U 350.0

-- Leg 3
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 49608.2 N 5770.2 U 250.0

-- Leg 3 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 49608.2 N 5770.2 U 12.5

-- Leg 3 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 49640.4 N 5802.4 U 350.0

-- Leg 4
NEW BOX
XLEN 200.0
YLEN 200.0
ZLEN 500.0
POS E 50067.8 N 5770.2 U 250.0

-- Leg 4 base plate
NEW BOX
XLEN 320.0
YLEN 320.0
ZLEN 25.0
POS E 50067.8 N 5770.2 U 12.5

-- Leg 4 top gusset
NEW BOX
XLEN 300.0
YLEN 300.0
ZLEN 300.0
POS E 50035.6 N 5802.4 U 350.0

NEW SUBE /205_TA_052_SHELL
-- Conical bottom, 1200 high, DN400 outlet
NEW CONE
DTOP 1050.0
DBOT 400.0
HEIG 1200.0
ORI Z IS U AND Y IS N
POS E 49838.0 N 6000.0 U 600.0

-- Shell: DN1050 x 12000
NEW CYLI
DIAM 1050.0
HEIG 12000.0
ORI Z IS U AND Y IS N
POS E 49838.0 N 6000.0 U 6500.0

-- Flat roof plate
NEW CYLI
DIAM 1050.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 49838.0 N 6000.0 U 12512.5

-- Roof rim angle
NEW CYLI
DIAM 1250.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 49838.0 N 6000.0 U 12375.0

NEW SUBE /205_TA_052_N1
-- N1  DN400  EL +11640  -  Filtrate inlet from washer vat
-- N1 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 49838.0 N 6540.0 U 12140.0

-- N1  DN400  EL +11640  90 deg  -  Filtrate inlet from washer vat
NEW NOZZLE /205_TA_052_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 49838.0 N 6875.0 U 12140.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_052_N2
-- N2  DN400  EL +300  -  Seal pot / filtrate outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 49838.0 N 5460.0 U 800.0

-- N2  DN400  EL +300  270 deg  -  Seal pot / filtrate outlet
NEW NOZZLE /205_TA_052_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 49838.0 N 5125.0 U 800.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_052_N3
-- N3  DN150  EL +12000  -  Vacuum / air separation vent
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 50048.0 N 6000.0 U 12515.0

-- N3  DN150  roof nozzle  -  Vacuum / air separation vent
NEW NOZZLE /205_TA_052_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 50048.0 N 6000.0 U 12700.0
ORI P1 IS U
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_052_ACCESS
-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 12200.0
ORI Z IS U AND Y IS N
POS E 49313.0 N 6300.0 U 6400.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 12200.0
ORI Z IS U AND Y IS N
POS E 49313.0 N 5700.0 U 6400.0

-- Ladder safety cage required over the 12200 run (4 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)

-- ====================================================================
-- 205-TA-056  BLEACHED PULP STORAGE TOWER
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 67030.0  N 21008.0  U 0.0
-- Shell:       DN6470 x 26400 high, outer envelope DN9900
-- Closure:     Conical roof / Dished bottom
-- Support:     Ground / slab bearing

NEW EQUI /205_TA_056
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_056_SHELL
-- Bottom plate on slab (dished head has no clearance below grade)
NEW CYLI
DIAM 6470.0
HEIG 20.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 10.0

-- Shell: DN6470 x 26400
NEW CYLI
DIAM 6470.0
HEIG 26400.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 13200.0

-- Roof curb / compression ring
NEW CYLI
DIAM 6670.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 26275.0

-- Conical roof, 1300 rise
NEW CONE
DTOP 300.0
DBOT 6470.0
HEIG 1300.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 27050.0

-- Roof apex cap
NEW CYLI
DIAM 400.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 27730.0

-- Outer shell / insulation envelope DN9900 (annulus 1715 radial)
NEW CYLI
DIAM 9900.0
HEIG 26400.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 13200.0

NEW SUBE /205_TA_056_N1
-- N1  DN400  EL +24000  -  Bleached MC pulp feed inlet (top)
-- N1 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 67030.0 N 25973.0 U 24000.0

-- N1  DN400  EL +24000  90 deg  -  Bleached MC pulp feed inlet (top)
NEW NOZZLE /205_TA_056_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY
POS E 67030.0 N 26308.0 U 24000.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_056_N2
-- N2  DN500  EL +500  -  Bottom discharge to machine chest
-- N2 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 67030.0 N 16043.0 U 500.0

-- N2  DN500  EL +500  270 deg  -  Bottom discharge to machine chest
NEW NOZZLE /205_TA_056_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB011
POS E 67030.0 N 15708.0 U 500.0
ORI P1 IS S
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_056_N3
-- N3  DN200  EL +3000  -  Dilution water
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 71995.0 N 21008.0 U 3000.0

-- N3  DN200  EL +3000  0 deg  -  Dilution water
NEW NOZZLE /205_TA_056_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 72230.0 N 21008.0 U 3000.0
ORI P1 IS E
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_056_N4
-- N4  DN300  EL +26400  -  Vent
-- N4 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 68324.0 N 21008.0 U 27195.0

-- N4  DN300  roof nozzle  -  Vent
NEW NOZZLE /205_TA_056_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW
POS E 68324.0 N 21008.0 U 27430.0
ORI P1 IS U
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_056_M1
-- M1  DN600  EL +1500  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 62065.0 N 21008.0 U 1500.0

-- M1  DN600  EL +1500  135 deg  -  Manway
NEW NOZZLE /205_TA_056_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 61730.0 N 21008.0 U 1500.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_056_ACCESS
-- Stiffening ring 1 of 6
NEW CYLI
DIAM 10140.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 3871.4

-- Stiffening ring 2 of 6
NEW CYLI
DIAM 10140.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 7642.9

-- Stiffening ring 3 of 6
NEW CYLI
DIAM 10140.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 11414.3

-- Stiffening ring 4 of 6
NEW CYLI
DIAM 10140.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 15185.7

-- Stiffening ring 5 of 6
NEW CYLI
DIAM 10140.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 18957.1

-- Stiffening ring 6 of 6
NEW CYLI
DIAM 10140.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 22728.6

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 26100.0
ORI Z IS U AND Y IS N
POS E 62080.0 N 21308.0 U 13350.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 26100.0
ORI Z IS U AND Y IS N
POS E 62080.0 N 20708.0 U 13350.0

-- Ladder safety cage required over the 26100 run (8 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
-- Access platform required at EL +8000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +16000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +24000 (Reference Value - extent and support to be set by steel design)
NEW SUBE /205_TA_056_INTERNALS
-- Agitator mounting pedestal on roof
NEW CYLI
DIAM 776.4
HEIG 400.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 27900.0

-- Agitator mounting flange
NEW CYLI
DIAM 976.4
HEIG 40.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 28120.0

-- Agitator gearbox
NEW BOX
XLEN 1200.0
YLEN 900.0
ZLEN 700.0
POS E 67030.0 N 21008.0 U 28490.0

-- Agitator drive motor
NEW CYLI
DIAM 700.0
HEIG 900.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 29290.0

-- Agitator shaft
NEW CYLI
DIAM 180.0
HEIG 23740.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 15830.0

-- Impeller 1 of 2 hub, DN2264 swept
NEW CYLI
DIAM 324.0
HEIG 150.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 4827.0

-- Impeller 1 of 2 blade E
NEW BOX
XLEN 1042.2
YLEN 120.0
ZLEN 150.0
POS E 67641.1 N 21008.0 U 4827.0

-- Impeller 1 of 2 blade N
NEW BOX
XLEN 120.0
YLEN 1042.2
ZLEN 150.0
POS E 67030.0 N 21619.1 U 4827.0

-- Impeller 1 of 2 blade W
NEW BOX
XLEN 1042.2
YLEN 120.0
ZLEN 150.0
POS E 66418.9 N 21008.0 U 4827.0

-- Impeller 1 of 2 blade S
NEW BOX
XLEN 120.0
YLEN 1042.2
ZLEN 150.0
POS E 67030.0 N 20396.9 U 4827.0

-- Impeller 2 of 2 hub, DN2264 swept
NEW CYLI
DIAM 324.0
HEIG 150.0
ORI Z IS U AND Y IS N
POS E 67030.0 N 21008.0 U 14595.0

-- Impeller 2 of 2 blade E
NEW BOX
XLEN 1042.2
YLEN 120.0
ZLEN 150.0
POS E 67641.1 N 21008.0 U 14595.0

-- Impeller 2 of 2 blade N
NEW BOX
XLEN 120.0
YLEN 1042.2
ZLEN 150.0
POS E 67030.0 N 21619.1 U 14595.0

-- Impeller 2 of 2 blade W
NEW BOX
XLEN 1042.2
YLEN 120.0
ZLEN 150.0
POS E 66418.9 N 21008.0 U 14595.0

-- Impeller 2 of 2 blade S
NEW BOX
XLEN 120.0
YLEN 1042.2
ZLEN 150.0
POS E 67030.0 N 20396.9 U 14595.0


-- ====================================================================
-- 205-TA-059  BLEACH PLANT SCRUBBER
-- ====================================================================
-- Area:        205 - Bleaching Plant
-- Bottom centre (installation coordinate): E 49515.0  N -9553.0  U 0.0
-- Shell:       DN1500 x 14000 high, outer envelope DN2700
-- Closure:     Conical roof / Conical bottom
-- Support:     Skirt support

NEW EQUI /205_TA_059
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_TA_059_SUPPORT
-- Skirt support, 2000 high to shell tangent
NEW CYLI
DIAM 1500.0
HEIG 2000.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 1000.0

-- Skirt base ring
NEW CYLI
DIAM 1800.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 15.0

-- Skirt access opening, DN600
NEW CYLI
DIAM 600.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 49515.0 N -8823.0 U 450.0

-- Skirt vent E
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS E AND Y IS U
POS E 50245.0 N -9553.0 U 1800.0

-- Skirt vent W
NEW CYLI
DIAM 200.0
HEIG 60.0
ORI Z IS W AND Y IS U
POS E 48785.0 N -9553.0 U 1800.0

NEW SUBE /205_TA_059_SHELL
-- Conical bottom, 1200 high, DN200 outlet
NEW CONE
DTOP 1500.0
DBOT 200.0
HEIG 1200.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 1400.0

-- Shell: DN1500 x 14000
NEW CYLI
DIAM 1500.0
HEIG 14000.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 9000.0

-- Roof curb / compression ring
NEW CYLI
DIAM 1700.0
HEIG 250.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 15875.0

-- Conical roof, 400 rise
NEW CONE
DTOP 150.0
DBOT 1500.0
HEIG 400.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 16200.0

-- Roof apex cap
NEW CYLI
DIAM 250.0
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 16430.0

-- Outer shell / insulation envelope DN2700 (annulus 600 radial)
NEW CYLI
DIAM 2700.0
HEIG 14000.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 9000.0

NEW SUBE /205_TA_059_N1
-- N1  DN500  EL +2500  -  Vent gas inlet from bleach stages
-- N1 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 49515.0 N -8188.0 U 4500.0

-- N1  DN500  EL +2500  90 deg  -  Vent gas inlet from bleach stages
NEW NOZZLE /205_TA_059_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB011
POS E 49515.0 N -7853.0 U 4500.0
ORI P1 IS N
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_059_N2
-- N2  DN500  EL +14000  -  Scrubbed gas outlet to stack
-- N2 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 49815.0 N -9553.0 U 16255.0

-- N2  DN500  roof nozzle  -  Scrubbed gas outlet to stack
NEW NOZZLE /205_TA_059_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB011
POS E 49815.0 N -9553.0 U 16590.0
ORI P1 IS U
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_059_N3
-- N3  DN150  EL +12000  -  Caustic scrubbing liquor inlet
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 48150.0 N -9553.0 U 14000.0

-- N3  DN150  EL +12000  180 deg  -  Caustic scrubbing liquor inlet
NEW NOZZLE /205_TA_059_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 47965.0 N -9553.0 U 14000.0
ORI P1 IS W
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_059_N4
-- N4  DN200  EL +0  -  Spent liquor drain from bottom cone
-- N4 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 15.0

-- N4  DN200  bottom nozzle  -  Spent liquor drain from bottom cone
NEW NOZZLE /205_TA_059_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 49515.0 N -9553.0 U 0.0
ORI P1 IS U
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_059_M1
-- M1  DN500  EL +4000  -  Manway - packing access
-- M1 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 48150.0 N -9553.0 U 6000.0

-- M1  DN500  EL +4000  135 deg  -  Manway - packing access
NEW NOZZLE /205_TA_059_M1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB011
POS E 47815.0 N -9553.0 U 6000.0
ORI P1 IS W
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_TA_059_ACCESS
-- Stiffening ring 1 of 3
NEW CYLI
DIAM 2940.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 5600.0

-- Stiffening ring 2 of 3
NEW CYLI
DIAM 2940.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 9100.0

-- Stiffening ring 3 of 3
NEW CYLI
DIAM 2940.0
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 49515.0 N -9553.0 U 12600.0

-- Access ladder stringer A
NEW CYLI
DIAM 60.0
HEIG 15700.0
ORI Z IS U AND Y IS N
POS E 48165.0 N -9253.0 U 8150.0

-- Access ladder stringer B
NEW CYLI
DIAM 60.0
HEIG 15700.0
ORI Z IS U AND Y IS N
POS E 48165.0 N -9853.0 U 8150.0

-- Ladder safety cage required over the 15700 run (5 hoops at 3000 centres, Reference Value - extent and fixings to be set by steel design)
-- Access platform required at EL +5000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +10000 (Reference Value - extent and support to be set by steel design)

-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 113 of 114 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- UNBOUND - ACTION REQUIRED: 1 nozzle(s) have a
-- bore the catalogue does not carry (largest is DN600).
-- These are created and positioned but have no geometry and
-- will not render. They are NOT downsized to the nearest
-- component: an under-sized flange on a real connection would
-- read as correct downstream and mislead the piping designer.

--   203_TA_019_N2_NOZZ  -  DN800
--   OLD /203_TA_019_N2_NOZZ
--   CATR SPCOMPONENT /<a spec carrying DN800>
--   ORI P1 IS <direction>


-- End of macro - 22 equipment, 451 primitives.
