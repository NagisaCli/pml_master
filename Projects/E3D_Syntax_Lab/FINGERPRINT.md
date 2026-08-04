# FINGERPRINT — E3D_Syntax_Lab

Stable signals used to identify an incoming file as this project **before**
editing. Match several signals, then read `TIMELINE.md` for the current
baseline.

## File-name signals

- `*_native.txt` imports under `imports/` or `experiments/*/source/`
  (e.g. `2026-07-30_pipe_native.txt`, `2026-08-03_pmp10_native.txt`)
- `PML-STUDY-*` experiment folders (`PML-STUDY-PIPE-001`, `PML-STUDY-EXTR-001`)
- `*_stress.pml`, `*_point_loop.pml` style candidate studies

## Zone / site signals

- Data listings contain `NEW SITE /SITE-PIPING-AREA01` and
  `NEW ZONE /ZONE-PIPING-AREA01`, `PURP PIPE`

## Element-name signals

- PIPE / BRANCH syntax studies: `NEW PIPE`, `NEW BRANCH`, drawing-image point
  loops; not tank `EQUIPMENT` blocks.
- EXTRUSION studies: `NEW EXTRU` under `PML-STUDY-EXTR-001`.

## Look-alikes

- `JK-Tank_Build` uses `TA` tags under `NEW ZONE /WSB_TA`.
- This project holds experiments, not client equipment deliverables.
