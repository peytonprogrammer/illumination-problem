"""Render only the two prescribed assemblies from the exact receipt."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

root=Path(__file__).parent
receipt=json.loads((root/'check.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(11,6.2))
colors=['#f1dfbe','#d6e5f4','#d9e9da']
for ax,fixture in zip(axes,receipt['fixtures'][:2]):
    for cells,color in zip(fixture['copy_cells'],colors):
        for x,y in cells: ax.add_patch(Rectangle((x,y),1,1,facecolor=color,edgecolor='none'))
    ax.add_patch(Polygon(fixture['vertices'],closed=True,fill=False,edgecolor='#263747',linewidth=2.2))
    for seam in fixture['seams']:
        ax.plot(*zip(*seam['segment']),color='#9c651b',lw=2,ls='--')
    ax.scatter(0,0,s=38,color='#2455a4',zorder=5)
    ax.annotate('S',(0,0),xytext=(10,-13),textcoords='offset points',weight='bold',color='#2455a4')
    if fixture['name']=='known22':
        ax.scatter(2,2,s=38,color='#7c3aed',zorder=5)
        ax.annotate('T',(2,2),xytext=(10,0),textcoords='offset points',weight='bold',color='#7c3aed')
        ax.set_xlim(-1.65,5.65)
        ax.set_title('Known assembly: 22 walls',loc='left',fontsize=13,weight='bold',pad=14)
    else:
        for x in fixture['mark_fibers']['b']:
            p=x['point'];ax.scatter(*p,s=90,facecolor='white',edgecolor='#7c3aed',lw=2,zorder=6)
        ax.scatter(-1,0,marker='X',s=95,color='#c12a34',zorder=7)
        ax.annotate('New reflex corner',(-1,0),xytext=(-3.6,-1.1),fontsize=10,color='#b91c1c',
                    arrowprops=dict(arrowstyle='->',color='#b91c1c',lw=1.2))
        ax.set_xlim(-4.65,2.65)
        ax.set_title('Shared endpoint: 24 walls',loc='left',fontsize=13,weight='bold',pad=14)
    ax.set_ylim(-3.5,3.5);ax.set_aspect('equal');ax.axis('off')
fig.suptitle('Sharing this endpoint adds two walls',x=.06,ha='left',fontsize=17,weight='bold')
fig.text(.06,.09,'Dashed lines: open seams. Purple rings: target copies left on the boundary.',fontsize=11,color='#46515f')
fig.text(.06,.045,'Both rooms use the same five-square base and three reflected copies.',fontsize=10,color='#46515f')
fig.subplots_adjust(left=.04,right=.98,top=.84,bottom=.15,wspace=.15)
fig.savefig(root/'comparison.png',dpi=180,facecolor='white')
fig.savefig(root/'comparison.svg',facecolor='white')
