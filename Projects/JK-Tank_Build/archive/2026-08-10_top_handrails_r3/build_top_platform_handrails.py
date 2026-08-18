"""Build WSB tank-top handrails r3 (primitive-based, user-corrected).

Reconciled continuation of:
  imports/2026-08-10_jk_tank_edited_by_me_hexbolts.txt

r2 (HANDRA + RPATH CURTYP THRU + RAILSET, no posts) loaded in E3D but rendered
nothing and the user rejected it:

> 没有形成楼梯，放置的位置也不对；应是圆盘底座；

This revision replaces the unverified HANDRA/RPATH template form with plain
CYLI primitives under a new SUBEQUIPMENT per tank, so the geometry is
guaranteed visible and placed on the real roof-frustum top platform:

* a circular platform disc (圆盘底座) closing the frustum top face;
* one circular base plate per post;
* vertical posts at the platform rim (post spacing <= 1000 mm);
* top rail (platform + 1100 mm) and mid rail (platform + 550 mm) built from
  short tangent CYLI segments (sagitta < 2.5 mm, visually smooth).

Only two insertion points are used (after the existing ACCESS SUBEQUIPMENT of
205_TA_001 and 205_TA_056); everything else is preserved byte-for-byte.
205-TA-006 does not exist in this export; 205-TA-056 is the second frustum-top
platform tank (see REVISION_RECORD.md).
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.parents[1]))  # repo root, where the wsb package lives
IMPORT = ROOT / "imports" / "2026-08-10_jk_tank_edited_by_me_hexbolts.txt"
OUTPUT = ROOT / "output" / "WSB_TA_top_handrails_20260810_r3.txt"
DESKTOP = Path(r"C:\Users\A\Desktop\jk_tank_edited_by_me_top_handrails_r3.txt")

# ---------------------------------------------------------------------------
# Reference values (labelled in REVISION_RECORD.md)
# ---------------------------------------------------------------------------
DISC_HEIG_MM = 12.0          # circular platform plate thickness
BASE_DIAM_MM = 200.0         # circular post base plate diameter
BASE_HEIG_MM = 10.0          # circular post base plate thickness
POST_DIAM_MM = 48.3          # post tube OD (matches /SLH/PIPE48.3x3.6)
POST_HEIG_MM = 1090.0        # from plate top to the top-rail centreline
RAIL_DIAM_MM = 48.3          # rail tube OD
RAIL_TOP_U_MM = 1100.0       # top rail centreline above the platform
RAIL_MID_U_MM = 550.0        # mid rail centreline above the platform
RAIL_INSET_MM = 150.0        # handrail circle inset from the platform rim
RAIL_SEGMENTS_PER_POST = 4   # rail facet count = 4 * post count

# tag -> (centre E, centre N, platform top U, platform radius, post count)
TANKS = {
    "TA_001": dict(tag="205_TA_001", ce=26863.0, cn=-11601.0,
                   plat_u=28200.0, plat_r=3000.0, posts=20),
    "TA_056": dict(tag="205_TA_056", ce=67030.0, cn=21008.0,
                   plat_u=27700.0, plat_r=3250.0, posts=24),
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
    """E3D direction text for an XY bearing measured East towards North.

    Mirrors wsb.pml_builder._plan_direction (verified formatting).
    30 -> 'E 30 N'; 135 -> 'N 45 W'.
    """
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
    plat_u, plat_r = cfg["plat_u"], cfg["plat_r"]
    n_posts = cfg["posts"]
    rail_r = plat_r - RAIL_INSET_MM

    lines = [
        f"NEW SUBEQUIPMENT /{tag}_TOP_PLATFORM",
        "FUNC '001024'",
        "BUIL false",
        "DSCO unset",
        "PTSP unset",
        "INSC unset",
        "",
        f"-- {tag}: circular platform disc (disc base), DIAM {2 * plat_r:.0f} x {DISC_HEIG_MM:.0f}, top face at U {plat_u:.0f}",
        _cylinder(_pos(ce, cn, plat_u - DISC_HEIG_MM / 2.0),
                  _fmt_num(2 * plat_r), _fmt_num(DISC_HEIG_MM)),
        "",
    ]

    step = 360.0 / n_posts
    for i in range(n_posts):
        theta = math.radians(i * step)
        pe = ce + rail_r * math.cos(theta)
        pn = cn + rail_r * math.sin(theta)
        lines += [
            f"-- {tag}: post {i + 1}/{n_posts}, circular base plate + post at bearing {i * step:.1f} deg",
            _cylinder(_pos(pe, pn, plat_u + BASE_HEIG_MM / 2.0),
                      _fmt_num(BASE_DIAM_MM), _fmt_num(BASE_HEIG_MM)),
            _cylinder(_pos(pe, pn, plat_u + BASE_HEIG_MM + POST_HEIG_MM / 2.0),
                      _fmt_num(POST_DIAM_MM), _fmt_num(POST_HEIG_MM)),
            "",
        ]

    n_seg = RAIL_SEGMENTS_PER_POST * n_posts
    seg_step = 360.0 / n_seg
    chord = 2.0 * rail_r * math.sin(math.radians(seg_step / 2.0))
    lines += [
        f"-- {tag}: top rail, {n_seg} tangent segments, tube DIAM {RAIL_DIAM_MM:.1f} at U {plat_u + RAIL_TOP_U_MM:.0f}",
    ]
    for i in range(n_seg):
        theta_mid = math.radians((i + 0.5) * seg_step)
        me = ce + rail_r * math.cos(theta_mid)
        mn = cn + rail_r * math.sin(theta_mid)
        bearing = math.degrees(theta_mid) + 90.0
        ori = f"ORI Z IS {_plan_direction(bearing)} AND Y IS U"
        lines.append(
            _cylinder(_pos(me, mn, plat_u + RAIL_TOP_U_MM),
                      _fmt_num(RAIL_DIAM_MM), _fmt_num(chord), ori)
        )
    lines += [
        "",
        f"-- {tag}: mid rail, {n_seg} tangent segments, tube DIAM {RAIL_DIAM_MM:.1f} at U {plat_u + RAIL_MID_U_MM:.0f}",
    ]
    for i in range(n_seg):
        theta_mid = math.radians((i + 0.5) * seg_step)
        me = ce + rail_r * math.cos(theta_mid)
        mn = cn + rail_r * math.sin(theta_mid)
        bearing = math.degrees(theta_mid) + 90.0
        ori = f"ORI Z IS {_plan_direction(bearing)} AND Y IS U"
        lines.append(
            _cylinder(_pos(me, mn, plat_u + RAIL_MID_U_MM),
                      _fmt_num(RAIL_DIAM_MM), _fmt_num(chord), ori)
        )
    lines.append("")
    lines.append("END")
    return "\n".join(lines)


def _new_stack_end(lines: list[str], start: int, token: str) -> int:
    """Index of the END that closes the NEW token opened at ``start``."""
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
        block_text = block.replace("\n", "\r\n") + "\r\n"
        lines.insert(index, block_text)
    return "".join(lines)


def verify_geometry(blocks: dict[str, str]) -> None:
    for tag, cfg in TANKS.items():
        block = blocks[tag]
        plat_u, plat_r = cfg["plat_u"], cfg["plat_r"]
        ce, cn = cfg["ce"], cfg["cn"]
        n_posts = cfg["posts"]
        rail_r = plat_r - RAIL_INSET_MM

        # Parse every CYLINDER block, whatever its attribute order.
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
        assert len(cylinders) == 1 + 2 * n_posts + 2 * RAIL_SEGMENTS_PER_POST * n_posts, (
            f"{tag}: expected {1 + 2 * n_posts + 2 * RAIL_SEGMENTS_PER_POST * n_posts} "
            f"CYLINDERs, got {len(cylinders)}"
        )

        # Disc: centred on the tank, top face flush with the platform.
        disc = cylinders[0]
        assert abs(disc["e"] - ce) < 0.01 and abs(disc["n"] - cn) < 0.01, (
            f"{tag}: disc centre mismatch"
        )
        assert abs(float(disc["u"]) - (plat_u - DISC_HEIG_MM / 2.0)) < 0.01
        assert abs(float(disc["diam"]) - 2 * plat_r) < 0.01
        assert abs(float(disc["heig"]) - DISC_HEIG_MM) < 0.01
        assert disc["ori"] is None

        # Every post base sits on the rail circle; heights match.
        for idx in range(1, 1 + 2 * n_posts, 2):
            base, post = cylinders[idx], cylinders[idx + 1]
            for part, expect_diam, expect_heig, expect_u in (
                (base, BASE_DIAM_MM, BASE_HEIG_MM, plat_u + BASE_HEIG_MM / 2.0),
                (post, POST_DIAM_MM, POST_HEIG_MM,
                 plat_u + BASE_HEIG_MM + POST_HEIG_MM / 2.0),
            ):
                assert abs(math.hypot(part["e"] - ce, part["n"] - cn) - rail_r) < 0.05, (
                    f"{tag}: element off the rail circle by "
                    f"{abs(math.hypot(part['e'] - ce, part['n'] - cn) - rail_r):.3f} mm"
                )
                assert abs(float(part["u"]) - expect_u) < 0.01
                assert abs(float(part["diam"]) - expect_diam) < 0.01
                assert abs(float(part["heig"]) - expect_heig) < 0.01
                assert part["ori"] is None

        # Every rail segment: midpoint on the rail circle, tangent ORI,
        # chord length matching the facet geometry, joint gap negligible.
        rails = cylinders[1 + 2 * n_posts:]
        assert len(rails) == 2 * RAIL_SEGMENTS_PER_POST * n_posts
        n_seg = RAIL_SEGMENTS_PER_POST * n_posts
        seg_step = math.radians(360.0 / n_seg)
        chord = 2.0 * rail_r * math.sin(seg_step / 2.0)
        for idx, part in enumerate(rails):
            dist = math.hypot(part["e"] - ce, part["n"] - cn)
            assert abs(dist - rail_r) < 0.1, f"{tag}: rail segment {idx} off circle by {abs(dist - rail_r):.3f} mm"
            assert abs(float(part["u"]) - (plat_u + (RAIL_TOP_U_MM if idx < n_seg else RAIL_MID_U_MM))) < 0.01
            assert abs(float(part["diam"]) - RAIL_DIAM_MM) < 0.01
            assert abs(float(part["heig"]) - chord) < 0.01
            assert part["ori"] is not None

        # Bounds: nothing below the disc bottom, all heights positive.
        assert DISC_HEIG_MM > 0 and BASE_HEIG_MM > 0 and POST_HEIG_MM > 0 and chord > 0
        assert all(float(p["u"]) >= plat_u - DISC_HEIG_MM / 2.0 - 1e-9 for p in cylinders)


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

    # Prove the candidate is the original with exactly two insertions.
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

    import hashlib

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
