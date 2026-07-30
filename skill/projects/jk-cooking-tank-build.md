# JK_Cooking_Tank_Build — Cooking Plant Tanks and Vessels

**Scope:** 15 cooking-plant equipment items for AVEVA E3D.  
**Status:** Revisions 1–5 loaded successfully in the user's E3D project.
Revision 5's corrected Blow Tank height/support chain and ground-mounted
vertical bottom-entry agitators were visually accepted by the user as perfect
on 2026-07-30. R5 is archived as the accepted continuation baseline.  
**Folder:** `Projects/JK_Cooking_Tank_Build/`  
**Brief:** [DO.txt](../../Projects/JK_Cooking_Tank_Build/DO.txt)

---

## Delivered

| Metric | Value |
|---|---:|
| Independent equipment macros | 15 |
| Combined convenience macro | 1 |
| E3D primitives | 1,801 |
| Native NOZZLE elements | 80 |
| Hardware primitives | 721 |
| Plan-oriented BOX elements | 458 |
| Non-cardinal BOX orientations | 308 |
| Nozzle/manway SUBE groups | 80 |
| Anchor nuts | 196 |
| Ladder rungs | 224 |
| Blow Tank agitator/internal primitives | 52 |
| Explicit Reference Values | 49 |
| Numerical positioning/bounds checks | 15 / 15 passed |

Regenerate and validate:

```bash
python -m wsb --project JK_Cooking_Tank_Build --dry-run
python -m wsb --project JK_Cooking_Tank_Build --no-timestamp
```

The output folder contains one macro per equipment item,
`JK_Cooking_Tank_Build.pml` for loading the whole set, and the engineering
report.

---

## Source data

| Source | Use |
|---|---|
| `Tank_list.xlsx`, `Sheet1!A1:H16` | 15 names, global bottom-centre coordinates, diameters/envelopes, capacities and two Blow Tank profile strings |
| `Refs/*.png` | 16 plan/side extracts: plan envelope, visible connection bearings and Blow Tank leg/profile arrangement |
| `DO.txt` | Data precedence, total-height definition and authoritative TOP-to-BOTTOM profile-string interpretation |
| Cooking-plant DWG | Supplied but not parsed: no local DWG reader was installed and the file was not uploaded externally |

No workbook value was silently changed. Missing side elevations and nozzle
schedules are explicitly reported as Reference Values.

---

## Modeling decisions

### Capacity-derived atmospheric tanks

For every row marked `CALCULATE BY DIAMETER AND CAPACITY`, the cylindrical
section is resolved from:

```text
H = V / (pi D^2 / 4)
```

The supplied diameter and capacity remain unchanged. A conical-roof rise of
`0.15 D` is added above the capacity cylinder as a Reference Value, so it is not
hidden inside the contractual volume calculation.

### Blow Tank-1 and Blow Tank-2

The workbook's last-cone value was user-confirmed erroneous. Revision 5
preserves the first three TOP-to-BOTTOM segments and applies the corrected
fourth:

```text
CY D3876 H2508
CONE top 3876 -> bottom 7300 H2944
CY D7300 H8753
CONE top 7300 -> bottom 555 H5898
```

The corrected body sum is 20,103 mm. Its DN555 bottom opening is 1,848 mm above
grade, giving 21,951 mm grade-to-top and global top U=21,651 mm from the listed
U=-300 installation datum. Four legs extend from grade to the DN7300 cone/shell
junction at local U=7,746 mm. PML elements remain in the same semantic order.

The corrected profile's gross cylinder/frustum volume is 559.4 m3; the listed
380 m3 is 67.9% of that gross envelope.

### Main Condensate Tank

The non-circular plan dimensions are authoritative: 3400 × 2017 mm. It is
modelled as a horizontal receiver with a 2391.5 mm straight barrel, two D/4 head
envelopes and two saddles. The calculated gross envelope is 9.79 m3; the listed
8 m3 is 81.7% of gross.

### Accumulators, auxiliary accumulators and junk traps

The external sources establish their process functions, not universal
dimensions:

- batch-cooking accumulators balance liquor flows;
- junk traps remove sand/debris from chip-chute circulation;
- blow-tank flash vapour continues to blow-heat recovery.

Pressure-style heads, skirt heights, auxiliary-vessel aspect ratios and all
missing nozzle sizes therefore remain Reference Values pending vendor GAs.

### Nozzles

Revision 3 replaces every former pad/neck/flange primitive stack with one native
E3D `NOZZLE` placeholder in the same connection SUBE. It reuses the shared,
verified `/150lb_Ansi_Flanged/<component>` DN-to-SPCO mapping. Every block is
emitted in catalogue-safe order: `CATR`, flange-face `POS`, `ORI P1 IS`, then
`HEIG`; an independent parser verifies all four values.

The workbook's Blow Tank bottom cone outlet is 555 mm, but DN555 is not present
in that verified catalogue family. Its temporary element is therefore explicitly
labelled as a **DN500 Reference Value placeholder for the authoritative 555 mm
opening**, rather than inventing an unverified catalogue component. All
Reference Value sizes remain replaceable when the vendor nozzle schedule and
receiving-project catalogue are confirmed.

### User-directed detail pass

The first two 2026-07-30 visual reviews requested reasonable maximum detail without
changing supplied basic data. Revisions 2 and 3 therefore add:

- base/skirt/saddle/support-foot anchors with separate studs, washers and nuts;
- vessel/skirt anchor clamp plates and chair webs that carry bolt load back to
  the supported steel;
- support-foot grout pads, sole plates, top load spreaders and gusset webs;
- selective fixed ladders with four different bearings, foundation-level base
  shoes, 350 mm rung pitch and physically connected stand-off brackets;
- leg-connected crossbars below the Blow Tank cylindrical shell, so no lower
  ladder bracket terminates in space;
- ground-mounted central bottom-entry agitators for Blow Tank-1 and Blow Tank-2,
  including grout/baseplate and anchors, vertical motor/gearbox/bearing stack,
  vertical shaft and two horizontal four-blade stages;
- lifting lugs and pin envelopes;
- equipment nameplates with four visible screws;
- grounding lugs and bolts.

Revision 4 adds plan orientation without changing primitive count or any
authoritative vessel dimension. At circular supports, BOX local X is radial,
local Y is tangential and local Z is Up. The same bearing is applied to the
plate, clamp/chair, gussets and foot anchor pattern.

These use `role=hardware/access/detail`, so the authoritative `role=body`
envelopes, supplied diameters, capacities, Blow Tank profile segments and total
heights remain unchanged.

---

## Problems encountered and how they were resolved

| Symptom / risk | Cause | Resolution |
|---|---|---|
| Original generator could only build one-cylinder vertical `TankSpec` items | New project includes authoritative compound profiles and a horizontal receiver | Added generic resolved `EquipmentModel` / `PrimitiveSpec` schema and composite generator in the shared engine |
| Model tuple order differed from emitted PML order | SUBE grouping gathers same-group primitives before moving to the next group | Numerical verifier now compares against the actual first-seen group emission order |
| `ACCUMULATOR_TANK` top head floated above the shell by 877.9 mm in E3D | The global centre-datum correction was wrongly applied to `DISH`; its actual `POS` is the rim/tangent plane | `PMLBuilder.dish()` now passes the rim point through unchanged; top `POS` changed from U 15285.2 to U 14407.3; bottom head and horizontal end heads corrected in the same pass |
| Blow Tank ladders extended unsupported beside the lower cone and appeared to float | The original bracket reach used the maximum vessel radius even where the local profile narrowed, and the rails started 250 mm above grade | Ladders now start on base shoes at U=0, stop at the supported DN7300 shell, and use leg-connected lower crossbars where the cone cannot support a wall bracket |
| Every tank carried the same-side ladder | Access detail was copied uniformly without considering grade access, vessel size or layout variety | Removed ladders from low/auxiliary vessels, retained nine justified ladders and distributed them over E/W/N/S bearings |
| Nozzles looked like repeated basic-primitive stacks | Revision 2 used catalogue-independent pad/neck/flange envelopes | Added `NativeNozzleSpec`, native NOZZLE emission and independent CATR/POS/P1/HEIG verification; all 80 connection groups now contain one catalogue-backed placeholder and no nozzle primitives |
| Blow Tanks lacked their internal agitators | The first source pass captured external vessel geometry only | Added detailed agitator assemblies; the final user-confirmed form is the central ground-mounted vertical bottom-entry arrangement recorded below |
| Blow Tank last cone, clearance, support height and total elevation were wrong | The source string carried H2636 for the final cone and the model landed its DN555 opening at grade; the user supplied corrected H5898 and 1848 mm bottom clearance | Preserved the first three segments, set the final cone to H5898 at local U1848–7746, extended legs from U0 to U7746, and derived local top U21951/global top U21651 |
| Blow Tank agitators appeared on the side although the reference shows a central drive below the cone | A side-entry arrangement was inferred without reading the side-view drive location closely enough | Removed both side assemblies and added ground-mounted vertical bottom-entry drives through the central bottom opening; relative nozzle/access locations move upward with the corrected body datum |
| Support legs and anchor bolts lacked a visible force path | Posts ended against vessel/ground faces and bolts were not tied back to tank steel | Added leg-top spreaders/gussets, grout/sole plates, and connected anchor clamp/chair geometry |
| Skew perimeter clamp plates twisted and failed to meet the cylindrical shell tangentially | Their rectangular dimensions were derived independently from absolute E/N deltas, while every BOX remained aligned to the world axes | Added arbitrary plan rotation to the shared BOX schema/builder/parser; circular hardware now uses fixed local dimensions with X radial and Y tangential, and rotated bounds/orientation are independently verified |
| WSB tests referenced logical project `JK-Project` while its historical folder is `Projects/JK-Tank_Build` | Project lookup previously used only the physical folder name | Added optional `project.json` logical-name metadata; both names resolve without moving the folder and output remains `JK-Project.*` |
| DWG geometry unavailable | No local DWG parser/converter installed | Used the 16 supplied PNG exports and reported the unread DWG rather than uploading it to a third party |

---

## Verification

`tests/test_cooking_tanks.py` covers:

- all 15 workbook rows and unique equipment names;
- local datum at zero and no geometry below foundation;
- no geometry above declared overall height;
- PML1 validation and one EQUI per individual macro;
- one EQUI per item in the combined macro;
- exact capacity-height formula;
- exact Blow Tank segment order, dimensions and total;
- Blow Tank DN555 cone bottom at local U1848, leg tops at U7746,
  grade-to-top U21951 and global top U21651;
- exact 3400 × 2017 Main Condensate Tank plan envelope;
- DISH `POS` at the shell tangent plane and exact shell/head contact;
- exactly one verified native NOZZLE and no primitive stack in every
  nozzle/manway SUBE;
- selective ladders with varied bearings, base shoes and connected brackets;
- Blow Tank ladder limits and lower crossbar-to-leg physical contact;
- ground-mounted central drives, vertical bottom-entry shafts and two
  horizontal impeller stages in both Blow Tanks;
- unchanged body-relative Blow Tank nozzle locations after the datum shift;
- byte-identical normalized R4 macros for all 13 non-Blow-Tank equipment items;
- leg-top spreaders/gussets, foot grout/anchors and tank anchor clamp/chair
  connections;
- quadrant-correct BOX orientation emitted before POS;
- fixed-dimension perimeter clamps whose local X is radial, whose local Y is
  tangential and whose inner edge overlaps the shell connection;
- end-to-end generation of 15 individual macros, combined macro and report.

Result: **17 passed**.

The original R5 applicable project, agent, full, pump, stability and
skill-integrity selection passed **84 tests, with 2 skipped and 3 deselected**.
The later repository archive pass removes the historical logical-name/folder
mismatch through `project.json`; the complete suite then passes
**199 tests, with 2 skipped and 0 failed** before upload.

---

## Reference Values

The generated report itemises 49 Reference Values. The largest groups are:

- conical-roof rise for capacity-derived atmospheric tanks;
- nozzle/manway sizes and elevations;
- accumulator pressure-head and skirt configuration;
- auxiliary accumulator shell height;
- junk-trap hopper/shell/head height;
- horizontal condensate receiver saddles and nozzle schedule;
- Blow Tank support-leg sections and connection schedule;
- replaceable fastener/accessory dimensions added during the visual-detail pass;
- Blow Tank agitator detail dimensions and selective ladder/access arrangement.

---

## Outstanding issues

- Confirm the temporary `/150lb_Ansi_Flanged` family is available and acceptable
  in the receiving project; replace Reference Value DN/elevations from vendor
  schedules, including the DN500 placeholder at the 555 mm Blow Tank outlet.
- Confirm all vendor GA heights, support dimensions, nozzle schedules and exact
  skew bearings.
- Read the DWG when a trusted local parser is available.

---

## Accepted archive and future continuation

The complete R5 project, including source data, drawings, individual macros,
combined macro and report, is versioned in Git. The revision record is
`Projects/JK_Cooking_Tank_Build/archive/R5_ACCEPTED_2026-07-30.md`.

Future user-supplied PML files are expected to be native E3D exports containing
manual edits. The hierarchy and names will usually remain stable, while
attributes may change and new children may be added. Such a file becomes the
working baseline. Before any modification, use
`python -m wsb.pml_compare <R5-or-later-accepted> <native-export>` and build a
preservation set from the hierarchy/attribute differences. Only the new
requested scope may supersede those manual edits.

---

## Lessons promoted

- Batch-cooking accumulator, junk-trap and blow-tank functional knowledge was
  added to [fibreline.md](../equipment/fibreline.md), with primary Valmet
  sources and an explicit warning that function does not establish dimensions.
- Tank/vessel guidance now requires justified selective access, varied ladder
  bearings, real bracket termination, connected support load spreaders and
  anchor clamps; it also prefers native NOZZLE placeholders when a verified
  catalogue mapping is available.
- IR-3a and the PML1 reference now record the verified plan-rotated BOX form:
  `ORI Z IS U AND X IS <bearing>` before POS. Circular-vessel rectangular
  hardware uses radial local X and tangential local Y; world-axis dimension
  decomposition is explicitly prohibited.
- Fibreline memory now records the user-confirmed project variation: these two
  Blow Tanks use central ground-mounted vertical bottom-entry agitators. The
  earlier side-entry interpretation is explicitly marked wrong.
- The native-export reconciliation workflow now treats later user-edited E3D
  exports as the working baseline and requires semantic comparison plus a
  preservation set before modification.
- IR-1 was corrected from a universal centre-datum claim to the verified
  element-specific rule: CYLI/CONE/BOX use centre; DISH uses its rim/tangent
  plane. The screenshot evidence and the exact HEIG/2 offset are recorded in
  the Iron Rules and failure register.
