from __future__ import annotations

import json

import pytest

from wsb.projects import (
    ProjectNotFoundError,
    discover_projects,
    find_project,
    resolve_project,
)


def test_project_metadata_preserves_logical_name_without_renaming_folder(tmp_path):
    project_root = tmp_path / "historical-folder"
    project_root.mkdir()
    (project_root / "project.json").write_text(
        json.dumps({"name": "Logical-Project"}),
        encoding="utf-8",
    )

    projects = discover_projects(tmp_path)
    assert len(projects) == 1
    assert projects[0].name == "Logical-Project"
    assert projects[0].root == project_root
    assert projects[0].macro_path().name == "Logical-Project.pml"

    assert find_project("Logical-Project", tmp_path) == projects[0]
    assert find_project("historical-folder", tmp_path) == projects[0]
    assert resolve_project("logical", tmp_path) == projects[0]


def test_invalid_project_metadata_is_rejected(tmp_path):
    project_root = tmp_path / "bad-project"
    project_root.mkdir()
    (project_root / "project.json").write_text('{"name": ""}', encoding="utf-8")

    with pytest.raises(ProjectNotFoundError, match="non-empty string"):
        discover_projects(tmp_path)
