# PML Spatial Construction Lookup

This is the fast path from **modeling intent** to the PML form currently safe to
use. It complements [pml1-reference.md](pml1-reference.md), which carries syntax
examples and evidence details, and [iron-rules.md](iron-rules.md), which carries
failure-paid constraints.

Status vocabulary:

- **VERIFIED** — demonstrated in E3D or traced to authoritative AVEVA code;
- **RECOMMENDED** — project construction practice, not a language fact;
- **EXPERIMENTAL** — requires a controlled E3D trial;
- **NATIVE-OBSERVED** — present in an authentic export but not yet semantically
  certified.

The map is deliberately complete only for what the project can currently
justify. Unknown syntax remains visible as a gap rather than being guessed.

---

## 1. Choose the database level

| Modeling intent | Element/command | Ownership pattern | Current rule | Status |
|---|---|---|---|---|
| One selectable equipment item | `NEW EQUI /<tag>` | Under a writable `ZONE` | One `EQUI` per equipment item; anchor it explicitly at zero | VERIFIED / RECOMMENDED |
| Selectable equipment subassembly | `NEW SUBE /<name>` | Under its `EQUI` | Separate support, shell, each nozzle, access and internals | VERIFIED / RECOMMENDED |
| Native piping connection | `NEW NOZZLE /<name>` | Normally isolated in its own `SUBE` | Catalogue-bind inline before pose; its position is the flange face | VERIFIED |
| Piping network owner | `NEW PIPE /<name>` | Under a piping `ZONE` | Administrative owner for one or more BRANCH elements | NATIVE-OBSERVED / OFFICIAL-SUPPORTED |
| Routed pipe section | `NEW BRANCH /<name>` | Under its `PIPE` | Head/tail and owned catalogue components define the centreline | NATIVE-OBSERVED / OFFICIAL-SUPPORTED |
| Plant/site/zone creation | `NEW SITE`, `NEW ZONE` observed | Above `PIPE`/`EQUI` | Native data-listing form is under current certification | NATIVE-OBSERVED |
| Structural hierarchy (`FRMWORK`, etc.) | `HANDRA 1 of FRMWORK /<name>` | Under structural `ZONE` | Structural framework parent for beams, columns, and handrails | NATIVE-OBSERVED |
| Multi-Discipline Support | `NEW SUPPORT /<name>` | Under `ZONE` with `PURP SUPP` | Individual pipe support or cable tray bracket owning `STRUCTURE`/`FRMWORK` and `SUBSTRUCTURE` | NATIVE-OBSERVED |
| Structural handrail | `NEW HANDRA` + `NEW RPATH` | Under `FRMWORK` / `STRU` | Dual rails (`RAILHE`), posts (`POSTSP`), route points (`POINTR`), curves (`CURVE`) | VERIFIED — E3D Design Mk3.1 |


---

## 2. Choose the geometric element

| Desired physical form | Safe PML element | Required size attributes | Best current use | Do not use it for | Status |
|---|---|---|---|---|---|
| Solid cylinder or short solid disc | `CYLI` | `DIAM`, `HEIG` | Shell course, skirt, shaft, roll, neck | A hollow ring by itself | VERIFIED |
| Circular frustum/cone | `CONE` | `DTOP`, `DBOT`, `HEIG` | Conical roof/bottom, reducer-like body, hopper | A rectangular taper | VERIFIED |
| Dished circular closure | `DISH` | `DIAM`, `HEIG`, `RADIUS` | Vessel head with a real crown | Flat plate or arbitrary dome | VERIFIED |
| Rectangular solid | `BOX` | `XLEN`, `YLEN`, `ZLEN` | Base, frame member, motor block, plate | Curved/ring geometry by itself | VERIFIED |
| Rectangular pyramid/frustum | `PYRAMID` | `XBOT`, `YBOT`, `XTOP`, `YTOP`, `HEIG`; optional `XOFF`, `YOFF` | Tapered support plate or gusset | Writing bottom-face U directly to centre-datum POS | VERIFIED — native export + user E3D result 2026-08-19 |
| Native flanged connection | `NOZZLE` | Catalogue binding plus `HEIG` and process attributes | Piping connection with P-points | Generic decorative neck | VERIFIED |
| Routed Up-to-West pipe direction change (tested `/A3B/EA100`) | `ELBOW` | `SPRE`, `LSTU`, `ARRI 2`, `LEAV 1`, native pose | BRANCH-owned elbow | Omitting component-specific arrive/leave | VERIFIED — E3D Design Mk3.1.11.0 |
| Vertical 100-to-80 transition (tested `/A3B/RC100X80`) | `REDUCER` | `SPRE`, `LSTU`, `ORI Y IS N AND Z IS E` | BRANCH-owned vertical reducer | Applying primitive Z-axis reasoning | VERIFIED — E3D Design Mk3.1.11.0 |
| Routed branch outlet | `TEE` / `OLET` | Catalogue `SPRE`, pose and reciprocal connection | BRANCH split/connection | Unconnected visual-only fitting | NATIVE-OBSERVED |
| Inline pipe function | `VALVE`, `FILTER`, `INSTRUMENT`, etc. | Catalogue `SPRE` and pose | BRANCH-owned inline component | Guessing catalogue component paths | NATIVE-OBSERVED |
| Hollow ring | Array of small `BOX`/`CYLI` segments | Segment dimensions and bearings | Only when justified and attachment is verified | One axial `CYLI`, which becomes a solid disc | RECOMMENDED |
| Sloped or irregular body | Additive slices of verified primitives | Per-slice dimensions | Approximation with explicit resolution | Invented negative/Boolean forms | RECOMMENDED |
| Extruded custom section | `EXTRUSION` + owned `LOOP` / ordered `VERTEX` | `HEIG`; LOOP local-XY profile | Non-standard constant section, true polygonal head | Guessing the longitudinal POS datum or using it for every solid | VERIFIED — hierarchy, axis and end-plane POS datum |
| Curved transition with changing section | Assembly of thin triangular `EXTRUSION` panels | Ordered triangle profiles, local frames, thickness and subdivision | [Hollow transition fitting](detail-and-composite-surfaces.md) with explicit approximation and joint checks | Treating a faceted assembly as an exact smooth or automatically watertight surface | RECOMMENDED — user-endorsed approach 2026-09-28; validate each implementation |
| Detailed fastener / screw | Head by head form: `EXTRUSION` for hex, `DISH` for dome/button, `BOX` for square; shank and thread root `CYLI`; transitions `CONE` | Per-element size attributes | Real fastener detail where the drawing or study justifies it | One familiar primitive for every head form | VERIFIED — user-accepted PML-STUDY-SCREW-001/01 (2026-08-05); each element form individually VERIFIED |
| Circular torus / pipe bend | `CTORUS` | `RINS`, `ROUT`, `ANGL` | Gooseneck breather elbow, smooth pipe bend | Multi-cylinder stacked step bends | VERIFIED — E3D Design Mk3.1.11.0 |
| Structural / platform handrail | `HANDRA` + `RPATH` | `RAILHE`, `POSTSP`, `TANGOF`, `BRAD`; path `POINTR` / `CURVE` | Platform, tank-top, and walkway railing | Synthetic RAILSET with no POINTR | VERIFIED — user-certified 2026-08-31 in E3D Design Mk3.1 (PML-STUDY-HANDRA-001) |
| Catalogue structural member | `SCTN` | `POSS`, `POSE`, `DRNS`, `DRNE`, `JUSL`, `SPRE` | Structural beam, column or brace under `FRMWORK` | Guessing specification paths | NATIVE-OBSERVED |


---

## 3. Position and orientation contract

| Element family | Caller supplies | Meaning of emitted `POS` | Aim/orientation form | Required order | Status |
|---|---|---|---|---|---|
| `CYLI` | Bottom-face centre | Geometric centre after half-height conversion | `ORI Z IS <axis> AND Y IS <roll>` | Size → `ORI` → `POS` | VERIFIED |
| `CONE` | Bottom-face centre | Geometric centre after half-height conversion | `ORI Z IS <axis> AND Y IS <roll>` | Size → `ORI` → `POS` | VERIFIED |
| `DISH` | Flat rim/tangent-plane datum point | Passed through unchanged | `ORI Z IS <axis> AND Y IS <roll>` | Size → `ORI` → `POS` | VERIFIED |
| Axis-aligned `BOX` | Geometric centre | Passed through unchanged | None required | Size → `POS` | VERIFIED |
| Rotated `BOX` | Geometric centre plus plan bearing | Passed through unchanged | `ORI Z IS U AND X IS <bearing>` | Size → `ORI` → `POS` | VERIFIED |
| `PYRAMID` | Required bottom/top faces and local rectangles | **Geometric centre** — local faces are at `POS +/- HEIG/2` | `ORI Z IS <axis>` plus a local roll axis | Size/offsets → `ORI` → midpoint `POS` | VERIFIED — user E3D result 2026-08-19 |
| `CTORUS` | Centre of curvature | Centre of the circular torus arc | `ORI Z IS <normal-axis> AND Y IS <tangent-axis>` | Radii → `ORI` → `POS` → `ANGL` | VERIFIED — E3D Design Mk3.1.11.0 |
| `NOZZLE` | Flange-face point | Position in owning equipment frame | `ORI P1 IS <direction>` | `CATR` → `POS` → `ORI` → attributes | VERIFIED |
| `EXTRUSION` | Profile end-plane position plus ordered local-XY profile | **Profile end plane** — the LOOP plane sits at POS, the solid extends `HEIG` toward +Z (user E3D result 2026-08-04) | `ORI Y IS <axis> AND Z IS <extrusion-axis>` | `POS` → `ORI` → `HEIG` (native form); `ORI` → `POS` places identically (candidate `/03`) | VERIFIED |
| `HANDRA` | Origin insertion point and route path vertices | Base origin of the handrail system | `DRNS` / `DRNE` for route path tangents | `POS` → `RAILHE`/`POSTSP` → `RPATH` | VERIFIED — E3D Design Mk3.1 |

Do not infer a datum from the spelling of a `POS` line. Verify occupied geometry
or a meaningful P-point in E3D.

---

## 4. Axis choice from spatial intent

| Spatial intent | Primary orientation | Typical application | Status |
|---|---|---|---|
| Vertical body | `Z` points Up | Tank shell, vessel skirt, vertical shaft | VERIFIED |
| Cross-machine horizontal body | `Z` points North/South | Paper-machine and dryer rolls | VERIFIED |
| Machine-direction horizontal body | `Z` points East/West | Horizontal shaft or barrel | VERIFIED |
| Radial rectangular hardware | local `X` radial, local `Y` tangential, local `Z` Up | Anchor plate, clamp, chair, gusset | VERIFIED |
| Catalogue connection direction | `P1` points along connection direction | Native `NOZZLE` | VERIFIED |
| Arbitrary compound 3D rotation | Not generalized yet | Skew piping/structural items | EXPERIMENTAL |

For non-cardinal bearings, retain the object's physical local dimensions and
rotate its frame. Do not enlarge world-axis dimensions to imitate a rotation.

---

## 5. Common assemblies

| Equipment feature | Preferred construction | Placement invariant | Status |
|---|---|---|---|
| Vertical cylindrical vessel | support + `CYLI` shell + `CONE`/`DISH` closure | Lowest support point equals equipment bottom-centre elevation | RECOMMENDED; primitives VERIFIED |
| Horizontal pump envelope | `CYLI` shafts/casings + `BOX` base/motor + justified tapers | Shaft centreline and suction/discharge axes drive the composition | RECOMMENDED |
| Platform/base frame | Rotated or axis-aligned `BOX` members | Member local axes follow the frame, not world axes by accident | RECOMMENDED |
| Vessel nozzle | One `SUBE` + native `NOZZLE` | Flange face, bore direction and wall penetration are checked separately | VERIFIED / RECOMMENDED |
| Atmospheric tank breather/vent | Vertical `CYLI` riser + $90^\circ$ `CTORUS` bend + horizontal `CYLI` spool | Rooted at tank roof apex/geometric center; no flanged nozzle | VERIFIED / RECOMMENDED |
| Top-discharge pump volute & casing bend | $360^\circ$ `CTORUS` ring + reverse-bend `CTORUS` ($60^\circ$) + vertical `CYLI`/`NOZZLE` | $G^1$ tangent transition from volute quadrant into equipment center vertical axis | VERIFIED — user-confirmed 2026-09-03 |
| Ring/stiffener | Segmented additive geometry only when detail is justified | Every segment attaches to shell or to an attachment chain | RECOMMENDED |
| Threaded fastener detail | Head primitive chosen by head form; CYLINDER shank/root; additive thin CYLINDER thread ridges; CONE fillet and tip | Every part touches its neighbour; ridges stay inside the root range; lowest point at the bearing plane | VERIFIED — user-accepted 2026-08-05; element forms individually VERIFIED |
| Tank roof / platform handrail | Native structural `NEW HANDRA` + `NEW RPATH` under `NEW STRU` / `NEW FRMWORK` (`wsb.handrail_builder`) | Follows platform perimeter or tank shell top rim with dual rail heights (`RAILHE`), posts (`POSTSP`), `CURTYP THRU`, and outward connection to ladder handrail stringers | VERIFIED — E3D Design Mk3.1 (PML-STUDY-HANDRA-001 & JK-Tank_Build R8) |

Equipment-specific decisions—what belongs on a digester, pump, paper machine or
tank—live in [the equipment index](../equipment/README.md). This table selects a
syntax form after that engineering decision has been made.

---

## 6. Attribute meaning quick table

| Attribute | Applies to | Current interpretation | Status |
|---|---|---|---|
| `DIAM` | `CYLI`, `DISH` | Outside diameter of the solid/body form | VERIFIED |
| `HEIG` | `CYLI`, `CONE`, `DISH`, `PYRAMID`, `NOZZLE` | Element-specific axial extent; PYRAMID spans half on each side of POS; for `NOZZLE`, its own projection length | VERIFIED |
| `XLEN`, `YLEN`, `ZLEN` | `BOX` | Dimensions along the BOX local axes | VERIFIED |
| `DTOP`, `DBOT` | `CONE` | Diameters at the local positive-Z and negative-Z ends | VERIFIED |
| `RADIUS` | `DISH` | Crown radius controlling curvature | VERIFIED |
| `HEIG` | `EXTRUSION` | Distance extruded along the element's local Z axis | VERIFIED |
| `POS` | Many elements | Element- and owner-specific position; consult section 3 | VERIFIED |
| `ORI` | Oriented elements | Establishes the local frame or aims a P-point | VERIFIED |
| `CATR SPCOMPONENT` | `NOZZLE` | Binds the live catalogue component that supplies geometry/P-points | VERIFIED |
| `TEMP`, `PRES`, `TPRESS`, `DUTY` | `NOZZLE` | Process/design attributes carried by the native element | VERIFIED syntax; project values vary |
| `RAILHE`, `POSTSP`, `TANGOF`, `SHOWKP`, `BRAD` | `HANDRA` | Top/mid rail heights, post spacing, tangent offset, kickplate display, bend radius | VERIFIED — E3D Design Mk3.1 |
| `DRNS`, `DRNE` | `RPATH` | Tangent direction bearings at start and end of path | VERIFIED — E3D Design Mk3.1 |
| `FRAD`, `CURTYP` | `POINTR`, `CURVE` | Fillet radius on route points; curve interpolation mode (`CURTYP THRU`) | VERIFIED — E3D Design Mk3.1 |

---

## 7. Selection algorithm

When choosing syntax for a feature:

1. Decide the engineering feature and whether it is justified by project data.
2. Choose the selectable hierarchy level.
3. Choose the simplest verified element whose real solid matches the feature.
4. Define the physical datum and local axes before calculating coordinates.
5. Apply the element's order contract from section 3.
6. Verify extents, attachments, bounds and P-points numerically.
7. If no verified element fits, stop production use and start
   [a native-export syntax study](../workflows/learning-from-native-exports.md).

---

## 8. Capability gaps to target next

These are learning targets, not supported promises:

| Priority | Native specimen requested | Question to settle |
|---|---|---|
| 1 | EXTRUSION study `PML-STUDY-EXTR-001` received | **CLOSED 2026-08-04** — datum (01), order (03) and two-head fastener contact contract (04) all user-certified in E3D; production generation may use EXTRUSION with end-plane POS |
| 2 | A native `SCTN` beam/column | Catalogue binding, start/end geometry, orientation and owner hierarchy |
| 3 | A native structural framework with connections | `FRMW` hierarchy and member/connection ownership |
| 4 | PIPE/BRANCH study `PML-STUDY-PIPE-001` received | Core rounds 1–2 VERIFIED in E3D Design Mk3.1.11.0; remaining advanced forms still open |
| 5 | An arbitrarily rotated primitive/assembly | Stable representation of compound 3D orientation |
| 6 | A native negative/Boolean example, if E3D exports one | Whether the operation survives macro export/import and remains editable |

Every new row is promoted through the learning workflow; it is never filled from
memory or analogy alone.
