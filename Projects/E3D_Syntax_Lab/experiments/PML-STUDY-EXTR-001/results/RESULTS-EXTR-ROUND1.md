# EXTRUSION Round 1 — user E3D results (2026-08-04)

## Evidence

User-supplied report files archived under `results/evidence/`:

| File | SHA-256 |
|---|---|
| `evidence/2026-08-04_EXTR02_user_report.txt` | `418D0B31C0FB58467480C8EA518A007F4292E49747C6FFF60DE51B7D82EDE6C8` |

Chat-confirmed results on the same date:

- Candidate 01: occupied U 1000..1800 for `POS U 1000` / `HEIG 800` —
  end-plane datum, `HEIG` toward +Z. **VERIFIED.**
- Candidate 03: A/C (POS->ORI) and B/D (ORI->POS) occupied ranges identical —
  assignment order independent. **VERIFIED.**

## Candidate 02 — measured attributes

`Q ATT` on the three elements of `/CODEX_EXTR_FASTENER_ASSEMBLY`:

| Element | POS | ORI | Size | Occupied U |
|---|---|---|---|---|
| CYLINDER 1 | E 0 N 0 U 60 | Y is N and Z is U | DIAM 15, HEIG 100 | 10..110 |
| EXTRUSION 1 | E 0 N 0 U 20 | Y is N and Z is U | HEIG 20 | 20..40 |
| EXTRUSION 2 | E 0 N 0 U 100 | Y is N and Z is U | HEIG 20 | 100..120 |

User's visual observation: the assembly is coaxial and reads as a vertical
stem with two lateral bars; the upper head appears seated on the top of the
shaft, while the lower head is threaded on the lower shaft with the shaft
protruding below it.

## Expected contact contract — derived from the native specimen

Candidate 02 was emitted without a stated contact expectation. The native
`/PMP-10` data (2026-08-03, shank at E 317 S 1274.99 D 313 with heads at
D 348 and D 288) now defines it. With the verified end-plane datum:

| Feature | Native relationship | In candidate 02 terms (shank U 10..110) |
|---|---|---|
| Lower head | Profile plane 10 mm above the shank lower end; shank protrudes 10 mm | POS U 20, occupies 20..40 — **already correct** |
| Upper head | Profile plane flush with the shank upper end; top faces coincide | should be POS U 90 (90..110) — candidate 02 emitted 100 (100..120, 10 mm proud) |

The native pattern is therefore: both heads are coaxial hex *nuts* on the
shank — the lower one inset 10 mm from the end, the upper one flush — not caps
outside the shank.

## Disposition

- Candidate 02 stays archived as measured (its upper head is 10 mm proud).
- Candidate `04_extruded_hex_fastener_native_contact.pml` reproduces the
  native contract: shank POS U 60, lower head POS U 20, upper head POS U 90.
  Awaiting E3D visual confirmation.
