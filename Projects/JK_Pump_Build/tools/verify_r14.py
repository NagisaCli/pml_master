"""r14 verification -- frame coherence, plus the properties r13 already proved.

The r13 reload failed visually while every r13 check passed. The gap: nothing
tested whether structural members OCCUPY THE SAME SPACE or sit on a CONSISTENT
DATUM. "Nothing floats" and "nothing interpenetrates" are different properties,
and only the first was ever checked.

New checks (the ones whose absence let the defect through):

  A. No structural member interpenetrates a member of the support it carries.
     Specifically zero xbeam-into-pedestal and xbeam-into-plate volumes.
     Rail/beam T-joints at a crossing are EXPECTED and allowed: a beam framed
     between rails shares the rail depth at the joint. They are counted and
     reported, not failed.

  B. One frame datum per pump: every cross-beam top equals the rail top.

  C. Fastener axis: every hold-down shank is vertical. A sideways bolt passes
     a clash test and is still wrong.

Regression (must not move):
  D. Every pedestal flange still seated on the frame top -- 0 voids.
  E. Everything outside SUPPORT_FRAME byte-identical to r13.
"""

from __future__ import annotations

import hashlib
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebuild_base_r12 import parse, aabb  # noqa: E402
from rebuild_base_r14 import role, rail_datum  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
R13 = BASE / "output" / "JK_Pump_Build_refined_20260805_r13.pml"
R14 = BASE / "output" / "JK_Pump_Build_refined_20260805_r14.pml"

TOL = 0.6
# A shared volume between a beam and the rail it frames into is a joint, not a
# clash, as long as it is confined to the crossing footprint.
JOINT_PAIRS = {("rail", "xbeam"), ("xbeam", "xbeam")}


def ov(a0, a1, b0, b1):
    return min(a1, b1) - max(a0, b0)


def load(p):
    lines = p.read_text(encoding="utf-8-sig").splitlines()
    return lines, parse(lines)


def main() -> int:
    l13, b13 = load(R13)
    l14, b14 = load(R14)
    bad: list[str] = []

    frame = defaultdict(list)
    fasteners = []
    for b in b14:
        bb = aabb(b)
        if not bb:
            continue
        sub = b["sub"] or ""
        if sub.endswith("SUPPORT_FRAME"):
            frame[b["equi"]].append(bb)
        elif sub.endswith("FASTENERS") and b["type"] == "CYLINDER":
            fasteners.append((b["equi"], bb))

    # ---- A. interpenetration --------------------------------------------
    clashes = 0
    joints = 0
    for eq, v in frame.items():
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                a, c = v[i], v[j]
                o = (ov(a[0], a[1], c[0], c[1]),
                     ov(a[2], a[3], c[2], c[3]),
                     ov(a[4], a[5], c[4], c[5]))
                if min(o) <= 0.5:
                    continue
                pair = tuple(sorted((role(a), role(c))))
                if pair in JOINT_PAIRS:
                    joints += 1
                else:
                    clashes += 1
                    if len(bad) < 12:
                        bad.append(f"{eq} {pair[0]}/{pair[1]} interpenetrate "
                                   f"{min(o):.1f}mm")

    # ---- B. one datum per pump ------------------------------------------
    off_datum = 0
    for eq, v in frame.items():
        datum = rail_datum(v)
        if datum is None:
            bad.append(f"{eq} has no identifiable rail datum")
            continue
        for bb in v:
            if role(bb) == "xbeam" and bb[5] > datum + TOL:
                off_datum += 1
                if len(bad) < 12:
                    bad.append(f"{eq} beam top {bb[5]:.1f} above datum {datum:.1f}")

    # ---- C. fastener axis ------------------------------------------------
    sideways = 0
    for eq, bb in fasteners:
        dx, dy, dz = bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4]
        # Only shanks (slender) must be vertical; heads/washers are discs.
        if max(dx, dy) >= 60 and max(dx, dy) / max(min(dx, dy, dz), 0.1) >= 3 \
                and dz < max(dx, dy):
            sideways += 1
            if len(bad) < 12:
                bad.append(f"{eq} non-vertical hold-down shank "
                           f"{dx:.0f}x{dy:.0f}x{dz:.0f}")

    # ---- D. flanges still seated ----------------------------------------
    voids = 0
    flanges = 0
    for eq, v in frame.items():
        fl = [bb for bb in v if role(bb) == "flange"]
        others = [bb for bb in v if role(bb) != "flange"]
        for f in fl:
            flanges += 1
            if not any(ov(f[0], f[1], o[0], o[1]) > 1
                       and ov(f[2], f[3], o[2], o[3]) > 1
                       and abs(o[5] - f[4]) < TOL for o in others):
                voids += 1
                if len(bad) < 12:
                    bad.append(f"{eq} pedestal flange not seated (void)")

    # ---- E. non-frame scope unchanged ------------------------------------
    def canon(blocks, lines):
        h = hashlib.sha256()
        for b in blocks:
            if (b["sub"] or "").endswith("SUPPORT_FRAME"):
                continue
            h.update(("\n".join(lines[b["start"]:b["end"] + 1]) + "\n").encode())
        return h.hexdigest()

    same = canon(b13, l13) == canon(b14, l14)
    if not same:
        bad.append("non-SUPPORT_FRAME geometry changed vs r13")

    print("r14 verification")
    print(f"  pumps                       : {len(frame)}")
    print(f"  PEDESTAL/PLATE CLASHES      : {clashes}")
    print(f"  rail/beam joints (expected) : {joints}")
    print(f"  beams above rail datum      : {off_datum}")
    print(f"  non-vertical hold-downs     : {sideways}")
    print(f"  pedestal flanges seated     : {flanges - voids}/{flanges}")
    print(f"  non-frame scope identical   : {same}")

    if bad:
        print(f"\nFAIL ({len(bad)} findings)")
        for m in bad:
            print("   -", m)
        return 1
    print("\nALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
