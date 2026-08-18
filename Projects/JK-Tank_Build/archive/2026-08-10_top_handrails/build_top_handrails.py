"""Build WSB tank-top handrails (native E3D structural syntax).

Reconciled continuation of:
  imports/2026-08-10_jk_tank_edited_by_me_hexbolts.txt

The user asked for a 1.1 m high circular handrail around the top platform of
two tanks. 205-TA-006 does not exist in this export; the only two 205-series
tanks whose roof is a frustum with a flat top platform are 205-TA-001
(DTOP 6000) and 205-TA-056 (DTOP 6500), so those are the modelled pair.

This script inserts ONE new STRUCTURE block (with one FRMWORK + one HANDRA per
tank) immediately before the first `OLD NOZZLE` binding pass, so every
pre-existing element is preserved byte-for-byte outside the insertion point.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IMPORT = ROOT / "imports" / "2026-08-10_jk_tank_edited_by_me_hexbolts.txt"
OUTPUT = ROOT / "output" / "WSB_TA_top_handrails_20260810_r2.txt"

RAIL_SPCOMPONENT = "/SLH/PIPE48.3x3.6"
RAIL_HEIGHTS_MM = (1100.0, 550.0)  # top / mid rail; user asked for 1.1 m
POST_SPACING_MM = 1000.0

# tag -> (centre E, centre N, platform U, platform radius)
TANKS = {
    "TA_001": (26863.0, -11601.0, 28200.0, 3000.0),
    "TA_056": (67030.0, 21008.0, 27700.0, 3250.0),
}


def circle_points(radius: float, start_x: float, start_y: float) -> dict[str, tuple[float, float]]:
    """Absolute circle points used to build a 4x90-degree closed RPATH."""
    pts = {}
    for deg in (0, 45, 90, 135, 180, 225, 270, 315, 360):
        rad = math.radians(deg)
        pts[deg] = (
            start_x + radius * math.cos(rad),
            start_y + radius * math.sin(rad),
        )
    return pts


def fmt_dir(value: float) -> str:
    """Format a signed delta as E/W + N/S native syntax."""
    if value >= 0:
        return f"E {value:.2f}mm"
    return f"W {-value:.2f}mm"


def fmt_ns(value: float) -> str:
    if value >= 0:
        return f"N {value:.2f}mm"
    return f"S {-value:.2f}mm"


def fmt_pos(e: float, n: float, u: float) -> str:
    return f"POS {fmt_dir(e)} {fmt_ns(n)} U {u:.2f}mm"


def build_rpath(radius: float, start_e: float, start_n: float) -> str:
    """Closed circular RPATH: 4 x 90-degree arcs, each via a CURTYP THRU point."""
    abs_pts = circle_points(radius, start_e, start_n)
    rel = {
        deg: (abs_pts[deg][0] - abs_pts[0][0], abs_pts[deg][1] - abs_pts[0][1])
        for deg in abs_pts
    }
    lines = [
        "NEW RPATH",
        "DRNS E",
        "DRNE E",
        "",
        "NEW POINTR",
        "END",
    ]
    for mid, end in ((45, 90), (135, 180), (225, 270), (315, 360)):
        lines.append(f"NEW CURVE\n{fmt_pos(*rel[mid], 0.0)}\nCURTYP THRU\nEND")
        lines.append(f"NEW POINTR\n{fmt_pos(*rel[end], 0.0)}\nEND")
    lines.append("END")
    return "\n".join(lines)


def build_handrail(tag: str, centre_e: float, centre_n: float, platform_u: float, radius: float) -> str:
    start_e = centre_e + radius  # path starts on the east point of the platform rim
    lines = [
        f"-- {tag}: circular handrail, R={radius:.0f} mm, platform U={platform_u:.0f} mm",
        f"NEW HANDRA /{tag}_TOP/HR_001",
        fmt_pos(start_e, centre_n, platform_u),
        f"RAILHE {RAIL_HEIGHTS_MM[0]:.0f}mm {RAIL_HEIGHTS_MM[1]:.0f}mm",
        f"POSTSP {POST_SPACING_MM:.0f}mm",
        "SHOWKP false",
        "FIRE 0",
        "BUIL false",
        "SHOP false",
        "",
        build_rpath(radius, start_e, centre_n),
        "",
        "NEW RAILSET",
        f"NEW RAIL\nFUNC 'HAND'\nSPRE SPCOMPONENT {RAIL_SPCOMPONENT}\nZOFF {RAIL_HEIGHTS_MM[0]:.0f}mm\nJUSL NA\nRADS true\nEND",
        f"NEW RAIL\nSPRE SPCOMPONENT {RAIL_SPCOMPONENT}\nZOFF {RAIL_HEIGHTS_MM[1]:.0f}mm\nJUSL NA\nRADS true\nEND",
        "END",
        "END",
    ]
    return "\n".join(lines)


def build_block() -> str:
    parts = [
        "NEW STRUCTURE /TA_TOP_HANDRAILS",
        "BUIL false",
        "PDNAME unset",
        "",
    ]
    for tag, (ce, cn, pu, r) in TANKS.items():
        parts += [
            f"NEW FRMWORK /{tag}_TOP",
            "BUIL false",
            "SHOP false",
            "GRADE 0",
            "FIRE 0",
            "PTSP unset",
            "INSC unset",
            "PDNAME unset",
            "",
            build_handrail(tag, ce, cn, pu, r),
            "",
            "END",
            "",
        ]
    parts.append("END")
    return "\n".join(parts)


def verify_block(block: str) -> None:
    """Numerical self-check of the generated circle geometry."""
    for tag, (ce, cn, pu, r) in TANKS.items():
        hand = block.split(f"NEW HANDRA /{tag}_TOP/HR_001", 1)[1]
        hand = hand.split("NEW HANDRA /TA_056_TOP/HR_001", 1)[0] if tag == "TA_001" else hand
        head = re.search(
            r"POS (E|W) ([0-9.]+)mm (N|S) ([0-9.]+)mm U ([0-9.]+)mm",
            hand,
        )
        assert head, f"{tag}: HANDRA POS not found"
        start_e = float(head.group(2)) if head.group(1) == "E" else -float(head.group(2))
        start_n = float(head.group(4)) if head.group(3) == "N" else -float(head.group(4))
        assert abs(head.group(5) and float(head.group(5)) - pu) < 0.01, f"{tag}: platform U mismatch"
        assert abs(start_e - (ce + r)) < 0.01, f"{tag}: east start mismatch"
        assert abs(start_n - cn) < 0.01, f"{tag}: north start mismatch"

        # Every RPATH point (POINTR and CURVE through-point) must sit on the circle.
        pts = re.findall(
            r"POS (E|W) ([0-9.]+)mm (N|S) ([0-9.]+)mm U 0\.00mm",
            hand,
        )
        assert len(pts) == 8, f"{tag}: expected 8 RPATH points, got {len(pts)}"
        for p in pts:
            de = float(p[1]) if p[0] == "E" else -float(p[1])
            dn = float(p[3]) if p[2] == "N" else -float(p[3])
            dist = math.hypot(start_e + de - ce, start_n + dn - cn)
            assert abs(dist - r) < 0.02, f"{tag}: point {de},{dn} is {dist:.3f} from centre (R={r})"


def find_zone_end(lines: list[str]) -> int:
    """Index of the END that closes ZONE /WSB_TA (first time the NEW/END stack empties)."""
    stack: list[str] = []
    for i, raw in enumerate(lines):
        line = raw.strip()
        m = re.match(r"^NEW (\S+)", line)
        if m:
            stack.append(m.group(1))
        elif line == "END":
            if stack:
                stack.pop()
                if not stack:
                    return i
    raise AssertionError("ZONE closing END not found")


def assert_stack_balanced(script: str, new_block: str) -> None:
    """The NEW/END stack must empty exactly once, at the ZONE closing END."""
    lines = script.splitlines()
    stack: list[str] = []
    emptied_at: list[int] = []
    for i, raw in enumerate(lines):
        line = raw.strip()
        m = re.match(r"^NEW (\S+)", line)
        if m:
            stack.append(m.group(1))
        elif line == "END":
            assert stack, f"stray END at line {i + 1}"
            stack.pop()
            if not stack:
                emptied_at.append(i + 1)
    assert not stack, f"unbalanced stack, {len(stack)} open at EOF"
    assert len(emptied_at) == 1, f"expected exactly one stack-empty point, got {emptied_at}"
    block_lines = new_block.count("\n") + 1
    assert emptied_at[0] == 12984 + block_lines, (
        f"ZONE END expected at line {12984 + block_lines}, got {emptied_at[0]}"
    )


def main() -> None:
    with IMPORT.open("r", encoding="utf-8-sig", errors="replace", newline="") as fh:
        original = fh.read()
    block = build_block()
    verify_block(block)

    lines = original.splitlines(True)
    zone_end_idx = find_zone_end(lines)
    offset = sum(len(x) for x in lines[:zone_end_idx])
    # Preserve the original file's byte conventions: UTF-8 BOM and CRLF.
    block = block.replace("\n", "\r\n")
    candidate = original[:offset] + block + "\r\n" + original[offset:]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as fh:
        fh.write(candidate)

    # The candidate must be the original with ONE insertion, and the NEW/END
    # hierarchy must stay balanced (the structure block lives inside the ZONE).
    with OUTPUT.open("r", encoding="utf-8-sig", newline="") as fh:
        written = fh.read()
    assert written == original[:offset] + block + "\r\n" + original[offset:]
    assert_stack_balanced(written, block)
    print(f"wrote {OUTPUT}")
    print(f"inserted {len(block.splitlines())} lines before original ZONE END line {zone_end_idx + 1}")


if __name__ == "__main__":
    main()
