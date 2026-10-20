"""Generate and audit the standalone square-to-round fitting.

The shared PML builder emits all positive geometry. The shared native-tree
parser reads the delivered file back, retaining local subtractive children.
No live host or other project's geometry/catalogue is used.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re
import sys

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
sys.path.insert(0, str(ROOT))
from wsb.pml_builder import PMLBuilder, validate_pml
from wsb.pml_parser import parse_native_tree

OUT = PROJECT / "output"
TAG = "SQROUND_DN600_H500"
NAME = "Square_to_Round_DN600"
FLANGE = 820.0
OPENING = 720.0
WALL = 6.0
OD = 610.0
ID = OD - 2 * WALL
FACETS = 24
SEAM = 0.30
SOURCE = "https://www.united-steel.com/m/newsshow/1102.html"
PIPE_SOURCE = "https://www.united-steel.com/productshow/lsaw-steel-pipe.html"


def fmt(value):
    return f"{0 if abs(value) < 1e-9 else value:.8f}".rstrip("0").rstrip(".")


def pos(point):
    return "E {} N {} U {}".format(*(fmt(x) for x in point))


def xyz(text):
    match = re.fullmatch(r"E ([-\d.]+)(?:mm)? N ([-\d.]+)(?:mm)? U ([-\d.]+)(?:mm)?", text)
    if not match:
        raise ValueError(f"Unsupported position: {text}")
    return np.array([float(x) for x in match.groups()])


def direction(vector):
    """PML plan bearing followed by elevation; decoded independently below."""
    x, y, z = np.asarray(vector) / np.linalg.norm(vector)
    horizontal = math.hypot(x, y)
    if horizontal < 1e-10:
        return "U" if z > 0 else "D"
    azimuth = math.degrees(math.atan2(abs(y), abs(x)))
    if azimuth < 1e-8:
        text = "E" if x >= 0 else "W"
    elif 90 - azimuth < 1e-8:
        text = "N" if y >= 0 else "S"
    else:
        text = f'{"E" if x >= 0 else "W"} {fmt(azimuth)} {"N" if y >= 0 else "S"}'
    elevation = math.degrees(math.atan2(abs(z), horizontal))
    if elevation > 1e-8:
        text += f' {fmt(elevation)} {"U" if z >= 0 else "D"}'
    return text


def read_direction(text):
    axes = dict(zip("EWNSUD", np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]], float)))
    tokens = text.split()
    vector = axes[tokens[0]]
    for i in range(1, len(tokens), 2):
        angle = math.radians(float(tokens[i]))
        vector = math.cos(angle) * vector + math.sin(angle) * axes[tokens[i+1]]
    return vector


def basis(text):
    vectors = {}
    for clause in text.split(" AND "):
        axis, value = clause.split(" IS ")
        vectors[axis] = read_direction(value)
    if "X" not in vectors:
        vectors["X"] = np.cross(vectors["Y"], vectors["Z"])
    if "Y" not in vectors:
        vectors["Y"] = np.cross(vectors["Z"], vectors["X"])
    matrix = np.column_stack([vectors[a] for a in "XYZ"])
    if not np.allclose(matrix.T @ matrix, np.eye(3), atol=1e-8) or np.linalg.det(matrix) < .999999:
        raise ValueError(f"Invalid right-handed frame: {text}")
    return matrix


class DetailBuilder(PMLBuilder):
    """Preserve shared emission while retaining panel coordinates to 8 decimals."""
    def group(self, suffix):
        self.sube(TAG + suffix, attributes=("ORI Y IS N AND Z IS U", "POS E 0 N 0 U 0"))

    def panel(self, triangle, label):
        tri = np.array(triangle, float)
        a, b, c = tri
        normal = np.cross(b-a, c-a)
        if np.linalg.norm(normal) < 1e-6:
            raise ValueError("Zero-area panel")
        normal /= np.linalg.norm(normal)
        if np.dot(normal[:2], tri.mean(0)[:2]) < 0:
            tri = tri[[0, 2, 1]]
            a, b, c = tri
            normal = -normal
        xaxis = (b-a) / np.linalg.norm(b-a)
        yaxis = np.cross(normal, xaxis)
        profile = np.array([[np.dot(p-a, xaxis), np.dot(p-a, yaxis)] for p in tri])
        # A bounded vertex expansion gives a small construction overlap, without
        # the large apex spikes produced by offsetting a narrow triangle's edges.
        centre = profile.mean(0)
        delta = profile-centre
        profile += SEAM * delta / np.linalg.norm(delta, axis=1)[:,None]
        orientation = f"X IS {direction(xaxis)} AND Z IS {direction(normal)}"
        matrix = basis(orientation)
        assert np.max(np.abs(matrix-np.column_stack([xaxis, yaxis, normal]))) < 2e-9
        origin = a-WALL*normal
        start = len(self._lines)
        self.extrusion(tuple(origin), orientation, WALL, profile, label=label)
        count = 0
        in_profile = False
        for i in range(start, len(self._lines)):
            if self._lines[i] == "NEW VERTEX":
                in_profile = True
                self._lines[i+1] = "POS " + pos((*profile[count], 0))
                count += 1
            elif self._lines[i].startswith("POS ") and not in_profile:
                self._lines[i] = "POS " + pos(origin)
        assert count == 3

    def bores(self, offsets, diameter, length):
        assert self._lines.pop() == "END"
        for offset in offsets:
            self._lines.extend(("NEW NCYLINDER", f"DIAM {fmt(diameter)}", f"HEIG {fmt(length)}",
                                "ORI Z IS U AND Y IS N", "POS " + pos(offset), "NAPPFLAG 2", "END"))
        self._lines.append("END")


def build():
    b = DetailBuilder(close_elements=True)
    b.header("Square flange to DN600 round outlet, overall height 500 mm", (
        ("Source", "User image: flange 820 / opening 720 / 12 x diameter 14"),
        ("Reference Values", "Flange 20; shell 6; DN600 OD 610 / ID 598; outlet 80"),
        ("Datum", "Local bottom centre; square face U 500; outlet face U 0"),
        ("Status", "Offline candidate; native loading and visual acceptance pending"),
        ("Connection", "Fabricated open stub; receiving catalogue/P-points not supplied"),
        ("Load", "Select a writable ZONE; use $M with this file's absolute path")))
    b.equi(TAG)
    b.group("_01_FLANGE")
    ordinates = [-387.5, -129.5, 129.5, 387.5]
    for side in (-1, 1):
        b.box(50, 820, 20, (side*385, 0, 490), label="Square flange side strip")
        b.bores([(side*2.5, y, 0) for y in ordinates], 14, 22)
    for side in (-1, 1):
        b.box(720, 50, 20, (0, side*385, 490), label="Square flange cross strip")
        b.bores([(x, side*2.5, 0) for x in ordinates[1:3]], 14, 22)

    b.group("_02_TRANSITION")
    b.comment("Reference Value: 380 mm taper plus 20 mm square neck; shell thickness 6 mm.")
    b.comment("Neck extends 2 mm into flange and 4 mm into taper for joint contact.")
    for side in (-1, 1):
        b.box(6, 732, 26, (side*363, 0, 469), label="Open square neck side")
        b.box(720, 6, 26, (0, side*363, 469), label="Open square neck cross strip")
    radius = OD/2
    half = OPENING/2 + WALL
    for quarter in range(4):
        def rotate(p):
            angle = quarter*math.pi/2
            return np.array([p[0]*math.cos(angle)-p[1]*math.sin(angle),
                             p[0]*math.sin(angle)+p[1]*math.cos(angle), p[2]])
        # Radial-line development: each square side is a planar triangle;
        # the corner fans are conical sectors, discretised at the round rim.
        apex = rotate((half, half, 460))
        b.panel([rotate((half,-half,460)), rotate((radius,0,80)), apex],
                f"Flat transition panel {quarter+1}")
        for j in range(FACETS):
            a, c = j*math.pi/(2*FACETS), (j+1)*math.pi/(2*FACETS)
            b.panel([apex, rotate((radius*math.cos(a),radius*math.sin(a),80)),
                     rotate((radius*math.cos(c),radius*math.sin(c),80))],
                    f"Corner fan {quarter+1}, facet {j+1:02d}; 0.30 mm vertex overlap")

    b.group("_03_OUTLET")
    b.comment("DN600 is nominal. Reference Value: OD 610, wall 6, clear bore 598 mm.")
    b.comment("80 mm exposed outlet plus 4 mm joint overlap into the taper.")
    b.cyli(OD, 84, (0,0,0), label="Open fabricated DN600 circular outlet")
    b.bores([(0,0,0)], ID, 86)
    b.footer()
    return b.build()


def read_model(script):
    roots = parse_native_tree(script)
    assert len(roots) == 1 and roots[0].name == "/" + TAG
    root = roots[0]
    assert np.array_equal(xyz(root.get("POS")), [0,0,0])
    assert [s.name for s in root.children] == [f"/{TAG}{s}" for s in ("_01_FLANGE", "_02_TRANSITION", "_03_OUTLET")]
    solids = []
    for group in root.children:
        assert np.array_equal(xyz(group.get("POS")), [0,0,0])
        for node in group.children:
            primitive = {"node":node,"group":group.name,"origin":xyz(node.get("POS")),
                         "matrix":basis(node.get("ORI", "Y IS N AND Z IS U"))}
            if node.kind == "BOX":
                dims = np.array([float(node.get(k)) for k in ("XLEN","YLEN","ZLEN")])
                assert min(dims) > 0
                local = np.array([[a,b,c] for a in (-dims[0]/2,dims[0]/2)
                                  for b in (-dims[1]/2,dims[1]/2) for c in (-dims[2]/2,dims[2]/2)])
                primitive["dims"] = dims
            elif node.kind == "EXTRUSION":
                loops = [n for n in node.children if n.kind == "LOOP"]
                assert len(loops) == 1
                profile = np.array([xyz(n.get("POS"))[:2] for n in loops[0].children])
                assert len(profile) == 3
                ab, ac = profile[1]-profile[0], profile[2]-profile[0]
                assert ab[0]*ac[1]-ab[1]*ac[0] > 1e-3
                height = float(node.get("HEIG"))
                assert height > 0
                local = np.array([[*p,z] for z in (0,height) for p in profile])
                primitive.update(profile=profile,height=height)
            elif node.kind == "CYLI":
                diameter, height = float(node.get("DIAM")), float(node.get("HEIG"))
                assert min(diameter,height) > 0
                local = np.array([[diameter/2*math.cos(t),diameter/2*math.sin(t),z]
                                  for z in (-height/2,height/2) for t in np.linspace(0,2*math.pi,97)[:-1]])
                primitive.update(diameter=diameter,height=height)
            else:
                raise AssertionError(f"Unrecognised positive: {node.kind}")
            primitive["vertices"] = local@primitive["matrix"].T + primitive["origin"]
            solids.append(primitive)
    assert len(solids) == 109
    return roots, solids


def ray_ranges(solid, z, directions):
    """Intersect horizontal rays with actual parsed convex prisms/boxes."""
    matrix, origin, node = solid["matrix"], solid["origin"], solid["node"]
    o = (np.array([0,0,z])-origin)@matrix
    d = directions@matrix
    if node.kind == "BOX":
        normals = np.vstack((np.eye(3), -np.eye(3)))
        rhs = np.tile(solid["dims"]/2, 2)
    elif node.kind == "EXTRUSION":
        p = solid["profile"]
        normals, rhs = [[0,0,-1],[0,0,1]], [0,solid["height"]]
        for a,b in zip(p,np.roll(p,-1,axis=0)):
            edge = b-a
            n = np.array([edge[1],-edge[0],0])
            normals.append(n)
            rhs.append(np.dot(n[:2],a))
        normals,rhs = np.array(normals),np.array(rhs)
    else:
        if abs(z-origin[2]) > solid["height"]/2 + 1e-7:
            return np.full(len(directions),np.inf),np.full(len(directions),-np.inf)
        return np.full(len(directions),ID/2),np.full(len(directions),OD/2)
    numerator = rhs - normals@o
    denominator = d@normals.T
    parallel = np.abs(denominator) < 1e-10
    invalid = np.any(parallel & (numerator < -1e-7),axis=1)
    with np.errstate(divide="ignore",invalid="ignore"):
        t = numerator / denominator
    low = np.max(np.where(denominator < -1e-10,t,-np.inf),axis=1)
    high = np.min(np.where(denominator > 1e-10,t,np.inf),axis=1)
    low[invalid],high[invalid] = np.inf,-np.inf
    return low,high


def verify(script):
    assert not validate_pml(script)
    roots,solids = read_model(script)
    all_vertices = np.vstack([s["vertices"] for s in solids])
    bounds = np.stack([all_vertices.min(0),all_vertices.max(0)])
    assert np.allclose(bounds,[[-410,-410,0],[410,410,500]],atol=1e-6)
    flange = [s for s in solids if s["group"].endswith("_01_FLANGE")]
    holes = []
    for s in flange:
        assert s["node"].kind == "BOX" and len(s["node"].children) in (2,4)
        for hole in s["node"].children:
            assert hole.kind == "NCYLINDER"
            assert float(hole.get("DIAM")) == 14
            assert float(hole.get("HEIG")) > s["dims"][2]
            assert hole.get("NAPPFLAG") == "2"
            local = xyz(hole.get("POS"))
            assert all(s["dims"][:2]/2 - np.abs(local[:2]) >= 7)
            holes.append(local@s["matrix"].T+s["origin"])
    holes = np.array(holes)
    expected = {(x,y) for x in (-387.5,-129.5,129.5,387.5) for y in (-387.5,387.5)}
    expected |= {(x,y) for x in (-387.5,387.5) for y in (-129.5,129.5)}
    assert len(holes) == 12 and set(map(tuple, holes[:,:2])) == expected
    pipe = [s for s in solids if s["node"].kind == "CYLI"]
    assert len(pipe) == 1
    pipe = pipe[0]
    assert pipe["diameter"] == OD and pipe["height"] == 84
    assert np.array_equal(pipe["origin"],[0,0,42])
    assert len(pipe["node"].children) == 1
    cut = pipe["node"].children[0]
    assert cut.kind == "NCYLINDER" and float(cut.get("DIAM")) == ID
    assert float(cut.get("HEIG")) > 84 and cut.get("NAPPFLAG") == "2"
    assert np.array_equal(xyz(cut.get("POS")),[0,0,0])
    # Full polar rays detect detached panels, missing angular sectors and
    # unexpected inward caps; use the emitted solids rather than source faces.
    angles = np.linspace(0,2*math.pi,1440,endpoint=False)
    directions = np.column_stack([np.cos(angles),np.sin(angles),np.zeros(len(angles))])
    samples = []
    body = [s for s in solids if not s["group"].endswith("_01_FLANGE")]
    for z in (0,40,78,79,80,81,82,83,84,85,100,150,250,350,450,456,458,460,462,470,480):
        ranges = [ray_ranges(s,z,directions) for s in body]
        lows,highs = np.array([r[0] for r in ranges]),np.array([r[1] for r in ranges])
        valid = (highs >= lows-1e-7) & (highs > 0)
        covered = np.any(valid,axis=0)
        assert np.all(covered), f"Open angular sector at U {z}: {np.count_nonzero(~covered)} rays"
        inner = np.min(np.where(valid,lows,np.inf),axis=0)
        outer = np.max(np.where(valid,highs,-np.inf),axis=0)
        order = np.argsort(np.where(valid,lows,np.inf),axis=0)
        sorted_lows = np.take_along_axis(np.where(valid,lows,np.inf),order,axis=0)
        sorted_highs = np.take_along_axis(np.where(valid,highs,-np.inf),order,axis=0)
        running_highs = np.maximum.accumulate(sorted_highs,axis=0)
        eligible = np.isfinite(sorted_lows[1:]) & np.isfinite(running_highs[:-1])
        with np.errstate(invalid="ignore"):
            gaps = sorted_lows[1:] - running_highs[:-1]
        maximum_gap = float(np.max(np.where(eligible,np.maximum(gaps,0),0)))
        assert maximum_gap < .05, f"Disconnected wall along a ray at U {z}: {maximum_gap}"
        assert np.min(inner) > ID/2 - .75, f"Obstructed bore at U {z}"
        assert np.min(outer-inner) > 5.9, f"Thin or missing wall at U {z}"
        samples.append({"elevation_mm":z,"rays":len(angles),"covered_rays":int(covered.sum()),
                        "minimum_inner_radius_mm":float(inner.min()),"minimum_radial_wall_mm":float((outer-inner).min()),
                        "maximum_internal_radial_gap_mm":maximum_gap})
    assert np.allclose([np.min(s["vertices"][:,2]) for s in flange],480)
    return {"status":"PASS_OFFLINE","equipment":1,"subequipment":3,"positive_solids":109,
            "transition_triangular_panels":100,"negative_cylinders":13,"flange_bolt_holes":12,
            "overall_bounds_mm":bounds.tolist(),"dn":600,"outlet_od_mm":OD,"outlet_id_mm":ID,
            "flange_clear_opening_mm":[720,720],"square_neck_clear_opening_mm":[720,720],
            "hole_xy_mm":holes[:,:2].tolist(),"quarter_circle_facets":FACETS,
            "circle_chord_sagitta_mm":OD/2*(1-math.cos(math.pi/(4*FACETS))),
            "panel_vertex_expansion_mm":SEAM,"outlet_joint_overlap_mm":4,"section_ray_checks":samples,
            "native_E3D_load":"PENDING","native_visual_acceptance":"PENDING",
            "save_work":"NOT_REQUESTED","reopen_persistence":"PENDING",
            "receiving_catalogue_P_points":"NOT_BOUND_FABRICATED_STUB",
            "notes":["Polar sampling does not certify pressure integrity or manufacture.",
                     "Thin triangular prisms are a faceted approximation; native rendering requires review."]}


def preview(script):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle,Rectangle
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    _,solids = read_model(script)
    fig = plt.figure(figsize=(14,8),facecolor="#f6f8fb")
    ax = fig.add_subplot(121,projection="3d",computed_zorder=False)
    ax.set_facecolor("#f6f8fb")
    faces,colors = [],[]
    for s in solids:
        v = s["vertices"]
        kind=s["node"].kind
        if kind == "BOX":
            ids = ((0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3))
        elif kind == "EXTRUSION":
            ids = ((0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5))
        else:
            # Both cylindrical wall surfaces and the open annular end faces.
            n=len(v)//2
            inside=v.copy()
            inside[:,:2]*=ID/OD
            for j in range(n):
                k=(j+1)%n
                faces.extend(([v[j],v[k],v[n+k],v[n+j]],
                              [inside[j],inside[n+j],inside[n+k],inside[k]],
                              [v[j],inside[j],inside[k],v[k]]))
                colors.extend(["#6c91ac","#39566b","#9bb6c8"])
            continue
        faces.extend([[v[i] for i in face] for face in ids])
        color="#a3b9c9" if s["group"].endswith("_01_FLANGE") else "#7298b2"
        colors.extend([color]*len(ids))
    ax.add_collection3d(Poly3DCollection(faces,facecolors=colors,edgecolors="#55778d",linewidths=.12,alpha=1))
    # Dark disks mark the verified bores in the overview. The dimensioned plan
    # at right shows their exact circular boundaries; PML contains real cuts.
    for s in solids:
        if not s["group"].endswith("_01_FLANGE"):continue
        for h in s["node"].children:
            c=s["origin"]+xyz(h.get("POS"))
            ring=[[c[0]+7*math.cos(a),c[1]+7*math.sin(a),500.05] for a in np.linspace(0,2*math.pi,24)]
            ax.add_collection3d(Poly3DCollection([ring],facecolors="#263946",edgecolors="#263946"))
    ax.set(xlim=(-450,450),ylim=(-450,450),zlim=(-5,510))
    ax.set_box_aspect((900,900,515));ax.view_init(elev=23,azim=-54)
    ax.set_axis_off();ax.set_title("Square flange to DN600\nEQUI / 3 SUBE groups",fontweight="bold",pad=15)
    plan=fig.add_subplot(222);plan.set_aspect("equal");plan.set_facecolor("#f6f8fb")
    plan.add_patch(Rectangle((-410,-410),820,820,facecolor="#afc4d2",edgecolor="#284a60",lw=1.8))
    plan.add_patch(Rectangle((-360,-360),720,720,facecolor="#f6f8fb",edgecolor="#284a60",lw=1.4))
    plan.add_patch(Circle((0,0),OD/2,fill=False,edgecolor="#487b9a",ls="--",lw=1.2))
    holes=verify(script)["hole_xy_mm"]
    for c in holes:plan.add_patch(Circle(c,7,facecolor="#f6f8fb",edgecolor="#243b49",lw=.8))
    plan.set(xlim=(-465,465),ylim=(-465,465));plan.axis("off")
    plan.set_title("820 x 820 flange / 720 x 720 opening\n12 x diameter 14 holes",fontsize=11)
    side=fig.add_subplot(224);side.set_aspect("equal");side.set_facecolor("#f6f8fb")
    side.plot([-410,-410,410,410], [480,500,500,480],color="#294d64",lw=2)
    side.plot([-366,-366,-305,-305,305,305,366,366],[480,460,80,0,0,80,460,480],color="#294d64",lw=2)
    side.axvline(0,color="#b3c1cb",ls="--",lw=.7)
    side.annotate("",xy=(445,0),xytext=(445,500),arrowprops=dict(arrowstyle="<->",color="#be692f"))
    side.text(460,250,"500",va="center",color="#a75420",fontweight="bold")
    for y,t in ((490,"20 flange"),(270,"400 transition"),(40,"80 outlet")):
        side.text(700,y,t,va="center",fontsize=10)
    side.text(0,-55,"DN600: reference OD 610 / wall 6",ha="center",fontsize=10)
    side.set(xlim=(-460,1250),ylim=(-80,550));side.axis("off")
    fig.suptitle("SQUARE TO ROUND  |  H 500 mm",fontsize=18,fontweight="bold",x=.04,ha="left")
    fig.text(.04,.025,"Offline geometry preview. Thicknesses and axial allocation are Reference Values. Native E3D acceptance pending.",fontsize=9,color="#526775")
    fig.subplots_adjust(top=.87,bottom=.1,wspace=.1,hspace=.3)
    fig.savefig(OUT/f"{NAME}_preview.png",dpi=160,bbox_inches="tight")
    plt.close(fig)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    script=build()
    audit=verify(script)
    path=OUT/f"{NAME}.pml"
    path.write_text(script,encoding="ascii")
    # Reopen bytes from disk for the final audit, not the in-memory builder.
    audit=verify(path.read_text(encoding="ascii"))
    audit["pml_sha256"]=hashlib.sha256(path.read_bytes()).hexdigest()
    audit["source_plan_sha256"]=hashlib.sha256((PROJECT/"imports/source_plan.png").read_bytes()).hexdigest()
    (OUT/f"{NAME}_audit.json").write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    preview(path.read_text(encoding="ascii"))
    print(json.dumps({k:audit[k] for k in ("status","positive_solids","transition_triangular_panels","flange_bolt_holes","overall_bounds_mm","pml_sha256")},indent=2))


if __name__ == "__main__":
    main()
