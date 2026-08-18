-- ====================================================================
-- 204-PU-003 - PRIMARY SCREEN FEED PUMP
-- ====================================================================
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 204-PU-003
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
