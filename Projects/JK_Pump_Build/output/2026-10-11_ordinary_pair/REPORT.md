# JK_Pump_Build - Ordinary Pump Pair, 2026-10-11

Two independent equipment models were generated from the latest archived
ordinary-pump native template, `imports/2026-09-10_TEM.txt` (`204-PU-006`).
The later MC and vacuum-pump work is a different equipment family and was not
used for this request.

| Item | User length | User width | Thickness | Main axis | Suction | Discharge |
|---|---:|---:|---:|---|---|---|
| 203-PU-010 | 1724 mm | 760 mm | 50 mm | +E | DN100, +E | DN150, +U |
| 204-PU-022 | 1724 mm | 760 mm | 50 mm | +E | DN100, +E | DN150, +U |

Only the tags, requested baseplate/skid envelope, template coordinate datum,
and the explicit source repairs below change. Pump, motor, drive, support
profiles and PYRAMID axes are retained without scaling or rotation. Each pump
contains one EQUIPMENT, six SUBEQUIPMENT assemblies, 104 positive solids,
two nested negative children, one ELCONN and two catalogue-bound NOZZLEs.
Including LOOP/VERTEX children, there are 196 native nodes per pump.

## Reference Values and unresolved project data

- Baseplate thickness 50 mm: standing client requirement in `DO.txt`, retained
  from the template; the current request specifies length and width only.
- All remaining component dimensions, support heights and fastener sizes:
  Reference Values copied from the 2026-09-10 native template. Shaft centreline
  remains U 418.12 mm above the local baseplate underside.
- Main axis +E, suction +E and discharge +U: Reference Values from the native
  assembly. Nozzle directions are resolved from their physical connections;
  catalogue NOZZLEs are explicitly aimed using `ORI P1 IS`, rather than copying
  geometric-axis clauses from the export.
- DN100 suction (`/150lb_Ansi_Flanged/AAZFBB0NN`) and DN150 discharge
  (`/150lb_Ansi_Flanged/AAZFBB0RR`): template references cross-checked against
  the stored catalogue bore mapping. Availability in the receiving MDB has
  not been checked in a live E3D session.
- Plant installation coordinates, required plant orientation, duty, vendor
  model and tag-specific nozzle schedules: **TBC**. The template's secondary
  screen duty description/function code is not assigned to the new tags.
- Individual files use baseplate underside centre `(0,0,0)` mm. The combined
  review macro stages the second pump at `(0,1520,0)` mm, giving 760 mm clear
  space between the two baseplates. This is a Reference Value review layout,
  not confirmed plant placement. All EQUI origins are explicitly zero.

## Native preservation and source repairs

The immutable source SHA-256 is
`50c22a325a390f4ef7bd0fb91eabde19adfd69bbec43180f7980ea06d6dac09a`.

1. The central plate becomes 1724 x 760 x 50 mm. The four original outer rail
   lengths become 1724 mm. Each rail moves inward by 0.045 mm to reduce the
   native overall width of 760.09 mm to exactly 760 mm.
2. Native rail heights were rounded to 8.33/41.67 mm with thickness 16.67 mm,
   extending 0.005 mm beyond the U=0/U=50 faces. Centres are corrected to
   8.335/41.665 mm, seating those faces exactly without changing thickness.
3. One DRIVER BOX carried invalid `ZLEN -5.25mm` at native position
   `(19571.45,17592.78,392.73)` mm. The candidate uses `ZLEN 5.25mm`, preserving
   its centre and absolute span. This is an explicit Reference Value repair,
   pending visual review; it is not a vendor-confirmed dimension.
4. Primitive ORI is emitted before POS. Each NOZZLE binds its native CATR
   first, followed by POS and `ORI P1 IS`. Export error/synonym wrappers and
   deferred rebinding passes are replaced by balanced creation blocks.
5. Native NCONE/NCYLINDER children remain inside their original positive
   owners, with local zero position/orientation inherited. `NAPPFLAG 2` is
   restored so the intended openings can subtract after import.

## Offline verification

The finished files were re-read through the shared native creation-tree reader.
Source/candidate hierarchy, all non-target dimensions and local child profiles
were compared numerically. Positive solid bounds use the actual native local
axes; PYRAMIDs use geometric-centre datums, DISH uses its rim plane and
EXTRUSION uses its profile end plane. CTORUS bounds conservatively enclose the
actual swept arc, not an unused full circle.

- Individual baseplate bounds: E -862..862, N -380..380, U 0..50 mm.
- Every positive solid lies on or above U=0 and inside the baseplate plan.
- Discharge nozzle root meets its casing CONE top with 0.000 mm terminal gap.
- Suction barrel root remains inside the casing barrel at shaft elevation.
- All ten original anchor/hex pairs are retained; maximum plan axis offset
  is 0.006009 mm, within native export rounding.
- Combined names are unique; both equipment blocks close back to the selected
  ZONE. No source tag, SAVEWORK, deletion or project-session command is emitted.
- Five mutations were rejected: wrong baseplate width, buried gusset, missing
  native solid, invalid catalogue binding and moved local negative child.
- Focused regression suite: 95 tests passed across the native-template reader,
  PML validation/parser/comparison and skill integrity tests.

See `AUDIT.json` for per-item results and output SHA-256 hashes. These checks
prove offline preservation and geometry properties. Native catalogue readback,
macro loading, graphical acceptance and persistence are **not verified**.

## Deliverables and loading

- `203-PU-010.pml`: first pump, local bottom-centre origin.
- `204-PU-022.pml`: second pump, local bottom-centre origin.
- `JK_Pump_Build_203_PU_010_204_PU_022_20261011.pml`: both independent pumps in
  the temporary review layout.

Select a writable ZONE, then run the combined macro:

```pml
$M C:\Muvsera\Projects\pml_master\Projects\JK_Pump_Build\output\2026-10-11_ordinary_pair\JK_Pump_Build_203_PU_010_204_PU_022_20261011.pml
```

Use either the combined macro or the individual macros for a fresh import;
their names refer to the same equipment. The macros contain no Save Work.
Reproduce and verify with:

```powershell
python Projects/JK_Pump_Build/tools/build_ordinary_pair_20261011.py
```

## Lessons recorded

The previous generated-model checker rejected legitimate native Y-first and
tilted motor-fin orientations. Native-template validation now explicitly checks
the actual orthonormal frame while retaining the existing default conventions
and nozzle/order checks. Native export status alone also did not guarantee
positive dimensions: the -5.25 mm BOX was caught by a physical bounds check.
