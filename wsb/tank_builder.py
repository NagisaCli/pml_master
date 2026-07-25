"""
Tank Geometry Generator
=======================
Turns a :class:`~wsb.equipment_data.TankSpec` into AVEVA E3D primitives.

Positioning contract
--------------------
The project requires every tank's **bottom centre point** to land exactly on the
installation coordinate from the equipment list - not the geometric centre, model
centre or bounding-box centre. That is enforced here in one place: all geometry
is generated in a local frame whose origin is the bottom centre, then translated
by the tank's installation coordinate. :func:`verify_bottom_centre` re-checks the
result against the source data.

The bottom centre is the underside of the *supported* vessel: where a skirt or
legs are present, the datum sits at the bottom of the skirt (the foundation
bearing plane) and the shell starts one skirt-height above it. That matches how
an installation coordinate is set out on site.

Model tree
----------
One ``EQUI`` per item of equipment, named for its tag. Body assemblies get one
``SUBE`` each, and **every nozzle gets its own ``SUBE``** so a piping designer
can select, attach to and modify one connection without disturbing the shell or
its neighbours::

    EQUI /203_TA_006            POS E 0 N 0 U 0
      SUBE /203_TA_006_SUPPORT     skirt or legs, base ring
      SUBE /203_TA_006_SHELL       shell, heads, bottom
      SUBE /203_TA_006_N1          neck + flange
      SUBE /203_TA_006_N2          neck + flange
      ...
      SUBE /203_TA_006_M1          manway
      SUBE /203_TA_006_ACCESS      stiffening rings
      SUBE /203_TA_006_INTERNALS   agitator, if fitted

The EQUI is anchored at ``POS E 0 N 0 U 0``. A bare ``POS`` in E3D is measured
with respect to the owner, not the world - the world form is ``POS ... WRT /*``.
The primitives below hold world-absolute coordinates, so the EQUI must sit at
zero; if it inherited a position the whole tank would shift by that amount.
"""

from __future__ import annotations

import math
import re
from typing import List, Optional, Sequence, Tuple

from .schema import (
    AgitatorType,
    BottomType,
    HeadType,
    Nozzle,
    SupportType,
    TankSpec,
)
from .pml_builder import PMLBuilder, PMLValidationError

__all__ = ["TankBuilder", "build_tank", "verify_bottom_centre"]


#: Wall thickness used for the visual shell envelope of double-shell towers (mm).
#: A Reference Value - the equipment list gives outer and inner diameters but no
#: annulus detail.
_DEFAULT_INSULATION_MM = 100.0

#: Radial projection of a nozzle beyond the shell (mm). Long enough to clear
#: insulation and present a face the piping designer can connect to.
_NOZZLE_PROJECTION_MM = 350.0

#: Nozzle length band by bore (mm) - a Reference Value.
#:
#: No nozzle projection is given in the project data, so length follows normal
#: vessel practice: a nozzle must clear the shell insulation and any reinforcing
#: pad and still leave the flange face accessible for bolting, and a larger bore
#: needs a proportionally longer neck to do it. Refine these once the vendor's
#: nozzle schedule is issued.
_NOZZLE_LENGTH_BANDS: Tuple[Tuple[int, float], ...] = (
    (80, 250.0),
    (150, 300.0),
    (300, 350.0),
    (600, 450.0),
)
#: Length for any bore above the largest band (mm).
_NOZZLE_LENGTH_MAX_MM = 550.0

#: How far a nozzle neck is sunk into the shell wall (mm), so it reads as
#: penetrating the vessel rather than merely abutting it. Without this the neck
#: and shell share a tangent surface, which renders as a visible seam.
_NOZZLE_EMBED_MM = 50.0

#: How far a nozzle barrel penetrates past the shell face (mm).
#:
#: A NOZZLE is positioned by its **flange face**, so this is what decides how
#: much of the barrel ends up inside the vessel and how much projects outside:
#: the barrel spans ``face - penetration`` to ``face - penetration + length``.
#:
#: 100 mm is a deliberate middle setting. Using the full nozzle length as the
#: offset would leave the barrel merely touching the shell - no penetration, and
#: the maximum unsupported stub outside, which reads as unrealistic. Too little
#: and the connection buries itself again. At 100 the barrel passes convincingly
#: through the plate while 150-450 mm still projects for piping, depending on
#: bore.
_NOZZLE_WALL_PENETRATION_MM = 100.0

#: Unit vector for each cardinal axis, as (east, north).
_AXIS_UNIT = {
    "E": (1.0, 0.0),
    "W": (-1.0, 0.0),
    "N": (0.0, 1.0),
    "S": (0.0, -1.0),
}

#: Flange thickness and diameter oversize relative to the nozzle bore (mm).
_FLANGE_THICKNESS_MM = 40.0
_FLANGE_OVERSIZE_MM = 120.0

#: Reinforcing pad at a shell penetration (mm). Smallest bore that gets one,
#: how far it extends past the bore, and its plate thickness.
_PAD_MIN_DN = 100
_PAD_OVERSIZE_MM = 220.0
_PAD_THICKNESS_MM = 30.0

#: Stiffening ring section (mm): radial projection and vertical depth.
_RING_PROJECTION_MM = 120.0
_RING_DEPTH_MM = 200.0

#: Roof curb / compression ring at the roof-to-shell joint (mm).
_CURB_PROJECTION_MM = 100.0
_CURB_DEPTH_MM = 250.0
#: Cap closing the apex ring of a conical roof (mm).
_APEX_CAP_MM = 60.0

#: Access platform width and grating thickness (mm).
_PLATFORM_WIDTH_MM = 1200.0
_PLATFORM_THICKNESS_MM = 60.0

# -- Access ladder (Reference Value) ----------------------------------------
# Deliberately minimal. Assumed access steel that projects far from the shell is
# what produced tank-to-tank clashes with real equipment before; this reads as a
# ladder without occupying space a piping or steel designer needs.

#: Cardinal axis the ladder is mounted on. West is clear of the manway face
#: (45/135 deg) used throughout these nozzle schedules.
_LADDER_AXIS = "W"
#: Ladder width between stringers, stringer bar diameter, and cage hoop section.
_LADDER_WIDTH_MM = 600.0
_LADDER_STRINGER_DN = 60.0
_LADDER_HOOP_MM = 50.0
#: How far the cage stands off the shell (mm).
_LADDER_CAGE_PROJECTION_MM = 700.0
#: Vertical spacing of cage hoops (mm).
_LADDER_HOOP_SPACING_MM = 3000.0
#: Ladder starts this far above the datum, the normal first-rung height (mm).
_LADDER_BASE_MM = 300.0
#: Shortest run worth a fixed ladder (mm); below this the vessel is reached from
#: grade and a ladder would be fabricated detail serving nothing.
_LADDER_MIN_HEIGHT_MM = 4000.0

#: Support leg section for leg-supported vessels (mm).
_LEG_SECTION_MM = 200.0
#: Number of legs on a leg-supported vessel.
_LEG_COUNT = 4
#: Bolted foot at the base of each leg (mm). Its thickness sits within the base
#: plate so it adds nothing below the bottom-centre datum.
_LEG_FOOT_MM = 320.0
_LEG_FOOT_THICKNESS_MM = 25.0
#: Gusset stiffening a leg into the vessel bottom (mm).
_LEG_GUSSET_MM = 300.0

#: Skirt access opening and vents (mm). Modelled as raised collars: E3D
#: primitives are solid, so an opening reads as a collar rather than a hole.
_SKIRT_OPENING_DN = 600.0
_SKIRT_VENT_DN = 200.0
_SKIRT_COLLAR_MM = 60.0
#: Shortest skirt that can take an access opening (mm).
_SKIRT_OPENING_MIN_MM = 1200.0

# -- Agitators and scrapers (Reference Values) ------------------------------
# No agitator is dimensioned in the project data: the drawings show that a unit
# is fitted and how it is mounted, not its size. These proportions follow normal
# Valmet/ANDRITZ pulp-mill practice and are reported as Reference Values.

#: Agitator shaft diameter (mm).
_AGITATOR_SHAFT_DN = 180.0
#: Height of the pedestal carrying a top-entry drive above the roof (mm).
_AGITATOR_PEDESTAL_MM = 400.0
#: Impeller hub depth and blade thickness (mm).
_IMPELLER_HUB_MM = 150.0
_IMPELLER_BLADE_MM = 120.0
#: Shell height above which a top-entry agitator gets a second impeller (mm).
#: One impeller cannot turn over the full depth of a storage tower.
_TWIN_IMPELLER_HEIGHT_MM = 12000.0

#: Cardinal axis a side-entry agitator is mounted on. A cardinal is required
#: because E3D extrudes primitives along cardinal axes only.
_SIDE_ENTRY_AXIS = "S"
#: Mounting nozzle bore for a side-entry agitator (mm).
_SIDE_ENTRY_NOZZLE_DN = 500.0

#: Bottom-entry discharge scraper proportions (mm).
_SCRAPER_DRIVE_DN = 1400.0
_SCRAPER_DRIVE_MM = 700.0
_SCRAPER_HUB_DN = 900.0
_SCRAPER_HUB_MM = 400.0
_SCRAPER_ARM_MM = 250.0
#: Fraction of the shell diameter the sweep arms cover. Short of the wall so the
#: arms clear the shell and any bottom-course weld.
_SCRAPER_SWEEP_FRACTION = 0.82


def _nozzle_length(bore_dn: int) -> float:
    """
    Projection from the shell to the flange face for a given bore (mm).

    A Reference Value: see :data:`_NOZZLE_LENGTH_BANDS`. Larger bores get longer
    necks so the flange stays clear of the shell and its reinforcing pad.
    """
    for limit, length in _NOZZLE_LENGTH_BANDS:
        if bore_dn <= limit:
            return length
    return _NOZZLE_LENGTH_MAX_MM


class TankBuilder:
    """
    Generates the primitives for one tank.

    Args:
        spec: The tank to model.
        builder: Builder to emit into. Supplying a shared builder places several
            tanks in one macro under a single top-level EQUI.
    """

    def __init__(self, spec: TankSpec, builder: PMLBuilder) -> None:
        self.spec = spec
        self.b = builder
        self._prefix = spec.tag.replace("-", "_")

    # -- frame ----------------------------------------------------------

    @property
    def _origin(self) -> Tuple[float, float, float]:
        """The installation coordinate: the tank's bottom centre point."""
        return self.spec.position

    def _at(self, du: float, de: float = 0.0, dn: float = 0.0) -> Tuple[float, float, float]:
        """
        Translate a point from the local frame into world coordinates.

        Args:
            du: Height above the bottom centre datum (mm).
            de: Offset East of the vessel centreline (mm).
            dn: Offset North of the vessel centreline (mm).
        """
        east, north, up = self._origin
        return (east + de, north + dn, up + du)

    @property
    def _shell_base(self) -> float:
        """
        Local height at which the shell starts.

        Skirt- and leg-supported vessels carry the shell one support height above
        the datum; ground-bearing vessels start at the datum itself.
        """
        return self.spec.skirt_height

    @property
    def _shell_top(self) -> float:
        """Local height of the top tangent line, where the head begins."""
        return self._shell_base + self.spec.height

    # -- entry point ----------------------------------------------------

    def build(self) -> None:
        """Emit every assembly for this tank."""
        s = self.spec
        self.b.comment()
        self.b.banner(f"{s.tag}  {s.name}")
        self.b.comment(f"Area:        {s.area}")
        self.b.comment(
            f"Bottom centre (installation coordinate): "
            f"E {s.position[0]:.1f}  N {s.position[1]:.1f}  U {s.position[2]:.1f}"
        )
        self.b.comment(
            f"Shell:       DN{s.diameter:.0f} x {s.height:.0f} high"
            + (f", outer envelope DN{s.outer_diameter:.0f}" if s.outer_diameter else "")
        )
        self.b.comment(f"Closure:     {s.head.value} / {s.bottom.value}")
        self.b.comment(f"Support:     {s.support.value}")
        if s.volume_m3:
            self.b.comment(f"Volume:      {s.volume_m3:.0f} m3")
        self.b.comment()

        # One EQUI per item of equipment, per AVEVA hierarchy convention.
        self.b.equi(s.tag)

        self._build_support()
        self._build_shell()
        self._build_nozzles()
        self._build_access()
        self._build_internals()

    # -- support --------------------------------------------------------

    def _build_support(self) -> None:
        """Skirt, legs or slab bearing, occupying the datum-to-shell gap."""
        s = self.spec
        if s.support is SupportType.GROUND or s.skirt_height <= 0:
            return

        self.b.sube(f"{self._prefix}_SUPPORT")

        if s.support is SupportType.SKIRT:
            # A skirt is a cylindrical shell continuing the vessel bore down to
            # the foundation, so its bottom face sits exactly on the datum.
            self.b.cyli(
                s.diameter,
                s.skirt_height,
                self._at(0.0),
                label=f"Skirt support, {s.skirt_height:.0f} high to shell tangent",
            )
            # Base ring transferring load to the foundation.
            self.b.cyli(
                s.diameter + 300.0,
                30.0,
                self._at(0.0),
                label="Skirt base ring",
            )
            self._build_skirt_details()
        elif s.support is SupportType.LEGS:
            self.b.comment(
                f"{_LEG_COUNT} support legs on a {s.diameter:.0f} bolt circle"
            )
            # Base plate at the foundation bearing plane. Legs are boxes
            # positioned by their centre, so without this plate no primitive
            # would sit on the bottom-centre datum and the installation
            # coordinate would not be represented in the model.
            self.b.cyli(
                s.diameter + 200.0,
                25.0,
                self._at(0.0),
                label="Support base plate at foundation bearing plane",
            )
            radius = s.diameter / 2.0 - _LEG_SECTION_MM
            for i in range(_LEG_COUNT):
                angle = math.radians(45.0 + i * 360.0 / _LEG_COUNT)
                offset_e = radius * math.cos(angle)
                offset_n = radius * math.sin(angle)
                self.b.box(
                    _LEG_SECTION_MM,
                    _LEG_SECTION_MM,
                    s.skirt_height,
                    self._at(s.skirt_height / 2.0, offset_e, offset_n),
                    label=f"Leg {i + 1}",
                )
                # Bolted foot at the bottom of each leg, sitting on the base
                # plate. Kept inside the plate thickness so it adds no depth
                # below the datum.
                self.b.box(
                    _LEG_FOOT_MM,
                    _LEG_FOOT_MM,
                    _LEG_FOOT_THICKNESS_MM,
                    self._at(_LEG_FOOT_THICKNESS_MM / 2.0, offset_e, offset_n),
                    label=f"Leg {i + 1} base plate",
                )
                # Gusset stiffening the leg into the vessel bottom, the usual
                # detail where a leg meets a dished head.
                self.b.box(
                    _LEG_GUSSET_MM,
                    _LEG_GUSSET_MM,
                    _LEG_GUSSET_MM,
                    self._at(
                        s.skirt_height - _LEG_GUSSET_MM / 2.0,
                        offset_e * 0.86,
                        offset_n * 0.86,
                    ),
                    label=f"Leg {i + 1} top gusset",
                )

    def _build_skirt_details(self) -> None:
        """
        Access opening and vents on a skirt.

        Every skirt-supported vessel has an opening for access to the bottom
        head and its connections, and vents to stop vapour collecting inside.
        They are modelled as raised collars on the skirt surface: E3D primitives
        are solid, so a hole cannot be cut without a negative primitive, and the
        collar is what actually reads as an opening in a shaded view.
        """
        s = self.spec
        if s.skirt_height < _SKIRT_OPENING_MIN_MM:
            # Too short to take a manway-sized opening; a low skirt is a plain
            # ring in practice.
            return

        opening = min(_SKIRT_OPENING_DN, s.skirt_height - 300.0)
        wall = s.diameter / 2.0 - _NOZZLE_EMBED_MM
        # Opposite the side-entry agitator axis so the two cannot collide.
        axis = "N"
        unit_e, unit_n = _AXIS_UNIT[axis]
        elevation = opening / 2.0 + 150.0

        self.b.cyli(
            opening,
            _SKIRT_COLLAR_MM,
            self._at(elevation, wall * unit_e, wall * unit_n),
            axis=axis,
            label=f"Skirt access opening, DN{opening:.0f}",
        )

        # Vent holes near the top of the skirt, on the two side axes.
        for vent_axis in ("E", "W"):
            vent_e, vent_n = _AXIS_UNIT[vent_axis]
            self.b.cyli(
                _SKIRT_VENT_DN,
                _SKIRT_COLLAR_MM,
                self._at(
                    s.skirt_height - _SKIRT_VENT_DN,
                    wall * vent_e,
                    wall * vent_n,
                ),
                axis=vent_axis,
                label=f"Skirt vent {vent_axis}",
            )

    # -- shell and closures ---------------------------------------------

    def _build_shell(self) -> None:
        """Bottom closure, cylindrical shell, top closure, outer envelope."""
        s = self.spec
        self.b.sube(f"{self._prefix}_SHELL")

        self._build_bottom()

        self.b.cyli(
            s.diameter,
            s.height,
            self._at(self._shell_base),
            label=f"Shell: DN{s.diameter:.0f} x {s.height:.0f}",
        )

        self._build_head()

        if s.outer_diameter and s.outer_diameter > s.diameter:
            # Double-shell tower: the equipment list gives an outside and an
            # inside diameter. Modelled as an outer envelope over the shell
            # height so clash detection sees the true occupied envelope.
            self.b.cyli(
                s.outer_diameter,
                s.height,
                self._at(self._shell_base),
                label=(
                    f"Outer shell / insulation envelope DN{s.outer_diameter:.0f} "
                    f"(annulus {(s.outer_diameter - s.diameter) / 2:.0f} radial)"
                ),
            )

    def _build_bottom(self) -> None:
        """
        Bottom closure.

        A conical bottom occupies the space directly above the shell base, so the
        shell is not shortened for it: the cone sits inside the skirt where one is
        fitted, which is how upflow towers are actually arranged.
        """
        s = self.spec
        if s.bottom is BottomType.CONICAL and s.cone_height > 0:
            outlet = s.cone_outlet_dn or 300.0
            # Cone narrows downward: wide top at the shell base, outlet below.
            self.b.cone(
                outlet,
                s.diameter,
                s.cone_height,
                self._at(max(0.0, self._shell_base - s.cone_height)),
                label=(
                    f"Conical bottom, {s.cone_height:.0f} high, "
                    f"DN{outlet:.0f} outlet"
                ),
            )
        elif s.bottom is BottomType.DISHED:
            # A dished bottom bulges downward from the shell tangent line, so it
            # can only occupy space the support provides. On a skirt or legs the
            # rise is capped at the support height; a ground-bearing vessel has
            # no room at all, and its bottom is dished upward into the shell
            # instead - which is how a flat-bottom storage tower is actually
            # built. Without this cap the head would extend below the foundation.
            preferred = s.diameter / 4.0
            if self._shell_base > 0:
                rise = min(preferred, self._shell_base)
                self.b.dish_down(
                    s.diameter,
                    rise,
                    self._at(self._shell_base),
                    label=f"Dished bottom head, {rise:.0f} rise",
                )
            else:
                self.b.cyli(
                    s.diameter,
                    20.0,
                    self._at(0.0),
                    label="Bottom plate on slab (dished head has no clearance below grade)",
                )
        else:
            self.b.cyli(
                s.diameter,
                20.0,
                self._at(self._shell_base),
                label="Flat bottom plate",
            )

    def _build_head(self) -> None:
        """Top closure at the shell's top tangent line."""
        s = self.spec
        top = self._shell_top

        if s.head is HeadType.DISHED:
            rise = s.head_height or s.diameter / 4.0
            self.b.dish(
                s.diameter,
                rise,
                self._at(top),
                label=f"Dished top head, {rise:.0f} rise",
            )
        elif s.head is HeadType.CONICAL:
            rise = s.head_height or s.diameter * 0.15
            # Curb angle at the roof-to-shell joint. A real conical-roof tank has
            # a compression ring here, and it gives the roofline a defined edge
            # instead of a bare cone-on-cylinder junction.
            self.b.cyli(
                s.diameter + 2 * _CURB_PROJECTION_MM,
                _CURB_DEPTH_MM,
                self._at(top - _CURB_DEPTH_MM),
                label="Roof curb / compression ring",
            )
            # Conical roof closing to a small apex ring, the normal arrangement
            # for an atmospheric process tank.
            apex_dn = min(300.0, s.diameter * 0.1)
            self.b.cone(
                s.diameter,
                apex_dn,
                rise,
                self._at(top),
                label=f"Conical roof, {rise:.0f} rise",
            )
            # Cap closing the apex ring, so the roof does not read as open.
            self.b.cyli(
                apex_dn + 100.0,
                _APEX_CAP_MM,
                self._at(top + rise),
                label="Roof apex cap",
            )
        else:
            # Flat roof: a plate, never a DISH. Per Iron Rule 2 a DISH at this
            # diameter would create a large hemispherical bulge.
            self.b.cyli(
                s.diameter,
                25.0,
                self._at(top),
                label="Flat roof plate",
            )
            # Rim angle stiffening the plate edge, as on a fabricated flat cover.
            self.b.cyli(
                s.diameter + 2 * _CURB_PROJECTION_MM,
                _CURB_DEPTH_MM,
                self._at(top - _CURB_DEPTH_MM),
                label="Roof rim angle",
            )

    # -- nozzles --------------------------------------------------------

    def _build_nozzles(self) -> None:
        """
        Native E3D ``NOZZLE`` elements, placed from the bottom-centre datum.

        Each nozzle gets its own SUBE, kept separate from the vessel body and
        from every other nozzle. That is what lets a piping designer select,
        attach to and modify one connection without disturbing the shell or its
        neighbours, and it is the arrangement AVEVA's equipment hierarchy
        expects.

        A nozzle is a **catalogue element**, not an assembly of primitives: its
        flange, face position and bore come from the specification component it
        references, so no CYLI is emitted for the neck or the flange. The one
        primitive that remains alongside a nozzle is the reinforcing pad, which
        is vessel shell plate rather than part of the nozzle itself.
        """
        s = self.spec
        for nozzle in s.nozzles:
            self.b.sube(f"{self._prefix}_{nozzle.name}")
            self.b.comment(
                f"{nozzle.name}  DN{nozzle.dn}  EL +{nozzle.elevation:.0f}  -  "
                f"{nozzle.service}"
            )
            if nozzle.vertical:
                self._build_vertical_nozzle(nozzle)
            else:
                self._build_radial_nozzle(nozzle)

    def _nozzle_datum_radius(self, bore_dn: int) -> float:
        """
        Radius at which a radial nozzle's ``POS`` is placed (mm).

        **A NOZZLE is positioned by its flange face, not by its root.** The
        barrel runs back from ``POS`` toward the vessel along the nozzle axis,
        so the flange face must sit a full nozzle length *outside* the point
        where the barrel should meet the shell.

        Placing ``POS`` on the shell face instead put the whole barrel inside
        the tank: for a DN400 with a 450 long neck on a DN5600 shell, the barrel
        spanned N 22160..22610 against a shell face at N 22660 - entirely
        buried, with only the flange rim showing where it pierced the plate.

        The barrel is sunk :data:`_NOZZLE_WALL_PENETRATION_MM` past the shell
        face so it reads as penetrating the wall rather than butting against it,
        leaving ``length - penetration`` projecting for the piping designer::

            POS radius = shell_face - penetration + length

        Args:
            bore_dn: Nominal bore (mm), which selects the length band.
        """
        s = self.spec
        face = (s.outer_diameter or s.diameter) / 2.0
        return face - _NOZZLE_WALL_PENETRATION_MM + _nozzle_length(bore_dn)

    def _build_radial_nozzle(self, nozzle: Nozzle) -> None:
        """
        Nozzle projecting horizontally from the shell.

        The nozzle is positioned at the shell surface and projects outward along
        its bearing, so its flange face is clear of the shell for connection.
        """
        s = self.spec

        # A nozzle is placed on the cardinal direction nearest its bearing.
        # E3D orients on cardinal axes, so placing it at the true bearing while
        # orienting on a cardinal leaves the connection point off the shell -
        # the nozzle appears to float beside the vessel.
        axis = self._bearing_axis(nozzle.bearing)
        unit_e, unit_n = _AXIS_UNIT[axis]

        # A NOZZLE's POS is its FLANGE FACE, not its root on the shell, so the
        # barrel runs back from POS towards the vessel. Placing POS at the shell
        # face (less an embed) therefore put the entire barrel *inside* the tank,
        # with only the flange rim emerging - see _nozzle_datum_radius.
        wall = self._nozzle_datum_radius(nozzle.dn)
        height = self._shell_base + nozzle.elevation

        # Reinforcing pad around the shell penetration. This stays a primitive:
        # it is shell plate welded to the vessel, not part of the nozzle
        # catalogue component, and a real vessel has one at every larger bore.
        #
        # The pad is set out from the shell FACE, not from the nozzle's embedded
        # base. Taking the nozzle's `wall` put the pad's outer surface at
        # face - embed, burying all 104 pads inside the shell where none of them
        # could be seen. A welded pad lies on the outside of the plate.
        # cyli() takes the BASE face, so passing the shell radius makes the pad
        # span face .. face + thickness: welded onto the outside of the plate.
        if nozzle.dn >= _PAD_MIN_DN:
            face = (s.outer_diameter or s.diameter) / 2.0
            self.b.cyli(
                nozzle.dn + _PAD_OVERSIZE_MM,
                _PAD_THICKNESS_MM,
                self._at(height, face * unit_e, face * unit_n),
                axis=axis,
                label=f"{nozzle.name} reinforcing pad",
            )

        self.b.nozzle(
            f"{self._prefix}_{nozzle.name}_NOZZ",
            nozzle.dn,
            _nozzle_length(nozzle.dn),
            self._at(height, wall * unit_e, wall * unit_n),
            axis=axis,
            label=(
                f"{nozzle.name}  DN{nozzle.dn}  EL +{nozzle.elevation:.0f}  "
                f"{nozzle.bearing:.0f} deg  -  {nozzle.service}"
            ),
        )

    def _build_vertical_nozzle(self, nozzle: Nozzle) -> None:
        """
        Nozzle on the roof or in the floor.

        A roof nozzle projects up from the head; a floor nozzle (elevation 0)
        projects down from the bottom, which is how a bottom cone outlet or a
        drain connects.
        """
        s = self.spec
        on_roof = nozzle.elevation > 0
        axis = "U"

        # A NOZZLE's POS is its FLANGE FACE and its barrel runs back toward the
        # vessel, so the datum sits one nozzle length beyond where the barrel
        # should meet the plate - exactly as for a radial nozzle.
        length = _nozzle_length(nozzle.dn)

        if on_roof:
            # Set the nozzle off the centreline so it does not collide with the
            # agitator drive, then find the roof height at that radius. A
            # conical roof slopes away from its apex, so a nozzle placed at the
            # apex height would hang in mid-air above the sloping plate.
            offset = s.diameter * 0.2
            plate_u = self._shell_top + self._roof_rise_at(offset)
            base_u = plate_u - _NOZZLE_WALL_PENETRATION_MM + length
        else:
            # Bottom outlet through the floor, pointing UP into the vessel: the
            # flange face is the lowest point, so the datum sits on the floor
            # itself and the barrel rises from there. Nothing may hang below the
            # bottom-centre datum (IR-6), which is what makes this case differ
            # from the roof: there is no room to offset downward.
            offset = 0.0
            plate_u = 0.0
            base_u = 0.0

        # Reinforcing pad at the penetration, as on a radial nozzle: set out from
        # the plate surface rather than from the nozzle's embedded base, so it
        # lies on the outside of the plate instead of being sunk into it.
        if nozzle.dn >= _PAD_MIN_DN:
            # The pad belongs on the plate the nozzle passes through, not at the
            # flange face, so it is set out from plate_u rather than base_u.
            pad_base = plate_u if on_roof else base_u
            self.b.cyli(
                nozzle.dn + _PAD_OVERSIZE_MM,
                _PAD_THICKNESS_MM,
                self._at(pad_base, offset),
                axis=axis,
                label=f"{nozzle.name} reinforcing pad",
            )

        self.b.nozzle(
            f"{self._prefix}_{nozzle.name}_NOZZ",
            nozzle.dn,
            _nozzle_length(nozzle.dn),
            self._at(base_u, offset),
            axis=axis,
            label=(
                f"{nozzle.name}  DN{nozzle.dn}  "
                f"{'roof' if on_roof else 'bottom'} nozzle  -  {nozzle.service}"
            ),
        )

    def _roof_rise_at(self, radius: float) -> float:
        """
        Height of the roof above the top tangent line at a given radius.

        A flat roof is level, so the rise is zero everywhere. A conical roof
        falls linearly from its apex to the shell rim, and a dished head is
        approximated the same way - close enough to seat a nozzle on the plate
        rather than leaving it floating above or sunk below.
        """
        s = self.spec
        if s.head is HeadType.FLAT:
            return 0.0
        rise = s.head_height or (
            s.diameter / 4.0 if s.head is HeadType.DISHED else s.diameter * 0.15
        )
        shell_radius = s.diameter / 2.0
        if shell_radius <= 0:
            return 0.0
        fraction = max(0.0, 1.0 - radius / shell_radius)
        return rise * fraction

    @staticmethod
    def _bearing_axis(bearing: float) -> str:
        """
        Map a plan bearing to the nearest cardinal axis.

        E3D primitives orient along cardinal axes, so a nozzle is placed at its
        true bearing but oriented to the nearest of East/North/West/South. For
        the 45-degree spacing used in these schedules this keeps every nozzle
        within 45 degrees of its nominal direction, which is adequate for
        piping-readiness and avoids skewed primitives that complicate editing.
        """
        normalized = bearing % 360.0
        if normalized < 45.0 or normalized >= 315.0:
            return "E"
        if normalized < 135.0:
            return "N"
        if normalized < 225.0:
            return "W"
        return "S"

    # -- access and reinforcement ---------------------------------------

    def _build_access(self) -> None:
        """Stiffening rings, access ladder and platforms."""
        s = self.spec
        self.b.sube(f"{self._prefix}_ACCESS")

        if s.stiffening_rings:
            # Rings spread evenly up the shell, the usual arrangement for
            # resisting buckling on a tall thin-walled vessel. On a double-shell
            # tower they belong on the outer envelope - sized to the inner shell
            # they would sit entirely inside the annulus and never be seen.
            ring_base = s.outer_diameter or s.diameter
            spacing = s.height / (s.stiffening_rings + 1)
            for i in range(1, s.stiffening_rings + 1):
                self.b.cyli(
                    ring_base + 2 * _RING_PROJECTION_MM,
                    _RING_DEPTH_MM,
                    self._at(self._shell_base + spacing * i),
                    label=f"Stiffening ring {i} of {s.stiffening_rings}",
                )

        self._build_ladder()

        # Access platforms are recorded in the spec but deliberately NOT modelled
        # as geometry. Their elevations are Reference Values, and a full 1200 mm
        # annular platform around every tower is not how a bleach plant is laid
        # out - platforms are partial, shared between adjacent towers, and set
        # out by the steel designer. Drawing them as full rings produced clashes
        # between assumed steel and real equipment (e.g. 205-TA-042 against
        # 205-TA-059, whose shells are actually 1377 mm clear), which would send
        # a reviewer chasing a problem that does not exist.
        for elevation in s.platform_elevations:
            self.b.comment(
                f"Access platform required at EL +{elevation:.0f} "
                f"(Reference Value - extent and support to be set by steel design)"
            )

    def _build_ladder(self) -> None:
        """
        Caged access ladder up the shell.

        Kept deliberately tight to the shell. The platforms were removed from
        this model because full-ring assumed steel clashed with real equipment;
        a ladder carries the same risk, so it projects only far enough to read
        as a ladder (stringers plus a cage hoop) and sits on the cardinal axis
        that no nozzle in these schedules uses as a manway face.

        The ladder is modelled from the datum to the top tangent line, not to
        the roof apex: it must not overhang the roof or extend below the
        foundation bearing plane.
        """
        s = self.spec
        top = self._shell_top
        if top - _LADDER_BASE_MM < _LADDER_MIN_HEIGHT_MM:
            # A short tank is reached from grade or a local platform; a fixed
            # ladder would be fabricated detail with nothing to serve.
            return

        radius = (s.outer_diameter or s.diameter) / 2.0
        unit_e, unit_n = _AXIS_UNIT[_LADDER_AXIS]
        run = top - _LADDER_BASE_MM

        # Two stringers, offset either side of the ladder centreline. The offset
        # is perpendicular to the mounting axis, so it swaps E and N.
        for side in (-1.0, 1.0):
            half = _LADDER_WIDTH_MM / 2.0 * side
            self.b.cyli(
                _LADDER_STRINGER_DN,
                run,
                self._at(
                    _LADDER_BASE_MM,
                    radius * unit_e + half * unit_n,
                    radius * unit_n + half * unit_e,
                ),
                label=f"Access ladder stringer {'A' if side < 0 else 'B'}",
            )

        # Cage hoops are NOT modelled as geometry.
        #
        # They were, and they are what produced the row of floating discs beside
        # every tank. A cage hoop is an annulus, and E3D's CYLI is solid with no
        # inner diameter, so the nearest primitive to a DN700 hoop is a DN700
        # *disc*. Worse, it was oriented along the radial axis - the axis the
        # hoop stands off on - which turned its flat face towards the vessel and
        # left it hanging in clear air:
        #
        #     203-TA-006: shell face at E 12200, disc spanning E 11800..11850
        #                 -> a 350 mm gap, repeated up the shell
        #
        # A hoop can only be built honestly from an arrayed set of small slices
        # around the ring (IR-9), which is a dozen primitives per hoop and up to
        # seven hoops per tank for assumed access steel that no drawing
        # dimensions. Per IR-10 that detail is not justifiable, so the cage is
        # reported rather than drawn - the same call already made for the access
        # platforms below, and for the same reason.
        count = max(1, int(run // _LADDER_HOOP_SPACING_MM))
        self.b.comment(
            f"Ladder safety cage required over the {run:.0f} run "
            f"({count} hoops at {_LADDER_HOOP_SPACING_MM:.0f} centres, "
            f"Reference Value - extent and fixings to be set by steel design)"
        )

    # -- internals ------------------------------------------------------

    def _build_internals(self) -> None:
        """
        Mixing equipment, in the arrangement the reference drawing shows.

        The three mountings occupy entirely different space on the vessel, so
        each is built separately rather than approximated by one shape. Drawing a
        roof drive on a tower whose scraper is under the floor would put
        fabricated steel where the real tower has clear air, and leave the real
        drive unmodelled.
        """
        mixer = self.spec.mixer
        if mixer is AgitatorType.NONE:
            return
        self.b.sube(f"{self._prefix}_INTERNALS")

        if mixer is AgitatorType.TOP_ENTRY:
            self._build_top_entry_agitator()
        elif mixer is AgitatorType.SIDE_ENTRY:
            self._build_side_entry_agitator()
        else:
            self._build_bottom_scraper()

    def _build_top_entry_agitator(self) -> None:
        """
        Roof-mounted drive with a vertical shaft down the centreline.

        The drive sits on a mounting pedestal above the roof plate rather than
        directly on it, which is how a gearbox is actually carried and what
        gives the roofline its recognisable stepped profile.
        """
        s = self.spec
        roof_apex = self._shell_top + (s.head_height or 0.0)

        # Mounting nozzle and stool carrying the gearbox above the roof.
        pedestal_dn = max(600.0, s.diameter * 0.12)
        self.b.cyli(
            pedestal_dn,
            _AGITATOR_PEDESTAL_MM,
            self._at(roof_apex),
            label="Agitator mounting pedestal on roof",
        )
        pedestal_top = roof_apex + _AGITATOR_PEDESTAL_MM
        self.b.cyli(
            pedestal_dn + 200.0,
            _FLANGE_THICKNESS_MM,
            self._at(pedestal_top),
            label="Agitator mounting flange",
        )

        # Gearbox, then the motor stacked on it - the stepped silhouette that
        # makes a top-entry unit recognisable from a plain box.
        gearbox_base = pedestal_top + _FLANGE_THICKNESS_MM
        self.b.box(
            1200.0, 900.0, 700.0,
            self._at(gearbox_base + 350.0),
            label="Agitator gearbox",
        )
        self.b.cyli(
            700.0,
            900.0,
            self._at(gearbox_base + 700.0),
            label="Agitator drive motor",
        )

        # Shaft from just under the roof down to the impellers.
        shaft_top = roof_apex
        shaft_bottom = self._shell_base + s.height * 0.15
        self.b.cyli(
            _AGITATOR_SHAFT_DN,
            shaft_top - shaft_bottom,
            self._at(shaft_bottom),
            label="Agitator shaft",
        )

        # Two impellers on a tall vessel, one on a short one: a single impeller
        # cannot turn over the full depth of a storage tower.
        impeller_diameter = s.diameter * 0.35
        elevations = [self._shell_base + s.height * 0.18]
        if s.height > _TWIN_IMPELLER_HEIGHT_MM:
            elevations.append(self._shell_base + s.height * 0.55)
        for index, elevation in enumerate(elevations, 1):
            self._build_impeller(impeller_diameter, elevation, index, len(elevations))

    def _build_impeller(
        self, diameter: float, elevation: float, index: int, total: int
    ) -> None:
        """
        One impeller: a hub with radial blades.

        Modelled as blades rather than the solid disc used previously. A disc at
        impeller diameter reads as a plate closing off the vessel bore, which is
        both wrong and visually alarming in a section view.
        """
        label = f"Impeller {index} of {total}" if total > 1 else "Impeller"
        self.b.cyli(
            _AGITATOR_SHAFT_DN * 1.8,
            _IMPELLER_HUB_MM,
            self._at(elevation),
            label=f"{label} hub, DN{diameter:.0f} swept",
        )
        # Blades on the cardinal axes: E3D extrudes along cardinals, so four
        # blades land exactly rather than being rotated approximations.
        blade_length = (diameter - _AGITATOR_SHAFT_DN) / 2.0
        for axis in ("E", "N", "W", "S"):
            unit_e, unit_n = _AXIS_UNIT[axis]
            start = _AGITATOR_SHAFT_DN / 2.0
            self.b.box(
                blade_length if axis in ("E", "W") else _IMPELLER_BLADE_MM,
                blade_length if axis in ("N", "S") else _IMPELLER_BLADE_MM,
                _IMPELLER_HUB_MM,
                self._at(
                    elevation + _IMPELLER_HUB_MM / 2.0,
                    (start + blade_length / 2.0) * unit_e,
                    (start + blade_length / 2.0) * unit_n,
                ),
                label=f"{label} blade {axis}",
            )

    def _build_side_entry_agitator(self) -> None:
        """
        Motor and gearbox on a shell nozzle low down, with a short shaft inboard.

        This is the blow-tank arrangement: the drive hangs off the shell rather
        than the roof, so all of its steel is outside the vessel and has to
        clear the skirt.
        """
        s = self.spec
        # Low on the shell, above the bottom cone so the drive clears the skirt.
        elevation = self._shell_base + max(1500.0, s.height * 0.12)
        axis = _SIDE_ENTRY_AXIS
        unit_e, unit_n = _AXIS_UNIT[axis]
        wall = s.diameter / 2.0 - _NOZZLE_EMBED_MM

        # Mounting nozzle through the shell.
        self.b.cyli(
            _SIDE_ENTRY_NOZZLE_DN,
            _NOZZLE_PROJECTION_MM,
            self._at(elevation, wall * unit_e, wall * unit_n),
            axis=axis,
            label="Side-entry agitator mounting nozzle",
        )
        face = wall + _NOZZLE_PROJECTION_MM
        self.b.cyli(
            _SIDE_ENTRY_NOZZLE_DN + _FLANGE_OVERSIZE_MM,
            _FLANGE_THICKNESS_MM,
            self._at(elevation, (face - _FLANGE_THICKNESS_MM) * unit_e,
                     (face - _FLANGE_THICKNESS_MM) * unit_n),
            axis=axis,
            label="Side-entry agitator mounting flange",
        )

        # Gearbox and motor outboard of the flange, on the nozzle centreline.
        gearbox_start = face
        self.b.cyli(
            700.0,
            600.0,
            self._at(elevation, gearbox_start * unit_e, gearbox_start * unit_n),
            axis=axis,
            label="Side-entry agitator gearbox",
        )
        motor_start = gearbox_start + 600.0
        self.b.cyli(
            550.0,
            900.0,
            self._at(elevation, motor_start * unit_e, motor_start * unit_n),
            axis=axis,
            label="Side-entry agitator drive motor",
        )

        # Short shaft and propeller reaching inboard from the shell.
        reach = s.diameter * 0.3
        self.b.cyli(
            _AGITATOR_SHAFT_DN,
            reach,
            self._at(elevation, (wall - reach) * unit_e, (wall - reach) * unit_n),
            axis=axis,
            label="Side-entry agitator shaft",
        )
        propeller_dn = s.diameter * 0.2
        hub = wall - reach
        self.b.cyli(
            propeller_dn,
            _IMPELLER_BLADE_MM,
            self._at(elevation, hub * unit_e, hub * unit_n),
            axis=axis,
            label=f"Side-entry agitator propeller, DN{propeller_dn:.0f}",
        )

    def _build_bottom_scraper(self) -> None:
        """
        Bottom-entry discharge scraper for an MC storage tower.

        The drive is below the floor and the sweep arms rotate just above it,
        pushing stock to the outlet. Nothing is mounted on the roof. The drive
        must not extend below the bottom-centre datum: on a ground-bearing tower
        the datum is the foundation, so the drive is carried in a pit whose top
        is at the floor - modelled from the datum upward.
        """
        s = self.spec

        # Drive head at the floor centre. Kept above the datum so the tank's
        # lowest geometry stays the bottom centre point.
        self.b.cyli(
            _SCRAPER_DRIVE_DN,
            _SCRAPER_DRIVE_MM,
            self._at(0.0),
            label="Discharge scraper drive head (at floor centre)",
        )
        hub_base = _SCRAPER_DRIVE_MM
        self.b.cyli(
            _SCRAPER_HUB_DN,
            _SCRAPER_HUB_MM,
            self._at(hub_base),
            label="Discharge scraper hub",
        )

        # Sweep arms reaching most of the way to the wall, just above the floor.
        sweep = s.diameter * _SCRAPER_SWEEP_FRACTION
        arm_length = (sweep - _SCRAPER_HUB_DN) / 2.0
        for axis in ("E", "N", "W", "S"):
            unit_e, unit_n = _AXIS_UNIT[axis]
            start = _SCRAPER_HUB_DN / 2.0
            centre = start + arm_length / 2.0
            self.b.box(
                arm_length if axis in ("E", "W") else _SCRAPER_ARM_MM,
                arm_length if axis in ("N", "S") else _SCRAPER_ARM_MM,
                _SCRAPER_ARM_MM,
                self._at(
                    hub_base + _SCRAPER_ARM_MM / 2.0,
                    centre * unit_e,
                    centre * unit_n,
                ),
                label=f"Discharge scraper sweep arm {axis}",
            )


# ---------------------------------------------------------------------------
# Convenience API
# ---------------------------------------------------------------------------


def build_tank(spec: TankSpec, builder: PMLBuilder) -> None:
    """Emit one tank into an existing builder."""
    TankBuilder(spec, builder).build()


def verify_bottom_centre(spec: TankSpec, script: str) -> List[str]:
    """
    Confirm the macro actually places the tank's bottom centre on the
    installation coordinate.

    This parses the emitted primitives and computes each one's true occupied
    extent from its E3D centre datum, then checks that the lowest point of the
    tank's geometry lands on the listed elevation and is centred on the listed
    plan position.

    An earlier version searched for the coordinate as a literal ``POS`` string.
    That only proved *some* primitive was positioned there - it could not detect
    a wrong datum, because a primitive whose centre sits on the coordinate
    string-matches just as well as one whose base does. It passed a model in
    which every element was half its own height too low.

    Returns one message per discrepancy; an empty list means the tank is
    correctly positioned.
    """
    east, north, up = spec.position
    prims = _parse_primitives(script, spec.tag)
    if not prims:
        return [f"{spec.tag}: no primitives found in the macro"]

    problems: List[str] = []

    lowest = min(p["u_min"] for p in prims)
    if abs(lowest - up) > _TOLERANCE_MM:
        problems.append(
            f"{spec.tag}: lowest geometry sits at U {lowest:.1f} but the "
            f"installation coordinate is U {up:.1f} "
            f"(off by {lowest - up:+.1f} mm) - the bottom centre point does not "
            f"coincide with the equipment list position"
        )

    # Plan position: the shell axis must pass through the listed E/N. Only the
    # shell itself is checked - nozzles, legs and platforms are deliberately
    # offset from the centreline, so including them would be meaningless.
    shell = next(
        (
            p for p in prims
            if p["kind"] == "CYLI"
            and p["axis"] in ("U", "D")
            and abs(p.get("diam", 0.0) - spec.diameter) <= _TOLERANCE_MM
            and abs(p.get("heig", 0.0) - spec.height) <= _TOLERANCE_MM
        ),
        None,
    )
    if shell is None:
        problems.append(
            f"{spec.tag}: no shell primitive found matching DN{spec.diameter:.0f} "
            f"x {spec.height:.0f}"
        )
    elif (
        abs(shell["east"] - east) > _TOLERANCE_MM
        or abs(shell["north"] - north) > _TOLERANCE_MM
    ):
        problems.append(
            f"{spec.tag}: shell centreline at E {shell['east']:.1f} "
            f"N {shell['north']:.1f} but the installation coordinate is "
            f"E {east:.1f} N {north:.1f}"
        )

    return problems


#: Positional tolerance (mm). Coordinates are emitted to 0.1 mm, so anything
#: above rounding is a real error.
_TOLERANCE_MM = 0.2

#: Axis extracted from an ORI line: the primitive extends along its Z axis.
_ORI_RE = re.compile(r"^ORI\s+Z\s+IS\s+([UDENSW])\b", re.IGNORECASE)
_POS_RE = re.compile(
    r"^POS\s+E\s+(-?[\d.]+)\s+N\s+(-?[\d.]+)\s+U\s+(-?[\d.]+)", re.IGNORECASE
)


#: Element types that carry geometry. EQUI and SUBE are grouping elements: they
#: own a position but occupy no space, so they must never be treated as
#: geometry when computing a tank's extent.
_GEOMETRY_KINDS = frozenset({"CYLI", "CONE", "DISH", "BOX"})


def _parse_primitives(script: str, tag: str) -> List[dict]:
    """
    Extract the primitives belonging to one tag, with their true extents.

    Each returned dict carries the primitive's centre and the lowest elevation it
    actually occupies, derived from the E3D centre datum and the primitive's own
    dimensions - which is what makes the check independent of the builder's
    internal bookkeeping.

    Membership follows the tree: everything from a tank's ``NEW EQUI`` up to the
    next one belongs to that tank, which covers the vessel body and every nozzle
    SUBE beneath it.
    """
    prefix = tag.replace("-", "_")
    prims: List[dict] = []
    in_tag = False
    cur: dict = {}

    for raw in script.split("\n"):
        line = raw.strip()
        if line.startswith("NEW EQUI /"):
            # An EQUI opens a new item of equipment and closes the previous one.
            in_tag = line[len("NEW EQUI /"):] == prefix
            cur = {}
            continue
        if not in_tag:
            continue

        if line.startswith("NEW "):
            kind = line[4:].strip().upper()
            # Skip grouping elements: a SUBE's POS would otherwise be read as a
            # zero-sized primitive sitting at the tank's origin.
            cur = {"kind": kind, "axis": "U"} if kind in _GEOMETRY_KINDS else {}
            continue
        if not cur:
            continue

        for attr in ("DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "DTOP", "DBOT"):
            if line.startswith(attr + " "):
                cur[attr.lower()] = float(line.split()[1])

        ori = _ORI_RE.match(line)
        if ori:
            cur["axis"] = ori.group(1).upper()
            continue

        pos = _POS_RE.match(line)
        if pos:
            east, north, up = (float(g) for g in pos.groups())
            cur.update(east=east, north=north, up=up)
            cur["u_min"] = _lowest_point(cur)
            prims.append(cur)
            cur = {}

    return prims


def _lowest_point(prim: dict) -> float:
    """
    The lowest elevation a primitive occupies, given its E3D centre datum.

    For a BOX that is the centre less half its vertical size. For an oriented
    primitive it depends on the axis: one aligned with U extends half its height
    below the centre, while a horizontal one only extends half its diameter.
    """
    up = prim["up"]
    kind = prim["kind"]

    if kind == "BOX":
        return up - prim.get("zlen", 0.0) / 2.0

    height = prim.get("heig", 0.0)
    diameter = max(
        prim.get("diam", 0.0), prim.get("dbot", 0.0), prim.get("dtop", 0.0)
    )
    if prim["axis"] in ("U", "D"):
        return up - height / 2.0
    return up - diameter / 2.0
