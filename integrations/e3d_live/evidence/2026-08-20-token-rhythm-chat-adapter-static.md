# Token Rhythm Chat Completions Adapter - Static Evidence

Date: 2026-08-20

## Scope

This change is confined to `integrations/e3d_live` and its bridge tests. It
does not import or modify the E3D modeling skill, project geometry generators,
or another project knowledge source.

## Implemented provider boundary

- Existing provider retained: `openai_responses`.
- New provider: `token_rhythm_chat`.
- Fixed provider endpoint: `https://tokenrhythm.studio/v1`.
- Documented default model: `deepseek-v4-flash`.
- SDK call shape: `client.chat.completions.create(model=..., messages=...,
  stream=False)`.
- The bridge token and bridge session ID are excluded from the external model
  payload.
- API keys are accepted only through the authenticated loopback configuration
  message, cleared from the E3D password field, held in gateway memory, and
  excluded from responses, session files, and audit records.
- Placeholder values `YOUR_API_KEY`, `sk_xxx`, and `MODEL_ID` fail closed.
- The Token Rhythm base URL is pinned by the provider profile; HTTP, embedded
  credentials, query strings, fragments, and unrelated endpoints fail closed.
- Chat output must be one direct JSON object and pass the same local typed
  ChangeSet, target, scope, expected-value, operation-count, and attribute
  allowlist validation as the official provider.
- Reconfiguring a provider clears cached previews and pending ChangeSets. An
  in-flight preview from the prior provider is rejected before registration.

## E3D panel

The panel now presents:

- `Token Rhythm (Chat Completions)` (default), with the documented endpoint and
  `deepseek-v4-flash` prefilled;
- `OpenAI (Responses)`, with the existing fixed OpenAI model prefilled;
- an editable model ID and a password-masked API key field.

The default Token Rhythm workflow therefore requires only the API key. The
model remains editable because actual account availability may differ.

## Verification

- Focused bridge suite: `36 passed`.
- Full current local-work baseline suite: `565 passed, 4 skipped`.
- Clean release branch based on `origin/main`: bridge suite `36 passed`; full
  baseline suite `322 passed, 2 failed, 2 skipped`. The two existing failures
  are SHA-256 assertions for pipe-study evidence files in
  `tests/test_pipe_study.py`; they are outside this module and were not folded
  into the isolated bridge commit.
- Pinned isolated OpenAI SDK import: `3.3.1`.
- x86 Add-in build: succeeded.
- Source DLL SHA-256:
  `00A0D565530F6729E55435463532FDB606DD46EB69C73E29BCD38E13D2A6638C`.
- Isolated runtime DLL SHA-256:
  `00A0D565530F6729E55435463532FDB606DD46EB69C73E29BCD38E13D2A6638C`.
- Clean release-worktree DLL SHA-256:
  `006C65F503A6DC76D29D7647A1C388DD5152D1250ED1CD821526D3128A115DAE`.
- Installed AVEVA `DesignAddins.xml` remained:
  `A064B408D876FB8441B412E9F99A0E3A5BDC41AF889D053D3E276608D00DDC04`.

## Remaining live boundary

No real Token Rhythm request was sent because no API key was supplied to the
test harness. Live acceptance still requires the operator to authenticate in
AVEVA, open Design, enter the API key in the controlled panel, and run a
preview. No E3D write is accepted merely from this static evidence.
