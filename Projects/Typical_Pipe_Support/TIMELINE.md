# Timeline

| Date | Event | Evidence |
|---|---|---|
| 2026-09-13 | User confirmed screenshot is unedited R2; requested visual reconstruction. R3 retains main steel and revises lap nodes, angle cuts, bored plates/washers, hex heads and explicit ownership. Static checks pass; E3D review pending. | [Screenshot](results/evidence/R2_unedited_user_review.png), [R3 report](output/Typical_Pipe_Support_R3_report.md), [checks](output/Typical_Pipe_Support_R3_checks.json) |
| 2026-09-13 | R1 resume failed: TPS_R1_FRAME undefined. Superseded by complete R2 with new names and no R1 dependencies; 17 focused tests pass, geometry unchanged. Live trial pending. | [Error](results/evidence/2026-09-13_R1_FRAME_undefined_user_report.txt), [R2 report](output/Typical_Pipe_Support_R2_report.md), [R2 checks](output/Typical_Pipe_Support_R2_checks.json) |
| 2026-09-13 | R1 load failed on FRMW ORI, line 12. Header corrected; geometry unchanged; targeted continuation generated. 83 focused and integrity tests passed; E3D retry pending. | [User error](results/evidence/2026-09-13_FRMW_ORI_user_report.txt), [archived failing macro](archive/R1_before_FRMW_fix/Typical_Pipe_Support_R1.pml), [resume](output/Typical_Pipe_Support_R1_RESUME.pml) |
| 2026-09-13 | R1 independent review candidate; static PASS, live acceptance pending. Provisional source identified by exact zone and matching desktop bytes. | [Report](output/Typical_Pipe_Support_R1_report.md), [checks](output/Typical_Pipe_Support_R1_checks.json) |

No accepted E3D baseline has been established for this isolated project.
