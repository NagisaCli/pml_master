"""
Generate the complete E3D pump models, including the 2026-08-20 r12 rebuild.

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

Top-discharge connection
    The native NOZZLE keeps its r9 CATR, plan position, orientation and
    flange-face U.  A nozzle no wider than the casing directly penetrates the
    crown with at least 70% of its HEIG outside.  A wider nozzle is carried by
    a casing-owned lower socket and CONE whose upper face meets the native
    nozzle root exactly; no extra primitive neck sits above the reducer.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, List, Optional

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all                      # noqa: E402
from recover_nozzle_axes import classify                        # noqa: E402
from pump_model import (AXIS_VECTOR, OPPOSITE,  # noqa: E402
                        REF, RIB_COUNT, Primitive, PumpModel)
from base_deform import (ReferenceDeformer, Target,  # noqa: E402
                         parse_reference)
from wsb.pml_builder import NOZZLE_BORE_COMPONENTS    # noqa: E402

OUTPUT_DIR = (REPO / "Projects" / "JK_Pump_Build" / "output" /
              "2026-08-20_top_nozzle_r12")

MOTOR_CONE_OUTER_RATIO = 2.0 / 3.0
MOTOR_LENGTH_OVERRIDE_TAG = "205-PU-012"
TOP_NOZZLE_CASING_EMBED = 20.0
TOP_NOZZLE_CONNECTOR_PROJECTION = 20.0
TOP_NOZZLE_SOCKET_VISIBLE = 8.0
TOP_NOZZLE_CASING_SEAT_RATIO = 0.90
TOP_NOZZLE_MIN_NATIVE_PROJECTION = 25.0
SMALL_NOZZLE_EXTERNAL_TARGET_RATIO = 0.75
NOZZLE_DN_BY_COMPONENT = {
    component: float(dn) for dn, component in NOZZLE_BORE_COMPONENTS.items()
}


def perpendicular(letter: str) -> str:
    """The plan axis at right angles to a cardinal direction."""
    return "E" if letter in ("N", "S") else "N"


def axis_component(east: float, north: float, letter: str) -> float:
    """Signed distance along a cardinal plan direction."""
    vector = AXIS_VECTOR[letter]
    return east * vector[0] + north * vector[1]


def _source_envelope(tag: str, sources: dict) -> tuple[float, float, float]:
    """Plate longitudinal/transverse sizes and governing casing diameter."""
    plate = sources["location"][tag].baseplate
    xlen = plate.attrs["XLEN"]
    ylen = plate.attrs["YLEN"]
    length, width = max(xlen, ylen), min(xlen, ylen)
    casing = sources["casing"].get(tag)
    casing_dia = (casing or {}).get("diameter") or width * 0.72
    return length, width, casing_dia


def _derive_missing_engine(tag: str, sources: dict) -> dict:
    """
    Derive a traceable motor/shaft record for a tag absent from the CSV.

    The nearest measured non-MC pump is selected from plate length, plate width
    and casing diameter. Axial dimensions/offsets follow the plate-length ratio
    and radial dimensions follow the plate-width ratio. This keeps the complete
    measured four-part motor and three-part drive-shaft construction while
    making the fallback fit the target skid. Every use is reported as a
    Reference Value; the source CSV itself is never edited.
    """
    target_length, target_width, target_casing = _source_envelope(tag, sources)
    ranked = []
    for donor_tag, donor in sources["engine"].items():
        if donor.get("is_mc"):
            continue
        donor_length, donor_width, donor_casing = _source_envelope(
            donor_tag, sources)
        score = (
            ((donor_length - target_length) / target_length) ** 2
            + ((donor_width - target_width) / target_width) ** 2
            + 2.0 * ((donor_casing - target_casing) / target_casing) ** 2
        )
        # A geometrically similar but axially overfilled donor is not a sound
        # fallback. Penalise families whose motor + free-shaft source lengths
        # already consume nearly the whole donor skid; this prevents a large
        # driver from being compressed to a token shaft on a shorter target.
        occupied_ratio = (
            (donor.get("engine_total_L_mm") or 0.0)
            + (donor.get("shaft_total_L_mm") or 0.0)
        ) / donor_length
        score += 4.0 * max(0.0, occupied_ratio - 0.90) ** 2
        ranked.append((score, donor_tag, donor, donor_length, donor_width))
    if not ranked:
        raise ValueError(f"{tag}: no measured non-MC engine donor is available")

    _, donor_tag, donor, donor_length, donor_width = min(ranked)
    axial_scale = target_length / donor_length
    radial_scale = target_width / donor_width
    record = dict(donor)
    for key, value in tuple(record.items()):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            continue
        if key.endswith("_L_mm") or "axial_offset" in key:
            record[key] = value * axial_scale
        elif (key.endswith("_D_mm") or key.endswith("_dia_mm")
              or key.endswith("_D_min_mm") or key.endswith("_D_max_mm")
              or "radial_offset" in key):
            record[key] = value * radial_scale

    casing = sources["casing"].get(tag)
    record["equipment_name"] = ((casing or {}).get("pump_name")
                                or sources["location"][tag].func or tag)
    record["pump_type_raw"] = "NON-MC PUMP (DERIVED REFERENCE VALUE)"
    record["is_mc"] = False
    record["derived_from_tag"] = donor_tag
    record["derived_axial_scale"] = axial_scale
    record["derived_radial_scale"] = radial_scale
    return record


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

    # Three project tags have no CSV row. Omitting the complete driver left
    # those r6 models incomplete, so r7 uses a deterministic nearest measured
    # non-MC family and labels every resulting dimension as a Reference Value.
    # The supplied CSV remains immutable.
    if engine is None:
        engine = _derive_missing_engine(tag, sources)
        donor = engine["derived_from_tag"]
        model.description = str(engine["equipment_name"])[:120]
        model.facts["engine_source"] = f"DERIVED from {donor}"
        model.reference_values.append(
            f"motor/drive layout derived from measured {donor}: axial scale "
            f"{engine['derived_axial_scale']:.4f}, radial scale "
            f"{engine['derived_radial_scale']:.4f}")
        model.unresolved.append(
            f"no engine_shaft CSV row; motor/drive derived from nearest "
            f"measured non-MC pump {donor}")
    else:
        model.facts["engine_source"] = "engine_shaft_measurements_updated.csv"
    model.facts["engine_record"] = engine

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
    # r6 established an accepted driver clearance envelope for the support
    # geometry.  r7 replaces the old visual end covers with measured CONEs but
    # deliberately preserves that envelope, so improving the motor does not
    # silently reopen the already accepted base/support elevation.
    suction_u = suction["pos"]["up"]
    motor_dia = (engine or {}).get("engine_max_dia_mm")
    accepted_driver_envelope = ((motor_dia or 0.0)
                                * REF["motor_end_dish_dia"])
    required = max(casing_dia, accepted_driver_envelope) / 2
    governing_body = ("accepted r6 driver clearance envelope"
                      if accepted_driver_envelope > casing_dia else "casing")
    model.reference_values.append(
        "r6 driver clearance envelope retained for shaft/support elevation; "
        "r7 motor end geometry is measured CONE/CYLINDER construction")

    # A pump is CARRIED on its mounting; the casing does not rest on the
    # baseplate.  Seating the machine flat on the plate left zero clearance on
    # most pumps and crushed the whole support chain into a few millimetres.
    #
    # /P1501B holds its volute 110 mm clear of the plate top on a 170 mm casing
    # radius -- 0.647 of the radius -- and fills that space with sole plates,
    # gusset webs and a mounting pad.  The same allowance is applied here so the
    # reference's own support has the room it needs.
    support_allowance = max(required * REF["support_clearance"], 90.0)
    seated_u = plate_top + required + support_allowance
    model.facts["support_allowance"] = support_allowance

    if suction_u < seated_u - 0.5:
        shaft_u = seated_u
        model.unresolved.append(
            f"CONFLICT: suction elevation U {suction_u:.1f} is below the "
            f"{governing_body} radius {required:.1f} (casing_reference.txt / "
            f"engine_shaft CSV); a machine on that axis would sink below the "
            f"foundation. Shaft raised to U {seated_u:.1f} to seat it on the "
            f"baseplate.")
        model.facts["shaft_u_basis"] = (
            f"raised from suction U {suction_u:.1f} to seat {governing_body}")
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

    # The machine is emitted first so the support can be sized from its real
    # measured underside rather than from a ratio.
    _build_casing(model, casing_e, casing_n, casing_dia, casing_len,
                  shaft_u, long_axis, wet_end, plate_top, is_mc)
    _build_top_discharge_connection(
        model, discharge, casing_e, casing_n, casing_dia, casing_len, shaft_u)
    _build_drive(model, engine, casing_e, casing_n, casing_dia, casing_len, shaft_u,
                 long_axis, wet_end, motor_end, plate_e, plate_n,
                 half_long, plate_top, is_mc)

    # --- the base, reproduced from Base_reference.txt ---------------------
    # Not redesigned: every one of /P1501B-BASE's 43 elements is mapped into
    # this pump's frame, adapted to its own plate, casing and motor positions.
    _build_reference_base(model, plate_e, plate_n, xlen, ylen, plate_top,
                          long_axis, wet_end, casing_e, casing_n)

    _build_nozzles(model, suction, discharge, casing_e, casing_n,
                   casing_dia, casing_len, shaft_u, location)
    return model


def hex_profile(across_flats: float):
    """
    A regular hexagon profile, as /P1501B writes its washers.

    The reference washer is a true six-vertex hexagon (34.64 across flats, which
    is 20 * sqrt(3)), not a cylinder.  The client asked specifically for hex
    hardware, so the shape is reproduced rather than approximated.
    """
    radius = across_flats / math.sqrt(3.0)      # circumradius
    return [(radius * math.cos(math.radians(60 * i)),
             radius * math.sin(math.radians(60 * i))) for i in range(6)]


def _lowest_of(model, sube: str, kinds: tuple = ()) -> float:
    """
    The measured underside of an assembly already emitted into the model.

    A support has to reach the real bottom of the body it carries, so that
    height is read back off the geometry rather than guessed from a fraction of
    a diameter.  Deriving it from a ratio is what buried the pedestals inside
    the machines and left the render showing a floating pump on flat rails.
    """
    lows = []
    for primitive in model.primitives:
        if primitive.sube != sube:
            continue
        if kinds and primitive.kind not in kinds:
            continue
        attrs = primitive.attrs
        if primitive.kind == "CYLINDER":
            axis = _ori_axis(primitive.ori)
            radius = attrs.get("DIAM", 0) / 2
            half = attrs.get("HEIG", 0) / 2
            # Only the axial component lowers a cylinder along U; a horizontal
            # barrel drops by its radius instead.
            drop = abs(half * axis[2]) + radius * math.sqrt(
                max(0.0, 1.0 - axis[2] ** 2))
            lows.append(primitive.up - drop)
        elif primitive.kind == "DISH":
            axis = _ori_axis(primitive.ori)
            radius = attrs.get("DIAM", 0) / 2
            height = attrs.get("HEIG", 0)
            drop = radius * math.sqrt(max(0.0, 1.0 - axis[2] ** 2))
            lows.append(min(primitive.up, primitive.up + height * axis[2]) - drop)
        elif primitive.kind == "BOX":
            lows.append(primitive.up - attrs.get("ZLEN", 0) / 2)
    return min(lows) if lows else model.facts["plate_top"]


def _ori_axis(ori: str):
    """Unit vector of the axis named by an ``ORI ... Z is <letter>`` clause."""
    if not ori:
        return (0.0, 0.0, 1.0)
    tokens = ori.replace(" and ", " ").replace(" AND ", " ").split()
    for index, token in enumerate(tokens):
        if token.upper() == "Z" and index + 2 < len(tokens):
            letter = tokens[index + 2].upper()
            if letter in AXIS_VECTOR:
                return AXIS_VECTOR[letter]
    return (0.0, 0.0, 1.0)


def _build_reference_base(model, plate_e, plate_n, xlen, ylen, plate_top,
                          long_axis, wet_end, casing_e, casing_n):
    """
    Emit ``Base_reference.txt``'s own geometry, deformed to fit this pump.

    The reference is the geometric master: its members, their relative
    arrangement, gusset tapers, bracket layout and hex profiles all come across
    unchanged.  Only two things are adapted, and only as far as this pump needs:

    * each **station translates** to its machine's real plan position, moving
      as a rigid group so the shape inside it is untouched;
    * the band **above the plate top stretches per station**, so the pump
      mounting lands on the casing and the motor mounting on the stator.

    The mounting elevations are measured from the machine that has just been
    emitted, so the equipment sits directly on its support with no gap.
    """
    plate_under = model.facts["plate_under"]
    width = xlen if long_axis == "N" else ylen
    length = ylen if long_axis == "N" else xlen

    vector = AXIS_VECTOR[wet_end]
    casing_station = ((casing_e - plate_e) * vector[0]
                      + (casing_n - plate_n) * vector[1])

    casing_dia, casing_len = model.facts["casing"]
    shaft_u = model.facts["shaft_u"]

    motor_support = model.facts.get("motor_support")
    if motor_support:
        motor_station = ((motor_support["centre_e"] - plate_e) * vector[0]
                         + (motor_support["centre_n"] - plate_n) * vector[1])
        motor_radius = motor_support["diameter"] / 2
        motor_length = motor_support["barrel_length"]
    else:
        # No driver modelled: keep the native motor relationship as a clearly
        # labelled reference value rather than inventing target motor data.
        motor_station = None
        motor_radius = None
        motor_length = None

    # Keep both stations on the plate.
    limit = length / 2 - length * 0.10
    casing_station = max(-limit, min(limit, casing_station))
    if motor_station is not None:
        motor_station = max(-limit, min(limit, motor_station))

    target = Target(
        plate_e=plate_e, plate_n=plate_n,
        plate_top=plate_top, plate_under=plate_under,
        width=width, length=length, wet_end=wet_end,
        pump_machine=casing_station, pump_axis_up=shaft_u,
        pump_radius=casing_dia / 2, pump_length=casing_len,
        motor_machine=motor_station, motor_axis_up=shaft_u,
        motor_radius=motor_radius, motor_length=motor_length)

    def emit(kind, attrs, east, north, up, ori, profile, note):
        model.add(Primitive(
            kind=kind, sube="BASE", attrs=attrs,
            east=east, north=north, up=up,
            ori=ori, profile=profile or None, note=note))

    elements = _reference_elements()
    adapter = ReferenceDeformer(target, elements)
    adapter.build(emit)

    model.facts["base_stations"] = [
        ("pump", round(adapter.station_target["pump"], 1),
         round(shaft_u, 1)),
        ("motor", round(adapter.station_target["motor"], 1),
         round(shaft_u, 1)),
    ]
    model.facts["base_adapter"] = {
        station: tuple(round(value, 6) for value in scale)
        for station, scale in adapter.scales.items()
    }
    model.facts["base_station_targets"] = dict(adapter.station_target)
    model.reference_values.append(
        "base: all 43 /P1501B-BASE members; skid fitted to the project "
        "envelope, pump station to the casing, motor station to the stator")


_REFERENCE_CACHE = None


def _reference_elements():
    """The parsed reference, read once and shared across all 30 pumps."""
    global _REFERENCE_CACHE
    if _REFERENCE_CACHE is None:
        _REFERENCE_CACHE = parse_reference()
    return _REFERENCE_CACHE


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

    # The casing's support chain is built by _build_machine_support, which
    # reproduces the reference's rail -> sole plate -> gusseted pedestal ->
    # machine sequence rather than a single block.


def _nozzle_dn(catr: Optional[str]) -> Optional[float]:
    """Return the verified catalogue nominal diameter for one nozzle."""
    if not catr:
        return None
    return NOZZLE_DN_BY_COMPONENT.get(catr.rsplit("/", 1)[-1])


def _top_nozzle_face_u(row: dict, crown: float) -> float:
    """The r9 flange-face elevation, retained as an invariant in r12."""
    return crown - 100.0 + (row.get("heig") or 150.0)


def _top_nozzle_interface_u(crown: float) -> float:
    """Upper terminal face shared by an overwidth reducer and native nozzle."""
    return crown + TOP_NOZZLE_CONNECTOR_PROJECTION


def _top_nozzle_resolution(row: dict, crown: float,
                           casing_width: float) -> Optional[dict]:
    """Resolve the native root from the two client-required width branches."""
    nozzle_dia = _nozzle_dn(row.get("catr"))
    if nozzle_dia is None:
        return None
    face_u = _top_nozzle_face_u(row, crown)
    overwidth = nozzle_dia > casing_width + 0.01
    if overwidth:
        root_u = _top_nozzle_interface_u(crown)
        heig = face_u - root_u
        external_ratio = 1.0
    else:
        external_height = face_u - crown
        heig = external_height / SMALL_NOZZLE_EXTERNAL_TARGET_RATIO
        root_u = face_u - heig
        external_ratio = external_height / heig
    return {
        "nozzle_diameter": nozzle_dia,
        "casing_width": casing_width,
        "casing_crown_u": crown,
        "nozzle_face_u": face_u,
        "nozzle_root_u": root_u,
        "nozzle_heig": heig,
        "external_ratio": external_ratio,
        "overwidth": overwidth,
    }


def _build_top_discharge_connection(model, discharge, casing_e, casing_n, dia,
                                    casing_width, shaft_u):
    """Build only the overwidth socket/CONE shown in the client schematic.

    A smaller/equal nozzle uses no additive connector: the native NOZZLE itself
    penetrates the casing with at least 70% outside.  A wider nozzle receives a
    lower socket that starts inside the crown and remains visibly proud, then a
    CONE that expands directly to the native nozzle bottom.
    """
    if not discharge or discharge.get("letter") != "U":
        return

    crown = shaft_u + dia / 2.0
    resolution = _top_nozzle_resolution(discharge, crown, casing_width)
    if resolution is None:
        model.unresolved.append(
            "top discharge has no verified catalogue DN; casing connector omitted")
        return

    nozzle_dia = resolution["nozzle_diameter"]
    nozzle_e = discharge["pos"]["east"]
    nozzle_n = discharge["pos"]["north"]
    face_u = resolution["nozzle_face_u"]
    top_u = resolution["nozzle_root_u"]
    native_projection = resolution["nozzle_heig"]
    if resolution["overwidth"] and native_projection < TOP_NOZZLE_MIN_NATIVE_PROJECTION:
        model.unresolved.append(
            f"top discharge has only {native_projection:.1f} mm between the "
            "connector top and fixed flange face; connector omitted")
        return

    overwidth = resolution["overwidth"]
    connection = dict(resolution, role=discharge["role"], top_u=top_u)

    if not overwidth:
        connection["primitive_count"] = 0
        connection["direct_penetration"] = True
        connection["bottom_u"] = top_u
        model.facts.setdefault("top_nozzle_connections", []).append(connection)
        model.reference_values.append(
            "top discharge within casing width uses the native NOZZLE directly; "
            "75% external projection provides margin over the 70% minimum")
        return

    bottom_u = crown - TOP_NOZZLE_CASING_EMBED
    connection["bottom_u"] = bottom_u
    connection["direct_penetration"] = False
    ori = "ORI Z is U and Y is N"
    prefix = "top discharge casing connection"
    seat_dia = casing_width * TOP_NOZZLE_CASING_SEAT_RATIO
    socket_top = crown + TOP_NOZZLE_SOCKET_VISIBLE
    transition_top = top_u

    # One MC casing datum (205-PU-054) is offset in plan from its fixed top
    # nozzle. Preserve both project positions and join them with a solid
    # casing-owned CYLINDER. It is an additive basic body, not PIPE/BRANCH.
    delta_e = nozzle_e - casing_e
    delta_n = nozzle_n - casing_n
    plan_offset = math.hypot(delta_e, delta_n)
    if plan_offset > casing_width / 2.0 - TOP_NOZZLE_CASING_EMBED:
        unit_e = delta_e / plan_offset
        unit_n = delta_n / plan_offset
        start_distance = max(0.0, casing_width / 2.0
                             - TOP_NOZZLE_CASING_EMBED)
        overlap = min(15.0, seat_dia * 0.10)
        start_e = casing_e + unit_e * start_distance
        start_n = casing_n + unit_n * start_distance
        end_e = nozzle_e + unit_e * overlap
        end_n = nozzle_n + unit_n * overlap
        bridge_length = math.hypot(end_e - start_e, end_n - start_n)
        bridge_axis = ("E" if unit_e > 0 else "W") \
            if abs(unit_e) >= abs(unit_n) else ("N" if unit_n > 0 else "S")
        model.add(Primitive(
            kind="CYLINDER", sube="CASING",
            attrs={"DIAM": seat_dia, "HEIG": bridge_length},
            east=(start_e + end_e) / 2.0,
            north=(start_n + end_n) / 2.0,
            up=(bottom_u + socket_top) / 2.0,
            ori=f"ORI Z is {bridge_axis} and Y is U",
            note="top discharge casing offset bridge: solid basic body"))
        connection["offset_bridge"] = True
        model.reference_values.append(
            "fixed offset top nozzle is joined to the unchanged casing "
            "position by an overlapping solid CYLINDER basic body")
    else:
        connection["offset_bridge"] = False

    model.add(Primitive(
        kind="CYLINDER", sube="CASING",
        attrs={"DIAM": seat_dia, "HEIG": socket_top - bottom_u},
        east=nozzle_e, north=nozzle_n, up=(bottom_u + socket_top) / 2.0,
        ori=ori,
        note=f"{prefix}: overwidth lower socket"))
    model.add(Primitive(
        kind="CONE", sube="CASING",
        attrs={"DBOT": seat_dia, "DTOP": nozzle_dia,
               "HEIG": transition_top - socket_top},
        east=nozzle_e, north=nozzle_n,
        up=(socket_top + transition_top) / 2.0,
        ori=ori,
        note=f"{prefix}: overwidth smooth reducer transition"))
    connection["primitive_count"] = 2
    connection["seat_diameter"] = seat_dia

    model.facts.setdefault("top_nozzle_connections", []).append(connection)
    model.reference_values.append(
        "overwidth top discharge uses a 90%-of-width lower socket and one "
        "concentric CONE; the CONE upper face closes directly on the native "
        "nozzle bottom with no extra primitive neck")


def _motor_cone_length(engine: dict, total: float) -> float:
    """One shared end-cone length; either measured side may supply it."""
    candidates = [float(value) for value in (
        engine.get("engine_part1_rear_cover_L_mm"),
        engine.get("engine_front_frustum_L_mm"),
    ) if value is not None and float(value) > 0.01]
    return sum(candidates) / len(candidates) if candidates else total * 0.08


def _motor_segments(model, engine: dict, total: float, maximum: float) -> list[dict]:
    """Resolve a closed motor whose terminal body at each end is a CONE."""
    cone_len = _motor_cone_length(engine, total)
    source_small_len = engine.get("engine_small_cyl_L_mm") or 0.0
    main_len = ((engine.get("engine_part2_main_body_L_mm") or total)
                + source_small_len)
    if model.tag == MOTOR_LENGTH_OVERRIDE_TAG:
        # This tag's r8 envelope is an explicit user correction. Removing the
        # terminal small cylinder must not shorten it again.
        main_len = total - 2 * cone_len

    # r8 placed the CSV rear-small CYLINDER outside the rear cone, so the motor
    # tail was still cylindrical. The client requires the physical tail itself
    # to be a frustum. Omit that exterior cylinder and absorb its axial allowance
    # into the main stator, preserving the already corrected total envelope.
    raw_sum = main_len + 2 * cone_len
    correction = total - raw_sum
    if abs(correction) > 0.01:
        adjusted = main_len + correction
        if adjusted <= 1.0:
            scale = total / raw_sum
            cone_len *= scale
            main_len *= scale
        else:
            main_len = adjusted
        if abs(correction) > 0.51:
            model.unresolved.append(
                f"CONFLICT: motor component lengths total {raw_sum:.1f} mm "
                f"against resolved envelope {total:.1f} mm; main barrel fitted "
                f"to preserve the user-corrected overall construction")

    main_dia = engine.get("engine_part2_main_body_D_mm") or maximum
    outer_dia = main_dia * MOTOR_CONE_OUTER_RATIO

    model.facts["motor_cone_length"] = cone_len
    model.facts["motor_cone_outer_diameter"] = outer_dia
    model.reference_values.append(
        "user-corrected motor end construction: two similar CONEs, each "
        "tapering from the main stator to a 2/3-diameter outward face")
    if (engine.get("engine_small_cyl_L_mm") or 0.0) > 0.01:
        model.reference_values.append(
            "rear-small-cylinder source allowance absorbed into the main "
            "stator so the motor tail terminates directly in a CONE")

    segments: list[dict] = []
    segments.append({
        "role": "rear frustum", "kind": "CONE", "length": cone_len,
        "DBOT": outer_dia, "DTOP": main_dia,
    })
    segments.append({
        "role": "main stator barrel", "kind": "CYLINDER",
        "length": main_len, "DIAM": main_dia,
    })
    segments.append({
        "role": "front frustum", "kind": "CONE", "length": cone_len,
        "DBOT": main_dia, "DTOP": outer_dia,
    })
    return segments


def _build_drive(model, engine, casing_e, casing_n, casing_dia, casing_len, shaft_u,
                 long_axis, wet_end, motor_end, plate_e, plate_n,
                 half_long, plate_top, is_mc):
    """
    Build the measured segmented motor and drive train on one centreline.

    Non-MC motors use the CSV's rear frustum, small barrel, main barrel and
    front frustum. Their drive train uses two cylinders plus the pump-side
    circular frustum. Axial shaft part ratios are retained but uniformly fitted
    between the motor front and a controlled engagement into the casing when
    source offsets conflict with an attached construction. MC rows explicitly
    carry no free shaft, so a close-coupled lantern spans the physical gap.
    """
    motor_vector = AXIS_VECTOR[motor_end]
    wet_vector = AXIS_VECTOR[wet_end]

    motor_source_len = engine.get("engine_total_L_mm")
    motor_dia = engine.get("engine_max_dia_mm")
    motor_axial = engine.get("engine_axial_offset_mm")
    if motor_source_len is None or motor_dia is None:
        model.unresolved.append("motor length/diameter missing from the CSV")
        return
    motor_len = float(motor_source_len)
    if model.tag == MOTOR_LENGTH_OVERRIDE_TAG:
        cone_len = _motor_cone_length(engine, motor_len)
        small_len = engine.get("engine_small_cyl_L_mm") or 0.0
        # The r7 interpretation compressed this motor's main barrel to 717 mm.
        # The client identified the result as too short. Keep the supplied
        # 997.4 mm as the main barrel and place its end construction outside it.
        motor_len = motor_len + float(small_len) + 2 * cone_len
        model.reference_values.append(
            f"{model.tag} user-corrected motor envelope {motor_len:.1f} mm: "
            f"source total {motor_source_len:.1f} mm retained as main barrel, "
            f"rear small barrel and two end CONEs added outside")
    model.facts["motor_source_total"] = float(motor_source_len)
    model.facts["motor_effective_total"] = motor_len

    motor_centre_offset = abs(motor_axial) if motor_axial is not None else \
        half_long * 0.5
    if motor_axial is None:
        model.unresolved.append("engine_axial_offset is N/A; motor placed by proportion")
        model.reference_values.append("motor axial position DERIVED")

    motor_e = plate_e + motor_vector[0] * motor_centre_offset
    motor_n = plate_n + motor_vector[1] * motor_centre_offset
    motor_centre_along = _along(
        motor_e, motor_n, plate_e, plate_n, wet_vector)
    motor_start = motor_centre_along - motor_len / 2
    motor_end_face = motor_centre_along + motor_len / 2

    # ---- measured motor segmentation ----------------------------------
    resolved = _motor_segments(model, engine, motor_len, motor_dia)
    cursor = motor_start
    emitted_segments = []
    main_primitive = None
    for segment in resolved:
        length = segment["length"]
        centre = cursor + length / 2
        east = plate_e + wet_vector[0] * centre
        north = plate_n + wet_vector[1] * centre
        if segment["kind"] == "CONE":
            attrs = {"DBOT": segment["DBOT"], "DTOP": segment["DTOP"],
                     "HEIG": length}
        else:
            attrs = {"DIAM": segment["DIAM"], "HEIG": length}
        primitive = model.add(Primitive(
            kind=segment["kind"], sube="DRIVER", attrs=attrs,
            east=east, north=north, up=shaft_u,
            ori=f"ORI Z is {wet_end} and Y is U",
            note=f"motor {segment['role']}: engine_shaft CSV"))
        if segment["role"] == "main stator barrel":
            main_primitive = primitive
        emitted_segments.append({
            **segment, "start": cursor, "end": cursor + length,
            "east": east, "north": north,
        })
        cursor += length

    if abs(cursor - motor_end_face) > 0.05:
        raise ValueError(
            f"{model.tag}: motor segments end at {cursor}, expected {motor_end_face}")
    model.facts["motor_segments"] = emitted_segments
    model.facts["motor_axis_span"] = (motor_start, motor_end_face)

    # ---- measured three-part drive shaft or MC close coupling ----------
    casing_along = _along(
        casing_e, casing_n, plate_e, plate_n, wet_vector)
    casing_back = casing_along - casing_len / 2
    shaft_total = engine.get("shaft_total_L_mm")
    if shaft_total is None:
        gap = casing_back - motor_end_face
        if gap > 0.5:
            centre = motor_end_face + gap / 2
            model.add(Primitive(
                kind="CYLINDER", sube="BEARING",
                attrs={"DIAM": casing_dia * REF["bearing_dia"], "HEIG": gap},
                east=plate_e + wet_vector[0] * centre,
                north=plate_n + wet_vector[1] * centre,
                up=shaft_u, ori=f"ORI Z is {wet_end} and Y is U",
                note="close-coupled MC lantern: spans motor to casing"))
            model.reference_values.append(
                "MC close-coupled lantern diameter proportioned from /P1501B")
        model.facts["shaft"] = "N/A -- close-coupled MC arrangement"
        model.facts["drive_span"] = (motor_end_face, max(motor_end_face, casing_back))
    else:
        source_parts = [
            ("cylinder 1", "CYLINDER", engine.get("shaft_cyl1_L_mm"),
             engine.get("shaft_cyl1_D_mm"), None),
            ("cylinder 2", "CYLINDER", engine.get("shaft_cyl2_L_mm"),
             engine.get("shaft_cyl2_D_mm"), None),
            ("pump-side frustum", "CONE", engine.get("shaft_frust3_L_mm"),
             engine.get("shaft_frust3_D_min_mm"),
             engine.get("shaft_frust3_D_max_mm")),
        ]
        if any(length is None or diameter is None
               for _, _, length, diameter, _ in source_parts):
            model.unresolved.append(
                "drive-shaft segment data incomplete; free shaft not emitted")
            model.facts["shaft"] = "unresolved -- incomplete segment data"
        else:
            source_sum = sum(float(part[2]) for part in source_parts)
            if abs(source_sum - shaft_total) > 0.51:
                model.unresolved.append(
                    f"CONFLICT: shaft parts total {source_sum:.1f} mm against "
                    f"shaft_total {shaft_total:.1f} mm; part ratios retained")

            shaft_offset = engine.get("shaft_axial_offset_mm")
            natural_end = (abs(shaft_offset) + shaft_total / 2
                           if shaft_offset is not None else casing_back)
            engagement = min(max(casing_len * 0.15, 10.0), 40.0)
            target_end = min(max(natural_end, casing_back + engagement),
                             casing_along)
            target_span = target_end - motor_end_face
            if target_span <= 1.0:
                target_end = max(casing_back, motor_end_face + 1.0)
                target_span = target_end - motor_end_face
            fit_scale = target_span / source_sum
            if not 0.5 <= fit_scale <= 1.5:
                model.unresolved.append(
                    f"CONFLICT: shaft structural fit scale {fit_scale:.3f} "
                    f"outside preferred 0.5..1.5 range")

            cursor = motor_end_face
            drive_segments = []
            for role, kind, source_length, first_dia, second_dia in source_parts:
                length = float(source_length) * fit_scale
                centre = cursor + length / 2
                if kind == "CONE":
                    attrs = {"DBOT": float(first_dia),
                             "DTOP": float(second_dia), "HEIG": length}
                else:
                    attrs = {"DIAM": float(first_dia), "HEIG": length}
                model.add(Primitive(
                    kind=kind, sube="DRIVE_SHAFT", attrs=attrs,
                    east=plate_e + wet_vector[0] * centre,
                    north=plate_n + wet_vector[1] * centre,
                    up=shaft_u, ori=f"ORI Z is {wet_end} and Y is U",
                    note=f"drive shaft {role}: measured shape, axial fit "
                         f"{fit_scale:.4f}"))
                drive_segments.append({
                    "role": role, "kind": kind,
                    "source_length": float(source_length), "length": length,
                    "start": cursor, "end": cursor + length,
                    "diameter_1": float(first_dia),
                    "diameter_2": (float(second_dia)
                                   if second_dia is not None else None),
                })
                cursor += length

            model.facts["drive_segments"] = drive_segments
            model.facts["drive_span"] = (motor_end_face, target_end)
            model.facts["shaft_fit_scale"] = fit_scale
            model.facts["shaft_source_total"] = shaft_total
            model.facts["shaft"] = (
                f"three-part drive shaft, source {shaft_total:.1f} mm, "
                f"structural axial fit {fit_scale:.4f}")
            if abs(fit_scale - 1.0) > 0.01:
                model.reference_values.append(
                    f"drive-shaft axial lengths uniformly fitted by "
                    f"{fit_scale:.4f} to close motor/casing interfaces; "
                    f"source diameters and part ratios retained")

    # Cooling ribs: axial ribs on the full 360 degrees, as /P1501B builds them
    # and as the client required.  Each overlaps the stator and projects
    # beyond it.
    if main_primitive is None:
        raise ValueError(f"{model.tag}: motor main barrel was not resolved")
    main_dia = main_primitive.attrs["DIAM"]
    main_len = main_primitive.attrs["HEIG"]
    rib_radial = main_dia * REF["rib_radial"]
    rib_thick = main_dia * REF["rib_thick"]
    radius = main_dia / 2
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
            rib_e = main_primitive.east + offset_tran
            rib_n = main_primitive.north
        else:
            rib_e = main_primitive.east
            rib_n = main_primitive.north + offset_tran

        # IR-3a: a rectangular plate on a circular body must rotate with its
        # radial bearing.  The rib is expressed in its OWN frame -- local X
        # radial, local Y along the machine, local Z tangential -- and the
        # rotation is carried by ORI, not by swapping world-aligned lengths.
        model.add(Primitive(
            kind="BOX", sube="DRIVER",
            attrs={"XLEN": rib_radial, "YLEN": main_len, "ZLEN": rib_thick},
            east=rib_e, north=rib_n, up=shaft_u + offset_up,
            ori=_rib_ori(long_axis, math.degrees(angle)),
            note=f"cooling rib {index + 1}/{RIB_COUNT} at "
                 f"{math.degrees(angle):.0f} deg"))
    model.reference_values.append(
        f"{RIB_COUNT} axial cooling ribs, 360-degree distribution (/P1501B)")

    # Terminal box on the motor crown, and its electrical connection.  It is
    # seated so its underside overlaps the stator surface rather than hovering
    # above the rib tips, which would leave it detached from the machine.
    box = main_dia * REF["terminal_box"]
    box_height = box * 0.6
    crown = shaft_u + main_dia / 2
    box_centre_u = crown + box_height / 2 - box_height * 0.25
    model.add(Primitive(
        kind="BOX", sube="DRIVER",
        attrs={"XLEN": box, "YLEN": box, "ZLEN": box_height},
        east=main_primitive.east, north=main_primitive.north, up=box_centre_u,
        note="terminal box: proportion from /P1501B, seated on the stator"))
    model.reference_values.append("terminal box proportioned from /P1501B")

    model.add(Primitive(
        kind="ELCONN", sube="DRIVER",
        attrs={}, east=main_primitive.east, north=main_primitive.north,
        up=box_centre_u + box_height / 2,
        note="electrical connection"))

    # The motor's support chain is built by _build_machine_support alongside
    # the casing's, so both use the same reference construction.
    model.facts["motor_support"] = {
        "centre_e": motor_e, "centre_n": motor_n,
        "bearing_top": shaft_u - motor_dia * 0.42,
        "width": motor_dia * 0.85,
        "length": motor_len * 0.46,
        "diameter": motor_dia,
        "barrel_length": motor_len,
        # The stator's full length, which the mounting feet must straddle.
        "span": motor_len,
    }


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

    Plan position and direction are reproduced exactly.  The r9 emitted
    flange-face U and CATR remain fixed in r12.  Only an upward nozzle's HEIG
    changes: small nozzles penetrate the crown with at least 70% outside;
    overwidth nozzles begin exactly at the reducer upper face.
    """
    catr = {n.name: n.catr for n in location.nozzles}

    for row in (suction, discharge):
        if row is None:
            continue
        letter = row["letter"]
        east = row["pos"]["east"]
        north = row["pos"]["north"]
        up = row["pos"]["up"]
        heig = row["heig"] or 150.0
        note = "plan position and direction preserved exactly"

        if letter == "U":
            # The nozzle POS is its flange face (IR-9a). Preserve that face,
            # then solve HEIG from the required bottom-face connection.
            crown = shaft_u + casing_dia / 2
            wanted = _top_nozzle_face_u(row, crown)
            if abs(wanted - up) > 1.0:
                note = (f"Z adjusted {up:.1f} -> {wanted:.1f} so the flange "
                        f"face clears the casing crown at {crown:.1f}")
                model.facts.setdefault("nozzle_z_adjustments", []).append(
                    f"{row['role']}: {up:.1f} -> {wanted:.1f}")
                up = wanted
            resolution = _top_nozzle_resolution(row, crown, casing_len)
            root_u = (resolution["nozzle_root_u"] if resolution else
                      _top_nozzle_interface_u(crown))
            heig = up - root_u
            old_heig = row["heig"] or 150.0
            model.facts.setdefault("top_nozzle_heig_adjustments", []).append(
                f"{row['role']}: {old_heig:.1f} -> {heig:.1f} mm; root U {root_u:.1f}")
            if resolution and not resolution["overwidth"]:
                note += "; HEIG adapted for at least 70% direct casing projection"
            else:
                note += "; HEIG adapted for exact bottom-to-reducer contact"
        else:
            # A horizontal nozzle stays on the shaft centreline.
            if abs(up - shaft_u) > 1.0:
                note = f"Z adjusted {up:.1f} -> {shaft_u:.1f} onto the shaft centreline"
                model.facts.setdefault("nozzle_z_adjustments", []).append(
                    f"{row['role']}: {up:.1f} -> {shaft_u:.1f}")
                up = shaft_u

        model.add(Primitive(
            kind="NOZZLE", sube=row["role"],
            attrs={"HEIG": heig},
            east=east, north=north, up=up,
            ori=f"ORI P1 IS {letter}",
            name=f"{model.element}_{row['role']}_NOZZLE",
            catr=catr.get(row["name"]),
            note=note))


def main() -> int:
    """
    Write the single combined macro.

    The client asked for the combined file only, so no per-tag
    macros are emitted.  It still contains one independent ``EQUI`` per pump,
    never a shared equipment hierarchy.
    """
    sources = load_all()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    models = [build_pump(tag, sources) for tag in sorted(sources["location"])]

    combined = (OUTPUT_DIR /
                "JK_Pump_Build_2026-08-20_top_nozzle_r12_all_pumps.pml")
    combined.write_text(
        "-- JK_Pump_Build -- all pumps, 2026-08-20 top-nozzle width branches r12\n"
        "-- One independent EQUI per pump.\n"
        + "\n".join(m.to_pml() for m in models), encoding="utf-8")

    total = sum(len(m.primitives) for m in models)
    print(f"Wrote {combined}")
    print(f"  {len(models)} pumps, {total} elements")
    for model in models:
        print(f"  {model.tag:<12} {len(model.primitives):>4} elements  "
              f"{len(model.unresolved)} unresolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
