"""
Extract the authoritative per-pump project data for the 2026-08-19 rebuild.

Reads the four client reference files and produces one merged record per pump
tag, with the provenance of every field recorded.  Nothing here invents a
value: a field the sources do not carry comes back as ``None`` so the caller
must decide whether to report it unresolved (IR-10).

Precedence, from the client's task statement:

* ``location_nozzle_reference.txt`` -- the project equipment set, overall
  position/orientation, baseplate, and the nozzle schedule (count, size,
  plan X/Y, direction).  Plan positions and directions are HARD constraints.
* ``engine_shaft_measurements_updated.csv`` -- motor/shaft fundamental sizes
  and axial offsets.  ``N/A`` means "not applicable", never zero.
* ``casing_reference.txt`` -- governing casing diameter and axial length.
* ``mc_pump_casing_location_relative_center.txt`` -- casing plan offset for MC
  pumps, which carry no upper nozzle to centre the casing on.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

DESKTOP = Path(r"C:\Users\A\Desktop")
LOCATION_NOZZLE = DESKTOP / "location_nozzle_reference.txt"
ENGINE_SHAFT = DESKTOP / "engine_shaft_measurements_updated.csv"
CASING = DESKTOP / "casing_reference.txt"
MC_OFFSET = DESKTOP / "mc_pump_casing_location_relative_center.txt"

# ``POS E 13971mm N 14114.3mm U 25mm`` -> signed east/north/up in millimetres.
_POS_TOKEN = re.compile(r"\b([ENSWUD])\s*(-?[\d.]+)\s*mm", re.IGNORECASE)
_SIGN = {"E": 1.0, "W": -1.0, "N": 1.0, "S": -1.0, "U": 1.0, "D": -1.0}
_AXIS = {"E": "east", "W": "east", "N": "north", "S": "north", "U": "up", "D": "up"}

_DIMENSION_KEYS = (
    "DIAM", "HEIG", "XLEN", "YLEN", "ZLEN",
    "XBOT", "YBOT", "XTOP", "YTOP", "XOFF", "YOFF", "RADI",
)


def parse_pos(line: str) -> Optional[Dict[str, float]]:
    """Signed E/N/U from a POS line, defaulting an omitted axis to 0."""
    out = {"east": 0.0, "north": 0.0, "up": 0.0}
    found = False
    for letter, value in _POS_TOKEN.findall(line):
        letter = letter.upper()
        out[_AXIS[letter]] = _SIGN[letter] * float(value)
        found = True
    return out if found else None


def _number(line: str) -> Optional[float]:
    match = re.search(r"(-?[\d.]+)", line)
    return float(match.group(1)) if match else None


@dataclass
class Element:
    """One primitive or nozzle read out of the reference listing."""

    kind: str
    sube: str
    name: Optional[str] = None
    pos: Optional[Dict[str, float]] = None
    ori: Optional[str] = None
    attrs: Dict[str, float] = field(default_factory=dict)
    catr: Optional[str] = None


@dataclass
class PumpLocation:
    """Everything ``location_nozzle_reference.txt`` says about one pump."""

    tag: str
    element: str
    func: Optional[str]
    elements: List[Element]

    @property
    def baseplate(self) -> Optional[Element]:
        """The single BOX under the ``_BASEPLATE`` SUBE."""
        for element in self.elements:
            if element.sube.endswith("_BASEPLATE") and element.kind == "BOX":
                return element
        return None

    @property
    def nozzles(self) -> List[Element]:
        return [e for e in self.elements if e.kind == "NOZZLE"]


def parse_location_nozzle(path: Path = LOCATION_NOZZLE) -> Dict[str, PumpLocation]:
    """
    Parse the 30-pump native listing into per-tag records.

    Only element headers, POS/ORI, dimension attributes and CATR are kept --
    the EXTRUSION vertex loops are skipped, because this file is being read for
    the baseplate and nozzle schedule, not to re-derive the old geometry.
    """
    text = path.read_text(encoding="utf-8-sig")
    pumps: Dict[str, PumpLocation] = {}
    current: Optional[PumpLocation] = None
    sube = ""
    element: Optional[Element] = None
    in_loop = False
    # Catalogue bindings arrive in a trailing ``OLD NOZZLE`` / ``CATR`` pass,
    # exactly as in AVEVA's own SMLdataPlant.pmlmac, so they are collected by
    # name here and attached to the nozzles afterwards.
    rebound: Dict[str, str] = {}
    old_target: Optional[str] = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        if line.startswith("OLD "):
            parts = line.split("/", 1)
            old_target = parts[1].strip() if len(parts) > 1 else None
            element = None
            continue

        if old_target is not None:
            if line.startswith("CATR"):
                rebound[old_target] = line.split(None, 2)[-1].strip()
                continue
            if not line.startswith(("NEW ", "INPUT", "LABEL", "$", "--")):
                continue
            old_target = None

        if line.startswith("NEW EQUIPMENT /"):
            name = line.split("/", 1)[1].strip()
            tag = name.replace("_", "-")
            current = PumpLocation(tag=tag, element=name, func=None, elements=[])
            pumps[tag] = current
            sube, element, in_loop = "", None, False
            continue

        if current is None:
            continue

        if line.startswith("NEW SUBEQUIPMENT /"):
            sube = line.split("/", 1)[1].strip()
            element, in_loop = None, False
            continue

        # A LOOP/VERTEX belongs to an EXTRUSION profile; skip until it closes.
        if line.startswith("NEW LOOP"):
            in_loop = True
            continue
        if line.startswith("NEW VERTEX"):
            continue
        if in_loop and line == "END":
            continue

        if line.startswith("NEW "):
            in_loop = False
            parts = line[4:].split("/", 1)
            kind = parts[0].strip()
            name = parts[1].strip() if len(parts) > 1 else None
            element = Element(kind=kind, sube=sube, name=name)
            current.elements.append(element)
            continue

        if element is None:
            if line.startswith("FUNC") and current.func is None:
                current.func = line.split("'")[1] if "'" in line else None
            continue

        if line.startswith("POS"):
            if not in_loop:
                element.pos = parse_pos(line)
        elif line.startswith("ORI"):
            element.ori = line[3:].strip()
        elif line.startswith("CATR"):
            element.catr = line.split(None, 2)[-1].strip()
        else:
            for key in _DIMENSION_KEYS:
                if line.startswith(key):
                    value = _number(line[len(key):])
                    if value is not None:
                        element.attrs[key] = value
                    break

    # Attach the trailing-pass bindings to the nozzles they name.
    for pump in pumps.values():
        for nozzle in pump.nozzles:
            if nozzle.name and nozzle.name in rebound:
                nozzle.catr = rebound[nozzle.name]

    return pumps


def _na(value: Optional[str]) -> Optional[float]:
    """
    ``N/A`` is preserved as ``None``.

    The client instruction is explicit: an ``N/A`` must not be read as zero.
    A zero would silently place a real component at the origin; ``None`` forces
    the caller to handle the absence.
    """
    value = (value or "").strip()
    if not value or value.upper().startswith("N/A"):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_engine_shaft(path: Path = ENGINE_SHAFT) -> Dict[str, dict]:
    """Motor/shaft fundamentals, keyed by tag, with N/A preserved as None."""
    records: Dict[str, dict] = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            tag = (row.get("equipment_tag") or "").strip()
            if not tag:
                continue
            record = {
                "equipment_name": (row.get("equipment_name") or "").strip(),
                "pump_type_raw": (row.get("pump_type") or "").strip(),
            }
            record["is_mc"] = record["pump_type_raw"].upper().startswith("MC")
            for key, value in row.items():
                if key in ("equipment_tag", "equipment_name", "pump_type"):
                    continue
                record[key] = _na(value)
            records[tag] = record
    return records


def parse_casing(path: Path = CASING) -> Dict[str, dict]:
    """Governing casing diameter and axial height per tag."""
    records: Dict[str, dict] = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            tag = (row.get("Tag") or "").strip()
            if not tag:
                continue
            records[tag] = {
                "pump_name": (row.get("Pump Name") or "").strip(),
                "diameter": _na(row.get("Casing_Cylinder_Diameter")),
                "height": _na(row.get("Casing_Cylinder_Height")),
            }
    return records


def parse_mc_offset(path: Path = MC_OFFSET) -> Dict[str, float]:
    """MC casing plan offset from the pump/baseplate centre, in millimetres."""
    records: Dict[str, float] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"\s*(\d{3}-PU-\d{3})\s+([\d.]+)\s*MM", line.strip(), re.IGNORECASE)
        if match:
            records[match.group(1)] = float(match.group(2))
    return records


def load_all() -> dict:
    return {
        "location": parse_location_nozzle(),
        "engine": parse_engine_shaft(),
        "casing": parse_casing(),
        "mc_offset": parse_mc_offset(),
    }


if __name__ == "__main__":
    data = load_all()
    print(f"location_nozzle_reference : {len(data['location'])} pumps")
    print(f"engine_shaft CSV          : {len(data['engine'])} rows")
    print(f"casing_reference          : {len(data['casing'])} rows")
    print(f"mc_pump_casing_location   : {len(data['mc_offset'])} rows")
