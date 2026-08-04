"""
Design Drawing Parser
=====================
Supports parsing of PDF P&IDs, SVG process diagrams, and DWG construction drawings.
Outputs a unified "design intent" data structure for the PML generator.

Focused on paper mill plant equipment: pumps, tanks, vessels, heat exchangers,
pulp processing equipment, pipe networks, and structural elements.
"""

from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger("e3d_agent.drawing_parser")


# -- Unified Data Structures ------------------------------------------

@dataclass
class DesignElement:
    """A single design element extracted from a drawing or description."""
    type: str           # EQUIPMENT / PIPE / NOZZLE / STRUCTURE / VALVE / INSTRUMENT
    name: str           # Element name/tag
    label: str = ""     # Annotation text
    category: str = ""  # Equipment subtype (VESSEL/PUMP/TANK/COLUMN/HEATEX/FILTER/etc.)
    east: float = 0     # X coordinate (machine direction)
    north: float = 0    # Y coordinate (cross-machine direction)
    up: float = 0       # Z elevation
    width: float = 0    # Dimensions
    depth: float = 0
    height: float = 0
    bore: float = 0     # Nominal pipe diameter
    spec: str = ""      # Specification reference
    material: str = ""  # Material grade
    connections: List[str] = field(default_factory=list)
    source_svg: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0

@dataclass
class DesignIntent:
    """Complete design intent — from drawing parsing or natural language."""
    project: str = "AvevaPlantSample"
    zone: str = "PAPER_MILL_ZONE"
    system: str = ""
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


# -- Parser Base Class ------------------------------------------------

class BaseParser:
    def can_parse(self, file_path: str) -> bool:
        raise NotImplementedError

    def parse(self, file_path: str) -> DesignIntent:
        raise NotImplementedError


# -- SVG Parser (AVEVA Diagrams exports) ------------------------------

class SVGParser(BaseParser):
    """Parses SVG process system diagrams exported from AVEVA Diagrams."""

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

            # 1. Extract drawing metadata
            for meta in root.iter("{http://www.aveva.com/PDMS/Compare2D3D/DrawingSVG}drawing"):
                intent.system = meta.get("pc:number", "")
                if "Marine" in intent.system or "/711R_" in intent.system:
                    intent.project = "AvevaMarineSample"

            # 2. Extract title
            title_elem = root.find(".//svg:title", ns)
            if title_elem is not None and title_elem.text:
                intent.system = title_elem.text

            # 3. Extract all equipment/piping elements
            # Title block / header exclusion list
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

                if not label:
                    continue
                label_lower = label.strip().lower()
                if label_lower in skip_labels:
                    continue

                has_line = any("L" in (p.get("d", "") or "") for p in paths)
                has_shape = bool(rects)
                seen_names = {e.name for e in intent.elements}

                if has_line:
                    if self._looks_like_tag(label) or any(
                        kw in label.upper() for kw in [
                            "PUMP", "FILTER", "EXCHANGER", "PURIFIER",
                            "EJECTOR", "CHEST", "COOLER", "HEATER",
                            "PULPER", "REFINER", "SCREEN", "CLEANER",
                            "DIGESTER", "EVAPORATOR", "WASHER", "TOWER",
                        ]
                    ):
                        etype = self._infer_type(label)
                        if label not in seen_names:
                            intent.elements.append(DesignElement(
                                type=etype, name=label, label=label,
                                source_svg=str(file_path), confidence=0.7,
                            ))
                    else:
                        if label not in seen_names:
                            intent.elements.append(DesignElement(
                                type="PIPE", name=label, label=label,
                                source_svg=str(file_path), confidence=0.6,
                            ))
                elif has_shape and label:
                    etype = self._infer_type(label)
                    name = label.strip().rstrip(".")
                    if name not in seen_names:
                        intent.elements.append(DesignElement(
                            type=etype, name=name, label=label,
                            source_svg=str(file_path), confidence=0.7,
                        ))

            logger.info(f"[SVG] Parse complete: {len(intent.elements)} elements, "
                        f"{len(intent.connections)} connections")
            return intent

        except ImportError:
            logger.error("lxml library required: pip install lxml")
            return intent
        except Exception as e:
            logger.error(f"SVG parse failed: {e}")
            return intent

    def _infer_type(self, label: str) -> str:
        """Infer element type from label content."""
        import re
        label_upper = label.upper()

        # Check tag prefix (more precise matching)
        prefix_tag = re.match(r'^/?([A-Z]+)', label_upper)
        if prefix_tag:
            prefix = prefix_tag.group(1)
            if prefix in ("P", "PU", "PUMP"): return "EQUIPMENT"
            if prefix in ("V", "VES", "TNK", "TANK", "DRUM"): return "VESSEL"
            if prefix in ("E", "HEX", "HE", "EXC"): return "HEATEX"
            if prefix in ("F", "FIL", "FLT"): return "FILTER"
            if prefix in ("C", "COM", "CPR"): return "COMPRESSOR"
            if prefix in ("XV", "HV", "MOV", "FCV", "PCV", "LCV"): return "VALVE"
            if prefix in ("FT", "PT", "LT", "TT", "FIC", "PIC", "LIC"): return "INSTRUMENT"

        # Keyword matching
        words = label_upper.replace("/", " ").replace("-", " ").replace("_", " ").split()
        for w in words:
            if w in ("PUMP", "PULPER", "REFINER"): return "EQUIPMENT"
            if w in ("TANK", "VESSEL", "CHEST", "SILO", "TOWER"): return "VESSEL"
            if w in ("HEAT", "EXCHANGER", "COOLER", "HEATER", "EVAPORATOR"): return "HEATEX"
            if w in ("FILTER", "SCREEN", "CLEANER"): return "FILTER"
            if w in ("COMPRESSOR",): return "COMPRESSOR"
            if w in ("VALVE",): return "VALVE"
        return "EQUIPMENT"

    @staticmethod
    def _looks_like_tag(text: str) -> bool:
        """Check if text matches an engineering tag format."""
        import re
        patterns = [
            r'^/?[A-Z]+-\d+[A-Z]?$',       # T-101, /SWC1001
            r'^/?[A-Z]{2,5}\d{3,5}$',       # SWC1001, OBD001
            r'^\d{2,3}[A-Z]{2}\d{2,4}$',    # 01EQ001
            r'^[A-Z]+-\d{3,5}-\d{3,5}$',    # SWC-001-600
        ]
        return any(re.match(p, text.strip()) for p in patterns)


# -- PDF Parser -------------------------------------------------------

class PDFParser(BaseParser):
    """Parses PDF format P&ID drawings."""

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

                for line in full_text.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    if self._looks_like_tag(line):
                        etype = SVGParser()._infer_type(line)
                        intent.elements.append(DesignElement(
                            type=etype, name=line, label=line, confidence=0.4,
                        ))
                    intent.notes.append(f"TEXT: {line[:200]}")

                logger.info(f"[PDF] Parse complete: {len(intent.elements)} elements, "
                            f"{len(full_text)} chars text")
                return intent

        except ImportError:
            logger.error("pdfplumber required: pip install pdfplumber")
            return intent
        except Exception as e:
            logger.error(f"PDF parse failed: {e}")
            return intent

    def _looks_like_tag(self, text: str) -> bool:
        import re
        patterns = [
            r'^[A-Z]+-\d+[A-Z]?$',
            r'^[A-Z]{2,3}-\d{3,5}$',
            r'^\d{2,3}[A-Z]{2}\d{2,4}$',
        ]
        return any(re.match(p, text) for p in patterns)


# -- DWG Parser Framework ---------------------------------------------

class DWGParser(BaseParser):
    """DWG parser — base framework. Full parsing requires ezdxf or AutoCAD COM API."""

    def can_parse(self, file_path: str) -> bool:
        return str(file_path).lower().endswith(".dwg")

    def parse(self, file_path: str) -> DesignIntent:
        intent = DesignIntent(source_file=str(file_path))
        intent.notes.append(f"DWG file '{file_path}' requires DXF conversion first")
        intent.notes.append("Current mode: framework only, extracting filename info")

        fname = Path(file_path).name
        if fname.startswith("acp"):
            intent.project = "AvevaCatalogue"
        elif fname.startswith("aps"):
            intent.project = "AvevaPlantSample"
        elif fname.startswith("ams"):
            intent.project = "AvevaMarineSample"

        return intent

    def parse_dxf(self, file_path: str) -> DesignIntent:
        """Parse DXF format (requires prior DWG→DXF conversion)."""
        intent = DesignIntent(source_file=str(file_path))
        try:
            import ezdxf
            doc = ezdxf.readfile(file_path)
            msp = doc.modelspace()

            for entity in msp:
                etype = entity.dxftype()
                if etype == "TEXT":
                    intent.elements.append(DesignElement(
                        type=SVGParser()._infer_type(entity.dxf.text),
                        name=entity.dxf.text, label=entity.dxf.text, confidence=0.5,
                    ))
                elif etype in ("LINE", "POLYLINE", "LWPOLYLINE"):
                    intent.connections.append(("DXF_LINE", etype, "LINE"))

            logger.info(f"[DXF] Parse complete: {len(intent.elements)} texts, "
                        f"{len(intent.connections)} lines")
            return intent

        except ImportError:
            intent.notes.append("ezdxf required: pip install ezdxf")
            return intent
        except Exception as e:
            logger.error(f"DXF parse failed: {e}")
            return intent


# -- Parser Factory ---------------------------------------------------

class DrawingParserFactory:
    """Auto-selects the appropriate parser based on file type."""

    _parsers = [SVGParser(), PDFParser(), DWGParser()]

    def get_parser(self, file_path: str) -> Optional[BaseParser]:
        for parser in self._parsers:
            if parser.can_parse(file_path):
                return parser
        return None

    def parse(self, file_path: str) -> DesignIntent:
        parser = self.get_parser(file_path)
        if parser is None:
            logger.warning(f"Unsupported drawing format: {file_path}")
            intent = DesignIntent(source_file=str(file_path))
            intent.notes.append(f"Unsupported file format: {Path(file_path).suffix}")
            return intent
        return parser.parse(file_path)


# -- Natural Language Parser ------------------------------------------

class NaturalLanguageParser:
    """Creates DesignIntent from natural language descriptions."""

    # Paper mill equipment type patterns
    EQUIPMENT_PATTERNS = [
        (r'headbox|slice|manifold', 'HEADBOX', 'HEADBOX'),
        (r'hydrapulper|pulper|slusher', 'PULPER', 'PULPER'),
        (r'refiner|disc refiner|twin.?disc', 'REFINER', 'REFINER'),
        (r'pressure screen|fine screen', 'SCREEN', 'SCREEN'),
        (r'cleaner|centrifugal cleaner', 'CLEANER', 'CLEANER'),
        (r'digester|cooker', 'DIGESTER', 'DIGESTER'),
        (r'blow tank', 'BLOW_TANK', 'BLOW_TANK'),
        (r'vacuum washer|drum washer', 'WASHER', 'WASHER'),
        (r'bleach tower|bleaching tower', 'BLEACH_TOWER', 'BLEACH_TOWER'),
        (r'evaporator|falling film', 'EVAPORATOR', 'EVAPORATOR'),
        (r'recovery boiler', 'RECOVERY_BOILER', 'RECOVERY_BOILER'),
        (r'lime kiln|rotary kiln', 'KILN', 'KILN'),
        (r'causticiz', 'CAUSTICIZER', 'CAUSTICIZER'),
        (r'paper machine|fourdrinier|pm\d', 'PAPER_MACHINE', 'PAPER_MACHINE'),
        (r'stock chest|storage chest|pulp chest', 'STOCK_CHEST', 'STOCK_CHEST'),
        (r'white water|effluent|wastewater', 'WATER_SYSTEM', 'WATER_SYSTEM'),
        (r'clarifier|thickener', 'CLARIFIER', 'CLARIFIER'),
        (r'boiler|steam boiler|cfb', 'BOILER', 'BOILER'),
        (r'turbo.?generator|turbine generator', 'TURBOGEN', 'TURBOGEN'),
        (r'tank|vessel|silo|储罐|贮罐|料仓|槽', 'VESSEL', 'VESSEL'),
        (r'pump|泵', 'PUMP', 'PUMP'),
        (r'valve|阀', 'VALVE', 'VALVE'),
        (r'pipe|piping|pipeline|header|管道|管线', 'PIPE', 'PIPE'),
    ]

    @staticmethod
    def parse(description: str) -> DesignIntent:
        """Build DesignIntent from natural language description."""
        intent = DesignIntent()
        intent.notes.append(f"Natural language: {description}")
        import re

        desc_upper = description.upper()

        # Detect project type
        if any(kw in description for kw in ["paper", "pulp", "mill", "paper machine",
                                              "fourdrinier", "digester", "stock prep"]):
            intent.project = "AvevaPlantSample"

        # Detect zone name. Chinese descriptions put the marker after the
        # name (e.g. "AREA_100 <zone-marker>"), English before it
        # ("in AREA_100 zone"), so the Chinese pattern is tried first: an
        # English-only regex matches the wrong token on Chinese input rather
        # than failing outright.
        zone_match = re.search(r'([A-Za-z0-9_\-]{2,})\s*(?:区域|区|车间)', description)
        if not zone_match:
            zone_match = re.search(
                r'(?:in\s+)?(\S+)\s+(?:zone|area|hall)', description, re.IGNORECASE
            )
        if zone_match:
            candidate = zone_match.group(1).strip()
            if len(candidate) < 20:
                intent.zone = candidate.upper()

        # Detect dimensions: diameter, width, height. Each pattern accepts the
        # English keyword-first form and the Chinese keyword-then-value form,
        # including the bare CJK unit characters for metre and millimetre.
        width = depth = height = 0.0
        _NUM = r'(\d+(?:\.\d+)?)'
        _UNIT = r'\s*(毫米|mm|米|m)?'

        def _to_mm(value: str, unit: Optional[str]) -> float:
            """Normalize a parsed dimension to millimetres."""
            v = float(value)
            if unit in ("mm", "毫米"):
                return v
            if unit in ("m", "米"):
                return v * 1000
            # Unit omitted: values under 100 are metres by convention, since no
            # plant dimension is 100 mm or less at equipment scale.
            return v * 1000 if v < 100 else v

        dim_match = re.search(
            rf'(?:diameter|dia\.?|直径){_UNIT}?\s*{_NUM}{_UNIT}', description, re.IGNORECASE
        )
        if dim_match:
            width = depth = _to_mm(dim_match.group(2), dim_match.group(3) or dim_match.group(1))

        w_match = re.search(rf'(?:width|宽度|宽)\s*{_NUM}{_UNIT}', description, re.IGNORECASE)
        if w_match:
            width = _to_mm(w_match.group(1), w_match.group(2))

        h_match = re.search(rf'(?:height|高度|高)\s*{_NUM}{_UNIT}', description, re.IGNORECASE)
        if h_match:
            height = _to_mm(h_match.group(1), h_match.group(2))

        # Detect equipment tag
        tag_match = re.search(r'\b([A-Z]+-\d+[A-Z]?)\b', description)
        tag_name = tag_match.group(1) if tag_match else ""

        # Match equipment type
        for pattern, etype, cat in NaturalLanguageParser.EQUIPMENT_PATTERNS:
            if re.search(pattern, description, re.IGNORECASE):
                name = tag_name if tag_name else f"{etype}-001"
                elem = DesignElement(
                    type="EQUIPMENT",
                    name=name,
                    category=cat,
                    label=etype,
                    width=width or 1000,
                    depth=depth or 1000,
                    height=height or 2000,
                    confidence=0.6 if not tag_name else 0.8,
                )
                intent.elements.append(elem)
                break

        return intent
