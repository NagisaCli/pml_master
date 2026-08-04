# Workflow: A Modeling Run

The standard procedure for turning a modeling request into a macro that loads in
E3D on the first attempt. Follow the phases in order; the ordering exists because
each phase catches a class of error that is expensive to find later.

---

## Phase 0 — Load context

Read, in this order:

1. [SKILL.md](../../SKILL.md) — the precedence rules and the evolution loop
2. [skill/knowledge/iron-rules.md](../knowledge/iron-rules.md) — every time, no exceptions
3. [project-structure.md](project-structure.md) — **identify the project folder**,
   then read its `DO.txt`. That file is the standing statement of what this
   project requires and outranks any default you would otherwise assume.
4. [skill/projects/](../projects/README.md) — **has this equipment been modelled before?**

```bash
python -m wsb --list-projects
```

Step 4 is the one most often skipped and the most valuable. If a similar tank
exists in a project log, you inherit its resolved parameters, its user
corrections, and its mistakes-already-made. Start there rather than from scratch.

### Phase 0a — Detect a native/manual continuation

Before treating an incoming PML as generator output, determine why it was
supplied:

- a teaching specimen for learning new E3D syntax → follow
  [learning-from-native-exports.md](learning-from-native-exports.md);
- a model exported after manual work, to be continued → follow
  [reconciling-native-exports.md](reconciling-native-exports.md);
- both → reconcile/preserve first, then study an evidence copy.

Stable hierarchy and names do **not** mean unchanged geometry: designers
commonly change attributes on an existing element or add a child beneath an
existing SUBE.

If it is a native/manual continuation, stop the ordinary regenerate-first path
and follow
[reconciling-native-exports.md](reconciling-native-exports.md). The supplied
file becomes the working geometry baseline. The previous accepted macro remains
the comparison baseline; neither may be overwritten.

---

## Phase 1 — Establish the data, and its provenance

Collect for each item: tag, name, diameter, height, volume, elevation,
installation coordinate, roof type, bottom type, support type, nozzle schedule.

Apply the precedence ladder from `SKILL.md`. **Record where every number came
from as you go** — reconstructing provenance afterwards is unreliable, and the
deliverable depends on it.

| Provenance | Meaning |
|------------|---------|
| `EXCEL` | Read from the equipment list. Contractual data. |
| `SIDE_VIEW` / `TOP_VIEW` | Read from a project reference drawing. |
| `RECOVERED` | Recovered from a corrupted source cell. |
| `DERIVED` | Computed from project data. |
| `STANDARD` | Reference Value — standard practice. |
| `VENDOR_TYPICAL` | Reference Value — Valmet / ANDRITZ / Voith practice. |

The last three are assumptions and must be listed individually in the deliverable
so they can be replaced when official design data is issued.

### Cross-check the source data before trusting it

Source data is frequently defective. Check, at minimum:

- **Volume reconciliation.** Does π/4 · D² · H match the stated volume? A
  mismatch of an order of magnitude usually means height and diameter are
  transposed.
- **Coordinate plausibility.** Do the coordinates place equipment inside the
  plant, on sane elevations, without collisions?
- **Formatting corruption.** Numeric cells can lose their separators, turning
  `(15000, 19860, 300)` into `-1500019860300`. Re-derive from the raw file rather
  than the rendered value.
- **Filename/content mismatch** on drawings.

Correct defects **in the data layer, never by editing the source workbook**, and
report each one as a data-quality exception. The user needs to know their source
data is wrong; silently fixing it hides a problem that will recur.

---

## Phase 2 — Resolve the configuration

Determine roof, bottom, support and nozzle arrangement from the reference
drawings first, then from [skill/equipment/](../equipment/README.md).

Sanity-check the process logic — this is the most common *engineering* error, as
opposed to syntax error:

- **Upflow** (reactor, bleaching tower): fed at the bottom cone, discharges at
  the top.
- **Downflow / storage**: fed high on the shell, drawn from the bottom.

Nozzle elevations must follow the flow direction. A vent belongs at the high
point, a drain at the low point.

---

## Phase 3 — Generate

For a new/generated model, use the procedure below. For a user-edited native
export, apply only the reconciled delta described in Phase 0a; do not rebuild the
file from project data until its manual changes have been identified and
preserved.

Build geometry in a **local frame whose origin is the equipment bottom centre**,
then translate by the installation coordinate (IR-6). Never compute absolute
coordinates per primitive.

Convert CYLI/CONE bottom-face points to E3D centre datums in **one** helper;
pass DISH rim/tangent-plane points through unchanged (IR-1).

Emit through a builder that enforces ORI-before-POS structurally, rather than
relying on review (IR-2). `wsb/pml_builder.py` is the reference implementation.

---

## Phase 4 — Verify numerically

**A textual check is not verification.** Searching the macro for a coordinate
proves only that *some* primitive sits there; it passes a model in which every
element has the wrong datum.

Parse the emitted primitives, compute each one's true extent from its
element-specific datum and dimensions, then assert:

- [ ] Lowest point of the equipment = the listed installation elevation
- [ ] Bottom centre E/N = the listed installation coordinate
- [ ] Nothing modelled below the foundation bearing plane
- [ ] No primitive with zero or negative dimensions
- [ ] Shell, heads and support meet without gaps or telescoping

Then run the [Iron Rules checklist](../knowledge/iron-rules.md#pre-delivery-checklist).

This is automated:

```bash
python -m wsb --project <Name> --dry-run
```

It exits non-zero if any tank fails.

---

## Phase 5 — Deliver

Report per equipment item:

- **Completed**: tag, name
- **Modeling parameters**: diameter, overall height, head type, skirt dimensions,
  nozzle count
- **Reference Values**: every assumed value with its basis ("based on a similar
  Valmet design", "standard pulp mill practice"). Never bury these.
- **Outstanding issues**: what still needs confirmation — unknown overall height,
  unavailable nozzle sizes, unidentifiable top structure

Deliverables land in `Projects/<Name>/output/` and are **named after the
project**, so the macro can be traced back and reopened in a later session.

State the load instruction: select a writable ZONE, then `$M <path>`.

---

## Phase 6 — Write back (mandatory)

The run is not finished when the macro is delivered. It is finished when the
skill is larger than it was.

- Update `Projects/<name>/DO.txt` if any new requirement arrived during the job.
  A requirement that lives only in a chat message is lost at the end of the
  session.
- Update or create `skill/projects/<project>.md` — what was modelled, what was
  assumed, what remains open.
- If the user supplied a native export, record its archive path, comparison
  baseline and preservation set so the next session does not overwrite manual
  edits.
- If E3D rejected anything → [diagnosing-failures.md](diagnosing-failures.md),
  then promote the lesson if it generalises.
- If the user corrected anything → [capturing-feedback.md](capturing-feedback.md).
- If a syntax form was proven → promote it to VERIFIED in
  [pml1-reference.md](../knowledge/pml1-reference.md).

If nothing was learned, write one line saying so. An explicit "no new lessons" is
information; silence is indistinguishable from having skipped the step.

---

## Anti-patterns

| Don't | Do |
|-------|-----|
| Compute absolute coordinates per primitive | Local frame + single translation |
| Convert the datum at each call site | One central helper |
| Verify by grepping for `POS` | Parse geometry and compute extents |
| Invent detail to enrich the model | Model what is justified; flag the rest |
| Silently "fix" a user's parameter | Model as given; raise the concern separately |
| Fix a bug only in the output | Fix it in `skill/` so it never recurs |
| Read the whole skill directory | Read entry + iron rules + what the task needs |
