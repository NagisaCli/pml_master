# PML-STUDY-SCREW-001 — Refined Fastener Set / Primitive Selection

## Purpose

Build a refined screw detail and demonstrate that the choice of E3D element
is driven by the shape of each feature, not by whichever primitive a previous
project happened to use. One fastener set carries three real head forms, each
modelled with the primitive family that actually matches it:

| Feature | Element | Why this element |
|---|---|---|
| Hex head (M20-style bolt) | `EXTRUSION` + `LOOP` + `VERTEX` | A true hexagonal section; BOX would be square, a CYLINDER would be round |
| Button head (M10-style screw) | `DISH` | A real shallow dome; DISH is the crown primitive, not a flat plate (IR-9) |
| Square head (M16-style bolt) | `BOX` | A real square prism, axis-aligned, no ORI needed |
| Shanks, thread root | `CYLINDER` | Bodies of revolution |
| Thread ridges | thin `CYLINDER` discs | Additive thread detail; every ridge overlaps the root cylinder, so nothing is detached (IR-9b) |
| Under-head fillets, tip chamfers | `CONE` | True frustum transitions |

All element forms are individually VERIFIED in E3D Design Mk3.1.11.0
(EXTRUSION via PML-STUDY-EXTR-001/01-04; CYLINDER/CONE/DISH/BOX via the
production tank and pump macros). The assembly itself is new and awaits a
user E3D verdict; nothing here is promoted to `skill/` before certification.

This is a syntax-laboratory study. It does not modify any client project,
create a SITE/ZONE, or overwrite existing E3D elements.

## Receiving runtime

- AVEVA Everything3D 3.1
- E3D Design Mk3.1.11.0[Z31110-056]

## Geometry contract (Reference Values)

The dimensions are study values sized to the VERIFIED hex profile (20 mm
sides, 40 mm across corners, 34.64 mm across flats). They are not client
project data; every number here is a Reference Value with basis "fastener
detail study, sized to the PML-STUDY-EXTR-001 verified hex specimen".

| Screw | Head | Body | Thread | Tip | Total U |
|---|---|---|---|---|---|
| `/CODEX_SCREW_001_HEX_BOLT` at E -150 | EXTRUSION HEIG 20, hex 34.64 AF | CYLI DIAM 20 x 30 | root DIAM 17.5 x 40 + 16 ridges DIAM 20, pitch 2.5 | CONE 17.5 -> 7.5 x 5 | 0..99 |
| `/CODEX_SCREW_001_BUTTON_SCREW` at E 0 | DISH DIAM 24 x 6, RADIUS 36 | CYLI DIAM 10 x 35 | root DIAM 8.5 x 30 + 12 ridges DIAM 10, pitch 1.5 | CONE 8.5 -> 3.5 x 4 | 0..75 |
| `/CODEX_SCREW_001_SQUARE_BOLT` at E 150 | BOX 28 x 28 x 14 | CYLI DIAM 16 x 40 | root DIAM 13.5 x 35 + 14 ridges DIAM 16, pitch 2.0 | CONE 13.5 -> 5.5 x 4 | 0..96 |

Contact contract: every structural part meets its neighbour face-to-face
(head bottom = chamfer top, chamfer bottom = shank top, shank bottom = thread
root top, root bottom = tip top). Every thread ridge lies fully inside the
root cylinder's axial range and adds the major diameter around it. Nothing
is modelled below U 0.

## Isolated candidate

| Candidate | SHA-256 | Status |
|---|---|---|
| `candidate/01_refined_screw_set.pml` | `4EC02396EBD54D7F42E957A5091F9895246B521B64AD23EAE7363CED677D0923` | **VERIFIED — user-accepted in E3D 2026-08-05 ("OK")**; local PML1 + geometry verification clean |

One `EQUIPMENT` named `/CODEX_SCREW_001` under the current writable ZONE, with
one `SUBEQUIPMENT` per screw. 56 primitives: hex bolt 21, button screw 16,
square bolt 19.

## Local validation (already run)

`build_candidates.py` regenerates the candidate and verifies it before
writing:

- `wsb.pml_builder.validate_pml` — PML1-only, no banned forms, no render
  prologue, ORI-before-POS for CYLINDER/CONE/DISH and oriented BOX.
- Numeric geometry parse — occupied U range derived from each element's own
  datum (CYLINDER/CONE centre, BOX centre, DISH rim, EXTRUSION end plane),
  then: face-to-face contacts, ridge containment, positive bounds, screw axes
  at their E offsets, lowest point exactly U 0.

Command:

```bash
python Projects/E3D_Syntax_Lab/experiments/PML-STUDY-SCREW-001/build_candidates.py
```

## Required E3D observations

1. Select a writable ZONE, load the candidate with `$M <full path>`.
2. Confirm all three screws render: hex head shows six flat faces, button
   head shows a shallow dome, square head shows a square prism.
3. Confirm each screw reads as one connected solid: head meets shank, shank
   meets threads, threads meet the chamfered tip, no gaps or detached discs.
4. Run `queries/01_measure_screws.mac` (make each SUBEQUIPMENT current, then
   `$M`) and record the `Q ATT` output; screenshot the set.
5. Report any element that does not display or any face that does not touch.

Observations 1-3 were accepted by the user on 2026-08-05 ("OK").
Observation 4 remains optional: the Q ATT pack is ready for a detailed
attribute record.

## Promotion boundary

The user E3D verdict arrived 2026-08-05. The reusable knowledge
(primitive-per-head-form selection and the additive thread-ridge contract)
is promoted to `skill/knowledge/pml-spatial-lookup.md` as VERIFIED: every
element form used was already individually VERIFIED, the set was accepted in
E3D, and the local numeric checks passed. A reusable `wsb/` builder for
fastener detail can follow once a client project actually needs one; until
then the candidate remains the reference specimen.
