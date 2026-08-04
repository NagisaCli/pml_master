# TEE/GASKET query — success (2026-08-04)

## Evidence

User-supplied Q ATT output archived at
`results/evidence/2026-08-04_tee_gasket_query_success.txt`, produced by
candidate `13_tee_gasket_query_kit.pml` (rev 2, queries inside the INPUT
transaction).

## TEE — CREF confirmed

`TEE 1 of BRANCH /CODEX-Q13-TEE/B1`:

| Attribute | Value |
|---|---|
| `Spref` | `/A1A/TA150` |
| `Lstube` | `/A1A/PA150` |
| `Arrive` / `Leave` | 3 / 2 |
| `Angle` | 90degree |
| **`Cref`** | **`/CODEX-Q13-TEE/B2`** |
| `Height` / `Radius` | 0mm / 0mm |

This closes the round-1 outstanding item: the two-pass
`OLD ... CREF BRANCH /B2 TAIL` + `OLD BRANCH /B2 TREF TEE 1 of BRANCH /B1`
creates a working reciprocal pair — B2's `TREF` passed in round 1 and the
TEE-side `CREF` now queries back to B2.

## GASKET — identity and thickness

`GASKET 1 of BRANCH /CODEX-Q13-GASKET/B1`:

| Attribute | Value |
|---|---|
| `Spref` | `/A3B/GC20` |
| `Lstube` | `/A3B/PA20` |
| `Arrive` / `Leave` | 1 / 2 |
| **`Height`** | **0mm** |
| `RLOC` | not present in Q ATT (unset) |

The `/A3B/GC20` gasket is a **zero-thickness joint marker**: `Height 0mm`, no
real solid thickness, positioned between the flange and valve P-points
(Arrive 1 / Leave 2). This matches its round-1 appearance as a thin occluded
joint component.

## Disposition

- TEE `CREF` outstanding item: **RESOLVED**.
- GASKET identity outstanding item: **RESOLVED** (marker, zero thickness).
- Candidate 13: **VERIFIED** as the self-contained query kit form.
