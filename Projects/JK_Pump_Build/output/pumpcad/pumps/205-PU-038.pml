-- ====================================================================
-- 205-PU-038 - EOP STAGE MC PUMP (205-PU-038/MC PUMP)
-- ====================================================================
-- Project: JK_Pump_Build (pumpcad reconstruction)
-- Equipment: 205-PU-038
-- Units: mm
-- Frame: E = East, N = North, U = Up
-- Datum: metadata coordinate = geometric centre of baseplate underside
-- Source view: plan
-- Layout axis: W (driver -> casing)
-- Hierarchy: Exactly one EQUI in this file
-- Execution: Select a writable ZONE, then $M <this file>
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
