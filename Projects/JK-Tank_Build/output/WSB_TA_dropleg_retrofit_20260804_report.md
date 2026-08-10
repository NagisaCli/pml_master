# WSB_TA.txt — DROPLEG Appearance Retrofit Report (2026-08-04)

## Files

- Deliverable: `C:\Users\A\Desktop\WSB_TA.txt` (retrofitted in place)
- Delivery copy: `Projects/JK-Tank_Build/output/WSB_TA_dropleg_retrofit_20260804.txt`
- Original backup (unchanged, SHA-256 verified):
  `Projects/JK-Tank_Build/imports/2026-08-04_WSB_TA.txt`
  `26A99DD4BB7B19B96F3C7CE1486B185C161FB7D858A68F4EC72599FB00A4B45B`

## Scope of changes

Only the appearance of the 5 DROPLEG units was changed (SUPPORT/SHELL
geometry) and a DN200 lower nozzle added per unit; the other 17 units and the
target units' original nozzles (N1–N3/M1), ACCESS and catalogue bindings were
not modified.

| Equipment | Bottom centre (unchanged) | New nozzle |
|---|---|---|
| 203_TA_019 | E 15445 / N 6415 / U 0 | N6 (DN200) |
| 204_TA_021 | E 23650 / N 6000 / U 0 | N4 (DN200) |
| 205_TA_016 | E 33833 / N 6000 / U 0 | N4 (DN200) |
| 205_TA_036 | E 41833 / N 6000 / U 0 | N4 (DN200) |
| 205_TA_052 | E 49838 / N 6000 / U 0 | N4 (DN200) |

## New appearance: four cylinders from bottom to top

| Section | Diameter mm | Height mm | U range | Centre U (POS) |
|---|---|---|---|---|
| 1 base | 1246 | 100 | 0–100 | 50 |
| 2 lower shell | 1006 | 4991 | 100–5091 | 2595.5 |
| 3 transition ring | 1044 | 10 | 5091–5101 | 5096 |
| 4 upper shell | 610 | 4885 | 5101–9986 | 7543.5 |

Geometry written per the CYLI geometric-centre POS rule; all five units
verified: bottom U=0, four sections continuous without gaps, axis E/N
identical to the original coordinates, total height 9986.

## New DN200 nozzle

- Direction: east (90°), on the lower shell (D1006), elevation U 500
- Flange-face coordinate: per unit `centre E + 753 / centre N / U 500`
  (D1006 radius 503 + projection 250; HEIG 350, penetration 100, per IR-9a)
- Default parameters: DN200, HEIG 350, 150 lb ANSI flange
  `CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0TT`
- Matching reinforcing pad: D420 × 30, consistent with existing pads in the
  file
- Catalogue binding appended in the trailing OLD pass per this file's native
  export format

## Reference Values (assumptions)

1. New nozzle elevation U500, east-facing: the user only asked for "a suitable
   lower location"; this position is the selected value.
2. Nozzle "default parameters": inherited from the project generator
   defaults — DN200/HEIG 350/150lb ANSI/pad D420×30.
3. Transition ring modelled as given by the user (D1044×10); no top cover,
   cone or other detail without a dimensional basis was added.

## Issues to confirm

**Resolved (2026-08-04, user confirmed).** Top nozzles exceeding the new
shell (203 N5 height 514; 204/205 N1/N3 heights 2154/2714) and side nozzles
floating because they were laid out at the original D2000 radius were
manually adjusted by the user and confirmed; the ACCESS and original-nozzle
deletions were explicitly instructed by the user (R2).

> Convention (from 2026-08-04): for parts that look "superseded by new
> geometry", keep them and submit for review first; delete only when the user
> explicitly asks.

## Loading

Keep the original Data Listing format (`INPUT BEGIN` / `INPUT FINISH`) and
re-load it the same way as before.

## Revision R2 (2026-08-04, per follow-up user instruction)

- Deleted the ACCESS subequipment of the 5 DROPLEG units and all original
  nozzles except the new DN200:
  - 203_TA_019: delete N1–N5, M1, ACCESS; keep N6 (DN200)
  - 204_TA_021 / 205_TA_016 / 205_TA_036 / 205_TA_052: delete N1–N3, ACCESS;
    keep N4 (DN200)
- Deleted the corresponding 17 catalogue bindings in the trailing OLD pass
  (114 → 97, no duplicates).
- Each unit now has only SUPPORT, SHELL and the new DN200 subequipment; shell
  geometry unchanged.
- R2 delivery copy: `Projects/JK-Tank_Build/output/WSB_TA_dropleg_retrofit_20260804_r2.txt`
- R1 version retained at `WSB_TA_dropleg_retrofit_20260804.txt`, rollback
  possible.

## Revision R3 (2026-08-04, nozzle orientation correction)

The new DN200 nozzles (203_TA_019_N6 / 204_TA_021_N4 / 205_TA_016_N4 /
205_TA_036_N4 / 205_TA_052_N4) had their ORI changed from `Y is E and Z is U`
to `Y is S and Z is U` — in this data-listing export, a side nozzle's `Y` is
the roll reference perpendicular to the aim direction: north-facing nozzles
use `Y is E`, east-facing nozzles should use `Y is S` (consistent with the
file's 203_TA_019_N3). Position (east side, U500) unchanged; everything else
identical to R2.

R3 delivery copy: `Projects/JK-Tank_Build/output/WSB_TA_dropleg_retrofit_20260804_r3.txt`
