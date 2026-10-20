# FINGERPRINT — 203_TA_401_BS_Filtrate_Tank

Stable signals used to identify an incoming file as this project **before**
editing. Match several signals, then read `TIMELINE.md` for the current
baseline.

## File-name signals

- `203_TA_401_BS_Filtrate_Tank*.pml`
- `900135359*` — the ANDRITZ drawing number, on the PDF and the DWG

## Element-name signals

- `NEW EQUIPMENT /203_TA_401` — a single equipment item, not a tank register
- SUBE convention: `203_TA_401_SHELL`, `_INTERNALS`, `_OVERFLOW`, `_ACCESS`,
  `_EARTHING`, `_SUPPORT`, and one `_N<mark>` per nozzle
- Nozzle marks are ANDRITZ-style with a dot in the drawing and an underscore in
  the model: `N1.1 -> 203_TA_401_N1_1_NOZZ`, `N1.2`, `N2.1`, `N2.2`, `N5`, `N6`,
  `N8`, `N9`, `N11`, `N12`, `N13`, `MW`

## Geometric anchors (tank-local, mm)

| Feature | Value |
|---------|-------|
| Shell | ID 6000 x 6.35 wall, top of shell U 8000 |
| Roof | 12 deg cone, eave U 8003.8, collar OD 1305.5, deck U 8704.7 |
| Air-separation cylinders | ID 1502.5 to U 5105 and ID 2201.5 to U 4298, axis offset **E -501.9** |
| Soap launder | R2400-3000, az 264.5-339.6 |
| Overflow | seal box U 6589-7950 at az 30, downcomer O323.9 at R3544.2 |
| Nominal volume | 226 m3 (pi/4 x 6.0^2 x 8.0 = 226.2) |

The **E -501.9 cylinder offset** is the single most distinctive number: this
vessel's air-separation cylinders are deliberately eccentric to the tank axis.

## Look-alikes

- `JK-Tank_Build` uses a 22-tank register under zone `WSB_TA`; this project is
  one bespoke vessel with a hand-built geometry script.
- `203-TA-006` in JK-Tank_Build is also a brown-stock filtrate tank, but
  ID 5600 x 9200 with a dished/conical roof and no eccentric internals.
