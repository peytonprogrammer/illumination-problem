from pathlib import Path
from fractions import Fraction
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
R=Path(__file__).resolve().parent
controls=json.loads((R/'check.json').read_text())['controls']
fig,axs=plt.subplots(1,2,figsize=(12,6),layout='constrained')
for ax,n,key,title in zip(axs,['row2101_fullH','row2110_Ecenter'],['seven','six'],['Seven reflections · right wall and roof','Six reflections · diagonal mirror']):
 g=controls[n];p=json.loads((R/(key+'-path.json')).read_text());P=[tuple(float(Fraction(q)) for q in v) for v in p['path']]
 ax.add_patch(Polygon(g['vertices'],facecolor='#f1f5f9',edgecolor='#334155',lw=2,zorder=2))
 ax.add_patch(Polygon([(-2,1),(-2,2),(-1,1)],facecolor='#c7d2fe',edgecolor='#6366f1',lw=1,zorder=3))
 if key=='six':ax.add_patch(Polygon([(3,3),(4,2),(3,2)],facecolor='#ffedd5',edgecolor='#ea580c',lw=1,zorder=3))
 for i,(a,b) in enumerate(zip(P,P[1:])):
  col='#2563eb' if i<5 else '#d97706';ax.plot([a[0],b[0]],[a[1],b[1]],color=col,lw=1.8,zorder=4)
  x=(a[0]+b[0])/2;y=(a[1]+b[1])/2
  ax.annotate('',xy=(x+.06*(b[0]-a[0]),y+.06*(b[1]-a[1])),xytext=(x,y),arrowprops={'arrowstyle':'->','color':col},zorder=5)
 for label,pt,c in [('S',(0,0),'#047857'),('T',(2,2),'#be123c')]:
  ax.scatter(*pt,color=c,s=60,edgecolors='white',zorder=6);ax.annotate(label,pt,xytext=(6,-14),textcoords='offset points',color=c,fontweight='bold')
 ax.set_title(title,loc='left',fontsize=12);ax.set_xlim(-3.3,4.4);ax.set_ylim(-2.3,4.3);ax.set_aspect('equal');ax.set_xticks(range(-3,5));ax.set_yticks(range(-2,5));ax.grid(alpha=.15);ax.spines[['top','right']].set_visible(False)
fig.suptitle('Same launch (5, −6), two verified connections',fontsize=17,fontweight='bold')
fig.savefig(R/'six-seven-paths.png',dpi=160,facecolor='white')
