# pumpcad — JSON-driven pump reconstruction

Rebuilds each pump from the CAD linework exported alongside its
`Pump_details.xlsx` row, instead of from a generic pump template.

```bash
python -m pumpcad.batch --source "C:\Users\A\Desktop\pumps" --out <dir>
```

Outputs, per run:

- `JK_Pump_Build_All_Pumps.pml` — **all 30 pumps in one macro**, 30 `EQUI`
- `pumps/<tag>.pml` — one E3D macro per pump, one `EQUI` each
- `audit/<tag>.txt` — the audit record (evidence, components, transform, validation)
- `pumpcad_batch_report.md` — batch summary

The combined file is the per-pump macros concatenated in tag order under a
single header — same content, no renaming or merging of elements. It is
validated in its own right (syntax plus unique `EQUI` names); any defect
introduced by concatenation is written to
`JK_Pump_Build_All_Pumps_PROBLEMS.txt` rather than passing silently.

## Pipeline

```
JSON -> source.py    RawCadEntity, PumpRecord (metadata + CAD, no repair)
     -> contours.py  dedupe, chain, close, recover circles, find the outline
     -> features.py  the drawn topology: disc stacks, rail cylinders, profiles
     -> assembly.py  features -> named components along the machine axis
     -> semantic.py  view type, then components with confidence + reason
     -> transform.py CAD -> pump-local -> world (the only frame changes)
     -> build.py     3-D solids and PML
     -> audit.py     numeric validation and the audit record
```

## Topology recovery

Contour detection recovers *shapes*; `features.py` recovers what they mean
together. Three structures carry most of the topology:

| Structure | Physical meaning |
| --- | --- |
| concentric circles | one stepped feature — volute + flange + hub |
| parallel line pair | a cylinder seen from the side — shaft, column |
| shared span along the axis | one component — motor body + fins + terminal box |

The dimensioned outline and any full-height side profile are excluded
first: both span the drawing, and either one merges every band into a
single blob.

This matters quantitatively. Classifying raw contours consumed 40% of the
linework (8–11% on plan views) and gave 2–3 boxes per pump — an envelope,
not a machine. Recovering topology first gives **57–91% coverage** and
**9–13 solids**, reported per pump in the audit.

## The three coordinate spaces

| Space | Origin | Used for |
| --- | --- | --- |
| CAD | the drawing's own frame | interpreting evidence |
| LOCAL | baseplate underside centre | pump-relative geometry |
| WORLD | plant E/N/U | the emitted PML |

`transform.py` is the only module that converts between them. Angles are
counter-clockwise degrees from +E; `ori_clause()` is the only place an E3D
`ORI` string is built.

## What the data actually is

Two findings drive the design, both established by measurement:

**Every primitive is a `Line`.** The exporter tessellates all curves, so
circles are *recovered* by fitting, never read. There are no `Arc`,
`CIRCLE` or `LWPOLYLINE` entities in any file, and `unsupported`/`warnings`
are empty throughout.

**Every geometry-bearing drawing is a top view of a horizontal pump.**
The JSON's own `reference_top_view` field says so for all 28 files that
carry linework, and the client re-confirmed it on 2026-08-13: the plan
view is the strict modelling reference.  A North/South pump's plan
outline is legitimately taller than it is wide, so an aspect-ratio
"elevation" heuristic is forbidden here - it was exactly that heuristic
which misread 24 pumps as vertical machines in the first pass.

The view comes from the declared field (`classify_view`).  The geometric
fallback exists only for files whose declared field is absent, and in
that case a drawing with unexplained geometry below its outline is
reported as UNKNOWN rather than silently rotated into the ground.

## Source authority

Priority is enforced, and a lower-priority source never silently overrides
a higher one — substitutions are recorded in the audit.

| Quantity | Authority |
| --- | --- |
| plan/body geometry | CAD JSON |
| world position, orientation | `Pump_details.xlsx` |
| baseplate size | metadata, always the plan L x W pair |
| nozzle size | metadata, snapped to the nearest catalogue DN |

Metadata bores are measured values (173, 539 mm …), not catalogue sizes, so
they are snapped to a real SPCO and the substitution is reported.

## Inherited from JK_Pump_Build

Naming (`safe_tag`), the `EQUI`/`SUBE` hierarchy, the baseplate datum
convention, `layout_axis` = suction direction, ORI-before-POS ordering, the
nozzle catalogue tables and `validate_pml` all come from the existing
project so output drops into the same workflow.

## Known limits

- Component confidence is `HIGH`/`MEDIUM`/`LOW`; only `HIGH` items should be
  treated as measured. Every component states its reason in the audit.
- Z geometry on plan views is engineering inference, bounded so the XY
  footprint always stays as drawn.
- `203-PU-020` and `205-PU-004` have no CAD evidence and fall back to
  metadata-only geometry; both are flagged `CHECK` in the batch report.
