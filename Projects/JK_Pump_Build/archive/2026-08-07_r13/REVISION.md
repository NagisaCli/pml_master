# Revision record — r13 (2026-08-07)

Status: **awaiting E3D visual reload** (IR-13a).

Fixes the two defects the client reported after loading r12.

## Deliverable

- `output/JK_Pump_Build_refined_20260805_r13.pml`
  - SHA-256: `3228272162761505CC259DB816B1C4587F3FB7497132AB8E29B7EF623B89ADBC`
  - Lines: 76,256; 30 EQUI / 360 SUBE / 6,763 primitives
- Tools: `tools/rebuild_base_r13.py`, `tools/verify_r13.py`

Baseline: r12 (its pedestals and bearing elevations are correct and are kept
byte-identical; r13 adds the casing feet and re-places the fasteners).

## bug 1 — "collision between the bolts and the support legs"

Measured in r12: **1,700 intersections** between fastener solids and
pedestal/plate solids, on all 30 pumps. The r12 anchors sat on each plate's
long centreline, which is exactly where the pedestal webs run.

Root cause of the first failed fix attempt, worth recording: the clearance
test was written as

```python
overlap > clear          # WRONG
```

so a 1.9 mm interference passed a 2.0 mm "clearance" check. The parameter was
inverted — `clear` must *grow* the test box, not license overlap:

```python
overlap > -clear         # correct
```

With that corrected, and with `is_vertical()` shared between the generator and
the verifier (they had drifted to 40 mm / 60 mm thresholds and disagreed about
which members were obstacles), the count went 1,700 → 466 → **0**.

`is_vertical()` also now requires height > thinnest plan dimension, so a long
flat cross-beam (454 × 40 × 33) is correctly treated as something a hold-down
passes through, not something it must dodge.

### Bolt POSITIONS — a second defect found after the first fix

The client then noted "that could be some errors with the position of bolt".
Correct: **zero collisions only proves the bolts miss the steel, not that they
are anywhere sensible.** A positional audit of the first r13 attempt found:

- 84 bolts hanging off the edge of the plate they clamp (two 0.2 mm past it);
- 180 bolt groups off-centre — worst case four bolts crammed into the top
  15 mm of a 160 mm plate;
- 3 pumps with mixed patterns (2 bolts on two feet, 4 on the others).

Cause: the placement search was allowed to slide the pattern off-centre to
dodge steel, and scored only "widest spread", so a bunched, edge-hugging
layout could win. Patterns are now **symmetric about the plate centre by
construction** and required to sit fully inside with a ≥1.5·d edge distance.

That alone dropped coverage to 48/120, which exposed the real problem:
measured across all 30 pumps, the r12 pedestal webs run to within **4 mm of
the bearing-plate ends** and span its full width. There is physically nowhere
on the bearing plate for a 17 mm bolt — every earlier "solution" was contorting
around geometry that had no room in it.

The structural answer, and what real fabricated pedestals do: the hold-downs
go through the pedestal's **bottom flange**, which projects ~8 mm beyond the
bearing plate on all four sides, sits on the frame top, and is clear of the
webs. Both ends are now bolted this way.

An intermediate attempt — shortening the webs to open a bolt zone on the
bearing plate — was **reverted**: it broke the support chain, reintroducing
44 mm voids under the plates. Trimming a stiffener to make room for a bolt is
not worth losing the support the pedestal exists to provide.

## bug 2 — "not an effective support / no proper interface to the pump body"

Measured in r12: the casing is a horizontal barrel of radius R whose axis is
the pump centreline. The bearing plates sit ≈0.91·R either side of that axis,
i.e. under the barrel's steeply curved flank. A flat plate meeting a round
barrel there touches along a tangent sliver — there was no foot bringing the
casting down to a flat machined face, so the pump was resting on a line, not
a surface.

r13 adds a cast **casing foot** on every pump-end pedestal (120 total):

```
        )        <- barrel flank (round)
       /|
      / |        <- cast rib, reaches up into the casting
     +--+        <- flat machined sole pad, underside = pedestal plate top
     ====        <- pedestal plate (r12, unchanged)
```

- the machined sole pad matches the pedestal plate footprint exactly, so the
  base/pump interface is flat-on-flat over the whole plate;
- the rib rises from the pad to the computed barrel surface height at its own
  lateral offset, plus 14 mm, so it visibly merges into the casting instead of
  stopping in mid-air;
- the rib spans 45% of the pad, leaving the pad ends clear for the bolts.

## Verification (`tools/verify_r13.py`)

- **0 bolt/structure collisions** (1,856 fastener solids checked against every
  vertical member of SUPPORT_FRAME, DRIVER and CASING);
- **bolt positions**: 0 bolts off the edge of the flange they clamp, 0
  off-centre groups, edge distance ≥1.4·d, uniform pattern per pump;
- 120 flat casing-foot interfaces, one per pump-end pedestal plate;
- 88 casing-foot ribs, each reaching the barrel surface;
- 120 support chains continuous, **0 voids** (independent r12 audit re-run);
- 210 locked blocks byte-identical; SUPPORT_FRAME unchanged from r12;
- nozzles (60) and CATR (60) unchanged; INPUT block stack balanced;
- `verify_r12.py` still passes in full (240 bearing interfaces in contact);
- project suite: 288 passed, 2 skipped.

## Bolt coverage

| interface | bolted |
|-----------|--------|
| pedestal flanges (pump + motor) | 234 / 240 |
| bolts placed | 928 (464 pump + 464 motor) |

The 6 unbolted flanges are on **203-PU-020**, where a neighbouring low casing
detail occupies the flange's clear zone. Rather than draw bolts through steel
(the original defect), r13 omits them and reports it.

## Open items

- **IR-13a** — E3D visual reload. What to look at: each pump foot now has a
  cast foot with a flat pad seated on its pedestal; the hold-downs pass
  through the projecting pedestal flange, symmetric and clear of every web.
- 203-PU-020: 6 flanges unbolted (above).
- `PUMP_MID_LINE.txt` centreline values remain reported, not applied (see the
  r12 record) — unchanged by this revision.

## Lessons

- **A clearance parameter must be sign-checked against a known interference.**
  `overlap > clear` reads naturally and is exactly backwards; it silently
  permitted every near-miss it was written to prevent. Test a clash routine on
  a pair you *know* overlaps before trusting a "0 collisions" result.
- **A generator and its verifier must share one definition of the thing they
  disagree about.** Two copies of `is_vertical` with different thresholds meant
  the generator considered a member harmless and the verifier flagged it. The
  fix was to import one function, not to re-tune two.
- **A flat plate under a round barrel is not a support.** Bearing contact needs
  a matched flat face on both sides; a tangent line passes a naive contact test
  while reading, correctly, as "floating" in E3D.
- **Derive clash obstacles from the geometry actually emitted.** Computing the
  emitted rib and its obstacle box separately let them disagree.
- **"Clash-free" is not "correct".** A bolt can miss every member and still be
  hanging off a plate edge or bunched at one end. Fasteners need positional
  properties of their own — inside the part, symmetric about it, sane edge
  distance, same pattern on matching feet — and those are now verified.
- **When a placement search keeps needing exceptions, the host geometry is
  wrong, not the search.** Six attempts at fitting bolts onto the bearing
  plate all failed because the webs left 4 mm of room. Measuring the available
  space first would have pointed at the projecting flange immediately.
- **Do not trade away a property you already proved to buy a new one.**
  Shortening the webs made room for bolts and silently reopened 44 mm voids
  under the plates; it was reverted.
