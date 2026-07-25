# Utilities, Piping & Structures

Supporting infrastructure: pipe bridges, buildings, platforms, utility equipment.
**RECOMMENDED** typical practice unless marked otherwise.

---

## Piping in macro mode — VERIFIED constraint

In PML1 `$M` macro mode, pipes **cannot** be routed with branch/pipe commands.
Model pipe runs as `CYLI` primitives at their elevation:

```pml
NEW CYLI
DIAM 508.0          -- pipe OD, not DN
HEIG 80000.0        -- run length
ORI Z IS E AND Y IS U
POS E 25000.0 N -1500.0 U 4850.0
```

Remember `POS` is the **midpoint** of the run (IR-1), not its start.

| Component | Primitive | Approach |
|-----------|-----------|----------|
| Straight run | `CYLI` | axis E or N, DIAM = OD, HEIG = length |
| Flange pair | `CYLI` ×2 | DIAM = OD + 180, HEIG = 70 |
| Gate/globe valve | `BOX` | XLEN = OD+120, YLEN = OD+220, ZLEN = OD+320 |
| Valve handwheel | `CYLI` | axis U |
| Pipe support shoe | `BOX` | small box beneath the pipe at intervals |

This is a **representation**, not a piping model. It is for visualisation and
clash checking. Real piping is routed in E3D's piping application, which is why
equipment nozzles get their own SUBEs (IR-8).

---

## Pipe sizes by service

DN and outside diameter — use OD for `DIAM`:

| Service | DN | OD (mm) | Material |
|---------|-----|---------|----------|
| Thick stock (3–12%) | 200–400 | 219.1–406.4 | SS 316L |
| Thin stock (0.5–2%) | 400–800 | 406.4–812.8 | SS 316L |
| White water | 600–1000 | 609.6–1016.0 | SS 304 |
| HP steam | 200–500 | 219.1–508.0 | CS A106 Gr.B |
| MP steam | 300–600 | 323.9–609.6 | CS A106 Gr.B |
| LP steam | 400–800 | 406.4–812.8 | CS A53 Gr.B |
| Condensate | 100–300 | 114.3–323.9 | CS |
| Black liquor (weak) | 250–500 | 273.0–508.0 | SS 304L |
| Black liquor (heavy) | 150–350 | 168.3–355.6 | SS 304L / Duplex |
| Green liquor | 200–350 | 219.1–355.6 | SS 304L |
| White liquor | 150–350 | 168.3–355.6 | SS 304L |
| ClO₂ solution | 80–150 | 88.9–168.3 | Titanium / FRP |
| Compressed air | 80–250 | 88.9–273.0 | CS / galvanised |
| Cooling water | 200–600 | 219.1–609.6 | CS / HDPE |

Stock lines are large for their flow because pulp runs at low velocity to avoid
flocculation — a DN600 stock line is normal, not an error.

---

## Pipe bridges

- Column spacing: 4000–6000 mm (typically 5000)
- Column section: 600 × 600 mm in model
- Tier beam: 600 wide × 400 deep
- Tiers: 3–4; vertical spacing 3000 mm
- Column pairs at N ±2500 from bridge centreline
- Minimum headroom underneath: 2500 mm

Arrangement on the racks:

- Heavy/large pipes on the **lower** tiers (load path)
- Hot steam lines on **upper** tiers, with expansion loops
- Chemical lines separated from steam to avoid overheating

---

## Buildings & structures

| Element | Dimensions |
|---------|------------|
| Building column | 600–800 mm square, 18000 mm high |
| Column spacing | 5000–8000 mm along MD |
| Bay width | 24000 mm (columns at N ±12000) |
| Crane girder | ~1400 W × 1800 H, twin box |
| Crane rail top | 16500–18000 mm |
| Operating floor | U = 4500 mm |
| Grating | 50 mm thick (`BOX` ZLEN 50) |
| Handrail top rail | platform + 1100 mm |
| Handrail mid rail | platform + 550 mm |
| Handrail post | φ40 mm at 2000 mm spacing |

---

## Access & safety minimums

These are safety requirements, not preferences — a model that violates them
describes a plant that cannot be built:

- Walkway width: **800 mm** minimum (1000–1200 mm preferred)
- Platform/stair width: **1000 mm** minimum
- Clearance between major equipment: **1200 mm**
- Headroom under bridges: **2500 mm**

---

## Utility equipment

| Equipment | Typical size | Structure |
|-----------|--------------|-----------|
| CFB power boiler | 15 × 10 × 28 m | `BOX` furnace + `CYLI` drum + `CYLI` cyclone |
| Turbo-generator | φ2.8 m × 6 m | `CYLI` turbine + `BOX` generator |
| Deaerator | φ2.8 m × 12 m | horizontal `CYLI` + vertical `CYLI` tower |
| White water silo | φ6 m × 15 m | `CYLI` + `CONE` bottom |
| Clarifier | φ16 m × 4 m | `CYLI` tank + `BOX` scraper bridge |
| Cooling tower | 12 × 12 × 15 m | `BOX` structure + `CYLI` fans |

---

## Plant layout

| Area | Footprint (m) |
|------|---------------|
| Woodyard & chip prep | 200 × 80 |
| Fibreline | 80 × 50 |
| Chemical recovery | 100 × 70 |
| Paper machine hall | 120 × 40 |
| Finishing & warehouse | 80 × 60 |
| Power plant | 60 × 40 |
| Water treatment | 80 × 60 |

Vertical zoning: basement −4500, ground 0, mezzanine 4500, bridge tiers
7500–11500, roof 18000.
