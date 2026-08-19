"""
Build a complete E3D pump model from the 2026-08-19 project data.

Design
------
The task sets a strict division of authority:

* **Size and position come from project data** -- baseplate and nozzles from
  ``location_nozzle_reference.txt``, casing from ``casing_reference.txt``,
  motor/shaft from ``engine_shaft_measurements_updated.csv``, MC casing plan
  offset from ``mc_pump_casing_location_relative_center.txt``.
* **Structure comes from /P1501B** -- which parts exist, how they chain
  together, and the proportions of details the project does not dimension.

So this module never copies a reference absolute size that the project
dimensions itself.  Where the project is silent (rib count, terminal-box size,
gusset proportions) the reference ratio is applied to the target's own
governing dimension and the result is flagged as a Reference Value.

Geometry conventions (Iron Rules)
---------------------------------
* ``ORI`` before ``POS`` for every oriented primitive; ``NOZZLE`` is the
  exception and takes ``CATR`` -> ``POS`` -> ``ORI P1 IS`` (IR-2, IR-9a).
* ``POS`` is the geometric centre for BOX/CYLI/CONE, the rim plane for DISH,
  and the profile end plane for EXTRUSION (IR-1).
* Each pump is one ``EQUI`` anchored at ``POS E 0 N 0 U 0`` so the
  world-absolute child coordinates below are read in the world frame (IR-7).
* PML1 only, no render prologue, ``--`` comments (IR-4, IR-5).

Coordinate frame
----------------
Unlike /P1501B -- whose origin sits on its shaft centreline -- this project's
equipment is set out in **world coordinates**, because the baseplate positions
and the nozzle plan positions in ``location_nozzle_reference.txt`` are already
world-absolute and are hard constraints.  Every primitive is therefore emitted
with world E/N/U under an EQUI anchored at the origin.  The shaft centreline is
computed per pump and every rotating part is placed on it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# --- reference proportions, measured from /P1501B ----------------------
# Each is a ratio against a dimension the project supplies, never an absolute.
REF = {
    "casing_dish_dia": 350.0 / 340.0,      # volute end cover vs casing bore
    "casing_dish_heig": 25.0 / 340.0,
    "casing_dish_radi": 5.0 / 340.0,
    "bearing_dia": 175.0 / 340.0,          # bearing housing vs casing
    "bearing_heig": 84.0 / 340.0,
    "shaft_dia": 75.0 / 340.0,
    "motor_end_dish_dia": 400.0 / 360.0,   # end bell vs stator barrel
    "motor_end_dish_heig": 100.0 / 360.0,
    "motor_end_dish_radi": 2.0 / 360.0,
    "rib_radial": 50.0 / 360.0,            # cooling rib, radial projection
    "rib_thick": 10.0 / 360.0,
    "terminal_box": 150.0 / 360.0,         # terminal box cube vs stator
    "gland_dia": 10.0 / 360.0,
    "gland_heig": 175.0 / 360.0,
}
RIB_COUNT = 36            # /P1501B carries 36 axial ribs on a full 360 degrees
BASEPLATE_THICKNESS = 50.0    # client-confirmed, DO.txt 2026-07-29

#: Unit vector per E3D axis letter, in world E/N/U.
AXIS_VECTOR = {
    "E": (1.0, 0.0, 0.0), "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0), "S": (0.0, -1.0, 0.0),
    "U": (0.0, 0.0, 1.0), "D": (0.0, 0.0, -1.0),
}
OPPOSITE = {"E": "W", "W": "E", "N": "S", "S": "N", "U": "D", "D": "U"}


def fmt(value: float) -> str:
    """Millimetre literal, trimmed so the macro stays readable."""
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return text if text not in ("", "-0") else "0"


def pos_line(east: float, north: float, up: float) -> str:
    """A ``POS`` line using E3D's signed-letter form."""
    return (f"POS {'E' if east >= 0 else 'W'} {fmt(abs(east))}mm "
            f"{'N' if north >= 0 else 'S'} {fmt(abs(north))}mm "
            f"{'U' if up >= 0 else 'D'} {fmt(abs(up))}mm")


@dataclass
class Primitive:
    """One emitted element, kept as data so it can be verified before writing."""

    kind: str
    sube: str
    attrs: Dict[str, float]
    east: float
    north: float
    up: float
    ori: Optional[str] = None
    name: Optional[str] = None
    catr: Optional[str] = None
    note: str = ""

    def to_pml(self) -> List[str]:
        header = f"NEW {self.kind}" + (f" /{self.name}" if self.name else "")
        lines = [header]
        if self.kind == "NOZZLE":
            # IR-9a: CATR first (there is no P-point to aim until a component
            # is bound), then POS, then ORI P1 IS -- the opposite of a
            # primitive's ORI-before-POS order (IR-2).
            if self.catr:
                lines.append(f"CATR SPCOMPONENT {self.catr}")
            lines.append(pos_line(self.east, self.north, self.up))
            if self.ori:
                lines.append(self.ori)
            for key in ("HEIG",):
                if key in self.attrs:
                    lines.append(f"{key} {fmt(self.attrs[key])}mm")
            lines += ["TEMP -100000degC", "PRES 0pascal", "TPRESS 0pascal",
                      "DUTY unset"]
        else:
            for key in ("DIAM", "HEIG", "XLEN", "YLEN", "ZLEN",
                        "XBOT", "YBOT", "XTOP", "YTOP", "HEIG2",
                        "XOFF", "YOFF", "RADI"):
                if key in self.attrs:
                    label = "HEIG" if key == "HEIG2" else key
                    lines.append(f"{label} {fmt(self.attrs[key])}mm")
            # IR-2: orientation must be established before the position is
            # read, or the element drifts silently.
            if self.ori:
                lines.append(self.ori)
            lines.append(pos_line(self.east, self.north, self.up))
        lines.append("END")
        return lines


@dataclass
class PumpModel:
    """A complete pump, assembled as SUBE-grouped primitives."""

    tag: str
    element: str
    description: str
    primitives: List[Primitive] = field(default_factory=list)
    reference_values: List[str] = field(default_factory=list)
    unresolved: List[str] = field(default_factory=list)
    facts: Dict[str, object] = field(default_factory=dict)

    def add(self, primitive: Primitive) -> Primitive:
        self.primitives.append(primitive)
        return primitive

    def by_sube(self) -> Dict[str, List[Primitive]]:
        groups: Dict[str, List[Primitive]] = {}
        for primitive in self.primitives:
            groups.setdefault(primitive.sube, []).append(primitive)
        return groups

    def to_pml(self) -> str:
        lines = [
            f"-- {self.tag}  {self.description}",
            "-- Generated from location_nozzle_reference.txt (baseplate,",
            "-- position, nozzles), casing_reference.txt (casing),",
            "-- engine_shaft_measurements_updated.csv (motor/shaft) and",
            "-- mc_pump_casing_location_relative_center.txt (MC casing plan).",
            "-- Structure adapted from /P1501B in Reference_pumps.txt.",
            f"NEW EQUIPMENT /{self.element}",
            f"DESC '{self.description}'",
            "POS E 0mm N 0mm U 0mm",
        ]
        for sube, items in self.by_sube().items():
            lines.append(f"NEW SUBEQUIPMENT /{self.element}_{sube}")
            for primitive in items:
                lines.extend(primitive.to_pml())
        return "\n".join(lines) + "\n"
