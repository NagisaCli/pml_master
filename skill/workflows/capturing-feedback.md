# Workflow: Capturing User Feedback

User corrections are the highest-value input this skill receives. They are the
only source that can tell you the *appearance* of real equipment is wrong — no
amount of syntax validation catches "that is not what a filtrate tank looks
like".

A correction that is applied to the current model but not written back into
`skill/` will be paid for again on the next project. Treat write-back as part of
the correction, not as follow-up work.

---

## Classify first

| Feedback | Goes to | Authority |
|----------|---------|-----------|
| "This tank should have a conical roof, not flat" | `skill/equipment/<type>.md` | **Overrides the knowledge base** |
| "The diameter is 5400, not 5000" | Project data + project log | **Overrides everything** |
| "Nozzles should be spread around the shell" | `skill/equipment/` or a workflow | Practice |
| "E3D rejected this command" | [diagnosing-failures.md](diagnosing-failures.md) | Verified fact |
| "Always report assumptions separately" | `skill/workflows/` | Process |
| "Don't model the ladder unless it's on the drawing" | Iron Rules if general, else equipment file | Practice |

---

## The precedence rule this enforces

**A user statement about their equipment outranks the knowledge base
permanently, not just for the current model.**

If the user says an oxygen reactor has a dished bottom and
`skill/equipment/tanks.md` says conical, the file is wrong — update it. Do not
apply the correction locally and leave the default to mislead the next run.

Where a correction may be project-specific rather than universal, record it in
the project log **and** note the variation in the equipment file, rather than
silently overwriting a default that is right elsewhere.

---

## Procedure

1. **Apply** the correction to the current model.
2. **Locate** the file that produced the wrong output. If a default made you get
   it wrong, that default is the bug — not the generated file.
3. **Amend** it, replacing the incorrect claim rather than appending a
   contradiction. Two contradicting statements are worse than one wrong one.
4. **Attribute** it: mark the entry as user-corrected with the date and project,
   so its authority is visible.
5. **Generalise, carefully.** One correction on one tank is a data point. Ask
   whether it reflects how this equipment class is always built, or just this
   item. When unsure, record it narrowly — over-generalising a correction creates
   a new wrong default.
6. **Check for contradictions** elsewhere in `skill/` and fix them in the same
   pass.

---

## Recording format

In the relevant `skill/equipment/` or `skill/knowledge/` file:

```markdown
> **User-corrected 2026-07-24 (JK-Project).** Filtrate tanks in this service have
> a conical roof, not a flat roof. Previously defaulted to flat.
```

Keep the previous claim visible in the correction line — knowing what it *used*
to say prevents someone from re-introducing the old default later.

---

## What not to write back

Restraint keeps this knowledge base trustworthy:

- **Conversational detail.** "The user asked for this on Tuesday" is not
  knowledge.
- **One-off project parameters.** These belong in the project log, not in the
  prototype knowledge base. A single tank's diameter is not a default.
- **Anything you inferred but the user did not confirm.** If you guessed and the
  user stayed silent, that is not validation.
- **Numbers without a source.** Better to record nothing than something
  unverifiable — see the evidence standard in [SKILL.md](../../SKILL.md).

---

## Reading feedback carefully

When the user says a model is wrong, distinguish:

- **Wrong data** — a number is incorrect → fix the data and the log.
- **Wrong interpretation** — the number was right but you applied it to the wrong
  part of the equipment (e.g. treating overall height as shell height, or
  diameter as radius) → this is a *parameter-mapping* error and belongs in
  `skill/equipment/`, since it will recur across every item of that type.
- **Wrong appearance** — the geometry does not resemble the real equipment →
  update the prototype description.

The middle case is the one most often misfiled. "The height is wrong" frequently
means "you applied the height to the wrong dimension", which is a knowledge
defect, not a data defect. Ask which part of the equipment the parameter refers
to rather than simply changing the number.
