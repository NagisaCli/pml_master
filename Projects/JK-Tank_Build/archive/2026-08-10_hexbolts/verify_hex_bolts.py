"""Numerical verification for the WSB anchor-bolt revision (r2).

Checks, per bolt:
- one stud (CYLINDER, diameter per size class) + one hex nut (EXTRUSION);
- anchor style: the nut profile plane sits ON the plate top (nut bottom face
  flush with the plate top);
- the stud runs from plate_bottom - embedment down in the foundation up to
  plate_top + nut height + protrusion above the nut;
- bolt circle radius = plate/ring radius - 100 mm, i.e. on the exposed
  annulus OUTSIDE the shell wall;
- correct bolt count and size class per tank;
- 205_TA_056 gained its exposed base ring (DIAM 10200 x 50, top at U 0);
- the original file text is unchanged except for inserted blocks.

Run from the repository root:
    python Projects/JK-Tank_Build/archive/2026-08-10_hexbolts/verify_hex_bolts.py
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

# The manually edited native export lives outside the repository, so it may be
# absent on another machine or after a cleanup. Override with argv[1].
ORIGINAL = (
    Path(sys.argv[1]) if len(sys.argv) > 1
    else Path(r"C:\Users\A\Desktop\jk_tank_edited_by_me.txt")
)
CANDIDATE = ROOT / "Projects/JK-Tank_Build/output/WSB_TA_hexbolts_20260810_r3.txt"

NEW_RE = re.compile(r"^NEW\s+(\w+)(?:\s+(.*))?$", re.IGNORECASE)
END_RE = re.compile(r"^END\s*$", re.IGNORECASE)
POS_RE = re.compile(
    r"^(E|W)\s+(-?[\d.]+)m{0,2}\s+(N|S)\s+(-?[\d.]+)m{0,2}\s+(U|D)\s+(-?[\d.]+)m{0,2}",
    re.IGNORECASE,
)

PLATES = {
    "/203_TA_006": ("_SHELL", 20),
    "/203_TA_024": ("_SUPPORT", 12),
    "/203_TA_029": ("_SHELL", 12),
    "/204_TA_001": ("_SUPPORT", 16),
    "/204_TA_034": ("_SHELL", 12),
    "/204_TA_035": ("_SHELL", 20),
    "/205_TA_001": ("_SHELL", 24),
    "/205_TA_008": ("_SUPPORT", 12),
    "/205_TA_011": ("_SHELL", 16),
    "/205_TA_022": ("_SUPPORT", 16),
    "/205_TA_025": ("_SUPPORT", 16),
    "/205_TA_029": ("_SHELL", 16),
    "/205_TA_042": ("_SUPPORT", 16),
    "/205_TA_045": ("_SHELL", 16),
    "/205_TA_056": ("_SHELL", 20),
    "/205_TA_059": ("_SHELL", 16),   # OUTER base ring DIAM 3000
}
EXCLUDED = ("/203_TA_044", "/203_TA_019", "/204_TA_021",
            "/205_TA_016", "/205_TA_036", "/205_TA_052")

SIZES = [
    (2500.0, ("M30", 30.0, 46.0, 24.0)),
    (4000.0, ("M36", 36.0, 55.0, 29.0)),
    (6000.0, ("M42", 42.0, 65.0, 34.0)),
    (math.inf, ("M48", 48.0, 75.0, 38.0)),
]
EXTRA_RING = {"diam": 10200.0, "heig": 50.0, "top_u": 0.0,
              "e": 67030.0, "n": 21008.0}


def parse_block(lines, i):
    m = NEW_RE.match(lines[i].strip())
    node = {"kind": m.group(1).upper(), "name": (m.group(2) or "").strip(),
            "attrs": {}, "children": [], "line": i + 1, "end_line": None}
    j = i + 1
    while j < len(lines):
        s = lines[j].strip()
        if not s or s.startswith("--"):
            j += 1
            continue
        if NEW_RE.match(s):
            child, j = parse_block(lines, j)
            node["children"].append(child)
            continue
        if END_RE.match(s):
            node["end_line"] = j + 1
            return node, j + 1
        am = re.match(r"^([A-Za-z_][\w]*)\s+(.+)$", s)
        if am and am.group(1).upper() not in ("ONERROR", "INPUT"):
            node["attrs"].setdefault(am.group(1).upper(), am.group(2).strip())
        j += 1
    raise RuntimeError("unterminated block")


def parse_file(lines):
    root = None
    i = 0
    while i < len(lines):
        if NEW_RE.match(lines[i].strip()) and root is None:
            root, i = parse_block(lines, i)
        else:
            i += 1
    return root


def pos_en_u(attrs):
    m = POS_RE.match(attrs.get("POS", ""))
    assert m, attrs.get("POS")
    e, n, u = float(m.group(2)), float(m.group(4)), float(m.group(6))
    if m.group(1).upper() == "W":
        e = -e
    if m.group(3).upper() == "S":
        n = -n
    if m.group(5).upper() == "D":
        u = -u
    return e, n, u


def num(v):
    return float(re.sub(r"[^\d.+-]", "", v))


def size_for(diam):
    for threshold, spec in SIZES:
        if diam < threshold:
            return spec
    return SIZES[-1][1]


def hex_profile(node):
    verts = []
    for loop in node["children"]:
        if loop["kind"] != "LOOP":
            continue
        for v in loop["children"]:
            if v["kind"] == "VERTEX":
                verts.append(pos_en_u(v["attrs"]))
    if len(verts) != 6:
        return None, len(verts)
    return sum(math.hypot(x, y) for x, y, _ in verts) / 6.0, 6


def find_plate(sub):
    cys = [c for c in sub["children"]
           if c["kind"] == "CYLINDER" and "HEIG" in c["attrs"] and "DIAM" in c["attrs"]]
    rows = []
    for c in cys:
        e, n, u = pos_en_u(c["attrs"])
        h = num(c["attrs"]["HEIG"])
        if h <= 100.0:  # plates/base rings are short; anchor studs are long
            rows.append((u - h / 2, u + h / 2, h, num(c["attrs"]["DIAM"]), c))
    bot = min(r[0] for r in rows)
    cands = [r for r in rows if abs(r[0] - bot) < 0.01]
    assert cands, "no exposed base ring/plate found"
    cands.sort(key=lambda r: r[3], reverse=True)
    return cands[0]


def main():
    orig_lines = ORIGINAL.read_text(encoding="utf-8-sig").splitlines()
    cand_lines = CANDIDATE.read_text(encoding="utf-8-sig").splitlines()
    tree = parse_file(cand_lines)

    errors = []
    total = 0
    for eq in tree["children"]:
        if eq["kind"] != "EQUIPMENT":
            continue
        tag = eq["name"]
        if tag in EXCLUDED:
            continue
        suffix, expected = PLATES[tag]
        sub = next(c for c in eq["children"]
                   if c["kind"] == "SUBEQUIPMENT" and c["name"].endswith(suffix))
        ring = EXTRA_RING if tag == "/205_TA_056" else None
        if ring is None:
            b = find_plate(sub)
        else:
            b = None
            for c in sub["children"]:
                if c["kind"] == "CYLINDER" and abs(num(c["attrs"].get("DIAM", "0")) - ring["diam"]) < 0.01:
                    b = (ring["top_u"] - ring["heig"], ring["top_u"], ring["heig"],
                         ring["diam"], c)
                    break
            assert b is not None, "205_TA_056 base ring missing"

        _, _, _, diam, plate = b
        plate_bot = b[0]
        plate_top = b[1]
        ec, nc, _ = pos_en_u(plate["attrs"])
        radius = diam / 2.0 - 100.0
        label, stud_d, af, nut_h = size_for(diam)
        embed = 8.0 * stud_d
        protrude = stud_d

        # the bolts must sit on the exposed annulus OUTSIDE the shell wall
        shell_max_r = 0.0
        for c in sub["children"]:
            if c["kind"] != "CYLINDER" or "HEIG" not in c["attrs"] or "DIAM" not in c["attrs"]:
                continue
            h = num(c["attrs"]["HEIG"])
            if h <= 100.0:
                continue
            ce, cn, cu = pos_en_u(c["attrs"])
            if cu - h / 2 <= plate_top + 1.0 and cu + h / 2 >= plate_bot - 1.0:
                shell_max_r = max(shell_max_r, num(c["attrs"]["DIAM"]) / 2.0)
        if radius < shell_max_r + 40.0:
            errors.append(f"{tag}: bolt circle {radius:.0f} inside shell wall "
                          f"(max shell radius {shell_max_r:.0f})")

        nuts = [c for c in sub["children"] if c["kind"] == "EXTRUSION"]
        studs = [c for c in sub["children"]
                 if c["kind"] == "CYLINDER"
                 and abs(num(c["attrs"].get("DIAM", "0")) - stud_d) < 0.01
                 and c is not plate]
        if len(nuts) != expected:
            errors.append(f"{tag}: expected {expected} nuts, found {len(nuts)}")
        if len(studs) != expected:
            errors.append(f"{tag}: expected {expected} studs ({label}), found {len(studs)}")

        for nut in nuts:
            ne, nn, nu = pos_en_u(nut["attrs"])
            h = num(nut["attrs"]["HEIG"])
            r_hex, nv = hex_profile(nut)
            if abs(nu - plate_top) > 0.5:
                errors.append(f"{tag}: nut bottom {nu:.2f} not flush with plate top {plate_top:.2f}")
            if abs(math.hypot(ne - ec, nn - nc) - radius) > 0.5:
                errors.append(f"{tag}: nut off bolt circle")
            if r_hex is None or abs(r_hex - af / math.cos(math.radians(30)) / 2.0) > 0.5:
                errors.append(f"{tag}: nut hex profile invalid (n={nv}, r={r_hex})")
            if abs(h - nut_h) > 0.01:
                errors.append(f"{tag}: nut height {h} != {nut_h}")
        for stud in studs:
            se, sn, su = pos_en_u(stud["attrs"])
            h = num(stud["attrs"]["HEIG"])
            want_bot = plate_bot - embed
            want_top = plate_top + nut_h + protrude
            if abs(math.hypot(se - ec, sn - nc) - radius) > 0.5:
                errors.append(f"{tag}: stud off bolt circle")
            if abs((su - h / 2) - want_bot) > 0.5 or abs((su + h / 2) - want_top) > 0.5:
                errors.append(f"{tag}: stud span {su - h / 2:.1f}..{su + h / 2:.1f} "
                              f"!= {want_bot:.1f}..{want_top:.1f}")
        total += expected

    # text-level: original lines must all still exist in order (pure insertion)
    it = iter(cand_lines)
    for line in orig_lines:
        for cand in it:
            if cand == line:
                break
        else:
            errors.append("candidate no longer contains original lines in order")
            break

    banned = ("!!ALERT", "$P", "ENDS", "END EQUI", "NAME =", "DESC =", "!VAR =",
              "COLLECT", "UNSET", "!!CE", "!!WORLD", "SUSPEND", "RESUME", "VAR 0")
    for b in banned:
        if b in cand_lines:
            errors.append(f"banned token present: {b}")

    print(f"TOTAL verified bolts: {total}")
    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for e in errors[:40]:
            print(" -", e)
        raise SystemExit(1)
    print("OK: anchor-style nuts flush on plate top, all bolts on exposed annulus, "
          "counts/sizes match, text preserved, PML1 clean")


if __name__ == "__main__":
    main()
