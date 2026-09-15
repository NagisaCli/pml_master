"""R3: explicit assembly ownership, tapered lap nodes and machined fasteners."""
import hashlib
import json
import math
import re
from pathlib import Path

from build_review import PROJECT, PMLBuilder, parse_primitives, validate_pml, extent, vertices3

BASE=PROJECT/"output/Typical_Pipe_Support_R2.pml"
BASE_HASH="129dc71d658babb981e318b64c87371aa77044a9a8406483610b83d18604dbb0"
OUT=PROJECT/"output/Typical_Pipe_Support_R3.pml"
DEPLOY=Path(r"C:\e3d_models\SINGLE_TYPICAL_PIPE_SUPPORT_R3.pml")
EQ="TPS_R3_HARDWARE"
ZONE="ZONE_TYPICAL_SUPPORT_R3"
THETA=math.atan2(285,1039)
S,C=math.sin(THETA),math.cos(THETA)
LOWER=[(16,-530),(16,-398),(32,-398),(190,-424),(200,-438),(200,-478),(176,-505),(32,-530)]
UPPER=[(920,-150),(1140,-150),(1140,-200),(1115,-234),(945,-281),(930,-278),(920,-262)]
FASTENERS=[(-45,60),(45,60),(-45,-210),(45,-210),(-45,-470),(45,-470)]

def zline(n): return -470+(n-16)*285/1039

def area(v):
    return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(v,v[1:]+v[:1]))/2

def clockwise(v):
    v=list(v)
    return v if area(v)<0 else list(reversed(v))

class DetailBuilder(PMLBuilder):
    """Use the shared emitter and native closed ownership, with precise profiles."""
    def group(self,name):
        self.sube("TPS_R3_"+name,attributes=("ORI Y IS N AND Z IS U","POS E 0 N 0 U 0"))

    def profile(self,label,pos,ori,length,vertices):
        verts=clockwise(vertices)
        start=len(self._lines)
        self.extrusion(pos,ori,length,verts,level=(5,10),label=label)
        # Preserve the shared command/ownership emitter while supplying exact
        # numeric coordinates to its generated VERTEX slots (default is 0.1 mm).
        idx=0
        for i in range(start,len(self._lines)):
            if self._lines[i]=="NEW VERTEX":
                x,y=verts[idx]
                self._lines[i+1]=f"POS E {x:.6f} N {y:.6f} U 0"
                idx+=1
        assert idx==len(verts)

    def bores(self,positions,diameter,length):
        # The immediately preceding closed positive primitive is reopened for
        # its negative children; no negative is created at SUBE level.
        while self._lines and not self._lines[-1].strip(): self._lines.pop()
        assert self._lines.pop()=="END"
        for x,y,z in positions:
            self._lines.extend(["NEW NCYLINDER",f"DIAM {diameter:.6f}",f"HEIG {length:.6f}",
                "ORI Y IS N AND Z IS U",f"POS E {x:.6f} N {y:.6f} U {z:.6f}",
                "NAPPFLAG 2","END"])
        self._lines.append("END")

def clipped(w,h,k):
    x,y=w/2,h/2
    return [(-x+k,-y),(x-k,-y),(x,-y+k),(x,y-k),(x-k,y),(-x+k,y),(-x,y-k),(-x,-y+k)]

def build_r3(base):
    # Keep the native main channel exactly. Shorten/reposition the angle's cut
    # ends inside longer lap regions; its centreline bearing/profile are retained.
    sections=re.findall(r"NEW SCTN /\S+\n.*?\nEND",base,re.S)
    assert len(sections)==2
    beam=sections[0].replace("TPS_R2_","TPS_R3_")
    brace=sections[1].replace("TPS_R2_","TPS_R3_")
    brace=re.sub(r"(?m)^POSS .*",f"POSS E 0 N 80 U {zline(80):.6f}",brace)
    brace=re.sub(r"(?m)^POSE .*",f"POSE E 0 N 1080 U {zline(1080):.6f}",brace)
    header="\n".join([
        "-- Typical Pipe Support R3: complete independent geometry review.",
        "-- Start from a writable SITE. No DELETE, external model lookup or SAVEWORK.",
        "-- All new connection and fastener detail dimensions are Reference Values.",
        "-- R2 screenshot is the unedited working baseline; original steel catalogue retained.",
        f"NEW ZONE /{ZONE}","ORI Y IS N AND Z IS U","POS E 0 N 0 U 0",
        "NEW STRU /TPS_R3_STRUCTURE","ORI Y IS N AND Z IS U","POS E 0 N 0 U 0",
        "NEW FRMW /TPS_R3_FRAME",beam,brace,"END","END",f"/{ZONE}",""])
    b=DetailBuilder(close_elements=True)
    b.equi(EQ)
    b.group("MOUNTING_PLATES")
    for name,cu,height,holes in (("UPPER",-75,350,FASTENERS[:4]),("LOWER",-470,160,FASTENERS[4:])):
        b.profile(f"{name}_MOUNT_PLATE Reference Value: 6 mm clipped corners; source envelope",
            (0,0,cu),"Y IS U AND Z IS N",16,clipped(180,height,6))
        # Plate local X is West, Y is Up, Z is North; EXTRUSION origin is N=0.
        b.bores([(-e,u-cu,8) for e,u in holes],22,20)

    b.group("GUSSETS")
    b.profile("ROOT_HAUNCH Reference Value: clipped 8 mm plate below the beam",
        (-4,0,0),"Y IS U AND Z IS E",8,
        [(16,-220),(16,-156),(22,-150),(130,-150),(136,-156),(26,-220)])
    b.profile("UPPER_GUSSET Reference Value: tapered to the brace envelope; E=0..8 face pending",
        (0,0,0),"Y IS U AND Z IS E",8,UPPER)
    b.profile("LOWER_GUSSET Reference Value: extended tapered lap; E=0..8 face pending",
        (0,0,0),"Y IS U AND Z IS E",8,LOWER)

    b.group("FILLET_WELDS")
    b.profile("BEAM_ROOT_WELD Reference Value: 6 mm leg",(-37.5,16,-150),"Y IS U AND Z IS E",75,[(0,0),(6,0),(0,-6)])
    for side in (-1,1):
        b.profile(f"HAUNCH_TOP_WELD_{side} Reference Value: 6 mm leg",(4*side,28,-150),"Y IS U AND Z IS N",92,[(0,0),(-6*side,0),(0,-6)])
        b.profile(f"HAUNCH_WALL_WELD_{side} Reference Value: 6 mm leg",(4*side,16,-214),"Y IS N AND Z IS U",48,[(0,0),(6*side,0),(0,6)])
    for e,sign in ((0,-1),(8,1)):
        b.profile(f"UPPER_GUSSET_BEAM_WELD_{e} Reference Value: 6 mm leg",(e,935,-150),"Y IS U AND Z IS N",190,[(0,0),(-6*sign,0),(0,-6)])
        b.profile(f"LOWER_GUSSET_WALL_WELD_{e} Reference Value: 6 mm leg",(e,16,-518),"Y IS N AND Z IS U",108,[(0,0),(6*sign,0),(0,6)])
    for joint,a,bn in (("LOWER",95,170),("UPPER",970,1060)):
        for edge,off,sign in (("TOP",0,1),("BOTTOM",-50,-1)):
            b.profile(f"{joint}_LAP_{edge} Reference Value: continuous 5 mm fillet; section face pending",
                (0,a-off*S,zline(a)+off*C),f"Y IS E AND Z IS N {math.degrees(THETA):.6f} U",
                (bn-a)/C,[(0,0),(sign*5,0),(0,-5)])

    for i,(e,u) in enumerate(FASTENERS,1):
        b.group(f"SCREW_{i:02d}")
        b.cyli(20,19,(e,0,u),axis="N",label=f"SHANK_{i} Reference Value: 20 mm; anchor internals TBC")
        b.cyli(40,3,(e,16,u),axis="N",label=f"WASHER_{i} Reference Value: OD40 ID22 x3, one bored solid")
        b.bores([(0,0,0)],22,5)
        r=30/math.sqrt(3)
        b.profile(f"HEX_HEAD_{i} Reference Value: AF30 x12, clockwise native-style loop",
            (e,19,u),"Y IS U AND Z IS N",12,
            [(r*math.cos(k*math.pi/3),r*math.sin(k*math.pi/3)) for k in range(6)])
    return header+b.build()+f"\n/{ZONE}\n"

def labelled(script,label):
    m=re.search(r"(?m)^-- "+re.escape(label)+r"(?:[ \t][^\n]*)?\n",script)
    assert m,label
    block=script[m.end():].split("\n-- ",1)[0]
    ps=parse_primitives(f"NEW EQUI /{EQ}\n"+block,EQ)
    assert ps,label
    return ps[0],block

def inside(pt,poly):
    # Ray crossing, including boundary; unlike convex-only tests this also
    # handles the root relief/corner changes in the new node silhouettes.
    yes=False
    x,y=pt
    for a,b in zip(poly,poly[1:]+poly[:1]):
        cross=(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])
        if abs(cross)<.02 and min(a[0],b[0])-.01<=x<=max(a[0],b[0])+.01 and min(a[1],b[1])-.01<=y<=max(a[1],b[1])+.01: return True
        if (a[1]>y)!=(b[1]>y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]: yes=not yes
    return yes

def verify_r3(script,base):
    assert not validate_pml(script),validate_pml(script)
    assert not re.search(r"(?im)^\s*(DELETE|SAVEWORK|\$M)\b",script)
    assert "/TPS_R2_" not in script and "/TPS_R1_" not in script
    # Explicit hierarchy proves that neither bore nor LOOP owns a following part.
    allowed={"SITE":{"ZONE"},"ZONE":{"STRU","EQUI"},"STRU":{"FRMW"},
        "FRMW":{"SCTN"},"SCTN":set(),"EQUI":{"SUBE"},"SUBE":{"BOX","CYLI","EXTRUSION"},
        "CYLI":{"NCYLINDER"},"EXTRUSION":{"LOOP","NCYLINDER"},"LOOP":{"VERTEX"},
        "VERTEX":set(),"NCYLINDER":set(),"BOX":{"NCYLINDER"}}
    stack=[("SITE",None)]; named={}; holes=[]
    for line in script.splitlines():
        if not line or line.startswith("--"): continue
        if line.startswith("NEW "):
            words=line.split();kind=words[1];name=words[2] if len(words)>2 else None
            assert kind in allowed[stack[-1][0]],(kind,stack)
            parent=stack[-1][0]
            stack.append((kind,name))
            if name:
                assert name not in named
                named[name]=list(stack)
            if kind=="NCYLINDER": holes.append({"parent":parent,"attrs":{}})
        elif line=="END":
            assert len(stack)>1
            stack.pop()
        elif line.startswith("/"):
            assert line in named,f"Undefined model lookup: {line}"
            stack=list(named[line])
        elif stack[-1][0]=="NCYLINDER":
            k,*v=line.split();holes[-1]["attrs"][k]=" ".join(v)
    assert stack[-1]==("ZONE","/"+ZONE)
    assert len(holes)==12
    for idx,h in enumerate(holes):
        assert h["parent"] in {"EXTRUSION","CYLI"}
        assert h["attrs"]["NAPPFLAG"]=="2"
        assert h["attrs"]["ORI"]=="Y IS N AND Z IS U"
        assert float(h["attrs"]["DIAM"])==22
        pos=tuple(float(v) for v in h["attrs"]["POS"].split()[1::2])
        if idx<6:
            e,u=FASTENERS[idx]
            assert pos==(-e,u-(-75 if idx<4 else -470),8)
            assert float(h["attrs"]["HEIG"])==20
        else:
            assert pos==(0,0,0),"Washer bore must be coaxial in its rotated owner frame"
            assert float(h["attrs"]["HEIG"])==5
    ps=parse_primitives(script,EQ)
    assert len(ps)==36,len(ps)
    bounds=[extent(p) for p in ps]
    assert min(b[2] for b in bounds)>=-.001
    assert min(b[4] for b in bounds)==-550 and max(b[5] for b in bounds)==100
    for p in ps:
        assert p.get("heig",1)>0
        if p["kind"]=="EXTRUSION": assert area(p["vertices"])<-.001
    for tag,oldtag in (("TPS_R3_BEAM","TPS_R2_BEAM"),):
        extract=lambda s,t: re.search(r"NEW SCTN /"+t+r"\n(.*?)\nEND",s,re.S)[1]
        assert extract(script,tag)==extract(base,oldtag)
    brace=re.search(r"NEW SCTN /TPS_R3_BRACE\n(.*?)\nEND",script,re.S)[1]
    ends=[tuple(map(float,m)) for m in re.findall(r"(?m)^POS[SE] E ([\d.-]+) N ([\d.-]+) U ([\d.-]+)",brace)]
    assert len(ends)==2
    assert ends[0][1]-16>=60 and ends[1][2]<=-175
    assert all(abs(p[2]-zline(p[1]))<1e-5 for p in ends)
    for i,(e,u) in enumerate(FASTENERS,1):
        h,_=labelled(script,f"HEX_HEAD_{i}")
        sh,_=labelled(script,f"SHANK_{i}")
        w,wb=labelled(script,f"WASHER_{i}")
        assert len(h["vertices"])==6
        assert abs(max(v[1] for v in h["vertices"])-min(v[1] for v in h["vertices"])-30)<.0001
        assert (h["east"],h["up"])==(e,u)
        assert extent(sh)[2:4]==(0,19) and extent(w)[2:4]==(16,19) and extent(h)[2:4]==(19,31)
        assert w["kind"]=="CYLI" and "NEW NCYLINDER" in wb
    for joint in ("UPPER","LOWER"):
        plate,_=labelled(script,joint+"_GUSSET")
        poly=[(v[1],v[2]) for v in vertices3(plate)[::2]]
        assert extent(plate)[:2]==(0,8)
        for edge in ("TOP","BOTTOM"):
            p,_=labelled(script,joint+"_LAP_"+edge)
            assert all(inside((v[1],v[2]),poly) for v in vertices3(p)),(joint,edge)
            assert p["heig"]>75
        # Both corners of the cut end's connected leg are covered by the plate.
        end=ends[0 if joint=="LOWER" else 1]
        assert inside((end[1],end[2]),poly)
        assert inside((end[1]+50*S,end[2]-50*C),poly)
    return {"status":"STATIC_PASS_E3D_REVIEW_PENDING","sections":2,"positive_hardware_solids":36,
        "negative_bores":12,"hex_heads":6,"single_solid_washers":6,"weld_runs":13,
        "main_beam_unchanged":True,"brace_cut_end_clearance_to_wall_mm":ends[0][1]-16,
        "new_values":"Reference Values; no structural capacity or anchor design certification",
        "uncertainty":"R2 crescent-head cause unproven; R3 changes loop winding, washer construction and explicit ownership. Catalogue face contact still needs E3D review."}

def main():
    raw=BASE.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE_HASH
    base=raw.decode("ascii").replace("\r\n","\n")
    script=build_r3(base);checks=verify_r3(script,base)
    for path in (OUT,DEPLOY):
        if path.exists(): assert path.read_text(encoding="ascii")==script,"Existing R3 differs; preserve before replacing"
        else: path.write_text(script,encoding="ascii")
        verify_r3(path.read_text(encoding="ascii"),base)
    assert OUT.read_bytes()==DEPLOY.read_bytes()
    checks["sha256"]=hashlib.sha256(OUT.read_bytes()).hexdigest()
    checks["source_r2_sha256"]=BASE_HASH
    OUT.with_name("Typical_Pipe_Support_R3_checks.json").write_text(json.dumps(checks,indent=2)+"\n",encoding="ascii")
    print(json.dumps(checks,indent=2))

if __name__=="__main__":main()
