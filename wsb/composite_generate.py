"""Generation pipeline for resolved composite equipment models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from .composite_builder import (
    build_combined_macro,
    build_equipment_macro,
    verify_equipment_macro,
)
from .composite_schema import EquipmentModel, SourceRecord
from .projects import Project

__all__ = [
    "CompositeGenerationResult",
    "build_composite_report",
    "generate_composite_project",
]


@dataclass
class CompositeGenerationResult:
    models: Sequence[EquipmentModel]
    individual_macros: Tuple[str, ...]
    combined_macro: str
    report: str
    verification_problems: Tuple[str, ...]
    macro_paths: Tuple[Path, ...] = ()
    combined_path: Optional[Path] = None
    report_path: Optional[Path] = None

    @property
    def verified(self) -> bool:
        return not self.verification_problems

    @property
    def primitive_count(self) -> int:
        return sum(model.primitive_count for model in self.models)

    @property
    def nozzle_count(self) -> int:
        return sum(model.nozzle_count for model in self.models)


def _source_key(source: SourceRecord) -> Tuple[str, str, str]:
    return (source.label, source.detail, source.url)


def _fmt_height(value: float) -> str:
    return f"{value:.1f} mm"


def build_composite_report(
    project: Project,
    models: Sequence[EquipmentModel],
    *,
    verification_problems: Sequence[str] = (),
    output_dir: Optional[Path] = None,
) -> str:
    """Answer-first engineering deliverable for the composite project."""
    primitive_count = sum(model.primitive_count for model in models)
    nozzle_count = sum(model.nozzle_count for model in models)
    native_nozzle_count = sum(len(model.native_nozzles) for model in models)
    plan_oriented_box_count = sum(
        primitive.kind == "BOX"
        and abs(primitive.plan_rotation_deg) > 1e-9
        for model in models
        for primitive in model.primitives
    )
    reference_count = sum(len(model.reference_values) for model in models)
    problems = list(verification_problems)

    lines: List[str] = [
        "# JK Cooking Plant E3D Equipment — Engineering Deliverable",
        "",
        f"**Project folder:** `Projects/{project.name}`  ",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        "**Datum:** equipment bottom centre / foundation bearing plane  ",
        "**Coordinates:** global E3D East, North, Up; millimetres",
        "",
        "## Outcome",
        "",
        f"- Independent equipment macros: **{len(models)}**",
        f"- Convenience combined macro: **1**",
        f"- E3D primitives: **{primitive_count}**",
        f"- Nozzle/manway assemblies: **{nozzle_count}**",
        f"- Catalogue-backed native NOZZLE placeholders: "
        f"**{native_nozzle_count}**",
        f"- Plan-oriented support/detail BOX elements: "
        f"**{plan_oriented_box_count}**",
        f"- Explicit Reference Values: **{reference_count}**",
    ]
    if problems:
        lines.extend(
            [
                f"- Numerical verification: **FAILED ({len(problems)} issues)**",
                "",
            ]
        )
        lines.extend(f"  - {problem}" for problem in problems)
    else:
        lines.extend(
            [
                "- Numerical verification: **passed for all equipment**",
                "",
                "Every emitted primitive was parsed back using its PML element-"
                "specific datum (centre for CYLI/CONE/BOX; rim for DISH) and "
                "reconciled with the resolved local geometry. "
                "All 15 models touch their listed bottom-centre elevation, no "
                "primitive falls below the foundation datum, and no model "
                "exceeds its declared overall height.",
            ]
        )

    lines.extend(
        [
            "",
            "## Deliverables and loading",
            "",
            "Select a writable **ZONE** in AVEVA E3D Design, then load either an "
            "individual macro or the combined macro:",
            "",
            "```text",
            "$M <full path to the .pml file>",
            "```",
            "",
        ]
    )
    if output_dir is not None:
        lines.extend(
            [
                f"Output folder: `{output_dir}`",
                "",
                f"Combined macro: `{output_dir / (project.slug + '.pml')}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Completed equipment",
            "",
            "| # | Equipment | Bottom centre E, N, U (mm) | Main dimensions | "
            "Overall height | Capacity | Primitives | Nozzle groups |",
            "|---:|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for index, model in enumerate(models, start=1):
        e, n, u = model.position
        capacity = f"{model.capacity_m3:g} m3" if model.capacity_m3 is not None else "—"
        lines.append(
            f"| {index} | {model.display_name} | {e:.0f}, {n:.0f}, {u:.0f} | "
            f"{model.main_dimensions} | {_fmt_height(model.overall_height)} | "
            f"{capacity} | {model.primitive_count} | {model.nozzle_count} |"
        )

    lines.extend(
        [
            "",
            "## Height and geometry calculations",
            "",
            "Where the workbook says `CALCULATE BY DIAMETER AND CAPACITY`, the "
            "capacity cylinder is calculated from `H = V / (πD²/4)`. A conical "
            "roof is then added above that cylinder; its rise is an explicit "
            "Reference Value, not hidden inside the capacity calculation.",
            "",
        ]
    )
    for model in models:
        lines.extend([f"### {model.display_name}", ""])
        for parameter in model.parameters:
            lines.append(
                f"- **{parameter.name}:** {parameter.value}  \n"
                f"  Source/basis: {parameter.source}"
            )
        for note in model.notes:
            lines.append(f"- {note}")
        lines.append("")

    lines.extend(
        [
            "## Reference Values",
            "",
            "These values are assumptions pending project/vendor confirmation. "
            "They do not override workbook dimensions or the authoritative Blow "
            "Tank profile strings.",
            "",
            "| Equipment | Parameter | Value | Basis |",
            "|---|---|---|---|",
        ]
    )
    for model in models:
        for reference in model.reference_values:
            lines.append(
                f"| {model.display_name} | {reference.parameter} | "
                f"{reference.value} | {reference.basis} |"
            )

    lines.extend(
        [
            "",
            "## Outstanding issues",
            "",
        ]
    )
    for model in models:
        if not model.outstanding:
            continue
        lines.extend([f"**{model.display_name}**", ""])
        lines.extend(f"- {issue}" for issue in model.outstanding)
        lines.append("")
    lines.extend(
        [
            "**Project-wide**",
            "",
            "- The supplied DWG could not be read locally because no DWG parser "
            "is installed. It was not uploaded to a third-party converter. The "
            "16 exported PNG reference views were used.",
            "- Each connection is represented by one native E3D `NOZZLE` "
            "placeholder in its own SUBE. The verified "
            "`/150lb_Ansi_Flanged` component mapping supplies a realistic "
            "temporary catalogue shape; Reference Value sizes must still be "
            "reconciled with the final vendor schedule and receiving-project "
            "catalogue.",
            "- Replace Reference Value nozzle schedules, support dimensions and "
            "unknown side elevations when vendor GAs become available.",
            "",
            "## Source register",
            "",
        ]
    )

    sources = {}
    for model in models:
        for source in model.sources:
            sources[_source_key(source)] = source
    for source in sources.values():
        detail = source.detail
        if source.url:
            detail += f" — {source.url}"
        lines.append(f"- **{source.label}:** {detail}")

    lines.extend(
        [
            "",
            "## PML implementation guarantees",
            "",
            "- PML1 element-creation commands only; no render prologue or PML2.",
            "- Every EQUI is anchored at `POS E 0 N 0 U 0`.",
            "- `ORI` precedes `POS` for CYLI, CONE and DISH.",
            "- Element-specific E3D datums are enforced centrally: CYLI/CONE/"
            "BOX centre; DISH rim/tangent plane.",
            "- Native NOZZLE elements are emitted CATR first, then flange-face "
            "POS, `ORI P1 IS <axis>` and HEIG; the generated values are parsed "
            "back and checked independently.",
            "- Off-axis rectangular support hardware is emitted with local X "
            "on its radial bearing and local Y tangent to the vessel; BOX "
            "orientation precedes POS and rotated bounds are parsed back.",
            "- One independent EQUI per equipment item and one SUBE per nozzle/"
            "manway assembly.",
            "- Blow Tank profile sections preserve the workbook's authoritative "
            "TOP-to-BOTTOM sequence and dimensions.",
            "",
            "Final visual acceptance still requires loading the macros in the "
            "user's AVEVA E3D project; numerical and syntax verification cannot "
            "substitute for that E3D review.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_composite_project(
    project: Project,
    models: Sequence[EquipmentModel],
    *,
    output_dir: Optional[Path] = None,
) -> CompositeGenerationResult:
    """Generate individual macros, one combined macro and the report."""
    individual = tuple(build_equipment_macro(model) for model in models)
    combined = build_combined_macro(models, project.name)
    verification: List[str] = []
    for model, macro in zip(models, individual):
        verification.extend(verify_equipment_macro(model, macro))
    for model in models:
        verification.extend(verify_equipment_macro(model, combined))

    report = build_composite_report(
        project,
        models,
        verification_problems=verification,
        output_dir=output_dir,
    )
    result = CompositeGenerationResult(
        models=models,
        individual_macros=individual,
        combined_macro=combined,
        report=report,
        verification_problems=tuple(verification),
    )

    if output_dir is None:
        return result

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    macro_paths = []
    for index, (model, macro) in enumerate(zip(models, individual), start=1):
        path = output_dir / f"{index:02d}_{model.name}.pml"
        path.write_text(macro, encoding="utf-8", newline="\n")
        macro_paths.append(path)

    combined_path = output_dir / f"{project.slug}.pml"
    combined_path.write_text(combined, encoding="utf-8", newline="\n")
    report_path = output_dir / f"{project.slug}_report.md"
    report_path.write_text(report, encoding="utf-8", newline="\n")

    result.macro_paths = tuple(macro_paths)
    result.combined_path = combined_path
    result.report_path = report_path
    return result
