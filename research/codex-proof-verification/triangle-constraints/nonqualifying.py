from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

HERE=Path(__file__).resolve().parent
INK='#23384b'; GRID='#c9d1da'; BLUE='#1667ad'; ORANGE='#b65212'; GREEN='#20805d'
isA=lambda x,y:x%2==y%2==0
interior=[(x,y) for x in range(1,6) for y in range(1,6) if x+y<6]
ia=[p for p in interior if isA(*p)]
jn=[p for p in interior if not isA(*p)]
sn=sorted({(x,y) for x in range(7) for y in range(7) if x+y<=6 and (x==0 or y==0 or x+y==6) and (x,y) not in [(0,0),(6,0),(0,6)] and not isA(x,y)})
assert ia==[(2,2)] and len(jn)==len(sn)==9
fig,ax=plt.subplots(figsize=(8,7.2))
plt.rcParams.update({'font.family':'DejaVu Sans'})
ax.add_patch(Polygon([(0,0),(6,0),(0,6)],facecolor='#eef2f6',edgecolor='none'))
for x in range(6):
    for y in range(6):
        corners=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        a=next(p for p in corners if isA(*p))
        b=next(p for p in corners if p[0]%2==p[1]%2==1)
        for p,q in list(zip(corners,corners[1:]+corners[:1]))+[(a,b)]:
            if sum(p)<=6 and sum(q)<=6:ax.plot([p[0],q[0]],[p[1],q[1]],color=GRID,lw=.8)
ax.add_patch(Polygon([(0,0),(6,0),(0,6)],fill=False,edgecolor=INK,lw=2.5))
ax.scatter(*zip(*jn),s=65,color=ORANGE,edgecolors='white',zorder=5,label='9 interior exceptions')
ax.scatter(*zip(*sn),s=65,color=GREEN,marker='s',edgecolors='white',zorder=5,label='9 straight-wall exceptions')
ax.scatter(2,2,s=160,color=BLUE,edgecolors='white',zorder=6,label='Only 1 interior A point')
ax.annotate('A (2, 2)',(2,2),xytext=(12,10),textcoords='offset points',color=BLUE,fontsize=13,weight='bold')
for p,offset in [((0,0),(-22,-23)),((6,0),(-12,-23)),((0,6),(-22,10))]:
    ax.annotate(str(p),p,xytext=offset,textcoords='offset points',fontsize=11,color=INK)
ax.set(xlim=(-.6,6.6),ylim=(-.6,6.6),aspect='equal');ax.axis('off')
fig.suptitle('A triangle-shaped room outside the theorem',x=.08,ha='left',fontsize=17,color=INK,weight='bold')
ax.legend(loc='upper right',frameon=False,fontsize=11,labelcolor=INK)
fig.text(.08,.04,'Same 45° triangle grid; ordinary mirrored boundary.\nFails: 1 interior A point instead of 3; 18 exceptions instead of at most 6.',fontsize=12,color=INK,linespacing=1.5)
fig.subplots_adjust(left=.07,right=.95,top=.89,bottom=.15)
fig.savefig(HERE/'nonqualifying.png',dpi=160,facecolor='white')
(HERE/'nonqualifying.json').write_text(json.dumps({'vertices':[[0,0],[6,0],[0,6]],'interior_A':ia,'interior_non_A':jn,'smooth_boundary_non_A':sn,'exceptions':len(jn)+len(sn),'walls':3},indent=2)+'\n')
print('Verified: one interior A point, 9 interior + 9 smooth boundary exceptions, three walls.')
