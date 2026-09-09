# JK_Pump_Build motor/drive rebuild r7

Status: **candidate; fresh E3D load and client visual acceptance required**.

## Baseline and scope

- Accepted baseline: `output/2026-08-19_pumps_r6/JK_Pump_Build_2026-08-19_base_rebuild_r6_all_pumps.pml`
- Baseline SHA-256: `0F9D1FBB4CEF9597C36433F4EB193FBB3E60EAD074F59FBA09BEADBDB84F6E68`
- Measurement source: `imports/2026-08-19_engine_shaft_measurements_updated.csv`
- Source SHA-256: `C3E8B5CD96CB0E76BBEDAAE15F87202BD110696B8FCBF4834B1B639FE29C141E`
- Authorised direct-data scope: DRIVER, BEARING, COUPLING and DRIVE_SHAFT.
- Three tags absent from the CSV (`203-PU-020`, `203-PU-026`, `205-PU-004`)
  are completed from declared Reference-Value donor families; their whole
  machine/support relationship is allowed to adapt.

## Construction change

- Removed every DRIVER DISH.
- Motor sequence is rear CONE, optional small CYLINDER, main stator CYLINDER,
  and optional front CONE, closing exactly inside `engine_total_L_mm`.
- Every non-MC free drive is exactly CYLINDER/CYLINDER/CONE. Source diameters
  and part ratios are preserved; the three axial lengths are uniformly fitted
  to close the motor and casing interfaces.
- MC shaft data is N/A, so no free DRIVE_SHAFT is invented; a close-coupled
  lantern closes the physical gap.
- Missing-row donors: `203-PU-020` → `203-PU-031`; `203-PU-026` →
  `205-PU-024`; `205-PU-004` → `204-PU-006`.

## Verification

- 30 pumps, 2747 elements, numeric geometry verification: 0 problems.
- Emitted macro text: 0 problems.
- 1080 cooling ribs: 0 orientation problems.
- 34/34 injected mutations caught, including forbidden DRIVER DISH and an
  open internal drive-shaft interface.
- r6→r7 canonical comparison: non-target geometry unchanged for all 27 tags
  with direct CSV rows.
- Focused motor/drive regression tests: 7 passed.
- Side-elevation QA: `output/2026-08-20_motor_drive_r7/motor_drive_side_elevation_QA.png`.

## Final candidate hashes

- Combined r7 macro SHA-256:
  `E08D3314A3A4ACCE0AD28AB51CA28EB260DCFAE74280A8A554CF7A24645A8D6C`
- Audit SHA-256:
  `E9417A497E7DEF92C1B8B2E6CF601AD240FC5E2DB077424660EA84518B219781`
- Side-elevation QA SHA-256:
  `C1996410E5D4DAD4BA808C943E1F13DFA2B3B5C00AEA9E1F0C75ABD67CEAFDE4`
