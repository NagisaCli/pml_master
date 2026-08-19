"""
Recover each nozzle's true bore direction geometrically.

Why this is needed
------------------
A native E3D listing writes ``ORI Y is .. and Z is ..`` -- the axis triad E3D
derived, not the ``ORI P1 IS <dir>`` command that aimed the nozzle (IR-2).  The
/P1501B job in this project already proved that reading a bore off that line
gets it wrong.

Here the evidence is even sharper.  All 28 discharge nozzles that carry an ORI
share ONE triad, ``Y is N and Z is E``, across pumps whose plan axes run both
North-South and East-West.  A constant triad cannot encode 28 different
physical directions, so it is not the bore.  The direction must therefore be
recovered from geometry, and this script does it by testing each candidate
direction against the pump's own body:

* the suction bore should run along the pump's longitudinal axis, outward past
  the end of the baseplate;
* a discharge sitting well above the shaft centreline is a crown (top)
  discharge and its bore is Up.

Each candidate is scored on physical evidence and the winner is printed with
the reason, so no direction is adopted silently.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_project_data import load_all  # noqa: E402

CANDIDATES = {
    "E": (1.0, 0.0, 0.0), "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0), "S": (0.0, -1.0, 0.0),
    "U": (0.0, 0.0, 1.0),
}

#: Client-confirmed suction directions recorded in ``DO.txt`` (2026-07-29) for
#: the two East-West MC pumps.  Kept as data, not buried in a branch, so the
#: override is visible and can be revised if the client revises the layout.
CLIENT_CONFIRMED_SUCTION = {
    "205-PU-018": "S",
    "205-PU-038": "S",
}


def classify(tag, pump):
    """Return the recovered geometry for one pump's two nozzles."""
    plate = pump.baseplate
    centre_e, centre_n = plate.pos["east"], plate.pos["north"]
    xlen, ylen = plate.attrs["XLEN"], plate.attrs["YLEN"]
    plate_top = plate.pos["up"] + plate.attrs["ZLEN"] / 2

    # The longitudinal axis is the plate's long side.
    longitudinal = "N" if ylen >= xlen else "E"
    half_long = (ylen if longitudinal == "N" else xlen) / 2
    half_tran = (xlen if longitudinal == "N" else ylen) / 2

    results = []
    for nozzle in pump.nozzles:
        if nozzle.pos is None:
            continue
        role = "SUCTION" if "SUCTION" in (nozzle.name or "") else "DISCHARGE"
        delta_e = nozzle.pos["east"] - centre_e
        delta_n = nozzle.pos["north"] - centre_n
        height = nozzle.pos["up"] - plate_top

        along = delta_n if longitudinal == "N" else delta_e
        across = delta_e if longitudinal == "N" else delta_n

        # How far out along each axis does the nozzle sit, as a fraction of
        # the plate half-extent?  A nozzle at or beyond the plate end is an
        # end connection; one near the centre line is not.
        along_frac = along / half_long if half_long else 0.0
        across_frac = across / half_tran if half_tran else 0.0

        if role == "SUCTION" and tag in CLIENT_CONFIRMED_SUCTION:
            # DO.txt records a client confirmation for the two E-W MC pumps:
            # suction points South, discharge West, sharing one elevation.
            # Their suction sits beyond the plate edge on BOTH plan axes
            # (-1.09 E and -1.06 N for 205-PU-018), so the outward-fraction
            # test is a near-tie there and cannot be trusted to break it.
            # A recorded client confirmation outranks the geometric heuristic.
            letter = CLIENT_CONFIRMED_SUCTION[tag]
            basis = "client-confirmed (DO.txt 2026-07-29): E-W MC pump, suction South"
        elif role == "SUCTION":
            # End suction: the bore runs outward along the longitudinal axis,
            # on whichever side of centre the nozzle sits.
            if abs(along_frac) >= abs(across_frac):
                letter = ("N" if along > 0 else "S") if longitudinal == "N" \
                    else ("E" if along > 0 else "W")
                basis = f"end suction, {along_frac:+.2f} of plate half-length"
            else:
                letter = ("E" if across > 0 else "W") if longitudinal == "N" \
                    else ("N" if across > 0 else "S")
                basis = f"side suction, {across_frac:+.2f} of plate half-width"
        else:
            # A discharge is a crown (top) discharge only if it actually
            # stands above the machine.  Where suction and discharge share one
            # elevation the discharge is horizontal instead, and its bore runs
            # outward along whichever plan axis carries its offset -- the
            # arrangement DO.txt records for the E-W MC pumps 205-PU-018/038.
            suction_up = next(
                (n.pos["up"] for n in pump.nozzles
                 if n.pos and "SUCTION" in (n.name or "")), None)
            horizontal = suction_up is not None and abs(nozzle.pos["up"] - suction_up) < 1.0

            if horizontal:
                if abs(delta_e) >= abs(delta_n):
                    letter = "E" if delta_e > 0 else "W"
                else:
                    letter = "N" if delta_n > 0 else "S"
                basis = (f"horizontal discharge, shares suction elevation "
                         f"U {nozzle.pos['up']:.1f}; plan offset "
                         f"dE{delta_e:+.0f}/dN{delta_n:+.0f}")
            else:
                letter = "U"
                basis = (f"top discharge, {height:.0f} mm above plate top, "
                         f"plan offset {along_frac:+.2f}L/{across_frac:+.2f}W")

        results.append({
            "role": role, "name": nozzle.name, "letter": letter,
            "basis": basis, "pos": nozzle.pos,
            "heig": nozzle.attrs.get("HEIG"), "catr": nozzle.catr,
            "longitudinal": longitudinal, "height_above_plate": height,
        })
    return results


def main() -> int:
    location = load_all()["location"]
    print(f"{'tag':<12} {'role':<10} {'bore':>4} {'H above plate':>14}  basis")
    counts = {}
    for tag in sorted(location):
        for row in classify(tag, location[tag]):
            counts[(row["role"], row["letter"])] = \
                counts.get((row["role"], row["letter"]), 0) + 1
            print(f"{tag:<12} {row['role']:<10} {row['letter']:>4} "
                  f"{row['height_above_plate']:>14.1f}  {row['basis']}")
    print("\nRecovered direction census:")
    for (role, letter), count in sorted(counts.items()):
        print(f"  {role:<10} {letter}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
