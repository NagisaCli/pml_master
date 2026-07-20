"""
E3D AI Agent 主编排器
=====================
端到端流程：
  图纸/自然语言 → 解析 → 知识检索 → PML 生成 → E3D 执行 → 记忆学习
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
    E3D AI Agent 主编排器。

    使用示例:
        agent = E3DAgent()
        
        # 从自然语言建模
        agent.run("在 AREA_100 创建一台直径2m高5m的储罐 T-101")
        
        # 从图纸建模
        agent.run_from_drawing("path/to/pid.pdf")
        
        # 从 SVG 系统图建模
        agent.run_from_drawing("path/to/system.svg")
    """

    def __init__(self, memory_path: Optional[Path] = None):
        # 初始化各模块
        self.memory = MemoryStore(memory_path or MEMORY_DB_PATH)
        self.knowledge_base = PMLKnowledgeBase()
        self.pml_generator = PMLGenerator(self.knowledge_base)
        self.e3d = E3DInterface(self.memory)
        self.drawing_parser = DrawingParserFactory()

        # 记录会话
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._log("info", "E3D Agent 初始化完成", {
            "knowledge_docs": list(self.knowledge_base.documents.keys()),
            "e3d_available": self.e3d.e3d_available,
            "memory_entries": self.memory.get_stats()["total"],
        })

    # ── 主入口 ────────────────────────────────

    def run(self, user_input: str, execute: bool = False) -> Dict:
        """
        主入口：接收自然语言或文件路径，执行完整流水线。

        Args:
            user_input: 自然语言描述 或 图纸文件路径
            execute: 是否尝试在 E3D 中执行（默认 False=仅生成脚本）

        Returns:
            执行结果字典
        """
        self._log("info", f"收到输入: {user_input[:200]}")

        # Step 1: 判断输入类型
        if self._is_file_path(user_input):
            return self.run_from_drawing(user_input, execute)
        else:
            return self.run_from_description(user_input, execute)

    def run_from_description(self, description: str, execute: bool = False) -> Dict:
        """从自然语言描述启动流水线。"""
        self._log("info", "模式: 自然语言描述 → PML")

        # 1. 解析自然语言
        intent = NaturalLanguageParser.parse(description)

        # 2. 检索知识库补充
        self._enrich_from_knowledge(intent, description)

        # 3. 生成 PML 脚本
        script = self.pml_generator.generate(intent)

        # 4. 执行或保存
        return self._finalize(script, intent, execute)

    def run_from_drawing(self, file_path: str, execute: bool = False) -> Dict:
        """从图纸文件启动流水线。"""
        self._log("info", f"模式: 图纸解析 → PML ({file_path})")

        # 1. 解析图纸
        intent = self.drawing_parser.parse(file_path)
        self._log("info", f"图纸解析结果: {len(intent.elements)} 元素, {len(intent.connections)} 连接")

        # 2. 知识库增强
        self._enrich_from_knowledge(intent, file_path)

        # 3. 生成 PML
        script = self.pml_generator.generate(intent)

        # 4. 执行或保存
        return self._finalize(script, intent, execute)

    def run_svg_drawing(self, svg_file: str, execute: bool = False) -> Dict:
        """专门处理项目已有的 SVG 系统图。"""
        return self.run_from_drawing(svg_file, execute)

    def run_pdf_pid(self, pdf_file: str, execute: bool = False) -> Dict:
        """专门处理 PDF P&ID。"""
        return self.run_from_drawing(pdf_file, execute)

    # ── 内部流水线 ───────────────────────────

    def _enrich_from_knowledge(self, intent: DesignIntent, context: str):
        """用知识库补充设计意图。"""
        # 搜索相关 PML 知识
        results = self.knowledge_base.search(context)
        if results:
            best = results[0]
            intent.notes.append(f"[知识库] 参考文档: {best['source']} (相关度: {best['relevance']})")
            # 检查是否有可用的元素类型
            for elem in intent.elements:
                if elem.type == "EQUIPMENT" and not elem.category:
                    # 尝试从知识中推断更具体的类型
                    pass

    def _finalize(self, script: str, intent: DesignIntent, execute: bool) -> Dict:
        """执行或保存脚本，返回结果。"""
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
            # 尝试在 E3D 中执行
            exec_result = self.e3d.execute_cmd_mode(script)
            result["execute_mode"] = "cmd"
            result["execution"] = exec_result
            if not exec_result["success"]:
                self.memory.add_error(
                    module="Agent.execute",
                    error_text=exec_result.get("error", "未知错误"),
                    context={"script": script[:500], "intent": intent.to_dict()},
                )
        else:
            # 文件模式：保存脚本
            filepath = self.e3d.execute_file_mode(script)
            result["execute_mode"] = "file"
            result["script_file"] = filepath
            if not execute:
                result["note"] = "已生成 PML 脚本。将 execute=True 传入 run() 可尝试在 E3D 中自动执行。"

        # 保存成功的模式到记忆
        self.memory.add_pattern(
            name=intent.zone,
            description=f"从 {intent.source_file or '自然语言'} 生成的建模模式",
            pml_code=script[:500],
            success=True,
        )

        return result

    # ── 查询工具 ─────────────────────────────

    def query_knowledge(self, question: str) -> List[Dict]:
        """直接查询 PML 知识库。"""
        return self.knowledge_base.search(question)

    def get_memory_report(self) -> str:
        """获取记忆报告（含未处理错误）。"""
        return self.memory.export_to_markdown()

    def get_unresolved_errors(self) -> List[Dict]:
        """获取所有待人工处理的错误。"""
        return self.memory.get_unresolved_errors()

    def review_and_learn(self, error_id: str, resolution: str):
        """人工审核错误后标记解决，Agent 从中学习。"""
        success = self.memory.mark_resolved(error_id, resolution)
        if success:
            self.memory.add_lesson(
                topic=f"error_{error_id}",
                lesson=resolution,
            )
        return success

    # ── 辅助 ─────────────────────────────────

    def _is_file_path(self, text: str) -> bool:
        """判断输入是否为文件路径。"""
        text = text.strip().lower()
        return any(text.endswith(ext) for ext in ['.pdf', '.svg', '.dwg', '.dxf', '.png', '.jpg'])

    def _log(self, level: str, message: str, data: Dict = None):
        """内部日志。"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{timestamp}][{level.upper()}]"
        print(f"{prefix} {message}", file=sys.stderr)
        if data:
            for k, v in data.items():
                print(f"  {k}: {v}", file=sys.stderr)

    def summary(self) -> str:
        """打印 Agent 状态摘要。"""
        stats = self.memory.get_stats()
        unresolved = stats.get("unresolved_errors", 0)
        lines = [
            "╔══════════════════════════════════════════╗",
            "║       E3D AI Agent 状态摘要              ║",
            "╠══════════════════════════════════════════╣",
            f"║  知识库文档: {len(self.knowledge_base.documents)} 篇              ║",
            f"║  记忆条目:   {stats['total']} 条                 ║",
            f"║  待处理错误: {unresolved} 个                  ║",
            f"║  E3D 可用:   {'是' if self.e3d.e3d_available else '否'}                    ║",
            f"║  会话 ID:    {self.session_id}  ║",
            "╚══════════════════════════════════════════╝",
        ]
        return "\n".join(lines)


# ── CLI 入口 ──────────────────────────────────

def main():
    """命令行入口。"""
    import argparse

    parser = argparse.ArgumentParser(
        description="E3D AI Agent — 自然语言/图纸 → AVEVA E3D 自动建模"
    )
    parser.add_argument("input", nargs="?", help="自然语言描述 或 图纸文件路径")
    parser.add_argument("--execute", "-e", action="store_true",
                        help="尝试在 E3D 中执行（需安装 E3D Design）")
    parser.add_argument("--file", "-f", help="指定图纸文件路径")
    parser.add_argument("--svg", help="指定 SVG 系统图路径")
    parser.add_argument("--pdf", help="指定 PDF P&ID 路径")
    parser.add_argument("--query", "-q", help="查询知识库")
    parser.add_argument("--memory", "-m", action="store_true",
                        help="显示记忆报告")
    parser.add_argument("--errors", action="store_true",
                        help="显示未处理的错误")
    parser.add_argument("--summary", "-s", action="store_true",
                        help="显示 Agent 状态摘要")

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
            print(f"未处理错误 ({len(errors)}):")
            for e in errors:
                print(f"  [{e['id']}] {e['error']}")
        else:
            print("没有未处理的错误。")
        return

    if args.query:
        results = agent.query_knowledge(args.query)
        print(f"\n知识库搜索结果 (查询: '{args.query}'):\n")
        for r in results:
            print(f"📖 {r['source']} (相关度: {r['relevance']})")
            print(f"   {r['chunk'][:200]}...\n")
        return

    # 输入来源优先级：--file > --svg > --pdf > positional
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

    # 输出结果
    print(f"\n{'='*60}")
    print(f"  E3D Agent 执行结果")
    print(f"{'='*60}")
    print(f"  项目:     {result['project']}")
    print(f"  区域:     {result['zone']}")
    print(f"  元素数:   {result['elements_count']}")
    print(f"  连接数:   {result['connections_count']}")
    print(f"  执行模式: {result['execute_mode']}")
    if result.get("script_file"):
        print(f"  脚本文件: {result['script_file']}")
    if result.get("execution"):
        print(f"  执行结果: {'成功' if result['execution']['success'] else '失败'}")
    if result.get("note"):
        print(f"  备注: {result['note']}")

    # 显示脚本预览
    script_lines = result['pml_script'].split('\n')
    preview = '\n'.join(script_lines[:15])
    print(f"\n  PML 脚本预览 (前15行):\n{preview}")
    if len(script_lines) > 15:
        print(f"  ... 共 {len(script_lines)} 行")

    # 检查是否有待处理错误
    errors = agent.get_unresolved_errors()
    if errors:
        print(f"\n  ⚠️ 有 {len(errors)} 个未处理的错误在记忆库中:")
        for e in errors[-3:]:
            print(f"     [{e['module']}] {e['error'][:100]}")
        print("     使用 agent.review_and_learn() 人工审核")


if __name__ == "__main__":
    main()
