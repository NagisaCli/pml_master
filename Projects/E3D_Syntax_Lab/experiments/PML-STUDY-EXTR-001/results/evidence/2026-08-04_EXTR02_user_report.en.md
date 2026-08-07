# EXTR-02 user report — English rendering (2026-08-04)

**This is a translation, not evidence.** The record of what the user observed
is `2026-08-04_EXTR02_user_report.txt`, and that file is the one to cite. This
rendering exists only so a non-Chinese reader can follow the observation; where
the two disagree, the original is right.

| | |
|---|---|
| Source | [`2026-08-04_EXTR02_user_report.txt`](2026-08-04_EXTR02_user_report.txt) |
| Source SHA-256 | `418D0B31C0FB58467480C8EA518A007F4292E49747C6FFF60DE51B7D82EDE6C8` |
| Translated | 2026-08-07 |
| Covers | The closing observation only. The `Q ATT` output above it is already English and is not reproduced here — read it from the original. |

Per IR-12, the original must never be translated, reformatted or edited in
place. If the source is ever re-captured, update the hash above and re-check
this rendering against it.

---

## The user's closing observation

> 管道同轴，整体是像一个"干"，你没有给出你对于这个的预期表现，这里只有一些数据，看起来上面的螺帽是完美套在轴的上端，但是下面的螺帽是串在下轴的的，穿出一部分；

Rendered:

> The pipe is coaxial. The whole thing looks like the character 干 — you didn't
> state what you expected it to look like, there's only data here. The upper nut
> looks as though it sits perfectly over the top end of the shaft, but the lower
> nut is skewered onto the lower shaft with part of the shaft passing through
> and out of it.

## Notes on the rendering

Two words carry geometric meaning and lose it in a loose translation:

- **像一个"干"** — the character 干 used as a picture, not as a word: an upright
  stroke crossed by two horizontal bars. That is a description of the shape
  under test — a shank with two heads on it — and it is why
  `RESULTS-EXTR-ROUND1.md` describes the assembly as "a vertical stem with two
  lateral bars". "Looks like a stem" would drop the two bars, which are the
  whole point.
- **串** — skewered or threaded *through*, as food on a skewer. It says the
  shaft passes through the lower nut and emerges past it. "Threaded onto" would
  suggest a screwed-on cap sitting outside the shank, which is the opposite of
  what was measured.

Both distinctions matter to the conclusion: the heads are hex **nuts on** the
shank, not caps **outside** it, and the lower one has the shank protruding
through it. See "Expected contact contract" in
[`../RESULTS-EXTR-ROUND1.md`](../RESULTS-EXTR-ROUND1.md).

## What this observation established

- The assembly is **coaxial** — confirmed by the `Q ATT` block in the original
  (all three elements at E 0 N 0).
- The **upper head is proud**: candidate 02 emitted `POS U 100`, occupying
  100..120 against a shank ending at 110, so it stands 10 mm above the shaft
  top rather than flush. Candidate 04 corrects this to `POS U 90`.
- The **lower head is already correct**: at `POS U 20` it occupies 20..40 with
  the shank starting at 10, so the shank protrudes 10 mm below it — which is
  the native `/PMP-10` relationship.

The user also noted that no expected appearance had been stated for candidate
02 before it was submitted. That gap is what the contact contract in
`RESULTS-EXTR-ROUND1.md` was written to close.
