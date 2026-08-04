# PMP-10 Native Construction Analysis

## Model reading

The supplied model is a long-coupled, base-mounted horizontal pump package. Its
visual quality comes from recognizable assemblies, stable proportions and
physical contact—not from raw primitive count.

- `/PMP-10-HEAD` carries the hydraulic casing and two native catalogue-bound
  nozzles.
- `/PMP-10-BASE` carries the skid/support construction and every EXTRUSION.
- `/M-PMP10-B` carries the motor body, fins/cover construction and two
  electrical connections.
- One outer BOX is used as an equipment-level volume/detail element.

## Element distribution

| Owner | Important contents | Interpretation |
|---|---|---|
| `/PMP-10-HEAD` | 4 CYLINDER, 1 DISH, 2 NOZZLE | Casing, branches and connection interfaces |
| `/PMP-10-BASE` | 13 BOX, 8 CYLINDER, 10 PYRAMID, 17 EXTRUSION | Skid, feet/gussets, support profiles and bolted details |
| `/M-PMP10-B` | 37 BOX, 5 CYLINDER, 2 DISH, 2 ELCONN | Motor barrel, ribs/end forms, feet and electrical interfaces |

## EXTRUSION decomposition

### Custom support profile

The first EXTRUSION begins at native listing line 114. It has `HEIG 440mm`,
`ORI Y IS S AND Z IS W` and an asymmetric eight-vertex LOOP. In signed local XY
coordinates its explicit points are:

`(-10,0), (-10,170), (-93,170), (-93,0), (-103,0), (-103,190), (0,190), (0,0)`

The profile bounds are X = -103..0 mm and Y = 0..190 mm; signed area is
-5460 mm2. The non-rectangular notch makes EXTRUSION materially more faithful
than stacking unrelated BOX elements.

### Hexagonal fastener heads

The other 16 EXTRUSION elements repeat mirrored forms of one regular hexagonal
profile. A canonical point order is:

`(0,0), (0,20), (-17.32,30), (-34.64,20), (-34.64,0), (-17.32,-10), (0,0)`

Each has `HEIG 20mm`. Eight 15 mm diameter CYLINDER elements act as shanks and
two hexagonal extrusions surround each shank at opposing ends. This is the
important screw-scale lesson: the head is not a circular visual proxy; it is a
true polygonal solid, and its value comes from its relation to the shank and
the retained part.

The sample's 20/40/34.64 mm values are evidence about this object only. A future
project must derive fastener size from its own reference data.

## Spatial grammar learned

1. A LOOP is a local 2D construction plane.
2. Ordered VERTEX positions trace its boundary.
3. EXTRUSION HEIG creates the third dimension along local Z.
4. EXTRUSION ORI maps that local section and axis into equipment space.
5. EXTRUSION POS is element-specific and remains unresolved until the isolated
   axes/datum candidate is measured in E3D.

Therefore a valid future workflow is profile first, local frame second, datum
third, then numerical world-extents/contact verification. String matching a
POS line is insufficient.

## Quality baseline promoted from the specimen

- Choose syntax by physical form: true custom sections use EXTRUSION; axial
  round solids use CYLINDER; rectilinear plates/rails use BOX; crowned ends use
  DISH; tapered rectangular supports may use a verified tapered element.
- Build recognizable subassemblies under meaningful SUBE owners rather than a
  flat field of decorative solids.
- Every foot must transfer load into a skid or plate. Every fastener shank/head
  set must be coaxial and touch the clamped construction.
- Preserve suction/discharge flange-face positions, shaft centreline, coupling
  alignment, skid datum and motor-pump ordering before adding fine detail.
- Use repeated detail only when repetition expresses manufacture: bolt groups,
  cooling fins, paired feet and flange patterns.
- Reject floating blocks, detached nozzles, fake dashed-line connection cues and
  visually dense component dumps without a route or load-path logic.
- Future pump models should meet or exceed this level through better physical
  relationships and measured proportions—not merely by producing more elements.

## Deliberate non-promotions

- The final native `OLD ... ORRF ...` and NOZZLE `CATR` blocks are template and
  catalogue rebinding context; they are not EXTRUSION syntax and do not replace
  the established nozzle workflow.
- No universal pump dimension, bolt size, flange class or support spacing is
  inferred from `/PMP-10`.
- No production model may convert EXTRUSION POS to a centre/bottom datum until
  the live E3D result resolves its longitudinal meaning.

