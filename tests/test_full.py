#!/usr/bin/env python3
"""E3D Agent end-to-end smoke test."""
if __name__ != "__main__":
    import unittest
    raise unittest.SkipTest("manual end-to-end script; run explicitly, not in CI")

import sys
sys.path.insert(0, '.')
from e3d_agent.agent import E3DAgent
from e3d_agent.drawing_parser import SVGParser, NaturalLanguageParser
import os

agent = E3DAgent()
print("=" * 60)
print("  E3D AI Agent - end-to-end test")
print("=" * 60)

# -- Test 1: natural language -> PML --------------------------------
print("\n## Test 1: natural-language description -> PML generation\n")
nl = "在 AREA_100 区域创建一台直径2米高5米的立式储罐 T-101"
intent = NaturalLanguageParser.parse(nl)
print(f"  description: {nl}")
print(f"  elements identified: {len(intent.elements)}")
for e in intent.elements:
    print(f"    - [{e.type}] {e.name} (cat={e.category}, size={e.width}x{e.depth}x{e.height}mm)")
for n in intent.notes:
    print(f"    > {n}")

result = agent.run(nl)
script_path = result.get("script_file", "N/A")
print(f"  PML script file: {script_path}")

# -- Test 2: SVG drawing parsing -------------------------------------
print("\n## Test 2: SVG system diagram parsing\n")
svg_dir = "D:/AVEVA/Projects/E3D3.1/AvevaMarineSample/amsdia"
svg_files = [f for f in os.listdir(svg_dir) if f.endswith('.svg')]
if svg_files:
    svg_path = os.path.join(svg_dir, svg_files[0])
    print(f"  drawing: {svg_files[0]}")
    parser = SVGParser()
    intent = parser.parse(svg_path)
    pipes = [e for e in intent.elements if e.type == "PIPE"]
    equip = [e for e in intent.elements if e.type != "PIPE"]
    print(f"  equipment/valves/instruments: {len(equip)}")
    print(f"  pipes/lines: {len(pipes)}")
    print(f"  system name: {intent.system}")
    print("\n[OK] test complete!")
    for e in equip[:20]:
        print(f"    [{e.type:12s}] {e.name}")
    if len(equip) > 20:
        print(f"    ... {len(equip)} total")
    print(f"\n  key lines:")
    for e in pipes[:15]:
        print(f"    {e.name}")
    if len(pipes) > 15:
        print(f"    ... {len(pipes)} total")
else:
    print("  (no SVG file available)")

# -- Test 3: knowledge-base retrieval ---------------------------------
print("\n## Test 3: PML knowledge-base retrieval\n")
for query in ["创建设备", "管道建模", "NEW EQUIPMENT"]:
    results = agent.query_knowledge(query)
    print(f"  query '{query}': {len(results)} results")
    for r in results[:1]:
        print(f"    -> reference: {r['source']} (relevance={r['relevance']})")

# -- Test 4: memory system --------------------------------------------
print("\n## Test 4: memory system\n")
agent.memory.add_lesson("equipment_modeling",
    "Vertical storage tanks use VESSEL type, GTYP=CYLINDER, "
    "diameter=WIDTH=DEPTH, height=HEIGHT",
    "!eqp = NEW VESSEL\n!eqp.GTYP = 'CYLINDER'\n!eqp.WIDTH = !eqp.DEPTH = 2000")
stats = agent.memory.get_stats()
print(f"  memory entries: {stats['total']}")
print(f"  type distribution: {stats['by_type']}")

# -- Summary ----------------------------------------------------------
print("\n" + agent.summary())
print("\n[OK] all tests complete")
