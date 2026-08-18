#!/usr/bin/env python3
"""Rotate the casing tie rods of every pump in a native E3D data listing.

Each pump's CASING carries small long tie-rod cylinders (ORI Y is U, Z is the
casing axis) arranged around the casing centre.  The rod at the 12-o'clock
position passes through the top discharge boss on every pump (the reported
clash).  This tool rotates the whole rod pattern CCW (RHR) about the casing
axis; pumps whose rod count is exactly 3 keep the requested 45 deg; other
arrangements try 45 deg first and then nearby angles until the whole pattern
is clash-free.  Only the rod POS lines are changed; nothing else is touched.

Usage:
  python rotate_casing_rods.py <input> <output> [--report report.txt]
"""
import math
import re
import sys

# ---------------------------------------------------------------- parsing

POS_RE = re.compile(
    r"POS\s+"
    r"(?:(?P<EA>[EW])\s+(?P<E>-?\d+(?:\.\d+)?)mm\s+)?"
    r"(?:(?P<NA>[NS])\s+(?P<N>-?\d+(?:\.\d+)?)mm\s+)?"
    r"(?:(?P<UA>[UD])\s+(?P<U>-?\d+(?:\.\d+)?)mm)?"
)
ORI_RE = re.compile(r"ORI\s+Y is ([UDSNEW])\s+and\s+Z is ([UDSNEW])")
DIM_RE = re.compile(r"^(DIAM|HEIG|XLEN|YLEN|ZLEN|DTOP|DBOT)\s+"
                    r"(-?\d+(?:\.\d+)?)mm$")

AXIS = {"N": (0.0, 1.0, 0.0), "S": (0.0, -1.0, 0.0),
        "E": (1.0, 0.0, 0.0), "W": (-1.0, 0.0, 0.0)}


def parse(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        lines = f.readlines()
    stack = []
    top = None
    root = {"type": "ROOT", "children": []}
    for idx, raw in enumerate(lines, 1):
        line = raw.rstrip("\r\n")
        if line.startswith("NEW "):
            rest = line[4:].strip()
            m = re.match(r"^(EQUIPMENT|SUBEQUIPMENT|ZONE|CYLINDER|BOX|CONE|"
                         r"EXTRUSION|NOZZLE|NCYLINDER|NBOX|LOOP|VERTEX|PYRAMID|"
                         r"SNOUT|DISH|CTORUS|NCTORUS|SOLID|SLOPE)\b\s*(.*)$", rest)
            etype = m.group(1) if m else rest.split()[0]
            name = m.group(2).strip() if m else ""
            el = {"type": etype, "name": name, "line": idx,
                  "pos": None, "ori": None, "dims": {}, "children": []}
            stack.append(el)
            top = el
            continue
        if top is None:
            continue
        if line.startswith("POS "):
            m = POS_RE.match(line)
            if m:
                top["pos"] = {}
                for ax, val in (("E", m.group("E")), ("N", m.group("N")),
                                ("U", m.group("U"))):
                    if val is not None:
                        top["pos"][ax] = float(val)
        elif line.startswith("ORI "):
            m = ORI_RE.match(line)
            if m:
                top["ori"] = {"y": m.group(1), "z": m.group(2)}
        else:
            m = DIM_RE.match(line)
            if m:
                top["dims"][m.group(1)] = float(m.group(2))
        if line == "END":
            el = stack.pop()
            el["end_line"] = idx
            parent = stack[-1] if stack else None
            if parent is not None:
                parent["children"].append(el)
            else:
                root["children"].append(el)
            top = stack[-1] if stack else None
    return lines, root


# ---------------------------------------------------------------- geometry

def sub(v, w):
    return (v[0] - w[0], v[1] - w[1], v[2] - w[2])


def add(v, w):
    return (v[0] + w[0], v[1] + w[1], v[2] + w[2])


def dot(v, w):
    return v[0] * w[0] + v[1] * w[1] + v[2] * w[2]


def vec3(pos):
    return (pos.get("E", 0.0), pos.get("N", 0.0), pos.get("U", 0.0))


def rod_box_clearance(pos, axis, length, radius, center, half):
    """Exact clearance between an axis-aligned rod cylinder and an AABB."""
    ra = AXIS[axis]
    i_r = 0 if ra[0] else (1 if ra[1] else 2)
    lo = (center[0] - half[0], center[1] - half[1], center[2] - half[2])
    hi = (center[0] + half[0], center[1] + half[1], center[2] + half[2])
    a1 = pos[i_r] - length / 2
    a2 = pos[i_r] + length / 2
    if a2 < lo[i_r]:
        d_along = lo[i_r] - a2
    elif a1 > hi[i_r]:
        d_along = a1 - hi[i_r]
    else:
        d_along = 0.0
    d_perp2 = 0.0
    for i in range(3):
        if i == i_r:
            continue
        if pos[i] < lo[i]:
            d_perp2 += (pos[i] - lo[i]) ** 2
        elif pos[i] > hi[i]:
            d_perp2 += (pos[i] - hi[i]) ** 2
    return math.sqrt(d_along * d_along + d_perp2) - radius


def rod_cyl_clearance(pos, axis, length, radius, cpos, caxis, clength, cradius):
    """Exact clearance between two world-axis-aligned cylinders."""
    ra = AXIS[axis]
    ca = AXIS.get(caxis, (0.0, 0.0, 1.0))
    if ra == ca:
        i_r = 0 if ra[0] else (1 if ra[1] else 2)
        perp2 = 0.0
        for i in range(3):
            if i != i_r:
                perp2 += (pos[i] - cpos[i]) ** 2
        a1 = pos[i_r] - length / 2
        a2 = pos[i_r] + length / 2
        b1 = cpos[i_r] - clength / 2
        b2 = cpos[i_r] + clength / 2
        if a2 < b1:
            d_along = b1 - a2
        elif a1 > b2:
            d_along = a1 - b2
        else:
            d_along = 0.0
        return math.sqrt(perp2 + d_along * d_along) - radius - cradius
    # perpendicular axes: three separable coordinates
    i_r = 0 if ra[0] else (1 if ra[1] else 2)
    i_c = 0 if ca[0] else (1 if ca[1] else 2)
    d2 = 0.0
    for i in range(3):
        if i == i_r:
            gap = abs(cpos[i] - pos[i]) - length / 2
            d2 += max(0.0, gap) ** 2
        elif i == i_c:
            gap = abs(pos[i] - cpos[i]) - clength / 2
            d2 += max(0.0, gap) ** 2
        else:
            d2 += (pos[i] - cpos[i]) ** 2
    return math.sqrt(d2) - radius - cradius


def obstacle_from_el(el, tag):
    if el["pos"] is None:
        return None
    center = vec3(el["pos"])
    t = el["type"]
    d = el["dims"]
    lbl = (f"{tag} {t} " + " ".join(f"{k}={v:g}"
                                    for k, v in d.items()) +
           f" @ {center[0]:.1f},{center[1]:.1f},{center[2]:.1f}")
    if t == "BOX":
        half = (d.get("XLEN", 0.0) / 2, d.get("YLEN", 0.0) / 2,
                d.get("ZLEN", 0.0) / 2)
        return {"kind": "box", "center": center, "half": half, "label": lbl}
    if t in ("CYLINDER", "CONE"):
        if t == "CYLINDER":
            radius = d.get("DIAM", 0.0) / 2
            length = d.get("HEIG", 0.0)
        else:
            radius = max(d.get("DTOP", 0.0), d.get("DBOT", 0.0)) / 2
            length = d.get("HEIG", 0.0)
        z = el["ori"]["z"] if el["ori"] else "U"
        return {"kind": "cyl", "center": center, "axis": z,
                "length": length, "radius": radius, "label": lbl}
    return None


def rod_clearance(pos, axis, length, radius, obstacles):
    best = 1e9
    best_ob = None
    for ob in obstacles:
        if ob is None:
            continue
        if ob["kind"] == "box":
            dist = rod_box_clearance(pos, axis, length, radius,
                                     ob["center"], ob["half"])
        else:
            dist = rod_cyl_clearance(pos, axis, length, radius,
                                     ob["center"], ob["axis"],
                                     ob["length"], ob["radius"])
        if dist < best:
            best = dist
            best_ob = ob
    return best, best_ob


def rotate_about(axis, pos, center, theta_deg):
    """Rotate pos about the axis line through center by theta (RHR)."""
    d = sub(pos, center)
    th = math.radians(theta_deg)
    c, s = math.cos(th), math.sin(th)
    if axis == "N":
        e = d[0] * c - d[2] * s
        u = d[0] * s + d[2] * c
        return add(center, (e, d[1], u))
    if axis == "S":
        e = d[0] * c + d[2] * s
        u = -d[0] * s + d[2] * c
        return add(center, (e, d[1], u))
    if axis == "E":
        n = d[1] * c - d[2] * s
        u = d[1] * s + d[2] * c
        return add(center, (d[0], n, u))
    if axis == "W":
        n = d[1] * c + d[2] * s
        u = -d[1] * s + d[2] * c
        return add(center, (d[0], n, u))
    raise ValueError(axis)


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s != "-0" else "0"


# ---------------------------------------------------------------- main

CANDIDATES = [45.0, 50.0, 40.0, 55.0, 35.0, 60.0, 30.0]


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    src = argv[0] if len(argv) > 0 else r"C:\Users\A\Desktop\PUMP.txt"
    dst = argv[1] if len(argv) > 1 else None
    report_path = None
    if "--report" in sys.argv:
        report_path = sys.argv[sys.argv.index("--report") + 1]

    lines, root = parse(src)
    pumps = []
    for zone in root["children"]:
        if zone["type"] != "ZONE":
            continue
        for equi in zone["children"]:
            if equi["type"] == "EQUIPMENT":
                pumps.append(equi)

    edits = []
    report = []
    total_rods = 0

    for pump in pumps:
        tag = pump["name"].strip("/")
        subs = {}
        for c in pump["children"]:
            if c["type"] == "SUBEQUIPMENT":
                subs[c["name"].rsplit("_", 1)[-1]] = c
        casing = subs.get("CASING")
        if casing is None:
            report.append(f"{tag}: no CASING block")
            continue

        axis = None
        rods = []
        for el in casing["children"]:
            if el["type"] != "CYLINDER" or el["pos"] is None:
                continue
            if el["ori"] and el["ori"].get("y") == "U":
                if axis is None:
                    axis = el["ori"]["z"]
                if (el["ori"]["z"] == axis
                        and el["dims"].get("DIAM", 999) <= 21.0
                        and el["dims"].get("HEIG", 0) >= 90.0):
                    rods.append(el)
        if axis is None or not rods:
            report.append(f"{tag}: no axis/rods found")
            continue

        # axis point = centroid of the (symmetric) rod pattern
        center = (sum(vec3(r["pos"])[0] for r in rods) / len(rods),
                  sum(vec3(r["pos"])[1] for r in rods) / len(rods),
                  sum(vec3(r["pos"])[2] for r in rods) / len(rods))

        def in_plane_dist(pos):
            d = sub(pos, center)
            if axis in ("N", "S"):
                return math.hypot(d[0], d[2])
            return math.hypot(d[1], d[2])

        # obstacles: all pump solids except the rods, the casing barrel
        # stack and negative primitives
        obstacles = []

        def collect(el, in_casing):
            if el["type"] in ("CYLINDER", "CONE", "BOX") and el["pos"] is not None:
                if in_casing:
                    is_rod = el in rods
                    is_body = (el["type"] in ("CYLINDER", "CONE")
                               and el["ori"]
                               and el["ori"].get("z") == axis
                               and in_plane_dist(vec3(el["pos"])) < 2.0
                               and max(el["dims"].get("DIAM", 0),
                                       el["dims"].get("DTOP", 0),
                                       el["dims"].get("DBOT", 0)) >= 100.0)
                    if is_rod or is_body:
                        return
                ob = obstacle_from_el(el, tag)
                if ob is not None:
                    obstacles.append(ob)
            for ch in el.get("children", []):
                collect(ch, in_casing)

        for name, sub_el in subs.items():
            collect(sub_el, name == "CASING")

        # choose the rotation angle
        chosen = None
        forced = (len(rods) == 3)
        cands = [45.0] if forced else CANDIDATES
        tried = []
        for th in cands:
            ok = True
            min_cl = 1e9
            worst = None
            for rod in rods:
                new_pos = rotate_about(axis, vec3(rod["pos"]), center, th)
                cl, ob = rod_clearance(new_pos, axis, rod["dims"]["HEIG"],
                                       rod["dims"]["DIAM"] / 2, obstacles)
                if cl < min_cl:
                    min_cl = cl
                    worst = ob
                if cl < 3.0:
                    ok = False
                    tried.append((th, cl, ob["label"] if ob else "?"))
                    break
            if ok:
                chosen = (th, min_cl, worst)
                break
        if chosen is None:
            report.append(f"{tag}: NO clash-free angle among candidates "
                          f"({len(rods)} rods); details:")
            for th, cl, lbl in tried:
                report.append(f"    theta {th:g}: min clearance {cl:.1f} mm "
                              f"vs {lbl}")
            continue

        theta, min_cl, worst_ob = chosen
        total_rods += len(rods)
        report.append(f"{tag}: axis {axis}, {len(rods)} rods, "
                      f"theta=+{theta:g} CCW, min clearance {min_cl:.1f} mm"
                      + (f" vs {worst_ob['label']}" if worst_ob else ""))

        for rod in rods:
            old_pos = rod["pos"]
            new_vec = rotate_about(axis, vec3(old_pos), center, theta)
            ln = rod["line"]
            pos_line = lines[ln]  # 0-based -> line after NEW CYLINDER
            assert pos_line.strip().startswith("POS "), (tag, ln, pos_line)
            parts = {}
            for ax in ("E", "N", "U"):
                if ax in old_pos:
                    if ax == "E":
                        v = new_vec[0] if axis in ("N", "S") else old_pos["E"]
                    elif ax == "N":
                        v = new_vec[1] if axis in ("E", "W") else old_pos["N"]
                    else:
                        v = new_vec[2]
                    parts[ax] = f"{ax} {fmt(v)}mm"
            new_text = "POS " + " ".join(parts[ax] for ax in ("E", "N", "U")
                                         if ax in parts)
            edits.append((ln, pos_line.rstrip("\r\n"), new_text))

    if dst:
        out = list(lines)
        for ln, old, new in edits:
            assert out[ln - 1].rstrip("\r\n") == old, (ln, old)
            suffix = out[ln - 1][len(old):]
            out[ln - 1] = new + suffix
        with open(dst, "w", encoding="utf-8", newline="") as f:
            f.writelines(out)
        print(f"wrote {dst} ({len(edits)} POS lines changed, "
              f"{total_rods} rods)")

    if report_path:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report) + "\n")
        print(f"wrote report {report_path}")
    else:
        print("\n".join(report))


if __name__ == "__main__":
    main()
