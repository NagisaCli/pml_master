# E3D Live Bridge Robustness and Feasibility Evidence

Date: 2026-08-20

Status: **AUTOMATED ROBUSTNESS VERIFIED; live E3D write feasibility pending.**

## Concrete risks found and corrected

- Parallel duplicate preview requests could enter the provider lane together.
  Preview execution is now serialized, preserving exactly one provider call,
  one cached response, and one registered ChangeSet per request ID.
- A result receipt was not previously bound strongly enough to the authorized
  operation sequence. Terminal receipts now validate the ordered operation
  prefix, attributes, before/requested values, terminal statuses, persistence,
  and same-request payload identity.
- A gateway bound only by PID could outlive the original E3D process and face a
  later PID reuse. On Windows it now waits on a handle to the exact target
  process and shuts down when that process exits.
- The health endpoint previously exposed session metadata without the session
  token. It is now loopback-only and authenticated like the control endpoints.
- Unexpected request exceptions could expose provider or internal text. The
  HTTP boundary now returns a fixed sanitized failure and remains available.
- Session gateway metadata could express URL variants beyond the intended
  endpoint. The Add-in now accepts only an exact
  `http://127.0.0.1:<port>/` origin.

## Automated evidence

- Focused bridge suite: `36 passed`.
- Full current local-work baseline suite: `565 passed, 4 skipped`.
- Clean release branch focused suite: `36 passed`.
- Clean release branch full suite: `322 passed, 2 failed, 2 skipped`. The two
  failures are pre-existing SHA-256 assertions in `tests/test_pipe_study.py`
  and have no import, file, or test dependency on this integration.
- Forty parallel calls with one preview request ID produced one provider call,
  one accepted preview, one active ChangeSet, and identical client responses.
- A short-lived child process caused the exact-process watchdog to request
  gateway shutdown after the original process exited.
- Unauthenticated `/health` returned `401`; the same endpoint with the bridge
  token returned the session health record.
- Fault-injection tests rejected false success, reordered or missing execution
  results, altered terminal retry payloads, and secret-bearing exception text.
- The Token Rhythm adapter test constructed the official Python SDK with the
  fixed base URL, operator API key, 60-second timeout, and three SDK retries,
  then exercised `chat.completions.create` without a network request.
- Python bytecode compilation, JSON parsing, and the x86 Add-in build passed.
- Current source Add-in DLL SHA-256:
  `00A0D565530F6729E55435463532FDB606DD46EB69C73E29BCD38E13D2A6638C`.
- Isolated runtime Add-in DLL SHA-256:
  `00A0D565530F6729E55435463532FDB606DD46EB69C73E29BCD38E13D2A6638C`.
- The installed AVEVA `DesignAddins.xml` remained unchanged at SHA-256:
  `A064B408D876FB8441B412E9F99A0E3A5BDC41AF889D053D3E276608D00DDC04`.
- Clean release-worktree Add-in DLL SHA-256:
  `006C65F503A6DC76D29D7647A1C388DD5152D1250ED1CD821526D3128A115DAE`.

## Network feasibility evidence

An unauthenticated TLS request to `https://tokenrhythm.studio/v1/models`
reached the endpoint and returned HTTP `401`. This supports endpoint and
authentication-entry reachability only. It does not prove that an operator key
is valid, that the account can use `deepseek-v4-flash`, or that a model response
conforms to the local ChangeSet contract.

## Remaining live feasibility boundary

The following require a real isolated E3D Design session and cannot be inferred
from unit tests or native API signatures:

1. AVEVA `SetAttribute(double)` database-unit behavior and exact readback
   formatting for every numerical allowlisted attribute.
2. Real `UndoTransaction.AbortTransaction()` behavior after an injected
   mid-ChangeSet write or readback failure.
3. Unsaved-session undo behavior and explicit `SaveWork` persistence after
   closing and reopening the project.
4. Provider authentication, selected-model availability, structured response
   quality, timeout behavior, and E3D panel recovery after provider failure.
5. Repeated preview, gateway restart, duplicate authorization, and process exit
   under the real E3D UI event lifecycle.

No production-readiness or live-write acceptance claim is made until these
items are observed and recorded against the isolated target process.
