-- ====================================================================
-- PULP MILL - WASHING, SCREENING & BLEACHING (WSB) AREA
-- ====================================================================
-- Project: JK-Project
-- Scope: 22 tank-type equipment items
-- Units: mm
-- Frame: E = East, N = North, U = Up (elevation)
-- Datum: Each tank is positioned by its BOTTOM CENTRE POINT
-- Source: Projects/JK-Project/ equipment list + drawings
-- Generated: 2026-07-24 21:35:18
-- Execution: Select a writable ZONE in E3D, then $$MACRO <this file>


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
POS E 15000.0 N 22625.0 U 7820.0

-- N1  DN400  EL +7820  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /203_TA_006_N1_NOZZ
ORI Y is N and Z is U
POS E 15000.0 N 22610.0 U 7820.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /203_TA_006_N2
-- N2  DN400  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 15000.0 N 17095.0 U 400.0

-- N2  DN400  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /203_TA_006_N2_NOZZ
ORI Y is S and Z is U
POS E 15000.0 N 17110.0 U 400.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /203_TA_006_N3
-- N3  DN200  EL +8648  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 12235.0 N 19860.0 U 8648.0

-- N3  DN200  EL +8648  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /203_TA_006_N3_NOZZ
ORI Y is W and Z is U
POS E 12250.0 N 19860.0 U 8648.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /203_TA_006_N4
-- N4  DN150  EL +9200  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 16120.0 N 19860.0 U 9585.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /203_TA_006_N4_NOZZ
ORI Y is U and Z is N
POS E 16120.0 N 19860.0 U 9570.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /203_TA_006_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /203_TA_006_N5_NOZZ
ORI Y is E and Z is U
POS E 17750.0 N 19860.0 U 250.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN80
END

NEW SUBE /203_TA_006_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 15000.0 N 22625.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /203_TA_006_M1_NOZZ
ORI Y is N and Z is U
POS E 15000.0 N 22610.0 U 1200.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 2
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 11825.0 N 19860.0 U 3266.7

-- Access ladder cage hoop 2 of 2
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 11825.0 N 19860.0 U 6233.3

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
POS E 15445.0 N 7380.0 U 9300.0

-- N1  DN200  EL +7800  90 deg  -  Brown stock feed inlet
NEW NOZZLE /203_TA_019_N1_NOZZ
ORI Y is N and Z is U
POS E 15445.0 N 7365.0 U 9300.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
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
ORI Y is U and Z is N
POS E 15445.0 N 6415.0 U 0.0
HEIG 550.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN800
END

NEW SUBE /203_TA_019_N3
-- N3  DN100  EL +6500  -  Level transmitter LS-3492 connection
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 16410.0 N 6415.0 U 8000.0

-- N3  DN100  EL +6500  0 deg  -  Level transmitter LS-3492 connection
NEW NOZZLE /203_TA_019_N3_NOZZ
ORI Y is E and Z is U
POS E 16395.0 N 6415.0 U 8000.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /203_TA_019_N4
-- N4  DN100  EL +3000  -  Level control LIC-3493 connection
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 14480.0 N 6415.0 U 4500.0

-- N4  DN100  EL +3000  180 deg  -  Level control LIC-3493 connection
NEW NOZZLE /203_TA_019_N4_NOZZ
ORI Y is W and Z is U
POS E 14495.0 N 6415.0 U 4500.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /203_TA_019_N5
-- N5  DN150  EL +8500  -  Vent
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 15845.0 N 6415.0 U 10265.0

-- N5  DN150  roof nozzle  -  Vent
NEW NOZZLE /203_TA_019_N5_NOZZ
ORI Y is U and Z is N
POS E 15845.0 N 6415.0 U 10250.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /203_TA_019_M1
-- M1  DN500  EL +1800  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 14480.0 N 6415.0 U 3300.0

-- M1  DN500  EL +1800  135 deg  -  Manway
NEW NOZZLE /203_TA_019_M1_NOZZ
ORI Y is W and Z is U
POS E 14495.0 N 6415.0 U 3300.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN500
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

-- Access ladder cage hoop 1 of 3
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14070.0 N 6415.0 U 2725.0

-- Access ladder cage hoop 2 of 3
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14070.0 N 6415.0 U 5150.0

-- Access ladder cage hoop 3 of 3
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14070.0 N 6415.0 U 7575.0


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
POS E 12005.0 N -2787.0 U 2600.0

-- N1  DN300  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /203_TA_024_N1_NOZZ
ORI Y is N and Z is U
POS E 12005.0 N -2802.0 U 2600.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /203_TA_024_N2
-- N2  DN300  EL +19488  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 12005.0 N -4717.0 U 21488.0

-- N2  DN300  EL +19488  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /203_TA_024_N2_NOZZ
ORI Y is S and Z is U
POS E 12005.0 N -4702.0 U 21488.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /203_TA_024_N3
-- N3  DN100  EL +6090  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 12970.0 N -3752.0 U 8090.0

-- N3  DN100  EL +6090  0 deg  -  Chemical injection / sample point
NEW NOZZLE /203_TA_024_N3_NOZZ
ORI Y is E and Z is U
POS E 12955.0 N -3752.0 U 8090.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /203_TA_024_N4
-- N4  DN100  EL +12180  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 11040.0 N -3752.0 U 14180.0

-- N4  DN100  EL +12180  180 deg  -  Sample point
NEW NOZZLE /203_TA_024_N4_NOZZ
ORI Y is W and Z is U
POS E 11055.0 N -3752.0 U 14180.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /203_TA_024_N5
-- N5  DN150  EL +20300  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 12405.0 N -3752.0 U 22565.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /203_TA_024_N5_NOZZ
ORI Y is U and Z is N
POS E 12405.0 N -3752.0 U 22550.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /203_TA_024_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 11040.0 N -3752.0 U 3500.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /203_TA_024_M1_NOZZ
ORI Y is W and Z is U
POS E 11055.0 N -3752.0 U 3500.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 10630.0 N -3752.0 U 3050.0

-- Access ladder cage hoop 2 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 10630.0 N -3752.0 U 5800.0

-- Access ladder cage hoop 3 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 10630.0 N -3752.0 U 8550.0

-- Access ladder cage hoop 4 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 10630.0 N -3752.0 U 11300.0

-- Access ladder cage hoop 5 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 10630.0 N -3752.0 U 14050.0

-- Access ladder cage hoop 6 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 10630.0 N -3752.0 U 16800.0

-- Access ladder cage hoop 7 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 10630.0 N -3752.0 U 19550.0

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
POS E 16609.0 N -2487.0 U 2600.0

-- N1  DN300  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /203_TA_029_N1_NOZZ
ORI Y is N and Z is U
POS E 16609.0 N -2502.0 U 2600.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /203_TA_029_N2
-- N2  DN300  EL +22560  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 16609.0 N -5017.0 U 24560.0

-- N2  DN300  EL +22560  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /203_TA_029_N2_NOZZ
ORI Y is S and Z is U
POS E 16609.0 N -5002.0 U 24560.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /203_TA_029_N3
-- N3  DN100  EL +7050  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 17874.0 N -3752.0 U 9050.0

-- N3  DN100  EL +7050  0 deg  -  Chemical injection / sample point
NEW NOZZLE /203_TA_029_N3_NOZZ
ORI Y is E and Z is U
POS E 17859.0 N -3752.0 U 9050.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /203_TA_029_N4
-- N4  DN100  EL +14100  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 15344.0 N -3752.0 U 16100.0

-- N4  DN100  EL +14100  180 deg  -  Sample point
NEW NOZZLE /203_TA_029_N4_NOZZ
ORI Y is W and Z is U
POS E 15359.0 N -3752.0 U 16100.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /203_TA_029_N5
-- N5  DN150  EL +23500  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 17129.0 N -3752.0 U 25855.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /203_TA_029_N5_NOZZ
ORI Y is U and Z is N
POS E 17129.0 N -3752.0 U 25840.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /203_TA_029_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 15344.0 N -3752.0 U 3500.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /203_TA_029_M1_NOZZ
ORI Y is W and Z is U
POS E 15359.0 N -3752.0 U 3500.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14934.0 N -3752.0 U 3100.0

-- Access ladder cage hoop 2 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14934.0 N -3752.0 U 5900.0

-- Access ladder cage hoop 3 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14934.0 N -3752.0 U 8700.0

-- Access ladder cage hoop 4 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14934.0 N -3752.0 U 11500.0

-- Access ladder cage hoop 5 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14934.0 N -3752.0 U 14300.0

-- Access ladder cage hoop 6 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14934.0 N -3752.0 U 17100.0

-- Access ladder cage hoop 7 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14934.0 N -3752.0 U 19900.0

-- Access ladder cage hoop 8 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 14934.0 N -3752.0 U 22700.0

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
ORI Y is N and Z is U
POS E 11601.0 N 4331.0 U 2800.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN80
END

NEW SUBE /203_TA_044_N2
-- N2  DN80  EL +500  -  Air outlet to distribution header
-- N2  DN80  EL +500  270 deg  -  Air outlet to distribution header
NEW NOZZLE /203_TA_044_N2_NOZZ
ORI Y is S and Z is U
POS E 11601.0 N 3631.0 U 1100.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN80
END

NEW SUBE /203_TA_044_N3
-- N3  DN25  EL +0  -  Condensate drain / auto trap
-- N3  DN25  bottom nozzle  -  Condensate drain / auto trap
NEW NOZZLE /203_TA_044_N3_NOZZ
ORI Y is U and Z is N
POS E 11601.0 N 3981.0 U 0.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN25
END

NEW SUBE /203_TA_044_N4
-- N4  DN50  EL +2500  -  Safety relief valve
-- N4  DN50  roof nozzle  -  Safety relief valve
NEW NOZZLE /203_TA_044_N4_NOZZ
ORI Y is U and Z is N
POS E 11761.0 N 3981.0 U 3170.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN50
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
POS E 21008.0 N -2586.0 U 13000.0

-- N1  DN400  EL +11500  90 deg  -  Blow line inlet from O2 reactor
NEW NOZZLE /204_TA_001_N1_NOZZ
ORI Y is N and Z is U
POS E 21008.0 N -2601.0 U 13000.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
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
ORI Y is U and Z is N
POS E 21008.0 N -4151.0 U 0.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /204_TA_001_N3
-- N3  DN600  EL +13000  -  Steam / vapour relief to cyclone
-- N3 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 21648.0 N -4151.0 U 15005.0

-- N3  DN600  roof nozzle  -  Steam / vapour relief to cyclone
NEW NOZZLE /204_TA_001_N3_NOZZ
ORI Y is U and Z is N
POS E 21648.0 N -4151.0 U 14990.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
END

NEW SUBE /204_TA_001_N4
-- N4  DN200  EL +6000  -  Dilution filtrate
-- N4 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 19443.0 N -4151.0 U 7500.0

-- N4  DN200  EL +6000  180 deg  -  Dilution filtrate
NEW NOZZLE /204_TA_001_N4_NOZZ
ORI Y is W and Z is U
POS E 19458.0 N -4151.0 U 7500.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /204_TA_001_M1
-- M1  DN600  EL +2000  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 19443.0 N -4151.0 U 3500.0

-- M1  DN600  EL +2000  135 deg  -  Manway
NEW NOZZLE /204_TA_001_M1_NOZZ
ORI Y is W and Z is U
POS E 19458.0 N -4151.0 U 3500.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 19033.0 N -4151.0 U 3140.0

-- Access ladder cage hoop 2 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 19033.0 N -4151.0 U 5980.0

-- Access ladder cage hoop 3 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 19033.0 N -4151.0 U 8820.0

-- Access ladder cage hoop 4 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 19033.0 N -4151.0 U 11660.0

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
POS E 23650.0 N 6320.0 U 12140.0

-- N1  DN400  EL +11640  90 deg  -  Filtrate inlet from washer vat
NEW NOZZLE /204_TA_021_N1_NOZZ
ORI Y is N and Z is U
POS E 23650.0 N 6305.0 U 12140.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /204_TA_021_N2
-- N2  DN400  EL +300  -  Seal pot / filtrate outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 23650.0 N 5680.0 U 800.0

-- N2  DN400  EL +300  270 deg  -  Seal pot / filtrate outlet
NEW NOZZLE /204_TA_021_N2_NOZZ
ORI Y is S and Z is U
POS E 23650.0 N 5695.0 U 800.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /204_TA_021_N3
-- N3  DN150  EL +12000  -  Vacuum / air separation vent
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 23792.0 N 6000.0 U 12465.0

-- N3  DN150  roof nozzle  -  Vacuum / air separation vent
NEW NOZZLE /204_TA_021_N3_NOZZ
ORI Y is U and Z is N
POS E 23792.0 N 6000.0 U 12450.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
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

-- Access ladder cage hoop 1 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 22920.0 N 6000.0 U 2740.0

-- Access ladder cage hoop 2 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 22920.0 N 6000.0 U 5180.0

-- Access ladder cage hoop 3 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 22920.0 N 6000.0 U 7620.0

-- Access ladder cage hoop 4 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 22920.0 N 6000.0 U 10060.0


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
POS E 22512.0 N 22473.0 U 6460.0

-- N1  DN250  EL +6460  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /204_TA_034_N1_NOZZ
ORI Y is N and Z is U
POS E 22512.0 N 22458.0 U 6460.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN250
END

NEW SUBE /204_TA_034_N2
-- N2  DN300  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 22512.0 N 20243.0 U 400.0

-- N2  DN300  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /204_TA_034_N2_NOZZ
ORI Y is S and Z is U
POS E 22512.0 N 20258.0 U 400.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /204_TA_034_N3
-- N3  DN200  EL +7144  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 21397.0 N 21358.0 U 7144.0

-- N3  DN200  EL +7144  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /204_TA_034_N3_NOZZ
ORI Y is W and Z is U
POS E 21412.0 N 21358.0 U 7144.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /204_TA_034_N4
-- N4  DN150  EL +7600  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 22972.0 N 21358.0 U 7775.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /204_TA_034_N4_NOZZ
ORI Y is U and Z is N
POS E 22972.0 N 21358.0 U 7760.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /204_TA_034_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /204_TA_034_N5_NOZZ
ORI Y is E and Z is U
POS E 23612.0 N 21358.0 U 250.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN80
END

NEW SUBE /204_TA_034_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 22473.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /204_TA_034_M1_NOZZ
ORI Y is N and Z is U
POS E 22512.0 N 22458.0 U 1200.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 2
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 20987.0 N 21358.0 U 2733.3

-- Access ladder cage hoop 2 of 2
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 20987.0 N 21358.0 U 5166.7


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
POS E 27013.0 N 22625.0 U 5500.0

-- N1  DN300  EL +5500  90 deg  -  DN300 filtrate inlet
NEW NOZZLE /204_TA_035_N1_NOZZ
ORI Y is N and Z is U
POS E 27013.0 N 22610.0 U 5500.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /204_TA_035_N2
-- N2  DN400  EL +400  -  Filtrate pump suction
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 27013.0 N 17095.0 U 400.0

-- N2  DN400  EL +400  270 deg  -  Filtrate pump suction
NEW NOZZLE /204_TA_035_N2_NOZZ
ORI Y is S and Z is U
POS E 27013.0 N 17110.0 U 400.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /204_TA_035_N3
-- N3  DN300  EL +7100  -  Overflow
-- N3 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 24248.0 N 19860.0 U 7100.0

-- N3  DN300  EL +7100  180 deg  -  Overflow
NEW NOZZLE /204_TA_035_N3_NOZZ
ORI Y is W and Z is U
POS E 24263.0 N 19860.0 U 7100.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /204_TA_035_N4
-- N4  DN200  EL +7600  -  Vent
-- N4 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 28133.0 N 19860.0 U 7985.0

-- N4  DN200  roof nozzle  -  Vent
NEW NOZZLE /204_TA_035_N4_NOZZ
ORI Y is U and Z is N
POS E 28133.0 N 19860.0 U 7970.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /204_TA_035_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /204_TA_035_N5_NOZZ
ORI Y is E and Z is U
POS E 29763.0 N 19860.0 U 250.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN80
END

NEW SUBE /204_TA_035_M1
-- M1  DN600  EL +1200  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 27013.0 N 22625.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Manway
NEW NOZZLE /204_TA_035_M1_NOZZ
ORI Y is N and Z is U
POS E 27013.0 N 22610.0 U 1200.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 2
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 23838.0 N 19860.0 U 2733.3

-- Access ladder cage hoop 2 of 2
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 23838.0 N 19860.0 U 5166.7

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
POS E 26863.0 N -6236.0 U 24000.0

-- N1  DN400  EL +24000  90 deg  -  MC pulp feed inlet (top)
NEW NOZZLE /205_TA_001_N1_NOZZ
ORI Y is N and Z is U
POS E 26863.0 N -6251.0 U 24000.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /205_TA_001_N2
-- N2  DN500  EL +500  -  Bottom discharge to drop leg
-- N2 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 26863.0 N -16966.0 U 500.0

-- N2  DN500  EL +500  270 deg  -  Bottom discharge to drop leg
NEW NOZZLE /205_TA_001_N2_NOZZ
ORI Y is S and Z is U
POS E 26863.0 N -16951.0 U 500.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN500
END

NEW SUBE /205_TA_001_N3
-- N3  DN200  EL +3000  -  Dilution water ring - lower
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 32228.0 N -11601.0 U 3000.0

-- N3  DN200  EL +3000  0 deg  -  Dilution water ring - lower
NEW NOZZLE /205_TA_001_N3_NOZZ
ORI Y is E and Z is U
POS E 32213.0 N -11601.0 U 3000.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /205_TA_001_N4
-- N4  DN200  EL +3000  -  Dilution water ring - upper
-- N4 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 21498.0 N -11601.0 U 3000.0

-- N4  DN200  EL +3000  180 deg  -  Dilution water ring - upper
NEW NOZZLE /205_TA_001_N4_NOZZ
ORI Y is W and Z is U
POS E 21513.0 N -11601.0 U 3000.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /205_TA_001_N5
-- N5  DN300  EL +26400  -  Vent
-- N5 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 28663.0 N -11601.0 U 27445.0

-- N5  DN300  roof nozzle  -  Vent
NEW NOZZLE /205_TA_001_N5_NOZZ
ORI Y is U and Z is N
POS E 28663.0 N -11601.0 U 27430.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /205_TA_001_M1
-- M1  DN600  EL +1500  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 21498.0 N -11601.0 U 1500.0

-- M1  DN600  EL +1500  135 deg  -  Manway
NEW NOZZLE /205_TA_001_M1_NOZZ
ORI Y is W and Z is U
POS E 21513.0 N -11601.0 U 1500.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 21088.0 N -11601.0 U 3200.0

-- Access ladder cage hoop 2 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 21088.0 N -11601.0 U 6100.0

-- Access ladder cage hoop 3 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 21088.0 N -11601.0 U 9000.0

-- Access ladder cage hoop 4 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 21088.0 N -11601.0 U 11900.0

-- Access ladder cage hoop 5 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 21088.0 N -11601.0 U 14800.0

-- Access ladder cage hoop 6 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 21088.0 N -11601.0 U 17700.0

-- Access ladder cage hoop 7 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 21088.0 N -11601.0 U 20600.0

-- Access ladder cage hoop 8 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 21088.0 N -11601.0 U 23500.0

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
POS E 34016.0 N -3236.0 U 3100.0

-- N1  DN300  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /205_TA_008_N1_NOZZ
ORI Y is N and Z is U
POS E 34016.0 N -3251.0 U 3100.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /205_TA_008_N2
-- N2  DN300  EL +17856  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 34016.0 N -5766.0 U 20356.0

-- N2  DN300  EL +17856  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /205_TA_008_N2_NOZZ
ORI Y is S and Z is U
POS E 34016.0 N -5751.0 U 20356.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /205_TA_008_N3
-- N3  DN100  EL +5580  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 35281.0 N -4501.0 U 8080.0

-- N3  DN100  EL +5580  0 deg  -  Chemical injection / sample point
NEW NOZZLE /205_TA_008_N3_NOZZ
ORI Y is E and Z is U
POS E 35266.0 N -4501.0 U 8080.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /205_TA_008_N4
-- N4  DN100  EL +11160  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 32751.0 N -4501.0 U 13660.0

-- N4  DN100  EL +11160  180 deg  -  Sample point
NEW NOZZLE /205_TA_008_N4_NOZZ
ORI Y is W and Z is U
POS E 32766.0 N -4501.0 U 13660.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /205_TA_008_N5
-- N5  DN150  EL +18600  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 34536.0 N -4501.0 U 21065.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /205_TA_008_N5_NOZZ
ORI Y is U and Z is N
POS E 34536.0 N -4501.0 U 21050.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /205_TA_008_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 32751.0 N -4501.0 U 4000.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_008_M1_NOZZ
ORI Y is W and Z is U
POS E 32766.0 N -4501.0 U 4000.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 6
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32341.0 N -4501.0 U 3271.4

-- Access ladder cage hoop 2 of 6
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32341.0 N -4501.0 U 6242.9

-- Access ladder cage hoop 3 of 6
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32341.0 N -4501.0 U 9214.3

-- Access ladder cage hoop 4 of 6
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32341.0 N -4501.0 U 12185.7

-- Access ladder cage hoop 5 of 6
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32341.0 N -4501.0 U 15157.1

-- Access ladder cage hoop 6 of 6
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32341.0 N -4501.0 U 18128.6

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
POS E 33067.0 N 21022.0 U 4505.0

-- N1  DN300  EL +4505  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /205_TA_011_N1_NOZZ
ORI Y is N and Z is U
POS E 33067.0 N 21007.0 U 4505.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /205_TA_011_N2
-- N2  DN350  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 570.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 33067.0 N 17092.0 U 400.0

-- N2  DN350  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /205_TA_011_N2_NOZZ
ORI Y is S and Z is U
POS E 33067.0 N 17107.0 U 400.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN350
END

NEW SUBE /205_TA_011_N3
-- N3  DN200  EL +4982  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 31102.0 N 19057.0 U 4982.0

-- N3  DN200  EL +4982  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /205_TA_011_N3_NOZZ
ORI Y is W and Z is U
POS E 31117.0 N 19057.0 U 4982.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /205_TA_011_N4
-- N4  DN150  EL +5300  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 33867.0 N 19057.0 U 5565.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /205_TA_011_N4_NOZZ
ORI Y is U and Z is N
POS E 33867.0 N 19057.0 U 5550.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /205_TA_011_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /205_TA_011_N5_NOZZ
ORI Y is E and Z is U
POS E 35017.0 N 19057.0 U 250.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN80
END

NEW SUBE /205_TA_011_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 33067.0 N 21022.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_011_M1_NOZZ
ORI Y is N and Z is U
POS E 33067.0 N 21007.0 U 1200.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 1
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 30692.0 N 19057.0 U 2800.0


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
POS E 33833.0 N 6490.0 U 12140.0

-- N1  DN400  EL +11640  90 deg  -  Filtrate inlet from washer vat
NEW NOZZLE /205_TA_016_N1_NOZZ
ORI Y is N and Z is U
POS E 33833.0 N 6475.0 U 12140.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /205_TA_016_N2
-- N2  DN400  EL +300  -  Seal pot / filtrate outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 33833.0 N 5510.0 U 800.0

-- N2  DN400  EL +300  270 deg  -  Seal pot / filtrate outlet
NEW NOZZLE /205_TA_016_N2_NOZZ
ORI Y is S and Z is U
POS E 33833.0 N 5525.0 U 800.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /205_TA_016_N3
-- N3  DN150  EL +12000  -  Vacuum / air separation vent
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 34043.0 N 6000.0 U 12465.0

-- N3  DN150  roof nozzle  -  Vacuum / air separation vent
NEW NOZZLE /205_TA_016_N3_NOZZ
ORI Y is U and Z is N
POS E 34043.0 N 6000.0 U 12450.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
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

-- Access ladder cage hoop 1 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32933.0 N 6000.0 U 2740.0

-- Access ladder cage hoop 2 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32933.0 N 6000.0 U 5180.0

-- Access ladder cage hoop 3 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32933.0 N 6000.0 U 7620.0

-- Access ladder cage hoop 4 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 32933.0 N 6000.0 U 10060.0


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
POS E 38469.0 N -3036.0 U 3100.0

-- N1  DN300  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /205_TA_022_N1_NOZZ
ORI Y is N and Z is U
POS E 38469.0 N -3051.0 U 3100.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /205_TA_022_N2
-- N2  DN300  EL +21120  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 38469.0 N -5766.0 U 23620.0

-- N2  DN300  EL +21120  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /205_TA_022_N2_NOZZ
ORI Y is S and Z is U
POS E 38469.0 N -5751.0 U 23620.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /205_TA_022_N3
-- N3  DN100  EL +6600  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 39834.0 N -4401.0 U 9100.0

-- N3  DN100  EL +6600  0 deg  -  Chemical injection / sample point
NEW NOZZLE /205_TA_022_N3_NOZZ
ORI Y is E and Z is U
POS E 39819.0 N -4401.0 U 9100.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /205_TA_022_N4
-- N4  DN100  EL +13200  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 37104.0 N -4401.0 U 15700.0

-- N4  DN100  EL +13200  180 deg  -  Sample point
NEW NOZZLE /205_TA_022_N4_NOZZ
ORI Y is W and Z is U
POS E 37119.0 N -4401.0 U 15700.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /205_TA_022_N5
-- N5  DN150  EL +22000  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 39029.0 N -4401.0 U 24885.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /205_TA_022_N5_NOZZ
ORI Y is U and Z is N
POS E 39029.0 N -4401.0 U 24870.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /205_TA_022_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 37104.0 N -4401.0 U 4000.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_022_M1_NOZZ
ORI Y is W and Z is U
POS E 37119.0 N -4401.0 U 4000.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 36694.0 N -4401.0 U 2988.9

-- Access ladder cage hoop 2 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 36694.0 N -4401.0 U 5677.8

-- Access ladder cage hoop 3 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 36694.0 N -4401.0 U 8366.7

-- Access ladder cage hoop 4 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 36694.0 N -4401.0 U 11055.6

-- Access ladder cage hoop 5 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 36694.0 N -4401.0 U 13744.4

-- Access ladder cage hoop 6 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 36694.0 N -4401.0 U 16433.3

-- Access ladder cage hoop 7 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 36694.0 N -4401.0 U 19122.2

-- Access ladder cage hoop 8 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 36694.0 N -4401.0 U 21811.1

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
POS E 43067.0 N -2936.0 U 13000.0

-- N1  DN400  EL +11500  90 deg  -  Blow line inlet from EOP reactor
NEW NOZZLE /205_TA_025_N1_NOZZ
ORI Y is N and Z is U
POS E 43067.0 N -2951.0 U 13000.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
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
ORI Y is U and Z is N
POS E 43067.0 N -4501.0 U 0.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /205_TA_025_N3
-- N3  DN600  EL +13000  -  Vapour relief
-- N3 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 43707.0 N -4501.0 U 15005.0

-- N3  DN600  roof nozzle  -  Vapour relief
NEW NOZZLE /205_TA_025_N3_NOZZ
ORI Y is U and Z is N
POS E 43707.0 N -4501.0 U 14990.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
END

NEW SUBE /205_TA_025_N4
-- N4  DN200  EL +6000  -  Dilution filtrate
-- N4 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 41502.0 N -4501.0 U 7500.0

-- N4  DN200  EL +6000  180 deg  -  Dilution filtrate
NEW NOZZLE /205_TA_025_N4_NOZZ
ORI Y is W and Z is U
POS E 41517.0 N -4501.0 U 7500.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /205_TA_025_M1
-- M1  DN600  EL +2000  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 41502.0 N -4501.0 U 3500.0

-- M1  DN600  EL +2000  135 deg  -  Manway
NEW NOZZLE /205_TA_025_M1_NOZZ
ORI Y is W and Z is U
POS E 41517.0 N -4501.0 U 3500.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 41092.0 N -4501.0 U 3140.0

-- Access ladder cage hoop 2 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 41092.0 N -4501.0 U 5980.0

-- Access ladder cage hoop 3 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 41092.0 N -4501.0 U 8820.0

-- Access ladder cage hoop 4 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 41092.0 N -4501.0 U 11660.0


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
POS E 39418.0 N 20807.0 U 4505.0

-- N1  DN300  EL +4505  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /205_TA_029_N1_NOZZ
ORI Y is N and Z is U
POS E 39418.0 N 20792.0 U 4505.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /205_TA_029_N2
-- N2  DN350  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 570.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 39418.0 N 17307.0 U 400.0

-- N2  DN350  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /205_TA_029_N2_NOZZ
ORI Y is S and Z is U
POS E 39418.0 N 17322.0 U 400.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN350
END

NEW SUBE /205_TA_029_N3
-- N3  DN200  EL +4982  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 37668.0 N 19057.0 U 4982.0

-- N3  DN200  EL +4982  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /205_TA_029_N3_NOZZ
ORI Y is W and Z is U
POS E 37683.0 N 19057.0 U 4982.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /205_TA_029_N4
-- N4  DN150  EL +5300  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 40132.0 N 19057.0 U 5535.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /205_TA_029_N4_NOZZ
ORI Y is U and Z is N
POS E 40132.0 N 19057.0 U 5520.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /205_TA_029_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /205_TA_029_N5_NOZZ
ORI Y is E and Z is U
POS E 41153.0 N 19057.0 U 250.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN80
END

NEW SUBE /205_TA_029_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 20807.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_029_M1_NOZZ
ORI Y is N and Z is U
POS E 39418.0 N 20792.0 U 1200.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 1
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 37258.0 N 19057.0 U 2800.0


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
POS E 41833.0 N 6490.0 U 12140.0

-- N1  DN400  EL +11640  90 deg  -  Filtrate inlet from washer vat
NEW NOZZLE /205_TA_036_N1_NOZZ
ORI Y is N and Z is U
POS E 41833.0 N 6475.0 U 12140.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /205_TA_036_N2
-- N2  DN400  EL +300  -  Seal pot / filtrate outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 41833.0 N 5510.0 U 800.0

-- N2  DN400  EL +300  270 deg  -  Seal pot / filtrate outlet
NEW NOZZLE /205_TA_036_N2_NOZZ
ORI Y is S and Z is U
POS E 41833.0 N 5525.0 U 800.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /205_TA_036_N3
-- N3  DN150  EL +12000  -  Vacuum / air separation vent
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 42043.0 N 6000.0 U 12465.0

-- N3  DN150  roof nozzle  -  Vacuum / air separation vent
NEW NOZZLE /205_TA_036_N3_NOZZ
ORI Y is U and Z is N
POS E 42043.0 N 6000.0 U 12450.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
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

-- Access ladder cage hoop 1 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 40933.0 N 6000.0 U 2740.0

-- Access ladder cage hoop 2 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 40933.0 N 6000.0 U 5180.0

-- Access ladder cage hoop 3 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 40933.0 N 6000.0 U 7620.0

-- Access ladder cage hoop 4 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 40933.0 N 6000.0 U 10060.0


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
POS E 49380.0 N -3213.0 U 3100.0

-- N1  DN350  EL +600  90 deg  -  MC pulp feed inlet (bottom, upflow)
NEW NOZZLE /205_TA_042_N1_NOZZ
ORI Y is N and Z is U
POS E 49380.0 N -3228.0 U 3100.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN350
END

NEW SUBE /205_TA_042_N2
-- N2  DN350  EL +19200  -  Pulp discharge outlet (top)
-- N2 reinforcing pad
NEW CYLI
DIAM 570.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 49380.0 N -6793.0 U 21700.0

-- N2  DN350  EL +19200  270 deg  -  Pulp discharge outlet (top)
NEW NOZZLE /205_TA_042_N2_NOZZ
ORI Y is S and Z is U
POS E 49380.0 N -6778.0 U 21700.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN350
END

NEW SUBE /205_TA_042_N3
-- N3  DN100  EL +6000  -  Chemical injection / sample point
-- N3 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 51170.0 N -5003.0 U 8500.0

-- N3  DN100  EL +6000  0 deg  -  Chemical injection / sample point
NEW NOZZLE /205_TA_042_N3_NOZZ
ORI Y is E and Z is U
POS E 51155.0 N -5003.0 U 8500.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /205_TA_042_N4
-- N4  DN100  EL +12000  -  Sample point
-- N4 reinforcing pad
NEW CYLI
DIAM 320.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 47590.0 N -5003.0 U 14500.0

-- N4  DN100  EL +12000  180 deg  -  Sample point
NEW NOZZLE /205_TA_042_N4_NOZZ
ORI Y is W and Z is U
POS E 47605.0 N -5003.0 U 14500.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN100
END

NEW SUBE /205_TA_042_N5
-- N5  DN150  EL +20000  -  Vent / relief
-- N5 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 50110.0 N -5003.0 U 22465.0

-- N5  DN150  roof nozzle  -  Vent / relief
NEW NOZZLE /205_TA_042_N5_NOZZ
ORI Y is U and Z is N
POS E 50110.0 N -5003.0 U 22450.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /205_TA_042_M1
-- M1  DN600  EL +1500  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 47590.0 N -5003.0 U 4000.0

-- M1  DN600  EL +1500  135 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_042_M1_NOZZ
ORI Y is W and Z is U
POS E 47605.0 N -5003.0 U 4000.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47180.0 N -5003.0 U 3075.0

-- Access ladder cage hoop 2 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47180.0 N -5003.0 U 5850.0

-- Access ladder cage hoop 3 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47180.0 N -5003.0 U 8625.0

-- Access ladder cage hoop 4 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47180.0 N -5003.0 U 11400.0

-- Access ladder cage hoop 5 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47180.0 N -5003.0 U 14175.0

-- Access ladder cage hoop 6 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47180.0 N -5003.0 U 16950.0

-- Access ladder cage hoop 7 of 7
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47180.0 N -5003.0 U 19725.0

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
POS E 47423.0 N 20772.0 U 4505.0

-- N1  DN300  EL +4505  90 deg  -  Stock / filtrate feed inlet
NEW NOZZLE /205_TA_045_N1_NOZZ
ORI Y is N and Z is U
POS E 47423.0 N 20757.0 U 4505.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /205_TA_045_N2
-- N2  DN350  EL +400  -  Pump suction / discharge outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 570.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 47423.0 N 17342.0 U 400.0

-- N2  DN350  EL +400  270 deg  -  Pump suction / discharge outlet
NEW NOZZLE /205_TA_045_N2_NOZZ
ORI Y is S and Z is U
POS E 47423.0 N 17357.0 U 400.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN350
END

NEW SUBE /205_TA_045_N3
-- N3  DN200  EL +4982  -  Overflow to sewer / recovery
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 45708.0 N 19057.0 U 4982.0

-- N3  DN200  EL +4982  180 deg  -  Overflow to sewer / recovery
NEW NOZZLE /205_TA_045_N3_NOZZ
ORI Y is W and Z is U
POS E 45723.0 N 19057.0 U 4982.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /205_TA_045_N4
-- N4  DN150  EL +5300  -  Roof vent
-- N4 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 48123.0 N 19057.0 U 5535.0

-- N4  DN150  roof nozzle  -  Roof vent
NEW NOZZLE /205_TA_045_N4_NOZZ
ORI Y is U and Z is N
POS E 48123.0 N 19057.0 U 5520.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
END

NEW SUBE /205_TA_045_N5
-- N5  DN80  EL +250  -  Drain
-- N5  DN80  EL +250  315 deg  -  Drain
NEW NOZZLE /205_TA_045_N5_NOZZ
ORI Y is E and Z is U
POS E 49123.0 N 19057.0 U 250.0
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN80
END

NEW SUBE /205_TA_045_M1
-- M1  DN600  EL +1200  -  Shell manway - inspection access
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 47423.0 N 20772.0 U 1200.0

-- M1  DN600  EL +1200  45 deg  -  Shell manway - inspection access
NEW NOZZLE /205_TA_045_M1_NOZZ
ORI Y is N and Z is U
POS E 47423.0 N 20757.0 U 1200.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 1
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 45298.0 N 19057.0 U 2800.0


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
POS E 49838.0 N 6490.0 U 12140.0

-- N1  DN400  EL +11640  90 deg  -  Filtrate inlet from washer vat
NEW NOZZLE /205_TA_052_N1_NOZZ
ORI Y is N and Z is U
POS E 49838.0 N 6475.0 U 12140.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /205_TA_052_N2
-- N2  DN400  EL +300  -  Seal pot / filtrate outlet
-- N2 reinforcing pad
NEW CYLI
DIAM 620.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 49838.0 N 5510.0 U 800.0

-- N2  DN400  EL +300  270 deg  -  Seal pot / filtrate outlet
NEW NOZZLE /205_TA_052_N2_NOZZ
ORI Y is S and Z is U
POS E 49838.0 N 5525.0 U 800.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /205_TA_052_N3
-- N3  DN150  EL +12000  -  Vacuum / air separation vent
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 50048.0 N 6000.0 U 12465.0

-- N3  DN150  roof nozzle  -  Vacuum / air separation vent
NEW NOZZLE /205_TA_052_N3_NOZZ
ORI Y is U and Z is N
POS E 50048.0 N 6000.0 U 12450.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
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

-- Access ladder cage hoop 1 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 48938.0 N 6000.0 U 2740.0

-- Access ladder cage hoop 2 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 48938.0 N 6000.0 U 5180.0

-- Access ladder cage hoop 3 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 48938.0 N 6000.0 U 7620.0

-- Access ladder cage hoop 4 of 4
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 48938.0 N 6000.0 U 10060.0


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
POS E 67030.0 N 25923.0 U 24000.0

-- N1  DN400  EL +24000  90 deg  -  Bleached MC pulp feed inlet (top)
NEW NOZZLE /205_TA_056_N1_NOZZ
ORI Y is N and Z is U
POS E 67030.0 N 25908.0 U 24000.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN400
END

NEW SUBE /205_TA_056_N2
-- N2  DN500  EL +500  -  Bottom discharge to machine chest
-- N2 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 67030.0 N 16093.0 U 500.0

-- N2  DN500  EL +500  270 deg  -  Bottom discharge to machine chest
NEW NOZZLE /205_TA_056_N2_NOZZ
ORI Y is S and Z is U
POS E 67030.0 N 16108.0 U 500.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN500
END

NEW SUBE /205_TA_056_N3
-- N3  DN200  EL +3000  -  Dilution water
-- N3 reinforcing pad
NEW CYLI
DIAM 420.0
HEIG 30.0
ORI Z IS E AND Y IS U
POS E 71945.0 N 21008.0 U 3000.0

-- N3  DN200  EL +3000  0 deg  -  Dilution water
NEW NOZZLE /205_TA_056_N3_NOZZ
ORI Y is E and Z is U
POS E 71930.0 N 21008.0 U 3000.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /205_TA_056_N4
-- N4  DN300  EL +26400  -  Vent
-- N4 reinforcing pad
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 68324.0 N 21008.0 U 27145.0

-- N4  DN300  roof nozzle  -  Vent
NEW NOZZLE /205_TA_056_N4_NOZZ
ORI Y is U and Z is N
POS E 68324.0 N 21008.0 U 27130.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN300
END

NEW SUBE /205_TA_056_M1
-- M1  DN600  EL +1500  -  Manway
-- M1 reinforcing pad
NEW CYLI
DIAM 820.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 62115.0 N 21008.0 U 1500.0

-- M1  DN600  EL +1500  135 deg  -  Manway
NEW NOZZLE /205_TA_056_M1_NOZZ
ORI Y is W and Z is U
POS E 62130.0 N 21008.0 U 1500.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN600
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

-- Access ladder cage hoop 1 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 61705.0 N 21008.0 U 3200.0

-- Access ladder cage hoop 2 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 61705.0 N 21008.0 U 6100.0

-- Access ladder cage hoop 3 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 61705.0 N 21008.0 U 9000.0

-- Access ladder cage hoop 4 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 61705.0 N 21008.0 U 11900.0

-- Access ladder cage hoop 5 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 61705.0 N 21008.0 U 14800.0

-- Access ladder cage hoop 6 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 61705.0 N 21008.0 U 17700.0

-- Access ladder cage hoop 7 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 61705.0 N 21008.0 U 20600.0

-- Access ladder cage hoop 8 of 8
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 61705.0 N 21008.0 U 23500.0

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
POS E 49515.0 N -8238.0 U 4500.0

-- N1  DN500  EL +2500  90 deg  -  Vent gas inlet from bleach stages
NEW NOZZLE /205_TA_059_N1_NOZZ
ORI Y is N and Z is U
POS E 49515.0 N -8253.0 U 4500.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN500
END

NEW SUBE /205_TA_059_N2
-- N2  DN500  EL +14000  -  Scrubbed gas outlet to stack
-- N2 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 49815.0 N -9553.0 U 16205.0

-- N2  DN500  roof nozzle  -  Scrubbed gas outlet to stack
NEW NOZZLE /205_TA_059_N2_NOZZ
ORI Y is U and Z is N
POS E 49815.0 N -9553.0 U 16190.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN500
END

NEW SUBE /205_TA_059_N3
-- N3  DN150  EL +12000  -  Caustic scrubbing liquor inlet
-- N3 reinforcing pad
NEW CYLI
DIAM 370.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 48200.0 N -9553.0 U 14000.0

-- N3  DN150  EL +12000  180 deg  -  Caustic scrubbing liquor inlet
NEW NOZZLE /205_TA_059_N3_NOZZ
ORI Y is W and Z is U
POS E 48215.0 N -9553.0 U 14000.0
HEIG 300.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN150
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
ORI Y is U and Z is N
POS E 49515.0 N -9553.0 U 0.0
HEIG 350.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN200
END

NEW SUBE /205_TA_059_M1
-- M1  DN500  EL +4000  -  Manway - packing access
-- M1 reinforcing pad
NEW CYLI
DIAM 720.0
HEIG 30.0
ORI Z IS W AND Y IS U
POS E 48200.0 N -9553.0 U 6000.0

-- M1  DN500  EL +4000  135 deg  -  Manway - packing access
NEW NOZZLE /205_TA_059_M1_NOZZ
ORI Y is W and Z is U
POS E 48215.0 N -9553.0 U 6000.0
HEIG 450.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
-- CATREF to be assigned from ANSI-NOZZLES / 150lb Ansi Flanges, bore DN500
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

-- Access ladder cage hoop 1 of 5
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47790.0 N -9553.0 U 2916.7

-- Access ladder cage hoop 2 of 5
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47790.0 N -9553.0 U 5533.3

-- Access ladder cage hoop 3 of 5
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47790.0 N -9553.0 U 8150.0

-- Access ladder cage hoop 4 of 5
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47790.0 N -9553.0 U 10766.7

-- Access ladder cage hoop 5 of 5
NEW CYLI
DIAM 700.0
HEIG 50.0
ORI Z IS W AND Y IS U
POS E 47790.0 N -9553.0 U 13383.3

-- Access platform required at EL +5000 (Reference Value - extent and support to be set by steel design)
-- Access platform required at EL +10000 (Reference Value - extent and support to be set by steel design)

-- End of macro - 22 equipment, 544 primitives.
