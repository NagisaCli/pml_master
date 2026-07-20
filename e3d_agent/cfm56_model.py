#!/usr/bin/env python3
"""
CFM56-7B 涡扇发动机 — 修正版
=============================
严格轴向堆叠，无重叠，同心环结构
EAST=发动机轴线(0=进气口, 2286=尾喷口), N/U=径向平面
"""

from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(r"D:\AVEVA\Projects\E3D3.1\e3d_agent\output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class CFM56:
    LEN=2286          # 总长mm
    FAN_D=1549;  NACELLE_D=1585;  SPINNER_D=420
    CORE_D=580;  LPT_D=620;       EXIT_D=520
    HPC_STG=9;   LPT_STG=4

    def __init__(self):
        self.L=[]; self.n=0

    def H(self,t):
        self.L.extend(["",f"-- {'='*50}",f"--  {t}",f"-- {'='*50}",""])
    def C(self,t):
        self.L.append(f"-- {t}")

    # 创建: CYLI轴向=E时, DIAM在N-U面, HEIG沿E, POS=(底面中心E,N,U)
    def R(self,name,d,length, e_start, n=0, u=0):
        """短圆筒段(ring), 轴=E"""
        self.n+=1; s=name.replace(" ","_")
        self.L.append(f"NEW EQUI /{s}")
        self.L.append(f"NEW CYLI")
        self.L.append(f"DIAM {d}")
        self.L.append(f"HEIG {length}")
        self.L.append(f"POS E {e_start} N {n} U {u}")
        self.L.append(f"ORI Y IS E AND Z IS U")
        self.L.append("")
        return s

    def B(self,name,x,y,z, e=0,n=0,u=0):
        self.n+=1; s=name.replace(" ","_")
        self.L.append(f"NEW EQUI /{s}")
        self.L.append(f"NEW BOX")
        self.L.append(f"XLEN {x}")
        self.L.append(f"YLEN {y}")
        self.L.append(f"ZLEN {z}")
        self.L.append(f"POS E {e} N {n} U {u}")
        self.L.append("")
        return s

    def build(self):
        ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.L=[
            f"-- CFM56-7B 涡扇发动机 | 61in风扇/1585mm短舱/2286mm总长",
            f"-- 生成: {ts} | E=轴(进→排) N/U=径向 | 前置: 选ZONE后$$MACRO",
            "",
        ]

        m=self  # shorthand

        # ═══════════════════════════════════════
        # 1. 进气锥+风扇盘(同心)
        # ═══════════════════════════════════════
        self.H("1. 进气锥 & 风扇 Spinner & Fan")
        self.R("PM1_CONE_TIP",   60,  80,  20)         #锥尖 E20-100
        self.R("PM1_CONE_MID",  200, 100, 100)         #锥中 E100-200
        self.R("PM1_CONE_BASE", 380,  80, 200)         #锥底 E200-280
        self.R("PM1_FAN_DISC",  m.FAN_D-20, 30, 340)   #风扇盘 E340-370
        # 风扇机匣
        self.R("PM1_FAN_CASE",  m.NACELLE_D, 200, 300) #E300-500
        self.C("  进气锥3段 φ60→200→380 + 风扇盘φ1530 + 机匣")

        # ═══════════════════════════════════════
        # 2. 分流环 → 外涵道外壁(短舱) + 核心整流罩
        # ═══════════════════════════════════════
        self.H("2. 外涵道 & 短舱 Bypass & Nacelle")
        # 短舱前段(进气道)
        self.R("PM1_NACELLE_FWD",  m.NACELLE_D, 300, 0)     #E0-300
        # 短舱中段(风扇段)
        self.R("PM1_NACELLE_MID",  m.NACELLE_D, 200, 300)   #E300-500 (同上)
        # 短舱后段(外涵)
        self.R("PM1_NACELLE_AFT",  m.NACELLE_D, 1500, 500)  #E500-2000
        # 尾喷口外涵
        self.R("PM1_NACELLE_EXIT", m.NACELLE_D-40, 200, 2000)#E2000-2200
        # 分流环
        self.R("PM1_SPLITTER",  m.FAN_D-80, 120, 500)       #E500-620
        # 核心整流罩(内涵外壁)
        self.R("PM1_CORE_COWL",  m.CORE_D+30, 1350, 620)    #E620-1970
        self.C("  短舱5段 φ1585 + 分流环 + 核心整流罩φ610")

        # ═══════════════════════════════════════
        # 3. 高压压气机(9级, 逐级略缩)
        # ═══════════════════════════════════════
        self.H("3. 高压压气机 HPC 9-stage")
        hp_start=650; hp_pitch=55
        self.R("PM1_HPC_CASE", m.CORE_D-20, m.HPC_STG*hp_pitch+30,
               hp_start)  # 机匣
        for i in range(m.HPC_STG):
            ep=hp_start+20+i*hp_pitch
            od=m.CORE_D-50-i*8   #逐级缩径
            id_=160+i*12
            self.R(f"PM1_HPC_D{i+1:02d}", od, 15, ep)
            self.R(f"PM1_HPC_R{i+1:02d}", id_,  15, ep)
        self.C("  HPC 9级盘+轮毂 + 机匣φ560")

        # ═══════════════════════════════════════
        # 4. 燃烧室
        # ═══════════════════════════════════════
        self.H("4. 燃烧室 Combustor")
        cb_e=hp_start+m.HPC_STG*hp_pitch+50  # ≈ 1200
        self.R("PM1_DIFFUSER",  m.CORE_D+30, 80, cb_e)
        self.R("PM1_COMB_OUTER",m.CORE_D+40, 200, cb_e+80)
        self.R("PM1_COMB_INNER",m.CORE_D-90, 180, cb_e+90)
        self.C("  扩压器+火焰筒外壁+内壁 φ620/490")

        # ═══════════════════════════════════════
        # 5. 高压涡轮 + 低压涡轮
        # ═══════════════════════════════════════
        self.H("5. 涡轮 HPT+LPT")
        tb_e=cb_e+300  # ≈1500
        #HPT
        self.R("PM1_HPT_CASE",  m.CORE_D, 80, tb_e)
        self.R("PM1_HPT_DISC",  m.CORE_D-30, 20, tb_e+30)
        self.R("PM1_HPT_NGV",   m.CORE_D-20, 25, tb_e)
        #LPT机匣(逐级扩大)
        self.R("PM1_LPT_CASE",  m.LPT_D, m.LPT_STG*60+30, tb_e+80)
        for i in range(m.LPT_STG):
            ep=tb_e+100+i*60
            od=m.LPT_D-20-i*12
            self.R(f"PM1_LPT_D{i+1:02d}", od, 15, ep)
        self.C(f"  HPT1级+NGV + LPT{m.LPT_STG}级")

        # ═══════════════════════════════════════
        # 6. 排气
        # ═══════════════════════════════════════
        self.H("6. 排气 Exhaust")
        ex_e=tb_e+m.LPT_STG*60+100  #≈1840
        self.R("PM1_CORE_NOZZLE", m.EXIT_D, 160, ex_e)
        self.R("PM1_TAIL_CONE",   120, 200, ex_e)
        self.C("  核心喷管φ520 + 尾锥")

        # ═══════════════════════════════════════
        # 7. 双转子轴
        # ═══════════════════════════════════════
        self.H("7. 转轴 Shafts")
        self.R("PM1_LP_SHAFT", 70,  self.LEN-300, 340)  #风扇→LPT
        self.R("PM1_HP_SHAFT", 110, 900, hp_start)       #HPC→HPT
        self.C("  LP轴φ70全长 + HP轴φ110(HPC-HPT段)")

        # ═══════════════════════════════════════
        # 8. 附件+吊架
        # ═══════════════════════════════════════
        self.H("8. 附件 Accessories")
        n_bot=-(m.NACELLE_D//2+250)  #底部
        self.B("PM1_AGB",    500, 350, 280,  500, 0, n_bot)     #齿轮箱
        self.B("PM1_GEN",    200, 200, 400,  700, 180, n_bot-200) #发电机
        self.B("PM1_FUEL_P", 180, 180, 200,  500, -200, n_bot-200)#燃油泵
        self.B("PM1_OIL_TK", 300, 150, 200,  400, 220, n_bot-200) #滑油箱
        # 吊架
        self.B("PM1_PYLON_FWD", 200, 180, 150, 400, 0, m.NACELLE_D//2+75)
        self.B("PM1_PYLON_AFT", 200, 180, 150, 900, 0, m.NACELLE_D//2+75)
        self.C("  AGB+发电机+燃油泵+滑油箱+2吊点")

        self.L.extend(["",f"-- ══ CFM56-7B: {self.n} EQUIPMENT ══",""])
        return "\n".join(self.L)

    def save(self):
        pml=self.build()
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        fp=OUTPUT_DIR/f"cfm56_7b_{ts}.pml"
        fp.write_text(pml,encoding="utf-8",newline="\n")
        return fp,pml

if __name__=="__main__":
    m=CFM56(); fp,pml=m.save()
    for b in["!!Alert","UNSET(","FIRST","END EQUI","ENDS","!!WORLD","!eqp","!!CE","COLLECT","NAME =","DESC =","$P"]:
        for i,l in enumerate(pml.split("\n"),1):assert b not in l,f"{b}@L{i}"
    print(f"OK: {fp.name} | {len(pml.split(chr(10)))}L | {m.n}EQ | PML1✓")
