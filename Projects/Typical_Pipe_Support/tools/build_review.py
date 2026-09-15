"""Build an isolated review of the located typical support; never deploy live."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from wsb.pml_builder import PMLBuilder, validate_pml
from wsb.pml_parser import parse_primitives, bounds_of
from wsb.extrusion_builder import ExtrusionBuilder, ExtrusionSpec

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"C:\e3d_models\SINGLE_TYPICAL_PIPE_SUPPORT.pml")
EXPECTED_HASH = "52c523d709d5f46bd0a9a4fd10f7cbb36eeac5046c1cf45896c45abc09f3806c"
EQ = "TPS_R1_HARDWARE"
ZONE = "ZONE_TYPICAL_SUPPORT_R1"
OUT = PROJECT / "output" / "Typical_Pipe_Support_R1.pml"
T = math.atan2(285, 1039)
SN, CS = math.sin(T), math.cos(T)
CARDINAL = {"E": (1,0,0), "N": (0,1,0), "U": (0,0,1),
            "W": (-1,0,0), "S": (0,-1,0), "D": (0,0,-1)}

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def frame(ori):
    m = re.fullmatch(r"Y IS ([ENUSWD]) AND Z IS ([ENUSWD])(?: ([\d.]+) U)?", ori)
    assert m, ori
    y = CARDINAL[m[1]]
    z = CARDINAL[m[2]]
    if m[3]:
        assert m[2] == "N"
        a = math.radians(float(m[3]))
        z = (0, math.cos(a), math.sin(a))
    return cross(y, z), y, z

def vertices3(p):
    """Transform parsed extrusion vertices, including both end planes.

    The shared parser is used; its current bounds_of EXTRUSION branch assumes
    world Z, so rotated bounds are evaluated explicitly for this scoped report.
    """
    x, y, z = frame(p["orientation"])
    o = (p["east"], p["north"], p["up"])
    return [tuple(o[i] + a*x[i] + b*y[i] + h*z[i] for i in range(3))
            for a,b in p["vertices"] for h in (0,p["heig"])]

def extent(p):
    if p["kind"] != "EXTRUSION":
        return bounds_of(p)
    v = vertices3(p)
    return tuple(q for i in range(3) for q in (min(t[i] for t in v),max(t[i] for t in v)))

def only(script, label):
    match = re.search(r"(?m)^-- " + re.escape(label) + r"(?:[ \t][^\n]*)?\n",script)
    assert match, label
    fragment = script[match.end():].split("\n-- ",1)[0]
    found = parse_primitives(f"NEW EQUI /{EQ}\n" + fragment, EQ)
    assert found, label
    return found

def build(source):
    # Preserve source section attributes verbatim, changing only their names.
    sections = re.findall(r"NEW SCTN /\S+\n(?:[^\n]*\n)*?SPRE SPCOMPONENT /\S+", source)
    assert len(sections) == 2
    sections = [s.replace("SCTN-TYPICAL-BEAM", "TPS_R1_BEAM").replace(
        "SCTN-TYPICAL-BRACE", "TPS_R1_BRACE") + "\nEND" for s in sections]
    header = "\n".join([
        "-- Typical Pipe Support R1: independent review candidate.",
        "-- Select a writable SITE before loading. No delete or save commands.",
        "-- Source identification is provisional; see the review report.",
        "-- All new details are Reference Values, not a fabrication design.",
        f"NEW ZONE /{ZONE}", "ORI Y IS N AND Z IS U", "POS E 0 N 0 U 0",
        "NEW STRU /TPS_R1_STRUCTURE", "ORI Y IS N AND Z IS U", "POS E 0 N 0 U 0",
        "NEW FRMW /TPS_R1_FRAME",
        *sections, f"/{ZONE}", "",
    ])
    b = PMLBuilder()
    b.equi(EQ)
    b.sube("TPS_R1_WALL_PLATES")
    b.box(180,16,350,(0,8,-75),label="UPPER_WALL_PLATE")
    b.box(180,16,160,(0,8,-470),label="LOWER_WALL_PLATE")

    # The gusset is placed to one side of the angle's TOAY face, rather than
    # centred on the angle workline. This catalogue face/roll must be checked live.
    b.sube("TPS_R1_CONNECTION_PLATES")
    b.extrusion((-4,0,0),"Y IS U AND Z IS E",8,
        [(16,-220),(16,-156),(22,-150),(130,-150),(136,-156),(26,-220)],
        label="ROOT_HAUNCH Reference Value: 8 mm plate, 120 mm reach, weld relief")
    b.extrusion((0,0,0),"Y IS U AND Z IS E",8,
        [(965,-150),(1145,-150),(1145,-255),(1130,-270),(980,-270),(965,-255)],
        label="UPPER_GUSSET Reference Value: 8 mm, 180 x 120 envelope, 15 mm clips")
    b.extrusion((0,0,0),"Y IS U AND Z IS E",8,
        [(16,-530),(16,-420),(86,-420),(96,-430),(96,-500),(70,-530)],
        label="LOWER_GUSSET Reference Value: 8 mm, 80 x 110 envelope, clipped corners")

    b.sube("TPS_R1_FILLET_WELDS")
    # Physical triangular fillet sections. No arbitrary spheres or bead blobs.
    b.extrusion((-37.5,16,-150),"Y IS U AND Z IS E",75,
        [(0,0),(6,0),(0,-6)], label="BEAM_ROOT_WELD Reference Value: 6 mm leg")
    for side in (-1,1):
        # Local X points West for Y=Up / Z=North.
        b.extrusion((4*side,28,-150),"Y IS U AND Z IS N",92,
            [(0,0),(-6*side,0),(0,-6)],
            label=f"HAUNCH_TOP_WELD_{side} Reference Value: 6 mm leg")
        b.extrusion((4*side,16,-214),"Y IS N AND Z IS U",48,
            [(0,0),(6*side,0),(0,6)],
            label=f"HAUNCH_WALL_WELD_{side} Reference Value: 6 mm leg")
    for e,sgn in ((0,-1),(8,1)):
        b.extrusion((e,977,-150),"Y IS U AND Z IS N",156,
            [(0,0),(-6*sgn,0),(0,-6)],
            label=f"UPPER_GUSSET_BEAM_WELD_{e} Reference Value: 6 mm leg")
        b.extrusion((e,16,-524),"Y IS N AND Z IS U",98,
            [(0,0),(6*sgn,0),(0,6)],
            label=f"LOWER_GUSSET_WALL_WELD_{e} Reference Value: 6 mm leg")

    # Angle-local +X is perpendicular upward to the brace, local +Y is East.
    # Weld triangles fill the outside corner at the angle/gusset lap face E=0.
    for joint, n0, n1 in (("LOWER",35,75),("UPPER",995,1043)):
        for edge, offset, sign in (("TOP",0,1),("BOTTOM",-50,-1)):
            pos = (0,n0-offset*SN,-470+(n0-16)*285/1039+offset*CS)
            b.extrusion(pos,f"Y IS E AND Z IS N {math.degrees(T):.6f} U",
                (n1-n0)/CS,[(0,0),(sign*5,0),(0,-5)],
                label=f"{joint}_LAP_{edge} Reference Value: 5 mm leg; catalogue face pending")

    positions = [(-45,60),(45,60),(-45,-210),(45,-210),(-45,-470),(45,-470)]
    for i,(e,u) in enumerate(positions,1):
        b.sube(f"TPS_R1_HEX_SCREW_{i:02d}")
        b.cyli(20,19,(e,0,u),axis="N",label=f"SHANK_{i} Reference Value: diameter 20; hidden anchorage unspecified")
        # Hollow washers consist of closed annular sectors; shank does not
        # substitute for a hole and no solid disk is mislabelled as a washer.
        for k in range(24):
            a,c = 2*math.pi*k/24,2*math.pi*(k+1)/24
            pts = [(r*math.cos(t),r*math.sin(t)) for r,t in ((11,a),(20,a),(20,c),(11,c))]
            b.extrusion((e,16,u),"Y IS U AND Z IS N",3,pts,
                label=f"WASHER_{i}_{k:02d} Reference Value: OD40 ID22 x3; 24 sectors")
        r = 30/math.sqrt(3)
        b.comment(f"HEX_HEAD_{i} Reference Value: AF30 x12; not a certified fastener standard")
        head = ExtrusionBuilder().build(ExtrusionSpec(
            (e,19,u),"Y IS U AND Z IS N",12,
            tuple((r*math.cos(k*math.pi/3),r*math.sin(k*math.pi/3)) for k in range(6))))
        # Use the shared six-decimal emitter for the regular hexagon. Remove
        # unit suffixes only for compatibility with the shared primitive parser.
        b._lines.extend(head.replace("mm", "").splitlines())
        b.primitive_count += 1
    return header + b.build() + f"\n/{ZONE}\n"

def verify(script, source):
    assert not validate_pml(script), validate_pml(script)
    assert not re.search(r"(?im)^\s*(DELETE|SAVEWORK|SAVE WORK)\b",script)
    assert len(re.findall(r"(?m)^NEW SCTN ",script)) == 2
    for old,new in (("SCTN-TYPICAL-BEAM","TPS_R1_BEAM"),("SCTN-TYPICAL-BRACE","TPS_R1_BRACE")):
        pat = r"NEW SCTN /{}\n(.*?)SPRE SPCOMPONENT (/\S+)"
        assert re.search(pat.format(old),source,re.S).groups() == re.search(pat.format(new),script,re.S).groups()
    names = re.findall(r"(?m)^NEW \S+ (/\S+)",script)
    assert len(names) == len(set(names))
    ps = parse_primitives(script,EQ)
    assert len(ps) == 174, len(ps)
    for p in ps:
        for key in ("heig","diam","xlen","ylen","zlen"):
            if key in p: assert 0 < p[key] < 2000, (key,p)
        if p["kind"] == "EXTRUSION":
            v=p["vertices"]
            assert len(set(v)) >= 3
            assert abs(sum(a[0]*c[1]-c[0]*a[1] for a,c in zip(v,v[1:]+v[:1]))) > .001
    eb = [extent(p) for p in ps]
    assert min(x[2] for x in eb) >= -1e-6, "Geometry penetrates the wall datum"
    assert extent(only(script,"UPPER_WALL_PLATE")[0]) == (-90,90,0,16,-250,100)
    assert extent(only(script,"LOWER_WALL_PLATE")[0]) == (-90,90,0,16,-550,-390)
    for i in range(1,7):
        h = next(p for p in ps if p["kind"]=="EXTRUSION" and p["heig"]==12 and
                 abs(p["east"]-((-45,45)[(i-1)%2]))<1e-5 and p["up"]==[60,60,-210,-210,-470,-470][i-1])
        assert len(h["vertices"]) == 6
        v=h["vertices"]
        lengths=[math.dist(a,c) for a,c in zip(v,v[1:]+v[:1])]
        assert max(lengths)-min(lengths)<.03
        hb=extent(h)
        assert abs(hb[2]-19)<.001 and abs(hb[3]-31)<.001
        assert max(abs(hb[0]),abs(hb[1])) < 90
    # Confirm the four lap seam roots sit within their plate outlines in side view.
    gp=[only(script,k)[0] for k in ("UPPER_GUSSET", "LOWER_GUSSET")]
    for p in gp:
        assert extent(p)[:2] == (0,8), "Gusset must abut, not straddle, the assumed E=0 angle face"
    upper,lower = [[(v[1],v[2]) for v in vertices3(p)[::2]] for p in gp]
    def inside(pt, poly):
        vals=[(b[0]-a[0])*(pt[1]-a[1])-(b[1]-a[1])*(pt[0]-a[0])
              for a,b in zip(poly,poly[1:]+poly[:1])]
        return min(vals)>=-.03 or max(vals)<=.03
    laps=[p for p in ps if p.get("orientation","").startswith("Y IS E AND Z IS N ")]
    assert len(laps)==4
    for p in laps:
        poly = upper if p["north"]>900 else lower
        assert all(inside((v[1],v[2]),poly) for v in vertices3(p))
    # Seating chain and actual hollow washer geometry, read back from output.
    for i in range(1,7):
        shank=only(script,f"SHANK_{i}")[0]
        head=only(script,f"HEX_HEAD_{i}")[0]
        assert extent(shank)[2:4] == (0,19)
        assert abs(extent(head)[2]-19)<.001
        for k in range(24):
            washer=only(script,f"WASHER_{i}_{k:02d}")[0]
            assert extent(washer)[2:4] == (16,19)
            radii=sorted(math.hypot(*v) for v in washer["vertices"])
            assert all(abs(r-11)<.08 for r in radii[:2])
            assert all(abs(r-20)<.08 for r in radii[2:])
            assert radii[0]*math.cos(math.pi/24)>shank["diam"]/2, "Washer bore clashes with screw"
    # All projecting weld runs stay below TOS. Wall fasteners above U=0 are
    # inherited mounting positions, not obstructions on the cantilever surface.
    weld_start=script.index("NEW SUBE /TPS_R1_FILLET_WELDS")
    weld_end=script.index("NEW SUBE /TPS_R1_HEX_SCREW_01")
    welds=parse_primitives(f"NEW EQUI /{EQ}\n"+script[weld_start:weld_end],EQ)
    assert len(welds)==13 and all(extent(w)[5] <= -149.99 for w in welds)
    return {"status":"STATIC_PASS_LIVE_PENDING", "hardware_primitives":len(ps),
            "native_sections":2,"hex_heads":6,"annular_washers":6,"weld_runs":13,
            "source_sections_preserved":True,"wall_plates_preserved":True,
            "hardware_bounds_enu_mm":[min(t[0] for t in eb),max(t[1] for t in eb),
                                      min(t[2] for t in eb),max(t[3] for t in eb),
                                      min(t[4] for t in eb),max(t[5] for t in eb)],
            "limits":["Source identity provisional", "SCTN catalogue and roll not read live",
                      "Angle TOAY face assumed at E=0 with steel to West and down",
                      "Full catalogue steel/weld contact and clashes require E3D",
                      "Load rating, anchor embedment, weld sizing and material grades TBC"]}

def build_resume(script):
    """Continue the reported R1 failure, after FRMW exists but before SCTN.

    This continuation is deliberately specific to the reported line-12 failure.
    It never recreates or deletes the existing ZONE/STRU/FRMW containers.
    """
    tail = script[script.index("NEW SCTN /TPS_R1_BEAM\n"):]
    return ("-- Resume R1 only after the reported FRMW ORI failure, before any SCTN exists.\n"
            "-- No deletion or save. Run once.\n/TPS_R1_FRAME\n" + tail)


def main():
    raw=SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_HASH, "Source changed: reconcile before generating"
    archive=PROJECT/"imports"/"2026-09-13_SINGLE_TYPICAL_PIPE_SUPPORT.pml"
    archive.parent.mkdir(parents=True,exist_ok=True)
    if archive.exists(): assert archive.read_bytes()==raw
    else: archive.write_bytes(raw)
    source=raw.decode("utf-8-sig").replace("\r\n","\n")
    script=build(source)
    audit=verify(script,source)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(script,encoding="ascii")
    reread=OUT.read_text(encoding="ascii")
    verify(reread,source)
    resume_path=OUT.with_name("Typical_Pipe_Support_R1_RESUME.pml")
    resume=build_resume(reread)
    assert not validate_pml(resume)
    assert parse_primitives(resume,EQ) == parse_primitives(reread,EQ)
    resume_path.write_text(resume,encoding="ascii")
    assert resume_path.read_text(encoding="ascii")==resume
    audit["source_sha256"]=EXPECTED_HASH
    audit["output_sha256"]=hashlib.sha256(OUT.read_bytes()).hexdigest()
    audit["resume_sha256"]=hashlib.sha256(resume_path.read_bytes()).hexdigest()
    audit["framework_header_fix"]="Removed ORI and unneeded POS; E3D retry pending"
    (OUT.parent/"Typical_Pipe_Support_R1_checks.json").write_text(json.dumps(audit,indent=2)+"\n",encoding="ascii")
    print(json.dumps(audit,indent=2))

if __name__ == "__main__": main()
