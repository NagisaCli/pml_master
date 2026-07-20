# PML 设备建模参考
# =================

## 1. 设备类型

| PML 类型    | 说明         | 典型用途       |
|-------------|-------------|---------------|
| EQUIPMENT   | 通用设备     | 所有设备基类   |
| VESSEL      | 容器/塔器    | 储罐、反应器   |
| PUMP        | 泵           | 离心泵、柱塞泵 |
| HEATEX      | 换热器       | 管壳式换热器   |
| COMPRESSOR  | 压缩机       | 离心/往复式    |
| TANK        | 储罐         | 常压储罐       |
| COLUMN      | 塔           | 精馏塔、吸收塔 |
| FILTER      | 过滤器       | 管道过滤器     |
| VALVE       | 阀门（在线）  | 各类阀门       |

## 2. 常用几何类型 (GTYP)

```
CYLINDER     -- 圆柱体
BOX          -- 长方体
SPHERE       -- 球体
CONE         -- 锥体
PYRAMID      -- 棱锥体
DISHEAD      -- 碟形封头
TORISPH      -- 准球形封头
HEMISPH      -- 半球形封头
EXTRUSION    -- 拉伸体
REVOLUTION   -- 旋转体
NOSHAPE      -- 无几何形状
```

## 3. 设备建模步骤

### 3.1 创建基本设备
```
!!CE = !zone
!eqp = NEW EQUIPMENT
!eqp.NAME = 'E-101'
!eqp.DESC = 'Heat Exchanger'
!eqp.GTYP = 'CYLINDER'
!eqp.POSITION = EAST 8000, NORTH 5000, UP 0
!eqp.WIDTH = 1000
!eqp.DEPTH = 1000
!eqp.HEIGHT = 4000
!eqp.ORIENTATION = NORTH
```

### 3.2 带封头的容器
```
!vessel = NEW VESSEL
!vessel.NAME = 'V-101'
!vessel.GTYP = 'CYLINDER'
!vessel.POSITION = EAST 10000, NORTH 6000, UP 0
!vessel.WIDTH = 2000       -- 直径
!vessel.HEIGHT = 6000      -- 筒体高度
!vessel.ORIENTATION = UP
!vessel.DISHEAD = 'TORISPH'  -- 封头类型
!vessel.DISHT = 300          -- 封头厚度
!vessel.HEADS = 'BOTH'       -- 两端封头
```

### 3.3 添加管口 (Nozzle)
```
!!CE = !vessel
!n1 = NEW NOZZLE
!n1.NAME = 'N1'
!n1.POSITION = EAST 0, NORTH 0, UP 5500 WRT !vessel
!n1.DIRECTION = NORTH
!n1.BORE = 200
!n1.OTHR = 250
!n1.FACEL = 350
!n1.RATING = 'CL150'

!n2 = NEW NOZZLE
!n2.NAME = 'N2'
!n2.POSITION = EAST 0, NORTH 0, UP 500 WRT !vessel
!n2.DIRECTION = SOUTH
!n2.BORE = 150
!n2.OTHR = 200
!n2.FACEL = 300
```

### 3.4 设备平台/梯子
```
!!CE = !vessel
!plat = NEW PLATFORM
!plat.NAME = 'PL-01'
!plat.POSITION = EAST 0, NORTH 0, UP 3000 WRT !vessel
!plat.WIDTH = 2500
!plat.DEPTH = 2000
!plat.THICKNESS = 50

!ladder = NEW LADDER
!ladder.NAME = 'LD-01'
!ladder.POSITION = EAST 1200, NORTH 0, UP 0 WRT !vessel
!ladder.HEIGHT = 6000
!ladder.WIDTH = 600
```

## 4. 设备属性参考

```
NAME         -- 名称（必需，唯一）
DESC         -- 描述
GTYP         -- 几何类型
POSITION     -- 位置 (EAST, NORTH, UP)
ORIENTATION  -- 方向
WIDTH        -- X 方向尺寸/直径
DEPTH        -- Y 方向尺寸
HEIGHT       -- Z 方向尺寸
BORE         -- 公称直径（管口）
OTHR         -- 外径
FACEL        -- 法兰面长度
RATING       -- 压力等级
MATR         -- 材料
SPRE         -- 规格引用
WEIGHT       -- 重量
INSUL        -- 保温厚度
PAINT        -- 防腐涂层
TAGNO        -- 位号
```

## 5. 高级：参数化设备（从Excel/CSV批量创建）

PML 支持从外部文件读取批量创建设备：
```
!!FILE OPEN 'equipment_list.csv' FOR READ AS !file
DO WHILE NOT !!FILE.END(!file)
  !line = !!FILE.READ(!file)
  !parts = !!STRING.SPLIT(!line, ',')
  !name = !parts[1]
  !east = !parts[2]
  !north = !parts[3]
  !up = !parts[4]
  
  !eqp = NEW EQUIPMENT
  !eqp.NAME = !name
  !eqp.POSITION = EAST !east, NORTH !north, UP !up
ENDDO
!!FILE.CLOSE(!file)
```
