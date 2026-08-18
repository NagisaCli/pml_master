"""
Repository hygiene tests.

``test_skill_integrity.py`` guards the knowledge in ``skill/``. Nothing guarded
the *tooling* around it, and three failures grew there unnoticed:

* **Machine-bound paths.** Every ``Projects/JK_Pump_Build/tools/`` script
  resolved repository files through an absolute
  ``C:\\Users\\A\\Desktop\\Projects\\e3d_agent\\...`` path. Those scripts are the
  numeric evidence behind the r9-r14 revision records, so the audit trail was
  reproducible only on one machine and only while the checkout stayed put. The
  r12+ scripts already used ``Path(__file__).resolve().parent.parent``; the rule
  below stops the older idiom from coming back.

* **Verbatim evidence left unprotected.** ``.gitattributes`` pinned
  ``Projects/**/results/evidence/**`` as ``-text`` so ``core.autocrlf`` cannot
  rewrite bytes that ``test_extrusion_study.py`` hashes. A 2026-08-10 record
  landed in ``archive/<date>/evidence/`` instead, which that pattern does not
  match, and would have been silently CRLF-rewritten on the next checkout --
  the exact failure the attribute exists to prevent.

* **Syntax rot in unimported scripts.** Nothing imports the ``tools/`` scripts,
  so a broken edit there is invisible to the rest of the suite until someone
  runs the file by hand, months later, while trying to verify a revision.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECTS_ROOT = REPO_ROOT / "Projects"

# Scripts under Projects/ are standalone: run directly, never imported. They are
# the ones no other test would notice breaking.
PROJECT_SCRIPTS = sorted(
    p for p in PROJECTS_ROOT.rglob("*.py") if "__pycache__" not in p.parts
)


def _is_superseded_archive(script: Path) -> bool:
    """
    True for a script archived as a historical record rather than as a tool.

    An archive directory whose REVISION_RECORD.md declares it SUPERSEDED holds
    files preserved *exactly as written*, defects included -- that is the whole
    point of keeping them. Rewriting one to satisfy a present-day rule would
    falsify the record it exists to be. Such scripts are still required to
    parse; they are exempt only from the path rule.
    """
    for parent in script.parents:
        if parent == PROJECTS_ROOT:
            break
        record = parent / "REVISION_RECORD.md"
        if record.is_file() and "SUPERSEDED" in _text(record):
            return True
    return False

# The repository root as an absolute path is what must never be hardcoded. A
# path pointing *outside* the repository (a user's Desktop export) is legitimate
# -- those inputs really do live there -- so only the self-referential form is
# banned.
REPO_PATH_PATTERN = re.compile(r"[A-Za-z]:\\+[^\"'\n]*?e3d_agent", re.IGNORECASE)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


@pytest.mark.parametrize("script", PROJECT_SCRIPTS, ids=lambda p: p.name)
def test_project_scripts_parse(script: Path):
    """
    Every standalone script must at least be syntactically valid.

    Nothing imports these, so a bad edit stays hidden until the file is run by
    hand -- typically when someone is trying to reproduce a revision check and
    least wants to debug the tool instead.
    """
    try:
        ast.parse(_text(script))
    except SyntaxError as exc:  # pragma: no cover - the failure message is the point
        pytest.fail(f"{script.relative_to(REPO_ROOT)} does not parse: {exc}")


@pytest.mark.parametrize("script", PROJECT_SCRIPTS, ids=lambda p: p.name)
def test_no_hardcoded_repository_paths(script: Path):
    """
    Repository files must be reached relative to the script, not through an
    absolute path containing the checkout location.

    Use the idiom the r12+ tools already share::

        BASE = Path(__file__).resolve().parent.parent
        OUT  = BASE / "output" / "<macro>.pml"

    Scripts in a SUPERSEDED archive are exempt: they are kept verbatim as
    evidence, and editing one to satisfy this rule would falsify the record.
    """
    if _is_superseded_archive(script):
        pytest.skip("superseded archive: preserved verbatim as a historical record")

    offenders = [
        line.strip()
        for line in _text(script).splitlines()
        if REPO_PATH_PATTERN.search(line)
    ]
    assert not offenders, (
        f"{script.relative_to(REPO_ROOT)} hardcodes the repository location:\n  "
        + "\n  ".join(offenders)
        + "\nDerive it from Path(__file__) instead so the script survives a clone."
    )


def test_every_evidence_directory_is_byte_protected():
    """
    Verbatim user evidence is worth exactly its unedited bytes, and
    ``test_extrusion_study.py`` asserts a SHA-256 over it. Any directory named
    ``evidence/`` must therefore be matched by a ``-text`` rule in
    ``.gitattributes``, wherever under ``Projects/`` it happens to sit.

    This caught ``archive/2026-08-10_top_handrails/evidence/``, which the
    original ``results/evidence`` pattern missed.
    """
    attributes = _text(REPO_ROOT / ".gitattributes")
    protected = {
        line.split()[0]
        for line in attributes.splitlines()
        if line.strip() and not line.startswith("#") and "-text" in line
    }
    assert "Projects/**/evidence/**" in protected, (
        "`.gitattributes` must carry `Projects/**/evidence/** -text` so every "
        "evidence directory is protected from core.autocrlf, not only those "
        "under results/."
    )

    evidence_dirs = [
        d for d in PROJECTS_ROOT.rglob("evidence") if d.is_dir()
    ]
    assert evidence_dirs, "expected at least one evidence/ directory to exist"
