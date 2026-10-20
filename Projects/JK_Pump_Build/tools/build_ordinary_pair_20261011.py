"""Adapt the latest archived ordinary-pump template to two requested skids.

Run from the repository root. No E3D session is accessed or modified.
"""

from __future__ import annotations

import copy
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

from wsb.pml_builder import NOZZLE_BORE_COMPONENTS, validate_pml
from wsb.pml_parser import NativeNode, native_orientation_basis, parse_native_tree
from base_deform import profile_centre
from extract_project_data import parse_pos

PROJECT = REPO / "Projects" / "JK_Pump_Build"
SOURCE = PROJECT / "imports" / "2026-09-10_TEM.txt"
OUTPUT = PROJECT / "output" / "2026-10-11_ordinary_pair"
SOURCE_TAG = "204_PU_006"
TAGS = ("203_PU_010", "204_PU_022")
SOURCE_DATUM = (20000.05, 17410.0, 0.0)
LENGTH, WIDTH, THICKNESS = 1724.0, 760.0, 50.0
STAGING_N = 1520.0
POSITIVE = {"BOX", "CYLINDER", "CONE", "DISH", "PYRAMID", "EXTRUSION", "CTORUS"}
DIMENSIONS = {"XLEN", "YLEN", "ZLEN", "DIAM", "HEIG", "DTOP", "DBOT",
              "XBOT", "YBOT", "XTOP", "YTOP", "RINS", "ROUT", "RADI"}


def number(node: NativeNode, key: str) -> float:
    value = node.get(key)
    if value is None:
        raise ValueError(f"{node.kind} has no {key}")
    return float(re.sub(r"(?:mm|degree)$", "", value, flags=re.I))


def position(node: NativeNode) -> tuple[float, float, float]:
    value = parse_pos("POS " + node.get("POS", "E 0mm N 0mm U 0mm"))
    if value is None:
        raise ValueError(f"Unrecognised {node.kind} position")
    return tuple(value[key] for key in ("east", "north", "up"))


def fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".") if abs(value) >= 0.0005 else "0"


def pos_text(point) -> str:
    return " ".join(f"{positive if value >= 0 else negative} {fmt(abs(value))}mm"
                    for value, positive, negative in zip(point, "ENU", "WSD"))


def source_tree() -> NativeNode:
    text = SOURCE.read_text(encoding="utf-8-sig")
    start = text.index(f"NEW EQUIPMENT /{SOURCE_TAG}")
    stop = text.index("OLD NOZZLE", start)
    roots = parse_native_tree(text[start:stop])
    assert len(roots) == 1 and roots[0].name == f"/{SOURCE_TAG}"
    bindings = dict(re.findall(r"OLD NOZZLE\s+(/\S+)\s+CATR SPCOMPONENT\s+(/\S+)", text[stop:]))
    for node in roots[0].walk():
        if node.kind == "NOZZLE":
            node.set("CATR", "SPCOMPONENT " + bindings[node.name])
    return roots[0]


def adapt(source: NativeNode, tag: str, staging_n: float = 0.0) -> NativeNode:
    root = copy.deepcopy(source)
    for node in root.walk():
        if node.name:
            node.name = node.name.replace(SOURCE_TAG, tag)
    root.set("DESC", "'Ordinary process pump - native template adaptation'")
    root.attributes = [(key, value) for key, value in root.attributes if key != "FUNC"]
    root.set("POS", "E 0mm N 0mm U 0mm")
    for sube in root.children:
        assert sube.kind == "SUBEQUIPMENT" and sube.get("POS") is None
        for node in sube.children:
            assert node.kind in POSITIVE | {"NOZZLE", "ELCONN"}
            e, n, u = position(node)
            node.set("POS", pos_text((e - SOURCE_DATUM[0], n - SOURCE_DATUM[1] + staging_n, u)))
            if sube.name.endswith("_BASE") and node.kind == "BOX" and node.get("YLEN") == "1725.1mm":
                node.set("YLEN", f"{fmt(LENGTH)}mm")
                if node.get("XLEN") == "447.12mm":
                    node.set("XLEN", f"{fmt(WIDTH)}mm")
                else:
                    # The native outer rail envelope is 760.09 mm. Move only
                    # these four skid rails inward by 0.045 mm on each side.
                    e, n, u = position(node)
                    rail_n = math.copysign(WIDTH / 2 - number(node, "XLEN") / 2, n - staging_n)
                    half_height = number(node, "ZLEN") / 2
                    u = half_height if u < THICKNESS / 2 else THICKNESS - half_height
                    node.set("POS", pos_text((e, rail_n + staging_n, u)))
            if node.kind == "NOZZLE":
                node.set("ORI", "P1 IS " + ("E" if "SUCTION" in node.name else "U"))
            if sube.name.endswith("_DRIVER") and node.kind == "BOX" and node.get("ZLEN") == "-5.25mm":
                # Source defect: retain the native centre and absolute span.
                # This is a documented Reference Value repair, not vendor data.
                node.set("ZLEN", "5.25mm")
            for child in node.walk():
                if child.kind in {"NCONE", "NCYLINDER"}:
                    child.set("NAPPFLAG", "2")
    return root


def emit(node: NativeNode) -> list[str]:
    lines = [f"NEW {node.kind}" + (f" {node.name}" if node.name else "")]
    attrs = dict(node.attributes)
    if node.kind == "NOZZLE":
        order = ["CATR", "POS", "ORI"]
    else:
        order = [key for key in attrs if key not in {"ORI", "POS"}] + ["ORI", "POS"]
    order += [key for key in attrs if key not in order]
    lines.extend(f"{key} {attrs[key]}" for key in order if key in attrs)
    for child in node.children:
        lines.append("")
        lines.extend(emit(child))
    lines.append("END")
    return lines


def macro(roots: list[NativeNode], combined: bool = False) -> str:
    header = ["-- JK_Pump_Build - ordinary pump pair - 2026-10-11",
              "-- User baseplate: L 1724mm, W 760mm; thickness 50mm from project.",
              "-- Reference Value: remaining geometry and DN100/DN150 from native TEM, 2026-09-10.",
              "-- Reference Value: native main axis +E; installation coordinates/orientation TBC.",
              "-- Source repair / Reference Value: one DRIVER BOX ZLEN -5.25mm -> +5.25mm; centre retained.",
              "-- Skid rail faces seated exactly at U=0 and U=50; native rounding corrected by 0.005mm.",
              "-- Equipment origin is zero; geometry is referenced to baseplate underside centre."]
    if combined:
        header += ["-- REVIEW LAYOUT ONLY: 203-PU-010 at (0,0,0); 204-PU-022 at (0,1520,0) mm.",
                   "-- The 760mm clear gap is a Reference Value, not plant installation data."]
    else:
        header += ["-- Local baseplate underside centre: (0,0,0) mm; position after import."]
    return "\n".join(header + [line for root in roots for line in emit(root)]) + "\n"


def bounds(node: NativeNode) -> tuple[float, ...]:
    p = position(node)
    basis = native_orientation_basis(node.get("ORI"))
    points = []

    def add(local):
        points.append(tuple(p[i] + sum(basis[axis][i] * value
                                      for axis, value in zip("XYZ", local)) for i in range(3)))

    kind = node.kind
    if kind == "BOX":
        half = [number(node, key) / 2 for key in ("XLEN", "YLEN", "ZLEN")]
        for x in (-half[0], half[0]):
            for y in (-half[1], half[1]):
                for z in (-half[2], half[2]):
                    add((x, y, z))
    elif kind == "PYRAMID":
        height = number(node, "HEIG")
        for xlen, ylen, cx, cy, z in (
            (number(node, "XBOT"), number(node, "YBOT"), 0, 0, -height / 2),
            (number(node, "XTOP"), number(node, "YTOP"), float(node.get("XOFF", "0mm")[:-2]),
             float(node.get("YOFF", "0mm")[:-2]), height / 2),
        ):
            for x in (-xlen / 2, xlen / 2):
                for y in (-ylen / 2, ylen / 2):
                    add((cx + x, cy + y, z))
    elif kind == "EXTRUSION":
        loops = [child for child in node.children if child.kind == "LOOP"]
        assert len(loops) == 1 and len(loops[0].children) >= 4
        for vertex in loops[0].children:
            x, y, z = position(vertex)
            for offset in (0.0, number(node, "HEIG")):
                add((x, y, z + offset))
    else:
        if kind == "CTORUS":
            assert 0 < number(node, "RINS") < number(node, "ROUT")
            assert 0 < number(node, "ANGL") <= 180
            # Bound the actual arc, not an unused full circle. Each world
            # coordinate has extrema at arc endpoints or atan2(B,A) + k*pi.
            major = (number(node, "ROUT") + number(node, "RINS")) / 2
            tube = (number(node, "ROUT") - number(node, "RINS")) / 2
            end = math.radians(number(node, "ANGL"))
            result = []
            for i in range(3):
                a, b = basis["X"][i], basis["Y"][i]
                candidates = [0.0, end]
                for k in (-2, -1, 0, 1, 2):
                    angle = math.atan2(b, a) + k * math.pi
                    if 0 <= angle <= end:
                        candidates.append(angle)
                values = [p[i] + major * (a * math.cos(t) + b * math.sin(t)) for t in candidates]
                result.extend((min(values) - tube, max(values) + tube))
            return tuple(result)
        else:
            r = (number(node, "DIAM") if kind != "CONE" else max(number(node, "DBOT"), number(node, "DTOP"))) / 2
            h = number(node, "HEIG")
            lows, highs = (-r, -r, 0 if kind == "DISH" else -h / 2), (r, r, h if kind == "DISH" else h / 2)
        for x in (lows[0], highs[0]):
            for y in (lows[1], highs[1]):
                for z in (lows[2], highs[2]):
                    add((x, y, z))
    return tuple(value for i in range(3) for value in (min(p[i] for p in points), max(p[i] for p in points)))


def verify(source: NativeNode, root: NativeNode, staging_n: float) -> dict:
    before, after = list(source.walk()), list(root.walk())
    assert Counter(n.kind for n in before) == Counter(n.kind for n in after)
    assert len(after) == 196, "Native inventory changed; review the template before adapting"
    assert position(root) == (0.0, 0.0, 0.0)
    # Preserve every dimension, native local ORI/profile, and child position,
    # except the five explicitly adapted full-length skid members.
    base_source = next(n for n in source.children if n.name.endswith("_BASE"))
    skid_ids = {id(n) for n in base_source.children if n.kind == "BOX" and n.get("YLEN") == "1725.1mm"}
    direct_ids = {id(n) for sube in source.children for n in sube.children}
    for a, b in zip(before, after):
        assert a.kind == b.kind and len(a.children) == len(b.children)
        for key in DIMENSIONS | {"ANGL"}:
            if id(a) in skid_ids and key in {"XLEN", "YLEN"}:
                continue
            if a.kind == "BOX" and key == "ZLEN" and a.get(key) == "-5.25mm":
                assert b.get(key) == "5.25mm"
                continue
            assert a.get(key) == b.get(key), (a.kind, key, a.get(key), b.get(key))
        if a.kind != "NOZZLE":
            assert a.get("ORI") == b.get("ORI"), (a.kind, "native local axes changed")
        if id(a) in direct_ids:
            expected = (position(a)[0] - SOURCE_DATUM[0], position(a)[1] - SOURCE_DATUM[1] + staging_n, position(a)[2])
            if id(a) in skid_ids and a.get("XLEN") == "156.49mm":
                u = 8.335 if expected[2] < 25 else 41.665
                expected = (expected[0], math.copysign(301.755, expected[1] - staging_n) + staging_n, u)
            assert max(abs(x - y) for x, y in zip(expected, position(b))) < 0.0006
        elif a.kind not in {"EQUIPMENT"}:
            assert a.get("POS") == b.get("POS"), (a.kind, "local child moved")
        if a.kind == "NOZZLE":
            assert a.get("CATR") == b.get("CATR") and a.get("HEIG") == b.get("HEIG")
        if b.kind in {"NCONE", "NCYLINDER"}:
            assert b.get("NAPPFLAG") == "2" and b.get("POS") is None and b.get("ORI") is None
    solids = [n for n in after if n.kind in POSITIVE]
    assert len(solids) == 104
    for node in solids:
        for key in DIMENSIONS - {"RADI"}:
            if node.get(key) is not None:
                assert number(node, key) > 0, (node.kind, key)
        if node.get("ORI") is not None:
            keys = [key for key, _ in node.attributes]
            assert keys.index("ORI") < keys.index("POS")
    boxes = [n for n in solids if n.kind == "BOX" and number(n, "ZLEN") == THICKNESS
             and number(n, "YLEN") == LENGTH and number(n, "XLEN") == WIDTH]
    assert len(boxes) == 1
    plate = bounds(boxes[0])
    assert max(abs(x - y) for x, y in zip(plate, (-862, 862, staging_n - 380, staging_n + 380, 0, 50))) < 1e-6
    occupied = [bounds(node) for node in solids]
    minimum = min(b[4] for b in occupied)
    assert minimum >= -1e-8, ("solid below foundation", minimum)
    assert all(b[0] >= -862 - 0.01 and b[1] <= 862 + 0.01
               and b[2] >= staging_n - 380 - 0.01 and b[3] <= staging_n + 380 + 0.01 for b in occupied)
    nozzles = [n for n in after if n.kind == "NOZZLE"]
    assert len(nozzles) == 2
    suction = next(n for n in nozzles if "SUCTION" in n.name)
    discharge = next(n for n in nozzles if "DISCHARGE" in n.name)
    assert suction.get("CATR").endswith(NOZZLE_BORE_COMPONENTS[100])
    assert discharge.get("CATR").endswith(NOZZLE_BORE_COMPONENTS[150])
    assert suction.get("ORI") == "P1 IS E" and discharge.get("ORI") == "P1 IS U"
    suction_root = position(suction)[0] - number(suction, "HEIG")
    casing = root.children[0]
    barrel = next(n for n in casing.children if n.kind == "CYLINDER")
    assert abs(suction_root - position(barrel)[0]) <= 0.1
    cone = next(n for n in casing.children if n.kind == "CONE")
    outlet_top = position(cone)[2] + number(cone, "HEIG") / 2
    discharge_gap = position(discharge)[2] - number(discharge, "HEIG") - outlet_top
    assert abs(discharge_gap) < 0.01
    base = next(n for n in root.children if n.name.endswith("_BASE"))
    bolts = [n for n in base.children if n.kind == "CYLINDER"]
    washers = [n for n in base.children if n.kind == "EXTRUSION"]
    assert len(bolts) == len(washers) == 10
    distances = []
    unused = bolts[:]
    for washer in washers:
        profile = [position(n)[:2] for n in washer.children[0].children]
        x, y = profile_centre(profile)
        axes = native_orientation_basis(washer.get("ORI"))
        centre = tuple(position(washer)[i] + axes["X"][i] * x + axes["Y"][i] * y for i in (0, 1))
        bolt = min(unused, key=lambda n: math.dist(position(n)[:2], centre))
        distances.append(math.dist(position(bolt)[:2], centre))
        unused.remove(bolt)
    assert max(distances) <= 0.02, ("hex/anchor axes", max(distances))
    return {"tag": root.name.lstrip("/").replace("_", "-"), "native_nodes": len(after),
            "positive_solids": len(solids), "negative_children": 2, "subequipment": 6,
            "nozzles": 2, "baseplate_bounds_mm": plate,
            "minimum_solid_elevation_mm": round(minimum, 6),
            "discharge_terminal_gap_mm": round(discharge_gap, 6),
            "maximum_anchor_hex_axis_offset_mm": round(max(distances), 6),
            "status": "Offline verification passed; native E3D loading and visual acceptance pending"}


def build() -> None:
    original = source_tree()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    products = []
    audits = []
    for tag in TAGS:
        text = macro([adapt(original, tag)])
        assert not validate_pml(text, native_templates=True), validate_pml(text, native_templates=True)
        path = OUTPUT / (tag.replace("_", "-") + ".pml")
        path.write_text(text, encoding="utf-8")
        reread = parse_native_tree(path.read_text(encoding="utf-8"))
        audits.append(verify(original, reread[0], 0.0))
        products.append(path)
    combined = OUTPUT / "JK_Pump_Build_203_PU_010_204_PU_022_20261011.pml"
    combined.write_text(macro([adapt(original, TAGS[0]), adapt(original, TAGS[1], STAGING_N)], True), encoding="utf-8")
    combined_text = combined.read_text(encoding="utf-8")
    assert not validate_pml(combined_text, native_templates=True), validate_pml(combined_text, native_templates=True)
    roots = parse_native_tree(combined_text)
    assert len(roots) == 2
    named = [n.name for root in roots for n in root.walk() if n.name]
    assert len(named) == len(set(named))
    assert SOURCE_TAG not in combined_text
    pair_audits = [verify(original, root, index * STAGING_N) for index, root in enumerate(roots)]
    products.append(combined)
    # Small mutations must be rejected by the same finished-output checker.
    mutations = {}
    for label in ("wrong_plate_width", "buried_gusset", "missing_native_solid", "missing_catalogue", "moved_local_hole"):
        candidate = copy.deepcopy(roots[0])
        base = next(n for n in candidate.children if n.name.endswith("_BASE"))
        if label == "wrong_plate_width":
            next(n for n in base.children if n.get("XLEN") == "760mm").set("XLEN", "750mm")
        elif label == "buried_gusset":
            next(n for n in base.children if n.kind == "PYRAMID").set("POS", "E 0mm N 0mm D 100mm")
        elif label == "missing_native_solid":
            candidate.children[0].children.pop(0)
        elif label == "missing_catalogue":
            next(n for n in candidate.walk() if n.kind == "NOZZLE").set("CATR", "SPCOMPONENT /invalid")
        else:
            next(n for n in candidate.walk() if n.kind == "NCONE").set("POS", "E 500mm N 0mm U 0mm")
        try:
            verify(original, candidate, 0.0)
        except (AssertionError, ValueError):
            mutations[label] = "rejected"
        else:
            raise AssertionError(f"Verifier accepted mutation: {label}")
    audit = {"template": str(SOURCE.relative_to(PROJECT)),
             "template_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
             "individual_macros": audits, "combined_review_layout": pair_audits,
             "verifier_mutations": mutations,
             "file_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in products}}
    (OUTPUT / "AUDIT.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))
    for path in products:
        print(path)


if __name__ == "__main__":
    build()
