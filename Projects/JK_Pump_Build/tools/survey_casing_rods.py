#!/usr/bin/env python3
"""Survey every *_CASING subequipment in a native E3D pump data listing.

Lists each cylinder (and box) with its POS / ORI / dims so the tie rods
(small long cylinders around the casing) can be identified per pump.
Read-only: prints a compact report.
"""
import re
import sys
from collections import OrderedDict

POS_RE = re.compile(
    r"POS\s+"
    r"(?:(?P<E>[EW])\s+(?P<Eval>-?\d+(?:\.\d+)?)mm\s+)?"
    r"(?:(?P<N>[NS])\s+(?P<Nval>-?\d+(?:\.\d+)?)mm\s+)?"
    r"(?:(?P<U>[UD])\s+(?P<Uval>-?\d+(?:\.\d+)?)mm)?"
)
ORI_RE = re.compile(r"ORI\s+Y is ([UDSNEW])\s+and\s+Z is ([UDSNEW])")
DIM_RE = re.compile(r"(DIAM|HEIG|XLEN|YLEN|ZLEN|DTOP|DBOT)\s+(-?\d+(?:\.\d+)?)mm")


def parse(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    stack = []          # open elements
    top = None          # current element dict
    root = {"type": "ROOT", "children": []}
    current_parent = root
    results = OrderedDict()   # subequipment name -> element list

    for idx, raw in enumerate(lines, 1):
        line = raw.strip()
        if line.startswith("NEW "):
            rest = line[4:].strip()
            m = re.match(r"^(EQUIPMENT|SUBEQUIPMENT|ZONE|CYLINDER|BOX|CONE|"
                         r"EXTRUSION|NOZZLE|NCYLINDER|NBOX|LOOP|VERTEX|PYRAMID|"
                         r"SNOUT|DIS[HC]?|CTORUS|NCTORUS|SOLID|NLSOF|SLOPE|DISH)\b\s*(.*)$",
                         rest)
            etype = m.group(1) if m else rest.split()[0]
            name = m.group(2).strip() if m else ""
            el = {
                "type": etype,
                "name": name,
                "line": idx,
                "pos": None,
                "ori": None,
                "dims": {},
                "attrs": [],
                "children": [],
            }
            stack.append(el)
            top = el
            continue

        if top is None:
            continue

        if line.startswith("POS "):
            m = POS_RE.match(line)
            if m:
                pos = {}
                for ax, val in (("E", m.group("Eval")), ("N", m.group("Nval")),
                                ("U", m.group("Uval"))):
                    if val is not None:
                        pos[ax] = float(val)
                top["pos"] = pos
        elif line.startswith("ORI "):
            m = ORI_RE.match(line)
            if m:
                top["ori"] = {"y": m.group(1), "z": m.group(2)}
        elif line.startswith(("DIAM ", "HEIG ", "XLEN ", "YLEN ", "ZLEN ",
                              "DTOP ", "DBOT ")):
            m = DIM_RE.match(line)
            if m:
                top["dims"][m.group(1)] = float(m.group(2))
        elif line == "END":
            el = stack.pop()
            parent = stack[-1] if stack else None
            if parent is not None:
                parent["children"].append(el)
            if stack:
                top = stack[-1]
            else:
                top = None
            # record subequipments of interest
            if el["type"] == "SUBEQUIPMENT" and re.search(r"_(CASING|DISCHARGE|SUCTION|CASING_FASTENERS)$", el["name"]):
                results.setdefault(el["name"], el)

    return results


def fmt_pos(pos):
    if not pos:
        return "?"
    return " ".join(f"{k} {v}" for k, v in pos.items())


def fmt_ori(ori):
    if not ori:
        return "?"
    return f"Y is {ori['y']} Z is {ori['z']}"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\A\Desktop\PUMP.txt"
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    blocks = parse(path)
    lines = []
    for name, sub in blocks.items():
        lines.append(f"== {name} (line {sub['line']})")
        for child in sub["children"]:
            if child["type"] in ("CYLINDER", "BOX", "CONE"):
                pos = child["pos"] or {}
                dims = child["dims"]
                d = " ".join(f"{k}={v}" for k, v in dims.items())
                lines.append(f"   {child['type']:<8} {fmt_pos(pos):<42} {fmt_ori(child['ori']):<22} {d}")
        lines.append("")
    text = "\n".join(lines)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {out_path} ({len(lines)} lines)")
    else:
        print(text)


if __name__ == "__main__":
    main()
