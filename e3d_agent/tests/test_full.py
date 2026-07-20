#!/usr/bin/env python3
"""E3D Agent 完整测试"""
if __name__ != "__main__":
    import unittest
    raise unittest.SkipTest("手动端到端脚本；请显式运行，不参与自动化回归测试")

import sys
sys.path.insert(0, '.')
from e3d_agent.agent import E3DAgent
from e3d_agent.drawing_parser import SVGParser, NaturalLanguageParser
import os

agent = E3DAgent()
print("=" * 60)
print("  E3D AI Agent — 端到端测试")
print("=" * 60)

# ── 测试1: 自然语言 → PML ──────────────────
print("\n## 测试1: 自然语言描述 → PML 脚本生成\n")
nl = "在 AREA_100 区域创建一台直径2米高5米的立式储罐 T-101"
intent = NaturalLanguageParser.parse(nl)
print(f"  描述: {nl}")
print(f"  识别元素: {len(intent.elements)}")
for e in intent.elements:
    print(f"    - [{e.type}] {e.name} (cat={e.category}, size={e.width}x{e.depth}x{e.height}mm)")
for n in intent.notes:
    print(f"    > {n}")

result = agent.run(nl)
script_path = result.get("script_file", "N/A")
print(f"  PML 脚本文件: {script_path}")

# ── 测试2: SVG 图纸解析 ────────────────────
print("\n## 测试2: SVG 系统图解析\n")
svg_dir = "D:/AVEVA/Projects/E3D3.1/AvevaMarineSample/amsdia"
svg_files = [f for f in os.listdir(svg_dir) if f.endswith('.svg')]
if svg_files:
    svg_path = os.path.join(svg_dir, svg_files[0])
    print(f"  图纸: {svg_files[0]}")
    parser = SVGParser()
    intent = parser.parse(svg_path)
    pipes = [e for e in intent.elements if e.type == "PIPE"]
    equip = [e for e in intent.elements if e.type != "PIPE"]
    print(f"  设备/阀/仪表: {len(equip)} 个")
    print(f"  管道/管线:     {len(pipes)} 个")
    print(f"  系统名称:      {intent.system}")
    print("\n[OK] 测试完成！")
    for e in equip[:20]:
        print(f"    [{e.type:12s}] {e.name}")
    if len(equip) > 20:
        print(f"    ... 共 {len(equip)} 个")
    print(f"\n  关键管线:")
    for e in pipes[:15]:
        print(f"    {e.name}")
    if len(pipes) > 15:
        print(f"    ... 共 {len(pipes)} 个")
else:
    print("  (无 SVG 文件)")

# ── 测试3: 知识库检索 ──────────────────────
print("\n## 测试3: PML 知识库检索\n")
for query in ["创建设备", "管道建模", "NEW EQUIPMENT"]:
    results = agent.query_knowledge(query)
    print(f"  查询 '{query}': {len(results)} 条结果")
    for r in results[:1]:
        print(f"    → 参考文档: {r['source']} (相关度={r['relevance']})")

# ── 测试4: 记忆系统 ────────────────────────
print("\n## 测试4: 记忆系统\n")
agent.memory.add_lesson("equipment_modeling",
    "立式储罐使用 VESSEL 类型，GTYP=CYLINDER，直径=WIDTH=DEPTH，高度=HEIGHT",
    "!eqp = NEW VESSEL\n!eqp.GTYP = 'CYLINDER'\n!eqp.WIDTH = !eqp.DEPTH = 2000")
stats = agent.memory.get_stats()
print(f"  记忆条目: {stats['total']}")
print(f"  类型分布: {stats['by_type']}")

# ── 摘要 ────────────────────────────────────
print("\n" + agent.summary())
print("\n[OK] 全部测试完成")
