# Equipment Prototype Knowledge Base

What each class of equipment **looks like** and **how it is built** — so that
when project data is incomplete, defaults are reasoned rather than invented.

| File | Covers |
|------|--------|
| [tanks-and-vessels.md](tanks-and-vessels.md) | Tank-type equipment: roofs, bottoms, supports, nozzles, platforms |
| [fibreline.md](fibreline.md) | Washing, screening, bleaching, pulping, recovery |
| [paper-machine.md](paper-machine.md) | Fourdrinier machine sections and components |
| [utilities-and-structures.md](utilities-and-structures.md) | Piping, pipe bridges, buildings, platforms |
| [horizontal-pumps.md](horizontal-pumps.md) | Long-coupled process pumps, MC pumps, motors, couplings and visible fasteners |

---

## The rule that governs every file here

**User-supplied parameters always take absolute priority.** Everything in this
directory is a fallback for when data is missing. When the user or the project
data gives a value, use it exactly — even if it contradicts these files, and even
if you believe it is wrong. If you think a given value is mistaken, model it as
given and raise the concern separately.

Defaults used from these files are **Reference Values** and must be labelled as
such in the deliverable.

---

## Know which part each parameter describes

Most parameter errors are not wrong numbers — they are right numbers applied to
the wrong part of the equipment. Before using a dimension, establish what it
measures:

| Term | Usually means | Frequently confused with |
|------|---------------|--------------------------|
| Diameter | Shell **inside** diameter | Outside diameter over insulation |
| Height | Shell tangent-to-tangent height | Overall height including heads and skirt |
| Overall height | Bearing plane to highest point | Shell height |
| Elevation | Bottom centre point (bearing plane) | Shell bottom, or grade |
| Volume | Working volume | Total geometric volume |

A tank whose stated height is tangent-to-tangent but modelled as overall height
will be short by the head and skirt heights combined. **When a stated volume does
not reconcile with D and H, that is the signal a term has been misread** — check
before modelling.

---

## Evidence standard

Numbers here must be traceable to a named manufacturer, a standard, project data,
or a user correction. Vague recall is not a source.

- Ranges (`φ3000–5500`) are typical-practice envelopes for sanity-checking and
  reasoned defaults.
- Single values are defaults to use when nothing better exists.
- **It is better to record nothing than to record something wrong.** A missing
  default makes you ask; a wrong default makes you confidently wrong.

Anything marked *unverified* is a working assumption and must not be presented as
established practice.

---

## Adding equipment

Structure over precision. Record, in order of usefulness:

1. **Function** — what it does in the process, which drives its shape
2. **Structural configuration** — roof, bottom, support, orientation
3. **Typical geometry** — size envelope
4. **Nozzle logic** — where connections go and why
5. **Distinguishing features** — what makes it recognisable

The first two are worth more than exact dimensions: a correctly-configured tank
with reference-value sizes is useful, whereas a precisely-sized tank with the
wrong configuration is not.

Adding another industry means adding files here. The Iron Rules do not change —
E3D's geometry semantics are industry-neutral.
