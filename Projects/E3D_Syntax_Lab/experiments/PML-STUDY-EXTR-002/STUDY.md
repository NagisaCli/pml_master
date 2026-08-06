# PML-STUDY-EXTR-002 — High-Fidelity End-Suction Pump

## Purpose

Push EXTRUSION to its intended role: any constant, non-rectangular section
that a 2D draughtsman could draw, E3D can extrude. Candidate 01 (a bolted
channel frame) was rejected by the user on 2026-08-05 as too ordinary and
not enough detail ("太普通了细节也一般，也没有充分发挥拉伸体的特色"). This
study now targets one high-fidelity end-suction centrifugal pump with no
primitive-count ceiling, where the irregular solids are EXTRUSION profiles
and the basic solids are used only where they are the true form.

| Feature | Construction | Profile |
|---|---|---|
| Volute casing | One EXTRUSION, 260 mm deep | Archimedean spiral + radial cutwater slit, 19 vertices |
| Motor frame | One EXTRUSION, 560 mm long | Circle + 12 cast cooling fins merged into one LOOP, 48 vertices |
| Impeller | 6 EXTRUSION curved blade bands + 2 CYLINDER | Swept blade profile, 12 vertices each |
| Fan | 8 EXTRUSION curved blades + hub CYLINDER | Swept blade profile, 12 vertices each |
| Coupling elastomer | One EXTRUSION | 16-tooth star profile, 32 vertices |
| Fan shroud grille | 12 EXTRUSION arc strips between two disc rings | Arc strip, 6 vertices each |
| Base frame | H-section beams, corner-cut plates, rounded anchor pads | H beam 12 vertices; plates 8; pads 20 |
| Flanges / nuts | Octagonal flange plates and hex nuts | 8 / 6 vertices |
| Shaft, necks, studs, bosses | CYLINDER | Bodies of revolution |

No BOX is used anywhere in this candidate.

## Receiving runtime

- AVEVA Everything3D 3.1
- E3D Design Mk3.1.11.0[Z31110-056]

## Geometry contract (Reference Values)

All dimensions are study values with basis "high-fidelity pump syntax study,
proportions follow a typical end-suction centrifugal pump with an IEC-frame
motor". They are not client project data.

Layout: shaft centreline horizontal along E at N 0, U 400; suction flange
faces -E; discharge flange faces +U; motor behind the pump at +E.

| Component | Extent | Notes |
|---|---|---|
| Base frame | E -220..1680, N -230..230, U 0..100 | Two H-beams + three cross beams; pump and motor plates U 80..100; four anchor pads + bolts |
| Volute | E -130..130, N -280..280, U 120..680 | Spiral r 190..280 mm around (N 0, U 400) |
| Suction connection | E -208..-130 | Neck DIAM 190, octagonal flange, 8 studs + hex nuts |
| Discharge connection | U 680..804 | Neck DIAM 150, octagonal flange, 8 studs + hex nuts |
| Seal gland / boss | E 130..184 | Rounded-square gland + boss |
| Pump feet | N +-135..175, U 100..205 | Top face embeds into the volute underside |
| Impeller | E -70..50 | Hub, suction ring, 6 curved blades inside the volute |
| Bearing housing | E 150..320 | Finned octagon (8 fins), two feet, two caps, shaft DIAM 55 |
| Coupling | E 320..530 | Hex hubs, 16-tooth star elastomer; shroud E 320..560, U 100..610 |
| Motor | E 510..1470 | Frame + fins, DE/NDE discs and bosses, 4 feet, 12 end-cover studs, terminal box, fan, shroud, nameplate |

Contact chain (all verified numerically): base top U 100 -> feet/plates;
volute -> pump feet, suction neck and discharge neck; gland -> bearing cap ->
coupling hub -> elastomer -> motor hub -> DE boss -> DE disc -> frame ->
NDE disc -> NDE boss -> fan shroud; nuts seat on flange/plate faces.

### Local-frame notes

- The EXTRUSION local frame is right-handed: X = Y x Z. With
  `ORI Y IS U AND Z IS E` local X is N; with `ORI Y IS N AND Z IS U`
  local X is E.
- For a negative extrusion axis (`ORI ... Z IS W`), POS is the profile
  plane at the *inner* face: the solid sweeps from POS toward -E. The
  suction flange therefore uses POS E -160 (neck face), not its outer face.
- Profiles carry either absolute world coordinates (volute, motor frame,
  plates, box, nameplate) or relative coordinates (flanges, nuts, pads);
  the builder is deliberately permissive because the verifier re-derives
  occupied ranges from the emitted POS/ORI/VERTEX data.

## Candidates

| Candidate | SHA-256 | Status |
|---|---|---|
| `candidate/01_bolted_channel_frame.pml` | `70CE42874B505A4B739FEBB3C456CB4107DC2901659AC5DE670AA4F5BECB4094` | **REJECTED 2026-08-05** — user: too ordinary, not enough detail, under-uses EXTRUSION |
| `candidate/02_high_fidelity_pump.pml` | `341D2E565A99E4BADEE951D790434FBC555E4FC943B9047A19F2517E0AF1B8F9` | Local validation clean; superseded by 03 after user bug report |
| `candidate/03_high_fidelity_pump_v3.pml` | `1086C7E167FBC162F7F27F20EC459C9B674B698C72539D4B90796EFC5EBDD8A3` | **PRESSURE TEST** 1154 primitives (950 EXTRUSION / 204 CYLINDER / 0 BOX), 23 712 profile vertices, floating audit clean; user-verified in E3D |
| `candidate/03_high_fidelity_pump_v3_physics_fixed_20260805.pml` | `04FE9886BB6BF5B5AB6C8CB07E074D51F7601141FB9C4FE0DB943EEC171AC5DC` | **USER-ACCEPTED 2026-08-05** ("基本可以了") physics-fixed working baseline from the user-edited native export; 1,104 primitives; see BUG_REVIEW_03.md |

## Candidate 03 round 2 — physics fixes (2026-08-05)

User feedback after loading the cleaned candidate: pedestal nuts float,
junction boxes do not display as boxes, and the pump-to-top-nozzle connection
is open. The user also edited the export themselves (deleted two casing
rounded plates and one bearing breather cylinder) and returned it as the new
working baseline (`source/2026-08-05_pump_edit_user_native.txt`).

Round-2 fixes (all evidence in [BUG_REVIEW_03.md](BUG_REVIEW_03.md)):

- Pedestal nuts seated on the sole plates: U 140..156 instead of U 170..186.
- Junction boxes rebuilt as native `BOX` primitives (60 x 50 x 50 mm) so they
  display as boxes.
- Top suction nozzle pipe extended U 745..835 -> U 678..835, embedding it
  into the volute dome (peak U 700, dome at r 85 ≈ U 682) — no rim gap.
- Discharge nozzle pipe extended X -208..-168 -> X -208..-150, flush with the
  volute left face.

Result: 46,613 -> 46,455 lines, 1,104 primitives, balanced parse, envelope
unchanged, user-accepted as a modeling pressure test. Nothing is promoted to
`skill/` from a single stress test.

## Candidate 03 — internal drive train and full profile detail

User feedback on 02: raise profile resolution, fix floating parts (terminal
box ears, volute ribs, cross beam), model the complete drive train and true
appearance, 1000-5000 solids, no padding. Root causes and numerical
evidence for every reported bug are in [BUG_REVIEW_02.md](BUG_REVIEW_02.md).

Structure (Reference Values; sources: Grundfos end-suction module, EASA
squirrel-cage rotor design, Firgelli jaw-coupling mechanism, CFturbo volute
geometry, Goulds 3180 IOM):

| Assembly | Primitives | Highlights |
|---|---|---|
| Base frame | 48 | H-beams, lower lapped cross beams (U 0..80), corner-cut plates, drainage grid, 16 stiffeners, anchor pads |
| Casing | 170 | 96-vertex volute spiral + cutwater, 36 embedded ribs (6 mm), pump cover + 16 studs, suction/discharge flanges + 16 studs each, mechanical seal stack (seat, static/rotating rings, 10 spring washers, gland) |
| Impeller | 24 | Closed impeller: front/back shrouds, 14 curved blades, hub, inlet ring, 6 balance ribs |
| Bearing housing | 92 | 16-fin housing, labyrinth rings, two rolling bearings (20 rollers each), caps, oil cup, sight glasses, 6-section stepped shaft |
| Coupling | 85 | Two 6-jaw hubs, 32-tooth star spider, retaining rings, 8 set screws, guard (2 rings + 60 grille bars) |
| Motor | 719 | 24-fin frame, 4 embedded cast pads, 32 stator lamination discs, 180 winding end coils, 72 slot wedges, 28 rotor discs, 144 squirrel-cage bars, end rings + 24 cast fan blades, 2 rolling bearings, finned end shields + 24 studs, 20-blade fan, 72-bar shroud, terminal box seated on pads with 4 bolts, nameplate, ground, lifting eye |
| Fasteners | 16 | Pump-foot bolts, guard feet bolts |

Verification (automated in `build_high_fidelity_pump_v3.py`):

- PML1 validation clean; no BOX.
- Floating-part audit: every one of the 1154 primitives must intersect at
  least one other primitive (1 mm tolerance). Zero floating parts.
- Repair checks: pads embed below the frame top (578 < 581.9); box ears sit
  exactly on pad tops (608); every volute rib overlaps the wall; cross
  beams sit lower than and lap the main beams.
- Internal drive train inside the volute and motor frame; shaft centreline
  N 0 / U 400 for all rotating bodies.
- Envelope, lowest point U 0, all profiles non-degenerate, 23 712 profile
  vertices (about 20x candidate 02).

## Local validation (already run)

`build_high_fidelity_pump.py` regenerates the candidate and verifies it
before writing:

- `wsb.pml_builder.validate_pml` — PML1-only, no banned forms, no render
  prologue, ORI-before-POS for CYLINDER.
- Numeric geometry parse — every primitive's occupied world range is
  re-derived from its own datum (CYLINDER centre, EXTRUSION profile end
  plane), then checked: lowest point exactly U 0, assembly envelope,
  shaft centreline N 0 / U 400 for every axial body of revolution, the full
  contact chain above, all profiles non-degenerate, no non-positive
  dimensions, 185 primitives (128 EXTRUSION / 57 CYLINDER / 0 BOX).

Command:

```bash
python Projects/E3D_Syntax_Lab/experiments/PML-STUDY-EXTR-002/build_high_fidelity_pump.py
```

## Required E3D observations

1. Select a writable ZONE, load the candidate with `$M <full path>`.
2. Confirm the pump reads as one connected machine: base frame -> feet ->
   volute; volute -> suction/discharge connections; coupling chain; motor
   frame with fins, terminal box and fan shroud.
3. Confirm the profile solids render as intended: volute spiral shows the
   snail-shell outline and cutwater slit; motor frame fins are one solid
   casting; hex nuts and octagonal flanges show their true faces; elastomer
   shows 16 teeth.
4. Run `queries/02_measure_pump.mac` (make each SUBEQUIPMENT current, then
   `$M`) and record the `Q ATT` output; screenshot the set.
5. Report any element that does not display, any face that does not touch,
   or any part that floats.

## Promotion boundary

The candidate uses only element forms already individually VERIFIED in E3D
Design Mk3.1.11.0. The assembly-level knowledge it demonstrates — profile
families per physical form, right-handed local-frame mapping, negative-axis
datum handling — is promoted to `skill/knowledge/pml-spatial-lookup.md`
only after the user's E3D verdict.
