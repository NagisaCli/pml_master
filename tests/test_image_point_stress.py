from __future__ import annotations

from pathlib import Path


def test_image_point_stress_is_isolated_and_dense():
    path = Path(__file__).parents[1] / "Projects/E3D_Syntax_Lab/experiments/PML-STUDY-PIPE-001/build_image_point_stress.py"
    namespace: dict[str, object] = {"__file__": str(path), "__name__": "image_stress_test"}
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), namespace)
    macro = namespace["build"]()
    assert macro.count("NEW DRAWING") == 3
    assert macro.count("NEW POINT") > 1000
    assert "NEW SITE" not in macro
    assert "NEW PIPE" not in macro
