"""
Export the reconstruction for the HTML viewer.
==============================================

The viewer exists to close the loop: PML output cannot be seen from
here, so geometry errors survived every numeric check.  Rendering the
same reconstruction in a browser makes the shape reviewable before it
reaches E3D.

The data written here is the *same* geometry the PML emitter uses - the
revolution profile and the plan contours - so what the viewer shows is
what E3D will build.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Sequence

from .assembly_model import decompose
from .contours import find_outline_rectangle
from .profile import extract_profile
from .semantic import PumpSemanticModel, ViewType, build_semantic_model
from .source import PumpRecord, load_all

__all__ = ["pump_payload", "write_viewer"]


def pump_payload(record: PumpRecord, model: PumpSemanticModel) -> Dict[str, object]:
    """Everything the viewer needs for one pump."""
    payload: Dict[str, object] = {
        "tag": record.tag,
        "name": record.name,
        "view": model.view.value,
        "position": list(record.location_e_n_u),
        "metadata": {
            "length": record.length_mm,
            "width": record.width_mm,
            "suction": record.dn_input_mm,
            "discharge": record.dn_output_mm,
            "inlet": record.inlet_orientation,
            "outlet": record.outlet_orientation,
        },
        "outline": list(model.outline) if model.outline else None,
        "profile": None,
        "lines": [],
        "components": [],
        "parts": [],
    }

    # Raw linework, so the viewer can show the source beside the model.
    payload["lines"] = [
        [
            round(entity.start.x, 2),
            round(entity.start.y, 2),
            round(entity.end.x, 2),
            round(entity.end.y, 2),
        ]
        for entity in record.entities
    ]

    if model.outline is not None and model.view is ViewType.ELEVATION:
        vertical = (model.outline[3] - model.outline[1]) >= (
            model.outline[2] - model.outline[0]
        )
        profile = extract_profile(
            record.entities, model.outline, vertical=vertical
        )
        if profile is not None:
            simple = profile.simplified(tolerance=3.0)
            payload["profile"] = {
                "centreline": round(simple.centreline, 2),
                "vertical": vertical,
                "points": [
                    [round(p.height, 1), round(p.radius, 1)] for p in simple.points
                ],
            }

    # Every part the drawing contains, not just the pump body.
    outline = model.outline or find_outline_rectangle(record.entities)
    assembly = decompose(record.entities, outline)
    payload["parts"] = [
        {
            "kind": region.kind,
            "bounds": [round(v, 2) for v in region.bounds],
            "axis": region.axis,
            "revolve": region.revolve,
            "detail": region.detail,
            "profile": [[round(a, 1), round(b, 1)] for a, b in region.profile],
        }
        for region in assembly.regions
    ]
    payload["assemblyNotes"] = assembly.notes

    for component in model.components:
        payload["components"].append(
            {
                "kind": component.kind.value,
                "confidence": component.confidence.value,
                "reason": component.reason,
                "bounds": [round(v, 2) for v in component.bounds],
                "radius": component.radius,
                "roundAxis": component.round_axis,
            }
        )
    return payload


def write_viewer(source_dir: str, out_path: str, template: str) -> int:
    """Render every pump into a self-contained HTML page."""
    records, _ = load_all(source_dir)
    pumps: List[Dict[str, object]] = []
    for record in records:
        try:
            model = build_semantic_model(record)
        except Exception:  # noqa: BLE001 - one pump must not stop the export
            continue
        if not record.has_geometry:
            continue
        pumps.append(pump_payload(record, model))

    with open(template, encoding="utf-8") as handle:
        html = handle.read()
    # The placeholder is followed by an empty array so the un-substituted
    # template is still valid JavaScript; replace both together.
    payload = json.dumps(pumps, separators=(",", ":"))
    if "/*__PUMP_DATA__*/ []" in html:
        html = html.replace("/*__PUMP_DATA__*/ []", payload)
    else:
        html = html.replace("/*__PUMP_DATA__*/", payload)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(html)
    return len(pumps)
