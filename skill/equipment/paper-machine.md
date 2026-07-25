# Paper Machine (Fourdrinier)

A long assembly of rolls in sequence. Reference figures below assume a 4800 mm
trim machine — **RECOMMENDED** typical practice for sanity-checking and defaults,
not vendor data. Project data always wins.

---

## Coordinate convention

- **E** = machine direction (MD); headbox at E = 0, reel at positive E
- **N** = cross-machine direction (CD); machine centreline at N = 0
- **U** = vertical; ground floor at U = 0

Nearly every roll is a `CYLI` with its axis cross-machine: `ORI Z IS N AND Y IS U`
(IR-3). Face width scales with trim, so define trim once and derive from it.

---

## Section layout along E

| Section | E range (mm) | Key equipment |
|---------|--------------|---------------|
| Headbox | −1500 → 0 | Tapered inlet header, turbulence generator, slice lip |
| Wire (Fourdrinier) | 0 → 18000 | Breast roll, forming board, table rolls, foils, dandy roll, suction boxes, couch roll |
| Press | 19000 → 28000 | 3–4 nips, felt rolls, Uhle boxes, press frames |
| Dryer | 26000 → 62000 | 40–60 cylinders in 2 tiers, fabric rolls, steam joints, hood |
| Size press | 62000 → 63500 | Roll pair, starch supply |
| After-dryer | 63500 → 65000 | 4–8 cylinders |
| Calender | 65000 → 66000 | 4–8 rolls, vertical stack |
| Reel | 66000 → 68000 | Reel drum, spools, rider roll |

Total machine length is typically 50–120 m (~70 m for this reference).

---

## Key dimensions

| Component | Typical range | Reference value |
|-----------|---------------|-----------------|
| Trim width | 2400–5000 mm | 4800 mm |
| Wire width | trim + 300–500 mm | 5200 mm |
| Breast roll | φ600–900 mm | φ800 |
| Table roll | φ250–400 mm | φ320 |
| Couch roll | φ800–1200 mm | φ1000 |
| Press roll | φ800–1400 mm | φ900–1300 |
| **Dryer cylinder** | **φ1500–2200 mm** | **φ1800** (most common) |
| Dryer face width | trim + 200–300 mm | 5000–5400 mm |
| Dryer pitch | 2000–2500 mm | **2400 mm** |
| Calender roll | φ600–900 mm | φ800 |
| Reel drum | φ900–1200 mm | φ1100 |

---

## Dryer section — two-tier arrangement

The most repetitive and highest-primitive-count part of any machine model. With
φ1800, pitch 2400, face 5400:

- **Top row**: shaft centre at U = 6000, cylinders at E = 26000 + i·2400
- **Bottom row**: shaft centre at U = 3800, same E positions
- Rows **interleave** in plan view — the sheet runs alternately over top and
  bottom cylinders
- Steam joints at both ends: N = ±(face/2 + 150)

Generate rows in a loop, never by hand. Getting the interleave or the pitch wrong
is immediately visible to anyone who knows the machine.

---

## Press nips

A nip is a roll pair in vertical contact. The top roll centre sits at:

```
U_top = U_bottom + (D_bottom + D_top) / 2
```

Because `POS` is the geometric centre (IR-1), this places the two shells exactly
tangent. Getting it wrong leaves a visible gap or an overlap at the nip.

| Nip | Bottom roll | Top roll |
|-----|-------------|----------|
| 1st press | φ900–1000 | φ800–900 |
| 2nd press | φ1000–1200 | φ900–1000 |
| 3rd press | φ1200–1400 | φ1000–1200 |

---

## Headbox

| Component | Reference dimensions | Primitive |
|-----------|---------------------|-----------|
| Tapered inlet header | DTOP 200, DBOT 700, L 5500 | `CONE`, axis N |
| Main chamber | 500 E × 5400 N × 700 U | `BOX` |
| Slice lip | 300 E × 5200 N × 80 U | `BOX` |
| Stands (×2) | 600 × 600 × 2000 | `BOX` |

The tapered header is what makes a headbox recognisable — it distributes stock
evenly across the machine width, so it tapers along N.

---

## Typical elevations

| Feature | U (mm) |
|---------|--------|
| Foundation slab | −300 to −600 |
| Wire section | 3500 |
| Press section base | 2700 |
| Dryer shaft, bottom row | 3800 |
| Dryer shaft, top row | 6000 |
| Operating platform | 4500 |
| Crane rail | 16500–18000 |

The machine sits on a continuous reinforced concrete foundation: length = machine
length + 3000 mm each end, width = frame width + 4000 mm, thickness 600–1000 mm.

---

## Modeling note

`examples/paper_machine_model.py` generates a full machine and is useful as a
worked reference for the loop structure. Note that the `examples/` scripts use a
**flat hierarchy** (one EQUI, area-level SUBEs) to demonstrate geometry at scale.
That is not the equipment hierarchy convention — real equipment follows IR-8: one
EQUI per tag, one SUBE per nozzle.
