# Horizontal Process Pumps

Engineering prototype knowledge for detailed AVEVA E3D pump models. All sizes
are Reference Values unless project data or a vendor GA supplies them.

## Data that must never be inferred

- installation coordinate and its datum;
- baseplate length, width and thickness;
- pump/driver longitudinal direction;
- suction and discharge directions;
- nozzle DN, shaft elevation and vendor model when they are project data.

User and project values always win. A visual-detail pass may replace a coarse
shape, but it must not alter any of these underlying parameters.

## Recognisable long-coupled process-pump construction

**RECOMMENDED**, based on official ANDRITZ ACP and KSB Etanorm descriptions:

1. rectangular torsion-resistant baseplate or skid;
2. single-stage radially split volute casing with integral feet;
3. removable casing cover, seal housing and stepped bearing bracket;
4. flexible coupling with a contact guard;
5. foot-mounted, totally enclosed fan-cooled electric motor;
6. suction at the impeller eye and a radial discharge branch.

The external model should therefore show the casing split, cover fasteners,
bearing/seal transition, coupling hubs/guard, motor feet, cooling fins, end
bells, fan grille and terminal box. A single BOX for the entire motor is a
coarse envelope, not a high-detail motor.

### TEFC motor detail that must read as connected construction

**RECOMMENDED.** A motor can contain many primitives and still look false when
its basic proportions or contacts are wrong.

- Select the motor envelope from a documented skid-size/family tier and apply
  lower bounds to motor length, height and length-to-finned-diameter ratio.
  Primitive count is not a substitute for a plausible frame size.
- Cooling ribs run axially and surround the full stator circumference. In the
  proven additive PML1 subset, use small axial `CYLI` elements at equal angular
  intervals. Set their radius so every rib overlaps the stator solid while its
  outer edge remains visible. A few BOX strips on the top surface fail this
  test.
- A round stator's underside changes with transverse offset. Calculate the
  attachment elevation from the circle at the motor-foot web position; using
  only the barrel's centreline bottom leaves off-centre feet floating.
- Separate each foot into a low mounting pad and an inward web that intersects
  the barrel. Place hold-down fasteners through the pad, not at the web top.
- Do not close the fan inlet with one large thin solid `CYLI`. Without verified
  boolean/ring geometry, a bounded horizontal/vertical BOX lattice with a
  central hub reads more truthfully as an open grille.

These details remain Reference Values until a vendor motor schedule or GA is
available. Verification should check geometric contact, angular coverage and
proportion floors, not merely search for labels.

Sources:

- [ANDRITZ single-stage centrifugal pump, ACP series](https://www.andritz.com/products-en/group-de/pumps/end-suction)
- [KSB Etanorm — radially split volute casing pump](https://www.ksb.com/en-se/lc/products/pump/dry-installed-pump/etanorm/E04B)

## Duty-driven differentiation

**RECOMMENDED.** The duty name is evidence for broad external construction, not
for exact performance or internal impeller geometry.

| Duty | Visible emphasis suitable for a Reference-Value model |
|------|--------------------------------------------------------|
| Dilution/process water | full volute, vent/flush boss, conventional bearing bracket |
| Filtrate/washer return | slimmer volute, inspection/vent boss |
| Screen or stock feed | heavier volute ribs, larger clean-out/access cover |
| Booster/high head | compact casing, more pronounced bearing bracket and pressure tapping |
| Wire wash | compact hydraulic end, longer high-speed motor proportion |
| Washer feed | stock-duty casing ribs and clean-out cover |
| Scrubber circulation | robust seal area, seal-flush manifold and splash shield |
| Medium consistency | fluidizer/volute package plus separation, degassing and auxiliary drive |

Do not encode an internal impeller shape without a section drawing. Do not
claim materials from service alone.

Matched pumps with the same duty, size and drawing may legitimately share a
construction family. "Individual model" means every tag is independently
generated and evaluated against its own data; it does not justify arbitrary
differences between genuinely identical duty pairs.

## Medium-consistency pumps

**SUPPORTED BY OFFICIAL VENDOR DESCRIPTION.** ANDRITZ describes its MC series as
a single-stage, single-flow pump with an integrated SMARTSEP separation/
degassing system, a flexible degassing-line arrangement and a volute with four
supporting legs. These are appropriate visible features when an MC pump lacks a
vendor GA, but their dimensions and side arrangement remain Reference Values.

Source:

- [ANDRITZ medium-consistency pumps](https://www.andritz.com/products-en/group/pumps/medium-consistency)
- [ANDRITZ MC-series product sheet](https://grzg.andritz.com/c/com2011/00/01/23/12398/1/1/0/125092449/hy-andritz_medium_consistency_pump_en.pdf)

## Fasteners in additive PML geometry

PML1 has no verified threaded-bolt primitive. Before the native EXTRUSION study,
a useful visual bolt was modeled as:

1. a small `CYLI` shank;
2. a larger, thin solid `CYLI` washer around the filled shank;
3. a short larger `CYLI` cap/hex-head envelope.

The washer is not treated as an unsupported annulus: its centre is filled by the
shank, so the combined solid reads correctly without a floating disc. Thread
pitch and exact hex flats remain UNCONFIRMED. Never add anchor embedment below
the project's foundation datum merely for appearance.

### Native high-detail EXTRUSION baseline — 2026-08-03

**NATIVE-OBSERVED, with hierarchy/local-axis behavior supported by installed
AVEVA E3D 3.1 code.** The `/PMP-10` specimen in `PML-STUDY-EXTR-001` raises the
preferred visible fastener quality above a circular head envelope:

- eight `CYLINDER` shanks are paired with sixteen short hexagonal `EXTRUSION`
  heads, two heads per shank;
- the heads are true ordered LOOP profiles extruded along local Z;
- a separate asymmetric EXTRUSION is used for a genuinely non-standard support
  section;
- the remaining pump uses BOX, CYLINDER, DISH and PYRAMID where those forms
  match the actual feature.

For future high-detail pumps, use a true hex EXTRUSION head when the fastener is
large enough to read and the live project justifies that fidelity. The head,
shank and retained plate/flange must be coaxial and in numerical contact. Use a
CYLINDER head only as an explicitly documented lower-detail envelope. Do not
copy the specimen's 20 mm hex side, 40 mm across-corners, 34.64 mm across-flats
or 20 mm head height: these are source-specific observations, not reference
values for other equipment.

This is also a syntax-weight rule. EXTRUSION is selected for constant custom or
polygonal sections; it must not replace simpler primitives for circular,
rectangular or crowned features. A model exceeds this specimen by improving
proportion, contact, hierarchy and recognisable construction—not by maximizing
EXTRUSION count.

### Bridge-type support brackets — RECOMMENDED (JK_Pump_Build 2026-08-05)

For foot-mounted horizontal pumps, a solid rectangular mounting block under
each pump foot or motor pad can be refined into a bridge-type standard
bracket without changing any bearing surface:

- one sole plate (BOX) at the old pad top height;
- two trapezoid gusset plates (EXTRUSION, 4-vertex profile in the pad
  cross-section plane) at the two ends of the pad's long axis;
- gusset bottom at the old pad bottom (baseplate top or rail top); gusset top
  flush with the sole-plate bottom; sole-plate footprint equal to the old pad.

Keep the pad footprint, bottom face and top bearing height identical so the
support chain (baseplate -> rail -> bracket -> casing/motor foot) is
unchanged. Fastener caps may be upgraded to true hex EXTRUSION nuts with
across-flats equal to the old cap diameter; the EXTRUSION POS for a Z=U nut is
its bottom face, which must seat on the washer or shank top.

### MC auxiliary vessel placement — RECOMMENDED (JK_Pump_Build 2026-08-05)

An MC separator/degassing vessel must have a valid footprint. Before placing
it beside the pump, check it against the casing body, the cover cone and any
flange ring on that side; on a small skid the discharge side may be entirely
occupied while the motor-side corner is free. Verify with an AABB clash search
after any relocation, and keep the vessel's outlet pipe inside the skid or
document the protrusion as a nozzle projection.

### Negative primitives for real holes — EXPERIMENTAL (JK_Pump_Build r2 2026-08-05)

When a small cylinder visually crosses a plate to suggest a gland or conduit
opening, prefer a true hole: nest a `NCYLINDER` inside the plate `BOX` with
the cylinder's own POS/ORI/DIAM/HEIG and delete the stub. The form is backed by
the client's native listings and AVEVA's PMLLIB, but is EXPERIMENTAL on this
project until the user confirms the holes render in E3D. Apply the same idea
to any future "part passes through plate" feature (cable glands, sight
glasses, pipe sleeves, bolt clearance holes) instead of adding a positive
stub.

> **User-corrected 2026-07-29 (JK_Pump_Build).**

The final connection-flange arrangement below was reloaded in E3D and visually
accepted by the client. Earlier placements at the cone root and on a solved
sloped-cone point were rejected as buried and floating, respectively.

Position the three solids as one seated assembly, not as three separated
decorations:

- For a base anchor, the washer bears on the baseplate top and the head bears
  directly on the washer. Shift the shank into the plate so it reaches the head
  top but does not cross below the foundation datum.
- Casing-cover bolts belong to the physical split-flange bearing surface at the
  cylinder/cone connection; placing axial bolt stacks on a separately solved
  point of the sloped cone makes them float without a meaningful clamped joint.
- Put the bolt-circle centreline inside the protruding annular band, preferably
  at the midpoint between the cone-root radius and flange outside radius. Seat
  the washer on the common connection plane, place the head immediately outward
  and extend the shank backward into the flange.

> **User-corrected 2026-07-30 (JK_Pump_Build).**

Do not add a bearing-frame pedestal, oil-fill cap or coupling-guard support foot
merely because it is recognizable pump detail. In the accepted long-coupled
layout, the generated pedestal/cap and the two guard feet were detached from a
credible bearing surface and appeared as floating blocks in E3D. The client
required their removal from all 30 pumps.

This correction generalizes as a contact rule: a support, cap or foot must
numerically touch the part it supports and its bearing surface. If the available
project data cannot establish both contacts, omit the assumed primitive rather
than leave a visually plausible but physically floating detail.

## Verification properties

**Native-template adaptation -- RECOMMENDED, 2026-10-11:** preserve complete
primitive-local axes, including tilted motor-fin BOX frames and Y-first axis
clauses. A generated-model convention that expects Z first is not proof that
a native orientation is invalid. The shared `native_orientation_basis` checks
cardinal/quadrant orthonormal frames; `validate_pml(native_templates=True)`
opts into this check without relaxing nozzle binding or ORI/POS ordering.
Keep negative children and EXTRUSION vertices in their actual parent frames.
Bounds-check every native dimension before reuse: the 2026-09-10 ordinary TEM
carried one DRIVER BOX with `ZLEN -5.25mm`. Its absolute-span repair and native
rail-rounding corrections are documented in the
[ordinary-pair candidate report](../../Projects/JK_Pump_Build/output/2026-10-11_ordinary_pair/REPORT.md),
with native E3D visual acceptance still pending.

- baseplate underside centre and dimensions are numerically unchanged;
- nothing falls below the foundation datum;
- every primitive remains within the allowed equipment footprint unless the
  drawing explicitly documents an overhang;
- motor stays opposite the casing along the confirmed main axis;
- longitudinal interfaces satisfy `motor front < bearing start < casing rear`;
  never hide a negative gap with a minimum coupling-length clamp;
- every motor pad overlaps a longitudinal skid rail in plan, every hold-down
  shank lands inside that rail, and each inner foot web intersects the barrel;
- nozzle directions and flange-face datums are unchanged;
- catalogue DN changes must not silently move a nozzle face, alter its
  orientation or change its projection length;
- every modeled fastener touches the part it retains; casing fasteners bear on
  the cylinder/cone connection-flange plane, never on a detached cone point;
- one independent `EQUI` exists per pump and each native nozzle retains its own
  `SUBE`.

A project may also request one loading macro containing many pumps. Generate it
directly through one builder and retain one independent zero-anchored `EQUI` per
tag. Verify each EQUI block with the same single-pump numerical checks; do not
concatenate previously written files or nest all pumps under one shared EQUI.

> **User-corrected 2026-08-20 (JK_Pump_Build).** When an upward native NOZZLE
> must visibly join a horizontal volute, preserve its catalogue element and
> branch on verified nominal diameter versus casing axial width. If DN is no
> greater than the casing width, add no connector primitive: the native
> NOZZLE itself must penetrate the crown and at least 70% of its HEIG must be
> outside the casing. If DN exceeds the casing width, model the outlet as
> casing-owned basic bodies, not PIPE/BRANCH: a lower CYLINDER socket that
> starts inside and projects visibly above the crown, followed by one
> concentric CONE. The physical native NOZZLE bottom (`face - HEIG`) must equal
> the CONE upper face directly; do not insert another primitive neck. Require
> exact face/diameter closure at the socket/CONE and CONE/NOZZLE interfaces.
> Keep catalogue binding, plan position, flange-face POS and ORI fixed. If
> fixed nozzle and casing plan datums differ, do not silently move either; add
> an explicitly documented equipment-side solid bridge or report the conflict.

## Scaling an accepted native listing to a new baseplate — RECOMMENDED

**(JK_Pump_Build 2026-08-13.)** When a client asks to re-size an accepted
native E3D data listing while keeping the construction and the nozzle sizes:

- Archive the received listing byte-for-byte and check it for duplicated
  exports of the same `EQUI`; a duplicate name collides on load, so keep
  exactly one block.
- Keep the baseplate thickness and underside-centre datum.  Apply **one
  uniform similarity factor** to the superstructure: scale plan coordinates
  about the plate centre and elevations about the plate top plane, so the
  rail -> sole -> pedestal -> machine bearing chain stays seated.  Do not
  stretch the machine anisotropically; `CYLI`/`CONE` cannot follow it.  If the
  requested plate width does not match the same factor, the width is an
  explicit plate override, not a second machine scale.
- Native `NOZZLE` elements keep `CATR`, `HEIG`, `ORI` and process attributes.
  Scale the barrel **root** with the machine, then re-add the unchanged
  `HEIG` along the aim direction.  Scaling the flange face directly leaves the
  barrel floating `(s - 1) * HEIG` clear of the enlarged casing.
- Keep machine-side connection stubs (a discharge boss) at their connection
  size and reposition them on the scaled casing surface, so the boss still
  matches the unchanged nozzle bore.
- A native listing can omit `NAPPFLAG` on a nested negative cylinder even
  though the loaded database carried it; re-emit `NAPPFLAG 2` or the hole will
  not cut after reload.
- Verify numerically: element inventory, per-attribute uniform-scale
  prediction, plate dimensions/datum, bounds above the foundation and inside
  the new plate, support-chain U-span scale invariance, nozzle root
  attachment, and negative-hole rim containment.

## Adapting a native pump-base assembly — user-corrected 2026-08-19

**RECOMMENDED (JK_Pump_Build).** A native base cannot be reconstructed from
member count and world-position ordering alone. Preserve and verify four layers:

1. source member identity and inventory;
2. member-local axes, dimensions, offsets and profiles;
3. the member-to-machine datum (casing centre, motor centre and shaft axis);
4. the original overlap/contact relationship with the machine envelope.

Use independent mappings for the skid, pump station and motor station. The
skid fits the project base envelope; pump support scales from casing diameter
and axial length; motor support scales from stator diameter and length. Do not
map a sole-plate centre to a motor centre unless the native model proves they
are the same datum.

An element without an explicit native ORI still has the default local frame.
When the pump turns in plan, give that element the corresponding explicit ORI;
swapping world-aligned dimensions does not rotate a PYRAMID, its offsets or an
EXTRUSION profile. Fabricated gusset thickness and hex hardware scale from
plate/hardware thickness, while their plan spacing follows the machine. A true
hex profile scales isotropically or it stops being the reference shape.

### Off-origin base hardware and tapered-gusset handedness — user-corrected 2026-08-19

**RECOMMENDED (JK_Pump_Build).** When a native support is rotated into a target
pump direction, transform member positions and local ORIs with the same
right-handed frame. For a machine's longitudinal unit vector `(E, N)`, the
reference-compatible right-hand transverse vector is `(N, -E)`. Using the
opposite transverse vector only for positions mirrors every offset PYRAMID
relative to its ORI and makes inward braces lean outward.

Check the physical result: for any midline brace carrying `XOFF` or `YOFF`,
the top transverse offset must be no greater than the base offset. This is
independent of the transformation formula and therefore can catch a mirrored
implementation.

An EXTRUSION's LOOP may be deliberately off-origin. Its `POS` is the profile
end-plane origin, not necessarily the midpoint of a nut or washer. When plan
spacing is scaled anisotropically but a regular hex profile is scaled
isotropically, map the intended fastener axis first and solve the EXTRUSION POS
from the transformed LOOP geometry. Verify a one-to-one pairing between every
hex midpoint and anchor-cylinder axis after emitted-coordinate rounding.

### Interface-driven support sizing — user-corrected 2026-08-19

**RECOMMENDED (JK_Pump_Build).** Once the client accepts a support's member
combination and plan arrangement, keep that construction stable while adapting
its height to each machine. Do not apply one vertical scale to sole plates,
gussets, pads and fasteners: different shaft elevations turn native clearances
into visible gaps and turn hardware into oversized columns.

Treat each fabricated member as a connection between named bearing surfaces.
A sole plate begins on the skid top and keeps plate-proportioned thickness. A
lower gusset spans from that sole top to its upper bearing. An upper saddle
spans from its mounting pad to its machine-relative top. A fastener head keeps
hardware-proportioned thickness and bears on the retained plate; its shank
ends at the head top and begins at the native-scaled embedment.

Verify continuity with a structural contact graph that excludes bolts, nuts
and washers. Every load-carrying plate, pad and gusset must reach the skid
through structural members alone. Hardware may clamp a continuous assembly;
it must never be counted as the bridge that makes a detached assembly pass.

For a tapered PYRAMID, certify its intended terminal faces rather than its
axis-aligned bounding box. An inner gusset must have its bottom face on the sole
plate and its top face on the mounting-plate underside. An outer stay must have
its bottom face on the fixed sole plate even when its top is positioned from a
machine envelope. Require equal interface U and positive overlap of the actual
end-face rectangles in plan. Crossing or overlapping AABBs are not evidence of
a fabricated bearing or weld.

PYRAMID POS is its geometric centre, not either terminal face. After solving a
required low/high span, emit `HEIG = high - low` and place POS at their midpoint.
Verify occupied local-Z faces at `POS +/- HEIG/2`. Writing the bottom face to
POS drives half a tall stay through the skid and leaves the opposite end short
by the same half-height.

> **User-confirmed 2026-08-20 (JK_Pump_Build).** The client accepted the r6 E3D
> result after the adapter solved physical terminal faces first and emitted the
> midpoint as PYRAMID POS. This acceptance closes the preceding r5 failure in
> which the same intended spans were emitted from a bottom-face POS.

## Data-driven segmented motors and drive shafts — user-corrected 2026-08-20

**RECOMMENDED; not yet client-accepted outside JK_Pump_Build.** A circular
frustum is a centre-datum CONE with both end diameters; replacing it with a DISH
changes both shape and datum. For this project the client requires a similar,
mirrored cone at both ends of every motor. Each cone joins the main stator at
full diameter and tapers to an outward face at 2/3 diameter. When source end
diameters conflict with this construction, the user ratio wins. If only one end
has a measured positive length, use it for both cones.

> **User-corrected 2026-08-20 (JK_Pump_Build).** The prior rule treated every
> `engine_total` as an accessory-inclusive closed envelope. That made
> `205-PU-012` visibly too short by compressing its main stator to 717 mm. Its
> project-specific correction keeps a 1277.8 mm total envelope, absorbs the
> rear-small-cylinder allowance into a 1126.8 mm main barrel and terminates
> both ends with 75.5 mm cones.
> Do not generalise this one tag's number to another motor.

> **User-corrected 2026-08-20 (JK_Pump_Build).** The motor/outboard tail must
> physically terminate in the rear CONE. A small cylinder outside that cone is
> not acceptable even when the model contains two correct cones elsewhere.
> Preserve the required envelope by absorbing that axial allowance into the
> main stator, and verify the outboard-most body type after sorting by axis.

For a measured free drive comprising cylinders and a pump-side frustum,
preserve its topology, diameters and axial part ratios. Raw offsets can be less
reliable than the required physical interfaces. If they leave a gap or excessive
penetration, uniformly fit only the axial part lengths between the motor face
and a controlled casing engagement, and disclose the factor. An explicit N/A
free-shaft record should select a close-coupled construction rather than a
Reference-Value shaft.

If a project tag has no motor/shaft row, a family-derived fallback must be
deterministic and traceable. Select donors on machine/skid envelope similarity,
reject donors that would require extreme compression, scale axial and radial
dimensions independently from documented target evidence, and label every
result as a Reference Value until vendor data or client review supersedes it.

---

## Top-discharge volute casing / pump head bend transition — user-confirmed 2026-09-03

**VERIFIED / USER-CONFIRMED.** On centrifugal process pumps with top-centerline
discharge nozzles, the casing volute wraps circumferentially and transitions
into the central vertical discharge spool via an intermediate reverse bend:

1. **Main volute ring**: Modeled additively as a full $360^\circ$ ring in the
   transverse plane (normal axis $Z$ parallel to the pump shaft) using two
   back-to-back $180^\circ$ `CTORUS` primitives.
2. **Transition auxiliary bend (`CTORUS`)**: Directly connects to the approach
   quadrant of the volute ring (e.g. West quadrant for clockwise rotation) with
   tangent continuity ($G^1$). When the transition bend radius equals the volute
   radius ($R_2 = R_1$), the sweep is exactly $60^\circ$ (`ANGL 60degree`),
   shifting the horizontal offset from $E_{\text{center}} - R_1/2$ smoothly into
   $E_{\text{center}}$ with a strictly vertical ($+U$) tangent.
3. **Discharge nozzle / straight spool (`CYLINDER` / `NOZZLE`)**: Aligned
   coaxially on the equipment center vertical axis ($E_{\text{center}}, N_{\text{casing}}$)
   and seated directly on the transition bend exit elevation ($U_0 + \sqrt{3} R_1$).

```pml
-- Volute main ring lower half
NEW CTORUS
ORI Z IS N AND Y IS D
POS E 48852mm N 5610.9mm U 622.17mm
RINS 159.5mm
ROUT 262.5mm
ANGL 180degree
END

-- Volute main ring upper half
NEW CTORUS
ORI Z IS N AND Y IS U
POS E 48852mm N 5610.9mm U 622.17mm
RINS 159.5mm
ROUT 262.5mm
ANGL 180degree
END

-- West-to-up transition auxiliary bend (60deg S-bend into top centerline)
NEW CTORUS
ORI Z IS N AND Y IS D
POS E 48641mm N 5610.9mm U 987.63mm
RINS 159.5mm
ROUT 262.5mm
ANGL 60degree
END

-- Top vertical discharge straight spool
NEW CYLINDER
ORI Z IS U AND Y IS N
POS E 48852mm N 5610.9mm U 1137.63mm
DIAM 103mm
HEIG 300mm
END
```

---

## Horizontal liquid ring vacuum pump packages — user-confirmed 2026-10-10

**VERIFIED / USER-CONFIRMED.** Liquid ring vacuum pump units (e.g., Brown Stock
Drum Displacer vacuum pumps, tag pattern `*-PU-*` or `*-VP-*`) are skid-mounted,
horizontal rotating packages consisting of a horizontal driver (TEFC motor),
bearing bracket, liquid ring pump casing, and side-mounted seal-water circulation
auxiliaries:

### Drawing interpretation: Plan view vs. Elevation view

On plant layout CAD drawings (floor arrangement / piping plan views):
1. **Plan view appearance**: A rectangular perimeter with an internal cylinder
   and crosshaired concentric circles is almost always a **Plan View (top-down)**
   of a horizontal package, NOT an elevation view of a vertical pump.
2. **Concentric circles with crosshairs**: Indicate top vertical nozzle
   flanges/necks pointing upwards (`ORI P1 IS U`), viewed along their centerline.
3. **Shaft centerline**: Lies horizontal (typically along the long axis of the
   skid, e.g. North-South `ORI Z IS N AND Y IS U`), with centerline elevation
   derived from base skid height plus pump shaft centerline height (typically
   $U \approx 300\text{--}400\text{ mm}$ above foundation).

### Layout components and hierarchy

1. **Base Skid (`SUBE /..._SKID`)**: Structural perimeter channel frame sitting
   directly on the foundation floor ($U = 0\text{ mm}$).
2. **Motor (`SUBE /..._MOTOR`)**: TEFC motor barrel, axial cooling fins, end
   bells, terminal box, and fan cowl facing rearwards.
3. **Bearing & Coupling Bracket (`SUBE /..._BRACKET`)**: Intermediate pedestal
   and protective coupling guard connecting motor and pump shaft.
4. **Vacuum Pump Casing (`SUBE /..._CASING`)**: Horizontal cylindrical chamber
   with end covers, shaft seal housings, and suction/discharge manifolds.
5. **Auxiliary Unit (`SUBE /..._AUX`)**: Side-mounted seal-water circulation pump
   or separator pot on the skid extension.
6. **Nozzles (`NOZZLE`)**:
   - Main suction (N1): DN150 top vertical (`ORI P1 IS U`).
   - Auxiliary discharge (N2): DN50 horizontal or vertical tie-in.
   - Aux separator/pump connection (N3): DN100 top vertical (`ORI P1 IS U`).
   - Always ensure nozzle names are distinct from sub-equipment names (e.g.,
     use suffix `_NOZZ` to avoid E3D `(41,12) Name already used` errors).


