#!/usr/bin/env python3
"""E3D 基本体验证宏 — 每种基本体创建1个测试元素"""
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(r"D:\AVEVA\Projects\E3D3.1\e3d_agent\output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

L = []
def CY(name, d, h, e=0, n=0, u=0, ax='E'):
    L.append(f"NEW EQUI /TEST_{name}")
    L.append(f"NEW CYLI")
    L.append(f"DIAM {d}")
    L.append(f"HEIG {h}")
    L.append(f"POS E {e} N {n} U {u}")
    L.append(f"ORI Y IS {ax} AND Z IS U")
    L.append("")

def BX(name, x, y, z, e=0, n=0, u=0):
    L.append(f"NEW EQUI /TEST_{name}")
    L.append(f"NEW BOX")
    L.append(f"XLEN {x}")
    L.append(f"YLEN {y}")
    L.append(f"ZLEN {z}")
    L.append(f"POS E {e} N {n} U {u}")
    L.append("")

# Header
L = [f"-- E3D Primitives Test Macro | {datetime.now():%Y-%m-%d %H:%M:%S}",
     "-- 每个基本体一个测试元素, 间距1000mm沿EAST排列",
     "-- 前置: E3D中选可写ZONE → $$MACRO <本文件>",
     ""]

# 1. CYLI (已验证) @ E=0
CY("CYLI", 400, 500, 0, 0, 0, 'E')

# 2. BOX (已验证) @ E=1000
BX("BOX", 400, 400, 400, 1000, 0, 200)

# 3. CONE @ E=2000
L.append(f"NEW EQUI /TEST_CONE")
L.append(f"NEW CONE")
L.append(f"DTOP 200")
L.append(f"DBOT 400")
L.append(f"HEIG 500")
L.append(f"POS E 2000 N 0 U 0")
L.append(f"ORI Y IS E AND Z IS U")
L.append("")

# 4. DISH @ E=3000
L.append(f"NEW EQUI /TEST_DISH")
L.append(f"NEW DISH")
L.append(f"DIAM 400")
L.append(f"HEIG 150")
L.append(f"POS E 3000 N 0 U 0")
L.append(f"ORI Y IS E AND Z IS U")
L.append("")

# 5. SNOT @ E=4000
L.append(f"NEW EQUI /TEST_SNOT")
L.append(f"NEW SNOT")
L.append(f"DTOP 400")
L.append(f"DBOT 400")
L.append(f"HEIG 500")
L.append(f"POS E 4000 N 0 U 0")
L.append(f"ORI Y IS E AND Z IS U")
L.append("")

# 6. PYRA @ E=5000
L.append(f"NEW EQUI /TEST_PYRA")
L.append(f"NEW PYRA")
L.append(f"XTOP 200")
L.append(f"YTOP 200")
L.append(f"XBOT 400")
L.append(f"YBOT 400")
L.append(f"ZLEN 500")
L.append(f"POS E 5000 N 0 U 0")
L.append("")

# 7. CTOR @ E=6000
L.append(f"NEW EQUI /TEST_CTOR")
L.append(f"NEW CTOR")
L.append(f"DIAM 200")
L.append(f"HEIG 100")
L.append(f"POS E 6000 N 0 U 0")
L.append(f"ORI Y IS N AND Z IS U")
L.append("")

# 8. RTOR @ E=7000
L.append(f"NEW EQUI /TEST_RTOR")
L.append(f"NEW RTOR")
L.append(f"XLEN 400")
L.append(f"YLEN 400")
L.append(f"ZLEN 300")
L.append(f"POS E 7000 N 0 U 0")
L.append("")

# 9. NCYLI (负圆柱/开孔) @ E=8000
L.append(f"NEW EQUI /TEST_NCYLI")
L.append(f"NEW CYLI")
L.append(f"DIAM 400")
L.append(f"HEIG 500")
L.append(f"POS E 8000 N 0 U 0")
L.append(f"ORI Y IS E AND Z IS U")
L.append(f"NEW NCYLI")
L.append(f"DIAM 150")
L.append(f"HEIG 500")
L.append(f"POS E 8000 N 100 U 0")
L.append(f"ORI Y IS E AND Z IS U")
L.append("")

# 10. NBOX (负方体) @ E=9000
L.append(f"NEW EQUI /TEST_NBOX")
L.append(f"NEW BOX")
L.append(f"XLEN 400")
L.append(f"YLEN 400")
L.append(f"ZLEN 400")
L.append(f"POS E 9000 N 0 U 200")
L.append(f"NEW NBOX")
L.append(f"XLEN 150")
L.append(f"YLEN 150")
L.append(f"ZLEN 400")
L.append(f"POS E 9000 N 0 U 200")
L.append("")

L.append(f"-- 验证完成: 10个测试元素沿EAST 0-9000mm排列")

pml = "\n".join(L)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
fp = OUTPUT_DIR / f"test_primitives_{ts}.pml"
fp.write_text(pml, encoding="utf-8", newline="\n")

# Self-check: no PML2-isms
for b in ["!!Alert","$P","ENDS","END EQUI","NAME =","DESC =","!var =","COLLECT","UNSET","!!CE","!!WORLD"]:
    assert b not in pml, f"PML2-ism: {b}"

print(f"OK: {fp.name} | {len(pml.split(chr(10)))} lines | PML1✓")
print("测试元素: CYLI BOX CONE DISH SNOT PYRA CTOR RTOR NCYLI NBOX")
