"""Adapt the user-supplied native TEM.txt into a standalone 202-PU-068 macro.

The native template is kept as the geometry baseline.  Only explicitly
authorised fields are changed: tag, plan datum/envelope, plan orientation and
the two nozzle catalogue references.
"""

from __future__ import annotations

import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
PROJECT = REPO / "Projects" / "JK_Pump_Build"
SOURCE = PROJECT / "imports" / "2026-09-10_TEM.txt"
OUTPUT = PROJECT / "output" / "202-PU-068_from_TEM_20260910.pml"
REPORT = PROJECT / "output" / "202-PU-068_from_TEM_20260910_report.md"

SOURCE_TAG = "204_PU_006"
TARGET_TAG = "202_PU_068"
TEMPLATE_BASE_E = 20000.05
TEMPLATE_BASE_N = 17410.0
TEMPLATE_XLEN = 447.12       # native BOX XLEN: transverse for axis E
TEMPLATE_YLEN = 1725.1       # native BOX YLEN: longitudinal for axis E
TARGET_E = 4000.0
TARGET_N = 36780.0
TARGET_XLEN = 750.0          # transverse for target axis N
TARGET_YLEN = 1920.0         # longitudinal for target axis N
TARGET_BOTTOM_U = 0.0
PLATE_THICKNESS = 50.0
DN200_CATR = "/150lb_Ansi_Flanged/AAZFBB0TT"


def fmt(value: float) -> str:
    value = round(value, 2)
    if abs(value - round(value)) < 0.005:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def pos_line(east: float, north: float, up: float) -> str:
    e_letter, e_value = ("E", east) if east >= 0 else ("W", -east)
    n_letter, n_value = ("N", north) if north >= 0 else ("S", -north)
    u_letter, u_value = ("U", up) if up >= 0 else ("D", -up)
    return (
        f"POS {e_letter} {fmt(e_value)}mm "
        f"{n_letter} {fmt(n_value)}mm "
        f"{u_letter} {fmt(u_value)}mm"
    )


def parse_pos(line: str) -> tuple[float, float, float] | None:
    values = {"E": 0.0, "N": 0.0, "U": 0.0}
    found = False
    for axis, text in re.findall(r"\b([EWNSUD])\s+([+-]?[\d.]+)mm", line):
        value = float(text)
        if axis == "E":
            values["E"] = value
        elif axis == "W":
            values["E"] = -value
        elif axis == "N":
            values["N"] = value
        elif axis == "S":
            values["N"] = -value
        elif axis == "U":
            values["U"] = value
        else:
            values["U"] = -value
        found = True
    return (values["E"], values["N"], values["U"]) if found else None


def rotate_direction_tokens(line: str) -> str:
    """Rotate the native E-axis frame into the target +N frame: E->N, N->W."""
    mapping = {"E": "N", "W": "S", "N": "W", "S": "E", "U": "U", "D": "D"}
    if not line.lstrip().upper().startswith("ORI "):
        return line
    return re.sub(
        r"(?<![A-Z])([EWNSUD])(?![A-Z])",
        lambda match: mapping[match.group(1).upper()],
        line,
        flags=re.IGNORECASE,
    )


def extract_parts(text: str) -> tuple[str, str, str]:
    start = text.find(f"NEW EQUIPMENT /{SOURCE_TAG}")
    old_nozzle = text.find("OLD NOZZLE", start)
    input_end = text.find("INPUT END", old_nozzle)
    if start < 0 or old_nozzle < 0 or input_end < 0:
        raise RuntimeError("TEM.txt does not contain the expected native pump sections")
    return text[:start], text[start:old_nozzle].strip(), text[old_nozzle:input_end].strip()


def transform_body(body: str) -> str:
    # This is a rigid template placement.  Do not scale the pump assembly:
    # changing the baseplate envelope must not change the native clearances
    # between casing, shaft, driver, feet, and accessories.
    sx = 1.0
    sy = 1.0
    lines = body.replace(f"/{SOURCE_TAG}", f"/{TARGET_TAG}").splitlines()
    out: list[str] = []
    in_loop = False
    current_sube = ""
    equipment_pos_done = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("NEW SUBEQUIPMENT /"):
            current_sube = stripped.split("/", 1)[1]
        if stripped == "NEW LOOP":
            in_loop = True

        if stripped.startswith("POS ") and not in_loop:
            parsed = parse_pos(stripped)
            if parsed is not None:
                east, north, up = parsed
                if not equipment_pos_done:
                    out.append("POS E 0mm N 0mm U 0mm")
                    equipment_pos_done = True
                    continue
                # Native template axis +E becomes target axis +N.  Native +N
                # becomes target -E, preserving the right-handed plan frame.
                # The placement is rigid; only the base envelope is adapted.
                new_e = TARGET_E - (north - TEMPLATE_BASE_N) * sx
                new_n = TARGET_N + (east - TEMPLATE_BASE_E) * sy
                new_u = TARGET_BOTTOM_U + up
                out.append(pos_line(new_e, new_n, new_u))
                continue

        if stripped.startswith("ORI "):
            out.append(rotate_direction_tokens(line))
            continue

        # Baseplate and full-length base members are the only dimensional
        # changes.  All pump, motor, casing and fastener dimensions remain
        # native template values as requested.
        if current_sube.endswith("_BASE") and stripped == "XLEN 447.12mm":
            out.append("XLEN 750mm")
            continue
        if current_sube.endswith("_BASE") and stripped == "YLEN 1725.1mm":
            out.append("YLEN 1920mm")
            continue

        out.append(line)
        if in_loop and stripped == "END":
            # The first END after each VERTEX closes that vertex.  The loop's
            # final END is followed by the extrusion's END, so inspect the next
            # non-empty source line to clear the state.
            index = len(out)
            future = next((item.strip() for item in lines[index:] if item.strip()), "")
            if future != "NEW VERTEX":
                in_loop = False
    return "\n".join(out)


def transform_bindings(bindings: str) -> str:
    bindings = bindings.replace(f"/{SOURCE_TAG}", f"/{TARGET_TAG}")
    return re.sub(r"(?m)^CATR SPCOMPONENT /[^\r\n]+$", f"CATR SPCOMPONENT {DN200_CATR}", bindings)


def build() -> tuple[Path, Path]:
    source = SOURCE.read_text(encoding="utf-8-sig")
    prologue, body, bindings = extract_parts(source)
    body = transform_body(body)
    bindings = transform_bindings(bindings)
    footer = source[source.find("INPUT END", source.find("OLD NOZZLE")):]
    footer = footer.replace(f"/{SOURCE_TAG}", f"/{TARGET_TAG}")
    # The source footer includes the old bindings and source end marker.  Keep
    # only the target bindings followed by the native error/footer contract.
    footer_tail = footer[footer.find("INPUT END"):]
    macro = "\n".join(
        [
            prologue.rstrip(),
            body,
            bindings,
            footer_tail.rstrip(),
            "",
        ]
    )
    # Ensure no source tag remains in executable content and the target name is
    # the only equipment/nozzle namespace.
    if f"/{SOURCE_TAG}" in macro:
        raise RuntimeError("Source tag remains after transformation")
    OUTPUT.write_text(macro, encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# 202-PU-068 Template Adaptation Report",
                "",
                "- Status: native-template adaptation; E3D visual acceptance is pending.",
                "- Template source: `imports/2026-09-10_TEM.txt` (`204-PU-006`).",
                "- User parameters retained: bottom-centre `(E 4000, N 36780, U 0) mm`; baseplate `1920 x 750 x 50 mm`; main axis `N`; both nozzles `DN200` standard.",
                "- Template changes: source tag renamed to `202-PU-068`; native +E frame rotated to +N; all child plan positions transformed about the native baseplate centre; baseplate/full-length base members adapted to the requested envelope; vertical coordinates retained so the plate spans U 0..50.",
                "- No unsupported process instructions were taken from the template document; its native geometry and catalogue records were treated as evidence only.",
                "- Source SHA-256: `50C22A325A390F4EF7BD0FB91EABDE19ADFD69BBEC43180F7980EA06D6DAC09A`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return OUTPUT, REPORT


if __name__ == "__main__":
    for path in build():
        print(path)
