# JK_Pump_Build — 管口目录元件对应表

数据源：`Projects/JK_Pump_Build/pump_nozzle_modify.xlsx`，`Sheet1!A1:E31`。

## 采用规则

- `DN_INPUT` 对应泵吸入口（`SUCTION_NOZZLE`），`DN_OUTPUT` 对应泵排出口（`DISCHARGE_NOZZLE`）。
- Excel 数值不是现有目录 DN 时，取 `ANSI-NOZZLES / 150lb_Ansi_Flanged` 中绝对差值最小的已验证 DN。
- 若上下两个 DN 距离相同，取较小 DN，避免目录元件放大原始开口。该规则只影响 `204-PU-017` 的输入值 `85 mm`，选择 `DN80`。
- 只变更原生 `NOZZLE` 的目录绑定和管口 DN 注释；原有 `POS`、`ORI`、`HEIG`、排出颈部基本体及其他几何保持不变。

## 数据质量说明

Excel 的 `Specification` 30 行均为 `ANSI-NOZZLES`。`Generic Type` 从第 2 行的
`150Ib Ansi Flanges` 连续填充为 `151Ib` 至 `179Ib`；其中使用的是字母 `I`
而不是压力等级中的小写 `l`，且 151–179 lb 不是本项目已验证的目录系列。
本次没有改写源工作簿，所有泵均映射到接收项目已验证的
`150lb Ansi Flanges` / `150lb_Ansi_Flanged`。如 E 列原本意图表达其他压力等级，
应先修正工作簿并重新查询该 E3D 项目的实际 SPCO。

## 逐泵对应

| 泵位号 | Excel 输入 → 目录 DN | 吸入口 SPCO | Excel 输出 → 目录 DN | 排出口 SPCO | Excel E 列原值 |
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
| 204-PU-017 | 85 → DN80 (-5，等距时取小) | `/150lb_Ansi_Flanged/AAZFBB0LL` | 146 → DN150 (+4) | `/150lb_Ansi_Flanged/AAZFBB0RR` | 161Ib Ansi Flanges |
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

差值定义为 `目录 DN - Excel 数值`，单位为 mm。
