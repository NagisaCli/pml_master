# Square flange to DN600 round outlet

Status: offline candidate, generated 2026-10-19. Native E3D loading, readback,
visual acceptance and save/reopen persistence remain pending.

The macro creates one concentric, hollow fabricated transition with a local
bottom-centre datum at `(0, 0, 0)` and an overall envelope of
`820 x 820 x 500 mm`. It creates one EQUI and three SUBE assemblies in
physical top-to-bottom order:

| Assembly | Nominal elevation | Governing geometry |
|---|---|---|
| `SQROUND_DN600_H500_01_FLANGE` | U 480 to 500 | Square frame 820 x 820, clear opening 720 x 720; 12 holes diameter 14 |
| `SQROUND_DN600_H500_02_TRANSITION` | U 80 to 480 | 380 tapered length and 20 square neck; open square to round transition |
| `SQROUND_DN600_H500_03_OUTLET` | U 0 to 80 exposed | DN600 circular open stub, plus 4 mm overlap into the taper |

## Source dimensions

The archived [source plan](../imports/source_plan.png) governs the flange.
Hole centres lie on a 775 mm square, 22.5 mm from each outer edge. The four
ordinates along each side, measured from the first hole, are `0, 258, 517,
775 mm`. The corresponding centred coordinates are `-387.5, -129.5, 129.5,
387.5 mm`. Corner holes are shared, giving twelve unique holes.

The conversation governs overall height 500 mm and the user's clarification
governs the nominal outlet size DN600.

## Reference Values

The drawing does not specify plate thickness, pipe series, wall thickness,
pressure class, axial subdivision, material or installation coordinates.
The candidate uses the following replaceable Reference Values:

- Flange thickness 20 mm, shell and pipe wall thickness 6 mm.
- DN600 Series A outside diameter 610 mm; the assumed wall gives an actual
  clear bore of 598 mm. DN600 remains the nominal designation, not a claim
  that either measured diameter equals 600 mm. Basis: the manufacturer's
  [DN600 Series A dimension table](https://www.united-steel.com/m/newsshow/1102.html)
  and [LSAW pipe dimensions](https://www.united-steel.com/productshow/lsaw-steel-pipe.html).
- Nominal axial allocation 20 flange + 400 transition assembly + 80 outlet.
- Square neck extends from U 456 to 482, providing 4 mm overlap into the
  taper and 2 mm into the flange. The nominal neck occupies U 460 to 480.
- Outlet solid length 84 mm includes 4 mm overlap into the taper. This
  maintains wall coverage at the lower edge of the inclined panels.
- Local bottom-centre datum; no plant coordinates are inferred.

These references specify a geometry candidate, not a pressure-rated standard
fitting or an approved fabrication drawing. The custom square flange follows
the supplied dimensions. No circular flange, bolt set, gasket or weld bead
was added because the source does not define them.

## Construction and verification

The taper uses a radial-line development: four planar triangular sides and
four conical corner fans, each discretised into 24 triangular prisms. There
are 100 transition panels; maximum circular chord sagitta is about 0.1633 mm.
Each panel is 6 mm thick normal to its face, with a bounded 0.30 mm in-plane
vertex expansion for neighbouring-panel overlap. This is a faceted geometric
approximation, not an exact smooth loft or a fabrication shell analysis.

The macro contains 109 positive solids and 13 owned NCYLINDER children.
Twelve negatives cut the flange bolt holes; the thirteenth opens the round
stub. Every negative has `NAPPFLAG 2` and owner-local coordinates.

The [audit](Square_to_Round_DN600_audit.json) is computed after reopening the
written PML, through the shared native-tree parser. It checks exact bounds,
ownership, three SUBE groups, nonzero panel areas, right-handed frames,
hole count/positions/diameters, pipe bore and negative application. Horizontal
ray intersections inspect 1,440 directions at each of 21 elevations, including
both joints. Every sampled direction has wall coverage and an open passage;
the audit also rejects radial gaps over 0.05 mm and radial wall thickness
below 5.9 mm. Sampling does not certify watertightness or manufacturability.

Seven physical mutation probes must be rejected: equipment displacement,
flange separation, disabled subtraction, wrong bore, duplicated fan leaving
a missing sector, a vertically detached taper and an undersized panel wall.
All retain the original element inventory, so counting elements cannot pass
these faults by itself.

## Load and review

Select a writable ZONE, then run:

```text
$M C:\Muvsera\Projects\pml_master\Projects\Square_to_Round_DN600\output\Square_to_Round_DN600.pml
```

The resulting equipment is `/SQROUND_DN600_H500`. Review native rendering of
the flange bores, square neck, corner fans and open lower stub. No live E3D
session was mutated in this run. The macro does not contain Save Work.

The receiving catalogue was not supplied. The circular outlet is a fabricated
geometric stub with no native NOZZLE or piping P-point binding. A catalogue
connection must be selected separately if downstream piping connectivity is
needed; no reference from another project's catalogue is reused.

Rebuild and audit from the repository root:

```text
python Projects/Square_to_Round_DN600/tools/build.py
python -m pytest Projects/Square_to_Round_DN600/tools/test_build.py -q
```
