# Square to Round DN600

Status: EXPERIMENTAL native candidate; offline geometry checks passed.
Native E3D load/readback, visual acceptance and save/reopen remain pending.

Project: [Square_to_Round_DN600](../../Projects/Square_to_Round_DN600/DO.txt).
The [report](../../Projects/Square_to_Round_DN600/output/Square_to_Round_DN600_report.md)
records source dimensions, assumptions and verification. No dimensions or
catalogue references from JK pumps/tanks are used.

The supplied plan defines a square flange, a 720 mm opening and twelve holes.
The user confirmed DN600 and overall height 500 mm. Thicknesses, pipe series
and axial allocation remain Reference Values. There is one EQUI and three
top-to-bottom SUBE groups: flange, transition, outlet.

Recommended construction reasoning: a square-to-round radial-line transition
can combine four planar side triangles with four conical corner fans. Thin
triangular EXTRUSION prisms preserve the open passage where a solid PYRAMID
would block it. This candidate uses the existing
[composite-surface guidance](../knowledge/detail-and-composite-surfaces.md).
Its numerical pose reconstruction is not evidence of native syntax acceptance.

The initial offline section audit found only about 3 mm radial wall coverage
immediately above the lower joint when the stub stopped exactly at the start
of the inclined skin. Extending the stub 4 mm into the taper restored at least
5.9 mm coverage on the sampled sections. This is a project-specific numerical
finding, not a VERIFIED native-host or fabrication rule.

The final audit parses the delivered file and checks 30,240 horizontal rays
over 21 sections, including both joints. Seven mutations retain the element
count while introducing physical faults; all must be rejected. Point sampling
cannot establish exact solid watertightness or pressure integrity.

No new syntax claim was promoted to VERIFIED. The round stub deliberately has
no invented catalogue binding; native piping connectivity remains unassigned.
