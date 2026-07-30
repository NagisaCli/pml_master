"""
High-detail Horizontal Pump Geometry Builder
============================================

Builds one independently selectable E3D ``EQUI`` per pump. Geometry is laid
out in a local frame whose longitudinal positive direction points from the
driver toward the pump casing, then transformed to world E/N/U coordinates.

Contractual/project parameters stay in ``PumpSpec``. Every dimension introduced
here is an explicitly bounded engineering Reference Value. The high-detail
model adds construction that is visible on a real long-coupled pump set:

* welded base rails, cross-members and exposed anchor fasteners;
* radially split volute casing, cover, ribs and flange-face bolting;
* seal housing, multi-diameter bearing bracket and oil/grease fittings;
* flexible coupling, hubs, clamp bands and a guarded coupling;
* TEFC motor barrel, end bells, feet, fins, fan grille, terminal box and bolts;
* service-specific clean-out, inspection, vent or seal-flush details;
* tag-specific MC-pump degassing/separation and auxiliary-drive arrangements.

Only PML1 primitives proven by this repository are used. Primitive ``POS`` is
always a geometric centre through ``PMLBuilder``; oriented primitives always
emit ``ORI`` before ``POS``.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

from .pml_builder import PMLBuilder, validate_pml
from .pump_schema import (
    CasingStyle,
    CouplingGuardStyle,
    MotorStyle,
    PumpDuty,
    PumpFamily,
    PumpSpec,
)
from .tank_builder import _parse_primitives

__all__ = [
    "DerivedPumpGeometry",
    "PumpDetailProfile",
    "PumpBuilder",
    "derive_detail_profile",
    "derive_pump_geometry",
    "verify_pump",
]


_AXIS_VECTOR: Dict[str, Tuple[float, float]] = {
    "E": (1.0, 0.0),
    "W": (-1.0, 0.0),
    "N": (0.0, 1.0),
    "S": (0.0, -1.0),
}
_OPPOSITE = {"E": "W", "W": "E", "N": "S", "S": "N", "U": "D", "D": "U"}
_TOLERANCE_MM = 0.25
_MOTOR_BODY_FACTOR = {
    MotorStyle.IEC_STANDARD: 0.82,
    MotorStyle.HEAVY_DUTY: 0.86,
    MotorStyle.HIGH_SPEED: 0.78,
    MotorStyle.CHEMICAL_DUTY: 0.81,
    MotorStyle.MC_MAIN_DRIVE: 0.85,
}


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _odd(value: int, low: int, high: int) -> int:
    bounded = max(low, min(high, value))
    return bounded if bounded % 2 else min(high, bounded + 1)


def _dn_for_width(width: float, *, discharge: bool = False, mc: bool = False) -> int:
    """Engineering Reference Value: a catalogue-supported nominal bore."""
    if mc:
        base = 200 if width >= 1000 else 150
    elif width >= 1150:
        base = 150
    elif width >= 820:
        base = 100
    else:
        base = 80
    if discharge and base > 80:
        return {100: 80, 150: 100, 200: 150}[base]
    return base


@dataclass(frozen=True)
class DerivedPumpGeometry:
    """All non-contractual envelope dimensions used to build one pump."""

    rail_height: float
    rail_width: float
    motor_length: float
    motor_width: float
    motor_height: float
    motor_centre_l: float
    shaft_u: float
    casing_length: float
    casing_diameter: float
    casing_centre_l: float
    coupling_length: float
    suction_dn: int
    discharge_dn: int
    suction_length: float
    discharge_length: float
    overall_height: float


@dataclass(frozen=True)
class PumpDetailProfile:
    """Visible construction choices derived from service and skid scale."""

    duty: PumpDuty
    appearance_code: str
    motor_style: MotorStyle
    casing_style: CasingStyle
    guard_style: CouplingGuardStyle
    motor_fin_count: int
    casing_bolt_count: int
    anchor_bolt_count: int
    crossmember_count: int
    casing_rib_count: int
    bearing_sections: int
    terminal_mount_side: int
    cable_gland_side: int
    service_feature: str
    mc_variant: str

    @property
    def signature(self) -> str:
        return (
            f"{self.appearance_code}:{self.motor_style.name}:"
            f"{self.casing_style.name}:{self.guard_style.name}:"
            f"f{self.motor_fin_count}:c{self.casing_bolt_count}:"
            f"a{self.anchor_bolt_count}:x{self.crossmember_count}:"
            f"r{self.casing_rib_count}:b{self.bearing_sections}:"
            f"tm{self.terminal_mount_side:+d}:g{self.cable_gland_side:+d}:"
            f"{self.service_feature}:{self.mc_variant}"
        )


_SERVICE_FEATURE = {
    PumpDuty.DILUTION: "casing vent and flush boss",
    PumpDuty.FILTRATE: "side inspection and drain boss",
    PumpDuty.SCREEN_FEED: "heavy clean-out cover",
    PumpDuty.BOOSTER: "compact pressure tapping and reinforced bearing frame",
    PumpDuty.WIRE_WASH: "compact seal housing and pressure tapping",
    PumpDuty.WASHER_FEED: "stock-duty clean-out cover",
    PumpDuty.MEDIUM_CONSISTENCY: "integrated separation and degassing package",
    PumpDuty.SCRUBBER_CIRCULATION: "seal-flush manifold and splash shield",
}


def derive_detail_profile(
    spec: PumpSpec, geometry: DerivedPumpGeometry | None = None
) -> PumpDetailProfile:
    """Resolve the explicit tag profile plus scale-dependent skid details."""
    _ = geometry or derive_pump_geometry(spec)
    appearance = spec.appearance
    anchor_count = 8 if spec.length >= 2000.0 or spec.width >= 1000.0 else 6
    crossmembers = 4 if spec.length >= 2000.0 else 3
    return PumpDetailProfile(
        duty=spec.duty,
        appearance_code=appearance.code,
        motor_style=appearance.motor_style,
        casing_style=appearance.casing_style,
        guard_style=appearance.guard_style,
        motor_fin_count=appearance.fin_count,
        casing_bolt_count=appearance.casing_bolt_count,
        anchor_bolt_count=anchor_count,
        crossmember_count=crossmembers,
        casing_rib_count=appearance.casing_rib_count,
        bearing_sections=appearance.bearing_sections,
        terminal_mount_side=appearance.terminal_mount_side,
        cable_gland_side=appearance.cable_gland_side,
        service_feature=_SERVICE_FEATURE[spec.duty],
        mc_variant=appearance.mc_variant,
    )


def derive_pump_geometry(spec: PumpSpec) -> DerivedPumpGeometry:
    """
    Scale a vendor-neutral pump envelope from the contractual baseplate.

    The baseplate, coordinate, orientation and nozzle directions are never
    altered. These derived dimensions remain bounded Reference Values because
    the workbook contains no vendor GA, shaft elevation or motor schedule.
    """
    length, width, thickness = spec.length, spec.width, spec.baseplate_thickness
    appearance = spec.appearance
    if spec.family is PumpFamily.MEDIUM_CONSISTENCY:
        rail_height = _clamp(width * 0.075, 50.0, 95.0)
        motor_length = min(
            max(
                length * 0.35 * appearance.motor_length_scale,
                width * 0.57,
            ),
            length * 0.46,
        )
        motor_width = width * 0.60
        motor_height = _clamp(
            width * 0.46 * appearance.motor_diameter_scale,
            max(280.0, width * 0.40),
            min(620.0, width * 0.56),
        )
        motor_centre_l = -length * 0.27
        casing_length = _clamp(
            length * 0.30 * appearance.casing_length_scale,
            length * 0.26,
            length * 0.34,
        )
        casing_diameter = _clamp(
            width * 0.46 * appearance.casing_diameter_scale,
            max(300.0, width * 0.40),
            min(580.0, width * 0.54),
        )
        casing_centre_l = length * 0.10
        coupling_length = length * 0.07
        suction_length = _clamp(length * 0.14, 150.0, 300.0)
    else:
        rail_height = _clamp(width * 0.075, 48.0, 90.0)
        motor_length = min(
            length * 0.40 * appearance.motor_length_scale,
            length * 0.46,
        )
        motor_width = width * 0.60
        motor_height = _clamp(
            width * 0.47 * appearance.motor_diameter_scale,
            max(275.0, width * 0.42),
            min(620.0, width * 0.56),
        )
        motor_centre_l = -length * 0.25
        casing_length = _clamp(
            length * 0.20 * appearance.casing_length_scale,
            length * 0.17,
            length * 0.23,
        )
        casing_diameter = _clamp(
            width * 0.38 * appearance.casing_diameter_scale,
            max(230.0, width * 0.31),
            min(520.0, width * 0.50),
        )
        casing_centre_l = length * 0.18
        coupling_length = length * 0.14
        suction_length = _clamp(length * 0.12, 150.0, 250.0)

    # Fit the longitudinal train from real interfaces rather than allowing an
    # enlarged driver to overlap the bearing frame.  _build_bearing_frame uses
    # min(0.52 * motor-to-casing gap, 0.12L); solve that relation backwards so
    # the remaining clear span is exactly the declared coupling length.
    uncapped_total_gap = coupling_length / (1.0 - 0.52)
    if 0.52 * uncapped_total_gap <= length * 0.12:
        required_motor_to_casing_gap = uncapped_total_gap
    else:
        required_motor_to_casing_gap = coupling_length + length * 0.12
    motor_front = motor_centre_l + motor_length / 2.0
    minimum_casing_centre = (
        motor_front
        + required_motor_to_casing_gap
        + casing_length / 2.0
    )
    casing_centre_l = max(casing_centre_l, minimum_casing_centre)

    shaft_u = thickness + rail_height + motor_height / 2.0
    discharge_length = _clamp(width * 0.18, 150.0, 280.0)
    hydraulic_top = (
        shaft_u + casing_diameter / 2.0 + discharge_length
        if spec.discharge_axis.upper() == "U"
        else shaft_u + casing_diameter / 2.0
    )
    detailed_motor_top = thickness + rail_height + motor_height * 1.42
    overall_height = max(hydraulic_top, detailed_motor_top)
    return DerivedPumpGeometry(
        rail_height=rail_height,
        rail_width=_clamp(width * 0.08, 55.0, 100.0),
        motor_length=motor_length,
        motor_width=motor_width,
        motor_height=motor_height,
        motor_centre_l=motor_centre_l,
        shaft_u=shaft_u,
        casing_length=casing_length,
        casing_diameter=casing_diameter,
        casing_centre_l=casing_centre_l,
        coupling_length=coupling_length,
        suction_dn=_dn_for_width(width, mc=spec.is_mc),
        discharge_dn=_dn_for_width(width, discharge=True, mc=spec.is_mc),
        suction_length=suction_length,
        discharge_length=discharge_length,
        overall_height=overall_height,
    )


class PumpBuilder:
    """Emit one high-detail pump under one independent EQUI."""

    def __init__(self, spec: PumpSpec, builder: PMLBuilder) -> None:
        self.spec = spec
        self.b = builder
        self.g = derive_pump_geometry(spec)
        self.detail = derive_detail_profile(spec, self.g)
        forward = _AXIS_VECTOR[spec.layout_axis]
        self._forward = forward
        # Transverse positive points left when looking from driver to casing.
        self._cross = (-forward[1], forward[0])

    def _at(
        self, longitudinal: float = 0.0, transverse: float = 0.0, up: float = 0.0
    ) -> Tuple[float, float, float]:
        east, north, datum_u = self.spec.position
        return (
            east + self._forward[0] * longitudinal + self._cross[0] * transverse,
            north + self._forward[1] * longitudinal + self._cross[1] * transverse,
            datum_u + up,
        )

    def _cross_axis(self, side: int = 1) -> str:
        vector = (self._cross[0] * side, self._cross[1] * side)
        for axis, candidate in _AXIS_VECTOR.items():
            if vector == candidate:
                return axis
        raise ValueError(f"Unsupported transverse vector {vector}")

    def _box(
        self,
        longitudinal: float,
        transverse: float,
        height: float,
        centre_l: float,
        centre_t: float,
        centre_u: float,
        *,
        label: str,
    ) -> None:
        if self.spec.layout_axis in ("E", "W"):
            xlen, ylen = longitudinal, transverse
        else:
            xlen, ylen = transverse, longitudinal
        self.b.box(
            xlen,
            ylen,
            height,
            self._at(centre_l, centre_t, centre_u),
            label=label,
        )

    def _cylinder_local(
        self,
        diameter: float,
        length: float,
        base_l: float,
        base_t: float,
        centre_u: float,
        *,
        positive: bool = True,
        label: str,
    ) -> None:
        axis = self.spec.layout_axis if positive else _OPPOSITE[self.spec.layout_axis]
        self.b.cyli(
            diameter,
            length,
            self._at(base_l, base_t, centre_u),
            axis=axis,
            label=label,
        )

    def _cylinder_cross(
        self,
        diameter: float,
        length: float,
        base_l: float,
        base_t: float,
        centre_u: float,
        *,
        side: int,
        label: str,
    ) -> None:
        self.b.cyli(
            diameter,
            length,
            self._at(base_l, base_t, centre_u),
            axis=self._cross_axis(side),
            label=label,
        )

    def _vertical_fastener(
        self,
        longitudinal: float,
        transverse: float,
        surface_u: float,
        shank_diameter: float,
        *,
        seated: bool = False,
        label: str,
    ) -> None:
        shank_h = _clamp(shank_diameter * 1.35, 18.0, 38.0)
        washer_h = _clamp(shank_diameter * 0.22, 3.0, 6.0)
        head_h = _clamp(shank_diameter * 0.62, 8.0, 16.0)
        shank_base_u = (
            surface_u + washer_h + head_h - shank_h
            if seated
            else surface_u
        )
        head_base_u = surface_u + washer_h if seated else surface_u + shank_h
        self.b.cyli(
            shank_diameter,
            shank_h,
            self._at(longitudinal, transverse, shank_base_u),
            axis="U",
            label=f"{label}: exposed threaded shank Reference Value",
        )
        self.b.cyli(
            shank_diameter * 2.15,
            washer_h,
            self._at(longitudinal, transverse, surface_u),
            axis="U",
            label=f"{label}: solid washer under filled shank Reference Value",
        )
        self.b.cyli(
            shank_diameter * 1.72,
            head_h,
            self._at(longitudinal, transverse, head_base_u),
            axis="U",
            label=f"{label}: cap/hex-head envelope Reference Value",
        )

    def _axial_flange_fastener(
        self,
        face_l: float,
        transverse: float,
        up: float,
        shank_diameter: float,
        *,
        label: str,
    ) -> None:
        washer_t = _clamp(shank_diameter * 0.22, 3.0, 6.0)
        shank_l = _clamp(shank_diameter * 0.95, 14.0, 28.0)
        head_l = _clamp(shank_diameter * 0.58, 8.0, 16.0)
        self._cylinder_local(
            shank_diameter,
            shank_l,
            face_l + washer_t + head_l - shank_l,
            transverse,
            up,
            positive=True,
            label=f"{label}: flange-penetrating stud Reference Value",
        )
        self._cylinder_local(
            shank_diameter * 2.10,
            washer_t,
            face_l,
            transverse,
            up,
            positive=True,
            label=f"{label}: flange-face washer Reference Value",
        )
        self._cylinder_local(
            shank_diameter * 1.72,
            head_l,
            face_l + washer_t,
            transverse,
            up,
            positive=True,
            label=f"{label}: cap/hex-head envelope Reference Value",
        )

    def build(self) -> DerivedPumpGeometry:
        prefix = self.spec.safe_tag
        self.b.equi(prefix)
        self._build_baseplate()
        self._build_support_frame()
        self._build_casing()
        bearing_start = self._build_bearing_frame()
        self._build_nozzles()
        self._build_coupling(bearing_start)
        self._build_driver()
        self._build_service_details()
        if self.spec.is_mc:
            self._build_mc_auxiliary()
        return self.g

    def _build_baseplate(self) -> None:
        s, b = self.spec, self.b
        prefix = s.safe_tag
        b.sube(f"{prefix}_BASEPLATE")
        xlen, ylen, zlen = s.world_baseplate_dimensions
        b.box(
            xlen,
            ylen,
            zlen,
            self._at(up=zlen / 2.0),
            label=(
                "PROJECT DATA: contractual rectangular baseplate; POS is its "
                "geometric centre and the coordinate is its underside centre"
            ),
        )

        b.sube(f"{prefix}_BASE_FASTENERS")
        margin_l = max(55.0, s.length * 0.055)
        margin_t = max(50.0, s.width * 0.065)
        half_l = s.length / 2.0 - margin_l
        half_t = s.width / 2.0 - margin_t
        positions = [
            (-half_l, -half_t),
            (-half_l, half_t),
            (half_l, -half_t),
            (half_l, half_t),
            (0.0, -half_t),
            (0.0, half_t),
        ]
        if self.detail.anchor_bolt_count == 8:
            positions.extend([(-half_l, 0.0), (half_l, 0.0)])
        anchor_d = _clamp(s.width * 0.020, 14.0, 24.0)
        for index, (lpos, tpos) in enumerate(positions, 1):
            self._vertical_fastener(
                lpos,
                tpos,
                s.baseplate_thickness,
                anchor_d,
                seated=True,
                label=f"Reference Value: baseplate anchor fastener A{index}",
            )

    def _build_support_frame(self) -> None:
        s, g, b = self.spec, self.g, self.b
        prefix = s.safe_tag
        deck_top = s.baseplate_thickness
        b.sube(f"{prefix}_SUPPORT_FRAME")
        for side in (-1.0, 1.0):
            self._box(
                s.length * 0.82,
                g.rail_width,
                g.rail_height,
                -s.length * 0.02,
                side * s.width * 0.24,
                deck_top + g.rail_height / 2.0,
                label=f"Reference Value: welded longitudinal skid rail {side:+.0f}",
            )

        cross_h = g.rail_height * 0.68
        usable = s.length * 0.68
        for index in range(self.detail.crossmember_count):
            fraction = (
                0.0
                if self.detail.crossmember_count == 1
                else index / (self.detail.crossmember_count - 1) - 0.5
            )
            self._box(
                g.rail_width * 0.72,
                s.width * 0.72,
                cross_h,
                fraction * usable,
                0.0,
                deck_top + cross_h / 2.0,
                label=f"Reference Value: skid cross-member {index + 1}",
            )

        foot_h = max(35.0, g.shaft_u - g.casing_diameter / 2.0 - deck_top)
        for lpos in (
            g.casing_centre_l - g.casing_length * 0.27,
            g.casing_centre_l + g.casing_length * 0.24,
        ):
            for side in (-1.0, 1.0):
                self._box(
                    s.length * 0.075,
                    s.width * 0.13,
                    foot_h,
                    lpos,
                    side * s.width * 0.18,
                    deck_top + foot_h / 2.0,
                    label="Reference Value: integrally supported casing foot",
                )

    def _build_casing(self) -> None:
        s, g, b = self.spec, self.g, self.b
        style = self.detail.casing_style
        prefix = s.safe_tag
        b.sube(f"{prefix}_CASING")
        rear_l = g.casing_centre_l - g.casing_length / 2.0
        style_shape = {
            CasingStyle.PROCESS_VOLUTE: (0.12, 0.60, 0.57, 0.60, 1.075),
            CasingStyle.FILTRATE_VOLUTE: (0.14, 0.56, 0.60, 0.62, 1.050),
            CasingStyle.STOCK_VOLUTE: (0.10, 0.64, 0.62, 0.65, 1.100),
            CasingStyle.HIGH_HEAD_VOLUTE: (0.16, 0.58, 0.46, 0.50, 1.065),
            CasingStyle.CLEAN_WATER_VOLUTE: (0.15, 0.55, 0.54, 0.58, 1.040),
            CasingStyle.ABRASIVE_VOLUTE: (0.10, 0.65, 0.60, 0.65, 1.120),
            CasingStyle.CHEMICAL_VOLUTE: (0.14, 0.58, 0.54, 0.58, 1.080),
            CasingStyle.MC_FLUIDIZER: (0.12, 0.58, 0.48, 0.52, 1.100),
        }[style]
        rear_fraction, body_fraction, eye_ratio, nose_ratio, flange_ratio = (
            style_shape
        )
        rear_plate_l = g.casing_length * rear_fraction
        body_l = g.casing_length * body_fraction
        cover_l = g.casing_length - rear_plate_l - body_l

        self._cylinder_local(
            g.casing_diameter * 0.88,
            rear_plate_l,
            rear_l,
            0.0,
            g.shaft_u,
            label=f"Reference Value: {style.value} back-pull-out rear plate",
        )
        self._cylinder_local(
            g.casing_diameter,
            body_l,
            rear_l + rear_plate_l,
            0.0,
            g.shaft_u,
            label=f"Reference Value: {style.value} radially split casing envelope",
        )
        split_l = rear_l + rear_plate_l + body_l
        flange_t = _clamp(g.casing_length * 0.035, 10.0, 20.0)
        self._cylinder_local(
            g.casing_diameter * flange_ratio,
            flange_t,
            split_l - flange_t,
            0.0,
            g.shaft_u,
            label="Reference Value: casing split flange",
        )
        b.cone(
            g.casing_diameter * 0.98,
            g.casing_diameter * eye_ratio,
            cover_l,
            self._at(split_l, 0.0, g.shaft_u),
            axis=s.layout_axis,
            label=f"Reference Value: {style.value} tapered impeller-eye cover",
        )
        nose_t = _clamp(cover_l * 0.16, 10.0, 22.0)
        self._cylinder_local(
            g.casing_diameter * nose_ratio,
            nose_t,
            split_l + cover_l - nose_t,
            0.0,
            g.shaft_u,
            label="Reference Value: suction-cover wear-ring boss",
        )

        rib_t = _clamp(g.casing_diameter * 0.040, 11.0, 22.0)
        rib_l = body_l * 0.68
        rib_start_l = rear_l + rear_plate_l + body_l * 0.16
        rib_radius = g.casing_diameter / 2.0 + rib_t * 0.18
        for index in range(self.detail.casing_rib_count):
            angle = math.pi / 2.0 + (
                2.0 * math.pi * index / self.detail.casing_rib_count
            )
            self._cylinder_local(
                rib_t,
                rib_l,
                rib_start_l,
                rib_radius * math.cos(angle),
                g.shaft_u + rib_radius * math.sin(angle),
                label=(
                    f"Reference Value: {style.value} circumferentially distributed "
                    f"axial casing rib {index + 1}/{self.detail.casing_rib_count}"
                ),
            )

        if style is CasingStyle.HIGH_HEAD_VOLUTE:
            band_t = _clamp(body_l * 0.045, 8.0, 16.0)
            for index, fraction in enumerate((0.26, 0.72), 1):
                self._cylinder_local(
                    g.casing_diameter * 1.035,
                    band_t,
                    rear_l + rear_plate_l + body_l * fraction,
                    0.0,
                    g.shaft_u,
                    label=f"Reference Value: high-head casing reinforcement band {index}",
                )
        elif style is CasingStyle.ABRASIVE_VOLUTE:
            liner_t = _clamp(g.casing_length * 0.045, 12.0, 22.0)
            self._cylinder_local(
                g.casing_diameter * 1.135,
                liner_t,
                split_l - liner_t * 1.30,
                0.0,
                g.shaft_u,
                label="Reference Value: abrasive-service replaceable liner cover",
            )
        elif style is CasingStyle.CHEMICAL_VOLUTE:
            collar_t = _clamp(g.casing_length * 0.035, 10.0, 18.0)
            for index in range(2):
                self._cylinder_local(
                    g.casing_diameter * (0.36 + index * 0.035),
                    collar_t,
                    rear_l - collar_t * (index + 1),
                    0.0,
                    g.shaft_u,
                    label=f"Reference Value: chemical-duty seal collar {index + 1}",
                )
        elif style is CasingStyle.MC_FLUIDIZER:
            sleeve_l = _clamp(cover_l * 0.22, 18.0, 42.0)
            self._cylinder_local(
                g.casing_diameter * 0.44,
                sleeve_l,
                split_l + cover_l - sleeve_l,
                0.0,
                g.shaft_u,
                label="Reference Value: MC fluidizer nose sleeve",
            )

        b.sube(f"{prefix}_CASING_FASTENERS")
        bolt_d = _clamp(g.casing_diameter * 0.045, 14.0, 24.0)
        cover_root_r = g.casing_diameter * 0.98 / 2.0
        flange_outer_r = g.casing_diameter * flange_ratio / 2.0
        circle_r = (cover_root_r + flange_outer_r) / 2.0
        for index in range(self.detail.casing_bolt_count):
            angle = 2.0 * math.pi * index / self.detail.casing_bolt_count
            transverse = circle_r * math.cos(angle)
            up = g.shaft_u + circle_r * math.sin(angle)
            self._axial_flange_fastener(
                split_l,
                transverse,
                up,
                bolt_d,
                label=f"Reference Value: casing split-line bolt C{index + 1}",
            )

    def _build_bearing_frame(self) -> float:
        s, g, b = self.spec, self.g, self.b
        prefix = s.safe_tag
        b.sube(f"{prefix}_BEARING_FRAME")
        motor_front = g.motor_centre_l + g.motor_length / 2.0
        casing_rear = g.casing_centre_l - g.casing_length / 2.0
        clear_gap = max(55.0, casing_rear - motor_front)
        bearing_l = min(clear_gap * 0.52, s.length * 0.12)
        bearing_start = casing_rear - bearing_l
        section_l = bearing_l / self.detail.bearing_sections
        diameters = [
            g.casing_diameter * (0.23 + 0.035 * index)
            for index in range(self.detail.bearing_sections)
        ]
        for index, diameter in enumerate(diameters):
            self._cylinder_local(
                diameter,
                section_l,
                bearing_start + index * section_l,
                0.0,
                g.shaft_u,
                label=f"Reference Value: stepped bearing bracket section {index + 1}",
            )

        seal_l = _clamp(g.casing_length * 0.10, 24.0, 55.0)
        b.cone(
            g.casing_diameter * 0.32,
            g.casing_diameter * 0.22,
            seal_l,
            self._at(casing_rear - seal_l, 0.0, g.shaft_u),
            axis=s.layout_axis,
            label="Reference Value: mechanical-seal/gland housing",
        )

        bearing_d = max(diameters)
        pedestal_top = g.shaft_u - bearing_d / 2.0
        pedestal_h = max(
            24.0,
            pedestal_top - (s.baseplate_thickness + g.rail_height),
        )
        self._box(
            bearing_l * 0.70,
            bearing_d * 0.72,
            pedestal_h,
            bearing_start + bearing_l * 0.55,
            0.0,
            s.baseplate_thickness + g.rail_height + pedestal_h / 2.0,
            label="Reference Value: bearing-frame pedestal",
        )
        cap_d = _clamp(bearing_d * 0.12, 20.0, 36.0)
        b.cyli(
            cap_d,
            _clamp(cap_d * 0.90, 20.0, 34.0),
            self._at(
                bearing_start + bearing_l * 0.56,
                0.0,
                g.shaft_u + bearing_d / 2.0,
            ),
            axis="U",
            label="Reference Value: bearing grease/oil fill cap",
        )
        return bearing_start

    def _build_nozzles(self) -> None:
        s, g, b = self.spec, self.g, self.b
        prefix = s.safe_tag
        casing_centre = self._at(g.casing_centre_l, 0.0, g.shaft_u)

        b.sube(f"{prefix}_SUCTION")
        suction_axis = s.suction_axis.upper()
        suction_vector = _AXIS_VECTOR[suction_axis]
        if suction_axis in (s.layout_axis, _OPPOSITE[s.layout_axis]):
            suction_surface = g.casing_length / 2.0
        else:
            suction_surface = g.casing_diameter / 2.0
        suction_root = (
            casing_centre[0] + suction_vector[0] * suction_surface,
            casing_centre[1] + suction_vector[1] * suction_surface,
            casing_centre[2],
        )
        suction_face = (
            suction_root[0] + suction_vector[0] * g.suction_length,
            suction_root[1] + suction_vector[1] * g.suction_length,
            suction_root[2],
        )
        b.nozzle(
            f"{prefix}_SUCTION_NOZZLE",
            g.suction_dn,
            g.suction_length,
            suction_face,
            axis=suction_axis,
            label=(
                f"Reference Value: suction DN{g.suction_dn}; POS is flange face, "
                f"contractual direction {suction_axis}"
            ),
        )

        b.sube(f"{prefix}_DISCHARGE")
        discharge_axis = s.discharge_axis.upper()
        root_e, root_n, root_u = self._at(
            g.casing_centre_l, 0.0, g.shaft_u + g.casing_diameter / 2.0
        )
        if discharge_axis == "U":
            boss_h = _clamp(g.discharge_dn * 0.28, 24.0, 52.0)
            b.cyli(
                g.discharge_dn * 1.35,
                boss_h,
                (root_e, root_n, root_u - boss_h * 0.35),
                axis="U",
                label="Reference Value: integrally cast discharge-neck boss",
            )
            discharge_face = (root_e, root_n, root_u + g.discharge_length)
        elif discharge_axis == "D":
            discharge_face = (root_e, root_n, root_u - g.discharge_length)
        else:
            de, dn = _AXIS_VECTOR[discharge_axis]
            surface = (
                g.casing_length / 2.0
                if discharge_axis in (s.layout_axis, _OPPOSITE[s.layout_axis])
                else g.casing_diameter / 2.0
            )
            root_e = s.position[0] + self._forward[0] * g.casing_centre_l + de * surface
            root_n = s.position[1] + self._forward[1] * g.casing_centre_l + dn * surface
            discharge_face = (
                root_e + de * g.discharge_length,
                root_n + dn * g.discharge_length,
                s.position[2] + g.shaft_u,
            )
        b.nozzle(
            f"{prefix}_DISCHARGE_NOZZLE",
            g.discharge_dn,
            g.discharge_length,
            discharge_face,
            axis=discharge_axis,
            label=(
                f"Reference Value: discharge DN{g.discharge_dn}; POS is flange "
                f"face, contractual direction {discharge_axis}"
            ),
        )

    def _build_coupling(self, bearing_start: float) -> None:
        s, g, b = self.spec, self.g, self.b
        p = self.detail
        prefix = s.safe_tag
        b.sube(f"{prefix}_COUPLING")
        motor_front = g.motor_centre_l + g.motor_length / 2.0
        span = bearing_start - motor_front
        if span <= 0.0:
            raise ValueError(
                f"{s.tag}: motor front overlaps the bearing frame by "
                f"{-span:.1f} mm"
            )
        hub_l = min(span * 0.25, 45.0)
        shaft_d = _clamp(g.motor_height * 0.075, 18.0, 36.0)
        hub_d = shaft_d * 2.15
        element_d = hub_d * 1.18
        self._cylinder_local(
            shaft_d,
            span,
            motor_front,
            0.0,
            g.shaft_u,
            label="Reference Value: exposed common shaft between driver and pump",
        )
        self._cylinder_local(
            hub_d,
            hub_l,
            motor_front,
            0.0,
            g.shaft_u,
            label="Reference Value: motor-side flexible-coupling hub",
        )
        self._cylinder_local(
            hub_d,
            hub_l,
            bearing_start - hub_l,
            0.0,
            g.shaft_u,
            label="Reference Value: pump-side flexible-coupling hub",
        )
        element_l = max(12.0, min(28.0, span - 2.0 * hub_l))
        self._cylinder_local(
            element_d,
            element_l,
            motor_front + (span - element_l) / 2.0,
            0.0,
            g.shaft_u,
            label="Reference Value: elastomeric flexible-coupling element",
        )

        guard_d = _clamp(g.motor_height * 0.38, 110.0, 220.0)
        band_t = _clamp(span * 0.045, 5.0, 12.0)
        if p.guard_style is CouplingGuardStyle.ROUND:
            self._cylinder_local(
                guard_d,
                span,
                motor_front,
                0.0,
                g.shaft_u,
                label="Reference Value: full rounded coupling guard",
            )
        elif p.guard_style is CouplingGuardStyle.TAPERED:
            b.cone(
                guard_d * 0.86,
                guard_d,
                span,
                self._at(motor_front, 0.0, g.shaft_u),
                axis=s.layout_axis,
                label="Reference Value: tapered coupling guard",
            )
        elif p.guard_style is CouplingGuardStyle.BOXED:
            self._box(
                span,
                guard_d * 0.92,
                guard_d * 0.78,
                motor_front + span / 2.0,
                0.0,
                g.shaft_u,
                label="Reference Value: fabricated rectangular coupling guard",
            )
            self._box(
                span * 0.82,
                _clamp(guard_d * 0.055, 8.0, 15.0),
                _clamp(guard_d * 0.055, 8.0, 15.0),
                motor_front + span / 2.0,
                0.0,
                g.shaft_u + guard_d * 0.42,
                label="Reference Value: boxed guard top reinforcing seam",
            )
        else:
            cage_rod_d = _clamp(guard_d * 0.075, 10.0, 18.0)
            cage_radius = guard_d * 0.40
            for index in range(8):
                angle = 2.0 * math.pi * index / 8.0
                self._cylinder_local(
                    cage_rod_d,
                    span,
                    motor_front,
                    cage_radius * math.cos(angle),
                    g.shaft_u + cage_radius * math.sin(angle),
                    label=f"Reference Value: ventilated guard cage rail {index + 1}",
                )
            for end_index, lpos in enumerate(
                (motor_front + band_t / 2.0, bearing_start - band_t / 2.0),
                1,
            ):
                self._box(
                    band_t,
                    guard_d * 0.82,
                    cage_rod_d,
                    lpos,
                    0.0,
                    g.shaft_u,
                    label=(
                        f"Reference Value: ventilated guard end horizontal brace "
                        f"{end_index}"
                    ),
                )
                self._box(
                    band_t,
                    cage_rod_d,
                    guard_d * 0.82,
                    lpos,
                    0.0,
                    g.shaft_u,
                    label=(
                        f"Reference Value: ventilated guard end vertical brace "
                        f"{end_index}"
                    ),
                )

        if p.guard_style in (
            CouplingGuardStyle.ROUND,
            CouplingGuardStyle.TAPERED,
        ):
            for index, lpos in enumerate((motor_front, bearing_start - band_t), 1):
                self._cylinder_local(
                    guard_d * 1.045,
                    band_t,
                    lpos,
                    0.0,
                    g.shaft_u,
                    label=f"Reference Value: coupling-guard clamp band {index}",
                )
        guard_foot_h = max(
            18.0,
            g.shaft_u
            - guard_d / 2.0
            - (s.baseplate_thickness + g.rail_height),
        )
        for lpos in (motor_front + span * 0.18, motor_front + span * 0.82):
            self._box(
                max(24.0, span * 0.12),
                guard_d * 0.62,
                guard_foot_h,
                lpos,
                0.0,
                s.baseplate_thickness + g.rail_height + guard_foot_h / 2.0,
                label="Reference Value: coupling-guard support foot",
            )

    def _build_driver(self) -> None:
        s, g, b = self.spec, self.g, self.b
        prefix = s.safe_tag
        p = self.detail
        b.sube(f"{prefix}_DRIVER")
        motor_back = g.motor_centre_l - g.motor_length / 2.0
        motor_front = g.motor_centre_l + g.motor_length / 2.0
        body_factor = _MOTOR_BODY_FACTOR[p.motor_style]
        body_d = g.motor_height * body_factor
        fan_fraction = {
            MotorStyle.IEC_STANDARD: 0.15,
            MotorStyle.HEAVY_DUTY: 0.14,
            MotorStyle.HIGH_SPEED: 0.18,
            MotorStyle.CHEMICAL_DUTY: 0.16,
            MotorStyle.MC_MAIN_DRIVE: 0.15,
        }[p.motor_style]
        bell_fraction = {
            MotorStyle.IEC_STANDARD: 0.11,
            MotorStyle.HEAVY_DUTY: 0.12,
            MotorStyle.HIGH_SPEED: 0.09,
            MotorStyle.CHEMICAL_DUTY: 0.13,
            MotorStyle.MC_MAIN_DRIVE: 0.12,
        }[p.motor_style]
        fan_l = g.motor_length * fan_fraction
        front_bell_l = g.motor_length * bell_fraction
        body_start = motor_back + fan_l * 0.72
        body_l = motor_front - front_bell_l - body_start

        self._cylinder_local(
            body_d
            * (0.98 if p.motor_style is MotorStyle.HEAVY_DUTY else 0.92),
            fan_l,
            motor_back,
            0.0,
            g.shaft_u,
            label=(
                f"Reference Value: {p.motor_style.value} TEFC motor fan cowl"
            ),
        )
        b.cone(
            body_d * 0.90,
            body_d,
            fan_l * 0.45,
            self._at(motor_back + fan_l * 0.55, 0.0, g.shaft_u),
            axis=s.layout_axis,
            label="Reference Value: motor non-drive end bell",
        )
        self._cylinder_local(
            body_d,
            body_l,
            body_start,
            0.0,
            g.shaft_u,
            label=(
                f"Reference Value: finned IEC TEFC motor stator barrel; "
                f"tag profile {p.appearance_code}"
            ),
        )
        b.cone(
            body_d,
            body_d * 0.72,
            front_bell_l,
            self._at(motor_front - front_bell_l, 0.0, g.shaft_u),
            axis=s.layout_axis,
            label="Reference Value: motor drive-end bell",
        )
        cap_l = _clamp(front_bell_l * 0.22, 8.0, 18.0)
        self._cylinder_local(
            body_d * 0.38,
            cap_l,
            motor_front - cap_l,
            0.0,
            g.shaft_u,
            label="Reference Value: motor drive-end bearing cap",
        )

        # Fan grille: an open PML1 lattice rather than a single solid end disc.
        # BOX has no arbitrary-angle ORI in the proven subset, so the circular
        # grille is represented by bounded horizontal/vertical bars plus a
        # filled central hub.  This keeps the air openings visually readable.
        grille_t = _clamp(body_d * 0.025, 6.0, 12.0)
        self._cylinder_local(
            body_d * 0.18,
            grille_t * 1.35,
            motor_back + grille_t * 1.35,
            0.0,
            g.shaft_u,
            positive=False,
            label="Reference Value: motor fan grille central hub",
        )
        grille_radius = body_d * 0.43
        bar_t = _clamp(body_d * 0.018, 5.0, 9.0)
        offsets = (-0.62, -0.31, 0.0, 0.31, 0.62)
        for index, fraction in enumerate(offsets, 1):
            offset = grille_radius * fraction
            clear_span = 2.0 * math.sqrt(
                max(0.0, grille_radius * grille_radius - offset * offset)
            )
            self._box(
                grille_t,
                clear_span,
                bar_t,
                motor_back + grille_t / 2.0,
                0.0,
                g.shaft_u + offset,
                label=f"Reference Value: open fan-grille horizontal bar {index}",
            )
            self._box(
                grille_t,
                bar_t,
                clear_span,
                motor_back + grille_t / 2.0,
                offset,
                g.shaft_u,
                label=f"Reference Value: open fan-grille vertical bar {index}",
            )

        rail_top = s.baseplate_thickness + g.rail_height
        foot_l = g.motor_length * 0.14
        foot_w = g.motor_width * 0.24
        foot_pad_h = _clamp(g.motor_height * 0.055, 16.0, 28.0)
        foot_web_w = foot_w * 0.42
        foot_positions = (
            motor_back + g.motor_length * 0.27,
            motor_back + g.motor_length * 0.73,
        )
        for lpos in foot_positions:
            for side in (-1.0, 1.0):
                tpos = side * s.width * 0.22
                web_tpos = tpos - side * foot_w * 0.22
                # A low pad carries the hold-down bolt.  A narrower inward web
                # rises to the actual round-barrel surface; this avoids both a
                # detached foot and an implausible full-width block reaching
                # high up the side of the motor.
                self._box(
                    foot_l,
                    foot_w,
                    foot_pad_h,
                    lpos,
                    tpos,
                    rail_top + foot_pad_h / 2.0,
                    label="Reference Value: cast motor foot mounting pad",
                )
                radial_offset = min(
                    max(0.0, abs(web_tpos) - foot_web_w / 2.0),
                    body_d * 0.49,
                )
                barrel_contact_u = g.shaft_u - math.sqrt(
                    max(0.0, (body_d / 2.0) ** 2 - radial_offset**2)
                )
                web_h = max(
                    18.0,
                    barrel_contact_u
                    - (rail_top + foot_pad_h)
                    + _clamp(body_d * 0.0125, 3.0, 8.0),
                )
                self._box(
                    foot_l * 0.78,
                    foot_web_w,
                    web_h,
                    lpos,
                    web_tpos,
                    rail_top + foot_pad_h + web_h / 2.0,
                    label="Reference Value: barrel-connected motor foot web",
                )

        # Real TEFC motor ribs run axially and surround the complete stator
        # circumference. Small overlapping axial CYLIs provide a verified-PML1
        # additive approximation without inventing an unsupported annulus.
        fin_d = _clamp(body_d * 0.055, 12.0, 26.0)
        fin_radius = body_d / 2.0 + fin_d * 0.22
        fin_start = body_start + body_l * 0.06
        fin_length = body_l * 0.88
        for index in range(p.motor_fin_count):
            angle = math.pi / 2.0 + 2.0 * math.pi * index / p.motor_fin_count
            self._cylinder_local(
                fin_d,
                fin_length,
                fin_start,
                fin_radius * math.cos(angle),
                g.shaft_u + fin_radius * math.sin(angle),
                label=(
                    f"Reference Value: 360-degree motor cooling rib "
                    f"{index + 1}/{p.motor_fin_count}"
                ),
            )

        if p.motor_style in (MotorStyle.HEAVY_DUTY, MotorStyle.MC_MAIN_DRIVE):
            band_t = _clamp(body_l * 0.035, 10.0, 18.0)
            band_count = 3 if p.motor_style is MotorStyle.MC_MAIN_DRIVE else 2
            for index in range(band_count):
                fraction = (index + 1) / (band_count + 1)
                self._cylinder_local(
                    body_d * 1.055,
                    band_t,
                    body_start + body_l * fraction - band_t / 2.0,
                    0.0,
                    g.shaft_u,
                    label=(
                        f"Reference Value: {p.motor_style.value} stator "
                        f"reinforcing band {index + 1}/{band_count}"
                    ),
                )
        elif p.motor_style is MotorStyle.HIGH_SPEED:
            collar_t = _clamp(body_l * 0.028, 8.0, 14.0)
            for index, fraction in enumerate((0.10, 0.86), 1):
                self._cylinder_local(
                    body_d * 1.035,
                    collar_t,
                    body_start + body_l * fraction,
                    0.0,
                    g.shaft_u,
                    label=(
                        "Reference Value: compact high-speed motor end-frame "
                        f"collar {index}"
                    ),
                )
        elif p.motor_style is MotorStyle.CHEMICAL_DUTY:
            seal_t = _clamp(front_bell_l * 0.17, 8.0, 14.0)
            self._cylinder_local(
                body_d * 0.76,
                seal_t,
                motor_front - front_bell_l - seal_t,
                0.0,
                g.shaft_u,
                label="Reference Value: chemical-duty sealed drive-end collar",
            )

        terminal_factors = {
            MotorStyle.IEC_STANDARD: (0.24, 0.42, 0.20),
            MotorStyle.HEAVY_DUTY: (0.28, 0.46, 0.23),
            MotorStyle.HIGH_SPEED: (0.20, 0.35, 0.18),
            MotorStyle.CHEMICAL_DUTY: (0.25, 0.42, 0.24),
            MotorStyle.MC_MAIN_DRIVE: (0.27, 0.45, 0.22),
        }[p.motor_style]
        term_l = g.motor_length * terminal_factors[0]
        term_w = g.motor_width * terminal_factors[1]
        term_h = g.motor_height * terminal_factors[2]
        term_centre_l = g.motor_centre_l - g.motor_length * 0.04
        term_centre_t = p.terminal_mount_side * g.motor_width * 0.09
        term_bottom = g.shaft_u + body_d / 2.0 + fin_d * 0.72
        self._box(
            term_l,
            term_w,
            term_h,
            term_centre_l,
            term_centre_t,
            term_bottom + term_h / 2.0,
            label="Reference Value: cast motor terminal box",
        )
        lid_h = _clamp(term_h * 0.12, 6.0, 12.0)
        self._box(
            term_l * 1.04,
            term_w * 1.04,
            lid_h,
            term_centre_l,
            term_centre_t,
            term_bottom + term_h + lid_h / 2.0,
            label="Reference Value: terminal-box gasketed lid",
        )
        terminal_bolt_d = _clamp(term_w * 0.035, 6.0, 10.0)
        for dl in (-term_l * 0.38, term_l * 0.38):
            for dt in (-term_w * 0.36, term_w * 0.36):
                self.b.cyli(
                    terminal_bolt_d * 1.65,
                    lid_h * 0.55,
                    self._at(
                        term_centre_l + dl,
                        term_centre_t + dt,
                        term_bottom + term_h + lid_h,
                    ),
                    axis="U",
                    label="Reference Value: terminal-box lid screw head",
                )

        gland_d = _clamp(term_h * 0.22, 12.0, 24.0)
        gland_side = p.cable_gland_side
        self._cylinder_cross(
            gland_d * 1.35,
            gland_d * 0.55,
            term_centre_l,
            term_centre_t + gland_side * term_w / 2.0,
            term_bottom + term_h * 0.45,
            side=gland_side,
            label="Reference Value: motor terminal cable gland body",
        )
        self._cylinder_cross(
            gland_d,
            gland_d * 0.65,
            term_centre_l,
            term_centre_t + gland_side * (term_w / 2.0 + gland_d * 0.55),
            term_bottom + term_h * 0.45,
            side=gland_side,
            label="Reference Value: motor terminal cable gland compression nut",
        )

        # Lifting lug and nameplate are visible construction, without pretending
        # to encode an unsupported negative hole or vendor text.
        lug_l = term_l * 0.32
        lug_t = _clamp(g.motor_width * 0.035, 12.0, 22.0)
        lug_h = _clamp(g.motor_height * 0.14, 32.0, 58.0)
        lug_centre_l = g.motor_centre_l + g.motor_length * 0.18
        lug_base = g.shaft_u + body_d / 2.0
        self._box(
            lug_l,
            lug_t,
            lug_h,
            lug_centre_l,
            0.0,
            lug_base + lug_h / 2.0,
            label="Reference Value: motor lifting lug plate",
        )
        self._cylinder_cross(
            lug_t * 1.35,
            lug_t * 1.70,
            lug_centre_l,
            -lug_t * 0.85,
            lug_base + lug_h * 0.78,
            side=1,
            label="Reference Value: filled lifting-lug pin envelope",
        )
        self._box(
            g.motor_length * 0.16,
            _clamp(g.motor_width * 0.018, 5.0, 9.0),
            g.motor_height * 0.12,
            g.motor_centre_l + g.motor_length * 0.06,
            -p.cable_gland_side * (body_d / 2.0 + 2.0),
            g.shaft_u + body_d * 0.06,
            label="Reference Value: motor rating/nameplate",
        )

        b.sube(f"{prefix}_DRIVER_FASTENERS")
        hold_d = _clamp(g.motor_width * 0.035, 12.0, 20.0)
        for lpos in foot_positions:
            for side in (-1.0, 1.0):
                self._vertical_fastener(
                    lpos,
                    side * s.width * 0.24,
                    rail_top + foot_pad_h,
                    hold_d,
                    label="Reference Value: motor hold-down fastener",
                )

    def _build_service_details(self) -> None:
        s, g, b = self.spec, self.g, self.b
        prefix = s.safe_tag
        duty = s.duty
        b.sube(f"{prefix}_SERVICE_DETAILS")
        side = s.auxiliary_side
        casing_side_t = side * g.casing_diameter / 2.0

        if duty in (PumpDuty.SCREEN_FEED, PumpDuty.WASHER_FEED):
            cover_d = g.casing_diameter * (0.30 if duty is PumpDuty.SCREEN_FEED else 0.25)
            cover_t = _clamp(cover_d * 0.08, 12.0, 22.0)
            self._cylinder_cross(
                cover_d,
                cover_t,
                g.casing_centre_l,
                casing_side_t,
                g.shaft_u,
                side=side,
                label="Reference Value: stock-duty casing clean-out cover",
            )
            bolt_d = _clamp(cover_d * 0.055, 8.0, 14.0)
            for du, dl in (
                (-cover_d * 0.26, 0.0),
                (cover_d * 0.26, 0.0),
                (0.0, -cover_d * 0.26),
                (0.0, cover_d * 0.26),
            ):
                self._cylinder_cross(
                    bolt_d * 1.7,
                    cover_t * 0.65,
                    g.casing_centre_l + dl,
                    casing_side_t + side * cover_t,
                    g.shaft_u + du,
                    side=side,
                    label="Reference Value: clean-out cover bolt head",
                )
            if s.tag == "205-PU-027":
                branch_d = _clamp(g.suction_dn * 0.72, 65.0, 125.0)
                branch_l = _clamp(s.width * 0.14, 95.0, 150.0)
                branch_start_t = side * g.casing_diameter * 0.48
                self._cylinder_cross(
                    branch_d,
                    branch_l,
                    g.casing_centre_l - g.casing_length * 0.08,
                    branch_start_t,
                    g.shaft_u + g.casing_diameter * 0.08,
                    side=side,
                    label=(
                        "TOP_VIEW Reference Value: 205-PU-027 stock-casing "
                        "lateral branch"
                    ),
                )
                self._cylinder_cross(
                    branch_d * 1.28,
                    _clamp(branch_l * 0.12, 14.0, 22.0),
                    g.casing_centre_l - g.casing_length * 0.08,
                    branch_start_t + side * branch_l,
                    g.shaft_u + g.casing_diameter * 0.08,
                    side=side,
                    label=(
                        "TOP_VIEW Reference Value: 205-PU-027 lateral-branch "
                        "end collar"
                    ),
                )
        elif duty is PumpDuty.FILTRATE:
            inspection_d = g.casing_diameter * 0.18
            self._cylinder_cross(
                inspection_d,
                _clamp(inspection_d * 0.10, 10.0, 18.0),
                g.casing_centre_l,
                casing_side_t,
                g.shaft_u - g.casing_diameter * 0.12,
                side=side,
                label="Reference Value: filtrate-pump side inspection boss",
            )
            b.cyli(
                _clamp(g.discharge_dn * 0.22, 18.0, 30.0),
                _clamp(g.discharge_dn * 0.20, 16.0, 28.0),
                self._at(
                    g.casing_centre_l,
                    side * g.casing_diameter * 0.20,
                    g.shaft_u + g.casing_diameter * 0.38,
                ),
                axis="U",
                label="Reference Value: filtrate casing vent plug",
            )
        elif duty is PumpDuty.DILUTION:
            boss_d = _clamp(g.discharge_dn * 0.26, 22.0, 38.0)
            b.cyli(
                boss_d,
                boss_d * 0.80,
                self._at(
                    g.casing_centre_l - g.casing_length * 0.08,
                    side * g.casing_diameter * 0.18,
                    g.shaft_u + g.casing_diameter * 0.42,
                ),
                axis="U",
                label="Reference Value: dilution-pump vent/flush boss",
            )
        elif duty in (PumpDuty.BOOSTER, PumpDuty.WIRE_WASH):
            boss_d = _clamp(g.discharge_dn * 0.20, 16.0, 28.0)
            b.cyli(
                boss_d,
                boss_d * 0.90,
                self._at(
                    g.casing_centre_l,
                    0.0,
                    g.shaft_u + g.casing_diameter * 0.46,
                ),
                axis="U",
                label="Reference Value: compact pressure tapping boss",
            )
            if duty is PumpDuty.BOOSTER:
                for index in (-1.0, 1.0):
                    self._box(
                        g.casing_length * 0.32,
                        _clamp(g.casing_diameter * 0.035, 9.0, 15.0),
                        _clamp(g.casing_diameter * 0.05, 12.0, 22.0),
                        g.casing_centre_l - g.casing_length * 0.28,
                        index * g.casing_diameter * 0.20,
                        g.shaft_u + g.casing_diameter * 0.30,
                        label="Reference Value: booster bearing cooling rib",
                    )
        elif duty is PumpDuty.SCRUBBER_CIRCULATION:
            manifold_d = _clamp(g.discharge_dn * 0.22, 18.0, 30.0)
            manifold_l = g.casing_length * 0.36
            self._cylinder_local(
                manifold_d,
                manifold_l,
                g.casing_centre_l - g.casing_length * 0.42,
                side * g.casing_diameter * 0.30,
                g.shaft_u + g.casing_diameter * 0.20,
                label="Reference Value: scrubber-pump seal-flush manifold",
            )
            self._box(
                g.casing_length * 0.34,
                g.casing_diameter * 0.58,
                _clamp(g.casing_diameter * 0.045, 12.0, 22.0),
                g.casing_centre_l - g.casing_length * 0.38,
                0.0,
                g.shaft_u - g.casing_diameter * 0.42,
                label="Reference Value: scrubber-pump seal splash shield",
            )

    def _build_mc_auxiliary(self) -> None:
        """Build the top-view-specific MC separation and auxiliary-drive package."""
        s, g, b = self.spec, self.g, self.b
        prefix = s.safe_tag
        variant = self.detail.mc_variant
        side = float(s.auxiliary_side)
        deck_top = s.baseplate_thickness
        rail_top = deck_top + g.rail_height
        b.sube(f"{prefix}_MC_AUXILIARY")

        separator_scale = 1.14 if variant == "EOP_LARGE_SEPARATOR" else 1.0
        separator_d = _clamp(
            s.width * 0.16 * separator_scale, 120.0, 230.0
        )
        separator_h = _clamp(
            s.width * 0.30 * separator_scale, 200.0, 390.0
        )
        separator_l_fraction = {
            "EOP_LARGE_SEPARATOR": 0.24,
            "D1_DUAL_AUX": 0.15,
            "D0_SIDE_SUCTION": 0.04,
            "COMPACT_NO_VIEW": 0.02,
            "REACTOR_NO_VIEW": 0.04,
        }.get(variant, 0.04)
        separator_l = s.length * separator_l_fraction
        separator_t = side * s.width * 0.31
        b.cyli(
            separator_d,
            separator_h,
            self._at(separator_l, separator_t, rail_top),
            axis="U",
            label=(
                "Reference Value: MC integrated air separator; structure based "
                "on project top view and official MC-pump separation descriptions"
            ),
        )
        b.cone(
            separator_d,
            separator_d * 0.62,
            separator_h * 0.16,
            self._at(separator_l, separator_t, rail_top + separator_h),
            axis="U",
            label="Reference Value: MC separator top reducer",
        )
        b.cyli(
            _clamp(separator_d * 0.22, 30.0, 48.0),
            _clamp(separator_h * 0.15, 34.0, 58.0),
            self._at(
                separator_l,
                separator_t,
                rail_top + separator_h + separator_h * 0.16,
            ),
            axis="U",
            label="Reference Value: MC separator degassing outlet",
        )

        line_length = max(35.0, abs(separator_t) - g.casing_diameter * 0.28)
        line_start_t = side * g.casing_diameter * 0.28
        self._cylinder_cross(
            _clamp(s.width * 0.045, 35.0, 65.0),
            line_length,
            g.casing_centre_l,
            line_start_t,
            g.shaft_u + g.casing_diameter * 0.22,
            side=int(side),
            label="Reference Value: MC degassing connection line",
        )

        # Compact separator drive.  For missing-view pumps this is an official
        # MC-family Reference Value, not a claimed tag-specific observation.
        aux_l = s.length * (0.22 if s.length >= 1500.0 else 0.18)
        aux_d = _clamp(s.width * 0.16, 105.0, 175.0)
        aux_centre_l = -s.length * (
            0.16 if variant == "EOP_LARGE_SEPARATOR" else 0.20
        )
        aux_centre_t = side * s.width * 0.31
        aux_back = aux_centre_l - aux_l / 2.0
        aux_u = rail_top + aux_d * 0.62
        aux_body_start = aux_back + aux_l * 0.16
        aux_body_l = aux_l * 0.72
        self._cylinder_local(
            aux_d,
            aux_body_l,
            aux_body_start,
            aux_centre_t,
            aux_u,
            label="Reference Value: MC separator auxiliary motor barrel",
        )
        self._cylinder_local(
            aux_d * 0.90,
            aux_l * 0.18,
            aux_back,
            aux_centre_t,
            aux_u,
            label="Reference Value: MC auxiliary motor fan cover",
        )
        b.cone(
            aux_d,
            aux_d * 0.66,
            aux_l * 0.12,
            self._at(
                aux_centre_l + aux_l * 0.34,
                aux_centre_t,
                aux_u,
            ),
            axis=s.layout_axis,
            label="Reference Value: MC auxiliary motor drive-end bell",
        )
        aux_fin_count = 10
        aux_fin_d = _clamp(aux_d * 0.060, 7.0, 12.0)
        aux_fin_radius = aux_d / 2.0 + aux_fin_d * 0.22
        for index in range(aux_fin_count):
            angle = math.pi / 2.0 + 2.0 * math.pi * index / aux_fin_count
            self._cylinder_local(
                aux_fin_d,
                aux_body_l * 0.86,
                aux_body_start + aux_body_l * 0.07,
                aux_centre_t + aux_fin_radius * math.cos(angle),
                aux_u + aux_fin_radius * math.sin(angle),
                label=(
                    "Reference Value: 360-degree MC auxiliary-motor cooling "
                    f"rib {index + 1}/{aux_fin_count}"
                ),
            )
        aux_term_l = aux_l * 0.20
        aux_term_w = aux_d * 0.40
        aux_term_h = aux_d * 0.17
        self._box(
            aux_term_l,
            aux_term_w,
            aux_term_h,
            aux_centre_l,
            aux_centre_t,
            aux_u + aux_d / 2.0 + aux_fin_d + aux_term_h / 2.0,
            label="Reference Value: MC auxiliary-motor terminal box",
        )
        for lpos in (aux_centre_l - aux_l * 0.22, aux_centre_l + aux_l * 0.22):
            self._box(
                aux_l * 0.18,
                aux_d * 0.72,
                max(18.0, aux_u - aux_d / 2.0 - rail_top),
                lpos,
                aux_centre_t,
                rail_top + max(18.0, aux_u - aux_d / 2.0 - rail_top) / 2.0,
                label="Reference Value: MC auxiliary motor foot",
            )

        # The supplied EOP and D1 plans show materially different outboard
        # packages from the compact D0 sidecar arrangement.
        if variant in ("EOP_LARGE_SEPARATOR", "D1_DUAL_AUX"):
            enclosure_l = s.length * 0.18
            enclosure_w = s.width * 0.23
            enclosure_h = _clamp(g.motor_height * 0.34, 105.0, 170.0)
            enclosure_centre_l = (
                s.length * 0.31
                if variant == "EOP_LARGE_SEPARATOR"
                else s.length * 0.24
            )
            enclosure_centre_t = -side * s.width * 0.31
            self._box(
                enclosure_l,
                enclosure_w,
                enclosure_h,
                enclosure_centre_l,
                enclosure_centre_t,
                rail_top + enclosure_h / 2.0,
                label=(
                    "Reference Value: enlarged MC separation/control side package "
                    "matched to the tag-specific top view"
                ),
            )
            lid_h = _clamp(enclosure_h * 0.08, 8.0, 14.0)
            self._box(
                enclosure_l * 1.03,
                enclosure_w * 1.03,
                lid_h,
                enclosure_centre_l,
                enclosure_centre_t,
                rail_top + enclosure_h + lid_h / 2.0,
                label="Reference Value: MC side-package access lid",
            )
            bolt_d = _clamp(enclosure_w * 0.035, 7.0, 11.0)
            for dl in (-enclosure_l * 0.38, enclosure_l * 0.38):
                for dt in (-enclosure_w * 0.36, enclosure_w * 0.36):
                    b.cyli(
                        bolt_d * 1.7,
                        lid_h * 0.65,
                        self._at(
                            enclosure_centre_l + dl,
                            enclosure_centre_t + dt,
                            rail_top + enclosure_h + lid_h,
                        ),
                        axis="U",
                        label="Reference Value: MC side-package lid fastener",
                    )

        if variant == "D1_DUAL_AUX":
            # 205-PU-054's plan has an additional orthogonal local drive.
            # Keep it inside the skid and visibly distinct from the parallel
            # compact sidecar used on 205-PU-018/038.
            cross_l = s.width * 0.27
            cross_d = _clamp(s.width * 0.13, 105.0, 155.0)
            cross_centre_l = s.length * 0.18
            cross_centre_t = -side * s.width * 0.23
            cross_u = rail_top + cross_d * 0.61
            self._cylinder_cross(
                cross_d,
                cross_l,
                cross_centre_l,
                cross_centre_t,
                cross_u,
                side=-int(side),
                label=(
                    "Reference Value: D1 MC orthogonal auxiliary-drive barrel "
                    "matched to 205-PU-054 top-view arrangement"
                ),
            )
            self._box(
                cross_d * 0.52,
                cross_l * 0.24,
                max(18.0, cross_u - cross_d / 2.0 - rail_top),
                cross_centre_l,
                cross_centre_t,
                rail_top
                + max(18.0, cross_u - cross_d / 2.0 - rail_top) / 2.0,
                label="Reference Value: D1 orthogonal auxiliary-drive pedestal",
            )


def _world_plan_half_extents(primitive: dict) -> Tuple[float, float]:
    kind = primitive["kind"]
    if kind == "BOX":
        return primitive.get("xlen", 0.0) / 2.0, primitive.get("ylen", 0.0) / 2.0
    diameter = max(
        primitive.get("diam", 0.0),
        primitive.get("dbot", 0.0),
        primitive.get("dtop", 0.0),
    )
    axis = primitive.get("axis", "U")
    if axis in ("E", "W"):
        return primitive.get("heig", 0.0) / 2.0, diameter / 2.0
    if axis in ("N", "S"):
        return diameter / 2.0, primitive.get("heig", 0.0) / 2.0
    return diameter / 2.0, diameter / 2.0


def _nozzle_direction(script: str, nozzle_name: str) -> str:
    in_nozzle = False
    for raw in script.splitlines():
        line = raw.strip()
        if line.startswith("NEW NOZZLE /"):
            in_nozzle = line == f"NEW NOZZLE /{nozzle_name}"
            continue
        if in_nozzle and line.startswith("ORI P1 IS "):
            return line.rsplit(" ", 1)[-1].upper()
        if in_nozzle and line.startswith("NEW "):
            break
    return ""


def _labeled_cylinders(script: str, label_fragment: str) -> List[dict]:
    """Parse CYLIs immediately following a selected generated comment label."""
    cylinders: List[dict] = []
    lines = script.splitlines()
    for index, raw in enumerate(lines):
        if not raw.startswith("-- ") or label_fragment not in raw:
            continue
        block = "\n".join(lines[index + 1 : index + 8])
        match = re.search(
            r"(?m)^NEW CYLI\n"
            r"DIAM (-?[\d.]+)\n"
            r"HEIG (-?[\d.]+)\n"
            r"ORI Z IS ([ENSWUD]) AND Y IS [ENSWUD]\n"
            r"POS E (-?[\d.]+) N (-?[\d.]+) U (-?[\d.]+)$",
            block,
        )
        if match:
            diameter, length, axis, east, north, up = match.groups()
            cylinders.append(
                {
                    "diam": float(diameter),
                    "heig": float(length),
                    "axis": axis,
                    "east": float(east),
                    "north": float(north),
                    "up": float(up),
                }
            )
    return cylinders


def _labeled_boxes(script: str, label_fragment: str) -> List[dict]:
    """Parse BOXes immediately following a selected generated comment label."""
    boxes: List[dict] = []
    lines = script.splitlines()
    for index, raw in enumerate(lines):
        if not raw.startswith("-- ") or label_fragment not in raw:
            continue
        block = "\n".join(lines[index + 1 : index + 8])
        match = re.search(
            r"(?m)^NEW BOX\n"
            r"XLEN (-?[\d.]+)\n"
            r"YLEN (-?[\d.]+)\n"
            r"ZLEN (-?[\d.]+)\n"
            r"POS E (-?[\d.]+) N (-?[\d.]+) U (-?[\d.]+)$",
            block,
        )
        if match:
            xlen, ylen, zlen, east, north, up = match.groups()
            boxes.append(
                {
                    "xlen": float(xlen),
                    "ylen": float(ylen),
                    "zlen": float(zlen),
                    "east": float(east),
                    "north": float(north),
                    "up": float(up),
                }
            )
    return boxes


def verify_pump(spec: PumpSpec, script: str) -> List[str]:
    """
    Numerically verify immutable data, footprint, hierarchy and orientations.

    The baseplate check parses the BOX and computes its underside from E3D's
    centre datum. It never passes merely because a matching POS string exists.
    """
    problems = list(validate_pml(script))
    safe = spec.safe_tag
    equi_lines = [
        line.strip()
        for line in script.splitlines()
        if line.strip().startswith("NEW EQUI /")
    ]
    if equi_lines != [f"NEW EQUI /{safe}"]:
        problems.append(
            f"{spec.tag}: expected exactly one EQUI /{safe}, got {equi_lines}"
        )

    required_subes = {
        f"{safe}_BASEPLATE",
        f"{safe}_BASE_FASTENERS",
        f"{safe}_SUPPORT_FRAME",
        f"{safe}_CASING",
        f"{safe}_CASING_FASTENERS",
        f"{safe}_BEARING_FRAME",
        f"{safe}_SUCTION",
        f"{safe}_DISCHARGE",
        f"{safe}_COUPLING",
        f"{safe}_DRIVER",
        f"{safe}_DRIVER_FASTENERS",
        f"{safe}_SERVICE_DETAILS",
    }
    if spec.is_mc:
        required_subes.add(f"{safe}_MC_AUXILIARY")
    actual_subes = {
        line.strip().split("/", 1)[1]
        for line in script.splitlines()
        if line.strip().startswith("NEW SUBE /")
    }
    missing_subes = sorted(required_subes - actual_subes)
    if missing_subes:
        problems.append(f"{spec.tag}: missing detail SUBEs {missing_subes}")

    prims = _parse_primitives(script, spec.tag)
    if not prims:
        return problems + [f"{spec.tag}: no primitives parsed"]

    expected_x, expected_y, expected_z = spec.world_baseplate_dimensions
    east, north, up = spec.position
    baseplates = [
        p
        for p in prims
        if p["kind"] == "BOX"
        and abs(p.get("xlen", 0.0) - expected_x) <= _TOLERANCE_MM
        and abs(p.get("ylen", 0.0) - expected_y) <= _TOLERANCE_MM
        and abs(p.get("zlen", 0.0) - expected_z) <= _TOLERANCE_MM
    ]
    if len(baseplates) != 1:
        problems.append(
            f"{spec.tag}: expected one {expected_x:.1f} x {expected_y:.1f} x "
            f"{expected_z:.1f} baseplate, found {len(baseplates)}"
        )
    else:
        base = baseplates[0]
        underside = base["up"] - base["zlen"] / 2.0
        if (
            abs(base["east"] - east) > _TOLERANCE_MM
            or abs(base["north"] - north) > _TOLERANCE_MM
            or abs(underside - up) > _TOLERANCE_MM
        ):
            problems.append(
                f"{spec.tag}: baseplate datum is E {base['east']:.1f} "
                f"N {base['north']:.1f} U(bottom) {underside:.1f}; expected "
                f"E {east:.1f} N {north:.1f} U {up:.1f}"
            )

    lowest = min(p["u_min"] for p in prims)
    if abs(lowest - up) > _TOLERANCE_MM:
        problems.append(
            f"{spec.tag}: lowest primitive U {lowest:.1f}, expected foundation "
            f"datum U {up:.1f}"
        )

    forward = _AXIS_VECTOR[spec.layout_axis]
    cross = (-forward[1], forward[0])
    for primitive in prims:
        half_e, half_n = _world_plan_half_extents(primitive)
        local_l = (
            (primitive["east"] - east) * forward[0]
            + (primitive["north"] - north) * forward[1]
        )
        local_t = (
            (primitive["east"] - east) * cross[0]
            + (primitive["north"] - north) * cross[1]
        )
        half_l = half_e if abs(forward[0]) == 1 else half_n
        half_t = half_n if abs(forward[0]) == 1 else half_e
        if abs(local_l) + half_l > spec.length / 2.0 + _TOLERANCE_MM:
            problems.append(
                f"{spec.tag}: {primitive['kind']} exceeds baseplate longitudinal "
                f"footprint by {abs(local_l) + half_l - spec.length / 2.0:.1f} mm"
            )
        if abs(local_t) + half_t > spec.width / 2.0 + _TOLERANCE_MM:
            problems.append(
                f"{spec.tag}: {primitive['kind']} exceeds baseplate transverse "
                f"footprint by {abs(local_t) + half_t - spec.width / 2.0:.1f} mm"
            )

    suction_direction = _nozzle_direction(script, f"{safe}_SUCTION_NOZZLE")
    if suction_direction != spec.suction_axis.upper():
        problems.append(
            f"{spec.tag}: suction nozzle direction {suction_direction or 'missing'}, "
            f"expected {spec.suction_axis.upper()}"
        )
    discharge_direction = _nozzle_direction(script, f"{safe}_DISCHARGE_NOZZLE")
    if discharge_direction != spec.discharge_axis.upper():
        problems.append(
            f"{spec.tag}: discharge nozzle direction "
            f"{discharge_direction or 'missing'}, expected "
            f"{spec.discharge_axis.upper()}"
        )

    g = derive_pump_geometry(spec)
    motor_front_l = g.motor_centre_l + g.motor_length / 2.0
    casing_rear_l = g.casing_centre_l - g.casing_length / 2.0
    motor_to_casing_gap = casing_rear_l - motor_front_l
    bearing_l = min(
        max(55.0, motor_to_casing_gap) * 0.52,
        spec.length * 0.12,
    )
    bearing_start_l = casing_rear_l - bearing_l
    if not motor_front_l < bearing_start_l < casing_rear_l:
        problems.append(
            f"{spec.tag}: invalid longitudinal train; expected motor front "
            f"{motor_front_l:.1f} < bearing start {bearing_start_l:.1f} < "
            f"casing rear {casing_rear_l:.1f}"
        )
    actual_coupling_span = bearing_start_l - motor_front_l
    if abs(actual_coupling_span - g.coupling_length) > 0.5:
        problems.append(
            f"{spec.tag}: coupling clear span is {actual_coupling_span:.1f} mm, "
            f"expected {g.coupling_length:.1f} mm"
        )

    motor_e = east + forward[0] * g.motor_centre_l
    motor_n = north + forward[1] * g.motor_centre_l
    motor_candidates = [
        p
        for p in prims
        if p["kind"] == "CYLI"
        and p.get("axis") in (spec.layout_axis, _OPPOSITE[spec.layout_axis])
        and p.get("diam", 0.0) >= g.motor_height * 0.58
        and p.get("heig", 0.0) >= g.motor_length * 0.45
        and abs(p["east"] - motor_e) <= g.motor_length * 0.18
        and abs(p["north"] - motor_n) <= g.motor_length * 0.18
    ]
    if not motor_candidates:
        problems.append(
            f"{spec.tag}: detailed driver barrel not found at the motor end "
            f"opposite the casing"
        )

    profile = derive_detail_profile(spec, g)
    minimum_motor_length_ratio = 0.325 if spec.is_mc else 0.375
    minimum_motor_height_ratio = 0.40 if spec.is_mc else 0.43
    if g.motor_length < spec.length * minimum_motor_length_ratio:
        problems.append(
            f"{spec.tag}: motor length {g.motor_length:.1f} is below the "
            f"realistic envelope floor of {minimum_motor_length_ratio:.3f} x "
            "baseplate length"
        )
    if g.motor_height < spec.width * minimum_motor_height_ratio:
        problems.append(
            f"{spec.tag}: motor height {g.motor_height:.1f} is below the "
            f"realistic envelope floor of {minimum_motor_height_ratio:.2f} x "
            "baseplate width"
        )
    body_diameter = g.motor_height * _MOTOR_BODY_FACTOR[profile.motor_style]
    fin_diameter = _clamp(body_diameter * 0.055, 12.0, 26.0)
    finned_diameter = body_diameter + 1.44 * fin_diameter
    minimum_motor_aspect = 1.30 if spec.is_mc else 1.80
    if g.motor_length / finned_diameter < minimum_motor_aspect:
        problems.append(
            f"{spec.tag}: motor length/finned-diameter ratio "
            f"{g.motor_length / finned_diameter:.2f} is below the "
            f"{minimum_motor_aspect:.2f} realistic envelope floor"
        )

    cooling_ribs = _labeled_cylinders(
        script, "360-degree motor cooling rib "
    )
    if len(cooling_ribs) != profile.motor_fin_count:
        problems.append(
            f"{spec.tag}: expected {profile.motor_fin_count} full-circumference "
            f"motor cooling ribs, found {len(cooling_ribs)}"
        )
    elif cooling_ribs:
        body_radius = body_diameter / 2.0
        transverse_offsets: List[float] = []
        vertical_offsets: List[float] = []
        for rib in cooling_ribs:
            transverse = (
                (rib["east"] - east) * cross[0]
                + (rib["north"] - north) * cross[1]
            )
            vertical = rib["up"] - (up + g.shaft_u)
            transverse_offsets.append(transverse)
            vertical_offsets.append(vertical)
            radial = math.hypot(transverse, vertical)
            inner_radius = radial - rib["diam"] / 2.0
            outer_radius = radial + rib["diam"] / 2.0
            if inner_radius > body_radius + 0.6:
                problems.append(
                    f"{spec.tag}: a motor cooling rib is detached from the "
                    f"stator by {inner_radius - body_radius:.1f} mm"
                )
                break
            if outer_radius <= body_radius + 0.6:
                problems.append(
                    f"{spec.tag}: a motor cooling rib is buried inside the "
                    "stator envelope"
                )
                break
        coverage_floor = body_radius * 0.55
        if not (
            min(transverse_offsets) < -coverage_floor
            and max(transverse_offsets) > coverage_floor
            and min(vertical_offsets) < -coverage_floor
            and max(vertical_offsets) > coverage_floor
        ):
            problems.append(
                f"{spec.tag}: motor cooling ribs do not cover all four sides "
                "of the stator circumference"
            )

    if spec.is_mc:
        auxiliary_ribs = _labeled_cylinders(
            script, "360-degree MC auxiliary-motor cooling rib "
        )
        if len(auxiliary_ribs) != 10:
            problems.append(
                f"{spec.tag}: expected 10 all-round MC auxiliary-motor ribs, "
                f"found {len(auxiliary_ribs)}"
            )

    foot_pads = _labeled_boxes(script, "cast motor foot mounting pad")
    foot_webs = _labeled_boxes(script, "barrel-connected motor foot web")
    skid_rails = _labeled_boxes(script, "welded longitudinal skid rail")
    if len(foot_pads) != 4 or len(foot_webs) != 4:
        problems.append(
            f"{spec.tag}: expected four motor foot pads and four barrel webs, "
            f"found {len(foot_pads)} pads and {len(foot_webs)} webs"
        )
    else:
        rail_top_world = up + spec.baseplate_thickness + g.rail_height
        expected_pad_top = rail_top_world + _clamp(
            g.motor_height * 0.055, 16.0, 28.0
        )
        for pad in foot_pads:
            if abs(pad["up"] - pad["zlen"] / 2.0 - rail_top_world) > 0.3:
                problems.append(
                    f"{spec.tag}: a motor foot pad does not bear on the rail top"
                )
                break
        for web in foot_webs:
            local_t = (
                (web["east"] - east) * cross[0]
                + (web["north"] - north) * cross[1]
            )
            half_transverse = (
                web["ylen"] / 2.0
                if spec.layout_axis in ("E", "W")
                else web["xlen"] / 2.0
            )
            inner_t = max(0.0, abs(local_t) - half_transverse)
            if inner_t >= body_diameter / 2.0:
                problems.append(
                    f"{spec.tag}: a motor foot web misses the stator in plan"
                )
                break
            barrel_surface = up + g.shaft_u - math.sqrt(
                (body_diameter / 2.0) ** 2 - inner_t**2
            )
            web_bottom = web["up"] - web["zlen"] / 2.0
            web_top = web["up"] + web["zlen"] / 2.0
            overlap = web_top - barrel_surface
            if abs(web_bottom - expected_pad_top) > 0.3:
                problems.append(
                    f"{spec.tag}: a motor foot web is detached from its pad"
                )
                break
            if not 2.4 <= overlap <= 8.6:
                problems.append(
                    f"{spec.tag}: motor foot web/stator overlap is "
                    f"{overlap:.1f} mm; expected 2.4..8.6 mm"
                )
                break

        if len(skid_rails) != 2:
            problems.append(
                f"{spec.tag}: expected two longitudinal skid rails, found "
                f"{len(skid_rails)}"
            )
        else:
            for pad in foot_pads:
                pad_l = (
                    (pad["east"] - east) * forward[0]
                    + (pad["north"] - north) * forward[1]
                )
                pad_t = (
                    (pad["east"] - east) * cross[0]
                    + (pad["north"] - north) * cross[1]
                )
                pad_half_t = (
                    pad["ylen"] / 2.0
                    if spec.layout_axis in ("E", "W")
                    else pad["xlen"] / 2.0
                )
                rail = min(
                    skid_rails,
                    key=lambda candidate: abs(
                        (
                            (candidate["east"] - east) * cross[0]
                            + (candidate["north"] - north) * cross[1]
                        )
                        - pad_t
                    ),
                )
                rail_t = (
                    (rail["east"] - east) * cross[0]
                    + (rail["north"] - north) * cross[1]
                )
                rail_half_t = (
                    rail["ylen"] / 2.0
                    if spec.layout_axis in ("E", "W")
                    else rail["xlen"] / 2.0
                )
                overlap_t = min(
                    pad_t + pad_half_t,
                    rail_t + rail_half_t,
                ) - max(
                    pad_t - pad_half_t,
                    rail_t - rail_half_t,
                )
                if overlap_t < min(20.0, pad_half_t * 0.40):
                    problems.append(
                        f"{spec.tag}: motor foot pad at local L {pad_l:.1f} "
                        f"has only {max(0.0, overlap_t):.1f} mm transverse "
                        "bearing on its skid rail"
                    )
                    break

        hold_downs = _labeled_cylinders(
            script, "motor hold-down fastener: exposed threaded shank"
        )
        if len(hold_downs) != 4:
            problems.append(
                f"{spec.tag}: expected four motor hold-down shanks, found "
                f"{len(hold_downs)}"
            )
        elif len(skid_rails) == 2:
            for bolt in hold_downs:
                bolt_l = (
                    (bolt["east"] - east) * forward[0]
                    + (bolt["north"] - north) * forward[1]
                )
                bolt_t = (
                    (bolt["east"] - east) * cross[0]
                    + (bolt["north"] - north) * cross[1]
                )
                bolt_r = bolt["diam"] / 2.0
                rail = min(
                    skid_rails,
                    key=lambda candidate: abs(
                        (
                            (candidate["east"] - east) * cross[0]
                            + (candidate["north"] - north) * cross[1]
                        )
                        - bolt_t
                    ),
                )
                rail_l = (
                    (rail["east"] - east) * forward[0]
                    + (rail["north"] - north) * forward[1]
                )
                rail_t = (
                    (rail["east"] - east) * cross[0]
                    + (rail["north"] - north) * cross[1]
                )
                rail_half_l = (
                    rail["xlen"] / 2.0
                    if spec.layout_axis in ("E", "W")
                    else rail["ylen"] / 2.0
                )
                rail_half_t = (
                    rail["ylen"] / 2.0
                    if spec.layout_axis in ("E", "W")
                    else rail["xlen"] / 2.0
                )
                if (
                    abs(bolt_l - rail_l) + bolt_r > rail_half_l + 0.3
                    or abs(bolt_t - rail_t) + bolt_r > rail_half_t + 0.3
                ):
                    problems.append(
                        f"{spec.tag}: a motor hold-down bolt does not land "
                        "inside the longitudinal skid rail"
                    )
                    break
                bolt_base = bolt["up"] - bolt["heig"] / 2.0
                if abs(bolt_base - expected_pad_top) > 0.3:
                    problems.append(
                        f"{spec.tag}: a motor hold-down bolt does not start "
                        "at the foot-pad top"
                    )
                    break

    grille_horizontal = _labeled_boxes(
        script, "open fan-grille horizontal bar"
    )
    grille_vertical = _labeled_boxes(script, "open fan-grille vertical bar")
    if (
        len(grille_horizontal) != 5
        or len(grille_vertical) != 5
        or "motor fan grille face" in script
    ):
        problems.append(
            f"{spec.tag}: fan grille must be an open 5 x 5 lattice without "
            "a solid grille-face disc"
        )

    min_primitives = 145 if spec.is_mc else 105
    if len(prims) < min_primitives:
        problems.append(
            f"{spec.tag}: high-detail model has only {len(prims)} primitives; "
            f"expected at least {min_primitives} for {profile.duty.value}"
        )

    return problems
