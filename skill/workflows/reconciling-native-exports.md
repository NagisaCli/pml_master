# Workflow: Reconciling Manually Edited Native E3D Exports

Use this workflow whenever the user supplies a PML file exported from E3D after
manual editing. The user normally preserves hierarchy and names, but may change
attributes or add elements at an existing level. Those edits are intentional
project data and must survive later agent work.

If the export was supplied only to teach a new syntax/model form, use
[learning-from-native-exports.md](learning-from-native-exports.md) instead. If it
is both a continuation and a teaching specimen, preserve and reconcile it here
before studying a separate evidence copy.

---

## Authority and non-negotiable rule

The user's current instruction remains the highest authority. For geometry,
the newest user-supplied native export is the **working baseline**. The previous
accepted/generated file is retained only as the **comparison baseline**.

Never regenerate wholesale over a native export before reconciliation. A clean
generator run can silently remove a designer's new child element, restore an old
`POS` or `ORI`, replace a catalogue reference, or reintroduce a previously
corrected visual defect.

## Phase 0 — Identify the project first

Before preserving or comparing anything, identify which project the export
belongs to using that project's `FINGERPRINT.md` (file patterns, zone/site
names, tag conventions, coordinate anchors). Then read its `TIMELINE.md` for
the current accepted baseline. The user's versions frequently contain manual
edits, so the fingerprint match is the guard that keeps those edits in the
right project's memory.

---

## Phase 1 — Preserve both sides

1. Copy the received file unchanged to
   `Projects/<name>/imports/<received-date>_<original-name>.pml`.
2. Keep the last user-accepted macro under version control. Do not overwrite it.
3. Record SHA-256 hashes for both files in the project log or revision record.
4. Identify the requested change separately from differences already present in
   the native export.

The original import is evidence. All editing happens in a working copy.

---

## Phase 2 — Compare semantics before text

Run the hierarchy/attribute comparator:

```bash
python -m wsb.pml_compare \
  Projects/<name>/archive/<accepted>.pml \
  Projects/<name>/imports/<native-export>.pml
```

Use `--format json` when another script will consume the result.

The comparator ignores comments, blank lines, whitespace and equivalent numeric
formatting. It aligns stable named elements and reports:

- added or removed `EQUI`, `SUBE`, `NOZZLE` and primitive elements;
- changes to dimensions, `POS`, `ORI`, `CATR`, `HEIG` and other attributes;
- attribute-order changes that may affect E3D evaluation;
- unnamed primitive changes within their owning hierarchy.

Then use a normal textual diff around each reported element to retain nearby
comments and export-specific syntax. A semantic diff tells you **what changed**;
the focused text diff shows **exactly how the native file expresses it**.

---

## Phase 3 — Build the preservation set

Classify every difference before editing:

| Difference | Default treatment |
|---|---|
| User-added named child or primitive | Preserve |
| Changed geometry/property attribute | Preserve |
| Changed catalogue reference or nozzle data | Preserve |
| Changed hierarchy ownership | Preserve and verify the resulting coordinates |
| Comments/formatting only | May normalise only when necessary |
| Difference explicitly superseded by the new request | Change, and record why |
| Clearly invalid export artefact | Report; do not silently delete |

Create a short preservation set listing element paths and attributes that are
outside the current request. This list becomes a regression contract for the
revision.

Do not infer that an unfamiliar addition is accidental. If the name and purpose
are unclear, preserve it while continuing with the requested, independent edit.

---

## Phase 4 — Apply the smallest patch

Prefer editing the native-export working copy directly when the requested change
is local. If the shared generator must also learn the change:

1. update the generator/data model;
2. regenerate to a separate candidate file;
3. replay or merge every preservation-set delta onto the candidate;
4. never use the regenerated file as the final result until the preservation
   comparison passes.

Changes are matched by hierarchy and element name first. For unnamed primitives,
use owner, type, neighbouring elements and key attributes together; ordinal
position alone is insufficient when a new primitive was inserted.

### Equipment Duplication and Transformation in Zone Macros

When replicating a template equipment model to other equipment items with different orientations:
- **Unique Subequipment Naming**: Subequipment names starting with `/` (e.g. `/Copy-of-MOTOR_FRAME`) are globally scoped in E3D MDBs. Prepend the target equipment tag (`/<TAG>_MOTOR_FRAME`) to prevent `(2, 102) Name already exists` errors.
- **Coordinate Frame Separation**: Subequipments with world `POS` use local relative $(dx, dy, dz)$ vectors for child primitives, which must be rotated as local vectors. Subequipments without world `POS` use world $(E, N, U)$ coordinates, which transform relative to the target anchor.
- **Unoriented Primitives**: Primitives without an explicit `ORI` default to world E-N-U axes. When rotating equipment, inject the rotated default `ORI` (e.g. `ORI Y is W and Z is U` for 90° CCW; `ORI Y is E and Z is U` for 90° CW) so that $XLEN$ and $YLEN$ keep their physical dimensions.
- **Nozzle Catalogue Bindings**: Ensure trailing `OLD NOZZLE` / `CATR` bindings in the epilogue are duplicated and updated for all newly added or replaced equipment.

---

## Phase 5 — Prove nothing was overwritten

Before delivery:

- compare native baseline → candidate and confirm every preservation-set item
  remains;
- compare candidate against the requested scope and list every intentional
  change;
- verify element counts and named hierarchy;
- run `validate_pml()` and numerical geometry checks;
- inspect `ORI`/`POS` order, catalogue binding and datum-sensitive elements;
- confirm no previously accepted project correction regressed.

The final report distinguishes:

1. **manual edits preserved**;
2. **new requested changes applied**;
3. **unexpected differences requiring review**.

---

## Phase 6 — Archive the continuation

Store the accepted result and comparison report in the project, update
`DO.txt`, and append the revision to `skill/projects/<project>.md`. The next
continuation compares against this newly accepted result, not against the
original generator output.

This workflow is a process safeguard, not evidence that a native export is
correct. E3D visual acceptance and the Iron Rules still apply.
