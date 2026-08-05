# E3D Syntax Lab

## Scope and status

Active capability-development project. It preserves native E3D exports, derives
testable syntax hypotheses and packages isolated macros for user certification.

Current study: `PML-STUDY-PIPE-001`, native PIPE/BRANCH network. Rounds 1 and 2
have user-observed results; candidates 06 and 07 both matched expectation.
Receiving runtime: AVEVA Everything3D 3.1, E3D Design
Mk3.1.11.0[Z31110-056].

Second active study: `PML-STUDY-EXTR-001`, the native `/PMP-10` pump listing
and three orthographic screenshots supplied on 2026-08-03. Its immutable source,
analysis and three isolated certification candidates live under
`experiments/PML-STUDY-EXTR-001/`: 01 datum/axes, 02 hex-fastener contact and
03 POS/ORI assignment-order sensitivity. The hierarchy and local profile/axis
contract are supported by the native export, AVEVA documentation and installed
E3D 3.1 PML source. The longitudinal POS datum is now traced to AVEVA's own
creation code (`dbenextrusion.pmlfrm:1448`, `dbeextrusion.pmlfrm:1153`,
`mmmcounterweight.pmlobj:820`) as the profile end plane with `HEIG` sweeping
toward +Z, and that meaning plus assignment-order independence were certified
by the user in E3D on 2026-08-04: candidate 01 occupied U 1000..1800 from
`POS U 1000`/`HEIG 800` (end plane), and candidate 03 showed POS->ORI and
ORI->POS occupy identical ranges. Candidate 02 was measured the same day:
coaxial, lower head matching the native pattern (POS U 20, shank protrudes
10 mm), upper head 10 mm proud of the shank top. The native `/PMP-10` specimen
defines the expected two-head contract (lower head 10 mm inset, upper head
flush), and candidate 04 reproduces it — visually confirmed by the user on
2026-08-04 ("EXTR is perfect"). **The EXTRUSION study is closed.**

PML delivery rule: generated PML is always saved as a `.pml` file and returned
as a file link; do not paste the full macro into the chat window.

Archived DRAWING syntax experiments include the 26-letter point-loop alphabet;
see `PML-STUDY-PIPE-001/results/RESULTS-ALPHABET.md`.

Current next candidate: `08_balanced_pipe_cluster.pml`, combining a straight
header, a 1:100 sloped run, the verified Up-to-West elbow form and the verified
vertical reducer form in one isolated ZONE. Local builder equivalence and
hierarchy validation pass. Its first E3D attempt ended in a Collections/My Data
add-in fatal exception with no PML error. Candidates 09 and 10 split the core
and catalogue-component halves for crash isolation.

For the PIPE study's outstanding TEE/GASKET evidence, a query pack now exists
at `PML-STUDY-PIPE-001/queries/12_query_tee_gasket.mac`, but it is superseded
by candidate `13_tee_gasket_query_kit.pml`: a self-contained kit that creates
`/CODEX-PIPE-LAB13` (TEE + reciprocal CREF/TREF and the GASKET/FLANGE/VALVE
assembly) and prints `Q ATT` for both components in one `$M` run. The earlier
approaches failed because `Q NAME ANSWER` is attribute-specific (ZONE error)
and because the round-1 lab sites no longer exist (`(2,109) Undefined name`);
rev 2 runs the queries inside the INPUT transaction (relative references,
proved by candidate 04) because post-INPUT leading-slash paths did not
resolve against WORLD. The kit succeeded on 2026-08-04: TEE `CREF` queried
back to `/CODEX-Q13-TEE/B2` and the `/A3B/GC20` gasket measured `Height 0mm`
— a zero-thickness joint marker. Both outstanding PIPE study queries are
closed.
For the EXTRUSION study, a matching measurement pack is at
`PML-STUDY-EXTR-001/queries/01_measure_extrusions.mac`.

## PML-STUDY-SCREW-001 (2026-08-05)

Newest study: a refined fastener set that exercises primitive selection
instead of path dependency. One `/CODEX_SCREW_001` EQUIPMENT carries three
screws, each head form built with the primitive that matches its real shape:
hex head as EXTRUSION/LOOP/VERTEX (the VERIFIED native form), button head as
a shallow DISH dome, square head as a BOX. CYLINDER carries the shank and
thread root, thin CYLINDER discs add the thread ridges (all inside the root
range, so nothing is detached), and CONE forms the head fillets and tip
chamfers. Candidate 01 was generated from individually VERIFIED forms,
passes `validate_pml` and a numeric geometry parse (face-to-face contacts,
ridge containment, bounds, lowest point U 0), and the user accepted it in
E3D on 2026-08-05 ("可以的"). The assembly contract — head primitive chosen
by head form, CYLINDER body/root, additive thread ridges, CONE transitions —
is promoted to `skill/knowledge/pml-spatial-lookup.md` as VERIFIED, because
every element form it uses was already individually VERIFIED and the set was
user-accepted. A detailed Q ATT measurement pack remains available but is
optional.

Crash isolation closed 2026-08-04: candidates 09 (straight/slope) and 10
(elbow/reducer) both passed visual and attribute confirmation, so the
candidate 08 Collections/My Data crash is an application/add-in level failure,
not a syntax problem. Candidate 08 can be re-submitted as a combined-load
stress case now that both halves are certified.

Candidate 08 was re-submitted on 2026-08-04 and loaded normally (user: "not
complex"); the Collections/My Data crash investigation is closed as an
application/add-in level failure.

Advanced PIPE families are now isolated in candidates 14-17 (generated from
verbatim native slices by `build_advanced_candidates.py`): inline families
(FILTER, CLOSURE, FBLIND, COUPLING, WELD), pose families (BEND, OLET,
PTAPPING+PIPCARTESIAN), a connection-first `/100-B-1` B1/B2/B3 network with
only its internal reciprocal references, and a CAP probe that intentionally
tests the known-undefined `/FIRE` spec. User verdicts 2026-08-04: candidates
14, 15 and 16 imported normally with every component family displaying
(VERIFIED for the exact native forms); candidate 17 failed exactly as
predicted with `(2,109) Undefined name /FIRE`, so CAP stays gated on the
receiving project defining `/FIRE`.

The next stress artifact was candidate 11, generated by the project-local
`build_high_density.py`: 16 dense PIPE routes and 180 native-copied component
blocks across the observed A3B and FIRE families. It is now quarantined: the
receiving project rejected `/FIRE` as undefined, and the user screenshots show
that the generic component rows were not connected into logical routes. The
user had earlier confirmed that, after resetting E3D, a normal elbow import
completed and displayed correctly; that environment recovery does not validate
candidate 11.

An independent deletion of an existing project element produced the same
Collections/My Data startup failure and then crashed through
`MyDataCollectionClaimlist.DatabaseService_ClaimRelease`. Read-only browsing
works. The blocker is therefore an E3D add-in mutation-event failure, not the
PIPE candidate.

## Source data

- `Projects/E3D_Syntax_Lab/imports/2026-07-30_pipe_native.txt`
- SHA-256:
  `A2E80B00C9B009F56260925B72FEFE4E0508006BFDC9BE374F983B9DB5437A77`
- Three user-supplied E3D screenshots preserved under the study `source/`
  directory.
- E3D version confirmed by the user/SIR: AVEVA Everything3D 3.1, E3D Design
  `Mk3.1.11.0[Z31110-056]`.

## Modeling/experiment decisions

- Split the first trial into independent numbered candidates so one failing
  hypothesis cannot hide the others.
- Test core hierarchy and common catalogue components first.
- Compare component pose order in two otherwise equivalent candidates.
- Test cyclic TEE/BRANCH references using the native two-pass `OLD` pattern.
- Defer fabrication and Router metadata until base route semantics are proven.

## Problems found

The shared validator globally rejected `SPRE SPCOMPONENT`, based on a failure
specific to native equipment NOZZLE binding. The pipe export contains 1,112
valid-looking `SPRE` lines and AVEVA documentation requires component `SPREF`.
The validator was corrected to reject SPRE only inside NOZZLE blocks and accept
it for piping components.

Round 1 then exposed two geometry failures:

- an ELBOW rendered but both legs remained dashed because the copied native
  `ARRI 2 / LEAV 1` contract had been omitted;
- a REDUCER rendered North/South because primitive Z-axis reasoning was applied
  to a P-point-oriented catalogue component.

The `POS/ORI` comparison also disproved the predicted order sensitivity for the
tested ELBOW: both orders placed it identically.

## Round 2 accepted results

- Candidate 06 restored `ARRI 2 / LEAV 1`; the DN100 Up-to-West elbow and both
  legs rendered as one continuous solid route.
- Candidate 07 used `ORI Y IS N AND Z IS E`; the 100-to-80 reducer stood
  vertically and both adjacent legs were solid and coaxial.
- Screenshots and SHA-256 hashes are recorded in
  `results/RESULTS-ROUND2.md`.

## Outstanding issues

- Catalogue paths `/A3B`, `/A1A` and slope `/1in100` must resolve in the
  receiving project.
- TEE CREF still requires a query while the TEE—not B1—is current.
- GASKET identity/attributes are not yet queried; it is visually occluded at
  the flange interface.

## Lessons promoted

- Added `skill/knowledge/piping-reference.md`.
- Corrected element-specific SPRE validation and added a regression test.
- PIPE/BRANCH moved from an unspecified capability gap to a formal
  native-observed, official-supported study.
- Added the evidence-gated `wsb.piping_builder` engine for the
  E3D Design Mk3.1.11.0 VERIFIED free-ended straight/slope BRANCH forms. Catalogue-component
  generation now includes the exact candidate-06 elbow and candidate-07
  vertical reducer contracts; other bearings and multi-component routes remain
  evidence-gated.
- Added the project rule that syntax selection is intent- and evidence-weighted,
  not biased toward whichever primitive or catalogue form is most familiar.
- Added the evidence-gated `wsb.extrusion_builder`. It emits full-name
  `EXTRUSION`/`LOOP`/`VERTEX` hierarchy, validates a non-zero ordered planar
  profile and deliberately accepts a native POS datum without inventing a
  centre/bottom conversion.
- The pump specimen contains 17 extrusions: one custom support section and 16
  true hex heads paired around eight CYLINDER shanks. This is now the quality
  lesson for balanced high-detail modeling: use EXTRUSION for real section
  geometry, preserve simpler primitives where they are physically correct and
  verify every fine detail as part of a connected assembly.
