from __future__ import annotations

from pathlib import Path


def test_alphabet_stress_is_composed_of_closed_drawings_only():
    path = Path(__file__).parents[1] / "Projects/E3D_Syntax_Lab/experiments/PML-STUDY-PIPE-001/build_alphabet_stress.py"
    namespace: dict[str, object] = {"__file__": str(path), "__name__": "alphabet_test"}
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), namespace)
    macro = namespace["build"]()
    assert macro.count("-- LETTER ") == 26
    assert macro.count("NEW DRAWING") > 200
    assert macro.count("NEW DRAWING") == macro.count("END") // 6
    assert "NEW SITE" not in macro
    assert "NEW PIPE" not in macro
