# 造纸厂设备建模规范与参数库 (Paper Mill Equipment Modeling Guide)

本文档整理造纸厂全流程设备（制浆备料、造纸机组、化工回收、辅助设施）在 AVEVA E3D 3.1 中的标准建模尺寸、PML1 几何组合模式与管口布置规范。

---

## 1. 制浆备料设备 (Stock Preparation Equipment)

### 1.1 水碎解浆机 (Pulper)
- **设备类型**: `EQUIPMENT` / `VESSEL`
- **主要参数**: 容积 5m³ ~ 80m³ | 槽体直径 φ2000 ~ φ4500mm | 槽体高度 2500 ~ 5000mm
- **E3D 几何组合**:
  - 槽体主体: `NEW CYLI` (DIAM 3200, HEIG 3500)
  - 底部锥形排水斗: `NEW CONE` (DTOP 3200, DBOT 1200, HEIG 800)
  - 转子转盘: `NEW CYLI` (DIAM 1200, HEIG 150)
  - 电机与皮带轮: `NEW BOX` (电机 800×600×700) + `NEW CYLI` (皮带轮 φ500×200)
- **管口布置**:
  - 浆料出口 N1: 底部 CONE 下端 DN300
  - 进水管口 N2: 槽体上部 DN250
  - 废渣排出口 N3: 槽底侧面 DN200

### 1.2 离心除渣器组 (Cleaners Cluster)
- **设备类型**: `EQUIPMENT`
- **高浓/低浓除渣器单体**:
  - 上部圆筒: `NEW CYLI` (DIAM 300, HEIG 600)
  - 下部长锥体: `NEW CONE` (DTOP 300, DBOT 50, HEIG 1500)
  - 进浆口 (切向): `NEW CYLI` (DIAM 80, HEIG 200, 轴沿 E/N)
  - 良浆口 (顶部): `NEW CYLI` (DIAM 100, HEIG 150, 轴沿 U)
  - 尾渣口 (底部): `NEW CYLI` (DIAM 40, HEIG 100, 轴沿 U)
- **多联除渣器总管 (Header Manifold)**:
  - 进浆总管/良浆总管: `NEW CYLI` (DIAM 400 ~ 800, HEIG 3000 ~ 8000)

### 1.3 双盘磨浆机 (Disc Refiner)
- **设备类型**: `EQUIPMENT`
- **几何构成**:
  - 磨头磨室: `NEW CYLI` (DIAM 1200, HEIG 800, 轴沿 E/N)
  - 进浆轴套: `NEW CYLI` (DIAM 400, HEIG 600, 同轴)
  - 驱动电机: `NEW BOX` (XLEN 1800, YLEN 1000, ZLEN 900)
  - 进退刀液压缸: `NEW CYLI` (DIAM 250, HEIG 500)
  - 公共底座: `NEW BOX` (XLEN 3500, YLEN 1400, ZLEN 250)
- **管口**: 进浆口 N1 (轴向入口 DN200), 出浆口 N2 (切向顶出 DN200)

### 1.4 压力筛 (Pressure Screen)
- **设备类型**: `EQUIPMENT`
- **几何构成**:
  - 筛体圆筒: `NEW CYLI` (DIAM 1000 ~ 1600, HEIG 1800 ~ 2800, 轴沿 U)
  - 上盖: `NEW DISH` (DIAM 1000 ~ 1600, HEIG 250, RADIUS 1200)
  - 底部驱动底座: `NEW CYLI` (DIAM 800, HEIG 600) + 电机 `NEW BOX`
- **管口**:
  - 进浆口 N1: 筒体切向 DN250 (U=1200)
  - 良浆口 N2: 筒体侧向 DN300 (U=1600)
  - 重渣口 N3: 底部侧向 DN150 (U=300)
  - 轻渣口 N4: 上盖顶端 DN100 (U=MAX)

### 1.5 盘式浓缩过滤机 (Disc Filter)
- **设备类型**: `EQUIPMENT`
- **主要参数**: 盘片数量 10 ~ 30 盘 | 盘片直径 φ3500 ~ φ5200mm | 总长 6000 ~ 15000mm
- **几何构成**:
  - 过滤槽体 (Vat): `NEW BOX` (XLEN 8000, YLEN 4200, ZLEN 2200) + 下部半圆弧 `NEW CYLI`
  - 中心分配轴: `NEW CYLI` (DIAM 1200, HEIG 8500, 轴沿 E)
  - 滤盘阵列: `NEW CYLI` × 20 (DIAM 4200, HEIG 80, 间隔 350mm)
  - 上部密闭罩壳 (Hood): `NEW BOX` (XLEN 8200, YLEN 4300, ZLEN 1800)

---

## 2. 造纸机组各部套件 (Paper Machine Components)

### 2.1 流浆箱 (Headbox)
- **水力式/气垫式流浆箱**:
  - 锥形进浆总管 (Tapered Header): `NEW CONE` (DTOP 600, DBOT 200, HEIG 5500, 轴沿 N)
  - 阶梯扩散器/管束库: `NEW BOX` (XLEN 400, YLEN 5400, ZLEN 600)
  - 稳浆室/气垫室: `NEW CYLI` (DIAM 800, HEIG 5400, 轴沿 N)
  - 唇板出浆口 (Slice Lip): `NEW BOX` (XLEN 300, YLEN 5300, ZLEN 80, 紧贴网部胸辊)

### 2.2 成型网部 (Fourdrinier Forming Section)
- **胸辊 (Breast Roll)**: `NEW CYLI` (DIAM 800, HEIG 5400, 轴沿 N, E=0)
- **成型板 (Forming Board)**: `NEW BOX` (XLEN 600, YLEN 5400, ZLEN 150)
- **案辊/脱水板 (Table Rolls & Foils)**:
  - 案辊: `NEW CYLI` × 15 (DIAM 320, HEIG 5400)
  - 脱水箱体: `NEW BOX` × 10 (XLEN 400, YLEN 5400, ZLEN 300)
- **水印辊 (Dandy Roll)**: `NEW CYLI` (DIAM 1000, HEIG 5400, 网面上方)
- **真空吸水箱 (Suction Boxes)**: `NEW BOX` × 8 (XLEN 350, YLEN 5400, ZLEN 400, 底部带吸水管口 DN200)
- **伏辊 (Couch Roll)**: `NEW CYLI` (DIAM 1000, HEIG 5400, 带真空吸水箱)

### 2.3 压榨部 (Press Section)
- **大直径盲孔/网眼压榨辊**: `NEW CYLI` (DIAM 1000 ~ 1500, HEIG 5400)
- **花岗岩/橡胶压榨辊**: `NEW CYLI` (DIAM 900 ~ 1300, HEIG 5400)
- **毛布导辊 (Felt Rolls)**: `NEW CYLI` × 20 (DIAM 400 ~ 500, HEIG 5600, 沿毛布环路布置)
- **接水盘 (Catch Pans)**: `NEW BOX` (XLEN 1200, YLEN 5600, ZLEN 300)

### 2.4 干燥部 (Dryer Section)
- **烘缸组 (Dryer Cylinders)**:
  - 标准缸径: φ1500mm 或 φ1800mm | 缸面宽: 5200 ~ 9500mm
  - 铸铁烘缸: `NEW CYLI` (DIAM 1500/1800, HEIG 5400, 轴沿 N)
  - 缸盖: `NEW DISH` × 2 (DIAM 1500, HEIG 120, 扣在两端)
  - 蒸汽安全头 (Rotary Joint): `NEW CYLI` (DIAM 250, HEIG 350, 传动侧轴端 DN80)
  - 双层错位布置: 下排烘缸标高 U=2800, 上排烘缸标高 U=5000, 间距 E=2400mm
- **密闭气罩 (Canopy Hood)**: `NEW BOX` (XLEN 35000, YLEN 6500, ZLEN 4500, 覆盖整个干燥部上方)

### 2.5 施胶机 / 压光机 / 卷纸机
- **斜式施胶机 (Size Press)**: 双辊 `NEW CYLI` (DIAM 900, HEIG 5400) 45° 倾斜对压
- **压光机 (Calender Stack)**: 4 ~ 8 辊垂直重叠 `NEW CYLI` (DIAM 600 ~ 900)
- **卷纸机 (Pope Reel)**: 卷纸缸 `NEW CYLI` (DIAM 1100, HEIG 5400) + 退纸架 + 纸卷卷芯

---

## 3. 化工回收与蒸煮设备 (Pulping & Recovery)

### 3.1 连续蒸煮锅 (Continuous Digester)
- **设备类型**: `VESSEL` / `COLUMN`
- **主要尺寸**: 直径 φ4500 ~ φ6500mm | 高度 35.0m ~ 65.0m
- **E3D PML1 几何构建**:
  - 上封头: `NEW DISH` (DIAM 5500, HEIG 1200, RADIUS 5500)
  - 筒体分段: `NEW CYLI` × 8 (DIAM 5500, HEIG 6000)
  - 下部锥形底: `NEW CONE` (DTOP 5500, DBOT 1500, HEIG 3500)
  - 吹出搅拌器底座: `NEW CYLI` (DIAM 1500, HEIG 800)
- **管口**:
  - 木片入口 N1: 上封头 DN400
  - 蒸煮液循环口 N2~N8: 沿高度方向分布 DN250/DN300
  - 浆料吹出口 N9: 锥底 DN300

### 3.2 吹出罐 (Blow Tank)
- **设备类型**: `VESSEL`
- **尺寸**: 直径 φ6000 ~ φ9000mm | 高度 12.0m ~ 18.0m
- **几何**: 直立 `NEW CYLI` (DIAM 7500, HEIG 12000) + 锥底 `NEW CONE` (DTOP 7500, DBOT 1200, HEIG 2500) + 顶部切向进浆管 DN500

### 3.3 黑液降膜蒸发器 (Black Liquor Evaporator)
- **设备类型**: `HEATEX` / `VESSEL`
- **几何**:
  - 蒸发器加热室: 直立 `NEW CYLI` (DIAM 2800, HEIG 8000)
  - 分离室: `NEW CYLI` (DIAM 3800, HEIG 4500)
  - 二次蒸汽管道: `NEW CYLI` (DIAM 1200, 轴沿 E/U)
