#!/usr/bin/env python3
"""Quick E3D Agent smoke test."""
if __name__ != "__main__":
    import unittest
    raise unittest.SkipTest("manual smoke script; run explicitly, not in CI")

import sys
sys.path.insert(0, '.')
from e3d_agent.agent import E3DAgent

agent = E3DAgent()
print(agent.summary())
print()

# Test 1: natural language -> PML
print("=== Test: natural language -> PML ===")
result = agent.run("Create a vertical storage tank T-101 with diameter 2 m and height 5 m in AREA_100 zone")
print(f"element count: {result['elements_count']}")
script = result['pml_script']
# Show only the key lines
for line in script.split('\n'):
    if 'NEW' in line or 'NAME' in line or 'POSITION' in line or 'WIDTH' in line or 'HEIGHT' in line:
        print(f"  {line.strip()}")
print(f"... {len(script.split(chr(10)))} lines total")
print()

# Test 2: knowledge-base query
print("=== Test: knowledge-base query ===")
results = agent.query_knowledge("how to create piping")
for r in results[:2]:
    print(f"  [{r['source']}] relevance={r['relevance']}")
print()

# Test 3: memory system
print("=== Test: memory system ===")
stats = agent.memory.get_stats()
print(f"  memory entries: {stats['total']}")
print(f"  type distribution: {stats['by_type']}")
print()

# Test 4: SVG drawing parsing (if a file exists)
import os
svg_files = []
for root, dirs, files in os.walk('D:/AVEVA/Projects/E3D3.1/AvevaMarineSample/amsdia'):
    for f in files:
        if f.endswith('.svg'):
            svg_files.append(os.path.join(root, f))
    break

if svg_files:
    svg_path = svg_files[0]
    print(f"=== Test: SVG drawing parsing ({os.path.basename(svg_path)}) ===")
    result = agent.run_from_drawing(svg_path)
    print(f"  element count: {result['elements_count']}")
    print(f"  connection count: {result['connections_count']}")
    print(f"  system: {result.get('zone', 'N/A')}")
    for line in result['pml_script'].split('\n')[:5]:
        print(f"  {line}")
else:
    print("(no SVG file available to test)")

print()
print("=== All tests complete ===")
print(agent.summary())
