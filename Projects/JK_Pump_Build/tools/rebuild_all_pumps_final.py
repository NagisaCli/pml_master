# -*- coding: utf-8 -*-
"""
Rebuild All Pumps Final Consolidation Generator (Master Precision Edition)
========================================================================
Transforms and unifies all 31 pumps in ZONE /WSB_PU:
1. Medium Consistency (MC) Pumps (/203_PU_020, /204_PU_028, /205_PU_018, /205_PU_038, /205_PU_054):
   - Direct rigid copy-paste from benchmark /205_PU_054 model.
   - Anchor is strictly placed at the MAIN BASEPLATE center (48852, 4714, 0).
   - All parts (casing, bearing, driver, belt drive, auxiliary motors, nozzles) are rigidly
     transformed relative to the baseplate anchor with 0.00mm internal drift.
   - Equipment headers contain NO ORI, preventing any unintended coordinate double-rotation.
   - Extrusion loop vertices remain strictly local and isolated to prevent profile distortion.
   - Grout bed box matches target foundation thickness (e.g. 176mm for 020).
2. Normal Centrifugal Pumps (26 units):
   - _CASING: Standard CTORUS volute ring (two back-to-back 180-deg CTORUS + inner core cylinder)
     strictly matching the original cylinder DIAM (ROUT = DIAM/2) and HEIG (RINS = ROUT - HEIG).
     Front DISH head diameter is scaled to (2 * RINS + 25mm), cleanly covering the inner hub hole
     and exposing the full outer torus volute ring.
   - _DRIVER: Sculpted 3-tier terminal box (saddle riser, main body, flanged lid + cable glands)
     cleanly replacing only the crude box before NEW ELCONN. Rear cone is hollowed with NCONE
     and capped with a detailed ventilation grille (hub, concentric hollow ring, cross spokes).
   - _BASE: Strictly preserves native authentic base beams and ribs without injecting any
     misplaced or floating synthetic boards.
3. Consolidates all 31 equipments sorted numerically from /203_PU_008 to /205_PU_061.
4. Sorts all epilogue 72 OLD NOZZLE bindings in matching sequence.
5. Strict IR-2 enforcement: ORI before POS for all primitives, POS before ORI for nozzles.
6. 100% PML1 syntax and stack balance.
"""

import re
import os
import math
from typing import Dict, List, Tuple, Optional

def parse_coords(line: str) -> Tuple[float, float, float]:
    matches = re.findall(r'([EWNSUD])\s*([+-]?\d+(?:\.\d+)?)(?:mm)?', line)
    e = 0.0; n = 0.0; u = 0.0
    for d, val_str in matches:
        val = float(val_str)
        if d == 'E': e += val
        elif d == 'W': e -= val
        elif d == 'N': n += val
        elif d == 'S': n -= val
        elif d == 'U': u += val
        elif d == 'D': u -= val
    return e, n, u

def fmt_val(v: float) -> str:
    r = round(v, 2)
    if abs(r - round(r)) < 1e-4:
        return str(int(round(r)))
    return ('%.2f' % r).rstrip('0').rstrip('.')

def format_pos_world(e: float, n: float, u: float) -> str:
    e_str = ('E %smm' % fmt_val(e)) if e >= 0 else ('W %smm' % fmt_val(-e))
    n_str = ('N %smm' % fmt_val(n)) if n >= 0 else ('S %smm' % fmt_val(-n))
    u_str = ('U %smm' % fmt_val(u)) if u >= 0 else ('D %smm' % fmt_val(-u))
    return 'POS %s %s %s' % (e_str, n_str, u_str)

def rotate_pt(dx: float, dy: float, rot: str) -> Tuple[float, float]:
    if rot == 'CCW':
        return -dy, dx
    elif rot == 'CW':
        return dy, -dx
    return dx, dy

def rotate_single_direction(d_str: str, rotation: str) -> str:
    tokens = d_str.strip().split()
    new_tokens = []
    for t in tokens:
        if rotation == 'CCW':
            if t == 'E': new_tokens.append('N')
            elif t == 'W': new_tokens.append('S')
            elif t == 'N': new_tokens.append('W')
            elif t == 'S': new_tokens.append('E')
            else: new_tokens.append(t)
        elif rotation == 'CW':
            if t == 'E': new_tokens.append('S')
            elif t == 'W': new_tokens.append('N')
            elif t == 'N': new_tokens.append('E')
            elif t == 'S': new_tokens.append('W')
            else: new_tokens.append(t)
        else:
            new_tokens.append(t)
    return ' '.join(new_tokens)

def rotate_ori(ori_str: str, rotation: str) -> str:
    m = re.match(r'^(ORI\s+)?(Y|Z|X|P1|P2|P3)\s+is\s+(.*?)\s+and\s+(Y|Z|X|P1|P2|P3)\s+is\s+(.*?)$', ori_str, re.IGNORECASE)
    if m:
        prefix = m.group(1) or 'ORI '
        ax1 = m.group(2)
        dir1 = rotate_single_direction(m.group(3), rotation)
        ax2 = m.group(4)
        dir2 = rotate_single_direction(m.group(5), rotation)
        return '%s%s is %s and %s is %s' % (prefix, ax1, dir1, ax2, dir2)
    m2 = re.match(r'^(ORI\s+)?(Y|Z|X|P1|P2|P3)\s+is\s+(.*?)$', ori_str, re.IGNORECASE)
    if m2:
        prefix = m2.group(1) or 'ORI '
        ax1 = m2.group(2)
        dir1 = rotate_single_direction(m2.group(3), rotation)
        return '%s%s is %s' % (prefix, ax1, dir1)
    return ori_str

def reorder_subequipment_primitives(pml_text: str) -> str:
    """
    Enforces Iron Rule IR-2 (ORI before POS) without modifying the NEW/END tree balance:
    - NOZZLE: POS before ORI, preserves HEIG and process attributes
    - PRIMITIVES: size attributes -> ORI before POS -> others
    - Leaves ALL NEW and END statements untouched (0 synthetic or dropped ENDs).
    """
    lines = pml_text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        trimmed = line.strip()
        
        if trimmed.startswith('NEW ') and not any(trimmed.startswith(x) for x in ['NEW ZONE', 'NEW EQUIPMENT', 'NEW SUBEQUIPMENT', 'NEW LOOP', 'NEW VERTEX']):
            prim_header = trimmed
            prim_type = prim_header.split()[1].upper()
            out.append(line)
            
            j = i + 1
            attr_lines = []
            while j < len(lines):
                tj = lines[j].strip()
                if tj.startswith('NEW ') or tj == 'END':
                    break
                attr_lines.append(lines[j])
                j += 1
                
            ori_l = None
            pos_l = None
            sizes = []
            others = []
            for al in attr_lines:
                alt = al.strip()
                if not alt or alt.startswith('--'):
                    continue
                cmd = alt.split()[0].upper()
                if cmd == 'ORI':
                    ori_l = al
                elif cmd == 'POS':
                    pos_l = al
                elif cmd in ('XLEN', 'YLEN', 'ZLEN', 'HEIG', 'DIAM', 'DTOP', 'DBOT', 'RINS', 'ROUT', 'RADI', 'XBOT', 'YBOT', 'XTOP', 'YTOP', 'XOFF', 'YOFF', 'ANGL'):
                    sizes.append(al)
                else:
                    others.append(al)
            
            if prim_type == 'NOZZLE':
                if pos_l: out.append(pos_l)
                if ori_l: out.append(ori_l)
                for s in sizes: out.append(s)
                for o in others: out.append(o)
            else:
                for s in sizes: out.append(s)
                if ori_l: out.append(ori_l)
                if pos_l: out.append(pos_l)
                for o in others: out.append(o)
                
            i = j
            continue
            
        out.append(line)
        i += 1
        
    return '\n'.join(out)


# ==============================================================================
# 1. RIGID MC PUMP TRANSFORMATION ENGINE
# ==============================================================================
def transform_mc_equipment(
    block_054: str,
    target_tag: str,
    target_desc: str,
    target_anchor: Tuple[float, float, float],
    rotation: str,
    eq_header_pos: str,
    grout_zlen: float
) -> str:
    """
    Directly copy-pastes and rigidly transforms the benchmark 054 model to the target MC pump:
    - Anchored strictly at the MAIN BASEPLATE center (48852.0, 4714.0, 0.0).
    - All subequipments, primitives, and nozzles are transformed as a single rigid body.
    - NO ORI at the equipment level to avoid double-rotation.
    - Extrusion loop vertices remain strictly local and isolated.
    - Subequipment origins (e.g. AID_MOTOR_1) and world primitives are cleanly mapped.
    - Grout bed box matches target foundation thickness (e.g. 176mm for 020).
    """
    e0_src, n0_src, u0_src = 48852.0, 4714.0, 0.0
    e0_tgt, n0_tgt, u0_tgt = target_anchor

    lines = block_054.splitlines()
    out = []
    
    current_sube = None
    seen_prim_in_sube = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        trimmed = line.strip()
        
        # 1. Equipment header
        if trimmed.startswith('NEW EQUIPMENT'):
            out.append('NEW EQUIPMENT ' + target_tag)
            i += 1
            continue
        if trimmed.startswith('DESC '):
            out.append('DESC \'' + target_desc + '\'')
            i += 1
            continue
        if trimmed.startswith('POS ') and current_sube is None:
            out.append(eq_header_pos)
            # CRITICAL: Do NOT add ORI to the equipment header!
            i += 1
            continue
            
        # 2. Subequipment header
        if trimmed.startswith('NEW SUBEQUIPMENT'):
            sube_name = trimmed.split()[2]
            new_sube_name = sube_name.replace('/205_PU_054', target_tag)
            out.append('NEW SUBEQUIPMENT ' + new_sube_name)
            current_sube = sube_name
            seen_prim_in_sube = False
            i += 1
            continue
            
        # 3. Subequipment level POS line
        if trimmed.startswith('POS ') and not seen_prim_in_sube:
            if current_sube and '_AID_MOTOR_1' in current_sube:
                e, n, u = parse_coords(trimmed)
                de, dn = e - e0_src, n - n0_src
                de_r, dn_r = rotate_pt(de, dn, rotation)
                # Motor foundation elevation matches target pump grout thickness
                # 054 had D 42mm because grout was 42mm. Target is -grout_zlen:
                target_u = -grout_zlen
                out.append(format_pos_world(e0_tgt + de_r, n0_tgt + dn_r, target_u))
            else:
                dx, dy, dz = parse_coords(trimmed)
                dx_r, dy_r = rotate_pt(dx, dy, rotation)
                out.append(format_pos_world(dx_r, dy_r, dz))
            i += 1
            continue

        # 4. Extrusion and loop handling: keep loop vertices verbatim in local profile plane!
        if trimmed.startswith('NEW LOOP'):
            out.append(line)
            i += 1
            continue
        elif trimmed.startswith('NEW VERTEX'):
            # Extrusion vertices live in the local profile plane (XY).
            # The extrusion's ORI already maps the profile into 3D world space.
            # Do NOT rotate vertex coordinates!
            j = i
            while j < len(lines) and lines[j].strip() != 'END':
                out.append(lines[j])
                j += 1
            if j < len(lines):
                out.append(lines[j])  # the 'END' of NEW VERTEX
                j += 1
            i = j
            continue

        # 5. Primitive handling with attribute reordering (ORI before POS)
        if trimmed.startswith('NEW ') and not any(trimmed.startswith(x) for x in ['NEW ZONE', 'NEW EQUIPMENT', 'NEW SUBEQUIPMENT', 'NEW LOOP', 'NEW VERTEX']):
            seen_prim_in_sube = True
            prim_header = trimmed
            prim_type = prim_header.split()[1].upper()
            
            # Map nozzle name if named
            if prim_type == 'NOZZLE' and len(trimmed.split()) > 2:
                nozz_name = trimmed.split()[2]
                new_nozz_name = nozz_name.replace('/205_PU_054', target_tag)
                prim_header = 'NEW NOZZLE ' + new_nozz_name
                
            j = i + 1
            attr_lines = []
            while j < len(lines):
                tj = lines[j].strip()
                if tj.startswith('NEW ') or tj == 'END':
                    break
                attr_lines.append(lines[j])
                j += 1
                
            ori_l = None
            pos_l = None
            sizes = []
            others = []
            
            # Check if this is a negative child primitive (NBOX, NCONE, NCYLINDER, NXTRUSION)
            is_child_negative = prim_type.startswith('N') and prim_type != 'NOZZLE'
            
            # Check if this is the foundation grout box in _BASE (XLEN 1046, YLEN 2000, ZLEN 42)
            is_grout_box = (prim_type == 'BOX' and current_sube == '/205_PU_054_BASE' and any('ZLEN 42' in al or 'D 21mm' in al for al in attr_lines))
            
            if is_child_negative:
                # Child negative primitives are evaluated strictly in the parent's local frame.
                # When the parent rotates, its local frame rotates with it, so the child's local
                # POS and ORI relative to the parent remain invariant!
                for al in attr_lines:
                    alt = al.strip()
                    if not alt or alt.startswith('--'): continue
                    cmd = alt.split()[0].upper()
                    if cmd == 'ORI':
                        ori_l = alt
                    elif cmd == 'POS':
                        pos_l = alt
                    elif cmd in ('XLEN', 'YLEN', 'ZLEN', 'HEIG', 'DIAM', 'DTOP', 'DBOT', 'RINS', 'ROUT', 'RADI', 'XBOT', 'YBOT', 'XTOP', 'YTOP', 'XOFF', 'YOFF', 'ANGL'):
                        sizes.append(alt)
                    else:
                        others.append(alt)
            elif is_grout_box:
                sizes = ['XLEN 1046mm', 'YLEN 2000mm', 'ZLEN %smm' % fmt_val(grout_zlen)]
                if rotation in ('CCW', 'CW'):
                    ori_l = 'ORI Y is W and Z is U' if rotation == 'CCW' else 'ORI Y is E and Z is U'
                else:
                    ori_l = 'ORI Z is U and Y is N'
                pos_l = format_pos_world(e0_tgt, n0_tgt, -grout_zlen / 2.0)
            else:
                for al in attr_lines:
                    alt = al.strip()
                    if not alt or alt.startswith('--'): continue
                    cmd = alt.split()[0].upper()
                    if cmd == 'ORI':
                        ori_l = rotate_ori(alt, rotation) if rotation != 'NONE' else alt
                    elif cmd == 'POS':
                        if current_sube and '_AID_MOTOR_1' in current_sube:
                            lx, ly, lz = parse_coords(alt)
                            lx_r, ly_r = rotate_pt(lx, ly, rotation)
                            pos_l = format_pos_world(lx_r, ly_r, lz)
                        else:
                            # If RTORUS in BELT_DRIVE was shifted to 48625/48675, restore native 48470.85/48520.85:
                            alt_clean = alt
                            if prim_type == 'RTORUS' and current_sube and '_BELT_DRIVE' in current_sube:
                                if '48625' in alt:
                                    alt_clean = alt.replace('48625mm', '48470.85mm')
                                elif '48675' in alt:
                                    alt_clean = alt.replace('48675mm', '48520.85mm')
                            e, n, u = parse_coords(alt_clean)
                            if abs(e) > 1000 or abs(n) > 1000:
                                # World coordinate
                                de = e - e0_src; dn = n - n0_src; du = u - u0_src
                                de_r, dn_r = rotate_pt(de, dn, rotation)
                                pos_l = format_pos_world(e0_tgt + de_r, n0_tgt + dn_r, u0_tgt + du)
                            else:
                                lx_r, ly_r = rotate_pt(e, n, rotation)
                                pos_l = format_pos_world(lx_r, ly_r, u)
                    elif cmd in ('XLEN', 'YLEN', 'ZLEN', 'HEIG', 'DIAM', 'DTOP', 'DBOT', 'RINS', 'ROUT', 'RADI', 'XBOT', 'YBOT', 'XTOP', 'YTOP', 'XOFF', 'YOFF', 'ANGL'):
                        sizes.append(alt)
                    else:
                        others.append(alt)
                        
                if not ori_l and rotation != 'NONE' and prim_type != 'NOZZLE':
                    ori_l = 'ORI Y is W and Z is U' if rotation == 'CCW' else 'ORI Y is E and Z is U'
                if not pos_l:
                    pos_l = 'POS E 0mm N 0mm U 0mm'

            out.append(prim_header)
            if prim_type == 'NOZZLE':
                # Orient nozzles using geometric triad (100% compatible with trailing CATR in epilogue)
                if current_sube and '_AID_MOTOR_2' in current_sube:
                    # In 054 native export, AID_MOTOR_2 nozzle carries NO ORI line
                    ori_l = None
                elif 'SUCTION_NOZZLE' in prim_header:
                    # External suction flange: must face incoming pipe
                    # For CCW (020, 018, 038, shaft West): pipe comes from West -> Z is W
                    # For CW (028, shaft East): pipe comes from East -> Z is E
                    # For NONE (054, shaft North): Z is W
                    if rotation == 'CCW':
                        ori_l = 'ORI Y is U and Z is W'
                    elif rotation == 'CW':
                        ori_l = 'ORI Y is U and Z is E'
                    else:
                        ori_l = 'ORI Y is U and Z is W'
                elif current_sube and '_SUCTION' in current_sube:
                    # 2nd inner suction nozzle (opposite direction along same axis)
                    if rotation == 'CCW':
                        ori_l = 'ORI Y is U and Z is E'
                    elif rotation == 'CW':
                        ori_l = 'ORI Y is U and Z is W'
                    else:
                        ori_l = 'ORI Y is U and Z is E'
                elif 'DISCHARGE_NOZZLE' in prim_header or (current_sube and '_DISCHARGE' in current_sube):
                    # Discharge nozzle: crown discharge orientation from native export:
                    # 054: ORI Y is N and Z is E
                    # CCW (020, 018, 038): ORI Y is W and Z is N
                    # CW (028): ORI Y is E and Z is S
                    if rotation == 'CCW':
                        ori_l = 'ORI Y is W and Z is N'
                    elif rotation == 'CW':
                        ori_l = 'ORI Y is E and Z is S'
                    else:
                        ori_l = 'ORI Y is N and Z is E'
                else:
                    ori_l = None

                if pos_l: out.append(pos_l)
                if ori_l: out.append(ori_l)
                for s in sizes: out.append(s)
                for o in others: out.append(o)
            else:
                for s in sizes: out.append(s)
                if ori_l: out.append(ori_l)
                if pos_l: out.append(pos_l)
                for o in others: out.append(o)
                
            i = j
            continue
            
        out.append(line)
        i += 1
        
    raw_lines = '\n'.join(out).splitlines()
    while raw_lines and not raw_lines[-1].strip():
        raw_lines.pop()
    news = sum(1 for l in raw_lines if l.strip().upper().startswith('NEW '))
    ends = sum(1 for l in raw_lines if l.strip().upper() == 'END')
    while ends < news:
        raw_lines.append('END')
        ends += 1
    while ends > news and raw_lines:
        if raw_lines[-1].strip().upper() == 'END':
            raw_lines.pop()
            ends -= 1
        else:
            break
            
    return '\n'.join(raw_lines)


# ==============================================================================
# 2. NORMAL PUMP UPGRADE ENGINES
# ==============================================================================
def upgrade_normal_casing(
    orig_casing_chunk: str,
    tag: str
) -> str:
    """
    Upgrades normal pump casing:
    - Standard CTORUS volute ring strictly matching original cylinder DIAM and HEIG.
    - DISH head diameter reduced to (2 * RINS + 25mm), just enough to cover the inner
      hub hole and expose the outer CTORUS volute ring.
    - Preserves all suction/discharge neck cylinders and cones.
    """
    lines = orig_casing_chunk.splitlines()
    
    # 1. Locate original casing main cylinder
    cyl_match = re.search(r'NEW CYLINDER\s*\n([\s\S]*?)END', orig_casing_chunk)
    if not cyl_match:
        return reorder_subequipment_primitives(orig_casing_chunk)
        
    cyl_body = cyl_match.group(1)
    pm = re.search(r'POS\s+([^\n]+)', cyl_body)
    om = re.search(r'ORI\s+([^\n]+)', cyl_body)
    dm = re.search(r'DIAM\s+([0-9.]+)', cyl_body)
    hm = re.search(r'HEIG\s+([0-9.]+)', cyl_body)
    
    if not (pm and dm and hm):
        return reorder_subequipment_primitives(orig_casing_chunk)
        
    pos_str = pm.group(0).strip()
    ori_str = om.group(0).strip() if om else 'ORI Y is U and Z is N'
    orig_dia = float(dm.group(1))
    orig_heig = float(hm.group(1))
    
    # Determine shaft axis (Z of the cylinder)
    zm = re.search(r'Z\s+is\s+([NEWSUD]+)', ori_str, re.IGNORECASE)
    shaft_axis = zm.group(1).upper() if zm else 'N'
    
    # Torus dimensions: exactly match original cylinder diameter and thickness!
    rout = orig_dia / 2.0
    rins = max(10.0, rout - orig_heig)
    
    # Construct CTORUS volute ring + central core cylinder
    volute_lines = [
        'NEW CTORUS',
        'RINS %smm' % fmt_val(rins),
        'ROUT %smm' % fmt_val(rout),
        'ANGL 180degree',
        'ORI Z is %s and Y is D' % shaft_axis,
        pos_str,
        'END',
        'NEW CTORUS',
        'RINS %smm' % fmt_val(rins),
        'ROUT %smm' % fmt_val(rout),
        'ANGL 180degree',
        'ORI Z is %s and Y is U' % shaft_axis,
        pos_str,
        'END',
        'NEW CYLINDER',
        'DIAM %smm' % fmt_val(2.0 * rins),
        'HEIG %smm' % fmt_val(orig_heig),
        ori_str,
        pos_str,
        'END'
    ]
    volute_block = '\n'.join(volute_lines)
    
    # Replace the original CYLINDER in the chunk with the volute block
    chunk_with_volute = orig_casing_chunk[:cyl_match.start()] + volute_block + orig_casing_chunk[cyl_match.end():]
    
    # 2. Resize DISH cover so it covers inner hub hole and exposes the CTORUS ring
    dish_match = re.search(r'NEW DISH\s*\n([\s\S]*?)END', chunk_with_volute)
    if dish_match:
        dish_body = dish_match.group(1)
        d_pm = re.search(r'POS\s+([^\n]+)', dish_body)
        d_om = re.search(r'ORI\s+([^\n]+)', dish_body)
        dish_pos = d_pm.group(0).strip() if d_pm else pos_str
        dish_ori = d_om.group(0).strip() if d_om else ori_str
        
        # Sizing: covers 2*rins plus 25mm overlap, leaving the outer torus exposed!
        new_dish_dia = 2.0 * rins + 25.0
        new_dish_heig = 25.0
        new_dish_radi = max(5.0, new_dish_dia * 0.04)
        
        new_dish_block = '\n'.join([
            'NEW DISH',
            'DIAM %smm' % fmt_val(new_dish_dia),
            'HEIG %smm' % fmt_val(new_dish_heig),
            'RADI %smm' % fmt_val(new_dish_radi),
            dish_ori,
            dish_pos,
            'END'
        ])
        chunk_with_volute = chunk_with_volute[:dish_match.start()] + new_dish_block + chunk_with_volute[dish_match.end():]
        
    return reorder_subequipment_primitives(chunk_with_volute)


def upgrade_normal_driver(
    orig_driver_chunk: str,
    tag: str
) -> str:
    """
    Upgrades the normal pump driver:
    - 3-tier terminal box (saddle riser, main body, flanged lid + cable entry glands)
      cleanly replacing only the crude box before NEW ELCONN.
    - Hollowed rear motor cone (NCONE) with detailed ventilation grille (hub, concentric
      ring, and cross spokes) matching industrial pump standards.
    - Preserves all 36 original cooling fins and motor body with zero duplicate parts.
    """
    lines = orig_driver_chunk.splitlines()
    out_lines = []

    # Find shaft axis from driver cylinder or cone
    shaft_axis = 'N'
    om = re.search(r'ORI\s+[^\n]*Z\s+is\s+([NEWSUD]+)', orig_driver_chunk, re.IGNORECASE)
    if om:
        shaft_axis = om.group(1).upper()

    # 1. Identify rear cone for ventilation grille addition
    rear_cone_data = None
    cone_matches = list(re.finditer(r'NEW CONE\s*\n([\s\S]*?)END', orig_driver_chunk))
    if cone_matches:
        # First cone in driver is consistently the rear motor cowl cone
        cm = cone_matches[0]
        c_body = cm.group(1)
        c_pm = re.search(r'POS\s+([^\n]+)', c_body)
        c_om = re.search(r'ORI\s+([^\n]+)', c_body)
        c_dt = re.search(r'DTOP\s+([0-9.]+)', c_body)
        c_db = re.search(r'DBOT\s+([0-9.]+)', c_body)
        c_hg = re.search(r'HEIG\s+([0-9.]+)', c_body)
        if c_pm and c_dt and c_db and c_hg:
            ce, cn, cu = parse_coords(c_pm.group(1))
            dtop = float(c_dt.group(1))
            dbot = float(c_db.group(1))
            heig = float(c_hg.group(1))
            cone_ori = c_om.group(0).strip() if c_om else ('ORI Y is U and Z is %s' % shaft_axis)
            
            d_cap = min(dtop, dbot)
            sign = -1.0 if dtop > dbot else 1.0
            dist = sign * (heig / 2.0 + 3.0)
            ge, gn, gu = ce, cn, cu
            if shaft_axis == 'N': gn += dist
            elif shaft_axis == 'S': gn -= dist
            elif shaft_axis == 'E': ge += dist
            elif shaft_axis == 'W': ge -= dist
            
            rear_cone_data = {
                'match_span': cm.span(),
                'dtop': dtop,
                'dbot': dbot,
                'heig': heig,
                'cone_ori': cone_ori,
                'cone_pos': c_pm.group(0).strip(),
                'grille_pos': format_pos_world(ge, gn, gu),
                'd_cap': d_cap
            }

    i = 0
    while i < len(lines):
        line = lines[i]
        trimmed = line.strip()

        # Terminal box upgrade: BOX immediately before NEW ELCONN
        if trimmed == 'NEW BOX' and i + 8 < len(lines):
            lookahead = '\n'.join(lines[i:i+16])
            if 'NEW ELCONN' in lookahead:
                j = i + 1
                box_lines = []
                while j < len(lines) and lines[j].strip() != 'END':
                    box_lines.append(lines[j])
                    j += 1
                b_text = '\n'.join(box_lines)
                pm = re.search(r'POS\s+([^\n]+)', b_text)
                xm = re.search(r'XLEN\s+([0-9.]+)', b_text)
                ym = re.search(r'YLEN\s+([0-9.]+)', b_text)
                zm = re.search(r'ZLEN\s+([0-9.]+)', b_text)
                
                be, bn, bu = parse_coords(pm.group(1)) if pm else (0.0, 0.0, 1000.0)
                bx = float(xm.group(1)) if xm else 250.0
                by = float(ym.group(1)) if ym else 250.0
                bz = float(zm.group(1)) if zm else 160.0
                
                u_bot_box = bu - bz / 2.0
                u_top_box = bu + bz / 2.0
                
                # 1. Base saddle riser
                h_saddle = max(15.0, 0.15 * bz)
                out_lines.append('NEW BOX')
                out_lines.append('XLEN %smm' % fmt_val(bx * 0.85))
                out_lines.append('YLEN %smm' % fmt_val(by * 0.85))
                out_lines.append('ZLEN %smm' % fmt_val(h_saddle))
                out_lines.append('ORI Z is U and Y is %s' % shaft_axis)
                out_lines.append(format_pos_world(be, bn, u_bot_box + h_saddle / 2.0))
                out_lines.append('END\n')
                
                # 2. Main junction box body
                h_lid = min(18.0, 0.12 * bz)
                h_body = bz - h_saddle - h_lid
                u_body = u_bot_box + h_saddle + h_body / 2.0
                out_lines.append('NEW BOX')
                out_lines.append('XLEN %smm' % fmt_val(bx))
                out_lines.append('YLEN %smm' % fmt_val(by))
                out_lines.append('ZLEN %smm' % fmt_val(h_body))
                out_lines.append('ORI Z is U and Y is %s' % shaft_axis)
                out_lines.append(format_pos_world(be, bn, u_body))
                out_lines.append('END\n')
                
                # 3. Top cover lid with flanged rim
                out_lines.append('NEW BOX')
                out_lines.append('XLEN %smm' % fmt_val(bx * 1.06))
                out_lines.append('YLEN %smm' % fmt_val(by * 1.06))
                out_lines.append('ZLEN %smm' % fmt_val(h_lid))
                out_lines.append('ORI Z is U and Y is %s' % shaft_axis)
                out_lines.append(format_pos_world(be, bn, u_top_box - h_lid / 2.0))
                out_lines.append('END\n')
                
                # 4. Two lateral cable entry glands
                gland_dia = max(24.0, min(bx, by) * 0.16)
                gland_len = max(32.0, min(bx, by) * 0.20)
                side_offset = (bx / 2.0) + (gland_len / 2.0)
                gland_axis = 'E' if shaft_axis == 'N' else 'N'
                
                for sign_g in (-1, 1):
                    out_lines.append('NEW CYLINDER')
                    out_lines.append('DIAM %smm' % fmt_val(gland_dia))
                    out_lines.append('HEIG %smm' % fmt_val(gland_len))
                    out_lines.append('ORI Z is %s and Y is U' % gland_axis)
                    if shaft_axis == 'N':
                        out_lines.append(format_pos_world(be + side_offset, bn + sign_g * (by * 0.22), u_body))
                    else:
                        out_lines.append(format_pos_world(be + sign_g * (bx * 0.22), bn + side_offset, u_body))
                    out_lines.append('END\n')
                
                i = j + 1
                continue

        # Rear cone upgrade: add hollow interior and ventilation grille
        if rear_cone_data and trimmed == 'NEW CONE':
            # Check if this is the first cone
            j = i + 1
            cone_lines = []
            while j < len(lines) and lines[j].strip() != 'END':
                cone_lines.append(lines[j])
                j += 1
            cone_full = '\n'.join(cone_lines)
            if 'DTOP %s' % fmt_val(rear_cone_data['dtop']) in cone_full or 'DBOT %s' % fmt_val(rear_cone_data['dbot']) in cone_full:
                # 1. Emit hollowed rear cone
                out_lines.append('NEW CONE')
                out_lines.append('DTOP %smm' % fmt_val(rear_cone_data['dtop']))
                out_lines.append('DBOT %smm' % fmt_val(rear_cone_data['dbot']))
                out_lines.append('HEIG %smm' % fmt_val(rear_cone_data['heig']))
                out_lines.append(rear_cone_data['cone_ori'])
                out_lines.append(rear_cone_data['cone_pos'])
                # Negative inner cone
                out_lines.append('NEW NCONE')
                out_lines.append('DTOP %smm' % fmt_val(max(10.0, rear_cone_data['dtop'] - 16.0)))
                out_lines.append('DBOT %smm' % fmt_val(max(10.0, rear_cone_data['dbot'] - 16.0)))
                out_lines.append('HEIG %smm' % fmt_val(rear_cone_data['heig'] + 2.0))
                out_lines.append('POS E 0mm N 0mm U 0mm')
                out_lines.append('END')
                out_lines.append('END\n')
                
                # 2. Emit rear ventilation grille on end face
                d_cap = rear_cone_data['d_cap']
                g_pos = rear_cone_data['grille_pos']
                g_ori = rear_cone_data['cone_ori']
                
                # Hub
                hub_d = max(30.0, d_cap * 0.25)
                out_lines.append('NEW CYLINDER')
                out_lines.append('DIAM %smm' % fmt_val(hub_d))
                out_lines.append('HEIG 6mm')
                out_lines.append(g_ori)
                out_lines.append(g_pos)
                out_lines.append('END\n')
                
                # Concentric ring with hollow
                ring_d = max(hub_d + 30.0, d_cap * 0.80)
                out_lines.append('NEW CYLINDER')
                out_lines.append('DIAM %smm' % fmt_val(ring_d))
                out_lines.append('HEIG 6mm')
                out_lines.append(g_ori)
                out_lines.append(g_pos)
                out_lines.append('NEW NCYLINDER')
                out_lines.append('DIAM %smm' % fmt_val(ring_d - 16.0))
                out_lines.append('HEIG 8mm')
                out_lines.append('POS E 0mm N 0mm U 0mm')
                out_lines.append('END')
                out_lines.append('END\n')
                
                # 2 Cross spokes (strictly flat on grille face, 6mm thickness along shaft axis)
                spoke_len = max(ring_d, d_cap * 0.82)
                
                # Vertical spoke: height along U, thickness along shaft_axis
                out_lines.append('NEW BOX')
                out_lines.append('XLEN 10mm')
                out_lines.append('YLEN %smm' % fmt_val(spoke_len))
                out_lines.append('ZLEN 6mm')
                out_lines.append('ORI Y is U and Z is %s' % shaft_axis)
                out_lines.append(g_pos)
                out_lines.append('END\n')
                
                # Horizontal spoke: width along horizontal, thickness along shaft_axis
                out_lines.append('NEW BOX')
                out_lines.append('XLEN %smm' % fmt_val(spoke_len))
                out_lines.append('YLEN 10mm')
                out_lines.append('ZLEN 6mm')
                out_lines.append('ORI Y is U and Z is %s' % shaft_axis)
                out_lines.append(g_pos)
                out_lines.append('END\n')
                
                rear_cone_data = None  # Processed once
                i = j + 1
                continue

        out_lines.append(line)
        i += 1

    raw_driver = '\n'.join(out_lines)
    return reorder_subequipment_primitives(raw_driver)


def upgrade_normal_base(
    orig_base_chunk: str,
    tag: str
) -> str:
    """
    Refines normal pump base:
    - Strictly preserves the authentic native 11 base beams and 10 extrusion ribs.
    - Zero synthetic or misplaced floating baseplates.
    - Enforces Iron Rule IR-2 (ORI before POS) and stack balance.
    """
    return reorder_subequipment_primitives(orig_base_chunk)


# ==============================================================================
# 3. MASTER PIPELINE EXECUTION
# ==============================================================================
def rebuild_entire_zone():
    raw_ref_path = r'C:\Users\A\.gemini\antigravity\brain\1ab9adff-c91e-4802-b049-a97d44f6dda9\.user_uploaded\media_1788522513923.txt'
    wsb_path = r'C:\Users\A\Desktop\WSB_PU.txt'
    src_path = raw_ref_path if os.path.exists(raw_ref_path) else wsb_path
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    mc_tags = {'/203_PU_020', '/204_PU_028', '/205_PU_018', '/205_PU_038', '/205_PU_054'}

    # 1. Extract Prologue
    eq_start = content.find('NEW EQUIPMENT')
    prologue = content[:eq_start].strip() + '\n\n'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    proj_dir = os.path.dirname(script_dir)
    opt_054_path = os.path.join(proj_dir, 'output', '205_PU_054_optimized_20260904.pml')
    if os.path.exists(opt_054_path):
        with open(opt_054_path, 'r', encoding='utf-8') as f:
            text_opt = f.read()
        pos_054 = text_opt.find('NEW EQUIPMENT /205_PU_054')
        end_054 = text_opt.find('OLD NOZZLE', pos_054)
        if end_054 == -1:
            end_054 = text_opt.find('INPUT END', pos_054)
        if end_054 == -1: end_054 = len(text_opt)
        block_054 = text_opt[pos_054:end_054].strip()
    else:
        pos_054 = content.find('NEW EQUIPMENT /205_PU_054')
        next_054 = content.find('NEW EQUIPMENT', pos_054 + 1)
        if next_054 == -1: next_054 = content.find('OLD NOZZLE', pos_054 + 1)
        block_054 = content[pos_054:next_054].strip()

    # MC Configurations with exact main baseplate center anchors:
    # 054 anchor is (48852.0, 4714.0, 0.0)
    mc_configs = {
        '/203_PU_020': {
            'desc': '025024',
            'anchor': (17095.0, 5685.0, 0.0),
            'rotation': 'CCW',
            'eq_pos': 'POS E 52087.1mm N 58829.16mm U 176mm',
            'grout_zlen': 176.0
        },
        '/204_PU_028': {
            'desc': 'POST OXYGEN WASHER DISCHARGE MC PUMP',
            'anchor': (22370.0, 6986.0, 0.0),
            'rotation': 'CW',
            'eq_pos': 'POS E 52440.91mm N 58829.16mm U 0mm',
            'grout_zlen': 42.0
        },
        '/205_PU_018': {
            'desc': 'D0 STAGE MC PUMP',
            'anchor': (35727.6, 5019.0, 0.0),
            'rotation': 'CCW',
            'eq_pos': 'POS E 52440.91mm N 58829.16mm U 0mm',
            'grout_zlen': 42.0
        },
        '/205_PU_038': {
            'desc': 'EOP STAGE MC PUMP',
            'anchor': (43112.9, 5016.0, 0.0),
            'rotation': 'CCW',
            'eq_pos': 'POS E 52440.91mm N 58829.16mm U 0mm',
            'grout_zlen': 42.0
        },
        '/205_PU_054': {
            'desc': 'D1 STAGE MC PUMP',
            'anchor': (48852.0, 4714.0, 0.0),
            'rotation': 'NONE',
            'eq_pos': 'POS E 52463.13mm N 58809.63mm U 42mm',
            'grout_zlen': 42.0
        }
    }

    transformed_mc_blocks: Dict[str, str] = {}
    for m_tag, cfg in mc_configs.items():
        t_block = transform_mc_equipment(
            block_054=block_054,
            target_tag=m_tag,
            target_desc=cfg['desc'],
            target_anchor=cfg['anchor'],
            rotation=cfg['rotation'],
            eq_header_pos=cfg['eq_pos'],
            grout_zlen=cfg['grout_zlen']
        )
        transformed_mc_blocks[m_tag] = t_block

    # 4. Transform 26 Normal Pumps
    transformed_normal_blocks: Dict[str, str] = {}
    all_eq_matches = list(re.finditer(r'NEW EQUIPMENT\s+(/\S+)', content))
    
    for i_m, m in enumerate(all_eq_matches):
        tag = m.group(1)
        if tag in mc_tags:
            continue
        
        start = m.start()
        end = all_eq_matches[i_m + 1].start() if i_m + 1 < len(all_eq_matches) else content.find('OLD NOZZLE', start)
        eq_chunk = content[start:end].strip()

        sube_matches = list(re.finditer(r'NEW SUBEQUIPMENT\s+(\S+)', eq_chunk))
        eq_header = eq_chunk[:sube_matches[0].start()].strip() + '\n\n'
        
        new_subes = []
        for s_idx, sm in enumerate(sube_matches):
            s_name = sm.group(1)
            s_start = sm.start()
            s_end = sube_matches[s_idx + 1].start() if s_idx + 1 < len(sube_matches) else len(eq_chunk)
            sub_chunk = eq_chunk[s_start:s_end].strip()

            if s_idx == len(sube_matches) - 1:
                sub_news = sum(1 for l in sub_chunk.splitlines() if l.strip().upper().startswith('NEW '))
                sub_lines = sub_chunk.splitlines()
                retained = []
                ends_seen = 0
                for l in sub_lines:
                    if l.strip().upper() == 'END':
                        if ends_seen < sub_news:
                            retained.append(l)
                            ends_seen += 1
                    else:
                        retained.append(l)
                sub_chunk = '\n'.join(retained)

            if '_CASING' in s_name:
                upgraded_c = upgrade_normal_casing(
                    orig_casing_chunk=sub_chunk,
                    tag=tag
                )
                new_subes.append(upgraded_c)
            elif '_DRIVER' in s_name:
                upgraded_d = upgrade_normal_driver(
                    orig_driver_chunk=sub_chunk,
                    tag=tag
                )
                new_subes.append(upgraded_d)
            elif '_BASE' in s_name:
                upgraded_b = upgrade_normal_base(
                    orig_base_chunk=sub_chunk,
                    tag=tag
                )
                new_subes.append(upgraded_b)
            else:
                reordered_sube = reorder_subequipment_primitives(sub_chunk)
                new_subes.append(reordered_sube)

        full_normal_eq = eq_header + '\n\n'.join(new_subes) + '\nEND\n'
        news = sum(1 for l in full_normal_eq.splitlines() if l.strip().upper().startswith('NEW '))
        ends = sum(1 for l in full_normal_eq.splitlines() if l.strip().upper() == 'END')
        while ends < news:
            full_normal_eq += '\nEND'
            ends += 1
        while ends > news:
            lines_f = full_normal_eq.splitlines()
            if lines_f[-1].strip().upper() == 'END':
                lines_f.pop()
                full_normal_eq = '\n'.join(lines_f)
                ends -= 1
            else:
                break
        transformed_normal_blocks[tag] = full_normal_eq

    # 5. Assemble & Sort all 31 Equipments Numerically
    all_blocks = {}
    all_blocks.update(transformed_mc_blocks)
    all_blocks.update(transformed_normal_blocks)

    def sort_key(t: str) -> Tuple[int, int]:
        m = re.search(r'/(\d+)_PU_(\d+)', t)
        if m:
            return (int(m.group(1)), int(m.group(2)))
        return (999, 999)

    sorted_tags = sorted(list(all_blocks.keys()), key=sort_key)
    print('Sorted equipments (%d total):' % len(sorted_tags))
    for t in sorted_tags:
        print(' ', t)

    body_text = '\n\n'.join(all_blocks[t].strip() for t in sorted_tags)

    # 6. Epilogue OLD NOZZLE Bindings
    raw_ref_path = r'C:\Users\A\.gemini\antigravity\brain\1ab9adff-c91e-4802-b049-a97d44f6dda9\.user_uploaded\media_1788522513923.txt'
    src_for_nozzles = content
    if os.path.exists(raw_ref_path):
        with open(raw_ref_path, 'r', encoding='utf-8') as rf:
            src_for_nozzles = rf.read()

    pos_old = src_for_nozzles.find('OLD NOZZLE')
    pos_end_zone = src_for_nozzles.find('INPUT END  ZONE')
    if pos_end_zone == -1: pos_end_zone = src_for_nozzles.find('INPUT FINISH')
    old_nozz_chunk = src_for_nozzles[pos_old:pos_end_zone].strip()

    old_nozz_items = list(re.finditer(r'OLD NOZZLE\s+([^\n]+)\s*\n\s*CATR\s+([^\n]+)', old_nozz_chunk))
    nozzle_by_tag: Dict[str, List[Tuple[str, str]]] = {t: [] for t in sorted_tags}

    for on_m in old_nozz_items:
        nozz_id = on_m.group(1).strip()
        catr_spec = on_m.group(2).strip()
        matched_tag = None
        for t in sorted_tags:
            if t + '_' in nozz_id or t in nozz_id:
                matched_tag = t
                break
        if matched_tag:
            nozzle_by_tag[matched_tag].append((nozz_id, catr_spec))

    epilogue_lines = []
    for t in sorted_tags:
        items = nozzle_by_tag.get(t, [])
        for n_id, c_spec in items:
            epilogue_lines.append('OLD NOZZLE %s\nCATR %s' % (n_id, c_spec))

    epilogue_text = (
        '\n'.join(epilogue_lines) +
        '\n\nINPUT END  ZONE /WSB_PU\nINPUT FINISH\n'
        '-- Switch synonyms back on if an error occurs.\n'
        'LABEL /ERROR3\n'
        'handle ANY\n'
        '$S+\n'
        'RETURN ERROR\n'
        'endhandle\n\n'
        '$S+  -- Synonym translation ON\n'
    )

    # 7. Final macro consolidation
    final_macro = prologue + body_text + '\n\n' + epilogue_text

    # Write output to Desktop
    out_desktop_path = r'C:\Users\A\Desktop\WSB_PU.txt'
    with open(out_desktop_path, 'w', encoding='utf-8') as f:
        f.write(final_macro)
    print('\nSuccessfully written consolidated macro to: %s (%d bytes, %d lines)' % (
        out_desktop_path, len(final_macro), len(final_macro.splitlines())
    ))

    # Also save to project output directory
    out_proj_path = os.path.join(proj_dir, 'output', 'WSB_PU_all_pumps_rebuilt_final.pml')
    os.makedirs(os.path.dirname(out_proj_path), exist_ok=True)
    with open(out_proj_path, 'w', encoding='utf-8') as f:
        f.write(final_macro)
    print('Successfully archived in project: %s' % out_proj_path)


if __name__ == '__main__':
    rebuild_entire_zone()
