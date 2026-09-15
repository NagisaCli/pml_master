"""Draw output-backed review projections, not a simulated E3D rendering."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from build_review import OUT, EQ, parse_primitives, vertices3, extent, only, SN, CS

script=OUT.read_text(encoding="ascii")
ps=parse_primitives(script,EQ)
fig,axes=plt.subplots(1,3,figsize=(17,5),gridspec_kw={"width_ratios":[2.4,1.2,1]})
fig.suptitle("Typical Pipe Support R1 | Geometric review projections",fontsize=17)
fig.text(.5,.025,"Steel envelopes and TOAY face are provisional. This is not an E3D rendering or live clash clearance.",ha="center",fontsize=10,color="#9a4720")

def hull(points):
    pts=sorted(set(points))
    def turn(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    parts=[]
    for seq in (pts,pts[::-1]):
        half=[]
        for p in seq:
            while len(half)>=2 and turn(half[-2],half[-1],p)<=0: half.pop()
            half.append(p)
        parts.extend(half[:-1])
    return parts

for ax in axes[:2]:
    ax.add_patch(Rectangle((16,-150),1484,150,facecolor="#a4bacb",alpha=.35,edgecolor="#536f88",linestyle="--"))
    brace=[(16,-470),(1055,-185),(1055+50*SN,-185-50*CS),(16+50*SN,-470-50*CS)]
    ax.add_patch(Polygon(brace,facecolor="#a4bacb",alpha=.45,edgecolor="#536f88",linestyle="--"))
    for p in ps:
        if p["kind"]=="EXTRUSION":
            pts=hull([(v[1],v[2]) for v in vertices3(p)])
            color="#d48b37" if p["heig"] not in (8,12,3) else "#516f89"
            ax.add_patch(Polygon(pts,facecolor=color,edgecolor=color,linewidth=.4))
        else:
            b=extent(p)
            ax.add_patch(Rectangle((b[2],b[4]),b[3]-b[2],b[5]-b[4],facecolor="#687e93",edgecolor="#435368",linewidth=.5))
    ax.set_aspect("equal")
    ax.set_xlabel("N (mm)")
    ax.set_ylabel("U (mm)")
    ax.grid(alpha=.16)
axes[0].set(xlim=(-45,1560),ylim=(-595,140),title="Side view | 1500 mm reach from wall")
axes[1].set(xlim=(925,1180),ylim=(-310,-110),title="Upper lap | steel / plate / weld")
head=only(script,"HEX_HEAD_1")[0]
ax=axes[2]
for k in range(24):
    p=only(script,f"WASHER_1_{k:02d}")[0]
    ax.add_patch(Polygon([(v[0]+45,v[2]-60) for v in vertices3(p)[::2]],facecolor="#a7b9c7",edgecolor="none"))
ax.add_patch(Polygon([(v[0]+45,v[2]-60) for v in vertices3(head)[::2]],facecolor="#435f79",edgecolor="#172c41",linewidth=1.5))
ax.annotate("",xy=(22,-15),xytext=(22,15),arrowprops={"arrowstyle":"<->"})
ax.text(25,0,"AF 30",rotation=90,va="center")
ax.set(xlim=(-29,36),ylim=(-30,30),title="One of six hex heads\nAF30 / washer OD40: Reference Values")
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout(rect=(0,.07,1,.94))
fig.savefig(OUT.parent/"Typical_Pipe_Support_R1_review.png",dpi=160)
print(OUT.parent/"Typical_Pipe_Support_R1_review.png")
