"""Render representative r12 top-nozzle width-branch QA diagrams."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_pumps import OUTPUT_DIR, build_pump                    # noqa: E402
from extract_project_data import load_all                         # noqa: E402
from verify_pumps import bounds                                   # noqa: E402

OUT = OUTPUT_DIR / "top_nozzle_width_branch_QA.png"
TAGS = ("203-PU-008", "203-PU-011", "205-PU-054")
PREFIX = "top discharge casing connection"


def _along(model, east: float, north: float) -> float:
    casing_e, casing_n = model.facts["casing_centre"]
    if model.facts["long_axis"] == "N":
        return north - casing_n
    return east - casing_e


def _draw(model, ax) -> None:
    casing_dia, casing_width = model.facts["casing"]
    shaft_u = model.facts["shaft_u"]
    crown = shaft_u + casing_dia / 2.0
    nozzle = next(item for item in model.primitives
                  if item.kind == "NOZZLE" and item.ori.endswith(" U"))
    nozzle_x = _along(model, nozzle.east, nozzle.north)
    connector = sorted((item for item in model.primitives
                        if item.note.startswith(PREFIX)),
                       key=lambda item: bounds(item)[2][0])
    bridge = next((item for item in model.primitives
                   if item.note.startswith("top discharge casing offset bridge")), None)

    ax.add_patch(Rectangle(
        (-casing_width / 2.0, shaft_u - casing_dia / 2.0),
        casing_width, casing_dia,
        facecolor="#fca5a5", edgecolor="#991b1b", linewidth=1.4,
        label="existing casing"))

    if bridge is not None:
        bridge_box = bounds(bridge)
        x_low = ((bridge_box[1][0] - model.facts["casing_centre"][1])
                 if model.facts["long_axis"] == "N" else
                 (bridge_box[0][0] - model.facts["casing_centre"][0]))
        x_high = ((bridge_box[1][1] - model.facts["casing_centre"][1])
                  if model.facts["long_axis"] == "N" else
                  (bridge_box[0][1] - model.facts["casing_centre"][0]))
        ax.add_patch(Rectangle(
            (x_low, bridge_box[2][0]), x_high - x_low,
            bridge_box[2][1] - bridge_box[2][0],
            facecolor="#fdba74", edgecolor="#c2410c", linewidth=1.2,
            label="solid casing bridge"))

    for item in connector:
        span = bounds(item)[2]
        if item.kind == "CONE":
            lower = item.attrs["DBOT"] / 2.0
            upper = item.attrs["DTOP"] / 2.0
            shape = [(nozzle_x - lower, span[0]),
                     (nozzle_x + lower, span[0]),
                     (nozzle_x + upper, span[1]),
                     (nozzle_x - upper, span[1])]
            ax.add_patch(Polygon(shape, closed=True, facecolor="#fbbf24",
                                 edgecolor="#92400e", linewidth=1.2,
                                 label="CONE transition"))
        else:
            radius = item.attrs["DIAM"] / 2.0
            ax.add_patch(Rectangle(
                (nozzle_x - radius, span[0]), item.attrs["DIAM"],
                span[1] - span[0], facecolor="#fde68a",
                edgecolor="#92400e", linewidth=1.2,
                label="lower CYLINDER socket"))

    record = model.facts["top_nozzle_connections"][0]
    dn = record["nozzle_diameter"]
    root_u = nozzle.up - nozzle.attrs["HEIG"]
    ax.add_patch(Rectangle(
        (nozzle_x - dn / 2.0, root_u), dn, nozzle.attrs["HEIG"],
        fill=False, edgecolor="#1d4ed8", linewidth=1.5, linestyle="--",
        label="native NOZZLE, HEIG adapted"))
    root_label = ("reducer top = nozzle bottom"
                  if record["overwidth"] else
                  "native nozzle root inside casing")
    ax.plot([nozzle_x - dn / 2.0, nozzle_x + dn / 2.0],
            [root_u, root_u], color="#15803d", linewidth=3,
            label=root_label)
    ax.plot([nozzle_x - dn * 0.65, nozzle_x + dn * 0.65],
            [nozzle.up, nozzle.up], color="#1d4ed8", linewidth=4)
    ax.axhline(crown, color="#7f1d1d", linewidth=0.8, linestyle=":")

    kind = ("overwidth socket + CONE"
            if record["overwidth"] else "direct native-nozzle penetration")
    if record.get("offset_bridge"):
        kind += " + offset solid bridge"
    ax.set_title(
        f"{model.tag}: {kind}\nDN {dn:.0f}, casing width {casing_width:.0f} mm",
        fontsize=10)
    ax.text(nozzle_x, nozzle.up + 12, f"fixed face U {nozzle.up:.1f}",
            ha="center", va="bottom", fontsize=8, color="#1d4ed8")
    detail = (f"nozzle bottom = CONE top U {root_u:.1f}"
              if record["overwidth"] else
              f"native root U {root_u:.1f}; "
              f"external {record['external_ratio']:.1%}")
    ax.text(nozzle_x, root_u + 6, detail,
            ha="center", va="bottom", fontsize=7.5, color="#15803d")
    ax.text(casing_width / 2 + 8, crown - 3, "casing crown", fontsize=8,
            ha="left", va="top", color="#7f1d1d")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, alpha=0.18)
    ax.set_xlabel("casing longitudinal axis (mm)")


def main() -> int:
    sources = load_all()
    models = [build_pump(tag, sources) for tag in TAGS]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6), constrained_layout=True)
    for model, ax in zip(models, axes):
        _draw(model, ax)
    axes[0].set_ylabel("world U (mm)")
    handles, labels = axes[-1].get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    fig.legend(unique.values(), unique.keys(), loc="lower center", ncol=4,
               fontsize=8, frameon=False)
    fig.suptitle(
        "JK_Pump_Build r12 — width-dependent top-nozzle construction\n"
        "Overwidth: socket + CONE + native NOZZLE; otherwise direct with "
        "at least 70% outside",
        fontsize=13)
    fig.savefig(OUT, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
