#!/usr/bin/env python3
"""
PM1 纸机高精度模型 v2 — 精细化版
===============================
4800mm 长网多缸造纸机，含网部/压榨/干燥/施胶/压光/卷纸
增强: 成型板/水印辊/毛布辊/刮刀/引纸绳/蒸汽接头/走台护栏
"""

from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(r"D:\AVEVA\Projects\E3D3.1\e3d_agent\output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class PM1:
    # ── 基础参数 ──
    TRIM   = 4800;  WIRE_W = 5200;  FRAME_W = 5800
    NW = FRAME_W//2 + 400   # 柱北坐标
    SW = -(FRAME_W//2 + 400) # 柱南坐标

    # ── 标高 ──
    FLOOR  = 0;      WALKWAY = 1800
    WIRE_EL= 3500;   PRESS_BASE = 2700
    DRY_BOT= 2800;   DRY_TOP = 5000
    SP_EL  = 3500;   CAL_BOT = 500
    REEL_EL= 1500

    # ── 网部 ──
    BREAST_D = 700;  BREAST_E = 0
    FORMING_E= 1000; TABLE_D=320; TABLE_N=18; TABLE_SP=600
    DANDY_D = 800;   DANDY_E = 8500
    SUCT_N  = 7;     SUCT_W=280; SUCT_START=11800
    COUCH_D = 900;   COUCH_E = 16800
    WIRE_RETURN_D=500

    # ── 压榨 ──
    P1_E=19200; P1_D=900;  P2_E=21800; P2_D=950; P3_E=24600; P3_D=1050
    FELT_D = 500  # 毛布导辊直径

    # ── 干燥 ──
    D_START=26000; D_DIAM=1500; D_FACE=5200; D_N=28; D_PITCH=2400
    D_RET_D=700  # 干网返回辊

    # ── 施胶/压光/卷纸 ──
    SP_E=62000; SP_D=900
    CAL_E=64500; CAL_D=700; CAL_N=6; CAL_P=900
    REEL_E=66000; REEL_D=1000; SPOOL_D=450

    def __init__(self):
        self.L = []; self.n = 0

    def H(self, title):
        self.L.extend(["",f"-- {'='*60}",f"--  {title}",f"-- {'='*60}",""])

    def C(self, text): self.L.append(f"-- {text}")

    # ── 基元 ──
    def CY(self, name, d, h, e=0, n=0, u=0, ax='N'):
        self.n+=1; s=name.replace(" ","_").replace("/","_").replace("-","_")
        self.L.append(f"NEW EQUI /{s}")
        self.L.append(f"NEW CYLI")
        self.L.append(f"DIAM {d}")
        self.L.append(f"HEIG {h}")
        self.L.append(f"POS E {e} N {n} U {u}")
        self.L.append(f"ORI Y IS {ax} AND Z IS U")
        self.L.append("")
        return s

    def BX(self, name, x,y,z, e=0,n=0,u=0):
        self.n+=1; s=name.replace(" ","_").replace("/","_").replace("-","_")
        self.L.append(f"NEW EQUI /{s}")
        self.L.append(f"NEW BOX")
        self.L.append(f"XLEN {x}")
        self.L.append(f"YLEN {y}")
        self.L.append(f"ZLEN {z}")
        self.L.append(f"POS E {e} N {n} U {u}")
        self.L.append("")
        return s

    # 横向辊(跨幅宽) / 纵向分段辊
    def roll(self, name, d, e, n=0, u=3500, face=None):
        return self.CY(name, d, face or self.WIRE_W+400, e, n, u, 'N')

    def roll_box(self, name, d, e, n=0, u=3500, face=None):
        # 辊的BOX近似(方轴颈)
        w=face or self.WIRE_W+400
        return self.BX(name, d+100, w, d, e, n, u)

    # 双辊对(pair)
    def roll_pair(self, prefix, e, d, base_u, face=None):
        f=face or self.TRIM+600
        self.roll(f"{prefix}_TOP", d, e, 0, base_u+d, f)
        self.roll(f"{prefix}_BOT", d, e, 0, base_u, f)

    # ── 机架组件 ──
    def col(self, name, h, e, n, u_base, w=600):
        return self.BX(name, w, w, h, e, n, u_base+h//2)

    def beam(self, name, length, h, e, n, u, w=350):
        return self.BX(name, length, w, h, e, n, u)

    def soleplate(self, name, e, n):
        return self.BX(name, 1000, 800, 300, e, n, 150)

    # ════════════════════════════════════════
    #  1. 流浆箱
    # ════════════════════════════════════════
    def headbox(self):
        self.H("1. 流浆箱 Headbox")
        hb_e=-1500; hb_u=self.WIRE_EL+600
        # 主体
        self.BX("PM1_HDBX_MAIN", 1400, self.WIRE_W+300, 1100, hb_e, 0, hb_u)
        # 上唇板+下唇板
        self.BX("PM1_HDBX_TOP_LIP", 250, self.WIRE_W, 60, hb_e+800, 0, hb_u+520)
        self.BX("PM1_HDBX_BOT_LIP", 250, self.WIRE_W, 60, hb_e+800, 0, hb_u-620)
        # 锥形进浆总管(2段近似)
        self.roll("PM1_HDBX_HEADER", 550, hb_e, 0, hb_u+700, self.WIRE_W+500)
        # 稀释水总管
        self.roll("PM1_HDBX_DILUTION", 150, hb_e, 0, hb_u+1200, self.WIRE_W+200)
        # 流浆箱支架
        self.col("PM1_HDBX_STAND_N", 2000, hb_e, self.NW-300, 1200)
        self.col("PM1_HDBX_STAND_S", 2000, hb_e, self.SW+300, 1200)
        self.C(f"  流浆箱: 6 EQUI (主体+唇板+进浆管+稀释水管+支架×2)")

    # ════════════════════════════════════════
    #  2. 网部
    # ════════════════════════════════════════
    def wire_section(self):
        self.H("2. 网部 Fourdrinier Wire")
        wu=self.WIRE_EL; fw=self.WIRE_W+300

        # 2.1 胸辊
        self.roll("PM1_BREAST_ROLL", self.BREAST_D, self.BREAST_E, 0, wu, fw)

        # 2.2 成型板(多块窄条)
        for i in range(5):
            self.BX(f"PM1_FORMING_BRD_{i+1}", 200, self.WIRE_W-200, 100,
                    self.FORMING_E+i*250, 0, wu-60)

        # 2.3 案辊组(带轴承座)
        for i in range(self.TABLE_N):
            ep=self.FORMING_E+1500+i*self.TABLE_SP
            self.roll(f"PM1_TABLE_ROLL_{i+1:02d}", self.TABLE_D, ep, 0, wu-self.TABLE_D//2, self.WIRE_W+150)
        self.C(f"  案辊 ×{self.TABLE_N} φ{self.TABLE_D} 间距{self.TABLE_SP}")

        # 2.4 脱水板/刮水板(foil blades) — 窄长条
        foil_start=self.FORMING_E+1500+self.TABLE_N*self.TABLE_SP+500
        for i in range(12):
            self.BX(f"PM1_FOIL_{i+1:02d}", 80, self.WIRE_W-300, 60,
                    foil_start+i*250, 0, wu-40)

        # 2.5 水印辊 (dandy roll)
        self.roll("PM1_DANDY_ROLL", self.DANDY_D, self.DANDY_E, 0, wu+self.DANDY_D//2, self.WIRE_W+200)
        # 水印辊支架
        self.col("PM1_DANDY_STAND_N", 2000, self.DANDY_E, self.NW-200, self.WIRE_EL-500)
        self.col("PM1_DANDY_STAND_S", 2000, self.DANDY_E, self.SW+200, self.WIRE_EL-500)

        # 2.6 真空吸水箱(逐步增加真空度)
        for i in range(self.SUCT_N):
            ep=self.SUCT_START+i*(self.SUCT_W+250)
            self.BX(f"PM1_SUCT_BOX_{i+1}", self.SUCT_W, self.WIRE_W-400, 400,
                    ep, 0, wu-200)
        self.C(f"  真空吸水箱 ×{self.SUCT_N}")

        # 2.7 伏辊
        couch_e=self.SUCT_START+self.SUCT_N*(self.SUCT_W+250)+800
        self.roll("PM1_COUCH_ROLL", self.COUCH_D, couch_e, 0, wu, fw)
        self.C(f"  伏辊 φ{self.COUCH_D}")

        # 2.8 网部回网辊(under-table wire return rolls)
        for i in range(5):
            self.roll(f"PM1_WIRE_RET_{i+1}", self.WIRE_RETURN_D,
                      self.BREAST_E+2000+i*3200, 0, wu-2200, self.WIRE_W+200)

        # 2.9 网案纵梁+横撑+立柱
        wl=self.SUCT_START+self.SUCT_N*(self.SUCT_W+250)
        for side, ns in [("N",self.NW),("S",self.SW)]:
            # 下纵梁(通长)
            self.beam(f"PM1_WIRE_RAIL_LOW_{side}", wl+2000, 450,
                      wl//2-1000, ns-100, 1200, 350)
            # 上纵梁
            self.beam(f"PM1_WIRE_RAIL_HI_{side}", wl+2000, 350,
                      wl//2-1000, ns-100, wu+300, 280)
            # 底座垫板(每3m)
            for i in range(0, wl, 3000):
                self.soleplate(f"PM1_WIRE_SP_{side}_{i//3000+1:02d}", i, ns)
            # 立柱(每3m)
            for i in range(0, wl, 3000):
                self.col(f"PM1_WIRE_COL_{side}_{i//3000+1:02d}",
                         wu+800, i, ns, 300, 450)
        self.C(f"  网案机架: 纵梁×4 + 立柱 + 垫板")

    # ════════════════════════════════════════
    #  3. 压榨部
    # ════════════════════════════════════════
    def press_section(self):
        self.H("3. 压榨部 Press Section")
        bu=self.PRESS_BASE

        # 3.1 三压区压辊
        self.roll_pair("PM1_PRESS1", self.P1_E, self.P1_D, bu)
        self.roll_pair("PM1_PRESS2", self.P2_E, self.P2_D, bu)
        self.roll_pair("PM1_PRESS3", self.P3_E, self.P3_D, bu)
        self.C("  三压区: P1 φ900 + P2 φ950 + P3 φ1050")

        # 3.2 毛布导辊(每压区4-6根)
        for pi, pe in [("P1",self.P1_E),("P2",self.P2_E),("P3",self.P3_E)]:
            for j in range(4):
                self.roll(f"PM1_FELT_{pi}_{j+1}", self.FELT_D,
                          pe-1200+j*800, 0, bu-500, self.TRIM+400)

        # 3.3 真空吸水箱(Uhle boxes, 每压区2个)
        for pi, pe in [("P1",self.P1_E),("P2",self.P2_E),("P3",self.P3_E)]:
            self.BX(f"PM1_UHLE_{pi}_1", 200, self.TRIM-400, 300, pe-500, 0, bu-800)
            self.BX(f"PM1_UHLE_{pi}_2", 200, self.TRIM-400, 300, pe+500, 0, bu-800)

        # 3.4 压榨机架
        for pe in [self.P1_E, self.P2_E, self.P3_E]:
            for ns in [self.NW, self.SW]:
                self.col(f"PM1_PRESS_COL_{pe}_{ns}", 3500, pe, ns, bu-500, 700)
                self.soleplate(f"PM1_PRESS_SP_{pe}_{ns}", pe, ns)
        self.C("  压榨机架: 立柱×6 + 垫板×6")

    # ════════════════════════════════════════
    #  4. 干燥部
    # ════════════════════════════════════════
    def dryer_section(self):
        self.H("4. 干燥部 Dryer Section")
        half=self.D_N//2; df=self.D_FACE

        # 4.1 烘缸(上排+下排)
        for i in range(half):
            ep=self.D_START+i*self.D_PITCH
            self.roll(f"PM1_DRYER_HI_{i+1:02d}", self.D_DIAM, ep, 0, self.DRY_TOP, df)
            self.roll(f"PM1_DRYER_LO_{i+1:02d}", self.D_DIAM, ep, 0, self.DRY_BOT, df)
        self.C(f"  烘缸: {self.D_N}个 φ{self.D_DIAM}×{df}L @{self.D_PITCH}")

        # 4.2 刮刀(doctor blade) — 窄长薄板,每缸1个
        for i in range(half):
            ep=self.D_START+i*self.D_PITCH
            self.BX(f"PM1_DOCTOR_HI_{i+1:02d}", 80, df-200, 100, ep+self.D_DIAM//2+50, 0, self.DRY_TOP+self.D_DIAM//2-50)
            self.BX(f"PM1_DOCTOR_LO_{i+1:02d}", 80, df-200, 100, ep+self.D_DIAM//2+50, 0, self.DRY_BOT+self.D_DIAM//2-50)
        self.C(f"  刮刀: {self.D_N}个")

        # 4.3 干网返回辊(dryer fabric return rolls)
        for i in range(0, half, 2):
            ep=self.D_START+i*self.D_PITCH
            self.roll(f"PM1_FABRET_HI_{i//2+1}", self.D_RET_D, ep, 0, self.DRY_TOP+self.D_DIAM+300, df-400)
            self.roll(f"PM1_FABRET_LO_{i//2+1}", self.D_RET_D, ep, 0, self.DRY_BOT-self.D_DIAM-300, df-400)

        # 4.4 蒸汽接头(steam joint) — 每缸末端小圆柱
        for i in range(half):
            ep=self.D_START+i*self.D_PITCH
            for ns, nv in [("N",df//2+150),("S",-df//2-150)]:
                self.CY(f"PM1_STEAM_HI_{i+1:02d}_{ns}", 200, 600, ep, nv, self.DRY_TOP+self.D_DIAM//2, 'E')
                self.CY(f"PM1_STEAM_LO_{i+1:02d}_{ns}", 200, 600, ep, nv, self.DRY_BOT+self.D_DIAM//2, 'E')

        # 4.5 引纸绳轮(rope sheave) — 传动侧每缸间
        for i in range(half):
            ep=self.D_START+i*self.D_PITCH
            self.roll(f"PM1_ROPE_HI_{i+1:02d}", 300, ep, self.NW-100, self.DRY_TOP, 100)
            self.roll(f"PM1_ROPE_LO_{i+1:02d}", 300, ep, self.NW-100, self.DRY_BOT, 100)

        # 4.6 干燥部机架
        dryer_end=self.D_START+(half-1)*self.D_PITCH
        frame_h=self.DRY_TOP+self.D_DIAM//2+600
        for i in range(0, half, 2):
            ep=self.D_START+i*self.D_PITCH
            for ns in [self.NW+100, self.SW-100]:
                self.col(f"PM1_DRY_FRM_{i//2+1:02d}_{ns}", frame_h, ep, ns, frame_h//2, 550)
                self.soleplate(f"PM1_DRY_SP_{i//2+1:02d}_{ns}", ep, ns)
        self.C(f"  干燥部机架: 立柱×{half} + 垫板")

        # 4.7 烘缸罩
        self.BX("PM1_HOOD", dryer_end-self.D_START+3000, self.FRAME_W+1000, 2200,
                (self.D_START+dryer_end)//2, 0, self.DRY_TOP+self.D_DIAM//2+1100)
        self.C(f"  烘缸罩 {dryer_end-self.D_START+3000}L×{self.FRAME_W+1000}W×2200H")

    # ════════════════════════════════════════
    #  5. 施胶机
    # ════════════════════════════════════════
    def size_press(self):
        self.H("5. 施胶机 Size Press")
        self.roll_pair("PM1_SP", self.SP_E, self.SP_D, self.SP_EL, self.TRIM+400)
        # 上料管
        self.roll("PM1_SP_SUPPLY", 100, self.SP_E, self.NW-400, self.SP_EL+self.SP_D+200, self.TRIM)
        # 机架
        for ns in [self.NW, self.SW]:
            self.col(f"PM1_SP_FRM_{ns}", 4500, self.SP_E, ns, self.SP_EL-500, 700)
            self.soleplate(f"PM1_SP_SP_{ns}", self.SP_E, ns)
        self.C(f"  施胶机: 2辊 φ{self.SP_D} + 上料管 + 机架")

    # ════════════════════════════════════════
    #  6. 压光机
    # ════════════════════════════════════════
    def calender(self):
        self.H("6. 压光机 Calender")
        for i in range(self.CAL_N):
            ru=self.CAL_BOT+i*self.CAL_P+self.CAL_D//2
            self.roll(f"PM1_CAL_R{i+1}", self.CAL_D, self.CAL_E, 0, ru, self.TRIM+300)
        # 框架
        ft=self.CAL_BOT+(self.CAL_N-1)*self.CAL_P+self.CAL_D+600
        for ns in [self.NW-100, self.SW+100]:
            self.col(f"PM1_CAL_FRM_{ns}", ft, self.CAL_E, ns, ft//2, 750)
            self.soleplate(f"PM1_CAL_SP_{ns}", self.CAL_E, ns)
        self.C(f"  压光机: {self.CAL_N}辊 φ{self.CAL_D} 垂直堆叠 + 机架")

    # ════════════════════════════════════════
    #  7. 卷纸机
    # ════════════════════════════════════════
    def reel(self):
        self.H("7. 卷纸机 Reel")
        # 卷纸缸
        self.roll("PM1_REEL_DRUM", self.REEL_D, self.REEL_E, 0, self.REEL_EL+self.REEL_D//2, self.TRIM+300)
        # 卷纸轴(2个位置: 初卷+满卷)
        self.roll("PM1_REEL_SPOOL1", self.SPOOL_D, self.REEL_E+700, 0, self.REEL_EL+self.REEL_D+200, self.TRIM+400)
        self.roll("PM1_REEL_SPOOL2", self.SPOOL_D, self.REEL_E+1200, 0, self.REEL_EL+self.REEL_D+600, self.TRIM+400)
        # 压纸辊(rider roll)
        self.roll("PM1_REEL_RIDER", 400, self.REEL_E+900, 0, self.REEL_EL+self.REEL_D+1100, self.TRIM+200)
        # 机架
        for ns in [self.NW, self.SW]:
            self.col(f"PM1_REEL_FRM_{ns}", 5500, self.REEL_E+600, ns, 3000, 700)
            self.soleplate(f"PM1_REEL_SP_{ns}", self.REEL_E+600, ns)
        self.C("  卷纸机: 卷纸缸+2卷纸轴+压纸辊+机架")

    # ════════════════════════════════════════
    #  8. 走台+护栏
    # ════════════════════════════════════════
    def walkways(self):
        self.H("8. 走台与护栏 Walkways & Handrails")
        ml=self.REEL_E+2000  # 机长
        ww=1200

        for side, ns, hn in [("N", self.NW+ww//2+300, self.NW+ww+300),
                             ("S", self.SW-ww//2-300, self.SW-ww-300)]:
            # 走台板
            self.BX(f"PM1_WALKWAY_{side}", ml, ww, 100, ml//2-1000, ns, self.WALKWAY)
            # 护栏立柱(每4m)
            for i in range(0, ml, 4000):
                self.col(f"PM1_RAIL_COL_{side}_{i//4000+1:02d}", 1100, i, hn, self.WALKWAY+550, 80)
            # 护栏横杆(上+中)
            self.beam(f"PM1_RAIL_TOP_{side}", ml, 60, ml//2-1000, hn, self.WALKWAY+1100, 60)
            self.beam(f"PM1_RAIL_MID_{side}", ml, 60, ml//2-1000, hn, self.WALKWAY+700, 60)
        self.C(f"  走台2条 + 护栏4条(上/中横杆各2) + 立柱")

    # ════════════════════════════════════════
    #  9. 基础
    # ════════════════════════════════════════
    def foundation(self):
        self.H("9. 基础 Foundation")
        ml=self.REEL_E+3000
        self.BX("PM1_FOUNDATION", ml, self.FRAME_W+4000, 600, ml//2-500, 0, -300)
        self.C(f"  基础平台 {ml}L×{self.FRAME_W+4000}W×600H")

        # 传动侧电机平台
        ds=self.D_START+(self.D_N//4)*self.D_PITCH
        self.BX("PM1_MOTOR_DECK", 6000, 3000, 300, ds, self.NW+2000, self.WALKWAY)
        # 电机(简化为圆柱+方箱)
        self.CY("PM1_MOTOR_1", 800, 2000, ds-2000, self.NW+2500, self.WALKWAY+300, 'E')
        self.BX("PM1_MOTOR_1_BOX", 1500, 1200, 1000, ds, self.NW+2500, self.WALKWAY+500)
        self.C("  传动侧电机平台+电机")

        # 真空泵平台(湿部)
        self.BX("PM1_VAC_DECK", 5000, 3000, 300, 8000, self.NW+2000, self.WALKWAY)
        self.BX("PM1_VAC_PUMP", 3000, 1500, 1800, 8000, self.NW+2500, self.WALKWAY+900)

    # ════════════════════════════════════════
    #  入口
    # ════════════════════════════════════════
    def build(self):
        ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.L=[
            f"-- PM1 纸机高精度模型 v2 — 4800mm Fourdrinier",
            f"-- 生成: {ts} | 数据基线: 工业长网多缸造纸机",
            "-- 前置: E3D中先选可写ZONE → $$MACRO <本文件>",
            "-- 单位: mm | EAST=纸机方向 N=横向 U=垂直",
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
            "",f"-- ══ PM1 完成: {self.n} EQUIPMENT ══",""
        ])
        return "\n".join(self.L)

    def save(self):
        pml=self.build()
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        fp=OUTPUT_DIR/f"paper_machine_pm1_{ts}.pml"
        fp.write_text(pml, encoding="utf-8", newline="\n")
        return fp,pml


if __name__=="__main__":
    b=PM1()
    fp,pml=b.save()
    lc=len(pml.split("\n"))
    print(f"OK: {fp}")
    print(f"   {lc} lines | {b.n} EQUIPMENT")
    print("\n".join(pml.split("\n")[:15]))
