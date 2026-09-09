"""
Mutation-test the verifier.

A verifier that passes everything is indistinguishable from a verifier that
checks nothing.  This project has already been burned twice by that: the
2026-08-18 post-mortem records a verifier that passed a visibly broken model
because every check restated the generator's own premise.

So each mutation below injects one defect that a reviewer would call obviously
wrong, and the run FAILS if the verifier does not catch it.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all      # noqa: E402
from build_pumps import build_pump              # noqa: E402
from verify_pumps import bounds, verify         # noqa: E402
from check_base_shape import check as check_base_shape  # noqa: E402
from base_deform import parse_reference         # noqa: E402

TAG = "203-PU-011"


def mutate_baseplate_size(model):
    plate = next(p for p in model.primitives
                 if "element 40:" in p.note)
    plate.attrs["XLEN"] += 250.0
    return "reference centre plate widened by 250 mm"


def mutate_duplicate_baseplate(model):
    plate = copy.deepcopy(next(p for p in model.primitives
                               if "element 40:" in p.note))
    plate.sube = "BASEPLATE"
    model.primitives.append(plate)
    return "old full baseplate emitted in addition to the reference base"


def mutate_compress_pump_station(model):
    barrel = next(p for p in model.primitives
                  if p.sube == "CASING" and p.kind == "CYLINDER")
    machine_bottom = barrel.up - barrel.attrs["DIAM"] / 2
    changed = False
    for primitive in model.primitives:
        if "(pump station)" not in primitive.note:
            continue
        if (primitive.kind == "PYRAMID"
                and bounds(primitive)[2][1] > machine_bottom):
            low = bounds(primitive)[2][0]
            high = max(machine_bottom, low + 1.0)
            primitive.attrs["HEIG"] = high - low
            primitive.up = (low + high) / 2
            changed = True
    return ("pump saddle compressed to the casing underside, losing reference penetration"
            if changed else None)


def mutate_distort_hex(model):
    washer = next((p for p in model.primitives
                   if p.kind == "EXTRUSION" and p.sube == "BASE"), None)
    if washer is None:
        return None
    washer.profile = [(x * 1.8, y) for x, y in washer.profile]
    return "hex washer anisotropically stretched into a non-reference profile"


def mutate_shift_motor_station(model):
    moved = False
    for primitive in model.primitives:
        if "(motor station)" in primitive.note:
            primitive.north += 140.0
            moved = True
    return "motor support station shifted away from its motor" if moved else None


def mutate_swap_gusset_axes(model):
    gusset = next((p for p in model.primitives
                   if p.kind == "PYRAMID" and p.sube == "BASE"), None)
    if gusset is None:
        return None
    gusset.attrs["XBOT"], gusset.attrs["YBOT"] = (
        gusset.attrs["YBOT"], gusset.attrs["XBOT"])
    return "gusset local X/Y dimensions swapped as if they were world axes"


def mutate_mirror_pyramid_positions(model):
    """Reproduce the E3D-visible r2 defect: positions mirrored, ORIs unchanged."""
    wet = model.facts["wet_end"]
    along = {"N": (0.0, 1.0), "S": (0.0, -1.0),
             "E": (1.0, 0.0), "W": (-1.0, 0.0)}[wet]
    across = (along[1], -along[0])
    plate_e, plate_n = model.facts["plate_centre"]
    changed = False
    for member in model.primitives:
        if member.sube != "BASE" or member.kind != "PYRAMID":
            continue
        offset = ((member.east - plate_e) * across[0]
                  + (member.north - plate_n) * across[1])
        member.east -= 2 * offset * across[0]
        member.north -= 2 * offset * across[1]
        changed = True
    return ("all PYRAMID positions mirrored while their local ORIs stay fixed"
            if changed else None)


def mutate_shift_hex_off_anchor(model):
    washer = next((p for p in model.primitives
                   if p.kind == "EXTRUSION" and p.sube == "BASE"), None)
    if washer is None:
        return None
    washer.east += 35.0
    return "hex head shifted 35 mm away from its anchor shaft"


def mutate_nozzle_plan(model):
    nozzle = next(p for p in model.primitives if p.kind == "NOZZLE")
    nozzle.east += 120.0
    return "nozzle moved 120 mm in plan"


def mutate_casing_diameter(model):
    barrel = next(p for p in model.primitives
                  if p.sube == "CASING" and p.kind == "CYLINDER")
    barrel.attrs["DIAM"] *= 0.8
    return "casing diameter shrunk 20%"


def mutate_break_coaxial(model):
    motor = max((p for p in model.primitives if p.sube == "DRIVER"
                 and p.kind == "CYLINDER"), key=lambda p: p.attrs.get("HEIG", 0))
    motor.up += 180.0
    return "motor lifted 180 mm off the shaft centreline"


def mutate_sink_below_foundation(model):
    barrel = next(p for p in model.primitives
                  if p.sube == "CASING" and p.kind == "CYLINDER")
    barrel.up -= 400.0
    return "casing sunk 400 mm below the foundation"


def mutate_float_part(model):
    shaft = next(p for p in model.primitives if p.sube == "DRIVE_SHAFT")
    shaft.up += 900.0
    shaft.east += 900.0
    return "drive-shaft segment detached into mid-air"


def mutate_restore_driver_dish(model):
    """Re-introduce the forbidden generic end DISH in the measured driver."""
    cone = next((p for p in model.primitives
                 if p.sube == "DRIVER" and p.kind == "CONE"), None)
    if cone is None:
        return None
    cone.kind = "DISH"
    cone.attrs = {"DIAM": max(cone.attrs["DBOT"], cone.attrs["DTOP"]),
                  "HEIG": cone.attrs["HEIG"],
                  "RADI": max(cone.attrs["DBOT"], cone.attrs["DTOP"])}
    return "measured motor end CONE replaced by a generic DISH"


def mutate_open_drive_interface(model):
    """Open an axial gap inside the measured three-part drive shaft."""
    parts = [p for p in model.primitives if p.sube == "DRIVE_SHAFT"]
    if len(parts) < 2:
        return None
    wet = model.facts["wet_end"]
    vector = {"N": (0.0, 1.0), "S": (0.0, -1.0),
              "E": (1.0, 0.0), "W": (-1.0, 0.0)}[wet]
    parts[1].east += vector[0] * 60.0
    parts[1].north += vector[1] * 60.0
    return "60 mm axial gap opened between drive-shaft segments"


def mutate_wrong_motor_cone_ratio(model):
    """Make one outward motor-cone face too large and break end symmetry."""
    cone = next((p for p in model.primitives
                 if p.sube == "DRIVER" and "rear frustum" in p.note), None)
    if cone is None:
        return None
    cone.attrs["DBOT"] *= 1.25
    return "rear motor CONE outward face widened beyond the 2/3 rule"


def mutate_motor_tail_to_cylinder(model):
    """Reproduce r8: the physical motor tail is not a frustum."""
    cone = next((p for p in model.primitives
                 if p.sube == "DRIVER" and "rear frustum" in p.note), None)
    if cone is None:
        return None
    cone.kind = "CYLINDER"
    cone.attrs = {"DIAM": cone.attrs["DBOT"], "HEIG": cone.attrs["HEIG"]}
    cone.note = "motor rear terminal incorrectly rebuilt as CYLINDER"
    return "motor tail terminal changed from CONE to CYLINDER"


def mutate_unbind_nozzle(model):
    nozzle = next(p for p in model.primitives if p.kind == "NOZZLE")
    nozzle.catr = None
    return "nozzle catalogue binding removed (would render nothing)"


def mutate_bury_discharge(model):
    nozzle = next((p for p in model.primitives
                   if p.kind == "NOZZLE" and p.ori.endswith("U")), None)
    if nozzle is None:
        return None
    nozzle.up -= 500.0
    return "top discharge buried 500 mm into the casing"


def mutate_remove_top_connection(model):
    victims = [p for p in model.primitives
               if p.note.startswith("top discharge casing connection")]
    if not victims:
        return None
    for victim in victims:
        model.primitives.remove(victim)
    return "all primitive casing connectors removed below the up nozzle"


def mutate_open_top_connection_interface(model):
    reducer = next((p for p in model.primitives
                    if "top discharge casing connection: overwidth smooth reducer"
                    in p.note), None)
    if reducer is None:
        return None
    reducer.up += 30.0
    return "30 mm gap opened between the lower socket and reducer/nozzle root"


def mutate_widen_top_connection_socket(model):
    socket = next((p for p in model.primitives
                   if "top discharge casing connection: overwidth lower socket"
                   in p.note), None)
    if socket is None:
        return None
    socket.attrs["DIAM"] *= 2.0
    return "top-nozzle lower socket widened beyond the casing axial width"


def mutate_overlap_nozzle_root_with_connector(model):
    """Reproduce r10: preserve the face but extend the nozzle through the boss."""
    nozzle = next((p for p in model.primitives
                   if p.kind == "NOZZLE" and p.ori.endswith(" U")), None)
    if nozzle is None:
        return None
    nozzle.attrs["HEIG"] += 100.0
    return "native nozzle HEIG extended 100 mm through the connector upper face"


def mutate_remove_offset_bridge(model):
    bridge = next((p for p in model.primitives
                   if p.note.startswith("top discharge casing offset bridge")), None)
    if bridge is None:
        return None
    model.primitives.remove(bridge)
    return "offset top nozzle left without its solid casing bridge"


def mutate_reduce_direct_nozzle_external_ratio(model):
    nozzle = next((p for p in model.primitives
                   if p.kind == "NOZZLE" and p.ori.endswith(" U")), None)
    if nozzle is None:
        return None
    nozzle.attrs["HEIG"] *= 2.0
    return "direct top nozzle external projection reduced below 70 percent"


def mutate_absurd_heig(model):
    nozzle = next(p for p in model.primitives if p.kind == "NOZZLE")
    nozzle.attrs["HEIG"] = 42000.0
    return "nozzle HEIG set to 42 m"


def mutate_float_hex_washer(model):
    washer = next((p for p in model.primitives if p.kind == "EXTRUSION"), None)
    if washer is None:
        return None
    washer.up += 700.0
    return "hex washer lifted 700 mm off its sole plate"


def mutate_float_gusset(model):
    gusset = next((p for p in model.primitives if p.kind == "PYRAMID"), None)
    if gusset is None:
        return None
    gusset.east += 1200.0
    return "gusset displaced 1200 mm off the pedestal"


def mutate_seat_machine_on_plate(model):
    """
    The 2026-08-19 support regression: seat the machine flat on the baseplate
    so there is no room for a support chain, and shrink the pedestal to the
    sliver that produced.  Connectivity and foundation checks both pass on
    this, which is exactly why it shipped.
    """
    plate_top = model.facts["plate_top"]
    machine = [p for p in model.primitives
               if p.sube in ("CASING", "DRIVER", "BEARING", "COUPLING",
                             "DRIVE_SHAFT")]
    if not machine:
        return None
    lowest = min(p.up - p.attrs.get("DIAM", 0) / 2 for p in machine)
    drop = lowest - plate_top
    for primitive in machine:
        primitive.up -= drop
    for primitive in model.primitives:
        if primitive.sube == "BASE":
            # Crush the base down onto the plate, as the rejected revision did.
            primitive.up = min(primitive.up, plate_top + 10.0)
    return "machine seated flat on the plate, pedestal crushed to 10 mm"


def mutate_sink_skid_rail(model):
    rail = next((p for p in model.primitives
                 if p.sube == "BASE" and p.kind == "BOX"), None)
    if rail is None:
        return None
    rail.up -= 300.0
    return "base rail sunk 300 mm below the baseplate"


def mutate_slab_thickness(model):
    """
    The 2026-08-19 rejected render: base members scaled off plate WIDTH.

    On a wide pump that made every plate ~3x too thick -- 72 mm sole plates and
    a 130 mm foot pad on a 50 mm baseplate -- which reads as stacked slabs.
    Every positional check passed it, because none asked whether a plate still
    looked like a plate.
    """
    hit = False
    for primitive in model.primitives:
        if primitive.sube == "BASE" and primitive.kind == "BOX":
            primitive.attrs["ZLEN"] *= 3.5
            hit = True
    return "base member thicknesses scaled 3.5x into slabs" if hit else None


def mutate_anchor_through_foundation(model):
    """Drive the anchor bolts out through the underside of the baseplate."""
    bolts = [p for p in model.primitives if "anchor bolt" in p.note]
    if not bolts:
        return None
    for bolt in bolts:
        bolt.up -= 120.0
    return "anchor bolts driven through the foundation"


def mutate_lift_machine_off_pad(model):
    """
    The 2026-08-19 render defect: the machine floats above its mounting.

    This is what the client saw twice -- everything touches *something*, and
    nothing is below the foundation, so only a pad-to-machine seating check
    finds it.
    """
    for primitive in model.primitives:
        if primitive.sube in ("CASING", "DRIVER", "BEARING", "COUPLING",
                              "DRIVE_SHAFT"):
            primitive.up += 90.0
    return "machine lifted 90 mm off its foot pads"


def mutate_shrink_foot_pad(model):
    """Shrink a foot pad so the machine overhangs its own mounting."""
    pad = next((p for p in model.primitives
                if "mounting pad" in p.note), None)
    if pad is None:
        return None
    pad.attrs["XLEN"] *= 0.15
    pad.attrs["YLEN"] *= 0.15
    return "foot pad shrunk to 15%: the machine overhangs its mounting"


def mutate_remove_gussets(model):
    """Delete the gussets: the pad is then carried by nothing."""
    victims = [p for p in model.primitives if "gusset" in p.note]
    if not victims:
        return None
    for victim in victims:
        model.primitives.remove(victim)
    return "all gussets deleted: the foot pads have no support beneath"


def mutate_drop_base_member(model):
    """
    Delete one family of base members.

    This is the failure that reached the client three times: a support that
    passes every positional check but is not the reference structure.
    """
    victims = [p for p in model.primitives if "sole plate" in p.note]
    if not victims:
        return None
    for victim in victims:
        model.primitives.remove(victim)
    return "all sole plates deleted from the base load path"


def mutate_lift_sole_off_skid(model):
    """Open a vertical gap between one sole plate and the skid."""
    sole = next((p for p in model.primitives if "sole plate" in p.note), None)
    if sole is None:
        return None
    sole.up += 40.0
    return "sole plate lifted 40 mm off the skid"


def mutate_shorten_lower_gusset(model):
    """Keep a gusset's top but open a gap above its sole plate."""
    gusset = next((p for p in model.primitives
                   if "sole gusset" in p.note), None)
    if gusset is None or gusset.attrs.get("HEIG", 0.0) <= 40.0:
        return None
    gusset.up += 20.0
    gusset.attrs["HEIG"] -= 40.0
    return "lower gusset shortened 40 mm above its sole plate"


def mutate_stretch_hex_head(model):
    """Reproduce the shaft-height-scaled, oversized hex-head defect."""
    washer = next((p for p in model.primitives
                   if p.sube == "BASE" and p.kind == "EXTRUSION"), None)
    if washer is None:
        return None
    washer.attrs["HEIG"] *= 4.0
    return "hex head thickness stretched 4x by support height"


def mutate_shorten_inner_gusset_from_top(model):
    """Open the E3D-visible gap between an inner gusset and its top plate."""
    gusset = next((p for p in model.primitives
                   if "sole gusset" in p.note), None)
    if gusset is None or gusset.attrs.get("HEIG", 0.0) <= 40.0:
        return None
    gusset.up -= 20.0
    gusset.attrs["HEIG"] -= 40.0
    return "inner PYRA shortened 40 mm below its mounting top plate"


def mutate_float_outer_stay_base(model):
    """Keep an outer stay top but lift its base off the fixed sole plate."""
    stay = next((p for p in model.primitives
                 if "side stay" in p.note or "motor stay" in p.note), None)
    if stay is None or stay.attrs.get("HEIG", 0.0) <= 40.0:
        return None
    stay.up += 20.0
    stay.attrs["HEIG"] -= 40.0
    return "outer PYRA base lifted 40 mm off its fixed sole plate"


def mutate_use_pyramid_bottom_as_pos(model):
    """Reproduce r5: write intended bottom U directly into centre-datum POS."""
    stay = next((p for p in model.primitives
                 if "motor stay" in p.note), None)
    if stay is None:
        return None
    intended_bottom = bounds(stay)[2][0]
    stay.up = intended_bottom
    return "PYRAMID POS set to intended bottom instead of geometric centre"


MUTATIONS = [
    mutate_duplicate_baseplate,
    mutate_compress_pump_station,
    mutate_distort_hex,
    mutate_shift_motor_station,
    mutate_swap_gusset_axes,
    mutate_mirror_pyramid_positions,
    mutate_shift_hex_off_anchor,
    mutate_float_hex_washer,
    mutate_float_gusset,
    mutate_sink_skid_rail,
    mutate_drop_base_member,
    mutate_lift_sole_off_skid,
    mutate_shorten_lower_gusset,
    mutate_stretch_hex_head,
    mutate_shorten_inner_gusset_from_top,
    mutate_float_outer_stay_base,
    mutate_use_pyramid_bottom_as_pos,
    mutate_slab_thickness,
    mutate_anchor_through_foundation,
    mutate_lift_machine_off_pad,
    mutate_shrink_foot_pad,
    mutate_remove_gussets,
    mutate_seat_machine_on_plate,
    mutate_baseplate_size,
    mutate_nozzle_plan,
    mutate_casing_diameter,
    mutate_break_coaxial,
    mutate_restore_driver_dish,
    mutate_wrong_motor_cone_ratio,
    mutate_motor_tail_to_cylinder,
    mutate_open_drive_interface,
    mutate_sink_below_foundation,
    mutate_float_part,
    mutate_unbind_nozzle,
    mutate_bury_discharge,
    mutate_remove_top_connection,
    mutate_open_top_connection_interface,
    mutate_widen_top_connection_socket,
    mutate_overlap_nozzle_root_with_connector,
    mutate_absurd_heig,
]

SPECIAL_MUTATIONS = [
    ("205-PU-054", mutate_remove_offset_bridge),
    ("203-PU-008", mutate_reduce_direct_nozzle_external_ratio),
]
MUTATION_COUNT = len(MUTATIONS) + len(SPECIAL_MUTATIONS)


def main() -> int:
    sources = load_all()
    reference = parse_reference()
    baseline = build_pump(TAG, sources)
    problems = verify(baseline, sources) + check_base_shape(baseline, reference)
    if problems:
        print(f"BASELINE {TAG} does not pass cleanly:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"baseline {TAG}: clean\n")

    escaped = 0
    tested = 0
    for mutation in MUTATIONS:
        model = copy.deepcopy(baseline)
        label = mutation(model)
        if label is None:
            continue
        tested += 1
        found = verify(model, sources) + check_base_shape(model, reference)
        if found:
            print(f"[caught] {label}")
            print(f"         -> {found[0]}")
        else:
            print(f"[ESCAPED] {label}  <-- the verifier is blind to this")
            escaped += 1

    for tag, mutation in SPECIAL_MUTATIONS:
        model = build_pump(tag, sources)
        clean = verify(model, sources) + check_base_shape(model, reference)
        if clean:
            print(f"SPECIAL BASELINE {tag} does not pass cleanly: {clean[0]}")
            return 1
        label = mutation(model)
        if label is None:
            print(f"[ESCAPED] special mutation did not apply to {tag}")
            escaped += 1
            continue
        tested += 1
        found = verify(model, sources) + check_base_shape(model, reference)
        if found:
            print(f"[caught] {label}")
            print(f"         -> {found[0]}")
        else:
            print(f"[ESCAPED] {label}  <-- the verifier is blind to this")
            escaped += 1

    print(f"\n{tested} mutations, {escaped} escaped")
    if tested != MUTATION_COUNT:
        print(f"expected {MUTATION_COUNT} applied mutations")
        return 1
    return 1 if escaped else 0


if __name__ == "__main__":
    raise SystemExit(main())
