# E3D 基本体参考 — 实机验证版
# ============================
# 经 E3D Design Mk3.1.11.0 加载验证: CYLI/BOX/CONE/DISH ✅
# SNOT/PYRA/CTOR/RTOR/NCYLI/NBOX 报 Syntax error ❌

## 可用基本体 (4种)

| 类型 | PML1命令 | 形状 | 关键属性 | 基准点 |
|------|---------|------|---------|--------|
| 长方体 | `NEW BOX` | 矩形块 | XLEN YLEN ZLEN | 几何中心 |
| 圆柱 | `NEW CYLI` | 圆柱 | DIAM HEIG | 底面中心 |
| 圆台/圆锥 | `NEW CONE` | 锥台 | DTOP DBOT HEIG | 底面中心 |
| 碟形封头 | `NEW DISH` | 球冠 | DIAM HEIG RADIUS | 底面中心 |

## NEW CONE (圆台/圆锥) ✅

```
NEW EQUI /NAME
NEW CONE
DTOP 300     ← 顶面直径 (DTOP=0时为圆锥)
DBOT 800     ← 底面直径
HEIG 1500    ← 沿主轴(Y)方向高度
POS E 0 N 0 U 0        ← 底面中心
ORI Y IS E AND Z IS U  ← 轴方向
```

DTOP=DBOT 时等同于 CYLI。最常用于锥形过渡段、料斗。

## NEW DISH (碟形封头) ✅

```
NEW EQUI /NAME
NEW DISH
DIAM 800     ← 直径(匹配圆柱)
HEIG 150     ← 拱高(封头深度)
RADIUS 800   ← 球面半径(≥DIAM/2, 越大越平)
POS E 0 N 0 U 0
ORI Y IS E AND Z IS U
```

最常用于压力容器/储罐封头。

## 被拒绝的基本体 ❌

以下在 E3D 3.1 宏模式下报 Syntax error，不可用:
- `NEW SNOT` (斜底圆柱)
- `NEW PYRA` (棱锥/棱台)
- `NEW CTOR` (圆环体)
- `NEW RTOR` (矩形环)
- `NEW NCYLI / NEW NBOX` (负基本体/开孔)

## 属性名速查

| 属性 | 适用 | 含义 |
|------|-----|------|
| DIAM | CYLI, DISH | 直径 mm |
| HEIG | CYLI, CONE, DISH | 沿主轴(Y)高度/长度 mm |
| DTOP | CONE | 顶径 mm |
| DBOT | CONE | 底径 mm |
| XLEN | BOX | EAST方向 mm |
| YLEN | BOX | NORTH方向 mm |
| ZLEN | BOX | UP方向 mm |
| RADIUS | DISH | 球面半径 mm |

## Python 辅助函数

```python
def CONE(self, name, dtop, dbot, height, e=0, n=0, u=0, axis='E'):
    self.n += 1
    self.L.append(f"NEW EQUI /{name.replace(' ','_')}")
    self.L.append(f"NEW CONE")
    self.L.append(f"DTOP {dtop}")
    self.L.append(f"DBOT {dbot}")
    self.L.append(f"HEIG {height}")
    self.L.append(f"POS E {e} N {n} U {u}")
    self.L.append(f"ORI Y IS {axis} AND Z IS U")
    self.L.append("")

def DISH(self, name, diam, height, radius=None, e=0, n=0, u=0, axis='E'):
    self.n += 1
    r = radius or diam  # 默认球面半径=直径
    self.L.append(f"NEW EQUI /{name.replace(' ','_')}")
    self.L.append(f"NEW DISH")
    self.L.append(f"DIAM {diam}")
    self.L.append(f"HEIG {height}")
    self.L.append(f"RADIUS {r}")
    self.L.append(f"POS E {e} N {n} U {u}")
    self.L.append(f"ORI Y IS {axis} AND Z IS U")
    self.L.append("")
```
