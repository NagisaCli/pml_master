# PML-STUDY-SCREW-001 — local validation record

| Artifact | SHA-256 |
|---|---|
| `candidate/01_refined_screw_set.pml` | `4EC02396EBD54D7F42E957A5091F9895246B521B64AD23EAE7363CED677D0923` |

Run: 2026-08-05, `build_candidates.py`.

- PML1 validation: clean (`validate_pml` returned no problems).
- Geometry verification: clean — 56 primitives parsed; face-to-face contacts,
  thread-ridge containment, positive bounds, screw axes and lowest-point U 0
  all checked numerically from the emitted text.
- E3D verdict: **user-accepted 2026-08-05 ("可以的")** — candidate loaded
  and accepted; detailed Q ATT measurement pack remains available but
  optional.
