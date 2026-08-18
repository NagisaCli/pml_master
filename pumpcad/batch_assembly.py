"""
Batch driver for the whole-assembly PML.
========================================

Runs the assembly decomposition over every pump and writes one macro per
pump plus a combined file, alongside the earlier component-based output
rather than replacing it, so the two can be compared in E3D.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import traceback
from typing import List, Optional, Tuple

from wsb.pml_builder import validate_pml

from .assembly_model import decompose
from .assembly_pml import emit_assembly, name_parts, render_assembly_pml
from .contours import find_outline_rectangle
from .semantic import ViewType, build_semantic_model
from .source import load_all
from .transform import Placement

__all__ = ["run_assembly_batch", "main"]

BASEPLATE_THICKNESS = 50.0


def _layout_axis(inlet: str) -> str:
    axis = (inlet or "E").upper()
    return axis if axis in ("E", "W", "N", "S") else "E"


def run_assembly_batch(source_dir: str, out_dir: str) -> Tuple[int, int, List[str]]:
    """Reconstruct every pump as a full assembly.  Returns (pumps, parts, problems)."""
    generated = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    records, _ = load_all(source_dir)

    pml_dir = os.path.join(out_dir, "assembly")
    os.makedirs(pml_dir, exist_ok=True)

    problems: List[str] = []
    scripts: List[Tuple[str, str]] = []
    total_parts = 0

    for record in records:
        try:
            if not record.has_geometry:
                problems.append(f"{record.tag}: no CAD geometry; skipped")
                continue
            model = build_semantic_model(record)
            outline = model.outline or find_outline_rectangle(record.entities)
            if outline is None:
                problems.append(f"{record.tag}: no outline; skipped")
                continue

            assembly = decompose(record.entities, outline)
            placement = Placement(
                origin=record.location_e_n_u,
                layout_axis=_layout_axis(record.inlet_orientation),
            )
            elevation = model.view is ViewType.ELEVATION
            solids, notes = emit_assembly(
                assembly,
                placement,
                prefix=record.tag.replace("-", "_"),
                elevation=elevation,
                base_elevation=BASEPLATE_THICKNESS,
            )
            if not solids:
                problems.append(f"{record.tag}: decomposition produced no solids")
                continue

            labels = name_parts(assembly, elevation=elevation)
            script = render_assembly_pml(
                record.tag,
                record.name,
                solids,
                labels,
                generated=generated,
                header_notes=list(assembly.notes) + notes,
            )
            found = validate_pml(script)
            if found:
                problems.append(f"{record.tag}: {'; '.join(found[:2])}")

            path = os.path.join(pml_dir, f"{record.tag}.pml")
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(script)
            scripts.append((record.tag, script))
            total_parts += len(solids)
        except Exception as exc:  # noqa: BLE001 - batch isolation
            problems.append(f"{record.tag}: {type(exc).__name__}: {exc}")
            problems.append(traceback.format_exc(limit=2))

    if scripts:
        combined: List[str] = []
        combined.append("-- " + "=" * 68)
        combined.append("-- JK_Pump_Build - all pumps, whole-assembly reconstruction")
        combined.append("-- " + "=" * 68)
        combined.append(f"-- Pumps: {len(scripts)}   Parts: {total_parts}")
        combined.append(f"-- Generated: {generated}")
        combined.append("-- Execution: select a writable ZONE, then $M <this file>")
        combined.append("-- " + "=" * 68)
        for tag, script in scripts:
            combined.append("")
            combined.append("-- " + "-" * 66)
            combined.append(f"-- {tag}")
            combined.append("-- " + "-" * 66)
            combined.extend(
                line for line in script.splitlines() if not line.startswith("-- =")
            )
        text = "\n".join(combined).rstrip() + "\n"
        names = re.findall(r"^NEW EQUI (/\S+)", text, flags=re.MULTILINE)
        if len(set(names)) != len(names):
            problems.append("combined assembly file has duplicate EQUI names")
        with open(
            os.path.join(out_dir, "JK_Pump_Build_All_Pumps_Assembly.pml"),
            "w",
            encoding="utf-8",
            newline="\n",
        ) as handle:
            handle.write(text)

    return len(scripts), total_parts, problems


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reconstruct pumps as complete assemblies."
    )
    parser.add_argument("--source", default=r"C:\Users\A\Desktop\pumps")
    parser.add_argument(
        "--out",
        default=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Projects",
            "JK_Pump_Build",
            "output",
            "pumpcad",
        ),
    )
    args = parser.parse_args(argv)

    pumps, parts, problems = run_assembly_batch(args.source, args.out)
    print(f"assembly reconstruction -> {args.out}")
    print(f"  pumps: {pumps}")
    print(f"  parts: {parts}")
    if problems:
        print(f"  problems: {len(problems)}")
        for line in problems[:12]:
            print(f"    {line.splitlines()[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
