# JK_Pump_Build Pump Model Refinement Report (2026-08-05)

## Task and constraints

Based on the native export `C:\Users\A\Desktop\JK_PU.txt` (accepted baseline,
SHA-256
`D59B89BB2E07CF25EF28A671F969ED1B38C62D6F556A0F040742CEC103AAB43F`), using
the newly verified syntax (EXTRUSION solids, hex nuts, end-plane POS
semantics), refine the 30 pump models in detail:

- do not change baseplate sizes or coordinates;
- do not change nozzle positions, orientations or sizes;
- optimise model detail only; convert the motor and pump supports to
  bridge-type standard brackets;
- fix unreasonable structure and interpenetration conflicts.

## Deliverables

- Refined combined macros:
  - r1: `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805.pml`
    (55,843 lines)
  - **r2 (current)**: `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r2.pml`
    (55,061 lines)
  - **r3 (current, NCYLI fix)**:
    `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r3.pml`
    (55,086 lines)
  - **r4 (current, NCYLI local-coordinate)**:
    `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r4.pml`
    (55,086 lines)
  - **r5 (current, hole-boundary adaptation + C-channel base)**:
    `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r5.pml`
    (56,766 lines)
  - **r6 (current, reference-base structure correction)**:
    `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r6.pml`
    (62,630 lines)
  - **r7 (current, wholesale base rebuild)**:
    `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r7.pml`
    (64,306 lines)
  - **r8 (current, direct reference-base copy)**:
    `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r8.pml`
    (57,406 lines)
  - **r9 (current, PUMP006/DBOutput base rebuild)**:
    `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r9.pml`
    (53,784 lines)
  - **r10 (current, physical-support logic correction)**:
    `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r10.pml`
    (69,044 lines)
  - **r11 (current, bridge-bracket version)**:
    `Projects/JK_Pump_Build/output/JK_Pump_Build_refined_20260805_r11.pml`
    (64,420 lines)
- Base reference archive:
  `Projects/E3D_Syntax_Lab/imports/2026-08-05_base_structure_reference.txt`
  (P1501A-BASE, SHA-256
  `0347E0072EB044608B867A866BD03629FFE996BE5A25EED49F621893197DAC7F`)
- **PUMP006 base reference archive (r9)**:
  `Projects/JK_Pump_Build/imports/2026-08-06_P1502B_PUMP006_DBOutput.txt`
  (P1502B-BASE, SHA-256
  `E6EF37E6A5FFCDC497821C42B998EB6306D63EFBDA55CB6C1CE71030A057A221`)
- Native import archive:
  `Projects/JK_Pump_Build/imports/2026-08-05_JK_PU_native.txt`
- Error archive:
  `Projects/JK_Pump_Build/imports/2026-08-05_SIR_Cannot_create_EQUI.txt`
- Conversion script: `Projects/JK_Pump_Build/tools/refine_bridge_brackets.py`
- Numerical verification script: `Projects/JK_Pump_Build/tools/verify_refined.py`

## r2 additional changes (second instruction on 2026-08-05)

Two items added per the user's latest instruction on top of r1:

### D. Temporarily remove the MC_AUXILIARY subequipment (5 pumps)

The `MC_AUXILIARY` subequipment of `203_PU_020`, `205_PU_004`, `205_PU_018`,
`205_PU_038` and `205_PU_054` was removed wholesale (geometry and hierarchy
headers fully deleted), to be re-added later. Numerical verification after
removal: 0 `MC_AUXILIARY` residue in the whole file; the other subequipment
(baseplate, pump frame, casing, bearing frame, coupling, motor, etc.) is
unaffected.

### E. Negative-primitive hole cutting (NCYLINDER, learning application)

Per the user's suggestion, use a negative cylinder instead of the old
"top connecting plate + cylinder passing through it" expression:

- each pump's `DRIVER` BOX21 (terminal-box mounting plate) embeds a
  `NEW NCYLINDER` child carrying the original CYLI's POS / ORI / DIAM / HEIG;
- the original through-plate cylinders (CYLI25–36, depending on the pump)
  were deleted;
- 30 NCYLI holes in total (1 per pump), all intersecting their BOX21 (30/30
  pass); no residual cylinder remains at the BOX21 centre (0 residue).

Syntax basis:

- the user's own native E3D listing
  (`JK-Tank_Build/imports/2026-08-04_WSB_TA.txt`) contains `NEW NCYLINDER`
  nested inside positive `CYLINDER`;
- AVEVA's official PMLLIB (`mmmcounterweight.pmlobj`,
  `mmmconveyortakeup.pmlobj`) creates NBOX / NCYLINDER with their own
  POS/ORI inside positive primitive blocks.

**Status: EXPERIMENTAL.** The form has been registered in the knowledge base
(negative primitives were previously verified unavailable only in `$M` macro
mode; this is the native INPUT data-listing path). Please load r2 and confirm
the holes display correctly; once confirmed, promote to VERIFIED and
generalise to other hole-cutting scenarios.

## r2 load error and fix (same evening)

The user's load of r2 reported a rare error (SIR file archived):

```
(41,8)  Cannot create a EQUI at this level.
In line 7121 of Macro ...JK_Pump_Build_refined_20260805_r2.pml
Command: NEW EQUIPMENT /203_PU_026
```

### Root cause

In a native INPUT data listing, every `SUBEQUIPMENT` and `EQUIPMENT` block has
its own closing `END` line (unlike generated macros where the next NEW
implicitly closes the block). When r2 deleted the `MC_AUXILIARY` of the 5
pumps, it removed the subequipment headers and primitive blocks but left each
subequipment's own closing `END` behind. The extra `END`s closed the
EQUIPMENT and then the ZONE, so pump 5 (203_PU_026) `NEW EQUIPMENT` ran
outside the ZONE and failed — the first 4 pumps loaded, everything after was
missing.

### Fix

- The deletion range was extended to "subequipment header through the SUBE
  END that immediately follows the last primitive's END";
- the verification script gained an **INPUT block-stack replay check**: EQUI
  only inside ZONE, SUBE only inside EQUI, primitives only inside
  SUBE/parent primitive, END never out of bounds, no residual stack at EOF —
  this catches such hierarchy errors before delivery;
- r2 regenerated (55,056 lines): EQUI 30/30 created at the correct hierarchy
  level, 360 SUBEs (source 365 − 5), 5,233 primitives, no out-of-bounds END,
  no residual stack.

Registered as F-18 in the skill process (diagnostics manual), and "data
listings use explicit SUBE/EQUI END; deleting a SUBE must delete its END too"
was written into the pml1-reference structure entries.

## r3 — NCYLI no-hole fix (NAPPFLAG 2)

The user confirmed r2 loaded but none of the 30 NCYLI cut holes, and
self-tested that "positive primitive + negative primitive" does cut
(excluding system settings). Findings:

**Root cause: the negative primitive lacked the negative-application flag.**
AVEVA's official hole code (`hmcontrol.pmlobj`
`createHoleNegativeExtrusion`) sets `!!ce.nappflag = 2` immediately after
creating the negative extrusion; `strSctnGensec.pmlobj` also corrects
`NAPPFLAG -1` to 2. A negative primitive only participates in Boolean
subtraction when this flag is 2 — r2's NCYLINDER did not have the attribute,
so it loaded but had no effect.

**Fix:** add `NAPPFLAG 2` to every `NCYLINDER` block (r3, 30/30 verified).

**Still under verification:** the POS/ORI semantics of negative children
(world coordinates vs inherited owner pose vs relative offset, and whether
standalone negatives at SUBE level work). A minimal comparison experiment
macro `PML-STUDY-NCYL-001` was generated (desktop copy
`C:\Users\A\Desktop\NCYLI_test.pml`, 4 candidates C1–C4); after loading,
report which candidate cuts holes and the hole position/direction per the
experiment notes, and the form can be locked and NCYLI promoted to VERIFIED.

## r4 — negative-child local-coordinate semantics fix (user experiment confirmed)

After the user loaded the comparison experiment `PML-STUDY-NCYL-001` (desktop
`NCYLI_test.pml`), conclusions:

- C2 (child, no POS/ORI, inherits owner) and C3 (child, POS zero offset +
  horizontal ORI) both cut correctly;
- C1 (child, world-coordinate POS) loaded but had no modelling effect — a
  child's POS is **local to its owner**; the world coordinates were treated
  as a local offset and the hole fell outside the plate;
- C4 (standalone NCYLINDER at SUBE level) reported
  `(41,8) Cannot create a NCYL at this level.` — negative primitives can only
  be children of positive primitives, never standalone.

**r4 fix:** each `NCYLINDER`'s POS changed from the original CYLI world
coordinate to an offset relative to the BOX21 centre (e.g. 203-PU-008:
`POS E 0mm N 0mm U 16.3mm`); ORI / DIAM / HEIG unchanged; NAPPFLAG 2 kept.
Verification: 30/30 "owner centre + local offset" equal the original CYLI
world position (local-pos mismatch 0); all holes intersect BOX21;
baseplate/nozzle/CATR and all other checks pass.

**NCYLI syntax promoted to VERIFIED per the experiment conclusions**
(pml1-reference: a negative primitive must be a child of a positive
primitive, POS is local to the owner, ORI is honoured, NAPPFLAG 2 required).

## r5 — per-pump hole-boundary adaptation + base profile optimisation (2026-08-06)

### A. Open-hole fix (per-pump adaptation)

The user confirmed hole cutting works but noted that some holes were not
adapted per pump's plate and cut through the plate edge, forming "open
holes". Per-pump checks confirmed 10 pumps whose hole circle exceeded the
BOX21 boundary in U (203-PU-011/020/031, 204-PU-017/023,
205-PU-012/018/032/038/054; overshoot 0.10–2.15mm).

Fix rule: clamp each NCYLI's U local offset per the pump's plate thickness
and hole diameter so `|dz| + DIAM/2 ≤ ZLEN/2 − 2mm`, i.e. the hole circle
sits fully inside the plate with a 2mm rim; the hole axis direction,
diameter and through-length are unchanged. Pumps whose holes almost touched
the top (e.g. 008) were also clamped to the safe rim (e.g. 203-PU-008: U
offset 16.3 → 14.9mm, visually imperceptible). Verification: 30/30 hole
circles fully contained in their plates (open/out-of-plate = 0).

### B. Base model optimisation (sizes/coordinates unchanged)

Constrained by each pump's own attributes (baseplate size/coordinates, pump
axis direction, support spacing all unchanged), upgrade the two solid
rectangular skid rails of `SUPPORT_FRAME` to standard **C-channel
EXTRUSIONs**:

- outer envelope, centre position, length, top/bottom elevations identical
  to the original rails (e.g. 203-PU-008: 68.2×63.9×1751.5; the top face
  remains the motor/bridge bearing surface);
- web 8mm, flange 10mm (Reference Value);
- the two rails' openings face each other, toward the pump centre (standard
  C-channel base layout);
- cross beams, bridge brackets (sole plate + trapezoid gussets), hex nuts,
  baseplate and anchors retained.

Verification: 60 C-channel EXTRUSIONs (8-vertex LOOP) structurally valid;
position/envelope identical to the source rails; no new clashes; lowest point
U=0; baseplates/nozzles/CATR unchanged.

## r6 — correction to the reference base structure (reference file provided by user on 2026-08-06)

After the user provided the standard base reference
(P1501A-BASE), it was confirmed that r5's C-channel rails
were not as expected; the base should follow the reference structure.
Reference base elements: rectangular flat-bar rails + equipment sole plates +
trapezoid gussets + **hex washers** + anchor bolts (hexagonal EXTRUSION
washers paired with bolts).

r6 corrections:

1. **Rails back to rectangular**: remove r5's C-channel section; rails revert
   to rectangular BOXes (envelope, position, length, top/bottom elevations
   consistent with each pump's attributes — the rail height is locked by the
   pump's bearing-height chain and cannot be changed to the reference's 20mm
   flat-bar height);
2. **Anchor washers hexagonised**: all circular washers in
   `BASE_FASTENERS` / `DRIVER_FASTENERS` upgraded to hex EXTRUSION washers
   (across-flats = original washer diameter, same thickness, end-plane
   seating, matching the reference base's hex washers); 328 total;
3. pump-foot/motor bridge brackets (sole plate + trapezoid gussets), hex
   nuts, cross beams, baseplate and holes retained.

Verification: 1136 EXTRUSIONs (480 gussets + 328 hex washers + 328 hex nuts)
structurally valid; 328 nuts all seated (washer top or shank top); 30 holes
closed; baseplates/nozzles/CATR unchanged; no new clashes; lowest point U=0.

## r7 — wholesale base rebuild (per reference P1501A-BASE)

Per the user's instruction "rebuild the base wholesale; just adapt the size
and position", rebuild each pump's `SUPPORT_FRAME` wholesale using the
reference base (P1501A-BASE: built-up I-section + sole plates/gussets + thick
hex washers + through anchors) as the blueprint:

1. **Rails → built-up I-sections**: each solid rectangular rail rebuilt as
   three pieces (lower flange 20 + web 8 + upper flange 20, Reference Value);
   outer profile, centre position, length, top/bottom elevations identical to
   the original rail — from the side it reads as a standard I-beam, visually
   distinct from the original solid rectangle;
2. **Anchors → reference-style thick hex washers + extended shanks**:
   - `BASE_FASTENERS`: hex washer thickness 3.7→12mm, still seated on the
     baseplate top; shank extended to the nut top (e.g. 203-PU-008: HEIG
     23→31.4mm); hex nut raised onto the washer top;
   - `DRIVER_FASTENERS`: hex washer 3.9→12mm (seated on the motor pad top);
     nut still seated on the shank top;
3. pump-foot/motor bridge brackets (sole plate + trapezoid gussets), cross
   beams, baseplate, holes and nozzles unchanged.

Verification: each pump's 2 I-beam rails (6 BOXes) match the original outer
profile/bearing height; 328 hex washers all seated on end planes, 328 nuts
all seated; 30 holes closed; baseplates/nozzles/CATR unchanged; no new
clashes; lowest point U=0.

## r8 — direct copy of the reference base (2026-08-06, user confirmed the reference)

The user confirmed `C:\Users\A\Desktop\E3D_model_TRAIN\euip\pump.txt` is the
reference (identical to the earlier base-structure reference except the
export timestamp) and
required a direct copy of the P1501A-BASE structure, with sizes/positions
adapted per pump. r8 rebuilds the base exactly per the reference:

1. **flat-bar flange rails** (adapted from the reference's 105×20 flat bar):
   each original rail becomes a 20mm-thick flat bar seated on the baseplate
   top; position/length/width follow the original rail;
2. **PYRAMID solid trapezoid gussets** (reference's own syntax, copied): 2
   PYRAMID gussets per pump-foot/motor-foot location, bottom on the
   flange-bar top, top face shortened (YBOT×0.7), carrying the sole plate;
   480 total;
3. **sole plates**: pump-foot/motor-foot sole-plate tops keep the original
   bearing heights;
4. **20mm hex washers + through shanks + hex nuts** (reference washers 20
   thick, bolts through): BASE anchor washers 20mm seated on the baseplate
   top, shanks extended to the nut top, nuts seated on the washer top; DRIVER
   washers 20mm seated on the motor pad top, nuts seated on the shank top;
5. cross beams, baseplates, 30 holes and nozzles unchanged.

Verification: 480 PYRAMIDs all touching the sole-plate bottoms; 328 hex
washers + 328 nuts all seated; 30 holes closed; baseplates/nozzles/CATR
unchanged; no new clashes; lowest point U=0.

## r9 — base rebuilt per DBOutput (P1502B / PUMP006) (2026-08-06)

The user stated that r5–r8 changed the base too little visually and
designated `C:\Users\A\Desktop\DBOutput.txt` (P1502B, template
`/STD/PUMP006`) as the base reference, replacing pump.txt (PUMP005). r9
rebuilds all 30 pump bases per the PUMP006 structure, adapting per pump; only
the base scope changes:

1. **5-member longitudinal frame**: each pump's former 2 flat-bar rails +
   cross braces become 2 outer rails + 2 inner rails + centre plate, 5
   members total (20mm high, seated on the baseplate top, original rail
   footprint/length kept; former cross braces removed); 150 members total;
2. **pump-end side plates + cross beam**: 2 vertical side plates (10×188mm)
   in the gap between the pump-end foot columns, plus 1 through cross-beam
   EXTRUSION (4-vertex LOOP); side-plate tops clear the casing/casing
   fasteners/suction-discharge bottoms (some casings already embed into the
   sole plates by a few mm); when low drain/seal-flush pipes block the
   footprint, the whole group is trial-shifted outward from the pump end by
   two steps; 60 side plates + 30 cross beams;
3. **large/small PYRAMID gussets**: each pump foot and motor pad becomes the
   reference "one large + one small" pair: the large gusset along the foot's
   long axis (YBOT=foot length, offset toward the frame centre), the small
   one along the transverse axis (0.75×foot width, offset toward the
   centre); 480 total;
4. **anchors moved into the feet**: BASE 4 (pump-foot outer edges) + DRIVER 4
   (motor-pad outer edges), each "through shank + 20mm hex washer on the
   baseplate top + hex nut on the sole/pad top" (240 shanks + 240 washers +
   240 nuts).

Unchanged: baseplate sizes/coordinates, 60 nozzles, trailing CATR, pump/motor
bodies, 30 NCYLI holes, hierarchy and naming; lowest point U 0.

Verification (`tools/verify_r9.py`):

- hierarchy: 30 EQUI / 360 SUBE / 5045 primitives, no out-of-bounds END, no
  residual stack;
- non-base scope block-identical to r8 (3365 blocks); baseplates/nozzles/CATR
  unchanged;
- all 150 frame members seated on the baseplate top (bottom 50 / top 70);
- 60 side plates + 30 cross beams all seated and clash-free against
  casing/fasteners/suction-discharge;
- 480 PYRAMIDs bottomed on the frame top, top faces touching the
  sole-plate/motor-pad bottoms;
- all 240 anchor sets pass (shank bottom embedded in the baseplate ≥40mm,
  washer seated on the baseplate top, nut seated on the sole/pad top, shank
  top = nut top), hex sizes plausible (across-flats <200mm);
- large cross-SUBE overlap list identical to r8 (no new clashes).

Loading is the same as r8 (E3D data import); r9 still needs an E3D visual
review (IR-11d): check that the 5-member frame, pump-end side plates/cross
beam, large/small gussets and through anchors read as the PUMP006 base.

## r10 — physical support logic correction (2026-08-06, user rejected r9)

User feedback: r9's base has "floating parts, no visual support, misplaced
bolts, no physical logic". r10 redoes the base around the reference's support
essence. Principle: **every part either carries what is above it or is
carried by what is below it; no floating parts allowed**.

1. **Anchors through the foot/pad centres**: 2 anchors per pump foot/motor
   pad (at 1/4 and 3/4 of the long axis, transversely centred); shank through
   the foot plate, hex washer seated on the baseplate top, hex nut seated on
   the sole/pad top; 480 shanks + 480 washers + 480 nuts. r9 placed anchors
   at the foot outer edges, leaving nuts hanging beside the plates — fixed;
2. **pump-end structure emitted only when it can be fully carried**: 2 side
   plates stand on the frame top and genuinely carry a pump-end sole plate
   (at the same height as the foot sole plates), with a cross beam tying the
   side plates; the whole set must sit fully inside the frame footprint and
   clear the casing/fasteners/suction-discharge. 13 pumps qualify; the other
   17 cannot accommodate it because real low-hanging small pipes/flange parts
   exist at the pump end (lowest U 89.9–180.6mm), so the whole group is
   omitted — no more floating side plates/cross beams;
3. **support-chain numerical audit**: all base elements of all 30 pumps have
   their bottom faces on a supporter (baseplate top/frame top/gusset
   top/side-plate top) within 0.51mm; floating count 0.

Unchanged: baseplate sizes/coordinates, 60 nozzles, CATR, pump/motor bodies,
30 NCYLI holes, hierarchy and naming; non-base scope block-identical to r8;
lowest point U 0; large cross-SUBE overlap list identical to r8 (no new
clashes).

Verification: `tools/verify_r10.py` all green (30 EQUI / 360 SUBE / 5727
primitives; 150 5-member frame members; 480 gussets; anchors 8+8 per pump all
seated and inside the foot plates; pump-end support chain complete; 973
EXTRUSIONs structurally valid).

## r11 — bridge brackets (horizontal-diagonal-flat-diagonal-horizontal, 2026-08-06, user rejected r10)

User feedback: the diagonal plates and screws intersect at the same position;
the diagonals are too short and do not reach the upper platform; the
diagonals' bottom needs a screw-fixed auxiliary block; the support-plate
cross-section should look like a bridge — **horizontal-diagonal-flat-
diagonal-horizontal**. r11 discards the old PYRAMID diagonals + through-foot
anchors and replaces every pump-foot/motor-pad support with a bridge bracket:

1. **bottom auxiliary block** (12mm, full sole-plate footprint) seated on the
   frame top, fixed by 1 screw at each transverse edge (nut on the block top,
   shank into the frame/baseplate);
2. **lower diagonal plate**: EXTRUSION parallelogram slanted plate from the
   block top up to the middle-plate bottom;
3. **middle flat plate** (8mm);
4. **upper diagonal plate**: from the middle-plate top up to the platform
   bottom, full-width contact — the diagonal now genuinely connects to the
   upper platform; the two diagonals lean in opposite directions, forming the
   bridge look;
5. the diagonals are transversely narrower than the block (leaving the screw
   positions at both sides), so screws/nuts have zero intersection with the
   diagonals (verified with an exact parallelogram intersection check, not
   AABB approximation); small platforms scale each thickness proportionally,
   and the nut across-flats shrinks accordingly (≥6mm).

Numerical verification (`tools/verify_r11.py` all green):

- 30 EQUI / 360 SUBE / 5727 primitives; non-base scope block-identical to
  r8;
- PYRAMID count 0; 240 auxiliary blocks + 240 middle plates all seated;
- 480 diagonal plates' support chain continuous:
  block→lower diagonal→middle plate→upper diagonal→platform (contact
  ≤0.51mm);
- 480 screws (8 BASE + 8 DRIVER per pump), nuts on the block top, zero
  intersection with diagonals/middle plates;
- support-chain audit 0 floating; large cross-SUBE overlap list identical to
  r8.

Unchanged: baseplate sizes/coordinates, 60 nozzles, CATR, pump/motor bodies,
30 NCYLI holes, hierarchy and naming; lowest point U 0.

## Loading

Same as JK_PU.txt: load
`JK_Pump_Build_refined_20260805_r11.pml` via E3D data import in a writable
ZONE. After loading, visually review (IR-11d): whether the bridge bracket
under each foot/pad shows the horizontal-diagonal-flat-diagonal-horizontal
profile, whether the diagonals seat flush against the platform bottoms,
whether the auxiliary-block edge screws are fully clear of the diagonals, and
whether the pump-end side plates/sole plate genuinely carry.

## Failure record (2026-08-06, r11 finally rejected)

After loading r11, the user's verdict: "complete failure: the base support
and the pump/motor are completely separated" — the base supports and
pump/motor were completely separated, not as expected; no further
modification requested; this version is archived as a **failed revision
case**. On the same day r9 (PUMP006 copy) and r10 (physical-support
correction) were also rejected; the day's only retained achievement is the
negative-primitive (NCYLI) series (r2–r5: child local coordinates, NAPPFLAG
2, per-pump hole boundary — VERIFIED in pml1-reference). The base optimisation
thread is closed, to continue when new direction arrives.

## Change list

### A. Bridge-type standard brackets (30 pumps)

The two solid foot pads of each pump become "bridge-type standard brackets" —
top sole plate + two trapezoid gussets:

- pump brackets (4 solid foot pads in `SUPPORT_FRAME`): each pad replaced by
  1 sole plate (BOX) + 2 trapezoid gussets (EXTRUSION, at the two ends along
  the pad's long axis);
- motor brackets (4 mounting pads in `DRIVER`): likewise replaced by 1 sole
  plate + 2 trapezoid gussets;
- the original pads' plan footprint, bottom elevation and top bearing height
  are all unchanged (numerical verification 0 deviation);
- gusset bottoms flush with the original pad bottom; gusset tops contact the
  sole-plate bottoms (all within 0.5mm tolerance).

All new dimensions are Reference Values:

| Item | Value | Basis |
|------|------|------|
| Sole-plate thickness | 42% of the original pad height, 10–16mm | proportional to pad height, visually reasonable |
| Gusset thickness | 10mm | common plate-bracket thickness (Reference Value) |
| Gusset taper | ≤24mm (each side) | trapezoid-gusset visual proportion (Reference Value) |
| Hex-nut across-flats | = original round-cap diameter | retains the original fastener envelope |

### B. Hex nuts (EXTRUSION, new syntax)

All 328 circular caps in `BASE_FASTENERS` and `DRIVER_FASTENERS` upgraded to
true hex nuts:

- each nut is a 6-vertex EXTRUSION (VERIFIED form) whose end-plane POS sits
  at the original cap's bottom face;
- contacts the washer/shank top (328/328 pass the 1mm seating check);
- position, height and centre identical to the original cap; only the outline
  changes from round to hex.

### C. Clash and structural fixes

1. **205-PU-054 (MC pump)**:
   - the separator column group (first 20 primitives of `MC_AUXILIARY`)
     translated -E by 30mm, clear of the pump casing;
   - the separator vessel group (box, top plate, studs, feet, outlet pipe)
     previously interpenetrated the casing, front cover cone and discharge
     flange disc simultaneously, with no usable clearance on the discharge
     side; moved as a whole to the only viable motor-side position
     (E +60mm / N -1292mm); the outlet pipe follows and still runs from the
     box to the baseplate's east edge;
   - after the fix, overlaps with casing, support frame, casing fasteners,
     discharge subassembly and baseplate fasteners are all 0.
2. **205-PU-038 (MC pump)**: separator columns and vessel box raised +U 5mm,
   seated on the pump support feet, no longer cutting into the support-foot
   tops (overlap cleared).
3. **205-PU-060 / 061 (wash-water circulation pumps)**: `SERVICE_DETAILS`
   splash plate lowered 35mm, clear of the main casing bottom; the retained
   casing–seal-flush pipe overlap is an intentional connection (φ18 pipe
   enters the casing).

## Unchanged (verified)

- 30 baseplates: per-block attribute signatures identical to the source file;
- 60 nozzles: POS / ORI / HEIG / TEMP / PRES / TPRESS identical to the source
  file;
- trailing 60 `OLD NOZZLE ... CATR SPCOMPONENT ...` bindings: byte-identical;
- EQUI/SUBE hierarchy and naming: unchanged;
- all other unauthorised geometry (casing, bearing frame, coupling, motor
  body, service details, etc.): unchanged.

## Numerical verification results

- baseplate signatures identical: 30/30;
- nozzle blocks identical: 60/60; CATR bindings identical: 60/60;
- bridge gussets: 8 per pump (4 pump + 4 motor), 480 total, all touching
  their sole plates;
- EXTRUSION structure: 808 blocks, LOOP + 4/6 vertices, no structural errors;
- lowest point: U = 0 (no primitive below the foundation plane);
- bearing heights preserved: 240 replacement pads 0 deviation;
- nuts seated: 328/328;
- targeted clash pairs: 054 (5 sets), 038 (1 set), 060/061 (2 sets) all
  cleared;
- remaining large overlaps are pre-existing intentional contacts: pump feet
  embedded in the casing bottom, discharge stubs embedded in the casing,
  bearing frame seated in the casing (consistent with the source file; no new
  overlaps introduced).

## Notes and open items

- The 205-PU-054 separator vessel moved a large distance (about 1.3m); this
  is the only placement found by the numerical search that both avoids the
  casing/cone and stays on the baseplate; confirm the separator-side
  arrangement against the pump's top view.
- 205-PU-054's outlet pipe outer end protrudes about 60mm beyond the
  baseplate's east edge as a nozzle projection for piping connection (the
  nozzle itself is unchanged).
- 205-PU-018 / 004 MC auxiliary motors have about 5–8mm embedded contact with
  the main motor mounting pads (present in the original model; visually the
  motor sits into the pad); not changed this round; provide a top-view basis
  if full separation is required.
- This file is an E3D native data-listing format (`INPUT BEGIN/END`);
  primitive attributes use E3D's own POS-first export order; the project's
  `validate_pml` ORI-before-POS rule targets generated macros and does not
  apply to this loading path.
- All bridge and nut dimensions are Reference Values and can be replaced when
  vendor GA/motor samples are updated.
