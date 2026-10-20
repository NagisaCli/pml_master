# 203-PU-409 (BS DD Drum Wash Pump) E3D Modeling Report

- **Equipment Tag**: `/203_PU_409`
- **Duty Description**: `BS DD Drum Wash Pump` (Brown Stock DD Washer Drum Wash Pump)
- **Standard**: AVEVA E3D Design Mk3.1 PML1 Compatible (Iron Rules Verified)
- **Model Files**:
  - `output/203_PU_409.pml`
  - `Projects/JK_Pump_Build/output/203_PU_409.pml`
- **Combined Review Macro**:
  - `output/JK_Pump_Build_203_PU_409_410.pml`
- **Test Suite**: `tests/test_203_pu_410.py` (3/3 test groups passing)

---

## 1. Parameters & Drawing Evidence

| Parameter | Value | Source / Authority |
|---|---|---|
| Baseplate Width | **516.0 mm** | User instruction ("一样的大小") / CAD Plan View |
| Baseplate Length | **1278.0 mm** | User instruction ("一样的大小") / CAD Plan View |
| Baseplate Thickness | **50.0 mm** | Contractual Standing Requirement (`DO.txt`) |
| Shaft Axis | **North (+N)** | User CAD Plan View (motor South, pump casing North) |
| Shaft Elevation | **U 356.00 mm** | Derived to seat Dia 371.5 mm casing with support allowance |
| Local Origin | **(E 0.0, N 0.0, U 0.0) mm** | Geometric centre of baseplate underside (foundation level) |
| Suction Nozzle | **DN100, 150# RF (+N)** | Catalogue `/150lb_Ansi_Flanged/AAZFBB0NN`, face at N +639.0 mm |
| Discharge Nozzle | **DN80, 150# RF (+U)** | Catalogue `/150lb_Ansi_Flanged/AAZFBB0LL`, face at U +641.76 mm |

---

## 2. Structural & Geometric Breakdown

The equipment model contains **1 EQUIPMENT, 6 SUBEQUIPMENT groups, and 91 elements**:

1. **`_BASE` (43 members)**:
   - Piecewise-rigid adaptation of the `/P1501B-BASE` engineering assembly.
   - Outer skid rails (YLEN 1278.0 mm, XLEN 106.24 mm) seated flush from U 0.0 to U 50.0 mm, defining the exact 516.0 x 1278.0 mm plan boundary.
   - Pump and motor sole plates, 12 trapezoid `PYRAMID` stays (geometric center datum per IR-1), 10 `CYLINDER` anchor shanks, and 10 true hexagonal `EXTRUSION` washers/nuts seated on the baseplate.
2. **`_DRIVER` (41 members)**:
   - Foot-mounted totally enclosed fan-cooled (TEFC) electric motor.
   - Dual mirrored `CONE` end frustums tapering to 2/3 diameter outward; outboard rear terminal body is a frustum per accepted r9 standard.
   - Stator barrel (Dia 260.25 mm, length 330.95 mm).
   - 36 axial `CYLINDER` cooling ribs distributed 360° around the stator circumference.
   - Terminal box with negative penetration opening.
3. **`_DRIVE_SHAFT` (3 members)**:
   - Stepped drive shaft cylinder, flexible coupling hub, and contact guard closing the gap between motor and casing with 0.00 mm gap.
4. **`_CASING` (2 members)**:
   - Radially split volute casing cylinder (Dia 371.52 mm, axial length 111.46 mm) centered at N +400.0 mm.
   - Volute end cover `DISH` seated on its tangent/rim plane per IR-1.
5. **`_SUCTION` (1 member)**:
   - Catalogue NOZZLE placeholder `/203_PU_409_SUCTION_NOZZLE` bound to `/150lb_Ansi_Flanged/AAZFBB0NN`.
   - Flange face lands flush at the front edge of the baseplate: `POS E 0mm N 639mm U 356mm`, pointing North (`ORI P1 IS N`).
6. **`_DISCHARGE` (1 member)**:
   - Catalogue NOZZLE placeholder `/203_PU_409_DISCHARGE_NOZZLE` bound to `/150lb_Ansi_Flanged/AAZFBB0LL`.
   - Radial top discharge pointing Up (`ORI P1 IS U`) at `POS E 0mm N 400mm U 641.76mm`, directly penetrating the casing crown with 75% external projection.

---

## 3. Iron Rules & Numerical Verification

- **IR-1 (Element Datums)**: Verified. `BOX`, `CYLINDER`, `CONE`, `PYRAMID` use geometric centre; `DISH` uses flat rim/tangent plane; `EXTRUSION` uses profile end plane.
- **Fastener Coaxiality & Mesh Integrity**: Verified. Corrected native template anomaly where East motor washers (`EXTRUSION`) carried an inverted `ORI Y is S and Z is U`, causing 16.66 mm displacement and mesh facet tearing in E3D. Emitted profile with normalized orientation and exact coaxial alignment with anchor cylinders (plan error < 0.01 mm, seated flush at U 70.83 mm with zero floating geometry).
- **IR-2 (`ORI` before `POS`)**: Verified. All 91 primitives emit `ORI` before `POS`.
- **IR-3 (PML1 Strict)**: Verified. 0 banned PML2 variables, functions, or commands.
- **IR-4 (No Render Prologue)**: Clean macro loaded with `$M <path>`, no `SUSPEND`/`RESUME`/`ALPHA HEADER`.
- **IR-5 (Catalogue NOZZLEs)**: Verified. Both nozzles bind `CATR SPCOMPONENT` first, followed by `POS` and `ORI P1 IS`.
- **IR-6 (Bounds & Foundation)**:
  - Baseplate: E `[-258.0 .. +258.0]`, N `[-639.0 .. +639.0]`, U `[0.0 .. 50.0]` mm.
  - Equipment overall: E `[-258.0 .. +258.0]`, N `[-639.0 .. +639.0]`, U `[0.0 .. 641.8]` mm.
  - Zero foundation penetration: minimum U across all positive solids is 0.00 mm.
  - Zero plan overhang: all elements remain strictly inside the 516 x 1278 mm footprint.

---

## 4. Execution in AVEVA E3D

In AVEVA E3D Command Window:

```pml
-- 1. 导航到可写的设备 ZONE：
/<YOUR_ZONE_NAME>

-- 2. 运行单个 203-PU-409 宏文件：
$M C:\Muvsera\Projects\pml_master\output\203_PU_409.pml

-- 3. 或者运行 203-PU-409 与 203-PU-410 联合审查宏（并排间距 760mm）：
$M C:\Muvsera\Projects\pml_master\output\JK_Pump_Build_203_PU_409_410.pml
```
