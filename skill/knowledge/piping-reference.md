# PIPE and BRANCH Syntax Reference

Status: **NATIVE-OBSERVED / OFFICIAL-SUPPORTED / VERIFIED / EXPERIMENTAL**.
Rounds 1 and 2 of `PML-STUDY-PIPE-001` were tested by the user in **E3D Design
Mk3.1.11.0[Z31110-056]** under AVEVA Everything3D 3.1. Exact accepted forms
are marked VERIFIED below; untested generalizations remain EXPERIMENTAL.

Evidence:

- Native export:
  `Projects/E3D_Syntax_Lab/imports/2026-07-30_pipe_native.txt`
- SHA-256:
  `A2E80B00C9B009F56260925B72FEFE4E0508006BFDC9BE374F983B9DB5437A77`
- Study:
  `Projects/E3D_Syntax_Lab/experiments/PML-STUDY-PIPE-001/STUDY.md`

---

## 1. Hierarchy

The native export and AVEVA documentation agree on:

```
SITE
  ZONE
    PIPE
      BRANCH
        ELBOW / TEE / FLANGE / GASKET / VALVE / REDUCER / ...
```

- `PIPE` is an administrative owner for branches sharing piping properties.
- `BRANCH` is the routed two-ended entity.
- Catalogue components owned by the branch define changes of direction, bore,
  connection and inline function.
- Straight variable tube is implicit between adjacent endpoints/components; it
  is not emitted as a separate `TUBE` member in this native listing.

This hierarchy is **OFFICIAL-SUPPORTED** and `NATIVE-OBSERVED`.

---

## 2. PIPE form

Observed core:

```pml
NEW PIPE /100-B-1
BORE 100mm
TEMP 50degC
PRES 0pascal
TPRESS 0pascal
PSPE SPECIFICATION /A3B
END
```

`BORE` may be omitted at PIPE level in the native export when branches carry
their own head/tail bores. `PSPE` is the piping specification and is repeated on
almost every branch. Which defaults are truly required remains EXPERIMENTAL.

---

## 3. Free BRANCH endpoints

Observed core:

```pml
NEW BRANCH /100-B-1/B1
HPOS E 0mm N 0mm U 0mm
TPOS E 4000mm N 0mm U 0mm
HDIR E
TDIR W
LHEA true
LTAI true
HBOR 100mm
TBOR 100mm
HCON OPEN
TCON OPEN
HSTU SPCOMPONENT /A3B/PA100
PSPE SPECIFICATION /A3B
END
```

| Attribute | Interpretation | Evidence state |
|---|---|---|
| `HPOS`, `TPOS` | Head/tail positions | OFFICIAL-SUPPORTED |
| `HDIR`, `TDIR` | Direction at each free end | OFFICIAL-SUPPORTED |
| `LHEA`, `LTAI` | Position-valid/fixed flags | OFFICIAL-SUPPORTED |
| `HBOR`, `TBOR` | Head/tail nominal bore | OFFICIAL-SUPPORTED |
| `HCON`, `TCON` | End connection types | OFFICIAL-SUPPORTED |
| `HSTU` | Head-side tube SPCOMPONENT | NATIVE-OBSERVED |
| `PSPE` | Piping specification | OFFICIAL-SUPPORTED |

### Shared generator support

`wsb.piping_builder` now provides `PipeSpec`, `BranchSpec` and
`PipingBuilder` for this E3D Design Mk3.1.11.0 VERIFIED free-end form. It emits:

- one `PIPE` beneath the current writable ZONE;
- one or more child `BRANCH` elements;
- explicit head/tail position, direction, bore and connection attributes;
- matching `PSPE` and optional matching `SLOREF` at PIPE/BRANCH level;
- no transaction wrapper, render prologue or catalogue component guess.

The builder bounds-checks bores and pressures, rejects coincident endpoints,
requires absolute database paths, and requires every BRANCH name to be beneath
its PIPE. After the round-2 user verdict it also exposes two deliberately
narrow component records:

- `ElbowSpec`: the tested Up-to-West form with mandatory `ARRI 2 / LEAV 1`;
- `VerticalReducerSpec`: the tested vertical form with
  `ORI Y IS N AND Z IS E`.

It still rejects multi-component routes and does not infer arbitrary component
bearings; those remain evidence-gated.

For the high-density stress package only, `NativeCatalogueComponentSpec` can
copy an explicit native block with its element type, `ORI` basis, `SPRE`,
`LSTU` and optional attributes such as `ARRI`, `LEAV`, `RLOC`, `RADI` and
`ANGL`. This is an **EXPERIMENTAL** escape hatch for a bounded catalogue
inventory test; it does not promote the copied family to VERIFIED and it does
not infer connection semantics.

---

## 4. Catalogue piping component form

Observed pattern:

```pml
NEW ELBOW
POS E 0mm N 0mm U 2000mm
ORI Y is D and Z is N
BUIL false
SHOP true
SPRE SPCOMPONENT /A3B/EA100
LSTU SPCOMPONENT /A3B/PA100
ORIF true
POSF true
END
```

Important scope rule:

- `SPRE SPCOMPONENT` is valid for piping components and `SPREF` is required by
  AVEVA's pipework documentation.
- The NOZZLE-specific rule remains different: native equipment `NOZZLE` binds
  with `CATR SPCOMPONENT` before pose.
- Never generalise a catalogue-binding command from one element family to all
  catalogue elements.

The native export contains 1,112 `SPRE` assignments. The validator was corrected
on 2026-07-30 after this evidence exposed a global NOZZLE-derived ban.

---

## 5. Component pose order

Every one of the 1,013 new piping component blocks that contains both attributes
uses:

```
POS
ORI
```

No counterexample occurs. This establishes the exporter's canonical form but
does not prove order sensitivity. Candidates 02 and 03 isolate the order:

- 02: `POS` then `ORI` — native control;
- 03: `ORI` then `POS` — single-variable reversal.

Until the user compares the E3D result, the semantic order rule is
**EXPERIMENTAL**.

> **User-tested 2026-07-30 (PML-STUDY-PIPE-001).** The native `POS → ORI`
> candidate and a single-variable `ORI → POS` candidate both loaded and placed
> the ELBOW identically. In this tested data-listing/ELBOW context, attribute
> order did not change final pose. Continue emitting the native canonical
> `POS → ORI` form, but do not claim the reverse causes drift.

Both candidates still showed dashed legs because the route was ill-defined.
This was independent of pose order.

---

## 5a. Arrive and Leave P-points

`ARRI` and `LEAV` select the component P-points used by the logical route.
AVEVA documents default Arrive 1 / Leave 2. The native ELBOW copied into the
first study explicitly carried:

```pml
ARRI 2
LEAV 1
```

The first candidates omitted these attributes and E3D displayed both legs as
green dashed lines. AVEVA defines this display as a geometrically incorrect or
ill-defined route, including bad alignment of adjacent arrive/leave directions.

> **User-confirmed 2026-07-30 (PML-STUDY-PIPE-001 candidate 06).** Restoring
> `ARRI 2` and `LEAV 1` produced a continuous solid DN100 Up-to-West route.
> Both legs met the ELBOW without the dashed/ill-defined display from round 1.

Status: tested `/A3B/EA100` Up-to-West form **VERIFIED in E3D Design
Mk3.1.11.0**. Do not generalize the same P-point numbers to every elbow
catalogue component.

---

## 6. Network connections

Observed branch-end references:

| Attribute | Role |
|---|---|
| `HREF` | Connect BRANCH head to a nozzle, tee/olet, or another branch end |
| `TREF` | Connect BRANCH tail to a nozzle, tee/olet, or another branch end |
| `CREF` | Component-side reciprocal connection to a BRANCH head/tail |

The export creates circular relationships in a later pass:

```pml
OLD TEE 1 of BRANCH /P/B1
CREF BRANCH /P/B2 TAIL

OLD BRANCH /P/B2
TREF TEE 1 of BRANCH /P/B1
```

AVEVA documentation says setting `HREF`/`TREF` also resets the corresponding
reciprocal reference. Whether both explicit lines are necessary in data-listing
input is part of the E3D trial; copying both is the conservative native form.

> **User-confirmed 2026-08-04 (PML-STUDY-PIPE-001 candidate 13).** The
> two-pass form works end to end: `Q ATT` on the TEE returned
> `Cref /CODEX-Q13-TEE/B2`, closing the round-1 loop where only B2's `TREF`
> had been confirmed. Both explicit lines (TEE `CREF` and B2 `TREF`) are
> emitted and verified; keep the native shape rather than relying on
> implicit reciprocal reset.

## 6a. GASKET is a zero-thickness joint marker (tested /A3B/GC20)

`Q ATT` on `GASKET 1 of BRANCH /CODEX-Q13-GASKET/B1` (candidate 13,
2026-08-04) returned:

| Attribute | Value |
|---|---|
| `Spref` | `/A3B/GC20` |
| `Arrive` / `Leave` | 1 / 2 |
| `Height` | 0mm |
| `RLOC` | absent from Q ATT (unset) |

The tested gasket carries **no real thickness** (`Height 0mm`): it is a
flange-joint marker that occupies the interface plane and contributes no solid
volume. It is bounded by P-points like any inline component (Arrive 1 /
Leave 2). Do not model a gasket as a solid disc in piping routes; the
catalogue component is already the thin joint representation.

---

## 7. Slope

Native pipes and branches carry references such as:

```pml
SLOREF SLOELE /1in100
```

The native export also represents a 1:200 run with directions such as
`E 0.2865 D`, consistent with the angle of a 1-in-200 slope. Candidate 05 tests
the `/1in100` reference together with a 100 mm fall over 10,000 mm.

> **User-tested 2026-07-30 (PML-STUDY-PIPE-001).** A 10,000 mm run falling
> 100 mm displayed correctly, and both PIPE and BRANCH returned
> `Sloreference /1in100`.

Status: **VERIFIED in E3D Design Mk3.1.11.0** for the tested 1:100 form.

---

## 7a. Piping component axes are not primitive axes

The round-1 REDUCER used `ORI Y is E and Z is U` and appeared on the
North/South axis, while the BRANCH was vertical. Native evidence confirms that
this basis belongs to North/South two-way components.

Multiple native vertical REDUCER instances instead use:

```pml
ORI Y is N and Z is E
```

This demonstrates why the primitive rule "axis of revolution is Z" must not be
applied to catalogue piping components. Their route axis is determined by
catalogue P-points/local axes.

> **User-confirmed 2026-07-30 (PML-STUDY-PIPE-001 candidate 07).**
> `ORI Y IS N AND Z IS E` placed `/A3B/RC100X80` vertically and made both
> adjacent legs solid and coaxial. The branch visibly transitioned from
> HBOR 100 mm to TBOR 80 mm.

Round-1 primitive-axis hypothesis: `REJECTED`. Tested vertical native-axis
form: **VERIFIED in E3D Design Mk3.1.11.0**.

---

## 7b. Syntax-weight balance

Choose syntax by engineering intent and evidence strength, not by familiarity:

| Intent | Preferred family |
|---|---|
| Connectable process route | Native `PIPE` / `BRANCH` / catalogue components |
| Equipment connection point | Catalogue-backed `NOZZLE` |
| Vessel shell or justified solid body | Primitive `CYLI` / `CONE` / `BOX` / `DISH` |
| Visual-only pipe representation with no receiving catalogue | Primitive approximation, explicitly labelled non-connectable |
| Unsupported catalogue geometry | Isolated experiment first; never replace it silently with the most familiar syntax |

“Balanced” does not mean forcing equal element counts. It means no syntax
family receives an artificial default weight. Project data and user intent
select the feature; evidence status selects the safest implementation.

---

## 8. Deferred advanced forms

These are observed but not yet interpreted sufficiently for generation:

- `VTWAY` and multi-way reciprocal networks beyond the verified OLET/TEE pairs;
- `RPLANE`, `RPLGROUP`, `STRUCTURE` and Router commands;
- insulation/tracing specs, fluid and pressure inheritance;
- `INPRTR`/`OUPRTR` metadata.

Do not use these in production until each has an isolated study and user verdict.

## 8a. Advanced families — VERIFIED native slices (2026-08-04)

Candidates 14-16 (generated verbatim from the native export by
`build_advanced_candidates.py`) were loaded by the user in E3D Design
Mk3.1.11.0; every component family displayed correctly:

| Family | Candidate | Notes |
|---|---|---|
| FILTER, CLOSURE, FBLIND, COUPLING, WELD | 14 | All `/A3B`; weld gaps `/WELDGAP` resolved |
| BEND (incl. 45° `ANGL`), OLET, PTAPPING + PIPCARTESIAN | 15 | `/General-Tappings/TAPPING-200mm` resolved |
| OLET↔B2, TEE2↔B3 reciprocal network + PSPOOL/PPLIST/PPIECE | 16 | Internal two-pass references only; routes connected |

CAP is **GATED**: every native CAP sits under `/FIRE`, which the receiving
project does not define (`(2,109) Undefined name /FIRE`). CAP cannot be
certified until `/FIRE` exists; do not substitute another component for it.

These verdicts certify the exact native forms tested, not every catalogue
path of the same element type — a different project's catalogue must be
verified family by family.
