"""Evidence-gated AVEVA E3D EXTRUSION / LOOP / VERTEX builder.

The element hierarchy and local-profile contract are verified from AVEVA's
installed E3D 3.1 PML library and a user-supplied native Design data listing.
The longitudinal POS datum is VERIFIED (user E3D result 2026-08-04, candidate
PML-STUDY-EXTR-001/01): POS is the profile end plane — the LOOP plane sits at
POS and the solid extends HEIG toward local +Z. Assignment order was shown
equivalent for the tested forms (candidate /03), so this builder keeps the
native POS -> ORI order without enforcing an ORI-before-POS rule.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Iterable, Tuple

from .pml_builder import PMLValidationError, validate_pml

Point2 = Tuple[float, float]
Point3 = Tuple[float, float, float]

_CARDINAL = {"E", "N", "W", "S", "U", "D"}
_VECTOR = {
    "E": (1, 0, 0),
    "W": (-1, 0, 0),
    "N": (0, 1, 0),
    "S": (0, -1, 0),
    "U": (0, 0, 1),
    "D": (0, 0, -1),
}
_ORI = re.compile(r"^Y\s+IS\s+([ENWSUD])\s+AND\s+Z\s+IS\s+([ENWSUD])$", re.I)


def _fmt(value: float) -> str:
    if not math.isfinite(value):
        raise PMLValidationError(f"EXTRUSION value must be finite, got {value!r}")
    if abs(value) < 1e-9:
        value = 0.0
    return f"{value:.6f}".rstrip("0").rstrip(".") or "0"


def _signed_area(vertices: Tuple[Point2, ...]) -> float:
    return 0.5 * sum(
        x1 * y2 - x2 * y1
        for (x1, y1), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1])
    )


@dataclass(frozen=True)
class ExtrusionSpec:
    """One native-form EXTRUSION with one planar LOOP.

    ``position`` is the EXTRUSION's profile end-plane POS (VERIFIED): the LOOP
    plane sits at this point and ``height`` is swept toward local +Z. It is
    not a bottom-face or centre abstraction and must not be converted.
    ``vertices`` are local LOOP XY coordinates in source order. The LOOP closes
    the final edge back to the first vertex implicitly.
    """

    position: Point3
    orientation: str
    height: float
    vertices: Tuple[Point2, ...]
    level: Tuple[int, int] | None = None

    def __post_init__(self) -> None:
        if len(self.vertices) < 3:
            raise PMLValidationError("EXTRUSION LOOP needs at least three vertices")
        if not math.isfinite(self.height) or self.height <= 0:
            raise PMLValidationError(f"EXTRUSION HEIG must be positive, got {self.height!r}")
        for value in (*self.position, *(coordinate for point in self.vertices for coordinate in point)):
            if not math.isfinite(value):
                raise PMLValidationError(f"EXTRUSION coordinate must be finite, got {value!r}")

        match = _ORI.fullmatch(" ".join(self.orientation.upper().split()))
        if not match:
            raise PMLValidationError(
                "EXTRUSION orientation must be 'Y IS <cardinal> AND Z IS <cardinal>'"
            )
        y_axis, z_axis = match.groups()
        if y_axis not in _CARDINAL or z_axis not in _CARDINAL:
            raise PMLValidationError("EXTRUSION orientation contains an unknown axis")
        if sum(a * b for a, b in zip(_VECTOR[y_axis], _VECTOR[z_axis])) != 0:
            raise PMLValidationError("EXTRUSION Y and Z directions must be orthogonal")

        normalized = self.normalized_vertices
        if len(set(normalized)) < 3 or abs(_signed_area(normalized)) < 1e-6:
            raise PMLValidationError("EXTRUSION LOOP must enclose a non-zero planar area")
        if self.level is not None:
            low, high = self.level
            if low < 0 or high < low:
                raise PMLValidationError(f"Invalid EXTRUSION LEVE range {self.level!r}")

    @property
    def normalized_vertices(self) -> Tuple[Point2, ...]:
        """Remove only a repeated closing vertex; LOOP closure is implicit."""
        if len(self.vertices) > 1 and self.vertices[-1] == self.vertices[0]:
            return self.vertices[:-1]
        return self.vertices

    @property
    def profile_area(self) -> float:
        return abs(_signed_area(self.normalized_vertices))

    @property
    def profile_bounds(self) -> Tuple[float, float, float, float]:
        xs = [point[0] for point in self.normalized_vertices]
        ys = [point[1] for point in self.normalized_vertices]
        return min(xs), max(xs), min(ys), max(ys)


class ExtrusionBuilder:
    """Emit the exact full-name native EXTRUSION hierarchy."""

    def build(self, spec: ExtrusionSpec) -> str:
        east, north, up = spec.position
        orientation = " ".join(spec.orientation.upper().split())
        lines = [
            "NEW EXTRUSION",
            f"POS E {_fmt(east)}mm N {_fmt(north)}mm U {_fmt(up)}mm",
            f"ORI {orientation}",
        ]
        if spec.level is not None:
            lines.append(f"LEVE {spec.level[0]} {spec.level[1]}")
        lines.extend((f"HEIG {_fmt(spec.height)}mm", "", "NEW LOOP"))
        for x, y in spec.normalized_vertices:
            lines.extend(
                (
                    "NEW VERTEX",
                    f"POS E {_fmt(x)}mm N {_fmt(y)}mm U 0mm",
                    "END",
                )
            )
        lines.extend(("END", "END"))
        macro = "\n".join(lines) + "\n"
        problems = validate_pml(macro)
        if problems:
            raise PMLValidationError("Generated EXTRUSION failed PML validation: " + "; ".join(problems))
        return macro


def build_extrusion(
    position: Point3,
    orientation: str,
    height: float,
    vertices: Iterable[Point2],
    *,
    level: Tuple[int, int] | None = None,
) -> str:
    return ExtrusionBuilder().build(
        ExtrusionSpec(position, orientation, height, tuple(vertices), level)
    )


__all__ = ["ExtrusionBuilder", "ExtrusionSpec", "build_extrusion"]
