#!/usr/bin/env python3
"""
PM1 Paper Machine High-Precision Model v3
===========================================
4800mm fourdrinier multi-cylinder paper machine.
Sections: headbox / wire / press / dryer / size press / calender / reel.

Based on real paper machine engineering data:
  - Dryer cylinders: dia 1800mm (industry most common)
  - Dryer pitch: 2400mm
  - 40 dryer cylinders (20 top + 20 bottom, 2-tier)
  - 3 press nips with increasing nip load
  - Tapered hydraulic headbox with inlet manifold
  - Full walkways, handrails, and drive-side platform
"""

from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BANNED = ["!!Alert", "$P", "ENDS", "END EQUI", "NAME =", "DESC =",
          "!var =", "COLLECT", "UNSET", "!!CE", "!!WORLD"]


class PM1PaperMachine:
    """4800mm Fourdrinier Paper Machine — High-Precision PML1 Generator"""

    # -- Basic Parameters (mm) --
    TRIM = 4800
    WIRE_W = 5200
    FRAME_W = 5800
    NW = FRAME_W // 2 + 400    # North frame column coordinate
    SW = -(FRAME_W // 2 + 400) # South frame column coordinate

    # -- Key Elevations (U, mm) --
    FLOOR = 0
    WALKWAY = 1800
    WIRE_EL = 3500           # Fourdrinier wire table elevation
    PRESS_BASE = 2700        # Press section base elevation
    DRY_BOT = 3800           # Bottom dryer row shaft center U
    DRY_TOP = 6000           # Top dryer row shaft center U
    SP_EL = 3500             # Size press base
    CAL_BOT = 500            # Calender bottom roll
    REEL_EL = 1500           # Reel drum shaft center

    # -- Wire Section Parameters --
    BREAST_D = 800
    TABLE_D = 320
    TABLE_N = 18
    TABLE_SP = 600
    DANDY_D = 800
    DANDY_E = 8500
    SUCT_N = 8
    SUCT_W = 280
    SUCT_START = 11800
    COUCH_D = 1000
    COUCH_E = 17500
    WIRE_RETURN_D = 500

    # -- Press Section --
    P1_E = 19500; P1_D_BOT = 900;  P1_D_TOP = 800
    P2_E = 22000; P2_D_BOT = 1000; P2_D_TOP = 900
    P3_E = 24500; P3_D_BOT = 1200; P3_D_TOP = 1000
    FELT_D = 500

    # -- Dryer Section (Industry Standard: φ1800, pitch 2400) --
    D_START = 26000
    D_DIAM = 1800            # Most common dryer diameter
    D_FACE = 5400            # trim + 600mm
    D_N = 40                 # 40 cylinders (20 top + 20 bottom)
    D_PITCH = 2400           # Standard pitch
    D_HALF = D_N // 2        # 20 per row
    D_RET_D = 700            # Dryer fabric return roll

    # -- Size Press / Calender / Reel --
    SP_E = 62000; SP_D = 900
    CAL_E = 65000; CAL_D = 800; CAL_N = 6; CAL_P = 900
    REEL_E = 66500; REEL_D = 1100; SPOOL_D = 450

    def __init__(self):
        self.L = []; self.n = 0

    def H(self, title):
        self.L.extend(["", f"-- {'='*60}", f"--  {title}", f"-- {'='*60}", ""])

    def C(self, text):
        self.L.append(f"-- {text}")

    # -- Primitive Helpers (PML1 Compliant) --
    def CY(self, name, d, h, e=0, n=0, u=0, ax='N'):
        """CYLI: dia x height, axis=N (CD) / E (MD) / U (vertical). ORI before POS."""
        self.n += 1
        s = name.replace(" ", "_").replace("/", "_").replace("-", "_")
        self.L.append(f"NEW EQUI /{s}")
        self.L.append("NEW CYLI")
        self.L.append(f"DIAM {d}")
        self.L.append(f"HEIG {h}")
        self.L.append(f"ORI Z IS {ax} AND Y IS U")
        self.L.append(f"POS E {e} N {n} U {u}")
        self.L.append("")
        return s

    def BX(self, name, x, y, z, e=0, n=0, u=0):
        """BOX: XLEN=E YLEN=N ZLEN=U, POS=geometric center."""
        self.n += 1
        s = name.replace(" ", "_").replace("/", "_").replace("-", "_")
        self.L.append(f"NEW EQUI /{s}")
        self.L.append("NEW BOX")
        self.L.append(f"XLEN {x}")
        self.L.append(f"YLEN {y}")
        self.L.append(f"ZLEN {z}")
        self.L.append(f"POS E {e} N {n} U {u}")
        self.L.append("")
        return s

    def CN(self, name, dtop, dbot, h, e=0, n=0, u=0, ax='N'):
        """CONE: tapered frustum. ORI before POS."""
        self.n += 1
        s = name.replace(" ", "_").replace("/", "_").replace("-", "_")
        self.L.append(f"NEW EQUI /{s}")
        self.L.append("NEW CONE")
        self.L.append(f"DTOP {dtop}")
        self.L.append(f"DBOT {dbot}")
        self.L.append(f"HEIG {h}")
        self.L.append(f"ORI Z IS {ax} AND Y IS U")
        self.L.append(f"POS E {e} N {n} U {u}")
        self.L.append("")
        return s

    def roll(self, name, d, e, n=0, u=3500, face=None):
        """Transverse roll (cross-machine axis)."""
        return self.CY(name, d, face or self.WIRE_W + 400, e, n, u, 'N')

    def col(self, name, h, e, n, u_base, w=600):
        """Structural column: square hollow section."""
        return self.BX(name, w, w, h, e, n, u_base + h // 2)

    def beam(self, name, length, h, e, n, u, w=350):
        """Structural beam: I-beam approximation."""
        return self.BX(name, length, w, h, e, n, u)

    def soleplate(self, name, e, n):
        """Base plate / soleplate."""
        return self.BX(name, 1000, 800, 300, e, n, 150)

    # =============================================================
    #  1. Hydraulic Headbox
    # =============================================================
    def headbox(self):
        self.H("1. Hydraulic Headbox")
        hb_e = -1200; hb_u = self.WIRE_EL + 500

        # Tapered inlet header (manifold) — CONE
        self.CN("PM1_HDBX_MANIFOLD", 200, 700, 5500, hb_e - 300, -2750, hb_u + 200, 'N')
        # Main chamber body
        self.BX("PM1_HDBX_CHAMBER", 500, self.WIRE_W + 300, 700, hb_e + 100, 0, hb_u)
        # Top lip
        self.BX("PM1_HDBX_TOP_LIP", 300, self.WIRE_W, 80, hb_e + 500, 0, hb_u + 350)
        # Bottom lip
        self.BX("PM1_HDBX_BOT_LIP", 300, self.WIRE_W, 80, hb_e + 500, 0, hb_u - 450)
        # Air pad dome
        self.CY("PM1_HDBX_AIR_DOME", self.WIRE_W, 300, hb_e + 100, 0, hb_u + 500, 'U')
        # Dilution water header
        self.roll("PM1_HDBX_DILUTION", 150, hb_e, 0, hb_u + 900, self.WIRE_W + 200)
        # Support stands
        self.col("PM1_HDBX_STAND_N", 2500, hb_e, self.NW - 300, 1000)
        self.col("PM1_HDBX_STAND_S", 2500, hb_e, self.SW + 300, 1000)
        self.C("  Headbox: manifold (CONE) + chamber + lips + dome + dilution header + stands x2")

    # =============================================================
    #  2. Fourdrinier Wire Section
    # =============================================================
    def wire_section(self):
        self.H("2. Wire Section (Fourdrinier Table)")
        wu = self.WIRE_EL; fw = self.WIRE_W + 300

        # 2.1 Breast roll
        self.roll("PM1_BREAST_ROLL", self.BREAST_D, 0, 0, wu, fw)

        # 2.2 Forming board (5 strips)
        for i in range(5):
            self.BX(f"PM1_FORMING_BRD_{i+1}", 200, self.WIRE_W - 200, 100,
                    800 + i * 250, 0, wu - 60)

        # 2.3 Table rolls
        for i in range(self.TABLE_N):
            ep = 1500 + i * self.TABLE_SP
            self.roll(f"PM1_TABLE_ROLL_{i+1:02d}", self.TABLE_D, ep, 0,
                      wu - self.TABLE_D // 2, self.WIRE_W + 150)
        self.C(f"  Table rolls: {self.TABLE_N} × dia{self.TABLE_D}mm @{self.TABLE_SP}mm pitch")

        # 2.4 Foil blades (12 narrow strips)
        foil_start = 1500 + self.TABLE_N * self.TABLE_SP + 500
        for i in range(12):
            self.BX(f"PM1_FOIL_{i+1:02d}", 80, self.WIRE_W - 300, 60,
                    foil_start + i * 250, 0, wu - 40)

        # 2.5 Dandy roll
        self.roll("PM1_DANDY_ROLL", self.DANDY_D, self.DANDY_E, 0,
                  wu + self.DANDY_D // 2, self.WIRE_W + 200)
        self.col("PM1_DANDY_STAND_N", 2500, self.DANDY_E, self.NW - 200, self.WIRE_EL - 400)
        self.col("PM1_DANDY_STAND_S", 2500, self.DANDY_E, self.SW + 200, self.WIRE_EL - 400)

        # 2.6 Wet suction boxes
        for i in range(self.SUCT_N):
            ep = self.SUCT_START + i * (self.SUCT_W + 250)
            self.BX(f"PM1_SUCT_BOX_{i+1}", self.SUCT_W, self.WIRE_W - 400, 400,
                    ep, 0, wu - 200)
        self.C(f"  Vacuum suction boxes: {self.SUCT_N} units")

        # 2.7 Couch roll
        self.roll("PM1_COUCH_ROLL", self.COUCH_D, self.COUCH_E, 0, wu, fw)

        # 2.8 Under-table wire return rolls
        for i in range(5):
            self.roll(f"PM1_WIRE_RET_{i+1}", self.WIRE_RETURN_D,
                      2000 + i * 3200, 0, wu - 2200, self.WIRE_W + 200)

        # 2.9 Wire table frame (longitudinal rails + columns)
        wl_end = self.COUCH_E + 1000
        for side, ns in [("N", self.NW), ("S", self.SW)]:
            self.beam(f"PM1_WIRE_RAIL_LO_{side}", wl_end + 1000, 450,
                      wl_end // 2 - 500, ns - 100, 1200, 350)
            self.beam(f"PM1_WIRE_RAIL_HI_{side}", wl_end + 1000, 350,
                      wl_end // 2 - 500, ns - 100, wu + 300, 280)
            for i in range(0, wl_end, 3000):
                self.soleplate(f"PM1_WIRE_SP_{side}_{i//3000+1:02d}", i, ns)
                self.col(f"PM1_WIRE_COL_{side}_{i//3000+1:02d}", wu + 800, i, ns, 300, 450)
        self.C("  Wire table frame: rails × 4 + columns + soleplates")

    # =============================================================
    #  3. Press Section (3 Nips)
    # =============================================================
    def press_section(self):
        self.H("3. Press Section — 3 Press Nips")
        bu = self.PRESS_BASE

        press_configs = [
            (self.P1_E, self.P1_D_BOT, self.P1_D_TOP, "P1"),
            (self.P2_E, self.P2_D_BOT, self.P2_D_TOP, "P2"),
            (self.P3_E, self.P3_D_BOT, self.P3_D_TOP, "P3"),
        ]

        for pe, d_bot, d_top, tag in press_configs:
            # Bottom press roll
            self.roll(f"PM1_{tag}_BOT", d_bot, pe, 0, bu, self.WIRE_W + 600)
            # Top press roll (correctly stacked)
            top_u = bu + d_bot / 2 + d_top / 2
            self.roll(f"PM1_{tag}_TOP", d_top, pe, 0, top_u, self.WIRE_W + 600)

        self.C("  3 press nips: P1(φ900+φ800), P2(φ1000+φ900), P3(φ1200+φ1000)")

        # Felt guide rolls (4-6 per nip)
        for tag, pe in [("P1", self.P1_E), ("P2", self.P2_E), ("P3", self.P3_E)]:
            for j in range(4):
                self.roll(f"PM1_FELT_{tag}_{j+1}", self.FELT_D,
                          pe - 1200 + j * 800, 0, bu - 500, self.TRIM + 400)

        # Uhle boxes (2 per press nip)
        for tag, pe in [("P1", self.P1_E), ("P2", self.P2_E), ("P3", self.P3_E)]:
            self.BX(f"PM1_UHLE_{tag}_1", 200, self.TRIM - 400, 300, pe - 500, 0, bu - 800)
            self.BX(f"PM1_UHLE_{tag}_2", 200, self.TRIM - 400, 300, pe + 500, 0, bu - 800)

        # Press frames
        for pe in [self.P1_E, self.P2_E, self.P3_E]:
            for ns in [self.NW, self.SW]:
                self.col(f"PM1_PRESS_COL_{pe}_{ns}", 4000, pe, ns, bu - 500, 700)
                self.soleplate(f"PM1_PRESS_SP_{pe}_{ns}", pe, ns)
        self.C("  Press frames: columns × 6 + soleplates × 6")

    # =============================================================
    #  4. Dryer Section (40 Cylinders, φ1800, 2-Tier)
    # =============================================================
    def dryer_section(self):
        self.H("4. Dryer Section — 40 Cylinders φ1800mm × 5400mm Face")
        df = self.D_FACE

        # 4.1 Dryer cylinders: 20 top + 20 bottom, interleaved
        for i in range(self.D_HALF):
            ep = self.D_START + i * self.D_PITCH
            # Bottom row (U = 3800)
            self.roll(f"PM1_DRYER_LO_{i+1:02d}", self.D_DIAM, ep, 0, self.DRY_BOT, df)
            # Top row (U = 6000)
            self.roll(f"PM1_DRYER_HI_{i+1:02d}", self.D_DIAM, ep, 0, self.DRY_TOP, df)
        self.C(f"  Dryer cylinders: {self.D_N} units φ{self.D_DIAM}mm × {df}mm face, "
               f"@{self.D_PITCH}mm pitch")

        # 4.2 Doctor blades (thin strip behind each cylinder)
        for i in range(self.D_HALF):
            ep = self.D_START + i * self.D_PITCH
            self.BX(f"PM1_DOCTOR_HI_{i+1:02d}", 80, df - 200, 100,
                    ep + self.D_DIAM // 2 + 50, 0, self.DRY_TOP + self.D_DIAM // 2 - 50)
            self.BX(f"PM1_DOCTOR_LO_{i+1:02d}", 80, df - 200, 100,
                    ep + self.D_DIAM // 2 + 50, 0, self.DRY_BOT + self.D_DIAM // 2 - 50)
        self.C(f"  Doctor blades: {self.D_N} units")

        # 4.3 Dryer fabric return rolls
        for i in range(0, self.D_HALF, 2):
            ep = self.D_START + i * self.D_PITCH
            self.roll(f"PM1_FABRET_HI_{i//2+1}", self.D_RET_D, ep, 0,
                      self.DRY_TOP + self.D_DIAM + 300, df - 400)
            self.roll(f"PM1_FABRET_LO_{i//2+1}", self.D_RET_D, ep, 0,
                      self.DRY_BOT - self.D_DIAM - 300, df - 400)

        # 4.4 Rotary steam joints (both ends of each cylinder)
        for i in range(self.D_HALF):
            ep = self.D_START + i * self.D_PITCH
            for ns, nv in [("N", df // 2 + 150), ("S", -df // 2 - 150)]:
                # Top row
                self.CY(f"PM1_STEAM_HI_{i+1:02d}_{ns}", 200, 600, ep, nv,
                        self.DRY_TOP + self.D_DIAM // 2, 'E')
                # Bottom row
                self.CY(f"PM1_STEAM_LO_{i+1:02d}_{ns}", 200, 600, ep, nv,
                        self.DRY_BOT + self.D_DIAM // 2, 'E')

        # 4.5 Rope sheaves (drive side threading system)
        for i in range(self.D_HALF):
            ep = self.D_START + i * self.D_PITCH
            self.roll(f"PM1_ROPE_HI_{i+1:02d}", 300, ep, self.NW - 100, self.DRY_TOP, 100)
            self.roll(f"PM1_ROPE_LO_{i+1:02d}", 300, ep, self.NW - 100, self.DRY_BOT, 100)

        # 4.6 Dryer section frame
        dryer_end = self.D_START + (self.D_HALF - 1) * self.D_PITCH
        frame_h = self.DRY_TOP + self.D_DIAM // 2 + 600
        for i in range(0, self.D_HALF, 2):
            ep = self.D_START + i * self.D_PITCH
            for ns in [self.NW + 100, self.SW - 100]:
                self.col(f"PM1_DRY_FRM_{i//2+1:02d}_{ns}", frame_h, ep, ns, frame_h // 2, 550)
                self.soleplate(f"PM1_DRY_SP_{i//2+1:02d}_{ns}", ep, ns)
        self.C(f"  Dryer frame: columns × {self.D_HALF} + soleplates")

        # 4.7 Dryer hood
        hood_len = dryer_end - self.D_START + 3000
        self.BX("PM1_HOOD", hood_len, self.FRAME_W + 1000, 2200,
                (self.D_START + dryer_end) // 2, 0, self.DRY_TOP + self.D_DIAM // 2 + 1100)
        self.C(f"  Dryer hood: {hood_len}mm L × {self.FRAME_W + 1000}mm W × 2200mm H")

    # =============================================================
    #  5. Size Press
    # =============================================================
    def size_press(self):
        self.H("5. Size Press")
        # Roll pair
        self.roll("PM1_SP_TOP", self.SP_D, self.SP_E, 0,
                  self.SP_EL + self.SP_D, self.TRIM + 400)
        self.roll("PM1_SP_BOT", self.SP_D, self.SP_E, 0, self.SP_EL, self.TRIM + 400)
        # Starch supply header
        self.roll("PM1_SP_SUPPLY", 100, self.SP_E, self.NW - 400,
                  self.SP_EL + self.SP_D + 200, self.TRIM)
        # Frame
        for ns in [self.NW, self.SW]:
            self.col(f"PM1_SP_FRM_{ns}", 5000, self.SP_E, ns, self.SP_EL - 500, 700)
            self.soleplate(f"PM1_SP_SP_{ns}", self.SP_E, ns)
        self.C("  Size press: 2 rolls φ900mm + starch supply pipe + frame")

    # =============================================================
    #  6. Calender Stack (6 rolls, vertical)
    # =============================================================
    def calender(self):
        self.H("6. Calender Stack — 6 Rolls")
        for i in range(self.CAL_N):
            ru = self.CAL_BOT + i * self.CAL_P + self.CAL_D // 2
            self.roll(f"PM1_CAL_R{i+1}", self.CAL_D, self.CAL_E, 0, ru, self.TRIM + 300)
        # Frame
        ft = self.CAL_BOT + (self.CAL_N - 1) * self.CAL_P + self.CAL_D + 600
        for ns in [self.NW - 100, self.SW + 100]:
            self.col(f"PM1_CAL_FRM_{ns}", ft, self.CAL_E, ns, ft // 2, 750)
            self.soleplate(f"PM1_CAL_SP_{ns}", self.CAL_E, ns)
        self.C(f"  Calender: {self.CAL_N} rolls φ{self.CAL_D}mm vertical stack + frame")

    # =============================================================
    #  7. Reel
    # =============================================================
    def reel(self):
        self.H("7. Pope Reel")
        # Reel drum
        self.roll("PM1_REEL_DRUM", self.REEL_D, self.REEL_E, 0,
                  self.REEL_EL + self.REEL_D // 2, self.TRIM + 300)
        # Primary spool (empty)
        self.roll("PM1_REEL_SPOOL", self.SPOOL_D, self.REEL_E + 800, 0,
                  self.REEL_EL + self.REEL_D + 200, self.TRIM + 400)
        # Full parent reel
        self.roll("PM1_PARENT_REEL", 2200, self.REEL_E + 1200, 0,
                  self.REEL_EL + self.REEL_D + 600, self.TRIM - 200)
        # Rider roll
        self.roll("PM1_REEL_RIDER", 400, self.REEL_E + 1000, 0,
                  self.REEL_EL + self.REEL_D + 1100, self.TRIM + 200)
        # Frame
        for ns in [self.NW, self.SW]:
            self.col(f"PM1_REEL_FRM_{ns}", 6000, self.REEL_E + 700, ns, 3000, 700)
            self.soleplate(f"PM1_REEL_SP_{ns}", self.REEL_E + 700, ns)
        self.C("  Reel: reel drum φ1100mm + spool + full parent reel + rider roll + frame")

    # =============================================================
    #  8. Walkways & Handrails
    # =============================================================
    def walkways(self):
        self.H("8. Walkways & Safety Handrails")
        ml = self.REEL_E + 3000
        ww = 1200

        for side, ns, hn in [("N", self.NW + ww // 2 + 300, self.NW + ww + 300),
                             ("S", self.SW - ww // 2 - 300, self.SW - ww - 300)]:
            # Walkway deck (grating)
            self.BX(f"PM1_WALKWAY_{side}", ml, ww, 100, ml // 2 - 500, ns, self.WALKWAY)
            # Handrail posts (every 4000mm)
            for i in range(0, ml, 4000):
                self.col(f"PM1_RAIL_COL_{side}_{i//4000+1:02d}", 1100, i, hn,
                         self.WALKWAY + 550, 80)
            # Top + mid rails
            self.beam(f"PM1_RAIL_TOP_{side}", ml, 60, ml // 2 - 500, hn,
                      self.WALKWAY + 1100, 60)
            self.beam(f"PM1_RAIL_MID_{side}", ml, 60, ml // 2 - 500, hn,
                      self.WALKWAY + 700, 60)
        self.C("  Walkways × 2 + handrails (top + mid rails) + posts at 4m spacing")

    # =============================================================
    #  9. Foundation & Drive-Side Platform
    # =============================================================
    def foundation(self):
        self.H("9. Foundation & Drive-Side Platform")
        ml = self.REEL_E + 3000

        # Main machine foundation
        self.BX("PM1_FOUNDATION", ml, self.FRAME_W + 4000, 600,
                ml // 2 - 500, 0, -300)
        self.C(f"  Foundation slab: {ml}mm L × {self.FRAME_W + 4000}mm W × 600mm H")

        # Drive side motor platform
        ds = self.D_START + (self.D_HALF // 2) * self.D_PITCH
        self.BX("PM1_MOTOR_DECK", 6000, 3000, 300, ds, self.NW + 2000, self.WALKWAY)
        # Drive motor (simplified)
        self.CY("PM1_DRIVE_MOTOR", 800, 2500, ds - 1500, self.NW + 2500,
                self.WALKWAY + 300, 'E')
        self.BX("PM1_MOTOR_GEARBOX", 1500, 1200, 1000, ds, self.NW + 2500,
                self.WALKWAY + 500)
        self.C("  Drive-side: motor platform + drive motor + gearbox")

        # Vacuum pump platform (wet end)
        self.BX("PM1_VAC_DECK", 5000, 3000, 300, 8000, self.NW + 2000, self.WALKWAY)
        self.BX("PM1_VAC_PUMP", 3000, 1500, 1800, 8000, self.NW + 2500, self.WALKWAY + 900)

    # =============================================================
    #  Main Build Entry
    # =============================================================
    def build(self):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.L = [
            f"-- PM1 Paper Machine High-Precision Model v3 — 4800mm Fourdrinier",
            f"-- Specs: trim={self.TRIM}mm, wire={self.WIRE_W}mm, {self.D_N} dryer cylinders φ{self.D_DIAM}mm",
            f"-- Dryer pitch={self.D_PITCH}mm, face={self.D_FACE}mm, 2-tier arrangement",
            f"-- Generated: {ts} | Data baseline: industrial fourdrinier multi-cylinder paper machine",
            "-- Prerequisite: select writable ZONE in E3D → $$MACRO <this file>",
            "-- Units: mm | E=machine direction | N=cross-machine | U=vertical",
            "",
        ]
        self.headbox()
        self.foundation()
        self.wire_section()
        self.press_section()
        self.dryer_section()
        self.size_press()
        self.calender()
        self.reel()
        self.walkways()
        self.L.extend([
            "", f"-- == PM1 complete: {self.n} EQUIPMENT ==", ""
        ])
        return "\n".join(self.L)

    def save(self):
        pml = self.build()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fp = OUTPUT_DIR / f"paper_machine_pm1_{ts}.pml"
        fp.write_text(pml, encoding="utf-8", newline="\n")
        return fp, pml


if __name__ == "__main__":
    b = PM1PaperMachine()
    fp, pml = b.save()

    # Self-check
    errors = []
    lines = pml.split("\n")
    for banned in BANNED:
        for i, l in enumerate(lines, 1):
            if banned in l:
                errors.append(f"PML2 violation '{banned}' @ L{i}: {l.strip()}")

    # Check ORI-before-POS for CYLI
    cyli_lines = [i for i, l in enumerate(lines) if l.strip() == "NEW CYLI"]
    for idx in cyli_lines:
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
        print(f"[OK] {fp}")
        print(f"     {len(lines)} lines | {b.n} EQUIPMENT | PML1 ✓")
        print("\n".join(pml.split("\n")[:15]))
