"""
Numeric validation and the per-pump audit record.
=================================================

Validation is numeric only.  A render that "looks like a pump" proves
nothing about whether the reconstruction followed the CAD, so every check
here compares measured quantities and reports the deviation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from .build import BASEPLATE_THICKNESS, PumpBuild, snap_to_catalogue_dn
from .semantic import ComponentKind, PumpSemanticModel, ViewType
from .source import CLIENT_LONGITUDINAL_AXIS, PumpRecord
from .transform import world_size

__all__ = ["Validation", "validate", "render_audit"]

#: Footprint agreement (mm) within which a reconstruction is accepted.
FOOTPRINT_TOL = 25.0


@dataclass
class Validation:
    """Outcome of checking one pump against its sources."""

    tag: str
    passed: bool
    checks: List[Tuple[str, bool, str]] = field(default_factory=list)

    def record(self, name: str, ok: bool, detail: str) -> None:
        self.checks.append((name, ok, detail))
        if not ok:
            self.passed = False

    @property
    def failures(self) -> List[Tuple[str, bool, str]]:
        return [c for c in self.checks if not c[1]]


def validate(
    record: PumpRecord, model: PumpSemanticModel, build: PumpBuild
) -> Validation:
    """Check the reconstruction against metadata and CAD evidence."""
    result = Validation(tag=record.tag, passed=True)

    # --- world placement is contractual ---
    plate = build.solids[0] if build.solids else None
    if plate is None:
        result.record("baseplate built", False, "no baseplate solid emitted")
        return result

    east, north, up = plate.position
    want_e, want_n, want_u = record.location_e_n_u
    dx, dy = abs(east - want_e), abs(north - want_n)
    result.record(
        "base centre matches metadata",
        dx < 1e-6 and dy < 1e-6,
        f"plate centre E{east:.1f} N{north:.1f} vs metadata E{want_e:.1f} "
        f"N{want_n:.1f} (dE={dx:.3f}, dN={dy:.3f})",
    )
    expected_up = want_u + BASEPLATE_THICKNESS / 2.0
    result.record(
        "baseplate underside sits on the metadata elevation",
        abs(up - expected_up) < 1e-6,
        f"plate centre U{up:.1f}, underside U{up - BASEPLATE_THICKNESS / 2.0:.1f} "
        f"vs metadata U{want_u:.1f}",
    )

    # --- baseplate dimensions ---
    if model.view is ViewType.ELEVATION and model.outline_size is not None:
        # The metadata pair is a drawn outline here, one figure of which is a
        # height; the plate is built from the horizontal span instead.
        span = min(model.outline_size)
        result.record(
            "baseplate footprint uses the drawn plan span, not the height",
            abs(plate.xlen - span) < 1.0 and abs(plate.ylen - span) < 1.0,
            f"plate {plate.xlen:.1f}x{plate.ylen:.1f} from drawn span "
            f"{span:.1f} mm (metadata {record.length_mm:.0f}x"
            f"{record.width_mm:.0f} describes the elevation outline)",
        )
    else:
        want_x, want_y = world_size(
            record.length_mm, record.width_mm, build.placement
        )
        result.record(
            "baseplate dimensions match metadata",
            abs(plate.xlen - want_x) < 0.05 and abs(plate.ylen - want_y) < 0.05,
            f"plate {plate.xlen:.1f}x{plate.ylen:.1f} vs metadata "
            f"{want_x:.1f}x{want_y:.1f} for layout axis "
            f"{build.placement.layout_axis}",
        )

    # --- orientation ---
    expected_axis = (
        CLIENT_LONGITUDINAL_AXIS.get(record.tag)
        or record.inlet_orientation
        or "E"
    ).upper()
    result.record(
        "orientation follows the contractual suction direction",
        build.placement.layout_axis == expected_axis
        or record.inlet_orientation.upper() not in ("E", "W", "N", "S"),
        f"layout axis {build.placement.layout_axis}, expected {expected_axis} "
        f"(metadata inlet {record.inlet_orientation!r})",
    )

    # --- nozzle sizes ---
    for nozzle in build.nozzles:
        source = record.dn_input_mm if nozzle.role == "SUCTION" else record.dn_output_mm
        nearest, _ = snap_to_catalogue_dn(source)
        result.record(
            f"{nozzle.role.lower()} bore traceable to metadata",
            nozzle.dn == nearest,
            f"DN{nozzle.dn} is the nearest catalogue bore to the measured "
            f"{source:.0f} mm (nearest available: DN{nearest})",
        )

    # --- top-view fidelity against the CAD evidence ---
    if model.view is ViewType.PLAN and model.outline_size is not None:
        bounds = build.top_view_bounds()
        if bounds is None:
            result.record("top view reconstructed", False, "model has no footprint")
        else:
            # Strict top-view property, stated positively rather than as an
            # extent difference: the contractual baseplate is the datum (the
            # model is built on it by construction), the drawing's own
            # outline must agree with it, and the model must never invent
            # geometry outside everything the drawing shows.  Attached
            # pipework legitimately extends the drawing beyond the outline,
            # but the pump macro models equipment only, so "contained in the
            # CAD extent" is the right upper bound.
            plate = build.solids[0]
            pe, pn, _ = plate.position
            plate_bounds = (
                pe - plate.xlen / 2.0,
                pn - plate.ylen / 2.0,
                pe + plate.xlen / 2.0,
                pn + plate.ylen / 2.0,
            )
            outline_world = _cad_box_to_world(model.outline, model, build)
            delta = max(
                abs(plate_bounds[i] - outline_world[i]) for i in range(4)
            )
            cad_world = (
                _cad_box_to_world(record.bounds, model, build)
                if record.bounds is not None
                else None
            )
            contained = (
                _contains(cad_world, bounds, slack=25.0)
                if cad_world is not None
                else True
            )
            ok = delta <= 10.0 and contained
            cover_note = (
                f"drawn outline agrees with the contractual plate within "
                f"{delta:.1f} mm"
                if delta <= 10.0
                else (
                    f"drawn outline deviates from the contractual plate by "
                    f"{delta:.1f} mm"
                )
            )
            contained_note = (
                "stays inside the CAD extent"
                if contained
                else f"projects outside the drawn extent {cad_world!r}"
            )
            result.record(
                "top-view footprint matches the CAD extent",
                ok,
                f"plate ({plate_bounds[0]:.0f},{plate_bounds[1]:.0f})-"
                f"({plate_bounds[2]:.0f},{plate_bounds[3]:.0f}), model "
                f"({bounds[0]:.0f},{bounds[1]:.0f})-({bounds[2]:.0f},"
                f"{bounds[3]:.0f}): {cover_note}; {contained_note}",
            )
    elif model.view is ViewType.ELEVATION and model.outline_size is not None:
        # On an elevation the drawing measures height directly, so height is
        # what gets checked.  The reference is the CAD extent rather than the
        # dimensioned outline: several drawings dimension only the machine
        # envelope and leave suction pipework or a pedestal outside it
        # (204-PU-003 draws 1509 mm of elbow above its own dimension), so the
        # outline alone would understate the pump.
        cad_bounds = record.bounds
        outline_height = max(model.outline_size)
        if cad_bounds is not None:
            vertical_is_y = (
                model.outline is not None
                and (model.outline[3] - model.outline[1])
                >= (model.outline[2] - model.outline[0])
            )
            cad_height = (
                cad_bounds[3] - cad_bounds[1]
                if vertical_is_y
                else cad_bounds[2] - cad_bounds[0]
            )
        else:
            cad_height = outline_height

        tops = [
            s.position[2] + (s.zlen if s.primitive == "BOX" else s.height) / 2.0
            for s in build.solids
        ]
        model_height = max(tops) - record.location_e_n_u[2] if tops else 0.0
        # The reconstruction must reach the dimensioned envelope and must not
        # exceed everything actually drawn.
        tolerance = max(cad_height * 0.10, 60.0)
        ok = (
            model_height >= outline_height - tolerance
            and model_height <= cad_height + tolerance
        )
        result.record(
            "elevation height is consistent with the CAD evidence",
            ok,
            f"model stands {model_height:.0f} mm tall; dimensioned envelope "
            f"{outline_height:.0f} mm, full drawn extent {cad_height:.0f} mm",
        )
    else:
        result.record(
            "CAD top-view evidence applied",
            False,
            "no top-view geometry exists in this file; the pump is built "
            "from metadata-proportioned Reference Values and remains "
            "UNCONFIRMED until a view or vendor data is supplied",
        )

    # --- per-component plan silhouettes follow the drawing ---
    # The batch-level bounds check can pass while an individual body is the
    # wrong size; this check compares each main body's own plan footprint
    # against the contour that produced it.  Detail solids (fins, bolts,
    # flanges) legitimately project a little beyond the body, so the
    # tolerance is a small fixed band rather than zero.
    mismatched: List[str] = []
    for component in model.components:
        if component.kind not in (
            ComponentKind.MOTOR,
            ComponentKind.PUMP_CASING,
            ComponentKind.BEARING_HOUSING,
            ComponentKind.COUPLING,
        ):
            continue
        primary = next(
            (
                solid
                for solid in build.solids
                if set(component.handles) & set(solid.source_handles)
                and solid.label.startswith(component.kind.value)
            ),
            None,
        )
        if primary is None:
            mismatched.append(f"{component.kind.value} (no emitted body)")
            continue
        want = _cad_box_to_world(component.bounds, model, build)
        got = primary.top_view_bounds()
        deviation = max(abs(want[i] - got[i]) for i in range(4))
        if deviation > 30.0:
            mismatched.append(
                f"{component.kind.value} (plan deviation {deviation:.0f} mm)"
            )
    result.record(
        "component plan silhouettes follow the drawing",
        not mismatched,
        (
            "all main bodies match their drawn contours within 30 mm"
            if not mismatched
            else "; ".join(mismatched)
        ),
    )

    # --- how much of the drawing the reconstruction actually used ---
    if record.entities:
        outline = model.outline
        eligible = {
            entity.handle
            for entity in record.entities
            if outline is None
            or _inside_entity(entity, outline, slack=2.0)
        }
        available = {entity.handle for entity in record.entities}
        consumed = set()
        for component in model.components:
            consumed.update(component.handles)
        # The baseplate is contractual and modelled, so the entities that
        # draw the dimensioned outline are consumed too - they are not
        # dropped linework, they are the plate itself.
        consumed |= _outline_handles(record.entities, outline)
        denominator = len(eligible) or len(available) or 1
        coverage = len(consumed & available & eligible) / denominator
        # Some linework is legitimately not modelled (centrelines, hatching,
        # the dimension annotation itself), so full coverage is not the
        # target; a low figure means real components were dropped.
        result.record(
            "CAD linework is substantially consumed",
            coverage >= 0.40,
            f"{len(consumed & available & eligible)}/{denominator} in-outline "
            f"entities ({100 * coverage:.0f}%) contribute to a modelled "
            f"component; {len(available) - denominator} out-of-outline entities "
            f"are attached pipework and are deliberately not modelled",
        )

    return result


def _contains(
    outer: Optional[Tuple[float, float, float, float]],
    inner: Tuple[float, float, float, float],
    *,
    slack: float,
) -> bool:
    """Whether ``inner`` sits inside ``outer``, or True when there is no outer."""
    if outer is None:
        return True
    return (
        inner[0] >= outer[0] - slack
        and inner[1] >= outer[1] - slack
        and inner[2] <= outer[2] + slack
        and inner[3] <= outer[3] + slack
    )


def _inside_entity(entity, bounds, *, slack: float) -> bool:
    x0 = min(entity.start.x, entity.end.x)
    x1 = max(entity.start.x, entity.end.x)
    y0 = min(entity.start.y, entity.end.y)
    y1 = max(entity.start.y, entity.end.y)
    return (
        x0 >= bounds[0] - slack
        and y0 >= bounds[1] - slack
        and x1 <= bounds[2] + slack
        and y1 <= bounds[3] + slack
    )


def _outline_handles(entities, outline: Optional[Tuple[float, float, float, float]]) -> set:
    """Handles of segments lying on the dimensioned outline rectangle."""
    if outline is None:
        return set()
    x0, y0, x1, y1 = outline
    handles = set()
    for entity in entities:
        ex0 = min(entity.start.x, entity.end.x)
        ex1 = max(entity.start.x, entity.end.x)
        ey0 = min(entity.start.y, entity.end.y)
        ey1 = max(entity.start.y, entity.end.y)
        vertical = abs(ex1 - ex0) < 1.0
        horizontal = abs(ey1 - ey0) < 1.0
        if vertical and (
            abs(ex0 - x0) < 2.0 or abs(ex1 - x1) < 2.0
        ) and ey0 >= y0 - 2.0 and ey1 <= y1 + 2.0:
            handles.add(entity.handle)
        elif horizontal and (
            abs(ey0 - y0) < 2.0 or abs(ey1 - y1) < 2.0
        ) and ex0 >= x0 - 2.0 and ex1 <= x1 + 2.0:
            handles.add(entity.handle)
    return handles


def _cad_box_to_world(box, model: PumpSemanticModel, build: PumpBuild) -> Tuple[float, float, float, float]:
    """Map a CAD-space bounds box onto the E/N plane through the pump frame."""
    if model.outline is None:
        return box
    ox0, oy0, ox1, oy1 = model.outline
    plate_cx = (ox0 + ox1) / 2.0
    plate_cy = (oy0 + oy1) / 2.0
    x0, y0, x1, y1 = box
    corners = (
        (x0, y0),
        (x1, y0),
        (x1, y1),
        (x0, y1),
    )
    world: List[Tuple[float, float]] = []
    for corner in corners:
        if model.long_axis == "x":
            along, across = corner[0] - plate_cx, corner[1] - plate_cy
        else:
            along, across = corner[1] - plate_cy, -(corner[0] - plate_cx)
        fx, fy = build.placement.forward
        lx, ly = build.placement.left
        world.append(
            (
                build.placement.origin[0] + along * fx + across * lx,
                build.placement.origin[1] + along * fy + across * ly,
            )
        )
    xs = [point[0] for point in world]
    ys = [point[1] for point in world]
    return (min(xs), min(ys), max(xs), max(ys))


def render_audit(
    record: PumpRecord,
    model: PumpSemanticModel,
    build: Optional[PumpBuild],
    validation: Optional[Validation],
) -> str:
    """Render the per-pump audit record required by the brief."""
    out: List[str] = []
    add = out.append

    add(f"Pump: {record.tag}")
    add("")
    add("Source:")
    add(f"  JSON: {record.source_path}")
    add(f"  Metadata row: {record.source_row if record.source_row else 'unknown'}")
    add(f"  Name: {record.name}")
    add(f"  Drawing: {record.source_drawing or 'n/a'}")
    add(f"  Units: {record.source_units or 'n/a'}")
    add("")
    add("CAD:")
    add(f"  valid entities: {len(record.entities)}")
    add(f"  skipped entities: {len(record.skipped)}")
    for skipped in record.skipped[:10]:
        add(f"    - {skipped.handle} ({skipped.kind}): {skipped.reason}")
    if len(record.skipped) > 10:
        add(f"    ... and {len(record.skipped) - 10} more")
    for key, value in sorted(model.stats.items()):
        add(f"  {key}: {value}")
    add(f"  view: {model.view.value.upper()}")
    add(f"  view evidence: {model.view_reason}")
    if model.outline_size:
        add(
            f"  outline: {model.outline_size[0]:.1f} x {model.outline_size[1]:.1f} mm"
        )
    add("")
    if model.features:
        add(f"Topology recovered ({len(model.features)} features):")
        counts: Dict[str, int] = {}
        for feature in model.features:
            key = getattr(getattr(feature, "kind", None), "value", "unknown")
            counts[key] = counts.get(key, 0) + 1
        for key in sorted(counts):
            add(f"  {key}: {counts[key]}")
        for feature in model.features[:12]:
            detail = getattr(feature, "detail", "")
            kind = getattr(getattr(feature, "kind", None), "value", "?")
            size = getattr(feature, "size", (0.0, 0.0))
            add(f"    {kind}: {size[0]:.0f} x {size[1]:.0f} mm - {detail}")
        if len(model.features) > 12:
            add(f"    ... and {len(model.features) - 12} more")
        add("")
    add("Components:")
    if model.components:
        for component in model.components:
            width, height = component.size
            add(
                f"  {component.kind.value}: {width:.0f} x {height:.0f} mm "
                f"[{component.confidence.value}] - {component.reason}"
            )
    else:
        add("  (none inferred)")
    add("")

    if build is not None:
        add("Transform:")
        add("  Local origin: baseplate underside centre")
        add(
            f"  World position: E {build.placement.origin[0]:.1f} "
            f"N {build.placement.origin[1]:.1f} U {build.placement.origin[2]:.1f}"
        )
        add(
            f"  Orientation: layout axis {build.placement.layout_axis} "
            f"({build.placement.rotation_deg:.0f} deg CCW from +E)"
        )
        add("")
        add("Model:")
        add(f"  solids: {len(build.solids)}")
        add(f"  nozzles: {len(build.nozzles)}")
        for nozzle in build.nozzles:
            add(
                f"    {nozzle.role} DN{nozzle.dn} axis {nozzle.axis} "
                f"-> {nozzle.catref}"
            )
        add("")
        add("Validation:")
        if validation is not None:
            for name, ok, detail in validation.checks:
                add(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
            add(f"  overall: {'PASS' if validation.passed else 'FAIL'}")
        add("")

    warnings = list(model.warnings) + (list(build.warnings) if build else [])
    notes = list(build.notes) if build else []
    add("Warnings:")
    if warnings:
        for warning in dict.fromkeys(warnings):
            add(f"  - {warning}")
    else:
        add("  (none)")
    if notes:
        add("")
        add("Notes:")
        for note in dict.fromkeys(notes):
            add(f"  - {note}")

    return "\n".join(out) + "\n"
