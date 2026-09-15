-- ====================================================================
-- Equipment Support Leg Bracket (Curved Welded Backing Pad)
-- Orientation: Sits on West, Faces East (坐西朝东)
-- Tank Bottom Center: E 14000.00 mm, N 38435.00 mm, U 14.50 mm
-- Tank Diameter: OD = 2022.00 mm (R_in = 1011.00 mm)
-- CAD Reference: DIGESTER HOUSE LAYOUT_SPM_CTE_10MAR26 (DWG loose-1)
-- Base Plate: 250.28 x 252.79 x 16.00 mm (Nominal 10" x 10" x 5/8")
-- Anchor Bolt Hole: Diam 43.20 mm (Clearance for M36 / 1-1/2" anchor bolt)
-- Backing Pad: R_in = 1011.0 mm, R_out = 1018.2 mm, Thk = 7.20 mm, H = 220 mm
-- Dual Gussets: Thk = 14.87 mm, H = 180 mm, Span between ribs = 173.5 mm
-- ====================================================================

NEW SUBEQUIPMENT /TANK_SUPPORT_EAST
DESC 'LEG SUPPORT BRACKET WITH CURVED WELDED BACKING PAD - EAST'
POS E 14000.00mm N 38435.00mm U 14.50mm

-- 1. Base Mounting Plate (250.28 x 252.79 x 16.00 mm, U: 0..16 mm)
NEW BOX
ORI Z IS U AND X IS E
POS E 1136.14mm N 0.00mm U 8.00mm
XLEN 250.28mm
YLEN 252.79mm
ZLEN 16.00mm

-- Anchor Bolt Hole (Ø43.20mm M36 Clearance Cutout)
NEW NCYLINDER
POS E 48.73mm N 0.00mm U 0.00mm
DIAM 43.20mm
HEIG 40.00mm
NAPPFLAG 2
END
END

-- 2. Curved Welded Backing Pad (R_in=1011.0mm, R_out=1018.2mm, Thk=7.2mm, U: 16..236mm)
NEW EXTRUSION
ORI Y IS N AND Z IS U
POS E 0.00mm N 0.00mm U 16.00mm
HEIG 220.00mm

NEW LOOP
NEW VERTEX
POS E 1000.00mm N -148.70mm U 0.00mm
END
NEW VERTEX
POS E 1003.96mm N -119.12mm U 0.00mm
END
NEW VERTEX
POS E 1007.04mm N -89.43mm U 0.00mm
END
NEW VERTEX
POS E 1009.24mm N -59.66mm U 0.00mm
END
NEW VERTEX
POS E 1010.56mm N -29.84mm U 0.00mm
END
NEW VERTEX
POS E 1011.00mm N 0.00mm U 0.00mm
END
NEW VERTEX
POS E 1010.56mm N 29.84mm U 0.00mm
END
NEW VERTEX
POS E 1009.24mm N 59.66mm U 0.00mm
END
NEW VERTEX
POS E 1007.04mm N 89.43mm U 0.00mm
END
NEW VERTEX
POS E 1003.96mm N 119.12mm U 0.00mm
END
NEW VERTEX
POS E 1000.00mm N 148.70mm U 0.00mm
END
NEW VERTEX
POS E 1007.13mm N 149.76mm U 0.00mm
END
NEW VERTEX
POS E 1011.11mm N 119.96mm U 0.00mm
END
NEW VERTEX
POS E 1014.21mm N 90.06mm U 0.00mm
END
NEW VERTEX
POS E 1016.43mm N 60.09mm U 0.00mm
END
NEW VERTEX
POS E 1017.76mm N 30.06mm U 0.00mm
END
NEW VERTEX
POS E 1018.20mm N 0.00mm U 0.00mm
END
NEW VERTEX
POS E 1017.76mm N -30.06mm U 0.00mm
END
NEW VERTEX
POS E 1016.43mm N -60.09mm U 0.00mm
END
NEW VERTEX
POS E 1014.21mm N -90.06mm U 0.00mm
END
NEW VERTEX
POS E 1011.11mm N -119.96mm U 0.00mm
END
NEW VERTEX
POS E 1007.13mm N -149.76mm U 0.00mm
END
END
END

-- 3. External Sloped Gusset 1 (SOUTH, Thk: 14.87mm, U: 16..196mm)
NEW EXTRUSION
ORI X IS E AND Y IS U
POS E 1013.83mm N -86.73mm U 16.00mm
HEIG 14.87mm

NEW LOOP
NEW VERTEX
POS E 0.00mm N 0.00mm U 0.00mm
END
NEW VERTEX
POS E 237.54mm N 0.00mm U 0.00mm
END
NEW VERTEX
POS E 237.54mm N 15.00mm U 0.00mm
END
NEW VERTEX
POS E 12.00mm N 180.00mm U 0.00mm
END
NEW VERTEX
POS E 0.00mm N 180.00mm U 0.00mm
END
END
END

-- 4. External Sloped Gusset 2 (NORTH, Thk: 14.87mm, U: 16..196mm)
NEW EXTRUSION
ORI X IS E AND Y IS U
POS E 1013.83mm N 101.60mm U 16.00mm
HEIG 14.87mm

NEW LOOP
NEW VERTEX
POS E 0.00mm N 0.00mm U 0.00mm
END
NEW VERTEX
POS E 237.54mm N 0.00mm U 0.00mm
END
NEW VERTEX
POS E 237.54mm N 15.00mm U 0.00mm
END
NEW VERTEX
POS E 12.00mm N 180.00mm U 0.00mm
END
NEW VERTEX
POS E 0.00mm N 180.00mm U 0.00mm
END
END
END

END
