# JK-Project — Pulp Mill WSB Area

**Scope:** 3D modelling of all tank-type equipment in the Washing, Screening and
Bleaching area, for AVEVA E3D.
**Status:** Delivered and verified.
**Folder:** `Projects/JK-Tank_Build/` (logical name `JK-Project`, declared in
`project.json`)
**Brief:** [Do.txt](../../Projects/JK-Tank_Build/Do.txt) — the client's
specification, and the living instruction prompt for this project.

---

## Delivered

| Metric | Value |
|--------|-------|
| Equipment items | 22 |
| Primitives | 451 |
| Nozzles | 114 |
| Reference Values pending confirmation | 104 |
| Source data defects corrected | 18 |
| Bottom centre points verified | 22 / 22 |

Regenerate:

```bash
python -m wsb --project JK-Project
```

Outputs `Projects/JK-Tank_Build/output/JK-Project_<timestamp>.pml` and a matching
report, named after the project so a macro found later can be traced back to the
folder that produced it. `--dry-run` validates without writing; it exits non-zero
if any tank fails verification.

---

## Equipment

| Area | Items |
|------|-------|
| 203 — Brown Stock / O₂ | TA-006 filtrate tank, TA-019 O₂ feed tank, TA-024 1st O₂ reactor, TA-029 2nd O₂ reactor, TA-044 instrument air receiver |
| 204 — Screening & Washing | TA-001 O₂ blow tank, TA-021 primary screen dropleg, TA-034 screen dilution tank, TA-035 post-O₂ filtrate tank |
| 205 — Bleaching Plant | TA-001 unbleached storage tower, TA-008 D0 tower, TA-011 D0 filtrate tank, TA-016 D0 dropleg, TA-022 EOP reactor, TA-025 EOP blow tank, TA-029 EOP filtrate tank, TA-036 EOP dropleg, TA-042 D1 tower, TA-045 D1 filtrate tank, TA-052 D1 dropleg, TA-056 bleached storage tower, TA-059 scrubber |

Configuration per duty follows
[tanks-and-vessels.md](../equipment/tanks-and-vessels.md); that table was derived
from this project.

---

## Source data

All under `Projects/JK-Tank_Build/`:

| File | Role |
|------|------|
| `Do.txt` | Instruction prompt — the requirements, kept current |
| `Modeling_lists.xlsx` | Primary contractual equipment data |
| `equipment_data.py` | The 22-tank dataset, with provenance per value |
| `Model_Reference(All_Top_View)/` | Configuration and appearance |
| `Model_reference(Part_Side_View)/` | P&ID sketches: volume, height, diameter, temperature |
| `output/` | `JK-Project.pml` and the engineering report |

Every value carries a provenance; assumptions (`STANDARD`, `VENDOR_TYPICAL`,
`DERIVED`) are listed individually in the deliverable so they can be replaced when
official design data is issued.

### Data defects found — corrected in the data layer, never in the workbook

**1. Corrupted coordinates (13 of 22 rows).** Rows Excel stored as numbers lost
their parentheses and commas, concatenating the digits: `-1500019860300` is
`(15000, 19860, 300)`.

All restored coordinates are positive — **the minus sign on a corrupted cell is
an artefact of the concatenation, not project data.** The 9 rows that survived as
text keep their listed signs unchanged. Every one of the 22 coordinates was
re-derived from the raw workbook XML and matches the dataset exactly.

**2. Transposed height and diameter on `205-TA-008` and `205-TA-011`.** The side
views give the correct orientation. For `205-TA-008` the transposed reading
implies 706 m³ against a stated 65 m³ — an order of magnitude out.

*This is the general detection method:* reconcile π/4·D²·H against the stated
volume. A ~10× discrepancy means the terms are swapped.

**3. `2205-TA-050.png` is misnamed.** The drawing it contains is `205-TA-059`.

Each defect is reported as a data-quality exception in the deliverable. The
client needs to know the source data is defective; silently fixing it hides a
problem that recurs.

---

## Problems encountered and how they were solved

| Problem | Symptom | Resolution |
|---------|---------|------------|
| Invented render prologue | `(47,15) CP: Syntax error / ^^SUSPEND` | `SUSPEND`/`RESUME`/`VAR 0`/`ALPHA HEADER` are not E3D commands — confirmed absent from AVEVA's `pmllib`. Removed and banned. → **IR-4** |
| Wrong CYLI/CONE datum | Shells, skirts and primitive nozzle parts telescoped into one another | Knowledge base wrongly claimed a bottom-face datum. CYLI/CONE `POS` is the geometric centre; conversion centralised in `PMLBuilder._position`. A later user correction established that DISH is the rim-plane exception. → **IR-1** |
| Coordinate drift | Transverse elements away from intended positions, no error | `POS` was emitted before `ORI`. Builder now emits `ORI` first structurally. → **IR-2** |
| Vessels on their side | Vertical tanks rendering horizontally | Axis is Z, not Y — verified against `gphFactory.pmlobj:632`. → **IR-3** |
| False-positive verification | Verification passed a model with wrong datums | String-matching a `POS` line proves only that *some* primitive sits there. Replaced with a geometric parse computing true extents. → **IR-6** |
| Equipment shifted as a block | Whole tanks offset by a constant | A bare `POS` is relative to the owner; every EQUI now explicitly anchored at `POS E 0 N 0 U 0`. → **IR-7** |

**The pattern worth remembering:** four of these six were *silent* — the macro
loaded cleanly and the geometry was wrong. Only numerical verification caught
them. This is why [IR-6](../knowledge/iron-rules.md#ir-6--tank-equipment-is-set-out-from-its-bottom-centre-point)
insists on parsing geometry rather than reading the macro.

### Second round: the nozzle campaign

A later session found the model's nozzles unusable. What looked like one bug was
six, each hiding the next — and **numerical verification caught none of them**.
Every one was found by the client loading the macro and reporting what they saw.

| # | Symptom | Cause | Rule |
|---|---------|-------|------|
| 1 | Floating discs beside every tank | Ladder cage hoops as solid `CYLI` rings | IR-9b |
| 2 | Nozzles in the tree, invisible in 3D | No catalogue component bound | IR-9a |
| 3 | Only the first tank loaded | `CATR` emitted in a trailing pass; P-points do not exist yet | IR-9a |
| 4 | `(2,108) ... is not a SPCO` | Passed the SPCO's `Catref` value, not its own path | [catalogue-elements](../knowledge/catalogue-elements.md) |
| 5 | Nozzles aimed wrongly | Oriented on a geometric axis instead of `ORI P1 IS` | IR-2 |
| 6 | Barrels buried; only flange rims visible | `POS` is the **flange face**, not the root | IR-9a |

Plus a self-inflicted regression: a mis-read `HEIG` datum emitted lengths from
−61680 to +72280 mm and drew the model as a thicket of flying tubes. A negative
length is impossible; no datum argument was needed to reject it. That produced
**[IR-11](../knowledge/iron-rules.md#ir-11--how-a-rule-earns-the-word-verified)**
— bounds before theories, and property tests over formula tests.

**Why this round was harder than the first.** A catalogue element has more
independent failure modes than a primitive, and the geometric checks that caught
round one are blind to all of them: an unbound nozzle has a *correct* position.
Verification has to reach the property a designer cares about — does the barrel
pass through the wall — not the numbers the generator just wrote.

The client's screenshots were the diagnostic instrument throughout. Two of the
six were identified by the client directly, including the flange-face datum.

---

## Client corrections

| Date | Correction | Applied |
|------|------------|---------|
| 2026-07 | `205-TA-052` diameter corrected against the equipment list | `Provenance.CLIENT`, which ranks above `EXCEL` — later information from the same authority |

The `CLIENT` provenance exists because of this: a client confirmation must
outrank the equipment list without being mistaken for an assumption.

---

## Reference Values

104 values are assumed pending confirmation — principally nozzle schedules where
the drawings do not dimension them, head and skirt heights, stiffening rings and
platform details. Each is itemised in the generated report with its basis.

Nozzles are the largest group: where drawings do not show them, the minimum
process-logical set was provided (feed, discharge, overflow, vent, drain, manway),
sized to duty and spread across distinct bearings so future piping does not
collide.

---

## Outstanding issues

- Nozzle schedules require confirmation against vendor GA drawings for most items
- Overall heights unconfirmed where derived from volume
- Top-mounted structures on several towers cannot be identified from available
  photographs
- Platform extents are approximate where drawings show them only partially

---

## Lessons promoted into the skill

All six problems above became Iron Rules IR-1 through IR-7, and are enforced in
code rather than by review:

- `validate_pml()` rejects PML2 syntax, banned directives, and ORI/POS ordering
  violations
- `verify_bottom_centre()` verifies datums geometrically
- `python -m wsb` exits non-zero on any failure

93 tests cover the guarantees that cannot be checked by eye across 400+
primitives.

## 2026-08-04 — DROPLEG appearance retrofit (WSB_TA.txt)

Native export `WSB_TA.txt` was retrofitted for five droplegs
(203-TA-019, 204-TA-021, 205-TA-016, 205-TA-036, 205-TA-052): SUPPORT/SHELL
rebuilt as a four-cylinder stack (D1246×100 / D1006×4991 / D1044×10 /
D610×4885) from the unchanged bottom centre, plus a default DN200 lower nozzle
with pad and catalogue binding per the export's trailing OLD/CATR style.
Original preserved under `Projects/JK-Tank_Build/imports/2026-08-04_WSB_TA.txt`;
deliverable and report under `Projects/JK-Tank_Build/output/`. Outstanding:
existing top/side nozzles keep their original coordinates and will stand off
the shorter body; user confirmation needed before re-seating them.

R2 (same day, user follow-up): removed every original nozzle and the ACCESS
subequipment from the five droplegs, keeping only the new DN200 lower nozzle;
17 matching OLD/CATR bindings removed (114 -> 97). Final file
`Projects/JK-Tank_Build/output/WSB_TA_dropleg_retrofit_20260804_r2.txt`; R1
kept for rollback.

R3 (same day, user correction): new DN200 nozzle ORI corrected to
`Y is S and Z is U` (East-facing side nozzle). Lesson: in native data-listing
NOZZLE blocks, ORI Y is the roll reference perpendicular to the bore, not the
bore direction (North-facing = Y is E, East-facing = Y is S). Final file
`Projects/JK-Tank_Build/output/WSB_TA_dropleg_retrofit_20260804_r3.txt`.

Archived 2026-08-04 under
`Projects/JK-Tank_Build/archive/2026-08-04_WSB_TA_dropleg/` (R1/R2/R3 + hashes
in `REVISION_RECORD.md`); project time tree added at
`Projects/JK-Tank_Build/TIMELINE.md`.

The duty-based configuration table in
[tanks-and-vessels.md](../equipment/tanks-and-vessels.md) is this project's main
reusable output.

## 2026-08-10 — Bottom hex-bolt detail pass (R4)

User supplied a new native export `jk_tank_edited_by_me.txt` (zone `/WSB_TA`)
with manual edits on top of the R3 baseline, and asked for bottom hex bolts on
every tank except 203-TA-044, 203-TA-019, 204-TA-021, 205-TA-016,
205-TA-036 and 205-TA-052, with the nut flush against the bottom plate and
counts scaled to tank size.

r1 (under-plate nuts, bolt circle on the inner plate) was rejected in visual
review with three corrections: the bottom-plate boundary had to be the widest
lowest short cylinder (exposed base ring), the style had to be anchor bolts
(nut flush on the plate top, stud embedded below), and the nut had to scale
up to M30–M48 to read as physically plausible. r2 applies all three:
260 anchor bolts inserted only into the 16 target SHELL/SUPPORT
subequipments, on a bolt circle at plate/ring radius − 100 mm (>= 40 mm
outside the shell wall, verified per tank). 205-TA-056 gained one base ring
DIAM 10200 × 50 (it had no exposed annulus under its 9900 outer shell).
Excluded tanks byte-identical; all user manual edits preserved. r3 fixes the
one remaining placement error: 205-TA-059 now anchors on its OUTER base ring
(DIAM 3000, SHELL, 16 × M36) instead of the inner DIAM 1800 ring in SUPPORT.
Deliverable:
`Projects/JK-Tank_Build/output/WSB_TA_hexbolts_20260810_r3.txt`; archive and
hashes in `Projects/JK-Tank_Build/archive/2026-08-10_hexbolts/`.

**User accepted r3 on 2026-08-10** ("可以，将错误原因记好"). The recorded
error causes, kept for the next continuation:

1. r1 — plate boundary read as the thinnest lowest cylinder instead of the
   widest exposed base ring; bolt circle inside the shell footprint and nut
   under the plate. Fix: anchor on the exposed annulus of the widest short
   bottom cylinder, nut flush on the plate top.
2. r2 — 205-TA-059's outer base ring (DIAM 3000) lives in the SHELL
   subequipment under the 2700 outer shell, while SUPPORT only holds the
   inner DIAM 1800 skirt ring; the schedule pointed at SUPPORT and anchored
   on the inner ring. Fix: when a tank has two base rings, anchor on the
   OUTERMOST one; check the SHELL subequipment for the outer ring, not just
   the SUPPORT subequipment.

Both causes and the general rule are recorded in
[tanks-and-vessels.md](../equipment/tanks-and-vessels.md) and in
`Projects/JK-Tank_Build/archive/2026-08-10_hexbolts/REVISION_RECORD.md`.

Assumptions flagged in the record: size classes, count bands and embedment
8×d / protrusion 1×d (anchor-bolt practice); the added 205-TA-056 base ring.

No new lessons promoted: the hex `EXTRUSION` form was already VERIFIED and the
workflow (preserve native export, insert-only patch, numeric verification)
reused the existing rules unchanged. The one reusable refinement — "the 底盘
boundary is the widest short cylinder at the lowest elevation, and anchor
bolts go on its exposed annulus" — is captured in
[tanks-and-vessels.md](../equipment/tanks-and-vessels.md) guidance below.

## 2026-08-10 — Top platform handrails r3 (candidate, pending E3D acceptance)

Continuing the R5 top-handrail job: r2 (native HANDRA + RPATH `CURTYP THRU` +
RAILSET, no posts) loaded but rendered nothing the user could see; the user
rejected it with "没有形成楼梯，放置的位置也不对；应是圆盘底座" (no handrail
formed, wrong position, needs a circular disc base) and asked to continue the
next day.

r3 replaces the unverified HANDRA/RPATH template form with plain CYLI
primitives inserted as one new SUBEQUIPMENT per tank
(`/205_TA_001_TOP_PLATFORM`, `/205_TA_056_TOP_PLATFORM`) under the existing
EQUIPMENT blocks:

- circular platform disc closing the frustum top (DIAM 6000 x 12 at U 28200 /
  DIAM 6500 x 12 at U 27700) — the 圆盘底座;
- 20 / 24 posts (DIAM 48.3, spacing <= 1000 mm) on individual circular base
  plates (DIAM 200 x 10) at the rail circle (platform rim inset 150 mm);
- top rail at platform + 1100 mm and mid rail at + 550 mm, built from 80 / 96
  short tangent CYLI segments per rail (sagitta 1.7–2.2 mm, visually smooth).

Insertion-only: everything outside the two insertion points is byte-identical
to the accepted R4 hex-bolt baseline; `validate_pml()` reports 0 new findings;
NEW/END hierarchy balanced; geometry verified numerically (disc flush at the
platform top, every post and rail segment on the rail circle).

Deliverable: `Projects/JK-Tank_Build/output/WSB_TA_top_handrails_20260810_r3.txt`
(desktop copy `jk_tank_edited_by_me_top_handrails_r3.txt`); archive and hashes
in `Projects/JK-Tank_Build/archive/2026-08-10_top_handrails_r3/`.

Reference values flagged in the record: tube OD 48.3 mm, base plate
DIAM 200 x 10, disc thickness 12 mm, rail inset 150 mm, top/mid rail heights
1100 / 550 mm. Open: confirm the second tank is 205-TA-056 (205-TA-006 does
not exist), and confirm the user's "楼梯/扶梯" wording means the top platform
handrail and not a spiral access stair up the shell.

**Lesson recorded (F-22 in diagnosing-failures.md):** a HANDRA block with an
RPATH of `CURTYP THRU` curves and no POSTSE/HRPOST loaded silently and rendered
nothing — an unverified structural-template form must not be shipped as the
sole representation. Primitives are the fallback until a native handrail block
is proven in E3D.

### 2026-08-10 — r4: handrail moved to the cylinder-top big circle (CONFIRMED)

The user accepted that r3 rendered ("可以，楼梯正常出现") but corrected the
position: the handrail must circle the shell-cylinder top big circle, not the
frustum-top small circle; the frustum will be adjusted by the designer
afterwards. r4 drops the platform disc and places the handrail on the cylinder
top face at U 26400 — TA-001 rail circle R 5300 (36 posts), TA-056 rail circle
R 4850 (32 posts), base plates flush at the rim, top rail +1100 mm, mid rail
+550 mm, 144/128 tangent CYLI segments. The cone surface near the rim passes
through the post zone for ~30–40 mm until the frustum is re-sized; this is
reported rather than hidden (user said "我再调整圆台大小").

**User confirmed r4 on 2026-08-10** ("可以，干的漂亮"). The r4 file is the
accepted working baseline for the next continuation.

Deliverable:
`Projects/JK-Tank_Build/output/WSB_TA_top_handrails_20260810_r4.txt`; archive
and hashes in `Projects/JK-Tank_Build/archive/2026-08-10_top_handrails_r4/`.
The reusable correction is recorded in
[tanks-and-vessels.md](../equipment/tanks-and-vessels.md): a frustum-roof top
handrail follows the shell-cylinder rim, not the frustum top.

### 2026-08-31 — R8: Native structural handrail (HANDRA/RPATH) & ladder safety integration (CONFIRMED)

The earlier 2026-08-10 failure (F-22) was settled via `PML-STUDY-HANDRA-001`. Replaced
the 200+ cylinder approximations on `205-TA-056` and `205-TA-001` with native structural
`HANDRA` / `RPATH` / `POINTR` / `CURVE` (`CURTYP THRU`).

Key rules verified in production (user confirmed: "OK简直完美"):
1. **Structural Hierarchy Contract**: `HANDRA` must be owned by `STRU` -> `FRMWORK`,
   never `SUBEQUIPMENT`.
2. **Absolute Datum Seating Contract**: Handrail base elevation under `ZONE` matches the
   true world elevation of the cylinder rim ($U_{world} = U_{local\_rim} + U_{equipment\_origin}$).
3. **Outward Ladder Connection Contract**: Handrails turn radially OUTWARD across the rim
   to connect directly into the vertical ladder handrail stringers, eliminating sloped roof
   cone penetration.
4. **Vertical Ladder Safety Cage Extension**: Ladder safety cages raised $+1100\text{ mm}$
   (to $U = 27500\text{ mm}$) with added upper hoops and extended bars for complete back protection.

Deliverables: `Projects/JK-Tank_Build/output/WSB_TA_two_tanks_handrails_20260831.pml`
and `WSB_TA_handrails_20260831.txt`. Preserved user screenshot evidence in `archive/`.
