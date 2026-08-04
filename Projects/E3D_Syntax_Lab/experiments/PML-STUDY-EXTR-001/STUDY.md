# PML-STUDY-EXTR-001 — Native Pump EXTRUSION Study

## Purpose

Learn the editable `EXTRUSION` / `LOOP` / `VERTEX` construction used by the
native `/PMP-10` equipment listing, preserve the supplied evidence and isolate
the remaining E3D 3.1 geometry questions before this syntax is used in
production pump generation.

This is a syntax-laboratory study. It does not modify `JK_Pump_Build`, create a
SITE/ZONE or overwrite any existing E3D element.

## Receiving runtime

- AVEVA Everything3D 3.1
- E3D Design Mk3.1.11.0[Z31110-056]

## Immutable source evidence

| Evidence | Preserved file | SHA-256 |
|---|---|---|
| Native data listing | `source/2026-08-03_pmp10_native.txt` | `4CD84139C043C06635C4138C8F676680C7B5143043C32DE5EC11931BE9E52D26` |
| Front screenshot | `source/pmp10_front.png` | `ED9E9021CEE10870991651E52CEC7157D649C8C3247A7FD0D11FFEAFF6C5669B` |
| Side screenshot | `source/pmp10_side.png` | `31A7206974EFBCC4F859FFDB2B9182E0884995E3443B178C07BA2EC10E6F4DF7` |
| Rear screenshot | `source/pmp10_rear.png` | `EFE2714744F3ED886510B71EA7A2CBFFBA525381D8CB9FD3ABA6138B4DDCAB0D` |

The original desktop text file is also preserved unchanged at
`Projects/E3D_Syntax_Lab/imports/2026-08-03_pmp10_native.txt`.

## Native inventory

| Element | Count |
|---|---:|
| `EQUIPMENT` | 1 |
| `SUBEQUIPMENT` | 3 |
| `BOX` | 51 |
| `CYLINDER` | 17 |
| `DISH` | 3 |
| `PYRAMID` | 10 |
| `EXTRUSION` | 17 |
| `LOOP` | 17 |
| `VERTEX` | 120 |
| `NOZZLE` | 2 |
| `ELCONN` | 2 |

All 17 extrusions belong to `/PMP-10-BASE`. The syntax is used selectively,
not as a replacement for cylinders, boxes, dishes or pyramids.

## Evidence ledger

### VERIFIED from native export plus AVEVA evidence

- Editable hierarchy: `NEW EXTRUSION` -> `NEW LOOP` -> ordered
  `NEW VERTEX` elements.
- Each vertex uses a local position in the LOOP's XY plane; every observed
  vertex has local U = 0.
- `HEIG` extrudes the profile along the EXTRUSION's local Z direction.
- Cardinal `ORI Y IS ... AND Z IS ...` selects the local frame.
- One LOOP profile can be emitted without repeating the first vertex: the
  closing edge is implicit. The native listing contains coincident terminal
  vertices, while AVEVA's loop editor explicitly supports removing coincident
  vertices; generated output therefore normalizes only a repeated final point.
- The full element names `EXTRUSION`, `LOOP` and `VERTEX` are valid forms.

Evidence basis: the supplied native E3D listing, installed E3D 3.1 PML source
(`mmmcounterweight.pmlobj`) and
[AVEVA's Extrusion Primitive documentation](https://help.aveva.com/AVEVA_Everything3D/1.1/EUG/EUG4.05.3.html).

### TRACED from installed E3D 3.1 source — longitudinal datum and creation order

Reading the code that *writes* EXTRUSION elements (not just the sample data)
now supports a specific datum hypothesis:

- `dbenextrusion.pmlfrm:1448-1452` (negative extrusion creation) maps the
  picked point onto the surface plane, offsets it by the **full thickness**
  along the plane's -Z, then emits:

  ```
  NEW NXTR
  POSITION $!<position>
  ORI $!<this.surfacePlane.orientation>
  HEIGHT $!<this.thickness.val>
  ```

  Offsetting by the whole thickness only makes sense if POS is the profile
  end plane and the solid sweeps toward +Z: the far face lands on the surface.
  A centre datum would require a half-thickness offset.

- `dbeextrusion.pmlfrm:1153-1156` (positive extrusion creation) uses the same
  creation shape: `AT <plane.position>` -> `ORI <plane.orientation>` ->
  `HEIGHT <thickness>`.

- `mmmcounterweight.pmlobj:820-960` assigns `!!ce.position` from a frame's
  `startPosition` (or `endPosition` with the opposite local-Z orientation) and
  `!!ce.heig` from the frame's `length()`. The cylinder in the same method is
  positioned with `proportion(0.5)` — the code that wants a centre datum says
  so explicitly, and it does not for EXTRUSION.

**CONFIRMED in E3D 2026-08-04:** candidate 01 measured occupied U 1000..1800
for `POS U 1000` + `HEIG 800`, i.e. the EXTRUSION `POS` is the LOOP/profile
plane at one longitudinal end and `HEIG` sweeps toward local +Z — exactly the
installed-code interpretation above. Candidate 03 measured identical occupied
ranges for POS->ORI (A/C) and ORI->POS (B/D), so assignment order is not
significant for the tested forms.

### NATIVE-OBSERVED physical use

- One extrusion forms an asymmetric/notched support profile with `HEIG 440mm`.
- Sixteen extrusions form real regular-hexagonal heads around eight cylindrical
  shanks: two heads per shank. The observed profile has 20 mm sides, 40 mm
  across corners, 34.64 mm across flats and area 1039.2 mm2. Those dimensions
  belong to this specimen; they are not universal bolt dimensions.
- The sample demonstrates syntax balance: EXTRUSION is reserved for profiles
  that are materially better expressed as a true section, while other features
  retain the primitive family that matches their shape.

### Study status — closed

All geometry questions are now settled by user E3D observation on 2026-08-04:
end-plane datum (01), order independence (03) and the two-head fastener
contact contract (04, confirmed visually as matching the native `/PMP-10`
pattern: lower head 10 mm inset with the shank protruding, upper head flush).

## Isolated candidates

| Candidate | Purpose | SHA-256 | Status |
|---|---|---|---|
| `candidate/01_extrusion_axes_and_datum.pml` | Three asymmetric L profiles with local Z aimed Up, East and North; query occupied extents and POS relationship | `D17A4B02FD087C9FC814B5613DF03BC0DB63D5934CCB14B1DEEFC459F18DE8E0` | **VERIFIED** — user measured U 1000..1800 for POS U 1000 / HEIG 800 (2026-08-04) |
| `candidate/02_extruded_hex_fastener.pml` | One cylindrical shank plus two true hex EXTRUSION heads; inspect contact and alignment | `0B7E219883A8CAAA4576C75573FA4D753D6F00BE119B2C087C027639E2103CB4` | **Measured 2026-08-04** — coaxial; lower head matches native (POS U 20), upper head 10 mm proud vs native flush (POS U 100) |
| `candidate/03_extrusion_order_sensitivity.pml` | Two 90-degree orientation pairs; A/C use native POS->ORI, B/D use ORI->POS at the same POS; discriminates assignment-order sensitivity | `2DEE4536D2C15230788D8AD90869F4FE5D0E26D1C4AD580271CBCF3F8C0AC9DA` | **VERIFIED** — A/C and B/D occupied ranges identical (2026-08-04) |
| `candidate/04_extruded_hex_fastener_native_contact.pml` | Same shank/heads as 02 but with the native contact contract: lower head POS U 20 (10 mm inset), upper head POS U 90 (flush with shank top) | `B1A4D7DBCFEA06C9814E78DEF5E85F8E40B42D7064B2168ED9B03D352C69B60C` | **VERIFIED** — user visual confirmation 2026-08-04 ("EXTR完美") |

All candidates create one uniquely named `EQUIPMENT` under the current
writable ZONE. They do not create or delete project administration elements.

Query pack: `queries/01_measure_extrusions.mac` — run `$M` with each EXTRUSION
current; capture the Q output and occupied extents.

## Required E3D observations

1. Load candidate 01 and confirm all three profiles render with the same local
   shape. — **DONE** (2026-08-04).
2. For each EXTRUSION, record its world occupied minimum/maximum E, N and U or
   query the attributes that establish the longitudinal POS datum. Predictions
   with POS U 1000 and HEIG 800: end-plane datum spans U 1000..1800 for the
   Up-oriented profile; centre datum U 600..1400; far-face datum U 200..1000.
   — **DONE**: U 1000..1800, end-plane datum.
3. Confirm which side of POS receives positive `HEIG`, or whether the solid is
   centred about POS. — **DONE**: +Z.
4. Load candidate 02 and inspect whether both hex heads are coaxial with and
   physically touch the shank. — **DONE** (2026-08-04): coaxial; shank
   U 10..110, lower head 20..40 (native pattern), upper head 100..120
   (10 mm proud of the shank top; native is flush at 90..110).
5. Load candidate 03 and compare the occupied extents of A/C (POS->ORI) with
   B/D (ORI->POS) at identical POS values. Equivalent extents prove order
   independence; differing extents prove order sensitivity. — **DONE**:
   identical; order-independent.
6. Return screenshots plus any query output. — Partial: numerical results
   supplied; no screenshots archived.
7. Load candidate 04 and confirm: lower head occupies U 20..40 with the shank
   protruding 10 mm below, upper head occupies U 90..110 flush with the shank
   top, all three coaxial at E/N = 0. — **DONE** (2026-08-04): visually
   confirmed.

## Promotion boundary

The reusable builder emits the evidence-backed hierarchy, validates a non-zero
planar profile and treats POS as the profile end plane (VERIFIED). It must not
claim a bottom-face or centre abstraction: `PML-STUDY-EXTR-001/01` measured the
end-plane datum in E3D Design Mk3.1.11.0 on 2026-08-04. The two-head fastener
contact contract is now defined from the native `/PMP-10` specimen (lower head
10 mm inset, upper head flush) and candidate 04 was visually confirmed in E3D
on 2026-08-04. The study is closed; production generation may treat POS as the
profile end plane and use the two-head fastener contact contract without
further experiment.
