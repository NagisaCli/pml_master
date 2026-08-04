# TEE/GASKET query — first attempt error (2026-08-04)

## Evidence

User-supplied report file archived under `results/evidence/`:

| File | SHA-256 |
|---|---|
| `evidence/2026-08-04_tee_gasket_query_error.txt` | `F044F47A258F9002650447CD8C8EACFC2DDE505278D276EEBCEEF99FF24A233F` |

## What the report contains

1. `Q ATT` ran on **ZONE 1 of SITE 1 of WORLD** — the query pack was executed
   while a ZONE was current, not a TEE or GASKET. No component attributes were
   captured.
2. `Q NAME ANSWER` then failed:

   ```
   (2,201)   Element ZONE 1 of SITE 1 of WORLD /* does not have attribute ANSW
   In line 21 of Macro ...\queries\12_query_tee_gasket.mac
   ```

## Diagnosis

- `Q NAME ANSWER` is **attribute-specific**: it queries the `ANSWER`
  attribute, which exists on catalogue SPCOs (where it holds the bore) but not
  on ZONE or piping components. It must not be used as a generic
  "named attributes only" query. The earlier reading in `pml1-reference.md`
  was corrected accordingly.
- The pack's instruction "make the TEE current" was not specific enough. The
  current element must be the autonamed TEE/GASKET component under the BRANCH,
  selected in the model hierarchy; a ZONE or BRANCH current element returns
  only that element's attributes.

## Corrected procedure

The pack is now self-navigating — it uses the ordinal reference form from the
native two-pass blocks instead of depending on the current element:

```
TEE 1 of BRANCH /CODEX-PIPE-LAB04/CODEX-P04-TEE/B1
Q ATT
GASKET 1 of BRANCH /CODEX-PIPE-LAB01/CODEX-P01-T03-VALVE/B1
Q ATT
```

Run `$M queries/12_query_tee_gasket.mac`. `/CODEX-PIPE-LAB04` and
`/CODEX-PIPE-LAB01` must exist — re-load candidates 04 and 01 first if they were
deleted. A second attempt with the old pack still returned ZONE attributes
because it queried the current element without navigating; the ordinal form
fixes that.

## Third attempt (same day) — targets no longer exist

The full-path ordinal form parsed correctly but the targets were gone:

```
(2,109)   Undefined name /CODEX-PIPE-LAB04/CODEX-P04-TEE/B1
```

The round-1 lab sites were removed from the receiving project, so no query
against them can succeed. The fix is candidate
`candidate/13_tee_gasket_query_kit.pml`: it creates a fresh
`/CODEX-PIPE-LAB13` (TEE + reciprocal CREF/TREF, GASKET/FLANGE/VALVE
assembly) and immediately prints `Q ATT` for both components in the same
`$M` run. Delete `/CODEX-PIPE-LAB13` before re-running.

## Fourth attempt — post-INPUT path did not resolve

Rev 1 of the kit placed the queries after `INPUT FINISH` with full paths:

```
(2,109)   Undefined name /CODEX-PIPE-LAB13/CODEX-Q13-TEE/B1
```

Two possible causes, both fixed in rev 2: an earlier creation error could have
rolled the INPUT transaction back (the ONERROR handler swallowed it), or a
leading-slash path after `INPUT FINISH` is resolved against the then-current
element rather than from WORLD. Rev 2 therefore runs the `Q ATT` lines
**inside** the INPUT transaction, immediately after the two-pass
OLD/CREF/TREF block, using the same relative references candidate 04 proved,
and removes the ONERROR handler so any creation failure is reported at its
exact line.

Target values to look for: TEE `SPRE SPCOMPONENT /A1A/TA150` and its `CREF`
pointing back at `/CODEX-P04-TEE/B2`; GASKET `SPRE /A3B/GC20`, `RLOC`,
P-points and thickness.
