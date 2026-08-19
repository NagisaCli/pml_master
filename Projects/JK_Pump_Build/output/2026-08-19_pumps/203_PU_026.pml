-- 203-PU-026  OXIDISED WL BOOSTER PUMP
-- Generated from location_nozzle_reference.txt (baseplate,
-- position, nozzles), casing_reference.txt (casing),
-- engine_shaft_measurements_updated.csv (motor/shaft) and
-- mc_pump_casing_location_relative_center.txt (MC casing plan).
-- Structure adapted from /P1501B in Reference_pumps.txt.
NEW EQUIPMENT /203_PU_026
DESC 'OXIDISED WL BOOSTER PUMP'
POS E 0mm N 0mm U 0mm
NEW SUBEQUIPMENT /203_PU_026_BASEPLATE
NEW BOX
XLEN 760.1mm
YLEN 1691.4mm
ZLEN 50mm
POS E 13809mm N 372.3mm U 25mm
END
NEW SUBEQUIPMENT /203_PU_026_CASING
NEW CYLINDER
DIAM 361mm
HEIG 81mm
ORI Z is N and Y is U
POS E 13809mm S 323.3mm U 285.6mm
END
NEW DISH
DIAM 371.62mm
HEIG 26.54mm
RADI 5.31mm
ORI Z is S and Y is U
POS E 13809mm S 363.8mm U 285.6mm
END
NEW SUBEQUIPMENT /203_PU_026_SUPPORT
NEW BOX
XLEN 198.55mm
YLEN 72.9mm
ZLEN 127.3mm
POS E 13809mm S 323.3mm U 113.65mm
END
NEW SUBEQUIPMENT /203_PU_026_SUCTION
NEW NOZZLE /203_PU_026_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0PP
POS E 13809mm S 474.7mm U 285.6mm
ORI P1 IS S
HEIG 63.75mm
TEMP -100000degC
PRES 0pascal
TPRESS 0pascal
DUTY unset
END
NEW SUBEQUIPMENT /203_PU_026_DISCHARGE
NEW NOZZLE /203_PU_026_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 13809mm S 323.3mm U 516.1mm
ORI P1 IS U
HEIG 150mm
TEMP -100000degC
PRES 0pascal
TPRESS 0pascal
DUTY unset
END
