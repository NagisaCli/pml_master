# PML-STUDY-HANDRA-001 — Native Structural Handrail (`HANDRA`) Study

## Purpose

Learn the native structural `HANDRA` / `RPATH` / `POINTR` / `CURVE` construction used by
AVEVA E3D for platform, tank-top, and structural walkway handrails, preserve the supplied
native evidence, and establish a reusable builder and test suite.

This study resolves the historical gap noted on 2026-08-10 (`JK-Tank_Build r2`), where an
unverified handrail template failed to render because it lacked the native `RPATH` path
geometry with `POINTR` + `CURVE` (`CURTYP THRU`) structure.

## Receiving runtime

- AVEVA Everything3D 3.1
- E3D Design Mk3.1.11.0 / Mk3.1

## Immutable source evidence

| Evidence | Preserved file | SHA-256 |
|---|---|---|
| Native data listing | `source/2026-08-31_handra_native.txt` | `76efb61dd2b7ab95517c297a089a2ea6616bbd4265b8f1b5c42aba8de0a43f93` |

The original native export is also preserved unchanged at:
`Projects/E3D_Syntax_Lab/imports/2026-08-31_handra_native.txt`.

## Native inventory

| Element | Count | Description |
|---|---:|---|
| `HANDRA` | 1 | Structural handrail parent container (owned by `FRMWORK /402`) |
| `RPATH` | 1 | Route Path geometry definition |
| `POINTR` | 5 | Route points (start, 3 quadrant vertices, end) with `FRAD 100mm` fillet radius |
| `CURVE` | 4 | Mid-arc passing points with `CURTYP THRU` for smooth circular arc interpolation |

## Four-layer semantic analysis

### 1. Database & Hierarchy layer
- **Owner**: Structural framework (`FRMWORK`, e.g. `HANDRA 1 of FRMWORK /402`) or Structure (`STRU`).
- **Parent Element**: `NEW HANDRA`
- **Child Path**: `NEW RPATH` containing ordered child elements `NEW POINTR` and `NEW CURVE`.
- **Block Termination**: Standard E3D native data listing blocks ending with `END` lines.

### 2. Element & Attribute layer
- `POS E ... S ... U ...`: Handrail base/origin position in owning frame or world coordinates.
- `RAILHE 1250mm 750mm`: Dual rail heights (Top rail 1250 mm, intermediate/mid rail 750 mm above platform level).
- `POSTSP 1000mm`: Maximum post spacing along the route path (1000 mm).
- `TANGOF 300mm`: Tangent/end return offset (300 mm).
- `SHOWKP true`: Show kickplate / toe plate (`true` or `false`).
- `BRAD 100mm`: Default bend radius (100 mm).
- `FIRE 0`: Fireproofing rating (0).
- `BUIL false`, `SHOP false`: Fabrication / site status flags.

### 3. Spatial & Route Path Semantics
- `DRNS E 22.5 N`: Tangent vector at the start of the path.
- `DRNE E 22.5 S`: Tangent vector at the end of the path.
- `POINTR`: Definitive vertex of the route path. Carries `FRAD 100mm` (fillet radius).
- `CURVE`: Mid-point curve interpolation.
  - `CURTYP THRU`: Arc passes directly *through* the specified 3D coordinate point.
- **Mathematical Derivation of the Circular Arc**:
  The specimen defines a complete circle of radius $R = 2910\text{ mm}$ ($D = 5820\text{ mm}$),
  centered locally at $(E_c, N_c) = (0, 2910)\text{ mm}$:
  - Start (`POINTR 1`): $\theta = -90^\circ \implies (0, 0)$
  - Arc 1 (`CURVE 1`): $\theta = -45^\circ \implies (2910 \cdot \frac{\sqrt{2}}{2}, 2910 - 2910 \cdot \frac{\sqrt{2}}{2}) = (2057.68, 852.32)$
  - Vertex 1 (`POINTR 2`): $\theta = 0^\circ \implies (2910, 2910)$
  - Arc 2 (`CURVE 2`): $\theta = +45^\circ \implies (2057.68, 4967.68)$
  - Vertex 2 (`POINTR 3`): $\theta = +90^\circ \implies (0, 5820)$
  - Arc 3 (`CURVE 3`): $\theta = +135^\circ \implies (-2057.68, 4967.68) = \text{W } 2057.68\text{, N } 4967.68$
  - Vertex 3 (`POINTR 4`): $\theta = +180^\circ \implies (-2910, 2910) = \text{W } 2910\text{, N } 2910$
  - Arc 4 (`CURVE 4`): $\theta = +225^\circ \implies (-2057.68, 852.32) = \text{W } 2057.68\text{, N } 852.32$
  - End (`POINTR 5`): $\theta = +270^\circ \implies (0, 0)$

### 4. Macro & Execution layer
- Loaded inside an `INPUT BEGIN ... INPUT FINISH` transaction block in native listing mode or via standard `$M` macro when the parent `FRMWORK` is current.
- **Diagnostic on `(47,62) CP: Incomplete command line`**:
  Bare `INPUT END` without an element name/path triggers `(47,62) Incomplete command line` at the macro footer. The clean transaction closing form is `INPUT FINISH` alone (or `INPUT END HANDRA /<name>`). The handrail elements themselves were already constructed and rendered prior to that line.

## User E3D verdict — 2026-08-31

- **Candidate 01**: Successfully loaded and rendered a complete 3D circular structural handrail in AVEVA E3D Design. Top rail, intermediate mid rail, vertical stanchion posts, curved arc segments, and bottom kickplate are fully visible.
- **Evidence screenshot**: `results/2026-08-31_circular_handra_e3d_rendered.png`
  - SHA-256: `6483d9fc45d5677ca5164a478d827afc26333a42f93a61a74212dd23dc96ab9b`

## Trial candidates

| Candidate | Path Type | File | Description |
|---|---|---|---|
| 01 | Full Circular | `candidate/01_circular_handra_trial.pml` | $R=2910\text{ mm}$ ($D=5820\text{ mm}$) 4-quadrant circular handrail (cleaned transaction) |
| 02 | Rectangular Platform | `candidate/02_rectangular_platform_handra.pml` | $6000 \times 4000\text{ mm}$ closed 4-corner perimeter handrail with $150\text{ mm}$ fillet corners |
| 03 | Horseshoe / Open-Arc | `candidate/03_horseshoe_walkway_handra.pml` | Straight East $4000\text{ mm}$ run + $180^\circ$ circular curve return + parallel return run |
| 04 | Sloped Stair / Ramp | `candidate/04_sloped_stair_handra.pml` | Multi-elevation 3D path with bottom/top landings and $+1500\text{ mm}$ sloped rise |

## Status

- **VERIFIED in AVEVA Everything3D 3.1** (User certification 2026-08-31).
- Hierarchy (`FRMWORK` -> `HANDRA` -> `RPATH` -> `POINTR` / `CURVE`), dual rail heights (`RAILHE`), post spacing (`POSTSP`), tangent offset (`TANGOF`), kickplate flag (`SHOWKP`), bend radius (`BRAD`), and circular arc interpolation (`CURTYP THRU`) are all verified.
