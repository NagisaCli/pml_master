# JK_Pump_Build symmetric motor-cone r8

Status: **candidate; fresh E3D load and client visual acceptance required**.

## Trigger

The r7 E3D review found `205-PU-012` too short and the two motor end frustums
dissimilar. The verbatim feedback is preserved at
`results/evidence/2026-08-20_r7_motor_visual_feedback.txt`.

## Scoped correction

- Every DRIVER has exactly two same-length mirrored CONEs.
- Each cone joins the main stator at full diameter and tapers toward an outward
  face at 2/3 main-stator diameter. The user ratio overrides conflicting CSV
  end diameters.
- A positive side length supplies both cones when the opposite side is zero or
  N/A. A rear small cylinder uses the same 2/3 diameter.
- `205-PU-012`: main barrel 717.0 → 997.4 mm; resolved motor envelope
  997.4 → 1277.8 mm; end cones 75.5 mm each; outward diameter 639.7 mm against
  the 959.6 mm main stator. DRIVE_SHAFT is axially refitted to the new front
  face and BASE adapts to the longer motor.
- r7→r8 canonical changes are restricted to DRIVER on all tags plus
  DRIVE_SHAFT and BASE on `205-PU-012`.

## Verification target

- 30 pumps, 2751 elements.
- Numeric geometry, base reference, emitted PML text and rib orientation: zero
  problems.
- 35/35 injected mutations caught, including a widened outward cone face.
- Eight focused motor/drive tests, including the exact `205-PU-012` dimensions.

## Final candidate hashes

- Combined r8 macro SHA-256:
  `4C8DCD026F3F8DAE7FAB4C5B6CE7AB4B74D041F705BAB7D9458050A8B6E663B5`
- Audit SHA-256:
  `E486A0472FD56E155CEBEB29778BD2906A4DFC40A9B7E2CA4CB995670E94B351`
- Side-elevation QA SHA-256:
  `817CC169CB72FD8EB9E73412EA0AFE9944C1571B4176D35D77044769D3CABD39`
- Verbatim feedback SHA-256:
  `8D2BF8B3AC1C10F04046F85905B8BF6CD6C36EA2BB75973EC71BB8BA0CD94C49`
