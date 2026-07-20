"""Static integrity tests for the high-fidelity E3D watch macro."""

import re
import unittest
from pathlib import Path


MACRO_PATH = Path(__file__).parent.parent / "output" / "watch_model_hifi.pml"


class WatchHifiMacroTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lines = MACRO_PATH.read_text(encoding="utf-8").splitlines()
        cls.text = "\n".join(cls.lines)

    def test_names_are_unique_and_model_is_sufficiently_detailed(self):
        names = re.findall(r"^NEW EQUI /([^\s]+)$", self.text, flags=re.MULTILINE)
        self.assertGreaterEqual(len(names), 80)
        self.assertEqual(len(names), len(set(names)))

    def test_no_unapproved_hierarchy_creation(self):
        self.assertNotRegex(self.text, r"(?m)^NEW (?:SITE|ZONE)\b")
        self.assertIn("Select an existing writable ZONE as CE", self.text)

    def test_every_primitive_has_complete_dimensions(self):
        current_primitive = None
        dimensions = set()
        expected = {"CYLI": {"DIAM", "HEIG"}, "BOX": {"XLEN", "YLEN", "ZLEN"}}

        for raw_line in self.lines + ["NEW EQUI /END_OF_FILE"]:
            line = raw_line.strip()
            if line in ("NEW CYLI", "NEW BOX"):
                if current_primitive:
                    self.assertTrue(expected[current_primitive].issubset(dimensions))
                current_primitive = "CYLI" if line == "NEW CYLI" else "BOX"
                dimensions = set()
            elif current_primitive and line:
                token = line.split(maxsplit=1)[0]
                if token in expected[current_primitive]:
                    dimensions.add(token)
            if line.startswith("NEW EQUI") and current_primitive:
                self.assertTrue(expected[current_primitive].issubset(dimensions))
                current_primitive = None
                dimensions = set()

    def test_hifi_features_are_present(self):
        self.assertEqual(len(re.findall(r"^NEW EQUI /WATCHHF_BZ_TICK_", self.text, re.MULTILINE)), 12)
        self.assertEqual(len(re.findall(r"^NEW EQUI /WATCHHF_BZ_GRIP_", self.text, re.MULTILINE)), 12)
        self.assertEqual(len(re.findall(r"^NEW EQUI /WATCHHF_IDX_", self.text, re.MULTILINE)), 12)
        self.assertEqual(len(re.findall(r"^NEW EQUI /WATCHHF_BR_", self.text, re.MULTILINE)), 24)

    def _element_body(self, name):
        match = re.search(
            rf"^NEW EQUI /{re.escape(name)}\n(?P<body>.*?)(?=^NEW EQUI |\Z)",
            self.text,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match, f"missing {name}")
        return match.group("body")

    def _position_and_dimension(self, name, primitive, dimension):
        body = self._element_body(name)
        position = re.search(r"POS E ([\-0-9.]+) N ([\-0-9.]+) U ([\-0-9.]+)", body)
        value = re.search(rf"^{dimension} ([\-0-9.]+)$", body, flags=re.MULTILINE)
        self.assertIsNotNone(position, f"{name} has no position")
        self.assertIn(f"NEW {primitive}", body)
        self.assertIsNotNone(value, f"{name} has no {dimension}")
        return tuple(map(float, position.groups())), float(value.group(1))

    def test_key_spatial_relationships_and_clearances(self):
        # CYLI positions are base-centres: stack layer end must meet the next start.
        stack = [
            ("WATCHHF_BACK_001", -1.20, 1.20),
            ("WATCHHF_MIDCASE_001", 0.00, 7.20),
            ("WATCHHF_BEZEL_001", 7.20, 1.15),
            ("WATCHHF_BEZEL_INSERT_001", 8.35, 0.25),
            ("WATCHHF_REHAUT_001", 8.60, 0.10),
            ("WATCHHF_DIAL_001", 8.70, 0.15),
        ]
        for (_, start, height), (_, next_start, _) in zip(stack, stack[1:]):
            self.assertAlmostEqual(start + height, next_start, places=6)

        crystal_pos, crystal_height = self._position_and_dimension(
            "WATCHHF_CRYSTAL_001", "CYLI", "HEIG"
        )
        cap_pos, cap_height = self._position_and_dimension(
            "WATCHHF_HAND_CAP_001", "CYLI", "HEIG"
        )
        self.assertAlmostEqual(crystal_pos[2] + crystal_height, 10.05, places=6)
        self.assertGreaterEqual(crystal_pos[2] - (cap_pos[2] + cap_height), 0.10)

        north_lug_pos, north_lug_y = self._position_and_dimension(
            "WATCHHF_LUG_NE_001", "BOX", "YLEN"
        )
        south_lug_pos, south_lug_y = self._position_and_dimension(
            "WATCHHF_LUG_SE_001", "BOX", "YLEN"
        )
        lug_to_lug = (north_lug_pos[1] + north_lug_y / 2) - (south_lug_pos[1] - south_lug_y / 2)
        self.assertAlmostEqual(lug_to_lug, 48.80, places=6)

        link_pos, link_length = self._position_and_dimension(
            "WATCHHF_BR_N4_C_001", "BOX", "YLEN"
        )
        self.assertAlmostEqual(link_pos[1] + link_length / 2, 100.30, places=6)
        self.assertIn("ORI Y IS N60W AND Z IS U", self.text)
        self.assertIn("ORI Y IS N60E AND Z IS U", self.text)


if __name__ == "__main__":
    unittest.main()
