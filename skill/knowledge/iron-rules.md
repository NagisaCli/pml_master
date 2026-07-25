# Iron Rules

**Status: VERIFIED on AVEVA E3D Design Mk3.1.11.0. Read this file on every job.**

These are not style preferences. Each one was written after a macro failed, a
model loaded wrong, or a user rejected the output. Violating any of them
produces either a macro E3D refuses to load, or — worse — a macro that loads
silently with the geometry in the wrong place.

Rules are ordered by how expensive the failure is.

---

## IR-1 — `POS` is the geometric CENTRE of every primitive

Applies to `CYLI`, `CONE`, `DISH` **and** `BOX`. There is no bottom-face datum
in E3D. An earlier revision of this knowledge base claimed one; following it put
every primitive half its own height too low.

```
A DN2000 x 1500 skirt whose base must sit on the slab at U 300:
  WRONG   POS ... U 300     -> spans U -450 .. 1050  (half underground)
  CORRECT POS ... U 1050    -> spans U  300 .. 1800
```

**Evidence.** AVEVA's own PML offsets by half the height to make a cylinder
*start* at a point:

```
pipeEditor.pmlfrm:7807
    !cylinderPosition = !position.offset(!direction, !height / 2)
```

**Why it is so damaging.** Each element has a different height, so each shifts by
a different amount. The result does not look like a uniform offset that you would
notice immediately — it looks like overlapping clutter, with shells, skirts,
heads and nozzles telescoped into one another.

**Do the conversion once, centrally.** Take the bottom-face point from the
drawing and add half the extent along the primitive's own axis in a single helper
(`wsb.pml_builder.PMLBuilder._position`). Never do this arithmetic at the call
site — scattered conversions are how half of them end up missing.

---

## IR-2 — `ORI` before `POS`

```
WRONG (POS before ORI rotates the coordinate vector -> severe drift):
NEW CYLI
DIAM 1800
HEIG 5400
POS E 26000 N 0 U 3800
ORI Z IS N AND Y IS U

CORRECT (establish axes first, then absolute world coordinates):
NEW CYLI
DIAM 1800
HEIG 5400
ORI Z IS N AND Y IS U
POS E 26000 N 0 U 3800
```

**There is no error message.** The macro loads and the element is simply in the
wrong place. This is why the ordering is enforced structurally in the builder
(`_orient()` is always called before `_position()`) and re-checked by
`validate_pml()` rather than left to review.

Attribute order for every primitive:

1. `NEW <TYPE>`
2. size attributes
3. `ORI` (for `CYLI`, `CONE`, `DISH`)
4. `POS`

### `NOZZLE` takes the OPPOSITE order — `POS` then `ORI`

This rule does **not** generalise to `NOZZLE`, and assuming it did aimed every
nozzle in the JK-Project model off its shell. A primitive's `POS` is consumed by
its own orientation; a nozzle's `POS` is expressed in its **owning equipment's**
frame, so orienting first rotates the frame the position is then read in.

**Evidence.** All ten `NOZZLE` blocks in AVEVA's own macro data are written
`POS` first, without exception:

```
PDMSUI\data\SMLdataPlant.pmlmac:48
    NEW NOZZLE /SML/HO9007/N1
    POS -X 1600.554687 -Y 1031.290527 -Z 150.034179
    ORI Y is -Z and Z is -X
    TEMP -100000 / PRES 0 / TPRESS 0 / HEIG 122 / DUTY unset
    END
```

Both orders load without error, so this is checked explicitly by
`_check_nozzle_pos_before_ori()`.

| Element family | Axis | Order |
|----------------|------|-------|
| `CYLI` / `CONE` / `DISH` | `Z` | `ORI` then `POS` |
| `NOZZLE` | `Y` | `POS` then `ORI` |

---

## IR-3 — Z is the axis of revolution

`ORI Z IS <axis>` sets the primitive's longitudinal axis. Putting the axis on Y
lays the vessel on its side.

**Evidence.** `gphFactory.pmlobj:632` builds a cylinder's orientation as
`Z IS $!normal AND X IS $!xDirection`, where `!normal` is the axis direction.

| Application | ORI |
|-------------|-----|
| Vertical tank, tower, chest, digester | `ORI Z IS U AND Y IS N` |
| Dryer cylinder, press roll (cross-machine) | `ORI Z IS N AND Y IS U` |
| Pipe in machine direction | `ORI Z IS E AND Y IS U` |

The second axis in the pair is only a roll reference; it does not affect a body
of revolution.

---

## IR-4 — Emit only commands that exist: there is no render prologue

`ALPHA HEADER OFF`, `VAR 0`, `SUSPEND` and `RESUME` are **not** E3D Design
commands. An earlier revision of this document prescribed them as an "anti-freeze"
prologue. They are not real: none appears as a command anywhere in AVEVA's PML
library under `%AVEVA_DESIGN_EXE%\pmllib\` — every occurrence of "suspend" there
is a PML method name or a word inside a comment.

Emitting any of them aborts the macro on that line:

```
(47,15)   CP: Syntax error
Command: ^^SUSPEND
```

A macro contains **element creation only**. Large macros load without any
directive; if load time is a concern, split the model by area into several
macros and run them separately.

The comment token is `--`, which is valid and used throughout AVEVA's own
`%AVEVA_DESIGN_EXE%\data\*.mac` files.

---

## IR-5 — PML1 only, zero tolerance

Macros must be 100% PML1 commands. Any of these causes an E3D load failure:

```
!!Alert   $P   ENDS   END EQUI   NAME =   DESC =   !var =
COLLECT   UNSET   !!CE   !!WORLD
```

There is no `END EQUI` or `ENDS` in PML1 — the next `NEW EQUI` implicitly closes
the preceding block.

This matters because PML2 is what most general-purpose PML examples on the
internet are written in, and it is the single most likely thing for a language
model to reach for by default. Check the output, not your intent.

---

## IR-6 — Tank equipment is set out from its bottom centre point

Tank-type equipment is positioned from the **bottom centre point** — the centre
of the equipment base. The model centre and bounding box centre must **not** be
used. This is the datum of the *equipment*, and is separate from IR-1, which is
the datum of each *primitive*; the builder converts between them.

For a skirt- or leg-supported vessel the datum is the foundation bearing plane at
the bottom of the support, not the bottom of the shell, since that is how the
coordinate is set out on site. **Nothing may be modelled below it.**

Generate geometry in a local frame whose origin is the bottom centre, then
translate by the installation coordinate. Do not compute absolute coordinates per
primitive — that is what produces global offsets.

**Verify geometrically, not textually.** Parse the emitted primitives, compute
each one's true extent from its centre datum and dimensions, and check that the
lowest point lands on the listed elevation; see
`wsb.tank_builder.verify_bottom_centre`. Searching the macro for the coordinate
as a `POS` string proves only that *some* primitive sits there — it passes a
model in which every element has the wrong datum.

---

## IR-7 — Anchor every EQUI at its owner origin

A bare `POS` is measured **with respect to the owner**, not the world; the world
form is `POS ... WRT /*`. Primitives written with world-absolute coordinates
therefore require their owning EQUI to sit at zero:

```
NEW EQUI /203_TA_006
POS E 0.0 N 0.0 U 0.0
```

Without an explicit `POS E 0 N 0 U 0` the EQUI takes whatever position the
current element happens to have, and the entire item shifts by that amount.

**Corollary: restructuring the tree can silently move geometry.** After any
hierarchy change, re-parse the macro and diff the primitive list — type,
dimensions, orientation, position — against the previous output to prove the
model is unchanged.

Names cannot contain hyphens: tag `203-TA-006` becomes `203_TA_006`.

---

## IR-8 — One EQUI per equipment item; every nozzle its own SUBE

```
NEW EQUI /203_TA_006          -- one per tag, never one per plant or area
  SUBE /203_TA_006_SUPPORT       skirt or legs, base ring
  SUBE /203_TA_006_SHELL         shell, roof, bottom
  SUBE /203_TA_006_N1            one SUBE per nozzle: neck + flange
  SUBE /203_TA_006_N2
  SUBE /203_TA_006_M1            manway
  SUBE /203_TA_006_ACCESS        stiffening rings, platforms
  SUBE /203_TA_006_INTERNALS     agitator, if fitted
```

Every nozzle gets its own `SUBE`, kept separate from the vessel body and from
other nozzles. That is what lets a piping designer select, attach to and modify
one connection without disturbing the shell or its neighbours. This is the
difference between a model that is merely correct and one that is *usable
downstream*.

The bulk plant-scale scripts under `examples/` use a flatter arrangement (one
EQUI with an area-level SUBE per zone). That is a demonstration of geometry
generation at scale, **not** the convention to follow for real equipment.

---

## IR-9 — DISH and CONE are closures, not shaping surfaces

1. Never use `DISH` as a flat cover plate — at large diameters (φ2000+) it
   creates a massive hemispherical bulge.
2. Correct uses of `DISH`: vessel heads, end covers, digester top/bottom
   closures, storage chest domes.
3. For surface subdivision use small `BOX` / `CYLI` slices arrayed along the
   curve — never a single giant `DISH`.

---

## IR-9a — A `NOZZLE` draws nothing until a catalogue component is bound

`NOZZLE` is a **catalogue element**, not a primitive. Its flange, bore and face
position all come from the `SPCO` component it references. Create one without
binding a component and it sits in the tree, reports the right position, passes
every geometric check — and **renders nothing at all**. That is what "the
nozzles are not displaying" means in practice, and no amount of checking `POS`,
`ORI` and `HEIG` will find it.

The binding cannot go inline in the `NEW NOZZLE` block. AVEVA's own data does it
as a **separate pass keyed by name**, after all the elements exist:

```
SMLdataPlant.pmlmac:13733
    OLD /SML/HO9007/N1
    CATR SPCOMPONENT /DICHTFL_C/ND-16RF-150
```

Note `CATR SPCOMPONENT`, not `SPRE SPCOMPONENT`. The earlier `SPRE` attempt
failed with `(2,109) Undefined name` and the fix applied then — dropping the
reference entirely — is what left all 114 nozzles invisible. **Removing a
reference that will not resolve does not make the element correct; it makes it
empty.**

Because the SPCO path belongs to the receiving project's catalogue, the builder
emits the pass **commented out** (`PMLBuilder.catref_pass()`), so a designer
uncomments one block rather than binding 114 nozzles by hand.

---

## IR-9b — `CYLI` is solid: there is no annulus primitive

E3D's `CYLI` has a diameter and no bore. Anything ring-shaped — a cage hoop, a
flange face ring, a stiffener — modelled as a single `CYLI` becomes a **solid
disc**, and if it is oriented along the axis it stands off on, that disc turns
its flat face to the vessel and hangs in clear air:

```
203-TA-006 ladder cage hoop, DN700 x 50 CYLI, ORI Z IS W
  shell face   E 12200
  disc spans   E 11800 .. 11850     -> floating 350 mm clear, up every tank
```

The user saw this as "a row of floating circular discs beside each equipment
item." Per IR-9 an annulus needs arrayed slices; per IR-10, assumed access steel
that no drawing dimensions is not worth a dozen primitives per hoop, so it is
**reported rather than drawn**.

**Check for detached geometry numerically.** Every radial primitive must either
touch the shell or overlap another that chains back to it — see
`test_no_primitive_floats_detached_from_its_tank`. A part legitimately carried
on a stalk (a side-entry agitator's motor, outboard of its mounting nozzle)
passes that check; a floating disc does not.

---

## IR-10 — Model only what you can justify

Do not invent structural detail to make a model look richer. Invented detail
clashes with real geometry during clash detection, and a designer cannot tell
your guess from project data.

Where the drawings dimension something, follow the drawings. Where they do not,
model the minimum process-logical set and flag it as a Reference Value. If you
cannot justify a feature from data, a drawing, or documented prototype
knowledge — leave it out and say so in the Outstanding Issues.

---

## Pre-delivery checklist

Run through this before returning any macro:

- [ ] `POS` treated as geometric centre for **all** primitives, converted centrally (IR-1)
- [ ] `ORI` precedes `POS` for every `CYLI` / `CONE` / `DISH` (IR-2)
- [ ] `POS` precedes `ORI` for every `NOZZLE` — the opposite order (IR-2)
- [ ] Every `NOZZLE` has a catalogue binding pass, or it renders nothing (IR-9a)
- [ ] No ring modelled as a single `CYLI`; no detached geometry (IR-9b)
- [ ] Axis of revolution on Z (IR-3)
- [ ] Zero render directives: `SUSPEND`, `RESUME`, `VAR 0`, `ALPHA HEADER` (IR-4)
- [ ] Zero PML2 syntax (IR-5)
- [ ] Bottom centre point verified **numerically**, not by string match (IR-6)
- [ ] Every `EQUI` explicitly at `POS E 0 N 0 U 0`; no hyphens in names (IR-7)
- [ ] One EQUI per tag; one SUBE per nozzle (IR-8)
- [ ] No `DISH` used as a flat plate (IR-9)
- [ ] Every assumed value labelled as a Reference Value with its basis (IR-10)
- [ ] Nothing modelled below the foundation bearing plane (IR-6)

---

## Adding a rule

A new Iron Rule earns its place only if it (a) caused a real failure and (b)
generalises beyond one project. Record the symptom and the evidence, not just the
fix — the symptom is what a future reader will recognise. One-off project quirks
belong in that project's log instead.
