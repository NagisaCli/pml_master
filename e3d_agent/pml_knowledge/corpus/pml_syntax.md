# PML 语法参考 — E3D 3.1 实测验证版
# =========================================
# ⚠️ 以下语法经 E3D Design Mk3.1.11.0 实际加载验证通过。
#    未经验证的 PML2 语法（!!Alert, COLLECT...FIRST, UNSET, ENDS, 变量赋值）会直接报错。

## 0. 唯一正确的 EQUIPMENT 创建语法（已实机验证）

```
NEW EQUI /EQUIPMENT_NAME          ← 内联命名，/ 前缀必须
NEW CYLI                          ← 子几何体：圆柱
DIAM 1500                         ← 属性无 = 号
HEIG 5200
ORI Z IS N AND Y IS U             ← 【关键】：方向设定必须在 POS 之前！
POS E 0 N 0 U 3500               ← 位置设定 (先 ORI 后 POS，保障几何不旋转漂移)

NEW EQUI /NEXT_EQUIPMENT           ← 下一个 EQUI 隐式关闭上一个
NEW BOX                           ← 子几何体：长方体
XLEN 1500
YLEN 5400
ZLEN 1000
POS E -1500 N 0 U 4100
```

### 核心规则
- **只用 `NEW EQUI /NAME`** — 不用 `NEW EQUIPMENT` + `NAME = '...'`
- **无 ENDS** — 下一个 `NEW EQUI /` 自动结束前一个块
- **无 `=` 号** — 属性命令模式：`DIAM 1500` 不是 `DIAM = 1500`
- **无变量赋值** — 不用 `!var = NEW ...`、`!var.ATTR = ...`
- **不创建 SITE/ZONE** — 用户先在 Model Explorer 中手动选中 ZONE
- **无 !!CE / COLLECT / !!Alert / $P / UNSET / !!WORLD**

### 属性命令一览
| 属性 | 语法 | 说明 |
|------|------|------|
| 直径 | `DIAM 1500` | CYLI 直径 mm |
| 高度/长度 | `HEIG 5200` | CYLI 高度 mm |
| 长/宽/高 | `XLEN 1500` `YLEN 5400` `ZLEN 1000` | BOX 尺寸 mm |
| 位置 | `POS E 0 N 0 U 4100` | EAST/NORTH/UP mm |
| 方向 | `ORI Y IS N AND Z IS U` | Y轴指N, Z轴指U (横向辊) |
| 方向 | `ORI Y IS E AND Z IS U` | Y轴指E, Z轴指U (纵向辊) |
| 描述 | `DESC 'text'` | 可选注释 |

### 禁止的 PML2 语法（会报 Syntax error / Function not found）
```
❌ !!Alert('...')      → 删掉或改用 -- 注释
❌ $P ...              → 删掉或改用 -- 注释  
❌ !var = NEW SITE     → 不在宏中创建 SITE/ZONE
❌ !var = NEW EQUIPMENT → 用 NEW EQUI /NAME
❌ NAME = '...'        → 用 NEW EQUI /NAME 内联命名
❌ DESC = '...'        → 用 DESC '...' 无等号
❌ COLLECT 'Q ...' FIRST → 不支持
❌ IF UNSET(!var)      → 不支持
❌ IF (ARRAYSIZE ...)  → 不支持
❌ !!CE = ...          → 不支持
❌ !!WORLD             → 不支持
❌ END EQUI            → 不用，下一行 NEW EQUI / 自动关闭
❌ ENDS                → 不用
```

## 1. 基本语法

### 注释
```
-- 单行注释
!-- 另一种注释形式
```

### 变量
```
!var_name = 100                     -- 数值变量
!var_name = 'STRING'                -- 字符串变量
!var_name = TRUE                    -- 布尔值
!ref = !!CE                         -- 对象引用（当前元素 Current Element）
!db_ref = !element.dbref()          -- 数据库引用
```

### 条件判断
```
IF condition THEN
  -- do something
ELSEIF condition THEN
  -- do something else
ELSE
  -- fallback
ENDIF
```

### 循环
```
DO !i FROM 1 TO 10
  -- loop body
ENDDO

FOREACH !elem IN !collection
  -- process each
ENDFOREACH
```

### 函数定义
```
!function_name(FUNCTION !arg1, !arg2)
  -- function body
  RETURN !result
ENDFUNCTION
```

### 错误处理
```
ON ERROR
  -- error handler
  -- !ERROR.STATUS, !ERROR.TEXT 获取错误信息
ENDERROR

-- 或使用 TRY/CATCH
!!TRY
  -- risky code
!!CATCH
  -- handle error
!!ENDTRY
```

## 2. 数据库操作

### 创建元素
```
!new_elem = NEW ELEMENT_TYPE
!new_elem.NAME = 'UNIQUE_NAME'
```

### 常用元素类型
```
WORLD          -- 世界（根）
SITE           -- 场地
ZONE           -- 区域
FRMWRK         -- 框架
EQUIPMENT      -- 设备
VESSEL         -- 容器
PUMP           -- 泵
NOZZLE         -- 管口
PIPE           -- 管道
SCTN           -- 管段（Section）
BRAN           -- 分支
BEND           -- 弯头
GENSEC         -- 通用截面（结构）
PANEL          -- 面板
SUBSTN         -- 子结构
CABLE          -- 电缆
TRAY           -- 电缆桥架
```

### 属性设置
```
!elem.NAME = 'V-101'
!elem.DESC = 'Reactor Vessel'
!elem.POSITION = EAST 5000, NORTH 2000, UP 300
!elem.POSS = EAST 0, NORTH 0, UP 0        -- 管段起点
!elem.POSE = EAST 10000, NORTH 0, UP 0    -- 管段终点
!elem.BORE = 150                           -- 公称直径(mm)
!elem.OTHR = 200                           -- 外径(mm)
!elem.WT = 8                               -- 壁厚(mm)
!elem.WIDTH = 2000                         -- 宽度
!elem.DEPTH = 2000                         -- 深度
!elem.HEIGHT = 5000                        -- 高度
!elem.SPRE = 'CS_SCH40_CL150'             -- 规格引用
!elem.MATR = 'CS_A106_GRB'                -- 材料引用
!elem.JUSL = 'BOP'                         -- 定位基准
!elem.GTYP = 'CYLINDER'                    -- 几何类型
!elem.CUTL = 6000                          -- 切割长度
```

### 位置定位
```
-- 绝对坐标
!elem.POSITION = EAST 5000, NORTH 3000, UP 0

-- 相对坐标（相对于当前元素）
!elem.POSITION = EAST 1000, NORTH 0, UP 0 WRT !reference

-- 方向
!elem.DIRECTION = NORTH                    -- 方向
!elem.ORIENTATION = EAST 45, NORTH 45     -- 朝向
```

## 3. 集合与查询

### Q 查询
```
!collection = COLLECT 'Q SITE BY NAME "MY_SITE"'
!collection = COLLECT 'Q ZONE BY NAME "AREA_100"'
!collection = COLLECT 'Q EQUIPMENT BY NAME "V-*"'

-- 获取子元素
!children = !element.MEMBER
!children = !element.BELOW
```

### 循环处理集合
```
FOREACH !item IN !collection
  !name = !item.NAME
  !type = !item.ACTTYPE
  !east = !item.EAST
ENDFOREACH
```

## 4. 常用建模模式

### 创建设备
```
!zone = COLLECT 'Q ZONE BY NAME "AREA_100"' FIRST
!!CE = !zone

!tank = NEW VESSEL
!tank.NAME = 'T-101'
!tank.DESC = 'Storage Tank'
!tank.POSITION = EAST 5000, NORTH 3000, UP 0
!tank.WIDTH = 2000
!tank.DEPTH = 2000
!tank.HEIGHT = 5000
!tank.GTYP = 'CYLINDER'
```

### 创建管口
```
!vessel = COLLECT 'Q VESSEL BY NAME "T-101"' FIRST
!!CE = !vessel

!nozzle = NEW NOZZLE
!nozzle.NAME = 'N1'
!nozzle.POSITION = EAST 0, NORTH 0, UP 2000 WRT !vessel
!nozzle.DIRECTION = NORTH
!nozzle.BORE = 150
!nozzle.OTHR = 200
!nozzle.FACEL = 300
```

### 创建管道
```
!zone = COLLECT 'Q ZONE BY NAME "PIPING_ZONE"' FIRST
!!CE = !zone

!pipe = NEW PIPE
!pipe.NAME = 'P-001'
!pipe.SPRE = 'CS_SCH40_CL150'
!pipe.BORE = 100

!!CE = !pipe
!sctn = NEW SCTN
!sctn.NAME = 'S-001'
!sctn.POSS = EAST 5000, NORTH 3000, UP 4500
!sctn.POSE = EAST 15000, NORTH 3000, UP 4500
!sctn.BORE = 100
```

### 创建钢结构
```
!zone = COLLECT 'Q ZONE BY NAME "STRUCT_ZONE"' FIRST
!!CE = !zone

!frame = NEW FRMWRK
!frame.NAME = 'FR-01'

!!CE = !frame
!beam = NEW GENSEC
!beam.NAME = 'B-01'
!beam.POSS = EAST 0, NORTH 0, UP 0
!beam.POSE = EAST 6000, NORTH 0, UP 0
!beam.SPRE = 'IPE300'
!beam.JUSL = 'TOP'
```

## 5. 报告与输出
```
-- 生成报告
!report = REPORT 'PIPE' WITH 'NAME, BORE, SPRE'

-- 写入文件
!!WRITE 'output.txt' ('Pipe: ' + !pipe.NAME)
```

## 6. 与 .NET 互操作
```
-- 调用 .NET 方法
!result = !!DotNetCall('MyAssembly.MyClass.MyMethod', !arg1, !arg2)

-- 加载 .NET 程序集
!!DotNetLoad('C:\\Path\\To\\Assembly.dll')

-- 创建 .NET 对象
!obj = !!DotNetNew('System.Collections.ArrayList')
```

## 7. 项目特定约定（从本项目提取）

### 命令环境变量
```
ACP000, APS000, AMS000  -- 数据库路径
ACP000ID=ProjACP        -- 项目标识
APS000ID=ProjAPS
AMS000ID=ProjAMS
```

### 命名规则
```
-- 支撑命名
Prefix: \PS  Index: \ 2025  IWidth: \ 5

-- 系统默认目录
/MDS-Drawing-Templates       -- 图纸模板
/MDS-ABA-Area-Library        -- 区域库
/PROJ/ABA/CLASS              -- 分类
/MDS-Drawing-Templates       -- 绘图模板
```

### 工具提示展示的属性字段
```
ACTTYPE     -- 实际类型
SPRE        -- 规格引用
JUSL        -- 定位基准
MEMLINE     -- 成员线
JLINE       -- 连接线
MATR        -- 材料引用
GTYP        -- 几何类型
STRUCLASS   -- 结构分类
CUTL        -- 切割长度
POSS/POSE   -- 起点/终点坐标
```
