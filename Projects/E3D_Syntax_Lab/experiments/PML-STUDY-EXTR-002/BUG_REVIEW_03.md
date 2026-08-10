# Bug Review — PML-STUDY-EXTR-002 candidate 03, round 2 (physics fixes)

Date: 2026-08-05.

Baseline: the user-edited native E3D export
`source/2026-08-05_pump_edit_user_native.txt`
(SHA-256 `0AFE420B2450AFA70FD60473A961D881CAF918E8BD684E20F4C61C4046043630`),
which the user received as `C:\Users\A\Desktop\pump_edit.txt` after loading
the previous cleanup and deleting two floating rounded plates in the casing
and one bearing breather cylinder. It is treated as the new working baseline;
those three user deletions were preserved and never re-added.

All findings below were reproduced numerically by parsing the file and
re-deriving occupied ranges from each element's own datum. None of them is a
visual guess.

---

## User report

1. The motor pedestal bolt nuts float in the air.
2. The junction boxes are not displayed as boxes.
3. The pump-to-top-nozzle connection is open — "part of the connection is empty",
   the nozzle must plug into the pump.

---

## Bug 1 — Pedestal nuts float at the stud tip

**Numerical finding:**

| Item | U range | Result |
|---|---|---|
| Pedestal sole plate top | U 140 | bearing face |
| 8 hex nuts | U 170..186 | 30 mm above the plate |
| 8 bolt studs | U 100..170 | nuts threaded on the stud tip |

The nuts were placed at the top of the stud instead of on the plate, so they
hung in the air with a bare shaft between nut and plate.

**Fix:** nut blocks moved to U 140..156 (seated on the plate); bolts stay
U 100..170, leaving a 14 mm stud protrusion above each nut.

---

## Bug 2 — Junction boxes do not display as boxes

**Finding:** the two terminal boxes were 20-vertex rounded-rectangle
`EXTRUSION` blocks (60 x 50 mm profile, 50 mm high at X 870/970, U 665..715).
The user's E3D session did not show them as boxes.

**Fix:** replaced both extrusions with native `BOX` primitives
(XLEN 60 / YLEN 50 / ZLEN 50 at E 870/970, N 0, U 690, i.e. U 665..715).
Mounting plate, centre pedestal column, conduit stubs and plate bolts are
unchanged, so the assembly keeps its coupling.

---

## Bug 3 — Nozzle-to-pump connection gaps

**Numerical finding (top suction nozzle):**

| Item | Extent | Result |
|---|---|---|
| Volute dome peak | U 700 at N 0 | dome surface at r 85 ≈ U 681.6 |
| Top nozzle pipe (DIAM 170) | U 745..835 | 45 mm open gap above the dome |

The pipe bottom face was flat at U 745 while the dome peak was U 700, so the
connection was visibly empty.

**Numerical finding (discharge nozzle):**

| Item | Extent | Result |
|---|---|---|
| Volute left face | X -150 | flush face of the 97-vertex extrusion |
| Discharge pipe (DIAM 170) | X -208..-168 | 18 mm open gap |

**Fix:** top nozzle pipe moved to U 678..835 (embedded ~22 mm at the dome
peak and ~4 mm below the dome at its rim radius, so no rim gap remains);
discharge pipe extended to X -208..-150 so its end face meets the volute
left face flush.

**Rule that the fix demonstrates:** a flat-ended nozzle plugged into a curved
shell must be embedded below the shell surface at its own rim radius;
touching only the peak leaves a visible rim gap.

---

## Verification

- File: 46,613 -> 46,455 lines; 1,104 geometry elements
  (781 extrusions / 315 cylinders / 8 boxes).
- Structural parse balanced; global envelope unchanged
  (X -278..1770, Y -360..360, U 0..862 mm).
- Final file SHA-256 `04FE9886BB6BF5B5AB6C8CB07E074D51F7601141FB9C4FE0DB943EEC171AC5DC`
  (archived as `candidate/03_high_fidelity_pump_v3_physics_fixed_20260805.pml`).
- cad-agent `scripts/verify.ps1` passed (0 errors).
- User verdict: "basically OK" — accepted as a modeling pressure test, not a
  production standard.

---

## Candidate lessons (not promoted)

These are candidate-only lessons from one stress test. Promotion to
`skill/` requires reproduction on another task, human review and regression
(equivalent of cad-agent ADR-0002).

1. **Fastener seating:** a nut's bottom face must equal the bearing face top;
   a nut at the stud tip floats even though it is threaded on.
2. **Guaranteed box display:** when a part must read as a rectangular box,
   use the `BOX` primitive; do not rely on a rounded-rectangle extrusion.
3. **Connection continuity:** before finishing an equipment assembly, check
   body-to-nozzle contact numerically (gap = 0 or intentional embed); a
   flat-ended cylinder on a curved shell must be embedded below the shell
   surface at its rim radius.
4. **Primitive intent:** circle -> CYLINDER, box -> BOX, complex constant
   section -> EXTRUSION; the simplest true form renders and maintains best.

## Artifacts

- `source/2026-08-05_pump_edit_user_native.txt` — immutable user baseline.
- `candidate/03_high_fidelity_pump_v3_physics_fixed_20260805.pml` — accepted
  working file.
- `tools/pml_analyze.py` — structural/numeric PML analyzer used for evidence.
- `tools/fix_pump_edit.py` — the differential fix script (nuts, boxes,
  nozzle extensions).
- `tools/sig_ours.txt`, `tools/sig_theirs.txt` — element-signature diffs.
