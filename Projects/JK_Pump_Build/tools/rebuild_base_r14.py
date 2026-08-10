"""r14 -- frame cross-beams trimmed to the rail datum.

Starting point: JK_Pump_Build_refined_20260805_r13.pml
Output:         JK_Pump_Build_refined_20260805_r14.pml

Client bug from the r13 E3D reload: the base reads as a jumble of overlapping
blocks at inconsistent levels, and the support still does not look like it
meets the machine cleanly.

Measured cause -- ONE defect, present since r8 and never touched by any of the
support revisions (r9-r13 all rebuilt the pedestals and left the frame alone):

  The rails are a clean datum: every rail is U 50.0 .. 70.0, and the pedestal
  bottom flanges start at exactly U 70.0. Correct.

  The cross-beams are not. They all start at U 50 but their tops run to
  U 82.6 .. 111.2 -- 13 distinct top elevations, 12 to 41 mm ABOVE the rail
  top they should be flush with. Fleet-wide that produces 412 interpenetrating
  member pairs:

      rail   x xbeam : 202   beams sunk 20 mm into the rails
      web    x xbeam : 134   beams punching up into the pedestal webs
      flange x xbeam :  60   beams punching through the pedestal flange
      plate  x xbeam :  10   beams reaching the bearing plate
      xbeam  x xbeam :   6   beams crossing each other

  194 of those are cross-beams driven 6.8-12 mm INTO the pedestals that carry
  the pump. That is not a cosmetic overlap: the beam occupies the same space
  as the support, which is exactly the "not an effective support" reading.

r14 sets every cross-beam top to the rail datum (U 70.0), so the beams frame
between the rails instead of through them, and the pedestals sit on a flat
continuous frame top. Beam plan position, thickness and length are unchanged;
only ZLEN/HEIG and the vertical centre move.

Nothing else is touched. Pedestals, casing feet, bearing plates, bolts,
DRIVER (including the motor cooling fins), nozzles, baseplates and every
locked block stay byte-identical to r13.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebuild_base_r12 import parse, aabb  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "output" / "JK_Pump_Build_refined_20260805_r13.pml"
OUT = BASE / "output" / "JK_Pump_Build_refined_20260805_r14.pml"

RAIL_MIN_LEN = 1000.0   # plan length above which a member is a rail
XBEAM_MIN_LEN = 400.0   # plan length above which a non-rail member is a beam


def role(bb):
    """Classify a SUPPORT_FRAME member from its world AABB."""
    dx, dy, dz = bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4]
    plan = max(dx, dy)
    if plan > RAIL_MIN_LEN:
        return "rail"
    if plan > XBEAM_MIN_LEN:
        return "xbeam"
    if dz <= 12.5 and plan > 120:
        return "flange"
    if dz <= 16.5:
        return "plate"
    return "web"


def rail_datum(members):
    """Top of the rails for one pump -- the elevation beams must not exceed.

    Normally the rails are the >1 m members. On a short skid (203-PU-020, whose
    longest member is 759 mm) nothing clears that bar, so fall back to the
    longest members present: whatever spans the skid IS the rail, and its top
    is the frame datum the pedestals are already seated on.
    """
    tops = [bb[5] for bb in members if role(bb) == "rail"]
    if tops:
        return max(tops)
    spans = [bb for bb in members if role(bb) == "xbeam"]
    if not spans:
        return None
    longest = max(max(bb[1] - bb[0], bb[3] - bb[2]) for bb in spans)
    return max(bb[5] for bb in spans
               if max(bb[1] - bb[0], bb[3] - bb[2]) >= longest - 1.0)


def main() -> int:
    lines = SRC.read_text(encoding="utf-8-sig").splitlines()
    blocks = parse(lines)

    by_eq = defaultdict(list)
    for b in blocks:
        bb = aabb(b)
        if bb and (b["sub"] or "").endswith("SUPPORT_FRAME"):
            by_eq[b["equi"]].append((b, bb))

    st = defaultdict(int)
    edits: dict[int, tuple[float, float]] = {}   # line index -> (new_zlen, new_u)

    for eq, members in by_eq.items():
        datum = rail_datum([bb for _, bb in members])
        if datum is None:
            st["pumps_without_rail"] += 1
            continue
        st["pumps"] += 1
        for b, bb in members:
            if role(bb) != "xbeam":
                continue
            top, bot = bb[5], bb[4]
            if top <= datum + 0.05:
                st["beams_already_ok"] += 1
                continue
            new_h = datum - bot
            if new_h <= 0:
                # A beam entirely above the rail top would be something other
                # than a frame beam; leave it and report rather than invert it.
                st["beams_skipped_degenerate"] += 1
                continue
            edits[(b["start"], b["end"])] = (new_h, bot + new_h / 2.0)
            st["beams_trimmed"] += 1
            st["mm_removed"] += round(top - datum, 1)

    if not edits:
        print("nothing to trim")
        return 1

    # Rewrite ZLEN/HEIG and the U component of POS for each trimmed beam.
    out = list(lines)
    for (start, end), (new_h, new_u) in edits.items():
        # Only the block's own attribute lines; nested LOOP/VERTEX bodies of a
        # cross-beam are not touched (frame beams are plain BOXes anyway).
        for i in range(start + 1, end):
            s = out[i].strip()
            up = s.upper()
            if up.startswith(("ZLEN", "HEIG")):
                out[i] = f"{s.split()[0]} {new_h:.6g}mm"
            elif up.startswith("POS "):
                out[i] = _repos_u(s, new_u)

    OUT.write_text("\n".join(out) + "\n", encoding="utf-8-sig")
    print(f"Wrote {OUT}")
    print(f"  lines {len(lines)} -> {len(out)}")
    for k in sorted(st):
        print(f"  {k}: {st[k]}")
    return 0


def _repos_u(s: str, new_u: float) -> str:
    """Replace the U/D component of a POS line, preserving E/N wording."""
    toks = s.split()
    for j, t in enumerate(toks):
        if t.upper() in ("U", "D") and j + 1 < len(toks):
            word = "U" if new_u >= 0 else "D"
            toks[j] = word
            toks[j + 1] = f"{abs(new_u):.6g}mm"
            return " ".join(toks)
    return s


if __name__ == "__main__":
    raise SystemExit(main())
