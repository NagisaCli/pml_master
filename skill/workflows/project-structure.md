# Workflow: Projects

Every modeling job belongs to a project folder under `Projects/`. This is how
work stays traceable across sessions: given any macro, you can find the folder
that produced it; given any folder, you can see what was asked for and what was
delivered.

---

## Anatomy of a project

```
Projects/<Project-Name>/
    DO.txt                  the instruction prompt — what the user wants
    project.json            optional stable logical/output name
    equipment_data.py       the project's dataset
    Modeling_lists.xlsx     source equipment data
    Model_Reference.../     reference drawings
    imports/                immutable native E3D exports received from the user
    archive/                accepted revision records and baseline hashes
    output/
        <Project-Name>.pml          the macro, named after the project
        <Project-Name>_report.md    the engineering deliverable
```

**Only data and project-specific configuration live here.** The engine —
`wsb/pml_builder.py`, `wsb/tank_builder.py`, `wsb/report.py`, `wsb/schema.py` —
stays at the repository root and is shared by every project. That is deliberate:
an Iron Rule fix applied to the engine protects every project at once, whereas a
copy inside each project folder would have to be fixed repeatedly and would
inevitably drift.

`project.json` is optional. Use `{"name": "Logical-Project"}` when a historical
folder name must remain unchanged but commands and deliverables use a different,
stable project name. Project lookup accepts either the logical name or folder
name.

---

## Locating the project

Always start by identifying which project you are working on.

```bash
python -m wsb --list-projects
```

Then read its `DO.txt` **before** modelling anything. It is the authoritative
statement of requirements for that project and outranks any assumption you would
otherwise make.

In code:

```python
from wsb import resolve_project

project = resolve_project("JK-Project")   # forgiving: exact, case-insensitive, or unique partial
project.instructions()                    # DO.txt text
project.tanks()                           # the equipment register
project.macro_path()                      # where the deliverable goes
```

With a single project present, `resolve_project()` with no argument resolves to
it. With several, it refuses to guess and lists them — modelling the wrong
project silently is worse than stopping to ask.

---

## DO.txt is a living document

`DO.txt` is not a historical record of the original request. It is the current
statement of what the project requires, and it **evolves**:

- The user supplies it directly, or it is extracted from their prompt.
- When new requirements arrive mid-project, **update it** — do not leave the
  requirement only in a chat message that the next session will never see.
- When the user corrects an assumption, and the correction is specific to this
  project, record it here. If it generalises to all equipment of that type, it
  belongs in [skill/equipment/](../equipment/README.md) instead — see
  [capturing-feedback.md](capturing-feedback.md).

A requirement that exists only in conversation is lost at the end of the session.
That is the failure this file exists to prevent.

### Native-export continuations

When the user supplies a PML exported after manual E3D editing, save the original
unchanged under `imports/` and compare it against the last accepted file before
making any modification. The native export is the new working baseline; the
generator's earlier output is historical evidence, not an overwrite target.
Follow [reconciling-native-exports.md](reconciling-native-exports.md).

---

## Output naming

Deliverables are named after the project:

```
Projects/JK-Project/output/JK-Project.pml
Projects/JK-Project/output/JK-Project_20260724_193000.pml
```

Never `model.pml`, `output.pml`, or `wsb_tanks.pml`. The name is what lets you —
or the user, months later — identify which project a macro belongs to, reopen it,
and iterate on it. `--no-timestamp` overwrites the canonical name; the default
keeps successive runs side by side.

---

## Running a job

```bash
python -m wsb --project JK-Project --dry-run     # validate, write nothing
python -m wsb --project JK-Project               # generate, timestamped
python -m wsb --project JK-Project --no-timestamp
python -m wsb --project JK-Project --tag 205-TA-008
```

Output defaults to the project's own `output/` folder. Verification runs on every
invocation and the command exits non-zero if any equipment fails.

---

## Starting a new project

1. Create `Projects/<Name>/`.
2. Write `DO.txt` — the requirements, from the user's prompt or supplied directly.
3. Add the source data (equipment list, drawings).
4. Write `equipment_data.py`, importing its types from `wsb.schema`:

   ```python
   from wsb.schema import TankSpec, Nozzle, HeadType, BottomType, SupportType, Provenance

   TANKS = (TankSpec(tag="...", ...),)
   ```

   The register may be named `TANKS`, `WSB_TANKS` or `EQUIPMENT`.
   Record a `Provenance` for every value as you go — reconstructing it later is
   unreliable, and the deliverable's Reference Values section depends on it.
5. Generate, verify, deliver.
6. **Create `skill/projects/<name>.md`** — see
   [the project memory README](../projects/README.md). The folder holds the data;
   the skill log holds the experience: what went wrong, and how it was solved.

---

## Two kinds of memory, kept apart

| | `Projects/<name>/` | `skill/projects/<name>.md` |
|---|---|---|
| Holds | Data, instructions, deliverables | Experience and lessons |
| Answers | "What are the numbers?" | "What went wrong and why?" |
| Read when | Executing this project | Starting any similar project |

Keep them separate. The project folder is what the *client* work needs; the skill
log is what the *next* project needs. Merging them buries the transferable
lessons inside project-specific detail where nobody will find them again.
