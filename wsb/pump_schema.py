"""
Pump Equipment Schema
=====================

Shared data vocabulary for horizontal process pumps.  Project folders provide
``PumpSpec`` instances; the geometry and verification logic remain in ``wsb``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

from .schema import ASSUMED_PROVENANCES, Provenance

__all__ = [
    "CasingStyle",
    "CouplingGuardStyle",
    "MotorStyle",
    "PumpAppearance",
    "PumpDuty",
    "PumpFamily",
    "PumpSpec",
]


_CARDINAL_AXES = frozenset({"E", "W", "N", "S"})
_DISCHARGE_AXES = frozenset({"E", "W", "N", "S", "U", "D"})


class PumpFamily(str, Enum):
    """Geometry family used by the pump builder."""

    STANDARD_HORIZONTAL = "Standard horizontal centrifugal pump"
    MEDIUM_CONSISTENCY = "Medium-consistency pulp pump"


class PumpDuty(str, Enum):
    """Process-duty classification used to select visible construction details."""

    DILUTION = "Dilution/process-water service"
    FILTRATE = "Filtrate/washer-return service"
    SCREEN_FEED = "Stock/screen-feed service"
    BOOSTER = "Booster/high-head service"
    WIRE_WASH = "Wire-wash clean-water service"
    WASHER_FEED = "Washer stock-feed service"
    MEDIUM_CONSISTENCY = "Medium-consistency stock service"
    SCRUBBER_CIRCULATION = "Scrubber circulation service"


class MotorStyle(str, Enum):
    """Externally visible motor construction family."""

    IEC_STANDARD = "IEC standard ribbed motor"
    HEAVY_DUTY = "Heavy-duty high-torque motor"
    HIGH_SPEED = "Compact high-speed motor"
    CHEMICAL_DUTY = "Chemical-duty sealed motor"
    MC_MAIN_DRIVE = "MC-pump main drive"


class CasingStyle(str, Enum):
    """Externally visible pump hydraulic-end construction family."""

    PROCESS_VOLUTE = "General process volute"
    FILTRATE_VOLUTE = "Filtrate-service volute"
    STOCK_VOLUTE = "Stock/screen-feed open-impeller volute"
    HIGH_HEAD_VOLUTE = "Booster/high-head volute"
    CLEAN_WATER_VOLUTE = "Wire-wash clean-water volute"
    ABRASIVE_VOLUTE = "Abrasive-service lined volute"
    CHEMICAL_VOLUTE = "Chemical/scrubber circulation volute"
    MC_FLUIDIZER = "Medium-consistency fluidizer volute"


class CouplingGuardStyle(str, Enum):
    """Visible coupling-guard construction."""

    ROUND = "Full rounded guard"
    TAPERED = "Tapered guard"
    BOXED = "Fabricated box guard"
    VENTED_CAGE = "Open ventilated cage guard"


@dataclass(frozen=True)
class PumpAppearance:
    """
    Evidence-based Reference Values controlling non-contractual appearance.

    ``terminal_mount_side`` locates the terminal box across the motor and may
    be ``0`` when the plan only supports a centred top mounting.
    ``cable_gland_side`` controls only which side of that box receives the
    gland.  Keeping these separate avoids moving the complete terminal box
    merely to create an unsupported left/right variation.
    """

    code: str = "GENERIC"
    motor_style: MotorStyle = MotorStyle.IEC_STANDARD
    casing_style: CasingStyle = CasingStyle.PROCESS_VOLUTE
    guard_style: CouplingGuardStyle = CouplingGuardStyle.ROUND
    motor_diameter_scale: float = 1.0
    motor_length_scale: float = 1.0
    casing_diameter_scale: float = 1.0
    casing_length_scale: float = 1.0
    fin_count: int = 14
    casing_bolt_count: int = 10
    casing_rib_count: int = 2
    bearing_sections: int = 3
    terminal_mount_side: int = 0
    cable_gland_side: int = 1
    mc_variant: str = "NONE"

    def __post_init__(self) -> None:
        if not self.code:
            raise ValueError("Pump appearance code cannot be empty")
        for value, label in (
            (self.motor_diameter_scale, "motor_diameter_scale"),
            (self.motor_length_scale, "motor_length_scale"),
            (self.casing_diameter_scale, "casing_diameter_scale"),
            (self.casing_length_scale, "casing_length_scale"),
        ):
            if not 0.75 <= value <= 1.25:
                raise ValueError(f"{label} must be within 0.75..1.25, got {value}")
        if not 10 <= self.fin_count <= 24:
            raise ValueError(f"fin_count must be within 10..24, got {self.fin_count}")
        if not 6 <= self.casing_bolt_count <= 16:
            raise ValueError(
                f"casing_bolt_count must be within 6..16, got "
                f"{self.casing_bolt_count}"
            )
        if not 2 <= self.casing_rib_count <= 6:
            raise ValueError(
                f"casing_rib_count must be within 2..6, got {self.casing_rib_count}"
            )
        if not 3 <= self.bearing_sections <= 5:
            raise ValueError(
                f"bearing_sections must be within 3..5, got {self.bearing_sections}"
            )
        if self.terminal_mount_side not in (-1, 0, 1):
            raise ValueError("terminal_mount_side must be -1, 0 or 1")
        if self.cable_gland_side not in (-1, 1):
            raise ValueError("cable_gland_side must be -1 or 1")


@dataclass(frozen=True)
class PumpSpec:
    """
    Complete project specification for one pump.

    ``position`` is the geometric centre of the underside of the rectangular
    baseplate.  ``length`` is the longitudinal dimension and ``width`` is the
    transverse dimension, independent of world orientation.
    """

    tag: str
    name: str
    excel_row: int
    position: Tuple[float, float, float]
    length: float
    width: float
    suction_axis: str
    discharge_axis: str
    family: PumpFamily = PumpFamily.STANDARD_HORIZONTAL
    duty: PumpDuty = PumpDuty.DILUTION
    appearance: PumpAppearance = field(default_factory=PumpAppearance)
    longitudinal_axis: Optional[str] = None
    baseplate_thickness: float = 50.0
    top_view: Optional[str] = None
    auxiliary_side: int = 1
    suction_dn: Optional[int] = None
    discharge_dn: Optional[int] = None
    nozzle_specification: str = "ANSI-NOZZLES"
    nozzle_generic_type: str = "150lb Ansi Flanges"
    sources: Dict[str, Provenance] = field(default_factory=dict)
    notes: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        suction = self.suction_axis.upper()
        discharge = self.discharge_axis.upper()
        longitudinal = (self.longitudinal_axis or self.suction_axis).upper()
        if suction not in _CARDINAL_AXES:
            raise ValueError(
                f"{self.tag}: suction axis {self.suction_axis!r} is not cardinal"
            )
        if discharge not in _DISCHARGE_AXES:
            raise ValueError(
                f"{self.tag}: discharge axis {self.discharge_axis!r} is invalid"
            )
        if longitudinal not in _CARDINAL_AXES:
            raise ValueError(
                f"{self.tag}: longitudinal axis {longitudinal!r} is not cardinal"
            )
        if min(self.length, self.width, self.baseplate_thickness) <= 0:
            raise ValueError(f"{self.tag}: baseplate dimensions must be positive")
        for value, label in (
            (self.suction_dn, "suction_dn"),
            (self.discharge_dn, "discharge_dn"),
        ):
            if value is not None and value <= 0:
                raise ValueError(f"{self.tag}: {label} must be positive")
        if not self.nozzle_specification:
            raise ValueError(f"{self.tag}: nozzle_specification cannot be empty")
        if not self.nozzle_generic_type:
            raise ValueError(f"{self.tag}: nozzle_generic_type cannot be empty")
        if self.auxiliary_side not in (-1, 1):
            raise ValueError(f"{self.tag}: auxiliary_side must be -1 or 1")

    @property
    def safe_tag(self) -> str:
        """E3D-safe element name; filenames retain the contractual tag."""
        return self.tag.replace("-", "_")

    @property
    def is_mc(self) -> bool:
        return self.family is PumpFamily.MEDIUM_CONSISTENCY

    @property
    def layout_axis(self) -> str:
        """
        Direction from driver toward the pump casing in plan.

        It normally equals suction direction. Special side-suction pumps can
        override it without corrupting their contractual nozzle directions.
        """
        return (self.longitudinal_axis or self.suction_axis).upper()

    @property
    def world_baseplate_dimensions(self) -> Tuple[float, float, float]:
        """Baseplate ``XLEN, YLEN, ZLEN`` for the world-aligned PML BOX."""
        if self.layout_axis in ("E", "W"):
            return self.length, self.width, self.baseplate_thickness
        return self.width, self.length, self.baseplate_thickness

    def assumed_fields(self) -> List[Tuple[str, Provenance]]:
        """Project fields that remain Reference Values."""
        return [
            (field_name, provenance)
            for field_name, provenance in sorted(self.sources.items())
            if provenance in ASSUMED_PROVENANCES
        ]
