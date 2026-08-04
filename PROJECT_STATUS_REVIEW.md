# 项目状态审查清单 — 2026-08-04

供逐一审查使用。测试基线：**264 passed / 2 skipped**。

## 0. 工作区卫生

- 当前 git 有大量未提交改动 + 未跟踪目录（`Projects/E3D_Syntax_Lab/`、
  `Projects/JK-Tank_Build/`、`Projects/JK_Cooking_Tank_Build/`、
  `Projects/JK_Pump_Build/` 的新文件、新 builder/测试/知识文件）。
- 审查完成后建议整体提交一次，作为本轮工作快照。

## 1. E3D_Syntax_Lab — 语法实验室（已实质完成）

### EXTRUSION 研究 — 已闭环

| 候选 | 结论 | 证据 |
|---|---|---|
| 01 | VERIFIED：POS=轮廓端面，HEIG 沿 +Z | 用户实测 U 1000–1800 |
| 02 | 已测：同轴；上头比原生高 10 mm | Q ATT + 原生对照 |
| 03 | VERIFIED：POS→ORI 与 ORI→POS 顺序无关 | 占用范围一致 |
| 04 | VERIFIED：双头接触契约（下头内缩 10 mm、上头齐平） | 用户目视“EXTR完美” |

### PIPE 研究 — 核心与高级家族全部有实测结论

| 候选 | 内容 | 结论 |
|---|---|---|
| 01–07 | 直管、斜管 1:100、弯头、变径、TEE/B2 互引 | 轮次 1–2 VERIFIED |
| 08 | 组合平衡簇（四路由同 ZONE） | 重提 VERIFIED（“不复杂”）；崩溃=应用/插件级 |
| 09/10 | 崩溃隔离两半 | VERIFIED（09 Q ATT 全对、10 HBore/TBore=100/80） |
| 11 | 高密度全组件 | 隔离（/FIRE 未定义、组件未成路由）→ 由 14–17 取代 |
| 13 | TEE CREF + GASKET 查询套件 | VERIFIED：CREF=/CODEX-Q13-TEE/B2；GASKET Height 0mm 零厚度标记 |
| 14 | FILTER/CLOSURE/FBLIND/COUPLING/WELD | VERIFIED（导入正常、组件显示） |
| 15 | BEND/OLET/PTAPPING+PIPCARTESIAN | VERIFIED（含 45° 弯头、/General-Tappings 解析成功） |
| 16 | B1/B2/B3 网络 + TEE2/OLET 互引（连接优先） | VERIFIED |
| 17 | CAP（/FIRE） | GATED：`(2,109) Undefined name /FIRE`，与预期一致；等项目补 /FIRE |

剩余证据缺口（需要新的原生样本，非写宏可补）：
`VTWAY`、路由平面/Router 命令、保温绝缘继承、`INPRTR/OUPRTR` 元数据。

## 2. JK-Tank_Build — WSB 罐区（22 台）

- 历史基线：22 台、451 primitives、114 nozzles（JK-Project）。
- **dropleg 外观改造 R3 — 已确认（2026-08-04）**
  - 交付：`Projects/JK-Tank_Build/output/WSB_TA_dropleg_retrofit_20260804_r3.txt`
  - R1→R3：四段筒体（总高 9986）+ 每台新增东向 DN200 下管口；
    R2 删除 ACCESS 与原有管口；R3 修正管口 ORI 为 `Y is S and Z is U`。
  - 顶部管口超高与侧向管口悬空：由用户手动调整并确认，项目无遗留问题。

## 3. JK_Cooking_Tank_Build — 煮浆罐（15 台）

- R5（2026-07-30）目视接受，为已接受基线。
- **R6 原生导出改造 — 已确认（2026-08-04）**
  - 14 台加 50 mm 底座板（直径=筒体+300）；10 台精简支撑、348 颗螺栓内移；
    ACCUMULATOR/AID_1/AID_2 保留裙座；4 台未动。
  - 注意：三个改造脚本对当前文件重跑会损坏，需先恢复归档备份。

## 4. JK_Pump_Build — 泵批（30 台）

- 2026-07-29 组合宏已加载并目视确认（当前基线）。
- **2026-07-30 修正版 — 已确认（2026-08-04 E3D 重载接受）**
  - 每台删除 BEARING_FRAME 末两个浮空件 + COUPLING 末两个支撑脚（共 4 个）；
  - 60 个管口按实测开口映射到目录 DN（见 `JK_Pump_Build_nozzle_mapping.md`）；
  - 静态/数值校验通过，E3D 重载已确认。
- 3 台缺俯视图（203-PU-020 / 205-PU-004 / 205-PU-032）→ 保持 UNCONFIRMED。
- 源工作簿 `Generic Type` 151Ib–179Ib 自动填充异常：已记录、未改源。

## 5. 待你提供的输入

- 无（桌面 `泵中线基准.txt` 等未提及文件按约定忽略，不纳入系统工作）。

## 6. 工作约定（2026-08-04 起）

1. **默认没问题**：用户未主动提出问题 = 交付被接受；不来回确认。
2. **删除纪律**：原生导出/手工基线的延续工作中，疑似多余的部分先保留并
   提交审查，只有用户明确要求删除时才删。
3. 未提及的桌面/外部文件不纳入工作范围，专注仓库内系统工作。

## 7. 建议的下一步

1. 本轮工作提交（git commit）——三项目确认已全部写回，工作区待提交。
2. E3D_Syntax_Lab 保持完成状态；CAP（q17）待项目补 `/FIRE` 后再收。
