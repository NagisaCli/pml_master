# Candidate 08 Application Crash — 2026-07-30

## Evidence

- User-supplied SIR:
  `SIR-20260730-184519-collections-addin-crash.txt`
- SHA-256:
  `4ABB9671646F22EFBCEC507734A7F4EBD211C5C0125B000F0D821D02CB487CC3`
- Independent delete-operation SIR:
  `SIR-20260730-185650-delete-crash.txt`
- Delete SIR SHA-256:
  `13B35F12689C3118183151A60DC45119DEA5594B13553DE15A421D5AE6A86DEF`
- Runtime:
  AVEVA Everything3D 3.1, E3D Design Mk3.1.11.0[Z31110-056]

## Observed failure

This is not a PML command error. The SIR contains no `(group,error)` CP
diagnostic, macro line number or echoed command.

The application records this sequence:

1. `Failed to start Collections Addin`;
2. `SEHException` while `MyDataAddin` reads a database element name;
3. later `NullReferenceException` in
   `MyDataCollectionSystem.mSystemCollection_CollectionChanged`;
4. the event is raised through `DrawListManager_Changed`;
5. `des.exe : A fatal error has been detected. Design must exit.`

The immediate crash path is therefore the failed Collections/My Data add-in
responding to a draw-list change. Candidate 08 may have triggered the draw-list
event, but the SIR does not identify any PIPE/BRANCH command as invalid.

The second SIR reproduces the same startup failure during deletion of an
existing project element. Its later trigger is:

```
DeleteCommand.Execute
  -> DBCallbacks.PostClaim
  -> DatabaseService_ClaimRelease
  -> MyDataCollectionClaimlist.DatabaseService_ClaimRelease
  -> MyDataCollectionSystem.mSystemCollection_CollectionChanged
  -> NullReferenceException
  -> Design must exit
```

Read-only browsing remains normal. This confirms the failure boundary is a
database mutation/claim or draw-list event reaching an incompletely initialised
My Data collection handler, not PIPE syntax.

The installed `D:\AVEVA\Everything3D3.1\DesignAddins.xml` explicitly loads
`MyDataAddin`; `CAF_ADDINS_PATH` is not set in the inspected shell. AVEVA's
official .NET customisation guide permits a copied module add-in configuration
to be selected through `CAF_ADDINS_PATH`. A reversible isolation test is
therefore to point a test launch at a copy of `DesignAddins.xml` with only
`MyDataAddin` removed. Do not edit the installation copy.

## Isolation package

- Candidate 09: straight and sloped free branches only.
- Candidate 10: verified ELBOW and vertical REDUCER routes only.

Run them separately in a fresh session. The results distinguish:

- both crash before producing a CP error → Collections/My Data add-in/session
  problem;
- 09 passes, 10 fails with a PML error → capture the new SIR/alert containing
  the exact component command;
- both pass → candidate 08 exposed a batch/draw-list update problem rather than
  a syntax defect.

State: Collections/My Data add-in mutation-event crash confirmed independently
of candidate 08. No PIPE syntax rejection has been observed.

## Follow-up after reset

The user reset the E3D session and then imported the elbow again; it completed
and displayed normally. This is a successful environment recovery signal for
the previously observed add-in/session state. It is not yet a certification of
candidate 11, so the high-density package should still be loaded as a separate
stress run with a fresh SIR if the application exits.
