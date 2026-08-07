# Project Status Review Checklist — 2026-08-04

For item-by-item review. Test baseline: **288 passed / 2 skipped**.

## 0. Workspace hygiene

- The git working tree currently has many uncommitted changes plus untracked
  directories (`Projects/E3D_Syntax_Lab/`, `Projects/JK-Tank_Build/`,
  `Projects/JK_Cooking_Tank_Build/`, `Projects/JK_Pump_Build/` new files,
  new builders/tests/knowledge files).
- After the review, commit once as a snapshot of this round of work.

## 1. E3D_Syntax_Lab — syntax laboratory (substantially complete)

### EXTRUSION study — closed loop

| Candidate | Conclusion | Evidence |
|---|---|---|
| 01 | VERIFIED: POS = profile end plane, HEIG along +Z | user measured U 1000–1800 |
| 02 | Measured: coaxial; upper head 10 mm proud of native | Q ATT + native comparison |
| 03 | VERIFIED: POS→ORI and ORI→POS order-independent | occupied ranges identical |
| 04 | VERIFIED: two-head contact contract (lower head inset 10 mm, upper head flush) | user visual "EXTR perfect" |

### PIPE study — core and advanced families all measured

| Candidate | Content | Conclusion |
|---|---|---|
| 01–07 | straight pipe, 1:100 slope, elbow, reducer, TEE/B2 reciprocal references | rounds 1–2 VERIFIED |
| 08 | combined balanced cluster (four routes in the same ZONE) | re-submitted VERIFIED ("not complex"); crash = application/add-in level |
| 09/10 | crash-isolation halves | VERIFIED (09 Q ATT all correct, 10 HBore/TBore=100/80) |
| 11 | high-density full-component | isolated (/FIRE undefined, components not routed) → superseded by 14–17 |
| 13 | TEE CREF + GASKET query kit | VERIFIED: CREF=/CODEX-Q13-TEE/B2; GASKET Height 0mm zero-thickness marker |
| 14 | FILTER/CLOSURE/FBLIND/COUPLING/WELD | VERIFIED (imports normally, components display) |
| 15 | BEND/OLET/PTAPPING+PIPCARTESIAN | VERIFIED (incl. 45° elbow, /General-Tappings resolved) |
| 16 | B1/B2/B3 network + TEE2/OLET reciprocal refs (connection-first) | VERIFIED |
| 17 | CAP (/FIRE) | GATED: `(2,109) Undefined name /FIRE`, as predicted; await project supplying /FIRE |

Remaining evidence gaps (need new native samples; cannot be closed by writing
macros): `VTWAY`, routing plane/Router commands, insulation inheritance,
`INPRTR/OUPRTR` metadata.

## 2. JK-Tank_Build — WSB tank farm (22 units)

- Historical baseline: 22 units, 451 primitives, 114 nozzles (JK-Project).
- **dropleg appearance retrofit R3 — confirmed (2026-08-04)**
  - Deliverable: `Projects/JK-Tank_Build/output/WSB_TA_dropleg_retrofit_20260804_r3.txt`
  - R1→R3: four-section shell (total height 9986) + new east-facing DN200
    lower nozzle per unit; R2 deleted ACCESS and the original nozzles; R3
    corrected the nozzle ORI to `Y is S and Z is U`.
  - Over-height top nozzles and floating side nozzles: adjusted manually by
    the user and confirmed; no outstanding project issues.

## 3. JK_Cooking_Tank_Build — cooking tanks (15 units)

- R5 (2026-07-30) visually accepted; that is the accepted baseline.
- **R6 native-export retrofit — confirmed (2026-08-04)**
  - 14 units get a 50 mm base plate (diameter = shell + 300); 10 units get
    simplified supports, 348 bolts moved inward; ACCUMULATOR/AID_1/AID_2
    keep skirts; 4 units untouched.
  - Note: re-running the three retrofit scripts on the current file will
    corrupt it; restore the archived backup first.

## 4. JK_Pump_Build — pump batch (30 units)

- 2026-07-29 combined macro loaded and visually confirmed (current baseline).
- **2026-07-30 revision — confirmed (2026-08-04 E3D reload accepted)**
  - Per unit: removed the last two floating parts of BEARING_FRAME plus the
    last two support feet of COUPLING (4 total);
  - 60 nozzles mapped to catalogue DNs from the measured openings (see
    `JK_Pump_Build_nozzle_mapping.md`);
  - static/numeric checks pass; E3D reload confirmed.
- 3 units lack top views (203-PU-020 / 205-PU-004 / 205-PU-032) → remain
  UNCONFIRMED.
- Source workbook `Generic Type` 151Ib–179Ib autofill anomaly: recorded,
  source unchanged.

## 5. Inputs awaiting you

- None (unmentioned desktop files such as the pump centreline reference
  `PUMP_MID_LINE.txt` are ignored by convention and kept out of system work).

## 6. Working conventions (from 2026-08-04)

1. **No news is good news**: if the user does not raise a problem, the
   deliverable is accepted; do not loop back for confirmation.
2. **Deletion discipline**: in continuation work on native exports / manual
   baselines, parts that look redundant are kept and submitted for review
   first; delete only when the user explicitly asks.
3. Unmentioned desktop/external files are out of scope; focus on in-repo
   system work.

## 7. Suggested next steps

1. Commit this round's work (git commit) — all three project confirmations
   have been written back; the working tree awaits commit.
2. Keep E3D_Syntax_Lab complete; CAP (q17) waits for the project to supply
   `/FIRE`.
