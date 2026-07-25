"""
Equipment Schema
================
The vocabulary every tank-modelling project shares: provenance levels, closure
and support types, and the :class:`TankSpec` / :class:`Nozzle` records the
geometry builder consumes.

This is engine code, not project data. A project supplies *instances* of these
types in its own ``Projects/<name>/equipment_data.py``; the definitions live here
so every project speaks the same vocabulary and the builder, report and
validator work against any of them unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple

__all__ = [
    "ASSUMED_PROVENANCES",
    "AgitatorType",
    "BottomType",
    "DataQualityException",
    "HeadType",
    "Nozzle",
    "Provenance",
    "SupportType",
    "TankSpec",
]


class Provenance(str, Enum):
    """Where a value came from. Drives the 'Reference Value' report section."""

    #: Read directly from Modeling_lists.xlsx. Contractual data.
    EXCEL = "Excel equipment list"
    #: Read from a JK-Project side-view P&ID sketch (V / h / o / T annotations).
    SIDE_VIEW = "Project side-view reference drawing"
    #: Read from a JK-Project top-view reference drawing.
    TOP_VIEW = "Project top-view reference drawing"
    #: Recovered from a corrupted Excel cell; see DATA_QUALITY_EXCEPTIONS.
    RECOVERED = "Recovered from corrupted Excel cell"
    #: Confirmed directly by the client, overriding the equipment list. Ranks
    #: above EXCEL: it is later information from the same authority.
    CLIENT = "Client confirmation (supersedes equipment list)"
    #: Derived arithmetically from primary data (e.g. shell height from volume).
    DERIVED = "Derived from project data"
    #: Reference Value - standard pulp-mill practice, pending confirmation.
    STANDARD = "Engineering-standard reference value"
    #: Reference Value - typical of Valmet/ANDRITZ/Voith equipment of this duty.
    VENDOR_TYPICAL = "Vendor-typical reference value (Valmet/ANDRITZ/Voith practice)"


#: Provenances that represent assumed rather than contractual data. Every value
#: carrying one of these must be listed as a Reference Value in the deliverable.
ASSUMED_PROVENANCES = frozenset(
    {Provenance.STANDARD, Provenance.VENDOR_TYPICAL, Provenance.DERIVED}
)


class HeadType(str, Enum):
    """Top closure geometry."""

    DISHED = "Dished head"
    CONICAL = "Conical roof"
    FLAT = "Flat roof"


class BottomType(str, Enum):
    """Bottom closure geometry."""

    FLAT = "Flat bottom"
    DISHED = "Dished bottom"
    CONICAL = "Conical bottom"


class SupportType(str, Enum):
    """How the vessel is carried."""

    SKIRT = "Skirt support"
    LEGS = "Support legs"
    GROUND = "Ground / slab bearing"


class AgitatorType(str, Enum):
    """
    How a mixing element is mounted, which decides where its steel appears.

    The three arrangements occupy completely different space on the vessel, so
    they cannot share one geometry. A top-entry unit puts a drive on the roof
    and a shaft down the centreline; a side-entry unit puts a motor on a shell
    nozzle low down with a short horizontal shaft; a bottom-entry scraper puts a
    drive underneath and sweeps the floor. Drawing one where the reference shows
    another is the kind of fabricated detail that clashes with real steel.
    """

    #: No mixing element fitted.
    NONE = "None"
    #: Roof-mounted drive, vertical shaft down the vessel centreline.
    TOP_ENTRY = "Top-entry agitator"
    #: Motor on a shell nozzle, short horizontal shaft - normal for a blow tank.
    SIDE_ENTRY = "Side-entry agitator"
    #: Drive below the cone, sweeping the floor - the discharge scraper fitted to
    #: an MC pulp storage tower.
    BOTTOM_SCRAPER = "Bottom-entry discharge scraper"


@dataclass(frozen=True)
class Nozzle:
    """
    A vessel nozzle.

    Elevations are measured from the tank bottom-center datum, so a nozzle's
    absolute position follows the vessel without recomputation.

    Args:
        name: Nozzle mark, unique within the parent tank.
        dn: Nominal diameter, DN (mm).
        elevation: Height above the tank bottom datum (mm).
        bearing: Plan bearing in degrees, measured counter-clockwise from East.
        service: Process duty, used to explain the placement in the report.
        vertical: True for a nozzle on the roof or floor pointing along U.
        provenance: Source of this nozzle's configuration.
    """

    name: str
    dn: int
    elevation: float
    bearing: float
    service: str
    vertical: bool = False
    provenance: Provenance = Provenance.STANDARD

    @property
    def is_assumed(self) -> bool:
        return self.provenance in ASSUMED_PROVENANCES


@dataclass(frozen=True)
class TankSpec:
    """
    Complete modeling specification for one tank.

    Geometry is expressed so that the model's **bottom center point** lands
    exactly on :attr:`position`, per the project positioning requirement.

    Args:
        tag: Equipment tag number.
        name: Equipment name / description.
        area: Process area.
        discipline: Discipline grouping from the equipment list.
        position: Installation coordinate (x, y, z) in mm - the BOTTOM CENTER.
        diameter: Shell inside diameter (mm).
        height: Overall height from bottom datum to top tangent (mm).
        volume_m3: Nominal working volume from project data, if stated.
        head: Top closure type.
        bottom: Bottom closure type.
        support: Support arrangement.
        skirt_height: Skirt/leg height below the shell (mm); 0 if ground-bearing.
        cone_height: Height of the bottom cone (mm); 0 if not conical.
        cone_outlet_dn: Bottom cone outlet diameter (mm).
        head_height: Rise of the top head above the top tangent line (mm).
        outer_diameter: Outer shell diameter for double-shell towers (mm).
        agitator: True if an agitator/scraper is shown on the reference drawing.
        agitator_type: How that agitator is mounted. Defaults to a top-entry unit
            when ``agitator`` is set but no type is given, which is the common
            arrangement for a stock chest.
        stiffening_rings: Number of external stiffening rings.
        platform_elevations: Access platform elevations above datum (mm).
        nozzles: Nozzle schedule.
        sources: Provenance per geometric field.
        notes: Outstanding issues to carry into the deliverable.
    """

    tag: str
    name: str
    area: str
    discipline: str
    position: Tuple[float, float, float]
    diameter: float
    height: float
    volume_m3: Optional[float] = None
    head: HeadType = HeadType.DISHED
    bottom: BottomType = BottomType.FLAT
    support: SupportType = SupportType.GROUND
    skirt_height: float = 0.0
    cone_height: float = 0.0
    cone_outlet_dn: float = 0.0
    head_height: float = 0.0
    outer_diameter: float = 0.0
    agitator: bool = False
    agitator_type: Optional[AgitatorType] = None
    stiffening_rings: int = 0
    platform_elevations: Tuple[float, ...] = ()
    nozzles: Tuple[Nozzle, ...] = ()
    sources: Dict[str, Provenance] = field(default_factory=dict)
    notes: Tuple[str, ...] = ()

    @property
    def radius(self) -> float:
        return self.diameter / 2.0

    @property
    def mixer(self) -> AgitatorType:
        """
        The mixing arrangement to build, reconciling the flag and the type.

        ``agitator`` predates ``agitator_type``: entries that only set the flag
        get a top-entry unit, which is what the builder drew before the mounting
        types existed and what a stock chest normally has. Setting the type is
        what a reference drawing showing a different arrangement calls for.
        """
        if self.agitator_type is not None:
            return self.agitator_type
        return AgitatorType.TOP_ENTRY if self.agitator else AgitatorType.NONE

    @property
    def total_height(self) -> float:
        """Bottom datum to head apex, including skirt and top head."""
        return self.skirt_height + self.height + self.head_height

    def assumed_fields(self) -> List[Tuple[str, Provenance]]:
        """Fields whose values are Reference Values, for the report."""
        return [
            (fname, prov)
            for fname, prov in sorted(self.sources.items())
            if prov in ASSUMED_PROVENANCES
        ]


@dataclass(frozen=True)
class DataQualityException:
    """A defect found in the source data and the correction applied."""

    tag: str
    field_name: str
    source_value: str
    corrected_value: str
    rationale: str
