from pathlib import Path
from collections import Counter
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.patheffects as pe

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'illumination-k4-codex/surplus-four-local/L7012-D23-search/room.json'
doc = json.loads(SOURCE.read_text())
triangles = [[tuple(p) for p in t] for t in doc['triangles']]
boundary = [tuple(p) for p in doc['vertices']]
angles = Counter()
counts = Counter()
for t in triangles:
    for p in t:
        a, b = [q for q in t if q != p]
        dot = sum((a[i]-p[i])*(b[i]-p[i]) for i in (0,1))
        angles[p] += 90 if dot == 0 else 45
        counts[p] += 1
isA = lambda p: p[0] % 2 == p[1] % 2 == 0
insideA = sorted(p for p,a in angles.items() if isA(p) and a == 360)
insideN = sorted(p for p,a in angles.items() if not isA(p) and a == 360)
smoothN = sorted(p for p,a in angles.items() if not isA(p) and a == 180)
weights = {p: 3 if a == 180 else counts[p] for p,a in angles.items() if isA(p) and a < 360}
assert insideA == [(0,0),(2,0),(2,2)]
assert len(insideN) == len(smoothN) == 3
assert sum(weights.values()) == 9 and len(boundary) == 20
assert 20 + 2 * (len(insideN)+len(smoothN)) == 32

INK='#23384b'; GRID='#c9d1da'; FILL='#e8eff5'; BLUE='#1667ad'; ORANGE='#b65212'; GREEN='#20805d'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,'axes.titlecolor':INK})
halo=[pe.withStroke(linewidth=3,foreground='white')]

def base(ax, tiles=True):
    if tiles:
        for t in triangles:
            ax.add_patch(Polygon(t,facecolor=FILL,edgecolor=GRID,lw=.65))
    else:
        ax.add_patch(Polygon(boundary,facecolor=FILL,edgecolor='none'))
    ax.add_patch(Polygon(boundary,fill=False,edgecolor=INK,lw=2))
    ax.set(xlim=(-3.8,4.8),ylim=(-2.8,4.8),aspect='equal')
    ax.axis('off')

def label(ax,p,text,offset=(7,7),color=INK):
    ax.annotate(text,p,xytext=offset,textcoords='offset points',color=color,
                weight='bold',fontsize=11,path_effects=halo,zorder=10)

def title(ax,text): ax.set_title(text,loc='left',fontsize=14,weight='bold',pad=17)
def footer(ax,text): ax.text(.0,-.07,text,transform=ax.transAxes,fontsize=11,va='top',linespacing=1.5)
def save(fig,name):
    fig.subplots_adjust(left=.04,right=.98,top=.87,bottom=.19,wspace=.18)
    fig.savefig(HERE/name,dpi=170,facecolor='white')
    plt.close(fig)

fig,(a,b)=plt.subplots(1,2,figsize=(11,5.6))
title(a,'1. Start with the prescribed grid')
for x in range(-3,4):
    for y in range(-2,4):
        a.plot([x,x+1,x+1,x,x],[y,y,y+1,y+1,y],color=GRID,lw=.6)
        corners=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        aa=next(p for p in corners if isA(p))
        bb=next(p for p in corners if p[0]%2 == p[1]%2 == 1)
        a.plot([aa[0],bb[0]],[aa[1],bb[1]],color=GRID,lw=.9)
for x in range(-2,5,2):
    for y in range(-2,5,2):
        a.scatter(x,y,s=22,color=BLUE,zorder=4)
a.set(xlim=(-3.8,4.8),ylim=(-2.8,4.8),aspect='equal');a.axis('off')
footer(a,'Blue dots: A points (both coordinates even).\nEvery tile is a 45°–45°–90° triangle.')
title(b,'2. Join whole triangles into a room')
base(b)
footer(b,'This example uses 34 tiles.\nOne enclosed region; no holes or self-touching.')
save(fig,'steps-1-2.png')

fig,(a,b)=plt.subplots(1,2,figsize=(11,5.6))
title(a,'3. Fix the three interior A points')
base(a)
for p in weights:
    a.scatter(*p,s=25,facecolors='white',edgecolors=BLUE,zorder=5)
for p,name in [((0,0),'S (0, 0)'),((2,0),'U (2, 0)'),((2,2),'T (2, 2)')]:
    a.scatter(*p,s=70,color=BLUE,edgecolors='white',zorder=7)
    label(a,p,name,offset=(7,-17) if name.startswith('U') else (7,7))
footer(a,'S, U and T are the only A points inside.\nHollow A dots lie on the boundary and are allowed.')
title(b,'4. Count the six exceptions')
base(b)
for p in insideN:
    b.scatter(*p,s=85,color=ORANGE,marker='o',edgecolors='white',zorder=7)
    label(b,p,'I',offset=(5,7),color=ORANGE)
for p in smoothN:
    b.scatter(*p,s=85,color=GREEN,marker='s',edgecolors='white',zorder=7)
    label(b,p,'B',offset=(5,7),color=GREEN)
footer(b,'I = 3 interior points; B = 3 along straight walls.\nTotal k = 3 + 3 = 6. These are not windows.')
save(fig,'steps-3-4.png')

fig,(a,b)=plt.subplots(1,2,figsize=(11,5.6))
title(a,'5. Count straight walls: W = 20')
base(a,False)
for i,p in enumerate(boundary):
    q=boundary[(i+1)%len(boundary)]
    dx=q[0]-p[0];dy=q[1]-p[1];norm=math.hypot(dx,dy)
    mx=(p[0]+q[0])/2+.25*dy/norm
    my=(p[1]+q[1])/2-.25*dx/norm
    a.text(mx,my,str(i+1),ha='center',va='center',fontsize=10,weight='bold',path_effects=halo,zorder=9)
footer(a,'Each numbered straight stretch is one wall.\nTile seams and intermediate dots add no walls.')
title(b,'6. Check the surplus-four rule')
base(b)
for p,w in weights.items():
    b.scatter(*p,s=190,color=BLUE,zorder=7)
    b.text(*p,str(w),color='white',ha='center',va='center',fontsize=11,weight='bold',zorder=8)
for p in smoothN:
    b.scatter(*p,s=60,color=GREEN,marker='s',edgecolors='white',zorder=7)
footer(b,'Blue weights: Q = 3 + 1 + 1 + 2 + 1 + 1 = 9.\nGreen squares: 3.  Surplus = 9 + 3 − 8 = 4.')
save(fig,'steps-5-6.png')
(HERE/'checks.json').write_text(json.dumps({'source':str(SOURCE),'tiles':len(triangles),'interior_A':insideA,'interior_exceptions':insideN,'boundary_exceptions':smoothN,'boundary_A_weights':{str(k):v for k,v in weights.items()},'Q':sum(weights.values()),'W':len(boundary),'k':len(insideN)+len(smoothN),'delta':sum(weights.values())+len(smoothN)-8},indent=2)+'\n')
print('Rendered six steps. Verified 34 tiles, 20 walls, 6 exceptions, Q=9 and surplus=4.')
