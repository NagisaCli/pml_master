"""
JK Pump Batch Generation
========================

Generates one independent, one-EQUI PML macro per pump, a shared-builder
all-pumps macro for a complete register, and two project-level engineering
reports.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence

from .pml_builder import PMLBuilder, PMLValidationError, validate_pml
from .projects import Project, ProjectNotFoundError, resolve_project
from .pump_builder import (
    DerivedPumpGeometry,
    PumpBuilder,
    derive_detail_profile,
    verify_pump,
)
from .pump_schema import PumpSpec
from .schema import DataQualityException

__all__ = [
    "PumpFileResult",
    "PumpGenerationResult",
    "generate_pumps",
    "main",
]


@dataclass
class PumpFileResult:
    spec: PumpSpec
    geometry: DerivedPumpGeometry
    macro: str
    problems: List[str]
    primitive_count: int
    nozzle_count: int
    path: Optional[Path] = None

    @property
    def verified(self) -> bool:
        return not self.problems


@dataclass
class PumpGenerationResult:
    project: Project
    pumps: Sequence[PumpFileResult]
    combined_macro: str
    combined_problems: List[str]
    verification_report: str
    uncertainty_report: str
    combined_macro_path: Optional[Path] = None
    verification_report_path: Optional[Path] = None
    uncertainty_report_path: Optional[Path] = None

    @property
    def verified(self) -> bool:
        return (
            all(pump.verified for pump in self.pumps)
            and not self.combined_problems
        )


def _load_pumps(project: Project) -> Sequence[PumpSpec]:
    dataset = project.load_dataset()
    pumps = getattr(dataset, "PUMPS", None)
    if pumps is None:
        raise AttributeError(f"{project.dataset_path} defines no PUMPS register")
    return pumps


def _build_macro(project: Project, spec: PumpSpec) -> PumpFileResult:
    builder = PMLBuilder(spec.tag)
    builder.header(
        f"{spec.tag} - {spec.name}",
        meta=[
            ("Project", project.name),
            ("Equipment", spec.tag),
            ("Units", "mm"),
            ("Frame", "E = East, N = North, U = Up"),
            (
                "Datum",
                "Excel/client coordinate = geometric centre of baseplate underside",
            ),
            (
                "Orientation",
                f"Main axis {spec.layout_axis} from driver to casing; suction "
                f"{spec.suction_axis}; discharge {spec.discharge_axis}",
            ),
            ("Hierarchy", "Exactly one EQUI in this file"),
            ("Execution", "Select a writable ZONE, then $M <this file>"),
            ("Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ],
    )
    geometry = PumpBuilder(spec, builder).build()
    builder.catref_pass()
    builder.footer()
    macro = builder.build()
    problems = verify_pump(spec, macro)
    return PumpFileResult(
        spec=spec,
        geometry=geometry,
        macro=macro,
        problems=problems,
        primitive_count=builder.primitive_count,
        nozzle_count=builder.nozzle_count,
    )


def _duplicates(values: Sequence[str]) -> List[str]:
    """Return each duplicate value once, in deterministic order."""
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _equi_blocks(script: str) -> List[tuple[str, str]]:
    """Split a multi-equipment macro into its independent ``NEW EQUI`` blocks."""
    starts = list(
        re.finditer(r"(?m)^NEW EQUI /([A-Za-z0-9_]+)$", script)
    )
    blocks: List[tuple[str, str]] = []
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(script)
        blocks.append((match.group(1), script[match.start():end]))
    return blocks


def _verify_combined_macro(
    specs: Sequence[PumpSpec],
    script: str,
) -> List[str]:
    """
    Verify the combined macro structurally and pump-by-pump.

    ``verify_pump`` intentionally accepts one EQUI only, so the combined text is
    split at each ``NEW EQUI`` and each block is checked independently. This
    preserves the same numerical baseplate, footprint and orientation checks
    used for the standalone files.
    """
    problems = list(validate_pml(script))
    expected_equis = [spec.safe_tag for spec in specs]
    actual_equis = re.findall(
        r"(?m)^NEW EQUI /([A-Za-z0-9_]+)$",
        script,
    )
    if actual_equis != expected_equis:
        problems.append(
            "Combined macro EQUI order/names differ from the selected pump "
            f"register: expected {expected_equis}, got {actual_equis}"
        )
    duplicate_equis = _duplicates(actual_equis)
    if duplicate_equis:
        problems.append(
            f"Combined macro has duplicate EQUI names: {duplicate_equis}"
        )

    anchored_equis = re.findall(
        r"(?m)^NEW EQUI /([A-Za-z0-9_]+)\n"
        r"POS E 0\.0 N 0\.0 U 0\.0$",
        script,
    )
    if anchored_equis != expected_equis:
        problems.append(
            "Every combined EQUI must be immediately anchored at "
            "'POS E 0.0 N 0.0 U 0.0'; "
            f"anchored in order: {anchored_equis}"
        )

    expected_nozzles = [
        name
        for spec in specs
        for name in (
            f"{spec.safe_tag}_SUCTION_NOZZLE",
            f"{spec.safe_tag}_DISCHARGE_NOZZLE",
        )
    ]
    actual_nozzles = re.findall(
        r"(?m)^NEW NOZZLE /([A-Za-z0-9_]+)$",
        script,
    )
    if actual_nozzles != expected_nozzles:
        problems.append(
            "Combined macro NOZZLE order/names differ from the selected pump "
            f"register: expected {expected_nozzles}, got {actual_nozzles}"
        )
    duplicate_nozzles = _duplicates(actual_nozzles)
    if duplicate_nozzles:
        problems.append(
            f"Combined macro has duplicate NOZZLE names: {duplicate_nozzles}"
        )

    named_elements = re.findall(
        r"(?m)^NEW (?:EQUI|SUBE|NOZZLE) /([A-Za-z0-9_]+)$",
        script,
    )
    duplicate_elements = _duplicates(named_elements)
    if duplicate_elements:
        problems.append(
            "Combined macro has duplicate named structural elements: "
            f"{duplicate_elements}"
        )

    catref_count = len(
        re.findall(r"(?m)^CATR SPCOMPONENT /[^\s]+$", script)
    )
    if catref_count != len(expected_nozzles):
        problems.append(
            "Combined macro must bind every native nozzle inline: expected "
            f"{len(expected_nozzles)} CATR SPCOMPONENT commands, got "
            f"{catref_count}"
        )

    blocks = _equi_blocks(script)
    block_names = [name for name, _block in blocks]
    if block_names != expected_equis:
        problems.append(
            "Combined macro could not be split into the expected ordered EQUI "
            f"blocks: expected {expected_equis}, got {block_names}"
        )

    blocks_by_name: dict[str, List[str]] = {}
    for name, block in blocks:
        blocks_by_name.setdefault(name, []).append(block)
    for spec in specs:
        matching = blocks_by_name.get(spec.safe_tag, [])
        if len(matching) != 1:
            problems.append(
                f"{spec.tag}: expected exactly one combined EQUI block, "
                f"found {len(matching)}"
            )
            continue
        for problem in verify_pump(spec, matching[0]):
            problems.append(f"Combined EQUI block: {problem}")

    return problems


def _build_combined_macro(
    project: Project,
    results: Sequence[PumpFileResult],
) -> tuple[str, List[str]]:
    """
    Build all selected pumps with one shared builder.

    Geometry is regenerated from the authoritative specs rather than spliced
    from files on disk. The shared builder extends EQUI/SUBE duplicate detection
    across the whole batch and produces one truthful header, catalogue summary
    and footer.
    """
    builder = PMLBuilder(f"{project.slug}_All_Pumps")
    builder.header(
        f"{project.name} - ALL SELECTED PUMPS",
        meta=[
            ("Project", project.name),
            ("Scope", f"{len(results)} pump equipment items"),
            ("Units", "mm"),
            ("Frame", "E = East, N = North, U = Up"),
            (
                "Datum",
                "Each coordinate is the geometric centre of its baseplate underside",
            ),
            (
                "Hierarchy",
                f"{len(results)} independent EQUI elements; one EQUI per pump tag",
            ),
            (
                "Execution",
                "Select a writable ZONE, then $M <this combined file>",
            ),
            ("Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ],
    )
    for result in results:
        builder.banner(f"{result.spec.tag} - {result.spec.name}")
        PumpBuilder(result.spec, builder).build()
    builder.catref_pass()
    builder.footer()
    macro = builder.build()
    return macro, _verify_combined_macro(
        [result.spec for result in results],
        macro,
    )


def _fmt_position(position: tuple[float, float, float]) -> str:
    return f"({position[0]:.0f}, {position[1]:.0f}, {position[2]:.0f})"


def _build_verification_report(
    project: Project,
    results: Sequence[PumpFileResult],
    exceptions: Sequence[DataQualityException],
    combined_problems: Sequence[str],
    combined_macro_path: Optional[Path],
    full_register: bool,
) -> str:
    combined_status = "PASS" if not combined_problems else "FAIL"
    if combined_macro_path is not None:
        combined_file = f"`{combined_macro_path}`"
    elif full_register and combined_problems:
        combined_file = "(not written because combined validation failed)"
    elif full_register:
        combined_file = "(dry run — validated in memory, not written)"
    else:
        combined_file = (
            "(filtered selection — the formal all-pumps file was not overwritten)"
        )
    lines = [
        f"# {project.name} — Pump Modeling Verification Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Verification scope",
        "",
        "- One independent PML file per pump.",
        "- Exactly one E3D `EQUI` hierarchy in each file.",
        "- One combined macro is built directly through a shared `PMLBuilder`,",
        "  with one independent `EQUI` per selected pump and no disk-file splicing.",
        "- Baseplate dimensions and 50 mm thickness checked numerically.",
        "- Baseplate underside centre checked against the project coordinate.",
        "- Suction direction, motor-opposite arrangement and discharge direction checked.",
        "- Contractual coordinates, baseplate dimensions and directions remain unchanged",
        "  by the high-detail construction pass.",
        "- Detailed hierarchy, seated base/driver and flange-face casing fasteners,",
        "  coupling guard, finned motor and service-specific features checked.",
        "- Primitive footprint checked against the rectangular baseplate.",
        "- PML1 banned syntax, primitive ORI/POS order and NOZZLE catalogue order checked.",
        "- The client loaded and visually accepted the current combined macro in E3D",
        "  on 2026-07-29; future changes remain subject to a new visual reload.",
        "",
        "## Summary",
        "",
        f"- Pumps generated: **{len(results)}**",
        f"- Static verification passed: **{sum(r.verified for r in results)}**",
        f"- Static verification failed: **{sum(not r.verified for r in results)}**",
        f"- Total primitives: **{sum(r.primitive_count for r in results)}**",
        f"- Native catalogue nozzles: **{sum(r.nozzle_count for r in results)}**",
        f"- Combined macro static/numerical validation: **{combined_status}**",
        f"- One-click combined load file: {combined_file}",
        "",
    ]
    if combined_problems:
        lines.extend(
            [
                "### Combined macro validation problems",
                "",
                *[f"- {problem}" for problem in combined_problems],
                "",
            ]
        )
    lines.extend(
        [
            "## Pump-by-pump results",
            "",
            "| Excel row | Pump tag | Family | Duty/detail basis | Position — baseplate underside centre (mm) | Baseplate L × W × T (mm) | Main axis driver→casing | Suction | Discharge | Primitives | Drawing | Generated file | Validation |",
            "|---:|---|---|---|---|---:|---|---|---|---:|---|---|---|",
        ]
    )
    for result in results:
        spec = result.spec
        drawing = spec.top_view or "**UNCONFIRMED — no reference**"
        file_path = str(result.path) if result.path else "(dry run)"
        validation = (
            "PASS — static/numerical"
            if result.verified
            else "FAIL — " + "; ".join(result.problems)
        )
        detail = derive_detail_profile(spec, result.geometry)
        lines.append(
            f"| {spec.excel_row} | {spec.tag} | {spec.family.value} | "
            f"{spec.duty.value}; `{detail.signature}` | "
            f"{_fmt_position(spec.position)} | "
            f"{spec.length:.0f} × {spec.width:.0f} × "
            f"{spec.baseplate_thickness:.0f} | {spec.layout_axis} | "
            f"{spec.suction_axis} | {spec.discharge_axis} | "
            f"{result.primitive_count} | {drawing} | "
            f"`{file_path}` | {validation} |"
        )

    lines.extend(
        [
            "",
            "## Modeling parameters and Reference Values",
            "",
            "The following values are not vendor GA data. They are explicit Reference",
            "Values scaled from each contractual baseplate and retained in the data/model",
            "report so they can be replaced when vendor documents are issued.",
            "",
            "| Pump tag | Shaft CL above datum (mm) | Casing Ø × axial length (mm) | Motor L × W × H (mm) | Suction DN / length (mm) | Discharge DN / length (mm) | Approx. overall height (mm) |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for result in results:
        spec, geom = result.spec, result.geometry
        lines.append(
            f"| {spec.tag} | {geom.shaft_u:.1f} | "
            f"{geom.casing_diameter:.1f} × {geom.casing_length:.1f} | "
            f"{geom.motor_length:.1f} × {geom.motor_width:.1f} × "
            f"{geom.motor_height:.1f} | DN{geom.suction_dn} / "
            f"{geom.suction_length:.1f} | DN{geom.discharge_dn} / "
            f"{geom.discharge_length:.1f} | {geom.overall_height:.1f} |"
        )

    lines.extend(
        [
            "",
            "Common Reference Values:",
            "",
            "- Driver frame, cooling fins, coupling, guard, skid rails and support feet",
            "  are engineering-proportional geometry, not vendor-confirmed dimensions.",
            "- Exposed anchor/motor fasteners use a three-piece visual envelope:",
            "  filled shank, solid washer around that shank, and cap/hex-head envelope.",
            "  Exact thread pitch, head flats and manufacturer are UNCONFIRMED.",
            "- Motor fin counts are deterministic S/M/L/XL Reference Value tiers,",
            "  not counts measured from the small plan images. Motor ribs run axially",
            "  around the complete 360-degree stator circumference.",
            "- Casing-bolt count tiers are deterministic Reference Values. Their",
            "  centres lie on the protruding cylinder/cone connection-flange band;",
            "  washers bear on its front face and studs penetrate back into it.",
            "- Terminal boxes use a centred top mount where the plan does not prove an",
            "  offset. Cable-gland side, skid cross-members and other small details",
            "  remain bounded Reference Values.",
            "- Volute split flange, casing ribs, back-pull-out bearing bracket, seal",
            "  housing, flexible coupling, guard bands, fan grille, cable gland,",
            "  lifting lug and rating plate are visible engineering-level details.",
            "- Standard horizontal pumps use a single-stage horizontal centrifugal",
            "  back-pull-out arrangement with a volute casing, coupling and TEFC motor.",
            "- Duty-specific external details are differentiated for dilution, filtrate,",
            "  stock/screen feed, booster, wire-wash, washer-feed, MC and scrubber",
            "  circulation services. These classifications come from the supplied names.",
            "- 205-PU-018 and 205-PU-038 are client-confirmed exceptions: their",
            "  driver/casing axis runs E-W (driver east, casing west), while suction",
            "  points S and discharge points W at the same centreline elevation.",
            "- MC pumps add a side degassing/separation assembly and four casing support",
            "  feet. This structural choice is supported by ANDRITZ's published MC-pump",
            "  description of an integrated separation system and a volute with four",
            "  supporting legs.",
            "- Suction/discharge source openings come from pump_nozzle_modify.xlsx;",
            "  each is mapped to the nearest verified catalogue DN and documented.",
            "",
            "Vendor structural references:",
            "",
            "- [ANDRITZ medium-consistency pumps](https://www.andritz.com/products-en/group/pumps/medium-consistency)",
            "- [ANDRITZ pumps for pulp and paper brochure](https://www.andritz.com/resource/blob/699140/af345d60b77d727f79091e1722dae332/hy-andritz-pumps-pulp-paper-brochure-en-data.pdf)",
            "- [Valmet medium-consistency pumps](https://www.valmet.com/pulp/mechanical-pulping/bleaching/pumps/)",
            "",
            "## Client-confirmed source corrections",
            "",
        ]
    )
    for exception in exceptions:
        lines.append(
            f"- **{exception.tag} — {exception.field_name}:** "
            f"`{exception.source_value}` → `{exception.corrected_value}`. "
            f"Basis: {exception.rationale}"
        )

    lines.extend(
        [
            "",
            "## Load instruction",
            "",
        ]
    )
    if full_register and not combined_problems:
        combined_load = (
            str(combined_macro_path)
            if combined_macro_path is not None
            else f"<output>/{project.slug}_All_Pumps.pml"
        )
        lines.extend(
            [
                "To create all pumps in one operation, select a writable ZONE in",
                "AVEVA E3D Design and load the combined macro:",
                "",
                "```text",
                f"$M {combined_load}",
                "```",
                "",
            ]
        )
    elif full_register:
        lines.extend(
            [
                "The combined macro failed static validation and was not written.",
                "Resolve the listed combined-macro problems before loading it in E3D.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "This was a filtered pump selection. The canonical all-pumps macro",
                "was deliberately not written or overwritten.",
                "",
            ]
        )
    lines.extend(
        [
            "To load an individual pump, select a writable ZONE and run:",
            "",
            "```text",
            "$M <full path to the pump .pml file>",
            "```",
            "",
            "A PASS in this report means static PML1 and numerical geometry checks",
            "passed. It does **not** claim the macro was interactively loaded in E3D.",
            "",
        ]
    )
    return "\n".join(lines)


def _build_uncertainty_report(
    project: Project, results: Sequence[PumpFileResult]
) -> str:
    missing_drawings = [r.spec.tag for r in results if not r.spec.top_view]
    special_notes = [
        (r.spec.tag, note) for r in results for note in r.spec.notes
    ]
    lines = [
        f"# {project.name} — Uncertainty and Outstanding-Issue Report",
        "",
        "## UNCONFIRMED",
        "",
        "- **E3D interactive execution:** UNCONFIRMED. The macros passed static and",
        "  numerical verification only; the user must load them in the receiving E3D",
        "  project before they can be called E3D-verified.",
        "- **Vendor dimensions and performance data:** UNCONFIRMED. No vendor GA,",
        "  motor schedule, pump model, shaft elevation or nozzle schedule was supplied.",
        "- **Nozzle catalogue portability:** UNCONFIRMED outside the current receiving",
        "  catalogue. The generated `CATR SPCOMPONENT` paths use the project's verified",
        "  `150lb_Ansi_Flanged` mapping and must be re-queried for another catalogue.",
        "- **Materials, mass, maintenance envelope, anchor bolts and design conditions:**",
        "  UNCONFIRMED. Visible anchor and hold-down fasteners are modeled as bounded",
        "  Reference Values, but their grade, thread and embedment are not claimed.",
        "- **High-detail dimensions:** UNCONFIRMED. Bolt sizes/counts, motor frame,",
        "  cooling-fin tier, cable-gland side, bearing bracket, seal housing, coupling",
        "  hardware and service accessories are engineering Reference Values derived",
        "  from duty, skid scale and the available top-view outlines.",
        "",
        "## Missing top-view references",
        "",
    ]
    lines.extend(f"- {tag}" for tag in missing_drawings)
    lines.extend(
        [
            "",
            "These pumps use a same-family structural model scaled only to their own",
            "contractual baseplate and confirmed directions; no dimensions were copied",
            "from `Horizontal_Pump_Example.txt`.",
            "",
            "## Tag-specific notes",
            "",
        ]
    )
    lines.extend(f"- **{tag}:** {note}" for tag, note in special_notes)
    lines.extend(
        [
            "",
            "## Resolved items",
            "",
            "- 205-PU-046 position is confirmed as `(45221, 14294, 0)` mm.",
            "- 205-PU-061 position is confirmed as `(46154, -8256, 0)` mm.",
            "- Baseplate thickness is confirmed as 50 mm for every pump.",
            "- Each pump is confirmed to require its own independent EQUI hierarchy.",
            "- 205-PU-018 and 205-PU-038 are confirmed as E-W main-axis special",
            "  arrangements with coplanar S and W nozzles.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_pumps(
    pumps: Optional[Sequence[PumpSpec]] = None,
    *,
    project: Optional[Project] = None,
    output_dir: Optional[Path] = None,
) -> PumpGenerationResult:
    """Generate, verify and optionally write every selected pump."""
    if project is None:
        project = resolve_project("JK_Pump_Build")
    register = tuple(_load_pumps(project))
    if pumps is None:
        pumps = register
    else:
        pumps = tuple(pumps)

    results = [_build_macro(project, spec) for spec in pumps]
    combined_macro, combined_problems = _build_combined_macro(project, results)
    dataset = project.load_dataset()
    exceptions = getattr(dataset, "DATA_QUALITY_EXCEPTIONS", ())
    selected_tags = [spec.tag for spec in pumps]
    register_tags = [spec.tag for spec in register]
    # Only the authoritative full register in its canonical order may replace
    # the formal all-pumps delivery.  A reordered/all-tag CLI selection is
    # still an ad-hoc filtered run and must not silently rewrite that file.
    full_register = selected_tags == register_tags

    combined_macro_path: Optional[Path] = None
    if output_dir is not None:
        output_dir = Path(output_dir)
        pumps_dir = output_dir / "pumps"
        pumps_dir.mkdir(parents=True, exist_ok=True)
        for result in results:
            result.path = pumps_dir / f"{result.spec.tag}.pml"
        if full_register and not combined_problems:
            combined_macro_path = (
                output_dir / f"{project.slug}_All_Pumps.pml"
            )

    verification_report = _build_verification_report(
        project,
        results,
        exceptions,
        combined_problems,
        combined_macro_path,
        full_register,
    )
    uncertainty_report = _build_uncertainty_report(project, results)
    generation = PumpGenerationResult(
        project=project,
        pumps=results,
        combined_macro=combined_macro,
        combined_problems=combined_problems,
        verification_report=verification_report,
        uncertainty_report=uncertainty_report,
        combined_macro_path=combined_macro_path,
    )

    if output_dir is not None:
        for result in results:
            result.path.write_text(
                result.macro,
                encoding="utf-8",
                newline="\n",
            )
        if generation.combined_macro_path is not None:
            generation.combined_macro_path.write_text(
                combined_macro,
                encoding="utf-8",
                newline="\n",
            )
        generation.verification_report_path = (
            Path(output_dir) / f"{project.slug}_verification_report.md"
        )
        generation.uncertainty_report_path = (
            Path(output_dir) / f"{project.slug}_uncertainty_report.md"
        )
        generation.verification_report_path.write_text(
            verification_report, encoding="utf-8", newline="\n"
        )
        generation.uncertainty_report_path.write_text(
            uncertainty_report, encoding="utf-8", newline="\n"
        )

    return generation


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m wsb.pump_generate",
        description=(
            "Generate one independent AVEVA E3D PML macro per pump and, for "
            "the complete register, one combined all-pumps macro."
        ),
    )
    parser.add_argument("-p", "--project", default="JK_Pump_Build")
    parser.add_argument("-t", "--tag", action="append", dest="tags")
    parser.add_argument("-o", "--output-dir", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        project = resolve_project(args.project)
        register = tuple(_load_pumps(project))
        if args.tags:
            by_tag = {pump.tag: pump for pump in register}
            pumps = tuple(by_tag[tag] for tag in args.tags)
        else:
            pumps = register
        result = generate_pumps(
            pumps,
            project=project,
            output_dir=None
            if args.dry_run
            else (args.output_dir or project.output_dir),
        )
    except (ProjectNotFoundError, AttributeError, KeyError, PMLValidationError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"Project            : {project.name}")
    print(f"Pumps generated    : {len(result.pumps)}")
    print(f"Independent EQUIs  : {len(result.pumps)}")
    print(f"Primitives         : {sum(r.primitive_count for r in result.pumps)}")
    print(f"Native nozzles     : {sum(r.nozzle_count for r in result.pumps)}")
    print(
        "Static verification: "
        + ("PASS" if result.verified else "FAIL")
    )
    for pump in result.pumps:
        if not pump.verified:
            for problem in pump.problems:
                print(f"  - {problem}", file=sys.stderr)
    print(
        "Combined validation: "
        + ("PASS" if not result.combined_problems else "FAIL")
    )
    for problem in result.combined_problems:
        print(f"  - {problem}", file=sys.stderr)
    if args.dry_run:
        print("Dry run            : no files written")
    else:
        print(f"Output             : {args.output_dir or project.output_dir}")
        if result.combined_macro_path is not None:
            print(
                "One-click macro    : "
                f"{result.combined_macro_path}"
            )
            print(
                "E3D load command   : "
                f"$M {result.combined_macro_path}"
            )
        elif args.tags:
            print(
                "One-click macro    : unchanged (filtered --tag selection)"
            )
        else:
            print("One-click macro    : not written (validation failed)")
    return 0 if result.verified else 1


if __name__ == "__main__":
    raise SystemExit(main())
