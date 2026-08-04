# PML-STUDY-PIPE-001 — Native PIPE Export

## State

Rounds 1 and 2 completed in E3D Design Mk3.1.11.0[Z31110-056]: mixed
`VERIFIED` and `REJECTED` results. Candidates 06 and 07 both matched the
expected geometry.

## Evidence

- Native file:
  `Projects/E3D_Syntax_Lab/imports/2026-07-30_pipe_native.txt`
- Original path: `C:\Users\A\Desktop\pipe.txt`
- SHA-256:
  `A2E80B00C9B009F56260925B72FEFE4E0508006BFDC9BE374F983B9DB5437A77`
- Original size: 431,758 bytes; 26,379 lines
- Native listing timestamp: 30 Jul 2026 05:05
- E3D product/version: not stated in the evidence; user confirmation required
- Model intent supplied by user: native PIPE/piping network export
- Visual evidence: `source/pipe-view-01.png` through `pipe-view-03.png`

The screenshots show a multi-level network with long headers, many drops and
risers, equipment tie-ins, repeated parallel runs and dense local manifolds.

## Four-layer interpretation

### Database hierarchy

Observed hierarchy:

```
SITE
  ZONE
    PIPE
      BRANCH
        piping component
```

The export contains 3 new SITE elements, 4 ZONE elements, 84 PIPE elements and
166 BRANCH elements.

### Element and attribute layer

Most frequent new piping components:

| Element | Count | Initial interpretation |
|---|---:|---|
| `ELBOW` | 354 | Catalogue elbow; changes branch direction |
| `GASKET` | 170 | Flanged-joint gasket |
| `FLANGE` | 155 | Catalogue flange |
| `TEE` | 103 | Inline component with a connection P-point |
| `VALVE` | 74 | Catalogue valve |
| `COUPLING` | 47 | Coupling; also used around fabricated bends |
| `REDUCER` | 24 | Bore transition |
| `INSTRUMENT` | 12 | Inline instrument component |
| `BEND` | 9 | Fabricated/variable bend with explicit radius |
| `OLET` | 7 | Branch outlet component |

Also observed: `CAP`, `CLOSURE`, `FBLIND`, `FILTER`, `PCOMPONENT`,
`PTAPPING`, `PIPCARTESIAN`, `VTWAY`, `WELD`, `PSPOOL`, `PPLIST`, `PPIECE`,
`RPLANE`, `RPLGROUP` and `STRUCTURE`.

### Pose and connection layer

- A free BRANCH end is described by `HPOS/TPOS`, `HDIR/TDIR`,
  `HBOR/TBOR`, `HCON/TCON` and `LHEA/LTAI`.
- `HREF` and `TREF` connect BRANCH head/tail to nozzles, tees, olets,
  branch ends and other connectable components.
- `CREF` is the component-side reference from a TEE/OLET/VTWAY to a connected
  BRANCH end.
- Cyclic references are created in a second pass with `OLD ...`, after both
  referenced elements exist.
- All 1,013 new component blocks containing both pose attributes use `POS`
  before `ORI`. No `ORI`-before-`POS` counterexample occurs in this export.
- `SPRE SPCOMPONENT` selects component geometry; `HSTU` and `LSTU` identify
  the connected tube component.

### Macro/execution layer

The native listing is wrapped by synonym control, an error label and an
`INPUT BEGIN` / `INPUT END ...` / `INPUT FINISH` transaction. Nested elements
are closed by plain `END`. This is a data-listing form and must not be confused
with the equipment primitive macro conventions.

## Official support

AVEVA's Model Reference/Pipework Design help supports these interpretations:

- PIPE is administrative; PIPE owns BRANCH elements; BRANCH owns catalogue
  piping components.
- BRANCH has head and tail endpoints.
- Straight variable tube is automatically routed between adjacent components.
- When unconnected, a head uses `HBOR`, `HCON`, `LHEA`, `HPOS`, `HDIR`; tail
  has the corresponding `T...` attributes.
- Connected ends use `HREF`/`TREF`, and the reciprocal component reference is
  maintained through `CREF`.
- A piping component requires its `SPRE` attribute.

Official pages:

- https://help.aveva.com/AVEVA_Everything3D/2.1/PDUV/PDUV7.4.1.html
- https://help.aveva.com/AVEVA_Everything3D/2.1/DRMPGC/DRMPCM24.09.01.html
- https://help.aveva.com/AVEVA_E3D_Design/2.1/DRMPGC/DRMPCM24.09.05.html
- https://help.aveva.com/AVEVA_Everything3D/1.1/PDUV/PDUV8.09.4.html

Official documentation supports the data model, but does not by itself certify
the candidate against the user's receiving catalogue and E3D version.

## Study cards

### PML-STUDY-PIPE-001-A — Basic hierarchy and automatic tube

- Question: does the exported `SITE → ZONE → PIPE → BRANCH` form recreate a
  visible straight tube from only fixed head/tail attributes and `HSTU`?
- Candidate: `candidate/01_pipe_core.pml`, test T01.
- Prediction: a 100 mm nominal-bore straight tube appears from E 0 to E 4000.
- Decisive observation: visible tube and correct queried head/tail positions.

### PML-STUDY-PIPE-001-B — Catalogue components

- Question: do copied `/A3B` SPCOMPONENT references create an elbow, a small
  valve train and a 100×80 reducer in the receiving project?
- Candidate: `candidate/01_pipe_core.pml`, tests T02–T04.
- Prediction: all components render and implied tube fills the gaps.
- Alternative: undefined catalogue names mean syntax is sound but the receiving
  project catalogue differs.

### PML-STUDY-PIPE-001-C — Piping component pose order

- Question: is `POS → ORI` semantically required, or merely the exporter's
  canonical serialization order?
- Candidates: `02_pose_pos_then_ori.pml` and
  `03_pose_ori_then_pos.pml`.
- Prediction: the native-order candidate forms the intended Up-to-West elbow.
  The reversed candidate is expected either to drift, orient incorrectly or
  fail; an identical result would prove order independence for this component.
- Decisive observation: compare elbow position, branch centreline and connected
  tube shape between the two isolated sites.

### PML-STUDY-PIPE-001-D — TEE reciprocal references

- Question: does the native two-pass `CREF`/`TREF` pattern connect B2 to TEE P3?
- Candidate: `candidate/04_tee_branch_refs.pml`.
- Prediction: B2 meets the main-line tee without a gap and both references query
  back to each other.
- Decisive queries:
  `Q CREF` at TEE 1 and `Q TREF` at branch B2.

### PML-STUDY-PIPE-001-E — Slope reference

- Question: does `/1in100` resolve and persist on both PIPE and BRANCH, and does
  a matching 10,000 mm run with 100 mm fall display as one sloped tube?
- Candidate: `candidate/05_slope_1in100.pml`.
- Prediction: a straight line falls 100 mm in 10,000 mm and both `SLOREF`
  attributes query as `/1in100`.

### Round 1 result

See [RESULTS-ROUND1.md](results/RESULTS-ROUND1.md).

- Straight free-end BRANCH: passed visually and by endpoint attributes.
- ELBOW: component rendered but tube route remained dashed/ill-defined.
- ELBOW pose order: POS→ORI and ORI→POS produced equivalent placement.
- Valve assembly: flange, valve and implicit tube rendered; gasket is a thin
  joint component, not the long tube.
- REDUCER: component rendered on North/South axis; vertical-axis hypothesis
  rejected.
- TEE/B2: visual connection and B2 TREF passed; TEE CREF query still pending.
- 1:100 slope: visual and both SLOREF queries passed.

### PML-STUDY-PIPE-001-F — ELBOW Arrive/Leave

- Question: were the missing `ARRI 2` / `LEAV 1` attributes the cause of the
  dashed legs?
- Candidate: `candidate/06_elbow_arrive2_leave1.pml`.
- Prediction: both legs become solid tube and meet the elbow.
- Decisive evidence: solid tube plus `Q ARRIVE`, `Q LEAVE`, `Q ADIR`, `Q LDIR`
  on the ELBOW.

### PML-STUDY-PIPE-001-G — Vertical REDUCER axes

- Question: does the native vertical basis `ORI Y is N and Z is E` align the
  reducer and its P1/P2 with a vertical branch?
- Candidate: `candidate/07_reducer_vertical_native_axes.pml`.
- Prediction: reducer stands vertically and both adjacent legs become solid.
- Decisive evidence: visible axis and `Q ADIR`, `Q LDIR`, `Q ABORE`, `Q LBORE`
  on the REDUCER.

### Round 2 result

See [RESULTS-ROUND2.md](results/RESULTS-ROUND2.md).

- Candidate 06: `ARRI 2 / LEAV 1` produced a continuous solid Up-to-West
  DN100 elbow route, matching expectation.
- Candidate 07: `ORI Y IS N AND Z IS E` aligned the 100-to-80 reducer and both
  adjacent legs vertically, matching expectation.
- Both forms are now encoded in `wsb.piping_builder` as deliberately narrow
  E3D Design Mk3.1.11.0 VERIFIED contracts.

### Outstanding queries — RESOLVED (2026-08-04)

- TEE `CREF`: resolved. `Q ATT` on `TEE 1 of BRANCH /CODEX-Q13-TEE/B1`
  returned `Cref /CODEX-Q13-TEE/B2`, closing the reciprocal pair with B2's
  round-1 `TREF`.
- GASKET identity: resolved. `GASKET 1 of BRANCH /CODEX-Q13-GASKET/B1` carries
  `SPRE /A3B/GC20`, Arrive 1 / Leave 2 and **`Height 0mm`** — a zero-thickness
  joint marker, not a solid part. `RLOC` is not present in its Q ATT.
- Full transcript:
  `results/RESULTS-TEE-GASKET-QUERY.md`, raw evidence
  `results/evidence/2026-08-04_tee_gasket_query_success.txt`.
- 2026-08-04 first attempt errored: the macro ran while a ZONE was current, so
  `Q ATT` returned the ZONE, and `Q NAME ANSWER` failed with `(2,201) ... does
  not have attribute ANSW` — `Q NAME ANSWER` is attribute-specific (the SPCO
  bore) and must not be used as a generic query. Full transcript:
  `results/RESULTS-TEE-GASKET-QUERY-ERROR.md`, raw evidence
  `results/evidence/2026-08-04_tee_gasket_query_error.txt`. The second attempt
  (Q ATT only) still ran against a ZONE because the pack had no navigation; a
  third attempt with full-path ordinal references failed with
  `(2,109) Undefined name /CODEX-PIPE-LAB04/CODEX-P04-TEE/B1` — the round-1
  lab sites no longer exist in the receiving project.
- **Current tool:** candidate `13_tee_gasket_query_kit.pml` — self-contained;
  creates `/CODEX-PIPE-LAB13` (TEE route with reciprocal CREF/TREF plus the
  GASKET/FLANGE/VALVE assembly) and prints `Q ATT` for the TEE and GASKET in
  one `$M` run. No dependency on the deleted lab sites. Rev 2 runs the queries
  **inside** the INPUT transaction right after the two-pass references (site is
  current), because a leading-slash path after `INPUT FINISH` resolved against
  the then-current element and failed with `(2,109) Undefined name`. There is
  no ONERROR handler so a creation failure reports its exact line. Its
  creation+query form is **VERIFIED** by the successful 2026-08-04 run.

### PML-STUDY-PIPE-001-H — Balanced pipe cluster

- Question: can the shared builder emit several spatially separated PIPEs in
  one ZONE while selecting different verified syntax families by route intent?
- Candidate: `candidate/08_balanced_pipe_cluster.pml`.
- SHA-256:
  `0FA99F634B4D436BF2D95940A4908D10386FBFFD11842219FDB29C3B98606306`.
- Contents: one straight header, one 1:100 sloped run, one Up-to-West elbow
  route and one vertical 100-to-80 reducer route.
- Local verification: the embedded PIPE fragment is byte-for-byte equal to
  `PipingBuilder` output; four PIPEs/four BRANCHes are balanced; general PML
  validation and NEW/END hierarchy checks pass.
- Decisive E3D evidence: all four routes render simultaneously as solid,
  separated geometry; the slope falls correctly; elbow and reducer remain
  aligned in the combined cluster.
- First E3D attempt ended in an application-level Collections/My Data add-in
  crash with no CP error or echoed macro command. See
  `results/RESULTS-CLUSTER-CRASH.md`.
- Isolation candidates:
  `09_cluster_core_straight_slope.pml` and
  `10_cluster_components_elbow_reducer.pml`.
- Isolation candidate SHA-256:
  `69DF07785633D8ED3D13A2BBDBABF8F46ED0A098A616DC7620C94254054DF930`
  (09) and
  `E216485FAC75F33A03B40C844E30CE7B115DFF90C32FA428BB95627877D6F5BF`
  (10).
- State: `EXPERIMENTAL`; no PIPE syntax rejection has been observed.

> **User-confirmed 2026-08-04 (candidates 09/10).** Both isolation halves
> passed: 09 rendered the straight header and 1:100 slope with all queried
> HPOS/TPOS/HDIR/TDIR/HSTU/PSPE/SLOREF values matching the macro
> (`Sloreference /1in100` persisted); 10 rendered the Up-to-West elbow and the
> vertical reducer with `HBore 100mm` / `TBore 80mm`. The Collections/My Data
> crash in candidate 08 is therefore not caused by any of the four verified
> syntax families — it is an application/add-in level failure. See
> `results/RESULTS-ISOLATION-09-10.md`.

> **User-confirmed 2026-08-04 (candidate 08 re-submitted).** The balanced
> cluster loaded without issue and was described as "not complex" — all four
> routes (straight, 1:100 slope, Up-to-West elbow, vertical reducer) coexist in
> one ZONE. The earlier Collections/My Data fatal exception is therefore
> finally closed as an application/add-in level failure; candidate 08 is
> VERIFIED as a combined-load form.

### PML-STUDY-PIPE-001-I — High-density all-component stress package

- Generator: `build_high_density.py`.
- Candidate: `candidate/11_high_density_all_components.pml`.
- Inventory: 16 PIPE, 16 BRANCH and 180 catalogue component blocks. It covers
  FLANGE, GASKET, VALVE, INSTRUMENT, ELBOW, TEE, REDUCER, OLET, COUPLING,
  BEND, FILTER, CLOSURE, CAP and WELD across A3B and FIRE specifications,
  plus alternating 1:100 sloped branches.
- Catalogue evidence: paths are copied from the preserved A3B native export;
  component semantics beyond the previously verified ELBOW/REDUCER forms are
  still experimental.
- Local verification: shared builder output, PML validation and inventory
  counts pass. Candidate SHA-256:
  `F655678400CD5EA69AA346996AAAE72AA13A10766496FF0A539183EFC7A339FF`.
- Decisive E3D evidence: all 16 routes load, components render, no draw-list
  crash occurs, and no component remains dashed or detached unexpectedly.
- State: `EXPERIMENTAL`, pending high-density E3D 3.1 verdict.

### PML-STUDY-PIPE-001-J — Advanced family isolation (candidates 14-17)

Generator: `build_advanced_candidates.py` — slices the exact native blocks,
renames them into isolated SITEs and adds nothing by hand. No component
syntax is synthesized.

| Candidate | SITE | Families | Contents |
|---|---|---|---|
| `14_advanced_inline_families.pml` | `/CODEX-PIPE-LAB14` | FILTER, CLOSURE, FBLIND, COUPLING, WELD | One native PIPE/BRANCH slice per family, all `/A3B` (+ `/WELDGAP` weld gaps) |
| `15_advanced_pose_families.pml` | `/CODEX-PIPE-LAB15` | BEND, OLET, PTAPPING + PIPCARTESIAN | Native slices incl. 45° elbow (`ANGL 45degree`), `/A3B/TOL:100_80`, `/General-Tappings/TAPPING-200mm` |
| `16_connection_first_network.pml` | `/CODEX-PIPE-LAB16` | TEE 2, OLET 1/2 + B1/B2/B3 network | `/100-B-1` verbatim with only its internal reciprocal refs (OLET↔B2, TEE2↔B3) and PSPOOL/PPLIST/PPIECE metadata |
| `17_cap_fire_spec.pml` | `/CODEX-PIPE-LAB17` | CAP | Native `/FIRE` slice; expected to fail with `(2,109) Undefined name /FIRE` until the receiving project defines that spec |

Expected observations (14/15): each pipe renders as a solid route with its
component visible and correctly posed; a family whose catalogue path does not
resolve reports `(2,109)` at its own line instead of silently drawing nothing.
Expected observations (16): the three branches stay connected — B2 meets the
two OLETs and B3 meets TEE 2 without gaps; queried `HREF/TREF/CREF` point back
at each other; no dashed route legs.
Expected observations (17): `/FIRE` either resolves and CAP renders, or the
known undefined-spec error appears — either is a recorded verdict.

Run order suggestion: `q14.pml` → `q15.pml` → `q16.pml` → `q17.pml` (Desktop
short-path copies). Delete the corresponding `/CODEX-PIPE-LAB1x` site before
re-running a candidate.

> **User-confirmed 2026-08-04.** Candidates 14, 15 and 16 imported normally
> with every component family displaying — FILTER, CLOSURE, FBLIND, COUPLING,
> WELD, BEND, OLET, PTAPPING+PIPCARTESIAN and the B1/B2/B3 network all render
> from their verbatim native slices. Candidate 17 failed exactly as predicted:
> `(2,109) Undefined name /FIRE` — CAP is gated on the receiving project
> defining `/FIRE`, not on syntax. See
> `results/RESULTS-ADVANCED-CANDIDATES.md`.

## Deferred studies

The following forms are real native observations but are intentionally excluded
from the first certification package:

1. `BEND`, `COUPLING`, `WELD`, `PSPOOL`, `PPLIST`, `PPIECE` — VERIFIED in
   candidates 14/16;
2. `PTAPPING` + `PIPCARTESIAN` — VERIFIED in candidate 15
   (`/General-Tappings` resolved);
3. `OLET` and multi-branch reciprocal connections — VERIFIED in candidates
   15/16; `VTWAY` still needs its own slice;
4. routing planes, routing groups and `Router` UI commands;
5. insulation/tracing specs, fluid and pressure inheritance;
6. `INPRTR/OUPRTR`, which appear to be project/router metadata rather than
   geometry essentials.

Items 4-6 remain open; each needs its own native slice and isolated study.
CAP is additionally gated on the receiving project defining `/FIRE`.
