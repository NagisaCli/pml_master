-- ==============================================================================
-- AVEVA E3D / PDMS PML1 Standalone Typical Pipe Support Macro (Single Typical Pipe Support)
-- Purpose: Directly manual optimization, fine-tuning dimensions, adjusting connection details and parameters in E3D
-- Coordinate System: Standard origin (Wall face Y=0, cantilever arm along +N, beam TOS elevation U=0)
-- Components: Channel cantilever beam + angle brace + gusset plate + root stiffeners + dual baseplates + 6x circular anchor bolts
-- Flange Protection: Brace work point within gusset (U -185), 35mm clearance below bottom flange, 100% clash-free!
-- Surface State: Top flange 100% flat, no isolation pads, reserved for pipe shoe/clamp installation
-- ==============================================================================

-- 1. Cleanup old test elements (with handle protection)
/STRU-TYPICAL-PIPE-SUPPORT
handle (2,109)
elsehandle none
  DELETE STRU
endhandle

/EQUI-TYPICAL-PIPE-SUPPORT-HDW
handle (2,109)
elsehandle none
  DELETE EQUI
endhandle

/ZONE-TYPICAL-SUPPORT
handle (2,109)
  NEW SITE /SITE-TYPICAL-SUPPORT
  NEW ZONE /ZONE-TYPICAL-SUPPORT
endhandle

-- 2. Structural members (Structure module: STRU -> FRMW -> SCTN)
/ZONE-TYPICAL-SUPPORT
NEW STRU /STRU-TYPICAL-PIPE-SUPPORT
NEW FRMW /FRMW-TYPICAL-PIPE-SUPPORT

-- [A] Cantilever channel main beam (Profile: /BS-PFC150x75x18, length 1500mm, JUSL CTOP)
NEW SCTN /SCTN-TYPICAL-BEAM
POSS E 0.0 N 16.0 U 0.0
POSE E 0.0 N 1500.0 U 0.0
DRNS PERP
DRNE PERP
JUSL CTOP
SPRE SPCOMPONENT /BS-PFC150x75x18

-- [B] Angle diagonal brace (Profile: /BS-L50x50x6, apex terminates in gusset U -185, zero flange clash!)
NEW SCTN /SCTN-TYPICAL-BRACE
POSS E 0.0 N 16.0 U -470.0
POSE E 0.0 N 1055.0 U -185.0
DRNS PERP
DRNE PERP
JUSL TOAY
SPRE SPCOMPONENT /BS-L50x50x6

-- 3. Hardware, baseplates, welded gussets and fasteners (EQUI -> SUBE -> Primitives)
/ZONE-TYPICAL-SUPPORT
NEW EQUI /EQUI-TYPICAL-PIPE-SUPPORT-HDW
ORI Y IS N AND Z IS U
POS E 0.0 N 0.0 U 0.0

NEW SUBE /SUBE-TYPICAL-HDW

-- [1] Upper wall baseplate (W180 x T16 x H350, center U -75, flush with wall Y 0~16)
NEW BOX
XLEN 180.0
YLEN 16.0
ZLEN 350.0
POS E 0.0 N 8.0 U -75.0

-- [2] 4x Upper plate circular anchor bolts (DIAM 28mm, projection 10mm, spacing 90x270mm)
NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E -45.0 N 21.0 U 60.0

NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E 45.0 N 21.0 U 60.0

NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E -45.0 N 21.0 U -210.0

NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E 45.0 N 21.0 U -210.0

-- [3] Channel beam root welded stiffener (T8 x L80 x H150, center U -75)
NEW BOX
XLEN 8.0
YLEN 80.0
ZLEN 150.0
POS E 0.0 N 56.0 U -75.0

-- [4] Under-beam welded stiffener gusset plate (T8 x L180 x H90, flush to bottom flange, center U -195)
NEW BOX
XLEN 8.0
YLEN 180.0
ZLEN 90.0
POS E 0.0 N 1055.0 U -195.0

-- [5] Lower brace wall mounting plate (W180 x T16 x H160, center U -470)
NEW BOX
XLEN 180.0
YLEN 16.0
ZLEN 160.0
POS E 0.0 N 8.0 U -470.0

-- [6] 2x Lower baseplate circular anchor bolts (DIAM 28mm, projection 10mm, horizontal spacing 90mm)
NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E -45.0 N 21.0 U -470.0

NEW CYLI
DIAM 28.0
HEIG 10.0
ORI Z IS N AND Y IS U
POS E 45.0 N 21.0 U -470.0

-- [7] Lower brace root welded gusset plate (T8 x L80 x H100, center U -470)
NEW BOX
XLEN 8.0
YLEN 80.0
ZLEN 100.0
POS E 0.0 N 56.0 U -470.0

SAVEWORK
-- ==============================================================================
-- Single typical pipe support loaded successfully!
-- View commands:
-- ADD /ZONE-TYPICAL-SUPPORT
-- AUTO CE
-- ==============================================================================
