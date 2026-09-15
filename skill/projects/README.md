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
| JK_Pump_Build | `Projects/JK_Pump_Build/` | 30 horizontal process/MC pumps; individual macros plus one combined loader, one EQUI per tag | Final combined macro visually accepted in E3D; ongoing customization memory retained | [jk-pump-build.md](jk-pump-build.md) — current state; rounds in [jk-pump-build-history.md](jk-pump-build-history.md) |
| JK_Cooking_Tank_Build | `Projects/JK_Cooking_Tank_Build/` | 15 cooking-plant tanks/vessels; compound Blow Tank profiles, accumulators, junk traps and a horizontal condensate receiver | R5 loaded and visually accepted; R6 native-export rework (base plates + slimmed supports) archived 2026-08-02 | [jk-cooking-tank-build.md](jk-cooking-tank-build.md) |
| E3D_Syntax_Lab | `Projects/E3D_Syntax_Lab/` | Native-export-driven syntax studies and E3D certification packages | PIPE core rounds 1–2 VERIFIED in E3D Design Mk3.1.11.0 | [e3d-syntax-lab.md](e3d-syntax-lab.md) |
| Typical_Pipe_Support | `Projects/Typical_Pipe_Support/` | Standalone STRUCT cantilever, hex screws and welded connection review | R2 screenshot reviewed; reconstructed R3 static PASS, E3D review pending | [typical-pipe-support.md](typical-pipe-support.md) |

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

Every project folder also carries `TIMELINE.md` — the project time tree (newest
first, current baseline marked ●). It is the dated history of revisions and
archives; see
[project-structure.md](../workflows/project-structure.md#the-time-tree--timelinemd).

Every project folder also carries `FINGERPRINT.md` — the stable signals used to
identify an incoming file as that project before editing (file patterns, zone
names, tag conventions, coordinate anchors). See
[project-structure.md](../workflows/project-structure.md#identify-before-you-edit).
