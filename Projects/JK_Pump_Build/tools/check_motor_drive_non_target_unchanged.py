"""Prove r9 changes only DRIVER tail construction from r8."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OLD = (REPO / "Projects" / "JK_Pump_Build" / "output" /
       "2026-08-20_motor_drive_r8" /
       "JK_Pump_Build_2026-08-20_motor_drive_r8_all_pumps.pml")
NEW = (REPO / "Projects" / "JK_Pump_Build" / "output" /
       "2026-08-20_motor_drive_r9" /
       "JK_Pump_Build_2026-08-20_motor_drive_r9_all_pumps.pml")


def blocks(path: Path) -> dict[tuple[str, str], str]:
    result: dict[tuple[str, str], str] = {}
    equipment = None
    sube = None
    lines: list[str] = []

    def flush() -> None:
        if equipment and sube:
            result[(equipment, sube)] = "\n".join(lines).strip()

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


def _tag(equipment: str) -> str:
    return equipment.removesuffix("_EQUIPMENT").replace("_PU_", "-PU-")


def authorised(key: tuple[str, str]) -> bool:
    _, sube = key
    return sube.endswith("_DRIVER")


def main() -> int:
    old = blocks(OLD)
    new = blocks(NEW)
    changed = {key for key in old.keys() & new.keys() if old[key] != new[key]}
    missing = set(old) - set(new)
    extra = set(new) - set(old)
    illegal = sorted(key for key in changed | missing | extra if not authorised(key))

    print(f"r8 blocks: {len(old)}; r9 blocks: {len(new)}")
    print(f"changed: {len(changed)}; missing: {len(missing)}; extra: {len(extra)}")
    if illegal:
        for equipment, sube in illegal:
            print(f"ILLEGAL_DELTA: {equipment} / {sube}")
        return 1
    print("NON_TARGET_CANONICAL=UNCHANGED")
    print("AUTHORISED_SCOPE=DRIVER_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
