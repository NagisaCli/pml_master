# Revision record — r10 (2026-08-06)

Status: generated and numerically verified; **awaits E3D visual reload**.

## Deliverable

- `JK_Pump_Build_refined_20260805_r10.pml`
  - SHA-256: `84C695F8DAFC94870DA74D8641C69855E32CDD5C62968D91DE44744A6D58F6FE`
  - Lines: 69,044; 30 EQUI / 360 SUBE / 5,727 primitives
- Report: `JK_Pump_Build_refined_20260805_report.md` (r10 section)

## Reference

- `C:\Users\A\Desktop\DBOutput.txt` (P1502B, template `/STD/PUMP006`),
  archived at `../../imports/2026-08-06_P1502B_PUMP006_DBOutput.txt`
  (SHA-256 `E6EF37E6A5FFCDC497821C42B998EB6306D63EFBDA55CB6C1CE71030A057A221`)

## What changed (base scope only)

- 5-member longitudinal frame on each baseplate top (150 members).
- 480 reference-style PYRAMID gussets (large + small per foot/pad).
- Anchors through the foot/pad centres: 2 per pump foot + 2 per motor pad
  (480 shanks + 480 hex washers + 480 hex nuts), nuts on the sole/pad tops.
- Pump-end stand (2 side plates + cross beam + carried pump-end plate) on
  13 pumps; skipped on 17 pumps blocked by low casing/drain details.
- Support-chain audit: 0 floating base elements (all bottoms carried).
- Non-base blocks byte-identical to r8 (3,365 blocks); baseplates, nozzles,
  CATR pass and NCYLI holes unchanged; lowest point U 0.

## Generators / verifiers

- `../../tools/rebuild_base_pump006.py`
- `../../tools/verify_r10.py` (all checks pass)

## Open item

- E3D visual reload and client confirmation (IR-11d).
