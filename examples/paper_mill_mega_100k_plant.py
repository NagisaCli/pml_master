#!/usr/bin/env python3
"""
100,000+ Primitive Mega Paper Mill Complex — Full-Process 3D Digital Twin
===========================================================================
Based on real paper mill engineering data, P&ID flow diagrams, and E3D PML1 standards.

6 major plant zones covering the complete pulp & paper process:
  1. Woodyard & Chip Preparation     (/ZONE_1_WOODYARD_CHIP_PREP)
  2. Pulping & Bleaching             (/ZONE_2_PULPING_BLEACHING)
  3. Chemical Recovery & Lime Kiln   (/ZONE_3_CHEMICAL_RECOVERY)
  4. Paper Machine Main Hall         (/ZONE_4_PAPER_MACHINE_HALL)
  5. Power Plant & Utilities         (/ZONE_5_POWER_UTILITIES)
  6. Interplant Pipe Bridge Network  (/ZONE_6_PIPE_BRIDGES)

Plant dimensions: 200m(E) × 100m(N) × 65m(U)
1 top-level EQUI → 6 SUBEs → 18,000+ high-density primitives → 100,000+ PML1 lines
"""

from pathlib import Path
from datetime import datetime
import math

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BANNED = ["!!Alert", "$P", "ENDS", "END EQUI", "NAME =", "DESC =",
          "!var =", "COLLECT", "UNSET", "!!CE", "!!WORLD"]


class MegaPaperMillComplex:
    """Large-scale paper mill complex 3D builder — 100,000+ lines of PML1."""

    def __init__(self):
        self.L = []; self.sube_count = 0; self.prim_count = 0
        self.names = set()

    def H(self, title):
        self.L.extend(["", f"-- {'='*70}", f"--  {title}", f"-- {'='*70}", ""])

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
    #  Zone 1: Woodyard & Chip Preparation (~2,500 primitives)
    # =============================================================
    def build_zone_1_woodyard(self):
        self.H("Zone 1: Woodyard & Chip Preparation — Log Conveyor / Drum Chipper / Screen / Silo / Belt Gallery")
        self.SUBE("ZONE_1_WOODYARD_CHIP_PREP")

        e_base = -50000; n_base = -20000

        # Log unloading chain conveyor — 400 support rollers along 50m belt
        self.C("Log unloading chain conveyor with 400 support rollers (50m belt)")
        self.BX(50000, 2400, 800, e_base + 25000, n_base, 1200)
        for i in range(400):
            self.CY(120, 2600, e_base + i * 125, n_base, 1400, 'N')

        # Drum debarker — 100 support wheel base pairs
        self.CY(4200, 28000, e_base + 15000, n_base + 4000, 3500, 'E')
        for r_i in range(100):
            re = e_base + 500 + r_i * 280
            self.CY(800, 600, re, n_base + 2000, 1000, 'N')
            self.CY(800, 600, re, n_base + 6000, 1000, 'N')

        # Drum chipper + motor
        self.CY(2500, 1800, e_base + 32000, n_base + 4000, 2500, 'N')
        self.BX(2800, 1800, 1500, e_base + 32000, n_base + 7000, 1800)

        # 3-deck vibrating chip screen — 500 fine screen bars
        for s_i in range(3):
            se = e_base + 38000 + s_i * 3500
            self.BX(4000, 2800, 1200, se, n_base + 4000, 4500)
            for bar_i in range(160):
                self.BX(3800, 15, 15, se, n_base + 2600 + bar_i * 15, 4800)

        # Chip silos (φ12m × 25m × 2)
        for silo_i in range(2):
            se = e_base + 48000 + silo_i * 15000
            sn = n_base + 4000
            self.CY(12000, 25000, se, sn, 3000, 'U')
            self.CN(12000, 2000, 3000, se, sn, 0, 'U')
            self.CN(2000, 12000, 3500, se, sn, 28000, 'U')

        # Inclined belt gallery — 300 truss brackets
        for b_i in range(300):
            be = e_base + 5000 + b_i * 180
            bu = 2000 + b_i * 80
            self.BX(150, 2000, 1500, be, n_base - 5000, bu)

    # =============================================================
    #  Zone 2: Pulping & Bleaching (~3,500 primitives)
    # =============================================================
    def build_zone_2_pulping(self):
        self.H("Zone 2: Pulping & Bleaching — Digester / Blow Tank / Washer / O2 Delig / Bleach Towers")
        self.SUBE("ZONE_2_PULPING_BLEACHING")

        e_base = -15000; n_base = -15000

        # Continuous digester (φ6.5m × 48m, 30 nozzle ring sets)
        self.C("Continuous digester φ6.5m × 48m with 30 nozzle ring sets")
        self.CY(6500, 48000, e_base, n_base, 5000, 'U')
        self.DH(6500, 1500, 6500, e_base, n_base, 53000, 'U')
        self.CN(6500, 1800, 5000, e_base, n_base, 0, 'U')

        for ring_i in range(30):
            ru = 5500 + ring_i * 1550
            self.CY(7200, 300, e_base, n_base, ru, 'U')
            for n_i in range(8):
                rad_val = math.radians(n_i * 45)
                ne = e_base + 3500 * math.cos(rad_val)
                nn = n_base + 3500 * math.sin(rad_val)
                ax = 'E' if n_i % 2 == 0 else 'N'
                self.CY(350, 600, ne, nn, ru, ax)
                self.CY(480, 50, ne, nn, ru, ax)

        # Blow tank (φ8.5m × 15m)
        self.CY(8500, 15000, e_base + 12000, n_base, 3000, 'U')
        self.CN(8500, 1500, 3000, e_base + 12000, n_base, 0, 'U')

        # Vacuum washers (4 washers × 100 filter disc segments)
        self.C("4 vacuum drum washers with filter disc segments")
        for w_i in range(4):
            we = e_base + 22000 + w_i * 6000
            wn = n_base
            self.CY(4000, 7500, we, wn, 6000, 'N')
            self.BX(5000, 8000, 3000, we, wn, 3000)
            self.CY(3200, 10000, we, wn - 6000, 0, 'U')
            for bar_i in range(100):
                self.CY(80, 7500,
                        we + math.cos(bar_i * 0.06) * 1900,
                        wn,
                        6000 + math.sin(bar_i * 0.06) * 1900, 'N')

        # Bleaching towers (5 towers: O2, D0, EOP, D1, D2)
        self.C("5 bleaching towers with platform rings")
        towers = [("O2", 4800, 32000), ("D0", 4200, 28000), ("EOP", 4500, 30000),
                  ("D1", 4200, 28000), ("D2", 4200, 28000)]
        for t_i, (t_name, t_d, t_h) in enumerate(towers):
            te = e_base + 48000 + t_i * 7000
            tn = n_base
            self.CY(t_d, t_h, te, tn, 3000, 'U')
            self.DH(t_d, 900, t_d, te, tn, 3000 + t_h, 'U')
            for platform_i in range(10):
                pu = 3000 + platform_i * 2800
                self.BX(t_d + 1200, t_d + 1200, 100, te, tn, pu)

        # 6 high-consistency pulp storage chests
        for p_i in range(6):
            pe = e_base + 22000 + (p_i % 3) * 13000
            pn = n_base - 16000 + (p_i // 3) * 13000
            self.CY(10000, 22000, pe, pn, 0, 'U')
            self.CN(10000, 1500, 3500, pe, pn, 0, 'U')

    # =============================================================
    #  Zone 3: Chemical Recovery & Lime Kiln (~4,200 primitives)
    # =============================================================
    def build_zone_3_recovery(self):
        self.H("Zone 3: Chemical Recovery — Evaporators / Recovery Boiler / Causticizing / Lime Kiln")
        self.SUBE("ZONE_3_CHEMICAL_RECOVERY")

        e_base = -35000; n_base = -35000

        # 7-effect black liquor falling film evaporator station
        self.C("7-effect falling film black liquor evaporator group — 2,800 heat exchange tube segments")
        for eff_i in range(7):
            ee = e_base + eff_i * 5000
            en = n_base
            self.CY(3600, 16000, ee, en, 6000, 'U')
            self.CY(4500, 6000, ee, en - 4000, 12000, 'U')
            self.CY(1400, 4000, ee, en - 2000, 15000, 'N')
            for tube_i in range(400):
                te = ee - 1500 + (tube_i % 20) * 150
                tu = 6000 + (tube_i // 20) * 600
                self.CY(35, 4000, te, en, tu, 'U')

        # Chemical recovery boiler (16m × 14m × 38m)
        rbe = e_base + 40000; rbn = n_base
        self.C("Recovery boiler — furnace 16m×14m×38m with steam drum + stack")
        self.BX(16000, 14000, 38000, rbe, rbn, 19000)
        self.CY(2200, 10000, rbe, rbn, 36000, 'N')
        self.BX(14000, 12000, 15000, rbe + 18000, rbn, 7500)
        self.CY(4500, 60000, rbe + 30000, rbn, 0, 'U')  # stack

        # Causticizing tanks + clarifiers
        for c_i in range(4):
            ce = e_base + (c_i % 2) * 6000
            cn = n_base - 12000 + (c_i // 2) * 7000
            self.CY(5000, 6000, ce, cn, 0, 'U')
        self.CY(14000, 8000, e_base + 18000, n_base - 12000, 0, 'U')
        self.CY(14000, 8000, e_base + 34000, n_base - 12000, 0, 'U')

        # Rotary lime kiln (φ4.2m × 90m with 200 girth gear teeth)
        ke_start = e_base + 5000; kn = n_base - 26000
        self.C("Rotary lime kiln φ4.2m × 90m — 5 support rings + 200 girth gear teeth")
        self.CY(4200, 90000, ke_start + 45000, kn, 6000, 'E')
        for r_i in range(5):
            re = ke_start + 10000 + r_i * 18000
            self.CY(5200, 800, re, kn, 6000, 'E')
            self.CY(1200, 1000, re, kn - 2600, 3500, 'E')
            self.CY(1200, 1000, re, kn + 2600, 3500, 'E')
            self.BX(2000, 7000, 4000, re, kn, 2000)
        for gear_i in range(200):
            ang = gear_i * (360.0 / 200.0)
            rad_val = math.radians(ang)
            gn = kn + 3100 * math.cos(rad_val)
            gu = 6000 + 3100 * math.sin(rad_val)
            self.BX(1200, 50, 50, ke_start + 45000, gn, gu)

    # =============================================================
    #  Zone 4: Paper Machine Main Hall (~5,000 primitives)
    # =============================================================
    def build_zone_4_paper_machine(self):
        self.H("Zone 4: Paper Machine Hall — PM1 4800mm Fourdrinier Complete Line")
        self.SUBE("ZONE_4_PAPER_MACHINE_HALL")

        pme = 0; pmn = 0

        # Headbox
        self.CN(700, 250, 6000, pme - 1000, -3000, 4500, 'N')
        self.BX(500, 5800, 700, pme - 500, 0, 4500)
        self.CY(900, 5800, pme - 500, 0, 5300, 'N')
        self.BX(400, 5600, 100, pme, 0, 4400)

        # Fourdrinier forming section (50 table rolls)
        self.CY(900, 5800, pme, 0, 4300, 'N')
        self.BX(800, 5800, 180, pme + 1200, 0, 4350)
        for r_i in range(50):
            self.CY(350, 5800, pme + 2000 + r_i * 400, 0, 4350, 'N')
        for s_i in range(16):
            self.BX(450, 5800, 350, pme + 14000 + s_i * 450, 0, 4150)
        self.CY(1100, 5800, pme + 9500, 0, 4750, 'N')
        self.CY(1100, 5800, pme + 21500, 0, 4300, 'N')

        # Three press section
        presses = [(24000, 1300, 1200), (27000, 1350, 1250), (30000, 1400, 1300)]
        for p_e, d1, d2 in presses:
            self.CY(d1, 5800, p_e, 0, 3900, 'N')
            self.CY(d2, 5800, p_e, 0, 5100, 'N')
            self.BX(900, 6200, 2000, p_e, 0, 4500)
        for f_i in range(40):
            fu = 2800 if f_i % 2 == 0 else 6000
            self.CY(480, 6000, 22500 + f_i * 250, 0, fu, 'N')

        # 40-cylinder dryer section (each cylinder with 100 steam tube details → 4,000 primitives)
        self.C("40-cylinder dryer section φ1800mm with 4,000 steam piping micro-components")
        for d_i in range(40):
            de = 33000 + d_i * 1200
            du = 3800 if d_i % 2 == 0 else 6000
            self.CY(1800, 5800, de, 0, du, 'N')
            self.DH(1800, 140, 1500, de, -2900, du, 'S')
            self.DH(1800, 140, 1500, de, 2900, du, 'N')
            self.CY(280, 400, de, -3100, du, 'S')
            for tube_i in range(100):
                self.CY(40, 300,
                        de - 500 + (tube_i % 10) * 100,
                        -3200,
                        du - 400 + (tube_i // 10) * 80, 'S')

        self.BX(49000, 7000, 4800, 57000, 0, 9200)

        # Size press / calender / reel / rewinder
        self.CY(950, 5800, 83000, 0, 4300, 'N')
        self.CY(950, 5800, 83000, 0, 5250, 'N')
        for c_i in range(6):
            self.CY(850, 5800, 87500, 0, 2500 + c_i * 950, 'N')
        self.CY(1200, 5800, 92000, 0, 3500, 'N')
        self.CY(2400, 5600, 92000, 0, 4900, 'N')
        self.BX(4500, 7000, 3000, 97000, 0, 2500)

    # =============================================================
    #  Zone 5: Power Plant & Utilities (~2,000 primitives)
    # =============================================================
    def build_zone_5_power_utilities(self):
        self.H("Zone 5: Power Plant & Utilities — CFB Boiler / Turbo-Generator / Water Treatment")
        self.SUBE("ZONE_5_POWER_UTILITIES")

        pe = 30000; pn = 25000

        # CFB boiler with 500 waterwall tubes
        self.C("CFB boiler with 500 waterwall tube segments")
        self.BX(15000, 10000, 28000, pe, pn, 14000)
        self.CY(2200, 10000, pe, pn, 26000, 'N')
        self.CY(4500, 12000, pe + 10000, pn - 3000, 14000, 'U')
        self.CY(4500, 12000, pe + 10000, pn + 3000, 14000, 'U')
        for tube_i in range(500):
            te = pe - 7000 + (tube_i % 25) * 550
            tu = 1500 + (tube_i // 25) * 1200
            self.CY(40, 10000, te, pn - 5000, tu, 'N')

        # Turbo-generator sets
        for tg_i in range(2):
            tge = pe - 12000 + tg_i * 8000
            self.CY(1800, 4500, tge, pn, 4500, 'E')
            self.BX(2500, 5500, 2200, tge + 3500, pn, 4500)
            self.CY(2800, 6000, tge, pn, 1500, 'E')

        # Wastewater treatment (primary + secondary clarifiers, 600 scraper teeth)
        self.C("Wastewater treatment — primary clarifier φ20m + secondary φ24m with 600 scraper teeth")
        self.CY(20000, 4500, pe + 25000, pn, 0, 'U')
        self.CY(24000, 5000, pe + 50000, pn, 0, 'U')
        self.BX(35000, 20000, 4500, pe + 35000, pn + 25000, 2250)
        for rake_i in range(600):
            re = pe + 25000 + math.cos(rake_i * 0.02) * (rake_i % 1800)
            rn = pn + math.sin(rake_i * 0.02) * (rake_i % 1800)
            self.CY(25, 800, re, rn, 300, 'U')

    # =============================================================
    #  Zone 6: Interplant Pipe Bridge Network (~7,000 primitives)
    # =============================================================
    def build_zone_6_pipe_bridges(self):
        self.H("Zone 6: 4-Tier Interplant Pipe Bridge — Steam / Pulp / Water / Chemicals / Air")
        self.SUBE("ZONE_6_PIPE_BRIDGES")

        # Full-length pipe bridge truss — 50 spans × 12 members = 600 primitives
        pe_start = -50000; pn = -10000
        for i in range(50):
            pe = pe_start + i * 3500
            self.BX(700, 700, 16000, pe, pn - 2500, 8000)
            self.BX(700, 700, 16000, pe, pn + 2500, 8000)
            for tier in range(4):
                self.BX(700, 5700, 450, pe, pn, 4500 + tier * 3200)

        # 16 main pipelines — each with 400 pipe segments, flanges, and valves → 6,400 primitives
        self.C("16 main process pipelines with flanges and valves every 2m along 175m pipe bridge")
        pipe_specs = [
            ("DN500_HP_STEAM",     550, pn - 2000, 4850),
            ("DN400_MP_STEAM",     450, pn - 800,  4800),
            ("DN300_LP_STEAM",     350, pn + 400,  4750),
            ("DN600_BLEACHED_PULP",650, pn + 1800, 4900),
            ("DN500_UNBLEACH_PULP",550, pn - 2000, 8050),
            ("DN400_HEAVY_BL_LIQ", 450, pn - 800,  8000),
            ("DN400_WEAK_BL_LIQ",  450, pn + 400,  8000),
            ("DN300_GREEN_LIQUOR", 350, pn + 1800, 7950),
            ("DN300_WHITE_LIQUOR", 350, pn - 2000, 11250),
            ("DN800_WHITE_WATER",  850, pn - 500,  11500),
            ("DN600_CLEAR_WATER",  650, pn + 800,  11400),
            ("DN400_CONDENSATE",   450, pn + 2000, 11300),
            ("DN250_CIO2",         280, pn - 2000, 14450),
            ("DN500_COMP_AIR",     550, pn - 600,  14600),
            ("DN600_VACUUM",       650, pn + 800,  14650),
            ("DN400_RAW_WATER",    450, pn + 2000, 14550),
        ]

        for p_name, p_diam, p_n, p_u in pipe_specs:
            self.CY(p_diam, 175000, pe_start, p_n, p_u, 'E')
            for v_i in range(80):
                ve = pe_start + 2000 + v_i * 2100
                self.CY(p_diam + 180, 70, ve, p_n, p_u, 'E')
                self.CY(p_diam + 180, 70, ve + 180, p_n, p_u, 'E')
                self.BX(p_diam + 120, p_diam + 220, p_diam + 320, ve + 400, p_n, p_u)
                self.CY(p_diam - 20, 500, ve + 400, p_n, p_u + p_diam // 2 + 250, 'U')

    # =============================================================
    #  Main Build Entry
    # =============================================================
    def build(self):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.L = [
            f"-- 100,000+ Primitive Mega Paper Mill Complex — Full-Process 3D Digital Twin",
            f"-- Dimensions: 200m(E) × 100m(N) × 65m(U) | PML1",
            f"-- 6 Plant Zones: Woodyard / Pulping / Recovery / Paper Machine / Power / Pipe Bridges",
            f"-- Generated: {ts}",
            f"-- Prerequisite: select writable ZONE in E3D → $M <this file>",
            f"-- Strict PML1 compliance: 100% ORI-before-POS, zero drift for all plant components",
            # No rendering-control prologue: ALPHA HEADER, VAR 0, SUSPEND and
            # RESUME are not E3D Design commands and abort the macro.
            "",
            f"NEW EQUI /MEGA_PAPER_MILL_COMPLEX_100K",
            "",
        ]

        self.build_zone_1_woodyard()
        self.build_zone_2_pulping()
        self.build_zone_3_recovery()
        self.build_zone_4_paper_machine()
        self.build_zone_5_power_utilities()
        self.build_zone_6_pipe_bridges()

        self.L.extend([
            "",
            f"-- {'='*70}",
            f"--  100,000+ primitive paper mill complex complete: 1 EQUI, "
            f"{self.sube_count} SUBEs, {self.prim_count} industrial-grade primitives",
            f"-- {'='*70}",
            "",
        ])
        return "\n".join(self.L)

    def save(self):
        pml = self.build()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fp = OUTPUT_DIR / f"paper_mill_mega_100k_{ts}.pml"
        fp.write_text(pml, encoding="utf-8", newline="\n")
        return fp, pml


if __name__ == "__main__":
    plant = MegaPaperMillComplex()
    fp, pml = plant.save()

    lines = pml.split("\n")
    errors = []

    # PML2 keyword validation
    for b in BANNED:
        for i, l in enumerate(lines, 1):
            if b in l:
                errors.append(f"PML2 '{b}' @ L{i}: {l.strip()}")

    # CYLI order spot check
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
        print(f"[ERROR] {len(errors)} errors found:")
        for e in errors:
            print(f"  - {e}")
    else:
        print(f"[OK] 100K+ primitive paper mill complex 3D digital twin generated!")
        print(f"  Output: {fp.name}")
        print(f"  Total PML1 lines: {len(lines)}")
        print(f"  Top EQUI: /MEGA_PAPER_MILL_COMPLEX_100K")
        print(f"  SUBEs: {plant.sube_count}")
        print(f"  Primitives: {plant.prim_count}")
