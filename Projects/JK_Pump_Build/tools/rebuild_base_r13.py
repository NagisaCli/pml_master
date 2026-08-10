"""r13 -- casing feet + clash-free hold-downs.

Starting point: JK_Pump_Build_refined_20260805_r12.pml
Output:         JK_Pump_Build_refined_20260805_r13.pml

Client bugs from the r12 E3D reload:

  bug 1  "There is a collision between the bolts and the support legs."
         Measured: 1,700 intersections between fastener solids and
         pedestal/plate solids across all 30 pumps. The r12 anchors were
         placed on the plate's long centreline and run from inside the frame
         to a nut above the plate, so every shank pierced the sole plate, the
         pedestal flange and (at the motor) the pad stack.

  bug 2  "It is not considered an effective support; the base structure should
         better match the pump geometry, with a precise and proper interface
         between the base and the pump body."
         Measured: the pump casing is a horizontal barrel of radius R whose
         axis is the pump centreline. The bearing plates sit ~0.91*R to each
         side of that axis, i.e. under the barrel's steeply curved flank. A
         flat plate meeting a round barrel there touches on a tangent sliver
         only (28-51% AABB overlap, no real bearing area). Nothing brings the
         round casing down to a flat machined pad.

r13 fixes both:

  A. CASING FEET (new, in CASING scope)
     Each pump gets cast support feet that do what a real pump foot does:
     take the round casing flank and carry it out and down to a flat
     machined pad exactly on the pedestal plate top. Each foot is
       - a vertical rib rising from the pad into the barrel flank (so it
         merges with the casting instead of floating beside it), and
       - a flat sole pad whose underside IS the pedestal plate top.
     The pad plan is matched to the pedestal plate, so the interface is
     flat-on-flat over the full plate area instead of a tangent line.

  B. HOLD-DOWNS MOVED TO A CLEAR ZONE
     Bolts now sit in the plan gap BESIDE the casing foot rib and BETWEEN the
     pedestal webs, and the shank stops at the plate top instead of running
     through it. Each bolt is checked against every pedestal/plate/foot solid
     before it is emitted; a bolt that cannot be placed clear is not emitted
     at all rather than being drawn through steel.

Bearing plate elevations, pump positions, nozzles, baseplate dimensions and
all locked scope are unchanged. New dimensions are Reference Values.
"""

from __future__ import annotations

import math
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebuild_base_r12 import (  # noqa: E402
    parse, aabb, block_geom, pos_text, r1, signed,
    box_text, hex_text, shank_text, sube_span, HEX_H,
)

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "output" / "JK_Pump_Build_refined_20260805_r12.pml"
OUT = BASE / "output" / "JK_Pump_Build_refined_20260805_r13.pml"

FOOT_PAD_T = 18.0     # machined sole pad thickness
# The r12 pedestal webs ran to within 4 mm of the plate ends and spanned its
# full width, so there was physically nowhere on the plate for a hold-down.
# Shortening the webs creates a real bolt zone at each end -- which is how a
# fabricated pedestal is actually detailed.
WEB_END_CLEAR = 34.0  # web end held back this far from the plate end
RIB_T = 14.0          # cast rib thickness
RIB_SPAN = 0.45       # rib length as a fraction of the pad, leaving the pad
                      # ends clear for the hold-down bolts
BOLT_CLEAR = 2.0      # required clearance between a bolt and any steel


def is_vertical(g):
    """A member a bolt must sit beside rather than pass through.

    A vertical plate is TALLER than it is thin: its height must dominate its
    smallest plan dimension. A long flat cross-beam (454 x 40 x 33) is wide,
    not tall, and a hold-down may pass through it exactly as it passes
    through the bearing plate.

    Shared by the generator and `verify_r13.py` -- when these two definitions
    drifted apart (40 mm here, 60 mm there) the generator happily placed
    bolts through members the verifier then flagged.
    """
    h = g[5] - g[4]
    thin = min(g[1] - g[0], g[3] - g[2])
    return h > 25.0 and thin < 60.0 and h > thin


def boxes_intersect(a, b, clear=0.0):
    """True if `a` comes within `clear` of `b`.

    `clear` GROWS the test box -- it is a required separation, not a licence
    to overlap. Writing `overlap > clear` (the earlier form) inverted this:
    a 1.9 mm interference passed a 2.0 mm "clearance" check, which is exactly
    how bolts ended up 1.9 mm inside the pedestal webs.
    """
    return (min(a[1], b[1]) - max(a[0], b[0]) > -clear and
            min(a[3], b[3]) - max(a[2], b[2]) > -clear and
            min(a[5], b[5]) - max(a[4], b[4]) > -clear)


def cyl_aabb(e, n, u0, u1, diam):
    r = diam / 2
    return (e - r, e + r, n - r, n + r, u0, u1)


def casing_foot(plate, barrel_axis_e, barrel_axis_n, barrel_r,
                barrel_centre_u, long_axis):
    """Cast foot carrying the round casing flank onto a flat pad.

    plate = the pedestal bearing plate AABB (its TOP is the machined face).

    Section across the pump axis:

          )   <- barrel flank (round)
         /|
        / |   <- cast rib, merges into the flank
       +--+   <- flat sole pad, underside on the plate top
       ====   <- pedestal plate (already correct, untouched)
    """
    e0, e1, n0, n1, u0, u1 = plate
    ce, cn = (e0 + e1) / 2, (n0 + n1) / 2
    pad_top = u1 + FOOT_PAD_T
    out: list[str] = []
    solids: list[tuple] = []          # AABBs of what this foot actually emits

    # Flat machined sole pad, footprint = the plate (a true flat interface).
    out += box_text(ce, cn, u1 + FOOT_PAD_T / 2,
                    e1 - e0, n1 - n0, FOOT_PAD_T,
                    "casing foot machined sole pad (flat interface on pedestal)")
    solids.append((e0, e1, n0, n1, u1, pad_top))

    # Rib from the pad up into the barrel flank. It must reach far enough
    # inboard/upward to be inside the barrel surface, so it visibly merges
    # with the casting rather than stopping in mid air.
    if long_axis == "N":
        # barrel axis runs N; lateral offset is along E
        lateral = ce - barrel_axis_e
        d = abs(lateral)
        if d >= barrel_r:
            return out, solids
        # barrel surface height directly above the rib centre
        surf_u = barrel_centre_u - math.sqrt(max(barrel_r ** 2 - d ** 2, 1.0))
        rib_h = max(surf_u - pad_top, 0.0) + 14.0   # overlap into the casting
        if rib_h > 4.0:
            rib_e = ce + (RIB_T / 2) * (-1 if lateral > 0 else 1)
            rib_d = (n1 - n0) * RIB_SPAN
            out += box_text(rib_e, cn, pad_top + rib_h / 2,
                            RIB_T, rib_d, rib_h,
                            "casing foot cast rib (merges into casing flank)")
            solids.append((rib_e - RIB_T / 2, rib_e + RIB_T / 2,
                           cn - rib_d / 2, cn + rib_d / 2,
                           pad_top, pad_top + rib_h))
    else:
        lateral = cn - barrel_axis_n
        d = abs(lateral)
        if d >= barrel_r:
            return out, solids
        surf_u = barrel_centre_u - math.sqrt(max(barrel_r ** 2 - d ** 2, 1.0))
        rib_h = max(surf_u - pad_top, 0.0) + 14.0
        if rib_h > 4.0:
            rib_n = cn + (RIB_T / 2) * (-1 if lateral > 0 else 1)
            rib_w = (e1 - e0) * RIB_SPAN
            out += box_text(ce, rib_n, pad_top + rib_h / 2,
                            rib_w, RIB_T, rib_h,
                            "casing foot cast rib (merges into casing flank)")
            solids.append((ce - rib_w / 2, ce + rib_w / 2,
                           rib_n - RIB_T / 2, rib_n + RIB_T / 2,
                           pad_top, pad_top + rib_h))
    return out, solids


def clear_bolts(plate, frame_top, obstacles, hex_side, bolt_d, kind,
                seat_top=None, want=None):
    """Hold-downs placed in a plan zone that hits no VERTICAL steel.

    A hold-down bolt is supposed to pass through the horizontal plates it
    clamps -- that is what clamping means, and the client's complaint was not
    about that. The r12 defect was the shank running through the pedestal
    WEBS and the casing foot: vertical members it should sit beside.

    So `obstacles` here must contain only the vertical members. Candidate
    positions are the plate corners, where a real hold-down goes and where
    the webs (which run under the plate edges) are not.
    """
    e0, e1, n0, n1, u0, u1 = plate
    ce, cn = (e0 + e1) / 2, (n0 + n1) / 2
    # the nut seats on whatever is actually the top face here: the bearing
    # plate, or the casing foot pad stacked on it
    if seat_top is not None:
        u1 = seat_top
    out: list[str] = []
    placed = 0
    hx = max(hex_side, bolt_d * 0.9)
    # Bolt patterns are ALWAYS symmetric about the plate centre and always
    # fully inside the plate. An earlier version allowed the pattern to slide
    # off-centre to dodge steel; that produced four bolts crammed into the
    # top 15 mm of a 160 mm plate with two of them 0.2 mm over the edge.
    # A hold-down that is merely clash-free is not correct -- it must also
    # look like a bolt pattern.
    edge = max(1.5 * bolt_d, hx + 3.0)      # min centre-to-edge distance
    max_ix = (e1 - e0) / 2 - edge
    max_iy = (n1 - n0) / 2 - edge
    if max_ix <= 2.0 or max_iy <= 2.0:
        return out

    steps = 16
    offs_x = [max_ix * (1.0 - k / steps) for k in range(steps + 1)]
    offs_y = [max_iy * (1.0 - k / steps) for k in range(steps + 1)]
    offs_x = [v for v in offs_x if v >= 6.0]
    offs_y = [v for v in offs_y if v >= 6.0]

    cand: list[tuple[float, list[tuple[float, float]]]] = []
    # 4-bolt rectangle, centred, widest spread first
    for ix in offs_x:
        for iy in offs_y:
            cand.append((-(ix + iy) - 1e6,          # 4-bolt always beats 2
                         [(ce - ix, cn - iy), (ce + ix, cn - iy),
                          (ce - ix, cn + iy), (ce + ix, cn + iy)]))
    # 2-bolt pairs on a centreline, for plates whose webs leave no room for
    # four -- still symmetric about the plate centre.
    for iy in offs_y:
        cand.append((-iy, [(ce, cn - iy), (ce, cn + iy)]))
    for ix in offs_x:
        cand.append((-ix, [(ce - ix, cn), (ce + ix, cn)]))
    cand.sort(key=lambda q: q[0])
    quads = [q for _, q in cand]

    if want is not None:
        quads = [q for q in quads if len(q) == want]
    for quad in quads:
        ok = True
        for be, bn in quad:
            shank = cyl_aabb(be, bn, frame_top - 10.0, u1 + HEX_H, bolt_d)
            nut = cyl_aabb(be, bn, u1, u1 + HEX_H, hx * 2)
            if any(boxes_intersect(shank, o, BOLT_CLEAR) or
                   boxes_intersect(nut, o, BOLT_CLEAR) for o in obstacles):
                ok = False
                break
        if not ok:
            continue
        for be, bn in quad:
            # shank runs from inside the frame up to the nut top, clamping
            # the plate stack it passes through
            out += shank_text(be, bn, frame_top - 10.0, u1 + HEX_H, bolt_d)
            out += hex_text(be, bn, u1, HEX_H, hx,
                            f"{kind} hold-down nut on plate top (clear of webs)")
            placed += 1
        break
    return out


def main() -> None:
    lines = SRC.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks = parse(lines)
    by = defaultdict(list)
    for b in blocks:
        if b["equi"]:
            by[(b["equi"], b["sub"])].append(b)

    equis = sorted({b["equi"] for b in blocks if b["equi"]})
    ops: list[tuple[int, int, list[str]]] = []
    st = defaultdict(int)

    for eq in equis:
        sf = by[(eq, eq + "_SUPPORT_FRAME")]
        dr = by[(eq, eq + "_DRIVER")]
        ca = by[(eq, eq + "_CASING")]
        bp = by[(eq, eq + "_BASEPLATE")]
        if not sf or not bp:
            continue
        bpb = aabb([b for b in bp if b["type"] == "BOX"][0])
        long_axis = "E" if (bpb[1] - bpb[0]) >= (bpb[3] - bpb[2]) else "N"

        rails = [b for b in sf if b["type"] == "BOX"
                 and abs(aabb(b)[5] - aabb(b)[4] - 20.0) < 0.6
                 and max(aabb(b)[1] - aabb(b)[0], aabb(b)[3] - aabb(b)[2]) > 500]
        frame_top = max((aabb(b)[5] for b in rails), default=bpb[5] + 20.0)

        bolt_d, hex_side = 17.0, 11.0
        for b in by[(eq, eq + "_BASE_FASTENERS")]:
            if b["type"] == "CYLINDER":
                bolt_d = block_geom(b)[1].get("DIAM", 17.0)
                break

        # ---- barrel of the casing (the thing the feet must merge into) ----
        barrel = None
        for b in ca:
            pos, d, ori = block_geom(b)
            if b["type"] == "CYLINDER" and d.get("DIAM", 0) > 150:
                v = d["DIAM"] * d.get("HEIG", 0)
                if barrel is None or v > barrel[0]:
                    barrel = (v, pos, d)
        if barrel is None:
            continue
        _, bpos, bdim = barrel
        b_r = bdim["DIAM"] / 2
        b_axis_e, b_axis_n, b_centre_u = bpos

        # ---- pump-end bearing plates ----
        plates = [aabb(b) for b in sf if b["type"] == "BOX"
                  and 9 <= (aabb(b)[5] - aabb(b)[4]) <= 18
                  and aabb(b)[4] > frame_top + 20]

        # Obstacles for a bolt = the VERTICAL members only (pedestal webs,
        # stiffeners, cross-beams, and the casing itself). Horizontal plates
        # are meant to be clamped through.
        obst = [aabb(b) for b in sf + ca
                if aabb(b) and is_vertical(aabb(b))]

        # A. casing feet -> appended into the CASING SUBE.
        # Build the complete foot geometry FIRST, then add every rib to the
        # obstacle set, then place bolts. Adding ribs while iterating meant
        # early plates were tested against an incomplete obstacle set and
        # their bolts landed inside ribs emitted later.
        feet_txt: list[str] = []
        for pl in plates:
            t, foot_solids = casing_foot(pl, b_axis_e, b_axis_n, b_r,
                                         b_centre_u, long_axis)
            if t:
                feet_txt += t
                st["feet"] += 1
                # Obstacles derive from the geometry actually emitted, so the
                # clash test can never disagree with what is in the file.
                obst += [s for s in foot_solids if is_vertical(s)]
        if feet_txt:
            last = max(ca, key=lambda b: b["end"])
            ops.append((last["end"] + 1, last["end"], [""] + feet_txt))

        # B. pump-end hold-downs, clash-checked
        for i, ln in enumerate(lines):
            if ln.strip().upper().startswith("NEW SUBEQUIPMENT") and \
               (eq + "_BASE_FASTENERS") in ln:
                end = sube_span(lines, i)
                # All feet of one pump must get the SAME pattern -- four bolts
                # on two pedestals and two on the others reads as a mistake.
                # Find the count every plate can achieve, then emit that.
                # Hold-downs go through the pedestal's BOTTOM FLANGE, which
                # projects ~8 mm beyond the bearing plate on every side and
                # is clear of the webs. The bearing plate itself is fully
                # occupied by the webs and the machine foot -- trying to bolt
                # through it is what produced every earlier bad placement.
                flanges = []
                for pl in plates:
                    best = None
                    for b in sf:
                        g = aabb(b)
                        if (not g or b["type"] != "BOX"
                                or abs(g[4] - frame_top) > 0.6
                                or (g[5] - g[4]) > 20.0):
                            continue
                        if (min(pl[1], g[1]) - max(pl[0], g[0]) > 0 and
                                min(pl[3], g[3]) - max(pl[2], g[2]) > 0):
                            best = g
                            break
                    flanges.append(best if best is not None else pl)
                seats = [f[5] for f in flanges]
                trial = [clear_bolts(f, frame_top, obst, hex_side, bolt_d,
                                     "pump", seat_top=s)
                         for f, s in zip(flanges, seats)]
                counts = [t.count("NEW CYLINDER") for t in trial]
                # smallest NON-ZERO count: a plate that can take no bolt at
                # all must not strip the bolts off every other plate.
                nz = [c for c in counts if c]
                common = min(nz) if nz else 0
                txt: list[str] = []
                for fl, s, t, c in zip(flanges, seats, trial, counts):
                    if c == 0 or common == 0:
                        continue
                    if c != common:
                        t = clear_bolts(fl, frame_top, obst, hex_side, bolt_d,
                                        "pump", seat_top=s, want=common)
                    txt += t
                    st["bolts_pump"] += t.count("NEW CYLINDER")
                ops.append((i + 1, end - 1, txt))
                break

        # ---- motor end: pads keep their stack; bolts move clear ----
        drb = [(b, aabb(b)) for b in dr]
        drb = [(b, g) for b, g in drb if g]
        feet_m = [g for b, g in drb if b["type"] == "BOX"
                  and (g[5] - g[4]) > 40 and g[4] < 400]
        pads = []
        for b, g in drb:
            if b["type"] != "BOX":
                continue
            if not (8 <= (g[5] - g[4]) <= 17 and frame_top + 20 < g[4] < 320):
                continue
            if any(abs(f[4] - g[5]) < 1.0
                   and min(f[1], g[1]) - max(f[0], g[0]) > 0.5
                   and min(f[3], g[3]) - max(f[2], g[2]) > 0.5 for f in feet_m):
                pads.append(g)
        # motor side: vertical members (pedestal webs, motor feet blocks)
        obst_m = [g for b, g in drb if is_vertical(g)]
        for i, ln in enumerate(lines):
            if ln.strip().upper().startswith("NEW SUBEQUIPMENT") and \
               (eq + "_DRIVER_FASTENERS") in ln:
                end = sube_span(lines, i)
                # Same as the pump end: bolt the pedestal bottom flange,
                # which projects beyond the pad and is clear of the webs.
                mflanges = []
                for pd in pads:
                    best = None
                    for b, g in drb:
                        if (b["type"] != "BOX"
                                or abs(g[4] - frame_top) > 0.6
                                or (g[5] - g[4]) > 20.0):
                            continue
                        if (min(pd[1], g[1]) - max(pd[0], g[0]) > 0 and
                                min(pd[3], g[3]) - max(pd[2], g[2]) > 0):
                            best = g
                            break
                    mflanges.append(best if best is not None else pd)
                trial = [clear_bolts(f, frame_top, obst_m, hex_side, bolt_d,
                                     "motor", seat_top=f[5])
                         for f in mflanges]
                counts = [t.count("NEW CYLINDER") for t in trial]
                nz = [c for c in counts if c]
                common = min(nz) if nz else 0
                txt = []
                for fl, t, c in zip(mflanges, trial, counts):
                    if c == 0 or common == 0:
                        continue
                    if c != common:
                        t = clear_bolts(fl, frame_top, obst_m, hex_side,
                                        bolt_d, "motor", seat_top=fl[5],
                                        want=common)
                    txt += t
                    st["bolts_motor"] += t.count("NEW CYLINDER")
                ops.append((i + 1, end - 1, txt))
                break

    # Apply bottom-up. Inserts are encoded as (start, start-1, text); the
    # slice assignment handles them naturally, so they must NOT be skipped.
    ops.sort(key=lambda x: (x[0], x[1]), reverse=True)
    prev_start = None
    dropped = 0
    out_lines = list(lines)
    for start, end, text in ops:
        if prev_start is not None and end >= prev_start:
            dropped += 1
            continue
        out_lines[start:end + 1] = text
        prev_start = start
    if dropped:
        print(f"  WARNING: {dropped} overlapping ops dropped")

    OUT.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  lines {len(lines)} -> {len(out_lines)}")
    for k, v in sorted(st.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
