"""
PML1 Primitive Builder
======================
Emits AVEVA E3D PML1 macro commands with the project's Iron Rules enforced by
construction rather than by inspection afterwards.

Two rules are structural here:

* **ORI before POS.** Every primitive writer emits the orientation line before
  the position line, so the coordinate drift caused by the reverse order cannot
  occur. Callers never write ``POS`` themselves.
* **PML1 only.** The builder emits nothing but PML1 commands, so a macro
  produced solely through this class cannot contain PML2 syntax.
  :meth:`PMLBuilder.build` re-checks the assembled text regardless.

Datum conversion
----------------
**E3D positions CYLI, CONE and BOX by geometric centre.  DISH is the important
exception: its POS is the flat rim / tangent plane.**  The centre rule for
CYLI/CONE is verified in AVEVA's own PML, which offsets by half the height to
make a cylinder *start* at a given point::

    pipeEditor.pmlfrm:7807
        !cylinderPosition = !position.offset(!direction, !height / 2)

Engineering drawings, by contrast, dimension a vessel from its **bottom face**.
This builder accepts the bottom-face point that callers naturally have and
converts CYLI/CONE to the centre datum E3D wants in
:meth:`PMLBuilder._position`.  DISH already accepts the rim point E3D wants and
passes it through.  Callers never do this arithmetic themselves.

===========  =================  ==============================================
Primitive    E3D datum          What this builder accepts
===========  =================  ==============================================
``CYLI``     geometric centre   ``base`` - bottom-face centre, converted
``CONE``     geometric centre   ``base`` - bottom-face centre, converted
``DISH``     flat rim plane     ``base`` - the flat rim, passed through
``BOX``      geometric centre   ``centre`` - geometric centre, passed through
``PYRAMID``  geometric centre   ``centre`` - geometric centre, passed through
===========  =================  ==============================================
"""

from __future__ import annotations

import math
import re
from typing import Iterable, List, Optional, Sequence, Tuple

__all__ = [
    "PMLBuilder",
    "PMLValidationError",
    "Axis",
    "validate_pml",
    "nozzle_component_path",
]


#: Vertical axis, the orientation used by every upright vessel in this area.
AXIS_UP = "U"
#: Horizontal axis along East.
AXIS_EAST = "E"
#: Horizontal axis along North.
AXIS_NORTH = "N"

Axis = str

#: PML comment token. Verified against AVEVA's own macros in
#: ``%AVEVA_DESIGN_EXE%\data\*.mac``, which open with ``-- ====`` banners.
COMMENT = "--"

#: Nozzle catalogue specification and generic type, per project direction.
#:
#: **These name the component each nozzle is to be bound to; they are not
#: emitted as an inline ``SPRE``.** An earlier version emitted
#: ``SPRE SPCOMPONENT /ANSI-NOZZLES/150lb-ANSI-Flanges:400`` and E3D rejected
#: every nozzle with::
#:
#:     (2,109) Undefined name /ANSI-NOZZLES/150lb-ANSI-Flanges:400
#:
#: Reading the catalogue database itself
#: (``AvevaCatalogue/acp000/acp7014_0001``, the MASTER/EQUICATA equipment
#: catalogue) shows why:
#:
#: * ``/ANSI-NOZZLES`` **does** exist, so the specification name is right.
#: * The generic type is stored as the description ``150lb Ansi Flanges`` -
#:   spaces and mixed case, not ``150lb-ANSI-Flanges``. It is a SELE's
#:   *description*, which is display text and not part of any path.
#: * The bore components beneath it are ``SPCO`` elements that carry **no
#:   names** in this catalogue. ``equnozzle.pmlfrm:672`` picks them by DBREF at
#:   runtime, so there is no ``/spec/type:bore`` path to resolve.
#:
#: What the earlier fix got wrong was the conclusion. Dropping the reference
#: altogether leaves every nozzle with **no catalogue component and therefore no
#: geometry**: a NOZZLE is a catalogue element, so with nothing bound it is a
#: bare connection point that draws nothing in a shaded view. That is precisely
#: the "nozzles not displaying" symptom.
#:
#: The binding command is ``CATR SPCOMPONENT <path>``, and it must be emitted
#: **inline, immediately after ``NEW NOZZLE``** - before ``POS``, ``ORI`` or any
#: other attribute. A nozzle's P-points and position come from its catalogue
#: component, so until one is bound there is nothing to position or aim.
#: AVEVA's creation form does exactly this (``equnozzle.pmlfrm:894``)::
#:
#:     NEW NOZZ
#:     !!ce.catref = !this.nozzSpecRef      <- the very next statement
#:
#: The trailing ``OLD``/``CATR`` pass in ``SMLdataPlant.pmlmac:13733`` is a
#: *rebinding* of nozzles that already have a component, not a creation
#: sequence. Using it to create aborts each nozzle on its ``ORI`` line with
#: ``(2,360) Cannot get position of NOZZLE``.
NOZZLE_SPEC = "ANSI-NOZZLES"
NOZZLE_TYPE = "150lb Ansi Flanges"

#: Bore (mm) -> SPCO component name under the ``150lb_Ansi_Flanged`` SELEC of
#: ``/ANSI-NOZZLES``. **Read out of the live project catalogue**, not inferred.
#:
#: Every attempt to derive this from the component-code ordering failed, and the
#: reason is visible in the table: ``011`` and ``033`` are DN500 and DN600 - the
#: two *largest* bores sit at the *start* of the sequence, before DN15. The
#: ladder also contains DN90, which is not in the standard ANSI series. No
#: ordering rule reproduces that, so guessing a code for a bore would have bound
#: the wrong flange to most of the schedule while still loading cleanly.
#:
#: Obtained by running ``list_nozzle_bores.mac`` in E3D (bare path to navigate,
#: then ``Q NAME ANSWER``) and reading the ``Answer`` attribute of each SPCO.
#: Regenerate it the same way against any other receiving project - these names
#: are catalogue-specific and must never be assumed to carry across.
#:
#: **These are component names, not full paths.** ``CATR SPCOMPONENT`` takes the
#: SPCO's own path, which is ``/<selec>/<component>`` - see
#: :data:`NOZZLE_SELEC`. Emitting the bare component name produced::
#:
#:     (2,108) SCOMPONENT /AAZFBB0YY is not a SPCO
#:
#: because ``/AAZFBB0YY`` is the SPCO's ``Catref`` *value* (the catalogue
#: geometry it points at), not the SPCO itself. The ``Q ATT`` output shows both,
#: and they are easy to confuse::
#:
#:     Name   /150lb_Ansi_Flanged/AAZFBB0YY   <- the SPCO, what CATR wants
#:     Catref /AAZFBB0YY                      <- what the SPCO points at
#:
#: AVEVA's own data uses the two-segment form throughout
#: (``SMLdataPlant.pmlmac:13735``: ``CATR SPCOMPONENT /DICHTFL_C/ND-16RF-150``).
NOZZLE_BORE_COMPONENTS: dict = {
    15: "AAZFBB0DD",
    20: "AAZFBB0EE",
    25: "AAZFBB0FF",
    32: "AAZFBB0GG",
    40: "AAZFBB0HH",
    50: "AAZFBB0JJ",
    65: "AAZFBB0KK",
    80: "AAZFBB0LL",
    90: "AAZFBB0MM",
    100: "AAZFBB0NN",
    125: "AAZFBB0PP",
    150: "AAZFBB0RR",
    200: "AAZFBB0TT",
    250: "AAZFBB0VV",
    300: "AAZFBB0WW",
    350: "AAZFBB0XX",
    400: "AAZFBB0YY",
    450: "AAZFBB0ZZ",
    500: "AAZFBB011",
    600: "AAZFBB033",
}

#: SELEC that owns the nozzle SPCOs, from ``Q ATT``'s
#: ``Owner SELEC 14 of SPECIFICATION /ANSI-NOZZLES``. A component's full path is
#: ``/<NOZZLE_SELEC>/<component>``, which is what ``CATR SPCOMPONENT`` resolves.
NOZZLE_SELEC = "150lb_Ansi_Flanged"

#: Largest bore the catalogue carries (mm). A nozzle above this has no component
#: to bind, and is reported rather than silently downsized - see
#: :meth:`PMLBuilder.catref_pass`.
NOZZLE_MAX_CATALOGUE_DN = max(NOZZLE_BORE_COMPONENTS)


def nozzle_component_path(bore_dn: int) -> str:
    """
    Full SPCO path for a bore, as ``CATR SPCOMPONENT`` requires.

    Args:
        bore_dn: Nominal bore (mm).

    Raises:
        KeyError: if the catalogue carries no component at that bore. Callers
            must report the nozzle rather than substitute a nearby size.
    """
    return f"/{NOZZLE_SELEC}/{NOZZLE_BORE_COMPONENTS[bore_dn]}"

#: PML2 constructs that make an E3D macro fail to load. Matched case-insensitively
#: as whole tokens where the term is a word, so that legitimate PML1 text such as
#: a comment mentioning "ENDS" of a vessel is not a false positive.
_BANNED_PATTERNS: Tuple[Tuple[str, str], ...] = (
    (r"!!\s*alert", "!!Alert"),
    (r"!!\s*ce\b", "!!CE"),
    (r"!!\s*world\b", "!!WORLD"),
    (r"!!\s*dotnet", "!!DotNet* (PML2 .NET bridge)"),
    (r"\$P\b", "$P"),
    (r"^\s*ENDS\s*$", "ENDS"),
    (r"^\s*END\s+EQUI\s*$", "END EQUI"),
    (r"^\s*NAME\s*=", "NAME ="),
    (r"^\s*DESC\s*=", "DESC ="),
    (r"^\s*COLLECT\b", "COLLECT"),
    (r"^\s*UNSET\b", "UNSET"),
    (r"^\s*(IF|ELSEIF)\b.*\bTHEN\b", "IF/THEN block (PML2)"),
    (r"^\s*ENDIF\b", "ENDIF (PML2)"),
    (r"^\s*DO\b.*\$", "DO loop (PML2)"),
    (r"^\s*ENDDO\b", "ENDDO (PML2)"),
    # SPRE is valid and required for catalogue-backed piping components such as
    # ELBOW, TEE and VALVE. It is invalid only inside a NOZZLE block in this
    # project, where CATR binds the SPCO and creates the P-points. That
    # element-specific check lives in _check_nozzle_catref_first(); a global
    # ban here incorrectly rejected 1,112 native piping SPRE lines.
    (r"^\s*CATREF\s*/", "CATREF /path (attribute form; use CATR SPCOMPONENT)"),
    # PDMS alphanumeric-window command. Not valid in E3D Design Mk3.1: it
    # aborts the macro with "(47,15) CP: Syntax error / ALPHA ^^HEADER OFF".
    # Use SUSPEND/RESUME alone for rendering control.
    (r"^\s*ALPHA\s+HEADER\b", "ALPHA HEADER (PDMS-only, rejected by E3D Design)"),
    # SUSPEND / RESUME are not E3D Design commands. They appear nowhere as
    # commands in AVEVA's PML library - every occurrence there is a method name
    # or a word inside a comment. Emitting them aborts the macro with
    # "(47,15) CP: Syntax error / ^^SUSPEND".
    (r"^\s*(SUSPEND|RESUME)\s*$", "SUSPEND/RESUME (not an E3D Design command)"),
)

#: PML2 variable assignment, e.g. ``!x = 3`` or ``!!gv = 4``. Excluded inside
#: comment lines, which start with ``--``.
_PML2_ASSIGN = re.compile(r"^\s*!{1,2}[A-Za-z_][A-Za-z0-9_]*\s*=")

#: A PML comment line. Both ``--`` (used throughout AVEVA's own .mac files) and
#: ``$*`` are treated as comments for validation purposes.
_COMMENT = re.compile(r"^\s*(--|\$\*)")


class PMLValidationError(RuntimeError):
    """Raised when a generated macro violates a PML1 rule."""


def validate_pml(script: str, *, native_templates: bool = False) -> List[str]:
    """
    Check a PML macro for syntax that would break E3D, returning one message per
    problem found. An empty list means the script passed.

    Three classes of defect are checked:

    1. PML2 constructs that cause a load failure.
    2. PML2 variable assignment outside comments.
    3. ``POS`` emitted before ``ORI`` within a primitive block, which silently
       rotates the position vector and drifts the element.

    ``native_templates=True`` additionally accepts source-backed two-axis
    cardinal/quadrant orientations, checking their orthonormal frame. Default
    generated-model conventions and all nozzle/order checks remain in force.
    """
    problems: List[str] = []
    lines = script.split("\n")

    for lineno, line in enumerate(lines, 1):
        if _COMMENT.match(line):
            continue
        for pattern, label in _BANNED_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE | re.MULTILINE):
                problems.append(
                    f"L{lineno}: PML2 syntax {label!r} -> {line.strip()}"
                )
        if _PML2_ASSIGN.match(line):
            problems.append(
                f"L{lineno}: PML2 variable assignment -> {line.strip()}"
            )

    problems.extend(_check_ori_before_pos(lines))
    problems.extend(_check_nozzle_pos_before_ori(lines))
    problems.extend(_check_nozzle_catref_first(lines))
    problems.extend(_check_nozzle_heig_plausible(lines))
    problems.extend(_check_element_axis_convention(lines, native_templates=native_templates))
    problems.extend(_check_framework_orientation(lines))
    return problems


def _check_framework_orientation(lines: Sequence[str]) -> List[str]:
    """Reject ORI in a directly selected/created FRMW header.

    User E3D evidence: Typical_Pipe_Support R1, error (2,201) on line 12.
    This checks known headers, not a complete database attribute schema.
    A new element or a cursor-changing command ends the known header scope.
    """
    problems: List[str] = []
    framework_names: set[str] = set()
    in_framework = False
    for lineno, raw in enumerate(lines, 1):
        line = raw.strip().upper()
        if not line or _COMMENT.match(raw):
            continue
        creation = re.match(r"^(?:NEW|OLD)\s+(\w+)(?:\s+(/\S+))?", line)
        if creation:
            in_framework = creation[1] in {"FRMW", "FRMWORK", "FRAMEWORK"}
            if in_framework and creation[2]:
                framework_names.add(creation[2])
        elif line.startswith("/"):
            in_framework = line in framework_names
        elif re.match(r"^(?:END|OWNER|CE|GOTO|OLD)\b", line):
            in_framework = False
        elif in_framework and re.match(r"^(?:ORI|ORIENT|ORIENTATION)\s", line):
            problems.append(f"L{lineno}: FRMWORK does not have attribute ORI -> {raw.strip()}")
    return problems


#: Bounds on a nozzle's ``HEIG`` (mm). A nozzle is a short stub: anything
#: outside this is a datum error, not a dimension choice.
_NOZZLE_HEIG_MIN_MM = 1.0
_NOZZLE_HEIG_MAX_MM = 2000.0


def _check_nozzle_heig_plausible(lines: Sequence[str]) -> List[str]:
    """
    Verify every nozzle's ``HEIG`` is a plausible nozzle length.

    ``HEIG`` is the nozzle's own length - the projection from its connection
    point to the flange face. A version of this builder instead computed it as
    the distance from the owning equipment's origin, which emitted values from
    **-61680 to +72280 mm** for nozzles 250-450 mm long and drew the model as a
    thicket of metre-long tubes flying off the vessels.

    A negative length is impossible and a 72 m nozzle is absurd, so a bounds
    check catches that class of error immediately - without needing to know
    which datum is correct. Cheap bounds on a physical quantity are worth more
    than an elaborate check that encodes the same assumption as the code.
    """
    problems: List[str] = []
    in_nozzle = False
    block_start = 0

    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()
        if _COMMENT.match(raw):
            continue
        new_match = re.match(r"^NEW\s+([A-Z]+)", line, re.IGNORECASE)
        if new_match:
            in_nozzle = new_match.group(1).upper() == "NOZZLE"
            block_start = lineno
            continue
        if not in_nozzle:
            continue
        heig_match = re.match(r"^HEIG\s+(-?[\d.]+)", line, re.IGNORECASE)
        if not heig_match:
            continue
        value = float(heig_match.group(1))
        if not _NOZZLE_HEIG_MIN_MM <= value <= _NOZZLE_HEIG_MAX_MM:
            problems.append(
                f"L{lineno}: NEW NOZZLE (L{block_start}) has HEIG {value} - a "
                f"nozzle's HEIG is its own length and must lie between "
                f"{_NOZZLE_HEIG_MIN_MM} and {_NOZZLE_HEIG_MAX_MM} mm; a value "
                f"outside that means the wrong datum was used"
            )
        in_nozzle = False

    return problems


def _check_nozzle_catref_first(lines: Sequence[str]) -> List[str]:
    """
    Verify ``CATR`` precedes ``POS`` and ``ORI`` in every NOZZLE block, reject
    the piping-only ``SPRE`` form there, and ensure an unbound nozzle carries no
    ``ORI``.

    A nozzle's P-points and position come from its catalogue component, so
    binding late aborts the macro mid-load::

        (2,360) Cannot get position of NOZZLE /203_TA_006_N1_NOZZ

    That failure stops the whole macro at the first nozzle, so only part of the
    model loads - which is far less obvious than a syntax error on line 1.
    """
    problems: List[str] = []
    in_nozzle = False
    block_start = 0
    seen: List[Tuple[str, int]] = []

    def close_block() -> None:
        if not in_nozzle:
            return
        verbs = [v for v, _ in seen]
        at = dict(seen)
        if "SPRE" in verbs:
            problems.append(
                f"L{at['SPRE']}: NEW NOZZLE uses SPRE SPCOMPONENT "
                f"(unresolvable catalogue path for NOZZLE); bind its SPCO "
                f"with CATR SPCOMPONENT before POS and ORI instead"
            )
        if "CATR" in verbs:
            for later in ("POS", "ORI"):
                if later in verbs and at[later] < at["CATR"]:
                    problems.append(
                        f"L{block_start}: NEW NOZZLE has {later} (L{at[later]}) "
                        f"before CATR (L{at['CATR']}) - a nozzle has no "
                        f"P-points or position until its catalogue component "
                        f"is bound, so this aborts with '(2,360) Cannot get "
                        f"position of NOZZLE'"
                    )
        elif "ORI" in verbs:
            problems.append(
                f"L{block_start}: NEW NOZZLE is aimed (L{at['ORI']}) but has no "
                f"CATR - there is no P1 to orient without a bound component"
            )

    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()
        if _COMMENT.match(raw):
            continue
        new_match = re.match(r"^NEW\s+([A-Z]+)", line, re.IGNORECASE)
        if new_match:
            close_block()
            in_nozzle = new_match.group(1).upper() == "NOZZLE"
            block_start = lineno
            seen = []
            continue
        if not in_nozzle:
            continue
        verb_match = re.match(r"^(CATR|SPRE|POS|ORI)\b", line, re.IGNORECASE)
        if verb_match:
            verb = verb_match.group(1).upper()
            if verb not in dict(seen):
                seen.append((verb, lineno))

    close_block()
    return problems


def _check_nozzle_pos_before_ori(lines: Sequence[str]) -> List[str]:
    """
    Verify POS precedes ORI in every NOZZLE block - the reverse of a primitive.

    Both orders load without error, so nothing but a check like this catches the
    fault before the model is opened. See :func:`_check_ori_before_pos` for why
    the two element families differ.
    """
    problems: List[str] = []
    block_start = 0
    in_nozzle = False
    ori_at: Optional[int] = None
    pos_at: Optional[int] = None

    def close_block() -> None:
        if in_nozzle and ori_at is not None and pos_at is not None:
            if ori_at < pos_at:
                problems.append(
                    f"L{block_start}: NEW NOZZLE has ORI (L{ori_at}) before POS "
                    f"(L{pos_at}) - a nozzle's POS is read in its owner's frame, "
                    f"so orienting first rotates it off the shell"
                )

    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()
        if _COMMENT.match(raw):
            continue
        new_match = re.match(r"^NEW\s+([A-Z]+)", line, re.IGNORECASE)
        if new_match:
            close_block()
            in_nozzle = new_match.group(1).upper() == "NOZZLE"
            block_start = lineno
            ori_at = pos_at = None
            continue
        if not in_nozzle:
            continue
        if re.match(r"^ORI\b", line, re.IGNORECASE) and ori_at is None:
            ori_at = lineno
        elif re.match(r"^POS\b", line, re.IGNORECASE) and pos_at is None:
            pos_at = lineno

    close_block()
    return problems


def _check_element_axis_convention(lines: Sequence[str], *, native_templates: bool = False) -> List[str]:
    """
    Verify each element family orients on the axis E3D actually uses.

    The two families genuinely differ, and both mistakes load without error:

    * A **primitive**'s length runs along Z (``gphFactory.pmlobj:632``), so a
      vertical vessel needs ``ORI Z IS U``. Orienting on Y lays it on its side.
    * A **NOZZLE** is aimed by its P-point, ``ORI P1 IS <direction>``, which is
      what AVEVA's own Modify Nozzle form emits (``equnozzle.pmlfrm:851``).
      Orienting a nozzle on a geometric axis (``ORI Y is ...``) points it
      somewhere other than its bore, and still loads without error.

    Because neither fault is a syntax error, nothing but a check like this
    catches them before the model is opened.
    """
    problems: List[str] = []
    primitives = {"CYLI", "CONE", "DISH"}
    block: Optional[str] = None
    block_start = 0

    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()
        if _COMMENT.match(raw):
            continue
        new_match = re.match(r"^NEW\s+([A-Z]+)", line, re.IGNORECASE)
        if new_match:
            block = new_match.group(1).upper()
            block_start = lineno
            continue
        if not re.match(r"^ORI\b", line, re.IGNORECASE):
            continue
        if native_templates and block in {"CYLI", "CYLINDER", "CONE", "DISH", "BOX", "PYRAMID", "EXTRUSION", "CTORUS"}:
            # Native listings legitimately put Y before Z and rotate motor
            # fin boxes out of the horizontal plane. Preserve their axes;
            # check the actual orthonormal frame instead of keyword order.
            from .pml_parser import native_orientation_basis
            try:
                native_orientation_basis(line)
                if not re.search(r"\bZ\s+IS\b", line, re.I):
                    raise ValueError("Native primitive must explicitly define Z")
            except ValueError as error:
                problems.append(f"L{lineno}: {error}")
            continue
        if block in primitives and not re.match(
            r"^ORI\s+Z\s+IS\b", line, re.IGNORECASE
        ):
            problems.append(
                f"L{lineno}: NEW {block} (L{block_start}) orients on the wrong "
                f"axis - a primitive's length runs along Z -> {line}"
            )
        elif block == "BOX" and not re.match(
            r"^ORI\s+Z\s+IS\s+U\s+AND\s+X\s+IS\b",
            line,
            re.IGNORECASE,
        ):
            problems.append(
                f"L{lineno}: NEW BOX (L{block_start}) uses an unsupported "
                f"orientation - plan-rotated boxes take "
                f"'ORI Z IS U AND X IS <bearing>' -> {line}"
            )
        elif block == "NOZZLE" and not re.match(
            r"^ORI\s+P\d+\s+IS\b", line, re.IGNORECASE
        ):
            problems.append(
                f"L{lineno}: NEW NOZZLE (L{block_start}) is not aimed by its "
                f"P-point - a nozzle takes 'ORI P1 IS <direction>', not a "
                f"geometric axis -> {line}"
            )

    return problems


def _check_ori_before_pos(lines: Sequence[str]) -> List[str]:
    """
    Verify ORI precedes POS in every oriented **primitive** block.

    A block runs from a ``NEW <element>`` line to the next ``NEW`` line, so
    attributes are attributed to the element that owns them regardless of how
    many attribute lines sit between.

    **NOZZLE is deliberately excluded, and takes the opposite order.** An earlier
    version of this check included it, reasoning that a nozzle carries an ORI and
    a POS just as a primitive does. AVEVA's own macro data contradicts that: all
    ten NOZZLE blocks in ``PDMSUI\\data\\SMLdataPlant.pmlmac`` are written
    POS-then-ORI. A nozzle's POS is expressed in its owning equipment's frame
    rather than being consumed by its own orientation, so orienting first
    rotates the frame the position is read in. The order is checked for nozzles
    by :func:`_check_nozzle_pos_before_ori`.
    """
    problems: List[str] = []
    required_orientation = {"CYLI", "CONE", "DISH"}
    optional_orientation = {"BOX"}

    block_prim: Optional[str] = None
    block_start = 0
    ori_at: Optional[int] = None
    pos_at: Optional[int] = None

    def close_block() -> None:
        if block_prim in required_orientation and pos_at is not None:
            if ori_at is None:
                problems.append(
                    f"L{block_start}: NEW {block_prim} has POS at L{pos_at} but no "
                    f"ORI - orientation defaults and the element may drift"
                )
            elif pos_at < ori_at:
                problems.append(
                    f"L{block_start}: NEW {block_prim} has POS (L{pos_at}) before "
                    f"ORI (L{ori_at}) - this rotates the position vector and "
                    f"drifts the element"
                )
        elif (
            block_prim in optional_orientation
            and ori_at is not None
            and pos_at is not None
            and pos_at < ori_at
        ):
            problems.append(
                f"L{block_start}: NEW {block_prim} has POS (L{pos_at}) before "
                f"ORI (L{ori_at}) - this rotates the position vector and "
                f"drifts the element"
            )

    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()
        if _COMMENT.match(raw):
            continue
        new_match = re.match(r"^NEW\s+([A-Z]+)", line, re.IGNORECASE)
        if new_match:
            close_block()
            block_prim = new_match.group(1).upper()
            block_start = lineno
            ori_at = pos_at = None
            continue
        if re.match(r"^ORI\b", line, re.IGNORECASE) and ori_at is None:
            ori_at = lineno
        elif re.match(r"^POS\b", line, re.IGNORECASE) and pos_at is None:
            pos_at = lineno

    close_block()
    return problems


def _fmt(value: float) -> str:
    """Format a length for PML: millimetres to 1 decimal place."""
    return f"{value:.1f}"


def _fmt_angle(value: float) -> str:
    """Format an orientation angle without losing off-axis bearing accuracy."""
    return f"{value:.4f}".rstrip("0").rstrip(".")


def _plan_direction(rotation_deg: float) -> str:
    """
    E3D direction text for an XY bearing measured East towards North.

    Examples: 30 degrees -> ``E 30 N``; 135 degrees -> ``N 45 W``.
    """
    angle = rotation_deg % 360.0
    cardinals = ((0.0, "E"), (90.0, "N"), (180.0, "W"), (270.0, "S"))
    for cardinal_angle, direction in cardinals:
        if abs(angle - cardinal_angle) < 1e-9:
            return direction
    if angle < 90.0:
        return f"E {_fmt_angle(angle)} N"
    if angle < 180.0:
        return f"N {_fmt_angle(angle - 90.0)} W"
    if angle < 270.0:
        return f"W {_fmt_angle(angle - 180.0)} S"
    return f"S {_fmt_angle(angle - 270.0)} E"


def _sanitize(name: str) -> str:
    """
    Convert an equipment tag into a legal E3D element name.

    E3D names cannot contain spaces or hyphens, so both become underscores.
    """
    cleaned = re.sub(r"[^A-Za-z0-9_/]", "_", name.strip())
    return re.sub(r"_{2,}", "_", cleaned).strip("_")


class PMLBuilder:
    """
    Accumulates PML1 commands for one macro.

    Args:
        name: Label for the macro, used in the header banner only. Equipment
            elements are opened individually with :meth:`equi`.
        close_elements: Emit the native data-listing closure: ``END`` after
            every primitive, and ``END`` for each open SUBE/EQUI before the
            next one opens (and in :meth:`close_all`). The default, open form
            relies on ``NEW`` climbing to a valid owner, which is how every
            generated macro in this project has loaded; the closed form is
            what E3D's own listings use and is the right shape for a block
            that is spliced into a native export (JK-Tank_Build R8,
            ``WSB_TA_two_tanks_handrails_20260831.pml``).
    """

    def __init__(self, name: str = "", *, close_elements: bool = False) -> None:
        self._lines: List[str] = []
        self._name = _sanitize(name)
        self._equi_names: set[str] = set()
        self._sube_names: set[str] = set()
        #: (name, bore, spec, generic type) per nozzle, for :meth:`catref_pass`.
        self._nozzle_bindings: List[Tuple[str, int, str, str]] = []
        self._close_elements = close_elements
        self._equi_open = False
        self._sube_open = False
        self.primitive_count = 0
        self.equipment_count = 0
        self.nozzle_count = 0

    # -- structure ------------------------------------------------------

    def comment(self, text: str = "") -> "PMLBuilder":
        """
        Emit a comment line, or a blank line when text is empty.

        The comment token is ``--``, as used throughout AVEVA's own
        ``%AVEVA_DESIGN_EXE%\\data\\*.mac`` files.
        """
        self._lines.append(f"{COMMENT} {text}" if text else "")
        return self

    def banner(self, text: str) -> "PMLBuilder":
        """Emit a visually separated section comment."""
        rule = f"{COMMENT} " + "=" * 68
        self._lines.extend([rule, f"{COMMENT} {text}", rule])
        return self

    def header(self, title: str, meta: Iterable[Tuple[str, str]] = ()) -> "PMLBuilder":
        """
        Emit the macro header.

        No element is opened here: each item of equipment opens its own EQUI via
        :meth:`equi`, which is the AVEVA convention - one EQUI per item of
        equipment, not one per macro.
        """
        self.banner(title)
        for key, value in meta:
            self.comment(f"{key}: {value}")
        self.comment()
        # No rendering-control prologue is emitted. The ALPHA HEADER / VAR 0 /
        # SUSPEND / RESUME sequence this project previously used is not valid in
        # E3D Design Mk3.1 - none of those are Design commands, and each aborts
        # the macro on its own line. The macro contains element creation only,
        # which is what E3D actually executes.
        return self

    def footer(self) -> "PMLBuilder":
        """Close the macro and restore rendering."""
        self.comment()
        self.comment(
            f"End of macro - {self.equipment_count} equipment, "
            f"{self.primitive_count} primitives."
        )
        return self

    def equi(
        self,
        name: str,
        *,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        attributes: Iterable[str] = (),
    ) -> "PMLBuilder":
        """
        Open an equipment element - one per item of equipment.

        The EQUI is explicitly anchored, by default at its owner's origin. A
        bare ``POS`` in E3D is measured **with respect to the owner**, not the
        world (the world form is ``POS ... WRT /*``), so every primitive
        underneath is positioned relative to this element. Anchoring the EQUI
        at zero keeps the primitives' existing coordinates world-absolute and
        unchanged: without it the EQUI would take whatever position the
        current element happens to have, and the whole tank would shift by
        that amount.

        An explicit ``position`` is for continuing a native baseline whose
        EQUI already carries an owner-relative POS (the WSB_TA export after
        the 2026-09-02 relocation places every EQUI at
        ``E 51267 N 58841 D 300``). The primitives beneath are then written in
        the EQUI's own frame, and the line here must reproduce the accepted
        value exactly or the whole item moves.

        Args:
            name: Equipment name, unique within the macro.
            position: Owner-relative (east, north, up) of the EQUI origin.
            attributes: Extra attribute lines written after ``POS``, verbatim
                (e.g. the ``FUNC``/``BUIL`` lines a native export carries).

        Raises:
            PMLValidationError: if the name has already been used.
        """
        clean = _sanitize(name)
        if clean in self._equi_names:
            raise PMLValidationError(
                f"Duplicate EQUI name {clean!r} - E3D would create two "
                f"indistinguishable elements"
            )
        self.close_all()
        self._equi_names.add(clean)
        self._lines.append(f"NEW EQUI /{clean}")
        east, north, up = position
        self._lines.append(f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(up)}")
        for line in attributes:
            self._lines.append(line)
        self._equi_open = True
        self.equipment_count += 1
        return self

    def sube(self, name: str, *, attributes: Iterable[str] = ()) -> "PMLBuilder":
        """
        Open a sub-equipment grouping under the current EQUI.

        Args:
            name: Grouping name, unique within the macro.
            attributes: Extra attribute lines written after ``NEW SUBE``,
                verbatim.

        Raises:
            PMLValidationError: if the name has already been used, which would
                produce two indistinguishable elements in the model tree.
        """
        clean = _sanitize(name)
        if clean in self._sube_names:
            raise PMLValidationError(
                f"Duplicate SUBE name {clean!r} - E3D would create two "
                f"indistinguishable elements"
            )
        self._close_sube()
        self._sube_names.add(clean)
        self._lines.append(f"NEW SUBE /{clean}")
        for line in attributes:
            self._lines.append(line)
        self._sube_open = True
        return self

    def close_all(self) -> "PMLBuilder":
        """
        Close the open SUBE and EQUI with ``END`` lines.

        Only emits anything in the END-closed form; the open form has nothing
        to close because the next ``NEW`` climbs to its owner on its own.
        Safe to call more than once.
        """
        self._close_sube()
        if self._equi_open:
            if self._close_elements:
                self._lines.append("END")
            self._equi_open = False
        return self

    def _close_sube(self) -> None:
        if self._sube_open:
            if self._close_elements:
                self._lines.append("END")
            self._sube_open = False

    def _close_primitive(self) -> None:
        """``END`` after a primitive in the closed form; nothing otherwise."""
        if self._close_elements:
            self._lines.append("END")

    # -- catalogue elements ---------------------------------------------

    def nozzle(
        self,
        name: str,
        bore_dn: int,
        height: float,
        base: Tuple[float, float, float],
        *,
        axis: Axis = AXIS_UP,
        spec: str = NOZZLE_SPEC,
        generic_type: str = NOZZLE_TYPE,
        label: str = "",
    ) -> "PMLBuilder":
        """
        Native E3D ``NOZZLE`` element, positioned by its **flange face**.

        A NOZZLE is a catalogue element, not a primitive: its flange geometry,
        bore and face position come from the specification component it points
        at, so this emits no CYLI of its own. Only the length (``HEIG``) and the
        flange-face datum are set here.

        Syntax verified against AVEVA's own macro data in
        ``%AVEVA_DESIGN_EXE%\\PMLUI\\data\\SMLdataPlant.pmlmac``, which contains
        ten complete NOZZLE blocks::

            NEW NOZZLE /SML/HO9007/N1
            POS -X 1600.554687 -Y 1031.290527 -Z 150.034179
            ORI Y is -Z and Z is -X
            TEMP -100000
            PRES 0
            TPRESS 0
            HEIG 122
            DUTY unset
            END

        Two facts from that data drive this method:

        * **A nozzle is aimed by its P-point.** The verified creation form emits
          ``ORI P1 IS <direction>``. This is different from a primitive, whose
          length is aimed with ``ORI Z IS``.
        * **There is no DIAM attribute.** The bore is a property of the
          catalogue component, so it is selected through the spec reference
          rather than set on the element.

        Args:
            name: Nozzle mark, appended to the current equipment name.
            bore_dn: Nominal bore (mm), used to select the catalogue component.
            height: Projection from the shell to the flange face (mm).
            base: (east, north, up) of the flange face. The barrel runs back
                from this datum through the vessel wall.
            axis: Direction the nozzle points away from the vessel.
            spec: Nozzle specification name.
            generic_type: Generic type within that specification.
            label: Optional comment written above the element.
        """
        if height <= 0:
            raise PMLValidationError(
                f"NOZZLE {name!r} needs a positive height, got {height}"
            )
        if bore_dn <= 0:
            raise PMLValidationError(
                f"NOZZLE {name!r} needs a positive bore, got {bore_dn}"
            )
        if label:
            self.comment(label)

        clean = _sanitize(name)
        self._lines.append(f"NEW NOZZLE /{clean}")
        # CATR comes FIRST, immediately after creation. A nozzle's P-points and
        # geometry come from its catalogue component, so until one is bound the
        # element has no P1 to aim and no position to set. AVEVA's own creation
        # form does exactly this - `!!ce.catref = !this.nozzSpecRef` is the
        # first thing after `NEW NOZZ` (equnozzle.pmlfrm:894), before height,
        # temperature or anything else.
        #
        # An earlier version bound the catalogue in a separate pass at the end
        # of the macro. That aborted every nozzle on its ORI line with
        # "(2,360) Cannot get position of NOZZLE" - the P-point did not exist
        # yet - and the macro stopped at the first tank.
        if bore_dn in NOZZLE_BORE_COMPONENTS:
            self._lines.append(
                f"CATR SPCOMPONENT {nozzle_component_path(bore_dn)}"
            )
        else:
            self.comment(
                f"No catalogue component at DN{bore_dn} (largest is "
                f"DN{NOZZLE_MAX_CATALOGUE_DN}) - left unbound, will not render"
            )
        # POS precedes ORI here, which is the reverse of a primitive and is
        # deliberate. All ten NOZZLE blocks in AVEVA's own macro data
        # (PDMSUI\data\SMLdataPlant.pmlmac:48, 58, 11018, ...) are written
        # POS-then-ORI, without exception. A NOZZLE's POS is expressed in its
        # owning equipment's frame, so orienting first rotates the frame the
        # position is then read in and throws the connection point off the
        # shell. Primitives behave the opposite way, which is why _orient() is
        # called before _position() there - see the note in _check_ori_before_pos.
        east, north, up = base
        self._lines.append(f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(up)}")
        # A nozzle with no bound component has no P1 to aim; emitting ORI would
        # abort the macro. Position alone is still meaningful.
        if bore_dn in NOZZLE_BORE_COMPONENTS:
            self._orient_nozzle(axis)
        # HEIG is the nozzle's own LENGTH - the projection from its connection
        # point to the flange face. It is a dimension of the nozzle, not a
        # distance from anything else.
        #
        # A previous version computed it as the distance from the owning EQUI's
        # origin to the flange face. That produced values from -61680 to +72280
        # for a set of nozzles 250-450 mm long, and drew the model as a thicket
        # of metre-long tubes flying off the vessels. The negative values alone
        # disprove the theory: a length cannot be negative, and nothing in the
        # datum reading survives that.
        self._lines.append(f"HEIG {_fmt(height)}")
        # Process attributes, as carried by every NOZZLE in AVEVA's macro data.
        # Emitted unset/zero rather than invented: no design conditions are
        # given in the project data, and a fabricated design pressure is worse
        # than a blank one a process engineer will fill in.
        self._lines.append("TEMP -100000")
        self._lines.append("PRES 0")
        self._lines.append("TPRESS 0")
        self._lines.append("DUTY unset")
        self._lines.append("END")
        self._lines.append("")
        # Recorded only so the report can list what was and was not bound. The
        # binding itself is emitted inline above, not in a trailing pass.
        self._nozzle_bindings.append((clean, bore_dn, spec, generic_type))
        self.nozzle_count += 1
        return self

    def catref_pass(self) -> "PMLBuilder":
        """
        Summarise which nozzles were bound to a catalogue component.

        **This emits no commands.** The binding itself is inline in each
        ``NEW NOZZLE`` block, immediately after creation - a nozzle's P-points
        and position come from its catalogue component, so nothing else about
        the element can be set until one is bound.

        An earlier version emitted the binding here instead, as a trailing pass
        of ``OLD``/``CATR`` pairs keyed by name. That shape does appear in
        AVEVA's data (``SMLdataPlant.pmlmac:13733``), but it is a *rebinding* of
        nozzles that already have a component - not how they are created. Used
        for creation it aborted every nozzle on its ``ORI`` line with::

            (2,360) Cannot get position of NOZZLE /203_TA_006_N1_NOZZ

        because the P-point did not exist yet, and the macro stopped at the
        first tank. AVEVA's own form binds first (``equnozzle.pmlfrm:894``:
        ``!!ce.catref = !this.nozzSpecRef``, the line straight after
        ``NEW NOZZ``), which is what the builder now does.
        """
        if not self._nozzle_bindings:
            return self
        unbound = [
            (name, dn) for name, dn, _s, _t in self._nozzle_bindings
            if dn not in NOZZLE_BORE_COMPONENTS
        ]
        bound = len(self._nozzle_bindings) - len(unbound)

        self.comment()
        self.banner("NOZZLE CATALOGUE SUMMARY")
        self.comment(
            f"{bound} of {len(self._nozzle_bindings)} nozzles bound to a "
            f"catalogue component."
        )
        self.comment(
            "Each binding is inline in its NEW NOZZLE block: a nozzle has no"
        )
        self.comment(
            "P-points or position until a component is bound, so CATR must"
        )
        self.comment(
            "precede POS and ORI (equnozzle.pmlfrm:894)."
        )
        if unbound:
            self.comment()
            self.comment(
                f"UNBOUND - ACTION REQUIRED: {len(unbound)} nozzle(s) have a"
            )
            self.comment(
                f"bore the catalogue does not carry (largest is "
                f"DN{NOZZLE_MAX_CATALOGUE_DN})."
            )
            self.comment(
                "These are created and positioned but have no geometry and"
            )
            self.comment(
                "will not render. They are NOT downsized to the nearest"
            )
            self.comment(
                "component: an under-sized flange on a real connection would"
            )
            self.comment("read as correct downstream and mislead the piping designer.")
            self.comment()
            for clean, bore_dn in unbound:
                self.comment(f"  {clean}  -  DN{bore_dn}")
                self.comment(f"  OLD /{clean}")
                self.comment(f"  CATR SPCOMPONENT /<a spec carrying DN{bore_dn}>")
                self.comment(f"  ORI P1 IS <direction>")
                self.comment()
        return self


    def _orient_nozzle(self, axis: Axis) -> None:
        """
        Aim a nozzle by its **P-point 1**, the bore direction.

        A nozzle is oriented by ``ORI P1 IS <direction>`` - not by any geometric
        axis. AVEVA's own Modify Nozzle form does exactly this
        (``equnozzle.pmlfrm:851``)::

            ORI P1 IS $!direction

        and reads the value back as ``pdir[1]`` (:852). ``ORI P<n> IS`` appears
        1087 times across the installed library and is macro-legal - it is
        emitted as literal macro text in ``nucoldocech.pmlobj:663``.

        **An earlier version emitted ``ORI Y is <axis> and Z is U``**, on the
        theory that a nozzle's axis runs along Y. That was wrong, and it aimed
        every nozzle in the model incorrectly while still loading cleanly. The
        rule came from the ``ORI Y is -Z and Z is -X`` lines in AVEVA's sample
        macro data, read without checking what they meant. Two things should
        have caught it sooner:

        * ``/SML/XX9004/N2`` in that same file reads ``ORI Y is Y and Z is -Z``.
          If Y were the bore and Z a free roll reference, that is a pure 180
          degree roll about the bore of an axisymmetric flange - meaningless.
        * The ``ORI Y is S and Z is U`` lines cited as corroboration sit on
          ``NEW FLANGE`` elements (``designcheckerrules.pmlmac:1171``), not on
          nozzles. Different element family, different convention.

        Orienting P1 states the bore direction directly, so there is no second
        axis to get wrong and no roll reference to misread.
        """
        directions = {
            "U": "ORI P1 IS U",
            "D": "ORI P1 IS D",
            "E": "ORI P1 IS E",
            "W": "ORI P1 IS W",
            "N": "ORI P1 IS N",
            "S": "ORI P1 IS S",
        }
        try:
            self._lines.append(directions[axis.upper()])
        except KeyError:
            raise PMLValidationError(
                f"Unknown nozzle axis {axis!r}; expected one of "
                f"{sorted(directions)}"
            ) from None

    # -- primitives -----------------------------------------------------

    def cyli(
        self,
        diameter: float,
        height: float,
        base: Tuple[float, float, float],
        *,
        axis: Axis = AXIS_UP,
        label: str = "",
    ) -> "PMLBuilder":
        """
        Cylinder positioned by its **bottom-face centre**.

        Args:
            diameter: Cylinder diameter (mm).
            height: Cylinder length along its axis (mm).
            base: (east, north, up) of the bottom-face centre.
            axis: Axis the cylinder extends along - ``U``, ``E`` or ``N``.
            label: Optional comment written above the primitive.
        """
        if diameter <= 0 or height <= 0:
            raise PMLValidationError(
                f"CYLI needs positive dimensions, got diameter={diameter}, "
                f"height={height}"
            )
        if label:
            self.comment(label)
        self._lines.append("NEW CYLI")
        self._lines.append(f"DIAM {_fmt(diameter)}")
        self._lines.append(f"HEIG {_fmt(height)}")
        self._orient(axis)
        self._position(base, axis=axis, extent=height)
        self._close_primitive()
        self.primitive_count += 1
        return self

    def cone(
        self,
        d_bottom: float,
        d_top: float,
        height: float,
        base: Tuple[float, float, float],
        *,
        axis: Axis = AXIS_UP,
        label: str = "",
    ) -> "PMLBuilder":
        """
        Cone or frustum positioned by its **bottom-face centre**.

        Args:
            d_bottom: Diameter at the base (mm).
            d_top: Diameter at the top (mm); may be smaller or larger than the base.
            height: Axial height (mm).
            base: (east, north, up) of the bottom-face centre.
            axis: Axis the cone extends along.
            label: Optional comment written above the primitive.
        """
        if height <= 0 or d_bottom <= 0 or d_top < 0:
            raise PMLValidationError(
                f"CONE needs positive dimensions, got dbot={d_bottom}, "
                f"dtop={d_top}, height={height}"
            )
        if label:
            self.comment(label)
        self._lines.append("NEW CONE")
        self._lines.append(f"DTOP {_fmt(d_top)}")
        self._lines.append(f"DBOT {_fmt(d_bottom)}")
        self._lines.append(f"HEIG {_fmt(height)}")
        self._orient(axis)
        self._position(base, axis=axis, extent=height)
        self._close_primitive()
        self.primitive_count += 1
        return self

    def dish(
        self,
        diameter: float,
        height: float,
        base: Tuple[float, float, float],
        *,
        axis: Axis = AXIS_UP,
        radius: Optional[float] = None,
        label: str = "",
    ) -> "PMLBuilder":
        """
        Dished head positioned by its **base-plane centre** - the flat rim where
        it meets the shell, not the apex.

        Per Iron Rule 2 a DISH is only ever a vessel head or closure. It must not
        be used as a flat cover, where at large diameters it produces a
        hemispherical bulge.

        Args:
            diameter: Rim diameter (mm), normally the shell diameter.
            height: Rise from rim to apex (mm).
            base: (east, north, up) of the rim-plane centre.
            axis: Direction the apex points - ``U`` for a top head, and pass a
                negative height convention via a downward variant for a bottom
                head (see :meth:`dish_down`).
            radius: Knuckle radius (mm). Defaults to the diameter, giving the
                2:1 semi-ellipsoidal proportion normal for process vessels.
            label: Optional comment written above the primitive.
        """
        if diameter <= 0 or height <= 0:
            raise PMLValidationError(
                f"DISH needs positive dimensions, got diameter={diameter}, "
                f"height={height}"
            )
        if label:
            self.comment(label)
        self._lines.append("NEW DISH")
        self._lines.append(f"DIAM {_fmt(diameter)}")
        self._lines.append(f"HEIG {_fmt(height)}")
        self._lines.append(f"RADIUS {_fmt(radius if radius is not None else diameter)}")
        self._orient(axis)
        # E3D's DISH datum is its flat rim / tangent plane.  Do not apply the
        # half-height centre conversion used by CYLI and CONE.  The previous
        # conversion made the ACCUMULATOR_TANK top head float by HEIG / 2 in
        # the user's E3D session (JK_Cooking_Tank_Build, 2026-07-30).
        self._position(base)
        self._close_primitive()
        self.primitive_count += 1
        return self

    def dish_down(
        self,
        diameter: float,
        height: float,
        rim: Tuple[float, float, float],
        *,
        radius: Optional[float] = None,
        label: str = "",
    ) -> "PMLBuilder":
        """
        Dished head pointing downward, for a vessel bottom.

        Positioned by the rim plane where the head meets the shell; the apex sits
        ``height`` below it.
        """
        return self.dish(
            diameter, height, rim, axis="D", radius=radius, label=label
        )

    def box(
        self,
        xlen: float,
        ylen: float,
        zlen: float,
        centre: Tuple[float, float, float],
        *,
        label: str = "",
        plan_rotation_deg: float = 0.0,
    ) -> "PMLBuilder":
        """
        Box positioned by its **geometric centre**.

        Args:
            xlen: Size along the BOX local X axis (mm).
            ylen: Size along the BOX local Y axis (mm).
            zlen: Size along Up (mm).
            centre: (east, north, up) of the geometric centre.
            label: Optional comment written above the primitive.
            plan_rotation_deg: Local X bearing measured from East towards North.
                Zero leaves the BOX on the global E/N axes.
        """
        if min(xlen, ylen, zlen) <= 0:
            raise PMLValidationError(
                f"BOX needs positive dimensions, got {xlen}x{ylen}x{zlen}"
            )
        if not math.isfinite(plan_rotation_deg):
            raise PMLValidationError(
                f"BOX plan rotation must be finite, got {plan_rotation_deg}"
            )
        if label:
            self.comment(label)
        self._lines.append("NEW BOX")
        self._lines.append(f"XLEN {_fmt(xlen)}")
        self._lines.append(f"YLEN {_fmt(ylen)}")
        self._lines.append(f"ZLEN {_fmt(zlen)}")
        rotation = plan_rotation_deg % 360.0
        if abs(rotation) > 1e-9:
            # AVEVA's own support/working-plane forms create a BOX, then set
            # `ORI Z IS <up> AND X IS <direction>` before POS.  X is the local
            # radial axis here; Y is consequently tangent to the vessel.
            self._lines.append(
                f"ORI Z IS U AND X IS {_plan_direction(rotation)}"
            )
        self._position(centre)
        self._close_primitive()
        self.primitive_count += 1
        return self

    def pyramid(
        self,
        xbot: float,
        ybot: float,
        xtop: float,
        ytop: float,
        height: float,
        centre: Tuple[float, float, float],
        *,
        xoff: float = 0.0,
        yoff: float = 0.0,
        plan_rotation_deg: float = 0.0,
        label: str = "",
    ) -> "PMLBuilder":
        """
        Rectangular pyramid/frustum positioned by its **geometric centre**.

        VERIFIED in E3D Design Mk3.1.11.0 (native ``/P1501B-BASE`` export and
        the JK_Pump_Build r6 acceptance, 2026-08-20): the bottom rectangle sits
        at local ``-HEIG/2`` and the top rectangle at ``+HEIG/2``, so a
        required span ``low..high`` is emitted as ``HEIG = high - low`` at
        ``POS U = (low + high) / 2``. ``XOFF``/``YOFF`` shift the top face in
        the element's local X/Y, which with equal faces gives a sheared prism -
        the verified form for an inclined leg or stay. The full keyword
        ``PYRAMID`` is required; ``PYRA`` is not a macro primitive.

        Args:
            xbot, ybot: Bottom rectangle (mm).
            xtop, ytop: Top rectangle (mm).
            height: Vertical extent along local Z (mm).
            centre: (east, north, up) of the geometric centre.
            xoff, yoff: Top-face centre offset from the bottom-face centre, in
                local X/Y (mm).
            plan_rotation_deg: Local X bearing measured from East towards
                North, exactly as for :meth:`box`.
            label: Optional comment written above the primitive.
        """
        if height <= 0 or min(xbot, ybot) <= 0 or min(xtop, ytop) < 0:
            raise PMLValidationError(
                f"PYRAMID needs positive height and faces, got "
                f"{xbot}x{ybot} -> {xtop}x{ytop}, height={height}"
            )
        if not all(math.isfinite(v) for v in (xoff, yoff, plan_rotation_deg)):
            raise PMLValidationError(
                f"PYRAMID offsets/rotation must be finite, got "
                f"{xoff}, {yoff}, {plan_rotation_deg}"
            )
        if label:
            self.comment(label)
        self._lines.append("NEW PYRAMID")
        self._lines.append(f"XBOT {_fmt(xbot)}")
        self._lines.append(f"YBOT {_fmt(ybot)}")
        self._lines.append(f"XTOP {_fmt(xtop)}")
        self._lines.append(f"YTOP {_fmt(ytop)}")
        self._lines.append(f"HEIG {_fmt(height)}")
        if abs(xoff) > 1e-9:
            self._lines.append(f"XOFF {_fmt(xoff)}")
        if abs(yoff) > 1e-9:
            self._lines.append(f"YOFF {_fmt(yoff)}")
        rotation = plan_rotation_deg % 360.0
        if abs(rotation) > 1e-9:
            self._lines.append(
                f"ORI Z IS U AND X IS {_plan_direction(rotation)}"
            )
        else:
            self._lines.append("ORI Z IS U AND Y IS N")
        self._position(centre)
        self._close_primitive()
        self.primitive_count += 1
        return self

    def extrusion(
        self,
        position: Tuple[float, float, float],
        orientation: str,
        height: float,
        vertices: Iterable[Tuple[float, float]],
        *,
        level: Optional[Tuple[int, int]] = None,
        label: str = "",
    ) -> "PMLBuilder":
        """
        Native EXTRUSION positioned by its profile end plane.

        Args:
            position: (east, north, up) of the profile end plane.
            orientation: Orientation string, e.g. ``'Y IS N AND Z IS U'``.
            height: Length extruded along local +Z (mm).
            vertices: Ordered (x, y) coordinates of the 2D profile loop.
            level: Optional display level tuple (low, high).
            label: Optional comment written above the primitive.
        """
        if height <= 0:
            raise PMLValidationError(f"EXTRUSION needs positive height, got {height}")
        vert_list = tuple(vertices)
        if len(vert_list) < 3:
            raise PMLValidationError("EXTRUSION LOOP needs at least three vertices")
        if label:
            self.comment(label)
        east, north, up = position
        ori = " ".join(orientation.upper().split())
        self._lines.append("NEW EXTRUSION")
        self._lines.append(f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(up)}")
        self._lines.append(f"ORI {ori}")
        if level is not None:
            self._lines.append(f"LEVE {level[0]} {level[1]}")
        self._lines.append(f"HEIG {_fmt(height)}")
        self._lines.append("")
        self._lines.append("NEW LOOP")
        for x, y in vert_list:
            self._lines.append("NEW VERTEX")
            self._lines.append(f"POS E {_fmt(x)} N {_fmt(y)} U 0")
            self._lines.append("END")
        self._lines.append("END")
        self._lines.append("END")
        self.primitive_count += 1
        return self

    def circular_handrail(
        self,
        center_local: Tuple[float, float],
        radius: float,
        *,
        elevation: float = 0.0,
        name: Optional[str] = None,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        top_rail_height: float = 1250.0,
        mid_rail_height: float = 750.0,
        post_spacing: float = 1000.0,
        tangent_offset: float = 300.0,
        fillet_radius: float = 100.0,
        label: Optional[str] = None,
    ) -> "PMLBuilder":
        """
        Native structural circular handrail (HANDRA / RPATH) verified in E3D Design Mk3.1.

        Args:
            center_local: (East, North) local center of the circle.
            radius: Outer platform / tank rim radius (mm).
            elevation: Elevation offset (mm).
            name: Optional element name.
            position: Insertion origin (East, North, Up).
            top_rail_height: Top rail height (mm).
            mid_rail_height: Intermediate rail height (mm).
            post_spacing: Post spacing (mm).
            tangent_offset: Tangent return offset (mm).
            fillet_radius: Fillet radius on vertices (mm).
            label: Optional comment written above the element.
        """
        from .handrail_builder import build_circular_handrail

        if label:
            self.comment(label)
        macro_text = build_circular_handrail(
            center_local=center_local,
            radius=radius,
            elevation=elevation,
            name=name,
            position=position,
            top_rail_height=top_rail_height,
            mid_rail_height=mid_rail_height,
            post_spacing=post_spacing,
            tangent_offset=tangent_offset,
            fillet_radius=fillet_radius,
        )
        self._lines.extend(macro_text.strip().split("\n"))
        self.primitive_count += 1
        return self

    def rectangular_handrail(
        self,
        length_e: float,
        width_n: float,
        *,
        origin: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        elevation: float = 0.0,
        name: Optional[str] = None,
        top_rail_height: float = 1250.0,
        mid_rail_height: float = 750.0,
        post_spacing: float = 1000.0,
        tangent_offset: float = 300.0,
        fillet_radius: float = 100.0,
        show_kickplate: bool = True,
        label: Optional[str] = None,
    ) -> "PMLBuilder":
        """
        Native structural rectangular platform perimeter handrail.
        """
        from .handrail_builder import build_rectangular_handrail

        if label:
            self.comment(label)
        macro_text = build_rectangular_handrail(
            length_e=length_e,
            width_n=width_n,
            origin=origin,
            elevation=elevation,
            name=name,
            top_rail_height=top_rail_height,
            mid_rail_height=mid_rail_height,
            post_spacing=post_spacing,
            tangent_offset=tangent_offset,
            fillet_radius=fillet_radius,
            show_kickplate=show_kickplate,
        )
        self._lines.extend(macro_text.strip().split("\n"))
        self.primitive_count += 1
        return self

    # -- internals ------------------------------------------------------

    def _orient(self, axis: Axis) -> None:
        """
        Emit the ORI line. Always called before :meth:`_position`, which is what
        keeps Iron Rule 1 structural rather than advisory.
        """
        orientations = {
            "U": "ORI Z IS U AND Y IS N",
            "D": "ORI Z IS D AND Y IS N",
            "E": "ORI Z IS E AND Y IS U",
            "W": "ORI Z IS W AND Y IS U",
            "N": "ORI Z IS N AND Y IS U",
            "S": "ORI Z IS S AND Y IS U",
        }
        try:
            self._lines.append(orientations[axis.upper()])
        except KeyError:
            raise PMLValidationError(
                f"Unknown axis {axis!r}; expected one of {sorted(orientations)}"
            ) from None

    def _position(
        self,
        point: Tuple[float, float, float],
        *,
        axis: Optional[Axis] = None,
        extent: float = 0.0,
    ) -> None:
        """
        Emit a POS line, optionally converting a face datum to a centre datum.

        E3D positions CYLI and CONE by geometric centre, but callers supply the
        bottom-face point that engineering drawings dimension from.  Their
        centre lies half the axial extent along the primitive's own axis, so
        that shift is applied here once.  BOX centre points and DISH rim points
        pass through unchanged.

        Args:
            point: Bottom-face centre for CYLI/CONE; geometric centre for BOX;
                rim-plane centre for DISH.
            axis: The primitive's axis. ``None`` passes the point through
                unchanged, which is what BOX wants.
            extent: Axial size (mm). Half of it is the offset applied.

        For an oriented element this is only called after its ORI line. An
        unrotated BOX has no ORI and passes its centre directly.
        """
        east, north, up = point
        if axis is not None and extent:
            half = extent / 2.0
            # Offset along the axis the primitive was just oriented onto.
            delta = {
                "U": (0.0, 0.0, half),
                "D": (0.0, 0.0, -half),
                "E": (half, 0.0, 0.0),
                "W": (-half, 0.0, 0.0),
                "N": (0.0, half, 0.0),
                "S": (0.0, -half, 0.0),
            }[axis.upper()]
            east, north, up = east + delta[0], north + delta[1], up + delta[2]
        self._lines.append(f"POS E {_fmt(east)} N {_fmt(north)} U {_fmt(up)}")
        self._lines.append("")

    # -- output ---------------------------------------------------------

    def build(self) -> str:
        """
        Assemble the macro and validate it.

        Raises:
            PMLValidationError: if the assembled text contains PML2 syntax or an
                ORI/POS ordering fault. This is a defensive backstop - building
                only through this class should make it unreachable.
        """
        self.close_all()
        script = "\n".join(self._lines).rstrip() + "\n"
        problems = validate_pml(script)
        if problems:
            detail = "\n  ".join(problems)
            raise PMLValidationError(
                f"Generated macro failed PML1 validation:\n  {detail}"
            )
        return script
