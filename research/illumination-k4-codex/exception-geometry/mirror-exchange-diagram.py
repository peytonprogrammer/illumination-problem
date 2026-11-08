"""Draw the three explicitly proved blocker situations; no search or census."""
from pathlib import Path
from collections import Counter
import importlib.util
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tile_shapes',HERE.parent/'persisted-replay/audit.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
core=set().union(*(a.incident(p) for p in ((0,0),(2,0),(2,2))))
cap=lambda *p:tuple(sorted(p))
base=core|{
cap((-2,0),(-1,0),(-1,1)),cap((0,-2),(0,-1),(1,-1)),
cap((4,2),(3,2),(3,1)),cap((2,4),(2,3),(1,3))}
nb=cap((0,1),(0,2),(1,1));nr=cap((0,2),(1,1),(1,2))
fig,axes=plt.subplots(1,3,figsize=(12,4.9),dpi=180)
for ax,added,title,caption in zip(axes,({nb},{nr},{nb,nr}),
 ('First path blocked','Reflected path blocked','Both blockers present'),
 ('Reflected path survives','First path survives','Straight path opens')):
    for tri in base|added:
        ax.add_patch(Polygon(tri,facecolor='#edb981' if tri in added else '#e7edf2',edgecolor='none'))
    edges=Counter()
    for tri in base|added:
        u,v,w=tri
        if a.cross(a.sub(v,u),a.sub(w,u))<0:v,w=w,v
        for p,q in ((u,v),(v,w),(w,u)):
            if edges[q,p]:edges[q,p]-=1
            else:edges[p,q]+=1
    for (p,q),n in edges.items():
        if n:ax.plot((p[0],q[0]),(p[1],q[1]),color='#344a5e',lw=1.9,zorder=3)
    both=len(added)==2
    ax.plot((0,2),(0,2),color='#288568' if both else '#a4b0b9',lw=2 if both else 1.2,ls='-' if both else '--',zorder=4)
    ax.scatter([0,2],[0,2],color='#1e4663',s=25,zorder=5)
    ax.text(-.25,-.03,'S',ha='right',va='center',fontsize=11,color='#1e4663')
    ax.text(2.15,2.08,'T',fontsize=11,color='#1e4663')
    ax.scatter([1],[1],s=55,facecolor='#288568' if both else 'white',edgecolor='#288568' if both else '#aa602a',lw=1.7,zorder=6)
    ax.annotate('interior' if both else 'corner',(1,1),xytext=(13,-12),textcoords='offset points',fontsize=9,color='#207456' if both else '#925027',zorder=7)
    ax.set_title(title,fontsize=13,pad=11)
    ax.text(.5,-.045,caption,transform=ax.transAxes,ha='center',fontsize=11,color='#207456' if both else '#1e4663')
    ax.set_aspect('equal');ax.set_xlim(-2.35,4.35);ax.set_ylim(-2.25,4.25);ax.axis('off')
fig.suptitle('Blocking both routes opens a direct connection',fontsize=17,y=.98)
fig.text(.5,.035,'Exact boundary-charge equality is essential. Orange: the two possible blocking triangles.',ha='center',fontsize=11)
fig.subplots_adjust(top=.86,bottom=.13,wspace=.06,left=.015,right=.985)
fig.savefig(HERE/'mirror-exchange-diagram.png',facecolor='white')
fig.savefig(HERE/'mirror-exchange-diagram.svg',facecolor='white')
