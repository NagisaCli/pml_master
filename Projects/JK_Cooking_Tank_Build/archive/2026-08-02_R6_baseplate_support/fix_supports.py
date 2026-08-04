# -*- coding: utf-8 -*-
"""Two fixes to cooking_tank.txt (state: after SUPPORT slim-down):

1. RESTORE the skirt + base-ring CYLINDERs for ACCUMULATOR_TANK,
   ACCUMULATOR_TANK_AID_1, ACCUMULATOR_TANK_AID_2 (they were wrongly
   removed by the slim step). Taken verbatim from the pre-slim backup.

2. MOVE every bolt CYLINDER (DIAM 30/60/52) in the 10 slimmed SUPPORT
   blocks radially inward so the bolt ring sits at tank-wall + 75mm
   (mid-width of the 300mm-wide base plate) instead of at the plate edge
   (tank-wall + 150mm).

Only these lines change; everything else stays byte-identical.
"""
import io
import re

SRC = r'C:\Users\A\Desktop\cooking_tank.txt'
PRE_SLIM = r'C:\Users\A\Desktop\cooking_tank_before_slim_backup.txt'
BAK = r'C:\Users\A\Desktop\cooking_tank_before_restore_backup.txt'

TARGETS = {
    "ACCUMULATOR_TANK",
    "ACCUMULATOR_TANK_AID_1",
    "ACCUMULATOR_TANK_AID_2",
    "BLEACH_HOT_WATER_TANK",
    "BROWN_HOT_WATER_TANK",
    "B_L_TANK",
    "SPENT_LIQUOR_TANK",
    "WARM_WATER_TANK",
    "W_L_SERVICE_TANK_1",
    "W_L_SERVICE_TANK_2",
}

RESTORE = {"ACCUMULATOR_TANK", "ACCUMULATOR_TANK_AID_1", "ACCUMULATOR_TANK_AID_2"}

# tank axis + main-body radius (mm) -- axis taken from each tank's shell POS
GEOM = {
    "BLEACH_HOT_WATER_TANK":    (18720.0, -6004.0, 5020.0 / 2),
    "WARM_WATER_TANK":          (35894.0, -5970.0, 5700.0 / 2),
    "BROWN_HOT_WATER_TANK":     (44004.0, -6002.0, 5714.0 / 2),
    "B_L_TANK":                 (37501.0, 27801.0, 5020.0 / 2),
    "SPENT_LIQUOR_TANK":        (32502.0, 27803.0, 3000.0 / 2),
    "W_L_SERVICE_TANK_1":       (44006.0, 20002.0, 5000.0 / 2),
    "W_L_SERVICE_TANK_2":       (44004.0, 27801.0, 5000.0 / 2),
    "ACCUMULATOR_TANK":         (44001.0, 12002.0, 7023.0 / 2),
    "ACCUMULATOR_TANK_AID_1":   (38433.0, 10002.0, 2022.0 / 2),
    "ACCUMULATOR_TANK_AID_2":   (38433.0, 14002.0, 2022.0 / 2),
}

TARGET_RADIUS_OFFSET = 75.0  # bolts sit at tank wall + 75mm

POS_RE = re.compile(
    r'^POS E ([\d.]+)mm (N|S) ([\d.]+)mm (U|D) ([\d.]+)mm$')


def read_lines(path):
    with io.open(path, 'r', encoding='utf-8-sig', newline='') as f:
        content = f.read()
    content = content.replace('\r\n', '\n')
    lines = content.split('\n')
    if lines and lines[-1] == '':
        return lines[:-1], True
    return lines, False


def write_lines(path, lines, trailing):
    out = '\r\n'.join(lines) + ('\r\n' if trailing else '')
    with io.open(path, 'w', encoding='utf-8-sig', newline='') as f:
        f.write(out)


def extract_skirt_ring(pre_lines, tank):
    """Return the first two primitive chunks (skirt CYLI + ring CYLI) of the
    tank's SUPPORT block in the pre-slim backup, verbatim (list of lines).
    """
    i = pre_lines.index(f'NEW SUBEQUIPMENT /{tank}_SUPPORT')
    chunks = []
    cur = None
    for l in pre_lines[i + 1:]:
        if l.startswith('NEW ') and cur is None:
            cur = [l]
        elif cur is not None:
            cur.append(l)
            if l == 'END':
                chunks.append(cur)
                cur = None
                if len(chunks) == 2:
                    return chunks
    raise RuntimeError(f'skirt/ring not found for {tank}')


def move_bolt_pos(pos_line, e0, n0, r):
    """Move one bolt POS line radially inward to radius (r + 75mm).
    Keeps the N/S and U/D axis naming of the original line.
    """
    m = POS_RE.match(pos_line)
    if not m:
        return pos_line
    e, ns, ns_v, ud, ud_v = m.group(1), m.group(2), float(m.group(3)), m.group(4), float(m.group(5))
    e = float(e)
    n = -ns_v if ns == 'S' else ns_v
    de, dn = e - e0, n - n0
    cur_r = (de * de + dn * dn) ** 0.5
    new_r = r + TARGET_RADIUS_OFFSET
    f = new_r / cur_r if cur_r else 1.0
    ne, nn = e0 + de * f, n0 + dn * f
    # keep axis naming: S if the value would be negative, else N
    if ns == 'S':
        new_ns = f'S {abs(nn):.1f}mm'
    else:
        new_ns = f'N {nn:.1f}mm'
    return f'POS E {ne:.1f}mm {new_ns} {ud} {ud_v:.1f}mm'


def main():
    lines, trailing = read_lines(SRC)
    pre_lines, _ = read_lines(PRE_SLIM)

    with io.open(BAK, 'w', encoding='utf-8-sig', newline='') as f:
        f.write('\r\n'.join(lines) + ('\r\n' if trailing else ''))

    # 1. restore skirt + ring for ACCUMULATOR tanks
    for tank in sorted(RESTORE):
        i = lines.index(f'NEW SUBEQUIPMENT /{tank}_SUPPORT')
        # find end of header: first primitive start after header lines
        j = i + 1
        while j < len(lines) and lines[j] in (
                'BUIL false', 'DSCO unset', 'PTSP unset', 'INSC unset', ''):
            j += 1
        skirt, ring = extract_skirt_ring(pre_lines, tank)
        lines[j:j] = skirt + ring

    # 2. move bolts inward in all 10 slimmed SUPPORT blocks
    moved = 0
    for tank in sorted(TARGETS):
        e0, n0, r = GEOM[tank]
        i = lines.index(f'NEW SUBEQUIPMENT /{tank}_SUPPORT')
        j = i + 1
        in_prim = False
        while j < len(lines):
            l = lines[j]
            if l.startswith('NEW SUBEQUIPMENT') and j > i:
                break
            if l.startswith('NEW ') and not l.startswith('NEW SUBEQUIPMENT'):
                in_prim = True
            elif l == 'END' and in_prim:
                in_prim = False
            elif l == 'END' and not in_prim:
                break
            if in_prim and l.startswith('POS E '):
                # only move bolt cylinders; check this primitive's DIAM
                k = j + 1
                diam = None
                while k < len(lines) and lines[k] != 'END':
                    dm = re.match(r'^DIAM ([\d.]+)mm$', lines[k])
                    if dm:
                        diam = float(dm.group(1))
                        break
                    k += 1
                if diam in (30.0, 60.0, 52.0):
                    lines[j] = move_bolt_pos(l, e0, n0, r)
                    moved += 1
            j += 1

    write_lines(SRC, lines, trailing)
    print(f'restored skirt+ring for {len(RESTORE)} tanks; moved {moved} bolt positions')


if __name__ == '__main__':
    main()
