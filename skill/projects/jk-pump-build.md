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

The client confirmed the holes cut ("holes cut perfectly") and settled the NCYLI rules,
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
(archived as the `PML-STUDY-NCYL-001` sibling import
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

Lesson: when the client says "study this base structure", ask for or archive the
reference export before changing rails — a plausible standard section (C
channel) can be the wrong family even when it fits geometrically.

### r7 — base rebuilt wholesale to the reference (same day)

The client directed a full rebuild: "rebuild the base wholesale; just adapt the size and position".
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

Lesson: when the client says "rebuild wholesale", rebuild the visible structure (rail
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

Lesson: "copy directly" means copy the reference elements themselves (PYRAMID
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

The client rejected r9: "parts float, there is no visual support, and the bolts are misplaced; in short
there is no physical logic - studied, but the essence was not captured". r10 corrects the base construction:

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
- "capture the essence" for a fabricated pump base means the support chain reads
  physically: nothing may be emitted merely because it resembles the
  reference. If a feature cannot both carry something and be carried, it
  must not be emitted at all.
- Anchors belong through the foot/pad plate (nut on top), not beside it;
  a bolt whose nut floats next to a plate is the fastest way to lose the
  reference look.
- A stand/riser must be verified inside the FRAME footprint as well as
  under the casing: shifting a stand past the frame end puts its bottom in
  mid-air above the baseplate (20 mm gap), which reads as floating.

### r11 — bridge-bracket supports horizontal-diagonal-flat-diagonal-horizontal (same day, client rejection of r10)

The client rejected the PYRAMID gussets + through-foot anchors: the
diagonals and screws intersected at the same position, the diagonals were
too short to connect to the upper platform, and a bolted auxiliary block
was required at the diagonals' bottom. The requested support cross-section
is a bridge: horizontal-diagonal-flat-diagonal-horizontal (bottom block, diagonal web, middle plate,
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
  mistake. The horizontal-diagonal-flat-diagonal-horizontal profile gives each part a neighbour it
  supports and a neighbour that supports it.

### FAILURE RECORD — r11 rejected, base thread closed (same day)

Client verdict on r11 after loading: "complete failure: the base support and the pump/
motor are completely separated". No modification requested. r9-r11 are all recorded
as rejected base revisions; the base optimisation thread is CLOSED until
new direction arrives. The day's accepted work is the negative-primitive
(NCYLI) series only (r2-r5 rules VERIFIED: child-only, owner-relative POS,
NAPPFLAG 2, per-pump hole containment).

Lesson (write-back): a numerically "connected" support chain (contact
tests within 0.51 mm) does not guarantee the model reads as connected in
E3D. The final failure -- base and pump/motor visibly separated -- means
the datum/connection between the support brackets and the pump/motor feet
was wrong at a level the local checks did not model (the checks verified
contacts inside the base assembly, not the assembly's connection to the
casing/motor). Any future base work must verify the SUPPORT-TO-PUMP/
MOTOR bearing surfaces against the actual casing/motor foot datums, not
only internal bracket contacts.

### r12 — foundation repair, rebased on r8 (2026-08-07)

The client asked for the foundation defects and physical-representation
errors to be repaired, with pump positions, nozzle locations and baseplate
overall dimensions held fixed.

Two separate findings, both established by measurement rather than by
re-reading the reference:

1. **Why r11 failed.** Measured footprint-aware, r8 has 0/30 defective
   bearing interfaces and r11 has 30/30, with the base ending 40.7–112.6 mm
   below the machine. r11's bracket stack was shorter than the sole plate it
   replaced and never reached the casing/motor foot. Its verifier passed it
   because it only tested contacts *inside* the base assembly — the blind
   spot the r11 failure record had already named. r12 therefore rebases on
   **r8**, not r11.
2. **The genuine inherited defect.** In r8 (and so in every later revision)
   all 60 support interfaces had a **void of 10.5–54.3 mm** between the
   gusset top and the bearing plate above it, and 59 of 60 gussets were
   **buried** below the frame top. The machine sat correctly on its plates;
   the plates rested on nothing.

r12 replaces the 480 decorative PYRAMID gussets with 240 fabricated
plate-girder pedestals — bottom flange seated on the frame top, two vertical
web plates at full clear height, one transverse stiffener — sized per foot
from the measured plate underside, so pump-end and motor-end heights differ
naturally. 480 hold-down anchors run from inside the frame through the plate
with the hex nut on the plate top. **The bearing plates themselves are never
moved**; moving them is what destroyed r11.

Result: voids 60 → 0, buried elements 59 → 0, 240 bearing interfaces in
contact within 0.6 mm, non-base geometry byte-identical to r8
(`a08d84df…cceba`), 288 tests pass. Awaits E3D reload (IR-12a).

`PUMP_MID_LINE.txt` shaft-centreline values (840/640/640 mm for 203-PU-020,
205-PU-018, 205-PU-038) are **reported, not applied**: reaching them needs
248–562 mm of extra pedestal, which would move the casing, shaft and both
nozzles against the standing instruction. `204-PU-028` and `205-PU-056` are
not in the 30-pump scope.

Lessons promoted:

- A support chain verified only inside the base assembly proves nothing;
  anchor every bearing test to the machine being carried.
- Bearing checks must be footprint-aware — drain/flush stubs hang below a
  pump barrel and invent interference that is not there, masking the real
  defect. (This corrected an initial "casing embeds 7–26 mm" reading that
  was an artefact.)
- "Nothing floats" and "everything is connected" are different properties:
  r8 had no floating elements by its own test, yet all 60 of its support
  interfaces were voids.
- After a run of rejected revisions, re-measure the last accepted baseline
  before extending the newest attempt.

### r13 — casing feet + clash-free hold-downs (2026-08-07)

The client loaded r12 and reported two bugs: (1) the bolts collide with the
support legs, and (2) it is not an effective support — the base should match
the pump geometry with a precise interface to the pump body.

Both were reproduced numerically before any change: 1,700 fastener/structure
intersections, and bearing plates meeting the round casing barrel on a tangent
line (the plates sit ≈0.91·R either side of the barrel axis, under its curved
flank, with nothing bringing the casting down to a flat face).

r13 adds 120 cast **casing feet** — a machined sole pad matching the pedestal
plate footprint exactly, plus a rib rising to the computed barrel surface at
its own lateral offset so it merges into the casting — and re-places every
hold-down by searching for a plan position clear of all vertical steel,
falling back from four bolts to two flanking the machine foot on small pads.
Collisions: 1,700 → 0. Pedestals, bearing elevations and SUPPORT_FRAME are
byte-identical to r12; voids remain 0; 288 tests pass.

The client then flagged the bolt **positions**. A positional audit of that
first attempt found 84 bolts hanging off the plate edge, 180 off-centre groups
(worst: four bolts crammed into the top 15 mm of a 160 mm plate) and 3 mixed
patterns — all caused by letting the placement search slide off-centre to dodge
steel while scoring only "widest spread". Patterns are now symmetric about the
plate centre by construction, fully contained, with a ≥1.5·d edge distance.

That alone dropped coverage to 48/120, which exposed the real constraint:
measured across all 30 pumps, the r12 pedestal webs run to within **4 mm of the
bearing-plate ends** and span its full width — there is physically nowhere on
that plate for a 17 mm bolt. The hold-downs were therefore moved to the
pedestal's **bottom flange**, which projects ~8 mm beyond the plate on all four
sides and is clear of the webs, which is what real fabricated pedestals do.
Final: 928 bolts, 234/240 flanges, 0 collisions, 0 off-edge, 0 off-centre.

An intermediate attempt to shorten the webs instead was **reverted** — it
reopened 44 mm voids under the plates.

Lessons promoted:

- **"Clash-free" is not "correct".** A bolt can miss every member and still
  hang off an edge or bunch at one end. Fasteners need positional properties
  of their own (inside the part, symmetric, sane edge distance, uniform
  pattern), and those are now verified rather than assumed.
- **When a placement search keeps needing exceptions, the host geometry is
  wrong, not the search.** Measuring the available space first would have
  pointed at the projecting flange immediately.
- **Do not trade away a property already proved to buy a new one** — the
  web-shortening fix bought bolt room and silently lost the support chain.

- **Sign-check a clearance parameter against a known interference.**
  `overlap > clear` reads naturally and is exactly backwards — it let a 1.9 mm
  interference pass a 2.0 mm clearance check, silently permitting every
  near-miss the test existed to catch. The first "fix" therefore changed
  nothing measurable.
- **A generator and its verifier must import one definition of the property
  they argue about.** Two copies of `is_vertical` (40 mm vs 60 mm) meant the
  generator thought a member harmless while the verifier flagged it.
- **A flat plate under a round barrel is not a support.** Bearing needs a
  matched flat face on both sides; a tangent line satisfies a naive contact
  test but reads as floating in E3D — which is precisely what the client saw.
- **Derive clash obstacles from the geometry actually emitted**, not from a
  parallel recomputation that can drift from it.

### Outstanding

- r13 needs an E3D visual reload (IR-13a): confirm each pump foot has a cast
  foot with a flat pad on its pedestal, and that the hold-downs sit
  symmetrically on the projecting pedestal flange, clear of every web.
- 203-PU-020: 6 pedestal flanges unbolted, blocked by a low casing detail.
- r12 needs an E3D visual reload (IR-12a): confirm each pump foot and motor
  pad now stands on a visible pedestal reaching the frame, nut on the plate
  top. This supersedes the r9–r11 base thread.
- A decision is needed on `PUMP_MID_LINE.txt`: if the pumps are genuinely to
  be raised to those centrelines, nozzle elevations and connected piping
  must move with them.
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
  reload; if another reference base structure was meant by "study this base
  structure and model", supply its path and the rails will be reworked to match.
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

## 2026-08-13 — pumpcad plan rebuild from the JSON top views

### What was delivered

The client supplied `C:\Users\A\Desktop\pumps` (30 JSON exports + the same
`Pump_details.xlsx`, SHA-256 `BE7E38…29C0`) and required the top view to
strictly follow the JSON linework while the table supplies everything else,
with maximum realistic detail.  This supersedes the first pumpcad pass,
which had classified 24 of 30 drawings as elevations.

- `pumpcad/` reconstruction pipeline corrected: `classify_view` now honours
  the JSON's own `reference_top_view` (all 28 geometry-bearing files are
  plans of horizontal pumps); the aspect-ratio "elevation" heuristic is
  gone.
- Out-of-outline linework (suction elbows, drain runs) is excluded from
  component assembly but still measures horizontal nozzle reach.
- Casing identification prefers the wet-end concentric disc stack, then the
  roundest compact wet-end body, with the wet end anchored by the layout
  axis so the driver can never be promoted to casing.
- Enriched plan construction, every size traced to the drawn contour or
  labelled as a bounded Reference Value: motor barrel + end bells +
  360-degree cooling ribs + terminal box + gland + lifting lug + nameplate
  + feet + hold-downs; volute + suction cover cone + shaft boss + split
  flange + flange-face bolt ring + casing ribs + foot; bearing housing +
  pedestal; coupling shaft + hubs + guard end plates.
- 203-PU-020 and 205-PU-004 have no CAD and build a metadata-proportioned
  horizontal body, flagged UNCONFIRMED.

### Client refinement round (same day)

- Hierarchy is one SUBE per major assembly - BASEPLATE / SUPPORT / CASING
  / BEARING / COUPLING / DRIVER / AUXILIARY / SUCTION / DISCHARGE - not one
  SUBE per primitive.
- Nozzle datums: horizontal nozzles at the shaft centreline, top-discharge
  at the casing crown, and the centreline is raised to clear the suction
  flange radius so a DN600 suction can never dip below U 0.  Neck length
  is bridged to the casing surface instead of a canned 120 mm.
- Fasteners are true hex EXTRUSION nuts (verified native form), not
  cylinders; motor cooling ribs are equal-angle axial rods around the full
  stator; a drawn circle becomes a vertical cylinder, a closed polygon
  (octagon/diamond/arc) becomes a vertical EXTRUSION of that polygon, and
  only a drawn rectangle becomes a box or barrel cylinder.

Deliverables under `Projects/JK_Pump_Build/output/pumpcad/`: per-pump
macros and audits, `JK_Pump_Build_All_Pumps.pml` (30 independent EQUI,
60 catalogue-bound NOZZLEs, 342 EXTRUSIONs, 1,640 box/cylinder/cones),
the whole-assembly comparison set, the browser viewer and the batch
report.  27/30 pumps pass every numeric check; 373 tests pass.

### The failure this corrected

The first pumpcad run reasoned "an outline taller than it is wide must be
an elevation" and built 24 North/South pumps as stacked vertical machines
on square baseplates, standing up to 3 m tall.  The JSON itself said
`reference_top_view: "Top View - …"` on every file, and a horizontal
pump whose long axis runs North legitimately has a taller-than-wide plan
outline.  The client restated the requirement explicitly: the plan view
is strict; only other quantities come from the table.

### Verification

Numeric, not textual: baseplate underside-centre vs Excel; plate L/W/T vs
Excel; layout axis vs suction (with the client E-W override for
205-PU-018/038); nearest-catalogue DN for all 60 nozzles; drawn outline vs
contractual plate within 10 mm; model top-view bounds contained in the CAD
extent; each main body's plan silhouette vs its drawn contour within
30 mm; in-outline linework consumption; PML1 validity; ORI-before-POS,
CATR-first nozzle binding and no geometry below U 0 across all 30 files.
85 `pumpcad` tests pass.  **Awaiting a fresh E3D visual reload before this
can be called accepted (IR-11d).**

### Lessons

- **A declared view field outranks any geometric heuristic.**  The
  drawings were self-describing; the classifier ignored the label and
  reasoned from aspect ratio, and got 24 of 28 wrong while every numeric
  check stayed green.  Read the metadata that names the projection before
  inferring it from the linework.
- **The baseplate outline is the assembly boundary.**  Including pipework
  drawn beyond the plate made one "motor" swallow 2 m of suction line;
  excluding it left clean driver/coupling/casing bands on the same
  drawings.
- **Anchoring the wet end by the layout axis removes a chicken-and-egg.**
  With both ends holding large bodies, "largest compact body at an end"
  can crown the motor as the casing; the contractual suction/longitudinal
  direction decides which end is the wet end without needing the casing
  first.
- **Plan fidelity is verifiable per component, not just as a batch
  envelope.**  Mapping each body's drawn contour into the world frame and
  comparing its own footprint catches a wrong-sized casing that a
  whole-model bounds check cannot see.
- **A sliver is not a body.**  The first fallback promoted a 340x16
  feature to "casing"; a compactness ratio (min/max extent) rejects those
  while accepting genuine round cover plates.
- **The primitive must match the drawn silhouette, not merely its bounds.**
  A bounding circle over a drawn rectangle passes an extent check and
  still reads wrong in plan; a vertical cylinder for a circle, a vertical
  EXTRUSION for a polygon and a barrel only for a rectangle is what makes
  the plan "strict" in E3D rather than in the verifier.
- **A nozzle's elevation is part of its datum.**  Everything had passed
  while the suction flange sat at plate-plus-bore height: the flange face
  was at U 240 with the shaft at U 400, which the client read as "the
  nozzles fell on the ground".  Anchor horizontal nozzles to the shaft
  centreline and vertical ones to the casing crown, then size the neck to
  bridge the actual gap.
- **Big bores own the centreline.**  The shaft height must be bounded from
  below by half the suction flange diameter, or a DN600 flange projects
  through the foundation while every other check stays green.
- **Grouping is a downstream contract too.**  One SUBE per primitive makes
  the tree unmaintainable for piping and structural designers; the
  grouping belongs in the renderer, classified from the part label so
  builders never have to thread a group tag through every emitter.
- **Close what the draughtsman closed, and nothing else.**  The octagon
  and arc silhouettes in these exports are mostly open strokes broken at
  dimension ticks; bridging free chain ends within 8 mm recovers real
  closed polygons, and a plausibility guard (aspect ratio, filled area)
  keeps a chance bridge from becoming a nonsense EXTRUSION.  Where the
  drawing stays open, the nearest legitimate primitive (vertical cylinder
  for a circle, barrel for a rectangle) is used and the choice is stated
  rather than fabricating a closed LOOP.
- **A cover cone still obeys the plate.**  The suction cover closes toward
  the wet end, but its reach must be capped at the plate/drawn extent or
  it becomes an out-of-drawing spout that only the plan-containment check
  ever sees.

### Third client round (same day)

- A nozzle is emitted as the catalogue NOZZLE alone; the previously added
  neck/flange primitives were removed - the bound SPCO already draws the
  barrel and face, and duplicating it reads as clutter at the connection.
- Bottom supports are fabricated detail: sole plate on the baseplate top,
  pedestal web, two triangular EXTRUSION gussets in the machine vertical
  plane, and two hold-downs with hex nuts, with the bearing chain plate ->
  sole -> pedestal -> machine body verified by construction.
- The "twisted main body" fault was the casing fallback preferring the
  roundest compact body, which crowned a 334x172 discharge boss as the
  casing while the drawn 652x210 volute band stayed auxiliary.  The
  fallback now takes the largest body inside the outer 30% of the plate,
  which restores the real volute envelope on the eight large
  filtrate/process pumps (203-PU-009, 204-PU-015/016, 205-PU-030/031/
  047/048, 205-PU-027).
- Curved corners are the drawing's own tessellated arcs: E3D's native
  EXTRUSION VERTEX carries no radius attribute, so an arc is expressed as
  the multi-vertex LOOP the drawing supplies - a many-sided approximation
  of the same curve, never a fabricated fillet.

## 2026-08-13 — custom 205-PU-012 scale variant (3504 x 1500 baseplate)

The client supplied `C:\Users\A\Desktop\Custom_pump.txt`, a native E3D data
listing of the accepted 205-PU-012, and asked for a variant with a
3504 x 1500 mm baseplate, the rest of the pump enlarged proportionally, the
construction/shape kept and the nozzle sizes kept.

### What was delivered

- Original archived byte-for-byte at
  `imports/2026-08-13_Custom_pump.txt`
  (SHA-256 `1C7EEC29388F41AA0F096BC5DC2875CA488C5DB8E720CEC24AB28A986A175D9F`).
- `output/205-PU-012_3504x1500.txt` plus a Desktop copy
  `Custom_pump_3504x1500.txt`, and repeatable tools
  `tools/scale_pump_3504x1500.py` / `tools/verify_scale_3504x1500.py`.
- Baseplate exactly 1500 (E) x 3504 (N) x 50, underside centre unchanged.
- Superstructure scaled by one similarity factor `s = 3504/2701`: plan about
  the plate centre, elevations about the plate top U=50.
- Nozzles unchanged in size: CATR/HEIG/ORI/process attributes kept; barrel
  roots scale with the machine and the unchanged HEIG is re-added, so both
  nozzles stay attached.  The discharge boss keeps DIAM 135 / HEIG 28 and
  moves with the scaled casing crown.

### Defects found and fixed in the supplied file

- The file contained the same pump exported twice back to back.  Loading both
  would collide on the duplicate `/205_PU_012` name, so the deliverable keeps
  exactly one EQUI block.
- The native listing omitted `NAPPFLAG` on the nested NCYLINDER.  The
  project-verified form requires `NAPPFLAG 2` for the hole to cut, so it was
  re-added (native-listing omission is NATIVE-OBSERVED, not independently
  re-certified in this exact listing).

### Verification

Numeric, not textual: 471-element inventory identical to the source block;
every attribute independently re-predicted; 244 solid AABBs checked; no solid
below U 0 or outside the new plate envelope; support-chain U spans scale
invariantly about U=50; suction root meets the scaled casing crown and the
discharge root stays inside the boss; NCYL hole keeps a >= 2 mm plate rim.
**Awaits a fresh E3D visual reload before acceptance (IR-11d).**

### Open decision

A single uniform scale cannot satisfy both 3504 and 1500 from 2701 x 1245
(3504 needs s=1.2973, 1500 needs s=1.2048).  The delivered variant is
length-driven (s=1.2973) and treats 1500 as an explicit plate-width override.
If the client prefers the width-driven factor or a non-uniform treatment, the
tool only needs a new factor and a regeneration pass.

## 2026-08-18 — /P1501B -> /P1501C scale variant (1807 x 663 baseplate)

The client supplied `C:\Users\A\Desktop\Reference_pumps.txt`, a native E3D
data listing of `/P1501B` "Reflux Pump - Standby", and asked for a re-sized
variant that keeps the same construction.  This is the second application of
the 2026-08-13 scaling method, on a different and simpler source: a
`TMPLATE /STD/PUMP005`-derived template pump.

### What was delivered

- Original archived byte-for-byte at
  `imports/2026-08-18_Reference_pumps_P1501B.txt`
  (SHA-256 `BA32D303A790A501C36F36E1D2BF408720AB2304CF26EA53CBCC4AEB120A0F67`).
- `output/P1501C_1807x663.txt` plus a Desktop copy
  `Reference_pumps_P1501C_1807x663.txt`, and repeatable tools
  `tools/scale_pump_P1501B.py` / `tools/verify_scale_P1501B.py`.
- One uniform similarity factor `S = 1.30`; baseplate 1390 x 510 -> 1807 x
  663, all 182 elements retained, construction geometrically similar.
- Nozzle sizes unchanged: CATR/HEIG/ORI/process attributes kept.

### How this source differed from the 205-PU-012 job

- **Local, not world, POS.**  Every primitive POS is expressed in its owner's
  frame with the EQUI origin on the *shaft centreline*, not on the plate.
  Plan scaling is therefore a plain multiply with no centre offset removed.
- **No elevation re-datuming at all** (corrected 2026-08-18 after the client's
  E3D reload; see the post-mortem below).  The equipment origin is on the
  shaft centreline, so a local `U` is an offset from that axis, not a height
  above the foundation.
- **Signed axis letters flip.**  Motor ribs written `D 30.39` legitimately
  become `U 9.11` once the machine lifts.  A sign flip is not a defect here;
  the emitter must derive the letter from the scaled sign.
- `RADI`, `XOFF` and `YOFF` are true lengths and must scale.  Freezing the
  PYRAMID offsets would shear every gusset as the pyramid grew.

### The nozzle bore axis must be recovered geometrically

A native export writes `ORI Y is .. and Z is ..` — E3D's dump of the
resulting axis triad, **not** the `ORI P1 IS` command that aimed the nozzle
(IR-2).  The bore direction cannot be read off it.  Each axis was instead
recovered by testing which candidate direction lands the barrel root on the
casing (volute r=170 about the origin, N -60..+60):

| Nozzle | Aim | Root | Evidence |
|--------|-----|------|----------|
| N1 | N | `(0,0,0)` | exactly the impeller eye; an end-suction inlet |
| N2 | U | `(135,0,30)` | radius 138.3 < 170; aiming E gives 239, floating 69 mm clear |
| N3 | E | `(55,-5,0)`  | radius 55, inside the body |

Guessing from the exported ORI would have put two of three nozzles wrong.

### Defects found and fixed

- **`CREF` connections were inherited.**  All three nozzles carried
  `CREF BRANCH /100-B-8/B2` etc.  A CREF is one half of a *reciprocal* pipe
  connection — the branch holds the matching HREF/TREF back to `/P1501B` —
  so copying it makes the new pump claim pipework already terminated on the
  original.  All three are dropped and reported; routing `/P1501C` is a
  piping decision, not something to inherit.
- **Line-ending and BOM dialect.**  The source is UTF-8-with-BOM and pure
  CRLF.  Text-mode reads normalise CRLF to LF silently, so terminator
  detection must be done on the raw bytes, and a `.*` in a date-restamp
  regex will eat the CR and leave a lone LF.  The deliverable now matches the
  source dialect exactly (BOM, 1187 CRLF, 0 bare LF).
- The header date is restamped with a derivation note so the file does not
  claim to be E3D's own listing of a pump that never existed.

### Verification

Numeric, independent of the generator: 182-element inventory identical; 276
length attributes plus 148 POS lines each re-predicted from first
principles; baseplate envelope measured at exactly 1807 x 663; lowest solid
exactly on the foundation datum; transverse overhang count unchanged; all 82
solid U spans scaling by exactly 1.30; every nozzle root re-measured against
the *raised* casing axis; all catalogue bindings intact.

The verifier was mutation-tested: perturbing a DIAM, floating a nozzle,
sinking a solid below the datum, shrinking the baseplate, breaking U-span
invariance, moving the EQUI coordinate and re-adding a CREF are **all**
caught.  459 repo tests pass.
**Awaits a fresh E3D visual reload before acceptance (IR-11d).**

### A verification bug worth remembering

The first verifier run failed N2 with "root radial 225.1 vs casing r 221".
The model was correct; the *check* was wrong.  It measured the radius from
`U = 0`, but the casing axis had itself risen to `U = 102` under the
elevation rule.  Measured from the true axis the root is at radius 179.8,
the same 0.81 proportion as the source.  When a scaled model fails a check,
confirm the check scaled too.

### A latent retrieval bug this entry exposed

Appending this section made `test_knowledge_base_loads_the_skill_corpus`
fail: a spatial-intent query started returning `projects/jk-pump-build`
instead of `knowledge/pml-spatial-lookup`.  The model was fine and so was
the prose — the router was wrong.  `PMLKnowledgeBase.search` scored raw term
frequency over the whole document and then added a flat `+750` to the routed
document.  Term frequency grows without bound as a project log accumulates
entries; the flat bonus does not.  This log had already reached ~1065 on
that query against the spatial map's ~282 and was winning on sheer length,
so the boost was one entry away from being overtaken no matter what the new
text said.

Two fixes were needed, and the second only surfaced when this file grew
again with the 2026-08-18 post-mortem:

1. `route_to()` now lifts a routed document above the current leader rather
   than adding a flat bonus, because routing is an intent decision that must
   not be outvoted by an unrelated document's size.
2. Term frequency is now **normalised by document length** (`sqrt` of the
   ratio to the median document).  Raw counts made relevance a proxy for
   size: this log reached 46 uses of "centre" against iron-rules.md's 18
   purely by being 2.2x longer, and began winning datum queries that the
   Iron Rules must own — a query with no routing rule to save it.

All five canonical retrieval queries now resolve to their intended
documents.  Note the honest limit: normalisation defeats *incidental* length
bias, not deliberate keyword stuffing — 600 synthetic keyword lines still
win an unrouted query.  That is inherent to term-frequency scoring and is
not a realistic failure mode for a hand-written log.

The lesson generalises: when adding to a long knowledge file breaks a
retrieval test, check whether the ranking rule scales with document length
before rewording the entry.  Twice now the text was fine and the ranking
rule was wrong.

### User-corrected 2026-08-18: the motor was 204 mm off the shaft

The client reloaded the first `/P1501C` and the render showed the coupling
parted, with the motor floating above the pump.  Root cause, measured:

The first revision scaled elevations about the baseplate underside
(`U' = -340 + (U + 340) * S`) to stop the plate "sinking" from `U -340` to
`U -442`.  Two errors compounded:

1. **A SUBE `POS` is a relative offset between coordinate frames, not a
   point in space.**  `/Motor` carries `POS U 0`, meaning "the motor frame
   shares the equipment's elevation datum".  Re-datuming that turned the 0
   into +102 and lifted the entire motor subassembly.
2. **Every child of `/Motor` was then re-datumed again in its own right**, so
   the motor was lifted *twice* and ended 204 mm above the casing axis.

The deeper error was the premise.  This equipment's origin sits on the
**shaft centreline** — the casing volute is centred on `U 0` and the motor
frame is offset `U 0` from it — so *every* local `U` is an offset from that
axis, not an elevation above the foundation.  The "sinking plate" was never
real: the EQUI installation `POS U 100645` is the shaft-centreline
elevation, so a larger pump legitimately carries its plate further below a
fixed shaft height.  The correct transform is a **pure uniform scale about
the equipment origin**, with no per-axis re-anchoring anywhere.

The plate underside consequently sits 102 mm lower relative to the shaft than
on `/P1501B`.  That is a real civil/plinth consequence of fitting a larger
pump at the same shaft elevation, and it belongs in a note to the client, not
hidden by distorting the machine.

**Generalised rule.**  A similarity transform must be uniform about a single
origin.  The moment different parts of one assembly are re-datumed about
different planes, the assembly shears — and every part can still individually
satisfy its own rule.  Before choosing a scaling origin, establish what the
model's origin physically *is*; here it was a machine axis, not a floor.

### Why the verifier passed a visibly broken model

Every check compared the output against the transform I had chosen, so a
wrong transform applied consistently passed all of them.  Not one check asked
whether the parts still touch each other.

The verifier now carries relational `[8b]` checks that compare parts to
**other parts** rather than to a formula:

- the motor barrel and casing volute must be **coaxial**, verified in the
  source *and* the output;
- every SUBE frame offset must scale by exactly `S` and never be re-datumed;
- the distance between any two solid centres must scale by exactly `S`, which
  catches any relative displacement whatever its cause.

The last one is the important one: it is an invariant of a similarity
transform, so it holds for any `S` without encoding the transform under test.
Re-injecting the original `/Motor` defect is now caught by four independent
checks.

**Generalised rule.**  A verifier built from the same assumption as the
generator can only confirm that assumption was applied consistently.  At
least one check must be relational — parts against other parts — so that a
wrong premise still fails.

## 2026-08-19 — Five-file rebuild of the 30-pump register

The client replaced the Excel/JSON source chain with five files and asked for
the whole register to be rebuilt: `location_nozzle_reference.txt` (equipment
set, baseplate, nozzle schedule), `engine_shaft_measurements_updated.csv`
(motor/shaft), `casing_reference.txt` (casing), the MC casing-offset file, and
`Reference_pumps.txt` (/P1501B) as a **structure-only** reference.

Delivered: 30 macros plus a combined loader in
`Projects/JK_Pump_Build/output/2026-08-19_pumps/`, with `AUDIT.md`. 0
verification problems, 9/9 verifier mutations caught, 481 repo tests pass.
Awaiting an E3D reload before acceptance (IR-11d).

### An exported `ORI` triad cannot be inverted into a direction

The 2026-08-18 /P1501B entry already warned that a native export writes E3D's
derived axis triad, not the `ORI P1 IS` that aimed the nozzle. This job gave
the clean proof: **all 28 discharge nozzles that carry an `ORI` share the single
triad `Y is N and Z is E`**, across pumps whose machine axes run both N-S and
E-W. One constant cannot encode 28 different physical directions.

So the census itself is the evidence — before theorising about which clause is
the bore, count the distinct values and compare that against the number of
distinct physical situations. If the source has fewer values than the world has
cases, the field is not what you think it is, and no amount of decoding will
recover the information.

Directions were instead recovered geometrically: a suction points outward past
the plate edge along the machine axis; a discharge standing well above the plate
is a crown discharge. That yielded 30 top discharges — but two of them were
wrong, and the *shared elevation* caught it: on 205-PU-018 and 205-PU-038 the
suction and discharge sit at the same U, which is a horizontal pair, not a
crown. DO.txt had already recorded the client's confirmation of exactly that
layout. **A "top discharge" that shares its suction's elevation is not a top
discharge**, and the elevation comparison is a cheaper test than any plan
heuristic.

### Where a geometric heuristic ties, a recorded client confirmation wins

205-PU-018's suction sits beyond the plate on *both* plan axes (-1.09 of the E
half, -1.06 of the N half). The outward-fraction test is a near-tie there and
picked E-W; DO.txt records the client confirming suction South. The override is
kept as a small data table (`CLIENT_CONFIRMED_SUCTION`), not buried in a branch,
so it stays visible and revisable. A heuristic that is within 3% of a tie is not
evidence.

### Two sources can each be right and still be jointly impossible

For 23 of 30 pumps the casing diameter (`casing_reference.txt`) or the motor
end-bell diameter (engine CSV) is larger than twice the suction nozzle
elevation. A machine centred on the suction axis would pass through the
baseplate and below the foundation.

Neither file is wrong on its own; they were measured independently. The
resolution is physical rather than arithmetic — the machine is a solid that must
rest on its plate — so the shaft was raised to the minimum seating height
(median 45 mm, max 174 mm), nozzle plan positions and directions untouched, and
every raise recorded per pump in the audit. The general rule: when two sources
conflict, look for the physical constraint that outranks both, and report the
adjustment rather than silently splitting the difference.

Handling the casing and the end bell in one place mattered: fixing only the
casing left 205-PU-046 failing on its motor, and the temptation is a per-pump
patch. One `max(casing, end_bell)` in the shared path fixed the class.

### IR-3a is a principle about local frames, not a literal axis pattern

The repo validator requires `ORI Z IS U AND X IS <bearing>` for a rotated BOX.
That form is correct for IR-3a's worked example — a plate on a **vertical**
vessel, where every radial direction lies in the horizontal plane. A motor is a
**horizontal** cylinder, so its cooling ribs sweep a *vertical* plane; `Z IS U`
would hold all 36 ribs upright and only the two at top and bottom dead centre
would lie flat on the barrel.

What carries over is the principle (local X radial, local Y along the body,
local Z tangential), not the axis letters. The ribs are emitted as
`ORI Y IS <axis> AND X IS <transverse> <bearing> U`, and the validator still
flags them — a scope limitation of a rule written for vertical vessels, not a
defect.

Because "the validator is wrong here" is exactly the reasoning that hides real
bugs, the claim is not left as prose: `tools/check_rib_orientation.py` resolves
every emitted `ORI` into an actual axis triad and asserts that local X points at
the machine axis, local Y is the machine axis, and the triad is orthonormal.
972 ribs, 0 wrong. **When you decide a checker does not apply, replace it with a
stricter check rather than an explanation.**

### A verifier earns trust by failing

The verifier's first run reported the casing sinking below the foundation and
the bearing housing "floating" — one real defect and one false positive. The
float check only looked *downward*, so it condemned parts that are legitimately
cantilevered off the machine (bearing housing, terminal box). Replacing it with
**connectivity to the baseplate through any chain of touching parts** kept the
real defects and dropped the false alarms.

It also found a genuine one that way: on the close-coupled MC pumps the bearing
housing was sized by proportion and left an 800 mm gap to the motor, so the
drive train was parted — the exact defect the client rejected in r11. On a
close-coupled machine the lantern housing must *span* casing to motor, so it is
now sized from that gap rather than from a ratio.

All nine injected defects (moved plan position, unbound nozzle, broken
coaxiality, buried discharge, 42 m nozzle, detached part, sunk casing, resized
plate, shrunk casing) are caught.

### User-corrected 2026-08-19: the support was not derived from the reference

The client's E3D reload showed the failure plainly: plain rectangular blocks
under the casing and motor. The first pass had read `Reference_pumps.txt` for
the *machine* (casing, shaft, motor, ribs) and then invented the support from
scratch as one box per foot — discarding the richest part of the reference.

`/P1501B`'s `Baseplate_and_support` holds 43 elements in five systems, and a
composition count would have exposed the gap immediately:

| System | Reference | First pass |
|--------|-----------|------------|
| skid frame (I-section side rails) | 5 BOX | — |
| sole plates | 4 BOX | — |
| tapered gussets | 12 PYRAMID | — |
| anchor bolts | 10 CYLI | — |
| hex washers | 10 EXTRUSION | — |
| plain foot blocks | — | 3 BOX |

**The lesson: when a reference is supplied for structure, diff the composition
per assembly, not just the overall element count.** The first pass produced 53
elements against the reference's 99 and still looked plausible in aggregate; it
was the per-SUBE breakdown — 0 PYRAMID, 0 EXTRUSION against 12 and 10 — that
named exactly what was missing. A count of primitive *kinds* per assembly is a
cheap structural check and catches "adapted" work that quietly dropped a whole
system.

The rebuilt chain is baseplate -> rail -> sole plate -> gusseted pedestal ->
machine, with anchors through the sole plate and a true six-vertex hex washer
seated on top. Support elements went from 3 to ~30 per pump.

### The verifier was blind to the parts that were just added

`bounds()` handled BOX, CYLI and DISH only, so every new PYRAMID gusset and
EXTRUSION washer was silently skipped — 12 unchecked parts per pump, and the
suite still reported "0 problems". This is IR-11f in its purest form: the
silence meant the verifier had not looked, not that the geometry was sound.

Adding PYRAMID (base-centre datum, tapering up) and EXTRUSION (profile
end-plane datum, IR-1) to `bounds()`, then adding three support-specific
mutations — floating washer, displaced gusset, sunk rail — restored real
coverage. All twelve mutations are now caught.

**Whenever a new primitive KIND enters the model, check the verifier's type
list before trusting its next clean run.** A verifier silently narrower than
the model is worse than no verifier, because it reports success.

### User-corrected 2026-08-19 (second): the support had no room to exist

The client's next reload was worse than the one before it — flat strips on the
plate with the machine floating clear above. Two errors compounded, and both
were mine:

1. **A support height taken from a ratio instead of a measurement.**
   `_build_machine_support` used `shaft_u - casing_dia * 0.30` as the height to
   reach. That expression has no physical meaning: for 203-PU-008 the casing
   underside is at U 53.4 while the pedestal was told to stop at U 195.8, i.e.
   *inside* the volute.

2. **A seating rule that left zero clearance.** The earlier "raise the shaft to
   seat the casing" fix used `plate_top + radius`, which puts the machine
   *resting on* the baseplate. On most pumps that left 0.0 mm underneath — so
   the frame, sole plate, gussets and anchors were all squeezed into nothing.

The fix for (1) is `_lowest_of()`, which reads the assembly's real underside
back off the emitted geometry. The fix for (2) came from the reference itself:
/P1501B holds its volute **110 mm clear of the plate top on a 170 mm casing
radius** — 0.647 of the radius — which is precisely the room its 43-element
support occupies. That ratio is now `REF["support_clearance"]`.

**The general lesson: a support's dimensions are a consequence of the gap it
spans, so measure the gap.** Every ratio-derived height in this job has been
wrong at least once, because a ratio encodes an assumption about proportions
that the project data is free to violate. Where one part must reach another,
read the other part's position.

And the second-order lesson: **when a fix makes the render worse, suspect the
fix before the renderer.** The "seat the casing on the plate" rule was itself a
correction, applied to resolve a genuine data conflict. It resolved that
conflict by creating a new one, and nothing in the checks noticed because the
result was still self-consistent.

### Why the verifier passed a support that had been crushed to nothing

Both existing structural checks are blind to this failure by construction:

* **connectivity** — the parts *do* all touch; they are simply 8 mm tall;
* **foundation** — nothing sinks below U 0; everything is squeezed above it.

A model can satisfy every relational check and still be physically absurd if no
check asserts that a member has **depth**. Two were added: a support pedestal
must exceed 25 mm, and the machine underside must clear the plate by 40 mm.

`mutate_seat_machine_on_plate` now reproduces the exact shipped regression —
machine dropped onto the plate, pedestal crushed to 10 mm — and is caught. That
mutation is worth more than the two checks it exercises, because it encodes a
failure that actually reached the client.

One further gap surfaced while testing it: floating a hex washer 700 mm upward
*stopped* being caught once the machine sat higher, because the washer then
landed inside the raised machine and still touched something. Generic
connectivity is too weak for hardware, so a washer is now checked against **its
own sole plate**. When a mutation stops failing after an unrelated change, the
check was relying on a coincidence.

### User-corrected 2026-08-19 (third): use the reference's support, don't invent one

The client asked it plainly — *"why don't you use my reference pump's support
structure"* — and the answer is that I had not. Twice I invented a support
(I-section rails, sole plate, solid pedestal block) and labelled it
"proportioned from /P1501B" because I had measured a couple of ratios off the
reference. Measuring ratios from a reference is not using its structure.

What /P1501B actually builds, decoded in its own frame:

| Member | Reference | What I had built |
|--------|-----------|------------------|
| rails | 4 flat bars 105x1390x20 lying ON the plate | tall I-sections standing proud of it |
| sole plates | 125x300x25 on the plate top | one plate, then a block |
| gussets | 12 PYRAMID **plates**, XBOT == XTOP == 20 | solid tapered wedges |
| mounting pad | pad top only 80-107 mm above the plate | a 130-250 mm solid pedestal |
| anchors | 10 bolts + 10 hex washers | 8 + 8 |

The two structural misreadings that mattered:

1. **A PYRAMID with `XBOT == XTOP` is a plate, not a wedge.** The reference's
   gussets are 20 mm thick top and bottom and narrow only in *length*. Reading
   them as solid tapered blocks turned twelve thin webs into a couple of chunky
   masses.
2. **The machine sits LOW.** The reference pad top is 80-107 mm above the plate
   top, with the machine braced by webs rather than lifted on a pedestal. I had
   been raising the machine and filling the space with a solid block, which is
   why each attempt looked heavier and less like the reference.

Every reference ratio is against the plate **width** (510), not its length. An
earlier revision scaled rail thickness from plate length and produced 8 mm
strips under a 360 mm gap.

**The generalised lesson, and it is the third time this project has paid for
it: when a reference is supplied for structure, reproduce its element list.**
Not its silhouette, not a few ratios sampled from it. The check that would have
caught all three attempts in seconds is a composition diff per assembly:

```
kind        /P1501B   mine
BOX              11      9
CYLINDER         10      8
EXTRUSION        10      8
PYRAMID          12      8
```

The first attempt scored 3/43 on that table with zero PYRAMID and zero
EXTRUSION, while every geometric check passed. A model can satisfy every
positional check ever written and still not be the thing that was asked for,
because "is this the same structure?" is a question about the *inventory*, and
no amount of checking positions asks it.

### User-corrected 2026-08-19 (fourth): reproduce the reference, don't re-derive it

The client supplied `Base_reference.txt` — /P1501B-BASE isolated, 43 elements —
and asked for it to be reproduced strictly for every pump. Three previous
attempts had *redesigned* the support from ratios sampled off the reference.
The fix was to stop designing: `tools/base_reference.py` parses the reference's
own elements and maps each through an affine transform. Nothing is invented,
so the composition matches by construction rather than by intention.

**The measurement that unlocked it.** The reference's base is 510 wide overall
while its plate member is only 300 — its brackets deliberately reach beyond the
plate. Scaling transversely on the plate width threw every bracket off the
target. The envelope and the plate member are different things, and a support
is proportioned on the envelope.

**Vertical scale must be per-station.** The reference carries its pump end
170 mm above the plate top and its motor end 155 mm; a target's casing and
motor rarely share an underside either. One global factor left whichever
machine sat higher floating clear of its mounting. Two factors, interpolated
between the stations, seat both.

**Anchor at the plate underside, and clamp per element datum.** The reference
keeps nothing below its own underside. Clamping the POS was not enough: a BOX's
POS is its centre (IR-1), so a member whose centre clears the underside can
still dip below by half its thickness.

### A faithful copy failed the contact check, and the check was wrong

The reference base is a **bolted assembly, not a fused solid**. Its sole plates
stop at U -255 while the gussets above start at -236; its pump-end pad tops out
at -200 with the side brackets starting at -170. Those 19–30 mm joints are how
the real thing is built.

So a faithful reproduction failed a strict contact test — and the tolerance has
to *scale*, because a base adapted to a 2701 mm plate is 2.4x the reference and
its 30 mm joint opens to ~72 mm. A fixed millimetre tolerance passes the small
pumps and fails the large ones for being equally faithful. The tolerance is now
a fraction of plate length.

The trap to avoid here: I twice widened the tolerance to make failures go away
and let two mutations escape doing it. **Loosening a check to accommodate your
own transform is how a verifier stops working.** The right move was to measure
the reference's real joint gaps first, and only then set a tolerance that
admits them — and to re-run the mutations afterward to prove nothing was lost.

### The composition check, at last

The verifier now asserts the base's element census per pump: 11 BOX, 12
PYRAMID, 10 EXTRUSION, 10 CYLINDER. Three rejected redesigns would each have
failed it in seconds, while all three passed every positional check that
existed at the time.

**When a client supplies a reference for structure, the inventory is the
specification.** Positions can be adapted; the parts list cannot.

### E3D load failure 2026-08-19: the checking layer never read the macro

The client's load failed on the first base element:

```
(47,15)   CP: Syntax error
^^Y is N and Z is D
```

The ORI keyword was missing. `base_reference.py` stores an orientation as the
*clause* (`line[3:]`, stripping "ORI") because that is how it reads the
reference listing back, while every machine builder stores the full
`"ORI Z is ..."`. The emitter wrote `self.ori` verbatim, so base elements
shipped without the keyword. Fixed by normalising in `Primitive.ori_line()`,
at the single point that does the writing.

**The real failure is that nothing could have caught it.** Every check in this
project inspected `Primitive` objects — geometry, datums, connectivity,
composition, 14 mutations — and that entire layer is blind to *how* an object
becomes text. The repo's `validate_pml` missed it too: a bare clause is
indistinguishable from an unrecognised attribute, so it produced no finding.

30 pumps passed every check and the macro would not load.

**Generalised rule: a generator needs one check that reads its own output as
text.** Object-level verification proves the model is right; it says nothing
about the serialisation. Any place where two code paths store the same field in
different shapes — here, with and without a keyword prefix — is invisible to
every check that reads the field rather than the file.

`tools/check_macro_text.py` now parses the finished `.pml` and asserts what only
the text can show: bare orientation clauses, unrecognised commands, PML2 and
prologue tokens, unbalanced blocks, and the IR-2/IR-9a ordering rules surviving
the trip from object to file. It is mutation-tested against the shipped defect
and four others.

One detail worth keeping: the first version of that checker reported "258
element blocks left unclosed", because it counted `EQUIPMENT` and
`SUBEQUIPMENT` as openable. They are grouping elements closed implicitly by the
next one (IR-5), never by an `END`. A text checker has to model the language's
block rules, not just its line syntax.

### User-corrected 2026-08-19 (fifth): a transform reproduces a point cloud, not an assembly

The client rejected the transformed base as "a collection of basic primitives
stacked together without proper structural organization or relationships",
with machines still separated from their mounting surfaces.

The previous revision had parsed `Base_reference.txt` and mapped its 43 element
**positions** through an affine transform. Every element was present, the
composition check passed, and the result was mechanically meaningless: a
member's job is to bear on the member below it, and a coordinate map does not
preserve that. Scale the frame and each part lands where its *number* says, not
where its *neighbour* is.

**The fix was to read the reference as roles and rebuild the load path:**

```
plate -> sole plates -> gussets -> foot pad -> machine
outrigger rails along both plate edges carry the hold-down anchors
```

`base_assembly.py` positions every member **relative to the member it bears
on**. The foot pad's top is set to the machine's measured underside first, and
the gusset height is then whatever remains between the sole-plate top and the
pad bottom. Contact becomes a property of the construction rather than
something to verify afterwards — measured seat gap is 0.00 mm on all 30 pumps.

**Generalised rule: when copying a structure, copy its dependency graph, not
its coordinates.** A transform is correct only for a rigid body. An assembly is
not rigid — it is a set of contact constraints, and those are what must be
reproduced.

### Two modelling facts the render exposed

**A motor stands on two feet, not one pad.** A single central pad covered ~33%
of the stator length and the motor visibly overhung it at both ends. Two feet
straddling the stator at 0.62 of its length fixed it.

**Seat the feet on the stator barrel, not the assembly's lowest point.**
`_lowest_of("DRIVER")` returns the end bells — they are the larger diameter and
hang lower — leaving the feet 36 mm short of the barrel they carry. On a real
motor the end bells overhang the feet; that is not a gap to close. When a part
mounts to an assembly, the mounting face is a *specific member's* surface, and
asking for the assembly's extreme picks the wrong one.

### A verifier check that was right, then wrong

The element-census check (11 BOX / 12 PYRAMID / 10 EXTRUSION / 10 CYLINDER)
caught three rejected redesigns and was the right check while the base was a
literal transformed copy. The moment the client asked for a coherent assembly
*adapted per pump*, it became wrong: station count varies legitimately, so a
fixed inventory is no longer the specification.

It is replaced by role checks — every station needs sole plates, gussets, a
foot pad, anchors and washers — plus a seating check that each pad actually
carries its machine in plan and elevation. **A check encodes an assumption
about the deliverable; when the deliverable's definition changes, re-derive the
check rather than relaxing it.**

### User-corrected 2026-08-19 (sixth): thickness does not scale with width

The client rejected the render as bad work. Measuring it rather than looking at
it found one arithmetic error behind every visible defect:

**Member thicknesses were scaled off the plate WIDTH.** The project fixes every
baseplate at 50 mm while plate widths run 631–2013 mm, so on a wide pump each
member came out up to 3.5x too fat: 72 mm sole plates and a 130 mm foot pad on
a 50 mm plate. That is what "primitives stacked together" looks like from the
outside — it was never a layout problem, it was a units problem.

The rule now separates the two datums explicitly:

* **plan sizes** (rail width, sole width, pad footprint) scale with plate width;
* **thicknesses** (rail, sole, gusset, pad, anchor, washer) scale with plate
  *thickness*.

Every base BOX is now 14.6–37.5 mm against the 50 mm plate.

Two other defects fell out of the same measurement, both of them places where I
had emitted a member *near* the reference's position instead of *at* it:

* the upper rail stood 58 mm proud of the plate, so the sole plates landed on
  top of it and produced the stepped clutter. The reference's rail sits flush
  **in** the plate's top band (U -300..-280 against a plate top of -280);
* the anchor bolt ran the full height from the plate underside to the washer,
  protruding below the foundation and standing 130 mm above the sole. The
  reference's bolt is *buried* in the plate (U -325..-235 against a plate of
  -340..-280).

### The check that was missing for six revisions

Every geometric check I had asked *where* a part is. None asked *what shape it
is*. A 130 mm-thick foot pad satisfies seating, connectivity, foundation and
composition checks perfectly — it is in exactly the right place and carries its
machine — and it is still obviously wrong to anyone looking at it.

The new check is dimensional plausibility: a fabricated plate's thickness must
not exceed ~1.6x the baseplate it belongs to, nor 0.8 of its own span. It is
the cheap bounds check of IR-11a applied to *proportion* rather than position,
and it would have caught this revision, and probably two earlier ones, in
seconds.

**Generalised rule: verify proportion as well as position.** "Is it in the
right place?" and "does it look like the thing it is?" are independent
questions, and a model can pass every instance of the first while failing the
second on every member.
