"""
设计图纸解析器
=============
支持 PDF P&ID、SVG 系统图、DWG 施工图的解析。
输出统一的 "设计意图" 数据结构，供 PML 生成器消费。
"""

from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger("e3d_agent.drawing_parser")


# ── 统一数据结构 ─────────────────────────────

@dataclass
class DesignElement:
    """从图纸中提取的单个设计元素。"""
    type: str           # EQUIPMENT / PIPE / NOZZLE / STRUCTURE / VALVE / INSTRUMENT
    name: str            # 元素名称/位号
    label: str = ""      # 标注文字
    category: str = ""   # 设备类型细分 (VESSEL/PUMP/TANK 等)
    east: float = 0      # X 坐标（如可用）
    north: float = 0     # Y 坐标
    up: float = 0        # Z 高度
    width: float = 0     # 尺寸
    depth: float = 0
    height: float = 0
    bore: float = 0      # 公称直径
    spec: str = ""       # 规格引用
    material: str = ""   # 材料
    connections: List[str] = field(default_factory=list)  # 连接到的其他元素名称
    source_svg: str = ""  # 来源 SVG 文件名
    properties: Dict[str, Any] = field(default_factory=dict)  # 额外属性
    confidence: float = 1.0  # 解析置信度 0-1

@dataclass
class DesignIntent:
    """完整的"设计意图"——可从图纸解析或自然语言描述生成。"""
    project: str = "AvevaMarineSample"  # 目标项目
    zone: str = "AREA_100"              # 目标区域
    system: str = ""                     # 系统名称
    elements: List[DesignElement] = field(default_factory=list)
    connections: List[tuple] = field(default_factory=list)  # (from, to, type)
    notes: List[str] = field(default_factory=list)
    source_file: str = ""

    def to_dict(self) -> dict:
        return {
            "project": self.project,
            "zone": self.zone,
            "system": self.system,
            "elements": [asdict(e) for e in self.elements],
            "connections": self.connections,
            "notes": self.notes,
            "source_file": self.source_file,
        }


# ── 图纸解析器基类 ───────────────────────────

class BaseParser:
    def can_parse(self, file_path: str) -> bool:
        raise NotImplementedError

    def parse(self, file_path: str) -> DesignIntent:
        raise NotImplementedError


# ── SVG 解析器（项目已有图纸）────────────────

class SVGParser(BaseParser):
    """解析 AVEVA Diagrams 导出的 SVG 系统原理图。"""

    def can_parse(self, file_path: str) -> bool:
        return str(file_path).lower().endswith(".svg")

    def parse(self, file_path: str) -> DesignIntent:
        intent = DesignIntent(source_file=str(file_path))
        try:
            from lxml import etree
            tree = etree.parse(file_path)
            root = tree.getroot()
            ns = {
                "svg": "http://www.w3.org/2000/svg",
                "v": "http://schemas.microsoft.com/visio/2003/SVGExtensions/",
                "pc": "http://www.aveva.com/PDMS/Compare2D3D/DrawingSVG",
            }

            # 1. 提取图纸元数据
            for meta in root.iter("{http://www.aveva.com/PDMS/Compare2D3D/DrawingSVG}drawing"):
                intent.system = meta.get("pc:number", "")
                # 从标题推断 project
                if "Marine" in intent.system or "/711R_" in intent.system:
                    intent.project = "AvevaMarineSample"

            # 2. 提取标题
            title_elem = root.find(".//svg:title", ns)
            if title_elem is not None and title_elem.text:
                intent.system = title_elem.text

            # 3. 提取所有设备/管道元素
            ns_all = {
                None: "http://www.w3.org/2000/svg",
                "v": "http://schemas.microsoft.com/visio/2003/SVGExtensions/",
            }

            # ── 标题栏/页眉排除列表 ──
            skip_labels = {
                "title", "drawing no", "department", "system", "func.",
                "created on", "created by", "sht.", "of", "status",
                "last modified on", "last modified by", "gsc",
                "tps marine training project",
            }

            for g in root.iter("{http://www.w3.org/2000/svg}g"):
                texts = g.findall(".//{http://www.w3.org/2000/svg}text")
                descs = g.findall(".//{http://www.w3.org/2000/svg}desc")
                paths = g.findall(".//{http://www.w3.org/2000/svg}path")
                rects = g.findall(".//{http://www.w3.org/2000/svg}rect")

                label = ""
                for t in texts:
                    if t.text and t.text.strip():
                        label = t.text.strip()
                        break
                if not label:
                    for d in descs:
                        if d.text and d.text.strip():
                            label = d.text.strip()
                            break

                # 跳过空标签、标题栏、日期、纯数字页码
                if not label:
                    continue
                label_lower = label.strip().lower()
                if label_lower in skip_labels:
                    continue
                if label_lower in ("1", "2", "3", "4", "5", "department",
                                    "title", "of", "status", "func."):
                    continue
                if any(c.isdigit() for c in label) and len(label) <= 4 and "/" not in label and "-" not in label:
                    # 隔离的日期/页码
                    if len(label) <= 10 and "/" not in label:
                        continue

                # 有 path+L 元素 → 管道连线
                has_line = any(
                    "L" in (p.get("d", "") or "")
                    for p in paths
                )
                has_shape = bool(rects)

                # 去重：同标签只保留第一个
                seen_names = {e.name for e in intent.elements}

                if has_line:
                    # 判断是设备还是管线
                    if self._looks_like_tag(label) or any(
                        kw in label.upper() for kw in ["PUMP", "FILTER", "EXCHANGER",
                                                        "PURIFIER", "EJECTOR", "CHEST",
                                                        "COOLER", "HEATER"]
                    ):
                        etype = self._infer_type(label)
                        if label not in seen_names:
                            intent.elements.append(DesignElement(
                                type=etype,
                                name=label,
                                label=label,
                                source_svg=str(file_path),
                                confidence=0.7,
                            ))
                    else:
                        if label not in seen_names:
                            intent.elements.append(DesignElement(
                                type="PIPE",
                                name=label,
                                label=label,
                                source_svg=str(file_path),
                                confidence=0.6,
                            ))
                elif has_shape and label:
                    etype = self._infer_type(label)
                    name = label.strip().rstrip(".")
                    if name not in seen_names:
                        intent.elements.append(DesignElement(
                            type=etype,
                            name=name,
                            label=label,
                            source_svg=str(file_path),
                            confidence=0.7,
                        ))

            # 4. 提取连接关系
            shapes = root.findall(".//{http://www.w3.org/2000/svg}g[{http://schemas.microsoft.com/visio/2003/SVGExtensions/}groupContext='shape']")
            for shape in shapes:
                pid = shape.get("{http://schemas.microsoft.com/visio/2003/SVGExtensions/}mID", "")
                path_elems = shape.findall("{http://www.w3.org/2000/svg}path")
                for p in path_elems:
                    d = p.get("d", "")
                    if "L" in d:
                        # 记录连接
                        intent.connections.append((f"Shape_{pid}", f"Endpoint_{d[-20:]}", "LINE"))

            logger.info(f"[SVG] 解析完成: {len(intent.elements)} 个元素, {len(intent.connections)} 条连接")
            return intent

        except ImportError:
            logger.error("需要 lxml 库: pip install lxml")
            return intent
        except Exception as e:
            logger.error(f"SVG 解析失败: {e}")
            return intent

    def _infer_type(self, label: str) -> str:
        """从标签内容推断元素类型。"""
        label_upper = label.upper()
        # 先检查位号前缀（更精确的匹配）
        import re
        prefix_tag = re.match(r'^/?([A-Z]+)', label_upper)
        if prefix_tag:
            prefix = prefix_tag.group(1)
            if prefix in ("P", "PU", "PUMP"):
                return "EQUIPMENT"
            if prefix in ("V", "VES", "TNK", "TANK", "DRUM"):
                return "VESSEL"
            if prefix in ("E", "HEX", "HE", "EXC"):
                return "HEATEX"
            if prefix in ("F", "FIL", "FLT"):
                return "FILTER"
            if prefix in ("C", "COM", "CPR"):
                return "COMPRESSOR"
            if prefix in ("XV", "HV", "MOV", "FCV", "PCV", "LCV"):
                return "VALVE"
            if prefix in ("FT", "PT", "LT", "TT", "FIC", "PIC", "LIC", "FIQ"):
                return "INSTRUMENT"

        # 关键词匹配（更严格的单词边界）
        words = label_upper.replace("/", " ").replace("-", " ").replace("_", " ").split()
        for w in words:
            if w in ("PUMP",): return "EQUIPMENT"
            if w in ("TANK", "VESSEL"): return "VESSEL"
            if w in ("HEAT", "EXCHANGER", "COOLER", "HEATER"): return "HEATEX"
            if w in ("FILTER",): return "FILTER"
            if w in ("COMPRESSOR",): return "COMPRESSOR"
            if w in ("VALVE",): return "VALVE"
        return "EQUIPMENT"

    @staticmethod
    def _looks_like_tag(text: str) -> bool:
        """判断文本是否为工程位号格式。"""
        import re
        patterns = [
            r'^/?[A-Z]+-\d+[A-Z]?$',        # T-101, /SWC1001
            r'^/?[A-Z]{2,5}\d{3,5}$',        # SWC1001, OBD001
            r'^\d{2,3}[A-Z]{2}\d{2,4}$',     # 01EQ001
            r'^[A-Z]+-\d{3,5}-\d{3,5}$',     # SWC-001-600
        ]
        return any(re.match(p, text.strip()) for p in patterns)


# ── PDF 解析器 ────────────────────────────────

class PDFParser(BaseParser):
    """解析 PDF 格式的 P&ID 图纸。"""

    def can_parse(self, file_path: str) -> bool:
        return str(file_path).lower().endswith(".pdf")

    def parse(self, file_path: str) -> DesignIntent:
        intent = DesignIntent(source_file=str(file_path))
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text() or ""

                # 提取文本内容中的设备/管道线索
                for line in full_text.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    # 尝试匹配设备位号模式
                    if self._looks_like_tag(line):
                        etype = self._infer_type(line)
                        intent.elements.append(DesignElement(
                            type=etype,
                            name=line,
                            label=line,
                            source_svg="",
                            confidence=0.4,
                        ))
                    intent.notes.append(f"TEXT: {line[:200]}")

                logger.info(f"[PDF] 解析完成: {len(intent.elements)} 个元素, {len(full_text)} 字符文本")
                return intent

        except ImportError:
            logger.error("需要 pdfplumber: pip install pdfplumber")
            return intent
        except Exception as e:
            logger.error(f"PDF 解析失败: {e}")
            return intent

    def _looks_like_tag(self, text: str) -> bool:
        """判断是否为设备位号（如 T-101, P-001A, FT-101 等）。"""
        import re
        patterns = [
            r'^[A-Z]+-\d+[A-Z]?$',        # T-101, P-001A
            r'^[A-Z]{2,3}-\d{3,5}$',       # FT-101, PIC-001
            r'^\d{2,3}[A-Z]{2}\d{2,4}$',   # 01EQ001
        ]
        return any(re.match(p, text) for p in patterns)


# ── DWG 解析器框架 ───────────────────────────

class DWGParser(BaseParser):
    """
    DWG 解析器 — 基础框架。
    完整解析需要 ezdxf (DXF) 或 AutoCAD COM API。
    目前实现 DWG → DXF 转换后的基础解析。
    """

    def can_parse(self, file_path: str) -> bool:
        return str(file_path).lower().endswith(".dwg")

    def parse(self, file_path: str) -> DesignIntent:
        intent = DesignIntent(source_file=str(file_path))
        intent.notes.append(f"DWG文件 '{file_path}' 需要先转换为DXF格式再解析")
        intent.notes.append("当前使用基础框架模式，仅提取文件名信息")

        # 从文件名推断项目归属
        fname = Path(file_path).name
        if fname.startswith("acp"):
            intent.project = "AvevaCatalogue"
        elif fname.startswith("aps"):
            intent.project = "AvevaPlantSample"
        elif fname.startswith("ams"):
            intent.project = "AvevaMarineSample"

        return intent

    def parse_dxf(self, file_path: str) -> DesignIntent:
        """解析 DXF 格式（需先转换）。"""
        intent = DesignIntent(source_file=str(file_path))
        try:
            import ezdxf
            doc = ezdxf.readfile(file_path)
            msp = doc.modelspace()

            for entity in msp:
                etype = entity.dxftype()
                if etype == "TEXT":
                    intent.elements.append(DesignElement(
                        type=self._dxf_infer_type(entity.dxf.text),
                        name=entity.dxf.text,
                        label=entity.dxf.text,
                        confidence=0.5,
                    ))
                elif etype in ("LINE", "POLYLINE", "LWPOLYLINE"):
                    intent.connections.append(("DXF_LINE", etype, "LINE"))

            logger.info(f"[DXF] 解析完成: {len(intent.elements)} 个文本, {len(intent.connections)} 条线")
            return intent

        except ImportError:
            intent.notes.append("需要 ezdxf 库: pip install ezdxf")
            return intent
        except Exception as e:
            logger.error(f"DXF 解析失败: {e}")
            return intent

    def _dxf_infer_type(self, text: str) -> str:
        return SVGParser()._infer_type(text)


# ── 解析器工厂 ────────────────────────────────

class DrawingParserFactory:
    """根据文件类型自动选择合适的解析器。"""

    _parsers = [SVGParser(), PDFParser(), DWGParser()]

    def get_parser(self, file_path: str) -> Optional[BaseParser]:
        for parser in self._parsers:
            if parser.can_parse(file_path):
                return parser
        return None

    def parse(self, file_path: str) -> DesignIntent:
        parser = self.get_parser(file_path)
        if parser is None:
            logger.warning(f"不支持的图纸格式: {file_path}")
            intent = DesignIntent(source_file=str(file_path))
            intent.notes.append(f"不支持的文件格式: {Path(file_path).suffix}")
            return intent
        return parser.parse(file_path)


# ── 自然语言解析器 ───────────────────────────

class NaturalLanguageParser:
    """从自然语言描述创建设计意图。"""

    @staticmethod
    def parse(description: str) -> DesignIntent:
        """从自然语言描述构建 DesignIntent。"""
        intent = DesignIntent()
        intent.notes.append(f"自然语言描述: {description}")
        import re

        # 检测项目
        desc_upper = description.upper()
        if "船舶" in description or "船" in description or "MARINE" in desc_upper:
            intent.project = "AvevaMarineSample"
        elif "工厂" in description or "PLANT" in desc_upper or "化工" in description:
            intent.project = "AvevaPlantSample"

        # 检测区域名称（支持 "在 XXX 区域" 和 "区域 XXX"）
        zone_match = re.search(r'(?:在\s*)?(\S+)\s*区域', description)
        if not zone_match:
            zone_match = re.search(r'区域[：:]?\s*(\S+)', description)
        if zone_match:
            candidate = zone_match.group(1).strip()
            # 忽略明显不是区域名的长文本
            if len(candidate) < 20 and not any(c in candidate for c in "的创建建一"):
                intent.zone = candidate.upper()

        # 检测尺寸参数: 直径/宽x深x高
        width = depth = height = 0.0
        dim_match = re.search(r'直径\s*(\d+(?:\.\d+)?)\s*[米mM]', description)
        if dim_match:
            width = depth = float(dim_match.group(1)) * 1000  # 转 mm

        wh_match = re.search(r'宽\s*(\d+(?:\.\d+)?)\s*[米mM]', description)
        if wh_match:
            width = float(wh_match.group(1)) * 1000

        dh_match = re.search(r'深\s*(\d+(?:\.\d+)?)\s*[米mM]', description)
        if dh_match:
            depth = float(dh_match.group(1)) * 1000

        hh_match = re.search(r'高\s*(\d+(?:\.\d+)?)\s*[米mM]', description)
        if hh_match:
            height = float(hh_match.group(1)) * 1000

        # 检测设备名称/位号
        tag_match = re.search(r'\b([A-Z]+-\d+[A-Z]?)\b', description)
        tag_name = tag_match.group(1) if tag_match else ""

        # 检测设备类型
        found_equipment = False
        equipment_map = [
            (r'储罐|容器|VESSEL|TANK', 'VESSEL', 'VESSEL'),
            (r'立式\s*(?:储)?罐', 'VESSEL', 'VESSEL'),
            (r'卧式\s*(?:储)?罐', 'VESSEL', 'VESSEL'),
            (r'泵|PUMP', 'PUMP', 'PUMP'),
            (r'换热器|HEAT\s*EXCHANGER|冷却器', 'HEATEX', 'HEATEX'),
            (r'塔|COLUMN|精馏', 'COLUMN', 'COLUMN'),
            (r'过滤器|FILTER', 'FILTER', 'FILTER'),
            (r'压缩机|COMPRESSOR', 'COMPRESSOR', 'COMPRESSOR'),
        ]

        for pattern, etype, cat in equipment_map:
            if re.search(pattern, description, re.IGNORECASE):
                name = tag_name if tag_name else f"{etype}-001"
                elem = DesignElement(
                    type="EQUIPMENT",  # 统一为 EQUIPMENT，ACTTYPE 区分
                    name=name,
                    category=cat,
                    label=etype,
                    width=width or 1000,
                    depth=depth or 1000,
                    height=height or 2000,
                    confidence=0.6 if not tag_name else 0.8,
                )
                intent.elements.append(elem)
                found_equipment = True
                # 只匹配第一个设备类型
                break

        # 检测管道
        if any(kw in desc_upper for kw in ["管道", "管线", "PIPE", "PIPING", "管路"]):
            bore_match = re.search(r'(\d+)\s*寸\b', description)
            if bore_match:
                bore = int(bore_match.group(1)) * 25  # 寸转 mm
            else:
                bore_match = re.search(r'DN\s*(\d+)', description, re.IGNORECASE)
                bore = int(bore_match.group(1)) if bore_match else 100
            pipe_name = tag_name if tag_name and not intent.elements else "P-001"
            intent.elements.append(DesignElement(
                type="PIPE",
                name=pipe_name,
                bore=bore,
                confidence=0.5,
            ))

        if not found_equipment and not intent.elements:
            intent.notes.append("未识别出具体设备/管道，请提供更详细的描述。例如：\n"
                                "  \"在 AREA_100 区域创建一台直径2米高5米的立式储罐 T-101\"\n"
                                "  \"创建一条DN200的冷却水管线 P-001\"")
        else:
            if width and not height:
                height = 2000
            if intent.elements:
                e = intent.elements[0]
                if e.type == "EQUIPMENT":
                    intent.notes.append(
                        f"[AI] 已解析: {e.name} ({e.category})"
                        f" 尺寸 {e.width:.0f}x{e.depth:.0f}x{e.height:.0f} mm"
                    )

        return intent
