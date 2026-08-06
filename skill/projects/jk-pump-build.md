# JK_Pump_Build — Horizontal Pump Batch

## Scope and status

- 30 pump tags from `Projects/JK_Pump_Build/Pump_details.xlsx`.
- One independent `.pml` file per tag.
- One directly generated `JK_Pump_Build_All_Pumps.pml` loading macro containing
  the same 30 independent EQUI elements for one-click import.
- Exactly one `EQUI` per file, with separate SUBEs for baseplate, supports,
  casing, suction, discharge, coupling, driver and MC auxiliaries where fitted.
- High-detail generated geometry: 4,807 primitives and 60 native catalogue
  `NOZZLE` elements.
- Status on 2026-07-29: the first combined high-detail macro loaded
  successfully in E3D; the client confirmed the independent EQUI hierarchy,
  native nozzles and most geometry. The subsequent base-fastener seating and
  casing-fastener connection-flange placement pass static PML1, immutable-input
  and numerical verification for all 30 pumps and the combined macro; 19
  pump-specific regression tests pass. The client reloaded the final version
  and confirmed it visually correct. The 2026-07-30 floating-block removal and
  nozzle remapping preserve that accepted baseline outside the authorized
  sections and pass static/numerical checks. **User-confirmed 2026-08-04:** the
  2026-07-30 revision was reloaded in E3D and accepted; no further changes were
  requested.

## Source data

- Excel supplies tag, description, baseplate underside-centre coordinate,
  baseplate length/width, suction direction and discharge direction.
- `pump_nozzle_modify.xlsx` supplies measured suction/discharge openings plus
  the requested ANSI nozzle/150 lb flange family; its Generic Type autofill
  anomaly is documented rather than silently corrected in the workbook.
- 27 tag-matched top-view PNGs are available.
- No top view exists for `203-PU-020`, `205-PU-004` or `205-PU-032`.
- `Horizontal_Pump_Example.txt` is an E3D-native structural reference only.
  None of its dimensions, coordinates, orientations or proportions were copied.

## Client-confirmed corrections

> **User-corrected 2026-07-29 (JK_Pump_Build).**

- `205-PU-046` position is `(45221, 14294, 0)` mm, superseding Excel
  `(15221, 14294, 0)`.
- `205-PU-061` position is `(46154, -8256, 0)` mm, superseding Excel
  `(461554, -8256, 0)`.
- Every baseplate is 50 mm thick.
- Every pump occupies its own independent EQUI hierarchy.
- `205-PU-018` and `205-PU-038` are special E-W main-axis arrangements:
  driver east, casing west, with the South suction and West discharge nozzles
  on the same horizontal centreline plane. They must not inherit the normal
  suction-defines-longitudinal rule.

These are project-specific requirements and live in the project data/DO rather
than being generalized as defaults for all pump projects.

## Modeling decisions

- The coordinate is the geometric centre of the baseplate underside. The PML
  baseplate BOX is therefore positioned at `U + 25 mm`, because BOX `POS` is its
  geometric centre.
- The local positive longitudinal axis points from the motor toward the pump
  casing. It normally also points toward suction; side-suction special pumps
  keep the nozzle direction independent. The motor is always placed at a
  negative local longitudinal coordinate.
- Standard pumps use a horizontal single-stage centrifugal arrangement:
  suction, casing, coupling and motor share the longitudinal axis.
- MC pumps add a side air-separation/degassing assembly and four casing support
  feet. Structural basis:
  [ANDRITZ medium-consistency pumps](https://www.andritz.com/products-en/group/pumps/medium-consistency)
  and
  [Valmet medium-consistency pumps](https://www.valmet.com/pulp/mechanical-pulping/bleaching/pumps/).
- Native nozzles bind catalogue components first, use flange-face POS, then
  `ORI P1 IS <direction>`. The 2026-07-30 nozzle schedule supplies measured
  opening sizes; each is mapped to the closest bore in the verified project
  catalogue and recorded in the project mapping table.
- The client requested an individual high-realism pass without changing the
  underlying project parameters. Coordinates, baseplate L/W/T, main axis and
  nozzle directions are now locked by an explicit 30-tag regression register.
- Eight service classes now drive visible construction: dilution, filtrate,
  screen feed, booster, wire wash, washer feed, MC and scrubber circulation.
- Each model now includes seated base anchors, a casing split flange and
  flange-face casing fasteners,
  stepped bearing/seal housing, flexible coupling and guard, and a detailed
  finned TEFC motor with feet, end bells, fan grille, terminal box, cable gland,
  lifting lug, nameplate and hold-down fasteners.
- The corrected motor envelopes occupy a realistic proportion of each skid.
  Main and MC auxiliary motors use overlapping axial ribs around the complete
  360° barrel, open lattice fan grilles, and two-piece feet whose inner webs
  intersect the round stator. Static verification checks the frame proportion,
  rib count, four-side angular coverage and rib-to-stator contact.
- The generator now has five motor construction families, eight casing
  families and four coupling-guard families. These choices alter actual
  geometry. Duty details and the three supplied MC arrangements add further
  physical differentiation.
- Matched evidence-equivalent pumps deliberately share profiles; in particular,
  `205-PU-060/061` are the same scrubber-circulation construction and are not
  invented mirror variants.
- Base anchors and motor hold-downs use a three-solid visual envelope (shank,
  filled washer and cap/head) because exact threads and hex flats are not
  available as verified PML1 primitives. They remain Reference Values.
- Base anchors now seat the washer/head on the plate top and embed the remaining
  shank inside the 50 mm plate. Casing fasteners now bear on the cylinder/cone
  connection-flange front face; their bolt-circle centres lie at the midpoint
  of the protruding annular band and their shanks penetrate back into the
  flange.
- `205-PU-018`, `205-PU-038` and `205-PU-054` use distinct MC auxiliary layouts
  based on their tag-specific top views. The missing-view MC pumps remain
  explicitly UNCONFIRMED.

## Problems encountered and resolution

### Source coordinates contained two high-risk defects

Symptoms:

- `205-PU-061` was an order-of-magnitude E-coordinate outlier.
- `205-PU-046` left only about 108 mm between unrelated pump skids and was far
  outside the spatial sequence of adjacent D1 tags.

Resolution:

- Batch generation was stopped at Phase 1.
- The client confirmed both corrected coordinates.
- The source workbook was not edited; corrections carry `CLIENT` provenance in
  `equipment_data.py`.

### The project had no pump data layer

Symptom:

- `python -m wsb --list-projects` reported `JK_Pump_Build` as `no data`.
- The shared WSB engine only had a tank schema/builder and could not verify a
  rectangular pump baseplate datum or suction/motor relationship.

Resolution:

- Added a shared pump schema, pump builder, pump generator and pump-specific
  numerical verifier.
- Added the project `equipment_data.py`.
- Added regression tests covering the 30 independent macros, hierarchy,
  corrected coordinates, 50 mm thickness, motor-opposite-suction rule and
  output file count.

### A high primitive count still produced undersized, repetitive motors

Symptoms:

- The motor envelope was too small for the skid and read as the wrong frame
  size.
- Only a few surface strips represented cooling ribs.
- Motor feet were positioned from the barrel centreline bottom even though they
  sat off centre, leaving a geometric gap to the round barrel.
- After the motor enlargement, the compact MC train could place the motor end
  beyond the bearing-frame start; a 32 mm `max()` then concealed the negative
  gap and made the coupling/guard penetrate adjacent solids.
- The first connected-foot revision left only a narrow edge of each pad on the
  longitudinal rail, with the hold-down bolt centre outside the rail.
- Unique per-tag configuration labels did not guarantee distinct physical
  construction.

Resolution:

- Increased the bounded motor length/height Reference Values and added
  proportion floors, including a length-to-finned-diameter floor for the compact
  missing-view MC pump.
- Replaced surface strips with equal-angle axial CYLI ribs that overlap the
  complete stator circumference; the same correction was applied to MC
  auxiliary motors.
- Replaced the solid fan-grille disc with a bounded open BOX lattice and split
  each foot into a rail-mounted pad plus a barrel-connected inner web.
- Solved the motor-to-casing gap backwards from the bearing-frame rule and the
  required coupling span. Static verification now enforces
  `motor front < bearing start < casing rear` and checks the exact clear span.
- Moved the longitudinal rails under the motor pads and placed the hold-down
  shanks on the rail centreline. The verifier now checks pad/rail plan overlap,
  bolt containment, pad/web elevation contact and barrel-web penetration.
- Made motor, casing and guard enums drive different primitives, not only
  comments. Added the visible `205-PU-027` lateral branch and distinct
  `205-PU-018`, `205-PU-038` and `205-PU-054` MC packages.
- Collapsed evidence-equivalent pairs back to shared core profiles instead of
  fabricating unsupported left/right or accessory variations.

### One-click delivery could not be a disk concatenation

Risk:

- Concatenating 30 completed files would repeat headers/catalogue summaries and
  could conceal duplicate element names or a malformed individual block.

Resolution:

- The all-pumps macro is rebuilt from the 30 authoritative PumpSpec records
  through one shared `PMLBuilder`.
- It retains 30 zero-anchored independent EQUIs, 60 unique nozzles and 60
  inline catalogue bindings.
- The verifier checks global uniqueness/order, then splits the combined macro
  by EQUI and runs the full numerical single-pump verifier on every block.
- Filtered `--tag` generation never overwrites the formal all-pumps macro.

### Casing fasteners were attached to the wrong surface

Symptoms observed after the first successful E3D load:

- Every `BASE_FASTENERS` shank started at the baseplate top, leaving its full
  length exposed between the washer and head instead of entering the plate.
- `CASING_FASTENERS` grew from the split plane toward the tapered front cover.
  The bolt circle therefore intersected the cover and only crescent-shaped
  portions of some heads remained visible.
- Moving the same solids out to the mathematical cone surface produced a second
  failure: the stacks became fully visible but floated on the sloped cover
  without representing a cylinder/cone flange connection.
- Omitting the fasteners avoided the floating geometry, but the client clarified
  that the desired detail is the bolted cylinder/cone joint rather than no
  bolting at all.

Resolution:

- Seated each base washer at the plate top, placed its head immediately above
  it and shifted the shank down so its upper end aligns with the head top while
  its lower end remains inside the plate and above the foundation datum.
- Restored all `CASING_FASTENERS` without changing their Reference-Value
  diameter, length or count. Set the bolt-circle centreline to the midpoint
  between the tapered-cover root radius and the split-flange outside radius.
- Set the washer base to the common cylinder/cone connection plane, place the
  head directly outward and shift the shank backward so it penetrates the
  flange. Numerical regression checks both the annular-band centreline and the
  axial bearing/contact chain.
- Added a canonical SHA-256 regression of all non-target PML geometry. Excluding
  only `BASE_FASTENERS` and `CASING_FASTENERS`, the regenerated combined macro
  retains the exact pre-correction hash
  `a5fce5959232cda68bb343c5fd4a52a5f0c75b4027f9caa4e28734ec8d2dc57c`.

### Floating bearing/coupling blocks and project nozzle measurements

Symptoms:

- The final `BOX` and `CYLI` in every `BEARING_FRAME` appeared as a detached
  pedestal/cap pair without useful visual or physical meaning.
- The final two `BOX` primitives in every `COUPLING` appeared as floating guard
  feet that did not provide credible support.
- The original pump register contained no nozzle schedule, but
  `pump_nozzle_modify.xlsx` later supplied tag-specific suction and discharge
  opening measurements.
- The new workbook's `Generic Type` column contains an apparent autofill error:
  `150Ib Ansi Flanges` becomes `151Ib` through `179Ib`.

Resolution:

- Removed exactly four primitives per pump: the bearing pedestal, bearing cap
  and two coupling-guard support feet. No other primitive dimensions or
  coordinates were changed.
- Mapped all 60 measured openings to the closest verified
  `ANSI-NOZZLES / 150lb_Ansi_Flanged` catalogue DN. An equal-distance tie uses
  the lower DN; `204-PU-017` input 85 mm therefore maps to DN80.
- Changed only the native-nozzle DN comments and inline `CATR SPCOMPONENT`
  paths. Every nozzle `POS`, `ORI`, `HEIG` and process attribute is unchanged.
- Added `output/JK_Pump_Build_nozzle_mapping.md` with all source values,
  selected DNs, deltas and SPCO paths. The source workbook remains unedited and
  its flange-class anomaly is explicitly reported.
- A canonical comparison against the previously accepted combined macro proves
  all non-target geometry unchanged. Static PML1/numerical checks and 19 pump
  regression tests pass; this 2026-07-30 revision still requires a fresh E3D
  visual reload before it can be called E3D-verified.

## Reference Values

The workbook contains no vendor GA, motor schedule or side elevation. The
nozzle workbook supplies opening measurements but no vendor nozzle projections.
The following remain assumptions:

- casing diameter and axial length;
- shaft centreline and overall height;
- motor frame, cooling-fin tier and cable-gland side (terminal boxes are
  centred on top where the plan does not establish an offset);
- coupling and guard;
- skid rails and support feet;
- nozzle projection;
- MC auxiliary separator/drive dimensions.
- casing split/rib details and flange-face bolt count;
- base anchor and motor hold-down bolt visual sizes/counts;
- stepped bearing bracket, seal housing and coupling hardware;
- motor end bells, fin count, fan grille, cable-gland side and lifting details;
- service-specific clean-out, inspection, vent, pressure and seal-flush details.

Every value is scaled from the contractual baseplate and listed in the project
verification report. None is presented as vendor-confirmed data.

## Outstanding issues

- The 2026-07-30 floating-block removal and nozzle remapping were accepted by
  the user on 2026-08-04; no open verification item remains for that revision.
- Replace Reference Values when vendor GA drawings, motor data and nozzle
  schedules are issued or the client opens the retained customization window.
- Re-query the nozzle catalogue mapping if the receiving E3D project changes.
- Exact thread forms, bolt grade, material, motor manufacturer, shaft/seal model,
  terminal orientation and service-accessory dimensions require vendor data.

## Lessons promoted

- No new Iron Rule was needed. Existing centre-datum, ORI-before-POS, catalogue
  binding and one-EQUI-per-equipment rules covered the job.
- The new reusable pump schema/builder/verifier lives in `wsb/`; project data
  remains under `Projects/JK_Pump_Build/`.
- Added `skill/equipment/horizontal-pumps.md`: a high-detail pass must preserve
  contractual datums, differentiate duty-backed construction, and label every
  added fastener/motor/casing detail as a Reference Value rather than fabricated
  vendor data.
- Promoted the connected-motor lesson: full-circumference ribs, round-barrel
  foot contact, open additive grilles and proportion checks are required;
  primitive count alone is not evidence of realism.

## 2026-08-05 — Bridge brackets, hex nuts and clash fixes

The user supplied the accepted model as a fresh native E3D data listing
(`Projects/JK_Pump_Build/imports/2026-08-05_JK_PU_native.txt`); numeric
comparison against the accepted combined macro showed identical geometry —
only representation differs (native POS-first attribute order, omitted default
ORI, trailing CATR pass).

### What was delivered

- `output/JK_Pump_Build_refined_20260805.pml` (55,843 lines) + report + two
  repeatable tools (`tools/refine_bridge_brackets.py`, `tools/verify_refined.py`).
- All 30 pumps: the four solid pump support feet and the four solid motor
  mounting pads were replaced by bridge-type standard brackets — one sole
  plate (BOX) plus two trapezoid gusset plates (EXTRUSION, profile end-plane
  POS). Footprints, bottom faces and bearing heights are unchanged
  (0 mm deviation, all 480 gussets contact their sole plate).
- All 328 circular fastener caps in BASE_FASTENERS / DRIVER_FASTENERS were
  upgraded to true hex nuts (6-vertex EXTRUSION, across-flats equal to the
  original cap diameter, seated on the washer/shand).
- Clash fixes: 205-PU-054 MC separator train moved clear of the casing and
  the separator vessel relocated to the only free skid position; 205-PU-038
  separators seated on the support feet; 205-PU-060/061 splash plate lowered
  clear of the casing.

### Lessons

- A bridge bracket reads correctly as a sole plate carried by two trapezoid
  gussets; keep the gusset bottom at the old pad bottom and the sole-plate top
  at the old pad top so the bearing chain is untouched.
- EXTRUSION `POS` is the profile end plane: a Z=U hex nut's POS is its bottom
  face, not its centre — subtracting half the height double-shifts it.
- When a modelled vessel has no valid footprint on the side where it was
  placed (it overlaps casing, cover cone and a flange ring, and the remaining
  space is smaller than the vessel), the drawing or a numeric placement search
  must decide; here the only feasible position was the motor-side corner.
- Native data listings use POS-first attribute order; `validate_pml`'s
  ORI-before-POS rule targets generator macros and does not apply to this
  loading path.
- Verification properties that caught real bugs: gusset-bottom == pad bottom
  (the first version floated 40 mm), gusset-top == sole-plate bottom,
  nut bottom == washer/shand top, baseplate/nozzle/CATR invariance, and
  targeted clash-pair clearance.

### r2 — MC aux removal and negative-primitive holes (same day)

The client asked to (1) temporarily remove the MC_AUXILIARY subequipment from
the five MC pumps and (2) learn negative primitives: replace the gland-stub
cylinder through each DRIVER terminal-box plate with a `NCYLINDER` child that
carries the stub's own POS/ORI/DIAM/HEIG, then delete the stub. r2 delivers
this for all 30 pumps (one hole each) and removes the five MC subequipment
blocks.

Evidence gathered before emitting: the client's own native listing contains
`NEW NCYLINDER` nested inside positive CYLINDER blocks (inherited pose), and
AVEVA's PMLLIB (`mmmcounterweight.pmlobj`, `mmmconveyortakeup.pmlobj`) creates
nested NBOX/NCYLINDER children with explicit position/orientation. The
knowledge base previously marked NCYLI/NBOX "VERIFIED to fail" for `$M` macro
mode; the r2 form targets the native INPUT data-listing path and is recorded
as EXPERIMENTAL until the user reloads and confirms the holes.

Implementation detail worth keeping: a cylinder's bounding box is symmetric
about its centre for every axis direction (E3D centre datum), so a verifier
that treats POS as an end face for W/S axes silently reverses the AABB and
falsely reports holes "not intersecting" their plates — the verify script was
fixed to use centre-symmetric extents.

### r2 hotfix — "Cannot create a EQUI at this level" (same evening)

The user's E3D load of r2 aborted at `NEW EQUIPMENT /203_PU_026` with
`(41,8) Cannot create a EQUI at this level`. Root cause: in a native INPUT
data listing every SUBEQUIPMENT and EQUIPMENT block ends with its own `END`
(unlike a generated macro where the next NEW closes the block). Deleting the
five MC_AUXILIARY subequipment blocks removed headers and primitives but left
each subequipment's closing END behind; the stray ENDs closed the EQUIPMENT
and then the ZONE, so the fifth EQUI could not be created. Fix: delete the
subequipment's closing END with the block, and replay the INPUT block stack in
the verifier (EQUI only inside ZONE, SUBE only inside EQUI, primitives only
inside SUBE/primitive, no residual stack, END never pops the INPUT level).
Registered as F-18 in diagnosing-failures.md.

### r3 — NCYLI loaded but cut no hole: NAPPFLAG is the gate

After the hierarchy fix the NCYLI holes loaded cleanly but did not cut; the
user proved their own primitive+negative pair does cut. Root cause: a
negative primitive only subtracts when its negative-application flag is 2.
AVEVA's own hole code (`hmcontrol.pmlobj` `.createHoleNegativeExtrusion`)
creates the negative and immediately sets `!!ce.nappflag = 2`;
`strSctnGensec.pmlobj` defaults `NAPPFLAG -1` to 2. r3 emits `NAPPFLAG 2` on
every NCYLINDER. Placement semantics (world POS/ORI vs inherited pose vs
standalone at SUBE level) are isolated in `PML-STUDY-NCYL-001` with the
desktop copy `C:\Users\A\Desktop\NCYLI_test.pml`; the client's verdict on
candidates C1–C4 will promote the exact form to VERIFIED.

### r4 — negative-child POS is local to its owner (user verdict 2026-08-06)

The client loaded the four-candidate test (`PML-STUDY-NCYL-001`, desktop
`NCYLI_test.pml`):

- C2 (child, no POS/ORI) and C3 (child, POS E 0 N 0 U 0 + ORI) cut correctly;
- C1 (child, world-coordinate POS) loaded but cut nothing — a negative
  child's POS is local to the owner, so the world value displaced the hole;
- C4 (standalone NCYLINDER at SUBE level) failed with
  `(41,8) Cannot create a NCYL at this level.`

r4 therefore emits every NCYLINDER with `POS` = removed stub world position
minus the BOX21 owner centre (`POS E 0 N 0 U <dz>`, same ORI/DIAM/HEIG,
`NAPPFLAG 2`). The verifier adds the owner centre back before geometry checks
and asserts the recomposed position equals the removed stub. All 30 pass.
The NCYLI child form is now VERIFIED in pml1-reference.md (F-19/F-20 in
diagnosing-failures.md).

### r5 — hole containment per pump + C-channel skid rails (same day)

The client confirmed the holes cut ("完美挖孔") and settled the NCYLI rules,
then reported that some holes were not adapted per pump and opened through
the plate edge. A per-pump check found 10 pumps whose hole circle exceeded
the BOX21 plate in U (0.10–2.15 mm). Fix: clamp the NCYLI local U offset so
`|dz| + DIAM/2 <= ZLEN/2 - 2 mm`; the axis, diameter and through-length are
unchanged. All 30 holes now sit fully inside their plates.

The client also asked to study the base structure and optimise the pump
bases (JK_PU.txt baseline) without touching any pump-specific attribute.
r5 converts the two solid rectangular skid rails of every SUPPORT_FRAME into
standard C-channel EXTRUSIONs with the identical outer envelope, position,
length and top/bottom elevations (web 8 mm, flange 10 mm Reference Values),
with the channel openings facing the pump centre. Cross beams, bridge
brackets, hex nuts, baseplate and anchors are unchanged. 60 rail EXTRUSIONs
pass the 8-vertex LOOP structure check; no new clashes, lowest point still
U 0.

Lesson: when a feature is repeated across a family with varying geometry
(here: a gland hole in plates of different sizes), the containment must be
checked per instance, not once for the template — a formula that fits one
pump silently opens a hole through the plate edge on another.

### r6 — base reworked to the client's reference (P1501A-BASE)

The client supplied the intended base reference
(`底座结构学习.txt` → archived `PML-STUDY-NCYL-001` sibling import
`2026-08-05_base_structure_reference.txt`): a fabricated pump base with
rectangular bar rails, equipment sole plates, trapezoid gussets, hex
EXTRUSION washers and anchor bolts. The r5 C-channel rails did not match it.

r6 reverts the skid rails to rectangular bars (outer envelope, position and
length unchanged; the rail height is locked by the pump support chain, so the
reference's 20 mm flat-bar height cannot be adopted without raising the whole
train) and upgrades every circular anchor washer in BASE_FASTENERS /
DRIVER_FASTENERS to a hex EXTRUSION washer (across-flats = original diameter,
same thickness, end-plane POS). Nuts seat on the washer top or the shank top,
depending on the original stack layout. 1136 EXTRUSIONs (480 gussets + 328
washers + 328 nuts) all pass structure checks.

Lesson: when the client says "学习这个的底座结构", ask for or archive the
reference export before changing rails — a plausible standard section (C
channel) can be the wrong family even when it fits geometrically.

### r7 — base rebuilt wholesale to the reference (same day)

The client directed a full rebuild: "底座整体直接重构，大小和位置适配就行".
Every solid skid rail is now a built-up I-section (lower flange 20 mm + web
8 mm + upper flange 20 mm, Reference Values) with the identical outer
envelope, centre, length and top/bottom elevations, so the pump support
chain is untouched but the rail reads as a standard fabricated I-beam.
Base anchors were reworked to the reference style: hex washer 12 mm seated on
the baseplate top, shank extended to the nut top, nut raised onto the washer
top; driver washers are hex 12 mm with the nut remaining on the shank top.
Verification: rail envelopes/bearing heights preserved, 328 washers and 328
nuts seated, 30 holes closed, baseplates/nozzles/CATR unchanged, no new
clashes, lowest point U 0.

Lesson: when the client says "整体重构", rebuild the visible structure (rail
section, anchor hardware), not just the tiny parts — small upgrades read as
"no change" in E3D.

### r8 — base copied directly from the reference template (same day)

The client confirmed the intended base is the P1501A-BASE export verbatim
(`pump.txt` is byte-identical to the earlier reference except the export
timestamp) and directed a direct copy with per-pump size/position
adaptation. r8 replaces the SUPPORT_FRAME with the reference construction:

- flat-bar rails (20 mm) seated on the baseplate top, keeping the original
  rail footprint/length;
- PYRAMID solid trapezoid gussets (480 total, 2 per pump/motor foot) from
  the flange-bar top to the sole plates, with the original bearing heights
  preserved;
- 20 mm hex EXTRUSION washers: BASE anchors seated on the baseplate top with
  shanks extended to the nut top and nuts on the washer top; DRIVER washers
  seated on the motor pad top with nuts on the shank top.

Verification now understands PYRAMID (hierarchy, AABB, contact, bearing
chain) and confirms: 480 gussets touch their sole plates, 328 washers and
328 nuts seated, 30 holes closed, baseplates/nozzles/CATR unchanged, no new
clashes, lowest point U 0.

Lesson: "直接照抄" means copy the reference elements themselves (PYRAMID
gussets, flat-bar rails, thick hex washers), not an interpreted equivalent —
the client can tell the difference in E3D.

### r8 re-verification against `pump.txt` (same day)

The client re-issued the adaptation request with the explicit reference path
`C:\Users\A\Desktop\E3D_model_TRAIN\euip\pump.txt` (SHA-256
`AECEBFBB...A77B7`; byte-identical to the archived P1501A-BASE reference
except the export timestamp). A per-pump audit of r8 confirmed the requested
scope is already fully applied on all 30 pumps:

- 60 flat-bar rails (20 mm thick, ZLEN=20) seated on the baseplate top,
  keeping each pump's original rail footprint and length;
- 480 PYRAMID gussets (16 per pump) standing on the rail top (U 70) with
  their top face exactly at the sole-plate bottom (0/480 float);
- 328 hex EXTRUSION washers (208 BASE + 120 DRIVER, 20 mm thick) and 328 hex
  nuts, all seated (BASE nuts on washer top, DRIVER nuts on shank top);
- BASE anchor shanks extended to the nut top; DRIVER shanks unchanged;
- outside the base scope (SUPPORT_FRAME / BASE_FASTENERS /
  DRIVER_FASTENERS / motor pad + gusset blocks) r8 is byte-identical to r7;
  baseplates, nozzles and the CATR pass unchanged; lowest point U 0.

No new revision was needed: r8 is the deliverable for this request. A fresh
E3D visual reload remains the only open item (IR-11d).

### r9 — bases rebuilt to the DBOutput (PUMP006) reference (same day)

The client clarified that the earlier base passes "did not change much"
visually and designated `C:\Users\A\Desktop\DBOutput.txt` (P1502B, template
`/STD/PUMP006`) as the base reference — superseding pump.txt (PUMP005).
DBOutput was archived at
`Projects/JK_Pump_Build/imports/2026-08-06_P1502B_PUMP006_DBOutput.txt`
(SHA-256 `E6EF37E6...`).

`tools/rebuild_base_pump006.py` rebuilds each pump's base (SUPPORT_FRAME,
BASE_FASTENERS, DRIVER_FASTENERS and the motor mounting pads' gussets) to
the PUMP006 construction, adapted per pump:

- 5-member longitudinal frame (2 outer rails + 2 inner rails + centre
  plate), 20 mm tall, seated on the baseplate top with the original rail
  footprint/length; the former transverse cross plates are removed;
- pump-end stand: 2 vertical side plates in the centre gap between the
  pump feet plus 1 cross-beam EXTRUSION spanning between them, height
  capped below the casing/fastener underside (some casings embed into the
  foot plates already); the stand is shifted outward if a low drain/pipe
  blocks its footprint;
- one large (long-axis, XOFF toward centre) + one small (transverse-axis)
  PYRAMID gusset per pump foot and per motor pad — the PUMP006 "big + small"
  pattern from P1502B-BASE;
- anchors: 4 BASE anchors at the pump feet + 4 DRIVER anchors at the motor
  pads (moved from the baseplate corners), each a shank through the
  foot/pad with a 20 mm hex washer on the baseplate top and a hex nut on
  the sole/pad top.

Verification (`tools/verify_r9.py`): hierarchy 30 EQUI / 360 SUBE;
non-base blocks byte-identical to r8 (3365 blocks); baseplates/nozzles/CATR
unchanged; 150 frame members seated; 60 side plates + 30 beams present,
clear of casing/fasteners/suction/discharge; 480 PYRAMIDs bottomed on the
frame top and touching their sole/pad; 240 anchors fully seated with
plausible hex sizes; lowest point U 0; EXTRUSION structure valid; the
large cross-SUBE overlap set is identical to r8 (no new clashes).

Lessons:
- A "reference base" is template-specific: PUMP005 and PUMP006 are
  different constructions, and copying the wrong one produces "no visible
  change" against the client's expectation. Always record the template ID
  (`/STD/PUMP005` vs `/STD/PUMP006`) with the reference.
- When placing new structure under a pump, the casing underside is not a
  flat plane: small drain/seal-flush cylinders and flange fasteners hang
  below the casing and must be treated as footprint-specific blockers
  (union AABB of CASING / CASING_FASTENERS / SUCTION / DISCHARGE), with
  outward trial shifts when the gap is too small.
- A verifier that only checks positions can pass giant hexes: when copying
  reference-sized parts, add physical bounds (hex across-flats < 200 mm);
  the first r9 generated hexes with side length equal to a world anchor
  coordinate (14 m) because the size extraction regex matched the
  EXTRUSION's own POS line instead of the VERTEX profile points.

### r10 — physical support logic (same day, client rejection of r9)

The client rejected r9: "底座物件之間懸空，沒有視覺支撐，螺絲錯位；總之
就是沒有物理邏輯，學了，但是沒有學到精髓" (parts float, no visual
support chain, bolts misplaced -- the reference's physical logic was not
captured). r10 corrects the base construction:

- anchors now pass through the FOOT/PAD CENTRES: 2 per pump foot and 2 per
  motor pad at the quarter points of the long axis (8 BASE + 8 DRIVER =
  480 shanks + 480 hex washers + 480 hex nuts), with the nut seated on the
  sole/pad top and the washer on the baseplate top. r9 had placed the
  anchors at the foot outer edges, so the nuts floated beside the plates;
- the pump-end stand is emitted only when its full stack fits inside the
  frame and is clear of casing/fasteners/suction/discharge: two side plates
  standing on the frame top, a pump-end sole plate CARRIED by them at the
  foot elevation, and a cross-beam tie between the side plates. r9 emitted
  stands capped below the sole plates or shifted outside the frame, leaving
  orphaned parts. 13 pumps receive the stand; 17 are blocked by genuine low
  casing details (drains at U 89.9-180.6, casing fastener rings) and
  correctly skip it;
- support-chain audit: every base element's bottom face rests on a
  supporter (baseplate, frame top, gusset top, side-plate top) within
  0.51 mm -- 0 floating base elements across all 30 pumps.

Lessons promoted:
- "學到精髓" for a fabricated pump base means the support chain reads
  physically: nothing may be emitted merely because it resembles the
  reference. If a feature cannot both carry something and be carried, it
  must not be emitted at all.
- Anchors belong through the foot/pad plate (nut on top), not beside it;
  a bolt whose nut floats next to a plate is the fastest way to lose the
  reference look.
- A stand/riser must be verified inside the FRAME footprint as well as
  under the casing: shifting a stand past the frame end puts its bottom in
  mid-air above the baseplate (20 mm gap), which reads as floating.

### r11 — bridge-bracket supports 横-斜-平-斜-横 (same day, client rejection of r10)

The client rejected the PYRAMID gussets + through-foot anchors: the
diagonals and screws intersected at the same position, the diagonals were
too short to connect to the upper platform, and a bolted auxiliary block
was required at the diagonals' bottom. The requested support cross-section
is a bridge: 横-斜-平-斜-横 (bottom block, diagonal web, middle plate,
diagonal web, upper platform). r11 discards the old gusset/anchor
architecture and emits, under every pump foot and motor pad:

- bottom auxiliary block (12 mm) on the frame top, fixed by 2 screws at
  its transverse edges (nut on the block top, shank into frame/baseplate);
- lower diagonal web: EXTRUSION with a parallelogram (slanted) profile
  from the block top to the middle plate bottom;
- middle horizontal plate (8 mm);
- upper diagonal web from the middle plate top to the platform bottom,
  full-width contact -- the diagonals visibly connect to the upper
  platform;
- the two webs lean in opposite directions (bridge look); the webs are
  transversely narrower than the block (W_p - 2*(hex+18)) so the block-edge
  screws sit beside them with zero intersection; small platforms scale all
  heights proportionally and shrink the nut hex (>=6 mm).

Verification (`tools/verify_r11.py`): hierarchy 30/360; non-base blocks
byte-identical to r8; 0 PYRAMIDs; 240 auxiliary blocks + 240 middle plates
fully seated; 480 diagonal webs with the exact chain
block->web1->middle->web2->platform (contact within 0.51 mm); 480 screws
(8 per pump BASE + 8 DRIVER) with nut on the block top and no screw/nut x
web intersection (exact parallelogram-box test, not AABB); support-chain
audit 0 floating; large cross-SUBE overlap set identical to r8.

Lessons promoted:
- A bracket's "essence" is the support chain AND the clearance of its
  fasteners: when diagonals and bolts share a plan position, move the
  bolts to a zone the webs never occupy (transverse edges with narrower
  webs) rather than shrinking the webs everywhere.
- Slanted EXTRUSION webs have AABBs that overestimate their corners; an
  AABB clash test reports false positives against bolts. Use an exact
  parallelogram-vs-box intersection test for slanted webs.
- Every new part needs a visible purpose: a bolt with its nut beside the
  plate, or a diagonal that stops short of the platform, reads as a
  mistake. The 横-斜-平-斜-横 profile gives each part a neighbour it
  supports and a neighbour that supports it.

### Outstanding

- A fresh E3D visual reload is required before this revision can be called
  accepted (IR-11d). Confirm the 205-PU-054 separator position against its
  top view (moot while MC_AUXILIARY is removed; re-check when re-added).
- The previous r2 load failed at pump 5; the regenerated r2 passes the
  hierarchy-balance replay and needs a fresh load.
- r3 needs the client's E3D verdict: do the 30 holes now cut (NAPPFLAG 2),
  and which candidate form (C1–C4) matches the expected position/direction?
- r4 (owner-relative NCYLI positions) awaits the client's E3D reload; if the
  holes appear at the terminal-box plates, close this thread.
- r5 (hole containment + C-channel skid rails) awaits the client's E3D
  reload; if another reference base structure was meant by "学习这个的底座
  结构和模型", supply its path and the rails will be reworked to match.
- r6 (reference-style base: rectangular rails + hex washers) awaits the
  client's E3D reload.
- r7 (built-up I-section rails + thick hex anchor washers) awaits the
  client's E3D reload.
- r8 (reference-copy base: flat-bar rails + PYRAMID gussets + 20 mm hex
  washers) awaits the client's E3D reload.
- MC_AUXILIARY is temporarily absent on the five MC pumps and must be re-added
  later (its previous clash fixes are moot while removed).
- The 30 NCYLI holes are EXPERIMENTAL pending the user's E3D confirmation;
  after confirmation, promote in pml1-reference.md and reuse negative
  primitives for future hole features.
