# TIMELINE — 203_TA_401_BS_Filtrate_Tank

Newest first. **●** marks the current accepted baseline.

| Date | Version / event | Evidence |
|------|-----------------|----------|
| 2026-09-22 | **R2 — precision rebuild.** R1 rejected by the user for model precision and accuracy. True hollow solids via nested `NCYLINDER`/`NBOX`; the separation wall as one `RTORUS` on its fitted R9000.00/9006.35 arc; rafters as true sloped `EXTRUSION`s. 60 solids, 11 nested voids, 12 NOZZLE. Two precision bugs caught by the verifier (rounded arc geometry; `ANGL` at 1 d.p. = 15.7 mm of arc). **Pending E3D visual acceptance.** | `output/203_TA_401_BS_Filtrate_Tank.pml` |
| 2026-09-21 | R1 — first issue, superseded. Full model generated from ANDRITZ 900135359 plus the DWG nozzle-modification notes. 186 primitives, 12 native NOZZLE elements, 18 subequipments. Numeric verification clean; **pending E3D visual acceptance**, so not yet a baseline. | `output/203_TA_401_BS_Filtrate_Tank.pml`, `output/203_TA_401_BS_Filtrate_Tank_report.md` |
| 2026-09-21 | Project established. Source PDF + DWG archived under `imports/`. DWG decoded to DXF with LibreDWG 0.13.4 (npm `dwg2dxf-converter`) and all geometry measured numerically from the 1:1 view copies. | `DO.txt`, `equipment_data.py` |

## Open items

1. **Not yet loaded in E3D.** Nothing here may be called verified until the
   user has loaded the macro and looked at it (IR-11d).
0. **`RTORUS` height datum and attribute order** are the two unsettled forms;
   each is behind one constant in the build script. See the report §7.
2. **Installation coordinate outstanding.** The EQUI is at E 0 N 0 U 0 in
   drawing orientation; the site layout wants it rotated 180° about U.
3. **N2.2 size** — modelled DN300 on the user's direction; the drawing is
   internally inconsistent (DN300 / DN200 / drawn DN150 on the issued sheet).
4. **Engine gap.** `PMLBuilder._orient_nozzle` accepts only the six cardinal
   directions. This vessel needed plan bearings, so `BearingPMLBuilder` in
   `tools/build_203_TA_401.py` extends it locally. Proposed for promotion into
   `wsb/pml_builder.py` — not done unilaterally.
