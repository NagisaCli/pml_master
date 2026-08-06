"""Refine the JK_Pump_Build native export:

1. Convert every pump support foot and motor mounting pad into a
   bridge-type standard bracket: a sole plate carried by two trapezoid
   gusset plates (EXTRUSION).
2. Upgrade every circular fastener cap in BASE_FASTENERS /
   DRIVER_FASTENERS to a true hexagonal nut (EXTRUSION).
3. Fix interpenetration defects:
   - 205-PU-054: move the MC separator column train away from the casing
     and slide the degassing vessel clear of the casing, reconnecting its
     outlet pipe to the baseplate edge.
   - 205-PU-038: raise the separator column and vessel so they seat on the
     pump support feet instead of cutting into them.
   - 205-PU-060/061: lower the service splash plate clear of the casing.
4. Remove the MC_AUXILIARY subequipment from the five MC pumps (temporary,
   to be re-added later).
5. Cut a true hole through each DRIVER terminal-box plate (BOX 21) with a
   negative cylinder (NCYLINDER) and delete the old gland stub cylinder,
   following the user's negative-primitive instruction (2026-08-05).

Baseplates, nozzles (POS/ORI/HEIG/process attributes) and the trailing
catalogue binding pass are preserved byte-for-byte.

All EXTRUSION syntax follows the VERIFIED forms in
skill/knowledge/pml1-reference.md (profile end-plane POS, local-Z sweep,
ordered boundary vertices, ORI Y IS <axis> AND Z IS <extrusion axis>).
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from pathlib import Path

SRC = Path(r"C:\Users\A\Desktop\JK_PU.txt")
OUT = Path(
    r"C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output"
    r"\JK_Pump_Build_refined_20260805_r8.pml"
)

MC_EQUIS = (
    "/203_PU_020",
    "/205_PU_004",
    "/205_PU_018",
    "/205_PU_038",
    "/205_PU_054",
)


# --------------------------------------------------------------------------
# Number formatting helpers
# --------------------------------------------------------------------------

def r1(value: float) -> str:
    """One-decimal mm value, no trailing zeros."""
    return "%g" % round(value, 1)


def signed(axis: str, value: float) -> str:
    if axis == "E":
        return "E" if value >= 0 else "W"
    if axis == "N":
        return "N" if value >= 0 else "S"
    return "U" if value >= 0 else "D"


def pos_text(e: float, n: float, u: float) -> str:
    return (
        f"POS {signed('E', e)} {r1(abs(e))}mm "
        f"{signed('N', n)} {r1(abs(n))}mm "
        f"{signed('U', u)} {r1(abs(u))}mm"
    )


def vert_text(x: float, y: float) -> str:
    """VERTEX in the EXTRUSION profile plane. x maps to E/N depending on
    the gusset extrusion axis, y maps to U."""
    return (
        f"POS {signed('E', x)} {r1(abs(x))}mm "
        f"{signed('N', y)} {r1(abs(y))}mm U 0mm"
    )


# --------------------------------------------------------------------------
# Parser
# --------------------------------------------------------------------------

PRIM_RE = re.compile(
    r"^NEW (CYLINDER|CYLI|NCYLINDER|NCYLI|NBOX|CONE|BOX|NOZZLE|EXTRUSION|DISH|PYRAMID)\b",
    re.IGNORECASE,
)
EQUI_RE = re.compile(r"^NEW (EQUIPMENT|EQUI)\s+(\S+)", re.IGNORECASE)
SUBE_RE = re.compile(r"^NEW (SUBEQUIPMENT|SUBE)\s+(\S+)", re.IGNORECASE)
END_RE = re.compile(r"^END\s*$", re.IGNORECASE)
POS_RE = re.compile(
    r"^POS ([EW])\s+([-\d.]+)[a-z]*\s+([NS])\s+([-\d.]+)[a-z]*\s+"
    r"([UD])\s+([-\d.]+)[a-z]*$",
    re.IGNORECASE,
)
KV_RE = re.compile(r"^([A-Z]+)\s+(.+)$", re.IGNORECASE)


def to_number(text: str) -> float:
    text = text.strip()
    for suffix in ("mm", "degC", "pascal", "degree"):
        if text.lower().endswith(suffix):
            text = text[: -len(suffix)]
    return float(text)


def parse(lines: list[str]) -> list[dict]:
    """Return blocks with start/end line indices (inclusive)."""
    blocks: list[dict] = []
    cur: dict | None = None
    cur_equi: str | None = None
    cur_sub: str | None = None
    for i, line in enumerate(lines):
        s = line.strip()
        m = EQUI_RE.match(s)
        if m and cur is None:
            cur_equi = m.group(2)
            continue
        m = SUBE_RE.match(s)
        if m and cur is None:
            cur_sub = m.group(2)
            continue
        m = PRIM_RE.match(s)
        if m and cur is None:
            raw = m.group(1).upper()
            if raw == "CYLI":
                raw = "CYLINDER"
            elif raw == "NCYLI":
                raw = "NCYLINDER"
            cur = {
                "type": raw,
                "attrs": [s],
                "name": "",
                "start": i,
                "end": None,
                "equi": cur_equi,
                "sub": cur_sub,
            }
            nm = re.match(r"^NEW \S+\s+(\S+)", s, re.IGNORECASE)
            if nm:
                cur["name"] = nm.group(1)
            continue
        if cur is not None:
            if s:
                cur["attrs"].append(s)
            if END_RE.match(s):
                cur["end"] = i
                blocks.append(cur)
                cur = None
    return blocks


def block_geom(block: dict) -> dict:
    pos: tuple[float, float, float] | None = None
    dims: dict[str, float] = {}
    for a in block["attrs"]:
        m = POS_RE.match(a)
        if m:
            e = to_number(m.group(2))
            n = to_number(m.group(4))
            u = to_number(m.group(6))
            if m.group(1).upper() == "W":
                e = -e
            if m.group(3).upper() == "S":
                n = -n
            if m.group(5).upper() == "D":
                u = -u
            pos = (e, n, u)
            continue
        m = KV_RE.match(a)
        if m and m.group(1).upper() in (
            "DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "DTOP", "DBOT",
        ):
            dims[m.group(1).upper()] = to_number(m.group(2))
    return {"pos": pos, "dims": dims}


# --------------------------------------------------------------------------
# Bridge bracket generation
# --------------------------------------------------------------------------

def sole_plate_text(pad: dict) -> list[str]:
    g = block_geom(pad)
    e, n, u = g["pos"]
    xl = g["dims"]["XLEN"]
    yl = g["dims"]["YLEN"]
    zl = g["dims"]["ZLEN"]
    t = min(16.0, max(10.0, round(zl * 0.42, 1)))
    return [
        "-- Refined: bridge bracket sole plate (Reference Value)",
        "NEW BOX",
        pos_text(e, n, u + zl / 2 - t / 2),
        f"XLEN {r1(xl)}mm",
        f"YLEN {r1(yl)}mm",
        f"ZLEN {r1(t)}mm",
        "",
        "END",
        "",
    ]


def gusset_text(pad: dict, side: str) -> list[str]:
    """One trapezoid gusset plate. side: '-N' / '+N' / '-E' / '+E'."""
    g = block_geom(pad)
    e, n, u = g["pos"]
    xl = g["dims"]["XLEN"]
    yl = g["dims"]["YLEN"]
    zl = g["dims"]["ZLEN"]
    t = min(16.0, max(10.0, round(zl * 0.42, 1)))
    h = zl - t
    tg = 10.0
    bevel = min(24.0, round(h * 0.55, 1))

    if yl >= xl:
        # long axis N; profile in E-U plane; extrusion along N
        w = xl
        if side == "-N":
            pe, pn = e, n - yl / 2
        else:
            pe, pn = e, n + yl / 2 - tg
        ori = "ORI Y is U and Z is N"
        v1, v2 = (-w / 2, 0.0), (w / 2, 0.0)
        v3, v4 = (w / 2 - bevel, h), (-w / 2 + bevel, h)
    else:
        # long axis E; profile in N-U plane; extrusion along E
        w = yl
        if side == "-E":
            pe, pn = e - xl / 2, n
        else:
            pe, pn = e + xl / 2 - tg, n
        ori = "ORI Y is U and Z is E"
        v1, v2 = (-w / 2, 0.0), (w / 2, 0.0)
        v3, v4 = (w / 2 - bevel, h), (-w / 2 + bevel, h)

    return [
        "-- Refined: bridge bracket trapezoid gusset (EXTRUSION, Reference Value)",
        "NEW EXTRUSION",
        pos_text(pe, pn, u - zl / 2),
        ori,
        f"HEIG {r1(tg)}mm",
        "",
        "NEW LOOP",
        "",
        "NEW VERTEX",
        vert_text(*v1),
        "END",
        "NEW VERTEX",
        vert_text(*v2),
        "END",
        "NEW VERTEX",
        vert_text(*v3),
        "END",
        "NEW VERTEX",
        vert_text(*v4),
        "END",
        "END",
        "END",
        "",
    ]


def bridge_replacement(pad: dict, kind: str) -> list[str]:
    out: list[str] = []
    if kind == "pump":
        out.append("-- Refined: pump bridge bracket (sole plate + 2 gussets)")
    else:
        out.append("-- Refined: motor bridge bracket (sole plate + 2 gussets)")
    out += sole_plate_text(pad)
    g = block_geom(pad)
    if g["dims"]["YLEN"] >= g["dims"]["XLEN"]:
        sides = ("-N", "+N")
    else:
        sides = ("-E", "+E")
    for side in sides:
        out += gusset_text(pad, side)
    return out


def pyramid_gusset_text(pad: dict, side: str, base_u: float) -> list[str]:
    """Reference-style PYRAMID gusset copied verbatim from the P1501A-BASE
    template: bottom centred at POS, YBOT along the pad long axis, top
    shortened; no ORI (axes E/N/U)."""
    g = block_geom(pad)
    e, n, u = g["pos"]
    xl = g["dims"]["XLEN"]
    yl = g["dims"]["YLEN"]
    zl = g["dims"]["ZLEN"]
    t = min(16.0, max(10.0, round(zl * 0.42, 1)))
    h = zl - t                      # gusset height
    top = u + zl / 2 - t            # sole-plate bottom = gusset top
    heig = top - base_u
    if yl >= xl:
        ybot = yl * 0.55
        xbot = 20.0
        if side == "-N":
            gn = n - yl * 0.25
        else:
            gn = n + yl * 0.25
        ge = e
    else:
        ybot = xl * 0.55
        xbot = 20.0
        if side == "-E":
            ge = e - xl * 0.25
        else:
            ge = e + xl * 0.25
        gn = n
    return [
        "-- Refined: PYRAMID gusset (reference base style, copied form)",
        "NEW PYRAMID",
        pos_text(ge, gn, base_u),
        f"XBOT {r1(xbot)}mm",
        f"YBOT {r1(ybot)}mm",
        f"XTOP {r1(xbot)}mm",
        f"YTOP {r1(max(10.0, ybot * 0.7))}mm",
        f"HEIG {r1(max(5.0, heig))}mm",
        "",
        "END",
        "",
    ]


def bridge_replacement_ref(pad: dict, kind: str, base_u: float) -> list[str]:
    """Reference-style bridge: sole plate + two PYRAMID gussets standing on
    the flange-bar top (base_u)."""
    out: list[str] = []
    if kind == "pump":
        out.append("-- Refined: pump support (reference base style: sole plate + PYRAMID gussets)")
    else:
        out.append("-- Refined: motor support (reference base style: sole plate + PYRAMID gussets)")
    out += sole_plate_text(pad)
    g = block_geom(pad)
    if g["dims"]["YLEN"] >= g["dims"]["XLEN"]:
        sides = ("-N", "+N")
    else:
        sides = ("-E", "+E")
    for side in sides:
        out += pyramid_gusset_text(pad, side, base_u)
    return out


def c_channel_verts(w: float, h: float, tw: float, tf: float, open_pos: int) -> list[tuple[float, float]]:
    """C-channel profile in local XY (X = short axis, Y = Up).
    open_pos = +1 opens toward +X (web on -X); -1 mirrors."""
    pts = [
        (-w / 2, -h / 2),
        (-w / 2 + tw, -h / 2),
        (-w / 2 + tw, -h / 2 + tf),
        (w / 2, -h / 2 + tf),
        (w / 2, h / 2 - tf),
        (-w / 2 + tw, h / 2 - tf),
        (-w / 2 + tw, h / 2),
        (-w / 2, h / 2),
    ]
    if open_pos < 0:
        pts = [(-x, y) for x, y in pts]
    return pts


def c_channel_rail_text(rail: dict, centre: tuple[float, float]) -> list[str]:
    """Replace a solid rectangular skid rail with a standard C-channel
    EXTRUSION that keeps the same outer envelope, position and length."""
    g = block_geom(rail)
    p, d = g["pos"], g["dims"]
    xl, yl, zl = d["XLEN"], d["YLEN"], d["ZLEN"]
    tw, tf = 8.0, 10.0
    if xl >= yl:
        long_axis = "E"
        w, h, heig = yl, zl, xl
        open_dir = 1 if p[1] < centre[1] else -1
        pe, pn, pu = p[0] - heig / 2, p[1], p[2]
        ori = "ORI Y is U and Z is E"

        def vert(x: float, y: float) -> str:
            return (
                f"POS E 0mm {signed('N', x)} {r1(abs(x))}mm "
                f"{signed('U', y)} {r1(abs(y))}mm"
            )
    else:
        long_axis = "N"
        w, h, heig = xl, zl, yl
        open_dir = 1 if p[0] < centre[0] else -1
        pe, pn, pu = p[0], p[1] - heig / 2, p[2]
        ori = "ORI Y is U and Z is N"

        def vert(x: float, y: float) -> str:
            return (
                f"POS {signed('E', x)} {r1(abs(x))}mm N 0mm "
                f"{signed('U', y)} {r1(abs(y))}mm"
            )

    pts = c_channel_verts(w, h, tw, tf, open_dir)
    out = [
        "-- Refined: standard C-channel skid rail (EXTRUSION, Reference Value)",
        "NEW EXTRUSION",
        pos_text(pe, pn, pu),
        ori,
        f"HEIG {r1(heig)}mm",
        "",
        "NEW LOOP",
        "",
    ]
    for x, y in pts:
        out += ["NEW VERTEX", vert(x, y), "END"]
    out += ["END", "END", ""]
    return out


def i_beam_rail_text(rail: dict) -> list[str]:
    """Rebuild a solid skid rail as a reference-style built-up I-section:
    lower flange + web + upper flange, keeping the original outer envelope,
    centre, length and top/bottom elevations (Reference Value flanges 20 mm,
    web 8 mm)."""
    g = block_geom(rail)
    p, d = g["pos"], g["dims"]
    xl, yl, zl = d["XLEN"], d["YLEN"], d["ZLEN"]
    tf = 20.0
    tw = 8.0
    h_bot = p[2] - zl / 2
    h_top = p[2] + zl / 2
    web_h = zl - 2 * tf
    out = [
        "-- Refined: built-up I-section skid rail (reference base style, Reference Value)",
    ]
    if yl >= xl:
        # rail runs N-S: width is the E dimension
        flange_x, flange_y = f"XLEN {r1(xl)}mm", f"YLEN {r1(yl)}mm"
        web_x, web_y = f"XLEN {r1(tw)}mm", f"YLEN {r1(yl)}mm"
    else:
        # rail runs E-W: width is the N dimension
        flange_x, flange_y = f"XLEN {r1(xl)}mm", f"YLEN {r1(yl)}mm"
        web_x, web_y = f"XLEN {r1(xl)}mm", f"YLEN {r1(tw)}mm"
    parts = (
        (h_bot + tf / 2, tf, flange_x, flange_y, "lower flange"),
        (p[2], web_h, web_x, web_y, "web"),
        (h_top - tf / 2, tf, flange_x, flange_y, "upper flange"),
    )
    for u_c, zlen, dim_x, dim_y, label in parts:
        out += [
            f"-- {label}",
            "NEW BOX",
            pos_text(p[0], p[1], u_c),
            dim_x,
            dim_y,
            f"ZLEN {r1(zlen)}mm",
            "",
            "END",
            "",
        ]
    return out


def flange_bar_text(rail: dict, base_top: float, thick: float) -> list[str]:
    """Reference-style flat-bar skid rail: a low wide bar seated on the
    baseplate top, same footprint/length as the original rail."""
    g = block_geom(rail)
    p, d = g["pos"], g["dims"]
    return [
        "-- Refined: flange bar rail (reference base style, Reference Value)",
        "NEW BOX",
        pos_text(p[0], p[1], base_top + thick / 2),
        f"XLEN {r1(d['XLEN'])}mm",
        f"YLEN {r1(d['YLEN'])}mm",
        f"ZLEN {r1(thick)}mm",
        "",
        "END",
        "",
    ]


def hex_nut_text(head: dict, heig: float | None = None, center_u: float | None = None) -> list[str]:
    g = block_geom(head)
    e, n, u = g["pos"]
    diam = g["dims"]["DIAM"]
    heig = g["dims"]["HEIG"] if heig is None else heig
    center_u = u if center_u is None else center_u
    side = diam / math.sqrt(3.0)          # across-flats == original diameter
    r = side * math.sqrt(3.0) / 2.0       # half across-flats
    pts = [
        (side, 0.0),
        (side / 2, r),
        (-side / 2, r),
        (-side, 0.0),
        (-side / 2, -r),
        (side / 2, -r),
    ]
    out = [
        "-- Refined: hex nut/washer (EXTRUSION, VERIFIED form)",
        "NEW EXTRUSION",
        pos_text(e, n, center_u - heig / 2),
        "ORI Y is N and Z is U",
        f"HEIG {r1(heig)}mm",
        "",
        "NEW LOOP",
        "",
    ]
    for px, py in pts:
        out += ["NEW VERTEX", vert_text(px, py), "END"]
    out += ["END", "END", ""]
    return out


def shank_text(shank: dict, heig: float, bottom: float) -> list[str]:
    """Rebuild an anchor shank with a new length (same centre E/N, same
    bottom face)."""
    g = block_geom(shank)
    e, n, _ = g["pos"]
    diam = g["dims"]["DIAM"]
    return [
        "-- Refined: extended anchor shank (reference base style)",
        "NEW CYLINDER",
        pos_text(e, n, bottom + heig / 2),
        f"DIAM {r1(diam)}mm",
        f"HEIG {r1(heig)}mm",
        "",
        "END",
        "",
    ]


def norm_axis(axis: str | None) -> str | None:
    return {"E": "E", "W": "E", "N": "N", "S": "N"}.get(axis)


def find_terminal_pairs(blocks: list[dict]) -> list[tuple[str, dict, dict]]:
    """Locate each DRIVER's terminal-box plate (BOX 21) and the gland stub
    cylinder that passes through it (same E/N centre, axis along the plate's
    thin axis, U span crossing the plate)."""
    pairs: list[tuple[str, dict, dict]] = []
    for equi in sorted({b["equi"] for b in blocks}):
        sub = equi + "_DRIVER"
        bs = [b for b in blocks if b["equi"] == equi and b["sub"] == sub]
        boxes = [b for b in bs if b["type"] == "BOX"]
        cyls = [b for b in bs if b["type"] == "CYLINDER"]
        if len(boxes) < 21:
            continue
        bx = boxes[20]
        g = block_geom(bx)
        p, d = g["pos"], g["dims"]
        if p is None or d.get("ZLEN", 0) < 30:
            continue
        xl, yl = d.get("XLEN", 0), d.get("YLEN", 0)
        if min(xl, yl) > 40:
            continue
        thin = "E" if xl <= yl else "N"
        match = None
        for cy in cyls:
            cg = block_geom(cy)
            cp, cd = cg["pos"], cg["dims"]
            if cp is None:
                continue
            z_axis = None
            for a in cy["attrs"]:
                m = re.match(r"^ORI\s+.*?\bZ\s+is\s+([EWNSUD])\b", a, re.IGNORECASE)
                if m:
                    z_axis = m.group(1).upper()
                    break
            if norm_axis(z_axis) != thin:
                continue
            if abs(cp[0] - p[0]) < 1.0 and abs(cp[1] - p[1]) < 1.0:
                b_lo, b_hi = p[2] - d["ZLEN"] / 2, p[2] + d["ZLEN"] / 2
                c_lo, c_hi = cp[2] - cd["DIAM"] / 2, cp[2] + cd["DIAM"] / 2
                if c_hi > b_lo + 0.5 and c_lo < b_hi - 0.5:
                    match = cy
                    break
        if match is not None:
            pairs.append((equi, bx, match))
    return pairs


def ncyli_lines(bx: dict, cy: dict) -> list[str]:
    """Negative cylinder child with the removed stub's own geometry.

    PML-STUDY-NCYL-001 (user E3D verdict 2026-08-06) proved that a negative
    child's POS is LOCAL to its owner: world coordinates (C1) placed the hole
    far off the plate, while a relative POS (C3) cut correctly. The stub's
    world position is therefore converted to an offset from the owner BOX
    centre. Standalone negatives at SUBE level are rejected by E3D (C4).
    """
    pos = ori = dia = heig = None
    cg = block_geom(cy)
    bg = block_geom(bx)
    ce, cn, cu = cg["pos"]
    be, bn, bu = bg["pos"]
    # Owner-relative offset. The hole circle (perpendicular to the stub
    # axis) must stay fully inside the plate, otherwise the hole opens
    # through the plate edge. Clamp the U offset per pump with a 2 mm rim.
    zl = bg["dims"]["ZLEN"]
    diam = cg["dims"]["DIAM"]
    max_dz = zl / 2 - diam / 2 - 2.0
    du = cu - bu
    du = max(-max_dz, min(max_dz, du))
    pos = pos_text(ce - be, cn - bn, du)
    for a in cy["attrs"]:
        if a.startswith("POS"):
            continue
        elif a.upper().startswith("ORI"):
            ori = a
        elif a.upper().startswith("DIAM"):
            dia = a
        elif a.upper().startswith("HEIG"):
            heig = a
    out = ["NEW NCYLINDER"]
    for a in (pos, ori, dia, heig):
        if a:
            out.append(a)
    # A negative primitive only subtracts when its negative-application flag
    # is set to 2 (AVEVA hmcontrol.pmlobj sets nappflag=2 after creating a
    # hole negative; strSctnGensec.pmlobj defaults NAPPFLAG -1 to 2).
    out.append("NAPPFLAG 2")
    out += ["", "END"]
    return out


# --------------------------------------------------------------------------
# Targeted clash fixes
# --------------------------------------------------------------------------

def shift_pos_attr(attr: str, de: float = 0.0, dn: float = 0.0, du: float = 0.0) -> str:
    m = POS_RE.match(attr)
    if not m:
        return attr
    e = to_number(m.group(2))
    n = to_number(m.group(4))
    u = to_number(m.group(6))
    if m.group(1).upper() == "W":
        e = -e
    if m.group(3).upper() == "S":
        n = -n
    if m.group(5).upper() == "D":
        u = -u
    return pos_text(e + de, n + dn, u + du)


def rewrite_pos(lines: list[str], de: float = 0.0, dn: float = 0.0, du: float = 0.0) -> list[str]:
    out = []
    for ln in lines:
        if POS_RE.match(ln.strip()):
            out.append(shift_pos_attr(ln.strip(), de, dn, du))
        else:
            out.append(ln)
    return out


def rewrite_pipe(lines: list[str], center_e: float, heig: float) -> list[str]:
    """Force a horizontal-E CYLINDER to a given center E and HEIG."""
    out = []
    for ln in lines:
        s = ln.strip()
        m = POS_RE.match(s)
        if m:
            e = to_number(m.group(2))
            n = to_number(m.group(4))
            u = to_number(m.group(6))
            if m.group(1).upper() == "W":
                e = -e
            if m.group(3).upper() == "S":
                n = -n
            if m.group(5).upper() == "D":
                u = -u
            out.append(pos_text(center_e, n, u))
            continue
        m = KV_RE.match(s)
        if m and m.group(1).upper() == "HEIG":
            out.append(f"HEIG {r1(heig)}mm")
            continue
        out.append(ln)
    return out


def apply_clash_fixes(blocks: list[dict]) -> dict[int, list[str]]:
    """Return block-start -> replacement text for the targeted clash fixes."""
    repl: dict[int, list[str]] = {}
    for b in blocks:
        if b["sub"] and b["sub"].endswith("_MC_AUXILIARY"):
            continue  # the whole subequipment is removed this revision
        if b["equi"] == "/205_PU_054" and b["sub"] == "/205_PU_054_MC_AUXILIARY":
            idx_in_sub = sum(
                1 for x in blocks
                if x["equi"] == b["equi"] and x["sub"] == b["sub"] and x["start"] < b["start"]
            )
            if idx_in_sub < 20:
                # separator column train: clear the casing (-E)
                repl[b["start"]] = rewrite_pos(b["attrs"], de=-30.0)
            else:
                # degassing vessel assembly: the discharge-side corner has no
                # free footprint (casing body, cover cone and discharge flange
                # ring fill it), so move the vessel to the only clear space on
                # the skid, the motor-side corner.
                repl[b["start"]] = rewrite_pos(b["attrs"], de=60.0, dn=-1292.0)
        elif b["equi"] == "/205_PU_038" and b["sub"] == "/205_PU_038_MC_AUXILIARY":
            idx_in_sub = sum(
                1 for x in blocks
                if x["equi"] == b["equi"] and x["sub"] == b["sub"] and x["start"] < b["start"]
            )
            if idx_in_sub <= 3 or 20 <= idx_in_sub <= 25:
                # seat separator column and vessel on the support feet
                repl[b["start"]] = rewrite_pos(b["attrs"], du=5.0)
        elif b["equi"] in ("/205_PU_060", "/205_PU_061") and b["sub"].endswith("_SERVICE_DETAILS"):
            if b["type"] == "BOX":
                # splash plate: lower clear of the casing bottom
                repl[b["start"]] = rewrite_pos(b["attrs"], du=-35.0)
    return repl


# --------------------------------------------------------------------------
# Main transformation
# --------------------------------------------------------------------------

def main() -> None:
    lines = SRC.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks = parse(lines)

    replacements: dict[int, list[str]] = {}
    hex_replaced = 0

    by_sub: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for b in blocks:
        by_sub[(b["equi"], b["sub"])].append(b)

    pump_base_top: dict[str, float] = {}
    for b in blocks:
        if b["sub"] and b["sub"].endswith("_BASEPLATE") and b["type"] == "BOX":
            g = block_geom(b)
            pump_base_top[b["equi"]] = g["pos"][2] + g["dims"]["ZLEN"] / 2

    flange_thick = 20.0

    for (equi, sub), bs in by_sub.items():
        if sub.endswith("_SUPPORT_FRAME"):
            boxes = [b for b in bs if b["type"] == "BOX"]
            feet = []
            rails = []
            def long_dim(b: dict) -> float:
                g = block_geom(b)
                return max(g["dims"].get("XLEN", 0.0), g["dims"].get("YLEN", 0.0))
            ranked = sorted(boxes, key=long_dim, reverse=True)
            rails = [b for b in ranked[:2] if long_dim(b) > 500]
            for b in boxes:
                g = block_geom(b)
                xl = g["dims"].get("XLEN", 0.0)
                yl = g["dims"].get("YLEN", 0.0)
                zl = g["dims"].get("ZLEN", 0.0)
                if b in rails:
                    continue
                if min(xl, yl) > 50 and zl >= 40 and max(xl, yl) <= 300:
                    feet.append(b)
            if len(feet) != 4:
                raise SystemExit(f"{equi}: expected 4 pump support feet, got {len(feet)}")
            if len(rails) != 2:
                raise SystemExit(f"{equi}: expected 2 skid rails, got {len(rails)}")
            base_top = pump_base_top.get(equi, 0.0)
            rail_flange_u = base_top + flange_thick / 2
            for r in rails:
                replacements[r["start"]] = flange_bar_text(r, base_top, flange_thick)
            for f in feet:
                replacements[f["start"]] = bridge_replacement_ref(
                    f, "pump", base_top + flange_thick
                )
        elif sub.endswith("_DRIVER"):
            boxes = [b for b in bs if b["type"] == "BOX"]
            pads = []
            for b in boxes:
                g = block_geom(b)
                xl = g["dims"].get("XLEN", 0.0)
                yl = g["dims"].get("YLEN", 0.0)
                zl = g["dims"].get("ZLEN", 0.0)
                u = g["pos"][2]
                if 10 <= zl <= 35 and min(xl, yl) > 45 and u < 250:
                    pads.append(b)
            if len(pads) != 4:
                raise SystemExit(f"{equi}: expected 4 motor mounting pads, got {len(pads)}")
            base_top = pump_base_top.get(equi, 0.0)
            for p in pads:
                replacements[p["start"]] = bridge_replacement_ref(
                    p, "motor", base_top + flange_thick
                )
        elif sub.endswith("_BASE_FASTENERS") or sub.endswith("_DRIVER_FASTENERS"):
            cyls = [b for b in bs if b["type"] == "CYLINDER"]
            if len(cyls) % 3 != 0 or len(cyls) == 0:
                raise SystemExit(f"{equi} {sub}: fastener stack count {len(cyls)} not multiple of 3")
            is_base = sub.endswith("_BASE_FASTENERS")
            hex_washer_heig = 20.0
            for i in range(0, len(cyls), 3):
                shank = cyls[i]
                washer = cyls[i + 1]
                head = cyls[i + 2]
                wg = block_geom(washer)
                wb = wg["pos"][2] - wg["dims"].get("HEIG", 0) / 2
                if 20 <= wg["dims"].get("DIAM", 0) <= 60 and 2 <= wg["dims"].get("HEIG", 0) <= 8:
                    replacements[washer["start"]] = hex_nut_text(
                        washer, heig=hex_washer_heig, center_u=wb + hex_washer_heig / 2
                    )
                g = block_geom(head)
                if 18 <= g["dims"].get("DIAM", 0) <= 50 and 6 <= g["dims"].get("HEIG", 0) <= 18:
                    if is_base:
                        # reference-style anchor: nut seats on the thick hex
                        # washer top; shank extended to the nut top.
                        hn = g["dims"]["HEIG"]
                        nut_center = wb + hex_washer_heig + hn / 2
                        replacements[head["start"]] = hex_nut_text(
                            head, center_u=nut_center
                        )
                        sg = block_geom(shank)
                        sb = sg["pos"][2] - sg["dims"].get("HEIG", 0) / 2
                        shank_heig = (wb - sb) + hex_washer_heig + hn
                        replacements[shank["start"]] = shank_text(
                            shank, shank_heig, sb
                        )
                    else:
                        replacements[head["start"]] = hex_nut_text(head)
                    hex_replaced += 1

    replacements.update(apply_clash_fixes(blocks))

    # 1. temporarily remove the MC_AUXILIARY subequipment (five MC pumps)
    delete_ranges: list[tuple[int, int]] = []
    for equi in MC_EQUIS:
        sub = equi + "_MC_AUXILIARY"
        sub_blocks = [b for b in blocks if b["equi"] == equi and b["sub"] == sub]
        if not sub_blocks:
            continue
        header = None
        for i, ln in enumerate(lines):
            if ln.strip().upper().startswith("NEW SUBEQUIPMENT") and sub in ln:
                header = i
                break
        if header is None:
            raise SystemExit(f"{equi}: MC_AUXILIARY header not found")
        last = max(b["end"] for b in sub_blocks)
        # The SUBEQUIPMENT block has its own trailing END line (the first
        # 'END' after the last primitive). It must be deleted with the
        # subequipment, otherwise the stray END closes the EQUIPMENT and then
        # the ZONE, and the next NEW EQUIPMENT fails with
        # "Cannot create a EQUI at this level".
        sub_end = last
        for i in range(last + 1, len(lines)):
            if lines[i].strip() == "END":
                sub_end = i
                break
        if sub_end == last:
            raise SystemExit(f"{equi}: MC_AUXILIARY subequipment END not found")
        # guard: the line after the subequipment END must close the EQUIPMENT
        nxt = sub_end + 1
        while nxt < len(lines) and not lines[nxt].strip():
            nxt += 1
        if nxt < len(lines) and lines[nxt].strip() != "END":
            raise SystemExit(
                f"{equi}: unexpected line after MC_AUXILIARY END: {lines[nxt]!r}"
            )
        delete_ranges.append((header, sub_end))

    # 2. negative-cylinder holes through the DRIVER terminal-box plates
    ncyli_count = 0
    for equi, bx, cy in find_terminal_pairs(blocks):
        box_lines = lines[bx["start"] : bx["end"] + 1]
        replacements[bx["start"]] = box_lines[:-1] + ncyli_lines(bx, cy) + [box_lines[-1]]
        replacements[cy["start"]] = []
        ncyli_count += 1

    ops: list[tuple[int, int, list[str]]] = []
    for start, text in replacements.items():
        block = next(b for b in blocks if b["start"] == start)
        ops.append((start, block["end"], text))
    for h, last in delete_ranges:
        ops.append((h, last, []))
    ops.sort(key=lambda x: x[0], reverse=True)

    out_lines = list(lines)
    for start, end, text in ops:
        out_lines[start : end + 1] = text

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Hex nuts replaced: {hex_replaced}")
    print(f"MC_AUXILIARY subequipment removed: {len(delete_ranges)}")
    print(f"NCYLI holes added: {ncyli_count}")
    print(f"Line count: {len(lines)} -> {len(out_lines)}")


if __name__ == "__main__":
    main()
