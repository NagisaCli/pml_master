"""
PML 代码生成器
==============
从 DesignIntent（图纸解析/自然语言）生成可执行的 PML 脚本。
使用知识库 + 模板 + LLM 的组合策略。

语法规范: PML1 (E3D 3.1 $$MACRO 模式)
禁止列表: !!Alert $P ENDS END EQUI NAME = DESC = !var = COLLECT UNSET !!CE !!WORLD
"""

from typing import Dict, List, Optional
import re
from datetime import datetime

from ..drawing_parser import DesignIntent, DesignElement
from ..pml_knowledge import PMLKnowledgeBase


class PMLGenerator:
    """
    PML 代码生成器。

    策略：
    1. 模板匹配 — 使用预定义模板处理常见建模模式
    2. 知识检索 — 从 PMLKnowledgeBase 查找相关语法
    3. LLM 生成 — 复杂/未匹配的请求通过 LLM 补充

    语法要求:
    - 仅使用 PML1 语法 (NEW EQUI / NEW CYLI / NEW BOX / NEW CONE / NEW DISH)
    - 禁止所有 PML2 语法 (变量赋值、COLLECT、UNSET、!!CE 等)
    - 生成前自动校验，确保零 PML2 残留
    """

    # PML2 禁止语法列表
    BANNED_SYNTAX = [
        '!!Alert', '$P', 'ENDS', 'END EQUI', 'NAME =', 'DESC =',
        '!var =', 'COLLECT', 'UNSET', '!!CE', '!!WORLD',
    ]

    def __init__(self, knowledge_base: Optional[PMLKnowledgeBase] = None):
        self.kb = knowledge_base or PMLKnowledgeBase()

    def generate(self, intent: DesignIntent, model: str = "deepseek-v4-flash") -> str:
        """
        从 DesignIntent 生成完整的 PML 脚本。

        Args:
            intent: 设计意图
            model: 使用的 LLM 模型名

        Returns:
            PML 脚本字符串
        """
        lines = []
        lines.append("-- ============================================")
        lines.append(f"-- E3D AI Agent 自动生成 PML 脚本")
        lines.append(f"-- 生成时间: {datetime.now().isoformat()}")
        lines.append(f"-- 数据来源: {intent.source_file or '自然语言描述'}")
        lines.append(f"-- 目标项目: {intent.project}")
        lines.append(f"-- 目标区域: {intent.zone}")
        lines.append("-- 单位: mm | E=轴向 N=横向 U=垂直")
        lines.append("-- ============================================")
        lines.append("")

        # 1. 环境设置
        lines.extend(self._generate_header(intent))

        # 2. 前置条件提示（替代原 PML2 区域创建）
        lines.extend(self._generate_zone_setup(intent))

        # 3. 生成元素代码
        for elem in intent.elements:
            elem_lines = self._generate_element(elem, intent)
            lines.extend(elem_lines)
            lines.append("")

        # 4. 生成连接代码
        if intent.connections:
            lines.append("-- === 连接 === ")
            for conn in intent.connections:
                lines.append(f"-- CONNECT: {conn[0]} -> {conn[1]} ({conn[2] if len(conn) > 2 else 'DEFAULT'})")
            lines.append("")

        # 5. 备注
        for note in intent.notes:
            lines.append(f"-- NOTE: {note}")

        lines.append("")
        lines.append("-- === 恢复渲染与视图刷新 ===")
        lines.append("RESUME")
        lines.append("RECREATE")
        lines.append("ALPHA HEADER ON")
        lines.append("-- === 脚本结束 ===")
        lines.append("-- 请检查脚本后再执行！")

        pml_script = "\n".join(lines)

        # 自动校验: 确保零 PML2 残留
        errors = self.validate(pml_script)
        if errors:
            warning_lines = ["", "-- !!! 校验警告: 发现禁止语法 !!!"]
            for err in errors:
                warning_lines.append(f"-- {err}")
            warning_lines.append("-- !!! 请修正后再执行 !!!")
            pml_script += "\n".join(warning_lines)

        return pml_script

    def _generate_header(self, intent: DesignIntent) -> List[str]:
        """生成脚本头部（注释信息与性能优化指令）。"""
        lines = []
        lines.append("-- 项目设置与高性能加载控制")
        lines.append(f"-- 项目: {intent.project}")
        lines.append("ALPHA HEADER OFF")
        lines.append("VAR 0")
        lines.append("SUSPEND")
        lines.append("")
        return lines

    def _generate_zone_setup(self, intent: DesignIntent) -> List[str]:
        """前置条件提示（PML1 宏模式下不可编程创建区域）。"""
        return [
            f"-- 前置条件: 请先在 E3D 中选择可写 ZONE ({intent.zone})",
            f"-- 执行方式: $$MACRO <本脚本路径>",
            "",
        ]

    def _generate_element(self, elem: DesignElement, intent: DesignIntent) -> List[str]:
        """生成单个元素的 PML 代码。"""
        lines = []

        if elem.type == "PIPE":
            lines.extend(self._generate_pipe(elem))
        elif elem.type in ("EQUIPMENT", "VESSEL", "PUMP", "HEATEX", "COMPRESSOR", "FILTER", "COLUMN"):
            lines.extend(self._generate_equipment(elem))
        elif elem.type == "VALVE":
            lines.extend(self._generate_valve(elem))
        elif elem.type == "NOZZLE":
            lines.extend(self._generate_nozzle(elem))
        elif elem.type == "INSTRUMENT":
            lines.append(f"-- INSTRUMENT: {elem.name} — 仪表需要在 E3D Design 中手动添加")
        elif elem.type == "STRUCTURE":
            lines.extend(self._generate_structure(elem))
        else:
            lines.append(f"-- 未知元素类型 '{elem.type}': {elem.name} — 请手动创建")
            lines.append(f"-- 建议类型: {self._suggest_type(elem.label)}")

        return lines

    def _generate_equipment(self, elem: DesignElement) -> List[str]:
        """生成设备 PML 代码（PML1: NEW EQUI + NEW CYLI / NEW BOX）。"""
        lines = []
        name = elem.name.replace(' ', '_').replace('-', '_')
        lines.append(f"-- 创建设备: {elem.name}")
        lines.append(f"NEW EQUI /{name}")

        # 根据设备类型选择基本体
        if elem.type in ('VESSEL', 'COLUMN') or (elem.width and not elem.depth):
            # 圆形设备用 CYLI
            d = elem.width or 1000
            h = elem.height or 2000
            lines.append("NEW CYLI")
            lines.append(f"DIAM {d}")
            lines.append(f"HEIG {h}")
        else:
            # 矩形设备用 BOX
            lines.append("NEW BOX")
            lines.append(f"XLEN {elem.width or 1000}")
            lines.append(f"YLEN {elem.depth or 1000}")
            lines.append(f"ZLEN {elem.height or 2000}")

        e = elem.east or 0
        n = elem.north or 0
        u = elem.up or 0
        lines.append(f"POS E {e} N {n} U {u}")

        # CYLI 需要方向
        if elem.type in ('VESSEL', 'COLUMN') or (elem.width and not elem.depth):
            lines.append("ORI Y IS U AND Z IS N")

        lines.append(f"-- 设备 {elem.name} ({elem.type}) 创建完成")
        return lines

    def _generate_pipe(self, elem: DesignElement) -> List[str]:
        """生成管道注释提示（PML1 宏模式下无法直接创建管道路由）。"""
        return [
            f"-- 管道: {elem.name} (BORE={elem.bore or 'TBD'}, SPEC={elem.spec or 'TBD'})",
            f"-- 注意: 管道路由需在 E3D Design 交互模式下手动创建",
            f"-- 起点: E {elem.east or 0} N {elem.north or 0} U {elem.up or 0}",
        ]

    def _generate_valve(self, elem: DesignElement) -> List[str]:
        """生成阀门注释提示（PML1 宏模式下无法直接创建阀门）。"""
        return [
            f"-- 阀门: {elem.name} (BORE={elem.bore or 'TBD'}, SPEC={elem.spec or 'TBD'})",
            f"-- 注意: 阀门需在 E3D Design 交互模式下手动添加到管道路由中",
            f"-- 位置: E {elem.east or 0} N {elem.north or 0} U {elem.up or 0}",
        ]

    def _generate_nozzle(self, elem: DesignElement) -> List[str]:
        """生成管口几何（PML1: NEW EQUI + NEW CYLI）。"""
        name = elem.name.replace(' ', '_').replace('-', '_')
        d = elem.bore or 150
        lines = [
            f"-- 管口: {elem.name}",
            f"NEW EQUI /{name}",
            "NEW CYLI",
            f"DIAM {d}",
            f"HEIG 200",
            f"POS E {elem.east or 0} N {elem.north or 0} U {elem.up or 0}",
            "ORI Y IS E AND Z IS U",
        ]
        return lines

    def _generate_structure(self, elem: DesignElement) -> List[str]:
        """生成结构几何（PML1: NEW EQUI + NEW BOX）。"""
        name = elem.name.replace(' ', '_').replace('-', '_')
        lines = [
            f"-- 结构: {elem.name}",
            f"NEW EQUI /{name}",
            "NEW BOX",
            f"XLEN {elem.width or 6000}",
            f"YLEN {elem.depth or 300}",
            f"ZLEN {elem.height or 300}",
            f"POS E {elem.east or 0} N {elem.north or 0} U {elem.up or 0}",
        ]
        return lines

    def _suggest_type(self, label: str) -> str:
        """根据标签推荐元素类型。"""
        from ..drawing_parser import SVGParser
        return SVGParser()._infer_type(label)

    def validate(self, pml_script: str) -> list:
        """
        检查 PML 脚本中的禁止语法，返回错误列表。

        对照 AGENTS.md 禁止列表 + PML2 变量赋值模式进行扫描。
        空列表表示通过校验。
        """
        errors = []
        for i, line in enumerate(pml_script.split('\n'), 1):
            for b in self.BANNED_SYNTAX:
                if b in line:
                    errors.append(f'L{i}: 禁止语法 "{b}" → {line.strip()}')
        # 检查 PML2 变量赋值模式: !xxx = yyy
        for i, line in enumerate(pml_script.split('\n'), 1):
            if re.match(r'\s*![a-zA-Z]', line) and '=' in line:
                errors.append(f'L{i}: PML2变量赋值 → {line.strip()}')

        # 检查 PML1 命令顺序 (NEW CYLI 中 ORI 必须在 POS 之前)
        lines_list = pml_script.split('\n')
        for i, line in enumerate(lines_list):
            if line.strip() == "NEW CYLI":
                chunk = lines_list[i:i+8]
                ori_idx = -1; pos_idx = -1
                for c_i, c_l in enumerate(chunk):
                    if c_l.strip().startswith("ORI "): ori_idx = c_i
                    elif c_l.strip().startswith("POS "): pos_idx = c_i
                if ori_idx != -1 and pos_idx != -1 and pos_idx < ori_idx:
                    errors.append(f'L{i+1}: 语法顺序错误 (POS 在 ORI 之前导致飘移) → {chunk[pos_idx].strip()}')

        return errors

    def generate_from_description(self, description: str) -> str:
        """
        从自然语言描述直接生成 PML 脚本。
        综合使用知识库检索 + 模板 + LLM 生成。
        """
        from ..drawing_parser import NaturalLanguageParser
        intent = NaturalLanguageParser.parse(description)
        # 用 LLM 增强意图理解
        self._enrich_with_llm(intent, description)
        return self.generate(intent)

    def _enrich_with_llm(self, intent: DesignIntent, description: str):
        """
        使用 LLM 增强设计意图。
        当模板匹配不足时，通过 LLM 补充参数。
        """
        # 检查是否有低置信度的元素需要增强
        low_conf = [e for e in intent.elements if e.confidence < 0.6]
        if not low_conf:
            return

        # 检索相关知识
        kb_results = self.kb.search(description)
        if kb_results:
            intent.notes.append(f"知识库提示: 参考 '{kb_results[0]['source']}' — {kb_results[0]['chunk'][:100]}")

        # 此处留出 LLM 接口，后续可接入 Hermes LLM
        # 目前简单补充常见默认值
        for elem in low_conf:
            if elem.type == "EQUIPMENT" and not elem.width:
                elem.width = 1000
                elem.depth = 1000
                elem.height = 2000
                elem.confidence = 0.5
                intent.notes.append(f"[AI] 为 {elem.name} 补充了默认尺寸 1000x1000x2000")

    def save_script(self, script: str, filepath: str = None) -> str:
        """保存 PML 脚本到文件。"""
        from ..config import PML_OUTPUT_DIR
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = str(PML_OUTPUT_DIR / f"e3d_auto_{timestamp}.pml")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(script)
        return filepath
