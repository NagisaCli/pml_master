# JK_Pump_Build base rebuild r4 — 2026-08-19

## Client correction captured

The client accepted r3's structural combination and arrangement, but the E3D
view showed that pumps with different dimensions and shaft elevations retained
unadapted support gaps. Sole plates floated above the skid, gusset layers were
separated, and hardware height followed the support rise.

The preserved screenshot is
`2026-08-19_r3_e3d_support_gap.png`, SHA-256
`4629A5A98178E2DDB671D75E0B0BD2EFF1678148A2C5D9C3EBA81C5315AA18AE`.
Its bytes are identical to the user-supplied attachment.

## Scoped change

- Preserved: 43-member inventory, plan positions and proportions, local ORIs,
  PYRAMID handedness, taper offsets, profiles, hardware plan axes, and all
  non-base pump geometry.
- Adapted per pump: sole/skid bearing, lower-gusset/sole bearing,
  saddle/mounting-pad bearing, fixed hex-head height, and anchor vertical span.
- The structural contact graph excludes all hardware and requires members
  1..19 and 40..43 to reach the five-member skid.

## Generated candidate

`output/2026-08-19_pumps_r4/JK_Pump_Build_2026-08-19_base_rebuild_r4_all_pumps.pml`

SHA-256: `F8F722361328A7F3D099C3384283C36F4648A6E81176BD627BEED6E918468403`

Audit SHA-256:
`0C3C6EF865DB75F393D2E189D85F65FDA28B074AD66A8B3A191A3E3F6BC3E029`

QA image SHA-256:
`D591B9C3F7BD63A9D49CCD3E0B9E73BDDF9D2237571D2EBDFA07E04B367C2C01`

## Static verification

- 30 pumps, 2616 elements.
- Numeric model verifier: 0 problems.
- Reference fidelity and hardware-free structural load path: 0 problems.
- Emitted macro parser: 0 text-level problems.
- 300/300 hex-head and anchor axes remain coaxial after output rounding.
- 29/29 injected defects caught.
- 168/168 non-base SUBE blocks are exactly unchanged from r3.

This is a candidate, not an accepted E3D result. A fresh E3D visual reload is
required under IR-11d.
