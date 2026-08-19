"""
Scale the native E3D listing of /P1501B into a larger, same-shape pump /P1501C.

Why this tool exists
--------------------
The client supplied ``C:\\Users\\A\\Desktop\\Reference_pumps.txt``, a native
AVEVA E3D data listing of the accepted ``/P1501B`` "Reflux Pump - Standby",
and asked for another pump of a different size with the same shape and
structure.

Scaling rules (Reference decisions, reported to the client)
-----------------------------------------------------------
* One uniform similarity factor ``S = 1.30`` is applied to the whole machine,
  so the construction stays geometrically similar.  The 1390 x 510 mm
  baseplate becomes 1807 x 663 mm.

* This listing expresses every primitive ``POS`` in the **owning element's
  local frame** (the EQUI origin sits on the shaft centreline, not on the
  baseplate), so the scale is a plain multiply about that local origin --
  unlike the world-coordinate 205-PU-012 job, no plan centre offset is
  removed first.

* The scale is applied uniformly about the equipment origin, with **no**
  elevation re-datuming.  This equipment's origin sits on the SHAFT
  CENTRELINE -- the casing volute is centred on ``U 0`` and the ``/Motor``
  frame is offset ``U 0`` from it -- so a local ``U`` is an offset from that
  axis, not a height above the foundation.

  An earlier revision re-anchored elevations about the plate underside to
  stop the plate "sinking" from ``U -340`` to ``U -442``.  That was a
  misreading: the EQUI installation ``POS U 100645`` is the shaft-centreline
  elevation, so a larger pump legitimately carries its plate further below a
  fixed shaft height.  The re-anchoring instead sheared the machine -- it
  lifted the motor off the shaft axis while leaving the casing on it, and
  the client's E3D reload showed the coupling parted.

  The plate underside therefore lands 102 mm lower relative to the shaft
  than on ``/P1501B``.  That is a real civil/plinth consequence of fitting a
  bigger pump to the same shaft elevation and is reported to the client, not
  hidden by distorting the machine.

* Native ``NOZZLE`` elements keep ``CATR``, ``HEIG``, ``ORI``, TEMP/PRES/
  TPRESS and DUTY -- the flange is a catalogue item, not free geometry.
  Their flange faces are re-anchored the verified way: the barrel **root**
  is scaled with the machine and the unchanged ``HEIG`` is re-added along
  the aim direction, so a nozzle stays attached to the enlarged casing
  instead of floating ``(S - 1) * HEIG`` clear of it.

* ``RADI`` (DISH knuckle) scales with the machine.  ``XOFF``/``YOFF``
  (PYRAMID apex offsets) are true lengths in the local frame and scale too;
  leaving them fixed would shear every gusset as the pyramid grew.

* ``DESP`` design parameters are rewritten so the template's own parameter
  list still describes the delivered solid.  The two nozzle-bore entries
  (60.3 pipe OD and the 135 discharge offset) are handled per the nozzle
  rule -- 60.3 is a bore and stays, 135 is a position and scales.

* ``USRWEI``/``USRWWE`` (weights) scale by ``S**3``; ``USRCOG``/``USRWCO``
  (centre-of-gravity offsets) are lengths and scale by ``S``.

The tool is a mechanical rewrite: it transforms numbers line by line and
never reorders attributes or replaces the native INPUT listing form, so the
``ORI``-before-``POS`` order of the source (and the opposite order the
source uses on NOZZLE) is preserved exactly as E3D wrote it.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT / "output"
IMPORTS_DIR = PROJECT / "imports"

# The native export lives outside the repository, so it may be absent on
# another machine or after a cleanup.  Override with argv[1].
SOURCE = (
    Path(sys.argv[1]) if len(sys.argv) > 1
    else Path(r"C:\Users\A\Desktop\Reference_pumps.txt")
)

OLD_TAG = "/P1501B"
NEW_TAG = "/P1501C"
NEW_DESC = "'Reflux Pump - Standby (large frame)'"

S = Decimal("1.30")

# Source envelope, measured from the solids and confirmed by DESP 1/2.
OLD_LEN = Decimal("1390")
OLD_WID = Decimal("510")

# Baseplate underside in the EQUI local frame: the elevation scaling origin.
PLATE_BOTTOM = Decimal("-340")

SIGN = {"E": 1, "W": -1, "N": 1, "S": -1, "U": 1, "D": -1}
POS_AXES = (("E", "W"), ("N", "S"), ("U", "D"))

POS_RE = re.compile(
    r"^POS\s+([ENSWUD])\s+([-\d.]+)mm"
    r"\s+([ENSWUD])\s+([-\d.]+)mm"
    r"\s+([ENSWUD])\s+([-\d.]+)mm$"
)
# Every length attribute in this listing.  RADI/XOFF/YOFF are included
# deliberately: they are true lengths, not ratios.
DIM_RE = re.compile(
    r"^(XLEN|YLEN|ZLEN|DIAM|HEIG|RADI|XBOT|YBOT|XTOP|YTOP|XOFF|YOFF)"
    r"\s+([-\d.]+)mm$"
)
NEW_RE = re.compile(r"^NEW\s+([A-Z]+)(?:\s+(\S+))?$", re.IGNORECASE)

# Nozzle invariants.  ``root`` is the barrel attachment point on the machine
# in the EQUI local frame, ``aim`` is the local bore direction and ``heig`` is
# the unchanged catalogue projection, so  face = root + aim * heig.
#
# The bore axis is NOT read from the exported ``ORI Y is .. and Z is ..``
# line.  That is E3D's dump of the resulting axis triad, not the ``ORI P1 IS``
# command that aimed the nozzle, and the two do not correspond (IR-2).  Each
# axis below was instead recovered geometrically, by testing which candidate
# direction puts the barrel root on the casing.  The volute is a DIAM 340
# (r=170) cylinder about the origin spanning N -60..+60:
#
#   N1  aim N  -> root (0, 0, 0)        exactly the volute centre / impeller
#                                       eye; an end-suction inlet.  Aiming U
#                                       would leave the root at radius 155
#                                       outside the N span entirely.
#   N2  aim U  -> root (135, 0, 30)     radius 138.3 < 170, on the casing
#                                       crown.  Aiming E gives radius 239,
#                                       floating 69 mm clear of the casing.
#   N3  aim E  -> root (55, -5, 0)      radius 55, inside the body.
#
# Getting this wrong is the failure the previous scaling job documented: the
# flange face scales but the barrel does not reach the enlarged casing.
NOZZLES = {
    "/P1501B/N1": {
        "root": (Decimal("0"), Decimal("0"), Decimal("0")),
        "aim": (Decimal("0"), Decimal("1"), Decimal("0")),
        "heig": Decimal("155"),
    },
    "/P1501B/N2": {
        "root": (Decimal("135"), Decimal("0"), Decimal("30")),
        "aim": (Decimal("0"), Decimal("0"), Decimal("1")),
        "heig": Decimal("200"),
    },
    "/P1501B/N3": {
        "root": (Decimal("55"), Decimal("-5"), Decimal("0")),
        "aim": (Decimal("1"), Decimal("0"), Decimal("0")),
        "heig": Decimal("200"),
    },
}


def require_input(path: Path, what: str) -> Path:
    """Exit with an actionable message when an external input is absent."""
    if not path.exists():
        raise SystemExit(
            "Input not found: {0}\n"
            "  This script needs {1}.\n"
            "  That file is external to the repository and is not versioned.\n"
            "  Pass it explicitly:  python {2} <path>".format(
                path, what, Path(__file__).name
            )
        )
    return path


def q(value: Decimal) -> Decimal:
    """Round to the native listing's 0.01 mm precision, half away from zero."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def fmt(value: Decimal) -> str:
    """Format a length like the native listing (integers stay integer)."""
    value = q(value)
    if value == value.to_integral_value():
        return str(int(value))
    return str(value.normalize())


def scale_pos(vec):
    """Uniformly scale a local position about the equipment origin.

    There is deliberately no elevation re-datuming here.  This equipment's
    origin sits on the SHAFT CENTRELINE (the casing volute is centred on
    U 0 and the motor frame is offset U 0 from it), so a local ``U`` is an
    offset from that axis, not a height above the foundation.  Re-anchoring
    it about the plate underside shears the machine apart: it moved the
    motor off the shaft axis while leaving the casing on it.

    A similarity transform must be uniform about a single origin, or the
    parts stop fitting each other.
    """
    return tuple(v * S for v in vec)


def pos_line(vec) -> str:
    """Emit a POS line, choosing the sign letter the native form uses."""
    parts = []
    for value, (plus, minus) in zip(vec, POS_AXES):
        value = q(value)
        letter = plus if value >= 0 else minus
        parts.append(f"{letter} {fmt(abs(value))}mm")
    return "POS " + " ".join(parts)


def read_pos(match) -> tuple:
    """Decode a POS line into a signed (E, N, U) local vector."""
    vec = [Decimal(0)] * 3
    for letter, number in (
        (match.group(1), match.group(2)),
        (match.group(3), match.group(4)),
        (match.group(5), match.group(6)),
    ):
        value = Decimal(number) * SIGN[letter]
        index = 0 if letter in "EW" else (1 if letter in "NS" else 2)
        vec[index] = value
    return tuple(vec)


def nozzle_face(name: str) -> str:
    """Scale a nozzle's root, then re-add its unchanged catalogue projection."""
    spec = NOZZLES[name]
    root = scale_pos(spec["root"])
    aim, heig = spec["aim"], spec["heig"]
    return pos_line(tuple(root[i] + aim[i] * heig for i in range(3)))


def scale_bracketed(line: str) -> str:
    """Scale every ``( <number> mm )`` length inside a USRCOG/USRWCO line."""
    return re.sub(
        r"\(\s*([-\d.]+)\s*mm\s*\)",
        lambda m: f"( {fmt(Decimal(m.group(1)) * S)} mm )",
        line,
    )


def scale_weight(line: str) -> str:
    """Scale a ``( <number>kg )`` mass by the cube of the length factor."""
    return re.sub(
        r"\(\s*([-\d.]+)\s*kg\s*\)",
        lambda m: f"( {fmt(Decimal(m.group(1)) * S ** 3)}kg )",
        line,
    )


def transform_lines(lines):
    """Mechanical numeric rewrite of the INPUT listing body."""
    out = []
    stack = []
    nozzle_name = None
    in_despec = False
    dropped_crefs = []

    for line in lines:
        text = line.strip()

        # DESP is a continued parameter list ("... $" carries to the next
        # line).  Rewrite it so the template parameters still describe the
        # delivered solid.
        if text.startswith("DESP ") or in_despec:
            in_despec = text.endswith("$")
            def scale_desp(m):
                value = Decimal(m.group(0))
                # 60.3 is a pipe outside diameter tied to the unchanged
                # nozzle catalogue, so it is a bore, not a machine length.
                if value == Decimal("60.3"):
                    return m.group(0)
                return fmt(value * S)
            out.append(re.sub(r"[-\d.]+", scale_desp, line))
            continue

        new_match = NEW_RE.match(text)
        if new_match:
            element = new_match.group(1).upper()
            name = new_match.group(2)
            if element == "NOZZLE":
                nozzle_name = name
            stack.append(element)
            out.append(line.replace(OLD_TAG, NEW_TAG))
            continue

        if text == "END":
            if not stack:
                raise ValueError("unbalanced END in source listing")
            closed = stack.pop()
            if closed == "NOZZLE":
                nozzle_name = None
            out.append(line)
            continue

        if text.startswith("POS "):
            match = POS_RE.match(text)
            if not match:
                raise ValueError(f"unrecognised POS line: {text!r}")
            if "NOZZLE" in stack:
                if nozzle_name not in NOZZLES:
                    raise ValueError(f"unknown nozzle {nozzle_name}")
                out.append(nozzle_face(nozzle_name))
            elif "EQUIPMENT" in stack and len(stack) == 1:
                # The installation coordinate is project data and never moves.
                out.append(line)
            elif stack and stack[-1] == "SUBEQUIPMENT":
                # A SUBE POS is a RELATIVE OFFSET between coordinate frames,
                # not a point in space.  It scales like everything else, but
                # it must never be re-datumed: an earlier revision applied an
                # elevation re-anchoring here, which turned /Motor's POS U 0
                # into U 102 and lifted the motor off the shaft it drives.
                # Because each child of the SUBE was re-anchored again in its
                # own right, the motor ended 204 mm above the casing axis with
                # the coupling visibly parted in E3D.
                out.append(pos_line(scale_pos(read_pos(match))))
            elif stack and stack[-1] == "VERTEX":
                # LOOP vertices are profile-local offsets; scale them plainly
                # so the hex head grows with its shank.
                vec = read_pos(match)
                out.append(pos_line(tuple(v * S for v in vec)))
            else:
                out.append(pos_line(scale_pos(read_pos(match))))
            continue

        dim_match = DIM_RE.match(text)
        if dim_match:
            attribute = dim_match.group(1)
            value = Decimal(dim_match.group(2))
            if "NOZZLE" in stack:
                out.append(line)  # catalogue projection is unchanged
            else:
                out.append(f"{attribute} {fmt(value * S)}mm")
            continue

        # A CREF is one half of a reciprocal pipe connection: the branch it
        # names carries the matching HREF/TREF pointing back at /P1501B's
        # nozzle.  Copying it would make the new pump claim pipework that is
        # already terminated on the original, so the connection is dropped.
        # Routing /P1501C is a piping decision, not something to inherit.
        if text.startswith("CREF "):
            dropped_crefs.append(text)
            continue

        if text.startswith("USRWEI") or text.startswith("USRWWE"):
            out.append(scale_weight(line))
            continue

        if text.startswith("USRCOG") or text.startswith("USRWCO"):
            out.append(scale_bracketed(line))
            continue

        out.append(line.replace(OLD_TAG, NEW_TAG))

    if stack:
        raise ValueError(f"unclosed elements at end of body: {stack}")
    return out, dropped_crefs


def main() -> None:
    require_input(SOURCE, "the native E3D data listing of /P1501B")
    raw = SOURCE.read_text(encoding="utf-8-sig", errors="strict")

    IMPORTS_DIR.mkdir(parents=True, exist_ok=True)
    archive = IMPORTS_DIR / "2026-08-18_Reference_pumps_P1501B.txt"
    if not archive.exists():
        shutil.copyfile(SOURCE, archive)

    # E3D writes this listing with CRLF line endings.  Detect the terminator
    # from the raw BYTES: ``raw`` was decoded in text mode, which silently
    # normalises CRLF to LF, so testing the decoded string always says LF and
    # would quietly ship a Windows tool a dialect it never produces itself.
    newline = "\r\n" if b"\r\n" in SOURCE.read_bytes() else "\n"
    lines = raw.replace("\r\n", "\n").split("\n")
    result, dropped_crefs = transform_lines(lines)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUTPUT_DIR / "P1501C_1807x663.txt"
    body = newline.join(result)
    # The description is the one free-text field that should say what this is.
    body = body.replace("DESC 'Reflux Pump - Standby'", f"DESC {NEW_DESC}")
    # The source header date belongs to the original export; restamp it so the
    # file does not claim to be E3D's own listing of a pump that never existed.
    stamp = date.today().strftime("%d %b %Y")
    # ``.*`` would eat the CR of a CRLF terminator and leave a lone LF behind,
    # so exclude both terminator characters from the match.
    body = re.sub(
        r"(-- (?:End )?Data Listing[ \t]+Date : )[^\r\n]*",
        lambda m: f"{m.group(1)}{stamp}  (derived from /P1501B, scale {S})",
        body,
    )
    # Match the source's encoding as well as its line endings: E3D wrote this
    # listing as UTF-8 with a BOM, so the variant is delivered the same way.
    raw_bytes = SOURCE.read_bytes()
    encoding = "utf-8-sig" if raw_bytes[:3] == b"\xef\xbb\xbf" else "utf-8"
    target.write_text(body, encoding=encoding, newline="")

    digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
    print(f"source      : {SOURCE}")
    print(f"archived    : {archive}")
    print(f"factor S    : {S}")
    print(f"baseplate   : {OLD_LEN} x {OLD_WID}  ->  "
          f"{fmt(OLD_LEN * S)} x {fmt(OLD_WID * S)}")
    for cref in dropped_crefs:
        print(f"dropped     : {cref}   (reciprocal connection to /P1501B pipework)")
    print(f"written     : {target}")
    print(f"sha256      : {digest}")


if __name__ == "__main__":
    main()
