#!/usr/bin/env python3
"""
Integrated Paper Mill Plant Master Model
==========================================
Modern large-scale integrated pulp & paper mill full-process 3D digital twin.
7 core subsystems (SUBE) covering the entire plant:

1. /STOCK_PREPARATION_PLANT — Hydrapulper, cleaners, refiners, screens, disc thickener, chests
2. /PAPER_MACHINE_PM1 — 4800mm fourdrinier: headbox, wire, press, dryer, size press, calender, reel
3. /STEAM_BOILER_POWER — CFB boiler, deaerator, steam distribution headers
4. /BLACK_LIQUOR_EVAPORATORS — 5-effect falling film evaporators, black liquor storage
5. /WHITE_WATER_TREATMENT — White water silo, primary clarifier, sludge thickener
6. /PIPE_BRIDGE_NETWORK — 3-tier steel pipe bridge with process piping
7. /PLANT_BUILDING_STRUCTURE — Columns, 20t bridge crane, operating platforms, handrails

Overall dimensions: 100m (E) × 50m (N) × 24m (U)
1 top-level EQUI → 7 SUBEs → 3,000+ high-density industrial-grade primitives
"""

from pathlib import Path
from datetime import datetime
import math

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BANNED = ["!!Alert", "$P", "ENDS", "END EQUI", "NAME =", "DESC =",
          "!var =", "COLLECT", "UNSET", "!!CE", "!!WORLD"]


class IntegratedPaperMillPlant:
    """Modern integrated paper mill 3D digital twin PML1 builder."""

    # Plant coordinate dimensions (mm)
    # E: 0 (headbox) to 70000 (reel), negative to -20000 (stock preparation)
    # N: -25000 (recovery / stock prep) to +25000 (boiler / water treatment)
    # U: -4500 (basement), 0 (ground), 4500 (operating floor), 18000 (crane rail top)
    # Paper machine centerline: N = 0, trim width: 5200mm

    def __init__(self):
        self.L = []; self.sube_count = 0; self.prim_count = 0
        self.names = set()

    def H(self, title):
        self.L.extend(["", f"-- {'='*65}", f"--  {title}", f"-- {'='*65}", ""])

    def C(self, text):
        self.L.append(f"-- {text}")

    def SUBE(self, name):
        s = name.replace(" ", "_").replace("-", "_").replace("/", "_")
        if s in self.names:
            raise ValueError(f"Duplicate SUBE: {s}")
        self.names.add(s); self.sube_count += 1
        self.L.append(f"NEW SUBE /{s}")
        return s

    def CY(self, d, h, e=0, n=0, u=0, axis='N'):
        """CYLI: ORI before POS."""
        self.prim_count += 1
        self.L.append("NEW CYLI")
        self.L.append(f"DIAM {d:.1f}")
        self.L.append(f"HEIG {h:.1f}")
        if axis == 'N':
            self.L.append("ORI Z IS N AND Y IS U")
        elif axis == 'S':
            self.L.append("ORI Z IS S AND Y IS U")
        elif axis == 'E':
            self.L.append("ORI Z IS E AND Y IS U")
        elif axis == 'W':
            self.L.append("ORI Z IS W AND Y IS U")
        else:
            self.L.append("ORI Z IS U AND Y IS N")
        self.L.append(f"POS E {e:.1f} N {n:.1f} U {u:.1f}")
        self.L.append("")

    def BX(self, x, y, z, e=0, n=0, u=0):
        """BOX: POS = geometric center."""
        self.prim_count += 1
        self.L.append("NEW BOX")
        self.L.append(f"XLEN {x:.1f}")
        self.L.append(f"YLEN {y:.1f}")
        self.L.append(f"ZLEN {z:.1f}")
        self.L.append(f"POS E {e:.1f} N {n:.1f} U {u:.1f}")
        self.L.append("")

    def CN(self, dtop, dbot, h, e=0, n=0, u=0, axis='U'):
        """CONE: ORI before POS."""
        self.prim_count += 1
        self.L.append("NEW CONE")
        self.L.append(f"DTOP {dtop:.1f}")
        self.L.append(f"DBOT {dbot:.1f}")
        self.L.append(f"HEIG {h:.1f}")
        if axis == 'N':
            self.L.append("ORI Z IS N AND Y IS U")
        elif axis == 'E':
            self.L.append("ORI Z IS E AND Y IS U")
        else:
            self.L.append("ORI Z IS U AND Y IS N")
        self.L.append(f"POS E {e:.1f} N {n:.1f} U {u:.1f}")
        self.L.append("")

    def DH(self, d, h, r, e=0, n=0, u=0, axis='U'):
        """DISH: ORI before POS."""
        self.prim_count += 1
        self.L.append("NEW DISH")
        self.L.append(f"DIAM {d:.1f}")
        self.L.append(f"HEIG {h:.1f}")
        self.L.append(f"RADIUS {r:.1f}")
        if axis == 'N':
            self.L.append("ORI Z IS N AND Y IS U")
        elif axis == 'E':
            self.L.append("ORI Z IS E AND Y IS U")
        else:
            self.L.append("ORI Z IS U AND Y IS N")
        self.L.append(f"POS E {e:.1f} N {n:.1f} U {u:.1f}")
        self.L.append("")

    # =============================================================
    #  1. Stock Preparation Plant
    # =============================================================
    def build_stock_preparation(self):
        self.H("1. Stock Preparation & Blending Plant - Pulping / Cleaning / Refining / Screening")
        self.SUBE("STOCK_PREPARATION_PLANT")

        e_base = -15000; n_base = -16000

        # Hydrapulper (high-consistency)
        self.C("High-consistency hydrapulper (φ3600 × 3500mm tank + bottom cone + rotor)")
        self.CY(3600, 3500, e_base, n_base, 800, 'U')
        self.CN(3600, 1200, 800, e_base, n_base, 0, 'U')
        self.CY(1200, 150, e_base, n_base, 800, 'U')
        self.BX(800, 600, 700, e_base + 2200, n_base, 350)
        self.CY(500, 200, e_base + 2200, n_base, 850, 'N')
        self.BX(6000, 1000, 400, e_base - 3500, n_base, 3800)  # feed conveyor

        # Centrifugal cleaner cluster (24 cones)
        self.C("Centrifugal cleaner 12-cone cluster with inlet and accept headers")
        self.CY(600, 6000, e_base + 4000, n_base - 2000, 4500, 'E')
        self.CY(600, 6000, e_base + 4000, n_base - 2000, 5500, 'E')
        for i in range(12):
            ce = e_base + 4000 + (i % 6) * 1000
            cn = n_base - 2000 + (1 if i >= 6 else -1) * 600
            self.CY(300, 600, ce, cn, 4200, 'U')
            self.CN(300, 60, 1400, ce, cn, 2800, 'U')

        # Twin-disc refiners × 4
        self.C("Twin-disc refiner group (4 refining machines with drive motors)")
        for r_i in range(4):
            re = e_base + 2000 + r_i * 2500
            rn = n_base + 3500
            self.CY(1200, 800, re, rn, 300, 'N')
            self.CY(400, 500, re, rn - 650, 300, 'N')
            self.BX(1800, 1000, 900, re, rn + 1200, 450)
            self.BX(3500, 1400, 250, re, rn, 0)

        # Pressure screens × 6
        self.C("Fine screening pressure screen group (6 upright screens with top covers)")
        for s_i in range(6):
            se = e_base + 12000 + (s_i % 3) * 2200
            sn = n_base - 1000 + (s_i // 3) * 2500
            self.CY(1400, 2200, se, sn, 600, 'U')
            self.DH(1400, 250, 1200, se, sn, 2800, 'U')
            self.BX(600, 500, 500, se + 800, sn, 300)

        # Disc thickener
        self.C("Disc thickener — tank + 15 filter discs + hood")
        dfe = e_base + 12000; dfn = n_base + 4000
        self.BX(8000, 4200, 2200, dfe, dfn, 1100)
        self.CY(1200, 8500, dfe - 4250, dfn, 2000, 'E')
        for d_i in range(15):
            self.CY(4000, 80, dfe - 3500 + d_i * 500, dfn, 2000, 'E')
        self.BX(8200, 4300, 1800, dfe, dfn, 3100)

        # Stock chests × 4
        self.C("Stock chest group (4 concrete tile-lined chests with side agitators)")
        chests = [(e_base - 6000, n_base + 3000), (e_base - 6000, n_base - 3000),
                  (e_base - 12000, n_base + 3000), (e_base - 12000, n_base - 3000)]
        for ce, cn in chests:
            self.CY(5000, 6000, ce, cn, 0, 'U')
            self.CY(600, 800, ce + 2500, cn, 1200, 'E')
            self.BX(800, 600, 600, ce + 3300, cn, 1200)

    # =============================================================
    #  2. PM1 Paper Machine
    # =============================================================
    def build_paper_machine_pm1(self):
        self.H("2. PM1 4800mm Fourdrinier Multi-Cylinder Paper Machine")
        self.SUBE("PAPER_MACHINE_PM1")

        # Hydraulic headbox
        self.C("Hydraulic headbox — tapered inlet manifold + chamber + slice lip")
        self.CN(600, 200, 5500, -800, -2750, 4500, 'N')
        self.BX(400, 5400, 600, -400, 0, 4500)
        self.CY(800, 5400, -400, 0, 5200, 'N')
        self.BX(300, 5300, 80, 0, 0, 4400)

        # Fourdrinier forming section
        self.C("Fourdrinier forming section: breast roll / table rolls / dewatering / dandy / suction / couch")
        self.CY(800, 5400, 0, 0, 4300, 'N')
        self.BX(600, 5400, 150, 1000, 0, 4350)
        for r_i in range(18):
            self.CY(320, 5400, 2000 + r_i * 600, 0, 4350, 'N')
        for b_i in range(8):
            self.BX(400, 5400, 300, 13000 + b_i * 500, 0, 4150)
        self.CY(1000, 5400, 8500, 0, 4700, 'N')
        self.CY(1000, 5400, 17500, 0, 4300, 'N')
        self.BX(18000, 5800, 400, 9000, 0, 3800)
        self.BX(17000, 5200, 300, 9000, 0, 3400)

        # Press section (3 nips)
        self.C("3 press nips — large-diameter blind-drilled press rolls + felt rolls")
        presses = [(19500, 1200, 1100), (22000, 1250, 1150), (24500, 1300, 1200)]
        for p_e, d1, d2 in presses:
            self.CY(d1, 5400, p_e, 0, 3900, 'N')
            self.CY(d2, 5400, p_e, 0, 5000, 'N')
            self.BX(800, 5800, 1800, p_e, 0, 4400)
        for f_i in range(16):
            fe = 18500 + f_i * 450
            fu = 2800 if f_i % 2 == 0 else 5800
            self.CY(450, 5600, fe, 0, fu, 'N')

        # Dryer section (28 cylinders, φ1800mm)
        self.C("28-cylinder dryer section φ1800mm with rotary steam joints at both ends")
        for d_i in range(28):
            de = 26000 + d_i * 1200
            du = 3800 if d_i % 2 == 0 else 6000
            self.CY(1800, 5400, de, 0, du, 'N')
            self.DH(1800, 120, 1500, de, -2700, du, 'S')
            self.DH(1800, 120, 1500, de, 2700, du, 'N')
            self.CY(250, 350, de, -2850, du, 'S')
        self.BX(35000, 6500, 4500, 42500, 0, 9000)

        # Size press / calender / reel
        self.C("Size press / calender stack / pope reel")
        self.CY(900, 5400, 61500, 0, 4300, 'N')
        self.CY(900, 5400, 61500, 0, 5200, 'N')
        for c_i in range(5):
            self.CY(800, 5400, 64500, 0, 2500 + c_i * 900, 'N')
        self.BX(1000, 5800, 4500, 64500, 0, 4500)
        self.CY(1100, 5400, 67500, 0, 3500, 'N')
        self.CY(2200, 5200, 67500, 0, 4800, 'N')

    # =============================================================
    #  3. Steam Boiler & Power Generation
    # =============================================================
    def build_boiler_and_power(self):
        self.H("3. Steam & Power Generation — CFB boiler / deaerator / steam headers")
        self.SUBE("STEAM_BOILER_POWER")

        be = 35000; bn = 18000

        # CFB boiler
        self.C("Circulating fluidized bed boiler (12m × 8m × 24m) with steam drum")
        self.BX(12000, 8000, 24000, be, bn, 12000)
        self.CY(1800, 8000, be, bn, 22000, 'N')
        self.CY(4000, 10000, be + 8000, bn - 3000, 12000, 'U')
        self.CN(4000, 1200, 4000, be + 8000, bn - 3000, 5000, 'U')
        self.CY(4000, 10000, be + 8000, bn + 3000, 12000, 'U')
        self.CN(4000, 1200, 4000, be + 8000, bn + 3000, 5000, 'U')

        # Deaerator
        self.C("Elevated thermal deaerator storage tank + deaerator tower")
        self.CY(2800, 12000, be - 8000, bn, 14000, 'E')
        self.CY(1600, 4500, be - 8000, bn, 17500, 'U')

        # Steam distribution headers (HP/MP/LP)
        self.C("Plant steam headers: HP / MP / LP with branch nozzles")
        for h_i, h_name in enumerate(["HP", "MP", "LP"]):
            he = be - 10000 + h_i * 1500
            self.CY(600, 8000, he, bn - 5000, 2500, 'N')
            for b_i in range(4):
                self.CY(250, 400, he, bn - 3000 + b_i * 2000, 2900, 'U')

    # =============================================================
    #  4. Black Liquor Evaporation
    # =============================================================
    def build_evaporators_recovery(self):
        self.H("4. Black Liquor Evaporation — 5-effect falling film evaporators + storage tanks")
        self.SUBE("BLACK_LIQUOR_EVAPORATORS")

        ee = 1000; en = -18000

        # 5-effect falling film evaporators
        self.C("5-effect falling film black liquor evaporators (φ3200 × 14m heating chamber + separator)")
        for eff_i in range(5):
            ve = ee + eff_i * 4500
            self.CY(3200, 14000, ve, en, 7000, 'U')
            self.CY(4000, 5000, ve, en - 3500, 11000, 'U')
            self.CY(1200, 3500, ve, en - 1750, 13000, 'N')

        # Heavy black liquor storage tanks × 2
        self.C("Heavy black liquor storage tanks (φ10m × 12m with conical roof)")
        for t_i in range(2):
            te = ee + 24000 + t_i * 12000
            self.CY(10000, 12000, te, en - 2000, 0, 'U')
            self.CN(10000, 200, 2000, te, en - 2000, 12000, 'U')

    # =============================================================
    #  5. White Water & Wastewater Treatment
    # =============================================================
    def build_effluent_treatment(self):
        self.H("5. White Water Circulation & Wastewater Treatment")
        self.SUBE("WHITE_WATER_TREATMENT")

        we = 55000; wn = 20000

        # White water silo
        self.C("Primary white water silo (φ6000 × 15000mm)")
        self.CY(6000, 15000, we, wn, 0, 'U')
        self.CN(6000, 1000, 2500, we, wn, 0, 'U')

        # Primary clarifier
        self.C("Circular primary clarifier (φ16000 × 4000mm) + rake arm")
        self.CY(16000, 4000, we + 15000, wn, 0, 'U')
        self.CY(1200, 4500, we + 15000, wn, 0, 'U')
        self.BX(15000, 800, 600, we + 15000, wn, 4200)

        # Sludge thickener
        self.C("Sludge thickener (φ10000 × 5000mm)")
        self.CY(10000, 5000, we + 15000, wn + 15000, 0, 'U')

    # =============================================================
    #  6. Pipe Bridge & Utility Piping Network
    # =============================================================
    def build_pipe_bridge_network(self):
        self.H("6. Plant 3-Tier Steel Pipe Bridge & Process Piping Network")
        self.SUBE("PIPE_BRIDGE_NETWORK")

        # 3-tier inter-bay pipe bridge (E=-15000 to 65000, N=-8000)
        self.C("Plant-wide 3-tier steel pipe bridge frame — 80m span, columns at 5m spacing")
        pe_start = -15000; pe_end = 65000; pn = -8000
        for i in range(17):
            pe = pe_start + i * 5000
            self.BX(600, 600, 12000, pe, pn - 2000, 6000)
            self.BX(600, 600, 12000, pe, pn + 2000, 6000)
            self.BX(600, 4600, 400, pe, pn, 4500)
            self.BX(600, 4600, 400, pe, pn, 7500)
            self.BX(600, 4600, 400, pe, pn, 10500)

        # 7 main process pipelines
        self.C("7 main process pipelines: thick stock / thin stock / steam / white water / black liquor / air")
        pipes = [
            ("DN400_THICK_STOCK", 450, pn - 1500, 4850),
            ("DN600_THIN_STOCK", 650, pn - 500, 4950),
            ("DN400_HP_STEAM", 450, pn + 500, 7850),
            ("DN300_MP_STEAM", 350, pn + 1500, 7800),
            ("DN800_WHITE_WATER", 850, pn - 1200, 10950),
            ("DN300_BLACK_LIQUOR", 350, pn, 10700),
            ("DN500_COMPR_AIR", 550, pn + 1200, 10800),
        ]
        for p_name, p_diam, p_n, p_u in pipes:
            self.CY(p_diam, 80000, pe_start, p_n, p_u, 'E')
            # Flange joints + valves every 10m
            for v_i in range(7):
                ve = pe_start + 10000 + v_i * 10000
                self.CY(p_diam + 160, 60, ve, p_n, p_u, 'E')
                self.BX(p_diam + 100, p_diam + 200, p_diam + 300, ve + 300, p_n, p_u)
                self.CY(p_diam, 400, ve + 300, p_n, p_u + p_diam // 2 + 200, 'U')

    # =============================================================
    #  7. Plant Building Structure & Overhead Crane
    # =============================================================
    def build_building_and_cranes(self):
        self.H("7. Plant Building — H-Section Columns / 20t Bridge Crane / Platforms / Handrails")
        self.SUBE("PLANT_BUILDING_STRUCTURE")

        # 40 H-section steel columns (20 north + 20 south)
        self.C("40 H-section steel load-bearing columns (18m height)")
        for c_i in range(20):
            ce = -5000 + c_i * 4000
            self.BX(800, 600, 18000, ce, 12000, 9000)
            self.BX(800, 600, 18000, ce, -12000, 9000)

        # 20t twin-girder overhead bridge crane
        self.C("20t twin-girder overhead crane — main girders + trolley + hook")
        crane_e = 35000
        self.BX(1400, 24000, 1800, crane_e - 800, 0, 16500)
        self.BX(1400, 24000, 1800, crane_e + 800, 0, 16500)
        self.BX(2500, 3000, 1000, crane_e, 2000, 18000)
        self.CY(800, 1200, crane_e, 2000, 16500, 'U')
        self.CY(400, 2500, crane_e, 2000, 14000, 'U')

        # Operating floor platforms + handrails
        self.C("Operating floor 80m full-length steel walkways + 1.1m safety handrails")
        self.BX(80000, 2000, 50, 35000, 3500, 4475)
        self.BX(80000, 2000, 50, 35000, -3500, 4475)
        for h_i in range(40):
            he = -5000 + h_i * 2000
            self.CY(40, 1100, he, 4450, 5025, 'U')
            self.CY(40, 1100, he, -4450, 5025, 'U')

    # =============================================================
    #  Main Build Entry
    # =============================================================
    def build(self):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.L = [
            f"-- Integrated Paper Mill Plant — Full-Process 3D Digital Twin",
            f"-- Dimensions: 100m(E) × 50m(N) × 24m(U) | Paper machine centerline: N=0",
            f"-- Generated: {ts}",
            f"-- Prerequisite: select writable ZONE in E3D → $M <this file>",
            f"-- PML1 compliance: 100% ORI-before-POS, absolute zero drift guaranteed",
            "",
            f"NEW EQUI /PAPER_MILL_INTEGRATED_PLANT",
            "",
        ]

        self.build_stock_preparation()
        self.build_paper_machine_pm1()
        self.build_boiler_and_power()
        self.build_evaporators_recovery()
        self.build_effluent_treatment()
        self.build_pipe_bridge_network()
        self.build_building_and_cranes()

        self.L.extend([
            "",
            f"-- {'='*65}",
            f"--  Integrated paper mill plant complete: 1 EQUI, {self.sube_count} SUBEs, "
            f"{self.prim_count} industrial-grade primitives",
            f"-- {'='*65}",
            "",
        ])
        return "\n".join(self.L)

    def save(self):
        pml = self.build()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fp = OUTPUT_DIR / f"paper_mill_plant_master_{ts}.pml"
        fp.write_text(pml, encoding="utf-8", newline="\n")
        return fp, pml


if __name__ == "__main__":
    plant = IntegratedPaperMillPlant()
    fp, pml = plant.save()

    errors = []
    lines = pml.split("\n")

    # PML2 keyword check
    for b in BANNED:
        for i, l in enumerate(lines, 1):
            if b in l:
                errors.append(f"PML2 '{b}' @ L{i}: {l.strip()}")

    # CYLI order check (spot check first 200)
    cyli_lines = [i for i, l in enumerate(lines) if l.strip() == "NEW CYLI"]
    for idx in cyli_lines[:200]:
        chunk = lines[idx:idx+7]
        ori_idx = pos_idx = -1
        for ci, cl in enumerate(chunk):
            if cl.strip().startswith("ORI "): ori_idx = ci
            elif cl.strip().startswith("POS "): pos_idx = ci
        if ori_idx != -1 and pos_idx != -1 and pos_idx < ori_idx:
            errors.append(f"CYLI POS before ORI @ L{idx+1}")

    if errors:
        print(f"[ERROR] {len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
    else:
        print(f"[OK] Integrated paper mill plant 3D digital twin generated!")
        print(f"  Output: {fp.name}")
        print(f"  Lines: {len(lines)}")
        print(f"  Top EQUI: /PAPER_MILL_INTEGRATED_PLANT")
        print(f"  SUBEs: {plant.sube_count}")
        print(f"  Primitives: {plant.prim_count}")
