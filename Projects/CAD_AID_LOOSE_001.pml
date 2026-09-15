-- ====================================================================
-- Equipment: CAD_AID_LOOSE_001 (Updated 7 Segments, East to West)
-- Start Point (East): E 34626.6mm N 5019mm U 622.17mm
-- Total Length: 609.16 mm, End Point (West): E 34017.44mm N 5019mm U 622.17mm
-- ====================================================================

-- Segment 1: East Flange Cylinder (CAD X: [31840.10, 31861.66])
-- Range: E 34626.60 -> E 34605.04 (Length = 21.56 mm, Diam = 285.71 mm)
NEW CYLI
DIAM 285.71
HEIG 21.56
ORI Z IS W AND Y IS U
POS E 34615.82 N 5019.00 U 622.17 WRT /*

-- Segment 2: East Shaft Cylinder (CAD X: [31726.89, 31840.10])
-- Range: E 34605.04 -> E 34491.83 (Length = 113.21 mm, Diam = 274.93 mm)
NEW CYLI
DIAM 274.93
HEIG 113.21
ORI Z IS W AND Y IS U
POS E 34548.43 N 5019.00 U 622.17 WRT /*

-- Segment 3: Transition Cone 1 (CAD X: [31699.94, 31726.89])
-- Range: E 34491.83 -> E 34464.87 (Length = 26.95 mm, East D = 274.93 mm, West D = 296.50 mm)
NEW CONE
DTOP 296.50
DBOT 274.93
HEIG 26.95
ORI Z IS W AND Y IS U
POS E 34478.35 N 5019.00 U 622.17 WRT /*

-- Segment 4: Central Flange Cylinder (CAD X: [31646.03, 31699.94])
-- Range: E 34464.87 -> E 34410.97 (Length = 53.91 mm, Diam = 393.53 mm)
NEW CYLI
DIAM 393.53
HEIG 53.91
ORI Z IS W AND Y IS U
POS E 34437.92 N 5019.00 U 622.17 WRT /*

-- Segment 5: Transition Cone 2 (CAD X: [31624.47, 31646.03])
-- Range: E 34410.97 -> E 34389.40 (Length = 21.56 mm, East D = 296.50 mm, West D = 274.93 mm)
NEW CONE
DTOP 274.93
DBOT 296.50
HEIG 21.56
ORI Z IS W AND Y IS U
POS E 34400.18 N 5019.00 U 622.17 WRT /*

-- Segment 6: Main Body Cylinder (CAD X: [31360.32, 31624.47])
-- Range: E 34389.40 -> E 34125.25 (Length = 264.15 mm, Diam = 274.93 mm)
NEW CYLI
DIAM 274.93
HEIG 264.15
ORI Z IS W AND Y IS U
POS E 34257.33 N 5019.00 U 622.17 WRT /*

-- Segment 7: West Reducer Cone (CAD X: [31252.50, 31360.32])
-- Range: E 34125.25 -> E 34017.44 (Length = 107.82 mm, East D = 274.93 mm, West D = 221.02 mm)
NEW CONE
DTOP 221.02
DBOT 274.93
HEIG 107.82
ORI Z IS W AND Y IS U
POS E 34071.34 N 5019.00 U 622.17 WRT /*
