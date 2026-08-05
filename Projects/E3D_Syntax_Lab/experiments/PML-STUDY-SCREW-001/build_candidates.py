"""Generate the refined screw/fastener certification candidate.

PML-STUDY-SCREW-001 tests one idea: a small fastener set where every head
form uses the primitive family that actually matches its geometry, instead of
defaulting every screw to one familiar element.

All forms used here are individually VERIFIED in E3D Design Mk3.1.11.0:

* EXTRUSION / LOOP / VERTEX for true hexagonal heads - PML-STUDY-EXTR-001/01-04
* CYLINDER, CONE, DISH and BOX primitives - production tank/pump macros

The assembly itself is new and awaits a user E3D verdict. Nothing in this
script is promoted to the shared skill until the candidate is certified.
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


HEX_PROFILE = (
    (-20.0, 0.0),
    (-10.0, 17.320508),
    (10.0, 17.320508),
    (20.0, 0.0),
    (10.0, -17.320508),
    (-10.0, -17.320508),
)


def cylinder(diameter: float, height: float, bottom: Tuple[float, float, float]) -> str:
    """Solid cylinder, bottom-face datum, ORI before POS (IR-1/IR-2)."""
    east, north, up = bottom
    return "\n".join(
        (
            "NEW CYLINDER",
            f"DIAM {fmt(diameter)}mm",
            f"HEIG {fmt(height)}mm",
            "ORI Z IS U AND Y IS N",
            f"POS E {fmt(east)}mm N {fmt(north)}mm U {fmt(up + height / 2)}mm",
            "END",
        )
    )


def cone(d_top: float, d_bottom: float, height: float, bottom: Tuple[float, float, float]) -> str:
    """Frustum, bottom-face datum, DTOP at the local +Z end (top)."""
    east, north, up = bottom
    return "\n".join(
        (
            "NEW CONE",
            f"DTOP {fmt(d_top)}mm",
            f"DBOT {fmt(d_bottom)}mm",
            f"HEIG {fmt(height)}mm",
            "ORI Z IS U AND Y IS N",
            f"POS E {fmt(east)}mm N {fmt(north)}mm U {fmt(up + height / 2)}mm",
            "END",
        )
    )


def dish(diameter: float, height: float, radius: float, rim: Tuple[float, float, float]) -> str:
    """Dished head positioned by its rim plane (IR-1); apex at rim + HEIG."""
    east, north, up = rim
    return "\n".join(
        (
            "NEW DISH",
            f"DIAM {fmt(diameter)}mm",
            f"HEIG {fmt(height)}mm",
            f"RADIUS {fmt(radius)}mm",
            "ORI Z IS U AND Y IS N",
            f"POS E {fmt(east)}mm N {fmt(north)}mm U {fmt(up)}mm",
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


def thread_ridges(diameter: float, height: float, pitch: float, bottom: Tuple[float, float, float], count: int) -> str:
    """Additive thread detail: thin CYLINDER ridges on a root cylinder.

    Each ridge is a full disc of the major diameter; the root cylinder below
    it carries the minor diameter, so the union is a threaded solid shaft.
    Every ridge overlaps the root cylinder, which keeps the assembly connected
    (IR-9b: no detached geometry).
    """
    east, north, up = bottom
    blocks = []
    for index in range(count):
        ridge_bottom = (east, north, up + index * pitch)
        blocks.append(cylinder(diameter, height, ridge_bottom))
    return "\n".join(blocks)


def hex_bolt(east: float) -> str:
    """M20-style hex head bolt: EXTRUSION head, CONE chamfers, CYLINDER body."""
    head = build_extrusion(
        (east, 0.0, 0.0), "Y IS N AND Z IS U", 20.0, HEX_PROFILE, level=(5, 10)
    ).rstrip()
    parts = [
        head,
        cone(24.0, 20.0, 4.0, (east, 0.0, 20.0)),
        cylinder(20.0, 30.0, (east, 0.0, 24.0)),
        cylinder(17.5, 40.0, (east, 0.0, 54.0)),
        thread_ridges(20.0, 1.2, 2.5, (east, 0.0, 54.0), 16),
        cone(17.5, 7.5, 5.0, (east, 0.0, 94.0)),
    ]
    return "\n".join(parts)


def button_screw(east: float) -> str:
    """M10-style button head screw: DISH dome, CYLINDER body, CONE tip."""
    parts = [
        dish(24.0, 6.0, 36.0, (east, 0.0, 0.0)),
        cylinder(10.0, 35.0, (east, 0.0, 6.0)),
        cylinder(8.5, 30.0, (east, 0.0, 41.0)),
        thread_ridges(10.0, 0.8, 1.5, (east, 0.0, 41.0), 12),
        cone(8.5, 3.5, 4.0, (east, 0.0, 71.0)),
    ]
    return "\n".join(parts)


def square_bolt(east: float) -> str:
    """M16-style square head bolt: BOX head, CYLINDER body, CONE tip."""
    parts = [
        box(28.0, 28.0, 14.0, (east, 0.0, 7.0)),
        cone(22.0, 16.0, 3.0, (east, 0.0, 14.0)),
        cylinder(16.0, 40.0, (east, 0.0, 17.0)),
        cylinder(13.5, 35.0, (east, 0.0, 57.0)),
        thread_ridges(16.0, 1.0, 2.0, (east, 0.0, 57.0), 14),
        cone(13.5, 5.5, 4.0, (east, 0.0, 92.0)),
    ]
    return "\n".join(parts)


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
    screws = (
        ("CODEX_SCREW_001_HEX_BOLT", hex_bolt(-150.0)),
        ("CODEX_SCREW_001_BUTTON_SCREW", button_screw(0.0)),
        ("CODEX_SCREW_001_SQUARE_BOLT", square_bolt(150.0)),
    )
    body = "\n".join(
        f"NEW SUBEQUIPMENT /{name}\n{macro}\nEND" for name, macro in screws
    )
    return wrap(
        "CODEX_SCREW_001",
        body,
        "REFINED FASTENER SET - PRIMITIVE SELECTION STUDY",
    )


# --------------------------------------------------------------------------
# Numerical verification - property checks on the emitted text, not the spec
# list above. The parser re-derives every primitive's occupied range from its
# element-specific datum, then checks contacts, bounds and lowest points.
# --------------------------------------------------------------------------

_NEW = re.compile(r"^NEW\s+(CYLINDER|CONE|DISH|BOX|EXTRUSION)\b", re.I)
_SUBE = re.compile(r"^NEW\s+SUBEQUIPMENT\s+(/\S+)", re.I)
_ATTR = re.compile(r"^(DIAM|HEIG|DTOP|DBOT|RADIUS|XLEN|YLEN|ZLEN|POS|ORI)\s+(.*)$", re.I)


def _numbers(text: str) -> List[float]:
    return [float(m) for m in re.findall(r"[-+]?\d+(?:\.\d+)?", text)]


def parse_blocks(macro: str) -> List[Dict]:
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
            block = {"type": new_match.group(1).upper(), "sube": sube, "attrs": {}, "order": []}
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
            # VERTEX positions are LOOP-local profile points, not EXTRUSION
            # attributes; they must never overwrite the block's own POS.
            continue
        attr_match = _ATTR.match(line)
        if attr_match and not line.startswith("NEW "):
            key = attr_match.group(1).upper()
            values = _numbers(attr_match.group(2))
            block["attrs"][key] = values
            block["order"].append(key)
    return blocks


def _pos(block: Dict) -> Tuple[float, float, float]:
    e, n, u = block["attrs"].get("POS", [0.0, 0.0, 0.0])
    return float(e), float(n), float(u)


def occupied_u(block: Dict) -> Tuple[float, float]:
    """Occupied U range from the element-specific POS datum (IR-1)."""
    _, _, pos_u = _pos(block)
    kind = block["type"]
    attrs = block["attrs"]
    if kind in ("CYLINDER", "CONE"):
        half = float(attrs["HEIG"][0]) / 2.0
        return pos_u - half, pos_u + half
    if kind == "BOX":
        half = float(attrs["ZLEN"][0]) / 2.0
        return pos_u - half, pos_u + half
    if kind == "DISH":
        return pos_u, pos_u + float(attrs["HEIG"][0])
    if kind == "EXTRUSION":
        return pos_u, pos_u + float(attrs["HEIG"][0])
    raise AssertionError(f"unhandled primitive {kind}")


def verify_geometry(macro: str) -> List[str]:
    """Return a list of geometry problems; empty means the model is coherent."""
    problems: List[str] = []
    blocks = parse_blocks(macro)
    if not blocks:
        return ["no primitive blocks parsed"]

    by_sube: Dict[str, List[Dict]] = {}
    for block in blocks:
        by_sube.setdefault(block["sube"], []).append(block)

    expected_offsets = {
        "/CODEX_SCREW_001_HEX_BOLT": -150.0,
        "/CODEX_SCREW_001_BUTTON_SCREW": 0.0,
        "/CODEX_SCREW_001_SQUARE_BOLT": 150.0,
    }
    expected_heads = {
        "/CODEX_SCREW_001_HEX_BOLT": "EXTRUSION",
        "/CODEX_SCREW_001_BUTTON_SCREW": "DISH",
        "/CODEX_SCREW_001_SQUARE_BOLT": "BOX",
    }
    # Structural part index of the thread-root cylinder within each screw's
    # block list; everything after it (except the final tip cone) is a ridge.
    root_index = {
        "/CODEX_SCREW_001_HEX_BOLT": 3,
        "/CODEX_SCREW_001_BUTTON_SCREW": 2,
        "/CODEX_SCREW_001_SQUARE_BOLT": 3,
    }

    def is_thread_ridge(block: Dict) -> bool:
        return block["type"] == "CYLINDER" and float(block["attrs"]["HEIG"][0]) <= 1.2

    for sube, expected_e in expected_offsets.items():
        parts = by_sube.get(sube)
        if not parts:
            problems.append(f"{sube}: no primitives found")
            continue
        if parts[0]["type"] != expected_heads[sube]:
            problems.append(f"{sube}: first part is {parts[0]['type']}, expected {expected_heads[sube]}")

        lowest, highest = min(occupied_u(p)[0] for p in parts), max(occupied_u(p)[1] for p in parts)
        if abs(lowest) > 1e-6:
            problems.append(f"{sube}: lowest point U {lowest:.3f} - nothing may sit below U 0")
        if not 50.0 <= highest <= 150.0:
            problems.append(f"{sube}: total length {highest:.3f} outside 50..150 mm")

        for block in parts:
            e, n, u = _pos(block)
            if abs(e - expected_e) > 1e-6 or abs(n) > 1e-6:
                problems.append(f"{sube}: {block['type']} POS E {e} N {n} off the screw axis")
            if not all(math.isfinite(v) for v in (e, n, u)):
                problems.append(f"{sube}: non-finite POS")
            attrs = block["attrs"]
            for key in ("DIAM", "HEIG", "DTOP", "DBOT", "RADIUS", "XLEN", "YLEN", "ZLEN"):
                if key in attrs and any(not math.isfinite(v) or v <= 0 for v in attrs[key]):
                    problems.append(f"{sube}: {block['type']} has non-positive {key}")

            order = block["order"]
            if block["type"] in ("CYLINDER", "CONE", "DISH"):
                if "ORI" not in order or "POS" not in order or order.index("POS") < order.index("ORI"):
                    problems.append(f"{sube}: {block['type']} violates ORI-before-POS")
            elif block["type"] == "BOX" and "ORI" in order and order.index("POS") < order.index("ORI"):
                problems.append(f"{sube}: BOX violates ORI-before-POS")

        # Contact chain: every adjacent structural part's faces must meet
        # exactly. Thread ridges overlap the root cylinder and are checked
        # separately below.
        structural = [p for p in parts if not is_thread_ridge(p)]
        ranges = [occupied_u(p) for p in structural]
        for previous, current in zip(ranges, ranges[1:]):
            if abs(previous[1] - current[0]) > 1e-6:
                problems.append(
                    f"{sube}: gap or overlap between faces {previous[1]:.3f} and {current[0]:.3f}"
                )

        # Thread ridges must sit fully inside the thread-root cylinder.
        root_min, root_max = occupied_u(parts[root_index[sube]])
        ridges = [p for p in parts if is_thread_ridge(p)]
        if ridges:
            for ridge in ridges:
                ridge_min, ridge_max = occupied_u(ridge)
                if ridge_min < root_min - 1e-6 or ridge_max > root_max + 1e-6:
                    problems.append(f"{sube}: thread ridge {ridge_min:.3f}..{ridge_max:.3f} escapes root {root_min:.3f}..{root_max:.3f}")

    return problems


if __name__ == "__main__":
    macro = candidate()
    problems = validate_pml(macro)
    if problems:
        raise SystemExit("PML validation failed:\n  " + "\n  ".join(problems))
    geometry_problems = verify_geometry(macro)
    if geometry_problems:
        raise SystemExit("Geometry verification failed:\n  " + "\n  ".join(geometry_problems))

    path = ROOT / "candidate" / "01_refined_screw_set.pml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(macro, encoding="utf-8", newline="\n")

    digest = hashlib.sha256(macro.encode("utf-8")).hexdigest().upper()
    count = len(parse_blocks(macro))
    print(f"candidate: {path}")
    print(f"SHA-256:   {digest}")
    print(f"primitives: {count} (hex 21 / button 16 / square 19)")
    print("PML1 validation: clean")
    print("geometry verification: clean (contacts, bounds, datums, lowest point)")
