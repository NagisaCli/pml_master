-- 205-PU-004  PUMP
-- Generated from location_nozzle_reference.txt (baseplate,
-- position, nozzles), casing_reference.txt (casing),
-- engine_shaft_measurements_updated.csv (motor/shaft) and
-- mc_pump_casing_location_relative_center.txt (MC casing plan).
-- Structure adapted from /P1501B in Reference_pumps.txt.
NEW EQUIPMENT /205_PU_004
DESC 'PUMP'
POS E 0mm N 0mm U 0mm
NEW SUBEQUIPMENT /205_PU_004_BASEPLATE
NEW BOX
XLEN 1725mm
YLEN 760mm
ZLEN 50mm
POS E 30441mm S 10580mm U 25mm
END
NEW SUBEQUIPMENT /205_PU_004_CASING
NEW CYLINDER
DIAM 547.2mm
HEIG 164.16mm
ORI Z is E and Y is U
POS E 30798.7mm S 10580mm U 323.6mm
END
NEW DISH
DIAM 563.29mm
HEIG 40.24mm
RADI 8.05mm
ORI Z is E and Y is U
POS E 30880.78mm S 10580mm U 323.6mm
END
NEW SUBEQUIPMENT /205_PU_004_SUPPORT
NEW BOX
XLEN 147.74mm
YLEN 300.96mm
ZLEN 109.44mm
POS E 30798.7mm S 10580mm U 104.72mm
END
NEW SUBEQUIPMENT /205_PU_004_SUCTION
NEW NOZZLE /205_PU_004_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 31304.1mm S 10580mm U 323.6mm
ORI P1 IS E
HEIG 241.5mm
TEMP -100000degC
PRES 0pascal
TPRESS 0pascal
DUTY unset
END
NEW SUBEQUIPMENT /205_PU_004_DISCHARGE
NEW NOZZLE /205_PU_004_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 30798.7mm S 10580mm U 647.2mm
ORI P1 IS U
HEIG 150mm
TEMP -100000degC
PRES 0pascal
TPRESS 0pascal
DUTY unset
END
