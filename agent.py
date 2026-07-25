"""
E3D Paper Mill AI Agent — Main Orchestrator
============================================
End-to-end pipeline:
  Description / Drawing → Parse → Knowledge Retrieval → PML Generation → E3D Execution → Memory Learning

Specialized for pulp and paper mill plant modeling:
  - Fourdrinier paper machines (all sections: headbox through reel)
  - Stock preparation (pulping, refining, screening, cleaning)
  - Chemical recovery (digesters, evaporators, recovery boiler, lime kiln)
  - Utilities (steam boilers, water treatment, pipe bridges)
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

from .config import MEMORY_DB_PATH
from .drawing_parser import (
    DrawingParserFactory, NaturalLanguageParser,
    DesignIntent,
)
from .pml_knowledge import PMLKnowledgeBase
from .pml_generator import PMLGenerator
from .e3d_interface import E3DInterface
from .memory import MemoryStore


class E3DAgent:
    """
    E3D Paper Mill AI Agent — main orchestrator.

    Usage examples:
        agent = E3DAgent()

        # Generate paper machine model from natural language
        agent.run("Create a 4800mm fourdrinier paper machine with 40 dryer cylinders")

        # Generate from a P&ID drawing
        agent.run_from_drawing("path/to/pid.pdf")

        # Generate from an SVG process diagram
        agent.run_from_drawing("path/to/process.svg")
    """

    def __init__(self, memory_path: Optional[Path] = None):
        # Initialize each module
        self.memory = MemoryStore(memory_path or MEMORY_DB_PATH)
        self.knowledge_base = PMLKnowledgeBase()
        self.pml_generator = PMLGenerator(self.knowledge_base)
        self.e3d = E3DInterface(self.memory)
        self.drawing_parser = DrawingParserFactory()

        # Record session
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._log("info", "E3D Paper Mill Agent initialized", {
            "knowledge_docs": list(self.knowledge_base.documents.keys()),
            "e3d_available": self.e3d.e3d_available,
            "memory_entries": self.memory.get_stats()["total"],
        })

    # -- Main entry ----------------------------------------------------

    def run(self, user_input: str, execute: bool = False) -> Dict:
        """
        Main entry: receives natural language or file path and executes the full pipeline.

        Args:
            user_input: natural language description or process diagram file path
            execute: whether to attempt execution in E3D (default False = generate script only)

        Returns:
            Result dictionary with PML script, file path, and execution status
        """
        self._log("info", f"Received input: {user_input[:200]}")

        # Step 1: Determine input type
        if self._is_file_path(user_input):
            return self.run_from_drawing(user_input, execute)
        else:
            return self.run_from_description(user_input, execute)

    def run_from_description(self, description: str, execute: bool = False) -> Dict:
        """Start the pipeline from a natural language description."""
        self._log("info", "Mode: natural language description → PML")

        # 1. Parse natural language
        intent = NaturalLanguageParser.parse(description)

        # 2. Retrieve knowledge base for enrichment
        self._enrich_from_knowledge(intent, description)

        # 3. Generate PML script
        script = self.pml_generator.generate(intent)

        # 4. Execute or save
        return self._finalize(script, intent, execute)

    def run_from_drawing(self, file_path: str, execute: bool = False) -> Dict:
        """Start the pipeline from a process diagram file."""
        self._log("info", f"Mode: drawing parsing → PML ({file_path})")

        # 1. Parse the drawing
        intent = self.drawing_parser.parse(file_path)
        self._log("info", f"Drawing parse result: {len(intent.elements)} elements, "
                  f"{len(intent.connections)} connections")

        # 2. Knowledge base enrichment
        self._enrich_from_knowledge(intent, file_path)

        # 3. Generate PML
        script = self.pml_generator.generate(intent)

        # 4. Execute or save
        return self._finalize(script, intent, execute)

    def run_svg_drawing(self, svg_file: str, execute: bool = False) -> Dict:
        """Handle SVG process system diagrams specifically."""
        return self.run_from_drawing(svg_file, execute)

    def run_pdf_pid(self, pdf_file: str, execute: bool = False) -> Dict:
        """Handle PDF P&IDs specifically."""
        return self.run_from_drawing(pdf_file, execute)

    # -- Internal pipeline --------------------------------------------------

    def _enrich_from_knowledge(self, intent: DesignIntent, context: str):
        """Enrich design intent using the paper mill knowledge base."""
        # Search for relevant PML and equipment knowledge
        results = self.knowledge_base.search(context)
        if results:
            best = results[0]
            intent.notes.append(
                f"[Knowledge base] Reference: {best['source']} "
                f"(relevance: {best['relevance']})"
            )

    def _finalize(self, script: str, intent: DesignIntent, execute: bool) -> Dict:
        """Execute or save the script and return the result."""
        result = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "project": intent.project,
            "zone": intent.zone,
            "elements_count": len(intent.elements),
            "connections_count": len(intent.connections),
            "pml_script": script,
            "execute_mode": "none",
        }

        if execute and self.e3d.e3d_available:
            # Attempt execution in E3D
            exec_result = self.e3d.execute_cmd_mode(script)
            result["execute_mode"] = "cmd"
            result["execution"] = exec_result
            if not exec_result["success"]:
                self.memory.add_error(
                    module="Agent.execute",
                    error_text=exec_result.get("error", "Unknown error"),
                    context={"script": script[:500], "intent": intent.to_dict()},
                )
        else:
            # File mode: save the script
            filepath = self.e3d.execute_file_mode(script)
            result["execute_mode"] = "file"
            result["script_file"] = filepath
            if not execute:
                result["note"] = (
                    "PML script generated. Pass execute=True to run() "
                    "to attempt automatic execution in E3D."
                )

        # Save successful patterns to memory
        self.memory.add_pattern(
            name=intent.zone,
            description=f"Modeling pattern from {intent.source_file or 'natural language'}",
            pml_code=script[:500],
            success=True,
        )

        return result

    # -- Query tools --------------------------------------------------------

    def query_knowledge(self, question: str) -> List[Dict]:
        """Query the paper mill PML knowledge base directly."""
        return self.knowledge_base.search(question)

    def get_memory_report(self) -> str:
        """Get a memory report including unresolved errors."""
        return self.memory.export_to_markdown()

    def get_unresolved_errors(self) -> List[Dict]:
        """Get all errors pending manual review."""
        return self.memory.get_unresolved_errors()

    def review_and_learn(self, error_id: str, resolution: str):
        """Mark an error as resolved after manual review; the Agent learns from it."""
        success = self.memory.mark_resolved(error_id, resolution)
        if success:
            self.memory.add_lesson(
                topic=f"error_{error_id}",
                lesson=resolution,
            )
        return success

    # -- Helpers ------------------------------------------------------------

    def _is_file_path(self, text: str) -> bool:
        """Determine whether the input is a file path."""
        text = text.strip().lower()
        return any(text.endswith(ext) for ext in ['.pdf', '.svg', '.dwg', '.dxf', '.png', '.jpg'])

    def _log(self, level: str, message: str, data: Dict = None):
        """Internal logging."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{timestamp}][{level.upper()}]"
        print(f"{prefix} {message}", file=sys.stderr)
        if data:
            for k, v in data.items():
                print(f"  {k}: {v}", file=sys.stderr)

    def summary(self) -> str:
        """Print the Agent status summary."""
        stats = self.memory.get_stats()
        unresolved = stats.get("unresolved_errors", 0)
        lines = [
            "+==============================================+",
            "|      E3D Paper Mill Agent Status Summary     |",
            "+==============================================+",
            f"|  Knowledge docs: {len(self.knowledge_base.documents):<28} |",
            f"|  Memory entries: {stats['total']:<28} |",
            f"|  Pending errors: {unresolved:<28} |",
            f"|  E3D available:  {'Yes' if self.e3d.e3d_available else 'No':<28} |",
            f"|  Session ID:     {self.session_id:<28} |",
            "+==============================================+",
        ]
        return "\n".join(lines)


# -- CLI entry ----------------------------------------------------

def main():
    """Command-line entry."""
    import argparse

    parser = argparse.ArgumentParser(
        description="E3D Paper Mill AI Agent — paper-making plant modeling for AVEVA E3D"
    )
    parser.add_argument("input", nargs="?",
                        help="Natural language description or process diagram file path")
    parser.add_argument("--execute", "-e", action="store_true",
                        help="Attempt execution in E3D (requires E3D Design installed)")
    parser.add_argument("--file", "-f", help="Specify drawing file path")
    parser.add_argument("--svg", help="Specify SVG process diagram path")
    parser.add_argument("--pdf", help="Specify PDF P&ID path")
    parser.add_argument("--query", "-q", help="Query the paper mill knowledge base")
    parser.add_argument("--memory", "-m", action="store_true",
                        help="Show memory report")
    parser.add_argument("--errors", action="store_true",
                        help="Show unresolved errors")
    parser.add_argument("--summary", "-s", action="store_true",
                        help="Show Agent status summary")

    args = parser.parse_args()

    agent = E3DAgent()

    if args.summary:
        print(agent.summary())
        return

    if args.memory:
        print(agent.get_memory_report())
        return

    if args.errors:
        errors = agent.get_unresolved_errors()
        if errors:
            print(f"Unresolved errors ({len(errors)}):")
            for e in errors:
                print(f"  [{e['id']}] {e['error']}")
        else:
            print("No unresolved errors.")
        return

    if args.query:
        results = agent.query_knowledge(args.query)
        print(f"\nKnowledge base search results (query: '{args.query}'):\n")
        for r in results:
            print(f"  {r['source']} (relevance: {r['relevance']})")
            print(f"   {r['chunk'][:200]}...\n")
        return

    # Input source priority: --file > --svg > --pdf > positional
    input_source = args.file or args.svg or args.pdf or args.input
    if not input_source:
        parser.print_help()
        return

    if args.svg:
        result = agent.run_svg_drawing(input_source, execute=args.execute)
    elif args.pdf:
        result = agent.run_pdf_pid(input_source, execute=args.execute)
    else:
        result = agent.run(input_source, execute=args.execute)

    # Output results
    print(f"\n{'='*60}")
    print(f"  E3D Paper Mill Agent Execution Result")
    print(f"{'='*60}")
    print(f"  Project:       {result['project']}")
    print(f"  Zone:          {result['zone']}")
    print(f"  Elements:      {result['elements_count']}")
    print(f"  Connections:   {result['connections_count']}")
    print(f"  Execute mode:  {result['execute_mode']}")
    if result.get("script_file"):
        print(f"  Script file:   {result['script_file']}")
    if result.get("execution"):
        exec_ok = "Success" if result['execution']['success'] else "Failed"
        print(f"  Execution:     {exec_ok}")
    if result.get("note"):
        print(f"  Note:          {result['note']}")

    # Show script preview
    script_lines = result['pml_script'].split('\n')
    preview = '\n'.join(script_lines[:15])
    print(f"\n  PML script preview (first 15 lines):\n{preview}")
    if len(script_lines) > 15:
        print(f"  ... {len(script_lines)} lines total")

    # Check for pending errors
    errors = agent.get_unresolved_errors()
    if errors:
        print(f"\n  Warning: {len(errors)} unresolved errors in memory store:")
        for e in errors[-3:]:
            print(f"     [{e['module']}] {e['error'][:100]}")
        print("     Use agent.review_and_learn() for manual review")


if __name__ == "__main__":
    main()
