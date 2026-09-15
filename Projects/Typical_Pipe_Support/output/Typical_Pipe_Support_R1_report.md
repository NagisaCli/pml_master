# Typical Pipe Support R1 review

**Superseded loading instructions:** the R1 continuation failed because its
framework did not exist. Use the complete [R2 load](Typical_Pipe_Support_R2_report.md).
The geometry and Reference Values below still apply. The old nested-path
interpretation below was caused by escaped underscores in chat and is corrected
in the R2 report.

Status: **static geometry checks passed; E3D loading and visual acceptance pending**.

**R1 load correction:** the user reported `(2,201)` at line 12 because FRMWORK
does not have ORI. The full macro now omits the framework ORI and redundant POS
lines. Comparison against the archived failing macro proves these are the only
two deleted lines: all section and hardware geometry is unchanged. 83 focused,
extrusion-builder and skill-integrity tests passed after this correction.

For the existing partial load stopped at that exact line, run once:

```pml
$M C:\e3d_models\SINGLE_TYPICAL_PIPE_SUPPORT_R1_RESUME.pml
ADD /ZONE_TYPICAL_SUPPORT_R1
/ZONE_TYPICAL_SUPPORT_R1
AUTO CE
```

This continuation selects `/TPS_R1_FRAME` and starts at the first SCTN. It does
not recreate or delete its containers. The full macro remains for a fresh load
where the R1 names do not already exist. The error's reported nested `C:\e3d\...`
file path is not accessible here; the delivery paths above are the verified local
files. Neither corrected loading route has yet been observed running in E3D.

The requested `C:\e3d\_models\SINGLE\_TYPICAL\_PIPE\_SUPPORT.pml` does not
exist on this machine. This candidate uses the provisionally identified
`C:\e3d_models\SINGLE_TYPICAL_PIPE_SUPPORT.pml`, which contains the exact
requested `/ZONE-TYPICAL-SUPPORT`. Its desktop copy is byte-identical.
The original was archived without alteration under `../imports/`.
No live E3D action was performed. This is not an accepted fabrication model.

## Preserved geometry and intentional changes

| Item | R1 behavior |
|---|---|
| Primary frame | Native `STRU / FRMW / SCTN`, two catalogue sections |
| Cantilever | Existing `(0,16,0)` to `(0,1500,0)` and `/BS-PFC150x75x18`, CTOP preserved; actual section workline length 1484 mm |
| Brace | Existing `(0,16,-470)` to `(0,1055,-185)` and `/BS-L50x50x6`, TOAY preserved |
| Wall mounting plates | Existing 180 x 16 x 350 and 180 x 16 x 160 mm, including positions, preserved |
| Six fastener centres | Existing E/U coordinates preserved |
| Hex screws | Six regular six-vertex heads with separate shanks and bored washers |
| Root stiffener | Rectangular block inside the channel replaced by a clipped triangular haunch below the lower flange |
| Upper connection plate | Increased depth for the angle lap; clipped corners; placed at E=0..8 on one side of the assumed angle face |
| Lower connection plate | Clipped 80 x 110 mm envelope at E=0..8; joined to the lower wall plate |
| Welds | 13 continuous triangular fillet prisms: flange/root, haunch, gusset/wall or beam, and four longitudinal angle lap seams |
| Beam surface | Projecting connection details remain below the beam; no pipe clamps or isolation blocks added |
| Loading | Independent `/ZONE_TYPICAL_SUPPORT_R1`; no DELETE or SAVEWORK commands |

STRUCT owns the primary load-carrying members. The auxiliary EQUI only groups
the detailed plates, screws and weld solids. No generic blocks replace the two
catalogue sections. This is the source's section workflow; it does not convert
legacy SCTN to GENSEC or add analytical joint/fixing database relationships.
AVEVA documents the [Structure/Framework/Section hierarchy and section attributes](https://help.aveva.com/AVEVA_Everything3D/1.1/EUG/EUG15.14.2.html).

## Reference Values and their basis

These values are model proposals fitted to the source envelope, not a claimed
fastener standard, structural calculation, weld procedure or anchor schedule.

| Proposed value | Basis |
|---|---|
| Screw shank diameter 20 mm; modelled N=0..19 | Visual replacement at the six original mounting centres; hidden anchorage is not specified |
| Hex head AF30 x 12 mm | Readable six-sided head fitting the existing plate and centre spacing |
| Washer OD40 / ID22 x 3 mm, 24 sectors | Bored seating washer around the 20 mm shank; about 0.17 mm outer chord approximation |
| Haunch thickness 8 mm; reach 120 mm; bottom U=-220 | Source 8 mm stiffener thickness retained; tapered below-flange connection avoids filling the channel interior |
| Upper gusset 8 x 180 x 120 mm; 15 mm lower clips | Source thickness and longitudinal width retained; depth enlarged to contain both lap seams |
| Lower gusset 8 x 80 x 110 mm; clipped free corners | Source thickness and reach retained, height enlarged to contain the lower lap |
| Main fillet legs 6 mm; angle lap fillets 5 mm | Review-scale detail compatible with proposed 8 mm plates and nominal 6 mm angle leg; strength not calculated |
| Angle face E=0; angle material to West and below the workline | Provisional zero-roll TOAY interpretation; must be checked against the receiving catalogue |
| Beam width 75 and depth 150 mm for contact checks | Nominal source profile description; exact catalogue flange/web dimensions not retrieved |

The cut ends of the angle remain inside the lap region in side projection.
Welds cover the proposed longitudinal lap edges; no unsupported catalogue joint
references have been invented. The hidden anchor mechanism, thread pitch,
steel/bolt grades, load capacity and weld sizing are TBC.

## Validation and limits

- 2 native sections, 174 auxiliary primitives, 6 hex heads, 6 bored washers,
  13 weld runs.
- Shared PML validation and shared primitive parsing pass.
- Source section attributes and wall-plate dimensions/positions are preserved.
- Numeric checks cover positive dimensions, rotated extrusion extents, wall
  penetration, regular hexagons, seating planes, washer bore clearance, projected
  lap containment and weld clearance below the beam top.
- Six focused tests pass, including intentional floating-head, wall-penetration,
  straddling-gusset and empty-output failures.
- Files are verified after writing; hashes are in `Typical_Pipe_Support_R1_checks.json`.
- The current shared `bounds_of()` branch assumes world-Z for extrusions. This
  project's verifier transforms the parsed profile through its actual orientation
  before calculating bounds; it does not silently use that shortcut.

These are static checks, not full catalogue-aware clash detection. SCTN roll,
TOAY face, live specification resolution and actual weld-to-steel contact remain
pending. The inclined weld orientation uses an existing E3D directional form:
installed `D:\AVEVA\Everything3D3.1\pmllib\laser\forms\laserBubble.pmlfrm:644`
contains `Y is N 33 U and Z is S 60 U`; this exact candidate still needs trial.

## Manual E3D test

1. Choose a writable SITE in the intended E3D project. If either source profile
   cannot resolve, stop and report its name; do not replace it with a guessed profile.
2. Run these commands once:

   ```pml
   $M C:\e3d_models\SINGLE_TYPICAL_PIPE_SUPPORT_R1.pml
   ADD /ZONE_TYPICAL_SUPPORT_R1
   /ZONE_TYPICAL_SUPPORT_R1
   AUTO CE
   ```

3. Inspect the hierarchy: `/TPS_R1_STRUCTURE` → `/TPS_R1_FRAME` →
   `/TPS_R1_BEAM` and `/TPS_R1_BRACE`. Both must render as catalogue steel.
4. View the wall from +N. All six screws must show six flat sides. The washer
   seats on N=16; the head underside is N=19 and its front is N=31.
5. Inspect the brace from both sides. Its outer vertical leg must lie against
   the E=0 side of the gussets; the angle must extend to West, not through the
   plate. If this is reversed, stop and supply `Q ATT` for `/TPS_R1_BRACE`
   plus an end-on view. Do not mirror it by guesswork.
6. Inspect both lap weld pairs and the root haunch. Welds must touch both parts,
   with no angle/flange piercing or floating seams. Inspect in solid mode and
   use the project's structural checking/clash workflow. Record any error text.
7. Do not reload over the same R1 names. This macro does not delete existing
   elements or save work. Save only after your project review is accepted.

Reproduce static checks from the repository root:

```powershell
python Projects/Typical_Pipe_Support/tools/build_review.py
python -m pytest Projects/Typical_Pipe_Support/tools/test_review.py -q
```
