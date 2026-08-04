"""Regression tests that do not require an E3D installation and never write
into production project data."""

import json
import tempfile
import unittest
from pathlib import Path

from e3d_agent.agent import E3DAgent
from e3d_agent.drawing_parser import NaturalLanguageParser
from e3d_agent.memory import MemoryStore
from e3d_agent.pml_generator import PMLGenerator
from e3d_agent.pml_knowledge import PMLKnowledgeBase


class StabilityTests(unittest.TestCase):
    def test_chinese_equipment_description_generates_pml(self):
        # The Chinese description is functional test data for the
        # natural-language parser; project content stays English.
        intent = NaturalLanguageParser.parse(
            "在 AREA_100 区域创建一台直径2米高5米的立式储罐 T-101"
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
            self.assertFalse(agent._is_file_path("创建一台储罐 T-101"))

    def test_memory_file_remains_valid_after_multiple_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            store = MemoryStore(path)
            for index in range(20):
                store.add_lesson(f"topic-{index}", "test")
            self.assertEqual(len(json.loads(path.read_text(encoding="utf-8"))), 20)


if __name__ == "__main__":
    unittest.main()
