# Advanced family candidates 14-17 — status

Generated 2026-08-04 by `build_advanced_candidates.py` (verbatim native
slices, renamed into isolated SITEs). All pass local PML validation and
NEW/END balance. Awaiting the user's E3D verdict.

| Candidate | SITE | Families | Expected E3D result | Status |
|---|---|---|---|---|
| 14 | `/CODEX-PIPE-LAB14` | FILTER, CLOSURE, FBLIND, COUPLING, WELD | Solid routes, components posed; `/WELDGAP` paths resolve | **VERIFIED** — imported, all components display (2026-08-04) |
| 15 | `/CODEX-PIPE-LAB15` | BEND, OLET, PTAPPING+PIPCARTESIAN | BEND/OLET render; `/General-Tappings` resolves | **VERIFIED** — imported, all components display (2026-08-04) |
| 16 | `/CODEX-PIPE-LAB16` | B1/B2/B3 + TEE 2/OLET 1/OLET 2 network | Branches connected; HREF/TREF/CREF reciprocal; no dashed legs | **VERIFIED** — imported, all components display (2026-08-04) |
| 17 | `/CODEX-PIPE-LAB17` | CAP (`/FIRE`) | Either renders or `(2,109) Undefined name /FIRE` | **GATED** — `(2,109) Undefined name /FIRE` exactly as predicted; CAP not testable until the project defines `/FIRE` |

Record user observations here when supplied (visual + any `Q ATT` output or
exact E3D error line).

## 2026-08-04 — candidate 14 first attempt

Aborted at line 21:

```
(2,111)   Cannot access element type SPEC from the level of PIPE /CODEX-QFILTER
PSPE SPECIFICATION SPECIFICATION /A3B
```

**Cause: generator bug, not an E3D syntax verdict.** `build_advanced_candidates.py`
re-added the `SPECIFICATION` keyword on top of the branch's own
`PSPE SPECIFICATION /A3B` value. Fixed; all generated `PSPE` lines are now
`PSPE SPECIFICATION <spec>` and all candidates re-validate. Re-run q14 after
deleting `/CODEX-PIPE-LAB14`.

## 2026-08-04 — user verdicts

- Candidates 14, 15 and 16: imported normally, every component family in the
  slices displays correctly. VERIFIED for the exact native forms tested.
- Candidate 17: `(2,109) Undefined name /FIRE` at line 21
  (`PSPE SPECIFICATION /FIRE`) — the receiving project has no `/FIRE`
  specification. CAP therefore remains GATED on `/FIRE` being added to the
  project; the syntax itself produced no other error.
