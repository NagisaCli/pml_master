from __future__ import annotations

import pytest

from wsb.drawing_builder import DrawingBuilder, DrawingSpec, PointSpec, build_drawing
from wsb.pml_builder import PMLValidationError, validate_pml


def test_builds_ordered_closed_xy_drawing_with_independent_points():
    macro = build_drawing(((0, 0), (100, 0), (100, 50), (0, 0)))
    assert macro == (
        "NEW DRAWING\n"
        "NEW POINT\nPOS E 0mm N 0mm U 0mm\nEND\n"
        "NEW POINT\nPOS E 100mm N 0mm U 0mm\nEND\n"
        "NEW POINT\nPOS E 100mm N 50mm U 0mm\nEND\n"
        "NEW POINT\nPOS E 0mm N 0mm U 0mm\nEND\n"
        "END\n"
    )
    assert validate_pml(macro) == []


def test_rejects_open_outline():
    with pytest.raises(PMLValidationError, match="repeat the first 3D point"):
        DrawingBuilder().build(
            DrawingSpec(tuple(PointSpec(east, north) for east, north in ((0, 0), (1, 0), (1, 1), (0, 1))))
        )


def test_allows_arbitrary_3d_points():
    macro = build_drawing(((0, 0, 10), (100, 0, 20), (100, 50, 30), (0, 0, 10)))
    assert "POS E 100mm N 0mm U 20mm" in macro


def test_rejects_too_few_points():
    with pytest.raises(PMLValidationError, match="at least four"):
        DrawingSpec((PointSpec(0, 0), PointSpec(0, 0), PointSpec(0, 0)))
