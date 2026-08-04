from __future__ import annotations

import importlib.util
from pathlib import Path

from wsb.drawing_builder import build_drawing


def test_2000_point_stress_is_standalone_and_closed():
    path = Path(__file__).parents[1] / "Projects/E3D_Syntax_Lab/experiments/PML-STUDY-PIPE-001/build_drawing_stress.py"
    spec = importlib.util.spec_from_file_location("drawing_stress", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    torus_knot_points = module.torus_knot_points

    points = torus_knot_points()
    assert len(points) == 2000
    assert points[0] == points[-1]
    assert any(point[2] != 0 for point in points)
    macro = build_drawing(points)
    assert macro.count("NEW DRAWING") == 1
    assert macro.count("NEW POINT") == 2000
    assert "NEW SITE" not in macro
    assert "NEW PIPE" not in macro
