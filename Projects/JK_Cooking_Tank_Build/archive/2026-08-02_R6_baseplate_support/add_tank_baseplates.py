# -*- coding: utf-8 -*-
"""Add a 50mm-high base plate (CYLI) under every tank in cooking_tank.txt
except MAIN_CONDENSATE_TANK. Plate DIAM = tank main-body DIAM + 300,
top surface flush with the tank bottom (D 300 / U -300).
Only inserts new SUBEQUIPMENT blocks; touches nothing else.
"""
import io
import sys

SRC = r'C:\Users\A\Desktop\cooking_tank.txt'
BAK = r'C:\Users\A\Desktop\cooking_tank_orig_backup.txt'

# (tank name, horizontal axis string from its own shell POS line, main body DIAM)
TANKS = [
    ("BLEACH_HOT_WATER_TANK",    "E 18720mm S 6004mm", 5020),
    ("BLOW_TANK_1",              "E 27276mm N 6034mm", 7300),
    ("BLOW_TANK_2",              "E 27498mm N 18002mm", 7300),
    ("WARM_WATER_TANK",          "E 35894mm S 5970mm", 5700),
    ("BROWN_HOT_WATER_TANK",     "E 44004mm S 6002mm", 5714),
    ("JUNK_TRAP_1",              "E 33635mm N 8034mm", 1770),
    ("JUNK_TRAP_2",              "E 33635mm N 15965mm", 1770),
    ("ACCUMULATOR_TANK",         "E 44001mm N 12002mm", 7023),
    ("ACCUMULATOR_TANK_AID_1",   "E 38433mm N 10002mm", 2022),
    ("ACCUMULATOR_TANK_AID_2",   "E 38433mm N 14002mm", 2022),
    ("W_L_SERVICE_TANK_1",       "E 44006mm N 20002mm", 5000),
    ("W_L_SERVICE_TANK_2",       "E 44004mm N 27801mm", 5000),
    ("SPENT_LIQUOR_TANK",        "E 32502mm N 27803mm", 3000),
    ("B_L_TANK",                 "E 37501mm N 27801mm", 5020),
]

PLATE_TOP_D = 300   # all tank assemblies bottom out at D 300 (U -300)
PLATE_HEIG = 50
PLATE_ADD = 300


def make_block(name, horiz, body_diam):
    plate_diam = body_diam + PLATE_ADD
    pos = f"POS {horiz} D {PLATE_TOP_D + PLATE_HEIG // 2}mm"
    return [
        f"NEW SUBEQUIPMENT /{name}_BASEPLATE",
        "BUIL false",
        "DSCO unset",
        "PTSP unset",
        "INSC unset",
        "",
        "NEW CYLINDER",
        pos,
        f"DIAM {plate_diam}mm",
        f"HEIG {PLATE_HEIG}mm",
        "",
        "END",
    ]


def main():
    with io.open(SRC, 'r', encoding='utf-8-sig', newline='') as f:
        content = f.read()
    # normalize to \n for processing (original is CRLF; restored on write)
    content = content.replace('\r\n', '\n')
    lines = content.split('\n')
    if lines and lines[-1] == '':
        trailing_newline = True
        lines = lines[:-1]
    else:
        trailing_newline = False

    # safety: original backup
    with io.open(BAK, 'w', encoding='utf-8-sig', newline='') as f:
        f.write('\r\n'.join(lines) + ('\r\n' if trailing_newline else ''))

    inserted = []
    missing = []
    for name, horiz, body_diam in TANKS:
        anchor = f"NEW SUBEQUIPMENT /{name}_N1"
        try:
            idx = lines.index(anchor)
        except ValueError:
            missing.append(name)
            continue
        block = make_block(name, horiz, body_diam)
        lines[idx:idx] = block
        inserted.append((name, body_diam, body_diam + PLATE_ADD, horiz))

    out = '\r\n'.join(lines) + ('\r\n' if trailing_newline else '')
    with io.open(SRC, 'w', encoding='utf-8-sig', newline='') as f:
        f.write(out)

    print(f"inserted {len(inserted)} base plates")
    for name, bd, pd, horiz in inserted:
        print(f"  /{name}_BASEPLATE  DIAM {pd}mm (= {bd}+300)  {horiz} D 325mm")
    if missing:
        print("MISSING ANCHORS (not modified):", missing)


if __name__ == '__main__':
    main()
