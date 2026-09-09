# JK_Pump_Build top-nozzle terminal connection r11

Status: **candidate; fresh E3D load and client visual acceptance required**.

## Trigger

The client rejected r10's spatial logic: the native nozzle bottom must connect
to the upper face of the size transition. Verbatim evidence:
`results/evidence/2026-08-20_r10_nozzle_root_feedback.txt`.

## Root cause

r10 preserved each upward NOZZLE HEIG while raising its casing connector to
8 mm below the fixed flange face. Since NOZZLE POS is the flange face, the
preserved HEIG left the physical root 100 mm below the casing crown. The added
body therefore overlapped the native nozzle instead of meeting its terminal
face. The r10 verifier encoded the same incorrect overlap requirement.

## Scoped correction

- Preserved CATR, flange-face POS including U, ORI and plan position for all 60
  native nozzles.
- Preserved all 32 horizontal native NOZZLE blocks completely.
- Adapted only HEIG on the 28 upward nozzles so `face U - HEIG` equals the
  casing connector upper face.
- Each connector starts 20 mm inside the crown and ends 20 mm above it.
- Retained 14 straight CYLINDER bosses and 14 overwidth
  CYLINDER/CONE/CYLINDER transitions with exact internal face and diameter
  closure.
- Retained the `205-PU-054` fixed plan offset and horizontal solid casing
  bridge.
- Preserved every pre-existing r9 primitive canonically. The 57 connector
  primitives remain the only additive geometry.

## Verification target

- 30 pumps, 2781 elements.
- 28/28 nozzle-bottom/connector-top terminal differences equal zero within
  0.01 mm; both gaps and penetrations fail.
- 60/60 nozzle CATR/POS/ORI values unchanged; 32/32 horizontal blocks fully
  unchanged; 28/28 upward HEIG fields are the only native-nozzle adaptation.
- 14 straight and 14 overwidth top connections; one offset bridge on
  `205-PU-054`.
- 0 reference-fidelity problems; 1080/1080 ribs correct; emitted text has
  0 problems.
- 41/41 verifier mutations caught, including a 100 mm HEIG extension that
  reproduces r10's overlap.
- Full repository suite: 529 passed, 4 skipped.

## Final candidate hashes (SHA-256)

- Macro: `A4AC916697C040F9FFBCA09C921636EDD82798D90811C40A481F87CAFEC889EA`
- Audit: `69D32ED2BBFB4D761F2EE584055C600C01D46457A8E23CBF29680D1DBC2839C7`
- QA image: `2FE9550A5C89B3B8D76EA262195443CF9876586EB406EDEA081B760011FFE027`
- Verbatim feedback evidence: `88199CF33B21046337D77FADC025E44917762CAAF7CC58F35ACBAA071028C689`
