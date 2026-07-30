# E3D Agent — AVEVA E3D Modeling Automation for Pulp & Paper Plants

Generates PML1 macro scripts for **AVEVA E3D (Everything3D Mk3.1)** from project
data, drawings, and natural language. Every rule it applies has been verified
against E3D Design Mk3.1.11.0.

The current delivery is the **Washing, Screening & Bleaching (WSB)** tank
package: 22 tank-type equipment items modelled from the JK-Project equipment
list, each positioned by its bottom centre point and ready for piping design.

---

## Quick start

Requires Python 3.9+. No third-party packages are needed to generate models;
`pytest` is needed to run the tests.

List the available projects:

```bash
python -m wsb --list-projects
```

Generate a project's models and engineering report:

```bash
python -m wsb --project JK-Project
```

This writes two files to `Projects/JK-Project/output/`, both named after the
project so a macro can be traced back to the folder that produced it:

- `JK-Project_<timestamp>.pml` — the E3D macro, 451 primitives and 114 native NOZZLE elements across 22 tanks
- `JK-Project_<timestamp>_report.md` — the engineering deliverable

Use `--no-timestamp` to write the canonical `JK-Project.pml` instead.

Model a single tank:

```bash
python -m wsb --project JK-Project --tag 205-TA-008
```

Validate without writing anything:

```bash
python -m wsb --project JK-Project --dry-run
```

With exactly one project present, `--project` may be omitted.

Load the macro in E3D: open Design, select a **writable ZONE** as the current
element, then run `$M <path to the .pml file>`.

---

## What the WSB package produces

Each tank is built from standard E3D primitives — `CYLI`, `CONE`, `DISH`, `BOX` —
with no Boolean operations, so the models stay editable and maintainable.

Per tank the generator models the shell and its head and bottom closures, the
skirt or legs, stiffening rings, access platforms, the nozzle schedule with
flanges, manways, and agitators where the reference drawings show them.

The model tree keeps assemblies separable:

```
EQUI /203_TA_006            POS E 0 N 0 U 0
  SUBE /203_TA_006_SUPPORT     skirt or legs, base ring
  SUBE /203_TA_006_SHELL       shell, roof, bottom
  SUBE /203_TA_006_N1          neck + flange
  SUBE /203_TA_006_N2          neck + flange
  ...                          one SUBE per nozzle
  SUBE /203_TA_006_M1          manway
  SUBE /203_TA_006_ACCESS      stiffening rings
  SUBE /203_TA_006_INTERNALS   agitator
```

One `EQUI` per item of equipment, named for its tag, and **every nozzle in its
own `SUBE`** — so a piping designer can select, attach to and modify one
connection without disturbing the shell or its neighbours.

Each `EQUI` is anchored at `POS E 0 N 0 U 0`. A bare `POS` in E3D is measured
with respect to the owner, not the world (the world form is `POS ... WRT /*`).
The primitives below hold world-absolute coordinates, so the `EQUI` must sit at
zero; if it inherited a position, the whole tank would shift by that amount.

### Positioning

The project requires each tank's **bottom centre point** to coincide with the
installation coordinate from the equipment list — not the geometric centre,
model centre, or bounding box centre.

All geometry is generated in a local frame whose origin is the bottom centre,
then translated by the installation coordinate, so the requirement holds by
construction.

E3D datums are element-specific: `CYLI`, `CONE` and `BOX` use geometric centre,
while `DISH` uses its flat rim / tangent plane. The builder converts the
bottom-face point for CYLI/CONE into the centre datum in one place and passes a
DISH rim point through unchanged. Getting either rule wrong shifts geometry by
half its own height and either telescopes the model or makes a head float.

`verify_bottom_centre()` re-checks every tank by parsing the emitted primitives
and computing their true extents, rather than string-matching a `POS` line — a
textual check cannot detect a wrong datum. `python -m wsb` exits non-zero if any
tank fails.

For a skirt- or leg-supported vessel the datum is the foundation bearing plane
at the bottom of the support, which is how the coordinate is set out on site.
Nothing is modelled below it.

---

## Source data

Each project's data lives in its own folder. For JK-Project, primary data is
`Projects/JK-Project/Modeling_lists.xlsx`. The reference drawings in
`Model_Reference(All_Top_View)` and `Model_reference(Part_Side_View)` establish
the structural configuration; the side views are P&ID sketches carrying volume,
height, diameter and temperature annotations. `Do.txt` states the requirements
and is kept current as they evolve.

Every value in the dataset carries a `Provenance` recording where it came from,
which drives the report's Reference Values section:

| Provenance | Meaning |
|------------|---------|
| `EXCEL` | Read from the equipment list. Contractual data. |
| `SIDE_VIEW` / `TOP_VIEW` | Read from a project reference drawing. |
| `RECOVERED` | Recovered from a corrupted Excel cell. |
| `DERIVED` | Computed from project data. |
| `STANDARD` | Reference Value — standard pulp mill practice. |
| `VENDOR_TYPICAL` | Reference Value — Valmet / ANDRITZ / Voith practice. |

The last three are assumptions and are listed individually in the deliverable so
they can be replaced when official design data is issued.

### Source data defects

Three defects in the workbook are corrected in the data layer, never by editing
the workbook, and each is reported as a data-quality exception:

1. **Corrupted coordinates (13 of 22 rows).** Rows Excel stored as numbers lost
   their parentheses and commas, concatenating the digits: `-1500019860300` is
   `(15000, 19860, 300)`. All restored coordinates are positive — the minus sign
   on a corrupted cell is an artefact of the concatenation, not project data. The
   9 rows that survived as text keep their listed signs unchanged. Every one of
   the 22 coordinates has been re-derived from the raw workbook XML and matches
   the dataset exactly.
2. **Transposed height and diameter on `205-TA-008` and `205-TA-011`.** The side
   views give the correct orientation. For `205-TA-008` the transposed reading
   implies 706 m³ against a stated 65 m³ — an order of magnitude out.
3. **`2205-TA-050.png` is misnamed.** The drawing it contains is `205-TA-059`.

---

## PML1 compliance

Macros must be pure PML1; PML2 syntax makes E3D fail to load the file. Two rules
are enforced structurally rather than by review:

**ORI before POS.** `PMLBuilder` emits the orientation line before the position
line for every primitive, and callers never write `POS` themselves. With the
reverse order E3D rotates the position vector and the element drifts silently —
there is no error to notice.

**PML1 only.** The builder emits nothing but PML1. `validate_pml()` re-checks the
assembled text for PML2 constructs, PML2 variable assignment, and ORI/POS
ordering across all three oriented primitive types, and `build()` raises rather
than return a macro that would fail in E3D.

**No rendering-control prologue.** `ALPHA HEADER OFF`, `VAR 0`, `SUSPEND` and
`RESUME` are not E3D Design commands — they appear nowhere as commands in
AVEVA's PML library, where every occurrence of "suspend" is a method name or a
word inside a comment. Each aborts the macro at its own line with
`(47,15) CP: Syntax error`. The macro therefore contains element creation only,
and the validator rejects all four. The comment token is `--`, as used
throughout AVEVA's own `data\*.mac` files.

Full modeling rules, primitive reference and equipment specifications live in the
skill: start at [SKILL.md](SKILL.md), then
[skill/knowledge/iron-rules.md](skill/knowledge/iron-rules.md).

---

## Continuing from a manually edited E3D export

A PML file exported after manual E3D work is treated as the new working
baseline, not as disposable generated output. Archive the received file
unchanged, compare it with the last accepted macro, and preserve every
out-of-scope manual change:

```bash
python -m wsb.pml_compare accepted.pml native-export.pml
python -m wsb.pml_compare accepted.pml native-export.pml --format json
```

The comparison is hierarchy- and attribute-aware: it reports added/removed
elements and changes to `POS`, `ORI`, dimensions, catalogue references and other
properties while ignoring comment, whitespace and numeric-format noise. The
full procedure is in
[reconciling-native-exports.md](skill/workflows/reconciling-native-exports.md).

---

## Project layout

```
SKILL.md                Entry point — read this first
skill/                  The skill: knowledge, workflows, memory
  knowledge/            Iron Rules and verified PML1 reference
  workflows/            Project structure, modeling run, failure diagnosis, feedback
  equipment/            Equipment prototype knowledge base
  projects/             Project memory — what was built and what went wrong
Projects/               One folder per modeling project
  JK-Project/
    Do.txt              Instruction prompt — the living requirements
    equipment_data.py   This project's 22-tank dataset, with provenance
    Modeling_lists.xlsx Source equipment list
    Model_Reference*/   Reference drawings
    output/             JK-Project.pml and the engineering report
wsb/                    Shared modeling engine — used by every project
  schema.py             TankSpec, Nozzle, Provenance and the closure/support types
  pml_builder.py        PML1 primitive emitter and validator
  tank_builder.py       Tank geometry generation
  report.py             Engineering deliverable
  projects.py           Project registry: discovery, loading, output naming
  generate.py           Pipeline and CLI
  pml_compare.py        Semantic comparison for accepted/native-export PML files
drawing_parser/         SVG / PDF / DXF and natural language parsing
pml_knowledge/          Retrieval over skill/ for the Python pipeline
pml_generator/          DesignIntent to PML1 generation
e3d_interface/          E3D execution: file mode and command line
memory/                 Runtime error tracking
examples/               Standalone reference plant generators
tests/                  Test suite, including skill integrity checks
```

**Engine at the root, data in the project folder.** `wsb/` is generic and shared,
so an Iron Rule fix applies to every project at once; only data and
project-specific configuration live under `Projects/`. A project supplies
instances of the `wsb.schema` types, and the builder, validator and report work
against any project unchanged.

`skill/` is the single source of truth for modeling knowledge. It is read by
humans, by any AI model, and by `pml_knowledge/knowledge_base.py` — so the rules
cannot drift between a human copy and a machine copy, which is what previously
went wrong.

---

## General agent pipeline

Beyond the WSB package, the agent generates models from descriptions or drawings:

```bash
python -m e3d_agent.agent "a 4800mm fourdrinier paper machine with 40 dryer cylinders"
```

```bash
python -m e3d_agent.agent --svg path/to/process.svg
```

```bash
python -m e3d_agent.agent --query "bleach tower dimensions"
```

Run these from the parent directory of the repository, since the repository is
itself the `e3d_agent` package.

Standalone reference generators:

```bash
python -m e3d_agent.examples.paper_machine_model
```

---

## Configuration

Paths resolve from environment variables, so no source edits are needed:

| Variable | Purpose | Default |
|----------|---------|---------|
| `E3D_PROJECT_ROOT` | AVEVA project root | `D:\AVEVA\Projects\E3D3.1` |
| `E3D_DESIGN_EXE` | `des.exe`, only for direct execution | `D:\AVEVA\Everything3D3.1\des.exe` |
| `E3D_OUTPUT_DIR` | Macro output directory | `output/` beside the package |
| `E3D_MEMORY_PATH` | Memory store location | `memory/memory_store.json` |

Generation works without E3D installed.

---

## Tests

```bash
python -m pytest tests/ -v
```

The suite covers the guarantees that cannot be checked by eye across 400+
primitives: that every tank sits on its listed coordinate, that ORI precedes POS
for every oriented primitive, that no PML2 syntax reaches the macro, and that
the corrected dimensions reconcile with the stated volumes.

---

## License

MIT
