"""Generate the advanced PIPE study candidates 14-16.

Candidates are sliced verbatim from the preserved native export, then renamed
into isolated SITEs. Nothing is synthesized: a family enters the study with the
exact POS/ORI/SPRE/LSTU/ARRI/LEAV attributes E3D itself exported.

14_advanced_inline_families.pml  - FILTER, CLOSURE, FBLIND, COUPLING, WELD
15_advanced_pose_families.pml    - BEND, OLET, PTAPPING + PIPCARTESIAN
16_connection_first_network.pml  - /100-B-1 B1/B2/B3 verbatim with the
                                   internal reciprocal references (OLET<->B2,
                                   TEE2<->B3); external references dropped.
17_cap_fire_spec.pml             - CAP under /FIRE (known undefined in the
                                   receiving project; probe candidate)
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NATIVE = ROOT.parent.parent / "imports" / "2026-07-30_pipe_native.txt"
CANDIDATE = ROOT / "candidate"


def _lines() -> list[str]:
    return NATIVE.read_text(encoding="utf-8-sig").splitlines()


def _target_lines() -> list[tuple[str, int]]:
    """(family label, 1-based line) for each component chosen for study 14/15."""

    return [
        ("FILTER", 5028),
        ("CLOSURE", 684),
        ("CAP", 13998),
        ("FBLIND", 2374),
        ("COUPLING", 4021),
        ("WELD", 2948),
        ("BEND", 20664),
        ("OLET", 198),
        ("PTAPPING", 3651),
    ]


def _enclosing(line_no: int, lines: list[str], kind: str) -> int:
    for index in range(line_no - 1, -1, -1):
        if lines[index].startswith(f"NEW {kind} "):
            return index + 1
    raise ValueError(f"no enclosing NEW {kind} before line {line_no}")


def _block_end(start_index: int, lines: list[str]) -> int:
    """Index (0-based, inclusive) of the END closing the block at start_index."""

    depth = 1
    for index in range(start_index + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped.startswith("NEW "):
            depth += 1
        elif stripped == "END":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unterminated block")


def _branch_attributes(branch: list[str]) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for line in branch:
        match = re.match(r"^(HBOR|TBOR|PSPE|TEMP|PRES|TPRESS)\s+(.+)$", line.strip())
        if match:
            attrs.setdefault(match.group(1), match.group(2))
    return attrs


def _pipe_header(family: str, branch: list[str]) -> list[str]:
    attrs = _branch_attributes(branch)
    header = [
        f"NEW PIPE /CODEX-Q{family}",
        "BUIL false",
        "SHOP false",
    ]
    bore = attrs.get("HBOR") or attrs.get("TBOR")
    if bore:
        header.append(f"BORE {bore}")
    if "TEMP" in attrs:
        header.append(f"TEMP {attrs['TEMP']}")
    if "PRES" in attrs:
        header.append(f"PRES {attrs['PRES']}")
    if "TPRESS" in attrs:
        header.append(f"TPRESS {attrs['TPRESS']}")
    # The branch attribute line is already "PSPE SPECIFICATION /A3B", so the
    # captured value carries the "SPECIFICATION " keyword; do not re-add it.
    header.append(f"PSPE {attrs.get('PSPE', 'SPECIFICATION /A3B')}")
    header.append("DELDSG FALS")
    return header


def wrap(site: str, description: str, pipes: list[list[str]]) -> str:
    body: list[str] = [
        "$S-  -- Synonym translation OFF",
        "",
        "ONERROR GOLABEL /ERROR3",
        "",
        "INPUT BEGIN",
        f"NEW SITE /{site}",
        "PURP PIPE",
        "",
        f"NEW ZONE /{site}-ZONE",
        f"DESC '{description}'",
        "FUNC 'Piping'",
        "PURP PIPE",
        "",
    ]
    for pipe in pipes:
        body.extend(pipe)
        body.append("END")
        body.append("")
    body.extend(("END", "END", ""))
    body.extend(
        (
            f"INPUT END SITE /{site}",
            "INPUT FINISH",
            "",
            "LABEL /ERROR3",
            "handle ANY",
            "$S+",
            "RETURN ERROR",
            "endhandle",
            "",
            "$S+  -- Synonym translation ON",
            "",
        )
    )
    return "\n".join(body)


def inline_candidate(lines: list[str]) -> tuple[str, str]:
    families = ["FILTER", "CLOSURE", "FBLIND", "COUPLING", "WELD"]
    targets = {name: line for name, line in _target_lines() if name in families}
    pipes: list[list[str]] = []
    for family in families:
        line_no = targets[family]
        pipe_line = _enclosing(line_no, lines, "PIPE")
        branch_line = _enclosing(line_no, lines, "BRANCH")
        end = _block_end(branch_line - 1, lines)
        original_pipe = re.match(r"NEW PIPE (\S+)", lines[pipe_line - 1]).group(1)
        original_branch = re.match(r"NEW BRANCH (\S+)", lines[branch_line - 1]).group(1)
        branch = lines[branch_line - 1 : end + 1]
        branch_text = "\n".join(branch)
        branch_text = branch_text.replace(original_branch, f"/CODEX-Q{family}/B1")
        branch_text = branch_text.replace(original_pipe, f"/CODEX-Q{family}")
        pipe = _pipe_header(family, branch)
        pipe.extend(branch_text.splitlines())
        pipes.append(pipe)
    return wrap(
        "CODEX-PIPE-LAB14",
        "ADVANCED INLINE FAMILY ISOLATION",
        pipes,
    ), "14_advanced_inline_families.pml"


def pose_candidate(lines: list[str]) -> tuple[str, str]:
    families = ["BEND", "OLET", "PTAPPING"]
    targets = {name: line for name, line in _target_lines() if name in families}
    pipes: list[list[str]] = []
    for family in families:
        line_no = targets[family]
        pipe_line = _enclosing(line_no, lines, "PIPE")
        branch_line = _enclosing(line_no, lines, "BRANCH")
        end = _block_end(branch_line - 1, lines)
        original_pipe = re.match(r"NEW PIPE (\S+)", lines[pipe_line - 1]).group(1)
        original_branch = re.match(r"NEW BRANCH (\S+)", lines[branch_line - 1]).group(1)
        branch = lines[branch_line - 1 : end + 1]
        branch_text = "\n".join(branch)
        branch_text = branch_text.replace(original_branch, f"/CODEX-Q{family}/B1")
        branch_text = branch_text.replace(original_pipe, f"/CODEX-Q{family}")
        pipe = _pipe_header(family, branch)
        pipe.extend(branch_text.splitlines())
        pipes.append(pipe)
    return wrap(
        "CODEX-PIPE-LAB15",
        "ADVANCED POSE FAMILY ISOLATION",
        pipes,
    ), "15_advanced_pose_families.pml"


def cap_fire_candidate(lines: list[str]) -> tuple[str, str]:
    line_no = 13998  # CAP /100-FW-201/B1
    pipe_line = _enclosing(line_no, lines, "PIPE")
    branch_line = _enclosing(line_no, lines, "BRANCH")
    end = _block_end(branch_line - 1, lines)
    original_pipe = re.match(r"NEW PIPE (\S+)", lines[pipe_line - 1]).group(1)
    original_branch = re.match(r"NEW BRANCH (\S+)", lines[branch_line - 1]).group(1)
    branch = lines[branch_line - 1 : end + 1]
    branch_text = "\n".join(branch)
    branch_text = branch_text.replace(original_branch, "/CODEX-QCAP/B1")
    branch_text = branch_text.replace(original_pipe, "/CODEX-QCAP")
    pipe = _pipe_header("CAP", branch)
    pipe.extend(branch_text.splitlines())
    return wrap(
        "CODEX-PIPE-LAB17",
        "CAP /FIRE SPEC PROBE",
        [pipe],
    ), "17_cap_fire_spec.pml"


def connection_candidate(lines: list[str]) -> tuple[str, str]:
    pipe_start = _enclosing(34, lines, "PIPE")  # line 16
    next_pipe = next(
        index
        for index in range(pipe_start + 1, len(lines))
        if lines[index].startswith("NEW PIPE ")
    )
    pipe_end = next_pipe - 2  # the END closing /100-B-1 sits before NEW PIPE
    block = lines[pipe_start - 1 : pipe_end + 1]
    text = "\n".join(block).replace("/100-B-1", "/CODEX-Q16-NET")

    # Two-pass reciprocal references that stay inside the slice.
    allowed = re.compile(
        r"^(BRANCH /CODEX-Q16-NET(?!\w)/B[0-9]|"
        r"(?:ELBOW|TEE|OLET|FLANGE|GASKET|REDUCER|VALVE|CLOSURE|INSTRUMENT) [0-9]+ of BRANCH /CODEX-Q16-NET(?!\w)/B[0-9]|"
        r"VALVE /V(?:104|105|106|131)$|"
        r"INSTRUMENT /(?:FE-222|FV-222)$|"
        r"PSPOOL /CODEX-Q16-NET(?!\w)-PS[0-9]+|"
        r"PPLIST [0-9]+ of PIPE /CODEX-Q16-NET(?!\w)|"
        r"PPIECE [0-9]+ of PPLIST [0-9]+ of PIPE /CODEX-Q16-NET(?!\w))"
    )
    kept: list[str] = []
    current: list[str] = []
    in_two_pass = False
    for raw in lines[22349:22780]:
        stripped = raw.strip()
        if stripped.startswith("OLD "):
            in_two_pass = True
            if current:
                target = current[0].strip()[4:].replace(
                    "/100-B-1", "/CODEX-Q16-NET"
                )
                if allowed.match(target):
                    kept.extend(current)
                current = []
        if not in_two_pass:
            continue
        if stripped.startswith(("INPRTR", "OUPRTR")):
            continue
        current.append(raw)
    if current:
        target = current[0].strip()[4:].replace("/100-B-1", "/CODEX-Q16-NET")
        if allowed.match(target):
            kept.extend(current)

    renamed = "\n".join(kept).replace("/100-B-1", "/CODEX-Q16-NET")
    inside = [
        line
        for line in renamed.splitlines()
        if (
            line.strip().startswith("OLD ")
            or (
                "/CODEX-Q16-NET" in line
                and "/CODEX-Q16-NETA" not in line
                and "/CODEX-Q16-NETB" not in line
                and "NOZZLE /" not in line
            )
        )
    ]
    refs = "\n".join(inside)
    body = "\n".join(
        (
            "$S-  -- Synonym translation OFF",
            "",
            "ONERROR GOLABEL /ERROR3",
            "",
            "INPUT BEGIN",
            "NEW SITE /CODEX-PIPE-LAB16",
            "PURP PIPE",
            "",
            "NEW ZONE /CODEX-PIPE-LAB16-ZONE",
            "DESC 'CONNECTION-FIRST NATIVE NETWORK SLICE'",
            "FUNC 'Piping'",
            "PURP PIPE",
            "",
            text,
            "END",
            "END",
            "END",
            "",
            refs,
            f"INPUT END SITE /CODEX-PIPE-LAB16",
            "INPUT FINISH",
            "",
            "LABEL /ERROR3",
            "handle ANY",
            "$S+",
            "RETURN ERROR",
            "endhandle",
            "",
            "$S+  -- Synonym translation ON",
            "",
        )
    )
    return body, "16_connection_first_network.pml"


if __name__ == "__main__":
    source = _lines()
    outputs = [
        inline_candidate(source),
        pose_candidate(source),
        connection_candidate(source),
        cap_fire_candidate(source),
    ]
    for text, filename in outputs:
        path = CANDIDATE / filename
        path.write_text(text, encoding="utf-8", newline="\n")
        print(path)
