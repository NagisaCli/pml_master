-- ====================================================================
-- 203-PU-008 - BLOW TANK DILUTION PUMP
-- ====================================================================
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 203-PU-008
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: N (driver -> casing)
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
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
