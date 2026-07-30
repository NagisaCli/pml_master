"""
Project Registry
================
Locates modeling projects under ``Projects/`` and loads each one's dataset.

Every project is a self-contained folder::

    Projects/<Project-Name>/
        DO.txt              instruction prompt (evolves with the requirements)
        equipment_data.py   the project's dataset
        <source data>       equipment list, reference drawings
        output/             deliverables, named after the project

The engine (``wsb.pml_builder``, ``wsb.tank_builder``, ``wsb.report``) is generic
and lives at the repository root, so an Iron Rule fix applies to every project at
once. Only data and per-project configuration live inside a project folder.

Datasets are loaded by file path rather than imported as a package, so a project
folder needs no ``__init__.py`` and its name is free of Python identifier rules
("JK-Project" contains a hyphen).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import List, Optional, Sequence

__all__ = [
    "PROJECTS_DIR",
    "Project",
    "ProjectNotFoundError",
    "discover_projects",
    "find_project",
    "resolve_project",
]

#: Root of the project registry, beside this package.
PROJECTS_DIR = Path(__file__).resolve().parent.parent / "Projects"

#: The per-project instruction prompt. Matched case-insensitively, because the
#: file has been written as DO.txt, Do.txt and ClaudeDo.txt at different times.
_DO_NAMES = ("do.txt", "claudedo.txt")

#: The module inside a project folder that defines its equipment.
_DATASET_FILENAME = "equipment_data.py"

#: Optional metadata allows a stable logical project/output name when the
#: on-disk folder was created under a different historical name.
_METADATA_FILENAME = "project.json"


class ProjectNotFoundError(LookupError):
    """Raised when a named project cannot be located under ``Projects/``."""


@dataclass(frozen=True)
class Project:
    """A modeling project: its folder, instructions, and dataset."""

    name: str
    root: Path

    # -- Locations -----------------------------------------------------

    @property
    def do_file(self) -> Optional[Path]:
        """The project's instruction prompt, if it has one."""
        for child in sorted(self.root.iterdir()):
            if child.is_file() and child.name.lower() in _DO_NAMES:
                return child
        return None

    @property
    def dataset_path(self) -> Optional[Path]:
        """The project's ``equipment_data.py``, if it has one."""
        path = self.root / _DATASET_FILENAME
        return path if path.is_file() else None

    @property
    def output_dir(self) -> Path:
        """Where this project's deliverables belong."""
        return self.root / "output"

    # -- Naming --------------------------------------------------------

    @property
    def slug(self) -> str:
        """
        Base filename for this project's deliverables.

        Output is named after the project so that a macro can be traced back to
        the folder that produced it, and reopened in a later session without
        guesswork. Spaces become underscores; the name is otherwise preserved.
        """
        return self.name.replace(" ", "_")

    def macro_path(self, *, timestamp: Optional[str] = None) -> Path:
        """Path for this project's ``.pml`` macro."""
        suffix = f"_{timestamp}" if timestamp else ""
        return self.output_dir / f"{self.slug}{suffix}.pml"

    def report_path(self, *, timestamp: Optional[str] = None) -> Path:
        """Path for this project's engineering report."""
        suffix = f"_{timestamp}" if timestamp else ""
        return self.output_dir / f"{self.slug}{suffix}_report.md"

    # -- Content -------------------------------------------------------

    def instructions(self) -> str:
        """The DO.txt text, or an empty string when the project has none."""
        do_file = self.do_file
        return do_file.read_text(encoding="utf-8") if do_file else ""

    def load_dataset(self) -> ModuleType:
        """
        Import this project's ``equipment_data.py`` from its file path.

        Loaded under a namespaced module name so two projects can each define a
        dataset without colliding in ``sys.modules``.
        """
        path = self.dataset_path
        if path is None:
            raise ProjectNotFoundError(
                f"Project '{self.name}' has no {_DATASET_FILENAME}. "
                f"Expected it at {self.root / _DATASET_FILENAME}"
            )

        module_name = f"_e3d_project_{self.slug.replace('-', '_')}"
        cached = sys.modules.get(module_name)
        if cached is not None:
            return cached

        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:  # pragma: no cover - unreachable
            raise ImportError(f"Cannot load dataset for '{self.name}' from {path}")

        module = importlib.util.module_from_spec(spec)
        # Registered before execution so a dataclass defined inside the dataset
        # can resolve its own module during creation.
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(module_name, None)
            raise
        return module

    def tanks(self) -> Sequence:
        """The project's equipment register."""
        dataset = self.load_dataset()
        for attribute in ("WSB_TANKS", "TANKS", "EQUIPMENT"):
            tanks = getattr(dataset, attribute, None)
            if tanks is not None:
                return tanks
        raise AttributeError(
            f"{self.dataset_path} defines no equipment register "
            f"(expected WSB_TANKS, TANKS or EQUIPMENT)"
        )


def discover_projects(projects_dir: Optional[Path] = None) -> List[Project]:
    """Every project folder under ``Projects/``, sorted by name."""
    root = projects_dir or PROJECTS_DIR
    if not root.is_dir():
        return []
    projects: List[Project] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith((".", "_")):
            continue
        name = child.name
        metadata_path = child / _METADATA_FILENAME
        if metadata_path.is_file():
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ProjectNotFoundError(
                    f"Invalid project metadata at {metadata_path}: {exc}"
                ) from exc
            configured_name = metadata.get("name")
            if not isinstance(configured_name, str) or not configured_name.strip():
                raise ProjectNotFoundError(
                    f"{metadata_path} must define a non-empty string 'name'"
                )
            name = configured_name.strip()
        projects.append(Project(name=name, root=child))
    return projects


def find_project(
    name: str, projects_dir: Optional[Path] = None
) -> Optional[Project]:
    """
    Locate a project by name.

    Matching is deliberately forgiving -- exact, then case-insensitive, then
    unique partial -- because the name reaches this function from a user's
    prompt ("the JK project") as often as from a command line.
    """
    projects = discover_projects(projects_dir)
    if not projects:
        return None

    for project in projects:
        if project.name == name or project.root.name == name:
            return project

    lowered = name.lower()
    for project in projects:
        if project.name.lower() == lowered or project.root.name.lower() == lowered:
            return project

    partial = [
        project
        for project in projects
        if lowered in project.name.lower() or lowered in project.root.name.lower()
    ]
    return partial[0] if len(partial) == 1 else None


def resolve_project(
    name: Optional[str] = None, projects_dir: Optional[Path] = None
) -> Project:
    """
    Resolve the project to work on, raising a helpful error when ambiguous.

    With no name, resolves to the only project when exactly one exists; with
    several, it refuses to guess rather than silently modelling the wrong one.
    """
    projects = discover_projects(projects_dir)
    root = projects_dir or PROJECTS_DIR

    if not projects:
        raise ProjectNotFoundError(f"No project folders found under {root}")

    if name is None:
        if len(projects) == 1:
            return projects[0]
        available = ", ".join(p.name for p in projects)
        raise ProjectNotFoundError(
            f"Several projects exist ({available}); name the one to model, "
            f"e.g. --project {projects[0].name}"
        )

    project = find_project(name, projects_dir)
    if project is None:
        available = ", ".join(p.name for p in projects) or "none"
        raise ProjectNotFoundError(
            f"No project matching '{name}' under {root}. Available: {available}"
        )
    return project
