"""
Composite Equipment PML Builder
===============================

Serialises :class:`wsb.composite_schema.EquipmentModel` instances through the
verified PML1 primitive builder and independently parses the resulting macro to
check real occupied bounds.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Iterable, List, Optional, Sequence, Tuple

from .composite_schema import Bounds, EquipmentModel, PrimitiveSpec
from .pml_builder import PMLBuilder, nozzle_component_path
from .pml_parser import (
    AXIS_VECTOR,
    bounds_of,
    equipment_name_to_element,
    parse_nozzles,
    parse_plan_direction,
    parse_primitives,
)

__all__ = [
    "build_combined_macro",
    "build_equipment_macro",
    "emit_equipment",
    "verify_equipment_macro",
    "validate_equipment_model",
]


_TOLERANCE_MM = 0.2
#: Axis unit vectors, re-exported from the shared parser so the emitter and
#: the verifier cannot disagree about what an axis letter means.
_AXIS_VECTOR = AXIS_VECTOR


def _world_point(
    local: Tuple[float, float, float],
    origin: Tuple[float, float, float],
) -> Tuple[float, float, float]:
    return tuple(local[i] + origin[i] for i in range(3))  # type: ignore[return-value]


def _parse_plan_direction(direction: str) -> float:
    """Inverse of the builder's cardinal/quadrant BOX bearing formatter."""
    return parse_plan_direction(direction)


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
    """The world extent of a parsed primitive, honouring its E3D datum."""
    return bounds_of(primitive)


def _parse_primitives(script: str, equipment_name: str) -> List[dict]:
    """Parse actual E3D element datums from one EQUI block, with bounds."""
    return parse_primitives(script, equipment_name, with_bounds=True)


def _parse_nozzles(script: str, equipment_name: str) -> List[dict]:
    """Parse native NOZZLE blocks from one EQUI for independent verification."""
    return parse_nozzles(script, equipment_name)


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
        expected_name = equipment_name_to_element(
            f"{model.name}_{expected_nozzle.name}_NOZZ"
        )
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
