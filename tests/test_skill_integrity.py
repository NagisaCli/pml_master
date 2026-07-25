"""
Skill integrity tests.

The ``skill/`` directory is knowledge, not code, so nothing else would notice if
it started contradicting itself or the implementation. These tests guard the
failure modes that have actually happened here:

* A stale rule contradicting a verified one. ``pml_knowledge/corpus/`` claimed a
  bottom-face datum and a SUSPEND/RESUME prologue long after both were proven
  wrong, and any model built from it would have reproduced failures F-1 and F-2.
* Documentation drift. The README advertised "427 primitives" against an actual
  403 -- a number nobody re-checked after the geometry changed.
* Broken cross-references, which quietly turn a navigable skill into a pile of
  files.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = REPO_ROOT / "skill"
ENTRY_POINT = REPO_ROOT / "SKILL.md"

SKILL_DOCS = sorted(SKILL_ROOT.rglob("*.md"))
ALL_DOCS = [ENTRY_POINT, *SKILL_DOCS]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_skill_structure_exists():
    """The four sections the entry point promises must all be present."""
    assert ENTRY_POINT.is_file(), "SKILL.md entry point is missing"
    for section in ("knowledge", "workflows", "equipment", "projects"):
        assert (SKILL_ROOT / section).is_dir(), f"skill/{section}/ is missing"
    assert (SKILL_ROOT / "knowledge" / "iron-rules.md").is_file()


# --- Contradiction guards -------------------------------------------------
#
# Each pattern is a claim proven false in E3D. They are matched case-insensitively
# against every skill document. Occurrences are legitimate only where the file is
# explaining that the thing is wrong, so we allow lines that carry an explicit
# negation marker.

_NEGATION_MARKERS = (
    "not ", "never", "no ", "wrong", "banned", "abort", "fail", "error",
    "instead", "previously", "incorrect", "claimed", "rejects", "prohibited",
    "zero ", "cannot", "^^",
)

_FALSE_CLAIMS = (
    # Only flag the phrase where it is *asserted as E3D's datum*. Saying that the
    # builder converts "the bottom-face datum to E3D's centre datum" is correct
    # and must not trip the guard -- drawings really are dimensioned that way.
    (r"\bdatum\b[^.\n]*\bis\b[^.\n]*\bbottom[- ]face\b", "bottom-face datum (F-2 / IR-1)"),
    (r"\bdatum\s*\*{0,2}\s*[:=]\s*\*{0,2}\s*bottom\b", "bottom-face datum (F-2 / IR-1)"),
    (r"\bpos\b[^.\n]*\bis\b[^.\n]*\bbottom[- ]face\b", "bottom-face datum (F-2 / IR-1)"),
    (r"\banti[- ]freeze\b", "anti-freeze prologue (F-1 / IR-4)"),
)


@pytest.mark.parametrize("doc", ALL_DOCS, ids=lambda p: p.name)
def test_no_superseded_claims(doc: Path):
    """No skill document may assert a claim that E3D has already disproved."""
    lines = _text(doc).splitlines()
    for lineno, line in enumerate(lines, start=1):
        lowered = line.lower()
        # Prose wraps, so a refutation ("these are *not* commands") often sits on
        # a neighbouring line. Judge the surrounding context, not one line, or
        # every file that explains a mistake trips its own guard.
        context = " ".join(lines[max(0, lineno - 3):lineno + 2]).lower()
        if any(marker in context for marker in _NEGATION_MARKERS):
            continue  # the passage is describing the error, not asserting it
        for pattern, label in _FALSE_CLAIMS:
            assert not re.search(pattern, lowered), (
                f"{doc.relative_to(REPO_ROOT)}:{lineno} asserts {label}, which is "
                f"false in E3D Mk3.1.11.0:\n    {line.strip()}"
            )


@pytest.mark.parametrize("doc", ALL_DOCS, ids=lambda p: p.name)
def test_no_prologue_commands_presented_as_valid(doc: Path):
    """
    SUSPEND / RESUME / VAR 0 / ALPHA HEADER are not E3D commands. They may be
    named in prose, but never inside a PML code fence, where a reader would copy
    them straight into a macro.
    """
    in_fence = False
    for lineno, line in enumerate(_text(doc).splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            continue
        stripped = line.strip().lstrip("^")
        if re.match(r"^(SUSPEND|RESUME|VAR\s+0|ALPHA\s+HEADER)\b", stripped, re.I):
            # Allowed only when shown as captured error output.
            assert "syntax error" in _text(doc).lower(), (
                f"{doc.relative_to(REPO_ROOT)}:{lineno} shows a non-existent "
                f"command inside a code block: {stripped}"
            )


def test_pml_examples_put_ori_before_pos():
    """
    Every PML example in the skill must obey IR-2. A counter-example in the
    documentation is worse than none: it gets copied.

    Two exemptions, both narrow:

    * **NOZZLE takes the opposite order** - ``POS`` then ``ORI`` - so a block
      opened by ``NEW NOZZLE`` is skipped. Applying the primitive rule to a
      nozzle is itself a documented fault (IR-2).
    * A line explicitly marked ``WRONG`` on that line, or inside a fence whose
      opening region says so. An earlier version accepted the example if the
      word "WRONG" appeared **anywhere in the file**, which exempted every
      example in any document that discussed a mistake - most of them.
    """
    for doc in ALL_DOCS:
        lines = _text(doc).splitlines()
        in_fence = False
        seen_pos = False
        block_is_nozzle = False
        fence_start = 0
        for lineno, line in enumerate(lines, start=1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                seen_pos = False
                block_is_nozzle = False
                fence_start = lineno
                continue
            if not in_fence:
                continue
            stripped = line.strip()
            upper = stripped.upper()
            if upper.startswith("NEW "):
                seen_pos = False
                block_is_nozzle = upper.startswith("NEW NOZZLE")
            elif upper.startswith("POS "):
                seen_pos = True
            elif upper.startswith("ORI ") and seen_pos and not block_is_nozzle:
                # Marked wrong on the line itself, or in this fence's header.
                context = "\n".join(lines[fence_start - 1:lineno])
                assert "WRONG" in context.upper(), (
                    f"{doc.relative_to(REPO_ROOT)}:{lineno} shows ORI after POS "
                    f"on a primitive, violating IR-2"
                )


# --- Drift guards ---------------------------------------------------------


def test_documented_primitive_count_matches_reality():
    """
    The README once advertised 427 primitives against an actual 403. Any figure
    quoted for the WSB package must match what the generator really produces.
    """
    from wsb.generate import generate

    result = generate(timestamp=False)  # in-memory: writes nothing
    actual = {
        "primitive": result.primitive_count,
        "tank": len(result.tanks),
        "nozzle": sum(len(t.nozzles) for t in result.tanks),
    }

    # "403 primitives", "22 tanks", "114 nozzles" -- in any skill or README text.
    pattern = re.compile(
        r"\*{0,2}(\d{2,4})\*{0,2}\s+(primitives|tanks|nozzles)\b", re.I
    )
    singular = {"primitives": "primitive", "tanks": "tank", "nozzles": "nozzle"}

    for doc in [*ALL_DOCS, REPO_ROOT / "README.md"]:
        if not doc.is_file():
            continue
        for lineno, line in enumerate(_text(doc).splitlines(), start=1):
            for value, noun in pattern.findall(line):
                key = singular[noun.lower()]
                assert int(value) == actual[key], (
                    f"{doc.relative_to(REPO_ROOT)}:{lineno} claims {value} {noun}, "
                    f"but the generator produces {actual[key]}. Regenerate and "
                    f"update the figure.\n    {line.strip()}"
                )


def test_internal_links_resolve():
    """A skill is only navigable if its cross-references work."""
    link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    broken = []
    for doc in ALL_DOCS:
        for target in link.findall(_text(doc)):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path = (doc.parent / target.split("#", 1)[0]).resolve()
            if not path.exists():
                broken.append(f"{doc.relative_to(REPO_ROOT)} -> {target}")
    assert not broken, "Broken cross-references:\n  " + "\n  ".join(broken)


def test_knowledge_claims_carry_a_status():
    """
    Knowledge files must state VERIFIED / RECOMMENDED / EXPERIMENTAL somewhere,
    so a reader can tell proven fact from working assumption.
    """
    for doc in sorted((SKILL_ROOT / "knowledge").glob("*.md")):
        text = _text(doc).upper()
        assert any(s in text for s in ("VERIFIED", "RECOMMENDED", "EXPERIMENTAL")), (
            f"{doc.relative_to(REPO_ROOT)} states no confidence level"
        )


# --- Project registry guards ---------------------------------------------


def test_every_project_folder_has_instructions():
    """
    DO.txt is the project's standing requirements. A project without one gives a
    later session nothing to work from but the raw data.
    """
    from wsb.projects import discover_projects

    for project in discover_projects():
        assert project.do_file is not None, (
            f"Projects/{project.name}/ has no DO.txt"
        )


def test_deliverables_are_named_after_their_project():
    """
    Output must carry the project name, which is what lets a macro found later
    be traced back to the folder that produced it and reopened.
    """
    from wsb.projects import discover_projects

    for project in discover_projects():
        assert project.macro_path().name == f"{project.slug}.pml"
        assert project.macro_path().parent == project.output_dir
        stamped = project.macro_path(timestamp="20260724_193000")
        assert stamped.name.startswith(f"{project.slug}_")
        assert stamped.name.endswith(".pml")


def test_generated_macro_lands_in_the_project_folder(tmp_path):
    """End to end: the generator names and places deliverables per project."""
    from wsb import generate, resolve_project

    project = resolve_project("JK-Project")
    result = generate(
        project=project, output_dir=tmp_path, timestamp=False
    )
    assert result.macro_path.name == "JK-Project.pml"
    assert result.report_path.name == "JK-Project_report.md"
    assert result.verified, result.verification_problems


def test_engine_holds_no_project_data():
    """
    The engine must stay generic. A dataset inside wsb/ means the next project
    starts by copying it -- which is how the Iron Rules previously drifted.
    """
    engine = REPO_ROOT / "wsb"
    assert not (engine / "equipment_data.py").exists(), (
        "wsb/equipment_data.py is project data; it belongs in Projects/<name>/"
    )
    for module in engine.glob("*.py"):
        text = module.read_text(encoding="utf-8")
        assert "WSB_TANKS" not in text or module.name == "projects.py", (
            f"{module.name} references a specific project's register"
        )


def test_knowledge_base_loads_the_skill_corpus():
    """
    The machine loader and the human reader must consume the same files, or the
    two sources of truth drift apart -- which is exactly what happened with the
    old pml_knowledge/corpus/.
    """
    from pml_knowledge.knowledge_base import PMLKnowledgeBase

    kb = PMLKnowledgeBase()
    assert "knowledge/iron-rules" in kb.documents, (
        "Knowledge base is not loading the skill corpus"
    )
    assert not (REPO_ROOT / "pml_knowledge" / "corpus").exists(), (
        "The superseded corpus has reappeared; it contradicts skill/knowledge/"
    )

    top = kb.search("primitive position datum centre", top_k=1)
    assert top and top[0]["source"] == "knowledge/iron-rules", (
        "A datum query must retrieve the Iron Rules first"
    )
