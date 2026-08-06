"""Generate the bolted channel frame EXTRUSION certification candidate.

PML-STUDY-EXTR-002 tests one idea: EXTRUSION is not only for isolated
fastener heads. It is the right element whenever a solid has a constant,
non-rectangular cross-section. The candidate is one coherent, bolted
mounting frame that uses five distinct profile families:

* an 8-vertex C-channel rail (web plus two tall flanges with return lips),
* a 6-vertex notched cleat bracket, mirrored for the west end,
* the M16 hex nut profile (the VERIFIED native form), used 16 times,
* BOX for the base plate and the pedestal block,
* CYLINDER for the bolt shanks and the pedestal boss.

Every element form used here is individually VERIFIED in E3D Design
Mk3.1.11.0 (EXTRUSION via PML-STUDY-EXTR-001/01-04; CYLINDER and BOX via
the production tank/pump macros). The assembly itself is new and awaits a
user E3D verdict. Nothing is promoted to the shared skill before
certification.
"""

from __future__ import annotations

import hashlib
import math
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[3]
sys.path.insert(0, str(REPO_ROOT))

from wsb.extrusion_builder import build_extrusion
from wsb.pml_builder import validate_pml


def fmt(value: float) -> str:
    if abs(value) < 1e-9:
        value = 0.0
    return f"{value:.6f}".rstrip("0").rstrip(".") or "0"


# ---------------------------------------------------------------------------
# Profiles (local LOOP XY coordinates)
# ---------------------------------------------------------------------------

# M16 hex nut: 24 mm across flats. Local X maps to world E/W by orientation;
# the profile is centred on the bolt axis so the mapping direction is
# irrelevant for position.
HEX_M16 = (
    (-13.856406, 0.0),
    (-6.928203, 12.0),
    (6.928203, 12.0),
    (13.856406, 0.0),
    (6.928203, -12.0),
    (-6.928203, -12.0),
)

# C-channel rail, local X = world N, local Y = world U (ORI Y IS U AND
# Z IS E): web at U 16..26 spanning N -50..50, flanges at N +/-40..50 up to
# U 66, return lips down to U 26.
CHANNEL = (
    (-50.0, 16.0),
    (50.0, 16.0),
    (50.0, 66.0),
    (40.0, 66.0),
    (40.0, 26.0),
    (-40.0, 26.0),
    (-40.0, 66.0),
    (-50.0, 66.0),
)

# Notched cleat. With ORI Y IS U AND Z IS N the local X axis maps to world
# W (right-handed frame), so a cleat occupying world E 130..170 uses local
# X -170..-130. The notch leaves the world-East top corner cut down.
CLEAT_PLUS = (
    (-170.0, 16.0),
    (-130.0, 16.0),
    (-130.0, 136.0),
    (-150.0, 136.0),
    (-150.0, 106.0),
    (-170.0, 106.0),
)

# Mirror cleat for world E -170..-130 (local X runs 130..170).
CLEAT_MINUS = tuple((-x, y) for x, y in CLEAT_PLUS)


# ---------------------------------------------------------------------------
# Primitive helpers
# ---------------------------------------------------------------------------


def cylinder(
    diameter: float,
    height: float,
    bottom: Tuple[float, float, float],
    z_axis: str = "U",
    y_axis: str = "N",
) -> str:
    """Solid cylinder, bottom-face datum, ORI before POS (IR-1/IR-2)."""
    east, north, up = bottom
    axis = {"U": 2, "D": 2, "N": 1, "S": 1, "E": 0, "W": 0}[z_axis]
    centre = [east, north, up]
    if z_axis in ("U", "N", "E"):
        centre[axis] += height / 2.0
    else:
        centre[axis] -= height / 2.0
    return "\n".join(
        (
            "NEW CYLINDER",
            f"DIAM {fmt(diameter)}mm",
            f"HEIG {fmt(height)}mm",
            f"ORI Y IS {y_axis} AND Z IS {z_axis}",
            f"POS E {fmt(centre[0])}mm N {fmt(centre[1])}mm U {fmt(centre[2])}mm",
            "END",
        )
    )


def box(xlen: float, ylen: float, zlen: float, centre: Tuple[float, float, float]) -> str:
    """Axis-aligned BOX positioned by its geometric centre; no ORI needed."""
    east, north, up = centre
    return "\n".join(
        (
            "NEW BOX",
            f"XLEN {fmt(xlen)}mm",
            f"YLEN {fmt(ylen)}mm",
            f"ZLEN {fmt(zlen)}mm",
            f"POS E {fmt(east)}mm N {fmt(north)}mm U {fmt(up)}mm",
            "END",
        )
    )


def hex_nut(
    bolt_e: float,
    north: float,
    up: float,
    height: float = 20.0,
) -> str:
    """True hexagonal nut: EXTRUSION profile plane at (E, N, U), HEIG along
    local +Z (world +N)."""
    return build_extrusion(
        (bolt_e, north, up),
        "Y IS U AND Z IS N",
        height,
        HEX_M16,
        level=(5, 10),
    ).rstrip()


def bolt(name: str, bolt_e: float, side: int) -> str:
    """One through-bolt clamping a cleat to the rail flange.

    side +1 (north flange, N 40..50):
        inner nut N 20..40, flange 40..50, cleat 50..66, outer nut 66..86,
        shank N 20..86 (HEIG 66).
    side -1 (south flange, N -50..-40):
        outer nut -86..-66, cleat -66..-50, flange -50..-40, inner nut
        -60..-40, shank N -86..-40 (HEIG 46).

    Every nut touches a face and every shank passes through the whole
    sandwich, so nothing is detached (IR-9b).
    """
    if side == 1:
        inner_north, outer_north, shank_bottom, shank_height = 20.0, 66.0, 20.0, 66.0
    else:
        inner_north, outer_north, shank_bottom, shank_height = -60.0, -86.0, -86.0, 46.0
    parts = [
        hex_nut(bolt_e, inner_north, 45.0),
        hex_nut(bolt_e, outer_north, 45.0),
        cylinder(16.0, shank_height, (bolt_e, shank_bottom, 45.0), z_axis="N", y_axis="U"),
    ]
    return f"NEW SUBEQUIPMENT /{name}\n" + "\n".join(parts) + "\nEND"


def cleat(name: str, profile: Sequence[Tuple[float, float]], side: int) -> str:
    """One notched cleat bracket, profile end plane on the rail flange face."""
    north = 50.0 if side == 1 else -66.0
    body = build_extrusion(
        (0.0, north, 0.0),
        "Y IS U AND Z IS N",
        16.0,
        profile,
    ).rstrip()
    return f"NEW SUBEQUIPMENT /{name}\n{body}\nEND"


def wrap(name: str, body: str, description: str) -> str:
    """Same loadable wrapper as the VERIFIED EXTRUSION candidates."""
    return "\n".join(
        (
            "$S-  -- Synonym translation OFF",
            "ONERROR GOLABEL /ERROR3",
            "INPUT BEGIN",
            f"NEW EQUIPMENT /{name}",
            "POS E 0mm N 0mm U 0mm",
            f"DESC '{description}'",
            body.rstrip(),
            "END",
            f"INPUT END EQUIPMENT /{name}",
            "INPUT FINISH",
            "LABEL /ERROR3",
            "handle ANY",
            "$S+",
            "RETURN ERROR",
            "endhandle",
            "$S+  -- Synonym translation ON",
            "",
        )
    )


def candidate() -> str:
    """Assemble the bolted channel mounting frame."""
    base = box(400.0, 200.0, 16.0, (0.0, 0.0, 8.0))
    rail = build_extrusion(
        (-180.0, 0.0, 0.0),
        "Y IS U AND Z IS E",
        360.0,
        CHANNEL,
    ).rstrip()
    pedestal = "\n".join(
        (
            box(80.0, 60.0, 40.0, (0.0, 0.0, 46.0)),
            cylinder(30.0, 30.0, (0.0, 0.0, 66.0)),
        )
    )

    subes = [
        f"NEW SUBEQUIPMENT /CODEX_EXTR_002_BASE\n{base}\nEND",
        f"NEW SUBEQUIPMENT /CODEX_EXTR_002_RAIL\n{rail}\nEND",
        f"NEW SUBEQUIPMENT /CODEX_EXTR_002_PEDESTAL\n{pedestal}\nEND",
        cleat("CODEX_EXTR_002_CLEAT_NE", CLEAT_PLUS, 1),
        cleat("CODEX_EXTR_002_CLEAT_NW", CLEAT_MINUS, 1),
        cleat("CODEX_EXTR_002_CLEAT_SE", CLEAT_PLUS, -1),
        cleat("CODEX_EXTR_002_CLEAT_SW", CLEAT_MINUS, -1),
        bolt("CODEX_EXTR_002_BOLT_NE1", 138.0, 1),
        bolt("CODEX_EXTR_002_BOLT_NE2", 162.0, 1),
        bolt("CODEX_EXTR_002_BOLT_NW1", -138.0, 1),
        bolt("CODEX_EXTR_002_BOLT_NW2", -162.0, 1),
        bolt("CODEX_EXTR_002_BOLT_SE1", 138.0, -1),
        bolt("CODEX_EXTR_002_BOLT_SE2", 162.0, -1),
        bolt("CODEX_EXTR_002_BOLT_SW1", -138.0, -1),
        bolt("CODEX_EXTR_002_BOLT_SW2", -162.0, -1),
    ]
    return wrap(
        "CODEX_EXTR_002_FRAME",
        "\n".join(subes),
        "BOLTED CHANNEL MOUNTING FRAME - EXTRUSION ASSEMBLY STUDY",
    )


# ---------------------------------------------------------------------------
# Numerical verification - property checks on the emitted text. The parser
# re-derives every primitive's occupied world ranges from its element-specific
# datum, then checks contacts, bounds and the lowest point. It never greps for
# a POS string.
# ---------------------------------------------------------------------------

_NEW = re.compile(r"^NEW\s+(CYLINDER|CONE|DISH|BOX|EXTRUSION)\b", re.I)
_SUBE = re.compile(r"^NEW\s+SUBEQUIPMENT\s+(/\S+)", re.I)
_ATTR = re.compile(r"^(DIAM|HEIG|DTOP|DBOT|RADIUS|XLEN|YLEN|ZLEN|POS|ORI|LEVE)\s+(.*)$", re.I)
_ORI = re.compile(r"^Y\s+IS\s+([ENWSUD])\s+AND\s+Z\s+IS\s+([ENWSUD])$", re.I)

_VECTORS = {
    "E": (1.0, 0.0, 0.0),
    "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0),
    "S": (0.0, -1.0, 0.0),
    "U": (0.0, 0.0, 1.0),
    "D": (0.0, 0.0, -1.0),
}


def _numbers(text: str) -> List[float]:
    return [float(m) for m in re.findall(r"[-+]?\d+(?:\.\d+)?", text)]


def _cross(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def parse_blocks(macro: str) -> List[Dict]:
    """Parse emitted primitive blocks into type / sube / attrs / vertices."""
    blocks: List[Dict] = []
    sube: Optional[str] = None
    block: Optional[Dict] = None
    depth = 0
    for raw in macro.splitlines():
        line = raw.strip()
        sube_match = _SUBE.match(line)
        if sube_match:
            sube = sube_match.group(1)
            continue
        new_match = _NEW.match(line)
        if new_match:
            block = {
                "type": new_match.group(1).upper(),
                "sube": sube,
                "attrs": {},
                "vertices": [],
                "order": [],
            }
            if block["type"] == "EXTRUSION":
                depth = 0
            continue
        if block is None:
            continue
        if line == "END":
            if block["type"] == "EXTRUSION":
                if depth == 0:
                    blocks.append(block)
                    block = None
                elif depth == 1:
                    depth = 0
                else:
                    depth = 1
            else:
                blocks.append(block)
                block = None
            continue
        if line.startswith("NEW LOOP"):
            depth = 1
            continue
        if line.startswith("NEW VERTEX"):
            depth = 2
            continue
        if block["type"] == "EXTRUSION" and depth > 0:
            if depth == 2:
                east, north, _ = _numbers(line)
                block["vertices"].append((east, north))
            continue
        attr_match = _ATTR.match(line)
        if attr_match and not line.startswith("NEW "):
            key = attr_match.group(1).upper()
            if key == "ORI":
                block["attrs"][key] = attr_match.group(2).strip()
            else:
                block["attrs"][key] = _numbers(attr_match.group(2))
            block["order"].append(key)
    return blocks


def _pos(block: Dict) -> Tuple[float, float, float]:
    e, n, u = block["attrs"].get("POS", [0.0, 0.0, 0.0])
    return float(e), float(n), float(u)


def _orientation(block: Dict) -> Optional[Tuple[Tuple[float, float, float], Tuple[float, float, float]]]:
    text = block["attrs"].get("ORI")
    if not text:
        return None
    match = _ORI.fullmatch(" ".join(text.upper().split()))
    if not match:
        raise AssertionError(f"unparseable ORI {text!r}")
    y_axis, z_axis = match.groups()
    return _VECTORS[y_axis], _VECTORS[z_axis]


def occupied_ranges(block: Dict) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
    """World (E, N, U) occupied ranges re-derived from element-specific datum."""
    pos = _pos(block)
    kind = block["type"]
    attrs = block["attrs"]

    if kind in ("CYLINDER", "CONE"):
        height = float(attrs["HEIG"][0])
        half = height / 2.0
        zv = _orientation(block)[1]
        ranges = [(p - half, p + half) if zv[axis] else (p, p) for axis, p in enumerate(pos)]
        return tuple(ranges)  # type: ignore[return-value]

    if kind == "BOX":
        half = (float(attrs["XLEN"][0]) / 2.0, float(attrs["YLEN"][0]) / 2.0, float(attrs["ZLEN"][0]) / 2.0)
        return tuple((pos[axis] - half[axis], pos[axis] + half[axis]) for axis in range(3))  # type: ignore[return-value]

    if kind == "DISH":
        height = float(attrs["HEIG"][0])
        zv = _orientation(block)[1]
        ranges = []
        for axis, p in enumerate(pos):
            if zv[axis] == 1.0:
                ranges.append((p, p + height))
            elif zv[axis] == -1.0:
                ranges.append((p - height, p))
            else:
                ranges.append((p, p))
        return tuple(ranges)  # type: ignore[return-value]

    if kind == "EXTRUSION":
        height = float(attrs["HEIG"][0])
        yv, zv = _orientation(block)
        xv = _cross(yv, zv)
        xs = [vertex[0] for vertex in block["vertices"]]
        ys = [vertex[1] for vertex in block["vertices"]]
        extents = ((xv, (min(xs), max(xs))), (yv, (min(ys), max(ys))), (zv, (0.0, height)))
        ranges = []
        for axis in range(3):
            lo = hi = pos[axis]
            for vector, (a, b) in extents:
                if vector[axis] == 1.0:
                    lo += a
                    hi += b
                elif vector[axis] == -1.0:
                    lo += -b
                    hi += -a
            ranges.append((lo, hi))
        return tuple(ranges)  # type: ignore[return-value]

    raise AssertionError(f"unhandled primitive {kind}")


def _area(vertices: Sequence[Tuple[float, float]]) -> float:
    return abs(
        0.5
        * sum(
            x1 * y2 - x2 * y1
            for (x1, y1), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1])
        )
    )


def verify_geometry(macro: str) -> List[str]:
    """Return a list of geometry problems; empty means the model is coherent."""
    problems: List[str] = []
    blocks = parse_blocks(macro)
    if not blocks:
        return ["no primitive blocks parsed"]

    by_sube: Dict[str, List[Dict]] = {}
    for block in blocks:
        by_sube.setdefault(block["sube"], []).append(block)

    expected_subes = {
        "/CODEX_EXTR_002_BASE": 1,
        "/CODEX_EXTR_002_RAIL": 1,
        "/CODEX_EXTR_002_PEDESTAL": 2,
        "/CODEX_EXTR_002_CLEAT_NE": 1,
        "/CODEX_EXTR_002_CLEAT_NW": 1,
        "/CODEX_EXTR_002_CLEAT_SE": 1,
        "/CODEX_EXTR_002_CLEAT_SW": 1,
    }
    for name in ("NE1", "NE2", "NW1", "NW2", "SE1", "SE2", "SW1", "SW2"):
        expected_subes[f"/CODEX_EXTR_002_BOLT_{name}"] = 3
    if set(by_sube) != set(expected_subes):
        problems.append(f"SUBE set mismatch: {sorted(by_sube)}")
    for name, count in expected_subes.items():
        if len(by_sube.get(name, [])) != count:
            problems.append(f"{name}: expected {count} primitives, got {len(by_sube.get(name, []))}")

    if len(blocks) != 32:
        problems.append(f"expected 32 primitives, got {len(blocks)}")
    if sum(1 for b in blocks if b["type"] == "EXTRUSION") != 21:
        problems.append("expected 21 EXTRUSION primitives")
    if sum(1 for b in blocks if b["type"] == "CYLINDER") != 9:
        problems.append("expected 9 CYLINDER primitives")
    if sum(1 for b in blocks if b["type"] == "BOX") != 2:
        problems.append("expected 2 BOX primitives")

    def ranges_of(sube: str) -> List[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]]:
        return [occupied_ranges(block) for block in by_sube[sube]]

    def lo_axis(ranges: Sequence[Tuple[Tuple[float, float], ...]], axis: int) -> float:
        return min(r[axis][0] for r in ranges)

    def hi_axis(ranges: Sequence[Tuple[Tuple[float, float], ...]], axis: int) -> float:
        return max(r[axis][1] for r in ranges)

    # Global lowest point and dimension bounds.
    all_ranges = [occupied_ranges(block) for block in blocks]
    if lo_axis(all_ranges, 2) < -1e-6:
        problems.append(f"geometry extends below U 0: {lo_axis(all_ranges, 2):.3f}")
    for block in blocks:
        for key in ("DIAM", "HEIG", "DTOP", "DBOT", "RADIUS", "XLEN", "YLEN", "ZLEN"):
            if key in block["attrs"] and any(v <= 0 for v in block["attrs"][key]):
                problems.append(f"{block['sube']}: {block['type']} has non-positive {key}")
        if block["type"] == "EXTRUSION":
            if len(block["vertices"]) < 3 or _area(block["vertices"]) < 1e-6:
                problems.append(f"{block['sube']}: degenerate EXTRUSION profile")
        order = block["order"]
        if block["type"] in ("CYLINDER", "CONE", "DISH") and (
            "ORI" not in order or "POS" not in order or order.index("POS") < order.index("ORI")
        ):
            problems.append(f"{block['sube']}: {block['type']} violates ORI-before-POS")

    base = ranges_of("/CODEX_EXTR_002_BASE")
    rail = ranges_of("/CODEX_EXTR_002_RAIL")
    pedestal = ranges_of("/CODEX_EXTR_002_PEDESTAL")

    # Base plate: U 0..16 and footprint that covers the whole assembly.
    if hi_axis(base, 2) != 16.0 or lo_axis(base, 2) != 0.0:
        problems.append("base plate must occupy U 0..16")
    for block in blocks:
        r = occupied_ranges(block)
        if r[0][0] < -200.0 or r[0][1] > 200.0 or r[1][0] < -100.0 or r[1][1] > 100.0:
            problems.append(f"{block['sube']} {block['type']} escapes base footprint")

    # Rail sits on the base; web top U 26 carries the pedestal.
    if lo_axis(rail, 2) != 16.0 or hi_axis(rail, 2) != 66.0:
        problems.append("rail must occupy U 16..66")
    if hi_axis(rail, 0) - lo_axis(rail, 0) != 360.0:
        problems.append("rail must be 360 mm long in E")
    if lo_axis(pedestal, 2) != 26.0 or hi_axis(pedestal, 2) != 96.0:
        problems.append("pedestal must occupy U 26..96 (block 26..66, boss 66..96)")
    if lo_axis(pedestal, 0) != -40.0 or hi_axis(pedestal, 0) != 40.0:
        problems.append("pedestal must sit centred on the rail web (E -40..40)")
    if lo_axis(pedestal, 1) != -30.0 or hi_axis(pedestal, 1) != 30.0:
        problems.append("pedestal must stay between the rail flanges (N -30..30)")

    # Cleats: bottom face on the base, inner face on the rail flange face.
    for side_name, side in (("NE", 1), ("NW", 1), ("SE", -1), ("SW", -1)):
        cleat_ranges = ranges_of(f"/CODEX_EXTR_002_CLEAT_{side_name}")
        if lo_axis(cleat_ranges, 2) != 16.0 or hi_axis(cleat_ranges, 2) != 136.0:
            problems.append(f"{side_name} cleat must occupy U 16..136")
        if hi_axis(cleat_ranges, 0) - lo_axis(cleat_ranges, 0) != 40.0:
            problems.append(f"{side_name} cleat must be 40 mm wide in E")
        if hi_axis(cleat_ranges, 1) - lo_axis(cleat_ranges, 1) != 16.0:
            problems.append(f"{side_name} cleat must be 16 mm thick in N")
        if side == 1:
            if lo_axis(cleat_ranges, 1) != 50.0 or hi_axis(rail, 1) != 50.0:
                problems.append(f"{side_name} cleat inner face must touch rail N 50 face")
        else:
            if hi_axis(cleat_ranges, 1) != -50.0 or lo_axis(rail, 1) != -50.0:
                problems.append(f"{side_name} cleat inner face must touch rail N -50 face")

    # Bolts: nut faces, shank coverage and web clearance.
    for side_name, side, bolt_e in (
        ("NE1", 1, 138.0), ("NE2", 1, 162.0),
        ("NW1", 1, -138.0), ("NW2", 1, -162.0),
        ("SE1", -1, 138.0), ("SE2", -1, 162.0),
        ("SW1", -1, -138.0), ("SW2", -1, -162.0),
    ):
        bolt_ranges = ranges_of(f"/CODEX_EXTR_002_BOLT_{side_name}")
        nuts = [r for r in bolt_ranges if r[0][1] - r[0][0] > 1.0]
        shank = [r for r in bolt_ranges if r[0][1] - r[0][0] < 1.0]
        if len(nuts) != 2 or len(shank) != 1:
            problems.append(f"bolt {side_name}: expected 2 nuts + 1 shank")
            continue
        if abs(nuts[0][0][0] - bolt_e) > 20.0 or abs(nuts[1][0][0] - bolt_e) > 20.0:
            problems.append(f"bolt {side_name}: nuts not on the bolt axis E {bolt_e}")
        for nut in nuts:
            if nut[2][0] <= 26.0:
                problems.append(f"bolt {side_name}: nut dips into the rail web (U {nut[2][0]:.2f})")
            if nut[2][1] > 66.0:
                problems.append(f"bolt {side_name}: nut exceeds rail flange height")
        if side == 1:
            inner, outer = sorted(nuts, key=lambda r: r[1][0])
            if abs(inner[1][1] - 40.0) > 1e-6 or abs(outer[1][0] - 66.0) > 1e-6:
                problems.append(f"bolt {side_name}: nut faces must touch N 40 and N 66")
            if abs(shank[0][1][0] - 20.0) > 1e-6 or abs(shank[0][1][1] - 86.0) > 1e-6:
                problems.append(f"bolt {side_name}: shank must span N 20..86")
        else:
            inner, outer = sorted(nuts, key=lambda r: r[1][0], reverse=True)
            if abs(inner[1][1] - -40.0) > 1e-6 or abs(outer[1][1] - -66.0) > 1e-6:
                problems.append(f"bolt {side_name}: nut faces must touch N -40 and N -66")
            if abs(shank[0][1][0] - -86.0) > 1e-6 or abs(shank[0][1][1] - -40.0) > 1e-6:
                problems.append(f"bolt {side_name}: shank must span N -86..-40")

    return problems


if __name__ == "__main__":
    macro = candidate()
    problems = validate_pml(macro)
    if problems:
        raise SystemExit("PML validation failed:\n  " + "\n  ".join(problems))
    geometry_problems = verify_geometry(macro)
    if geometry_problems:
        raise SystemExit("Geometry verification failed:\n  " + "\n  ".join(geometry_problems))

    path = ROOT / "candidate" / "01_bolted_channel_frame.pml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(macro, encoding="utf-8", newline="\n")

    digest = hashlib.sha256(macro.encode("utf-8")).hexdigest().upper()
    count = len(parse_blocks(macro))
    print(f"candidate: {path}")
    print(f"SHA-256:   {digest}")
    print(f"primitives: {count} (EXTRUSION 21 / CYLINDER 9 / BOX 2)")
    print("PML1 validation: clean")
    print("geometry verification: clean (contacts, bounds, datums, lowest point)")
