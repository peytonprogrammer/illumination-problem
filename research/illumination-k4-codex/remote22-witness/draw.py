from pathlib import Path
from fractions import Fraction
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'check.json').read_text());V=json.loads((ROOT/'inputs/one-room-geometry.json').read_text())['vertices'];P=[tuple(float(Fraction(q)) for q in p) for p in d['path']]
fig,axs=plt.subplots(2,2,figsize=(12,10),layout='constrained')
blue='#2563eb';orange='#d97706';purple='#7c3aed'
for ax,title,start,end in zip(axs.flat,['Complete connection · 14 reflections','1–5 · Return through the left pocket','6–10 · Across the lower and upper chambers','11–14 · Return through the elbow, then reach T'],[0,0,5,10],[15,5,10,15]):
    ax.add_patch(Polygon(V,facecolor='#f1f5f9',edgecolor='#334155',linewidth=2,zorder=2))
    if start or end!=15:
        ax.plot(*zip(*P),color='#cbd5e1',lw=.8,zorder=3)
    for i in range(start,end):
        color=blue if i<5 else orange if i<10 else purple
        a,b=P[i:i+2];ax.plot([a[0],b[0]],[a[1],b[1]],color=color,lw=1.5,zorder=4)
        t=.55;x=a[0]+t*(b[0]-a[0]);y=a[1]+t*(b[1]-a[1]);ax.annotate('',xy=(x+.06*(b[0]-a[0]),y+.06*(b[1]-a[1])),xytext=(x,y),arrowprops={'arrowstyle':'->','color':color,'lw':1.4},zorder=5)
    if title.startswith('Complete'):
        ax.text(-2.8,3.3,'Launch direction (10, −13)',fontsize=10,color='#334155')
    else:
        for j in range(max(1,start+1),min(end,14)+1):
            x,y=P[j];ax.scatter([x],[y],s=17,color='#0f172a',zorder=6)
            dx,dy={2:(-20,-1),3:(7,0),4:(0,9),5:(-20,2),8:(-20,0),9:(0,8),10:(8,0),11:(-25,-10),12:(0,8),14:(8,0)}.get(j,(5,-15))
            ax.annotate(str(j),(x,y),xytext=(dx,dy),textcoords='offset points',fontsize=9,fontweight='bold',zorder=7)
    for name,p,offset,c in [('S',(0,0),(-18,8),'#047857'),('T',(2,2),(7,8),'#be123c')]:
        ax.scatter(*p,s=65,color=c,edgecolors='white',linewidths=1.3,zorder=8);ax.annotate(f'{name} {p}',p,xytext=offset,textcoords='offset points',fontsize=10,fontweight='bold',color=c,zorder=9)
    ax.set_title(title,loc='left',fontsize=11,pad=10);ax.set_aspect('equal');ax.set_xlim(-3.4,4.4);ax.set_ylim(-2.4,4.5);ax.set_xticks(range(-3,5));ax.set_yticks(range(-2,5));ax.grid(alpha=.14);ax.spines[['top','right']].set_visible(False);ax.tick_params(labelsize=8)
fig.suptitle('This 20-wall room is lit: an exact path from S to T',fontsize=17,fontweight='bold')
fig.savefig(ROOT/'verified-path.png',dpi=170,facecolor='white');fig.savefig(ROOT/'verified-path.svg',facecolor='white')
