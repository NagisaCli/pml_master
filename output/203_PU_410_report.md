# 203-PU-410 (BS DD Return Filtrate Pump) E3D Modeling Report

- **Equipment Tag**: `/203_PU_410`
- **Duty Description**: `BS DD Return Filtrate Pump` (Brown Stock DD Washer Return Filtrate Pump)
- **Standard**: AVEVA E3D Design Mk3.1 PML1 Compatible (Iron Rules Verified)
- **Model Files**:
  - `output/203_PU_410.pml`
  - `Projects/JK_Pump_Build/output/203_PU_410.pml`
- **Test Suite**: `tests/test_203_pu_410.py` (6/6 tests passing)

---

## 1. Parameters & Drawing Evidence

| Parameter | Value | Source / Authority |
|---|---|---|
| Baseplate Width | **516.0 mm** | User CAD Plan View (horizontal dimension) |
| Baseplate Length | **1278.0 mm** | User CAD Plan View (vertical dimension) |
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
   - Exact piecewise-rigid adaptation of the accepted `/P1501B-BASE` engineering assembly.
   - Outer skid rails (YLEN 1278.0 mm, XLEN 106.24 mm) seated flush from U 0.0 to U 50.0 mm, defining the exact 516.0 x 1278.0 mm plan boundary.
   - Pump and motor sole plates, 12 trapezoid `PYRAMID` stays (with geometric center datum per IR-1), 10 `CYLINDER` anchor shanks, and 10 true hexagonal `EXTRUSION` washers/nuts seated on the baseplate.
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
   - Catalogue NOZZLE placeholder `/203_PU_410_SUCTION_NOZZLE` bound to `/150lb_Ansi_Flanged/AAZFBB0NN`.
   - Flange face lands flush at the front edge of the baseplate: `POS E 0mm N 639mm U 356mm`, pointing North (`ORI P1 IS N`).
6. **`_DISCHARGE` (1 member)**:
   - Catalogue NOZZLE placeholder `/203_PU_410_DISCHARGE_NOZZLE` bound to `/150lb_Ansi_Flanged/AAZFBB0LL`.
   - Radial top discharge pointing Up (`ORI P1 IS U`) at `POS E 0mm N 400mm U 641.76mm`, directly penetrating the casing crown with 75% external projection.

---

## 3. Iron Rules & Numerical Verification

- **IR-1 (Element Datums)**: Verified. `BOX`, `CYLINDER`, `CONE`, `PYRAMID` use geometric centre; `DISH` uses flat rim/tangent plane; `EXTRUSION` uses profile end plane.
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
-- 1. Navigate to a writable ZONE:
/<YOUR_EQUIPMENT_ZONE>

-- 2. Run the macro:
$M C:\Muvsera\Projects\pml_master\output\203_PU_410.pml

-- 3. (Optional) If setting out at plant coordinates (E, N, U):
/203_PU_410
POS E <East>mm N <North>mm U <Elev>mm
```
