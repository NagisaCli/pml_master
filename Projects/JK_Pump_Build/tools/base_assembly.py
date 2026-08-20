"""
Build the pump base as a MECHANICAL ASSEMBLY, per pump.

Why this replaces the affine transform
--------------------------------------
The previous revision parsed ``Base_reference.txt`` and mapped its 43 element
positions through an affine transform.  That reproduced the reference's *point
cloud* and destroyed its *assembly*: members landed at scaled coordinates
instead of on the parts they bear on, so brackets tilted, gussets floated and
nothing carried anything.  The client's render showed exactly that.

Here the reference is read as a structure instead.  Its roles and load path are

    plate -> sole plates -> gussets -> foot pad -> machine
    rails along both plate edges carry the hold-down anchors

and every member is positioned **relative to the member it sits on**, so
contact is a property of the construction rather than something to be checked
afterwards.  The reference's proportions are kept; its absolute sizes are not.

Reference proportions, measured from /P1501B-BASE (plate 300 wide x 1390 long
x 60 thick, local U -340..-280, shaft axis at U 0):

===========================  ==========================================
member                       reference geometry
===========================  ==========================================
rail (x4)                    105 wide x 20 thick, at E +/-202.5
sole plate (x4)              125 x 300/400 x 25, at E +/-182.5, on plate top
gusset (x4)                  20 thick, 37 tall, 250/400 long, at E +/-125
foot pad (pump)              225 x 150 x 17.5, top 80 above plate top
foot pad (motor)             225 x 300 x 45, top 107 above plate top
casing bracket (x2)          20 thick, 60 tall, 220 long, on the pad
side stay (x4-6)             20 thick, 65-110 tall, at E +/-150
anchor bolt (x10)            DIA 15 x 90, at E +/-205
hex washer (x10)             34.64 across flats x 20 thick
===========================  ==========================================
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

# --- reference geometry, as ratios of the things the project supplies ---
REF_PLATE_W = 300.0
REF_PLATE_L = 1390.0
REF_PLATE_T = 60.0

#: Transverse stations, as a fraction of the plate half-width (150).
RAIL_INSET = 202.5 / 150.0        # outrigger rails, outside the plate edge
SOLE_INSET = 182.5 / 150.0        # sole plates
GUSSET_INSET = 125.0 / 150.0      # gussets under the foot pad
STAY_INSET = 150.0 / 150.0        # outboard side stays
ANCHOR_INSET = 205.0 / 150.0      # hold-down bolts

#: PLAN sizes scale with the plate WIDTH (300).
RAIL_W = 105.0 / 300.0
SOLE_W = 125.0 / 300.0
PAD_W = 225.0 / 300.0

#: THICKNESSES scale with the plate THICKNESS (60), never with its width.
#:
#: This distinction is the whole difference between a plausible base and the
#: one the client rejected.  The project fixes every baseplate at 50 mm while
#: plate widths run 631..2013, so a thickness taken as a fraction of width came
#: out up to 3.5x too fat: 72 mm sole plates and a 130 mm foot pad on a 50 mm
#: plate, which reads as a pile of slabs rather than fabricated steel.
RAIL_T = 20.0 / 60.0
SOLE_T = 25.0 / 60.0
GUSSET_T = 20.0 / 60.0
PAD_T_PUMP = 17.5 / 60.0
PAD_T_MOTOR = 45.0 / 60.0
BRACKET_T = 20.0 / 60.0
STAY_T = 20.0 / 60.0
ANCHOR_D = 15.0 / 60.0
WASHER_FLATS = 34.64 / 60.0
WASHER_T = 20.0 / 60.0
GUSSET_H = 37.0 / 60.0

#: Longitudinal member lengths, as a fraction of the machine footprint.
SOLE_OVERHANG = 1.00     # sole plate length vs the foot pad it carries
PAD_LEN_PUMP = 150.0 / 300.0     # vs plate width, when no better figure
STAY_LEN = 75.0 / 300.0


def hex_profile(across_flats: float) -> List[Tuple[float, float]]:
    """A regular hexagon, as /P1501B-BASE writes its washers."""
    radius = across_flats / math.sqrt(3.0)
    return [(radius * math.cos(math.radians(60 * i)),
             radius * math.sin(math.radians(60 * i))) for i in range(6)]


@dataclass
class Station:
    """One machine mounting: where it is, how wide, and what it must reach."""

    name: str            # "pump" or "motor"
    centre: float        # offset along the machine axis from the plate centre
    length: float        # footprint along the machine axis
    width: float         # footprint across the machine
    machine_under: float # world U of the machine's underside
    pad_thick: float     # foot pad thickness


class BaseAssembly:
    """
    Assembles one pump's base.

    ``emit`` is called with (kind, attrs, east, north, up, ori, profile, note)
    for each member, so this module stays independent of the caller's Primitive
    class.  Positions are computed from the member below, never from a mapped
    coordinate, which is what keeps the assembly in contact.
    """

    def __init__(self, plate_e: float, plate_n: float, plate_top: float,
                 plate_under: float, width: float, length: float,
                 wet_end: str, emit: Callable):
        self.plate_e = plate_e
        self.plate_n = plate_n
        self.plate_top = plate_top
        self.plate_under = plate_under
        self.width = width
        self.length = length
        self.wet_end = wet_end
        self.emit = emit

        # Machine axis = the wet-end direction; transverse = its left normal.
        vectors = {"N": (0.0, 1.0), "S": (0.0, -1.0),
                   "E": (1.0, 0.0), "W": (-1.0, 0.0)}
        self.along = vectors[wet_end]
        self.across = (-self.along[1], self.along[0])
        self.half_w = width / 2
        #: Plate thickness governs every MEMBER thickness; plate width governs
        #: plan sizes.  Keeping the two apart is what stops a wide pump getting
        #: a base built from slabs.
        self.thick = plate_top - plate_under

    # -- placement helpers ------------------------------------------------
    def point(self, along: float, across: float) -> Tuple[float, float]:
        """World (E, N) from offsets along and across the machine axis."""
        return (self.plate_e + self.along[0] * along + self.across[0] * across,
                self.plate_n + self.along[1] * along + self.across[1] * across)

    def plan(self, across_size: float, along_size: float) -> Tuple[float, float]:
        """(XLEN, YLEN) for a member sized across and along the machine."""
        if self.wet_end in ("N", "S"):
            return (across_size, along_size)
        return (along_size, across_size)

    def add_box(self, along, across, up, across_size, along_size, thick, note):
        east, north = self.point(along, across)
        xlen, ylen = self.plan(across_size, along_size)
        self.emit("BOX", {"XLEN": xlen, "YLEN": ylen, "ZLEN": thick},
                  east, north, up, None, None, note)

    def add_gusset(self, along, across, base_up, height,
                   thick, bottom_len, top_len, note):
        """
        A tapered web plate: constant thickness, narrowing in length.

        The reference's gussets keep ``XBOT == XTOP`` -- they are plates, not
        wedges -- and taper only along the machine.  POS is the base centre and
        the solid grows upward, so it is placed on whatever it stands on.
        """
        east, north = self.point(along, across)
        xbot, ybot = self.plan(thick, bottom_len)
        xtop, ytop = self.plan(thick, top_len)
        self.emit("PYRAMID",
                  {"XBOT": xbot, "YBOT": ybot, "XTOP": xtop, "YTOP": ytop,
                   "HEIG": height},
                  east, north, base_up, None, None, note)

    def add_anchor(self, along, across, top_up, note):
        """A hold-down bolt with its hex washer, seated on the member below."""
        east, north = self.point(along, across)
        diameter = max(ANCHOR_D * self.thick, 10.0)
        washer_t = max(WASHER_T * self.thick, 5.0)
        # The reference's bolt spans from INSIDE the plate to just above the
        # sole plate (U -325..-235 against a plate of -340..-280): it is buried
        # in the plate, not driven through it.  An earlier version ran the
        # shank from the plate underside to the washer top, so it protruded
        # below the foundation and stood 130 mm proud of the sole.
        bottom = self.plate_under + self.thick * 0.25
        top = top_up + washer_t
        self.emit("CYLINDER", {"DIAM": diameter, "HEIG": top - bottom},
                  east, north, (bottom + top) / 2,
                  "ORI Z is U and Y is N", None, f"{note} anchor bolt")
        # IR-1: an EXTRUSION's POS is its profile end plane.
        self.emit("EXTRUSION", {"HEIG": washer_t}, east, north, top_up,
                  "ORI Z is U and Y is N",
                  hex_profile(max(WASHER_FLATS * self.thick, 20.0)),
                  f"{note} hex washer")

    # -- the assembly -----------------------------------------------------
    def build(self, stations: List[Station]) -> None:
        self.build_rails()
        for station in stations:
            self.build_station(station)

    def build_rails(self) -> None:
        """
        The two outrigger rails, each an upper and a lower bar.

        In the reference they run the full plate length just outside the plate
        edge, the upper bar level with the plate top and the lower bar level
        with its underside.  They are what the anchors bolt through.
        """
        rail_w = max(RAIL_W * self.width, 20.0)
        rail_t = max(RAIL_T * self.thick, 6.0)
        inset = self.half_w * RAIL_INSET
        # Keep the rail inside the plate footprint: the reference's plate is
        # narrower than its base envelope, but the project fixes the plate, so
        # the rail is tucked to the plate edge rather than hung outside it.
        inset = min(inset, self.half_w - rail_w / 2)

        for sign in (-1.0, +1.0):
            across = inset * sign
            # The reference's upper rail sits IN the plate's top band
            # (U -300..-280 against a plate top of -280), i.e. flush with the
            # plate surface rather than standing on it.  Emitting it proud left
            # the sole plates landing on top of the rails and produced the
            # stepped, stacked look the client rejected.
            self.add_box(0.0, across, self.plate_top - rail_t / 2,
                         rail_w, self.length, rail_t,
                         "skid rail, upper bar flush in the plate top")
            self.add_box(0.0, across, self.plate_under + rail_t / 2,
                         rail_w, self.length, rail_t,
                         "skid rail, lower bar at the plate underside")

    def build_station(self, station: Station) -> None:
        """
        One machine mounting, assembled bottom-up so every part bears.

        Order and datum, each derived from the member below:

        1. two **sole plates** on the plate top, one either side;
        2. two **gussets** standing on those sole plates;
        3. a **foot pad** spanning both gussets, its TOP at the machine
           underside so the machine seats on it with no gap;
        4. two **side stays** outboard, from the sole plates to the pad;
        5. **anchors** through the sole plates.

        The gusset height is solved from the pad, not assumed: whatever is left
        between the sole-plate top and the pad underside is exactly the height
        the gusset must be, so the chain closes by construction.
        """
        sole_t = max(SOLE_T * self.thick, 8.0)
        sole_w = max(SOLE_W * self.width, 30.0)
        gusset_t = max(GUSSET_T * self.thick, 6.0)
        pad_t = station.pad_thick
        sole_inset = self.half_w * SOLE_INSET
        gusset_inset = self.half_w * GUSSET_INSET
        stay_inset = self.half_w * STAY_INSET
        # Keep every member inside the plate.
        sole_inset = min(sole_inset, self.half_w - sole_w / 2)
        gusset_inset = min(gusset_inset, sole_inset)
        stay_inset = min(stay_inset, self.half_w - gusset_t / 2)

        sole_top = self.plate_top + sole_t
        # The pad's TOP is the machine's underside: that is the whole point of
        # the mounting, and it is set before anything below it is sized.
        pad_top = station.machine_under
        pad_bottom = pad_top - pad_t
        gusset_h = pad_bottom - sole_top

        if gusset_h < 5.0:
            # The machine sits too low for a gusseted pad; thin the pad and
            # sole so the chain still closes rather than emitting a floater.
            available = max(pad_top - self.plate_top, 12.0)
            sole_t = max(available * 0.30, 6.0)
            pad_t = max(available * 0.30, 6.0)
            sole_top = self.plate_top + sole_t
            pad_bottom = pad_top - pad_t
            gusset_h = max(pad_bottom - sole_top, 4.0)

        sole_len = station.length * SOLE_OVERHANG
        label = station.name

        # 1. sole plates, flat on the plate top
        for sign in (-1.0, +1.0):
            self.add_box(station.centre, sole_inset * sign,
                         self.plate_top + sole_t / 2,
                         sole_w, sole_len, sole_t,
                         f"{label} sole plate on the baseplate")

        # 2. gussets standing on the sole plates
        for sign in (-1.0, +1.0):
            self.add_gusset(station.centre, gusset_inset * sign, sole_top,
                            gusset_h, gusset_t,
                            sole_len, sole_len * 0.62,
                            f"{label} gusset, sole plate to foot pad")

        # 3. foot pad spanning both gussets, top at the machine underside.
        #    It must be wide enough to reach both gussets AND long enough to
        #    carry the machine footprint, or the machine overhangs its own
        #    mounting -- which is what the client saw as a misaligned support.
        pad_width = max(gusset_inset * 2 + gusset_t, station.width * 0.95)
        pad_width = min(pad_width, self.width * 0.98)
        self.add_box(station.centre, 0.0, pad_bottom + pad_t / 2,
                     pad_width, station.length, pad_t,
                     f"{label} foot pad carrying the machine")

        # 4. outboard side stays, sole plate up to the pad
        for sign in (-1.0, +1.0):
            self.add_gusset(station.centre, stay_inset * sign, sole_top,
                            max(gusset_h * 0.85, 4.0), gusset_t,
                            station.length * 0.45, station.length * 0.28,
                            f"{label} outboard stay")

        # 5. anchors through the sole plates, two per side
        for sign in (-1.0, +1.0):
            for offset in (-sole_len * 0.34, sole_len * 0.34):
                self.add_anchor(station.centre + offset, sole_inset * sign,
                                sole_top, label)
