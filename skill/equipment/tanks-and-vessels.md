# Tank-Type Equipment

Vertical cylindrical vessels: tanks, chests, towers, reactors, receivers. The
dominant equipment class in a pulp mill and the most-modelled type in this skill.

**User-supplied parameters always override this file.**

---

## Anatomy

```
            ┌─────────┐   ← roof: flat / conical / dished
            │         │   ← top-mounted accessories
            │  shell  │   ← stiffening rings (external, on tall thin shells)
            │         │   ← nozzles: neck + flange
            │         │   ← manway (access, ~DN600, at grade or platform level)
            └─────────┘   ← bottom: flat / conical / dished
             ║       ║    ← support: skirt / legs / ground
        ─────╨───────╨────← foundation bearing plane = BOTTOM CENTRE POINT
```

The **bottom centre point** is the setting-out datum (IR-6): the centre of the
foundation bearing plane at the bottom of the support, not the bottom of the
shell. Nothing is modelled below it.

---

## Configuration by duty — VERIFIED in production (JK-Project, 22 tanks)

Configuration follows the equipment's process duty. This table drove 22 delivered
models:

| Equipment class | Roof | Bottom | Support | Notes |
|-----------------|------|--------|---------|-------|
| Filtrate / dilution tank | Conical | Flat | Ground | Atmospheric, often agitated |
| Feed tank | Dished | Dished | Skirt | Elevated above an MC pump |
| Oxygen / EOP reactor | Dished | Conical | Skirt | Upflow, pressurised, platforms |
| Bleaching tower (D0/D1) | Flat | Conical | Skirt | Flat roof carries top equipment |
| Blow tank | Conical | Conical | Skirt | Large vapour relief to cyclone |
| Storage tower | Conical | Dished | Ground | Double shell, bottom scraper |
| Washer dropleg | Flat | Conical | Legs | Barometric leg, >10 m for vacuum seal |
| Vent scrubber | Conical | Conical | Skirt | Packed column inside an outer shell |
| Air receiver | Dished | Dished | Legs | Pressure vessel, relief valve |

### Why the configuration follows the duty

- **Pressurised** → dished heads. Flat heads cannot carry internal pressure at
  these diameters.
- **Solids or pulp to be drained completely** → conical bottom.
- **Elevated for pump suction (NPSH)** → skirt.
- **Atmospheric, sits on a slab** → flat bottom, ground bearing.
- **Carries equipment on top** → flat roof.
- **Vapour to be collected centrally** → conical roof.

Reasoning from duty is more reliable than memorising the table; the table is the
worked result of it.

---

## Process logic — the most common engineering error

- **Upflow** (reactor, bleaching tower): fed at the **bottom** cone, discharges
  at the **top**.
- **Downflow / storage**: fed **high** on the shell, drawn from the **bottom**.

Nozzle elevations must follow the flow direction. Getting this backwards produces
a model that is geometrically perfect and process-nonsense.

Additionally: vents at the **high** point, drains at the **low** point, overflow
below the roof.

---

## Nozzles

**Never place nozzles arbitrarily.** Where reference drawings dimension them,
follow the drawings. Otherwise provide the minimum process-logical set — feed,
discharge, overflow, vent, drain, manway — sized to the duty, spread across
distinct bearings so future piping does not collide, and flagged as Reference
Values.

Model as a catalogue-backed native `NOZZLE`, each in its **own SUBE** (IR-8), so
a piping designer can attach to one connection without disturbing its
neighbours. Do not rebuild a placeholder nozzle from stacked `CYLI` neck,
flange, gasket and fastener primitives when a verified receiving-project
catalogue component is available.

> **User-corrected 2026-07-30 (JK_Cooking_Tank_Build).** Temporary cooking-area
> connections should be single native `NOZZLE` placeholders. The previous
> primitive neck/flange/bolt stacks were visually excessive and harder to
> replace uniformly.

Production constants (`wsb/tank_builder.py`) — RECOMMENDED:

| Feature | Value |
|---------|-------|
| Flange oversize on DN | +120 mm |
| Flange thickness | 40 mm |
| Manway | ~DN600, reachable from grade or a platform |

**Spread the bearings.** Nozzles stacked on one bearing are unusable downstream —
the pipes cannot all be routed. Distribute them around the shell.

---

## Support

**Skirt** — cylindrical shell from the bearing plane to the vessel bottom. Datum
is the skirt base. Used where the vessel is pressurised, elevated, or has a
conical bottom needing clearance.

**Legs** — typically 4, equally spaced. Datum is the base of the legs.
Each leg needs a physical load path at both ends: a top load-spreader/cap plate
and gussets into the vessel, plus a sole plate, grout/cleats and anchored foot at
the foundation. A bare rectangular post merely touching a curved cone is not a
credible support.

**Ground** — bottom bears directly on the slab. Datum is the bottom of the shell.
An external anchor stud must pass through a baseplate or clamp chair tied back
to the shell/skirt. A bolt standing beside the tank with no connecting plate has
no physical restraining function.

> **User-corrected 2026-08-10 (JK-Tank_Build / WSB).** For visual anchor bolts
> on a tank bottom, the "底盘" (bearing plate) boundary is the **widest short
> cylinder at the lowest elevation** — the exposed base ring or bottom plate
> that overhangs the shell — not the thinnest or innermost plate. Anchor bolts
> sit on that ring's exposed annulus, outside the shell wall, with the hex nut
> flush on the plate top and the stud embedded below into the foundation.
> Placing the bolt circle inside the shell footprint (or hanging the nut under
> the plate) reads as wrong in visual review. Nut size should scale with the
> tank (M30–M48 class), not stay a constant tiny fastener. Where a tank has
> two base rings (an inner one under an inner skirt/shell and an outer one
> under the outer shell), anchor on the OUTERMOST ring — the inner ring is
> not the visible 底盘 boundary.

For any baseplate, clamp, chair or gusset arranged around a circular shell, use
the attachment's **local radial/tangential frame**: the plate's long axis points
radially and the edge at the shell is tangential. Only the E/W/N/S locations can
look correct while remaining world-axis-aligned; every skew location needs a
real BOX orientation.

> **User-corrected 2026-07-30 (JK_Cooking_Tank_Build).** The previous perimeter
> anchors calculated BOX lengths from absolute E/N deltas and never rotated the
> boxes. Skew clamps consequently distorted and did not meet the vessel
> tangentially. Circular support hardware now carries its radial bearing and the
> bolt pattern rotates with it.

---

## Structural detail — RECOMMENDED

| Feature | Value | When |
|---------|-------|------|
| Stiffening ring projection | 120 mm | Tall thin shells, external |
| Stiffening ring depth | 200 mm | — |
| Platform width | 1200 mm | Where drawings show access |
| Platform thickness | 60 mm | — |
| Insulation thickness | 100 mm | Hot service, where modelled |
| Conical roof rise | 0.15 × diameter | No stated head height |
| Dished head rise | 0.25 × diameter | No stated head height |

Dished head rise of D/4 corresponds to a 2:1 elliptical head, the standard
pressure-vessel form. For a `DISH` primitive, `RADIUS ≈ DIAM` approximates it
(IR-9).

Do not add ladders, platforms or accessories that no drawing shows (IR-10).
Where a user authorises reference access steel, place ladders only on vessels
whose height creates a real access need, vary the bearing to suit the layout,
provide base shoes, and make every stand-off terminate on shell/support steel.
Do not copy the same free-floating ladder onto every tank.

> **User-corrected 2026-07-30 (JK_Cooking_Tank_Build).** The previous detail
> pass put a same-bearing ladder on nearly every vessel and carried the Blow
> Tank ladder into an unsupported reducing section. Low/grade-accessible vessels
> now omit ladders; remaining ladder bearings vary, and Blow Tank ladders stop at
> the supported main-shell top with lower crossbars tied to a support leg.

> **User-corrected 2026-08-10 (JK-Tank_Build top platform handrail).** A top
> handrail on a frustum-roof tank follows the **shell-cylinder top rim (the big
> circle, outer diameter)**, not the frustum top (the small circle, DTOP). Post
> base plates sit fully on the cylinder top face with their outer edge flush
> with the rim; the frustum and its platform may be adjusted by the designer
> afterwards. The cone surface near the rim intersects the post zone for the
> first ~30–40 mm of post height until the frustum is re-sized — report that
> interaction instead of hiding it.
>
> **Mandatory Structural Handrail Rule (2026-08-31, PML-STUDY-HANDRA-001 & JK-Tank_Build R8).**
> Whenever a tank top, roof deck, or access platform requires perimeter handrails by drawing
> or project instruction:
> 1. **Structural Hierarchy Contract**: `HANDRA` is a structural element and **MUST** be
>    created under `NEW STRU /<tag>_STRU` -> `NEW FRMWORK /<tag>_FRMWORK` -> `NEW HANDRA /<tag>_TOP_HANDRAIL`,
>    peer to `EQUIPMENT`. Creating `HANDRA` inside `SUBEQUIPMENT` triggers `(41,8) Cannot create a HANDRA at this level`.
> 2. **Datum Seating Contract**: `STRU` is positioned under `ZONE` (world coordinates). Its
>    emitted `POS` must equal the true world elevation of the cylinder top rim
>    ($U_{world} = U_{local\_rim} + U_{equipment\_origin}$).
> 3. **Ladder Outward Connection Contract (User-corrected 2026-08-31)**: At a vertical access ladder
>    exit, the perimeter handrail must **NOT** break open or bend inward into the sloped roof cone
>    (which causes clashing). The handrail turns **radially OUTWARD** at the rim to connect directly
>    and seamlessly into the two vertical ladder handrail stringers (e.g. at $W 5150\text{ mm}$, $N \pm 240\text{ mm}$).
> 4. **Ladder Top Safety Cage Extension (User-corrected 2026-08-31)**: The vertical ladder safety
>    cage (护笼) must extend upward by $+1100\text{ mm}$ all the way to the top handrail elevation
>    ($U = 27500\text{ mm}$), adding upper safety hoops and extending the 7 vertical cage bars to
>    provide complete $360^\circ$ fall protection behind the worker's back at the landing.

> **User-corrected 2026-08-28 (JK-Tank_Build roof breather vent).** An atmospheric
> tank breather / vent elbow is rooted at the **tank roof apex / geometric center**
> $(E_c, N_c, U_{apex})$, not at an offset perimeter nozzle. It is built as an open
> $90^\circ$ pipe gooseneck using native `CYLINDER` riser + `CTORUS` ($90^\circ$
> smooth elbow, `ANGL 90degree`) + horizontal `CYLINDER` discharge spool. It does
> not use a flanged `NOZZLE` element. A $180^\circ$ hairpin return bend is too
> restrictive and impedes atmospheric vapour relief; a $90^\circ$ horizontal
> discharge allows unobstructed venting while preventing vertical rain ingress.

> **User-corrected 2026-08-28 (JK-Tank_Build shell stiffeners).** When removing
> crude placeholder access ladders (e.g. $\Phi 60\,\text{mm}$ cylinders), always
> **preserve the tank shell circumferential stiffening rings** (wind girders /
> stiffener rings with projection $\approx 120\,\text{mm}$ and depth $\approx 100\sim 200\,\text{mm}$)
> located across the height of the cylindrical shell. Never purge the entire
> access subequipment if it houses the shell stiffener geometry.

---

## Special cases

**Double-shell vessels.** Where the equipment list gives an outer and an inner
diameter ("Outside 9.9, inside 6.47"), model both: the inner shell is the process
boundary, the outer is the insulation or containment envelope that clash
detection must see.

**Droplegs.** A barometric leg holds the vacuum seal for a drum washer and must
exceed roughly 10 m — this is a physical requirement (the height of a water
column the atmosphere can support), not a convention. Model as a tall small-bore
standpipe on legs with an offset conical bottom to a seal pot.

---

## Sanity checks before modelling

- π/4 · D² · H ≈ stated volume? A ~10× discrepancy means **height and diameter
  are transposed** in the source data — a defect confirmed twice in JK-Project.
- Height understood as tangent-to-tangent or overall? See
  [README](README.md#know-which-part-each-parameter-describes).
- Does the support type match the bottom type? A conical bottom on ground
  bearing, with no skirt, is usually an error.
