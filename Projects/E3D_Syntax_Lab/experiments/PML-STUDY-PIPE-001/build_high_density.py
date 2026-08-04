"""Generate the all-component/high-density PIPE stress candidate.

This is an E3D stress specimen, not production equipment data. Catalogue paths
come from the preserved native export and the A3B study catalogue. The output
is intentionally tagged as experimental until the receiving E3D session
confirms every family in one dense model.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from wsb.piping_builder import (
    BranchSpec,
    NativeCatalogueComponentSpec,
    PipeSpec,
    PipingBuilder,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "candidate" / "11_high_density_all_components.pml"


def component(
    kind: str,
    x: float,
    north: float,
    up: float,
    orientation: str,
    spref: str,
    lstu: str,
    *,
    name: str | None = None,
    attributes: tuple[tuple[str, str], ...] = (),
) -> NativeCatalogueComponentSpec:
    return NativeCatalogueComponentSpec(
        element_type=kind,
        position=(x, north, up),
        orientation=orientation,
        spref=spref,
        lstu=lstu,
        name=name,
        attributes=attributes,
    )


def build_specs() -> tuple[PipeSpec, ...]:
    specs: list[PipeSpec] = []
    for lane in range(12):
        north = lane * 1800.0
        up = (lane % 3) * 600.0
        bore = 100.0
        pipe_name = f"/CODEX-P11-{lane + 1:02d}-DENSE"
        branch_name = f"{pipe_name}/B1"
        if lane % 2:
            head = (0.0, north, up + 200.0)
            tail = (16000.0, north, up)
            head_direction = "E 0.716 D"
            tail_direction = "W 0.716 U"
        else:
            head = (0.0, north, up)
            tail = (16000.0, north, up)
            head_direction = "E"
            tail_direction = "W"

        comps = (
            component("FLANGE", 800, north, up, "Y IS W AND Z IS U", "/A3B/FO100", "/A3B/PA100", attributes=(("ARRI", "2"), ("LEAV", "1"), ("RLOC", "2"))),
            component("GASKET", 1050, north, up, "Y IS E AND Z IS U", "/A3B/GC100", "/A3B/PA100", attributes=(("RLOC", "2"),)),
            component("VALVE", 1400, north, up, "Y IS E AND Z IS N", "/A3B/VG100", "/A3B/PA100", name=f"/CODEX-P11-V{lane + 1:02d}"),
            component("INSTRUMENT", 1800, north, up, "Y IS W AND Z IS U", "/A3B/OP100", "/A3B/PA100", name=f"/CODEX-P11-I{lane + 1:02d}", attributes=(("ARRI", "2"), ("LEAV", "1"))),
            component("ELBOW", 3200, north, up, "Y IS D AND Z IS N", "/A3B/EA100", "/A3B/PA100", attributes=(("ARRI", "2"), ("LEAV", "1"))),
            component("TEE", 5000, north, up, "Y IS N AND Z IS D", "/A3B/ST:100_100", "/A3B/PA100", attributes=(("ARRI", "3"),)),
            component("REDUCER", 6800, north, up, "Y IS E AND Z IS U", "/A3B/RC100X80", "/A3B/PA80"),
            component("OLET", 8000, north, up, "Y IS E AND Z IS N", "/A3B/TOL:100_80", "/A3B/PA100", attributes=(("ARRI", "2"), ("LEAV", "1"))),
            component("COUPLING", 9200, north, up, "Y IS N AND Z IS W", "/A3B/HC5:25", "/A3B/PA25"),
            component("BEND", 10500, north, up, "Y IS U AND Z IS E", "/A3B/EV50", "/A3B/PA50", attributes=(("RADI", "152.4mm"), ("ANGL", "90degree"))),
            component("FILTER", 12200, north, up, "Y IS W AND Z IS U", "/A3B/FIB100", "/A3B/PA100"),
            component("CLOSURE", 14500, north, up, "Y IS N AND Z IS E", "/A3B/KM20", "/A3B/PA20"),
            component("WELD", 5600, north, up, "Y IS W AND Z IS U", "/A3B/100WELFFWW", "/A3B/PA100", attributes=(("DESP", "0"), ("WLDN", str(lane + 1)))),
        )

        branch = BranchSpec(
            name=branch_name,
            head=head,
            tail=tail,
            head_direction=head_direction,
            tail_direction=tail_direction,
            head_bore=bore,
            tail_bore=bore,
            tube_component="/A3B/PA100",
            slope_ref="/1in100" if lane % 2 else None,
            components=comps,
        )
        specs.append(
            PipeSpec(
                name=pipe_name,
                specification="/A3B",
                bore=bore,
                temperature_c=50.0,
                slope_ref="/1in100" if lane % 2 else None,
                branches=(branch,),
            )
        )

    # A second catalogue/specification family proves that the stress harness is
    # not accidentally tied to the A3B plant-pipe family. These paths are copied
    # from the native FIRE network and remain experimental in this combined run.
    for lane in range(4):
        north = 25000.0 + lane * 1800.0
        pipe_name = f"/CODEX-P11-FIRE-{lane + 1:02d}"
        branch_name = f"{pipe_name}/B1"
        fire_components = (
            component("COUPLING", 800, north, 0, "Y IS E AND Z IS U", "/FIRE/COUP-2", "/FIRE/TUBE-1"),
            component("ELBOW", 1800, north, 0, "Y IS D AND Z IS W", "/FIRE/ELBO-1", "/FIRE/TUBE-1"),
            component("TEE", 3000, north, 0, "Y IS U AND Z IS S", "/FIRE/TEE-12", "/FIRE/TUBE-1"),
            component("VALVE", 4200, north, 0, "Y IS W AND Z IS U", "/FIRE/VALV-3", "/FIRE/TUBE-1"),
            component("CLOSURE", 5200, north, 0, "Y IS U AND Z IS S", "/FIRE/SPRINKLERHEAD-15", "/FIRE/TUBE-1"),
            component("CAP", 6200, north, 0, "Y IS U AND Z IS S", "/FIRE/CAP-6", "/FIRE/TUBE-1"),
        )
        specs.append(
            PipeSpec(
                name=pipe_name,
                specification="/FIRE",
                bore=50,
                temperature_c=20,
                branches=(
                    BranchSpec(
                        name=branch_name,
                        head=(0, north, 0),
                        tail=(7000, north, 0),
                        head_direction="E",
                        tail_direction="W",
                        head_bore=50,
                        tail_bore=50,
                        tube_component="/FIRE/TUBE-1",
                        components=fire_components,
                    ),
                ),
            )
        )
    return tuple(specs)


def build_macro() -> str:
    fragment = PipingBuilder().extend(build_specs()).build()
    return "\n".join(
        (
            "$S-  -- Synonym translation OFF",
            "-- PML-STUDY-PIPE-001 / candidate 11",
            "-- EXPERIMENTAL high-density all-component stress test",
            "-- 16 PIPE / 16 BRANCH / 180 catalogue component blocks",
            "ONERROR GOLABEL /ERROR3",
            "",
            "INPUT BEGIN",
            "NEW SITE /CODEX-PIPE-LAB11",
            "PURP PIPE",
            "",
            "NEW ZONE /CODEX-PIPE-LAB11-ZONE",
            "DESC 'HIGH DENSITY ALL COMPONENT STRESS TEST'",
            "FUNC 'Piping'",
            "PURP PIPE",
            "",
            fragment.rstrip(),
            "",
            "END",
            "END",
            "",
            "INPUT END SITE /CODEX-PIPE-LAB11",
            "INPUT FINISH",
            "",
            "LABEL /ERROR3",
            "handle ANY",
            "$S+",
            "RETURN ERROR",
            "endhandle",
            "",
            "$S+  -- Synonym translation ON",
            "",
        )
    )


if __name__ == "__main__":
    OUTPUT.write_text(build_macro(), encoding="utf-8", newline="\n")
    print(OUTPUT)
