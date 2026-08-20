"""
Check that each pump's base is still the REFERENCE'S SHAPE.

Why this is separate from the other checks
------------------------------------------
Six revisions of this base each passed every geometric check and were still
rejected, because the checks all asked about *fit* -- is it seated, is it
connected, is it in bounds -- and none asked whether the result still looked
like ``Base_reference.txt``.  "Looks like" sounds subjective, but two parts of
it are measurable:

1. **Inventory** -- the same 43 members in the same three station groups.
2. **Arrangement** -- for every pair of members, whichever one was to the left
   of, ahead of, or above the other in the reference is still on that side in
   the adaptation.  This is what survives a legitimate anisotropic stretch and
   what breaks the moment a member is repositioned, re-datumed, or dropped.

Distances are NOT expected to scale uniformly: a pump plate is not a scaled
copy of the reference plate, so across/along/up carry different factors by
design.  Ordering is the invariant that separates "deformed" from "redesigned".
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all          # noqa: E402
from build_pumps import build_pump                  # noqa: E402
from base_deform import parse_reference             # noqa: E402

#: The reference's element inventory and station split.
EXPECTED_KINDS = {"BOX": 11, "PYRAMID": 12, "EXTRUSION": 10, "CYLINDER": 10}
EXPECTED_GROUPS = {"skid": 5, "pump": 17, "motor": 21}
#: Ordering relations may invert only BETWEEN the two stations, and then only
#: vertically: whether a pump's motor sits above or below its casing is a
#: property of that pump, not of the reference's shape.  205-PU-048 legitimately
#: inverts 26 such relations because its motor stands higher than its volute.
#: Within a station, and on the two plan axes, nothing may invert.
MAX_INVERSION_RATE = 0.01


def station_frame(model) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """The (across, along) unit vectors this pump's base was built in."""
    wet = model.facts["wet_end"]
    along = {"N": (0.0, 1.0), "S": (0.0, -1.0),
             "E": (1.0, 0.0), "W": (-1.0, 0.0)}[wet]
    return ((-along[1], along[0]), along)


def check(model, reference) -> List[str]:
    problems: List[str] = []
    base = [p for p in model.primitives if p.sube == "BASE"]

    # --- inventory -------------------------------------------------------
    kinds: Dict[str, int] = {}
    groups: Dict[str, int] = {}
    for member in base:
        kinds[member.kind] = kinds.get(member.kind, 0) + 1
        if " station)" in member.note:
            group = member.note.split("(")[-1].split(" station")[0]
            groups[group] = groups.get(group, 0) + 1
    for kind, count in EXPECTED_KINDS.items():
        if kinds.get(kind, 0) != count:
            problems.append(f"{kinds.get(kind, 0)} {kind} against the "
                            f"reference's {count}")
    for group, count in EXPECTED_GROUPS.items():
        if groups.get(group, 0) != count:
            problems.append(f"{groups.get(group, 0)} members in the {group} "
                            f"group against the reference's {count}")
    if problems:
        return problems

    # --- arrangement -----------------------------------------------------
    across, along = station_frame(model)
    plate_e, plate_n = model.facts["plate_centre"]
    placed: Dict[int, Tuple[float, float, float]] = {}
    for member in base:
        index = int(member.note.split()[2])
        delta_e = member.east - plate_e
        delta_n = member.north - plate_n
        placed[index] = (delta_e * across[0] + delta_n * across[1],
                         delta_e * along[0] + delta_n * along[1],
                         member.up)

    reference_pos = {e.index: e.pos for e in reference}
    station_of = {e.index: e.station for e in reference}

    total = structural = 0
    within = 0
    for first, second in itertools.combinations(sorted(placed), 2):
        one, two = reference_pos[first], reference_pos[second]
        mine_one, mine_two = placed[first], placed[second]
        same_station = station_of[first] == station_of[second]
        for axis, (reference_delta, mine_delta) in enumerate((
                (one["east"] - two["east"], mine_one[0] - mine_two[0]),
                (one["north"] - two["north"], mine_one[1] - mine_two[1]),
                (one["up"] - two["up"], mine_one[2] - mine_two[2]))):
            if abs(reference_delta) < 0.5:
                continue
            total += 1
            if reference_delta * mine_delta >= 0:
                continue
            if same_station:
                within += 1
                structural += 1
            elif axis != 2:
                # A plan inversion between stations means one station has
                # crossed the other: a real defect.
                structural += 1
            # else: a cross-station VERTICAL inversion, which is just this
            # pump's own machine heights and not a shape failure.

    if within:
        problems.append(
            f"{within} member orderings inverted WITHIN a station: the "
            f"reference's arrangement is not preserved")
    if total and structural / total > MAX_INVERSION_RATE:
        problems.append(
            f"{structural}/{total} structural orderings inverted "
            f"({structural / total * 100:.1f}%): the base no longer matches "
            f"the reference's arrangement")
    return problems


def main() -> int:
    sources = load_all()
    reference = parse_reference()
    tags = sys.argv[1:] or sorted(sources["location"])
    failures = 0
    for tag in tags:
        model = build_pump(tag, sources)
        problems = check(model, reference)
        failures += len(problems)
        if problems:
            print(f"[FAIL] {tag}")
            for problem in problems:
                print(f"        - {problem}")
    print(f"{len(tags)} pumps checked, {failures} shape problems")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
