# JK_Pump_Build base rebuild r5 — 2026-08-19

## Client correction captured

The r4 E3D reload showed two remaining defects:

- inner PYRA sole gussets stopped below their mounting top plate;
- an outer front PYRA stay started above its fixed sole plate.

The two user screenshots were preserved byte-for-byte:

| Evidence | SHA-256 |
|----------|---------|
| `2026-08-19_r4_e3d_inner_pyra_gap.png` | `C4D328335CBDD4F14EAC9DE1A0C26316EB963401FC18EDAA1AAC9E27A969ACB8` |
| `2026-08-19_r4_e3d_outer_pyra_float.png` | `24A7D0DD03A7C554F6C377079BC171F1B9E7BA7D4C419AA203704BD6B36DD004` |

## Scoped change

- Elements 6..9 now span exactly from their sole-plate top to the underside of
  the corresponding pump or motor mounting pad for each pump.
- Elements 14..19 now start exactly on their corresponding fixed sole-plate
  top while retaining their accepted plan geometry and machine-relative tops.
- Structural verification now uses explicit horizontal end-face contact and
  positive plan overlap. AABB crossings do not create graph edges.
- All non-base geometry, member plan arrangement, ORIs, PYRA offsets, profiles
  and fastener axes remain outside the delta.

## Generated candidate

`output/2026-08-19_pumps_r5/JK_Pump_Build_2026-08-19_base_rebuild_r5_all_pumps.pml`

SHA-256: `46D7E9D92F66C438EB4C4B23E465D188B1DB37C39B79D43C1300AF09E2C504D3`

Audit SHA-256:
`30754B7BD389D63C16F744DF8DADD30CA1F681AA02EA34B65B79964E2DF381A2`

QA image SHA-256:
`1433E94C123D0C441F6FB207D70B7E2165CCD01E75E7FCB096BF759376A4DD2B`

## Static verification

- 30 pumps, 2616 elements.
- 4/4 inner sole-gusset top interfaces per pump: zero U gap and positive end-
  face plan overlap.
- 6/6 outer side/motor-stay bottom interfaces per pump: zero U gap and positive
  end-face plan overlap.
- Numeric model verifier: 0 problems.
- Reference/end-face fidelity verifier: 0 problems.
- Emitted macro parser: 0 text-level problems.
- 31/31 injected defects caught.
- 168/168 non-base SUBE blocks exactly unchanged from r4.
- 972 cooling ribs checked, 0 wrong.

This is a candidate, not an accepted E3D result. A fresh E3D visual reload is
required under IR-11d.
