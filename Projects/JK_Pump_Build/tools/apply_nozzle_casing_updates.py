"""
Apply nozzle casing updates to WSB_PU pumps:
1. Preserve the 5 MC pumps untouched.
2. For all 26 conventional pumps: extend suction nozzle length (HEIG) to casing center.
3. For the 13 overwidth conventional pumps (discharge nozzle DN > casing thickness):
   add 60° CTORUS transition bend and smooth CONE reducer, and adjust discharge nozzle
   flange elevation and length (HEIG 70mm) for a realistic, seamless connection.
"""

import re
import math
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from wsb.pml_builder import NOZZLE_BORE_COMPONENTS

INV_BORE = {v.rsplit('/', 1)[-1]: int(dn) for dn, v in NOZZLE_BORE_COMPONENTS.items()}

MC_TAGS = {
    '203_PU_020', '204_PU_028', '205_PU_018', '205_PU_038', '205_PU_054'
}

OVERWIDTH_TAGS = [
    '203_PU_011', '203_PU_026', '203_PU_031', '204_PU_006', '204_PU_008',
    '204_PU_017', '204_PU_023', '205_PU_013', '205_PU_024', '205_PU_032',
    '205_PU_049', '205_PU_060', '205_PU_061'
]

def fmt_mm(val: float) -> str:
    val = round(val, 2)
    if abs(val - round(val)) < 0.005:
        return f"{int(round(val))}mm"
    # eliminate trailing zero in decimals if clean (e.g. 15.5mm instead of 15.50mm)
    s = f"{val:.2f}"
    if s.endswith('0'):
        s = s[:-1]
    return f"{s}mm"

def fmt_coord(e: float, n: float, u: float) -> str:
    e_str = f"E {fmt_mm(e)}" if e >= -0.001 else f"W {fmt_mm(-e)}"
    n_str = f"N {fmt_mm(n)}" if n >= -0.001 else f"S {fmt_mm(-n)}"
    u_str = f"U {fmt_mm(u)}" if u >= -0.001 else f"D {fmt_mm(-u)}"
    return f"{e_str} {n_str} {u_str}"

def parse_pos(s: str) -> dict[str, float]:
    res = {'E': 0.0, 'N': 0.0, 'U': 0.0}
    if not s:
        return res
    for m in re.finditer(r'([ENSWUD])\s+(-?[\d.]+)mm', s):
        axis, val = m.group(1), float(m.group(2))
        if axis == 'W': res['E'] = -val
        elif axis == 'E': res['E'] = val
        elif axis == 'S': res['N'] = -val
        elif axis == 'N': res['N'] = val
        elif axis == 'D': res['U'] = -val
        elif axis == 'U': res['U'] = val
    return res

def process_equipment(eq_text: str, tag: str, catrs: dict[str, str]) -> str:
    if tag in MC_TAGS:
        return eq_text

    # 1. Update Suction Nozzle HEIG
    # Find casing center
    casing_sube = re.search(r'NEW SUBEQUIPMENT /' + tag + r'_CASING\s*(POS [^\n]+)?', eq_text)
    casing_sube_p = parse_pos(casing_sube.group(1)) if casing_sube and casing_sube.group(1) else {'E': 0.0, 'N': 0.0, 'U': 0.0}
    
    casing_m = re.search(r'NEW SUBEQUIPMENT /' + tag + r'_CASING(.*?)(?=NEW SUBEQUIPMENT|\Z)', eq_text, re.DOTALL)
    casing_body = casing_m.group(1) if casing_m else ''
    cyl_m = re.search(r'NEW CYLINDER\s+POS ([^\n]+)\s+ORI ([^\n]+)\s+DIAM ([\d.]+)mm\s+HEIG ([\d.]+)mm', casing_body)
    cp_local = parse_pos(cyl_m.group(1))
    cp_world = {k: cp_local[k] + casing_sube_p[k] for k in ('E', 'N', 'U')}
    
    c_thick = float(cyl_m.group(4))
    c_axis = cyl_m.group(2)
    shaft = 'E' if 'Z is E' in c_axis else 'N'
    
    ctorus_m = re.search(r'NEW CTORUS\s+POS [^\n]+\s+ORI [^\n]+\s+RINS ([\d.]+)mm\s+ROUT ([\d.]+)mm', casing_body)
    rins = float(ctorus_m.group(1))
    rout = float(ctorus_m.group(2))
    r1 = (rins + rout) / 2.0
    tube_d = rout - rins
    
    # Suction nozzle
    suct_sube = re.search(r'NEW SUBEQUIPMENT /' + tag + r'_SUCTION\s*(POS [^\n]+)?', eq_text)
    suct_sube_p = parse_pos(suct_sube.group(1)) if suct_sube and suct_sube.group(1) else {'E': 0.0, 'N': 0.0, 'U': 0.0}
    
    suct_m = re.search(r'NEW NOZZLE /' + tag + r'_SUCTION_NOZZLE\s+POS ([^\n]+)\s+ORI ([^\n]+)\s+.*?HEIG ([\d.]+)mm', eq_text, re.DOTALL)
    sp_local = parse_pos(suct_m.group(1))
    sp_world = {k: sp_local[k] + suct_sube_p[k] for k in ('E', 'N', 'U')}
    
    de = sp_world['E'] - cp_world['E']
    dn = sp_world['N'] - cp_world['N']
    du = sp_world['U'] - cp_world['U']
    suct_dist = (de**2 + dn**2 + du**2)**0.5
    new_suct_heig = round(suct_dist, 2)
    
    # Replace suction nozzle HEIG in eq_text
    def replace_suct_heig(m):
        full = m.group(0)
        return re.sub(r'HEIG [\d.]+mm', f'HEIG {fmt_mm(new_suct_heig)}', full)

    eq_text = re.sub(r'NEW NOZZLE /' + tag + r'_SUCTION_NOZZLE\s+POS [^\n]+\s+ORI [^\n]+\s+.*?HEIG [\d.]+mm',
                     replace_suct_heig, eq_text, count=1, flags=re.DOTALL)

    # 2. Check if overwidth
    disc_catr = catrs.get(f'{tag}_DISCHARGE_NOZZLE', '').rsplit('/', 1)[-1]
    d_dn = INV_BORE.get(disc_catr, 150)
    
    if tag in OVERWIDTH_TAGS:
        # We need to update CASING (remove old cylinder/cone, insert 60° CTORUS + CONE)
        # and update DISCHARGE nozzle (POS U and HEIG)
        e0, n0, u0 = cp_world['E'], cp_world['N'], cp_world['U']
        u_exit = u0 + math.sqrt(3) * r1
        
        if shaft == 'N':
            ctor_pos_str = fmt_coord(e0 - r1, n0, u_exit)
            ctor_ori = "ORI Y is D and Z is N"
            cone_ori_y = "N"
        else: # shaft == 'E'
            ctor_pos_str = fmt_coord(e0, n0 + r1, u_exit)
            ctor_ori = "ORI Y is D and Z is E"
            cone_ori_y = "E"
            
        h_cone = 35.0
        cone_pos_str = fmt_coord(e0, n0, u_exit + h_cone / 2.0)
        dtop = float(d_dn) # 150mm
        dbot = tube_d     # matches CTORUS tube diameter!
        
        h_nozz = 70.0
        nozz_flg_u = u_exit + h_cone + h_nozz
        nozz_pos_str = fmt_coord(e0, n0, nozz_flg_u)
        
        # In casing: remove old vertical cylinder and cone at the end
        # Find the casing block
        # Pattern matching the old cylinder + cone:
        # NEW CYLINDER\nPOS ...\nDIAM ...\nHEIG 28mm\n\nEND\nNEW CONE\nPOS ...\nDTOP ...\nDBOT ...\nHEIG 12mm\n\nEND
        old_conn_pat = re.compile(
            r'NEW CYLINDER\s+POS [^\n]+\s+DIAM [\d.]+mm\s+HEIG 28mm\s*\n\s*END\s*\n\s*NEW CONE\s+POS [^\n]+\s+DTOP [\d.]+mm\s+DBOT [\d.]+mm\s+HEIG 12mm\s*\n\s*END',
            re.DOTALL
        )
        
        new_casing_additions = (
            f"NEW CTORUS\n"
            f"POS {ctor_pos_str}\n"
            f"{ctor_ori}\n"
            f"RINS {fmt_mm(rins)}\n"
            f"ROUT {fmt_mm(rout)}\n"
            f"ANGL 60degree\n\n"
            f"END\n"
            f"NEW CONE\n"
            f"ORI Z is U and Y is {cone_ori_y}\n"
            f"POS {cone_pos_str}\n"
            f"DTOP {fmt_mm(dtop)}\n"
            f"DBOT {fmt_mm(dbot)}\n"
            f"HEIG {fmt_mm(h_cone)}\n\n"
            f"END"
        )
        
        if old_conn_pat.search(eq_text):
            eq_text = old_conn_pat.sub(new_casing_additions, eq_text)
        else:
            # If not matching the exact 28/12mm pattern, find the end of CASING and replace
            print(f"Warning: could not find exact old cylinder/cone in {tag}_CASING, appending instead")
            casing_end_pat = re.compile(r'(NEW SUBEQUIPMENT /' + tag + r'_CASING.*?)(END\s*\n)(NEW SUBEQUIPMENT|\Z)', re.DOTALL)
            m_ce = casing_end_pat.search(eq_text)
            if m_ce:
                c_block = m_ce.group(1) + new_casing_additions + "\n\n" + m_ce.group(2) + m_ce.group(3)
                eq_text = eq_text[:m_ce.start()] + c_block + eq_text[m_ce.end():]
                
        # Now update DISCHARGE nozzle
        # NEW NOZZLE /<TAG>_DISCHARGE_NOZZLE\nPOS ...\nORI ...\n...\nHEIG ...\nDUTY unset\n\nEND
        def replace_disc_nozz(m):
            body = m.group(0)
            body = re.sub(r'POS [^\n]+', f'POS {nozz_pos_str}', body, count=1)
            body = re.sub(r'HEIG [\d.]+mm', f'HEIG {fmt_mm(h_nozz)}', body, count=1)
            return body
            
        eq_text = re.sub(r'NEW NOZZLE /' + tag + r'_DISCHARGE_NOZZLE\s+POS [^\n]+\s+ORI [^\n]+\s+.*?HEIG [\d.]+mm',
                         replace_disc_nozz, eq_text, count=1, flags=re.DOTALL)
                         
    return eq_text

def main():
    src_path = Path(r'C:\Users\A\Desktop\wsb.txt')
    text = src_path.read_text(encoding='utf-8', errors='ignore')
    
    # Split header, equipments, footer
    # Header is up to the first NEW EQUIPMENT
    m_first_eq = re.search(r'\n(NEW EQUIPMENT /[^\n]+)', text)
    header = text[:m_first_eq.start() + 1]
    
    # Footer is from INPUT END or first OLD NOZZLE
    m_foot = re.search(r'\n(OLD NOZZLE [^\n]+)', text)
    if not m_foot:
        m_foot = re.search(r'\n(INPUT END\b[^\n]*)', text)
    footer = text[m_foot.start() + 1:]
    
    # Extract all equipment text
    body = text[len(header):m_foot.start() + 1]
    equis = re.findall(r'(NEW EQUIPMENT /([^\n]+).*?)(?=\nNEW EQUIPMENT /|\Z)', body, re.DOTALL)
    
    catrs = dict(re.findall(r'OLD NOZZLE /([^\n]+)\s+CATR SPCOMPONENT /([^\n]+)', footer))
    
    print(f"Header length: {len(header)} chars")
    print(f"Found {len(equis)} equipments")
    print(f"Footer length: {len(footer)} chars, {len(catrs)} CATR bindings")
    
    new_equis = []
    for eq_text, tag in equis:
        new_eq = process_equipment(eq_text, tag, catrs)
        new_equis.append(new_eq)
        
    updated_macro = header + "\n".join(new_equis) + "\n" + footer
    
    out_proj = REPO / "Projects" / "JK_Pump_Build" / "output" / "WSB_PU_all_pumps_rebuilt_updated.pml"
    out_proj.parent.mkdir(parents=True, exist_ok=True)
    out_proj.write_text(updated_macro, encoding='utf-8')
    print(f"Wrote updated macro to: {out_proj} ({len(updated_macro)} chars)")
    
    # Also write to Desktop/wsb.txt
    src_path.write_text(updated_macro, encoding='utf-8')
    print(f"Overwrote Desktop file: {src_path} ({len(updated_macro)} chars)")

if __name__ == '__main__':
    main()
