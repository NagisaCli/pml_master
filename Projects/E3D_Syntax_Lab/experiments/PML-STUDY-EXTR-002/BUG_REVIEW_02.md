# Bug Review — PML-STUDY-EXTR-002 candidate 02

Date: 2026-08-05. Source candidate: `candidate/02_high_fidelity_pump.pml`
(SHA-256 `341D2E56...B8F9`). All findings below were reproduced numerically
by parsing the emitted macro and re-deriving occupied ranges from each
element's own datum; none of them is a visual guess.

---

## Bug 1 — Motor terminal-box mounting ears float above the frame

**User symptom:** "the two small pieces on top of the motor terminal box" are detached / physically
impossible.

**Numerical finding:**

| Item | U range | Result |
|---|---|---|
| Terminal-box ear (N +-90..110) | U 590..610 | bottom 590 |
| Motor frame outer surface at N 100 | U = 400 + sqrt(210^2 - 100^2) = 584.66 | top 584.66 |

The ear bottoms sat at U 590, which is **5.3 mm above** the frame's curved
top at that N. There was no overlap, no embedment, no bolt, and no visible
support — two small blocks hanging in air beside the terminal box.

**Root cause:** the ears were placed at a fixed height (U 590) that was
chosen without computing the frame's actual outer surface at their N
position. The generator used a flat height constant instead of deriving it
from the frame profile.

**Fix (candidate 03):** the box is now mounted on four cast pads that are
part of the motor frame package. Each pad bottom (U 578) is computed to be
below the frame outer surface at its N position (581.8), so it embeds into
the frame by ~4 mm; the box ears sit exactly on the pad tops (U 608), and
four through-bolts pass through ear and pad.

---

## Bug 2 — Volute side ribs appear as floating chips

**User symptom:** "there are also four small floating pieces around the casing".

**Numerical finding:** the four ribs were emitted with their inner edge
radius exactly equal to the volute wall radius at their angle
(r(theta) = 190 + 90*theta/360, contact-only). The rib was only 10 mm thick
in E, so each rib touched the volute end face along a single edge and
visually detached.

**Root cause:** ribs were sized as "touch the wall" (zero clearance) instead
of "grow out of the wall" (embedment). With no overlap the rib reads as a
separate floating chip wherever the spiral curvature changes.

**Fix (candidate 03):** 36 ribs (18 per end face) with inner radius
r(theta) - 6 mm, so each rib is embedded 6 mm into the volute wall; ribs
are also thicker (16 mm) and taller (70 mm), reading as cast stiffeners.

---

## Bug 3 — Cross beam floats as an unexplained block

**User symptom:** "that BEAM in the middle has no obvious purpose and just looks odd as a block".

**Numerical finding:** the three cross beams were identical H-sections at the
same height as the longitudinal beams (U 0..100), running N -170..170. They
crossed the longitudinal beams at N +-110..230 with the same top surface, so
there was no visible load path or lap joint — just a bar intersecting the
frame.

**Root cause:** cross members were modelled with the same height and
zero-lap geometry instead of sitting between the main beams. Nothing showed
how they connect.

**Fix (candidate 03):** cross beams are now lower (U 0..80) with their ends
lapping into the main-beam web zone (N +-110..200), exactly like a welded
frame member; two end cross beams and two mid cross beams form a clear
grid.

---

## Bug 4 — Profile resolution too low

**User symptom:** "the face count is too low, which makes it look a bit rough".

**Numerical finding:** circle profiles used 24 vertices, the volute spiral
used 19, the motor frame used 48, grille bars 6. The total EXTRUSION vertex
count of candidate 02 was 1171.

**Fix (candidate 03):** circles 48 vertices, volute spiral 48, motor frame
24 fins (144 vertices), end shields 16-24 ribs, 72 rotor bars, 108 winding
end-coil segments, 60 fan-shroud grille bars, and a target total vertex
count above 30 000 (about 25x candidate 02).

---

## Bug 5 (scope) — No internal drive train

**User symptom:** request to model the internal structure: a complete,
physically consistent drive train and true appearance.

**Fix (candidate 03):** closed impeller (front/back shrouds + 14 curved
blades), stepped shaft, mechanical seal stack, rolling bearings with
rollers, labyrinth rings, pump cover with bolted joint, jaw coupling with
toothed hubs and star spider, squirrel-cage rotor (24 lamination segments,
72 bars, end rings), stator (24 segments, 108 winding end coils, 72 slot
wedges), motor bearings, fan with 20 blades, and a guarded coupling.

Reference sources used for component structure (all cited in STUDY.md):
Grundfos end-suction pump module; EASA squirrel-cage rotor design;
Firgelli jaw-coupling mechanism; CFturbo volute geometry; Goulds 3180 IOM
(bearing frame, labyrinth seals).
