# PML1 Syntax Reference

Every entry carries a status. **VERIFIED** = observed working in E3D Design
Mk3.1.11.0 or traced to AVEVA's own PML library. **RECOMMENDED** = sound practice.
**EXPERIMENTAL** = unproven; never rely on it silently.

Geometry semantics live in [iron-rules.md](iron-rules.md). This file is the
syntax lookup.

---

## Primitives — VERIFIED

All four position by **geometric centre** (IR-1). All rotational primitives take
`ORI` before `POS` (IR-2), with the axis of revolution on Z (IR-3).

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

No `ORI` required. Foundations, platforms, hoods, frames, motors, headbox
chambers, valve bodies.

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

- 2:1 elliptical approximation: `RADIUS ≈ DIAM`
- Flatter head: `RADIUS > DIAM`
- **Never** as a flat cover plate (IR-9)

To point a dish downward, invert the axis (`ORI Z IS D ...`); see
`PMLBuilder.dish_down`.

---

## Not available — VERIFIED to fail

These produce a syntax error in `$$MACRO` mode:

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
$$MACRO <full path to the .pml file>
```

If the current element is not a writable zone, element creation fails regardless
of macro correctness.

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

The unverified part is narrower than the old entry implied: whether the emitted
`CATR SPCOMPONENT` path resolves in **the receiving project's** catalogue. It is
site-dependent, which is why the binding pass is emitted commented-out.

---

## Promotion rules

Move an entry from EXPERIMENTAL to VERIFIED only with evidence: a macro that
loaded, or a citation into AVEVA's PML library with file and line. Confidence is
not evidence. On the first contradiction, downgrade or delete immediately — a
rule that is quietly wrong costs more than a missing one.
