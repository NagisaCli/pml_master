"""
Check the EMITTED MACRO TEXT, not the model that produced it.

Why this exists
---------------
Every other check in this project inspects ``Primitive`` objects.  That whole
layer is blind to how those objects are written out, and on 2026-08-19 a base
element reached the client as

    NEW BOX
    XLEN 382.76mm
    YLEN 231.43mm
    ZLEN 23.95mm
    Y is N and Z is D          <- the ORI keyword was missing
    POS E 13975.25mm ...

which E3D rejected with ``(47,15) CP: Syntax error``.  The model was correct;
the *emission* was not.  30 pumps had passed every geometric and relational
check, and the repo's own ``validate_pml`` did not flag it either -- a bare
clause is indistinguishable from an unrecognised attribute.

So this module reads the finished ``.pml`` back as text and asserts the things
only the text can tell you: that every line is a command E3D knows, that
element blocks are well formed, and that the Iron Rules about ordering survived
the trip from object to file.
"""

from __future__ import annotations

import re
import sys
import math
from pathlib import Path
from typing import Dict, List, Tuple

from base_deform import orientation_basis, profile_centre

REPO = Path(__file__).resolve().parents[3]
DEFAULT = (REPO / "Projects" / "JK_Pump_Build" / "output" /
           "2026-08-20_top_nozzle_r12" /
           "JK_Pump_Build_2026-08-20_top_nozzle_r12_all_pumps.pml")

#: Every attribute keyword this project legitimately emits.
ATTRIBUTES = {
    "DIAM", "DTOP", "DBOT", "HEIG", "XLEN", "YLEN", "ZLEN",
    "XBOT", "YBOT", "XTOP", "YTOP",
    "XOFF", "YOFF", "RADI", "TEMP", "PRES", "TPRESS", "DUTY", "DESC", "CATR",
    "POS", "ORI", "NAPPFLAG", "OBST", "LEVE", "FUNC", "BUIL", "DSCO", "PTSP",
    "INSC", "USRWEI", "USRWWE", "USRCOG", "USRWCO", "DESP",
}
#: PML2 and render-prologue tokens that must never appear (IR-4, IR-5).
FORBIDDEN = re.compile(
    r"^\s*(!!|\$P\b|ENDS\b|END\s+EQUI\b|COLLECT\b|UNSET\b|SUSPEND\b|"
    r"RESUME\b|VAR\s+0\b|ALPHA\b)", re.IGNORECASE)
#: A line that looks like an orientation clause but has lost its keyword.
BARE_ORI = re.compile(r"^\s*[XYZ]\s+is\s+", re.IGNORECASE)
POSITION_TOKEN = re.compile(r"\b([ENSWUD])\s*(-?[\d.]+)\s*mm", re.IGNORECASE)
POSITION_AXIS = {"E": ("east", 1.0), "W": ("east", -1.0),
                 "N": ("north", 1.0), "S": ("north", -1.0),
                 "U": ("up", 1.0), "D": ("up", -1.0)}


def _position(line: str) -> Dict[str, float]:
    result = {"east": 0.0, "north": 0.0, "up": 0.0}
    for letter, value in POSITION_TOKEN.findall(line):
        axis, sign = POSITION_AXIS[letter.upper()]
        result[axis] = sign * float(value)
    return result


def _emitted_hardware(text: str) -> Dict[str, List[dict]]:
    """Parse only anchor CYLINDERs and nested-profile EXTRUSIONs from BASE."""
    equipment = ""
    in_base = False
    stack: List[str] = []
    primitive = None
    result: Dict[str, List[dict]] = {}

    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("NEW EQUIPMENT /", "NEW EQUI /")):
            equipment = line.split("/", 1)[1]
            in_base = False
            stack = []
            primitive = None
            continue
        if line.startswith(("NEW SUBEQUIPMENT /", "NEW SUBE /")):
            sube = line.split("/", 1)[1]
            in_base = sube.endswith("_BASE")
            stack = []
            primitive = None
            continue
        if not in_base or not line or line.startswith("--"):
            continue
        if line.startswith("NEW "):
            kind = line[4:].split()[0].upper()
            stack.append(kind)
            if len(stack) == 1 and kind in ("CYLINDER", "EXTRUSION"):
                primitive = {"kind": kind, "pos": None, "ori": None,
                             "profile": [], "vertex": None}
            elif primitive is not None and kind == "VERTEX":
                primitive["vertex"] = (0.0, 0.0)
            continue
        if line == "END":
            if not stack:
                continue
            kind = stack.pop()
            if primitive is not None and kind == "VERTEX":
                primitive["profile"].append(primitive["vertex"])
                primitive["vertex"] = None
            elif primitive is not None and kind == primitive["kind"]:
                result.setdefault(equipment, []).append(primitive)
                primitive = None
            continue
        if primitive is None:
            continue
        if line.startswith("ORI ") and len(stack) == 1:
            primitive["ori"] = line
        elif line.startswith("POS "):
            pos = _position(line)
            if stack and stack[-1] == "VERTEX":
                primitive["vertex"] = (pos["east"], pos["north"])
            elif len(stack) == 1:
                primitive["pos"] = pos
    return result


def _hardware_axis_problems(text: str) -> List[str]:
    """Check the rounded emitted coordinates, not the pre-emission objects."""
    problems: List[str] = []
    groups = _emitted_hardware(text)
    if len(groups) != 30:
        problems.append(
            f"emitted hardware parser found {len(groups)} BASE groups, expected 30")
    for equipment, hardware in groups.items():
        washers = [item for item in hardware if item["kind"] == "EXTRUSION"]
        bolts = [item for item in hardware if item["kind"] == "CYLINDER"]
        if len(washers) != 10 or len(bolts) != 10:
            problems.append(
                f"{equipment}: emitted {len(washers)} washers / {len(bolts)} bolts")
            continue
        unused = list(bolts)
        for number, washer in enumerate(washers, 1):
            if washer["pos"] is None:
                problems.append(f"{equipment}: washer {number} has no POS")
                continue
            local_x, local_y = profile_centre(washer["profile"])
            basis = orientation_basis(washer["ori"])
            centre = (
                washer["pos"]["east"] + basis["X"][0] * local_x
                + basis["Y"][0] * local_y,
                washer["pos"]["north"] + basis["X"][1] * local_x
                + basis["Y"][1] * local_y,
            )
            bolt = min(unused, key=lambda item: math.hypot(
                item["pos"]["east"] - centre[0],
                item["pos"]["north"] - centre[1]))
            distance = math.hypot(bolt["pos"]["east"] - centre[0],
                                  bolt["pos"]["north"] - centre[1])
            if distance > 0.05:
                problems.append(
                    f"{equipment}: emitted washer {number} centre is "
                    f"{distance:.3f} mm from its anchor axis")
            unused.remove(bolt)
    return problems


def _emitted_base_members(text: str) -> Dict[str, Dict[int, dict]]:
    """Parse rounded top-level BASE members in their preserved 1..43 order."""
    equipment = ""
    in_base = False
    stack: List[str] = []
    current = None
    index = 0
    result: Dict[str, Dict[int, dict]] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("NEW EQUIPMENT /", "NEW EQUI /")):
            equipment = line.split("/", 1)[1]
            in_base = False
            stack = []
            current = None
            continue
        if line.startswith(("NEW SUBEQUIPMENT /", "NEW SUBE /")):
            sube = line.split("/", 1)[1]
            in_base = sube.endswith("_BASE")
            stack = []
            current = None
            index = 0
            continue
        if not in_base or not line or line.startswith("--"):
            continue
        if line.startswith("NEW "):
            kind = line[4:].split()[0].upper()
            if not stack:
                index += 1
                current = {"kind": kind, "attrs": {}, "pos": None}
            stack.append(kind)
            continue
        if line == "END":
            if not stack:
                continue
            stack.pop()
            if not stack and current is not None:
                result.setdefault(equipment, {})[index] = current
                current = None
            continue
        if current is None or len(stack) != 1:
            continue
        keyword = line.split()[0].upper()
        if keyword == "POS":
            current["pos"] = _position(line)
        elif keyword in {"HEIG", "ZLEN"}:
            token = line.split()[1].lower().removesuffix("mm")
            current["attrs"][keyword] = float(token)
    return result


def _pyramid_datum_problems(text: str) -> List[str]:
    """Verify emitted PYRAMID centre datums against named bearing faces."""
    problems: List[str] = []
    groups = _emitted_base_members(text)
    if len(groups) != 30:
        return [f"emitted base parser found {len(groups)} BASE groups, expected 30"]

    def box_span(member):
        half = member["attrs"]["ZLEN"] / 2
        return (member["pos"]["up"] - half, member["pos"]["up"] + half)

    def pyramid_span(member):
        half = member["attrs"]["HEIG"] / 2
        return (member["pos"]["up"] - half, member["pos"]["up"] + half)

    tolerance = 0.06
    station = {6: "motor", 7: "pump", 8: "pump", 9: "motor",
               14: "motor", 15: "pump", 16: "pump", 17: "motor",
               18: "motor", 19: "motor"}
    sole_index = {"pump": 10, "motor": 3}
    pad_index = {"pump": 1, "motor": 13}
    for equipment, members in groups.items():
        if set(members) != set(range(1, 44)):
            problems.append(
                f"{equipment}: emitted base member order is not complete 1..43")
            continue
        foundation = box_span(members[40])[0]
        for index in range(1, 44):
            if members[index]["pos"] is None:
                problems.append(f"{equipment}: element {index} has no POS")
        for index in range(4, 10):
            if members[index]["kind"] != "PYRAMID":
                problems.append(f"{equipment}: element {index} is not PYRAMID")
        for index in range(14, 20):
            if members[index]["kind"] != "PYRAMID":
                problems.append(f"{equipment}: element {index} is not PYRAMID")

        for index in (6, 7, 8, 9):
            group = station[index]
            low, high = pyramid_span(members[index])
            expected_low = box_span(members[sole_index[group]])[1]
            expected_high = box_span(members[pad_index[group]])[0]
            if abs(low - expected_low) > tolerance or abs(high - expected_high) > tolerance:
                problems.append(
                    f"{equipment}: emitted inner PYRAMID {index} spans "
                    f"{low:.2f}..{high:.2f}, expected "
                    f"{expected_low:.2f}..{expected_high:.2f}")
        for index in (14, 15, 16, 17, 18, 19):
            group = station[index]
            low, _ = pyramid_span(members[index])
            expected_low = box_span(members[sole_index[group]])[1]
            if abs(low - expected_low) > tolerance:
                problems.append(
                    f"{equipment}: emitted outer PYRAMID {index} bottom "
                    f"{low:.2f}, expected sole top {expected_low:.2f}")
        for index in (4, 5):
            low, _ = pyramid_span(members[index])
            expected_low = box_span(members[1])[1]
            if abs(low - expected_low) > tolerance:
                problems.append(
                    f"{equipment}: emitted saddle PYRAMID {index} bottom "
                    f"{low:.2f}, expected pad top {expected_low:.2f}")
        for index in (*range(4, 10), *range(14, 20)):
            low, _ = pyramid_span(members[index])
            if low < foundation - tolerance:
                problems.append(
                    f"{equipment}: emitted PYRAMID {index} reaches U "
                    f"{low:.2f} below foundation U {foundation:.2f}")
    return problems


def check(path: Path) -> List[str]:
    problems: List[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    block: str = ""
    block_line = 0
    seen_pos = False
    seen_ori = False
    depth = 0

    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("--"):
            continue

        if FORBIDDEN.match(line):
            problems.append(f"L{number}: forbidden PML2/prologue token: {line}")
            continue

        # A bare orientation clause: the exact defect that reached the client.
        if BARE_ORI.match(line):
            problems.append(
                f"L{number}: orientation clause without its ORI keyword "
                f"(E3D reports 'CP: Syntax error'): {line}")
            continue

        if line.startswith("NEW "):
            kind = line[4:].split("/", 1)[0].strip().upper()
            # IR-5: EQUIPMENT and SUBEQUIPMENT are grouping elements closed
            # implicitly by the next one, not by an END.  Counting them as
            # openable blocks reports every macro as unclosed.
            if kind not in ("EQUIPMENT", "SUBEQUIPMENT"):
                depth += 1
            block = kind
            block_line = number
            seen_pos = seen_ori = False
            continue

        if line == "END":
            depth -= 1
            if depth < 0:
                problems.append(f"L{number}: END without a matching NEW")
                depth = 0
            block = ""
            continue

        keyword = line.split()[0].upper()
        if keyword not in ATTRIBUTES:
            problems.append(
                f"L{number}: unrecognised command in {block or '(top level)'} "
                f"block from L{block_line}: {line}")
            continue

        # IR-2: primitives take ORI before POS; a NOZZLE takes POS before ORI.
        if keyword == "POS":
            seen_pos = True
            if block == "NOZZLE" and seen_ori:
                problems.append(
                    f"L{number}: NOZZLE (L{block_line}) has ORI before POS")
        elif keyword == "ORI":
            seen_ori = True
            if block in ("CYLINDER", "CONE", "DISH", "BOX", "PYRAMID",
                         "EXTRUSION") and seen_pos:
                problems.append(
                    f"L{number}: {block} (L{block_line}) has POS before ORI "
                    f"(IR-2: the element drifts silently)")
        elif keyword == "CATR" and block == "NOZZLE" and (seen_pos or seen_ori):
            # IR-9a: the catalogue binding must come first or the load aborts.
            problems.append(
                f"L{number}: NOZZLE (L{block_line}) binds CATR after POS/ORI")

    if depth != 0:
        problems.append(f"{depth} element block(s) left unclosed at end of file")

    problems.extend(_hardware_axis_problems(text))
    problems.extend(_pyramid_datum_problems(text))

    return problems


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.exists():
        print(f"macro not found: {path}")
        return 1
    problems = check(path)
    print(f"{path.name}: {len(problems)} text-level problems")
    for problem in problems[:40]:
        print(f"  - {problem}")
    if len(problems) > 40:
        print(f"  ... and {len(problems) - 40} more")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
