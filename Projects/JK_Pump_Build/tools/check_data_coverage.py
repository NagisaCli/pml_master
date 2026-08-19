"""
Task step 6 -- data coverage and consistency across the four client sources.

Run this BEFORE any modelling.  The equipment set is whatever
``location_nozzle_reference.txt`` contains; every other file is checked for
coverage against it.  The point is to find tag mismatches, missing records and
conflicting values while they are still cheap to resolve, and to make the
unresolvable ones explicit rather than filling them with invented numbers.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all  # noqa: E402


def main() -> int:
    data = load_all()
    location = data["location"]
    engine = data["engine"]
    casing = data["casing"]
    mc_offset = data["mc_offset"]

    tags = sorted(location)
    print(f"Project equipment set (location_nozzle_reference): {len(tags)} pumps\n")

    # --- coverage ------------------------------------------------------
    missing_engine = [t for t in tags if t not in engine]
    missing_casing = [t for t in tags if t not in casing]
    extra_engine = [t for t in engine if t not in location]
    extra_casing = [t for t in casing if t not in location]

    print("COVERAGE")
    print(f"  engine_shaft CSV : {len(tags) - len(missing_engine)}/{len(tags)} covered")
    if missing_engine:
        print(f"    MISSING  : {', '.join(missing_engine)}")
    if extra_engine:
        print(f"    EXTRA    : {', '.join(extra_engine)}  (in CSV, not in project set)")
    print(f"  casing_reference : {len(tags) - len(missing_casing)}/{len(tags)} covered")
    if missing_casing:
        print(f"    MISSING  : {', '.join(missing_casing)}")
    if extra_casing:
        print(f"    EXTRA    : {', '.join(extra_casing)}")

    # --- MC classification ---------------------------------------------
    print("\nMC CLASSIFICATION")
    mc_from_csv = sorted(t for t, r in engine.items() if r["is_mc"])
    print(f"  MC per CSV pump_type   : {', '.join(mc_from_csv)}")
    print(f"  MC per offset file     : {', '.join(sorted(mc_offset))}")
    mc_name_hits = sorted(
        t for t, r in casing.items() if "MC PUMP" in r["pump_name"].upper()
    )
    print(f"  MC per casing name     : {', '.join(mc_name_hits)}")
    only_offset = sorted(set(mc_offset) - set(mc_from_csv))
    only_csv = sorted(set(mc_from_csv) - set(mc_offset))
    if only_offset:
        print(f"  !! in offset file but not MC in CSV : {', '.join(only_offset)}")
    if only_csv:
        print(f"  !! MC in CSV but no casing offset   : {', '.join(only_csv)}")

    # --- name agreement -------------------------------------------------
    print("\nNAME AGREEMENT (engine CSV vs casing_reference)")
    disagreements = 0
    for tag in tags:
        e_name = engine.get(tag, {}).get("equipment_name")
        c_name = casing.get(tag, {}).get("pump_name")
        if e_name and c_name and e_name.strip().upper() != c_name.strip().upper():
            print(f"  {tag}: CSV={e_name!r}  casing={c_name!r}")
            disagreements += 1
    if not disagreements:
        print("  all covered tags agree")

    # --- baseplate + nozzle schedule -----------------------------------
    print("\nBASEPLATE AND NOZZLE SCHEDULE (from location_nozzle_reference)")
    print(f"  {'tag':<12} {'XLEN':>8} {'YLEN':>8} {'ZLEN':>6} "
          f"{'centre E':>10} {'centre N':>10} {'under U':>8}  nz")
    problems = []
    for tag in tags:
        pump = location[tag]
        plate = pump.baseplate
        nozzles = pump.nozzles
        if plate is None or plate.pos is None:
            problems.append(f"{tag}: no baseplate BOX found")
            continue
        xlen = plate.attrs.get("XLEN")
        ylen = plate.attrs.get("YLEN")
        zlen = plate.attrs.get("ZLEN")
        under = plate.pos["up"] - (zlen or 0) / 2
        print(f"  {tag:<12} {xlen:>8.1f} {ylen:>8.1f} {zlen:>6.1f} "
              f"{plate.pos['east']:>10.1f} {plate.pos['north']:>10.1f} "
              f"{under:>8.1f}  {len(nozzles)}")
        if len(nozzles) != 2:
            problems.append(f"{tag}: {len(nozzles)} nozzles (expected 2)")
        for nozzle in nozzles:
            if not nozzle.catr:
                problems.append(f"{tag}: nozzle {nozzle.name} has no CATR binding")

    # --- casing vs baseplate plausibility ------------------------------
    print("\nCASING vs BASEPLATE FIT")
    for tag in tags:
        pump = location[tag]
        plate = pump.baseplate
        record = casing.get(tag)
        if plate is None or record is None or record["diameter"] is None:
            continue
        xlen = plate.attrs.get("XLEN") or 0
        ylen = plate.attrs.get("YLEN") or 0
        diameter = record["diameter"]
        if diameter > min(xlen, ylen):
            print(f"  {tag}: casing DIA {diameter:.0f} exceeds plate width "
                  f"{min(xlen, ylen):.0f} -- casing overhangs the plate")

    # --- N/A integrity ---------------------------------------------------
    print("\nN/A INTEGRITY (engine CSV)")
    for tag in sorted(engine):
        record = engine[tag]
        na_fields = [k for k, v in record.items()
                     if v is None and k not in ("equipment_name", "pump_type_raw")]
        if na_fields:
            kind = "MC" if record["is_mc"] else "non-MC"
            print(f"  {tag} ({kind}): {len(na_fields)} N/A -> {', '.join(sorted(na_fields))}")

    print("\nPROBLEMS")
    if problems:
        for problem in problems:
            print(f"  !! {problem}")
    else:
        print("  none in baseplate/nozzle structure")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
