# JK_Pump_Build — Nozzle Catalogue Component Mapping

Data source: `Projects/JK_Pump_Build/pump_nozzle_modify.xlsx`, `Sheet1!A1:E31`.

## Rules adopted

- `DN_INPUT` maps to the pump suction nozzle (`SUCTION_NOZZLE`); `DN_OUTPUT`
  maps to the pump discharge nozzle (`DISCHARGE_NOZZLE`).
- When an Excel value is not an existing catalogue DN, take the verified DN in
  `ANSI-NOZZLES / 150lb_Ansi_Flanged` with the smallest absolute difference.
- When the two neighbouring DNs are equidistant, take the smaller DN to avoid
  the catalogue component enlarging the original opening. This rule affects
  only `204-PU-017`'s input value `85 mm`, selecting `DN80`.
- Only the native `NOZZLE`'s catalogue binding and nozzle DN comments change;
  the original `POS`, `ORI`, `HEIG`, discharge-neck primitives and all other
  geometry remain unchanged.

## Data quality notes

All 30 rows of Excel's `Specification` are `ANSI-NOZZLES`. The `Generic Type`
column autofills from `150Ib Ansi Flanges` on row 2 to `151Ib` through
`179Ib`; it uses the letter `I` rather than the lowercase `l` used in
pressure classes, and 151–179 lb is not a verified catalogue series in this
project. The source workbook was not rewritten; every pump maps to the
receiving project's verified `150lb Ansi Flanges` / `150lb_Ansi_Flanged`. If
column E originally intended different pressure classes, correct the
workbook first and re-query the receiving E3D project's actual SPCOs.

## Per-pump mapping

| Pump tag | Excel input → catalogue DN | Suction SPCO | Excel output → catalogue DN | Discharge SPCO | Excel column E original |
|---|---:|---|---:|---|---|
| 203-PU-008 | 216 → DN200 (-16) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 151 → DN150 (-1) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 150Ib Ansi Flanges |
| 203-PU-009 | 221 → DN200 (-21) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 151 → DN150 (-1) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 151Ib Ansi Flanges |
| 203-PU-011 | 92 → DN90 (-2) | `/150lb_Ansi_Flanged/AAZFBB0MM` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 152Ib Ansi Flanges |
| 203-PU-020 | 539 → DN500 (-39) | `/150lb_Ansi_Flanged/AAZFBB011` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 153Ib Ansi Flanges |
| 203-PU-026 | 113 → DN125 (+12) | `/150lb_Ansi_Flanged/AAZFBB0PP` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 154Ib Ansi Flanges |
| 203-PU-031 | 59 → DN65 (+6) | `/150lb_Ansi_Flanged/AAZFBB0KK` | 143 → DN150 (+7) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 155Ib Ansi Flanges |
| 204-PU-003 | 216 → DN200 (-16) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 151 → DN150 (-1) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 156Ib Ansi Flanges |
| 204-PU-008 | 108 → DN100 (-8) | `/150lb_Ansi_Flanged/AAZFBB0NN` | 167 → DN150 (-17) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 157Ib Ansi Flanges |
| 204-PU-006 | 108 → DN100 (-8) | `/150lb_Ansi_Flanged/AAZFBB0NN` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 158Ib Ansi Flanges |
| 204-PU-015 | 221 → DN200 (-21) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 159Ib Ansi Flanges |
| 204-PU-016 | 221 → DN200 (-21) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 160Ib Ansi Flanges |
| 204-PU-017 | 85 → DN80 (-5, smaller DN at equal distance) | `/150lb_Ansi_Flanged/AAZFBB0LL` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 161Ib Ansi Flanges |
| 204-PU-023 | 92 → DN90 (-2) | `/150lb_Ansi_Flanged/AAZFBB0MM` | 151 → DN150 (-1) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 162Ib Ansi Flanges |
| 205-PU-004 | 216 → DN200 (-16) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 151 → DN150 (-1) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 163Ib Ansi Flanges |
| 205-PU-012 | 619 → DN600 (-19) | `/150lb_Ansi_Flanged/AAZFBB033` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 164Ib Ansi Flanges |
| 205-PU-013 | 65 → DN65 (0) | `/150lb_Ansi_Flanged/AAZFBB0KK` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 165Ib Ansi Flanges |
| 205-PU-018 | 140 → DN150 (+10) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 161 → DN150 (-11) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 166Ib Ansi Flanges |
| 205-PU-024 | 113 → DN125 (+12) | `/150lb_Ansi_Flanged/AAZFBB0PP` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 167Ib Ansi Flanges |
| 205-PU-027 | 216 → DN200 (-16) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 151 → DN150 (-1) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 168Ib Ansi Flanges |
| 205-PU-030 | 216 → DN200 (-16) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 169Ib Ansi Flanges |
| 205-PU-031 | 221 → DN200 (-21) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 151 → DN150 (-1) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 170Ib Ansi Flanges |
| 205-PU-032 | 216 → DN200 (-16) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 171Ib Ansi Flanges |
| 205-PU-038 | 140 → DN150 (+10) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 167 → DN150 (-17) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 172Ib Ansi Flanges |
| 205-PU-046 | 92 → DN90 (-2) | `/150lb_Ansi_Flanged/AAZFBB0MM` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 173Ib Ansi Flanges |
| 205-PU-047 | 221 → DN200 (-21) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 174Ib Ansi Flanges |
| 205-PU-048 | 216 → DN200 (-16) | `/150lb_Ansi_Flanged/AAZFBB0TT` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 175Ib Ansi Flanges |
| 205-PU-049 | 113 → DN125 (+12) | `/150lb_Ansi_Flanged/AAZFBB0PP` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 176Ib Ansi Flanges |
| 205-PU-054 | 173 → DN150 (-23) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 177Ib Ansi Flanges |
| 205-PU-060 | 113 → DN125 (+12) | `/150lb_Ansi_Flanged/AAZFBB0PP` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 178Ib Ansi Flanges |
| 205-PU-061 | 113 → DN125 (+12) | `/150lb_Ansi_Flanged/AAZFBB0PP` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 179Ib Ansi Flanges |

The delta is defined as `catalogue DN − Excel value`, in millimetres.
