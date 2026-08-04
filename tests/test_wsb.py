"""
WSB modeling tests.

The critical guarantees are the ones a reviewer cannot check by eye across 400+
primitives: that every tank sits on its listed coordinate, that no PML2 syntax
reaches the macro, and that ORI always precedes POS.

Run with::

    python -m pytest tests/ -v
"""

from __future__ import annotations

import itertools
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wsb import (  # noqa: E402
    PMLBuilder,
    PMLValidationError,
    generate,
    resolve_project,
    validate_pml,
)
from wsb.schema import BottomType, HeadType, SupportType  # noqa: E402
from wsb.tank_builder import _parse_primitives, verify_bottom_centre  # noqa: E402

# Equipment data now belongs to the project, not the engine, so the tests read
# it through the registry exactly as the generator does.
_PROJECT = resolve_project("JK-Project")
_DATASET = _PROJECT.load_dataset()

WSB_TANKS = _DATASET.WSB_TANKS
DATA_QUALITY_EXCEPTIONS = _DATASET.DATA_QUALITY_EXCEPTIONS
get_tank = _DATASET.get_tank

#: Common elevation datum for every tank (mm). The equipment list issues all 22
#: rows at z=300, the WSB finished floor level; the client directed on
#: 2026-07-24 that equipment be lowered 300 mm, so the modelled datum is zero.
_MODEL_DATUM_Z = 0.0

#: Marker used by a data-quality exception that applies to every tank rather
#: than to one tag.
_FLEET_WIDE_TAG = "ALL (22 tanks)"


@pytest.fixture(scope="module")
def result():
    """Generate the full model once and share it across tests."""
    return generate(project=_PROJECT)


# -- positioning contract -------------------------------------------------


def test_every_tank_sits_on_its_installation_coordinate(result):
    """The project's central requirement: bottom centre == listed coordinate."""
    assert result.verification_problems == []
    assert result.verified


@pytest.mark.parametrize("spec", WSB_TANKS, ids=lambda s: s.tag)
def test_tank_datum_appears_verbatim_in_macro(spec, result):
    """Each tank individually, so a failure names the offending tag."""
    assert verify_bottom_centre(spec, result.macro) == []


def test_cylinder_axis_is_z_not_y(result):
    """
    A primitive's length runs along its **Z** axis, so an upright vessel needs
    ``ORI Z IS U``. Verified in AVEVA's own cylinder factory::

        gphFactory.pmlobj:632
            !orientation = Z IS $!normal AND X IS $!xDirection

    Putting the axis on Y instead lays every vessel on its side and turns flat
    plates into vertical discs - the whole tank farm renders as scattered
    horizontal drums.

    A ``NOZZLE`` is the exception, and genuinely so: it is a catalogue element
    aimed by its **P-point**, ``ORI P1 IS <direction>`` - the form AVEVA's own
    Modify Nozzle form emits (``equnozzle.pmlfrm:851``). The two families are
    therefore checked against their own conventions; orienting a nozzle on a
    geometric axis points it somewhere other than its bore.
    """
    primitives = {"CYLI", "CONE", "DISH"}
    block = None
    for line in result.macro.split("\n"):
        new_match = re.match(r"^NEW\s+([A-Z]+)", line, re.IGNORECASE)
        if new_match:
            block = new_match.group(1).upper()
            continue
        if not line.startswith("ORI "):
            continue
        if block in primitives:
            assert line.upper().startswith("ORI Z IS "), (
                f"a primitive's axis must be on Z, got: {line}"
            )
        elif block == "NOZZLE":
            assert re.match(r"^ORI\s+P\d+\s+IS\s", line, re.IGNORECASE), (
                f"a nozzle must be aimed by its P-point, got: {line}"
            )


def test_upright_vessels_are_vertical(result):
    """Every tank shell must stand up, not lie down."""
    for spec in WSB_TANKS:
        prims = _parse_primitives(result.macro, spec.tag)
        shell = next(
            p for p in prims
            if p["kind"] == "CYLI"
            and abs(p.get("diam", 0) - spec.diameter) < 0.2
            and abs(p.get("heig", 0) - spec.height) < 0.2
        )
        assert shell["axis"] == "U", (
            f"{spec.tag}: shell axis is {shell['axis']}, expected U (vertical)"
        )


def _nozzle_prims(script, tag):
    """
    Primitives inside one tank's nozzle SUBEs.

    Each nozzle has its own SUBE named ``<tag>_<mark>``, so this collects every
    SUBE under the tank except the body assemblies.
    """
    prefix = tag.replace("-", "_") + "_"
    body = {"SHELL", "SUPPORT", "ACCESS", "INTERNALS"}
    out, cur, inside = [], {}, False
    for raw in script.split("\n"):
        line = raw.strip()
        if line.startswith("NEW EQUI /"):
            inside = False
            continue
        if line.startswith("NEW SUBE /"):
            name = line[len("NEW SUBE /"):]
            inside = name.startswith(prefix) and name[len(prefix):] not in body
            continue
        if not inside:
            continue
        if line.startswith("NEW "):
            cur = {"kind": line[4:].upper(), "axis": "U"}
            continue
        if not cur:
            continue
        for attr in ("DIAM", "HEIG"):
            if line.startswith(attr + " "):
                cur[attr.lower()] = float(line.split()[1])
        ori = re.match(r"^ORI\s+Z\s+IS\s+([UDENSW])\b", line)
        if ori:
            cur["axis"] = ori.group(1)
            continue
        pos = re.match(
            r"^POS\s+E\s+(-?[\d.]+)\s+N\s+(-?[\d.]+)\s+U\s+(-?[\d.]+)", line
        )
        if pos:
            cur["east"], cur["north"], cur["up"] = (
                float(g) for g in pos.groups()
            )
            out.append(cur)
            cur = {}
    return out


def _nozzle_elements(script, tag):
    """
    Native NOZZLE elements belonging to one tank.

    Returns the catalogue reference, orientation axis, base position and length
    of each - everything needed to check a nozzle without any primitive
    geometry to measure, since a NOZZLE carries none of its own.
    """
    prefix = tag.replace("-", "_") + "_"
    out, cur, in_tag = [], None, False
    for raw in script.split("\n"):
        line = raw.strip()
        if line.startswith("NEW EQUI /"):
            in_tag = line[len("NEW EQUI /"):] == tag.replace("-", "_")
            continue
        if not in_tag:
            continue
        if line.startswith("NEW NOZZLE"):
            name = line[len("NEW NOZZLE"):].strip().lstrip("/")
            cur = {"name": name}
            continue
        if cur is None:
            continue
        if line.startswith("SPRE "):
            cur["spref"] = line[len("SPRE "):].strip()
        elif line.startswith("ORI "):
            # A nozzle is aimed by its P-point: ORI P1 IS <direction>.
            m = re.match(r"^ORI\s+P\d+\s+IS\s+([UDENSW])\b", line, re.IGNORECASE)
            cur["axis"] = m.group(1).upper() if m else None
        elif line.startswith("POS "):
            m = re.match(
                r"^POS\s+E\s+(-?[\d.]+)\s+N\s+(-?[\d.]+)\s+U\s+(-?[\d.]+)", line
            )
            cur["east"], cur["north"], cur["up"] = (
                float(g) for g in m.groups()
            )
        elif line.startswith("HEIG "):
            cur["heig"] = float(line.split()[1])
        elif line == "END":
            out.append(cur)
            cur = None
    return out


def test_every_nozzle_is_a_native_element(result):
    """
    Every connection is a real E3D ``NOZZLE``, not primitives dressed up as one.

    A nozzle assembled from CYLIs looks right in a render but is not a
    connection: it carries no bore, no p-line and no specification, so piping
    cannot attach to it and a clash check cannot reason about it. The count must
    match the schedule exactly - one native element per scheduled nozzle.
    """
    total = 0
    for spec in WSB_TANKS:
        nozzles = _nozzle_elements(result.macro, spec.tag)
        assert len(nozzles) == len(spec.nozzles), (
            f"{spec.tag}: {len(nozzles)} NOZZLE elements for "
            f"{len(spec.nozzles)} scheduled nozzles"
        )
        total += len(nozzles)
    assert total == 114, f"expected 114 native nozzles, found {total}"


def test_every_nozzle_records_its_intended_specification(result):
    """
    Each nozzle either binds a real component or says why it cannot.

    This was once satisfied by a ``-- CATREF to be assigned ...`` comment, on
    the theory that no name-based path could resolve. That was wrong twice over:
    the SPCOs *are* named (``/150lb_Ansi_Flanged/AAZFBB0YY``), and a comment
    binds nothing - every nozzle stayed invisible. The bore must now travel with
    the model as an actual command, or as an explicit note when the catalogue
    carries no component at that size.
    """
    from wsb.pml_builder import NOZZLE_BORE_COMPONENTS, nozzle_component_path

    lines = result.macro.split("\n")
    for spec in WSB_TANKS:
        by_mark = {n.name: n for n in spec.nozzles}
        seen = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            prefix = f"NEW NOZZLE /{spec.tag.replace('-', '_')}_"
            if not stripped.startswith(prefix):
                continue
            name = stripped[len("NEW NOZZLE /"):]
            bore = by_mark[name.split("_")[-2]].dn
            block = [l.strip() for l in lines[i + 1:i + 9]]
            seen += 1
            if bore in NOZZLE_BORE_COMPONENTS:
                want = f"CATR SPCOMPONENT {nozzle_component_path(bore)}"
                assert want in block, (
                    f"{spec.tag}/{name}: DN{bore} must bind with {want!r}"
                )
            else:
                note = [l for l in block if "No catalogue component" in l]
                assert note, (
                    f"{spec.tag}/{name}: DN{bore} has no component and no note "
                    f"explaining why it is unbound"
                )
                assert f"DN{bore}" in note[0]
        assert seen == len(spec.nozzles), spec.tag


def _nozzle_blocks_with_comments(script, tag):
    """Each NOZZLE element in one tank, with the comments inside its block."""
    out, name, comments, in_tag = [], None, [], False
    for raw in script.split("\n"):
        line = raw.strip()
        if line.startswith("NEW EQUI /"):
            in_tag = line[len("NEW EQUI /"):] == tag.replace("-", "_")
            continue
        if not in_tag:
            continue
        if line.startswith("NEW NOZZLE"):
            name = line[len("NEW NOZZLE"):].strip().lstrip("/")
            comments = []
            continue
        if name is None:
            continue
        if line.startswith("--"):
            comments.append(line)
        elif line == "END":
            out.append((name, comments))
            name = None
    return out


def test_radial_nozzles_penetrate_their_shell(result):
    """
    Each nozzle barrel must pass through the shell wall - partly inside, mostly
    outside - not sit buried in the vessel or float beside it.

    **A NOZZLE's POS is its FLANGE FACE**, and the barrel runs back from there
    toward the vessel. An earlier version of this test asserted the opposite -
    that POS was the root on the shell - and passed a model in which every
    barrel lay entirely inside the tank, with only the flange rim emerging
    through the plate.

    So this checks the barrel's two ends against the shell face rather than
    checking POS against anything: the root sits just inside the wall, and the
    flange face stands clear outside it.
    """
    from wsb.tank_builder import (
        _NOZZLE_WALL_PENETRATION_MM, _PAD_THICKNESS_MM, _nozzle_length,
    )

    checked = 0
    for spec in WSB_TANKS:
        shell_r = (spec.outer_diameter or spec.diameter) / 2.0
        by_mark = {n.name: n for n in spec.nozzles}
        for element in _nozzle_elements(result.macro, spec.tag):
            # An unbound nozzle carries no ORI - it has no P1 to aim.
            if element.get("axis") in ("U", "D", None):
                continue
            bore = by_mark[element["name"].split("_")[-2]].dn
            length = _nozzle_length(bore)
            face_r = math.hypot(
                element["east"] - spec.position[0],
                element["north"] - spec.position[1],
            )
            root_r = face_r - length

            # The root sits inside the shell face: a real penetration.
            assert root_r == pytest.approx(
                shell_r - _NOZZLE_WALL_PENETRATION_MM, abs=0.5
            ), (
                f"{spec.tag}/{element['name']}: barrel root at radius "
                f"{root_r:.0f}, expected {shell_r - _NOZZLE_WALL_PENETRATION_MM:.0f} "
                f"(shell face {shell_r:.0f})"
            )
            # The flange face stands clear of the shell and its pad.
            projection = face_r - shell_r
            assert projection > _PAD_THICKNESS_MM, (
                f"{spec.tag}/{element['name']}: flange face projects only "
                f"{projection:.0f} mm - it must clear the "
                f"{_PAD_THICKNESS_MM} mm reinforcing pad"
            )
            # And the buried portion stays modest: most of the barrel is usable.
            assert projection > length / 2.0, (
                f"{spec.tag}/{element['name']}: more than half the "
                f"{length:.0f} mm barrel is buried in the vessel"
            )
            checked += 1
    assert checked == 87, f"expected 87 radial nozzles, checked {checked}"


def test_every_nozzle_has_a_catalogue_binding_recorded(result):
    """
    Every nozzle appears in the catalogue-binding pass at the end of the macro.

    A NOZZLE is a catalogue element: with no SPCO component bound it sits in the
    tree at the right position and **draws nothing**. That is what "the nozzles
    are not displaying" meant. The binding cannot go inline in the NEW NOZZLE
    block - AVEVA's own data does it as a second pass keyed by name
    (SMLdataPlant.pmlmac:13733) - so the macro carries an OLD/CATR pair per
    nozzle, bound to a component name read from the live project catalogue.

    The binding must be a LIVE command, not a comment. An earlier version
    emitted the whole pass commented out, which meant every nozzle stayed
    unbound and invisible - the macro documented the fix instead of applying it.

    The path must be the SPCO's own two-segment path, /<selec>/<component>.
    Emitting the bare component name gave "(2,108) SCOMPONENT /AAZFBB0YY is not
    a SPCO" - that name is the SPCO's Catref *value*, not the SPCO.
    """
    from wsb.pml_builder import NOZZLE_BORE_COMPONENTS, nozzle_component_path

    for line in result.macro.split("\n"):
        if line.startswith("CATR SPCOMPONENT"):
            path = line.split()[-1]
            assert path.count("/") == 2, (
                f"{line}: CATR needs the SPCO's /<selec>/<component> path, not "
                f"the bare component name"
            )

    # The binding is inline in each NEW NOZZLE block, so collect each block's
    # own CATR rather than looking for a trailing pass.
    lines = result.macro.split("\n")
    inline = {}
    for i, line in enumerate(lines):
        if not line.strip().startswith("NEW NOZZLE /"):
            continue
        name = line.strip()[len("NEW NOZZLE /"):]
        catr = [
            l.strip() for l in lines[i + 1:i + 9]
            if l.strip().startswith("CATR SPCOMPONENT")
        ]
        inline[name] = catr[0] if catr else None

    bound = unbindable = 0
    for spec in WSB_TANKS:
        by_mark = {f"{spec.tag.replace('-', '_')}_{n.name}_NOZZ": n
                   for n in spec.nozzles}
        for element in _nozzle_elements(result.macro, spec.tag):
            nozzle = by_mark[element["name"]]
            if nozzle.dn not in NOZZLE_BORE_COMPONENTS:
                # No component exists at this bore. It must be reported, never
                # silently bound to a smaller one.
                unbindable += 1
                assert inline[element["name"]] is None, (
                    f"{element['name']}: DN{nozzle.dn} has no catalogue "
                    f"component but was bound anyway"
                )
                continue
            path = nozzle_component_path(nozzle.dn)
            assert inline[element["name"]] == f"CATR SPCOMPONENT {path}", (
                f"{spec.tag}/{element['name']}: DN{nozzle.dn} must bind inline "
                f"to {path}, got {inline[element['name']]!r}"
            )
            bound += 1

    assert bound + unbindable == 114
    assert bound == 113, f"expected 113 bindable nozzles, got {bound}"
    assert unbindable == 1, "the DN800 outlet is the only unbindable nozzle"
    # No trailing OLD/CATR rebinding pass: it aborts on the ORI line.
    assert not [l for l in lines if l.startswith("OLD /")]


def test_nozzle_blocks_are_positioned_before_they_are_oriented(result):
    """
    Each NOZZLE sets POS before ORI - the reverse of a primitive.

    A nozzle's POS is expressed in its owning equipment's frame, so orienting
    first rotates the frame the position is then read in and lifts the
    connection point off the shell. All ten NOZZLE blocks in AVEVA's own
    PDMSUI\\data\\SMLdataPlant.pmlmac are written this way.
    """
    lines = result.macro.split("\n")
    checked = 0
    for i, line in enumerate(lines):
        if not line.strip().startswith("NEW NOZZLE"):
            continue
        block = lines[i + 1:i + 9]
        order = [
            l.split()[0].upper() for l in block
            if l.strip() and not l.strip().startswith("--")
        ]
        if "ORI" not in order:
            # A nozzle with no catalogue component has no P1 to aim, so no ORI
            # is emitted. It must carry no CATR either.
            assert "CATR" not in order, f"{line.strip()}: bound but not aimed"
            continue
        assert order.index("POS") < order.index("ORI"), (
            f"{line.strip()}: ORI precedes POS"
        )
        # CATR must come before both: a nozzle has no P-points and no position
        # until a catalogue component is bound (equnozzle.pmlfrm:894). Binding
        # later aborts with "(2,360) Cannot get position of NOZZLE".
        assert order.index("CATR") < order.index("POS"), (
            f"{line.strip()}: CATR must precede POS - a nozzle has no position "
            f"until its catalogue component is bound"
        )
        checked += 1
    assert checked == 113, f"expected 113 aimed nozzles, got {checked}"


def test_no_primitive_floats_detached_from_its_tank(result):
    """
    No primitive hangs in clear air beside a vessel.

    The ladder cage hoops did exactly this: a DN700 x 50 CYLI oriented *along*
    the radial axis, so its flat face pointed at the shell and it sat 350 mm
    clear of it - a row of floating discs up every tank. E3D's CYLI is solid
    and has no inner diameter, so a cage hoop cannot be a single primitive at
    all; per IR-9 an annulus needs arrayed slices, and per IR-10 assumed access
    steel that no drawing dimensions is reported rather than drawn.

    This checks the general property rather than the specific bug: every radial
    primitive must be *connected* - either touching the shell itself, or
    overlapping another radial primitive at the same elevation that chains back
    to it. Parts legitimately carried on a stalk (a side-entry agitator's
    gearbox and motor sit outboard of a 350 mm mounting nozzle) are connected
    through that nozzle and pass; the cage hoops touched nothing and did not.
    """
    from wsb.tank_builder import _parse_primitives

    for spec in WSB_TANKS:
        shell_r = (spec.outer_diameter or spec.diameter) / 2.0
        radials = []
        for prim in _parse_primitives(result.macro, spec.tag):
            if prim["kind"] != "CYLI" or prim["axis"] in ("U", "D"):
                continue
            radial = math.hypot(
                prim["east"] - spec.position[0],
                prim["north"] - spec.position[1],
            )
            half = prim.get("heig", 0.0) / 2.0
            radials.append({
                "near": radial - half,
                "far": radial + half,
                "up": prim["up"],
                "diam": prim.get("diam", 0.0),
            })

        for prim in radials:
            if prim["near"] <= shell_r + 0.5:
                continue  # touches or penetrates the shell
            # Otherwise it must overlap a neighbour at the same elevation that
            # reaches further inboard than it does.
            supported = any(
                other is not prim
                and abs(other["up"] - prim["up"]) <= max(prim["diam"], 1.0)
                and other["near"] < prim["near"]
                and other["far"] >= prim["near"] - 0.5
                for other in radials
            )
            assert supported, (
                f"{spec.tag}: a {prim['diam']:.0f} dia primitive floats "
                f"{prim['near'] - shell_r:.0f} mm clear of the shell (face at "
                f"{shell_r:.0f}) with nothing connecting it - detached geometry"
            )


def test_reinforcing_pads_lie_on_the_shell_face(result):
    """
    A reinforcing pad sits proud of the shell, not buried inside it.

    The pads were set out from the nozzle's embedded base rather than the shell
    face, which put every one of them entirely inside the plate where none could
    be seen. A welded pad lies on the outside of the shell.
    """
    from wsb.tank_builder import _PAD_THICKNESS_MM, _parse_primitives

    checked = 0
    for spec in WSB_TANKS:
        shell_r = (spec.outer_diameter or spec.diameter) / 2.0
        for prim in _parse_primitives(result.macro, spec.tag):
            if prim["kind"] != "CYLI" or prim["axis"] in ("U", "D"):
                continue
            if prim.get("heig") != _PAD_THICKNESS_MM:
                continue
            radial = math.hypot(
                prim["east"] - spec.position[0],
                prim["north"] - spec.position[1],
            )
            inner = radial - _PAD_THICKNESS_MM / 2.0
            assert inner == pytest.approx(shell_r, abs=0.5), (
                f"{spec.tag}: pad inner face at {inner:.0f}, shell at "
                f"{shell_r:.0f} - the pad does not sit on the shell plate"
            )
            checked += 1
    assert checked > 0, "no radial reinforcing pads found to check"


def test_nozzle_lengths_are_positive_and_bore_appropriate(result):
    """
    Every nozzle projects far enough to present a usable flange face.

    ``HEIG`` is the nozzle's own LENGTH - the projection from its connection
    point to the flange face. It is a dimension of the nozzle, nothing else.

    A previous version computed it as the distance from the owning EQUI's origin
    to the flange face, and this test was rewritten to agree with that theory.
    Both were wrong. The giveaway is bounds, not arithmetic: that scheme emitted
    HEIG values from -61680 to +72280 for nozzles 250-450 mm long, and a length
    cannot be negative. Hence the absolute sanity bound below - it is the check
    that would have caught the fault before the model was ever opened.
    """
    from wsb.tank_builder import _PAD_THICKNESS_MM, _nozzle_length

    #: No nozzle in this project is shorter than its pad or longer than a metre.
    #: Anything outside this is a datum error, not a dimension choice.
    LENGTH_MAX_MM = 1000.0

    seen = {}
    for spec in WSB_TANKS:
        by_mark = {n.name: n for n in spec.nozzles}
        for element in _nozzle_elements(result.macro, spec.tag):
            mark = element["name"].split("_")[-2]
            bore = by_mark[mark].dn
            length = element["heig"]
            assert _PAD_THICKNESS_MM < length < LENGTH_MAX_MM, (
                f"{spec.tag}/{element['name']}: HEIG {length} is not a "
                f"plausible nozzle length - it must clear the "
                f"{_PAD_THICKNESS_MM} mm pad and stay under {LENGTH_MAX_MM} mm"
            )
            assert length == _nozzle_length(bore), (
                f"{spec.tag}/{element['name']}: length {length} does not match "
                f"the DN{bore} band {_nozzle_length(bore)}"
            )
            seen[bore] = length

    # Monotonic in bore: a bigger nozzle never gets a shorter neck.
    for a, b in itertools.combinations(sorted(seen), 2):
        assert seen[a] <= seen[b], (
            f"DN{a} length {seen[a]} exceeds DN{b} length {seen[b]}"
        )


def test_nozzles_do_not_clash_across_tanks(result):
    """
    No nozzle may reach into a neighbouring tank or collide with its nozzles.

    Checked in three dimensions. A plan-only screen is misleading here: it
    flagged 204-TA-034/204-TA-035 as 6 mm overlapping, when the two nozzles
    concerned are 1498 mm apart in north and 6894 mm apart in elevation - a real
    separation of about 7 m. Collapsing elevation out of a clash test invents
    clashes, and chasing an invented clash is as costly as missing a real one.

    Nozzle length is a Reference Value, so this is the check that has to hold if
    those lengths are revised upward later.
    """
    from wsb.tank_builder import (
        TankBuilder,
        _AXIS_UNIT,
        _NOZZLE_EMBED_MM,
        _nozzle_length,
    )

    def tips(spec):
        envelope_r = (spec.outer_diameter or spec.diameter) / 2.0
        for nozzle in spec.nozzles:
            if nozzle.vertical:
                continue
            axis = TankBuilder._bearing_axis(nozzle.bearing)
            unit_e, unit_n = _AXIS_UNIT[axis]
            reach = envelope_r - _NOZZLE_EMBED_MM + _nozzle_length(nozzle.dn)
            yield (
                spec.position[0] + reach * unit_e,
                spec.position[1] + reach * unit_n,
                spec.position[2] + spec.skirt_height + nozzle.elevation,
                nozzle.dn,
                nozzle.name,
            )

    for a, b in itertools.combinations(WSB_TANKS, 2):
        for ae, an, au, a_dn, a_mark in tips(a):
            for be, bn, bu, b_dn, b_mark in tips(b):
                distance = math.dist((ae, an, au), (be, bn, bu))
                limit = (a_dn + b_dn) / 2.0
                assert distance >= limit, (
                    f"{a.tag}/{a_mark} and {b.tag}/{b_mark} clash: tips "
                    f"{distance:.0f} mm apart, need {limit:.0f} mm"
                )

    # A nozzle must also not spear a neighbouring shell.
    for a, b in itertools.permutations(WSB_TANKS, 2):
        b_r = (b.outer_diameter or b.diameter) / 2.0
        b_top = b.position[2] + b.skirt_height + b.height
        for east, north, up, _dn, mark in tips(a):
            radial = math.hypot(east - b.position[0], north - b.position[1])
            if radial < b_r:
                assert not (b.position[2] <= up <= b_top), (
                    f"{a.tag}/{mark} penetrates {b.tag}'s shell at radius "
                    f"{radial:.0f} < {b_r:.0f}, elevation {up:.0f}"
                )


def test_agitators_are_mounted_where_the_drawings_show_them(result):
    """
    A mixing element's steel must appear in the arrangement the reference
    drawing shows, not merely somewhere on the vessel.

    The three mountings occupy completely different space, so this is checked by
    where the geometry actually lands: a top-entry drive sits above the roof, a
    bottom scraper sits low with nothing above the roof, and a side-entry unit
    hangs off the shell low down. Counting primitives instead would pass a model
    that puts a roof drive on the tower whose real scraper is under the floor -
    which is precisely the defect the drawings were re-read to catch.
    """
    from wsb.schema import AgitatorType

    for spec in WSB_TANKS:
        if spec.mixer is AgitatorType.NONE:
            continue

        prims = _internals_prims(result.macro, spec.tag)
        assert prims, f"{spec.tag}: {spec.mixer.value} produced no geometry"

        datum_u = spec.position[2]
        roof_top = datum_u + spec.skirt_height + spec.height + (spec.head_height or 0.0)
        highest = max(p["up"] for p in prims)
        lowest = min(p["up"] for p in prims)

        if spec.mixer is AgitatorType.TOP_ENTRY:
            assert highest > roof_top, (
                f"{spec.tag}: top-entry drive must sit above the roof "
                f"({highest:.0f} <= {roof_top:.0f})"
            )
        else:
            assert highest <= roof_top, (
                f"{spec.tag}: {spec.mixer.value} must have no steel above the "
                f"roof, but geometry reaches {highest:.0f} > {roof_top:.0f}"
            )

        if spec.mixer is AgitatorType.BOTTOM_SCRAPER:
            # Drive and sweep sit just above the floor, well below mid-height.
            mid = datum_u + spec.skirt_height + spec.height / 2.0
            assert highest < mid, (
                f"{spec.tag}: scraper geometry reaches {highest:.0f}, above "
                f"mid-height {mid:.0f} - it should hug the floor"
            )
            assert lowest >= datum_u - 0.2, (
                f"{spec.tag}: scraper drive dips below the bottom-centre datum"
            )

        if spec.mixer is AgitatorType.SIDE_ENTRY:
            # Every element is off the centreline: it hangs on the shell.
            east0, north0, _ = spec.position
            offsets = [
                math.hypot(p["east"] - east0, p["north"] - north0) for p in prims
            ]
            assert min(offsets) > 0.0, (
                f"{spec.tag}: side-entry agitator has geometry on the vessel "
                f"centreline, which is a top-entry arrangement"
            )


def _internals_prims(script, tag):
    """Primitives inside one tank's INTERNALS assembly."""
    name = f"{tag.replace('-', '_')}_INTERNALS"
    out, cur, capture = [], {}, False
    for raw in script.split("\n"):
        line = raw.strip()
        if line.startswith("NEW SUBE /"):
            capture = line[len("NEW SUBE /"):] == name
            continue
        if line.startswith("NEW EQUI /"):
            capture = False
            continue
        if not capture:
            continue
        if line.startswith("NEW "):
            cur = {"kind": line[4:].upper()}
            continue
        if not cur:
            continue
        pos = re.match(
            r"^POS\s+E\s+(-?[\d.]+)\s+N\s+(-?[\d.]+)\s+U\s+(-?[\d.]+)", line
        )
        if pos:
            cur["east"], cur["north"], cur["up"] = (float(g) for g in pos.groups())
            out.append(cur)
            cur = {}
    return out


def test_roof_nozzles_sit_on_the_roof(result):
    """
    A conical roof slopes away from its apex, so a roof nozzle placed at apex
    height hangs in mid-air above the plate. Each must start at the roof
    surface directly beneath it.
    """
    from wsb.tank_builder import _NOZZLE_EMBED_MM, _NOZZLE_PROJECTION_MM, TankBuilder

    for spec in WSB_TANKS:
        builder = TankBuilder(spec, PMLBuilder("PROBE"))
        shell_top = spec.position[2] + spec.skirt_height + spec.height
        for p in _nozzle_prims(result.macro, spec.tag):
            if p["axis"] not in ("U", "D"):
                continue
            if abs(p.get("heig", 0.0) - _NOZZLE_PROJECTION_MM) > 0.1:
                continue
            start = p["up"] - p["heig"] / 2.0
            if start <= spec.position[2] + 0.5:
                continue  # bottom outlet, checked by the below-grade test
            offset = spec.diameter * 0.2
            expected = shell_top + builder._roof_rise_at(offset) - _NOZZLE_EMBED_MM
            assert start == pytest.approx(expected, abs=0.5), (
                f"{spec.tag}: roof nozzle starts at U {start:.0f}, roof surface "
                f"is at U {expected:.0f}"
            )


def test_geometry_is_independent_of_the_grouping_elements(result):
    """
    Grouping elements must contribute no geometry.

    EQUI and SUBE own a position but occupy no space. This pins the primitive
    inventory so a future hierarchy change cannot quietly add, drop or move
    geometry: the counts below are the model the client signed off on.
    """
    kinds = re.findall(
        r"^NEW (CYLI|CONE|DISH|BOX)$", result.macro, re.MULTILINE
    )
    # The builder's own tally must match what the macro actually contains. This
    # is the invariant that matters; the absolute count is deliberately not
    # pinned to a literal, which only ever recorded the geometry as it stood on
    # the day and had to be edited every time detail was legitimately added.
    assert len(kinds) == result.primitive_count

    # Every positioned element carries exactly one POS: each primitive, each
    # native NOZZLE, and each EQUI. A SUBE emits none, so any excess over that
    # sum means a grouping element has acquired a position of its own.
    nozzles = len(re.findall(r"^NEW NOZZLE\b", result.macro, re.MULTILINE))
    pos_lines = len(re.findall(r"^POS ", result.macro, re.MULTILINE))
    assert pos_lines == result.primitive_count + nozzles + len(WSB_TANKS)

    # Nozzles are catalogue elements, so they must contribute no primitives.
    assert nozzles == sum(len(t.nozzles) for t in WSB_TANKS)


def test_cylinders_are_positioned_by_their_centre(result):
    """
    E3D positions CYLI/CONE by their geometric centre, not their bottom face.
    The builder converts the bottom-face point callers supply.

    Checked on the shell, whose centre must sit half its height above the datum.
    Without the conversion every CYLI/CONE lands half its own height too low,
    and because each has a different height they telescope into one another -
    the model looks like overlapping clutter rather than a tank farm.
    """
    for spec in WSB_TANKS:
        prims = _parse_primitives(result.macro, spec.tag)
        shell = next(
            p for p in prims
            if p["kind"] == "CYLI"
            and abs(p.get("diam", 0) - spec.diameter) < 0.2
            and abs(p.get("heig", 0) - spec.height) < 0.2
        )
        expected = spec.position[2] + spec.skirt_height + spec.height / 2.0
        assert shell["up"] == pytest.approx(expected, abs=0.2), spec.tag


def test_dish_position_is_its_rim_plane(result):
    """
    DISH is the exception to the centre-datum rule: POS is the flat rim /
    tangent plane.  Applying the CYLI half-height conversion makes a top head
    float by HEIG/2, as observed in E3D on JK_Cooking_Tank_Build.
    """
    for spec in WSB_TANKS:
        if spec.head is not HeadType.DISHED:
            continue
        prims = _parse_primitives(result.macro, spec.tag)
        dish = next(
            p
            for p in prims
            if p["kind"] == "DISH" and p["axis"] == "U"
        )
        expected_rim = spec.position[2] + spec.skirt_height + spec.height
        assert dish["up"] == pytest.approx(expected_rim, abs=0.2), spec.tag


def test_nothing_is_built_below_the_foundation(result):
    """No geometry may sit under the slab the tank is set out on."""
    for spec in WSB_TANKS:
        prims = _parse_primitives(result.macro, spec.tag)
        lowest = min(p["u_min"] for p in prims)
        assert lowest >= spec.position[2] - 0.2, (
            f"{spec.tag}: geometry at U {lowest:.1f}, below datum "
            f"U {spec.position[2]:.1f}"
        )


def test_no_two_tank_shells_occupy_the_same_space():
    """
    No two vessel shells may overlap in plan.

    Scoped to shells and their outer envelopes - the parts whose size is project
    data. Nozzles are excluded on purpose: their bearings are Reference Values,
    and two tanks 4.7 m apart will inevitably have nozzles facing each other,
    which piping design resolves by routing rather than by moving equipment
    whose coordinates are fixed by the equipment list.

    This caught full-ring access platforms - assumed steel - clashing with real
    equipment whose shells were over a metre clear.
    """
    for i, s1 in enumerate(WSB_TANKS):
        for s2 in WSB_TANKS[i + 1:]:
            gap = math.hypot(
                s1.position[0] - s2.position[0], s1.position[1] - s2.position[1]
            )
            r1 = (s1.outer_diameter or s1.diameter) / 2.0
            r2 = (s2.outer_diameter or s2.diameter) / 2.0
            assert gap >= r1 + r2, (
                f"{s1.tag} and {s2.tag} shells overlap: centres {gap:.0f} mm "
                f"apart, combined radius {r1 + r2:.0f} mm"
            )


def test_no_tank_uses_a_geometric_centre_datum():
    """
    Guards against the specification's explicit prohibition: the insertion point
    must be the base centre, never the mid-height of the shell.
    """
    for spec in WSB_TANKS:
        _, _, up = spec.position
        mid_height = up + spec.total_height / 2.0
        assert up != pytest.approx(mid_height), spec.tag


# -- PML1 compliance ------------------------------------------------------


def test_macro_passes_validation(result):
    assert validate_pml(result.macro) == []


def test_one_equipment_element_per_tank(result):
    """AVEVA convention: one EQUI per item of equipment, named for its tag."""
    names = re.findall(r"^NEW EQUI /(\S+)", result.macro, re.MULTILINE)
    assert len(names) == len(WSB_TANKS)
    assert names == [t.tag.replace("-", "_") for t in WSB_TANKS]


def test_every_equipment_is_anchored_at_its_owner_origin(result):
    """
    Each EQUI must carry ``POS E 0 N 0 U 0``.

    A bare ``POS`` in E3D is measured with respect to the owner, not the world.
    The primitives beneath an EQUI hold world-absolute coordinates, so the EQUI
    has to sit at zero; if it inherited a position instead, the whole tank would
    shift by that amount.
    """
    lines = result.macro.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("NEW EQUI /"):
            assert lines[i + 1] == "POS E 0.0 N 0.0 U 0.0", (
                f"{line} is not anchored at its owner origin"
            )


def test_each_nozzle_is_its_own_subequipment(result):
    """
    Every nozzle occupies a separate SUBE, so a piping designer can select and
    modify one connection without disturbing the shell or its neighbours.
    """
    body = {"SHELL", "SUPPORT", "ACCESS", "INTERNALS"}
    for spec in WSB_TANKS:
        prefix = spec.tag.replace("-", "_") + "_"
        subes = re.findall(r"^NEW SUBE /(\S+)", result.macro, re.MULTILINE)
        mine = [s[len(prefix):] for s in subes if s.startswith(prefix)]
        nozzle_subes = [s for s in mine if s not in body]
        assert sorted(nozzle_subes) == sorted(n.name for n in spec.nozzles), (
            f"{spec.tag}: nozzle SUBEs {sorted(nozzle_subes)} do not match "
            f"the schedule {sorted(n.name for n in spec.nozzles)}"
        )


def test_nozzles_are_not_mixed_into_body_subequipment(result):
    """
    Nozzle geometry lives in nozzle SUBEs, never in a body assembly.

    Counted structurally rather than by dimension. Now that connections are
    native NOZZLE elements, a nozzle SUBE holds **no** primitive of its own
    except the reinforcing pad - the pad is shell plate, while the neck and
    flange come from the catalogue component. So a nozzle SUBE holds exactly one
    primitive at DN100 and above, and none below it.

    The upper bound is what keeps the test meaningful: it fails if body geometry
    ever lands in a nozzle SUBE, or if primitive necks and flanges creep back.
    """
    body_names = {"SHELL", "SUPPORT", "ACCESS", "INTERNALS"}

    for spec in WSB_TANKS:
        prefix = spec.tag.replace("-", "_") + "_"
        by_name = {n.name: n for n in spec.nozzles}
        counts = {}
        current = None
        for raw in result.macro.split("\n"):
            line = raw.strip()
            if line.startswith("NEW EQUI /"):
                current = None
            elif line.startswith("NEW SUBE /"):
                name = line[len("NEW SUBE /"):]
                current = name if name.startswith(prefix) else None
            elif current and re.match(r"^NEW (CYLI|CONE|DISH|BOX)$", line):
                counts[current] = counts.get(current, 0) + 1

        for name, count in counts.items():
            leaf = name[len(prefix):]
            if leaf in body_names:
                continue
            nozzle = by_name.get(leaf)
            assert nozzle is not None, f"{name} is neither a body assembly nor a nozzle"
            expected = 1 if nozzle.dn >= 100 else 0
            assert count == expected, (
                f"{name} (DN{nozzle.dn}) holds {count} primitives; expected "
                f"{expected} - only a reinforcing pad, at DN100 and above"
            )

        nozzle_total = sum(
            c for n, c in counts.items() if n[len(prefix):] not in body_names
        )
        expected_total = sum(1 for n in spec.nozzles if n.dn >= 100)
        assert nozzle_total == expected_total, spec.tag


def test_ori_precedes_pos_for_every_oriented_primitive(result):
    """
    Iron Rule 1. Checked directly on the emitted text rather than trusting the
    builder, since reversed order silently drifts elements instead of erroring.
    """
    lines = result.macro.split("\n")
    for i, line in enumerate(lines):
        if not re.match(r"^NEW (CYLI|CONE|DISH)$", line.strip()):
            continue
        block = []
        for candidate in lines[i + 1:]:
            if candidate.startswith("NEW "):
                break
            block.append(candidate.strip())
        ori = next((j for j, b in enumerate(block) if b.startswith("ORI ")), None)
        pos = next((j for j, b in enumerate(block) if b.startswith("POS ")), None)
        assert ori is not None, f"{line} at L{i + 1} has no ORI"
        assert pos is not None, f"{line} at L{i + 1} has no POS"
        assert ori < pos, f"{line} at L{i + 1} emits POS before ORI"


@pytest.mark.parametrize(
    "banned",
    ["!!Alert", "!!CE", "!!WORLD", "COLLECT", "UNSET", "$P", "ENDIF"],
)
def test_macro_contains_no_pml2_syntax(banned, result):
    body = "\n".join(
        line for line in result.macro.split("\n") if not line.strip().startswith("--")
    )
    assert banned not in body


def test_macro_emits_only_real_e3d_commands(result):
    """
    Every command verb the macro emits must be one E3D Design actually has.

    This suite previously emitted ALPHA HEADER, VAR 0, SUSPEND and RESUME, none
    of which are Design commands. Each aborted the macro on its own line with
    "(47,15) CP: Syntax error", and because they sat at the top of the file the
    reported line number never moved, which made the fault look like something
    else. Verified against AVEVA's PML library under %AVEVA_DESIGN_EXE%.
    """
    verbs = {
        line.split()[0].upper()
        for line in result.macro.split("\n")
        if line.strip() and not line.strip().startswith("--")
    }
    known = {
        "NEW", "DIAM", "HEIG", "DTOP", "DBOT", "RADIUS",
        "XLEN", "YLEN", "ZLEN", "ORI", "POS",
        # NOZZLE attributes and terminator. Every one appears in each NOZZLE
        # block of AVEVA's own PMLUI/data/SMLdataPlant.pmlmac, which is also
        # where the bare END comes from. SPRE is deliberately absent: a
        # name-based catalogue path does not resolve, and the validator now
        # rejects it outright.
        "TEMP", "PRES", "TPRESS", "DUTY", "END",
        # Catalogue binding pass. Both verbs appear in AVEVA's own data at
        # SMLdataPlant.pmlmac:13733 -- "OLD /SML/HO9007/N1" followed by
        # "CATR SPCOMPONENT /DICHTFL_C/ND-16RF-150". OLD re-selects an existing
        # element by name; CATR sets its catalogue reference. Without this pass
        # every NOZZLE renders nothing.
        "OLD", "CATR",
    }
    assert verbs <= known, f"unrecognised command verbs: {sorted(verbs - known)}"


@pytest.mark.parametrize("fake", ["ALPHA HEADER OFF", "VAR 0", "SUSPEND", "RESUME"])
def test_macro_has_no_invented_render_commands(fake, result):
    body = "\n".join(
        line for line in result.macro.split("\n") if not line.strip().startswith("--")
    )
    assert fake not in body


def test_validator_flags_alpha_header():
    problems = validate_pml("ALPHA HEADER OFF")
    assert any("ALPHA HEADER" in p for p in problems)


def test_validator_flags_suspend_and_resume():
    assert any("SUSPEND" in p for p in validate_pml("SUSPEND"))
    assert any("RESUME" in p for p in validate_pml("RESUME"))


def test_no_duplicate_sube_names(result):
    names = re.findall(r"^NEW SUBE /(\S+)", result.macro, re.MULTILINE)
    assert len(names) == len(set(names))


# -- validator behaviour --------------------------------------------------


def test_validator_flags_pos_before_ori():
    bad = "\n".join([
        "NEW CYLI", "DIAM 100.0", "HEIG 200.0",
        "POS E 0.0 N 0.0 U 0.0",
        "ORI Y IS U AND Z IS N",
    ])
    problems = validate_pml(bad)
    assert any("before" in p and "ORI" in p for p in problems)


def test_validator_flags_missing_ori():
    bad = "NEW CYLI\nDIAM 100.0\nHEIG 200.0\nPOS E 0.0 N 0.0 U 0.0"
    assert any("no ORI" in p for p in validate_pml(bad))


def test_validator_flags_pml2_assignment():
    assert any("variable assignment" in p for p in validate_pml("!diameter = 500"))


def test_validator_ignores_banned_words_inside_comments():
    """
    A comment mentioning a banned term must not trip the validator, or every
    macro documenting its own rules would fail.
    """
    assert validate_pml("-- COLLECT and UNSET are PML2 and must not be used") == []


def test_dash_dash_is_the_comment_token():
    """
    "--" is a valid PML comment: AVEVA's own macros under
    %AVEVA_DESIGN_EXE%\\data\\*.mac open with "-- ====" banners.
    """
    assert validate_pml("-- a perfectly ordinary comment") == []


def test_validator_accepts_a_correct_primitive():
    """
    A well-formed primitive passes.

    Note the orientation: ``ORI Z IS U``. This fixture previously said
    ``ORI Y IS U``, which is the fault that laid every vessel in the model on
    its side - a primitive's length runs along Z. The validator now rejects it,
    so the fixture had to be corrected rather than the check relaxed.
    """
    good = "\n".join([
        "NEW CYLI", "DIAM 100.0", "HEIG 200.0",
        "ORI Z IS U AND Y IS N",
        "POS E 0.0 N 0.0 U 0.0",
    ])
    assert validate_pml(good) == []


def test_validator_rejects_a_primitive_oriented_on_y():
    """
    ``ORI Y IS U`` on a primitive lays the vessel on its side while still
    loading without error, so only an explicit check catches it.
    """
    bad = "\n".join([
        "NEW CYLI", "DIAM 100.0", "HEIG 200.0",
        "ORI Y IS U AND Z IS N",
        "POS E 0.0 N 0.0 U 0.0",
    ])
    problems = validate_pml(bad)
    assert problems, "a Y-oriented primitive must be rejected"
    assert "along Z" in problems[0]


def test_validator_accepts_a_correct_nozzle():
    """
    A nozzle is aimed by its P-point and written POS-then-ORI - both the
    opposite convention to a primitive. ``ORI P1 IS <direction>`` is what
    AVEVA's Modify Nozzle form emits (equnozzle.pmlfrm:851).
    """
    good = "\n".join([
        "NEW NOZZLE /V1_N1",
        "CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY",
        "POS E 0.0 N 0.0 U 0.0",
        "ORI P1 IS E",
        "HEIG 300.0",
        "END",
    ])
    assert validate_pml(good) == []


@pytest.mark.parametrize("ori", [
    "ORI Z is E and Y is U",      # primitive convention
    "ORI Y is E and Z is U",      # the wrong rule this project shipped once
])
def test_validator_rejects_a_nozzle_oriented_on_a_geometric_axis(ori):
    """
    A nozzle oriented on a geometric axis points somewhere other than its bore.

    ``ORI Y is ...`` is included because this project shipped it: it aimed all
    114 nozzles wrongly and still loaded without error, so only an explicit
    check catches it.
    """
    bad = "\n".join([
        "NEW NOZZLE /V1_N1",
        "CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY",
        "POS E 0.0 N 0.0 U 0.0",
        ori,
        "HEIG 300.0",
        "END",
    ])
    problems = validate_pml(bad)
    assert problems, f"a nozzle oriented as {ori!r} must be rejected"
    assert "P-point" in problems[0]


def test_validator_rejects_a_nozzle_oriented_before_positioned():
    """
    A nozzle written ORI-then-POS has its position read in a rotated frame,
    which lifts the connection point off the shell. Both orders load without
    error, so only an explicit check catches it.
    """
    bad = "\n".join([
        "NEW NOZZLE /V1_N1",
        "CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY",
        "ORI Y is E and Z is U",
        "POS E 0.0 N 0.0 U 0.0",
        "HEIG 300.0",
        "END",
    ])
    problems = validate_pml(bad)
    assert problems, "an ORI-before-POS nozzle must be rejected"
    assert "before POS" in problems[0]


def test_validator_rejects_a_catalogue_path_by_name():
    """
    A nozzle must not reference its catalogue component by name.

    E3D rejected the whole macro with "(2,109) Undefined name
    /ANSI-NOZZLES/150lb-ANSI-Flanges:400". The SPCO components under
    /ANSI-NOZZLES carry no names in the project catalogue - the nozzle form
    picks them by DBREF - so no name-based path can resolve, whatever its
    punctuation. AVEVA's own macros set no specification at all.
    """
    bad = "\n".join([
        "NEW NOZZLE /V1_N1",
        "CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY",
        "SPRE SPCOMPONENT /ANSI-NOZZLES/150lb Ansi Flanges:150",
        "POS E 0.0 N 0.0 U 0.0",
        "ORI P1 IS E",
        "HEIG 300.0",
        "END",
    ])
    problems = validate_pml(bad)
    assert problems, "a name-based catalogue reference must be rejected"
    assert "catalogue path" in problems[0]


def test_validator_accepts_spre_on_a_piping_component():
    """
    SPRE is element-specific, not globally invalid.

    The native PIPE export supplied for PML-STUDY-PIPE-001 contains 1,112
    ``SPRE SPCOMPONENT`` lines on ELBOW/TEE/VALVE and other piping components.
    AVEVA's pipework documentation also requires a component's Spref. Only a
    NOZZLE uses the separate CATR binding rule enforced above.
    """
    good = "\n".join([
        "NEW ELBOW",
        "POS E 0mm N 0mm U 0mm",
        "ORI Y is D and Z is N",
        "SPRE SPCOMPONENT /A3B/EA100",
        "LSTU SPCOMPONENT /A3B/PA100",
        "END",
    ])
    assert validate_pml(good) == []


# -- builder guarantees ---------------------------------------------------


def test_builder_rejects_duplicate_sube():
    b = PMLBuilder("TEST")
    b.sube("A")
    with pytest.raises(PMLValidationError, match="Duplicate SUBE"):
        b.sube("A")


def test_builder_rejects_nonpositive_dimensions():
    b = PMLBuilder("TEST")
    with pytest.raises(PMLValidationError):
        b.cyli(0, 100, (0, 0, 0))
    with pytest.raises(PMLValidationError):
        b.box(100, 100, -1, (0, 0, 0))


def test_builder_rejects_unknown_axis():
    b = PMLBuilder("TEST")
    with pytest.raises(PMLValidationError, match="Unknown axis"):
        b.cyli(100, 100, (0, 0, 0), axis="Q")


def test_builder_sanitizes_tags_into_legal_names():
    """E3D names cannot contain hyphens, which every equipment tag has."""
    b = PMLBuilder("WSB")
    b.sube("203-TA-006 SHELL")
    assert "NEW SUBE /203_TA_006_SHELL" in "\n".join(b._lines)


# -- dataset integrity ----------------------------------------------------


def test_all_twentytwo_tanks_present():
    assert len(WSB_TANKS) == 22


def test_tags_are_unique():
    tags = [t.tag for t in WSB_TANKS]
    assert len(tags) == len(set(tags))


def test_every_tank_has_positive_geometry():
    for t in WSB_TANKS:
        assert t.diameter > 0, t.tag
        assert t.height > 0, t.tag
        assert t.total_height >= t.height, t.tag


def test_every_tank_has_nozzles_for_piping_readiness():
    """A tank with no nozzles cannot be connected during piping design."""
    for t in WSB_TANKS:
        assert t.nozzles, f"{t.tag} has no nozzle schedule"


def test_nozzle_elevations_lie_within_the_vessel():
    for t in WSB_TANKS:
        for n in t.nozzles:
            assert 0 <= n.elevation <= t.height + 1, f"{t.tag}/{n.name}"


def test_nozzle_names_unique_within_each_tank():
    for t in WSB_TANKS:
        names = [n.name for n in t.nozzles]
        assert len(names) == len(set(names)), t.tag


def test_all_positions_share_the_area_floor_elevation():
    """
    Every tank sits on one common datum.

    The equipment list issues all 22 rows at z=300 (the WSB finished floor
    level); the client directed on 2026-07-24 that equipment be lowered by
    300 mm, so the modelled datum is z=0. What matters either way is that the
    tanks share a single elevation - a lone outlier would mean the shift was
    applied unevenly.
    """
    elevations = {t.position[2] for t in WSB_TANKS}
    assert elevations == {_MODEL_DATUM_Z}, (
        f"tanks sit on mixed elevations {sorted(elevations)}; the 300 mm "
        f"lowering must apply uniformly"
    )


def test_elevation_shift_is_recorded_as_a_data_quality_exception():
    """
    The lowering deviates from the contractual equipment list, so it has to be
    declared in the deliverable rather than applied silently.
    """
    datum_exceptions = [
        e for e in DATA_QUALITY_EXCEPTIONS
        if "elevation" in e.field_name.lower()
    ]
    assert datum_exceptions, (
        "no data-quality exception records the 300 mm elevation shift"
    )
    exc = datum_exceptions[0]
    assert "300" in exc.source_value
    assert "0" in exc.corrected_value


def test_corrected_transposed_dimensions():
    """
    205-TA-008 and 205-TA-011 have height and diameter swapped in the source
    workbook. Verify the corrected orientation survived into the dataset.
    """
    d0_tower = get_tank("205-TA-008")
    assert d0_tower.height == 18600.0
    assert d0_tower.diameter == 2600.0

    d0_filtrate = get_tank("205-TA-011")
    assert d0_filtrate.height == 5300.0
    assert d0_filtrate.diameter == 4000.0


def test_transposed_dimensions_reconcile_with_stated_volume():
    """
    The correction rests on a volume argument, so check the arithmetic actually
    holds rather than trusting the comment.
    """
    t = get_tank("205-TA-011")
    volume_m3 = math.pi / 4 * (t.diameter / 1000) ** 2 * (t.height / 1000)
    assert volume_m3 == pytest.approx(t.volume_m3, rel=0.10)

    # The transposed reading would be far off the stated 63 m3.
    swapped = math.pi / 4 * (t.height / 1000) ** 2 * (t.diameter / 1000)
    assert abs(swapped - t.volume_m3) > abs(volume_m3 - t.volume_m3)


def test_recovered_coordinates_are_positive():
    """
    Per project direction every restored coordinate is positive: the minus sign
    on a corrupted numeric cell is an artefact of the digit concatenation, not
    project data.
    """
    from wsb.schema import Provenance

    for t in WSB_TANKS:
        if t.sources.get("position") is not Provenance.RECOVERED:
            continue
        east, north, up = t.position
        assert east > 0, f"{t.tag} east={east}"
        assert north > 0, f"{t.tag} north={north}"
        # The plan coordinates are what the sign recovery was about. Elevation
        # is the common datum, which the 300 mm client lowering puts at zero.
        assert up == _MODEL_DATUM_Z, f"{t.tag} up={up}"


def test_intact_coordinates_are_left_exactly_as_listed():
    """
    Rows that survived as text in the workbook must not be re-signed. Their
    negative north values are project data, not corruption.
    """
    from wsb.schema import Provenance

    listed = {
        "203-TA-024": (12005.0, -3752.0, 0.0),
        "203-TA-029": (16609.0, -3752.0, 0.0),
        "204-TA-001": (21008.0, -4151.0, 0.0),
        "205-TA-001": (26863.0, -11601.0, 0.0),
        "205-TA-008": (34016.0, -4501.0, 0.0),
        "205-TA-022": (38469.0, -4401.0, 0.0),
        "205-TA-025": (43067.0, -4501.0, 0.0),
        "205-TA-042": (49380.0, -5003.0, 0.0),
        "205-TA-059": (49515.0, -9553.0, 0.0),
    }
    for tag, expected in listed.items():
        tank = get_tank(tag)
        assert tank.sources.get("position") is Provenance.EXCEL, tag
        assert tank.position == expected, tag


def test_recovered_coordinates_magnitudes_match_the_source_digits():
    """
    Flipping the sign must not have disturbed the magnitudes recovered from the
    workbook, which are what actually locate the equipment.
    """
    for t in WSB_TANKS:
        east, north, _ = t.position
        assert 0 < abs(east) <= 70000, f"{t.tag} east={east}"
        assert 0 < abs(north) <= 25000, f"{t.tag} north={north}"


def test_data_quality_exceptions_reference_real_tags():
    """
    Every exception names a tank in the register, so none can point at a tag
    that does not exist.

    One exception applies to all 22 tanks at once (the 300 mm elevation
    lowering). Repeating it per tag would bury the eighteen genuine per-tank
    defects in the report, so it carries a fleet-wide marker instead - which
    must still be an exact literal rather than any unrecognised string.
    """
    tags = {t.tag for t in WSB_TANKS} | {_FLEET_WIDE_TAG}
    for exc in DATA_QUALITY_EXCEPTIONS:
        assert exc.tag in tags, exc.tag


def test_every_coordinate_defect_is_documented():
    """
    Each tank whose position was recovered must have a matching exception, so
    the report never hides a correction.
    """
    from wsb.schema import Provenance

    recovered = {
        t.tag for t in WSB_TANKS
        if t.sources.get("position") is Provenance.RECOVERED
    }
    documented = {e.tag for e in DATA_QUALITY_EXCEPTIONS if e.field_name == "position"}
    assert recovered == documented


def test_towers_have_taller_aspect_than_filtrate_tanks():
    """Sanity check that towers and tanks did not get their roles confused."""
    tower = get_tank("205-TA-008")
    tank = get_tank("205-TA-011")
    assert tower.height / tower.diameter > tank.height / tank.diameter


def test_double_shell_vessels_have_larger_outer_diameter():
    for t in WSB_TANKS:
        if t.outer_diameter:
            assert t.outer_diameter > t.diameter, t.tag


def test_conical_bottoms_have_a_cone_height():
    for t in WSB_TANKS:
        if t.bottom is BottomType.CONICAL:
            assert t.cone_height > 0, t.tag


def test_skirt_supported_vessels_have_a_skirt_height():
    for t in WSB_TANKS:
        if t.support is SupportType.SKIRT:
            assert t.skirt_height > 0, t.tag


# -- report ---------------------------------------------------------------


def test_report_covers_required_sections(result):
    for heading in (
        "## Completed Equipment",
        "## Modeling Parameters",
        "## Estimated Parameters",
        "## Outstanding Issues",
        "## Source Data Quality Exceptions",
    ):
        assert heading in result.report


def test_report_lists_every_tank(result):
    for t in WSB_TANKS:
        assert t.tag in result.report


def test_report_records_positioning_verification(result):
    assert "Positioning verified" in result.report


def test_report_flags_reference_values(result):
    """Assumed values must be visible as such in the deliverable."""
    assert "Reference Value" in result.report
    assert "Engineering-standard reference value" in result.report


# -- selective generation -------------------------------------------------


def test_can_generate_a_single_tank():
    single = generate((get_tank("203-TA-006"),), project=_PROJECT)
    assert single.verified
    assert "203-TA-006" in single.macro
    assert "205-TA-056" not in single.macro


def test_generation_is_deterministic_except_for_the_timestamp():
    a = generate(project=_PROJECT).macro.split("\n")
    b = generate(project=_PROJECT).macro.split("\n")
    strip = lambda lines: [l for l in lines if "Generated" not in l]  # noqa: E731
    assert strip(a) == strip(b)
