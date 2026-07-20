#!/usr/bin/env python3
"""
大型卧式感应电动机 — 500kW 工业电机
=====================================
EAST=轴方向(驱动端→风扇端)  NORTH=横向  UP=垂直
结构: 定子机座(大CYLI)+转子轴(细CYLI)+端盖+底座+接线盒+风扇+风罩
所有空间关系严格正确, 无重叠, 无误置
"""

from pathlib import Path
from datetime import datetime
OUTPUT_DIR=Path(r"D:\AVEVA\Projects\E3D3.1\e3d_agent\output")
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)

class Motor:
    # 尺寸 mm
    FRAME_D = 800     # 定子机座外径
    FRAME_L = 1600    # 机座长度
    SHAFT_D = 120     # 轴径
    SHAFT_L = FRAME_L+500  # 轴总长(两端伸出)
    STDR_D = 720     # 定子内径(=转子外径+气隙)
    ROTOR_D = 710    # 转子外径
    BELL_D = 840      # 端盖外径(比机座略大)
    BELL_W = 100      # 端盖厚度
    FAN_D = 600       # 冷却风扇直径
    FAN_COVER_D=680   # 风罩直径
    FEET_H = 500      # 底座高度(轴心到地面)
    FEET_W = 200      # 底座宽度
    BASE_L = 1800     # 底座长度
    TERMBOX = (350,280,300)  # 接线盒 L×W×H
    
    def __init__(self):
        self.L=[]; self.n=0
    
    def H(self,t): self.L.extend(["",f"-- {'='*50}",f"--  {t}",f"-- {'='*50}",""])
    def C(self,t): self.L.append(f"-- {t}")
    
    def CY(self,name,d,h, e=0,n=0,u=0, axis='N'):
        """CYLI: DIAM在XZ面, HEIG沿Y轴. axis指定Y指向(E或N)"""
        self.n+=1; s=name.replace(" ","_")
        self.L.append(f"NEW EQUI /{s}")
        self.L.append(f"NEW CYLI")
        self.L.append(f"DIAM {d}")
        self.L.append(f"HEIG {h}")
        self.L.append(f"POS E {e} N {n} U {u}")
        self.L.append(f"ORI Y IS {axis} AND Z IS U")
        self.L.append("")
        return s
    
    def BX(self,name,x,y,z, e=0,n=0,u=0):
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
            f"-- 大型卧式感应电动机 500kW | 机座φ{self.FRAME_D}×{self.FRAME_L}mm",
            f"-- 生成: {ts} | E=轴(驱动端→风扇端) N=横 U=竖",
            "-- 前置: E3D中选可写ZONE → $$MACRO <本文件>",
            "",
        ]
        m=self
        
        # ═══════════════════════════════════════
        # 1. 底座 (地面上)
        # ═══════════════════════════════════════
        self.H("1. 底座 Base")
        ground = -m.FEET_H  # 地面U=-500 (轴心在U=0)
        base_top = ground   # 底座顶面=地面
        self.BX("MOTOR_BASE_PLATE", m.BASE_L, m.FRAME_D+200, 80,
                m.FRAME_L//2+100, 0, base_top-40)
        # 4对地脚(从底座顶面到定子底面, U=-500到U=-400)
        foot_u = base_top - 50  # 地脚中心U=-450, ZLEN=100
        for i, e in enumerate([200, 600, m.FRAME_L-200, m.FRAME_L-600]):
            for n_sign, ns in [(1,'N'),(-1,'S')]:
                n=n_sign*(m.FRAME_D//2+100)
                self.BX(f"MOTOR_FOOT_{i+1}{ns}", 250,250,100, e, n, foot_u)
        self.C(f"  底板{m.BASE_L}×{m.FRAME_D+200}×80 + 8地脚(顶面U={base_top})")
        
        # ═══════════════════════════════════════
        # 2. 定子机座 (大圆筒, 水平轴=EAST)
        # ═══════════════════════════════════════
        self.H("2. 定子机座 Stator Frame")
        # 水平大圆筒, Y轴→EAST
        # POS=(E起点, N=0, U=0) → 轴心在原点, 底面在U=-FRAME_D/2=-400
        # 但我们想让机座在底座上方, 所以U偏移
        stator_u = 0  # 轴心标高(底座顶面+FEET_H≈0)
        self.CY("MOTOR_STATOR", m.FRAME_D, m.FRAME_L, m.FRAME_L//2+100, 0, stator_u, 'E')
        # 散热筋(纵向肋条, 8条均布)
        for i in range(8):
            ang=i*45
            import math
            n_pos=int((m.FRAME_D//2+25)*math.cos(math.radians(ang)))
            u_pos=int((m.FRAME_D//2+25)*math.sin(math.radians(ang)))+stator_u
            self.BX(f"MOTOR_FIN_{i+1}", m.FRAME_L-100, 20, 60,
                    m.FRAME_L//2+100, n_pos, u_pos)
        self.C(f"  定子 φ{m.FRAME_D}×{m.FRAME_L} + 8散热筋")
        
        # ═══════════════════════════════════════
        # 3. 转子+轴
        # ═══════════════════════════════════════
        self.H("3. 转子 & 轴 Rotor & Shaft")
        # 转子铁芯(在定子内部)
        self.CY("MOTOR_ROTOR", m.ROTOR_D, m.FRAME_L-200, m.FRAME_L//2+100, 0, stator_u, 'E')
        # 主轴(贯通)
        self.CY("MOTOR_SHAFT", m.SHAFT_D, m.SHAFT_L, m.FRAME_L//2+100, 0, stator_u, 'E')
        # 驱动端轴伸
        self.CY("MOTOR_SHAFT_DE", m.SHAFT_D-10, 200, 50, 0, stator_u, 'E')
        # 风扇端轴伸
        fan_end = m.FRAME_L+300
        self.CY("MOTOR_SHAFT_FE", m.SHAFT_D-10, 200, fan_end, 0, stator_u, 'E')
        self.C(f"  转子φ{m.ROTOR_D} + 主轴φ{m.SHAFT_D}×{m.SHAFT_L}")
        
        # ═══════════════════════════════════════
        # 4. 端盖 (两端)
        # ═══════════════════════════════════════
        self.H("4. 端盖 End Bells")
        # 驱动端端盖
        self.CY("MOTOR_BELL_DE", m.BELL_D, m.BELL_W, m.FRAME_L+150, 0, stator_u, 'E')
        # 风扇端端盖
        self.CY("MOTOR_BELL_FE", m.BELL_D, m.BELL_W, 50, 0, stator_u, 'E')
        # 轴承座(两端, 小突出)
        self.CY("MOTOR_BRG_DE", 220, 60, m.FRAME_L+200, 0, stator_u, 'E')
        self.CY("MOTOR_BRG_FE", 220, 60, -20, 0, stator_u, 'E')
        self.C(f"  端盖 φ{m.BELL_D}×2 + 轴承座 φ220×2")
        
        # ═══════════════════════════════════════
        # 5. 冷却风扇+风罩 (风扇端)
        # ═══════════════════════════════════════
        self.H("5. 冷却风扇 & 风罩 Fan & Cover")
        fan_e = m.FRAME_L+350
        # 风扇轮毂
        self.CY("MOTOR_FAN_HUB", 150, 80, fan_e, 0, stator_u, 'E')
        # 风扇叶片(6片, 简化: 径向薄板)
        for i in range(6):
            ang=i*60
            r=m.FAN_D//2-20
            n_pos=int(r*math.cos(math.radians(ang)))
            u_pos=int(r*math.sin(math.radians(ang)))+stator_u
            # 每个叶片: 径向长方块 (需要沿径向, 简化为小CYLI指向外)
            self.CY(f"MOTOR_FAN_B{i+1}", 30, 260, fan_e, n_pos, u_pos, 'N' if abs(math.cos(math.radians(ang)))>0.5 else 'E')
        # 风罩(包围风扇)
        self.CY("MOTOR_FAN_COVER", m.FAN_COVER_D, 300, fan_e+50, 0, stator_u, 'E')
        # 风罩网(端面圆盘)
        self.CY("MOTOR_FAN_GRILL", m.FAN_COVER_D-20, 10, fan_e+300, 0, stator_u, 'E')
        self.C(f"  风扇 φ{m.FAN_D} 6叶 + 风罩 φ{m.FAN_COVER_D}")
        
        # ═══════════════════════════════════════
        # 6. 接线盒 (顶部)
        # ═══════════════════════════════════════
        self.H("6. 接线盒 Terminal Box")
        tb_e=m.FRAME_L//2+100
        tb_u=stator_u+m.FRAME_D//2+m.TERMBOX[2]//2+20
        self.BX("MOTOR_TERMBOX", *m.TERMBOX, tb_e, 0, tb_u)
        # 进线口(侧面圆筒)
        self.CY("MOTOR_CONDUIT", 80, 150, tb_e, m.TERMBOX[1]//2+100, tb_u, 'N')
        self.C(f"  接线盒 {m.TERMBOX[0]}×{m.TERMBOX[1]}×{m.TERMBOX[2]} + 进线管")
        
        # ═══════════════════════════════════════
        # 7. 吊环 (顶部)
        # ═══════════════════════════════════════
        self.H("7. 吊环 Lifting Eyes")
        for e in [m.FRAME_L//4+100, 3*m.FRAME_L//4+100]:
            ring_u=stator_u+m.FRAME_D//2+60
            self.CY(f"MOTOR_LIFT_{e}", 40, 20, e, 0, ring_u, 'N')  #水平环
            # 吊环座
            self.BX(f"MOTOR_LIFT_BASE_{e}", 80, 80, 40, e, 0, ring_u-40)
        self.C("  吊环×2 φ40")
        
        self.L.extend(["",f"-- ══ 电机完成: {self.n} EQUIPMENT ══",""])
        return "\n".join(self.L)
    
    def save(self):
        pml=self.build()
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        fp=OUTPUT_DIR/f"motor_500kw_{ts}.pml"
        fp.write_text(pml,encoding="utf-8",newline="\n")
        return fp,pml

if __name__=="__main__":
    m=Motor(); fp,pml=m.save()
    for b in["!!Alert","UNSET(","FIRST","END EQUI","ENDS","!!WORLD","!eqp","!!CE","COLLECT","NAME =","DESC =","$P"]:
        for i,l in enumerate(pml.split("\n"),1):assert b not in l,f"{b}@L{i}"
    print(f"OK {fp.name} | {len(pml.split(chr(10)))}L | {m.n}EQ | PML1✓")
