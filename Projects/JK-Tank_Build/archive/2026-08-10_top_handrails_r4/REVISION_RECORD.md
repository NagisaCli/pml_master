# WSB Tank Top Handrails — r4 (position corrected to the cylinder top, pending E3D acceptance)

**State:** r4 CONFIRMED by the user on 2026-08-10 ("Approved, nicely done") after
loading in E3D. Accepted baseline for the next continuation.

## Why r4 exists

r3 rendered the handrail correctly but the user corrected its position:

> Approved, stairs appear normally; but position wrong, what I want is circling around the big circle at the cylinder top,
> not the small circle at the frustum top; place them directly on the cylinder top surface circling around,
> and I will adjust the cone frustum size later

Verbatim evidence: user message 2026-08-10 (continuation of the R5/R6 job).

The handrail ring therefore moves from the roof-frustum top (small circle,
DTOP) to the top of the shell cylinder (big circle). The frustum and its top
platform remain the designer's to adjust afterwards, so **no platform disc is
emitted in this revision** and the r3 disc/handrail blocks are not included.

## What r4 adds (insertion only)

Two new SUBEQUIPMENT blocks, each inserted after the tank's existing
`_ACCESS` SUBEQUIPMENT, containing only the handrail itself:

```
NEW SUBEQUIPMENT /205_TA_001_TOP_HANDRAIL
├─ 36 x CYLI base plate   DIAM 200 x 10, on the cylinder top face
├─ 36 x CYLI post         DIAM 48.3 x 1090
├─ CYLI top rail          144 tangent segments, DIAM 48.3, centre U 27500
└─ CYLI mid rail          144 tangent segments, DIAM 48.3, centre U 26950

NEW SUBEQUIPMENT /205_TA_056_TOP_HANDRAIL
├─ 32 x CYLI base plate   DIAM 200 x 10
├─ 32 x CYLI post         DIAM 48.3 x 1090
├─ CYLI top rail          128 tangent segments, centre U 27500
└─ CYLI mid rail          128 tangent segments, centre U 26950
```

| Tag | Cylinder top (big circle) | Rail circle | Posts | Spacing |
|-----|---------------------------|-------------|-------|---------|
| 205-TA-001 | DIAM 10800 at U 26400 (R 5400) | R 5300 (inset 100 mm) | 36 | 925 mm |
| 205-TA-056 | DIAM 9900 at U 26400 (R 4950) | R 4850 (inset 100 mm) | 32 | 952 mm |

The base-plate outer edge is flush with the cylinder rim, so every plate sits
fully on the cylinder top face while the ring reads as following the big
circle. Post bottom is on the cylinder top face (U 26400); post top and top
rail centreline are at U 27500 (face + 1100 mm); mid rail centreline at
U 26950 (face + 550 mm). Rail circles use 144 / 128 tangent CYLI segments —
sagitta 1.2 mm, visually smooth.

## Working baseline and hashes

Working baseline is unchanged: `imports/2026-08-10_jk_tank_edited_by_me_hexbolts.txt`
(accepted R4 anchor-bolt result). The r3 platform blocks are not part of this
file; load r4 on a model state without `/205_TA_001_TOP_PLATFORM` and
`/205_TA_056_TOP_PLATFORM` (delete them first or reload the baseline), otherwise
two handrail rings will coexist.

| File | SHA-256 (UTF-8 BOM bytes) |
|------|---------------------------|
| Baseline import (unchanged) | `B3DC32B9BEDD147CBEA24CDDC9E954434BDF41B289CEA6F5BF3401EC4617EA94` |
| r4 `output/WSB_TA_top_handrails_20260810_r4.txt` | `946F87CA5F3DFC887D3FBAA25A330845AAEE7BA52CDB184B4C55FBA08FEC9642` |
| Desktop copy `C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails_r4.txt` | same as r4 |

## Preservation set

Everything outside the two insertion points is byte-identical to the baseline:
all 22 equipment blocks, the 260 anchor bolts, every nozzle `CATR` binding and
every manual user edit. `build_cylinder_top_handrails.py` asserts the candidate
equals the baseline with the two blocks removed.

## Verification (all pass)

- NEW/END stack balanced; empties exactly once at the ZONE `/WSB_TA` END.
- `validate_pml()`: 231 pre-existing native-export findings unchanged, **0 new**;
  each inserted block validates standalone with 0 findings.
- Numerical geometry: every base plate and post on the rail circle
  (error < 0.05 mm); every rail segment midpoint on the rail circle
  (error < 0.1 mm) at the correct U; chord lengths match `2R sin(pi/N)`;
  all dimensions positive; nothing below the cylinder top face.
- ORI before POS on every oriented rail segment; vertical elements have no ORI
  (E3D default axis is U, matching the native export).

## Known interaction to watch when loading

The existing roof frustum (TA-001 DBOT 10800 -> DTOP 6000; TA-056 DBOT 9900 ->
DTOP 6500) rises from the same rim the handrail follows. The cone surface
passes through the post zone for roughly the first 30–40 mm above the face at
this rail radius. This is the expected temporary condition the user accepted
("I will adjust the cone frustum size later" — the frustum will be adjusted afterwards); if the posts
must clear the cone as-built, the user is asked to supply the adjusted frustum
bottom diameter and the rail radius will be moved accordingly.

## Reference values (to be replaced when design data is issued)

- Rail/post tube OD 48.3 mm — matches `/SLH/PIPE48.3x3.6` in the
  structural-area native export.
- Base plate DIAM 200 x 10 — typical post base plate practice.
- Rail inset 100 mm (plate outer edge flush with the cylinder rim) — chosen so
  the plates stay on the cylinder top face.
- Post spacing 925 / 952 mm — under the 1000 mm post-spacing practice.
- Top rail 1100 mm, mid rail 550 mm — safety-railing practice per
  `skill/equipment/utilities-and-structures.md`.

## Open points

- `205-TA-006` does not exist in the export; `205-TA-056` is modelled as the
  intended second tank. Confirm the tag.
- If the user wants the ring exactly on the cylinder rim (base plates
  half-overhanging) instead of inset 100 mm, only the rail radius changes.
- The frustum/platform size remains the designer's to adjust after this load.

## Files

| Path | Purpose |
|------|---------|
| `build_cylinder_top_handrails.py` | r4 generator (insertion only, self-verifying) |
| `../../output/WSB_TA_top_handrails_20260810_r4.txt` | Result for E3D |
| `C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails_r4.txt` | Desktop copy for `$M` |

Load instruction (E3D): select a writable ZONE (model state without the r3
platform blocks), then
`$M C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails_r4.txt`.
