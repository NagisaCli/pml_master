"""Evidence-gated E3D DRAWING/POINT builder.

The project drawing contract is deliberately small: a DRAWING contains an
ordered sequence of independent POINT elements in 3D space. Closed outlines
repeat the first point as the final point.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Tuple

from .pml_builder import PMLValidationError, validate_pml

Point2 = Tuple[float, float]


def _fmt(value: float) -> str:
    if not math.isfinite(value):
        raise PMLValidationError(f"Drawing coordinate must be finite, got {value!r}")
    if abs(value) < 1e-9:
        value = 0.0
    return f"{value:.6f}".rstrip("0").rstrip(".") or "0"


@dataclass(frozen=True)
class PointSpec:
    """One drawing point in E/N/U space."""

    east: float
    north: float
    up: float = 0.0

    def __post_init__(self) -> None:
        for label, value in (("east", self.east), ("north", self.north), ("up", self.up)):
            if not math.isfinite(value):
                raise PMLValidationError(f"{label} must be finite, got {value!r}")
    @property
    def xyz(self) -> tuple[float, float, float]:
        return (self.east, self.north, self.up)


@dataclass(frozen=True)
class DrawingSpec:
    """An ordered, closed XY outline."""

    points: Tuple[PointSpec, ...]

    def __post_init__(self) -> None:
        if len(self.points) < 4:
            raise PMLValidationError("A closed drawing needs at least four points, including the repeated first point")
        if self.points[-1].xyz != self.points[0].xyz:
            raise PMLValidationError("Closed drawing must repeat the first 3D point as the final point")


class DrawingBuilder:
    """Emit the user's exact NEW DRAWING / NEW POINT form."""

    def build(self, spec: DrawingSpec) -> str:
        lines = ["NEW DRAWING"]
        for point in spec.points:
            lines.extend(
                (
                    "NEW POINT",
                    f"POS E {_fmt(point.east)}mm N {_fmt(point.north)}mm U {_fmt(point.up)}mm",
                    "END",
                )
            )
        lines.append("END")
        macro = "\n".join(lines) + "\n"
        errors = validate_pml(macro)
        if errors:
            raise PMLValidationError("Generated DRAWING failed PML validation: " + "; ".join(errors))
        return macro


def build_drawing(points: Iterable[PointSpec | Point2]) -> str:
    """Build a closed 3D drawing from PointSpec objects or ``(E, N[, U])`` tuples."""

    normalized = tuple(
        point if isinstance(point, PointSpec) else PointSpec(
            float(point[0]), float(point[1]), float(point[2]) if len(point) > 2 else 0.0
        )
        for point in points
    )
    return DrawingBuilder().build(DrawingSpec(normalized))


__all__ = ["DrawingBuilder", "DrawingSpec", "PointSpec", "build_drawing"]
