# WSB Tank Anchor-Bolt Detail Pass — 2026-08-10 (r3)

**State:** Generated and verified locally; not yet re-imported into E3D.

Revision history:

- r1 — nuts under the plate, bolt circle on the inner plate (rejected).
- r2 — anchor style, nut on the plate top, M30–M48 sizes, bolt circle on the
  exposed annulus; corrected the plate boundary for the tanks whose base ring
  is wider than the inner plate (accepted except for 205-TA-059).
- r3 — the single remaining error fixed: 205-TA-059 anchors on its OUTER
  base ring (DIAM 3000 in SHELL), not the inner ring (DIAM 1800 in SUPPORT).

## Request and corrections

User instruction (2026-08-10):

> Except 044, 019, 021, 016, 036, 052, every tank gets bottom hex bolts.
> Allocate the bolt count by tank scale. The nut must sit tight against the
> bottom plate. Do not touch the rest of the structure.

User corrections after r1:

1. **Bottom-plate boundary was misidentified** — some bolts landed inside
   the shell footprint. The correct boundary is the WIDEST short cylinder at
   the lowest elevation (the exposed base ring / bottom plate); bolts sit on
   its exposed annulus outside the shell wall.
2. **Anchor-bolt style required** — the nut goes on the plate TOP (flush
   against it), and the stud extends DOWN into the foundation; the nut must
   not sit under the plate.
3. **Nut too small visually** — nut size now scales with tank size
   (M30–M48) so the fastener reads as physically plausible.

User correction after r2 (single remaining error):

> 205-TA-059 is the only wrong one — the bolts sit on the INNER plate instead
> of the OUTER one.

205-TA-059 has two base rings: DIAM 1800 × 30 under the inner 1500 skirt in
SUPPORT, and DIAM 3000 × 50 under the outer 2700 shell in SHELL. r2 anchored
on the inner 1800 ring. r3 anchors on the **outer 3000 ring in SHELL**
(bolt circle radius 1400 mm, 50 mm outside the 2700 shell wall); count and
size follow the same scale bands as every other tank: 16 × M36
(previously 8 × M30 on the wrong ring).

## Working baseline

`C:\Users\A\Desktop\jk_tank_edited_by_me.txt` — native E3D data listing of
zone `/WSB_TA`, exported 10 Aug 2026 04:32 (user-edited continuation of the
accepted R3 retrofit baseline). The user's manual edits were preserved
untouched; every revision is insertion-only.

| File | SHA-256 |
|------|---------|
| Original user export (archived `imports/2026-08-10_jk_tank_edited_by_me.txt`) | `33415BC95ECDC70EB3C5355FDBCAA5051BE7B85FD2D7B1E88AC40C5784D151B9` |
| r1 (superseded) `output/WSB_TA_hexbolts_20260810.txt` | `951FA9D1DE1B8E2368B311B712D46F8571F1A2C4D1B2C4DAF85C7114E892FDC7` |
| r2 (superseded) `output/WSB_TA_hexbolts_20260810_r2.txt` | `A91ED2CD2D18FD66338B22990C042C27829D1045EC48FE26995439C4B3E62380` |
| r3 result `output/WSB_TA_hexbolts_20260810_r3.txt` | `B3DC32B9BEDD147CBEA24CDDC9E954434BDF41B289CEA6F5BF3401EC4617EA94` |
| Desktop copy `jk_tank_edited_by_me_hexbolts.txt` (overwritten with r3) | same as r3 result |

## Scope and bolt schedule

16 tanks receive bolts; 6 are excluded byte-identically:
`203_TA_019`, `203_TA_044`, `204_TA_021`, `205_TA_016`, `205_TA_036`,
`205_TA_052`.

| Tag | Host subequipment | 底盘 (plate/ring DIAM, mm) | Bolts | Size |
|-----|-------------------|----------------------------|-------:|------|
| 203_TA_006 | SHELL | 6000 | 20 | M48 |
| 203_TA_024 | SUPPORT | 2300 | 12 | M30 |
| 203_TA_029 | SHELL | 2900 | 12 | M36 |
| 204_TA_001 | SUPPORT | 3500 | 16 | M36 |
| 204_TA_034 | SHELL | 2600 | 12 | M36 |
| 204_TA_035 | SHELL | 5900 | 20 | M42 |
| 205_TA_001 | SHELL | 11100 | 24 | M48 |
| 205_TA_008 | SUPPORT | 2900 | 12 | M36 |
| 205_TA_011 | SHELL | 4300 | 16 | M42 |
| 205_TA_022 | SUPPORT | 3100 | 16 | M36 |
| 205_TA_025 | SUPPORT | 3500 | 16 | M36 |
| 205_TA_029 | SHELL | 3870 | 16 | M36 |
| 205_TA_042 | SUPPORT | 3950 | 16 | M36 |
| 205_TA_045 | SHELL | 3800 | 16 | M36 |
| 205_TA_056 | SHELL | 10200 (added ring) | 20 | M48 |
| 205_TA_059 | SHELL (outer) | 3000 | 16 | M36 |

Total: **260 bolts** (520 new solids) + 1 added base ring for 205_TA_056.

Count bands and size classes (Reference Values): < 2000 mm → 8 × M30;
2000–2999 → 12 × M36; 3000–3999 → 16 × M36; 4000–5999 → 16/20 × M42;
>= 6000 → 20/24 × M48. M30 = AF 46/h 24, M36 = AF 55/h 29, M42 = AF 65/h 34,
M48 = AF 75/h 38.

## Anchor-bolt design

Each bolt is inserted inside the existing SHELL/SUPPORT subequipment, in the
same local coordinate frame as the 底盘:

- **Stud** — `CYLINDER`, DIAM 30/36/42/48, axis U, embedded 8×d below the
  plate bottom and protruding 1×d above the nut top.
- **Nut** — `EXTRUSION` + `LOOP` + 6 `VERTEX` (verified hex form), profile
  plane ON the plate top: nut bottom face flush with the plate top
  ("螺帽紧贴底盘", anchor style). Verified to 0.5 mm for all 260.
- **Bolt circle** — radius = plate/ring radius − 100 mm, on the exposed
  annulus outside the shell wall (>= 40 mm clearance, verified per tank).

### 205_TA_056 — added base ring

This tank has no exposed base ring: its 9900 mm outer shell and 6470 mm inner
shell both start at grade and the inner plate carries no overhang, so anchor
bolts had no physical home. One base ring was added inside its SHELL
subequipment: `CYLINDER` DIAM 10200 × HEIG 50, top flush with the shell
bottom (U 0), matching the cooking-area baseplate convention
(shell DIAM + 300). The bolts sit on this ring at radius 5000 mm.

### 205_TA_059 — outer ring correction (r3)

The r2 schedule pointed 205-TA-059 at the SUPPORT subequipment, whose only
bottom ring is DIAM 1800 under the inner 1500 skirt. The exposed outer ring
is DIAM 3000 × 50 in the SHELL subequipment, under the 2700 outer shell.
r3 moves all 16 bolts there (radius 1400 mm) and upgrades them to M36.

## Preservation set

The user's manual edits (nozzle moves/ORI changes, added INTERNALS,
`AIDGROUP`/`AIDLINE`, equipment POS changes, CATR set) are untouched. Text
diff shows **insertions only**: every original line still occurs in order,
and the six excluded equipment blocks are byte-identical. The only added
non-fastener structure is the 205_TA_056 base ring above.

## Verification

`verify_hex_bolts.py` (same folder) passes:

- 260 nuts, all flush on the plate top (<= 0.5 mm);
- 260 studs, all on the bolt circle (<= 0.5 mm), embedded below the plate and
  protruding above the nut;
- every bolt circle lies >= 40 mm outside the widest shell cylinder in the
  same subequipment (no bolt inside the tank footprint);
- per-tank counts and size classes match the schedule;
- hex profile: 6 vertices, radius per size class;
- 205_TA_056 base ring present (DIAM 10200 × 50, top U 0);
- original lines preserved in order;
- `validate_pml()` clean (PML1 only, no banned forms);
- UTF-8 BOM + CRLF preserved.

## Files

| Path | Purpose |
|------|---------|
| `add_hex_bolts.py` | Generator (insertion only) |
| `verify_hex_bolts.py` | Numerical verifier |
| `../../imports/2026-08-10_jk_tank_edited_by_me.txt` | Immutable original |
| `../../output/WSB_TA_hexbolts_20260810_r3.txt` | Result for E3D |
| `../../output/WSB_TA_hexbolts_20260810_r2.txt` | r2 (superseded) |
| `../../output/WSB_TA_hexbolts_20260810.txt` | r1 (superseded) |
| `C:\Users\A\Desktop\jk_tank_edited_by_me_hexbolts.txt` | Desktop copy (r3) |

Load instruction (E3D): select a writable ZONE, then `$M
C:\Users\A\Desktop\jk_tank_edited_by_me_hexbolts.txt`.
