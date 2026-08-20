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
from pathlib import Path
from typing import List

REPO = Path(__file__).resolve().parents[3]
DEFAULT = (REPO / "Projects" / "JK_Pump_Build" / "output" / "2026-08-19_pumps"
           / "JK_Pump_Build_2026-08-19_all_pumps.pml")

#: Every attribute keyword this project legitimately emits.
ATTRIBUTES = {
    "DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "XBOT", "YBOT", "XTOP", "YTOP",
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
