"""
Source loading for the pump JSON exports.
=========================================

Each file under ``C:\\Users\\A\\Desktop\\pumps`` is the ``Pump_details.xlsx``
row merged with a ``shape-reference`` CAD export (schema ``cad2e3d-aid`` v1).

This module only *reads*; it never repairs, recentres or rescales geometry.
Entities that cannot be reconstructed are recorded in ``skipped`` with a
reason rather than being coerced into the model.
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

__all__ = [
    "SUPPORTED_SCHEMA",
    "CadPoint",
    "RawCadEntity",
    "SkippedEntity",
    "PumpRecord",
    "load_pump",
    "load_all",
    "discover",
]

SUPPORTED_SCHEMA = "cad2e3d-aid"
SUPPORTED_SCHEMA_VERSION = 1

# Client-confirmed special main-axis layouts (JK_Pump_Build DO.txt 2026-07-29).
# The pump longitudinal axis normally equals the suction direction, but these
# MC pumps run East-West with the driver on the EAST side and the casing on the
# WEST side while their suction/discharge nozzles keep their own directions.
CLIENT_LONGITUDINAL_AXIS = {
    "205-PU-018": "W",
    "205-PU-038": "W",
}

# Millimetre tolerance below which two coordinates are the same point.  The
# exporter writes full double precision, so this only collapses genuine
# duplicates and zero-length stubs.
POINT_EPS = 1e-6


@dataclass(frozen=True)
class CadPoint:
    """A 2-D point in the source CAD coordinate space (millimetres)."""

    x: float
    y: float

    def distance_to(self, other: "CadPoint") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


@dataclass(frozen=True)
class RawCadEntity:
    """One usable CAD primitive, kept in its original coordinate space.

    The exporter tessellates every curve into straight segments, so in
    practice ``kind`` is always ``Line``.  ``radius``/``start_angle``/
    ``end_angle`` are carried through anyway so a future export containing
    real arcs needs no schema change here.
    """

    kind: str
    start: CadPoint
    end: CadPoint
    handle: str
    radius: float = 0.0
    start_angle: float = 0.0
    end_angle: float = 0.0

    @property
    def length(self) -> float:
        return self.start.distance_to(self.end)

    @property
    def is_degenerate(self) -> bool:
        return self.length <= POINT_EPS


@dataclass(frozen=True)
class SkippedEntity:
    """An entity that was not reconstructed, with the reason why."""

    handle: str
    kind: str
    reason: str


@dataclass
class PumpRecord:
    """A pump's metadata row plus its CAD evidence.

    ``entities`` holds only geometry that passed validation.  Anything
    dropped is in ``skipped`` so the audit can explain the difference
    between the source file and the reconstruction.
    """

    tag: str
    name: str
    source_path: str
    # --- metadata (authoritative for installation) ---
    location_e_n_u: Tuple[float, float, float]
    length_mm: float
    width_mm: float
    inlet_orientation: str
    outlet_orientation: str
    dn_input_mm: float
    dn_output_mm: float
    specification: str
    generic_type: str
    reference_top_view: Optional[str]
    source_row: Optional[int] = None
    # --- CAD evidence (authoritative for shape) ---
    entities: List[RawCadEntity] = field(default_factory=list)
    skipped: List[SkippedEntity] = field(default_factory=list)
    declared_bounds: Optional[Dict[str, float]] = None
    source_drawing: Optional[str] = None
    source_units: Optional[str] = None
    exporter_warnings: List[str] = field(default_factory=list)

    @property
    def has_geometry(self) -> bool:
        return bool(self.entities)

    @property
    def bounds(self) -> Optional[Tuple[float, float, float, float]]:
        """Measured (min_x, min_y, max_x, max_y) of the usable geometry."""
        if not self.entities:
            return None
        xs: List[float] = []
        ys: List[float] = []
        for entity in self.entities:
            xs.append(entity.start.x)
            xs.append(entity.end.x)
            ys.append(entity.start.y)
            ys.append(entity.end.y)
        return (min(xs), min(ys), max(xs), max(ys))

    @property
    def cad_size(self) -> Optional[Tuple[float, float]]:
        box = self.bounds
        if box is None:
            return None
        return (box[2] - box[0], box[3] - box[1])


def _as_point(raw: object, ) -> Optional[CadPoint]:
    """Convert an exporter point to a ``CadPoint``, or ``None`` if unusable."""
    if not isinstance(raw, dict):
        return None
    x = raw.get("x")
    y = raw.get("y")
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return None
    if not (math.isfinite(x) and math.isfinite(y)):
        return None
    return CadPoint(float(x), float(y))


def _as_float(raw: object, default: float = 0.0) -> float:
    if isinstance(raw, (int, float)) and math.isfinite(raw):
        return float(raw)
    return default


def _parse_location(raw: object) -> Tuple[float, float, float]:
    """Parse ``"E,N,U"``.  Raises ``ValueError`` if it is not usable -
    position is contractual, so a bad value must not be silently defaulted.
    """
    if not isinstance(raw, str):
        raise ValueError(f"location_e_n_u is not a string: {raw!r}")
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) != 3:
        raise ValueError(f"location_e_n_u must have 3 components: {raw!r}")
    try:
        values = tuple(float(p) for p in parts)
    except ValueError as exc:
        raise ValueError(f"location_e_n_u is not numeric: {raw!r}") from exc
    if not all(math.isfinite(v) for v in values):
        raise ValueError(f"location_e_n_u is not finite: {raw!r}")
    return (values[0], values[1], values[2])


def _extract_entities(
    group: Dict[str, object],
) -> Tuple[List[RawCadEntity], List[SkippedEntity]]:
    """Pull usable primitives out of one exporter group.

    Malformed primitives are skipped individually; one bad record must not
    discard the rest of the pump.
    """
    entities: List[RawCadEntity] = []
    skipped: List[SkippedEntity] = []

    primitives = group.get("primitives")
    if not isinstance(primitives, list):
        return entities, skipped

    for index, raw in enumerate(primitives):
        if not isinstance(raw, dict):
            skipped.append(SkippedEntity(f"#{index}", "?", "primitive is not an object"))
            continue
        kind = str(raw.get("kind") or "?")
        handle = str(raw.get("handle") or f"#{index}")
        start = _as_point(raw.get("start"))
        end = _as_point(raw.get("end"))

        if kind != "Line":
            # Preserve curved geometry if a future export ever emits it, but
            # never guess at parameters that are not present.
            skipped.append(
                SkippedEntity(handle, kind, f"unsupported entity kind {kind!r}")
            )
            continue
        if start is None or end is None:
            skipped.append(
                SkippedEntity(handle, kind, "incomplete or non-finite coordinates")
            )
            continue

        entity = RawCadEntity(
            kind=kind,
            start=start,
            end=end,
            handle=handle,
            radius=_as_float(raw.get("radius")),
            start_angle=_as_float(raw.get("startAngle")),
            end_angle=_as_float(raw.get("endAngle")),
        )
        if entity.is_degenerate:
            skipped.append(SkippedEntity(handle, kind, "zero-length segment"))
            continue
        entities.append(entity)

    return entities, skipped


def load_pump(path: str) -> PumpRecord:
    """Load one pump JSON.  Raises only on damage to the metadata itself."""
    with open(path, encoding="utf-8-sig") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise ValueError(f"{path}: top level is not an object")

    tag = payload.get("equipment_tag")
    if not isinstance(tag, str) or not tag.strip():
        raise ValueError(f"{path}: missing equipment_tag")

    source = payload.get("source")
    source_row = None
    if isinstance(source, dict) and isinstance(source.get("row"), int):
        source_row = source["row"]

    record = PumpRecord(
        tag=tag.strip(),
        name=str(payload.get("equipment_name") or "").strip(),
        source_path=path,
        location_e_n_u=_parse_location(payload.get("location_e_n_u")),
        length_mm=_as_float(payload.get("length_mm")),
        width_mm=_as_float(payload.get("width_mm")),
        inlet_orientation=str(payload.get("inlet_nozzle_orientation") or "").strip().upper(),
        outlet_orientation=str(payload.get("outlet_nozzle_orientation") or "").strip().upper(),
        dn_input_mm=_as_float(payload.get("dn_input_mm")),
        dn_output_mm=_as_float(payload.get("dn_output_mm")),
        specification=str(payload.get("specification") or "").strip(),
        generic_type=str(payload.get("generic_type") or "").strip(),
        reference_top_view=(
            payload.get("reference_top_view")
            if isinstance(payload.get("reference_top_view"), str)
            else None
        ),
        source_row=source_row,
    )

    shape = payload.get("shape-reference")
    if not isinstance(shape, dict):
        # Legitimate case: 203-PU-020 and 205-PU-004 carry no CAD evidence.
        return record

    schema = shape.get("schema")
    if schema != SUPPORTED_SCHEMA:
        record.skipped.append(
            SkippedEntity("-", "-", f"unrecognised shape-reference schema {schema!r}")
        )
        return record

    record.source_drawing = (
        shape.get("sourceDrawing") if isinstance(shape.get("sourceDrawing"), str) else None
    )
    record.source_units = (
        shape.get("sourceUnits") if isinstance(shape.get("sourceUnits"), str) else None
    )

    groups = shape.get("groups")
    if not isinstance(groups, list):
        return record

    for group in groups:
        if not isinstance(group, dict):
            continue
        entities, skipped = _extract_entities(group)
        record.entities.extend(entities)
        record.skipped.extend(skipped)

        bounds = group.get("bounds")
        if isinstance(bounds, dict) and record.declared_bounds is None:
            keys = ("minX", "minY", "maxX", "maxY")
            if all(isinstance(bounds.get(k), (int, float)) for k in keys):
                record.declared_bounds = {k: float(bounds[k]) for k in keys}

        for warning in group.get("warnings") or []:
            record.exporter_warnings.append(str(warning))
        for unsupported in group.get("unsupported") or []:
            record.skipped.append(
                SkippedEntity(
                    str(unsupported.get("handle", "-"))
                    if isinstance(unsupported, dict)
                    else "-",
                    str(unsupported.get("type", "?"))
                    if isinstance(unsupported, dict)
                    else "?",
                    "reported unsupported by the exporter",
                )
            )

    return record


def discover(directory: str) -> List[str]:
    """Return the pump JSON paths in ``directory``, sorted by tag."""
    paths = [
        os.path.join(directory, name)
        for name in sorted(os.listdir(directory))
        if name.lower().endswith(".json")
    ]
    return paths


def load_all(directory: str) -> Tuple[List[PumpRecord], List[Tuple[str, str]]]:
    """Load every pump JSON.  Returns (records, failures).

    A file that cannot be loaded at all is reported in ``failures`` rather
    than raising, so one damaged file cannot stop the batch.
    """
    records: List[PumpRecord] = []
    failures: List[Tuple[str, str]] = []
    for path in discover(directory):
        try:
            records.append(load_pump(path))
        except Exception as exc:  # noqa: BLE001 - batch isolation is required
            failures.append((path, f"{type(exc).__name__}: {exc}"))
    return records, failures
