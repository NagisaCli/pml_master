# Workflow: Diagnosing an E3D Failure

Every E3D error is an opportunity for the skill to improve. This file is both the
diagnostic procedure and the register of failures already solved — **check the
register first**, because the answer is often already here.

---

## Two classes of failure

**Loud** — E3D reports a syntax error and aborts the macro. Annoying, but
self-announcing.

**Silent** — the macro loads cleanly and the geometry is wrong. Far more
dangerous, because it reaches the deliverable. Every silent failure below was
caught by numerical verification, not by reading the macro.

---

## Loud failures: reading the error

```
(47,15)   CP: Syntax error
Command: ^^SUSPEND
```

The reported line number is accurate. But **a prologue fault always sits at the
first executable line, so the number does not move when you change what that line
says.** If the error stays on the same line across edits, that line is the
problem — do not assume your edit was ineffective.

Before substituting another command, verify the command exists at all:

```bash
grep -ric "^\s*COMMANDNAME\b" "$AVEVA_DESIGN_EXE/pmllib"
```

Zero line-start hits in AVEVA's own library means the command is invented. This
check is the single most useful diagnostic in this file: it distinguishes "wrong
syntax" from "this command does not exist", which are fixed differently.

### Procedure

1. Note the line number and the echoed command.
2. Check it against the banned list in [pml1-reference.md](../knowledge/pml1-reference.md).
3. Run the `grep` above to confirm the command exists.
4. Fix the generator, not the output file — regenerating from a patched artifact
   loses the fix.
5. Regenerate, reload, and record the result below.

---

## Silent failures: recognising them by symptom

| Symptom | Almost certainly | Rule |
|---------|------------------|------|
| Elements telescoped into one another; "overlapping clutter" | `POS` treated as bottom-face instead of centre | [IR-1](../knowledge/iron-rules.md#ir-1--pos-is-the-geometric-centre-of-every-primitive) |
| Whole item offset by a constant amount | Owning `EQUI` not anchored at `POS E 0 N 0 U 0` | [IR-7](../knowledge/iron-rules.md#ir-7--anchor-every-equi-at-its-owner-origin) |
| One element drifted, no error | `POS` emitted before `ORI` | [IR-2](../knowledge/iron-rules.md#ir-2--ori-before-pos) |
| Vessel lying on its side | Axis put on Y instead of Z | [IR-3](../knowledge/iron-rules.md#ir-3--z-is-the-axis-of-revolution) |
| Geometry moved after a "cosmetic" tree change | Hierarchy change altered the owner | [IR-7](../knowledge/iron-rules.md#ir-7--anchor-every-equi-at-its-owner-origin) |
| Huge hemispherical bulge on a flat top | `DISH` used as a cover plate | [IR-9](../knowledge/iron-rules.md#ir-9--dish-and-cone-are-closures-not-shaping-surfaces) |
| Half the vessel underground | Datum conversion missing at one call site | [IR-1](../knowledge/iron-rules.md#ir-1--pos-is-the-geometric-centre-of-every-primitive) |

The "overlapping clutter" symptom deserves emphasis: because each element shifts
by half of *its own* height, the failure does not look like an offset. It looks
like the model was built badly. Recognising it as a datum error saves hours.

---

## Register of solved failures

| # | Symptom | Cause | Resolution | Status |
|---|---------|-------|------------|--------|
| F-1 | `(47,15) CP: Syntax error / ^^SUSPEND` | `SUSPEND`/`RESUME`/`VAR 0`/`ALPHA HEADER` prescribed as an anti-freeze prologue; not E3D commands | Prologue removed; all four banned in `validate_pml()` | Fixed — IR-4 |
| F-2 | Shells, skirts, heads and nozzles telescoped together | Knowledge base claimed a bottom-face datum for `CYLI`/`CONE`/`DISH` | Datum corrected to geometric centre; conversion centralised in `PMLBuilder._position` | Fixed — IR-1 |
| F-3 | Transverse elements drifting from intended positions | `POS` emitted before `ORI`, rotating the position vector | Builder emits `ORI` first structurally; `validate_pml()` re-checks | Fixed — IR-2 |
| F-4 | Vessels rendering on their side | Axis assumed to be Y | Verified against `gphFactory.pmlobj:632` that Z is the axis | Fixed — IR-3 |
| F-5 | Verification passed on a model with wrong datums | Verification string-matched the `POS` line | Replaced with geometric parse in `verify_bottom_centre` | Fixed — IR-6 |
| F-6 | Macro loads but creates nothing | Current element was not a writable ZONE | Select a writable zone before `$$MACRO` | Documented |

---

## Recording a new failure

Add a row above, then decide where the lesson belongs:

- **Generalises to all E3D work** → new or amended Iron Rule. Include the symptom
  and the evidence, not just the fix; the symptom is what a future reader
  recognises.
- **Syntax-specific** → [pml1-reference.md](../knowledge/pml1-reference.md),
  including demoting anything contradicted.
- **Project-specific quirk** → that project's log.

Also state how the failure would be *caught automatically* next time. A lesson
that relies on remembering to look is weaker than one enforced by the builder or
a test. F-2, F-3 and F-5 are all now enforced in code, which is why they have not
recurred.

---

## When a knowledge base entry is proven wrong

Correct it immediately and note the correction, as with IR-1 and IR-4 above. Both
of those rules exist because a *previous version of this knowledge base* was
confidently wrong, and the error propagated into generated models.

Leaving a superseded claim in place is worse than having no entry: a future
reader cannot tell which of two contradicting statements to trust, and will
sometimes pick the wrong one.
