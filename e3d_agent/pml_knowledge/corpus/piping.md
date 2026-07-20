# PML 管道建模参考
# =================

## 1. 管道层级结构

```
PIPE (管道)
 ├── SCTN (管段)     -- 直管段
 ├── BRAN (分支)     -- 分支
 ├── BEND (弯头)     -- 弯头
 ├── TEE (三通)      -- 三通
 ├── REDUCER (大小头) -- 变径
 ├── VALVE (阀门)    -- 阀门
 ├── FLANGE (法兰)   -- 法兰
 ├── GASKET (垫片)   -- 垫片
 └── BOLTSET (螺栓)  -- 螺栓组
```

## 2. 创建管道系统

### 2.1 创建主管道 (PIPE + SCTN)
```
!zone = COLLECT 'Q ZONE BY NAME "PIPING_ZONE"' FIRST
!!CE = !zone

!pipe = NEW PIPE
!pipe.NAME = 'P-001'
!pipe.DESC = 'Cooling Water Line'
!pipe.SPRE = 'CS_SCH40_CL150'
!pipe.BORE = 100
!pipe.PRESS = '150'        -- 压力等级
!pipe.TEMP = '100'         -- 设计温度
!pipe.SERV = 'CW'          -- 介质代号

!!CE = !pipe
!sctn = NEW SCTN
!sctn.NAME = 'S-001'
!sctn.BORE = 100
!sctn.POSS = EAST 5000, NORTH 3000, UP 4500
!sctn.POSE = EAST 15000, NORTH 3000, UP 4500
!sctn.JUSL = 'BOP'         -- Bottom Of Pipe
!sctn.ROUTE = 'HORIZ'      -- 路由方向
```

### 2.2 创建弯头和分支
```
!sctn1 = COLLECT 'Q SCTN BY NAME "S-001"' FIRST
!!CE = !sctn1

!bend = NEW BEND
!bend.BORE = 100
!bend.ANGLE = 90
!bend.RADIUS = 150
!bend.DIRECTION = UP

!sctn2 = NEW SCTN
!sctn2.NAME = 'S-002'
!sctn2.BORE = 100
!sctn2.POSS = EAST 15000, NORTH 3000, UP 4500
!sctn2.POSE = EAST 15000, NORTH 3000, UP 7000

!tee = NEW TEE
!tee.BORE = 100
!tee.BORE2 = 50
!tee.POSITION = EAST 15000, NORTH 3000, UP 4500
```

### 2.3 添加阀门和管件
```
!!CE = !sctn1
!valve = NEW VALVE
!valve.NAME = 'V-001'
!valve.BORE = 100
!valve.SPRE = 'GATE_VALVE_CL150'
!valve.POSITION = EAST 10000, NORTH 3000, UP 4500
!valve.ACTUATOR = 'MANUAL'
!valve.OPR = 'HW'           -- Handwheel

!flange = NEW FLANGE
!flange.NAME = 'FL-001'
!flange.BORE = 100
!flange.RATING = 'CL150'
!flange.FACETYPE = 'RF'     -- Raised Face
```

## 3. 管道属性参考

```
NAME         -- 名称
DESC         -- 描述
BORE         -- 公称直径 (DN/mm)
OTHR         -- 外径
WT           -- 壁厚
SPRE         -- 规格引用（Pipe Spec）
MATR         -- 材料
POSS         -- 起点坐标 (EAST, NORTH, UP)
POSE         -- 终点坐标
JUSL         -- 定位基准: BOP(管底), COP(管心), TOP(管顶)
CUTL         -- 切割长度
ROUTE        -- 路由方向: HORIZ, VERT, INCLINED
TEMP         -- 设计温度
PRESS        -- 设计压力
SERV         -- 介质代号
INSUL        -- 保温厚度
TRACING      -- 伴热类型
TESTPRESS    -- 试验压力
PAINT        -- 防腐涂层
```

## 4. 规格引用 (SPRE) 说明

规格引用连接设计模型到 Catalogue 中的管道等级：
```
'CS_SCH40_CL150'   -- 碳钢 Sch40 150磅级
'SS_SCH10S_CL150'  -- 不锈钢 Sch10S 150磅级
'CS_SCH80_CL300'   -- 碳钢 Sch80 300磅级
```

规格决定了：
- 允许的管径范围
- 匹配的管件类型
- 壁厚系列
- 材料要求
- 阀门类型

## 5. 管道连接命令

```
!pipe1.CONNECT !pipe2       -- 连接两条管道
!branch.ATTACH !parent      -- 分支连接到主管
!sctn.ALIGN !target         -- 对齐到目标
!sctn.JOIN !target          -- 连接到目标管口
```

## 6. 管道应力接口 (PSI)
```
!pipe.EXPORT_PSI 'file.psf'     -- 导出应力分析文件
!pipe.IMPORT_PSI 'file.psf'     -- 导入应力分析结果
```

## 7. PML 管道导管布线 (Pipe Routing)
```
-- 自动路由
!route = !!Route.Create(!start_point, !end_point)
!route.SPRE = 'CS_SCH40'
!route.CLR = 25              -- 间距 (mm)
!route.AVOID !obstruction    -- 避开障碍
!route.EXECUTE
```
