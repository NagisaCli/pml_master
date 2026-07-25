# Catalogue Elements — NOZZLE and friends

**Status: VERIFIED on AVEVA E3D Design Mk3.1.11.0**, against a live project
catalogue and AVEVA's installed PML library.

A **catalogue element** is not a primitive. It has no dimensions of its own: its
geometry comes from a `SPCO` (specification component) in the project catalogue.
`NOZZLE` is the one this project uses; `FLANGE`, `SCTN` and piping components
behave the same way.

This distinction causes a whole class of failures that primitives never produce,
because a catalogue element can exist, report a correct position, pass every
geometric check — **and draw nothing at all**.

---

## The five rules, in the order they bite

| # | Rule | Failure if broken |
|---|------|-------------------|
| 1 | Bind a component, or nothing renders | Invisible nozzles, no error |
| 2 | Bind it FIRST, inline | `(2,360)` abort, partial model |
| 3 | Use the SPCO's own path | `(2,108) ... is not a SPCO` |
| 4 | Aim by P-point, not a geometric axis | Nozzles point the wrong way |
| 5 | `POS` is the flange face | Barrel buried inside the vessel |

Each is expanded below. All five were shipped as bugs in one project; four of
them loaded without any error message.

---

## 1. A NOZZLE draws nothing until a component is bound

```
NEW NOZZLE /203_TA_006_N1_NOZZ
POS ...
ORI ...
HEIG 450
END
```

This is a valid nozzle. It sits in the Model Explorer, reports the right
position, and **renders nothing** — the flange, bore and face position all live
in the catalogue component it does not yet have.

The symptom reads as "the nozzles are not displaying", which sounds like a
rendering or graphics problem. It is not: the element is empty.

> **Anti-lesson.** An earlier fix hit `(2,109) Undefined name` from an inline
> `SPRE SPCOMPONENT`, and concluded the reference should be dropped. Removing a
> reference that will not resolve does not make the element correct — it makes
> it empty. When a reference fails, fix the reference.

---

## 2. Bind FIRST — `CATR` before `POS` and `ORI`

A nozzle's P-points *and its position* come from the component. Until one is
bound there is nothing to position and no P1 to aim.

```
CORRECT                                      WRONG
NEW NOZZLE /...                              NEW NOZZLE /...
CATR SPCOMPONENT /150lb_Ansi_Flanged/...     POS ...
POS ...                                      ORI P1 IS N     <- aborts here
ORI P1 IS N                                  ... CATR later ...
HEIG 450
```

```
(2,360)   Cannot get position of NOZZLE /203_TA_006_N1_NOZZ
Command: ORI P1 IS N
```

**Evidence.** AVEVA's creation form sets the catref as the statement straight
after `NEW NOZZ` — `!!ce.catref = !this.nozzSpecRef` (`equnozzle.pmlfrm:894`),
before height, temperature or anything else.

**The trap.** The `OLD` / `CATR` pass at `SMLdataPlant.pmlmac:13733` looks like a
creation idiom:

```
OLD /SML/HO9007/N1
CATR SPCOMPONENT /DICHTFL_C/ND-16RF-150
```

It is a **rebinding** of nozzles that already have a component. Copying its shape
put the binding at the end of the macro, which aborted the first nozzle and
**stopped the whole load at the first equipment item** — 21 of 22 tanks silently
absent.

A nozzle with no component must also carry **no `ORI`**: there is no P1 to aim.

---

## 3. `CATR SPCOMPONENT` takes the SPCO's own path

`Q ATT` prints two similar-looking references one line apart:

```
Name   /150lb_Ansi_Flanged/AAZFBB0YY   <- the SPCO: what CATR wants
Catref /AAZFBB0YY                      <- what the SPCO itself points at
```

Passing the second gives:

```
(2,108)   SCOMPONENT /AAZFBB0YY is not a SPCO
```

The path is always two segments, `/<selec>/<component>` — matching AVEVA's own
`CATR SPCOMPONENT /DICHTFL_C/ND-16RF-150`.

Note the SELEC name (`150lb_Ansi_Flanged`) is **not** the specification name
(`/ANSI-NOZZLES`). It comes from `Q ATT`'s `Owner SELEC 14 of SPECIFICATION
/ANSI-NOZZLES` line. The specification is not itself navigable as a path.

---

## 4. Aim by the P-point

```
CORRECT   ORI P1 IS N
WRONG     ORI Y is N and Z is U      -- points somewhere other than the bore
```

See [IR-2](iron-rules.md#a-nozzle-is-aimed-by-its-p-point-not-by-a-geometric-axis)
for the evidence and the misreading that produced it.

---

## 5. `POS` is the FLANGE FACE, not the root

The barrel runs **back** from `POS` toward the vessel:

```
POS radius = shell_face − penetration + nozzle_length
```

Placing `POS` on the shell face buries the entire barrel inside the vessel, with
only the flange rim emerging. See
[IR-9a](iron-rules.md#a-nozzles-pos-is-its-flange-face-not-its-root-on-the-shell).

---

## Reading a catalogue: the procedure

**Never infer component names from their codes.** In the AVEVA sample catalogue
the nozzle SPCOs are `AAZFBB0xx`, and the bore ordering defeats every reasonable
guess:

```
AAZFBB011 = DN500     <- the two LARGEST bores come FIRST
AAZFBB033 = DN600
AAZFBB0DD = DN15      <- then the ladder restarts at the smallest
AAZFBB0MM = DN90      <- a bore not in the standard ANSI series
```

Three ordering hypotheses were tested against known points; all three failed. A
wrong guess binds the wrong flange to a real connection and still loads cleanly.

### Step 1 — find the family

Scan the catalogue databases for the specification name:

```python
import pathlib
d = pathlib.Path(r"<project>\AvevaCatalogue\acp000")
for f in sorted(d.glob("acp*")):
    if b"ANSI-NOZZ" in f.read_bytes().upper():
        print(f.name)
```

ASCII runs in those binaries give the SELEC and component names. **Numeric
attributes are packed floats and are not readable this way** — bores must come
from E3D itself.

### Step 2 — read the bores from the live model

Write a `.mac` of bare-path/`Q` pairs (see
[querying-e3d.md](../workflows/querying-e3d.md)) and run it with `$M`:

```
/150lb_Ansi_Flanged/AAZFBB0KK
Q NAME ANSWER
```

`Answer` is the bore. `Tanswer NOZZ` confirms it is a nozzle component.

### Step 3 — store the mapping, and mark it project-specific

`wsb.pml_builder.NOZZLE_BORE_COMPONENTS` holds the result. **These names are a
property of the receiving catalogue, not of the model.** Re-read them for any
other project; never assume they carry across.

---

## Bores the catalogue does not carry

Report them; do not approximate.

The JK-Project DN800 bottom outlet has no 150lb component — that family stops at
DN600. It is created and positioned but left unbound, with an explicit note in
the macro. Silently binding it to the DN600 component would put an under-sized
flange on a real connection, read as correct downstream, and mislead the piping
designer. An unbound nozzle is visibly missing; a wrong one is not.

---

## Checklist for any catalogue element

- [ ] A component is bound, or the element is explicitly reported as unbound
- [ ] `CATR` precedes `POS` and `ORI` in the block
- [ ] The path is the SPCO's own `/<selec>/<component>`, two segments
- [ ] Component names were **read from the catalogue**, never inferred
- [ ] Bores with no component are reported, not downsized
- [ ] The mapping is marked project-specific and re-read for a new project
