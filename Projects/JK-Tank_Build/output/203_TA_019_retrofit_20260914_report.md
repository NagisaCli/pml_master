# 203-TA-019 Equipment and Top Walkway Structure Retrofit Delivery Report (2026-09-14)

## 1. Task Summary and Engineering Context

Following user instructions, implemented four specialized retrofits and geometric corrections on the oxygen stage feed tank `203-TA-019` (including top structure `/203_TA_019_STRU` and equipment `/203_TA_019`) newly exported from AVEVA E3D:
1. **Full-Circle Walkway Conversion**: Expanded from the previous south-only arc ($120^\circ$ sector) to a complete $360^\circ$ annular walkway surrounding the shell perimeter ($R_{\text{out}} = 1900\,\text{mm}$, $R_{\text{in}} = 1000\,\text{mm}$, net width $900\,\text{mm}$), preserving the southern vertical ladder access passage.
2. **Handrail Update**: Updated the top structural curved handrail (`NEW HANDRA`) to a $360^\circ$ fully closed perimeter handrail; west half-ring `/203_TA_019_TOP_HANDRAIL_A` and east half-ring `_B` meet at North center, with smooth turn-ins at the south ladder landing connecting to ladder stringers.
3. **Bottom Dropleg Addition**: Correlated with the side elevation drawing (`Model_reference(Part_Side_View)/203-TA-019.png` clearly indicating a `DN800` dropleg), completed the concentric $\Phi 800\,\text{mm}$ dropleg column and base flange plate between the bottom dished head ($U = 2000\,\text{mm}$) and grade level foundation ($U = 0\,\text{mm}$).
4. **Position Correction**: Corrected bottom pump suction nozzle N9 (previously floating on the west side), translating it to the East side ($E = 16001.5\,\text{mm}, N = 6415\,\text{mm}, U = 500\,\text{mm}$) to penetrate the dropleg shell directly facing the process pump; strictly preserved existing connected pipe elevations and coordinates for N1 and N2 (`/203-POD-350-P12-2501-150/B1` and `/203-PUW-600-P12-2460-150/B1`).

---

## 2. Geometry and Parameter Verification Table

- **Equipment Tag**: `203-TA-019` (PML Name `/203_TA_019`, RefNo `=18409/227848`)
- **Owner**: `ZONE /WSB_TA`
- **Root Container Position (Position WRT Owner)**: `POS E 52402.88mm N 58697.69mm U 0mm` (updated per latest measured survey coordinates)
- **Internal Local Datum Center**: $E = 15445.0\,\text{mm}, N = 6415.0\,\text{mm}$ (all dish heads, cylinders, walkways, and legs referenced to this datum)

| Component / Attribute | Original Exported State | Retrofitted Delivery State | Engineering / Drawing Basis |
| :--- | :--- | :--- | :--- |
| **Top Walkway** (`EXTRUSION`) | South-only arc walkway (W 30° S to E 30° S) | **Full $360^\circ$ Annular Walkway** (R=1000~1900 mm, thickness 50 mm, south opening W250~E250) | Top view `Model_Reference(All_Top_View)/203-TA-019.png` clearly shows full annular walkway |
| **Walkway Brackets** (`BOX`) | South-side 4 bracket sets only (140°, 160°, 200°, 220°) | **Full perimeter 9 radial brackets** (added 0° N, 45° NE, 90° E, 270° W, 315° NW at U=7875) | Uniform support for full walkway, strictly following `Size -> ORI -> POS` |
| **Structural Handrail A (West)** | Semicircular handrail terminating at W 30° S | **$180^\circ$ Arc Handrail**, extending from ladder stringer W240 along R=1840 arc to North center (E 0, N 1840) | Native `CURTYP THRU` arc algorithm, flush with deck at U=8050 |
| **Structural Handrail B (East)** | Semicircular handrail terminating at E 30° S | **$180^\circ$ Arc Handrail**, extending from ladder stringer E240 along R=1840 arc to North center (E 0, N 1840) | Seamlessly closed with West handrail at North center |
| **Bottom Dropleg Baseplate** | Missing (bottom dished head floating unsupported) | **$\Phi 1050\,\text{mm} \times H 50\,\text{mm}$ Circular Flange Plate** (U = 0 ~ 50 mm) | Elevation drawing `Model_reference(Part_Side_View)/203-TA-019.png` bottom flange |
| **Bottom Dropleg Column** | Missing (severe void at U 0 ~ 2000 mm) | **$\Phi 800\,\text{mm} \times H 1950\,\text{mm}$ Vertical Dropleg** (U = 50 ~ 2000 mm) | Elevation drawing clearly marks `DN800`, top connects flush to dished head vertex U=2000 |
| **Bottom Suction Nozzle N9** | West side floating at $E = 14888.5\,\text{mm}$ (opposite pump) | **Corrected to East side $E = 16001.5\,\text{mm}$**, $N = 6415\,\text{mm}, U = 500\,\text{mm}$ | Penetrates DN800 dropleg wall, flange faces East toward process pump suction |
| **Top Connecting Nozzle N1** | $E = 16100\,\text{mm}, N = 6415\,\text{mm}, U = 8600\,\text{mm}$ | **100% Unchanged** | Connects to existing pipe `203-POD-350-P12-2501-150/B1` |
| **Top Feed Nozzle N2** | $E = 15445\,\text{mm}, N = 6415\,\text{mm}, U = 8700\,\text{mm}$ | **100% Unchanged** | Connects to existing pipe `203-PUW-600-P12-2460-150/B1` |
| **Other Nozzles N4 ~ N8** | Coordinates and elevations retained | **100% Retained** | Instrument and vent nozzles |
| **4 Inclined Support Legs & Feet** | Retained as-is | **100% Retained** | 4 sets of pyramid legs + baseplates + anchor bolts fully preserved |
| **South Access Ladder & Safety Cage** | Retained as-is | **100% Retained** | Ladder stringers, rungs, 8 safety cage hoops, and vertical bars fully preserved |

---

## 3. Geometric Elevation Continuity Verification

```
+-------------------------------------------------------------+  U = 8500 mm (Top Dished Head Apex)
|                    NEW DISH Top Head                        |
+-------------------------------------------------------------+  U = 8000 mm (Cylinder Tangent / Walkway U=8000)
|                                                             |  (Walkway top U=8050, handrail base seated at U=8050)
|                                                             |
|                    NEW CYLINDER Main Shell                  |
|                  (DIAM 2000mm, HEIG 5500mm)                 |
|                                                             |
+-------------------------------------------------------------+  U = 2500 mm (Bottom Tangent / Leg Support Interface)
|                    NEW DISH Bottom Head                     |
+-------------------------------------------------------------+  U = 2000 mm (Bottom Dish Head Apex)
|                                                             |
|              NEW CYLINDER DN800 Dropleg Pipe                |  <--- N9 Center Elevation U = 500 mm
|                  (DIAM 800mm, HEIG 1950mm)                  |       Facing East E = 16001.5 mm
|                                                             |
+-------------------------------------------------------------+  U = 50 mm (Bottom Flange Top)
|              NEW CYLINDER Dropleg Foundation Flange Plate   |
+-------------------------------------------------------------+  U = 0 mm (Grade Foundation Datum)
```

Geometric tolerance between all interfaces is **0.0 mm**, with zero clash and zero gap.

---

## 4. Deliverables and Quality Verification

- **PML Deliverables**:
  - **Combined Macro (Both Nodes Unified)**: [`WSB_TA_203_TA_019_retrofit_20260914.pml`](file:///c:/Muvsera/Projects/pml_master/Projects/JK-Tank_Build/output/WSB_TA_203_TA_019_retrofit_20260914.pml)
  - **Main Equipment Macro (Recommended: Walkway + DN800 Dropleg + East N9)**: [`WSB_TA_203_TA_019_EQUI_20260914.pml`](file:///c:/Muvsera/Projects/pml_master/Projects/JK-Tank_Build/output/WSB_TA_203_TA_019_EQUI_20260914.pml)
  - **Structural Handrail Macro (Top Ring Handrail)**: [`WSB_TA_203_TA_019_STRU_20260914.pml`](file:///c:/Muvsera/Projects/pml_master/Projects/JK-Tank_Build/output/WSB_TA_203_TA_019_STRU_20260914.pml)
- **Generator Script**: `Projects/JK-Tank_Build/tools/generate_203_ta_019_retrofit.py`
- **Automated Test Suite**: `tests/test_203_ta_019_retrofit.py`
- **E3D Hierarchy Notes**:
  - E3D error `(41,8) Cannot create a STRU at this level.` occurs if Current Element (CE) is inside `EQUIPMENT` or non-`ZONE` hierarchy.
  - Prior to import, ensure the parent **ZONE** is selected as CE, or import the dedicated EQUI and STRU macros under their respective Zone containers.
- **Verification Results**:
  - `pytest tests/test_203_ta_019_retrofit.py`: **9/9 tests passed** (100% Passed).
  - `validate_pml()` audit: **0 new findings, 0 syntax errors**, strictly adhering to AVEVA E3D PML1 standards and Iron Rules (`Size -> ORI -> POS`).
  - Full-process stack balance: `NEW` and `END` strictly paired; remaining stack depth is 0.
