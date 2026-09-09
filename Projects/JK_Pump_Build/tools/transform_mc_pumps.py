# -*- coding: utf-8 -*-
"""
Robust, verified MC Pump transformer:
Replaces and generates modeling based on the UPDATED 2026-08-24 054 model for:
1. 203-PU-020 (replace existing with updated 054 model, 90 deg CCW, anchor 17095, 5685, 0)
2. 204-PU-028 (NEW MC pump added to Zone, 90 deg CW, nozzle towards E, anchor 22370, 6986, 0)
3. 205-PU-018 (replace existing with updated 054 model, 90 deg CCW, anchor 35727.6, 5019, 0)
4. 205-PU-038 (replace existing with updated 054 model, 90 deg CCW, anchor 43112.9, 5016, 0)
5. 205-PU-054 (update with latest 054 model)
All other 26 equipment items and zone structures are preserved untouched.
"""

import re
import os

def parse_coords(line):
    matches = re.findall(r'([EWNSUD])\s*([+-]?\d+(?:\.\d+)?)(?:mm)?', line)
    e = 0.0; n = 0.0; u = 0.0
    for dir_letter, val_str in matches:
        val = float(val_str)
        if dir_letter == 'E': e += val
        elif dir_letter == 'W': e -= val
        elif dir_letter == 'N': n += val
        elif dir_letter == 'S': n -= val
        elif dir_letter == 'U': u += val
        elif dir_letter == 'D': u -= val
    return e, n, u

def fmt_val(v):
    r = round(v, 2)
    if abs(r - round(r)) < 1e-5:
        return str(int(round(r)))
    return ('%.2f' % r).rstrip('0').rstrip('.')

def format_pos_world(e, n, u):
    e_str = ('E %smm' % fmt_val(e)) if e >= 0 else ('W %smm' % fmt_val(-e))
    n_str = ('N %smm' % fmt_val(n)) if n >= 0 else ('S %smm' % fmt_val(-n))
    u_str = ('U %smm' % fmt_val(u)) if u >= 0 else ('D %smm' % fmt_val(-u))
    return 'POS %s %s %s' % (e_str, n_str, u_str)

def rotate_single_direction(d_str, rotation='CCW'):
    tokens = d_str.strip().split()
    new_tokens = []
    for t in tokens:
        if rotation == 'CCW':
            # 90 deg CCW: E->N, N->W, W->S, S->E, U->U, D->D
            if t == 'E': new_tokens.append('N')
            elif t == 'W': new_tokens.append('S')
            elif t == 'N': new_tokens.append('W')
            elif t == 'S': new_tokens.append('E')
            elif t in ('U', 'D'): new_tokens.append(t)
            else: new_tokens.append(t)
        elif rotation == 'CW':
            # 90 deg CW: N->E, E->S, S->W, W->N, U->U, D->D
            if t == 'E': new_tokens.append('S')
            elif t == 'W': new_tokens.append('N')
            elif t == 'N': new_tokens.append('E')
            elif t == 'S': new_tokens.append('W')
            elif t in ('U', 'D'): new_tokens.append(t)
            else: new_tokens.append(t)
    return ' '.join(new_tokens)

def rotate_ori(ori_str, rotation='CCW'):
    m = re.match(r'^(ORI\s+)?(Y|Z|X)\s+is\s+(.*?)\s+and\s+(Y|Z|X)\s+is\s+(.*?)$', ori_str, re.IGNORECASE)
    if m:
        prefix = m.group(1) or ''
        ax1 = m.group(2)
        dir1 = rotate_single_direction(m.group(3), rotation)
        ax2 = m.group(4)
        dir2 = rotate_single_direction(m.group(5), rotation)
        return '%s%s is %s and %s is %s' % (prefix, ax1, dir1, ax2, dir2)
    
    m2 = re.match(r'^(ORI\s+)?(Y|Z|X)\s+is\s+(.*?)$', ori_str, re.IGNORECASE)
    if m2:
        prefix = m2.group(1) or ''
        ax1 = m2.group(2)
        dir1 = rotate_single_direction(m2.group(3), rotation)
        return '%s%s is %s' % (prefix, ax1, dir1)
    
    return ori_str

def transform_054_equipment(block_054, target_tag, target_desc, target_anchor, rotation='CCW'):
    e0_src = 48852.0
    n0_src = 4714.0
    u0_src = 0.0
    
    e0_tgt, n0_tgt, u0_tgt = target_anchor
    
    lines = block_054.splitlines()
    out_lines = []
    
    # Pre-scan primitives to know if each primitive block has an ORI line
    prim_has_ori = {}
    for idx, l in enumerate(lines):
        t = l.strip()
        if t.startswith('NEW ') and not t.startswith('NEW SUBEQUIPMENT') and not t.startswith('NEW EQUIPMENT') and not t.startswith('NEW LOOP') and not t.startswith('NEW VERTEX') and not t.startswith('NEW NXTRUSION') and not t.startswith('NEW AIDGROUP') and not t.startswith('NEW AIDLINE') and not t.startswith('NEW AIDPOINT'):
            has_o = False
            j = idx + 1
            while j < len(lines):
                jl = lines[j].strip()
                if jl.startswith('ORI '):
                    has_o = True
                if jl == 'END' or jl.startswith('NEW '):
                    break
                j += 1
            prim_has_ori[idx] = has_o

    current_sube_name = None
    sube_has_world_pos = False
    current_prim_idx = -1
    
    i = 0
    while i < len(lines):
        line = lines[i]
        trimmed = line.strip()
        
        # 1. Equipment header
        if trimmed.startswith('NEW EQUIPMENT'):
            out_lines.append('NEW EQUIPMENT ' + target_tag)
            i += 1
            continue
        if trimmed.startswith('DESC '):
            out_lines.append("DESC '%s'" % target_desc)
            i += 1
            continue
            
        # 2. Subequipment header
        if trimmed.startswith('NEW SUBEQUIPMENT'):
            sube_name = trimmed.split()[2]
            if sube_name == '/Copy-of-MOTOR_FRAME':
                new_sube_name = target_tag + '_MOTOR_FRAME'
            else:
                new_sube_name = sube_name.replace('/205_PU_054', target_tag)
            out_lines.append('NEW SUBEQUIPMENT ' + new_sube_name)
            current_sube_name = sube_name
            
            # Check next line for SUBE POS
            if i + 1 < len(lines) and lines[i+1].strip().startswith('POS '):
                pos_line = lines[i+1].strip()
                e_sub, n_sub, u_sub = parse_coords(pos_line)
                if current_sube_name in ('/Copy-of-MOTOR_FRAME', '/205_PU_054_AID_MOTOR_1'):
                    sube_has_world_pos = True
                    de = e_sub - e0_src
                    dn = n_sub - n0_src
                    du = u_sub - u0_src
                    if rotation == 'CCW':
                        de_tgt = -dn
                        dn_tgt = +de
                    else: # CW
                        de_tgt = +dn
                        dn_tgt = -de
                    du_tgt = +du
                    e_tgt = e0_tgt + de_tgt
                    n_tgt = n0_tgt + dn_tgt
                    u_tgt = u0_tgt + du_tgt
                    out_lines.append(format_pos_world(e_tgt, n_tgt, u_tgt))
                elif current_sube_name == '/205_PU_054_CASING':
                    sube_has_world_pos = False
                    if rotation == 'CCW':
                        dx_tgt = -n_sub
                        dy_tgt = +e_sub
                    else: # CW
                        dx_tgt = +n_sub
                        dy_tgt = -e_sub
                    dz_tgt = +u_sub
                    out_lines.append(format_pos_world(dx_tgt, dy_tgt, dz_tgt))
                else:
                    sube_has_world_pos = False
                    de = e_sub - e0_src
                    dn = n_sub - n0_src
                    du = u_sub - u0_src
                    if rotation == 'CCW':
                        de_tgt = -dn
                        dn_tgt = +de
                    else: # CW
                        de_tgt = +dn
                        dn_tgt = -de
                    e_tgt = e0_tgt + de_tgt
                    n_tgt = n0_tgt + dn_tgt
                    u_tgt = u0_tgt + du
                    out_lines.append(format_pos_world(e_tgt, n_tgt, u_tgt))
                i += 2
                continue
            else:
                sube_has_world_pos = False
                i += 1
                continue
                
        # 3. Nozzle header
        if trimmed.startswith('NEW NOZZLE'):
            current_prim_idx = i
            parts = trimmed.split()
            if len(parts) > 2:
                nozz_name = parts[2].replace('/205_PU_054', target_tag)
                out_lines.append('NEW NOZZLE ' + nozz_name)
            else:
                out_lines.append('NEW NOZZLE')
            i += 1
            continue
            
        # 4. Primitive / AID element header
        if trimmed.startswith('NEW ') and not trimmed.startswith('NEW SUBEQUIPMENT') and not trimmed.startswith('NEW EQUIPMENT') and not trimmed.startswith('NEW LOOP') and not trimmed.startswith('NEW VERTEX') and not trimmed.startswith('NEW NXTRUSION'):
            current_prim_idx = i
            out_lines.append(line)
            i += 1
            continue
            
        # 5. Handle POS line
        if trimmed.startswith('POS '):
            prev = lines[i-1].strip() if i > 0 else ''
            if prev == 'NEW VERTEX':
                # Extrusion profile vertex: preserve coordinate
                out_lines.append(line)
            elif sube_has_world_pos:
                dx, dy, dz = parse_coords(trimmed)
                if rotation == 'CCW':
                    dx_tgt = -dy
                    dy_tgt = +dx
                else: # CW
                    dx_tgt = +dy
                    dy_tgt = -dx
                dz_tgt = +dz
                out_lines.append(format_pos_world(dx_tgt, dy_tgt, dz_tgt))
                
                if current_prim_idx in prim_has_ori and not prim_has_ori[current_prim_idx]:
                    prim_type = lines[current_prim_idx].strip().split()[1]
                    if prim_type in ('BOX', 'PYRAMID', 'EXTRUSION'):
                        default_ori = 'ORI Y is W and Z is U' if rotation == 'CCW' else 'ORI Y is E and Z is U'
                        out_lines.append(default_ori)
            else:
                e, n, u = parse_coords(trimmed)
                de = e - e0_src
                dn = n - n0_src
                du = u - u0_src
                if rotation == 'CCW':
                    de_tgt = -dn
                    dn_tgt = +de
                else: # CW
                    de_tgt = +dn
                    dn_tgt = -de
                e_tgt = e0_tgt + de_tgt
                n_tgt = n0_tgt + dn_tgt
                u_tgt = u0_tgt + du
                out_lines.append(format_pos_world(e_tgt, n_tgt, u_tgt))
                
                if current_prim_idx in prim_has_ori and not prim_has_ori[current_prim_idx]:
                    prim_type = lines[current_prim_idx].strip().split()[1]
                    if prim_type in ('BOX', 'PYRAMID', 'EXTRUSION'):
                        default_ori = 'ORI Y is W and Z is U' if rotation == 'CCW' else 'ORI Y is E and Z is U'
                        out_lines.append(default_ori)
            i += 1
            continue
            
        # 6. Handle ORI line
        if trimmed.startswith('ORI '):
            out_lines.append(rotate_ori(trimmed, rotation))
            i += 1
            continue
            
        # Default pass-through
        out_lines.append(line)
        i += 1
        
    return '\n'.join(out_lines)

def process_zone_macro():
    in_zone_path = 'Projects/JK_Pump_Build/imports/2026-08-23_PUMP_native_zone.txt'
    with open(in_zone_path, 'r', encoding='utf-8') as f:
        input_text = f.read()

    in_054_path = 'Projects/JK_Pump_Build/imports/2026-08-24_205_PU_054_native_updated.txt'
    with open(in_054_path, 'r', encoding='utf-8') as f:
        text_054 = f.read()

    pos_054 = text_054.find('NEW EQUIPMENT /205_PU_054')
    end_054 = text_054.find('OLD NOZZLE', pos_054)
    if end_054 == -1: end_054 = text_054.find('INPUT END', pos_054)
    block_054 = text_054[pos_054:end_054].strip()
    
    targets = {
        '/203_PU_020': {
            'desc': '025024',
            'anchor': (17095.0, 5685.0, 0.0),
            'rotation': 'CCW'
        },
        '/204_PU_028': {
            'desc': 'POST OXYGEN WASHER DISCHARGE MC PUMP',
            'anchor': (22370.0, 6986.0, 0.0),
            'rotation': 'CW'
        },
        '/205_PU_018': {
            'desc': 'D0 STAGE MC PUMP',
            'anchor': (35727.6, 5019.0, 0.0),
            'rotation': 'CCW'
        },
        '/205_PU_038': {
            'desc': 'EOP STAGE MC PUMP',
            'anchor': (43112.9, 5016.0, 0.0),
            'rotation': 'CCW'
        },
        '/205_PU_054': {
            'desc': 'D1 STAGE MC PUMP',
            'anchor': (48852.0, 4714.0, 0.0),
            'rotation': 'NONE'
        }
    }
    
    replaced_blocks = {}
    for tag, cfg in targets.items():
        if cfg['rotation'] == 'NONE':
            replaced_blocks[tag] = block_054
        else:
            transformed = transform_054_equipment(block_054, tag, cfg['desc'], cfg['anchor'], cfg['rotation'])
            replaced_blocks[tag] = transformed
        
    eq_matches = list(re.finditer(r'NEW EQUIPMENT\s+(/\S+)', input_text))
    prologue = input_text[:eq_matches[0].start()]
    
    new_equi_sections = []
    for i, m in enumerate(eq_matches):
        tag = m.group(1)
        start = m.start()
        if i + 1 < len(eq_matches):
            end = eq_matches[i+1].start()
        else:
            m_old = re.search(r'\n(OLD NOZZLE|INPUT END)', input_text[start:])
            end = start + m_old.start() + 1 if m_old else len(input_text)
                
        original_block = input_text[start:end].strip()
        
        if tag in replaced_blocks:
            new_equi_sections.append(replaced_blocks[tag])
        else:
            new_equi_sections.append(original_block)
            
        # If this is 204_PU_023, insert 204_PU_028 right after it!
        if tag == '/204_PU_023' and '/204_PU_028' in replaced_blocks:
            new_equi_sections.append(replaced_blocks['/204_PU_028'])
            
    epilogue_start = input_text.find('OLD NOZZLE')
    if epilogue_start == -1:
        epilogue_start = input_text.find('INPUT END')
        
    epilogue = input_text[epilogue_start:]
    
    # Extract 054 OLD NOZZLE section from text_054
    pos_old_054 = text_054.find('OLD NOZZLE')
    end_old_054 = text_054.find('INPUT END', pos_old_054)
    old_nozz_054 = text_054[pos_old_054:end_old_054].strip()

    def gen_old_nozz(t_tag):
        return old_nozz_054.replace('/205_PU_054', t_tag)
        
    # Replace in epilogue for existing pumps
    epilogue = re.sub(
        r'OLD NOZZLE /203_PU_020_SUCTION_NOZZLE\s+CATR [^\n]+\s+OLD NOZZLE /203_PU_020_DISCHARGE_NOZZLE\s+CATR [^\n]+',
        gen_old_nozz('/203_PU_020'),
        epilogue
    )
    epilogue = re.sub(
        r'OLD NOZZLE /205_PU_018_SUCTION_NOZZLE\s+CATR [^\n]+\s+OLD NOZZLE /205_PU_018_DISCHARGE_NOZZLE\s+CATR [^\n]+',
        gen_old_nozz('/205_PU_018'),
        epilogue
    )
    epilogue = re.sub(
        r'OLD NOZZLE /205_PU_038_SUCTION_NOZZLE\s+CATR [^\n]+\s+OLD NOZZLE /205_PU_038_DISCHARGE_NOZZLE\s+CATR [^\n]+',
        gen_old_nozz('/205_PU_038'),
        epilogue
    )
    # Replace 205_PU_054 OLD NOZZLE section
    epilogue = re.sub(
        r'OLD NOZZLE /205_PU_054_NOZZLE_A\s+CATR [^\n]+\s+OLD NOZZLE /205_PU_054_SUCTION_NOZZLE\s+CATR [^\n]+\s+OLD NOZZLE 2 of SUBEQUIPMENT /205_PU_054_SUCTION\s+CATR [^\n]+\s+OLD NOZZLE /205_PU_054_DISCHARGE_NOZZLE\s+CATR [^\n]+',
        old_nozz_054,
        epilogue
    )
    
    # Insert 204_PU_028 OLD NOZZLE after 204_PU_023
    p23_match = re.search(r'(OLD NOZZLE /204_PU_023_DISCHARGE_NOZZLE\s+CATR [^\n]+)', epilogue)
    if p23_match:
        ins_pos = p23_match.end()
        epilogue = epilogue[:ins_pos] + '\n\n' + gen_old_nozz('/204_PU_028') + epilogue[ins_pos:]

    full_output = prologue + '\n'.join(new_equi_sections) + '\n' + epilogue
    
    out_dir = 'Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced'
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'JK_Pump_Build_all_pumps_20260823_mc_replaced.pml')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(full_output)
    print('Successfully generated updated transformed PML to:', out_file)
    return full_output

if __name__ == '__main__':
    process_zone_macro()
