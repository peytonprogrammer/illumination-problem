"""Draw only the prescribed paths in check.json; no tracing or discovery."""
from fractions import Fraction
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

root=Path(__file__).parent
data=json.loads((root/'check.json').read_text())
def points(raw): return [[float(Fraction(c)) for c in p] for p in raw]
fig,axes=plt.subplots(1,2,figsize=(10,5.3))
boundary=[(0,0),(2,0),(2,1),(1,1),(1,2),(0,2)]
S=(1.5,.5);T=(.5,1.5);V=(1,1)
for ax in axes:
    ax.add_patch(Polygon(boundary,closed=True,facecolor='#f2f4f7',edgecolor='#374151',lw=2))
    ax.scatter(*S,color='#1d4ed8',s=42,zorder=5)
    ax.scatter(*T,color='#7c3aed',s=42,zorder=5)
    ax.scatter(*V,marker='X',color='#111827',s=65,zorder=6)
    ax.annotate('S',S,xytext=(8,-12),textcoords='offset points',weight='bold',color='#1d4ed8')
    ax.annotate('T',T,xytext=(-15,9),textcoords='offset points',weight='bold',color='#7c3aed')
    ax.annotate('V',V,xytext=(8,8),textcoords='offset points',weight='bold')
    ax.set(xlim=(-.12,2.15),ylim=(-.12,2.15),aspect='equal',xticks=[0,1,2],yticks=[0,1,2])
    ax.spines[['top','right']].set_visible(False)
    ax.tick_params(length=0,labelcolor='#6b7280')
p=points(data['singular_family_controls'][1]['path'])
# This is the explicitly prescribed formal continuation after the corner.
i=p.index([1.,1.]);axes[0].plot(*zip(*p[:i+1]),color='#dc2626',lw=1.8)
axes[0].plot(*zip(*p[i:]),color='#dc2626',lw=1.8,ls='--')
axes[0].set_title('One corner blocks many attempts',loc='left',fontsize=12,weight='bold',pad=14)
axes[0].text(.02,-.17,'Example k=1: six smooth bounces, one corner hit.\nDashed line is formal continuation; a real ray stops at V.',transform=axes[0].transAxes,fontsize=9,color='#4b5563',va='top')
q=points(data['legal_path']);axes[1].plot(*zip(*q),color='#15803d',lw=2.2)
axes[1].plot([S[0],T[0]],[S[1],T[1]],color='#dc2626',lw=1.5,ls=':',alpha=.8)
axes[1].scatter(0,1.25,s=23,color='#15803d',zorder=5)
axes[1].set_title('A different itinerary reaches T',loc='left',fontsize=12,weight='bold',pad=14)
axes[1].text(.02,-.17,'Dotted direct path: length √2, hits V.\nGreen path: length √5, the shortest legal connection.',transform=axes[1].transAxes,fontsize=9,color='#4b5563',va='top')
fig.suptitle('A six-wall L-room with one reflex corner',x=.08,ha='left',fontsize=15,weight='bold')
fig.subplots_adjust(left=.08,right=.97,bottom=.22,top=.82,wspace=.28)
fig.savefig(root/'comparison.png',dpi=180,facecolor='white')
fig.savefig(root/'comparison.svg',facecolor='white')
