# PIPE Native Syntax — Round 1 E3D Certification Notes

## Before importing

These macros create independent test SITEs and never write into existing
equipment EQUIs:

- `/CODEX-PIPE-LAB01`
- `/CODEX-PIPE-LAB02`
- `/CODEX-PIPE-LAB03`
- `/CODEX-PIPE-LAB04`
- `/CODEX-PIPE-LAB05`

In E3D Design, select `WORLD` and run:

```
$M <full path to the candidate macro>
```

Each macro runs once. Before re-running, delete or rename the corresponding
`/CODEX-PIPE-LABxx` in E3D, otherwise duplicate element names will interfere
with the verdict.

## Recommended execution order

### 1. `01_pipe_core.pml`

Goal: verify the basic hierarchy, automatic straight tube and common piping
components.

Predicted results:

1. `/CODEX-P01-T01-STRAIGHT`
   - a DN100 horizontal straight pipe;
   - from `E 0 N 0 U 0` to `E 4000 N 0 U 0`;
   - if present, this confirms a BRANCH forms tube automatically between its
     head and tail without an explicit TUBE element.
2. `/CODEX-P01-T02-ELBOW`
   - DN100 pipe rises 2000 mm, then turns West 4000 mm through the elbow;
   - the elbow sits at `E 0 N 5000 U 2000`.
3. `/CODEX-P01-T03-VALVE`
   - DN20 `GASKET → FLANGE → VALVE` assembly;
   - arranged along South.
4. `/CODEX-P01-T04-REDUCER`
   - a vertical downward run;
   - transitions from DN100 to DN80.

If `/A3B/...` is reported undefined, keep the full error. That means the
receiving project's catalogue differs; it is not necessarily a PIPE syntax
error.

### 2. `02_pose_pos_then_ori.pml`

Goal: verify the native component order `POS → ORI`.

Prediction:

- the macro loads;
- DN100 pipe rises 2000 mm from the origin, then turns West 4000 mm;
- the elbow centre is at `E 0 N 0 U 2000`;
- the runs stay continuous with the elbow, no drift.

### 3. `03_pose_ori_then_pos.pml`

Goal: identical to 02 except the ELBOW uses `ORI → POS`.

Compare:

- any direct error;
- whether the elbow still sits at `E 0 N 0 U 2000`;
- whether the runs are broken, drifted or wrongly directed;
- whether the final shape is identical to 02.

Judgement:

- if 03 errors or differs: component order is semantic; `POS → ORI` is
  required for this family;
- if 02 and 03 are identical: the native order is only the exporter's
  canonical serialisation, not an execution constraint.

### 4. `04_tee_branch_refs.pml`

Goal: verify the reciprocal connection between the TEE and a second BRANCH.

Prediction:

- B1 is the main line with one ELBOW and one TEE;
- B2 enters the TEE branch point from North;
- no gap or duplicate tube between B2 and the TEE.

Query respectively:

```
TEE 1 of BRANCH /CODEX-P04-TEE/B1
Q CREF

/CODEX-P04-TEE/B2
Q TREF
```

Expected:

- the TEE's `CREF` points to `/CODEX-P04-TEE/B2 TAIL`;
- B2's `TREF` points to `TEE 1 of BRANCH /CODEX-P04-TEE/B1`.

### 5. `05_slope_1in100.pml`

Goal: verify the slope reference and its direction expression.

Prediction:

- a DN100 straight pipe with 10000 mm horizontal projection;
- falls from `U 100` to `U 0`, i.e. 1:100;
- both PIPE and BRANCH report `SLOREF /1in100`.

Run `Q SLOREF` on the PIPE and on the BRANCH.

## What to report back

1. Exact E3D version and module;
2. whether each macro loaded;
3. for failures: error code, line number and echoed command;
4. whether all four models in 01 display;
5. whether 02 and 03 are identical;
6. the `Q CREF` / `Q TREF` output of 04;
7. the `Q SLOREF` output of 05;
8. screenshots of anything unexpected.

After the results, passing entries are promoted to `VERIFIED`, failing entries
marked `REJECTED`, and the round-2 experiments continue.

## Round 2 supplements

Round 1 established that the green dashed lines represent geometrically
incomplete routes, not solid pipe.

### 6. `06_elbow_arrive2_leave1.pml`

Only restores the native elbow's:

```
ARRI 2
LEAV 1
```

Prediction: both dashed legs become solid tube and stay continuous with the
elbow.

Query on the ELBOW:

```
Q ARRIVE
Q LEAVE
Q ADIR
Q LDIR
```

### 7. `07_reducer_vertical_native_axes.pml`

Only changes the REDUCER to the basis used by native vertical reducers:

```
ORI Y is N and Z is E
```

Prediction: the reducer stands vertically instead of North/South, with the
DN100 and DN80 runs forming solid tube above and below.

Query on the REDUCER:

```
Q ADIR
Q LDIR
Q ABORE
Q LBORE
```
