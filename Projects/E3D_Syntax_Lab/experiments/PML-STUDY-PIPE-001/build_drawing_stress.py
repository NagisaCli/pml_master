"""Build a standalone 2,000-point 3D DRAWING syntax stress specimen.

This deliberately creates no SITE, ZONE, PIPE, BRANCH or catalogue element.
The torus-knot path exercises dense point ordering, non-planar coordinates and
exact closure without touching project databases.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from wsb.drawing_builder import build_drawing


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "candidate" / "drawing_2000pt_torus_knot_stress.pml"
POINT_COUNT = 2000


def torus_knot_points(count: int = POINT_COUNT) -> tuple[tuple[float, float, float], ...]:
    if count < 4:
        raise ValueError("A stress drawing needs at least four points")
    points: list[tuple[float, float, float]] = []
    for index in range(count - 1):
        t = 2.0 * math.pi * index / (count - 1)
        # A closed (p=5, q=3) torus knot in millimetres.
        major = 2500.0
        minor = 850.0
        p = 5.0
        q = 3.0
        radial = major + minor * math.cos(q * t)
        points.append(
            (
                radial * math.cos(p * t),
                radial * math.sin(p * t),
                minor * math.sin(q * t),
            )
        )
    points.append(points[0])
    return tuple(points)


if __name__ == "__main__":
    OUTPUT.write_text(build_drawing(torus_knot_points()), encoding="utf-8", newline="\n")
    print(OUTPUT)
