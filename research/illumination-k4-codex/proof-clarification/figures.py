from pathlib import Path
import json,importlib.util
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon
ROOT=Path(__file__).resolve().parent
j=json.loads((ROOT/'check.json').read_text());P=j['base'];Q=j['packets'][0];R=j['packets'][1]
COLORS=['#f0d6ac','#bcd9ef','#bedfc8','#d8c5e8'];INK='#172b45';GREEN='#197b62';ORANGE='#bd6923';RED='#b43d3d';BLUE='#2466a1'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
def save(fig,name):
 fig.savefig(ROOT/(name+'.png'),dpi=200,bbox_inches='tight',facecolor='white');fig.savefig(ROOT/(name+'.svg'),bbox_inches='tight',facecolor='white');plt.close(fig)
def setup(ax,cells,pad=.4):
 xs=[p[0] for p in cells];ys=[p[1] for p in cells];ax.set_aspect('equal');ax.set_xlim(min(xs)-pad,max(xs)+1+pad);ax.set_ylim(min(ys)-pad,max(ys)+1+pad)
 ax.set_xticks(range(min(xs),max(xs)+2));ax.set_yticks(range(min(ys),max(ys)+2));ax.grid(color='#dce2e8',linewidth=.5,zorder=0);ax.tick_params(labelsize=9,length=0);ax.spines[['top','right','bottom','left']].set_visible(False)
def boundary(ax,vs,lw=2.2):
 w=vs+[vs[0]];ax.plot([p[0] for p in w],[p[1] for p in w],color=INK,lw=lw,zorder=4,solid_joinstyle='miter')
def mark(ax,p,label,color,offset=(6,7)):
 ax.scatter(*p,s=42,color=color,edgecolors='white',linewidths=.9,zorder=8);ax.annotate(label,p,xytext=offset,textcoords='offset points',color=color,fontsize=11,fontweight='bold',zorder=9)
def cells_image(g):
 sx,sy,dx,dy=g;return [(min(sx*x+dx,sx*(x+1)+dx),min(sy*y+dy,sy*(y+1)+dy)) for x,y in P['cells']]
def room(ax,packet,extra=False):
 setup(ax,packet['room']['cells'])
 for i,g in enumerate(packet['copy_maps']):
  for x,y in cells_image(g):ax.add_patch(Rectangle((x,y),1,1,fc=COLORS[i],ec='none',zorder=1))
 boundary(ax,packet['room']['vertices'])
 for item in packet['seams']:
  for e in item['edges']:ax.plot([z[0] for z in e],[z[1] for z in e],ls=(0,(5,3)),color=GREEN,lw=2,zorder=5)
 for item in packet['reversal_points']:ax.scatter(*item['physical'],s=44,fc='white',ec=ORANGE,lw=1.5,zorder=7)
 mark(ax,(0,0),'S',RED,(-16,-18));mark(ax,(2,2),'T',BLUE,(8,4))
 for i,g in enumerate(packet['copy_maps']):
  sx,sy,dx,dy=g;p=(sx*.5+dx,sy*(-1.5)+dy);ax.text(*p,'P'+str(i),color=INK,ha='center',va='center',fontweight='bold',fontsize=10,zorder=8)
 if extra:
  ax.annotate('actual corner',(-1,0),xytext=(-.6,1.8),fontsize=9,color=INK,arrowprops=dict(arrowstyle='-',color=INK,lw=.8),ha='center')
 ax.text(.01,-.08,'Solid outline: mirrors    Dashed lines: open seams',transform=ax.transAxes,fontsize=8.5,color=INK)
def base(ax):
 setup(ax,P['cells'])
 for x,y in P['cells']:ax.add_patch(Rectangle((x,y),1,1,fc='#e8edf3',ec='#bcc8d5',lw=.6,zorder=1))
 boundary(ax,P['vertices']);ax.scatter(*zip(*P['corners']),s=16,color=INK,zorder=6)
 mark(ax,(0,0),'a = (0,0)',RED,(6,11));mark(ax,(2,-2),'b = (2,-2)',BLUE,(10,-4))
 ax.text(.02,-.11,'Black dots are actual corners.',transform=ax.transAxes,fontsize=9,color=INK)
fig,ax=plt.subplots(figsize=(5.2,4.3));base(ax);save(fig,'base-panel')
fig,axs=plt.subplots(1,2,figsize=(9,4.3),gridspec_kw={'width_ratios':[1,1.7]});base(axs[0]);axs[0].set_title('Five-square base P',loc='left',color=INK,fontweight='bold');room(axs[1],Q);axs[1].set_title('Three reflected copies: 22 walls',loc='left',color=INK,fontweight='bold');fig.subplots_adjust(wspace=.48);save(fig,'room-panel')
fig,ax=plt.subplots(figsize=(8,5.3));room(ax,R,True);ax.set_title('Four reflected copies: 30 walls',loc='left',fontweight='bold',color=INK,pad=14);save(fig,'second-example')
# The parity picture is explicitly an arithmetic illustration, not a candidate path.
fig,ax=plt.subplots(figsize=(7,1.6));ax.set_xlim(-.2,8.8);ax.set_ylim(-.8,.9);ax.axis('off')
ax.annotate('',(8.4,0),(0,0),arrowprops=dict(arrowstyle='->',color=INK,lw=1.6))
for t,label,y,c in [(0,'a = (0,0)',-.34,RED),(1,'z = (1,-1)',.35,ORANGE),(2,'V/4 = (2,-2)',-.34,INK),(4,'V/2 = (4,-4)',.35,INK),(8,'V = (8,-8)',-.34,BLUE)]:
 ax.scatter(t,0,s=40,color=c,zorder=3);ax.text(t,y,label,ha='center',color=c,fontsize=10)
ax.text(4,.8,'Repeatedly halve an even-even unfolded endpoint',ha='center',color=INK,fontweight='bold')
ax.text(4,-.73,'Illustration only: the straight segment is the hypothetical unfolded path.',ha='center',fontsize=9,color='#5c6c7c');save(fig,'parity-panel')
def arrow(ax,p,q,color=INK,ls='-'):
 ax.annotate('',q,p,arrowprops=dict(arrowstyle='->',color=color,lw=2,linestyle=ls),zorder=8)
def local(ax,title):
 ax.set_xlim(-1.05,1.05);ax.set_ylim(-.95,.95);ax.set_aspect('equal');ax.axis('off');ax.set_title(title,color=INK,fontweight='bold',fontsize=11,pad=9)
fig,axs=plt.subplots(1,2,figsize=(8,2.1));local(axs[0],'In Q: pass through an open seam');local(axs[1],'After folding: reflect in a wall')
for x,y,c in [(-1,-1,COLORS[0]),(-1,0,COLORS[1])]:axs[0].add_patch(Rectangle((x,y),2,1,fc=c,ec='none'))
axs[0].plot([-1,1],[0,0],ls=(0,(5,3)),color=GREEN,lw=2);arrow(axs[0],(-.8,.6),(0,0));arrow(axs[0],(0,0),(.8,-.6));axs[0].text(.7,.6,'P1',color=INK);axs[0].text(-.85,-.7,'P0',color=INK)
axs[1].add_patch(Rectangle((-1,-1),2,1,fc='#e8edf3',ec='none'));axs[1].plot([-1,1],[0,0],color=INK,lw=2);arrow(axs[1],(-.8,-.6),(0,0));arrow(axs[1],(0,0),(.8,-.6));axs[1].text(.72,-.75,'P',color=INK)
fig.subplots_adjust(wspace=.22);save(fig,'fold-panel')
fig,axs=plt.subplots(1,2,figsize=(8,2.1));local(axs[0],'In Q: ordinary reflection at E');local(axs[1],'After folding: exact retracing')
axs[0].add_patch(Rectangle((-1,-1),1,1,fc=COLORS[0],ec='none'));axs[0].add_patch(Rectangle((-1,0),1,1,fc=COLORS[1],ec='none'));axs[0].plot([-1,0],[0,0],ls=(0,(5,3)),color=GREEN,lw=2);axs[0].plot([0,0],[-1,1],color=INK,lw=2)
arrow(axs[0],(-.8,.6),(0,0));arrow(axs[0],(0,0),(-.8,-.6));axs[0].text(-.92,.7,'P1',color=INK);axs[0].text(-.92,-.8,'P0',color=INK);axs[0].text(.08,.08,'E',color=ORANGE,fontweight='bold');axs[0].text(.15,-.2,'mirror',fontsize=9,color=INK,rotation=90)
axs[1].add_patch(Rectangle((-1,-1),1,1,fc='#e8edf3',ec='none'));axs[1].plot([-1,0],[0,0],color=INK,lw=2);axs[1].plot([0,0],[-1,0],color=INK,lw=2)
arrow(axs[1],(-.8,-.6),(0,0),BLUE);arrow(axs[1],(-.1,-.075),(-.8,-.6),RED,ls='--');axs[1].text(.12,-.35,'incoming',color=BLUE,fontsize=9);axs[1].text(.12,-.62,'retracing',color=RED,fontsize=9);axs[1].text(.08,.06,'corner of P',color=ORANGE,fontsize=9)
for ax in axs:ax.scatter(0,0,s=45,fc='white',ec=ORANGE,lw=1.5,zorder=10)
fig.subplots_adjust(wspace=.28);save(fig,'reversal-panel')
print('Six figure pairs generated.')
