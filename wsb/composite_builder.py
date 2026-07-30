"""
Composite Equipment PML Builder
===============================

Serialises :class:`wsb.composite_schema.EquipmentModel` instances through the
verified PML1 primitive builder and independently parses the resulting macro to
check real occupied bounds.
"""

from __future__ import annotations

import math
import re
from datetime import datetime
from typing import Iterable, List, Optional, Sequence, Tuple

from .composite_schema import Bounds, EquipmentModel, PrimitiveSpec
from .pml_builder import PMLBuilder, nozzle_component_path

__all__ = [
    "build_combined_macro",
    "build_equipment_macro",
    "emit_equipment",
    "verify_equipment_macro",
    "validate_equipment_model",
]


_TOLERANCE_MM = 0.2
_ORI_RE = re.compile(r"^ORI\s+Z\s+IS\s+([UDENSW])\b", re.IGNORECASE)
_NOZZLE_ORI_RE = re.compile(
    r"^ORI\s+P1\s+IS\s+([UDENSW])\b", re.IGNORECASE
)
_BOX_PLAN_ORI_RE = re.compile(
    r"^ORI\s+Z\s+IS\s+U\s+AND\s+X\s+IS\s+(.+)$", re.IGNORECASE
)
_POS_RE = re.compile(
    r"^POS\s+E\s+(-?[\d.]+)\s+N\s+(-?[\d.]+)\s+U\s+(-?[\d.]+)",
    re.IGNORECASE,
)
_GEOMETRY = frozenset({"CYLI", "CONE", "DISH", "BOX"})
_AXIS_VECTOR = {
    "U": (0.0, 0.0, 1.0),
    "D": (0.0, 0.0, -1.0),
    "E": (1.0, 0.0, 0.0),
    "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0),
    "S": (0.0, -1.0, 0.0),
}


def _world_point(
    local: Tuple[float, float, float],
    origin: Tuple[float, float, float],
) -> Tuple[float, float, float]:
    return tuple(local[i] + origin[i] for i in range(3))  # type: ignore[return-value]


def _parse_plan_direction(direction: str) -> float:
    """Inverse of the builder's cardinal/quadrant BOX bearing formatter."""
    tokens = direction.upper().split()
    cardinal = {"E": 0.0, "N": 90.0, "W": 180.0, "S": 270.0}
    if len(tokens) == 1 and tokens[0] in cardinal:
        return cardinal[tokens[0]]
    if len(tokens) != 3:
        raise ValueError(f"Unsupported BOX plan direction {direction!r}")
    first, angle_text, second = tokens
    angle = float(angle_text)
    quadrant_start = {
        ("E", "N"): 0.0,
        ("N", "W"): 90.0,
        ("W", "S"): 180.0,
        ("S", "E"): 270.0,
    }
    try:
        start = quadrant_start[(first, second)]
    except KeyError:
        raise ValueError(f"Unsupported BOX plan direction {direction!r}") from None
    if not 0.0 < angle < 90.0:
        raise ValueError(f"BOX quadrant angle must be 0..90, got {angle}")
    return start + angle


def _plan_rotation_difference(first: float, second: float) -> float:
    """Smallest BOX orientation difference, accounting for 180° symmetry."""
    difference = abs((first - second) % 180.0)
    return min(difference, 180.0 - difference)


def _emit_primitive(
    primitive: PrimitiveSpec,
    model: EquipmentModel,
    builder: PMLBuilder,
) -> None:
    point = _world_point(primitive.point, model.position)
    if primitive.kind == "CYLI":
        builder.cyli(
            primitive.diameter,
            primitive.height,
            point,
            axis=primitive.axis,
            label=primitive.label,
        )
    elif primitive.kind == "CONE":
        builder.cone(
            primitive.d_bottom,
            primitive.d_top,
            primitive.height,
            point,
            axis=primitive.axis,
            label=primitive.label,
        )
    elif primitive.kind == "DISH":
        builder.dish(
            primitive.diameter,
            primitive.height,
            point,
            axis=primitive.axis,
            radius=primitive.radius or primitive.diameter,
            label=primitive.label,
        )
    elif primitive.kind == "BOX":
        builder.box(
            primitive.xlen,
            primitive.ylen,
            primitive.zlen,
            point,
            label=primitive.label,
            plan_rotation_deg=primitive.plan_rotation_deg,
        )
    else:  # pragma: no cover - protected by PrimitiveSpec validation
        raise ValueError(f"Unsupported primitive {primitive.kind}")


def emit_equipment(model: EquipmentModel, builder: PMLBuilder) -> None:
    """Emit one independent EQUI and its SUBE hierarchy."""
    builder.comment()
    builder.banner(model.display_name)
    builder.comment(
        f"Bottom centre: E {model.position[0]:.1f}  "
        f"N {model.position[1]:.1f}  U {model.position[2]:.1f}"
    )
    builder.comment(f"Main dimensions: {model.main_dimensions}")
    builder.comment(f"Overall height: {model.overall_height:.1f} mm")
    if model.capacity_m3 is not None:
        builder.comment(f"Listed capacity: {model.capacity_m3:g} m3")
    builder.comment()

    builder.equi(model.name)
    for group in model.groups():
        builder.sube(f"{model.name}_{group}")
        for primitive in model.primitives_for_group(group):
            _emit_primitive(primitive, model, builder)
        for nozzle in model.nozzles_for_group(group):
            builder.nozzle(
                f"{model.name}_{nozzle.name}_NOZZ",
                nozzle.dn,
                nozzle.height,
                nozzle.translated_face(model.position),
                axis=nozzle.axis,
                label=nozzle.label,
            )


def _header(builder: PMLBuilder, title: str, scope: str) -> None:
    builder.header(
        title,
        meta=(
            ("Scope", scope),
            ("Units", "mm"),
            ("Frame", "E = East, N = North, U = Up"),
            ("Datum", "Equipment bottom centre / foundation bearing plane"),
            ("Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ("Execution", "Select a writable ZONE, then $M <this file>"),
        ),
    )


def build_equipment_macro(model: EquipmentModel) -> str:
    """Build and PML-validate one equipment macro."""
    validate_equipment_model(model)
    builder = PMLBuilder(model.name)
    _header(builder, model.display_name, "One independent equipment model")
    emit_equipment(model, builder)
    builder.catref_pass()
    builder.footer()
    script = builder.build()
    problems = verify_equipment_macro(model, script)
    if problems:
        raise ValueError(
            f"{model.display_name} failed numerical verification:\n  "
            + "\n  ".join(problems)
        )
    return script


def build_combined_macro(models: Sequence[EquipmentModel], project_name: str) -> str:
    """Build a convenience macro containing every independent EQUI."""
    for model in models:
        validate_equipment_model(model)
    builder = PMLBuilder(project_name)
    _header(
        builder,
        f"{project_name} - COOKING PLANT EQUIPMENT",
        f"{len(models)} independent equipment items",
    )
    for model in models:
        emit_equipment(model, builder)
    builder.catref_pass()
    builder.footer()
    script = builder.build()
    problems: List[str] = []
    for model in models:
        problems.extend(verify_equipment_macro(model, script))
    if problems:
        raise ValueError(
            "Combined macro failed numerical verification:\n  "
            + "\n  ".join(problems)
        )
    return script


def _inside(inner: Bounds, outer: Bounds, tolerance: float = _TOLERANCE_MM) -> bool:
    return (
        inner[0] >= outer[0] - tolerance
        and inner[1] <= outer[1] + tolerance
        and inner[2] >= outer[2] - tolerance
        and inner[3] <= outer[3] + tolerance
        and inner[4] >= outer[4] - tolerance
        and inner[5] <= outer[5] + tolerance
    )


def _union(bounds: Iterable[Bounds]) -> Optional[Bounds]:
    items = list(bounds)
    if not items:
        return None
    return (
        min(b[0] for b in items),
        max(b[1] for b in items),
        min(b[2] for b in items),
        max(b[3] for b in items),
        min(b[4] for b in items),
        max(b[5] for b in items),
    )


def validate_equipment_model(model: EquipmentModel) -> None:
    """
    Validate the resolved geometry before any PML is emitted.

    This is deliberately property-based: no primitive may fall below the
    foundation, the complete model must touch the datum, every primitive must
    remain inside the declared overall height, and authoritative body geometry
    must fit the project envelope.
    """
    local_bounds = [p.bounds() for p in model.primitives]
    lowest = min(b[4] for b in local_bounds)
    highest = max(b[5] for b in local_bounds)
    if abs(lowest) > _TOLERANCE_MM:
        raise ValueError(
            f"{model.display_name}: lowest local geometry is {lowest:.1f} mm; "
            "the bottom-centre datum must be 0"
        )
    if highest > model.overall_height + _TOLERANCE_MM:
        raise ValueError(
            f"{model.display_name}: geometry reaches {highest:.1f} mm but "
            f"overall height is {model.overall_height:.1f} mm"
        )

    body = [p.bounds() for p in model.primitives if p.role == "body"]
    if not body:
        raise ValueError(f"{model.display_name}: no authoritative body primitives")
    for bounds in body:
        if not _inside(bounds, model.body_envelope):
            raise ValueError(
                f"{model.display_name}: body primitive {bounds} exceeds "
                f"the declared body envelope {model.body_envelope}"
            )
    body_union = _union(body)
    if body_union is None:  # pragma: no cover
        raise ValueError(f"{model.display_name}: empty body")
    for actual, declared in zip(body_union, model.body_envelope):
        if abs(actual - declared) > _TOLERANCE_MM:
            raise ValueError(
                f"{model.display_name}: body union {body_union} does not match "
                f"declared envelope {model.body_envelope}"
            )


def _parsed_bounds(primitive: dict) -> Bounds:
    e = primitive["east"]
    n = primitive["north"]
    u = primitive["up"]
    if primitive["kind"] == "BOX":
        angle = math.radians(primitive.get("plan_rotation_deg", 0.0))
        cosine = abs(math.cos(angle))
        sine = abs(math.sin(angle))
        half_e = (
            cosine * primitive["xlen"] / 2.0
            + sine * primitive["ylen"] / 2.0
        )
        half_n = (
            sine * primitive["xlen"] / 2.0
            + cosine * primitive["ylen"] / 2.0
        )
        return (
            e - half_e,
            e + half_e,
            n - half_n,
            n + half_n,
            u - primitive["zlen"] / 2.0,
            u + primitive["zlen"] / 2.0,
        )

    diameter = max(
        primitive.get("diam", 0.0),
        primitive.get("dbot", 0.0),
        primitive.get("dtop", 0.0),
    )
    radius = diameter / 2.0
    de, dn, du = _AXIS_VECTOR[primitive["axis"]]
    if primitive["kind"] == "DISH":
        # DISH POS is the flat rim / tangent plane, not a geometric centre.
        start = (e, n, u)
        end = (
            e + de * primitive["heig"],
            n + dn * primitive["heig"],
            u + du * primitive["heig"],
        )
    else:
        half = primitive["heig"] / 2.0
        axis_half = (de * half, dn * half, du * half)
        start = (e - axis_half[0], n - axis_half[1], u - axis_half[2])
        end = (e + axis_half[0], n + axis_half[1], u + axis_half[2])
    e_min, e_max = sorted((start[0], end[0]))
    n_min, n_max = sorted((start[1], end[1]))
    u_min, u_max = sorted((start[2], end[2]))
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


def _parse_primitives(script: str, equipment_name: str) -> List[dict]:
    """Parse actual E3D element datums from one EQUI block."""
    expected = re.sub(r"[^A-Za-z0-9_/]", "_", equipment_name.strip())
    expected = re.sub(r"_{2,}", "_", expected).strip("_")
    in_equipment = False
    current: dict = {}
    primitives: List[dict] = []

    for raw in script.splitlines():
        line = raw.strip()
        if line.startswith("NEW EQUI /"):
            in_equipment = line[len("NEW EQUI /") :] == expected
            current = {}
            continue
        if not in_equipment:
            continue
        if line.startswith("NEW "):
            kind = line[4:].split()[0].upper()
            current = {"kind": kind, "axis": "U"} if kind in _GEOMETRY else {}
            continue
        if not current:
            continue
        for attribute in (
            "DIAM",
            "HEIG",
            "XLEN",
            "YLEN",
            "ZLEN",
            "DTOP",
            "DBOT",
        ):
            if line.startswith(attribute + " "):
                current[attribute.lower()] = float(line.split()[1])
        box_orientation = _BOX_PLAN_ORI_RE.match(line)
        if box_orientation and current.get("kind") == "BOX":
            current["plan_rotation_deg"] = _parse_plan_direction(
                box_orientation.group(1)
            )
        orientation = _ORI_RE.match(line)
        if orientation:
            current["axis"] = orientation.group(1).upper()
        position = _POS_RE.match(line)
        if position:
            current["east"], current["north"], current["up"] = (
                float(value) for value in position.groups()
            )
            current["bounds"] = _parsed_bounds(current)
            primitives.append(current)
            current = {}
    return primitives


def _parse_nozzles(script: str, equipment_name: str) -> List[dict]:
    """Parse native NOZZLE blocks from one EQUI for independent verification."""
    expected = re.sub(r"[^A-Za-z0-9_/]", "_", equipment_name.strip())
    expected = re.sub(r"_{2,}", "_", expected).strip("_")
    in_equipment = False
    current: dict = {}
    nozzles: List[dict] = []

    for raw in script.splitlines():
        line = raw.strip()
        if line.startswith("NEW EQUI /"):
            in_equipment = line[len("NEW EQUI /") :] == expected
            current = {}
            continue
        if not in_equipment:
            continue
        if line.startswith("NEW NOZZLE /"):
            current = {"name": line[len("NEW NOZZLE /") :]}
            continue
        if line.startswith("NEW "):
            current = {}
            continue
        if not current:
            continue
        if line.startswith("CATR SPCOMPONENT "):
            current["catref"] = line[len("CATR SPCOMPONENT ") :]
        position = _POS_RE.match(line)
        if position:
            current["face"] = tuple(float(value) for value in position.groups())
        orientation = _NOZZLE_ORI_RE.match(line)
        if orientation:
            current["axis"] = orientation.group(1).upper()
        if line.startswith("HEIG "):
            current["height"] = float(line.split()[1])
        if line == "END":
            nozzles.append(current)
            current = {}
    return nozzles


def _bounds_close(actual: Bounds, expected: Bounds) -> bool:
    return all(
        abs(a - e) <= _TOLERANCE_MM for a, e in zip(actual, expected)
    )


def verify_equipment_macro(model: EquipmentModel, script: str) -> List[str]:
    """
    Numerically verify the emitted macro, independently of the writer.

    The parser applies E3D's element-specific datums (centre for CYLI/CONE/BOX,
    rim plane for DISH), derives occupied bounds from the emitted
    dimensions/orientation, and compares those bounds to the local geometry
    resolved by the project.
    """
    parsed = _parse_primitives(script, model.name)
    emitted_sources = [
        primitive
        for group in model.groups()
        for primitive in model.primitives_for_group(group)
    ]
    problems: List[str] = []
    if len(parsed) != len(emitted_sources):
        return [
            f"{model.display_name}: expected {len(emitted_sources)} primitives "
            f"but parsed {len(parsed)}"
        ]

    for index, (actual, source) in enumerate(
        zip(parsed, emitted_sources), start=1
    ):
        if actual["kind"] != source.kind:
            problems.append(
                f"{model.display_name} primitive {index}: expected "
                f"{source.kind}, got {actual['kind']}"
            )
            continue
        if source.kind == "BOX":
            actual_rotation = actual.get("plan_rotation_deg", 0.0)
            if (
                _plan_rotation_difference(
                    actual_rotation, source.plan_rotation_deg
                )
                > 0.01
            ):
                problems.append(
                    f"{model.display_name} primitive {index} ({source.label}): "
                    f"emitted BOX plan rotation {actual_rotation} deg != "
                    f"expected {source.plan_rotation_deg} deg"
                )
        expected = source.translated_bounds(model.position)
        if not _bounds_close(actual["bounds"], expected):
            problems.append(
                f"{model.display_name} primitive {index} ({source.label}): "
                f"emitted bounds {actual['bounds']} != expected {expected}"
            )

    actual_nozzles = _parse_nozzles(script, model.name)
    expected_nozzles = [
        nozzle
        for group in model.groups()
        for nozzle in model.nozzles_for_group(group)
    ]
    if len(actual_nozzles) != len(expected_nozzles):
        problems.append(
            f"{model.display_name}: expected {len(expected_nozzles)} native "
            f"NOZZLE elements but parsed {len(actual_nozzles)}"
        )
    for index, (actual, expected_nozzle) in enumerate(
        zip(actual_nozzles, expected_nozzles), start=1
    ):
        expected_name = re.sub(
            r"[^A-Za-z0-9_/]",
            "_",
            f"{model.name}_{expected_nozzle.name}_NOZZ",
        )
        expected_name = re.sub(r"_{2,}", "_", expected_name).strip("_")
        if actual.get("name") != expected_name:
            problems.append(
                f"{model.display_name} nozzle {index}: expected name "
                f"{expected_name}, got {actual.get('name')}"
            )
        expected_face = expected_nozzle.translated_face(model.position)
        actual_face = actual.get("face")
        if actual_face is None or any(
            abs(actual_face[i] - expected_face[i]) > _TOLERANCE_MM
            for i in range(3)
        ):
            problems.append(
                f"{model.display_name} nozzle {expected_nozzle.name}: face "
                f"{actual_face} != expected {expected_face}"
            )
        if actual.get("axis") != expected_nozzle.axis:
            problems.append(
                f"{model.display_name} nozzle {expected_nozzle.name}: axis "
                f"{actual.get('axis')} != {expected_nozzle.axis}"
            )
        if abs(actual.get("height", -1.0) - expected_nozzle.height) > _TOLERANCE_MM:
            problems.append(
                f"{model.display_name} nozzle {expected_nozzle.name}: HEIG "
                f"{actual.get('height')} != {expected_nozzle.height}"
            )
        try:
            expected_catref = nozzle_component_path(expected_nozzle.dn)
        except KeyError:
            problems.append(
                f"{model.display_name} nozzle {expected_nozzle.name}: "
                f"DN{expected_nozzle.dn} has no verified catalogue component"
            )
        else:
            if actual.get("catref") != expected_catref:
                problems.append(
                    f"{model.display_name} nozzle {expected_nozzle.name}: CATR "
                    f"{actual.get('catref')} != {expected_catref}"
                )

    if parsed:
        lowest = min(p["bounds"][4] for p in parsed)
        highest = max(p["bounds"][5] for p in parsed)
        expected_low = model.position[2]
        expected_high = model.position[2] + model.overall_height
        if abs(lowest - expected_low) > _TOLERANCE_MM:
            problems.append(
                f"{model.display_name}: lowest emitted geometry U {lowest:.1f} "
                f"!= bottom datum U {expected_low:.1f}"
            )
        if highest > expected_high + _TOLERANCE_MM:
            problems.append(
                f"{model.display_name}: emitted geometry reaches U "
                f"{highest:.1f}, above declared overall U {expected_high:.1f}"
            )
    return problems
