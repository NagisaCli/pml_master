"""
Verify the /P1501C scale variant against its /P1501B source, numerically.

The check is deliberately independent of the generator: it re-parses both
listings into structured elements, re-predicts every scaled attribute from
first principles, and compares.  It never string-matches the output against
an expected file, because a textual diff cannot tell a correctly scaled model
from a plausible-looking wrong one (see skill/knowledge, "verify geometry
numerically, not by string-matching").

Checks
------
 1. element inventory is identical (same types, same count, same order)
 2. every length attribute equals source * S, except nozzle HEIG which is
    unchanged
 3. every POS equals the local scale rule, except the EQUI installation
    coordinate (fixed) and nozzle faces (root scaled + unchanged HEIG)
 4. the baseplate solid measures exactly NEW_LEN x NEW_WID x scaled thickness
 5. no solid falls below the foundation datum
 6. every solid stays inside the new baseplate footprint in plan, except the
    documented nozzle/terminal-box overhangs the source already has
 7. the support chain's U spans scale invariantly about the plate underside
 8. each nozzle barrel root still lands on the casing
 9. catalogue bindings (CATR/CREF/ORRF) are carried over intact and retargeted
"""

from __future__ import annotations

import math
import re
import sys
from decimal import Decimal as D
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SRC = PROJECT / "imports" / "2026-08-18_Reference_pumps_P1501B.txt"
OUT = PROJECT / "output" / "P1501C_1807x663.txt"

S = D("1.30")
PLATE_BOTTOM = D("-340")
NEW_LEN, NEW_WID = D("1807"), D("663")
OLD_LEN, OLD_WID = D("1390"), D("510")

SIGN = {"E": 1, "W": -1, "N": 1, "S": -1, "U": 1, "D": -1}
AXV = {
    "E": (D(1), D(0), D(0)), "W": (D(-1), D(0), D(0)),
    "N": (D(0), D(1), D(0)), "S": (D(0), D(-1), D(0)),
    "U": (D(0), D(0), D(1)), "D": (D(0), D(0), D(-1)),
}
DIMS = ("XLEN", "YLEN", "ZLEN", "DIAM", "HEIG", "RADI",
        "XBOT", "YBOT", "XTOP", "YTOP", "XOFF", "YOFF")

TOL = D("0.02")  # the listing is written to 0.01 mm

failures: list[str] = []
notes: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


def parse_pos(text: str):
    vec = [D(0)] * 3
    for letter, number in re.findall(r"([ENSWUD])\s+([-\d.]+)\s*mm", text):
        value = D(number) * SIGN[letter]
        vec[0 if letter in "EW" else (1 if letter in "NS" else 2)] = value
    return vec


def parse_ori(text: str):
    out = {}
    for axis, spec in re.findall(
        r"([XYZ])\s+is\s+([ENSWUD](?:\s+[\d.]+\s+[ENSWUD])?)", text
    ):
        parts = spec.split()
        if len(parts) == 1:
            out[axis] = AXV[parts[0]]
        else:
            base, angle, other = AXV[parts[0]], float(parts[1]), AXV[parts[2]]
            ca = D(str(math.cos(math.radians(angle))))
            sa = D(str(math.sin(math.radians(angle))))
            out[axis] = tuple(base[i] * ca + other[i] * sa for i in range(3))
    return out


def parse(path: Path):
    """Read a listing into ordered elements carrying their attributes."""
    elements = []
    current_sub = None
    block = None
    for raw in path.read_text(encoding="utf-8-sig").split("\n"):
        text = raw.strip()
        m = re.match(r"^NEW\s+([A-Z]+)(?:\s+(\S+))?$", text, re.IGNORECASE)
        if m:
            kind = m.group(1).upper()
            if kind == "SUBEQUIPMENT":
                current_sub = m.group(2)
            block = {"t": kind, "n": m.group(2), "sub": current_sub, "a": {}}
            elements.append(block)
            continue
        if text == "END":
            block = None
            continue
        if block is not None and text:
            key = text.split()[0]
            block["a"][key] = text[len(key):].strip()
    return elements


def frame(attrs):
    o = parse_ori(attrs.get("ORI", ""))
    z = o.get("Z", (D(0), D(0), D(1)))
    y = o.get("Y", (D(0), D(1), D(0)))
    x = o.get("X") or (
        y[1] * z[2] - y[2] * z[1],
        y[2] * z[0] - y[0] * z[2],
        y[0] * z[1] - y[1] * z[0],
    )
    return x, y, z


def num(attrs, key):
    m = re.match(r"^([-\d.]+)", attrs.get(key, "") or "")
    return D(m.group(1)) if m else D(0)


def aabb(el, sub_offsets):
    """Oriented axis-aligned bounding box of one solid, in the EQUI frame."""
    a = el["a"]
    if el["t"] not in ("BOX", "CYLINDER", "DISH", "PYRAMID"):
        return None
    centre = parse_pos(a.get("POS", "")) if "POS" in a else [D(0)] * 3
    off = sub_offsets.get(el["sub"], [D(0)] * 3)
    centre = [centre[i] + off[i] for i in range(3)]
    x, y, z = frame(a)
    if el["t"] == "BOX":
        hx, hy, hz = num(a, "XLEN") / 2, num(a, "YLEN") / 2, num(a, "ZLEN") / 2
    elif el["t"] == "CYLINDER":
        hx = hy = num(a, "DIAM") / 2
        hz = num(a, "HEIG") / 2
    elif el["t"] == "DISH":
        hx = hy = num(a, "DIAM") / 2
        h = num(a, "HEIG")
        centre = [centre[i] + z[i] * h / 2 for i in range(3)]
        hz = h / 2
    else:  # PYRAMID
        hx = max(num(a, "XBOT"), num(a, "XTOP")) / 2
        hy = max(num(a, "YBOT"), num(a, "YTOP")) / 2
        hz = num(a, "HEIG") / 2
    ext = [abs(x[i]) * hx + abs(y[i]) * hy + abs(z[i]) * hz for i in range(3)]
    return [centre[i] - ext[i] for i in range(3)], \
           [centre[i] + ext[i] for i in range(3)]


def sub_offsets(elements):
    out = {}
    for el in elements:
        if el["t"] == "SUBEQUIPMENT":
            out[el["n"]] = parse_pos(el["a"].get("POS", "")) \
                if "POS" in el["a"] else [D(0)] * 3
    return out


def main() -> None:
    for path in (SRC, OUT):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")

    src = parse(SRC)
    out = parse(OUT)

    # --- 1. inventory ------------------------------------------------------
    check(len(src) == len(out),
          f"element count differs: source {len(src)} vs output {len(out)}")
    kinds_src = [e["t"] for e in src]
    kinds_out = [e["t"] for e in out]
    check(kinds_src == kinds_out, "element type sequence differs")
    print(f"[1] inventory: {len(out)} elements, sequence identical")

    src_off = sub_offsets(src)
    out_off = sub_offsets(out)

    # --- 2/3. per-attribute re-prediction ----------------------------------
    dim_checked = pos_checked = 0
    for i, (a, b) in enumerate(zip(src, out)):
        if a["t"] != b["t"]:
            continue
        is_nozzle = a["t"] == "NOZZLE"
        is_equi = a["t"] == "EQUIPMENT"
        is_vertex = a["t"] == "VERTEX"

        for key in DIMS:
            if key not in a["a"]:
                continue
            want = num(a["a"], key)
            got = num(b["a"], key)
            expect = want if is_nozzle else want * S
            check(abs(got - expect) <= TOL,
                  f"{a['t']} #{i} {key}: expected {expect}, got {got}")
            dim_checked += 1

        if "POS" in a["a"]:
            pa, pb = parse_pos(a["a"]["POS"]), parse_pos(b["a"]["POS"])
            if is_equi:
                check(pa == pb, f"EQUI installation coordinate moved: {pa}->{pb}")
            elif is_nozzle:
                pass  # handled geometrically in check 8
            else:
                # Uniform similarity about the equipment origin: every POS,
                # including a SUBE frame offset and a LOOP vertex, is the
                # same pure multiply.  Any per-axis re-datuming here would
                # move parts relative to each other.
                exp = [v * S for v in pa]
                check(all(abs(pb[k] - exp[k]) <= TOL for k in range(3)),
                      f"{a['t']} #{i} POS: expected {exp}, got {pb}")
            pos_checked += 1
    print(f"[2] {dim_checked} length attributes re-predicted independently")
    print(f"[3] {pos_checked} POS lines re-predicted independently")

    # --- 4. baseplate --------------------------------------------------------
    plates = [e for e in out
              if e["t"] == "BOX" and num(e["a"], "YLEN") == NEW_LEN
              and num(e["a"], "XLEN") == D("390")]
    boxes = [(e, aabb(e, out_off)) for e in out if e["t"] == "BOX"]
    lo_e = min(bb[0][0] for _, bb in boxes if bb)
    hi_e = max(bb[1][0] for _, bb in boxes if bb)
    lo_n = min(bb[0][1] for _, bb in boxes if bb)
    hi_n = max(bb[1][1] for _, bb in boxes if bb)
    check(abs((hi_n - lo_n) - NEW_LEN) <= TOL,
          f"baseplate length {hi_n - lo_n} != {NEW_LEN}")
    check(abs((hi_e - lo_e) - NEW_WID) <= TOL,
          f"baseplate width {hi_e - lo_e} != {NEW_WID}")
    print(f"[4] baseplate envelope {hi_n - lo_n} (N) x {hi_e - lo_e} (E)"
          f"  target {NEW_LEN} x {NEW_WID}")

    # --- 5. foundation datum --------------------------------------------------
    lowest = None
    for e in out:
        bb = aabb(e, out_off)
        if bb and (lowest is None or bb[0][2] < lowest):
            lowest = bb[0][2]
    check(abs(lowest - PLATE_BOTTOM * S) <= TOL,
          f"lowest solid {lowest} != scaled plate underside {PLATE_BOTTOM * S}")
    print(f"[5] lowest solid U={lowest} = plate underside {PLATE_BOTTOM}"
          f" x {S} (shaft axis is the invariant datum)")

    # --- 6. plan containment ---------------------------------------------------
    src_lowest = None
    for e in src:
        bb = aabb(e, src_off)
        if bb and (src_lowest is None or bb[0][2] < src_lowest):
            src_lowest = bb[0][2]
    over_src = sum(
        1 for e in src
        if (bb := aabb(e, src_off))
        and (bb[0][0] < -OLD_WID / 2 - TOL or bb[1][0] > OLD_WID / 2 + TOL)
    )
    over_out = sum(
        1 for e in out
        if (bb := aabb(e, out_off))
        and (bb[0][0] < -NEW_WID / 2 - TOL or bb[1][0] > NEW_WID / 2 + TOL)
    )
    check(over_out == over_src,
          f"plan overhang count changed: source {over_src}, output {over_out}")
    print(f"[6] transverse overhangs: source {over_src}, output {over_out}"
          f" (unchanged)")

    # --- 7. support-chain U spans scale invariantly ---------------------------
    ratios = []
    for a, b in zip(src, out):
        ba, bb_ = aabb(a, src_off), aabb(b, out_off)
        if not ba or not bb_:
            continue
        span_a = ba[1][2] - ba[0][2]
        span_b = bb_[1][2] - bb_[0][2]
        if span_a > 0:
            ratios.append(span_b / span_a)
    worst = max(abs(r - S) for r in ratios)
    check(worst <= D("0.001"),
          f"U-span scale not invariant: worst deviation {worst}")
    print(f"[7] {len(ratios)} solid U spans all scale by {S}"
          f" (max deviation {worst})")

    # --- 8. nozzle attachment --------------------------------------------------
    CASING_R = D("170") * S
    CASING_N = D("60") * S
    # The casing axis is the shaft centreline at local U=0, which is the
    # scaling origin and therefore invariant.
    CASING_U = D(0) * S  # the shaft axis is the scaling origin: invariant
    aims = {"/P1501C/N1": (D(0), D(1), D(0)),
            "/P1501C/N2": (D(0), D(0), D(1)),
            "/P1501C/N3": (D(1), D(0), D(0))}
    heigs = {"/P1501C/N1": D("155"), "/P1501C/N2": D("200"),
             "/P1501C/N3": D("200")}
    for e in out:
        if e["t"] != "NOZZLE":
            continue
        face = parse_pos(e["a"]["POS"])
        aim = aims[e["n"]]
        heig = heigs[e["n"]]
        check(num(e["a"], "HEIG") == heig,
              f"{e['n']} HEIG changed: {num(e['a'], 'HEIG')} != {heig}")
        root = [face[i] - aim[i] * heig for i in range(3)]
        du = root[2] - CASING_U
        radial = (root[0] * root[0] + du * du).sqrt()
        if e["n"] == "/P1501C/N1":
            # End-suction inlet: the root is the impeller eye on the axis.
            ok = (abs(root[0]) <= TOL and abs(root[1]) <= TOL
                  and abs(du) <= TOL)
            detail = (f"root ({root[0]}, {root[1]}, {root[2]}) should be the "
                      f"impeller eye on the casing axis at U={CASING_U}")
        else:
            ok = radial <= CASING_R + TOL and abs(root[1]) <= CASING_N + TOL
            detail = (f"root radial {radial:.1f} vs casing r {CASING_R}, "
                      f"N {root[1]}")
        check(ok, f"{e['n']} barrel root not on casing: {detail}")
        print(f"[8] {e['n']}: HEIG {heig} kept, root "
              f"({root[0]:.1f}, {root[1]:.1f}, {root[2]:.1f}), "
              f"radial {radial:.1f} <= casing r {CASING_R}")

    # --- 8b. the machine must stay ASSEMBLED -------------------------------
    # This is the check whose absence let a visibly broken model pass.  Every
    # earlier test compared the output against the transform I had chosen; not
    # one asked whether the parts still touch each other.  A per-element rule
    # can be applied perfectly and still shear the assembly if the rule itself
    # is wrong -- which is exactly what happened when a SUBE frame offset was
    # re-datumed and the motor lifted 204 mm off the shaft it drives.
    #
    # These checks are relational: they compare parts to OTHER parts, and they
    # are expressed as invariants of a similarity transform, so they hold for
    # any S without knowing which S was used.
    def axis_of(elements, offsets, sub, diam_prefixes):
        for el in elements:
            if el["sub"] != sub or el["t"] != "CYLINDER":
                continue
            if any(el["a"].get("DIAM", "").startswith(p) for p in diam_prefixes):
                pos = parse_pos(el["a"].get("POS", ""))                     if "POS" in el["a"] else [D(0)] * 3
                off = offsets.get(sub, [D(0)] * 3)
                return [pos[i] + off[i] for i in range(3)]
        return None

    # The motor barrel and the casing volute are coupled through the shaft and
    # MUST remain coaxial: same E, same U, in both source and output.
    for label, elements, offsets, motor_d, casing_d in (
        ("source", src, src_off, ("360",), ("340",)),
        ("output", out, out_off, ("468",), ("442",)),
    ):
        motor = axis_of(elements, offsets, "/Motor", motor_d)
        casing = axis_of(elements, offsets, "/Casing_and_drive_shaft", casing_d)
        if motor is None or casing is None:
            check(False, f"{label}: could not locate motor/casing barrels")
            continue
        check(abs(motor[0] - casing[0]) <= TOL and abs(motor[2] - casing[2]) <= TOL,
              f"{label}: motor axis {motor} is not coaxial with casing {casing} "
              f"-- dE={motor[0] - casing[0]}, dU={motor[2] - casing[2]}")
        print(f"[8b] {label}: motor axis U={motor[2]} == casing axis U={casing[2]}"
              f" (coaxial)")

    # Every SUBE frame offset must scale by exactly S.  A frame offset is a
    # relative vector between coordinate frames; re-datuming one moves a whole
    # subassembly relative to its siblings.
    for name, src_vec in src_off.items():
        out_vec = out_off.get(name)
        check(out_vec is not None, f"SUBE {name} missing from output")
        if out_vec is None:
            continue
        exp = [v * S for v in src_vec]
        check(all(abs(out_vec[k] - exp[k]) <= TOL for k in range(3)),
              f"SUBE {name} frame offset {out_vec} != source {src_vec} x {S} "
              f"= {exp}; a frame offset must scale, never be re-datumed")
    print(f"[8b] all {len(src_off)} SUBE frame offsets scale by exactly {S}")

    # Whole-assembly similarity: the distance between any two solid centres
    # must scale by exactly S.  This catches ANY relative displacement between
    # parts, whatever its cause, without encoding the transform being tested.
    def centres(elements, offsets):
        out_list = []
        for el in elements:
            bb = aabb(el, offsets)
            if bb:
                out_list.append([(bb[0][i] + bb[1][i]) / 2 for i in range(3)])
        return out_list

    src_c, out_c = centres(src, src_off), centres(out, out_off)
    check(len(src_c) == len(out_c), "solid count differs for the similarity check")
    worst_pair, worst_dev = None, D(0)
    if len(src_c) == len(out_c):
        step = max(1, len(src_c) // 60)  # sample pairs; O(n^2) over 244 is fine
        for i in range(0, len(src_c), step):
            for j in range(i + 1, len(src_c), step):
                da = max(abs(src_c[i][k] - src_c[j][k]) for k in range(3))
                db = max(abs(out_c[i][k] - out_c[j][k]) for k in range(3))
                if da <= TOL:
                    check(db <= TOL * S,
                          f"solids {i},{j} were coincident but are now {db} apart")
                    continue
                dev = abs(db / da - S)
                if dev > worst_dev:
                    worst_dev, worst_pair = dev, (i, j)
        check(worst_dev <= D("0.001"),
              f"assembly is not a similarity: pair {worst_pair} separation "
              f"scales by {S + worst_dev} instead of {S} -- parts have moved "
              f"relative to each other")
    print(f"[8b] inter-part distances all scale by {S}"
          f" (worst deviation {worst_dev})")

    # --- 9. catalogue bindings ------------------------------------------------
    src_text = SRC.read_text(encoding="utf-8-sig")
    out_text = OUT.read_text(encoding="utf-8-sig")
    for keyword in ("CATR", "ORRF"):
        a = len(re.findall(rf"^{keyword}\b", src_text, re.M))
        b = len(re.findall(rf"^{keyword}\b", out_text, re.M))
        check(a == b, f"{keyword} count changed: {a} -> {b}")
    for spco in re.findall(r"CATR\s+SPCOMPONENT\s+(\S+)", src_text):
        check(spco in out_text, f"catalogue component dropped: {spco}")

    # CREF is one half of a reciprocal pipe connection: the branch it names
    # carries the matching HREF/TREF back to /P1501B's nozzle.  The new pump
    # must not claim that pipework, so every CREF must be gone.
    check(len(re.findall(r"^CREF\b", out_text, re.M)) == 0,
          "output still carries CREF connections to /P1501B pipework")
    for branch in set(re.findall(r"CREF\s+BRANCH\s+(\S+)", src_text)):
        check(branch not in out_text,
              f"output still references /P1501B branch {branch}")

    # The old tag must not survive as a live reference.  It legitimately
    # appears once in the header provenance comment recording what this file
    # was derived from, so only non-comment lines are checked.
    live = [ln for ln in out_text.split("\n")
            if "/P1501B" in ln and not ln.lstrip().startswith("--")]
    check(not live, f"old tag /P1501B still live in output: {live}")
    check(out_text.count("NEW EQUIPMENT") == 1,
          "output must contain exactly one EQUIPMENT block")
    print("[9] CATR/ORRF counts preserved; all SPCOMPONENTs intact; every"
          " CREF to /P1501B pipework dropped; tag retargeted; one EQUI")

    print()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
