# JK_Pump_Build cone-terminated motor r9

Status: **candidate; fresh E3D load and client visual acceptance required**.

## Trigger

r8 contained two symmetric motor cones, but 27 non-MC motors still placed a
rear-small CYLINDER outside the rear cone. The client requires the physical
motor tail itself to be a frustum. Verbatim feedback:
`results/evidence/2026-08-20_r8_motor_tail_feedback.txt`.

## Scoped correction

- Removed the terminal rear-small CYLINDER from 27 DRIVER groups.
- Absorbed its axial allowance into the main stator, preserving all r8 motor
  envelopes, centres and front faces.
- All 30 outboard terminal motor bodies are now rear CONEs. The forward ends
  remain mirrored CONEs; outward diameters remain 2/3 of main-stator diameter.
- `205-PU-012` remains 1277.8 mm overall: 1126.8 mm main stator plus two
  75.5 mm terminal cones. DRIVE_SHAFT and BASE are unchanged from r8.
- Canonical r8→r9 delta is restricted to DRIVER only.

## Verification target

- 30 pumps, 2724 elements.
- Numeric geometry, base reference, emitted PML text and rib orientation: zero
  problems.
- 36/36 mutations, including a rear terminal changed from CONE to CYLINDER.
- Eight focused motor/drive tests require CONE at both axial extrema.

## Final candidate hashes (SHA-256)

- Macro: `85E239B96DC3B3AE10770E245C2A284A3CF2B55CFA4211CFA093D8455DF7E26C`
- Audit: `1743F357EE6EBE7B389D730CEA760C7AB3A20F617948EFC25F2750E91EC21E8E`
- QA image: `B04B01F260BDDC451CD041AB93276B12D8965D5FCE4CE4BA24351C3774F1FDDD`
- Verbatim feedback evidence: `9A79360F41F7DC5A3FC47BAF49176BC151D93A56452B800C76B3F260B317CD37`
