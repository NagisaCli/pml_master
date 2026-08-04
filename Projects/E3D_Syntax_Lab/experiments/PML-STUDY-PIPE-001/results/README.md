# E3D Verdict Sheet

Run the candidate files in numeric order. Each creates its own isolated SITE.
Select WORLD before loading a candidate, then use:

```
$M <full path to candidate file>
```

Do not load the same candidate twice without first removing or renaming its
isolated test SITE; duplicate names would contaminate the result.

Record for every file:

| Candidate | Loaded? | Visible result | Queries/results | Screenshot | Verdict |
|---|---|---|---|---|---|
| 01 core | | | | | |
| 02 POS→ORI | | | | | |
| 03 ORI→POS | | | | | |
| 04 TEE refs | | | | | |
| 05 slope | | | | | |
| 06 ELBOW ARR2/LEAV1 | | | | | |
| 07 vertical REDUCER axes | | | | | |
| 08 balanced pipe cluster | | | | | |
| 09 core cluster isolation | | | | | |
| 10 component cluster isolation | | | | | |
| 11 high-density all-component stress | | | | | |

For a failure, capture the exact E3D error number, line and echoed command.
For a successful load, confirm geometry rather than reporting only "loaded".

Minimum useful verdict:

1. E3D version/module;
2. which SITE/PIPE elements appeared;
3. whether tubes and catalogue components rendered;
4. whether the two pose-order candidates match or differ;
5. queried `CREF`, `TREF` and `SLOREF` values;
6. screenshots of any unexpected geometry.
