"""Render representative r9 motor/drive side-elevation QA diagrams."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_pumps import OUTPUT_DIR, build_pump                    # noqa: E402
from extract_project_data import load_all                         # noqa: E402

OUT = OUTPUT_DIR / "motor_drive_side_elevation_QA.png"
TAGS = ("203-PU-008", "205-PU-018", "205-PU-012")


def _part(ax, start, end, lower_start, upper_start, lower_end, upper_end,
          color, label):
    ax.add_patch(Polygon(
        [(start, lower_start), (start, upper_start),
         (end, upper_end), (end, lower_end)],
        closed=True, facecolor=color, edgecolor="#292524", linewidth=0.8))
    ax.text((start + end) / 2, max(upper_start, upper_end) + 16, label,
            ha="center", va="bottom", fontsize=6.5, rotation=0)


def _diameters(segment):
    if segment["kind"] == "CONE":
        return segment["DBOT"], segment["DTOP"]
    return segment["DIAM"], segment["DIAM"]


def render_tag(ax, model):
    shaft_u = model.facts["shaft_u"]
    plate_top = model.facts["plate_top"]
    base_y = plate_top - shaft_u

    motor_colors = {"CONE": "#f59e0b", "CYLINDER": "#fcd34d"}
    for segment in model.facts["motor_segments"]:
        first, second = _diameters(segment)
        _part(ax, segment["start"], segment["end"], -first / 2, first / 2,
              -second / 2, second / 2, motor_colors[segment["kind"]],
              segment["role"].replace(" ", "\n"))

    for segment in model.facts.get("drive_segments", []):
        first = segment["diameter_1"]
        second = segment["diameter_2"] or first
        _part(ax, segment["start"], segment["end"], -first / 2, first / 2,
              -second / 2, second / 2, "#60a5fa",
              segment["role"].replace(" ", "\n"))

    wet = {"N": (0.0, 1.0), "S": (0.0, -1.0),
           "E": (1.0, 0.0), "W": (-1.0, 0.0)}[model.facts["wet_end"]]
    casing_e, casing_n = model.facts["casing_centre"]
    plate_e, plate_n = model.facts["plate_centre"]
    casing_centre = ((casing_e - plate_e) * wet[0]
                     + (casing_n - plate_n) * wet[1])
    casing_dia, casing_len = model.facts["casing"]
    ax.add_patch(Rectangle((casing_centre - casing_len / 2, -casing_dia / 2),
                           casing_len, casing_dia, facecolor="#fb7185",
                           edgecolor="#292524", linewidth=0.9))
    ax.text(casing_centre, casing_dia / 2 + 16, "casing", ha="center",
            va="bottom", fontsize=7)

    lantern = [item for item in model.primitives if item.sube == "BEARING"]
    if lantern:
        item = lantern[0]
        centre = ((item.east - plate_e) * wet[0]
                  + (item.north - plate_n) * wet[1])
        diameter = item.attrs["DIAM"]
        length = item.attrs["HEIG"]
        ax.add_patch(Rectangle((centre - length / 2, -diameter / 2),
                               length, diameter, facecolor="#60a5fa",
                               edgecolor="#292524", linewidth=0.8))
        ax.text(centre, diameter / 2 + 16, "close-coupled\nlantern",
                ha="center", va="bottom", fontsize=6.5)

    half_long = max(model.facts["plate"][0], model.facts["plate"][1]) / 2
    ax.add_patch(Rectangle((-half_long, base_y - model.facts["plate"][2]),
                           2 * half_long, model.facts["plate"][2],
                           facecolor="#d6d3d1", edgecolor="#57534e",
                           linewidth=0.7))
    ax.axhline(0, color="#334155", linewidth=0.7, linestyle="--")
    ax.text(-half_long, 10, "shaft axis", ha="left", va="bottom",
            color="#334155", fontsize=6.5)

    source = model.facts["engine_source"]
    fit = ("close-coupled / no free shaft" if model.facts["is_mc"] else
           f"shaft axial fit {model.facts['shaft_fit_scale']:.4f}")
    ax.set_title(f"{model.tag} — {source}\n{fit}", fontsize=9, loc="left")
    ax.set_aspect("equal", adjustable="datalim")
    ax.autoscale_view()
    ax.margins(x=0.04, y=0.18)
    ax.set_ylabel("U relative to shaft axis (mm)", fontsize=7)
    ax.tick_params(labelsize=6)
    ax.grid(axis="y", color="#e7e5e4", linewidth=0.5)


def main() -> int:
    sources = load_all()
    fig, axes = plt.subplots(len(TAGS), 1, figsize=(14, 10), constrained_layout=True)
    fig.suptitle("JK_Pump_Build r9 — cone-terminated motor and drive-shaft QA",
                 fontsize=14)
    for ax, tag in zip(axes, TAGS):
        render_tag(ax, build_pump(tag, sources))
    axes[-1].set_xlabel("longitudinal axis: motor/outboard → pump/wet end (mm)",
                        fontsize=8)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=180, facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
