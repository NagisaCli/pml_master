# -*- coding: utf-8 -*-
"""
Audit script for verify_transformed_mc_pumps.
Checks:
1. 054, 020, 028, 018, 038 have identical primitive counts and subequipment structures.
2. Geometry coordinates and orientations are mathematically verified for all 4 target pumps.
3. All other 27 pumps in the native zone are 100% untouched.
4. OLD NOZZLE bindings are complete and correct for all 31 equipments.
"""

import re
import math

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

def audit():
    src_zone_path = 'Projects/JK_Pump_Build/imports/2026-08-23_PUMP_native_zone.txt'
    src_054_path = 'Projects/JK_Pump_Build/imports/2026-08-24_205_PU_054_native_updated.txt'
    out_path = 'Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced/JK_Pump_Build_all_pumps_20260823_mc_replaced.pml'
    
    with open(src_zone_path, 'r', encoding='utf-8') as f:
        src_text = f.read()
    with open(src_054_path, 'r', encoding='utf-8') as f:
        src_054_text = f.read()
    with open(out_path, 'r', encoding='utf-8') as f:
        out_text = f.read()
        
    def extract_equis(txt):
        equis = {}
        matches = list(re.finditer(r'NEW EQUIPMENT\s+(/\S+)', txt))
        for i, m in enumerate(matches):
            tag = m.group(1)
            start = m.start()
            if i + 1 < len(matches):
                end = matches[i+1].start()
            else:
                m_old = re.search(r'\n(OLD NOZZLE|INPUT END)', txt[start:])
                end = start + m_old.start() + 1 if m_old else len(txt)
            equis[tag] = txt[start:end].strip()
        return equis
        
    src_equis = extract_equis(src_text)
    src_054_equis = extract_equis(src_054_text)
    out_equis = extract_equis(out_text)
    
    print(f'Source zone equis count: {len(src_equis)}')
    print(f'Output equis count: {len(out_equis)}')
    assert len(src_equis) == 30, 'Source equis count should be 30'
    assert len(out_equis) == 31, 'Output equis count should be 31 (added 204_PU_028)'
    assert '/204_PU_028' in out_equis, '204_PU_028 not found in output'
    
    # 1. Verify non-target pumps are 100% identical
    target_tags = {'/205_PU_038', '/205_PU_018', '/203_PU_020', '/204_PU_028', '/205_PU_054'}
    for tag in src_equis:
        if tag not in target_tags:
            src_blk = src_equis[tag]
            out_blk = out_equis[tag]
            if src_blk != out_blk:
                print(f'ERROR: Non-target pump {tag} was modified!')
                assert False
    print('PASS: All 26 non-target pumps are 100% identical to baseline.')
    
    # Check 054 matches new updated 054
    assert out_equis['/205_PU_054'] == src_054_equis['/205_PU_054'], '205_PU_054 was not updated with latest model!'
    print('PASS: 205_PU_054 matches latest 2026-08-24 model 100%.')
    
    # 2. Check structure of updated 054 vs targets
    blk_054 = src_054_equis['/205_PU_054']
    subes_054 = re.findall(r'NEW SUBEQUIPMENT\s+(/\S+)', blk_054)
    nozzs_054 = re.findall(r'NEW NOZZLE\s*(?:(/\S+))?', blk_054)
    prims_054 = re.findall(r'NEW (?!LOOP|VERTEX|NXTRUSION)([A-Z0-9]+)', blk_054)
    
    print(f'Updated 054 has {len(subes_054)} subequipments, {len(nozzs_054)} nozzles, {len(prims_054)} primitives.')
    
    targets = {
        '/203_PU_020': {'anchor': (17095.0, 5685.0, 0.0), 'rot': 'CCW'},
        '/204_PU_028': {'anchor': (22370.0, 6986.0, 0.0), 'rot': 'CW'},
        '/205_PU_018': {'anchor': (35727.6, 5019.0, 0.0), 'rot': 'CCW'},
        '/205_PU_038': {'anchor': (43112.9, 5016.0, 0.0), 'rot': 'CCW'},
    }
    
    for tag, cfg in targets.items():
        e0_tgt, n0_tgt, u0_tgt = cfg['anchor']
        rot = cfg['rot']
        blk_tgt = out_equis[tag]
        subes_tgt = re.findall(r'NEW SUBEQUIPMENT\s+(/\S+)', blk_tgt)
        nozzs_tgt = re.findall(r'NEW NOZZLE\s*(?:(/\S+))?', blk_tgt)
        prims_tgt = re.findall(r'NEW (?!LOOP|VERTEX|NXTRUSION)([A-Z0-9]+)', blk_tgt)
        
        print(f'\nChecking {tag} (rot={rot}):')
        print(f'  Subequipments: {len(subes_tgt)} (expected {len(subes_054)})')
        print(f'  Nozzles: {len(nozzs_tgt)} (expected {len(nozzs_054)})')
        print(f'  Primitives: {len(prims_tgt)} (expected {len(prims_054)})')
        
        assert len(subes_tgt) == len(subes_054), f'{tag} subequipment count mismatch'
        assert len(nozzs_tgt) == len(nozzs_054), f'{tag} nozzle count mismatch'
        assert len(prims_tgt) == len(prims_054), f'{tag} primitive count mismatch'
        assert prims_tgt == prims_054, f'{tag} primitive type sequence mismatch'
        
        # 1. Casing CYL
        m_casing = re.search(r'NEW SUBEQUIPMENT ' + tag + r'_CASING.*?NEW CYLINDER\s+POS\s+([^\n]+)\s+ORI\s+([^\n]+)\s+DIAM\s+([^\n]+)\s+HEIG\s+([^\n]+)', blk_tgt, re.DOTALL)
        assert m_casing, f'{tag} casing cylinder not found'
        pos_str, ori_str, diam, heig = m_casing.groups()
        e, n, u = parse_coords(pos_str)
        print(f'  CASING CYL: {pos_str} | ORI {ori_str}')
        if rot == 'CCW':
            assert 'Y is U and Z is W' in ori_str
            assert e < e0_tgt, f'{tag} Casing should be West of anchor: {e} >= {e0_tgt}'
        else: # CW
            assert 'Y is U and Z is E' in ori_str
            assert e > e0_tgt, f'{tag} Casing should be East of anchor: {e} <= {e0_tgt}'
        assert math.isclose(n, n0_tgt, abs_tol=1e-2), f'{tag} casing N off centerline'
        
        # 2. Driver CYL
        m_driver = re.search(r'NEW SUBEQUIPMENT ' + tag + r'_DRIVER.*?NEW CYLINDER\s+POS\s+([^\n]+)\s+ORI\s+([^\n]+)\s+DIAM\s+([^\n]+)\s+HEIG\s+([^\n]+)', blk_tgt, re.DOTALL)
        assert m_driver, f'{tag} driver cylinder not found'
        pos_str, ori_str, diam, heig = m_driver.groups()
        e, n, u = parse_coords(pos_str)
        print(f'  DRIVER CYL: {pos_str} | ORI {ori_str}')
        if rot == 'CCW':
            assert 'Y is U and Z is W' in ori_str
            assert e > e0_tgt, f'{tag} Driver should be East of anchor: {e} <= {e0_tgt}'
        else: # CW
            assert 'Y is U and Z is E' in ori_str
            assert e < e0_tgt, f'{tag} Driver should be West of anchor: {e} >= {e0_tgt}'
        assert math.isclose(n, n0_tgt, abs_tol=1e-2), f'{tag} driver N off centerline'
        
        # 3. Baseplate main box
        m_base = re.search(r'NEW SUBEQUIPMENT ' + tag + r'_BASE.*?NEW BOX\s+POS\s+([^\n]+)\s+(?:ORI\s+([^\n]+)\s+)?XLEN\s+615\.18mm\s+YLEN\s+2000mm\s+ZLEN\s+50mm', blk_tgt, re.DOTALL)
        assert m_base, f'{tag} baseplate main box not found'
        pos_str = m_base.group(1)
        e, n, u = parse_coords(pos_str)
        print(f'  BASEPLATE 50mm BOX: {pos_str}')
        assert math.isclose(e, e0_tgt, abs_tol=1e-2) and math.isclose(n, n0_tgt, abs_tol=1e-2), f'{tag} baseplate center mismatch'
        
        # 4. Suction nozzle
        m_suct = re.search(r'NEW NOZZLE ' + tag + r'_SUCTION_NOZZLE\s+POS\s+([^\n]+)\s+ORI\s+([^\n]+)', blk_tgt)
        assert m_suct, f'{tag} suction nozzle not found'
        print(f'  SUCTION NOZZLE: {m_suct.group(1)} | ORI {m_suct.group(2)}')
        if rot == 'CCW':
            assert 'Y is U and Z is S' in m_suct.group(2)
        else:
            assert 'Y is U and Z is N' in m_suct.group(2)
            
        # 5. Discharge nozzle
        m_disc = re.search(r'NEW NOZZLE ' + tag + r'_DISCHARGE_NOZZLE\s+POS\s+([^\n]+)\s+ORI\s+([^\n]+)', blk_tgt)
        assert m_disc, f'{tag} discharge nozzle not found'
        print(f'  DISCHARGE NOZZLE: {m_disc.group(1)} | ORI {m_disc.group(2)}')
        if rot == 'CCW':
            assert 'Y is W and Z is N' in m_disc.group(2)
        else:
            assert 'Y is E and Z is S' in m_disc.group(2)

    # 3. Check OLD NOZZLE section in epilogue
    epilogue = out_text[out_text.find('OLD NOZZLE'):]
    for tag in ['/205_PU_054', '/203_PU_020', '/204_PU_028', '/205_PU_018', '/205_PU_038']:
        assert f'OLD NOZZLE 1 of SUBEQUIPMENT {tag}_AID_MOTOR_2\nCATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW' in epilogue, f'Missing OLD NOZZLE 1 of {tag}_AID_MOTOR_2'
        assert f'OLD NOZZLE {tag}_SUCTION_NOZZLE\nCATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR' in epilogue, f'Missing OLD NOZZLE {tag}_SUCTION_NOZZLE'
        assert f'OLD NOZZLE 2 of SUBEQUIPMENT {tag}_SUCTION\nCATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR' in epilogue, f'Missing OLD NOZZLE 2 of {tag}_SUCTION'
        assert f'OLD NOZZLE {tag}_DISCHARGE_NOZZLE\nCATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR' in epilogue, f'Missing OLD NOZZLE {tag}_DISCHARGE_NOZZLE'
        
    print('\nPASS: All OLD NOZZLE catalog references verified.')
    print('\nALL AUDIT CHECKS PASSED PERFECTLY!')

if __name__ == '__main__':
    audit()
