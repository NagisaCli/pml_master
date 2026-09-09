# JK_Pump_Build top-nozzle width branches r12

Status: **candidate; fresh E3D load and client visual acceptance required**.

## Trigger

The client supplied a schematic and clarified that the socket/reducer applies
only when nozzle DN exceeds casing width; a contained nozzle must directly
penetrate the casing with at least 70% outside. Verbatim and image evidence:
`results/evidence/2026-08-20_r11_width_branch_feedback.txt` and
`results/evidence/2026-08-20_r11_top_nozzle_schematic.png`.

## Root cause

r11 correctly joined the native NOZZLE bottom to its connector terminal face,
but generalized one additive construction to all upward nozzles. It retained
14 unnecessary straight bosses and placed an extra upper CYLINDER between each
overwidth CONE and native NOZZLE. The verifier checked r11's closed faces but
did not encode the client's conditional topology or minimum direct external
proportion.

## Scoped correction

- Preserved CATR, flange-face POS including U, ORI and plan position for all 60
  native nozzles; all 32 horizontal NOZZLE blocks remain canonical unchanged.
- Adapted only HEIG on the 28 upward nozzles.
- For the 14 nozzles whose verified DN is no greater than casing axial width,
  emitted no additive connector. The native root penetrates the crown and 75%
  of NOZZLE HEIG remains outside, above the required 70% minimum.
- For the 14 overwidth nozzles, emitted exactly a casing-owned lower CYLINDER
  socket and one concentric CONE. The socket starts 20 mm inside the crown,
  projects 8 mm above it and the CONE ends 20 mm above the crown. Its upper
  face equals the native NOZZLE bottom; there is no added upper neck.
- Retained the `205-PU-054` fixed plan offset and horizontal solid casing
  bridge.
- Preserved every pre-existing r9 primitive canonically. Only 14 CASING blocks
  receive 29 added solids: 14 sockets, 14 CONEs and one offset bridge.

## Verification target

- 30 pumps, 2753 elements.
- 14/14 overwidth nozzle-bottom/CONE-top differences are 0.000 mm.
- 14/14 direct-nozzle external ratios are 0.7500 and every root is below the
  casing crown.
- 60/60 nozzle CATR/POS/ORI values unchanged; 32/32 horizontal blocks fully
  unchanged; 28/28 upward HEIG fields are the only native-nozzle adaptation.
- 0 reference-fidelity problems; 1080/1080 ribs correct; emitted text has
  0 problems.
- 42/42 verifier mutations caught, including a direct nozzle reduced to 37.5%
  external projection.
- Full repository suite: 529 passed, 4 skipped.

## Final candidate hashes (SHA-256)

- Macro: `C2578497900AB4997CE549629C50A1F2C71BC61A5908EDE534531BA810C644A2`
- Audit: `411646BEF333E5322D69F0403D81FA2293E2D30DBF9517D3358261ADB5865DBC`
- QA image: `F3E4AA486E993DA8DF92C83A51DCDFF7DBC058A800F5CB4A421F38EF96CA7739`
- Verbatim feedback evidence: `661B4B62BB28F19B3DAD0BB89C433D2B5746B2BD8442D17E05280CE8FDDC29C2`
- Client schematic evidence: `98EE3179D218A143F2D23D86D86850DB96C5D237EB116F7F8A99672A9B168D05`
