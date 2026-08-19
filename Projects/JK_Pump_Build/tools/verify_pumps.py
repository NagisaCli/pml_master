"""
Verify the generated pump models numerically.

Two kinds of check are mixed here deliberately, because the 2026-08-18
post-mortem in this project showed that a verifier built from the generator's
own premise can only confirm the premise was applied consistently:

* **Absolute** checks -- a value against project data (baseplate size, nozzle
  plan position, casing diameter).  These catch a transcription error.
* **Relational** checks -- one part against another part (casing coaxial with
  motor, every body carried by something below it, nozzle root inside the
  casing).  These catch a wrong premise applied consistently, which is the
  failure mode the absolute checks cannot see.

Nothing here re-derives a number the way the builder did; each check states an
independent physical expectation.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all                     # noqa: E402
from build_pumps import build_pump                             # noqa: E402
from pump_model import AXIS_VECTOR                             # noqa: E402

TOL = 0.51          # millimetre tolerance, just over the emitted rounding


def bounds(primitive) -> tuple:
    """
    World extent of one primitive, applying E3D's element-specific datum.

    IR-1: BOX/CYLI/CONE are centred on POS; a DISH sits on its rim and extends
    along its axis.  Getting this wrong is exactly the failure the rule exists
    to prevent, so the verifier reproduces it rather than assuming a centre.
    """
    attrs = primitive.attrs
    east, north, up = primitive.east, primitive.north, primitive.up

    if primitive.kind == "BOX":
        half = (attrs.get("XLEN", 0) / 2, attrs.get("YLEN", 0) / 2,
                attrs.get("ZLEN", 0) / 2)
        return ((east - half[0], east + half[0]),
                (north - half[1], north + half[1]),
                (up - half[2], up + half[2]))

    if primitive.kind == "PYRAMID":
        # POS is the base centre; the solid tapers upward along local +Z.
        # The enclosing extent uses the larger of base and top on each axis.
        width = max(attrs.get("XBOT", 0), attrs.get("XTOP", 0))
        depth = max(attrs.get("YBOT", 0), attrs.get("YTOP", 0))
        height = attrs.get("HEIG", 0)
        return ((east - width / 2, east + width / 2),
                (north - depth / 2, north + depth / 2),
                (up, up + height))

    if primitive.kind == "EXTRUSION":
        # IR-1: POS is the profile END PLANE and the solid grows HEIG along
        # local +Z.  The profile's own extent gives the plan footprint.
        profile = primitive.profile or []
        if profile:
            radius = max(math.hypot(x, y) for x, y in profile)
        else:
            radius = 0.0
        height = attrs.get("HEIG", 0)
        axis = _axis_of(primitive.ori)
        vector = AXIS_VECTOR.get(axis, (0.0, 0.0, 1.0))
        out = []
        for index, centre in enumerate((east, north, up)):
            low, high = sorted((0.0, height * vector[index]))
            radial = radius * math.sqrt(max(0.0, 1.0 - vector[index] ** 2))
            out.append((centre + low - radial, centre + high + radial))
        return tuple(out)

    if primitive.kind in ("CYLINDER", "DISH"):
        diameter = attrs.get("DIAM", 0)
        height = attrs.get("HEIG", 0)
        radius = diameter / 2
        axis = _axis_of(primitive.ori)
        vector = AXIS_VECTOR.get(axis, (0.0, 0.0, 1.0))
        if primitive.kind == "DISH":
            span = [(0.0, height * component) for component in vector]
        else:
            span = [(-height / 2 * component, height / 2 * component)
                    for component in vector]
        out = []
        for index, centre in enumerate((east, north, up)):
            low, high = sorted(span[index])
            # Radial extent applies on the two axes the element does not run along.
            radial = radius * math.sqrt(max(0.0, 1.0 - vector[index] ** 2))
            out.append((centre + low - radial, centre + high + radial))
        return tuple(out)

    return ((east, east), (north, north), (up, up))


def _axis_of(ori: str) -> str:
    """The axis letter a primitive runs along, from its ``Z is`` clause."""
    if not ori:
        return "U"
    tokens = ori.replace(" and ", " ").split()
    for index, token in enumerate(tokens):
        if token.upper() == "Z" and index + 2 < len(tokens):
            letter = tokens[index + 2].upper()
            if letter in AXIS_VECTOR:
                return letter
    return "U"


def verify(model, sources) -> List[str]:
    """Return a list of failures; empty means the model passed."""
    problems: List[str] = []
    tag = model.tag
    location = sources["location"][tag]
    plate_src = location.baseplate
    facts = model.facts

    solids = [p for p in model.primitives
              if p.kind in ("BOX", "CYLINDER", "DISH", "PYRAMID", "EXTRUSION")]
    nozzles = [p for p in model.primitives if p.kind == "NOZZLE"]

    # --- [1] baseplate reproduces the project data exactly ---------------
    plate = next((p for p in model.primitives if p.sube == "BASEPLATE"), None)
    if plate is None:
        problems.append("no baseplate emitted")
    else:
        for key in ("XLEN", "YLEN", "ZLEN"):
            want = plate_src.attrs[key]
            got = plate.attrs[key]
            if abs(want - got) > TOL:
                problems.append(f"baseplate {key}: {got} != source {want}")
        for axis, key in (("east", "east"), ("north", "north"), ("up", "up")):
            want = plate_src.pos[key]
            got = getattr(plate, axis)
            if abs(want - got) > TOL:
                problems.append(f"baseplate {axis}: {got} != source {want}")

    # --- [2] nozzle plan position and direction are unchanged -------------
    source_nozzles = {("SUCTION" if "SUCTION" in n.name else "DISCHARGE"): n
                      for n in location.nozzles}
    for nozzle in nozzles:
        role = nozzle.sube
        origin = source_nozzles.get(role)
        if origin is None:
            problems.append(f"{role}: no source nozzle")
            continue
        if abs(nozzle.east - origin.pos["east"]) > TOL:
            problems.append(f"{role} E moved: {nozzle.east} != {origin.pos['east']}")
        if abs(nozzle.north - origin.pos["north"]) > TOL:
            problems.append(f"{role} N moved: {nozzle.north} != {origin.pos['north']}")
        if not nozzle.catr:
            problems.append(f"{role}: nozzle is not bound to a catalogue component")
        if nozzle.ori is None or "P1 IS" not in nozzle.ori:
            problems.append(f"{role}: nozzle not aimed with ORI P1 IS")
        heig = nozzle.attrs.get("HEIG", 0)
        if not (1.0 <= heig <= 2000.0):
            problems.append(f"{role}: HEIG {heig} outside 1..2000 mm")

    # --- [3] casing diameter matches the governing source -----------------
    casing_row = sources["casing"].get(tag)
    barrel = next((p for p in model.primitives
                   if p.sube == "CASING" and p.kind == "CYLINDER"), None)
    if casing_row and casing_row["diameter"] and barrel:
        if abs(barrel.attrs["DIAM"] - casing_row["diameter"]) > TOL:
            problems.append(
                f"casing DIAM {barrel.attrs['DIAM']} != "
                f"casing_reference {casing_row['diameter']}")
        if abs(barrel.attrs["HEIG"] - casing_row["height"]) > TOL:
            problems.append(
                f"casing HEIG {barrel.attrs['HEIG']} != "
                f"casing_reference {casing_row['height']}")

    # --- [4] RELATIONAL: casing and motor share one centreline ------------
    motor = next((p for p in model.primitives
                  if p.sube == "DRIVER" and p.kind == "CYLINDER"
                  and p.attrs.get("HEIG", 0) > 100), None)
    if barrel and motor:
        if abs(barrel.up - motor.up) > TOL:
            problems.append(
                f"casing U {barrel.up} and motor U {motor.up} are not coaxial")
        long_axis = facts.get("long_axis")
        # The transverse coordinate must also agree, or the machine is bent.
        if long_axis == "N" and abs(barrel.east - motor.east) > TOL:
            problems.append(
                f"casing E {barrel.east} and motor E {motor.east} not coaxial")
        if long_axis == "E" and abs(barrel.north - motor.north) > TOL:
            problems.append(
                f"casing N {barrel.north} and motor N {motor.north} not coaxial")

    # --- [5] nothing sinks below the foundation ---------------------------
    plate_under = facts["plate_under"]
    for primitive in solids:
        low = bounds(primitive)[2][0]
        if low < plate_under - TOL:
            problems.append(
                f"{primitive.kind} in {primitive.sube} reaches U {low:.1f}, "
                f"below the foundation {plate_under:.1f} ({primitive.note})")

    # --- [6] RELATIONAL: every body is connected to the machine -----------
    # A part is legitimately supported either by resting on something below it
    # (a pedestal on the plate) or by being attached to the machine it belongs
    # to (a bearing housing on the shaft line, a terminal box on the motor).
    # An earlier version of this check only looked downward and reported the
    # bearing housing and terminal box as floating, which they are not -- they
    # are cantilevered off parts that are themselves carried.  What actually
    # matters is that every body touches the assembly at all, so the test is
    # connectivity to the baseplate through any chain of touching parts.
    plate_top = facts["plate_top"]
    seeded = set()
    for index, primitive in enumerate(solids):
        if primitive.sube == "BASEPLATE" or bounds(primitive)[2][0] <= plate_top + TOL:
            seeded.add(index)

    boxes = [bounds(p) for p in solids]

    def touching(first: int, second: int) -> bool:
        one, two = boxes[first], boxes[second]
        for axis in range(3):
            if min(one[axis][1], two[axis][1]) < max(one[axis][0], two[axis][0]) - TOL:
                return False
        return True

    reached = set(seeded)
    frontier = list(seeded)
    while frontier:
        current = frontier.pop()
        for index in range(len(solids)):
            if index not in reached and touching(current, index):
                reached.add(index)
                frontier.append(index)

    for index, primitive in enumerate(solids):
        if index not in reached:
            problems.append(
                f"{primitive.kind} in {primitive.sube} is detached from the "
                f"machine: base U {boxes[index][2][0]:.1f} ({primitive.note})")

    # --- [7] RELATIONAL: a nozzle must meet the machine, not hang in air --
    if barrel:
        casing_dia = barrel.attrs["DIAM"]
        casing_len = barrel.attrs["HEIG"]
        axis = facts.get("long_axis")
        for nozzle in nozzles:
            vector = AXIS_VECTOR[_aim_of(nozzle.ori)]
            # Walk back along the bore by the nozzle's own length to the root.
            root = (nozzle.east - vector[0] * nozzle.attrs["HEIG"],
                    nozzle.north - vector[1] * nozzle.attrs["HEIG"],
                    nozzle.up - vector[2] * nozzle.attrs["HEIG"])
            # Distance from the root to the casing axis, measured in the plane
            # perpendicular to the machine axis.
            if axis == "N":
                radial = math.hypot(root[0] - barrel.east, root[2] - barrel.up)
                along = abs(root[1] - barrel.north)
            else:
                radial = math.hypot(root[1] - barrel.north, root[2] - barrel.up)
                along = abs(root[0] - barrel.east)
            inside = radial <= casing_dia / 2 + TOL and along <= casing_len / 2 + TOL
            reaches = radial <= casing_dia / 2 + 250.0
            if not (inside or reaches):
                problems.append(
                    f"{nozzle.sube} nozzle root is {radial:.0f} mm from the "
                    f"casing axis (casing radius {casing_dia / 2:.0f}): floating")

    # --- [7a] each anchor's washer must sit on its own sole plate ---------
    # Generic connectivity is not enough for hardware: a washer floated up into
    # the machine above still "touches" something and passes.  A washer belongs
    # to its anchor, so it is checked against the sole plate it seats on.
    soles = [p for p in solids if "sole plate" in p.note]
    for washer in (p for p in solids if "washer" in p.note):
        seated = False
        washer_box = bounds(washer)
        for sole in soles:
            sole_box = bounds(sole)
            overlaps = all(
                min(washer_box[axis][1], sole_box[axis][1])
                > max(washer_box[axis][0], sole_box[axis][0]) - TOL
                for axis in (0, 1))
            if overlaps and abs(washer_box[2][0] - sole_box[2][1]) <= 2.0:
                seated = True
                break
        if not seated:
            problems.append(
                f"hex washer is not seated on a sole plate: base U "
                f"{washer_box[2][0]:.1f} ({washer.note})")

    # --- [7b] the support must be a real structure, not a sliver ----------
    # The first support rebuild passed every other check while emitting rails
    # 8 mm tall and a 10 mm pedestal, because the machine had been seated flat
    # on the baseplate and there was no room left underneath.  Connectivity and
    # foundation checks are both blind to that: the parts touch, and nothing
    # sinks.  What was missing is a check that the support has DEPTH.
    support = [p for p in solids if p.sube == "SUPPORT"]
    if support:
        pedestals = [p for p in support if "pedestal" in p.note or "mounting pad" in p.note]
        for pedestal in pedestals:
            box = bounds(pedestal)
            height = box[2][1] - box[2][0]
            if height < 25.0:
                problems.append(
                    f"support pedestal is only {height:.1f} mm tall -- the "
                    f"machine is seated too low for a real support chain "
                    f"({pedestal.note})")
        # The machine must stand clear of the plate, or there is nowhere for
        # the frame, sole plate, gussets and anchors to live.
        machine = [p for p in solids
                   if p.sube in ("CASING", "DRIVER") and p.kind != "BOX"]
        if machine and plate is not None:
            plate_top_u = bounds(plate)[2][1]
            lowest = min(bounds(p)[2][0] for p in machine)
            if lowest - plate_top_u < 40.0:
                problems.append(
                    f"machine underside is only {lowest - plate_top_u:.1f} mm "
                    f"above the baseplate: no room for the support structure")

    # --- [8] a nozzle flange must not be buried inside the casing ---------
    if barrel:
        for nozzle in nozzles:
            if _aim_of(nozzle.ori) == "U":
                crown = barrel.up + barrel.attrs["DIAM"] / 2
                if nozzle.up < crown:
                    problems.append(
                        f"{nozzle.sube} flange face U {nozzle.up:.1f} is below "
                        f"the casing crown {crown:.1f}: buried")
    return problems


def _aim_of(ori: str) -> str:
    """The bore letter from ``ORI P1 IS <letter>``."""
    if not ori:
        return "U"
    return ori.strip().split()[-1].upper()


def main() -> int:
    sources = load_all()
    tags = sys.argv[1:] or sorted(sources["location"])
    total = 0
    for tag in tags:
        model = build_pump(tag, sources)
        problems = verify(model, sources)
        total += len(problems)
        status = "OK  " if not problems else "FAIL"
        print(f"[{status}] {tag}  {len(model.primitives):>3} elements")
        for problem in problems:
            print(f"        - {problem}")
        for note in model.unresolved:
            print(f"        ? UNRESOLVED: {note}")
    print(f"\n{len(tags)} pumps checked, {total} problems")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
