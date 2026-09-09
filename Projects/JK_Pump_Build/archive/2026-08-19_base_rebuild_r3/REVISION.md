# JK_Pump_Build base rebuild r3

**State:** Candidate generated and locally verified; pending a fresh E3D visual
reload. It is not the accepted baseline.

## User verdict that opened this revision

The client loaded r2 in E3D and reported two visible defects:

- all support PYRAMIDs leaned in the opposite direction;
- hex screw heads and screw shafts did not share one axis.

The verbatim screenshot was preserved unchanged as
`2026-08-19_r2_e3d_rejection.png`.

## Preserved evidence and baselines

| Item | SHA-256 |
|------|---------|
| `imports/2026-08-19_Base_reference.txt` | `D8C17257E318162FC4BBDC901C82EA2C2811E7E3775DA860C5F7A770EC9101AF` |
| r2 rejected candidate | `3C5C6D38578D54165EB2A8E4CDBA3710AD1DE25B6D499D74C78B498FB735AC59` |
| r2 E3D rejection screenshot | `1B520B64C429FFECA4B74155EAA2FF0205C315DB88B2AFF0F339F8C35B6F740A` |
| r3 combined candidate | `73EA855719FAF0D892780CF3C37B568F8EAC44C22366ACEBC95A6BCEC9F60C33` |
| r3 audit | `C229BC63EDD826660302C8882455B177166ED9691510CD8871F26E2AF1F33A2E` |
| r3 orthographic QA image | `184FF0FA42A285094649DADB35F30D5BBF5AEDEA3C35A5599E1141FA66EB6CFE` |

## Root causes and authorized delta

1. `ReferenceAdapter.across` used the opposite transverse sign from
   `rotate_ori()`. Member placement was mirrored while local ORIs were not, so
   every offset PYRAMID leaned outward.
2. The native hex LOOP is off-origin. Its physical midpoint is approximately
   `(-17.32, +10)` in local coordinates. Mapping raw EXTRUSION POS with machine
   scale while scaling the regular hex isotropically separated its physical
   midpoint from the anchor CYLINDER.

r3 changes only `/P1501B-BASE`-derived geometry. It restores a right-handed
plan frame, pairs the ten reference hex profiles one-to-one with the ten anchor
cylinders, maps each physical hardware axis, and solves the emitted EXTRUSION
POS from the scaled LOOP geometry.

Every non-base SUBE block was compared between r2 and r3:

```text
old non-base blocks: 168
new non-base blocks: 168
missing: 0, extra: 0, changed: 0
NON_BASE_BLOCKS=UNCHANGED
```

## Verification

- 30 pumps, 2616 elements.
- 0 numeric geometry problems.
- 0 reference-fidelity problems.
- 0 emitted-text or emitted-hardware-axis problems.
- 12 offset PYRAMIDs per pump taper toward the machine axis.
- 10/10 hex-head/anchor-shaft pairs per pump are coaxial after macro rounding
  (300 pairs total, tolerance 0.05 mm).
- 972 cooling ribs checked, 0 wrong.
- 26/26 injected defects caught, including the two client-reported failures.
- 9 focused base-adapter regressions pass.
- Full repository: 506 passed, 4 skipped.

## Output

`output/2026-08-19_pumps_r3/JK_Pump_Build_2026-08-19_base_rebuild_r3_all_pumps.pml`

Load into a fresh writable ZONE with `$M <absolute-path>`. E3D visual acceptance
is required before this candidate can replace the current accepted baseline.
