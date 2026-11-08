"""Draw only the fixed checked geometry and prescribed path."""
import json
from pathlib import Path
from fractions import Fraction
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
root=Path(__file__).parent
data=json.loads((root/'check.json').read_text())
point=lambda p:tuple(float(Fraction(v)) for v in p)
V=list(map(point,data['vertices'])); S=point(data['source']); T=point(data['target']); path=list(map(point,data['connecting_path']['path']))
fig,axes=plt.subplots(1,2,figsize=(10,7),dpi=160)
fig.patch.set_facecolor('white')
for ax in axes:
    ax.add_patch(Polygon(V,closed=True,facecolor='#f2f5f8',edgecolor='#243746',linewidth=2,zorder=1))
    ax.plot([0,.1],[2,2],color='#16836d',linewidth=6,zorder=5)
    ax.plot([.8,1],[3,3],color='#16836d',linewidth=6,zorder=5)
    ax.scatter(*S,color='#2455a4',s=35,zorder=9);ax.scatter(*T,color='#2455a4',s=35,zorder=9)
    ax.annotate('S',S,xytext=(-15,-2),textcoords='offset points',fontsize=12,color='#2455a4')
    ax.annotate('T',T,xytext=(8,2),textcoords='offset points',fontsize=12,color='#2455a4')
    ax.set_aspect('equal');ax.set_xlim(-1.2,2.2);ax.set_ylim(-.2,4.35);ax.axis('off')
axes[0].set_title('Going upward without turning back fails',fontsize=12,pad=14)
axes[0].plot([.4,.6],[3,3],color='#c64d35',linewidth=8,zorder=7)
axes[0].annotate('Every first arrival:\nx between 0.4 and 0.6',xy=(.5,3),xytext=(-1.1,3.65),fontsize=10,color='#a83d28',arrowprops={'arrowstyle':'->','color':'#a83d28'})
axes[0].annotate('Second opening:\n0.8 < x < 1',xy=(.9,3),xytext=(1.25,2.45),fontsize=10,color='#126956',arrowprops={'arrowstyle':'->','color':'#126956'})
axes[0].annotate('First opening:\n0 < x < 0.1',xy=(.05,2),xytext=(-1.1,1.45),fontsize=10,color='#126956',arrowprops={'arrowstyle':'->','color':'#126956'})
axes[0].plot([S[0],.48],[S[1],3],color='#c64d35',linewidth=1.6,linestyle='--',zorder=4)
axes[0].text(.5,-.45,'All launch slopes and all side-bounce counts\nare covered by the interval proof.',ha='center',fontsize=10,color='#45515b')
axes[1].set_title('Turning back and retrying reaches T',fontsize=12,pad=14)
axes[1].plot([p[0] for p in path],[p[1] for p in path],color='#2455a4',linewidth=1.35,zorder=4)
axes[1].scatter([p[0] for p in path[1:-1]],[p[1] for p in path[1:-1]],s=12,color='#2455a4',zorder=8)
axes[1].annotate('Fourth upward approach\npasses through the opening',xy=(.88,3),xytext=(.65,4.1),fontsize=10,color='#2455a4',arrowprops={'arrowstyle':'->','color':'#2455a4'})
axes[1].text(.5,-.45,'One exact path: 10 legal reflections.\nThe room is lit; only the forward-only claim fails.',ha='center',fontsize=10,color='#45515b')
fig.suptitle('Two passages: a 12-wall obstruction to forward-only transport',fontsize=15,y=.98)
fig.subplots_adjust(left=.04,right=.97,top=.87,bottom=.13,wspace=.2)
fig.savefig(root/'two-passages.png',dpi=160,facecolor='white')
fig.savefig(root/'two-passages.svg',facecolor='white')
print(root/'two-passages.png')
