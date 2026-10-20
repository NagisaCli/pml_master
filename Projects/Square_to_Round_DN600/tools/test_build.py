"""Physical fault probes for the delivered geometry and its audit."""
import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location("square_round_build", Path(__file__).with_name("build.py"))
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


def render(node):
    lines = ["NEW " + node.kind + (" " + node.name if node.name else "")]
    lines.extend(key + " " + value for key, value in node.attributes)
    lines.extend(render(child) for child in node.children)
    return "\n".join(lines + ["END"])


@pytest.fixture(scope="module")
def candidate():
    return build.build()


def test_real_candidate_has_open_passage_and_exact_envelope(candidate):
    audit = build.verify(candidate)
    assert audit["overall_bounds_mm"] == [[-410,-410,0],[410,410,500]]
    assert audit["flange_bolt_holes"] == 12
    assert all(s["covered_rays"] == s["rays"] for s in audit["section_ray_checks"])


@pytest.mark.parametrize("fault", ["equipment_drift", "flange_off_joint", "unapplied_hole",
                                  "undersized_pipe_bore", "missing_fan_sector", "detached_taper", "thin_taper"])
def test_audit_rejects_physical_faults_with_unchanged_inventory(candidate, fault):
    root = build.parse_native_tree(candidate)[0]
    flange, transition, outlet = root.children
    if fault == "equipment_drift":
        root.set("POS", "E 0 N 1 U 0")
    elif fault == "flange_off_joint":
        flange.children[0].set("POS", "E -385 N 0 U 489")
    elif fault == "unapplied_hole":
        flange.children[0].children[0].set("NAPPFLAG", "0")
    elif fault == "undersized_pipe_bore":
        outlet.children[0].children[0].set("DIAM", "580")
    elif fault == "missing_fan_sector":
        # Keep the same element count while leaving one conical sector absent.
        transition.children[5] = transition.children[6]
    elif fault == "detached_taper":
        for panel in transition.children:
            if panel.kind == "EXTRUSION":
                point = build.xyz(panel.get("POS"))
                point[2] += 25
                panel.set("POS", build.pos(point))
    elif fault == "thin_taper":
        for panel in transition.children:
            if panel.kind == "EXTRUSION":
                panel.set("HEIG", "2")
    with pytest.raises((AssertionError, ValueError)):
        build.verify(render(root))
