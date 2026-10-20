-- ====================================================================
-- 204-PU-401 VACUUM PUMP (HORIZONTAL LIQUID RING VACUUM PUMP UNIT)
-- ====================================================================
-- Equipment Tag: /204_PU_401
-- Duty Description: Post 02 DD1 Vacuum Pump (load: 4.5 t)
-- Configuration: Horizontal Skid Package (100% CAD Plan View Silhouette)
-- Design Standard: AVEVA E3D Design Mk3.1 PML1 Compatible
-- Main Shaft Axis: East (+E) from E 0.0 to E 1977.0 mm
-- Centerline Elevation: U 280.0 mm
-- Overall Length: 1977.0 mm (CAD Verified: E 0.0 to E 1977.0 mm)
-- Casing & Motor Width: 442.0 mm (CAD Verified: N -221.0 to N +221.0 mm)
-- Auxiliary Unit Center: E 261.0 mm, N 610.0 mm (CAD Verified)
-- Aux Unit Overall Width: 436.0 mm (CAD Verified)
-- Aux Discharge Nozzle: 113.0 mm OD at E 49.0 mm, N 765.0 mm
-- Nozzle N1 (Suction): DN150 150lb RF at E 199.0, N 0.0 pointing UP
-- Nozzle N2 (Aux Discharge): DN100 150lb RF at E 49.0, N 765.0 pointing WEST
-- Nozzle N3 (Aux Top): DN100 150lb RF at E 261.0, N 610.0 pointing UP
-- Nozzle N4 (Front Cleanout): DN80 150lb RF at E 0.0, N 0.0 pointing WEST

NEW EQUI /204_PU_401
POS E 0.0 N 0.0 U 0.0
NEW SUBE /204_PU_401_BASE_SKID
-- Low profile mounting skid and foundation pads (U 0..60)
-- South Base Rail
NEW BOX
XLEN 1900.0
YLEN 80.0
ZLEN 60.0
POS E 1000.0 N -170.0 U 30.0

END
-- North Base Rail
NEW BOX
XLEN 1900.0
YLEN 80.0
ZLEN 60.0
POS E 1000.0 N 170.0 U 30.0

END
-- Aux Unit Skid Rail
NEW BOX
XLEN 400.0
YLEN 80.0
ZLEN 60.0
POS E 261.0 N 610.0 U 30.0

END
-- Aux Cross Beam
NEW BOX
XLEN 80.0
YLEN 440.0
ZLEN 60.0
POS E 261.0 N 390.0 U 30.0

END
-- Skid Anchor Pad
NEW CYLI
DIAM 45.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 100.0 N -170.0 U 72.5

END
-- Skid Anchor Pad
NEW CYLI
DIAM 45.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 100.0 N 170.0 U 72.5

END
-- Skid Anchor Pad
NEW CYLI
DIAM 45.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 950.0 N -170.0 U 72.5

END
-- Skid Anchor Pad
NEW CYLI
DIAM 45.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 950.0 N 170.0 U 72.5

END
-- Skid Anchor Pad
NEW CYLI
DIAM 45.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 1850.0 N -170.0 U 72.5

END
-- Skid Anchor Pad
NEW CYLI
DIAM 45.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 1850.0 N 170.0 U 72.5

END
END
NEW SUBE /204_PU_401_PUMP_CASING
-- Liquid ring vacuum pump casing with front suction manifold (E 0..873)
-- Front Casing Spool
NEW CYLI
DIAM 168.0
HEIG 120.0
ORI Z IS E AND Y IS U
POS E 60.0 N 0.0 U 280.0

END
-- Front Cover Flange
NEW CYLI
DIAM 220.0
HEIG 25.0
ORI Z IS E AND Y IS U
POS E 12.5 N 0.0 U 280.0

END
-- Front Suction Chamber
NEW CYLI
DIAM 320.0
HEIG 155.0
ORI Z IS E AND Y IS U
POS E 197.5 N 0.0 U 280.0

END
-- Main Vacuum Rotor Casing (Dia 442 x 598)
NEW CYLI
DIAM 442.0
HEIG 598.0
ORI Z IS E AND Y IS U
POS E 574.0 N 0.0 U 280.0

END
-- Stiffener Ring 1
NEW CYLI
DIAM 460.0
HEIG 16.0
ORI Z IS E AND Y IS U
POS E 488.0 N 0.0 U 280.0

END
-- Stiffener Ring 2
NEW CYLI
DIAM 460.0
HEIG 16.0
ORI Z IS E AND Y IS U
POS E 728.0 N 0.0 U 280.0

END
-- Rear Casing DE Flange
NEW CYLI
DIAM 460.0
HEIG 20.0
ORI Z IS E AND Y IS U
POS E 863.0 N 0.0 U 280.0

END
-- Pump Front Foot
NEW BOX
XLEN 90.0
YLEN 430.0
ZLEN 29.0
POS E 330.0 N 0.0 U 74.5

END
-- Pump Rear Foot
NEW BOX
XLEN 90.0
YLEN 430.0
ZLEN 29.0
POS E 780.0 N 0.0 U 74.5

END
-- Casing Side Branch Neck
NEW CYLI
DIAM 140.0
HEIG 70.0
ORI Z IS N AND Y IS U
POS E 398.0 N 256.0 U 280.0

END
-- Casing Side Branch Flange
NEW CYLI
DIAM 210.0
HEIG 20.0
ORI Z IS N AND Y IS U
POS E 398.0 N 301.0 U 280.0

END
END
NEW SUBE /204_PU_401_INTERCONNECT
-- Interconnecting pipe spool between main casing and aux unit (E 398)
-- Interconnect Companion Flange
NEW CYLI
DIAM 210.0
HEIG 20.0
ORI Z IS S AND Y IS U
POS E 398.0 N 301.0 U 280.0

END
-- Interconnect Pipe Spool North
NEW CYLI
DIAM 114.3
HEIG 119.0
ORI Z IS N AND Y IS U
POS E 398.0 N 370.5 U 280.0

END
-- Interconnect Pipe Spool West
NEW CYLI
DIAM 114.3
HEIG 137.0
ORI Z IS E AND Y IS U
POS E 329.5 N 430.0 U 280.0

END
-- Interconnect Pipe Drop into Aux
NEW CYLI
DIAM 114.3
HEIG 180.0
ORI Z IS N AND Y IS U
POS E 261.0 N 520.0 U 280.0

END
END
NEW SUBE /204_PU_401_AUX_UNIT
-- Auxiliary separator / circulating pump volute (Center E 261, N 610, U 280)
-- Aux Volute Chamber (Dia 420)
NEW CYLI
DIAM 420.0
HEIG 240.0
ORI Z IS U AND Y IS N
POS E 261.0 N 610.0 U 280.0

END
-- Aux Volute Top Cover
NEW CYLI
DIAM 436.0
HEIG 25.0
ORI Z IS U AND Y IS N
POS E 261.0 N 610.0 U 412.5

END
-- Aux Tangential Discharge Barrel (Dia 113)
NEW CYLI
DIAM 113.0
HEIG 212.0
ORI Z IS W AND Y IS U
POS E 155.0 N 765.0 U 280.0

END
-- Aux Unit Pedestal
NEW BOX
XLEN 220.0
YLEN 220.0
ZLEN 100.0
POS E 261.0 N 610.0 U 110.0

END
END
NEW SUBE /204_PU_401_STOOL
-- Intermediate bearing bracket stool, drive shaft, and coupling guard (E 873..1420)
-- Stool Front Ring
NEW CYLI
DIAM 340.0
HEIG 112.0
ORI Z IS E AND Y IS U
POS E 929.0 N 0.0 U 280.0

END
-- Drive Shaft
NEW CYLI
DIAM 80.0
HEIG 149.0
ORI Z IS E AND Y IS U
POS E 1059.5 N 0.0 U 280.0

END
-- Pump Coupling Hub
NEW CYLI
DIAM 160.0
HEIG 45.0
ORI Z IS E AND Y IS U
POS E 1007.5 N 0.0 U 280.0

END
-- Motor Coupling Hub
NEW CYLI
DIAM 160.0
HEIG 45.0
ORI Z IS E AND Y IS U
POS E 1111.5 N 0.0 U 280.0

END
-- Coupling Protective Guard
NEW BOX
XLEN 149.0
YLEN 320.0
ZLEN 300.0
POS E 1059.5 N 0.0 U 280.0

END
-- Rear Bearing Housing
NEW CYLI
DIAM 260.0
HEIG 174.0
ORI Z IS E AND Y IS U
POS E 1221.0 N 0.0 U 280.0

END
-- Motor Adapter Bell Housing
NEW CONE
DTOP 370.0
DBOT 260.0
HEIG 62.0
ORI Z IS E AND Y IS U
POS E 1339.0 N 0.0 U 280.0

END
-- Motor Drive-End Flange
NEW CYLI
DIAM 370.0
HEIG 50.0
ORI Z IS E AND Y IS U
POS E 1395.0 N 0.0 U 280.0

END
-- DE Flange Bolt 1
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS E AND Y IS U
POS E 1407.5 N 160.0 U 280.0

END
-- DE Flange Bolt 2
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS E AND Y IS U
POS E 1407.5 N 113.1 U 393.1

END
-- DE Flange Bolt 3
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS E AND Y IS U
POS E 1407.5 N 0.0 U 440.0

END
-- DE Flange Bolt 4
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS E AND Y IS U
POS E 1407.5 N -113.1 U 393.1

END
-- DE Flange Bolt 5
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS E AND Y IS U
POS E 1407.5 N -160.0 U 280.0

END
-- DE Flange Bolt 6
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS E AND Y IS U
POS E 1407.5 N -113.1 U 166.9

END
-- DE Flange Bolt 7
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS E AND Y IS U
POS E 1407.5 N -0.0 U 120.0

END
-- DE Flange Bolt 8
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS E AND Y IS U
POS E 1407.5 N 113.1 U 166.9

END
END
NEW SUBE /204_PU_401_MOTOR
-- TEFC Electric Motor with top terminal box & axial fins (E 1420..1977)
-- Motor Stator Barrel (Dia 442 x 350)
NEW CYLI
DIAM 442.0
HEIG 350.0
ORI Z IS E AND Y IS U
POS E 1595.0 N 0.0 U 280.0

END
-- Motor Axial Rib 1
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N 226.0 U 280.0

END
-- Motor Axial Rib 2
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N 208.8 U 366.5

END
-- Motor Axial Rib 3
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N 159.8 U 439.8

END
-- Motor Axial Rib 4
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N 86.5 U 488.8

END
-- Motor Axial Rib 5
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N 0.0 U 506.0

END
-- Motor Axial Rib 6
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N -86.5 U 488.8

END
-- Motor Axial Rib 7
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N -159.8 U 439.8

END
-- Motor Axial Rib 8
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N -208.8 U 366.5

END
-- Motor Axial Rib 9
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N -226.0 U 280.0

END
-- Motor Axial Rib 10
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N -208.8 U 193.5

END
-- Motor Axial Rib 11
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N -159.8 U 120.2

END
-- Motor Axial Rib 12
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N -86.5 U 71.2

END
-- Motor Axial Rib 13
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N -0.0 U 54.0

END
-- Motor Axial Rib 14
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N 86.5 U 71.2

END
-- Motor Axial Rib 15
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N 159.8 U 120.2

END
-- Motor Axial Rib 16
NEW BOX
XLEN 346.0
YLEN 10.0
ZLEN 10.0
POS E 1595.0 N 208.8 U 193.5

END
-- Top Terminal Box Body
NEW BOX
XLEN 130.0
YLEN 170.0
ZLEN 120.0
POS E 1495.0 N 0.0 U 561.0

END
-- Terminal Box Lid
NEW BOX
XLEN 140.0
YLEN 180.0
ZLEN 20.0
POS E 1495.0 N 0.0 U 631.0

END
-- Terminal Cable Gland
NEW CYLI
DIAM 40.0
HEIG 40.0
ORI Z IS N AND Y IS U
POS E 1495.0 N 110.0 U 561.0

END
-- Motor Front South Foot
NEW BOX
XLEN 90.0
YLEN 100.0
ZLEN 29.0
POS E 1470.0 N -170.0 U 74.5

END
-- Motor Front North Foot
NEW BOX
XLEN 90.0
YLEN 100.0
ZLEN 29.0
POS E 1470.0 N 170.0 U 74.5

END
-- Motor Rear South Foot
NEW BOX
XLEN 90.0
YLEN 100.0
ZLEN 29.0
POS E 1720.0 N -170.0 U 74.5

END
-- Motor Rear North Foot
NEW BOX
XLEN 90.0
YLEN 100.0
ZLEN 29.0
POS E 1720.0 N 170.0 U 74.5

END
-- Fan Cowl Cylinder
NEW CYLI
DIAM 442.0
HEIG 145.0
ORI Z IS E AND Y IS U
POS E 1842.5 N 0.0 U 280.0

END
-- Fan Cowl Rear Dome (End E 1977.0)
NEW CONE
DTOP 320.0
DBOT 442.0
HEIG 62.0
ORI Z IS E AND Y IS U
POS E 1946.0 N 0.0 U 280.0

END
END
NEW SUBE /204_PU_401_N1
-- Main suction inlet N1 (DN150 150lb RF, Pointing UP at E 199.0, N 0.0)
-- N1: DN150 Top Suction Flange (Pointing UP)
NEW NOZZLE /204_PU_401_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 199.0 N 0.0 U 580.0
ORI P1 IS U
HEIG 220.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- N1 Nozzle Neck Barrel
NEW CYLI
DIAM 168.3
HEIG 200.0
ORI Z IS U AND Y IS N
POS E 199.0 N 0.0 U 480.0

END
END
NEW SUBE /204_PU_401_N2
-- Aux unit tangential discharge N2 (DN100 150lb RF, Pointing West at E 49.0, N 765.0)
-- N2: DN100 Tangential Discharge Flange (Pointing West)
NEW NOZZLE /204_PU_401_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 49.0 N 765.0 U 280.0
ORI P1 IS W
HEIG 180.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- N2 Discharge Neck Spool
NEW CYLI
DIAM 113.0
HEIG 150.0
ORI Z IS W AND Y IS U
POS E 124.0 N 765.0 U 280.0

END
END
NEW SUBE /204_PU_401_N3
-- Aux unit top connection N3 (DN100 150lb RF, Pointing UP at E 261.0, N 610.0)
-- N3: DN100 Aux Top Connection Flange (Pointing UP)
NEW NOZZLE /204_PU_401_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 261.0 N 610.0 U 560.0
ORI P1 IS U
HEIG 180.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- N3 Top Nozzle Barrel
NEW CYLI
DIAM 114.3
HEIG 160.0
ORI Z IS U AND Y IS N
POS E 261.0 N 610.0 U 480.0

END
END
NEW SUBE /204_PU_401_N4
-- Front casing cleanout/drain nozzle N4 (DN80 150lb RF, Pointing West at E 0.0, N 0.0)
-- N4: DN80 Front Casing Flange (Pointing West)
NEW NOZZLE /204_PU_401_N4_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0LL
POS E 0.0 N 0.0 U 280.0
ORI P1 IS W
HEIG 120.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

END
END

-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 4 of 4 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 74 primitives.
