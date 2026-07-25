"""
Engineering Deliverable Report
==============================
Builds the markdown report that accompanies the generated macro, covering the
four sections the project specification requires: completed equipment, modeling
parameters, estimated parameters with their sources, and outstanding issues.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, List, Sequence

from .schema import (
    ASSUMED_PROVENANCES,
    DataQualityException,
    Provenance,
    TankSpec,
)

__all__ = ["build_report"]


def _fmt_m(mm: float) -> str:
    """Format a millimetre dimension in metres, as the equipment list does."""
    return f"{mm / 1000.0:.2f} m"


def _completed_equipment(tanks: Sequence[TankSpec]) -> List[str]:
    lines = [
        "## Completed Equipment",
        "",
        f"{len(tanks)} tank-type equipment items modelled across the Washing, "
        "Screening and Bleaching area.",
        "",
        "| # | Tag | Equipment Name | Process Area |",
        "|---|-----|----------------|--------------|",
    ]
    for i, t in enumerate(tanks, 1):
        lines.append(f"| {i} | `{t.tag}` | {t.name} | {t.area} |")
    lines.append("")
    return lines


def _modeling_parameters(tanks: Sequence[TankSpec]) -> List[str]:
    lines = [
        "## Modeling Parameters",
        "",
        "All coordinates are the **bottom centre point** of the equipment, set "
        "out directly from the installation coordinates in the equipment list.",
        "",
        "| Tag | Diameter | Overall Height | Head Type | Bottom | Support | Skirt/Legs | Nozzles |",
        "|-----|----------|----------------|-----------|--------|---------|------------|---------|",
    ]
    for t in tanks:
        skirt = _fmt_m(t.skirt_height) if t.skirt_height else "-"
        diameter = _fmt_m(t.diameter)
        if t.outer_diameter:
            diameter += f" (outer {_fmt_m(t.outer_diameter)})"
        lines.append(
            f"| `{t.tag}` | {diameter} | {_fmt_m(t.total_height)} | "
            f"{t.head.value} | {t.bottom.value} | {t.support.value} | "
            f"{skirt} | {len(t.nozzles)} |"
        )
    lines.extend(["", "### Installation Coordinates", "",
                  "| Tag | East (mm) | North (mm) | Up (mm) | Source |",
                  "|-----|-----------|------------|---------|--------|"])
    for t in tanks:
        e, n, u = t.position
        source = t.sources.get("position", Provenance.EXCEL)
        flag = "recovered" if source is Provenance.RECOVERED else "as listed"
        lines.append(f"| `{t.tag}` | {e:.0f} | {n:.0f} | {u:.0f} | {flag} |")
    lines.append("")
    return lines


def _estimated_parameters(tanks: Sequence[TankSpec]) -> List[str]:
    lines = [
        "## Estimated Parameters (Reference Values)",
        "",
        "Every value below is an assumption, not project data. Each is flagged "
        "with the basis on which it was chosen so it can be replaced when "
        "official design information is issued.",
        "",
        "| Tag | Parameter | Basis |",
        "|-----|-----------|-------|",
    ]
    any_found = False
    for t in tanks:
        for field_name, provenance in t.assumed_fields():
            any_found = True
            lines.append(
                f"| `{t.tag}` | {field_name.replace('_', ' ')} | {provenance.value} |"
            )
    if not any_found:
        lines.append("| - | - | No assumed values |")
    lines.append("")
    return lines


def _data_quality(exceptions: Sequence[DataQualityException]) -> List[str]:
    lines = [
        "## Source Data Quality Exceptions",
        "",
        "Defects found in `Modeling_lists.xlsx` and the corrections applied. The "
        "workbook itself was **not** modified; every correction is made in the "
        "data layer and reported here so it can be verified against the source.",
        "",
    ]
    coordinate_defects = [e for e in exceptions if e.field_name == "position"]
    other_defects = [e for e in exceptions if e.field_name != "position"]

    if coordinate_defects:
        lines.extend([
            f"### Corrupted installation coordinates ({len(coordinate_defects)} rows)",
            "",
            coordinate_defects[0].rationale,
            "",
            "| Tag | Stored value | Recovered coordinate |",
            "|-----|--------------|----------------------|",
        ])
        for e in coordinate_defects:
            lines.append(f"| `{e.tag}` | `{e.source_value}` | `{e.corrected_value}` |")
        lines.append("")

    for e in other_defects:
        lines.extend([
            f"### `{e.tag}` - {e.field_name}",
            "",
            f"- **Listed:** {e.source_value}",
            f"- **Corrected to:** {e.corrected_value}",
            f"- **Basis:** {e.rationale}",
            "",
        ])
    return lines


def _outstanding_issues(tanks: Sequence[TankSpec]) -> List[str]:
    lines = [
        "## Outstanding Issues",
        "",
        "Items requiring confirmation before the models are used for detailed "
        "design.",
        "",
    ]
    found = False
    for t in tanks:
        issues = [n for n in t.notes if n.startswith("OUTSTANDING")]
        if not issues:
            continue
        found = True
        lines.append(f"**`{t.tag}` {t.name}**")
        lines.append("")
        for issue in issues:
            lines.append(f"- {issue[len('OUTSTANDING: '):]}")
        lines.append("")
    if not found:
        lines.extend(["No outstanding issues.", ""])
    return lines


def _modeling_notes(tanks: Sequence[TankSpec]) -> List[str]:
    lines = ["## Per-Equipment Modeling Notes", ""]
    for t in tanks:
        general = [n for n in t.notes if not n.startswith("OUTSTANDING")]
        if not general:
            continue
        lines.append(f"**`{t.tag}` {t.name}**")
        lines.append("")
        for note in general:
            lines.append(f"- {note}")
        lines.append("")
    return lines


def build_report(
    tanks: Sequence[TankSpec],
    *,
    macro_path: str = "",
    primitive_count: int = 0,
    verification_problems: Iterable[str] = (),
    data_quality_exceptions: Sequence[DataQualityException] = (),
) -> str:
    """
    Assemble the full engineering deliverable.

    Args:
        tanks: Tanks that were modelled.
        macro_path: Path of the generated PML macro, referenced in the header.
        primitive_count: Total primitives emitted.
        verification_problems: Any positioning failures found; an empty iterable
            means every tank verified.
        data_quality_exceptions: Source-data defects corrected in the data layer.
            Supplied by the project, since which defects exist is project data.
    """
    exceptions = list(data_quality_exceptions)
    problems = list(verification_problems)
    assumed_count = sum(len(t.assumed_fields()) for t in tanks)
    nozzle_count = sum(len(t.nozzles) for t in tanks)

    lines: List[str] = [
        "# WSB Area Tank Modeling - Engineering Deliverable",
        "",
        "**Project:** Pulp Mill - Washing, Screening and Bleaching (WSB)  ",
        "**Scope:** Tank-type equipment, 3D modelling for AVEVA E3D  ",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
    ]
    if macro_path:
        lines.append(f"**Macro:** `{macro_path}`  ")
    lines.extend([
        "",
        "---",
        "",
        "## Summary",
        "",
        f"- Equipment modelled: **{len(tanks)}**",
        f"- Primitives generated: **{primitive_count}**",
        f"- Nozzles modelled: **{nozzle_count}**",
        f"- Reference Values requiring confirmation: **{assumed_count}**",
        f"- Source data defects corrected: **{len(exceptions)}**",
        "",
    ])

    if problems:
        lines.extend([
            "> **Positioning verification FAILED**",
            "",
        ])
        lines.extend(f"> - {p}" for p in problems)
        lines.append("")
    else:
        lines.extend([
            "> **Positioning verified.** Every equipment item's bottom centre "
            "point coincides exactly with its installation coordinate from the "
            "equipment list. No global offset or positional deviation.",
            "",
        ])

    lines.extend(["---", ""])
    lines.extend(_completed_equipment(tanks))
    lines.extend(["---", ""])
    lines.extend(_modeling_parameters(tanks))
    lines.extend(["---", ""])
    lines.extend(_estimated_parameters(tanks))
    lines.extend(["---", ""])
    lines.extend(_data_quality(exceptions))
    lines.extend(["---", ""])
    lines.extend(_outstanding_issues(tanks))
    lines.extend(["---", ""])
    lines.extend(_modeling_notes(tanks))

    return "\n".join(lines).rstrip() + "\n"
