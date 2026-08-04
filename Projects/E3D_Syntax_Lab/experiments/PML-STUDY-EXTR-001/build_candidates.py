"""Generate isolated EXTRUSION certification candidates."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[3]
sys.path.insert(0, str(REPO_ROOT))

from wsb.extrusion_builder import build_extrusion

PROFILE = (
    (0.0, 0.0),
    (0.0, 300.0),
    (100.0, 300.0),
    (100.0, 100.0),
    (300.0, 100.0),
    (300.0, 0.0),
)
HEX = (
    (-20.0, 0.0),
    (-10.0, 17.320508),
    (10.0, 17.320508),
    (20.0, 0.0),
    (10.0, -17.320508),
    (-10.0, -17.320508),
)


def swap_pos_ori(macro: str) -> str:
    """Swap the POS and ORI lines of one EXTRUSION block (experimental order).

    The builder always emits the native POS -> ORI order. Candidate 03 exists
    solely to test whether E3D treats the reversed ORI -> POS order
    identically, so this helper produces the reversed variant by rearranging
    the two lines inside the generated block. The production builder is
    intentionally left unchanged until the discriminating E3D result exists.
    """

    lines = macro.splitlines()
    pos_index = next(i for i, line in enumerate(lines) if line.startswith("POS "))
    ori_index = next(i for i, line in enumerate(lines) if line.startswith("ORI "))
    if abs(pos_index - ori_index) != 1:
        raise ValueError("expected POS and ORI to be adjacent in EXTRUSION block")
    low, high = sorted((pos_index, ori_index))
    lines[low], lines[high] = lines[high], lines[low]
    return "\n".join(lines)


def wrap(name: str, body: str, description: str) -> str:
    return "\n".join(
        (
            "$S-  -- Synonym translation OFF",
            "ONERROR GOLABEL /ERROR3",
            "INPUT BEGIN",
            f"NEW EQUIPMENT /{name}",
            "POS E 0mm N 0mm U 0mm",
            f"DESC '{description}'",
            body.rstrip(),
            "END",
            f"INPUT END EQUIPMENT /{name}",
            "INPUT FINISH",
            "LABEL /ERROR3",
            "handle ANY",
            "$S+",
            "RETURN ERROR",
            "endhandle",
            "$S+  -- Synonym translation ON",
            "",
        )
    )


def axes_candidate() -> str:
    blocks = []
    cases = (
        ("U", (0.0, 0.0, 1000.0), "Y IS N AND Z IS U"),
        ("E", (2000.0, 0.0, 1000.0), "Y IS N AND Z IS E"),
        ("N", (4000.0, 0.0, 1000.0), "Y IS U AND Z IS N"),
    )
    for label, position, orientation in cases:
        blocks.extend(
            (
                f"NEW SUBEQUIPMENT /CODEX_EXTR_AXES_{label}",
                build_extrusion(position, orientation, 800.0, PROFILE, level=(5, 10)).rstrip(),
                "END",
            )
        )
    return wrap("CODEX_EXTR_AXES", "\n".join(blocks), "EXTRUSION LOCAL XY AND Z AXIS TEST")


def fastener_candidate() -> str:
    lower = build_extrusion((0.0, 0.0, 20.0), "Y IS N AND Z IS U", 20.0, HEX, level=(5, 10))
    upper = build_extrusion((0.0, 0.0, 100.0), "Y IS N AND Z IS U", 20.0, HEX, level=(5, 10))
    body = "\n".join(
        (
            "NEW SUBEQUIPMENT /CODEX_EXTR_FASTENER_ASSEMBLY",
            "NEW CYLINDER",
            "DIAM 15mm",
            "HEIG 100mm",
            "ORI Z IS U AND Y IS N",
            "POS E 0mm N 0mm U 60mm",
            "END",
            lower.rstrip(),
            upper.rstrip(),
            "END",
        )
    )
    return wrap("CODEX_EXTR_FASTENER", body, "EXTRUDED HEX FASTENER CONTACT TEST")


def native_contact_candidate() -> str:
    """Reproduce the native /PMP-10 fastener contact contract exactly.

    The native specimen (2026-08-03_pmp10_native.txt) shows the two hex heads
    are coaxial nuts on the shank, not caps outside it:
    - shank centre POS with HEIG 100 spans U 10..110 at centre U 60;
    - lower head profile plane 10 mm above the shank bottom (POS U 20,
      spans 20..40) so the shank protrudes 10 mm below;
    - upper head profile plane flush with the shank top (POS U 90,
      spans 90..110), top faces coincident.

    Candidate 02 deliberately left the upper head at POS U 100 (10 mm proud);
    this candidate moves it to the native flush position. The lower head at
    POS U 20 already matched the native pattern.
    """

    lower = build_extrusion((0.0, 0.0, 20.0), "Y IS N AND Z IS U", 20.0, HEX, level=(5, 10))
    upper = build_extrusion((0.0, 0.0, 90.0), "Y IS N AND Z IS U", 20.0, HEX, level=(5, 10))
    body = "\n".join(
        (
            "NEW SUBEQUIPMENT /CODEX_EXTR_FASTENER_ASSEMBLY",
            "NEW CYLINDER",
            "DIAM 15mm",
            "HEIG 100mm",
            "ORI Z IS U AND Y IS N",
            "POS E 0mm N 0mm U 60mm",
            "END",
            lower.rstrip(),
            upper.rstrip(),
            "END",
        )
    )
    return wrap(
        "CODEX_EXTR_FASTENER_NATIVE",
        body,
        "EXTRUDED HEX FASTENER NATIVE CONTACT CONTRACT",
    )


def order_candidate() -> str:
    """Discriminate POS->ORI vs ORI->POS for EXTRUSION.

    Two non-identity orientations are used because an identity frame (Z up /
    Y north) cannot reveal whether assigning POS before ORI rotates the
    position vector: the rotation is the identity. With a 90-degree frame,
    a rotated POS would land on a visibly different world coordinate.
    """

    profile = PROFILE
    cases = (
        # (sube, position, orientation, native_order)
        ("A", (0.0, 0.0, 1000.0), "Y IS N AND Z IS E", True),
        ("B", (0.0, 2000.0, 1000.0), "Y IS N AND Z IS E", False),
        ("C", (4000.0, 0.0, 1000.0), "Y IS U AND Z IS N", True),
        ("D", (4000.0, 2000.0, 1000.0), "Y IS U AND Z IS N", False),
    )
    blocks = []
    for label, position, orientation, native in cases:
        macro = build_extrusion(position, orientation, 800.0, profile, level=(5, 10))
        if not native:
            macro = swap_pos_ori(macro)
        blocks.extend(
            (
                f"NEW SUBEQUIPMENT /CODEX_EXTR_ORDER_{label}",
                macro.rstrip(),
                "END",
            )
        )
    return wrap(
        "CODEX_EXTR_ORDER",
        "\n".join(blocks),
        "EXTRUSION POS/ORI ASSIGNMENT ORDER SENSITIVITY TEST",
    )


if __name__ == "__main__":
    outputs = {
        "01_extrusion_axes_and_datum.pml": axes_candidate(),
        "02_extruded_hex_fastener.pml": fastener_candidate(),
        "03_extrusion_order_sensitivity.pml": order_candidate(),
        "04_extruded_hex_fastener_native_contact.pml": native_contact_candidate(),
    }
    for filename, text in outputs.items():
        path = ROOT / "candidate" / filename
        path.write_text(text, encoding="utf-8", newline="\n")
        print(path)
