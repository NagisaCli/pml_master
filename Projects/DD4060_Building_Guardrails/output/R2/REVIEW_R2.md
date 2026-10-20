# DD4060 Guardrails R2: Exterior Platform Correction

The marked bay is an exterior/derived platform. R2 encloses its three exposed
sides and removes the R1 rail across its connection to the building. All R1
segments outside this bay retain their exact geometry. The source building,
access structure, stairs, joints, plates and catalogue references are unchanged.

The user's marked image is archived unchanged in
`../../imports/2026-10-19_external_platform_marked.png`.

## Choose one load path

If the original R1 is already loaded and has not been manually edited, run this
patch **once**:

```pml
$M C:\Users\A\Desktop\building_F2_guardrails_R1_TO_R2.txt
```

It targets only `/DD4060_BUILDING_F2_GUARDRAILS_R1/PERIMETER`, navigates its
existing RPATH, repositions the original 37 points and appends two points. It
does not delete anything or change other handrail attributes. It requires the
exact original R1 hierarchy; repeated application is not supported. PML1
navigation has been statically inspected and its point updates simulated, but
the patch has not been executed in E3D.

If R1 has not been loaded, select the same writable ZONE as the building and use
the complete corrected macro instead:

```pml
$M C:\Users\A\Desktop\building_F2_guardrails_R2.txt
```

Do not load both. Neither macro saves work. The complete R2 uses its own
`/DD4060_BUILDING_F2_GUARDRAILS_R2` structure name; the patch keeps the R1 names.

## Geometry and provenance

- Source outboard beam: building-local E 11999.94..12600.02,
  N 1999.98..8800 mm, top U 9700 mm in the exported owner frame.
- The beam is approximately 6800 mm long. Its outer edge is 1500 mm beyond the
  main building's E 11100 mm slab edge.
- New exterior rail: E 12450.02 mm, from N 2150 to N 8750 mm, with returns to the
  retained building-side railing at both ends. There is no rail across the
  platform's inner opening.
- Heights remain 1100/550 mm; maximum post spacing remains 1200 mm.
- The complete perimeter has 39 route points including closure and an
  unfilleted path length of 70463.78 mm.

The received export contains the outboard beam but no separate platform slab in
this bay. The planar walking envelope used for routing is derived from that beam,
the main building edge and the user's platform identification. No new slab,
support or structural feature has been invented in the model. Matching this
beam to the marked screenshot remains an inference to review in E3D.

## Reference Values and local clearance

Outer-edge and south-end insets are 150 mm. The north return uses a 50 mm end
inset to pass outside `/DD4060-ACCESS-R6/P-EL2-N`; retaining the R1 150 mm inset
there would intersect the conservative section envelope. The 50 mm corner
radius, 125 mm section-axis envelope and 40 mm rail envelope are Reference
Values. The north return has 17 mm clearance between these assumed envelopes;
this is tighter than the original 100 mm layout allowance and is **not** a
verified native-solid clearance.

Actual catalogue section/tube sizes, corner posts, flush embedded plate
interfaces and end anchorage must be reviewed on the receiving host. Flush
embedded plates are below/at the floor plane; they are not treated as obstructions
to elevated horizontal rail tubes. Their post/base interfaces remain unchecked.

## Verification

The revision script verifies the immutable source hash, uniquely identifies the
outboard beam, parses the emitted full macro back, checks route closure and
self-intersection, samples 50 mm corner fillets, checks the rail envelope inside
the derived walking region, checks that the inner access stays open, compares
all geometry outside the correction window, retains both floor-stair entries,
and simulates the exact R1 point updates and two appended points. All pass.

Source SHA-256:
`c87af66310ac7b74281ad7339f17256ee4b79985c1bbd52a8448b761fe436dc0`.

The PML1 static validator passes for both outputs. Native loading, patch
navigation, actual-solid clashes, visual acceptance, Save Work and reopen
persistence remain pending. No live E3D model was changed during this revision.

`python -m pytest tests/test_handra_study.py tests/test_skill_integrity.py -q`:
85 passed.

Reproduce from the repository root:

```text
python Projects/DD4060_Building_Guardrails/tools/revise_external_platform_r2.py
```

The plan in `external_platform_R2.png` shows the cancelled inner R1 rail dashed
and the corrected outer route in blue. `layout_audit_R2.json` records coordinates
and numerical checks. R1 output remains preserved for traceability.
