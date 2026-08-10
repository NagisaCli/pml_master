# Revision record — r12 (2026-08-07)

Status: **awaiting E3D visual reload** (IR-12a).

Scope: foundation/base geometry only. Pump positions, nozzle locations and
baseplate overall dimensions are unchanged, as instructed.

## Deliverable

- `output/JK_Pump_Build_refined_20260805_r12.pml`
  - SHA-256: `A505FAF663392C35EE2B9C244D1D08752D59112B84595B8D4631137F010EC320`
  - Lines: 57,778; 30 EQUI / 360 SUBE / 5,659 primitives
- Tools: `tools/rebuild_base_r12.py`, `tools/verify_r12.py`

Baseline: **r8**, not r11. r9/r10/r11 were all client-rejected; r11's own
record closes the thread. Building further on r11 would have inherited the
defect that caused its rejection.

## The defect that actually caused the r11 failure

The client's verdict on r11 was "the base support and the pump/motor are
completely separated". A footprint-aware measurement of the bearing
interfaces explains it exactly:

| file | pumps with a defective bearing interface |
|------|------------------------------------------|
| r8   | **0 / 30** |
| r11  | **30 / 30** (gaps of 40.7 – 112.6 mm) |

r11 replaced each sole plate with a shorter bracket stack (bottom block +
diagonal web + middle plate + diagonal web) and never re-reached the machine
foot. Its verifier reported "0 floating base elements" because it only tested
contacts *inside* the base assembly — never the assembly's contact with the
casing or motor. That is the blind spot the r11 failure record itself
identified, and it is now closed by `verify_r12.py`.

### Why the earlier "casing embeds into the sole plate" reading was wrong

Comparing a sole-plate top against the globally lowest casing solid reports a
7–26 mm interference on all 30 pumps. That is an artefact: the lowest casing
solid is a small drain/seal-flush stub hanging below the barrel, well outside
the sole-plate footprint. Measured footprint-aware (only solids actually over
the plate), r8's interfaces are correct to within 0.1 mm. Any future bearing
check must be footprint-aware.

## The genuine foundation defect that r12 repairs

Present in r8 and inherited by every later revision — the pedestals were
decorative, not structural:

- **60 / 60 support interfaces had a void** of 10.5 – 54.3 mm between the top
  of the PYRAMID gussets and the underside of the bearing plate they were
  supposed to carry. Every sole plate and motor pad hung in mid-air.
- **59 / 60 gussets were buried** below the frame top, their bottoms sunk
  2.9 – 54.3 mm into the frame rails or the baseplate itself.

So the machine sat correctly on its plates, but the plates were connected to
nothing. In E3D this reads as a floating pump train over a decorative skid.

## What r12 changes

Per pump foot and motor pad (240 pedestals total), the 480 PYRAMID gussets
are replaced by a fabricated plate-girder pedestal that fills the void
exactly:

```
    +----------------------+  <- bearing plate (UNTOUCHED, r8 position)
    |  web    stiff   web  |     pedestal webs, full clear height
    +======================+  <- bottom flange, seated on the frame top
    ========================  <- frame rail on the baseplate
```

- bottom flange (12 mm, 8 mm oversize each side) seated **on** the frame top;
- two vertical web plates (10 mm) running the full depth under the plate
  edges, oriented along the long axis to resist machine thrust;
- one transverse stiffener tying the webs at mid-length;
- 480 hold-down anchors: shank from inside the frame through the plate, hex
  nut seated **on the plate top**.

Heights are derived per foot from the measured plate underside, so the pump
end and motor end take different pedestal heights naturally — the flaw in
r9–r11 was assuming one height for both.

**The bearing plates themselves are never moved.** r8 already places every
bearing surface exactly on its machine foot; moving them is what destroyed
r11.

## Verification (`tools/verify_r12.py`)

All checks pass:

- 120 pump-end and 120 motor-end bearing interfaces in contact (≤0.6 mm),
  measured footprint-aware against the casing/bearing-frame and motor feet;
- 240 support chains continuous from baseplate → frame → flange → webs →
  bearing plate, with **0 voids** and **0 buried elements**
  (independently reproduced: r8 60 voids / 59 buried → r12 0 / 0);
- 0 PYRAMID gussets remaining; lowest point U 0;
- 240 locked blocks byte-identical; non-base canonical SHA-256
  `a08d84df…cceba` identical between r8 and r12;
- baseplates, nozzles (60) and CATR pass (60) unchanged;
- INPUT block-stack replay balanced, identical to r8 (F-18 regression);
- project suite: 288 passed, 2 skipped.

## Open items

- **IR-12a** — E3D visual reload and client confirmation. The specific thing
  to look at: each pump foot and motor pad now stands on a visible pedestal
  (flange + two webs) that reaches the frame, with the hold-down nut on the
  plate top.
- `PUMP_MID_LINE.txt` shaft-centreline values are **not applied** — see below.
- MC_AUXILIARY remains temporarily absent on the five MC pumps (unchanged
  from r8).

## PUMP_MID_LINE.txt — reported, not applied

| tag | requested | current | delta |
|-----|-----------|---------|-------|
| 203-PU-020 | 840 mm | 278.3 mm | −561.7 |
| 205-PU-018 | 640 mm | 389.9 mm | −250.1 |
| 205-PU-038 | 640 mm | 392.3 mm | −247.7 |
| 204-PU-028 | 600 mm | — | not in the 30-pump scope |
| 205-PU-056 | 660 mm | — | not in the 30-pump scope |

Reaching these centrelines requires raising each pump by 248–562 mm, which
moves the casing, the shaft and both nozzles. That contradicts the standing
instruction to keep pump positions and nozzle locations unchanged, so it was
not applied as an opportunistic refinement. It needs an explicit decision:
if the pumps are genuinely to be raised onto tall pedestals, the nozzle
elevations and connected piping must move with them.

`204-PU-028` and `205-PU-056` do not exist in `Pump_details.xlsx` and were
left alone per the client's instruction.

## Lessons

- A support chain verified only *inside* the base assembly proves nothing.
  Anchor every bearing test to the machine it carries — r11 passed its own
  checks and still failed visually for exactly this reason.
- Bearing checks must be footprint-aware. Drain stubs and flush lines hang
  below a pump barrel; comparing against the globally lowest solid invents
  interference that is not there and hides the real defect.
- When a client rejects several revisions in a row, re-measure the last
  accepted baseline before extending the newest attempt. Here the rejected
  chain r9→r11 had drifted away from a baseline whose interfaces were
  already correct; the fix was to return to r8 and repair the one thing that
  was genuinely broken.
- "Nothing floats" and "everything is connected" are different properties. r8
  had no floating *elements* by its own test, yet all 60 of its support
  interfaces were voids.
