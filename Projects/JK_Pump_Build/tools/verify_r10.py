"""Numeric verification for JK_Pump_Build_refined_20260805_r10.pml.

r10 rebuilds every pump base to the DBOutput.txt (P1502B / PUMP006) style
with physical support logic: 5-member longitudinal frame, pump-end stand
(2 side plates carrying a pump-end sole plate + cross-beam EXTRUSION),
large+small PYRAMID gussets per foot/pad, and 2 through-foot anchors per
foot/pad (shank + hex washer + hex nut). Nothing floats: every element's
bottom face is carried by the element below, and every stand is emitted
only when its full stack fits. Everything outside the base scope must be
byte-identical to r8.
"""

from __future__ import annotations

import collections
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

R8 = BASE / "output" / "JK_Pump_Build_refined_20260805_r8.pml"
R10 = BASE / "output" / "JK_Pump_Build_refined_20260805_r10.pml"

TYPES = (
    "CYLINDER", "CYLI", "NCYLINDER", "NCYLI", "NBOX",
    "CONE", "BOX", "NOZZLE", "EXTRUSION", "LOOP", "VERTEX", "PYRAMID",
)


def val(x: str) -> float:
    x = x.strip()
    for suffix in ("mm", "degC", "pascal", "degree"):
        if x.lower().endswith(suffix):
            x = x[: -len(suffix)]
    return float(x)


def parse(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks: list[dict] = []
    cur: dict | None = None
    cur_equi: str | None = None
    cur_sub: str | None = None
    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r"^NEW (EQUIPMENT|EQUI)\s+(\S+)", s, re.I)
        if m:
            cur_equi = m.group(2)
            cur_sub = None
            continue
        m = re.match(r"^NEW (SUBEQUIPMENT|SUBE)\s+(\S+)", s, re.I)
        if m:
            cur_sub = m.group(2)
            continue
        m = re.match(r"^NEW (" + "|".join(TYPES) + r")\b(?:\s+(\S+))?", s, re.I)
        if m:
            raw = m.group(1).upper()
            if raw == "CYLI":
                raw = "CYLINDER"
            elif raw == "NCYLI":
                raw = "NCYLINDER"
            blocks.append({
                "type": raw,
                "name": m.group(2) or "",
                "attrs": [s],
                "equi": cur_equi,
                "sub": cur_sub,
                "start": i,
            })
            cur = blocks[-1]
            continue
        if cur is not None:
            if re.match(r"^END\s*$", s, re.I):
                cur["end"] = i
                cur = None
            elif s:
                cur["attrs"].append(s)
    return blocks


def pos_of(b: dict) -> tuple[float, float, float] | None:
    for a in b["attrs"]:
        m = re.match(
            r"^POS ([EW])\s+([-\d.]+)[a-z]*\s+([NS])\s+([-\d.]+)[a-z]*\s+"
            r"([UD])\s+([-\d.]+)[a-z]*$",
            a,
            re.I,
        )
        if m:
            e, n, u = val(m.group(2)), val(m.group(4)), val(m.group(6))
            if m.group(1).upper() == "W":
                e = -e
            if m.group(3).upper() == "S":
                n = -n
            if m.group(5).upper() == "D":
                u = -u
            return (e, n, u)
    return None


def ori_of(b: dict) -> tuple[tuple[str, str], ...]:
    for a in b["attrs"]:
        m = re.match(r"^ORI\s+(.*)$", a, re.I)
        if m:
            return tuple(
                sorted(
                    (p1.upper(), p2.upper())
                    for p1, p2 in re.findall(r"([XYZS])\s+is\s+([EWNSUD])", m.group(1), re.I)
                )
            )
    return ()


def dims_of(b: dict) -> dict[str, float]:
    d: dict[str, float] = {}
    for a in b["attrs"]:
        m = re.match(r"^([A-Z]+)\s+(.+)$", a, re.I)
        if m and m.group(1).upper() in (
            "DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "DTOP", "DBOT",
            "XBOT", "YBOT", "XTOP", "YTOP", "XOFF", "YOFF",
        ):
            d[m.group(1).upper()] = val(m.group(2))
    return d


def geom_sig(b: dict) -> tuple:
    return (
        b["type"],
        b["name"] or "",
        pos_of(b),
        ori_of(b),
        tuple(sorted(dims_of(b).items())),
    )


def ext_vertices(blocks: list[dict]) -> dict[int, list[tuple[float, float, float]]]:
    out: dict[int, list[tuple[float, float, float]]] = {}
    cur = None
    for b in blocks:
        if b["type"] == "EXTRUSION":
            cur = id(b)
            out[cur] = []
        elif b["type"] == "VERTEX" and cur is not None:
            v = pos_of(b)
            if v is not None:
                out[cur].append(v)
        elif b["type"] not in ("LOOP",):
            cur = None
    return out


def aabb(b: dict, verts: dict[int, list[tuple[float, float]]]) -> tuple | None:
    pos, d = pos_of(b), dims_of(b)
    if pos is None:
        return None
    t = b["type"]
    if t == "BOX":
        x, y, z = d["XLEN"] / 2, d["YLEN"] / 2, d["ZLEN"] / 2
        return (pos[0]-x, pos[1]-y, pos[2]-z, pos[0]+x, pos[1]+y, pos[2]+z)
    if t == "CYLINDER":
        r, h = d["DIAM"] / 2, d["HEIG"] / 2
        e, n, u = pos
        z = {p[0]: p[1] for p in ori_of(b)}.get("Z", "U")
        if z in ("N", "S"):
            return (e-r, n-h, u-r, e+r, n+h, u+r)
        if z in ("E", "W"):
            return (e-h, n-r, u-r, e+h, n+r, u+r)
        return (e-r, n-r, u-h, e+r, n+r, u+h)
    if t == "PYRAMID":
        xb, yb = d.get("XBOT", 0) / 2, d.get("YBOT", 0) / 2
        xt, yt = d.get("XTOP", 0) / 2, d.get("YTOP", 0) / 2
        h = d.get("HEIG", 0)
        xo, yo = d.get("XOFF", 0), d.get("YOFF", 0)
        return (
            min(pos[0]-xb, pos[0]+xo-xt), min(pos[1]-yb, pos[1]+yo-yt), pos[2],
            max(pos[0]+xb, pos[0]+xo+xt), max(pos[1]+yb, pos[1]+yo+yt), pos[2]+h,
        )
    if t == "EXTRUSION":
        heig = d.get("HEIG", 0.0)
        z = {p[0]: p[1] for p in ori_of(b)}.get("Z", "U")
        vs = verts.get(id(b), [])
        if not vs:
            return None
        e, n, u = pos
        ve = [v[0] for v in vs]
        vn = [v[1] for v in vs]
        vu = [v[2] for v in vs]
        if z in ("E", "W"):
            return (
                e - heig if z == "W" else e,
                n + min(vn), u + min(vu),
                e if z == "W" else e + heig,
                n + max(vn), u + max(vu),
            )
        if z in ("N", "S"):
            return (
                e + min(ve), n - heig if z == "S" else n, u + min(vu),
                e + max(ve), n if z == "S" else n + heig, u + max(vu),
            )
        if z == "D":
            return (e + min(ve), n + min(vn), u - heig,
                    e + max(ve), n + max(vn), u)
        return (e + min(ve), n + min(vn), u,
                e + max(ve), n + max(vn), u + heig)
    return None


def overlap(a: tuple, b: tuple, tol: float = 0.0) -> float:
    v = 1.0
    for i in range(3):
        lo, hi = max(a[i], b[i]), min(a[i+3], b[i+3])
        if hi - lo <= tol:
            return 0.0
        v *= hi - lo
    return v


def main() -> int:
    a_blocks = parse(R8)
    b_blocks = parse(R10)
    verts = ext_vertices(b_blocks)
    by_sub: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for b in b_blocks:
        by_sub[(b["equi"], b["sub"])].append(b)

    fails: list[str] = []

    # ---- hierarchy replay ----
    lines = R10.read_text(encoding="utf-8", errors="replace").splitlines()
    stack: list[str] = []
    eq_ok = sube_ok = prim_ok = 0
    eq_bad = sube_bad = prim_bad = end_bad = 0
    for ln in lines:
        s = ln.strip()
        if s.upper().startswith("INPUT BEGIN"):
            stack.append("INPUT")
        elif s.upper().startswith("INPUT END"):
            while stack and stack[-1] != "INPUT":
                stack.pop()
            if stack and stack[-1] == "INPUT":
                stack.pop()
        elif s.upper().startswith("NEW ZONE"):
            stack.append("ZONE")
        elif s.upper().startswith("NEW EQUIPMENT"):
            if stack and stack[-1] == "ZONE":
                eq_ok += 1
            else:
                eq_bad += 1
            stack.append("EQUI")
        elif s.upper().startswith("NEW SUBEQUIPMENT"):
            if stack and stack[-1] == "EQUI":
                sube_ok += 1
            else:
                sube_bad += 1
            stack.append("SUBE")
        elif re.match(r"^NEW (BOX|CYLINDER|CYLI|CONE|NOZZLE|EXTRUSION|NCYLINDER|NCYLI|NBOX|PYRAMID)\b", s, re.I):
            if stack and stack[-1] in ("SUBE", "PRIM"):
                prim_ok += 1
            else:
                prim_bad += 1
            stack.append("PRIM")
        elif s.upper().startswith("NEW LOOP"):
            if stack and stack[-1] == "PRIM":
                stack.append("LOOP")
        elif s.upper().startswith("NEW VERTEX"):
            if stack and stack[-1] == "LOOP":
                stack.append("VERTEX")
        elif s == "END":
            if stack and stack[-1] == "INPUT":
                end_bad += 1
            elif stack:
                stack.pop()
            else:
                end_bad += 1
    if not (eq_bad == 0 and sube_bad == 0 and prim_bad == 0 and end_bad == 0
            and eq_ok == 30 and not stack):
        fails.append(
            f"hierarchy: eq {eq_ok}/{eq_bad} sub {sube_ok}/{sube_bad} "
            f"prim {prim_ok}/{prim_bad} end {end_bad} residual {stack}"
        )
    else:
        print(f"hierarchy OK (30 EQUI / {sube_ok} SUBE / {prim_ok} PRIM)")

    # ---- invariance vs r8 ----
    def sig(b: dict) -> tuple:
        return (b["type"], b["name"], b["equi"], b["sub"], tuple(b["attrs"]))

    def base_scope(b: dict) -> bool:
        s = b["sub"] or ""
        if s.endswith(("_SUPPORT_FRAME", "_BASE_FASTENERS", "_DRIVER_FASTENERS")):
            return True
        if s.endswith("_DRIVER") and b["type"] in ("PYRAMID", "EXTRUSION", "LOOP", "VERTEX"):
            return True
        if s.endswith("_DRIVER") and b["type"] == "BOX":
            p, d = pos_of(b), dims_of(b)
            return bool(p and 9 <= d.get("ZLEN", 0) <= 17 and 90 < p[2] < 300)
        return False

    ca = collections.Counter(sig(b) for b in a_blocks if not base_scope(b))
    cb = collections.Counter(sig(b) for b in b_blocks if not base_scope(b))
    if ca != cb:
        only = [k for k in ca if cb.get(k, 0) != ca[k]] + [k for k in cb if ca.get(k, 0) != cb[k]]
        fails.append(f"non-base blocks differ: {len(only)} (first: {only[0][:3] if only else None})")
    else:
        print(f"non-base invariance OK ({sum(ca.values())} blocks identical to r8)")

    for label, pred in (
        ("baseplates", lambda b: b["sub"] and b["sub"].endswith("_BASEPLATE") and b["type"] == "BOX"),
        ("nozzles", lambda b: b["type"] == "NOZZLE"),
    ):
        sa = collections.Counter(geom_sig(b) for b in a_blocks if pred(b))
        sb = collections.Counter(geom_sig(b) for b in b_blocks if pred(b))
        if sa != sb:
            fails.append(f"{label} changed")
    print("baseplates/nozzles: identical to r8" if not any("baseplates" in f or "nozzles" in f for f in fails) else "baseplates/nozzles CHANGED")

    def catr(path: Path) -> list[str]:
        ls = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, ln in enumerate(ls):
            if ln.strip().upper().startswith("OLD NOZZLE"):
                return ls[i:]
        return []
    if catr(R8) != catr(R10):
        fails.append("CATR pass changed")

    # ---- per-pump base structure ----
    ncyli = 0
    ncyli_flag = 0
    for ln in lines:
        if re.match(r"^NEW NCYLINDER\b", ln.strip(), re.I):
            ncyli += 1
        if "NAPPFLAG 2" in ln:
            ncyli_flag += 1
    if ncyli != 30 or ncyli_flag != 30:
        fails.append(f"NCYLI: {ncyli} holes / {ncyli_flag} NAPPFLAG")

    per_pump_bad: list[str] = []
    for equi in sorted({b["equi"] for b in b_blocks}):
        sf = by_sub[(equi, equi + "_SUPPORT_FRAME")]
        dr = by_sub[(equi, equi + "_DRIVER")]
        bf = by_sub[(equi, equi + "_BASE_FASTENERS")]
        df = by_sub[(equi, equi + "_DRIVER_FASTENERS")]
        bp = by_sub[(equi, equi + "_BASEPLATE")]
        base_top = max(pos_of(b)[2] + dims_of(b)["ZLEN"] / 2 for b in bp if b["type"] == "BOX")

        boxes = [b for b in sf if b["type"] == "BOX"]
        rails = [b for b in boxes if abs(dims_of(b).get("ZLEN", 0) - 20) < 0.01
                 and max(dims_of(b).get("XLEN", 0), dims_of(b).get("YLEN", 0)) > 500]
        remaining = [b for b in boxes if b not in rails]
        if rails:
            rd = dims_of(rails[0])
            n_long = rd.get("YLEN", 0) >= rd.get("XLEN", 0)
        else:
            n_long = True
        def t_of(b: dict) -> float:
            p = pos_of(b)
            return p[0] if n_long else p[1]
        plate_like = [b for b in remaining if 9 <= dims_of(b).get("ZLEN", 0) <= 17]
        if plate_like:
            t_mid = (min(t_of(b) for b in plate_like) + max(t_of(b) for b in plate_like)) / 2
            pump_plate = [b for b in plate_like if abs(t_of(b) - t_mid) < 1.0]
            pump_plate.sort(key=lambda b: dims_of(b).get("XLEN", 0) + dims_of(b).get("YLEN", 0), reverse=True)
            if len(pump_plate) == 1:
                plate_box = pump_plate[0]
                soles = [b for b in plate_like if b is not plate_box]
            else:
                plate_box = pump_plate[0] if pump_plate else None
                soles = [b for b in plate_like if b is not plate_box]
        else:
            plate_box = None
            soles = []
        side = [b for b in remaining if b not in plate_like]
        pyr_sf = [b for b in sf if b["type"] == "PYRAMID"]
        pads = [b for b in dr if b["type"] == "BOX" and 9 <= dims_of(b).get("ZLEN", 0) <= 17
                and 90 < pos_of(b)[2] < 300]
        pyr_dr = [b for b in dr if b["type"] == "PYRAMID"]
        beam = [b for b in sf if b["type"] == "EXTRUSION"]

        if len(rails) != 5:
            per_pump_bad.append(f"{equi}: frame members {len(rails)} != 5")
        for r in rails:
            p, d = pos_of(r), dims_of(r)
            if abs(p[2] - d["ZLEN"] / 2 - base_top) > 0.51:
                per_pump_bad.append(f"{equi}: frame member not seated")
        has_stand = len(side) > 0 or beam or plate_box is not None
        if has_stand:
            if len(side) != 2 or len(beam) != 1 or plate_box is None:
                per_pump_bad.append(
                    f"{equi}: incomplete stand (side {len(side)}/beam {len(beam)}/plate {plate_box is not None})"
                )
            else:
                # frame longitudinal extent (rails)
                rp = [pos_of(r) for r in rails]
                if n_long:
                    f0, f1 = min(p[1] for p in rp) - dims_of(rails[0])["YLEN"] / 2, \
                             max(p[1] for p in rp) + dims_of(rails[0])["YLEN"] / 2
                else:
                    f0, f1 = min(p[0] for p in rp) - dims_of(rails[0])["XLEN"] / 2, \
                             max(p[0] for p in rp) + dims_of(rails[0])["XLEN"] / 2
                for b in side:
                    p, d = pos_of(b), dims_of(b)
                    if abs(p[2] - d["ZLEN"] / 2 - (base_top + 20)) > 0.51:
                        per_pump_bad.append(f"{equi}: side plate not seated on frame")
                    if n_long:
                        lo_, hi_ = p[1] - d["YLEN"] / 2, p[1] + d["YLEN"] / 2
                    else:
                        lo_, hi_ = p[0] - d["XLEN"] / 2, p[0] + d["XLEN"] / 2
                    if lo_ < f0 - 2.0 or hi_ > f1 + 2.0:
                        per_pump_bad.append(f"{equi}: side plate outside frame")
                sp = pos_of(plate_box)
                sd = dims_of(plate_box)
                plate_bottom = sp[2] - sd["ZLEN"] / 2
                if n_long:
                    plo, phi = sp[1] - sd["YLEN"] / 2, sp[1] + sd["YLEN"] / 2
                else:
                    plo, phi = sp[0] - sd["XLEN"] / 2, sp[0] + sd["XLEN"] / 2
                if plo < f0 - 2.0 or phi > f1 + 2.0:
                    per_pump_bad.append(f"{equi}: pump-end plate outside frame")
                for b in side:
                    p, d = pos_of(b), dims_of(b)
                    if abs(p[2] + d["ZLEN"] / 2 - plate_bottom) > 0.51:
                        per_pump_bad.append(f"{equi}: side plate top != pump-end plate bottom")
                if soles:
                    sole_top_ref = max(pos_of(s)[2] + dims_of(s)["ZLEN"] / 2 for s in soles)
                    if abs(sp[2] + sd["ZLEN"] / 2 - sole_top_ref) > 0.51:
                        per_pump_bad.append(f"{equi}: pump-end plate top != foot sole top")
        if len(pyr_sf) != 8:
            per_pump_bad.append(f"{equi}: pump gussets {len(pyr_sf)} != 8")
        if len(pyr_dr) != 8:
            per_pump_bad.append(f"{equi}: motor gussets {len(pyr_dr)} != 8")
        for g in pyr_sf + pyr_dr:
            p, d = pos_of(g), dims_of(g)
            if abs(p[2] - (base_top + 20)) > 0.51:
                per_pump_bad.append(f"{equi}: gusset bottom != frame top")
            top = p[2] + d.get("HEIG", 0)
            targets = soles if g in pyr_sf else pads
            if not any(abs(pos_of(x)[2] - dims_of(x)["ZLEN"] / 2 - top) < 0.51 for x in targets):
                per_pump_bad.append(f"{equi}: gusset top floating ({top:g})")
        # anchors: 8 + 8 (2 per foot/pad), each shank+washer+nut
        for name, bs_, pads_ in (("BASE", bf, soles), ("DRIVER", df, pads)):
            sh = [b for b in bs_ if b["type"] == "CYLINDER"]
            ex = [b for b in bs_ if b["type"] == "EXTRUSION"]
            if len(sh) != 8 or len(ex) != 16:
                per_pump_bad.append(f"{equi}: {name} anchors {len(sh)} shanks/{len(ex)} hexes")
                continue
            for k in range(8):
                wp = pos_of(ex[2*k])
                np_ = pos_of(ex[2*k+1])
                sp = pos_of(sh[k])
                sd = dims_of(sh[k])
                nd = dims_of(ex[2*k+1])
                if abs(wp[2] - base_top) > 0.51:
                    per_pump_bad.append(f"{equi}: {name} washer not on baseplate top")
                # find the foot/pad that contains this anchor in plan
                pad = min(pads_, key=lambda b: (
                    (pos_of(b)[0] - sp[0]) ** 2 + (pos_of(b)[1] - sp[1]) ** 2
                ))
                sole_top = pos_of(pad)[2] + dims_of(pad)["ZLEN"] / 2
                if abs(np_[2] - sole_top) > 0.51:
                    per_pump_bad.append(f"{equi}: {name} nut not on sole/pad top")
                if abs(sp[2] + sd["HEIG"] / 2 - (np_[2] + nd["HEIG"])) > 0.51:
                    per_pump_bad.append(f"{equi}: {name} shank top != nut top")
                if sp[2] - sd["HEIG"] / 2 < 40.0:
                    per_pump_bad.append(f"{equi}: {name} shank bottom too low")
                # anchor must lie inside its foot/pad in plan
                pp = pos_of(pad)
                pd = dims_of(pad)
                inside = (abs(sp[0] - pp[0]) <= pd["XLEN"] / 2 + 0.51
                          and abs(sp[1] - pp[1]) <= pd["YLEN"] / 2 + 0.51)
                if not inside:
                    per_pump_bad.append(f"{equi}: {name} anchor outside foot/pad")
                va = aabb(ex[2*k], verts)
                if va and max(va[3] - va[0], va[4] - va[1]) > 200.0:
                    per_pump_bad.append(f"{equi}: {name} hex oversized")
        # stand vs feet/gussets/casing clash
        stand_boxes = side + ([beam[0]] if beam else []) + ([plate_box] if plate_box is not None else [])
        stand_a = [aabb(b, verts) for b in stand_boxes]
        stand_a = [x for x in stand_a if x]
        others = [b for b in sf if b["type"] == "BOX" and b in soles] + pyr_sf
        others += [b for b in by_sub[(equi, equi + "_CASING")] if b["type"] in ("BOX", "CYLINDER", "CONE")]
        others += [b for b in by_sub[(equi, equi + "_CASING_FASTENERS")] if b["type"] in ("BOX", "CYLINDER")]
        for sa_ in stand_a:
            for ob in others:
                oa = aabb(ob, verts)
                if oa and overlap(sa_, oa, tol=1.0) > 200.0:
                    per_pump_bad.append(f"{equi}: stand x {ob['sub'].rsplit('_', 1)[-1]} clash")
                    break

    if per_pump_bad:
        fails.append("per-pump issues: " + "; ".join(dict.fromkeys(per_pump_bad))[:1200])
    else:
        print("per-pump base structure OK (5-member frame, stand, gussets, 8+8 anchors, no stand clash)")

    # ---- lowest point ----
    items = [(b, aabb(b, verts)) for b in b_blocks if b["type"] not in ("NOZZLE",)]
    items = [x for x in items if x[1] is not None]
    lo = min(x[1][2] for x in items if x[0]["type"] in ("BOX", "CYLINDER", "CONE", "EXTRUSION", "PYRAMID"))
    print(f"lowest point U: {lo:g}")
    if lo < -0.01:
        fails.append("geometry below U 0")

    # ---- EXTRUSION structure ----
    ext_bad = 0
    ext_n = 0
    depth = 0
    owner = None
    for ln in lines:
        s = ln.strip()
        m = re.match(r"^NEW (EXTRUSION|LOOP|VERTEX)\b", s, re.I)
        if m and depth == 0:
            owner = {"loops": 0, "verts": 0}
            depth = 1
            continue
        if m and depth > 0:
            if m.group(1).upper() == "LOOP":
                owner["loops"] += 1
            if m.group(1).upper() == "VERTEX":
                owner["verts"] += 1
            depth += 1
            continue
        if s == "END" and depth > 0:
            depth -= 1
            if depth == 0:
                ext_n += 1
                if owner["loops"] != 1 or owner["verts"] not in (4, 6):
                    ext_bad += 1
                owner = None
    print(f"EXTRUSION blocks: {ext_n}, bad structure: {ext_bad}")
    if ext_bad:
        fails.append("EXTRUSION structure errors")

    print()
    if fails:
        print("FAILURES:")
        for f in fails:
            print(" -", f)
        return 1
    print("ALL r10 CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
