# Candidate 11 — High-Density All-Component Stress Test

## Package

- Generator: `build_high_density.py`
- Candidate: `candidate/11_high_density_all_components.pml`
- Runtime: E3D Design Mk3.1.11.0[Z31110-056]
- Candidate SHA-256:
  `F655678400CD5EA69AA346996AAAE72AA13A10766496FF0A539183EFC7A339FF`

## Inventory

| Object | Count |
|---|---:|
| PIPE | 16 |
| BRANCH | 16 |
| FLANGE | 12 |
| GASKET | 12 |
| VALVE | 16 |
| INSTRUMENT | 12 |
| ELBOW | 16 |
| TEE | 16 |
| REDUCER | 12 |
| OLET | 12 |
| COUPLING | 16 |
| BEND | 12 |
| FILTER | 12 |
| CLOSURE | 16 |
| WELD | 12 |
| CAP | 4 |

## Loading instruction

Start from WORLD in a fresh E3D session and run:

```text
$M C:\Users\A\Desktop\Projects\e3d_agent\Projects\E3D_Syntax_Lab\experiments\PML-STUDY-PIPE-001\candidate\11_high_density_all_components.pml
```

Do not reload it without deleting or renaming `/CODEX-PIPE-LAB11`. If a
Collections/My Data crash occurs, capture the SIR separately; that is an
application result, not a component syntax verdict.

## Required observations

1. Does the complete SITE/ZONE/PIPE hierarchy appear?
2. Do all 16 branches display solid route geometry?
3. Which catalogue families render, remain dashed, or fail to display?
4. Query at least one instance of each family for `SPRE`, `LSTU`, `ORI` and
   `POS`; query `ARRI`/`LEAV` where present.
5. Confirm whether the alternating A3B sloped branches fall 200 mm over
   16,000 mm, and whether the FIRE specification routes load from the second
   catalogue family.
6. Record any exact E3D CP error and line before making another edit.

State: `FAILED / QUARANTINED`. The first load stopped at line 2073 because
`/FIRE` is not defined in the receiving project. The candidate must not be
used as a production macro. In addition, the screenshots show green dashed
ill-defined route lines: the generic copied component blocks were placed in a
row but were not connected to verified nozzle/branch P-points. A catalogue
component's presence is not a logical pipe connection.

Evidence SIR: `SIR-20260731-012752-undefined-fire.txt` (SHA-256
`C72ED280C92CD2D0BA4B3C5767DC5B5718E8484FB5F1A0FF6F3DC0839548B943`).

The next iteration must be connection-first: inventory the actual equipment
NOZZLE `HREF/TREF` targets and native component `ARRI/LEAV/CREF` relationships,
then generate one verified route family at a time. Nozzle geometry must use an
inline `CATR SPCOMPONENT` binding; it must never be represented by a free green
line.
