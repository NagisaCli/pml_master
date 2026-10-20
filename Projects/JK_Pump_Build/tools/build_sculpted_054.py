# -*- coding: utf-8 -*-
"""
Generator for High-Fidelity Sculpted MC Pump Model: /205_PU_054
- Full detail preservation (No simplification)
- Missing fasteners/bolts completed (Completed missing fasteners)
- Coordinates normalized and CAD offsets removed (Normalized coordinates)
- Nozzles and engineering attributes perfected (Attributes and nozzles finalized)
- Motor rear hollowed fan cowl, internal shaft, fan hub & radial blades (Rear fan cowl and internals)
- Auxiliary degassing/vacuum system completed and sculpted (Auxiliary system sculpted)
"""

import math
import os

def build_sculpted_054_pml():
    lines = []
    
    # Header
    lines.append("$S-  -- Synonym translation OFF")
    lines.append("-- ----------------------------------------------------------------")
    lines.append("-- Equipment Listing    Tag: 205_PU_054 (D1 STAGE MC PUMP - High Fidelity Sculpted)")
    lines.append("-- Process: Pulp & Paper Bleach Plant D1 Stage Medium Consistency Stock Pump")
    lines.append("-- Date   : 31 Aug 2026")
    lines.append("")
    lines.append("ONERROR GOLABEL /ERROR3")
    lines.append("")
    lines.append("INPUT BEGIN")
    lines.append("NEW EQUIPMENT /205_PU_054")
    lines.append("DESC 'D1 STAGE MC PUMP'")
    lines.append("FUNC '001000'")
    lines.append("POS E 0.0mm N 0.0mm U 0.0mm")
    lines.append("ORI Y is N and Z is U")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")

    # =========================================================================
    # 1. SUBEQUIPMENT /205_PU_054_BASE (Common Baseplate and Foundation System)
    # =========================================================================
    lines.append("NEW SUBEQUIPMENT /205_PU_054_BASE")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")
    
    # Main longitudinal baseplate beams (E 48852, N 4714)
    lines.append("NEW BOX")
    lines.append("POS E 48852mm N 4714mm U 25mm")
    lines.append("XLEN 615.18mm")
    lines.append("YLEN 2000mm")
    lines.append("ZLEN 50mm")
    lines.append("END")
    
    # Side channel frames
    lines.append("NEW BOX")
    lines.append("POS E 48436.76mm N 4714mm U 41.67mm")
    lines.append("XLEN 215.31mm")
    lines.append("YLEN 2000mm")
    lines.append("ZLEN 16.67mm")
    lines.append("END")
    
    lines.append("NEW BOX")
    lines.append("POS E 49267.24mm N 4714mm U 41.67mm")
    lines.append("XLEN 215.31mm")
    lines.append("YLEN 2000mm")
    lines.append("ZLEN 16.67mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 48436.76mm N 4714mm U 8.33mm")
    lines.append("XLEN 215.31mm")
    lines.append("YLEN 2000mm")
    lines.append("ZLEN 16.67mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 49267.24mm N 4714mm U 8.33mm")
    lines.append("XLEN 215.31mm")
    lines.append("YLEN 2000mm")
    lines.append("ZLEN 16.67mm")
    lines.append("END")

    # Bottom soleplate / grout bed
    lines.append("NEW BOX")
    lines.append("POS E 48852mm N 4714mm D 21mm")
    lines.append("XLEN 1046mm")
    lines.append("YLEN 2000mm")
    lines.append("ZLEN 42mm")
    lines.append("END")

    # Motor stool & support gussets
    lines.append("NEW BOX")
    lines.append("POS E 48856.34mm N 4163.24mm U 302.93mm")
    lines.append("ORI Y is N and Z is D")
    lines.append("XLEN 390.81mm")
    lines.append("YLEN 511.18mm")
    lines.append("ZLEN 37.5mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 48535.01mm N 4163.24mm U 60.42mm")
    lines.append("XLEN 217.12mm")
    lines.append("YLEN 681.57mm")
    lines.append("ZLEN 20.83mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 49168.99mm N 4163.24mm U 60.42mm")
    lines.append("XLEN 217.12mm")
    lines.append("YLEN 681.57mm")
    lines.append("ZLEN 20.83mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 48643.57mm N 4163.24mm U 177.51mm")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 681.57mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 511.18mm")
    lines.append("HEIG 213.35mm")
    lines.append("XOFF 69.48mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 49060.43mm N 4163.24mm U 177.51mm")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 681.57mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 511.18mm")
    lines.append("HEIG 213.35mm")
    lines.append("XOFF -69.48mm")
    lines.append("END")

    # Casing stool & gussets
    lines.append("NEW BOX")
    lines.append("POS E 48847.48mm N 5619mm U 235.2mm")
    lines.append("ORI Y is N and Z is D")
    lines.append("XLEN 406.99mm")
    lines.append("YLEN 175mm")
    lines.append("ZLEN 14.58mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 48521.89mm N 5619mm U 60.42mm")
    lines.append("XLEN 226.1mm")
    lines.append("YLEN 350mm")
    lines.append("ZLEN 20.83mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 49182.11mm N 5619mm U 60.42mm")
    lines.append("XLEN 226.1mm")
    lines.append("YLEN 350mm")
    lines.append("ZLEN 20.83mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 48847.48mm N 5665.67mm U 305.71mm")
    lines.append("ORI Y is E and Z is U")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 397.94mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 316.54mm")
    lines.append("HEIG 126.45mm")
    lines.append("YOFF 4.52mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 48847.48mm N 5598.17mm U 305.71mm")
    lines.append("ORI Y is E and Z is U")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 397.94mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 316.54mm")
    lines.append("HEIG 126.45mm")
    lines.append("YOFF 4.52mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 48625.9mm N 5619mm U 149.37mm")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 291.67mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 175mm")
    lines.append("HEIG 157.07mm")
    lines.append("XOFF 72.35mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 49078.1mm N 5619mm U 149.37mm")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 291.67mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 175mm")
    lines.append("HEIG 157.07mm")
    lines.append("XOFF -72.35mm")
    lines.append("END")

    # Angled rib supports
    lines.append("NEW PYRAMID")
    lines.append("POS E 48591.46mm N 4291.02mm U 190.18mm")
    lines.append("ORI Y is W and Z is U")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 104.22mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 130.27mm")
    lines.append("HEIG 238.69mm")
    lines.append("YOFF -173.69mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 49112.54mm N 4291.02mm U 190.18mm")
    lines.append("ORI Y is E and Z is U")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 104.22mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 130.27mm")
    lines.append("HEIG 238.69mm")
    lines.append("YOFF -173.69mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 48591.46mm N 4039.81mm U 190.18mm")
    lines.append("ORI Y is W and Z is U")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 104.22mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 130.27mm")
    lines.append("HEIG 238.69mm")
    lines.append("YOFF -173.69mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 49112.54mm N 4039.81mm U 190.18mm")
    lines.append("ORI Y is E and Z is U")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 104.22mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 130.27mm")
    lines.append("HEIG 238.69mm")
    lines.append("YOFF -173.69mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 48580.68mm N 5619mm U 153.65mm")
    lines.append("ORI Y is W and Z is U")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 108.53mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 135.66mm")
    lines.append("HEIG 165.64mm")
    lines.append("YOFF -180.88mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 49123.32mm N 5619mm U 153.65mm")
    lines.append("ORI Y is E and Z is U")
    lines.append("XBOT 16.67mm")
    lines.append("YBOT 108.53mm")
    lines.append("XTOP 16.67mm")
    lines.append("YTOP 135.66mm")
    lines.append("HEIG 165.64mm")
    lines.append("YOFF -180.88mm")
    lines.append("END")

    # Complete 10 Anchor Bolts & Hex Heads on Foundation
    anchor_coords = [
        (49208.07, 3924.69, 'S'),
        (48495.93, 3924.69, 'W'),
        (49208.07, 4163.24, 'S'),
        (48495.93, 4163.24, 'W'),
        (49208.07, 4401.79, 'S'),
        (48495.93, 4401.79, 'W'),
        (49222.81, 5531.50, 'S'),
        (48481.19, 5531.50, 'W'),
        (49222.81, 5706.50, 'S'),
        (48481.19, 5706.50, 'W')
    ]
    for e_a, n_a, hex_dir in anchor_coords:
        lines.append("NEW CYLINDER")
        lines.append("ORI Z is D and Y is S")
        lines.append(f"POS E {e_a:.2f}mm N {n_a:.2f}mm U 50mm")
        lines.append("DIAM 12.5mm")
        lines.append("HEIG 75mm")
        lines.append("END")
        
        lines.append("NEW EXTRUSION")
        if hex_dir == 'S':
            lines.append("ORI Y is S and Z is U")
        else:
            lines.append("ORI Y is N and Z is U")
        lines.append(f"POS E {e_a:.2f}mm N {n_a:.2f}mm U 70.83mm")
        lines.append("HEIG 16.67mm")
        lines.append("NEW LOOP")
        lines.append("NEW VERTEX")
        lines.append("POS E 0mm N 0mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 14.43mm S 8.33mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 28.87mm N 0mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 28.87mm N 16.67mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 14.43mm N 25mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS E 0mm N 16.67mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS E 0mm N 0mm U 0mm")
        lines.append("END")
        lines.append("END")
        lines.append("END")

    lines.append("END")
    lines.append("")

    # =========================================================================
    # 2. SUBEQUIPMENT /205_PU_054_CASING (Main Pump Casing and Volute Section)
    # =========================================================================
    lines.append("NEW SUBEQUIPMENT /205_PU_054_CASING")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")

    # Main volute casing body
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 5588.9mm U 622.17mm")
    lines.append("DIAM 615mm")
    lines.append("HEIG 140mm")
    lines.append("END")

    # Front casing end cover / dished head
    lines.append("NEW DISH")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 5658.9mm U 622.17mm")
    lines.append("DIAM 633.09mm")
    lines.append("HEIG 45.22mm")
    lines.append("RADI 9.04mm")
    lines.append("END")

    # Casing front wear ring & suction neck
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is U and Y is N")
    lines.append("POS E 48852mm N 5602mm U 929.67mm")
    lines.append("DIAM 126mm")
    lines.append("HEIG 28mm")
    lines.append("END")

    lines.append("NEW CONE")
    lines.append("ORI Z is U and Y is N")
    lines.append("POS E 48852mm N 5602mm U 943.67mm")
    lines.append("DTOP 150mm")
    lines.append("DBOT 126mm")
    lines.append("HEIG 12mm")
    lines.append("END")

    # Casing drain port & plug
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is D and Y is N")
    lines.append("POS E 48852mm N 5588.9mm U 300mm")
    lines.append("DIAM 45mm")
    lines.append("HEIG 35mm")
    lines.append("END")

    lines.append("END")
    lines.append("")

    # =========================================================================
    # 3. SUBEQUIPMENT /205_PU_054_BEARING (Bearing Housing and Cantilever Transition)
    # =========================================================================
    lines.append("NEW SUBEQUIPMENT /205_PU_054_BEARING")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4609.9mm U 622.17mm")
    lines.append("DIAM 108mm")
    lines.append("HEIG 22mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4650.4mm U 622.17mm")
    lines.append("DIAM 54mm")
    lines.append("HEIG 59mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4719.4mm U 622.17mm")
    lines.append("DIAM 140mm")
    lines.append("HEIG 79mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4783.4mm U 622.17mm")
    lines.append("DIAM 210mm")
    lines.append("HEIG 49mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4867.4mm U 622.17mm")
    lines.append("DIAM 140mm")
    lines.append("HEIG 119mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4951.4mm U 622.17mm")
    lines.append("DIAM 210mm")
    lines.append("HEIG 49mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 5015.4mm U 622.17mm")
    lines.append("DIAM 140mm")
    lines.append("HEIG 79mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 5068.4mm U 622.17mm")
    lines.append("DIAM 54mm")
    lines.append("HEIG 27mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 5092.9mm U 622.17mm")
    lines.append("DIAM 248mm")
    lines.append("HEIG 22mm")
    lines.append("END")

    # Transition adapter cone
    lines.append("NEW CONE")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 5346.4mm U 622.17mm")
    lines.append("DTOP 399mm")
    lines.append("DBOT 248mm")
    lines.append("HEIG 485mm")
    lines.append("END")

    # Bearing oil sight glass & breather
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is U")
    lines.append("POS E 48960mm N 4867.4mm U 622.17mm")
    lines.append("DIAM 32mm")
    lines.append("HEIG 20mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is U and Y is N")
    lines.append("POS E 48852mm N 4867.4mm U 700mm")
    lines.append("DIAM 25mm")
    lines.append("HEIG 30mm")
    lines.append("END")

    lines.append("END")
    lines.append("")

    # =========================================================================
    # 4. SUBEQUIPMENT /205_PU_054_DRIVER (Main Driver: Cooling Fins, Terminal Box, Lifting Lugs, Rear Cowl)
    # =========================================================================
    lines.append("NEW SUBEQUIPMENT /205_PU_054_DRIVER")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")

    # Stator Main Barrel
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4183.3mm U 622.17mm")
    lines.append("DIAM 625.3mm")
    lines.append("HEIG 679.2mm")
    lines.append("END")

    # Front DE Flange and Shaft
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4533.9mm U 622.17mm")
    lines.append("DIAM 555mm")
    lines.append("HEIG 22mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4558.4mm U 622.17mm")
    lines.append("DIAM 399mm")
    lines.append("HEIG 27mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 4585.4mm U 622.17mm")
    lines.append("DIAM 237mm")
    lines.append("HEIG 27mm")
    lines.append("END")

    # Stator Surface Axial Cooling Fins (Preserved 28 radial Box fins - duplicate removed)
    fin_angles = [
        (49072.49, 806.78, "E 50.3919 D"),
        (49101.20, 765.69, "E 60.3919 D"),
        (49122.34, 720.24, "E 70.3919 D"),
        (49135.26, 671.80, "E 80.3919 D"),
        (49139.57, 621.86, "W 89.6081 D"),
        (49135.15, 571.93, "W 79.6081 D"),
        (49122.13, 523.53, "W 69.6081 D"),
        (49100.89, 478.12, "W 59.6081 D"),
        (49072.10, 437.09, "W 49.6081 D"),
        (49036.61, 401.68, "W 39.6081 D"),
        (48995.52, 372.97, "W 29.6081 D"),
        (48950.07, 351.83, "W 19.6081 D"),
        (48901.63, 338.91, "W 9.60813 D"),
        (48851.69, 334.60, "W 0.391873 U"),
        (48801.76, 339.02, "W 10.3919 U"),
        (48753.36, 352.04, "W 20.3919 U"),
        (48707.95, 373.28, "W 30.3919 U"),
        (48666.92, 402.07, "W 40.3919 U"),
        (48631.51, 437.56, "W 50.3919 U"),
        (48602.80, 478.65, "W 60.3919 U"),
        (48581.66, 524.10, "W 70.3919 U"),
        (48568.74, 572.54, "W 80.3919 U"),
        (48564.43, 622.48, "E 89.6081 U"),
        (48568.85, 672.41, "E 79.6081 U"),
        (48581.87, 720.81, "E 69.6081 U"),
        (48603.11, 766.22, "E 59.6081 U"),
        (48631.90, 807.25, "E 49.6081 U")
    ]
    for e_fin, u_fin, z_rot in fin_angles:
        lines.append("NEW BOX")
        lines.append(f"ORI Z is {z_rot} and Y is N")
        lines.append(f"POS E {e_fin:.2f}mm N 4072.8mm U {u_fin:.2f}mm")
        lines.append("XLEN 89.85mm")
        lines.append("YLEN 900.2mm")
        lines.append("ZLEN 17.97mm")
        lines.append("END")

    # Stator Intermediate & DE Ring
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 3958.25mm U 622.17mm")
    lines.append("DIAM 625.28mm")
    lines.append("HEIG 229.1mm")
    lines.append("END")

    # Terminal Box Assembly
    lines.append("NEW BOX")
    lines.append("POS E 48846.62mm N 4361.8mm U 961.84mm")
    lines.append("XLEN 179.78mm")
    lines.append("YLEN 208mm")
    lines.append("ZLEN 80mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("POS E 48846.62mm N 4361.8mm U 1046.4mm")
    lines.append("XBOT 179.78mm")
    lines.append("YBOT 208mm")
    lines.append("XTOP 179.78mm")
    lines.append("YTOP 236mm")
    lines.append("HEIG 108mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 48846.7mm N 4361.8mm U 1117.9mm")
    lines.append("XLEN 178.24mm")
    lines.append("YLEN 236mm")
    lines.append("ZLEN 35mm")
    lines.append("END")

    # 4 Cable Glands with Hex Cutouts
    t_glands = [
        (48935.82, 4303.8, 'W'),
        (48935.82, 4419.8, 'W'),
        (48757.42, 4419.8, 'E'),
        (48757.42, 4303.8, 'E')
    ]
    for eg, ng, og in t_glands:
        lines.append("NEW CYLINDER")
        lines.append(f"ORI Z is {og} and Y is U")
        lines.append(f"POS E {eg:.2f}mm N {ng:.1f}mm U 1035.4mm")
        lines.append("DIAM 65mm")
        lines.append("HEIG 60mm")
        lines.append("NEW NBOX")
        lines.append("ORI Z is N and Y is W")
        lines.append("POS E 0mm N 0.02mm D 30mm")
        lines.append("XLEN 20mm")
        lines.append("YLEN 65mm")
        lines.append("ZLEN 8.45mm")
        lines.append("END")
        lines.append("NEW NBOX")
        lines.append("ORI Z is N and Y is D")
        lines.append("POS E 0mm N 0mm D 30mm")
        lines.append("XLEN 10mm")
        lines.append("YLEN 20mm")
        lines.append("ZLEN 70mm")
        lines.append("END")
        lines.append("END")

    # Lifting Eyebolts and Seating Bosses
    lines.append("NEW BOX")
    lines.append("POS E 48665.61mm N 4121.83mm U 871.99mm")
    lines.append("XLEN 40mm")
    lines.append("YLEN 30mm")
    lines.append("ZLEN 30mm")
    lines.append("END")

    lines.append("NEW CTORUS")
    lines.append("ORI Z is W and Y is D")
    lines.append("POS E 48653.61mm N 4123.34mm U 906.96mm")
    lines.append("RINS 20mm")
    lines.append("ROUT 36mm")
    lines.append("ANGL 180degree")
    lines.append("END")

    lines.append("NEW CTORUS")
    lines.append("ORI Z is W and Y is U")
    lines.append("POS E 48653.61mm N 4123.34mm U 906.96mm")
    lines.append("RINS 20mm")
    lines.append("ROUT 36mm")
    lines.append("ANGL 180degree")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("ORI Z is D and Y is N")
    lines.append("POS E 49038.39mm N 4121.83mm U 871.99mm")
    lines.append("XLEN 40mm")
    lines.append("YLEN 30mm")
    lines.append("ZLEN 30mm")
    lines.append("END")

    lines.append("NEW CTORUS")
    lines.append("ORI Z is W and Y is U")
    lines.append("POS E 49050.39mm N 4123.34mm U 906.96mm")
    lines.append("RINS 20mm")
    lines.append("ROUT 36mm")
    lines.append("ANGL 180degree")
    lines.append("END")

    lines.append("NEW CTORUS")
    lines.append("ORI Z is W and Y is D")
    lines.append("POS E 49050.39mm N 4123.34mm U 906.96mm")
    lines.append("RINS 20mm")
    lines.append("ROUT 36mm")
    lines.append("ANGL 180degree")
    lines.append("END")

    # -------------------------------------------------------------------------
    # Sculpted: Rear Fan Cowl & Internal Details
    # -------------------------------------------------------------------------
    # Rear Stator Transition & NDE Bearing Shield
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 3780mm U 622.17mm")
    lines.append("DIAM 630mm")
    lines.append("HEIG 35mm")
    lines.append("END")

    # Rear Bearing Cover
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 3745mm U 622.17mm")
    lines.append("DIAM 320mm")
    lines.append("HEIG 35mm")
    lines.append("END")

    # Grease pipe / nipple on NDE
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is U and Y is N")
    lines.append("POS E 48852mm N 3745mm U 800mm")
    lines.append("DIAM 16mm")
    lines.append("HEIG 40mm")
    lines.append("END")

    # Internal Shaft Extension at Rear
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 3670mm U 622.17mm")
    lines.append("DIAM 75mm")
    lines.append("HEIG 140mm")
    lines.append("END")

    # Internal Cooling Fan Hub
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 3660mm U 622.17mm")
    lines.append("DIAM 180mm")
    lines.append("HEIG 45mm")
    lines.append("END")

    # Internal Cooling Fan Radial Blades (8 Sculpted Radial Impeller Blades)
    for i_blade in range(8):
        ang_deg = i_blade * 45.0
        ang_rad = math.radians(ang_deg)
        r_mid = 190.0
        e_blade = 48852.0 + r_mid * math.cos(ang_rad)
        u_blade = 622.17 + r_mid * math.sin(ang_rad)
        
        cos_v = math.cos(ang_rad)
        sin_v = math.sin(ang_rad)
        lines.append("NEW BOX")
        if abs(cos_v) > 0.999:
            z_dir = "E" if cos_v > 0 else "W"
        elif abs(sin_v) > 0.999:
            z_dir = "U" if sin_v > 0 else "D"
        else:
            e_part = f"E {abs(cos_v):.4f}" if cos_v >= 0 else f"W {abs(cos_v):.4f}"
            u_part = f"U {abs(sin_v):.4f}" if sin_v >= 0 else f"D {abs(sin_v):.4f}"
            z_dir = f"{e_part} {u_part}"
        lines.append(f"ORI Z is {z_dir} and Y is N")
        lines.append(f"POS E {e_blade:.2f}mm N 3660mm U {u_blade:.2f}mm")
        lines.append("XLEN 12mm")
        lines.append("YLEN 40mm")
        lines.append("ZLEN 180mm")
        lines.append("END")

    # Outer Hollow Fan Cowl Shell
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 3733.2mm U 622.17mm")
    lines.append("DIAM 700mm")
    lines.append("HEIG 221mm")
    # Sculpt internal hollow chamber inside cowl
    lines.append("NEW NCYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 3733.2mm U 622.17mm")
    lines.append("DIAM 660mm")
    lines.append("HEIG 225mm")
    lines.append("END")
    lines.append("END")

    # Rear Cowl Dome Cone with Air Intake Grill Slots
    lines.append("NEW CONE")
    lines.append("ORI Z is S and Y is U")
    lines.append("POS E 48852mm N 3595.7mm U 622.17mm")
    lines.append("DTOP 518mm")
    lines.append("DBOT 700mm")
    lines.append("HEIG 54mm")
    # Hollow out the cone interior
    lines.append("NEW NCONE")
    lines.append("ORI Z is S and Y is U")
    lines.append("POS E 48852mm N 3595.7mm U 622.17mm")
    lines.append("DTOP 480mm")
    lines.append("DBOT 660mm")
    lines.append("HEIG 56mm")
    lines.append("END")
    lines.append("END")

    # Protective Air Intake Wire Mesh / Grille Ring on Rear Cowl Face
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 3568mm U 622.17mm")
    lines.append("DIAM 518mm")
    lines.append("HEIG 6mm")
    lines.append("NEW NCYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 48852mm N 3568mm U 622.17mm")
    lines.append("DIAM 480mm")
    lines.append("HEIG 10mm")
    lines.append("END")
    lines.append("END")

    # Rear Grille Radial Cross Braces (8-fold protective louvers)
    for i_louver in range(4):
        ang_deg = i_louver * 45.0
        ang_rad = math.radians(ang_deg)
        cos_v = math.cos(ang_rad)
        sin_v = math.sin(ang_rad)
        lines.append("NEW BOX")
        if abs(cos_v) > 0.999:
            z_dir = "E"
        elif abs(sin_v) > 0.999:
            z_dir = "U"
        else:
            e_part = f"E {abs(cos_v):.4f}" if cos_v >= 0 else f"W {abs(cos_v):.4f}"
            u_part = f"U {abs(sin_v):.4f}" if sin_v >= 0 else f"D {abs(sin_v):.4f}"
            z_dir = f"{e_part} {u_part}"
        lines.append(f"ORI Z is {z_dir} and Y is N")
        lines.append("POS E 48852mm N 3568mm U 622.17mm")
        lines.append("XLEN 8mm")
        lines.append("YLEN 6mm")
        lines.append("ZLEN 480mm")
        lines.append("END")

    # Cowl Side Brackets (4 Radial Mounting Tabs)
    lines.append("NEW BOX")
    lines.append("POS E 48541.85mm N 3733.2mm U 621.9mm")
    lines.append("ORI Z is E 89.6081 U and Y is N")
    lines.append("XLEN 83mm")
    lines.append("YLEN 221mm")
    lines.append("ZLEN 5mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 48851.73mm N 3733.2mm U 932.32mm")
    lines.append("ORI Z is E 0.3919 D and Y is N")
    lines.append("XLEN 83mm")
    lines.append("YLEN 221mm")
    lines.append("ZLEN 5mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 49162.15mm N 3733.2mm U 622.44mm")
    lines.append("ORI Z is W 89.6081 D and Y is N")
    lines.append("XLEN 83mm")
    lines.append("YLEN 221mm")
    lines.append("ZLEN 5mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS E 48852.27mm N 3733.2mm U 312.02mm")
    lines.append("ORI Z is W 0.3919 U and Y is N")
    lines.append("XLEN 83mm")
    lines.append("YLEN 221mm")
    lines.append("ZLEN 5mm")
    lines.append("END")

    lines.append("END")
    lines.append("")

    # =========================================================================
    # 5. SUBEQUIPMENT /205_PU_054_MOTOR_FRAME (Motor Slide Base and 4th Bolt)
    # =========================================================================
    lines.append("NEW SUBEQUIPMENT /205_PU_054_MOTOR_FRAME")
    lines.append("POS E 48499.16mm N 6841.31mm U 397.17mm")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")

    # 4 Base Mounting Pads
    for ep, np in [(110, 178), (110, -178), (425, 178), (425, -178)]:
        n_str = f"N {np}mm" if np >= 0 else f"S {-np}mm"
        lines.append("NEW BOX")
        lines.append(f"POS E {ep}mm {n_str} U 11mm")
        lines.append("XLEN 110mm")
        lines.append("YLEN 85mm")
        lines.append("ZLEN 22mm")
        lines.append("END")

    # 4 Tapered Stool Columns
    for ep, np in [(110, 168), (110, -168), (425, 168), (425, -168)]:
        n_str = f"N {np}mm" if np >= 0 else f"S {-np}mm"
        lines.append("NEW PYRAMID")
        lines.append(f"POS E {ep}mm {n_str} U 56mm")
        lines.append("XBOT 90mm")
        lines.append("YBOT 65mm")
        lines.append("XTOP 65mm")
        lines.append("YTOP 42mm")
        lines.append("HEIG 68mm")
        lines.append("END")

    # 8 Stiffener Web Plates
    for ep, np in [(82, 168), (138, 168), (82, -168), (138, -168),
                   (397, 168), (453, 168), (397, -168), (453, -168)]:
        n_str = f"N {np}mm" if np >= 0 else f"S {-np}mm"
        lines.append("NEW BOX")
        lines.append(f"POS E {ep}mm {n_str} U 49.5mm")
        lines.append("XLEN 12mm")
        lines.append("YLEN 60mm")
        lines.append("ZLEN 55mm")
        lines.append("END")

    # Complete 4 Anchor Cylinders (including the previously missing 4th one at E 425 S 178!)
    for ep, np in [(110, 178), (110, -178), (425, 178), (425, -178)]:
        n_str = f"N {np}mm" if np >= 0 else f"S {-np}mm"
        lines.append("NEW CYLINDER")
        lines.append(f"POS E {ep}mm {n_str} U 39.5mm")
        lines.append("DIAM 20mm")
        lines.append("HEIG 35mm")
        lines.append("END")

    # Belt tensioning lead screws & adjustment hex nuts
    for np in [168, -168]:
        n_str = f"N {np}mm" if np >= 0 else f"S {-np}mm"
        lines.append("NEW CYLINDER")
        lines.append("ORI Z is E and Y is U")
        lines.append(f"POS E 510mm {n_str} U 56mm")
        lines.append("DIAM 16mm")
        lines.append("HEIG 90mm")
        lines.append("END")
        lines.append("NEW BOX")
        lines.append(f"POS E 530mm {n_str} U 56mm")
        lines.append("XLEN 24mm")
        lines.append("YLEN 24mm")
        lines.append("ZLEN 24mm")
        lines.append("END")

    lines.append("END")
    lines.append("")

    # =========================================================================
    # 6. SUBEQUIPMENT /205_PU_054_AID_MOTOR_1 (Auxiliary Motor 1 Body and Base)
    # =========================================================================
    lines.append("NEW SUBEQUIPMENT /205_PU_054_AID_MOTOR_1")
    lines.append("POS E 48027.22mm N 4194mm D 42mm")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")

    # Baseplate
    lines.append("NEW BOX")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS E 0mm N 0mm U 25mm")
    lines.append("XLEN 603.77mm")
    lines.append("YLEN 50mm")
    lines.append("ZLEN 960mm")
    lines.append("END")

    # 4 Fastener Hex Heads
    hex_aid1 = [
        ("W 153.15mm S 313.61mm", ""),
        ("W 153.15mm S 165.61mm", "ORI Y is S and Z is U"),
        ("W 85.37mm S 165.61mm", "ORI Y is S and Z is U"),
        ("W 85.37mm S 313.61mm", "")
    ]
    for pos_h, ori_h in hex_aid1:
        lines.append("NEW EXTRUSION")
        if ori_h: lines.append(ori_h)
        lines.append(f"POS {pos_h} U 70mm")
        lines.append("HEIG 16.67mm")
        lines.append("NEW LOOP")
        lines.append("NEW VERTEX")
        lines.append("POS E 0mm N 0mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 14.43mm S 8.33mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 28.87mm N 0mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 28.87mm N 16.67mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 14.43mm N 25mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS E 0mm N 16.67mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS E 0mm N 0mm U 0mm")
        lines.append("END")
        lines.append("END")
        lines.append("END")

    # Support Gussets
    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is W")
    lines.append("POS W 40.37mm S 244.61mm U 102.5mm")
    lines.append("XBOT 150mm")
    lines.append("YBOT 10mm")
    lines.append("XTOP 100mm")
    lines.append("YTOP 10mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF 50mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is E")
    lines.append("POS W 198.14mm S 244.61mm U 102.5mm")
    lines.append("XBOT 150mm")
    lines.append("YBOT 10mm")
    lines.append("XTOP 100mm")
    lines.append("YTOP 10mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF 50mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is W")
    lines.append("POS W 191.3mm S 204.61mm U 102.34mm")
    lines.append("XBOT 10mm")
    lines.append("YBOT 50mm")
    lines.append("XTOP 10mm")
    lines.append("YTOP 50mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF -50mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is E")
    lines.append("POS W 47.22mm S 204.61mm U 102.34mm")
    lines.append("XBOT 10mm")
    lines.append("YBOT 50mm")
    lines.append("XTOP 10mm")
    lines.append("YTOP 50mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF -50mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is W")
    lines.append("POS W 191.3mm S 284.61mm U 102.34mm")
    lines.append("XBOT 10mm")
    lines.append("YBOT 50mm")
    lines.append("XTOP 10mm")
    lines.append("YTOP 50mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF -50mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is E")
    lines.append("POS W 47.22mm S 284.61mm U 102.34mm")
    lines.append("XBOT 10mm")
    lines.append("YBOT 50mm")
    lines.append("XTOP 10mm")
    lines.append("YTOP 50mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF -50mm")
    lines.append("END")

    # 36 Fin Plates on Aux Motor Stator (Preserved fine details)
    aid1_fins = [
        ("W 119.19mm", 398.99, "E 0.391873 D"),
        ("W 97.66mm", 397.10, "E 10.3919 D"),
        ("W 76.79mm", 391.49, "E 20.3919 D"),
        ("W 57.2mm", 382.35, "E 30.3919 D"),
        ("W 39.5mm", 369.94, "E 40.3919 D"),
        ("W 24.23mm", 354.65, "E 50.3919 D"),
        ("W 11.84mm", 336.94, "E 60.3919 D"),
        ("W 2.71mm", 317.34, "E 70.3919 D"),
        ("E 2.87mm", 296.46, "E 80.3919 D"),
        ("E 4.74mm", 274.93, "W 89.6081 D"),
        ("E 2.85mm", 253.40, "W 79.6081 D"),
        ("W 2.76mm", 232.52, "W 69.6081 D"),
        ("W 11.9mm", 212.94, "W 59.6081 D"),
        ("W 24.31mm", 195.24, "W 49.6081 D"),
        ("W 39.6mm", 179.96, "W 39.6081 D"),
        ("W 57.31mm", 167.58, "W 29.6081 D"),
        ("W 76.91mm", 158.45, "W 19.6081 D"),
        ("W 97.79mm", 152.87, "W 9.60813 D"),
        ("W 119.32mm", 151.00, "W 0.391873 U"),
        ("W 140.85mm", 152.89, "W 10.3919 U"),
        ("W 161.73mm", 158.50, "W 20.3919 U"),
        ("W 181.31mm", 167.64, "W 30.3919 U"),
        ("W 199.01mm", 180.05, "W 40.3919 U"),
        ("W 214.29mm", 195.34, "W 50.3919 U"),
        ("W 226.68mm", 213.05, "W 60.3919 U"),
        ("W 235.8mm", 232.65, "W 70.3919 U"),
        ("W 241.38mm", 253.53, "W 80.3919 U"),
        ("W 243.26mm", 275.06, "E 89.6081 U"),
        ("W 241.36mm", 296.59, "E 79.6081 U"),
        ("W 235.76mm", 317.47, "E 69.6081 U"),
        ("W 226.61mm", 337.05, "E 59.6081 U"),
        ("W 214.2mm", 354.75, "E 49.6081 U"),
        ("W 198.91mm", 370.03, "E 39.6081 U"),
        ("W 181.2mm", 382.41, "E 29.6081 U"),
        ("W 161.61mm", 391.54, "E 19.6081 U"),
        ("W 140.73mm", 397.12, "E 9.60813 U")
    ]
    for w_f, u_f, z_rf in aid1_fins:
        lines.append("NEW BOX")
        lines.append(f"ORI Z is {z_rf} and Y is N")
        lines.append(f"POS {w_f} S 239.22mm U {u_f:.2f}mm")
        lines.append("XLEN 20mm")
        lines.append("YLEN 275mm")
        lines.append("ZLEN 5mm")
        lines.append("END")

    # Aux Motor Stator, Cones & Pulleys
    lines.append("NEW CONE")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 119.26mm S 74.72mm U 275mm")
    lines.append("DTOP 183mm")
    lines.append("DBOT 248mm")
    lines.append("HEIG 54mm")
    lines.append("END")

    lines.append("NEW CONE")
    lines.append("ORI Z is S and Y is U")
    lines.append("POS W 119.26mm S 403.72mm U 275mm")
    lines.append("DTOP 183mm")
    lines.append("DBOT 248mm")
    lines.append("HEIG 54mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 119.26mm S 239.22mm U 275mm")
    lines.append("DIAM 248mm")
    lines.append("HEIG 275mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 127.39mm N 19.78mm U 275mm")
    lines.append("DIAM 108mm")
    lines.append("HEIG 135mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 127.39mm N 100.78mm U 275mm")
    lines.append("DIAM 81mm")
    lines.append("HEIG 27mm")
    lines.append("END")

    lines.append("NEW CONE")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 127.39mm N 207.28mm U 275mm")
    lines.append("DTOP 167mm")
    lines.append("DBOT 108mm")
    lines.append("HEIG 186mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 127.39mm N 313.78mm U 275mm")
    lines.append("DIAM 173mm")
    lines.append("HEIG 27mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 127.39mm N 335.28mm U 275mm")
    lines.append("DIAM 183mm")
    lines.append("HEIG 16mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 127.39mm N 345.78mm U 275mm")
    lines.append("DIAM 173mm")
    lines.append("HEIG 5mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 127.39mm N 428.78mm U 275mm")
    lines.append("DIAM 248mm")
    lines.append("HEIG 119mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 127.39mm N 499.28mm U 275mm")
    lines.append("DIAM 259mm")
    lines.append("HEIG 22mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 194.39mm N 539.3mm U 275mm")
    lines.append("DIAM 81mm")
    lines.append("HEIG 59mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 60.39mm N 539.3mm U 275mm")
    lines.append("DIAM 81mm")
    lines.append("HEIG 59mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 194.39mm N 593.3mm U 275mm")
    lines.append("DIAM 59mm")
    lines.append("HEIG 49mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 198.15mm S 239.61mm U 65mm")
    lines.append("XLEN 100mm")
    lines.append("YLEN 10mm")
    lines.append("ZLEN 178mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 40.37mm S 239.61mm U 65mm")
    lines.append("XLEN 100mm")
    lines.append("YLEN 10mm")
    lines.append("ZLEN 178mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 0.15mm N 3.61mm U 55mm")
    lines.append("XLEN 496mm")
    lines.append("YLEN 10mm")
    lines.append("ZLEN 857mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS W 119.29mm S 244.61mm U 143.49mm")
    lines.append("XLEN 117.7mm")
    lines.append("YLEN 183mm")
    lines.append("ZLEN 16.98mm")
    lines.append("END")

    # Anchor Fastener Cylinders
    for wc, sc in [(167.58, 305.27), (167.58, 173.95), (70.94, 173.95), (70.94, 305.27)]:
        lines.append("NEW CYLINDER")
        lines.append(f"POS W {wc:.2f}mm S {sc:.2f}mm U 49.16mm")
        lines.append("DIAM 12.5mm")
        lines.append("HEIG 75mm")
        lines.append("END")

    lines.append("NEW BOX")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 206.24mm N 414.29mm U 64.02mm")
    lines.append("XLEN 100mm")
    lines.append("YLEN 10mm")
    lines.append("ZLEN 60mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 48.46mm N 414.29mm U 64.02mm")
    lines.append("XLEN 100mm")
    lines.append("YLEN 10mm")
    lines.append("ZLEN 60mm")
    lines.append("END")

    for wc in [173.54, 80.91]:
        lines.append("NEW CYLINDER")
        lines.append(f"POS W {wc:.2f}mm N 414.12mm U 48.18mm")
        lines.append("DIAM 12.5mm")
        lines.append("HEIG 75mm")
        lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is E")
    lines.append("POS W 206.24mm N 414.28mm U 101.52mm")
    lines.append("XBOT 60mm")
    lines.append("YBOT 10mm")
    lines.append("XTOP 60mm")
    lines.append("YTOP 10mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF 50mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is W")
    lines.append("POS W 48.53mm N 414.28mm U 101.52mm")
    lines.append("XBOT 60mm")
    lines.append("YBOT 10mm")
    lines.append("XTOP 60mm")
    lines.append("YTOP 10mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF 50mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is W")
    lines.append("POS W 206.24mm N 409.28mm U 101.52mm")
    lines.append("XBOT 10mm")
    lines.append("YBOT 50mm")
    lines.append("XTOP 10mm")
    lines.append("YTOP 50mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF -50mm")
    lines.append("END")

    lines.append("NEW PYRAMID")
    lines.append("ORI Z is U and Y is E")
    lines.append("POS W 48.54mm N 409.28mm U 101.52mm")
    lines.append("XBOT 10mm")
    lines.append("YBOT 50mm")
    lines.append("XTOP 10mm")
    lines.append("YTOP 50mm")
    lines.append("HEIG 65mm")
    lines.append("YOFF -50mm")
    lines.append("END")

    lines.append("NEW BOX")
    lines.append("POS W 127.39mm N 409.28mm U 142.51mm")
    lines.append("XLEN 117.7mm")
    lines.append("YLEN 80mm")
    lines.append("ZLEN 16.98mm")
    lines.append("END")

    # Hex Fasteners 2
    for w_h in [159.11, 95.34]:
        lines.append("NEW EXTRUSION")
        lines.append(f"POS W {w_h:.2f}mm N 405.79mm U 69.01mm")
        lines.append("HEIG 16.67mm")
        lines.append("NEW LOOP")
        lines.append("NEW VERTEX")
        lines.append("POS E 0mm N 0mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 14.43mm S 8.33mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 28.87mm N 0mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 28.87mm N 16.67mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS W 14.43mm N 25mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS E 0mm N 16.67mm U 0mm")
        lines.append("END")
        lines.append("NEW VERTEX")
        lines.append("POS E 0mm N 0mm U 0mm")
        lines.append("END")
        lines.append("END")
        lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is N and Y is U")
    lines.append("POS W 127.39mm N 358.78mm U 275mm")
    lines.append("DIAM 199mm")
    lines.append("HEIG 21mm")
    lines.append("END")

    lines.append("END")
    lines.append("")

    # =========================================================================
    # 7. SUBEQUIPMENT /205_PU_054_AID_MOTOR_2 (Vacuum Degassing Pump, Belt Guard and Extrusions)
    # =========================================================================
    lines.append("NEW SUBEQUIPMENT /205_PU_054_AID_MOTOR_2")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")

    # Normalized Belt Guard Extrusion & Nxtrusion (CAD Coordinates Normalized)
    lines.append("NEW EXTRUSION")
    lines.append("ORI Z is W and Y is U")
    lines.append("POS E 48393mm N 6416mm U 622.17mm")
    lines.append("HEIG 135mm")
    lines.append("NEW LOOP")
    
    # Outer stadium loop (24 vertices centered around (0,0))
    loop_v_outer = [
        (-428.50, -156.00), (428.50, -156.00), (476.70, -148.37), (520.19, -126.21),
        (554.70, -91.70), (576.86, -48.21), (584.50, 0.00), (576.86, 48.21),
        (554.70, 91.69), (520.19, 126.21), (476.70, 148.36), (428.50, 156.00),
        (0.00, 156.00), (-428.50, 156.00), (-476.71, 148.36), (-520.20, 126.21),
        (-554.71, 91.69), (-576.87, 48.21), (-584.50, 0.00), (-576.87, -48.21),
        (-554.71, -91.70), (-520.20, -126.21), (-476.71, -148.37), (-428.50, -156.00)
    ]
    for vx, vy in loop_v_outer:
        x_str = f"E {vx:.2f}mm" if vx >= 0 else f"W {-vx:.2f}mm"
        y_str = f"N {vy:.2f}mm" if vy >= 0 else f"S {-vy:.2f}mm"
        lines.append("NEW VERTEX")
        lines.append(f"POS {x_str} {y_str} U 0mm")
        lines.append("END")
    lines.append("END")

    # Inner hollow loop
    lines.append("NEW NXTRUSION")
    lines.append("HEIG 135mm")
    lines.append("NEW LOOP")
    loop_v_inner = [
        (-428.50, -146.00), (428.50, -146.00), (473.61, -138.86), (514.31, -118.12),
        (546.61, -85.82), (567.35, -45.12), (574.50, 0.00), (567.35, 45.12),
        (546.61, 85.82), (514.31, 118.12), (473.61, 138.85), (428.50, 146.00),
        (-428.50, 146.00), (-473.62, 138.85), (-514.32, 118.12), (-546.62, 85.82),
        (-567.36, 45.12), (-574.50, 0.00), (-567.36, -45.12), (-546.62, -85.82),
        (-514.32, -118.12), (-473.62, -138.86), (-428.50, -146.00)
    ]
    for vx, vy in loop_v_inner:
        x_str = f"E {vx:.2f}mm" if vx >= 0 else f"W {-vx:.2f}mm"
        y_str = f"N {vy:.2f}mm" if vy >= 0 else f"S {-vy:.2f}mm"
        lines.append("NEW VERTEX")
        lines.append(f"POS {x_str} {y_str} U 0mm")
        lines.append("END")
    lines.append("END")
    lines.append("END")
    lines.append("END")

    # Aux Base Support Block
    lines.append("NEW BOX")
    lines.append("POS E 48738.16mm N 6842.31mm U 177.67mm")
    lines.append("XLEN 1078mm")
    lines.append("YLEN 803mm")
    lines.append("ZLEN 439mm")
    lines.append("END")

    # 36 Fin Plates on Aux Motor 2 (Preserved fine details)
    aid2_fins = [
        (48765.26, 6842.31, 790.93, "E 0.391873 D", "S"),
        (48765.26, 6813.01, 788.36, "E 0.068049 N 0.38592 D", "S 10 D"),
        (48765.26, 6784.59, 780.75, "E 0.13403 N 0.36824 D", "S 20 D"),
        (48765.26, 6757.93, 768.32, "E 0.195939 N 0.339372 D", "S 30 D"),
        (48765.26, 6733.84, 751.44, "E 0.251894 N 0.300191 D", "S 40 D"),
        (48765.26, 6713.04, 730.64, "E 0.300194 N 0.25189 D", "S 50 D"),
        (48765.26, 6696.16, 706.55, "E 0.339374 N 0.195936 D", "S 60 D"),
        (48765.26, 6683.73, 679.89, "E 0.368241 N 0.134028 D", "S 70 D"),
        (48765.26, 6676.12, 651.47, "E 0.38592 N 0.068048 D", "S 80 D"),
        (48765.26, 6673.55, 622.17, "E 0.391873 N", "D"),
        (48765.26, 6676.12, 592.87, "E 0.38592 N 0.068048 U", "N 80 D"),
        (48765.26, 6683.73, 564.45, "E 0.368241 N 0.134028 U", "N 70 D"),
        (48765.26, 6696.16, 537.79, "E 0.339374 N 0.195936 U", "N 60 D"),
        (48765.26, 6713.04, 513.70, "E 0.300194 N 0.25189 U", "N 50 D"),
        (48765.26, 6733.84, 492.90, "E 0.251894 N 0.300191 U", "N 40 D"),
        (48765.26, 6757.93, 476.02, "E 0.195939 N 0.339372 U", "N 30 D"),
        (48765.26, 6784.59, 463.59, "E 0.13403 N 0.36824 U", "N 20 D"),
        (48765.26, 6813.01, 455.98, "E 0.068049 N 0.38592 U", "N 10 D"),
        (48765.26, 6842.31, 453.41, "E 0.391873 U", "N"),
        (48765.26, 6871.61, 455.98, "E 0.068049 S 0.38592 U", "N 10 U"),
        (48765.26, 6900.03, 463.59, "E 0.13403 S 0.36824 U", "N 20 U"),
        (48765.26, 6926.69, 476.02, "E 0.195939 S 0.339372 U", "N 30 U"),
        (48765.26, 6950.78, 492.90, "E 0.251894 S 0.300191 U", "N 40 U"),
        (48765.26, 6971.58, 513.70, "E 0.300194 S 0.25189 U", "N 50 U"),
        (48765.26, 6988.46, 537.79, "E 0.339374 S 0.195936 U", "N 60 U"),
        (48765.26, 7000.89, 564.45, "E 0.368241 S 0.134028 U", "N 70 U"),
        (48765.26, 7008.50, 592.87, "E 0.38592 S 0.068048 U", "N 80 U"),
        (48765.26, 7011.07, 622.17, "E 0.391873 S", "U"),
        (48765.26, 7008.50, 651.47, "E 0.38592 S 0.068048 D", "S 80 U"),
        (48765.26, 7000.89, 679.89, "E 0.368241 S 0.134028 D", "S 70 U"),
        (48765.26, 6988.46, 706.55, "E 0.339374 S 0.195936 D", "S 60 U"),
        (48765.26, 6971.58, 730.64, "E 0.300194 S 0.25189 D", "S 50 U"),
        (48765.26, 6950.78, 751.44, "E 0.251894 S 0.300191 D", "S 40 U"),
        (48765.26, 6926.69, 768.32, "E 0.195939 S 0.339372 D", "S 30 U"),
        (48765.26, 6900.03, 780.75, "E 0.13403 S 0.36824 D", "S 20 U"),
        (48765.26, 6871.61, 788.36, "E 0.068049 S 0.38592 D", "S 10 U")
    ]
    for ea2, na2, ua2, y_dir, z_dir in aid2_fins:
        lines.append("NEW BOX")
        lines.append(f"ORI Z is {z_dir} and Y is {y_dir}")
        lines.append(f"POS E {ea2:.2f}mm N {na2:.2f}mm U {ua2:.2f}mm")
        lines.append("XLEN 89.85mm")
        lines.append("YLEN 560.69mm")
        lines.append("ZLEN 5mm")
        lines.append("END")

    # Aux Motor Body & Cones
    lines.append("NEW CONE")
    lines.append("ORI Z is E and Y is U")
    lines.append("POS E 49070.29mm N 6842.31mm U 622.17mm")
    lines.append("DTOP 274.93mm")
    lines.append("DBOT 423.53mm")
    lines.append("HEIG 50mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is U")
    lines.append("POS E 48764.96mm N 6842.31mm U 622.17mm")
    lines.append("DIAM 393.53mm")
    lines.append("HEIG 560.65mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is U")
    lines.append("POS E 48471.16mm N 6842.31mm U 622.17mm")
    lines.append("DIAM 382.75mm")
    lines.append("HEIG 26.95mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is U")
    lines.append("POS E 48441.51mm N 6842.31mm U 622.17mm")
    lines.append("DIAM 328.84mm")
    lines.append("HEIG 32.35mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is U")
    lines.append("POS E 48419.94mm N 6842.31mm U 622.17mm")
    lines.append("DIAM 231.81mm")
    lines.append("HEIG 10.78mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is U")
    lines.append("POS E 48406.47mm N 6845mm U 622.17mm")
    lines.append("DIAM 97.04mm")
    lines.append("HEIG 16.17mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is U")
    lines.append("POS E 48395.69mm N 6845mm U 622.17mm")
    lines.append("DIAM 53.91mm")
    lines.append("HEIG 5.39mm")
    lines.append("END")

    # Pulley Wheels at N 5987 and N 6845
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is N")
    lines.append("POS E 48325.5mm N 5987mm U 622.17mm")
    lines.append("DIAM 291mm")
    lines.append("HEIG 135mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is N")
    lines.append("POS E 48325.5mm N 6845mm U 622.17mm")
    lines.append("DIAM 291mm")
    lines.append("HEIG 135mm")
    lines.append("END")

    # Vacuum Degassing Pump Body & Adapter
    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is N")
    lines.append("POS E 48714mm N 5987mm U 622.17mm")
    lines.append("DIAM 221mm")
    lines.append("HEIG 16mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is N")
    lines.append("POS E 48196mm N 5987mm U 622.17mm")
    lines.append("DIAM 97mm")
    lines.append("HEIG 124mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is N")
    lines.append("POS E 48549.5mm N 5987mm U 622.17mm")
    lines.append("DIAM 151mm")
    lines.append("HEIG 313mm")
    lines.append("END")

    lines.append("NEW CYLINDER")
    lines.append("ORI Z is E and Y is N")
    lines.append("POS E 48875.5mm N 6003mm U 622.17mm")
    lines.append("DIAM 275mm")
    lines.append("HEIG 307mm")
    lines.append("END")

    lines.append("NEW CONE")
    lines.append("ORI Z is E and Y is N")
    lines.append("POS E 49042.5mm N 6003mm U 622.17mm")
    lines.append("DTOP 291mm")
    lines.append("DBOT 275mm")
    lines.append("HEIG 27mm")
    lines.append("END")

    # Auxiliary Degassing / Vacuum Exhaust Nozzle
    lines.append("NEW NOZZLE /205_PU_054_VACUUM_NOZZLE")
    lines.append("CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW")
    lines.append("POS E 49056mm N 6003mm U 622.17mm")
    lines.append("ORI P1 IS E")
    lines.append("HEIG 50mm")
    lines.append("TEMP 50degC")
    lines.append("PRES 100000pascal")
    lines.append("TPRESS 150000pascal")
    lines.append("DUTY 'DEGASSING'")
    lines.append("END")

    lines.append("END")
    lines.append("")

    # =========================================================================
    # 8. SUBEQUIPMENT /205_PU_054_SUCTION (Main Suction Nozzle)
    # =========================================================================
    lines.append("NEW SUBEQUIPMENT /205_PU_054_SUCTION")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")

    lines.append("NEW NOZZLE /205_PU_054_SUCTION_NOZZLE")
    lines.append("CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR")
    lines.append("POS E 48852mm N 5818mm U 622.17mm")
    lines.append("ORI P1 IS N")
    lines.append("HEIG 50mm")
    lines.append("TEMP 70degC")
    lines.append("PRES 1000000pascal")
    lines.append("TPRESS 1500000pascal")
    lines.append("DUTY 'SUCTION'")
    lines.append("END")

    lines.append("END")
    lines.append("")

    # =========================================================================
    # 9. SUBEQUIPMENT /205_PU_054_DISCHARGE (Main Discharge Nozzle)
    # =========================================================================
    lines.append("NEW SUBEQUIPMENT /205_PU_054_DISCHARGE")
    lines.append("BUIL false")
    lines.append("DSCO unset")
    lines.append("PTSP unset")
    lines.append("INSC unset")
    lines.append("")

    lines.append("NEW NOZZLE /205_PU_054_DISCHARGE_NOZZLE")
    lines.append("CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR")
    lines.append("POS E 48852mm N 5672mm U 1017.97mm")
    lines.append("ORI P1 IS U")
    lines.append("HEIG 68.3mm")
    lines.append("TEMP 70degC")
    lines.append("PRES 1000000pascal")
    lines.append("TPRESS 1500000pascal")
    lines.append("DUTY 'DISCHARGE'")
    lines.append("END")

    lines.append("END")
    lines.append("")

    # Close equipment & epilogue
    lines.append("INPUT END  EQUIPMENT /205_PU_054")
    lines.append("INPUT FINISH")
    lines.append("-- Switch synonyms back on if an error occurs.")
    lines.append("LABEL /ERROR3")
    lines.append("handle ANY")
    lines.append("$S+")
    lines.append("RETURN ERROR")
    lines.append("endhandle")
    lines.append("")
    lines.append("-- End Data Listing    Date : 31 Aug 2026")
    lines.append("$S+  -- Synonym translation ON")
    lines.append("-- ----------------------------------------------------------------")
    
    return "\n".join(lines)

if __name__ == "__main__":
    pml_text = build_sculpted_054_pml()
    out_dir = "Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "205_PU_054.pml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(pml_text)
    print(f"Generated {len(pml_text.splitlines())} lines to {out_path}")
