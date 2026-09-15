# Typical Pipe Support

Project: [Typical_Pipe_Support](../../Projects/Typical_Pipe_Support/DO.txt).
Status: R2 displayed in the user's confirmed unedited screenshot; geometry was
criticised. Reconstructed R3 passes static checks; E3D visual review pending.

R3 replaces rectangular lap tabs with tapered profiles, moves the angle cut ends
inside the lap regions, and uses bored single-solid washers and explicit closed
ownership for six hex-headed screws. Main beam attributes are unchanged.
See the [R3 report](../../Projects/Typical_Pipe_Support/output/Typical_Pipe_Support_R3_report.md).
The R2 screenshot shows crescent-like fastener outlines, but their root cause
is unproven; clockwise loop emission is a candidate choice, not a verified
universal remedy. Do not promote it without E3D evidence.

The shared parser previously discarded an open positive extrusion when it met
a negative child. Drilling the wall plates exposed this as a 34/36 positive-solid
count failure. Negative child scopes now leave the parent's pose/profile intact,
with regression coverage. Bore verification uses each owner's local coordinates.

R1 continuation subsequently failed with `/TPS_R1_FRAME` undefined. Do not infer
surviving elements from an earlier error's line number: verify current elements
before continuation, or use a full fresh namespace. R2 takes the latter route,
with unchanged geometry and all model lookups satisfied by preceding creation.
The current [R2 report](../../Projects/Typical_Pipe_Support/output/Typical_Pipe_Support_R2_report.md)
supersedes R1 loading instructions. Escaped underscores in chat explain the
previous nested-path interpretation; the decoded source path exists locally.

R1 was subsequently rejected by E3D on line 12: FRMWORK has no ORI attribute.
The generator now omits its framework ORI/POS header, with no geometry changes.
A resume macro selects the already-created empty frame and emits only the
remaining sections and hardware. The shared validator now rejects framework
orientation headers. The failing file and user report are archived in the
project; corrected full loading and continuation remain pending live tests.

The requested path was absent. A local macro with the exact requested zone was
found and archived as a provisional source. Its primary frame already used
native SCTN; its six visible fasteners were cylinders and its connection plates
were rectangular blocks. R1 preserves primary section attributes and wall
mountings, adds six true hexagonal heads with annular washers, and revises
haunches, side-mounted lap gussets and fillet-weld solids.

Keep the source hashes, assumed dimensions and live testing instructions in the
[project report](../../Projects/Typical_Pipe_Support/output/Typical_Pipe_Support_R1_report.md).
The angle TOAY face and roll were not read from a live catalogue. Do not reuse
this connection layout as a verified detail in another project.

Numerical review found two implementation concerns: the general builder's
0.1 mm formatting can distort a regular hexagon's equal edges, so the existing
six-decimal extrusion emitter is used for heads; and the shared parser's current
extrusion bounds shortcut ignores orientation, so the scoped verifier computes
rotated extents from the shared parser's vertices. No global syntax or
structural connection claim was promoted to VERIFIED in this run.
