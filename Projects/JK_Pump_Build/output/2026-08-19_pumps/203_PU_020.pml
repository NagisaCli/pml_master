-- 203-PU-020  PUMP
-- Generated from location_nozzle_reference.txt (baseplate,
-- position, nozzles), casing_reference.txt (casing),
-- engine_shaft_measurements_updated.csv (motor/shaft) and
-- mc_pump_casing_location_relative_center.txt (MC casing plan).
-- Structure adapted from /P1501B in Reference_pumps.txt.
NEW EQUIPMENT /203_PU_020
DESC 'PUMP'
POS E 0mm N 0mm U 0mm
NEW SUBEQUIPMENT /203_PU_020_BASEPLATE
NEW BOX
XLEN 926mm
YLEN 760mm
ZLEN 50mm
POS E 17095mm N 5685mm U 25mm
END
NEW SUBEQUIPMENT /203_PU_020_CASING
NEW CYLINDER
DIAM 547.2mm
HEIG 164.16mm
ORI Z is E and Y is U
POS E 16863.7mm N 5685mm U 323.6mm
END
NEW DISH
DIAM 563.29mm
HEIG 40.24mm
RADI 8.05mm
ORI Z is W and Y is U
POS E 16781.62mm N 5685mm U 323.6mm
END
NEW SUBEQUIPMENT /203_PU_020_SUPPORT
NEW BOX
XLEN 147.74mm
YLEN 300.96mm
ZLEN 109.44mm
POS E 16863.7mm N 5685mm U 104.72mm
END
NEW SUBEQUIPMENT /203_PU_020_SUCTION
NEW NOZZLE /203_PU_020_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB011
POS E 16580.3mm N 5685mm U 323.6mm
ORI P1 IS W
HEIG 150mm
TEMP -100000degC
PRES 0pascal
TPRESS 0pascal
DUTY unset
END
NEW SUBEQUIPMENT /203_PU_020_DISCHARGE
NEW NOZZLE /203_PU_020_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 16863.7mm N 5685mm U 647.2mm
ORI P1 IS U
HEIG 150mm
TEMP -100000degC
PRES 0pascal
TPRESS 0pascal
DUTY unset
END
