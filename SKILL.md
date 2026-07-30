# E3D Modeling Skill — Pulp & Paper Equipment

**You are reading the entry point. Read this file completely before generating any PML.**

This directory is a *skill*, not an application. It carries the accumulated
experience of generating AVEVA E3D PML1 macros for pulp & paper equipment. Every
rule here was paid for by a real failure in E3D Design Mk3.1.11.0.

There is no API and no daemon. You — whichever AI model is reading this — are the
runtime. Your job is to read the relevant files, generate a macro that loads in
E3D on the first attempt, and then **write back what you learned**.

---

## The 60-second orientation

| Question | File |
|----------|------|
| What must I never get wrong? | **[Iron Rules](skill/knowledge/iron-rules.md)** — read every time, no exceptions |
| Which project am I working on? | **[skill/workflows/project-structure.md](skill/workflows/project-structure.md)** — start here on any real job |
| How do I run a modeling job? | [skill/workflows/modeling-run.md](skill/workflows/modeling-run.md) |
| What PML syntax is safe? | [skill/knowledge/pml1-reference.md](skill/knowledge/pml1-reference.md) |
| I am modelling a NOZZLE | **[skill/knowledge/catalogue-elements.md](skill/knowledge/catalogue-elements.md)** — required; a nozzle fails in ways a primitive cannot |
| What does this equipment look like? | [skill/equipment/](skill/equipment/README.md) |
| Has this been done before? | [skill/projects/](skill/projects/README.md) |
| E3D rejected my macro | [skill/workflows/diagnosing-failures.md](skill/workflows/diagnosing-failures.md) |
| The model looks wrong but loaded fine | [skill/workflows/diagnosing-failures.md](skill/workflows/diagnosing-failures.md) — the symptom table |
| I need a fact from the user's E3D session | [skill/workflows/querying-e3d.md](skill/workflows/querying-e3d.md) |
| The user corrected me | [skill/workflows/capturing-feedback.md](skill/workflows/capturing-feedback.md) |
| The user supplied a manually edited native E3D export | **[skill/workflows/reconciling-native-exports.md](skill/workflows/reconciling-native-exports.md)** |

**Minimum viable read** for a modeling task: this file → `iron-rules.md` →
`project-structure.md` → the project's own `DO.txt` → `modeling-run.md`.
Everything else is retrieved on demand. Do not read the whole directory; that
wastes the context you need for the model itself.

If the input is a manually edited/native-exported PML file, also read
`reconciling-native-exports.md` before inspecting or changing that file.

---

## The seven rules that survive everything

These are compressed from `skill/knowledge/iron-rules.md`. If you read nothing
else, read these — but read the full file before emitting geometry.

1. **`POS` is element-specific.** `CYLI`, `CONE` and `BOX` use geometric centre;
   `DISH` uses its flat rim / tangent plane. Never apply a half-height centre
   conversion to a DISH.
2. **`ORI` before `POS`**, always. The reverse order rotates the position vector
   and the element drifts silently, with no error.
3. **PML1 only.** No `!var =`, `COLLECT`, `UNSET`, `ENDS`, `END EQUI`, `!!Alert`.
4. **No render prologue.** `SUSPEND`, `RESUME`, `VAR 0`, `ALPHA HEADER` are not
   E3D commands and abort the macro. Load with `$M <path>`, never `$$MACRO`.
5. **A `NOZZLE` is a catalogue element, and nothing about it works like a
   primitive.** Bind `CATR` first or it draws nothing; aim it with `ORI P1 IS`;
   its `POS` is the flange face. See
   [catalogue-elements.md](skill/knowledge/catalogue-elements.md).
6. **Bounds-check physical quantities before trusting any datum reasoning.**
   Lengths are positive; nozzles are under a metre; nothing sits below its
   foundation. A theory-shaped check confirms the theory, not the model (IR-11).
7. **User-supplied parameters always win** over anything in this knowledge base.
8. **A user-edited native export is the current geometry baseline.** Identify
   its hierarchy and attribute deltas before changing it; preserve every
   out-of-scope manual edit.

---

## Data precedence — never invert this

When a parameter is needed, take the first source that has it:

```
1. User instruction in the conversation      ← absolute authority
2. The project's DO.txt                      ← the standing requirements
3. Project data (equipment list / Excel)     ← contractual
4. Project reference drawings                ← configuration and appearance
5. skill/equipment/ prototype knowledge      ← reasoned default
6. Authoritative external source             ← must be citable
7. STOP. Ask, or emit and flag as assumption.
```

Anything from sources 5–7 is a **Reference Value** and must be labelled as such
in the deliverable, with its basis stated. Never present an assumption as project
data. Never silently overwrite a number the user gave you — if you believe it is
wrong, model it as given and say so separately.

---

## The evolution loop — this is the point of the skill

The skill is worthless if it ends each job the same size it started. Every run
must close this loop:

```
   read  →  model  →  verify  →  user/E3D feedback  →  WRITE BACK  →  read …
```

**Write back after every job.** Concretely:

| What happened | Where it goes |
|---------------|---------------|
| A macro failed to load in E3D | `skill/knowledge/iron-rules.md` (if it generalises) + the project log |
| The user corrected geometry or appearance | `skill/equipment/<type>.md` |
| A new requirement arrived for this project | `Projects/<name>/DO.txt` — keep it current |
| A tank/unit was delivered | `skill/projects/<project>.md` |
| A syntax form was proven to work | `skill/knowledge/pml1-reference.md`, marked VERIFIED |
| A syntax form is untested | same file, marked EXPERIMENTAL — never promote without evidence |
| A workflow step was missing | `skill/workflows/` |
| A manually edited export was supplied | Archive it under the project, compare it with the accepted baseline, and record the preservation set |

A fix that lives only in generated output and not in `skill/` will be paid for
again on the next project. That is the failure mode this whole structure exists
to prevent.

---

## Evidence standard

This knowledge base is trusted, so it must stay clean. **It is strictly better to
record nothing than to record something unverified.**

Every claim in `skill/knowledge/` carries a status:

- **VERIFIED** — observed working in E3D, or traced to AVEVA's own PML library
  under `%AVEVA_DESIGN_EXE%\pmllib\`. Cite the file and line where possible.
- **RECOMMENDED** — sound engineering practice, consistently applied here.
- **EXPERIMENTAL** — plausible but unproven. Never rely on it silently; if you
  use it, tell the user it is unproven.

Promotion to VERIFIED requires evidence, not confidence. Downgrade or delete on
the first contradiction — a rule that is quietly wrong is more expensive than a
missing one.

For equipment numbers from outside sources: dimensions must be traceable to a
named manufacturer or standard. Vague recall is not a source. Record the source
next to the number or leave the number out.

---

## Working state

The `wsb/` Python package is the shared engine and the reference implementation
of everything above — the proof that these rules produce a loadable model, and
the place where the datum conversion is done once, centrally. Projects supply
data; the engine is common to all of them, so a fix here protects every project.

```bash
python -m wsb --list-projects
python -m wsb --project JK-Project --dry-run
```

Current verified state: **22 tanks, 451 primitives, 114 native NOZZLE elements**, all bottom
centre points verified numerically. See
[skill/projects/jk-project-wsb.md](skill/projects/jk-project-wsb.md).

Verify geometry numerically, never by string-matching a `POS` line — a textual
check passes a model in which every element has the wrong datum.

---

## Scope

Present focus is pulp & paper. The structure is industry-neutral: to add an
industry, add files under `skill/equipment/` and a project log. Do not fork the
Iron Rules — E3D's geometry semantics are the same everywhere.
