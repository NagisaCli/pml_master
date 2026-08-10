"""r13 verification -- the two client bugs from the r12 E3D reload.

bug 1  "There is a collision between the bolts and the support legs."
       -> ZERO intersections between any fastener solid and any vertical
          structural member (pedestal web, stiffener, casing-foot rib,
          motor foot). A bolt may pass through the horizontal plates it
          clamps; that is what a hold-down does.

bug 2  "It is not considered an effective support ... precise and proper
       interface between the base and the pump body."
       -> every pump-end pedestal carries a casing foot whose flat machined
          pad sits fully on the pedestal plate, and whose cast rib reaches
          up into the casing barrel. The pump/base interface must be
          flat-on-flat over the whole plate, not a tangent line on a round
          barrel.

Plus the r12 properties that must not regress: continuous support chain,
no voids, bearing plates unmoved, locked scope byte-identical.
"""

from __future__ import annotations

import math
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebuild_base_r12 import parse, aabb, block_geom  # noqa: E402
from rebuild_base_r13 import FOOT_PAD_T, is_vertical  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
R12 = BASE / "output" / "JK_Pump_Build_refined_20260805_r12.pml"
R13 = BASE / "output" / "JK_Pump_Build_refined_20260805_r13.pml"

TOL = 0.6


def inter(a, b, clear=0.0):
    return (min(a[1], b[1]) - max(a[0], b[0]) > clear and
            min(a[3], b[3]) - max(a[2], b[2]) > clear and
            min(a[5], b[5]) - max(a[4], b[4]) > clear)


def plan_ov(a, b):
    ox = min(a[1], b[1]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[2], b[2])
    if ox <= 0 or oy <= 0:
        return 0.0
    area = (a[1] - a[0]) * (a[3] - a[2])
    return (ox * oy) / area if area else 0.0


def load(p):
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    by = defaultdict(list)
    for b in parse(lines):
        if b["equi"]:
            by[(b["equi"], b["sub"])].append(b)
    return lines, by


def main() -> int:
    l12, by12 = load(R12)
    l13, by13 = load(R13)
    equis = sorted({k[0] for k in by13})
    fails: list[str] = []
    st = defaultdict(int)

    for eq in equis:
        sf = by13[(eq, eq + "_SUPPORT_FRAME")]
        dr = by13[(eq, eq + "_DRIVER")]
        ca = by13[(eq, eq + "_CASING")]
        bf = by13[(eq, eq + "_BASE_FASTENERS")]
        df = by13[(eq, eq + "_DRIVER_FASTENERS")]
        bp = by13[(eq, eq + "_BASEPLATE")]
        bpb = aabb([b for b in bp if b["type"] == "BOX"][0])

        rails = [b for b in sf if b["type"] == "BOX"
                 and abs(aabb(b)[5] - aabb(b)[4] - 20.0) < 0.6
                 and max(aabb(b)[1] - aabb(b)[0], aabb(b)[3] - aabb(b)[2]) > 500]
        frame_top = max((aabb(b)[5] for b in rails), default=bpb[5] + 20.0)

        # ---------- bug 1: bolts vs vertical steel ----------
        verticals = [aabb(b) for b in sf + dr + ca if aabb(b) and is_vertical(aabb(b))]
        for f in bf + df:
            g = aabb(f)
            if not g:
                continue
            st["fasteners"] += 1
            for v in verticals:
                if inter(g, v, 0.05):
                    fails.append(
                        f"{eq} BOLT/STRUCTURE COLLISION at "
                        f"E{g[0]:.0f} N{g[2]:.0f} U{g[4]:.0f}")
                    st["collisions"] += 1
                    break

        # ---------- bolt POSITIONS must be plausible, not just clash-free ---
        # "0 collisions" only proves the bolts miss the steel. A hold-down
        # must also sit inside the plate it clamps, keep a sane edge distance,
        # and form a pattern symmetric about the plate centre.
        # Pump hold-downs go through the pedestal bottom FLANGE (seated on the
        # frame top), not the bearing plate -- see rebuild_base_r13.
        pump_plates = [aabb(b) for b in sf if b["type"] == "BOX"
                       and abs(aabb(b)[4] - frame_top) < 0.6
                       and (aabb(b)[5] - aabb(b)[4]) <= 20.0
                       and max(aabb(b)[1] - aabb(b)[0],
                               aabb(b)[3] - aabb(b)[2]) < 500]
        drb_ = [(b, aabb(b)) for b in dr]
        drb_ = [(b, g) for b, g in drb_ if g]
        feet_ = [g for b, g in drb_ if b["type"] == "BOX"
                 and (g[5] - g[4]) > 40 and g[4] < 400]
        # motor hold-downs also go through the pedestal bottom flange
        motor_pads = [g for b, g in drb_ if b["type"] == "BOX"
                      and abs(g[4] - frame_top) < 0.6
                      and (g[5] - g[4]) <= 20.0]
        for plates_, fasteners, label in (
                (pump_plates, bf, "pump"), (motor_pads, df, "motor")):
            shanks = [aabb(x) for x in fasteners if x["type"] == "CYLINDER"]
            counts = []
            for pl in plates_:
                mine = [s for s in shanks if plan_ov(pl, s) > 0]
                if not mine:
                    continue
                counts.append(len(mine))
                cx, cy = (pl[0] + pl[1]) / 2, (pl[2] + pl[3]) / 2
                for s in mine:
                    dia = s[1] - s[0]
                    if (s[0] < pl[0] - 0.01 or s[1] > pl[1] + 0.01 or
                            s[2] < pl[2] - 0.01 or s[3] > pl[3] + 0.01):
                        fails.append(
                            f"{eq} {label} bolt hangs off its plate at "
                            f"E{(s[0]+s[1])/2:.0f} N{(s[2]+s[3])/2:.0f}")
                    ed = min((s[0]+s[1])/2 - pl[0], pl[1] - (s[0]+s[1])/2,
                             (s[2]+s[3])/2 - pl[2], pl[3] - (s[2]+s[3])/2)
                    if ed < 1.4 * dia:
                        fails.append(
                            f"{eq} {label} bolt edge distance {ed:.1f} mm "
                            f"< 1.4x dia ({dia:.0f})")
                ox = sum((s[0]+s[1])/2 - cx for s in mine) / len(mine)
                oy = sum((s[2]+s[3])/2 - cy for s in mine) / len(mine)
                if abs(ox) > 1.0 or abs(oy) > 1.0:
                    fails.append(
                        f"{eq} {label} bolt group off-centre by "
                        f"E{ox:+.1f} N{oy:+.1f}")
                st["bolt_groups"] += 1
            if len(set(counts)) > 1:
                fails.append(
                    f"{eq} {label} feet got different bolt counts {counts}")

        # ---------- bug 2: casing feet give a flat interface ----------
        plates = [aabb(b) for b in sf if b["type"] == "BOX"
                  and 9 <= (aabb(b)[5] - aabb(b)[4]) <= 18
                  and aabb(b)[4] > frame_top + 20]
        pads = [aabb(b) for b in ca if b["type"] == "BOX"
                and abs((aabb(b)[5] - aabb(b)[4]) - FOOT_PAD_T) < 0.6]
        if not pads:
            fails.append(f"{eq} has NO casing feet (bug 2 unfixed)")
        for pl in plates:
            match = [p for p in pads if abs(p[4] - pl[5]) < TOL
                     and plan_ov(pl, p) > 0.95]
            if not match:
                fails.append(
                    f"{eq} pedestal plate at U{pl[5]:.1f} has no flat casing "
                    f"foot pad on it")
                continue
            st["flat_interfaces"] += 1

        # the cast rib must actually reach into the barrel
        barrel = None
        for b in ca:
            pos, d, ori = block_geom(b)
            if b["type"] == "CYLINDER" and d.get("DIAM", 0) > 150:
                v = d["DIAM"] * d.get("HEIG", 0)
                if barrel is None or v > barrel[0]:
                    barrel = (v, pos, d)
        if barrel:
            _, bpos, bdim = barrel
            r = bdim["DIAM"] / 2
            ribs = [aabb(b) for b in ca if b["type"] == "BOX"
                    and (aabb(b)[5] - aabb(b)[4]) > 4
                    and abs((aabb(b)[5] - aabb(b)[4]) - FOOT_PAD_T) > 0.6]
            for rb in ribs:
                st["ribs"] += 1
                # rib top must be at/above the barrel surface over its centre
                ce = (rb[0] + rb[1]) / 2
                cn = (rb[2] + rb[3]) / 2
                dE = abs(ce - bpos[0])
                dN = abs(cn - bpos[1])
                d_lat = min(dE, dN)
                if d_lat < r:
                    surf = bpos[2] - math.sqrt(max(r * r - d_lat * d_lat, 1.0))
                    if rb[5] < surf - 1.0:
                        fails.append(
                            f"{eq} casing foot rib stops {surf - rb[5]:.1f} mm "
                            f"below the barrel surface")

        # ---------- r12 properties must not regress ----------
        allb = [aabb(b) for b in sf + dr if aabb(b)]
        for pl in plates:
            unders = [x for x in allb if x is not pl and plan_ov(pl, x) > 0.05
                      and x[5] <= pl[4] + 1.0 and x[5] > frame_top - 0.1]
            if not unders:
                fails.append(f"{eq} plate at U{pl[4]:.1f} unsupported")
                continue
            void = pl[4] - max(x[5] for x in unders)
            if void > 1.0:
                fails.append(f"{eq} VOID {void:.1f} mm under plate")
            st["chain"] += 1

        lowest = min([x[4] for x in allb] + [bpb[4]])
        if lowest < -0.1:
            fails.append(f"{eq} lowest point U{lowest:.1f}")

    # ---------- locked scope ----------
    LOCKED = ("_BASEPLATE", "_CASING_FASTENERS", "_BEARING_FRAME",
              "_SUCTION", "_DISCHARGE", "_COUPLING", "_SERVICE_DETAILS")
    for eq in equis:
        for suf in LOCKED:
            a = [tuple(x["attrs"]) for x in by12.get((eq, eq + suf), [])]
            b = [tuple(x["attrs"]) for x in by13.get((eq, eq + suf), [])]
            if a != b:
                fails.append(f"{eq}{suf} CHANGED (locked scope)")
            else:
                st["locked_ok"] += 1
        # SUPPORT_FRAME: r13 shortens the pedestal webs to open a bolt zone,
        # so it is not byte-identical to r12. What must NOT change is the
        # element count and every bearing/bottom elevation -- the support
        # chain and the interface to the machine stay exactly where they were.
        a = by12.get((eq, eq + "_SUPPORT_FRAME"), [])
        b = by13.get((eq, eq + "_SUPPORT_FRAME"), [])
        if len(a) != len(b):
            fails.append(f"{eq} SUPPORT_FRAME element count changed "
                         f"({len(a)} -> {len(b)})")
        else:
            for x, y in zip(a, b):
                gx, gy = aabb(x), aabb(y)
                if not gx or not gy:
                    continue
                if abs(gx[4] - gy[4]) > 0.01 or abs(gx[5] - gy[5]) > 0.01:
                    fails.append(f"{eq} SUPPORT_FRAME elevation changed")
                    break

    n12 = [l for l in l12 if l.strip().upper().startswith(("NEW NOZZLE", "CATR"))]
    n13 = [l for l in l13 if l.strip().upper().startswith(("NEW NOZZLE", "CATR"))]
    if n12 != n13:
        fails.append("NOZZLE / CATR changed")

    print("r13 verification")
    print(f"  pumps                       : {len(equis)}")
    print(f"  fastener solids checked     : {st['fasteners']}")
    print(f"  BOLT/STRUCTURE COLLISIONS   : {st['collisions']}")
    print(f"  flat casing-foot interfaces : {st['flat_interfaces']}")
    print(f"  casing foot ribs            : {st['ribs']}")
    print(f"  support chains              : {st['chain']}")
    print(f"  locked blocks identical     : {st['locked_ok']}")
    print()
    if fails:
        uniq = list(dict.fromkeys(fails))
        print(f"FAIL ({len(fails)} findings, {len(uniq)} distinct)")
        for f in uniq[:30]:
            print("   -", f)
        if len(uniq) > 30:
            print(f"   ... and {len(uniq)-30} more")
        return 1
    print("ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
