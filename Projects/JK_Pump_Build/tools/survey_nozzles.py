"""
Survey the nozzle schedule that must be preserved exactly.

The client's hard constraint is that every nozzle's plan (E/N) position and its
direction are carried over unchanged; only the U elevation may move, and only
to make a sound physical connection to the casing.

Direction is the subtle part.  A native E3D listing writes ``ORI Y is .. and
Z is ..`` -- the axis triad E3D *derived*, not the ``ORI P1 IS <dir>`` command
that aimed the nozzle (IR-2).  The 2026-08-18 /P1501B job proved that reading
the bore off that line gets it wrong.  Here the triad is decoded properly: for
a NOZZLE, P1 (the bore) runs along the element's local **Y** axis, so the bore
direction is exactly the axis named by the ``Y is ..`` clause.  That decoding
is then cross-checked geometrically against the baseplate centre -- a suction
or discharge nozzle must point *outward*, away from the machine it serves.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all  # noqa: E402

#: Unit vector for each E3D axis letter, in world E/N/U.
AXIS = {
    "E": (1.0, 0.0, 0.0), "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0), "S": (0.0, -1.0, 0.0),
    "U": (0.0, 0.0, 1.0), "D": (0.0, 0.0, -1.0),
}


def bore_axis(ori: str) -> str:
    """
    The bore direction letter from an exported ``ORI Y is <a> and Z is <b>``.

    A NOZZLE's P1 points along its local +Y, so the ``Y is`` clause names the
    bore.  Anything else in the line is the roll reference and is ignored.
    """
    if not ori:
        return "?"
    tokens = ori.replace(" and ", " ").split()
    for index, token in enumerate(tokens):
        if token.upper() == "Y" and index + 2 < len(tokens) \
                and tokens[index + 1].lower() == "is":
            return tokens[index + 2].upper()
    return "?"


def main() -> int:
    data = load_all()
    location = data["location"]

    print(f"{'tag':<12} {'nozzle':<10} {'E':>10} {'N':>10} {'U':>8} "
          f"{'HEIG':>7} {'bore':>5} {'outward':>8}  CATR")
    disagree = []
    for tag in sorted(location):
        pump = location[tag]
        plate = pump.baseplate
        if plate is None or plate.pos is None:
            continue
        centre_e, centre_n = plate.pos["east"], plate.pos["north"]

        for nozzle in pump.nozzles:
            if nozzle.pos is None:
                continue
            kind = "SUCTION" if "SUCTION" in (nozzle.name or "") else "DISCH"
            letter = bore_axis(nozzle.ori or "")
            vector = AXIS.get(letter, (0.0, 0.0, 0.0))

            # A nozzle must face away from the machine: the component of its
            # aim along (nozzle - plate centre) should not be negative.
            delta_e = nozzle.pos["east"] - centre_e
            delta_n = nozzle.pos["north"] - centre_n
            radial = delta_e * vector[0] + delta_n * vector[1]
            if abs(vector[2]) > 0.5:
                verdict = "up/down"          # a crown discharge is fine
            elif radial > 1.0:
                verdict = "yes"
            elif radial < -1.0:
                verdict = "INWARD"
                disagree.append((tag, nozzle.name, letter, radial))
            else:
                verdict = "tangent"

            catr = (nozzle.catr or "").split("/")[-1]
            print(f"{tag:<12} {kind:<10} {nozzle.pos['east']:>10.1f} "
                  f"{nozzle.pos['north']:>10.1f} {nozzle.pos['up']:>8.1f} "
                  f"{nozzle.attrs.get('HEIG', 0):>7.1f} {letter:>5} "
                  f"{verdict:>8}  {catr}")

    print(f"\nNozzles aimed inward (needs review): {len(disagree)}")
    for tag, name, letter, radial in disagree:
        print(f"  {tag} {name} bore={letter} radial={radial:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
