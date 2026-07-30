"""
WSB Model Generation Pipeline
=============================
Ties the dataset, geometry builder, validator and report together into the one
command that produces the deliverables.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence

from .pml_builder import PMLBuilder, PMLValidationError
from .projects import (
    PROJECTS_DIR,
    Project,
    ProjectNotFoundError,
    discover_projects,
    resolve_project,
)
from .report import build_report
from .schema import TankSpec
from .tank_builder import TankBuilder, verify_bottom_centre

__all__ = ["GenerationResult", "generate", "main"]

#: Label for the macro header, derived from the project name. Each tank opens its
#: own EQUI named after its tag, so this is documentation only and creates no
#: element.


@dataclass
class GenerationResult:
    """Outcome of a generation run."""

    macro: str
    report: str
    tanks: Sequence[TankSpec]
    primitive_count: int
    verification_problems: List[str]
    macro_path: Optional[Path] = None
    report_path: Optional[Path] = None

    @property
    def verified(self) -> bool:
        """True when every tank's bottom centre matched its listed coordinate."""
        return not self.verification_problems


def generate(
    tanks: Optional[Sequence["TankSpec"]] = None,
    *,
    project: Optional[Project] = None,
    output_dir: Optional[Path] = None,
    timestamp: bool = True,
) -> GenerationResult:
    """
    Generate the PML macro and engineering report for a project.

    Args:
        tanks: Tanks to model. Defaults to the project's full register.
        project: Project supplying the dataset and the output naming. Defaults
            to the sole project under ``Projects/``.
        output_dir: Where to write the deliverables. Defaults to the project's
            own ``output/`` folder; pass ``None`` with ``write=False`` semantics
            by using :func:`generate` without an output directory to keep the
            run in memory.
        timestamp: Append a timestamp to the filenames, keeping successive runs
            side by side rather than overwriting.

    Returns:
        The generated macro, report and verification outcome.

    Raises:
        PMLValidationError: if the assembled macro violates a PML1 rule.
        ProjectNotFoundError: if no project can be resolved.
    """
    if project is None:
        project = resolve_project()
    if tanks is None:
        tanks = project.tanks()

    builder = PMLBuilder(project.slug)
    builder.header(
        "PULP MILL - WASHING, SCREENING & BLEACHING (WSB) AREA",
        meta=[
            ("Project", project.name),
            ("Scope", f"{len(tanks)} tank-type equipment items"),
            ("Units", "mm"),
            ("Frame", "E = East, N = North, U = Up (elevation)"),
            ("Datum", "Each tank is positioned by its BOTTOM CENTRE POINT"),
            ("Source", f"Projects/{project.name}/ equipment list + drawings"),
            ("Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            # The macro-run command is `$M <path>`, not `$$MACRO <path>`.
            # `$$MACRO` appears nowhere in AVEVA's installed library (0 hits
            # across ~6900 files in PMLLIB and PMLUI); `$M <path>` appears
            # throughout, e.g. abaloadsymbols.pmlfnc `$M $!file`. Running
            # `$$MACRO` aborts with "(47,50) CP: Meaningless symbol(s)".
            ("Execution", "Select a writable ZONE in E3D, then $M <this file>"),
        ],
    )

    for spec in tanks:
        TankBuilder(spec, builder).build()

    # Catalogue binding for every nozzle created above. A NOZZLE draws nothing
    # until an SPCO component is bound to it, and the binding is a separate pass
    # keyed by name - it cannot go inside the NEW NOZZLE block.
    builder.catref_pass()

    builder.footer()
    macro = builder.build()

    problems: List[str] = []
    for spec in tanks:
        problems.extend(verify_bottom_centre(spec, macro))

    result = GenerationResult(
        macro=macro,
        report="",
        tanks=tanks,
        primitive_count=builder.primitive_count,
        verification_problems=problems,
    )

    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        # Deliverables are named after the project, so a macro found later can be
        # traced back to the folder that produced it and reopened without
        # guesswork. The stem is the project slug even when the caller overrides
        # the directory.
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S") if timestamp else None
        suffix = f"_{stamp}" if stamp else ""
        result.macro_path = output_dir / f"{project.slug}{suffix}.pml"
        result.report_path = output_dir / f"{project.slug}{suffix}_report.md"

    # Which source-data defects exist is project data, so the project supplies
    # them rather than the report importing a global.
    exceptions = getattr(
        project.load_dataset(), "DATA_QUALITY_EXCEPTIONS", ()
    )

    result.report = build_report(
        tanks,
        macro_path=str(result.macro_path) if result.macro_path else "",
        primitive_count=builder.primitive_count,
        verification_problems=problems,
        data_quality_exceptions=exceptions,
    )

    if result.macro_path is not None:
        # newline="\n" keeps the macro LF-terminated: E3D's macro reader is
        # sensitive to stray CR characters on Windows.
        result.macro_path.write_text(macro, encoding="utf-8", newline="\n")
        result.report_path.write_text(result.report, encoding="utf-8", newline="\n")

    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        prog="python -m wsb",
        description="Generate AVEVA E3D models for WSB area tank equipment.",
    )
    parser.add_argument(
        "-p", "--project", metavar="NAME",
        help="Project under Projects/ to model. Defaults to the only one "
             "present; required when there are several.",
    )
    parser.add_argument(
        "--list-projects", action="store_true",
        help="List the projects under Projects/ and exit",
    )
    parser.add_argument(
        "-o", "--output-dir", type=Path, default=None,
        help="Directory for the deliverables (default: the project's output/)",
    )
    parser.add_argument(
        "-t", "--tag", action="append", dest="tags", metavar="TAG",
        help="Model only this tag; repeatable. Defaults to every tank in the "
             "project register.",
    )
    parser.add_argument(
        "--no-timestamp", action="store_true",
        help="Write to fixed filenames instead of timestamped ones",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Validate and report without writing any files",
    )
    args = parser.parse_args(argv)

    if args.list_projects:
        projects = discover_projects()
        if not projects:
            print(f"No projects found under {PROJECTS_DIR}", file=sys.stderr)
            return 2
        for entry in projects:
            marks = []
            if entry.do_file:
                marks.append(entry.do_file.name)
            if entry.dataset_path:
                marks.append("dataset")
            print(f"{entry.name:<24} {', '.join(marks) or 'no data'}")
        return 0

    try:
        project = resolve_project(args.project)
    except ProjectNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    try:
        register = project.tanks()
    except (AttributeError, ProjectNotFoundError, ImportError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # Composite projects resolve their geometry up front as generic primitive
    # assemblies.  They use the same project registry and PMLBuilder, but need
    # one macro per equipment item and a bounds-based verifier rather than the
    # original single-shell TankSpec pipeline.
    from .composite_schema import EquipmentModel

    if register and all(isinstance(item, EquipmentModel) for item in register):
        from .composite_generate import generate_composite_project

        models = tuple(register)
        if args.tags:
            lookup = {}
            for model in models:
                lookup[model.name] = model
                lookup[model.display_name] = model
            try:
                models = tuple(lookup[tag] for tag in args.tags)
            except KeyError as exc:
                print(
                    f"error: no equipment named {exc} in project "
                    f"'{project.name}'",
                    file=sys.stderr,
                )
                return 2

        output_dir = args.output_dir or project.output_dir
        try:
            result = generate_composite_project(
                project,
                models,
                output_dir=None if args.dry_run else output_dir,
            )
        except (PMLValidationError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

        print(f"Project            : {project.name}")
        print(f"Equipment modelled : {len(result.models)}")
        print(f"Primitives         : {result.primitive_count}")
        print(f"Nozzle groups      : {result.nozzle_count}")
        if result.verified:
            print("Positioning        : verified - all numeric bounds match")
        else:
            print("Positioning        : FAILED")
            for problem in result.verification_problems:
                print(f"  - {problem}", file=sys.stderr)
        if result.combined_path:
            print(f"Combined macro     : {result.combined_path}")
            print(f"Individual macros  : {len(result.macro_paths)}")
            print(f"Report             : {result.report_path}")
        else:
            print("Dry run            : no files written")
        return 0 if result.verified else 1

    if args.tags:
        by_tag = {spec.tag: spec for spec in register}
        try:
            tanks = tuple(by_tag[tag] for tag in args.tags)
        except KeyError as exc:
            print(
                f"error: no equipment tagged {exc} in project '{project.name}'",
                file=sys.stderr,
            )
            return 2
    else:
        tanks = register

    output_dir = args.output_dir or project.output_dir

    try:
        result = generate(
            tanks,
            project=project,
            output_dir=None if args.dry_run else output_dir,
            timestamp=not args.no_timestamp,
        )
    except PMLValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Project            : {project.name}")
    print(f"Equipment modelled : {len(result.tanks)}")
    print(f"Primitives         : {result.primitive_count}")
    print(f"Nozzles            : {sum(len(t.nozzles) for t in result.tanks)}")

    if result.verified:
        print("Positioning        : verified - all bottom centre points match")
    else:
        print("Positioning        : FAILED")
        for problem in result.verification_problems:
            print(f"  - {problem}", file=sys.stderr)

    if result.macro_path:
        print(f"Macro              : {result.macro_path}")
        print(f"Report             : {result.report_path}")
    else:
        print("Dry run            : no files written")

    return 0 if result.verified else 1


if __name__ == "__main__":
    raise SystemExit(main())
