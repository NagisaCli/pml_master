# Iron Rules

**Status: VERIFIED on AVEVA E3D Design Mk3.1.11.0. Read this file on every job.**

These are not style preferences. Each one was written after a macro failed, a
model loaded wrong, or a user rejected the output. Violating any of them
produces either a macro E3D refuses to load, or — worse — a macro that loads
silently with the geometry in the wrong place.

Rules are ordered by how expensive the failure is.

---

## IR-1 — `POS` is element-specific: centre for CYLI/CONE/BOX, rim for DISH,
end plane for EXTRUSION

`CYLI`, `CONE` and `BOX` use their **geometric centre**.  `DISH` uses its flat
rim / tangent-plane centre where the head joins the shell.  `EXTRUSION` uses
its **profile end plane**: the LOOP plane sits at `POS` and the solid extends
`HEIG` toward local +Z.  Do not apply the CYLI/CONE half-height conversion to a
DISH or an EXTRUSION.

An earlier revision of this knowledge base treated the drawing's bottom face as
the E3D datum for every element; following it put CYLI/CONE primitives half
their own height too low.

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

**DISH evidence.** In `JK_Cooking_Tank_Build`, the generated
`ACCUMULATOR_TANK` top head had `HEIG 1755.8` and the builder moved its `POS`
from the shell tangent plane `U 14407.3` to `U 15285.2`.  The macro loaded, but
the user's E3D view showed the head floating above the shell by exactly
`HEIG / 2 = 877.9 mm`.  Emitting `POS U 14407.3` seats the rim on the shell.

> **User-corrected 2026-07-30 (JK_Cooking_Tank_Build).** `DISH POS` is its
> rim/tangent plane.  This replaces the previous claim that DISH used a
> geometric-centre datum.

**EXTRUSION evidence — VERIFIED 2026-08-04 (E3D_Syntax_Lab).** Candidate
`PML-STUDY-EXTR-001/01` wrote `POS U 1000` with `HEIG 800`; the user measured
the occupied U range as 1000..1800 in E3D Design Mk3.1.11.0, exactly the
profile end-plane prediction.  A centre datum would have produced 600..1400 and
a far-face datum 200..1000.  AVEVA's own creation code agrees:
`dbenextrusion.pmlfrm:1448-1452` offsets the picked point by the **full
thickness** along -Z before `POSITION` (only an end-plane datum explains that),
and `mmmcounterweight.pmlobj:820-960` assigns `!!ce.position` from a frame's
`startPosition`/`endPosition` with `!!ce.heig` = the frame `length()`, while the
cylinder in the same method is centred with `proportion(0.5)`.

**Why it is so damaging.** Each element has a different height, so each shifts by
a different amount. The result does not look like a uniform offset that you would
notice immediately — it looks like overlapping clutter, with shells, skirts,
heads and nozzles telescoped into one another.

**Do the conversion once, centrally.** Take the bottom-face point for CYLI/CONE
from the drawing and add half the extent along the primitive's own axis in
`wsb.pml_builder.PMLBuilder._position`.  Pass BOX centre points, DISH rim
points and EXTRUSION profile end-plane points through unchanged
(`wsb.extrusion_builder`).  Never scatter this arithmetic across call sites.

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

| Element family | Aimed by | Order |
|----------------|----------|-------|
| `CYLI` / `CONE` / `DISH` | `ORI Z IS <axis>` | `ORI` then `POS` |
| `NOZZLE` | `ORI P1 IS <direction>` | `POS` then `ORI` |

### A `NOZZLE` is aimed by its P-point, not by a geometric axis

```
CORRECT   ORI P1 IS N
WRONG     ORI Y is N and Z is U     -- points somewhere other than the bore
```

**Evidence.** AVEVA's own Modify Nozzle form sets direction with
`ORI P1 IS $!direction` (`equnozzle.pmlfrm:851`) and reads it back as
`pdir[1]` (:858). `ORI P<n> IS` appears 1087 times across the installed library
and is macro-legal — emitted as literal macro text in `nucoldocech.pmlobj:663`.

**This project shipped `ORI Y is <axis> and Z is U` and it aimed all 114
nozzles wrongly** while loading without a single error. The rule was inferred
from `ORI Y is -Z and Z is -X` lines in `SMLdataPlant.pmlmac` without checking
what they meant. Two clues were already in the evidence:

* `/SML/XX9004/N2` in that same file reads `ORI Y is Y and Z is -Z`. If Y were
  the bore and Z a free roll reference, that is a pure 180° roll about the bore
  of an axisymmetric flange — meaningless.
* The `ORI Y is S and Z is U` lines cited as corroboration sit on `NEW FLANGE`
  elements (`designcheckerrules.pmlmac:1171`), a different element family.

**The general lesson:** a pattern seen in sample data is not a rule until you
find the code that *writes* it. Grepping for what a working file contains found
the wrong answer three times here; reading the form that generates it found the
right one.

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

## IR-3a — Off-axis rectangular hardware needs a local bearing

A rectangular plate on a circular vessel cannot remain aligned to global E/N
unless it lies on a cardinal axis. At a skew bearing, its local axes must follow
the equipment:

- local X = radial direction from the vessel centre;
- local Y = shell tangent;
- local Z = Up.

```pml
NEW BOX
XLEN 240
YLEN 90
ZLEN 20
ORI Z IS U AND X IS E 30 N
POS E ... N ... U ...
```

`ORI` still precedes `POS`. Do not calculate separate
`XLEN = abs(deltaE) + allowance` and `YLEN = abs(deltaN) + allowance`; that
changes the physical plate proportions at every bearing and produces a
world-aligned rectangle, not a rotated radial plate.

**Evidence.** AVEVA's installed `spcwfitspecsel.pmlfrm:2423-2434` creates a
BOX and emits `ORI Z IS $!zDir AND X IS $!xDir` before POS. In
`JK_Cooking_Tank_Build`, the user's E3D view exposed the geometry failure:
axis anchors appeared correct, while skew perimeter clamps were visibly twisted
and failed to meet the cylindrical shell tangentially.

> **User-corrected 2026-07-30 (JK_Cooking_Tank_Build).** Perimeter anchor
> baseplates, clamps, chairs and related gussets must rotate with their radial
> bearing. The previous model kept every BOX on global E/N axes.

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

**`CATR` must come FIRST, inline, immediately after `NEW NOZZLE`** — before
`POS`, before `ORI`, before anything. A nozzle's P-points *and its position*
come from the catalogue component, so until one is bound there is nothing to
position and no P1 to aim:

```
CORRECT                                     WRONG (aborts mid-load)
NEW NOZZLE /203_TA_006_N1_NOZZ              NEW NOZZLE /...
CATR SPCOMPONENT /150lb_Ansi_Flanged/...    POS E 15000 N 22610 U 7820
POS E 15000 N 22610 U 7820                  ORI P1 IS N
ORI P1 IS N                                 ... CATR far later ...
HEIG 450
```

```
(2,360)   Cannot get position of NOZZLE /203_TA_006_N1_NOZZ
Command: ORI P1 IS N
```

**Evidence.** AVEVA's creation form sets the catref as the statement straight
after `NEW NOZZ` (`equnozzle.pmlfrm:894`: `!!ce.catref = !this.nozzSpecRef`),
before height, temperature or anything else.

**The trap:** the `OLD` / `CATR` pass at `SMLdataPlant.pmlmac:13733` is a
*rebinding* of nozzles that already have a component — not a creation sequence.
Copying its shape put the binding at the end of the macro, which aborted the
first nozzle and **stopped the whole load at the first tank**. A partial model
is a much quieter failure than a syntax error: 21 of 22 tanks were simply
absent, with no error visible in the model at all.

A nozzle with no component must also carry **no `ORI`** — there is no P1 to aim.
Both orderings are enforced by `_check_nozzle_catref_first()`.

### A `NOZZLE`'s `POS` is its FLANGE FACE, not its root on the shell

The barrel runs **back** from `POS` toward the vessel, so the datum must sit a
full nozzle length *outside* where the barrel should meet the plate:

```
POS radius = shell_face − penetration + length
```

```
203-TA-006 N1, DN400, 450 long, shell face at N 22660:
  WRONG   POS N 22610   -> barrel spans 22160..22610, entirely INSIDE the tank;
                           only the flange rim shows where it pierces the plate
  CORRECT POS N 23010   -> barrel spans 22560..23010: 100 buried, 350 proud
```

Setting `POS` on the shell face (less a small embed) is the natural assumption
and it is wrong — it buries the whole barrel. The symptom is subtle: the nozzle
is at the right coordinate, aimed correctly, and still looks like a flange stuck
flat on the wall.

**Choose the penetration deliberately.** Offsetting by the full nozzle length
leaves the barrel merely touching the plate — no penetration, maximum
unsupported stub, unrealistic. `_NOZZLE_WALL_PENETRATION_MM = 100` buries enough
to read as a real wall penetration while leaving 150–350 mm projecting for
piping, depending on bore.

**Verify the barrel, not the datum.** Check both ends against the shell face:
root at `face − penetration`, flange face clear outside, and more than half the
barrel outside the vessel. A test that asserts where `POS` sits merely restates
whatever datum the code assumed — an earlier one did exactly that and passed a
model with all 87 barrels buried.

---

### `HEIG` is the nozzle's own length — bound it, don't theorise about it

`HEIG` is the projection from the connection point to the flange face. It is a
dimension of the nozzle and nothing else. For this project that is 250–550 mm.

**A revision of this file claimed `HEIG` was measured from the owning `EQUI`'s
origin.** It was wrong, and following it emitted values from **−61680 to
+72280 mm**, drawing the model as a thicket of metre-long tubes flying off the
vessels — far worse than the symptom it was meant to fix.

The reasoning that produced it: AVEVA's sample nozzles carry `HEIG 2.5` and
`HEIG 30`, which look impossible as projections, so the datum "must" be
something else. That inference was built on sample values whose vessels were
never examined, then confirmed by a test rewritten to expect the same thing.
**A test written after the theory only re-states the theory.**

**What would have caught it instantly is a bounds check, not a datum argument.**
A length cannot be negative and a 72 m nozzle is absurd — no knowledge of the
correct datum is needed to reject either. `_check_nozzle_heig_plausible()` now
enforces 1–2000 mm.

The general rule: when a physical quantity has obvious bounds, assert them.
Cheap bounds outrank elaborate checks that encode the same assumption as the
code they are checking.

**Emit the binding live, with real component names.** An intermediate version
emitted it commented out with a guessed `/ANSI-NOZZLES/DN<bore>` path, on the
reasoning that the path is site-specific. That fixed nothing: a commented
command does nothing, so every nozzle stayed unbound and invisible, and the
placeholder could never have resolved anyway. **Documenting a fix is not
applying one.**

**Pass the SPCO's own path, not its `Catref` value.** `Q ATT` prints both, one
line apart, and confusing them gives:

```
(2,108)   SCOMPONENT /AAZFBB0YY is not a SPCO
```

```
Name   /150lb_Ansi_Flanged/AAZFBB0YY   <- the SPCO: what CATR wants
Catref /AAZFBB0YY                      <- what the SPCO points at
```

The path is always two segments, `/<selec>/<component>` — matching AVEVA's own
`CATR SPCOMPONENT /DICHTFL_C/ND-16RF-150`. Note the SELEC name
(`150lb_Ansi_Flanged`) is *not* the specification name (`/ANSI-NOZZLES`); it is
the SELEC that owns the components, from `Q ATT`'s `Owner` line.

Read the real names out of the receiving catalogue instead. Navigate to a
component and query it (`Q ATT`, or `Q NAME ANSWER`); `Answer` is the bore.
`wsb/…/list_nozzle_bores.mac` does this for a whole family in one `$M` run, and
the result is stored in `NOZZLE_BORE_COMPONENTS`.

**Never infer a component name from its code.** In this catalogue the SPCOs are
`AAZFBB0xx` under a SELEC named `150lb_Ansi_Flanged`, and the ordering defeats
every reasonable guess:

```
AAZFBB011 = DN500     <- the two LARGEST bores come FIRST
AAZFBB033 = DN600
AAZFBB0DD = DN15      <- then the ladder restarts at the smallest
...
AAZFBB0MM = DN90      <- a bore that is not in the standard ANSI series
```

Three separate ordering hypotheses were tested against known points and all
failed. A wrong guess binds the wrong flange to a real connection and still
loads cleanly, which is worse than an unbound nozzle.

**A bore the catalogue does not carry is reported, never approximated.** The
JK-Project DN800 bottom outlet has no 150lb component (the family stops at
DN600). It is left unbound with an explicit note rather than downsized to DN600,
which would read as correct downstream and mislead the piping designer.

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

## IR-11 — How a rule earns the word "verified"

Most rules in this file replaced an earlier rule that was confidently wrong. The
failures below are not about E3D — they are about how the wrong answers got
believed, and they cost more time than any syntax error.

### 11a — Bounds before theories

When a quantity is physical, assert its bounds *first*. You do not need to know
the correct datum to reject a negative length.

```
HEIG values emitted under a mis-read datum:  -61680 .. +72280 mm
Actual nozzles:                                  250 .. 550 mm
```

A bounds check would have caught that in the generator, before the file was ever
sent. Instead a verification pass ran over it, confirmed the formula had been
applied consistently, and reported "all 87 verified" — because it checked
*consistency with the theory*, never *physical possibility*.

**Cheap bounds on a physical quantity outrank elaborate checks that share the
code's assumptions.** Lengths are positive. Diameters are positive. Equipment
does not sit below its foundation. Nozzles are shorter than a metre.

### 11b — A test written after the theory only restates the theory

Twice in one session a datum was mis-read, the test was rewritten to match, and
the suite went green over a broken model:

* the nozzle length test compared `HEIG` to the value the code had just computed;
* the shell-placement test asserted where `POS` sat, which merely re-stated
  whatever datum the code assumed.

**Test the property, not the formula.** Not "is `HEIG` what we computed" but
"does the barrel pass through the wall with most of it outside". A property test
fails when the theory is wrong; a formula test cannot.

### 11c — Read the code that *writes* a pattern, not the pattern

Sample data shows what some file contains, not what the rule is. Three wrong
conclusions came from grepping AVEVA's sample macros:

| Inferred from samples | Actually |
|-----------------------|----------|
| A nozzle's axis is Y | Aimed by `ORI P1 IS` (`equnozzle.pmlfrm:851`) |
| `CATR` goes in a trailing pass | Bound inline at creation (`equnozzle.pmlfrm:894`) |
| `HEIG` is measured from the owner origin | It is the nozzle's own length |

Each was settled by reading the form that *generates* nozzles. Two of the three
had contradicting evidence already visible in the same sample file — an
`ORI Y is Y and Z is -Z` that is meaningless as a bore direction, and `ORI Y`
lines that sit on `FLANGE` elements rather than nozzles.

**Before trusting a pattern, find the code that writes it.** If you cannot, say
the rule is unverified.

### 11d — "Fixed" means the user has seen it work

A macro that generates cleanly, validates cleanly and passes every test can still
be wrong in five different ways at once. Every fault in this session was caught
by the user loading the file and reporting what they saw — never by the test
suite alone.

State what was verified and how. "146 tests pass and the geometry checks are
clean" is honest; "the nozzles are fixed" is not, until someone has looked.

### 11e — Documenting a fix is not applying one

An entire catalogue-binding pass was emitted **commented out**, with a note
explaining what to uncomment. 228 comment lines, 0 executable commands, and every
nozzle still invisible.

If the generator can emit the working command, emit it. A comment is for
explaining a command, never for standing in place of one.

---

## Pre-delivery checklist

Run through this before returning any macro:

- [ ] `POS` uses the correct element datum: CYLI/CONE/BOX centre; DISH rim plane;
      EXTRUSION profile end plane (IR-1)
- [ ] `ORI` precedes `POS` for every `CYLI` / `CONE` / `DISH` (IR-2)
- [ ] `POS` precedes `ORI` for every `NOZZLE` — the opposite order (IR-2)
- [ ] Every `NOZZLE` aimed by `ORI P1 IS <direction>`, never a geometric axis (IR-2)
- [ ] Every `NOZZLE` binds `CATR` FIRST, inline — before `POS` and `ORI` (IR-9a)
- [ ] Nozzle `POS` is the FLANGE FACE; verify the barrel penetrates the wall (IR-9a)
- [ ] Nozzle `HEIG` is its own length, within plausible bounds (IR-9a)
- [ ] No ring modelled as a single `CYLI`; no detached geometry (IR-9b)
- [ ] Axis of revolution on Z (IR-3)
- [ ] Off-axis rectangular vessel hardware uses radial X / tangential Y and
      ORI-before-POS (IR-3a)
- [ ] Zero render directives: `SUSPEND`, `RESUME`, `VAR 0`, `ALPHA HEADER` (IR-4)
- [ ] Zero PML2 syntax (IR-5)
- [ ] Bottom centre point verified **numerically**, not by string match (IR-6)
- [ ] Physical quantities bounds-checked, not just formula-checked (IR-11a)
- [ ] Tests assert properties, not the formula the code just applied (IR-11b)
- [ ] Every "verified" claim traced to code that writes it, not sample data (IR-11c)
- [ ] No fix reported as complete before the user has loaded it (IR-11d)
- [ ] No command emitted commented-out in place of doing the work (IR-11e)
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
