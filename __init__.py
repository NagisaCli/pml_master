"""
E3D AI Agent — 自然语言/图纸 → AVEVA E3D 建模自动化
=====================================================
Modules:
  drawing_parser  — 解析 PDF/DWG/SVG 设计图纸
  pml_knowledge   — PML 语法/模式知识库（长期记忆）
  pml_generator   — LLM → PML 代码生成
  e3d_interface   — E3D 交互接口（PML 执行 + .NET API）
  memory          — 错误/反馈持久化记忆
  agent           — 主编排器
"""

__version__ = "0.1.0"
