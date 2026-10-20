-- ====================================================================
-- 203-PU-401 BS DD VACUUM PUMP (HORIZONTAL LIQUID RING VACUUM PUMP UNIT)
-- ====================================================================
-- Equipment Tag: /203_PU_401
-- Duty Description: BS DD Vacuum Pump (load: 4.5 t)
-- Configuration: Horizontal Foot-Mounted Skid Package (Horizontal Skid Unit)
-- Design Standard: AVEVA E3D Design Mk3.1 PML1 Compatible
-- Coordinate Origin: Foundation Floor at Pump Casing Centerline (U 0.0)
-- Shaft Elevation: U 320.0 mm (Horizontal Shaft along North-South)
-- Overall Length: 1977.0 mm (Verified against CAD plan view)
-- Motor Envelope: Dia 329.0 mm x 697.0 mm (TEFC with 16 Axial Cooling Fins)
-- Pump Casing: DN500 (Dia 505.0 mm) x 730.0 mm
-- Suction Nozzle N1: DN150 Flange OD 286.0 mm, Bore 167.0 mm, Pointing UP (U)
-- Aux Pump Volute: Dia 275.0 mm, Top Nozzle Dia 221.0 mm, Offset E 627.0 mm
-- Discharge Nozzle N2: DN50 Flange Dia 165.0 mm, Offset E 819.0 mm, Pointing South (S)

NEW EQUI /203_PU_401
POS E 0.0 N 0.0 U 0.0
NEW SUBE /203_PU_401_BASE_SKID
-- Heavy structural skid frame resting flat on the foundation slab (U 0..80)
-- Skid West Rail
NEW BOX
XLEN 120.0
YLEN 2150.0
ZLEN 80.0
POS E -220.0 N 975.0 U 40.0

END
-- Skid Center Rail
NEW BOX
XLEN 140.0
YLEN 2150.0
ZLEN 80.0
POS E 220.0 N 975.0 U 40.0

END
-- Skid East Rail
NEW BOX
XLEN 120.0
YLEN 2150.0
ZLEN 80.0
POS E 800.0 N 975.0 U 40.0

END
-- Skid Cross Beam
NEW BOX
XLEN 1140.0
YLEN 120.0
ZLEN 80.0
POS E 290.0 N -50.0 U 40.0

END
-- Skid Cross Beam
NEW BOX
XLEN 1140.0
YLEN 120.0
ZLEN 80.0
POS E 290.0 N 450.0 U 40.0

END
-- Skid Cross Beam
NEW BOX
XLEN 1140.0
YLEN 120.0
ZLEN 80.0
POS E 290.0 N 950.0 U 40.0

END
-- Skid Cross Beam
NEW BOX
XLEN 1140.0
YLEN 120.0
ZLEN 80.0
POS E 290.0 N 1450.0 U 40.0

END
-- Skid Cross Beam
NEW BOX
XLEN 1140.0
YLEN 120.0
ZLEN 80.0
POS E 290.0 N 2000.0 U 40.0

END
-- Anchor Bolt Pad
NEW CYLI
DIAM 50.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E -220.0 N -50.0 U 95.0

END
-- Anchor Bolt Pad
NEW CYLI
DIAM 50.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E -220.0 N 950.0 U 95.0

END
-- Anchor Bolt Pad
NEW CYLI
DIAM 50.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E -220.0 N 2000.0 U 95.0

END
-- Anchor Bolt Pad
NEW CYLI
DIAM 50.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 800.0 N -50.0 U 95.0

END
-- Anchor Bolt Pad
NEW CYLI
DIAM 50.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 800.0 N 950.0 U 95.0

END
-- Anchor Bolt Pad
NEW CYLI
DIAM 50.0
HEIG 30.0
ORI Z IS U AND Y IS N
POS E 800.0 N 2000.0 U 95.0

END
-- Motor Left Mounting Bed
NEW BOX
XLEN 100.0
YLEN 600.0
ZLEN 30.0
POS E -170.0 N 1550.0 U 95.0

END
-- Motor Right Mounting Bed
NEW BOX
XLEN 100.0
YLEN 600.0
ZLEN 30.0
POS E 170.0 N 1550.0 U 95.0

END
END
NEW SUBE /203_PU_401_PUMP_CASING
-- Horizontal Vacuum Pump Casing (Centerline E 0.0, U 320.0)
-- Pump Front Cover / Sole Plate
NEW CYLI
DIAM 300.0
HEIG 40.0
ORI Z IS N AND Y IS U
POS E 0.0 N 20.0 U 320.0

END
-- Front Sump Neck Cylinder
NEW CYLI
DIAM 219.0
HEIG 80.0
ORI Z IS N AND Y IS U
POS E 0.0 N 80.0 U 320.0

END
-- Conical Casing Reducer
NEW CONE
DTOP 505.0
DBOT 219.0
HEIG 135.0
ORI Z IS N AND Y IS U
POS E 0.0 N 187.5 U 320.0

END
-- Main Horizontal Pump Casing DN500
NEW CYLI
DIAM 505.0
HEIG 595.0
ORI Z IS N AND Y IS U
POS E 0.0 N 552.5 U 320.0

END
-- Casing Stiffener Ring 1
NEW CYLI
DIAM 525.0
HEIG 15.0
ORI Z IS N AND Y IS U
POS E 0.0 N 457.5 U 320.0

END
-- Casing Stiffener Ring 2
NEW CYLI
DIAM 525.0
HEIG 15.0
ORI Z IS N AND Y IS U
POS E 0.0 N 687.5 U 320.0

END
-- Casing Rear Cover Flange
NEW CYLI
DIAM 520.0
HEIG 30.0
ORI Z IS N AND Y IS U
POS E 0.0 N 865.0 U 320.0

END
-- Pump Front Support Foot
NEW BOX
XLEN 520.0
YLEN 80.0
ZLEN 17.5
POS E 0.0 N 300.0 U 88.8

END
-- Pump Rear Support Foot
NEW BOX
XLEN 520.0
YLEN 80.0
ZLEN 17.5
POS E 0.0 N 750.0 U 88.8

END
-- Pump Bottom Drain Boss
NEW CYLI
DIAM 50.0
HEIG 40.0
ORI Z IS D AND Y IS N
POS E 0.0 N 100.0 U 190.5

END
END
NEW SUBE /203_PU_401_STOOL
-- Horizontal intermediate bracket, drive shaft, coupling and guard
-- Bracket Front Mounting Ring
NEW CYLI
DIAM 300.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 0.0 N 910.0 U 320.0

END
-- Horizontal Drive Shaft
NEW CYLI
DIAM 75.0
HEIG 140.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1010.0 U 320.0

END
-- Pump Side Coupling Hub
NEW CYLI
DIAM 120.0
HEIG 40.0
ORI Z IS N AND Y IS U
POS E 0.0 N 960.0 U 320.0

END
-- Motor Side Coupling Hub
NEW CYLI
DIAM 120.0
HEIG 40.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1060.0 U 320.0

END
-- Bracket Stool Leg at 45.0 deg
NEW BOX
XLEN 36.0
YLEN 140.0
ZLEN 36.0
POS E 88.4 N 1010.0 U 408.4

END
-- Bracket Stool Leg at 135.0 deg
NEW BOX
XLEN 36.0
YLEN 140.0
ZLEN 36.0
POS E -88.4 N 1010.0 U 408.4

END
-- Bracket Stool Leg at 225.0 deg
NEW BOX
XLEN 36.0
YLEN 140.0
ZLEN 36.0
POS E -88.4 N 1010.0 U 231.6

END
-- Bracket Stool Leg at 315.0 deg
NEW BOX
XLEN 36.0
YLEN 140.0
ZLEN 36.0
POS E 88.4 N 1010.0 U 231.6

END
-- Bearing / Seal Housing
NEW CYLI
DIAM 263.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1110.0 U 320.0

END
-- Seal Flush Boss
NEW CYLI
DIAM 35.0
HEIG 40.0
ORI Z IS U AND Y IS N
POS E 0.0 N 1110.0 U 471.5

END
-- Motor Adapter Bell Housing
NEW CONE
DTOP 364.0
DBOT 263.0
HEIG 80.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1180.0 U 320.0

END
END
NEW SUBE /203_PU_401_MOTOR
-- Horizontal Foot/Flange-Mounted TEFC Electric Motor (N 1220..1977)
-- Motor Drive-End Flange
NEW CYLI
DIAM 364.0
HEIG 60.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1250.0 U 320.0

END
-- Motor Flange Bolt 1
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS N AND Y IS U
POS E 160.0 N 1267.5 U 320.0

END
-- Motor Flange Bolt 2
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS N AND Y IS U
POS E 113.1 N 1267.5 U 433.1

END
-- Motor Flange Bolt 3
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1267.5 U 480.0

END
-- Motor Flange Bolt 4
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS N AND Y IS U
POS E -113.1 N 1267.5 U 433.1

END
-- Motor Flange Bolt 5
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS N AND Y IS U
POS E -160.0 N 1267.5 U 320.0

END
-- Motor Flange Bolt 6
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS N AND Y IS U
POS E -113.1 N 1267.5 U 206.9

END
-- Motor Flange Bolt 7
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS N AND Y IS U
POS E -0.0 N 1267.5 U 160.0

END
-- Motor Flange Bolt 8
NEW CYLI
DIAM 20.0
HEIG 25.0
ORI Z IS N AND Y IS U
POS E 113.1 N 1267.5 U 206.9

END
-- Motor Stator Barrel (Dia 329)
NEW CYLI
DIAM 329.0
HEIG 495.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1527.5 U 320.0

END
-- Horizontal Cooling Fin 1
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E 193.5 N 1527.5 U 320.0

END
-- Horizontal Cooling Fin 2
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E 178.8 N 1527.5 U 394.0

END
-- Horizontal Cooling Fin 3
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E 136.8 N 1527.5 U 456.8

END
-- Horizontal Cooling Fin 4
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E 74.0 N 1527.5 U 498.8

END
-- Horizontal Cooling Fin 5
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E 0.0 N 1527.5 U 513.5

END
-- Horizontal Cooling Fin 6
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E -74.0 N 1527.5 U 498.8

END
-- Horizontal Cooling Fin 7
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E -136.8 N 1527.5 U 456.8

END
-- Horizontal Cooling Fin 8
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E -178.8 N 1527.5 U 394.0

END
-- Horizontal Cooling Fin 9
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E -193.5 N 1527.5 U 320.0

END
-- Horizontal Cooling Fin 10
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E -178.8 N 1527.5 U 246.0

END
-- Horizontal Cooling Fin 11
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E -136.8 N 1527.5 U 183.2

END
-- Horizontal Cooling Fin 12
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E -74.0 N 1527.5 U 141.2

END
-- Horizontal Cooling Fin 13
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E -0.0 N 1527.5 U 126.5

END
-- Horizontal Cooling Fin 14
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E 74.0 N 1527.5 U 141.2

END
-- Horizontal Cooling Fin 15
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E 136.8 N 1527.5 U 183.2

END
-- Horizontal Cooling Fin 16
NEW BOX
XLEN 58.0
YLEN 490.0
ZLEN 8.0
POS E 178.8 N 1527.5 U 246.0

END
-- Motor Terminal Box Body
NEW BOX
XLEN 160.0
YLEN 220.0
ZLEN 120.0
POS E -185.0 N 1480.0 U 320.0

END
-- Terminal Box Lid
NEW BOX
XLEN 170.0
YLEN 230.0
ZLEN 20.0
POS E -190.0 N 1480.0 U 385.0

END
-- Cable Gland Fitting
NEW CYLI
DIAM 45.0
HEIG 50.0
ORI Z IS D AND Y IS N
POS E -185.0 N 1480.0 U 235.0

END
-- Motor Front Left Foot
NEW BOX
XLEN 80.0
YLEN 180.0
ZLEN 75.5
POS E -170.0 N 1380.0 U 132.8

END
-- Motor Front Right Foot
NEW BOX
XLEN 80.0
YLEN 180.0
ZLEN 75.5
POS E 170.0 N 1380.0 U 132.8

END
-- Motor Rear Left Foot
NEW BOX
XLEN 80.0
YLEN 180.0
ZLEN 75.5
POS E -170.0 N 1680.0 U 132.8

END
-- Motor Rear Right Foot
NEW BOX
XLEN 80.0
YLEN 180.0
ZLEN 75.5
POS E 170.0 N 1680.0 U 132.8

END
-- Top Center Lifting Lug
NEW BOX
XLEN 30.0
YLEN 50.0
ZLEN 60.0
POS E 0.0 N 1480.0 U 500.0

END
-- Motor Fan Cowl Body
NEW CYLI
DIAM 329.0
HEIG 152.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1851.0 U 320.0

END
-- Fan Cowl Rear Chamfer (End N 1977.0)
NEW CONE
DTOP 273.0
DBOT 329.0
HEIG 50.0
ORI Z IS N AND Y IS U
POS E 0.0 N 1952.0 U 320.0

END
END
NEW SUBE /203_PU_401_INTERCONNECT
-- Interconnecting process piping between vacuum casing and aux pump
-- Casing Outlet Spool
NEW CYLI
DIAM 114.3
HEIG 70.0
ORI Z IS E AND Y IS U
POS E 285.0 N 384.0 U 320.0

END
-- Casing Outlet Flange
NEW CYLI
DIAM 220.0
HEIG 20.0
ORI Z IS W AND Y IS U
POS E 310.0 N 384.0 U 320.0

END
-- Pipe Inlet Flange
NEW CYLI
DIAM 220.0
HEIG 20.0
ORI Z IS E AND Y IS U
POS E 330.0 N 384.0 U 320.0

END
-- Flange Bolt at 45.0 deg
NEW CYLI
DIAM 18.0
HEIG 50.0
ORI Z IS E AND Y IS U
POS E 320.0 N 444.1 U 380.1

END
-- Flange Bolt at 135.0 deg
NEW CYLI
DIAM 18.0
HEIG 50.0
ORI Z IS E AND Y IS U
POS E 320.0 N 323.9 U 380.1

END
-- Flange Bolt at 225.0 deg
NEW CYLI
DIAM 18.0
HEIG 50.0
ORI Z IS E AND Y IS U
POS E 320.0 N 323.9 U 259.9

END
-- Flange Bolt at 315.0 deg
NEW CYLI
DIAM 18.0
HEIG 50.0
ORI Z IS E AND Y IS U
POS E 320.0 N 444.1 U 259.9

END
-- Connecting Pipe Spool
NEW CYLI
DIAM 114.3
HEIG 287.0
ORI Z IS E AND Y IS U
POS E 483.5 N 384.0 U 320.0

END
-- Aux Pump Suction Spool
NEW CYLI
DIAM 114.3
HEIG 146.0
ORI Z IS S AND Y IS U
POS E 627.0 N 311.0 U 320.0

END
END
NEW SUBE /203_PU_401_AUX_PUMP
-- Auxiliary centrifugal filtrate pump (Center E 627.0, N 238.0, U 320.0)
-- Aux Volute Casing (Dia 275)
NEW CYLI
DIAM 275.0
HEIG 180.0
ORI Z IS N AND Y IS U
POS E 627.0 N 238.0 U 320.0

END
-- Aux Front Cover (Dia 221)
NEW CYLI
DIAM 221.0
HEIG 25.0
ORI Z IS S AND Y IS U
POS E 627.0 N 135.5 U 320.0

END
-- Aux Suction Eye Hub
NEW CYLI
DIAM 100.0
HEIG 20.0
ORI Z IS S AND Y IS U
POS E 627.0 N 113.0 U 320.0

END
-- Casing Bolt 1
NEW CYLI
DIAM 18.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 717.0 N 108.0 U 320.0

END
-- Casing Bolt 2
NEW CYLI
DIAM 18.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 672.0 N 108.0 U 397.9

END
-- Casing Bolt 3
NEW CYLI
DIAM 18.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 582.0 N 108.0 U 397.9

END
-- Casing Bolt 4
NEW CYLI
DIAM 18.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 537.0 N 108.0 U 320.0

END
-- Casing Bolt 5
NEW CYLI
DIAM 18.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 582.0 N 108.0 U 242.1

END
-- Casing Bolt 6
NEW CYLI
DIAM 18.0
HEIG 30.0
ORI Z IS S AND Y IS U
POS E 672.0 N 108.0 U 242.1

END
-- Aux Rear Bearing Housing
NEW CYLI
DIAM 140.0
HEIG 140.0
ORI Z IS N AND Y IS U
POS E 627.0 N 398.0 U 320.0

END
-- Bearing End Cap
NEW CYLI
DIAM 90.0
HEIG 40.0
ORI Z IS N AND Y IS U
POS E 627.0 N 488.0 U 320.0

END
-- Aux Pump Support Pedestal
NEW BOX
XLEN 180.0
YLEN 200.0
ZLEN 122.5
POS E 627.0 N 238.0 U 141.2

END
END
NEW SUBE /203_PU_401_N1
-- Main process suction inlet N1 (DN150 150lb RF, Pointing UP)
-- N1: DN150 Top Suction Nozzle (Flange OD 286, ID 167, Pointing UP)
NEW NOZZLE /203_PU_401_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR
POS E 0.0 N 177.0 U 650.0
ORI P1 IS U
HEIG 250.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- N1 Nozzle Neck Barrel
NEW CYLI
DIAM 167.0
HEIG 220.0
ORI Z IS U AND Y IS N
POS E 0.0 N 177.0 U 540.0

END
END
NEW SUBE /203_PU_401_N2
-- Filtrate discharge nozzle N2 (DN50 150lb RF, Pointing South)
-- N2: DN50 Filtrate Discharge Nozzle (Offset E 819, Pointing South)
NEW NOZZLE /203_PU_401_N2_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0JJ
POS E 819.0 N 0.0 U 320.0
ORI P1 IS S
HEIG 180.0
TEMP -100000
PRES 0
TPRESS 0
DUTY unset
END

-- N2 Horizontal Discharge Spool
NEW CYLI
DIAM 60.3
HEIG 150.0
ORI Z IS S AND Y IS U
POS E 819.0 N 75.0 U 320.0

END
END
NEW SUBE /203_PU_401_N3
-- Auxiliary pump top nozzle N3 (DN100 150lb RF, Pointing UP)
-- N3: DN100 Aux Pump Top Connection (Flange Dia 221, Pointing UP)
NEW NOZZLE /203_PU_401_N3_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0NN
POS E 627.0 N 238.0 U 580.0
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
POS E 627.0 N 238.0 U 500.0

END
END
END

-- ====================================================================
-- NOZZLE CATALOGUE SUMMARY
-- ====================================================================
-- 3 of 3 nozzles bound to a catalogue component.
-- Each binding is inline in its NEW NOZZLE block: a nozzle has no
-- P-points or position until a component is bound, so CATR must
-- precede POS and ORI (equnozzle.pmlfrm:894).

-- End of macro - 1 equipment, 97 primitives.
