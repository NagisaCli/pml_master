# FINGERPRINT — JK_Pump_Build

Stable signals used to identify an incoming file as this project **before**
editing. Match several signals, then read `TIMELINE.md` for the current
baseline.

## File-name signals

- `NNN-PU-NNN.pml` — one macro per pump (e.g. `203-PU-008.pml`, `205-PU-054.pml`)
- `JK_Pump_Build_All_Pumps.pml` — combined loader
- `JK_Pump_Build_*_report.md` / `JK_Pump_Build_*_inventory.md` — study docs

## Element-name signals

- Equipment names follow `<area>_PU_<nnn>`: `NEW EQUI /204_PU_023`
- SUBE convention includes `_BASEPLATE`, `_SUPPORT_FRAME`, `_CASING`,
  `_BEARING_FRAME`, `_SUCTION`, `_DISCHARGE`, `_COUPLING`, `_DRIVER`,
  `_SERVICE_DETAILS`
- Nozzle names: `<tag>_SUCTION_NOZZLE`, `<tag>_DISCHARGE_NOZZLE`

## Zone / site signals

- Generated PML macro style (comments `-- Equipment: <tag>`), not a
  `NEW ZONE /WSB_TA` data listing.

## Look-alikes

- `JK-Tank_Build` uses `TA` tags and the `WSB_TA` zone.
- `JK_Cooking_Tank_Build` uses descriptive tank names, no `PU` tags.
