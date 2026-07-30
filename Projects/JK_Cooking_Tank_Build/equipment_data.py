"""
JK Cooking Plant — resolved equipment geometry.

Project data precedence:
1. ``DO.txt``
2. ``Tank_list.xlsx`` (Sheet1!A1:H16)
3. PNG reference views under ``Refs/``
4. Project knowledge-base defaults and named external process references

All coordinates are the equipment bottom-centre / foundation datum in the
global E3D frame.  Values not present in the first three sources are carried as
``ReferenceValue`` records and appear in the engineering deliverable.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import List, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from wsb.composite_schema import (  # noqa: E402
    EquipmentModel,
    NativeNozzleSpec,
    ParameterRecord,
    PrimitiveSpec,
    ReferenceValue,
    SourceRecord,
)

__all__ = ["EQUIPMENT", "EQUIPMENT_MODELS", "DATA_QUALITY_EXCEPTIONS"]


PROJECT_AREA = "Cooking Plant"
WORKBOOK_SOURCE = SourceRecord(
    "Equipment register",
    "Tank_list.xlsx, Sheet1!A1:H16",
)
DO_SOURCE = SourceRecord(
    "Project requirements",
    "DO.txt — bottom-centre datum, total-height and profile-string rules",
)
VALMET_COOKING_SOURCE = SourceRecord(
    "Cooking process basis",
    "Valmet cooking systems — kraft cooking and liquor circulation context",
    "https://www.valmet.com/pulp/cooking-and-fiberline/cooking/",
)
VALMET_ACCUMULATOR_SOURCE = SourceRecord(
    "Accumulator process basis",
    "Valmet application report 2611_01_01EN — batch cooking uses liquor "
    "accumulators to balance flows; digester circulation is pressure service",
    "https://www.valmet.com/globalassets/sharepoint/imported/2611_01_01en.pdf",
)
VALMET_JUNK_TRAP_SOURCE = SourceRecord(
    "Junk-trap process basis",
    "Valmet application-specific products — junk traps remove sand and debris "
    "from chip-chute circulation",
    "https://www.valmet.com/flowcontrol/valves/application-specific-products/",
)
VALMET_BLOW_SOURCE = SourceRecord(
    "Blow-tank process basis",
    "Valmet methanol white paper — blow-tank flash vapour is condensed in blow "
    "heat recovery",
    "https://www.valmet.com/globalassets/media/downloads/white-papers/"
    "power-and-recovery/methanol_waste_to_fuel_whitepaper.pdf",
)

_AXIS_UNIT = {
    "E": (1.0, 0.0),
    "W": (-1.0, 0.0),
    "N": (0.0, 1.0),
    "S": (0.0, -1.0),
}
_AXIS_VECTOR = {
    "U": (0.0, 0.0, 1.0),
    "D": (0.0, 0.0, -1.0),
    "E": (1.0, 0.0, 0.0),
    "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0),
    "S": (0.0, -1.0, 0.0),
}
_NOZZLE_WALL_PENETRATION = 80.0


def _point(e: float = 0.0, n: float = 0.0, u: float = 0.0):
    return (float(e), float(n), float(u))


def _radial_plan_rotation(e: float, n: float) -> float:
    """Local X bearing from the equipment centre to a perimeter attachment."""
    if abs(e) < 1e-9 and abs(n) < 1e-9:
        return 0.0
    return math.degrees(math.atan2(n, e)) % 360.0


def _rotate_plan(e: float, n: float, rotation_deg: float) -> Tuple[float, float]:
    """Rotate a local plan offset into the equipment E/N frame."""
    angle = math.radians(rotation_deg)
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return (
        cosine * e - sine * n,
        sine * e + cosine * n,
    )


def _cylindrical_height(diameter_mm: float, capacity_m3: float) -> float:
    """Cylinder height whose geometric volume equals the listed capacity."""
    area_mm2 = math.pi * diameter_mm**2 / 4.0
    return capacity_m3 * 1_000_000_000.0 / area_mm2


def _nozzle_length(dn: int) -> float:
    if dn <= 80:
        return 250.0
    if dn <= 150:
        return 300.0
    if dn <= 300:
        return 350.0
    return 450.0


def _footplate_hardware(
    primitives: List[PrimitiveSpec],
    *,
    group: str,
    centre_e: float,
    centre_n: float,
    plate_size: float,
    plate_thickness: float,
    label: str,
) -> None:
    """Four anchors plus grout and cleats tying a support foot to the ground."""
    rotation_deg = _radial_plan_rotation(centre_e, centre_n)
    primitives.extend(
        (
            PrimitiveSpec.box(
                group,
                plate_size + 80.0,
                plate_size + 80.0,
                12.0,
                _point(centre_e, centre_n, 6.0),
                f"{label} non-shrink grout pad",
                role="support",
                plan_rotation_deg=rotation_deg,
            ),
            PrimitiveSpec.box(
                group,
                plate_size * 0.55,
                35.0,
                150.0,
                _point(centre_e, centre_n, 75.0),
                f"{label} radial base gusset",
                role="support",
                plan_rotation_deg=rotation_deg,
            ),
            PrimitiveSpec.box(
                group,
                35.0,
                plate_size * 0.55,
                150.0,
                _point(centre_e, centre_n, 75.0),
                f"{label} tangential base gusset",
                role="support",
                plan_rotation_deg=rotation_deg,
            ),
        )
    )
    offset = plate_size * 0.34
    for index, (local_e, local_n) in enumerate(
        ((offset, offset), (-offset, offset), (-offset, -offset), (offset, -offset)),
        start=1,
    ):
        de, dn = _rotate_plan(local_e, local_n, rotation_deg)
        location = _point(centre_e + de, centre_n + dn, 0.0)
        primitives.extend(
            (
                PrimitiveSpec.cyli(
                    group,
                    24.0,
                    plate_thickness + 38.0,
                    location,
                    f"{label} anchor stud {index}",
                    role="hardware",
                ),
                PrimitiveSpec.box(
                    group,
                    75.0,
                    75.0,
                    10.0,
                    _point(
                        centre_e + de,
                        centre_n + dn,
                        plate_thickness + 5.0,
                    ),
                    f"{label} anchor clamp washer plate {index}",
                    role="support",
                    plan_rotation_deg=rotation_deg,
                ),
                PrimitiveSpec.cyli(
                    group,
                    48.0,
                    5.0,
                    _point(
                        centre_e + de,
                        centre_n + dn,
                        plate_thickness,
                    ),
                    f"{label} anchor washer {index}",
                    role="hardware",
                ),
                PrimitiveSpec.cyli(
                    group,
                    42.0,
                    18.0,
                    _point(
                        centre_e + de,
                        centre_n + dn,
                        plate_thickness + 5.0,
                    ),
                    f"{label} anchor nut {index}",
                    role="hardware",
                ),
            )
        )


def _leg_top_connection(
    primitives: List[PrimitiveSpec],
    *,
    group: str,
    centre_e: float,
    centre_n: float,
    leg_size: float,
    top_u: float,
    label: str,
) -> None:
    """Load-spreader cap and crossed gusset webs at a leg/vessel junction."""
    rotation_deg = _radial_plan_rotation(centre_e, centre_n)
    primitives.extend(
        (
            PrimitiveSpec.box(
                group,
                leg_size + 180.0,
                leg_size + 180.0,
                40.0,
                _point(centre_e, centre_n, top_u),
                f"{label} top load-spreader plate",
                role="support",
                plan_rotation_deg=rotation_deg,
            ),
            PrimitiveSpec.box(
                group,
                leg_size + 260.0,
                35.0,
                320.0,
                _point(centre_e, centre_n, top_u - 150.0),
                f"{label} radial top gusset web",
                role="support",
                plan_rotation_deg=rotation_deg,
            ),
            PrimitiveSpec.box(
                group,
                35.0,
                leg_size + 260.0,
                320.0,
                _point(centre_e, centre_n, top_u - 150.0),
                f"{label} tangential top gusset web",
                role="support",
                plan_rotation_deg=rotation_deg,
            ),
        )
    )


def _perimeter_anchor_hardware(
    primitives: List[PrimitiveSpec],
    *,
    shell_radius: float,
    count: int,
    label: str,
) -> None:
    """Anchors with a continuous baseplate/clamp load path back to the tank."""
    bolt_radius = shell_radius + 150.0
    for index in range(count):
        angle = 2.0 * math.pi * index / count
        unit_e = math.cos(angle)
        unit_n = math.sin(angle)
        e = unit_e * bolt_radius
        n = unit_n * bolt_radius
        shell_e = unit_e * shell_radius
        shell_n = unit_n * shell_radius
        clamp_e = (e + shell_e) / 2.0
        clamp_n = (n + shell_n) / 2.0
        rotation_deg = math.degrees(angle) % 360.0
        primitives.extend(
            (
                PrimitiveSpec.box(
                    "SUPPORT",
                    180.0,
                    180.0,
                    16.0,
                    _point(e, n, 8.0),
                    f"{label} anchor baseplate {index + 1:02d}",
                    role="support",
                    plan_rotation_deg=rotation_deg,
                ),
                PrimitiveSpec.box(
                    "SUPPORT",
                    bolt_radius - shell_radius + 90.0,
                    90.0,
                    20.0,
                    _point(clamp_e, clamp_n, 26.0),
                    f"{label} anchor clamp plate {index + 1:02d}",
                    role="support",
                    plan_rotation_deg=rotation_deg,
                ),
                PrimitiveSpec.box(
                    "SUPPORT",
                    100.0,
                    100.0,
                    140.0,
                    _point(
                        unit_e * (shell_radius + 35.0),
                        unit_n * (shell_radius + 35.0),
                        70.0,
                    ),
                    f"{label} anchor chair web {index + 1:02d}",
                    role="support",
                    plan_rotation_deg=rotation_deg,
                ),
                PrimitiveSpec.cyli(
                    "SUPPORT",
                    30.0,
                    105.0,
                    _point(e, n, 0.0),
                    f"{label} anchor stud {index + 1:02d}",
                    role="hardware",
                ),
                PrimitiveSpec.cyli(
                    "SUPPORT",
                    60.0,
                    6.0,
                    _point(e, n, 36.0),
                    f"{label} anchor washer {index + 1:02d}",
                    role="hardware",
                ),
                PrimitiveSpec.cyli(
                    "SUPPORT",
                    52.0,
                    24.0,
                    _point(e, n, 42.0),
                    f"{label} anchor nut {index + 1:02d}",
                    role="hardware",
                ),
            )
        )


def _rectangular_support_anchors(
    primitives: List[PrimitiveSpec],
    *,
    centre_e: float,
    centre_n: float,
    half_e: float,
    half_n: float,
    label: str,
) -> None:
    """Four anchor assemblies at the corners of a rectangular support."""
    for index, (de, dn) in enumerate(
        ((half_e, half_n), (-half_e, half_n), (-half_e, -half_n), (half_e, -half_n)),
        start=1,
    ):
        e = centre_e + de
        n = centre_n + dn
        primitives.extend(
            (
                PrimitiveSpec.cyli(
                    "SUPPORT",
                    24.0,
                    70.0,
                    _point(e, n, 0.0),
                    f"{label} anchor stud {index}",
                    role="hardware",
                ),
                PrimitiveSpec.cyli(
                    "SUPPORT",
                    48.0,
                    5.0,
                    _point(e, n, 20.0),
                    f"{label} anchor washer {index}",
                    role="hardware",
                ),
                PrimitiveSpec.cyli(
                    "SUPPORT",
                    42.0,
                    18.0,
                    _point(e, n, 25.0),
                    f"{label} anchor nut {index}",
                    role="hardware",
                ),
            )
        )


def _access_ladder(
    primitives: List[PrimitiveSpec],
    *,
    face_radius: float,
    start_u: float,
    top_u: float,
    bearing: str,
    label: str,
    lower_support_top: float = 0.0,
    lower_support_radius: float | None = None,
) -> None:
    """Bearing-aware fixed ladder with base shoes and connected wall brackets."""
    if top_u - start_u < 700.0:
        return
    bearing = bearing.upper()
    if bearing not in _AXIS_UNIT:
        raise ValueError(f"{label}: unsupported ladder bearing {bearing!r}")
    stand_off = 260.0
    half_width = 260.0
    radial_e, radial_n = _AXIS_UNIT[bearing]
    if bearing in ("E", "W"):
        tangent_e, tangent_n = (0.0, 1.0)
        rung_axis = "N"
    else:
        tangent_e, tangent_n = (1.0, 0.0)
        rung_axis = "E"
    ladder_e = radial_e * (face_radius + stand_off)
    ladder_n = radial_n * (face_radius + stand_off)
    rail_height = top_u - start_u
    rail_points = []
    for side, tangent_offset in (("left", -half_width), ("right", half_width)):
        rail_e = ladder_e + tangent_e * tangent_offset
        rail_n = ladder_n + tangent_n * tangent_offset
        rail_points.append((side, tangent_offset, rail_e, rail_n))
        primitives.extend(
            (
                PrimitiveSpec.box(
                    "ACCESS",
                    120.0,
                    120.0,
                    20.0,
                    _point(rail_e, rail_n, 10.0),
                    f"{label} {bearing} {side} ladder base shoe",
                    role="access",
                ),
                PrimitiveSpec.cyli(
                    "ACCESS",
                    42.0,
                    rail_height,
                    _point(rail_e, rail_n, start_u),
                    f"{label} {bearing} {side} ladder rail",
                    role="access",
                ),
            )
        )

    first_rung_u = start_u + 260.0
    rung_count = max(1, int((top_u - first_rung_u) // 350.0) + 1)
    for index in range(rung_count):
        u = min(top_u, first_rung_u + index * 350.0)
        rung_e = ladder_e - tangent_e * half_width
        rung_n = ladder_n - tangent_n * half_width
        primitives.append(
            PrimitiveSpec.cyli(
                "ACCESS",
                30.0,
                half_width * 2.0,
                _point(rung_e, rung_n, u),
                f"{label} {bearing} ladder rung {index + 1:02d}",
                axis=rung_axis,
                role="access",
            )
        )

    bracket_levels = max(2, int(rail_height // 2000.0) + 1)
    for level in range(bracket_levels):
        u = max(
            start_u + 120.0,
            start_u + rail_height * level / (bracket_levels - 1),
        )
        u = min(u, top_u - 120.0)
        carried_by_lower_frame = (
            lower_support_radius is not None and u <= lower_support_top
        )
        attach_radius = (
            lower_support_radius if carried_by_lower_frame else face_radius
        )
        if carried_by_lower_frame:
            crossbar_e = radial_e * attach_radius - tangent_e * half_width
            crossbar_n = radial_n * attach_radius - tangent_n * half_width
            primitives.append(
                PrimitiveSpec.cyli(
                    "ACCESS",
                    55.0,
                    half_width * 2.0,
                    _point(crossbar_e, crossbar_n, u),
                    f"{label} {bearing} ladder-to-leg crossbar "
                    f"{level + 1:02d}",
                    axis=rung_axis,
                    role="support",
                )
            )
        for side, tangent_offset, _rail_e, _rail_n in rail_points:
            attach_e = radial_e * attach_radius + tangent_e * tangent_offset
            attach_n = radial_n * attach_radius + tangent_n * tangent_offset
            bracket_length = face_radius + stand_off - attach_radius
            primitives.append(
                PrimitiveSpec.cyli(
                    "ACCESS",
                    30.0,
                    bracket_length,
                    _point(attach_e, attach_n, u),
                    f"{label} {bearing} {side} connected ladder bracket "
                    f"{level + 1:02d}",
                    axis=bearing,
                    role="access",
                )
            )


def _vessel_fittings(
    primitives: List[PrimitiveSpec],
    *,
    radius: float,
    shell_bottom: float,
    shell_top: float,
    label: str,
) -> None:
    """Lifting lugs, pin envelopes, nameplate screws and a grounding lug."""
    lug_u = max(shell_bottom + 250.0, shell_top - 380.0)
    for bearing, e, n, xlen, ylen, pin_axis in (
        ("east", radius + 70.0, 0.0, 140.0, 260.0, "N"),
        ("west", -radius - 70.0, 0.0, 140.0, 260.0, "N"),
        ("north", 0.0, radius + 70.0, 260.0, 140.0, "E"),
        ("south", 0.0, -radius - 70.0, 260.0, 140.0, "E"),
    ):
        primitives.extend(
            (
                PrimitiveSpec.box(
                    "DETAIL",
                    xlen,
                    ylen,
                    300.0,
                    _point(e, n, lug_u),
                    f"{label} {bearing} lifting lug plate",
                    role="detail",
                ),
                PrimitiveSpec.cyli(
                    "DETAIL",
                    70.0,
                    180.0,
                    (
                        _point(e, n - 90.0, lug_u)
                        if pin_axis == "N"
                        else _point(e - 90.0, n, lug_u)
                    ),
                    f"{label} {bearing} lifting-lug pin envelope",
                    axis=pin_axis,
                    role="hardware",
                ),
            )
        )

    plate_u = min(shell_top - 250.0, max(shell_bottom + 550.0, shell_bottom + 1200.0))
    primitives.append(
        PrimitiveSpec.box(
            "DETAIL",
            500.0,
            24.0,
            320.0,
            _point(0.0, -radius - 12.0, plate_u),
            f"{label} engraved equipment nameplate",
            role="detail",
        )
    )
    for index, (e, du) in enumerate(
        ((-210.0, -125.0), (210.0, -125.0), (-210.0, 125.0), (210.0, 125.0)),
        start=1,
    ):
        primitives.append(
            PrimitiveSpec.cyli(
                "DETAIL",
                18.0,
                18.0,
                _point(e, -radius - 3.0, plate_u + du),
                f"{label} nameplate screw {index}",
                axis="S",
                role="hardware",
            )
        )

    primitives.extend(
        (
            PrimitiveSpec.box(
                "DETAIL",
                160.0,
                80.0,
                120.0,
                _point(radius + 80.0, 0.0, shell_bottom + 120.0),
                f"{label} grounding lug",
                role="detail",
            ),
            PrimitiveSpec.cyli(
                "DETAIL",
                24.0,
                100.0,
                _point(radius + 80.0, -50.0, shell_bottom + 120.0),
                f"{label} grounding-lug bolt",
                axis="N",
                role="hardware",
            ),
        )
    )


def _blow_tank_agitator(
    primitives: List[PrimitiveSpec],
    *,
    cone_bottom_u: float,
    cone_top_u: float,
    label: str,
) -> None:
    """Ground-mounted bottom-entry drive with a vertical internal agitator."""
    grout_thickness = 12.0
    baseplate_thickness = 60.0
    baseplate_bottom = grout_thickness
    motor_bottom = baseplate_bottom + baseplate_thickness
    motor_height = 650.0
    gearbox_bottom = motor_bottom + motor_height
    gearbox_height = 400.0
    gearbox_top = gearbox_bottom + gearbox_height
    if gearbox_top >= cone_bottom_u:
        raise ValueError(
            f"{label}: ground drive stack reaches U={gearbox_top}, above "
            f"the cone bottom U={cone_bottom_u}"
        )

    shaft_top = cone_top_u + 1000.0
    primitives.extend(
        (
            PrimitiveSpec.box(
                "INTERNALS",
                1320.0,
                1320.0,
                grout_thickness,
                _point(u=grout_thickness / 2.0),
                f"{label} bottom-entry agitator non-shrink grout pad",
                role="support",
            ),
            PrimitiveSpec.box(
                "INTERNALS",
                1200.0,
                1200.0,
                baseplate_thickness,
                _point(u=baseplate_bottom + baseplate_thickness / 2.0),
                f"{label} bottom-entry agitator ground baseplate",
                role="support",
            ),
            PrimitiveSpec.cyli(
                "INTERNALS",
                650.0,
                motor_height,
                _point(u=motor_bottom),
                f"{label} ground-mounted vertical agitator motor",
                role="detail",
            ),
            PrimitiveSpec.box(
                "INTERNALS",
                760.0,
                760.0,
                gearbox_height,
                _point(u=gearbox_bottom + gearbox_height / 2.0),
                f"{label} bottom-entry agitator gearbox",
                role="detail",
            ),
            PrimitiveSpec.cyli(
                "INTERNALS",
                520.0,
                cone_bottom_u - gearbox_top,
                _point(u=gearbox_top),
                f"{label} bottom-entry packing-box and bearing housing",
                role="detail",
            ),
            PrimitiveSpec.cyli(
                "INTERNALS",
                120.0,
                shaft_top - gearbox_top,
                _point(u=gearbox_top),
                f"{label} internal vertical bottom-entry agitator shaft",
                role="internal",
            ),
        )
    )

    cone_height = cone_top_u - cone_bottom_u
    stage_elevations = (
        cone_bottom_u + cone_height * 0.30,
        cone_bottom_u + cone_height * 0.70,
    )
    for stage, elevation in enumerate(stage_elevations, start=1):
        blade_span = 1200.0 if stage == 1 else 1600.0
        primitives.extend(
            (
                PrimitiveSpec.cyli(
                    "INTERNALS",
                    360.0 if stage == 1 else 300.0,
                    240.0,
                    _point(u=elevation - 120.0),
                    f"{label} agitator impeller hub {stage}",
                    role="internal",
                ),
                PrimitiveSpec.box(
                    "INTERNALS",
                    blade_span,
                    90.0,
                    160.0,
                    _point(u=elevation),
                    f"{label} agitator east-west blade pair {stage}",
                    role="internal",
                ),
                PrimitiveSpec.box(
                    "INTERNALS",
                    90.0,
                    blade_span,
                    160.0,
                    _point(u=elevation),
                    f"{label} agitator north-south blade pair {stage}",
                    role="internal",
                ),
            )
        )

    support_height = gearbox_top - motor_bottom
    for index, offset_e in enumerate((-450.0, 450.0), start=1):
        primitives.append(
            PrimitiveSpec.box(
                "INTERNALS",
                100.0,
                180.0,
                support_height,
                _point(
                    e=offset_e,
                    u=motor_bottom + support_height / 2.0,
                ),
                f"{label} ground drive support post {index}",
                role="support",
            )
        )

    anchor_offset = 480.0
    for index, (e, n) in enumerate(
        (
            (anchor_offset, anchor_offset),
            (-anchor_offset, anchor_offset),
            (-anchor_offset, -anchor_offset),
            (anchor_offset, -anchor_offset),
        ),
        start=1,
    ):
        primitives.extend(
            (
                PrimitiveSpec.cyli(
                    "INTERNALS",
                    24.0,
                    100.0,
                    _point(e, n, 0.0),
                    f"{label} agitator ground anchor stud {index}",
                    role="hardware",
                ),
                PrimitiveSpec.cyli(
                    "INTERNALS",
                    48.0,
                    5.0,
                    _point(e, n, baseplate_bottom + baseplate_thickness),
                    f"{label} agitator ground anchor washer {index}",
                    role="hardware",
                ),
                PrimitiveSpec.cyli(
                    "INTERNALS",
                    42.0,
                    18.0,
                    _point(
                        e,
                        n,
                        baseplate_bottom + baseplate_thickness + 5.0,
                    ),
                    f"{label} agitator ground anchor nut {index}",
                    role="hardware",
                ),
            )
        )


def _radial_nozzle(
    native_nozzles: List[NativeNozzleSpec],
    nozzle_groups: List[str],
    *,
    group: str,
    dn: int,
    elevation: float,
    axis: str,
    face_radius: float,
    service: str,
) -> None:
    """One catalogue-backed native NOZZLE with POS at its flange face."""
    unit_e, unit_n = _AXIS_UNIT[axis]
    length = _nozzle_length(dn)
    face_datum_radius = (
        face_radius - _NOZZLE_WALL_PENETRATION + length
    )
    native_nozzles.append(
        NativeNozzleSpec(
            group=group,
            name=group,
            dn=dn,
            height=length,
            face=_point(
                face_datum_radius * unit_e,
                face_datum_radius * unit_n,
                elevation,
            ),
            axis=axis,
            label=f"{group} native NOZZLE placeholder — DN{dn} {service}",
        )
    )
    nozzle_groups.append(group)


def _vertical_nozzle(
    native_nozzles: List[NativeNozzleSpec],
    nozzle_groups: List[str],
    *,
    group: str,
    dn: int,
    plate_u: float,
    max_u: float,
    offset_e: float,
    offset_n: float,
    service: str,
) -> None:
    requested = _nozzle_length(dn)
    length = min(
        requested,
        max_u - plate_u + _NOZZLE_WALL_PENETRATION,
    )
    if length <= 80.0:
        raise ValueError(f"{group}: insufficient height for a roof nozzle")
    face_u = plate_u - _NOZZLE_WALL_PENETRATION + length
    native_nozzles.append(
        NativeNozzleSpec(
            group=group,
            name=group,
            dn=dn,
            height=length,
            face=_point(offset_e, offset_n, face_u),
            axis="U",
            label=f"{group} native NOZZLE placeholder — DN{dn} {service}",
        )
    )
    nozzle_groups.append(group)


def _bottom_nozzle(
    native_nozzles: List[NativeNozzleSpec],
    nozzle_groups: List[str],
    *,
    group: str,
    dn: int,
    service: str,
    face_u: float = 0.0,
) -> None:
    """Downward native placeholder positioned at its flange-face elevation."""
    native_nozzles.append(
        NativeNozzleSpec(
            group=group,
            name=group,
            dn=dn,
            height=_nozzle_length(dn),
            face=_point(u=face_u),
            axis="D",
            label=f"{group} native NOZZLE placeholder — DN{dn} {service}",
        )
    )
    nozzle_groups.append(group)


def _top_view_source(filename: str) -> SourceRecord:
    return SourceRecord(
        "Reference top view",
        f"Refs/{filename} — plan envelope and visible connection bearings",
    )


def _atmospheric_tank(
    *,
    name: str,
    display_name: str,
    position: Tuple[float, float, float],
    diameter: float,
    capacity: float,
    drawing: str,
    services: Sequence[Tuple[str, int, float, str, str]],
    ladder_bearing: str | None,
    extra_notes: Tuple[str, ...] = (),
) -> EquipmentModel:
    """
    Ground-bearing atmospheric tank.

    The cylinder is sized directly from V = pi/4 D^2 H.  The conical roof is
    added above that capacity cylinder, so the listed capacity is not consumed
    by an assumed roof volume.
    """
    shell_height = _cylindrical_height(diameter, capacity)
    roof_rise = diameter * 0.15
    overall = shell_height + roof_rise
    apex_dn = min(300.0, diameter * 0.08)
    primitives: List[PrimitiveSpec] = [
        PrimitiveSpec.cyli(
            "SHELL",
            diameter,
            20.0,
            _point(u=0.0),
            "Flat bottom plate at foundation datum",
            role="body",
        ),
        PrimitiveSpec.cyli(
            "SHELL",
            diameter,
            shell_height,
            _point(u=0.0),
            "Capacity cylinder",
            role="body",
        ),
        PrimitiveSpec.cone(
            "SHELL",
            diameter,
            apex_dn,
            roof_rise,
            _point(u=shell_height),
            "Conical atmospheric roof",
            role="body",
        ),
        PrimitiveSpec.cyli(
            "SHELL",
            apex_dn + 100.0,
            40.0,
            _point(u=overall - 40.0),
            "Roof apex cap within total-height envelope",
        ),
    ]
    native_nozzles: List[NativeNozzleSpec] = []
    nozzle_groups: List[str] = []
    schedule = []
    for group, dn, fraction, axis, service in services:
        elevation = max(dn / 2.0 + 80.0, shell_height * fraction)
        elevation = min(elevation, shell_height - dn / 2.0 - 80.0)
        _radial_nozzle(
            native_nozzles,
            nozzle_groups,
            group=group,
            dn=dn,
            elevation=elevation,
            axis=axis,
            face_radius=diameter / 2.0,
            service=service,
        )
        schedule.append(f"{group} DN{dn} {service}")

    vent_offset = diameter * 0.20
    vent_plate = shell_height + roof_rise * 0.60
    _vertical_nozzle(
        native_nozzles,
        nozzle_groups,
        group="N4",
        dn=150,
        plate_u=vent_plate,
        max_u=overall,
        offset_e=vent_offset,
        offset_n=0.0,
        service="high-point vent",
    )
    schedule.append("N4 DN150 high-point vent")

    manway_elevation = min(shell_height - 400.0, max(1200.0, shell_height * 0.25))
    _radial_nozzle(
        native_nozzles,
        nozzle_groups,
        group="M1",
        dn=600,
        elevation=manway_elevation,
        axis="S",
        face_radius=diameter / 2.0,
        service="shell access manway",
    )
    schedule.append("M1 DN600 shell access manway")

    _perimeter_anchor_hardware(
        primitives,
        shell_radius=diameter / 2.0,
        count=12,
        label=display_name,
    )
    if ladder_bearing is not None:
        _access_ladder(
            primitives,
            face_radius=diameter / 2.0,
            start_u=20.0,
            top_u=shell_height,
            bearing=ladder_bearing,
            label=display_name,
        )
    _vessel_fittings(
        primitives,
        radius=diameter / 2.0,
        shell_bottom=0.0,
        shell_top=shell_height,
        label=display_name,
    )

    return EquipmentModel(
        name=name,
        display_name=display_name,
        area=PROJECT_AREA,
        position=position,
        overall_height=overall,
        main_dimensions=(
            f"OD {diameter:.0f} mm; capacity cylinder {shell_height:.1f} mm; "
            f"roof rise {roof_rise:.1f} mm"
        ),
        capacity_m3=capacity,
        primitives=tuple(primitives),
        body_envelope=(
            -diameter / 2.0,
            diameter / 2.0,
            -diameter / 2.0,
            diameter / 2.0,
            0.0,
            overall,
        ),
        nozzle_groups=tuple(nozzle_groups),
        native_nozzles=tuple(native_nozzles),
        parameters=(
            ParameterRecord("Diameter", f"{diameter:.0f} mm", "Tank_list.xlsx"),
            ParameterRecord("Capacity", f"{capacity:g} m3", "Tank_list.xlsx"),
            ParameterRecord(
                "Capacity-cylinder height",
                f"{shell_height:.1f} mm",
                "Derived: V / (pi D^2 / 4)",
            ),
            ParameterRecord(
                "Overall height",
                f"{overall:.1f} mm",
                "Derived cylinder height + Reference Value roof rise",
            ),
        ),
        reference_values=(
            ReferenceValue(
                "Roof rise",
                f"{roof_rise:.1f} mm (0.15 D)",
                "skill/equipment/tanks-and-vessels.md, conical-roof default",
            ),
            ReferenceValue(
                "Nozzle/manway schedule",
                "; ".join(schedule),
                "Minimum process-logical atmospheric-tank connections; "
                "bearings reconciled with the supplied top view",
            ),
            ReferenceValue(
                "Detailed hardware",
                "12 connected anchor chairs; "
                + (
                    f"{ladder_bearing} fixed ladder with base shoes at 350 mm "
                    "rung pitch; "
                    if ladder_bearing is not None
                    else "no dedicated ladder on this grade-accessible vessel; "
                )
                + "four "
                "lifting lugs; nameplate, grounding lug; individual flange "
                "geometry supplied by native NOZZLE placeholders",
                "User-directed visual-detail pass, 2026-07-30; dimensions are "
                "replaceable reference geometry pending vendor GA",
            ),
        ),
        sources=(DO_SOURCE, WORKBOOK_SOURCE, _top_view_source(drawing)),
        notes=(
            "The listed capacity is matched by the cylindrical section alone; "
            "the roof is additional geometric free volume.",
            "Access and fastener details are isolated from the authoritative "
            "body envelope and can be replaced without changing tank data.",
        )
        + extra_notes,
        outstanding=(
            "Confirm vendor GA overall height and nozzle elevations/sizes.",
            "Confirm the placeholder native NOZZLE sizes and the receiving "
            "catalogue family against the final vendor nozzle schedule.",
        ),
    )


def _pressure_accumulator(
    *,
    name: str,
    display_name: str,
    position: Tuple[float, float, float],
    diameter: float,
    capacity: float | None,
    drawing: str,
    shell_height: float | None = None,
    skirt_height: float,
    ladder_bearing: str | None,
) -> EquipmentModel:
    if shell_height is None:
        if capacity is None:
            raise ValueError("Accumulator needs capacity or a resolved shell height")
        shell_height = _cylindrical_height(diameter, capacity)
    head_rise = diameter / 4.0
    bottom_rise = min(head_rise, skirt_height)
    shell_base = skirt_height
    shell_top = shell_base + shell_height
    overall = shell_top + head_rise
    primitives: List[PrimitiveSpec] = [
        PrimitiveSpec.cyli(
            "SUPPORT",
            diameter,
            skirt_height,
            _point(u=0.0),
            "Full-height skirt envelope",
            role="body",
        ),
        PrimitiveSpec.cyli(
            "SUPPORT",
            diameter,
            30.0,
            _point(u=0.0),
            "Skirt bearing plate at bottom datum",
            role="body",
        ),
        PrimitiveSpec.dish(
            "SHELL",
            diameter,
            bottom_rise,
            _point(u=shell_base),
            "Dished bottom inside skirt clearance",
            axis="D",
            role="body",
        ),
        PrimitiveSpec.cyli(
            "SHELL",
            diameter,
            shell_height,
            _point(u=shell_base),
            "Accumulator cylindrical shell",
            role="body",
        ),
        PrimitiveSpec.dish(
            "SHELL",
            diameter,
            head_rise,
            _point(u=shell_top),
            "2:1 elliptical top-head envelope",
            role="body",
        ),
    ]
    native_nozzles: List[NativeNozzleSpec] = []
    nozzle_groups: List[str] = []
    nozzle_specs = (
        ("N1", 400 if diameter > 3000 else 250, 0.22, "E", "liquor inlet"),
        ("N2", 400 if diameter > 3000 else 250, 0.18, "W", "liquor outlet"),
        ("N3", 250 if diameter > 3000 else 150, 0.78, "N", "circulation return"),
        ("N4", 150, 0.55, "S", "instrument / equalizing connection"),
    )
    schedule = []
    for group, dn, fraction, axis, service in nozzle_specs:
        elevation = shell_base + shell_height * fraction
        _radial_nozzle(
            native_nozzles,
            nozzle_groups,
            group=group,
            dn=dn,
            elevation=elevation,
            axis=axis,
            face_radius=diameter / 2.0,
            service=service,
        )
        schedule.append(f"{group} DN{dn} {service}")
    _vertical_nozzle(
        native_nozzles,
        nozzle_groups,
        group="N5",
        dn=150,
        plate_u=shell_top + head_rise * 0.60,
        max_u=overall,
        offset_e=diameter * 0.18,
        offset_n=0.0,
        service="top vent / relief connection",
    )
    schedule.append("N5 DN150 top vent / relief")
    manway_dn = 600 if diameter > 3000 else 500
    _radial_nozzle(
        native_nozzles,
        nozzle_groups,
        group="M1",
        dn=manway_dn,
        elevation=shell_base + min(1200.0, shell_height * 0.35),
        axis="S",
        face_radius=diameter / 2.0,
        service="shell manway",
    )
    schedule.append(f"M1 DN{manway_dn} shell manway")

    _perimeter_anchor_hardware(
        primitives,
        shell_radius=diameter / 2.0,
        count=16 if diameter > 3000.0 else 8,
        label=display_name,
    )
    if ladder_bearing is not None:
        _access_ladder(
            primitives,
            face_radius=diameter / 2.0,
            start_u=20.0,
            top_u=shell_top,
            bearing=ladder_bearing,
            label=display_name,
        )
    _vessel_fittings(
        primitives,
        radius=diameter / 2.0,
        shell_bottom=shell_base,
        shell_top=shell_top,
        label=display_name,
    )

    parameters = [
        ParameterRecord("Diameter", f"{diameter:.0f} mm", "Tank_list.xlsx"),
        ParameterRecord(
            "Shell height",
            f"{shell_height:.1f} mm",
            (
                "Derived: V / (pi D^2 / 4)"
                if capacity is not None
                else "Reference Value from equipment aspect ratio"
            ),
        ),
        ParameterRecord(
            "Overall height",
            f"{overall:.1f} mm",
            "Skirt + shell + top head",
        ),
    ]
    if capacity is not None:
        parameters.insert(
            1,
            ParameterRecord("Capacity", f"{capacity:g} m3", "Tank_list.xlsx"),
        )

    reference_values = [
        ReferenceValue(
            "Pressure-vessel configuration",
            f"{skirt_height:.0f} mm skirt; dished top/bottom; head rise D/4",
            "Batch-cooking liquor accumulator duty and "
            "skill/equipment/tanks-and-vessels.md pressure-vessel guidance",
        ),
        ReferenceValue(
            "Nozzle/manway schedule",
            "; ".join(schedule),
            "Minimum process-logical accumulator connections; plan bearings "
            "follow the visible top-view connections",
        ),
        ReferenceValue(
            "Detailed pressure-vessel hardware",
            (
                "16 skirt anchors" if diameter > 3000.0 else "8 skirt anchors"
            )
            + " with connected clamp plates; "
            + (
                f"{ladder_bearing} fixed ladder with base shoes at 350 mm "
                "rung pitch; "
                if ladder_bearing is not None
                else "no dedicated ladder on the auxiliary vessel; "
            )
            + "four lifting lugs; "
            "nameplate, grounding lug; native NOZZLE placeholders",
            "User-directed visual-detail pass, 2026-07-30; replaceable "
            "reference geometry pending vendor GA",
        ),
    ]
    if capacity is None:
        reference_values.append(
            ReferenceValue(
                "Cylindrical shell height",
                f"{shell_height:.1f} mm",
                "No capacity or side view supplied; approximately 2D for the "
                "small auxiliary accumulator vessel",
            )
        )

    return EquipmentModel(
        name=name,
        display_name=display_name,
        area=PROJECT_AREA,
        position=position,
        overall_height=overall,
        main_dimensions=(
            f"OD {diameter:.0f} mm; shell {shell_height:.1f} mm; "
            f"skirt {skirt_height:.0f} mm"
        ),
        capacity_m3=capacity,
        primitives=tuple(primitives),
        body_envelope=(
            -diameter / 2.0,
            diameter / 2.0,
            -diameter / 2.0,
            diameter / 2.0,
            0.0,
            overall,
        ),
        nozzle_groups=tuple(nozzle_groups),
        native_nozzles=tuple(native_nozzles),
        parameters=tuple(parameters),
        reference_values=tuple(reference_values),
        sources=(
            DO_SOURCE,
            WORKBOOK_SOURCE,
            _top_view_source(drawing),
            VALMET_ACCUMULATOR_SOURCE,
        ),
        notes=(
            "The outer platform/ring visible in plan is not modelled because no "
            "side elevation or steel dimensions were supplied.",
            "Top and bottom DISH elements use their rim/tangent-plane POS; the "
            "top head is numerically seated on the shell without changing the "
            "supplied diameter, capacity or derived height.",
        ),
        outstanding=(
            "Confirm pressure rating, head profile, support height and complete "
            "vendor nozzle schedule.",
            "Confirm whether the plan-view outer ring is a platform, stiffener "
            "or insulation envelope before adding it.",
        ),
    )


def _junk_trap(
    *,
    name: str,
    display_name: str,
    position: Tuple[float, float, float],
    drawing: str,
) -> EquipmentModel:
    diameter = 1770.0
    clearance = 150.0
    cone_height = 550.0
    shell_base = clearance + cone_height
    shell_height = 1800.0
    shell_top = shell_base + shell_height
    head_rise = diameter / 4.0
    overall = shell_top + head_rise
    primitives: List[PrimitiveSpec] = []

    leg_radius = diameter * 0.35
    for index, (de, dn) in enumerate(
        (
            (leg_radius, leg_radius),
            (-leg_radius, leg_radius),
            (-leg_radius, -leg_radius),
            (leg_radius, -leg_radius),
        ),
        start=1,
    ):
        primitives.extend(
            (
                PrimitiveSpec.box(
                    "SUPPORT",
                    180.0,
                    180.0,
                    shell_base,
                    _point(de, dn, shell_base / 2.0),
                    f"Support leg {index}",
                    role="support",
                ),
                PrimitiveSpec.box(
                    "SUPPORT",
                    300.0,
                    300.0,
                    25.0,
                    _point(de, dn, 12.5),
                    f"Support leg {index} foot plate",
                    role="support",
                ),
            )
        )
        _footplate_hardware(
            primitives,
            group="SUPPORT",
            centre_e=de,
            centre_n=dn,
            plate_size=300.0,
            plate_thickness=25.0,
            label=f"Junk-trap support leg {index}",
        )
        _leg_top_connection(
            primitives,
            group="SUPPORT",
            centre_e=de,
            centre_n=dn,
            leg_size=180.0,
            top_u=shell_base,
            label=f"Junk-trap support leg {index}",
        )

    primitives.extend(
        (
            PrimitiveSpec.cone(
                "SHELL",
                300.0,
                diameter,
                cone_height,
                _point(u=clearance),
                "Heavy-reject conical hopper",
                role="body",
            ),
            PrimitiveSpec.cyli(
                "SHELL",
                diameter,
                shell_height,
                _point(u=shell_base),
                "Junk-trap pressure shell",
                role="body",
            ),
            PrimitiveSpec.dish(
                "SHELL",
                diameter,
                head_rise,
                _point(u=shell_top),
                "Dished top closure",
                role="body",
            ),
        )
    )

    native_nozzles: List[NativeNozzleSpec] = []
    nozzle_groups: List[str] = []
    schedule = []
    for group, dn, elevation, axis, service in (
        ("N1", 300, 1100.0, "E", "chip-circulation inlet"),
        ("N2", 300, 1500.0, "W", "circulation outlet"),
        ("N3", 200, 1950.0, "N", "flush-water connection"),
        ("N4", 200, 2250.0, "S", "equalizing / vent connection"),
    ):
        _radial_nozzle(
            native_nozzles,
            nozzle_groups,
            group=group,
            dn=dn,
            elevation=elevation,
            axis=axis,
            face_radius=diameter / 2.0,
            service=service,
        )
        schedule.append(f"{group} DN{dn} {service}")

    _bottom_nozzle(
        native_nozzles,
        nozzle_groups,
        group="N5",
        dn=300,
        service="bottom heavy-reject discharge",
    )
    schedule.append("N5 DN300 bottom heavy-reject discharge")

    _vessel_fittings(
        primitives,
        radius=diameter / 2.0,
        shell_bottom=shell_base,
        shell_top=shell_top,
        label=display_name,
    )

    return EquipmentModel(
        name=name,
        display_name=display_name,
        area=PROJECT_AREA,
        position=position,
        overall_height=overall,
        main_dimensions=(
            f"OD {diameter:.0f} mm; shell {shell_height:.0f} mm; "
            f"hopper {cone_height:.0f} mm"
        ),
        primitives=tuple(primitives),
        body_envelope=(
            -diameter / 2.0,
            diameter / 2.0,
            -diameter / 2.0,
            diameter / 2.0,
            clearance,
            overall,
        ),
        nozzle_groups=tuple(nozzle_groups),
        native_nozzles=tuple(native_nozzles),
        parameters=(
            ParameterRecord("Diameter", "1770 mm", "Tank_list.xlsx"),
            ParameterRecord(
                "Overall height",
                f"{overall:.1f} mm",
                "Reference configuration: hopper + shell + dished head",
            ),
        ),
        reference_values=(
            ReferenceValue(
                "Vessel height/configuration",
                f"{clearance:.0f} mm outlet clearance + {cone_height:.0f} mm "
                f"hopper + {shell_height:.0f} mm shell + {head_rise:.1f} mm head",
                "Junk-trap heavy-debris duty; no side view or capacity supplied",
            ),
            ReferenceValue(
                "Nozzle schedule",
                "; ".join(schedule),
                "Five visible plan connections reconciled with junk-trap "
                "circulation, flushing and reject-removal duties",
            ),
            ReferenceValue(
                "Detailed hardware",
                f"Four anchors, grout/cleats and top gussets per support foot; "
                "no dedicated ladder on this low vessel; lifting lugs; "
                "nameplate, grounding lug; native NOZZLE placeholders",
                "User-directed visual-detail pass, 2026-07-30; replaceable "
                "reference geometry pending vendor GA",
            ),
        ),
        sources=(
            DO_SOURCE,
            WORKBOOK_SOURCE,
            _top_view_source(drawing),
            VALMET_JUNK_TRAP_SOURCE,
        ),
        notes=(
            "Diagonal plan connections are represented on the nearest verified "
            "cardinal E3D axis; exact skew bearings require a vendor GA or a "
            "verified arbitrary-vector PML orientation form.",
        ),
        outstanding=(
            "Confirm vessel height, design pressure and exact nozzle bearings.",
        ),
    )


def _blow_tank(
    *,
    name: str,
    display_name: str,
    position: Tuple[float, float, float],
    drawing_top: str,
    ladder_bearing: str,
) -> EquipmentModel:
    # User-corrected TOP-to-BOTTOM string (2026-07-30), overriding the
    # erroneous final-cone height in Tank_list.xlsx:
    # CY D3876 H2508
    # CONE DT3876 DB7300 H2944
    # CY D7300 H8753
    # CONE DT7300 DB555 H5898
    cone_bottom_clearance = 1848.0
    top_to_bottom = (
        ("CYLI", 3876.0, 3876.0, 2508.0, "Top cylindrical section"),
        ("CONE", 7300.0, 3876.0, 2944.0, "Upper transition"),
        ("CYLI", 7300.0, 7300.0, 8753.0, "Main blow-tank shell"),
        ("CONE", 555.0, 7300.0, 5898.0, "Bottom discharge cone"),
    )
    profile_height = sum(section[3] for section in top_to_bottom)
    overall = cone_bottom_clearance + profile_height
    primitives: List[PrimitiveSpec] = []
    cursor_top = overall
    for kind, d_bottom, d_top, height, label in top_to_bottom:
        bottom = cursor_top - height
        if kind == "CYLI":
            primitives.append(
                PrimitiveSpec.cyli(
                    "SHELL",
                    d_bottom,
                    height,
                    _point(u=bottom),
                    label,
                    role="body",
                )
            )
        else:
            primitives.append(
                PrimitiveSpec.cone(
                    "SHELL",
                    d_bottom,
                    d_top,
                    height,
                    _point(u=bottom),
                    label,
                    role="body",
                )
            )
        cursor_top = bottom
    if abs(cursor_top - cone_bottom_clearance) > 1e-9:
        raise ValueError(
            f"{display_name}: profile bottom {cursor_top} does not land at "
            f"the user-supplied {cone_bottom_clearance} mm clearance"
        )

    # Four legs rise from grade to the DN7300 cone/shell junction, carrying the
    # complete elevated body while the cone outlet remains 1848 mm above grade.
    cone_top_u = cone_bottom_clearance + 5898.0
    main_shell_top_u = cone_top_u + 8753.0
    leg_height = cone_top_u
    leg_radius = 3500.0
    for index, (de, dn) in enumerate(
        (
            (leg_radius, 0.0),
            (-leg_radius, 0.0),
            (0.0, leg_radius),
            (0.0, -leg_radius),
        ),
        start=1,
    ):
        primitives.extend(
            (
                PrimitiveSpec.box(
                    "SUPPORT",
                    250.0,
                    250.0,
                    leg_height,
                    _point(de, dn, leg_height / 2.0),
                    f"Blow-tank support leg {index}",
                    role="support",
                ),
                PrimitiveSpec.box(
                    "SUPPORT",
                    300.0,
                    300.0,
                    30.0,
                    _point(de, dn, 15.0),
                    f"Blow-tank support leg {index} foot plate",
                    role="support",
                ),
            )
        )
        _footplate_hardware(
            primitives,
            group="SUPPORT",
            centre_e=de,
            centre_n=dn,
            plate_size=300.0,
            plate_thickness=30.0,
            label=f"Blow-tank support leg {index}",
        )
        _leg_top_connection(
            primitives,
            group="SUPPORT",
            centre_e=de,
            centre_n=dn,
            leg_size=250.0,
            top_u=leg_height,
            label=f"Blow-tank support leg {index}",
        )
    primitives.append(
        PrimitiveSpec.cyli(
            "SHELL",
            3876.0,
            25.0,
            _point(u=overall - 25.0),
            "Top cover plate within authoritative overall height",
        )
    )

    native_nozzles: List[NativeNozzleSpec] = []
    nozzle_groups: List[str] = []
    schedule = []
    elevation_shift = cone_bottom_clearance + 5898.0 - 2636.0
    for group, dn, old_elevation, axis, face, service in (
        ("N1", 400, 15500.0, "E", 1938.0, "upper tangential blow-line inlet"),
        ("N2", 400, 15000.0, "W", 1938.0, "upper circulation connection"),
        ("N3", 600, 10000.0, "N", 3650.0, "large vapour / stock connection"),
        ("N4", 300, 5200.0, "S", 3650.0, "dilution / recirculation connection"),
        ("M1", 600, 4200.0, "E", 3650.0, "shell access manway"),
    ):
        _radial_nozzle(
            native_nozzles,
            nozzle_groups,
            group=group,
            dn=dn,
            elevation=old_elevation + elevation_shift,
            axis=axis,
            face_radius=face,
            service=service,
        )
        schedule.append(f"{group} DN{dn} {service}")

    _bottom_nozzle(
        native_nozzles,
        nozzle_groups,
        group="N5",
        dn=500,
        service=(
            "placeholder at the authoritative 555 mm bottom opening and "
            "bottom-entry agitator mounting"
        ),
        face_u=cone_bottom_clearance,
    )
    schedule.append(
        "N5 DN500 native placeholder at the 555 mm bottom opening / "
        "agitator mounting"
    )

    _access_ladder(
        primitives,
        face_radius=3650.0,
        start_u=20.0,
        top_u=main_shell_top_u,
        bearing=ladder_bearing,
        label=display_name,
        lower_support_top=leg_height,
        lower_support_radius=leg_radius + 125.0,
    )
    _blow_tank_agitator(
        primitives,
        cone_bottom_u=cone_bottom_clearance,
        cone_top_u=cone_top_u,
        label=display_name,
    )
    _vessel_fittings(
        primitives,
        radius=3650.0,
        shell_bottom=cone_top_u,
        shell_top=main_shell_top_u,
        label=display_name,
    )

    gross_volume = (
        math.pi * 3.876**2 / 4.0 * 2.508
        + math.pi
        * 2.944
        * (3.876**2 + 3.876 * 7.3 + 7.3**2)
        / 12.0
        + math.pi * 7.3**2 / 4.0 * 8.753
        + math.pi
        * 5.898
        * (7.3**2 + 7.3 * 0.555 + 0.555**2)
        / 12.0
    )

    return EquipmentModel(
        name=name,
        display_name=display_name,
        area=PROJECT_AREA,
        position=position,
        overall_height=overall,
        main_dimensions=(
            "TOP→BOTTOM: CY D3876 H2508; CONE 3876→7300 H2944; "
            "CY D7300 H8753; CONE 7300→555 H5898; "
            "bottom opening 1848 above grade"
        ),
        capacity_m3=380.0,
        primitives=tuple(primitives),
        body_envelope=(
            -3650.0,
            3650.0,
            -3650.0,
            3650.0,
            cone_bottom_clearance,
            overall,
        ),
        nozzle_groups=tuple(nozzle_groups),
        native_nozzles=tuple(native_nozzles),
        parameters=(
            ParameterRecord(
                "User-corrected profile",
                "CY 3876×2508; CONE 3876→7300×2944; "
                "CY 7300×8753; CONE 7300→555×5898",
                "User correction 2026-07-30; final-cone H2636 in "
                "Tank_list.xlsx was erroneous",
            ),
            ParameterRecord(
                "Profile and installed height",
                f"{profile_height:.0f} mm body; {cone_bottom_clearance:.0f} mm "
                f"bottom clearance; {overall:.0f} mm grade-to-top",
                "User-corrected segment and clearance chain",
            ),
            ParameterRecord(
                "Global top elevation",
                f"U {position[2] + overall:.0f} mm",
                f"Installation ground U {position[2]:.0f} + "
                f"{overall:.0f} mm grade-to-top",
            ),
            ParameterRecord(
                "Support height",
                f"{leg_height:.0f} mm",
                "Derived from ground to the DN7300 cone/shell junction",
            ),
            ParameterRecord(
                "Overall height",
                f"{overall:.0f} mm",
                "1848 mm bottom clearance plus 20103 mm corrected profile",
            ),
            ParameterRecord("Listed capacity", "380 m3", "Tank_list.xlsx"),
            ParameterRecord(
                "Profile gross volume",
                f"{gross_volume:.1f} m3",
                "Derived from cylinder/frustum volumes",
            ),
        ),
        reference_values=(
            ReferenceValue(
                "Support legs",
                f"4 × 250 mm square, {leg_height:.0f} mm high",
                "User-corrected side-view arrangement: legs extend from grade "
                "to the cone/shell junction; section size remains replaceable",
            ),
            ReferenceValue(
                "Nozzle schedule",
                "; ".join(schedule),
                "Visible top/side connections plus minimum blow-tank process "
                "connections; sizes/elevations pending vendor GA",
            ),
            ReferenceValue(
                "Detailed hardware",
                "Four anchors, grout/cleats and top gussets per support foot; "
                f"{ladder_bearing} ladder stops at the supported DN7300 shell "
                "top and has base shoes; lifting lugs, nameplate and grounding "
                "lug; native NOZZLE placeholders",
                "User-directed visual-detail pass, 2026-07-30; all additions "
                "are outside the authoritative four-segment body profile",
            ),
            ReferenceValue(
                "Internal agitator",
                "Ground-mounted central drive; vertical shaft enters through "
                "the 1848 mm-high cone bottom; two four-blade stages, packing/"
                "bearing housing, gearbox, motor, grout/baseplate and anchors",
                "User-corrected 2026-07-30 from the supplied side view; detail "
                "dimensions remain Reference Values pending vendor GA",
            ),
        ),
        sources=(
            DO_SOURCE,
            WORKBOOK_SOURCE,
            _top_view_source(drawing_top),
            SourceRecord(
                "Reference side view",
                "Refs/BLOW TANK-1-2(SIDE).png — legs and composite arrangement",
            ),
            VALMET_BLOW_SOURCE,
        ),
        notes=(
            f"Profile gross volume is {gross_volume:.1f} m3 versus the listed "
            f"380 m3 capacity ({380.0 / gross_volume * 100.0:.1f}% of the "
            "gross profile).",
            "The top-to-bottom sequence is preserved exactly; PML positions are "
            "computed from the 1848 mm cone-bottom clearance without changing "
            "the other three supplied segment dimensions.",
            f"The corrected exact chain gives {overall:.0f} mm grade-to-top "
            f"and global U={position[2] + overall:.0f}, consistent with the "
            "user's approximate 21 m overall-height direction.",
        ),
        outstanding=(
            "Confirm support-leg section, bottom agitator mounting detail and "
            "all nozzle dimensions against the vendor GA.",
        ),
    )


def _horizontal_condensate_tank() -> EquipmentModel:
    name = "MAIN_CONDENSATE_TANK"
    display_name = "MAIN CONDENSATE TANK"
    position = (28497.0, 27796.0, -300.0)
    overall_length = 3400.0
    diameter = 2017.0
    head_rise = diameter / 4.0
    straight_length = overall_length - 2.0 * head_rise
    saddle_height = 500.0
    centre_u = saddle_height + diameter / 2.0
    body_top = saddle_height + diameter
    primitives: List[PrimitiveSpec] = [
        PrimitiveSpec.cyli(
            "SHELL",
            diameter,
            straight_length,
            _point(n=-straight_length / 2.0, u=centre_u),
            "Horizontal condensate receiver shell",
            axis="N",
            role="body",
        ),
        PrimitiveSpec.dish(
            "SHELL",
            diameter,
            head_rise,
            _point(n=straight_length / 2.0, u=centre_u),
            "North 2:1 elliptical head envelope",
            axis="N",
            role="body",
        ),
        PrimitiveSpec.dish(
            "SHELL",
            diameter,
            head_rise,
            _point(n=-straight_length / 2.0, u=centre_u),
            "South 2:1 elliptical head envelope",
            axis="S",
            role="body",
        ),
    ]
    for index, offset_n in enumerate((-650.0, 650.0), start=1):
        primitives.extend(
            (
                PrimitiveSpec.box(
                    "SUPPORT",
                    1700.0,
                    400.0,
                    saddle_height,
                    _point(n=offset_n, u=saddle_height / 2.0),
                    f"Saddle support {index}",
                    role="support",
                ),
                PrimitiveSpec.box(
                    "SUPPORT",
                    1800.0,
                    500.0,
                    40.0,
                    _point(n=offset_n, u=saddle_height),
                    f"Saddle support {index} vessel wear/load-spreader plate",
                    role="support",
                ),
                PrimitiveSpec.box(
                    "SUPPORT",
                    1800.0,
                    500.0,
                    20.0,
                    _point(n=offset_n, u=10.0),
                    f"Saddle support {index} sole plate and grout interface",
                    role="support",
                ),
            )
        )
        _rectangular_support_anchors(
            primitives,
            centre_e=0.0,
            centre_n=offset_n,
            half_e=700.0,
            half_n=150.0,
            label=f"Condensate saddle {index}",
        )

    native_nozzles: List[NativeNozzleSpec] = []
    nozzle_groups: List[str] = []
    schedule = []
    for group, dn, axis, face, elevation, service in (
        ("N1", 200, "N", overall_length / 2.0, centre_u, "condensate inlet"),
        ("N2", 200, "S", overall_length / 2.0, centre_u, "condensate outlet"),
        ("N3", 150, "E", diameter / 2.0, centre_u, "level / overflow connection"),
        ("M1", 500, "W", diameter / 2.0, centre_u, "inspection manway"),
    ):
        _radial_nozzle(
            native_nozzles,
            nozzle_groups,
            group=group,
            dn=dn,
            elevation=elevation,
            axis=axis,
            face_radius=face,
            service=service,
        )
        schedule.append(f"{group} DN{dn} {service}")

    overall_height = body_top + 200.0
    _vertical_nozzle(
        native_nozzles,
        nozzle_groups,
        group="N4",
        dn=150,
        plate_u=body_top,
        max_u=overall_height,
        offset_e=0.0,
        offset_n=0.0,
        service="high-point vent",
    )
    schedule.append("N4 DN150 high-point vent")

    # Two top lifting pads, a side nameplate with four screws, and a low-point
    # grounding lug.  All remain below the declared vent-controlled height.
    for index, offset_n in enumerate((-650.0, 650.0), start=1):
        primitives.extend(
            (
                PrimitiveSpec.box(
                    "DETAIL",
                    260.0,
                    140.0,
                    120.0,
                    _point(0.0, offset_n, body_top + 60.0),
                    f"Condensate receiver lifting pad {index}",
                    role="detail",
                ),
                PrimitiveSpec.cyli(
                    "DETAIL",
                    60.0,
                    180.0,
                    _point(-90.0, offset_n, body_top + 60.0),
                    f"Condensate receiver lifting-pin envelope {index}",
                    axis="E",
                    role="hardware",
                ),
            )
        )
    primitives.append(
        PrimitiveSpec.box(
            "DETAIL",
            24.0,
            500.0,
            300.0,
            _point(diameter / 2.0 + 12.0, 0.0, centre_u),
            "Condensate receiver nameplate",
            role="detail",
        )
    )
    for index, (n, du) in enumerate(
        ((-210.0, -120.0), (210.0, -120.0), (-210.0, 120.0), (210.0, 120.0)),
        start=1,
    ):
        primitives.append(
            PrimitiveSpec.cyli(
                "DETAIL",
                18.0,
                18.0,
                _point(diameter / 2.0 + 3.0, n, centre_u + du),
                f"Condensate receiver nameplate screw {index}",
                axis="E",
                role="hardware",
            )
        )
    primitives.extend(
        (
            PrimitiveSpec.box(
                "DETAIL",
                120.0,
                160.0,
                80.0,
                _point(diameter / 2.0 + 60.0, 0.0, saddle_height + 120.0),
                "Condensate receiver grounding lug",
                role="detail",
            ),
            PrimitiveSpec.cyli(
                "DETAIL",
                24.0,
                100.0,
                _point(diameter / 2.0 + 60.0, -50.0, saddle_height + 120.0),
                "Condensate receiver grounding-lug bolt",
                axis="N",
                role="hardware",
            ),
        )
    )

    gross_volume = (
        math.pi * (diameter / 1000.0) ** 2 / 4.0 * (straight_length / 1000.0)
        + math.pi * (diameter / 1000.0) ** 3 / 12.0
    )

    return EquipmentModel(
        name=name,
        display_name=display_name,
        area=PROJECT_AREA,
        position=position,
        overall_height=overall_height,
        main_dimensions=(
            f"Horizontal envelope {overall_length:.0f} × {diameter:.0f} mm; "
            f"straight barrel {straight_length:.1f} mm"
        ),
        capacity_m3=8.0,
        primitives=tuple(primitives),
        body_envelope=(
            -diameter / 2.0,
            diameter / 2.0,
            -overall_length / 2.0,
            overall_length / 2.0,
            saddle_height,
            body_top,
        ),
        nozzle_groups=tuple(nozzle_groups),
        native_nozzles=tuple(native_nozzles),
        parameters=(
            ParameterRecord(
                "Plan envelope",
                "3400 × 2017 mm",
                "Tank_list.xlsx text and Refs/MAIN CONDENSATE TANK.png",
            ),
            ParameterRecord("Listed capacity", "8 m3", "Tank_list.xlsx"),
            ParameterRecord(
                "Calculated gross vessel volume",
                f"{gross_volume:.2f} m3",
                "Cylinder + two 2:1 ellipsoidal-head envelopes",
            ),
            ParameterRecord(
                "Overall model height",
                f"{overall_height:.1f} mm",
                "500 mm saddles + OD + 200 mm contained vent projection",
            ),
        ),
        reference_values=(
            ReferenceValue(
                "Horizontal vessel construction",
                f"{straight_length:.1f} mm straight shell, D/4 heads, "
                f"{saddle_height:.0f} mm saddles",
                "Plan view is a capsule with two transverse support bands; "
                "no side elevation was supplied",
            ),
            ReferenceValue(
                "Nozzle/manway schedule",
                "; ".join(schedule),
                "Minimum condensate-receiver process connections",
            ),
            ReferenceValue(
                "Detailed hardware",
                "Four anchors per saddle; two lifting pads and pins; nameplate "
                "with screws; grounding lug; saddle wear/load-spreader and "
                "sole plates; native NOZZLE placeholders",
                "User-directed visual-detail pass, 2026-07-30; replaceable "
                "reference geometry pending vendor GA",
            ),
        ),
        sources=(
            DO_SOURCE,
            WORKBOOK_SOURCE,
            _top_view_source("MAIN CONDENSATE TANK.png"),
        ),
        notes=(
            f"The 8 m3 listed capacity is {8.0 / gross_volume * 100.0:.1f}% of "
            f"the {gross_volume:.2f} m3 calculated gross vessel envelope.",
            "The long axis is placed North-South to match the supplied plan-view "
            "orientation.",
        ),
        outstanding=(
            "Confirm saddle height, head geometry, long-axis bearing and vendor "
            "nozzle schedule from a side-view GA.",
        ),
    )


EQUIPMENT_MODELS: Tuple[EquipmentModel, ...] = (
    _atmospheric_tank(
        name="BLEACH_HOT_WATER_TANK",
        display_name="BLEACH HOT WATER TANK",
        position=(18720.0, -6004.0, -300.0),
        diameter=5020.0,
        capacity=100.0,
        drawing="BLEACH HOT WATER TANK.png",
        services=(
            ("N1", 250, 0.82, "N", "hot-water feed"),
            ("N2", 300, 0.16, "W", "pump suction"),
            ("N3", 200, 0.90, "E", "overflow"),
        ),
        ladder_bearing="W",
    ),
    _blow_tank(
        name="BLOW_TANK_1",
        display_name="BLOW TANK-1",
        position=(27276.0, 6034.0, -300.0),
        drawing_top="BLOW TANK-1(TOP).png",
        ladder_bearing="W",
    ),
    _blow_tank(
        name="BLOW_TANK_2",
        display_name="BLOW TANK-2",
        position=(27498.0, 18002.0, -300.0),
        drawing_top="BLOW TANK-2(TOP).png",
        ladder_bearing="E",
    ),
    _atmospheric_tank(
        name="WARM_WATER_TANK",
        display_name="WARM WATER TANK",
        position=(35894.0, -5970.0, -300.0),
        diameter=5700.0,
        capacity=145.0,
        drawing="WARM WATER TANK.png",
        services=(
            ("N1", 300, 0.82, "N", "warm-water feed"),
            ("N2", 350, 0.16, "S", "pump suction"),
            ("N3", 200, 0.90, "E", "overflow"),
        ),
        ladder_bearing="N",
    ),
    _atmospheric_tank(
        name="BROWN_HOT_WATER_TANK",
        display_name="BROWN HOT WATER TANK",
        position=(44004.0, -6002.0, -300.0),
        diameter=5714.0,
        capacity=145.0,
        drawing="BROWN HOT WATER TANK.png",
        services=(
            ("N1", 300, 0.82, "N", "brown-hot-water feed"),
            ("N2", 350, 0.16, "S", "pump suction"),
            ("N3", 200, 0.90, "E", "overflow"),
        ),
        ladder_bearing="S",
    ),
    _junk_trap(
        name="JUNK_TRAP_1",
        display_name="JUNK TRAP-1",
        position=(33635.0, 8034.0, -300.0),
        drawing="JUNK TRAP-1.png",
    ),
    _junk_trap(
        name="JUNK_TRAP_2",
        display_name="JUNK TRAP-2",
        position=(33635.0, 15965.0, -300.0),
        drawing="JUNK-TRAP-2.png",
    ),
    _pressure_accumulator(
        name="ACCUMULATOR_TANK",
        display_name="ACCUMULATOR TANK",
        position=(44001.0, 12002.0, -300.0),
        diameter=7023.0,
        capacity=500.0,
        drawing="ACCUMULATOR TANK.png",
        skirt_height=1800.0,
        ladder_bearing="N",
    ),
    _pressure_accumulator(
        name="ACCUMULATOR_TANK_AID_1",
        display_name="ACCUMULATOR TANK AID-1",
        position=(38433.0, 10002.0, -300.0),
        diameter=2022.0,
        capacity=None,
        drawing="ACCUMULATOR TANK AID-1.png",
        shell_height=4044.0,
        skirt_height=800.0,
        ladder_bearing=None,
    ),
    _pressure_accumulator(
        name="ACCUMULATOR_TANK_AID_2",
        display_name="ACCUMULATOR TANK AID-2",
        position=(38433.0, 14002.0, -300.0),
        diameter=2022.0,
        capacity=None,
        drawing="ACCUMULATOR TANK AID-2.png",
        shell_height=4044.0,
        skirt_height=800.0,
        ladder_bearing=None,
    ),
    _atmospheric_tank(
        name="W_L_SERVICE_TANK_1",
        display_name="W-L SERVICE TANK-1",
        position=(44006.0, 20002.0, -300.0),
        diameter=5000.0,
        capacity=100.0,
        drawing="W-L SERVICE TANK-1.png",
        services=(
            ("N1", 250, 0.82, "N", "white-liquor service inlet"),
            ("N2", 300, 0.16, "W", "white-liquor outlet"),
            ("N3", 200, 0.90, "E", "overflow / return"),
        ),
        ladder_bearing="N",
    ),
    _atmospheric_tank(
        name="W_L_SERVICE_TANK_2",
        display_name="W-L SERVICE TANK-2",
        position=(44004.0, 27801.0, -300.0),
        diameter=5000.0,
        capacity=100.0,
        drawing="W-L SERVICE TANK-2.png",
        services=(
            ("N1", 250, 0.82, "N", "white-liquor service inlet"),
            ("N2", 300, 0.16, "W", "white-liquor outlet"),
            ("N3", 200, 0.90, "E", "overflow / return"),
        ),
        ladder_bearing="S",
    ),
    _horizontal_condensate_tank(),
    _atmospheric_tank(
        name="SPENT_LIQUOR_TANK",
        display_name="SPENT LIQUOR TANK",
        position=(32502.0, 27803.0, -300.0),
        diameter=3000.0,
        capacity=10.0,
        drawing="SPENT LIQUOR TANK.png",
        services=(
            ("N1", 150, 0.80, "N", "spent-liquor inlet"),
            ("N2", 200, 0.22, "S", "spent-liquor outlet"),
            ("N3", 100, 0.88, "E", "overflow / return"),
        ),
        ladder_bearing=None,
        extra_notes=(
            "The very low capacity-to-diameter ratio produces a shallow vessel; "
            "this follows the supplied 3000 mm diameter and 10 m3 capacity "
            "without increasing either value.",
        ),
    ),
    _atmospheric_tank(
        name="B_L_TANK",
        display_name="B-L TANK",
        position=(37501.0, 27801.0, -300.0),
        diameter=5020.0,
        capacity=100.0,
        drawing="B-L TANK.png",
        services=(
            ("N1", 250, 0.82, "N", "black-liquor inlet"),
            ("N2", 300, 0.16, "W", "black-liquor outlet"),
            ("N3", 200, 0.90, "E", "overflow / return"),
        ),
        ladder_bearing="E",
    ),
)

# Project registry compatibility.  The shared CLI discovers EQUIPMENT.
EQUIPMENT = EQUIPMENT_MODELS

# No workbook value was silently corrected.  Ambiguities are reported as
# Reference Values and Outstanding Issues on the individual equipment records.
DATA_QUALITY_EXCEPTIONS = ()
