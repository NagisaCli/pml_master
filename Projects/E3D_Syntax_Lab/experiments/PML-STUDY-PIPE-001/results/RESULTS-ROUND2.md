# Round 2 E3D Results — User Observed 2026-07-30

E3D version: AVEVA Everything3D 3.1, E3D Design
Mk3.1.11.0[Z31110-056].

## Evidence files

| Candidate | Screenshot | SHA-256 |
|---|---|---|
| 06 | `06_elbow_arrive2_leave1_pass.png` | `46146B0146769A668E95578F4480B30193A1063ACC31AB1C67685EA31C7DF901` |
| 07 | `07_reducer_vertical_native_axes_pass.png` | `BE303ABBE66E4F2C82115964A0951FCF4F3A4A12C844FCD045FEF72CEC59F597` |

## Candidate 06 — ELBOW Arrive 2 / Leave 1

User verdict: “完美符合预期”.

The screenshot shows:

- one continuous solid DN100 vertical leg;
- one continuous solid horizontal West leg;
- both legs meet the ELBOW without the green dashed/ill-defined display seen
  in round 1;
- Model Explorer shows ELBO 1 owned by the intended BRANCH.

Conclusion: for this native `/A3B/EA100` Up-to-West elbow contract, restoring
`ARRI 2` and `LEAV 1` repairs the logical route. State: `VERIFIED` in E3D
Design Mk3.1.11.0.

## Candidate 07 — vertical REDUCER native axes

User verdict: “完美符合预期”.

The screenshot shows:

- REDU 1 centred in a vertical BRANCH;
- both adjacent legs are solid and coaxial;
- branch attributes show head at U 3000, tail at U 0, HDIR D, TDIR U,
  HBOR 100 mm and TBOR 80 mm;
- the reducer visibly transitions between the two bores without the
  North/South misalignment from round 1.

Conclusion: `ORI Y IS N AND Z IS E` is the accepted native vertical basis for
the tested `/A3B/RC100X80` reducer. State: `VERIFIED` in AVEVA Everything3D
3.1.
