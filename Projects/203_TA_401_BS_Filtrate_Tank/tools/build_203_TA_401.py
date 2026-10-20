"""
Generate the AVEVA E3D PML1 macro for 203-TA-401 BS FILTRATE TANK.

    python Projects/203_TA_401_BS_Filtrate_Tank/tools/build_203_TA_401.py

R2 — precision rebuild. R1 approximated three things it did not have to:

* hollow cylinders were arrayed from 20-24 flat BOX facets (up to 15 mm out of
  round);
* the curved separation wall was 32 straight chords;
* the roof rafters were 6 stepped boxes each.

All three are now exact, using element forms taken from this account's own
native E3D export (`Projects/205_TA_059_BLEACH_PLANT_SCRUBBER.pml`):

* `NCYLINDER` / `NBOX` nested inside their parent as a child, which is how that
  export bores a pipe. A shell, a cylinder or a ring is now a real hollow solid;
* `RTORUS` — a rectangular torus, i.e. a curved plate of rectangular section.
  The separation wall is one of them (R 9000.00/9006.35, fitted to 0.002 mm);
* `EXTRUSION` with a parallelogram LOOP for each roof rafter, so a rafter is one
  true sloped member rather than a staircase.

Emission still goes through `wsb.pml_builder.PMLBuilder`, in its END-closed
native form, so the Iron Rules stay structural.

Two forms carry risk that only a load can settle, and both are called out in the
report:

1. `RTORUS` height datum. The native export's platform/toeboard pair is centred
   at E0 N0, where the datum is unobservable. Centre datum is assumed, matching
   every other primitive family (IR-1). `RTORUS_BASE_IS_CENTRE = False` flips
   every ring in one edit if a load shows otherwise.
2. `RTORUS` attribute order. The native export writes POS before ORI, but every
   one of its RTORUS elements sits at E0 N0, where the order cannot be
   distinguished. IR-2's rule for primitives is followed instead (ORI first) —
   the separation wall's arc centre is 10.5 m off axis, so if this is wrong the
   wall will be visibly rotated about the tank axis rather than subtly off.
"""

from __future__ import annotations

import importlib.util
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parent.parent

_spec = importlib.util.spec_from_file_location(
    "wsb_pml_builder", ROOT / "wsb" / "pml_builder.py"
)
_pml = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_pml)

PMLBuilder = _pml.PMLBuilder
PMLValidationError = _pml.PMLValidationError

sys.path.insert(0, str(PROJECT))
import equipment_data as D  # noqa: E402

#: Assumed RTORUS height datum. True = POS is the mid-height (the CYLI/CONE/BOX
#: convention). Set False if a load shows the rings sitting a half-height high.
RTORUS_BASE_IS_CENTRE = True

#: Extra length given to every negative primitive so it cuts cleanly through
#: its parent's end faces, as the native export does (+4 mm).
BORE_OVERCUT = 4.0


# =============================================================================
# Geometry helpers — azimuth is CLOCKWISE from North, matching the drawing
# =============================================================================

def en(radius: float, az_deg: float):
    a = math.radians(az_deg)
    return radius * math.sin(a), radius * math.cos(a)


def bearing(az_deg: float) -> float:
    """E3D plan bearing (measured East towards North) for a drawing azimuth."""
    return (90.0 - az_deg) % 360.0


def bearing_text(az_deg: float) -> str:
    return _pml._plan_direction(bearing(az_deg))


def dir_text(brg: float) -> str:
    """AVEVA direction text for a bearing already in the East->North frame."""
    return _pml._plan_direction(brg % 360.0)


def roof_u(radius: float) -> float:
    return D.ROOF_EAVE_U + (D.SHELL_OD / 2.0 - radius) * math.tan(
        math.radians(D.ROOF_SLOPE_DEG)
    )


class TankBuilder(PMLBuilder):
    """PMLBuilder plus the element forms this vessel needs."""

    # -- nozzles on arbitrary plan bearings ------------------------------
    def _orient_nozzle(self, axis) -> None:
        text = str(axis).strip()
        if " " in text:
            self._lines.append(f"ORI P1 IS {text}")
            return
        super()._orient_nozzle(text)

    # -- a real hollow cylinder: CYLI with a nested NCYLINDER bore -------
    def hollow_cyli(self, od, idia, height, base, *, axis="U", label=""):
        if not 0 < idia < od:
            raise PMLValidationError(
                f"hollow_cyli needs 0 < id ({idia}) < od ({od})")
        if label:
            self.comment(label)
        self._lines.append("NEW CYLI")
        self._lines.append(f"DIAM {_pml._fmt(od)}")
        self._lines.append(f"HEIG {_pml._fmt(height)}")
        self._orient(axis)
        self._position(base, axis=axis, extent=height)
        self._lines.append("NEW NCYLINDER")
        self._lines.append(f"DIAM {_pml._fmt(idia)}")
        self._lines.append(f"HEIG {_pml._fmt(height + BORE_OVERCUT)}")
        self._lines.append("END")
        self._lines.append("END")
        self._lines.append("")
        self.primitive_count += 1
        return self

    # -- a real hollow box: BOX with a nested NBOX void ------------------
    def hollow_box(self, xlen, ylen, zlen, wall, centre, *, plan_rotation_deg=0.0,
                   open_top=False, label=""):
        if label:
            self.comment(label)
        self._lines.append("NEW BOX")
        self._lines.append(f"XLEN {_pml._fmt(xlen)}")
        self._lines.append(f"YLEN {_pml._fmt(ylen)}")
        self._lines.append(f"ZLEN {_pml._fmt(zlen)}")
        rot = plan_rotation_deg % 360.0
        if abs(rot) > 1e-9:
            self._lines.append(f"ORI Z IS U AND X IS {dir_text(rot)}")
        self._position(centre)
        self._lines.append("NEW NBOX")
        self._lines.append(f"XLEN {_pml._fmt(xlen - 2 * wall)}")
        self._lines.append(f"YLEN {_pml._fmt(ylen - 2 * wall)}")
        self._lines.append(f"ZLEN {_pml._fmt(zlen - 2 * wall)}")
        self._lines.append("END")
        self._lines.append("END")
        self._lines.append("")
        self.primitive_count += 1
        return self

    # -- rectangular torus: a curved plate, or at 360 deg a hollow cylinder
    def rtorus(self, rins, rout, heig, centre_en, base_u, start_bearing,
               angle_deg, *, label=""):
        """
        Curved rectangular-section plate about a vertical axis.

        The sector sweeps `angle_deg` counter-clockwise from local +X, which is
        how the native export's four 90-degree quadrants tile a full ring
        (`TOEBOARD_1..4`, each with a different local Y and no ANGL).
        """
        if not 0 < rins < rout:
            raise PMLValidationError(
                f"RTORUS needs 0 < rins ({rins}) < rout ({rout})")
        if heig <= 0 or not 0 < angle_deg <= 360:
            raise PMLValidationError(
                f"RTORUS needs a positive height and 0 < angle <= 360, "
                f"got heig={heig}, angle={angle_deg}")
        if label:
            self.comment(label)
        self._lines.append("NEW RTORUS")
        # Two decimals, not _fmt()'s one: at 1 d.p. the wall's 6.35 mm plate
        # is emitted as 9006.4 - 9000.0 = 6.4 mm.
        self._lines.append(f"RINS {rins:.2f}")
        self._lines.append(f"ROUT {rout:.2f}")
        self._lines.append(f"HEIG {_pml._fmt(heig)}")
        # NOT _fmt(): that is 1 decimal place, which is right for millimetres
        # and far too coarse for an angle. On this vessel's 9 m separation-wall
        # arc, 0.1 deg is 15.7 mm of arc length. Six decimals keeps the sector
        # ends inside a hundredth of a millimetre.
        self._lines.append(f"ANGL {angle_deg:.6f}degree")
        self._lines.append(f"ORI Z IS U AND X IS {dir_text(start_bearing)}")
        u = base_u + (heig / 2.0 if RTORUS_BASE_IS_CENTRE else 0.0)
        self._lines.append(
            f"POS E {_pml._fmt(centre_en[0])} N {_pml._fmt(centre_en[1])} "
            f"U {_pml._fmt(u)}")
        self._lines.append("END")
        self._lines.append("")
        self.primitive_count += 1
        return self

    def ring(self, od, idia, heig, base_u, centre_en=(0.0, 0.0), *, label=""):
        """A full 360-degree ring, as four RTORUS quadrants (the native idiom)."""
        for k in range(4):
            self.rtorus(idia / 2.0, od / 2.0, heig, centre_en, base_u,
                        k * 90.0, 90.0, label=label if k == 0 else "")
        return self


# =============================================================================
# Build
# =============================================================================

def build() -> str:
    b = TankBuilder(D.ELEMENT, close_elements=True)
    b.header(
        f"{D.TAG}  {D.NAME}",
        meta=[
            ("Source", D.DRAWING),
            ("Revision", "R2 - precision rebuild: true solids, exact arc, true rafters"),
            ("Datum", "bottom centre of the tank at E 0 N 0 U 0"),
            ("Azimuth", "drawing 0 deg modelled as North, clockwise positive"),
            ("Note", "drawing orientation - rotate the EQUI 180 deg about U for site"),
            ("Units", "millimetres"),
        ],
    )
    b.equi(
        D.ELEMENT,
        position=(0.0, 0.0, 0.0),
        attributes=[
            f"DESC '{D.TAG} {D.NAME} | ID{int(D.SHELL_ID)} H{int(D.SHELL_TOP)} "
            f"| ANDRITZ 900135359 + DWG nozzle modification | R2'",
        ],
    )
    _shell(b)
    _internals(b)
    _nozzles(b)
    _overflow(b)
    _furniture(b)
    b.footer()
    return b.build()


# -- shell, bottom, roof ------------------------------------------------------

def _shell(b: TankBuilder) -> None:
    b.banner("SHELL / BOTTOM / ROOF")
    b.sube(f"{D.ELEMENT}_SHELL")

    b.cyli(D.BOTTOM_PLATE_OD, D.BOTTOM_PLATE_T, (0.0, 0.0, 0.0),
           label="Flat bottom plate, 60 mm proud of the shell (measured R3066.8)")

    b.hollow_cyli(
        D.SHELL_OD, D.SHELL_ID, D.SHELL_PLATE_TOP, (0.0, 0.0, 0.0),
        label=f"Shell ID {D.SHELL_ID:.0f} x {D.SHELL_T} wall - a true hollow "
              f"solid, so the internals read without hiding anything")

    for u in D.STIFFENER_ELEVATIONS:
        b.hollow_cyli(
            D.STIFFENER_OD, D.SHELL_OD, D.STIFFENER_T,
            (0.0, 0.0, u - D.STIFFENER_T / 2.0),
            label=f"Shell stiffening ring at U {u:.0f}, 100 x 9.5 flat "
                  f"(measured 6211.4 over the shell) - a real ring, not a disc")

    cone_h = D.ROOF_CONE_TOP_U - D.ROOF_EAVE_U
    b.cone(D.SHELL_OD, D.ROOF_COLLAR_OD, cone_h, (0.0, 0.0, D.ROOF_EAVE_U),
           label=f"Conical roof plate, {D.ROOF_SLOPE_DEG} deg "
                 f"(measured 11.98 deg over 2333 mm of run)")
    b.hollow_cyli(
        D.ROOF_COLLAR_OD, D.ROOF_COLLAR_OD - 2 * D.SHELL_T,
        D.ROOF_COLLAR_TOP_U - D.ROOF_CONE_TOP_U, (0.0, 0.0, D.ROOF_CONE_TOP_U),
        label="Roof centre collar (measured R652.73 / R646.37)")
    b.cyli(D.ROOF_COLLAR_OD, D.ROOF_DECK_T, (0.0, 0.0, D.ROOF_COLLAR_TOP_U),
           label="Roof centre deck plate - N8 rises from here")

    # Eight radial rafters lying on the roof plate. Each is ONE extrusion whose
    # LOOP is the rafter's true longitudinal section: a parallelogram following
    # the 12 deg slope with vertical ends, exactly as the elevation draws it.
    # Local X is radial and local Y is Up, so the profile coordinates are
    # (radius, elevation) directly.
    for k in range(D.RAFTER_COUNT):
        az = k * 360.0 / D.RAFTER_COUNT
        tang = bearing(az) - 90.0                 # local Z, horizontal tangent
        ox, oy = en(1.0, az)                      # unit radial, for nothing but clarity
        t = math.radians(tang)
        start = (-D.RAFTER_WIDTH / 2.0 * math.cos(t),
                 -D.RAFTER_WIDTH / 2.0 * math.sin(t), 0.0)
        b.extrusion(
            start,
            f"Y IS U AND Z IS {dir_text(tang)}",
            D.RAFTER_WIDTH,
            [(D.RAFTER_R_IN, roof_u(D.RAFTER_R_IN)),
             (D.RAFTER_R_OUT, roof_u(D.RAFTER_R_OUT)),
             (D.RAFTER_R_OUT, roof_u(D.RAFTER_R_OUT) + D.RAFTER_DEPTH),
             (D.RAFTER_R_IN, roof_u(D.RAFTER_R_IN) + D.RAFTER_DEPTH)],
            label=(f"Roof rafters, {D.RAFTER_COUNT} off at 45 deg centres, "
                   f"{D.RAFTER_WIDTH:.0f} wide x {D.RAFTER_DEPTH:.0f} deep, "
                   f"R{D.RAFTER_R_IN:.0f} to R{D.RAFTER_R_OUT:.0f} on the 12 deg "
                   f"slope") if k == 0 else f"rafter at az {az:.0f}")


# -- internals ----------------------------------------------------------------

def _internals(b: TankBuilder) -> None:
    b.banner("INTERNALS - air separation cylinders, separation wall, soap launder")
    b.sube(f"{D.ELEMENT}_INTERNALS")
    centre = (D.CYL_OFFSET_E, D.CYL_OFFSET_N)

    b.hollow_cyli(
        D.OUTER_CYL_BASE_RING_OD, D.OUTER_CYL_OD, D.OUTER_CYL_BASE_RING_T,
        (centre[0], centre[1], 0.0),
        label="Outer air-separation cylinder base ring (measured R1186.34)")
    b.hollow_cyli(
        D.OUTER_CYL_OD, D.OUTER_CYL_ID, D.OUTER_CYL_TOP, (centre[0], centre[1], 0.0),
        label=f"Outer air-separation cylinder ID {D.OUTER_CYL_ID:.1f} to U "
              f"{D.OUTER_CYL_TOP:.0f}; axis offset E {D.CYL_OFFSET_E:.1f} from the tank")
    b.hollow_cyli(
        D.INNER_CYL_OD, D.INNER_CYL_ID, D.INNER_CYL_TOP, (centre[0], centre[1], 0.0),
        label=f"Inner air-separation (seal) cylinder ID {D.INNER_CYL_ID:.1f} to "
              f"U {D.INNER_CYL_TOP:.0f}")

    r_in = D.INNER_CYL_OD / 2.0
    r_out = D.OUTER_CYL_ID / 2.0
    for j, az in enumerate(D.RIB_AZIMUTHS):
        e, n = en((r_in + r_out) / 2.0, az)
        b.box(r_out - r_in, D.RIB_T, D.OUTER_CYL_TOP,
              (centre[0] + e, centre[1] + n, D.OUTER_CYL_TOP / 2.0),
              plan_rotation_deg=bearing(az),
              label="Radial rib between the air-separation cylinders, 4 off "
                    "(measured at 90 deg centres about the cylinder axis)"
              if j == 0 else "")

    # The separation wall is a TRUE CIRCULAR ARC. Both drawn faces fit a common
    # centre to 0.002 mm, giving R 9000.00 inside / 9006.35 outside - the same
    # 6.35 plate as the shell - about a centre 10502.3 mm from the tank axis at
    # az 105.00 (110.00 before the overlay rotated it 5 deg CCW with N1.2).
    ce, cn = D.SEP_WALL_ARC_E, D.SEP_WALL_ARC_N
    # Derive the sector so BOTH ends meet the shell bore exactly. With the arc
    # centre a distance d off the tank axis and the plate's mid-thickness
    # radius R, the half-angle subtended at the arc centre by the shell bore is
    # acos((d^2 + R^2 - r_shell^2) / 2dR), measured either side of the
    # centre-to-tank-axis direction.
    d = math.hypot(ce, cn)
    R = (D.SEP_WALL_RINS + D.SEP_WALL_ROUT) / 2.0
    # Terminate on the shell plate's MID-THICKNESS, not its bore: the wall is
    # welded into the plate, and the drawn polyline overruns the bore by about
    # 1.5 mm at each end for exactly that reason. Ending on the bore leaves the
    # wall merely touching the shell.
    r_weld = (D.SHELL_ID / 2.0 + D.SHELL_OD / 2.0) / 2.0
    half = math.degrees(math.acos(
        (d * d + R * R - r_weld * r_weld) / (2.0 * d * R)))
    to_axis = math.degrees(math.atan2(-cn, -ce)) % 360.0
    start_brg, span = to_axis - half, 2.0 * half
    b.rtorus(
        D.SEP_WALL_RINS, D.SEP_WALL_ROUT, D.SEP_WALL_TOP, (ce, cn), 0.0,
        start_brg, span,
        label=f"Curved separation wall to U {D.SEP_WALL_TOP:.0f} - one RTORUS, "
              f"R{D.SEP_WALL_RINS:.2f}/{D.SEP_WALL_ROUT:.2f} about a centre "
              f"{d:.1f} from the tank axis; sector {span:.3f} deg from bearing "
              f"{start_brg:.3f}, both ends derived onto the shell bore")

    # Soap launder: a true annular sector against the shell bore.
    b0 = bearing(D.LAUNDER_AZ_END)                # sweep CCW towards az_start
    span = (D.LAUNDER_AZ_END - D.LAUNDER_AZ_START) % 360.0
    wall_h = D.LAUNDER_RIM_U - D.LAUNDER_FLOOR_U
    b.rtorus(D.LAUNDER_R_IN, D.LAUNDER_R_OUT, D.LAUNDER_PLATE_T, (0.0, 0.0),
             D.LAUNDER_FLOOR_U, b0, span,
             label=f"Soap launder floor, R{D.LAUNDER_R_IN:.0f}-"
                   f"{D.LAUNDER_R_OUT:.0f}, az {D.LAUNDER_AZ_START}-"
                   f"{D.LAUNDER_AZ_END} (chord at R2400 = the dimensioned 2921)")
    b.rtorus(D.LAUNDER_R_IN - D.LAUNDER_PLATE_T, D.LAUNDER_R_IN, wall_h,
             (0.0, 0.0), D.LAUNDER_FLOOR_U, b0, span,
             label="Soap launder inner wall")
    for j, az in enumerate((D.LAUNDER_AZ_START,) + D.LAUNDER_DIVIDER_AZ
                           + (D.LAUNDER_AZ_END,)):
        e, n = en((D.LAUNDER_R_IN + D.LAUNDER_R_OUT) / 2.0, az)
        b.box(D.LAUNDER_R_OUT - D.LAUNDER_R_IN, D.LAUNDER_PLATE_T, wall_h,
              (e, n, D.LAUNDER_FLOOR_U + wall_h / 2.0),
              plan_rotation_deg=bearing(az),
              label="Soap launder radial dividers and end plates (measured)"
              if j == 0 else "")


# -- nozzles ------------------------------------------------------------------

def _nozzles(b: TankBuilder) -> None:
    b.banner("NOZZLES - one SUBE each (IR-8)")
    shell_face = D.SHELL_OD / 2.0

    for mark, dn, u, az_orig, az, face_r, service in D.NOZZLES:
        sube = f"{D.ELEMENT}_{mark.replace('.', '_')}"
        b.sube(sube)
        moved = "" if abs(az - az_orig) < 1e-6 else \
            f" | MODIFIED: az {az_orig:.1f} -> {az:.1f}"

        if mark == "N1.1":
            pe, pn = en(shell_face, D.N1_1_PIERCE_AZ)
            a = math.radians(D.N1_1_AXIS_AZ)
            fe = pe + D.N1_1_PROJECTION * math.sin(a)
            fn = pn + D.N1_1_PROJECTION * math.cos(a)
            b.nozzle(f"{sube}_NOZZ", dn, D.N1_1_PROJECTION, (fe, fn, u),
                     axis=bearing_text(D.N1_1_AXIS_AZ),
                     label=f"{mark} DN{dn} U{u:.0f} - {service}; CHORD entry: "
                           f"pierces the shell at az {D.N1_1_PIERCE_AZ}, bore "
                           f"axis az {D.N1_1_AXIS_AZ} (walls measured 325.7 "
                           f"apart on a line 96.2 off the tank axis)")
            continue

        if mark == "N8":
            heig = u - D.ROOF_COLLAR_TOP_U
            b.nozzle(f"{sube}_NOZZ", dn, heig, (0.0, 0.0, u), axis="U",
                     label=f"{mark} DN{dn} - {service}; neck rises from the roof "
                           f"deck at U {D.ROOF_COLLAR_TOP_U}, flange face U {u} "
                           f"(both measured)")
            continue

        if mark in ("N9", "N12"):
            e, n = en(face_r, az)
            heig = D.N9_LENGTH if mark == "N9" else D.N12_LENGTH
            b.nozzle(f"{sube}_NOZZ", dn, heig, (e, n, u), axis="D",
                     label=f"{mark} DN{dn} U{u:.0f} az {az} - {service}{moved}")
            continue

        if mark in ("N11", "N13"):
            e, n = en(face_r, az)
            heig = D.N11_LENGTH if mark == "N11" else D.N13_LENGTH
            b.nozzle(f"{sube}_NOZZ", dn, heig, (e, n, u), axis="U",
                     label=f"{mark} DN{dn} U{u:.0f} az {az} - {service}{moved}")
            continue

        e, n = en(face_r, az)
        heig = face_r - shell_face
        b.nozzle(f"{sube}_NOZZ", dn, heig, (e, n, u), axis=bearing_text(az),
                 label=f"{mark} DN{dn} U{u:.0f} az {az} - {service}{moved}; "
                       f"flange face R{face_r:.1f}, projection {heig:.1f}")

        # N5 is a PAD FLANGE: the drawing shows a pad on the shell, measured
        # 200 wide from r 3006.35 out to r 3051.8 before the flange proper.
        if mark == "N5":
            pe, pn = en((shell_face + D.N5_PAD_R_OUT) / 2.0, az)
            b.box(D.N5_PAD_R_OUT - shell_face, D.N5_PAD_W, D.N5_PAD_W,
                  (pe, pn, u), plan_rotation_deg=bearing(az),
                  label="N5 reinforcing pad (PN40 pad flange, measured to R3051.8)")


# -- overflow seal box --------------------------------------------------------

def _overflow(b: TankBuilder) -> None:
    b.banner("N9 OVERFLOW WATER-SEAL BOX (E-E 1:15)")
    b.sube(f"{D.ELEMENT}_OVERFLOW")

    r_box = D.SHELL_OD / 2.0 + D.OVF_BOX_RADIAL / 2.0
    e, n = en(r_box, D.OVF_AZ)
    b.hollow_box(
        D.OVF_BOX_RADIAL, D.OVF_BOX_TANGENTIAL, D.OVF_HEIGHT, D.OVF_PLATE_T,
        (e, n, D.OVF_BOTTOM_U + D.OVF_HEIGHT / 2.0),
        plan_rotation_deg=bearing(D.OVF_AZ),
        label=f"Overflow seal box, {D.OVF_PLATE_T} plate, U {D.OVF_BOTTOM_U:.0f}"
              f"-{D.OVF_TOP_U:.0f} (E-E total 1361); opening to the shell 250 "
              f"high at U {D.OVF_OPENING_BASE_U:.0f}")
    e, n = en(D.OVF_PIPE_R, D.OVF_AZ)
    b.hollow_cyli(
        D.OVF_PIPE_OD, D.OVF_PIPE_OD - 2 * D.OVF_PLATE_T, D.OVF_HEIGHT,
        (e, n, D.OVF_BOTTOM_U),
        label=f"Overflow downcomer {D.OVF_PIPE_OD} x {D.OVF_PLATE_T} at "
              f"R{D.OVF_PIPE_R} (view A '3542'), az {D.OVF_AZ}")


# -- hatch, nameplate, grounding lugs, anchoring ------------------------------

def _furniture(b: TankBuilder) -> None:
    b.banner("ACCESS / EARTHING / ANCHORING")
    b.sube(f"{D.ELEMENT}_ACCESS")

    e, n = en(D.IH_R, D.IH_AZ)
    b.hollow_cyli(D.IH_CURB_OD, D.IH_OPENING_D, D.IH_CURB_H, (e, n, D.IH_CURB_U),
                  label=f"Inspection hatch IH: ID{D.IH_OPENING_D:.0f} opening "
                        f"through a {D.IH_CURB_OD:.0f} curb at R{D.IH_R} az "
                        f"{D.IH_AZ} (roof plate U {roof_u(D.IH_R):.0f}); curb "
                        f"measured U 8189..8284")
    b.cyli(D.IH_COVER_OD, D.IH_COVER_T, (e, n, D.IH_COVER_U),
           label="Inspection hatch hinged quick-lock cover with safety grating")

    e, n = en(D.NP_R, D.NP_AZ)
    b.box(D.NP_T, D.NP_W, D.NP_H, (e, n, D.NP_U), plan_rotation_deg=bearing(D.NP_AZ),
          label=f"Tank nameplate NP at U {D.NP_U:.0f} az {D.NP_AZ} "
                f"(measured az 287.9..292.1 at R3144)")

    b.sube(f"{D.ELEMENT}_EARTHING")
    for j, az in enumerate(D.GL_AZIMUTHS):
        r = D.SHELL_OD / 2.0 + D.GL_PROJECTION / 2.0
        e, n = en(r, az)
        b.box(D.GL_PROJECTION, D.GL_W, D.GL_T, (e, n, D.GL_U),
              plan_rotation_deg=bearing(az),
              label=f"Grounding lugs GL, 4 off at az "
                    f"{'/'.join(str(a) for a in D.GL_AZIMUTHS)} "
                    f"(measured in views A and C-C, projecting to R3156)"
              if j == 0 else "")

    b.sube(f"{D.ELEMENT}_SUPPORT")
    shell_face = D.SHELL_OD / 2.0
    for j, az in enumerate(D.ANCHOR_AZIMUTHS):
        e, n = en(shell_face + D.ANCHOR_PROJECTION / 2.0, az)
        b.box(D.ANCHOR_PROJECTION, D.ANCHOR_PAD_W, D.ANCHOR_PAD_H,
              (e, n, D.ANCHOR_PAD_U + D.ANCHOR_PAD_H / 2.0),
              plan_rotation_deg=bearing(az),
              label=f"Anchor shell pads, 6 off at az "
                    f"{'/'.join(str(a) for a in D.ANCHOR_AZIMUTHS)} (measured)"
              if j == 0 else "")

        r_strap = shell_face + D.ANCHOR_PROJECTION - D.ANCHOR_STRAP_T / 2.0
        e, n = en(r_strap, az)
        h = D.ANCHOR_PAD_U + D.ANCHOR_PAD_H
        b.box(D.ANCHOR_STRAP_T, D.ANCHOR_STRAP_W, h, (e, n, h / 2.0),
              plan_rotation_deg=bearing(az),
              label="Holding-down strap down to the anchor plate" if j == 0 else "")
        b.box(D.ANCHOR_PLATE, D.ANCHOR_PLATE, D.ANCHOR_PLATE_T,
              (e, n, D.ANCHOR_PLATE_T / 2.0), plan_rotation_deg=bearing(az),
              label="Anchor plate 200x200x10 embedded in the foundation base "
                    "(DWG FOUNDATION note: total 12 pieces)" if j == 0 else "")


if __name__ == "__main__":
    out = PROJECT / "output" / "203_TA_401_BS_Filtrate_Tank.pml"
    out.parent.mkdir(parents=True, exist_ok=True)
    script = build()
    out.write_text(script, encoding="utf-8")
    print(f"written {out}  ({len(script.splitlines())} lines)")
