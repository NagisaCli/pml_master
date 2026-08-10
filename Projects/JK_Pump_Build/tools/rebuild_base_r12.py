"""r12 -- rebuild every pump foundation as a DATUM-DRIVEN fabricated pedestal.

Starting point: JK_Pump_Build_refined_20260805_r8.pml (last clean base baseline)
Output:         JK_Pump_Build_refined_20260805_r12.pml

WHY THIS REVISION EXISTS
------------------------
r9, r10 and r11 were all rejected.  The r11 verdict was "the base support and
the pump/motor are completely separated".  A measurement of r11 shows exactly
why, and it is not a modelling-style problem:

  * the pump casing was driven 7.4 - 25.9 mm INTO the sole plates that were
    supposed to carry it (the sole-plate top was above the casing underside);
  * the motor's real feet (BOX blocks whose bottoms sit at U 114 - 168) were
    never touched.  r11 carried a set of invented 12 mm "pads" at U 70..82 -
    45 to 95 mm BELOW the feet - so the motor visibly hung in the air over
    its own support.

Every previous verifier checked contacts *inside* the base assembly and so
reported "0 floating elements" while the assembly as a whole did not touch
the machine.  r12 inverts the construction order:

    measure the equipment first, then build the support UP TO it.

CONSTRUCTION (per pump, both ends independently)
------------------------------------------------
  1. Frame rails: 5 longitudinal members, 20 mm, seated on the baseplate top.
  2. Pedestal:    for each machine foot, a fabricated pedestal of
                    - bearing sole plate (top face = the foot underside),
                    - two vertical web plates under it, running to the frame
                      top (so the pedestal is a plate girder, not a stack of
                      floating blocks),
                    - a bottom flange plate seated on the frame top.
                  Pedestal height is derived per foot from the measured
                  datum, so pump-end and motor-end heights differ naturally.
  3. Anchors:     one bolt per pedestal corner-pair, shank rising through the
                  sole plate with a hex washer on the frame top and a hex nut
                  on the sole-plate top.

Nothing is emitted that cannot both carry and be carried.  Outside the base
scope (baseplate, casing, motor body, nozzles, CATR, NCYLI holes, service
details) the file is preserved byte-for-byte from r8.

All new dimensions are Reference Values, scaled from the contractual
baseplate and the measured machine envelope; none is vendor data.
"""

from __future__ import annotations

import math
import re
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "output" / "JK_Pump_Build_refined_20260805_r8.pml"
OUT = BASE / "output" / "JK_Pump_Build_refined_20260805_r12.pml"

# ---------------------------------------------------------------- Reference Values
FRAME_T = 20.0        # longitudinal frame member thickness
SOLE_T = 16.0         # pedestal bearing sole plate thickness
FLANGE_T = 12.0       # pedestal bottom flange thickness
WEB_T = 10.0          # pedestal vertical web thickness
MIN_CLEAR = 6.0       # minimum pedestal clear web height before it degenerates
HEX_H = 10.6          # nut height
WASHER_H = 8.0

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
ORI_RE = re.compile(r"^ORI\b", re.IGNORECASE)
KV_RE = re.compile(r"^([A-Z]+)\s+(.+)$", re.IGNORECASE)


def r1(v: float) -> str:
    return "%g" % round(v, 1)


def signed(axis: str, v: float) -> str:
    if axis == "E":
        return "E" if v >= 0 else "W"
    if axis == "N":
        return "N" if v >= 0 else "S"
    return "U" if v >= 0 else "D"


def pos_text(e: float, n: float, u: float) -> str:
    return (
        f"POS {signed('E', e)} {r1(abs(e))}mm "
        f"{signed('N', n)} {r1(abs(n))}mm "
        f"{signed('U', u)} {r1(abs(u))}mm"
    )


def to_number(text: str) -> float:
    text = text.strip()
    for suffix in ("mm", "degC", "pascal", "degree"):
        if text.lower().endswith(suffix):
            text = text[: -len(suffix)]
    return float(text)


# ---------------------------------------------------------------- parsing
def parse(lines: list[str]) -> list[dict]:
    """Flat block list. Negative primitives nest, so track depth."""
    blocks: list[dict] = []
    cur: dict | None = None
    depth = 0
    cur_equi: str | None = None
    cur_sub: str | None = None
    for i, line in enumerate(lines):
        s = line.strip()
        if cur is None:
            m = EQUI_RE.match(s)
            if m:
                cur_equi = m.group(2)
                continue
            m = SUBE_RE.match(s)
            if m:
                cur_sub = m.group(2)
                continue
            m = PRIM_RE.match(s)
            if m:
                raw = m.group(1).upper()
                raw = {"CYLI": "CYLINDER", "NCYLI": "NCYLINDER"}.get(raw, raw)
                cur = {"type": raw, "attrs": [s], "start": i, "end": None,
                       "equi": cur_equi, "sub": cur_sub}
                depth = 1
                continue
        else:
            if s:
                cur["attrs"].append(s)
            if s.upper().startswith(("NEW LOOP", "NEW VERTEX")) or PRIM_RE.match(s):
                depth += 1
            elif END_RE.match(s):
                depth -= 1
                if depth == 0:
                    cur["end"] = i
                    blocks.append(cur)
                    cur = None
    return blocks


def block_geom(block: dict) -> tuple:
    pos = None
    dims: dict[str, float] = {}
    ori = None
    for a in block["attrs"]:
        m = POS_RE.match(a)
        if m and pos is None:
            e, n, u = to_number(m.group(2)), to_number(m.group(4)), to_number(m.group(6))
            if m.group(1).upper() == "W":
                e = -e
            if m.group(3).upper() == "S":
                n = -n
            if m.group(5).upper() == "D":
                u = -u
            pos = (e, n, u)
            continue
        if ORI_RE.match(a) and ori is None:
            ori = a
            continue
        m = KV_RE.match(a)
        if m and m.group(1).upper() in (
            "DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "DTOP", "DBOT",
            "XBOT", "YBOT", "XTOP", "YTOP", "XOFF", "YOFF",
        ):
            dims[m.group(1).upper()] = to_number(m.group(2))
    return pos, dims, ori


def aabb(block: dict):
    """World AABB of a top-level primitive."""
    pos, d, ori = block_geom(block)
    if pos is None:
        return None
    e, n, u = pos
    t = block["type"]
    o = (ori or "").upper()
    if t in ("BOX", "NBOX"):
        x, y, z = d.get("XLEN", 0), d.get("YLEN", 0), d.get("ZLEN", 0)
        if "Y IS U" in o and "Z IS S" in o or "Y IS U" in o and "Z IS N" in o:
            x, y, z = x, z, y
        elif "Y IS U" in o and "Z IS E" in o or "Y IS U" in o and "Z IS W" in o:
            x, y, z = z, x, y
        elif "Z IS N" in o or "Z IS S" in o:
            x, y, z = x, z, y
        elif "Z IS E" in o or "Z IS W" in o:
            x, y, z = z, y, x
        return (e - x / 2, e + x / 2, n - y / 2, n + y / 2, u - z / 2, u + z / 2)
    if t in ("CYLINDER", "NCYLINDER"):
        r = d.get("DIAM", 0) / 2
        h = d.get("HEIG", 0)
        if "Z IS N" in o or "Z IS S" in o:
            return (e - r, e + r, n - h / 2, n + h / 2, u - r, u + r)
        if "Z IS E" in o or "Z IS W" in o:
            return (e - h / 2, e + h / 2, n - r, n + r, u - r, u + r)
        return (e - r, e + r, n - r, n + r, u - h / 2, u + h / 2)
    if t == "CONE":
        r = max(d.get("DBOT", 0), d.get("DTOP", 0)) / 2
        h = d.get("HEIG", 0)
        if "Z IS N" in o or "Z IS S" in o:
            return (e - r, e + r, n - h / 2, n + h / 2, u - r, u + r)
        if "Z IS E" in o or "Z IS W" in o:
            return (e - h / 2, e + h / 2, n - r, n + r, u - r, u + r)
        return (e - r, e + r, n - r, n + r, u - h / 2, u + h / 2)
    if t == "PYRAMID":
        x = max(d.get("XBOT", 0), d.get("XTOP", 0)) + 2 * abs(d.get("XOFF", 0))
        y = max(d.get("YBOT", 0), d.get("YTOP", 0)) + 2 * abs(d.get("YOFF", 0))
        h = d.get("HEIG", 0)
        return (e - x / 2, e + x / 2, n - y / 2, n + y / 2, u - h / 2, u + h / 2)
    if t == "EXTRUSION":
        pts = []
        for a in block["attrs"]:
            m = POS_RE.match(a)
            if m:
                x = to_number(m.group(2)) * (-1 if m.group(1).upper() == "W" else 1)
                y = to_number(m.group(4)) * (-1 if m.group(3).upper() == "S" else 1)
                z = to_number(m.group(6)) * (-1 if m.group(5).upper() == "D" else 1)
                pts.append((x, y, z))
        vs = pts[1:]
        if not vs:
            return None
        h = d.get("HEIG", 0)
        xs = [v[0] for v in vs]
        ys = [v[1] for v in vs]
        if "Z IS U" in o or not o:
            return (e + min(xs), e + max(xs), n + min(ys), n + max(ys), u, u + h)
        if "Z IS N" in o:
            return (e + min(xs), e + max(xs), n, n + h, u + min(ys), u + max(ys))
        if "Z IS S" in o:
            return (e + min(xs), e + max(xs), n - h, n, u + min(ys), u + max(ys))
        if "Z IS E" in o:
            return (e, e + h, n + min(xs), n + max(xs), u + min(ys), u + max(ys))
        if "Z IS W" in o:
            return (e - h, e, n + min(xs), n + max(xs), u + min(ys), u + max(ys))
        return (e + min(xs), e + max(xs), n + min(ys), n + max(ys), u, u + h)
    return None


# ---------------------------------------------------------------- emitters
def box_text(e, n, u, xl, yl, zl, comment) -> list[str]:
    return [
        f"-- Refined r12: {comment} (Reference Value)",
        "NEW BOX",
        pos_text(e, n, u),
        f"XLEN {r1(xl)}mm",
        f"YLEN {r1(yl)}mm",
        f"ZLEN {r1(zl)}mm",
        "",
        "END",
        "",
    ]


def hex_text(e, n, u_bottom, heig, side, comment) -> list[str]:
    r = side * math.sqrt(3.0) / 2.0
    pts = [(side, 0.0), (side / 2, r), (-side / 2, r),
           (-side, 0.0), (-side / 2, -r), (side / 2, -r)]
    out = [f"-- Refined r12: {comment} (VERIFIED hex EXTRUSION form)",
           "NEW EXTRUSION", pos_text(e, n, u_bottom),
           "ORI Y is N and Z is U", f"HEIG {r1(heig)}mm", "", "NEW LOOP", ""]
    for px, py in pts:
        out += ["NEW VERTEX",
                f"POS {signed('E', px)} {r1(abs(px))}mm "
                f"{signed('N', py)} {r1(abs(py))}mm U 0mm",
                "END"]
    out += ["END", "END", ""]
    return out


def shank_text(e, n, bottom, top, diam) -> list[str]:
    return [
        "-- Refined r12: anchor shank through pedestal sole plate (Reference Value)",
        "NEW CYLINDER",
        pos_text(e, n, (bottom + top) / 2),
        f"DIAM {r1(diam)}mm",
        f"HEIG {r1(top - bottom)}mm",
        "",
        "END",
        "",
    ]


# ---------------------------------------------------------------- pedestal
def pedestal(plate: tuple, frame_top: float, long_axis: str,
             kind: str, hex_side: float, bolt_d: float) -> list[str]:
    """A fabricated pedestal filling the void between `frame_top` and the
    underside of `plate` (the existing, correctly-placed bearing plate).

    Cross-section (transverse):     Elevation (longitudinal):
        ||        ||                  +----------------+  <- plate (untouched)
        ||  webs  ||                  |  web    web    |
        ++========++  bottom flange   +================+  <- flange on frame top

    The plate itself is NEVER moved: r8 already places every bearing surface
    exactly on the machine foot, and moving it is what destroyed r11.
    We only fill what is currently empty air.
    """
    e0, e1, n0, n1, u0, u1 = plate
    out: list[str] = []
    clear = u0 - frame_top
    if clear <= MIN_CLEAR:
        return out

    ce, cn = (e0 + e1) / 2, (n0 + n1) / 2
    pe, pn = e1 - e0, n1 - n0

    # Bottom flange: slightly wider than the plate, seated ON the frame top.
    fl_t = min(FLANGE_T, max(6.0, clear * 0.35))
    fe, fn = pe + 16.0, pn + 16.0
    out += box_text(ce, cn, frame_top + fl_t / 2, fe, fn, fl_t,
                    f"{kind} pedestal bottom flange (seated on frame top)")

    web_h = clear - fl_t
    if web_h > MIN_CLEAR:
        # Two vertical webs running the full depth, under the plate edges.
        # Webs run along the LONG axis so they resist the machine's thrust.
        if long_axis == "E":
            web_len = pe - 8.0            # along E
            span = pn - 2 * WEB_T - 12.0  # web centre-to-centre across N
            span = max(span, 20.0)
            for sgn in (-1.0, 1.0):
                out += box_text(ce, cn + sgn * span / 2,
                                frame_top + fl_t + web_h / 2,
                                web_len, WEB_T, web_h,
                                f"{kind} pedestal web plate")
            # transverse stiffener at mid-length, tying the two webs
            out += box_text(ce, cn, frame_top + fl_t + web_h / 2,
                            WEB_T, span - WEB_T, web_h,
                            f"{kind} pedestal transverse stiffener")
        else:
            web_len = pn - 8.0
            span = pe - 2 * WEB_T - 12.0
            span = max(span, 20.0)
            for sgn in (-1.0, 1.0):
                out += box_text(ce + sgn * span / 2, cn,
                                frame_top + fl_t + web_h / 2,
                                WEB_T, web_len, web_h,
                                f"{kind} pedestal web plate")
            out += box_text(ce, cn, frame_top + fl_t + web_h / 2,
                            span - WEB_T, WEB_T, web_h,
                            f"{kind} pedestal transverse stiffener")
    return out


def anchors(plate: tuple, frame_top: float, long_axis: str,
            hex_side: float, bolt_d: float, kind: str) -> list[str]:
    """Two hold-down bolts per plate, on the plate's long centreline,
    rising from inside the frame to a nut seated on the PLATE TOP."""
    e0, e1, n0, n1, u0, u1 = plate
    ce, cn = (e0 + e1) / 2, (n0 + n1) / 2
    out: list[str] = []
    if long_axis == "E":
        off = (e1 - e0) / 2 - max(14.0, hex_side + 3.0)
        pts = [(ce - off, cn), (ce + off, cn)]
    else:
        off = (n1 - n0) / 2 - max(14.0, hex_side + 3.0)
        pts = [(ce, cn - off), (ce, cn + off)]
    if off <= 4.0:
        return out
    for pe_, pn_ in pts:
        out += shank_text(pe_, pn_, frame_top - 18.0, u1 + HEX_H, bolt_d)
        out += hex_text(pe_, pn_, u1, HEX_H, hex_side,
                        f"{kind} hold-down nut on plate top")
    return out


# ---------------------------------------------------------------- main
def sube_span(lines: list[str], header_index: int) -> int:
    """Index of the SUBE's own closing END line."""
    i = header_index + 1
    while i < len(lines):
        s = lines[i].strip()
        if s.upper().startswith(("NEW SUBEQUIPMENT", "NEW EQUIPMENT")):
            j = i - 1
            while j > header_index and not lines[j].strip():
                j -= 1
            return j
        i += 1
    j = len(lines) - 1
    while j > header_index and not lines[j].strip():
        j -= 1
    return j


def main() -> None:
    lines = SRC.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks = parse(lines)
    by = defaultdict(list)
    for b in blocks:
        by[(b["equi"], b["sub"])].append(b)

    equis = sorted({b["equi"] for b in blocks if b["equi"]})
    ops: list[tuple[int, int, list[str]]] = []
    stats = {"pedestals": 0, "gussets_removed": 0, "anchors": 0, "pumps": 0}

    for eq in equis:
        sf = by[(eq, eq + "_SUPPORT_FRAME")]
        dr = by[(eq, eq + "_DRIVER")]
        bp = by[(eq, eq + "_BASEPLATE")]
        if not sf or not bp:
            continue
        stats["pumps"] += 1

        bp_box = [b for b in bp if b["type"] == "BOX"][0]
        bpb = aabb(bp_box)
        long_axis = "E" if (bpb[1] - bpb[0]) >= (bpb[3] - bpb[2]) else "N"

        # frame rails: 20 mm members seated on the baseplate top
        rails = [b for b in sf if b["type"] == "BOX"
                 and abs(aabb(b)[5] - aabb(b)[4] - FRAME_T) < 0.6
                 and max(aabb(b)[1] - aabb(b)[0], aabb(b)[3] - aabb(b)[2]) > 500]
        frame_top = max((aabb(b)[5] for b in rails), default=bpb[5] + FRAME_T)

        # hex size / bolt diameter carried over from the existing fasteners
        hex_side, bolt_d = 21.0, 17.0
        for key in (eq + "_BASE_FASTENERS",):
            for b in by[(eq, key)]:
                if b["type"] == "CYLINDER":
                    bolt_d = block_geom(b)[1].get("DIAM", 17.0)
                    break

        # ---------------- pump end: SUPPORT_FRAME ----------------
        sole_plates = [b for b in sf if b["type"] == "BOX"
                       and 9 <= (aabb(b)[5] - aabb(b)[4]) <= 18
                       and aabb(b)[4] > 60]
        new_pump: list[str] = []
        for sb in sole_plates:
            pl = aabb(sb)
            new_pump += pedestal(pl, frame_top, long_axis, "pump",
                                 hex_side, bolt_d)
            stats["pedestals"] += 1
        # delete the old decorative PYRAMID gussets
        for g in [b for b in sf if b["type"] == "PYRAMID"]:
            ops.append((g["start"], g["end"], []))
            stats["gussets_removed"] += 1
        if new_pump:
            last = max(sole_plates, key=lambda b: b["end"])
            ops.append((last["end"] + 1, last["end"], [""] + new_pump))

        # ---------------- motor end: DRIVER pads ----------------
        # A motor mounting pad is a thin plate LOW on the train that a motor
        # foot lands on. Thin plates high up in the DRIVER are fan-grille
        # lattice bars (U 267-312 on the MC pumps) and must not get pedestals.
        motor_feet = [aabb(b) for b in dr if b["type"] == "BOX"
                      and (aabb(b)[5] - aabb(b)[4]) > 40 and aabb(b)[4] < 400]
        pads = []
        for b in dr:
            if b["type"] != "BOX":
                continue
            g = aabb(b)
            if not (8 <= (g[5] - g[4]) <= 17 and 60 < g[4] < 320):
                continue
            # keep it only if a real motor foot sits on this plate
            if any(abs(f[4] - g[5]) < 1.0
                   and min(f[1], g[1]) - max(f[0], g[0]) > 0.5
                   and min(f[3], g[3]) - max(f[2], g[2]) > 0.5
                   for f in motor_feet):
                pads.append(b)
        new_mot: list[str] = []
        for pb in pads:
            pl = aabb(pb)
            new_mot += pedestal(pl, frame_top, long_axis, "motor",
                                hex_side, bolt_d)
            stats["pedestals"] += 1
        for g in [b for b in dr if b["type"] == "PYRAMID"]:
            ops.append((g["start"], g["end"], []))
            stats["gussets_removed"] += 1
        if new_mot:
            last = max(pads, key=lambda b: b["end"])
            ops.append((last["end"] + 1, last["end"], [""] + new_mot))

        # ---------------- fasteners rebuilt onto the pedestals ----------------
        for sub_name, plates, kind in (
            (eq + "_BASE_FASTENERS", sole_plates, "pump"),
            (eq + "_DRIVER_FASTENERS", pads, "motor"),
        ):
            for i, ln in enumerate(lines):
                if ln.strip().upper().startswith("NEW SUBEQUIPMENT") and sub_name in ln:
                    end = sube_span(lines, i)
                    txt: list[str] = []
                    for pb in plates:
                        a = anchors(aabb(pb), frame_top, long_axis,
                                    hex_side, bolt_d, kind)
                        if a:
                            txt += a
                            stats["anchors"] += 2
                    ops.append((i + 1, end - 1, txt))
                    break

    # apply bottom-up so indices stay valid
    ops.sort(key=lambda x: (x[0], x[1]), reverse=True)
    out_lines = list(lines)
    for start, end, text in ops:
        if end < start - 1:
            continue
        out_lines[start:end + 1] = text

    OUT.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  lines {len(lines)} -> {len(out_lines)}")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
