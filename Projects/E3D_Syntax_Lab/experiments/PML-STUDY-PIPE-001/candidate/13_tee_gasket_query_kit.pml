$S-  -- Synonym translation OFF
-- PML-STUDY-PIPE-001 / candidate 13 (rev 2)
-- Self-contained TEE CREF + GASKET attribute query kit.
--
-- One $M run: creates an isolated SITE, connects TEE/B2 reciprocally, then
-- prints Q ATT for the autonamed TEE and GASKET. The queries run INSIDE the
-- INPUT transaction, immediately after the two-pass OLD/CREF/TREF block,
-- while the current element is the SITE — the same relative reference form
-- that candidate 04 proved. No world navigation is attempted, because a
-- leading-slash path after INPUT FINISH resolves against the then-current
-- element, not from WORLD.
--
-- There is deliberately no ONERROR handler: if any creation line fails, the
-- error is reported at its exact line instead of being swallowed.
--
-- Re-run: delete /CODEX-PIPE-LAB13 first (or rename the SITE), because
-- duplicate site names abort the creation pass.

INPUT BEGIN
NEW SITE /CODEX-PIPE-LAB13
PURP PIPE

NEW ZONE /CODEX-PIPE-LAB13-ZONE
DESC 'TEE CREF AND GASKET QUERY KIT'
FUNC 'Piping'
PURP PIPE

-- TEE route: candidate 04 shape with the round-2 verified elbow arrive/leave.
NEW PIPE /CODEX-Q13-TEE
BORE 150mm
TEMP 50degC
PRES 0pascal
TPRESS 0pascal
PSPE SPECIFICATION /A1A
DELDSG FALS

NEW BRANCH /CODEX-Q13-TEE/B1
HPOS E 0mm N 0mm U 2000mm
TPOS E 4000mm S 4000mm U 0mm
HDIR E
TDIR N
LHEA true
LTAI true
HBOR 150mm
TBOR 150mm
HCON OPEN
TCON OPEN
HSTU SPCOMPONENT /A1A/PA150
PSPE SPECIFICATION /A1A
DELDSG FALS

NEW ELBOW
POS E 4000mm N 0mm U 2000mm
ORI Y is D and Z is N
BUIL false
SHOP true
SPRE SPCOMPONENT /A1A/EA150
LSTU SPCOMPONENT /A1A/PA150
ARRI 2
LEAV 1
ORIF true
POSF true
DELDSG FALS

END
NEW TEE
POS E 4000mm N 0mm U 0mm
ORI Y is E and Z is U
BUIL false
SHOP true
SPRE SPCOMPONENT /A1A/TA150
LSTU SPCOMPONENT /A1A/PA150
ARRI 3
ORIF true
POSF true
DELDSG FALS
NOMDIR unset

END
END

NEW BRANCH /CODEX-Q13-TEE/B2
HPOS E 4000mm N 3000mm U 0mm
TPOS E 4000mm N 142.87mm U 0mm
HDIR S
TDIR N
LHEA true
LTAI true
HBOR 150mm
TBOR 150mm
HCON OPEN
TCON BWD
HSTU SPCOMPONENT /A1A/PA150
PSPE SPECIFICATION /A1A
DELDSG FALS

END
END

-- GASKET assembly: candidate 01 T03 shape (gasket + flange + valve).
NEW PIPE /CODEX-Q13-GASKET
BUIL false
SHOP false
BORE 20mm
TEMP 50degC
PRES 0pascal
TPRESS 0pascal
PSPE SPECIFICATION /A3B
DELDSG FALS

NEW BRANCH /CODEX-Q13-GASKET/B1
BUIL false
SHOP false
HPOS E 0mm N 12000mm U 0mm
TPOS E 0mm N 11000mm U 0mm
HDIR S
TDIR N
LHEA true
LTAI true
HBOR 20mm
TBOR 20mm
HCON FBD
TCON TUB
TEMP 50degC
PRES 0pascal
TPRESS 0pascal
HSTU SPCOMPONENT /A3B/PA20
PSPE SPECIFICATION /A3B
DELDSG FALS

NEW GASKET
POS E 0mm N 12000mm U 0mm
ORI Y is E and Z is U
BUIL false
SHOP false
SPRE SPCOMPONENT /A3B/GC20
LSTU SPCOMPONENT /A3B/PA20
ORIF true
POSF true
DELDSG FALS

END
NEW FLANGE
POS E 0mm N 11998.5mm U 0mm
ORI Y is E and Z is U
BUIL false
SHOP true
SPRE SPCOMPONENT /A3B/FS20
LSTU SPCOMPONENT /A3B/PA20
ORIF true
POSF true
DELDSG FALS

END
NEW VALVE /CODEX-Q13-V01
POS E 0mm N 11832.48mm U 0mm
ORI Y is E and Z is U
BUIL false
SHOP false
SPRE SPCOMPONENT /A3B/VG20
LSTU SPCOMPONENT /A3B/PA20
ORIF true
POSF true
DELDSG FALS

END
END
END

-- Second pass, then the queries, all while the SITE is current.
OLD TEE 1 of BRANCH /CODEX-Q13-TEE/B1
CREF BRANCH /CODEX-Q13-TEE/B2 TAIL
Q ATT

OLD BRANCH /CODEX-Q13-TEE/B2
TREF TEE 1 of BRANCH /CODEX-Q13-TEE/B1

OLD GASKET 1 of BRANCH /CODEX-Q13-GASKET/B1
Q ATT

END
END
INPUT END SITE /CODEX-PIPE-LAB13
INPUT FINISH

$S+  -- Synonym translation ON
