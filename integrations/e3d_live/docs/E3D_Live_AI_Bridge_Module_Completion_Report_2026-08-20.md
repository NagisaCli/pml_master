# E3D Live AI Bridge Module Completion Report

Report Date: 2026-08-20<br>
Module Location: `integrations/e3d_live`<br>
Current Conclusion: Code implementation, isolated deployment, protocol definitions, controlled write gates, and static stability verification are complete; live API calls and E3D write acceptance must be executed after user signs into Design and supplies an API key.

## 1. Objectives

This work establishes an isolated real-time AI interaction interface for AVEVA E3D Design, separated from other project knowledge, generators, and business modules, enabling operators to perform the following workflows directly within a designated E3D process:

1. Read real-time restricted attribute snapshots of the Current Element;
2. Enter natural language modification instructions inside an E3D docked panel;
3. Generate structured, reviewable modification previews via AI;
4. Perform dual validation of target element, current values, scope, and operation types via both Gateway and E3D Add-in;
5. Execute controlled transactions only upon secondary operator confirmation;
6. Default to not saving work, executing `Save Work` only when explicitly checked;
7. Record keyless JSONL audit receipts.

The module strictly binds to one E3D OS process, one project, one MDB, and one Design module. Other E3D processes, even within the same project, will not automatically connect to this session.

## 2. Overall Architecture

The system consists of three isolation layers:

### 1. E3D x86 Add-in

The Add-in runs inside the AVEVA E3D Design process, responsible for:

- Capturing Current Element changes;
- Reading whitelisted attributes and generating selection snapshots;
- Displaying AI Provider, model, API key, modification prompts, and responses;
- Displaying pending ChangeSets;
- Invoking AVEVA database APIs after final user confirmation;
- Executing changes using Undo Transactions;
- Reading back attributes to verify write results;
- Aborting the transaction if any operation fails;
- Determining whether to save work based on explicit user checkbox selection.

The Python Gateway never holds or passes `DbElement` across processes; all AVEVA API invocations remain on the E3D UI thread.

### 2. Local Loopback Gateway

The Python Gateway listens exclusively on `127.0.0.1` and authenticates requests using random session tokens. The Gateway handles:

- Validating the target E3D process PID;
- Validating project, MDB, and module scopes;
- Enforcing limits on message sizes and field sets;
- Calling local or external AI Providers;
- Enforcing strict local protocol schema validation on AI responses;
- Generating short-lived ChangeSets;
- Authorizing confirmation requests with single-use tokens;
- Logging keyless JSONL audit receipts;
- Guaranteeing idempotency for duplicate requests and failing conflicting requests cleanly.

### 3. AI Provider Adaptation Layer

Two non-interchangeable providers are currently retained:

| Provider | Invocation Paradigm | Default Model | Default Endpoint |
|---|---|---|---|
| Token Rhythm | OpenAI-compatible Chat Completions | `deepseek-v4-flash` | `https://tokenrhythm.studio/v1` |
| OpenAI | Responses API + Structured Outputs | `gpt-5.4-2026-03-05` | Official OpenAI Endpoint |

Token Rhythm panel configuration includes preset endpoint and default model; normally the operator only needs to supply an API Key. The Model ID remains customizable to match available account models.

## 3. Message and Response Protocol

Protocol version is `2.0`, using explicit fields and closed schema mode with `additionalProperties: false`.

Primary messages include:

- `selection_snapshot`: Whitelisted attribute snapshot of the Current Element;
- `change_preview_request`: Selection snapshot and user modification prompt;
- `configure_assistant`: Provider, model, and memory-only API key;
- `apply_authorization_request`: Precise ChangeSet authorization request after operator confirmation;
- `apply_result`: Actual E3D execution and read-back verification result.

AI cannot emit arbitrary PML or database commands directly. All AI outputs must map to locally defined operation objects, and re-validate:

- Target element matches Current Element exactly;
- Project, MDB, module, and E3D PID match exactly;
- Expected current values match live E3D values;
- Operation IDs, order, and count are unchanged;
- ChangeSet is not expired;
- Attributes are within the executable whitelist;
- No cross-element modifications exist.

## 4. Current Execution Boundaries

Currently permitted attributes:

- `DESC`
- `XLEN`
- `YLEN`
- `ZLEN`
- `HEIG`
- `DIAM`
- `DTOP`
- `DBOT`

Currently disabled capabilities:

- Creating or deleting elements;
- Modifying names or ownership;
- Modifying catalogue references;
- Executing arbitrary PML;
- Batch operations across elements;
- Writing position `POS` or orientation `ORI`;
- Auto-saving work without confirmation.

This is an intentional safety boundary. Spatial position and orientation modifications require dedicated type parsing, coordinate datums, and numerical geometric verification before being enabled.

## 5. API Key and Information Isolation

API Keys are handled via:

- Password masking input box in the E3D panel;
- Transmitted over authenticated local loopback session;
- Stored exclusively in process memory upon entering gateway;
- Never written to PID session files;
- Never written to audit logs;
- Never echoed back to E3D response fields;
- Automatically cleared upon Gateway exit;
- Replacing old keys and invalidating old previews upon Provider reconfiguration.

Example placeholders like `YOUR_API_KEY`, `sk_xxx`, and `MODEL_ID` are rejected. Token Rhythm Provider endpoint is fixed to the configured HTTPS endpoint; HTTP, embedded credentials, query strings, fragments, and unrelated addresses are rejected.

Outbound data includes only:

- Current scope;
- User prompt;
- Whitelisted attribute snapshot of Current Element.

Bridge tokens, session IDs, repository memory, other project files, and other E3D process data never enter AI requests.

## 6. Stability and Fault Protection

Implemented and verified:

- Rejection on PID and project scope mismatch;
- Rejection of unsupported fields and attributes;
- Rejection when external AI output target drifts;
- Rejection upon ChangeSet timeout;
- Invalidation of pending ChangeSet when selected element changes;
- Duplicate submissions with identical Request ID return identical results;
- Requests with duplicate ID but different payloads fail closed;
- Concurrent duplicate previews serialized via single execution channel; only one external model call and one ChangeSet generated per request;
- Cache and pending ChangeSets cleared upon Provider switch;
- Previews running during Provider switch will not register;
- Health checks require local session token; unauthenticated requests return `401`;
- Gateway holds exact Windows process handle to target E3D process; terminates automatically when target process exits to avoid PID reuse hijacking;
- Execution receipt must match original ChangeSet operation sequence, attributes, previous values, requested values, status, and persistence declaration;
- Rejection of duplicate result IDs with differing receipt payloads to prevent audit overwriting;
- Unexpected gateway exceptions sanitized to static generic errors, preventing leak of keys or internal traces to E3D;
- E3D current attributes re-read immediately prior to execution;
- All attributes read back following execution;
- Transaction rollback invoked upon any write or read-back failure;
- Save Work defaulted to OFF;
- Audit records exclude API keys and bridge tokens;
- Concurrent selection message handling does not corrupt counters or session state.

## 7. Verification Results

### Automated Tests

- E3D Live Bridge dedicated tests: `36 passed`;
- Current local main baseline full-project regression: `565 passed, 4 skipped`;
- Isolated release branch regression from GitHub `origin/main`:
  `322 passed, 2 failed, 2 skipped`. Both failures originate from pre-existing
  SHA-256 assertions in `tests/test_pipe_study.py` on pipe study evidence files,
  having no code, file, or test dependency on `integrations/e3d_live`; unrelated
  fixes were not mixed into the bridge module commit;
- Python file syntax compilation check: Passed;
- JSON protocol schema syntax check: Passed;
- Hardcoded secret pattern scan: No non-placeholder API keys found;
- Deprecated provider DTO and client symbols scan: No remnants found.

Dedicated test additions covered: 40 concurrent duplicate previews triggering exactly one provider invocation, target process watchdog, unauthenticated health check, exception sanitization, partial rollback receipt, pseudo-success rejection, terminal receipt drift rejection, and Token Rhythm SDK parameter and secret sanitization.

### Add-in and Runtime

- x86 Add-in compilation: Successful;
- OpenAI Python SDK: Pinned to `3.3.1`;
- Source DLL SHA-256 after hardening:
  `00A0D565530F6729E55435463532FDB606DD46EB69C73E29BCD38E13D2A6638C`;
- Isolated runtime DLL SHA-256:
  `00A0D565530F6729E55435463532FDB606DD46EB69C73E29BCD38E13D2A6638C`, matching source DLL;
- Recompiled DLL SHA-256 in independent GitHub release worktree:
  `006C65F503A6DC76D29D7647A1C388DD5152D1250ED1CD821526D3128A115DAE`;
- AVEVA install directory `DesignAddins.xml` SHA-256 maintained:
  `A064B408D876FB8441B412E9F99A0E3A5BDC41AF889D053D3E276608D00DDC04`.

Build artifacts, Python virtual environment, session tokens, and runtime logs reside in Git-ignored `deployment/runtime`, preventing accidental repository check-in.

## 8. Saved vs. Pending Status

### Persisted to Repository

- Python loopback gateway;
- OpenAI Responses Provider;
- Token Rhythm Chat Completions Provider;
- ChangeSet preview, authorization, and execution receipt protocols;
- E3D x86 Add-in source code;
- E3D docked panel;
- AVEVA controlled transaction executor;
- Isolated deployment scripts;
- JSON Schemas;
- Automated test suites;
- English README, static evidence, and this completion report.

### Resident Exclusively at Local Runtime

- Compiled DLLs;
- Isolated Python environment;
- Random bridge tokens;
- PID session files;
- Gateway runtime logs;
- Operator-entered API Keys.

### Awaiting Live Machine Acceptance

Because AVEVA Monitor currently rests at the login screen, the following items are not marked as "Passed":

1. Completing a live model request using an authentic Token Rhythm API Key;
2. Generating a live AI ChangeSet in the Add-in panel;
3. Verifying ChangeSet invalidation in UI upon switching Current Element;
4. Executing a live `DESC` modification and precise read-back on an isolated test element;
5. Verifying undo capability and database non-persistence when default Save Work is unchecked;
6. Injecting a simulated failure to confirm full transaction rollback;
7. Explicitly checking Save Work and reopening project to verify persistence;
8. Confirming duplicate previews, gateway restarts, and duplicate requests create no duplicate writes;
9. Re-auditing final audit files for secret or token leaks.

Additionally, unauthenticated request to `https://tokenrhythm.studio/v1/models` completed TLS handshake with expected `401`, proving the service authentication endpoint is reachable on current network; this does not substitute for validating authentic API Key credentials, account model quotas, or `deepseek-v4-flash` inference.

## 9. Operation Guide

1. Launch isolated Monitor and complete AVEVA user login;
2. Enter Design/Model module;
3. Start the local gateway bound to target `des.exe` PID;
4. Select Provider in the `E3D AI Assistant (Controlled)` panel;
5. Enter API Key strictly within the E3D panel; do not send to chat or store in configuration files;
6. Select a test element;
7. Enter modification prompt and click `Preview Changes`;
8. Review every individual attribute modification;
9. Click `Apply Verified ChangeSet` only after verifying targets and values;
10. For initial testing, do not check `Save Work after verified apply`.

## 10. Conclusion

Code, protocol, provider adaptation, process isolation, controlled write gates, rollback mechanisms, static testing, and isolated deployment for the E3D Live AI Bridge module are complete. The system provides a complete end-to-end technical pipeline for "selection snapshot -> natural language preview -> human verification -> controlled transaction -> read-back audit" in a designated E3D Design process.

This report does not claim unexecuted live API invocations or live E3D database writes as accepted. Final production-ready certification remains contingent on evidence gathered upon completion of the live machine acceptance checklist.
