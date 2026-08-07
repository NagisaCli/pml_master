"""Regression tests that do not require an E3D installation and never write
into production project data."""

import json
import re
import tempfile
import unittest
from pathlib import Path

from e3d_agent.agent import E3DAgent
from e3d_agent.drawing_parser import NaturalLanguageParser
from e3d_agent.memory import MemoryStore
from e3d_agent.pml_generator import PMLGenerator
from e3d_agent.pml_knowledge import PMLKnowledgeBase


class StabilityTests(unittest.TestCase):
    def test_equipment_description_generates_pml(self):
        # The English description exercises the natural-language parser.
        intent = NaturalLanguageParser.parse(
            "Create a vertical storage tank T-101 with diameter 2 m and height 5 m in AREA_100 zone"
        )
        self.assertEqual(intent.zone, "AREA_100")
        self.assertEqual(len(intent.elements), 1)
        equipment = intent.elements[0]
        self.assertEqual((equipment.name, equipment.width, equipment.depth, equipment.height),
                         ("T-101", 2000.0, 2000.0, 5000.0))
        script = PMLGenerator(PMLKnowledgeBase()).generate(intent)
        # PML1 spells the element type EQUI, not EQUIPMENT; see
        # skill/knowledge/pml1-reference.md.
        self.assertIn("NEW EQUI", script)
        self.assertIn("T_101", script)

    def test_generated_cylinder_uses_the_centre_datum(self):
        """
        A CYLI's POS must be its geometric centre, not the bottom face.

        Checked numerically rather than by matching a POS line: a textual
        check passes a model in which every element has the wrong datum
        (AGENTS.md, "Non-negotiable"). This regression exists because the
        generator emitted the bottom-face point directly, putting a 5 m tank
        2.5 m underground with no error from E3D.
        """
        intent = NaturalLanguageParser.parse(
            "Create a vertical storage tank T-101 with diameter 2 m and height 5 m in AREA_100 zone"
        )
        script = PMLGenerator(PMLKnowledgeBase()).generate(intent)

        match = re.search(
            r"NEW CYLI\nDIAM (?P<diam>[\d.]+)\nHEIG (?P<heig>[\d.]+)\n"
            r"ORI Z IS U AND Y IS N\n"
            r"POS E (?P<e>-?[\d.]+) N (?P<n>-?[\d.]+) U (?P<u>-?[\d.]+)",
            script,
        )
        self.assertIsNotNone(match, f"no oriented CYLI block found in:\n{script}")

        height = float(match.group("heig"))
        centre_u = float(match.group("u"))
        # The parser supplies no elevation, so the bottom face is U 0 and the
        # centre must sit half a height above it.
        self.assertAlmostEqual(centre_u, height / 2.0, places=6)
        # The element must occupy 0..height, never dipping below its base.
        self.assertAlmostEqual(centre_u - height / 2.0, 0.0, places=6)
        self.assertGreater(centre_u, 0.0, "cylinder centre must be above its base")

    def test_unpositioned_elements_are_flagged_as_reference_values(self):
        """
        No parser populates coordinates yet, so the macro must say so.

        SKILL.md requires an assumed value to be labelled a Reference Value
        with its basis; silently emitting the origin presents a placeholder as
        project data.
        """
        intent = NaturalLanguageParser.parse(
            "Create a vertical storage tank T-101 with diameter 2 m and height 5 m in AREA_100 zone"
        )
        script = PMLGenerator(PMLKnowledgeBase()).generate(intent)
        self.assertIn("Reference Value", script)
        self.assertIn("zone origin", script)

    def test_memory_round_trip_and_error_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            store = MemoryStore(path)
            error_id = store.add_error("test", "simulated error")
            self.assertTrue(store.mark_resolved(error_id, "verified"))
            restored = MemoryStore(path)
            self.assertEqual(restored.get_stats()["total"], 1)
            self.assertEqual(restored.get_unresolved_errors(), [])

    def test_corrupt_memory_is_preserved_before_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            path.write_text("{invalid json", encoding="utf-8")
            store = MemoryStore(path)
            self.assertEqual(store.get_stats()["total"], 0)
            self.assertFalse(path.exists())
            self.assertEqual(len(list(Path(directory).glob("memory.json.corrupt.*"))), 1)

    def test_uppercase_drawing_extension_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            agent = E3DAgent(memory_path=Path(directory) / "memory.json")
            self.assertTrue(agent._is_file_path("C:/drawings/PID.SVG"))
            self.assertFalse(agent._is_file_path("create a storage tank T-101"))

    def test_memory_file_remains_valid_after_multiple_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            store = MemoryStore(path)
            for index in range(20):
                store.add_lesson(f"topic-{index}", "test")
            self.assertEqual(len(json.loads(path.read_text(encoding="utf-8"))), 20)


if __name__ == "__main__":
    unittest.main()
