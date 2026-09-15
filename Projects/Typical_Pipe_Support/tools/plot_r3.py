"""Review projections from emitted geometry; steel is a nominal envelope."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle,Circle
from rebuild_r3 import BASE,OUT,EQ,parse_primitives,vertices3,extent,labelled,zline,S,C

def hull(points):
    pts=sorted(set(points)); result=[]
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    for seq in (pts,pts[::-1]):
        half=[]
        for p in seq:
            while len(half)>1 and cross(half[-2],half[-1],p)<=0:half.pop()
            half.append(p)
        result.extend(half[:-1])
    return result

script=OUT.read_text(encoding="ascii")
fig,axs=plt.subplots(2,2,figsize=(13,8),gridspec_kw={"height_ratios":[1,1],"width_ratios":[1.9,1]})
for ax,s,eq,start,end,title in ((axs[0,0],BASE.read_text(encoding="ascii"),"TPS_R2_HARDWARE",16,1055,"R2 | prior plate outlines"),(axs[1,0],script,EQ,80,1080,"R3 | tapered nodes, ends contained in lap regions")):
    ax.add_patch(Rectangle((16,-150),1484,150,facecolor="#aac4d6",edgecolor="#59788c",alpha=.45))
    ax.add_patch(Polygon([(start,zline(start)),(end,zline(end)),(end+50*S,zline(end)-50*C),(start+50*S,zline(start)-50*C)],facecolor="#91b1c9",alpha=.8))
    ps=parse_primitives(s,eq)
    # Plates first; welds last. Steel web material through the plate is not
    # inferred from the overlapping 2D projection.
    for p in ps:
        if p["kind"]=="EXTRUSION":
            poly=hull([(v[1],v[2]) for v in vertices3(p)])
            color="#ad8e77" if p["heig"] in (8,16) else ("#d79330" if p["heig"]>35 else "#536577")
            ax.add_patch(Polygon(poly,facecolor=color,edgecolor="#4e5962",linewidth=.25))
        else:
            b=extent(p)
            ax.add_patch(Rectangle((b[2],b[4]),b[3]-b[2],b[5]-b[4],facecolor="#9d8776" if p["kind"]=="BOX" else "#536577"))
    ax.set(xlim=(-40,1540),ylim=(-575,125),title=title,xlabel="N (mm)",ylabel="U (mm)")
    ax.set_aspect("equal");ax.grid(alpha=.14)
ax=axs[0,1]
for tag,col in (("LOWER_GUSSET","#b59880"),("UPPER_GUSSET","#9cafba")):
    p,_=labelled(script,tag)
    points=[(v[1],v[2]) for v in vertices3(p)[::2]]
    if tag=="LOWER_GUSSET": ax.add_patch(Polygon(points,facecolor=col,edgecolor="#4e5962"))
ax.plot([80,200],[zline(80),zline(200)],color="#266188",linewidth=3,label="Angle upper edge")
ax.plot([80+50*S,200+50*S],[zline(80)-50*C,zline(200)-50*C],color="#266188",linewidth=3)
ax.set(xlim=(0,220),ylim=(-545,-385),title="R3 lower node | 64 mm wall stand-off",xlabel="N (mm)",ylabel="U (mm)")
ax.set_aspect("equal");ax.grid(alpha=.14)
ax=axs[1,1]
ax.add_patch(Circle((0,0),20,facecolor="#b7c3cc",edgecolor="#566574"))
ax.add_patch(Circle((0,0),11,facecolor="white",edgecolor="#566574"))
p,_=labelled(script,"HEX_HEAD_1")
ax.add_patch(Polygon([(v[0]+45,v[2]-60) for v in vertices3(p)[::2]],facecolor="#526e86",edgecolor="#1f354b",linewidth=1.8))
ax.set(xlim=(-29,29),ylim=(-29,29),title="R3 screw | six solid flats + one bored washer")
ax.set_aspect("equal");ax.axis("off")
fig.suptitle("Pipe support reconstruction | output-backed geometry review",fontsize=16)
fig.text(.5,.015,"Reference dimensions. Nominal steel envelopes. Not an E3D rendering or structural approval.",ha="center",color="#965422",fontsize=10)
fig.tight_layout(rect=(0,.035,1,.95))
fig.savefig(OUT.with_name("Typical_Pipe_Support_R3_review.png"),dpi=155)
print(OUT.with_name("Typical_Pipe_Support_R3_review.png"))
