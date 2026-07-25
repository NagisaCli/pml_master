# JK-Project — Pulp Mill WSB Area

**Scope:** 3D modelling of all tank-type equipment in the Washing, Screening and
Bleaching area, for AVEVA E3D.
**Status:** Delivered and verified.
**Folder:** `Projects/JK-Project/`
**Brief:** [Do.txt](../../Projects/JK-Project/Do.txt) — the client's
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

Outputs `Projects/JK-Project/output/JK-Project_<timestamp>.pml` and a matching
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

All under `Projects/JK-Project/`:

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
| Wrong primitive datum | Shells, skirts, heads and nozzles telescoped into one another | Knowledge base wrongly claimed a bottom-face datum. `POS` is the geometric centre for all primitives; conversion centralised in `PMLBuilder._position`. → **IR-1** |
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

The duty-based configuration table in
[tanks-and-vessels.md](../equipment/tanks-and-vessels.md) is this project's main
reusable output.
