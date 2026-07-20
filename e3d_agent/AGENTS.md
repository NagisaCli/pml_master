# AVEVA E3D AI 建模规范 v3 — 大模型通用高效精准建模实战指南

本文档供所有 LLM / AI Agent（包括 GPT-4, Claude, Gemini, DeepSeek 等）在生成 E3D PML 宏时**强制遵守**。每条规则均经 E3D Design Mk3.1.11.0 实机验证。

---

## 0. LLM 核心避坑铁律（报错/变形/飘移三大杀手）

### 🚨 铁律一：PML1 属性与定位命令顺序（决定坐标是否飘移）
在 E3D 解析器中，`NEW CYLI` 等基本体**必须先指定 `ORI` 方向，后指定 `POS` 位置**！
```
❌ 错误顺序 (E3D 解析 ORI 时会把已设定的 POS 坐标矢量一并旋转，导致车轴/基本体严重飘移错位！):
NEW CYLI
DIAM 800
HEIG 260
POS E 1450 N 720 U 400
ORI Z IS N AND Y IS U

✅ 唯一正确顺序 (先确定坐标轴向，后写入绝对世界坐标):
NEW CYLI
DIAM 800
HEIG 260
ORI Z IS N AND Y IS U
POS E 1450 N 720 U 400
```

### 🚨 铁律二：DISH / CONE 曲面基本体使用禁忌（决定外形是否变态膨胀）
1. **禁止使用大型球冠 DISH 作为平面掩盖盖板**：`DISH` 是球冠封头，基准直径过大（如 φ2000+）时会在 3D 空间形成巨大的半球包块，导致模型严重膨胀变形失真！
2. **DISH 的正确用途**：容器封头、端盖、灯具透镜、轮毂沉头内凹碗面、座椅软包。
3. **曲面细分 (Subdivision) 的正确做法**：采用小尺寸切片 (`BOX` / `CYLI`) 沿数学曲线阵列，提升高面数平滑度，而不是用单块巨型 DISH 充当造型面。

### 🚨 铁律三：零容忍 PML2 语法（报错即死）
宏脚本必须 100% 为 **PML1 命令**。出现以下任何词汇将直接导致 E3D 加载失败：
`!!Alert` `$P` `ENDS` `END EQUI` `NAME =` `DESC =` `!var =` `COLLECT` `UNSET` `!!CE` `!!WORLD`

---

## 1. 语法规范与可用基本体

### 可用基本体 (仅 4 种通过 E3D 3.1 实机验证)
- ✅ `NEW BOX` (长方体): 属性 `XLEN`, `YLEN`, `ZLEN` (基准点: **几何中心**)
- ✅ `NEW CYLI` (圆柱): 属性 `DIAM`, `HEIG` (基准点: **底面中心**)
- ✅ `NEW CONE` (圆锥/圆台): 属性 `DTOP`, `DBOT`, `HEIG` (基准点: **底面中心**)
- ✅ `NEW DISH` (碟形封头): 属性 `DIAM`, `HEIG`, `RADIUS` (基准点: **底面中心**)

❌ **不可用基本体** (报 Syntax error): `SNOT`, `PYRA`, `CTOR`, `RTOR`, `NCYLI`, `NBOX`

---

## 2. 层级架构 (EQUI -> SUBE -> 基本体)

大型复杂模型（如汽车、精馏塔、成套设备）必须使用三层结构，严禁所有基本体平铺在单层：

```pml
NEW EQUI /EQUIPMENT_NAME        ← 顶级设备节点 (全模型仅 1 个)

NEW SUBE /SUB_SYSTEM_01         ← 子系统 1 (如 /WHEELS_AND_AXLES)
NEW CYLI
...
NEW BOX
...

NEW SUBE /SUB_SYSTEM_02         ← 子系统 2 (如 /CABIN_INTERIOR)
NEW BOX
...
```

---

## 3. 几何与空间精准定位推算模板

### 轮轴与轮胎对齐数学推算 (以轮距 1700mm, 胎宽 260mm 为例)
- **车轮几何中心**：左轮 `N = +850.0`, 右轮 `N = -850.0`
- **轮胎** (`W=260`): 
  - 左轮: `POS N = 720.0`, `HEIG = 260.0` (延伸 `N: 720.0 ~ 980.0`, 中心 = 850.0)
  - 右轮: `POS N = -980.0`, `HEIG = 260.0` (延伸 `N: -980.0 ~ -720.0`, 中心 = -850.0)
- **刹车盘** (`W=30`, 贴合轮胎内侧):
  - 左刹车盘: `POS N = 690.0`, `HEIG = 30.0` (延伸 `N: 690.0 ~ 720.0`)
  - 右刹车盘: `POS N = -720.0`, `HEIG = 30.0` (延伸 `N: -720.0 ~ -690.0`)
- **贯穿车轴无缝对接** (`L=1380`):
  - `POS N = -690.0`, `HEIG = 1380.0` (延伸 `N: -690.0 ~ +690.0`)，两端完美嵌合左右刹车盘内侧，绝不出头穿透轮胎！

---

## 4. Python 代码生成与自检模板 (Prompt 注入用)

```python
class E3DModelBuilder:
    def __init__(self, equi_name):
        self.L = [f"NEW EQUI /{equi_name}", ""]
        self.sube_set = set()
        self.prim_count = 0

    def SUBE(self, name):
        s = name.replace(" ", "_").replace("-", "_")
        assert s not in self.sube_set, f"SUBE 重名: {s}"
        self.sube_set.add(s)
        self.L.append(f"NEW SUBE /{s}")

    def CYLI(self, diam, heig, e, n, u, axis='N'):
        self.prim_count += 1
        self.L.append("NEW CYLI")
        self.L.append(f"DIAM {diam:.1f}")
        self.L.append(f"HEIG {heig:.1f}")
        # 必须先 ORI，后 POS！
        if axis == 'N':
            self.L.append("ORI Z IS N AND Y IS U")
        elif axis == 'E':
            self.L.append("ORI Z IS E AND Y IS U")
        else:
            self.L.append("ORI Z IS U AND Y IS N")
        self.L.append(f"POS E {e:.1f} N {n:.1f} U {u:.1f}")
        self.L.append("")

    def BOX(self, x, y, z, e, n, u):
        self.prim_count += 1
        self.L.append("NEW BOX")
        self.L.append(f"XLEN {x:.1f}")
        self.L.append(f"YLEN {y:.1f}")
        self.L.append(f"ZLEN {z:.1f}")
        self.L.append(f"POS E {e:.1f} N {n:.1f} U {u:.1f}")
        self.L.append("")

    def build_and_validate(self):
        pml = "\n".join(self.L)
        banned = ["!!Alert", "$P", "ENDS", "END EQUI", "NAME =", "DESC =",
                  "!var =", "COLLECT", "UNSET", "!!CE", "!!WORLD"]
        for b in banned:
            assert b not in pml, f"违反 PML1 语法，检测到 PML2 关键字: {b}"
        return pml
```

---

## 5. 大模型 (LLM) 交付前检查清单

在输出 PML 宏代码或 Python 生成脚本前，LLM 必须检查：
1. [ ] 是否只有 1 个顶级 `NEW EQUI /`？
2. [ ] 是否使用了 `NEW SUBE /` 划分各个子系统？
3. [ ] 所有的 `NEW CYLI` 是否都遵循了 **`先 ORI，后 POS`**？
4. [ ] 轴类与轮胎类的 `POS N` / `POS E` 长度与中心推算是否毫米级嵌合无穿透？
5. [ ] 代码中是否 0 次出现 `!!Alert` / `COLLECT` / `!var =` 等 PML2 禁用语法？

