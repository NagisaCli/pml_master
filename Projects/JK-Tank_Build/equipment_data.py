"""
JK-Project — WSB Tank Equipment Dataset
=======================================
Authoritative equipment data for the Pulp Mill Washing, Screening & Bleaching
(WSB) area, derived from ``Modeling_lists.xlsx`` in this folder and cross-checked
against the reference drawings in ``Model_reference(Part_Side_View)``.

This is **project data**. The types it instantiates (``TankSpec``, ``Nozzle``,
``Provenance`` and the closure/support enums) are engine code in
``wsb.schema``; the geometry builder, validator and report are shared by every
project. Only the numbers below are specific to JK-Project.

Data provenance policy
----------------------
The Excel equipment list is the contractual primary source. Where a value is
taken from anywhere else it carries an explicit :class:`Provenance`, so every
number in a delivered model can be traced back to its origin and revised when
official design data arrives.

Three data defects in the source workbook are corrected here rather than by
editing the workbook. Each correction is reported as a
:class:`DataQualityException` so it appears in the delivered engineering report:

1. Column F coordinates are corrupted on 13 of 22 rows. Rows stored as text
   retain ``(x,y,z)``; rows stored as numbers lost their parentheses and commas,
   so Excel concatenated the digits (``-1500019860300`` == ``(15000,19860,300)``).
   All restored coordinates are positive per project direction; the minus sign on
   the corrupted cell is an artefact of the concatenation. Rows that survived as
   text keep their listed signs unchanged.
2. Height and diameter are transposed for 205-TA-008 and 205-TA-011. The
   side-view sketches give the correct orientation, confirmed independently by
   the stated vessel volume.
3. ``Model_Reference(All_Top_View)/2205-TA-050.png`` is misnamed; the drawing it
   contains is 205-TA-059.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# A project folder is data, not an installed package, so it may be loaded by
# path with the repository root absent from sys.path. Make the engine importable
# either way.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from wsb.schema import (  # noqa: E402
    ASSUMED_PROVENANCES,
    AgitatorType,
    BottomType,
    DataQualityException,
    HeadType,
    Nozzle,
    Provenance,
    SupportType,
    TankSpec,
)

__all__ = [
    "WSB_TANKS",
    "DATA_QUALITY_EXCEPTIONS",
    "get_tank",
    "tanks_by_area",
    "reference_values",
]


# ---------------------------------------------------------------------------
# Data quality exceptions
# ---------------------------------------------------------------------------

_COORD_RATIONALE = (
    "Excel stored this cell as a number, so the parentheses and commas of the "
    "original '(x,y,z)' text were lost and the digits concatenated. Recovered by "
    "stripping the trailing z=300 (constant across all 22 rows) and splitting the "
    "remainder into a 5-digit x and a 4-5 digit y. Per project direction all "
    "restored coordinates are positive: the minus sign carried by the corrupted "
    "numeric cell is an artefact of the concatenation, not project data. Rows "
    "that survived as text are left exactly as listed and are not re-signed. "
    "The z shown here is the recovered value after the 300 mm lowering described "
    "in the ELEVATION-DATUM exception; the source cell held z=300."
)

#: Applies to every tank, so it is stated once rather than repeated 22 times.
_ELEVATION_RATIONALE = (
    "Client direction, 2026-07-24: lower all WSB equipment by 300 mm. The "
    "equipment list issues every installation coordinate at z=300 mm (the area "
    "finished floor level); the modelled datum is therefore z=0. This is a "
    "deliberate deviation from the contractual equipment list applied to the "
    "installation coordinate only - no diameter, height, support height, plan "
    "position or orientation changes with it, so every tank's bottom centre "
    "point still coincides exactly with its (shifted) installation coordinate."
)

DATA_QUALITY_EXCEPTIONS: Tuple[DataQualityException, ...] = (
    DataQualityException(
        "ALL (22 tanks)", "position - elevation datum", "z = 300 mm", "z = 0 mm",
        _ELEVATION_RATIONALE),
    DataQualityException(
        "203-TA-006", "position", "-1500019860300", "(15000, 19860, 0)", _COORD_RATIONALE),
    DataQualityException(
        "203-TA-019", "position", "-154456415300", "(15445, 6415, 0)", _COORD_RATIONALE),
    DataQualityException(
        "203-TA-044", "position", "-116013981300", "(11601, 3981, 0)", _COORD_RATIONALE),
    DataQualityException(
        "204-TA-021", "position", "-236506000300", "(23650, 6000, 0)", _COORD_RATIONALE),
    DataQualityException(
        "204-TA-034", "position", "-2251221358300", "(22512, 21358, 0)", _COORD_RATIONALE),
    DataQualityException(
        "204-TA-035", "position", "-2701319860300", "(27013, 19860, 0)", _COORD_RATIONALE),
    DataQualityException(
        "205-TA-011", "position", "-3306719057300", "(33067, 19057, 0)", _COORD_RATIONALE),
    DataQualityException(
        "205-TA-016", "position", "-338336000300", "(33833, 6000, 0)", _COORD_RATIONALE),
    DataQualityException(
        "205-TA-029", "position", "-3941819057300", "(39418, 19057, 0)", _COORD_RATIONALE),
    DataQualityException(
        "205-TA-036", "position", "-418336000300", "(41833, 6000, 0)", _COORD_RATIONALE),
    DataQualityException(
        "205-TA-045", "position", "-4742319057300", "(47423, 19057, 0)", _COORD_RATIONALE),
    DataQualityException(
        "205-TA-052", "position", "-498386000300", "(49838, 6000, 0)", _COORD_RATIONALE),
    DataQualityException(
        "205-TA-056", "position", "-6703021008300", "(67030, 21008, 0)", _COORD_RATIONALE),
    DataQualityException(
        "205-TA-008", "height / diameter", "h=2.6 m, dia=18.6 m", "h=18.6 m, dia=2.6 m",
        "Transposed in the equipment list. The side-view sketch states h=18.6 m, "
        "o=2.6 m. Confirmed by volume: the sketch gives V=65 m3, which matches a "
        "2.6 m bore (cylindrical shell plus bottom cone); the transposed reading "
        "would give roughly 706 m3.",
    ),
    DataQualityException(
        "205-TA-011", "height / diameter", "h=4.0 m, dia=5.3 m", "h=5.3 m, dia=4.0 m",
        "Transposed in the equipment list. The side-view sketch states h=5.3 m, "
        "o=4.0 m, V=63 m3. A 4.0 m bore at 5.3 m height gives 66.6 m3, matching "
        "the stated volume; the transposed reading would give 88 m3.",
    ),
    DataQualityException(
        "204-TA-001", "height", "(To Be Determined)", "13.0 m",
        "Absent from the equipment list but stated on the side-view sketch "
        "(V=64 m3, h=13.0 m, o=3.2 m, T=94 C).",
    ),
    DataQualityException(
        "205-TA-052", "diameter", "6.2 m", "1.05 m",
        "Corrected on client confirmation, 2026-07-24. The 6.2 m in the "
        "equipment list was queried as implausible for a barometric leg - it is "
        "six times the bore of the other two droplegs and would not hold a "
        "vacuum seal economically. The corrected 1.05 m matches 205-TA-016 and "
        "205-TA-036 exactly.",
    ),
    DataQualityException(
        "205-TA-059", "reference drawing filename",
        "Model_Reference(All_Top_View)/2205-TA-050.png",
        "should be 205-TA-059.png",
        "The file is misnamed. The drawing it contains is titled "
        "'205-TA-059 BLEACH PLANT SCRUBBER'. No tank 205-TA-050 exists in the "
        "equipment list.",
    ),
)


# ---------------------------------------------------------------------------
# Nozzle schedules
# ---------------------------------------------------------------------------
# Where a reference drawing shows the nozzle arrangement it is followed. Where it
# does not, a minimal process-logical set is provided so the vessel is ready for
# piping: feed, discharge, overflow, vent, drain and a manway. Sizes follow the
# tank duty and are flagged as Reference Values.


def _standard_tank_nozzles(
    diameter: float,
    height: float,
    *,
    feed_dn: int = 200,
    discharge_dn: int = 250,
    vent_dn: int = 150,
    overflow_dn: int = 200,
    manway_dn: int = 600,
    provenance: Provenance = Provenance.STANDARD,
) -> Tuple[Nozzle, ...]:
    """
    Minimum process-logical nozzle set for an atmospheric process tank.

    Placement follows normal practice: feed high on the shell, discharge at the
    low point, overflow just below the top tangent, vent on the roof, drain at
    the bottom, and a shell manway at accessible height. Bearings are spread so
    that connections do not collide when piping is routed later.
    """
    return (
        Nozzle("N1", feed_dn, height * 0.85, 90.0, "Stock / filtrate feed inlet",
               provenance=provenance),
        Nozzle("N2", discharge_dn, 400.0, 270.0, "Pump suction / discharge outlet",
               provenance=provenance),
        Nozzle("N3", overflow_dn, height * 0.94, 180.0, "Overflow to sewer / recovery",
               provenance=provenance),
        Nozzle("N4", vent_dn, height, 0.0, "Roof vent", vertical=True,
               provenance=provenance),
        Nozzle("N5", 80, 250.0, 315.0, "Drain", provenance=provenance),
        Nozzle("M1", manway_dn, 1200.0, 45.0, "Shell manway - inspection access",
               provenance=provenance),
    )


def _tower_nozzles(
    diameter: float,
    height: float,
    *,
    feed_dn: int = 250,
    discharge_dn: int = 300,
    provenance: Provenance = Provenance.STANDARD,
) -> Tuple[Nozzle, ...]:
    """
    Nozzle set for an upflow reactor / bleaching tower.

    Upflow towers are fed at the bottom cone and discharge at the top, with
    sample and chemical-injection points distributed up the shell.
    """
    return (
        Nozzle("N1", feed_dn, 600.0, 90.0, "MC pulp feed inlet (bottom, upflow)",
               provenance=provenance),
        Nozzle("N2", discharge_dn, height * 0.96, 270.0, "Pulp discharge outlet (top)",
               provenance=provenance),
        Nozzle("N3", 100, height * 0.30, 0.0, "Chemical injection / sample point",
               provenance=provenance),
        Nozzle("N4", 100, height * 0.60, 180.0, "Sample point",
               provenance=provenance),
        Nozzle("N5", 150, height, 45.0, "Vent / relief", vertical=True,
               provenance=provenance),
        Nozzle("M1", 600, 1500.0, 135.0, "Shell manway - inspection access",
               provenance=provenance),
    )


def _dropleg_nozzles(height: float) -> Tuple[Nozzle, ...]:
    """
    Nozzle set for a washer dropleg (barometric leg).

    A dropleg is a tall small-bore standpipe that maintains the vacuum seal for a
    drum washer: filtrate enters at the top and leaves through a seal pot at the
    bottom.
    """
    return (
        Nozzle("N1", 400, height * 0.97, 90.0, "Filtrate inlet from washer vat",
               provenance=Provenance.STANDARD),
        Nozzle("N2", 400, 300.0, 270.0, "Seal pot / filtrate outlet",
               provenance=Provenance.STANDARD),
        Nozzle("N3", 150, height, 0.0, "Vacuum / air separation vent",
               vertical=True, provenance=Provenance.STANDARD),
    )


# ---------------------------------------------------------------------------
# Equipment register - 22 tanks
# ---------------------------------------------------------------------------
# Elevation note: every position carries z=0 mm. The equipment list issues these
# coordinates at z=300 mm, the WSB area finished floor level; the client has
# since directed that all equipment be lowered by 300 mm, placing the
# bottom-center datum on the slab top rather than on the finished floor. The
# shift is applied to the installation coordinate only - no dimension, plan
# position or support height changes with it, and skirt or leg height still
# raises the shell above the datum.
#
# Recorded as a data-quality exception (ELEVATION-DATUM) so the deliverable
# shows the deviation from the contractual equipment list rather than hiding it.

WSB_TANKS: Tuple[TankSpec, ...] = (
    # -- Area 203: Brown Stock / O2 Stage -------------------------------
    TankSpec(
        tag="203-TA-006",
        name="BROWN STOCK WASHER FILTRATE TANK",
        area="203 - Brown Stock / O2 Stage",
        discipline="Tanks & Vessels",
        position=(15000.0, 19860.0, 0.0),
        diameter=5600.0,
        height=9200.0,
        volume_m3=197.0,
        head=HeadType.CONICAL,
        bottom=BottomType.FLAT,
        support=SupportType.GROUND,
        head_height=700.0,
        agitator=True,
        stiffening_rings=2,
        nozzles=_standard_tank_nozzles(5600.0, 9200.0, feed_dn=400, discharge_dn=400),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.EXCEL,
            "volume_m3": Provenance.EXCEL,
            "head": Provenance.SIDE_VIEW,
            "head_height": Provenance.STANDARD,
            "agitator": Provenance.SIDE_VIEW,
            "stiffening_rings": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "Side view shows two internal agitators (h=5.0 m o=1.6 m and "
            "h=4.1 m o=2.2 m); modelled as a single shaft with two impellers.",
            "Nozzle schedule not dimensioned on the reference drawings - "
            "Reference Values provided for piping readiness.",
        ),
    ),
    TankSpec(
        tag="203-TA-019",
        name="OXYGEN STAGE FEED TANK",
        area="203 - Brown Stock / O2 Stage",
        discipline="Tanks & Vessels",
        position=(15445.0, 6415.0, 0.0),
        diameter=2000.0,
        height=8500.0,
        volume_m3=13.0,
        head=HeadType.DISHED,
        bottom=BottomType.DISHED,
        support=SupportType.SKIRT,
        skirt_height=1500.0,
        head_height=500.0,
        stiffening_rings=0,
        nozzles=(
            Nozzle("N1", 200, 7800.0, 90.0, "Brown stock feed inlet",
                   provenance=Provenance.SIDE_VIEW),
            Nozzle("N2", 800, 0.0, 270.0, "DN800 bottom outlet to MC pump",
                   vertical=True, provenance=Provenance.SIDE_VIEW),
            Nozzle("N3", 100, 6500.0, 0.0, "Level transmitter LS-3492 connection",
                   provenance=Provenance.SIDE_VIEW),
            Nozzle("N4", 100, 3000.0, 180.0, "Level control LIC-3493 connection",
                   provenance=Provenance.SIDE_VIEW),
            Nozzle("N5", 150, 8500.0, 45.0, "Vent", vertical=True,
                   provenance=Provenance.STANDARD),
            Nozzle("M1", 500, 1800.0, 135.0, "Manway", provenance=Provenance.STANDARD),
        ),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.EXCEL,
            "volume_m3": Provenance.EXCEL,
            "head": Provenance.SIDE_VIEW,
            "bottom": Provenance.SIDE_VIEW,
            "support": Provenance.SIDE_VIEW,
            "skirt_height": Provenance.STANDARD,
            "head_height": Provenance.STANDARD,
            "nozzles": Provenance.SIDE_VIEW,
        },
        notes=(
            "Design temperature 92 C, consistency 11% per side view.",
            "Skirt height is a Reference Value - the drawing shows the vessel "
            "elevated above an MC pump but gives no dimension.",
        ),
    ),
    TankSpec(
        tag="203-TA-024",
        name="1st OXYGEN REACTOR",
        area="203 - Brown Stock / O2 Stage",
        discipline="Reactors & Towers",
        position=(12005.0, -3752.0, 0.0),
        diameter=2000.0,
        height=20300.0,
        volume_m3=49.0,
        head=HeadType.DISHED,
        bottom=BottomType.CONICAL,
        support=SupportType.SKIRT,
        skirt_height=2000.0,
        cone_height=1800.0,
        cone_outlet_dn=300.0,
        head_height=500.0,
        stiffening_rings=4,
        platform_elevations=(6000.0, 12000.0, 18000.0),
        nozzles=_tower_nozzles(2000.0, 20300.0, feed_dn=300, discharge_dn=300),
        sources={
            "position": Provenance.EXCEL,
            "diameter": Provenance.EXCEL,
            "height": Provenance.EXCEL,
            "volume_m3": Provenance.EXCEL,
            "head": Provenance.SIDE_VIEW,
            "bottom": Provenance.SIDE_VIEW,
            "cone_height": Provenance.STANDARD,
            "cone_outlet_dn": Provenance.SIDE_VIEW,
            "support": Provenance.STANDARD,
            "skirt_height": Provenance.STANDARD,
            "platform_elevations": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "Upflow oxygen delignification reactor: 91 C, 20 min retention, 11% "
            "consistency per side view.",
            "Side view shows a 300 mm bottom cone outlet and a 100 mm top "
            "connection; cone height is a Reference Value.",
            "Platform elevations are Reference Values - not shown on the "
            "available drawings.",
        ),
    ),
    TankSpec(
        tag="203-TA-029",
        name="2nd OXYGEN REACTOR",
        area="203 - Brown Stock / O2 Stage",
        discipline="Reactors & Towers",
        position=(16609.0, -3752.0, 0.0),
        diameter=2600.0,
        height=23500.0,
        volume_m3=97.0,
        head=HeadType.DISHED,
        bottom=BottomType.CONICAL,
        support=SupportType.SKIRT,
        skirt_height=2000.0,
        cone_height=2200.0,
        cone_outlet_dn=300.0,
        head_height=650.0,
        stiffening_rings=5,
        platform_elevations=(6000.0, 12000.0, 18000.0, 22000.0),
        nozzles=_tower_nozzles(2600.0, 23500.0, feed_dn=300, discharge_dn=300),
        sources={
            "position": Provenance.EXCEL,
            "diameter": Provenance.EXCEL,
            "height": Provenance.EXCEL,
            "volume_m3": Provenance.EXCEL,
            "head": Provenance.SIDE_VIEW,
            "bottom": Provenance.SIDE_VIEW,
            "cone_height": Provenance.STANDARD,
            "cone_outlet_dn": Provenance.SIDE_VIEW,
            "support": Provenance.STANDARD,
            "skirt_height": Provenance.STANDARD,
            "platform_elevations": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "Upflow reactor: 100 C, 40 min retention, 11% consistency per side view.",
            "Side view shows 300 mm and 150 mm bottom connections.",
        ),
    ),
    TankSpec(
        tag="203-TA-044",
        name="INSTRUMENT AIR RECEIVER",
        area="203 - Brown Stock / O2 Stage",
        discipline="Tanks & Vessels",
        position=(11601.0, 3981.0, 0.0),
        diameter=800.0,
        height=2500.0,
        head=HeadType.DISHED,
        bottom=BottomType.DISHED,
        support=SupportType.LEGS,
        skirt_height=600.0,
        head_height=200.0,
        nozzles=(
            Nozzle("N1", 80, 2200.0, 90.0, "Compressed air inlet",
                   provenance=Provenance.STANDARD),
            Nozzle("N2", 80, 500.0, 270.0, "Air outlet to distribution header",
                   provenance=Provenance.STANDARD),
            Nozzle("N3", 25, 0.0, 180.0, "Condensate drain / auto trap",
                   vertical=True, provenance=Provenance.STANDARD),
            Nozzle("N4", 50, 2500.0, 0.0, "Safety relief valve", vertical=True,
                   provenance=Provenance.STANDARD),
        ),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.STANDARD,
            "head": Provenance.STANDARD,
            "bottom": Provenance.STANDARD,
            "support": Provenance.STANDARD,
            "skirt_height": Provenance.STANDARD,
            "head_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height and volume are '(No Reference)' in the equipment "
            "list and no side view is provided. Height 2500 mm is a Reference "
            "Value - a vertical air receiver on legs at DN800, the standard "
            "configuration for an instrument air package.",
            "A pressure vessel, not an atmospheric tank: dished heads both ends "
            "and a relief valve are assumed.",
        ),
    ),

    # -- Area 204: Screening & Washing -----------------------------------
    TankSpec(
        tag="204-TA-001",
        name="OXYGEN STAGE BLOW TANK",
        area="204 - Screening & Washing",
        discipline="Tanks & Vessels",
        position=(21008.0, -4151.0, 0.0),
        diameter=3200.0,
        height=13000.0,
        volume_m3=64.0,
        head=HeadType.CONICAL,
        bottom=BottomType.CONICAL,
        support=SupportType.SKIRT,
        skirt_height=1500.0,
        cone_height=2000.0,
        cone_outlet_dn=400.0,
        head_height=900.0,
        stiffening_rings=3,
        agitator=True,
        agitator_type=AgitatorType.SIDE_ENTRY,
        nozzles=(
            Nozzle("N1", 400, 11500.0, 90.0, "Blow line inlet from O2 reactor",
                   provenance=Provenance.SIDE_VIEW),
            Nozzle("N2", 400, 0.0, 270.0, "Bottom cone outlet to pump",
                   vertical=True, provenance=Provenance.STANDARD),
            Nozzle("N3", 600, 13000.0, 0.0, "Steam / vapour relief to cyclone",
                   vertical=True, provenance=Provenance.SIDE_VIEW),
            Nozzle("N4", 200, 6000.0, 180.0, "Dilution filtrate",
                   provenance=Provenance.STANDARD),
            Nozzle("M1", 600, 2000.0, 135.0, "Manway", provenance=Provenance.STANDARD),
        ),
        sources={
            "position": Provenance.EXCEL,
            "diameter": Provenance.EXCEL,
            "height": Provenance.SIDE_VIEW,
            "volume_m3": Provenance.SIDE_VIEW,
            "head": Provenance.SIDE_VIEW,
            "bottom": Provenance.STANDARD,
            "support": Provenance.STANDARD,
            "cone_height": Provenance.STANDARD,
            "skirt_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
            "agitator_type": Provenance.TOP_VIEW,
        },
        notes=(
            "Height recovered from the side view (h=13.0 m, V=64 m3, T=94 C); the "
            "equipment list records it as 'To Be Determined'.",
            "Side view shows a tall vapour stack on the roof - modelled as the "
            "DN600 relief connection.",
            "Top view (filed as Model_Reference(All_Top_View)/203-TA-001.png, "
            "which is misnamed - the drawing inside is 204-TA-001) shows a "
            "side-entry agitator, 204-AG-001 'Screening feed tank agitator', "
            "mounted on the lower shell. Modelled as a side-entry unit; the "
            "motor and gearbox envelope is a Reference Value.",
        ),
    ),
    TankSpec(
        tag="204-TA-021",
        name="POST O2 WASHER DROPLEG",
        area="204 - Screening & Washing",
        discipline="Tanks & Vessels",
        position=(23650.0, 6000.0, 0.0),
        diameter=710.0,
        height=12000.0,
        head=HeadType.FLAT,
        bottom=BottomType.CONICAL,
        support=SupportType.LEGS,
        skirt_height=500.0,
        cone_height=900.0,
        cone_outlet_dn=300.0,
        nozzles=_dropleg_nozzles(12000.0),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.STANDARD,
            "name": Provenance.SIDE_VIEW,
            "head": Provenance.SIDE_VIEW,
            "bottom": Provenance.SIDE_VIEW,
            "support": Provenance.SIDE_VIEW,
            "cone_height": Provenance.SIDE_VIEW,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height is 'To Be Determined' in the equipment list and "
            "the side view is not dimensioned. 12000 mm is a Reference Value - a "
            "barometric dropleg must exceed roughly 10 m to hold the vacuum seal, "
            "which is standard washer practice.",
            "Side view confirms a tall slender standpipe with an offset conical "
            "bottom discharging to a pump through a valve.",
            "Service designation corrected: the side view titles this item 'Post "
            "O2 washer drop leg' and the top view labels it '204-TA-021/DROPLEG' "
            "served by 204-PU-028 MC pump. It takes filtrate from the post-oxygen "
            "washer, not from screening, so the nozzle services are named for the "
            "post-O2 washer vat.",
        ),
    ),
    TankSpec(
        tag="204-TA-034",
        name="SCREEN DILUTION TANK",
        area="204 - Screening & Washing",
        discipline="Tanks & Vessels",
        position=(22512.0, 21358.0, 0.0),
        diameter=2300.0,
        height=7600.0,
        volume_m3=29.0,
        head=HeadType.CONICAL,
        bottom=BottomType.FLAT,
        support=SupportType.GROUND,
        head_height=350.0,
        stiffening_rings=1,
        nozzles=_standard_tank_nozzles(2300.0, 7600.0, feed_dn=250, discharge_dn=300),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.EXCEL,
            "volume_m3": Provenance.EXCEL,
            "head": Provenance.SIDE_VIEW,
            "head_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=("Design temperature 91 C per side view.",),
    ),
    TankSpec(
        tag="204-TA-035",
        name="POST OXYGEN FILTRATE TANK",
        area="204 - Screening & Washing",
        discipline="Tanks & Vessels",
        position=(27013.0, 19860.0, 0.0),
        diameter=5600.0,
        height=7600.0,
        volume_m3=158.0,
        head=HeadType.CONICAL,
        bottom=BottomType.FLAT,
        support=SupportType.GROUND,
        head_height=700.0,
        agitator=True,
        stiffening_rings=2,
        nozzles=(
            Nozzle("N1", 300, 5500.0, 90.0, "DN300 filtrate inlet",
                   provenance=Provenance.SIDE_VIEW),
            Nozzle("N2", 400, 400.0, 270.0, "Filtrate pump suction",
                   provenance=Provenance.STANDARD),
            Nozzle("N3", 300, 7100.0, 180.0, "Overflow", provenance=Provenance.STANDARD),
            Nozzle("N4", 200, 7600.0, 0.0, "Vent", vertical=True,
                   provenance=Provenance.STANDARD),
            Nozzle("N5", 80, 250.0, 315.0, "Drain", provenance=Provenance.STANDARD),
            Nozzle("M1", 600, 1200.0, 45.0, "Manway", provenance=Provenance.STANDARD),
        ),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.EXCEL,
            "volume_m3": Provenance.EXCEL,
            "head": Provenance.SIDE_VIEW,
            "head_height": Provenance.STANDARD,
            "agitator": Provenance.SIDE_VIEW,
            "nozzles": Provenance.SIDE_VIEW,
        },
        notes=(
            "Side view shows two agitators (h=4.8 m o=1.3 m and h=4.0 m o=1.7 m) "
            "and a DN300 inlet; 91 C.",
        ),
    ),

    # -- Area 205: Bleaching Plant ---------------------------------------
    TankSpec(
        tag="205-TA-001",
        name="UNBLEACHED PULP STORAGE TOWER",
        area="205 - Bleaching Plant",
        discipline="Reactors & Towers",
        position=(26863.0, -11601.0, 0.0),
        diameter=9000.0,
        height=26400.0,
        volume_m3=1000.0,
        head=HeadType.CONICAL,
        bottom=BottomType.DISHED,
        support=SupportType.GROUND,
        head_height=1800.0,
        outer_diameter=10800.0,
        agitator=True,
        agitator_type=AgitatorType.BOTTOM_SCRAPER,
        stiffening_rings=6,
        platform_elevations=(8000.0, 16000.0, 24000.0),
        nozzles=(
            Nozzle("N1", 400, 24000.0, 90.0, "MC pulp feed inlet (top)",
                   provenance=Provenance.SIDE_VIEW),
            Nozzle("N2", 500, 500.0, 270.0, "Bottom discharge to drop leg",
                   provenance=Provenance.SIDE_VIEW),
            Nozzle("N3", 200, 3000.0, 0.0, "Dilution water ring - lower",
                   provenance=Provenance.SIDE_VIEW),
            Nozzle("N4", 200, 3000.0, 180.0, "Dilution water ring - upper",
                   provenance=Provenance.SIDE_VIEW),
            Nozzle("N5", 300, 26400.0, 45.0, "Vent", vertical=True,
                   provenance=Provenance.STANDARD),
            Nozzle("M1", 600, 1500.0, 135.0, "Manway", provenance=Provenance.STANDARD),
        ),
        sources={
            "position": Provenance.EXCEL,
            "diameter": Provenance.EXCEL,
            "height": Provenance.EXCEL,
            "volume_m3": Provenance.EXCEL,
            "head": Provenance.SIDE_VIEW,
            "bottom": Provenance.SIDE_VIEW,
            "outer_diameter": Provenance.TOP_VIEW,
            "agitator": Provenance.TOP_VIEW,
            "agitator_type": Provenance.TOP_VIEW,
            "head_height": Provenance.STANDARD,
            "platform_elevations": Provenance.STANDARD,
            "nozzles": Provenance.SIDE_VIEW,
        },
        notes=(
            "MC storage tower, 71 C, 12% consistency, V=1000 m3 per side view.",
            "Top view shows a concentric outer circle: modelled as an insulation "
            "or outer-shell envelope at 10800 mm. Its thickness is a Reference Value.",
            "Side view shows 205-AG-002 'MC discharge scrapper' at the bottom of "
            "the dished floor, and the top view labels the same item at the "
            "tower centre. Modelled as a bottom-entry discharge scraper: drive "
            "below the floor, hub and sweep arms above it. It is NOT a top-entry "
            "agitator - neither drawing shows a roof drive on this tower.",
            "Associated 205-TA-014 storage tower bottom drop leg is a separate tag "
            "and is not in the modelling scope.",
        ),
    ),
    TankSpec(
        tag="205-TA-008",
        name="D0 TOWER",
        area="205 - Bleaching Plant",
        discipline="Reactors & Towers",
        position=(34016.0, -4501.0, 0.0),
        diameter=2600.0,
        height=18600.0,
        volume_m3=65.0,
        head=HeadType.FLAT,
        bottom=BottomType.CONICAL,
        support=SupportType.SKIRT,
        skirt_height=2500.0,
        cone_height=3000.0,
        cone_outlet_dn=300.0,
        stiffening_rings=4,
        platform_elevations=(6000.0, 12000.0, 17000.0),
        nozzles=_tower_nozzles(2600.0, 18600.0, feed_dn=300, discharge_dn=300),
        sources={
            "position": Provenance.EXCEL,
            "diameter": Provenance.SIDE_VIEW,
            "height": Provenance.SIDE_VIEW,
            "volume_m3": Provenance.EXCEL,
            "head": Provenance.SIDE_VIEW,
            "bottom": Provenance.SIDE_VIEW,
            "cone_height": Provenance.SIDE_VIEW,
            "support": Provenance.SIDE_VIEW,
            "skirt_height": Provenance.STANDARD,
            "platform_elevations": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "Height and diameter are transposed in the equipment list - corrected "
            "from the side view and confirmed by volume. See the data quality "
            "exception register.",
            "D0 chlorine dioxide stage upflow tower: 61 C, 30 min retention, 10% "
            "consistency. Side view shows a flat roof with top-mounted equipment "
            "and a long conical bottom.",
        ),
    ),
    TankSpec(
        tag="205-TA-011",
        name="D0 FILTRATE TANK",
        area="205 - Bleaching Plant",
        discipline="Tanks & Vessels",
        position=(33067.0, 19057.0, 0.0),
        diameter=4000.0,
        height=5300.0,
        volume_m3=63.0,
        head=HeadType.CONICAL,
        bottom=BottomType.FLAT,
        support=SupportType.GROUND,
        head_height=500.0,
        stiffening_rings=1,
        nozzles=_standard_tank_nozzles(4000.0, 5300.0, feed_dn=300, discharge_dn=350),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.SIDE_VIEW,
            "height": Provenance.SIDE_VIEW,
            "volume_m3": Provenance.EXCEL,
            "head": Provenance.SIDE_VIEW,
            "head_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "Height and diameter are transposed in the equipment list - corrected "
            "from the side view (h=5.3 m, o=4.0 m, V=63 m3, T=64 C).",
        ),
    ),
    TankSpec(
        tag="205-TA-016",
        name="D0 WASHER DROPLEG",
        area="205 - Bleaching Plant",
        discipline="Tanks & Vessels",
        position=(33833.0, 6000.0, 0.0),
        diameter=1050.0,
        height=12000.0,
        head=HeadType.FLAT,
        bottom=BottomType.CONICAL,
        support=SupportType.LEGS,
        skirt_height=500.0,
        cone_height=1200.0,
        cone_outlet_dn=400.0,
        nozzles=_dropleg_nozzles(12000.0),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.STANDARD,
            "head": Provenance.STANDARD,
            "bottom": Provenance.STANDARD,
            "support": Provenance.STANDARD,
            "cone_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height is 'To Be Determined' and no side view is "
            "provided. Modelled at 12000 mm to match 204-TA-021, the equivalent "
            "dropleg, since a barometric leg must exceed roughly 10 m.",
        ),
    ),
    TankSpec(
        tag="205-TA-022",
        name="EOP REACTOR",
        area="205 - Bleaching Plant",
        discipline="Reactors & Towers",
        position=(38469.0, -4401.0, 0.0),
        diameter=2800.0,
        height=22000.0,
        head=HeadType.DISHED,
        bottom=BottomType.CONICAL,
        support=SupportType.SKIRT,
        skirt_height=2500.0,
        cone_height=2400.0,
        cone_outlet_dn=300.0,
        head_height=700.0,
        stiffening_rings=5,
        platform_elevations=(6000.0, 12000.0, 18000.0),
        nozzles=_tower_nozzles(2800.0, 22000.0, feed_dn=300, discharge_dn=300),
        sources={
            "position": Provenance.EXCEL,
            "diameter": Provenance.EXCEL,
            "height": Provenance.VENDOR_TYPICAL,
            "head": Provenance.STANDARD,
            "bottom": Provenance.STANDARD,
            "support": Provenance.STANDARD,
            "skirt_height": Provenance.STANDARD,
            "cone_height": Provenance.STANDARD,
            "head_height": Provenance.STANDARD,
            "platform_elevations": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height and volume are 'To Be Determined'/'(No Reference)' "
            "and no side view is provided. 22000 mm is a Reference Value sized "
            "between the two oxygen reactors (20.3 m at DN2000 and 23.5 m at "
            "DN2600), consistent with a pressurised EOP stage of this bore in "
            "Valmet/ANDRITZ bleach plant practice.",
            "Requires confirmation once vendor data is issued.",
        ),
    ),
    TankSpec(
        tag="205-TA-025",
        name="EOP BLOW TANK",
        area="205 - Bleaching Plant",
        discipline="Tanks & Vessels",
        position=(43067.0, -4501.0, 0.0),
        diameter=3200.0,
        height=13000.0,
        head=HeadType.CONICAL,
        bottom=BottomType.CONICAL,
        support=SupportType.SKIRT,
        skirt_height=1500.0,
        cone_height=2000.0,
        cone_outlet_dn=400.0,
        head_height=900.0,
        stiffening_rings=3,
        nozzles=(
            Nozzle("N1", 400, 11500.0, 90.0, "Blow line inlet from EOP reactor",
                   provenance=Provenance.STANDARD),
            Nozzle("N2", 400, 0.0, 270.0, "Bottom cone outlet to pump",
                   vertical=True, provenance=Provenance.STANDARD),
            Nozzle("N3", 600, 13000.0, 0.0, "Vapour relief", vertical=True,
                   provenance=Provenance.STANDARD),
            Nozzle("N4", 200, 6000.0, 180.0, "Dilution filtrate",
                   provenance=Provenance.STANDARD),
            Nozzle("M1", 600, 2000.0, 135.0, "Manway", provenance=Provenance.STANDARD),
        ),
        sources={
            "position": Provenance.EXCEL,
            "diameter": Provenance.EXCEL,
            "height": Provenance.VENDOR_TYPICAL,
            "head": Provenance.STANDARD,
            "bottom": Provenance.STANDARD,
            "support": Provenance.STANDARD,
            "cone_height": Provenance.STANDARD,
            "skirt_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height is 'To Be Determined' and no side view is "
            "provided. Modelled identically to 204-TA-001, the O2 stage blow tank, "
            "which shares the same DN3200 bore and duty - a defensible Reference "
            "Value pending vendor data.",
        ),
    ),
    TankSpec(
        tag="205-TA-029",
        name="EOP FILTRATE TANK",
        area="205 - Bleaching Plant",
        discipline="Tanks & Vessels",
        position=(39418.0, 19057.0, 0.0),
        diameter=3570.0,
        height=5300.0,
        head=HeadType.CONICAL,
        bottom=BottomType.FLAT,
        support=SupportType.GROUND,
        head_height=450.0,
        stiffening_rings=1,
        nozzles=_standard_tank_nozzles(3570.0, 5300.0, feed_dn=300, discharge_dn=350),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.STANDARD,
            "head": Provenance.STANDARD,
            "head_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height is 'To Be Determined'. 5300 mm is a Reference "
            "Value matching 205-TA-011, the D0 filtrate tank, which serves the "
            "adjacent stage at a comparable bore.",
        ),
    ),
    TankSpec(
        tag="205-TA-036",
        name="EOP WASHER DROPLEG",
        area="205 - Bleaching Plant",
        discipline="Tanks & Vessels",
        position=(41833.0, 6000.0, 0.0),
        diameter=1050.0,
        height=12000.0,
        head=HeadType.FLAT,
        bottom=BottomType.CONICAL,
        support=SupportType.LEGS,
        skirt_height=500.0,
        cone_height=1200.0,
        cone_outlet_dn=400.0,
        nozzles=_dropleg_nozzles(12000.0),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.STANDARD,
            "head": Provenance.STANDARD,
            "bottom": Provenance.STANDARD,
            "support": Provenance.STANDARD,
            "cone_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height is 'To Be Determined' and no side view is "
            "provided. Modelled identically to 205-TA-016, the D0 washer dropleg, "
            "which shares the same DN1050 bore.",
        ),
    ),
    TankSpec(
        tag="205-TA-042",
        name="D1 TOWER",
        area="205 - Bleaching Plant",
        discipline="Reactors & Towers",
        position=(49380.0, -5003.0, 0.0),
        diameter=3650.0,
        height=20000.0,
        head=HeadType.FLAT,
        bottom=BottomType.CONICAL,
        support=SupportType.SKIRT,
        skirt_height=2500.0,
        cone_height=3500.0,
        cone_outlet_dn=350.0,
        stiffening_rings=4,
        platform_elevations=(6000.0, 12000.0, 18000.0),
        nozzles=_tower_nozzles(3650.0, 20000.0, feed_dn=350, discharge_dn=350),
        sources={
            "position": Provenance.EXCEL,
            "diameter": Provenance.EXCEL,
            "height": Provenance.VENDOR_TYPICAL,
            "head": Provenance.STANDARD,
            "bottom": Provenance.STANDARD,
            "support": Provenance.STANDARD,
            "skirt_height": Provenance.STANDARD,
            "cone_height": Provenance.STANDARD,
            "platform_elevations": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height is 'To Be Determined' and no side view is "
            "provided. 20000 mm is a Reference Value - a D1 tower normally holds "
            "retention comparable to the D0 stage (205-TA-008 at 18.6 m) at the "
            "larger DN3650 bore.",
            "Modelled on the D0 tower pattern: flat roof, skirt support, long "
            "conical bottom for upflow discharge.",
        ),
    ),
    TankSpec(
        tag="205-TA-045",
        name="D1 FILTRATE TANK",
        area="205 - Bleaching Plant",
        discipline="Tanks & Vessels",
        position=(47423.0, 19057.0, 0.0),
        diameter=3500.0,
        height=5300.0,
        head=HeadType.CONICAL,
        bottom=BottomType.FLAT,
        support=SupportType.GROUND,
        head_height=450.0,
        stiffening_rings=1,
        nozzles=_standard_tank_nozzles(3500.0, 5300.0, feed_dn=300, discharge_dn=350),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "height": Provenance.STANDARD,
            "head": Provenance.STANDARD,
            "head_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height is 'To Be Determined'. 5300 mm is a Reference "
            "Value consistent with the D0 and EOP filtrate tanks, which form a "
            "matched set across the bleach plant stages.",
        ),
    ),
    TankSpec(
        tag="205-TA-052",
        name="D1 WASHER DROPLEG",
        area="205 - Bleaching Plant",
        discipline="Tanks & Vessels",
        position=(49838.0, 6000.0, 0.0),
        diameter=1050.0,
        height=12000.0,
        head=HeadType.FLAT,
        bottom=BottomType.CONICAL,
        support=SupportType.LEGS,
        skirt_height=500.0,
        cone_height=1200.0,
        cone_outlet_dn=400.0,
        nozzles=_dropleg_nozzles(12000.0),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.CLIENT,
            "height": Provenance.STANDARD,
            "head": Provenance.STANDARD,
            "bottom": Provenance.STANDARD,
            "support": Provenance.STANDARD,
            "cone_height": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "OUTSTANDING: height is 'To Be Determined'; modelled at 12000 mm to "
            "match the other droplegs.",
            "Diameter corrected to 1050 mm on client confirmation (2026-07-24). "
            "The equipment list records 6.2 m, which was queried as implausible "
            "for a barometric leg; the corrected value matches 205-TA-016 and "
            "205-TA-036, the D0 and EOP washer droplegs.",
        ),
    ),
    TankSpec(
        tag="205-TA-056",
        name="BLEACHED PULP STORAGE TOWER",
        area="205 - Bleaching Plant",
        discipline="Reactors & Towers",
        position=(67030.0, 21008.0, 0.0),
        diameter=6470.0,
        height=26400.0,
        head=HeadType.CONICAL,
        bottom=BottomType.DISHED,
        support=SupportType.GROUND,
        head_height=1300.0,
        outer_diameter=9900.0,
        agitator=True,
        agitator_type=AgitatorType.TOP_ENTRY,
        stiffening_rings=6,
        platform_elevations=(8000.0, 16000.0, 24000.0),
        nozzles=(
            Nozzle("N1", 400, 24000.0, 90.0, "Bleached MC pulp feed inlet (top)",
                   provenance=Provenance.STANDARD),
            Nozzle("N2", 500, 500.0, 270.0, "Bottom discharge to machine chest",
                   provenance=Provenance.STANDARD),
            Nozzle("N3", 200, 3000.0, 0.0, "Dilution water",
                   provenance=Provenance.STANDARD),
            Nozzle("N4", 300, 26400.0, 45.0, "Vent", vertical=True,
                   provenance=Provenance.STANDARD),
            Nozzle("M1", 600, 1500.0, 135.0, "Manway", provenance=Provenance.STANDARD),
        ),
        sources={
            "position": Provenance.RECOVERED,
            "diameter": Provenance.EXCEL,
            "outer_diameter": Provenance.EXCEL,
            "height": Provenance.STANDARD,
            "head": Provenance.STANDARD,
            "bottom": Provenance.STANDARD,
            "agitator": Provenance.TOP_VIEW,
            "head_height": Provenance.STANDARD,
            "platform_elevations": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "Equipment list records 'Outside 9.9, inside 6.47' - modelled as a "
            "6470 mm inner shell inside a 9900 mm outer envelope, matching the "
            "concentric circles on the top view.",
            "OUTSTANDING: height is 'To Be Determined'. 26400 mm is a Reference "
            "Value matching 205-TA-001, the unbleached storage tower, which is the "
            "paired vessel at the other end of the bleach line.",
            "Top view shows 205-AG-057 'Bleached pulp storage tower agitator' as "
            "a hub on the tower centreline with radial arms - a top-entry unit, "
            "unlike 205-TA-001 whose scraper drive is under the floor.",
        ),
    ),
    TankSpec(
        tag="205-TA-059",
        name="BLEACH PLANT SCRUBBER",
        area="205 - Bleaching Plant",
        discipline="Feeders & Specialty",
        position=(49515.0, -9553.0, 0.0),
        diameter=1500.0,
        height=14000.0,
        head=HeadType.CONICAL,
        bottom=BottomType.CONICAL,
        support=SupportType.SKIRT,
        skirt_height=2000.0,
        cone_height=1200.0,
        cone_outlet_dn=200.0,
        head_height=400.0,
        outer_diameter=2700.0,
        stiffening_rings=3,
        platform_elevations=(5000.0, 10000.0),
        nozzles=(
            Nozzle("N1", 500, 2500.0, 90.0, "Vent gas inlet from bleach stages",
                   provenance=Provenance.STANDARD),
            Nozzle("N2", 500, 14000.0, 0.0, "Scrubbed gas outlet to stack",
                   vertical=True, provenance=Provenance.STANDARD),
            Nozzle("N3", 150, 12000.0, 180.0, "Caustic scrubbing liquor inlet",
                   provenance=Provenance.STANDARD),
            Nozzle("N4", 200, 0.0, 270.0, "Spent liquor drain from bottom cone",
                   vertical=True, provenance=Provenance.STANDARD),
            Nozzle("M1", 500, 4000.0, 135.0, "Manway - packing access",
                   provenance=Provenance.STANDARD),
        ),
        sources={
            "position": Provenance.EXCEL,
            "diameter": Provenance.EXCEL,
            "outer_diameter": Provenance.EXCEL,
            "height": Provenance.STANDARD,
            "head": Provenance.STANDARD,
            "bottom": Provenance.STANDARD,
            "support": Provenance.STANDARD,
            "skirt_height": Provenance.STANDARD,
            "cone_height": Provenance.STANDARD,
            "head_height": Provenance.STANDARD,
            "platform_elevations": Provenance.STANDARD,
            "nozzles": Provenance.STANDARD,
        },
        notes=(
            "Equipment list records 'Outside 2.7, inside 1.5' - modelled as a "
            "1500 mm inner packed column inside a 2700 mm outer shell.",
            "OUTSTANDING: height is 'To Be Determined'. 14000 mm is a Reference "
            "Value - a packed chlorine dioxide vent scrubber needs roughly 8-10 "
            "diameters of packed height plus disengagement space.",
            "Top view (filed as 2205-TA-050.png) shows a circular vessel with an "
            "external ring of stiffeners or downcomers and a large inclined duct.",
        ),
    ),
)


# ---------------------------------------------------------------------------
# Accessors
# ---------------------------------------------------------------------------

_BY_TAG: Dict[str, TankSpec] = {t.tag: t for t in WSB_TANKS}


def get_tank(tag: str) -> TankSpec:
    """Look up one tank by tag. Raises KeyError if the tag is unknown."""
    try:
        return _BY_TAG[tag]
    except KeyError:
        raise KeyError(
            f"Unknown tank tag {tag!r}. Known tags: {', '.join(sorted(_BY_TAG))}"
        ) from None


def tanks_by_area() -> Dict[str, List[TankSpec]]:
    """Group the register by process area, preserving register order."""
    grouped: Dict[str, List[TankSpec]] = {}
    for tank in WSB_TANKS:
        grouped.setdefault(tank.area, []).append(tank)
    return grouped


def reference_values() -> List[Tuple[str, str, Provenance]]:
    """
    Every assumed value across the register, as (tag, field, provenance).

    Feeds the 'Estimated Parameters' section of the deliverable.
    """
    out: List[Tuple[str, str, Provenance]] = []
    for tank in WSB_TANKS:
        for fname, prov in tank.assumed_fields():
            out.append((tank.tag, fname, prov))
    return out
