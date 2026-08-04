"""
Evidence-gated PIPE / BRANCH builder.

This module emits the smallest reusable piping form that has already been
observed working in the user's E3D session:

* a PIPE owns one or more BRANCH elements;
* a free BRANCH is defined by head/tail position, direction, bore and
  connection attributes;
* straight tube between the two ends is implicit;
* an optional SLOREF may be carried by both PIPE and BRANCH.

Two catalogue-component contracts are also available after VERIFIED E3D Design
Mk3.1.11.0 round-2 trials in ``PML-STUDY-PIPE-001``: the exact Up-to-West ELBOW
form and the exact vertical REDUCER form. Other bearings, component families
and multi-component routes stay unavailable to the verified API; the native
stress-test API below can emit copied native forms as explicitly experimental
evidence packages.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Iterable, Tuple

from .pml_builder import PMLValidationError, validate_pml

__all__ = [
    "BranchSpec",
    "ElbowSpec",
    "NativeCatalogueComponentSpec",
    "PipeSpec",
    "PipingBuilder",
    "VerticalReducerSpec",
    "build_pipe",
]


Point3 = Tuple[float, float, float]

_NAME = re.compile(r"^/[A-Za-z0-9_.:/-]+$")
_DIRECTION = re.compile(
    r"^(?:[ENWSDU])(?:\s+(?:\d+(?:\.\d+)?)\s+[ENWSDU])?$",
    re.IGNORECASE,
)
_CONNECTION = re.compile(r"^[A-Za-z0-9_-]+$")
_DB_PATH = re.compile(r"^/[A-Za-z0-9_.:/-]+$")


def _fmt(value: float) -> str:
    if not math.isfinite(value):
        raise PMLValidationError(f"Piping coordinate must be finite, got {value!r}")
    if abs(value) < 0.000_000_1:
        value = 0.0
    text = f"{value:.6f}".rstrip("0").rstrip(".")
    return text or "0"


def _name(value: str, label: str) -> str:
    if not _NAME.fullmatch(value):
        raise PMLValidationError(
            f"{label} must be an absolute E3D name without spaces, got {value!r}"
        )
    return value


def _db_path(value: str, label: str) -> str:
    if not _DB_PATH.fullmatch(value):
        raise PMLValidationError(
            f"{label} must be an absolute E3D database path, got {value!r}"
        )
    return value


def _direction(value: str, label: str) -> str:
    value = " ".join(value.upper().split())
    if not _DIRECTION.fullmatch(value):
        raise PMLValidationError(
            f"{label} must be a cardinal direction, optionally with one "
            f"angle/direction pair (for example 'E 0.5729 D'), got {value!r}"
        )
    return value


def _connection(value: str, label: str) -> str:
    value = value.upper()
    if not _CONNECTION.fullmatch(value):
        raise PMLValidationError(
            f"{label} must be one E3D connection token, got {value!r}"
        )
    return value


def _positive(value: float, label: str) -> float:
    if not math.isfinite(value) or value <= 0:
        raise PMLValidationError(f"{label} must be positive and finite, got {value!r}")
    return value


_ELEMENT_TYPE = re.compile(r"^[A-Z][A-Z0-9_]*$")
_ORIENTATION = re.compile(
    r"^[XYZ] IS [ENWSDU](?: [0-9]+(?:\.[0-9]+)? [ENWSDU])?"
    r"(?: AND [XYZ] IS [ENWSDU](?: [0-9]+(?:\.[0-9]+)? [ENWSDU])?)+$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class NativeCatalogueComponentSpec:
    """A copied native catalogue block for an EXPERIMENTAL stress study.

    This is intentionally lower-trust than :class:`ElbowSpec` and
    :class:`VerticalReducerSpec`: the caller must supply the exact native
    element type, orientation, SPCO paths and optional attributes. It is for a
    bounded E3D trial, never an unlabelled production default.
    """

    element_type: str
    position: Point3
    orientation: str
    spref: str
    lstu: str
    name: str | None = None
    attributes: Tuple[Tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        kind = self.element_type.upper()
        if not _ELEMENT_TYPE.fullmatch(kind):
            raise PMLValidationError(f"Invalid catalogue element type {self.element_type!r}")
        object.__setattr__(self, "element_type", kind)
        if len(self.position) != 3:
            raise PMLValidationError(
                f"{kind} position must contain E/N/U coordinates"
            )
        for coordinate in self.position:
            _fmt(coordinate)
        orientation = " ".join(self.orientation.upper().split())
        if not _ORIENTATION.fullmatch(orientation):
            raise PMLValidationError(
                f"{kind} orientation is not a native Y/Z basis: {self.orientation!r}"
            )
        object.__setattr__(self, "orientation", orientation)
        _db_path(self.spref, f"{kind} SPRE component")
        _db_path(self.lstu, f"{kind} LSTU component")
        if self.name is not None:
            _name(self.name, f"{kind} name")
        for verb, value in self.attributes:
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", verb.upper()):
                raise PMLValidationError(f"Invalid native attribute verb {verb!r}")
            if not value or "\n" in value or "\r" in value:
                raise PMLValidationError(f"Invalid value for native attribute {verb!r}")


@dataclass(frozen=True)
class ElbowSpec:
    """
    The E3D Design Mk3.1.11.0 VERIFIED candidate-06 elbow contract.

    This is deliberately the exact Up-to-West form tested in E3D. In
    particular, ``ARRI 2`` and ``LEAV 1`` are mandatory: omitting them made the
    adjacent legs dashed/ill-defined, while restoring them produced a continuous
    solid route. Other elbow bearings need their own native-axis evidence before
    this API is generalized.
    """

    position: Point3
    component: str
    leave_tube: str
    bore: float
    name: str | None = None

    def __post_init__(self) -> None:
        if len(self.position) != 3:
            raise PMLValidationError("ELBOW position must contain E/N/U coordinates")
        for coordinate in self.position:
            _fmt(coordinate)
        _db_path(self.component, "ELBOW SPRE component")
        _db_path(self.leave_tube, "ELBOW LSTU component")
        _positive(self.bore, "ELBOW bore")
        if self.name is not None:
            _name(self.name, "ELBOW name")


@dataclass(frozen=True)
class VerticalReducerSpec:
    """
    The E3D Design Mk3.1.11.0 VERIFIED candidate-07 vertical reducer contract.

    ``ORI Y IS N AND Z IS E`` is the native vertical basis that aligned the
    REDUCER and both adjacent legs. This class intentionally does not accept an
    arbitrary orientation; horizontal/skew reducers remain evidence-gated.
    """

    position: Point3
    component: str
    leave_tube: str
    head_bore: float
    tail_bore: float
    name: str | None = None

    def __post_init__(self) -> None:
        if len(self.position) != 3:
            raise PMLValidationError(
                "REDUCER position must contain E/N/U coordinates"
            )
        for coordinate in self.position:
            _fmt(coordinate)
        _db_path(self.component, "REDUCER SPRE component")
        _db_path(self.leave_tube, "REDUCER LSTU component")
        _positive(self.head_bore, "REDUCER head bore")
        _positive(self.tail_bore, "REDUCER tail bore")
        if self.head_bore == self.tail_bore:
            raise PMLValidationError("REDUCER head and tail bores must differ")
        if self.name is not None:
            _name(self.name, "REDUCER name")


PipingComponent = ElbowSpec | VerticalReducerSpec | NativeCatalogueComponentSpec


def _point_line(verb: str, point: Point3) -> str:
    east, north, up = point
    return (
        f"{verb} E {_fmt(east)}mm N {_fmt(north)}mm U {_fmt(up)}mm"
    )


@dataclass(frozen=True)
class BranchSpec:
    """A free-ended BRANCH whose intervening tube is routed implicitly."""

    name: str
    head: Point3
    tail: Point3
    head_direction: str
    tail_direction: str
    head_bore: float
    tail_bore: float
    tube_component: str
    head_connection: str = "OPEN"
    tail_connection: str = "OPEN"
    slope_ref: str | None = None
    components: Tuple[PipingComponent, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _name(self.name, "BRANCH name")
        if self.head == self.tail:
            raise PMLValidationError(
                f"BRANCH {self.name} head and tail positions must differ"
            )
        for label, point in (("head", self.head), ("tail", self.tail)):
            if len(point) != 3:
                raise PMLValidationError(
                    f"BRANCH {self.name} {label} must contain E/N/U coordinates"
                )
            for coordinate in point:
                _fmt(coordinate)
        _direction(self.head_direction, "HDIR")
        _direction(self.tail_direction, "TDIR")
        _positive(self.head_bore, "HBOR")
        _positive(self.tail_bore, "TBOR")
        _db_path(self.tube_component, "HSTU component")
        _connection(self.head_connection, "HCON")
        _connection(self.tail_connection, "TCON")
        if self.slope_ref is not None:
            _db_path(self.slope_ref, "SLOREF")
        if len(self.components) > 1 and not all(
            isinstance(component, NativeCatalogueComponentSpec)
            for component in self.components
        ):
            raise PMLValidationError(
                f"BRANCH {self.name} supports one verified component at a time; "
                f"multi-component routes must use explicit native stress specs"
            )
        for component in self.components:
            if isinstance(component, ElbowSpec):
                if (
                    component.bore != self.head_bore
                    or component.bore != self.tail_bore
                ):
                    raise PMLValidationError(
                        f"ELBOW bore {component.bore} must match BRANCH "
                        f"HBOR/TBOR {self.head_bore}/{self.tail_bore}"
                    )
            elif isinstance(component, VerticalReducerSpec):
                if (
                    component.head_bore != self.head_bore
                    or component.tail_bore != self.tail_bore
                ):
                    raise PMLValidationError(
                        f"REDUCER bores {component.head_bore}/"
                        f"{component.tail_bore} must match BRANCH HBOR/TBOR "
                        f"{self.head_bore}/{self.tail_bore}"
                    )
            elif isinstance(component, NativeCatalogueComponentSpec):
                # Native stress blocks carry their own catalogue P-points and
                # are intentionally not inferred against branch bores here.
                pass
            else:
                raise PMLValidationError(
                    f"BRANCH {self.name} contains an unsupported component "
                    f"{type(component).__name__}"
                )


@dataclass(frozen=True)
class PipeSpec:
    """Administrative PIPE owner and its E3D Design Mk3.1.11.0 free branches."""

    name: str
    specification: str
    branches: Tuple[BranchSpec, ...] = field(default_factory=tuple)
    bore: float | None = None
    temperature_c: float = 20.0
    pressure_pa: float = 0.0
    test_pressure_pa: float = 0.0
    slope_ref: str | None = None

    def __post_init__(self) -> None:
        _name(self.name, "PIPE name")
        _db_path(self.specification, "PSPE specification")
        if not self.branches:
            raise PMLValidationError(f"PIPE {self.name} must own at least one BRANCH")
        if len({branch.name.upper() for branch in self.branches}) != len(
            self.branches
        ):
            raise PMLValidationError(f"PIPE {self.name} contains duplicate BRANCH names")
        if self.bore is not None:
            _positive(self.bore, "PIPE BORE")
        for value, label in (
            (self.temperature_c, "PIPE TEMP"),
            (self.pressure_pa, "PIPE PRES"),
            (self.test_pressure_pa, "PIPE TPRESS"),
        ):
            if not math.isfinite(value):
                raise PMLValidationError(f"{label} must be finite, got {value!r}")
        if self.pressure_pa < 0 or self.test_pressure_pa < 0:
            raise PMLValidationError("PIPE pressure values cannot be negative")
        if self.slope_ref is not None:
            _db_path(self.slope_ref, "PIPE SLOREF")
        for branch in self.branches:
            if not branch.name.upper().startswith(self.name.upper() + "/"):
                raise PMLValidationError(
                    f"BRANCH {branch.name} must be named beneath its PIPE "
                    f"{self.name}"
                )
            if branch.slope_ref and branch.slope_ref != self.slope_ref:
                raise PMLValidationError(
                    f"BRANCH {branch.name} SLOREF {branch.slope_ref} differs "
                    f"from PIPE {self.name} SLOREF {self.slope_ref}; the "
                    f"verified form carries the same reference on both"
                )


class PipingBuilder:
    """
    Emit native-canonical PIPE/BRANCH blocks beneath the current E3D ZONE.

    The caller selects or creates the owning ZONE.  This builder intentionally
    emits no INPUT transaction, synonym control, error handler or render
    prologue: the deliverable remains element-creation PML only.
    """

    def __init__(self) -> None:
        self._lines: list[str] = []
        self.pipe_count = 0
        self.branch_count = 0

    def comment(self, text: str) -> "PipingBuilder":
        for line in text.splitlines() or [""]:
            self._lines.append(f"-- {line}".rstrip())
        return self

    def pipe(self, spec: PipeSpec) -> "PipingBuilder":
        self._lines.append(f"NEW PIPE {spec.name}")
        if spec.bore is not None:
            self._lines.append(f"BORE {_fmt(spec.bore)}mm")
        self._lines.extend(
            (
                f"TEMP {_fmt(spec.temperature_c)}degC",
                f"PRES {_fmt(spec.pressure_pa)}pascal",
                f"TPRESS {_fmt(spec.test_pressure_pa)}pascal",
                f"PSPE SPECIFICATION {spec.specification}",
            )
        )
        if spec.slope_ref:
            self._lines.append(f"SLOREF SLOELE {spec.slope_ref}")

        for branch in spec.branches:
            self._branch(branch, spec)

        self._lines.extend(("END", ""))
        self.pipe_count += 1
        return self

    def _branch(self, branch: BranchSpec, pipe: PipeSpec) -> None:
        self._lines.extend(
            (
                f"NEW BRANCH {branch.name}",
                _point_line("HPOS", branch.head),
                _point_line("TPOS", branch.tail),
                f"HDIR {_direction(branch.head_direction, 'HDIR')}",
                f"TDIR {_direction(branch.tail_direction, 'TDIR')}",
                "LHEA true",
                "LTAI true",
                f"HBOR {_fmt(branch.head_bore)}mm",
                f"TBOR {_fmt(branch.tail_bore)}mm",
                f"HCON {_connection(branch.head_connection, 'HCON')}",
                f"TCON {_connection(branch.tail_connection, 'TCON')}",
                f"TEMP {_fmt(pipe.temperature_c)}degC",
                f"PRES {_fmt(pipe.pressure_pa)}pascal",
                f"TPRESS {_fmt(pipe.test_pressure_pa)}pascal",
                f"HSTU SPCOMPONENT {branch.tube_component}",
                f"PSPE SPECIFICATION {pipe.specification}",
            )
        )
        if branch.slope_ref:
            self._lines.append(f"SLOREF SLOELE {branch.slope_ref}")
        for component in branch.components:
            self._component(component)
        self._lines.append("END")
        self.branch_count += 1

    def _component(self, component: PipingComponent) -> None:
        if isinstance(component, ElbowSpec):
            new_line = "NEW ELBOW"
            orientation = "ORI Y IS D AND Z IS N"
            attributes = (("ARRI", "2"), ("LEAV", "1"))
            spref = component.component
            lstu = component.leave_tube
        elif isinstance(component, VerticalReducerSpec):
            new_line = "NEW REDUCER"
            orientation = "ORI Y IS N AND Z IS E"
            attributes = ()
            spref = component.component
            lstu = component.leave_tube
        else:
            new_line = f"NEW {component.element_type}"
            orientation = f"ORI {component.orientation}"
            attributes = component.attributes
            spref = component.spref
            lstu = component.lstu
        if component.name:
            new_line += f" {component.name}"
        self._lines.extend(
            (
                new_line,
                _point_line("POS", component.position),
                orientation,
                "BUIL false",
                "SHOP true",
                f"SPRE SPCOMPONENT {spref}",
                f"LSTU SPCOMPONENT {lstu}",
            )
        )
        for verb, value in attributes:
            self._lines.append(f"{verb.upper()} {value}")
        self._lines.extend(("ORIF true", "POSF true", "END"))

    def extend(self, pipes: Iterable[PipeSpec]) -> "PipingBuilder":
        for pipe in pipes:
            self.pipe(pipe)
        return self

    def build(self) -> str:
        script = "\n".join(self._lines).rstrip() + "\n"
        problems = validate_pml(script)
        if problems:
            raise PMLValidationError(
                "Generated PIPE macro failed validation:\n  "
                + "\n  ".join(problems)
            )
        return script


def build_pipe(spec: PipeSpec) -> str:
    """Build one PIPE macro fragment beneath the current writable ZONE."""

    return PipingBuilder().pipe(spec).build()
