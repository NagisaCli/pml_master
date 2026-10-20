# Project log — 203-TA-401 BS Filtrate Tank

One bespoke ANDRITZ vessel, modelled from a PDF general-arrangement drawing plus
an AutoCAD overlay carrying the client's nozzle modifications. Data lives in
`Projects/203_TA_401_BS_Filtrate_Tank/`; this file is the experience.

**State:** R1 generated and numerically verified 2026-09-21. **Not yet loaded in
E3D** — nothing below is VERIFIED in the project's sense.

---

## What made this job different

Every previous tank job took its numbers from an Excel register. This one had
only drawings, and the authoritative content was split across two files that
disagreed with each other. The method that worked is worth keeping.

### 1. A DWG is readable offline, and it is worth reading

The `.dwg` was AC1032 (AutoCAD 2018 format, saved by AutoCAD 2025). LibreDWG is
not installable from the sandbox's package mirrors, but the npm package
**`dwg2dxf-converter`** ships LibreDWG 0.13.4 compiled to WebAssembly and
converted the file in 1.5 s with no system dependencies:

```bash
npx dwg2dxf-converter tank.dwg tank.dxf
```

`ezdxf` then reads the DXF normally. **One trap:** every layer comes out of that
conversion with a negative colour, i.e. switched **off**, so `ezdxf`'s matplotlib
frontend renders a blank page. Turn them on before rendering:

```python
for layer in doc.layers:
    layer.dxf.color = abs(layer.dxf.color)
    layer.on()
```

### 2. Find the view scale, then measure instead of scaling

The overlay author had pasted three **proportionally scaled 1:1 copies** of the
plan views beside the original sheet. In those copies one drawing unit is one
millimetre, so `R = 3006.35` is literally the shell outside radius.

The original sheet is also measurable: its 1:30 elevation came out at exactly
1 unit = 1 mm, and its 1:50 plans at 1 unit = 1.6676 mm. Calibrate once against
two dimension *texts* whose values you can read (`7375` and `1200` on the
elevation datum line gave 0.094502 pt per unit), and everything else follows.

Measuring beats scaling by an order of magnitude. Wall thickness came out
6.35 mm (= ¼″) on the shell, both air-separation cylinders and the separation
wall — a number no one would have got off a raster.

### 3. Derive the modification deltas, do not trust the words alone

The annotations said "Rotated 15°", "Rotated 30°", "Rotated 180°" without a
direction. Clustering the shell-mounted features by azimuth in the *original*
views and again in the *modified* copies gave the signed deltas directly:
−15° for N6 and N9, −30° for N2.2, −5° for N1.2, 180° for N2.1 and N5. All
counter-clockwise. Two independent measurements, and the stated magnitudes
matched, so the direction is evidence rather than a guess.

### 4. Cross-checks that actually caught things

* **Volume.** π/4 × 6.0² × 8.0 = 226.2 m³ against the drawing's stated 226 m³.
  That reconciles ID and height in one line.
* **Foreshortened rafters.** The roof rafters at 45° in plan project at 16.71°
  in the elevation, and `atan(tan 12° / cos 45°) = 16.73°`. That confirmed the
  12° roof slope *and* the 8-rafter count from a number nobody dimensioned.
* **Neck diameters.** Measuring the parallel walls of each drawn nozzle gave
  273.2 (DN250), 324.0 (DN300), 220.6 flange (DN100). That is how the DN300 /
  DN200 conflict on N2.2 was resolved in favour of the modified geometry.

### 5. The drawn geometry and the connection list disagree — say so

The issued ANDRITZ schedule lists N2.1 as DN300 and N2.2 as DN200. The issued
sheet *draws* them at Ø273 (DN250) and Ø168 (DN150). The modification notes call
them DN250 and DN300. On a sheet stamped PRELIMINARY with HOLD in every
elevation and direction cell, the schedule is the weakest of the three. Model
what the client's own modification says, and put the conflict in Outstanding
Issues rather than picking silently.

---

## A real fault the plot caught, and the check that missed it

The curved separation wall is emitted as 32 `BOX` segments following a measured
plan path. The first version passed `plan_rotation_deg = bearing(segment_az)`,
which aims the BOX's local **X** along the run of the wall — so `XLEN`
(the 6.35 plate thickness) ran *along* the wall and `YLEN` (the segment length)
ran *across* it. The macro loaded, every numeric check passed, and the model
drew a fan of ticks perpendicular to the wall line instead of a wall.

`BOX` takes `XLEN` along local X, so for a plate the local X must be the plate
**normal**: `plan_rotation_deg = bearing(segment_az + 90)`.

The lesson is about verification, not about BOX. The numeric pass asserted
extents, datums and bounds — all of which a 90°-rotated plate satisfies. What
found it was plotting the parsed macro in plan and elevation and looking at it.
**For any model with arrayed or rotated hardware, plot it. Extents cannot see
orientation.**

---

## Engine gap: nozzles on non-cardinal bearings

`PMLBuilder._orient_nozzle` accepts only `U D E W N S`. A real vessel does not
oblige: this one needed 15 / 60 / 150.4 / 335 / 345°. The job used a local
subclass that passes an AVEVA direction phrase through:

```python
class BearingPMLBuilder(PMLBuilder):
    def _orient_nozzle(self, axis):
        text = str(axis).strip()
        if " " in text:
            self._lines.append(f"ORI P1 IS {text}")
            return
        super()._orient_nozzle(text)
```

Everything needed is already in the engine: `_plan_direction()` builds the
phrase, and `_check_element_axis_convention` accepts `ORI P<n> IS <anything>`.
Promoting this into `wsb/pml_builder.py` (with a regression test on a skew
bearing) would remove the need for every future vessel to re-invent it. **Left
unapplied pending the user's word — a shared-engine change is not a unilateral
call.**

---

## Open

* E3D visual acceptance of R1.
* Installation coordinate and the plant bearing of the tank's 0° mark. The
  overlay's equipment-layout plan shows the tank rotated 180° about U on site;
  the model is built in drawing orientation.
* Whether `NCYLINDER` (present in this account's own native export
  `Projects/205_TA_059_BLEACH_PLANT_SCRUBBER.pml`) should be promoted from
  NATIVE-OBSERVED, which would let open cylinders be bored out instead of
  arrayed from 20–32 `BOX` facets.
