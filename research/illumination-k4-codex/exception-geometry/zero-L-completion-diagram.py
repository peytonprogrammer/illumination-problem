"""Render the explicit four-reflection route in a permitted cap configuration."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import importlib.util
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('triangles',HERE.parent/'persisted-replay/audit.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
core=set().union(*(a.incident(p) for p in ((0,0),(2,0),(2,2))))
cap=lambda *v:tuple(sorted(v))
bottom=cap((0,-2),(0,-1),(1,-1))
room=core|{bottom,cap((4,2),(3,1),(3,2)),cap((2,-2),(1,-1),(2,-1)),cap((4,0),(3,-1),(3,0))}
record=json.loads((HERE/'zero-L-completion-check.json').read_text())['paths']['bottom_cap_four']
path=[tuple(F(*v) for v in p) for p in record['path']]
fig,ax=plt.subplots(figsize=(7.6,7),dpi=180)
for t in room:
 ax.add_patch(Polygon(t,facecolor='#edbd8b' if t==bottom else '#e8eef3',edgecolor='none'))
edges=Counter()
for t in room:
 u,v,w=t
 if a.cross(a.sub(v,u),a.sub(w,u))<0:v,w=w,v
 for p,q in ((u,v),(v,w),(w,u)):
  if edges[q,p]:edges[q,p]-=1
  else:edges[p,q]+=1
for (p,q),n in edges.items():
 if n:ax.plot((p[0],q[0]),(p[1],q[1]),color='#344b5d',lw=2,zorder=3)
ax.add_patch(Polygon(((1,3),(2,3),(2,4)),fill=False,edgecolor='#b87730',ls=(0,(4,3)),lw=1.5))
ax.text(1.3,3.75,'Top cap absent',ha='left',fontsize=11,color='#9c6229')
ax.plot([float(p[0]) for p in path],[float(p[1]) for p in path],color='#126ca5',lw=2.1,zorder=4)
ax.scatter([float(p[0]) for p in path[1:-1]],[float(p[1]) for p in path[1:-1]],s=28,color='#126ca5',zorder=5)
for i,(p,offset) in enumerate(zip(path[1:-1],((10,-17),(-19,0),(15,-3),(14,-14))),1):
 ax.annotate(str(i),tuple(map(float,p)),xytext=offset,textcoords='offset points',fontsize=11,color='#125a87',zorder=6)
for p,label,offset in ((path[0],'S',( -15,6)),(path[-1],'T',(10,-3))):
 ax.scatter(*map(float,p),color='#18384f',s=45,zorder=7)
 ax.annotate(label,tuple(map(float,p)),xytext=offset,textcoords='offset points',fontsize=14,color='#18384f')
ax.text(-.4,-1.9,'Bottom cap:\n3 reflections',ha='right',fontsize=11,color='#985d26')
for i in (0,3,4):
 p,q=path[i],path[i+1]
 start=tuple(float((2*p[k]+q[k])/3) for k in (0,1));end=tuple(float((p[k]+2*q[k])/3) for k in (0,1))
 ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle='->',color='#126ca5',lw=1.8),zorder=5)
ax.set_aspect('equal');ax.set_xlim(-1.8,4.4);ax.set_ylim(-2.5,4.35);ax.axis('off')
fig.suptitle('A missing top cap leaves a four-reflection connection',fontsize=15,y=.975)
fig.text(.5,.035,'Launch direction (1, -4): three cap reflections, then one top-wall reflection.',ha='center',fontsize=10.5)
fig.subplots_adjust(top=.92,bottom=.075,left=.025,right=.975)
fig.savefig(HERE/'zero-L-completion-diagram.png',facecolor='white')
fig.savefig(HERE/'zero-L-completion-diagram.svg',facecolor='white')
