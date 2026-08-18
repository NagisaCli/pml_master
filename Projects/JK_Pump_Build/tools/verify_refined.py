"""Numeric verification for JK_Pump_Build_refined_20260805.pml.

Checks:
- baseplates, nozzles and the trailing CATR pass unchanged vs the import;
- per-pump bridge bracket counts and bearing heights;
- hex nut seating on the washer/shand top;
- EXTRUSION structure (LOOP + 4/6 boundary vertices, balanced ENDs);
- nothing below U 0;
- targeted clash fixes leave no residual overlap;
- remaining large cross-SUBE overlaps are only intentional contact.
"""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# The native E3D export this verifier reads lives outside the repository, so it
# may be absent on another machine or after a cleanup. Override with argv[1];
# require_input() turns a missing file into a readable message rather than a
# bare FileNotFoundError traceback.
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\Users\A\Desktop\JK_PU.txt")
OUT = BASE / "output" / "JK_Pump_Build_refined_20260805_r8.pml"


def require_input(path: Path, what: str) -> Path:
    """Exit with an actionable message when an external input is absent."""
    if not path.exists():
        raise SystemExit(
            "Input not found: {0}\n"
            "  This script needs {1}.\n"
            "  That file is external to the repository and is not versioned.\n"
            "  Pass it explicitly:  python {2} <path>".format(
                path, what, Path(__file__).name
            )
        )
    return path

TYPES = (
    "CYLINDER", "CYLI", "NCYLINDER", "NCYLI", "NBOX",
    "CONE", "BOX", "NOZZLE", "EXTRUSION", "LOOP", "VERTEX", "PYRAMID",
)


def val(x: str) -> float:
    x = x.strip()
    for suffix in ("mm", "degC", "pascal", "degree"):
        if x.endswith(suffix):
            x = x[: -len(suffix)]
    return float(x)


def parse(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks: list[dict] = []
    stack: list[dict] = []
    cur_equi: str | None = None
    cur_sub: str | None = None
    for line in lines:
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
            b = {
                "type": raw,
                "name": m.group(2),
                "attrs": [s],
                "equi": cur_equi,
                "sub": cur_sub,
                "parent": stack[-1] if stack else None,
            }
            blocks.append(b)
            stack.append(b)
            continue
        if stack:
            if s:
                stack[-1]["attrs"].append(s)
            if re.match(r"^END\s*$", s, re.I):
                stack.pop()
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


def aabb(b: dict, ext_verts: dict[int, list[tuple[float, float]]]) -> tuple | None:
    pos, dims = pos_of(b), dims_of(b)
    if pos is None:
        return None
    t = b["type"]
    if t == "NCYLINDER":
        # NCYLI POS is LOCAL to its owner (PML-STUDY-NCYL-001, user verdict):
        # world centre = owner centre + local offset.
        parent = b.get("parent")
        base = (0.0, 0.0, 0.0)
        if parent is not None and pos_of(parent) is not None:
            base = pos_of(parent)
        pos = (pos[0] + base[0], pos[1] + base[1], pos[2] + base[2])
        t = "CYLINDER"
    if t == "BOX":
        x, y, z = dims["XLEN"] / 2, dims["YLEN"] / 2, dims["ZLEN"] / 2
        return (pos[0] - x, pos[1] - y, pos[2] - z, pos[0] + x, pos[1] + y, pos[2] + z)
    if t in ("CYLINDER", "NCYLINDER", "CONE"):
        r = (
            dims["DIAM"] / 2
            if t in ("CYLINDER", "NCYLINDER")
            else max(dims["DTOP"], dims["DBOT"]) / 2
        )
        h = dims["HEIG"] / 2
        e, n, u = pos
        z = {p[0]: p[1] for p in ori_of(b)}.get("Z", "U")
        if z in ("N", "S"):
            return (e - r, n - h, u - r, e + r, n + h, u + r)
        if z in ("E", "W"):
            return (e - h, n - r, u - r, e + h, n + r, u + r)
        return (e - r, n - r, u - h, e + r, n + r, u + h)
    if t == "PYRAMID":
        xb = dims.get("XBOT", 0) / 2
        yb = dims.get("YBOT", 0) / 2
        xt = dims.get("XTOP", 0) / 2
        yt = dims.get("YTOP", 0) / 2
        h = dims.get("HEIG", 0)
        xoff = dims.get("XOFF", 0)
        yoff = dims.get("YOFF", 0)
        x0 = min(pos[0] - xb, pos[0] + xoff - xt)
        x1 = max(pos[0] + xb, pos[0] + xoff + xt)
        y0 = min(pos[1] - yb, pos[1] + yoff - yt)
        y1 = max(pos[1] + yb, pos[1] + yoff + yt)
        return (x0, y0, pos[2], x1, y1, pos[2] + h)
    if t == "EXTRUSION":
        heig = dims.get("HEIG", 0.0)
        z = {p[0]: p[1] for p in ori_of(b)}.get("Z", "U")
        xs = [v[0] for v in ext_verts.get(id(b), [])]
        ys = [v[1] for v in ext_verts.get(id(b), [])]
        if not xs:
            return None
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        e, n, u = pos
        if z == "N":
            return (e + x0, n, u + y0, e + x1, n + heig, u + y1)
        if z == "S":
            return (e + x0, n - heig, u + y0, e + x1, n, u + y1)
        if z == "E":
            return (e, n + x0, u + y0, e + heig, n + x1, u + y1)
        if z == "W":
            return (e - heig, n + x0, u + y0, e, n + x1, u + y1)
        if z == "U":
            return (e + x0, n + y0, u, e + x1, n + y1, u + heig)
        return (e + x0, n + y0, u - heig, e + x1, n + y1, u)
    return None


def overlap(a: tuple, b: tuple) -> float:
    ov = 1.0
    for i in range(3):
        lo, hi = max(a[i], b[i]), min(a[i + 3], b[i + 3])
        if hi <= lo:
            return 0.0
        ov *= hi - lo
    return ov


def dilated(a: tuple, tol: float) -> tuple:
    return (a[0]-tol, a[1]-tol, a[2]-tol, a[3]+tol, a[4]+tol, a[5]+tol)


def main() -> int:
    require_input(SRC, "the native E3D export of the pump batch")
    a_blocks = parse(SRC)
    b_blocks = parse(OUT)

    # hierarchy balance: replay the INPUT block stack exactly as E3D parses it
    lines = OUT.read_text(encoding="utf-8", errors="replace").splitlines()
    stack: list[str] = []
    eq_ok = sube_ok = prim_ok = 0
    eq_bad = sube_bad = prim_bad = end_bad = 0
    for ln in lines:
        s = ln.strip()
        if s.upper().startswith("INPUT BEGIN"):
            stack.append("INPUT")
            continue
        if s.upper().startswith("INPUT END"):
            while stack and stack[-1] != "INPUT":
                stack.pop()
            if stack and stack[-1] == "INPUT":
                stack.pop()
            continue
        if s.upper().startswith("NEW ZONE"):
            stack.append("ZONE")
            continue
        if s.upper().startswith("NEW EQUIPMENT"):
            if stack and stack[-1] == "ZONE":
                eq_ok += 1
            else:
                eq_bad += 1
            stack.append("EQUI")
            continue
        if s.upper().startswith("NEW SUBEQUIPMENT"):
            if stack and stack[-1] == "EQUI":
                sube_ok += 1
            else:
                sube_bad += 1
            stack.append("SUBE")
            continue
        m = re.match(
            r"^NEW (BOX|CYLINDER|CYLI|CONE|NOZZLE|EXTRUSION|NCYLINDER|NCYLI|NBOX|PYRAMID)\b",
            s,
            re.I,
        )
        if m:
            if stack and stack[-1] in ("SUBE", "PRIM"):
                prim_ok += 1
            else:
                prim_bad += 1
            stack.append("PRIM")
            continue
        if s.upper().startswith("NEW LOOP"):
            if stack and stack[-1] == "PRIM":
                stack.append("LOOP")
            continue
        if s.upper().startswith("NEW VERTEX"):
            if stack and stack[-1] == "LOOP":
                stack.append("VERTEX")
            continue
        if s == "END":
            if stack and stack[-1] in ("INPUT",):
                end_bad += 1
            elif stack:
                stack.pop()
            else:
                end_bad += 1
    hierarchy_ok = (
        eq_bad == 0
        and sube_bad == 0
        and prim_bad == 0
        and end_bad == 0
        and eq_ok == 30
        and not stack
    )
    print(
        f"hierarchy: EQUI ok={eq_ok} bad={eq_bad}, SUBE ok={sube_ok} bad={sube_bad}, "
        f"PRIM ok={prim_ok} bad={prim_bad}, END bad={end_bad}, residual stack={stack}"
    )
    if not hierarchy_ok:
        print("HIERARCHY CHECK FAILED")

    print("== invariance ==")
    for label, pred in (
        ("baseplates", lambda b: b["sub"] and b["sub"].endswith("_BASEPLATE") and b["type"] == "BOX"),
        ("nozzles", lambda b: b["type"] == "NOZZLE"),
    ):
        sa = collections.Counter(geom_sig(b) for b in a_blocks if pred(b))
        sb = collections.Counter(geom_sig(b) for b in b_blocks if pred(b))
        print(f"{label}: identical={sa == sb} count={len(sb)}")

    def catr_pass(path: Path) -> list[str]:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, ln in enumerate(lines):
            if ln.strip().upper().startswith("OLD NOZZLE"):
                return lines[i:]
        return []

    print(f"CATR pass: identical={catr_pass(SRC) == catr_pass(OUT)}")

    # per-pump bridge counts
    by_sub: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for b in b_blocks:
        by_sub[(b["equi"], b["sub"])].append(b)
    bad = []
    hex_total = 0
    for (equi, sub), bs in sorted(by_sub.items()):
        if sub.endswith("_SUPPORT_FRAME") or sub.endswith("_DRIVER"):
            gussets = sum(1 for b in bs if b["type"] == "PYRAMID")
            if sub.endswith("_SUPPORT_FRAME") and gussets != 8:
                bad.append((equi, sub, gussets))
            if sub.endswith("_DRIVER") and gussets != 8:
                bad.append((equi, sub, gussets))
        if sub.endswith("_BASE_FASTENERS") or sub.endswith("_DRIVER_FASTENERS"):
            exts_sub = [b for b in bs if b["type"] == "EXTRUSION"]
            hex_total += sum(1 for k in range(1, len(exts_sub), 2))
    print(f"bridge gussets per pump: bad={bad or 'none'}")
    print(f"hex nuts total: {hex_total}")

    # EXTRUSION structure and vertex collection
    lines = OUT.read_text(encoding="utf-8", errors="replace").splitlines()
    depth = 0
    ext_owner: dict | None = None
    ext_verts: dict[int, list[tuple[float, float]]] = {}
    ext_bad = 0
    ext_count = 0
    for line in lines:
        s = line.strip()
        m = re.match(r"^NEW (EXTRUSION|LOOP|VERTEX)\b", s, re.I)
        if m and depth == 0:
            ext_owner = {"type": m.group(1).upper(), "verts": 0, "loops": 0}
            ext_verts[id(ext_owner)] = []
            depth = 1
            continue
        if m and depth > 0:
            if m.group(1).upper() == "VERTEX":
                ext_owner["verts"] += 1
                v = re.search(
                    r"POS ([EW])\s+([-\d.]+)[a-z]*\s+([NS])\s+([-\d.]+)[a-z]*\s+"
                    r"([UD])\s+([-\d.]+)[a-z]*",
                    s,
                    re.I,
                )
                if v:
                    x, y = val(v.group(2)), val(v.group(4))
                    if v.group(1).upper() == "W":
                        x = -x
                    if v.group(3).upper() == "S":
                        y = -y
                    ext_verts[id(ext_owner)].append((x, y))
            if m.group(1).upper() == "LOOP":
                ext_owner["loops"] += 1
            depth += 1
            continue
        if re.match(r"^END\s*$", s, re.I) and depth > 0:
            depth -= 1
            if depth == 0:
                ext_count += 1
                if ext_owner["loops"] != 1 or ext_owner["verts"] not in (4, 6, 8):
                    ext_bad += 1
                ext_owner = None
    print(f"EXTRUSION blocks: {ext_count}, bad structure: {ext_bad}")

    # rebuild with id-keyed verts by matching parse order
    blocks = b_blocks
    ext_ids = {id(b): i for i, b in enumerate(blocks) if b["type"] == "EXTRUSION"}
    vert_map: dict[int, list[tuple[float, float]]] = {}
    # collect vertices following each extrusion in parse order
    last_ext = None
    for b in blocks:
        if b["type"] == "EXTRUSION":
            last_ext = id(b)
            vert_map.setdefault(last_ext, [])
        elif b["type"] == "VERTEX" and last_ext is not None:
            v = None
            for a in b["attrs"]:
                m = re.match(
                    r"^POS ([EW])\s+([-\d.]+)[a-z]*\s+([NS])\s+([-\d.]+)[a-z]*\s+"
                    r"([UD])\s+([-\d.]+)[a-z]*$",
                    a,
                    re.I,
                )
                if m:
                    x, y = val(m.group(2)), val(m.group(4))
                    if m.group(1).upper() == "W":
                        x = -x
                    if m.group(3).upper() == "S":
                        y = -y
                    v = (x, y)
                    break
            if v:
                vert_map[last_ext].append(v)
        elif b["type"] not in ("LOOP", "VERTEX"):
            last_ext = None

    items = [
        (b, aabb(b, vert_map))
        for b in blocks
        if b["type"] not in ("NOZZLE", "NCYLINDER")
    ]
    items = [x for x in items if x[1] is not None]

    lo = min(
        x[1][2]
        for x in items
        if x[0]["type"] in ("BOX", "CYLINDER", "CONE", "EXTRUSION", "PYRAMID")
    )
    print(f"lowest point U: {lo:g}")

    # gusset/sole-plate contact: each gusset top touches its sole plate
    contact_bad = 0
    for (equi, sub), bs in by_sub.items():
        if not (sub.endswith("_SUPPORT_FRAME") or sub.endswith("_DRIVER")):
            continue
        gussets = [b for b in bs if b["type"] == "PYRAMID"]
        plates = [
            b for b in bs
            if b["type"] == "BOX"
            and 9.0 <= dims_of(b).get("ZLEN", 0) <= 17.0
            and pos_of(b)[2] > 90.0
        ]
        for g in gussets:
            ga = aabb(g, vert_map)
            ok = any(
                overlap(dilated(ga, 0.5), dilated(aabb(p, vert_map), 0.5)) > 0
                for p in plates
            )
            if not ok:
                contact_bad += 1
    print(f"gussets not touching any sole plate: {contact_bad}")

    # bearing-height preservation: old pad top == new sole plate top,
    # old pad bottom == new gusset bottom
    def old_pads(path: Path, sub_suffix: str) -> list[tuple]:
        blk = parse(path)
        out = []
        for b in blk:
            if b["sub"] and b["sub"].endswith(sub_suffix) and b["type"] == "BOX":
                d = dims_of(b)
                if sub_suffix == "_SUPPORT_FRAME":
                    xl, yl, zl = d.get("XLEN", 0), d.get("YLEN", 0), d.get("ZLEN", 0)
                    if max(xl, yl) <= 500 and min(xl, yl) > 50 and zl >= 40:
                        out.append((pos_of(b), d))
                else:
                    xl, yl, zl = d.get("XLEN", 0), d.get("YLEN", 0), d.get("ZLEN", 0)
                    u = pos_of(b)[2]
                    if 10 <= zl <= 35 and min(xl, yl) > 45 and u < 250:
                        out.append((pos_of(b), d))
        return out

    bearing_bad = 0
    for equi in sorted({b["equi"] for b in b_blocks}):
        for suffix in ("_SUPPORT_FRAME", "_DRIVER"):
            old = old_pads(SRC, suffix)
            old_this = [x for x in old if x[0] and equi in x[0] and False]
            # old_pads has no equi; rebuild per-equi
            old_this = []
            for b in parse(SRC):
                if b["equi"] == equi and b["sub"] and b["sub"].endswith(suffix) and b["type"] == "BOX":
                    d = dims_of(b)
                    xl, yl, zl = d.get("XLEN", 0), d.get("YLEN", 0), d.get("ZLEN", 0)
                    u = pos_of(b)[2]
                    if suffix == "_SUPPORT_FRAME":
                        if max(xl, yl) <= 500 and min(xl, yl) > 50 and zl >= 40:
                            old_this.append((pos_of(b), d))
                    elif 10 <= zl <= 35 and min(xl, yl) > 45 and u < 250:
                        old_this.append((pos_of(b), d))
            new_this = [b for b in b_blocks if b["equi"] == equi and b["sub"] and b["sub"].endswith(suffix)]
            for op, od in old_this:
                oe, on, ou = op
                oz = od["ZLEN"]
                plate = None
                guss = None
                for nb in new_this:
                    if nb["type"] == "BOX":
                        np_ = pos_of(nb)
                        nd = dims_of(nb)
                        if (
                            abs(np_[0] - oe) < 1.0
                            and abs(np_[1] - on) < 1.0
                            and 9.0 <= nd.get("ZLEN", 0) <= 17.0
                        ):
                            plate = (np_, nd)
                    if nb["type"] in ("EXTRUSION", "PYRAMID"):
                        np_ = pos_of(nb)
                        half = max(od["XLEN"], od["YLEN"]) / 2
                        if abs(np_[0] - oe) < half and abs(np_[1] - on) < half:
                            guss = nb
                if plate is None or guss is None:
                    bearing_bad += 1
                    continue
                old_top = ou + oz / 2
                new_top = plate[0][2] + plate[1]["ZLEN"] / 2
                ga = aabb(guss, vert_map)
                guss_top = ga[5] if ga is not None else None
                plate_bot = new_top - plate[1]["ZLEN"]
                if (
                    abs(old_top - new_top) > 0.5
                    or guss_top is None
                    or abs(guss_top - plate_bot) > 1.0
                ):
                    bearing_bad += 1
    print(f"bearing-height mismatches: {bearing_bad}")

    # hex nut seating: nut bottom on washer top or shank top
    nut_bad = 0
    nut_total = 0
    for (equi, sub), bs in by_sub.items():
        if not (sub.endswith("_BASE_FASTENERS") or sub.endswith("_DRIVER_FASTENERS")):
            continue
        cyls = [b for b in bs if b["type"] == "CYLINDER"]
        exts = [b for b in bs if b["type"] == "EXTRUSION"]
        for i in range(0, len(exts), 2):
            if i + 1 >= len(exts):
                break
            washer, nut = exts[i], exts[i + 1]
            nut_total += 1
            np_ = pos_of(nut)
            nd = dims_of(nut)
            # EXTRUSION POS is the profile end plane: for a Z=U nut that is
            # the bottom face, not the geometric centre.
            nut_bot = np_[2]
            wp_ = pos_of(washer)
            wd = dims_of(washer)
            washer_top = wp_[2] + wd.get("HEIG", 0)
            shank = cyls[i // 2] if i // 2 < len(cyls) else None
            shank_top = None
            if shank is not None:
                sp_ = pos_of(shank)
                sd = dims_of(shank)
                shank_top = sp_[2] + sd.get("HEIG", 0) / 2
            seated = abs(nut_bot - washer_top) < 1.0
            if shank_top is not None and abs(nut_bot - shank_top) < 1.0:
                seated = True
            if not seated:
                nut_bad += 1
    print(f"hex nuts: {nut_total}, not seated on washer/shank: {nut_bad}")

    # MC_AUXILIARY subequipment removed
    mc_left = [b for b in b_blocks if b["sub"] and b["sub"].endswith("_MC_AUXILIARY")]
    print(f"MC_AUXILIARY blocks remaining: {len(mc_left)}")

    # negative-cylinder holes
    ncylis = [b for b in b_blocks if b["type"] == "NCYLINDER"]
    ncyli_bad = 0
    ncyli_noflag = 0
    for n in ncylis:
        if not any(a.upper().startswith("NAPPFLAG") for a in n["attrs"]):
            ncyli_noflag += 1
        parent = n.get("parent")
        if parent is None or parent["type"] != "BOX":
            ncyli_bad += 1
            continue
        # Hole containment: the circle perpendicular to the stub axis must
        # stay fully inside the plate (closed hole, no open edge).
        np_ = pos_of(n)
        nd = dims_of(n)
        pp = pos_of(parent)
        pd = dims_of(parent)
        z_axis = None
        for a in n["attrs"]:
            m = re.match(r"^ORI\s+.*?\bZ\s+is\s+([EWNSUD])\b", a, re.I)
            if m:
                z_axis = m.group(1).upper()
                break
        norm = {"E": "E", "W": "E", "N": "N", "S": "N"}.get(z_axis)
        r = nd.get("DIAM", 0) / 2
        if norm == "E":
            radial_u = abs(np_[2])
            radial_2 = abs(np_[1])
            half_2 = pd.get("YLEN", 0) / 2
        else:
            radial_u = abs(np_[2])
            radial_2 = abs(np_[0])
            half_2 = pd.get("XLEN", 0) / 2
        u_ok = radial_u + r <= pd.get("ZLEN", 0) / 2 + 0.5
        r2_ok = radial_2 + r <= half_2 + 0.5
        if not (u_ok and r2_ok):
            ncyli_bad += 1
    # no leftover gland stub at the plate centre
    leftover = 0
    for b in b_blocks:
        if b["sub"] and b["sub"].endswith("_DRIVER") and b["type"] == "BOX":
            bp = pos_of(b)
            if bp is None:
                continue
            same = [
                c for c in b_blocks
                if c["sub"] == b["sub"] and c["type"] == "CYLINDER"
                and pos_of(c) is not None
                and abs(pos_of(c)[0] - bp[0]) < 1.0
                and abs(pos_of(c)[1] - bp[1]) < 1.0
            ]
            if len(same) > 0:
                # only BOX 21 is expected to have no matching stub left
                boxes = [x for x in b_blocks if x["sub"] == b["sub"] and x["type"] == "BOX"]
                if boxes and b is boxes[20]:
                    leftover += len(same)
    print(
        f"NCYLINDER holes: {len(ncylis)}, open/out-of-plate: {ncyli_bad}, "
        f"missing NAPPFLAG: {ncyli_noflag}, "
        f"leftover stubs at BOX21: {leftover}"
    )

    # footprint protrusions beyond baseplate AABB (delta vs source)
    def baseplate_aabb(path: Path) -> dict[str, tuple]:
        blk = parse(path)
        out = {}
        for b in blk:
            if b["sub"] and b["sub"].endswith("_BASEPLATE") and b["type"] == "BOX":
                p = pos_of(b)
                d = dims_of(b)
                out[b["equi"]] = (
                    p[0] - d["XLEN"] / 2, p[1] - d["YLEN"] / 2, p[2] - d["ZLEN"] / 2,
                    p[0] + d["XLEN"] / 2, p[1] + d["YLEN"] / 2, p[2] + d["ZLEN"] / 2,
                )
        return out

    def protrusions(path: Path, ext_map: dict) -> list[tuple]:
        blk = parse(path)
        bp = baseplate_aabb(path)
        out = []
        for b in blk:
            if b["type"] == "NOZZLE" or not b["sub"]:
                continue
            bb = aabb(b, ext_map) if b["type"] == "EXTRUSION" else aabb(b, {})
            if bb is None or b["equi"] not in bp:
                continue
            bx = bp[b["equi"]]
            over = []
            if bb[0] < bx[0] - 1:
                over.append(("E-", bx[0] - bb[0]))
            if bb[1] < bx[1] - 1:
                over.append(("N-", bx[1] - bb[1]))
            if bb[3] > bx[3] + 1:
                over.append(("E+", bb[3] - bx[3]))
            if bb[4] > bx[4] + 1:
                over.append(("N+", bb[4] - bx[4]))
            if over:
                out.append((b["equi"], b["sub"], over, " ".join(x for x in b["attrs"] if x and not x.startswith(("NEW", "--")))[:110]))
        return out

    src_pro = protrusions(SRC, {})
    out_pro = protrusions(OUT, vert_map)
    added = [x for x in out_pro if x not in src_pro]
    removed = [x for x in src_pro if x not in out_pro]
    print(f"footprint protrusions: source {len(src_pro)}, output {len(out_pro)}, added {len(added)}, removed {len(removed)}")
    for x in added[:10]:
        print("   +", x)
    for x in removed[:5]:
        print("   -", x)

    # targeted clash pairs
    def check(equi: str, subs: tuple[str, str], minvol: float = 1000.0) -> None:
        pairs = []
        worst = 0.0
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                b1, a1 = items[i]
                b2, a2 = items[j]
                if b1["equi"] != equi:
                    continue
                if not (
                    (b1["sub"].endswith(subs[0]) and b2["sub"].endswith(subs[1]))
                    or (b1["sub"].endswith(subs[1]) and b2["sub"].endswith(subs[0]))
                ):
                    continue
                v = overlap(a1, a2)
                if v >= minvol:
                    pairs.append((v, b1["sub"], b2["sub"]))
                    worst = max(worst, v)
        print(f"{equi} {subs}: pairs>= {minvol:g} -> {len(pairs)}, worst {worst:,.0f}")
        for v, s1, s2 in sorted(pairs, reverse=True)[:3]:
            print(f"    {v:,.0f}  {s1} x {s2}")

    check("/205_PU_054", ("MC_AUXILIARY", "CASING"))
    check("/205_PU_054", ("MC_AUXILIARY", "SUPPORT_FRAME"))
    check("/205_PU_054", ("MC_AUXILIARY", "CASING_FASTENERS"))
    check("/205_PU_054", ("MC_AUXILIARY", "DISCHARGE"))
    check("/205_PU_054", ("MC_AUXILIARY", "BASE_FASTENERS"))
    check("/205_PU_038", ("MC_AUXILIARY", "SUPPORT_FRAME"))
    check("/205_PU_060", ("SERVICE_DETAILS", "CASING"))
    check("/205_PU_061", ("SERVICE_DETAILS", "CASING"))

    # remaining large cross-SUBE overlaps (>= 100k) outside same-SUBE self-contact
    big: collections.Counter = collections.Counter()
    maxv: dict = {}
    example: dict = {}
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            b1, a1 = items[i]
            b2, a2 = items[j]
            if b1["equi"] != b2["equi"] or b1["sub"] == b2["sub"]:
                continue
            v = overlap(a1, a2)
            if v < 100000:
                continue
            k1 = b1["sub"].rsplit("_", 2)[-1]
            k2 = b2["sub"].rsplit("_", 2)[-1]
            key = (k1, k2) if k1 <= k2 else (k2, k1)
            big[key] += 1
            if v > maxv.get(key, 0):
                maxv[key] = v
                example[key] = (b1["equi"], b1["sub"], b2["sub"])
    print("\nremaining cross-SUBE overlaps >= 100,000 mm3:")
    for key, c in big.most_common():
        print(
            f"  {key[0]:14s}x{key[1]:14s} n={c:3d} max={maxv[key]:12,.0f} "
            f"@ {example[key][0]} ({example[key][1].rsplit('_',2)[-1]}/{example[key][2].rsplit('_',2)[-1]})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
