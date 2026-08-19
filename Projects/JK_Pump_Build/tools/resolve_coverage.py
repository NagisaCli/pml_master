"""
Resolve the coverage gaps found by ``check_data_coverage.py``.

The task allows using tag + pump name + pump type + other project data to work
out the correct relationship when sources disagree.  It also forbids inventing
dimensions to complete a model.  This script separates the two: it reports
which gaps are *resolvable by evidence* and which are genuinely unresolved.

Every candidate match is printed with the evidence for it, so a match is never
applied silently.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all  # noqa: E402


def main() -> int:
    data = load_all()
    location, engine, casing, mc_offset = (
        data["location"], data["engine"], data["casing"], data["mc_offset"]
    )
    tags = sorted(location)

    print("=" * 72)
    print("GAP 1 -- casing_reference carries 204-PU-028, the project set does not")
    print("=" * 72)
    record = casing.get("204-PU-028")
    print(f"  casing row      : {record}")
    print(f"  in MC offsets   : {'204-PU-028' in mc_offset}"
          f"  ({mc_offset.get('204-PU-028')} mm)")
    print(f"  in engine CSV   : {'204-PU-028' in engine}")
    print(f"  in project set  : {'204-PU-028' in location}")
    print("  Nearby project tags in the same 204 series:")
    for tag in tags:
        if tag.startswith("204-"):
            name = (engine.get(tag, {}).get("equipment_name")
                    or casing.get(tag, {}).get("pump_name") or "?")
            print(f"    {tag}: {name}")
    print("""
  VERDICT: not a tag typo for any project pump.  Its service name
  'POST OXYGEN WASHER DISCHARGE MC PUMP' is distinct from every 204-series
  pump in the project set, and it is the only tag carrying BOTH a casing row
  and an MC casing offset while being absent from the equipment set.  It is a
  pump that exists in the client's casing/MC data but is NOT in the project
  scope defined by location_nozzle_reference.txt.  Excluded from modelling and
  reported.""")

    print("=" * 72)
    print("GAP 2 -- project pumps with no casing_reference row")
    print("=" * 72)
    for tag in tags:
        if tag in casing:
            continue
        record = engine.get(tag)
        name = record["equipment_name"] if record else None
        print(f"  {tag}: engine CSV name = {name!r}")
        if name:
            twins = sorted(
                t for t, c in casing.items()
                if c["pump_name"].strip().upper() == name.strip().upper()
            )
            print(f"      same service name in casing_reference: {twins or 'none'}")

    print("""
  VERDICT:
    205-PU-046 (D1 WASHER FRONT DILUTION PUMP) and
    205-PU-047 (D1 FILTRATE PUMP) and
    205-PU-048 (D1 TOWER TOP DILUTION PUMP)
      -- have engine/shaft data but NO casing row and no same-named casing
         twin.  Casing diameter/height are UNRESOLVED for these three.
    203-PU-020, 205-PU-004
      -- absent from engine CSV *and* casing_reference.  Only the baseplate,
         position and nozzle schedule are known.""")

    print("=" * 72)
    print("GAP 3 -- project pumps with no engine/shaft CSV row")
    print("=" * 72)
    for tag in tags:
        if tag in engine:
            continue
        record = casing.get(tag)
        print(f"  {tag}: casing row = {record}")

    print("""
  VERDICT:
    203-PU-026 (OXIDISED WL BOOSTER PUMP) has a casing row (361 x 81) but no
      motor/shaft record.  Casing is known; motor and shaft are UNRESOLVED.
    203-PU-020 and 205-PU-004 have neither.""")

    print("=" * 72)
    print("GAP 4 -- MC classification conflict")
    print("=" * 72)
    print("  MC per engine CSV pump_type : 205-PU-018, 205-PU-038, 205-PU-054")
    print("  MC per casing service name  : + 204-PU-028")
    print("  MC per casing-offset file   : + 204-PU-028")
    print("""
  VERDICT: no conflict inside the project scope.  All three sources agree that
  the project's MC pumps are 205-PU-018, 205-PU-038 and 205-PU-054.  The extra
  204-PU-028 is consistently MC in both files that mention it, and is simply
  out of scope (Gap 1).  Every in-scope MC pump has a casing offset.""")

    print("=" * 72)
    print("BUILD CLASSIFICATION")
    print("=" * 72)
    full, partial, minimal = [], [], []
    for tag in tags:
        has_engine = tag in engine
        has_casing = tag in casing
        if has_engine and has_casing:
            full.append(tag)
        elif has_engine or has_casing:
            partial.append(tag)
        else:
            minimal.append(tag)
    print(f"  FULL data (baseplate+nozzles+casing+motor/shaft) : {len(full)}")
    print(f"    {', '.join(full)}")
    print(f"  PARTIAL (one dimensional source missing)         : {len(partial)}")
    print(f"    {', '.join(partial)}")
    print(f"  MINIMAL (baseplate + nozzles only)               : {len(minimal)}")
    print(f"    {', '.join(minimal)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
