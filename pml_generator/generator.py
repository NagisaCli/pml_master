"""
PML Code Generator
===================
Generates executable PML1 scripts from DesignIntent (drawing parse / natural language).
Uses a combined strategy of knowledge base + templates.

Syntax specification: PML1 (E3D 3.1 $$MACRO mode)
Banned: !!Alert $P ENDS END EQUI NAME = DESC = !var = COLLECT UNSET !!CE !!WORLD
"""

from typing import Dict, List, Optional
import re
from datetime import datetime

from ..drawing_parser import DesignIntent, DesignElement
from ..pml_knowledge import PMLKnowledgeBase


class PMLGenerator:
    """
    PML code generator for paper mill plant equipment.

    Strategy:
    1. Template matching — predefined templates for common paper mill patterns
    2. Knowledge retrieval — paper mill equipment specs from PMLKnowledgeBase
    3. PML1-only syntax — zero PML2 residue guaranteed
    """

    BANNED_SYNTAX = [
        '!!Alert', '$P', 'ENDS', 'END EQUI', 'NAME =', 'DESC =',
        '!var =', 'COLLECT', 'UNSET', '!!CE', '!!WORLD',
    ]

    # Paper mill equipment type → primitive mapping
    EQUIPMENT_PRIMITIVE = {
        'VESSEL':      'CYLI',   # Storage tanks, chests, silos
        'COLUMN':      'CYLI',   # Towers, digesters
        'DIGESTER':    'CYLI',
        'BLEACH_TOWER': 'CYLI',
        'BLOW_TANK':   'CYLI',
        'STOCK_CHEST': 'CYLI',
        'PULPER':      'CYLI',   # Hydrapulper tank body
        'EVAPORATOR':  'CYLI',
        'SCREEN':      'CYLI',   # Pressure screen body
        'WASHER':      'CYLI',   # Vacuum washer drum
        'KILN':        'CYLI',   # Lime kiln shell
        'CLARIFIER':   'CYLI',
        'BOILER':      'BOX',    # Recovery/power boiler furnace
        'HEADBOX':     'BOX',    # Headbox main chamber
        'REFINER':     'BOX',    # Refiner housing
        'PAPER_MACHINE': 'CYLI', # Dryer cylinders, rolls are CYLI
        'PUMP':        'BOX',    # Pump casing
    }

    def __init__(self, knowledge_base: Optional[PMLKnowledgeBase] = None):
        self.kb = knowledge_base or PMLKnowledgeBase()

    def generate(self, intent: DesignIntent, model: str = "deepseek-v4-flash") -> str:
        """Generate a complete PML script from DesignIntent."""
        lines = []
        lines.append("-- ============================================")
        lines.append("-- E3D Paper Mill AI Agent - Auto-generated PML Script")
        lines.append(f"-- Generated: {datetime.now().isoformat()}")
        lines.append(f"-- Source: {intent.source_file or 'natural language description'}")
        lines.append(f"-- Target project: {intent.project}")
        lines.append(f"-- Target zone: {intent.zone}")
        lines.append("-- Units: mm | E=machine direction N=cross-machine U=vertical")
        lines.append("-- ============================================")
        lines.append("")

        # 1. Header and rendering control
        lines.extend(self._generate_header(intent))

        # 2. Prerequisite notes
        lines.extend(self._generate_zone_setup(intent))

        # 3. Generate element code
        for elem in intent.elements:
            elem_lines = self._generate_element(elem, intent)
            lines.extend(elem_lines)
            lines.append("")

        # 4. Connections
        if intent.connections:
            lines.append("-- === Connections ===")
            for conn in intent.connections:
                conn_type = conn[2] if len(conn) > 2 else 'DEFAULT'
                lines.append(f"-- CONNECT: {conn[0]} -> {conn[1]} ({conn_type})")
            lines.append("")

        # 5. Notes
        for note in intent.notes:
            lines.append(f"-- NOTE: {note}")

        # 6. Footer
        lines.append("")
        lines.append("-- === End of script ===")
        lines.append("-- Please review before executing in E3D!")

        pml_script = "\n".join(lines)

        # Auto-validate
        errors = self.validate(pml_script)
        if errors:
            warning_lines = ["", "-- !!! Validation warning: banned syntax detected !!!"]
            for err in errors:
                warning_lines.append(f"-- {err}")
            warning_lines.append("-- !!! Please fix before executing !!!")
            pml_script += "\n".join(warning_lines)

        return pml_script

    def _generate_header(self, intent: DesignIntent) -> List[str]:
        """Generate script header with rendering optimization."""
        # No rendering-control prologue. ALPHA HEADER, VAR 0, SUSPEND and RESUME
        # are not E3D Design commands - none appears as a command anywhere in
        # AVEVA's PML library - and each aborts the macro on its own line with
        # "(47,15) CP: Syntax error".
        return [
            "-- Project setup",
            f"-- Project: {intent.project}",
            "",
        ]

    def _generate_zone_setup(self, intent: DesignIntent) -> List[str]:
        """Prerequisite notes for PML1 macro mode."""
        return [
            f"-- Prerequisite: select a writable ZONE ({intent.zone}) in E3D first",
            f"-- Execution: $$MACRO <path to this script>",
            "",
        ]

    def _generate_element(self, elem: DesignElement, intent: DesignIntent) -> List[str]:
        """Generate PML code for a single element."""
        if elem.type == "PIPE":
            return self._generate_pipe(elem)
        elif elem.type in ("EQUIPMENT", "VESSEL", "PUMP", "HEATEX",
                           "COMPRESSOR", "FILTER", "COLUMN"):
            return self._generate_equipment(elem)
        elif elem.type == "VALVE":
            return self._generate_valve(elem)
        elif elem.type == "NOZZLE":
            return self._generate_nozzle(elem)
        elif elem.type == "INSTRUMENT":
            return [f"-- INSTRUMENT: {elem.name} — add manually in E3D Design"]
        elif elem.type == "STRUCTURE":
            return self._generate_structure(elem)
        else:
            return [
                f"-- Unknown element type '{elem.type}': {elem.name} — create manually",
                f"-- Suggested type: {self._suggest_type(elem.label)}",
            ]

    def _generate_equipment(self, elem: DesignElement) -> List[str]:
        """Generate equipment PML code (PML1: NEW EQUI + primitives)."""
        lines = []
        name = elem.name.replace(' ', '_').replace('-', '_')
        lines.append(f"-- Create equipment: {elem.name} ({elem.category or elem.type})")
        lines.append(f"NEW EQUI /{name}")

        # Determine primitive based on equipment category
        primitive = self.EQUIPMENT_PRIMITIVE.get(elem.category, 'BOX')

        e = elem.east or 0
        n = elem.north or 0
        u = elem.up or 0

        if primitive == 'CYLI':
            d = elem.width or 1000
            h = elem.height or 2000
            lines.append("NEW CYLI")
            lines.append(f"DIAM {d}")
            lines.append(f"HEIG {h}")
            # Iron Rule 1: ORI must precede POS. With the reverse order E3D
            # rotates the position vector and the element drifts silently.
            lines.append("ORI Z IS U AND Y IS N")
            lines.append(f"POS E {e} N {n} U {u}")
        else:
            lines.append("NEW BOX")
            lines.append(f"XLEN {elem.width or 1000}")
            lines.append(f"YLEN {elem.depth or 1000}")
            lines.append(f"ZLEN {elem.height or 2000}")
            lines.append(f"POS E {e} N {n} U {u}")

        lines.append(f"-- Equipment {elem.name} created successfully")
        return lines

    def _generate_pipe(self, elem: DesignElement) -> List[str]:
        """Generate pipe notes (pipe routing is interactive in E3D)."""
        return [
            f"-- Pipe: {elem.name} (BORE={elem.bore or 'TBD'}, SPEC={elem.spec or 'TBD'})",
            f"-- Note: pipe routing must be created manually in E3D Design interactive mode",
            f"-- Start point: E {elem.east or 0} N {elem.north or 0} U {elem.up or 0}",
        ]

    def _generate_valve(self, elem: DesignElement) -> List[str]:
        """Generate valve notes."""
        return [
            f"-- Valve: {elem.name} (BORE={elem.bore or 'TBD'})",
            f"-- Note: valves must be added manually to pipe routing in E3D Design",
            f"-- Position: E {elem.east or 0} N {elem.north or 0} U {elem.up or 0}",
        ]

    def _generate_nozzle(self, elem: DesignElement) -> List[str]:
        """Generate nozzle geometry (PML1: NEW EQUI + NEW CYLI)."""
        name = elem.name.replace(' ', '_').replace('-', '_')
        d = elem.bore or 150
        return [
            f"-- Nozzle: {elem.name}",
            f"NEW EQUI /{name}",
            "NEW CYLI",
            f"DIAM {d}",
            f"HEIG 200",
            # Iron Rule 1: ORI before POS, or the nozzle drifts off the vessel.
            "ORI Z IS E AND Y IS U",
            f"POS E {elem.east or 0} N {elem.north or 0} U {elem.up or 0}",
        ]

    def _generate_structure(self, elem: DesignElement) -> List[str]:
        """Generate structure geometry (PML1: NEW EQUI + NEW BOX)."""
        name = elem.name.replace(' ', '_').replace('-', '_')
        return [
            f"-- Structure: {elem.name}",
            f"NEW EQUI /{name}",
            "NEW BOX",
            f"XLEN {elem.width or 6000}",
            f"YLEN {elem.depth or 300}",
            f"ZLEN {elem.height or 300}",
            f"POS E {elem.east or 0} N {elem.north or 0} U {elem.up or 0}",
        ]

    def _suggest_type(self, label: str) -> str:
        """Recommend element type based on label."""
        from ..drawing_parser import SVGParser
        return SVGParser()._infer_type(label)

    def validate(self, pml_script: str) -> list:
        """
        Check a PML script for syntax that would break E3D. Returns one message
        per problem; an empty list means it passed.

        Delegates to :func:`wsb.pml_builder.validate_pml`, which checks all three
        primitive types rather than CYLI alone, tracks each primitive block to
        its true end instead of a fixed 8-line window, and does not flag banned
        terms that appear inside comments.
        """
        from ..wsb.pml_builder import validate_pml

        return validate_pml(pml_script)

    def generate_from_description(self, description: str) -> str:
        """Generate PML script directly from natural language description."""
        from ..drawing_parser import NaturalLanguageParser
        intent = NaturalLanguageParser.parse(description)
        self._enrich_with_llm(intent, description)
        return self.generate(intent)

    def _enrich_with_llm(self, intent: DesignIntent, description: str):
        """Enhance design intent with knowledge base retrieval."""
        low_conf = [e for e in intent.elements if e.confidence < 0.6]
        if not low_conf:
            return

        kb_results = self.kb.search(description)
        if kb_results:
            intent.notes.append(
                f"Knowledge base: refer to '{kb_results[0]['source']}' — "
                f"{kb_results[0]['chunk'][:100]}"
            )

        for elem in low_conf:
            if elem.type == "EQUIPMENT" and not elem.width:
                elem.width = 1000
                elem.depth = 1000
                elem.height = 2000
                elem.confidence = 0.5
                intent.notes.append(
                    f"[AI] Supplemented default dimensions for {elem.name}"
                )

    def save_script(self, script: str, filepath: str = None) -> str:
        """Save PML script to file."""
        from ..config import ensure_output_dir
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = str(ensure_output_dir() / f"e3d_auto_{timestamp}.pml")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(script)
        return filepath
