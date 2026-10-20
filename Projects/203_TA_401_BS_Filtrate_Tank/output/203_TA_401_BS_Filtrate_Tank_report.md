# 203-TA-401 BS FILTRATE TANK — E3D model, R2

**Macro:** `Projects/203_TA_401_BS_Filtrate_Tank/output/203_TA_401_BS_Filtrate_Tank.pml`
**Generated:** 2026-09-22 · 60 solids + 11 nested voids · 12 native `NOZZLE` elements · 18 subequipments
**Source:** ANDRITZ 900135359 rev 0 (PRELIMINARY) + the nozzle-modification annotations in the accompanying DWG
**Status:** numeric verification clean; **not yet loaded in E3D**, so nothing here is verified in the project's sense (IR-11d).

> **R2 supersedes R1.** R1 was rejected for model precision and accuracy, correctly. It
> approximated three things it did not have to, and every one of them is now exact — see
> §0.

---

## 0. What changed in R2, and why R1 was wrong

| R1 | R2 | Why it matters |
|---|---|---|
| Both air-separation cylinders arrayed from 20/24 flat `BOX` facets | `CYLI` with a nested `NCYLINDER` bore — a true hollow solid | A 24-facet Ø2214 cylinder is up to 15 mm out of round. Wall thickness was right; the shape was not. |
| Shell a solid `CYLI`, internals buried inside it | Hollow shell, same way | The internals are now visible and the tank interior is not modelled as steel — which is also what clash detection wants. |
| Stiffening rings solid discs Ø6212 | Hollow rings | IR-9b in spirit: a ring is not a disc. |
| Separation wall = 32 straight chords | **One `RTORUS`** | The wall is a true circular arc. Both drawn faces fit a common centre to **0.002 mm** over 33 points: R 9000.00 inside, 9006.35 outside — the same 6.35 plate as the shell — about a centre 10502.3 mm from the tank axis at az 105.00 (110.00 as issued). The chord approximation threw all of that away. |
| 8 roof rafters × 6 stepped boxes = 48 primitives | 8 `EXTRUSION`s with a parallelogram `LOOP` | A rafter is now one true sloped member on the 12° plane, not a staircase. Verified profile slope 11.999°. |
| Overflow seal box a solid `BOX` | `BOX` + nested `NBOX` at the dimensioned 5 mm plate | It is a seal box; it has to be hollow. |
| N5 drawn as a bare catalogue flange | Reinforcing pad added, measured out to R3051.8 | The drawing calls it a PAD FLANGE. |

The element forms all come from **this account's own native E3D export**,
`Projects/205_TA_059_BLEACH_PLANT_SCRUBBER.pml`, which uses `NCYLINDER`, `NBOX`,
`RTORUS` and `CTORUS`. R1 avoided them as "unverified" and reached for facets
instead. That was the wrong call: the evidence was already in the project.

### Two precision bugs the verifier caught before delivery

1. **Rounded arc geometry.** Storing the wall's arc centre as "r 10502.3 / az 105.00"
   and its sector as "start 149.62°, span 30.75°" put the far end **10 mm** off the
   shell. The sector is now *derived* in the builder from the fitted centre, so both
   ends meet the shell plate by construction.
2. **`ANGL` emitted at one decimal place.** `_fmt()` is right for millimetres and far
   too coarse for an angle: 0.1° on a 9 m radius is **15.7 mm** of arc. Angles now
   carry six decimals. Both wall ends now land on the plate mid-thickness at
   R3003.2, and the arc measures 4831.5 against the drawn 4830.3.

---

## 1. Completed equipment

| | |
|---|---|
| Tag | 203-TA-401 |
| Name | BS Filtrate Tank (drawing title: DDW FILTRATE TANK) |
| Element | `/203_TA_401` |
| Duty | Filtrate, ρ 1050 kg/m³, 226 m³ nominal |
| Design | EN14015 / API650, 2 kPa(g) + hydrostatic max / −2 kPa(g) min, 100 °C / 0 °C |
| Material | 1.4307 or equal |

---

## 2. Modelling parameters

### Vessel

| Feature | Value | Where it came from |
|---|---|---|
| Shell | ID 6000 × 6.35 wall, U 0 → 8000 | "INSIDE Ø6000", "8000 SHELL"; wall measured 3006.35 − 3000.00 |
| Bottom | flat plate Ø6133.6 × 9.5 at U 0 | measured R3066.8, 60 mm proud of the shell |
| Roof | 12° cone, eave U 8003.8 at R3006.35 → U 8504.7 at R653 | annotated 12°; **measured 11.98°** over 2333 mm of run |
| Roof collar | OD 1305.5 × 200, U 8504.7 → 8704.7, deck plate on top | measured R652.73 / R646.37 |
| Roof rafters | 8 `EXTRUSION`s at az 0/45/…/315, 80 wide × 163 deep, R651.5 → R2984.8, true 12° parallelogram profile | measured; the 45° pairs project at 16.71° in the elevation, which is exactly `atan(tan12°/cos45°)` — an independent confirmation of both the slope and the count |
| Stiffening rings | 100 × 9.5 at U 3500, 5000, 6500 | measured 6211.4 long, i.e. 100 mm proud each side |
| Overflow level | U 7375 | "7375 OVERFLOW LEVEL" |
| Volume check | π/4 × 6.0² × 8.0 = **226.2 m³** vs the drawing's **226 m³** | independent reconciliation of ID and height |

### Internals

| Feature | Value |
|---|---|
| Inner air-separation (seal) cylinder | ID 1502.5 / OD 1515.2, U 0 → 5105 |
| Outer air-separation cylinder | ID 2201.5 / OD 2214.2, U 0 → 4298, base ring OD 2372.7 |
| **Cylinder axis** | offset **E −501.9, N 0** — both cylinders are eccentric to the tank axis |
| Radial ribs | 4 off between the cylinders, at 35.5 / 125.3 / 213.8 / 304.2° about the cylinder axis |
| Separation wall | **one RTORUS**: R 9000.00 / 9006.35 (6.35 plate), U 0 → 7800, about an arc centre 10502.3 mm from the tank axis at az 105.00. Meets the shell plate at az 52.34 and 157.66; arc length 4831.5 at R9000 |
| Soap launder | R2400 → 3000 (shell bore is the outer wall), az 264.5° → 339.6°, rim U 5400, floor U 5170, 4 radial dividers + 2 end plates |

The launder span reconciles with the drawing's own dimension: chord at R2400 over 75.1° = **2921 mm**, which is the "2921" dimensioned on view B-B.

### Overflow water-seal box (E-E 1:15)

Box U 6589 → 7950 (E-E total height 1361) at az 30°, 400 radial × 500 tangential, opening to the shell 250 high with its sill at U 6975 (6589 + 386). Downcomer Ø323.9 × 5 on R3544.2, which is the "3542" dimensioned on view A.

---

## 3. Nozzle schedule as modelled

Azimuth is measured clockwise from the drawing's 0° mark, modelled as North. E/N are the flange-face coordinates in the tank-local frame.

| Mark | Size | Service | Elev. U | Azimuth | Change from the issued sheet | Flange face | E | N |
|---|---|---|---|---|---|---|---|---|
| N1.1 | DN300 | Filtrate in — inner seal tank (2 × DN200 extraction filtrate combined) | 4500 | 336.8 pierce / 335.0 axis | unchanged | R3456.4 | −1374.5 | 3171.1 |
| N1.2 | DN300 | Filtrate in — outer tank (2 × DN150 washing filtrate combined) | 4300 | 150.4 | 155.4 → 150.4 | R3459.5 | 1708.8 | −3008.0 |
| N2.1 | DN250 | Pump out | 476 | 0 | 180 → 0, and DN300 → DN250 | R3254.1 | 0.0 | 3254.1 |
| N2.2 | DN300 | Pump out → digester displacement liquor tank | 476 | 60 | 90 → 60, and DN200 → DN300 | R3301.9 | 2859.5 | 1651.0 |
| N5 | DN80 | Level instrument, PN40 pad flange | 600 | 345 | 165 → 345 | R3085.0 | −798.5 | 2979.9 |
| N6 | DN100 | Drain | 0 | 15 | 30 → 15 | R3301.2 | 854.4 | 3188.7 |
| N8 | DN300 | Vent, roof centre, vertical up | 8809.4 | — | unchanged | on the axis | 0.0 | 0.0 |
| N9 | DN300 | Overflow outlet, vertical down | 6589 | 30 | 45 → 30 | R3544.2 | 1772.1 | 3069.4 |
| N11 | DN15 | Overflow water in, seal-box top | 8000 | 30 | 45 → 30 | R3222.6 | 1611.3 | 2790.9 |
| N12 | DN25 | Overflow drain, seal-box bottom | 6389 | 30 | 45 → 30 | R3222.6 | 1611.3 | 2790.9 |
| N13 | DN80 | Overflow vent, seal-box top | 8283 | 30 | 45 → 30 | R3544.2 | 1772.1 | 3069.4 |
| MW | DN600 | Davit-type manway ID600 | 700 | 270 | unchanged | R3215.0 | −3215.0 | 0.0 |

**Every rotation in the DWG is counter-clockwise in plan** (azimuth decreasing). That is not an assumption: the original and modified view copies were measured independently and the deltas came out −15° for N6 and N9, −30° for N2.2, −5° for N1.2 and the separation wall, and 180° for N2.1 and N5, matching each annotation's stated amount.

**N1.1 is a chord entry, not a radial nozzle.** Its two pipe walls in the modified B-B copy are 325.7 apart — DN300 pipe OD 323.9 — on a line offset 96.2 mm from the tank axis. It pierces the shell at az 336.8° and runs on bearing 155° into the inner seal cylinder, which is why its bore direction (335.0°) and its penetration azimuth differ.

Non-piping shell furniture: inspection hatch IH Ø500 (curb OD 670) at R1934.4 / az 349.6° on the roof; nameplate NP at az 290° / U 1200; 4 grounding lugs at az 10 / 100 / 190 / 280°; 6 anchor assemblies (shell pad + holding-down strap + 200 × 200 × 10 embedded plate) at az 15 / 75 / 135 / 195 / 255 / 315°.

---

## 4. Reference Values

Everything below is an assumption, not project data. Each is isolated so it can be replaced when the certified drawing is issued.

| Value | Assumed | Basis |
|---|---|---|
| N2.2 = DN300 | DN300 | **User direction, 2026-09-21.** The DWG annotations conflict (two say DN300, one says DN200) and the PDF list says DN200; the modified C-C copy draws Ø324.0, which agrees with DN300. |
| N1.1 projection | 450 mm | The drawn external run continues past R3690 without a dimensioned face. Engineering-standard projection for a DN300 shell nozzle with a reinforcing pad. |
| N9 / N11 / N12 / N13 nozzle lengths | 300 / 50 / 200 / 333 mm | E-E dimensions where given (50, 200, 333); N9's 300 is a standard stub. |
| Roof deck plate thickness | 8 mm | Not dimensioned; consistent with the 6.35 roof plate. |
| Soap launder floor U 5170 | measured wall height 231, rim set on the dimensioned 5400 | The "5400" dimension fixes the rim; the 231 wall height is measured, so the floor follows. ±40 mm. |
| Launder / divider plate thickness 8 mm | 8 mm | Not dimensioned. |
| Outer-cylinder base ring thickness | 12 mm | R1186.34 measured; thickness not dimensioned. |
| Radial rib thickness | 10 mm | Position measured (4 off, 90° apart); thickness not dimensioned. |
| Grounding lug elevation U 300 | U 300 | Plan positions measured in views A and C-C; elevation not dimensioned. |
| Overflow box tangential width 500 | 500 mm | E-E is a section; only the 350 radial dimension is given. |
| Anchor pad / strap dimensions | pad 150 × 250 × 300, strap 20 × 150 | The TANK ANCHORING detail gives "150" and a 5 mm strap; the rest is proportioned to it. The **200 × 200 × 10 anchor plate and the count of 12** come from the DWG FOUNDATION note and are project data, not assumed. |
| IH cover OD 720 | 720 mm | Curb OD 670 and both curb elevations are measured; the cover overhang is not dimensioned. |
| Nozzle catalogue components | `/150lb_Ansi_Flanged/AAZFBB0xx` | User direction: same E3D catalogue as JK-Tank_Build. Every bore needed (DN15/25/80/100/250/300/600) exists in that family, so nothing is downsized or left unbound. |

---

## 5. Verification performed

`tools/verify_203_TA_401.py` parses the emitted macro and asserts properties, not the formulas the builder applied:

* PML1 validation through the shared `wsb.pml_builder.validate_pml` — clean.
* Every primitive has positive dimensions.
* Occupied U range reconstructed from each element's own datum: **0.0 → 8712.7**. The lowest face is exactly the bottom-centre datum, and nothing sits below it.
* Every negative primitive is parsed as a **child** of a solid and proven to fit inside it and to overcut its end faces — a negative emitted at sibling level cuts nothing and would leave the solid looking correct.
* The separation wall's two ends are recomputed from the emitted `RTORUS` and land inside the shell plate band at **R3003.2**, az 52.34 and 157.66; arc length 4831.5 vs the drawn 4830.3.
* The rafter `LOOP` profile is measured back out of the macro at **11.999°** over 2333.3 mm of run, 163.0 deep.
* The single EQUI is anchored at `POS E 0 N 0 U 0` (IR-7).
* Plan envelope R 3706.2, inside the expected 3006…4200.
* Every `NOZZLE` binds `CATR` as its first statement, is positioned before it is oriented, is aimed by `ORI P1 IS`, and has a `HEIG` within 1…2000 mm.
* Every nozzle barrel reaches the shell face without being buried more than 400 mm.
* Shell volume reconciles with the drawing's stated nominal volume (226.2 vs 226 m³).

A plan and two elevations were plotted from the parsed macro and inspected at both revisions. In R1 that caught the separation-wall segments being emitted with local X along the run of the wall instead of across its thickness — it loaded cleanly and drew a fan of ticks. R2 replaces those segments entirely.

### One thing the checks deliberately allow

**N6 sits at U 0**, per the connection list's explicit "ELEVATION 0", so its DN100 flange reaches about U −110. The elevation view draws the drain body down to U −57 and the DWG FOUNDATION note dimensions an *"Embedded notch, 400 × 500 × 200 mm deep"* — the foundation is pocketed for exactly this. Modelled as drawn; flagged rather than silently raised.

---

## 6. Outstanding issues

1. **Not loaded in E3D yet.** Please run the macro and look at it before this is treated as a baseline.
2. **Installation coordinate not issued.** The EQUI is at the origin in drawing orientation. The DWG's equipment-layout plan shows the tank **rotated 180° about U** for site conditions; apply that when setting it out.
3. **The source drawing is PRELIMINARY.** ANDRITZ marks HOLD on every nozzle elevation and direction, on the pressure classes, the flange standard and the insulation. The nozzle elevations used here are the dimensioned ones from the elevation view, which are firmer than the schedule's HOLD cells, but the whole set should be re-checked against the certified issue.
4. **N2.2 size** remains internally inconsistent in the source material; modelled DN300 on your direction.
5. **Not modelled, and why:** the 450-high shell opening at the separation-wall/N1.2 junction and the hatches in the separation wall and the inner cylinder (shown but not fully dimensioned); the manway davit arm; the flat-pattern openings in the two air-separation cylinders (they are cutting patterns, not positioned features); the roof-to-shell SS attachment clips from detail D-D; and the foundation itself (the ±0.200 level, the 400 × 500 × 200 notch and the 12 embedded plates are recorded in `equipment_data.py` and belong to Civil).
6. **Shell is a solid `CYLI`**, which is the E3D convention and what JK-Tank_Build uses — so the internals are inside it. Hide `/203_TA_401_SHELL` to see them, or rebuild with `HOLLOW_SHELL = True` in the build script for a 32-facet plate shell.

---

## 7. Two forms that only a load can settle

Both are isolated behind one constant each, so either is a one-line fix:

1. **`RTORUS` height datum.** The native export's platform/toeboard pair both sit at
   E0 N0, where the datum is unobservable. Centre datum is assumed, matching every
   other primitive family (IR-1). `RTORUS_BASE_IS_CENTRE = False` in the build script
   flips every ring if a load shows them sitting a half-height high.
2. **`RTORUS` attribute order.** The native export writes `POS` before `ORI`, but again
   every one of its RTORUS elements is at E0 N0, where the order cannot be
   distinguished. IR-2's primitive rule is followed instead (ORI first). The separation
   wall's arc centre is 10.5 m off axis, so if this is wrong the wall will be obviously
   rotated about the tank rather than subtly off — it will not pass unnoticed.

---

## 8. Engine gap found (proposed, not applied)

`wsb.pml_builder.PMLBuilder._orient_nozzle` accepts only the six cardinal directions, but a real vessel puts nozzles on arbitrary bearings — this one has eight at 15 / 60 / 150.4 / 270 / 335 / 345°. The build script subclasses it as `BearingPMLBuilder`, which passes an AVEVA direction phrase (`ORI P1 IS E 30 N`) straight through and falls back to the parent for cardinals. `_plan_direction()` already in the engine produces the phrase, and `_check_element_axis_convention` already accepts it.

This is project-scoped on purpose. Promoting it into `wsb/pml_builder.py` would protect every future project, and it belongs there rather than in each job — say the word and I will make that change with a regression test.

---

## 9. Load instruction

Select a writable ZONE in E3D Design, then:

```
$M Projects\203_TA_401_BS_Filtrate_Tank\output\203_TA_401_BS_Filtrate_Tank.pml
```
