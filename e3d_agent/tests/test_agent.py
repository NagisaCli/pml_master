#!/usr/bin/env python3
"""E3D Agent 快速测试"""
if __name__ != "__main__":
    import unittest
    raise unittest.SkipTest("手动冒烟脚本；请显式运行，不参与自动化回归测试")

import sys
sys.path.insert(0, '.')
from e3d_agent.agent import E3DAgent

agent = E3DAgent()
print(agent.summary())
print()

# 测试 1: 自然语言
print("=== 测试: 自然语言 → PML ===")
result = agent.run("在 AREA_100 区域创建一台直径2米高5米的立式储罐 T-101")
print(f"元素数: {result['elements_count']}")
script = result['pml_script']
# 只显示关键部分
for line in script.split('\n'):
    if 'NEW' in line or 'NAME' in line or 'POSITION' in line or 'WIDTH' in line or 'HEIGHT' in line:
        print(f"  {line.strip()}")
print(f"... 共 {len(script.split(chr(10)))} 行")
print()

# 测试 2: 查询知识库
print("=== 测试: 知识库查询 ===")
results = agent.query_knowledge("如何创建管道")
for r in results[:2]:
    print(f"  [{r['source']}] 相关度={r['relevance']}")
print()

# 测试 3: 记忆系统
print("=== 测试: 记忆系统 ===")
stats = agent.memory.get_stats()
print(f"  记忆条目: {stats['total']}")
print(f"  类型分布: {stats['by_type']}")
print()

# 测试 4: SVG 解析（如果文件存在）
import os
svg_files = []
for root, dirs, files in os.walk('D:/AVEVA/Projects/E3D3.1/AvevaMarineSample/amsdia'):
    for f in files:
        if f.endswith('.svg'):
            svg_files.append(os.path.join(root, f))
    break

if svg_files:
    svg_path = svg_files[0]
    print(f"=== 测试: SVG 图纸解析 ({os.path.basename(svg_path)}) ===")
    result = agent.run_from_drawing(svg_path)
    print(f"  元素数: {result['elements_count']}")
    print(f"  连接数: {result['connections_count']}")
    print(f"  系统: {result.get('zone', 'N/A')}")
    for line in result['pml_script'].split('\n')[:5]:
        print(f"  {line}")
else:
    print("(无 SVG 文件可测试)")

print()
print("=== 全部测试完成 ===")
print(agent.summary())
