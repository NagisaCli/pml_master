# Workflow: Learning PML from Native E3D Exports

Use this workflow when the user supplies an E3D-native macro/export as a
**teaching specimen** and explains what the exported model represents. The
purpose is not merely to copy the text. The purpose is to recover a reusable
relationship between model intent, database hierarchy, element attributes,
coordinate semantics and executable macro syntax.

This is the primary capability-growth loop for the skill:

```
native export -> semantic analysis -> isolated experiment -> E3D trial
              -> user confirmation -> VERIFIED rule -> builder + regression test
```

The user operates the authoritative E3D runtime. A local parser or green Python
test can reject obvious defects, but it cannot promote an experimental geometry
claim to VERIFIED without E3D evidence.

---

## Route the input before touching it

Native exports arrive for two different reasons:

| Input intent | Route |
|---|---|
| "This export shows how E3D represents this model; learn it" | This workflow |
| "I edited this model in E3D; continue changing it" | [reconciling-native-exports.md](reconciling-native-exports.md) |
| Both: learn the syntax and continue the model | Preserve/reconcile first, then study a copy here |

A teaching specimen is evidence, not automatically the next project baseline.
A manually edited continuation is the working geometry baseline and must not be
overwritten.

---

## The four layers to recover

Do not treat exported macro text as one undifferentiated language. Classify each
meaningful line into one of four layers:

| Layer | Question it answers | Typical content |
|---|---|---|
| Database/hierarchy | What owns what, and what is selectable? | `EQUI`, `SUBE`, names, ownership transitions |
| Element/attributes | What E3D object is created and which properties define it? | `CYLI`, `BOX`, `DIAM`, `HEIG`, catalogue references |
| Pose/spatial semantics | Where is its datum, which local axis is meaningful, and in what order is pose evaluated? | `POS`, `ORI`, P-points, owner-relative coordinates |
| Macro/execution | How is command text loaded, queried or controlled? | `$M`, comments, query commands, PML1 expressions |

Official PML manuals primarily describe the language and execution layer. A
native export and the installed AVEVA library often reveal database-element
command forms. Only a controlled E3D experiment settles ambiguous spatial
semantics such as a datum or orientation order.

The official starting point for the language layer is AVEVA's
[E3D 3.1 PML Customisation User Guide](https://help.aveva.com/AVEVA_Everything3D/3.1/PMLPUG/PMLCG2.02.1.html).
Record the exact manual page and product version for every manual-derived claim.

---

## Phase 1 — Intake and preserve

For every specimen, capture:

- the model/equipment name and what the user says it represents;
- E3D product/version and module, when known;
- whether it is an untouched native export or manually edited after export;
- the export method/command, when known;
- expected visible shape, axes, connection points and important datums;
- the original filename and SHA-256 hash.

Store the original unchanged under:

```
Projects/<project>/imports/<date>_<topic>_native.<ext>
```

Study a copy. Never clean, reformat or rename elements inside the evidence file.

---

## Phase 2 — Parse the structure before interpreting it

Produce an inventory in source order:

1. hierarchy path and owner for every named element;
2. element type and all explicit attributes;
3. attribute order, especially catalogue binding, `ORI` and `POS`;
4. local/world coordinate forms and P-point references;
5. repeated blocks and the one attribute that varies between them;
6. commands or attributes not yet present in
   [pml1-reference.md](../knowledge/pml1-reference.md).

Use the semantic comparator where a known baseline exists:

```bash
python -m wsb.pml_compare known.pml native.pml --format json
```

An observed sequence proves only that the export contains that sequence. It
does not yet prove why the order matters, what the datum means, or whether a
shorter form is equivalent.

---

## Phase 3 — Build a syntax study card

Create one study card per new element, attribute or disputed behaviour. Do not
combine several unknowns into one claim.

| Field | Required content |
|---|---|
| Study ID | Stable identifier, for example `PML-STUDY-EXTRU-001` |
| Model intent | The visible/engineering feature being represented |
| Hierarchy context | Full owner path and neighbouring element types |
| Exact observed block | Minimal verbatim block from the preserved export |
| Attribute dictionary | Meaning hypothesis for each line |
| Datum hypothesis | What physical point `POS` appears to locate |
| Axis hypothesis | Which local axis/P-point controls the feature |
| Order hypothesis | Which attributes may be order-sensitive |
| Evidence | Native file/hash, official page, installed AVEVA source, prior trial |
| Current state | `NATIVE-OBSERVED`, `OFFICIAL-SUPPORTED`, `EXPERIMENTAL`, `VERIFIED`, `REJECTED` |
| Open question | The single fact the next experiment must settle |

`NATIVE-OBSERVED` is not a synonym for `VERIFIED`: the text is authentic, but
its semantics may still be misunderstood.

---

## Phase 4 — Design the smallest discriminating experiment

An experiment must change one semantic variable at a time and make competing
hypotheses visibly or numerically distinguishable.

Good experiment pairs include:

- same element and size, two candidate attribute orders;
- same element, two `POS` values separated by a known distance;
- same position, two orthogonal orientations;
- same catalogue element, bound and unbound;
- same hierarchy, local `POS` versus explicit world-relative `POS`.

Each experimental macro must contain:

- one writable owner context;
- clearly separated and uniquely named test objects;
- simple, exaggerated but physically bounded dimensions;
- comments stating the expected result for each candidate;
- no unrelated equipment detail;
- a companion trial sheet listing what the user should observe or query.

Store the package under:

```
Projects/<project>/experiments/<study-id>/
    source/       preserved evidence or focused excerpt
    candidate/    generated trial macros
    results/      screenshots, query output and user verdict
    STUDY.md      hypotheses, expected observations and conclusion
```

---

## Phase 5 — E3D certification

The user loads the experiment into E3D and reports one of:

| Verdict | Meaning |
|---|---|
| Loads and geometry/attributes match expectation | Candidate may be promoted |
| Loads but geometry is wrong | Syntax is executable; spatial hypothesis is rejected |
| Fails with an E3D error | Capture exact error, line and echoed command |
| Result is ambiguous | Redesign the experiment; do not promote |

For a spatial claim, "loads successfully" is insufficient. Record the visible
or queried property that distinguishes the candidates: occupied extents,
tangent location, P-point direction, owner, catalogue reference, or another
measurable result.

Promotion to `VERIFIED` requires:

1. preserved evidence;
2. a discriminating experiment or authoritative AVEVA generator/source code;
3. exact E3D version;
4. the user's E3D verdict and date;
5. no contradiction with existing Iron Rules.

---

## Phase 6 — Write back at every affected layer

When a trial is accepted:

1. Add the exact syntax and status to
   [pml1-reference.md](../knowledge/pml1-reference.md).
2. Add or update the fast spatial mapping in
   [pml-spatial-lookup.md](../knowledge/pml-spatial-lookup.md).
3. Encode the form in the shared builder/parser; do not leave it as copied text
   in one project's output.
4. Add validation for order, required attributes, bounds and unsupported forms.
5. Add a regression test that asserts the verified property, not just the
   formula used by the generator.
6. Record equipment-placement guidance in `skill/equipment/` if the lesson says
   where the feature belongs on a real machine.
7. Record the study and user verdict in the project log.
8. If the failure generalises and is costly, amend the Iron Rules and failure
   register.

If the experiment fails, record the rejected form and symptom so it is not
proposed again. Negative evidence is reusable knowledge.

---

## Completion definition

A syntax-learning cycle is complete only when the repository can answer all of
these without reopening the original conversation:

- What model feature was studied?
- What exact native evidence was supplied?
- What does each command/attribute mean?
- Which datum and local axis does it use?
- Which order constraints matter?
- What experiment distinguished the hypotheses?
- What did E3D show, on which version, and when?
- Where is the verified form implemented and regression-tested?

