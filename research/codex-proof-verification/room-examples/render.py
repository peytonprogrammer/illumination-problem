from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'illumination-k4-codex/surplus-four-local/L7012-D23-search'
INK, GRID = '#243547', '#a9b5c0'
LOWER, MIDDLE, UPPER = '#dceaf7', '#f8e6c9', '#deeee3'
RAY = '#c96520'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'text.color': INK, 'axes.titlecolor': INK})
fig, axes = plt.subplots(2, 2, figsize=(11.4, 9.2))
fig.patch.set_facecolor('white')

def endpoint(ax, p, label, color, delta=(0.10, 0.12)):
    ax.scatter(*p, s=45, color=color, zorder=6, edgecolors='white', linewidths=1)
    ax.annotate(label, p, xytext=(7, 6), textcoords='offset points',
                fontsize=12, weight='bold', color=INK, zorder=7)

def corridor(ax, title, d, g, hm, hp):
    for x,y,w,h,c in [(0,-hm,2*d,hm,LOWER), (d,0,2*d,g,MIDDLE),
                       (0,g,2*d,hp,UPPER)]:
        ax.add_patch(Rectangle((x,y),w,h,facecolor=c,edgecolor='none'))
    boundary = [(0,-hm),(2*d,-hm),(2*d,0),(3*d,0),(3*d,g),
                (2*d,g),(2*d,g+hp),(0,g+hp),(0,g),(d,g),(d,0),(0,0)]
    assert len(boundary) == 12
    ax.add_patch(Polygon(boundary, closed=True, fill=False, edgecolor=INK,
                         linewidth=2.3, joinstyle='miter'))
    for y in [0,g]:
        ax.plot([d,2*d],[y,y],color=GRID,linewidth=1.0,linestyle=(0,(4,4)))
    endpoint(ax,(.4*d,-.6*hm),'S','#34699b')
    endpoint(ax,(.4*d,g+.55*hp),'T','#32784f')
    ax.text(1.45*d,-.5*hm,'Lower',ha='center',va='center',fontsize=10)
    ax.text(2.20*d,.5*g,'Passage',ha='center',va='center',fontsize=10)
    ax.text(1.45*d,g+.5*hp,'Upper',ha='center',va='center',fontsize=10)
    ax.set_title(title+'\n'+f'Heights: {hm:g} / {g:g} / {hp:g}',
                 loc='left',fontsize=12,pad=16)
    ax.set_xlim(-.32*d,3.32*d)
    ax.set_ylim(-hm-.25,g+hp+.25)
    ax.set_aspect('equal'); ax.axis('off')

corridor(axes[0,0], 'A. Balanced corridor — 12 walls', 1,1,1,1)
corridor(axes[0,1], 'B. Tall corridor — 12 walls', 1,2,1.4,2.2)
corridor(axes[1,0], 'C. Wide, shallow corridor — 12 walls', 1.6,.6,.8,1.2)

doc=json.loads((SOURCE/'room.json').read_text())
triangles=[[tuple(p) for p in t] for t in doc['triangles']]
edges=Counter(); directed={}
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
for raw in triangles:
    t=raw if cross(*raw)>0 else [raw[0],raw[2],raw[1]]
    for a,b in zip(t,t[1:]+t[:1]):
        k=tuple(sorted((a,b)));edges[k]+=1;directed[k]=(a,b)
outer=[directed[k] for k,n in edges.items() if n==1]
nexts=defaultdict(list)
for a,b in outer:nexts[a].append(b)
assert all(len(v)==1 for v in nexts.values())
start=min(nexts); p=start; boundary=[]
while True:
    assert p not in boundary
    boundary.append(p);p=nexts[p][0]
    if p==start:break
assert len(boundary)==len(outer)
corners=[p for i,p in enumerate(boundary) if cross(boundary[i-1],p,boundary[(i+1)%len(boundary)])]
assert len(corners)==20 and len(triangles)==34
angle=Counter()
for t in triangles:
    for p in t:
        a,b=[q for q in t if q!=p]
        dot=(a[0]-p[0])*(b[0]-p[0])+(a[1]-p[1])*(b[1]-p[1])
        angle[p]+=90 if dot==0 else 45
A={p:v for p,v in angle.items() if p[0]%2==p[1]%2==0}
assert {p for p,v in A.items() if v==360}=={(0,0),(2,0),(2,2)}
nonA={p:v for p,v in angle.items() if p not in A}
J=sum(v==360 for v in nonA.values());smooth=sum(v==180 for v in nonA.values())
Q=sum(3 if v==180 else v//45 for v in A.values() if v!=360)
assert (J,smooth,Q,Q+smooth-8)==(3,3,9,4)
ax=axes[1,1]
for t in triangles:
    ax.add_patch(Polygon(t,closed=True,facecolor=LOWER,edgecolor=GRID,linewidth=.65))
ax.add_patch(Polygon(boundary,closed=True,fill=False,edgecolor=INK,linewidth=2.3))
cert=json.loads((SOURCE/'verification.json').read_text())
path=[tuple(Fraction(x) for x in p) for p in cert['path']]
assert path[0]==(0,0) and path[-1]==(2,2) and len(path)-2==4
xs,ys=zip(*path)
ax.plot([float(x) for x in xs],[float(y) for y in ys],color=RAY,lw=1.9,zorder=4)
ax.scatter([float(p[0]) for p in path[1:-1]],[float(p[1]) for p in path[1:-1]],
           s=20,color=RAY,zorder=5)
endpoint(ax,(0,0),'S','#34699b');endpoint(ax,(2,2),'T','#32784f')
endpoint(ax,(2,0),'U','#718096')
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-3.5,4.4);ax.set_ylim(-2.5,4.1)
ax.set_title('D. Triangle-tiled room — 20 walls\nActual example; orange path has 4 reflections',
             loc='left',fontsize=12,pad=16)

fig.suptitle('Examples covered by the two illumination results',fontsize=17,x=.06,ha='left',y=.985)
fig.text(.06,.025,'A–C: dashed seams are openings, not walls.  S = light source; T = target.\nD: faint lines show the triangle tiling; only the dark outer boundary is mirrored.',fontsize=11)
fig.subplots_adjust(left=.06,right=.97,top=.90,bottom=.10,wspace=.25,hspace=.30)
fig.savefig(HERE/'room-examples.png',dpi=180,facecolor='white')
fig.savefig(HERE/'room-examples.svg',facecolor='white')
(HERE/'geometry-check.json').write_text(json.dumps({'triangle_source':str(SOURCE/'room.json'),
    'tiles':len(triangles),'maximal_walls':len(corners),'J':J,'smooth_nonA':smooth,
    'Q':Q,'delta':Q+smooth-8,'transparent_exceptions':J+smooth,'displayed_reflections':4,
    'corridor_examples':[[1,1,1,1],[1,2,1.4,2.2],[1.6,.6,.8,1.2]]},indent=2)+'\n')
print('Saved room-examples.png; triangle geometry checks pass: 34 tiles, 20 walls, delta4, k6.')
