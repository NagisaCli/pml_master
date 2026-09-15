# Typical Pipe Support R3 reconstruction

Status: generated, numerically checked and deployed as a separate macro; E3D
visual review pending. The user confirmed the supplied screenshot is unedited R2.
The main beam's native section attributes are unchanged.

## What the screenshot shows

The connection does not yet read as a finished welded assembly. The upper
gusset looks like a hanging rectangular tab; the lower connection has a visually
awkward angle toe/plate intersection; welds read as short isolated marks; the
mounting fasteners show crescent-like outlines rather than clear six-sided heads.
The image alone cannot distinguish a hidden surface from an actual penetration,
or prove why the fastener faces are missing. Those are observations and hypotheses,
not a catalogue-aware clash verdict.

Evidence: [unedited R2 screenshot](../results/evidence/R2_unedited_user_review.png),
SHA-256 `ca21f3eddbfad56866c6127ac1897336b86a92e217068e039f7c23fa9ad925c9`.

## Applied reconstruction

| Feature | R3 change and purpose |
|---|---|
| Main structure | Retains native STRU / FRMW / SCTN, existing channel geometry and both profile references |
| Angle cut ends | Moves the start from N=16 to N=80, giving 64 mm clearance from the mounting-plate face; end changes from N=1055 to N=1080. Both remain on the original brace centreline |
| Lower node | Extends the lap to N=200 and tapers/clips the free edge around the angle envelope; the cut end is covered by the plate in side projection |
| Upper node | Uses an inclined lower outline matching the brace direction, instead of a square hanging tab; the cut end is covered by the plate in side projection |
| Lap welds | Lower longitudinal runs increase to about 77.8 mm, upper runs to about 93.3 mm; fillet roots are checked against the actual emitted plate outlines |
| Root haunch | Retains the below-flange triangular haunch and weld relief; no solid filler inside the channel |
| Mounting plates | Retain original outside envelopes and fastener centres, add 6 mm corner clips and real 22 mm clearance holes |
| Washers | Replace 24-sector approximations with one cylinder plus a coaxial negative bore per washer |
| Hex heads | Re-emit full six-vertex heads with precise coordinates, native-style clockwise loops and explicit display levels |
| Ownership | Explicit END closures and zero-origin subassemblies prevent one part's pose/hole from being applied to another |

There are 2 catalogue sections, 36 positive auxiliary solids, 12 negative bores,
6 hex heads, 6 single-solid washers and 13 weld runs. No R1/R2 database element
is modified or deleted. The R3 macro does not save work.

## Reference Values and limitations

All newly selected values remain modelling Reference Values, not a fabrication
release. They are based on fitting the visible assembly and retaining the source
section and mounting envelopes:

- Source beam and angle profiles: `/BS-PFC150x75x18` and `/BS-L50x50x6`.
- New brace endpoints: `(0,80,-452.444658)` and `(0,1080,-178.142445)` mm.
- Gussets: 8 mm thick; lower outline N=16..200, U=-530..-398;
  upper outline N=920..1140, U=-281..-150. Both use the proposed E=0..8 lap face.
- Plate clips: 6 mm; plate clearance bores: 22 mm.
- Screw shank: diameter 20 mm; head: AF30 x 12 mm; washer: OD40/ID22 x 3 mm.
- Fillets: main/root 6 mm legs, angle lap 5 mm legs. No strength calculation.
- Anchor mechanism, embedment, thread form, materials and load capacity are TBC.

The crescent-head root cause is **not proven**. R3 changes winding, washer
construction, display levels and explicit ownership as a corrective candidate.
It does not promote clockwise winding as a universal E3D requirement. AVEVA's
[extrusion and loop editor documentation](https://help.aveva.com/AVEVA_Everything3D/1.1/EUG/EUG4.05.3.html)
describes reversing loop direction; it does not establish the cause of this
particular screenshot. Positive head faces still require E3D review.

The angle profile's exact rolled shape and lap face are not retrieved live.
Numerical side-projection coverage does not establish transverse surface contact.
The continuous welds and changed node shapes must be inspected against the
actual catalogue solid in E3D.

## Verification

- PML checks reject unsupported framework ORI and banned commands.
- A complete ownership walk checks SITE/ZONE/STRU/FRMW/SCTN and
  EQUI/SUBE/positive/negative/LOOP/VERTEX relationships.
- All model selections refer to elements already created in the file.
- Numerical readback checks regular hex heads, seating planes, positive sizes,
  wall clearance, mounting envelopes, local bore positions and depths, and lap
  weld/cut-end coverage by the emitted node polygons.
- Geometry and deployment are re-read from the files; local and deployed bytes
  match. Hashes are in `Typical_Pipe_Support_R3_checks.json`.
- 92 relevant tests passed during generation. The shared parser was corrected
  to retain a positive EXTRUSION while skipping its negative children; previously
  it lost the two drilled plate bodies, which the nonzero/count checks caught.

The [review projection](Typical_Pipe_Support_R3_review.png) is generated from
emitted geometry with nominal steel envelopes. It is not an E3D screenshot.

## Load and inspect

Select a writable SITE, then run once:

```pml
$M C:\e3d_models\SINGLE_TYPICAL_PIPE_SUPPORT_R3.pml
ADD /ZONE_TYPICAL_SUPPORT_R3
/ZONE_TYPICAL_SUPPORT_R3
AUTO CE
```

Inspect with R2 hidden so overlapping copies do not obscure the result. Check:

1. All six head faces are solid hexagons, with single round washers seated flush.
2. Both brace ends stop inside their gusset lap region; no plate crosses the
   angle flange or web and no welding volume floats beside the steel.
3. Plate/washer bores are coaxial with their screws; the 22 mm holes cut through.
4. Main beam, root haunch and gusset welds form continuous physical contacts.

Do not save until your visual review is accepted. If a head still shows a crescent,
capture `Q ATT` for its EXTRUSION and owning SUBE plus a face-on view; do not
enlarge the head to hide the unexplained geometry issue.
