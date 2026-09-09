# JK_Pump_Build base rebuild r6 — 2026-08-19

## Client correction captured

The r5 E3D reload showed more severe geometry after the end-face adaptation:

- long outer PYRAMID stays passed through the skid and below the foundation;
- highlighted inner PYRAMID gussets still stopped below the mounting top plate.

The two user screenshots were preserved byte-for-byte:

| Evidence | SHA-256 |
|----------|---------|
| `2026-08-19_r5_e3d_pyra_below_foundation.png` | `F3129236C2831EE7AE589ABCF58C4E01CC0A2E506C840A0806A287F3651748E1` |
| `2026-08-19_r5_e3d_inner_pyra_short.png` | `5F45CE8F83724352742D0FCA34D0BF5EAD253E5F57F55CA91EB165B1B37042FF` |

## Root cause and scoped change

r5 wrote each intended lower face directly to PYRAMID POS. E3D PYRAMID POS is
the geometric centre, so its real faces are at `POS +/- HEIG/2` along local Z.

- Every adapted PYRAMID now emits `POS U = (low + high) / 2`.
- The verifier constructs its bottom at local `-HEIG/2` and top at
  `+HEIG/2`, applying XOFF/YOFF to the top face only.
- Elements 6..9 still span sole top to mounting-pad underside.
- Elements 14..19 still span sole top to their corrected native-relative tops.
- Corrected native maxima are pump saddle top `-140` and motor mounting-pad top
  `-173`; earlier `-110/-125` figures came from the rejected end-face datum.
- All non-base geometry, plan arrangement, ORIs, profiles and hardware axes are
  outside the delta.

## Accepted deliverable

`output/2026-08-19_pumps_r6/JK_Pump_Build_2026-08-19_base_rebuild_r6_all_pumps.pml`

SHA-256: `0F9D1FBB4CEF9597C36433F4EB193FBB3E60EAD074F59FBA09BEADBDB84F6E68`

Audit SHA-256:
`3E8FDD82FC343B02E7A10FBAA11858357D22C7F67743ACD9BF9691192D36ADB0`

QA image SHA-256:
`A540BE09B3F5D68A297C32711906EFC26759A9B0B951B531591FB5EC15663EBE`

## Static verification

- 30 pumps, 2616 elements.
- All 12 PYRAMIDs per pump use centre POS and remain above the foundation.
- 4/4 inner-gusset top interfaces and 6/6 outer-stay bottom interfaces per
  pump have zero U gap and positive end-face plan overlap.
- Numeric model verifier: 0 problems.
- Reference/end-face fidelity verifier: 0 problems.
- Emitted macro parser: 0 text-level problems.
- 32/32 injected defects caught, including the r5 bottom-as-POS regression.
- 168/168 non-base SUBE blocks exactly unchanged from r5.
- 972 cooling ribs checked, 0 wrong.

## Client acceptance

The client visually reviewed the r6 E3D result and accepted it on 2026-08-20.
The verbatim verdict is preserved at
`../../results/evidence/2026-08-20_r6_user_acceptance.txt` (SHA-256
`15BB70E08FA32519F18D8E06E12F291966ED4CDA24E07AE4EF5A4A29669D891A`). r6 is
now the current accepted base-rebuild baseline under IR-11d.

## Postmortem: gains, losses and causes

### What was gained

- The complete 43-member reference base was retained while its pump and motor
  stations became genuinely adaptive to all 30 machine envelopes and shaft
  elevations.
- PYRAMID datum behaviour is now evidenced by both the native `/P1501B-BASE`
  numbers and an accepted E3D result, rather than by analogy to another form.
- The verification stack now checks emitted macro geometry, real terminal-face
  contact, foundation bounds and parser inventory, and catches 32 independent
  regressions including the exact r5 bottom-as-POS defect.
- Scope control worked: 168/168 non-base SUBE blocks stayed unchanged through
  the final correction, so iterative base repair did not disturb the accepted
  pumps, motors, nozzles or auxiliary geometry.

### What was lost

- Several locally green candidates required client rejection and rework before
  acceptance. The avoidable cost was iteration time and reduced confidence in
  checks that initially certified the same assumptions as the generator.
- Early adaptations successively lost reference fidelity, frame handedness,
  fastener coaxiality, load-path continuity, terminal-face closure and finally
  the true PYRAMID datum. Each error was narrow, but together they made the base
  visually and structurally wrong.

### Why it happened

1. Member count and world-position ordering were treated as proof of shape,
   without checking member-local ORIs, profiles and machine-relative datums.
2. Generator and verifier shared the same reflected transverse frame, allowing
   a consistent but wrong result to pass.
3. AABB intersection was used as a proxy for a bearing/weld interface; crossing
   tapered solids can satisfy that test while both terminal faces remain open.
4. PYRAMID POS was inferred as a lower face instead of being resolved from the
   native reference. That one datum error shifted both ends by half the member
   height and created both reported symptoms at once.
5. The strongest evidence was the client's E3D view. Static checks were useful
   for containment and regression but could not grant visual acceptance.

### Prevention retained in the project

- Solve every support from named physical low/high interfaces, then emit
  `HEIG = high - low` and centre `POS = (low + high) / 2`.
- Verify actual PYRAMID bottom/top faces, positive plan overlap and zero U gap;
  never certify fabrication contact from AABBs alone.
- Reject every support whose occupied bound reaches below the foundation.
- Parse the emitted macro independently, assert the expected inventory and fail
  loudly if parsing returns less than the complete base.
- Keep exact failure mutations for reflected PYRAMIDs, displaced fasteners,
  detached plates, short inner gussets, floating outer stays and bottom-as-POS.
- Continue to label generated output as a candidate until the client has viewed
  it in E3D.
