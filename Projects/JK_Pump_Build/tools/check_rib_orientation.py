"""
Prove the cooling-rib orientation is geometrically right.

The repo validator flags every rib with "plan-rotated boxes take
``ORI Z IS U AND X IS <bearing>``".  That rule is written for a plate on a
VERTICAL vessel, where all radial directions lie in the horizontal plane.  A
motor is a HORIZONTAL cylinder: its ribs sweep a vertical plane, so pinning
local Z to Up would hold every rib upright and only the two at top and bottom
dead centre would sit flat on the barrel.

Rather than argue the point, this script resolves each emitted ``ORI`` into an
actual axis triad and checks the three physical properties a correct rib has:

1. its local X (the thin radial direction) points at the machine axis;
2. its local Y runs along the machine axis;
3. the triad is right-handed and orthonormal.

That is a check on the geometry, not on the wording of the rule.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all      # noqa: E402
from build_pumps import build_pump              # noqa: E402

AXIS = {"E": (1.0, 0.0, 0.0), "W": (-1.0, 0.0, 0.0),
        "N": (0.0, 1.0, 0.0), "S": (0.0, -1.0, 0.0),
        "U": (0.0, 0.0, 1.0), "D": (0.0, 0.0, -1.0)}


def resolve(spec: str):
    """Resolve ``E 30 U`` style axis text into a unit vector."""
    tokens = spec.split()
    base = AXIS[tokens[0].upper()]
    if len(tokens) == 1:
        return base
    angle = math.radians(float(tokens[1]))
    toward = AXIS[tokens[2].upper()]
    vector = tuple(base[i] * math.cos(angle) + toward[i] * math.sin(angle)
                   for i in range(3))
    length = math.sqrt(sum(component ** 2 for component in vector))
    return tuple(component / length for component in vector)


def parse_ori(ori: str):
    """Return the named axes from ``ORI Y IS <a> AND X IS <b>``."""
    body = ori[4:] if ori.upper().startswith("ORI ") else ori
    parts = [p.strip() for p in body.split(" AND ")]
    axes = {}
    for part in parts:
        tokens = part.split(None, 2)
        axes[tokens[0].upper()] = resolve(tokens[2])
    return axes


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def main() -> int:
    sources = load_all()
    failures = 0
    checked = 0

    for tag in sorted(sources["location"]):
        model = build_pump(tag, sources)
        facts = model.facts
        motor = next((p for p in model.primitives
                      if p.sube == "DRIVER" and p.kind == "CYLINDER"
                      and p.attrs.get("HEIG", 0) > 100), None)
        if motor is None:
            continue
        long_axis = facts["long_axis"]
        axis_vector = (0.0, 1.0, 0.0) if long_axis == "N" else (1.0, 0.0, 0.0)

        ribs = [p for p in model.primitives if "cooling rib" in p.note]
        for rib in ribs:
            checked += 1
            axes = parse_ori(rib.ori)
            local_y = axes["Y"]
            local_x = axes["X"]
            local_z = cross(local_x, local_y)

            # 1. local Y runs along the machine axis.
            if abs(abs(dot(local_y, axis_vector)) - 1.0) > 1e-6:
                print(f"{tag}: rib local Y is not the machine axis: {rib.ori}")
                failures += 1
                continue

            # 2. local X points radially -- i.e. straight at the machine axis.
            #    The vector from the rib centre to the nearest point on the
            #    axis must be antiparallel to local X.
            to_centre = (motor.east - rib.east,
                         motor.north - rib.north,
                         motor.up - rib.up)
            # Remove the component along the machine axis.
            along = dot(to_centre, axis_vector)
            radial = tuple(to_centre[i] - along * axis_vector[i] for i in range(3))
            length = math.sqrt(sum(c ** 2 for c in radial))
            if length < 1e-6:
                continue
            radial = tuple(c / length for c in radial)
            if dot(local_x, radial) > -0.999:
                print(f"{tag}: rib local X is not radial "
                      f"(dot {dot(local_x, radial):+.4f}): {rib.ori}")
                failures += 1
                continue

            # 3. the triad is orthonormal.
            for name, vector in (("X", local_x), ("Y", local_y), ("Z", local_z)):
                if abs(math.sqrt(sum(c ** 2 for c in vector)) - 1.0) > 1e-6:
                    print(f"{tag}: rib local {name} is not unit length")
                    failures += 1
            if abs(dot(local_x, local_y)) > 1e-6:
                print(f"{tag}: rib local X and Y are not perpendicular")
                failures += 1

    print(f"\n{checked} ribs checked, {failures} geometrically wrong")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
