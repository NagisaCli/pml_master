# Fibreline & Recovery Equipment

Pulping, washing, screening, bleaching, and chemical recovery. Sizes are
typical-practice envelopes for sanity-checking and reasoned defaults —
**RECOMMENDED**, not verified against a specific vendor datasheet. Project data
always wins.

Tank-type items in this area are configured per
[tanks-and-vessels.md](tanks-and-vessels.md).

---

## Process order

Understanding the sequence lets you infer what a piece of equipment connects to,
which drives nozzle placement and elevation:

```
chips → digester → blow tank → brown stock washing → O2 delignification
      → washing → bleaching (D0 - EOP - D1) → storage → stock prep → paper machine

black liquor → evaporators → recovery boiler → dissolving tank → green liquor
             → causticizing → white liquor → back to digester
             lime mud → lime kiln → CaO → back to causticizing
```

---

## Pulping

| Equipment | Typical size | Structure |
|-----------|--------------|-----------|
| Continuous digester | φ5.5–8.0 m × 45–65 m | `CYLI` shell + `DISH` top + `CONE` bottom; nozzle rings at many elevations |
| Blow tank | φ8.5 m × 15 m | `CYLI` + `CONE` bottom; large vapour relief to cyclone |
| Vacuum drum washer | φ4.0 m × 7.5 m drum | `CYLI` drum (horizontal) + `BOX` vat |
| Bleach tower | φ4.2–4.8 m × 28–32 m | `CYLI` + closure per duty; upflow |

The digester is the tallest item in a fibreline and usually the vertical
reference for surrounding structures. Nozzle rings occur at many elevations
because circulation and extraction are drawn off at several heights.

### Batch-cooking auxiliaries

**VERIFIED process functions; project-specific geometry remains a Reference
Value.**

| Equipment | Process function | Geometry implication |
|-----------|------------------|----------------------|
| Liquor accumulator | Balances liquor flows between batch-cooking stages | Vertical vessel; pressure-service closures and support must be confirmed from the vendor GA |
| Junk trap | Removes sand and other heavy debris from chip-chute circulation | Compact vertical vessel with a lower reject hopper and several circulation/flush connections |
| Blow tank | Receives the digester blow; flash vapour continues to blow-heat recovery | Large upper vapour space, stock connections and a low-point discharge |

> **User-corrected 2026-07-30 (JK_Cooking_Tank_Build).** The two cooking-area
> Blow Tanks contain ground-mounted, vertical bottom-entry agitators. The motor
> and gearbox sit centrally below the cone; the shaft rises through the bottom
> opening into horizontal impeller stages. The previous side-entry
> interpretation was wrong. Do not generalise this exact arrangement or its
> dimensions to every blow tank; those remain project/vendor data.

Sources:

- Valmet application report `2611_01_01EN` states that batch cooking uses liquor
  accumulators to balance flows between stages and that the digester/circulation
  system is pressure service:
  <https://www.valmet.com/globalassets/sharepoint/imported/2611_01_01en.pdf>
- Valmet lists junk traps as an application for automatic removal of sand and
  fine debris from chip-chute circulation:
  <https://www.valmet.com/flowcontrol/valves/application-specific-products/>
- Valmet's methanol white paper traces flash vapour from the blow tank into blow
  heat recovery:
  <https://www.valmet.com/globalassets/media/downloads/white-papers/power-and-recovery/methanol_waste_to_fuel_whitepaper.pdf>

These sources establish **function**, not a universal vessel height, nozzle size
or support dimension. Values inferred from the function stay labelled Reference
Values until a project or vendor drawing supplies them.

---

## Screening & cleaning

| Equipment | Typical size | Structure |
|-----------|--------------|-----------|
| Pressure screen | φ0.8–1.6 m × 2.0–2.8 m | `CYLI` body + `DISH` top + `CYLI` top motor + `BOX` reject chamber |
| Centrifugal cleaner | φ200–350 mm × 1.4–1.8 m | `CONE` body + `CYLI` inlet/outlet; banks of 4–20 |
| Disc thickener | φ3.5–5.0 m discs, 10–24 off | `CYLI` discs + `BOX` tank + `BOX` hood |

A pressure screen is recognisable by its **top-mounted motor** on a slim vertical
body. Cleaners are always in banks, never alone — model the bank and its headers.

---

## Stock preparation

| Equipment | Typical size | Structure |
|-----------|--------------|-----------|
| Hydrapulper | φ3.0–5.5 m × 3.0–5.0 m | `CYLI` tank + `CONE` bottom + `BOX` motor + `CYLI` shaft |
| Double disc refiner | φ1.0–1.4 m discs | `CYLI` discs + `BOX` housing + `BOX` motor + `BOX` baseplate |
| Stock chest | φ4–8 m × 5–10 m, 50–500 m³ | `CYLI` + `CONE` bottom if present + agitator |

Refiners are floor-mounted with a large motor alongside on a common baseplate;
the motor is often as large as the refiner itself and must not be omitted.

---

## Chemical recovery

| Equipment | Typical size | Structure |
|-----------|--------------|-----------|
| Falling-film evaporator | φ2.8–4.0 m × 12–16 m | `CYLI` heating chamber + `CYLI` separator + ducts; 5–7 effects in series |
| Recovery boiler | 12–17 × 10–15 × 35–45 m | `BOX` furnace + `CYLI` steam drum + `CYLI` stack |
| Rotary lime kiln | φ3.5–4.5 m × 75–120 m | `CYLI` shell on a slight slope + `CYLI` support rings + `BOX` pedestals |
| Causticizing tank | φ5 m × 6 m | `CYLI` + agitator |
| White liquor clarifier | φ14 m × 8 m | `CYLI` tank + `BOX` scraper bridge |

The lime kiln is the longest item in a mill and slopes 2–4% from feed to
discharge; it rests on 3–5 support rings ("tires"), each on a pedestal. Model the
rings — they are what makes it recognisable as a kiln rather than a pipe.

Evaporators come as a train of near-identical bodies; model the set, not one.

---

## Confidence note

These envelopes reflect general industry practice for kraft mills and are useful
for sanity-checking a stated dimension or filling a gap. They are **not**
substitutes for vendor data. Any value taken from this file into a model is a
Reference Value and must be reported as one, with the basis stated.

Where a figure here is contradicted by project data or a user correction, the
project data wins and this file should be updated per
[capturing-feedback.md](../workflows/capturing-feedback.md).
