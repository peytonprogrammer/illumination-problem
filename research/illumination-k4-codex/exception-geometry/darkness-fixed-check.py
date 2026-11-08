"""Check only the explicitly written L core and four prescribed cap triangles.
No geometry enumeration, solver, or ray discovery is implemented.
"""
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
CENTERS = ((0, 0), (2, 0), (2, 2))
CAPS = (
    ((0, -2), (0, -1), (1, -1)),
    ((4, 2), (3, 2), (3, 1)),
    ((2, 4), (2, 3), (1, 3)),
    ((-2, 0), (-1, 0), (-1, 1)),
)

def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def kind(p):
    return 'A' if p[0] % 2 == p[1] % 2 == 0 else 'B' if p[0] % 2 == p[1] % 2 == 1 else 'C'

def star(center):
    x, y = center
    sides = (((-1,-1),(0,-1),(1,-1)), ((1,-1),(1,0),(1,1)),
             ((1,1),(0,1),(-1,1)), ((-1,1),(-1,0),(-1,-1)))
    return [tuple(sorted((center, (x+a[0],y+a[1]), (x+b[0],y+b[1]))))
            for p,c,q in sides for a,b in ((p,c),(c,q))]

CORE = [tri for a in CENTERS for tri in star(a)]

def ledger(triangles):
    assert len(set(triangles)) == len(triangles)
    edges = Counter()
    incidents = Counter()
    for tri in triangles:
        assert {kind(v) for v in tri} == {'A','B','C'}
        assert abs(cross(*tri)) == 1
        a,b,c = tri
        if cross(a,b,c) < 0:
            b,c = c,b
        for u,v in ((a,b),(b,c),(c,a)):
            if edges[v,u]:
                edges[v,u] -= 1
            else:
                edges[u,v] += 1
        incidents.update(tri)
    boundary = [e for e,n in edges.items() if n]
    assert all(edges[e] == 1 for e in boundary)
    next_vertex = dict(boundary)
    assert len(next_vertex) == len(boundary)
    assert len({v for _,v in boundary}) == len(boundary)
    assert set(next_vertex) == {v for _,v in boundary}
    first = min(next_vertex)
    cycle = [first]
    while next_vertex[cycle[-1]] != first:
        assert next_vertex[cycle[-1]] not in cycle
        cycle.append(next_vertex[cycle[-1]])
    assert len(cycle) == len(boundary), 'extra boundary component'
    # Canonical triangles only meet along shared tiling edges or vertices;
    # a single boundary cycle with distinct vertices has no crossings/pinches.
    assert sum(cross((0,0),v,cycle[(i+1)%len(cycle)]) for i,v in enumerate(cycle)) == len(triangles)
    smooth = set()
    for i,v in enumerate(cycle):
        a,b = cycle[i-1],cycle[(i+1)%len(cycle)]
        if cross(a,v,b) == 0:
            assert (v[0]-a[0])*(b[0]-v[0])+(v[1]-a[1])*(b[1]-v[1]) > 0
            smooth.add(v)
    interior = set(incidents)-set(cycle)
    assert all(incidents[v] == (4 if kind(v)=='C' else 8) for v in interior)
    values = dict(N=len(triangles), W=len(cycle)-len(smooth),
                  I=sum(kind(v)=='A' for v in interior),
                  J=sum(kind(v)!='A' for v in interior),
                  s_A=sum(kind(v)=='A' for v in smooth),
                  s_N=sum(kind(v)!='A' for v in smooth))
    values['Q'] = sum(3 if v in smooth else incidents[v] for v in cycle if kind(v)=='A')
    values['k'] = values['J']+values['s_N']
    assert values['W'] == 2+6*values['I']+values['Q']-2*values['J']-values['s_N']
    assert values['N'] == 8*values['I']+values['Q']+values['s_A']
    values['interior_A'] = sorted(v for v in interior if kind(v)=='A')
    values['midpoint_B_fan_triangles'] = incidents[1,1]
    values['boundary_cycle'] = cycle
    return values

receipts = {
    'core': ledger(CORE),
    'two_forced_caps': ledger(CORE+[tuple(sorted(t)) for t in CAPS[:2]]),
    'four_cap_completion': ledger(CORE+[tuple(sorted(t)) for t in CAPS]),
}
expected = {'N':28, 'W':16, 'I':3, 'J':2, 's_A':0, 's_N':4, 'Q':4, 'k':6}
assert all(receipts['four_cap_completion'][k] == v for k,v in expected.items())
assert receipts['four_cap_completion']['midpoint_B_fan_triangles'] == 6
assert (0,2) not in {v for tri in CORE+[tuple(sorted(t)) for t in CAPS] for v in tri}
# Check the two prescribed reflection laws by exact rational arithmetic.
source, target = (F(0),F(0)), (F(2),F(2))
bottom, east = (F(1,2),F(-1)), (F(3),F(3,2))
sub = lambda a,b: (a[0]-b[0],a[1]-b[1])
v,w = sub(bottom,source),sub(target,bottom)
assert w == (3*v[0],-3*v[1])
v,w = sub(east,source),sub(target,east)
assert w == (-v[0]/3,v[1]/3)
# Explicit crossing points partition the legs among the three full squares.
paths = {
    'bottom': ((0,0),(F(1,2),-1),(1,0),(F(3,2),1),(2,2)),
    'east': ((0,0),(1,F(1,2)),(2,1),(3,F(3,2)),(2,2)),
}
# Each listed interval is in the specified full square by convexity.
for name,owners in (('bottom',(0,0,1,2)),('east',(0,1,2,2))):
    path=paths[name]
    for a,b,owner in zip(path,path[1:],owners):
        x,y=CENTERS[owner]
        assert all(x-1<=p[0]<=x+1 and y-1<=p[1]<=y+1 for p in (a,b))
receipts['fixed_paths'] = 'exact reflection laws and prescribed square-segment containment pass; smooth-contact implication proved in accompanying hand note'
receipts['scope'] = 'Three prescribed triangle unions only. No optical reachability assertion for the four-cap completion, no search, no solver.'
(HERE/'darkness-fixed-check.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps({k:{n:v for n,v in r.items() if n not in ('boundary_cycle','interior_A')} for k,r in receipts.items() if isinstance(r,dict)},indent=2))

if '--plot' in sys.argv:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon, Rectangle
    fig,ax=plt.subplots(figsize=(7,6),dpi=170)
    for x,y in CENTERS:
        ax.add_patch(Rectangle((x-1,y-1),2,2,facecolor='#e8edf1',edgecolor='#657483',linewidth=1.8))
    for tri in CAPS[:2]:
        ax.add_patch(Polygon(tri,facecolor='#f7d7bf',edgecolor='#b45b1b',linewidth=1.6,zorder=3))
    for path,color,label in (([source,bottom,target],'#1767a1','Bottom reflection'),
                             ([source,east,target],'#8b43a4','East reflection')):
        ax.plot([float(p[0]) for p in path],[float(p[1]) for p in path],color=color,lw=2,label=label,zorder=4)
        ax.scatter(float(path[1][0]),float(path[1][1]),color=color,s=40,zorder=5)
    for p,label,off in ((source,'S = (0, 0)',(-48,10)),(target,'T = (2, 2)',(-10,12))):
        ax.scatter(float(p[0]),float(p[1]),color='#172b3a',s=40,zorder=6)
        ax.annotate(label,tuple(map(float,p)),xytext=off,textcoords='offset points',fontsize=11)
    ax.text(1.9,-.15,'Third full star',ha='center',fontsize=10,color='#536474')
    ax.text(.35,-1.75,'Required cap 1',ha='left',fontsize=10,color='#8b4314')
    ax.text(3.45,2.25,'Required\ncap 2',ha='center',fontsize=10,color='#8b4314')
    ax.set_aspect('equal');ax.set_xlim(-1.8,4.4);ax.set_ylim(-2.25,3.6);ax.axis('off')
    ax.legend(loc='upper left',frameon=False,fontsize=10)
    fig.suptitle('Two routes that darkness must interrupt',fontsize=16,y=.98)
    fig.text(.5,.035,'Each path is valid when its orange cap triangle is absent.\nDarkness requires both orange triangles to be present.',ha='center',fontsize=11)
    fig.subplots_adjust(bottom=.12,top=.9,left=.03,right=.97)
    fig.savefig(HERE/'darkness-local-paths.png',facecolor='white')
    fig.savefig(HERE/'darkness-local-paths.svg',facecolor='white')
