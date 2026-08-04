# JK_Cooking_Tank_Build — R6 native-export rework archive

**Date:** 2026-08-02
**State:** Native E3D export `cooking_tank.txt` reworked per user request;
all three modification rounds verified numerically. Not yet re-imported.
**Continuation:** Baseline for any future request on these 15 tanks.

---

## What happened

The user supplied a fresh native E3D data listing of the `/COOKING_TANK`
zone (`cooking_tank.txt`, 14,498 lines, export 2026-08-02 19:39) and asked
for three sequential edits. Each round was verified against the previous
state with `diff` (only intended hunks), END-balance checks, and numeric
geometry checks.

### Round 1 — base plates under every tank

- Added one `_BASEPLATE` subequipment to **14 of 15 tanks**
  (`MAIN_CONDENSATE_TANK` excluded per instruction). Each contains one
  CYLINDER:
  - `HEIG 50mm`
  - `DIAM = tank main-shell diameter + 300mm`
  - top surface flush with tank bottom: `POS ... D 325mm`
    (all tank assemblies bottom out at D 300; plate centre at D 325)
  - same E/N axis as the tank shell
- Main-body diameters used: BLEACH 5020, BLOW 7300, WARM 5700,
  BROWN 5714, JUNK_TRAP 1770, ACCUMULATOR 7023, AID 2022,
  W_L_SERVICE 5000, SPENT 3000, B_L 5020.

### Round 2 — slim the SUPPORT subequipment

- For **10 of 15 tanks** (all except BLOW_TANK_1/2, JUNK_TRAP_1/2,
  MAIN_CONDENSATE_TANK), removed every BOX from the SUPPORT subequipment:
  foot plates (180×180×16), sole plates (240×90×20) and legs
  (100×100×140) — the "legs" group.
- Kept only the bolt CYLINDERs (DIAM 30 stud / 60 washer / 52 nut).
- Result per tank: 36 bolts kept (12 groups × 3), BOXes removed.

### Round 3 — correction + bolt ring moved inward

- **Correction:** `ACCUMULATOR_TANK`, `ACCUMULATOR_TANK_AID_1` and
  `ACCUMULATOR_TANK_AID_2` keep their **skirt** (CYLINDER, same DIAM as
  shell, HEIG 1800 / 800) and **base ring** (CYLINDER, same DIAM,
  HEIG 30, D 285). These were wrongly removed in round 2 and restored
  verbatim from the pre-slim backup. Only the small-leg BOXes stay
  deleted; the bolts stay.
- **Bolt ring:** all 348 bolts in the 10 slimmed tanks were moved
  radially inward from "tank wall + 150mm" (the plate edge) to
  "tank wall + 75mm" (mid-width of the 300mm-wide base plate).
  Verified per bolt: radial distance = tank radius + 75mm, error < 1mm.

---

## Current structure (10 slimmed tanks)

Mode A — 7 tanks (BLEACH / WARM / BROWN / B_L / SPENT / W_L_SERVICE_1/2):

```text
SUPPORT   = 36 bolt CYLINDERs only (12 groups × stud30 + washer60 + nut52)
BASEPLATE = 1 CYLINDER (DIAM = shell + 300, HEIG 50, D 325)
```

Mode B — 3 tanks (ACCUMULATOR / AID_1 / AID_2):

```text
SUPPORT   = skirt CYLINDER (shell DIAM, HEIG 1800/800, U 600/100)
          + base-ring CYLINDER (shell DIAM, HEIG 30, D 285)
          + bolt CYLINDERs (48 / 24 / 24)
BASEPLATE = 1 CYLINDER (DIAM = shell + 300, HEIG 50, D 325)
```

Untouched: BLOW_TANK_1/2, JUNK_TRAP_1/2, MAIN_CONDENSATE_TANK — their
SUPPORT blocks are byte-identical to the original export (verified).

---

## Verification performed

- `diff` old vs new: every hunk lies inside a target SUPPORT section; 0
  hunks outside. Excluded tanks byte-identical.
- END balance: each added CYLINDER block contributes +2 END; final count
  1695 (original 2029 → +14 base plates → −344 slim → +12 restore).
- Bolt geometry: all 348 bolts at shell radius + 75mm (±1mm).
- PML1: zero banned tokens (`!!Alert`, `ENDS`, `COLLECT`, `UNSET`, `$P`).
- File encoding preserved: UTF-8 with BOM, CRLF.

## Files

| File | Purpose |
|------|---------|
| `cooking_tank.txt` | Final reworked export (ready to import) |
| `add_tank_baseplates.py` | Round 1 generator (anchor-based) |
| `slim_tank_supports.py` | Round 2 slim-down (parses SUPPORT blocks) |
| `fix_supports.py` | Round 3 restore + bolt move |
| `backups/cooking_tank_orig_backup.txt` | Original export (pre-Round 1) |
| `backups/cooking_tank_before_slim_backup.txt` | After Round 1 |
| `backups/cooking_tank_before_restore_backup.txt` | After Round 2 |

**Caution:** the three scripts are anchored to the file state they were
written against (line indices / `NEW SUBEQUIPMENT /<tank>_N1` anchors).
Re-running them on the current file will corrupt it. To replay a round,
restore the matching backup first, or treat the scripts as reference
logic and re-derive the anchors.

---

## Coordinate system notes (read before any edit)

- The file mixes two POS conventions, sometimes within one tank:
  - `POS E ... N ... U ...` (north/up positive)
  - `POS E ... S ... D ...` (south/down positive; S = −N, D = −U)
- Example: `POS E 18720mm S 6004mm D 290mm` ≡ `E 18720 N -6004 U -290`.
- All tanks bottom out at **D 300 (= U −300)**; base plates sit at D 325.
- New elements must reuse the axis naming of the surrounding tank block.

## PML1 rules (violation aborts the macro)

- PML1 only: no `!!Alert`, `$P`, `ENDS`, `END EQUI`, `NAME =`, `DESC =`,
  `!var =`, `COLLECT`, `UNSET`, `!!CE`, `!!WORLD`. Attributes without `=`.
- `POS` is the geometric centre for CYLI/CONE/BOX; DISH uses its rim.
- New block template (follow the file's exact blank-line style: blank
  line before each primitive `END`, none between blocks).

## Pitfalls paid for in this session

1. Always back up before editing a large export (no git on Desktop).
2. Multi-block edits must be applied bottom-up, or line indices shift
   and later blocks land in the wrong place.
3. Parsing a SUBEQUIPMENT block: the subequipment-closing `END` is easily
   swallowed into the header — use primitive-depth counting, never simple
   string matching.
4. A passing text check is not a passing geometry check; verify numbers
   (AGENTS.md iron rule).

## Rollback

- To "after Round 1": `backups/cooking_tank_before_slim_backup.txt`
- To original export: `backups/cooking_tank_orig_backup.txt`
- Restore by `cp backups/<file> cooking_tank.txt`.
