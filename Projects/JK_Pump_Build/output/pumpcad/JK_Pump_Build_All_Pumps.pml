-- ====================================================================
-- JK_Pump_Build - all pumps (pumpcad reconstruction)
-- ====================================================================
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Pumps in this file: 30
-- Generated: 2026-08-13 03:44:51
--
-- Each pump is a separate EQUI, in tag order:
--   203-PU-008  (plan)
--   203-PU-009  (plan)
--   203-PU-011  (plan)
--   203-PU-020  (unknown)
--   203-PU-026  (plan)
--   203-PU-031  (plan)
--   204-PU-003  (plan)
--   204-PU-006  (plan)
--   204-PU-008  (plan)
--   204-PU-015  (plan)
--   204-PU-016  (plan)
--   204-PU-017  (plan)
--   204-PU-023  (plan)
--   205-PU-004  (unknown)
--   205-PU-012  (plan)
--   205-PU-013  (plan)
--   205-PU-018  (plan)
--   205-PU-024  (plan)
--   205-PU-027  (plan)
--   205-PU-030  (plan)
--   205-PU-031  (plan)
--   205-PU-032  (plan)
--   205-PU-038  (plan)
--   205-PU-046  (plan)
--   205-PU-047  (plan)
--   205-PU-048  (plan)
--   205-PU-049  (plan)
--   205-PU-054  (plan)
--   205-PU-060  (plan)
--   205-PU-061  (plan)
--
-- Execution: select a writable ZONE, then $M <this file>
-- The per-pump macros in pumps\ remain available for loading one
-- pump at a time; this file is the same content concatenated.
-- ====================================================================


-- --------------------------------------------------------------------
-- 203-PU-008
-- --------------------------------------------------------------------
-- 203-PU-008 - BLOW TANK DILUTION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 203-PU-008
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 216 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 151 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /203_PU_008
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_008_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 852.0
YLEN 2136.0
ZLEN 50.0
POS E 13971.0 N 14110.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.6
HEIG 38.3
ORI Z IS U AND Y IS N
POS E 13596.1 N 13132.0 U 69.2

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 13596.12mm N 13132mm U 88.34mm
ORI Y IS N AND Z IS U
HEIG 20.448mm

NEW LOOP
NEW VERTEX
POS E 21.726mm N 12.543512mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.087024mm U 0mm
END
NEW VERTEX
POS E -21.726mm N 12.543512mm U 0mm
END
NEW VERTEX
POS E -21.726mm N -12.543512mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.087024mm U 0mm
END
NEW VERTEX
POS E 21.726mm N -12.543512mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.6
HEIG 38.3
ORI Z IS U AND Y IS N
POS E 13596.1 N 15088.0 U 69.2

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 13596.12mm N 15088mm U 88.34mm
ORI Y IS N AND Z IS U
HEIG 20.448mm

NEW LOOP
NEW VERTEX
POS E 21.726mm N 12.543512mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.087024mm U 0mm
END
NEW VERTEX
POS E -21.726mm N 12.543512mm U 0mm
END
NEW VERTEX
POS E -21.726mm N -12.543512mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.087024mm U 0mm
END
NEW VERTEX
POS E 21.726mm N -12.543512mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.6
HEIG 38.3
ORI Z IS U AND Y IS N
POS E 14345.9 N 13132.0 U 69.2

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 14345.88mm N 13132mm U 88.34mm
ORI Y IS N AND Z IS U
HEIG 20.448mm

NEW LOOP
NEW VERTEX
POS E 21.726mm N 12.543512mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.087024mm U 0mm
END
NEW VERTEX
POS E -21.726mm N 12.543512mm U 0mm
END
NEW VERTEX
POS E -21.726mm N -12.543512mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.087024mm U 0mm
END
NEW VERTEX
POS E 21.726mm N -12.543512mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.6
HEIG 38.3
ORI Z IS U AND Y IS N
POS E 14345.9 N 15088.0 U 69.2

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 14345.88mm N 15088mm U 88.34mm
ORI Y IS N AND Z IS U
HEIG 20.448mm

NEW LOOP
NEW VERTEX
POS E 21.726mm N 12.543512mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.087024mm U 0mm
END
NEW VERTEX
POS E -21.726mm N 12.543512mm U 0mm
END
NEW VERTEX
POS E -21.726mm N -12.543512mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.087024mm U 0mm
END
NEW VERTEX
POS E 21.726mm N -12.543512mm U 0mm
END
END
END

NEW SUBE /203_PU_008_SUPPORT
-- 16 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 242.2
YLEN 29.8
ZLEN 25.3
POS E 14210.1 N 14045.3 U 62.6

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 122.1
YLEN 15.0
ZLEN 57.1
POS E 14210.1 N 14045.3 U 103.8

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 14262.785059mm N 14037.547165mm U 75.267926mm
ORI Y IS U AND Z IS E
HEIG 21.056605mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 15.525607mm N 0mm U 0mm
END
NEW VERTEX
POS E 8.539084mm N 50.24965mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 14136.445428mm N 14037.547165mm U 75.267926mm
ORI Y IS U AND Z IS E
HEIG 21.056605mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 15.525607mm N 0mm U 0mm
END
NEW VERTEX
POS E 8.539084mm N 50.24965mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 13.7
HEIG 39.0
ORI Z IS U AND Y IS N
POS E 14210.1 N 14036.0 U 62.6

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 14210.143546mm N 14035.994604mm U 75.267926mm
ORI Y IS N AND Z IS U
HEIG 10.949435mm

NEW LOOP
NEW VERTEX
POS E 11.633774mm N 6.716763mm U 0mm
END
NEW VERTEX
POS E 0mm N 13.433525mm U 0mm
END
NEW VERTEX
POS E -11.633774mm N 6.716763mm U 0mm
END
NEW VERTEX
POS E -11.633774mm N -6.716763mm U 0mm
END
NEW VERTEX
POS E 0mm N -13.433525mm U 0mm
END
NEW VERTEX
POS E 11.633774mm N -6.716763mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 13.7
HEIG 39.0
ORI Z IS U AND Y IS N
POS E 14210.1 N 14054.6 U 62.6

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 14210.143546mm N 14054.625333mm U 75.267926mm
ORI Y IS N AND Z IS U
HEIG 10.949435mm

NEW LOOP
NEW VERTEX
POS E 11.633774mm N 6.716763mm U 0mm
END
NEW VERTEX
POS E 0mm N 13.433525mm U 0mm
END
NEW VERTEX
POS E -11.633774mm N 6.716763mm U 0mm
END
NEW VERTEX
POS E -11.633774mm N -6.716763mm U 0mm
END
NEW VERTEX
POS E 0mm N -13.433525mm U 0mm
END
NEW VERTEX
POS E 11.633774mm N -6.716763mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 165.3
YLEN 120.9
ZLEN 17.2
POS E 14043.0 N 15023.7 U 58.6

-- Casing support: pedestal web
NEW BOX
XLEN 83.4
YLEN 61.0
ZLEN 106.7
POS E 14043.0 N 15023.7 U 120.6

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 14078.957589mm N 14992.210298mm U 67.246366mm
ORI Y IS U AND Z IS E
HEIG 14.371972mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 63.07278mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.690029mm N 93.884344mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 13992.725758mm N 14992.210298mm U 67.246366mm
ORI Y IS U AND Z IS E
HEIG 14.371972mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 63.07278mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.690029mm N 93.884344mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 29.2
ORI Z IS U AND Y IS N
POS E 14043.0 N 14985.9 U 58.6

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 14043.027659mm N 14985.90302mm U 67.246366mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 29.2
ORI Z IS U AND Y IS N
POS E 14043.0 N 15061.6 U 58.6

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 14043.027659mm N 15061.590357mm U 67.246366mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /203_PU_008_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 210x232 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22F2E9,22F2EA,22F2EB,22F2EC,22F2ED,22F2EE
NEW CYLI
DIAM 231.8
HEIG 210.2
ORI Z IS N AND Y IS U
POS E 14043.0 N 15023.7 U 285.2

-- volute closing onto the suction cover
NEW CONE
DTOP 143.7
DBOT 231.8
HEIG 38.5
ORI Z IS N AND Y IS U
POS E 14043.0 N 15148.1 U 285.2

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 97.4
HEIG 37.8
ORI Z IS N AND Y IS U
POS E 14043.0 N 14899.7 U 285.2

-- Reference Value: axial casing rib
NEW CYLI
DIAM 10.4
HEIG 109.3
ORI Z IS N AND Y IS U
POS E 14163.1 N 15023.7 U 285.2

-- Reference Value: axial casing rib
NEW CYLI
DIAM 10.4
HEIG 109.3
ORI Z IS N AND Y IS U
POS E 13923.0 N 15023.7 U 285.2

NEW SUBE /203_PU_008_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 32x340 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 22F2DB,22F2DC
NEW CYLI
DIAM 339.6
HEIG 32.3
ORI Z IS N AND Y IS U
POS E 14210.1 N 14045.3 U 285.2

NEW SUBE /203_PU_008_COUPLING
-- 3 part(s), 0 nozzle(s)
-- CouplingGuard [MEDIUM]: body 857x264 spanning the gap between driver and wet end, the coupling guard position
-- CAD handles: 22F2E4,22F2E5,22F2E6,22F2E7,22F2E8,22F32B ...
NEW BOX
XLEN 264.2
YLEN 857.1
ZLEN 264.2
POS E 14247.9 N 14490.1 U 285.2

-- Coupling guard end plate
NEW CYLI
DIAM 243.0
HEIG 21.1
ORI Z IS N AND Y IS U
POS E 14247.9 N 14072.0 U 285.2

-- Coupling guard end plate
NEW CYLI
DIAM 243.0
HEIG 21.1
ORI Z IS N AND Y IS U
POS E 14247.9 N 14908.1 U 285.2

NEW SUBE /203_PU_008_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /203_PU_008_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 13971.0 N 15172.3 U 285.2
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_008_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /203_PU_008_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 14043.0 N 15023.7 U 551.1
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 203-PU-009
-- --------------------------------------------------------------------
-- 203-PU-009 - BSW FILTRATE PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 203-PU-009
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 221 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 151 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /203_PU_009
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_009_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 857.0
YLEN 2129.0
ZLEN 50.0
POS E 16137.0 N 14089.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 15759.9 N 13114.5 U 69.3

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 15759.92mm N 13114.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 15759.9 N 15063.5 U 69.3

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 15759.92mm N 15063.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 16514.1 N 13114.5 U 69.3

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 16514.08mm N 13114.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 16514.1 N 15063.5 U 69.3

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 16514.08mm N 15063.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

NEW SUBE /203_PU_009_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 186.5
ZLEN 73.7
POS E 16139.7 N 13260.8 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.1
ZLEN 62.1
POS E 16139.7 N 13260.8 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 16293.334189mm N 13212.08892mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15924.601012mm N 13212.08892mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 16139.7 N 13202.4 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 16139.695365mm N 13202.356305mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 16139.7 N 13319.1 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 16139.695365mm N 13319.147687mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 186.5
ZLEN 73.7
POS E 16139.7 N 13871.4 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.1
ZLEN 62.1
POS E 16139.7 N 13871.4 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 16293.334189mm N 13822.762813mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15924.601012mm N 13822.762813mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 16139.7 N 13813.0 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 16139.695365mm N 13813.030198mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 16139.7 N 13929.8 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 16139.695365mm N 13929.82158mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 157.6
YLEN 401.7
ZLEN 16.4
POS E 16137.0 N 14261.5 U 58.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 79.5
YLEN 202.6
ZLEN 311.0
POS E 16137.0 N 14261.5 U 222.0

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 16171.258674mm N 14156.708926mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 273.723212mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 16089.037665mm N 14156.708926mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 273.723212mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 16137.0 N 14135.7 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 16136.99992mm N 14135.749356mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 16137.0 N 14387.3 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 16136.99992mm N 14387.264196mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 465.1
YLEN 131.3
ZLEN 48.5
POS E 16169.3 N 15005.4 U 74.3

-- Casing support: pedestal web
NEW BOX
XLEN 234.6
YLEN 66.2
ZLEN 65.3
POS E 16169.3 N 15005.4 U 131.2

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 16270.450072mm N 14971.196845mm U 98.530465mm
ORI Y IS U AND Z IS E
HEIG 40.442054mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 68.490576mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.669817mm N 57.485088mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 16027.797746mm N 14971.196845mm U 98.530465mm
ORI Y IS U AND Z IS E
HEIG 40.442054mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 68.490576mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.669817mm N 57.485088mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.3
HEIG 74.8
ORI Z IS U AND Y IS N
POS E 16169.3 N 14964.3 U 74.3

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 16169.344936mm N 14964.347787mm U 98.530465mm
ORI Y IS N AND Z IS U
HEIG 21.029868mm

NEW LOOP
NEW VERTEX
POS E 22.344235mm N 12.90045mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.8009mm U 0mm
END
NEW VERTEX
POS E -22.344235mm N 12.90045mm U 0mm
END
NEW VERTEX
POS E -22.344235mm N -12.90045mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.8009mm U 0mm
END
NEW VERTEX
POS E 22.344235mm N -12.90045mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.3
HEIG 74.8
ORI Z IS U AND Y IS N
POS E 16169.3 N 15046.5 U 74.3

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 16169.344936mm N 15046.536479mm U 98.530465mm
ORI Y IS N AND Z IS U
HEIG 21.029868mm

NEW LOOP
NEW VERTEX
POS E 22.344235mm N 12.90045mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.8009mm U 0mm
END
NEW VERTEX
POS E -22.344235mm N 12.90045mm U 0mm
END
NEW VERTEX
POS E -22.344235mm N -12.90045mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.8009mm U 0mm
END
NEW VERTEX
POS E 22.344235mm N -12.90045mm U 0mm
END
END
END

NEW SUBE /203_PU_009_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 210x652 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22BB79,22BB7A,22BB7B,22BB7C,22BB7D,22BB7E ...
NEW CYLI
DIAM 652.3
HEIG 228.3
ORI Z IS N AND Y IS U
POS E 16169.3 N 15005.4 U 477.0

-- volute closing onto the suction cover
NEW CONE
DTOP 404.4
DBOT 652.3
HEIG 24.1
ORI Z IS N AND Y IS U
POS E 16169.3 N 15131.6 U 477.0

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 274.0
HEIG 41.1
ORI Z IS N AND Y IS U
POS E 16169.3 N 14870.7 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 118.7
ORI Z IS N AND Y IS U
POS E 16502.7 N 15005.4 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 118.7
ORI Z IS N AND Y IS U
POS E 15836.0 N 15005.4 U 477.0

NEW SUBE /203_PU_009_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 437x221 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 22BB58,22BB59,22BB5A
NEW CYLI
DIAM 221.0
HEIG 436.7
ORI Z IS N AND Y IS U
POS E 16137.0 N 14261.5 U 477.0

NEW SUBE /203_PU_009_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 199 mm apart running 248 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BB5C,22BB5B
NEW CYLI
DIAM 199.5
HEIG 248.0
ORI Z IS N AND Y IS U
POS E 16137.0 N 14603.8 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 16137.0 N 14507.1 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 16137.0 N 14700.5 U 477.0

NEW SUBE /203_PU_009_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 954 mm along the machine axis x 647 mm across, consolidated from 2 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BB86,22BB87,22BB88,22BB8C,22BB8D,22BB8E ...
NEW CYLI
DIAM 646.9
HEIG 954.2
ORI Z IS N AND Y IS U
POS E 16139.7 N 13566.1 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 16139.7 N 13117.6 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 16139.7 N 14014.6 U 477.0

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 15808.2 N 13566.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 15833.5 N 13566.1 U 603.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 15905.3 N 13566.1 U 711.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16012.9 N 13566.1 U 783.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16139.7 N 13566.1 U 808.4

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16266.5 N 13566.1 U 783.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16374.1 N 13566.1 U 711.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16445.9 N 13566.1 U 603.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16471.1 N 13566.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16445.9 N 13566.1 U 350.1

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16374.1 N 13566.1 U 242.6

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16266.5 N 13566.1 U 170.7

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16139.7 N 13566.1 U 145.5

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 16012.9 N 13566.1 U 170.7

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 15905.3 N 13566.1 U 242.6

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 15833.5 N 13566.1 U 350.1

-- Motor terminal box
NEW BOX
XLEN 258.8
YLEN 286.3
ZLEN 142.3
POS E 16139.7 N 13566.1 U 871.6

-- Motor cable gland
NEW CYLI
DIAM 48.4
HEIG 142.3
ORI Z IS E AND Y IS U
POS E 15939.2 N 13566.1 U 871.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.3
YLEN 77.6
ZLEN 64.7
POS E 16139.7 N 13298.9 U 878.7

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.1
YLEN 171.8
ZLEN 6.0
POS E 16465.1 N 13680.6 U 477.0

-- Motor fan cowl disc
NEW CYLI
DIAM 711.6
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 16139.7 N 13085.0 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 16303.4 N 13085.0 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 15976.0 N 13085.0 U 477.0

NEW SUBE /203_PU_009_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 173x334 at the wet end, outboard of the casing
-- CAD handles: 22BB5D,22BB5E,22BB5F
NEW BOX
XLEN 334.2
YLEN 172.5
ZLEN 138.0
POS E 16139.7 N 14814.1 U 119.0

NEW SUBE /203_PU_009_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /203_PU_009_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 16137.0 N 15154.0 U 477.0
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_009_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /203_PU_009_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 16169.3 N 15005.4 U 953.1
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 203-PU-011
-- --------------------------------------------------------------------
-- 203-PU-011 - BROWN STOCK DD WASHER RETURN FILTRATE PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 203-PU-011
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 92 mm snapped to catalogue DN90 (nearest available in 'AAZFBB0MM'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /203_PU_011
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_011_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 17685.0 N 170.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 17350.6 N -600.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 17350.6mm N -600mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 17350.6 N 940.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 17350.6mm N 940mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 18019.4 N -600.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 18019.4mm N -600mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 18019.4 N 940.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 18019.4mm N 940mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /203_PU_011_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 257.5
YLEN 416.6
ZLEN 26.9
POS E 17685.0 N 253.6 U 63.4

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 129.9
YLEN 210.1
ZLEN 73.9
POS E 17685.0 N 253.6 U 113.8

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 17740.983815mm N 144.878731mm U 76.872231mm
ORI Y IS U AND Z IS E
HEIG 22.393526mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 217.358504mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.547177mm N 65.016604mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 17606.62266mm N 144.878731mm U 76.872231mm
ORI Y IS U AND Z IS E
HEIG 22.393526mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 217.358504mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.547177mm N 65.016604mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 17685.0 N 123.1 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 17685mm N 123.142881mm U 76.872231mm
ORI Y IS N AND Z IS U
HEIG 11.644633mm

NEW LOOP
NEW VERTEX
POS E 12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.286444mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N -7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.286444mm U 0mm
END
NEW VERTEX
POS E 12.372423mm N -7.143222mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 17685.0 N 384.0 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 17685mm N 383.973086mm U 76.872231mm
ORI Y IS N AND Z IS U
HEIG 11.644633mm

NEW LOOP
NEW VERTEX
POS E 12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.286444mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N -7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.286444mm U 0mm
END
NEW VERTEX
POS E 12.372423mm N -7.143222mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 435.8
YLEN 118.0
ZLEN 45.5
POS E 17687.7 N -451.8 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 219.8
YLEN 59.5
ZLEN 38.3
POS E 17687.7 N -451.8 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 17782.439373mm N -482.57149mm U 95.477086mm
ORI Y IS U AND Z IS E
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584915mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871703mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 17555.053944mm N -482.57149mm U 95.477086mm
ORI Y IS U AND Z IS E
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584915mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871703mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 17687.7 N -488.7 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 17687.695444mm N -488.729981mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 17687.7 N -414.8 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 17687.695444mm N -414.828083mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 435.8
YLEN 118.0
ZLEN 45.5
POS E 17687.7 N -65.4 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 219.8
YLEN 59.5
ZLEN 38.3
POS E 17687.7 N -65.4 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 17782.439373mm N -96.156337mm U 95.477086mm
ORI Y IS U AND Z IS E
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584915mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871703mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 17555.053944mm N -96.156337mm U 95.477086mm
ORI Y IS U AND Z IS E
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584915mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871703mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 17687.7 N -102.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 17687.695444mm N -102.314828mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 17687.7 N -28.4 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 17687.695444mm N -28.41293mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 143.2
YLEN 71.6
ZLEN 14.9
POS E 17687.0 N 880.9 U 57.5

-- Casing support: pedestal web
NEW BOX
XLEN 72.2
YLEN 36.1
ZLEN 152.0
POS E 17687.0 N 880.9 U 140.9

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 17718.142046mm N 862.244151mm U 64.937832mm
ORI Y IS U AND Z IS E
HEIG 12.448193mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.344579mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.539518mm N 133.740159mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 17643.452888mm N 862.244151mm U 64.937832mm
ORI Y IS U AND Z IS E
HEIG 12.448193mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.344579mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.539518mm N 133.740159mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 26.9
ORI Z IS U AND Y IS N
POS E 17687.0 N 858.5 U 57.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 17687.021563mm N 858.509693mm U 64.937832mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 26.9
ORI Z IS U AND Y IS N
POS E 17687.0 N 903.3 U 57.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 17687.021563mm N 903.323188mm U 64.937832mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /203_PU_011_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 100; the only large round feature in the plan, at the wet end
-- CAD handles: 22BBA7,22BBA0,22BBA1,22BBA2,22BBA3,22BBA4 ...
NEW CYLI
DIAM 200.8
HEIG 124.5
ORI Z IS U AND Y IS N
POS E 17687.0 N 880.9 U 313.3

-- casing split flange at the cover joint
NEW CYLI
DIAM 220.9
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 17687.0 N 880.9 U 383.5

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 17687.0 N 980.5 U 373.9

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 17687.021563mm N 980.543959mm U 391.529356mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 17616.6 N 951.4 U 373.9

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 17616.57427mm N 951.363734mm U 391.529356mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 17587.4 N 880.9 U 373.9

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 17587.394046mm N 880.916441mm U 391.529356mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 17616.6 N 810.5 U 373.9

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 17616.57427mm N 810.469147mm U 391.529356mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 17687.0 N 781.3 U 373.9

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 17687.021563mm N 781.288923mm U 391.529356mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 17757.5 N 810.5 U 373.9

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 17757.468857mm N 810.469147mm U 391.529356mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 17786.6 N 880.9 U 373.9

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 17786.649081mm N 880.916441mm U 391.529356mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 17757.5 N 951.4 U 373.9

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 17757.468857mm N 951.363734mm U 391.529356mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 124.5
DBOT 200.8
HEIG 37.3
ORI Z IS N AND Y IS U
POS E 17687.0 N 961.8 U 313.3

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 84.3
HEIG 22.4
ORI Z IS N AND Y IS U
POS E 17687.0 N 807.5 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 64.7
ORI Z IS N AND Y IS U
POS E 17791.0 N 880.9 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 64.7
ORI Z IS N AND Y IS U
POS E 17583.0 N 880.9 U 313.3

NEW SUBE /203_PU_011_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 453 mm along the machine axis x 361 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22BBDC,22BBDD,22BBDE,22BBA8,22BBA9,22BBAA
NEW CYLI
DIAM 361.2
HEIG 452.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 253.6 U 313.3

NEW SUBE /203_PU_011_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 226 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BBCE,22BBCD
NEW CYLI
DIAM 134.8
HEIG 226.4
ORI Z IS N AND Y IS U
POS E 17685.0 N 593.2 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 49.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 504.9 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 49.8
ORI Z IS N AND Y IS U
POS E 17685.0 N 681.5 U 313.3

NEW SUBE /203_PU_011_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 604 mm along the machine axis x 399 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BBD6,22BBD7,22BBD8,22BBD9,22BBDA,22BBDB ...
NEW CYLI
DIAM 398.9
HEIG 603.8
ORI Z IS N AND Y IS U
POS E 17687.7 N -258.6 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS N AND Y IS U
POS E 17687.7 N -542.3 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS N AND Y IS U
POS E 17687.7 N 25.2 U 313.3

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17482.6 N -258.6 U 313.3

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17498.3 N -258.6 U 391.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17542.7 N -258.6 U 458.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17609.2 N -258.6 U 502.7

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17687.7 N -258.6 U 518.3

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17766.2 N -258.6 U 502.7

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17832.7 N -258.6 U 458.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17877.1 N -258.6 U 391.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17892.7 N -258.6 U 313.3

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17877.1 N -258.6 U 234.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17832.7 N -258.6 U 168.3

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17766.2 N -258.6 U 123.9

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17687.7 N -258.6 U 108.2

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17609.2 N -258.6 U 123.9

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17542.7 N -258.6 U 168.3

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 17498.3 N -258.6 U 234.8

-- Motor terminal box
NEW BOX
XLEN 159.6
YLEN 181.1
ZLEN 87.8
POS E 17687.7 N -258.6 U 556.6

-- Motor cable gland
NEW CYLI
DIAM 29.8
HEIG 87.8
ORI Z IS E AND Y IS U
POS E 17564.0 N -258.6 U 556.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 27.9
YLEN 47.9
ZLEN 39.9
POS E 17687.7 N -427.6 U 561.0

-- Reference Value: motor nameplate
NEW BOX
XLEN 51.9
YLEN 108.7
ZLEN 6.0
POS E 17889.2 N -186.1 U 313.3

-- Motor fan cowl disc
NEW CYLI
DIAM 438.8
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 17687.7 N -564.5 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 201.9
YLEN 9.6
ZLEN 6.4
POS E 17788.6 N -564.5 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 201.9
YLEN 9.6
ZLEN 6.4
POS E 17586.8 N -564.5 U 313.3

NEW SUBE /203_PU_011_AUXILIARY
-- 3 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 146x394 at the wet end, outboard of the casing
-- CAD handles: 22BBCF,22BBD0,22BBD1,22BBCB,22BBCC,22BBCA ...
NEW BOX
XLEN 393.5
YLEN 145.6
ZLEN 116.4
POS E 17685.0 N 779.2 U 108.2

-- Auxiliary [LOW]: body 146x442 at the wet end, outboard of the casing
-- CAD handles: 22A790,22A791,22BBB8,22BBB9,22BBBA,22BBAB ...
NEW BOX
XLEN 442.0
YLEN 145.6
ZLEN 116.4
POS E 17698.5 N 881.6 U 108.2

-- Auxiliary [LOW]: body 27x199 at the wet end, outboard of the casing
-- CAD handles: 22BB9B,22BB98,22BB99,22BB9A
NEW BOX
XLEN 199.5
YLEN 27.0
ZLEN 60.0
POS E 17685.0 N 994.8 U 80.0

NEW SUBE /203_PU_011_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN90; POS is the flange face, contractual direction N
NEW NOZZLE /203_PU_011_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0MM
POS E 17685.0 N 1009.8 U 313.3
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_011_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /203_PU_011_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 17687.0 N 880.9 U 525.5
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 203-PU-020
-- --------------------------------------------------------------------
-- 203-PU-020 - OXYGEN STAGE FEED MC PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 203-PU-020
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: unknown
-- Layout axis: W (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 539 mm snapped to catalogue DN500 (nearest available in 'AAZFBB011'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)
-- Warning: no shape-reference geometry; the pump must fall back to metadata-driven geometry
-- Warning: no CAD top view in this file; pump body geometry is a metadata-proportioned Reference Value and remains UNCONFIRMED

NEW EQUI /203_PU_020
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_020_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 926.0
YLEN 760.0
ZLEN 50.0
POS E 17095.0 N 5685.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 16687.6 N 5381.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 16687.56mm N 5381mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 16687.6 N 5989.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 16687.56mm N 5989mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 17502.4 N 5381.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 17502.44mm N 5381mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 17502.4 N 5989.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 17502.44mm N 5989mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /203_PU_020_SUPPORT
-- 24 part(s), 0 nozzle(s)
-- UNCONFIRMED: motor foot: sole plate on the baseplate
NEW BOX
XLEN 76.0
YLEN 431.8
ZLEN 45.1
POS E 17424.7 N 5685.0 U 72.5

-- UNCONFIRMED: motor foot: pedestal web
NEW BOX
XLEN 38.3
YLEN 217.8
ZLEN 319.2
POS E 17424.7 N 5685.0 U 254.6

-- UNCONFIRMED: motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 17444.49092mm N 5778.86mm U 95.0528mm
ORI Y IS U AND Z IS N
HEIG 37.544mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 39.66984mm N 0mm U 0mm
END
NEW VERTEX
POS E 21.818412mm N 280.858336mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 17444.49092mm N 5553.596mm U 95.0528mm
ORI Y IS U AND Z IS N
HEIG 37.544mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 39.66984mm N 0mm U 0mm
END
NEW VERTEX
POS E 21.818412mm N 280.858336mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.4
HEIG 69.5
ORI Z IS U AND Y IS N
POS E 17448.5 N 5685.0 U 72.5

-- UNCONFIRMED: motor foot: hold-down hex nut
NEW EXTRUSION
POS E 17448.457904mm N 5685mm U 95.0528mm
ORI Y IS N AND Z IS U
HEIG 19.52288mm

NEW LOOP
NEW VERTEX
POS E 20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N 23.952023mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N -11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N -23.952023mm U 0mm
END
NEW VERTEX
POS E 20.74306mm N -11.976011mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.4
HEIG 69.5
ORI Z IS U AND Y IS N
POS E 17400.9 N 5685.0 U 72.5

-- UNCONFIRMED: motor foot: hold-down hex nut
NEW EXTRUSION
POS E 17400.854096mm N 5685mm U 95.0528mm
ORI Y IS N AND Z IS U
HEIG 19.52288mm

NEW LOOP
NEW VERTEX
POS E 20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N 23.952023mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N -11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N -23.952023mm U 0mm
END
NEW VERTEX
POS E 20.74306mm N -11.976011mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: sole plate on the baseplate
NEW BOX
XLEN 76.0
YLEN 431.8
ZLEN 45.1
POS E 17191.3 N 5685.0 U 72.5

-- UNCONFIRMED: motor foot: pedestal web
NEW BOX
XLEN 38.3
YLEN 217.8
ZLEN 319.2
POS E 17191.3 N 5685.0 U 254.6

-- UNCONFIRMED: motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 17211.13892mm N 5778.86mm U 95.0528mm
ORI Y IS U AND Z IS N
HEIG 37.544mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 39.66984mm N 0mm U 0mm
END
NEW VERTEX
POS E 21.818412mm N 280.858336mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 17211.13892mm N 5553.596mm U 95.0528mm
ORI Y IS U AND Z IS N
HEIG 37.544mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 39.66984mm N 0mm U 0mm
END
NEW VERTEX
POS E 21.818412mm N 280.858336mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.4
HEIG 69.5
ORI Z IS U AND Y IS N
POS E 17215.1 N 5685.0 U 72.5

-- UNCONFIRMED: motor foot: hold-down hex nut
NEW EXTRUSION
POS E 17215.105904mm N 5685mm U 95.0528mm
ORI Y IS N AND Z IS U
HEIG 19.52288mm

NEW LOOP
NEW VERTEX
POS E 20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N 23.952023mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N -11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N -23.952023mm U 0mm
END
NEW VERTEX
POS E 20.74306mm N -11.976011mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.4
HEIG 69.5
ORI Z IS U AND Y IS N
POS E 17167.5 N 5685.0 U 72.5

-- UNCONFIRMED: motor foot: hold-down hex nut
NEW EXTRUSION
POS E 17167.502096mm N 5685mm U 95.0528mm
ORI Y IS N AND Z IS U
HEIG 19.52288mm

NEW LOOP
NEW VERTEX
POS E 20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N 23.952023mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N -11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N -23.952023mm U 0mm
END
NEW VERTEX
POS E 20.74306mm N -11.976011mm U 0mm
END
END
END

-- UNCONFIRMED: casing foot: sole plate on the baseplate
NEW BOX
XLEN 159.7
YLEN 249.3
ZLEN 26.0
POS E 16807.9 N 5685.0 U 63.0

-- UNCONFIRMED: casing foot: pedestal web
NEW BOX
XLEN 80.6
YLEN 125.7
ZLEN 348.2
POS E 16807.9 N 5685.0 U 250.1

-- UNCONFIRMED: casing foot: triangular stiffener gusset
NEW EXTRUSION
POS E 16849.61mm N 5739.188mm U 76.01024mm
ORI Y IS U AND Z IS N
HEIG 21.6752mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 83.34mm N 0mm U 0mm
END
NEW VERTEX
POS E 45.837mm N 306.443949mm U 0mm
END
END
END

-- UNCONFIRMED: casing foot: triangular stiffener gusset
NEW EXTRUSION
POS E 16849.61mm N 5609.1368mm U 76.01024mm
ORI Y IS U AND Z IS N
HEIG 21.6752mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 83.34mm N 0mm U 0mm
END
NEW VERTEX
POS E 45.837mm N 306.443949mm U 0mm
END
END
END

-- UNCONFIRMED: casing foot: hold-down bolt shank
NEW CYLI
DIAM 14.1
HEIG 40.1
ORI Z IS U AND Y IS N
POS E 16857.9 N 5685.0 U 63.0

-- UNCONFIRMED: casing foot: hold-down hex nut
NEW EXTRUSION
POS E 16857.944mm N 5685mm U 76.01024mm
ORI Y IS N AND Z IS U
HEIG 11.271104mm

NEW LOOP
NEW VERTEX
POS E 11.975548mm N 6.914086mm U 0mm
END
NEW VERTEX
POS E 0mm N 13.828172mm U 0mm
END
NEW VERTEX
POS E -11.975548mm N 6.914086mm U 0mm
END
NEW VERTEX
POS E -11.975548mm N -6.914086mm U 0mm
END
NEW VERTEX
POS E 0mm N -13.828172mm U 0mm
END
NEW VERTEX
POS E 11.975548mm N -6.914086mm U 0mm
END
END
END

-- UNCONFIRMED: casing foot: hold-down bolt shank
NEW CYLI
DIAM 14.1
HEIG 40.1
ORI Z IS U AND Y IS N
POS E 16757.9 N 5685.0 U 63.0

-- UNCONFIRMED: casing foot: hold-down hex nut
NEW EXTRUSION
POS E 16757.936mm N 5685mm U 76.01024mm
ORI Y IS N AND Z IS U
HEIG 11.271104mm

NEW LOOP
NEW VERTEX
POS E 11.975548mm N 6.914086mm U 0mm
END
NEW VERTEX
POS E 0mm N 13.828172mm U 0mm
END
NEW VERTEX
POS E -11.975548mm N 6.914086mm U 0mm
END
NEW VERTEX
POS E -11.975548mm N -6.914086mm U 0mm
END
NEW VERTEX
POS E 0mm N -13.828172mm U 0mm
END
NEW VERTEX
POS E 11.975548mm N -6.914086mm U 0mm
END
END
END

NEW SUBE /203_PU_020_CASING
-- 2 part(s), 0 nozzle(s)
-- UNCONFIRMED: volute barrel (metadata-proportioned)
NEW CYLI
DIAM 349.6
HEIG 277.8
ORI Z IS W AND Y IS U
POS E 16807.9 N 5685.0 U 592.0

-- UNCONFIRMED: suction cover (metadata-proportioned)
NEW CONE
DTOP 216.8
DBOT 349.6
HEIG 88.9
ORI Z IS W AND Y IS U
POS E 16624.6 N 5685.0 U 592.0

NEW SUBE /203_PU_020_COUPLING
-- 2 part(s), 0 nozzle(s)
-- UNCONFIRMED: coupling (metadata-proportioned)
NEW CYLI
DIAM 142.3
HEIG 111.1
ORI Z IS W AND Y IS U
POS E 16882.0 N 5685.0 U 592.0

-- UNCONFIRMED: coupling guard (metadata-proportioned)
NEW BOX
XLEN 111.1
YLEN 181.8
ZLEN 181.8
POS E 16882.0 N 5685.0 U 592.0

NEW SUBE /203_PU_020_DRIVER
-- 1 part(s), 0 nozzle(s)
-- UNCONFIRMED: motor barrel (metadata-proportioned)
NEW CYLI
DIAM 395.2
HEIG 388.9
ORI Z IS W AND Y IS U
POS E 17308.0 N 5685.0 U 592.0

NEW SUBE /203_PU_020_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN500; POS is the flange face, contractual direction W
NEW NOZZLE /203_PU_020_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB011
POS E 16537.0 N 5685.0 U 592.0
ORI P1 IS W
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_020_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /203_PU_020_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 17095.0 N 5685.0 U 892.0
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 203-PU-026
-- --------------------------------------------------------------------
-- 203-PU-026 - OXIDISED WL BOOSTER PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 203-PU-026
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: S (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 113 mm snapped to catalogue DN125 (nearest available in 'AAZFBB0PP'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /203_PU_026
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_026_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 13809.0 N 358.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 13474.6 N -412.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 13474.6mm N -412mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 13474.6 N 1128.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 13474.6mm N 1128mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 14143.4 N -412.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 14143.4mm N -412mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 14143.4 N 1128.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 14143.4mm N 1128mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /203_PU_026_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 307.5
YLEN 376.9
ZLEN 32.1
POS E 13811.7 N 479.3 U 66.0

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 155.1
YLEN 190.1
ZLEN 122.5
POS E 13811.7 N 479.3 U 143.3

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 13744.849087mm N 577.622668mm U 82.086251mm
ORI Y IS U AND Z IS W
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.65772mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161746mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 13905.280345mm N 577.622668mm U 82.086251mm
ORI Y IS U AND Z IS W
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.65772mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161746mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 13811.7 N 597.3 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 13811.695444mm N 597.28844mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 13811.7 N 361.3 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 13811.695444mm N 361.299176mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 577.2
YLEN 133.8
ZLEN 60.2
POS E 13811.7 N 162.0 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 291.1
YLEN 67.5
ZLEN 50.7
POS E 13811.7 N 162.0 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 13686.223751mm N 196.905584mm U 110.226413mm
ORI Y IS U AND Z IS W
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.832878mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.408083mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 13987.355815mm N 196.905584mm U 110.226413mm
ORI Y IS U AND Z IS W
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.832878mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.408083mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 13811.7 N 203.9 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 13811.695444mm N 203.888872mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 13811.7 N 120.1 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 13811.695444mm N 120.089419mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 577.2
YLEN 133.8
ZLEN 60.2
POS E 13811.7 N -276.2 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 291.1
YLEN 67.5
ZLEN 50.7
POS E 13811.7 N -276.2 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 13686.223751mm N -241.261491mm U 110.226413mm
ORI Y IS U AND Z IS W
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.832878mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.408083mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 13987.355815mm N -241.261491mm U 110.226413mm
ORI Y IS U AND Z IS W
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.832878mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.408083mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 13811.7 N -234.3 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 13811.695444mm N -234.278204mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 13811.7 N -318.1 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 13811.695444mm N -318.077657mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 130.6
YLEN 65.3
ZLEN 13.6
POS E 13811.7 N 1066.9 U 56.8

-- Casing support: pedestal web
NEW BOX
XLEN 65.9
YLEN 32.9
ZLEN 247.2
POS E 13811.7 N 1066.9 U 187.2

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 13783.310398mm N 1083.925961mm U 63.624851mm
ORI Y IS U AND Z IS W
HEIG 11.354042mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.062127mm N 0mm U 0mm
END
NEW VERTEX
POS E 18.73417mm N 217.493863mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 13851.434653mm N 1083.925961mm U 63.624851mm
ORI Y IS U AND Z IS W
HEIG 11.354042mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.062127mm N 0mm U 0mm
END
NEW VERTEX
POS E 18.73417mm N 217.493863mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.6
ORI Z IS U AND Y IS N
POS E 13811.7 N 1087.3 U 56.8

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 13811.695504mm N 1087.332173mm U 63.624851mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.6
ORI Z IS U AND Y IS N
POS E 13811.7 N 1046.5 U 56.8

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 13811.695504mm N 1046.457621mm U 63.624851mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /203_PU_026_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 92; the only large round feature in the plan, at the wet end
-- CAD handles: 22BCD8,22BCD1,22BCD2,22BCD3,22BCD4,22BCD5 ...
NEW CYLI
DIAM 183.1
HEIG 113.5
ORI Z IS U AND Y IS N
POS E 13811.7 N 1066.9 U 398.7

-- casing split flange at the cover joint
NEW CYLI
DIAM 201.4
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 13811.7 N 1066.9 U 463.4

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 13811.7 N 977.0 U 453.8

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 13811.695504mm N 976.973553mm U 471.449444mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 13875.3 N 1003.3 U 453.8

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 13875.279496mm N 1003.310905mm U 471.449444mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 13901.6 N 1066.9 U 453.8

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 13901.616848mm N 1066.894897mm U 471.449444mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 13875.3 N 1130.5 U 453.8

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 13875.279496mm N 1130.478889mm U 471.449444mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 13811.7 N 1156.8 U 453.8

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 13811.695504mm N 1156.816241mm U 471.449444mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 13748.1 N 1130.5 U 453.8

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 13748.111512mm N 1130.478889mm U 471.449444mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 13721.8 N 1066.9 U 453.8

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 13721.77416mm N 1066.894897mm U 471.449444mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 13748.1 N 1003.3 U 453.8

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 13748.111512mm N 1003.310905mm U 471.449444mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 113.5
DBOT 183.1
HEIG 34.1
ORI Z IS S AND Y IS U
POS E 13811.7 N 993.1 U 398.7

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 76.9
HEIG 20.4
ORI Z IS S AND Y IS U
POS E 13811.7 N 1133.9 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 59.0
ORI Z IS S AND Y IS U
POS E 13716.5 N 1066.9 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 59.0
ORI Z IS S AND Y IS U
POS E 13906.9 N 1066.9 U 398.7

NEW SUBE /203_PU_026_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 410 mm along the machine axis x 431 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22BCBB,22BCBC,22BCBD,22BCFB,22BCFC,22BCFD
NEW CYLI
DIAM 431.3
HEIG 409.7
ORI Z IS S AND Y IS U
POS E 13811.7 N 479.3 U 398.7

NEW SUBE /203_PU_026_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 210 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BCBE,22BCBF
NEW CYLI
DIAM 134.8
HEIG 210.2
ORI Z IS S AND Y IS U
POS E 13809.0 N 789.3 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS S AND Y IS U
POS E 13809.0 N 871.3 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS S AND Y IS U
POS E 13809.0 N 707.3 U 398.7

NEW SUBE /203_PU_026_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 685 mm along the machine axis x 528 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BD05,22BD06,22BD07,22BD02,22BD03,22BD04 ...
NEW CYLI
DIAM 528.3
HEIG 684.6
ORI Z IS S AND Y IS U
POS E 13811.7 N -57.1 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 41.1
ORI Z IS S AND Y IS U
POS E 13811.7 N 264.7 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 41.1
ORI Z IS S AND Y IS U
POS E 13811.7 N -378.9 U 398.7

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 14083.2 N -57.1 U 398.7

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 14062.6 N -57.1 U 502.6

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 14003.7 N -57.1 U 590.7

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13915.6 N -57.1 U 649.6

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13811.7 N -57.1 U 670.2

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13707.8 N -57.1 U 649.6

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13619.7 N -57.1 U 590.7

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13560.8 N -57.1 U 502.6

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13540.1 N -57.1 U 398.7

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13560.8 N -57.1 U 294.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13619.7 N -57.1 U 206.7

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13707.8 N -57.1 U 147.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13811.7 N -57.1 U 127.1

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 13915.6 N -57.1 U 147.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 14003.7 N -57.1 U 206.7

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 14.8
HEIG 492.9
ORI Z IS S AND Y IS U
POS E 14062.6 N -57.1 U 294.8

-- Motor terminal box
NEW BOX
XLEN 211.3
YLEN 205.4
ZLEN 116.2
POS E 13811.7 N -57.1 U 720.9

-- Motor cable gland
NEW CYLI
DIAM 39.5
HEIG 116.2
ORI Z IS E AND Y IS U
POS E 13975.5 N -57.1 U 720.9

-- Reference Value: motor lifting lug
NEW BOX
XLEN 37.0
YLEN 63.4
ZLEN 52.8
POS E 13811.7 N 134.6 U 726.8

-- Reference Value: motor nameplate
NEW BOX
XLEN 68.7
YLEN 123.2
ZLEN 6.0
POS E 13545.5 N -139.3 U 398.7

-- Motor fan cowl disc
NEW CYLI
DIAM 581.1
HEIG 8.0
ORI Z IS S AND Y IS U
POS E 13811.7 N 289.2 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 267.3
YLEN 9.6
ZLEN 6.4
POS E 13678.0 N 289.2 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 267.3
YLEN 9.6
ZLEN 6.4
POS E 13945.4 N 289.2 U 398.7

NEW SUBE /203_PU_026_AUXILIARY
-- 3 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 16x221 at the wet end, outboard of the casing
-- CAD handles: 22BCCC,22BCC9,22BCCA,22BCCB
NEW BOX
XLEN 221.0
YLEN 16.2
ZLEN 60.0
POS E 13809.0 N 1182.8 U 80.0

-- Auxiliary [LOW]: body 162x361 at the wet end, outboard of the casing
-- CAD handles: 22BCC4,229EAC,22BCE9,22BCEA,22BCE2,22BCE3 ...
NEW BOX
XLEN 361.2
YLEN 161.7
ZLEN 129.4
POS E 13819.8 N 1072.3 U 114.7

-- Auxiliary [LOW]: body 135x237 at the wet end, outboard of the casing
-- CAD handles: 22BCC0,22BCC1,22BCC2
NEW BOX
XLEN 237.2
YLEN 134.8
ZLEN 107.8
POS E 13811.7 N 961.8 U 103.9

NEW SUBE /203_PU_026_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN125; POS is the flange face, contractual direction S
NEW NOZZLE /203_PU_026_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0PP
POS E 13809.0 N -481.8 U 398.7
ORI P1 IS S
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_026_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /203_PU_026_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 13811.7 N 1066.9 U 605.4
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 203-PU-031
-- --------------------------------------------------------------------
-- 203-PU-031 - OXYGEN REACTOR TOP SPOOLING BOOSTER PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 203-PU-031
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: S (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 59 mm snapped to catalogue DN65 (nearest available in 'AAZFBB0KK'; catalogue max is DN600)
-- Note: discharge: metadata bore 143 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /203_PU_031
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_031_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 631.0
YLEN 1353.0
ZLEN 50.0
POS E 15108.0 N 175.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 20.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 14830.4 N -411.5 U 65.0

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 14830.36mm N -411.5mm U 80mm
ORI Y IS N AND Z IS U
HEIG 16mm

NEW LOOP
NEW VERTEX
POS E 17mm N 9.814955mm U 0mm
END
NEW VERTEX
POS E 0mm N 19.629909mm U 0mm
END
NEW VERTEX
POS E -17mm N 9.814955mm U 0mm
END
NEW VERTEX
POS E -17mm N -9.814955mm U 0mm
END
NEW VERTEX
POS E 0mm N -19.629909mm U 0mm
END
NEW VERTEX
POS E 17mm N -9.814955mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 20.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 14830.4 N 761.5 U 65.0

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 14830.36mm N 761.5mm U 80mm
ORI Y IS N AND Z IS U
HEIG 16mm

NEW LOOP
NEW VERTEX
POS E 17mm N 9.814955mm U 0mm
END
NEW VERTEX
POS E 0mm N 19.629909mm U 0mm
END
NEW VERTEX
POS E -17mm N 9.814955mm U 0mm
END
NEW VERTEX
POS E -17mm N -9.814955mm U 0mm
END
NEW VERTEX
POS E 0mm N -19.629909mm U 0mm
END
NEW VERTEX
POS E 17mm N -9.814955mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 20.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 15385.6 N -411.5 U 65.0

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 15385.64mm N -411.5mm U 80mm
ORI Y IS N AND Z IS U
HEIG 16mm

NEW LOOP
NEW VERTEX
POS E 17mm N 9.814955mm U 0mm
END
NEW VERTEX
POS E 0mm N 19.629909mm U 0mm
END
NEW VERTEX
POS E -17mm N 9.814955mm U 0mm
END
NEW VERTEX
POS E -17mm N -9.814955mm U 0mm
END
NEW VERTEX
POS E 0mm N -19.629909mm U 0mm
END
NEW VERTEX
POS E 17mm N -9.814955mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 20.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 15385.6 N 761.5 U 65.0

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 15385.64mm N 761.5mm U 80mm
ORI Y IS N AND Z IS U
HEIG 16mm

NEW LOOP
NEW VERTEX
POS E 17mm N 9.814955mm U 0mm
END
NEW VERTEX
POS E 0mm N 19.629909mm U 0mm
END
NEW VERTEX
POS E -17mm N 9.814955mm U 0mm
END
NEW VERTEX
POS E -17mm N -9.814955mm U 0mm
END
NEW VERTEX
POS E 0mm N -19.629909mm U 0mm
END
NEW VERTEX
POS E 17mm N -9.814955mm U 0mm
END
END
END

NEW SUBE /203_PU_031_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 441.7
YLEN 98.0
ZLEN 46.1
POS E 15108.0 N 76.7 U 73.0

-- Motor foot: pedestal web
NEW BOX
XLEN 222.8
YLEN 49.4
ZLEN 38.8
POS E 15108.0 N 76.7 U 115.5

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15011.975735mm N 102.239888mm U 96.091647mm
ORI Y IS U AND Z IS W
HEIG 38.409706mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 51.13747mm N 0mm U 0mm
END
NEW VERTEX
POS E 28.125608mm N 34.156336mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15242.433971mm N 102.239888mm U 96.091647mm
ORI Y IS U AND Z IS W
HEIG 38.409706mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 51.13747mm N 0mm U 0mm
END
NEW VERTEX
POS E 28.125608mm N 34.156336mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 25.0
HEIG 71.1
ORI Z IS U AND Y IS N
POS E 15108.0 N 107.4 U 73.0

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 15108mm N 107.353635mm U 96.091647mm
ORI Y IS N AND Z IS U
HEIG 19.973047mm

NEW LOOP
NEW VERTEX
POS E 21.221363mm N 12.252159mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.504319mm U 0mm
END
NEW VERTEX
POS E -21.221363mm N 12.252159mm U 0mm
END
NEW VERTEX
POS E -21.221363mm N -12.252159mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.504319mm U 0mm
END
NEW VERTEX
POS E 21.221363mm N -12.252159mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 25.0
HEIG 71.1
ORI Z IS U AND Y IS N
POS E 15108.0 N 46.0 U 73.0

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 15108mm N 45.988671mm U 96.091647mm
ORI Y IS N AND Z IS U
HEIG 19.973047mm

NEW LOOP
NEW VERTEX
POS E 21.221363mm N 12.252159mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.504319mm U 0mm
END
NEW VERTEX
POS E -21.221363mm N 12.252159mm U 0mm
END
NEW VERTEX
POS E -21.221363mm N -12.252159mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.504319mm U 0mm
END
NEW VERTEX
POS E 21.221363mm N -12.252159mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 441.7
YLEN 98.0
ZLEN 46.1
POS E 15108.0 N -244.2 U 73.0

-- Motor foot: pedestal web
NEW BOX
XLEN 222.8
YLEN 49.4
ZLEN 38.8
POS E 15108.0 N -244.2 U 115.5

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15011.975735mm N -218.622666mm U 96.091647mm
ORI Y IS U AND Z IS W
HEIG 38.409706mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 51.13747mm N 0mm U 0mm
END
NEW VERTEX
POS E 28.125608mm N 34.156336mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15242.433971mm N -218.622666mm U 96.091647mm
ORI Y IS U AND Z IS W
HEIG 38.409706mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 51.13747mm N 0mm U 0mm
END
NEW VERTEX
POS E 28.125608mm N 34.156336mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 25.0
HEIG 71.1
ORI Z IS U AND Y IS N
POS E 15108.0 N -213.5 U 73.0

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 15108mm N -213.508919mm U 96.091647mm
ORI Y IS N AND Z IS U
HEIG 19.973047mm

NEW LOOP
NEW VERTEX
POS E 21.221363mm N 12.252159mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.504319mm U 0mm
END
NEW VERTEX
POS E -21.221363mm N 12.252159mm U 0mm
END
NEW VERTEX
POS E -21.221363mm N -12.252159mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.504319mm U 0mm
END
NEW VERTEX
POS E 21.221363mm N -12.252159mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 25.0
HEIG 71.1
ORI Z IS U AND Y IS N
POS E 15108.0 N -274.9 U 73.0

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 15108mm N -274.873883mm U 96.091647mm
ORI Y IS N AND Z IS U
HEIG 19.973047mm

NEW LOOP
NEW VERTEX
POS E 21.221363mm N 12.252159mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.504319mm U 0mm
END
NEW VERTEX
POS E -21.221363mm N 12.252159mm U 0mm
END
NEW VERTEX
POS E -21.221363mm N -12.252159mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.504319mm U 0mm
END
NEW VERTEX
POS E 21.221363mm N -12.252159mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 111.5
YLEN 188.5
ZLEN 11.6
POS E 15108.0 N 269.3 U 55.8

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 56.2
YLEN 95.1
ZLEN 184.9
POS E 15108.0 N 269.3 U 154.1

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 15083.768121mm N 318.504013mm U 61.631264mm
ORI Y IS U AND Z IS W
HEIG 9.69272mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 98.328822mm N 0mm U 0mm
END
NEW VERTEX
POS E 54.080852mm N 162.680962mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 15141.924439mm N 318.504013mm U 61.631264mm
ORI Y IS U AND Z IS W
HEIG 9.69272mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 98.328822mm N 0mm U 0mm
END
NEW VERTEX
POS E 54.080852mm N 162.680962mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 23.6
ORI Z IS U AND Y IS N
POS E 15108.0 N 328.3 U 55.8

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 15107.99992mm N 328.336895mm U 61.631264mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 23.6
ORI Z IS U AND Y IS N
POS E 15108.0 N 210.3 U 55.8

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 15107.99992mm N 210.342309mm U 61.631264mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 103.8
YLEN 51.9
ZLEN 10.8
POS E 15108.0 N 697.9 U 55.4

-- Casing support: pedestal web
NEW BOX
XLEN 52.3
YLEN 26.2
ZLEN 186.1
POS E 15108.0 N 697.9 U 153.9

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 15085.436334mm N 711.449317mm U 60.83056mm
ORI Y IS U AND Z IS W
HEIG 9.025467mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 27.0764mm N 0mm U 0mm
END
NEW VERTEX
POS E 14.89202mm N 163.80429mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 15139.589133mm N 711.449317mm U 60.83056mm
ORI Y IS U AND Z IS W
HEIG 9.025467mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 27.0764mm N 0mm U 0mm
END
NEW VERTEX
POS E 14.89202mm N 163.80429mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 22.8
ORI Z IS U AND Y IS N
POS E 15108.0 N 714.2 U 55.4

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 15108mm N 714.156957mm U 60.83056mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 22.8
ORI Z IS U AND Y IS N
POS E 15108.0 N 681.7 U 55.4

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 15108mm N 681.665278mm U 60.83056mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /203_PU_031_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 1 concentric circle(s) on one axis, radii 73; the only large round feature in the plan, at the wet end
-- CAD handles: 229D69,229D5A,229D5B,229D5C,229D5D,229D5E ...
NEW CYLI
DIAM 145.6
HEIG 90.3
ORI Z IS U AND Y IS N
POS E 15108.0 N 697.9 U 316.8

-- casing split flange at the cover joint
NEW CYLI
DIAM 160.1
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 15108.0 N 697.9 U 370.0

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15108.0 N 628.6 U 360.4

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 15108mm N 628.646495mm U 377.973711mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15157.0 N 648.9 U 360.4

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 15156.977484mm N 648.933633mm U 377.973711mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15177.3 N 697.9 U 360.4

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 15177.264622mm N 697.911117mm U 377.973711mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15157.0 N 746.9 U 360.4

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 15156.977484mm N 746.888602mm U 377.973711mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15108.0 N 767.2 U 360.4

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 15108mm N 767.17574mm U 377.973711mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15059.0 N 746.9 U 360.4

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 15059.022516mm N 746.888602mm U 377.973711mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15038.7 N 697.9 U 360.4

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 15038.735378mm N 697.911117mm U 377.973711mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15059.0 N 648.9 U 360.4

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 15059.022516mm N 648.933633mm U 377.973711mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 90.3
DBOT 145.6
HEIG 27.1
ORI Z IS S AND Y IS U
POS E 15108.0 N 639.2 U 316.8

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 61.1
HEIG 16.2
ORI Z IS S AND Y IS U
POS E 15108.0 N 751.2 U 316.8

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 46.9
ORI Z IS S AND Y IS U
POS E 15031.6 N 697.9 U 316.8

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 46.9
ORI Z IS S AND Y IS U
POS E 15184.4 N 697.9 U 316.8

NEW SUBE /203_PU_031_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 205x156 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 22BD20,22BD1D,22BD1E
NEW CYLI
DIAM 156.3
HEIG 204.9
ORI Z IS S AND Y IS U
POS E 15108.0 N 269.3 U 316.8

NEW SUBE /203_PU_031_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 162 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BD21,22BD22
NEW CYLI
DIAM 134.8
HEIG 161.7
ORI Z IS S AND Y IS U
POS E 15108.0 N 452.6 U 316.8

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 35.6
ORI Z IS S AND Y IS U
POS E 15108.0 N 515.7 U 316.8

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 35.6
ORI Z IS S AND Y IS U
POS E 15108.0 N 389.6 U 316.8

NEW SUBE /203_PU_031_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 501 mm along the machine axis x 404 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BD5C,22BD5B,22BD5A,22BD53,22BD50,22BD51 ...
NEW CYLI
DIAM 404.3
HEIG 501.3
ORI Z IS S AND Y IS U
POS E 15108.0 N -83.8 U 316.8

-- Motor end bell
NEW CYLI
DIAM 436.7
HEIG 30.1
ORI Z IS S AND Y IS U
POS E 15108.0 N 151.9 U 316.8

-- Motor end bell
NEW CYLI
DIAM 436.7
HEIG 30.1
ORI Z IS S AND Y IS U
POS E 15108.0 N -319.4 U 316.8

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15315.8 N -83.8 U 316.8

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15300.0 N -83.8 U 396.4

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15254.9 N -83.8 U 463.8

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15187.5 N -83.8 U 508.8

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15108.0 N -83.8 U 524.7

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15028.5 N -83.8 U 508.8

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 14961.1 N -83.8 U 463.8

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 14916.0 N -83.8 U 396.4

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 14900.2 N -83.8 U 316.8

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 14916.0 N -83.8 U 237.3

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 14961.1 N -83.8 U 169.9

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15028.5 N -83.8 U 124.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15108.0 N -83.8 U 109.0

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15187.5 N -83.8 U 124.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15254.9 N -83.8 U 169.9

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 11.3
HEIG 361.0
ORI Z IS S AND Y IS U
POS E 15300.0 N -83.8 U 237.3

-- Motor terminal box
NEW BOX
XLEN 161.7
YLEN 150.4
ZLEN 88.9
POS E 15108.0 N -83.8 U 563.5

-- Motor cable gland
NEW CYLI
DIAM 30.2
HEIG 88.9
ORI Z IS E AND Y IS U
POS E 15233.3 N -83.8 U 563.5

-- Reference Value: motor lifting lug
NEW BOX
XLEN 28.3
YLEN 48.5
ZLEN 40.4
POS E 15108.0 N 56.6 U 567.9

-- Reference Value: motor nameplate
NEW BOX
XLEN 52.6
YLEN 90.2
ZLEN 6.0
POS E 14903.8 N -143.9 U 316.8

-- Motor fan cowl disc
NEW CYLI
DIAM 444.7
HEIG 8.0
ORI Z IS S AND Y IS U
POS E 15108.0 N 170.9 U 316.8

-- Motor fan grille bar
NEW BOX
XLEN 204.6
YLEN 9.6
ZLEN 6.4
POS E 15005.7 N 170.9 U 316.8

-- Motor fan grille bar
NEW BOX
XLEN 204.6
YLEN 9.6
ZLEN 6.4
POS E 15210.3 N 170.9 U 316.8

NEW SUBE /203_PU_031_AUXILIARY
-- 3 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 22x167 at the wet end, outboard of the casing
-- CAD handles: 22BD2A,22BD27,22BD28,22BD29
NEW BOX
XLEN 167.1
YLEN 21.6
ZLEN 60.0
POS E 15108.0 N 792.3 U 80.0

-- Auxiliary [LOW]: body 151x313 at the wet end, outboard of the casing
-- CAD handles: 22BD45,22BD46,22BD47,22BD48,22BD49,22BD3E ...
NEW BOX
XLEN 312.7
YLEN 150.9
ZLEN 120.8
POS E 15116.1 N 700.6 U 110.4

-- Auxiliary [LOW]: body 135x232 at the wet end, outboard of the casing
-- CAD handles: 22BD3F,22BD40,22BD41,22BD42,22BD43,22BD44
NEW BOX
XLEN 231.8
YLEN 134.8
ZLEN 107.8
POS E 15108.0 N 600.9 U 103.9

NEW SUBE /203_PU_031_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN65; POS is the flange face, contractual direction S
NEW NOZZLE /203_PU_031_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0KK
POS E 15108.0 N -481.5 U 316.8
ORI P1 IS S
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /203_PU_031_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /203_PU_031_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 15108.0 N 697.9 U 512.0
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 204-PU-003
-- --------------------------------------------------------------------
-- 204-PU-003 - PRIMARY SCREEN FEED PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 204-PU-003
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 216 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 151 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /204_PU_003
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_003_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 857.0
YLEN 2129.0
ZLEN 50.0
POS E 20162.0 N -8768.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 19784.9 N -9742.5 U 69.3

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 19784.92mm N -9742.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 19784.9 N -7793.5 U 69.3

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 19784.92mm N -7793.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 20539.1 N -9742.5 U 69.3

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 20539.08mm N -9742.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 20539.1 N -7793.5 U 69.3

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 20539.08mm N -7793.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

NEW SUBE /204_PU_003_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 202.4
ZLEN 73.7
POS E 20164.7 N -9646.4 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 102.1
ZLEN 62.1
POS E 20164.7 N -9646.4 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 20318.334189mm N -9699.169923mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 105.574131mm N 0mm U 0mm
END
NEW VERTEX
POS E 58.065772mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19949.601012mm N -9699.169923mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 105.574131mm N 0mm U 0mm
END
NEW VERTEX
POS E 58.065772mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 20164.7 N -9709.7 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 20164.695365mm N -9709.727336mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 20164.7 N -9583.0 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 20164.695365mm N -9583.03838mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 202.4
ZLEN 73.7
POS E 20164.7 N -8984.0 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 102.1
ZLEN 62.1
POS E 20164.7 N -8984.0 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 20318.334189mm N -9036.744005mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 105.574131mm N 0mm U 0mm
END
NEW VERTEX
POS E 58.065772mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19949.601012mm N -9036.744005mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 105.574131mm N 0mm U 0mm
END
NEW VERTEX
POS E 58.065772mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 20164.7 N -9047.3 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 20164.695365mm N -9047.301418mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 20164.7 N -8920.6 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 20164.695365mm N -8920.612462mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 157.6
YLEN 401.7
ZLEN 16.4
POS E 20162.0 N -8579.3 U 58.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 79.5
YLEN 202.6
ZLEN 311.0
POS E 20162.0 N -8579.3 U 222.0

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 20196.258779mm N -8684.118646mm U 66.444214mm
ORI Y IS U AND Z IS E
HEIG 13.703511mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 273.723138mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 20114.03771mm N -8684.118646mm U 66.444214mm
ORI Y IS U AND Z IS E
HEIG 13.703511mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 273.723138mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 20162.0 N -8705.1 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 20162mm N -8705.078216mm U 66.444214mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 20162.0 N -8453.6 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 20162mm N -8453.563375mm U 66.444214mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 222.9
YLEN 102.3
ZLEN 23.3
POS E 20175.5 N -8029.5 U 61.6

-- Casing support: pedestal web
NEW BOX
XLEN 112.4
YLEN 51.6
ZLEN 253.6
POS E 20175.5 N -8029.5 U 200.1

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 20223.940686mm N -8056.14017mm U 73.262539mm
ORI Y IS U AND Z IS E
HEIG 19.385449mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.369276mm N 0mm U 0mm
END
NEW VERTEX
POS E 29.353102mm N 223.177476mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 20107.627991mm N -8056.14017mm U 73.262539mm
ORI Y IS U AND Z IS E
HEIG 19.385449mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.369276mm N 0mm U 0mm
END
NEW VERTEX
POS E 29.353102mm N 223.177476mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.6
HEIG 35.9
ORI Z IS U AND Y IS N
POS E 20175.5 N -8061.5 U 61.6

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 20175.477063mm N -8061.477097mm U 73.262539mm
ORI Y IS N AND Z IS U
HEIG 10.080434mm

NEW LOOP
NEW VERTEX
POS E 10.710461mm N 6.183687mm U 0mm
END
NEW VERTEX
POS E 0mm N 12.367375mm U 0mm
END
NEW VERTEX
POS E -10.710461mm N 6.183687mm U 0mm
END
NEW VERTEX
POS E -10.710461mm N -6.183687mm U 0mm
END
NEW VERTEX
POS E 0mm N -12.367375mm U 0mm
END
NEW VERTEX
POS E 10.710461mm N -6.183687mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.6
HEIG 35.9
ORI Z IS U AND Y IS N
POS E 20175.5 N -7997.4 U 61.6

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 20175.477063mm N -7997.433967mm U 73.262539mm
ORI Y IS N AND Z IS U
HEIG 10.080434mm

NEW LOOP
NEW VERTEX
POS E 10.710461mm N 6.183687mm U 0mm
END
NEW VERTEX
POS E 0mm N 12.367375mm U 0mm
END
NEW VERTEX
POS E -10.710461mm N 6.183687mm U 0mm
END
NEW VERTEX
POS E -10.710461mm N -6.183687mm U 0mm
END
NEW VERTEX
POS E 0mm N -12.367375mm U 0mm
END
NEW VERTEX
POS E 10.710461mm N -6.183687mm U 0mm
END
END
END

NEW SUBE /204_PU_003_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 178x313 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22BBF1,22BBF2,22BBF3
NEW CYLI
DIAM 312.7
HEIG 177.9
ORI Z IS N AND Y IS U
POS E 20175.5 N -8029.5 U 477.0

-- volute closing onto the suction cover
NEW CONE
DTOP 193.9
DBOT 312.7
HEIG 53.4
ORI Z IS N AND Y IS U
POS E 20175.5 N -7913.8 U 477.0

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 131.3
HEIG 32.0
ORI Z IS N AND Y IS U
POS E 20175.5 N -8134.4 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 14.1
HEIG 92.5
ORI Z IS N AND Y IS U
POS E 20337.4 N -8029.5 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 14.1
HEIG 92.5
ORI Z IS N AND Y IS U
POS E 20013.5 N -8029.5 U 477.0

NEW SUBE /204_PU_003_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 437x221 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 22BBEC,22BBED,22BBEE
NEW CYLI
DIAM 221.0
HEIG 436.7
ORI Z IS N AND Y IS U
POS E 20162.0 N -8579.3 U 477.0

NEW SUBE /204_PU_003_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 199 mm apart running 243 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BBF0,22BBEF
NEW CYLI
DIAM 199.5
HEIG 242.6
ORI Z IS N AND Y IS U
POS E 20162.0 N -8239.7 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 53.4
ORI Z IS N AND Y IS U
POS E 20162.0 N -8334.3 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 53.4
ORI Z IS N AND Y IS U
POS E 20162.0 N -8145.1 U 477.0

NEW SUBE /204_PU_003_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 1035 mm along the machine axis x 647 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BC03,22BC04,22BC05,22BC06,22BC07,22BC08 ...
NEW CYLI
DIAM 646.9
HEIG 1035.0
ORI Z IS N AND Y IS U
POS E 20164.7 N -9315.2 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 62.1
ORI Z IS N AND Y IS U
POS E 20164.7 N -9801.6 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 62.1
ORI Z IS N AND Y IS U
POS E 20164.7 N -8828.7 U 477.0

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 19833.2 N -9315.2 U 477.0

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 19858.5 N -9315.2 U 603.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 19930.3 N -9315.2 U 711.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20037.9 N -9315.2 U 783.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20164.7 N -9315.2 U 808.4

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20291.5 N -9315.2 U 783.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20399.1 N -9315.2 U 711.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20470.9 N -9315.2 U 603.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20496.1 N -9315.2 U 477.0

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20470.9 N -9315.2 U 350.1

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20399.1 N -9315.2 U 242.6

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20291.5 N -9315.2 U 170.7

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20164.7 N -9315.2 U 145.5

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 20037.9 N -9315.2 U 170.7

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 19930.3 N -9315.2 U 242.6

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 745.2
ORI Z IS N AND Y IS U
POS E 19858.5 N -9315.2 U 350.1

-- Motor terminal box
NEW BOX
XLEN 258.8
YLEN 310.5
ZLEN 142.3
POS E 20164.7 N -9315.2 U 871.6

-- Motor cable gland
NEW CYLI
DIAM 48.4
HEIG 142.3
ORI Z IS E AND Y IS U
POS E 19964.2 N -9315.2 U 871.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.3
YLEN 77.6
ZLEN 64.7
POS E 20164.7 N -9605.0 U 878.7

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.1
YLEN 186.3
ZLEN 6.0
POS E 20490.1 N -9191.0 U 477.0

-- Motor fan cowl disc
NEW CYLI
DIAM 711.6
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 20164.7 N -9836.7 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 20328.4 N -9836.7 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 20001.0 N -9836.7 U 477.0

NEW SUBE /204_PU_003_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 210x226 at the wet end, outboard of the casing
-- CAD handles: 22BBF9,22BBFA,22BBFB,22BBFC,22BBFD,22BBFE
NEW BOX
XLEN 226.4
YLEN 210.2
ZLEN 168.2
POS E 20407.3 N -7835.4 U 134.1

NEW SUBE /204_PU_003_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /204_PU_003_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 20162.0 N -7665.5 U 477.0
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_003_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /204_PU_003_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 20175.5 N -8029.5 U 783.3
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 204-PU-006
-- --------------------------------------------------------------------
-- 204-PU-006 - SECONDARY SCREEN FEED PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 204-PU-006
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: E (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 108 mm snapped to catalogue DN100 (nearest available in 'AAZFBB0NN'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /204_PU_006
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_006_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 1725.0
YLEN 760.0
ZLEN 50.0
POS E 20000.0 N 17410.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 19227.5 N 17106.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 19227.5mm N 17106mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 19227.5 N 17714.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 19227.5mm N 17714mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 20772.5 N 17106.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 20772.5mm N 17106mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 20772.5 N 17714.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 20772.5mm N 17714mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /204_PU_006_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 421.6
YLEN 253.7
ZLEN 26.5
POS E 20083.6 N 17407.3 U 63.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 212.6
YLEN 127.9
ZLEN 76.7
POS E 20083.6 N 17407.3 U 114.8

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 19973.584838mm N 17352.156384mm U 76.471161mm
ORI Y IS U AND Z IS S
HEIG 22.059301mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 219.946131mm N 0mm U 0mm
END
NEW VERTEX
POS E 120.970372mm N 67.504368mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 19973.584838mm N 17484.512187mm U 76.471161mm
ORI Y IS U AND Z IS S
HEIG 22.059301mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 219.946131mm N 0mm U 0mm
END
NEW VERTEX
POS E 120.970372mm N 67.504368mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.3
HEIG 40.8
ORI Z IS U AND Y IS N
POS E 19951.6 N 17407.3 U 63.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 19951.590225mm N 17407.304635mm U 76.471161mm
ORI Y IS N AND Z IS U
HEIG 11.470836mm

NEW LOOP
NEW VERTEX
POS E 12.187764mm N 7.036609mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.073217mm U 0mm
END
NEW VERTEX
POS E -12.187764mm N 7.036609mm U 0mm
END
NEW VERTEX
POS E -12.187764mm N -7.036609mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.073217mm U 0mm
END
NEW VERTEX
POS E 12.187764mm N -7.036609mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.3
HEIG 40.8
ORI Z IS U AND Y IS N
POS E 20215.5 N 17407.3 U 63.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 20215.525582mm N 17407.304635mm U 76.471161mm
ORI Y IS N AND Z IS U
HEIG 11.470836mm

NEW LOOP
NEW VERTEX
POS E 12.187764mm N 7.036609mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.073217mm U 0mm
END
NEW VERTEX
POS E -12.187764mm N 7.036609mm U 0mm
END
NEW VERTEX
POS E -12.187764mm N -7.036609mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.073217mm U 0mm
END
NEW VERTEX
POS E 12.187764mm N -7.036609mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 118.0
YLEN 435.8
ZLEN 45.5
POS E 19375.5 N 17407.3 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 59.5
YLEN 219.8
ZLEN 38.3
POS E 19375.5 N 17407.3 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19344.733125mm N 17312.560669mm U 95.477104mm
ORI Y IS U AND Z IS S
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19344.733125mm N 17539.946188mm U 95.477104mm
ORI Y IS U AND Z IS S
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 19338.6 N 17407.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 19338.574635mm N 17407.304635mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 19412.5 N 17407.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 19412.476514mm N 17407.304635mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 118.0
YLEN 435.8
ZLEN 45.5
POS E 19761.9 N 17407.3 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 59.5
YLEN 219.8
ZLEN 38.3
POS E 19761.9 N 17407.3 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19731.148176mm N 17312.560669mm U 95.477104mm
ORI Y IS U AND Z IS S
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19731.148176mm N 17539.946188mm U 95.477104mm
ORI Y IS U AND Z IS S
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 19725.0 N 17407.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 19724.989686mm N 17407.304635mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 19798.9 N 17407.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 19798.891565mm N 17407.304635mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 70.9
YLEN 141.8
ZLEN 14.8
POS E 20710.9 N 17408.0 U 57.4

-- Casing support: pedestal web
NEW BOX
XLEN 35.8
YLEN 71.5
ZLEN 153.0
POS E 20710.9 N 17408.0 U 141.3

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 20692.423936mm N 17377.157622mm U 64.79402mm
ORI Y IS U AND Z IS S
HEIG 12.32835mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 36.985049mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.341777mm N 134.683286mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 20692.423936mm N 17451.12772mm U 64.79402mm
ORI Y IS U AND Z IS S
HEIG 12.32835mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 36.985049mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.341777mm N 134.683286mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 26.8
ORI Z IS U AND Y IS N
POS E 20688.7 N 17408.0 U 57.4

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 20688.725431mm N 17407.978496mm U 64.79402mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 26.8
ORI Z IS U AND Y IS N
POS E 20733.1 N 17408.0 U 57.4

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 20733.10749mm N 17407.978496mm U 64.79402mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /204_PU_006_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 99; the only large round feature in the plan, at the wet end
-- CAD handles: 22C6F9,22C6F2,22C6F3,22C6F4,22C6F5,22C6F6 ...
NEW CYLI
DIAM 198.8
HEIG 123.3
ORI Z IS U AND Y IS N
POS E 20710.9 N 17408.0 U 313.3

-- casing split flange at the cover joint
NEW CYLI
DIAM 218.7
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 20710.9 N 17408.0 U 382.9

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 20809.5 N 17408.0 U 373.3

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 20809.480853mm N 17407.978496mm U 390.930245mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 20780.6 N 17477.7 U 373.3

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 20780.612011mm N 17477.674047mm U 390.930245mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 20710.9 N 17506.5 U 373.3

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 20710.91646mm N 17506.542889mm U 390.930245mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 20641.2 N 17477.7 U 373.3

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 20641.22091mm N 17477.674047mm U 390.930245mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 20612.4 N 17408.0 U 373.3

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 20612.352068mm N 17407.978496mm U 390.930245mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 20641.2 N 17338.3 U 373.3

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 20641.22091mm N 17338.282946mm U 390.930245mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 20710.9 N 17309.4 U 373.3

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 20710.91646mm N 17309.414103mm U 390.930245mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 20780.6 N 17338.3 U 373.3

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 20780.612011mm N 17338.282946mm U 390.930245mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 123.3
DBOT 198.8
HEIG 37.0
ORI Z IS E AND Y IS U
POS E 20791.1 N 17408.0 U 313.3

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 83.5
HEIG 22.2
ORI Z IS E AND Y IS U
POS E 20638.2 N 17408.0 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 64.1
ORI Z IS E AND Y IS U
POS E 20710.9 N 17305.0 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 64.1
ORI Z IS E AND Y IS U
POS E 20710.9 N 17511.0 U 313.3

NEW SUBE /204_PU_006_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 458 mm along the machine axis x 356 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22C730,22C731,22C732,22C6FA,22C6FB,22C6FC
NEW CYLI
DIAM 355.8
HEIG 458.2
ORI Z IS E AND Y IS U
POS E 20083.6 N 17407.3 U 313.3

NEW SUBE /204_PU_006_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 221 mm along x, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22C722,22C721
NEW CYLI
DIAM 134.8
HEIG 221.0
ORI Z IS E AND Y IS U
POS E 20423.2 N 17410.0 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 48.6
ORI Z IS E AND Y IS U
POS E 20337.0 N 17410.0 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 48.6
ORI Z IS E AND Y IS U
POS E 20509.4 N 17410.0 U 313.3

NEW SUBE /204_PU_006_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 604 mm along the machine axis x 399 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22C72A,22C72B,22C72C,22C72D,22C72E,22C72F ...
NEW CYLI
DIAM 398.9
HEIG 603.8
ORI Z IS E AND Y IS U
POS E 19568.7 N 17407.3 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS E AND Y IS U
POS E 19285.0 N 17407.3 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS E AND Y IS U
POS E 19852.5 N 17407.3 U 313.3

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17612.4 U 313.3

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17596.7 U 391.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17552.3 U 458.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17485.8 U 502.7

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17407.3 U 518.3

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17328.8 U 502.7

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17262.3 U 458.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17217.9 U 391.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17202.3 U 313.3

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17217.9 U 234.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17262.3 U 168.3

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17328.8 U 123.9

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17407.3 U 108.2

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17485.8 U 123.9

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17552.3 U 168.3

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19568.7 N 17596.7 U 234.8

-- Motor terminal box
NEW BOX
XLEN 181.1
YLEN 159.6
ZLEN 87.8
POS E 19568.7 N 17407.3 U 556.6

-- Motor cable gland
NEW CYLI
DIAM 29.8
HEIG 87.8
ORI Z IS N AND Y IS U
POS E 19568.7 N 17531.0 U 556.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 47.9
YLEN 27.9
ZLEN 39.9
POS E 19399.7 N 17407.3 U 561.0

-- Reference Value: motor nameplate
NEW BOX
XLEN 108.7
YLEN 51.9
ZLEN 6.0
POS E 19641.2 N 17205.8 U 313.3

-- Motor fan cowl disc
NEW CYLI
DIAM 438.8
HEIG 8.0
ORI Z IS E AND Y IS U
POS E 19262.8 N 17407.3 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 201.9
ZLEN 6.4
POS E 19262.8 N 17306.4 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 201.9
ZLEN 6.4
POS E 19262.8 N 17508.2 U 313.3

NEW SUBE /204_PU_006_AUXILIARY
-- 3 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 156x399 at the wet end, outboard of the casing
-- CAD handles: 22C723,22C724,22C725,22C71D,22C71B,22C71C ...
NEW BOX
XLEN 156.3
YLEN 398.9
ZLEN 125.1
POS E 20611.9 N 17407.3 U 112.5

-- Auxiliary [LOW]: body 151x447 at the wet end, outboard of the casing
-- CAD handles: 22C713,22C714,22C712,22C703,22C704,22C705 ...
NEW BOX
XLEN 150.9
YLEN 447.4
ZLEN 120.8
POS E 20738.5 N 17420.8 U 110.4

-- Auxiliary [LOW]: body 22x199 at the wet end, outboard of the casing
-- CAD handles: 22C6EE,22C6EB,22C6EC,22C6ED
NEW BOX
XLEN 21.6
YLEN 199.5
ZLEN 60.0
POS E 20824.8 N 17410.0 U 80.0

NEW SUBE /204_PU_006_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN100; POS is the flange face, contractual direction E
NEW NOZZLE /204_PU_006_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 20902.5 N 17410.0 U 313.3
ORI P1 IS E
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_006_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /204_PU_006_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 20710.9 N 17408.0 U 524.9
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 204-PU-008
-- --------------------------------------------------------------------
-- 204-PU-008 - SAND SEPARATOR FEED PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 204-PU-008
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: E (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 108 mm snapped to catalogue DN100 (nearest available in 'AAZFBB0NN'; catalogue max is DN600)
-- Note: discharge: metadata bore 167 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /204_PU_008
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_008_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 1720.0
YLEN 760.0
ZLEN 50.0
POS E 20000.0 N 19210.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 19230.0 N 18906.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 19230mm N 18906mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 19230.0 N 19514.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 19230mm N 19514mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 20770.0 N 18906.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 20770mm N 18906mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 20770.0 N 19514.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 20770mm N 19514mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /204_PU_008_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 416.6
YLEN 257.5
ZLEN 26.9
POS E 20083.6 N 19210.0 U 63.4

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 210.1
YLEN 129.9
ZLEN 73.9
POS E 20083.6 N 19210.0 U 113.8

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 19974.878652mm N 19154.016185mm U 76.872231mm
ORI Y IS U AND Z IS S
HEIG 22.393526mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 217.358504mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.547177mm N 65.016604mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 19974.878652mm N 19288.37734mm U 76.872231mm
ORI Y IS U AND Z IS S
HEIG 22.393526mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 217.358504mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.547177mm N 65.016604mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 19953.1 N 19210.0 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 19953.142801mm N 19210mm U 76.872231mm
ORI Y IS N AND Z IS U
HEIG 11.644633mm

NEW LOOP
NEW VERTEX
POS E 12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.286444mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N -7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.286444mm U 0mm
END
NEW VERTEX
POS E 12.372423mm N -7.143222mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 20214.0 N 19210.0 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 20213.973006mm N 19210mm U 76.872231mm
ORI Y IS N AND Z IS U
HEIG 11.644633mm

NEW LOOP
NEW VERTEX
POS E 12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.286444mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N -7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.286444mm U 0mm
END
NEW VERTEX
POS E 12.372423mm N -7.143222mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 118.0
YLEN 435.8
ZLEN 45.5
POS E 19378.2 N 19207.3 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 59.5
YLEN 219.8
ZLEN 38.3
POS E 19378.2 N 19207.3 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19347.42857mm N 19112.560627mm U 95.477086mm
ORI Y IS U AND Z IS S
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19347.42857mm N 19339.946056mm U 95.477086mm
ORI Y IS U AND Z IS S
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 19341.3 N 19207.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 19341.27008mm N 19207.304556mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 19415.2 N 19207.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 19415.171958mm N 19207.304556mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 118.0
YLEN 435.8
ZLEN 45.5
POS E 19764.6 N 19207.3 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 59.5
YLEN 219.8
ZLEN 38.3
POS E 19764.6 N 19207.3 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19733.84362mm N 19112.560627mm U 95.477086mm
ORI Y IS U AND Z IS S
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 19733.84362mm N 19339.946056mm U 95.477086mm
ORI Y IS U AND Z IS S
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 19727.7 N 19207.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 19727.685131mm N 19207.304556mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 19801.6 N 19207.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 19801.587009mm N 19207.304556mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 158.1
YLEN 319.0
ZLEN 33.3
POS E 20673.9 N 19220.8 U 66.6

-- Casing support: pedestal web
NEW BOX
XLEN 79.7
YLEN 160.9
ZLEN 20.0
POS E 20673.9 N 19220.8 U 93.3

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 20632.614542mm N 19151.428602mm U 83.289486mm
ORI Y IS U AND Z IS S
HEIG 27.741238mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 82.47979mm N 0mm U 0mm
END
NEW VERTEX
POS E 45.363884mm N 17.6mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 20632.614542mm N 19317.876033mm U 83.289486mm
ORI Y IS U AND Z IS S
HEIG 27.741238mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 82.47979mm N 0mm U 0mm
END
NEW VERTEX
POS E 45.363884mm N 17.6mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 18.0
HEIG 51.3
ORI Z IS U AND Y IS N
POS E 20624.4 N 19220.8 U 66.6

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 20624.366563mm N 19220.781698mm U 83.289486mm
ORI Y IS N AND Z IS U
HEIG 14.425444mm

NEW LOOP
NEW VERTEX
POS E 15.327034mm N 8.849067mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.698135mm U 0mm
END
NEW VERTEX
POS E -15.327034mm N 8.849067mm U 0mm
END
NEW VERTEX
POS E -15.327034mm N -8.849067mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.698135mm U 0mm
END
NEW VERTEX
POS E 15.327034mm N -8.849067mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 18.0
HEIG 51.3
ORI Z IS U AND Y IS N
POS E 20723.3 N 19220.8 U 66.6

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 20723.342311mm N 19220.781698mm U 83.289486mm
ORI Y IS N AND Z IS U
HEIG 14.425444mm

NEW LOOP
NEW VERTEX
POS E 15.327034mm N 8.849067mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.698135mm U 0mm
END
NEW VERTEX
POS E -15.327034mm N 8.849067mm U 0mm
END
NEW VERTEX
POS E -15.327034mm N -8.849067mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.698135mm U 0mm
END
NEW VERTEX
POS E 15.327034mm N -8.849067mm U 0mm
END
END
END

NEW SUBE /204_PU_008_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 275x447 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22C4C8,22C4C9,22C4CA,22C4C2,22C4C0,22C4C1 ...
NEW CYLI
DIAM 447.4
HEIG 274.9
ORI Z IS E AND Y IS U
POS E 20673.9 N 19220.8 U 313.3

-- volute closing onto the suction cover
NEW CONE
DTOP 277.4
DBOT 447.4
HEIG 38.5
ORI Z IS E AND Y IS U
POS E 20830.6 N 19220.8 U 313.3

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 187.9
HEIG 49.5
ORI Z IS E AND Y IS U
POS E 20511.6 N 19220.8 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 143.0
ORI Z IS E AND Y IS U
POS E 20673.9 N 18989.9 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 143.0
ORI Z IS E AND Y IS U
POS E 20673.9 N 19451.7 U 313.3

NEW SUBE /204_PU_008_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 453 mm along the machine axis x 361 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22C4D5,22C4D6,22C4D7,22C49F,22C4A0,22C4A1
NEW CYLI
DIAM 361.2
HEIG 452.8
ORI Z IS E AND Y IS U
POS E 20083.6 N 19210.0 U 313.3

NEW SUBE /204_PU_008_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 70 mm apart running 86 mm along x, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22C450,22C4C6
NEW CYLI
DIAM 70.1
HEIG 86.3
ORI Z IS E AND Y IS U
POS E 20493.3 N 19242.3 U 313.3

-- Coupling hub (d=123) on the shaft centreline
NEW CYLI
DIAM 122.6
HEIG 19.0
ORI Z IS E AND Y IS U
POS E 20459.6 N 19242.3 U 313.3

-- Coupling hub (d=123) on the shaft centreline
NEW CYLI
DIAM 122.6
HEIG 19.0
ORI Z IS E AND Y IS U
POS E 20526.9 N 19242.3 U 313.3

NEW SUBE /204_PU_008_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 604 mm along the machine axis x 399 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22C4CF,22C4D0,22C4D1,22C4D2,22C4D3,22C4D4 ...
NEW CYLI
DIAM 398.9
HEIG 603.8
ORI Z IS E AND Y IS U
POS E 19571.4 N 19207.3 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS E AND Y IS U
POS E 19287.7 N 19207.3 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS E AND Y IS U
POS E 19855.2 N 19207.3 U 313.3

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19412.4 U 313.3

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19396.7 U 391.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19352.3 U 458.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19285.8 U 502.7

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19207.3 U 518.3

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19128.8 U 502.7

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19062.3 U 458.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19017.9 U 391.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19002.3 U 313.3

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19017.9 U 234.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19062.3 U 168.3

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19128.8 U 123.9

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19207.3 U 108.2

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19285.8 U 123.9

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19352.3 U 168.3

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS E AND Y IS U
POS E 19571.4 N 19396.7 U 234.8

-- Motor terminal box
NEW BOX
XLEN 181.1
YLEN 159.6
ZLEN 87.8
POS E 19571.4 N 19207.3 U 556.6

-- Motor cable gland
NEW CYLI
DIAM 29.8
HEIG 87.8
ORI Z IS N AND Y IS U
POS E 19571.4 N 19331.0 U 556.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 47.9
YLEN 27.9
ZLEN 39.9
POS E 19402.4 N 19207.3 U 561.0

-- Reference Value: motor nameplate
NEW BOX
XLEN 108.7
YLEN 51.9
ZLEN 6.0
POS E 19643.9 N 19005.8 U 313.3

-- Motor fan cowl disc
NEW CYLI
DIAM 438.8
HEIG 8.0
ORI Z IS E AND Y IS U
POS E 19265.5 N 19207.3 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 201.9
ZLEN 6.4
POS E 19265.5 N 19106.4 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 201.9
ZLEN 6.4
POS E 19265.5 N 19308.2 U 313.3

NEW SUBE /204_PU_008_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: small fitting 81x65
-- CAD handles: 22C4C7,22C452
NEW BOX
XLEN 80.9
YLEN 64.7
ZLEN 60.0
POS E 20350.4 N 19175.0 U 80.0

NEW SUBE /204_PU_008_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN100; POS is the flange face, contractual direction E
NEW NOZZLE /204_PU_008_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 20900.0 N 19210.0 U 313.3
ORI P1 IS E
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_008_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /204_PU_008_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 20673.9 N 19220.8 U 687.0
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 204-PU-015
-- --------------------------------------------------------------------
-- 204-PU-015 - PRESSURE SCREEN REJECTION DILUTION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 204-PU-015
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 221 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /204_PU_015
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_015_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 863.0
YLEN 2135.0
ZLEN 50.0
POS E 22512.0 N 14092.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 22132.3 N 13114.5 U 69.4

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 22132.28mm N 13114.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 22132.3 N 15069.5 U 69.4

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 22132.28mm N 15069.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 22891.7 N 13114.5 U 69.4

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 22891.72mm N 13114.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 22891.7 N 15069.5 U 69.4

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 22891.72mm N 15069.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

NEW SUBE /204_PU_015_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 187.6
ZLEN 73.7
POS E 22512.0 N 13262.0 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.6
ZLEN 62.1
POS E 22512.0 N 13262.0 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 22665.638824mm N 13213.0889mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.876022mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.831812mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 22296.905647mm N 13213.0889mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.876022mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.831812mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 22512.0 N 13203.3 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 22512mm N 13203.301298mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 22512.0 N 13320.8 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 22512mm N 13320.752525mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 187.6
ZLEN 73.7
POS E 22512.0 N 13876.2 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.6
ZLEN 62.1
POS E 22512.0 N 13876.2 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 22665.638824mm N 13827.212962mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.876022mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.831812mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 22296.905647mm N 13827.212962mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.876022mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.831812mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 22512.0 N 13817.4 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 22512mm N 13817.42536mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 22512.0 N 13934.9 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 22512mm N 13934.876587mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 157.6
YLEN 396.8
ZLEN 16.4
POS E 22509.3 N 14264.5 U 58.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 79.5
YLEN 200.1
ZLEN 311.0
POS E 22509.3 N 14264.5 U 222.0

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 22543.56331mm N 14161.002739mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 207.008074mm N 0mm U 0mm
END
NEW VERTEX
POS E 113.854441mm N 273.723212mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 22461.3423mm N 14161.002739mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 207.008074mm N 0mm U 0mm
END
NEW VERTEX
POS E 113.854441mm N 273.723212mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 22509.3 N 14140.3 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 22509.304556mm N 14140.301932mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 22509.3 N 14388.7 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 22509.304556mm N 14388.71162mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 465.1
YLEN 131.3
ZLEN 48.5
POS E 22541.6 N 15005.7 U 74.3

-- Casing support: pedestal web
NEW BOX
XLEN 234.6
YLEN 66.2
ZLEN 65.3
POS E 22541.6 N 15005.7 U 131.2

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 22642.754707mm N 14971.501401mm U 98.530465mm
ORI Y IS U AND Z IS E
HEIG 40.442054mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 68.490576mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.669817mm N 57.485088mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 22400.102381mm N 14971.501401mm U 98.530465mm
ORI Y IS U AND Z IS E
HEIG 40.442054mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 68.490576mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.669817mm N 57.485088mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.3
HEIG 74.8
ORI Z IS U AND Y IS N
POS E 22541.6 N 14964.7 U 74.3

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 22541.649571mm N 14964.652343mm U 98.530465mm
ORI Y IS N AND Z IS U
HEIG 21.029868mm

NEW LOOP
NEW VERTEX
POS E 22.344235mm N 12.90045mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.8009mm U 0mm
END
NEW VERTEX
POS E -22.344235mm N 12.90045mm U 0mm
END
NEW VERTEX
POS E -22.344235mm N -12.90045mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.8009mm U 0mm
END
NEW VERTEX
POS E 22.344235mm N -12.90045mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.3
HEIG 74.8
ORI Z IS U AND Y IS N
POS E 22541.6 N 15046.8 U 74.3

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 22541.649571mm N 15046.841034mm U 98.530465mm
ORI Y IS N AND Z IS U
HEIG 21.029868mm

NEW LOOP
NEW VERTEX
POS E 22.344235mm N 12.90045mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.8009mm U 0mm
END
NEW VERTEX
POS E -22.344235mm N 12.90045mm U 0mm
END
NEW VERTEX
POS E -22.344235mm N -12.90045mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.8009mm U 0mm
END
NEW VERTEX
POS E 22.344235mm N -12.90045mm U 0mm
END
END
END

NEW SUBE /204_PU_015_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 210x652 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22C431,22C432,22C433,22C434,22C435,22C436 ...
NEW CYLI
DIAM 652.3
HEIG 228.3
ORI Z IS N AND Y IS U
POS E 22541.6 N 15005.7 U 477.0

-- volute closing onto the suction cover
NEW CONE
DTOP 404.4
DBOT 652.3
HEIG 29.5
ORI Z IS N AND Y IS U
POS E 22541.6 N 15134.6 U 477.0

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 274.0
HEIG 41.1
ORI Z IS N AND Y IS U
POS E 22541.6 N 14871.0 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 118.7
ORI Z IS N AND Y IS U
POS E 22875.0 N 15005.7 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 118.7
ORI Z IS N AND Y IS U
POS E 22208.3 N 15005.7 U 477.0

NEW SUBE /204_PU_015_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 431x221 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 22C414,22C415,22C416
NEW CYLI
DIAM 221.0
HEIG 431.3
ORI Z IS N AND Y IS U
POS E 22509.3 N 14264.5 U 477.0

NEW SUBE /204_PU_015_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 199 mm apart running 248 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22C418,22C417
NEW CYLI
DIAM 199.5
HEIG 248.0
ORI Z IS N AND Y IS U
POS E 22509.3 N 14604.1 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 22509.3 N 14507.4 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 22509.3 N 14700.8 U 477.0

NEW SUBE /204_PU_015_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 960 mm along the machine axis x 647 mm across, consolidated from 2 drawn sections (body, fin bands, cowl)
-- CAD handles: 22C43A,22C43B,22C43C,22C444,22C445,22C446 ...
NEW CYLI
DIAM 646.9
HEIG 959.6
ORI Z IS N AND Y IS U
POS E 22512.0 N 13569.1 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.6
ORI Z IS N AND Y IS U
POS E 22512.0 N 13118.1 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.6
ORI Z IS N AND Y IS U
POS E 22512.0 N 14020.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22180.5 N 13569.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22205.8 N 13569.1 U 603.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22277.6 N 13569.1 U 711.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22385.2 N 13569.1 U 783.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22512.0 N 13569.1 U 808.4

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22638.8 N 13569.1 U 783.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22746.4 N 13569.1 U 711.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22818.2 N 13569.1 U 603.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22843.5 N 13569.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22818.2 N 13569.1 U 350.1

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22746.4 N 13569.1 U 242.6

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22638.8 N 13569.1 U 170.7

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22512.0 N 13569.1 U 145.5

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22385.2 N 13569.1 U 170.7

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22277.6 N 13569.1 U 242.6

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 22205.8 N 13569.1 U 350.1

-- Motor terminal box
NEW BOX
XLEN 258.8
YLEN 287.9
ZLEN 142.3
POS E 22512.0 N 13569.1 U 871.6

-- Motor cable gland
NEW CYLI
DIAM 48.4
HEIG 142.3
ORI Z IS E AND Y IS U
POS E 22311.5 N 13569.1 U 871.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.3
YLEN 77.6
ZLEN 64.7
POS E 22512.0 N 13300.4 U 878.7

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.1
YLEN 172.7
ZLEN 6.0
POS E 22837.5 N 13684.2 U 477.0

-- Motor fan cowl disc
NEW CYLI
DIAM 711.6
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 22512.0 N 13085.3 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 22675.7 N 13085.3 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 22348.3 N 13085.3 U 477.0

NEW SUBE /204_PU_015_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 173x334 at the wet end, outboard of the casing
-- CAD handles: 22C419,22C41A,22C41B
NEW BOX
XLEN 334.2
YLEN 172.5
ZLEN 138.0
POS E 22512.0 N 14814.4 U 119.0

NEW SUBE /204_PU_015_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /204_PU_015_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 22512.0 N 15154.3 U 477.0
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_015_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /204_PU_015_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 22541.6 N 15005.7 U 953.1
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 204-PU-016
-- --------------------------------------------------------------------
-- 204-PU-016 - FEED TANK BOTTOM DILUTION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 204-PU-016
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 221 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /204_PU_016
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_016_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 857.0
YLEN 2129.0
ZLEN 50.0
POS E 28213.0 N 14089.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 27835.9 N 13114.5 U 69.3

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 27835.92mm N 13114.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 27835.9 N 15063.5 U 69.3

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 27835.92mm N 15063.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 28590.1 N 13114.5 U 69.3

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 28590.08mm N 13114.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 28590.1 N 15063.5 U 69.3

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 28590.08mm N 15063.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

NEW SUBE /204_PU_016_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 186.5
ZLEN 73.7
POS E 28215.7 N 13260.8 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.1
ZLEN 62.1
POS E 28215.7 N 13260.8 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 28369.334189mm N 13212.08892mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 28000.601012mm N 13212.08892mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 28215.7 N 13202.4 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 28215.695365mm N 13202.356305mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 28215.7 N 13319.1 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 28215.695365mm N 13319.147687mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 186.5
ZLEN 73.7
POS E 28215.7 N 13871.4 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.1
ZLEN 62.1
POS E 28215.7 N 13871.4 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 28369.334189mm N 13822.762813mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 28000.601012mm N 13822.762813mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 28215.7 N 13813.0 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 28215.695365mm N 13813.030198mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 28215.7 N 13929.8 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 28215.695365mm N 13929.82158mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 157.6
YLEN 401.7
ZLEN 16.4
POS E 28213.0 N 14261.5 U 58.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 79.5
YLEN 202.6
ZLEN 311.0
POS E 28213.0 N 14261.5 U 222.0

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 28247.258779mm N 14156.708926mm U 66.444214mm
ORI Y IS U AND Z IS E
HEIG 13.703511mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 273.723138mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 28165.03771mm N 14156.708926mm U 66.444214mm
ORI Y IS U AND Z IS E
HEIG 13.703511mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 273.723138mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 28213.0 N 14135.7 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 28213mm N 14135.749356mm U 66.444214mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 28213.0 N 14387.3 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 28213mm N 14387.264196mm U 66.444214mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 465.1
YLEN 131.3
ZLEN 48.5
POS E 28245.3 N 15005.4 U 74.3

-- Casing support: pedestal web
NEW BOX
XLEN 234.6
YLEN 66.2
ZLEN 65.3
POS E 28245.3 N 15005.4 U 131.2

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 28346.450127mm N 14971.196853mm U 98.530453mm
ORI Y IS U AND Z IS E
HEIG 40.442044mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 68.490559mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.669808mm N 57.485166mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 28103.79786mm N 14971.196853mm U 98.530453mm
ORI Y IS U AND Z IS E
HEIG 40.442044mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 68.490559mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.669808mm N 57.485166mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.3
HEIG 74.8
ORI Z IS U AND Y IS N
POS E 28245.3 N 14964.3 U 74.3

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 28245.345016mm N 14964.347797mm U 98.530453mm
ORI Y IS N AND Z IS U
HEIG 21.029863mm

NEW LOOP
NEW VERTEX
POS E 22.34423mm N 12.900447mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.800894mm U 0mm
END
NEW VERTEX
POS E -22.34423mm N 12.900447mm U 0mm
END
NEW VERTEX
POS E -22.34423mm N -12.900447mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.800894mm U 0mm
END
NEW VERTEX
POS E 22.34423mm N -12.900447mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.3
HEIG 74.8
ORI Z IS U AND Y IS N
POS E 28245.3 N 15046.5 U 74.3

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 28245.345016mm N 15046.536469mm U 98.530453mm
ORI Y IS N AND Z IS U
HEIG 21.029863mm

NEW LOOP
NEW VERTEX
POS E 22.34423mm N 12.900447mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.800894mm U 0mm
END
NEW VERTEX
POS E -22.34423mm N 12.900447mm U 0mm
END
NEW VERTEX
POS E -22.34423mm N -12.900447mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.800894mm U 0mm
END
NEW VERTEX
POS E 22.34423mm N -12.900447mm U 0mm
END
END
END

NEW SUBE /204_PU_016_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 210x652 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22BC8D,22BC8E,22BC8F,22BC90,22BC91,22BC92 ...
NEW CYLI
DIAM 652.3
HEIG 228.3
ORI Z IS N AND Y IS U
POS E 28245.3 N 15005.4 U 477.0

-- volute closing onto the suction cover
NEW CONE
DTOP 404.4
DBOT 652.3
HEIG 24.1
ORI Z IS N AND Y IS U
POS E 28245.3 N 15131.6 U 477.0

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 274.0
HEIG 41.1
ORI Z IS N AND Y IS U
POS E 28245.3 N 14870.7 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 118.7
ORI Z IS N AND Y IS U
POS E 28578.7 N 15005.4 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 118.7
ORI Z IS N AND Y IS U
POS E 27912.0 N 15005.4 U 477.0

NEW SUBE /204_PU_016_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 437x221 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 22BC6C,22BC6D,22BC6E
NEW CYLI
DIAM 221.0
HEIG 436.7
ORI Z IS N AND Y IS U
POS E 28213.0 N 14261.5 U 477.0

NEW SUBE /204_PU_016_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 199 mm apart running 248 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BC70,22BC6F
NEW CYLI
DIAM 199.5
HEIG 248.0
ORI Z IS N AND Y IS U
POS E 28213.0 N 14603.8 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 28213.0 N 14507.1 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 28213.0 N 14700.5 U 477.0

NEW SUBE /204_PU_016_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 954 mm along the machine axis x 647 mm across, consolidated from 2 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BC9A,22BC9B,22BC9C,22BCA0,22BCA1,22BCA2 ...
NEW CYLI
DIAM 646.9
HEIG 954.2
ORI Z IS N AND Y IS U
POS E 28215.7 N 13566.1 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 28215.7 N 13117.6 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 28215.7 N 14014.6 U 477.0

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 27884.2 N 13566.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 27909.5 N 13566.1 U 603.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 27981.3 N 13566.1 U 711.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28088.9 N 13566.1 U 783.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28215.7 N 13566.1 U 808.4

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28342.5 N 13566.1 U 783.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28450.1 N 13566.1 U 711.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28521.9 N 13566.1 U 603.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28547.1 N 13566.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28521.9 N 13566.1 U 350.1

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28450.1 N 13566.1 U 242.6

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28342.5 N 13566.1 U 170.7

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28215.7 N 13566.1 U 145.5

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 28088.9 N 13566.1 U 170.7

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 27981.3 N 13566.1 U 242.6

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 27909.5 N 13566.1 U 350.1

-- Motor terminal box
NEW BOX
XLEN 258.8
YLEN 286.3
ZLEN 142.3
POS E 28215.7 N 13566.1 U 871.6

-- Motor cable gland
NEW CYLI
DIAM 48.4
HEIG 142.3
ORI Z IS E AND Y IS U
POS E 28015.2 N 13566.1 U 871.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.3
YLEN 77.6
ZLEN 64.7
POS E 28215.7 N 13298.9 U 878.7

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.1
YLEN 171.8
ZLEN 6.0
POS E 28541.1 N 13680.6 U 477.0

-- Motor fan cowl disc
NEW CYLI
DIAM 711.6
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 28215.7 N 13085.0 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 28379.4 N 13085.0 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 28052.0 N 13085.0 U 477.0

NEW SUBE /204_PU_016_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 173x329 at the wet end, outboard of the casing
-- CAD handles: 22BC71,22BC72,22BC73
NEW BOX
XLEN 328.8
YLEN 172.5
ZLEN 138.0
POS E 28213.0 N 14814.1 U 119.0

NEW SUBE /204_PU_016_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /204_PU_016_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 28213.0 N 15154.0 U 477.0
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_016_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /204_PU_016_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 28245.3 N 15005.4 U 953.1
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 204-PU-017
-- --------------------------------------------------------------------
-- 204-PU-017 - POST OXYGEN FILTRATE PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 204-PU-017
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 85 mm snapped to catalogue DN80 (nearest available in 'AAZFBB0LL'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /204_PU_017
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_017_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 25814.0 N 14294.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 25479.6 N 13524.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 25479.6mm N 13524mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 25479.6 N 15064.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 25479.6mm N 15064mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 26148.4 N 13524.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 26148.4mm N 13524mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 26148.4 N 15064.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 26148.4mm N 15064mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /204_PU_017_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 257.5
YLEN 416.6
ZLEN 26.9
POS E 25814.0 N 14377.6 U 63.4

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 129.9
YLEN 210.1
ZLEN 73.9
POS E 25814.0 N 14377.6 U 113.8

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 25869.983919mm N 14268.878652mm U 76.872243mm
ORI Y IS U AND Z IS E
HEIG 22.393536mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 217.358504mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.547177mm N 65.016623mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 25735.622705mm N 14268.878652mm U 76.872243mm
ORI Y IS U AND Z IS E
HEIG 22.393536mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 217.358504mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.547177mm N 65.016623mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 25814.0 N 14247.1 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 25814.00008mm N 14247.142801mm U 76.872243mm
ORI Y IS N AND Z IS U
HEIG 11.644639mm

NEW LOOP
NEW VERTEX
POS E 12.372428mm N 7.143225mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.28645mm U 0mm
END
NEW VERTEX
POS E -12.372428mm N 7.143225mm U 0mm
END
NEW VERTEX
POS E -12.372428mm N -7.143225mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.28645mm U 0mm
END
NEW VERTEX
POS E 12.372428mm N -7.143225mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 25814.0 N 14508.0 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 25814.00008mm N 14507.973006mm U 76.872243mm
ORI Y IS N AND Z IS U
HEIG 11.644639mm

NEW LOOP
NEW VERTEX
POS E 12.372428mm N 7.143225mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.28645mm U 0mm
END
NEW VERTEX
POS E -12.372428mm N 7.143225mm U 0mm
END
NEW VERTEX
POS E -12.372428mm N -7.143225mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.28645mm U 0mm
END
NEW VERTEX
POS E 12.372428mm N -7.143225mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 435.8
YLEN 118.0
ZLEN 45.5
POS E 25811.3 N 13672.2 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 219.8
YLEN 59.5
ZLEN 38.3
POS E 25811.3 N 13672.2 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 25906.048602mm N 13641.42857mm U 95.477104mm
ORI Y IS U AND Z IS E
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 25678.663082mm N 13641.42857mm U 95.477104mm
ORI Y IS U AND Z IS E
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 25811.3 N 13635.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 25811.304635mm N 13635.27008mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 25811.3 N 13709.2 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 25811.304635mm N 13709.171958mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 435.8
YLEN 118.0
ZLEN 45.5
POS E 25811.3 N 14058.6 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 219.8
YLEN 59.5
ZLEN 38.3
POS E 25811.3 N 14058.6 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 25906.048602mm N 14027.84362mm U 95.477104mm
ORI Y IS U AND Z IS E
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 25678.663082mm N 14027.84362mm U 95.477104mm
ORI Y IS U AND Z IS E
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 25811.3 N 14021.7 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 25811.304635mm N 14021.685131mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 25811.3 N 14095.6 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 25811.304635mm N 14095.587009mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 143.2
YLEN 71.6
ZLEN 14.9
POS E 25812.0 N 15006.3 U 57.5

-- Casing support: pedestal web
NEW BOX
XLEN 72.2
YLEN 36.1
ZLEN 152.0
POS E 25812.0 N 15006.3 U 140.9

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 25843.098987mm N 14987.591888mm U 64.937836mm
ORI Y IS U AND Z IS E
HEIG 12.448196mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.344589mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.539524mm N 133.740224mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 25768.409809mm N 14987.591888mm U 64.937836mm
ORI Y IS U AND Z IS E
HEIG 12.448196mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.344589mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.539524mm N 133.740224mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 26.9
ORI Z IS U AND Y IS N
POS E 25812.0 N 14983.9 U 57.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 25811.978496mm N 14983.857429mm U 64.937836mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 26.9
ORI Z IS U AND Y IS N
POS E 25812.0 N 15028.7 U 57.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 25811.978496mm N 15028.670936mm U 64.937836mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /204_PU_017_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 100; the only large round feature in the plan, at the wet end
-- CAD handles: 22BC25,22BC1E,22BC1F,22BC20,22BC21,22BC22 ...
NEW CYLI
DIAM 200.8
HEIG 124.5
ORI Z IS U AND Y IS N
POS E 25812.0 N 15006.3 U 313.3

-- casing split flange at the cover joint
NEW CYLI
DIAM 220.9
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 25812.0 N 15006.3 U 383.5

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 25812.0 N 15105.9 U 373.9

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 25811.978496mm N 15105.891731mm U 391.529478mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 25741.5 N 15076.7 U 373.9

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 25741.531181mm N 15076.711498mm U 391.529478mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 25712.4 N 15006.3 U 373.9

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 25712.350948mm N 15006.264183mm U 391.529478mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 25741.5 N 14935.8 U 373.9

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 25741.531181mm N 14935.816868mm U 391.529478mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 25812.0 N 14906.6 U 373.9

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 25811.978496mm N 14906.636634mm U 391.529478mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 25882.4 N 14935.8 U 373.9

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 25882.425811mm N 14935.816868mm U 391.529478mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 25911.6 N 15006.3 U 373.9

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 25911.606045mm N 15006.264183mm U 391.529478mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 25882.4 N 15076.7 U 373.9

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 25882.425811mm N 15076.711498mm U 391.529478mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 124.5
DBOT 200.8
HEIG 37.3
ORI Z IS N AND Y IS U
POS E 25812.0 N 15087.2 U 313.3

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 84.3
HEIG 22.4
ORI Z IS N AND Y IS U
POS E 25812.0 N 14932.8 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 64.7
ORI Z IS N AND Y IS U
POS E 25916.0 N 15006.3 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 64.7
ORI Z IS N AND Y IS U
POS E 25708.0 N 15006.3 U 313.3

NEW SUBE /204_PU_017_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 453 mm along the machine axis x 361 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22BC5C,22BC5D,22BC5E,22BC26,22BC27,22BC28
NEW CYLI
DIAM 361.2
HEIG 452.8
ORI Z IS N AND Y IS U
POS E 25814.0 N 14377.6 U 313.3

NEW SUBE /204_PU_017_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 226 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BC4E,22BC4D
NEW CYLI
DIAM 134.8
HEIG 226.4
ORI Z IS N AND Y IS U
POS E 25814.0 N 14717.2 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 49.8
ORI Z IS N AND Y IS U
POS E 25814.0 N 14628.9 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 49.8
ORI Z IS N AND Y IS U
POS E 25814.0 N 14805.5 U 313.3

NEW SUBE /204_PU_017_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 604 mm along the machine axis x 399 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BC56,22BC57,22BC58,22BC59,22BC5A,22BC5B ...
NEW CYLI
DIAM 398.9
HEIG 603.8
ORI Z IS N AND Y IS U
POS E 25811.3 N 13865.4 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS N AND Y IS U
POS E 25811.3 N 13581.7 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS N AND Y IS U
POS E 25811.3 N 14149.2 U 313.3

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25606.3 N 13865.4 U 313.3

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25621.9 N 13865.4 U 391.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25666.3 N 13865.4 U 458.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25732.8 N 13865.4 U 502.7

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25811.3 N 13865.4 U 518.3

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25889.8 N 13865.4 U 502.7

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25956.3 N 13865.4 U 458.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 26000.7 N 13865.4 U 391.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 26016.4 N 13865.4 U 313.3

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 26000.7 N 13865.4 U 234.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25956.3 N 13865.4 U 168.3

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25889.8 N 13865.4 U 123.9

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25811.3 N 13865.4 U 108.2

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25732.8 N 13865.4 U 123.9

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25666.3 N 13865.4 U 168.3

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 25621.9 N 13865.4 U 234.8

-- Motor terminal box
NEW BOX
XLEN 159.6
YLEN 181.1
ZLEN 87.8
POS E 25811.3 N 13865.4 U 556.6

-- Motor cable gland
NEW CYLI
DIAM 29.8
HEIG 87.8
ORI Z IS E AND Y IS U
POS E 25687.6 N 13865.4 U 556.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 27.9
YLEN 47.9
ZLEN 39.9
POS E 25811.3 N 13696.4 U 561.0

-- Reference Value: motor nameplate
NEW BOX
XLEN 51.9
YLEN 108.7
ZLEN 6.0
POS E 26012.8 N 13937.9 U 313.3

-- Motor fan cowl disc
NEW CYLI
DIAM 438.8
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 25811.3 N 13559.5 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 201.9
YLEN 9.6
ZLEN 6.4
POS E 25912.2 N 13559.5 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 201.9
YLEN 9.6
ZLEN 6.4
POS E 25710.4 N 13559.5 U 313.3

NEW SUBE /204_PU_017_AUXILIARY
-- 3 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 156x399 at the wet end, outboard of the casing
-- CAD handles: 22BC4F,22BC50,22BC51,22BC4B,22BC4C,22BC4A ...
NEW BOX
XLEN 398.9
YLEN 156.3
ZLEN 125.1
POS E 25811.3 N 14908.6 U 112.5

-- Auxiliary [LOW]: body 124x447 at the wet end, outboard of the casing
-- CAD handles: 22BC39,22BC3A,22BC3B,22BC3C,22BC3D,22BC3E ...
NEW BOX
XLEN 447.4
YLEN 124.0
ZLEN 99.2
POS E 25824.8 N 15016.4 U 99.6

-- Auxiliary [LOW]: body 27x199 at the wet end, outboard of the casing
-- CAD handles: 22BC1A,22BC17,22BC18,22BC19
NEW BOX
XLEN 199.5
YLEN 27.0
ZLEN 60.0
POS E 25814.0 N 15118.8 U 80.0

NEW SUBE /204_PU_017_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN80; POS is the flange face, contractual direction N
NEW NOZZLE /204_PU_017_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 25814.0 N 15133.8 U 313.3
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_017_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /204_PU_017_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 25812.0 N 15006.3 U 525.5
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 204-PU-023
-- --------------------------------------------------------------------
-- 204-PU-023 - POST OXYGEN DD WASHER RETURN FILTRATE PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 204-PU-023
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 92 mm snapped to catalogue DN90 (nearest available in 'AAZFBB0MM'; catalogue max is DN600)
-- Note: discharge: metadata bore 151 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /204_PU_023
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_023_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1725.0
ZLEN 50.0
POS E 28520.0 N 415.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 28185.6 N -357.5 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 28185.6mm N -357.5mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 28185.6 N 1187.5 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 28185.6mm N 1187.5mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 28854.4 N -357.5 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 28854.4mm N -357.5mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 28854.4 N 1187.5 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 28854.4mm N 1187.5mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /204_PU_023_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 257.5
YLEN 421.6
ZLEN 26.9
POS E 28520.0 N 498.6 U 63.4

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 129.9
YLEN 212.6
ZLEN 73.9
POS E 28520.0 N 498.6 U 113.8

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 28575.983815mm N 388.584956mm U 76.872231mm
ORI Y IS U AND Z IS E
HEIG 22.393526mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 219.946055mm N 0mm U 0mm
END
NEW VERTEX
POS E 120.97033mm N 65.016604mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 28441.62266mm N 388.584956mm U 76.872231mm
ORI Y IS U AND Z IS E
HEIG 22.393526mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 219.946055mm N 0mm U 0mm
END
NEW VERTEX
POS E 120.97033mm N 65.016604mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 28520.0 N 366.6 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 28520mm N 366.590351mm U 76.872231mm
ORI Y IS N AND Z IS U
HEIG 11.644633mm

NEW LOOP
NEW VERTEX
POS E 12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.286444mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N -7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.286444mm U 0mm
END
NEW VERTEX
POS E 12.372423mm N -7.143222mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 28520.0 N 630.5 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 28520mm N 630.525616mm U 76.872231mm
ORI Y IS N AND Z IS U
HEIG 11.644633mm

NEW LOOP
NEW VERTEX
POS E 12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.286444mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N 7.143222mm U 0mm
END
NEW VERTEX
POS E -12.372423mm N -7.143222mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.286444mm U 0mm
END
NEW VERTEX
POS E 12.372423mm N -7.143222mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 435.8
YLEN 118.0
ZLEN 45.5
POS E 28517.3 N -209.5 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 219.8
YLEN 59.5
ZLEN 38.3
POS E 28517.3 N -209.5 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 28612.048484mm N -240.266854mm U 95.477086mm
ORI Y IS U AND Z IS E
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584915mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871703mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 28384.663055mm N -240.266854mm U 95.477086mm
ORI Y IS U AND Z IS E
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584915mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871703mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 28517.3 N -246.4 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 28517.304556mm N -246.425346mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 28517.3 N -172.5 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 28517.304556mm N -172.523448mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 435.8
YLEN 118.0
ZLEN 45.5
POS E 28517.3 N 176.9 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 219.8
YLEN 59.5
ZLEN 38.3
POS E 28517.3 N 176.9 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 28612.048484mm N 146.148298mm U 95.477086mm
ORI Y IS U AND Z IS E
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584915mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871703mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 28384.663055mm N 146.148298mm U 95.477086mm
ORI Y IS U AND Z IS E
HEIG 37.897571mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584915mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871703mm N 33.700914mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 28517.3 N 140.0 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 28517.304556mm N 139.989807mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 28517.3 N 213.9 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 28517.304556mm N 213.891705mm U 95.477086mm
ORI Y IS N AND Z IS U
HEIG 19.706737mm

NEW LOOP
NEW VERTEX
POS E 20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177591mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N 12.088796mm U 0mm
END
NEW VERTEX
POS E -20.938408mm N -12.088796mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177591mm U 0mm
END
NEW VERTEX
POS E 20.938408mm N -12.088796mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 141.8
YLEN 70.9
ZLEN 14.8
POS E 28518.0 N 1125.9 U 57.4

-- Casing support: pedestal web
NEW BOX
XLEN 71.5
YLEN 35.8
ZLEN 153.0
POS E 28518.0 N 1125.9 U 141.3

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 28548.799302mm N 1107.424001mm U 64.794016mm
ORI Y IS U AND Z IS E
HEIG 12.328346mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 36.985039mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.341771mm N 134.683221mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 28474.829225mm N 1107.424001mm U 64.794016mm
ORI Y IS U AND Z IS E
HEIG 12.328346mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 36.985039mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.341771mm N 134.683221mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 26.8
ORI Z IS U AND Y IS N
POS E 28518.0 N 1103.7 U 57.4

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 28517.978437mm N 1103.725497mm U 64.794016mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 26.8
ORI Z IS U AND Y IS N
POS E 28518.0 N 1148.1 U 57.4

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 28517.978437mm N 1148.107543mm U 64.794016mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /204_PU_023_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 99; the only large round feature in the plan, at the wet end
-- CAD handles: 22C2E8,22C2E1,22C2E2,22C2E3,22C2E4,22C2E5 ...
NEW CYLI
DIAM 198.8
HEIG 123.3
ORI Z IS U AND Y IS N
POS E 28518.0 N 1125.9 U 313.3

-- casing split flange at the cover joint
NEW CYLI
DIAM 218.7
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 28518.0 N 1125.9 U 382.9

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 28518.0 N 1224.5 U 373.3

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 28517.978437mm N 1224.480882mm U 390.930123mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 28448.3 N 1195.6 U 373.3

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 28448.282908mm N 1195.612049mm U 390.930123mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 28419.4 N 1125.9 U 373.3

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 28419.414075mm N 1125.91652mm U 390.930123mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 28448.3 N 1056.2 U 373.3

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 28448.282908mm N 1056.220991mm U 390.930123mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 28518.0 N 1027.4 U 373.3

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 28517.978437mm N 1027.352158mm U 390.930123mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 28587.7 N 1056.2 U 373.3

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 28587.673965mm N 1056.220991mm U 390.930123mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 28616.5 N 1125.9 U 373.3

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 28616.542798mm N 1125.91652mm U 390.930123mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 28587.7 N 1195.6 U 373.3

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 28587.673965mm N 1195.612049mm U 390.930123mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 123.3
DBOT 198.8
HEIG 37.0
ORI Z IS N AND Y IS U
POS E 28518.0 N 1206.1 U 313.3

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 83.5
HEIG 22.2
ORI Z IS N AND Y IS U
POS E 28518.0 N 1053.2 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 64.1
ORI Z IS N AND Y IS U
POS E 28621.0 N 1125.9 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 64.1
ORI Z IS N AND Y IS U
POS E 28415.0 N 1125.9 U 313.3

NEW SUBE /204_PU_023_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 458 mm along the machine axis x 361 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22C31F,22C320,22C321,22C2E9,22C2EA,22C2EB
NEW CYLI
DIAM 361.2
HEIG 458.2
ORI Z IS N AND Y IS U
POS E 28520.0 N 498.6 U 313.3

NEW SUBE /204_PU_023_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 221 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22C311,22C310
NEW CYLI
DIAM 134.8
HEIG 221.0
ORI Z IS N AND Y IS U
POS E 28520.0 N 838.2 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 48.6
ORI Z IS N AND Y IS U
POS E 28520.0 N 752.0 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 48.6
ORI Z IS N AND Y IS U
POS E 28520.0 N 924.4 U 313.3

NEW SUBE /204_PU_023_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 604 mm along the machine axis x 399 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22C319,22C31A,22C31B,22C31C,22C31D,22C31E ...
NEW CYLI
DIAM 398.9
HEIG 603.8
ORI Z IS N AND Y IS U
POS E 28517.3 N -16.3 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS N AND Y IS U
POS E 28517.3 N -300.0 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS N AND Y IS U
POS E 28517.3 N 267.5 U 313.3

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28312.3 N -16.3 U 313.3

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28327.9 N -16.3 U 391.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28372.3 N -16.3 U 458.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28438.8 N -16.3 U 502.7

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28517.3 N -16.3 U 518.3

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28595.8 N -16.3 U 502.7

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28662.3 N -16.3 U 458.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28706.7 N -16.3 U 391.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28722.4 N -16.3 U 313.3

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28706.7 N -16.3 U 234.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28662.3 N -16.3 U 168.3

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28595.8 N -16.3 U 123.9

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28517.3 N -16.3 U 108.2

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28438.8 N -16.3 U 123.9

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28372.3 N -16.3 U 168.3

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 28327.9 N -16.3 U 234.8

-- Motor terminal box
NEW BOX
XLEN 159.6
YLEN 181.1
ZLEN 87.8
POS E 28517.3 N -16.3 U 556.6

-- Motor cable gland
NEW CYLI
DIAM 29.8
HEIG 87.8
ORI Z IS E AND Y IS U
POS E 28393.6 N -16.3 U 556.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 27.9
YLEN 47.9
ZLEN 39.9
POS E 28517.3 N -185.3 U 561.0

-- Reference Value: motor nameplate
NEW BOX
XLEN 51.9
YLEN 108.7
ZLEN 6.0
POS E 28718.8 N 56.2 U 313.3

-- Motor fan cowl disc
NEW CYLI
DIAM 438.8
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 28517.3 N -322.2 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 201.9
YLEN 9.6
ZLEN 6.4
POS E 28618.2 N -322.2 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 201.9
YLEN 9.6
ZLEN 6.4
POS E 28416.4 N -322.2 U 313.3

NEW SUBE /204_PU_023_AUXILIARY
-- 3 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 146x394 at the wet end, outboard of the casing
-- CAD handles: 22C312,22C313,22C314,22C30C,22C30A,22C30B ...
NEW BOX
XLEN 393.5
YLEN 145.6
ZLEN 116.4
POS E 28520.0 N 1021.5 U 108.2

-- Auxiliary [LOW]: body 151x447 at the wet end, outboard of the casing
-- CAD handles: 22C2D6,22C2C2,22C2C3,22C2C4,22C2B6,22C2B7 ...
NEW BOX
XLEN 447.4
YLEN 150.9
ZLEN 120.8
POS E 28530.8 N 1126.6 U 110.4

-- Auxiliary [LOW]: body 22x199 at the wet end, outboard of the casing
-- CAD handles: 22C2DD,22C2DA,22C2DB,22C2DC
NEW BOX
XLEN 199.5
YLEN 21.6
ZLEN 60.0
POS E 28520.0 N 1239.8 U 80.0

NEW SUBE /204_PU_023_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN90; POS is the flange face, contractual direction N
NEW NOZZLE /204_PU_023_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0MM
POS E 28520.0 N 1257.5 U 313.3
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /204_PU_023_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /204_PU_023_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 28518.0 N 1125.9 U 524.9
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-004
-- --------------------------------------------------------------------
-- 205-PU-004 - D0 REACTOR FEED MC PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-004
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: unknown
-- Layout axis: E (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 216 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 151 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)
-- Warning: no shape-reference geometry; the pump must fall back to metadata-driven geometry
-- Warning: no CAD top view in this file; pump body geometry is a metadata-proportioned Reference Value and remains UNCONFIRMED

NEW EQUI /205_PU_004
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_004_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 1725.0
YLEN 760.0
ZLEN 50.0
POS E 30441.0 N -10580.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 29668.5 N -10884.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 29668.5mm N -10884mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 29668.5 N -10276.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 29668.5mm N -10276mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 31213.5 N -10884.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 31213.5mm N -10884mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 31213.5 N -10276.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 31213.5mm N -10276mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /205_PU_004_SUPPORT
-- 24 part(s), 0 nozzle(s)
-- UNCONFIRMED: motor foot: sole plate on the baseplate
NEW BOX
XLEN 141.6
YLEN 431.8
ZLEN 45.1
POS E 29826.9 N -10580.0 U 72.5

-- UNCONFIRMED: motor foot: pedestal web
NEW BOX
XLEN 71.4
YLEN 217.8
ZLEN 103.9
POS E 29826.9 N -10580.0 U 147.0

-- UNCONFIRMED: motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 29789.9505mm N -10673.86mm U 95.0528mm
ORI Y IS U AND Z IS S
HEIG 37.544mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 73.899mm N 0mm U 0mm
END
NEW VERTEX
POS E 40.64445mm N 91.438336mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 29789.9505mm N -10448.596mm U 95.0528mm
ORI Y IS U AND Z IS S
HEIG 37.544mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 73.899mm N 0mm U 0mm
END
NEW VERTEX
POS E 40.64445mm N 91.438336mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.4
HEIG 69.5
ORI Z IS U AND Y IS N
POS E 29782.6 N -10580.0 U 72.5

-- UNCONFIRMED: motor foot: hold-down hex nut
NEW EXTRUSION
POS E 29782.5606mm N -10580mm U 95.0528mm
ORI Y IS N AND Z IS U
HEIG 19.52288mm

NEW LOOP
NEW VERTEX
POS E 20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N 23.952023mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N -11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N -23.952023mm U 0mm
END
NEW VERTEX
POS E 20.74306mm N -11.976011mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.4
HEIG 69.5
ORI Z IS U AND Y IS N
POS E 29871.2 N -10580.0 U 72.5

-- UNCONFIRMED: motor foot: hold-down hex nut
NEW EXTRUSION
POS E 29871.2394mm N -10580mm U 95.0528mm
ORI Y IS N AND Z IS U
HEIG 19.52288mm

NEW LOOP
NEW VERTEX
POS E 20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N 23.952023mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N -11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N -23.952023mm U 0mm
END
NEW VERTEX
POS E 20.74306mm N -11.976011mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: sole plate on the baseplate
NEW BOX
XLEN 141.6
YLEN 431.8
ZLEN 45.1
POS E 30261.6 N -10580.0 U 72.5

-- UNCONFIRMED: motor foot: pedestal web
NEW BOX
XLEN 71.4
YLEN 217.8
ZLEN 103.9
POS E 30261.6 N -10580.0 U 147.0

-- UNCONFIRMED: motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 30224.6505mm N -10673.86mm U 95.0528mm
ORI Y IS U AND Z IS S
HEIG 37.544mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 73.899mm N 0mm U 0mm
END
NEW VERTEX
POS E 40.64445mm N 91.438336mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 30224.6505mm N -10448.596mm U 95.0528mm
ORI Y IS U AND Z IS S
HEIG 37.544mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 73.899mm N 0mm U 0mm
END
NEW VERTEX
POS E 40.64445mm N 91.438336mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.4
HEIG 69.5
ORI Z IS U AND Y IS N
POS E 30217.3 N -10580.0 U 72.5

-- UNCONFIRMED: motor foot: hold-down hex nut
NEW EXTRUSION
POS E 30217.2606mm N -10580mm U 95.0528mm
ORI Y IS N AND Z IS U
HEIG 19.52288mm

NEW LOOP
NEW VERTEX
POS E 20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N 23.952023mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N -11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N -23.952023mm U 0mm
END
NEW VERTEX
POS E 20.74306mm N -11.976011mm U 0mm
END
END
END

-- UNCONFIRMED: motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.4
HEIG 69.5
ORI Z IS U AND Y IS N
POS E 30305.9 N -10580.0 U 72.5

-- UNCONFIRMED: motor foot: hold-down hex nut
NEW EXTRUSION
POS E 30305.9394mm N -10580mm U 95.0528mm
ORI Y IS N AND Z IS U
HEIG 19.52288mm

NEW LOOP
NEW VERTEX
POS E 20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N 23.952023mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N 11.976011mm U 0mm
END
NEW VERTEX
POS E -20.74306mm N -11.976011mm U 0mm
END
NEW VERTEX
POS E 0mm N -23.952023mm U 0mm
END
NEW VERTEX
POS E 20.74306mm N -11.976011mm U 0mm
END
END
END

-- UNCONFIRMED: casing foot: sole plate on the baseplate
NEW BOX
XLEN 297.6
YLEN 249.3
ZLEN 26.0
POS E 30975.8 N -10580.0 U 63.0

-- UNCONFIRMED: casing foot: pedestal web
NEW BOX
XLEN 150.1
YLEN 125.7
ZLEN 133.0
POS E 30975.8 N -10580.0 U 142.5

-- UNCONFIRMED: casing foot: triangular stiffener gusset
NEW EXTRUSION
POS E 30898.125mm N -10634.188mm U 76.01024mm
ORI Y IS U AND Z IS S
HEIG 21.6752mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 155.25mm N 0mm U 0mm
END
NEW VERTEX
POS E 85.3875mm N 117.023949mm U 0mm
END
END
END

-- UNCONFIRMED: casing foot: triangular stiffener gusset
NEW EXTRUSION
POS E 30898.125mm N -10504.1368mm U 76.01024mm
ORI Y IS U AND Z IS S
HEIG 21.6752mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 155.25mm N 0mm U 0mm
END
NEW VERTEX
POS E 85.3875mm N 117.023949mm U 0mm
END
END
END

-- UNCONFIRMED: casing foot: hold-down bolt shank
NEW CYLI
DIAM 14.1
HEIG 40.1
ORI Z IS U AND Y IS N
POS E 30882.6 N -10580.0 U 63.0

-- UNCONFIRMED: casing foot: hold-down hex nut
NEW EXTRUSION
POS E 30882.6mm N -10580mm U 76.01024mm
ORI Y IS N AND Z IS U
HEIG 11.271104mm

NEW LOOP
NEW VERTEX
POS E 11.975548mm N 6.914086mm U 0mm
END
NEW VERTEX
POS E 0mm N 13.828172mm U 0mm
END
NEW VERTEX
POS E -11.975548mm N 6.914086mm U 0mm
END
NEW VERTEX
POS E -11.975548mm N -6.914086mm U 0mm
END
NEW VERTEX
POS E 0mm N -13.828172mm U 0mm
END
NEW VERTEX
POS E 11.975548mm N -6.914086mm U 0mm
END
END
END

-- UNCONFIRMED: casing foot: hold-down bolt shank
NEW CYLI
DIAM 14.1
HEIG 40.1
ORI Z IS U AND Y IS N
POS E 31068.9 N -10580.0 U 63.0

-- UNCONFIRMED: casing foot: hold-down hex nut
NEW EXTRUSION
POS E 31068.9mm N -10580mm U 76.01024mm
ORI Y IS N AND Z IS U
HEIG 11.271104mm

NEW LOOP
NEW VERTEX
POS E 11.975548mm N 6.914086mm U 0mm
END
NEW VERTEX
POS E 0mm N 13.828172mm U 0mm
END
NEW VERTEX
POS E -11.975548mm N 6.914086mm U 0mm
END
NEW VERTEX
POS E -11.975548mm N -6.914086mm U 0mm
END
NEW VERTEX
POS E 0mm N -13.828172mm U 0mm
END
NEW VERTEX
POS E 11.975548mm N -6.914086mm U 0mm
END
END
END

NEW SUBE /205_PU_004_CASING
-- 2 part(s), 0 nozzle(s)
-- UNCONFIRMED: volute barrel (metadata-proportioned)
NEW CYLI
DIAM 349.6
HEIG 517.5
ORI Z IS E AND Y IS U
POS E 30975.8 N -10580.0 U 376.8

-- UNCONFIRMED: suction cover (metadata-proportioned)
NEW CONE
DTOP 216.8
DBOT 349.6
HEIG 165.6
ORI Z IS E AND Y IS U
POS E 31317.3 N -10580.0 U 376.8

NEW SUBE /205_PU_004_COUPLING
-- 2 part(s), 0 nozzle(s)
-- UNCONFIRMED: coupling (metadata-proportioned)
NEW CYLI
DIAM 142.3
HEIG 207.0
ORI Z IS E AND Y IS U
POS E 30837.8 N -10580.0 U 376.8

-- UNCONFIRMED: coupling guard (metadata-proportioned)
NEW BOX
XLEN 207.0
YLEN 181.8
ZLEN 181.8
POS E 30837.8 N -10580.0 U 376.8

NEW SUBE /205_PU_004_DRIVER
-- 1 part(s), 0 nozzle(s)
-- UNCONFIRMED: motor barrel (metadata-proportioned)
NEW CYLI
DIAM 395.2
HEIG 724.5
ORI Z IS E AND Y IS U
POS E 30044.2 N -10580.0 U 376.8

NEW SUBE /205_PU_004_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction E
NEW NOZZLE /205_PU_004_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 31341.5 N -10580.0 U 376.8
ORI P1 IS E
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_004_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_004_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 30441.0 N -10580.0 U 676.8
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-012
-- --------------------------------------------------------------------
-- 205-PU-012 - D0 STAGE DILUTION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-012
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 619 mm snapped to catalogue DN600 (nearest available in 'AAZFBB033'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_012
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_012_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 1245.0
YLEN 2701.0
ZLEN 50.0
POS E 33065.0 N 13825.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 37.4
HEIG 56.0
ORI Z IS U AND Y IS N
POS E 32517.2 N 12564.5 U 78.0

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 32517.2mm N 12564.5mm U 106.025mm
ORI Y IS N AND Z IS U
HEIG 29.88mm

NEW LOOP
NEW VERTEX
POS E 31.7475mm N 18.329428mm U 0mm
END
NEW VERTEX
POS E 0mm N 36.658855mm U 0mm
END
NEW VERTEX
POS E -31.7475mm N 18.329428mm U 0mm
END
NEW VERTEX
POS E -31.7475mm N -18.329428mm U 0mm
END
NEW VERTEX
POS E 0mm N -36.658855mm U 0mm
END
NEW VERTEX
POS E 31.7475mm N -18.329428mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 37.4
HEIG 56.0
ORI Z IS U AND Y IS N
POS E 32517.2 N 15085.5 U 78.0

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 32517.2mm N 15085.5mm U 106.025mm
ORI Y IS N AND Z IS U
HEIG 29.88mm

NEW LOOP
NEW VERTEX
POS E 31.7475mm N 18.329428mm U 0mm
END
NEW VERTEX
POS E 0mm N 36.658855mm U 0mm
END
NEW VERTEX
POS E -31.7475mm N 18.329428mm U 0mm
END
NEW VERTEX
POS E -31.7475mm N -18.329428mm U 0mm
END
NEW VERTEX
POS E 0mm N -36.658855mm U 0mm
END
NEW VERTEX
POS E 31.7475mm N -18.329428mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 37.4
HEIG 56.0
ORI Z IS U AND Y IS N
POS E 33612.8 N 12564.5 U 78.0

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 33612.8mm N 12564.5mm U 106.025mm
ORI Y IS N AND Z IS U
HEIG 29.88mm

NEW LOOP
NEW VERTEX
POS E 31.7475mm N 18.329428mm U 0mm
END
NEW VERTEX
POS E 0mm N 36.658855mm U 0mm
END
NEW VERTEX
POS E -31.7475mm N 18.329428mm U 0mm
END
NEW VERTEX
POS E -31.7475mm N -18.329428mm U 0mm
END
NEW VERTEX
POS E 0mm N -36.658855mm U 0mm
END
NEW VERTEX
POS E 31.7475mm N -18.329428mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 37.4
HEIG 56.0
ORI Z IS U AND Y IS N
POS E 33612.8 N 15085.5 U 78.0

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 33612.8mm N 15085.5mm U 106.025mm
ORI Y IS N AND Z IS U
HEIG 29.88mm

NEW LOOP
NEW VERTEX
POS E 31.7475mm N 18.329428mm U 0mm
END
NEW VERTEX
POS E 0mm N 36.658855mm U 0mm
END
NEW VERTEX
POS E -31.7475mm N 18.329428mm U 0mm
END
NEW VERTEX
POS E -31.7475mm N -18.329428mm U 0mm
END
NEW VERTEX
POS E 0mm N -36.658855mm U 0mm
END
NEW VERTEX
POS E 31.7475mm N -18.329428mm U 0mm
END
END
END

NEW SUBE /205_PU_012_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 472.8
YLEN 610.0
ZLEN 49.3
POS E 33065.0 N 14083.8 U 74.7

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 238.4
YLEN 307.7
ZLEN 270.3
POS E 33065.0 N 14083.8 U 234.5

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 33167.776287mm N 13924.622648mm U 99.332618mm
ORI Y IS U AND Z IS E
HEIG 41.110515mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 318.274953mm N 0mm U 0mm
END
NEW VERTEX
POS E 175.051224mm N 237.89446mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 32921.113198mm N 13924.622648mm U 99.332618mm
ORI Y IS U AND Z IS E
HEIG 41.110515mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 318.274953mm N 0mm U 0mm
END
NEW VERTEX
POS E 175.051224mm N 237.89446mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 26.7
HEIG 76.1
ORI Z IS U AND Y IS N
POS E 33065.0 N 13892.8 U 74.7

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 33065mm N 13892.795153mm U 99.332618mm
ORI Y IS N AND Z IS U
HEIG 21.377468mm

NEW LOOP
NEW VERTEX
POS E 22.713559mm N 13.11368mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.227359mm U 0mm
END
NEW VERTEX
POS E -22.713559mm N 13.11368mm U 0mm
END
NEW VERTEX
POS E -22.713559mm N -13.11368mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.227359mm U 0mm
END
NEW VERTEX
POS E 22.713559mm N -13.11368mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 26.7
HEIG 76.1
ORI Z IS U AND Y IS N
POS E 33065.0 N 14274.7 U 74.7

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 33065mm N 14274.725096mm U 99.332618mm
ORI Y IS N AND Z IS U
HEIG 21.377468mm

NEW LOOP
NEW VERTEX
POS E 22.713559mm N 13.11368mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.227359mm U 0mm
END
NEW VERTEX
POS E -22.713559mm N 13.11368mm U 0mm
END
NEW VERTEX
POS E -22.713559mm N -13.11368mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.227359mm U 0mm
END
NEW VERTEX
POS E 22.713559mm N -13.11368mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 806.9
YLEN 221.3
ZLEN 84.2
POS E 33065.0 N 12823.9 U 92.1

-- Motor foot: pedestal web
NEW BOX
XLEN 406.9
YLEN 111.6
ZLEN 201.5
POS E 33065.0 N 12823.9 U 234.9

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 33240.404349mm N 12766.185917mm U 134.194088mm
ORI Y IS U AND Z IS E
HEIG 70.16174mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.471705mm N 0mm U 0mm
END
NEW VERTEX
POS E 63.509438mm N 177.329531mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 32819.433911mm N 12766.185917mm U 134.194088mm
ORI Y IS U AND Z IS E
HEIG 70.16174mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.471705mm N 0mm U 0mm
END
NEW VERTEX
POS E 63.509438mm N 177.329531mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 45.6
HEIG 129.8
ORI Z IS U AND Y IS N
POS E 33065.0 N 12754.6 U 92.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 33065mm N 12754.638746mm U 134.194088mm
ORI Y IS N AND Z IS U
HEIG 36.484105mm

NEW LOOP
NEW VERTEX
POS E 38.764361mm N 22.380614mm U 0mm
END
NEW VERTEX
POS E 0mm N 44.761229mm U 0mm
END
NEW VERTEX
POS E -38.764361mm N 22.380614mm U 0mm
END
NEW VERTEX
POS E -38.764361mm N -22.380614mm U 0mm
END
NEW VERTEX
POS E 0mm N -44.761229mm U 0mm
END
NEW VERTEX
POS E 38.764361mm N -22.380614mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 45.6
HEIG 129.8
ORI Z IS U AND Y IS N
POS E 33065.0 N 12893.2 U 92.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 33065mm N 12893.204793mm U 134.194088mm
ORI Y IS N AND Z IS U
HEIG 36.484105mm

NEW LOOP
NEW VERTEX
POS E 38.764361mm N 22.380614mm U 0mm
END
NEW VERTEX
POS E 0mm N 44.761229mm U 0mm
END
NEW VERTEX
POS E -38.764361mm N 22.380614mm U 0mm
END
NEW VERTEX
POS E -38.764361mm N -22.380614mm U 0mm
END
NEW VERTEX
POS E 0mm N -44.761229mm U 0mm
END
NEW VERTEX
POS E 38.764361mm N -22.380614mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 806.9
YLEN 221.3
ZLEN 84.2
POS E 33065.0 N 13548.5 U 92.1

-- Motor foot: pedestal web
NEW BOX
XLEN 406.9
YLEN 111.6
ZLEN 201.5
POS E 33065.0 N 13548.5 U 234.9

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 33240.404349mm N 13490.714265mm U 134.194088mm
ORI Y IS U AND Z IS E
HEIG 70.16174mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.471705mm N 0mm U 0mm
END
NEW VERTEX
POS E 63.509438mm N 177.329531mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 32819.433911mm N 13490.714265mm U 134.194088mm
ORI Y IS U AND Z IS E
HEIG 70.16174mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.471705mm N 0mm U 0mm
END
NEW VERTEX
POS E 63.509438mm N 177.329531mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 45.6
HEIG 129.8
ORI Z IS U AND Y IS N
POS E 33065.0 N 13479.2 U 92.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 33065mm N 13479.167094mm U 134.194088mm
ORI Y IS N AND Z IS U
HEIG 36.484105mm

NEW LOOP
NEW VERTEX
POS E 38.764361mm N 22.380614mm U 0mm
END
NEW VERTEX
POS E 0mm N 44.761229mm U 0mm
END
NEW VERTEX
POS E -38.764361mm N 22.380614mm U 0mm
END
NEW VERTEX
POS E -38.764361mm N -22.380614mm U 0mm
END
NEW VERTEX
POS E 0mm N -44.761229mm U 0mm
END
NEW VERTEX
POS E 38.764361mm N -22.380614mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 45.6
HEIG 129.8
ORI Z IS U AND Y IS N
POS E 33065.0 N 13617.7 U 92.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 33065mm N 13617.733141mm U 134.194088mm
ORI Y IS N AND Z IS U
HEIG 36.484105mm

NEW LOOP
NEW VERTEX
POS E 38.764361mm N 22.380614mm U 0mm
END
NEW VERTEX
POS E 0mm N 44.761229mm U 0mm
END
NEW VERTEX
POS E -38.764361mm N 22.380614mm U 0mm
END
NEW VERTEX
POS E -38.764361mm N -22.380614mm U 0mm
END
NEW VERTEX
POS E 0mm N -44.761229mm U 0mm
END
NEW VERTEX
POS E 38.764361mm N -22.380614mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 392.1
YLEN 145.7
ZLEN 40.9
POS E 32868.2 N 15005.6 U 70.5

-- Casing support: pedestal web
NEW BOX
XLEN 197.7
YLEN 73.5
ZLEN 313.2
POS E 32868.2 N 15005.6 U 247.5

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 32953.469969mm N 14967.587657mm U 90.910693mm
ORI Y IS U AND Z IS E
HEIG 34.092244mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 76.010818mm N 0mm U 0mm
END
NEW VERTEX
POS E 41.80595mm N 275.615433mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 32748.916507mm N 14967.587657mm U 90.910693mm
ORI Y IS U AND Z IS E
HEIG 34.092244mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 76.010818mm N 0mm U 0mm
END
NEW VERTEX
POS E 41.80595mm N 275.615433mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 22.2
HEIG 63.1
ORI Z IS U AND Y IS N
POS E 32868.2 N 14960.0 U 70.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 32868.23936mm N 14959.986576mm U 90.910693mm
ORI Y IS N AND Z IS U
HEIG 17.727967mm

NEW LOOP
NEW VERTEX
POS E 18.835965mm N 10.874949mm U 0mm
END
NEW VERTEX
POS E 0mm N 21.749899mm U 0mm
END
NEW VERTEX
POS E -18.835965mm N 10.874949mm U 0mm
END
NEW VERTEX
POS E -18.835965mm N -10.874949mm U 0mm
END
NEW VERTEX
POS E 0mm N -21.749899mm U 0mm
END
NEW VERTEX
POS E 18.835965mm N -10.874949mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 22.2
HEIG 63.1
ORI Z IS U AND Y IS N
POS E 32868.2 N 15051.2 U 70.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 32868.23936mm N 15051.199558mm U 90.910693mm
ORI Y IS N AND Z IS U
HEIG 17.727967mm

NEW LOOP
NEW VERTEX
POS E 18.835965mm N 10.874949mm U 0mm
END
NEW VERTEX
POS E 0mm N 21.749899mm U 0mm
END
NEW VERTEX
POS E -18.835965mm N 10.874949mm U 0mm
END
NEW VERTEX
POS E -18.835965mm N -10.874949mm U 0mm
END
NEW VERTEX
POS E 0mm N -21.749899mm U 0mm
END
NEW VERTEX
POS E 18.835965mm N -10.874949mm U 0mm
END
END
END

NEW SUBE /205_PU_012_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 253x550 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22BE08,22BE09,22BE0A,229B52,229B43,229B44 ...
NEW CYLI
DIAM 549.9
HEIG 253.4
ORI Z IS N AND Y IS U
POS E 32868.2 N 15005.6 U 668.0

-- volute closing onto the suction cover
NEW CONE
DTOP 340.9
DBOT 549.9
HEIG 33.1
ORI Z IS N AND Y IS U
POS E 32868.2 N 15148.8 U 668.0

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 230.9
HEIG 45.6
ORI Z IS N AND Y IS U
POS E 32868.2 N 14856.1 U 668.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 131.8
ORI Z IS N AND Y IS U
POS E 33150.4 N 15005.6 U 668.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 131.8
ORI Z IS N AND Y IS U
POS E 32586.1 N 15005.6 U 668.0

NEW SUBE /205_PU_012_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 663 mm along the machine axis x 663 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22BE48,22BE49,22BE4A,22BE0B,22BE0C,22BE0D
NEW CYLI
DIAM 663.1
HEIG 663.1
ORI Z IS N AND Y IS U
POS E 33065.0 N 14083.8 U 668.0

NEW SUBE /205_PU_012_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 216 mm apart running 156 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BE0F,22BE0E
NEW CYLI
DIAM 215.6
HEIG 215.6
ORI Z IS N AND Y IS U
POS E 33067.7 N 14493.5 U 668.0

-- Coupling hub (d=377) on the shaft centreline
NEW CYLI
DIAM 377.4
HEIG 47.4
ORI Z IS N AND Y IS U
POS E 33067.7 N 14409.4 U 668.0

-- Coupling hub (d=377) on the shaft centreline
NEW CYLI
DIAM 377.4
HEIG 47.4
ORI Z IS N AND Y IS U
POS E 33067.7 N 14577.6 U 668.0

NEW SUBE /205_PU_012_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 1132 mm along the machine axis x 739 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BE42,22BE43,22BE44,22BE45,22BE46,22BE47 ...
NEW CYLI
DIAM 738.5
HEIG 1132.1
ORI Z IS N AND Y IS U
POS E 33065.0 N 13186.2 U 668.0

-- Motor end bell
NEW CYLI
DIAM 797.6
HEIG 67.9
ORI Z IS N AND Y IS U
POS E 33065.0 N 12654.1 U 668.0

-- Motor end bell
NEW CYLI
DIAM 797.6
HEIG 67.9
ORI Z IS N AND Y IS U
POS E 33065.0 N 13718.3 U 668.0

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 32687.7 N 13186.2 U 668.0

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 32716.4 N 13186.2 U 812.4

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 32798.2 N 13186.2 U 934.8

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 32920.6 N 13186.2 U 1016.6

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 33065.0 N 13186.2 U 1045.3

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 33209.4 N 13186.2 U 1016.6

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 33331.8 N 13186.2 U 934.8

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 33413.6 N 13186.2 U 812.4

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 33442.3 N 13186.2 U 668.0

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 33413.6 N 13186.2 U 523.7

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 33331.8 N 13186.2 U 401.3

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 33209.4 N 13186.2 U 319.5

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 33065.0 N 13186.2 U 290.8

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 32920.6 N 13186.2 U 319.5

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 32798.2 N 13186.2 U 401.3

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 815.1
ORI Z IS N AND Y IS U
POS E 32716.4 N 13186.2 U 523.7

-- Motor terminal box
NEW BOX
XLEN 295.4
YLEN 339.6
ZLEN 162.5
POS E 33065.0 N 13186.2 U 1118.6

-- Motor cable gland
NEW CYLI
DIAM 55.2
HEIG 162.5
ORI Z IS E AND Y IS U
POS E 32836.1 N 13186.2 U 1118.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 51.7
YLEN 88.6
ZLEN 73.9
POS E 33065.0 N 12869.2 U 1126.7

-- Reference Value: motor nameplate
NEW BOX
XLEN 96.0
YLEN 203.8
ZLEN 6.0
POS E 33436.3 N 13322.0 U 668.0

-- Motor fan cowl disc
NEW CYLI
DIAM 812.4
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 33065.0 N 12616.1 U 668.0

-- Motor fan grille bar
NEW BOX
XLEN 373.7
YLEN 9.6
ZLEN 6.4
POS E 33251.9 N 12616.1 U 668.0

-- Motor fan grille bar
NEW BOX
XLEN 373.7
YLEN 9.6
ZLEN 6.4
POS E 32878.1 N 12616.1 U 668.0

NEW SUBE /205_PU_012_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: small fitting 70x38
-- CAD handles: 22BE53,22BE54
NEW BOX
XLEN 70.1
YLEN 37.7
ZLEN 60.0
POS E 33652.6 N 15156.5 U 80.0

NEW SUBE /205_PU_012_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN600; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_012_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB033
POS E 33065.0 N 15192.6 U 668.0
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_012_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_012_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 32868.2 N 15005.6 U 1093.0
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-013
-- --------------------------------------------------------------------
-- 205-PU-013 - D0 WASHER WIRE WASH PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-013
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_013
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_013_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 31566.0 N 14294.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 31231.6 N 13524.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 31231.6mm N 13524mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 31231.6 N 15064.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 31231.6mm N 15064mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 31900.4 N 13524.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 31900.4mm N 13524mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 31900.4 N 15064.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 31900.4mm N 15064mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /205_PU_013_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 269.1
YLEN 376.9
ZLEN 28.1
POS E 31590.3 N 14415.3 U 64.0

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 135.7
YLEN 190.1
ZLEN 115.2
POS E 31590.3 N 14415.3 U 135.7

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 31648.749315mm N 14316.964986mm U 78.075466mm
ORI Y IS U AND Z IS E
HEIG 23.396221mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.657643mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161704mm N 101.387379mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 31508.371987mm N 14316.964986mm U 78.075466mm
ORI Y IS U AND Z IS E
HEIG 23.396221mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.657643mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161704mm N 101.387379mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 15.2
HEIG 43.3
ORI Z IS U AND Y IS N
POS E 31590.3 N 14297.3 U 64.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 31590.258762mm N 14297.299222mm U 78.075466mm
ORI Y IS N AND Z IS U
HEIG 12.166035mm

NEW LOOP
NEW VERTEX
POS E 12.926412mm N 7.463068mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.926135mm U 0mm
END
NEW VERTEX
POS E -12.926412mm N 7.463068mm U 0mm
END
NEW VERTEX
POS E -12.926412mm N -7.463068mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.926135mm U 0mm
END
NEW VERTEX
POS E 12.926412mm N -7.463068mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 15.2
HEIG 43.3
ORI Z IS U AND Y IS N
POS E 31590.3 N 14533.3 U 64.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 31590.258762mm N 14533.288394mm U 78.075466mm
ORI Y IS N AND Z IS U
HEIG 12.166035mm

NEW LOOP
NEW VERTEX
POS E 12.926412mm N 7.463068mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.926135mm U 0mm
END
NEW VERTEX
POS E -12.926412mm N 7.463068mm U 0mm
END
NEW VERTEX
POS E -12.926412mm N -7.463068mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.926135mm U 0mm
END
NEW VERTEX
POS E 12.926412mm N -7.463068mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 518.3
YLEN 132.8
ZLEN 54.1
POS E 31590.3 N 13664.2 U 77.0

-- Motor foot: pedestal web
NEW BOX
XLEN 261.4
YLEN 67.0
ZLEN 45.5
POS E 31590.3 N 13664.2 U 126.9

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 31702.927207mm N 13629.601036mm U 104.080854mm
ORI Y IS U AND Z IS E
HEIG 45.067378mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 40.076759mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 31432.522938mm N 13629.601036mm U 104.080854mm
ORI Y IS U AND Z IS E
HEIG 45.067378mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 40.076759mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 29.3
HEIG 83.4
ORI Z IS U AND Y IS N
POS E 31590.3 N 13622.7 U 77.0

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 31590.258762mm N 13622.672734mm U 104.080854mm
ORI Y IS N AND Z IS U
HEIG 23.435037mm

NEW LOOP
NEW VERTEX
POS E 24.899726mm N 14.375864mm U 0mm
END
NEW VERTEX
POS E 0mm N 28.751728mm U 0mm
END
NEW VERTEX
POS E -24.899726mm N 14.375864mm U 0mm
END
NEW VERTEX
POS E -24.899726mm N -14.375864mm U 0mm
END
NEW VERTEX
POS E 0mm N -28.751728mm U 0mm
END
NEW VERTEX
POS E 24.899726mm N -14.375864mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 29.3
HEIG 83.4
ORI Z IS U AND Y IS N
POS E 31590.3 N 13705.8 U 77.0

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 31590.258762mm N 13705.812362mm U 104.080854mm
ORI Y IS N AND Z IS U
HEIG 23.435037mm

NEW LOOP
NEW VERTEX
POS E 24.899726mm N 14.375864mm U 0mm
END
NEW VERTEX
POS E 0mm N 28.751728mm U 0mm
END
NEW VERTEX
POS E -24.899726mm N 14.375864mm U 0mm
END
NEW VERTEX
POS E -24.899726mm N -14.375864mm U 0mm
END
NEW VERTEX
POS E 0mm N -28.751728mm U 0mm
END
NEW VERTEX
POS E 24.899726mm N -14.375864mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 518.3
YLEN 132.8
ZLEN 54.1
POS E 31590.3 N 14099.0 U 77.0

-- Motor foot: pedestal web
NEW BOX
XLEN 261.4
YLEN 67.0
ZLEN 45.5
POS E 31590.3 N 14099.0 U 126.9

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 31702.927207mm N 14064.318045mm U 104.080854mm
ORI Y IS U AND Z IS E
HEIG 45.067378mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 40.076759mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 31432.522938mm N 14064.318045mm U 104.080854mm
ORI Y IS U AND Z IS E
HEIG 45.067378mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 40.076759mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 29.3
HEIG 83.4
ORI Z IS U AND Y IS N
POS E 31590.3 N 14057.4 U 77.0

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 31590.258762mm N 14057.389742mm U 104.080854mm
ORI Y IS N AND Z IS U
HEIG 23.435037mm

NEW LOOP
NEW VERTEX
POS E 24.899726mm N 14.375864mm U 0mm
END
NEW VERTEX
POS E 0mm N 28.751728mm U 0mm
END
NEW VERTEX
POS E -24.899726mm N 14.375864mm U 0mm
END
NEW VERTEX
POS E -24.899726mm N -14.375864mm U 0mm
END
NEW VERTEX
POS E 0mm N -28.751728mm U 0mm
END
NEW VERTEX
POS E 24.899726mm N -14.375864mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 29.3
HEIG 83.4
ORI Z IS U AND Y IS N
POS E 31590.3 N 14140.5 U 77.0

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 31590.258762mm N 14140.52937mm U 104.080854mm
ORI Y IS N AND Z IS U
HEIG 23.435037mm

NEW LOOP
NEW VERTEX
POS E 24.899726mm N 14.375864mm U 0mm
END
NEW VERTEX
POS E 0mm N 28.751728mm U 0mm
END
NEW VERTEX
POS E -24.899726mm N 14.375864mm U 0mm
END
NEW VERTEX
POS E -24.899726mm N -14.375864mm U 0mm
END
NEW VERTEX
POS E 0mm N -28.751728mm U 0mm
END
NEW VERTEX
POS E 24.899726mm N -14.375864mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 230.6
YLEN 161.2
ZLEN 24.1
POS E 31590.3 N 14970.5 U 62.0

-- Casing support: pedestal web
NEW BOX
XLEN 116.3
YLEN 81.3
ZLEN 133.8
POS E 31590.3 N 14970.5 U 141.0

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 31640.393536mm N 14928.501353mm U 74.064692mm
ORI Y IS U AND Z IS E
HEIG 20.05391mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 84.097056mm N 0mm U 0mm
END
NEW VERTEX
POS E 46.253381mm N 117.725444mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 31520.070078mm N 14928.501353mm U 74.064692mm
ORI Y IS U AND Z IS E
HEIG 20.05391mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 84.097056mm N 0mm U 0mm
END
NEW VERTEX
POS E 46.253381mm N 117.725444mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 13.0
HEIG 37.1
ORI Z IS U AND Y IS N
POS E 31590.3 N 14920.1 U 62.0

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 31590.258762mm N 14920.091648mm U 74.064692mm
ORI Y IS N AND Z IS U
HEIG 10.428033mm

NEW LOOP
NEW VERTEX
POS E 11.079785mm N 6.396917mm U 0mm
END
NEW VERTEX
POS E 0mm N 12.793834mm U 0mm
END
NEW VERTEX
POS E -11.079785mm N 6.396917mm U 0mm
END
NEW VERTEX
POS E -11.079785mm N -6.396917mm U 0mm
END
NEW VERTEX
POS E 0mm N -12.793834mm U 0mm
END
NEW VERTEX
POS E 11.079785mm N -6.396917mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 13.0
HEIG 37.1
ORI Z IS U AND Y IS N
POS E 31590.3 N 15021.0 U 62.0

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 31590.258762mm N 15021.008115mm U 74.064692mm
ORI Y IS N AND Z IS U
HEIG 10.428033mm

NEW LOOP
NEW VERTEX
POS E 11.079785mm N 6.396917mm U 0mm
END
NEW VERTEX
POS E 0mm N 12.793834mm U 0mm
END
NEW VERTEX
POS E -11.079785mm N 6.396917mm U 0mm
END
NEW VERTEX
POS E -11.079785mm N -6.396917mm U 0mm
END
NEW VERTEX
POS E 0mm N -12.793834mm U 0mm
END
NEW VERTEX
POS E 11.079785mm N -6.396917mm U 0mm
END
END
END

NEW SUBE /205_PU_013_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 280x323 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22F13C,22F13A,22F13B,22BDF7,22BDF6,22F130 ...
NEW CYLI
DIAM 323.5
HEIG 280.3
ORI Z IS N AND Y IS U
POS E 31590.3 N 14970.5 U 363.1

-- volute closing onto the suction cover
NEW CONE
DTOP 200.5
DBOT 323.5
HEIG 33.1
ORI Z IS N AND Y IS U
POS E 31590.3 N 15127.3 U 363.1

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 135.8
HEIG 50.5
ORI Z IS N AND Y IS U
POS E 31590.3 N 14805.2 U 363.1

-- Reference Value: axial casing rib
NEW CYLI
DIAM 14.6
HEIG 145.8
ORI Z IS N AND Y IS U
POS E 31757.8 N 14970.5 U 363.1

-- Reference Value: axial casing rib
NEW CYLI
DIAM 14.6
HEIG 145.8
ORI Z IS N AND Y IS U
POS E 31422.7 N 14970.5 U 363.1

NEW SUBE /205_PU_013_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 410 mm along the machine axis x 377 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22F10D,22F10E,22BDD4,22BDD3,22F133,22F134 ...
NEW CYLI
DIAM 377.4
HEIG 409.7
ORI Z IS N AND Y IS U
POS E 31590.3 N 14415.3 U 363.1

NEW SUBE /205_PU_013_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 86 mm apart running 210 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22F132,22BDF8
NEW CYLI
DIAM 86.3
HEIG 210.2
ORI Z IS N AND Y IS U
POS E 31590.3 N 14725.3 U 363.1

-- Coupling hub (d=151) on the shaft centreline
NEW CYLI
DIAM 150.9
HEIG 46.3
ORI Z IS N AND Y IS U
POS E 31590.3 N 14643.3 U 363.1

-- Coupling hub (d=151) on the shaft centreline
NEW CYLI
DIAM 150.9
HEIG 46.3
ORI Z IS N AND Y IS U
POS E 31590.3 N 14807.3 U 363.1

NEW SUBE /205_PU_013_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 679 mm along the machine axis x 474 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BDD8,22BDD7,22F111,22F112,22F10F,22F110 ...
NEW CYLI
DIAM 474.4
HEIG 679.2
ORI Z IS N AND Y IS U
POS E 31590.3 N 13881.6 U 363.1

-- Motor end bell
NEW CYLI
DIAM 512.3
HEIG 40.8
ORI Z IS N AND Y IS U
POS E 31590.3 N 13562.4 U 363.1

-- Motor end bell
NEW CYLI
DIAM 512.3
HEIG 40.8
ORI Z IS N AND Y IS U
POS E 31590.3 N 14200.8 U 363.1

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31346.4 N 13881.6 U 363.1

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31365.0 N 13881.6 U 456.4

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31417.8 N 13881.6 U 535.5

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31496.9 N 13881.6 U 588.4

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31590.3 N 13881.6 U 606.9

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31683.6 N 13881.6 U 588.4

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31762.7 N 13881.6 U 535.5

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31815.5 N 13881.6 U 456.4

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31834.1 N 13881.6 U 363.1

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31815.5 N 13881.6 U 269.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31762.7 N 13881.6 U 190.7

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31683.6 N 13881.6 U 137.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31590.3 N 13881.6 U 119.3

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31496.9 N 13881.6 U 137.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31417.8 N 13881.6 U 190.7

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 13.3
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 31365.0 N 13881.6 U 269.8

-- Motor terminal box
NEW BOX
XLEN 189.8
YLEN 203.8
ZLEN 104.4
POS E 31590.3 N 13881.6 U 652.5

-- Motor cable gland
NEW CYLI
DIAM 35.5
HEIG 104.4
ORI Z IS E AND Y IS U
POS E 31443.2 N 13881.6 U 652.5

-- Reference Value: motor lifting lug
NEW BOX
XLEN 33.2
YLEN 56.9
ZLEN 47.4
POS E 31590.3 N 13691.4 U 657.7

-- Reference Value: motor nameplate
NEW BOX
XLEN 61.7
YLEN 122.3
ZLEN 6.0
POS E 31829.5 N 13963.1 U 363.1

-- Motor fan cowl disc
NEW CYLI
DIAM 521.8
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 31590.3 N 13538.0 U 363.1

-- Motor fan grille bar
NEW BOX
XLEN 240.0
YLEN 9.6
ZLEN 6.4
POS E 31710.3 N 13538.0 U 363.1

-- Motor fan grille bar
NEW BOX
XLEN 240.0
YLEN 9.6
ZLEN 6.4
POS E 31470.2 N 13538.0 U 363.1

NEW SUBE /205_PU_013_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 22x173 at the wet end, outboard of the casing
-- CAD handles: 22F12D,22BDF3,22BDF2,22BDF1,22F12B,22F12C
NEW BOX
XLEN 172.5
YLEN 21.6
ZLEN 60.0
POS E 31590.3 N 15121.5 U 80.0

NEW SUBE /205_PU_013_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN65; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_013_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0KK
POS E 31566.0 N 15133.8 U 363.1
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_013_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_013_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 31590.3 N 14970.5 U 674.8
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-018
-- --------------------------------------------------------------------
-- 205-PU-018 - D0 STAGE MC PUMP (205-PU-018/MC PUMP)
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-018
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: W (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 140 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)
-- Note: discharge: metadata bore 161 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_018
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_018_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 2022.0
YLEN 1051.0
ZLEN 50.0
POS E 35723.0 N 5019.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 31.5
HEIG 47.3
ORI Z IS U AND Y IS N
POS E 34802.0 N 4583.5 U 73.6

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 34802mm N 4583.5mm U 97.295mm
ORI Y IS N AND Z IS U
HEIG 25.224mm

NEW LOOP
NEW VERTEX
POS E 26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.946552mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N -15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.946552mm U 0mm
END
NEW VERTEX
POS E 26.8005mm N -15.473276mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 31.5
HEIG 47.3
ORI Z IS U AND Y IS N
POS E 34802.0 N 5454.5 U 73.6

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 34802mm N 5454.5mm U 97.295mm
ORI Y IS N AND Z IS U
HEIG 25.224mm

NEW LOOP
NEW VERTEX
POS E 26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.946552mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N -15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.946552mm U 0mm
END
NEW VERTEX
POS E 26.8005mm N -15.473276mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 31.5
HEIG 47.3
ORI Z IS U AND Y IS N
POS E 36644.0 N 4583.5 U 73.6

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 36644mm N 4583.5mm U 97.295mm
ORI Y IS N AND Z IS U
HEIG 25.224mm

NEW LOOP
NEW VERTEX
POS E 26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.946552mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N -15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.946552mm U 0mm
END
NEW VERTEX
POS E 26.8005mm N -15.473276mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 31.5
HEIG 47.3
ORI Z IS U AND Y IS N
POS E 36644.0 N 5454.5 U 73.6

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 36644mm N 5454.5mm U 97.295mm
ORI Y IS N AND Z IS U
HEIG 25.224mm

NEW LOOP
NEW VERTEX
POS E 26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.946552mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N -15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.946552mm U 0mm
END
NEW VERTEX
POS E 26.8005mm N -15.473276mm U 0mm
END
END
END

NEW SUBE /205_PU_018_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 347.2
YLEN 472.8
ZLEN 49.3
POS E 35758.0 N 5019.0 U 74.7

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 175.1
YLEN 238.4
ZLEN 79.2
POS E 35758.0 N 5019.0 U 139.0

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 35848.606516mm N 5121.776287mm U 99.332618mm
ORI Y IS U AND Z IS N
HEIG 41.110515mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 181.132112mm N 0mm U 0mm
END
NEW VERTEX
POS E 99.622662mm N 69.730161mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 35848.606516mm N 4875.113198mm U 99.332618mm
ORI Y IS U AND Z IS N
HEIG 41.110515mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 181.132112mm N 0mm U 0mm
END
NEW VERTEX
POS E 99.622662mm N 69.730161mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 26.7
HEIG 76.1
ORI Z IS U AND Y IS N
POS E 35866.7 N 5019.0 U 74.7

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 35866.719727mm N 5019mm U 99.332618mm
ORI Y IS N AND Z IS U
HEIG 21.377468mm

NEW LOOP
NEW VERTEX
POS E 22.713559mm N 13.11368mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.227359mm U 0mm
END
NEW VERTEX
POS E -22.713559mm N 13.11368mm U 0mm
END
NEW VERTEX
POS E -22.713559mm N -13.11368mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.227359mm U 0mm
END
NEW VERTEX
POS E 22.713559mm N -13.11368mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 26.7
HEIG 76.1
ORI Z IS U AND Y IS N
POS E 35649.4 N 5019.0 U 74.7

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 35649.361193mm N 5019mm U 99.332618mm
ORI Y IS N AND Z IS U
HEIG 21.377468mm

NEW LOOP
NEW VERTEX
POS E 22.713559mm N 13.11368mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.227359mm U 0mm
END
NEW VERTEX
POS E -22.713559mm N 13.11368mm U 0mm
END
NEW VERTEX
POS E -22.713559mm N -13.11368mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.227359mm U 0mm
END
NEW VERTEX
POS E 22.713559mm N -13.11368mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 167.6
YLEN 706.7
ZLEN 73.7
POS E 35415.1 N 5005.5 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 84.5
YLEN 356.4
ZLEN 62.1
POS E 35415.1 N 5005.5 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 35458.789741mm N 5159.16184mm U 123.746635mm
ORI Y IS U AND Z IS N
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 87.428577mm N 0mm U 0mm
END
NEW VERTEX
POS E 48.085717mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 35458.789741mm N 4790.428663mm U 123.746635mm
ORI Y IS U AND Z IS N
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 87.428577mm N 0mm U 0mm
END
NEW VERTEX
POS E 48.085717mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 35467.5 N 5005.5 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 35467.532598mm N 5005.523016mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 35362.6 N 5005.5 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 35362.618306mm N 5005.523016mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 167.6
YLEN 706.7
ZLEN 73.7
POS E 34866.5 N 5005.5 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 84.5
YLEN 356.4
ZLEN 62.1
POS E 34866.5 N 5005.5 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 34910.218277mm N 5159.16184mm U 123.746635mm
ORI Y IS U AND Z IS N
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 87.428577mm N 0mm U 0mm
END
NEW VERTEX
POS E 48.085717mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 34910.218277mm N 4790.428663mm U 123.746635mm
ORI Y IS U AND Z IS N
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 87.428577mm N 0mm U 0mm
END
NEW VERTEX
POS E 48.085717mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 34919.0 N 5005.5 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 34918.961135mm N 5005.523016mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 34814.0 N 5005.5 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 34814.046843mm N 5005.523016mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 415.4
YLEN 372.8
ZLEN 38.9
POS E 36275.6 N 5019.0 U 69.5

-- Casing support: pedestal web
NEW BOX
XLEN 209.5
YLEN 188.0
ZLEN 137.1
POS E 36275.6 N 5019.0 U 157.4

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 36383.916502mm N 5100.051306mm U 88.904589mm
ORI Y IS U AND Z IS N
HEIG 32.420491mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 216.711588mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.191373mm N 120.605998mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 36383.916502mm N 4905.528363mm U 88.904589mm
ORI Y IS U AND Z IS N
HEIG 32.420491mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 216.711588mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.191373mm N 120.605998mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 21.1
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 36405.6 N 5019.0 U 69.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 36405.587661mm N 5019.00008mm U 88.904589mm
ORI Y IS N AND Z IS U
HEIG 16.858655mm

NEW LOOP
NEW VERTEX
POS E 17.912321mm N 10.341683mm U 0mm
END
NEW VERTEX
POS E 0mm N 20.683367mm U 0mm
END
NEW VERTEX
POS E -17.912321mm N 10.341683mm U 0mm
END
NEW VERTEX
POS E -17.912321mm N -10.341683mm U 0mm
END
NEW VERTEX
POS E 0mm N -20.683367mm U 0mm
END
NEW VERTEX
POS E 17.912321mm N -10.341683mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 21.1
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 36145.5 N 5019.0 U 69.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 36145.533756mm N 5019.00008mm U 88.904589mm
ORI Y IS N AND Z IS U
HEIG 16.858655mm

NEW LOOP
NEW VERTEX
POS E 17.912321mm N 10.341683mm U 0mm
END
NEW VERTEX
POS E 0mm N 20.683367mm U 0mm
END
NEW VERTEX
POS E -17.912321mm N 10.341683mm U 0mm
END
NEW VERTEX
POS E -17.912321mm N -10.341683mm U 0mm
END
NEW VERTEX
POS E 0mm N -20.683367mm U 0mm
END
NEW VERTEX
POS E 17.912321mm N -10.341683mm U 0mm
END
END
END

NEW SUBE /205_PU_018_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 722x523 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22B938,22B939,22B97C,22B972,22B973,22B920 ...
NEW CYLI
DIAM 522.9
HEIG 722.4
ORI Z IS W AND Y IS U
POS E 36275.6 N 5019.0 U 477.0

-- volute closing onto the suction cover
NEW CONE
DTOP 324.2
DBOT 522.9
HEIG 216.7
ORI Z IS W AND Y IS U
POS E 35806.0 N 5019.0 U 477.0

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 219.6
HEIG 130.0
ORI Z IS W AND Y IS U
POS E 36701.8 N 5019.0 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 375.6
ORI Z IS W AND Y IS U
POS E 36275.6 N 5287.7 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 375.6
ORI Z IS W AND Y IS U
POS E 36275.6 N 4750.3 U 477.0

NEW SUBE /205_PU_018_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 377 mm along the machine axis x 663 mm across, consolidated from 4 drawn sections (housing sections)
-- CAD handles: 22B941,22B92B,22B940,22B92F,22B926,22B923 ...
NEW CYLI
DIAM 663.1
HEIG 377.4
ORI Z IS W AND Y IS U
POS E 35758.0 N 5019.0 U 477.0

NEW SUBE /205_PU_018_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 27 mm apart running 59 mm along x, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22B8F2,22908E
NEW CYLI
DIAM 27.0
HEIG 59.3
ORI Z IS W AND Y IS U
POS E 35679.9 N 5029.8 U 477.0

-- Coupling hub (d=47) on the shaft centreline
NEW CYLI
DIAM 47.2
HEIG 13.0
ORI Z IS W AND Y IS U
POS E 35703.0 N 5029.8 U 477.0

-- Coupling hub (d=47) on the shaft centreline
NEW CYLI
DIAM 47.2
HEIG 13.0
ORI Z IS W AND Y IS U
POS E 35656.7 N 5029.8 U 477.0

NEW SUBE /205_PU_018_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: large body 857 mm along the machine axis at the driver end, spanning 647 mm across the baseplate (2 drawn feature(s) merged)
-- CAD handles: 22B986,22B987,22B988,22B985,22B8F7,22B8F8 ...
NEW CYLI
DIAM 646.9
HEIG 857.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5005.5 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 51.4
ORI Z IS W AND Y IS U
POS E 35543.6 N 5005.5 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 51.4
ORI Z IS W AND Y IS U
POS E 34737.9 N 5005.5 U 477.0

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 4674.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 4699.3 U 603.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 4771.2 U 711.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 4878.7 U 783.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5005.5 U 808.4

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5132.4 U 783.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5239.9 U 711.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5311.7 U 603.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5337.0 U 477.0

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5311.7 U 350.1

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5239.9 U 242.6

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5132.4 U 170.7

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 5005.5 U 145.5

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 4878.7 U 170.7

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 4771.2 U 242.6

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 617.1
ORI Z IS W AND Y IS U
POS E 35140.8 N 4699.3 U 350.1

-- Motor terminal box
NEW BOX
XLEN 257.1
YLEN 258.8
ZLEN 142.3
POS E 35140.8 N 5005.5 U 871.6

-- Motor cable gland
NEW CYLI
DIAM 48.4
HEIG 142.3
ORI Z IS N AND Y IS U
POS E 35140.8 N 4805.0 U 871.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 77.6
YLEN 45.3
ZLEN 64.7
POS E 35380.8 N 5005.5 U 878.7

-- Reference Value: motor nameplate
NEW BOX
XLEN 154.3
YLEN 84.1
ZLEN 6.0
POS E 35037.9 N 5331.0 U 477.0

-- Motor fan cowl disc
NEW CYLI
DIAM 711.6
HEIG 8.0
ORI Z IS W AND Y IS U
POS E 35573.4 N 5005.5 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 327.3
ZLEN 6.4
POS E 35573.4 N 5169.2 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 327.3
ZLEN 6.4
POS E 35573.4 N 4841.9 U 477.0

NEW SUBE /205_PU_018_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: small fitting 75x135
-- CAD handles: 22B930,22B931,22B932
NEW BOX
XLEN 75.5
YLEN 134.8
ZLEN 60.4
POS E 35747.3 N 5019.0 U 80.2

NEW SUBE /205_PU_018_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN150; POS is the flange face, contractual direction S
NEW NOZZLE /205_PU_018_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 35723.0 N 4517.4 U 477.0
ORI P1 IS S
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_018_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction W
NEW NOZZLE /205_PU_018_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 34736.2 N 5019.0 U 477.0
ORI P1 IS W
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-024
-- --------------------------------------------------------------------
-- 205-PU-024 - EOP REACTOR TOP SPOOLING BOOSTER PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-024
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: S (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 113 mm snapped to catalogue DN125 (nearest available in 'AAZFBB0PP'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_024
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_024_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 41518.0 N 660.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 41183.6 N -110.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 41183.6mm N -110mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 41183.6 N 1430.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 41183.6mm N 1430mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 41852.4 N -110.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 41852.4mm N -110mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 41852.4 N 1430.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 41852.4mm N 1430mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /205_PU_024_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 307.5
YLEN 376.9
ZLEN 32.1
POS E 41515.3 N 781.3 U 66.0

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 155.1
YLEN 190.1
ZLEN 122.5
POS E 41515.3 N 781.3 U 143.3

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 41448.458198mm N 879.62263mm U 82.086251mm
ORI Y IS U AND Z IS W
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.657643mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161704mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 41608.889456mm N 879.62263mm U 82.086251mm
ORI Y IS U AND Z IS W
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.657643mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161704mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 41515.3 N 899.3 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 41515.304556mm N 899.288394mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 41515.3 N 663.3 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 41515.304556mm N 663.299222mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 577.2
YLEN 132.8
ZLEN 60.2
POS E 41515.3 N 465.0 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 291.1
YLEN 67.0
ZLEN 50.7
POS E 41515.3 N 465.0 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 41389.832862mm N 499.601068mm U 110.226413mm
ORI Y IS U AND Z IS W
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 41690.964926mm N 499.601068mm U 110.226413mm
ORI Y IS U AND Z IS W
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 41515.3 N 506.5 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 41515.304556mm N 506.52937mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 41515.3 N 423.4 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 41515.304556mm N 423.389742mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 577.2
YLEN 132.8
ZLEN 60.2
POS E 41515.3 N 30.2 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 291.1
YLEN 67.0
ZLEN 50.7
POS E 41515.3 N 30.2 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 41389.832862mm N 64.884059mm U 110.226413mm
ORI Y IS U AND Z IS W
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 41690.964926mm N 64.884059mm U 110.226413mm
ORI Y IS U AND Z IS W
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 41515.3 N 71.8 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 41515.304556mm N 71.812362mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 41515.3 N -11.3 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 41515.304556mm N -11.327266mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 132.9
YLEN 66.5
ZLEN 13.9
POS E 41515.3 N 1370.9 U 56.9

-- Casing support: pedestal web
NEW BOX
XLEN 67.0
YLEN 33.5
ZLEN 245.3
POS E 41515.3 N 1370.9 U 186.5

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 41486.410148mm N 1388.253109mm U 63.869287mm
ORI Y IS U AND Z IS W
HEIG 11.557739mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.673217mm N 0mm U 0mm
END
NEW VERTEX
POS E 19.07027mm N 215.890994mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 41555.756583mm N 1388.253109mm U 63.869287mm
ORI Y IS U AND Z IS W
HEIG 11.557739mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.673217mm N 0mm U 0mm
END
NEW VERTEX
POS E 19.07027mm N 215.890994mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.9
ORI Z IS U AND Y IS N
POS E 41515.3 N 1391.7 U 56.9

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 41515.304496mm N 1391.720431mm U 63.869287mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.9
ORI Z IS U AND Y IS N
POS E 41515.3 N 1350.1 U 56.9

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 41515.304496mm N 1350.11257mm U 63.869287mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /205_PU_024_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 93; the only large round feature in the plan, at the wet end
-- CAD handles: 22BF25,22BF1E,22BF1F,22BF20,22BF21,22BF22 ...
NEW CYLI
DIAM 186.4
HEIG 115.6
ORI Z IS U AND Y IS N
POS E 41515.3 N 1370.9 U 398.7

-- casing split flange at the cover joint
NEW CYLI
DIAM 205.1
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 41515.3 N 1370.9 U 464.5

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 41515.3 N 1279.2 U 454.9

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 41515.304496mm N 1279.188169mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 41580.2 N 1306.1 U 454.9

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 41580.166221mm N 1306.054775mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 41607.0 N 1370.9 U 454.9

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 41607.032827mm N 1370.9165mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 41580.2 N 1435.8 U 454.9

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 41580.166221mm N 1435.778225mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 41515.3 N 1462.6 U 454.9

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 41515.304496mm N 1462.644831mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 41450.4 N 1435.8 U 454.9

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 41450.442771mm N 1435.778225mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 41423.6 N 1370.9 U 454.9

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 41423.576165mm N 1370.9165mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 41450.4 N 1306.1 U 454.9

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 41450.442771mm N 1306.054775mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 115.6
DBOT 186.4
HEIG 34.7
ORI Z IS S AND Y IS U
POS E 41515.3 N 1295.8 U 398.7

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 78.3
HEIG 20.8
ORI Z IS S AND Y IS U
POS E 41515.3 N 1439.1 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 60.1
ORI Z IS S AND Y IS U
POS E 41418.5 N 1370.9 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 60.1
ORI Z IS S AND Y IS U
POS E 41612.1 N 1370.9 U 398.7

NEW SUBE /205_PU_024_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 410 mm along the machine axis x 431 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22BF08,22BF09,22BF0A,22BF42,22BF43,22BF44
NEW CYLI
DIAM 431.3
HEIG 409.7
ORI Z IS S AND Y IS U
POS E 41515.3 N 781.3 U 398.7

NEW SUBE /205_PU_024_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 210 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BF0B,22BF0C
NEW CYLI
DIAM 134.8
HEIG 210.2
ORI Z IS S AND Y IS U
POS E 41518.0 N 1091.3 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS S AND Y IS U
POS E 41518.0 N 1173.3 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS S AND Y IS U
POS E 41518.0 N 1009.3 U 398.7

NEW SUBE /205_PU_024_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 679 mm along the machine axis x 528 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BF49,22BF4A,22BF4B,22BF4C,22BF4D,22BF4E ...
NEW CYLI
DIAM 528.3
HEIG 679.2
ORI Z IS S AND Y IS U
POS E 41515.3 N 247.6 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS S AND Y IS U
POS E 41515.3 N 566.8 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS S AND Y IS U
POS E 41515.3 N -71.6 U 398.7

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41786.9 N 247.6 U 398.7

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41766.2 N 247.6 U 502.6

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41707.3 N 247.6 U 590.7

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41619.2 N 247.6 U 649.6

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41515.3 N 247.6 U 670.2

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41411.4 N 247.6 U 649.6

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41323.3 N 247.6 U 590.7

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41264.4 N 247.6 U 502.6

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41243.8 N 247.6 U 398.7

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41264.4 N 247.6 U 294.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41323.3 N 247.6 U 206.7

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41411.4 N 247.6 U 147.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41515.3 N 247.6 U 127.1

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41619.2 N 247.6 U 147.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41707.3 N 247.6 U 206.7

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS S AND Y IS U
POS E 41766.2 N 247.6 U 294.8

-- Motor terminal box
NEW BOX
XLEN 211.3
YLEN 203.8
ZLEN 116.2
POS E 41515.3 N 247.6 U 720.9

-- Motor cable gland
NEW CYLI
DIAM 39.5
HEIG 116.2
ORI Z IS E AND Y IS U
POS E 41679.1 N 247.6 U 720.9

-- Reference Value: motor lifting lug
NEW BOX
XLEN 37.0
YLEN 63.4
ZLEN 52.8
POS E 41515.3 N 437.8 U 726.8

-- Reference Value: motor nameplate
NEW BOX
XLEN 68.7
YLEN 122.3
ZLEN 6.0
POS E 41249.2 N 166.1 U 398.7

-- Motor fan cowl disc
NEW CYLI
DIAM 581.1
HEIG 8.0
ORI Z IS S AND Y IS U
POS E 41515.3 N 591.2 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 267.3
YLEN 9.6
ZLEN 6.4
POS E 41381.6 N 591.2 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 267.3
YLEN 9.6
ZLEN 6.4
POS E 41649.0 N 591.2 U 398.7

NEW SUBE /205_PU_024_AUXILIARY
-- 2 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 22x221 at the wet end, outboard of the casing
-- CAD handles: 22BF19,22BF16,22BF17,22BF18
NEW BOX
XLEN 221.0
YLEN 21.6
ZLEN 60.0
POS E 41518.0 N 1487.5 U 80.0

-- Auxiliary [LOW]: body 259x361 at the wet end, outboard of the casing
-- CAD handles: 22BF11,22A19D,22BF10,22A19C,22BF0D,22BF0E ...
NEW BOX
XLEN 361.2
YLEN 258.8
ZLEN 207.0
POS E 41528.8 N 1325.8 U 153.5

NEW SUBE /205_PU_024_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN125; POS is the flange face, contractual direction S
NEW NOZZLE /205_PU_024_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0PP
POS E 41518.0 N -179.8 U 398.7
ORI P1 IS S
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_024_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_024_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 41515.3 N 1370.9 U 606.5
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-027
-- --------------------------------------------------------------------
-- 205-PU-027 - EOP WASHER FEED PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-027
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 216 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 151 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_027
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_027_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 857.0
YLEN 2135.0
ZLEN 50.0
POS E 42218.0 N -8620.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 41840.9 N -9597.5 U 69.3

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 41840.92mm N -9597.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 41840.9 N -7642.5 U 69.3

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 41840.92mm N -7642.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 42595.1 N -9597.5 U 69.3

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 42595.08mm N -9597.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 42595.1 N -7642.5 U 69.3

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 42595.08mm N -7642.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

NEW SUBE /205_PU_027_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 187.6
ZLEN 73.7
POS E 42220.7 N -9512.0 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.6
ZLEN 62.1
POS E 42220.7 N -9512.0 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 42374.334189mm N -9560.905766mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.876022mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.831812mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 42005.601012mm N -9560.905766mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.876022mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.831812mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 42220.7 N -9570.7 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 42220.695365mm N -9570.693368mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 42220.7 N -9453.2 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 42220.695365mm N -9453.242141mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 187.6
ZLEN 73.7
POS E 42220.7 N -8897.8 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.6
ZLEN 62.1
POS E 42220.7 N -8897.8 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 42374.334189mm N -8946.781704mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.876022mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.831812mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 42005.601012mm N -8946.781704mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.876022mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.831812mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 42220.7 N -8956.6 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 42220.695365mm N -8956.569306mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 42220.7 N -8839.1 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 42220.695365mm N -8839.118079mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 157.6
YLEN 396.8
ZLEN 16.4
POS E 42218.0 N -8509.5 U 58.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 79.5
YLEN 200.1
ZLEN 311.0
POS E 42218.0 N -8509.5 U 222.0

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 42252.258779mm N -8612.991927mm U 66.444214mm
ORI Y IS U AND Z IS E
HEIG 13.703511mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 207.008074mm N 0mm U 0mm
END
NEW VERTEX
POS E 113.854441mm N 273.723138mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 42170.03771mm N -8612.991927mm U 66.444214mm
ORI Y IS U AND Z IS E
HEIG 13.703511mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 207.008074mm N 0mm U 0mm
END
NEW VERTEX
POS E 113.854441mm N 273.723138mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 42218.0 N -8633.7 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 42218mm N -8633.692734mm U 66.444214mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 42218.0 N -8385.3 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 42218mm N -8385.283046mm U 66.444214mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 311.3
YLEN 120.9
ZLEN 32.5
POS E 42358.2 N -7768.2 U 66.2

-- Casing support: pedestal web
NEW BOX
XLEN 157.0
YLEN 61.0
ZLEN 184.9
POS E 42358.2 N -7768.2 U 174.9

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 42425.843626mm N -7799.784368mm U 82.487334mm
ORI Y IS U AND Z IS E
HEIG 27.072778mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 63.07278mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.690029mm N 162.68663mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 42263.406958mm N -7799.784368mm U 82.487334mm
ORI Y IS U AND Z IS E
HEIG 27.072778mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 63.07278mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.690029mm N 162.68663mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 17.6
HEIG 50.1
ORI Z IS U AND Y IS N
POS E 42358.2 N -7806.1 U 66.2

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 42358.161681mm N -7806.091646mm U 82.487334mm
ORI Y IS N AND Z IS U
HEIG 14.077845mm

NEW LOOP
NEW VERTEX
POS E 14.95771mm N 8.635838mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.271676mm U 0mm
END
NEW VERTEX
POS E -14.95771mm N 8.635838mm U 0mm
END
NEW VERTEX
POS E -14.95771mm N -8.635838mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.271676mm U 0mm
END
NEW VERTEX
POS E 14.95771mm N -8.635838mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 17.6
HEIG 50.1
ORI Z IS U AND Y IS N
POS E 42358.2 N -7730.4 U 66.2

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 42358.161681mm N -7730.404309mm U 82.487334mm
ORI Y IS N AND Z IS U
HEIG 14.077845mm

NEW LOOP
NEW VERTEX
POS E 14.95771mm N 8.635838mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.271676mm U 0mm
END
NEW VERTEX
POS E -14.95771mm N 8.635838mm U 0mm
END
NEW VERTEX
POS E -14.95771mm N -8.635838mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.271676mm U 0mm
END
NEW VERTEX
POS E 14.95771mm N -8.635838mm U 0mm
END
END
END

NEW SUBE /205_PU_027_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 210x437 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22C271,22C272,22C273,22C274,22C275,22C276 ...
NEW CYLI
DIAM 436.7
HEIG 210.2
ORI Z IS N AND Y IS U
POS E 42358.2 N -7768.2 U 477.0

-- volute closing onto the suction cover
NEW CONE
DTOP 270.7
DBOT 436.7
HEIG 63.1
ORI Z IS N AND Y IS U
POS E 42358.2 N -7631.6 U 477.0

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 183.4
HEIG 37.8
ORI Z IS N AND Y IS U
POS E 42358.2 N -7892.3 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 109.3
ORI Z IS N AND Y IS U
POS E 42583.7 N -7768.2 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 109.3
ORI Z IS N AND Y IS U
POS E 42132.6 N -7768.2 U 477.0

NEW SUBE /205_PU_027_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 431x221 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 22C263,22C264,22C265
NEW CYLI
DIAM 221.0
HEIG 431.3
ORI Z IS N AND Y IS U
POS E 42218.0 N -8509.5 U 477.0

NEW SUBE /205_PU_027_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 199 mm apart running 248 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22C267,22C266
NEW CYLI
DIAM 199.5
HEIG 248.0
ORI Z IS N AND Y IS U
POS E 42218.0 N -8169.9 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 42218.0 N -8266.6 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 42218.0 N -8073.2 U 477.0

NEW SUBE /205_PU_027_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 960 mm along the machine axis x 647 mm across, consolidated from 2 drawn sections (body, fin bands, cowl)
-- CAD handles: 22C27E,22C27F,22C280,22C284,22C285,22C286 ...
NEW CYLI
DIAM 646.9
HEIG 959.6
ORI Z IS N AND Y IS U
POS E 42220.7 N -9204.9 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.6
ORI Z IS N AND Y IS U
POS E 42220.7 N -9655.9 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.6
ORI Z IS N AND Y IS U
POS E 42220.7 N -8753.9 U 477.0

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 41889.2 N -9204.9 U 477.0

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 41914.5 N -9204.9 U 603.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 41986.3 N -9204.9 U 711.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42093.9 N -9204.9 U 783.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42220.7 N -9204.9 U 808.4

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42347.5 N -9204.9 U 783.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42455.1 N -9204.9 U 711.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42526.9 N -9204.9 U 603.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42552.1 N -9204.9 U 477.0

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42526.9 N -9204.9 U 350.1

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42455.1 N -9204.9 U 242.6

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42347.5 N -9204.9 U 170.7

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42220.7 N -9204.9 U 145.5

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 42093.9 N -9204.9 U 170.7

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 41986.3 N -9204.9 U 242.6

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 690.9
ORI Z IS N AND Y IS U
POS E 41914.5 N -9204.9 U 350.1

-- Motor terminal box
NEW BOX
XLEN 258.8
YLEN 287.9
ZLEN 142.3
POS E 42220.7 N -9204.9 U 871.6

-- Motor cable gland
NEW CYLI
DIAM 48.4
HEIG 142.3
ORI Z IS E AND Y IS U
POS E 42020.2 N -9204.9 U 871.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.3
YLEN 77.6
ZLEN 64.7
POS E 42220.7 N -9473.6 U 878.7

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.1
YLEN 172.7
ZLEN 6.0
POS E 42546.1 N -9089.8 U 477.0

-- Motor fan cowl disc
NEW CYLI
DIAM 711.6
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 42220.7 N -9688.7 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 42384.4 N -9688.7 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 42057.0 N -9688.7 U 477.0

NEW SUBE /205_PU_027_AUXILIARY
-- 2 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 173x313 at the wet end, outboard of the casing
-- CAD handles: 22C268,22C269,22C26A
NEW BOX
XLEN 312.7
YLEN 172.5
ZLEN 138.0
POS E 42231.5 N -7959.6 U 119.0

-- Auxiliary [LOW]: body 16x340 at the wet end, outboard of the casing
-- CAD handles: 228F4B,22C2A3,22C2A2,22C2A1,210AB0,22C2A0 ...
NEW BOX
XLEN 339.6
YLEN 16.2
ZLEN 60.0
POS E 42218.0 N -7563.4 U 80.0

NEW SUBE /205_PU_027_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_027_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 42218.0 N -7587.3 U 477.0
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_027_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_027_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 42358.2 N -7768.2 U 845.3
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-030
-- --------------------------------------------------------------------
-- 205-PU-030 - EOP WASHER FRONT DILUTION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-030
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 216 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_030
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_030_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 863.0
YLEN 2129.0
ZLEN 50.0
POS E 40868.0 N 14089.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 40488.3 N 13114.5 U 69.4

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 40488.28mm N 13114.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 40488.3 N 15063.5 U 69.4

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 40488.28mm N 15063.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 41247.7 N 13114.5 U 69.4

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 41247.72mm N 13114.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 41247.7 N 15063.5 U 69.4

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 41247.72mm N 15063.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

NEW SUBE /205_PU_030_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 712.6
YLEN 186.5
ZLEN 74.4
POS E 40870.7 N 13260.8 U 87.2

-- Motor foot: pedestal web
NEW BOX
XLEN 359.4
YLEN 94.1
ZLEN 62.6
POS E 40870.7 N 13260.8 U 155.7

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 41025.614604mm N 13212.08892mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 40653.808621mm N 13212.08892mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 40870.7 N 13202.4 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 40870.695444mm N 13202.356305mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 40870.7 N 13319.1 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 40870.695444mm N 13319.147687mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 712.6
YLEN 186.5
ZLEN 74.4
POS E 40870.7 N 13871.4 U 87.2

-- Motor foot: pedestal web
NEW BOX
XLEN 359.4
YLEN 94.1
ZLEN 62.6
POS E 40870.7 N 13871.4 U 155.7

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 41025.614604mm N 13822.762813mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 40653.808621mm N 13822.762813mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 40870.7 N 13813.0 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 40870.695444mm N 13813.030198mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 40870.7 N 13929.8 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 40870.695444mm N 13929.82158mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 157.6
YLEN 401.7
ZLEN 16.4
POS E 40870.7 N 14261.5 U 58.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 79.5
YLEN 202.6
ZLEN 314.6
POS E 40870.7 N 14261.5 U 223.7

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 40904.954199mm N 14156.708926mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 276.85424mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 40822.733189mm N 14156.708926mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 276.85424mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 40870.7 N 14135.7 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 40870.695444mm N 14135.749356mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 40870.7 N 14387.3 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 40870.695444mm N 14387.264196mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 468.9
YLEN 132.4
ZLEN 48.9
POS E 40900.3 N 15005.4 U 74.5

-- Casing support: pedestal web
NEW BOX
XLEN 236.5
YLEN 66.8
ZLEN 65.9
POS E 40900.3 N 15005.4 U 131.9

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 41002.285739mm N 14970.913823mm U 98.931547mm
ORI Y IS U AND Z IS E
HEIG 40.776289mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.056619mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.981141mm N 57.986053mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 40757.628002mm N 14970.913823mm U 98.931547mm
ORI Y IS U AND Z IS E
HEIG 40.776289mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.056619mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.981141mm N 57.986053mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.5
HEIG 75.4
ORI Z IS U AND Y IS N
POS E 40900.3 N 14964.0 U 74.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 40900.345016mm N 14964.008161mm U 98.931547mm
ORI Y IS N AND Z IS U
HEIG 21.203671mm

NEW LOOP
NEW VERTEX
POS E 22.5289mm N 13.007066mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.014133mm U 0mm
END
NEW VERTEX
POS E -22.5289mm N 13.007066mm U 0mm
END
NEW VERTEX
POS E -22.5289mm N -13.007066mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.014133mm U 0mm
END
NEW VERTEX
POS E 22.5289mm N -13.007066mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.5
HEIG 75.4
ORI Z IS U AND Y IS N
POS E 40900.3 N 15046.9 U 74.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 40900.345016mm N 15046.876105mm U 98.931547mm
ORI Y IS N AND Z IS U
HEIG 21.203671mm

NEW LOOP
NEW VERTEX
POS E 22.5289mm N 13.007066mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.014133mm U 0mm
END
NEW VERTEX
POS E -22.5289mm N 13.007066mm U 0mm
END
NEW VERTEX
POS E -22.5289mm N -13.007066mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.014133mm U 0mm
END
NEW VERTEX
POS E 22.5289mm N -13.007066mm U 0mm
END
END
END

NEW SUBE /205_PU_030_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 210x658 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22BEB4,22BEB5,22BEB6,22BEB7,22BEB8,22BEB9 ...
NEW CYLI
DIAM 657.7
HEIG 230.2
ORI Z IS N AND Y IS U
POS E 40900.3 N 15005.4 U 480.5

-- volute closing onto the suction cover
NEW CONE
DTOP 407.8
DBOT 657.7
HEIG 23.2
ORI Z IS N AND Y IS U
POS E 40900.3 N 15132.1 U 480.5

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 276.2
HEIG 41.4
ORI Z IS N AND Y IS U
POS E 40900.3 N 14869.6 U 480.5

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 119.7
ORI Z IS N AND Y IS U
POS E 41236.4 N 15005.4 U 480.5

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 119.7
ORI Z IS N AND Y IS U
POS E 40564.3 N 15005.4 U 480.5

NEW SUBE /205_PU_030_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 437x221 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 22BE93,22BE94,22BE95
NEW CYLI
DIAM 221.0
HEIG 436.7
ORI Z IS N AND Y IS U
POS E 40870.7 N 14261.5 U 480.5

NEW SUBE /205_PU_030_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 199 mm apart running 248 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BE97,22BE96
NEW CYLI
DIAM 199.5
HEIG 248.0
ORI Z IS N AND Y IS U
POS E 40870.7 N 14603.8 U 480.5

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 40870.7 N 14507.1 U 480.5

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 40870.7 N 14700.5 U 480.5

NEW SUBE /205_PU_030_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 954 mm along the machine axis x 652 mm across, consolidated from 2 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BEC1,22BEC2,22BEC3,22BEC7,22BEC8,22BEC9 ...
NEW CYLI
DIAM 652.3
HEIG 954.2
ORI Z IS N AND Y IS U
POS E 40870.7 N 13566.1 U 480.5

-- Motor end bell
NEW CYLI
DIAM 704.5
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 40870.7 N 13117.6 U 480.5

-- Motor end bell
NEW CYLI
DIAM 704.5
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 40870.7 N 14014.6 U 480.5

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40536.5 N 13566.1 U 480.5

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40562.0 N 13566.1 U 608.4

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40634.4 N 13566.1 U 716.8

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40742.8 N 13566.1 U 789.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40870.7 N 13566.1 U 814.7

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40998.6 N 13566.1 U 789.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 41107.0 N 13566.1 U 716.8

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 41179.4 N 13566.1 U 608.4

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 41204.8 N 13566.1 U 480.5

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 41179.4 N 13566.1 U 352.6

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 41107.0 N 13566.1 U 244.2

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40998.6 N 13566.1 U 171.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40870.7 N 13566.1 U 146.4

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40742.8 N 13566.1 U 171.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40634.4 N 13566.1 U 244.2

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 40562.0 N 13566.1 U 352.6

-- Motor terminal box
NEW BOX
XLEN 260.9
YLEN 286.3
ZLEN 143.5
POS E 40870.7 N 13566.1 U 878.4

-- Motor cable gland
NEW CYLI
DIAM 48.8
HEIG 143.5
ORI Z IS E AND Y IS U
POS E 40668.5 N 13566.1 U 878.4

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.7
YLEN 78.3
ZLEN 65.2
POS E 40870.7 N 13298.9 U 885.6

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.8
YLEN 171.8
ZLEN 6.0
POS E 41198.8 N 13680.6 U 480.5

-- Motor fan cowl disc
NEW CYLI
DIAM 717.5
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 40870.7 N 13085.0 U 480.5

-- Motor fan grille bar
NEW BOX
XLEN 330.1
YLEN 9.6
ZLEN 6.4
POS E 41035.7 N 13085.0 U 480.5

-- Motor fan grille bar
NEW BOX
XLEN 330.1
YLEN 9.6
ZLEN 6.4
POS E 40705.7 N 13085.0 U 480.5

NEW SUBE /205_PU_030_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 173x334 at the wet end, outboard of the casing
-- CAD handles: 22BE98,22BE99,22BE9A
NEW BOX
XLEN 334.2
YLEN 172.5
ZLEN 138.0
POS E 40868.0 N 14814.1 U 119.0

NEW SUBE /205_PU_030_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_030_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 40868.0 N 15154.0 U 480.5
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_030_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_030_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 40900.3 N 15005.4 U 959.4
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-031
-- --------------------------------------------------------------------
-- 205-PU-031 - D0 STAGE DILUTION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-031
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 221 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 151 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_031
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_031_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 857.0
YLEN 2129.0
ZLEN 50.0
POS E 37916.0 N 14089.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 37538.9 N 13114.5 U 69.3

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 37538.92mm N 13114.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 37538.9 N 15063.5 U 69.3

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 37538.92mm N 15063.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 38293.1 N 13114.5 U 69.3

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 38293.08mm N 13114.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.7
HEIG 38.6
ORI Z IS U AND Y IS N
POS E 38293.1 N 15063.5 U 69.3

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 38293.08mm N 15063.5mm U 88.565mm
ORI Y IS N AND Z IS U
HEIG 20.568mm

NEW LOOP
NEW VERTEX
POS E 21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.234248mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N 12.617124mm U 0mm
END
NEW VERTEX
POS E -21.8535mm N -12.617124mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.234248mm U 0mm
END
NEW VERTEX
POS E 21.8535mm N -12.617124mm U 0mm
END
END
END

NEW SUBE /205_PU_031_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 186.5
ZLEN 73.7
POS E 37918.7 N 13260.8 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.1
ZLEN 62.1
POS E 37918.7 N 13260.8 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 38072.334189mm N 13212.08892mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 37703.601012mm N 13212.08892mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 37918.7 N 13202.4 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 37918.695365mm N 13202.356305mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 37918.7 N 13319.1 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 37918.695365mm N 13319.147687mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 706.7
YLEN 186.5
ZLEN 73.7
POS E 37918.7 N 13871.4 U 86.9

-- Motor foot: pedestal web
NEW BOX
XLEN 356.4
YLEN 94.1
ZLEN 62.1
POS E 37918.7 N 13871.4 U 154.8

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 38072.334189mm N 13822.762813mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 37703.601012mm N 13822.762813mm U 123.746635mm
ORI Y IS U AND Z IS E
HEIG 61.455529mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 54.650138mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 37918.7 N 13813.0 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 37918.695365mm N 13813.030198mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 39.9
HEIG 113.7
ORI Z IS U AND Y IS N
POS E 37918.7 N 13929.8 U 86.9

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 37918.695365mm N 13929.82158mm U 123.746635mm
ORI Y IS N AND Z IS U
HEIG 31.956875mm

NEW LOOP
NEW VERTEX
POS E 33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.20691mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N 19.603455mm U 0mm
END
NEW VERTEX
POS E -33.95418mm N -19.603455mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.20691mm U 0mm
END
NEW VERTEX
POS E 33.95418mm N -19.603455mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 157.6
YLEN 401.7
ZLEN 16.4
POS E 37916.0 N 14261.5 U 58.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 79.5
YLEN 202.6
ZLEN 311.0
POS E 37916.0 N 14261.5 U 222.0

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 37950.258779mm N 14156.708926mm U 66.444214mm
ORI Y IS U AND Z IS E
HEIG 13.703511mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 273.723138mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 37868.03771mm N 14156.708926mm U 66.444214mm
ORI Y IS U AND Z IS E
HEIG 13.703511mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 273.723138mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 37916.0 N 14135.7 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 37916mm N 14135.749356mm U 66.444214mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 37916.0 N 14387.3 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 37916mm N 14387.264196mm U 66.444214mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 465.1
YLEN 131.3
ZLEN 48.5
POS E 37948.3 N 15005.4 U 74.3

-- Casing support: pedestal web
NEW BOX
XLEN 234.6
YLEN 66.2
ZLEN 65.3
POS E 37948.3 N 15005.4 U 131.2

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 38049.450127mm N 14971.196853mm U 98.530453mm
ORI Y IS U AND Z IS E
HEIG 40.442044mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 68.490559mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.669808mm N 57.485166mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 37806.79786mm N 14971.196853mm U 98.530453mm
ORI Y IS U AND Z IS E
HEIG 40.442044mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 68.490559mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.669808mm N 57.485166mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.3
HEIG 74.8
ORI Z IS U AND Y IS N
POS E 37948.3 N 14964.3 U 74.3

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 37948.345016mm N 14964.347797mm U 98.530453mm
ORI Y IS N AND Z IS U
HEIG 21.029863mm

NEW LOOP
NEW VERTEX
POS E 22.34423mm N 12.900447mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.800894mm U 0mm
END
NEW VERTEX
POS E -22.34423mm N 12.900447mm U 0mm
END
NEW VERTEX
POS E -22.34423mm N -12.900447mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.800894mm U 0mm
END
NEW VERTEX
POS E 22.34423mm N -12.900447mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.3
HEIG 74.8
ORI Z IS U AND Y IS N
POS E 37948.3 N 15046.5 U 74.3

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 37948.345016mm N 15046.536469mm U 98.530453mm
ORI Y IS N AND Z IS U
HEIG 21.029863mm

NEW LOOP
NEW VERTEX
POS E 22.34423mm N 12.900447mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.800894mm U 0mm
END
NEW VERTEX
POS E -22.34423mm N 12.900447mm U 0mm
END
NEW VERTEX
POS E -22.34423mm N -12.900447mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.800894mm U 0mm
END
NEW VERTEX
POS E 22.34423mm N -12.900447mm U 0mm
END
END
END

NEW SUBE /205_PU_031_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 210x652 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22BE76,22BE77,22BE78,22BE79,22BE7A,22BE7B ...
NEW CYLI
DIAM 652.3
HEIG 228.3
ORI Z IS N AND Y IS U
POS E 37948.3 N 15005.4 U 477.0

-- volute closing onto the suction cover
NEW CONE
DTOP 404.4
DBOT 652.3
HEIG 24.1
ORI Z IS N AND Y IS U
POS E 37948.3 N 15131.6 U 477.0

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 274.0
HEIG 41.1
ORI Z IS N AND Y IS U
POS E 37948.3 N 14870.7 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 118.7
ORI Z IS N AND Y IS U
POS E 38281.7 N 15005.4 U 477.0

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 118.7
ORI Z IS N AND Y IS U
POS E 37615.0 N 15005.4 U 477.0

NEW SUBE /205_PU_031_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 437x221 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 22BE55,22BE56,22BE57
NEW CYLI
DIAM 221.0
HEIG 436.7
ORI Z IS N AND Y IS U
POS E 37916.0 N 14261.5 U 477.0

NEW SUBE /205_PU_031_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 199 mm apart running 248 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BE59,22BE58
NEW CYLI
DIAM 199.5
HEIG 248.0
ORI Z IS N AND Y IS U
POS E 37916.0 N 14603.8 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 37916.0 N 14507.1 U 477.0

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 37916.0 N 14700.5 U 477.0

NEW SUBE /205_PU_031_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 954 mm along the machine axis x 647 mm across, consolidated from 2 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BE83,22BE84,22BE85,22BE89,22BE8A,22BE8B ...
NEW CYLI
DIAM 646.9
HEIG 954.2
ORI Z IS N AND Y IS U
POS E 37918.7 N 13566.1 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 37918.7 N 13117.6 U 477.0

-- Motor end bell
NEW CYLI
DIAM 698.7
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 37918.7 N 14014.6 U 477.0

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 37587.2 N 13566.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 37612.5 N 13566.1 U 603.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 37684.3 N 13566.1 U 711.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 37791.9 N 13566.1 U 783.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 37918.7 N 13566.1 U 808.4

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 38045.5 N 13566.1 U 783.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 38153.1 N 13566.1 U 711.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 38224.9 N 13566.1 U 603.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 38250.1 N 13566.1 U 477.0

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 38224.9 N 13566.1 U 350.1

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 38153.1 N 13566.1 U 242.6

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 38045.5 N 13566.1 U 170.7

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 37918.7 N 13566.1 U 145.5

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 37791.9 N 13566.1 U 170.7

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 37684.3 N 13566.1 U 242.6

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 37612.5 N 13566.1 U 350.1

-- Motor terminal box
NEW BOX
XLEN 258.8
YLEN 286.3
ZLEN 142.3
POS E 37918.7 N 13566.1 U 871.6

-- Motor cable gland
NEW CYLI
DIAM 48.4
HEIG 142.3
ORI Z IS E AND Y IS U
POS E 37718.2 N 13566.1 U 871.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.3
YLEN 77.6
ZLEN 64.7
POS E 37918.7 N 13298.9 U 878.7

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.1
YLEN 171.8
ZLEN 6.0
POS E 38244.1 N 13680.6 U 477.0

-- Motor fan cowl disc
NEW CYLI
DIAM 711.6
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 37918.7 N 13085.0 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 38082.4 N 13085.0 U 477.0

-- Motor fan grille bar
NEW BOX
XLEN 327.3
YLEN 9.6
ZLEN 6.4
POS E 37755.0 N 13085.0 U 477.0

NEW SUBE /205_PU_031_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 173x334 at the wet end, outboard of the casing
-- CAD handles: 22BE5A,22BE5B,22BE5C
NEW BOX
XLEN 334.2
YLEN 172.5
ZLEN 138.0
POS E 37918.7 N 14814.1 U 119.0

NEW SUBE /205_PU_031_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_031_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 37916.0 N 15154.0 U 477.0
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_031_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_031_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 37948.3 N 15005.4 U 953.1
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-032
-- --------------------------------------------------------------------
-- 205-PU-032 - EOP WASHER WIRE WASH PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-032
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 216 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_032
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_032_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 765.0
YLEN 1671.0
ZLEN 50.0
POS E 39418.0 N 14294.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.9
HEIG 34.4
ORI Z IS U AND Y IS N
POS E 39081.4 N 13548.5 U 67.2

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 39081.4mm N 13548.5mm U 84.425mm
ORI Y IS N AND Z IS U
HEIG 18.36mm

NEW LOOP
NEW VERTEX
POS E 19.5075mm N 11.26266mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.525321mm U 0mm
END
NEW VERTEX
POS E -19.5075mm N 11.26266mm U 0mm
END
NEW VERTEX
POS E -19.5075mm N -11.26266mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.525321mm U 0mm
END
NEW VERTEX
POS E 19.5075mm N -11.26266mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.9
HEIG 34.4
ORI Z IS U AND Y IS N
POS E 39081.4 N 15039.5 U 67.2

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 39081.4mm N 15039.5mm U 84.425mm
ORI Y IS N AND Z IS U
HEIG 18.36mm

NEW LOOP
NEW VERTEX
POS E 19.5075mm N 11.26266mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.525321mm U 0mm
END
NEW VERTEX
POS E -19.5075mm N 11.26266mm U 0mm
END
NEW VERTEX
POS E -19.5075mm N -11.26266mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.525321mm U 0mm
END
NEW VERTEX
POS E 19.5075mm N -11.26266mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.9
HEIG 34.4
ORI Z IS U AND Y IS N
POS E 39754.6 N 13548.5 U 67.2

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 39754.6mm N 13548.5mm U 84.425mm
ORI Y IS N AND Z IS U
HEIG 18.36mm

NEW LOOP
NEW VERTEX
POS E 19.5075mm N 11.26266mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.525321mm U 0mm
END
NEW VERTEX
POS E -19.5075mm N 11.26266mm U 0mm
END
NEW VERTEX
POS E -19.5075mm N -11.26266mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.525321mm U 0mm
END
NEW VERTEX
POS E 19.5075mm N -11.26266mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.9
HEIG 34.4
ORI Z IS U AND Y IS N
POS E 39754.6 N 15039.5 U 67.2

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 39754.6mm N 15039.5mm U 84.425mm
ORI Y IS N AND Z IS U
HEIG 18.36mm

NEW LOOP
NEW VERTEX
POS E 19.5075mm N 11.26266mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.525321mm U 0mm
END
NEW VERTEX
POS E -19.5075mm N 11.26266mm U 0mm
END
NEW VERTEX
POS E -19.5075mm N -11.26266mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.525321mm U 0mm
END
NEW VERTEX
POS E 19.5075mm N -11.26266mm U 0mm
END
END
END

NEW SUBE /205_PU_032_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 303.6
YLEN 376.9
ZLEN 31.7
POS E 39415.3 N 14436.9 U 65.8

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 153.1
YLEN 190.1
ZLEN 125.3
POS E 39415.3 N 14436.9 U 144.4

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 39481.315325mm N 14338.528304mm U 81.685169mm
ORI Y IS U AND Z IS E
HEIG 26.404308mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.657643mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161704mm N 110.307907mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 39322.889478mm N 14338.528304mm U 81.685169mm
ORI Y IS U AND Z IS E
HEIG 26.404308mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.657643mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161704mm N 110.307907mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.2
HEIG 48.8
ORI Z IS U AND Y IS N
POS E 39415.3 N 14318.9 U 65.8

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 39415.304556mm N 14318.862539mm U 81.685169mm
ORI Y IS N AND Z IS U
HEIG 13.73024mm

NEW LOOP
NEW VERTEX
POS E 14.58838mm N 8.422605mm U 0mm
END
NEW VERTEX
POS E 0mm N 16.84521mm U 0mm
END
NEW VERTEX
POS E -14.58838mm N 8.422605mm U 0mm
END
NEW VERTEX
POS E -14.58838mm N -8.422605mm U 0mm
END
NEW VERTEX
POS E 0mm N -16.84521mm U 0mm
END
NEW VERTEX
POS E 14.58838mm N -8.422605mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.2
HEIG 48.8
ORI Z IS U AND Y IS N
POS E 39415.3 N 14554.9 U 65.8

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 39415.304556mm N 14554.851711mm U 81.685169mm
ORI Y IS N AND Z IS U
HEIG 13.73024mm

NEW LOOP
NEW VERTEX
POS E 14.58838mm N 8.422605mm U 0mm
END
NEW VERTEX
POS E 0mm N 16.84521mm U 0mm
END
NEW VERTEX
POS E -14.58838mm N 8.422605mm U 0mm
END
NEW VERTEX
POS E -14.58838mm N -8.422605mm U 0mm
END
NEW VERTEX
POS E 0mm N -16.84521mm U 0mm
END
NEW VERTEX
POS E 14.58838mm N -8.422605mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 577.2
YLEN 132.8
ZLEN 60.2
POS E 39418.0 N 13685.8 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 291.1
YLEN 67.0
ZLEN 50.7
POS E 39418.0 N 13685.8 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 39543.471693mm N 13651.164353mm U 110.226413mm
ORI Y IS U AND Z IS E
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 39242.339629mm N 13651.164353mm U 110.226413mm
ORI Y IS U AND Z IS E
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 39418.0 N 13644.2 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 39418mm N 13644.236051mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 39418.0 N 13727.4 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 39418mm N 13727.375679mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 577.2
YLEN 132.8
ZLEN 60.2
POS E 39418.0 N 14120.5 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 291.1
YLEN 67.0
ZLEN 50.7
POS E 39418.0 N 14120.5 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 39543.471693mm N 14085.881362mm U 110.226413mm
ORI Y IS U AND Z IS E
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 39242.339629mm N 14085.881362mm U 110.226413mm
ORI Y IS U AND Z IS E
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 39418.0 N 14079.0 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 39418mm N 14078.95306mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 39418.0 N 14162.1 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 39418mm N 14162.092687mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 230.6
YLEN 161.2
ZLEN 24.1
POS E 39439.6 N 14992.1 U 62.0

-- Casing support: pedestal web
NEW BOX
XLEN 116.3
YLEN 81.3
ZLEN 169.4
POS E 39439.6 N 14992.1 U 158.7

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 39489.698091mm N 14950.064671mm U 74.064692mm
ORI Y IS U AND Z IS E
HEIG 20.05391mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 84.097056mm N 0mm U 0mm
END
NEW VERTEX
POS E 46.253381mm N 149.03545mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 39369.374633mm N 14950.064671mm U 74.064692mm
ORI Y IS U AND Z IS E
HEIG 20.05391mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 84.097056mm N 0mm U 0mm
END
NEW VERTEX
POS E 46.253381mm N 149.03545mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 13.0
HEIG 37.1
ORI Z IS U AND Y IS N
POS E 39439.6 N 14941.7 U 62.0

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 39439.563317mm N 14941.654965mm U 74.064692mm
ORI Y IS N AND Z IS U
HEIG 10.428033mm

NEW LOOP
NEW VERTEX
POS E 11.079785mm N 6.396917mm U 0mm
END
NEW VERTEX
POS E 0mm N 12.793834mm U 0mm
END
NEW VERTEX
POS E -11.079785mm N 6.396917mm U 0mm
END
NEW VERTEX
POS E -11.079785mm N -6.396917mm U 0mm
END
NEW VERTEX
POS E 0mm N -12.793834mm U 0mm
END
NEW VERTEX
POS E 11.079785mm N -6.396917mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 13.0
HEIG 37.1
ORI Z IS U AND Y IS N
POS E 39439.6 N 15042.6 U 62.0

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 39439.563317mm N 15042.571432mm U 74.064692mm
ORI Y IS N AND Z IS U
HEIG 10.428033mm

NEW LOOP
NEW VERTEX
POS E 11.079785mm N 6.396917mm U 0mm
END
NEW VERTEX
POS E 0mm N 12.793834mm U 0mm
END
NEW VERTEX
POS E -11.079785mm N 6.396917mm U 0mm
END
NEW VERTEX
POS E -11.079785mm N -6.396917mm U 0mm
END
NEW VERTEX
POS E 0mm N -12.793834mm U 0mm
END
NEW VERTEX
POS E 11.079785mm N -6.396917mm U 0mm
END
END
END

NEW SUBE /205_PU_032_CASING
-- 4 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 280x323 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22F2AC,22F2AA,22F2AB,22F26B,22F26A,22F2A0 ...
NEW CYLI
DIAM 323.5
HEIG 280.3
ORI Z IS N AND Y IS U
POS E 39439.6 N 14992.1 U 398.7

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 135.8
HEIG 50.5
ORI Z IS N AND Y IS U
POS E 39439.6 N 14826.7 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 14.6
HEIG 145.8
ORI Z IS N AND Y IS U
POS E 39607.1 N 14992.1 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 14.6
HEIG 145.8
ORI Z IS N AND Y IS U
POS E 39272.0 N 14992.1 U 398.7

NEW SUBE /205_PU_032_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 410 mm along the machine axis x 426 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22F27D,22F27E,22F248,22F247,22BEDF,22BEE0 ...
NEW CYLI
DIAM 425.9
HEIG 409.7
ORI Z IS N AND Y IS U
POS E 39415.3 N 14436.9 U 398.7

NEW SUBE /205_PU_032_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 86 mm apart running 210 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22F2A2,22F26C
NEW CYLI
DIAM 86.3
HEIG 210.2
ORI Z IS N AND Y IS U
POS E 39439.6 N 14746.8 U 398.7

-- Coupling hub (d=151) on the shaft centreline
NEW CYLI
DIAM 150.9
HEIG 46.3
ORI Z IS N AND Y IS U
POS E 39439.6 N 14664.8 U 398.7

-- Coupling hub (d=151) on the shaft centreline
NEW CYLI
DIAM 150.9
HEIG 46.3
ORI Z IS N AND Y IS U
POS E 39439.6 N 14828.8 U 398.7

NEW SUBE /205_PU_032_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 679 mm along the machine axis x 528 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22F24C,22F24B,22F281,22F282,22BED9,22F27F ...
NEW CYLI
DIAM 528.3
HEIG 679.2
ORI Z IS N AND Y IS U
POS E 39418.0 N 13903.2 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS N AND Y IS U
POS E 39418.0 N 13583.9 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS N AND Y IS U
POS E 39418.0 N 14222.4 U 398.7

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39146.5 N 13903.2 U 398.7

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39167.1 N 13903.2 U 502.6

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39226.0 N 13903.2 U 590.7

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39314.1 N 13903.2 U 649.6

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 13903.2 U 670.2

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39521.9 N 13903.2 U 649.6

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39610.0 N 13903.2 U 590.7

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39668.9 N 13903.2 U 502.6

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39689.5 N 13903.2 U 398.7

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39668.9 N 13903.2 U 294.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39610.0 N 13903.2 U 206.7

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39521.9 N 13903.2 U 147.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39418.0 N 13903.2 U 127.1

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39314.1 N 13903.2 U 147.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39226.0 N 13903.2 U 206.7

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 39167.1 N 13903.2 U 294.8

-- Motor terminal box
NEW BOX
XLEN 211.3
YLEN 203.8
ZLEN 116.2
POS E 39418.0 N 13903.2 U 720.9

-- Motor cable gland
NEW CYLI
DIAM 39.5
HEIG 116.2
ORI Z IS E AND Y IS U
POS E 39254.2 N 13903.2 U 720.9

-- Reference Value: motor lifting lug
NEW BOX
XLEN 37.0
YLEN 63.4
ZLEN 52.8
POS E 39418.0 N 13713.0 U 726.8

-- Reference Value: motor nameplate
NEW BOX
XLEN 68.7
YLEN 122.3
ZLEN 6.0
POS E 39684.2 N 13984.7 U 398.7

-- Motor fan cowl disc
NEW CYLI
DIAM 581.1
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 39418.0 N 13559.5 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 267.3
YLEN 9.6
ZLEN 6.4
POS E 39551.7 N 13559.5 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 267.3
YLEN 9.6
ZLEN 6.4
POS E 39284.3 N 13559.5 U 398.7

NEW SUBE /205_PU_032_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_032_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 39418.0 N 15167.5 U 398.7
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_032_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_032_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 39439.6 N 14992.1 U 710.4
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-038
-- --------------------------------------------------------------------
-- 205-PU-038 - EOP STAGE MC PUMP (205-PU-038/MC PUMP)
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-038
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: W (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 140 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)
-- Note: discharge: metadata bore 167 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_038
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_038_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 2000.0
YLEN 1051.0
ZLEN 50.0
POS E 43119.0 N 5016.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 31.5
HEIG 47.3
ORI Z IS U AND Y IS N
POS E 42209.0 N 4580.5 U 73.6

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 42209mm N 4580.5mm U 97.295mm
ORI Y IS N AND Z IS U
HEIG 25.224mm

NEW LOOP
NEW VERTEX
POS E 26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.946552mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N -15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.946552mm U 0mm
END
NEW VERTEX
POS E 26.8005mm N -15.473276mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 31.5
HEIG 47.3
ORI Z IS U AND Y IS N
POS E 42209.0 N 5451.5 U 73.6

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 42209mm N 5451.5mm U 97.295mm
ORI Y IS N AND Z IS U
HEIG 25.224mm

NEW LOOP
NEW VERTEX
POS E 26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.946552mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N -15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.946552mm U 0mm
END
NEW VERTEX
POS E 26.8005mm N -15.473276mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 31.5
HEIG 47.3
ORI Z IS U AND Y IS N
POS E 44029.0 N 4580.5 U 73.6

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 44029mm N 4580.5mm U 97.295mm
ORI Y IS N AND Z IS U
HEIG 25.224mm

NEW LOOP
NEW VERTEX
POS E 26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.946552mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N -15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.946552mm U 0mm
END
NEW VERTEX
POS E 26.8005mm N -15.473276mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 31.5
HEIG 47.3
ORI Z IS U AND Y IS N
POS E 44029.0 N 5451.5 U 73.6

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 44029mm N 5451.5mm U 97.295mm
ORI Y IS N AND Z IS U
HEIG 25.224mm

NEW LOOP
NEW VERTEX
POS E 26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.946552mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N 15.473276mm U 0mm
END
NEW VERTEX
POS E -26.8005mm N -15.473276mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.946552mm U 0mm
END
NEW VERTEX
POS E 26.8005mm N -15.473276mm U 0mm
END
END
END

NEW SUBE /205_PU_038_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 317.4
YLEN 211.4
ZLEN 22.1
POS E 43143.3 N 5016.0 U 61.0

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 160.1
YLEN 106.6
ZLEN 285.7
POS E 43143.3 N 5016.0 U 214.9

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 43226.062014mm N 5061.956964mm U 72.059305mm
ORI Y IS U AND Z IS N
HEIG 18.382754mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 165.606505mm N 0mm U 0mm
END
NEW VERTEX
POS E 91.083578mm N 251.419013mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 43226.062014mm N 4951.660441mm U 72.059305mm
ORI Y IS U AND Z IS N
HEIG 18.382754mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 165.606505mm N 0mm U 0mm
END
NEW VERTEX
POS E 91.083578mm N 251.419013mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 34.1
ORI Z IS U AND Y IS N
POS E 43242.6 N 5016.0 U 61.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 43242.622665mm N 5016.00008mm U 72.059305mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 34.1
ORI Z IS U AND Y IS N
POS E 43043.9 N 5016.0 U 61.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 43043.894859mm N 5016.00008mm U 72.059305mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 134.9
YLEN 730.3
ZLEN 76.2
POS E 42846.5 N 5013.3 U 88.1

-- Motor foot: pedestal web
NEW BOX
XLEN 68.0
YLEN 368.3
ZLEN 64.2
POS E 42846.5 N 5013.3 U 158.3

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 42881.73851mm N 5172.064728mm U 126.204844mm
ORI Y IS U AND Z IS N
HEIG 63.504037mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 70.382748mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.710512mm N 56.471801mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 42881.73851mm N 4791.040505mm U 126.204844mm
ORI Y IS U AND Z IS N
HEIG 63.504037mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 70.382748mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.710512mm N 56.471801mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 41.3
HEIG 117.5
ORI Z IS U AND Y IS N
POS E 42888.8 N 5013.3 U 88.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 42888.776785mm N 5013.304635mm U 126.204844mm
ORI Y IS N AND Z IS U
HEIG 33.022099mm

NEW LOOP
NEW VERTEX
POS E 35.08598mm N 20.2569mm U 0mm
END
NEW VERTEX
POS E 0mm N 40.513801mm U 0mm
END
NEW VERTEX
POS E -35.08598mm N 20.2569mm U 0mm
END
NEW VERTEX
POS E -35.08598mm N -20.2569mm U 0mm
END
NEW VERTEX
POS E 0mm N -40.513801mm U 0mm
END
NEW VERTEX
POS E 35.08598mm N -20.2569mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 41.3
HEIG 117.5
ORI Z IS U AND Y IS N
POS E 42804.3 N 5013.3 U 88.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 42804.317487mm N 5013.304635mm U 126.204844mm
ORI Y IS N AND Z IS U
HEIG 33.022099mm

NEW LOOP
NEW VERTEX
POS E 35.08598mm N 20.2569mm U 0mm
END
NEW VERTEX
POS E 0mm N 40.513801mm U 0mm
END
NEW VERTEX
POS E -35.08598mm N 20.2569mm U 0mm
END
NEW VERTEX
POS E -35.08598mm N -20.2569mm U 0mm
END
NEW VERTEX
POS E 0mm N -40.513801mm U 0mm
END
NEW VERTEX
POS E 35.08598mm N -20.2569mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 134.9
YLEN 730.3
ZLEN 76.2
POS E 42404.9 N 5013.3 U 88.1

-- Motor foot: pedestal web
NEW BOX
XLEN 68.0
YLEN 368.3
ZLEN 64.2
POS E 42404.9 N 5013.3 U 158.3

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 42440.121265mm N 5172.064728mm U 126.204844mm
ORI Y IS U AND Z IS N
HEIG 63.504037mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 70.382748mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.710512mm N 56.471801mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 42440.121265mm N 4791.040505mm U 126.204844mm
ORI Y IS U AND Z IS N
HEIG 63.504037mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 70.382748mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.710512mm N 56.471801mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 41.3
HEIG 117.5
ORI Z IS U AND Y IS N
POS E 42447.2 N 5013.3 U 88.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 42447.15954mm N 5013.304635mm U 126.204844mm
ORI Y IS N AND Z IS U
HEIG 33.022099mm

NEW LOOP
NEW VERTEX
POS E 35.08598mm N 20.2569mm U 0mm
END
NEW VERTEX
POS E 0mm N 40.513801mm U 0mm
END
NEW VERTEX
POS E -35.08598mm N 20.2569mm U 0mm
END
NEW VERTEX
POS E -35.08598mm N -20.2569mm U 0mm
END
NEW VERTEX
POS E 0mm N -40.513801mm U 0mm
END
NEW VERTEX
POS E 35.08598mm N -20.2569mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 41.3
HEIG 117.5
ORI Z IS U AND Y IS N
POS E 42362.7 N 5013.3 U 88.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 42362.700242mm N 5013.304635mm U 126.204844mm
ORI Y IS N AND Z IS U
HEIG 33.022099mm

NEW LOOP
NEW VERTEX
POS E 35.08598mm N 20.2569mm U 0mm
END
NEW VERTEX
POS E 0mm N 40.513801mm U 0mm
END
NEW VERTEX
POS E -35.08598mm N 20.2569mm U 0mm
END
NEW VERTEX
POS E -35.08598mm N -20.2569mm U 0mm
END
NEW VERTEX
POS E 0mm N -40.513801mm U 0mm
END
NEW VERTEX
POS E 35.08598mm N -20.2569mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 415.4
YLEN 372.8
ZLEN 38.9
POS E 43650.0 N 5016.0 U 69.5

-- Casing support: pedestal web
NEW BOX
XLEN 209.5
YLEN 188.0
ZLEN 151.3
POS E 43650.0 N 5016.0 U 164.5

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 43758.353185mm N 5097.051306mm U 88.904589mm
ORI Y IS U AND Z IS N
HEIG 32.420491mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 216.711588mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.191373mm N 133.129926mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 43758.353185mm N 4902.528363mm U 88.904589mm
ORI Y IS U AND Z IS N
HEIG 32.420491mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 216.711588mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.191373mm N 133.129926mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 21.1
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 43780.0 N 5016.0 U 69.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 43780.024344mm N 5016.00008mm U 88.904589mm
ORI Y IS N AND Z IS U
HEIG 16.858655mm

NEW LOOP
NEW VERTEX
POS E 17.912321mm N 10.341683mm U 0mm
END
NEW VERTEX
POS E 0mm N 20.683367mm U 0mm
END
NEW VERTEX
POS E -17.912321mm N 10.341683mm U 0mm
END
NEW VERTEX
POS E -17.912321mm N -10.341683mm U 0mm
END
NEW VERTEX
POS E 0mm N -20.683367mm U 0mm
END
NEW VERTEX
POS E 17.912321mm N -10.341683mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 21.1
HEIG 60.0
ORI Z IS U AND Y IS N
POS E 43520.0 N 5016.0 U 69.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 43519.970438mm N 5016.00008mm U 88.904589mm
ORI Y IS N AND Z IS U
HEIG 16.858655mm

NEW LOOP
NEW VERTEX
POS E 17.912321mm N 10.341683mm U 0mm
END
NEW VERTEX
POS E 0mm N 20.683367mm U 0mm
END
NEW VERTEX
POS E -17.912321mm N 10.341683mm U 0mm
END
NEW VERTEX
POS E -17.912321mm N -10.341683mm U 0mm
END
NEW VERTEX
POS E 0mm N -20.683367mm U 0mm
END
NEW VERTEX
POS E 17.912321mm N -10.341683mm U 0mm
END
END
END

NEW SUBE /205_PU_038_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 722x523 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 22B80D,22B80E,22B84D,22B843,22B844,22B80F ...
NEW CYLI
DIAM 522.9
HEIG 722.4
ORI Z IS W AND Y IS U
POS E 43650.0 N 5016.0 U 491.2

-- volute closing onto the suction cover
NEW CONE
DTOP 324.2
DBOT 522.9
HEIG 216.7
ORI Z IS W AND Y IS U
POS E 43180.5 N 5016.0 U 491.2

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 219.6
HEIG 130.0
ORI Z IS W AND Y IS U
POS E 44076.2 N 5016.0 U 491.2

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 375.6
ORI Z IS W AND Y IS U
POS E 43650.0 N 5284.7 U 491.2

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 375.6
ORI Z IS W AND Y IS U
POS E 43650.0 N 4747.3 U 491.2

NEW SUBE /205_PU_038_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 345 mm along the machine axis x 296 mm across, consolidated from 3 drawn sections (housing sections)
-- CAD handles: 22B812,22B800,22B811,22B804,22B7FB,22B7F8 ...
NEW CYLI
DIAM 296.5
HEIG 345.0
ORI Z IS W AND Y IS U
POS E 43143.3 N 5016.0 U 491.2

NEW SUBE /205_PU_038_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 49 mm apart running 59 mm along x, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22B7AC,22B7AD
NEW CYLI
DIAM 48.5
HEIG 59.3
ORI Z IS W AND Y IS U
POS E 43054.3 N 5016.0 U 491.2

-- Coupling hub (d=85) on the shaft centreline
NEW CYLI
DIAM 84.9
HEIG 13.0
ORI Z IS W AND Y IS U
POS E 43077.4 N 5016.0 U 491.2

-- Coupling hub (d=85) on the shaft centreline
NEW CYLI
DIAM 84.9
HEIG 13.0
ORI Z IS W AND Y IS U
POS E 43031.2 N 5016.0 U 491.2

NEW SUBE /205_PU_038_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 690 mm along the machine axis x 668 mm across, consolidated from 2 drawn sections (body, fin bands, cowl)
-- CAD handles: 22B861,22B85A,22B85B,22B85C,22B85D,22B85E ...
NEW CYLI
DIAM 668.5
HEIG 690.0
ORI Z IS W AND Y IS U
POS E 42625.7 N 5013.3 U 491.2

-- Motor end bell
NEW CYLI
DIAM 721.9
HEIG 41.4
ORI Z IS W AND Y IS U
POS E 42950.1 N 5013.3 U 491.2

-- Motor end bell
NEW CYLI
DIAM 721.9
HEIG 41.4
ORI Z IS W AND Y IS U
POS E 42301.4 N 5013.3 U 491.2

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 4671.1 U 491.2

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 4697.1 U 622.2

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 4771.3 U 733.2

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 4882.3 U 807.4

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 5013.3 U 833.4

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 5144.3 U 807.4

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 5255.3 U 733.2

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 5329.5 U 622.2

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 5355.5 U 491.2

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 5329.5 U 360.2

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 5255.3 U 249.2

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 5144.3 U 175.0

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 5013.3 U 149.0

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 4882.3 U 175.0

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 4771.3 U 249.2

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 496.8
ORI Z IS W AND Y IS U
POS E 42625.7 N 4697.1 U 360.2

-- Motor terminal box
NEW BOX
XLEN 207.0
YLEN 267.4
ZLEN 147.1
POS E 42625.7 N 5013.3 U 898.9

-- Motor cable gland
NEW CYLI
DIAM 50.0
HEIG 147.1
ORI Z IS N AND Y IS U
POS E 42625.7 N 4806.1 U 898.9

-- Reference Value: motor lifting lug
NEW BOX
XLEN 80.2
YLEN 46.8
ZLEN 66.8
POS E 42818.9 N 5013.3 U 906.3

-- Reference Value: motor nameplate
NEW BOX
XLEN 124.2
YLEN 86.9
ZLEN 6.0
POS E 42542.9 N 5349.5 U 491.2

-- Motor fan cowl disc
NEW CYLI
DIAM 735.3
HEIG 8.0
ORI Z IS W AND Y IS U
POS E 42974.8 N 5013.3 U 491.2

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 338.2
ZLEN 6.4
POS E 42974.8 N 5182.4 U 491.2

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 338.2
ZLEN 6.4
POS E 42974.8 N 4844.2 U 491.2

NEW SUBE /205_PU_038_AUXILIARY
-- 3 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: small fitting 70x59
-- CAD handles: 22970A,229712
NEW BOX
XLEN 70.1
YLEN 59.3
ZLEN 60.0
POS E 44078.6 N 5420.3 U 80.0

-- Auxiliary [LOW]: small fitting 75x135
-- CAD handles: 22B805,22B806,22B807
NEW BOX
XLEN 75.5
YLEN 134.8
ZLEN 60.4
POS E 43121.7 N 5016.0 U 80.2

-- Auxiliary [LOW]: small fitting 27x113
-- CAD handles: 22B7BD,22B7BE,22B7BF
NEW BOX
XLEN 27.0
YLEN 113.2
ZLEN 60.0
POS E 43011.2 N 5016.0 U 80.0

NEW SUBE /205_PU_038_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN150; POS is the flange face, contractual direction S
NEW NOZZLE /205_PU_038_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 43119.0 N 4514.4 U 491.2
ORI P1 IS S
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_038_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction W
NEW NOZZLE /205_PU_038_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 42083.0 N 5016.0 U 491.2
ORI P1 IS W
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-046
-- --------------------------------------------------------------------
-- 205-PU-046 - D1 WASHER FRONT DILUTION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-046
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 92 mm snapped to catalogue DN90 (nearest available in 'AAZFBB0MM'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_046
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_046_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 15221.0 N 14294.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 14886.6 N 13524.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 14886.6mm N 13524mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 14886.6 N 15064.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 14886.6mm N 15064mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 15555.4 N 13524.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 15555.4mm N 13524mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 15555.4 N 15064.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 15555.4mm N 15064mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /205_PU_046_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 257.5
YLEN 416.6
ZLEN 26.9
POS E 15221.0 N 14377.6 U 63.4

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 129.9
YLEN 210.1
ZLEN 73.9
POS E 15221.0 N 14377.6 U 113.8

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 15276.983919mm N 14268.878652mm U 76.872243mm
ORI Y IS U AND Z IS E
HEIG 22.393536mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 217.358504mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.547177mm N 65.016623mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 15142.622705mm N 14268.878652mm U 76.872243mm
ORI Y IS U AND Z IS E
HEIG 22.393536mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 217.358504mm N 0mm U 0mm
END
NEW VERTEX
POS E 119.547177mm N 65.016623mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 15221.0 N 14247.1 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 15221.00008mm N 14247.142801mm U 76.872243mm
ORI Y IS N AND Z IS U
HEIG 11.644639mm

NEW LOOP
NEW VERTEX
POS E 12.372428mm N 7.143225mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.28645mm U 0mm
END
NEW VERTEX
POS E -12.372428mm N 7.143225mm U 0mm
END
NEW VERTEX
POS E -12.372428mm N -7.143225mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.28645mm U 0mm
END
NEW VERTEX
POS E 12.372428mm N -7.143225mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 14.6
HEIG 41.4
ORI Z IS U AND Y IS N
POS E 15221.0 N 14508.0 U 63.4

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 15221.00008mm N 14507.973006mm U 76.872243mm
ORI Y IS N AND Z IS U
HEIG 11.644639mm

NEW LOOP
NEW VERTEX
POS E 12.372428mm N 7.143225mm U 0mm
END
NEW VERTEX
POS E 0mm N 14.28645mm U 0mm
END
NEW VERTEX
POS E -12.372428mm N 7.143225mm U 0mm
END
NEW VERTEX
POS E -12.372428mm N -7.143225mm U 0mm
END
NEW VERTEX
POS E 0mm N -14.28645mm U 0mm
END
NEW VERTEX
POS E 12.372428mm N -7.143225mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 435.8
YLEN 118.0
ZLEN 45.5
POS E 15218.3 N 13672.2 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 219.8
YLEN 59.5
ZLEN 38.3
POS E 15218.3 N 13672.2 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15313.048602mm N 13641.42857mm U 95.477104mm
ORI Y IS U AND Z IS E
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15085.663082mm N 13641.42857mm U 95.477104mm
ORI Y IS U AND Z IS E
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 15218.3 N 13635.3 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 15218.304635mm N 13635.27008mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 15218.3 N 13709.2 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 15218.304635mm N 13709.171958mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 435.8
YLEN 118.0
ZLEN 45.5
POS E 15218.3 N 14058.6 U 72.7

-- Motor foot: pedestal web
NEW BOX
XLEN 219.8
YLEN 59.5
ZLEN 38.3
POS E 15218.3 N 14058.6 U 114.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15313.048602mm N 14027.84362mm U 95.477104mm
ORI Y IS U AND Z IS E
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 15085.663082mm N 14027.84362mm U 95.477104mm
ORI Y IS U AND Z IS E
HEIG 37.897587mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 61.584899mm N 0mm U 0mm
END
NEW VERTEX
POS E 33.871694mm N 33.700928mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 15218.3 N 14021.7 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 15218.304635mm N 14021.685131mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 24.6
HEIG 70.1
ORI Z IS U AND Y IS N
POS E 15218.3 N 14095.6 U 72.7

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 15218.304635mm N 14095.587009mm U 95.477104mm
ORI Y IS N AND Z IS U
HEIG 19.706745mm

NEW LOOP
NEW VERTEX
POS E 20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N 24.177601mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N 12.0888mm U 0mm
END
NEW VERTEX
POS E -20.938417mm N -12.0888mm U 0mm
END
NEW VERTEX
POS E 0mm N -24.177601mm U 0mm
END
NEW VERTEX
POS E 20.938417mm N -12.0888mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 144.5
YLEN 72.3
ZLEN 15.1
POS E 15220.3 N 15006.3 U 57.5

-- Casing support: pedestal web
NEW BOX
XLEN 72.9
YLEN 36.4
ZLEN 150.9
POS E 15220.3 N 15006.3 U 140.5

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 15251.740703mm N 14987.415468mm U 65.078972mm
ORI Y IS U AND Z IS E
HEIG 12.56581mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.69743mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.733586mm N 132.814735mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 15176.345844mm N 14987.415468mm U 65.078972mm
ORI Y IS U AND Z IS E
HEIG 12.56581mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.69743mm N 0mm U 0mm
END
NEW VERTEX
POS E 20.733586mm N 132.814735mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 27.1
ORI Z IS U AND Y IS N
POS E 15220.3 N 14983.6 U 57.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 15220.326179mm N 14983.645725mm U 65.078972mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 27.1
ORI Z IS U AND Y IS N
POS E 15220.3 N 15028.9 U 57.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 15220.326179mm N 15028.882641mm U 65.078972mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /205_PU_046_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 101; the only large round feature in the plan, at the wet end
-- CAD handles: 231699,231699,231699,231699,231699,231699 ...
NEW CYLI
DIAM 202.7
HEIG 125.7
ORI Z IS U AND Y IS N
POS E 15220.3 N 15006.3 U 313.3

-- casing split flange at the cover joint
NEW CYLI
DIAM 222.9
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 15220.3 N 15006.3 U 384.1

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15220.3 N 15106.9 U 374.5

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 15220.326179mm N 15106.935077mm U 392.117546mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15149.1 N 15077.4 U 374.5

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 15149.141107mm N 15077.449255mm U 392.117546mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15119.7 N 15006.3 U 374.5

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 15119.655284mm N 15006.264183mm U 392.117546mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15149.1 N 14935.1 U 374.5

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 15149.141107mm N 14935.079111mm U 392.117546mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15220.3 N 14905.6 U 374.5

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 15220.326179mm N 14905.593288mm U 392.117546mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15291.5 N 14935.1 U 374.5

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 15291.511251mm N 14935.079111mm U 392.117546mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15321.0 N 15006.3 U 374.5

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 15320.997073mm N 15006.264183mm U 392.117546mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 15291.5 N 15077.4 U 374.5

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 15291.511251mm N 15077.449255mm U 392.117546mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 125.7
DBOT 202.7
HEIG 37.7
ORI Z IS N AND Y IS U
POS E 15220.3 N 15087.9 U 313.3

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 85.1
HEIG 22.6
ORI Z IS N AND Y IS U
POS E 15220.3 N 14932.1 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.1
HEIG 65.3
ORI Z IS N AND Y IS U
POS E 15325.3 N 15006.3 U 313.3

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.1
HEIG 65.3
ORI Z IS N AND Y IS U
POS E 15115.3 N 15006.3 U 313.3

NEW SUBE /205_PU_046_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 453 mm along the machine axis x 361 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 2316A9,2316A9,2316A9,23169A,23169A,23169A
NEW CYLI
DIAM 361.2
HEIG 452.8
ORI Z IS N AND Y IS U
POS E 15221.0 N 14377.6 U 313.3

NEW SUBE /205_PU_046_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 226 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 2316A4,2316A3
NEW CYLI
DIAM 134.8
HEIG 226.4
ORI Z IS N AND Y IS U
POS E 15221.0 N 14717.2 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 49.8
ORI Z IS N AND Y IS U
POS E 15221.0 N 14628.9 U 313.3

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 49.8
ORI Z IS N AND Y IS U
POS E 15221.0 N 14805.5 U 313.3

NEW SUBE /205_PU_046_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 604 mm along the machine axis x 399 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 2316A7,2316A7,2316A7,2316A8,2316A8,2316A8 ...
NEW CYLI
DIAM 398.9
HEIG 603.8
ORI Z IS N AND Y IS U
POS E 15218.3 N 13865.4 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS N AND Y IS U
POS E 15218.3 N 13581.7 U 313.3

-- Motor end bell
NEW CYLI
DIAM 430.8
HEIG 36.2
ORI Z IS N AND Y IS U
POS E 15218.3 N 14149.2 U 313.3

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15013.3 N 13865.4 U 313.3

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15028.9 N 13865.4 U 391.8

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15073.3 N 13865.4 U 458.3

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15139.8 N 13865.4 U 502.7

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15218.3 N 13865.4 U 518.3

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15296.8 N 13865.4 U 502.7

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15363.3 N 13865.4 U 458.3

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15407.7 N 13865.4 U 391.8

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15423.4 N 13865.4 U 313.3

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15407.7 N 13865.4 U 234.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15363.3 N 13865.4 U 168.3

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15296.8 N 13865.4 U 123.9

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15218.3 N 13865.4 U 108.2

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15139.8 N 13865.4 U 123.9

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15073.3 N 13865.4 U 168.3

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 11.2
HEIG 434.7
ORI Z IS N AND Y IS U
POS E 15028.9 N 13865.4 U 234.8

-- Motor terminal box
NEW BOX
XLEN 159.6
YLEN 181.1
ZLEN 87.8
POS E 15218.3 N 13865.4 U 556.6

-- Motor cable gland
NEW CYLI
DIAM 29.8
HEIG 87.8
ORI Z IS E AND Y IS U
POS E 15094.6 N 13865.4 U 556.6

-- Reference Value: motor lifting lug
NEW BOX
XLEN 27.9
YLEN 47.9
ZLEN 39.9
POS E 15218.3 N 13696.4 U 561.0

-- Reference Value: motor nameplate
NEW BOX
XLEN 51.9
YLEN 108.7
ZLEN 6.0
POS E 15419.8 N 13937.9 U 313.3

-- Motor fan cowl disc
NEW CYLI
DIAM 438.8
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 15218.3 N 13559.5 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 201.9
YLEN 9.6
ZLEN 6.4
POS E 15319.2 N 13559.5 U 313.3

-- Motor fan grille bar
NEW BOX
XLEN 201.9
YLEN 9.6
ZLEN 6.4
POS E 15117.4 N 13559.5 U 313.3

NEW SUBE /205_PU_046_AUXILIARY
-- 3 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 156x394 at the wet end, outboard of the casing
-- CAD handles: 2316A5,2316A5,2316A5,2316A2,2316A2,2316A2 ...
NEW BOX
XLEN 393.5
YLEN 156.3
ZLEN 125.1
POS E 15221.0 N 14908.6 U 112.5

-- Auxiliary [LOW]: body 124x447 at the wet end, outboard of the casing
-- CAD handles: 23169E,23169E,23169E,23169E,23169E,23169E ...
NEW BOX
XLEN 447.4
YLEN 124.0
ZLEN 99.2
POS E 15231.8 N 15016.4 U 99.6

-- Auxiliary [LOW]: body 27x199 at the wet end, outboard of the casing
-- CAD handles: 231696,231696,231696,231696
NEW BOX
XLEN 199.5
YLEN 27.0
ZLEN 60.0
POS E 15221.0 N 15118.8 U 80.0

NEW SUBE /205_PU_046_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN90; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_046_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0MM
POS E 15221.0 N 15133.8 U 313.3
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_046_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_046_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 15220.3 N 15006.3 U 526.1
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-047
-- --------------------------------------------------------------------
-- 205-PU-047 - D1 FILTRATE PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-047
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 221 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_047
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_047_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 863.0
YLEN 2129.0
ZLEN 50.0
POS E 46620.0 N 14089.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 46240.3 N 13114.5 U 69.4

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 46240.28mm N 13114.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 46240.3 N 15063.5 U 69.4

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 46240.28mm N 15063.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 46999.7 N 13114.5 U 69.4

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 46999.72mm N 13114.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 46999.7 N 15063.5 U 69.4

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 46999.72mm N 15063.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

NEW SUBE /205_PU_047_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 712.6
YLEN 186.5
ZLEN 74.4
POS E 46622.7 N 13260.8 U 87.2

-- Motor foot: pedestal web
NEW BOX
XLEN 359.4
YLEN 94.1
ZLEN 62.6
POS E 46622.7 N 13260.8 U 155.7

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 46777.614525mm N 13212.08892mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 46405.808541mm N 13212.08892mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 46622.7 N 13202.4 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 46622.695365mm N 13202.356305mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 46622.7 N 13319.1 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 46622.695365mm N 13319.147687mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 712.6
YLEN 186.5
ZLEN 74.4
POS E 46622.7 N 13871.4 U 87.2

-- Motor foot: pedestal web
NEW BOX
XLEN 359.4
YLEN 94.1
ZLEN 62.6
POS E 46622.7 N 13871.4 U 155.7

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 46777.614525mm N 13822.762813mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 46405.808541mm N 13822.762813mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 46622.7 N 13813.0 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 46622.695365mm N 13813.030198mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 46622.7 N 13929.8 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 46622.695365mm N 13929.82158mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 157.6
YLEN 401.7
ZLEN 16.4
POS E 46622.7 N 14261.5 U 58.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 79.5
YLEN 202.6
ZLEN 314.6
POS E 46622.7 N 14261.5 U 223.7

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 46656.954119mm N 14156.708926mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 276.85424mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 46574.733109mm N 14156.708926mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 276.85424mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 46622.7 N 14135.7 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 46622.695365mm N 14135.749356mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 46622.7 N 14387.3 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 46622.695365mm N 14387.264196mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 468.9
YLEN 132.4
ZLEN 48.9
POS E 46652.3 N 15005.4 U 74.5

-- Casing support: pedestal web
NEW BOX
XLEN 236.5
YLEN 66.8
ZLEN 65.9
POS E 46652.3 N 15005.4 U 131.9

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 46754.285715mm N 14970.913832mm U 98.931536mm
ORI Y IS U AND Z IS E
HEIG 40.77628mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.056603mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.981131mm N 57.98613mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 46509.628037mm N 14970.913832mm U 98.931536mm
ORI Y IS U AND Z IS E
HEIG 40.77628mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.056603mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.981131mm N 57.98613mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.5
HEIG 75.4
ORI Z IS U AND Y IS N
POS E 46652.3 N 14964.0 U 74.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 46652.345016mm N 14964.008171mm U 98.931536mm
ORI Y IS N AND Z IS U
HEIG 21.203665mm

NEW LOOP
NEW VERTEX
POS E 22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.014127mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N -13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.014127mm U 0mm
END
NEW VERTEX
POS E 22.528894mm N -13.007063mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.5
HEIG 75.4
ORI Z IS U AND Y IS N
POS E 46652.3 N 15046.9 U 74.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 46652.345016mm N 15046.876095mm U 98.931536mm
ORI Y IS N AND Z IS U
HEIG 21.203665mm

NEW LOOP
NEW VERTEX
POS E 22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.014127mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N -13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.014127mm U 0mm
END
NEW VERTEX
POS E 22.528894mm N -13.007063mm U 0mm
END
END
END

NEW SUBE /205_PU_047_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 210x658 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 231679,231679,231679,231679,231679,231679 ...
NEW CYLI
DIAM 657.7
HEIG 230.2
ORI Z IS N AND Y IS U
POS E 46652.3 N 15005.4 U 480.5

-- volute closing onto the suction cover
NEW CONE
DTOP 407.8
DBOT 657.7
HEIG 23.2
ORI Z IS N AND Y IS U
POS E 46652.3 N 15132.1 U 480.5

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 276.2
HEIG 41.4
ORI Z IS N AND Y IS U
POS E 46652.3 N 14869.6 U 480.5

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 119.7
ORI Z IS N AND Y IS U
POS E 46988.4 N 15005.4 U 480.5

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 119.7
ORI Z IS N AND Y IS U
POS E 46316.3 N 15005.4 U 480.5

NEW SUBE /205_PU_047_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 437x221 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 23166E,23166E,23166E
NEW CYLI
DIAM 221.0
HEIG 436.7
ORI Z IS N AND Y IS U
POS E 46622.7 N 14261.5 U 480.5

NEW SUBE /205_PU_047_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 199 mm apart running 248 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 231670,23166F
NEW CYLI
DIAM 199.5
HEIG 248.0
ORI Z IS N AND Y IS U
POS E 46622.7 N 14603.8 U 480.5

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 46622.7 N 14507.1 U 480.5

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 46622.7 N 14700.5 U 480.5

NEW SUBE /205_PU_047_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 954 mm along the machine axis x 652 mm across, consolidated from 2 drawn sections (body, fin bands, cowl)
-- CAD handles: 23167C,23167C,23167C,23167E,23167E,23167E ...
NEW CYLI
DIAM 652.3
HEIG 954.2
ORI Z IS N AND Y IS U
POS E 46622.7 N 13566.1 U 480.5

-- Motor end bell
NEW CYLI
DIAM 704.5
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 46622.7 N 13117.6 U 480.5

-- Motor end bell
NEW CYLI
DIAM 704.5
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 46622.7 N 14014.6 U 480.5

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46288.5 N 13566.1 U 480.5

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46314.0 N 13566.1 U 608.4

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46386.4 N 13566.1 U 716.8

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46494.8 N 13566.1 U 789.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46622.7 N 13566.1 U 814.7

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46750.6 N 13566.1 U 789.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46859.0 N 13566.1 U 716.8

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46931.4 N 13566.1 U 608.4

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46956.8 N 13566.1 U 480.5

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46931.4 N 13566.1 U 352.6

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46859.0 N 13566.1 U 244.2

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46750.6 N 13566.1 U 171.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46622.7 N 13566.1 U 146.4

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46494.8 N 13566.1 U 171.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46386.4 N 13566.1 U 244.2

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 46314.0 N 13566.1 U 352.6

-- Motor terminal box
NEW BOX
XLEN 260.9
YLEN 286.3
ZLEN 143.5
POS E 46622.7 N 13566.1 U 878.4

-- Motor cable gland
NEW CYLI
DIAM 48.8
HEIG 143.5
ORI Z IS E AND Y IS U
POS E 46420.5 N 13566.1 U 878.4

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.7
YLEN 78.3
ZLEN 65.2
POS E 46622.7 N 13298.9 U 885.6

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.8
YLEN 171.8
ZLEN 6.0
POS E 46950.8 N 13680.6 U 480.5

-- Motor fan cowl disc
NEW CYLI
DIAM 717.5
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 46622.7 N 13085.0 U 480.5

-- Motor fan grille bar
NEW BOX
XLEN 330.1
YLEN 9.6
ZLEN 6.4
POS E 46787.7 N 13085.0 U 480.5

-- Motor fan grille bar
NEW BOX
XLEN 330.1
YLEN 9.6
ZLEN 6.4
POS E 46457.7 N 13085.0 U 480.5

NEW SUBE /205_PU_047_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 173x334 at the wet end, outboard of the casing
-- CAD handles: 231671,231671,231671
NEW BOX
XLEN 334.2
YLEN 172.5
ZLEN 138.0
POS E 46620.0 N 14814.1 U 119.0

NEW SUBE /205_PU_047_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_047_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 46620.0 N 15154.0 U 480.5
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_047_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_047_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 46652.3 N 15005.4 U 959.4
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-048
-- --------------------------------------------------------------------
-- 205-PU-048 - D1 TOWER TOP DILUTION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-048
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 216 mm snapped to catalogue DN200 (nearest available in 'AAZFBB0TT'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_048
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_048_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 863.0
YLEN 2129.0
ZLEN 50.0
POS E 48221.0 N 14089.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 47841.3 N 13114.5 U 69.4

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 47841.28mm N 13114.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 47841.3 N 15063.5 U 69.4

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 47841.28mm N 15063.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 48600.7 N 13114.5 U 69.4

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 48600.72mm N 13114.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 25.9
HEIG 38.8
ORI Z IS U AND Y IS N
POS E 48600.7 N 15063.5 U 69.4

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 48600.72mm N 15063.5mm U 88.835mm
ORI Y IS N AND Z IS U
HEIG 20.712mm

NEW LOOP
NEW VERTEX
POS E 22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N 25.410917mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N 12.705459mm U 0mm
END
NEW VERTEX
POS E -22.0065mm N -12.705459mm U 0mm
END
NEW VERTEX
POS E 0mm N -25.410917mm U 0mm
END
NEW VERTEX
POS E 22.0065mm N -12.705459mm U 0mm
END
END
END

NEW SUBE /205_PU_048_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 712.6
YLEN 186.5
ZLEN 74.4
POS E 48223.7 N 13260.8 U 87.2

-- Motor foot: pedestal web
NEW BOX
XLEN 359.4
YLEN 94.1
ZLEN 62.6
POS E 48223.7 N 13260.8 U 155.7

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 48378.614525mm N 13212.08892mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 48006.808541mm N 13212.08892mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 48223.7 N 13202.4 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 48223.695365mm N 13202.356305mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 48223.7 N 13319.1 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 48223.695365mm N 13319.147687mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 712.6
YLEN 186.5
ZLEN 74.4
POS E 48223.7 N 13871.4 U 87.2

-- Motor foot: pedestal web
NEW BOX
XLEN 359.4
YLEN 94.1
ZLEN 62.6
POS E 48223.7 N 13871.4 U 155.7

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 48378.614525mm N 13822.762813mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 48006.808541mm N 13822.762813mm U 124.361197mm
ORI Y IS U AND Z IS E
HEIG 61.967664mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 97.326152mm N 0mm U 0mm
END
NEW VERTEX
POS E 53.529383mm N 55.105561mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 48223.7 N 13813.0 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 48223.695365mm N 13813.030198mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 48223.7 N 13929.8 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 48223.695365mm N 13929.82158mm U 124.361197mm
ORI Y IS N AND Z IS U
HEIG 32.223185mm

NEW LOOP
NEW VERTEX
POS E 34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533637mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N 19.766819mm U 0mm
END
NEW VERTEX
POS E -34.237134mm N -19.766819mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533637mm U 0mm
END
NEW VERTEX
POS E 34.237134mm N -19.766819mm U 0mm
END
END
END

-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 157.6
YLEN 401.7
ZLEN 16.4
POS E 48223.7 N 14261.5 U 58.2

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 79.5
YLEN 202.6
ZLEN 314.6
POS E 48223.7 N 14261.5 U 223.7

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 48257.954119mm N 14156.708926mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 276.85424mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 48175.733109mm N 14156.708926mm U 66.444202mm
ORI Y IS U AND Z IS E
HEIG 13.703502mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 209.595701mm N 0mm U 0mm
END
NEW VERTEX
POS E 115.277635mm N 276.85424mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 48223.7 N 14135.7 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 48223.695365mm N 14135.749356mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 28.4
ORI Z IS U AND Y IS N
POS E 48223.7 N 14387.3 U 58.2

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 48223.695365mm N 14387.264196mm U 66.444202mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 468.9
YLEN 132.4
ZLEN 48.9
POS E 48253.3 N 15005.4 U 74.5

-- Casing support: pedestal web
NEW BOX
XLEN 236.5
YLEN 66.8
ZLEN 65.9
POS E 48253.3 N 15005.4 U 131.9

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 48355.285715mm N 14970.913832mm U 98.931536mm
ORI Y IS U AND Z IS E
HEIG 40.77628mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.056603mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.981131mm N 57.98613mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 48110.628037mm N 14970.913832mm U 98.931536mm
ORI Y IS U AND Z IS E
HEIG 40.77628mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.056603mm N 0mm U 0mm
END
NEW VERTEX
POS E 37.981131mm N 57.98613mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.5
HEIG 75.4
ORI Z IS U AND Y IS N
POS E 48253.3 N 14964.0 U 74.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 48253.345016mm N 14964.008171mm U 98.931536mm
ORI Y IS N AND Z IS U
HEIG 21.203665mm

NEW LOOP
NEW VERTEX
POS E 22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.014127mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N -13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.014127mm U 0mm
END
NEW VERTEX
POS E 22.528894mm N -13.007063mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 26.5
HEIG 75.4
ORI Z IS U AND Y IS N
POS E 48253.3 N 15046.9 U 74.5

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 48253.345016mm N 15046.876095mm U 98.931536mm
ORI Y IS N AND Z IS U
HEIG 21.203665mm

NEW LOOP
NEW VERTEX
POS E 22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.014127mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N -13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.014127mm U 0mm
END
NEW VERTEX
POS E 22.528894mm N -13.007063mm U 0mm
END
END
END

NEW SUBE /205_PU_048_CASING
-- 5 part(s), 0 nozzle(s)
-- PumpCasing [MEDIUM]: compact body 210x658 at the wet end; no concentric circle group was drawn, so the volute envelope is taken from the largest compact wet-end body
-- CAD handles: 23168C,23168C,23168C,23168C,23168C,23168C ...
NEW CYLI
DIAM 657.7
HEIG 230.2
ORI Z IS N AND Y IS U
POS E 48253.3 N 15005.4 U 480.5

-- volute closing onto the suction cover
NEW CONE
DTOP 407.8
DBOT 657.7
HEIG 23.2
ORI Z IS N AND Y IS U
POS E 48253.3 N 15132.1 U 480.5

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 276.2
HEIG 41.4
ORI Z IS N AND Y IS U
POS E 48253.3 N 14869.6 U 480.5

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 119.7
ORI Z IS N AND Y IS U
POS E 48589.4 N 15005.4 U 480.5

-- Reference Value: axial casing rib
NEW CYLI
DIAM 18.0
HEIG 119.7
ORI Z IS N AND Y IS U
POS E 47917.3 N 15005.4 U 480.5

NEW SUBE /205_PU_048_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [MEDIUM]: body 437x221 between the driver and the coupling, the bearing/adapter position
-- CAD handles: 231681,231681,231681
NEW CYLI
DIAM 221.0
HEIG 436.7
ORI Z IS N AND Y IS U
POS E 48223.7 N 14261.5 U 480.5

NEW SUBE /205_PU_048_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 199 mm apart running 248 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 231683,231682
NEW CYLI
DIAM 199.5
HEIG 248.0
ORI Z IS N AND Y IS U
POS E 48223.7 N 14603.8 U 480.5

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 48223.7 N 14507.1 U 480.5

-- Coupling hub (d=349) on the shaft centreline
NEW CYLI
DIAM 349.1
HEIG 54.6
ORI Z IS N AND Y IS U
POS E 48223.7 N 14700.5 U 480.5

NEW SUBE /205_PU_048_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 954 mm along the machine axis x 652 mm across, consolidated from 2 drawn sections (body, fin bands, cowl)
-- CAD handles: 23168F,23168F,23168F,231691,231691,231691 ...
NEW CYLI
DIAM 652.3
HEIG 954.2
ORI Z IS N AND Y IS U
POS E 48223.7 N 13566.1 U 480.5

-- Motor end bell
NEW CYLI
DIAM 704.5
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 48223.7 N 13117.6 U 480.5

-- Motor end bell
NEW CYLI
DIAM 704.5
HEIG 57.3
ORI Z IS N AND Y IS U
POS E 48223.7 N 14014.6 U 480.5

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 47889.5 N 13566.1 U 480.5

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 47915.0 N 13566.1 U 608.4

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 47987.4 N 13566.1 U 716.8

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48095.8 N 13566.1 U 789.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48223.7 N 13566.1 U 814.7

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48351.6 N 13566.1 U 789.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48460.0 N 13566.1 U 716.8

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48532.4 N 13566.1 U 608.4

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48557.8 N 13566.1 U 480.5

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48532.4 N 13566.1 U 352.6

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48460.0 N 13566.1 U 244.2

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48351.6 N 13566.1 U 171.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48223.7 N 13566.1 U 146.4

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 48095.8 N 13566.1 U 171.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 47987.4 N 13566.1 U 244.2

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 687.0
ORI Z IS N AND Y IS U
POS E 47915.0 N 13566.1 U 352.6

-- Motor terminal box
NEW BOX
XLEN 260.9
YLEN 286.3
ZLEN 143.5
POS E 48223.7 N 13566.1 U 878.4

-- Motor cable gland
NEW CYLI
DIAM 48.8
HEIG 143.5
ORI Z IS E AND Y IS U
POS E 48021.5 N 13566.1 U 878.4

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.7
YLEN 78.3
ZLEN 65.2
POS E 48223.7 N 13298.9 U 885.6

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.8
YLEN 171.8
ZLEN 6.0
POS E 48551.8 N 13680.6 U 480.5

-- Motor fan cowl disc
NEW CYLI
DIAM 717.5
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 48223.7 N 13085.0 U 480.5

-- Motor fan grille bar
NEW BOX
XLEN 330.1
YLEN 9.6
ZLEN 6.4
POS E 48388.7 N 13085.0 U 480.5

-- Motor fan grille bar
NEW BOX
XLEN 330.1
YLEN 9.6
ZLEN 6.4
POS E 48058.7 N 13085.0 U 480.5

NEW SUBE /205_PU_048_AUXILIARY
-- 1 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 173x334 at the wet end, outboard of the casing
-- CAD handles: 231684,231684,231684
NEW BOX
XLEN 334.2
YLEN 172.5
ZLEN 138.0
POS E 48221.0 N 14814.1 U 119.0

NEW SUBE /205_PU_048_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN200; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_048_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT
POS E 48221.0 N 15154.0 U 480.5
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_048_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_048_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 48253.3 N 15005.4 U 959.4
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-049
-- --------------------------------------------------------------------
-- 205-PU-049 - D1 WASHER WIRE WASH PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-049
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 113 mm snapped to catalogue DN125 (nearest available in 'AAZFBB0PP'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_049
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_049_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 760.0
YLEN 1720.0
ZLEN 50.0
POS E 49674.0 N 14294.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 49339.6 N 13524.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 49339.6mm N 13524mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 49339.6 N 15064.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 49339.6mm N 15064mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 50008.4 N 13524.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 50008.4mm N 13524mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 50008.4 N 15064.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 50008.4mm N 15064mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /205_PU_049_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 307.5
YLEN 376.9
ZLEN 32.1
POS E 49671.3 N 14415.3 U 66.0

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 155.1
YLEN 190.1
ZLEN 122.5
POS E 49671.3 N 14415.3 U 143.3

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 49738.150913mm N 14316.964986mm U 82.086251mm
ORI Y IS U AND Z IS E
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.657643mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161704mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 49577.719655mm N 14316.964986mm U 82.086251mm
ORI Y IS U AND Z IS E
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.657643mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161704mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 49671.3 N 14297.3 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 49671.304556mm N 14297.299222mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 49671.3 N 14533.3 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 49671.304556mm N 14533.288394mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 577.2
YLEN 132.8
ZLEN 60.2
POS E 49671.3 N 13664.2 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 291.1
YLEN 67.0
ZLEN 50.7
POS E 49671.3 N 13664.2 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 49796.776249mm N 13629.601036mm U 110.226413mm
ORI Y IS U AND Z IS E
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 49495.644185mm N 13629.601036mm U 110.226413mm
ORI Y IS U AND Z IS E
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 49671.3 N 13622.7 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 49671.304556mm N 13622.672734mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 49671.3 N 13705.8 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 49671.304556mm N 13705.812362mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 577.2
YLEN 132.8
ZLEN 60.2
POS E 49671.3 N 14099.0 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 291.1
YLEN 67.0
ZLEN 50.7
POS E 49671.3 N 14099.0 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 49796.776249mm N 14064.318045mm U 110.226413mm
ORI Y IS U AND Z IS E
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 49495.644185mm N 14064.318045mm U 110.226413mm
ORI Y IS U AND Z IS E
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 49671.3 N 14057.4 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 49671.304556mm N 14057.389742mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 49671.3 N 14140.5 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 49671.304556mm N 14140.52937mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 132.9
YLEN 66.5
ZLEN 13.9
POS E 49671.3 N 15006.3 U 56.9

-- Casing support: pedestal web
NEW BOX
XLEN 67.0
YLEN 33.5
ZLEN 245.3
POS E 49671.3 N 15006.3 U 186.5

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 49700.198963mm N 14988.927574mm U 63.869287mm
ORI Y IS U AND Z IS E
HEIG 11.557739mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.673217mm N 0mm U 0mm
END
NEW VERTEX
POS E 19.07027mm N 215.890994mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 49630.852528mm N 14988.927574mm U 63.869287mm
ORI Y IS U AND Z IS E
HEIG 11.557739mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.673217mm N 0mm U 0mm
END
NEW VERTEX
POS E 19.07027mm N 215.890994mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.9
ORI Z IS U AND Y IS N
POS E 49671.3 N 14985.5 U 56.9

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 49671.304615mm N 14985.460252mm U 63.869287mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.9
ORI Z IS U AND Y IS N
POS E 49671.3 N 15027.1 U 56.9

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 49671.304615mm N 15027.068113mm U 63.869287mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /205_PU_049_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 93; the only large round feature in the plan, at the wet end
-- CAD handles: 2316C0,2316C0,2316C0,2316C0,2316C0,2316C0 ...
NEW CYLI
DIAM 186.4
HEIG 115.6
ORI Z IS U AND Y IS N
POS E 49671.3 N 15006.3 U 398.7

-- casing split flange at the cover joint
NEW CYLI
DIAM 205.1
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 49671.3 N 15006.3 U 464.5

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 49671.3 N 15098.0 U 454.9

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 49671.304615mm N 15097.992514mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 49606.4 N 15071.1 U 454.9

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 49606.44289mm N 15071.125908mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 49579.6 N 15006.3 U 454.9

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 49579.576284mm N 15006.264183mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 49606.4 N 14941.4 U 454.9

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 49606.44289mm N 14941.402458mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 49671.3 N 14914.5 U 454.9

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 49671.304615mm N 14914.535852mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 49736.2 N 14941.4 U 454.9

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 49736.16634mm N 14941.402458mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 49763.0 N 15006.3 U 454.9

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 49763.032946mm N 15006.264183mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 49736.2 N 15071.1 U 454.9

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 49736.16634mm N 15071.125908mm U 472.467928mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 115.6
DBOT 186.4
HEIG 34.7
ORI Z IS N AND Y IS U
POS E 49671.3 N 15081.4 U 398.7

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 78.3
HEIG 20.8
ORI Z IS N AND Y IS U
POS E 49671.3 N 14938.1 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 60.1
ORI Z IS N AND Y IS U
POS E 49768.1 N 15006.3 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 60.1
ORI Z IS N AND Y IS U
POS E 49574.5 N 15006.3 U 398.7

NEW SUBE /205_PU_049_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 410 mm along the machine axis x 431 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 2316C8,2316C8,2316C8,2316B5,2316B5,2316B5
NEW CYLI
DIAM 431.3
HEIG 409.7
ORI Z IS N AND Y IS U
POS E 49671.3 N 14415.3 U 398.7

NEW SUBE /205_PU_049_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 210 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 2316B7,2316B6
NEW CYLI
DIAM 134.8
HEIG 210.2
ORI Z IS N AND Y IS U
POS E 49674.0 N 14725.3 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS N AND Y IS U
POS E 49674.0 N 14643.3 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS N AND Y IS U
POS E 49674.0 N 14807.3 U 398.7

NEW SUBE /205_PU_049_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 679 mm along the machine axis x 528 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 2316C6,2316C6,2316C6,2316C7,2316C7,2316C7 ...
NEW CYLI
DIAM 528.3
HEIG 679.2
ORI Z IS N AND Y IS U
POS E 49671.3 N 13881.6 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS N AND Y IS U
POS E 49671.3 N 13562.4 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS N AND Y IS U
POS E 49671.3 N 14200.8 U 398.7

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49399.8 N 13881.6 U 398.7

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49420.4 N 13881.6 U 502.6

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49479.3 N 13881.6 U 590.7

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49567.4 N 13881.6 U 649.6

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49671.3 N 13881.6 U 670.2

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49775.2 N 13881.6 U 649.6

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49863.3 N 13881.6 U 590.7

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49922.2 N 13881.6 U 502.6

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49942.9 N 13881.6 U 398.7

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49922.2 N 13881.6 U 294.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49863.3 N 13881.6 U 206.7

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49775.2 N 13881.6 U 147.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49671.3 N 13881.6 U 127.1

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49567.4 N 13881.6 U 147.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49479.3 N 13881.6 U 206.7

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS N AND Y IS U
POS E 49420.4 N 13881.6 U 294.8

-- Motor terminal box
NEW BOX
XLEN 211.3
YLEN 203.8
ZLEN 116.2
POS E 49671.3 N 13881.6 U 720.9

-- Motor cable gland
NEW CYLI
DIAM 39.5
HEIG 116.2
ORI Z IS E AND Y IS U
POS E 49507.5 N 13881.6 U 720.9

-- Reference Value: motor lifting lug
NEW BOX
XLEN 37.0
YLEN 63.4
ZLEN 52.8
POS E 49671.3 N 13691.4 U 726.8

-- Reference Value: motor nameplate
NEW BOX
XLEN 68.7
YLEN 122.3
ZLEN 6.0
POS E 49937.5 N 13963.1 U 398.7

-- Motor fan cowl disc
NEW CYLI
DIAM 581.1
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 49671.3 N 13538.0 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 267.3
YLEN 9.6
ZLEN 6.4
POS E 49805.0 N 13538.0 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 267.3
YLEN 9.6
ZLEN 6.4
POS E 49537.6 N 13538.0 U 398.7

NEW SUBE /205_PU_049_AUXILIARY
-- 2 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 259x356 at the wet end, outboard of the casing
-- CAD handles: 2316B8,2316B8,2316B8,2316B4,2316B4,2316B3 ...
NEW BOX
XLEN 355.8
YLEN 258.8
ZLEN 207.0
POS E 49682.1 N 14959.8 U 153.5

-- Auxiliary [LOW]: body 22x221 at the wet end, outboard of the casing
-- CAD handles: 2316BD,2316BD,2316BD,2316BD
NEW BOX
XLEN 221.0
YLEN 21.6
ZLEN 60.0
POS E 49674.0 N 15121.5 U 80.0

NEW SUBE /205_PU_049_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN125; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_049_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0PP
POS E 49674.0 N 15133.8 U 398.7
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_049_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_049_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 49671.3 N 15006.3 U 606.5
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-054
-- --------------------------------------------------------------------
-- 205-PU-054 - D1 STAGE MC PUMP (205-PU-054/MC PUMP)
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-054
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 173 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_054
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_054_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 1046.0
YLEN 2000.0
ZLEN 50.0
POS E 48852.0 N 4714.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 31.4
HEIG 47.1
ORI Z IS U AND Y IS N
POS E 48391.8 N 3804.0 U 73.5

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 48391.76mm N 3804mm U 97.07mm
ORI Y IS N AND Z IS U
HEIG 25.104mm

NEW LOOP
NEW VERTEX
POS E 26.673mm N 15.399664mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.799327mm U 0mm
END
NEW VERTEX
POS E -26.673mm N 15.399664mm U 0mm
END
NEW VERTEX
POS E -26.673mm N -15.399664mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.799327mm U 0mm
END
NEW VERTEX
POS E 26.673mm N -15.399664mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 31.4
HEIG 47.1
ORI Z IS U AND Y IS N
POS E 48391.8 N 5624.0 U 73.5

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 48391.76mm N 5624mm U 97.07mm
ORI Y IS N AND Z IS U
HEIG 25.104mm

NEW LOOP
NEW VERTEX
POS E 26.673mm N 15.399664mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.799327mm U 0mm
END
NEW VERTEX
POS E -26.673mm N 15.399664mm U 0mm
END
NEW VERTEX
POS E -26.673mm N -15.399664mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.799327mm U 0mm
END
NEW VERTEX
POS E 26.673mm N -15.399664mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 31.4
HEIG 47.1
ORI Z IS U AND Y IS N
POS E 49312.2 N 3804.0 U 73.5

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 49312.24mm N 3804mm U 97.07mm
ORI Y IS N AND Z IS U
HEIG 25.104mm

NEW LOOP
NEW VERTEX
POS E 26.673mm N 15.399664mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.799327mm U 0mm
END
NEW VERTEX
POS E -26.673mm N 15.399664mm U 0mm
END
NEW VERTEX
POS E -26.673mm N -15.399664mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.799327mm U 0mm
END
NEW VERTEX
POS E 26.673mm N -15.399664mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 31.4
HEIG 47.1
ORI Z IS U AND Y IS N
POS E 49312.2 N 5624.0 U 73.5

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 49312.24mm N 5624mm U 97.07mm
ORI Y IS N AND Z IS U
HEIG 25.104mm

NEW LOOP
NEW VERTEX
POS E 26.673mm N 15.399664mm U 0mm
END
NEW VERTEX
POS E 0mm N 30.799327mm U 0mm
END
NEW VERTEX
POS E -26.673mm N 15.399664mm U 0mm
END
NEW VERTEX
POS E -26.673mm N -15.399664mm U 0mm
END
NEW VERTEX
POS E 0mm N -30.799327mm U 0mm
END
NEW VERTEX
POS E 26.673mm N -15.399664mm U 0mm
END
END
END

NEW SUBE /205_PU_054_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 468.9
YLEN 243.0
ZLEN 48.9
POS E 48922.1 N 4816.4 U 74.5

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 236.5
YLEN 122.6
ZLEN 85.6
POS E 48922.1 N 4816.4 U 141.7

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 49024.021619mm N 4753.029651mm U 98.931536mm
ORI Y IS U AND Z IS E
HEIG 40.77628mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 126.79241mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.735825mm N 75.348841mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 48779.363941mm N 4753.029651mm U 98.931536mm
ORI Y IS U AND Z IS E
HEIG 40.77628mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 126.79241mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.735825mm N 75.348841mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 26.5
HEIG 75.4
ORI Z IS U AND Y IS N
POS E 48922.1 N 4740.4 U 74.5

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 48922.08092mm N 4740.35041mm U 98.931536mm
ORI Y IS N AND Z IS U
HEIG 21.203665mm

NEW LOOP
NEW VERTEX
POS E 22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.014127mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N -13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.014127mm U 0mm
END
NEW VERTEX
POS E 22.528894mm N -13.007063mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 26.5
HEIG 75.4
ORI Z IS U AND Y IS N
POS E 48922.1 N 4892.5 U 74.5

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 48922.08092mm N 4892.501302mm U 98.931536mm
ORI Y IS N AND Z IS U
HEIG 21.203665mm

NEW LOOP
NEW VERTEX
POS E 22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N 26.014127mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N 13.007063mm U 0mm
END
NEW VERTEX
POS E -22.528894mm N -13.007063mm U 0mm
END
NEW VERTEX
POS E 0mm N -26.014127mm U 0mm
END
NEW VERTEX
POS E 22.528894mm N -13.007063mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 712.6
YLEN 189.7
ZLEN 74.4
POS E 48935.6 N 3888.7 U 87.2

-- Motor foot: pedestal web
NEW BOX
XLEN 359.4
YLEN 95.7
ZLEN 62.6
POS E 48935.6 N 3888.7 U 155.7

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 49090.477105mm N 3839.175173mm U 124.361179mm
ORI Y IS U AND Z IS E
HEIG 61.967649mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 98.975748mm N 0mm U 0mm
END
NEW VERTEX
POS E 54.436661mm N 55.105547mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 48718.671212mm N 3839.175173mm U 124.361179mm
ORI Y IS U AND Z IS E
HEIG 61.967649mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 98.975748mm N 0mm U 0mm
END
NEW VERTEX
POS E 54.436661mm N 55.105547mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 48935.6 N 3829.3 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 48935.557983mm N 3829.277599mm U 124.361179mm
ORI Y IS N AND Z IS U
HEIG 32.223177mm

NEW LOOP
NEW VERTEX
POS E 34.237126mm N 19.766814mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533628mm U 0mm
END
NEW VERTEX
POS E -34.237126mm N 19.766814mm U 0mm
END
NEW VERTEX
POS E -34.237126mm N -19.766814mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533628mm U 0mm
END
NEW VERTEX
POS E 34.237126mm N -19.766814mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 48935.6 N 3948.0 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 48935.557983mm N 3948.048496mm U 124.361179mm
ORI Y IS N AND Z IS U
HEIG 32.223177mm

NEW LOOP
NEW VERTEX
POS E 34.237126mm N 19.766814mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533628mm U 0mm
END
NEW VERTEX
POS E -34.237126mm N 19.766814mm U 0mm
END
NEW VERTEX
POS E -34.237126mm N -19.766814mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533628mm U 0mm
END
NEW VERTEX
POS E 34.237126mm N -19.766814mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 712.6
YLEN 189.7
ZLEN 74.4
POS E 48935.6 N 4509.7 U 87.2

-- Motor foot: pedestal web
NEW BOX
XLEN 359.4
YLEN 95.7
ZLEN 62.6
POS E 48935.6 N 4509.7 U 155.7

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 49090.477105mm N 4460.199471mm U 124.361179mm
ORI Y IS U AND Z IS E
HEIG 61.967649mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 98.975748mm N 0mm U 0mm
END
NEW VERTEX
POS E 54.436661mm N 55.105547mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 48718.671212mm N 4460.199471mm U 124.361179mm
ORI Y IS U AND Z IS E
HEIG 61.967649mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 98.975748mm N 0mm U 0mm
END
NEW VERTEX
POS E 54.436661mm N 55.105547mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 48935.6 N 4450.3 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 48935.557983mm N 4450.301897mm U 124.361179mm
ORI Y IS N AND Z IS U
HEIG 32.223177mm

NEW LOOP
NEW VERTEX
POS E 34.237126mm N 19.766814mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533628mm U 0mm
END
NEW VERTEX
POS E -34.237126mm N 19.766814mm U 0mm
END
NEW VERTEX
POS E -34.237126mm N -19.766814mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533628mm U 0mm
END
NEW VERTEX
POS E 34.237126mm N -19.766814mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 40.3
HEIG 114.6
ORI Z IS U AND Y IS N
POS E 48935.6 N 4569.1 U 87.2

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 48935.557983mm N 4569.072794mm U 124.361179mm
ORI Y IS N AND Z IS U
HEIG 32.223177mm

NEW LOOP
NEW VERTEX
POS E 34.237126mm N 19.766814mm U 0mm
END
NEW VERTEX
POS E 0mm N 39.533628mm U 0mm
END
NEW VERTEX
POS E -34.237126mm N 19.766814mm U 0mm
END
NEW VERTEX
POS E -34.237126mm N -19.766814mm U 0mm
END
NEW VERTEX
POS E 0mm N -39.533628mm U 0mm
END
NEW VERTEX
POS E 34.237126mm N -19.766814mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 103.8
YLEN 51.9
ZLEN 10.8
POS E 48914.0 N 5441.8 U 55.4

-- Casing support: pedestal web
NEW BOX
XLEN 52.3
YLEN 26.2
ZLEN 349.8
POS E 48914.0 N 5441.8 U 235.7

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 48936.558253mm N 5428.22459mm U 60.83056mm
ORI Y IS U AND Z IS E
HEIG 9.025467mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 27.0764mm N 0mm U 0mm
END
NEW VERTEX
POS E 14.89202mm N 307.830114mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 48882.405454mm N 5428.22459mm U 60.83056mm
ORI Y IS U AND Z IS E
HEIG 9.025467mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 27.0764mm N 0mm U 0mm
END
NEW VERTEX
POS E 14.89202mm N 307.830114mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 22.8
ORI Z IS U AND Y IS N
POS E 48914.0 N 5425.5 U 55.4

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 48913.994587mm N 5425.51695mm U 60.83056mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 22.8
ORI Z IS U AND Y IS N
POS E 48914.0 N 5458.0 U 55.4

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 48913.994587mm N 5458.008629mm U 60.83056mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /205_PU_054_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 1 concentric circle(s) on one axis, radii 73; the only large round feature in the plan, at the wet end
-- CAD handles: 229557,229548,229549,22954A,22954B,22954C ...
NEW CYLI
DIAM 145.6
HEIG 90.3
ORI Z IS U AND Y IS N
POS E 48914.0 N 5441.8 U 480.5

-- casing split flange at the cover joint
NEW CYLI
DIAM 160.1
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 48914.0 N 5441.8 U 533.6

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 48914.0 N 5511.0 U 524.0

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 48913.994587mm N 5511.027412mm U 541.639419mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 48865.0 N 5490.7 U 524.0

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 48865.017102mm N 5490.740274mm U 541.639419mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 48844.7 N 5441.8 U 524.0

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 48844.729964mm N 5441.76279mm U 541.639419mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 48865.0 N 5392.8 U 524.0

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 48865.017102mm N 5392.785305mm U 541.639419mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 48914.0 N 5372.5 U 524.0

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 48913.994587mm N 5372.498167mm U 541.639419mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 48963.0 N 5392.8 U 524.0

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 48962.972071mm N 5392.785305mm U 541.639419mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 48983.3 N 5441.8 U 524.0

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 48983.259209mm N 5441.76279mm U 541.639419mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 48963.0 N 5490.7 U 524.0

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 48962.972071mm N 5490.740274mm U 541.639419mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 90.3
DBOT 145.6
HEIG 27.1
ORI Z IS N AND Y IS U
POS E 48914.0 N 5500.4 U 480.5

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 61.1
HEIG 16.2
ORI Z IS N AND Y IS U
POS E 48914.0 N 5388.5 U 480.5

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 46.9
ORI Z IS N AND Y IS U
POS E 48990.4 N 5441.8 U 480.5

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 46.9
ORI Z IS N AND Y IS U
POS E 48837.6 N 5441.8 U 480.5

NEW SUBE /205_PU_054_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 264 mm along the machine axis x 658 mm across, consolidated from 3 drawn sections (housing sections)
-- CAD handles: 22B6F1,22B6EF,22B6F0,22B635,22B636,22B637 ...
NEW CYLI
DIAM 657.7
HEIG 264.2
ORI Z IS N AND Y IS U
POS E 48922.1 N 4816.4 U 480.5

NEW SUBE /205_PU_054_COUPLING
-- 6 part(s), 0 nozzle(s)
-- CouplingGuard [MEDIUM]: body 113x302 spanning the gap between driver and wet end, the coupling guard position
-- CAD handles: 22B69A,22B684,22B699,22B688
NEW BOX
XLEN 301.9
YLEN 113.2
ZLEN 301.9
POS E 48922.1 N 5005.1 U 480.5

-- Coupling guard end plate
NEW CYLI
DIAM 277.7
HEIG 24.2
ORI Z IS N AND Y IS U
POS E 48922.1 N 4960.6 U 480.5

-- Coupling guard end plate
NEW CYLI
DIAM 277.7
HEIG 24.2
ORI Z IS N AND Y IS U
POS E 48922.1 N 5049.6 U 480.5

-- Coupling [HIGH]: shaft/coupling: parallel rail pair 54 mm apart running 59 mm along y, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22B622,22B623
NEW CYLI
DIAM 53.9
HEIG 59.3
ORI Z IS N AND Y IS U
POS E 48922.1 N 4794.9 U 480.5

-- Coupling hub (d=94) on the shaft centreline
NEW CYLI
DIAM 94.3
HEIG 13.0
ORI Z IS N AND Y IS U
POS E 48922.1 N 4771.7 U 480.5

-- Coupling hub (d=94) on the shaft centreline
NEW CYLI
DIAM 94.3
HEIG 13.0
ORI Z IS N AND Y IS U
POS E 48922.1 N 4818.0 U 480.5

NEW SUBE /205_PU_054_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: large body 970 mm along the machine axis at the driver end, spanning 652 mm across the baseplate (2 drawn feature(s) merged)
-- CAD handles: 22B62A,22B62B,22B627,22B628,22B629,22B624 ...
NEW CYLI
DIAM 652.3
HEIG 970.4
ORI Z IS N AND Y IS U
POS E 48935.6 N 4199.2 U 480.5

-- Motor end bell
NEW CYLI
DIAM 704.5
HEIG 58.2
ORI Z IS N AND Y IS U
POS E 48935.6 N 3743.1 U 480.5

-- Motor end bell
NEW CYLI
DIAM 704.5
HEIG 58.2
ORI Z IS N AND Y IS U
POS E 48935.6 N 4655.2 U 480.5

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 48601.4 N 4199.2 U 480.5

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 48626.8 N 4199.2 U 608.4

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 48699.3 N 4199.2 U 716.8

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 48807.7 N 4199.2 U 789.2

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 48935.6 N 4199.2 U 814.7

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 49063.4 N 4199.2 U 789.2

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 49171.8 N 4199.2 U 716.8

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 49244.3 N 4199.2 U 608.4

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 49269.7 N 4199.2 U 480.5

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 49244.3 N 4199.2 U 352.6

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 49171.8 N 4199.2 U 244.2

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 49063.4 N 4199.2 U 171.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 48935.6 N 4199.2 U 146.4

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 48807.7 N 4199.2 U 171.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 48699.3 N 4199.2 U 244.2

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 16.0
HEIG 698.7
ORI Z IS N AND Y IS U
POS E 48626.8 N 4199.2 U 352.6

-- Motor terminal box
NEW BOX
XLEN 260.9
YLEN 291.1
ZLEN 143.5
POS E 48935.6 N 4199.2 U 878.4

-- Motor cable gland
NEW CYLI
DIAM 48.8
HEIG 143.5
ORI Z IS E AND Y IS U
POS E 48733.3 N 4199.2 U 878.4

-- Reference Value: motor lifting lug
NEW BOX
XLEN 45.7
YLEN 78.3
ZLEN 65.2
POS E 48935.6 N 3927.5 U 885.6

-- Reference Value: motor nameplate
NEW BOX
XLEN 84.8
YLEN 174.7
ZLEN 6.0
POS E 49263.7 N 4315.6 U 480.5

-- Motor fan cowl disc
NEW CYLI
DIAM 717.5
HEIG 8.0
ORI Z IS N AND Y IS U
POS E 48935.6 N 3710.0 U 480.5

-- Motor fan grille bar
NEW BOX
XLEN 330.1
YLEN 9.6
ZLEN 6.4
POS E 49100.6 N 3710.0 U 480.5

-- Motor fan grille bar
NEW BOX
XLEN 330.1
YLEN 9.6
ZLEN 6.4
POS E 48770.5 N 3710.0 U 480.5

NEW SUBE /205_PU_054_AUXILIARY
-- 2 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: small fitting 140x75
-- CAD handles: 22B689,22B68A,22B68B
NEW BOX
XLEN 140.2
YLEN 75.5
ZLEN 60.4
POS E 48922.1 N 4862.2 U 80.2

-- Auxiliary [LOW]: body 631x496 at the wet end, outboard of the casing
-- CAD handles: 22B66E,22B66F,22B670,22B671,22B66A,22B66B ...
NEW BOX
XLEN 496.0
YLEN 630.7
ZLEN 396.8
POS E 48922.1 N 5344.7 U 248.4

NEW SUBE /205_PU_054_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN150; POS is the flange face, contractual direction N
NEW NOZZLE /205_PU_054_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 48852.0 N 5750.0 U 480.5
ORI P1 IS N
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_054_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_054_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 48914.0 N 5441.8 U 675.6
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-060
-- --------------------------------------------------------------------
-- 205-PU-060 - SCRUBBER CIRCULATION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-060
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: E (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 113 mm snapped to catalogue DN125 (nearest available in 'AAZFBB0PP'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_060
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_060_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 1720.0
YLEN 760.0
ZLEN 50.0
POS E 46154.0 N -10854.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 45384.0 N -11158.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 45384mm N -11158mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 45384.0 N -10550.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 45384mm N -10550mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 46924.0 N -11158.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 46924mm N -11158mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 46924.0 N -10550.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 46924mm N -10550mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /205_PU_060_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 376.9
YLEN 307.5
ZLEN 32.1
POS E 46275.3 N -10856.7 U 66.0

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 190.1
YLEN 155.1
ZLEN 122.5
POS E 46275.3 N -10856.7 U 143.3

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 46176.964948mm N -10923.541802mm U 82.086251mm
ORI Y IS U AND Z IS S
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.65772mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161746mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 46176.964948mm N -10763.110544mm U 82.086251mm
ORI Y IS U AND Z IS S
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.65772mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161746mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 46157.3 N -10856.7 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 46157.299176mm N -10856.695444mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 46393.3 N -10856.7 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 46393.28844mm N -10856.695444mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 132.8
YLEN 577.2
ZLEN 60.2
POS E 45524.2 N -10856.7 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 67.0
YLEN 291.1
ZLEN 50.7
POS E 45524.2 N -10856.7 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 45489.601116mm N -10982.167138mm U 110.226413mm
ORI Y IS U AND Z IS S
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 45489.601116mm N -10681.035074mm U 110.226413mm
ORI Y IS U AND Z IS S
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 45482.7 N -10856.7 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 45482.672813mm N -10856.695444mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 45565.8 N -10856.7 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 45565.812441mm N -10856.695444mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 132.8
YLEN 577.2
ZLEN 60.2
POS E 45959.0 N -10856.7 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 67.0
YLEN 291.1
ZLEN 50.7
POS E 45959.0 N -10856.7 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 45924.318124mm N -10982.167138mm U 110.226413mm
ORI Y IS U AND Z IS S
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 45924.318124mm N -10681.035074mm U 110.226413mm
ORI Y IS U AND Z IS S
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 45917.4 N -10856.7 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 45917.389822mm N -10856.695444mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 46000.5 N -10856.7 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 46000.52945mm N -10856.695444mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 66.5
YLEN 132.9
ZLEN 13.9
POS E 46864.9 N -10856.7 U 56.9

-- Casing support: pedestal web
NEW BOX
XLEN 33.5
YLEN 67.0
ZLEN 245.3
POS E 46864.9 N -10856.7 U 186.5

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 46847.57987mm N -10885.589735mm U 63.869288mm
ORI Y IS U AND Z IS S
HEIG 11.55774mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.673221mm N 0mm U 0mm
END
NEW VERTEX
POS E 19.070271mm N 215.890985mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 46847.57987mm N -10816.243294mm U 63.869288mm
ORI Y IS U AND Z IS S
HEIG 11.55774mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.673221mm N 0mm U 0mm
END
NEW VERTEX
POS E 19.070271mm N 215.890985mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.9
ORI Z IS U AND Y IS N
POS E 46844.1 N -10856.7 U 56.9

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 46844.112548mm N -10856.695385mm U 63.869288mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.9
ORI Z IS U AND Y IS N
POS E 46885.7 N -10856.7 U 56.9

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 46885.720413mm N -10856.695385mm U 63.869288mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /205_PU_060_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 93; the only large round feature in the plan, at the wet end
-- CAD handles: 22BD9A,22BD93,22BD94,22BD95,22BD96,22BD97 ...
NEW CYLI
DIAM 186.4
HEIG 115.6
ORI Z IS U AND Y IS N
POS E 46864.9 N -10856.7 U 398.7

-- casing split flange at the cover joint
NEW CYLI
DIAM 205.1
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 46864.9 N -10856.7 U 464.5

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46956.6 N -10856.7 U 454.9

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 46956.644822mm N -10856.695385mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46929.8 N -10791.8 U 454.9

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 46929.778212mm N -10791.833653mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46864.9 N -10765.0 U 454.9

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 46864.91648mm N -10764.967044mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46800.1 N -10791.8 U 454.9

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 46800.054748mm N -10791.833653mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46773.2 N -10856.7 U 454.9

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 46773.188139mm N -10856.695385mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46800.1 N -10921.6 U 454.9

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 46800.054748mm N -10921.557117mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46864.9 N -10948.4 U 454.9

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 46864.91648mm N -10948.423726mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46929.8 N -10921.6 U 454.9

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 46929.778212mm N -10921.557117mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 115.6
DBOT 186.4
HEIG 34.7
ORI Z IS E AND Y IS U
POS E 46940.0 N -10856.7 U 398.7

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 78.3
HEIG 20.8
ORI Z IS E AND Y IS U
POS E 46796.7 N -10856.7 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 60.1
ORI Z IS E AND Y IS U
POS E 46864.9 N -10953.5 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 60.1
ORI Z IS E AND Y IS U
POS E 46864.9 N -10759.9 U 398.7

NEW SUBE /205_PU_060_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 410 mm along the machine axis x 431 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22BD74,22BD75,22BD76,22BDAE,22BDAF,22BDB0
NEW CYLI
DIAM 431.3
HEIG 409.7
ORI Z IS E AND Y IS U
POS E 46275.3 N -10856.7 U 398.7

NEW SUBE /205_PU_060_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 210 mm along x, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BDAC,22BDAD
NEW CYLI
DIAM 134.8
HEIG 210.2
ORI Z IS E AND Y IS U
POS E 46585.3 N -10854.0 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS E AND Y IS U
POS E 46503.3 N -10854.0 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS E AND Y IS U
POS E 46667.3 N -10854.0 U 398.7

NEW SUBE /205_PU_060_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 679 mm along the machine axis x 528 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BD7A,22BD7B,22BD7C,22BD77,22BD78,22BD79 ...
NEW CYLI
DIAM 528.3
HEIG 679.2
ORI Z IS E AND Y IS U
POS E 45741.6 N -10856.7 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS E AND Y IS U
POS E 45422.4 N -10856.7 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS E AND Y IS U
POS E 46060.8 N -10856.7 U 398.7

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10585.1 U 398.7

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10605.8 U 502.6

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10664.7 U 590.7

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10752.8 U 649.6

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10856.7 U 670.2

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10960.6 U 649.6

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -11048.7 U 590.7

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -11107.6 U 502.6

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -11128.2 U 398.7

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -11107.6 U 294.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -11048.7 U 206.7

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10960.6 U 147.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10856.7 U 127.1

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10752.8 U 147.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10664.7 U 206.7

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -10605.8 U 294.8

-- Motor terminal box
NEW BOX
XLEN 203.8
YLEN 211.3
ZLEN 116.2
POS E 45741.6 N -10856.7 U 720.9

-- Motor cable gland
NEW CYLI
DIAM 39.5
HEIG 116.2
ORI Z IS N AND Y IS U
POS E 45741.6 N -10692.9 U 720.9

-- Reference Value: motor lifting lug
NEW BOX
XLEN 63.4
YLEN 37.0
ZLEN 52.8
POS E 45551.4 N -10856.7 U 726.8

-- Reference Value: motor nameplate
NEW BOX
XLEN 122.3
YLEN 68.7
ZLEN 6.0
POS E 45823.1 N -11122.8 U 398.7

-- Motor fan cowl disc
NEW CYLI
DIAM 581.1
HEIG 8.0
ORI Z IS E AND Y IS U
POS E 45398.0 N -10856.7 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 267.3
ZLEN 6.4
POS E 45398.0 N -10990.4 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 267.3
ZLEN 6.4
POS E 45398.0 N -10723.0 U 398.7

NEW SUBE /205_PU_060_AUXILIARY
-- 2 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 248x361 at the wet end, outboard of the casing
-- CAD handles: 22BDC6,22BDC4,22BDC5,22BDA9,22BDAA,22BDAB ...
NEW BOX
XLEN 248.0
YLEN 361.2
ZLEN 198.4
POS E 46814.4 N -10864.8 U 149.2

-- Auxiliary [LOW]: body 22x221 at the wet end, outboard of the casing
-- CAD handles: 22BDA8,22BDA5,22BDA6,22BDA7
NEW BOX
XLEN 21.6
YLEN 221.0
ZLEN 60.0
POS E 46981.5 N -10854.0 U 80.0

NEW SUBE /205_PU_060_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN125; POS is the flange face, contractual direction E
NEW NOZZLE /205_PU_060_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0PP
POS E 46993.8 N -10854.0 U 398.7
ORI P1 IS E
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_060_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_060_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 46864.9 N -10856.7 U 606.5
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- --------------------------------------------------------------------
-- 205-PU-061
-- --------------------------------------------------------------------
-- 205-PU-061 - SCRUBBER CIRCULATION PUMP
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-061
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: E (driver -> casing)
-- Generated: 2026-08-13 03:44:51
-- Note: suction: metadata bore 113 mm snapped to catalogue DN125 (nearest available in 'AAZFBB0PP'; catalogue max is DN600)
-- Note: discharge: metadata bore 146 mm snapped to catalogue DN150 (nearest available in 'AAZFBB0RR'; catalogue max is DN600)

NEW EQUI /205_PU_061
POS E 0.0 N 0.0 U 0.0
NEW SUBE /205_PU_061_BASEPLATE
-- 9 part(s), 0 nozzle(s)
-- contractual rectangular baseplate; POS is its geometric centre and the metadata coordinate is its underside centre
NEW BOX
XLEN 1720.0
YLEN 760.0
ZLEN 50.0
POS E 46154.0 N -8256.0 U 25.0

-- Baseplate anchor bolt A1: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 45384.0 N -8560.0 U 67.1

-- Baseplate anchor bolt A1: hex nut
NEW EXTRUSION
POS E 45384mm N -8560mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A2: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 45384.0 N -7952.0 U 67.1

-- Baseplate anchor bolt A2: hex nut
NEW EXTRUSION
POS E 45384mm N -7952mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A3: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 46924.0 N -8560.0 U 67.1

-- Baseplate anchor bolt A3: hex nut
NEW EXTRUSION
POS E 46924mm N -8560mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

-- Baseplate anchor bolt A4: exposed shank
NEW CYLI
DIAM 22.8
HEIG 34.2
ORI Z IS U AND Y IS N
POS E 46924.0 N -7952.0 U 67.1

-- Baseplate anchor bolt A4: hex nut
NEW EXTRUSION
POS E 46924mm N -7952mm U 84.2mm
ORI Y IS N AND Z IS U
HEIG 18.24mm

NEW LOOP
NEW VERTEX
POS E 19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N 22.378096mm U 0mm
END
NEW VERTEX
POS E -19.38mm N 11.189048mm U 0mm
END
NEW VERTEX
POS E -19.38mm N -11.189048mm U 0mm
END
NEW VERTEX
POS E 0mm N -22.378096mm U 0mm
END
NEW VERTEX
POS E 19.38mm N -11.189048mm U 0mm
END
END
END

NEW SUBE /205_PU_061_SUPPORT
-- 32 part(s), 0 nozzle(s)
-- Bearing housing pedestal: sole plate on the baseplate
NEW BOX
XLEN 376.9
YLEN 307.5
ZLEN 32.1
POS E 46275.3 N -8253.3 U 66.0

-- Bearing housing pedestal: pedestal web
NEW BOX
XLEN 190.1
YLEN 155.1
ZLEN 122.5
POS E 46275.3 N -8253.3 U 143.3

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 46176.964948mm N -8320.150913mm U 82.086251mm
ORI Y IS U AND Z IS S
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.65772mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161746mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: triangular stiffener gusset
NEW EXTRUSION
POS E 46176.964948mm N -8159.719655mm U 82.086251mm
ORI Y IS U AND Z IS S
HEIG 26.738543mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 196.65772mm N 0mm U 0mm
END
NEW VERTEX
POS E 108.161746mm N 107.820162mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 46157.3 N -8253.3 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 46157.299176mm N -8253.304556mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Bearing housing pedestal: hold-down bolt shank
NEW CYLI
DIAM 17.4
HEIG 49.5
ORI Z IS U AND Y IS N
POS E 46393.3 N -8253.3 U 66.0

-- Bearing housing pedestal: hold-down hex nut
NEW EXTRUSION
POS E 46393.28844mm N -8253.304556mm U 82.086251mm
ORI Y IS N AND Z IS U
HEIG 13.904042mm

NEW LOOP
NEW VERTEX
POS E 14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N 17.058443mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N 8.529221mm U 0mm
END
NEW VERTEX
POS E -14.773045mm N -8.529221mm U 0mm
END
NEW VERTEX
POS E 0mm N -17.058443mm U 0mm
END
NEW VERTEX
POS E 14.773045mm N -8.529221mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 132.8
YLEN 577.2
ZLEN 60.2
POS E 45524.2 N -8253.3 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 67.0
YLEN 291.1
ZLEN 50.7
POS E 45524.2 N -8253.3 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 45489.601116mm N -8378.776249mm U 110.226413mm
ORI Y IS U AND Z IS S
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 45489.601116mm N -8077.644185mm U 110.226413mm
ORI Y IS U AND Z IS S
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 45482.7 N -8253.3 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 45482.672813mm N -8253.304556mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 45565.8 N -8253.3 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 45565.812441mm N -8253.304556mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: sole plate on the baseplate
NEW BOX
XLEN 132.8
YLEN 577.2
ZLEN 60.2
POS E 45959.0 N -8253.3 U 80.1

-- Motor foot: pedestal web
NEW BOX
XLEN 67.0
YLEN 291.1
ZLEN 50.7
POS E 45959.0 N -8253.3 U 135.6

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 45924.318124mm N -8378.776249mm U 110.226413mm
ORI Y IS U AND Z IS S
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: triangular stiffener gusset
NEW EXTRUSION
POS E 45924.318124mm N -8077.644185mm U 110.226413mm
ORI Y IS U AND Z IS S
HEIG 50.188677mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 69.283023mm N 0mm U 0mm
END
NEW VERTEX
POS E 38.105663mm N 44.630942mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 45917.4 N -8253.3 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 45917.389822mm N -8253.304556mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Motor foot: hold-down bolt shank
NEW CYLI
DIAM 32.6
HEIG 92.8
ORI Z IS U AND Y IS N
POS E 46000.5 N -8253.3 U 80.1

-- Motor foot: hold-down hex nut
NEW EXTRUSION
POS E 46000.52945mm N -8253.304556mm U 110.226413mm
ORI Y IS N AND Z IS U
HEIG 26.098112mm

NEW LOOP
NEW VERTEX
POS E 27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N 32.018973mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N 16.009487mm U 0mm
END
NEW VERTEX
POS E -27.729244mm N -16.009487mm U 0mm
END
NEW VERTEX
POS E 0mm N -32.018973mm U 0mm
END
NEW VERTEX
POS E 27.729244mm N -16.009487mm U 0mm
END
END
END

-- Casing support: sole plate on the baseplate
NEW BOX
XLEN 66.5
YLEN 132.9
ZLEN 13.9
POS E 46864.9 N -8253.3 U 56.9

-- Casing support: pedestal web
NEW BOX
XLEN 33.5
YLEN 67.0
ZLEN 245.3
POS E 46864.9 N -8253.3 U 186.5

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 46847.57987mm N -8282.198847mm U 63.869288mm
ORI Y IS U AND Z IS S
HEIG 11.55774mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.673221mm N 0mm U 0mm
END
NEW VERTEX
POS E 19.070271mm N 215.890985mm U 0mm
END
END
END

-- Casing support: triangular stiffener gusset
NEW EXTRUSION
POS E 46847.57987mm N -8212.852405mm U 63.869288mm
ORI Y IS U AND Z IS S
HEIG 11.55774mm

NEW LOOP
NEW VERTEX
POS E 0mm N 0mm U 0mm
END
NEW VERTEX
POS E 34.673221mm N 0mm U 0mm
END
NEW VERTEX
POS E 19.070271mm N 215.890985mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.9
ORI Z IS U AND Y IS N
POS E 46844.1 N -8253.3 U 56.9

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 46844.112548mm N -8253.304496mm U 63.869288mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Casing support: hold-down bolt shank
NEW CYLI
DIAM 12.0
HEIG 25.9
ORI Z IS U AND Y IS N
POS E 46885.7 N -8253.3 U 56.9

-- Casing support: hold-down hex nut
NEW EXTRUSION
POS E 46885.720413mm N -8253.304496mm U 63.869288mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

NEW SUBE /205_PU_061_CASING
-- 22 part(s), 0 nozzle(s)
-- PumpCasing [HIGH]: volute: 2 concentric circle(s) on one axis, radii 73, 93; the only large round feature in the plan, at the wet end
-- CAD handles: 22BFE5,22BFDE,22BFDF,22BFE0,22BFE1,22BFE2 ...
NEW CYLI
DIAM 186.4
HEIG 115.6
ORI Z IS U AND Y IS N
POS E 46864.9 N -8253.3 U 398.7

-- casing split flange at the cover joint
NEW CYLI
DIAM 205.1
HEIG 16.0
ORI Z IS U AND Y IS N
POS E 46864.9 N -8253.3 U 464.5

-- Reference Value: casing flange bolt 1/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46956.6 N -8253.3 U 454.9

-- Reference Value: casing flange hex nut 1/8
NEW EXTRUSION
POS E 46956.644822mm N -8253.304496mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 2/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46929.8 N -8188.4 U 454.9

-- Reference Value: casing flange hex nut 2/8
NEW EXTRUSION
POS E 46929.778212mm N -8188.442764mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 3/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46864.9 N -8161.6 U 454.9

-- Reference Value: casing flange hex nut 3/8
NEW EXTRUSION
POS E 46864.91648mm N -8161.576155mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 4/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46800.1 N -8188.4 U 454.9

-- Reference Value: casing flange hex nut 4/8
NEW EXTRUSION
POS E 46800.054748mm N -8188.442764mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 5/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46773.2 N -8253.3 U 454.9

-- Reference Value: casing flange hex nut 5/8
NEW EXTRUSION
POS E 46773.188139mm N -8253.304496mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 6/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46800.1 N -8318.2 U 454.9

-- Reference Value: casing flange hex nut 6/8
NEW EXTRUSION
POS E 46800.054748mm N -8318.166228mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 7/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46864.9 N -8345.0 U 454.9

-- Reference Value: casing flange hex nut 7/8
NEW EXTRUSION
POS E 46864.91648mm N -8345.032837mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- Reference Value: casing flange bolt 8/8
NEW CYLI
DIAM 12.0
HEIG 35.2
ORI Z IS U AND Y IS N
POS E 46929.8 N -8318.2 U 454.9

-- Reference Value: casing flange hex nut 8/8
NEW EXTRUSION
POS E 46929.778212mm N -8318.166228mm U 472.467934mm
ORI Y IS N AND Z IS U
HEIG 9.6mm

NEW LOOP
NEW VERTEX
POS E 10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N 11.777945mm U 0mm
END
NEW VERTEX
POS E -10.2mm N 5.888973mm U 0mm
END
NEW VERTEX
POS E -10.2mm N -5.888973mm U 0mm
END
NEW VERTEX
POS E 0mm N -11.777945mm U 0mm
END
NEW VERTEX
POS E 10.2mm N -5.888973mm U 0mm
END
END
END

-- volute closing onto the suction cover
NEW CONE
DTOP 115.6
DBOT 186.4
HEIG 34.7
ORI Z IS E AND Y IS U
POS E 46940.0 N -8253.3 U 398.7

-- casing shaft boss toward the bearing frame
NEW CYLI
DIAM 78.3
HEIG 20.8
ORI Z IS E AND Y IS U
POS E 46796.7 N -8253.3 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 60.1
ORI Z IS E AND Y IS U
POS E 46864.9 N -8350.1 U 398.7

-- Reference Value: axial casing rib
NEW CYLI
DIAM 9.0
HEIG 60.1
ORI Z IS E AND Y IS U
POS E 46864.9 N -8156.5 U 398.7

NEW SUBE /205_PU_061_BEARING
-- 1 part(s), 0 nozzle(s)
-- BearingHousing [HIGH]: BearingHousing assembly 410 mm along the machine axis x 431 mm across, consolidated from 2 drawn sections (housing sections)
-- CAD handles: 22C002,22C003,22C004,22BFC8,22BFC9,22BFCA
NEW CYLI
DIAM 431.3
HEIG 409.7
ORI Z IS E AND Y IS U
POS E 46275.3 N -8253.3 U 398.7

NEW SUBE /205_PU_061_COUPLING
-- 3 part(s), 0 nozzle(s)
-- Coupling [HIGH]: shaft/coupling: parallel rail pair 135 mm apart running 210 mm along x, a cylindrical body seen from the side; drawn on the machine centreline between driver and casing
-- CAD handles: 22BFCB,22BFCC
NEW CYLI
DIAM 134.8
HEIG 210.2
ORI Z IS E AND Y IS U
POS E 46585.3 N -8256.0 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS E AND Y IS U
POS E 46503.3 N -8256.0 U 398.7

-- Coupling hub (d=236) on the shaft centreline
NEW CYLI
DIAM 235.8
HEIG 46.3
ORI Z IS E AND Y IS U
POS E 46667.3 N -8256.0 U 398.7

NEW SUBE /205_PU_061_DRIVER
-- 26 part(s), 0 nozzle(s)
-- Motor [HIGH]: Motor assembly 679 mm along the machine axis x 528 mm across, consolidated from 3 drawn sections (body, fin bands, cowl)
-- CAD handles: 22BFFC,22BFFD,22BFFE,22BFFF,22C000,22C001 ...
NEW CYLI
DIAM 528.3
HEIG 679.2
ORI Z IS E AND Y IS U
POS E 45741.6 N -8253.3 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS E AND Y IS U
POS E 45422.4 N -8253.3 U 398.7

-- Motor end bell
NEW CYLI
DIAM 570.6
HEIG 40.8
ORI Z IS E AND Y IS U
POS E 46060.8 N -8253.3 U 398.7

-- Reference Value: 360-degree motor cooling rib 1/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -7981.8 U 398.7

-- Reference Value: 360-degree motor cooling rib 2/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8002.4 U 502.6

-- Reference Value: 360-degree motor cooling rib 3/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8061.3 U 590.7

-- Reference Value: 360-degree motor cooling rib 4/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8149.4 U 649.6

-- Reference Value: 360-degree motor cooling rib 5/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8253.3 U 670.2

-- Reference Value: 360-degree motor cooling rib 6/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8357.2 U 649.6

-- Reference Value: 360-degree motor cooling rib 7/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8445.3 U 590.7

-- Reference Value: 360-degree motor cooling rib 8/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8504.2 U 502.6

-- Reference Value: 360-degree motor cooling rib 9/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8524.9 U 398.7

-- Reference Value: 360-degree motor cooling rib 10/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8504.2 U 294.8

-- Reference Value: 360-degree motor cooling rib 11/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8445.3 U 206.7

-- Reference Value: 360-degree motor cooling rib 12/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8357.2 U 147.8

-- Reference Value: 360-degree motor cooling rib 13/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8253.3 U 127.1

-- Reference Value: 360-degree motor cooling rib 14/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8149.4 U 147.8

-- Reference Value: 360-degree motor cooling rib 15/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8061.3 U 206.7

-- Reference Value: 360-degree motor cooling rib 16/16
NEW CYLI
DIAM 14.8
HEIG 489.1
ORI Z IS E AND Y IS U
POS E 45741.6 N -8002.4 U 294.8

-- Motor terminal box
NEW BOX
XLEN 203.8
YLEN 211.3
ZLEN 116.2
POS E 45741.6 N -8253.3 U 720.9

-- Motor cable gland
NEW CYLI
DIAM 39.5
HEIG 116.2
ORI Z IS N AND Y IS U
POS E 45741.6 N -8089.5 U 720.9

-- Reference Value: motor lifting lug
NEW BOX
XLEN 63.4
YLEN 37.0
ZLEN 52.8
POS E 45551.4 N -8253.3 U 726.8

-- Reference Value: motor nameplate
NEW BOX
XLEN 122.3
YLEN 68.7
ZLEN 6.0
POS E 45823.1 N -8519.5 U 398.7

-- Motor fan cowl disc
NEW CYLI
DIAM 581.1
HEIG 8.0
ORI Z IS E AND Y IS U
POS E 45398.0 N -8253.3 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 267.3
ZLEN 6.4
POS E 45398.0 N -8387.0 U 398.7

-- Motor fan grille bar
NEW BOX
XLEN 9.6
YLEN 267.3
ZLEN 6.4
POS E 45398.0 N -8119.6 U 398.7

NEW SUBE /205_PU_061_AUXILIARY
-- 2 part(s), 0 nozzle(s)
-- Auxiliary [LOW]: body 248x356 at the wet end, outboard of the casing
-- CAD handles: 22BFCD,22BFCE,22BFCF,22BFC6,22BFC5,22BFC2 ...
NEW BOX
XLEN 248.0
YLEN 355.8
ZLEN 198.4
POS E 46814.4 N -8264.1 U 149.2

-- Auxiliary [LOW]: body 22x221 at the wet end, outboard of the casing
-- CAD handles: 22BFD9,22BFD6,22BFD7,22BFD8
NEW BOX
XLEN 21.6
YLEN 221.0
ZLEN 60.0
POS E 46981.5 N -8256.0 U 80.0

NEW SUBE /205_PU_061_SUCTION
-- 0 part(s), 1 nozzle(s)
-- suction DN125; POS is the flange face, contractual direction E
NEW NOZZLE /205_PU_061_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0PP
POS E 46993.8 N -8256.0 U 398.7
ORI P1 IS E
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

NEW SUBE /205_PU_061_DISCHARGE
-- 0 part(s), 1 nozzle(s)
-- discharge DN150; POS is the flange face, contractual direction U
NEW NOZZLE /205_PU_061_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 46864.9 N -8253.3 U 606.5
ORI P1 IS U
HEIG 150.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END
