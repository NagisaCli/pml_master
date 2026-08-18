"""
Batch driver.
=============

Runs the whole pipeline over a directory of pump JSON files.  Every pump
is isolated: a failure is caught, logged with enough context to debug it
later, and the batch continues.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import traceback
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from wsb.pml_builder import validate_pml

from .audit import Validation, render_audit, validate
from .build import PumpBuild, build_pump, render_pml
from .semantic import PumpSemanticModel, ViewType, build_semantic_model
from .source import PumpRecord, load_all

__all__ = ["PumpOutcome", "run_batch", "main"]


@dataclass
class PumpOutcome:
    """What happened to one pump."""

    tag: str
    ok: bool
    view: str = "unknown"
    pml_path: Optional[str] = None
    audit_path: Optional[str] = None
    validation: Optional[Validation] = None
    error: Optional[str] = None
    traceback: Optional[str] = None
    #: The rendered macro, kept so the combined file can reuse it verbatim.
    script: Optional[str] = None

    @property
    def status(self) -> str:
        if not self.ok:
            return "ERROR"
        if self.validation is not None and not self.validation.passed:
            return "CHECK"
        return "OK"


def _process(
    record: PumpRecord, out_dir: str, generated: str
) -> PumpOutcome:
    model: PumpSemanticModel = build_semantic_model(record)
    build: PumpBuild = build_pump(record, model)
    result = validate(record, model, build)

    script = render_pml(build, generated=generated)
    problems = validate_pml(script)
    if problems:
        result.record(
            "PML passes syntax validation",
            False,
            "; ".join(problems[:3]),
        )
    else:
        result.record("PML passes syntax validation", True, "no banned constructs")

    pml_dir = os.path.join(out_dir, "pumps")
    audit_dir = os.path.join(out_dir, "audit")
    os.makedirs(pml_dir, exist_ok=True)
    os.makedirs(audit_dir, exist_ok=True)

    pml_path = os.path.join(pml_dir, f"{record.tag}.pml")
    audit_path = os.path.join(audit_dir, f"{record.tag}.txt")
    with open(pml_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(script)
    with open(audit_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(render_audit(record, model, build, result))

    return PumpOutcome(
        tag=record.tag,
        ok=True,
        view=model.view.value,
        pml_path=pml_path,
        audit_path=audit_path,
        validation=result,
        script=script,
    )


def run_batch(source_dir: str, out_dir: str) -> List[PumpOutcome]:
    """Reconstruct every pump in ``source_dir``.

    One malformed pump never stops the batch (brief section 23).
    """
    generated = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    records, failures = load_all(source_dir)

    outcomes: List[PumpOutcome] = []
    for path, message in failures:
        outcomes.append(
            PumpOutcome(
                tag=os.path.splitext(os.path.basename(path))[0],
                ok=False,
                error=f"could not load: {message}",
            )
        )

    for record in records:
        try:
            outcomes.append(_process(record, out_dir, generated))
        except Exception as exc:  # noqa: BLE001 - batch isolation is required
            outcomes.append(
                PumpOutcome(
                    tag=record.tag,
                    ok=False,
                    error=f"{type(exc).__name__}: {exc}",
                    traceback=traceback.format_exc(),
                )
            )

    _write_summary(outcomes, out_dir, generated)
    _write_combined(outcomes, out_dir, generated)
    return outcomes


def _write_combined(
    outcomes: List[PumpOutcome], out_dir: str, generated: str
) -> None:
    """Write every pump into one macro.

    The per-pump files stay as they are; this is an additional artefact for
    loading the whole package in a single ``$M``.  Each pump keeps its own
    ``EQUI``, so the combined file is simply the macros in tag order under
    one header - no renaming, no merging of elements.
    """
    built = [o for o in outcomes if o.script]
    if not built:
        return

    lines: List[str] = []
    add = lines.append
    add("-- " + "=" * 68)
    add("-- JK_Pump_Build - all pumps (pumpcad reconstruction)")
    add("-- " + "=" * 68)
    add("-- Units: mm")
    add("-- Frame: E = East, N = North, U = Up")
    add("-- Datum: metadata coordinate = geometric centre of baseplate underside")
    add(f"-- Pumps in this file: {len(built)}")
    add(f"-- Generated: {generated}")
    add("--")
    add("-- Each pump is a separate EQUI, in tag order:")
    for outcome in built:
        add(f"--   {outcome.tag}  ({outcome.view})")
    add("--")
    add("-- Execution: select a writable ZONE, then $M <this file>")
    add("-- The per-pump macros in pumps\\ remain available for loading one")
    add("-- pump at a time; this file is the same content concatenated.")
    add("-- " + "=" * 68)
    add("")

    for outcome in built:
        assert outcome.script is not None
        # Drop each macro's own banner block; the header above replaces it.
        body = [
            line
            for line in outcome.script.splitlines()
            if not line.startswith("-- =")
            # These two lines describe a standalone macro and would be
            # misleading here: this file holds 30 EQUI, and is loaded once.
            and not line.startswith("-- Hierarchy: Exactly one EQUI")
            and not line.startswith("-- Execution:")
        ]
        add("")
        add("-- " + "-" * 68)
        add(f"-- {outcome.tag}")
        add("-- " + "-" * 68)
        lines.extend(body)

    script = "\n".join(lines).rstrip() + "\n"

    # Concatenation can introduce defects the per-pump files do not have
    # (a stray END, a duplicated element name), so the combined file is
    # validated in its own right rather than trusted by construction.
    problems = validate_pml(script)
    names = re.findall(r"^NEW EQUI (/\S+)", script, flags=re.MULTILINE)
    duplicates = {name for name in names if names.count(name) > 1}
    if duplicates:
        problems.append(
            f"duplicate EQUI name(s) in the combined file: "
            f"{', '.join(sorted(duplicates))}"
        )
    if len(names) != len(built):
        problems.append(
            f"combined file has {len(names)} EQUI but {len(built)} pumps were built"
        )

    path = os.path.join(out_dir, "JK_Pump_Build_All_Pumps.pml")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(script)

    if problems:
        report = os.path.join(out_dir, "JK_Pump_Build_All_Pumps_PROBLEMS.txt")
        with open(report, "w", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(problems) + "\n")


def _write_summary(
    outcomes: List[PumpOutcome], out_dir: str, generated: str
) -> None:
    os.makedirs(out_dir, exist_ok=True)
    lines: List[str] = []
    add = lines.append

    ok = [o for o in outcomes if o.status == "OK"]
    check = [o for o in outcomes if o.status == "CHECK"]
    errors = [o for o in outcomes if o.status == "ERROR"]

    add("# pumpcad batch report")
    add("")
    add(f"Generated: {generated}")
    add("")
    add(f"- pumps processed: {len(outcomes)}")
    add(f"- fully validated: {len(ok)}")
    add(f"- built with check failures: {len(check)}")
    add(f"- failed: {len(errors)}")
    add("")
    add("| Pump | View | Status | Notes |")
    add("| --- | --- | --- | --- |")
    for outcome in outcomes:
        if outcome.error:
            note = outcome.error
        elif outcome.validation and outcome.validation.failures:
            note = "; ".join(name for name, _, _ in outcome.validation.failures)
        else:
            note = "all checks passed"
        add(f"| {outcome.tag} | {outcome.view} | {outcome.status} | {note} |")

    if errors:
        add("")
        add("## Failures")
        for outcome in errors:
            add("")
            add(f"### {outcome.tag}")
            add("```")
            add(outcome.traceback or outcome.error or "unknown")
            add("```")

    path = os.path.join(out_dir, "pumpcad_batch_report.md")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reconstruct pumps from CAD-derived JSON linework."
    )
    parser.add_argument(
        "--source",
        default=r"C:\Users\A\Desktop\pumps",
        help="directory containing the pump JSON exports",
    )
    parser.add_argument(
        "--out",
        default=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Projects",
            "JK_Pump_Build",
            "output",
            "pumpcad",
        ),
        help="output directory",
    )
    args = parser.parse_args(argv)

    outcomes = run_batch(args.source, args.out)
    ok = sum(1 for o in outcomes if o.status == "OK")
    check = sum(1 for o in outcomes if o.status == "CHECK")
    errors = sum(1 for o in outcomes if o.status == "ERROR")
    print(f"processed {len(outcomes)} pumps -> {args.out}")
    print(f"  fully validated: {ok}")
    print(f"  check failures:  {check}")
    print(f"  errors:          {errors}")
    combined = os.path.join(args.out, "JK_Pump_Build_All_Pumps.pml")
    if os.path.exists(combined):
        built = sum(1 for o in outcomes if o.script)
        print(f"  combined file:   {combined} ({built} pumps)")
        problems = os.path.join(args.out, "JK_Pump_Build_All_Pumps_PROBLEMS.txt")
        if os.path.exists(problems):
            print(f"  WARNING: combined file has problems, see {problems}")
    for outcome in outcomes:
        if outcome.status != "OK":
            detail = outcome.error or "; ".join(
                name for name, _, _ in (outcome.validation.failures if outcome.validation else [])
            )
            print(f"  [{outcome.status}] {outcome.tag}: {detail}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
