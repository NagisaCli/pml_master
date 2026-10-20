"""
Build AVEVA E3D PML1 macros for 203-PU-409 (BS DD Drum Wash Pump)
and 203-PU-410 (BS DD Return Filtrate Pump).

Baseplate footprint from user CAD drawing:
- Length: 1278 mm (along North-South axis)
- Width:  516 mm  (along East-West axis)
- Thickness: 50 mm (standing project requirement)

Architecture:
- High-detail long-coupled horizontal centrifugal process pump
- PML1 clean syntax conforming strictly to Iron Rules (IR-1 to IR-10)
- Piecewise rigid adaptation of /P1501B-BASE (43 structural & fastener members)
- Driver with dual mirrored CONE frustums (2/3 dia outward) and 36 axial CYLINDER cooling ribs
- Casing volute + DISH cover + top discharge casing connector
- Native E3D catalogue-bound NOZZLE placeholders (/150lb_Ansi_Flanged)
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PROJECT_DIR = REPO / "Projects" / "JK_Pump_Build"
TOOLS_DIR = PROJECT_DIR / "tools"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(TOOLS_DIR))

from extract_project_data import load_all, PumpLocation, Element
from build_pumps import build_pump
from pump_model import Primitive, fmt, pos_line
from wsb.pml_builder import validate_pml
from wsb.pml_parser import parse_native_tree


def generate_pump(
    tag: str,
    duty_desc: str,
    output_paths: list[Path],
    staging_e: float = 0.0,
) -> tuple[str, dict]:
    sources = load_all()
    element_name = tag.replace("-", "_")

    # Baseplate envelope from user CAD drawing
    length = 1278.0  # mm, longitudinal along North
    width = 516.0    # mm, transverse along East
    thickness = 50.0 # mm, standing requirement

    # Physical machine elevations and nozzle positions
    shaft_u = 356.0
    casing_dia = 371.52
    casing_crown_u = shaft_u + casing_dia / 2.0  # 541.76 mm

    # Suction: axial suction at the front edge of baseplate (N = +639.0 mm)
    suction_face_n = length / 2.0  # 639.0 mm
    suction_catr = "/150lb_Ansi_Flanged/AAZFBB0NN"  # DN100 ANSI 150# RF
    suction_heig = 127.5

    # Discharge: top discharge at casing plan center (N = +400.0 mm)
    discharge_casing_n = 400.0
    discharge_catr = "/150lb_Ansi_Flanged/AAZFBB0LL"  # DN80 ANSI 150# RF
    discharge_heig = 200.0
    discharge_face_u = casing_crown_u + 100.0        # 641.76 mm

    loc = PumpLocation(
        tag=tag,
        element=element_name,
        func=duty_desc,
        elements=[
            Element(
                kind="BOX",
                sube=f"{element_name}_BASEPLATE",
                attrs={"XLEN": width, "YLEN": length, "ZLEN": thickness},
                pos={"east": staging_e, "north": 0.0, "up": thickness / 2.0},
                ori="ORI Z IS U AND Y IS N",
            ),
            Element(
                kind="NOZZLE",
                sube=f"{element_name}_SUCTION",
                name=f"/{element_name}/SUCTION_NOZZLE",
                attrs={"HEIG": suction_heig},
                catr=suction_catr,
                pos={"east": staging_e, "north": suction_face_n, "up": shaft_u},
                ori="ORI P1 IS N",
            ),
            Element(
                kind="NOZZLE",
                sube=f"{element_name}_DISCHARGE",
                name=f"/{element_name}/DISCHARGE_NOZZLE",
                attrs={"HEIG": discharge_heig},
                catr=discharge_catr,
                pos={"east": staging_e, "north": discharge_casing_n, "up": discharge_face_u},
                ori="ORI P1 IS U",
            ),
        ],
    )

    sources["location"][tag] = loc
    model = build_pump(tag, sources)

    # 1. Normalize 36 motor cooling ribs to sit on the stator outer surface (straddling 6mm in, 6mm out)
    stator_len = 330.95   # length of main cylindrical stator
    stator_dia = 260.25   # diameter of main stator
    stator_radius = stator_dia / 2.0  # 130.125 mm
    stator_n = -280.04    # centre N of main stator
    rib_count = 36
    rib_diam = 12.0

    # 2. Hardware profile scale for hex washers (16.67 / 20.0 = 0.8335)
    hw_scale = 16.67 / 20.0
    east_hex_prof = [
        (0.0, 0.0),
        (0.0, 20.0 * hw_scale),
        (17.32 * hw_scale, 30.0 * hw_scale),
        (34.64 * hw_scale, 20.0 * hw_scale),
        (34.64 * hw_scale, 0.0),
        (17.32 * hw_scale, -10.0 * hw_scale),
        (0.0, 0.0),
    ]

    base_cyls = [c for c in model.primitives if c.sube == "BASE" and c.kind == "CYLINDER"]

    new_prims = []
    rib_idx = 0
    for p in model.primitives:
        if p.sube == "DRIVER" and "cooling rib" in (p.note or ""):
            # Place rib cylinder center on stator surface
            ang = 2.0 * math.pi * rib_idx / rib_count
            rib_idx += 1
            reast = stator_radius * math.cos(ang)
            rup = shaft_u + stator_radius * math.sin(ang)
            rib_cyl = Primitive(
                kind="CYLINDER",
                sube="DRIVER",
                attrs={"DIAM": rib_diam, "HEIG": stator_len},
                east=reast,
                north=stator_n,
                up=rup,
                ori="ORI Z IS N AND Y IS U",
                note=f"axial stator cooling rib {rib_idx}/{rib_count}: proven CYLI form",
            )
            new_prims.append(rib_cyl)
        elif p.sube == "BASE" and p.kind == "EXTRUSION" and p.ori == "ORI Y is S and Z is U":
            # Fix East-side motor hex washers: remove inverted ORI and align with bolt shank
            paired_cyl = min(base_cyls, key=lambda c: (c.east - p.east)**2 + (c.north - p.north)**2)
            new_east = paired_cyl.east - 17.32 * hw_scale
            new_north = paired_cyl.north - 10.0 * hw_scale
            fixed_p = Primitive(
                kind="EXTRUSION",
                sube="BASE",
                attrs=p.attrs,
                east=new_east,
                north=new_north,
                up=p.up,
                ori=None,
                profile=east_hex_prof,
                note=p.note.replace("reference member", "hex washer motor (East corrected)"),
            )
            new_prims.append(fixed_p)
        else:
            new_prims.append(p)
    model.primitives = new_prims

    # Render balanced PML macro with clean comments and explicit END closures
    lines: list[str] = [
        f"-- ====================================================================",
        f"-- {tag}  {duty_desc.upper()}",
        f"-- ====================================================================",
        f"-- Equipment Tag: /{element_name}",
        f"-- Duty Description: {duty_desc}",
        f"-- Standard: AVEVA E3D Design Mk3.1 PML1 Compatible (Iron Rules Verified)",
        f"-- Datum: Local Baseplate Underside Centre at (E {staging_e:.1f}mm N 0mm U 0mm)",
        f"-- Baseplate Envelope: {width:.1f} mm (W) x {length:.1f} mm (L) x {thickness:.1f} mm (T)",
        f"-- Shaft Elevation: U {shaft_u:.2f} mm (Longitudinal axis: North +N)",
        f"-- Base Structure: 43-member /P1501B-BASE piecewise adapted assembly",
        f"-- Motor: Symmetric dual-cone TEFC motor with 36 axial ribs & terminal box",
        f"-- Suction: DN100 ANSI 150# RF ({suction_catr}) pointing North (+N)",
        f"-- Discharge: DN80 ANSI 150# RF ({discharge_catr}) pointing Up (+U)",
        f"-- Generated: 2026-10-15",
        f"-- Execution: In E3D, select a writable ZONE, then: $M <this file>",
        f"",
        f"NEW EQUIPMENT /{element_name}",
        f"DESC '{duty_desc}'",
        f"POS E 0mm N 0mm U 0mm",
        f"",
    ]

    for sube_name, primitives in model.by_sube().items():
        lines.append(f"NEW SUBEQUIPMENT /{element_name}_{sube_name}")
        for p in primitives:
            lines.extend(p.to_pml())
            lines.append("")
        lines.append("END")
        lines.append("")

    lines.append("END")
    lines.append("")

    pml_text = "\n".join(lines)

    # Syntax and Iron Rule Validation
    findings = validate_pml(pml_text, native_templates=True)
    if findings:
        raise ValueError(f"validate_pml reported findings for {tag}: {findings}")

    # Tree balance validation
    roots = parse_native_tree(pml_text)
    if len(roots) != 1 or roots[0].name != f"/{element_name}":
        raise ValueError(f"Hierarchy balance check failed for {tag}")

    # Save to all requested output paths
    for p in output_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(pml_text, encoding="utf-8")
        print(f"Wrote {p}")

    stats = {
        "tag": tag,
        "element": element_name,
        "primitives_count": len(model.primitives),
        "subequipments": list(model.by_sube().keys()),
        "baseplate": (width, length, thickness),
        "shaft_u": shaft_u,
        "casing_centre": model.facts["casing_centre"],
        "suction_nozzle": (suction_catr, (staging_e, suction_face_n, shaft_u), "N"),
        "discharge_nozzle": (discharge_catr, (staging_e, discharge_casing_n, discharge_face_u), "U"),
    }
    return pml_text, stats


def generate_all() -> dict:
    pumps_to_build = [
        ("203-PU-409", "BS DD Drum Wash Pump"),
        ("203-PU-410", "BS DD Return Filtrate Pump"),
    ]
    all_stats = {}
    pml_blocks = []

    for tag, duty in pumps_to_build:
        elem = tag.replace("-", "_")
        targets = [
            REPO / "output" / f"{elem}.pml",
            PROJECT_DIR / "output" / f"{elem}.pml",
        ]
        pml, stats = generate_pump(tag, duty, targets)
        all_stats[tag] = stats
        pml_blocks.append(pml)

    # Also build a temporary side-by-side review macro (760 mm clear space between baseplates)
    # 203-PU-409 at E 0, 203-PU-410 at E 1276 mm (516 + 760 = 1276 mm)
    pml409, _ = generate_pump("203-PU-409", "BS DD Drum Wash Pump", [], staging_e=0.0)
    pml410_staged, _ = generate_pump("203-PU-410", "BS DD Return Filtrate Pump", [], staging_e=1276.0)

    combined_pml = (
        "-- JK_Pump_Build - Combined Review Layout: 203-PU-409 & 203-PU-410\n"
        "-- Envelope: 516 x 1278 x 50 mm per pump\n"
        "-- Staging: 203-PU-409 at (0,0,0); 203-PU-410 at (1276,0,0) mm (760 mm clear space)\n"
        "-- Temporary review spacing is a Reference Value, not plant coordinates.\n\n"
        + pml409.strip() + "\n\n" + pml410_staged.strip() + "\n"
    )

    combined_targets = [
        REPO / "output" / "JK_Pump_Build_203_PU_409_410.pml",
        PROJECT_DIR / "output" / "JK_Pump_Build_203_PU_409_410.pml",
    ]
    for cp in combined_targets:
        cp.parent.mkdir(parents=True, exist_ok=True)
        cp.write_text(combined_pml, encoding="utf-8")
        print(f"Wrote {cp}")

    return all_stats


if __name__ == "__main__":
    stats = generate_all()
    print("\nGeneration Finished Successfully!")
    for tag, s in stats.items():
        print(f"\n{tag}:")
        for k, v in s.items():
            print(f"  {k}: {v}")
