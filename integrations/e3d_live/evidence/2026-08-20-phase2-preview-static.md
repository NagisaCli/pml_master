# Phase-2 Typed Change Preview — Static Evidence — 2026-08-20

Status: **STATICALLY AND LIVE VERIFIED in local-only read-only mode.**

## Implemented boundary

- The E3D panel has a change-instruction field and `Preview Changes` action.
- Preview responses conform to `preview-response.schema.json`.
- The only operation type is `set_attribute`.
- A proposed target must equal the current selected element.
- The attribute must be in the separate preview allowlist.
- The expected current value must equal the captured selection snapshot.
- Every ChangeSet remains non-executable, requires user approval, has an empty
  legacy `changes` array, and declares `persistence: none`.
- No Apply button, database mutation API, or Save Work path exists.

## External AI boundary

The default backend is local-only and transmits no project data. The optional
OpenAI Responses adapter requires all three of an isolated API key, an explicit
model, and an external-transmission switch. It sends only scope, the operator
instruction, and the selected element snapshot. The bridge token and session ID
are excluded. The request uses Structured Outputs and `store: false`; all model
output is validated locally before display.

## Verification

- Focused bridge suite: `16 passed` before the final repository run.
- Full repository suite: `545 passed, 4 skipped`.
- A fake structured AI response produced one locally validated preview operation.
- Cross-element, stale-precondition, and non-allowlisted proposals were rejected.
- OpenAI backend startup without explicit external-transmission permission was
  rejected.
- `E3D_LIVE_OPENAI_API_KEY` was not configured during these tests, so no external
  model request occurred.
- New x86 Add-in build SHA-256:
  `AA10B2F9374B7521ACDBE728D4535FD99E5D833F8F4EDB1990F8F8A55557265B`.

## Live E3D acceptance

- Isolated launcher process: `mon.exe` PID `3020`.
- Bound Design process: `des.exe` PID `30336`, whose direct parent was PID
  `3020`.
- Bound scope: project `APS`, MDB `ALL`, module `DESIGN`.
- Loopback gateway: `127.0.0.1:48731`, backend `local_only`, mode `read_only`.
- Bridge session: `1d9f0bb8-ae2b-48dd-9b28-f46266bf6e67`.
- Selecting `/203_PU_009` caused the panel to reconnect to the PID-scoped
  session and submit one allowlisted snapshot.
- Clicking `Preview Changes` produced one accepted preview request with no
  operations and `persistence: none`, as expected without an external AI
  backend.
- Final health counters: `accepted_selection_count: 1` and
  `accepted_preview_count: 1`; target PID and scope remained unchanged.
- No Apply control was present, no E3D database write was requested, and no
  external API call occurred.

This verifies the isolated real-time selection and typed preview round trip.
Generating a non-empty AI proposal remains a separate opt-in test requiring an
explicit external-transmission decision, isolated API credential, and model.
