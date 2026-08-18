# Site-wide NOZZLE CATR repair — superseded by the native PML plugin

**State:** SUPERSEDED on 2026-08-18. Archived for the audit trail only. Do not
run these scripts; use `pml_plugins/nozzle_converter/` instead.

## What this was

A pair of one-off Python scripts that repaired NOZZLEs whose catalogue
reference had been lost (`Nulref`) after a cross-project library import. A
nozzle without a bound `CATR` draws nothing in E3D — see
[catalogue-elements.md](../../../../skill/knowledge/catalogue-elements.md) —
so the site appeared to be missing 235 nozzles that were in fact present but
invisible.

The scripts walked the workspace for every known `NOZZLE → CATR` pairing, then
emitted a PML1 macro rebinding each nozzle in `/SEAL/EQUIP`.

| File | Role |
|------|------|
| `fix_nozzle_catr.py` | Builds the macro, wrapping each repair in `handle ANY` / `endhandle` |
| `generate_pure_pml.py` | Later variant: same mapping, no error handling, wrote `.mac`/`.pml`/`.txt` to the Desktop |
| `fix_site_nozzles.pml` | The generated deliverable — 235 nozzles |

Of the 235 repairs, **222 carry a mapping recovered from existing project
files**; the remaining **13 fall back to the `AAZFBB0YY` default**, which is a
Reference Value, not project data — those 13 were guesses and should be
re-checked against the drawings if this record is ever relied on.

## Why it is superseded

`pml_plugins/nozzle_converter/` does the same job natively inside E3D and is
better on every axis that mattered here:

- **Scope control** — CE / Zone / Site / World, instead of one hardcoded site.
- **Non-destructive** — its "repair Nulref only" toggle cannot overwrite a
  nozzle that already holds a correct spec. These scripts rebound all 235
  unconditionally.
- **Bore-preserving** — `nozzle_smart_apply.mac` keeps the existing bore when
  changing the spec; these scripts did not read bore at all.
- **No external input** — the plugin reads the live model. These scripts
  depended on `C:\Users\A\Desktop\yes_detec.txt`, which no longer exists, so
  neither can be re-run as written.

## Why they were archived rather than deleted

They are the only record of *which* 235 nozzles were repaired and with what
specs. The macro is the evidence behind that pass; the plugin, being
interactive, leaves no equivalent artifact. If a nozzle in `/SEAL/EQUIP` is
later found with a wrong spec, this file is where to look first.

They also violated two standing rules while they sat in the repository root —
worth recording, since both are now enforced:

1. Deliverables belong in `Projects/<name>/output/`, never the repository root
   or the Desktop (`test_skill_integrity.py`).
2. Repository paths must not be hardcoded (`test_repo_hygiene.py`). Both
   scripts embedded `C:\Users\A\Desktop\Projects\e3d_agent`.

The scripts are archived **exactly as written**, still carrying those defects.
They are a record, not a template — do not copy this pattern.

## Integrity

```
0e8796d6972ffed5de4f33fad0cbf034cb2b70f71cb0a28afc83ddd1dfba9eeb  fix_nozzle_catr.py
f774a7c0eb7e43a3642178883af1e981a8981bb6fc2f31f41066cf7cc828116b  generate_pure_pml.py
e2f6879fc33830e95c6b361c5e49f313b8e12f17b017b84925ab91a577e7a2a7  fix_site_nozzles.pml
```
