# Revision record — r11 (2026-08-06)

Status: **FAILED REVISION CASE** (client verdict 2026-08-06).

Client verdict: "完全的失敗案例，底部支架和泵與Motor完全分離" -- the
base support and the pump/motor are completely separated. The bridge
brackets did not connect to the pump/motor as intended. No further
modification requested; this revision is archived for reference only.
Today's base revisions r9-r11 are all rejected; the only accepted work of
the day is the negative-primitive (NCYLI) series (r2-r5 rules, VERIFIED).

## Deliverable

- `JK_Pump_Build_refined_20260805_r11.pml`
  - SHA-256: `0969EEBA59BC3C9E51143CB1A0C99A6FC0BD299BD6D094DDB9DBA0D189BDA9B8`
  - Lines: 64,420; 30 EQUI / 360 SUBE / 5,727 primitives
- Report: `JK_Pump_Build_refined_20260805_report.md` (r11 section)

## Reference

- `C:\Users\A\Desktop\DBOutput.txt` (P1502B, template `/STD/PUMP006`),
  archived at `../../imports/2026-08-06_P1502B_PUMP006_DBOutput.txt`

## What changed (base scope only, r10 -> r11)

- Old PYRAMID gussets and through-foot anchors removed (PYRAMID count 0).
- Every pump foot and motor pad now has a bridge bracket with the side
  cross-section 横-斜-平-斜-横: bolted bottom auxiliary block (12 mm) on
  the frame top, lower diagonal web (slanted EXTRUSION), middle plate
  (8 mm), upper diagonal web, and the existing sole plate / pad on top.
- The upper web reaches the platform bottom across its full width (the
  diagonals visibly connect to the upper platform).
- 2 screws per bracket at the block's transverse edges (nut on the block
  top, shank into the frame/baseplate); webs are transversely narrower, so
  screws/nuts never intersect the webs (exact parallelogram-box tests).
- Small platforms scale block/middle/web heights and nut size.

## Verification (`tools/verify_r11.py`)

- Hierarchy 30 EQUI / 360 SUBE; non-base blocks byte-identical to r8.
- 240 auxiliary blocks + 240 middle plates seated; 480 webs with the
  contact chain block->web1->middle->web2->platform (<=0.51 mm).
- 480 screws (8 BASE + 8 DRIVER per pump), nut on block top, zero
  screw/nut x web intersection.
- Support-chain audit: 0 floating base elements; lowest point U 0.
- Large cross-SUBE overlap set identical to r8 (no new clashes).

## Open item

- E3D visual reload and client confirmation (IR-11d): check the
  横-斜-平-斜-横 profile, web-to-platform contact, and screw/web clearance.
