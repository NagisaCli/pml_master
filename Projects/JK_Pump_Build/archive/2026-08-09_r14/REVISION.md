# Revision record — r14 (2026-08-09)

Status: **awaiting E3D visual reload** (IR-14a).

Fixes the frame defect the client reported after loading r13 (screenshots of
the pump-end pedestal and the base structure).

## Deliverable

- `output/JK_Pump_Build_refined_20260805_r14.pml`
  - SHA-256: `bddf254c850882d08b2c01da4fa6007329fb147c4d8566ca9d886b59a1c897c7`
  - Lines: 76,256 (unchanged from r13 — this revision edits attributes only)
- Tools: `tools/rebuild_base_r14.py`, `tools/verify_r14.py`

Baseline: r13, chosen after measurement rather than assumption. r13's
pedestals, casing feet and hold-downs measured correct; the defect was
elsewhere.

## First: r13 was never written to disk

The r13 record described a deliverable with a SHA-256 and 76,256 lines, but
`output/` contained no r13 `.pml` — only the generator and verifier. The
client was loading **r12** while reading the r13 record. Regenerating from
`tools/rebuild_base_r13.py` reproduced the recorded hash
`3228272162761505…3b89adbc` bit-for-bit, so the record was honest about
content; the file had simply never been emitted. It exists now.

**Process lesson: a revision record must not be written until the artefact it
describes is on disk and re-hashed from it.**

## What the client's screenshots actually showed

Two complaints, and the first diagnosis of both was wrong. Recording the
error because it is the same failure mode as r11:

| read from the render | measured reality |
|---|---|
| "a bolt is lying horizontally" | **motor cooling fins.** 856 long horizontal cylinders (Ø15–26, 480–800 mm) in `DRIVER`, identical count in r8/r12/r13. No hold-down is misoriented: all 464 base + 464 driver anchors are long-axis U. Confirmed with the client as intended motor detail — left alone. |
| "the pedestals are a jumble of blocks" | **the pedestals are clean.** Per foot: flange 126.8×176.2×12 (U 70→82), two webs 10×152.2×57.8 (U 82→139.8), stiffener, bearing plate (U 139.8→155.8). Exactly as the r13 record describes. |

Diagnosing from a render before measuring produced two confident, wrong
causes. The screenshots were genuine evidence of a bad-looking model, but not
of the thing they appeared to show.

## The real defect — one number, wrong since r8

The rails are a clean datum: every rail is U 50.0 → **70.0**, and every
pedestal flange starts at exactly U 70.0.

The cross-beams are not. All start at U 50 but their tops ran to
U 82.6 – 111.2 — **13 distinct top elevations, 12–41 mm above the rail top
they should be flush with**. Fleet-wide that produced 412 interpenetrating
member pairs:

| pair | count | meaning |
|---|---|---|
| rail × xbeam | 202 | beams sunk 20 mm into the rails |
| **web × xbeam** | **134** | beams punching up into the pedestal webs |
| **flange × xbeam** | **60** | beams punching through the pedestal flange |
| plate × xbeam | 10 | beams reaching the bearing plate |
| xbeam × xbeam | 6 | beams crossing each other |

**194 of those were cross-beams driven 6.8–12 mm into the pedestals that carry
the pump** — the beam occupying the same space as the support. That is the
"not an effective support" reading, and it is a structural error, not a
cosmetic overlap.

No support revision ever touched it: r9–r13 all rebuilt the pedestals and left
the frame exactly as r8 emitted it.

## What r14 changes

Every cross-beam top is set to its pump's rail datum (U 70.0), so beams frame
*between* the rails and the pedestals sit on a flat, continuous frame top.
Plan position, thickness and length are untouched — only `ZLEN`/`HEIG` and the
`POS` U component move. 104 beams trimmed, 2,405 mm of material removed.

`203-PU-020` is a short skid whose longest member is 759 mm, below the 1 m
rail threshold. `rail_datum()` falls back to the longest members present
rather than special-casing the tag.

**Nothing else is touched**: 208 changed lines, all inside `SUPPORT_FRAME`;
the non-frame canonical hash is identical to r13.

## Verification (`tools/verify_r14.py`)

- **0 pedestal/plate clashes** (was 204);
- 208 rail/beam T-joints at crossings — counted and **allowed**: a beam framed
  between rails shares the rail depth at the joint, which is how a fabricated
  skid is detailed. Forcing these to zero would mean fragmenting every beam;
- **0 beams above the rail datum** (was 104); one beam-top elevation per pump;
- **0 non-vertical hold-down shanks**;
- 112/112 pedestal flanges seated, **0 voids**;
- non-`SUPPORT_FRAME` scope byte-identical to r13;
- r13's checks re-run on r14: 0 bolt/structure collisions (1,856 solids),
  120 casing-foot interfaces, 88 ribs, 120 support chains, 210 locked blocks;
- r12's checks re-run on r14: 240 bearing interfaces in contact, 240 support
  chains, 210 locked blocks;
- project suite: **288 passed, 2 skipped**.

The clash routine was **self-tested against known-bad geometry** before its
"0" was trusted: pointed at r13 it reports 204 clashes and 104 off-datum
beams, and exits non-zero. (r13's lesson — a clearance sign error once made
`overlap > clear` pass every near-miss it existed to catch.)

## Open items

- **IR-14a** — E3D visual reload. What to look at: the cross-beams now stop
  flush with the rail tops instead of rising through the pedestals; each
  pedestal sits on a flat frame top.
- 203-PU-020: 6 flanges still unbolted (carried from r13).
- `PUMP_MID_LINE.txt` centrelines remain reported, not applied (see the r12
  record) — unchanged.
- MC_AUXILIARY still absent on the five MC pumps (carried from r8).

## Lessons

- **Do not diagnose from a render.** Two defects were named from the
  screenshots and both were wrong — the "sideways bolt" was motor detail and
  the "jumbled pedestal" was the one clean assembly in the picture. A
  screenshot proves something looks wrong, never what is wrong.
- **"In contact" is not "coherent".** Every check through r13 asked *is there
  steel beneath this?* An AABB touch test is satisfied just as well by a heap
  of overlapping boxes as by a designed pedestal. Interpenetration and datum
  consistency are separate properties and needed their own tests.
- **Check what no revision has touched.** Five consecutive revisions rebuilt
  the pedestals because that is where the complaint pointed; the fault was in
  the frame beneath them, unchanged since r8 and never once measured.
- **A classification threshold is a hidden assumption.** The 1 m rail cut-off
  silently excluded one pump from the fix and reported it as "no rail" — the
  model was fine, the constant was not.
