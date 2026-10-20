# WSB Tank Top Platform Handrails — r3 (primitive-based, pending E3D acceptance)

**State:** r3 candidate generated and self-verified; NOT yet loaded in E3D.
Pending user visual acceptance.

## Why r3 exists

r2 (`output/WSB_TA_top_handrails_20260810_r2.txt`) loaded in E3D but the user
rejected the result:

> No handrail formed, wrong position; needs circular disc bases;

Verbatim evidence: `../2026-08-10_top_handrails/evidence/2026-08-10_r2_user_feedback.txt`.

The r2 block used the native HANDRA element with an RPATH built from
`CURTYP THRU` curves and a RAILSET, but **no posts (POSTSE/HRPOST) at all**.
It rendered nothing the user could see. The unverified HANDRA/RPATH template
form is therefore dropped for this job; r3 models the handrail with plain CYLI
primitives under each tank's EQUIPMENT, which is syntax verified many times in
this project.

## What r3 adds (insertion only)

Two new SUBEQUIPMENT blocks, each inserted after the tank's existing
`_ACCESS` SUBEQUIPMENT:

```
NEW SUBEQUIPMENT /205_TA_001_TOP_PLATFORM
├─ CYLI platform disc      DIAM 6000 x 12, top face U 28200  (disc base)
├─ 20 x CYLI base plate    DIAM 200 x 10, on the disc, at the rail circle
├─ 20 x CYLI post          DIAM 48.3 x 1090, to U 29300 (top-rail centre)
├─ CYLI top rail           80 tangent segments, DIAM 48.3, centre U 29300
└─ CYLI mid rail           80 tangent segments, DIAM 48.3, centre U 28750

NEW SUBEQUIPMENT /205_TA_056_TOP_PLATFORM
├─ CYLI platform disc      DIAM 6500 x 12, top face U 27700
├─ 24 x CYLI base plate    DIAM 200 x 10
├─ 24 x CYLI post          DIAM 48.3 x 1090
├─ CYLI top rail           96 tangent segments, centre U 28800
└─ CYLI mid rail           96 tangent segments, centre U 28250
```

| Tag | Platform centre | Platform top U | Platform R | Rail circle R | Posts |
|-----|-----------------|----------------|------------|---------------|-------|
| 205-TA-001 | E 26863 / S 11601 | 28200 mm | 3000 mm | 2850 mm | 20 (895 mm spacing) |
| 205-TA-056 | E 67030 / N 21008 | 27700 mm | 3250 mm | 3100 mm | 24 (812 mm spacing) |

The platform disc closes the open top face of the roof frustum
(`CONE DTOP 6000` / `DTOP 6500`) — the "circular disc base" the user asked for. Each post
stands on its own circular base plate on that disc. Top rail centreline is
1100 mm above the platform, mid rail 550 mm (per `skill/equipment/utilities-and-structures.md`).
The rail circle is inset 150 mm from the platform rim so the post base plates
stay on the disc.

Rail circles are approximated with short tangent CYLI segments:
80 segments at R 2850 (sagitta 2.2 mm) and 96 at R 3100 (sagitta 1.7 mm) per
rail — visually smooth. Segment joints land on the posts every fourth facet.

## Working baseline and hashes

The working baseline is unchanged from r2:
`imports/2026-08-10_jk_tank_edited_by_me_hexbolts.txt` (the accepted R4
anchor-bolt result, archived 2026-08-10).

| File | SHA-256 (UTF-8 BOM bytes) |
|------|---------------------------|
| Baseline import (unchanged) | `B3DC32B9BEDD147CBEA24CDDC9E954434BDF41B289CEA6F5BF3401EC4617EA94` |
| r3 `output/WSB_TA_top_handrails_20260810_r3.txt` | `AC19CECC0F02E1FD3786A7911C0B025363DEBF5BF01C3F07BC5CAC25E474B8A3` |
| Desktop copy `C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails_r3.txt` | same as r3 |

## Preservation set

Everything outside the two insertion points is byte-identical to the baseline:
all 22 equipment blocks, the 260 anchor bolts, every nozzle `CATR` binding and
every manual user edit. `build_top_platform_handrails.py` asserts the candidate
equals the baseline with the two blocks removed.

## Verification (all pass)

- NEW/END stack balanced; empties exactly once at the ZONE `/WSB_TA` END.
- `validate_pml()`: 231 pre-existing native-export findings unchanged, **0 new**;
  each inserted block validates standalone with 0 findings.
- Numerical geometry: disc centred on the tank centre with top face flush at
  the platform U; every base plate and post on the rail circle (error < 0.05 mm);
  every rail segment midpoint on the rail circle (error < 0.1 mm) at the correct
  U; chord lengths match `2R sin(π/N)`; all dimensions positive; nothing below
  the disc bottom.
- ORI before POS on every oriented rail segment; vertical elements have no ORI
  (E3D default axis is U, matching the native export).

## Reference values (to be replaced when design data is issued)

- Rail/post tube OD 48.3 mm — matches `/SLH/PIPE48.3x3.6` used in the
  structural-area native export.
- Base plate DIAM 200 x 10 and platform disc thickness 12 mm — typical post
  base plate / platform plate practice.
- Rail inset 150 mm and post spacing ~900 mm — platform-handrail practice;
  spacing is under the 1000 mm requested post spacing.
- Top rail 1100 mm, mid rail 550 mm — safety-railing practice per
  `skill/equipment/utilities-and-structures.md`.

## Open points

- `205-TA-006` does not exist in the export; `205-TA-056` is modelled as the
  intended second tank (the only other 205-series frustum-top platform tank).
  Confirm the tag.
- If the user intended a spiral access stair around the tank shell
  rather than a top platform handrail, this candidate does not cover it — say
  so in the next message and the geometry will be reworked.

## Files

| Path | Purpose |
|------|---------|
| `build_top_platform_handrails.py` | r3 generator (insertion only, self-verifying) |
| `../../output/WSB_TA_top_handrails_20260810_r3.txt` | Result for E3D |
| `C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails_r3.txt` | Desktop copy for `$M` |

Load instruction (E3D): select a writable ZONE, then
`$M C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails_r3.txt`.
