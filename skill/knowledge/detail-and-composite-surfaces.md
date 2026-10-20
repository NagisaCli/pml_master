# Detail and Composite Surfaces

**Status: RECOMMENDED construction practice.** User-directed 2026-09-28 after
the 204-SE-009 cleaner transition revision. The user explicitly praised the
triangular EXTRUSION approach and requested its reuse in this skill. This
feedback supports the modeling approach; it does not certify every orientation,
catalogue binding, saved database state or future implementation.

## Select shapes deliberately

Pursue the details that make the equipment credible: reference silhouettes,
continuous connections, open bores, wall thickness, flange seating, supported
attachments and usable interfaces. Loading successfully alone does not settle
these questions. Review the overall outline and close views of the joints.

Use CYLI for cylindrical forms, CONE for circular tapers, DISH for appropriate
heads, BOX for rectangular members, PYRAMID for rectangular tapers, CTORUS for
circular bends and EXTRUSION for custom profiles. Combine suitable forms for
geometry that changes section and direction. Consult the
[spatial lookup](pml-spatial-lookup.md) for each element's actual contract.
Prefer a simple analytic form where it matches the shape; use a faceted assembly
where it materially improves fidelity.

The project's governing view controls conflicting geometry. Another machine's
reference may explain construction details without supplying the target's
outline. Do not transfer dimensions, tessellation settings or catalogue paths
from one equipment item into another as defaults.

## Triangular EXTRUSION panels for a curved transition

A thin triangular extrusion is a small solid prism, not a native smooth surface.
An assembly of these prisms can approximate a hollow curved transition between
unlike sections without blocking a circular flange with a rectangular solid.

1. Establish the inlet/outlet boundary curves, tangents, shell intersection and
   governing envelope from the references. Parameterize section progression,
   thickness and resolution; label unspecified values as Reference Value / TBC.
2. Sample successive sections with consistent point order. Split each strip
   between them into triangles. Reject zero-area triangles and inconsistent
   winding before attempting to normalize their normals.
3. For triangle A, B, C in one owner frame, define local X along B-A, local Z
   along the consistently oriented cross product of B-A and C-A, and local Y
   as Z cross X. Project the vertices onto local XY to obtain the LOOP profile.
4. Use EXTRUSION's **profile end-plane datum**. If A lies on the desired outer
   surface and Z is its outward unit normal, a prism of thickness t starts at
   A-tZ and extends t along local +Z. Do not apply a centred-solid conversion.
   Emit the frame with supported PML direction syntax and numerically verify
   the resulting pose against the intended triangle.
5. Inspect neighbouring prism joints. Thin prisms with different normals can
   leave wedge gaps even when their outer triangle edges coincide. If a small
   overlap is used, make it explicit and verify the actual solid coverage,
   inner bore and external envelope. Overlap is not proof of a watertight shell.
6. Join the assembly to the nozzle barrel and equipment wall with controlled
   contact or penetration. Check the passage through the wall separately;
   a hollow transition outside an uncut wall still blocks the bore. Use only
   supported negative geometry with verified ownership when openings need it.
7. Keep real connection points as native NOZZLE elements. Follow the
   [catalogue contract](catalogue-elements.md), and verify the flange face,
   connection direction and barrel root independently of the transition skin.

## Resolution and acceptance

Choose subdivision from visible faceting, curvature and geometric error at the
required inspection scale. Refine tighter bends and section changes first.
Keep related panels under a meaningful assembly and retain parameters so later
editing does not require manipulating hundreds of separate faces. More elements
alone do not establish better detail.

Numerically check reconstructed coordinates, normals, section clearance,
attachment continuity and the governing envelope. Then inspect the native E3D
result from the source views and at each junction. A faceted shell does not
establish exact constant wall thickness, manufacturability or hydraulic quality.
Report offline checks, native load/readback, visual review and save/reopen
persistence as separate evidence.

## Case provenance and reuse boundary

The motivating case is `204-SE-009_R2` in
`C:/Users/A/Documents/Codex/2026-09-28/gao`:
`work/build_r2.py` builds a hollow round-to-oval curved inlet from triangular
EXTRUSION panels; `outputs/204-SE-009_R2/` holds the generated macros and checks.
User feedback in the 2026-09-28 conversation endorses the technique and the
ongoing pursuit of detail. These local artifacts are examples, not dependencies
of this skill. Reuse the construction reasoning, and establish dimensions,
catalogue choices and native acceptance afresh for each target project.
