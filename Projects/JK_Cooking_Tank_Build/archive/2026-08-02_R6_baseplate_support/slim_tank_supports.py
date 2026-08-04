# -*- coding: utf-8 -*-
"""Slim down SUPPORT subequipment for the 10 target tanks in cooking_tank.txt:
keep ONLY the bolt cylinders (DIAM 30 / 60 / 52), delete every BOX (foot
plate / pad / leg) and any structural CYLINDER (skirt / base ring).
Excluded tanks (SUPPORT untouched): BLOW_TANK_1, BLOW_TANK_2, JUNK_TRAP_1,
JUNK_TRAP_2, MAIN_CONDENSATE_TANK. Nothing else in the file is modified.
"""
import io

SRC = r'C:\Users\A\Desktop\cooking_tank.txt'
BAK = r'C:\Users\A\Desktop\cooking_tank_before_slim_backup.txt'

KEEP_DIAMS = {30.0, 60.0, 52.0}
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


def find_support_blocks(lines):
    """Return {equi: (start, end)} for each *_SUPPORT subequipment.
    start = index of 'NEW SUBEQUIPMENT /x_SUPPORT'
    end   = index of the subequipment's closing END.
    Robust: track primitive nesting -- an END while not inside a primitive
    closes the subequipment.
    """
    blocks = {}
    cur_equi = None
    n = len(lines)
    i = 0
    while i < n:
        l = lines[i]
        if l.startswith('NEW EQUIPMENT '):
            cur_equi = l.split('/')[1]
            i += 1
            continue
        if l.startswith('NEW SUBEQUIPMENT /') and l.endswith('_SUPPORT') and cur_equi:
            start = i
            i += 1
            in_prim = False
            while i < n:
                li = lines[i]
                if li.startswith('NEW ') and not li.startswith('NEW SUBEQUIPMENT'):
                    in_prim = True
                elif li == 'END' and in_prim:
                    in_prim = False
                elif li == 'END' and not in_prim:
                    blocks[cur_equi] = (start, i)
                    i += 1
                    break
                i += 1
            continue
        i += 1
    return blocks


def split_block(block_lines):
    """Split a SUPPORT block into (header, primitives, tail).
    block_lines: lines from the SUBEQUIPMENT header to its closing END (incl.).
    header = lines between the header line and the first primitive
             (BUIL..INSC + blank).
    primitives = list of chunks, each 'NEW xxx' .. 'END' (inclusive).
    tail = the subequipment closing 'END' (exactly one line).
    """
    header = []
    prims = []
    cur = None
    for l in block_lines[1:]:  # skip the NEW SUBEQUIPMENT line itself
        if l.startswith('NEW ') and cur is None:
            cur = [l]
        elif cur is not None:
            cur.append(l)
            if l == 'END':
                prims.append(cur)
                cur = None
        elif l == 'END':
            # stray END with no open primitive: closes the subequipment
            continue  # handled by tail below; nothing else may follow
        else:
            header.append(l)
    tail = 'END'
    # header must end with the blank separator before the first primitive
    if header and header[-1] != '':
        header.append('')
    return header, prims, tail


def main():
    with io.open(SRC, 'r', encoding='utf-8-sig', newline='') as f:
        content = f.read()
    content = content.replace('\r\n', '\n')
    lines = content.split('\n')
    if lines and lines[-1] == '':
        trailing_newline = True
        lines = lines[:-1]
    else:
        trailing_newline = False

    with io.open(BAK, 'w', encoding='utf-8-sig', newline='') as f:
        f.write('\r\n'.join(lines) + ('\r\n' if trailing_newline else ''))

    blocks = find_support_blocks(lines)
    report = []
    # process bottom-up so earlier line indices stay valid after shrinking
    for equi, (start, end) in sorted(blocks.items(), key=lambda kv: kv[1][0], reverse=True):
        if equi not in TARGETS:
            report.append((equi, 'SKIPPED (excluded)', 0, 0))
            continue
        block_lines = lines[start:end + 1]
        header, prims, tail = split_block(block_lines)
        kept, removed = [], []
        for p in prims:
            first = p[0]
            if first == 'NEW BOX':
                removed.append(p)
                continue
            if first == 'NEW CYLINDER':
                diam = None
                for pl in p:
                    if pl.startswith('DIAM '):
                        diam = float(pl.split()[1].replace('mm', ''))
                        break
                if diam in KEEP_DIAMS:
                    kept.append(p)
                else:
                    removed.append(p)
            else:
                removed.append(p)
        new_block = [block_lines[0]] + header
        for k in kept:
            new_block.extend(k)
        new_block.append(tail)
        lines[start:end + 1] = new_block
        report.append((equi, 'SLIMMED', len(kept), len(removed)))

    out = '\r\n'.join(lines) + ('\r\n' if trailing_newline else '')
    with io.open(SRC, 'w', encoding='utf-8-sig', newline='') as f:
        f.write(out)

    print(f"{'tank':32s} {'action':10s} kept  removed")
    for equi, act, k, r in report:
        print(f"{equi:32s} {act:10s} {k:4d}  {r:4d}")


if __name__ == '__main__':
    main()
