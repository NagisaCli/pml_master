# Read-Only Live Bridge Round-Trip Evidence — 2026-08-20

Status: **VERIFIED for the phase-1 read-only transport and panel; database
mutation remains disabled and unverified.**

## Runtime scope

- AVEVA E3D Design Mk3.1.11.0
- E3D process ID: `9540`
- Scope: `APS / ALL / DESIGN`
- Protocol: `1.0`
- Deployed Add-in SHA-256:
  `B608092878439CAF61B6E5C1453015DE3C08920CDE34A5D6D20E52AC8DDBEDF8`

## Observed result

The project-local CAF deployment loaded the docked panel titled
`E3D AI Assistant (Read Only)`. Windows Graphics Capture showed:

- green status `READ-ONLY: gateway response received`;
- selection `/pump_cad` with four allowlisted attributes;
- gateway response status `read_only`;
- response `changes: []` and `persistence: none`;
- message `No E3D changes were generated.`

The loopback gateway health endpoint independently reported four accepted
selection snapshots for PID `9540`. The last accepted request ID was
`f6846b3b-29fd-47f9-9273-3ee88e4ea923`.

## Operator confirmation

The operator subsequently confirmed that changing the selected E3D element
updated the assistant panel each time. The independently queried gateway count
rose from four to ten accepted snapshots. The last request ID after that test was
`8c73946b-64df-4050-96dd-411f22b7b3f4`.

## Verification boundary

The repository suite passed `540 passed, 4 skipped`. This evidence verifies
process targeting, scope checks, Current Element capture, request authentication,
loopback transport, response display, and an empty change contract. It does not
verify database writes, Save Work, or model persistence; none of those paths
exist in this build. Operator confirmation of an unchanged E3D database change
list remains pending.
