# PML 结构建模参考
# =================

## 1. 结构层级

```
FRMWRK (框架)
 ├── GENSEC (通用截面)   -- 梁/柱
 ├── PANEL (面板)        -- 地板/墙
 ├── BRACE (支撑)        -- 斜撑
 ├── STAIR (楼梯)        -- 楼梯
 ├── LADDER (梯子)       -- 爬梯
 └── HANDRAIL (栏杆)     -- 护栏
```

## 2. 创建结构框架

### 2.1 创建柱子
```
!zone = COLLECT 'Q ZONE BY NAME "STRUCT_ZONE"' FIRST
!!CE = !zone

!frame = NEW FRMWRK
!frame.NAME = 'FR-101'
!frame.DESC = 'Pipe Rack'

!!CE = !frame
!col1 = NEW GENSEC
!col1.NAME = 'C-01'
!col1.POSS = EAST 0, NORTH 0, UP 0
!col1.POSE = EAST 0, NORTH 0, UP 12000
!col1.SPRE = 'HEA300'
!col1.JUSL = 'BOTTOM'

!col2 = NEW GENSEC
!col2.NAME = 'C-02'
!col2.POSS = EAST 6000, NORTH 0, UP 0
!col2.POSE = EAST 6000, NORTH 0, UP 12000
!col2.SPRE = 'HEA300'
!col2.JUSL = 'BOTTOM'
```

### 2.2 创建梁
```
!beam1 = NEW GENSEC
!beam1.NAME = 'B-01'
!beam1.POSS = EAST 0, NORTH 0, UP 10000
!beam1.POSE = EAST 6000, NORTH 0, UP 10000
!beam1.SPRE = 'IPE240'
!beam1.JUSL = 'TOP'

!beam2 = NEW GENSEC
!beam2.NAME = 'B-02'
!beam2.POSS = EAST 0, NORTH 3000, UP 10000
!beam2.POSE = EAST 6000, NORTH 3000, UP 10000
!beam2.SPRE = 'IPE240'
!beam2.JUSL = 'TOP'
```

### 2.3 添加斜撑
```
!brace = NEW BRACE
!brace.NAME = 'BR-01'
!brace.POSS = EAST 0, NORTH 0, UP 0
!brace.POSE = EAST 6000, NORTH 0, UP 6000
!brace.SPRE = 'L100X100X10'
```

### 2.4 添加楼板
```
!!CE = !frame
!panel = NEW PANEL
!panel.NAME = 'FL-01'
!panel.POSITION = EAST 0, NORTH 0, UP 10000
!panel.WIDTH = 6000
!panel.DEPTH = 3000
!panel.THICKNESS = 150
!panel.TYPE = 'GRATING'     -- 格栅板
```

## 3. 型材规格 (SPRE) 参考

```
-- H型钢
HEA100, HEA200, HEA300, HEA400, HEA500, HEA600
HEB100, HEB200, HEB300, HEB400, HEB500, HEB600
HEM100, HEM200, HEM300, HEM400, HEM500, HEM600

-- I型钢
IPE80, IPE100, IPE120, IPE140, IPE160, IPE180
IPE200, IPE220, IPE240, IPE270, IPE300, IPE360

-- 槽钢
UPN80, UPN100, UPN120, UPN140, UPN160, UPN180
UPN200, UPN220, UPN240, UPN260, UPN280, UPN300

-- 角钢
L50X50X5, L60X60X6, L75X75X8, L80X80X8, L100X100X10

-- 方管/圆管
SHS50X50X5, SHS80X80X6, SHS100X100X8
CHS88.9X4, CHS114.3X5, CHS168.3X6
```

## 4. 结构属性

```
NAME         -- 名称
POSS         -- 起点
POSE         -- 终点
SPRE         -- 型材规格
JUSL         -- 定位基准: TOP, BOTTOM, CENTRE
MATR         -- 材料
GTYP         -- 几何类型（对 GENSEC 一般为 'CURVEPROFILE'）
CUTL         -- 实际切割长度
WEIGHT       -- 重量
STRUCLASS    -- 结构分类: PRIMARY, SECONDARY, TERTIARY
PAINT        -- 涂层
FIREPROOF    -- 防火
```

## 5. 预埋件 / 锚固
```
!!CE = !frame
!anchor = NEW ANCHOR
!anchor.NAME = 'AN-01'
!anchor.POSITION = EAST 0, NORTH 0, UP 0
!anchor.TYPE = 'BASE_PLATE'
!anchor.WIDTH = 400
!anchor.DEPTH = 400
!anchor.THICKNESS = 25
```
