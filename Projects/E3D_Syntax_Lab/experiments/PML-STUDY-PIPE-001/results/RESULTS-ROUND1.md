# Round 1 E3D Results — User Observed 2026-07-30

E3D version: AVEVA Everything3D 3.1, E3D Design
Mk3.1.11.0[Z31110-056].

## Evidence files

| Screenshot | SHA-256 |
|---|---|
| `01_CODEX-P01-T02-ELBOW-show.png` | `E34663CC749F0C89C57FBFAE395D75B4969C84936067E83E55945F03498FBC36` |
| `01_CODEX-P01-T03-ELBOW-show.png` | `CB90078FF59EE26020CAFA14D3CDAD09E40455FD2B9EB637F87C0582C1B67A5E` |
| `01_CODEX-P01-T04-REDUCER-show.png` | `92A38AD93AD072101C5E80C697558842163675660AB24E7D8DB31FA2AAACBA36` |
| `02_pose_pos_then_ori.pml-show.png` | `A9E11DC5401D7F077D02892514679117011D99B362E3069DB692371EF6536CD9` |
| `03_pose_ori_then_pos.pml-show.png` | `02A4088A29B489DB222CC94E7BFEAA799105C2ADC395492E05604FAE32647397` |

## T01 — Straight BRANCH

User result: passed visually and by attributes.

```
Hposition WRT Owner  E 0mm N 0mm U 0mm
Tposition WRT Owner  E 4000mm N 0mm U 0mm
```

A DN100 straight tube rendered. This confirms the tested free-end BRANCH form
can generate implicit tube without an owned component.

State: `VERIFIED` in E3D Design Mk3.1.11.0.

## T02 / candidates 02 and 03 — ELBOW and pose order

User result:

- ELBOW rendered at the intended position.
- Both route legs were green dashed lines rather than solid tube.
- `POS → ORI` and `ORI → POS` both loaded, placed the elbow correctly and
  produced visually equivalent results.

Interpretation:

1. The component pose assignment order did not affect this ELBOW in the tested
   data-listing input context.
2. The dashed legs are not a display preference. AVEVA documentation defines a
   dotted/dashed route as geometrically incorrect or ill-defined: adjacent
   arrive/leave directions do not form a valid tube route.
3. The copied native ELBOW block used `ARRI 2` and `LEAV 1`; the candidate
   accidentally omitted both. Default is Arrive 1, Leave 2. This is the leading
   root-cause hypothesis and is isolated in candidate 06.

State:

- pose-order comparison: `USER-CONFIRMED` for this ELBOW/context;
- complete elbow/tube construction: `REJECTED` for the round-1 form;
- `ARRI 2 / LEAV 1` repair: `EXPERIMENTAL`.

## T03 — FLANGE / VALVE / GASKET

User result: flange, valve and a solid straight tube rendered. The GASKET could
not be selected/highlighted in the view.

Interpretation:

- `GASKET` is a catalogue joint component, not the long straight tube.
- In this candidate the gasket and flange positions differ by only 1.5 mm, so
  the gasket is an extremely thin item at the flange interface and is visually
  occluded/easy to miss.
- The long solid cylinder after the valve is implicit branch tube.
- Select the GASKET in Model Explorer rather than trying to pick its thin
  geometry in the view.

State: common inline assembly visually `USER-CONFIRMED`; precise gasket
selection/attributes remain unqueried.

## T04 — REDUCER

User result:

- reducer rendered;
- branch legs remained dashed;
- reducer lay on the North/South axis instead of vertical.

Cause:

- the candidate used `ORI Y is E and Z is U`;
- native horizontal North/South reducers use that basis;
- multiple native vertical reducers use `ORI Y is N and Z is E`;
- piping catalogue component axes are P-point/local-axis based, not the
  primitive "axis of revolution is Z" rule.

State: round-1 vertical orientation hypothesis `REJECTED`. Candidate 07 uses the
native vertical basis.

## TEE references

User result: geometry and highlighting fully matched expectation. On B2:

```
Tref TEE 1 of BRANCH /CODEX-P04-TEE/B1
```

The reported `Q CREF` error says current element was:

```
BRANCH /CODEX-P04-TEE/B1
```

A BRANCH has no CREF, so this does not test the TEE's CREF. Select
`TEE 1 of BRANCH /CODEX-P04-TEE/B1` in Model Explorer, then execute `Q CREF`.

State:

- geometry: `USER-CONFIRMED`;
- B2 `TREF`: `USER-CONFIRMED`;
- TEE `CREF`: query pending.

## 1:100 slope

User result: visual geometry fully matched expectation. Both PIPE and BRANCH
returned:

```
Sloreference /1in100
```

State: `VERIFIED` in E3D Design Mk3.1.11.0.
