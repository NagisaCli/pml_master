# FINGERPRINT — JK_Cooking_Tank_Build

Stable signals used to identify an incoming file as this project **before**
editing. Match several signals, then read `TIMELINE.md` for the current
baseline.

## File-name signals

- `NN_<DESCRIPTIVE_NAME>.pml` — numbered cooking-plant tanks, e.g.
  `01_BLEACH_HOT_WATER_TANK.pml`, `06_JUNK_TRAP_1.pml`,
  `13_MAIN_CONDENSATE_TANK.pml`
- `JK_Cooking_Tank_Build.pml` — combined macro
- `cooking_tank*.txt` — native export used for the R6 rework

## Element-name signals

- Equipment names are the descriptive file base names, e.g.
  `NEW EQUI /01_BLEACH_HOT_WATER_TANK`
- Blow tanks / accumulator / junk-trap family names: `BLOW_TANK`,
  `ACCUMULATOR_TANK`, `JUNK_TRAP`, `CONDENSATE_TANK`, `SERVICE_TANK`

## Zone / site signals

- Generated PML macro style; the native export is not under the `WSB_TA` zone.

## Look-alikes

- `JK-Tank_Build` uses `TA` tags and `WSB_TA` zone.
- `JK_Pump_Build` uses `PU` tags and pump-specific SUBEs.
