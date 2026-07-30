# JK Cooking Plant E3D Equipment — Engineering Deliverable

**Project folder:** `Projects/JK_Cooking_Tank_Build`  
**Generated:** 2026-07-30 03:18  
**Datum:** equipment bottom centre / foundation bearing plane  
**Coordinates:** global E3D East, North, Up; millimetres

## Outcome

- Independent equipment macros: **15**
- Convenience combined macro: **1**
- E3D primitives: **1801**
- Nozzle/manway assemblies: **80**
- Catalogue-backed native NOZZLE placeholders: **80**
- Plan-oriented support/detail BOX elements: **458**
- Explicit Reference Values: **49**
- Numerical verification: **passed for all equipment**

Every emitted primitive was parsed back using its PML element-specific datum (centre for CYLI/CONE/BOX; rim for DISH) and reconciled with the resolved local geometry. All 15 models touch their listed bottom-centre elevation, no primitive falls below the foundation datum, and no model exceeds its declared overall height.

## Deliverables and loading

Select a writable **ZONE** in AVEVA E3D Design, then load either an individual macro or the combined macro:

```text
$M <full path to the .pml file>
```

Output folder: `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Cooking_Tank_Build\output`

Combined macro: `C:\Users\A\Desktop\Projects\e3d_agent\Projects\JK_Cooking_Tank_Build\output\JK_Cooking_Tank_Build.pml`

## Completed equipment

| # | Equipment | Bottom centre E, N, U (mm) | Main dimensions | Overall height | Capacity | Primitives | Nozzle groups |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | BLEACH HOT WATER TANK | 18720, -6004, -300 | OD 5020 mm; capacity cylinder 5052.5 mm; roof rise 753.0 mm | 5805.5 mm | 100 m3 | 115 | 5 |
| 2 | BLOW TANK-1 | 27276, 6034, -300 | TOP→BOTTOM: CY D3876 H2508; CONE 3876→7300 H2944; CY D7300 H8753; CONE 7300→555 H5898; bottom opening 1848 above grade | 21951.0 mm | 380 m3 | 215 | 6 |
| 3 | BLOW TANK-2 | 27498, 18002, -300 | TOP→BOTTOM: CY D3876 H2508; CONE 3876→7300 H2944; CY D7300 H8753; CONE 7300→555 H5898; bottom opening 1848 above grade | 21951.0 mm | 380 m3 | 215 | 6 |
| 4 | WARM WATER TANK | 35894, -5970, -300 | OD 5700 mm; capacity cylinder 5682.4 mm; roof rise 855.0 mm | 6537.4 mm | 145 m3 | 117 | 5 |
| 5 | BROWN HOT WATER TANK | 44004, -6002, -300 | OD 5714 mm; capacity cylinder 5654.5 mm; roof rise 857.1 mm | 6511.6 mm | 145 m3 | 117 | 5 |
| 6 | JUNK TRAP-1 | 33635, 8034, -300 | OD 1770 mm; shell 1800 mm; hopper 550 mm | 2942.5 mm | — | 114 | 5 |
| 7 | JUNK TRAP-2 | 33635, 15965, -300 | OD 1770 mm; shell 1800 mm; hopper 550 mm | 2942.5 mm | — | 114 | 5 |
| 8 | ACCUMULATOR TANK | 44001, 12002, -300 | OD 7023 mm; shell 12907.3 mm; skirt 1800 mm | 16463.0 mm | 500 m3 | 178 | 6 |
| 9 | ACCUMULATOR TANK AID-1 | 38433, 10002, -300 | OD 2022 mm; shell 4044.0 mm; skirt 800 mm | 5349.5 mm | — | 68 | 6 |
| 10 | ACCUMULATOR TANK AID-2 | 38433, 14002, -300 | OD 2022 mm; shell 4044.0 mm; skirt 800 mm | 5349.5 mm | — | 68 | 6 |
| 11 | W-L SERVICE TANK-1 | 44006, 20002, -300 | OD 5000 mm; capacity cylinder 5093.0 mm; roof rise 750.0 mm | 5843.0 mm | 100 m3 | 115 | 5 |
| 12 | W-L SERVICE TANK-2 | 44004, 27801, -300 | OD 5000 mm; capacity cylinder 5093.0 mm; roof rise 750.0 mm | 5843.0 mm | 100 m3 | 115 | 5 |
| 13 | MAIN CONDENSATE TANK | 28497, 27796, -300 | Horizontal envelope 3400 × 2017 mm; straight barrel 2391.5 mm | 2717.0 mm | 8 m3 | 44 | 5 |
| 14 | SPENT LIQUOR TANK | 32502, 27803, -300 | OD 3000 mm; capacity cylinder 1414.7 mm; roof rise 450.0 mm | 1864.7 mm | 10 m3 | 91 | 5 |
| 15 | B-L TANK | 37501, 27801, -300 | OD 5020 mm; capacity cylinder 5052.5 mm; roof rise 753.0 mm | 5805.5 mm | 100 m3 | 115 | 5 |

## Height and geometry calculations

Where the workbook says `CALCULATE BY DIAMETER AND CAPACITY`, the capacity cylinder is calculated from `H = V / (πD²/4)`. A conical roof is then added above that cylinder; its rise is an explicit Reference Value, not hidden inside the capacity calculation.

### BLEACH HOT WATER TANK

- **Diameter:** 5020 mm  
  Source/basis: Tank_list.xlsx
- **Capacity:** 100 m3  
  Source/basis: Tank_list.xlsx
- **Capacity-cylinder height:** 5052.5 mm  
  Source/basis: Derived: V / (pi D^2 / 4)
- **Overall height:** 5805.5 mm  
  Source/basis: Derived cylinder height + Reference Value roof rise
- The listed capacity is matched by the cylindrical section alone; the roof is additional geometric free volume.
- Access and fastener details are isolated from the authoritative body envelope and can be replaced without changing tank data.

### BLOW TANK-1

- **User-corrected profile:** CY 3876×2508; CONE 3876→7300×2944; CY 7300×8753; CONE 7300→555×5898  
  Source/basis: User correction 2026-07-30; final-cone H2636 in Tank_list.xlsx was erroneous
- **Profile and installed height:** 20103 mm body; 1848 mm bottom clearance; 21951 mm grade-to-top  
  Source/basis: User-corrected segment and clearance chain
- **Global top elevation:** U 21651 mm  
  Source/basis: Installation ground U -300 + 21951 mm grade-to-top
- **Support height:** 7746 mm  
  Source/basis: Derived from ground to the DN7300 cone/shell junction
- **Overall height:** 21951 mm  
  Source/basis: 1848 mm bottom clearance plus 20103 mm corrected profile
- **Listed capacity:** 380 m3  
  Source/basis: Tank_list.xlsx
- **Profile gross volume:** 559.4 m3  
  Source/basis: Derived from cylinder/frustum volumes
- Profile gross volume is 559.4 m3 versus the listed 380 m3 capacity (67.9% of the gross profile).
- The top-to-bottom sequence is preserved exactly; PML positions are computed from the 1848 mm cone-bottom clearance without changing the other three supplied segment dimensions.
- The corrected exact chain gives 21951 mm grade-to-top and global U=21651, consistent with the user's approximate 21 m overall-height direction.

### BLOW TANK-2

- **User-corrected profile:** CY 3876×2508; CONE 3876→7300×2944; CY 7300×8753; CONE 7300→555×5898  
  Source/basis: User correction 2026-07-30; final-cone H2636 in Tank_list.xlsx was erroneous
- **Profile and installed height:** 20103 mm body; 1848 mm bottom clearance; 21951 mm grade-to-top  
  Source/basis: User-corrected segment and clearance chain
- **Global top elevation:** U 21651 mm  
  Source/basis: Installation ground U -300 + 21951 mm grade-to-top
- **Support height:** 7746 mm  
  Source/basis: Derived from ground to the DN7300 cone/shell junction
- **Overall height:** 21951 mm  
  Source/basis: 1848 mm bottom clearance plus 20103 mm corrected profile
- **Listed capacity:** 380 m3  
  Source/basis: Tank_list.xlsx
- **Profile gross volume:** 559.4 m3  
  Source/basis: Derived from cylinder/frustum volumes
- Profile gross volume is 559.4 m3 versus the listed 380 m3 capacity (67.9% of the gross profile).
- The top-to-bottom sequence is preserved exactly; PML positions are computed from the 1848 mm cone-bottom clearance without changing the other three supplied segment dimensions.
- The corrected exact chain gives 21951 mm grade-to-top and global U=21651, consistent with the user's approximate 21 m overall-height direction.

### WARM WATER TANK

- **Diameter:** 5700 mm  
  Source/basis: Tank_list.xlsx
- **Capacity:** 145 m3  
  Source/basis: Tank_list.xlsx
- **Capacity-cylinder height:** 5682.4 mm  
  Source/basis: Derived: V / (pi D^2 / 4)
- **Overall height:** 6537.4 mm  
  Source/basis: Derived cylinder height + Reference Value roof rise
- The listed capacity is matched by the cylindrical section alone; the roof is additional geometric free volume.
- Access and fastener details are isolated from the authoritative body envelope and can be replaced without changing tank data.

### BROWN HOT WATER TANK

- **Diameter:** 5714 mm  
  Source/basis: Tank_list.xlsx
- **Capacity:** 145 m3  
  Source/basis: Tank_list.xlsx
- **Capacity-cylinder height:** 5654.5 mm  
  Source/basis: Derived: V / (pi D^2 / 4)
- **Overall height:** 6511.6 mm  
  Source/basis: Derived cylinder height + Reference Value roof rise
- The listed capacity is matched by the cylindrical section alone; the roof is additional geometric free volume.
- Access and fastener details are isolated from the authoritative body envelope and can be replaced without changing tank data.

### JUNK TRAP-1

- **Diameter:** 1770 mm  
  Source/basis: Tank_list.xlsx
- **Overall height:** 2942.5 mm  
  Source/basis: Reference configuration: hopper + shell + dished head
- Diagonal plan connections are represented on the nearest verified cardinal E3D axis; exact skew bearings require a vendor GA or a verified arbitrary-vector PML orientation form.

### JUNK TRAP-2

- **Diameter:** 1770 mm  
  Source/basis: Tank_list.xlsx
- **Overall height:** 2942.5 mm  
  Source/basis: Reference configuration: hopper + shell + dished head
- Diagonal plan connections are represented on the nearest verified cardinal E3D axis; exact skew bearings require a vendor GA or a verified arbitrary-vector PML orientation form.

### ACCUMULATOR TANK

- **Diameter:** 7023 mm  
  Source/basis: Tank_list.xlsx
- **Capacity:** 500 m3  
  Source/basis: Tank_list.xlsx
- **Shell height:** 12907.3 mm  
  Source/basis: Derived: V / (pi D^2 / 4)
- **Overall height:** 16463.0 mm  
  Source/basis: Skirt + shell + top head
- The outer platform/ring visible in plan is not modelled because no side elevation or steel dimensions were supplied.
- Top and bottom DISH elements use their rim/tangent-plane POS; the top head is numerically seated on the shell without changing the supplied diameter, capacity or derived height.

### ACCUMULATOR TANK AID-1

- **Diameter:** 2022 mm  
  Source/basis: Tank_list.xlsx
- **Shell height:** 4044.0 mm  
  Source/basis: Reference Value from equipment aspect ratio
- **Overall height:** 5349.5 mm  
  Source/basis: Skirt + shell + top head
- The outer platform/ring visible in plan is not modelled because no side elevation or steel dimensions were supplied.
- Top and bottom DISH elements use their rim/tangent-plane POS; the top head is numerically seated on the shell without changing the supplied diameter, capacity or derived height.

### ACCUMULATOR TANK AID-2

- **Diameter:** 2022 mm  
  Source/basis: Tank_list.xlsx
- **Shell height:** 4044.0 mm  
  Source/basis: Reference Value from equipment aspect ratio
- **Overall height:** 5349.5 mm  
  Source/basis: Skirt + shell + top head
- The outer platform/ring visible in plan is not modelled because no side elevation or steel dimensions were supplied.
- Top and bottom DISH elements use their rim/tangent-plane POS; the top head is numerically seated on the shell without changing the supplied diameter, capacity or derived height.

### W-L SERVICE TANK-1

- **Diameter:** 5000 mm  
  Source/basis: Tank_list.xlsx
- **Capacity:** 100 m3  
  Source/basis: Tank_list.xlsx
- **Capacity-cylinder height:** 5093.0 mm  
  Source/basis: Derived: V / (pi D^2 / 4)
- **Overall height:** 5843.0 mm  
  Source/basis: Derived cylinder height + Reference Value roof rise
- The listed capacity is matched by the cylindrical section alone; the roof is additional geometric free volume.
- Access and fastener details are isolated from the authoritative body envelope and can be replaced without changing tank data.

### W-L SERVICE TANK-2

- **Diameter:** 5000 mm  
  Source/basis: Tank_list.xlsx
- **Capacity:** 100 m3  
  Source/basis: Tank_list.xlsx
- **Capacity-cylinder height:** 5093.0 mm  
  Source/basis: Derived: V / (pi D^2 / 4)
- **Overall height:** 5843.0 mm  
  Source/basis: Derived cylinder height + Reference Value roof rise
- The listed capacity is matched by the cylindrical section alone; the roof is additional geometric free volume.
- Access and fastener details are isolated from the authoritative body envelope and can be replaced without changing tank data.

### MAIN CONDENSATE TANK

- **Plan envelope:** 3400 × 2017 mm  
  Source/basis: Tank_list.xlsx text and Refs/MAIN CONDENSATE TANK.png
- **Listed capacity:** 8 m3  
  Source/basis: Tank_list.xlsx
- **Calculated gross vessel volume:** 9.79 m3  
  Source/basis: Cylinder + two 2:1 ellipsoidal-head envelopes
- **Overall model height:** 2717.0 mm  
  Source/basis: 500 mm saddles + OD + 200 mm contained vent projection
- The 8 m3 listed capacity is 81.7% of the 9.79 m3 calculated gross vessel envelope.
- The long axis is placed North-South to match the supplied plan-view orientation.

### SPENT LIQUOR TANK

- **Diameter:** 3000 mm  
  Source/basis: Tank_list.xlsx
- **Capacity:** 10 m3  
  Source/basis: Tank_list.xlsx
- **Capacity-cylinder height:** 1414.7 mm  
  Source/basis: Derived: V / (pi D^2 / 4)
- **Overall height:** 1864.7 mm  
  Source/basis: Derived cylinder height + Reference Value roof rise
- The listed capacity is matched by the cylindrical section alone; the roof is additional geometric free volume.
- Access and fastener details are isolated from the authoritative body envelope and can be replaced without changing tank data.
- The very low capacity-to-diameter ratio produces a shallow vessel; this follows the supplied 3000 mm diameter and 10 m3 capacity without increasing either value.

### B-L TANK

- **Diameter:** 5020 mm  
  Source/basis: Tank_list.xlsx
- **Capacity:** 100 m3  
  Source/basis: Tank_list.xlsx
- **Capacity-cylinder height:** 5052.5 mm  
  Source/basis: Derived: V / (pi D^2 / 4)
- **Overall height:** 5805.5 mm  
  Source/basis: Derived cylinder height + Reference Value roof rise
- The listed capacity is matched by the cylindrical section alone; the roof is additional geometric free volume.
- Access and fastener details are isolated from the authoritative body envelope and can be replaced without changing tank data.

## Reference Values

These values are assumptions pending project/vendor confirmation. They do not override workbook dimensions or the authoritative Blow Tank profile strings.

| Equipment | Parameter | Value | Basis |
|---|---|---|---|
| BLEACH HOT WATER TANK | Roof rise | 753.0 mm (0.15 D) | skill/equipment/tanks-and-vessels.md, conical-roof default |
| BLEACH HOT WATER TANK | Nozzle/manway schedule | N1 DN250 hot-water feed; N2 DN300 pump suction; N3 DN200 overflow; N4 DN150 high-point vent; M1 DN600 shell access manway | Minimum process-logical atmospheric-tank connections; bearings reconciled with the supplied top view |
| BLEACH HOT WATER TANK | Detailed hardware | 12 connected anchor chairs; W fixed ladder with base shoes at 350 mm rung pitch; four lifting lugs; nameplate, grounding lug; individual flange geometry supplied by native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; dimensions are replaceable reference geometry pending vendor GA |
| BLOW TANK-1 | Support legs | 4 × 250 mm square, 7746 mm high | User-corrected side-view arrangement: legs extend from grade to the cone/shell junction; section size remains replaceable |
| BLOW TANK-1 | Nozzle schedule | N1 DN400 upper tangential blow-line inlet; N2 DN400 upper circulation connection; N3 DN600 large vapour / stock connection; N4 DN300 dilution / recirculation connection; M1 DN600 shell access manway; N5 DN500 native placeholder at the 555 mm bottom opening / agitator mounting | Visible top/side connections plus minimum blow-tank process connections; sizes/elevations pending vendor GA |
| BLOW TANK-1 | Detailed hardware | Four anchors, grout/cleats and top gussets per support foot; W ladder stops at the supported DN7300 shell top and has base shoes; lifting lugs, nameplate and grounding lug; native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; all additions are outside the authoritative four-segment body profile |
| BLOW TANK-1 | Internal agitator | Ground-mounted central drive; vertical shaft enters through the 1848 mm-high cone bottom; two four-blade stages, packing/bearing housing, gearbox, motor, grout/baseplate and anchors | User-corrected 2026-07-30 from the supplied side view; detail dimensions remain Reference Values pending vendor GA |
| BLOW TANK-2 | Support legs | 4 × 250 mm square, 7746 mm high | User-corrected side-view arrangement: legs extend from grade to the cone/shell junction; section size remains replaceable |
| BLOW TANK-2 | Nozzle schedule | N1 DN400 upper tangential blow-line inlet; N2 DN400 upper circulation connection; N3 DN600 large vapour / stock connection; N4 DN300 dilution / recirculation connection; M1 DN600 shell access manway; N5 DN500 native placeholder at the 555 mm bottom opening / agitator mounting | Visible top/side connections plus minimum blow-tank process connections; sizes/elevations pending vendor GA |
| BLOW TANK-2 | Detailed hardware | Four anchors, grout/cleats and top gussets per support foot; E ladder stops at the supported DN7300 shell top and has base shoes; lifting lugs, nameplate and grounding lug; native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; all additions are outside the authoritative four-segment body profile |
| BLOW TANK-2 | Internal agitator | Ground-mounted central drive; vertical shaft enters through the 1848 mm-high cone bottom; two four-blade stages, packing/bearing housing, gearbox, motor, grout/baseplate and anchors | User-corrected 2026-07-30 from the supplied side view; detail dimensions remain Reference Values pending vendor GA |
| WARM WATER TANK | Roof rise | 855.0 mm (0.15 D) | skill/equipment/tanks-and-vessels.md, conical-roof default |
| WARM WATER TANK | Nozzle/manway schedule | N1 DN300 warm-water feed; N2 DN350 pump suction; N3 DN200 overflow; N4 DN150 high-point vent; M1 DN600 shell access manway | Minimum process-logical atmospheric-tank connections; bearings reconciled with the supplied top view |
| WARM WATER TANK | Detailed hardware | 12 connected anchor chairs; N fixed ladder with base shoes at 350 mm rung pitch; four lifting lugs; nameplate, grounding lug; individual flange geometry supplied by native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; dimensions are replaceable reference geometry pending vendor GA |
| BROWN HOT WATER TANK | Roof rise | 857.1 mm (0.15 D) | skill/equipment/tanks-and-vessels.md, conical-roof default |
| BROWN HOT WATER TANK | Nozzle/manway schedule | N1 DN300 brown-hot-water feed; N2 DN350 pump suction; N3 DN200 overflow; N4 DN150 high-point vent; M1 DN600 shell access manway | Minimum process-logical atmospheric-tank connections; bearings reconciled with the supplied top view |
| BROWN HOT WATER TANK | Detailed hardware | 12 connected anchor chairs; S fixed ladder with base shoes at 350 mm rung pitch; four lifting lugs; nameplate, grounding lug; individual flange geometry supplied by native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; dimensions are replaceable reference geometry pending vendor GA |
| JUNK TRAP-1 | Vessel height/configuration | 150 mm outlet clearance + 550 mm hopper + 1800 mm shell + 442.5 mm head | Junk-trap heavy-debris duty; no side view or capacity supplied |
| JUNK TRAP-1 | Nozzle schedule | N1 DN300 chip-circulation inlet; N2 DN300 circulation outlet; N3 DN200 flush-water connection; N4 DN200 equalizing / vent connection; N5 DN300 bottom heavy-reject discharge | Five visible plan connections reconciled with junk-trap circulation, flushing and reject-removal duties |
| JUNK TRAP-1 | Detailed hardware | Four anchors, grout/cleats and top gussets per support foot; no dedicated ladder on this low vessel; lifting lugs; nameplate, grounding lug; native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; replaceable reference geometry pending vendor GA |
| JUNK TRAP-2 | Vessel height/configuration | 150 mm outlet clearance + 550 mm hopper + 1800 mm shell + 442.5 mm head | Junk-trap heavy-debris duty; no side view or capacity supplied |
| JUNK TRAP-2 | Nozzle schedule | N1 DN300 chip-circulation inlet; N2 DN300 circulation outlet; N3 DN200 flush-water connection; N4 DN200 equalizing / vent connection; N5 DN300 bottom heavy-reject discharge | Five visible plan connections reconciled with junk-trap circulation, flushing and reject-removal duties |
| JUNK TRAP-2 | Detailed hardware | Four anchors, grout/cleats and top gussets per support foot; no dedicated ladder on this low vessel; lifting lugs; nameplate, grounding lug; native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; replaceable reference geometry pending vendor GA |
| ACCUMULATOR TANK | Pressure-vessel configuration | 1800 mm skirt; dished top/bottom; head rise D/4 | Batch-cooking liquor accumulator duty and skill/equipment/tanks-and-vessels.md pressure-vessel guidance |
| ACCUMULATOR TANK | Nozzle/manway schedule | N1 DN400 liquor inlet; N2 DN400 liquor outlet; N3 DN250 circulation return; N4 DN150 instrument / equalizing connection; N5 DN150 top vent / relief; M1 DN600 shell manway | Minimum process-logical accumulator connections; plan bearings follow the visible top-view connections |
| ACCUMULATOR TANK | Detailed pressure-vessel hardware | 16 skirt anchors with connected clamp plates; N fixed ladder with base shoes at 350 mm rung pitch; four lifting lugs; nameplate, grounding lug; native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; replaceable reference geometry pending vendor GA |
| ACCUMULATOR TANK AID-1 | Pressure-vessel configuration | 800 mm skirt; dished top/bottom; head rise D/4 | Batch-cooking liquor accumulator duty and skill/equipment/tanks-and-vessels.md pressure-vessel guidance |
| ACCUMULATOR TANK AID-1 | Nozzle/manway schedule | N1 DN250 liquor inlet; N2 DN250 liquor outlet; N3 DN150 circulation return; N4 DN150 instrument / equalizing connection; N5 DN150 top vent / relief; M1 DN500 shell manway | Minimum process-logical accumulator connections; plan bearings follow the visible top-view connections |
| ACCUMULATOR TANK AID-1 | Detailed pressure-vessel hardware | 8 skirt anchors with connected clamp plates; no dedicated ladder on the auxiliary vessel; four lifting lugs; nameplate, grounding lug; native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; replaceable reference geometry pending vendor GA |
| ACCUMULATOR TANK AID-1 | Cylindrical shell height | 4044.0 mm | No capacity or side view supplied; approximately 2D for the small auxiliary accumulator vessel |
| ACCUMULATOR TANK AID-2 | Pressure-vessel configuration | 800 mm skirt; dished top/bottom; head rise D/4 | Batch-cooking liquor accumulator duty and skill/equipment/tanks-and-vessels.md pressure-vessel guidance |
| ACCUMULATOR TANK AID-2 | Nozzle/manway schedule | N1 DN250 liquor inlet; N2 DN250 liquor outlet; N3 DN150 circulation return; N4 DN150 instrument / equalizing connection; N5 DN150 top vent / relief; M1 DN500 shell manway | Minimum process-logical accumulator connections; plan bearings follow the visible top-view connections |
| ACCUMULATOR TANK AID-2 | Detailed pressure-vessel hardware | 8 skirt anchors with connected clamp plates; no dedicated ladder on the auxiliary vessel; four lifting lugs; nameplate, grounding lug; native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; replaceable reference geometry pending vendor GA |
| ACCUMULATOR TANK AID-2 | Cylindrical shell height | 4044.0 mm | No capacity or side view supplied; approximately 2D for the small auxiliary accumulator vessel |
| W-L SERVICE TANK-1 | Roof rise | 750.0 mm (0.15 D) | skill/equipment/tanks-and-vessels.md, conical-roof default |
| W-L SERVICE TANK-1 | Nozzle/manway schedule | N1 DN250 white-liquor service inlet; N2 DN300 white-liquor outlet; N3 DN200 overflow / return; N4 DN150 high-point vent; M1 DN600 shell access manway | Minimum process-logical atmospheric-tank connections; bearings reconciled with the supplied top view |
| W-L SERVICE TANK-1 | Detailed hardware | 12 connected anchor chairs; N fixed ladder with base shoes at 350 mm rung pitch; four lifting lugs; nameplate, grounding lug; individual flange geometry supplied by native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; dimensions are replaceable reference geometry pending vendor GA |
| W-L SERVICE TANK-2 | Roof rise | 750.0 mm (0.15 D) | skill/equipment/tanks-and-vessels.md, conical-roof default |
| W-L SERVICE TANK-2 | Nozzle/manway schedule | N1 DN250 white-liquor service inlet; N2 DN300 white-liquor outlet; N3 DN200 overflow / return; N4 DN150 high-point vent; M1 DN600 shell access manway | Minimum process-logical atmospheric-tank connections; bearings reconciled with the supplied top view |
| W-L SERVICE TANK-2 | Detailed hardware | 12 connected anchor chairs; S fixed ladder with base shoes at 350 mm rung pitch; four lifting lugs; nameplate, grounding lug; individual flange geometry supplied by native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; dimensions are replaceable reference geometry pending vendor GA |
| MAIN CONDENSATE TANK | Horizontal vessel construction | 2391.5 mm straight shell, D/4 heads, 500 mm saddles | Plan view is a capsule with two transverse support bands; no side elevation was supplied |
| MAIN CONDENSATE TANK | Nozzle/manway schedule | N1 DN200 condensate inlet; N2 DN200 condensate outlet; N3 DN150 level / overflow connection; M1 DN500 inspection manway; N4 DN150 high-point vent | Minimum condensate-receiver process connections |
| MAIN CONDENSATE TANK | Detailed hardware | Four anchors per saddle; two lifting pads and pins; nameplate with screws; grounding lug; saddle wear/load-spreader and sole plates; native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; replaceable reference geometry pending vendor GA |
| SPENT LIQUOR TANK | Roof rise | 450.0 mm (0.15 D) | skill/equipment/tanks-and-vessels.md, conical-roof default |
| SPENT LIQUOR TANK | Nozzle/manway schedule | N1 DN150 spent-liquor inlet; N2 DN200 spent-liquor outlet; N3 DN100 overflow / return; N4 DN150 high-point vent; M1 DN600 shell access manway | Minimum process-logical atmospheric-tank connections; bearings reconciled with the supplied top view |
| SPENT LIQUOR TANK | Detailed hardware | 12 connected anchor chairs; no dedicated ladder on this grade-accessible vessel; four lifting lugs; nameplate, grounding lug; individual flange geometry supplied by native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; dimensions are replaceable reference geometry pending vendor GA |
| B-L TANK | Roof rise | 753.0 mm (0.15 D) | skill/equipment/tanks-and-vessels.md, conical-roof default |
| B-L TANK | Nozzle/manway schedule | N1 DN250 black-liquor inlet; N2 DN300 black-liquor outlet; N3 DN200 overflow / return; N4 DN150 high-point vent; M1 DN600 shell access manway | Minimum process-logical atmospheric-tank connections; bearings reconciled with the supplied top view |
| B-L TANK | Detailed hardware | 12 connected anchor chairs; E fixed ladder with base shoes at 350 mm rung pitch; four lifting lugs; nameplate, grounding lug; individual flange geometry supplied by native NOZZLE placeholders | User-directed visual-detail pass, 2026-07-30; dimensions are replaceable reference geometry pending vendor GA |

## Outstanding issues

**BLEACH HOT WATER TANK**

- Confirm vendor GA overall height and nozzle elevations/sizes.
- Confirm the placeholder native NOZZLE sizes and the receiving catalogue family against the final vendor nozzle schedule.

**BLOW TANK-1**

- Confirm support-leg section, bottom agitator mounting detail and all nozzle dimensions against the vendor GA.

**BLOW TANK-2**

- Confirm support-leg section, bottom agitator mounting detail and all nozzle dimensions against the vendor GA.

**WARM WATER TANK**

- Confirm vendor GA overall height and nozzle elevations/sizes.
- Confirm the placeholder native NOZZLE sizes and the receiving catalogue family against the final vendor nozzle schedule.

**BROWN HOT WATER TANK**

- Confirm vendor GA overall height and nozzle elevations/sizes.
- Confirm the placeholder native NOZZLE sizes and the receiving catalogue family against the final vendor nozzle schedule.

**JUNK TRAP-1**

- Confirm vessel height, design pressure and exact nozzle bearings.

**JUNK TRAP-2**

- Confirm vessel height, design pressure and exact nozzle bearings.

**ACCUMULATOR TANK**

- Confirm pressure rating, head profile, support height and complete vendor nozzle schedule.
- Confirm whether the plan-view outer ring is a platform, stiffener or insulation envelope before adding it.

**ACCUMULATOR TANK AID-1**

- Confirm pressure rating, head profile, support height and complete vendor nozzle schedule.
- Confirm whether the plan-view outer ring is a platform, stiffener or insulation envelope before adding it.

**ACCUMULATOR TANK AID-2**

- Confirm pressure rating, head profile, support height and complete vendor nozzle schedule.
- Confirm whether the plan-view outer ring is a platform, stiffener or insulation envelope before adding it.

**W-L SERVICE TANK-1**

- Confirm vendor GA overall height and nozzle elevations/sizes.
- Confirm the placeholder native NOZZLE sizes and the receiving catalogue family against the final vendor nozzle schedule.

**W-L SERVICE TANK-2**

- Confirm vendor GA overall height and nozzle elevations/sizes.
- Confirm the placeholder native NOZZLE sizes and the receiving catalogue family against the final vendor nozzle schedule.

**MAIN CONDENSATE TANK**

- Confirm saddle height, head geometry, long-axis bearing and vendor nozzle schedule from a side-view GA.

**SPENT LIQUOR TANK**

- Confirm vendor GA overall height and nozzle elevations/sizes.
- Confirm the placeholder native NOZZLE sizes and the receiving catalogue family against the final vendor nozzle schedule.

**B-L TANK**

- Confirm vendor GA overall height and nozzle elevations/sizes.
- Confirm the placeholder native NOZZLE sizes and the receiving catalogue family against the final vendor nozzle schedule.

**Project-wide**

- The supplied DWG could not be read locally because no DWG parser is installed. It was not uploaded to a third-party converter. The 16 exported PNG reference views were used.
- Each connection is represented by one native E3D `NOZZLE` placeholder in its own SUBE. The verified `/150lb_Ansi_Flanged` component mapping supplies a realistic temporary catalogue shape; Reference Value sizes must still be reconciled with the final vendor schedule and receiving-project catalogue.
- Replace Reference Value nozzle schedules, support dimensions and unknown side elevations when vendor GAs become available.

## Source register

- **Project requirements:** DO.txt — bottom-centre datum, total-height and profile-string rules
- **Equipment register:** Tank_list.xlsx, Sheet1!A1:H16
- **Reference top view:** Refs/BLEACH HOT WATER TANK.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/BLOW TANK-1(TOP).png — plan envelope and visible connection bearings
- **Reference side view:** Refs/BLOW TANK-1-2(SIDE).png — legs and composite arrangement
- **Blow-tank process basis:** Valmet methanol white paper — blow-tank flash vapour is condensed in blow heat recovery — https://www.valmet.com/globalassets/media/downloads/white-papers/power-and-recovery/methanol_waste_to_fuel_whitepaper.pdf
- **Reference top view:** Refs/BLOW TANK-2(TOP).png — plan envelope and visible connection bearings
- **Reference top view:** Refs/WARM WATER TANK.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/BROWN HOT WATER TANK.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/JUNK TRAP-1.png — plan envelope and visible connection bearings
- **Junk-trap process basis:** Valmet application-specific products — junk traps remove sand and debris from chip-chute circulation — https://www.valmet.com/flowcontrol/valves/application-specific-products/
- **Reference top view:** Refs/JUNK-TRAP-2.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/ACCUMULATOR TANK.png — plan envelope and visible connection bearings
- **Accumulator process basis:** Valmet application report 2611_01_01EN — batch cooking uses liquor accumulators to balance flows; digester circulation is pressure service — https://www.valmet.com/globalassets/sharepoint/imported/2611_01_01en.pdf
- **Reference top view:** Refs/ACCUMULATOR TANK AID-1.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/ACCUMULATOR TANK AID-2.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/W-L SERVICE TANK-1.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/W-L SERVICE TANK-2.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/MAIN CONDENSATE TANK.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/SPENT LIQUOR TANK.png — plan envelope and visible connection bearings
- **Reference top view:** Refs/B-L TANK.png — plan envelope and visible connection bearings

## PML implementation guarantees

- PML1 element-creation commands only; no render prologue or PML2.
- Every EQUI is anchored at `POS E 0 N 0 U 0`.
- `ORI` precedes `POS` for CYLI, CONE and DISH.
- Element-specific E3D datums are enforced centrally: CYLI/CONE/BOX centre; DISH rim/tangent plane.
- Native NOZZLE elements are emitted CATR first, then flange-face POS, `ORI P1 IS <axis>` and HEIG; the generated values are parsed back and checked independently.
- Off-axis rectangular support hardware is emitted with local X on its radial bearing and local Y tangent to the vessel; BOX orientation precedes POS and rotated bounds are parsed back.
- One independent EQUI per equipment item and one SUBE per nozzle/manway assembly.
- Blow Tank profile sections preserve the workbook's authoritative TOP-to-BOTTOM sequence and dimensions.

Final visual acceptance still requires loading the macros in the user's AVEVA E3D project; numerical and syntax verification cannot substitute for that E3D review.
