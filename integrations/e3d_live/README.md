# E3D Live Bridge

Status: **PHASE-3 CONTROLLED-WRITE IMPLEMENTED; live write acceptance pending**
on AVEVA E3D Design Mk3.1.11.0. Phase-1 transport and Phase-2 preview were
verified live. Phase-3 protocol, x86 build, and failure gates are verified
offline; final controlled-write acceptance still requires an isolated live E3D
Design session and an operator-supplied API key.

This directory is an opt-in integration boundary. It does not import the core
agent, repository memory, any `Projects/` folder, or the geometry generators.
One gateway process is bound to exactly one E3D operating-system process,
project, MDB, and module. A message from any other process or scope is rejected
before it reaches the assistant backend.

## Controlled operation

The E3D panel owns the full operator workflow:

1. select an AI provider, enter its API key, and click `Configure AI`;
2. select one E3D element and enter a natural-language instruction;
3. click `Preview Changes` and review the typed ChangeSet;
4. click `Apply Verified ChangeSet` and accept the final confirmation dialog;
5. the Add-in rechecks PID, project, MDB, module, Current Element, expiry, and
   every expected current value before opening an AVEVA undo transaction;
6. it applies only allowlisted attributes, reads every value back, commits on
   complete success, or calls `AbortTransaction()` on failure;
7. it posts a terminal execution receipt to the gateway audit log.

The executable operation set is deliberately narrow: `DESC`, `XLEN`, `YLEN`,
`ZLEN`, `HEIG`, `DIAM`, `DTOP`, and `DBOT`. Creation, deletion, naming,
catalogue references, ownership changes, arbitrary PML, and cross-element
operations are rejected. Position and orientation remain visible context but
are not executable until their typed parsers and numerical verification are
separately proven.

`Save Work after verified apply` is off by default. With it off, a successful
transaction changes the current E3D session but remains unsaved. With it on,
the confirmation dialog states that `MDB.CurrentMDB.SaveWork(...)` follows the
verified transaction.

## API configuration: provider profiles and only the key

Run the installer once:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\integrations\e3d_live\deployment\install_runtime.ps1
```

It creates an isolated Python runtime and installs the pinned official OpenAI
SDK from `requirements.txt`. The E3D panel exposes two isolated profiles:

- `Token Rhythm (Chat Completions)` is the panel default. Its fixed endpoint is
  `https://tokenrhythm.studio/v1`; its default model is
  `deepseek-v4-flash`. The model field is editable for another model ID made
  available to the operator's account.
- `OpenAI (Responses)` uses the fixed `gpt-5.4-2026-03-05` snapshot and the
  official OpenAI endpoint.

With either profile, the preconfigured defaults mean the panel needs only the
provider API key. The key is sent over the authenticated loopback session,
held in gateway process memory, never echoed, never written to the PID session
file, and never written to the audit log. Restarting or reconfiguring the
gateway clears/replaces it. Changing provider also revokes ChangeSets and
cached previews produced by the previous provider.

The official profile uses Responses, strict Structured Outputs, and
`store: false`. The Token Rhythm profile follows its documented OpenAI
compatibility contract with `client.chat.completions.create(model=...,
messages=...)`, non-streaming output, JSON-only instructions, and strict local
schema validation. Both profiles use a 60-second timeout and three SDK retries.
The gateway sends only the active scope, operator instruction, and allowlisted
snapshot; the bridge token and session ID are excluded. See the
[OpenAI Chat Completions reference](https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions),
[Token Rhythm API integration guide](https://tokenrhythm.studio/docs/api-integration),
and [Token Rhythm model list](https://tokenrhythm.studio/models).

## Protocol and safety model

- `protocol.schema.json`: selection snapshot, protocol `2.0`.
- `preview-response.schema.json`: typed preview and bounded ChangeSet.
- `control-protocol.schema.json`: provider configuration and one-time
  authorization contracts.
- The ChangeSet expires after five minutes and is bound to the bridge session,
  E3D PID, exact scope, target element, and ordered operation IDs.
- Concurrent previews are serialized. A reused preview request ID returns the
  same response and cannot duplicate an external request or ChangeSet; reusing
  it with a different payload fails closed.
- Apply results are terminal and idempotent by result request ID. Their ordered
  operation prefix, values, statuses, and persistence claim must agree with the
  original authorized ChangeSet.
- `/health` is loopback-only and requires the per-session bridge token.
- The gateway holds an exact Windows process handle and shuts down when the
  bound E3D process exits, so a later PID reuse cannot inherit the session.
- The append-only JSONL audit excludes API keys and bearer tokens.
- The default local backend transmits no project data and returns zero
  operations until `Configure AI` is used.

The Add-in owns every AVEVA API call because the installed E3D/CAF runtime is
x86 while the Python gateway is x64. No `DbElement` crosses the process
boundary, and AVEVA writes run on the E3D UI thread.

## Build and isolated deployment

Build the x86 Add-in:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\integrations\e3d_live\addin\build.ps1
```

Prepare a project-local Add-in configuration without modifying the AVEVA
installation copy of `DesignAddins.xml`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\integrations\e3d_live\deployment\prepare_deployment.ps1
```

Start the isolated AVEVA monitor. Use `-Rebuild` only after all E3D processes
that loaded the prior DLL have closed:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\integrations\e3d_live\deployment\start_test_e3d.ps1
```

After login, list Design processes and bind the selected PID. Controlled write
is the default access mode, but nothing can execute before preview and operator
confirmation:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\integrations\e3d_live\deployment\list_e3d_processes.ps1

powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\integrations\e3d_live\deployment\start_target_gateway.ps1 `
  -TargetE3dPid 12345 -ProjectCode APS -Mdb ALL
```

The gateway writes only its PID session file and a secret-free audit receipt
under the ignored `deployment/runtime` directory. Other E3D processes remain
inactive even when they use the same project and MDB.

## Verification boundary

Static tests and compilation are not live-write acceptance. Phase 3 is VERIFIED
in E3D only after all of the following are observed in an isolated test process:

1. the controlled panel loads and accepts the API key without echoing it;
2. a selected element produces a typed preview;
3. changing Current Element invalidates the pending ChangeSet;
4. stale expected values and cross-element operations are rejected;
5. a confirmed `DESC` test change reads back exactly;
6. an injected operation failure aborts the whole undo transaction;
7. the change remains unsaved by default and can be undone;
8. an explicitly requested Save Work persists and reopens correctly;
9. repeated selection, preview, gateway restart, and duplicate requests do not
   crash E3D or duplicate a write;
10. the audit receipt contains no API key or bridge token.

Historical live evidence remains under `evidence/` and must not be rewritten as
Phase-3 proof.
