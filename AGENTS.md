# AGENTS.md

**Start here: [SKILL.md](SKILL.md).**

This project is a *skill*, not an application — a directory of knowledge that any
AI model reads before generating AVEVA E3D PML macros for pulp & paper equipment.
You are the runtime.

---

## Required reading, in order

1. **[SKILL.md](SKILL.md)** — entry point: data precedence, evidence standard,
   and the evolution loop
2. **[skill/knowledge/iron-rules.md](skill/knowledge/iron-rules.md)** — every
   time, no exceptions. Ten rules, each paid for by a real failure.
3. **[skill/workflows/modeling-run.md](skill/workflows/modeling-run.md)** — the
   procedure for an actual job

Then retrieve on demand:

| Need | File |
|------|------|
| PML1 syntax | [skill/knowledge/pml1-reference.md](skill/knowledge/pml1-reference.md) |
| What equipment looks like | [skill/equipment/](skill/equipment/README.md) |
| Prior work | [skill/projects/](skill/projects/README.md) |
| An E3D error | [skill/workflows/diagnosing-failures.md](skill/workflows/diagnosing-failures.md) |
| A user correction | [skill/workflows/capturing-feedback.md](skill/workflows/capturing-feedback.md) |

Do not read the whole directory. That wastes the context you need for the model.

---

## The five things that will break your macro

1. **`POS` is the geometric CENTRE** of every primitive — `CYLI`, `CONE`, `DISH`,
   `BOX` alike. There is no bottom-face datum in E3D.
2. **`ORI` before `POS`.** The reverse order drifts the element silently, with no
   error message.
3. **PML1 only.** No `!var =`, `COLLECT`, `UNSET`, `ENDS`, `END EQUI`, `!!Alert`.
4. **No render prologue.** `SUSPEND`, `RESUME`, `VAR 0`, `ALPHA HEADER` are not
   E3D commands and abort the macro.
5. **User parameters always win** over anything in this knowledge base.

Full detail and the evidence behind each is in the Iron Rules.

---

## Non-negotiable

- **Verify geometry numerically**, never by string-matching a `POS` line. A
  textual check passes a model in which every element has the wrong datum.
- **Label every assumed value** as a Reference Value with its basis.
- **Write back what you learn** — see the evolution loop in SKILL.md. A fix that
  lives only in generated output will be paid for again on the next project.

---

## This file deliberately contains no rules of its own

Everything above is a pointer. The previous version of this file duplicated the
full rule set, and the copy in `pml_knowledge/corpus/` drifted out of step with
it — still teaching a bottom-face datum and a `SUSPEND`/`RESUME` prologue long
after both were disproved. Any model built from the stale copy reproduced
failures that had already been fixed.

There is now one source of truth: `skill/`. It is read by humans, by LLMs, and by
`pml_knowledge/knowledge_base.py` alike. Add knowledge there, not here.

`tests/test_skill_integrity.py` enforces this: it fails if a superseded claim
reappears, if a documented figure drifts from what the generator produces, or if
a cross-reference breaks.
