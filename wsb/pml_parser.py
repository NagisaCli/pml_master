"""
PML Macro Parser
================
Reads back the macro text the builders emit, so verification can work from
what was actually written rather than from the builder's own bookkeeping.

Why this module exists
----------------------
Three verifiers grew their own copy of this parser -- ``tank_builder``,
``composite_builder`` and ``pump_builder`` -- and they drifted. Two carried
byte-identical ``_ORI_RE``/``_POS_RE`` definitions and the same geometry set
under two names (``_GEOMETRY_KINDS`` and ``_GEOMETRY``). The third matched a
fixed six-line block with a positional regex that encoded attribute *ordering*,
so any reordering inside :class:`~wsb.pml_builder.PMLBuilder` would have made
it silently match nothing.

That last failure mode is the dangerous one: a verifier that parses zero
primitives reports zero problems, and a broken safety net looks exactly like a
clean model. Parsing lives here once so a change to emission breaks one parser
loudly instead of quietly disabling a check.

Datum handling
--------------
The parser reproduces E3D's element-specific datums when computing extents,
because that is the whole point of verifying numerically:

* ``CYLI``/``CONE`` -- ``POS`` is the geometric centre; the element spans half
  its height either side along its axis.
* ``BOX`` -- ``POS`` is the geometric centre, spanning half of each of
  ``XLEN``/``YLEN``/``ZLEN``.
* ``PYRAMID`` -- ``POS`` is the geometric centre; the bottom rectangle sits at
  local ``-HEIG/2`` and the top rectangle, shifted by ``XOFF``/``YOFF``, at
  ``+HEIG/2`` (IR-1, verified 2026-08-19 on the native ``/P1501B-BASE``).
* ``DISH`` -- ``POS`` is the flat rim / tangent plane, and the element spans
  from there *along* its axis, not either side of it.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

__all__ = [
    "AXIS_VECTOR",
    "GEOMETRY_KINDS",
    "Bounds",
    "bounds_of",
    "equipment_name_to_element",
    "lowest_point",
    "parse_labelled",
    "parse_nozzles",
    "parse_plan_direction",
    "parse_primitives",
    "plan_half_extents",
    "pyramid_bounds",
    "PLAN_ROTATED_KINDS",
    "NativeNode",
    "parse_native_tree",
    "native_orientation_basis",
]


@dataclass
class NativeNode:
    """A native creation block, including local negative/profile children.

    Attribute text is retained verbatim so template adaptations do not lose
    vendor geometry that the simpler generated-primitive reader does not use.
    """

    kind: str
    name: Optional[str] = None
    attributes: List[Tuple[str, str]] = field(default_factory=list)
    children: List["NativeNode"] = field(default_factory=list)

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return next((value for attribute, value in self.attributes
                     if attribute == key.upper()), default)

    def set(self, key: str, value: str) -> None:
        key = key.upper()
        self.attributes = [(attribute, old) for attribute, old in self.attributes
                           if attribute != key]
        self.attributes.append((key, value))

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()


def parse_native_tree(script: str) -> List[NativeNode]:
    """Read balanced native NEW/END blocks, without flattening ownership.

    Pass creation text only: native INPUT/error wrappers and OLD rebinding
    passes must be separated by the caller. Unlike the simple primitive
    reader, this retains full attribute values, units, omitted zero vertex
    positions, and negative children inside their actual positive owner.
    """
    roots: List[NativeNode] = []
    stack: List[NativeNode] = []
    for lineno, raw in enumerate(script.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith(("--", "$*")):
            continue
        match = re.fullmatch(r"NEW\s+([A-Za-z][A-Za-z0-9]*)(?:\s+(/\S+))?",
                             line, re.IGNORECASE)
        if match:
            node = NativeNode(match.group(1).upper(), match.group(2))
            (stack[-1].children if stack else roots).append(node)
            stack.append(node)
        elif line.upper() == "END":
            if not stack:
                raise ValueError(f"L{lineno}: END has no open native element")
            stack.pop()
        else:
            if not stack:
                raise ValueError(f"L{lineno}: attribute outside a native element: {line}")
            parts = line.split(maxsplit=1)
            stack[-1].attributes.append((parts[0].upper(), parts[1] if len(parts) > 1 else ""))
    if stack:
        raise ValueError("Unclosed native elements: " + ", ".join(node.kind for node in stack))
    if not roots:
        raise ValueError("Native creation parser found no elements")
    return roots


def native_orientation_basis(orientation: Optional[str]) -> Dict[str, Tuple[float, float, float]]:
    """Resolve two native local-axis clauses, including quadrant angles.

    Examples: Y IS U AND Z IS E; Y IS E AND Z IS N 80 D. This reader is
    deliberately limited to the source-backed cardinal/quadrant forms.
    Unsupported or non-orthogonal orientations fail instead of defaulting.
    """
    vectors = {"E": (1., 0., 0.), "W": (-1., 0., 0.),
               "N": (0., 1., 0.), "S": (0., -1., 0.),
               "U": (0., 0., 1.), "D": (0., 0., -1.)}
    if not orientation:
        return dict(zip("XYZ", (vectors["E"], vectors["N"], vectors["U"])))
    text = re.sub(r"^ORI\s+", "", orientation.strip(), flags=re.I)
    basis = {}
    for clause in re.split(r"\s+AND\s+", text, flags=re.I):
        match = re.fullmatch(r"([XYZ])\s+IS\s+([EWNSUD])(?:\s+(\d+(?:\.\d+)?)\s+([EWNSUD]))?",
                             clause.strip(), re.I)
        if not match:
            raise ValueError(f"Unsupported native orientation: {orientation}")
        axis, first, degrees, second = match.groups()
        axis, first = axis.upper(), first.upper()
        if axis in basis:
            raise ValueError(f"Repeated native axis: {orientation}")
        value = vectors[first]
        if degrees is not None:
            other = vectors[second.upper()]
            if sum(x * y for x, y in zip(value, other)) != 0 or not 0 <= float(degrees) <= 90:
                raise ValueError(f"Invalid native quadrant: {orientation}")
            angle = math.radians(float(degrees))
            value = tuple(math.cos(angle) * x + math.sin(angle) * y for x, y in zip(value, other))
        basis[axis] = value
    if len(basis) != 2:
        raise ValueError(f"Native orientation needs two axes: {orientation}")
    a, b = list(basis.values())
    if abs(sum(x * y for x, y in zip(a, b))) > 1e-8:
        raise ValueError(f"Non-orthogonal native axes: {orientation}")

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    if "X" not in basis:
        basis["X"] = cross(basis["Y"], basis["Z"])
    elif "Y" not in basis:
        basis["Y"] = cross(basis["Z"], basis["X"])
    else:
        basis["Z"] = cross(basis["X"], basis["Y"])
    return basis

#: Element types that carry geometry. ``EQUI`` and ``SUBE`` are grouping
#: elements: they own a position but occupy no space, so treating one as
#: geometry would read a zero-sized primitive at the equipment origin.
GEOMETRY_KINDS = frozenset(
    {"CYLI", "CONE", "DISH", "BOX", "PYRAMID", "EXTRUSION"}
)

#: Unit vector for each E3D axis letter.
AXIS_VECTOR: Dict[str, Tuple[float, float, float]] = {
    "U": (0.0, 0.0, 1.0),
    "D": (0.0, 0.0, -1.0),
    "E": (1.0, 0.0, 0.0),
    "W": (-1.0, 0.0, 0.0),
    "N": (0.0, 1.0, 0.0),
    "S": (0.0, -1.0, 0.0),
}

#: Axial extent attributes read off a primitive.
_DIMENSION_ATTRIBUTES = (
    "DIAM", "HEIG", "XLEN", "YLEN", "ZLEN", "DTOP", "DBOT",
    "XBOT", "YBOT", "XTOP", "YTOP", "XOFF", "YOFF",
)

#: Elements whose local X may be turned to a plan bearing with
#: ``ORI Z IS U AND X IS <bearing>``. BOX is the verified form
#: (``spcwfitspecsel.pmlfrm:2423``); PYRAMID takes the same ORI command and
#: keeps local Z vertical, so its rectangles and offsets turn with local X.
PLAN_ROTATED_KINDS = frozenset({"BOX", "PYRAMID"})

ORI_RE = re.compile(r"^ORI\s+Z\s+IS\s+([UDENSW])\b", re.IGNORECASE)
NOZZLE_ORI_RE = re.compile(r"^ORI\s+P1\s+IS\s+([UDENSW])\b", re.IGNORECASE)
BOX_PLAN_ORI_RE = re.compile(
    r"^ORI\s+Z\s+IS\s+U\s+AND\s+X\s+IS\s+(.+)$", re.IGNORECASE
)
POS_RE = re.compile(
    r"^POS\s+E\s+(-?[\d.]+)\s+N\s+(-?[\d.]+)\s+U\s+(-?[\d.]+)", re.IGNORECASE
)

#: (e_min, e_max, n_min, n_max, u_min, u_max)
Bounds = Tuple[float, float, float, float, float, float]


def equipment_name_to_element(name: str) -> str:
    """
    The element name a display name becomes in the macro.

    ``PMLBuilder`` replaces every character that is illegal in an E3D name, so
    a verifier matching ``NEW EQUI /`` lines has to apply the same transform.
    Tank tags only ever need the hyphen rule; composite equipment names can
    contain spaces and punctuation, and collapsing runs keeps ``A -- B`` from
    becoming ``A___B``.
    """
    collapsed = re.sub(r"[^A-Za-z0-9_/]", "_", name.strip())
    return re.sub(r"_{2,}", "_", collapsed).strip("_")


def parse_primitives(
    script: str,
    equipment_name: str,
    *,
    simple_tag: bool = False,
    with_bounds: bool = False,
    with_lowest_point: bool = False,
) -> List[dict]:
    """
    Extract the geometry primitives belonging to one equipment item.

    Membership follows the macro's tree: everything from a ``NEW EQUI`` line
    up to the next one belongs to that item, which covers the vessel body and
    every nozzle ``SUBE`` beneath it.

    Args:
        script: The full macro text.
        equipment_name: Display name or tag of the item to collect.
        simple_tag: Match the name with the tank pipeline's hyphen-only rule
            rather than the full punctuation transform. Tank tags are matched
            this way, so ``205-TA-008`` becomes ``205_TA_008`` and nothing
            else changes.
        with_bounds: Attach a ``bounds`` key -- the axis-aligned extent in
            world coordinates, honouring BOX plan rotation.
        with_lowest_point: Attach a ``u_min`` key -- the lowest elevation the
            primitive occupies.

    Returns:
        One dict per primitive, carrying its kind, axis, dimensions and the
        emitted ``POS``, plus whichever derived keys were requested.
    """
    expected = (
        equipment_name.replace("-", "_")
        if simple_tag
        else equipment_name_to_element(equipment_name)
    )
    primitives: List[dict] = []
    current: dict = {}
    in_equipment = False

    extrusion_depth = 0
    negative_depth = 0

    for raw in script.splitlines():
        line = raw.strip()

        if line.startswith("NEW EQUI /"):
            # An EQUI opens a new item and closes the previous one.
            in_equipment = line[len("NEW EQUI /") :] == expected
            current = {}
            extrusion_depth = 0
            negative_depth = 0
            continue
        if not in_equipment:
            continue

        # A negative child must not overwrite the still-open positive extrusion
        # or be parsed as its LOOP vertices/pose. Keep the positive until its END.
        if negative_depth:
            if line.startswith("NEW "):
                negative_depth += 1
            elif line == "END":
                negative_depth -= 1
            continue
        if current.get("kind") == "EXTRUSION" and re.match(
            r"^NEW\s+(?:NCYLI\w*|NBOX|NCONE|NDISH|NPYRAMID|NXTR\w*)\b", line, re.I
        ):
            negative_depth = 1
            continue

        if line.startswith("NEW EXTRUSION"):
            current = {"kind": "EXTRUSION", "axis": "U", "vertices": []}
            extrusion_depth = 1
            continue

        if line == "NEW LOOP" and current.get("kind") == "EXTRUSION":
            extrusion_depth = 2
            continue

        if line == "NEW VERTEX" and current.get("kind") == "EXTRUSION":
            extrusion_depth = 3
            continue

        if line == "END" and current.get("kind") == "EXTRUSION":
            extrusion_depth -= 1
            if extrusion_depth <= 0:
                if with_bounds:
                    current["bounds"] = bounds_of(current)
                if with_lowest_point:
                    current["u_min"] = lowest_point(current)
                primitives.append(current)
                current = {}
                extrusion_depth = 0
            continue

        if line.startswith("NEW "):
            kind = line[4:].split()[0].upper() if len(line) > 4 else ""
            if kind in GEOMETRY_KINDS and kind != "EXTRUSION":
                current = {"kind": kind, "axis": "U"}
            else:
                current = {}
            continue
        if not current:
            continue

        for attribute in _DIMENSION_ATTRIBUTES:
            if line.startswith(attribute + " "):
                current[attribute.lower()] = float(line.split()[1])

        plan = BOX_PLAN_ORI_RE.match(line)
        if plan and current.get("kind") in PLAN_ROTATED_KINDS:
            current["plan_rotation_deg"] = parse_plan_direction(plan.group(1))

        if current.get("kind") == "EXTRUSION" and line.startswith("ORI "):
            current["orientation"] = line[4:].strip()
            continue

        orientation = ORI_RE.match(line)
        if orientation:
            current["axis"] = orientation.group(1).upper()
            continue

        position = POS_RE.match(line)
        if position:
            east, north, up = (float(value) for value in position.groups())
            if current.get("kind") == "EXTRUSION":
                if extrusion_depth == 3:
                    current.setdefault("vertices", []).append((east, north))
                else:
                    current.update(east=east, north=north, up=up)
            else:
                current.update(east=east, north=north, up=up)
                if with_bounds:
                    current["bounds"] = bounds_of(current)
                if with_lowest_point:
                    current["u_min"] = lowest_point(current)
                primitives.append(current)
                current = {}

    return primitives


def parse_nozzles(script: str, equipment_name: str) -> List[dict]:
    """
    Extract native ``NOZZLE`` elements from one equipment item.

    A nozzle is verified separately from the primitives because it is a
    catalogue element: its ``POS`` is the flange face and its geometry comes
    from the bound ``CATR SPCOMPONENT``, so an unbound nozzle draws nothing.
    """
    expected = equipment_name_to_element(equipment_name)
    nozzles: List[dict] = []
    current: dict = {}
    in_equipment = False

    for raw in script.splitlines():
        line = raw.strip()

        if line.startswith("NEW EQUI /"):
            in_equipment = line[len("NEW EQUI /") :] == expected
            current = {}
            continue
        if not in_equipment:
            continue

        if line.startswith("NEW NOZZLE /"):
            current = {"name": line[len("NEW NOZZLE /") :]}
            continue
        if line.startswith("NEW "):
            current = {}
            continue
        if not current:
            continue

        if line.startswith("CATR SPCOMPONENT "):
            current["catref"] = line[len("CATR SPCOMPONENT ") :]
        if line.startswith("HEIG "):
            current["height"] = float(line.split()[1])

        position = POS_RE.match(line)
        if position:
            current["face"] = tuple(float(value) for value in position.groups())

        orientation = NOZZLE_ORI_RE.match(line)
        if orientation:
            current["axis"] = orientation.group(1).upper()

        if line == "END":
            nozzles.append(current)
            current = {}

    return nozzles


def parse_labelled(
    script: str, label_fragment: str, kind: str, *, lookahead: int = 8
) -> List[dict]:
    """
    Primitives introduced by a generated comment containing ``label_fragment``.

    The pump verifier checks detail features -- cooling ribs, foot pads, skid
    rails -- that are identified by the comment the builder writes above them
    rather than by position in the tree.

    Attributes are matched **individually**, not as a fixed block. The previous
    implementation used one regex spanning six lines in a set order, so it
    encoded ``DIAM``-then-``HEIG``-then-``ORI``-then-``POS`` as a requirement.
    Reordering any attribute in the emitter would have made it match nothing,
    and a check that finds nothing reports no problems -- the verifier would
    have gone quiet instead of failing. Scanning attributes independently means
    a genuine emission change surfaces as a missing key, loudly.

    Args:
        script: The full macro text.
        label_fragment: Substring identifying the comment line.
        kind: Element type to collect, e.g. ``"CYLI"`` or ``"BOX"``.
        lookahead: How many lines after the comment to search.
    """
    kind = kind.upper()
    found: List[dict] = []
    lines = script.splitlines()

    for index, raw in enumerate(lines):
        if not raw.startswith("-- ") or label_fragment not in raw:
            continue

        current: Optional[dict] = None
        for line in lines[index + 1 : index + 1 + lookahead]:
            line = line.strip()
            if line.startswith("NEW "):
                if current is not None:
                    break  # a second element closes the labelled one
                if line[4:].split()[0].upper() != kind:
                    break  # the label does not introduce the requested kind
                current = {"kind": kind, "axis": "U"}
                continue
            if current is None:
                continue

            for attribute in _DIMENSION_ATTRIBUTES:
                if line.startswith(attribute + " "):
                    current[attribute.lower()] = float(line.split()[1])

            orientation = ORI_RE.match(line)
            if orientation:
                current["axis"] = orientation.group(1).upper()

            position = POS_RE.match(line)
            if position:
                east, north, up = (float(value) for value in position.groups())
                current.update(east=east, north=north, up=up)
                found.append(current)
                current = None
                break

    return found


def parse_plan_direction(direction: str) -> float:
    """
    Inverse of the builder's cardinal/quadrant BOX bearing formatter.

    Accepts a bare cardinal (``E``) or a quadrant bearing (``N 30 E``). The
    quadrant form is deliberately strict: only the four anticlockwise pairs the
    emitter actually produces are valid, and the angle must lie strictly inside
    the quadrant. A malformed bearing raises rather than silently resolving to
    0 deg, which would place a rotated BOX on the wrong axis and still verify.
    """
    tokens = direction.upper().split()
    cardinal = {"E": 0.0, "N": 90.0, "W": 180.0, "S": 270.0}
    if len(tokens) == 1 and tokens[0] in cardinal:
        return cardinal[tokens[0]]
    if len(tokens) != 3:
        raise ValueError(f"Unsupported BOX plan direction {direction!r}")
    first, angle_text, second = tokens
    angle = float(angle_text)
    quadrant_start = {
        ("E", "N"): 0.0,
        ("N", "W"): 90.0,
        ("W", "S"): 180.0,
        ("S", "E"): 270.0,
    }
    try:
        start = quadrant_start[(first, second)]
    except KeyError:
        raise ValueError(f"Unsupported BOX plan direction {direction!r}") from None
    if not 0.0 < angle < 90.0:
        raise ValueError(f"BOX quadrant angle must be 0..90, got {angle}")
    return start + angle


def bounds_of(primitive: dict) -> Bounds:
    """
    The axis-aligned world extent a primitive occupies.

    Applies E3D's element-specific datum: centre for BOX/CYLI/CONE, rim plane
    for DISH. A BOX rotated in plan is expanded to its enclosing box, so a
    containment check stays conservative rather than reporting a false fit.
    """
    east = primitive["east"]
    north = primitive["north"]
    up = primitive["up"]

    if primitive["kind"] == "EXTRUSION":
        verts = primitive.get("vertices", [(0.0, 0.0)])
        xs = [v[0] for v in verts]
        ys = [v[1] for v in verts]
        heig = primitive.get("heig", 0.0)
        return (
            east + min(xs),
            east + max(xs),
            north + min(ys),
            north + max(ys),
            up,
            up + heig,
        )

    if primitive["kind"] == "BOX":
        angle = math.radians(primitive.get("plan_rotation_deg", 0.0))
        cosine = abs(math.cos(angle))
        sine = abs(math.sin(angle))
        xlen = primitive.get("xlen", 0.0)
        ylen = primitive.get("ylen", 0.0)
        half_e = cosine * xlen / 2.0 + sine * ylen / 2.0
        half_n = sine * xlen / 2.0 + cosine * ylen / 2.0
        half_u = primitive.get("zlen", 0.0) / 2.0
        return (
            east - half_e,
            east + half_e,
            north - half_n,
            north + half_n,
            up - half_u,
            up + half_u,
        )

    if primitive["kind"] == "PYRAMID":
        return pyramid_bounds(
            (east, north, up),
            primitive.get("xbot", 0.0),
            primitive.get("ybot", 0.0),
            primitive.get("xtop", 0.0),
            primitive.get("ytop", 0.0),
            primitive.get("heig", 0.0),
            xoff=primitive.get("xoff", 0.0),
            yoff=primitive.get("yoff", 0.0),
            plan_rotation_deg=primitive.get("plan_rotation_deg", 0.0),
        )

    diameter = max(
        primitive.get("diam", 0.0),
        primitive.get("dbot", 0.0),
        primitive.get("dtop", 0.0),
    )
    radius = diameter / 2.0
    height = primitive.get("heig", 0.0)
    de, dn, du = AXIS_VECTOR[primitive.get("axis", "U")]

    if primitive["kind"] == "DISH":
        # DISH POS is the flat rim / tangent plane: the body extends from
        # there along the axis, not half a height either side of it.
        start = (east, north, up)
        end = (east + de * height, north + dn * height, up + du * height)
    else:
        half = height / 2.0
        start = (east - de * half, north - dn * half, up - du * half)
        end = (east + de * half, north + dn * half, up + du * half)

    e_min, e_max = sorted((start[0], end[0]))
    n_min, n_max = sorted((start[1], end[1]))
    u_min, u_max = sorted((start[2], end[2]))
    # Off-axis directions are bounded by the radius.
    if de == 0.0:
        e_min -= radius
        e_max += radius
    if dn == 0.0:
        n_min -= radius
        n_max += radius
    if du == 0.0:
        u_min -= radius
        u_max += radius
    return (e_min, e_max, n_min, n_max, u_min, u_max)


def pyramid_bounds(
    centre: Tuple[float, float, float],
    xbot: float,
    ybot: float,
    xtop: float,
    ytop: float,
    height: float,
    *,
    xoff: float = 0.0,
    yoff: float = 0.0,
    plan_rotation_deg: float = 0.0,
) -> Bounds:
    """
    Axis-aligned extent of a PYRAMID from its centre datum.

    The bottom rectangle (``xbot`` x ``ybot``) is centred on the local origin
    at ``-height/2``; the top rectangle (``xtop`` x ``ytop``) is centred at
    (``xoff``, ``yoff``) at ``+height/2``. Both rectangles turn with local X
    when the element is plan-rotated. The extent is the enclosing box of the
    eight corners, which is exact for the vertical span and conservative in
    plan -- the same convention as a rotated BOX.

    Shared by the writer (:class:`wsb.composite_schema.PrimitiveSpec`) and
    this parser so the two cannot disagree about where a PYRAMID sits.
    """
    east, north, up = centre
    angle = math.radians(plan_rotation_deg)
    cosine, sine = math.cos(angle), math.sin(angle)
    corners = []
    for cx, cy, sx, sy in (
        (0.0, 0.0, xbot, ybot),
        (xoff, yoff, xtop, ytop),
    ):
        for dx in (-sx / 2.0, sx / 2.0):
            for dy in (-sy / 2.0, sy / 2.0):
                lx, ly = cx + dx, cy + dy
                corners.append(
                    (cosine * lx - sine * ly, sine * lx + cosine * ly)
                )
    return (
        east + min(c[0] for c in corners),
        east + max(c[0] for c in corners),
        north + min(c[1] for c in corners),
        north + max(c[1] for c in corners),
        up - height / 2.0,
        up + height / 2.0,
    )


def lowest_point(primitive: dict) -> float:
    """
    The lowest elevation a primitive occupies, given its E3D datum.

    Used by the tank verifier to confirm nothing sits below its foundation
    (Iron Rule 11's bounds check).
    """
    return bounds_of(primitive)[4]


def plan_half_extents(primitive: dict) -> Tuple[float, float]:
    """
    Half the primitive's East and North footprint.

    The pump verifier checks that everything stays on the baseplate, which is
    a plan-view question and needs no elevation.
    """
    bounds = bounds_of(primitive)
    return (bounds[1] - bounds[0]) / 2.0, (bounds[3] - bounds[2]) / 2.0
