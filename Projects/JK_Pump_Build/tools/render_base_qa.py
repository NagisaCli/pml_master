"""Render orthographic QA views of representative adapted pump bases."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_pumps import OUTPUT_DIR, build_pump             # noqa: E402
from extract_project_data import load_all                  # noqa: E402
from verify_pumps import bounds                            # noqa: E402

TAGS = ("203-PU-008", "204-PU-006", "203-PU-026", "205-PU-018")
COLORS = {"skid": "#8b95a1", "pump": "#d97b29", "motor": "#3979b8",
          "CASING": "#b94a48", "DRIVER": "#579d62"}


def _frame(model):
    wet = model.facts["wet_end"]
    along = {"N": (0.0, 1.0), "S": (0.0, -1.0),
             "E": (1.0, 0.0), "W": (-1.0, 0.0)}[wet]
    return (along[1], -along[0]), along


def _project(box, centre, vector):
    values = []
    for east in box[0]:
        for north in box[1]:
            values.append((east - centre[0]) * vector[0]
                          + (north - centre[1]) * vector[1])
    return min(values), max(values)


def _draw(ax, model, plan_axis, title):
    centre = model.facts["plate_centre"]
    base = [p for p in model.primitives if p.sube == "BASE"]
    machine = [p for p in model.primitives
               if p.sube in ("CASING", "DRIVER")
               and p.kind in ("BOX", "CYLINDER", "DISH")]
    for primitive in base + machine:
        box = bounds(primitive)
        low, high = _project(box, centre, plan_axis)
        bottom, top = box[2]
        if primitive.sube == "BASE":
            station = primitive.note.rsplit("(", 1)[-1].split(" station", 1)[0]
            color = COLORS[station]
            alpha = 0.65
        else:
            color = COLORS[primitive.sube]
            alpha = 0.22
        ax.add_patch(Rectangle((low, bottom), high - low, top - bottom,
                               facecolor=color, edgecolor="#26313b",
                               linewidth=0.35, alpha=alpha))
    ax.axhline(model.facts["plate_under"], color="#222", linewidth=0.7)
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("mm")
    ax.set_ylabel("U mm")
    ax.grid(True, linewidth=0.25, alpha=0.35)
    ax.autoscale_view()
    ax.set_aspect("equal", adjustable="datalim")


def main() -> int:
    sources = load_all()
    figure, axes = plt.subplots(len(TAGS), 2, figsize=(15, 14), dpi=150)
    for row, tag in enumerate(TAGS):
        model = build_pump(tag, sources)
        across, along = _frame(model)
        _draw(axes[row][0], model, along,
              f"{tag} ({model.facts['wet_end']}) - longitudinal elevation")
        _draw(axes[row][1], model, across,
              f"{tag} ({model.facts['wet_end']}) - transverse elevation")
    figure.suptitle("/P1501B-BASE r6 adaptation QA\n"
                    "grey=skid, orange=pump support, blue=motor support, "
                    "red/green=machine envelopes",
                    fontsize=12)
    figure.tight_layout(rect=(0, 0, 1, 0.965))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "BASE_ADAPTATION_QA.png"
    figure.savefig(path, bbox_inches="tight")
    plt.close(figure)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
