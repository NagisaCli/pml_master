# PML-STUDY-NCYL-001 — Negative cylinder (NCYLINDER) placement forms

## Purpose

The JK_Pump_Build r2 NCYLINDER holes loaded but did not cut. The user verified
manually that a primitive with its own negative child does cut, so the failure
is in our emitted form, not in the system. This study isolates two unknowns:

1. `NAPPFLAG 2` — AVEVA's own hole code sets `!!ce.nappflag = 2`
   (`hmcontrol.pmlobj` createHoleNegativeExtrusion) and defaults `NAPPFLAG -1`
   to 2 (`strSctnGensec.pmlobj`). r3 now emits `NAPPFLAG 2` on every
   NCYLINDER.
2. POS/ORI semantics of a negative child in a native INPUT listing — world
   coordinates (r2/r3 form), inherited pose (no POS/ORI), zero/local offset,
   or standalone at SUBE level.

## Candidates

| Id | Plate E | NCYLINDER form |
|----|---------|----------------|
| C1 | 0 | child, world POS/ORI, Z is E (r3 form) |
| C2 | 4000 | child, no POS/ORI (inherits owner) |
| C3 | 8000 | child, POS E 0 N 0 U 0 + Z is E (local/zero probe) |
| C4 | 12000 | standalone at SUBE level, world POS/ORI |

All plates are BOX 20 x 200 x 300 at U 150 centre; all NCYLINDERs are
DIAM 60 / HEIG 400 with `NAPPFLAG 2`.

## Observations to report

- Which candidates cut a visible hole?
- C1/C3: is the hole at U 250 / U 0 (world) or offset from the plate centre
  (relative interpretation)? Horizontal (axis E) holes show a circle on the
  plate N face.
- C2: is the hole vertical (axis U, inherited) and centred on the plate?
- C4: does a standalone negative primitive subtract at all?

## User verdict — 2026-08-06

- **C2 (child, no POS/ORI, inherits owner)**: hole cuts correctly.
- **C3 (child, POS E 0 N 0 U 0 + ORI Z is E)**: hole cuts correctly.
- **C1 (child, world-coordinate POS E 0 N 0 U 250 + ORI)**: element loads
  (visible in the Explorer tree) but cuts nothing — the child's POS is
  interpreted in the owner's local frame, so the world value placed the hole
  far off the plate.
- **C4 (standalone NCYLINDER at SUBE level)**: rejected —
  `(41,8) Cannot create a NCYL at this level.`

### Conclusion (VERIFIED forms)

1. A negative primitive must be a **child of a positive primitive**;
   standalone negatives at SUBE/EQUI level are not creatable.
2. The child's `POS` is **local to the owner** (owner centre + offset), not
   world coordinates. `POS E 0 N 0 U 0` equals the owner centre.
3. The child's `ORI` is honoured (C3 cut a horizontal hole through a vertical
   plate with `ORI Y is U and Z is E`).
4. `NAPPFLAG 2` is required for the negative to subtract.
5. JK_Pump_Build r4 converts each removed stub's world POS into an offset
   from the BOX21 owner centre (`POS E 0 N 0 U <dz>`, same ORI/DIAM/HEIG,
   `NAPPFLAG 2`).

## Evidence

- AVEVA `hmcontrol.pmlobj` (`.createHoleNegativeExtrusion`): `NEW NXTR` then
  `!!ce.nappflag = 2`, positioned with `MOVE ... ALONG <zDir> THROUGH <pos>`.
- AVEVA `strSctnGensec.pmlobj` (`.tmplRestore`): collects negatives with
  `NAPPFLAG eq -1` and sets `NAPPFLAG 2`.
- AVEVA `mmmcounterweight.pmlobj` / `aslostepladderpresenter.pmlobj`: nested
  NBOX children may carry their own orientation/position in PML2 object code.
- User native listing `JK-Tank_Build/imports/2026-08-04_WSB_TA.txt`: nested
  NCYLINDER with no POS/ORI (inherited pose).
