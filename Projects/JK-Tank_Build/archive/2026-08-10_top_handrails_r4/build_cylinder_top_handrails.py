"""Build WSB tank-top handrails r4 (user-corrected position).

Reconciled continuation of:
  imports/2026-08-10_jk_tank_edited_by_me_hexbolts.txt

r3 (platform disc + handrail on the roof-frustum top) rendered correctly but
the user corrected the position:

> 可以，楼梯正常出现；但是位置不对，我要的围绕圆柱顶端的大圆转，
> 而不是圆柱上圆台顶端的小圆；你直接插在圆柱顶端圆面上绕着转，
> 然后我再调整圆台大小

So the handrail ring moves from the frustum top (small circle, DTOP) to the
top of the shell cylinder (big circle): TA-001 DIAM 10800 / TA-056 DIAM 9900,
both at U 26400. The frustum and its platform remain the designer's to adjust
afterwards; no platform disc is emitted in this revision.

The r3 SUBEQUIPMENTs (/205_TA_001_TOP_PLATFORM, /205_TA_056_TOP_PLATFORM)
are not present in this file; load r4 on a model state without them (or delete
them first), otherwise two handrail rings will coexist.
"""

from __future__ import annotations

import hashlib
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.parents[1]))  # repo root, where the wsb package lives

IMPORT = ROOT / "imports" / "2026-08-10_jk_tank_edited_by_me_hexbolts.txt"
OUTPUT = ROOT / "output" / "WSB_TA_top_handrails_20260810_r4.txt"
DESKTOP = Path(r"C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails_r4.txt")

# ---------------------------------------------------------------------------
# Reference values (labelled in REVISION_RECORD.md)
# ---------------------------------------------------------------------------
BASE_HEIG_MM = 10.0          # circular post base plate thickness
BASE_DIAM_MM = 200.0         # circular post base plate diameter
POST_DIAM_MM = 48.3          # post tube OD (matches /SLH/PIPE48.3x3.6)
POST_HEIG_MM = 1090.0        # from the cylinder top face to the top-rail centreline
RAIL_DIAM_MM = 48.3          # rail tube OD
RAIL_TOP_U_MM = 1100.0       # top rail centreline above the cylinder top face
RAIL_MID_U_MM = 550.0        # mid rail centreline above the cylinder top face
RAIL_INSET_MM = 100.0        # plate outer edge flush with the cylinder rim
RAIL_SEGMENTS_PER_POST = 4   # rail facet count = 4 * post count

# tag -> (centre E, centre N, cylinder top U, cylinder radius, post count)
TANKS = {
    "TA_001": dict(tag="205_TA_001", ce=26863.0, cn=-11601.0,
                   top_u=26400.0, cyl_r=5400.0, posts=36),
    "TA_056": dict(tag="205_TA_056", ce=67030.0, cn=21008.0,
                   top_u=26400.0, cyl_r=4950.0, posts=32),
}


def _fmt_num(value: float) -> str:
    """Format a coordinate/dimension like the native export (no trailing zeros)."""
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return text if text not in ("", "-0") else "0"


def _fmt_dir(e: float) -> str:
    return f"E {_fmt_num(e)}mm" if e >= 0 else f"W {_fmt_num(-e)}mm"


def _fmt_ns(n: float) -> str:
    return f"N {_fmt_num(n)}mm" if n >= 0 else f"S {_fmt_num(-n)}mm"


def _pos(e: float, n: float, u: float) -> str:
    return f"POS {_fmt_dir(e)} {_fmt_ns(n)} U {_fmt_num(u)}mm"


def _plan_direction(rotation_deg: float) -> str:
    """E3D direction text for an XY bearing measured East towards North."""
    angle = rotation_deg % 360.0
    cardinals = ((0.0, "E"), (90.0, "N"), (180.0, "W"), (270.0, "S"))
    for cardinal_angle, direction in cardinals:
        if abs(angle - cardinal_angle) < 1e-9:
            return direction
    if angle < 90.0:
        return f"E {_fmt_num(angle)} N"
    if angle < 180.0:
        return f"N {_fmt_num(angle - 90.0)} W"
    if angle < 270.0:
        return f"W {_fmt_num(angle - 180.0)} S"
    return f"S {_fmt_num(angle - 270.0)} E"


def _cylinder(pos: str, diag: str, heig: str, ori: str | None = None) -> str:
    if ori is None:
        return f"NEW CYLINDER\n{pos}\nDIAM {diag}mm\nHEIG {heig}mm\n\nEND"
    return f"NEW CYLINDER\nDIAM {diag}mm\nHEIG {heig}mm\n{ori}\n{pos}\n\nEND"


def _build_tank_block(cfg: dict) -> str:
    tag = cfg["tag"]
    ce, cn = cfg["ce"], cfg["cn"]
    top_u, cyl_r = cfg["top_u"], cfg["cyl_r"]
    n_posts = cfg["posts"]
    rail_r = cyl_r - RAIL_INSET_MM

    lines = [
        f"NEW SUBEQUIPMENT /{tag}_TOP_HANDRAIL",
        "FUNC '001024'",
        "BUIL false",
        "DSCO unset",
        "PTSP unset",
        "INSC unset",
        "",
    ]

    step = 360.0 / n_posts
    for i in range(n_posts):
        theta = math.radians(i * step)
        pe = ce + rail_r * math.cos(theta)
        pn = cn + rail_r * math.sin(theta)
        lines += [
            f"-- {tag}: post {i + 1}/{n_posts}, circular base plate + post at bearing {i * step:.1f} deg",
            _cylinder(_pos(pe, pn, top_u + BASE_HEIG_MM / 2.0),
                      _fmt_num(BASE_DIAM_MM), _fmt_num(BASE_HEIG_MM)),
            _cylinder(_pos(pe, pn, top_u + BASE_HEIG_MM + POST_HEIG_MM / 2.0),
                      _fmt_num(POST_DIAM_MM), _fmt_num(POST_HEIG_MM)),
            "",
        ]

    n_seg = RAIL_SEGMENTS_PER_POST * n_posts
    seg_step = 360.0 / n_seg
    chord = 2.0 * rail_r * math.sin(math.radians(seg_step / 2.0))
    lines += [
        f"-- {tag}: top rail, {n_seg} tangent segments, tube DIAM {RAIL_DIAM_MM:.1f} at U {top_u + RAIL_TOP_U_MM:.0f}",
    ]
    for i in range(n_seg):
        theta_mid = math.radians((i + 0.5) * seg_step)
        me = ce + rail_r * math.cos(theta_mid)
        mn = cn + rail_r * math.sin(theta_mid)
        bearing = math.degrees(theta_mid) + 90.0
        ori = f"ORI Z IS {_plan_direction(bearing)} AND Y IS U"
        lines.append(
            _cylinder(_pos(me, mn, top_u + RAIL_TOP_U_MM),
                      _fmt_num(RAIL_DIAM_MM), _fmt_num(chord), ori)
        )
    lines += [
        "",
        f"-- {tag}: mid rail, {n_seg} tangent segments, tube DIAM {RAIL_DIAM_MM:.1f} at U {top_u + RAIL_MID_U_MM:.0f}",
    ]
    for i in range(n_seg):
        theta_mid = math.radians((i + 0.5) * seg_step)
        me = ce + rail_r * math.cos(theta_mid)
        mn = cn + rail_r * math.sin(theta_mid)
        bearing = math.degrees(theta_mid) + 90.0
        ori = f"ORI Z IS {_plan_direction(bearing)} AND Y IS U"
        lines.append(
            _cylinder(_pos(me, mn, top_u + RAIL_MID_U_MM),
                      _fmt_num(RAIL_DIAM_MM), _fmt_num(chord), ori)
        )
    lines.append("")
    lines.append("END")
    return "\n".join(lines)


def _new_stack_end(lines: list[str], start: int, token: str) -> int:
    depth = 0
    for i in range(start, len(lines)):
        stripped = lines[i].strip()
        if re.match(r"^NEW \S+", stripped):
            depth += 1
        elif stripped == "END":
            depth -= 1
            if depth == 0:
                return i
    raise AssertionError(f"no closing END for {token}")


def build_blocks() -> dict[str, str]:
    return {key: _build_tank_block(cfg) for key, cfg in TANKS.items()}


def insert_blocks(original: str, blocks: dict[str, str]) -> str:
    lines = original.splitlines(True)
    inserts: list[tuple[int, str]] = []
    for tag, block in blocks.items():
        hit = None
        for i, raw in enumerate(lines):
            if raw.strip() == f"NEW SUBEQUIPMENT /{TANKS[tag]['tag']}_ACCESS":
                hit = i
                break
        assert hit is not None, f"{tag}: ACCESS SUBEQUIPMENT not found"
        end = _new_stack_end(lines, hit, "ACCESS")
        inserts.append((end + 1, block))
    inserts.sort(key=lambda item: item[0], reverse=True)
    for index, block in inserts:
        lines.insert(index, block.replace("\n", "\r\n") + "\r\n")
    return "".join(lines)


def verify_geometry(blocks: dict[str, str]) -> None:
    for tag, cfg in TANKS.items():
        block = blocks[tag]
        top_u, cyl_r = cfg["top_u"], cfg["cyl_r"]
        ce, cn = cfg["ce"], cfg["cn"]
        n_posts = cfg["posts"]
        rail_r = cyl_r - RAIL_INSET_MM

        cylinders: list[dict[str, float | str]] = []
        for part in block.split("NEW CYLINDER")[1:]:
            body = part.split("\nEND", 1)[0]
            pos = re.search(r"POS E (\S+)mm (N|S) (\S+)mm U (\S+)mm", body)
            diam = re.search(r"DIAM (\S+)mm", body)
            heig = re.search(r"HEIG (\S+)mm", body)
            ori = re.search(r"ORI Z IS (.+) AND Y IS U", body)
            assert pos and diam and heig, f"{tag}: malformed CYLINDER block"
            e = float(pos.group(1))
            n = float(pos.group(3)) if pos.group(2) == "N" else -float(pos.group(3))
            cylinders.append({
                "e": e, "n": n, "u": float(pos.group(4)),
                "diam": float(diam.group(1)), "heig": float(heig.group(1)),
                "ori": ori.group(1) if ori else None,
            })

        expected = 2 * n_posts + 2 * RAIL_SEGMENTS_PER_POST * n_posts
        assert len(cylinders) == expected, (
            f"{tag}: expected {expected} CYLINDERs, got {len(cylinders)}"
        )

        for idx in range(0, 2 * n_posts, 2):
            base, post = cylinders[idx], cylinders[idx + 1]
            for part, expect_diam, expect_heig, expect_u in (
                (base, BASE_DIAM_MM, BASE_HEIG_MM, top_u + BASE_HEIG_MM / 2.0),
                (post, POST_DIAM_MM, POST_HEIG_MM,
                 top_u + BASE_HEIG_MM + POST_HEIG_MM / 2.0),
            ):
                dist = math.hypot(part["e"] - ce, part["n"] - cn)
                assert abs(dist - rail_r) < 0.05, (
                    f"{tag}: post element off the rail circle by {abs(dist - rail_r):.3f} mm"
                )
                assert abs(float(part["u"]) - expect_u) < 0.01
                assert abs(float(part["diam"]) - expect_diam) < 0.01
                assert abs(float(part["heig"]) - expect_heig) < 0.01
                assert part["ori"] is None

        rails = cylinders[2 * n_posts:]
        n_seg = RAIL_SEGMENTS_PER_POST * n_posts
        seg_step = math.radians(360.0 / n_seg)
        chord = 2.0 * rail_r * math.sin(seg_step / 2.0)
        for idx, part in enumerate(rails):
            dist = math.hypot(part["e"] - ce, part["n"] - cn)
            assert abs(dist - rail_r) < 0.1, (
                f"{tag}: rail segment {idx} off circle by {abs(dist - rail_r):.3f} mm"
            )
            assert abs(float(part["u"]) - (top_u + (RAIL_TOP_U_MM if idx < n_seg else RAIL_MID_U_MM))) < 0.01
            assert abs(float(part["diam"]) - RAIL_DIAM_MM) < 0.01
            assert abs(float(part["heig"]) - chord) < 0.01
            assert part["ori"] is not None

        assert BASE_HEIG_MM > 0 and POST_HEIG_MM > 0 and chord > 0
        assert all(float(p["u"]) >= top_u - 1e-9 for p in cylinders)


def assert_stack_balanced(script: str) -> int:
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
    return emptied_at[0]


def main() -> None:
    with IMPORT.open("r", encoding="utf-8-sig", errors="replace", newline="") as fh:
        original = fh.read()
    blocks = build_blocks()
    verify_geometry(blocks)

    candidate = insert_blocks(original, blocks)
    assert_stack_balanced(candidate)

    rebuilt = candidate
    for block in reversed(list(blocks.values())):
        rebuilt = rebuilt.replace(block.replace("\n", "\r\n") + "\r\n", "", 1)
    assert rebuilt == original, "candidate is not original + 2 insertions"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as fh:
        fh.write(candidate)
    if DESKTOP.parent.exists():
        with DESKTOP.open("w", encoding="utf-8-sig", newline="") as fh:
            fh.write(candidate)

    from wsb.pml_builder import validate_pml

    base_problems = validate_pml(original)
    candidate_problems = validate_pml(candidate)
    norm = lambda text: re.sub(r"L\d+", "L#", text)
    base_norms = {norm(p) for p in base_problems}
    new_problems = [p for p in candidate_problems if norm(p) not in base_norms]
    assert not new_problems, f"validate_pml found {len(new_problems)} new problems: {new_problems}"
    for tag, block in blocks.items():
        block_problems = validate_pml(block)
        assert not block_problems, f"{tag}: block has {len(block_problems)} problems: {block_problems}"

    def sha256_bytes(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8-sig")).hexdigest().upper()

    print(f"wrote {OUTPUT}")
    if DESKTOP.parent.exists():
        print(f"wrote {DESKTOP}")
    print(f"inserted {len(blocks)} SUBEQUIPMENT blocks "
          f"({sum(len(b.splitlines()) for b in blocks.values())} lines total)")
    print(f"validate_pml: {len(base_problems)} pre-existing findings, "
          f"{len(new_problems)} new")
    print(f"SHA-256 (utf-8-sig bytes): {sha256_bytes(candidate)}")


if __name__ == "__main__":
    main()
