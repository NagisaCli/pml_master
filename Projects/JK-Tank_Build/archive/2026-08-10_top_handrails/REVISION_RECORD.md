# WSB Tank Top Handrail Pass — 2026-08-10 (r2 candidate)

**State:** r2 loaded in E3D but the result is NOT accepted; work paused per
the user ("continue tomorrow"). Saved as-is.

Revision history:

- r1 — inserted the STRUCTURE block immediately before the first `OLD NOZZLE`
  line. E3D rejected it with `(41,8) Cannot create a STRU at this level`:
  in this native export the ZONE `/WSB_TA` is already closed by its `END`
  before the nozzle-binding pass, so the STRUCTURE was created outside the
  ZONE (SIR `SIR-YHL-Design-20260810-061354.txt`).
- r2 — the same block is inserted **before the ZONE's closing END** (original
  line 12984, after the last EQUIPMENT block). The NEW/END stack is verified:
  it empties exactly once, at the ZONE END, now line 13137.

## E3D observation on r2 (2026-08-10, verbatim evidence)

The ZONE-level error is gone (the macro loaded), but the user rejected the
result:

> No handrail formed, wrong position; needs circular disc bases;

Verbatim record: `evidence/2026-08-10_r2_user_feedback.txt`.

Interpretation to investigate tomorrow (not yet confirmed with the user):

1. **"No handrail formed"** — the expected circular handrail did not appear (the
   user may describe the expected result loosely as a stair-like enclosure);
   the HANDRA/RPATH form produced nothing visible or something unintended.
2. **"Wrong position"** — the geometry that did appear is not on the tank
   top platform; likely the HANDRA `POS` / RPATH point coordinate semantics
   (relative vs absolute) do not match how E3D interprets them in this
   context. Need a minimal coordinate probe before regenerating.
3. **"Needs circular disc bases"** — the handrail posts must sit on circular disc base
   plates (circular disc base), not whatever the current HANDRA defaults generate. If we
   keep HANDRA, the post/base needs an explicit HRPOST/TMPLATE or catalogue
   part; alternatively fall back to primitives (CYLI posts + EXTRUSION rail
   segments + CYLI disc bases).

No new candidate was generated today; the r2 file and this record are the
saved state.

## Request

User instruction (2026-08-10):

> Add a 1.1 m high circular handrail around the flat top platform of the roof
> frustum on two tanks (205-TA-001 and "205-TA-006").

**Tag note:** `/205_TA_006` does not exist in this export or anywhere in the
project archive. The only two 205-series tanks whose roof is a frustum with a
flat top platform are:

| Tag | Roof frustum | Top platform |
|-----|--------------|--------------|
| 205_TA_001 | DBOT 10800, DTOP 6000, HEIG 1800 | DIAM 6000 at U 28200 |
| 205_TA_056 | DBOT 9900, DTOP 6500, HEIG 1300 | DIAM 6500 at U 27700 |

`205_TA_056` was therefore taken as the intended second tank (likely typo for
`205-TA-006`). If the user meant a different tank, only the table entries in
`build_top_handrails.py` need to change.

## Working baseline

`C:\Users\A\Desktop\jk_tank_edited_by_me_hexbolts.txt` — native E3D data
listing of zone `/WSB_TA`, exported 10 Aug 2026 04:32; the accepted R4
anchor-bolt result (260 bolts). Archived unchanged.

| File | SHA-256 |
|------|---------|
| Original user export (archived `imports/2026-08-10_jk_tank_edited_by_me_hexbolts.txt`) | `B3DC32B9BEDD147CBEA24CDDC9E954434BDF41B289CEA6F5BF3401EC4617EA94` |
| r1 (superseded) `output/WSB_TA_top_handrails_20260810_r1.txt` | `0BB7900177E4A85CAA85559FE93E2838814FE4EBBB663D8E060CA8CA39E0E474` |
| r2 result `output/WSB_TA_top_handrails_20260810_r2.txt` | `4DB5653012D4CA34DA4C104D98E977CA4BF4BF01CF7E58DC7BD1AF942F26B630` |
| Desktop copy `C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails.txt` | same as result |

## Change applied (insertion only)

One new structural block is inserted immediately before the ZONE `/WSB_TA`
closing `END` (original line 12984), after the last EQUIPMENT block, so the
STRUCTURE is created inside the zone:

```
STRUCTURE /TA_TOP_HANDRAILS
├─ FRMWORK /TA_001_TOP
│  └─ HANDRA /TA_001_TOP/HR_001   R 3000, platform U 28200
└─ FRMWORK /TA_056_TOP
   └─ HANDRA /TA_056_TOP/HR_001   R 3250, platform U 27700
```

Each HANDRA (native structural syntax, learned from the structural-area
export `C:\Users\A\Desktop\stuct_learn.txt`):

- `POS` on the east point of the platform rim; `RAILHE 1100mm 550mm`
  (1.1 m top rail per the request, 0.55 m mid rail);
- `POSTSP 1000mm` post spacing;
- closed circular `RPATH` of 4 x 90-degree arcs (`POINTR` + `CURTYP THRU`
  through-points at 45/135/225/315 degrees);
- `RAILSET` with two `RAIL` components, `SPRE SPCOMPONENT /SLH/PIPE48.3x3.6`
  (the handrail tube used in the structural-area native export),
  `ZOFF 1100mm / 550mm`, `RADS true`.

## Preservation set

Everything outside the insertion point is byte-identical: all 22 equipment
blocks (including the 260 anchor bolts and the user's manual edits), all
nozzle `CATR` bindings, `INPUT`/`ERROR` scaffolding. The candidate equals the
original with the new block removed — asserted in `build_top_handrails.py`.
UTF-8 BOM and CRLF are preserved.

## Verification

`build_top_handrails.py` asserts:

- every RPATH point (8 relative points + path start) lies on the platform
  circle, error < 0.02 mm;
- platform radius and elevation match the export (`DTOP` / `HEIG` of the roof
  frustum: TA_001 R 3000 at U 28200, TA_056 R 3250 at U 27700);
- `validate_pml()` reports no new problems vs. the original (231 pre-existing
  native-export findings unchanged; handrail block contributes 0);
- text-level single-insertion proof, BOM + CRLF preserved;
- NEW/END hierarchy balanced: the stack empties exactly once (the ZONE END),
  so no element is created outside its legal owner.

## Reference values and open points

- Rail tube `/SLH/PIPE48.3x3.6`, post spacing 1000 mm and mid-rail 550 mm are
  Reference Values copied from the structural-area native export (stuct_learn).
- Whether the E3D catalogue in this model contains `/SLH/PIPE48.3x3.6` is
  unverified; if the SPRE fails to resolve, the fallback is a primitive-based
  handrail (CYLI posts + EXTRUSION rail segments).
- Circular RPATH + CURVE (`CURTYP THRU`) under HANDRA is supported per AVEVA
  documentation (RPATH legal members include CURVE) but is **not yet verified
  in E3D** — this is the point of the user test.
- `205-TA-006` does not exist; 205-TA-056 is modelled instead. Confirm tag.

## Files

| Path | Purpose |
|------|---------|
| `build_top_handrails.py` | Generator (insertion only, with numerical self-check) |
| `../../imports/2026-08-10_jk_tank_edited_by_me_hexbolts.txt` | Immutable original |
| `../../output/WSB_TA_top_handrails_20260810_r2.txt` | Result for E3D |
| `../../output/WSB_TA_top_handrails_20260810_r1.txt` | r1 (superseded, rejected by E3D) |
| `C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails.txt` | Desktop copy for `$M` |

Load instruction (E3D): select a writable ZONE, then
`$M C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails.txt`.
