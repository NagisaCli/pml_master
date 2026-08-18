-- ====================================================================
-- 205-PU-027 - EOP WASHER FEED PUMP
-- ====================================================================
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-027
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
