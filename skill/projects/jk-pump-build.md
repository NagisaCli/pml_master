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

> **User-corrected 2026-08-23 / 2026-08-24 (JK_Pump_Build).**

- High-fidelity MC pump template from `205-PU-054` (9 subequipments, 4 nozzles, 274 primitives) replaces `205-PU-038`, `205-PU-018`, `203-PU-020` (rotated 90° CCW, main shaft West) and new pump `204-PU-028` is added at `(22370, 6986, 0)` mm (rotated 90° CW, nozzle East).
- All 26 non-MC pumps and the native Zone structure are preserved 100% untouched.

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

## Revision history

Every revision round — r1 through r13, the pumpcad plan rebuild, the two scale
variants, the five-file register rebuild and the rounds that followed — is
recorded verbatim in
[jk-pump-build-history.md](jk-pump-build-history.md), newest section last.

Read it when you need the reasoning behind a decision or the post-mortem of a
failure. Do not read it to learn the project's current state: that is this file,
and this file is kept short so it can be read in full.
