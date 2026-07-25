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
**E3D positions every primitive by its geometric centre**, including CYLI, CONE
and DISH. Verified in AVEVA's own PML, which offsets by half the height to make
a cylinder *start* at a given point::

    pipeEditor.pmlfrm:7807
        !cylinderPosition = !position.offset(!direction, !height / 2)

Engineering drawings, by contrast, dimension a vessel from its **bottom face**.
This builder accepts the bottom-face point that callers naturally have and
converts it to the centre datum E3D wants, in :meth:`PMLBuilder._position`.
Callers never do this arithmetic themselves - doing it per call site is what
produced a model where every element sat half its own height too low.

===========  =================  ==============================================
Primitive    E3D datum          What this builder accepts
===========  =================  ==============================================
``CYLI``     geometric centre   ``base`` - bottom-face centre, converted
``CONE``     geometric centre   ``base`` - bottom-face centre, converted
``DISH``     geometric centre   ``base`` - the flat rim, converted
``BOX``      geometric centre   ``centre`` - geometric centre, passed through
===========  =================  ==============================================
"""

from __future__ import annotations

import re
from typing import Iterable, List, Optional, Sequence, Tuple

__all__ = ["PMLBuilder", "PMLValidationError", "Axis", "validate_pml"]


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
#: AVEVA's own macro data shows the real arrangement. In
#: ``PDMSUI\data\SMLdataPlant.pmlmac`` the NOZZLE blocks carry no spec *at the
#: point of creation*, and the file then rebinds each one in a second pass by
#: name (``SMLdataPlant.pmlmac:13733``)::
#:
#:     OLD /SML/HO9007/N1
#:     CATR SPCOMPONENT /DICHTFL_C/ND-16RF-150
#:
#: So the reference is bound with ``CATR``, after creation, against a path that
#: exists in the receiving project's catalogue. This builder emits that second
#: pass - see :meth:`PMLBuilder.catref_pass`. The path is site-dependent, so it
#: is emitted commented-out with the exact command a designer uncomments once
#: the receiving project's nozzle catalogue is confirmed.
NOZZLE_SPEC = "ANSI-NOZZLES"
NOZZLE_TYPE = "150lb Ansi Flanges"

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
    # Catalogue reference by name. The SPCO components under /ANSI-NOZZLES are
    # unnamed, so E3D rejects any such path with "(2,109) Undefined name".
    # A nozzle's CATREF is bound after load, not in the macro - see NOZZLE_SPEC.
    (r"^\s*SPRE\s+SPCOMPONENT\b", "SPRE SPCOMPONENT (unresolvable catalogue path)"),
    (r"^\s*CATREF\s*/", "CATREF /path (unresolvable catalogue path)"),
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


def validate_pml(script: str) -> List[str]:
    """
    Check a PML macro for syntax that would break E3D, returning one message per
    problem found. An empty list means the script passed.

    Three classes of defect are checked:

    1. PML2 constructs that cause a load failure.
    2. PML2 variable assignment outside comments.
    3. ``POS`` emitted before ``ORI`` within a primitive block, which silently
       rotates the position vector and drifts the element.
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
    problems.extend(_check_element_axis_convention(lines))
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


def _check_element_axis_convention(lines: Sequence[str]) -> List[str]:
    """
    Verify each element family orients on the axis E3D actually uses.

    The two families genuinely differ, and both mistakes load without error:

    * A **primitive**'s length runs along Z (``gphFactory.pmlobj:632``), so a
      vertical vessel needs ``ORI Z IS U``. Orienting on Y lays it on its side.
    * A **NOZZLE**'s axis runs along Y. Every one of the ten NOZZLE blocks in
      ``PMLUI\\data\\SMLdataPlant.pmlmac`` orients Y first. Orienting a nozzle
      on Z aims it along its roll reference instead of its bore.

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
        if block in primitives and not re.match(
            r"^ORI\s+Z\s+IS\b", line, re.IGNORECASE
        ):
            problems.append(
                f"L{lineno}: NEW {block} (L{block_start}) orients on the wrong "
                f"axis - a primitive's length runs along Z -> {line}"
            )
        elif block == "NOZZLE" and not re.match(
            r"^ORI\s+Y\s+IS\b", line, re.IGNORECASE
        ):
            problems.append(
                f"L{lineno}: NEW NOZZLE (L{block_start}) orients on the wrong "
                f"axis - a nozzle's axis runs along Y -> {line}"
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
    oriented = {"CYLI", "CONE", "DISH"}

    block_prim: Optional[str] = None
    block_start = 0
    ori_at: Optional[int] = None
    pos_at: Optional[int] = None

    def close_block() -> None:
        if block_prim in oriented and pos_at is not None:
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
    """

    def __init__(self, name: str = "") -> None:
        self._lines: List[str] = []
        self._name = _sanitize(name)
        self._equi_names: set[str] = set()
        self._sube_names: set[str] = set()
        #: (name, bore, spec, generic type) per nozzle, for :meth:`catref_pass`.
        self._nozzle_bindings: List[Tuple[str, int, str, str]] = []
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

    def equi(self, name: str) -> "PMLBuilder":
        """
        Open an equipment element - one per item of equipment.

        The EQUI is explicitly anchored at its owner's origin. A bare ``POS`` in
        E3D is measured **with respect to the owner**, not the world (the world
        form is ``POS ... WRT /*``), so every primitive underneath is positioned
        relative to this element. Anchoring the EQUI at zero keeps the
        primitives' existing coordinates world-absolute and unchanged: without
        it the EQUI would take whatever position the current element happens to
        have, and the whole tank would shift by that amount.

        Args:
            name: Equipment name, unique within the macro.

        Raises:
            PMLValidationError: if the name has already been used.
        """
        clean = _sanitize(name)
        if clean in self._equi_names:
            raise PMLValidationError(
                f"Duplicate EQUI name {clean!r} - E3D would create two "
                f"indistinguishable elements"
            )
        self._equi_names.add(clean)
        self._lines.append(f"NEW EQUI /{clean}")
        self._lines.append("POS E 0.0 N 0.0 U 0.0")
        self.equipment_count += 1
        return self

    def sube(self, name: str) -> "PMLBuilder":
        """
        Open a sub-equipment grouping under the current EQUI.

        Args:
            name: Grouping name, unique within the macro.

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
        self._sube_names.add(clean)
        self._lines.append(f"NEW SUBE /{clean}")
        return self

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
        Native E3D ``NOZZLE`` element, positioned by its **base** on the shell.

        A NOZZLE is a catalogue element, not a primitive: its flange geometry,
        bore and face position come from the specification component it points
        at, so this emits no CYLI of its own. Only the length (``HEIG``) and the
        connection point are set here.

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

        * **A nozzle's axis is Y, not Z.** Every one of those ten blocks orients
          Y first. This is the opposite of a primitive, whose length runs along
          Z (see :meth:`_orient`), and getting it wrong points every nozzle in
          the wrong direction while still producing a loadable macro.
        * **There is no DIAM attribute.** The bore is a property of the
          catalogue component, so it is selected through the spec reference
          rather than set on the element.

        Args:
            name: Nozzle mark, appended to the current equipment name.
            bore_dn: Nominal bore (mm), used to select the catalogue component.
            height: Projection from the shell to the flange face (mm).
            base: (east, north, up) of the nozzle base on the vessel surface.
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
        self._orient_nozzle(axis)
        self._lines.append(f"HEIG {_fmt(height)}")
        # Process attributes, as carried by every NOZZLE in AVEVA's macro data.
        # Emitted unset/zero rather than invented: no design conditions are
        # given in the project data, and a fabricated design pressure is worse
        # than a blank one a process engineer will fill in.
        self._lines.append("TEMP -100000")
        self._lines.append("PRES 0")
        self._lines.append("TPRESS 0")
        self._lines.append("DUTY unset")
        self.comment(
            f"CATREF to be assigned from {spec} / {generic_type}, "
            f"bore DN{bore_dn}"
        )
        self._lines.append("END")
        self._lines.append("")
        # Record the nozzle for the catalogue-binding pass emitted at the end of
        # the macro. Without a bound component a NOZZLE has no geometry at all,
        # so this list is what turns the connection points into visible nozzles.
        self._nozzle_bindings.append((clean, bore_dn, spec, generic_type))
        self.nozzle_count += 1
        return self

    def catref_pass(self) -> "PMLBuilder":
        """
        Emit the catalogue-binding pass for every nozzle created in this macro.

        A ``NOZZLE`` is a catalogue element: its flange, bore and face position
        all come from the ``SPCO`` component it points at. Until one is bound the
        element exists in the tree and reports its position correctly but
        **draws nothing** - which is what "the nozzles are not displaying" means
        in practice.

        The binding cannot go inline in the ``NEW NOZZLE`` block. AVEVA's own
        macro data does it as a separate pass keyed by name
        (``SMLdataPlant.pmlmac:13733``)::

            OLD /SML/HO9007/N1
            CATR SPCOMPONENT /DICHTFL_C/ND-16RF-150

        and this method emits exactly that shape, one pair per nozzle.

        **The commands are emitted commented-out.** The SPCO path is a property
        of the receiving project's catalogue, not of this model: the components
        under ``/ANSI-NOZZLES`` in the catalogue read here are unnamed, so the
        path below is a template rather than a verified reference. Emitting it
        live would abort the macro on the first nozzle with ``(2,109) Undefined
        name`` - the failure this project already hit once. Emitting it as text
        the designer uncomments after confirming their own catalogue is what
        makes the binding a two-minute edit instead of 114 manual form entries.
        """
        if not self._nozzle_bindings:
            return self
        self.comment()
        self.banner("NOZZLE CATALOGUE BINDING PASS")
        self.comment(
            "A NOZZLE draws nothing until a catalogue component is bound to it."
        )
        self.comment(
            "Confirm the SPCO paths below against this project's own nozzle"
        )
        self.comment(
            "catalogue, then uncomment this section and re-run the macro."
        )
        self.comment(
            "Shape verified against AVEVA's own data, SMLdataPlant.pmlmac:13733."
        )
        self.comment()
        for clean, bore_dn, spec, generic_type in self._nozzle_bindings:
            self.comment(f"{clean}  -  {generic_type}, bore DN{bore_dn}")
            self.comment(f"OLD /{clean}")
            self.comment(f"CATR SPCOMPONENT /{spec}/DN{bore_dn}")
            self.comment()
        return self

    def _orient_nozzle(self, axis: Axis) -> None:
        """
        Emit a nozzle's ORI line, with the axis on **Y**.

        AVEVA's macro data orients every nozzle Y-first, so a nozzle pointing
        East is ``ORI Y is E and Z is U``. The second axis is a roll reference.
        This deliberately does not reuse :meth:`_orient`, which puts the axis on
        Z for primitives - the two element families genuinely differ, and
        sharing one method here would silently mis-aim every nozzle.
        """
        orientations = {
            "U": "ORI Y is U and Z is N",
            "D": "ORI Y is D and Z is N",
            "E": "ORI Y is E and Z is U",
            "W": "ORI Y is W and Z is U",
            "N": "ORI Y is N and Z is U",
            "S": "ORI Y is S and Z is U",
        }
        try:
            self._lines.append(orientations[axis.upper()])
        except KeyError:
            raise PMLValidationError(
                f"Unknown nozzle axis {axis!r}; expected one of "
                f"{sorted(orientations)}"
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
        self._position(base, axis=axis, extent=height)
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
    ) -> "PMLBuilder":
        """
        Box positioned by its **geometric centre**.

        Args:
            xlen: Size along East (mm).
            ylen: Size along North (mm).
            zlen: Size along Up (mm).
            centre: (east, north, up) of the geometric centre.
            label: Optional comment written above the primitive.
        """
        if min(xlen, ylen, zlen) <= 0:
            raise PMLValidationError(
                f"BOX needs positive dimensions, got {xlen}x{ylen}x{zlen}"
            )
        if label:
            self.comment(label)
        self._lines.append("NEW BOX")
        self._lines.append(f"XLEN {_fmt(xlen)}")
        self._lines.append(f"YLEN {_fmt(ylen)}")
        self._lines.append(f"ZLEN {_fmt(zlen)}")
        self._position(centre)
        self.primitive_count += 1
        return self

    # -- internals ------------------------------------------------------

    def _orient(self, axis: Axis) -> None:
        """
        Emit the ORI line. Always called before :meth:`_position`, which is what
        keeps Iron Rule 1 structural rather than advisory.
        """
        # The primitive's LENGTH runs along its Z axis. Verified in AVEVA's own
        # PML, where the cylinder factory builds its orientation from the axis
        # direction as Z:
        #
        #     gphFactory.pmlobj:632
        #         !orientation = Z IS $!normal AND X IS $!xDirection
        #
        # Putting the axis on Y instead lays every vessel on its side - the
        # second axis in each pair below is just a roll reference and does not
        # affect a body of revolution.
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
        Emit the POS line, converting a bottom-face datum to E3D's centre datum.

        E3D positions CYLI, CONE and DISH by their geometric centre, but callers
        supply the bottom-face point that engineering drawings dimension from.
        The centre lies half the axial extent along the primitive's own axis, so
        that shift is applied here - once, for every primitive - rather than at
        each call site.

        Args:
            point: Bottom-face centre for oriented primitives; geometric centre
                for BOX, which needs no conversion.
            axis: The primitive's axis. ``None`` passes the point through
                unchanged, which is what BOX wants.
            extent: Axial size (mm). Half of it is the offset applied.

        Only ever called after :meth:`_orient`.
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
        script = "\n".join(self._lines).rstrip() + "\n"
        problems = validate_pml(script)
        if problems:
            detail = "\n  ".join(problems)
            raise PMLValidationError(
                f"Generated macro failed PML1 validation:\n  {detail}"
            )
        return script
