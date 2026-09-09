"""Verify one-to-one fidelity and per-machine adaptation of /P1501B-BASE."""

from __future__ import annotations

import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all          # noqa: E402
from build_pumps import build_pump                  # noqa: E402
from base_deform import (ANCHOR_INDICES, LOWER_GUSSET_INDICES,
                         OUTER_STAY_INDICES,
                         REF_MOTOR_MACHINE_N, REF_PLATE_CENTRE_N,
                         REF_PLATE_T, REF_PLATE_UNDER, REF_PUMP_MACHINE_N,
                         SADDLE_GUSSET_INDICES, SOLE_PLATE_INDICES,
                         WASHER_INDICES,
                         orientation_basis, parse_reference, profile_centre,
                         rotate_ori)                # noqa: E402
from verify_pumps import bounds                     # noqa: E402

EXPECTED_KINDS = {"BOX": 11, "PYRAMID": 12,
                  "EXTRUSION": 10, "CYLINDER": 10}
EXPECTED_GROUPS = {"skid": 5, "pump": 17, "motor": 21}
TOL = 0.6


def station_frame(model) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    wet = model.facts["wet_end"]
    along = {"N": (0.0, 1.0), "S": (0.0, -1.0),
             "E": (1.0, 0.0), "W": (-1.0, 0.0)}[wet]
    return ((along[1], -along[0]), along)


def _normalise_ori(value) -> str:
    return " ".join((value or "").upper().split())


def _member_index(note: str) -> int:
    match = re.search(r"/P1501B-BASE element (\d+):", note)
    return int(match.group(1)) if match else -1


def _local_factor(reference, station_scales, axis: str) -> float:
    vector = orientation_basis(reference.ori)[axis]
    across, along = station_scales
    return math.sqrt((vector[0] * across) ** 2
                     + (vector[1] * along) ** 2)


def _close(problems: List[str], index: int, label: str,
           actual: float, expected: float, tolerance: float = TOL) -> None:
    if abs(actual - expected) > tolerance:
        problems.append(
            f"element {index} {label}: {actual:.3f} != {expected:.3f}")


def _check_hex(index: int, profile, problems: List[str]) -> None:
    if not profile:
        problems.append(f"element {index} has no hex washer profile")
        return
    vertices = list(profile)
    if len(vertices) > 1 and all(abs(vertices[0][axis] - vertices[-1][axis]) < TOL
                                 for axis in (0, 1)):
        vertices = vertices[:-1]
    unique = {(round(x, 3), round(y, 3)) for x, y in vertices}
    if len(unique) != 6:
        problems.append(f"element {index} washer has {len(unique)} unique vertices, expected 6")
        return
    edges = [math.dist(vertices[i], vertices[(i + 1) % len(vertices)])
             for i in range(len(vertices))]
    if max(edges) - min(edges) > TOL:
        problems.append(
            f"element {index} washer is not a regular hexagon: edge range "
            f"{min(edges):.2f}..{max(edges):.2f}")


def _profile_world_centre(member) -> Tuple[float, float]:
    local_x, local_y = profile_centre(member.profile or [])
    basis = orientation_basis(member.ori)
    return (member.east + basis["X"][0] * local_x
            + basis["Y"][0] * local_y,
            member.north + basis["X"][1] * local_x
            + basis["Y"][1] * local_y)


def _station(member) -> str:
    return member.note.rsplit("(", 1)[-1].split(" station", 1)[0]


def _face_plan_bounds(member, top: bool) -> Tuple[Tuple[float, float],
                                                   Tuple[float, float]]:
    """Exact E/N bounds of a horizontal BOX or PYRAMID end face."""
    if member.kind == "BOX":
        return bounds(member)[:2]
    if member.kind != "PYRAMID":
        raise ValueError(f"no horizontal bearing-face model for {member.kind}")
    suffix = "TOP" if top else "BOT"
    half_x = member.attrs[f"X{suffix}"] / 2
    half_y = member.attrs[f"Y{suffix}"] / 2
    offset_x = member.attrs.get("XOFF", 0.0) if top else 0.0
    offset_y = member.attrs.get("YOFF", 0.0) if top else 0.0
    basis = orientation_basis(member.ori)
    corners = []
    for local_x, local_y in ((-half_x, -half_y), (-half_x, half_y),
                             (half_x, half_y), (half_x, -half_y)):
        local_x += offset_x
        local_y += offset_y
        corners.append((
            member.east + basis["X"][0] * local_x
            + basis["Y"][0] * local_y,
            member.north + basis["X"][1] * local_x
            + basis["Y"][1] * local_y,
        ))
    return ((min(point[0] for point in corners),
             max(point[0] for point in corners)),
            (min(point[1] for point in corners),
             max(point[1] for point in corners)))


def _bearing_contact(lower, upper, tolerance: float = TOL) -> bool:
    """True when two horizontal end faces meet and overlap in plan."""
    if abs(bounds(lower)[2][1] - bounds(upper)[2][0]) > tolerance:
        return False
    lower_face = _face_plan_bounds(lower, top=True)
    upper_face = _face_plan_bounds(upper, top=False)
    overlap_e = (min(lower_face[0][1], upper_face[0][1])
                 - max(lower_face[0][0], upper_face[0][0]))
    overlap_n = (min(lower_face[1][1], upper_face[1][1])
                 - max(lower_face[1][0], upper_face[1][0]))
    return overlap_e > tolerance and overlap_n > tolerance


def check(model, reference) -> List[str]:
    problems: List[str] = []
    base = [p for p in model.primitives if p.sube == "BASE"]

    if any(p.sube == "BASEPLATE" for p in model.primitives):
        problems.append("a duplicate BASEPLATE exists outside the 43-member reference base")

    kinds = Counter(member.kind for member in base)
    groups = Counter(
        member.note.rsplit("(", 1)[-1].split(" station", 1)[0]
        for member in base if " station)" in member.note)
    for kind, count in EXPECTED_KINDS.items():
        if kinds[kind] != count:
            problems.append(f"{kinds[kind]} {kind} against the reference's {count}")
    for group, count in EXPECTED_GROUPS.items():
        if groups[group] != count:
            problems.append(f"{groups[group]} members in {group}, expected {count}")

    placed = {_member_index(member.note): member for member in base}
    if set(placed) != set(range(1, 44)):
        missing = sorted(set(range(1, 44)) - set(placed))
        extra = sorted(set(placed) - set(range(1, 44)))
        problems.append(f"reference member identity mismatch: missing={missing}, extra={extra}")
        return problems

    reference_by_index = {element.index: element for element in reference}
    across_vector, along_vector = station_frame(model)
    plate_e, plate_n = model.facts["plate_centre"]
    scales: Dict[str, Tuple[float, float]] = model.facts["base_adapter"]
    targets = model.facts["base_station_targets"]
    origins = {"skid": REF_PLATE_CENTRE_N,
               "pump": REF_PUMP_MACHINE_N,
               "motor": REF_MOTOR_MACHINE_N}
    plate_scale = model.facts["plate"][2] / REF_PLATE_T

    for index in range(1, 44):
        member = placed[index]
        ref = reference_by_index[index]
        if member.kind != ref.kind:
            problems.append(
                f"element {index} kind {member.kind}, reference {ref.kind}")
            continue
        expected_ori = rotate_ori(ref.ori, model.facts["wet_end"])
        if _normalise_ori(member.ori) != _normalise_ori(expected_ori):
            problems.append(
                f"element {index} ORI {_normalise_ori(member.ori)!r}, "
                f"expected {_normalise_ori(expected_ori)!r}")

        delta_e = member.east - plate_e
        delta_n = member.north - plate_n
        actual_across = delta_e * across_vector[0] + delta_n * across_vector[1]
        actual_along = delta_e * along_vector[0] + delta_n * along_vector[1]
        station_scale = scales[ref.station]
        if ref.kind != "EXTRUSION":
            expected_across = ref.pos["east"] * station_scale[0]
            expected_along = (targets[ref.station]
                              + (ref.pos["north"] - origins[ref.station])
                              * station_scale[1])
            _close(problems, index, "across position",
                   actual_across, expected_across)
            _close(problems, index, "along position",
                   actual_along, expected_along)

        sx = _local_factor(ref, station_scale, "X")
        sy = _local_factor(ref, station_scale, "Y")
        if ref.kind == "BOX":
            _close(problems, index, "XLEN", member.attrs["XLEN"],
                   ref.attrs["XLEN"] * sx)
            _close(problems, index, "YLEN", member.attrs["YLEN"],
                   ref.attrs["YLEN"] * sy)
            _close(problems, index, "ZLEN", member.attrs["ZLEN"],
                   ref.attrs["ZLEN"] * plate_scale)
        elif ref.kind == "PYRAMID":
            x_plate = abs(ref.attrs["XBOT"] - ref.attrs["XTOP"]) < 0.01
            y_plate = abs(ref.attrs["YBOT"] - ref.attrs["YTOP"]) < 0.01
            xfactor = plate_scale if x_plate else sx
            yfactor = plate_scale if y_plate else sy
            for key, factor in (("XBOT", xfactor), ("XTOP", xfactor),
                                ("YBOT", yfactor), ("YTOP", yfactor)):
                _close(problems, index, key, member.attrs[key],
                       ref.attrs[key] * factor)
            if "XOFF" in ref.attrs:
                _close(problems, index, "XOFF", member.attrs.get("XOFF", 0),
                       ref.attrs["XOFF"] * sx)
            if "YOFF" in ref.attrs:
                _close(problems, index, "YOFF", member.attrs.get("YOFF", 0),
                       ref.attrs["YOFF"] * sy)
        elif ref.kind == "CYLINDER":
            _close(problems, index, "DIAM", member.attrs["DIAM"],
                   ref.attrs["DIAM"] * plate_scale)
        elif ref.kind == "EXTRUSION":
            _close(problems, index, "HEIG", member.attrs["HEIG"],
                   ref.attrs["HEIG"] * plate_scale)
            if len(member.profile or []) != len(ref.profile):
                problems.append(
                    f"element {index} profile has {len(member.profile or [])} "
                    f"vertices, expected {len(ref.profile)}")
            else:
                for vertex, (actual, expected) in enumerate(
                        zip(member.profile or [], ref.profile), start=1):
                    _close(problems, index, f"vertex {vertex} X", actual[0],
                           expected[0] * plate_scale)
                    _close(problems, index, f"vertex {vertex} Y", actual[1],
                           expected[1] * plate_scale)
            _check_hex(index, member.profile, problems)

    # A taper offset must lean toward the machine centreline, never away from
    # it. This relational property is independent of the adapter's mapping
    # formula and catches a position/ORI mirror like the client's E3D view.
    for member in (item for item in base if item.kind == "PYRAMID"):
        xoff = member.attrs.get("XOFF", 0.0)
        yoff = member.attrs.get("YOFF", 0.0)
        if abs(xoff) + abs(yoff) < TOL:
            continue
        basis = orientation_basis(member.ori)
        top_e = member.east + basis["X"][0] * xoff + basis["Y"][0] * yoff
        top_n = member.north + basis["X"][1] * xoff + basis["Y"][1] * yoff
        base_across = ((member.east - plate_e) * across_vector[0]
                       + (member.north - plate_n) * across_vector[1])
        top_across = ((top_e - plate_e) * across_vector[0]
                      + (top_n - plate_n) * across_vector[1])
        if abs(top_across) > abs(base_across) + TOL:
            problems.append(
                f"element {_member_index(member.note)} PYRAMID leans outward: "
                f"across {base_across:.2f} -> {top_across:.2f}")

    # EXTRUSION POS is an off-origin LOOP datum. Match physical hex centres to
    # anchor-cylinder axes one-to-one instead of comparing their raw POS lines.
    sole_tops: Dict[str, float] = {}
    for index in SOLE_PLATE_INDICES:
        member = placed[index]
        low, high = bounds(member)[2]
        _close(problems, index, "sole bottom", low, model.facts["plate_top"])
        sole_tops[_station(member)] = max(
            sole_tops.get(_station(member), -math.inf), high)

    for index in LOWER_GUSSET_INDICES:
        member = placed[index]
        _close(problems, index, "lower gusset bottom", bounds(member)[2][0],
               sole_tops[_station(member)])

    pad_by_station = {"pump": placed[1], "motor": placed[13]}
    for index in LOWER_GUSSET_INDICES:
        member = placed[index]
        pad = pad_by_station[_station(member)]
        _close(problems, index, "lower gusset/top-plate interface",
               bounds(member)[2][1], bounds(pad)[2][0])

    for index in OUTER_STAY_INDICES:
        member = placed[index]
        _close(problems, index, "outer stay bottom", bounds(member)[2][0],
               sole_tops[_station(member)])

    pad_top = bounds(placed[1])[2][1]
    for index in SADDLE_GUSSET_INDICES:
        _close(problems, index, "saddle bottom", bounds(placed[index])[2][0],
               pad_top)

    washers = [placed[index] for index in sorted(WASHER_INDICES)]
    unused_bolts = [placed[index] for index in sorted(ANCHOR_INDICES)]
    reference_anchor = reference_by_index[min(ANCHOR_INDICES)]
    reference_anchor_bottom = (
        reference_anchor.pos["up"] - reference_anchor.attrs["HEIG"] / 2)
    anchor_bottom = (model.facts["plate_under"]
                     + (reference_anchor_bottom - REF_PLATE_UNDER)
                     * plate_scale)
    if len(washers) != len(unused_bolts):
        problems.append(
            f"hardware count mismatch: {len(washers)} washers / "
            f"{len(unused_bolts)} anchor cylinders")
    else:
        for washer in washers:
            washer_box = bounds(washer)
            _close(problems, _member_index(washer.note), "hex bearing face",
                   washer_box[2][0], sole_tops[_station(washer)])
            centre = _profile_world_centre(washer)
            bolt = min(unused_bolts, key=lambda item: math.hypot(
                item.east - centre[0], item.north - centre[1]))
            distance = math.hypot(bolt.east - centre[0],
                                  bolt.north - centre[1])
            if distance > TOL:
                problems.append(
                    f"element {_member_index(washer.note)} hex centre is "
                    f"{distance:.3f} mm from anchor element "
                    f"{_member_index(bolt.note)}")
            bolt_box = bounds(bolt)
            _close(problems, _member_index(bolt.note), "anchor embedment",
                   bolt_box[2][0], anchor_bottom)
            _close(problems, _member_index(bolt.note), "anchor/head top",
                   bolt_box[2][1], washer_box[2][1])
            unused_bolts.remove(bolt)

    # Structural primitives must form one continuous component back to the
    # five-member skid without using anchor shanks as artificial bridges. Use
    # explicit end-face bearings for the fabricated support chain; an AABB
    # intersection between crossing tapers does not prove physical seating.
    structure = {index: placed[index] for index in range(1, 20)}
    structure.update({index: placed[index] for index in range(40, 44)})
    adjacency = {index: set() for index in structure}
    bearing_pairs = (
        (2, 10), (2, 3), (40, 10), (40, 11), (40, 3), (40, 12),
        (41, 11), (41, 12),
        (10, 7), (11, 8), (3, 6), (12, 9),
        (7, 1), (8, 1), (6, 13), (9, 13),
        (1, 4), (1, 5),
        (3, 14), (12, 17), (3, 18), (12, 19),
        (10, 15), (11, 16),
    )
    for lower_index, upper_index in bearing_pairs:
        if _bearing_contact(placed[lower_index], placed[upper_index]):
            adjacency[lower_index].add(upper_index)
            adjacency[upper_index].add(lower_index)
        else:
            problems.append(
                f"bearing faces do not meet: element {lower_index} top / "
                f"element {upper_index} bottom")
    # The five native skid members are the root assembly. Their own lateral
    # weld/edge relationships are inherited and need not be bridged by a PYRA.
    for first in (2, 40, 41, 42, 43):
        for second in (2, 40, 41, 42, 43):
            if first != second:
                adjacency[first].add(second)
    connected = set()
    pending = [2, 40, 41, 42, 43]
    while pending:
        index = pending.pop()
        if index in connected:
            continue
        connected.add(index)
        pending.extend(adjacency.get(index, set()) - connected)
    detached = sorted(set(structure) - connected)
    if detached:
        problems.append(
            f"structural load path is detached from the skid: {detached}")

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
            for problem in problems[:30]:
                print(f"        - {problem}")
            if len(problems) > 30:
                print(f"        ... and {len(problems) - 30} more")
    print(f"{len(tags)} pumps checked, {failures} reference-fidelity problems")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
