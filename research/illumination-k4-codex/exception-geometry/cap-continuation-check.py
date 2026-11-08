"""Replay one saved witness and verify its explicitly derived cap formulas.
No ray tracing, direction/word enumeration, solving or room discovery.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('exact_saved_path_checker', HERE.parent/'persisted-replay/audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
raw = json.loads((HERE/'cap-continuation-witness.json').read_text())
source = Path(raw['source_file'])
assert hashlib.sha256(source.read_bytes()).hexdigest() == raw['source_sha256']
with source.open() as f:
    line = next(v for i,v in enumerate(f,1) if i == raw['source_line'])
assert json.loads(line) == raw['record']
original = raw['record']
original_check = audit.check_record(original, tuple(original['q']), False)
path = tuple((-F(*p[1]), F(*p[0])) for p in original['path'])
centers = ((0,0),(2,0),(2,2))
caps = (
    ((0,-2),(0,-1),(1,-1)), ((4,2),(3,2),(3,1)),
    ((2,4),(2,3),(1,3)), ((-2,0),(-1,0),(-1,1)),
)
core = frozenset().union(*(audit.incident(tuple(map(F,p))) for p in centers))
cap_sets = [tuple(sorted(t)) for t in caps]
room = core | frozenset(cap_sets)
assert len(room) == 28 and path[0] == (0,0) and path[-1] == (2,2)
need, forbidden = audit.path_requirements(path)
assert need <= room and not forbidden & room
assert need-core == {cap_sets[1],cap_sets[3]}
assert not forbidden & {cap_sets[0],cap_sets[2]}

# A separate validation using the actual 16 maximal boundary walls:
# every bounce is strictly inside one wall, and every open leg is interior.
ledger = json.loads((HERE/'darkness-fixed-check.json').read_text())['four_cap_completion']
cycle = list(map(tuple, ledger['boundary_cycle']))
cross = audit.cross
sub = audit.sub
corners = [p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
walls = list(zip(corners,corners[1:]+corners[:1]))
assert len(walls) == 16

def on_segment(p,u,v):
    return cross(sub(p,u),sub(v,u)) == 0 and all(min(u[k],v[k])<=p[k]<=max(u[k],v[k]) for k in (0,1))

def inside(p):
    assert not any(on_segment(p,u,v) for u,v in walls)
    hits = 0
    for u,v in walls:
        if (u[1]>p[1]) != (v[1]>p[1]):
            x = F(u[0])+F(p[1]-u[1],v[1]-u[1])*(v[0]-u[0])
            if x > p[0]: hits += 1
    return bool(hits % 2)

bounce_walls=[]
for prev,p,nxt in zip(path,path[1:],path[2:]):
    found=[(u,v) for u,v in walls if on_segment(p,u,v) and p not in (u,v)]
    assert len(found)==1
    u,v=found[0]
    d,e,t=sub(p,prev),sub(nxt,p),sub(v,u)
    reflected=tuple(2*audit.dot(d,t)*t[k]-audit.dot(t,t)*d[k] for k in (0,1))
    assert cross(reflected,e)==0 and audit.dot(reflected,e)>0
    bounce_walls.append((u,v))
for p,q in zip(path,path[1:]):
    d=sub(q,p)
    assert inside(tuple((p[k]+q[k])/2 for k in (0,1)))
    for u,v in walls:
        e=sub(v,u);den=cross(d,e)
        if den:
            t=F(cross(sub(u,p),e),den)
            s=F(cross(sub(u,p),d),den)
            assert not (0<t<1 and 0<=s<=1), ('open leg touches boundary',p,q,u,v)
        elif cross(sub(u,p),d)==0:
            k=0 if d[0] else 1
            lo,hi=sorted((F(u[k]-p[k],d[k]),F(v[k]-p[k],d[k])))
            assert max(lo,F(0))>=min(hi,F(1)), 'leg overlaps wall'
assert inside(path[0]) and inside(path[-1])

# These are exact formulas derived by hand for the same ten-wall word.
def family(r):
    return ((F(0),F(0)),(-r,F(-1)),(-3*r,F(1)),(-4*r,F(0)),
            (-6*r/(1+r),(2-4*r)/(1+r)),(F(3),2-9*r),
            (12-3/r,F(-1)),(F(-1),13*r-4),
            ((14*r-2)/(1-r),(16*r-4)/(1-r)),(18*r-2,F(2)),
            ((22*r-2)/(1+r),(20*r-4)/(1+r)),(F(2),20*r-4))
assert family(F(3,10)) == path
# Single supplied ray only: general interval validity is the hand proof.
r=F(3,10)
h_left=4-1/r
left_exit=1-r*(1+h_left)
h_east=17*r-5
east_exit=h_east+2*r
assert F(5,17)<r<F(4,13)
assert h_left==F(2,3) and left_exit==F(1,2)
assert h_east==F(1,10) and east_exit==F(7,10)
assert 20*r-4==2
encode=lambda p:[[v.numerator,v.denominator] for v in map(F,p)]
receipt = dict(status='PASS',reflections=len(path)-2,
    original_guard_check=original_check,source_file=str(source),
    source_line=raw['source_line'],source_sha256=raw['source_sha256'],
    path=[encode(p) for p in path], actual_maximal_walls=len(walls),
    smooth_integer_bounces=[encode(p) for p in path[1:-1] if all(v.denominator==1 for v in p)],
    used_cap_indices=[1,3],unused_optional_cap_indices=[0,2],
    required_triangles=len(need),forbidden_triangles=len(forbidden),
    forbidden=[list(map(list,t)) for t in sorted(forbidden)],
    required=[list(map(list,t)) for t in sorted(need)],
    bounce_walls=[[list(u),list(v)] for u,v in bounce_walls],
    cap_maps=dict(left_entry=str(h_left),left_exit=str(left_exit),
                  east_entry=str(h_east),east_exit=str(east_exit)),
    interval=['5/17','4/13'],target_height_interval=['32/17','28/13'],
    scope='One existing witness in one fixed room, exact two-method verification; interval and cap-map generalizations proved by hand in cap-continuation.txt. No search or global shortestness claim.')
(HERE/'cap-continuation-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ('path','required','forbidden','bounce_walls')},indent=2))
if '--plot' in sys.argv:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    fig,ax=plt.subplots(figsize=(9,8),dpi=170)
    ax.add_patch(Polygon(cycle,facecolor='#edf1f5',edgecolor='none'))
    for i in (1,3):
        ax.add_patch(Polygon(caps[i],facecolor='#f5d2b3',edgecolor='none'))
    ax.add_patch(Polygon(cycle,fill=False,edgecolor='#263c4e',linewidth=2.3,zorder=4))
    xx=[float(p[0]) for p in path]; yy=[float(p[1]) for p in path]
    ax.plot(xx,yy,color='#126fa6',lw=1.9,zorder=3)
    ax.scatter(xx[1:-1],yy[1:-1],color='#126fa6',s=24,zorder=5)
    offsets=[(2,-20),(-6,12),(-12,12),(-30,3),(13,-1),(0,-22),(18,-6),(-4,-21),(8,9),(18,-1)]
    for i,(p,off) in enumerate(zip(path[1:-1],offsets),1):
        ax.annotate(str(i),tuple(map(float,p)),xytext=off,textcoords='offset points',ha='center',va='center',fontsize=10,color='#0a5787',bbox=dict(facecolor='white',edgecolor='none',pad=1.2),zorder=6)
    for p,label,off in ((path[0],'S = (0, 0)',(15,9)),(path[-1],'T = (2, 2)',(-5,18))):
        ax.scatter(float(p[0]),float(p[1]),color='#152d3e',s=50,zorder=7)
        ax.annotate(label,tuple(map(float,p)),xytext=off,textcoords='offset points',fontsize=12,color='#152d3e')
    ax.text(-2.25,.6,'Left cap:\n2 reflections',ha='right',fontsize=11,color='#8c4b1e')
    ax.text(4.1,1.4,'East cap:\n3 reflections',ha='left',fontsize=11,color='#8c4b1e')
    ax.text(.45,-1.85,'Unused cap',ha='center',fontsize=10,color='#67727d')
    ax.text(1.4,3.6,'Unused cap',ha='right',fontsize=10,color='#67727d')
    for i in (0,3,6,9):
        p,q=path[i],path[i+1]
        a=tuple(float((2*p[k]+q[k])/3) for k in (0,1))
        b=tuple(float((p[k]+2*q[k])/3) for k in (0,1))
        ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',color='#126fa6',lw=1.7),zorder=4)
    ax.set_aspect('equal');ax.set_xlim(-3.45,5.35);ax.set_ylim(-2.2,4.3);ax.axis('off')
    fig.suptitle('A verified path through the 16-wall room',fontsize=17,y=.98)
    fig.text(.5,.055,'Launch direction: (-3, -10).  Numbered dots: 10 legal reflections.',ha='center',fontsize=11)
    fig.text(.5,.025,'Orange triangles redirect the ray; it reaches T without hitting a corner.',ha='center',fontsize=11)
    fig.subplots_adjust(top=.93,bottom=.09,left=.015,right=.985)
    fig.savefig(HERE/'cap-continuation-path.png',facecolor='white')
    fig.savefig(HERE/'cap-continuation-path.svg',facecolor='white')
