# JK_Pump_Build base rebuild r2

**State:** Candidate generated and locally verified; pending a fresh E3D visual
reload. It is not the accepted baseline.

## User verdict that opened this revision

The preceding 2026-08-19 base rebuild was rejected after visual loading: the
base did not fully reproduce the reference pump base and did not adapt to the
corresponding pump. The screenshot showed shallow, disjoint-looking pump and
motor supports on a duplicated full plate.

## Preserved evidence and baselines

| Item | SHA-256 |
|------|---------|
| `imports/2026-08-19_Base_reference.txt` | `D8C17257E318162FC4BBDC901C82EA2C2811E7E3775DA860C5F7A770EC9101AF` |
| rejected combined candidate | `5386598EAC8FF9C702E13FA0BCFEF8D48FB95D325F2D5D9C7C8309B9DCBDA44C` |
| r2 combined candidate | `3C5C6D38578D54165EB2A8E4CDBA3710AD1DE25B6D499D74C78B498FB735AC59` |
| r2 orthographic QA image | `D5CC0633B90563B24760F01CBCB5F77E248C1AF3A0DC124B8CBA7F526A34D838` |

The desktop `C:\Users\A\Desktop\Base_reference.txt` and the preserved project
copy had the same SHA-256 at intake.

## Authorized delta

Only the base/support construction changed. `check_non_base_unchanged.py`
compared every non-base SUBE block between the rejected macro and r2:

```text
old non-base blocks: 168
new non-base blocks: 168
missing: 0, extra: 0, changed: 0
NON_BASE_BLOCKS=UNCHANGED
```

The former standalone full `BASEPLATE` BOX was removed because the native
43-member base already contains its five-member skid, including the centre
plate. The five members' combined envelope now carries the project baseplate
size and datum.

## Reconstruction contract

- All reference elements 1..43 remain one-to-one by kind and station.
- Skid, pump support and motor support use independent plan frames.
- The motor group is based on the native motor centre N -880, not sole-plate
  centre N -804.62.
- Default-oriented members receive a rotated ORI on S/E/W pumps.
- PYRAMID dimensions and offsets scale in their local axes.
- Hex LOOP profiles remain regular and scale isotropically.
- Pump saddle penetration is 60/170 of target casing radius.
- Motor-stay penetration is 55/180 of target stator radius.
- Plate and hardware thickness scale from the 50 mm project base thickness.

## Verification

- 30 pumps, 2616 elements.
- 0 numeric geometry problems.
- 0 reference-fidelity problems.
- 0 emitted-text problems.
- 972 cooling ribs checked, 0 wrong.
- 24/24 injected defects caught.
- 6 focused adapter regressions pass.
- Full repository: 503 passed, 4 skipped.

## Output

`output/2026-08-19_pumps_r2/JK_Pump_Build_2026-08-19_base_rebuild_r2_all_pumps.pml`

Load into a fresh writable ZONE with `$M <absolute-path>`. E3D visual acceptance
is required before this candidate can replace the current accepted baseline.
