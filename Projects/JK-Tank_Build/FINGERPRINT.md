# FINGERPRINT — JK-Tank_Build (WSB tanks)

Stable signals used to identify an incoming file as this project **before**
editing. Match several signals, then read `TIMELINE.md` for the current
baseline.

## File-name signals

- `WSB_TA*.txt` — native E3D data listing of the WSB tank area
- `JK-Project*.pml`, `JK_wsb_tanks*.pml` — generated tank macros

## Zone / site signals

- Data listing header contains `NEW ZONE /WSB_TA`

## Element-name signals

- Equipment names follow `<area>_TA_<nnn>` with area ∈ {203, 204, 205}:
  `NEW EQUIPMENT /203_TA_006`, `/204_TA_021`, `/205_TA_052`, …
- Dropleg tags: 203_TA_019, 204_TA_021, 205_TA_016, 205_TA_036, 205_TA_052
- SUBE convention: `<tag>_SUPPORT`, `<tag>_SHELL`, `<tag>_N<n>`, `<tag>_M1`,
  `<tag>_ACCESS`

## Coordinate anchors (E / N, mm)

| Tag | Anchor |
|-----|--------|
| 203_TA_006 | 15000 / 19860 |
| 204_TA_021 | 23650 / 6000 |
| 205_TA_016 | 33833 / 6000 |
| 205_TA_036 | 41833 / 6000 |
| 205_TA_052 | 49838 / 6000 |

## Look-alikes

- `JK_Cooking_Tank_Build` uses descriptive file names, not `TA` tags.
- `JK_Pump_Build` uses `<area>_PU_<nnn>` equipment names.
- `E3D_Syntax_Lab` uses `SITE-PIPING-AREA01` / `ZONE-PIPING-AREA01`.
