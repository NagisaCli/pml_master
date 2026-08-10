"""Rebuild every pump base to the DBOutput.txt (P1502B / PUMP006) style,
with physical support logic (r11).

Starting point: JK_Pump_Build_refined_20260805_r8.pml (accepted baseline).
Output: JK_Pump_Build_refined_20260805_r11.pml

Only the base scope changes:
  - SUPPORT_FRAME   -> 5-member longitudinal frame (2 outer rails + 2 inner
                       rails + centre plate), pump-end stand (2 vertical side
                       plates carrying a pump-end sole plate + 1 cross-beam
                       EXTRUSION), and bridge brackets under each pump foot
                       and motor pad: bottom auxiliary block (bolted) +
                       diagonal web + middle plate + diagonal web, carrying
                       the existing sole plate / pad. Side cross-section
                       reads horizontal-diagonal-flat-diagonal-horizontal (a bridge).
  - BASE_FASTENERS  -> 8 screws fixing the four pump-foot auxiliary blocks
                       (2 per block at its transverse edges; shank + hex
                       washer + hex nut on the block top).
  - DRIVER_FASTENERS-> 8 screws fixing the four motor-pad blocks (same).
  - DRIVER          -> motor mounting pads keep their position/size; their
                       supports are rebuilt as bridge brackets.

Everything outside the base scope (baseplates, nozzles, CATR pass, casing,
motor body, NCYLI holes, service details) is preserved byte-for-byte.

Reference: C:\\Users\\A\\Desktop\\DBOutput.txt  (/P1502B-BASE, TMPLATE
/STD/PUMP006). Geometry is adapted to each pump's own envelope; every new
dimension is a Reference Value. Physical logic: nothing floats -- every
element either carries something above it or is carried by something below
(frame on baseplate, gussets/side plates on frame, sole plates on gussets
or side plates, anchors through feet with nut on the sole/pad top).
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from pathlib import Path

SRC = Path(
    r"C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output"
    r"\JK_Pump_Build_refined_20260805_r8.pml"
)
OUT = Path(
    r"C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Pump_Build\output"
    r"\JK_Pump_Build_refined_20260805_r11.pml"
)

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


def parse(lines: list[str]) -> list[dict]:
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
                "start": i,
                "end": None,
                "equi": cur_equi,
                "sub": cur_sub,
            }
            continue
        if cur is not None:
            if s:
                cur["attrs"].append(s)
            if END_RE.match(s):
                cur["end"] = i
                blocks.append(cur)
                cur = None
    return blocks


def block_geom(block: dict) -> tuple:
    pos: tuple[float, float, float] | None = None
    dims: dict[str, float] = {}
    for a in block["attrs"]:
        m = POS_RE.match(a)
        if m:
            e, n, u = to_number(m.group(2)), to_number(m.group(4)), to_number(m.group(6))
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
            "XBOT", "YBOT", "XTOP", "YTOP", "XOFF", "YOFF",
        ):
            dims[m.group(1).upper()] = to_number(m.group(2))
    return pos, dims


def box_text(e: float, n: float, u: float, xl: float, yl: float, zl: float,
             comment: str, ori: str | None = None) -> list[str]:
    out = [f"-- Refined: {comment} (PUMP006 reference style, Reference Value)"]
    out += ["NEW BOX", pos_text(e, n, u)]
    if ori:
        out.append(ori)
    out += [f"XLEN {r1(xl)}mm", f"YLEN {r1(yl)}mm", f"ZLEN {r1(zl)}mm", "", "END", ""]
    return out


def pyramid_text(e: float, n: float, u: float, xbot: float, ybot: float,
                 xtop: float, ytop: float, heig: float,
                 xoff: float = 0.0, yoff: float = 0.0,
                 ori: str | None = None, comment: str = "PYRAMID gusset") -> list[str]:
    out = [f"-- Refined: {comment} (PUMP006 reference style, copied form)"]
    out += ["NEW PYRAMID", pos_text(e, n, u)]
    if ori:
        out.append(ori)
    out += [
        f"XBOT {r1(xbot)}mm",
        f"YBOT {r1(ybot)}mm",
        f"XTOP {r1(xtop)}mm",
        f"YTOP {r1(ytop)}mm",
        f"HEIG {r1(heig)}mm",
    ]
    if xoff:
        out.append(f"XOFF {r1(xoff)}mm")
    if yoff:
        out.append(f"YOFF {r1(yoff)}mm")
    out += ["", "END", ""]
    return out


def hex_vertex_text(x: float, y: float) -> str:
    return (
        f"POS {signed('E', x)} {r1(abs(x))}mm "
        f"{signed('N', y)} {r1(abs(y))}mm U 0mm"
    )


def hex_text(e: float, n: float, u_bottom: float, heig: float,
             side: float, comment: str) -> list[str]:
    """Hexagonal EXTRUSION, profile end plane at u_bottom, swept +U."""
    r = side * math.sqrt(3.0) / 2.0
    pts = [
        (side, 0.0),
        (side / 2, r),
        (-side / 2, r),
        (-side, 0.0),
        (-side / 2, -r),
        (side / 2, -r),
    ]
    out = [f"-- Refined: {comment} (PUMP006 reference style, VERIFIED form)"]
    out += ["NEW EXTRUSION", pos_text(e, n, u_bottom), "ORI Y is N and Z is U",
            f"HEIG {r1(heig)}mm", "", "NEW LOOP", ""]
    for px, py in pts:
        out += ["NEW VERTEX", hex_vertex_text(px, py), "END"]
    out += ["END", "END", ""]
    return out


def beam_text(l0: float, t0: float, u0: float, span: float, length: float,
              height: float, long_axis: str) -> list[str]:
    """Cross-beam EXTRUSION between the pump-end side plates.

    Sweep axis = transverse axis; profile plane = (longitudinal, U).
    """
    if long_axis == "N":
        pe, pn, pu = t0, l0 - length / 2, u0
        ori = "ORI Y is U and Z is E"

        def vert(x: float, y: float) -> str:
            return f"POS E 0mm {signed('N', x)} {r1(abs(x))}mm {signed('U', y)} {r1(abs(y))}mm"
    else:
        pe, pn, pu = l0 - length / 2, t0, u0
        ori = "ORI Y is U and Z is N"

        def vert(x: float, y: float) -> str:
            return f"POS {signed('E', x)} {r1(abs(x))}mm N 0mm {signed('U', y)} {r1(abs(y))}mm"
    pts = [(0.0, 0.0), (0.0, height), (length, height), (length, 0.0)]
    out = [
        "-- Refined: pump-end cross beam EXTRUSION (PUMP006 reference style, Reference Value)",
        "NEW EXTRUSION",
        pos_text(pe, pn, pu),
        ori,
        f"HEIG {r1(span)}mm",
        "",
        "NEW LOOP",
        "",
    ]
    for x, y in pts:
        out += ["NEW VERTEX", vert(x, y), "END"]
    out += ["END", "END", ""]
    return out


def shank_text(e: float, n: float, bottom: float, top: float,
               diam: float) -> list[str]:
    return [
        "-- Refined: anchor shank through foot/pad (PUMP006 reference style, Reference Value)",
        "NEW CYLINDER",
        pos_text(e, n, (bottom + top) / 2),
        f"DIAM {r1(diam)}mm",
        f"HEIG {r1(top - bottom)}mm",
        "",
        "END",
        "",
    ]


class PumpFrame:
    """Per-pump geometry in a local (long, trans, U) frame."""

    def __init__(self, blocks: list[dict], equi: str):
        self.equi = equi
        by = defaultdict(list)
        for b in blocks:
            by[b["sub"]].append(b)
        self.by_sub = by
        bp = [b for b in by[equi + "_BASEPLATE"] if b["type"] == "BOX"][0]
        self.bp_pos, self.bp_dims = block_geom(bp)
        self.base_top = self.bp_pos[2] + self.bp_dims["ZLEN"] / 2
        self.frame_bottom = self.base_top
        self.frame_top = self.base_top + 20.0

        sf = by[equi + "_SUPPORT_FRAME"]
        rails = [
            b for b in sf if b["type"] == "BOX"
            and abs(block_geom(b)[1].get("ZLEN", 0) - 20) < 0.01
            and max(block_geom(b)[1].get("XLEN", 0), block_geom(b)[1].get("YLEN", 0)) > 500
        ]
        rails.sort(key=lambda b: block_geom(b)[0][0])
        self.rails = [block_geom(b) for b in rails[:2]]
        (p1, d1), (p2, d2) = self.rails
        if d1["XLEN"] >= d1["YLEN"]:
            self.long_axis = "E"
            self.trans_axis = "N"
            self.rail_len = d1["XLEN"]
            self.rail_w = d1["YLEN"]
            self.t1, self.t2 = sorted((p1[1], p2[1]))
            self.lc = (p1[0] + p2[0]) / 2
        else:
            self.long_axis = "N"
            self.trans_axis = "E"
            self.rail_len = d1["YLEN"]
            self.rail_w = d1["XLEN"]
            self.t1, self.t2 = sorted((p1[0], p2[0]))
            self.lc = (p1[1] + p2[1]) / 2

        self.cross = [
            b for b in sf if b["type"] == "BOX" and b not in rails
            and block_geom(b)[1].get("ZLEN", 0) > 30
        ]
        self.pump_soles = [
            block_geom(b) for b in sf if b["type"] == "BOX"
            and b not in rails and b not in self.cross
            and 9 <= block_geom(b)[1].get("ZLEN", 0) <= 17
        ]
        dr = by[equi + "_DRIVER"]
        self.motor_pads = [
            block_geom(b) for b in dr if b["type"] == "BOX"
            and 9 <= block_geom(b)[1].get("ZLEN", 0) <= 17
            and 90 < block_geom(b)[0][2] < 300
        ]
        self.pyr_sf_blocks = [b for b in sf if b["type"] == "PYRAMID"]
        self.pyr_dr_blocks = [b for b in dr if b["type"] == "PYRAMID"]
        self.pad_blocks = [
            b for b in dr if b["type"] == "BOX"
            and 9 <= block_geom(b)[1].get("ZLEN", 0) <= 17
            and 90 < block_geom(b)[0][2] < 300
        ]

        # pump-end sign along the long axis
        def l_of(g: tuple) -> float:
            p, _ = g
            return p[0] if self.long_axis == "E" else p[1]

        pump_l = [l_of(g) for g in self.pump_soles]
        motor_l = [l_of(g) for g in self.motor_pads]
        self.pump_end = 1.0 if max(pump_l) > max(motor_l) else -1.0
        self.pump_end_row = max(pump_l) if self.pump_end > 0 else min(pump_l)

        bf = by[equi + "_BASE_FASTENERS"]
        df = by[equi + "_DRIVER_FASTENERS"]
        self.bf_shanks = [b for b in bf if b["type"] == "CYLINDER"]
        self.df_shanks = [b for b in df if b["type"] == "CYLINDER"]
        self.hex_side = 21.0  # default; replaced per pump below
        for b in bf:
            if b["type"] == "EXTRUSION":
                for a in b["attrs"]:
                    # VERTEX profile points sit at U 0 and are small; the
                    # EXTRUSION's own POS carries the world anchor coordinate.
                    m = re.match(
                        r"^POS [EW]\s+([-\d.]+)[a-z]*\s+[NS]\s+([-\d.]+)[a-z]*\s+U\s+0(?:mm)?$",
                        a,
                        re.I,
                    )
                    if m and abs(to_number(m.group(1))) < 500.0:
                        self.hex_side = abs(to_number(m.group(1)))
                        break
                break

        # helper accessors
        def t_of(g: tuple) -> float:
            p, _ = g
            return p[1] if self.long_axis == "E" else p[0]

        def l_of_g(g: tuple) -> float:
            p, _ = g
            return p[0] if self.long_axis == "E" else p[1]

        self._t_of, self._l_of = t_of, l_of_g

    def to_world(self, l: float, t: float, u: float) -> tuple[float, float, float]:
        if self.long_axis == "E":
            return (l, t, u)
        return (t, l, u)

    # ------------------------------------------------------------------
    def frame_members(self) -> list[str]:
        out = ["-- Refined: 5-member longitudinal frame (PUMP006 reference style)"]
        gap = self.t2 - self.t1 - 2 * self.rail_w
        inner_w = min(self.rail_w, max(10.0, gap / 3.0))
        centre_w = max(0.0, gap - 2 * inner_w)
        members = [
            (self.t1, self.rail_w, "outer rail"),
            (self.t2, self.rail_w, "outer rail"),
            (self.t1 + self.rail_w + inner_w / 2, inner_w, "inner rail"),
            (self.t2 - self.rail_w - inner_w / 2, inner_w, "inner rail"),
        ]
        if centre_w >= 10.0:
            members.append(((self.t1 + self.rail_w + self.t2 - self.rail_w) / 2,
                            centre_w, "centre plate"))
        for t, w, label in members:
            e, n, u = self.to_world(self.lc, t, self.frame_bottom + 10.0)
            xl, yl = (w, self.rail_len) if self.long_axis == "N" else (self.rail_len, w)
            out += box_text(e, n, u, xl, yl, 20.0, f"frame {label}")
        return out

    def pump_end_stand(self) -> list[str]:
        """Reference pump-end stand: two side plates + cross beam + a
        pump-end sole plate CARRIED on top of the side plates.

        The stand is emitted only where the full stack fits (side plates
        from the frame top to the pump-end plate bottom, plate top at the
        foot sole-plate top) without the casing/fasteners/nozzles intruding.
        Otherwise it is skipped -- a stand that cannot carry its plate is
        never emitted, so nothing floats.
        """
        cols = sorted({self._t_of(g) for g in self.pump_soles})
        if len(cols) < 2:
            return []
        gap = cols[1] - cols[0]
        if gap < 60.0:
            return []
        sole = [g for g in self.pump_soles if self._l_of(g) == self.pump_end_row][0]
        _, sd = sole
        sole_bottom = sole[0][2] - sd["ZLEN"] / 2
        sole_top = sole[0][2] + sd["ZLEN"] / 2
        short = sd["XLEN"] if self.long_axis == "E" else sd["YLEN"]
        offset = max(15.0, (gap / 2.0) - (short / 2.0 + 15.0))
        t_c = (cols[0] + cols[1]) / 2
        plate_w = 2.0 * (offset + 15.0)
        span = 2.0 * offset - 10.0
        h = sole_bottom - self.frame_top
        if h < 12.0:
            return []

        frame_l0 = self.lc - self.rail_len / 2.0
        frame_l1 = self.lc + self.rail_len / 2.0
        frame_end = frame_l1 if self.pump_end > 0 else frame_l0

        def footprint(l_centre: float, length: float) -> tuple[float, float, float, float]:
            """(t0, l0, t1, l1) of the stand incl. the carried plate."""
            return (
                t_c - offset - 15.0 - 2.0,
                l_centre - length / 2 - 2.0,
                t_c + offset + 15.0 + 2.0,
                l_centre + length / 2 + 2.0,
            )

        length = min(188.0, self.rail_len * 0.35)
        l_c = None
        for length_try in (length, min(length, self.rail_len * 0.25),
                           min(length, self.rail_len * 0.15)):
            if length_try < 60.0:
                break
            for step in (0.0, 40.0, 80.0, 120.0, 160.0):
                cand = frame_end - self.pump_end * (length_try / 2.0 + 2.0 + step)
                if cand - length_try / 2.0 < frame_l0 + 1.0 or \
                   cand + length_try / 2.0 > frame_l1 - 1.0:
                    continue
                fp = footprint(cand, length_try)
                limit = float("inf")
                for sub_name in (
                    self.equi + "_CASING",
                    self.equi + "_CASING_FASTENERS",
                    self.equi + "_SUCTION",
                    self.equi + "_DISCHARGE",
                ):
                    for b in self.by_sub.get(sub_name, []):
                        lo = self.element_aabb(b)
                        if lo is None:
                            continue
                        # overlap in the (long, trans) plane
                        t0_fp, l0_fp, t1_fp, l1_fp = fp
                        if self.long_axis == "N":
                            l_range, t_range = (lo[1], lo[4]), (lo[0], lo[3])
                        else:
                            l_range, t_range = (lo[0], lo[3]), (lo[1], lo[4])
                        lo_l, hi_l = min(l_range), max(l_range)
                        lo_t, hi_t = min(t_range), max(t_range)
                        if hi_l <= l0_fp or lo_l >= l1_fp or hi_t <= t0_fp or lo_t >= t1_fp:
                            continue
                        limit = min(limit, lo[2])
                # The stack spans frame_top..sole_top. A part may rest ON the
                # plate top (contact) but must not intrude more than 2 mm.
                if limit >= sole_top - 2.0:
                    l_c, length = cand, length_try
                    break
            if l_c is not None:
                break
        if l_c is None:
            return []

        out: list[str] = []
        for side in (-1.0, 1.0):
            t = t_c + side * offset
            e, n, u = self.to_world(l_c, t, self.frame_top + h / 2)
            if self.long_axis == "N":
                xl, yl = 10.0, length
            else:
                xl, yl = length, 10.0
            out += box_text(e, n, u, xl, yl, h, "pump-end side plate")
        # cross beam between the side plates (cross tie, not a support)
        beam_h = max(10.0, h - 5.0)
        out += beam_text(l_c, t_c - offset + 5.0, self.frame_top,
                         span, length, beam_h, self.long_axis)
        # pump-end sole plate CARRIED by the two side plates
        e, n, u = self.to_world(l_c, t_c, (sole_bottom + sole_top) / 2.0)
        xl, yl = (plate_w, length) if self.long_axis == "N" else (length, plate_w)
        out += box_text(e, n, u, xl, yl, 16.0,
                        "pump-end sole plate (carried by side plates)")
        return out

    def element_aabb(self, b: dict) -> tuple | None:
        """(x0, y0, z0, x1, y1, z1) AABB in world E/N/U."""
        p, d = block_geom(b)
        if p is None:
            return None
        t = b["type"]
        if t == "BOX":
            return (p[0] - d.get("XLEN", 0) / 2, p[1] - d.get("YLEN", 0) / 2,
                    p[2] - d.get("ZLEN", 0) / 2, p[0] + d.get("XLEN", 0) / 2,
                    p[1] + d.get("YLEN", 0) / 2, p[2] + d.get("ZLEN", 0) / 2)
        if t in ("CYLINDER", "CYLI", "CONE"):
            r = d.get("DIAM", 0) / 2
            h = d.get("HEIG", 0) / 2
            z_axis = "U"
            for a in b["attrs"]:
                m = re.match(r"^ORI\s+.*?\bZ\s+is\s+([EWNSUD])\b", a, re.I)
                if m:
                    z_axis = m.group(1).upper()
                    break
            if z_axis in ("E", "W"):
                return (p[0] - h, p[1] - r, p[2] - r, p[0] + h,
                        p[1] + r, p[2] + r)
            if z_axis in ("N", "S"):
                return (p[0] - r, p[1] - h, p[2] - r, p[0] + r,
                        p[1] + h, p[2] + r)
            return (p[0] - r, p[1] - r, p[2] - h, p[0] + r,
                    p[1] + r, p[2] + h)
        return None

    def diag_web_text(self, l_c: float, t0: float, u0: float, L_p: float,
                      W_web: float, h: float, dx: float, sign: str,
                      kind: str) -> list[str]:
        """One diagonal web: a slanted flat plate (parallelogram profile in
        the longitudinal-vertical plane) extruded across the transverse
        width. sign '+' leans one way, '-' the other (bridge look)."""
        if self.long_axis == "N":
            pe, pn, pu = t0, l_c - L_p / 2, u0
            ori = "ORI Y is U and Z is E"

            def vert(x: float, y: float) -> str:
                return f"POS E 0mm {signed('N', x)} {r1(abs(x))}mm {signed('U', y)} {r1(abs(y))}mm"
        else:
            pe, pn, pu = l_c - L_p / 2, t0, u0
            ori = "ORI Y is U and Z is N"

            def vert(x: float, y: float) -> str:
                return f"POS {signed('E', x)} {r1(abs(x))}mm N 0mm {signed('U', y)} {r1(abs(y))}mm"
        s = dx if sign == "+" else -dx
        l0 = 0.15 * L_p
        l1 = 0.85 * L_p
        pts = [(l0, 0.0), (l1, 0.0), (l1 + s, h), (l0 + s, h)]
        out = [
            f"-- Refined: {kind} diagonal web (bridge bracket, horizontal-diagonal-flat-diagonal-horizontal, Reference Value)",
            "NEW EXTRUSION",
            pos_text(pe, pn, pu),
            ori,
            f"HEIG {r1(W_web)}mm",
            "",
            "NEW LOOP",
            "",
        ]
        for x, y in pts:
            out += ["NEW VERTEX", vert(x, y), "END"]
        out += ["END", "END", ""]
        return out

    def bridge_bracket_text(self, g: tuple, kind: str) -> list[str]:
        """Bridge-shaped support under one platform (foot sole or motor pad):

        platform (existing sole plate / pad)
          diagonal web 2 (\\)
          middle horizontal plate
          diagonal web 1 (/)
          bottom auxiliary block, bolted to the frame

        Side cross-section reads horizontal-diagonal-flat-diagonal-horizontal (a bridge). The diagonal
        webs touch the platform bottom and the middle plate, and the block
        carries the lower web. The old PYRAMID gussets are not used.
        """
        p, d = g
        zl = d["ZLEN"]
        bottom = p[2] - zl / 2
        gap = bottom - self.frame_top
        if gap < 12.0:
            return []
        L_p = d["XLEN"] if self.long_axis == "E" else d["YLEN"]
        W_p = d["YLEN"] if self.long_axis == "E" else d["XLEN"]
        l = self._l_of(g)
        t = self._t_of(g)
        block_h, mid_h = self.bracket_heights(gap)
        block_top = self.frame_top + block_h
        remaining = gap - block_h - mid_h
        web1_h = remaining / 2.0
        web2_h = remaining / 2.0
        mid_bottom = block_top + web1_h
        mid_top = mid_bottom + mid_h
        hex_side, W_web = self.bracket_web_span(W_p)
        dx = 0.10 * L_p

        out: list[str] = []
        # bottom auxiliary block (bolted to the frame)
        e, n, u = self.to_world(l, t, self.frame_top + block_h / 2.0)
        xl, yl = (W_p, L_p) if self.long_axis == "N" else (L_p, W_p)
        out += box_text(e, n, u, xl, yl, block_h,
                        f"{kind} auxiliary block (bolted)")
        # lower diagonal web: block top -> middle plate bottom
        t0 = t - W_web / 2.0
        out += self.diag_web_text(l, t0, block_top, L_p, W_web, web1_h, dx,
                                  "+", kind)
        # middle horizontal plate (same longitudinal band as the webs)
        e, n, u = self.to_world(l, t, (mid_bottom + mid_top) / 2.0)
        mid_l = 0.7 * L_p
        xl, yl = (W_web, mid_l) if self.long_axis == "N" else (mid_l, W_web)
        out += box_text(e, n, u, xl, yl, mid_h, f"{kind} middle plate")
        # upper diagonal web: middle plate top -> platform bottom
        out += self.diag_web_text(l, t0, mid_top, L_p, W_web, web2_h, dx,
                                  "-", kind)
        return out

    def bracket_web_span(self, W_p: float) -> tuple[float, float]:
        """(hex side, web transverse width) so the block-edge screws (at
        W_p/2-16 from the centre) sit beside the webs, clear of them."""
        if W_p >= 90.0:
            hex_side = min(self.hex_side * 0.8, 11.0)
            W_web = max(20.0, W_p - 2.0 * (hex_side + 18.0))
        else:
            W_web = 20.0
            hex_side = min(11.0, max(6.0, W_p / 2.0 - 28.0))
        return hex_side, W_web

    def bracket_heights(self, gap: float) -> tuple[float, float]:
        """(block height, middle-plate height) scaled to the available gap
        so even short supports keep the horizontal-diagonal-flat-diagonal-horizontal profile."""
        if gap >= 40.0:
            return 12.0, 8.0
        block = max(6.0, gap * 0.35)
        mid = max(4.0, gap * 0.15)
        return block, mid

    def screw_texts(self, g: tuple, kind: str, diam: float) -> list[str]:
        """Two screws fixing the bottom auxiliary block at its longitudinal
        ends (clear of the diagonal webs), nut on the block top."""
        p, d = g
        W_p = d["YLEN"] if self.long_axis == "E" else d["XLEN"]
        l = self._l_of(g)
        t = self._t_of(g)
        gap = p[2] - d["ZLEN"] / 2 - self.frame_top
        block_h, _ = self.bracket_heights(gap)
        block_top = self.frame_top + block_h
        shank_bottom = self.base_top - 8.7
        nut_heig = 10.6
        hex_side, _ = self.bracket_web_span(W_p)
        out: list[str] = []
        for ds in (-1.0, 1.0):
            at = t + ds * (W_p / 2.0 - 16.0)
            ae, an, _ = self.to_world(l, at, 0.0)
            out += shank_text(ae, an, shank_bottom, block_top + nut_heig, diam)
            out += hex_text(ae, an, block_top, nut_heig, hex_side,
                            f"{kind} block nut")
        return out


def sube_span(lines: list[str], header_index: int) -> int:
    """Index of the SUBE's own closing END line."""
    i = header_index + 1
    while i < len(lines):
        s = lines[i].strip()
        if s.upper().startswith("NEW SUBEQUIPMENT") or s.upper().startswith("NEW EQUIPMENT"):
            j = i - 1
            while j > header_index and not lines[j].strip():
                j -= 1
            if END_RE.match(lines[j].strip()):
                return j
            return j
        i += 1
    return len(lines) - 1


def main() -> None:
    lines = SRC.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks = parse(lines)
    by_sub = defaultdict(list)
    for b in blocks:
        by_sub[(b["equi"], b["sub"])].append(b)

    equis = sorted({b["equi"] for b in blocks})
    frames = {eq: PumpFrame(blocks, eq) for eq in equis}
    ops: list[tuple[int, int, list[str]]] = []

    for eq in equis:
        pf = frames[eq]
        # ---- SUPPORT_FRAME ----
        for i, ln in enumerate(lines):
            if ln.strip().upper().startswith("NEW SUBEQUIPMENT") and eq + "_SUPPORT_FRAME" in ln:
                end = sube_span(lines, i)
                new = pf.frame_members() + pf.pump_end_stand()
                # keep the sole plates in their original order, rebuild gussets
                sole_blocks = sorted(
                    [b for b in by_sub[(eq, eq + "_SUPPORT_FRAME")]
                     if b["type"] == "BOX"
                     and 9 <= block_geom(b)[1].get("ZLEN", 0) <= 17
                     and block_geom(b)[0][2] > 90],
                    key=lambda b: b["start"],
                )
                for sb in sole_blocks:
                    new += lines[sb["start"]:sb["end"] + 1] + [""]
                    g = block_geom(sb)
                    new += pf.bridge_bracket_text(g, "pump")
                ops.append((i + 1, end - 1, new))
                break

        # ---- BASE_FASTENERS ----
        for i, ln in enumerate(lines):
            if ln.strip().upper().startswith("NEW SUBEQUIPMENT") and eq + "_BASE_FASTENERS" in ln:
                end = sube_span(lines, i)
                new: list[str] = []
                diam = block_geom(pf.bf_shanks[0])[1].get("DIAM", 17.0) if pf.bf_shanks else 17.0
                for g in sorted(pf.pump_soles, key=lambda x: (x[0][0], x[0][1])):
                    new += pf.screw_texts(g, "BASE", diam)
                ops.append((i + 1, end - 1, new))
                break

        # ---- DRIVER_FASTENERS ----
        for i, ln in enumerate(lines):
            if ln.strip().upper().startswith("NEW SUBEQUIPMENT") and eq + "_DRIVER_FASTENERS" in ln:
                end = sube_span(lines, i)
                new = []
                diam = block_geom(pf.df_shanks[0])[1].get("DIAM", 17.0) if pf.df_shanks else 17.0
                for g in sorted(pf.motor_pads, key=lambda x: (x[0][0], x[0][1])):
                    new += pf.screw_texts(g, "DRIVER", diam)
                ops.append((i + 1, end - 1, new))
                break

        # ---- DRIVER: replace pad gussets ----
        pad_blocks = pf.pad_blocks
        for pb in pad_blocks:
            g = block_geom(pb)
            new = lines[pb["start"]:pb["end"] + 1] + [""] + pf.bridge_bracket_text(g, "motor")
            ops.append((pb["start"], pb["end"], new))
        for pb in pf.pyr_dr_blocks:
            ops.append((pb["start"], pb["end"], []))

    # delete old SUPPORT_FRAME gussets and cross plates (inside replaced range)
    # apply ops bottom-up
    ops.sort(key=lambda x: x[0], reverse=True)
    out_lines = list(lines)
    for start, end, text in ops:
        if end < start:
            continue
        out_lines[start:end + 1] = text

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Line count: {len(lines)} -> {len(out_lines)}")


if __name__ == "__main__":
    main()
