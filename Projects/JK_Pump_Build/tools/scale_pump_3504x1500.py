"""
Scale JK_Pump_Build 205-PU-012 to a 3504 x 1500 mm baseplate.

Why this tool exists
--------------------
The client supplied the accepted 205-PU-012 native E3D data listing
(``C:\\Users\\A\\Desktop\\Custom_pump.txt``) and asked for a variant whose
baseplate is 3504 mm long x 1500 mm wide, with the rest of the pump enlarged
proportionally, the construction/shape kept, and nozzle sizes kept unchanged.

Scaling rules (all are Reference decisions and are reported to the client):

* Baseplate:  ``XLEN 1500`` (E/width), ``YLEN 3504`` (N/length), ``ZLEN 50``;
  underside centre ``(E 33065, N 13825, U 0)`` is the fixed scaling origin in
  plan.
* Superstructure:  one uniform scale factor ``s = 3504 / 2701`` (the
  longitudinal baseplate ratio).  Plan coordinates scale about the baseplate
  centre ``(33065, 13825)``; elevations scale about the fixed baseplate top
  plane ``U = 50`` so the rail -> sole-plate -> pedestal -> machine bearing
  chain stays seated and nothing drops below the foundation.
* The baseplate width is the client's explicit override (a uniform scale
  would give 1615.1 mm, not 1500 mm); every other transverse dimension uses
  ``s``.
* Native NOZZLE elements keep ``CATR``, ``HEIG``, ``ORI``, TEMP/PRES/TPRESS
  and DUTY.  Their flange faces are re-anchored: the barrel root point is
  scaled with the machine and the unchanged HEIG is added along the aim
  direction, so a nozzle stays attached to the enlarged casing instead of
  floating ``(s - 1) * HEIG`` clear of it.
* The DISCHARGE boss cylinder is part of the unchanged connection, so its
  DIAM/HEIG stay fixed while its centre follows the scaled casing crown.
* Every other dimension (BOX/CYLINDER/CONE/EXTRUSION sizes, hex-vertex
  profiles, owner-relative NCYLINDER offsets) multiplies by ``s``.

Two defects in the supplied file are handled and reported:

* The file contains the same pump exported twice, back to back.  Loading both
  would collide on the duplicate ``/205_PU_012`` name, so the second listing
  is dropped and exactly one EQUI is emitted.
* The native listing omits ``NAPPFLAG 2`` on the nested NCYLINDER, which the
  project verified is mandatory for the negative cylinder to cut a hole
  (r3-r4).  The attribute is re-added so the terminal-box hole survives the
  reload.

The tool is a mechanical rewrite: it transforms numbers line by line and
never reorders attributes or replaces the native INPUT listing form.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


# The custom pump native export lives outside the repository, so it may be
# absent on another machine or after a cleanup. Override with argv[1];
# require_input() turns a missing file into a readable message rather than a
# bare "source not found" line.
SOURCE = (
    Path(sys.argv[1]) if len(sys.argv) > 1
    else Path(r"C:\Users\A\Desktop\Custom_pump.txt")
)
PROJECT = Path(__file__).resolve().parents[1]


def require_input(path: Path, what: str) -> Path:
    """Exit with an actionable message when an external input is absent."""
    if not path.exists():
        raise SystemExit(
            "Input not found: {0}\n"
            "  This script needs {1}.\n"
            "  That file is external to the repository and is not versioned.\n"
            "  Pass it explicitly:  python {2} <path>".format(
                path, what, Path(__file__).name
            )
        )
    return path
OUTPUT_DIR = PROJECT / "output"
IMPORTS_DIR = PROJECT / "imports"

EQUI_NAME = "/205_PU_012"
BASEPLATE_SUBE = "/205_PU_012_BASEPLATE"
DISCHARGE_SUBE = "/205_PU_012_DISCHARGE"

# Contractual baseplate underside centre.
CE = Decimal("33065")
CN = Decimal("13825")

# Baseplate stays 50 mm thick; the top plane is the elevation scaling origin.
PLATE_TOP = Decimal("50")
PLATE_T = Decimal("50")

OLD_LEN = Decimal("2701")
OLD_WID = Decimal("1245")
NEW_LEN = Decimal("3504")
NEW_WID = Decimal("1500")

S = NEW_LEN / OLD_LEN

# Nozzle invariants.  ``root`` is the barrel attachment point on the machine,
# ``aim`` is the world aim direction and ``heig`` is the unchanged projection.
NOZZLES = {
    "/205_PU_012_SUCTION_NOZZLE": {
        "root": (CE, Decimal("15008"), Decimal("450")),
        "aim": (Decimal("0"), Decimal("1"), Decimal("0")),
        "heig": Decimal("250"),
    },
    "/205_PU_012_DISCHARGE_NOZZLE": {
        "root": (CE, Decimal("14721.7"), Decimal("705.5")),
        "aim": (Decimal("0"), Decimal("0"), Decimal("1")),
        "heig": Decimal("224.1"),
    },
}

POS_RE = re.compile(
    r"^POS\s+([ENSWUD])\s+([\d.]+)mm\s+([ENSWUD])\s+([\d.]+)mm"
    r"\s+([ENSWUD])\s+([\d.]+)mm$"
)
DIM_RE = re.compile(r"^(XLEN|YLEN|ZLEN|DIAM|HEIG|DTOP|DBOT)\s+([\d.]+)mm$")
NEW_RE = re.compile(r"^NEW\s+([A-Z]+)(?:\s+(\S+))?$")


def q(value: Decimal) -> Decimal:
    """Round to the native listing's 0.1 mm precision, half away from zero."""
    return value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def fmt(value: Decimal) -> str:
    """Format a length like the native listing (integers stay integer)."""
    value = q(value)
    if value == value.to_integral_value():
        return str(int(value))
    return f"{value:.1f}"


def world_pos(east: Decimal, north: Decimal, up: Decimal) -> tuple:
    """Scale a world coordinate about the plate centre / plate top plane."""
    return (
        CE + (east - CE) * S,
        CN + (north - CN) * S,
        PLATE_TOP + (up - PLATE_TOP) * S,
    )


def pos_line(east: Decimal, north: Decimal, up: Decimal) -> str:
    return f"POS E {fmt(east)}mm N {fmt(north)}mm U {fmt(up)}mm"


def nozzle_face(name: str) -> str:
    spec = NOZZLES[name]
    root_e, root_n, root_u = spec["root"]
    aim_e, aim_n, aim_u = spec["aim"]
    heig = spec["heig"]
    east, north, up = world_pos(root_e, root_n, root_u)
    return pos_line(east + aim_e * heig, north + aim_n * heig, up + aim_u * heig)


def transform_lines(lines):
    """Mechanical numeric rewrite of one INPUT listing body."""
    out = []
    stack = []  # element type stack for the NEW/END nesting
    sube = None
    baseplate_box = False
    nozzle_name = None

    for line in lines:
        text = line.strip()

        new_match = NEW_RE.match(text)
        if new_match:
            element = new_match.group(1).upper()
            name = new_match.group(2)
            if element == "EQUIPMENT":
                stack.append("EQUI")
            elif element == "SUBEQUIPMENT":
                sube = name
                stack.append("SUBE")
            elif element == "NOZZLE":
                nozzle_name = name
                stack.append("NOZZLE")
            elif element == "NCYLINDER":
                stack.append("NCYL")
            elif element == "LOOP":
                stack.append("LOOP")
            elif element == "VERTEX":
                stack.append("VERTEX")
            else:
                stack.append(element)
                if element == "BOX" and sube == BASEPLATE_SUBE:
                    baseplate_box = True
            out.append(line)
            continue

        if text == "END":
            if not stack:
                raise ValueError("unbalanced END in source listing")
            closed = stack.pop()
            if closed == "BOX" and baseplate_box:
                baseplate_box = False
            if closed == "SUBE":
                sube = None
            if closed == "NOZZLE":
                nozzle_name = None
            out.append(line)
            continue

        if text.startswith("POS "):
            match = POS_RE.match(text)
            if not match:
                raise ValueError(f"unrecognised POS line: {text!r}")
            axes = (match.group(1), match.group(3), match.group(5))
            values = (Decimal(match.group(2)), Decimal(match.group(4)), Decimal(match.group(6)))
            if "NOZZLE" in stack:
                if nozzle_name not in NOZZLES:
                    raise ValueError(f"unknown nozzle {nozzle_name}")
                out.append(nozzle_face(nozzle_name))
            elif stack and (stack[-1] == "VERTEX" or "NCYL" in stack):
                parts = [f"{axis} {fmt(value * S)}mm" for axis, value in zip(axes, values)]
                out.append("POS " + " ".join(parts))
            elif baseplate_box:
                out.append(line)
            else:
                if axes != ("E", "N", "U"):
                    raise ValueError(f"world POS must use E/N/U, got {text!r}")
                east, north, up = world_pos(*values)
                out.append(pos_line(east, north, up))
            continue

        dim_match = DIM_RE.match(text)
        if dim_match:
            attribute, value = dim_match.group(1), Decimal(dim_match.group(2))
            if baseplate_box:
                replacement = {
                    "XLEN": NEW_WID,
                    "YLEN": NEW_LEN,
                    "ZLEN": PLATE_T,
                }[attribute]
                out.append(f"{attribute} {fmt(replacement)}mm")
            elif "NOZZLE" in stack:
                out.append(line)  # HEIG of a native nozzle is unchanged
            elif sube == DISCHARGE_SUBE and stack and stack[-1] == "CYLINDER":
                out.append(line)  # discharge boss keeps its connection size
            else:
                out.append(f"{attribute} {fmt(value * S)}mm")
                if stack and stack[-1] == "NCYL" and attribute == "HEIG":
                    out.append("NAPPFLAG 2")
            continue

        out.append(line)

    if stack:
        raise ValueError(f"unclosed elements at end of body: {stack}")
    return out


def duplicate_start(lines):
    """Return the first line index of the second export in the file."""
    markers = [index for index, line in enumerate(lines) if line.startswith("$S-")]
    if len(markers) < 2:
        return len(lines)
    return markers[1]


def archive_original():
    IMPORTS_DIR.mkdir(parents=True, exist_ok=True)
    destination = IMPORTS_DIR / f"{date.today().isoformat()}_Custom_pump.txt"
    current = hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper()
    if destination.exists():
        existing = hashlib.sha256(destination.read_bytes()).hexdigest().upper()
        if existing != current:
            raise SystemExit(
                f"archive already exists with different content: {destination}"
            )
        print(f"archive already present and byte-identical -> {destination}")
        return destination, existing
    shutil.copy2(SOURCE, destination)
    print(f"archived original -> {destination}")
    print(f"SHA-256 {current}")
    return destination, current


def main():
    require_input(SOURCE, "the custom pump native export")

    archive_path, digest = archive_original()

    lines = SOURCE.read_text(encoding="utf-8-sig").splitlines()
    body = lines[: duplicate_start(lines)]
    transformed = transform_lines(body)

    desktop_out = SOURCE.with_name("Custom_pump_3504x1500.txt")
    desktop_out.write_text("\n".join(transformed) + "\n", encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    project_out = OUTPUT_DIR / "205-PU-012_3504x1500.txt"
    project_out.write_text("\n".join(transformed) + "\n", encoding="utf-8")

    print(f"wrote -> {desktop_out}")
    print(f"wrote -> {project_out}")
    print(f"scale factor s = 3504/2701 = {S}")
    print(f"duplicate export dropped: kept {len(body)} lines of {len(lines)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
