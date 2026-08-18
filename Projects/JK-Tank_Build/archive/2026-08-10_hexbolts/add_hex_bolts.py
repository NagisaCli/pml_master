"""Add anchor-style bottom hex bolts to the WSB tank native export (r2).

User corrections (2026-08-10, after r1 review):
1. The bottom-plate boundary must be the WIDEST bottom ring/plate that
   extends outside the shell wall; bolts sit on its exposed annulus, never
   inside the shell footprint.
2. Anchor-bolt style: the hex nut sits on the plate TOP (flush against the
   plate), and the stud extends DOWN below the plate into the foundation.
3. Nut size scales with tank size (M30-M48) so the fastener reads as
   physically plausible.

Scope:
- Every tank EXCEPT 203_TA_044, 203_TA_019, 204_TA_021, 205_TA_016,
  205_TA_036 and 205_TA_052 receives anchor bolts.
- 205_TA_056 has no exposed base ring under its 9900 mm outer shell, so one
  base ring (DIAM 10200, HEIG 50, top flush with the shell bottom) is added
  inside its SHELL subequipment before the bolts.  Everything else is
  insertion-only.

Run from the repository root:
    python Projects/JK-Tank_Build/archive/2026-08-10_hexbolts/add_hex_bolts.py
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

# The manually edited native export lives outside the repository, so it may be
# absent on another machine or after a cleanup. Override with argv[1].
SOURCE = (
    Path(sys.argv[1]) if len(sys.argv) > 1
    else Path(r"C:\Users\A\Desktop\jk_tank_edited_by_me.txt")
)
IMPORT = ROOT / "Projects/JK-Tank_Build/imports/2026-08-10_jk_tank_edited_by_me.txt"
OUTPUT = ROOT / "Projects/JK-Tank_Build/output/WSB_TA_hexbolts_20260810_r3.txt"
DESKTOP_OUTPUT = Path(r"C:\Users\A\Desktop\jk_tank_edited_by_me_hexbolts.txt")

# tag -> (sube suffix, bolt count)
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
    "/205_TA_059": ("_SHELL", 16),   # OUTER base ring DIAM 3000, not the
                                     # 1800 ring under the inner skirt
}

EXCLUDED = ("/203_TA_044", "/203_TA_019", "/204_TA_021",
            "/205_TA_016", "/205_TA_036", "/205_TA_052")

# 205_TA_056: no exposed base ring exists; add one under the 9900 outer shell.
EXTRA_RING = {
    "/205_TA_056": {"diam": 10200.0, "heig": 50.0, "top_u": 0.0,
                    "e": 67030.0, "n": 21008.0},
}

# size class thresholds on plate/ring diameter -> (label, stud d, nut AF, nut h)
SIZES = [
    (2500.0, ("M30", 30.0, 46.0, 24.0)),
    (4000.0, ("M36", 36.0, 55.0, 29.0)),
    (6000.0, ("M42", 42.0, 65.0, 34.0)),
    (math.inf, ("M48", 48.0, 75.0, 38.0)),
]

RIM = 100.0          # bolt circle inset from the plate/ring outer edge
NEW_RE = re.compile(r"^NEW\s+(\w+)(?:\s+(.*))?$", re.IGNORECASE)
END_RE = re.compile(r"^END\s*$", re.IGNORECASE)
POS_RE = re.compile(
    r"^(E|W)\s+(-?[\d.]+)m{0,2}\s+(N|S)\s+(-?[\d.]+)m{0,2}\s+(U|D)\s+(-?[\d.]+)m{0,2}",
    re.IGNORECASE,
)


def parse_block(lines: list[str], i: int):
    m = NEW_RE.match(lines[i].strip())
    node = {"kind": m.group(1).upper(), "name": (m.group(2) or "").strip(),
            "line": i + 1, "attrs": {}, "children": [], "end_line": None}
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
    raise RuntimeError(f"unterminated block at line {i + 1}")


def parse_file(lines: list[str]):
    root = None
    i = 0
    while i < len(lines):
        if NEW_RE.match(lines[i].strip()) and root is None:
            root, i = parse_block(lines, i)
        else:
            i += 1
    return root


def pos_en_u(attrs: dict[str, str]):
    m = POS_RE.match(attrs.get("POS", ""))
    if not m:
        raise ValueError(f"unparsable POS: {attrs.get('POS')!r}")
    e, n, u = float(m.group(2)), float(m.group(4)), float(m.group(6))
    if m.group(1).upper() == "W":
        e = -e
    if m.group(3).upper() == "S":
        n = -n
    if m.group(5).upper() == "D":
        u = -u
    return e, n, u


def num(v: str) -> float:
    return float(re.sub(r"[^\d.+-]", "", v))


def find_plate(eq: dict, suffix: str):
    """Return (sube, plate_node, bottom_u, top_u) using the WIDEST short
    cylinder at the sube's lowest elevation (the exposed base ring/plate)."""
    for sub in eq["children"]:
        if sub["kind"] != "SUBEQUIPMENT" or not sub["name"].endswith(suffix):
            continue
        cys = []
        for c in sub["children"]:
            if c["kind"] != "CYLINDER" or "HEIG" not in c["attrs"] or "DIAM" not in c["attrs"]:
                continue
            e, n, u = pos_en_u(c["attrs"])
            h = num(c["attrs"]["HEIG"])
            cys.append((u - h / 2, u + h / 2, h, num(c["attrs"]["DIAM"]), c))
        if not cys:
            continue
        bot = min(b[0] for b in cys)
        candidates = [b for b in cys if abs(b[0] - bot) < 0.01 and b[2] <= 100.0]
        if not candidates:
            continue
        candidates.sort(key=lambda b: b[3], reverse=True)  # widest first
        b = candidates[0]
        return sub, b[4], b[0], b[1]
    raise ValueError(f"no exposed base ring/plate found for {eq['name']} suffix {suffix}")


def size_for(diam: float):
    for threshold, spec in SIZES:
        if diam < threshold:
            return spec
    return SIZES[-1][1]


def fmt_pos(e: float, n: float, u: float) -> str:
    ne, nn, nu = round(e, 1), round(n, 1), round(u, 1)
    e_txt = f"E {ne:.1f}mm"
    n_txt = f"S {-nn:.1f}mm" if nn < 0 else f"N {nn:.1f}mm"
    u_txt = f"D {-nu:.1f}mm" if nu < 0 else f"U {nu:.1f}mm"
    return f"POS {e_txt} {n_txt} {u_txt}"


def nut_vertices(af: float) -> list[str]:
    r = af / math.cos(math.radians(30)) / 2.0
    half_flat = af / 2.0
    pts = [(r, 0.0), (r / 2.0, half_flat), (-r / 2.0, half_flat),
           (-r, 0.0), (-r / 2.0, -half_flat), (r / 2.0, -half_flat)]
    lines = []
    for x, y in pts:
        x_txt = f"E {x:.2f}mm" if x >= 0 else f"W {-x:.2f}mm"
        y_txt = f"N {y:.2f}mm" if y >= 0 else f"S {-y:.2f}mm"
        lines.extend(("NEW VERTEX", f"POS {x_txt} {y_txt} U 0mm", "END"))
    return lines


def bolt_block(e: float, n: float, plate_bottom: float, plate_top: float,
               spec) -> list[str]:
    label, stud_d, af, nut_h = spec
    embed = 8.0 * stud_d
    protrude = stud_d
    stud_bottom = plate_bottom - embed
    stud_top = plate_top + nut_h + protrude
    stud_heig = stud_top - stud_bottom
    stud_u = (stud_bottom + stud_top) / 2.0
    lines = [
        "NEW CYLINDER",
        fmt_pos(e, n, stud_u),
        f"DIAM {stud_d:.0f}mm",
        f"HEIG {stud_heig:.1f}mm",
        "",
        "END",
        "NEW EXTRUSION",
        fmt_pos(e, n, plate_top),
        "ORI Y is N and Z is U",
        f"HEIG {nut_h:.0f}mm",
        "",
        "NEW LOOP",
    ]
    lines.extend(nut_vertices(af))
    lines.extend(("END", "END"))
    return lines


def ring_block(spec: dict) -> list[str]:
    top = spec["top_u"]
    return [
        "NEW CYLINDER",
        fmt_pos(spec["e"], spec["n"], top - spec["heig"] / 2.0),
        f"DIAM {spec['diam']:.0f}mm",
        f"HEIG {spec['heig']:.0f}mm",
        "",
        "END",
    ]


def build_insert(eq: dict, suffix: str, count: int, ring_spec: dict | None) -> list[str]:
    sub, plate, plate_bottom, plate_top = find_plate(eq, suffix)
    ec, nc, _ = pos_en_u(plate["attrs"])
    diam = num(plate["attrs"]["DIAM"])
    if ring_spec is not None:
        # 205_TA_056: anchor on the added base ring, not the inner plate.
        ec, nc = ring_spec["e"], ring_spec["n"]
        diam = ring_spec["diam"]
        plate_bottom = ring_spec["top_u"] - ring_spec["heig"]
        plate_top = ring_spec["top_u"]
    radius = diam / 2.0 - RIM
    spec = size_for(diam)
    lines = []
    if ring_spec is not None:
        lines.extend(ring_block(ring_spec))
        lines.append("")
    for i in range(count):
        ang = 2.0 * math.pi * i / count
        e = ec + radius * math.cos(ang)
        n = nc + radius * math.sin(ang)
        lines.extend(bolt_block(e, n, plate_bottom, plate_top, spec))
        if i != count - 1:
            lines.append("")
    return sub, lines


def main() -> None:
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    tree = parse_file(lines)
    if tree is None or tree["kind"] != "ZONE":
        raise RuntimeError("expected a ZONE root")

    inserts: dict[int, list[str]] = {}
    summary = []
    for eq in tree["children"]:
        if eq["kind"] != "EQUIPMENT":
            continue
        if eq["name"] in EXCLUDED:
            summary.append((eq["name"], 0, "-", "-"))
            continue
        suffix, count = PLATES[eq["name"]]
        ring_spec = EXTRA_RING.get(eq["name"])
        sub, block = build_insert(eq, suffix, count, ring_spec)
        inserts.setdefault(sub["end_line"], []).extend(block)
        diam = (ring_spec["diam"] if ring_spec
                else num(find_plate(eq, suffix)[1]["attrs"]["DIAM"]))
        spec = size_for(diam)
        summary.append((eq["name"], count, sub["name"], spec[0]))

    out_lines = list(lines)
    for end_line in sorted(inserts, reverse=True):
        block = inserts[end_line]
        out_lines[end_line - 1:end_line - 1] = [""] + block

    out_text = "\r\n".join(out_lines) + "\r\n"
    out_bytes = b"\xef\xbb\xbf" + out_text.encode("utf-8")
    IMPORT.parent.mkdir(parents=True, exist_ok=True)
    IMPORT.write_bytes(raw)
    for path in (OUTPUT, DESKTOP_OUTPUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(out_bytes)

    for tag, count, sube, label in summary:
        print(f"{tag:14s} {count:3d} x {label:4s} -> {sube}")
    total = sum(c for _, c, _, _ in summary)
    print(f"TOTAL bolts: {total}")
    print(f"Wrote {len(out_lines)} lines ({len(out_lines) - len(lines)} added):")
    print(f"  {OUTPUT}")
    print(f"  {DESKTOP_OUTPUT}")


if __name__ == "__main__":
    main()
