"""Prove r12 changes only top-nozzle HEIG and overwidth casing connectors."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OLD = (REPO / "Projects" / "JK_Pump_Build" / "output" /
       "2026-08-20_motor_drive_r9" /
       "JK_Pump_Build_2026-08-20_motor_drive_r9_all_pumps.pml")
NEW = (REPO / "Projects" / "JK_Pump_Build" / "output" /
       "2026-08-20_top_nozzle_r12" /
       "JK_Pump_Build_2026-08-20_top_nozzle_r12_all_pumps.pml")

ELEMENT = re.compile(r"^NEW (?:BOX|CYLINDER|CONE|DISH|PYRAMID|EXTRUSION|NOZZLE)\b")
NUMBER = r"(-?[\d.]+)"


def subequipment_blocks(path: Path) -> dict[tuple[str, str], list[str]]:
    result: dict[tuple[str, str], list[str]] = {}
    equipment = None
    sube = None
    lines: list[str] = []

    def flush() -> None:
        if equipment and sube:
            result[(equipment, sube)] = list(lines)

    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line.startswith(("NEW EQUIPMENT ", "NEW EQUI ")):
            flush()
            equipment = line.split("/", 1)[-1]
            sube = None
            lines = []
        elif line.startswith(("NEW SUBEQUIPMENT ", "NEW SUBE ")):
            flush()
            sube = line.split("/", 1)[-1]
            lines = [line]
        elif sube and not line.startswith("--"):
            lines.append(line)
    flush()
    return result


def elements(lines: list[str]) -> list[str]:
    """Canonical top-level element chunks in one flat pump SUBE."""
    chunks: list[list[str]] = []
    current: list[str] | None = None
    for line in lines[1:]:
        if ELEMENT.match(line):
            if current:
                chunks.append(current)
            current = [line]
        elif current is not None:
            current.append(line)
    if current:
        chunks.append(current)
    return ["\n".join(chunk).strip() for chunk in chunks]


def _without_nozzle_heig(chunk: str) -> str:
    return "\n".join("HEIG <ADAPTED>" if line.startswith("HEIG ") else line
                     for line in chunk.splitlines())


def _heig(chunk: str) -> str | None:
    return next((line for line in chunk.splitlines() if line.startswith("HEIG ")),
                None)


def _value(chunk: str, pattern: str) -> float:
    match = re.search(pattern, chunk, re.MULTILINE | re.IGNORECASE)
    if not match:
        raise ValueError(f"missing emitted value {pattern!r} in:\n{chunk}")
    return float(match.group(1))


def _vertical_top(chunk: str) -> float | None:
    if not re.search(r"^ORI Z is U\b", chunk, re.MULTILINE | re.IGNORECASE):
        return None
    up = _value(chunk, rf"^POS .*\bU {NUMBER}mm$")
    height = _value(chunk, rf"^HEIG {NUMBER}mm$")
    return up + height / 2.0


def _nozzle_root(chunk: str) -> float:
    face_u = _value(chunk, rf"^POS .*\bU {NUMBER}mm$")
    height = _value(chunk, rf"^HEIG {NUMBER}mm$")
    return face_u - height


def _casing_crown(chunk: str) -> float:
    centre_u = _value(chunk, rf"^POS .*\bU {NUMBER}mm$")
    diameter = _value(chunk, rf"^DIAM {NUMBER}mm$")
    return centre_u + diameter / 2.0


def main() -> int:
    old = subequipment_blocks(OLD)
    new = subequipment_blocks(NEW)
    missing = set(old) - set(new)
    extra_blocks = set(new) - set(old)
    illegal: list[str] = []
    changed_casing = 0
    changed_top_nozzles = 0
    added_primitives = 0
    connector_tops: dict[str, float] = {}
    nozzle_roots: dict[str, float] = {}
    nozzle_faces: dict[str, float] = {}
    nozzle_heights: dict[str, float] = {}
    casing_crowns: dict[str, float] = {}

    for key in sorted(old.keys() & new.keys()):
        old_lines = old[key]
        new_lines = new[key]
        equipment, sube = key
        if sube.endswith("_CASING"):
            old_elements = elements(old_lines)
            if old_elements:
                casing_crowns[equipment] = _casing_crown(old_elements[0])
        if old_lines == new_lines:
            continue
        if sube.endswith("_CASING"):
            new_elements = elements(new_lines)
            if new_elements[:len(old_elements)] != old_elements:
                illegal.append(f"existing CASING geometry changed: {equipment} / {sube}")
                continue
            additions = new_elements[len(old_elements):]
            if not additions:
                illegal.append(f"CASING changed without additive primitives: {equipment}")
                continue
            changed_casing += 1
            added_primitives += len(additions)
            vertical_tops = [value for value in
                             (_vertical_top(chunk) for chunk in additions)
                             if value is not None]
            if not vertical_tops:
                illegal.append(f"no emitted vertical connector: {equipment}")
            else:
                connector_tops[equipment] = max(vertical_tops)
            continue

        if sube.endswith("_DISCHARGE"):
            old_elements = elements(old_lines)
            new_elements = elements(new_lines)
            if (len(old_elements) != 1 or len(new_elements) != 1
                    or not old_elements[0].startswith("NEW NOZZLE")
                    or not new_elements[0].startswith("NEW NOZZLE")):
                illegal.append(f"unexpected DISCHARGE structure: {equipment} / {sube}")
                continue
            if _without_nozzle_heig(old_elements[0]) != _without_nozzle_heig(new_elements[0]):
                illegal.append(
                    f"top NOZZLE changed outside HEIG: {equipment} / {sube}")
                continue
            if _heig(old_elements[0]) == _heig(new_elements[0]):
                illegal.append(f"top NOZZLE HEIG did not adapt: {equipment} / {sube}")
                continue
            changed_top_nozzles += 1
            nozzle_roots[equipment] = _nozzle_root(new_elements[0])
            nozzle_faces[equipment] = _value(
                new_elements[0], rf"^POS .*\bU {NUMBER}mm$")
            nozzle_heights[equipment] = _value(
                new_elements[0], rf"^HEIG {NUMBER}mm$")
            continue

        illegal.append(f"changed non-target block: {equipment} / {sube}")

    if missing:
        illegal.extend(f"missing block: {item}" for item in sorted(missing))
    if extra_blocks:
        illegal.extend(f"extra block: {item}" for item in sorted(extra_blocks))
    if changed_casing != 14:
        illegal.append(f"changed CASING count {changed_casing}, expected 14")
    if changed_top_nozzles != 28:
        illegal.append(f"changed top-NOZZLE count {changed_top_nozzles}, expected 28")
    if added_primitives != 29:
        illegal.append(f"added primitive count {added_primitives}, expected 29")
    terminal_differences = {
        equipment: nozzle_roots[equipment] - connector_tops[equipment]
        for equipment in sorted(nozzle_roots.keys() & connector_tops.keys())
    }
    for equipment, difference in terminal_differences.items():
        if abs(difference) > 0.011:
            illegal.append(
                f"emitted terminal gap/overlap {difference:.3f} mm: {equipment}")
    if len(terminal_differences) != 14:
        illegal.append(
            f"emitted terminal closure count {len(terminal_differences)}, expected 14")

    direct_equipment = sorted(nozzle_roots.keys() - connector_tops.keys())
    direct_ratios: dict[str, float] = {}
    for equipment in direct_equipment:
        crown = casing_crowns.get(equipment)
        if crown is None:
            illegal.append(f"missing emitted casing crown: {equipment}")
            continue
        root = nozzle_roots[equipment]
        if root >= crown - 0.011:
            illegal.append(
                f"direct nozzle does not penetrate casing crown: {equipment}")
        ratio = ((nozzle_faces[equipment] - crown)
                 / nozzle_heights[equipment])
        direct_ratios[equipment] = ratio
        if ratio < 0.70 - 0.001:
            illegal.append(
                f"direct nozzle external ratio {ratio:.4f} below 0.70: {equipment}")
    if len(direct_ratios) != 14:
        illegal.append(
            f"direct nozzle projection count {len(direct_ratios)}, expected 14")

    print(f"r9 blocks: {len(old)}; r12 blocks: {len(new)}")
    print(f"top-discharge CASING blocks changed: {changed_casing}")
    print(f"top-discharge NOZZLE HEIG fields changed: {changed_top_nozzles}")
    print(f"additive casing primitives: {added_primitives}")
    if terminal_differences:
        print(f"emitted overwidth terminal closures: {len(terminal_differences)}/14; "
              f"signed range {min(terminal_differences.values()):.3f}.."
              f"{max(terminal_differences.values()):.3f} mm")
    if direct_ratios:
        print(f"emitted direct-nozzle external ratios: {len(direct_ratios)}/14; "
              f"range {min(direct_ratios.values()):.4f}.."
              f"{max(direct_ratios.values()):.4f}")
    if illegal:
        for problem in illegal:
            print(f"ILLEGAL_DELTA: {problem}")
        return 1
    print("NOZZLE_CATR_POS_ORI=60/60 UNCHANGED")
    print("HORIZONTAL_NOZZLE_BLOCKS=32/32 UNCHANGED")
    print("TOP_NOZZLE_HEIG=28/28 AUTHORISED_ADAPTATION")
    print("EXISTING_CASING_GEOMETRY=UNCHANGED")
    print("NON_TARGET_CANONICAL=UNCHANGED")
    print("AUTHORISED_SCOPE=TOP_NOZZLE_HEIG_PLUS_OVERWIDTH_CASING_CONNECTORS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
