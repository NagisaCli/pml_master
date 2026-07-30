# JK_Pump_Build — Phase 1 Pump Inventory and Risk Report

Status: **Phase 1 complete. Both critical coordinates and the baseplate
thickness were confirmed by the client on 2026-07-29; Phase 2 is authorized.**

## Sources inspected

- `Pump_details.xlsx`, `Sheet1!A1:H31`: 30 pump rows.
- `Sheet2` and `Sheet3`: blank.
- `PU_reference/`: 27 readable PNG top views, each linked to the matching Excel
  tag. Three rows explicitly state `no reference`.
- `Horizontal_Pump_Example.txt`: native E3D/exported horizontal-pump structure
  reference only.
- Project rules: `SKILL.md`, `skill/knowledge/iron-rules.md`,
  `skill/workflows/project-structure.md`,
  `skill/workflows/modeling-run.md`, and
  `skill/knowledge/pml1-reference.md`.

## Established coordinate and orientation convention

- Units: millimetres.
- Axes: E = East, N = North, U = Up; positive U is upward.
- Excel coordinate datum: geometric centre of the **underside** of the
  rectangular baseplate.
- Baseplate top elevation = Excel U + baseplate thickness.
- Excel Length is the pump longitudinal/baseplate long dimension; Width is the
  transverse dimension.
- Local longitudinal positive direction is from the motor toward the pump
  casing. It normally equals suction direction. `205-PU-018` and
  `205-PU-038` are client-confirmed exceptions with an E-W main axis.
- Planned world footprint mapping:
  - suction N or S: baseplate `YLEN = Length`, `XLEN = Width`;
  - suction E or W: baseplate `XLEN = Length`, `YLEN = Width`.

## Complete pump inventory

All coordinates below are Excel bottom-face-centre coordinates. `Std-H` means a
standard horizontal centrifugal/end-suction family model. `MC` means a
medium-consistency pump family model with the additional side equipment shown
where a top view exists.

| Excel row | Pump tag | Equipment description | E, N, U (mm) | Baseplate L × W (mm) | Suction / longitudinal direction | Discharge | Preliminary family | Top view | Row-specific issue |
|---:|---|---|---|---:|---|---|---|---|---|
| 2 | 203-PU-008 | BLOW TANK DILUTION PUMP | 13971, 14110, 0 | 2136 × 852 | N | U | Std-H | `203-PU-008.png` | Image has no visible dimension callouts; Excel governs |
| 3 | 203-PU-009 | BSW FILTRATE PUMP | 16137, 14089, 0 | 2129 × 857 | N | U | Std-H | `203-PU-009.png` | None identified |
| 4 | 203-PU-011 | BROWN STOCK DD WASHER RETURN FILTRATE PUMP | 17685, 170, 0 | 1720 × 760 | N | U | Std-H | `203-PU-011.png` | None identified |
| 5 | 203-PU-020 | OXYGEN STAGE FEED MC PUMP | 17095, 5685, 0 | 926 × 760 | W | U | MC | **No reference** | Configuration must be derived from the documented MC family |
| 6 | 203-PU-026 | OXIDISED WL BOOSTER PUMP | 13809, 358, 0 | 1720 × 760 | S | U | Std-H | `203-PU-026.png` | None identified |
| 7 | 203-PU-031 | OXYGEN REACTOR TOP SPOOLING BOOSTER PUMP | 15108, 175, 0 | 1353 × 631 | S | U | Std-H | `203-PU-031.png` | None identified |
| 8 | 204-PU-003 | PRIMARY SCREEN FEED PUMP | 20162, -8768, 0 | 2129 × 857 | N | U | Std-H | `204-PU-003.png` | Drawing shows attached piping extending beyond the baseplate; include only if modeled as documented auxiliary geometry |
| 9 | 204-PU-008 | SAND SEPARATOR FEED PUMP | 20000, 19210, 0 | 1720 × 760 | E | U | Std-H | `204-PU-008.png` | None identified |
| 10 | 204-PU-006 | SECONDARY SCREEN FEED PUMP | 20000, 17410, 0 | 1725 × 760 | E | U | Std-H | `204-PU-006.png` | None identified |
| 11 | 204-PU-015 | PRESSURE SCREEN REJECTION DILUTION PUMP | 22512, 14092, 0 | 2135 × 863 | N | U | Std-H | `204-PU-015.png` | None identified |
| 12 | 204-PU-016 | FEED TANK BOTTOM DILUTION PUMP | 28213, 14089, 0 | 2129 × 857 | N | U | Std-H | `204-PU-016.png` | None identified |
| 13 | 204-PU-017 | POST OXYGEN FILTRATE PUMP | 25814, 14294, 0 | 1720 × 760 | N | U | Std-H | `204-PU-017.png` | None identified |
| 14 | 204-PU-023 | POST OXYGEN DD WASHER RETURN FILTRATE PUMP | 28520, 415, 0 | 1725 × 760 | N | U | Std-H | `204-PU-023.png` | None identified |
| 15 | 205-PU-004 | D0 REACTOR FEED MC PUMP | 30441, -10580, 0 | 1725 × 760 | E | U | MC | **No reference** | Configuration must be derived from the documented MC family |
| 16 | 205-PU-012 | D0 STAGE DILUTION PUMP | 33065, 13825, 0 | 2701 × 1245 | N | U | Std-H, large skid | `205-PU-012.png` | None identified |
| 17 | 205-PU-013 | D0 WASHER WIRE WASH PUMP | 31566, 14294, 0 | 1720 × 760 | N | U | Std-H | `205-PU-013.png` | None identified |
| 18 | 205-PU-018 | D0 STAGE MC PUMP | 35723, 5019, 0 | 2022 × 1051 | S; special main axis W | W | MC | `205-PU-018.png` | Main assembly E-W, driver east/casing west; S and W nozzles coplanar |
| 19 | 205-PU-024 | EOP REACTOR TOP SPOOLING BOOSTER PUMP | 41518, 660, 0 | 1720 × 760 | S | U | Std-H | `205-PU-024.png` | None identified |
| 20 | 205-PU-027 | EOP WASHER FEED PUMP | 42218, -8620, 0 | 2135 × 857 | N | U | Std-H | `205-PU-027.png` | None identified |
| 21 | 205-PU-030 | EOP WASHER FRONT DILUTION PUMP | 40868, 14089, 0 | 2129 × 863 | N | U | Std-H | `205-PU-030.png` | None identified |
| 22 | 205-PU-031 | D0 STAGE DILUTION PUMP | 37916, 14089, 0 | 2129 × 857 | N | U | Std-H | `205-PU-031.png` | Description repeats D0 wording under a later tag; retain as supplied |
| 23 | 205-PU-032 | EOP WASHER WIRE WASH PUMP | 39418, 14294, 0 | 1671 × 765 | N | U | Std-H | **No reference** | Use same-family project drawings only for structure, scaled to this row |
| 24 | 205-PU-038 | EOP STAGE MC PUMP | 43119, 5016, 0 | 2000 × 1051 | S; special main axis W | W | MC | `205-PU-038.png` | Main assembly E-W, driver east/casing west; S and W nozzles coplanar |
| 25 | 205-PU-046 | D1 WASHER FRONT DILUTION PUMP | **45221, 14294, 0** | 1720 × 760 | N | U | Std-H | `205-PU-046.png` | Client-confirmed correction, superseding Excel E=15221 |
| 26 | 205-PU-047 | D1 FILTRATE PUMP | 46620, 14089, 0 | 2129 × 863 | N | U | Std-H | `205-PU-047.png` | None identified |
| 27 | 205-PU-048 | D1 TOWER TOP DILUTION PUMP | 48221, 14089, 0 | 2129 × 863 | N | U | Std-H | `205-PU-048.png` | None identified |
| 28 | 205-PU-049 | D1 WASHER WIRE WASH PUMP | 49674, 14294, 0 | 1720 × 760 | N | U | Std-H | `205-PU-049.png` | None identified |
| 29 | 205-PU-054 | D1 STAGE MC PUMP | 48852, 4714, 0 | 2000 × 1046 | N | U | MC | `205-PU-054.png` | Use the tag-specific auxiliary arrangement shown |
| 30 | 205-PU-060 | SCRUBBER CIRCULATION PUMP | 46154, -10854, 0 | 1720 × 760 | E | U | Std-H | `205-PU-060.png` | None identified |
| 31 | 205-PU-061 | SCRUBBER CIRCULATION PUMP | **46154, -8256, 0** | 1720 × 760 | E | U | Std-H | `205-PU-061.png` | Client-confirmed correction, superseding Excel E=461554 |

## Information available for every pump

- Exact pump tag and description.
- Baseplate underside-centre E/N/U coordinate.
- Baseplate Length and Width.
- Suction direction and discharge direction.
- A tag-matched top view for 27 of 30 pumps.

## Missing information and planned Reference Values

The following are absent for all or nearly all pumps and must not be presented
as project-confirmed data:

- baseplate thickness;
- total equipment height;
- pump casing diameter/height and vendor/model;
- motor power, frame size and shaft elevation;
- coupling and guard dimensions;
- suction/discharge nozzle DN, flange rating, projection and centreline
  elevation;
- support/pedestal/anchor-bolt dimensions;
- material, mass, maintenance envelope and design conditions.

Client-confirmed project value:

- **Baseplate thickness: 50 mm for every pump.**

All remaining dimensions should be derived by pump family from the known
baseplate envelope and the tag-specific top view. They must be listed
individually in the final verification report.

## Resolved critical ambiguities

1. **205-PU-046, Excel row 25:** client confirmed
   `(45221, 14294, 0)` mm.
2. **205-PU-061, Excel row 31:** client confirmed
   `(46154, -8256, 0)` mm.

The source workbook remains unchanged. These corrections are applied in the
project data layer with `CLIENT` provenance.

## Workflow and validation readiness

- `python -m wsb --list-projects` discovers `JK_Pump_Build` but reports
  `no data`: it has no pump dataset/schema registered with the current
  tank-oriented WSB generator.
- The shared `PMLBuilder` can safely emit and validate `BOX`, `CYLI`, `CONE`,
  `DISH` and catalogue `NOZZLE` elements, but there is no pump-specific builder
  or numerical pump verification routine yet.
- Phase 2 therefore requires a pump schema, pump-family builder, one-file-per-tag
  generation path, and numerical checks for baseplate datum/dimensions,
  component footprint and suction/motor orientation.
- Baseline test status before pump changes:
  - full `pytest` collection is blocked because tests still reference a missing
    project name `JK-Project`;
  - after adding the required `JK_Pump_Build/DO.txt`,
    `tests/test_skill_integrity.py` reports 39 passed and 3 failed;
  - the remaining failures are existing project-structure drift:
    hard-coded `JK-Project`, a broken project-log link, and multiple-project
    ambiguity.
- The native `Horizontal_Pump_Example.txt` is not directly executable as the
  project-generated macro template. Among other exported constructs, it writes
  `POS` before `ORI` for primitives, while this project's verified Iron Rule
  requires `ORI` before `POS`. Only its hierarchy and spatial component concept
  may be reused.

## Phase 1 conclusion

- Inventory complete: 30 pumps.
- Reference coverage: 27 top views present, 3 absent.
- Excel footprint/direction fields are complete for all rows.
- No baseplate footprint overlaps were detected using the supplied coordinates
  and suction-derived length/width mapping.
- Batch generation is authorized with one independent EQUI hierarchy per pump.
