"""
Shared test bootstrap.

Two import paths have to work no matter what the checkout is called or where it
sits:

* ``wsb``, ``pumpcad``, ``skill`` … — top-level packages inside the repository.
  Individual test modules each did their own ``sys.path.insert`` for these;
  doing it once here means a new test module does not have to remember.

* ``e3d_agent`` — ``tests/test_stability.py`` imports the orchestrator as
  ``from e3d_agent.agent import E3DAgent``, i.e. by the repository's *own*
  directory name. That only resolves when the checkout happens to be named
  ``e3d_agent`` and its parent is on ``sys.path``. Clone the repository under
  any other name and the import fails at collection time, which aborts the
  entire suite -- not just that module -- so every unrelated test disappears
  too. That is exactly what happened when this repository was first cloned to a
  scratch directory: 454 passing tests became "1 error during collection".

  Registering the repository root under the alias ``e3d_agent`` makes the
  existing imports resolve on their own terms, without rewriting them and
  without depending on what the directory is called.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Let `import wsb`, `import pumpcad`, ... find the packages in the repository.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _register_self_alias(alias: str = "e3d_agent") -> None:
    """
    Make the repository importable as `alias`, whatever the directory is named.

    The repository root is itself a package (it has __init__.py). Loading it
    under a fixed name decouples `from e3d_agent.agent import ...` from the
    checkout's directory name.
    """
    if alias in sys.modules:
        return

    init = REPO_ROOT / "__init__.py"
    if not init.is_file():  # pragma: no cover - repository layout changed
        return

    spec = importlib.util.spec_from_file_location(
        alias, init, submodule_search_locations=[str(REPO_ROOT)]
    )
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        return

    module = importlib.util.module_from_spec(spec)
    # Register before executing so that submodule imports performed during
    # execution resolve against the alias rather than re-entering here.
    sys.modules[alias] = module
    try:
        spec.loader.exec_module(module)
    except Exception:  # pragma: no cover - leave the failure to the test
        del sys.modules[alias]
        raise


_register_self_alias()
