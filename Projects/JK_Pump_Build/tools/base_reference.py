"""
Reproduce ``Base_reference.txt`` (/P1501B-BASE) for each project pump.

Method
------
Three earlier attempts REDESIGNED the support from ratios sampled off the
reference, and each was rejected.  This module does not design anything: it
parses the reference's own 43 elements and maps each one through an affine
transform into the target pump's frame.  Every member the reference has, the
target gets; nothing is added and nothing is dropped.

The transform
-------------
The reference base is expressed in /P1501B's equipment frame, whose origin sits
on the SHAFT CENTRELINE (established 2026-08-18).  Its baseplate occupies

    E  -150 .. +150      (width  300, centred on the axis)
    N  -1236 .. +154     (length 1390)
    U  -340 .. -280      (thickness 60, underside 340 below the shaft)

A target pump supplies its own plate width, length, underside and top, plus the
plan positions of the two machines it must carry.  The mapping is therefore
separable and, crucially, *anisotropic* -- a pump plate is not a scaled copy of
the reference plate, so one uniform factor cannot serve:

* **transverse (across the machine)** -- scale by ``width / 300``;
* **longitudinal (along the machine)** -- scale by ``length / 1390``;
* **vertical** -- scale by ``height_scale``, chosen so the reference's plate
  thickness maps onto the project's confirmed 50 mm plate and the machine
  mountings land under the real machines.

Members are anchored rather than blindly scaled where the reference ties them
to a feature: the pump-end mounting follows the target's casing, and the
motor-end mounting follows the target's motor, because those two N stations
(``N 0`` and ``N -804.62``) are what the reference's own layout is built around.

Element datums are preserved exactly (IR-1): BOX and PYRAMID keep their datum,
an EXTRUSION keeps its profile end plane and its LOOP vertices are scaled in
plan, a CYLINDER keeps its centre.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SOURCE = Path(r"C:\Users\A\Desktop\Base_reference.txt")

_POS_TOKEN = re.compile(r"\b([ENSWUD])\s*(-?[\d.]+)\s*mm", re.IGNORECASE)
_SIGN = {"E": 1.0, "W": -1.0, "N": 1.0, "S": -1.0, "U": 1.0, "D": -1.0}
_AXIS = {"E": "east", "W": "east", "N": "north", "S": "north", "U": "up", "D": "up"}
_DIMS = ("DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "XBOT", "YBOT",
         "XTOP", "YTOP", "XOFF", "YOFF", "RADI")

# --- the reference base's own geometry, measured from the listing -------
REF_PLATE_WIDTH = 300.0        # the plate MEMBER: BOX 300 x 1390 x 60
#: The base's OVERALL transverse envelope, -255..+255.  Its outrigger brackets
#: deliberately reach beyond the plate member, so the transverse scale is taken
#: against this, not against the plate: scaling on 300 pushed the brackets off
#: the target plate entirely.
REF_BASE_WIDTH = 510.0
REF_PLATE_LENGTH = 1390.0
REF_PLATE_THICK = 60.0
REF_PLATE_CENTRE_N = -541.0    # POS S 541 of the plate BOX
REF_PLATE_TOP = -280.0         # D 310 centre, 60 thick -> -340..-280
REF_PLATE_UNDER = -340.0
#: The two stations the reference's mountings sit on, in its own frame.
#: How far the base's topmost mounting surface stands above its plate top.
#: The reference's highest member reaches U -110 with the plate top at -280,
#: and its machine sits directly on that, so this is the rise a target base
#: must reproduce to meet its own machine.
#: The reference's two mounting rises above its plate top: the pump end
#: reaches +170 and the motor end +155, so the two are kept apart rather than
#: averaged into one figure.
REF_PUMP_RISE = 170.0
REF_MOTOR_RISE = 155.0
REF_BASE_RISE = 170.0
REF_PUMP_STATION_N = 0.0
REF_MOTOR_STATION_N = -804.62


@dataclass
class RefElement:
    """One element of the reference base, with its datum kept intact."""

    kind: str
    attrs: Dict[str, float] = field(default_factory=dict)
    pos: Optional[Dict[str, float]] = None
    ori: Optional[str] = None
    profile: List[Tuple[float, float]] = field(default_factory=list)


def _parse_pos(line: str) -> Dict[str, float]:
    pos = {"east": 0.0, "north": 0.0, "up": 0.0}
    for letter, value in _POS_TOKEN.findall(line):
        letter = letter.upper()
        pos[_AXIS[letter]] = _SIGN[letter] * float(value)
    return pos


def parse_base(path: Path = SOURCE) -> List[RefElement]:
    """Read the reference base into a flat element list, LOOPs included."""
    elements: List[RefElement] = []
    current: Optional[RefElement] = None
    in_loop = False

    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith(("--", "$", "ONERROR", "INPUT", "OLD",
                                        "ORRF", "LABEL", "handle", "endhandle",
                                        "RETURN")):
            continue
        if line.startswith("NEW SUBEQUIPMENT"):
            continue
        if line.startswith("NEW LOOP"):
            in_loop = True
            continue
        if line.startswith("NEW VERTEX"):
            # A bare VERTEX with no POS is the profile origin.
            if current is not None and in_loop:
                current.profile.append((0.0, 0.0))
            continue
        if line.startswith("NEW "):
            in_loop = False
            current = RefElement(kind=line[4:].split("/", 1)[0].strip())
            elements.append(current)
            continue
        if line == "END":
            continue
        if current is None:
            continue
        if line.startswith("POS"):
            pos = _parse_pos(line)
            if in_loop:
                # Overwrite the placeholder just appended for this vertex.
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
    return elements


@dataclass
class BaseTransform:
    """
    Maps the reference base frame onto one target pump.

    ``long_sign`` is +1 when the target's motor lies on -N (or -E) as the
    reference's does, and -1 when the pump is handed the other way, so the
    reference's pump end always lands on the target's wet end.
    """

    plate_e: float
    plate_n: float
    plate_top: float
    plate_under: float
    width: float
    length: float
    long_axis: str
    long_sign: float
    height_scale: float
    pump_station: float          # target long-offset of the casing mounting
    motor_station: float         # target long-offset of the motor mounting
    #: Per-station vertical factors, so each end meets its own machine.
    height_scale_pump: float = 0.0
    height_scale_motor: float = 0.0
    #: Which way this pump's wet end faces; the reference's +N maps onto it.
    wet_end: str = "N"
    #: Unit vector of that direction in world E/N.
    wet_vector: Tuple[float, float] = (0.0, 1.0)

    def __post_init__(self) -> None:
        # Default both station factors to the global one, so a caller that
        # does not distinguish the two ends still gets sane behaviour.
        if not self.height_scale_pump:
            self.height_scale_pump = self.height_scale
        if not self.height_scale_motor:
            self.height_scale_motor = self.height_scale

    def height_at(self, ref_north: float) -> float:
        """
        Vertical scale for a member at a given reference station.

        Members near the pump station use the factor that lands the pump-end
        mounting on the casing; members near the motor station use the one that
        lands the motor-end mounting on the motor.  Members between the two --
        the frame and rails -- interpolate, so the base does not step.
        """
        span = REF_MOTOR_STATION_N - REF_PUMP_STATION_N
        if abs(span) < 1e-6:
            return self.height_scale
        ratio = (ref_north - REF_PUMP_STATION_N) / span
        ratio = max(0.0, min(1.0, ratio))
        return (self.height_scale_pump
                + ratio * (self.height_scale_motor - self.height_scale_pump))

    @property
    def tran_scale(self) -> float:
        """
        Transverse scale, taken against the base's full 510 envelope.

        The reference's brackets extend to +/-255 while its plate member is only
        300 wide, so scaling on the plate would throw every bracket outside the
        target plate.  Matching envelopes keeps the base within its plate.
        """
        return self.width / REF_BASE_WIDTH

    @property
    def long_scale(self) -> float:
        return self.length / REF_PLATE_LENGTH

    def map_long(self, ref_north: float) -> float:
        """
        Reference N -> target longitudinal offset from the plate centre.

        The two machine stations are honoured exactly: anything at the
        reference's pump station lands on the target's casing, anything at its
        motor station lands on the target's motor, and everything else is
        interpolated between them so the frame stays proportionate.

        Beyond the two stations the interpolation would keep extrapolating and
        push the end members off a short plate, so outside that span the
        reference's own plate-relative geometry is used instead, scaled by the
        plate length.  That keeps the base inside its plate whatever spacing a
        given pump asks for.
        """
        span = REF_MOTOR_STATION_N - REF_PUMP_STATION_N       # -804.62
        if abs(span) < 1e-6:
            return ref_north * self.long_scale

        low = min(REF_PUMP_STATION_N, REF_MOTOR_STATION_N)
        high = max(REF_PUMP_STATION_N, REF_MOTOR_STATION_N)
        if low <= ref_north <= high:
            ratio = (ref_north - REF_PUMP_STATION_N) / span
            return self.pump_station + ratio * (self.motor_station - self.pump_station)

        # Outside the machine span: keep the reference's offset from the
        # nearer station, scaled so the plate ends still line up.
        if ref_north > high:
            anchor_ref, anchor = high, max(self.pump_station, self.motor_station)
            edge_ref = REF_PLATE_CENTRE_N + REF_PLATE_LENGTH / 2
            edge = self.length / 2
        else:
            anchor_ref, anchor = low, min(self.pump_station, self.motor_station)
            edge_ref = REF_PLATE_CENTRE_N - REF_PLATE_LENGTH / 2
            edge = -self.length / 2
        head_ref = edge_ref - anchor_ref
        head = edge - anchor
        if abs(head_ref) < 1e-6:
            return anchor
        return anchor + (ref_north - anchor_ref) / head_ref * head

    def point(self, pos: Dict[str, float]) -> Tuple[float, float, float]:
        """
        Map a reference POS into world E/N/U for this pump.

        The reference's +N (its pump end) runs along the target's wet-end
        direction, and its +E is the left-hand normal to that, so the base
        turns with the machine instead of being pinned to world axes.
        """
        across = pos["east"] * self.tran_scale
        along = self.map_long(pos["north"]) * self.long_sign
        # Anchored at the plate UNDERSIDE, not its top.  The reference has
        # nothing below its own underside (its anchor bolts stop flush), so
        # scaling about the top pushed those bolts through the foundation.
        #
        # The vertical scale is taken PER STATION.  The reference carries its
        # pump end 170 mm above the plate top and its motor end 155 mm, and a
        # target's two machines rarely share an underside either, so one global
        # factor leaves whichever machine sits higher floating clear of its
        # mounting.  Each member scales by the factor of the station it serves.
        up = self.plate_under + (pos["up"] - REF_PLATE_UNDER) * self.height_at(
            pos["north"])
        # The foundation guard cannot be applied to POS here: a BOX's POS is
        # its CENTRE (IR-1), so a member whose centre sits above the underside
        # can still dip below it by half its thickness.  The clamp is applied
        # in build_base_for_pump once the element's real extent is known.

        along_e, along_n = self.wet_vector
        # Left-hand normal, so the reference's E/W sense is preserved.
        across_e, across_n = -along_n, along_e
        return (self.plate_e + along * along_e + across * across_e,
                self.plate_n + along * along_n + across * across_n,
                up)

    def scale_pair(self, x_value: float, y_value: float) -> Tuple[float, float]:
        """
        Scale a reference (XLEN, YLEN) pair into the target's plan axes.

        The reference's X is transverse and its Y longitudinal; on an E-W pump
        those swap onto the world axes.
        """
        across = x_value * self.tran_scale
        along = y_value * self.long_scale
        return (across, along) if self.long_axis == "N" else (along, across)

    def scale_vertical(self, value: float) -> float:
        return value * self.height_scale


#: Map from a reference axis letter to the target's, for each wet-end
#: direction.  The reference's +N is its pump end and its +E the left-hand
#: normal, so rotating the base is a relabelling of the four plan letters.
_AXIS_ROTATION = {
    "N": {"N": "N", "S": "S", "E": "E", "W": "W"},
    "S": {"N": "S", "S": "N", "E": "W", "W": "E"},
    "E": {"N": "E", "S": "W", "E": "S", "W": "N"},
    "W": {"N": "W", "S": "E", "E": "N", "W": "S"},
}


def _swap_ori_axes(ori: str, wet_end: str) -> str:
    """
    Re-express a reference ORI in the target's frame.

    The reference's longitudinal axis is +N (its pump end).  When the target's
    wet end faces another direction the whole base rotates in plan, so every
    plan letter is relabelled through that rotation.  U and D are untouched --
    the base does not tip.
    """
    if not ori:
        return ori
    table = _AXIS_ROTATION[wet_end]
    return " ".join(table.get(token.upper(), token) if token.upper() in table
                    else token for token in ori.split())


def build_base_for_pump(transform: BaseTransform,
                        elements: Optional[List[RefElement]] = None) -> List[dict]:
    """
    Emit the reference base, adapted to one pump.

    Returns plain dicts so the caller can turn them into whatever Primitive
    type it uses, keeping this module free of the generator's classes.
    """
    elements = elements if elements is not None else parse_base()
    out: List[dict] = []

    for index, element in enumerate(elements, 1):
        pos = element.pos or {"east": 0.0, "north": 0.0, "up": 0.0}
        east, north, up = transform.point(pos)
        attrs: Dict[str, float] = {}

        if element.kind == "BOX":
            xlen, ylen = transform.scale_pair(element.attrs.get("XLEN", 0.0),
                                              element.attrs.get("YLEN", 0.0))
            attrs = {"XLEN": xlen, "YLEN": ylen,
                     "ZLEN": transform.scale_vertical(element.attrs.get("ZLEN", 0.0))}
        elif element.kind == "PYRAMID":
            xbot, ybot = transform.scale_pair(element.attrs.get("XBOT", 0.0),
                                              element.attrs.get("YBOT", 0.0))
            xtop, ytop = transform.scale_pair(element.attrs.get("XTOP", 0.0),
                                              element.attrs.get("YTOP", 0.0))
            xoff, yoff = transform.scale_pair(element.attrs.get("XOFF", 0.0),
                                              element.attrs.get("YOFF", 0.0))
            attrs = {"XBOT": xbot, "YBOT": ybot, "XTOP": xtop, "YTOP": ytop,
                     "HEIG": transform.scale_vertical(element.attrs.get("HEIG", 0.0))}
            # XOFF/YOFF are true lengths in the element's own frame and must
            # travel with it, or every gusset shears as the pyramid grows.
            if "XOFF" in element.attrs:
                attrs["XOFF"] = xoff
            if "YOFF" in element.attrs:
                attrs["YOFF"] = yoff
        elif element.kind == "CYLINDER":
            # An anchor bolt stays round: its diameter takes the transverse
            # scale and its length the vertical one.
            attrs = {"DIAM": element.attrs.get("DIAM", 0.0) * transform.tran_scale,
                     "HEIG": transform.scale_vertical(element.attrs.get("HEIG", 0.0))}
        elif element.kind == "EXTRUSION":
            attrs = {"HEIG": transform.scale_vertical(element.attrs.get("HEIG", 0.0))}

        profile = []
        for vertex_e, vertex_n in element.profile:
            across, along = transform.scale_pair(vertex_e, vertex_n)
            profile.append((across, along))

        # Guard the foundation using the element's OWN datum. BOX and PYRAMID
        # are centred on POS; EXTRUSION grows from its profile end plane.
        if element.kind == "BOX":
            low = up - attrs.get("ZLEN", 0.0) / 2
        elif element.kind == "PYRAMID":
            low = up - attrs.get("HEIG", 0.0) / 2
        elif element.kind == "CYLINDER":
            # An anchor bolt runs vertically here; its POS is its centre.
            low = up - attrs.get("HEIG", 0.0) / 2
        else:
            low = up
        if low < transform.plate_under:
            up += transform.plate_under - low

        out.append({
            "kind": element.kind,
            "attrs": attrs,
            "east": east, "north": north, "up": up,
            "ori": _swap_ori_axes(element.ori, transform.wet_end),
            "profile": profile,
            "note": f"/P1501B-BASE element {index} ({element.kind}), "
                    f"adapted to this pump",
        })
    return out


if __name__ == "__main__":
    elements = parse_base()
    from collections import Counter
    print(f"{len(elements)} elements: {dict(Counter(e.kind for e in elements))}")
    for kind in ("BOX", "PYRAMID", "CYLINDER", "EXTRUSION"):
        sample = next(e for e in elements if e.kind == kind)
        print(f"  {kind}: attrs={sample.attrs} pos={sample.pos} "
              f"profile={len(sample.profile)}")
