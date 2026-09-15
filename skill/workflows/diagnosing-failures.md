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
| CYLI/CONE elements telescoped into one another; "overlapping clutter" | `POS` treated as bottom-face instead of centre | [IR-1](../knowledge/iron-rules.md#ir-1--pos-is-element-specific-centre-for-cyliconebox-rim-for-dish) |
| **Dished head floats above the shell by exactly half its HEIG** | CYLI/CONE centre conversion incorrectly applied to `DISH`; its POS is the rim plane | [IR-1](../knowledge/iron-rules.md#ir-1--pos-is-element-specific-centre-for-cyliconebox-rim-for-dish) |
| Whole item offset by a constant amount | Owning `EQUI` not anchored at `POS E 0 N 0 U 0` | [IR-7](../knowledge/iron-rules.md#ir-7--anchor-every-equi-at-its-owner-origin) |
| One element drifted, no error | `POS` emitted before `ORI` | [IR-2](../knowledge/iron-rules.md#ir-2--ori-before-pos) |
| Vessel lying on its side | Axis put on Y instead of Z | [IR-3](../knowledge/iron-rules.md#ir-3--z-is-the-axis-of-revolution) |
| Geometry moved after a "cosmetic" tree change | Hierarchy change altered the owner | [IR-7](../knowledge/iron-rules.md#ir-7--anchor-every-equi-at-its-owner-origin) |
| Huge hemispherical bulge on a flat top | `DISH` used as a cover plate | [IR-9](../knowledge/iron-rules.md#ir-9--dish-and-cone-are-closures-not-shaping-surfaces) |
| Half a CYLI/CONE underground | Datum conversion missing at one call site | [IR-1](../knowledge/iron-rules.md#ir-1--pos-is-element-specific-centre-for-cyliconebox-rim-for-dish) |
| **Nozzles absent from the 3D view but present in the tree** | No catalogue component bound — the element is empty | [IR-9a](../knowledge/iron-rules.md#ir-9a--a-nozzle-draws-nothing-until-a-catalogue-component-is-bound) |
| **Only the flange rim shows; barrel invisible** | `POS` treated as the nozzle root, not the flange face | [IR-9a](../knowledge/iron-rules.md#a-nozzles-pos-is-its-flange-face-not-its-root-on-the-shell) |
| **Nozzles aimed off the shell, or rolled oddly** | Oriented on a geometric axis instead of `ORI P1 IS` | [IR-2](../knowledge/iron-rules.md#a-nozzle-is-aimed-by-its-p-point-not-by-a-geometric-axis) |
| **Only the first equipment item loaded** | Macro aborted mid-load — read the error file, not the model | F-8 below |
| **Nozzles as metre-long tubes flying off the vessels** | `HEIG` given a value that is not the nozzle's own length | [IR-9a](../knowledge/iron-rules.md#heig-is-the-nozzles-own-length--bound-it-dont-theorise-about-it) |
| Row of floating discs beside each item | A ring modelled as one solid `CYLI` | [IR-9b](../knowledge/iron-rules.md#ir-9b--cyli-is-solid-there-is-no-annulus-primitive) |

**A partial model is a failure, not a rendering quirk.** If some equipment is
missing entirely, the macro aborted partway: find the E3D alert file
(`SIR-*.txt` on the Desktop) and read the line number. Nothing about the loaded
geometry will tell you this — the model just looks incomplete.

The "overlapping clutter" symptom deserves emphasis: because each element shifts
by half of *its own* height, the failure does not look like an offset. It looks
like the model was built badly. Recognising it as a datum error saves hours.

---

## Register of solved failures

| # | Symptom | Cause | Resolution | Status |
|---|---------|-------|------------|--------|
| F-1 | `(47,15) CP: Syntax error / ^^SUSPEND` | `SUSPEND`/`RESUME`/`VAR 0`/`ALPHA HEADER` prescribed as an anti-freeze prologue; not E3D commands | Prologue removed; all four banned in `validate_pml()` | Fixed — IR-4 |
| F-2 | Shells, skirts and primitive nozzle parts telescoped together | Knowledge base claimed a bottom-face datum for `CYLI`/`CONE` | Their datum corrected to geometric centre; conversion centralised in `PMLBuilder._position` | Fixed — IR-1 |
| F-3 | Transverse elements drifting from intended positions | `POS` emitted before `ORI`, rotating the position vector | Builder emits `ORI` first structurally; `validate_pml()` re-checks | Fixed — IR-2 |
| F-4 | Vessels rendering on their side | Axis assumed to be Y | Verified against `gphFactory.pmlobj:632` that Z is the axis | Fixed — IR-3 |
| F-5 | Verification passed on a model with wrong datums | Verification string-matched the `POS` line | Replaced with geometric parse in `verify_bottom_centre` | Fixed — IR-6 |
| F-6 | Macro loads but creates nothing | Current element was not a writable ZONE | Select a writable zone before `$M` | Documented |
| F-7 | `(47,50) CP: Meaningless symbol(s)` on the load command | `$$MACRO` is not an E3D command — 0 hits in ~6900 library files. It was in the deliverable's own header, so the shipped instruction could never work | Corrected to `$M <path>` everywhere | Fixed — [pml1-reference](../knowledge/pml1-reference.md#loading-a-macro--verified) |
| F-8 | All 114 nozzles present in the tree, invisible in 3D | No catalogue component bound. A prior fix had *removed* the reference after it failed to resolve, leaving every element empty | `CATR SPCOMPONENT` emitted live, inline, per nozzle | Fixed — IR-9a |
| F-9 | `(2,360) Cannot get position of NOZZLE`; only the first tank loaded | Binding emitted as a trailing `OLD`/`CATR` pass, copying a *rebinding* idiom. P-points do not exist until a component is bound | `CATR` moved inline, before `POS`/`ORI`; enforced by `_check_nozzle_catref_first()` | Fixed — IR-9a |
| F-10 | `(2,108) SCOMPONENT /AAZFBB0YY is not a SPCO` | Passed the SPCO's `Catref` *value* instead of the SPCO's own two-segment path. `Q ATT` prints both, one line apart | Path built by `nozzle_component_path()` | Fixed — [catalogue-elements](../knowledge/catalogue-elements.md) |
| F-11 | Nozzles buried in the shell; only the flange rim visible | `POS` treated as the root on the shell. It is the **flange face**; the barrel runs back from it into the vessel | `POS = face − penetration + length`; test checks the barrel's two ends | Fixed — IR-9a |
| F-12 | Nozzles drawn as metre-long tubes flying off the vessels | `HEIG` computed from the EQUI origin on a mis-read datum; emitted −61680..+72280 mm for 250–450 mm nozzles | Reverted to the nozzle's own length; bounds check 1–2000 mm in `validate_pml()` | Fixed — IR-9a, IR-11 |
| F-13 | `ACCUMULATOR_TANK` top head floating above the shell by 877.9 mm | F-2 was over-generalised: DISH was wrongly assigned the CYLI/CONE centre conversion, but its `POS` is the rim/tangent plane | DISH now passes its rim point through unchanged; parsers use the same element-specific datum; regression checks shell top = head rim | Fixed in generator; awaiting user reload — IR-1 |
| F-14 | Piping component renders but connecting legs are green dashed lines instead of solid tube | BRANCH route is geometrically incorrect/ill-defined; first reproduced when an ELBOW copied from native export lost its `ARRI 2 / LEAV 1`, so its logical-route P-points no longer matched the branch legs | Preserve component-specific `ARRI/LEAV`; verify ADIR/LDIR and adjacent alignment, not just POS/ORI | Candidate 06 user-confirmed: solid continuous route after restoring `ARRI 2 / LEAV 1` — [piping-reference](../knowledge/piping-reference.md) |
| F-15 | REDUCER appears North/South inside a vertical BRANCH | Applied the primitive Z-axis rule to a catalogue piping component; its route axis comes from catalogue P-points/local axes | Use a native-proven component basis or direct P-point orientation; native vertical reducers use `ORI Y is N and Z is E` | Candidate 07 user-confirmed: vertical, solid and coaxial with `ORI Y is N and Z is E` — [piping-reference](../knowledge/piping-reference.md) |
| F-16 | E3D exits fatally on import/create or delete, while read-only browsing works; SIR says `Failed to start Collections Addin` followed by `MyDataCollectionSystem` `NullReferenceException` | Collections/My Data add-in fails while rebuilding shared collections, but its event handlers remain active; DrawList changes and database `PostClaim/ClaimRelease` then enter an incompletely initialised collection handler | Treat as an application/add-in failure, not a PML verdict; test with a copied `DesignAddins.xml` selected through `CAF_ADDINS_PATH` and only `MyDataAddin` removed; never edit the installation copy | Confirmed independently by candidate-08 import and ordinary Delete command SIRs |
| F-17 | Candidate 11 stops at `(2,109) Undefined name /FIRE`; loaded component rows also appear as green dashed/fake lines | Native catalogue paths and specification names were copied from another project without proving they exist in the receiving MDB; generic components were emitted without actual nozzle/branch P-point and reciprocal connection logic | Quarantine the stress macro; resolve every `PSPE/SPRE/LSTU/HSTU` path in the receiving project first, then generate routes from verified nozzle `HREF/TREF` and component `ARRI/LEAV/CREF` relationships. Never treat a catalogue block or free line as a connection | SIR `SIR-20260731-012752-undefined-fire.txt`; screenshots show repeated unconnected dashed routes |
| F-18 | `(41,8) Cannot create a EQUI at this level.` at `NEW EQUIPMENT /203_PU_026`, line 7121 of the r2 pump macro; only the first four pumps load | In a native INPUT data listing every `SUBEQUIPMENT` and `EQUIPMENT` block has its own trailing `END`. Deleting the five `MC_AUXILIARY` subequipment blocks removed their headers and primitives but left each subequipment's closing `END` behind; the stray `END` closed the EQUIPMENT and then the ZONE, so the next EQUI could not be created at that level | Delete the subequipment's closing `END` together with its block; the verify script now replays the INPUT block stack (EQUI only inside ZONE, SUBE only inside EQUI, primitives only inside SUBE/primitive, no residual stack) and would fail the r2 before delivery | Fixed in `refine_bridge_brackets.py`; r2 regenerated and hierarchy-balanced; SIR archived at `Projects/JK_Pump_Build/imports/2026-08-05_SIR_Cannot_create_EQUI.txt` |
| F-19 | NCYLINDER loads without error but cuts no hole; user's own primitive+negative test does cut | Negative primitive emitted without its negative-application flag. AVEVA's own hole code always sets `nappflag = 2` after creating the negative (`hmcontrol.pmlobj` `.createHoleNegativeExtrusion`) and defaults `NAPPFLAG -1` to 2 (`strSctnGensec.pmlobj` `.tmplRestore`) | Emit `NAPPFLAG 2` on every NCYLINDER/NBOX; verify script asserts each negative carries the flag | r3 regenerated (30/30 flagged); placement semantics under test in `PML-STUDY-NCYL-001` |
| F-20 | Negative child with world-coordinate POS loads (Explorer tree) but cuts nothing; standalone negative at SUBE level aborts `(41,8) Cannot create a NCYL at this level` | A negative child's POS is **local to its owner**, not world; a standalone negative is not creatable at SUBE/EQUI level | Emit child negatives with owner-relative POS (owner centre + offset), honouring the child's ORI; verifier adds owner centre to NCYLI POS before geometry checks | **Fixed — r4** (30/30 local offsets match removed stubs); PML-STUDY-NCYL-001 user-verified C2/C3 forms; NCYLI entry promoted to VERIFIED in pml1-reference |
| F-21 | `(41,8) Cannot create a STRU at this level.` on `NEW STRUCTURE` inserted into a native data listing | A native listing can close its ZONE (`END`) **before** the trailing `OLD`/`CATR` binding pass; inserting a new element after the ZONE END puts it outside the ZONE (at the input root), where STRUCTURE/EQUI cannot be created | Locate the owner's closing `END` with a NEW/END stack walk and insert **before** it; verify the stack empties exactly once, at the owner's END | r2 regenerated (STRUCTURE inside `/WSB_TA`); SIR archived at `Projects/JK-Tank_Build/imports/2026-08-10_SIR_Cannot_create_STRU.txt` |
| F-22 | Handrail macro loads cleanly but renders nothing; user: "没有形成楼梯，放置的位置也不对；应是圆盘底座" (no handrail formed, wrong position, needs circular disc bases) | HANDRA block shipped with an RPATH of `CURTYP THRU` curves, a RAILSET, and **no POSTSE/HRPOST posts** — a structural-template form never verified in E3D; without posts (and with an unproven path form) there is nothing visible to place | Fall back to verified primitives: post base plates + CYLI posts + tangent CYLI rail segments, inserted under the tank's EQUIPMENT. Follow-up correction: the ring goes on the shell-cylinder top rim (big circle), not the frustum top (small circle) | **RESOLVED — r4 accepted 2026-08-10** ("可以，干的漂亮"): `Projects/JK-Tank_Build/output/WSB_TA_top_handrails_20260810_r4.txt` |
| F-23 | `(47,15) CP: Syntax error In line 44 of Macro .../runsynonym.pmlmac ^^CALLG MSAVEW` on Delete, Save Work, or GUI action after a failed macro load | A macro with `$S-` (Synonym translation OFF) encountered an error and aborted before reaching `$S+` at the end; E3D's global session remains in the `$S-` state, so internal GUI callbacks like `!!runSynonym('CALLG MSAVEW')` cannot expand synonyms and fail as invalid syntax | Type `$S+` directly in the E3D Command Window and press Enter to restore synonym translation; never wrap interactive PML snippets with `$S-` | Confirmed 2026-08-24 in E3D Design; entering `$S+` immediately restores GUI operation |
| F-24 | Negative extrusion (`NXTRUSION`) inside an already-rotated parent (`CONE` with `ORI Y is U and Z is N`) rotates by 90°, sweeps in reverse, or flies 52 m away (`Position WRT Owner E 52600mm`) when `WRT /*` is written | A negative primitive's `POS` and `ORI` are evaluated strictly within the parent's local reference frame; writing `WRT /*` on a child negative causes E3D to compound hierarchy offsets, placing the cut tens of metres away. Furthermore, child `ORI` compounds with the parent's rotation ($R_{\text{world}} = R_{\text{parent}} \cdot R_{\text{local}}$) | Never emit `WRT /*` on child negatives; compute child `ORI` in parent local frame via $R_{\text{local}} = R_{\text{parent}}^T \cdot R_{\text{world}}$ (for parent `Y is U, Z is N`, child `ORI Y IS N AND Z IS W` yields world $Y=U, Z=E, X=N$) and start face `POS E <offset> N 0 U 0`; use 16-vertex rounded LOOP ($R=10\text{ mm}$) for cast bracket windows | **RESOLVED 2026-09-04** (user verified "这一版很完美") |

**F-25 — unsupported FRMWORK orientation (Typical_Pipe_Support R1).**
The user reported `(2,201)` on `ORI Y IS N AND Z IS U` immediately after
`NEW FRMW /TPS_R1_FRAME`. A generic pose header had been copied onto a framework.
Remove that header from the generator, preserve the member geometry, and reject
framework `ORI` in the shared validator. **Do not infer retained database state
from this error line.** The subsequent continuation failed with the framework
undefined. Before a continuation, verify that its owner currently exists and
its target members do not; otherwise use a complete fresh namespace as R2 does.
Evidence:
[user report](../../Projects/Typical_Pipe_Support/results/evidence/2026-09-13_FRMW_ORI_user_report.txt).
The [subsequent missing-frame error](../../Projects/Typical_Pipe_Support/results/evidence/2026-09-13_R1_FRAME_undefined_user_report.txt)
supersedes the earlier continuation recommendation. R2 passes static checks;
E3D retry pending.

### What F-8 through F-12 have in common

They are **one bug reported five times**. Each fix was correct as far as it went
and revealed the next layer:

```
bind nothing        -> invisible
bind late           -> abort mid-load
bind wrong path     -> (2,108)
aim wrong axis      -> pointing off the shell
place wrong datum   -> buried in the shell
```

A catalogue element has more independent ways to be wrong than a primitive, and
**four of the five produced no error message**. When a catalogue element
misbehaves, expect to work through the whole list in
[catalogue-elements.md](../knowledge/catalogue-elements.md) rather than assuming
the first fix is the last.

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
