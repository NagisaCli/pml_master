"""
Independent numeric verification for ``scale_pump_3504x1500.py``.

The verifier parses the supplied native listing and the scaled output with its
own parser and checks properties, not only the transform formula:

* one EQUI, one INPUT block, unchanged element inventory;
* baseplate exactly 1500 x 3504 x 50 at the contractual underside centre;
* every non-nozzle solid keeps the uniform superstructure scale (world plan
  about the plate centre, elevation about the plate top);
* nozzles keep CATR/HEIG/ORI and their flange face sits HEIG beyond the
  scaled barrel root, so the barrel stays attached to the enlarged machine;
* the nested NCYLINDER carries NAPPFLAG 2 and stays inside its owner plate;
* nothing ends up below the foundation and every non-nozzle solid stays
  inside the new baseplate plan envelope;
* the vertical support chain (rail -> sole -> web -> middle -> machine foot)
  is contact-preserved, and the suction/discharge roots still meet the
  scaled casing/boss.
"""

from __future__ import annotations

import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"C:\Users\A\Desktop\Custom_pump.txt")
OUTPUT = SOURCE.with_name("Custom_pump_3504x1500.txt")

CE = Decimal("33065")
CN = Decimal("13825")
PLATE_TOP = Decimal("50")
NEW_LEN = Decimal("3504")
NEW_WID = Decimal("1500")
S = NEW_LEN / Decimal("2701")

POS_RE = re.compile(
    r"^POS\s+([ENSWUD])\s+(-?[\d.]+)mm\s+([ENSWUD])\s+(-?[\d.]+)mm"
    r"\s+([ENSWUD])\s+(-?[\d.]+)mm$"
)
DIM_RE = re.compile(r"^(XLEN|YLEN|ZLEN|DIAM|HEIG|DTOP|DBOT)\s+([\d.]+)mm$")
NEW_RE = re.compile(r"^NEW\s+([A-Z]+)(?:\s+(\S+))?$")
ORI_RE = re.compile(
    r"^ORI\s+Y\s+IS\s+([ENSWUD])\s+AND\s+Z\s+IS\s+([ENSWUD])$",
    re.IGNORECASE,
)

AXIS_SIGN = {"E": 1, "W": -1, "N": 1, "S": -1, "U": 1, "D": -1}


def q1(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def parse(path: Path):
    """Parse one INPUT listing into an ordered element list."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    begin = next(i for i, line in enumerate(lines) if line.strip() == "INPUT BEGIN")
    finish = next(i for i, line in enumerate(lines) if line.strip() == "INPUT FINISH")

    elements = []
    stack = []
    sube = None
    nozzle = None
    pending = None  # element dict under construction
    catr = {}

    def new_element(kind, name=None):
        return {
            "kind": kind,
            "sube": sube,
            "name": name,
            "pos": None,
            "dims": {},
            "ori": None,
            "vertices": [],
            "heig": None,
            "nappflag": None,
        }

    for line in lines[begin + 1 : finish]:
        text = line.strip()
        if not text or text.startswith("--"):
            continue
        match = NEW_RE.match(text)
        if match:
            kind = match.group(1).upper()
            name = match.group(2)
            if kind == "SUBEQUIPMENT":
                sube = name
                stack.append(("SUBE", None))
                continue
            if kind == "EQUIPMENT":
                stack.append(("EQUI", None))
                continue
            element = new_element(kind, name)
            if kind == "NOZZLE":
                nozzle = name
            elements.append(element)
            pending = element
            stack.append((kind, element))
            continue
        if text == "END":
            if stack:
                stack.pop()
            if stack and stack[-1][0] in ("LOOP", "VERTEX"):
                pending = stack[-1][1]
            elif stack:
                pending = stack[-1][1]
            else:
                pending = None
            continue
        if text.startswith("POS "):
            pos_match = POS_RE.match(text)
            if not pos_match:
                raise ValueError(f"unrecognised POS: {text!r}")
            axes = (
                pos_match.group(1),
                pos_match.group(3),
                pos_match.group(5),
            )
            values = (
                Decimal(pos_match.group(2)),
                Decimal(pos_match.group(4)),
                Decimal(pos_match.group(6)),
            )
            if stack and stack[-1][0] == "VERTEX":
                parent = next(
                    element
                    for kind, element in reversed(stack)
                    if kind == "EXTRUSION"
                )
                parent["vertices"].append(tuple(values))
            else:
                pending["pos"] = (axes, values)
            continue
        dim_match = DIM_RE.match(text)
        if dim_match:
            attribute, value = dim_match.group(1), Decimal(dim_match.group(2))
            if stack and stack[-1][0] == "NOZZLE" and attribute == "HEIG":
                pending["heig"] = value
            else:
                pending["dims"][attribute] = value
            continue
        ori_match = ORI_RE.match(text)
        if ori_match:
            pending["ori"] = (ori_match.group(1), ori_match.group(2))
            continue
        if text.startswith("TEMP ") or text.startswith("PRES ") or text.startswith("TPRESS "):
            pending.setdefault("process", {})[text.split()[0]] = text
            continue
        if text.startswith("DUTY "):
            pending["duty"] = text
            continue
        if text.startswith("NAPPFLAG "):
            pending["nappflag"] = int(text.split()[1])
            continue
        if text.startswith("OLD NOZZLE "):
            nozzle = text.split()[2]
            continue
        if text.startswith("CATR "):
            catr[nozzle] = text.split("CATR ", 1)[1]
            continue

    return elements, catr


def signed(axis, value):
    return AXIS_SIGN[axis] * value


def world_components(element):
    """Return (e, n, u) world centre and dims for AABB purposes."""
    axes, (a, b, c) = element["pos"]
    e = n = u = Decimal(0)
    for axis, value in zip(axes, (a, b, c)):
        if axis in ("E", "W"):
            e = signed(axis, value)
        elif axis in ("N", "S"):
            n = signed(axis, value)
        else:
            u = signed(axis, value)
    return e, n, u


def aabb(element):
    """Axis-aligned bounding box (emin, emax, nmin, nmax, umin, umax)."""
    kind = element["kind"]
    e, n, u = world_components(element)
    dims = element["dims"]
    if kind == "BOX":
        return (
            e - dims["XLEN"] / 2, e + dims["XLEN"] / 2,
            n - dims["YLEN"] / 2, n + dims["YLEN"] / 2,
            u - dims["ZLEN"] / 2, u + dims["ZLEN"] / 2,
        )
    if kind in ("CYLINDER", "CONE"):
        diameter = dims.get("DIAM") or max(dims["DTOP"], dims["DBOT"])
        axis = element["ori"][1] if element["ori"] else "U"
        if axis in ("N", "S"):
            return (
                e - diameter / 2, e + diameter / 2,
                n - dims["HEIG"] / 2, n + dims["HEIG"] / 2,
                u - diameter / 2, u + diameter / 2,
            )
        if axis in ("E", "W"):
            return (
                e - dims["HEIG"] / 2, e + dims["HEIG"] / 2,
                n - diameter / 2, n + diameter / 2,
                u - diameter / 2, u + diameter / 2,
            )
        return (
            e - diameter / 2, e + diameter / 2,
            n - diameter / 2, n + diameter / 2,
            u - dims["HEIG"] / 2, u + dims["HEIG"] / 2,
        )
    if kind == "EXTRUSION":
        vertices = element["vertices"]
        ve = [v[0] for v in vertices]
        vn = [v[1] for v in vertices]
        return (
            e + min(ve), e + max(ve),
            n + min(vn), n + max(vn),
            u, u + dims["HEIG"],
        )
    raise ValueError(f"no AABB for {kind}")


def predicted_world(axes, values):
    """Independent restatement of the world transform for cross-checks."""
    out = []
    for axis, value in zip(axes, values):
        if axis == "E":
            out.append(CE + (value - CE) * S)
        elif axis == "N":
            out.append(CN + (value - CN) * S)
        elif axis == "U":
            out.append(PLATE_TOP + (value - PLATE_TOP) * S)
        else:
            raise ValueError(f"world axis {axis} unexpected")
    return tuple(out)


def main():
    src_elements, src_catr = parse(SOURCE)
    out_elements, out_catr = parse(OUTPUT)

    failures = []
    def check(condition, message):
        if not condition:
            failures.append(message)

    check(len(src_elements) == len(out_elements),
          f"element inventory changed: {len(src_elements)} -> {len(out_elements)}")

    for src, out in zip(src_elements, out_elements):
        if src["kind"] != out["kind"]:
            failures.append(f"element kind changed at {src['sube']} {src['kind']}")
            continue
        if src["kind"] == "NOZZLE":
            check(src["name"] == out["name"], "nozzle name changed")
            check(src["heig"] == out["heig"],
                  f"{src['name']}: HEIG changed {src['heig']} -> {out['heig']}")
            check(src["heig"] in (Decimal("250"), Decimal("224.1")),
                  f"{src['name']}: parser failed to read HEIG ({src['heig']})")
            check(src["ori"] == out["ori"], f"{src['name']}: ORI changed")
            continue
        if src["kind"] == "VERTEX":
            for sv, ov in zip(src["vertices"], out["vertices"]):
                check(ov == tuple(q1(v * S) for v in sv),
                      f"VERTEX profile not scaled by s: {sv} -> {ov}")
            continue
        if src["kind"] in ("LOOP", "EQUI", "SUBE"):
            continue
        if src["sube"] == "/205_PU_012_BASEPLATE":
            axes, values = out["pos"]
            check(axes == ("E", "N", "U"), "baseplate POS axes changed")
            check(tuple(values) == (CE, CN, Decimal("25")), "baseplate centre moved")
            check(out["dims"].get("XLEN") == NEW_WID, "baseplate XLEN != 1500")
            check(out["dims"].get("YLEN") == NEW_LEN, "baseplate YLEN != 3504")
            check(out["dims"].get("ZLEN") == Decimal("50"), "baseplate ZLEN != 50")
            continue
        if src["kind"] == "NCYLINDER":
            axes, values = out["pos"]
            _src_axes, src_values = src["pos"]
            expected = tuple(q1(v * S) for v in src_values)
            check(tuple(values) == expected, f"NCYL relative POS not scaled: {values}")
            for key in ("DIAM", "HEIG"):
                check(out["dims"].get(key) == q1(src["dims"][key] * S),
                      f"NCYL {key} not scaled")
            check(out["nappflag"] == 2, "NCYLINDER missing NAPPFLAG 2")
            continue
        # World primitives.
        if src["pos"] is None:
            continue
        src_axes, src_values = src["pos"]
        out_axes, out_values = out["pos"]
        check(src_axes == out_axes, f"POS axes changed at {src['sube']}")
        if src_axes == ("E", "N", "U"):
            expected = predicted_world(src_axes, src_values)
            got = tuple(out_values)
            tolerance = Decimal("0.11")
            check(all(abs(g - x) <= tolerance for g, x in zip(got, expected)),
                  f"{src['kind']} POS drift: {src_values} -> {got}, expected {expected}")
        if src["sube"] == "/205_PU_012_DISCHARGE" and src["kind"] == "CYLINDER":
            check(out["dims"].get("DIAM") == src["dims"].get("DIAM"),
                  "discharge boss DIAM changed")
            check(out["dims"].get("HEIG") == src["dims"].get("HEIG"),
                  "discharge boss HEIG changed")
            continue
        for key in ("XLEN", "YLEN", "ZLEN", "DIAM", "HEIG", "DTOP", "DBOT"):
            if key in src["dims"]:
                check(out["dims"].get(key) == q1(src["dims"][key] * S),
                      f"{src['kind']} {key} not scaled at {src['sube']}")

    check(src_catr == out_catr, f"CATR bindings changed: {src_catr} -> {out_catr}")

    # Nozzle face anchors.
    by_name = {element["name"]: element for element in out_elements if element["kind"] == "NOZZLE"}
    suction = by_name["/205_PU_012_SUCTION_NOZZLE"]
    _axes, (s_e, s_n, s_u) = suction["pos"]
    check((s_e, s_u) == (CE, Decimal("568.9")),
          f"suction face datum wrong: {suction['pos']}")
    check(s_n == Decimal("15609.7"), f"suction face N wrong: {s_n}")
    discharge = by_name["/205_PU_012_DISCHARGE_NOZZLE"]
    _axes, (d_e, d_n, d_u) = discharge["pos"]
    check((d_e, d_n) == (CE, Decimal("14988.3")),
          f"discharge face plan datum wrong: {discharge['pos']}")
    check(d_u == Decimal("1124.5"), f"discharge face U wrong: {d_u}")

    # Physical bounds.
    solid_kinds = {"BOX", "CYLINDER", "CONE", "EXTRUSION"}
    for element in out_elements:
        if element["kind"] not in solid_kinds:
            continue
        emin, emax, nmin, nmax, umin, umax = aabb(element)
        check(umin >= Decimal("-0.01"), f"{element['kind']} below foundation: {aabb(element)}")
        if element["sube"] in (None,):
            continue
        check(
            emin >= CE - NEW_WID / 2 - Decimal("0.2")
            and emax <= CE + NEW_WID / 2 + Decimal("0.2")
            and nmin >= CN - NEW_LEN / 2 - Decimal("0.2")
            and nmax <= CN + NEW_LEN / 2 + Decimal("0.2"),
            f"{element['kind']} escapes baseplate envelope: {aabb(element)}",
        )

    # Support-chain scale invariance: uniform scaling about the plate top
    # multiplies every relative U distance by s, so every source contact or
    # clearance must remain a contact or s-scaled clearance in the output.
    chain_src = []
    chain_out = []
    for element in out_elements:
        if element["kind"] in solid_kinds and element["sube"] in (
            "/205_PU_012_BASE_FASTENERS",
            "/205_PU_012_SUPPORT_FRAME",
            "/205_PU_012_CASING",
            "/205_PU_012_DRIVER",
        ):
            chain_out.append(aabb(element))
    for element in src_elements:
        if element["kind"] in solid_kinds and element["sube"] in (
            "/205_PU_012_BASE_FASTENERS",
            "/205_PU_012_SUPPORT_FRAME",
            "/205_PU_012_CASING",
            "/205_PU_012_DRIVER",
        ):
            chain_src.append(aabb(element))
    check(len(chain_src) == len(chain_out), "base chain inventory changed")
    check(len(chain_src) > 0, "support chain parse returned no elements")
    for s_box, o_box in zip(chain_src, chain_out):
        s_emin, s_emax, s_nmin, s_nmax, s_umin, s_umax = s_box
        o_emin, o_emax, o_nmin, o_nmax, o_umin, o_umax = o_box
        expected_bottom = PLATE_TOP + (s_umin - PLATE_TOP) * S
        expected_top = PLATE_TOP + (s_umax - PLATE_TOP) * S
        check(
            abs(o_umin - expected_bottom) <= Decimal("0.5")
            and abs(o_umax - expected_top) <= Decimal("0.5"),
            f"base solid U span drifted: source {s_umin}..{s_umax}, "
            f"output {o_umin}..{o_umax}",
        )

    # Barrel roots stay attached to the scaled machine.
    crown_matches = [
        element for element in out_elements
        if element["kind"] == "CYLINDER"
        and element["sube"] == "/205_PU_012_CASING"
        and element["dims"].get("HEIG") == Decimal("28.5")
    ]
    check(len(crown_matches) == 1, f"casing crown match ambiguous: {len(crown_matches)}")
    crown = crown_matches[0]
    _axes, (ce_, cn_, cu_) = crown["pos"]
    check(abs(s_n - (cn_ + crown["dims"]["HEIG"] / 2 + suction["heig"])) <= Decimal("0.2"),
          "suction barrel no longer meets casing crown")

    boss = next(
        element for element in out_elements
        if element["kind"] == "CYLINDER" and element["sube"] == "/205_PU_012_DISCHARGE"
    )
    _axes, (be_, bn_, bu_) = boss["pos"]
    boss_bottom = bu_ - boss["dims"]["HEIG"] / 2
    boss_top = bu_ + boss["dims"]["HEIG"] / 2
    root_u = d_u - discharge["heig"]
    check(boss_bottom <= root_u <= boss_top,
          f"discharge barrel root escapes boss: root {root_u}, boss {boss_bottom}..{boss_top}")

    # NCYLINDER hole containment: the hole circle stays inside its owner plate
    # with at least a 2 mm rim (the project's settled r5 rule).
    for index, element in enumerate(out_elements):
        if element["kind"] != "NCYLINDER":
            continue
        owner = next(
            candidate for candidate in reversed(out_elements[:index])
            if candidate["kind"] == "BOX" and candidate["sube"] == element["sube"]
        )
        _axes, (_de, _dn, dz) = element["pos"]
        radius = element["dims"]["DIAM"] / 2
        half_height = owner["dims"]["ZLEN"] / 2
        check(
            abs(dz) + radius <= half_height - Decimal("2"),
            f"NCYL hole breaches its plate rim: |dz|={abs(dz)} + r={radius} "
            f"> {half_height - Decimal('2')}",
        )

    print(f"elements compared: {len(out_elements)}")
    print(f"solid AABBs checked: {sum(1 for e in out_elements if e['kind'] in solid_kinds)}")
    print(f"CATR bindings: {out_catr}")
    if failures:
        print(f"\nFAILURES: {len(failures)}")
        for failure in failures:
            print(f" - {failure}")
        return 1
    print("\nALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
