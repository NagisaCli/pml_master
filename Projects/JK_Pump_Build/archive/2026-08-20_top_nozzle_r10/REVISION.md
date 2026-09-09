# JK_Pump_Build top-nozzle casing connection r10

Status: **candidate; fresh E3D load and client visual acceptance required**.

## Trigger

The client accepted the r9 motor-tail construction, then required every upward
nozzle to visibly join its casing and project above it. Where the upward nozzle
is wider than the casing barrel, the connection must resemble a smooth reducer
built from equipment primitives rather than piping. The native nozzle's
vertical height must not move. Verbatim feedback:
`results/evidence/2026-08-20_r9_top_nozzle_feedback.txt`.

## Scoped correction

- Preserved all 60 r9 native NOZZLE blocks exactly: CATR, POS including U, ORI
  and HEIG are unchanged.
- Added primitive-only casing connections to the 28 pumps with upward nozzles.
- Fourteen DN150 nozzles fit their casing axial width and use one straight,
  crown-embedded CYLINDER boss.
- Fourteen DN150 nozzles exceed the casing axial width and use a contained lower
  CYLINDER socket, a concentric CONE and a DN-sized upper CYLINDER neck.
- `205-PU-054` retains its fixed 308 mm casing/nozzle plan offset and receives
  one overlapping solid CASING bridge. Neither source position is moved.
- Every existing r9 primitive is canonical unchanged. The complete delta is 57
  additive CASING primitives.

## Verification target

- 30 pumps, 2781 elements.
- 28/28 top-nozzle connections present: 14 straight and 14 overwidth.
- Connector crown embedment, visible projection, neck overlap, vertical
  interface closure, smooth diameter matching and casing-width containment.
- 60/60 native NOZZLE blocks unchanged from r9.
- 40/40 mutations, including missing connector, open reducer/neck interface,
  oversized lower socket and missing offset bridge.

## Final candidate hashes (SHA-256)

- Macro: `A9B607452BD3E1893752C4F2E62D0C3A09C732D63C820F189C3C16B848B75267`
- Audit: `BD18360AFCDC490B17B14E3CD8CA07C1A112CC4FAD1D845C2BA597F65C61FA0D`
- QA image: `593D8C88EC605823EFCE0C77BDFB453F2F0C32172D25C2438BBDB733A92627E9`
- Verbatim feedback evidence: `2436DFCCBE32BA6C301910FD25B0A58CC4E5AB3E07CAC9FC77619646E0EE3CAE`
