"""Generate trial candidates for PML-STUDY-HANDRA-001."""

from pathlib import Path

from wsb.handrail_builder import (
    HandrailBuilder,
    HandrailSpec,
    RouteCurve,
    RoutePoint,
    build_arc_handrail,
    build_circular_handrail,
    build_polyline_handrail,
    build_rectangular_handrail,
)

CANDIDATES_DIR = Path(__file__).resolve().parent / "candidate"
CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)


def _wrap_transaction(body: str, title: str, stru_name: str = "CODEX_HANDRA_TEST") -> str:
    lines = [
        f"-- Macro: {title}",
        "-- Study: PML-STUDY-HANDRA-001 (AVEVA E3D Design)",
        "-- Hierarchy: STRU -> FRMWORK -> HANDRA",
        "-- ----------------------------------------------------------------",
        "",
        f"NEW STRU /{stru_name}_STRU",
        f"NEW FRMWORK /{stru_name}_FRMWORK",
        "",
        body.strip(),
        "",
        "END",
        "END",
        "",
    ]
    return "\n".join(lines)


def generate_all() -> None:
    # 01 - Circular Handrail (Cleaned transaction)
    pml_01 = build_circular_handrail(
        center_local=(0.0, 2910.0),
        radius=2910.0,
        position=(0.0, 0.0, 1000.0),
        name="CODEX_HANDRA_CIRC_01",
    )
    (CANDIDATES_DIR / "01_circular_handra_trial.pml").write_text(
        _wrap_transaction(pml_01, "Candidate 01 - Full Circular Handrail (R=2910mm)", "CODEX_HR_CIRC_01"),
        encoding="utf-8",
    )

    # 02 - Rectangular Platform Perimeter Handrail (6000 x 4000 mm)
    pml_02 = build_rectangular_handrail(
        length_e=6000.0,
        width_n=4000.0,
        origin=(0.0, 0.0, 1000.0),
        name="CODEX_HANDRA_RECT_02",
        post_spacing=1200.0,
        fillet_radius=150.0,
    )
    (CANDIDATES_DIR / "02_rectangular_platform_handra.pml").write_text(
        _wrap_transaction(pml_02, "Candidate 02 - Rectangular Platform Handrail (6000x4000mm)", "CODEX_HR_RECT_02"),
        encoding="utf-8",
    )

    # 03 - Horseshoe / Open-Arc Walkway Handrail (Straight runs + 180 deg curved return)
    # Straight East 4000mm -> 180 deg turn North (R=1000mm) -> Straight West 4000mm
    path_03 = [
        RoutePoint(position=(0.0, 0.0, 1000.0), fillet_radius=100.0),
        RoutePoint(position=(4000.0, 0.0, 1000.0), fillet_radius=100.0),
        RouteCurve(position=(4707.11, 292.89, 1000.0), curve_type="THRU"),
        RoutePoint(position=(5000.0, 1000.0, 1000.0), fillet_radius=100.0),
        RouteCurve(position=(4707.11, 1707.11, 1000.0), curve_type="THRU"),
        RoutePoint(position=(4000.0, 2000.0, 1000.0), fillet_radius=100.0),
        RoutePoint(position=(0.0, 2000.0, 1000.0), fillet_radius=100.0),
    ]
    pml_03 = HandrailBuilder().build(
        HandrailSpec(
            name="CODEX_HANDRA_HORSESHOE_03",
            position=(0.0, 0.0, 0.0),
            top_rail_height=1250.0,
            mid_rail_height=750.0,
            post_spacing=1000.0,
            path_items=path_03,
        )
    )
    (CANDIDATES_DIR / "03_horseshoe_walkway_handra.pml").write_text(
        _wrap_transaction(pml_03, "Candidate 03 - Horseshoe Walkway Handrail (Straight + 180 deg Curve)", "CODEX_HR_HORSESHOE_03"),
        encoding="utf-8",
    )

    # 04 - Sloped Stair / Ramp Handrail (with landing)
    # Flat run 1500mm -> Sloped rise 3000mm along E, rising +1500mm U -> Top landing 1500mm
    path_04 = [
        RoutePoint(position=(0.0, 0.0, 0.0), fillet_radius=150.0),
        RoutePoint(position=(1500.0, 0.0, 0.0), fillet_radius=150.0),
        RoutePoint(position=(4500.0, 0.0, 1500.0), fillet_radius=150.0),
        RoutePoint(position=(6000.0, 0.0, 1500.0), fillet_radius=150.0),
    ]
    pml_04 = build_polyline_handrail(
        [pt.position for pt in path_04],
        name="CODEX_HANDRA_SLOPED_04",
        fillet_radius=150.0,
        post_spacing=1000.0,
    )
    (CANDIDATES_DIR / "04_sloped_stair_handra.pml").write_text(
        _wrap_transaction(pml_04, "Candidate 04 - Sloped Stair / Ramp Handrail with Landings", "CODEX_HR_SLOPED_04"),
        encoding="utf-8",
    )

    print("Successfully generated all 4 handrail candidate macros.")


if __name__ == "__main__":
    generate_all()
