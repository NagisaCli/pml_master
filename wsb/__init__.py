"""
WSB Tank Modeling Package
=========================
Generates engineering-grade AVEVA E3D models for tank-type equipment in the
Pulp Mill Washing, Screening and Bleaching area.

This package is the generic engine. Equipment datasets are **project data** and
live in the project's own folder under ``Projects/<name>/equipment_data.py``,
loaded through :mod:`wsb.projects`. Keeping the engine here means an Iron Rule
fix applies to every project at once instead of being copied per project.

Typical use::

    from wsb import generate, resolve_project

    result = generate(project=resolve_project("JK-Project"))
    print(result.macro_path, result.report_path)

Or from the command line::

    python -m wsb --project JK-Project
"""

from .generate import GenerationResult, generate
from .pml_builder import PMLBuilder, PMLValidationError, validate_pml
from .projects import (
    PROJECTS_DIR,
    Project,
    ProjectNotFoundError,
    discover_projects,
    find_project,
    resolve_project,
)
from .report import build_report
from .tank_builder import TankBuilder, build_tank, verify_bottom_centre

__all__ = [
    "PROJECTS_DIR",
    "GenerationResult",
    "PMLBuilder",
    "PMLValidationError",
    "Project",
    "ProjectNotFoundError",
    "TankBuilder",
    "build_report",
    "build_tank",
    "discover_projects",
    "find_project",
    "generate",
    "resolve_project",
    "validate_pml",
    "verify_bottom_centre",
]

__version__ = "1.0.0"
