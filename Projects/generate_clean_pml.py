# -*- coding: utf-8 -*-
"""
Generate clean, 100% compliant PML1 macro for CAD_AID_LOOSE_001.
Follows Iron Rules IR-1 (centre POS), IR-2 (ORI before POS), IR-3 (Z IS axis), IR-4/5 (PML1 only, no prologue).
"""

pml_clean = """-- ----------------------------------------------------------------
-- Equipment: /CAD_AID_LOOSE_001
-- Description: East-West Horizontal Column / Vessel Assembly
-- ----------------------------------------------------------------

NEW EQUIPMENT /CAD_AID_LOOSE_001
DESC 'HORIZONTAL COLUMN ASSEMBLY'

NEW SUBEQUIPMENT /CAD_AID_LOOSE_001_BODY

-- Segment 1: East Cylinder (DN275 class)
NEW CYLINDER
DIAM 274.93mm
HEIG 113.21mm
ORI Z IS E AND Y IS U
POS E 73921.12mm N 76361.41mm U 0mm
END

-- Segment 2: Transition Cone (274.93 -> 296.50)
NEW CONE
DTOP 274.93mm
DBOT 296.50mm
HEIG 26.95mm
ORI Z IS E AND Y IS U
POS E 73851.04mm N 76361.41mm U 0mm
END

-- Segment 3: Collar / Flange Ring (OD 393.53)
NEW CYLINDER
DIAM 393.53mm
HEIG 53.91mm
ORI Z IS E AND Y IS U
POS E 73810.61mm N 76361.41mm U 0mm
END

-- Segment 4: Transition Cone (296.50 -> 274.93)
NEW CONE
DTOP 296.50mm
DBOT 274.93mm
HEIG 21.56mm
ORI Z IS E AND Y IS U
POS E 73772.87mm N 76361.41mm U 0mm
END

-- Segment 5: Main Body Cylinder (DN275 class)
NEW CYLINDER
DIAM 274.93mm
HEIG 264.15mm
ORI Z IS E AND Y IS U
POS E 73630.01mm N 76361.41mm U 0mm
END

-- Segment 6: West Reducer Cone (274.93 -> 221.02)
NEW CONE
DTOP 274.93mm
DBOT 221.02mm
HEIG 107.82mm
ORI Z IS E AND Y IS U
POS E 73444.03mm N 76361.41mm U 0mm
END

END
"""

with open("Projects/CAD_AID_LOOSE_001.pml", "w", encoding="utf-8") as f:
    f.write(pml_clean)

print("Wrote clean PML1 macro to Projects/CAD_AID_LOOSE_001.pml")
