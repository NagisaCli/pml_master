# JK_Pump_Build — Pump Modeling Verification Report

Generated: 2026-07-29 22:54:31

## Verification scope

- One independent PML file per pump.
- Exactly one E3D `EQUI` hierarchy in each file.
- One combined macro is built directly through a shared `PMLBuilder`,
  with one independent `EQUI` per selected pump and no disk-file splicing.
- Baseplate dimensions and 50 mm thickness checked numerically.
- Baseplate underside centre checked against the project coordinate.
- Suction direction, motor-opposite arrangement and discharge direction checked.
- Contractual coordinates, baseplate dimensions and directions remain unchanged
  by the high-detail construction pass.
- Detailed hierarchy, seated base/driver and flange-face casing fasteners,
  coupling guard, finned motor and service-specific features checked.
- Primitive footprint checked against the rectangular baseplate.
- PML1 banned syntax, primitive ORI/POS order and NOZZLE catalogue order checked.
- The client loaded and visually accepted the current combined macro in E3D
  on 2026-07-29; future changes remain subject to a new visual reload.

## Summary

- Pumps generated: **30**
- Static verification passed: **30**
- Static verification failed: **0**
- Total primitives: **4927**
- Native catalogue nozzles: **60**
- Combined macro static/numerical validation: **PASS**
- One-click combined load file: `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\JK_Pump_Build_All_Pumps.pml`

## Pump-by-pump results

| Excel row | Pump tag | Family | Duty/detail basis | Position — baseplate underside centre (mm) | Baseplate L × W × T (mm) | Main axis driver→casing | Suction | Discharge | Primitives | Drawing | Generated file | Validation |
|---:|---|---|---|---|---:|---|---|---|---:|---|---|---|
| 2 | 203-PU-008 | Standard horizontal centrifugal pump | Dilution/process-water service; `LARGE_PROCESS_PUMP_CORE:HEAVY_DUTY:PROCESS_VOLUTE:BOXED:f18:c12:a8:x4:r3:b4:tm+0:g+1:casing vent and flush boss:NONE` | (13971, 14110, 0) | 2136 × 852 × 50 | N | N | U | 163 | PU_reference/203-PU-008.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\203-PU-008.pml` | PASS — static/numerical |
| 3 | 203-PU-009 | Standard horizontal centrifugal pump | Filtrate/washer-return service; `LARGE_FILTRATE_PUMP_CORE:IEC_STANDARD:FILTRATE_VOLUTE:ROUND:f16:c10:a8:x4:r2:b3:tm+0:g+1:side inspection and drain boss:NONE` | (16137, 14089, 0) | 2129 × 857 × 50 | N | N | U | 153 | PU_reference/203-PU-009.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\203-PU-009.pml` | PASS — static/numerical |
| 4 | 203-PU-011 | Standard horizontal centrifugal pump | Filtrate/washer-return service; `MEDIUM_FILTRATE_PUMP_CORE:IEC_STANDARD:FILTRATE_VOLUTE:TAPERED:f14:c8:a6:x3:r2:b3:tm+0:g+1:side inspection and drain boss:NONE` | (17685, 170, 0) | 1720 × 760 × 50 | N | N | U | 138 | PU_reference/203-PU-011.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\203-PU-011.pml` | PASS — static/numerical |
| 5 | 203-PU-020 | Medium-consistency pulp pump | Medium-consistency stock service; `O2_MC_COMPACT:MC_MAIN_DRIVE:MC_FLUIDIZER:VENTED_CAGE:f14:c10:a6:x3:r4:b4:tm+0:g+1:integrated separation and degassing package:COMPACT_NO_VIEW` | (17095, 5685, 0) | 926 × 760 × 50 | W | W | U | 178 | **UNCONFIRMED — no reference** | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\203-PU-020.pml` | PASS — static/numerical |
| 6 | 203-PU-026 | Standard horizontal centrifugal pump | Booster/high-head service; `MEDIUM_BOOSTER_PUMP_CORE:HIGH_SPEED:HIGH_HEAD_VOLUTE:ROUND:f18:c10:a6:x3:r3:b5:tm+0:g+1:compact pressure tapping and reinforced bearing frame:NONE` | (13809, 358, 0) | 1720 × 760 × 50 | S | S | U | 156 | PU_reference/203-PU-026.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\203-PU-026.pml` | PASS — static/numerical |
| 7 | 203-PU-031 | Standard horizontal centrifugal pump | Booster/high-head service; `O2_TOP_SPOOL_BOOSTER:HIGH_SPEED:HIGH_HEAD_VOLUTE:TAPERED:f16:c8:a6:x3:r3:b4:tm+0:g+1:compact pressure tapping and reinforced bearing frame:NONE` | (15108, 175, 0) | 1353 × 631 × 50 | S | S | U | 147 | PU_reference/203-PU-031.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\203-PU-031.pml` | PASS — static/numerical |
| 8 | 204-PU-003 | Standard horizontal centrifugal pump | Stock/screen-feed service; `LARGE_STOCK_PUMP_CORE:HEAVY_DUTY:STOCK_VOLUTE:BOXED:f20:c14:a8:x4:r5:b5:tm+0:g+1:heavy clean-out cover:NONE` | (20162, -8768, 0) | 2129 × 857 × 50 | N | N | U | 178 | PU_reference/204-PU-003.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\204-PU-003.pml` | PASS — static/numerical |
| 9 | 204-PU-008 | Standard horizontal centrifugal pump | Stock/screen-feed service; `SAND_SEPARATOR_ABRASIVE:HEAVY_DUTY:ABRASIVE_VOLUTE:VENTED_CAGE:f18:c12:a6:x3:r5:b4:tm+0:g+1:heavy clean-out cover:NONE` | (20000, 19210, 0) | 1720 × 760 × 50 | E | E | U | 173 | PU_reference/204-PU-008.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\204-PU-008.pml` | PASS — static/numerical |
| 10 | 204-PU-006 | Standard horizontal centrifugal pump | Stock/screen-feed service; `SECONDARY_SCREEN:HEAVY_DUTY:STOCK_VOLUTE:TAPERED:f18:c12:a6:x3:r4:b4:tm+0:g+1:heavy clean-out cover:NONE` | (20000, 17410, 0) | 1725 × 760 × 50 | E | E | U | 162 | PU_reference/204-PU-006.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\204-PU-006.pml` | PASS — static/numerical |
| 11 | 204-PU-015 | Standard horizontal centrifugal pump | Dilution/process-water service; `LARGE_PROCESS_PUMP_CORE:HEAVY_DUTY:PROCESS_VOLUTE:BOXED:f18:c12:a8:x4:r3:b4:tm+0:g+1:casing vent and flush boss:NONE` | (22512, 14092, 0) | 2135 × 863 × 50 | N | N | U | 163 | PU_reference/204-PU-015.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\204-PU-015.pml` | PASS — static/numerical |
| 12 | 204-PU-016 | Standard horizontal centrifugal pump | Dilution/process-water service; `LARGE_PROCESS_PUMP_CORE:HEAVY_DUTY:PROCESS_VOLUTE:BOXED:f18:c12:a8:x4:r3:b4:tm+0:g+1:casing vent and flush boss:NONE` | (28213, 14089, 0) | 2129 × 857 × 50 | N | N | U | 163 | PU_reference/204-PU-016.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\204-PU-016.pml` | PASS — static/numerical |
| 13 | 204-PU-017 | Standard horizontal centrifugal pump | Filtrate/washer-return service; `MEDIUM_FILTRATE_PUMP_CORE:IEC_STANDARD:FILTRATE_VOLUTE:TAPERED:f14:c8:a6:x3:r2:b3:tm+0:g+1:side inspection and drain boss:NONE` | (25814, 14294, 0) | 1720 × 760 × 50 | N | N | U | 138 | PU_reference/204-PU-017.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\204-PU-017.pml` | PASS — static/numerical |
| 14 | 204-PU-023 | Standard horizontal centrifugal pump | Filtrate/washer-return service; `MEDIUM_FILTRATE_PUMP_CORE:IEC_STANDARD:FILTRATE_VOLUTE:TAPERED:f14:c8:a6:x3:r2:b3:tm+0:g+1:side inspection and drain boss:NONE` | (28520, 415, 0) | 1725 × 760 × 50 | N | N | U | 138 | PU_reference/204-PU-023.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\204-PU-023.pml` | PASS — static/numerical |
| 15 | 205-PU-004 | Medium-consistency pulp pump | Medium-consistency stock service; `D0_REACTOR_MC:MC_MAIN_DRIVE:MC_FLUIDIZER:VENTED_CAGE:f18:c12:a6:x3:r4:b5:tm+0:g+1:integrated separation and degassing package:REACTOR_NO_VIEW` | (30441, -10580, 0) | 1725 × 760 × 50 | E | E | U | 189 | **UNCONFIRMED — no reference** | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-004.pml` | PASS — static/numerical |
| 16 | 205-PU-012 | Standard horizontal centrifugal pump | Dilution/process-water service; `D0_DILUTION_XL:HEAVY_DUTY:PROCESS_VOLUTE:BOXED:f22:c16:a8:x4:r4:b5:tm+0:g+1:casing vent and flush boss:NONE` | (33065, 13825, 0) | 2701 × 1245 × 50 | N | N | U | 181 | PU_reference/205-PU-012.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-012.pml` | PASS — static/numerical |
| 17 | 205-PU-013 | Standard horizontal centrifugal pump | Wire-wash clean-water service; `MEDIUM_WIRE_WASH_PUMP_CORE:HIGH_SPEED:CLEAN_WATER_VOLUTE:ROUND:f18:c8:a6:x3:r2:b4:tm+0:g+1:compact seal housing and pressure tapping:NONE` | (31566, 14294, 0) | 1720 × 760 × 50 | N | N | U | 144 | PU_reference/205-PU-013.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-013.pml` | PASS — static/numerical |
| 18 | 205-PU-018 | Medium-consistency pulp pump | Medium-consistency stock service; `D0_MC_SIDE_SUCTION:MC_MAIN_DRIVE:MC_FLUIDIZER:VENTED_CAGE:f20:c14:a8:x4:r5:b5:tm+0:g+1:integrated separation and degassing package:D0_SIDE_SUCTION` | (35723, 5019, 0) | 2022 × 1051 × 50 | W | S | W | 204 | PU_reference/205-PU-018.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-018.pml` | PASS — static/numerical |
| 19 | 205-PU-024 | Standard horizontal centrifugal pump | Booster/high-head service; `MEDIUM_BOOSTER_PUMP_CORE:HIGH_SPEED:HIGH_HEAD_VOLUTE:ROUND:f18:c10:a6:x3:r3:b5:tm+0:g+1:compact pressure tapping and reinforced bearing frame:NONE` | (41518, 660, 0) | 1720 × 760 × 50 | S | S | U | 156 | PU_reference/205-PU-024.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-024.pml` | PASS — static/numerical |
| 20 | 205-PU-027 | Standard horizontal centrifugal pump | Washer stock-feed service; `LARGE_STOCK_PUMP_CORE:HEAVY_DUTY:STOCK_VOLUTE:BOXED:f20:c14:a8:x4:r5:b5:tm+0:g+1:stock-duty clean-out cover:NONE` | (42218, -8620, 0) | 2135 × 857 × 50 | N | N | U | 180 | PU_reference/205-PU-027.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-027.pml` | PASS — static/numerical |
| 21 | 205-PU-030 | Standard horizontal centrifugal pump | Dilution/process-water service; `LARGE_PROCESS_PUMP_CORE:HEAVY_DUTY:PROCESS_VOLUTE:BOXED:f18:c12:a8:x4:r3:b4:tm+0:g+1:casing vent and flush boss:NONE` | (40868, 14089, 0) | 2129 × 863 × 50 | N | N | U | 163 | PU_reference/205-PU-030.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-030.pml` | PASS — static/numerical |
| 22 | 205-PU-031 | Standard horizontal centrifugal pump | Dilution/process-water service; `LARGE_PROCESS_PUMP_CORE:HEAVY_DUTY:PROCESS_VOLUTE:BOXED:f18:c12:a8:x4:r3:b4:tm+0:g+1:casing vent and flush boss:NONE` | (37916, 14089, 0) | 2129 × 857 × 50 | N | N | U | 163 | PU_reference/205-PU-031.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-031.pml` | PASS — static/numerical |
| 23 | 205-PU-032 | Standard horizontal centrifugal pump | Wire-wash clean-water service; `WIRE_WASH_CORE_UNCONFIRMED:HIGH_SPEED:CLEAN_WATER_VOLUTE:ROUND:f18:c8:a6:x3:r2:b4:tm+0:g+1:compact seal housing and pressure tapping:NONE` | (39418, 14294, 0) | 1671 × 765 × 50 | N | N | U | 144 | **UNCONFIRMED — no reference** | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-032.pml` | PASS — static/numerical |
| 24 | 205-PU-038 | Medium-consistency pulp pump | Medium-consistency stock service; `EOP_MC_LARGE_SEPARATOR:MC_MAIN_DRIVE:MC_FLUIDIZER:BOXED:f20:c14:a8:x4:r5:b5:tm+0:g+1:integrated separation and degassing package:EOP_LARGE_SEPARATOR` | (43119, 5016, 0) | 2000 × 1051 × 50 | W | S | W | 200 | PU_reference/205-PU-038.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-038.pml` | PASS — static/numerical |
| 25 | 205-PU-046 | Standard horizontal centrifugal pump | Dilution/process-water service; `D1_FRONT_DILUTION_COMPACT:IEC_STANDARD:PROCESS_VOLUTE:TAPERED:f14:c10:a6:x3:r2:b3:tm+0:g+1:casing vent and flush boss:NONE` | (45221, 14294, 0) | 1720 × 760 × 50 | N | N | U | 143 | PU_reference/205-PU-046.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-046.pml` | PASS — static/numerical |
| 26 | 205-PU-047 | Standard horizontal centrifugal pump | Filtrate/washer-return service; `LARGE_FILTRATE_PUMP_CORE:IEC_STANDARD:FILTRATE_VOLUTE:ROUND:f16:c10:a8:x4:r2:b3:tm+0:g+1:side inspection and drain boss:NONE` | (46620, 14089, 0) | 2129 × 863 × 50 | N | N | U | 153 | PU_reference/205-PU-047.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-047.pml` | PASS — static/numerical |
| 27 | 205-PU-048 | Standard horizontal centrifugal pump | Dilution/process-water service; `LARGE_PROCESS_PUMP_CORE:HEAVY_DUTY:PROCESS_VOLUTE:BOXED:f18:c12:a8:x4:r3:b4:tm+0:g+1:casing vent and flush boss:NONE` | (48221, 14089, 0) | 2129 × 863 × 50 | N | N | U | 163 | PU_reference/205-PU-048.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-048.pml` | PASS — static/numerical |
| 28 | 205-PU-049 | Standard horizontal centrifugal pump | Wire-wash clean-water service; `MEDIUM_WIRE_WASH_PUMP_CORE:HIGH_SPEED:CLEAN_WATER_VOLUTE:ROUND:f18:c8:a6:x3:r2:b4:tm+0:g+1:compact seal housing and pressure tapping:NONE` | (49674, 14294, 0) | 1720 × 760 × 50 | N | N | U | 144 | PU_reference/205-PU-049.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-049.pml` | PASS — static/numerical |
| 29 | 205-PU-054 | Medium-consistency pulp pump | Medium-consistency stock service; `D1_MC_DUAL_AUX:MC_MAIN_DRIVE:MC_FLUIDIZER:BOXED:f22:c16:a8:x4:r6:b5:tm+0:g+1:integrated separation and degassing package:D1_DUAL_AUX` | (48852, 4714, 0) | 2000 × 1046 × 50 | N | N | U | 212 | PU_reference/205-PU-054.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-054.pml` | PASS — static/numerical |
| 30 | 205-PU-060 | Standard horizontal centrifugal pump | Scrubber circulation service; `MATCHED_SCRUBBER_CIRCULATION_CORE:CHEMICAL_DUTY:CHEMICAL_VOLUTE:VENTED_CAGE:f18:c12:a6:x3:r4:b4:tm+0:g+1:seal-flush manifold and splash shield:NONE` | (46154, -10854, 0) | 1720 × 760 × 50 | E | E | U | 169 | PU_reference/205-PU-060.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-060.pml` | PASS — static/numerical |
| 31 | 205-PU-061 | Standard horizontal centrifugal pump | Scrubber circulation service; `MATCHED_SCRUBBER_CIRCULATION_CORE:CHEMICAL_DUTY:CHEMICAL_VOLUTE:VENTED_CAGE:f18:c12:a6:x3:r4:b4:tm+0:g+1:seal-flush manifold and splash shield:NONE` | (46154, -8256, 0) | 1720 × 760 × 50 | E | E | U | 169 | PU_reference/205-PU-061.png | `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\pumps\205-PU-061.pml` | PASS — static/numerical |

## Modeling parameters and Reference Values

The following values are not vendor GA data. They are explicit Reference
Values scaled from each contractual baseplate and retained in the data/model
report so they can be replaced when vendor documents are issued.

| Pump tag | Shaft CL above datum (mm) | Casing Ø × axial length (mm) | Motor L × W × H (mm) | Suction DN / length (mm) | Discharge DN / length (mm) | Approx. overall height (mm) |
|---|---:|---:|---:|---:|---:|---:|
| 203-PU-008 | 324.1 | 336.7 × 435.7 | 880.0 × 511.2 × 420.5 | DN100 / 250.0 | DN80 / 153.4 | 711.0 |
| 203-PU-009 | 317.7 | 315.9 × 417.3 | 851.6 × 514.2 × 406.8 | DN100 / 250.0 | DN80 / 154.3 | 692.0 |
| 203-PU-011 | 278.5 | 271.5 × 330.2 | 660.5 × 456.0 × 342.9 | DN80 / 206.4 | DN80 / 150.0 | 593.9 |
| 203-PU-020 | 278.3 | 342.6 × 266.7 | 426.0 × 456.0 × 342.6 | DN150 / 150.0 | DN100 / 150.0 | 599.6 |
| 203-PU-026 | 285.6 | 262.8 × 323.4 | 729.3 × 456.0 × 357.2 | DN80 / 206.4 | DN80 / 150.0 | 614.2 |
| 203-PU-031 | 238.9 | 230.0 × 249.0 | 562.8 × 378.6 × 281.7 | DN80 / 162.4 | DN80 / 150.0 | 503.9 |
| 204-PU-003 | 333.8 | 355.0 × 459.9 | 902.7 × 514.2 × 439.0 | DN100 / 250.0 | DN80 / 154.3 | 737.7 |
| 204-PU-008 | 291.0 | 306.1 × 357.8 | 701.8 × 456.0 × 367.9 | DN80 / 206.4 | DN80 / 150.0 | 629.4 |
| 204-PU-006 | 292.7 | 300.4 × 355.4 | 696.9 × 456.0 × 371.5 | DN80 / 207.0 | DN80 / 150.0 | 634.5 |
| 204-PU-015 | 327.7 | 341.1 × 435.5 | 879.6 × 517.8 × 425.9 | DN100 / 250.0 | DN80 / 155.3 | 719.5 |
| 204-PU-016 | 325.7 | 338.7 × 434.3 | 877.1 × 514.2 × 422.9 | DN100 / 250.0 | DN80 / 154.3 | 714.8 |
| 204-PU-017 | 278.5 | 271.5 × 330.2 | 660.5 × 456.0 × 342.9 | DN80 / 206.4 | DN80 / 150.0 | 593.9 |
| 204-PU-023 | 278.5 | 271.5 × 331.2 | 662.4 × 456.0 × 342.9 | DN80 / 207.0 | DN80 / 150.0 | 593.9 |
| 205-PU-004 | 287.0 | 356.6 × 527.9 | 615.8 × 456.0 × 360.1 | DN150 / 241.5 | DN100 / 150.0 | 618.3 |
| 205-PU-012 | 450.0 | 510.9 × 572.6 | 1166.8 × 747.0 × 620.0 | DN150 / 250.0 | DN100 / 224.1 | 1020.4 |
| 205-PU-013 | 282.0 | 254.1 × 316.5 | 729.3 × 456.0 × 350.1 | DN80 / 206.4 | DN80 / 150.0 | 604.1 |
| 205-PU-018 | 389.9 | 512.5 × 630.9 | 743.1 × 630.6 × 522.1 | DN200 / 283.1 | DN150 / 189.2 | 870.3 |
| 205-PU-024 | 285.6 | 262.8 × 323.4 | 729.3 × 456.0 × 357.2 | DN80 / 206.4 | DN80 / 150.0 | 614.2 |
| 205-PU-027 | 333.8 | 355.0 × 461.2 | 905.2 × 514.2 × 439.0 | DN100 / 250.0 | DN80 / 154.3 | 737.7 |
| 205-PU-030 | 327.7 | 341.1 × 434.3 | 877.1 × 517.8 × 425.9 | DN100 / 250.0 | DN80 / 155.3 | 719.5 |
| 205-PU-031 | 325.7 | 338.7 × 434.3 | 877.1 × 514.2 × 422.9 | DN100 / 250.0 | DN80 / 154.3 | 714.8 |
| 205-PU-032 | 283.6 | 255.8 × 307.5 | 708.5 × 459.0 × 352.4 | DN80 / 200.5 | DN80 / 150.0 | 607.7 |
| 205-PU-038 | 392.3 | 517.3 × 630.0 | 742.0 × 630.6 × 527.0 | DN200 / 280.0 | DN150 / 189.2 | 877.1 |
| 205-PU-046 | 282.0 | 283.0 × 337.1 | 674.2 × 456.0 × 350.1 | DN80 / 206.4 | DN80 / 150.0 | 604.1 |
| 205-PU-047 | 319.6 | 318.1 × 417.3 | 851.6 × 517.8 × 409.7 | DN100 / 250.0 | DN80 / 155.3 | 696.5 |
| 205-PU-048 | 327.7 | 341.1 × 434.3 | 877.1 × 517.8 × 425.9 | DN100 / 250.0 | DN80 / 155.3 | 719.5 |
| 205-PU-049 | 282.0 | 254.1 × 316.5 | 729.3 × 456.0 × 350.1 | DN80 / 206.4 | DN80 / 150.0 | 604.1 |
| 205-PU-054 | 393.1 | 519.7 × 636.0 | 749.0 × 627.6 × 529.3 | DN200 / 280.0 | DN150 / 188.3 | 880.0 |
| 205-PU-060 | 291.0 | 288.8 × 350.9 | 701.8 × 456.0 × 367.9 | DN80 / 206.4 | DN80 / 150.0 | 629.4 |
| 205-PU-061 | 291.0 | 288.8 × 350.9 | 701.8 × 456.0 × 367.9 | DN80 / 206.4 | DN80 / 150.0 | 629.4 |

Common Reference Values:

- Driver frame, cooling fins, coupling, guard, skid rails and support feet
  are engineering-proportional geometry, not vendor-confirmed dimensions.
- Exposed anchor/motor fasteners use a three-piece visual envelope:
  filled shank, solid washer around that shank, and cap/hex-head envelope.
  Exact thread pitch, head flats and manufacturer are UNCONFIRMED.
- Motor fin counts are deterministic S/M/L/XL Reference Value tiers,
  not counts measured from the small plan images. Motor ribs run axially
  around the complete 360-degree stator circumference.
- Casing-bolt count tiers are deterministic Reference Values. Their
  centres lie on the protruding cylinder/cone connection-flange band;
  washers bear on its front face and studs penetrate back into it.
- Terminal boxes use a centred top mount where the plan does not prove an
  offset. Cable-gland side, skid cross-members and other small details
  remain bounded Reference Values.
- Volute split flange, casing ribs, back-pull-out bearing bracket, seal
  housing, flexible coupling, guard bands, fan grille, cable gland,
  lifting lug and rating plate are visible engineering-level details.
- Standard horizontal pumps use a single-stage horizontal centrifugal
  back-pull-out arrangement with a volute casing, coupling and TEFC motor.
- Duty-specific external details are differentiated for dilution, filtrate,
  stock/screen feed, booster, wire-wash, washer-feed, MC and scrubber
  circulation services. These classifications come from the supplied names.
- 205-PU-018 and 205-PU-038 are client-confirmed exceptions: their
  driver/casing axis runs E-W (driver east, casing west), while suction
  points S and discharge points W at the same centreline elevation.
- MC pumps add a side degassing/separation assembly and four casing support
  feet. This structural choice is supported by ANDRITZ's published MC-pump
  description of an integrated separation system and a volute with four
  supporting legs.
- Suction/discharge nominal bores use catalogue-supported Reference Values;
  no unsupported bore is silently substituted.

Vendor structural references:

- [ANDRITZ medium-consistency pumps](https://www.andritz.com/products-en/group/pumps/medium-consistency)
- [ANDRITZ pumps for pulp and paper brochure](https://www.andritz.com/resource/blob/699140/af345d60b77d727f79091e1722dae332/hy-andritz-pumps-pulp-paper-brochure-en-data.pdf)
- [Valmet medium-consistency pumps](https://www.valmet.com/pulp/mechanical-pulping/bleaching/pumps/)

## Client-confirmed source corrections

- **205-PU-046 — position:** `(15221, 14294, 0)` → `(45221, 14294, 0)`. Basis: Client confirmation on 2026-07-29.
- **205-PU-061 — position:** `(461554, -8256, 0)` → `(46154, -8256, 0)`. Basis: Client confirmation on 2026-07-29.

## Load instruction

To create all pumps in one operation, select a writable ZONE in
AVEVA E3D Design and load the combined macro:

```text
$M C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output\JK_Pump_Build_All_Pumps.pml
```

To load an individual pump, select a writable ZONE and run:

```text
$M <full path to the pump .pml file>
```

A PASS in this report means static PML1 and numerical geometry checks
passed. It does **not** claim the macro was interactively loaded in E3D.
