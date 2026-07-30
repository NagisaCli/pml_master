# JK_Pump_Build — Uncertainty and Outstanding-Issue Report

## UNCONFIRMED

- **E3D interactive execution:** UNCONFIRMED. The macros passed static and
  numerical verification only; the user must load them in the receiving E3D
  project before they can be called E3D-verified.
- **Vendor dimensions and performance data:** UNCONFIRMED. No vendor GA,
  motor schedule, pump model, shaft elevation or nozzle schedule was supplied.
- **Nozzle catalogue portability:** UNCONFIRMED outside the current receiving
  catalogue. The generated `CATR SPCOMPONENT` paths use the project's verified
  `150lb_Ansi_Flanged` mapping and must be re-queried for another catalogue.
- **Materials, mass, maintenance envelope, anchor bolts and design conditions:**
  UNCONFIRMED. Visible anchor and hold-down fasteners are modeled as bounded
  Reference Values, but their grade, thread and embedment are not claimed.
- **High-detail dimensions:** UNCONFIRMED. Bolt sizes/counts, motor frame,
  cooling-fin tier, cable-gland side, bearing bracket, seal housing, coupling
  hardware and service accessories are engineering Reference Values derived
  from duty, skid scale and the available top-view outlines.

## Missing top-view references

- 203-PU-020
- 205-PU-004
- 205-PU-032

These pumps use a same-family structural model scaled only to their own
contractual baseplate and confirmed directions; no dimensions were copied
from `Horizontal_Pump_Example.txt`.

## Tag-specific notes

- **203-PU-020:** No tag-specific top view; MC-family geometry is a Reference Value.
- **204-PU-003:** Top view shows attached piping beyond the skid; project macro models the pump equipment envelope only.
- **205-PU-004:** No tag-specific top view; MC-family geometry is a Reference Value.
- **205-PU-018:** Client-confirmed special layout: main equipment axis E-W with driver east and casing west; suction S and discharge W are coplanar horizontal nozzles.
- **205-PU-031:** Description retained exactly as supplied in Excel.
- **205-PU-032:** No tag-specific top view; same-duty project pumps inform structure only, scaled to this contractual baseplate.
- **205-PU-038:** Client-confirmed special layout: main equipment axis E-W with driver east and casing west; suction S and discharge W are coplanar horizontal nozzles.
- **205-PU-046:** Position supersedes Excel E=15221 per client confirmation.
- **205-PU-061:** Position supersedes Excel E=461554 per client confirmation.

## Resolved items

- 205-PU-046 position is confirmed as `(45221, 14294, 0)` mm.
- 205-PU-061 position is confirmed as `(46154, -8256, 0)` mm.
- Baseplate thickness is confirmed as 50 mm for every pump.
- Each pump is confirmed to require its own independent EQUI hierarchy.
- 205-PU-018 and 205-PU-038 are confirmed as E-W main-axis special
  arrangements with coplanar S and W nozzles.
