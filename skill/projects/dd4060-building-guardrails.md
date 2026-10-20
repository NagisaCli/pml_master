# DD4060 Building Second-Floor Guardrails

Project folder: `Projects/DD4060_Building_Guardrails/`.

## Current correction: R2

User-corrected 2026-10-19: the marked bay is a derived/exterior platform. Its
three exposed outer sides require railing; the inner side connecting it to the
building must stay open. The original R1 slab-only routing was wrong for this
bay. Other R1 segments are retained. See `output/R2/REVIEW_R2.md` and the
unaltered marked screenshot in `imports/`.

The unique outboard beam lies at building-local E 11999.94..12600.02,
N 1999.98..8800 mm. R2 uses its edges to define an exterior platform routing
envelope. The native export contains that beam but no separate deck slab there;
no structural/deck geometry was added. This identification is inferred from the
received model and the user-marked exterior-platform correction; live review
remains pending.

R2 supplies a complete fresh macro plus a deletion-free patch for the original
37-point R1: reposition its route points and append two points. Native PML1
navigation in that patch remains unexecuted. Do not load the fresh R2 alongside
R1, and do not apply the patch twice. Only this project's own railing is targeted.

The north return has a Reference Value 50 mm beam-end inset to clear P-EL2-N.
The conservative above-floor section/rail envelopes give 17 mm local clearance,
less than R1's nominal 100 mm allowance; this is not a verified native-solid
clearance. Post bases, embedded plate interfaces and end anchorage require live
review. All other R1 segments match numerically outside the correction window.

R2 has 39 route points including closure, approximately 70.46 m in total, and
keeps 1100/550 mm rails with 1200 mm post spacing. Offline route, floor-envelope,
stair-entry, source preservation and patch-simulation checks pass. Native
loading, visual acceptance, Save Work and reopen checks remain pending.

## Scope and source

The user requested guardrails around the building second-floor edge, bypassing
the maintenance-platform supports. The native source is archived unchanged as
`imports/2026-10-19_building.txt`; its SHA-256 is
`c87af66310ac7b74281ad7339f17256ee4b79985c1bbd52a8448b761fe436dc0`.

The export contains `/New_washer_biulding` and `/DD4060-ACCESS-R6`. No earlier
accepted building baseline was present in this repository. The source is the
working baseline, including its existing catalogue references, joints, stairs,
plates and all unnamed geometry. Earlier DD4060 revisions from other folders
do not supply dimensions for this continuation.

## Modeling decisions

- Derive the L-shaped floor from its native EXTRUSION/LOOP, including omitted
  zero vertex positions. Its top is U 9700 mm in the exported owner frame.
- Compose the access structure's 180-degree rotation with its own origin before
  comparing support locations with building coordinates.
- Add a separate STRU/FRMWORK/HANDRA hierarchy. Load it in the same owner ZONE
  as the building; do not assume that exported owner coordinates are world ones.
- Copy rail heights 1100/550 mm and post spacing 1200 mm from source HANDRA.
- Build continuous inward bays around columns, support feet, plates and braces.
  Group connected exclusions and short edge returns, without joining isolated
  interior stair feet to corner columns.
- Distinguish horizontal DTOP embed plates at floor top from anchor bars running
  down from the underside. Below-floor anchors do not require railing detours.

## Verification and open acceptance

The reproducible builder parses the emitted hierarchy back, checks closed/simple
route geometry, all 64 above-floor/flush obstacle envelopes, slab containment,
source-byte preservation and both floor-level stair entry points. The PML1
validator passes. The original R1 route is approximately 67.46 m with 37 route points
including closure. These are offline checks only.

Reference Values: 150 mm edge inset, 125 mm section-axis envelope radius,
40 mm rail envelope radius, 100 mm clearance, 50 mm fillet allowance, and
300 mm minimum gap for merging adjacent edge bays. Catalogue surfaces and
post/baseplate shapes must be checked in the receiving E3D host.

Native loading, visual acceptance, actual catalogue clash checking, anchorage
design, Save Work and reopen persistence remain pending. No new syntax claim
was promoted to VERIFIED; the existing HANDRA builder was reused.
