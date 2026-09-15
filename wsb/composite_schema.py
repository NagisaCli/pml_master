"""
Generic Composite Equipment Schema
==================================

Resolved geometry for equipment that cannot be described by the original
single-shell :class:`wsb.schema.TankSpec`.  A project owns the dimensions and
configuration; this module only provides the common vocabulary needed to emit
and verify a model made from E3D primitives.

Every point is expressed in a local frame whose origin is the equipment bottom
centre.  CYLI/CONE use a *base-face* datum and are converted to E3D's
geometric-centre datum by :class:`wsb.pml_builder.PMLBuilder`; DISH uses its
flat rim / tangent-plane datum directly.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

from .pml_parser import pyramid_bounds

__all__ = [
    "Bounds",
    "EquipmentModel",
    "NativeNozzleSpec",
    "ParameterRecord",
    "PrimitiveSpec",
    "ReferenceValue",
    "SourceRecord",
]


Point = Tuple[float, float, float]
Bounds = Tuple[float, float, float, float, float, float]

_AXIS_VECTOR = {
    "U": (0.0, 0.0, 1.0),
    "D": (0.0, 0.0, -1.0),
    "E": (1.0, 0.0, 0.0),
    "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0),
    "S": (0.0, -1.0, 0.0),
}


@dataclass(frozen=True)
class SourceRecord:
    """A project source used to resolve geometry."""

    label: str
    detail: str
    url: str = ""


@dataclass(frozen=True)
class ParameterRecord:
    """A reader-facing model parameter and its provenance."""

    name: str
    value: str
    source: str


@dataclass(frozen=True)
class ReferenceValue:
    """A value not supplied as contractual project data."""

    parameter: str
    value: str
    basis: str


@dataclass(frozen=True)
class NativeNozzleSpec:
    """One catalogue-backed E3D NOZZLE in equipment-local coordinates."""

    group: str
    name: str
    dn: int
    height: float
    face: Point
    axis: str
    label: str

    def __post_init__(self) -> None:
        axis = self.axis.upper()
        object.__setattr__(self, "axis", axis)
        if not self.group.strip() or not self.name.strip():
            raise ValueError("Native nozzle group and name are required")
        if self.dn <= 0:
            raise ValueError(f"{self.name}: nozzle DN must be positive")
        if not 1.0 <= self.height <= 2000.0:
            raise ValueError(
                f"{self.name}: nozzle height {self.height} mm is implausible"
            )
        if axis not in _AXIS_VECTOR:
            raise ValueError(f"{self.name}: unknown nozzle axis {axis!r}")
        if not self.label.strip():
            raise ValueError(f"{self.name}: nozzle label is required")

    def translated_face(self, origin: Point) -> Point:
        return tuple(
            self.face[index] + origin[index] for index in range(3)
        )  # type: ignore[return-value]


@dataclass(frozen=True)
class PrimitiveSpec:
    """
    One resolved E3D primitive in equipment-local coordinates.

    ``point`` is the base-face centre for CYLI/CONE, the rim-plane centre for
    DISH and the geometric centre for BOX and PYRAMID. ``plan_rotation_deg``
    rotates a BOX or PYRAMID local X axis from East towards North while
    keeping local Z vertical. A PYRAMID's top rectangle may be shifted by
    ``xoff``/``yoff`` in that local frame, which is how an inclined leg or
    stay is drawn from verified primitives (IR-1). ``role='body'`` marks the
    authoritative vessel envelope; supports, nozzle assemblies and visible
    detail use other role names.
    """

    group: str
    kind: str
    point: Point
    label: str
    role: str = "detail"
    axis: str = "U"
    diameter: float = 0.0
    height: float = 0.0
    d_bottom: float = 0.0
    d_top: float = 0.0
    radius: float = 0.0
    xlen: float = 0.0
    ylen: float = 0.0
    zlen: float = 0.0
    xbot: float = 0.0
    ybot: float = 0.0
    xtop: float = 0.0
    ytop: float = 0.0
    xoff: float = 0.0
    yoff: float = 0.0
    plan_rotation_deg: float = 0.0
    vertices: Tuple[Tuple[float, float], ...] = ()
    orientation: str = ""
    level: Optional[Tuple[int, int]] = None

    def __post_init__(self) -> None:
        kind = self.kind.upper()
        axis = self.axis.upper()
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "axis", axis)

        if not self.group.strip():
            raise ValueError("Primitive group cannot be blank")
        if not self.label.strip():
            raise ValueError("Primitive label cannot be blank")
        if kind not in {"CYLI", "CONE", "DISH", "BOX", "PYRAMID", "EXTRUSION"}:
            raise ValueError(f"Unsupported primitive kind {kind!r}")

        if kind == "EXTRUSION":
            if not self.vertices or len(self.vertices) < 3:
                raise ValueError("EXTRUSION needs at least 3 vertices")
            if self.height <= 0:
                raise ValueError(f"EXTRUSION needs positive height, got {self.height}")
            if not self.orientation.strip():
                object.__setattr__(self, "orientation", "Y IS N AND Z IS U")
            return

        if kind == "BOX":
            if min(self.xlen, self.ylen, self.zlen) <= 0:
                raise ValueError(
                    f"BOX needs positive dimensions, got "
                    f"{self.xlen} x {self.ylen} x {self.zlen}"
                )
            if not math.isfinite(self.plan_rotation_deg):
                raise ValueError(
                    f"BOX plan rotation must be finite, got "
                    f"{self.plan_rotation_deg}"
                )
            object.__setattr__(
                self, "plan_rotation_deg", self.plan_rotation_deg % 360.0
            )
            return
        if kind == "PYRAMID":
            if self.height <= 0:
                raise ValueError(
                    f"PYRAMID needs positive height, got {self.height}"
                )
            if min(self.xbot, self.ybot) <= 0 or min(self.xtop, self.ytop) < 0:
                raise ValueError(
                    f"PYRAMID needs XBOT/YBOT > 0 and XTOP/YTOP >= 0, got "
                    f"{self.xbot} x {self.ybot} -> {self.xtop} x {self.ytop}"
                )
            for value in (self.xoff, self.yoff, self.plan_rotation_deg):
                if not math.isfinite(value):
                    raise ValueError(
                        f"PYRAMID offsets and rotation must be finite, got "
                        f"{self.xoff}, {self.yoff}, {self.plan_rotation_deg}"
                    )
            object.__setattr__(
                self, "plan_rotation_deg", self.plan_rotation_deg % 360.0
            )
            return
        if self.plan_rotation_deg != 0.0:
            raise ValueError(
                f"{kind} does not use BOX plan rotation "
                f"{self.plan_rotation_deg}"
            )

        if axis not in _AXIS_VECTOR:
            raise ValueError(f"Unknown primitive axis {axis!r}")
        if self.height <= 0:
            raise ValueError(f"{kind} needs positive height, got {self.height}")
        if kind in {"CYLI", "DISH"} and self.diameter <= 0:
            raise ValueError(f"{kind} needs positive diameter, got {self.diameter}")
        if kind == "CONE" and (
            self.d_bottom <= 0 or self.d_top < 0
        ):
            raise ValueError(
                f"CONE needs DBOT > 0 and DTOP >= 0, got "
                f"{self.d_bottom}, {self.d_top}"
            )

    @classmethod
    def cyli(
        cls,
        group: str,
        diameter: float,
        height: float,
        base: Point,
        label: str,
        *,
        axis: str = "U",
        role: str = "detail",
    ) -> "PrimitiveSpec":
        return cls(
            group=group,
            kind="CYLI",
            point=base,
            label=label,
            role=role,
            axis=axis,
            diameter=diameter,
            height=height,
        )

    @classmethod
    def cone(
        cls,
        group: str,
        d_bottom: float,
        d_top: float,
        height: float,
        base: Point,
        label: str,
        *,
        axis: str = "U",
        role: str = "detail",
    ) -> "PrimitiveSpec":
        return cls(
            group=group,
            kind="CONE",
            point=base,
            label=label,
            role=role,
            axis=axis,
            d_bottom=d_bottom,
            d_top=d_top,
            height=height,
        )

    @classmethod
    def dish(
        cls,
        group: str,
        diameter: float,
        height: float,
        base: Point,
        label: str,
        *,
        axis: str = "U",
        radius: Optional[float] = None,
        role: str = "detail",
    ) -> "PrimitiveSpec":
        return cls(
            group=group,
            kind="DISH",
            point=base,
            label=label,
            role=role,
            axis=axis,
            diameter=diameter,
            height=height,
            radius=diameter if radius is None else radius,
        )

    @classmethod
    def box(
        cls,
        group: str,
        xlen: float,
        ylen: float,
        zlen: float,
        centre: Point,
        label: str,
        *,
        role: str = "detail",
        plan_rotation_deg: float = 0.0,
    ) -> "PrimitiveSpec":
        return cls(
            group=group,
            kind="BOX",
            point=centre,
            label=label,
            role=role,
            xlen=xlen,
            ylen=ylen,
            zlen=zlen,
            plan_rotation_deg=plan_rotation_deg,
        )

    @classmethod
    def pyramid(
        cls,
        group: str,
        xbot: float,
        ybot: float,
        xtop: float,
        ytop: float,
        height: float,
        centre: Point,
        label: str,
        *,
        xoff: float = 0.0,
        yoff: float = 0.0,
        plan_rotation_deg: float = 0.0,
        role: str = "detail",
    ) -> "PrimitiveSpec":
        """
        Rectangular frustum positioned by its **geometric centre**.

        With equal top and bottom rectangles and a non-zero ``xoff``/``yoff``
        this is a sheared prism: the verified way to draw an inclined leg or
        stay whose axis is not one of the six cardinal directions. Local X is
        the ``plan_rotation_deg`` bearing, so for a vessel leg ``xoff`` is the
        radial splay of the top face relative to the bottom face.
        """
        return cls(
            group=group,
            kind="PYRAMID",
            point=centre,
            label=label,
            role=role,
            xbot=xbot,
            ybot=ybot,
            xtop=xtop,
            ytop=ytop,
            height=height,
            xoff=xoff,
            yoff=yoff,
            plan_rotation_deg=plan_rotation_deg,
        )

    @classmethod
    def extrusion(
        cls,
        group: str,
        point: Point,
        height: float,
        vertices: Iterable[Tuple[float, float]],
        label: str,
        *,
        orientation: str = "Y IS N AND Z IS U",
        role: str = "detail",
        level: Optional[Tuple[int, int]] = None,
    ) -> "PrimitiveSpec":
        return cls(
            group=group,
            kind="EXTRUSION",
            point=point,
            label=label,
            role=role,
            height=height,
            orientation=orientation,
            vertices=tuple(vertices),
            level=level,
        )

    @classmethod
    def hex_nut(
        cls,
        group: str,
        point: Point,
        across_flats: float,
        height: float,
        label: str,
        *,
        orientation: str = "Y IS N AND Z IS U",
        role: str = "hardware",
        rotation_deg: float = 0.0,
    ) -> "PrimitiveSpec":
        r = across_flats / math.sqrt(3.0)
        half_flat = across_flats / 2.0
        base_pts = [
            (r, 0.0),
            (r / 2.0, half_flat),
            (-r / 2.0, half_flat),
            (-r, 0.0),
            (-r / 2.0, -half_flat),
            (r / 2.0, -half_flat),
        ]
        if abs(rotation_deg) > 1e-9:
            ang = math.radians(rotation_deg)
            cos_a, sin_a = math.cos(ang), math.sin(ang)
            base_pts = [
                (cos_a * x - sin_a * y, sin_a * x + cos_a * y) for x, y in base_pts
            ]
        return cls.extrusion(
            group=group,
            point=point,
            height=height,
            vertices=base_pts,
            label=label,
            role=role,
            orientation=orientation,
        )

    @property
    def cross_diameter(self) -> float:
        if self.kind == "CONE":
            return max(self.d_bottom, self.d_top)
        return self.diameter

    def bounds(self) -> Bounds:
        """Local axis-aligned occupied bounds of this primitive."""
        e, n, u = self.point
        if self.kind == "EXTRUSION":
            xs = [v[0] for v in self.vertices]
            ys = [v[1] for v in self.vertices]
            return (
                e + min(xs),
                e + max(xs),
                n + min(ys),
                n + max(ys),
                u,
                u + self.height,
            )

        if self.kind == "BOX":
            angle = math.radians(self.plan_rotation_deg)
            cosine = abs(math.cos(angle))
            sine = abs(math.sin(angle))
            half_e = cosine * self.xlen / 2.0 + sine * self.ylen / 2.0
            half_n = sine * self.xlen / 2.0 + cosine * self.ylen / 2.0
            return (
                e - half_e,
                e + half_e,
                n - half_n,
                n + half_n,
                u - self.zlen / 2.0,
                u + self.zlen / 2.0,
            )

        if self.kind == "PYRAMID":
            return pyramid_bounds(
                self.point,
                self.xbot,
                self.ybot,
                self.xtop,
                self.ytop,
                self.height,
                xoff=self.xoff,
                yoff=self.yoff,
                plan_rotation_deg=self.plan_rotation_deg,
            )

        de, dn, du = _AXIS_VECTOR[self.axis]
        end = (
            e + de * self.height,
            n + dn * self.height,
            u + du * self.height,
        )
        radius = self.cross_diameter / 2.0
        e_min, e_max = sorted((e, end[0]))
        n_min, n_max = sorted((n, end[1]))
        u_min, u_max = sorted((u, end[2]))

        if de == 0.0:
            e_min -= radius
            e_max += radius
        if dn == 0.0:
            n_min -= radius
            n_max += radius
        if du == 0.0:
            u_min -= radius
            u_max += radius
        return (e_min, e_max, n_min, n_max, u_min, u_max)

    def translated_bounds(self, origin: Point) -> Bounds:
        e, n, u = origin
        b = self.bounds()
        return (
            b[0] + e,
            b[1] + e,
            b[2] + n,
            b[3] + n,
            b[4] + u,
            b[5] + u,
        )


@dataclass(frozen=True)
class EquipmentModel:
    """A complete, resolved equipment model ready for PML generation."""

    name: str
    display_name: str
    area: str
    position: Point
    overall_height: float
    main_dimensions: str
    primitives: Tuple[PrimitiveSpec, ...]
    body_envelope: Bounds
    capacity_m3: Optional[float] = None
    nozzle_groups: Tuple[str, ...] = ()
    native_nozzles: Tuple[NativeNozzleSpec, ...] = ()
    parameters: Tuple[ParameterRecord, ...] = ()
    reference_values: Tuple[ReferenceValue, ...] = ()
    sources: Tuple[SourceRecord, ...] = ()
    notes: Tuple[str, ...] = ()
    outstanding: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.display_name.strip():
            raise ValueError("Equipment name and display name are required")
        if self.overall_height <= 0:
            raise ValueError(
                f"{self.display_name}: overall height must be positive"
            )
        if not self.primitives:
            raise ValueError(f"{self.display_name}: no primitives resolved")
        if self.body_envelope[4] < -0.2:
            raise ValueError(
                f"{self.display_name}: body envelope falls below local datum"
            )
        if self.body_envelope[5] > self.overall_height + 0.2:
            raise ValueError(
                f"{self.display_name}: body envelope exceeds overall height"
            )
        if len({nozzle.name for nozzle in self.native_nozzles}) != len(
            self.native_nozzles
        ):
            raise ValueError(f"{self.display_name}: duplicate native nozzle name")
        native_groups = {nozzle.group for nozzle in self.native_nozzles}
        if native_groups != set(self.nozzle_groups):
            raise ValueError(
                f"{self.display_name}: native nozzle groups {sorted(native_groups)} "
                f"do not match schedule {sorted(self.nozzle_groups)}"
            )

    @property
    def primitive_count(self) -> int:
        return len(self.primitives)

    @property
    def nozzle_count(self) -> int:
        return len(self.nozzle_groups)

    def groups(self) -> Tuple[str, ...]:
        """Hierarchy groups with body/support first and native nozzles separate."""
        primitive_order = []
        for primitive in self.primitives:
            if primitive.group not in primitive_order:
                primitive_order.append(primitive.group)

        accessories = {"INTERNALS", "ACCESS", "DETAIL"}
        seen = [
            group for group in primitive_order if group not in accessories
        ]
        for group in self.nozzle_groups:
            if group not in seen:
                seen.append(group)
        for group in primitive_order:
            if group not in seen:
                seen.append(group)
        return tuple(seen)

    def primitives_for_group(self, group: str) -> Iterable[PrimitiveSpec]:
        return (p for p in self.primitives if p.group == group)

    def nozzles_for_group(self, group: str) -> Iterable[NativeNozzleSpec]:
        return (nozzle for nozzle in self.native_nozzles if nozzle.group == group)
