"""
Adapt ``Base_reference.txt`` without losing its actual construction.

The reference base is not a point cloud. It is one 43-member assembly whose
five skid members form the authoritative base envelope, whose pump station is
fitted to a 340 x 120 casing, and whose motor station is fitted to a 360 x 560
stator. Each target therefore needs three independent plan mappings:

* skid -> the project's confirmed overall base envelope;
* pump station -> the target casing diameter and axial length;
* motor station -> the target stator diameter and axial length.

Local primitive axes matter. A PYRAMID whose local Y is East does not scale
its X dimension across the pump, and a default-oriented member must receive an
explicit rotated ORI when the target pump does not face North. The previous
adapter ignored both facts, which is why all 43 members could be present while
the rendered assembly still did not resemble the reference.

The reference's +E transverse direction must also remain the right-hand side
of its +N machine axis. Mirroring member positions while rotating their ORIs
normally makes every offset PYRAMID lean away from the machine. Hex washers
have an off-origin LOOP, so their physical centres -- not their EXTRUSION POS
datums -- are paired to the anchor-cylinder axes.

Vertical mapping preserves the reference's relationship to the machine, not
just its lowest point. PYRAMID uses a geometric-centre POS: the native pump
saddle spans -200..-140 around POS -170, and the motor mounting pad reaches
-173 above the -180 stator underside. Those relationships are adapted from
their physical end faces, never by treating POS as one end.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Tuple

SOURCE = (Path(__file__).resolve().parents[1] / "imports" /
          "2026-08-19_Base_reference.txt")

_POS_TOKEN = re.compile(r"\b([ENSWUD])\s*(-?[\d.]+)\s*mm", re.IGNORECASE)
_ORI_TOKEN = re.compile(r"\b([XYZ])\s+is\s+([ENSWUD])\b", re.IGNORECASE)
_SIGN = {"E": 1.0, "W": -1.0, "N": 1.0, "S": -1.0,
         "U": 1.0, "D": -1.0}
_AXIS = {"E": "east", "W": "east", "N": "north", "S": "north",
         "U": "up", "D": "up"}
_DIMS = ("DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "XBOT", "YBOT",
         "XTOP", "YTOP", "XOFF", "YOFF", "RADI")

VECTORS = {
    "E": (1.0, 0.0, 0.0), "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0), "S": (0.0, -1.0, 0.0),
    "U": (0.0, 0.0, 1.0), "D": (0.0, 0.0, -1.0),
}

# Reference skid and machine datums, measured directly from the native listing.
REF_BASE_W = 510.0
REF_BASE_L = 1390.0
REF_PLATE_T = 60.0
REF_PLATE_CENTRE_N = -541.0
REF_PLATE_TOP = -280.0
REF_PLATE_UNDER = -340.0

REF_PUMP_MACHINE_N = 0.0
REF_PUMP_RADIUS = 170.0
REF_PUMP_LENGTH = 120.0
REF_PUMP_BOTTOM = -REF_PUMP_RADIUS
REF_PUMP_SUPPORT_TOP = -140.0

REF_MOTOR_MACHINE_N = -880.0
REF_MOTOR_RADIUS = 180.0
REF_MOTOR_LENGTH = 560.0
REF_MOTOR_BOTTOM = -REF_MOTOR_RADIUS
REF_MOTOR_SUPPORT_TOP = -173.0

# Station membership is based on the support centres, not the machine centres.
REF_PUMP_SUPPORT_N = 0.0
REF_MOTOR_SUPPORT_N = -804.62
STATION_WINDOW = 200.0

# Semantic roles preserve the reference inventory and make verification and
# mutation tests address the part's job rather than a coincidental position.
ROLE_BY_INDEX = {
    1: "pump mounting pad",
    2: "skid upper rail left",
    3: "motor sole plate left",
    4: "pump saddle gusset north",
    5: "pump saddle gusset south",
    6: "motor sole gusset left",
    7: "pump sole gusset left",
    8: "pump sole gusset right",
    9: "motor sole gusset right",
    10: "pump sole plate left",
    11: "pump sole plate right",
    12: "motor sole plate right",
    13: "motor mounting pad",
    14: "motor stay left inner",
    15: "pump side stay left",
    16: "pump side stay right",
    17: "motor stay right inner",
    18: "motor stay left outer",
    19: "motor stay right outer",
    20: "hex washer motor 1", 21: "anchor bolt motor 1",
    22: "hex washer motor 2", 23: "hex washer motor 3",
    24: "hex washer motor 4", 25: "anchor bolt motor 2",
    26: "hex washer pump 1", 27: "hex washer pump 2",
    28: "anchor bolt pump 1", 29: "anchor bolt pump 2",
    30: "anchor bolt pump 3", 31: "anchor bolt pump 4",
    32: "hex washer pump 3", 33: "hex washer pump 4",
    34: "hex washer motor 5", 35: "anchor bolt motor 3",
    36: "anchor bolt motor 4", 37: "hex washer motor 6",
    38: "anchor bolt motor 5", 39: "anchor bolt motor 6",
    40: "skid centre plate",
    41: "skid upper rail right",
    42: "skid lower rail left",
    43: "skid lower rail right",
}

# Vertical construction roles. Their plan arrangement remains the native
# reference shape; only their bearing interfaces are solved per target pump.
SOLE_PLATE_INDICES = {3, 10, 11, 12}
LOWER_GUSSET_INDICES = {6, 7, 8, 9}
SADDLE_GUSSET_INDICES = {4, 5}
OUTER_STAY_INDICES = {14, 15, 16, 17, 18, 19}
WASHER_INDICES = {20, 22, 23, 24, 26, 27, 32, 33, 34, 37}
ANCHOR_INDICES = {21, 25, 28, 29, 30, 31, 35, 36, 38, 39}


def _cross(first: Tuple[float, float, float],
           second: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (first[1] * second[2] - first[2] * second[1],
            first[2] * second[0] - first[0] * second[2],
            first[0] * second[1] - first[1] * second[0])


def orientation_basis(ori: Optional[str]) -> Dict[str, Tuple[float, float, float]]:
    """Return local X/Y/Z unit vectors for the cardinal ORIs in the base."""
    basis: Dict[str, Tuple[float, float, float]] = {}
    for axis, letter in _ORI_TOKEN.findall(ori or ""):
        basis[axis.upper()] = VECTORS[letter.upper()]
    if not basis:
        return {"X": VECTORS["E"], "Y": VECTORS["N"], "Z": VECTORS["U"]}
    if "Y" in basis and "Z" in basis and "X" not in basis:
        basis["X"] = _cross(basis["Y"], basis["Z"])
    if "Z" in basis and "X" in basis and "Y" not in basis:
        basis["Y"] = _cross(basis["Z"], basis["X"])
    if "X" in basis and "Y" in basis and "Z" not in basis:
        basis["Z"] = _cross(basis["X"], basis["Y"])
    defaults = {"X": VECTORS["E"], "Y": VECTORS["N"], "Z": VECTORS["U"]}
    for axis, vector in defaults.items():
        basis.setdefault(axis, vector)
    return basis


def profile_centre(profile: Iterable[Tuple[float, float]]) -> Tuple[float, float]:
    """Return the plan centre of a closed regular LOOP without double-counting it."""
    vertices = list(profile)
    if len(vertices) > 1 and all(
            abs(vertices[0][axis] - vertices[-1][axis]) < 0.001
            for axis in (0, 1)):
        vertices.pop()
    if not vertices:
        return (0.0, 0.0)
    return (sum(x for x, _ in vertices) / len(vertices),
            sum(y for _, y in vertices) / len(vertices))


def profile_world_centre(element: RefElement) -> Tuple[float, float]:
    """Physical plan centre of an EXTRUSION whose LOOP is not POS-centred."""
    local_x, local_y = profile_centre(element.profile)
    basis = orientation_basis(element.ori)
    return (element.pos["east"] + basis["X"][0] * local_x
            + basis["Y"][0] * local_y,
            element.pos["north"] + basis["X"][1] * local_x
            + basis["Y"][1] * local_y)


@dataclass
class RefElement:
    index: int
    kind: str
    attrs: Dict[str, float] = field(default_factory=dict)
    pos: Dict[str, float] = field(default_factory=lambda: {
        "east": 0.0, "north": 0.0, "up": 0.0})
    ori: Optional[str] = None
    profile: List[Tuple[float, float]] = field(default_factory=list)
    station: str = "skid"


def parse_reference(path: Path = SOURCE) -> List[RefElement]:
    """Read the preserved native base listing in source order."""
    elements: List[RefElement] = []
    current: Optional[RefElement] = None
    in_loop = False
    index = 0

    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith(("--", "$", "ONERROR", "INPUT", "OLD",
                                        "ORRF", "LABEL", "handle", "endhandle",
                                        "RETURN", "NEW SUBEQUIPMENT")):
            continue
        if line.startswith("NEW LOOP"):
            in_loop = True
            continue
        if line.startswith("NEW VERTEX"):
            if current is not None and in_loop:
                current.profile.append((0.0, 0.0))
            continue
        if line.startswith("NEW "):
            in_loop = False
            index += 1
            current = RefElement(index=index,
                                 kind=line[4:].split("/", 1)[0].strip())
            elements.append(current)
            continue
        if line == "END" or current is None:
            continue
        if line.startswith("POS"):
            pos = {"east": 0.0, "north": 0.0, "up": 0.0}
            for letter, value in _POS_TOKEN.findall(line):
                letter = letter.upper()
                pos[_AXIS[letter]] = _SIGN[letter] * float(value)
            if in_loop:
                if current.profile:
                    current.profile[-1] = (pos["east"], pos["north"])
            else:
                current.pos = pos
            continue
        if line.startswith("ORI"):
            current.ori = line[3:].strip()
            continue
        for key in _DIMS:
            if line.startswith(key):
                match = re.search(r"(-?[\d.]+)", line[len(key):])
                if match:
                    current.attrs[key] = float(match.group(1))
                break

    for element in elements:
        north = element.pos["north"]
        if abs(north - REF_PUMP_SUPPORT_N) <= STATION_WINDOW:
            element.station = "pump"
        elif abs(north - REF_MOTOR_SUPPORT_N) <= STATION_WINDOW:
            element.station = "motor"
        else:
            element.station = "skid"
    return elements


@dataclass
class Target:
    plate_e: float
    plate_n: float
    plate_top: float
    plate_under: float
    width: float
    length: float
    wet_end: str
    pump_machine: float
    pump_axis_up: float
    pump_radius: float
    pump_length: float
    motor_machine: Optional[float] = None
    motor_axis_up: Optional[float] = None
    motor_radius: Optional[float] = None
    motor_length: Optional[float] = None


def _station_limits(elements: Iterable[RefElement], station: str,
                    origin: float) -> Tuple[float, float]:
    """Conservative reference along-axis limits for one station."""
    low = math.inf
    high = -math.inf
    for element in elements:
        if element.station != station:
            continue
        basis = orientation_basis(element.ori)
        half_n = 0.0
        if element.kind == "BOX":
            half_n = (abs(basis["X"][1]) * element.attrs.get("XLEN", 0.0) / 2
                      + abs(basis["Y"][1]) * element.attrs.get("YLEN", 0.0) / 2)
        elif element.kind == "PYRAMID":
            x = (max(element.attrs.get("XBOT", 0.0),
                     element.attrs.get("XTOP", 0.0)) / 2
                 + abs(element.attrs.get("XOFF", 0.0)))
            y = (max(element.attrs.get("YBOT", 0.0),
                     element.attrs.get("YTOP", 0.0)) / 2
                 + abs(element.attrs.get("YOFF", 0.0)))
            half_n = abs(basis["X"][1]) * x + abs(basis["Y"][1]) * y
        elif element.kind == "CYLINDER":
            half_n = element.attrs.get("DIAM", 0.0) / 2
        elif element.kind == "EXTRUSION" and element.profile:
            half_n = max(abs(basis["X"][1] * x + basis["Y"][1] * y)
                         for x, y in element.profile)
        centre = element.pos["north"] - origin
        low = min(low, centre - half_n)
        high = max(high, centre + half_n)
    return (low, high)


class ReferenceAdapter:
    """Map the native 43-member base onto one target pump."""

    def __init__(self, target: Target, elements: List[RefElement]):
        self.t = target
        self.elements = elements
        vectors = {"N": (0.0, 1.0), "S": (0.0, -1.0),
                   "E": (1.0, 0.0), "W": (-1.0, 0.0)}
        self.along = vectors[target.wet_end]
        # Reference +E is the right-hand transverse direction of reference +N.
        # Keep that handedness for every target direction. The opposite sign
        # mirrors member positions while ORI remains unmirrored.
        self.across = (self.along[1], -self.along[0])
        self.plate_scale = ((target.plate_top - target.plate_under)
                            / REF_PLATE_T)

        skid_across = target.width / REF_BASE_W
        skid_along = target.length / REF_BASE_L
        pump_across = min(target.pump_radius / REF_PUMP_RADIUS, skid_across)
        pump_along = target.pump_length / REF_PUMP_LENGTH

        if target.motor_radius and target.motor_length:
            motor_across = min(target.motor_radius / REF_MOTOR_RADIUS,
                               skid_across)
            motor_along = target.motor_length / REF_MOTOR_LENGTH
        else:
            motor_across = pump_across
            motor_along = pump_along

        self.station_target = {
            "skid": 0.0,
            "pump": target.pump_machine,
            "motor": (target.motor_machine if target.motor_machine is not None
                      else target.pump_machine - target.length *
                      ((-REF_MOTOR_MACHINE_N) / REF_BASE_L)),
        }
        self.station_reference = {
            "skid": REF_PLATE_CENTRE_N,
            "pump": REF_PUMP_MACHINE_N,
            "motor": REF_MOTOR_MACHINE_N,
        }

        # Keep each station within the base and on its own side of the midpoint.
        midpoint = ((self.station_target["pump"] + self.station_target["motor"])
                    / 2)
        pump_limits = _station_limits(elements, "pump", REF_PUMP_MACHINE_N)
        motor_limits = _station_limits(elements, "motor", REF_MOTOR_MACHINE_N)
        pump_along = min(pump_along, self._fit_scale(
            self.station_target["pump"], pump_limits, midpoint,
            target.length / 2))
        motor_along = min(motor_along, self._fit_scale(
            self.station_target["motor"], motor_limits, -target.length / 2,
            midpoint))

        self.scales = {
            "skid": (skid_across, skid_along),
            "pump": (pump_across, max(pump_along, 0.05)),
            "motor": (motor_across, max(motor_along, 0.05)),
        }

        # The native washer LOOPs are deliberately off-origin. Pair their
        # physical centres to the nearest reference cylinder so anisotropic
        # machine scaling cannot pull the hex head away from its bolt shaft.
        washers = [element for element in elements
                   if element.kind == "EXTRUSION"]
        bolts = [element for element in elements
                 if element.kind == "CYLINDER"]
        self.hardware_axes: Dict[int, Tuple[float, float]] = {}
        unused = {bolt.index: bolt for bolt in bolts}
        for washer in washers:
            centre = profile_world_centre(washer)
            candidates = [bolt for bolt in unused.values()
                          if bolt.station == washer.station]
            if not candidates:
                raise ValueError(
                    f"no unmatched anchor cylinder for washer {washer.index}")
            bolt = min(candidates, key=lambda item: math.hypot(
                item.pos["east"] - centre[0],
                item.pos["north"] - centre[1]))
            distance = math.hypot(bolt.pos["east"] - centre[0],
                                  bolt.pos["north"] - centre[1])
            if distance > 1.0:
                raise ValueError(
                    f"washer {washer.index} is {distance:.3f} mm from its "
                    f"nearest anchor cylinder {bolt.index} in the reference")
            self.hardware_axes[washer.index] = (
                bolt.pos["east"], bolt.pos["north"])
            del unused[bolt.index]
        if unused or len(self.hardware_axes) != len(washers):
            raise ValueError("reference washer/anchor pairing is not one-to-one")

        sole_by_station = {
            "pump": next(element for element in elements
                         if element.index == 10),
            "motor": next(element for element in elements
                          if element.index == 3),
        }
        self.sole_top = {
            station: target.plate_top
            + element.attrs["ZLEN"] * self.plate_scale
            for station, element in sole_by_station.items()
        }
        self.washer_thickness = (
            washers[0].attrs["HEIG"] * self.plate_scale)
        reference_anchor = next(element for element in elements
                                if element.index in ANCHOR_INDICES)
        reference_anchor_bottom = (
            reference_anchor.pos["up"]
            - reference_anchor.attrs["HEIG"] / 2)
        self.anchor_bottom = (
            target.plate_under
            + (reference_anchor_bottom - REF_PLATE_UNDER) * self.plate_scale)
        mounting_pads = {
            "pump": next(element for element in elements
                         if element.index == 1),
            "motor": next(element for element in elements
                          if element.index == 13),
        }
        self.mounting_pad_top = {
            station: self.map_up(
                element.pos["up"] + element.attrs["ZLEN"] / 2,
                station)
            for station, element in mounting_pads.items()
        }
        self.mounting_pad_bottom = {
            station: self.mounting_pad_top[station]
            - element.attrs["ZLEN"] * self.plate_scale
            for station, element in mounting_pads.items()
        }

    @staticmethod
    def _fit_scale(origin: float, limits: Tuple[float, float],
                   lower: float, upper: float) -> float:
        candidates = [math.inf]
        if limits[0] < 0:
            candidates.append((origin - lower) / -limits[0])
        if limits[1] > 0:
            candidates.append((upper - origin) / limits[1])
        return max(min(candidates), 0.05)

    def local_plan_factor(self, element: RefElement, axis: str) -> float:
        """Scale a local X or Y length using that local axis' real bearing."""
        vector = orientation_basis(element.ori)[axis]
        across_scale, along_scale = self.scales[element.station]
        return math.sqrt((vector[0] * across_scale) ** 2
                         + (vector[1] * along_scale) ** 2)

    def map_up(self, ref_up: float, station: str) -> float:
        if ref_up <= REF_PLATE_TOP or station == "skid":
            return (self.t.plate_top
                    + (ref_up - REF_PLATE_TOP) * self.plate_scale)

        if station == "pump":
            ref_radius = REF_PUMP_RADIUS
            target_radius = self.t.pump_radius
            axis_up = self.t.pump_axis_up
        else:
            ref_radius = REF_MOTOR_RADIUS
            target_radius = self.t.motor_radius or (
                self.t.pump_radius * REF_MOTOR_RADIUS / REF_PUMP_RADIUS)
            axis_up = self.t.motor_axis_up or self.t.pump_axis_up

        ref_bottom = -ref_radius
        target_bottom = axis_up - target_radius
        if ref_up <= ref_bottom:
            ref_gap = ref_bottom - REF_PLATE_TOP
            target_gap = target_bottom - self.t.plate_top
            factor = target_gap / ref_gap if ref_gap else 1.0
            return self.t.plate_top + (ref_up - REF_PLATE_TOP) * factor
        return target_bottom + (ref_up - ref_bottom) * (
            target_radius / ref_radius)

    def map_span(self, ref_low: float, ref_high: float,
                 station: str) -> Tuple[float, float]:
        return (self.map_up(ref_low, station),
                self.map_up(ref_high, station))

    def map_plan(self, east: float, north: float,
                 station: str) -> Tuple[float, float]:
        """Map one reference plan point without changing its handedness."""
        across_scale, along_scale = self.scales[station]
        across = east * across_scale
        offset = ((north - self.station_reference[station]) * along_scale)
        along = self.station_target[station] + offset
        east = (self.t.plate_e + self.along[0] * along
                + self.across[0] * across)
        north = (self.t.plate_n + self.along[1] * along
                 + self.across[1] * across)
        return east, north

    def map_point(self, element: RefElement) -> Tuple[float, float, float]:
        east, north = self.map_plan(
            element.pos["east"], element.pos["north"], element.station)
        return east, north, self.map_up(element.pos["up"], element.station)

    def build(self, emit: Callable) -> None:
        for element in self.elements:
            east, north, up = self.map_point(element)
            station = element.station
            sx = self.local_plan_factor(element, "X")
            sy = self.local_plan_factor(element, "Y")
            attrs: Dict[str, float] = {}

            if element.kind == "BOX":
                half = element.attrs.get("ZLEN", 0.0) / 2
                low, high = self.map_span(element.pos["up"] - half,
                                          element.pos["up"] + half, station)
                thickness = high - low
                if station != "skid":
                    thickness = min(thickness,
                                    element.attrs["ZLEN"] * self.plate_scale)
                if element.index in SOLE_PLATE_INDICES:
                    # A sole plate sits on the skid; it does not hang from its
                    # mapped top face. This was the first r3 load-path gap.
                    low = self.t.plate_top
                    thickness = element.attrs["ZLEN"] * self.plate_scale
                    high = low + thickness
                attrs = {
                    "XLEN": element.attrs.get("XLEN", 0.0) * sx,
                    "YLEN": element.attrs.get("YLEN", 0.0) * sy,
                    "ZLEN": thickness,
                }
                up = high - thickness / 2

            elif element.kind == "PYRAMID":
                low, high = self.map_span(
                    element.pos["up"] - element.attrs.get("HEIG", 0.0) / 2,
                    element.pos["up"] + element.attrs.get("HEIG", 0.0) / 2,
                    station)
                if element.index in LOWER_GUSSET_INDICES:
                    # Solve both bearing faces per pump. Mapping the native top
                    # independently left the motor pair short of its mounting
                    # pad whenever the stator and shaft height changed.
                    low = self.sole_top[station]
                    high = self.mounting_pad_bottom[station]
                    if high <= low:
                        raise ValueError(
                            f"element {element.index} has no height between "
                            f"sole plate U {low:.3f} and mounting pad U "
                            f"{high:.3f}")
                elif element.index in SADDLE_GUSSET_INDICES:
                    # The two upper casing saddles share the mounting pad as
                    # their bearing surface. Keeping the reference's 30 mm air
                    # gap makes them float when the target axis is raised.
                    low = self.mounting_pad_top[station]
                    if high <= low:
                        raise ValueError(
                            f"element {element.index} has no height between "
                            f"mounting pad U {low:.3f} and saddle U {high:.3f}")
                elif element.index in OUTER_STAY_INDICES:
                    # The reference starts these side stays above the sole.
                    # That inherited clearance is not a fixed joint and became
                    # a visible floating base after per-machine adaptation.
                    low = self.sole_top[station]
                    if high <= low:
                        raise ValueError(
                            f"element {element.index} has no height between "
                            f"sole plate U {low:.3f} and stay top U {high:.3f}")
                x_plate = (abs(element.attrs.get("XBOT", 0.0)
                               - element.attrs.get("XTOP", 0.0)) < 0.01)
                y_plate = (abs(element.attrs.get("YBOT", 0.0)
                               - element.attrs.get("YTOP", 0.0)) < 0.01)
                xsize = self.plate_scale if x_plate else sx
                ysize = self.plate_scale if y_plate else sy
                attrs = {
                    "XBOT": element.attrs.get("XBOT", 0.0) * xsize,
                    "YBOT": element.attrs.get("YBOT", 0.0) * ysize,
                    "XTOP": element.attrs.get("XTOP", 0.0) * xsize,
                    "YTOP": element.attrs.get("YTOP", 0.0) * ysize,
                    "HEIG": high - low,
                }
                if "XOFF" in element.attrs:
                    attrs["XOFF"] = element.attrs["XOFF"] * sx
                if "YOFF" in element.attrs:
                    attrs["YOFF"] = element.attrs["YOFF"] * sy
                # E3D PYRAMID POS is its geometric centre, like BOX/CYLINDER.
                # It is not the bottom face. r5 placed POS at ``low`` and E3D
                # therefore extended half the new height through the skid.
                up = (low + high) / 2

            elif element.kind == "CYLINDER":
                # Anchor shanks start at the reference-scaled embedment in the
                # 50 mm base and end at the top of the fixed-thickness hex head.
                low = self.anchor_bottom
                high = (self.sole_top[station]
                        + self.washer_thickness)
                attrs = {"DIAM": element.attrs.get("DIAM", 0.0)
                                   * self.plate_scale,
                         "HEIG": high - low}
                up = (low + high) / 2

            elif element.kind == "EXTRUSION":
                # Hex head thickness is hardware-sized, not shaft-height-sized.
                # Its lower face bears directly on the adapted sole plate.
                low = self.sole_top[station]
                high = low + element.attrs.get("HEIG", 0.0) * self.plate_scale
                attrs = {"HEIG": high - low}
                up = low

            # All ten reference extrusions are true hex washers. Scale them
            # isotropically with the hardware, not anisotropically with a skid.
            profile_scale = (self.plate_scale
                             if element.kind == "EXTRUSION" else 1.0)
            profile = [(x * profile_scale, y * profile_scale)
                       for x, y in element.profile]
            ori = rotate_ori(element.ori, self.t.wet_end)
            if element.kind == "EXTRUSION":
                # Put the physical hex centre exactly on its paired anchor
                # cylinder. EXTRUSION POS is the LOOP datum, not its centroid.
                axis_e, axis_n = self.map_plan(
                    *self.hardware_axes[element.index], station)
                local_x, local_y = profile_centre(profile)
                basis = orientation_basis(ori)
                east = (axis_e - basis["X"][0] * local_x
                        - basis["Y"][0] * local_y)
                north = (axis_n - basis["X"][1] * local_x
                         - basis["Y"][1] * local_y)
            role = ROLE_BY_INDEX.get(element.index, "reference member")
            emit(element.kind, attrs, east, north, up,
                 ori, profile,
                 f"/P1501B-BASE element {element.index}: {role} "
                 f"({station} station)")


# Compatibility alias for scripts written against the rejected r1 adapter.
ReferenceDeformer = ReferenceAdapter


_ROTATION = {
    "N": {"N": "N", "S": "S", "E": "E", "W": "W"},
    "S": {"N": "S", "S": "N", "E": "W", "W": "E"},
    "E": {"N": "E", "S": "W", "E": "S", "W": "N"},
    "W": {"N": "W", "S": "E", "E": "N", "W": "S"},
}


def rotate_ori(ori: Optional[str], wet_end: str) -> Optional[str]:
    """Rotate an explicit or default reference frame into the target plan."""
    if not ori:
        if wet_end == "N":
            return None
        return f"ORI Y is {_ROTATION[wet_end]['N']} and Z is U"
    table = _ROTATION[wet_end]
    return "ORI " + " ".join(
        table.get(token.upper(), token) if token.upper() in table else token
        for token in ori.split())
