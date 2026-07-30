# PML1 Syntax Reference

Every entry carries a status. **VERIFIED** = observed working in E3D Design
Mk3.1.11.0 or traced to AVEVA's own PML library. **RECOMMENDED** = sound practice.
**EXPERIMENTAL** = unproven; never rely on it silently.

Geometry semantics live in [iron-rules.md](iron-rules.md). This file is the
syntax lookup.

---

## Primitives — VERIFIED

CYLI, CONE and BOX position by **geometric centre**; DISH positions by its flat
rim / tangent plane (IR-1). All rotational primitives take `ORI` before `POS`
(IR-2), with the axis of revolution on Z (IR-3).

### CYLI — cylinder

```pml
NEW CYLI
DIAM 1800.0
HEIG 5400.0
ORI Z IS N AND Y IS U
POS E 26000.0 N 0 U 6000.0
```

Shell courses, rolls, dryer cylinders, pipes, nozzle necks, flanges, skirts,
stiffening rings, agitator shafts.

### BOX — rectangular prism

```pml
NEW BOX
XLEN 500.0      -- East dimension
YLEN 5400.0     -- North dimension
ZLEN 700.0      -- Up dimension
POS E 0 N 0 U 4500.0
```

No `ORI` is required for a world-axis-aligned BOX. Foundations, platforms,
hoods, frames, motors, headbox chambers, valve bodies.

For a BOX rotated in plan, set local Z vertical and local X to the required
bearing **before POS**:

```pml
NEW BOX
XLEN 240.0      -- local radial length
YLEN 90.0       -- local tangential width
ZLEN 20.0
ORI Z IS U AND X IS E 30 N
POS E 20958.7 N -4711.5 U -274.0
```

The bearing form is quadrant-based (`E 30 N`, `N 30 W`, `W 30 S`,
`S 30 E`). Evidence: AVEVA's own
`spcwfitspecsel.pmlfrm:2423-2434` creates a dummy BOX and writes
`ORI Z IS $!zDir AND X IS $!xDir` before `POS`; the installed direction
handling documents arbitrary bearings such as `E 45 N`. This project parses
the emitted bearing back and verifies the rotated occupied bounds.

> **User-corrected 2026-07-30 (JK_Cooking_Tank_Build).** Circular-vessel anchor
> plates at non-cardinal bearings distorted when left on global E/N axes.
> Their local X must be radial and local Y tangential; deriving XLEN/YLEN from
> absolute E/N deltas is not a rotation.

### CONE — frustum

```pml
NEW CONE
DTOP 200.0
DBOT 700.0
HEIG 5500.0
ORI Z IS U AND Y IS N
POS E 0 N 0 U 1500.0
```

Conical roofs and bottoms, silo discharge cones, cyclones, headbox tapered inlet.
A cone with `DTOP` ≈ 0 is a true cone; keep a small non-zero top diameter where
the real equipment has a discharge opening.

### DISH — dished head

```pml
NEW DISH
DIAM 6500.0
HEIG 1500.0
RADIUS 6500.0    -- crown radius; controls curvature
ORI Z IS U AND Y IS N
POS E 0 N 0 U 53000.0
```

- `POS` is the flat rim / shell tangent plane; the apex is `HEIG` along Z
- 2:1 elliptical approximation: `RADIUS ≈ DIAM`
- Flatter head: `RADIUS > DIAM`
- **Never** as a flat cover plate (IR-9)

To point a dish downward, invert the axis (`ORI Z IS D ...`); see
`PMLBuilder.dish_down`.

---

## Not available — VERIFIED to fail

These produce a syntax error in `$M` macro mode:

| Primitive | Intended use | Use instead |
|-----------|--------------|-------------|
| `SNOT` | Slanted-bottom cylinder | Stacked `CYLI` + `BOX` slices |
| `PYRA` | Rectangular pyramid/frustum | Tapered stacked `BOX` slices |
| `CTOR` | Circular torus / ring | Arrayed small `CYLI` segments |
| `RTOR` | Rectangular torus / ring | Arrayed small `BOX` segments |
| `NCYLI` | Negative cylinder (hole) | Not available in macro mode |
| `NBOX` | Negative box (hole) | Not available in macro mode |

Boolean/negative primitives are unavailable in macro mode, which is why models
here are built additively. This is an advantage, not a limitation: additive
models stay editable and maintainable downstream.

---

## Structure — VERIFIED

```pml
NEW EQUI /203_TA_006
POS E 0.0 N 0.0 U 0.0      -- mandatory anchor, see IR-7

NEW SUBE /203_TA_006_SHELL
NEW CYLI
...
```

- Inline naming with the `/` prefix.
- **No** `END EQUI`, **no** `ENDS`. The next `NEW EQUI` closes the block.
- Names cannot contain hyphens.
- Comment token is `--`.

---

## Banned — VERIFIED to fail

```
!!Alert   $P   ENDS   END EQUI   NAME =   DESC =   !var =
COLLECT   UNSET   !!CE   !!WORLD
```

Plus the non-existent render prologue: `ALPHA HEADER`, `VAR 0`, `SUSPEND`,
`RESUME` (IR-4).

`wsb.pml_builder.validate_pml()` enforces this list and the ORI/POS ordering, and
`build()` raises rather than return a macro that would fail in E3D.

---

## Loading a macro — VERIFIED

In E3D Design, select a **writable ZONE** as the current element, then:

```
$M <full path to the .pml file>
```

**The command is `$M`, not `$$MACRO`.** This entry previously said `$$MACRO`,
which is not an E3D command at all. It aborts before executing a single line:

```
(47,50)   CP: Meaningless symbol(s) in command line
^^$$MACRO C:\...\JK-Project.pml
```

**Evidence.** `$$MACRO` has **zero** occurrences across ~6900 files in
`%AVEVA%\Everything3D3.1\PMLLIB` and `PMLUI`. `$M <path>` appears throughout —
`abaloadsymbols.pmlfnc` (`$M $!file`), `assydbs.pmlfrm`
(`$M %PMLLIB%\assembly\data\assembly_adp_library.txt`), `nuccatwgensec.pmlfrm`
(`$M /%PMLUI%/DES/STLWRK/DSTLSPEC`).

This mattered more than a wrong-command annoyance: the generated deliverable
carried `$$MACRO` in its own header, so the instruction shipped to the user was
one that could never work.

If the current element is not a writable zone, element creation fails regardless
of macro correctness.

### Querying an element interactively

A **bare path navigates** — there is no `GOTO` (that is a macro label jump,
`GOTO IDLN`) and no `NAVIGATE`. Then query:

```
/150lb_Ansi_Flanged/AAZFBB0KK
Q ATT                      -- all attributes
Q NAME ANSWER              -- named attributes only
```

The Command Window accepts **PML1 single commands only**. `collect`,
`do`/`enddo` and `!var =` assignment are rejected there with
`(47,15) CP: Syntax error` even though they are valid inside a `.pmlfrm`. To run
a multi-step query, write it to a `.mac` file of bare-path/`Q` pairs and load it
with `$M`.

---

## Attribute reference — VERIFIED

| Primitive | Size attributes |
|-----------|-----------------|
| `CYLI` | `DIAM`, `HEIG` |
| `BOX` | `XLEN`, `YLEN`, `ZLEN` |
| `CONE` | `DTOP`, `DBOT`, `HEIG` |
| `DISH` | `DIAM`, `HEIG`, `RADIUS` |

Units are millimetres throughout.

---

## Coordinate convention — RECOMMENDED

- **E (East)** — primary plant axis; machine direction for a paper machine
- **N (North)** — cross-machine direction
- **U (Up)** — vertical, ground floor at U = 0

For a paper machine: headbox at E = 0, reel at positive E, machine centreline at
N = 0.

---

## EXPERIMENTAL — do not rely on without testing

Nothing is currently promoted here. Entries added to this section must state what
is unproven and what evidence would settle it.

| Item | Claim | What would verify it |
|------|-------|----------------------|
| `EXTRU` | Extrusion for non-standard cross-sections | Load a macro using it in Design and confirm the profile renders |
| `SCTN` | Structural sections for platforms/ladders | Confirm specification reference resolves in macro mode |

`Do.txt` lists `EXTRU`, `NOZZLE` and `SCTN` as acceptable primitives. `EXTRU` and
`SCTN` have **not** been verified in macro mode here, so they stay experimental
until someone runs them.

**`NOZZLE` has been promoted to VERIFIED** — this entry previously claimed
nozzles were modelled as `CYLI` neck + flange pairs, which had not been true of
the production code for some time. The element form, its attribute set, its
`POS`-before-`ORI` order and its two-pass `CATR SPCOMPONENT` binding are all
verified against AVEVA's own macro data in
`%AVEVA%\PDMSUI\data\SMLdataPlant.pmlmac` (ten complete blocks at :48, :58,
:11018 …, with the binding pass at :13733). See
[IR-9a](iron-rules.md#ir-9a--a-nozzle-draws-nothing-until-a-catalogue-component-is-bound).

The binding is now **fully verified against the live project catalogue**. The
components under `/ANSI-NOZZLES` sit beneath a SELEC named `150lb_Ansi_Flanged`
and are named `AAZFBB0xx`; the bore is each SPCO's `Answer` attribute. Read them
with `list_nozzle_bores.mac` (bare path + `Q NAME ANSWER`, run with `$M`) — the
mapping is stored in `wsb.pml_builder.NOZZLE_BORE_COMPONENTS` and must be
re-read for any other receiving project.

---

## Promotion rules

Move an entry from EXPERIMENTAL to VERIFIED only with evidence: a macro that
loaded, or a citation into AVEVA's PML library with file and line. Confidence is
not evidence. On the first contradiction, downgrade or delete immediately — a
rule that is quietly wrong costs more than a missing one.
