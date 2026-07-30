# Project Memory

What has been modelled, how, what went wrong, and how it was resolved.

**Read this before starting any modeling job.** If similar equipment appears in a
log below, you inherit its resolved parameters, its user corrections, and its
mistakes-already-made. Starting from a prior job is faster and more accurate than
starting from the equipment knowledge base.

---

## Completed projects

| Project | Folder | Scope | Status | Log |
|---------|--------|-------|--------|-----|
| JK-Project | `Projects/JK-Tank_Build/` | Pulp Mill WSB area — 22 tank-type items | Delivered, verified; logical name retained through `project.json` | [jk-project-wsb.md](jk-project-wsb.md) |
| JK_Pump_Build | `Projects/JK_Pump_Build/` | 30 horizontal process/MC pumps; individual macros plus one combined loader, one EQUI per tag | Final combined macro visually accepted in E3D; ongoing customization memory retained | [jk-pump-build.md](jk-pump-build.md) |
| JK_Cooking_Tank_Build | `Projects/JK_Cooking_Tank_Build/` | 15 cooking-plant tanks/vessels; compound Blow Tank profiles, accumulators, junk traps and a horizontal condensate receiver | R5 loaded and visually accepted; archived as the continuation baseline | [jk-cooking-tank-build.md](jk-cooking-tank-build.md) |

Each entry has **two homes**: the folder under `Projects/` holds its data,
`DO.txt` and deliverables; the log here holds the experience. See
[project-structure.md](../workflows/project-structure.md).

```bash
python -m wsb --list-projects
```

---

## Reference generators

Not client deliverables — worked examples of geometry generation at scale, under
`examples/`:

| Script | Demonstrates |
|--------|--------------|
| `paper_machine_model.py` | Full fourdrinier machine, section by section |
| `paper_mill_plant_master.py` | Whole-plant layout across areas |
| `paper_mill_mega_100k_plant.py` | High-primitive-count generation |

These use a **flat hierarchy** (one EQUI, area-level SUBEs) to keep large models
manageable. That is not the equipment convention — real equipment follows IR-8.
Do not copy their hierarchy into equipment work.

---

## Writing a project log

One file per project, named for it. Cover:

1. **Scope and status** — what was asked for, what was delivered, verified how
2. **Source data** — where it came from, and **what was wrong with it**
3. **Modeling decisions** — configuration choices and their reasoning
4. **Problems encountered and how they were solved** — the most valuable section
5. **Reference Values** — what was assumed, pending confirmation
6. **Outstanding issues** — what the next person must resolve
7. **Lessons promoted** — what moved into `skill/knowledge/` or `skill/equipment/`

Section 4 is why this directory exists. Record the **symptom** as well as the
fix — the symptom is what a future reader will recognise when it happens again.

Write the log even when a project goes perfectly; "nothing went wrong" is itself
a useful signal about which workflows are working.
