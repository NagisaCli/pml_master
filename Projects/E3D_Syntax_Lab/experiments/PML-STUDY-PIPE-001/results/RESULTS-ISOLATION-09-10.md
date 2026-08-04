# Crash-isolation candidates 09/10 — user results (2026-08-04)

## Evidence

| Candidate | User verdict | Query evidence | Archive |
|---|---|---|---|
| 09 (core straight/slope) | Visual confirmation correct | `Q ATT` on both BRANCHes | `evidence/2026-08-04_candidate09_att.txt`, SHA-256 `2B7A9DD70A20BA447B2CE03D6FB3659029AD2E0E206F935F770B4B9453BB1AB2` |
| 10 (elbow/reducer) | Visual confirmation correct | `HBore 100mm` / `TBore 80mm` | chat report 2026-08-04 |

## Candidate 09 — queried attributes match the macro exactly

`/CODEX-P09-01-HEADER/B1` (straight):

| Attribute | Written | Queried |
|---|---|---|
| `Hposition` | E 0 N 0 U 0 | E 0 N 0 U 0 |
| `Tposition` | E 12000 N 0 U 0 | E 12000 N 0 U 0 |
| `Hdirection` / `Tdirection` | E / W | E / W |
| `Hbore` / `Tbore` | 100 / 100 | 100mm / 100mm |
| `Hstube` | `/A3B/PA100` | `/A3B/PA100` |
| `Pspec` | `/A3B` | `/A3B` |
| `Sloreference` | (none) | Nulref |

`/CODEX-P09-02-SLOPE/B1` (1:100 slope):

| Attribute | Written | Queried |
|---|---|---|
| `Hposition` | E 0 N 2500 U 100 | E 0 N 2500 U 100 |
| `Tposition` | E 10000 N 2500 U 0 | E 10000 N 2500 U 0 |
| `Hdirection` / `Tdirection` | E 0.5729 D / W 0.5729 U | E 0.5729 D / W 0.5729 U |
| `Hstube` | `/A1A/PA100` | `/A1A/PA100` |
| `Pspec` | `/A1A` | `/A1A` |
| `Sloreference` | `/1in100` | `/1in100` |

## Candidate 10 — reducer bores confirmed

`/CODEX-P10-02-REDUCER/B1` queried `HBore 100mm` / `TBore 80mm`, matching the
written 100-to-80 vertical transition. The Up-to-West elbow route rendered as
one continuous solid, matching candidate 06's verified form.

## Disposition

- Both isolation halves pass: the multi-PIPE ZONE form itself (two PIPEs per
  ZONE in each candidate) loads and renders; the straight/slope and
  elbow/reducer families each work in isolation.
- Candidate 08's Collections/My Data fatal exception is therefore **not**
  attributable to any of the four verified syntax families; it remains an
  application/add-in level failure. Candidate 08 may be re-submitted now that
  both halves are certified, or kept as a combined-load stress case.

## Candidate 08 re-submitted — VERIFIED (2026-08-04)

The balanced cluster loaded normally; the user reported it is not complex. All
four routes coexist in one ZONE. The crash investigation is closed as an
application/add-in level failure.
