#!/usr/bin/env python3
"""
化工精馏塔装置 — 苯-甲苯精馏系统
===================================
工装级精细模型 | DN2400 | 40层浮阀塔盘 | 25.5m总高
含: 精馏塔/再沸器E-101/冷凝器E-102/回流罐V-101/管口法兰/钢平台/爬梯/护栏

使用 E3D 3.1 全部 4 种验证基本体:  CYLI ✅  BOX ✅  CONE ✅  DISH ✅

坐标系: EAST=东(+E)  NORTH=北(+N)  UP=上(+U)
塔中心: E=0, N=0  |  地面: U=0
单位: mm
"""

from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(r"D:\AVEVA\Projects\E3D3.1\e3d_agent\output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BANNED = ["!!Alert", "$P", "ENDS", "END EQUI", "NAME =", "DESC =",
          "!var =", "COLLECT", "UNSET", "!!CE", "!!WORLD"]


class DistillationColumn:
    """苯-甲苯精馏塔装置完整模型 — ~160 EQUI"""

    # ═══ 塔体几何 ═══
    SHELL_OD = 2440;   SHELL_ID = 2400;   SHELL_THK = 20
    SEG_N    = 5;      SEG_H    = 4000;   SHELL_H   = 20000   # 5段×4m

    # ═══ 裙座 ═══
    SKIRT_OD   = 2500;  SKIRT_H    = 4000
    BASE_OD    = 3200;  BASE_H     = 80
    ANCHOR_OD  = 2900;  ANCHOR_H   = 40
    TRANS_H    = 200    # CONE 过渡段

    # ═══ 封头 (2:1 椭圆) ═══
    HEAD_D = 2440;  HEAD_H = 610;  HEAD_R = 2440

    # ═══ 塔盘 ═══
    TRAY_N = 40;  TRAY_D = 2380;  TRAY_THK = 10;  TRAY_PITCH = 500
    FEED_TRAY = 20

    # ═══ 管口 / 法兰 ═══
    NZ_L = 300;  FL_EXTRA = 150;  FL_THK = 30
    MH_D = 600;  MH_L = 200

    # ═══ 加强环 ═══
    RING_OD = 2600;  RING_H = 100

    # ═══ 再沸器 E-101 ═══
    REB_D = 1200;  REB_L = 4000;  REB_TUBE_D = 1100;  REB_TUBE_L = 3600
    REB_BAFFLE_N = 2;  REB_BAFFLE_THK = 15

    # ═══ 冷凝器 E-102 ═══
    COND_D = 1000;  COND_L = 3500

    # ═══ 回流罐 V-101 ═══
    DRUM_D = 1200;  DRUM_L = 3000;  DRUM_HEAD_H = 300

    # ═══ 平台 / 爬梯 ═══
    PLAT_W = 1200;  PLAT_THK = 50;  HR_H = 1100

    def __init__(self):
        self.L = [];  self.n = 0;  self.names = set()

        # ── 标高计算 (从地面 U=0 往上) ──
        self.U_BASE      = 0                                        # 底座环底
        self.U_SKIRT     = self.BASE_H                              # 80
        self.U_SKIRT_TOP = self.U_SKIRT + self.SKIRT_H              # 4080
        self.U_TRANS_TOP = self.U_SKIRT_TOP + self.TRANS_H          # 4280
        self.U_BHEAD     = self.U_TRANS_TOP                         # 下封头底
        self.U_SHELL     = self.U_BHEAD + self.HEAD_H               # 4890
        self.U_SHELL_TOP = self.U_SHELL + self.SHELL_H              # 24890
        self.U_THEAD     = self.U_SHELL_TOP                         # 上封头底
        self.U_TOP       = self.U_THEAD + self.HEAD_H               # 25500
        self.U_TRAY1     = self.U_SHELL + 400                       # 5290
        self.U_FEED      = self.U_TRAY1 + (self.FEED_TRAY - 1) * self.TRAY_PITCH
        self.R           = self.SHELL_OD // 2                       # 1220

    # ════════════════════════════════════════
    #  基元助手
    # ════════════════════════════════════════
    def H(self, t):
        self.L.extend(["", f"-- {'='*60}", f"--  {t}", f"-- {'='*60}", ""])

    def C(self, t):
        self.L.append(f"-- {t}")

    def _add(self, name):
        s = name.replace(" ", "_").replace("-", "_").replace("/", "_")
        if s in self.names:
            raise ValueError(f"EQUI 重名: {s}")
        self.names.add(s);  self.n += 1
        return s

    def CY(self, name, d, h, e=0, n=0, u=0, axis='U'):
        """CYLI — axis: U=竖直, E=水平东, N=水平北"""
        s = self._add(name)
        z = 'N' if axis == 'U' else 'U'
        self.L += [f"NEW EQUI /{s}", "NEW CYLI",
                   f"DIAM {d}", f"HEIG {h}",
                   f"POS E {e} N {n} U {u}",
                   f"ORI Y IS {axis} AND Z IS {z}", ""]
        return s

    def BX(self, name, x, y, z, e=0, n=0, u=0):
        """BOX — XLEN=E, YLEN=N, ZLEN=U, POS=几何中心"""
        s = self._add(name)
        self.L += [f"NEW EQUI /{s}", "NEW BOX",
                   f"XLEN {x}", f"YLEN {y}", f"ZLEN {z}",
                   f"POS E {e} N {n} U {u}", ""]
        return s

    def CN(self, name, dtop, dbot, h, e=0, n=0, u=0, axis='U'):
        """CONE — dtop/dbot 上下径, axis 同 CYLI"""
        s = self._add(name)
        z = 'N' if axis == 'U' else 'U'
        self.L += [f"NEW EQUI /{s}", "NEW CONE",
                   f"DTOP {dtop}", f"DBOT {dbot}", f"HEIG {h}",
                   f"POS E {e} N {n} U {u}",
                   f"ORI Y IS {axis} AND Z IS {z}", ""]
        return s

    def DH(self, name, d, h, r, e=0, n=0, u=0, axis='U'):
        """DISH — 碟形封头, axis 同 CYLI"""
        s = self._add(name)
        z = 'N' if axis == 'U' else 'U'
        self.L += [f"NEW EQUI /{s}", "NEW DISH",
                   f"DIAM {d}", f"HEIG {h}", f"RADIUS {r}",
                   f"POS E {e} N {n} U {u}",
                   f"ORI Y IS {axis} AND Z IS {z}", ""]
        return s

    def nozzle(self, name, d, e, n, u, axis='E'):
        """管口+法兰 (2 EQUI): CYLI管段 + CYLI法兰盘"""
        self.CY(name, d, self.NZ_L, e, n, u, axis)
        if axis == 'E':   fe, fn, fu = e + self.NZ_L, n, u
        elif axis == 'N': fe, fn, fu = e, n + self.NZ_L, u
        else:             fe, fn, fu = e, n, u + self.NZ_L  # U
        self.CY(f"{name}_FL", d + self.FL_EXTRA, self.FL_THK, fe, fn, fu, axis)

    # ════════════════════════════════════════
    #  1. 裙座
    # ════════════════════════════════════════
    def skirt(self):
        self.H("1. 裙座 Skirt  (4 EQUI)")
        # 底座环板
        self.CY("T101_BASE_RING", self.BASE_OD, self.BASE_H,
                0, 0, self.U_BASE)
        # 地脚螺栓环
        self.CY("T101_ANCHOR_RING", self.ANCHOR_OD, self.ANCHOR_H,
                0, 0, self.U_BASE + 20)
        # 裙座筒体
        self.CY("T101_SKIRT", self.SKIRT_OD, self.SKIRT_H,
                0, 0, self.U_SKIRT)
        # 裙座→塔壳过渡段 CONE
        self.CN("T101_TRANSITION", self.SHELL_OD, self.SKIRT_OD, self.TRANS_H,
                0, 0, self.U_SKIRT_TOP)
        self.C(f"  裙座: φ{self.SKIRT_OD}×{self.SKIRT_H} + CONE过渡")

    # ════════════════════════════════════════
    #  2. 下封头
    # ════════════════════════════════════════
    def bottom_head(self):
        self.H("2. 下封头 Bottom Head  (3 EQUI)")
        # 2:1 椭圆封头 DISH
        self.DH("T101_BOTTOM_HEAD", self.HEAD_D, self.HEAD_H, self.HEAD_R,
                0, 0, self.U_BHEAD)
        # 排液管口+法兰
        self.nozzle("T101_N_DRAIN", 100, self.R, 0, self.U_SHELL + 100, 'E')
        self.C(f"  下封头 DISH φ{self.HEAD_D} H={self.HEAD_H} + 排液口 DN100")

    # ════════════════════════════════════════
    #  3. 塔壳 + 加强环
    # ════════════════════════════════════════
    def shell(self):
        self.H(f"3. 塔壳 Column Shell  ({self.SEG_N}段 + 3加强环 = 8 EQUI)")
        # 5 段等径筒体
        for i in range(self.SEG_N):
            u = self.U_SHELL + i * self.SEG_H
            self.CY(f"T101_SHELL_{i+1:02d}", self.SHELL_OD, self.SEG_H,
                    0, 0, u)
        self.C(f"  塔壳 {self.SEG_N}×φ{self.SHELL_OD}×{self.SEG_H}")
        # 3 道外加强环
        for i, u in enumerate([10000, 16000, 22000]):
            self.CY(f"T101_STIFF_RING_{i+1}", self.RING_OD, self.RING_H,
                    0, 0, u)
        self.C(f"  加强环 ×3 φ{self.RING_OD}×{self.RING_H}")

    # ════════════════════════════════════════
    #  4. 上封头
    # ════════════════════════════════════════
    def top_head(self):
        self.H("4. 上封头 Top Head  (1 EQUI)")
        self.DH("T101_TOP_HEAD", self.HEAD_D, self.HEAD_H, self.HEAD_R,
                0, 0, self.U_THEAD)
        self.C(f"  上封头 DISH φ{self.HEAD_D} H={self.HEAD_H}")

    # ════════════════════════════════════════
    #  5. 塔盘
    # ════════════════════════════════════════
    def trays(self):
        self.H(f"5. 塔盘 Trays  ({self.TRAY_N} EQUI)")
        for i in range(self.TRAY_N):
            u = self.U_TRAY1 + i * self.TRAY_PITCH
            tag = "FEED" if i + 1 == self.FEED_TRAY else ""
            self.CY(f"T101_TRAY_{i+1:02d}", self.TRAY_D, self.TRAY_THK,
                    0, 0, u)
        self.C(f"  塔盘 ×{self.TRAY_N} φ{self.TRAY_D}×{self.TRAY_THK}"
               f" @{self.TRAY_PITCH}间距")
        self.C(f"  进料塔盘 #{self.FEED_TRAY} U={self.U_FEED}")

    # ════════════════════════════════════════
    #  6. 工艺管口 + 法兰
    # ════════════════════════════════════════
    def column_nozzles(self):
        self.H("6. 工艺管口 Nozzles  (8×2 = 16 EQUI)")
        R = self.R
        nz = [
            # (name, diam, e, n, u, axis, description)
            ("T101_N01_FEED",      300, R,  0, self.U_FEED,           'E', "进料"),
            ("T101_N02_OVERHEAD",  500, 0,  0, self.U_TOP,            'U', "塔顶蒸气"),
            ("T101_N03_BOTTOM",    300, R,  0, self.U_SHELL + 200,    'E', "塔底液出"),
            ("T101_N04_REFLUX",    200, R,  0, self.U_SHELL_TOP - 400,'E', "回流入口"),
            ("T101_N05_REB_VAP",   400, R,  0, self.U_SHELL + 900,   'E', "再沸蒸气回"),
            ("T101_N06_REB_LIQ",   300, R,  0, self.U_SHELL + 400,   'E', "再沸液出"),
            ("T101_N07_THERMO",     50, 0,  R, 12000,                 'N', "温度计"),
            ("T101_N08_PRESS",      50, 0,  R, 20000,                 'N', "压力计"),
        ]
        for name, d, e, n, u, axis, desc in nz:
            self.C(f"  {desc}: DN{d} {axis}方向 U={u}")
            self.nozzle(name, d, e, n, u, axis)

    # ════════════════════════════════════════
    #  7. 人孔 + 法兰
    # ════════════════════════════════════════
    def manholes(self):
        self.H("7. 人孔 Manholes  (4×2 = 8 EQUI)")
        R = self.R
        mh = [
            ("T101_MH01", R,  0, 8000,  'E'),
            ("T101_MH02", 0,  R, 13000, 'N'),
            ("T101_MH03", R,  0, 18000, 'E'),
            ("T101_MH04", 0,  R, 23000, 'N'),
        ]
        for name, e, n, u, axis in mh:
            self.CY(name, self.MH_D, self.MH_L, e, n, u, axis)
            if axis == 'E':   fe, fn, fu = e + self.MH_L, n, u
            elif axis == 'N': fe, fn, fu = e, n + self.MH_L, u
            else:             fe, fn, fu = e, n, u + self.MH_L
            self.CY(f"{name}_FL", self.MH_D + self.FL_EXTRA,
                    self.FL_THK, fe, fn, fu, axis)
        self.C(f"  人孔 ×4 φ{self.MH_D} + 法兰")

    # ════════════════════════════════════════
    #  8. 再沸器 E-101  (卧式管壳换热器)
    # ════════════════════════════════════════
    def reboiler(self):
        self.H("8. 再沸器 E-101 Reboiler  (12 EQUI)")
        # 布局: 中心 E=3000, N=0, U=1200, 轴=EAST
        cx, cn, cu = 3000, 0, 1200
        e0 = cx - self.REB_L // 2   # 1000
        r  = self.REB_D // 2         # 600

        # 壳体
        self.CY("E101_SHELL", self.REB_D, self.REB_L, e0, cn, cu, 'E')
        # 管束
        self.CY("E101_TUBES", self.REB_TUBE_D, self.REB_TUBE_L,
                e0 + 200, cn, cu, 'E')
        # 折流板
        for i in range(self.REB_BAFFLE_N):
            ep = e0 + int(self.REB_L * (i + 1) / (self.REB_BAFFLE_N + 1))
            self.CY(f"E101_BAFFLE_{i+1}", self.REB_TUBE_D,
                    self.REB_BAFFLE_THK, ep, cn, cu, 'E')
        # 鞍座 (2个)
        sad_h = cu - r   # 从地面到壳底 = 600
        for i, frac in enumerate([0.25, 0.75]):
            ep = e0 + int(self.REB_L * frac)
            self.BX(f"E101_SADDLE_{i+1}", 200, self.REB_D + 200, sad_h,
                    ep, cn, sad_h // 2)
        # 管口+法兰 (壳进、壳出、管进)
        self.C("  壳侧进口(顶部左端)")
        self.nozzle("E101_N1_SHELL_IN", 300,
                    e0 + 800, cn, cu + r, 'U')
        self.C("  壳侧出口(顶部右端)")
        self.nozzle("E101_N2_SHELL_OUT", 300,
                    e0 + self.REB_L - 800, cn, cu + r, 'U')
        self.C("  管侧进口(北侧)")
        self.nozzle("E101_N3_TUBE_IN", 200,
                    e0 + 500, cn + r, cu, 'N')
        self.C(f"  再沸器: φ{self.REB_D}×{self.REB_L}")

    # ════════════════════════════════════════
    #  9. 冷凝器 E-102  (卧式管壳换热器)
    # ════════════════════════════════════════
    def condenser(self):
        self.H("9. 冷凝器 E-102 Condenser  (12 EQUI)")
        cx, cn, cu = 3000, 3000, 1200
        e0 = cx - self.COND_L // 2   # 1250
        r  = self.COND_D // 2         # 500

        # 壳体
        self.CY("E102_SHELL", self.COND_D, self.COND_L, e0, cn, cu, 'E')
        # 管束 (简化)
        self.CY("E102_TUBES", self.COND_D - 100, self.COND_L - 400,
                e0 + 200, cn, cu, 'E')
        # 折流板
        for i in range(self.REB_BAFFLE_N):
            ep = e0 + int(self.COND_L * (i + 1) / (self.REB_BAFFLE_N + 1))
            self.CY(f"E102_BAFFLE_{i+1}", self.COND_D - 100,
                    self.REB_BAFFLE_THK, ep, cn, cu, 'E')
        # 鞍座
        sad_h = cu - r
        for i, frac in enumerate([0.25, 0.75]):
            ep = e0 + int(self.COND_L * frac)
            self.BX(f"E102_SADDLE_{i+1}", 200, self.COND_D + 200, sad_h,
                    ep, cn, sad_h // 2)
        # 管口
        self.C("  壳侧进口(蒸气入)")
        self.nozzle("E102_N1_VAP_IN", 400,
                    e0 + 600, cn, cu + r, 'U')
        self.C("  壳侧出口(冷凝液)")
        self.nozzle("E102_N2_COND_OUT", 200,
                    e0 + self.COND_L - 600, cn, cu + r, 'U')
        self.C("  冷却水进口(北侧)")
        self.nozzle("E102_N3_CW_IN", 200,
                    e0 + 400, cn + r, cu, 'N')
        self.C(f"  冷凝器: φ{self.COND_D}×{self.COND_L}")

    # ════════════════════════════════════════
    #  10. 回流罐 V-101  (卧式储罐)
    # ════════════════════════════════════════
    def reflux_drum(self):
        self.H("10. 回流罐 V-101 Reflux Drum  (11 EQUI)")
        cx, cn, cu = 3000, 6000, 1200
        e0 = cx - self.DRUM_L // 2    # 1500
        r  = self.DRUM_D // 2          # 600

        # 筒体
        self.CY("V101_SHELL", self.DRUM_D, self.DRUM_L, e0, cn, cu, 'E')
        # 右端 DISH 封头 (轴=E, 向东延伸)
        self.DH("V101_HEAD_R", self.DRUM_D, self.DRUM_HEAD_H, self.DRUM_D,
                e0 + self.DRUM_L, cn, cu, 'E')
        # 左端 DISH 封头 (近似: 轴=E, 放在筒体左侧)
        self.DH("V101_HEAD_L", self.DRUM_D, self.DRUM_HEAD_H, self.DRUM_D,
                e0 - self.DRUM_HEAD_H, cn, cu, 'E')
        # 鞍座
        sad_h = cu - r
        for i, frac in enumerate([0.25, 0.75]):
            ep = e0 + int(self.DRUM_L * frac)
            self.BX(f"V101_SADDLE_{i+1}", 200, self.DRUM_D + 200, sad_h,
                    ep, cn, sad_h // 2)
        # 管口: 进料(顶左)、出液(顶右)、放空(顶右端)
        self.C("  进料口")
        self.nozzle("V101_N1_INLET", 200,
                    e0 + 600, cn, cu + r, 'U')
        self.C("  出液口")
        self.nozzle("V101_N2_OUTLET", 200,
                    e0 + self.DRUM_L - 600, cn, cu + r, 'U')
        self.C("  放空口")
        self.nozzle("V101_N3_VENT", 50,
                    e0 + self.DRUM_L - 200, cn, cu + r, 'U')
        self.C(f"  回流罐: φ{self.DRUM_D}×{self.DRUM_L} + 2 DISH封头")

    # ════════════════════════════════════════
    #  11. 钢平台 + 爬梯 + 护栏
    # ════════════════════════════════════════
    def platforms_ladders(self):
        self.H("11. 钢平台 & 爬梯 Platforms & Ladders  (~27 EQUI)")
        R = self.R   # 1220

        # 5层操作平台, 均在 -E 侧(西侧, 远离辅机)
        plat_levels = [7000, 11000, 15000, 19000, 23000]
        plat_cx = -(R + self.PLAT_W // 2)   # -1820 (平台中心E)
        plat_edge = -(R + self.PLAT_W)       # -2420 (外边缘E)

        for idx, u_plat in enumerate(plat_levels):
            tag = f"STR_PLAT_{idx+1}"
            # 格板甲板
            self.BX(f"{tag}_DECK", self.PLAT_W, 2000, self.PLAT_THK,
                    plat_cx, 0, u_plat)
            # 2 个悬臂支撑(三角托架简化为BOX)
            for j, n_off in enumerate([-600, 600]):
                self.BX(f"{tag}_BKT_{j+1}", 500, 200, 400,
                        -(R + 250), n_off, u_plat - 225)
            # 外侧护栏(横杆)
            self.BX(f"{tag}_RAIL", 60, 2200, 60,
                    plat_edge, 0, u_plat + self.HR_H)
            # 中部护栏
            self.BX(f"{tag}_MIDRAIL", 60, 2200, 60,
                    plat_edge, 0, u_plat + self.HR_H // 2)
        self.C(f"  操作平台 ×{len(plat_levels)} + 护栏 (甲板+2托架+2横杆)")

        # 主爬梯 (从地面到第1层平台, -E侧)
        ladder_e = plat_edge - 100   # -2520
        ladder_h = plat_levels[0]    # 7000
        self.BX("STR_LADDER_RAIL_N", 80, 40, ladder_h,
                ladder_e, 250, ladder_h // 2)
        self.BX("STR_LADDER_RAIL_S", 80, 40, ladder_h,
                ladder_e, -250, ladder_h // 2)
        self.C(f"  主爬梯 2侧梁 H={ladder_h}")

    # ════════════════════════════════════════
    #  12. 附属管口  (安全阀 / 液位计)
    # ════════════════════════════════════════
    def accessories(self):
        self.H("12. 附属管口 Accessories  (6 EQUI)")
        R = self.R
        # 安全阀口 (塔顶附近, +N侧)
        self.C("  安全阀口 DN80")
        self.nozzle("T101_N_SV", 80, 0, R, self.U_SHELL_TOP - 1000, 'N')
        # 液位计上接口 (塔底区, +E侧)
        self.C("  液位计上接口 DN50")
        self.nozzle("T101_N_LG_HI", 50, R, 0, self.U_SHELL + 2000, 'E')
        # 液位计下接口
        self.C("  液位计下接口 DN50")
        self.nozzle("T101_N_LG_LO", 50, R, 0, self.U_SHELL + 500, 'E')

    # ════════════════════════════════════════
    #  入口: 构建 + 保存
    # ════════════════════════════════════════
    def build(self):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.L = [
            f"-- 化工精馏塔装置 — 苯-甲苯精馏系统",
            f"-- DN{self.SHELL_ID} | {self.TRAY_N}层浮阀塔盘 | 总高{self.U_TOP/1000:.1f}m",
            f"-- 生成: {ts}",
            f"-- 数据基线: 工业标准苯-甲苯常压精馏塔",
            f"-- 前置: E3D 中先选可写 ZONE → $$MACRO <本文件>",
            f"-- 单位: mm | E=东 N=北 U=上 | 塔中心 E=0 N=0",
            "",
            f"-- 标高概览:",
            f"--   地面       U = 0",
            f"--   裙座底     U = {self.U_SKIRT}",
            f"--   裙座顶     U = {self.U_SKIRT_TOP}",
            f"--   下封头     U = {self.U_BHEAD} ~ {self.U_SHELL}",
            f"--   筒体       U = {self.U_SHELL} ~ {self.U_SHELL_TOP}",
            f"--   进料层     U = {self.U_FEED}  (第{self.FEED_TRAY}层塔盘)",
            f"--   上封头     U = {self.U_THEAD} ~ {self.U_TOP}",
            f"--   辅机(E-101/E-102/V-101)  E=3000 侧",
            "",
        ]

        self.skirt()
        self.bottom_head()
        self.shell()
        self.top_head()
        self.trays()
        self.column_nozzles()
        self.manholes()
        self.reboiler()
        self.condenser()
        self.reflux_drum()
        self.platforms_ladders()
        self.accessories()

        self.L.extend([
            "",
            f"-- {'='*60}",
            f"--  精馏塔装置完成: {self.n} EQUIPMENT",
            f"--  基本体: CYLI + BOX + CONE + DISH (全部 E3D 3.1 验证 ✓)",
            f"-- {'='*60}",
            "",
        ])
        return "\n".join(self.L)

    def save(self):
        pml = self.build()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fp = OUTPUT_DIR / f"distillation_column_{ts}.pml"
        fp.write_text(pml, encoding="utf-8", newline="\n")
        return fp, pml


if __name__ == "__main__":
    dc = DistillationColumn()
    fp, pml = dc.save()

    # ── 自检 ──
    errors = []
    lines = pml.split("\n")

    # 1. PML2 禁止语法
    for b in BANNED:
        for i, l in enumerate(lines, 1):
            if b in l:
                errors.append(f"PML2-ism '{b}' @ L{i}: {l.strip()}")

    # 2. PML2 变量赋值模式
    import re
    for i, l in enumerate(lines, 1):
        if re.match(r"\s*![a-zA-Z]", l) and "=" in l:
            errors.append(f"PML2 var @ L{i}: {l.strip()}")

    # 3. EQUI 名称唯一性
    equi_names = [l.split("/")[1].strip() for l in lines
                  if l.strip().startswith("NEW EQUI /")]
    dupes = [n for n in equi_names if equi_names.count(n) > 1]
    if dupes:
        errors.append(f"重名 EQUI: {set(dupes)}")

    # 4. CYLI 完整性 (每个 NEW CYLI 后必须有 DIAM + HEIG)
    in_cyli = False
    has_diam = has_heig = False
    for i, l in enumerate(lines, 1):
        ls = l.strip()
        if ls == "NEW CYLI":
            if in_cyli and (not has_diam or not has_heig):
                errors.append(f"CYLI 缺属性 @ ~L{i}")
            in_cyli = True; has_diam = has_heig = False
        elif ls.startswith("DIAM "): has_diam = True
        elif ls.startswith("HEIG "): has_heig = True
        elif ls.startswith("NEW ") and ls != "NEW CYLI":
            if in_cyli and (not has_diam or not has_heig):
                errors.append(f"CYLI 缺属性 @ ~L{i}")
            in_cyli = False

    # 5. 无 SITE/ZONE 创建
    for kw in ["NEW SITE", "NEW ZONE"]:
        if kw in pml:
            errors.append(f"禁止: {kw}")

    if errors:
        print(f"[ERROR] 发现 {len(errors)} 个问题:")
        for e in errors:
            print(f"  - {e}")
    else:
        print(f"[OK] PML1 语法校验通过")
        print(f"  文件: {fp.name}")
        print(f"  行数: {len(lines)}")
        print(f"  EQUI: {dc.n}")
        print(f"  名称: {len(dc.names)} 唯一")
        print(f"  基本体: CYLI + BOX + CONE + DISH")
        print(f"  标高: 地面0 -> 塔顶{dc.U_TOP}mm ({dc.U_TOP/1000:.1f}m)")
