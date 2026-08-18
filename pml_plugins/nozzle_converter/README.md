# Nozzle Specification Manager — AVEVA E3D PML2 form

A native E3D dialog for diagnosing and batch-repairing NOZZLE catalogue
references. It exists because a nozzle whose `CATR` is unbound (`Nulref`) draws
nothing at all — the model looks like it is missing nozzles that are in fact
present but invisible. See
[catalogue-elements.md](../../skill/knowledge/catalogue-elements.md).

Written in PML2 (form definition), unlike the PML1 macros this repository
generates for model geometry. Forms are a customisation surface and are not
subject to the PML1-only rule in the Iron Rules.

## Features

**Scoped scan and health diagnosis.** Scan by `Current Element (CE)`,
`Current Zone`, `Current Site` or `Entire World`. Each nozzle is listed as
`[OK] ...` or `[MISSING] ... (Nulref)`, so an invisible nozzle is identified
before anything is changed.

**Spec conversion and CATREF binding.** Enter any target specification path —
ANSI, or a GB/DIN component. A *repair Nulref only* toggle prevents overwriting
a nozzle that already holds a correct spec, which makes a batch run
non-destructive by default.

**Bore preservation.** `nozzle_smart_apply.mac` matches the existing bore when
changing spec, rather than forcing every nozzle to one size.

**Optional attribute updates.** Height (`HEIG`, mm), bore, design pressure
(`PRES`, bar), temperature (`TEMP`, °C), test pressure, insulation and
description — each behind its own toggle, all off unless explicitly enabled.

**No PMLLIB configuration.** The form is compiled in memory, so no E3D
environment variable or directory re-index is needed.

## Installation

The macros call each other by absolute path (`$M "C:\...\nozzle_scan.mac"`),
which is how E3D resolves macros — paths are absolute at call time, never
relative to the calling file. Copy the whole directory to one location and make
the paths inside agree with it. The paths currently point at
`C:\Users\A\Desktop\`.

Files needing a path edit if you install elsewhere:
`launch_nozzle_tool.mac`, `add_to_e3d_menu.mac`, and the `callback` lines in
`nozzleSpecConverter.pmlfrm`.

## Usage

Load the toolbar from the E3D **Command** window:

```pml
$M "C:\Users\A\Desktop\add_to_e3d_menu.mac"
```

That shows a small **Nozzle Tools** bar with three buttons — *Nozzle Spec
Manager*, *Native Nozzle*, *Auto-Fix Nulref*. Or open the main form directly:

```pml
$M "C:\Users\A\Desktop\launch_nozzle_tool.mac"
```

Then, in the dialog:

1. **1. Scope & Nozzles Browser** — pick a scope and click **Scan**. The list
   fills with every nozzle found and its binding state.
2. **2. Target Spec & Attributes** — enter the target specification path, and
   enable only the attribute toggles you intend to change.
3. **Smart Batch Convert** — applies the change. The 3-D view updates as the
   nozzles rebind and become visible.

Scan before converting. The scan is what tells you which nozzles are actually
broken, and with *repair Nulref only* enabled the conversion acts on exactly
those.

## Files

| File | Role |
|------|------|
| `nozzleSpecConverter.pmlfrm` | The form: layout, members, defaults |
| `launch_nozzle_tool.mac` | Loads and shows the form |
| `add_to_e3d_menu.mac` | Small always-on toolbar with three shortcuts |
| `nozzle_scan.mac` | Scope scan; populates the list with OK/MISSING state |
| `nozzle_smart_apply.mac` | Batch convert, preserving bore |
| `nozzle_apply.mac` | Direct apply path (not currently bound to a button) |
| `nozzle_spec_change.mac` | Single-nozzle spec change |
| `nozzle_read_ce.mac` | Reads the current element into the form |
| `nozzle_cata_scan.mac` | Queries the catalogue for available components |
| `nozzle_locate_3d.mac` | Locates the selected nozzle in the 3-D view |
| `nozzle_open_native.mac` | Opens E3D's own `!!equnozzle` form |

## Known gaps

- **`auto_fix_nozzles_in_ce.mac` is missing.** `add_to_e3d_menu.mac` binds it
  to the *Auto-Fix Nulref* button, but the file was never copied into the
  repository and is not on the machine that built it. That button will fail
  until it is restored or the callback is removed. The main form's
  *Smart Batch Convert* covers the same ground with more control.
- **`launch_nozzle_tool.mac` was reconstructed** on 2026-08-18 from the form
  definition, for the same reason. It has not been run in E3D since — verify it
  loads before relying on it.
- `nozzle_apply.mac` is present but no button calls it; `nozzle_smart_apply.mac`
  superseded it.

## Related

The Python precursor to this plugin is archived at
[`Projects/JK_Pump_Build/archive/2026-08-17_nozzle_catr_repair/`](../../Projects/JK_Pump_Build/archive/2026-08-17_nozzle_catr_repair/REVISION_RECORD.md).
It rebound 235 nozzles unconditionally, from a Desktop text file, with no bore
preservation — this form replaces it.
