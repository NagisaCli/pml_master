# MC Pump Transformation Audit Report (Updated to 2026-08-24 054 Baseline)

**Date**: 2026-08-24  
**Task**: Replicate and transform updated high-fidelity MC pump modeling of `205-PU-054` (Date: 24 Aug 2026 00:24) to specified MC pumps: `203-PU-020`, `204-PU-028 (NEW)`, `205-PU-018`, and `205-PU-038`.

---

## 1. Executive Summary

- **Source Master Model**: Updated `/205_PU_054` (D1 STAGE MC PUMP) containing latest refinement details:
  - Added new `EXTRUSION` / `NXTRUSION` and auxiliary nozzle / cone fittings on `_AID_MOTOR_2`.
  - Updated suction nozzle position (`N 5818mm`).
  - Added construction aid group (`AIDGROUP` with `AIDLINE` and `AIDPOINT`).
  - Total: **9 Subequipments, 4 Nozzles, 274 Primitives**.
- **Target MC Pumps in Scope**:
  1. `/203_PU_020` (025024 / OXYGEN STAGE FEED MC PUMP) — Baseplate Anchor $(E, N, U) = (17095.0, 5685.0, 0.0)$, Lying E-W, Casing/Nozzle West (`rot=CCW`)
  2. `/204_PU_028` (**NEW** / POST OXYGEN WASHER DISCHARGE MC PUMP) — Baseplate Anchor $(E, N, U) = (22370.0, 6986.0, 0.0)$, Lying E-W, Casing/Nozzle East (`rot=CW`)
  3. `/205_PU_018` (D0 STAGE MC PUMP) — Baseplate Anchor $(E, N, U) = (35727.6, 5019.0, 0.0)$, Lying E-W, Casing/Nozzle West (`rot=CCW`)
  4. `/205_PU_038` (EOP STAGE MC PUMP) — Baseplate Anchor $(E, N, U) = (43112.9, 5016.0, 0.0)$, Lying E-W, Casing/Nozzle West (`rot=CCW`)
  5. `/205_PU_054` (D1 STAGE MC PUMP) — Baseplate Anchor $(E, N, U) = (48852.0, 4714.0, 0.0)$, Updated to latest 054 model.
- **Unmodified Equipment**: All remaining 26 equipment items and zone structures are preserved 100% untouched. Total equipment count in the Zone macro is **31**.

---

## 2. Geometric Transformation & Orientation Alignment

### Orientation Basis
1. **`203_PU_020`, `205_PU_018`, `205_PU_038` (90° CCW Rotation)**:
   - Forward machine direction (+Shaft axis): **-E (West)**
   - Motor/Driver: East (+E)
   - Casing/Suction: West (-E)
   - Right side: +N (North)
   - Top: +U
   - Matrix: $\Delta E' = -\Delta N, \quad \Delta N' = +\Delta E, \quad \Delta U' = +\Delta U$
   - Shaft Vector: `ORI Y is U and Z is W`

2. **`204_PU_028` (90° CW Rotation — 东西横躺管口朝E)**:
   - Forward machine direction (+Shaft axis): **+E (East)**
   - Motor/Driver: West (-E)
   - Casing/Suction: East (+E)
   - Right side: -N (South)
   - Top: +U
   - Matrix: $\Delta E' = +\Delta N, \quad \Delta N' = -\Delta E, \quad \Delta U' = +\Delta U$
   - Shaft Vector: `ORI Y is U and Z is E`

---

## 3. Hierarchy and Element Count Verification

| Equipment | Subequipments | Nozzles | Primitives | Orientation | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/205_PU_054` (Source) | 9 | 4 | 274 | Forward +N | **PASS** (Updated) |
| `/203_PU_020` (Target) | 9 | 4 | 274 | Forward -E (West) | **PASS** |
| `/204_PU_028` (**NEW**) | 9 | 4 | 274 | Forward +E (East) | **PASS** |
| `/205_PU_018` (Target) | 9 | 4 | 274 | Forward -E (West) | **PASS** |
| `/205_PU_038` (Target) | 9 | 4 | 274 | Forward -E (West) | **PASS** |

### Key Landmark Locations

#### `/203_PU_020` (025024)
- Baseplate Center: `E 17095mm N 5685mm U 25mm`
- Casing Cylinder: `E 16220.1mm N 5685mm U 622.17mm` (`ORI Y is U and Z is W`)
- Driver Cylinder: `E 17736.2mm N 5685mm U 622.17mm` (`ORI Y is U and Z is W`)
- Suction Nozzle: `E 15991mm N 5685mm U 622.17mm` (`ORI Y is U and Z is S`)
- Discharge Nozzle: `E 16137mm N 5685mm U 1017.97mm` (`ORI Y is W and Z is N`)

#### `/204_PU_028` (NEW — 东西横躺管口朝东 +E)
- Baseplate Center: `E 22370mm N 6986mm U 25mm`
- Casing Cylinder: `E 23244.9mm N 6986mm U 622.17mm` (`ORI Y is U and Z is E`)
- Driver Cylinder: `E 21728.8mm N 6986mm U 622.17mm` (`ORI Y is U and Z is E`)
- Suction Nozzle: `E 23474mm N 6986mm U 622.17mm` (`ORI Y is U and Z is N`)
- Discharge Nozzle: `E 23328mm N 6986mm U 1017.97mm` (`ORI Y is E and Z is S`)

#### `/205_PU_018` (D0 STAGE MC PUMP)
- Baseplate Center: `E 35727.6mm N 5019mm U 25mm`
- Casing Cylinder: `E 34852.7mm N 5019mm U 622.17mm` (`ORI Y is U and Z is W`)
- Driver Cylinder: `E 36368.8mm N 5019mm U 622.17mm` (`ORI Y is U and Z is W`)
- Suction Nozzle: `E 34623.6mm N 5019mm U 622.17mm` (`ORI Y is U and Z is S`)
- Discharge Nozzle: `E 34769.6mm N 5019mm U 1017.97mm` (`ORI Y is W and Z is N`)

#### `/205_PU_038` (EOP STAGE MC PUMP)
- Baseplate Center: `E 43112.9mm N 5016mm U 25mm`
- Casing Cylinder: `E 42238mm N 5016mm U 622.17mm` (`ORI Y is U and Z is W`)
- Driver Cylinder: `E 43754.1mm N 5016mm U 622.17mm` (`ORI Y is U and Z is W`)
- Suction Nozzle: `E 42008.9mm N 5016mm U 622.17mm` (`ORI Y is U and Z is S`)
- Discharge Nozzle: `E 42154.9mm N 5016mm U 1017.97mm` (`ORI Y is W and Z is N`)

---

## 4. Catalogue Element Binding (`OLD NOZZLE` / `CATR`)
All 4 nozzles on each of the 4 target MC pumps + 054 are registered in the epilogue with their SPCO catalogue components:
- `OLD NOZZLE 1 of SUBEQUIPMENT /{TAG}_AID_MOTOR_2` $\to$ `/150lb_Ansi_Flanged/AAZFBB0WW`
- `OLD NOZZLE /{TAG}_SUCTION_NOZZLE` $\to$ `/150lb_Ansi_Flanged/AAZFBB0RR`
- `OLD NOZZLE 2 of SUBEQUIPMENT /{TAG}_SUCTION` $\to$ `/150lb_Ansi_Flanged/AAZFBB0RR`
- `OLD NOZZLE /{TAG}_DISCHARGE_NOZZLE` $\to$ `/150lb_Ansi_Flanged/AAZFBB0RR`

---

## 5. Artifacts and Generated Files
- **Full Zone PML (31 Pumps)**: `Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced/JK_Pump_Build_all_pumps_20260823_mc_replaced.pml`
- **Individual Equipment Macros**:
  - `Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced/203_PU_020.pml`
  - `Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced/204_PU_028.pml`
  - `Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced/205_PU_018.pml`
  - `Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced/205_PU_038.pml`
  - `Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced/205_PU_054.pml`
- **Audit Script**: `Projects/JK_Pump_Build/tools/audit_transformation.py`
