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
from verify_pumps import verify                 # noqa: E402

TAG = "203-PU-008"


def mutate_baseplate_size(model):
    plate = next(p for p in model.primitives if p.sube == "BASEPLATE")
    plate.attrs["XLEN"] += 250.0
    return "baseplate widened by 250 mm"


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
    bearing = next(p for p in model.primitives if p.sube == "BEARING")
    bearing.up += 900.0
    bearing.east += 900.0
    return "bearing housing detached into mid-air"


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
               if p.sube in ("CASING", "DRIVER", "BEARING", "COUPLING")]
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


def mutate_drop_base_member(model):
    """
    Delete one family of base members.

    This is the failure that reached the client three times: a support that
    passes every positional check but is not the reference structure.
    """
    victims = [p for p in model.primitives
               if p.sube == "BASE" and p.kind == "PYRAMID"]
    if not victims:
        return None
    for victim in victims[:4]:
        model.primitives.remove(victim)
    return "four PYRAMID gussets deleted from the reference base"


MUTATIONS = [
    mutate_float_hex_washer,
    mutate_float_gusset,
    mutate_sink_skid_rail,
    mutate_drop_base_member,
    mutate_seat_machine_on_plate,
    mutate_baseplate_size,
    mutate_nozzle_plan,
    mutate_casing_diameter,
    mutate_break_coaxial,
    mutate_sink_below_foundation,
    mutate_float_part,
    mutate_unbind_nozzle,
    mutate_bury_discharge,
    mutate_absurd_heig,
]


def main() -> int:
    sources = load_all()
    baseline = build_pump(TAG, sources)
    problems = verify(baseline, sources)
    if problems:
        print(f"BASELINE {TAG} does not pass cleanly:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"baseline {TAG}: clean\n")

    escaped = 0
    for mutation in MUTATIONS:
        model = copy.deepcopy(baseline)
        label = mutation(model)
        if label is None:
            continue
        found = verify(model, sources)
        if found:
            print(f"[caught] {label}")
            print(f"         -> {found[0]}")
        else:
            print(f"[ESCAPED] {label}  <-- the verifier is blind to this")
            escaped += 1

    print(f"\n{len(MUTATIONS)} mutations, {escaped} escaped")
    return 1 if escaped else 0


if __name__ == "__main__":
    raise SystemExit(main())
