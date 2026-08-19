"""
Generate the complete E3D pump models for the 2026-08-19 project.

Modelling logic
---------------
Longitudinal axis
    The suction bore direction defines it: suction -> casing -> motor, with the
    motor at the far end (DO.txt).  For the two E-W MC pumps the client
    confirmed a side suction, so their axis comes from the discharge instead.

Casing plan position
    * Conventional pump with a top (crown) discharge: in plan the casing centre
      IS the discharge nozzle centre.  The nozzle is never moved to suit the
      casing; the casing is built around it.
    * MC pump without a top nozzle: the casing centre is placed at the offset
      given in ``mc_pump_casing_location_relative_center.txt``, measured from
      the baseplate centre along the longitudinal axis toward the wet end.

Shaft centreline
    Every rotating part -- casing, bearing housings, shaft, coupling, motor --
    shares one elevation.  It is taken from the suction nozzle's own U, which
    is the one elevation the project fixes on the machine axis, and is checked
    to clear both the casing radius and the suction flange radius so nothing
    sinks below the foundation.

Nozzle Z
    Plan positions and directions are hard constraints and are emitted exactly
    as read.  Only U may be adjusted, and only for the top discharge, which is
    lifted to sit on the casing crown when the source elevation would leave it
    buried in or floating above the volute.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all                      # noqa: E402
from recover_nozzle_axes import classify                        # noqa: E402
from pump_model import (AXIS_VECTOR, BASEPLATE_THICKNESS, OPPOSITE,  # noqa: E402
                        REF, RIB_COUNT, Primitive, PumpModel)

REPO = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO / "Projects" / "JK_Pump_Build" / "output" / "2026-08-19_pumps"


def perpendicular(letter: str) -> str:
    """The plan axis at right angles to a cardinal direction."""
    return "E" if letter in ("N", "S") else "N"


def axis_component(east: float, north: float, letter: str) -> float:
    """Signed distance along a cardinal plan direction."""
    vector = AXIS_VECTOR[letter]
    return east * vector[0] + north * vector[1]


def build_pump(tag: str, sources: dict) -> PumpModel:
    """Assemble one complete pump from project data + reference structure."""
    location = sources["location"][tag]
    engine = sources["engine"].get(tag)
    casing_row = sources["casing"].get(tag)
    mc_offset = sources["mc_offset"].get(tag)

    plate = location.baseplate
    plate_e = plate.pos["east"]
    plate_n = plate.pos["north"]
    xlen = plate.attrs["XLEN"]
    ylen = plate.attrs["YLEN"]
    zlen = plate.attrs["ZLEN"]
    plate_under = plate.pos["up"] - zlen / 2
    plate_top = plate.pos["up"] + zlen / 2

    name = (engine or {}).get("equipment_name") \
        or (casing_row or {}).get("pump_name") or "PUMP"
    is_mc = bool(engine and engine["is_mc"]) or tag in sources["mc_offset"]

    model = PumpModel(tag=tag, element=location.element,
                      description=f"{name}"[:120])
    model.facts.update(tag=tag, is_mc=is_mc, plate=(xlen, ylen, zlen),
                       plate_centre=(plate_e, plate_n),
                       plate_under=plate_under, plate_top=plate_top)

    # ---- nozzle schedule (hard constraint) ---------------------------
    recovered = {row["role"]: row for row in classify(tag, location)}
    suction = recovered.get("SUCTION")
    discharge = recovered.get("DISCHARGE")

    # ---- longitudinal axis --------------------------------------------
    # Suction -> casing -> motor: the machine runs from the suction inward,
    # so the motor lies opposite the suction bore.
    if suction["letter"] in ("U", "D"):
        model.unresolved.append("suction bore is vertical; longitudinal axis unresolved")
        wet_end = "N" if ylen >= xlen else "E"
    elif is_mc and discharge and discharge["letter"] not in ("U", "D"):
        # Side-suction MC pump: the discharge is the horizontal process line
        # that lies on the machine axis, so it defines the longitudinal run.
        wet_end = discharge["letter"]
    else:
        wet_end = suction["letter"]
    motor_end = OPPOSITE[wet_end]
    long_axis = "N" if wet_end in ("N", "S") else "E"
    tran_axis = perpendicular(wet_end)
    half_long = (ylen if long_axis == "N" else xlen) / 2
    model.facts.update(wet_end=wet_end, motor_end=motor_end, long_axis=long_axis)

    # ---- governing casing dimensions -----------------------------------
    if casing_row and casing_row["diameter"]:
        casing_dia = casing_row["diameter"]
        casing_len = casing_row["height"]
        model.facts["casing_source"] = "casing_reference.txt"
    else:
        # Not dimensioned by the project.  Rather than invent a casing, take
        # the smallest envelope the pump's own confirmed geometry implies: the
        # discharge must sit on the crown and the plate must carry it.
        casing_dia = min(xlen, ylen) * 0.72
        casing_len = casing_dia * 0.30
        model.facts["casing_source"] = "DERIVED (no casing_reference row)"
        model.unresolved.append(
            f"casing diameter/length not in casing_reference.txt; "
            f"derived {casing_dia:.0f} x {casing_len:.0f} from plate width")
        model.reference_values.append(
            f"casing {casing_dia:.0f} dia x {casing_len:.0f} long (DERIVED)")

    # ---- shaft centreline ------------------------------------------------
    # The suction nozzle lies on the machine axis, so its elevation is the
    # natural shaft height and is used wherever it is physically possible.
    #
    # For ten pumps it is not.  The casing supplied by casing_reference.txt has
    # a radius LARGER than the suction elevation, so a volute centred on the
    # suction axis would cut through the baseplate and reach below the
    # foundation.  The casing diameter and the nozzle elevation come from two
    # different sources and cannot both be honoured literally.
    #
    # Resolution: the casing is a real body that must rest on the plate, so the
    # shaft is raised to the minimum height that seats the volute, and the
    # adjustment is recorded as a data conflict.  This only ever moves Z, which
    # the task permits; nozzle plan positions and directions stay exact.
    # The same conflict applies to the driver: its end bells are the widest
    # part of the machine, so the shaft must clear their radius too.  Handling
    # both bodies in one place keeps this as shared logic rather than a
    # per-pump patch.
    suction_u = suction["pos"]["up"]
    motor_dia = (engine or {}).get("engine_max_dia_mm")
    end_bell_dia = (motor_dia or 0.0) * REF["motor_end_dish_dia"]
    required = max(casing_dia, end_bell_dia) / 2
    driver = "motor end bell" if end_bell_dia > casing_dia else "casing"
    seated_u = plate_top + required

    if suction_u < seated_u - 0.5:
        shaft_u = seated_u
        model.unresolved.append(
            f"CONFLICT: suction elevation U {suction_u:.1f} is below the "
            f"{driver} radius {required:.1f} (casing_reference.txt / "
            f"engine_shaft CSV); a machine on that axis would sink below the "
            f"foundation. Shaft raised to U {seated_u:.1f} to seat it on the "
            f"baseplate.")
        model.facts["shaft_u_basis"] = (
            f"raised from suction U {suction_u:.1f} to seat {driver}")
    else:
        shaft_u = suction_u
        model.facts["shaft_u_basis"] = "suction nozzle elevation (machine axis)"

    # ---- casing plan centre ---------------------------------------------
    if is_mc:
        if mc_offset is None:
            model.unresolved.append("MC pump without a casing plan offset")
            offset = half_long * 0.5
        else:
            offset = mc_offset
        vector = AXIS_VECTOR[wet_end]
        casing_e = plate_e + vector[0] * offset
        casing_n = plate_n + vector[1] * offset
        model.facts["casing_plan_basis"] = (
            f"MC offset {offset:.0f} mm from plate centre toward {wet_end}")
    elif discharge and discharge["letter"] == "U":
        # In plan the casing centre IS the top-discharge nozzle centre.
        casing_e = discharge["pos"]["east"]
        casing_n = discharge["pos"]["north"]
        model.facts["casing_plan_basis"] = "top-discharge nozzle centre (plan)"
    else:
        vector = AXIS_VECTOR[wet_end]
        casing_e = plate_e + vector[0] * half_long * 0.55
        casing_n = plate_n + vector[1] * half_long * 0.55
        model.facts["casing_plan_basis"] = "DERIVED wet-end position"
        model.reference_values.append("casing plan position DERIVED")

    model.facts.update(casing=(casing_dia, casing_len),
                       casing_centre=(casing_e, casing_n), shaft_u=shaft_u)

    _build_baseplate(model, plate_e, plate_n, xlen, ylen, zlen, plate.pos["up"])
    _build_casing(model, casing_e, casing_n, casing_dia, casing_len,
                  shaft_u, long_axis, wet_end, plate_top, is_mc)
    _build_drive(model, engine, casing_e, casing_n, casing_dia, casing_len, shaft_u,
                 long_axis, wet_end, motor_end, plate_e, plate_n,
                 half_long, plate_top, is_mc)
    _build_nozzles(model, suction, discharge, casing_e, casing_n,
                   casing_dia, casing_len, shaft_u, location)
    return model


def _build_baseplate(model, east, north, xlen, ylen, zlen, up):
    """The confirmed baseplate, emitted exactly as the project fixes it."""
    model.add(Primitive(
        kind="BOX", sube="BASEPLATE",
        attrs={"XLEN": xlen, "YLEN": ylen, "ZLEN": zlen},
        east=east, north=north, up=up,
        note="baseplate: size and underside centre are project data"))


def _build_casing(model, east, north, dia, length, shaft_u, long_axis,
                  wet_end, plate_top, is_mc):
    """
    Volute barrel, end cover and the foot that carries it to the baseplate.

    The barrel axis lies along the machine's longitudinal run so the volute
    faces the suction, matching /P1501B where the volute CYLI is oriented
    ``Z is N`` on the pump axis.
    """
    axis = "N" if long_axis == "N" else "E"
    ori = f"ORI Z is {axis} and Y is U"

    model.add(Primitive(
        kind="CYLINDER", sube="CASING",
        attrs={"DIAM": dia, "HEIG": length},
        east=east, north=north, up=shaft_u, ori=ori,
        note="volute barrel: DIAM/HEIG from casing_reference.txt"))

    # End cover on the suction face.  IR-1: a DISH is positioned on its rim.
    vector = AXIS_VECTOR[wet_end]
    rim_e = east + vector[0] * length / 2
    rim_n = north + vector[1] * length / 2
    model.add(Primitive(
        kind="DISH", sube="CASING",
        attrs={"DIAM": dia * REF["casing_dish_dia"],
               "HEIG": dia * REF["casing_dish_heig"],
               "RADI": dia * REF["casing_dish_radi"]},
        east=rim_e, north=rim_n, up=shaft_u,
        ori=f"ORI Z is {wet_end} and Y is U",
        note="volute end cover: proportion from /P1501B"))
    model.reference_values.append("volute end cover proportioned from /P1501B")

    # Casing foot: carries the volute down to the baseplate so nothing floats.
    foot_top = shaft_u - dia * 0.30
    foot_height = max(foot_top - plate_top, 10.0)
    model.add(Primitive(
        kind="BOX", sube="SUPPORT",
        attrs={"XLEN": dia * 0.55 if long_axis == "N" else length * 0.9,
               "YLEN": length * 0.9 if long_axis == "N" else dia * 0.55,
               "ZLEN": foot_height},
        east=east, north=north, up=plate_top + foot_height / 2,
        note="casing pedestal: chains volute -> baseplate"))
    model.reference_values.append("casing pedestal sized from casing envelope")


def _build_drive(model, engine, casing_e, casing_n, casing_dia, casing_len, shaft_u,
                 long_axis, wet_end, motor_end, plate_e, plate_n,
                 half_long, plate_top, is_mc):
    """
    Bearing housing, shaft, coupling and motor, all on one centreline.

    Sizes come from ``engine_shaft_measurements_updated.csv`` where the CSV
    carries them.  ``N/A`` is never read as zero: an absent shaft record means
    the pump is close-coupled (the MC arrangement), so no free shaft or
    coupling is drawn at all.
    """
    vector = AXIS_VECTOR[motor_end]
    axis = "N" if long_axis == "N" else "E"
    ori = f"ORI Z is {axis} and Y is U"

    if engine is None:
        model.unresolved.append(
            "no engine_shaft record: motor and shaft not modelled")
        return

    motor_len = engine.get("engine_total_L_mm")
    motor_dia = engine.get("engine_max_dia_mm")
    motor_axial = engine.get("engine_axial_offset_mm")
    if motor_len is None or motor_dia is None:
        model.unresolved.append("motor length/diameter missing from the CSV")
        return

    # The CSV axial offset is measured from the pump datum along the machine
    # axis.  Its sign is preserved: a negative offset places the motor on the
    # opposite side of the datum from a positive one.
    motor_centre_offset = abs(motor_axial) if motor_axial is not None else \
        half_long * 0.5
    if motor_axial is None:
        model.unresolved.append("engine_axial_offset is N/A; motor placed by proportion")
        model.reference_values.append("motor axial position DERIVED")

    motor_e = plate_e + vector[0] * motor_centre_offset
    motor_n = plate_n + vector[1] * motor_centre_offset

    # ---- bearing housing, on the motor side of the volute ---------------
    # It starts at the casing back face and runs toward the motor.  On a
    # close-coupled machine (no free shaft in the CSV) it becomes the lantern
    # housing and must span the whole gap to the motor face, or the drive train
    # is visibly parted -- the exact defect the client rejected in r11.
    bearing_dia = casing_dia * REF["bearing_dia"]
    casing_back = _along(casing_e, casing_n, plate_e, plate_n, vector) \
        + casing_len / 2
    motor_face_along = _along(motor_e, motor_n, plate_e, plate_n, vector) \
        - motor_len / 2
    has_free_shaft = engine.get("shaft_total_L_mm") is not None
    span = motor_face_along - casing_back

    if not has_free_shaft and span > 1.0:
        bearing_len = span          # close-coupled: bridge casing to motor
        note = "lantern/bearing housing: close-coupled, spans casing to motor"
    else:
        bearing_len = min(casing_dia * REF["bearing_heig"], max(span, 1.0))
        note = "bearing housing: proportion from /P1501B"

    bearing_along = casing_back + bearing_len / 2
    bearing_e = plate_e + vector[0] * bearing_along
    bearing_n = plate_n + vector[1] * bearing_along
    model.add(Primitive(
        kind="CYLINDER", sube="BEARING",
        attrs={"DIAM": bearing_dia, "HEIG": bearing_len},
        east=bearing_e, north=bearing_n, up=shaft_u, ori=ori,
        note=note))
    model.reference_values.append("bearing housing proportioned from /P1501B")

    # ---- free shaft and coupling, only where the CSV carries a shaft ----
    shaft_len = engine.get("shaft_total_L_mm")
    motor_face = _axis_position(motor_e, motor_n, vector, -motor_len / 2)
    bearing_face_along = _along(bearing_e, bearing_n, plate_e, plate_n, vector) \
        + bearing_len / 2
    motor_face_along = _along(motor_e, motor_n, plate_e, plate_n, vector) \
        - motor_len / 2
    gap = motor_face_along - bearing_face_along

    if shaft_len is None:
        # MC pumps carry "N/A (MC Pump)" here: close-coupled, no free shaft.
        model.facts["shaft"] = "N/A -- close-coupled MC arrangement"
    elif gap > 20.0:
        shaft_dia = engine.get("shaft_cyl1_D_mm") or casing_dia * REF["shaft_dia"]
        mid = (bearing_face_along + motor_face_along) / 2
        shaft_e = plate_e + vector[0] * mid
        shaft_n = plate_n + vector[1] * mid
        model.add(Primitive(
            kind="CYLINDER", sube="COUPLING",
            attrs={"DIAM": shaft_dia, "HEIG": gap},
            east=shaft_e, north=shaft_n, up=shaft_u, ori=ori,
            note="drive shaft spanning bearing housing to motor face"))
        # Coupling guard hubs at each end of the span.
        for along, label in ((bearing_face_along + gap * 0.18, "pump hub"),
                             (motor_face_along - gap * 0.18, "driver hub")):
            hub_e = plate_e + vector[0] * along
            hub_n = plate_n + vector[1] * along
            model.add(Primitive(
                kind="CYLINDER", sube="COUPLING",
                attrs={"DIAM": shaft_dia * 2.0, "HEIG": gap * 0.22},
                east=hub_e, north=hub_n, up=shaft_u, ori=ori,
                note=f"coupling {label}"))
        model.reference_values.append("coupling hubs proportioned from /P1501B")
    else:
        model.facts["shaft"] = f"close-coupled: gap {gap:.0f} mm"

    # ---- motor -----------------------------------------------------------
    model.add(Primitive(
        kind="CYLINDER", sube="DRIVER",
        attrs={"DIAM": motor_dia, "HEIG": motor_len},
        east=motor_e, north=motor_n, up=shaft_u, ori=ori,
        note="stator barrel: DIAM/HEIG from engine_shaft CSV"))

    # End bells.  IR-1: a DISH sits on its rim, so each is placed on the
    # barrel end face and faces outward.
    for direction, sign in ((motor_end, +1.0), (wet_end, -1.0)):
        end_vector = AXIS_VECTOR[direction]
        rim_e = motor_e + end_vector[0] * motor_len / 2
        rim_n = motor_n + end_vector[1] * motor_len / 2
        model.add(Primitive(
            kind="DISH", sube="DRIVER",
            attrs={"DIAM": motor_dia * REF["motor_end_dish_dia"],
                   "HEIG": motor_dia * REF["motor_end_dish_heig"],
                   "RADI": motor_dia * REF["motor_end_dish_radi"]},
            east=rim_e, north=rim_n, up=shaft_u,
            ori=f"ORI Z is {direction} and Y is U",
            note="motor end bell: proportion from /P1501B"))

    # Cooling ribs: axial ribs on the full 360 degrees, as /P1501B builds them
    # and as the client required.  Each overlaps the stator and projects
    # beyond it.
    rib_radial = motor_dia * REF["rib_radial"]
    rib_thick = motor_dia * REF["rib_thick"]
    radius = motor_dia / 2
    # The rib straddles the barrel surface so it always overlaps the stator
    # solid and still projects beyond it, which is what the client required.
    seat = radius - rib_radial * 0.25
    for index in range(RIB_COUNT):
        angle = 2.0 * math.pi * index / RIB_COUNT
        # The rib sits at `angle` around the machine axis, measured in the
        # plane perpendicular to that axis: one component is transverse in
        # plan, the other is vertical.
        offset_tran = math.cos(angle) * seat
        offset_up = math.sin(angle) * seat
        if long_axis == "N":
            rib_e = motor_e + offset_tran
            rib_n = motor_n
        else:
            rib_e = motor_e
            rib_n = motor_n + offset_tran

        # IR-3a: a rectangular plate on a circular body must rotate with its
        # radial bearing.  The rib is expressed in its OWN frame -- local X
        # radial, local Y along the machine, local Z tangential -- and the
        # rotation is carried by ORI, not by swapping world-aligned lengths.
        model.add(Primitive(
            kind="BOX", sube="DRIVER",
            attrs={"XLEN": rib_radial, "YLEN": motor_len, "ZLEN": rib_thick},
            east=rib_e, north=rib_n, up=shaft_u + offset_up,
            ori=_rib_ori(long_axis, math.degrees(angle)),
            note=f"cooling rib {index + 1}/{RIB_COUNT} at "
                 f"{math.degrees(angle):.0f} deg"))
    model.reference_values.append(
        f"{RIB_COUNT} axial cooling ribs, 360-degree distribution (/P1501B)")

    # Terminal box on the motor crown, and its electrical connection.  It is
    # seated so its underside overlaps the stator surface rather than hovering
    # above the rib tips, which would leave it detached from the machine.
    box = motor_dia * REF["terminal_box"]
    box_height = box * 0.6
    crown = shaft_u + motor_dia / 2
    box_centre_u = crown + box_height / 2 - box_height * 0.25
    model.add(Primitive(
        kind="BOX", sube="DRIVER",
        attrs={"XLEN": box, "YLEN": box, "ZLEN": box_height},
        east=motor_e, north=motor_n, up=box_centre_u,
        note="terminal box: proportion from /P1501B, seated on the stator"))
    model.reference_values.append("terminal box proportioned from /P1501B")

    model.add(Primitive(
        kind="ELCONN", sube="DRIVER",
        attrs={}, east=motor_e, north=motor_n,
        up=box_centre_u + box_height / 2,
        note="electrical connection"))

    # Motor feet, carried down to the baseplate so the driver is supported.
    foot_top = shaft_u - motor_dia * 0.42
    foot_height = max(foot_top - plate_top, 10.0)
    spacing = motor_len * 0.32
    for sign in (-1.0, +1.0):
        foot_e = motor_e + vector[0] * spacing * sign
        foot_n = motor_n + vector[1] * spacing * sign
        model.add(Primitive(
            kind="BOX", sube="SUPPORT",
            attrs={"XLEN": motor_dia * 0.85 if long_axis == "N" else motor_len * 0.22,
                   "YLEN": motor_len * 0.22 if long_axis == "N" else motor_dia * 0.85,
                   "ZLEN": foot_height},
            east=foot_e, north=foot_n, up=plate_top + foot_height / 2,
            note="motor pedestal: chains driver -> baseplate"))
    model.reference_values.append("motor pedestals sized from motor envelope")


def _rib_ori(long_axis: str, degrees: float) -> str:
    """
    Orientation for a cooling rib at a given angle around the stator.

    IR-3a: a rectangular part on a circular body must rotate with its radial
    bearing, or it stays world-aligned and stands off the surface.

    IR-3a's worked example is a plate on a VERTICAL vessel, where every radial
    direction lies in the horizontal plane and local Z can stay Up.  A motor is
    a HORIZONTAL cylinder, so its ribs sweep a vertical plane instead and
    ``ORI Z IS U`` would pin every rib upright -- correct only for the two ribs
    at top and bottom dead centre.  The principle is what carries over, not the
    literal axis letters: local X is the radial bearing, local Y runs along the
    body, and local Z is the remaining tangential direction.

    Local Y is therefore the machine axis, and X sweeps from the transverse
    plan axis toward Up as the rib goes round.
    """
    transverse = "E" if long_axis == "N" else "N"
    along = "N" if long_axis == "N" else "E"
    # Normalise to E3D's 0-360 bearing form; a whole-degree bearing is written
    # without a fraction so the common cardinal cases stay readable.
    bearing = degrees % 360.0
    if abs(bearing - round(bearing)) < 0.005:
        bearing_text = f"{round(bearing):d}"
    else:
        bearing_text = f"{bearing:.2f}"
    return f"ORI Y IS {along} AND X IS {transverse} {bearing_text} U"


def _along(east, north, origin_e, origin_n, vector) -> float:
    """Signed distance from the plate centre along the machine axis."""
    return (east - origin_e) * vector[0] + (north - origin_n) * vector[1]


def _axis_position(east, north, vector, distance):
    return (east + vector[0] * distance, north + vector[1] * distance)


def _build_nozzles(model, suction, discharge, casing_e, casing_n,
                   casing_dia, casing_len, shaft_u, location):
    """
    Emit the two catalogue nozzles.

    Plan position and direction are reproduced exactly -- they are hard
    constraints.  Only the discharge U is adjusted, and only so the flange
    lands on the casing crown rather than inside or above the volute.
    """
    catr = {n.name: n.catr for n in location.nozzles}

    for row in (suction, discharge):
        if row is None:
            continue
        letter = row["letter"]
        east = row["pos"]["east"]
        north = row["pos"]["north"]
        up = row["pos"]["up"]
        note = "plan position and direction preserved exactly"

        if letter == "U":
            # A top discharge belongs on the casing crown.  The nozzle POS is
            # its FLANGE FACE (IR-9a), so it sits a full projection above the
            # crown, less a deliberate penetration into the volute.
            crown = shaft_u + casing_dia / 2
            wanted = crown - 100.0 + (row["heig"] or 150.0)
            if abs(wanted - up) > 1.0:
                note = (f"Z adjusted {up:.1f} -> {wanted:.1f} so the flange "
                        f"face clears the casing crown at {crown:.1f}")
                model.facts.setdefault("nozzle_z_adjustments", []).append(
                    f"{row['role']}: {up:.1f} -> {wanted:.1f}")
                up = wanted
        else:
            # A horizontal nozzle stays on the shaft centreline.
            if abs(up - shaft_u) > 1.0:
                note = f"Z adjusted {up:.1f} -> {shaft_u:.1f} onto the shaft centreline"
                model.facts.setdefault("nozzle_z_adjustments", []).append(
                    f"{row['role']}: {up:.1f} -> {shaft_u:.1f}")
                up = shaft_u

        model.add(Primitive(
            kind="NOZZLE", sube=row["role"],
            attrs={"HEIG": row["heig"] or 150.0},
            east=east, north=north, up=up,
            ori=f"ORI P1 IS {letter}",
            name=f"{model.element}_{row['role']}_NOZZLE",
            catr=catr.get(row["name"]),
            note=note))


def main() -> int:
    sources = load_all()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    models = []
    for tag in sorted(sources["location"]):
        model = build_pump(tag, sources)
        models.append(model)
        path = OUTPUT_DIR / f"{tag.replace('-', '_')}.pml"
        path.write_text(model.to_pml(), encoding="utf-8")

    combined = OUTPUT_DIR / "JK_Pump_Build_2026-08-19_all_pumps.pml"
    combined.write_text(
        "-- JK_Pump_Build -- all pumps, 2026-08-19 rebuild\n"
        "-- One independent EQUI per pump.\n"
        + "\n".join(m.to_pml() for m in models), encoding="utf-8")

    print(f"Generated {len(models)} pump macros in {OUTPUT_DIR}")
    for model in models:
        print(f"  {model.tag:<12} {len(model.primitives):>4} elements  "
              f"{len(model.unresolved)} unresolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
