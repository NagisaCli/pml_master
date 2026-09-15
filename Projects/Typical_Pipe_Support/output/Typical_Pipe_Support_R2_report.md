# Typical Pipe Support R2: complete load

Current delivery: `C:\e3d_models\SINGLE_TYPICAL_PIPE_SUPPORT_R2.pml`.
Status: static checks pass; E3D loading and visual acceptance pending.

R1 first failed on unsupported FRMW orientation. The proposed continuation then
failed because `/TPS_R1_FRAME` did not exist in the receiving session. The earlier
error was insufficient evidence of retained database state. No cause for the
missing element, such as rollback or a session change, has been established.

R2 creates its entire model hierarchy with fresh R2 names. It does not select
any R1 element, delete any model, run another macro or save work. Every explicit
model selection refers to an element created earlier in this same file. Catalogue
references remain external and must resolve in the receiving E3D project.

First select a writable **SITE** in the model tree. Then run once:

```pml
$M C:\e3d_models\SINGLE_TYPICAL_PIPE_SUPPORT_R2.pml
ADD /ZONE_TYPICAL_SUPPORT_R2
/ZONE_TYPICAL_SUPPORT_R2
AUTO CE
```

All section attributes and auxiliary geometry match the corrected full R1.
Only names and header comments differ: 2 SCTN, 174 auxiliary primitives,
6 hex heads, 6 bored washers and 13 fillet weld runs. All earlier Reference
Values and the pending catalogue-face, orientation and weld-contact checks in
the [geometry report](Typical_Pipe_Support_R1_report.md) continue to apply.

17 focused tests pass, including missing-frame creation, old-frame dependency,
framework ORI rejection and the prior geometric failure tests. Repository and
deployed files are byte-identical; see `Typical_Pipe_Support_R2_checks.json`.
Static validation is not evidence of E3D load success.

Path correction: chat strings such as `C:\e3d\_models\SINGLE\_TYPICAL...`
contain escaped underscores. Decoding these gives the existing
`C:\e3d_models\SINGLE_TYPICAL...` paths, consistent with the exact reported
line contents. The earlier claim of an absent nested source path was a formatting
misinterpretation. Use commands from fenced code blocks unchanged.
