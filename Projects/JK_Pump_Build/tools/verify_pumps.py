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
from base_deform import (REF_MOTOR_BOTTOM, REF_MOTOR_RADIUS,
                         REF_MOTOR_SUPPORT_TOP, REF_PUMP_BOTTOM,
                         REF_PUMP_RADIUS, REF_PUMP_SUPPORT_TOP,
                         orientation_basis)                    # noqa: E402
from wsb.pml_builder import NOZZLE_BORE_COMPONENTS             # noqa: E402

TOL = 0.51          # millimetre tolerance, just over the emitted rounding
TOP_CONNECTION_PREFIX = "top discharge casing connection"
NOZZLE_DN_BY_COMPONENT = {
    component: float(dn) for dn, component in NOZZLE_BORE_COMPONENTS.items()
}


def bounds(primitive) -> tuple:
    """
    World extent of one primitive, applying E3D's element-specific datum.

    IR-1: BOX/CYLI/CONE/PYRAMID are centred on POS; a DISH sits on its rim and
    extends along its axis. Getting this wrong is exactly the failure the rule
    exists to prevent, so the verifier models every datum explicitly.
    """
    attrs = primitive.attrs
    east, north, up = primitive.east, primitive.north, primitive.up

    basis = orientation_basis(primitive.ori)

    def transform(x: float, y: float, z: float) -> tuple:
        return (east + basis["X"][0] * x + basis["Y"][0] * y
                + basis["Z"][0] * z,
                north + basis["X"][1] * x + basis["Y"][1] * y
                + basis["Z"][1] * z,
                up + basis["X"][2] * x + basis["Y"][2] * y
                + basis["Z"][2] * z)

    def envelope(points) -> tuple:
        points = list(points)
        return tuple((min(p[axis] for p in points),
                      max(p[axis] for p in points)) for axis in range(3))

    if primitive.kind == "BOX":
        hx = attrs.get("XLEN", 0) / 2
        hy = attrs.get("YLEN", 0) / 2
        hz = attrs.get("ZLEN", 0) / 2
        return envelope(transform(x, y, z)
                        for x in (-hx, hx) for y in (-hy, hy)
                        for z in (-hz, hz))

    if primitive.kind == "PYRAMID":
        xbot = attrs.get("XBOT", 0) / 2
        ybot = attrs.get("YBOT", 0) / 2
        xtop = attrs.get("XTOP", 0) / 2
        ytop = attrs.get("YTOP", 0) / 2
        xoff = attrs.get("XOFF", 0)
        yoff = attrs.get("YOFF", 0)
        height = attrs.get("HEIG", 0)
        half_height = height / 2
        points = [transform(x, y, -half_height)
                  for x in (-xbot, xbot) for y in (-ybot, ybot)]
        points += [transform(xoff + x, yoff + y, half_height)
                   for x in (-xtop, xtop) for y in (-ytop, ytop)]
        return envelope(points)

    if primitive.kind == "EXTRUSION":
        profile = primitive.profile or [(0.0, 0.0)]
        height = attrs.get("HEIG", 0)
        return envelope(transform(x, y, z) for x, y in profile
                        for z in (0.0, height))

    if primitive.kind in ("CYLINDER", "CONE", "DISH"):
        diameter = (max(attrs.get("DBOT", 0), attrs.get("DTOP", 0))
                    if primitive.kind == "CONE" else attrs.get("DIAM", 0))
        height = attrs.get("HEIG", 0)
        radius = diameter / 2
        vector = basis["Z"]
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


def combined_bounds(primitives) -> tuple:
    """Combined world AABB for a non-empty primitive collection."""
    boxes = [bounds(primitive) for primitive in primitives]
    return tuple((min(box[axis][0] for box in boxes),
                  max(box[axis][1] for box in boxes)) for axis in range(3))


def verify(model, sources) -> List[str]:
    """Return a list of failures; empty means the model passed."""
    problems: List[str] = []
    tag = model.tag
    location = sources["location"][tag]
    plate_src = location.baseplate
    facts = model.facts

    solids = [p for p in model.primitives
              if p.kind in ("BOX", "CYLINDER", "CONE", "DISH",
                            "PYRAMID", "EXTRUSION")]
    nozzles = [p for p in model.primitives if p.kind == "NOZZLE"]
    base = [p for p in solids if p.sube == "BASE"]

    # --- [1] the reference skid IS the project base envelope -------------
    # The rejected version emitted the project's old single BOX and then all
    # 43 reference members, duplicating the baseplate. The reference's five
    # skid members now replace that box and their combined envelope must equal
    # the project's confirmed base size and datum.
    duplicates = [p for p in model.primitives if p.sube == "BASEPLATE"]
    if duplicates:
        problems.append("duplicate full baseplate emitted in addition to /P1501B-BASE")
    skid = [p for p in base if "(skid station)" in p.note]
    if len(skid) != 5:
        problems.append(f"reference skid has {len(skid)} members, expected 5")
    else:
        skid_box = combined_bounds(skid)
        got = (skid_box[0][1] - skid_box[0][0],
               skid_box[1][1] - skid_box[1][0],
               skid_box[2][1] - skid_box[2][0])
        want = (plate_src.attrs["XLEN"], plate_src.attrs["YLEN"],
                plate_src.attrs["ZLEN"])
        for label, actual, expected in zip(("XLEN", "YLEN", "ZLEN"), got, want):
            if abs(actual - expected) > TOL:
                problems.append(
                    f"reference skid envelope {label}: {actual:.1f} != "
                    f"source {expected:.1f}")
        centre = tuple((axis[0] + axis[1]) / 2 for axis in skid_box)
        expected_centre = (plate_src.pos["east"], plate_src.pos["north"],
                           plate_src.pos["up"])
        for label, actual, expected in zip(("E", "N", "U"), centre,
                                           expected_centre):
            if abs(actual - expected) > TOL:
                problems.append(
                    f"reference skid centre {label}: {actual:.1f} != "
                    f"source {expected:.1f}")

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
                  if p.sube == "DRIVER"
                  and p.note.startswith("motor main stator barrel")), None)
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

    # --- [4a] measured motor frustums and three-part drive train ----------
    # This checks physical interfaces and source fields independently of the
    # builder's placement loop. It specifically rejects the r6 simplifications:
    # two decorative DISHs on one full-length motor cylinder and a one-cylinder
    # shaft with invented hubs.
    engine = facts.get("engine_record")
    wet_end = facts.get("wet_end")
    wet_vector = AXIS_VECTOR.get(wet_end, (0.0, 1.0, 0.0))
    plate_e, plate_n = facts["plate_centre"]

    def axial_span(primitive):
        centre = ((primitive.east - plate_e) * wet_vector[0]
                  + (primitive.north - plate_n) * wet_vector[1])
        half = primitive.attrs.get("HEIG", 0.0) / 2
        return (centre - half, centre + half)

    def contiguous(items, label):
        ordered = sorted(items, key=lambda primitive: axial_span(primitive)[0])
        for first, second in zip(ordered, ordered[1:]):
            gap = axial_span(second)[0] - axial_span(first)[1]
            if abs(gap) > TOL:
                problems.append(
                    f"{label} axial interface gap/overlap {gap:.1f} mm "
                    f"between {first.note!r} and {second.note!r}")
        return ordered

    driver_bodies = [p for p in solids
                     if p.sube == "DRIVER" and p.kind in ("CYLINDER", "CONE", "DISH")]
    driver_dishes = [p for p in driver_bodies if p.kind == "DISH"]
    if driver_dishes:
        problems.append(
            f"DRIVER still contains {len(driver_dishes)} DISH end bell(s); "
            f"r9 requires cone-terminated motor ends")

    if engine:
        motor_parts = contiguous(
            [p for p in driver_bodies if p.kind in ("CYLINDER", "CONE")],
            "motor")
        if not motor_parts:
            problems.append("motor has no measured CYLINDER/CONE body segments")
        else:
            motor_low = axial_span(motor_parts[0])[0]
            motor_high = axial_span(motor_parts[-1])[1]
            if motor_parts[0].kind != "CONE" or "rear frustum" not in motor_parts[0].note:
                problems.append(
                    f"motor tail terminates in {motor_parts[0].kind} "
                    f"({motor_parts[0].note!r}); rear terminal body must be CONE")
            expected_total = facts.get("motor_effective_total")
            if expected_total and abs((motor_high - motor_low) - expected_total) > TOL:
                problems.append(
                    f"motor segmented envelope {motor_high - motor_low:.1f} != "
                    f"resolved total {expected_total:.1f}")
            expected_roles = ["rear frustum", "main stator barrel",
                              "front frustum"]
            for role in expected_roles:
                if not any(f"motor {role}:" in p.note for p in motor_parts):
                    problems.append(f"motor is missing required {role}")
            cones = [p for p in motor_parts if p.kind == "CONE"]
            if len(cones) != 2:
                problems.append(f"motor has {len(cones)} end CONEs, expected 2")
            elif motor_parts:
                main = next((p for p in motor_parts
                             if "motor main stator barrel:" in p.note), None)
                if main:
                    target_outer = main.attrs["DIAM"] * (2.0 / 3.0)
                    rear, front = cones
                    checks = (
                        (rear.attrs.get("DBOT"), target_outer, "rear outward face"),
                        (rear.attrs.get("DTOP"), main.attrs["DIAM"], "rear inner face"),
                        (front.attrs.get("DBOT"), main.attrs["DIAM"], "front inner face"),
                        (front.attrs.get("DTOP"), target_outer, "front outward face"),
                        (rear.attrs.get("HEIG"), front.attrs.get("HEIG"),
                         "front/rear cone length"),
                    )
                    for actual, expected, label in checks:
                        if actual is None or abs(actual - expected) > TOL:
                            problems.append(
                                f"motor {label} {actual} != {expected:.1f}")
            for cone in (p for p in motor_parts if p.kind == "CONE"):
                if cone.attrs.get("DBOT", 0) <= 0 or cone.attrs.get("DTOP", 0) <= 0:
                    problems.append(f"motor CONE has invalid end diameters: {cone.note}")
                if _axis_of(cone.ori) != wet_end:
                    problems.append(
                        f"motor CONE axis {_axis_of(cone.ori)} does not point "
                        f"toward wet end {wet_end}: {cone.note}")

        shaft_total = engine.get("shaft_total_L_mm")
        drive = [p for p in solids if p.sube == "DRIVE_SHAFT"]
        old_drive = [p for p in solids if p.sube == "COUPLING"]
        if old_drive:
            problems.append(
                f"old simplified COUPLING geometry remains ({len(old_drive)} solids)")

        casing_e, casing_n = facts["casing_centre"]
        casing_along = ((casing_e - plate_e) * wet_vector[0]
                        + (casing_n - plate_n) * wet_vector[1])
        casing_back = casing_along - facts["casing"][1] / 2
        motor_high = (max(axial_span(p)[1] for p in driver_bodies)
                      if driver_bodies else 0.0)

        if shaft_total is None:
            if drive:
                problems.append("MC/N/A shaft row emitted a free DRIVE_SHAFT")
            lanterns = [p for p in solids if p.sube == "BEARING"]
            if casing_back > motor_high + TOL:
                if len(lanterns) != 1:
                    problems.append(
                        f"close-coupled MC gap has {len(lanterns)} lanterns, expected 1")
                elif (abs(axial_span(lanterns[0])[0] - motor_high) > TOL
                      or abs(axial_span(lanterns[0])[1] - casing_back) > TOL):
                    problems.append(
                        "close-coupled MC lantern does not span motor face to casing")
        else:
            if [p.kind for p in drive] != ["CYLINDER", "CYLINDER", "CONE"]:
                problems.append(
                    f"DRIVE_SHAFT shape is {[p.kind for p in drive]}, expected "
                    f"CYLINDER/CYLINDER/CONE")
            ordered = contiguous(drive, "drive shaft") if drive else []
            if ordered:
                if abs(axial_span(ordered[0])[0] - motor_high) > TOL:
                    problems.append(
                        f"drive shaft starts {axial_span(ordered[0])[0] - motor_high:.1f} "
                        f"mm from motor front")
                drive_end = axial_span(ordered[-1])[1]
                if not (casing_back - TOL <= drive_end <= casing_along + TOL):
                    problems.append(
                        f"drive shaft pump end {drive_end:.1f} is outside casing "
                        f"engagement {casing_back:.1f}..{casing_along:.1f}")

                source_lengths = [
                    engine.get("shaft_cyl1_L_mm"),
                    engine.get("shaft_cyl2_L_mm"),
                    engine.get("shaft_frust3_L_mm"),
                ]
                scales = [p.attrs.get("HEIG", 0) / source
                          for p, source in zip(ordered, source_lengths)
                          if source]
                if len(scales) != 3 or max(scales) - min(scales) > 0.001:
                    problems.append(
                        f"drive shaft did not retain measured axial part ratios: {scales}")

                expected_diameters = (
                    ("DIAM", engine.get("shaft_cyl1_D_mm")),
                    ("DIAM", engine.get("shaft_cyl2_D_mm")),
                    ("DBOT", engine.get("shaft_frust3_D_min_mm")),
                    ("DTOP", engine.get("shaft_frust3_D_max_mm")),
                )
                actual = (ordered[0], ordered[1], ordered[2], ordered[2])
                for primitive, (key, expected) in zip(actual, expected_diameters):
                    if expected is not None and abs(primitive.attrs.get(key, 0) - expected) > TOL:
                        problems.append(
                            f"{primitive.note} {key} {primitive.attrs.get(key)} != "
                            f"source {expected}")

            for primitive in drive:
                if abs(primitive.up - facts["shaft_u"]) > TOL:
                    problems.append(
                        f"{primitive.note} U {primitive.up} is off shaft axis "
                        f"{facts['shaft_u']}")
                if _axis_of(primitive.ori) != wet_end:
                    problems.append(
                        f"{primitive.note} axis {_axis_of(primitive.ori)} != {wet_end}")

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
    # The tolerance for "touching" is wider than a rounding epsilon, because
    # the REFERENCE base itself is a bolted assembly rather than a fused solid:
    # in /P1501B-BASE the sole plates stop at U -255 while the gussets above
    # them start at -236, and the pump-end pad tops out at -200 with its side
    # brackets starting at -170.  Those 19-30 mm gaps are how the real thing is
    # built -- shims and bolted joints -- so a strict contact test would
    # condemn a faithful copy of the client's own reference.
    #
    # The tolerance must also SCALE.  A base adapted to a 2701 mm plate is
    # roughly 2.4x the reference, so the reference's own 30 mm joint opens to
    # ~72 mm.  A fixed millimetre figure would pass the small pumps and fail
    # the large ones for reproducing the reference faithfully, so it is
    # expressed as a fraction of the plate length with a floor for small
    # plates.  What must still be caught is a part in genuinely open air.
    plate_len = max(facts["plate"][0], facts["plate"][1])
    CONTACT_GAP = max(40.0, plate_len * 0.030)
    plate_top = facts["plate_top"]
    seeded = set()
    for index, primitive in enumerate(solids):
        if primitive.sube == "BASEPLATE" or bounds(primitive)[2][0] <= plate_top + TOL:
            seeded.add(index)

    boxes = [bounds(p) for p in solids]

    def touching(first: int, second: int) -> bool:
        one, two = boxes[first], boxes[second]
        for axis in range(3):
            if min(one[axis][1], two[axis][1])                     < max(one[axis][0], two[axis][0]) - CONTACT_GAP:
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

    # --- [7a] every hex washer must sit on a BASE member below it --------
    # Generic connectivity is not enough for hardware: a washer floated up into
    # the machine above still "touches" something and passes.  A washer is an
    # anchor fitting, so it must rest on a base member directly beneath it --
    # checked in plan, with the washer's underside on that member's top.
    washers = [p for p in solids if p.kind == "EXTRUSION" and p.sube == "BASE"]
    supports = [p for p in solids
                if p.sube == "BASE" and p.kind in ("BOX", "PYRAMID")]
    for washer in washers:
        washer_box = bounds(washer)
        seated = False
        for member in supports:
            member_box = bounds(member)
            overlaps = all(
                min(washer_box[axis][1], member_box[axis][1])
                > max(washer_box[axis][0], member_box[axis][0]) - TOL
                for axis in (0, 1))
            # The washer's base must be at or just above the member's top.
            if overlaps and -TOL <= washer_box[2][0] - member_box[2][1] <= 60.0:
                seated = True
                break
        if not seated:
            problems.append(
                f"hex washer is not seated on any base member: base U "
                f"{washer_box[2][0]:.1f} ({washer.note})")

    # --- [7b] the base must be a real structure, not a sliver -------------
    # An earlier rebuild passed every other check while emitting rails 8 mm
    # tall, because the machine had been seated flat on the baseplate and there
    # was no room underneath.  Connectivity and foundation checks are both
    # blind to that: the parts touch, and nothing sinks.  What was missing is a
    # check that the base has DEPTH.
    if base:
        plate_top_u = facts["plate_top"]
        base_top = max(bounds(p)[2][1] for p in base)
        rise = base_top - plate_top_u
        if rise < 25.0:
            problems.append(
                f"base rises only {rise:.1f} mm above the plate: the machine "
                f"is seated too low for the reference support structure")

        # The machine must stand clear of the plate, or there is nowhere for
        # the reference's mountings, gussets and anchors to live.
        machine = [p for p in solids
                   if p.sube in ("CASING", "DRIVER") and p.kind != "BOX"]
        if machine:
            lowest = min(bounds(p)[2][0] for p in machine)
            if lowest - plate_top_u < 40.0:
                problems.append(
                    f"machine underside is only {lowest - plate_top_u:.1f} mm "
                    f"above the baseplate: no room for the support structure")

        # The base must be the reference's own element set.  Now that the
        # base is /P1501B-BASE deformed rather than a hand-built assembly, the
        # inventory IS the specification again and can be asserted exactly:
        # 11 BOX, 12 PYRAMID, 10 EXTRUSION, 10 CYLINDER, in three station
        # groups.  A missing member means the reference shape was not
        # reproduced.
        from collections import Counter
        census = Counter(p.kind for p in base)
        expected = {"BOX": 11, "PYRAMID": 12, "EXTRUSION": 10, "CYLINDER": 10}
        for kind, count in expected.items():
            if census.get(kind, 0) != count:
                problems.append(
                    f"base has {census.get(kind, 0)} {kind} where "
                    f"/P1501B-BASE has {count}: the reference shape is not "
                    f"reproduced")

        groups = Counter(
            p.note.split("(")[-1].split(" station")[0] for p in base
            if " station)" in p.note)
        for group, count in (("skid", 5), ("pump", 17), ("motor", 21)):
            if groups.get(group, 0) != count:
                problems.append(
                    f"base has {groups.get(group, 0)} members in the {group} "
                    f"group where the reference has {count}")

        # The reference support penetrates the machine envelope deliberately:
        # pump saddle 60/170 of the casing radius, motor stays 55/180 of the
        # stator radius. Compressing each station to the cylinder's lowest
        # point produced the shallow, disconnected-looking support in the
        # rejected render while the old zero-gap check passed.
        relations = (
            ("pump", "CASING", REF_PUMP_BOTTOM, REF_PUMP_SUPPORT_TOP,
             REF_PUMP_RADIUS),
            ("motor", "DRIVER", REF_MOTOR_BOTTOM, REF_MOTOR_SUPPORT_TOP,
             REF_MOTOR_RADIUS),
        )
        for group, sube, ref_bottom, ref_top, ref_radius in relations:
            members = [p for p in base if f"({group} station)" in p.note]
            barrels = [p for p in solids
                       if p.sube == sube and p.kind == "CYLINDER"]
            if not members or not barrels:
                continue
            station_top = max(bounds(p)[2][1] for p in members)
            station_barrel = next(
                (item for item in barrels if "volute barrel" in item.note),
                max(barrels, key=lambda p: p.attrs.get("HEIG", 0)))
            machine_low = bounds(station_barrel)[2][0]
            radius = station_barrel.attrs.get("DIAM", 0) / 2
            expected_top = (machine_low
                            + (ref_top - ref_bottom) * radius / ref_radius)
            if abs(station_top - expected_top) > 1.0:
                problems.append(
                    f"{group} station tops out at U {station_top:.1f} against "
                    f"the reference-adapted target {expected_top:.1f} "
                    f"(machine underside {machine_low:.1f})")

        # Base members are FABRICATED PLATE: their thickness is set by the
        # baseplate thickness, not by the plate's width.  An earlier revision
        # scaled thickness off width, so a 2013-wide pump got 72 mm sole plates
        # and a 130 mm foot pad on a 50 mm plate -- the model the client
        # rejected as "primitives stacked together".  Every positional check
        # passed it, because nothing asked whether a plate looked like a plate.
        plate_thick = plate_src.attrs["ZLEN"] if plate_src else 50.0
        for member in base:
            if member.kind != "BOX":
                continue
            box = bounds(member)
            thickness = box[2][1] - box[2][0]
            span = max(box[0][1] - box[0][0], box[1][1] - box[1][0])
            if thickness > plate_thick * 1.6:
                problems.append(
                    f"base member is {thickness:.0f} mm thick against a "
                    f"{plate_thick:.0f} mm baseplate: a slab, not plate "
                    f"({member.note})")
            elif span > 0 and thickness > span * 0.8:
                problems.append(
                    f"base member is {thickness:.0f} mm thick over a "
                    f"{span:.0f} mm span: not a plate ({member.note})")

        # Nothing may protrude below the foundation, and an anchor must not
        # tower above the member it clamps.
        for member in base:
            box = bounds(member)
            if box[2][0] < facts["plate_under"] - TOL:
                problems.append(
                    f"base member reaches U {box[2][0]:.1f}, below the "
                    f"foundation ({member.note})")

        # The reference's side stays deliberately overhang the 510 mm skid
        # envelope. They are retained as part of the exact reference shape;
        # containing every support AABB inside the skid would reject the
        # client's own native base.

    # --- [8] a nozzle flange must not be buried inside the casing ---------
    if barrel:
        for nozzle in nozzles:
            if _aim_of(nozzle.ori) == "U":
                crown = barrel.up + barrel.attrs["DIAM"] / 2
                # The barrel deliberately penetrates the volute by up to
                # 100 mm; only a flange buried beyond that construction band
                # is invalid.
                if nozzle.up < crown - 100.0 - TOL:
                    problems.append(
                        f"{nozzle.sube} flange face U {nozzle.up:.1f} is below "
                        f"the casing crown {crown:.1f}: buried")

    # --- [9] top nozzles branch on nozzle DN vs casing axial width ----------
    # A contained native nozzle directly penetrates the casing with >=70% of
    # HEIG above the crown. An overwidth nozzle uses only a lower CYLINDER and
    # CONE, with the CONE upper face closing on the native nozzle bottom.
    top_nozzles = [p for p in nozzles if _aim_of(p.ori) == "U"]
    connectors = [p for p in solids
                  if p.note.startswith(TOP_CONNECTION_PREFIX)]
    offset_bridges = [p for p in solids
                      if p.note.startswith("top discharge casing offset bridge")]
    if not top_nozzles:
        if connectors or offset_bridges:
            problems.append("top-discharge casing connector emitted without an up nozzle")
    elif len(top_nozzles) != 1:
        problems.append(f"found {len(top_nozzles)} up nozzles; expected one")
    elif not barrel:
        problems.append("up nozzle has no casing barrel to connect to")
    else:
        nozzle = top_nozzles[0]
        component = (nozzle.catr or "").rsplit("/", 1)[-1]
        nozzle_dia = NOZZLE_DN_BY_COMPONENT.get(component)
        casing_width = barrel.attrs["HEIG"]
        crown = barrel.up + barrel.attrs["DIAM"] / 2.0
        root_u = nozzle.up - nozzle.attrs["HEIG"]
        parts = sorted(connectors, key=lambda item: bounds(item)[2][0])
        barrel_axis = _axis_of(barrel.ori)
        axial_offset = (abs(nozzle.north - barrel.north)
                        if barrel_axis == "N" else
                        abs(nozzle.east - barrel.east))
        needs_bridge = axial_offset > casing_width / 2.0 + TOL
        overwidth = nozzle_dia is not None and nozzle_dia > casing_width + TOL

        if nozzle_dia is None:
            problems.append("up nozzle has no verified DN for casing connection")
        elif not overwidth:
            if parts:
                problems.append(
                    "top nozzle within casing width must directly penetrate casing; "
                    "additive connector primitives are not allowed")
            if offset_bridges:
                problems.append("direct top nozzle has an unneeded horizontal bridge")
            if nozzle.attrs["HEIG"] <= TOL:
                problems.append("direct top nozzle has no positive HEIG")
            else:
                external_height = nozzle.up - crown
                external_ratio = external_height / nozzle.attrs["HEIG"]
                if external_height <= TOL:
                    problems.append("direct top nozzle flange face is not above casing crown")
                if external_ratio < 0.70 - 0.001:
                    problems.append(
                        f"direct top nozzle external ratio {external_ratio:.3f} is below 0.70")
                if root_u >= crown - TOL:
                    problems.append(
                        "direct top nozzle bottom does not penetrate the casing crown")
        elif not parts:
            problems.append("overwidth up nozzle has no primitive size transition")
        else:
            for part in parts:
                if part.sube != "CASING":
                    problems.append("top-nozzle connection is not owned by CASING")
                if _axis_of(part.ori) != "U":
                    problems.append(
                        f"top-nozzle {part.kind} axis is {_axis_of(part.ori)}, expected U")
                if abs(part.east - nozzle.east) > TOL or abs(part.north - nozzle.north) > TOL:
                    problems.append(
                        f"top-nozzle {part.kind} is not coaxial with the native nozzle")

            spans = [bounds(part)[2] for part in parts]
            if spans[0][0] >= crown - TOL:
                problems.append(
                    f"top-nozzle connection starts at U {spans[0][0]:.1f}, "
                    f"not embedded in casing crown U {crown:.1f}")
            if spans[0][1] <= crown + TOL:
                problems.append(
                    "overwidth lower socket does not project visibly above the casing")
            terminal_gap = root_u - spans[-1][1]
            if abs(terminal_gap) > TOL:
                problems.append(
                    f"native nozzle bottom / transition upper-face gap-overlap "
                    f"is {terminal_gap:.1f} mm; terminal faces must coincide")
            if root_u >= nozzle.up - TOL:
                problems.append("up nozzle has no positive projection above its connector")

            for index in range(len(spans) - 1):
                gap = spans[index + 1][0] - spans[index][1]
                if abs(gap) > TOL:
                    problems.append(
                        f"top-nozzle connection interface {index + 1} has "
                        f"vertical gap/overlap {gap:.1f} mm")

            if needs_bridge:
                if len(offset_bridges) != 1:
                    problems.append(
                        f"offset top nozzle needs one casing bridge; found "
                        f"{len(offset_bridges)}")
                else:
                    bridge = offset_bridges[0]
                    if bridge.kind != "CYLINDER" or _axis_of(bridge.ori) == "U":
                        problems.append(
                            "offset top-nozzle bridge must be one horizontal CYLINDER")

                    def intersects(first, second) -> bool:
                        one, two = bounds(first), bounds(second)
                        return all(min(one[axis][1], two[axis][1])
                                   >= max(one[axis][0], two[axis][0]) - TOL
                                   for axis in range(3))

                    if not intersects(bridge, barrel):
                        problems.append("offset top-nozzle bridge does not overlap casing")
                    if not intersects(bridge, parts[0]):
                        problems.append("offset top-nozzle bridge does not overlap lower socket")
            elif offset_bridges:
                problems.append("unneeded horizontal bridge emitted under centred top nozzle")

            if [part.kind for part in parts] != ["CYLINDER", "CONE"]:
                problems.append(
                    "overwidth top nozzle must use only CYLINDER/CONE before NOZZLE")
            else:
                socket, reducer = parts
                socket_dia = socket.attrs["DIAM"]
                if socket_dia > casing_width + TOL:
                    problems.append(
                        f"top-nozzle socket dia {socket_dia:.1f} exceeds "
                        f"casing width {casing_width:.1f}")
                if not (socket_dia < nozzle_dia - TOL
                        and abs(reducer.attrs["DBOT"] - socket_dia) <= TOL
                        and abs(reducer.attrs["DTOP"] - nozzle_dia) <= TOL):
                    problems.append(
                        "top-nozzle reducer diameters do not join socket and NOZZLE smoothly")
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
