from __future__ import annotations

import hashlib
from pathlib import Path

from wsb.pml_builder import validate_pml


ROOT = Path(__file__).parents[1]
STUDY = ROOT / "Projects/E3D_Syntax_Lab/experiments/PML-STUDY-EXTR-001"
SOURCE = STUDY / "source/2026-08-03_pmp10_native.txt"


def test_native_pump_extrusion_evidence_is_preserved():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == (
        "4cd84139c043c06635c4138c8f676680c7b5143043c32de5ec11931be9e52d26"
    )
    text = SOURCE.read_text(encoding="utf-8-sig")
    assert text.count("NEW EXTRUSION") == 17
    assert text.count("NEW LOOP") == 17
    assert text.count("NEW VERTEX") == 120


def test_extrusion_candidates_are_isolated_and_valid():
    for path in sorted((STUDY / "candidate").glob("*.pml")):
        text = path.read_text(encoding="utf-8")
        assert text.count("NEW EQUIPMENT") == 1
        assert "NEW SITE" not in text
        assert "NEW PIPE" not in text
        assert validate_pml(text) == []


def test_candidate_03_contains_both_assignment_orders():
    text = (STUDY / "candidate/03_extrusion_order_sensitivity.pml").read_text(
        encoding="utf-8"
    )
    # A/C emit the native POS -> ORI order; B/D emit the reversed ORI -> POS
    # order at identical POS values, so E3D can discriminate order sensitivity.
    assert (
        "NEW EXTRUSION\nPOS E 0mm N 0mm U 1000mm\nORI Y IS N AND Z IS E"
        in text
    )
    assert (
        "NEW EXTRUSION\nORI Y IS N AND Z IS E\nPOS E 0mm N 2000mm U 1000mm"
        in text
    )
    assert (
        "NEW EXTRUSION\nPOS E 4000mm N 0mm U 1000mm\nORI Y IS U AND Z IS N"
        in text
    )
    assert (
        "NEW EXTRUSION\nORI Y IS U AND Z IS N\nPOS E 4000mm N 2000mm U 1000mm"
        in text
    )


def test_candidate_04_reproduces_native_fastener_contact_contract():
    text = (STUDY / "candidate/04_extruded_hex_fastener_native_contact.pml").read_text(
        encoding="utf-8"
    )
    # Native /PMP-10 contract with the verified end-plane datum:
    # shank centre U 60 (occupies 10..110), lower head POS U 20 (20..40,
    # shank protrudes 10 mm), upper head POS U 90 (90..110, flush with top).
    assert "POS E 0mm N 0mm U 60mm" in text
    assert "POS E 0mm N 0mm U 20mm" in text
    assert "POS E 0mm N 0mm U 90mm" in text
    assert text.count("HEIG 20mm") == 2


def test_round1_user_evidence_is_preserved_byte_for_byte():
    path = STUDY / "results/evidence/2026-08-04_EXTR02_user_report.txt"
    assert path.is_file()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "418d0b31c0fb58467480c8ea518a007f4292e49747c6fff60de51b7d82ede6c8"
    )
