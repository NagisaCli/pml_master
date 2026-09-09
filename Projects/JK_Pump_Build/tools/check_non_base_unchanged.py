"""Prove that r6 changed only /P1501B-BASE-derived subequipment."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OLD = (REPO / "Projects" / "JK_Pump_Build" / "output" /
       "2026-08-19_pumps_r5" /
       "JK_Pump_Build_2026-08-19_base_rebuild_r5_all_pumps.pml")
NEW = (REPO / "Projects" / "JK_Pump_Build" / "output" /
       "2026-08-19_pumps_r6" /
       "JK_Pump_Build_2026-08-19_base_rebuild_r6_all_pumps.pml")


def blocks(path: Path):
    result = {}
    equipment = None
    sube = None
    lines = []

    def flush():
        if equipment and sube and not sube.endswith(("_BASE", "_BASEPLATE")):
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
        elif sube:
            lines.append(line)
    flush()
    return result


def main() -> int:
    old = blocks(OLD)
    new = blocks(NEW)
    missing = sorted(set(old) - set(new))
    extra = sorted(set(new) - set(old))
    changed = sorted(key for key in old.keys() & new.keys()
                     if old[key] != new[key])
    print(f"old non-base blocks: {len(old)}")
    print(f"new non-base blocks: {len(new)}")
    print(f"missing: {len(missing)}, extra: {len(extra)}, changed: {len(changed)}")
    for label, items in (("missing", missing), ("extra", extra),
                         ("changed", changed)):
        for item in items[:20]:
            print(f"  {label}: {item[0]} / {item[1]}")
    if missing or extra or changed:
        return 1
    print("NON_BASE_BLOCKS=UNCHANGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
