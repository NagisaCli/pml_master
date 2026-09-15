# Phase-3 Controlled Write — Static and Deployment Evidence — 2026-08-20

Status: **STATICALLY VERIFIED; isolated live write acceptance pending.**

## Implemented chain

- Protocol version `2.0` preserves the exact PID plus project/MDB/module scope.
- The E3D panel accepts a session-only OpenAI API key, natural-language
  instruction, typed preview, and operator-confirmed Apply action.
- The fixed model is `gpt-5.4-2026-03-05`; the pinned official SDK is
  `openai==3.3.1`.
- OpenAI requests use the Responses API, strict Structured Outputs,
  `store: false`, a 60-second timeout, and three SDK retries.
- A five-minute ChangeSet lease binds the session, PID, scope, exact target,
  ordered operation IDs, and expected current values.
- The x86 Add-in revalidates the live scope, Current Element, target, expiry,
  attribute allowlist, and every precondition on the E3D UI thread.
- E3D writes use `UndoTransaction.StartTransaction`, typed
  `DbElement.SetAttribute`, independent readback, `EndTransaction`, and
  `AbortTransaction` on failure.
- `Save Work` is a separate opt-in checkbox and is off by default.
- API keys and bridge tokens are excluded from append-only JSONL audit records.

## Native API evidence

The installed AVEVA `Samples.zip` was inspected locally. Its
`ExamplesAddin/ExampleUndo.cs` demonstrates `StartTransaction`,
`SetAttribute`, `EndTransaction`, and `PerformUndo`; reflection against the
installed x86 `Aveva.Core.Utilities.dll` confirmed the public
`AbortTransaction()` method. `StandaloneExample/Standalone.cs` demonstrates
typed `SetAttribute`, immediate readback, and `MDB.CurrentMDB.SaveWork(...)`.

## Stability verification

- Focused bridge suite: `23 passed`.
- Full repository suite: `552 passed, 4 skipped`.
- The focused suite covers scope/PID/target drift, stale and expired
  preconditions, one-time authorization, idempotent preview and result retries,
  conflicting request-ID reuse, 100 concurrent selection submissions, audit
  secret exclusion, runtime pinning, and source-level write confinement.
- Python bytecode compilation and PowerShell parser checks passed.
- The isolated OpenAI SDK import reported version `3.3.1`; no API key was
  configured and no OpenAI request was made.
- x86 Add-in build SHA-256:
  `87575917FC9ACBB39D47296348087DB9120AC6954B821797D8E8C23913B2ADCB`.
- The deployed runtime DLL hash matched the source DLL hash.
- The installed AVEVA `DesignAddins.xml` remained at SHA-256
  `A064B408D876FB8441B412E9F99A0E3A5BDC41AF889D053D3E276608D00DDC04`.

## Live boundary

An isolated AVEVA Monitor was started as PID `23824`. Live acceptance still
requires operator login, Design PID binding, API-key entry in the panel, an
explicitly reviewed test ChangeSet, E3D readback, undo verification, and a
separate explicit persistence test. None of those live-write claims are made by
this document.
