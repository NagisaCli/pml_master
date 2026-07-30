"""Semantic comparison for generated and native-exported E3D PML files.

The comparator deliberately ignores comments, blank lines, whitespace and
numeric formatting differences.  It compares the hierarchy and the attributes
owned by each ``NEW`` element, which makes a manual E3D edit visible without
burying it in a conventional line-by-line diff.

Run it directly:

    python -m wsb.pml_compare accepted.pml manual-export.pml
    python -m wsb.pml_compare accepted.pml manual-export.pml --format json

The newer/native export is not rewritten.  The report is an input to the
reconciliation workflow in ``skill/workflows/reconciling-native-exports.md``.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
from typing import Iterable, Sequence


_NEW_RE = re.compile(
    r"^NEW\s+(?P<kind>[A-Za-z][A-Za-z0-9]*)"
    r"(?:\s+/(?P<name>\S+))?\s*$",
    re.IGNORECASE,
)
_NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_.])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?"
)
_IGNORED_COMMANDS = {"END", "SAVEWORK"}


def _normalise_number(match: re.Match[str]) -> str:
    raw = match.group(0)
    try:
        value = Decimal(raw)
    except InvalidOperation:
        return raw
    if value == 0:
        return "0"
    return format(value.normalize(), "f")


def _normalise_value(value: str) -> str:
    value = " ".join(value.strip().split())
    return _NUMBER_RE.sub(_normalise_number, value)


@dataclass(frozen=True)
class PMLElement:
    """One ``NEW`` block and its directly assigned attributes."""

    kind: str
    name: str | None
    parent: str
    ordinal: int
    attributes: tuple[tuple[str, str], ...]

    @property
    def label(self) -> str:
        if self.name:
            absolute = self.name if self.name.startswith("/") else f"/{self.name}"
            return f"{self.kind} {absolute}"
        return f"{self.parent} > {self.kind} #{self.ordinal}"

    @property
    def named_key(self) -> tuple[str, str, str] | None:
        if not self.name:
            return None
        return (self.parent, self.kind, self.name.lstrip("/"))

    @property
    def alignment_signature(self) -> tuple[str, ...]:
        # Attribute order is verified after matching.  Sorting here lets an
        # element still match when a native exporter reorders harmless fields.
        return tuple(sorted(f"{key} {value}".rstrip() for key, value in self.attributes))


def parse_pml(text: str) -> list[PMLElement]:
    """Parse PML ``NEW`` blocks without assuming generator-specific comments.

    EQUI and SUBE names establish the stable hierarchy.  Named child elements
    keep their names; unnamed primitives receive an ordinal within their parent
    and type.  This mirrors the files produced by E3D while remaining tolerant
    of comments and formatting changes.
    """

    elements: list[PMLElement] = []
    current_kind: str | None = None
    current_name: str | None = None
    current_parent = "/"
    current_ordinal = 0
    current_attributes: list[tuple[str, str]] = []
    current_equi: str | None = None
    current_sube: str | None = None
    ordinals: dict[tuple[str, str], int] = {}

    def flush() -> None:
        nonlocal current_kind, current_name, current_attributes
        if current_kind is None:
            return
        elements.append(
            PMLElement(
                kind=current_kind,
                name=current_name,
                parent=current_parent,
                ordinal=current_ordinal,
                attributes=tuple(current_attributes),
            )
        )
        current_kind = None
        current_name = None
        current_attributes = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("--") or line.startswith("$*"):
            continue

        new_match = _NEW_RE.match(line)
        if new_match:
            flush()
            kind = new_match.group("kind").upper()
            name = new_match.group("name")
            clean_name = name.lstrip("/") if name else None

            if kind == "EQUI":
                parent = "/"
                current_equi = clean_name
                current_sube = None
            elif kind == "SUBE":
                parent = f"/{current_equi}" if current_equi else "/"
                current_sube = clean_name
            else:
                parts = [part for part in (current_equi, current_sube) if part]
                parent = "/" + "/".join(parts) if parts else "/"

            ordinal_key = (parent, kind)
            ordinal = ordinals.get(ordinal_key, 0) + 1
            ordinals[ordinal_key] = ordinal

            current_kind = kind
            current_name = clean_name
            current_parent = parent
            current_ordinal = ordinal
            current_attributes = []
            continue

        if current_kind is None:
            continue

        pieces = line.split(maxsplit=1)
        key = pieces[0].upper()
        if key in _IGNORED_COMMANDS:
            continue
        value = _normalise_value(pieces[1]) if len(pieces) == 2 else ""
        current_attributes.append((key, value))

    flush()
    return elements


def parse_pml_file(path: Path | str) -> list[PMLElement]:
    return parse_pml(Path(path).read_text(encoding="utf-8-sig"))


def _attribute_map(
    attributes: Iterable[tuple[str, str]],
) -> dict[str, tuple[str, ...]]:
    mapped: dict[str, list[str]] = {}
    for key, value in attributes:
        mapped.setdefault(key, []).append(value)
    return {key: tuple(values) for key, values in mapped.items()}


def _render_values(values: tuple[str, ...] | None) -> str | None:
    if values is None:
        return None
    return " | ".join(value or "<present>" for value in values)


def _element_changes(
    before: PMLElement,
    after: PMLElement,
) -> list[dict[str, str | None]]:
    changes: list[dict[str, str | None]] = []
    before_map = _attribute_map(before.attributes)
    after_map = _attribute_map(after.attributes)
    for key in sorted(before_map.keys() | after_map.keys()):
        if before_map.get(key) != after_map.get(key):
            changes.append(
                {
                    "attribute": key,
                    "before": _render_values(before_map.get(key)),
                    "after": _render_values(after_map.get(key)),
                }
            )

    before_order = tuple(key for key, _ in before.attributes)
    after_order = tuple(key for key, _ in after.attributes)
    if before_order != after_order and before_map == after_map:
        changes.append(
            {
                "attribute": "<ATTRIBUTE_ORDER>",
                "before": " → ".join(before_order),
                "after": " → ".join(after_order),
            }
        )
    return changes


def _similarity(before: PMLElement, after: PMLElement) -> float:
    return SequenceMatcher(
        None,
        before.alignment_signature,
        after.alignment_signature,
        autojunk=False,
    ).ratio()


def _match_unnamed_group(
    before: Sequence[PMLElement],
    after: Sequence[PMLElement],
) -> tuple[
    list[tuple[PMLElement, PMLElement]],
    list[PMLElement],
    list[PMLElement],
]:
    """Align an unnamed primitive group while tolerating inserted elements."""

    matcher = SequenceMatcher(
        None,
        [item.alignment_signature for item in before],
        [item.alignment_signature for item in after],
        autojunk=False,
    )
    pairs: list[tuple[PMLElement, PMLElement]] = []
    removed: list[PMLElement] = []
    added: list[PMLElement] = []

    for operation, i1, i2, j1, j2 in matcher.get_opcodes():
        old = list(before[i1:i2])
        new = list(after[j1:j2])
        if operation == "equal":
            pairs.extend(zip(old, new))
            continue
        if operation == "delete":
            removed.extend(old)
            continue
        if operation == "insert":
            added.extend(new)
            continue

        # A replacement is commonly one manually changed property.  Match the
        # most similar blocks first; leave genuinely new/removed geometry as
        # additions/removals.  The threshold is intentionally conservative.
        candidates = sorted(
            (
                (_similarity(old_item, new_item), old_index, new_index)
                for old_index, old_item in enumerate(old)
                for new_index, new_item in enumerate(new)
            ),
            reverse=True,
        )
        used_old: set[int] = set()
        used_new: set[int] = set()
        for score, old_index, new_index in candidates:
            if score < 0.34:
                break
            if old_index in used_old or new_index in used_new:
                continue
            used_old.add(old_index)
            used_new.add(new_index)
            pairs.append((old[old_index], new[new_index]))
        removed.extend(item for index, item in enumerate(old) if index not in used_old)
        added.extend(item for index, item in enumerate(new) if index not in used_new)

    return pairs, removed, added


def compare_elements(
    baseline: Sequence[PMLElement],
    modified: Sequence[PMLElement],
) -> dict[str, object]:
    """Return an element/attribute-level comparison suitable for JSON output."""

    baseline_named = {
        element.named_key: element for element in baseline if element.named_key
    }
    modified_named = {
        element.named_key: element for element in modified if element.named_key
    }

    added: list[str] = []
    removed: list[str] = []
    changed: list[dict[str, object]] = []

    for key in sorted(baseline_named.keys() - modified_named.keys()):
        removed.append(baseline_named[key].label)
    for key in sorted(modified_named.keys() - baseline_named.keys()):
        added.append(modified_named[key].label)
    for key in sorted(baseline_named.keys() & modified_named.keys()):
        old = baseline_named[key]
        new = modified_named[key]
        differences = _element_changes(old, new)
        if differences:
            changed.append({"element": old.label, "attributes": differences})

    baseline_groups: dict[tuple[str, str], list[PMLElement]] = {}
    modified_groups: dict[tuple[str, str], list[PMLElement]] = {}
    for element in baseline:
        if element.named_key is None:
            baseline_groups.setdefault((element.parent, element.kind), []).append(element)
    for element in modified:
        if element.named_key is None:
            modified_groups.setdefault((element.parent, element.kind), []).append(element)

    for group in sorted(baseline_groups.keys() | modified_groups.keys()):
        pairs, group_removed, group_added = _match_unnamed_group(
            baseline_groups.get(group, []),
            modified_groups.get(group, []),
        )
        removed.extend(element.label for element in group_removed)
        added.extend(element.label for element in group_added)
        for old, new in pairs:
            differences = _element_changes(old, new)
            if differences:
                changed.append(
                    {
                        "element": old.label,
                        "modified_element": new.label,
                        "attributes": differences,
                    }
                )

    added.sort()
    removed.sort()
    changed.sort(key=lambda item: str(item["element"]))
    return {
        "summary": {
            "baseline_elements": len(baseline),
            "modified_elements": len(modified),
            "added": len(added),
            "removed": len(removed),
            "changed": len(changed),
        },
        "added": added,
        "removed": removed,
        "changed": changed,
    }


def compare_files(baseline: Path | str, modified: Path | str) -> dict[str, object]:
    baseline_path = Path(baseline)
    modified_path = Path(modified)
    result = compare_elements(
        parse_pml_file(baseline_path),
        parse_pml_file(modified_path),
    )
    result["baseline"] = str(baseline_path.resolve())
    result["modified"] = str(modified_path.resolve())
    return result


def render_markdown(result: dict[str, object]) -> str:
    summary = result["summary"]
    assert isinstance(summary, dict)
    lines = [
        "# Native E3D PML semantic comparison",
        "",
        f"- Baseline: `{result.get('baseline', '<memory>')}`",
        f"- Modified/native export: `{result.get('modified', '<memory>')}`",
        (
            "- Elements: "
            f"{summary['baseline_elements']} → {summary['modified_elements']}; "
            f"added {summary['added']}, removed {summary['removed']}, "
            f"changed {summary['changed']}"
        ),
    ]

    added = result["added"]
    removed = result["removed"]
    changed = result["changed"]
    assert isinstance(added, list)
    assert isinstance(removed, list)
    assert isinstance(changed, list)

    if added:
        lines.extend(["", "## Added elements", ""])
        lines.extend(f"- `{item}`" for item in added)
    if removed:
        lines.extend(["", "## Removed elements", ""])
        lines.extend(f"- `{item}`" for item in removed)
    if changed:
        lines.extend(["", "## Changed attributes", ""])
        for item in changed:
            assert isinstance(item, dict)
            lines.append(f"### `{item['element']}`")
            lines.append("")
            for change in item["attributes"]:
                assert isinstance(change, dict)
                lines.append(
                    f"- `{change['attribute']}`: "
                    f"`{change['before']}` → `{change['after']}`"
                )
            lines.append("")

    if not added and not removed and not changed:
        lines.extend(["", "No semantic element or attribute differences detected."])
    return "\n".join(lines).rstrip() + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compare an accepted/generated PML baseline with a later native E3D "
            "export at hierarchy, element and attribute level."
        )
    )
    parser.add_argument("baseline", type=Path)
    parser.add_argument("modified", type=Path)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        dest="output_format",
    )
    parser.add_argument(
        "--fail-on-change",
        action="store_true",
        help="return exit code 1 when semantic differences are detected",
    )
    args = parser.parse_args(argv)

    result = compare_files(args.baseline, args.modified)
    if args.output_format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(result), end="")

    summary = result["summary"]
    assert isinstance(summary, dict)
    has_changes = any(summary[key] for key in ("added", "removed", "changed"))
    return 1 if args.fail_on_change and has_changes else 0


if __name__ == "__main__":
    raise SystemExit(main())
