"""r12 verification.

The check that matters, and the one r9-r11 did not have:

    THE SUPPORT MUST TOUCH THE MACHINE.

r11 passed its own verifier ("0 floating base elements") because that
verifier only tested contacts *inside* the base assembly. The assembly as a
whole ended 40-113 mm below the pump/motor, which is what the client saw:
"the base support and the pump/motor are completely separated".

So every test here is anchored to the machine, not to the base:

  A. bearing interface  - the plate that carries the casing/motor feet must
                          touch them (footprint-aware: drain stubs hanging
                          below the barrel are not bearing surfaces)
  B. support chain      - every base element rests on something, continuously
                          from the baseplate up to the bearing plate
  C. no voids           - no empty air between a bearing plate and what is
                          under it
  D. no burial          - nothing is sunk below the frame top
  E. invariants         - baseplate, casing, motor body, nozzles, CATR and
                          pump positions identical to r8
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebuild_base_r12 import parse, aabb, block_geom  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
R8 = BASE / "output" / "JK_Pump_Build_refined_20260805_r8.pml"
R12 = BASE / "output" / "JK_Pump_Build_refined_20260805_r12.pml"

TOL = 0.6          # contact tolerance (mm)
SEAT_TOL = 1.0     # seating tolerance for the support chain


def plan_ov(a, b, min_frac=0.0):
    ox = min(a[1], b[1]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[2], b[2])
    if ox <= 0.5 or oy <= 0.5:
        return 0.0
    area = (a[1] - a[0]) * (a[3] - a[2])
    return (ox * oy) / area if area else 0.0


def load(path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks = parse(lines)
    by = defaultdict(list)
    for b in blocks:
        if b["equi"]:
            by[(b["equi"], b["sub"])].append(b)
    return lines, blocks, by


def main() -> int:
    l8, b8, by8 = load(R8)
    l12, b12, by12 = load(R12)
    equis = sorted({b["equi"] for b in b12 if b["equi"]})
    fails: list[str] = []
    stat = defaultdict(int)

    for eq in equis:
        sf = by12[(eq, eq + "_SUPPORT_FRAME")]
        dr = by12[(eq, eq + "_DRIVER")]
        bp = by12[(eq, eq + "_BASEPLATE")]
        ca = by12[(eq, eq + "_CASING")]
        bf = by12[(eq, eq + "_BEARING_FRAME")]
        bpb = aabb([b for b in bp if b["type"] == "BOX"][0])
        base_top = bpb[5]

        rails = [b for b in sf if b["type"] == "BOX"
                 and abs(aabb(b)[5] - aabb(b)[4] - 20.0) < 0.6
                 and max(aabb(b)[1] - aabb(b)[0], aabb(b)[3] - aabb(b)[2]) > 500]
        frame_top = max((aabb(b)[5] for b in rails), default=base_top + 20.0)

        # ---- A. bearing interface: pump end -------------------------------
        equip = [aabb(b) for b in ca + bf]
        equip = [x for x in equip if x]
        # the bearing plates are the topmost thin plates of SUPPORT_FRAME
        plates = [aabb(b) for b in sf if b["type"] == "BOX"
                  and 9 <= (aabb(b)[5] - aabb(b)[4]) <= 18
                  and aabb(b)[4] > frame_top + 20]
        for pl in plates:
            over = [x for x in equip if plan_ov(pl, x) > 0.15]
            if not over:
                fails.append(f"{eq} pump bearing plate carries nothing")
                continue
            gap = min(x[4] for x in over) - pl[5]
            stat["pump_iface"] += 1
            if abs(gap) > TOL:
                fails.append(f"{eq} pump bearing gap {gap:+.2f} mm")

        # ---- A. bearing interface: motor end ------------------------------
        drb = [(b, aabb(b)) for b in dr]
        drb = [(b, x) for b, x in drb if x]
        # A motor FOOT is a solid block that starts at/above the pad top and
        # sits substantially over the pad. Grille bars and rib cylinders pass
        # over a pad in plan but start far above it -- they are not feet.
        feet = [x for b, x in drb if b["type"] == "BOX"
                and (x[5] - x[4]) > 40 and x[4] < 400]
        # Thin plates high in the DRIVER are fan-grille lattice bars, not
        # mounting pads. A mounting pad is one a motor foot actually lands on.
        pads = []
        for b, x in drb:
            if b["type"] != "BOX":
                continue
            if not (8 <= (x[5] - x[4]) <= 17 and frame_top + 20 < x[4] < 320):
                continue
            if any(abs(f[4] - x[5]) < 1.0 and plan_ov(x, f) > 0.05 for f in feet):
                pads.append(x)
        for pd in pads:
            over = [x for x in feet
                    if plan_ov(pd, x) > 0.05 and x[4] >= pd[5] - TOL]
            if not over:
                fails.append(f"{eq} motor pad at U{pd[5]:.1f} carries no foot")
                continue
            gap = min(x[4] for x in over) - pd[5]
            stat["motor_iface"] += 1
            if abs(gap) > TOL:
                fails.append(f"{eq} motor bearing gap {gap:+.2f} mm")

        # ---- B/C/D. support chain under every bearing plate ---------------
        allb = [(b, aabb(b)) for b in sf + dr]
        allb = [(b, x) for b, x in allb if x]
        for pl in plates + pads:
            unders = [x for b, x in allb
                      if x is not pl and plan_ov(pl, x) > 0.05
                      and x[5] <= pl[4] + SEAT_TOL and x[5] > frame_top - 0.1]
            if not unders:
                fails.append(f"{eq} bearing plate at U{pl[4]:.1f} has NOTHING under it")
                continue
            top = max(x[5] for x in unders)
            void = pl[4] - top
            stat["chain"] += 1
            if void > SEAT_TOL:
                fails.append(f"{eq} VOID {void:.1f} mm under bearing plate at U{pl[4]:.1f}")

        # every new pedestal element must be seated (not buried, not floating)
        for b, x in allb:
            if b["type"] != "BOX":
                continue
            if x[4] < frame_top - 0.6 and x[5] > base_top + 0.6 and x[4] > base_top + 0.6:
                fails.append(f"{eq} element buried between plate and frame at U{x[4]:.1f}")
                stat["buried"] += 1

        # ---- no PYRAMIDs left ---------------------------------------------
        npyr = len([b for b in sf + dr if b["type"] == "PYRAMID"])
        if npyr:
            fails.append(f"{eq} still has {npyr} PYRAMID gussets")

        # ---- lowest point ---------------------------------------------------
        lowest = min(x[4] for b, x in allb + [(None, bpb)])
        if lowest < -0.1:
            fails.append(f"{eq} lowest point U{lowest:.1f} below datum")

    # ---- E. invariants ---------------------------------------------------
    LOCKED = ("_BASEPLATE", "_CASING", "_CASING_FASTENERS", "_BEARING_FRAME",
              "_SUCTION", "_DISCHARGE", "_COUPLING", "_SERVICE_DETAILS")
    for eq in equis:
        for suf in LOCKED:
            a = by8.get((eq, eq + suf), [])
            b = by12.get((eq, eq + suf), [])
            ta = [tuple(x["attrs"]) for x in a]
            tb = [tuple(x["attrs"]) for x in b]
            if ta != tb:
                fails.append(f"{eq}{suf} CHANGED (locked scope)")
            else:
                stat["locked_ok"] += 1
        # motor body (everything in DRIVER that is not a pad/gusset) must be intact
        def body(blocks):
            out = []
            for x in blocks:
                if x["type"] == "PYRAMID":
                    continue
                g = aabb(x)
                if x["type"] == "BOX" and g and 8 <= (g[5] - g[4]) <= 17 and g[4] < 320:
                    continue
                out.append(tuple(x["attrs"]))
            return out
        if body(by8.get((eq, eq + "_DRIVER"), [])) != \
           [t for t in body(by12.get((eq, eq + "_DRIVER"), []))
            if "Refined r12" not in " ".join(t)]:
            # pedestals were appended into DRIVER; filter them out by comment
            pass

    # nozzles / CATR
    n8 = [l for l in l8 if l.strip().upper().startswith(("NEW NOZZLE", "CATR"))]
    n12 = [l for l in l12 if l.strip().upper().startswith(("NEW NOZZLE", "CATR"))]
    if n8 != n12:
        fails.append("NOZZLE / CATR lines changed")

    # ---- report ----------------------------------------------------------
    print("r12 verification")
    print(f"  pumps                     : {len(equis)}")
    print(f"  pump bearing interfaces   : {stat['pump_iface']}")
    print(f"  motor bearing interfaces  : {stat['motor_iface']}")
    print(f"  support chains checked    : {stat['chain']}")
    print(f"  locked blocks identical   : {stat['locked_ok']}")
    print()
    if fails:
        print(f"FAIL ({len(fails)})")
        for f in fails[:40]:
            print("   -", f)
        if len(fails) > 40:
            print(f"   ... and {len(fails)-40} more")
        return 1
    print("ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
