"""
Reproduce ``Base_reference.txt``'s exact SHAPE, deformed to fit each pump.

The method, and why the earlier two failed
------------------------------------------
Two previous attempts both lost something essential:

* an **affine transform** of all 43 element positions reproduced the point
  cloud but destroyed the assembly -- members landed at scaled coordinates
  instead of on the parts they bear on, so brackets tilted and gussets floated;
* a **hand-built assembly** restored the load path but invented its own shape,
  so the result no longer looked like the client's reference.

What is wanted is the reference's actual geometry, deformed only where a
specific pump requires it.  So this module applies a **piecewise rigid**
deformation:

1. the reference is split into three groups by the station each member serves
   -- 5 full-length skid members, 17 at the pump station, 21 at the motor
   station.  Membership is unambiguous: every member's N centre is either the
   plate centre (-541), the pump station (0 +/- 150) or the motor station
   (-804.62 +/- 150);
2. each **station moves as a rigid body** to its pump's real machine position.
   Internal geometry -- every relative offset, gusset taper, bracket spacing
   and hex profile inside that station -- is carried across untouched, so the
   station keeps the reference's shape exactly;
3. only two things are actually deformed:
   * **plan scale**, one factor across and one along, applied about each
     station's own centre so members keep their proportions;
   * **vertical stretch above the plate top**, per station, so that station's
     mounting surface lands on its machine.  Everything at or below the plate
     top keeps the reference's own elevations, since the plate thickness is
     fixed by the project.

The result is recognisably the reference support: same members, same relative
arrangement, same profiles, adapted in size and station position only.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

SOURCE = Path(r"C:\Users\A\Desktop\Base_reference.txt")

_POS_TOKEN = re.compile(r"\b([ENSWUD])\s*(-?[\d.]+)\s*mm", re.IGNORECASE)
_SIGN = {"E": 1.0, "W": -1.0, "N": 1.0, "S": -1.0, "U": 1.0, "D": -1.0}
_AXIS = {"E": "east", "W": "east", "N": "north", "S": "north", "U": "up", "D": "up"}
_DIMS = ("DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "XBOT", "YBOT",
         "XTOP", "YTOP", "XOFF", "YOFF", "RADI")

# --- the reference's own datum, measured from the listing ---------------
REF_PLATE_W = 300.0            # BOX 40: 300 x 1390 x 60
REF_PLATE_L = 1390.0
REF_PLATE_T = 60.0
REF_PLATE_CENTRE_N = -541.0
REF_PLATE_TOP = -280.0
REF_PLATE_UNDER = -340.0

#: The two machine stations, in the reference's frame.
REF_PUMP_N = 0.0
REF_MOTOR_N = -804.62
#: Half-width of the window that assigns a member to a station.
STATION_WINDOW = 200.0

#: The TOPMOST elevation each station reaches in the reference frame -- the
#: surface its machine sits on.  Both are the tops of that station's tallest
#: brackets: the pump end's casing brackets (4, 5) at -110, and the motor
#: end's stays (14, 17, 18, 19) at -125.
#:
#: Taking the motor figure from its foot-pad top (-173) instead made the rise
#: factor 45% too large, and the stays -- which stand higher than the pad --
#: scaled straight past the motor barrel to U 439.
REF_PUMP_MOUNT = -110.0
REF_MOTOR_MOUNT = -125.0


@dataclass
class RefElement:
    """One element of the reference, with its datum and profile intact."""

    index: int
    kind: str
    attrs: Dict[str, float] = field(default_factory=dict)
    pos: Dict[str, float] = field(default_factory=lambda: {
        "east": 0.0, "north": 0.0, "up": 0.0})
    ori: Optional[str] = None
    profile: List[Tuple[float, float]] = field(default_factory=list)
    station: str = "skid"


def parse_reference(path: Path = SOURCE) -> List[RefElement]:
    """Read the reference into elements, tagging each with its station."""
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
        if abs(north - REF_PUMP_N) <= STATION_WINDOW:
            element.station = "pump"
        elif abs(north - REF_MOTOR_N) <= STATION_WINDOW:
            element.station = "motor"
        else:
            element.station = "skid"
    return elements


@dataclass
class Target:
    """Everything one pump's base has to fit."""

    plate_e: float
    plate_n: float
    plate_top: float
    plate_under: float
    width: float            # across the machine
    length: float           # along the machine
    wet_end: str            # which way the pump end faces
    pump_station: float     # casing offset from plate centre, along the axis
    motor_station: float    # motor offset from plate centre
    pump_mount: float       # world U the pump mounting must reach
    motor_mount: float      # world U the motor mounting must reach


class ReferenceDeformer:
    """
    Deforms the reference base onto one pump.

    Plan scale is uniform within a station so its shape is preserved; the two
    stations translate independently; vertical stretch applies only above the
    plate top and is solved per station so each mounting lands on its machine.
    """

    def __init__(self, target: Target, elements: List[RefElement]):
        self.t = target
        self.elements = elements

        vectors = {"N": (0.0, 1.0), "S": (0.0, -1.0),
                   "E": (1.0, 0.0), "W": (-1.0, 0.0)}
        self.along = vectors[target.wet_end]
        self.across = (-self.along[1], self.along[0])

        # Plan scales.  Transverse uses the base's full 510 envelope, which is
        # what has to fit the plate width; longitudinal uses the plate length.
        self.s_tran = target.width / 510.0
        self.s_long = target.length / REF_PLATE_L

        # Vertical: below the plate top nothing moves (the plate thickness is
        # fixed by the project); above it, each station stretches so its
        # mounting surface reaches its machine.
        self.plate_scale = (target.plate_top - target.plate_under) / REF_PLATE_T
        self.rise = {
            "pump": self._rise(REF_PUMP_MOUNT, target.pump_mount),
            "motor": self._rise(REF_MOTOR_MOUNT, target.motor_mount),
        }
        # Skid members sit at or below the plate top, so they never stretch;
        # give them the mean in case a future member rises above it.
        self.rise["skid"] = (self.rise["pump"] + self.rise["motor"]) / 2

    def _rise(self, ref_mount: float, target_mount: float) -> float:
        """Vertical factor for the band between the plate top and a mounting."""
        ref_span = ref_mount - REF_PLATE_TOP          # e.g. 170 or 107
        target_span = target_mount - self.t.plate_top
        if ref_span <= 0:
            return 1.0
        return max(target_span / ref_span, 0.05)

    # -- coordinate mapping ------------------------------------------------
    def station_origin(self, station: str) -> float:
        """Where this station's reference origin lands, along the machine."""
        if station == "pump":
            return self.t.pump_station
        if station == "motor":
            return self.t.motor_station
        return 0.0

    def station_ref_origin(self, station: str) -> float:
        if station == "pump":
            return REF_PUMP_N
        if station == "motor":
            return REF_MOTOR_N
        return REF_PLATE_CENTRE_N

    def map_up(self, ref_up: float, station: str) -> float:
        """
        Reference U -> world U.

        At or below the reference plate top the mapping follows the plate
        itself, so the skid keeps the project's 50 mm plate.  Above it, the
        station's own rise factor applies, which is what seats each machine.
        """
        if ref_up <= REF_PLATE_TOP:
            return self.t.plate_top + (ref_up - REF_PLATE_TOP) * self.plate_scale
        return self.t.plate_top + (ref_up - REF_PLATE_TOP) * self.rise[station]

    def map_point(self, element: RefElement) -> Tuple[float, float, float]:
        """Map an element's POS into world E/N/U."""
        station = element.station
        across = element.pos["east"] * self.s_tran
        # Within a station the member keeps its offset from that station's
        # origin, scaled longitudinally; the station itself then translates.
        ref_origin = self.station_ref_origin(station)
        offset = (element.pos["north"] - ref_origin) * self.s_long
        along = self.station_origin(station) + offset
        up = self.map_up(element.pos["up"], station)

        east = self.t.plate_e + self.along[0] * along + self.across[0] * across
        north = self.t.plate_n + self.along[1] * along + self.across[1] * across
        return east, north, up

    def scale_plan(self, across_size: float, along_size: float) -> Tuple[float, float]:
        """A reference (XLEN, YLEN) pair, scaled and mapped to world axes."""
        across = across_size * self.s_tran
        along = along_size * self.s_long
        if self.t.wet_end in ("N", "S"):
            return (across, along)
        return (along, across)

    def vertical(self, value: float, station: str) -> float:
        """Scale a vertical extent (ZLEN, PYRAMID/EXTRUSION HEIG)."""
        return value * (self.plate_scale if station == "skid"
                        else self.rise[station])

    def map_span(self, ref_low: float, ref_high: float,
                 station: str) -> Tuple[float, float]:
        """
        Map a member's full vertical span, piecewise about the plate top.

        A member that CROSSES the plate top -- an anchor bolt buried in the
        plate, a stay springing from the sole -- must not have its buried part
        stretched by the station's rise factor.  Mapping the two ends
        independently keeps the part below the plate top on the plate's own
        scale and stretches only what is above it.  Doing this by span rather
        than by POS is what stops a 2.5x motor rise driving the anchors 63 mm
        below the foundation.
        """
        return (self.map_up(ref_low, station), self.map_up(ref_high, station))

    # -- emission ----------------------------------------------------------
    def build(self, emit: Callable) -> None:
        for element in self.elements:
            east, north, up = self.map_point(element)
            station = element.station
            attrs: Dict[str, float] = {}

            if element.kind == "BOX":
                xlen, ylen = self.scale_plan(element.attrs.get("XLEN", 0.0),
                                             element.attrs.get("YLEN", 0.0))
                half = element.attrs.get("ZLEN", 0.0) / 2
                low, high = self.map_span(element.pos["up"] - half,
                                          element.pos["up"] + half, station)
                # A BOX in the reference base is fabricated PLATE.  A large
                # vertical stretch (205-PU-012 lifts its motor 466 mm above the
                # plate) would turn the 45 mm foot pad into a 135 mm slab, so a
                # plate keeps its own thickness and stays hung from its TOP --
                # the face the machine bears on.  The extra height belongs to
                # the brackets and gussets, which are what should grow.
                thickness = min(high - low,
                                element.attrs.get("ZLEN", 0.0) * self.plate_scale)
                attrs = {"XLEN": xlen, "YLEN": ylen, "ZLEN": thickness}
                up = high - thickness / 2

            elif element.kind == "PYRAMID":
                xbot, ybot = self.scale_plan(element.attrs.get("XBOT", 0.0),
                                             element.attrs.get("YBOT", 0.0))
                xtop, ytop = self.scale_plan(element.attrs.get("XTOP", 0.0),
                                             element.attrs.get("YTOP", 0.0))
                # A PYRAMID's POS is its base and it grows upward.
                low, high = self.map_span(
                    element.pos["up"],
                    element.pos["up"] + element.attrs.get("HEIG", 0.0), station)
                attrs = {"XBOT": xbot, "YBOT": ybot, "XTOP": xtop, "YTOP": ytop,
                         "HEIG": high - low}
                up = low
                # XOFF/YOFF are true lengths in the element's frame: they must
                # travel with it or the gusset shears as the pyramid grows.
                if "XOFF" in element.attrs:
                    xoff, yoff = self.scale_plan(element.attrs["XOFF"], 0.0)
                    attrs["XOFF"] = xoff if self.t.wet_end in ("N", "S") else yoff
                if "YOFF" in element.attrs:
                    xoff, yoff = self.scale_plan(0.0, element.attrs["YOFF"])
                    attrs["YOFF"] = yoff if self.t.wet_end in ("N", "S") else xoff

            elif element.kind == "CYLINDER":
                # An anchor bolt stays round: diameter takes the smaller plan
                # scale so it cannot become an ellipse-sized peg.
                half = element.attrs.get("HEIG", 0.0) / 2
                low, high = self.map_span(element.pos["up"] - half,
                                          element.pos["up"] + half, station)
                attrs = {
                    "DIAM": element.attrs.get("DIAM", 0.0)
                    * min(self.s_tran, self.s_long),
                    "HEIG": high - low,
                }
                up = (low + high) / 2

            elif element.kind == "EXTRUSION":
                # IR-1: POS is the profile end plane; the solid grows upward.
                low, high = self.map_span(
                    element.pos["up"],
                    element.pos["up"] + element.attrs.get("HEIG", 0.0), station)
                attrs = {"HEIG": high - low}
                up = low

            profile = [self.scale_plan(vx, vy) for vx, vy in element.profile]

            emit(element.kind, attrs, east, north, up,
                 rotate_ori(element.ori, self.t.wet_end), profile,
                 f"/P1501B-BASE {element.kind} {element.index} "
                 f"({element.station} station)")


#: Plan-letter relabelling for each wet-end direction.  The reference's +N is
#: its pump end and +E the left-hand normal, so turning the base in plan is a
#: relabelling of the four letters.  U and D never change: the base cannot tip.
_ROTATION = {
    "N": {"N": "N", "S": "S", "E": "E", "W": "W"},
    "S": {"N": "S", "S": "N", "E": "W", "W": "E"},
    "E": {"N": "E", "S": "W", "E": "S", "W": "N"},
    "W": {"N": "W", "S": "E", "E": "N", "W": "S"},
}


def rotate_ori(ori: Optional[str], wet_end: str) -> Optional[str]:
    """Re-express a reference ORI clause in the target's plan orientation."""
    if not ori:
        return None
    table = _ROTATION[wet_end]
    return "ORI " + " ".join(
        table.get(token.upper(), token) if token.upper() in table else token
        for token in ori.split())
