"""
Analyse the /P1501B reference pump structurally.

``Reference_pumps.txt`` defines HOW a complete pump is built -- not what size
this project's pumps are.  This script measures the reference so its
construction can be re-expressed as proportions of each target pump's own
governing dimensions.  Its absolute sizes, coordinates and nozzle parameters
are deliberately NOT carried forward (DO.txt).

Key fact established on 2026-08-18 and re-checked here: the /P1501B equipment
origin sits on the SHAFT CENTRELINE, not on the foundation.  The casing volute
is centred on local U 0 and the baseplate sits at negative U.  Any adaptation
must therefore treat local U as an offset from the shaft axis.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

SOURCE = Path(r"C:\Users\A\Desktop\Reference_pumps.txt")

_POS_TOKEN = re.compile(r"\b([ENSWUD])\s*(-?[\d.]+)\s*mm", re.IGNORECASE)
_SIGN = {"E": 1.0, "W": -1.0, "N": 1.0, "S": -1.0, "U": 1.0, "D": -1.0}
_AXIS = {"E": "east", "W": "east", "N": "north", "S": "north", "U": "up", "D": "up"}
_DIMS = ("DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "XBOT", "YBOT",
         "XTOP", "YTOP", "XOFF", "YOFF", "RADI")


def parse(path: Path = SOURCE):
    """Return (elements, sube_offsets) for the reference listing."""
    elements = []
    sube_offsets = {}
    sube = "(equipment)"
    current = None
    in_loop = False

    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("NEW SUBEQUIPMENT /"):
            sube = line.split("/", 1)[1].strip()
            sube_offsets.setdefault(sube, {"east": 0.0, "north": 0.0, "up": 0.0})
            current = None
            in_loop = False
            continue
        if line.startswith("NEW LOOP"):
            in_loop = True
            continue
        if line.startswith("NEW VERTEX") or (in_loop and line == "END"):
            continue
        if line.startswith("NEW "):
            in_loop = False
            kind = line[4:].split("/", 1)[0].strip()
            current = {"kind": kind, "sube": sube, "attrs": {},
                       "pos": None, "ori": None}
            elements.append(current)
            continue
        if line.startswith("POS") and not in_loop:
            pos = {"east": 0.0, "north": 0.0, "up": 0.0}
            for letter, value in _POS_TOKEN.findall(line):
                letter = letter.upper()
                pos[_AXIS[letter]] = _SIGN[letter] * float(value)
            if current is None:
                # A POS directly under a SUBE header is that frame's offset.
                if sube in sube_offsets:
                    sube_offsets[sube] = pos
            else:
                current["pos"] = pos
            continue
        if current is None:
            continue
        if line.startswith("ORI"):
            current["ori"] = line[3:].strip()
        else:
            for key in _DIMS:
                if line.startswith(key):
                    match = re.search(r"(-?[\d.]+)", line[len(key):])
                    if match:
                        current["attrs"][key] = float(match.group(1))
                    break
    return elements, sube_offsets


def main() -> int:
    elements, offsets = parse()
    by_sube = defaultdict(list)
    for element in elements:
        by_sube[element["sube"]].append(element)

    print(f"Reference /P1501B -- {len(elements)} elements\n")
    print("SUBE frame offsets (a relative offset between frames, not a point):")
    for name, offset in offsets.items():
        print(f"  {name:<32} E{offset['east']:+8.2f} N{offset['north']:+8.2f} "
              f"U{offset['up']:+8.2f}")

    print("\nComposition by SUBE:")
    for name, items in by_sube.items():
        counts = defaultdict(int)
        for item in items:
            counts[item["kind"]] += 1
        summary = ", ".join(f"{k}x{v}" for k, v in sorted(counts.items()))
        print(f"  {name:<32} {len(items):>3} elements  ({summary})")

    # The governing dimensions the target project supplies per pump: casing
    # diameter and length, motor diameter and length, baseplate L x W.
    print("\nGoverning reference dimensions (for proportional adaptation):")
    casing = [e for e in by_sube["Casing_and_drive_shaft"] if e["kind"] == "CYLINDER"]
    for element in casing:
        print(f"  casing CYLI  DIAM {element['attrs'].get('DIAM'):>7} "
              f"HEIG {element['attrs'].get('HEIG'):>7}  "
              f"ORI {element['ori']}  POS {element['pos']}")
    motor = [e for e in by_sube["Motor"]
             if e["kind"] in ("CYLINDER", "DISH") and e["attrs"].get("DIAM", 0) > 200]
    for element in motor:
        print(f"  motor {element['kind']:<5} DIAM {element['attrs'].get('DIAM'):>7} "
              f"HEIG {element['attrs'].get('HEIG'):>7}  POS {element['pos']}")

    print("\nBaseplate / support members (largest BOXes):")
    plates = [e for e in by_sube["Baseplate_and_support"] if e["kind"] == "BOX"]
    plates.sort(key=lambda e: -(e["attrs"].get("XLEN", 0) * e["attrs"].get("YLEN", 0)))
    for element in plates[:6]:
        attrs = element["attrs"]
        print(f"  BOX {attrs.get('XLEN'):>7} x {attrs.get('YLEN'):>7} x "
              f"{attrs.get('ZLEN'):>6}  POS {element['pos']}")

    lows = [e["pos"]["up"] - e["attrs"].get("ZLEN", 0) / 2
            for e in plates if e["pos"]]
    print(f"\nLowest baseplate underside (local U): {min(lows):.2f}")
    print("Casing volute centred on local U 0 -> the EQUI origin is the SHAFT")
    print("CENTRELINE, and every local U is an offset from that axis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
