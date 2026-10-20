# DD4060 Second-Floor Guardrail Addition R1

The additive PML1 macro creates a continuous native HANDRA perimeter with inward
bays around existing maintenance-platform supports, diagonal braces and concrete
columns. The source building and access R6 export remains unchanged.

## Load

1. Keep the received building/access model loaded.
2. Select the same writable ZONE that owns `/New_washer_biulding`.
3. Run the additive macro once:

```pml
$M C:\Users\A\Desktop\building_F2_guardrails_R1.txt
```

The new structure is `/DD4060_BUILDING_F2_GUARDRAILS_R1`. The macro contains no
deletions, edits to existing elements, catalogue rebinding or Save Work command.
It creates new names and is intended for one initial load. Existing names will
conflict on a repeated load; review the created structure before any rerun.

## Derived layout

| Item | Value and provenance |
|---|---|
| Floor top | U 9700 mm, from building origin -300 + extrusion POS 9850 + HEIG 150 |
| Coordinate system | Exported owner ZONE frame; do not assume it is world |
| Top / intermediate rail | 1100 / 550 mm above slab; copied from source HANDRA |
| Maximum post spacing | 1200 mm; copied from source HANDRA |
| Toe plate | Enabled, as on the existing source guardrails |
| Unfilleted route length | 67463.74 mm |
| Route points | 37 including repeated closure point; no open ends |
| Shortest straight route segment | 591.84 mm |
| Source obstacle envelopes checked | 64, including flush embedded plate tops |
| Floor stair entries | Both remain inside the guarded perimeter; center-to-route distances 680.40 / 912.00 mm for 900 mm stair widths |

The access structure has its own origin and a 180-degree plan rotation.
Its transformed geometry, rather than its naming conventions, determines the
bypass locations. Concrete columns terminating flush with the floor are not
treated as above-floor obstacles. Anchor bars starting below the embedded
plate underside are also excluded from above-floor detours.

## Reference Values

These are layout assumptions, not contractual dimensions or a certified design:

| Value | Basis |
|---|---|
| Nominal edge inset 150 mm | Keep the route inside the received slab outline |
| Section-axis envelope radius 125 mm | Conservative offline envelope for source HE160A, IPE120 and IPE200 families; actual catalogue geometry pending |
| Rail envelope radius 40 mm | Provisional route-clearance envelope; native tube/post bases require review |
| Clearance 100 mm | Requested bypass interpreted as a continuous inboard detour with a visible clearance allowance |
| Fillet / extra allowance 50 mm | Native route corner radius; added to exclusions to cover corner deviation |
| Merge edge return gaps below 300 mm | Avoid short returns between adjoining perimeter bays; isolated interior stair feet are not merged into corner bays |

Connected plate/member exclusions are enclosed in rectangular bays. This gives
simple continuous routes without 18-80 mm jogs. Under these envelopes, the
minimum clearance after rail radius and fillet allowance is 100 mm. The route
plus both allowances remains within the slab. This does not establish an
actual E3D catalogue-solid clash clearance or anchor design.

## Preservation and verification

Original and archived source SHA-256:
`c87af66310ac7b74281ad7339f17256ee4b79985c1bbd52a8448b761fe436dc0`.

There was no earlier accepted building baseline in this repository. All source
bytes form the preservation set. The additive macro has no existing element
names in common with the received export and does not modify its 46 building
extrusions, 346 GENSEC members, 162 PANEL elements, 47 HANDRA elements, six
STRFLT stairs, connections or references.

- The builder parses native source hierarchy, including omitted zero vertices,
  and composes inherited position/orientation transforms.
- The emitted macro is parsed back and numerically checked for closure,
  self-intersection, elevation, slab containment, envelope clearance and stair
  entry clearance. A zero-result parse fails.
- PML1 validation passes.
- `python -m pytest tests/test_handra_study.py tests/test_skill_integrity.py -q`:
  **83 passed**.
- `guardrail_plan.png` was visually inspected as an offline plan preview.

Native E3D loading, generated catalogue geometry, visual acceptance, actual
solid clashes, post/base anchorage, Save Work and reopen persistence remain
pending. No E3D session was modified in this run.

Reproduce the offline calculation from the repository root:

```text
python Projects/DD4060_Building_Guardrails/tools/build_guardrails.py
```

`layout_audit.json` records all obstacle envelopes, route coordinates and counts.
