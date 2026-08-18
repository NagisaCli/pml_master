"""Tests for the batch driver and the combined all-pumps macro."""

from __future__ import annotations

import json
import os
import re

import pytest

from pumpcad.batch import run_batch
from wsb.pml_builder import validate_pml


def _pump_json(tag: str, east: float, north: float) -> dict:
    """A minimal but realistic export: outline, motor, casing, shaft."""

    def line(x1: float, y1: float, x2: float, y2: float, handle: str) -> dict:
        return {
            "kind": "Line",
            "start": {"x": x1, "y": y1},
            "end": {"x": x2, "y": y2},
            "radius": 0,
            "startAngle": 0,
            "endAngle": 0,
            "handle": handle,
        }

    def rect(x0: float, y0: float, x1: float, y1: float, t: str) -> list:
        return [
            line(x0, y0, x1, y0, f"{t}b"),
            line(x1, y0, x1, y1, f"{t}r"),
            line(x1, y1, x0, y1, f"{t}t"),
            line(x0, y1, x0, y0, f"{t}l"),
        ]

    primitives = (
        rect(0, 0, 1720, 760, f"{tag}_plate")
        + rect(313, 140, 776, 620, f"{tag}_motor")
        + rect(1200, 250, 1500, 510, f"{tag}_casing")
    )
    return {
        "equipment_tag": tag,
        "equipment_name": f"{tag} TEST PUMP",
        "location_e_n_u": f"{east},{north},0",
        "length_mm": 1720,
        "width_mm": 760,
        "inlet_nozzle_orientation": "E",
        "outlet_nozzle_orientation": "U",
        "reference_top_view": f"Top View - {tag}",
        "dn_input_mm": 150,
        "dn_output_mm": 100,
        "specification": "ANSI-NOZZLES",
        "generic_type": "150lb Ansi Flanges",
        "source": {"file": "Pump_details.xlsx", "sheet": "Sheet1", "row": 2},
        "shape-reference": {
            "schema": "cad2e3d-aid",
            "schemaVersion": 1,
            "sourceDrawing": "test.dwg",
            "sourceApplication": "test",
            "sourceUnits": "Millimetres",
            "batchBasePoint": {"x": 0, "y": 0},
            "createdUtc": "2026-08-12T00:00:00Z",
            "exporterVersion": "1.0.0",
            "groups": [
                {
                    "sourceId": "loose-1",
                    "groupingMode": "ManualBatch",
                    "sourceBlockName": "LOOSE",
                    "suggestedName": "/TEST",
                    "insertionPoint": {"x": 0, "y": 0},
                    "localBasePoint": {"x": 0, "y": 0},
                    "sourceHandles": [],
                    "bounds": {"minX": 0, "minY": 0, "maxX": 1720, "maxY": 760},
                    "primitives": primitives,
                    "unsupported": [],
                    "warnings": [],
                }
            ],
        },
    }


@pytest.fixture()
def batch_dirs(tmp_path):
    source = tmp_path / "pumps"
    source.mkdir()
    for index, tag in enumerate(["101-PU-001", "101-PU-002", "101-PU-003"]):
        payload = _pump_json(tag, 10000.0 + index * 5000.0, 20000.0)
        (source / f"{tag}.json").write_text(json.dumps(payload), encoding="utf-8")
    return str(source), str(tmp_path / "out")


class TestBatch:
    def test_writes_one_file_per_pump_and_a_combined_file(self, batch_dirs) -> None:
        source, out = batch_dirs
        outcomes = run_batch(source, out)
        assert len(outcomes) == 3
        assert all(o.ok for o in outcomes)
        assert len(os.listdir(os.path.join(out, "pumps"))) == 3
        assert os.path.exists(os.path.join(out, "JK_Pump_Build_All_Pumps.pml"))

    def test_combined_file_holds_every_pump_exactly_once(self, batch_dirs) -> None:
        source, out = batch_dirs
        run_batch(source, out)
        script = open(
            os.path.join(out, "JK_Pump_Build_All_Pumps.pml"), encoding="utf-8"
        ).read()
        names = re.findall(r"^NEW EQUI (/\S+)", script, flags=re.MULTILINE)
        assert len(names) == 3
        assert len(set(names)) == 3, "EQUI names must be unique across the package"

    def test_combined_file_passes_syntax_validation(self, batch_dirs) -> None:
        """Concatenation must not introduce defects of its own."""
        source, out = batch_dirs
        run_batch(source, out)
        script = open(
            os.path.join(out, "JK_Pump_Build_All_Pumps.pml"), encoding="utf-8"
        ).read()
        assert validate_pml(script) == []
        assert not os.path.exists(
            os.path.join(out, "JK_Pump_Build_All_Pumps_PROBLEMS.txt")
        )

    def test_combined_content_matches_the_per_pump_files(self, batch_dirs) -> None:
        source, out = batch_dirs
        run_batch(source, out)
        combined = open(
            os.path.join(out, "JK_Pump_Build_All_Pumps.pml"), encoding="utf-8"
        ).read()
        for tag in ["101-PU-001", "101-PU-002", "101-PU-003"]:
            single = open(
                os.path.join(out, "pumps", f"{tag}.pml"), encoding="utf-8"
            ).read()
            # Every geometry line of the standalone macro must appear in the
            # combined file: it is the same content, not a re-derivation.
            for line in single.splitlines():
                if line.startswith(("NEW ", "POS ", "XLEN", "YLEN", "ZLEN", "DIAM")):
                    assert line in combined, f"{tag}: {line!r} missing from combined"

    def test_combined_file_does_not_claim_to_hold_one_equi(self, batch_dirs) -> None:
        source, out = batch_dirs
        run_batch(source, out)
        script = open(
            os.path.join(out, "JK_Pump_Build_All_Pumps.pml"), encoding="utf-8"
        ).read()
        assert "Exactly one EQUI in this file" not in script

    def test_a_broken_file_does_not_stop_the_batch(self, tmp_path) -> None:
        source = tmp_path / "pumps"
        source.mkdir()
        (source / "101-PU-001.json").write_text(
            json.dumps(_pump_json("101-PU-001", 1000.0, 2000.0)), encoding="utf-8"
        )
        (source / "broken.json").write_text("{ not valid json", encoding="utf-8")
        outcomes = run_batch(str(source), str(tmp_path / "out"))
        assert any(o.status == "ERROR" for o in outcomes)
        assert any(o.status in ("OK", "CHECK") for o in outcomes)
        # The good pump still reaches the combined file.
        assert os.path.exists(
            os.path.join(str(tmp_path / "out"), "JK_Pump_Build_All_Pumps.pml")
        )
