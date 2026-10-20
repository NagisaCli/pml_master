"""Add a second-floor HANDRA perimeter to the immutable DD4060 native export.

This is an offline layout calculation. Catalogue member envelopes and handrail
clearance allowances are explicit Reference Values, not native clash results.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PlotPolygon
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from wsb.handrail_builder import HandrailBuilder, HandrailSpec, RoutePoint
from wsb.pml_builder import validate_pml
from wsb.pml_parser import native_orientation_basis, parse_native_tree

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "imports/2026-10-19_building.txt"
OUTPUT = PROJECT / "output"
PREFIX = "DD4060_BUILDING_F2_GUARDRAILS_R1"
SOURCE_HASH = "c87af66310ac7b74281ad7339f17256ee4b79985c1bbd52a8448b761fe436dc0"

# Reference Values: layout allowances, pending receiving-host visual review.
EDGE_INSET = 150.0
SECTION_RADIUS = 125.0  # Encloses the three source section families in plan.
RAIL_RADIUS = 40.0     # Assumed envelope; native post/base geometry is pending.
CLEARANCE = 100.0
FILLET = 50.0          # Extra allowance covers up to this path fillet deviation.
MIN_RETURN_GAP = 300.0 # Reference Value: merge short returns between edge bays.
IDENTITY = ((1., 0., 0.), (0., 1., 0.), (0., 0., 1.))


def position(text):
    result = [0., 0., 0.]
    if not text:
        return tuple(result)
    matches = re.findall(r"([EWNSUD])\s+(-?[\d.]+)\s*mm", text, re.I)
    if len(matches) != 3:
        raise ValueError(f"Unsupported native position: {text}")
    for direction, value in matches:
        direction = direction.upper()
        axis = {"E": 0, "W": 0, "N": 1, "S": 1, "U": 2, "D": 2}[direction]
        result[axis] = float(value) * (-1 if direction in "WSD" else 1)
    return tuple(result)


def transform(matrix, vector):
    return tuple(sum(matrix[j][i] * vector[j] for j in range(3)) for i in range(3))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def index_frames(roots):
    frames = {}

    def visit(node, parent_origin, parent_basis):
        origin = add(parent_origin, transform(parent_basis, position(node.get("POS"))))
        axes = native_orientation_basis(node.get("ORI"))
        basis = tuple(transform(parent_basis, axes[key]) for key in "XYZ")
        frames[id(node)] = (origin, basis)
        for child in node.children:
            visit(child, origin, basis)

    for root in roots:
        visit(root, (0., 0., 0.), IDENTITY)
    return frames


def clip_height(a, b, bottom, top):
    if abs(b[2] - a[2]) < 1e-9:
        return (a, b) if bottom <= a[2] <= top else None
    ts = sorted(((bottom - a[2]) / (b[2] - a[2]),
                 (top - a[2]) / (b[2] - a[2])))
    lo, hi = max(0., ts[0]), min(1., ts[1])
    if lo > hi:
        return None
    return tuple(tuple(a[i] + t * (b[i] - a[i]) for i in range(3)) for t in (lo, hi))


def fmt(value):
    return f"{value:.2f}".rstrip("0").rstrip(".") or "0"


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
    text = SOURCE.read_text(encoding="utf-8-sig")
    creation = text[text.index("NEW EQUIPMENT"):text.index("\nOLD ")]
    roots = parse_native_tree(creation)
    assert [node.name for node in roots] == ["/New_washer_biulding", "/DD4060-ACCESS-R6"]
    frames = index_frames(roots)
    building, access = roots
    building_origin, building_basis = frames[id(building)]
    assert building_basis == IDENTITY
    assert len([x for x in building.walk() if x.kind == "EXTRUSION"]) == 46
    slab = [x for x in building.walk() if x.kind == "EXTRUSION"
            and x.get("HEIG") == "150mm"]
    assert len(slab) == 1
    slab = slab[0]
    slab_vertices = [frames[id(v)][0] for loop in slab.children for v in loop.children
                     if v.kind == "VERTEX"]
    # The 0.02 mm native listing round-off is below layout precision; round only
    # the new routing outline to 0.1 mm. The source model bytes remain unchanged.
    floor = Polygon([(round(p[0] - building_origin[0], 1),
                      round(p[1] - building_origin[1], 1)) for p in slab_vertices])
    assert floor.is_valid and floor.area > 170_000_000
    floor_top = slab_vertices[0][2] + float(slab.get("HEIG")[:-2])
    assert abs(floor_top - 9700.) < 1e-6
    rail_attributes = [x for x in access.walk() if x.kind == "HANDRA"]
    assert rail_attributes and {x.get("RAILHE") for x in rail_attributes} == {"1100mm 550mm"}
    assert {x.get("POSTSP") for x in rail_attributes} == {"1200mm"}
    top_height, mid_height, spacing = 1100., 550., 1200.
    rail_top = floor_top + top_height
    obstacles = []

    def add_obstacle(name, category, points, margin=0.):
        xs = [p[0] - building_origin[0] for p in points]
        ys = [p[1] - building_origin[1] for p in points]
        shape = box(min(xs) - margin, min(ys) - margin,
                    max(xs) + margin, max(ys) + margin)
        if shape.area <= 0:
            raise ValueError(f"Empty obstacle: {name}")
        if shape.intersects(floor):
            obstacles.append({"name": name, "category": category, "shape": shape})

    for number, node in enumerate(building.walk()):
        if node.kind != "EXTRUSION":
            continue
        points = [frames[id(v)][0] for loop in node.children for v in loop.children
                  if v.kind == "VERTEX"]
        height = float(node.get("HEIG")[:-2])
        # Upright concrete columns only; members ending at slab top do not
        # obstruct an above-floor railing. Slabs/beams below the floor are kept.
        if min(p[2] for p in points) < rail_top and max(p[2] for p in points) + height > floor_top + .1:
            assert not node.get("ORI")
            add_obstacle(f"building/extrusion-{number}", "Concrete column", points)

    section_refs = set()
    for node in access.walk():
        if node.kind == "GENSEC":
            points = [frames[id(v)][0] for spine in node.children if spine.kind == "SPINE"
                      for v in spine.children if v.kind == "POINSP"]
            assert len(points) == 2, node.name
            section_refs.add(node.get("SPRE"))
            clipped = clip_height(*points, floor_top - SECTION_RADIUS, rail_top + SECTION_RADIUS)
            if clipped:
                add_obstacle(node.name, "Access member envelope", clipped, SECTION_RADIUS)
        elif node.kind == "PANEL":
            loops = [x for x in node.children if x.kind == "PLOOP"]
            assert len(loops) == 1
            thickness = float(loops[0].get("HEIG")[:-2])
            points = [frames[id(v)][0] for v in loops[0].children if v.kind == "PAVERT"]
            assert len(points) >= 3
            horizontal = max(p[2] for p in points) - min(p[2] for p in points) < .1
            if horizontal and loops[0].get("SJUS") == "DTOP":
                # Source anchorage is explicit: embedded plate TOP is 9700;
                # anchor bars start at its underside (9688) and run downwards.
                # Below-slab anchor bars must not create false above-floor bays.
                low, high = min(p[2] for p in points) - thickness, max(p[2] for p in points)
                plan_margin = 0.
            else:
                low, high = min(p[2] for p in points) - thickness, max(p[2] for p in points) + thickness
                plan_margin = thickness
            if high >= floor_top - .1 and low <= rail_top:
                add_obstacle(node.name, "Plate envelope", points, plan_margin)
    assert section_refs == {"SPCOMPONENT /DIN-SPEC/HE160A", "SPCOMPONENT /DIN-SPEC/IPE120",
                            "SPCOMPONENT /DIN-SPEC/IPE200"}
    assert len(obstacles) >= 60
    exclusion_margin = CLEARANCE + RAIL_RADIUS + FILLET
    obstacle_union = unary_union([item["shape"] for item in obstacles])
    exclusions = unary_union([item["shape"].buffer(exclusion_margin, join_style=2)
                              for item in obstacles])
    # Adjacent feet, plates and braces in one connected exclusion get one
    # rectangular bay. This removes 18-80 mm jogs that cannot carry sensible
    # bent handrail corners; isolated supports retain their own bay.
    pieces = list(exclusions.geoms) if exclusions.geom_type == "MultiPolygon" else [exclusions]
    while True:
        merged = unary_union([box(*piece.bounds) for piece in pieces])
        updated = list(merged.geoms) if merged.geom_type == "MultiPolygon" else [merged]
        if len(updated) == len(pieces) and all(piece.equals(box(*piece.bounds)) for piece in updated):
            pieces = updated
            exclusions = merged
            break
        pieces = updated
    nominal_edge = floor.buffer(-EDGE_INSET, join_style=2).boundary
    # Join short returns only between bays already crossing the nominal edge.
    # An isolated interior stair foot must not become fenced off merely because
    # it lies close to a concrete column at a building corner.
    while True:
        pair = None
        for i, a in enumerate(pieces):
            if a.distance(nominal_edge) > .1:
                continue
            for j in range(i + 1, len(pieces)):
                b = pieces[j]
                if b.distance(nominal_edge) > .1:
                    continue
                ax0, ay0, ax1, ay1 = a.bounds
                bx0, by0, bx1, by1 = b.bounds
                x_overlap = min(ax1, bx1) - max(ax0, bx0)
                y_overlap = min(ay1, by1) - max(ay0, by0)
                x_gap = max(ax0 - bx1, bx0 - ax1, 0.)
                y_gap = max(ay0 - by1, by0 - ay1, 0.)
                if ((x_overlap >= 0 and y_gap < MIN_RETURN_GAP)
                        or (y_overlap >= 0 and x_gap < MIN_RETURN_GAP)):
                    pair = (i, j)
                    break
            if pair:
                break
        if pair is None:
            exclusions = unary_union(pieces)
            break
        i, j = pair
        merged_box = box(*unary_union([pieces[i], pieces[j]]).bounds)
        pieces = [p for k, p in enumerate(pieces) if k not in pair] + [merged_box]
    usable = floor.buffer(-EDGE_INSET, join_style=2).difference(exclusions)
    discarded_slivers = []
    if usable.geom_type == "MultiPolygon":
        pieces = sorted(usable.geoms, key=lambda piece: piece.area, reverse=True)
        discarded_slivers = [{"area_mm2": p.area, "bounds_mm": list(p.bounds)} for p in pieces[1:]]
        print("Peripheral remnants:", discarded_slivers)
        assert sum(p.area for p in pieces[1:]) < .02 * floor.area
        usable = pieces[0]
    assert usable.geom_type == "Polygon"
    # Internal holes are support locations inside the floor; only the exterior
    # perimeter needs a guardrail. No railing is placed around interior columns.
    # Simplification removes collinear vertices, never large structural details.
    outline = Polygon(usable.exterior).simplify(.05, preserve_topology=True)
    route = [(round(x, 2), round(y, 2), 0.) for x, y in outline.exterior.coords]
    assert len(route) > 20 and route[0] == route[-1]
    path = LineString([p[:2] for p in route])
    assert path.is_simple and path.is_ring
    assert path.distance(obstacle_union) >= exclusion_margin - .1
    assert floor.buffer(.1).covers(path.buffer(RAIL_RADIUS + FILLET, join_style=2))
    segment_lengths = [LineString([a[:2], b[:2]]).length for a, b in zip(route, route[1:])]
    if min(segment_lengths) < 100.:
        print("Short segments:", [(a, b, length) for a, b, length in zip(route, route[1:], segment_lengths) if length < 100.])
    assert min(segment_lengths) >= 100.
    floor_stair_entries = []
    for node in access.walk():
        if node.kind == "STRFLT":
            origin = frames[id(node)][0]
            if abs(origin[2] - floor_top) < .1:
                point = Point(origin[0] - building_origin[0], origin[1] - building_origin[1])
                width = float(node.get("TWIDTH")[:-2])
                assert Polygon(path).contains(point), node.name
                assert point.distance(path) >= width / 2 + CLEARANCE, node.name
                floor_stair_entries.append({"name": node.name, "xy_mm": list(point.coords[0]),
                                            "entry_to_rail_distance_mm": point.distance(path),
                                            "width_mm": width})
    assert len(floor_stair_entries) == 2

    spec = HandrailSpec(
        name=f"{PREFIX}/PERIMETER", position=(0., 0., 0.),
        top_rail_height=top_height, mid_rail_height=mid_height,
        post_spacing=spacing, tangent_offset=0., bend_radius=FILLET,
        show_kickplate=True,
        path_items=tuple(RoutePoint(p, FILLET) for p in route),
    )
    handrail = HandrailBuilder().build(spec)
    macro = "\n".join([
        "-- DD4060 building second-floor perimeter guardrail, additive candidate R1.",
        "-- Select the SAME writable ZONE that owns /New_washer_biulding before loading.",
        "-- Positions use that exported owner frame; no world-origin assumption is needed.",
        "-- Existing building/access elements are neither selected nor modified.",
        "-- Top/mid rails 1100/550 and post spacing 1200 are copied from source HANDRA.",
        "-- Reference Values: edge inset 150; member envelope radius 125; rail radius 40;",
        "-- clearance 100; corner fillet 50 mm. Includes 50 mm extra fillet clearance.",
        "-- Reference Value: merge edge-bay return gaps below 300 mm; interior stair feet retained.",
        "-- Native catalogue solids, post bases and load capacity require receiving-host review.",
        f"NEW STRU /{PREFIX}",
        "DESC 'Building second-floor guardrail; bypass access supports; offline layout R1'",
        "ORI Y IS N AND Z IS U",
        f"POS E {fmt(building_origin[0])}mm N {fmt(building_origin[1])}mm U {fmt(floor_top)}mm",
        "BUIL false",
        f"NEW FRMWORK /{PREFIX}/RAILS", "BUIL false", "SHOP false", "",
        handrail, "END", "END", "",
    ])
    assert not validate_pml(macro), validate_pml(macro)
    assert not re.search(r"^(?:OLD|DELETE|SAVEWORK|SAVE WORK|INPUT|SUSPEND|RESUME)\b", macro, re.M | re.I)

    # Parse emitted NEW/END hierarchy, independently recover route elevations
    # and positions, and check the actual emitted file before delivery.
    emitted = parse_native_tree(macro)
    emitted_frames = index_frames(emitted)
    points = [emitted_frames[id(x)][0] for x in emitted[0].walk() if x.kind == "POINTR"]
    recovered = LineString([(p[0] - building_origin[0], p[1] - building_origin[1]) for p in points])
    assert len(points) == len(route) and all(abs(p[2] - floor_top) < .001 for p in points)
    assert recovered.is_ring and recovered.is_simple
    assert recovered.hausdorff_distance(path) < .001
    assert recovered.distance(obstacle_union) - RAIL_RADIUS - FILLET >= CLEARANCE - .1
    new_names = {x.name for x in emitted[0].walk() if x.name}
    source_names = {x.name for root in roots for x in root.walk() if x.name}
    assert new_names.isdisjoint(source_names)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
    OUTPUT.mkdir(exist_ok=True)
    macro_path = OUTPUT / f"{PREFIX}.txt"
    macro_path.write_bytes(macro.replace("\n", "\r\n").encode("ascii"))
    (OUTPUT / f"{PREFIX}.pml").write_bytes(macro_path.read_bytes())

    affected = [item for item in obstacles if item["shape"].buffer(exclusion_margin + .1, join_style=2).intersects(path)]
    audit = {
        "status": "OFFLINE_LAYOUT_PASS_NATIVE_ACCEPTANCE_PENDING",
        "source_sha256": SOURCE_HASH,
        "source_counts": dict(Counter(x.kind for root in roots for x in root.walk())),
        "preservation": "All received bytes and all existing hierarchy/attributes remain unchanged; additive macro only.",
        "coordinate_frame": "Same ZONE owner frame as the received building; absolute world frame is not asserted.",
        "building_origin_mm": building_origin,
        "access_origin_mm": frames[id(access)][0],
        "access_axes": frames[id(access)][1],
        "slab_top_mm": floor_top,
        "rail_top_mm": rail_top,
        "rail_mid_mm": floor_top + mid_height,
        "post_spacing_mm": spacing,
        "route_length_mm": recovered.length,
        "route_vertices_including_closure": len(points),
        "minimum_segment_mm": min(LineString([a[:2], b[:2]]).length for a, b in zip(route, route[1:])),
        "minimum_route_to_obstacle_envelope_mm": recovered.distance(obstacle_union),
        "minimum_rail_clearance_after_fillet_allowance_mm": recovered.distance(obstacle_union) - RAIL_RADIUS - FILLET,
        "minimum_route_to_slab_edge_mm": recovered.distance(floor.boundary),
        "obstacles_checked": len(obstacles),
        "peripheral_domain_remnants": discarded_slivers,
        "floor_stair_entries": floor_stair_entries,
        "reference_values_mm": {"edge_inset": EDGE_INSET, "section_radius": SECTION_RADIUS,
                                "rail_radius": RAIL_RADIUS, "clearance": CLEARANCE, "fillet": FILLET,
                                "minimum_edge_bay_return_gap": MIN_RETURN_GAP},
        "route_building_xy_mm": [list(p[:2]) for p in route],
        "bypassed_obstacles": [{"name": x["name"], "category": x["category"],
                                "bounds_mm": list(x["shape"].bounds)} for x in affected],
        "all_obstacles": [{"name": x["name"], "category": x["category"],
                           "bounds_mm": list(x["shape"].bounds)} for x in obstacles],
        "open_acceptance": ["Native E3D macro loading and generated catalogue geometry",
                            "Visual review of support bypasses, corner posts and toe plates",
                            "Receiving-host clash check, post/base anchorage and civil design",
                            "Save Work and reopen persistence"],
    }
    (OUTPUT / "layout_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    plot_plan(floor, path, obstacles, affected, route)
    print(json.dumps({key: audit[key] for key in ["status", "slab_top_mm", "route_length_mm",
                     "route_vertices_including_closure", "minimum_segment_mm",
                     "minimum_rail_clearance_after_fillet_allowance_mm", "obstacles_checked"]}, indent=2))
    print("Bypassed:", ", ".join(x["name"].split("/")[-1] for x in affected))


def plot_plan(floor, path, obstacles, affected, route):
    fig, ax = plt.subplots(figsize=(10, 12), layout="constrained")
    ax.add_patch(PlotPolygon([(x / 1000, y / 1000) for x, y in floor.exterior.coords],
                            facecolor="#f3f5f8", edgecolor="#485467", linewidth=1.5, label="Received floor slab"))
    seen = set()
    for item in obstacles:
        category = item["category"]
        color = "#6b7280" if category == "Concrete column" else "#e29742"
        xy = [(x / 1000, y / 1000) for x, y in item["shape"].exterior.coords]
        ax.add_patch(PlotPolygon(xy, facecolor=color, edgecolor=color, alpha=.6,
                                label=category if category not in seen else None))
        seen.add(category)
    x, y = path.xy
    ax.plot([v / 1000 for v in x], [v / 1000 for v in y], color="#1473dc", linewidth=2.5,
            label="New continuous HANDRA route")
    ax.scatter([p[0] / 1000 for p in route], [p[1] / 1000 for p in route], color="#1473dc", s=9)
    ax.annotate("West supports + brace\ncontinuous inward bypass", xy=(.73, 6.), xytext=(1.7, 6.),
                arrowprops={"arrowstyle": "->", "color": "#334155"}, fontsize=9)
    ax.annotate("East landing supports\ncontinuous inward bypass", xy=(10.4, 8.3), xytext=(7.1, 8.6),
                arrowprops={"arrowstyle": "->", "color": "#334155"}, fontsize=9)
    ax.text(1.2, 12.8, "Existing access structure retained\nInterior supports need no extra rail loop",
            fontsize=10, color="#475569", bbox={"boxstyle": "round,pad=.5", "fc": "white", "ec": "#d8dee8"})
    ax.set(title="DD4060 | Second-floor guardrail addition R1\nSlab top U 9700 mm | Top/mid rails 1100/550 mm\nOffline layout; E3D visual review pending",
           xlabel="East from building origin (m)", ylabel="North from building origin (m)")
    ax.set_aspect("equal")
    ax.set_xlim(-.6, 11.7)
    ax.set_ylim(-.6, 18.3)
    ax.grid(alpha=.16)
    ax.legend(loc="upper right", fontsize=8)
    fig.savefig(OUTPUT / "guardrail_plan.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
