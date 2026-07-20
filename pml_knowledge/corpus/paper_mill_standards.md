# 造纸厂车间布置与空间坐标系标准 (Paper Mill Layout & Coordinate Standards)

本文档规定造纸车间（造纸厂房、制浆车间、化工回收区）在 E3D 中的三维空间坐标系设定、车间布置方位、造纸机中心线对齐规范与通道安全净空。

---

## 1. 造纸车间空间坐标系 (Coordinate System Setup)

造纸车间采用 AVEVA E3D 右手直角坐标系，约定如下：

| 世界轴 | 造纸工程含义 | 方向定义 | 车间代表方向 |
|--------|-------------|---------|-------------|
| **EAST (+E)** | 纸机运行线 (Machine Line) | 纸页出纸运行方向 | 湿端流浆箱 (E=0) → 压榨 → 干燥 → 卷纸机 (E=60000+) |
| **NORTH (+N)** | 操作侧 (Operating Side) / 传动侧 (Drive Side) | 垂直于纸机线 | `+N` 为操作侧 (OS), `-N` 为传动侧 (DS) |
| **UP (+U)** | 车间标高 (Elevation) | 垂直向上 | 地面 `U=0`, 操作平台 `U=4500mm`, 地下室 `U=-4000mm` |

---

## 2. 造纸车间多层标高规划 (Building Elevations)

典型的多层造纸车间（Two-Floor Paper Mill Layout）：

```text
U = 18000mm  ▲ 屋架下弦 / 天车轨顶 (Crane Hook Clearance)
             │ 
U = 9000mm   ▲ 密闭气罩排风/二次蒸汽管道标高
             │
U = 4500mm   ▲ 造纸车间主操作层 (Operating Floor)
             │   包含: 纸机本体、流浆箱、控制室、走台
U = 0mm      ▲ 厂房零点地面 (Ground Floor)
             │   包含: 浆池、水力碎浆机、白水槽、泵房、离心除渣器
U = -4500mm  ▲ 地下室 / 损纸池 (Basement / Broke Pit)
```

---

## 3. 传动侧与操作侧布置规范 (OS / DS Layout)

1. **传动侧 (Drive Side, -N 侧)**:
   - 布置纸机主减速机、驱动电机、蒸汽接头与分汽缸、润滑油站。
   - 传动侧维修通道净宽: **≥ 2500mm**。
2. **操作侧 (Operating Side, +N 侧)**:
   - 布置控制操作台、换网/换毛布吊装空间、换辊通道。
   - 操作侧通道净宽: **≥ 3500mm**。

---

## 4. 净空与安全通道标准 (Clearance & Safety Maintenance)

- **主干道与吊装通道**: 净宽 ≥ 4000mm，净高 ≥ 4500mm (供叉车与装载机通行)。
- **设备操作走台 (Walkways)**: 宽 800 ~ 1200mm，护栏高 1100mm，踢脚板高 150mm。
- **管道过道净空**: 跨越通道的管道底包保温层下沿距地面/走台净高 **≥ 2200mm**。
- **泵与设备检修间距**: 泵体与墙壁或邻近泵净距 **≥ 1200mm**。

---

## 5. 造纸厂 3D 模型 PML1 命名规范 (Naming Conventions)

所有的 E3D 节点名称在数据库中必须唯一，格式：
`/<区域>_<设备类型>_<位号>`

### 示例:
- 水碎解浆机: `/PM1_PULP_HYDRAPULPER_01`
- 双盘磨浆机: `/PM1_PULP_REFINER_01`
- 流浆箱: `/PM1_PM_HEADBOX_01`
- 烘缸组第 1 缸: `/PM1_DRYER_CYLINDER_01`
- 烘缸组第 28 缸: `/PM1_DRYER_CYLINDER_28`
- 白水泵: `/PM1_PUMP_WHITEWATER_01`
- 进浆管道管口: `/PM1_HEADBOX_N1_INLET`
