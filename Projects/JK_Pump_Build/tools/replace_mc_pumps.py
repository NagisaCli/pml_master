# -*- coding: utf-8 -*-
import re, os

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

def rotate_single_direction(d_str):
    tokens = d_str.strip().split()
    new_tokens = []
    for t in tokens:
        if t == 'E': new_tokens.append('N')
        elif t == 'W': new_tokens.append('S')
        elif t == 'N': new_tokens.append('W')
        elif t == 'S': new_tokens.append('E')
        elif t in ('U', 'D'): new_tokens.append(t)
        else: new_tokens.append(t)
    return ' '.join(new_tokens)

def rotate_ori(ori_str):
    m = re.match(r'^(ORI\s+)?(Y|Z|X)\s+is\s+(.*?)\s+and\s+(Y|Z|X)\s+is\s+(.*?)$', ori_str, re.IGNORECASE)
    if m:
        prefix = m.group(1) or ''
        ax1 = m.group(2)
        dir1 = rotate_single_direction(m.group(3))
        ax2 = m.group(4)
        dir2 = rotate_single_direction(m.group(5))
        return '%s%s is %s and %s is %s' % (prefix, ax1, dir1, ax2, dir2)
    
    m2 = re.match(r'^(ORI\s+)?(Y|Z|X)\s+is\s+(.*?)$', ori_str, re.IGNORECASE)
    if m2:
        prefix = m2.group(1) or ''
        ax1 = m2.group(2)
        dir1 = rotate_single_direction(m2.group(3))
        return '%s%s is %s' % (prefix, ax1, dir1)
    
    return ori_str

print('Transformer functions loaded')
