# Workflow: Querying a Live E3D Session

Some facts only exist in the user's E3D project — catalogue component names,
bores, MDB contents. This file is how to get them **in one round trip instead of
five**.

It exists because a single catalogue lookup took five attempts: `Q VAR`, `GOTO`,
`collect`, `$$MACRO` and a wrong SPCO path were all handed to the user and all
failed. Every one was avoidable by checking the installed library first.

---

## Rule 0 — verify the command exists before sending it

The user's time is the expensive resource. Before asking anyone to run anything:

```bash
grep -rlic "^\s*COMMANDNAME\b" "$AVEVA_DESIGN_EXE/PMLLIB" | head
```

Zero line-start hits across ~6900 files means the command is **invented**, no
matter how plausible it looks. `$$MACRO` had zero. So did `GOTO` as a navigation
command — it exists only as a macro label jump (`GOTO IDLN`).

Better still, find the AVEVA form that does the thing you want and read how *it*
does it (IR-11c).

---

## What the Command Window actually accepts

**PML1 single commands only.** This is the constraint that invalidated three of
the five attempts.

| Works | Fails with `(47,15) CP: Syntax error` |
|-------|----------------------------------------|
| `/path/to/element` (bare path navigates) | `collect all SPCO for ...` |
| `Q ATT` | `do !x values !list` / `enddo` |
| `Q NAME ANSWER` | `!var = ...` (PML2 assignment) |
| `$M <path>` | `$$MACRO <path>` — not a command at all |

`collect`, `do`/`enddo` and `!var =` are valid **inside a `.pmlfrm`**, which is
why they look right in the library. They cannot be pasted into the Command
Window.

### Navigation

A **bare path** sets the current element. There is no `GOTO`, no `NAVIGATE`:

```
/150lb_Ansi_Flanged/AAZFBB0KK
Q ATT
```

`!!CE = /path` also works and is what AVEVA's own PML uses internally.

Not every name is navigable: a SELEC's name resolves, a SPECIFICATION's may not.
`(2,109) Undefined name` on a path that clearly exists usually means you are
addressing the wrong level of the hierarchy.

### Querying

| Command | Returns |
|---------|---------|
| `Q ATT` | Every attribute of the current element |
| `Q NAME ANSWER` | Just those attributes — better for bulk reads |
| `Q DB` | *Not valid* — `(47,62) Incomplete command line` |

For a `SPCO`, the useful attributes are:

```
Name     /150lb_Ansi_Flanged/AAZFBB0KK   <- the SPCO path, what CATR wants
Owner    SELEC 14 of SPECIFICATION /ANSI-NOZZLES
Answer   65mm                            <- the BORE
Catref   /AAZFBB0KK                      <- NOT the SPCO; do not pass this to CATR
Tanswer  NOZZ                            <- component type
```

---

## Bulk reads: write a `.mac`, don't paste a loop

Loops cannot be pasted, but a macro file of bare-path/`Q` pairs runs fine:

```
-- list_nozzle_bores.mac
/150lb_Ansi_Flanged/AAZFBB011
Q NAME ANSWER
/150lb_Ansi_Flanged/AAZFBB033
Q NAME ANSWER
...
```

```
$M C:\full\path\to\list_nozzle_bores.mac
```

Twenty components, two lines of output each, one round trip. This is the pattern
for any bulk catalogue read.

`Projects/JK-Project/output/list_nozzle_bores.mac` is a working example.

---

## Asking the user well

The user is running the software; you are not. Treat each request as costly.

**Do:**

- Send **one** command, or one `.mac` file, per turn.
- State what the output will tell you and what you will do with it.
- Give a fallback that is known to work, in case the primary form fails.
- Warn when output may be long, and say "first 30 lines is enough".
- Ask for the **E3D alert file** (`SIR-*.txt`) on any abort — it carries the
  exact line number, command and project identity.

**Do not:**

- Send a list of commands you have not verified exist.
- Ask for "any relevant files" — name the one file and what it should contain.
- Ask for a screenshot when a numeric query would settle it, or vice versa.

### A screenshot is evidence, not decoration

Every geometry fault in the JK-Project session was identified from a user
screenshot, not from the macro. When the model is wrong in a way the generator
cannot see, ask for a picture — and read it carefully:

| What the picture shows | What it means |
|------------------------|---------------|
| Only one equipment item in the tree | Macro aborted mid-load; find the alert file |
| Element present in tree, absent in 3D | Catalogue element with nothing bound |
| Flange rim flush on the wall, no barrel | Datum inverted — `POS` is the flange face |
| Geometry flying off into space | A dimension has the wrong magnitude; bounds-check it |

---

## Reading a project's catalogue offline

Component **names** can be recovered from the catalogue databases without the
user, which saves a round trip:

```python
import pathlib, re
d = pathlib.Path(r"<project>\AvevaCatalogue\acp000")
for f in sorted(d.glob("acp*")):
    b = f.read_bytes()
    if b"ANSI-NOZZ" in b.upper():
        runs = [m.group().decode() for m in re.finditer(rb"[ -~]{4,}", b)]
        print(f.name, [s for s in runs if s.startswith("/150lb")][:5])
```

**Numeric attributes cannot** — bores are packed floats, not ASCII. Names
offline, numbers from E3D.

Locating the install: check `%AVEVA_DESIGN_EXE%` in any alert file's header. It
may differ from what is on `PATH`; one machine here had an old PDMS 12.1 on `C:`
and the live E3D 3.1 on `D:`.

---

## Checklist before sending a command to the user

- [ ] The command appears in AVEVA's installed library, or in a form that writes it
- [ ] It is a PML1 single command, or a `.mac` run with `$M`
- [ ] One request this turn, with a stated purpose
- [ ] A fallback is offered if the form is uncertain
- [ ] Expected output volume is flagged
