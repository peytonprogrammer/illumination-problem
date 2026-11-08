"""Exact geometry of three prescribed assemblies; no placement or ray search."""
from pathlib import Path
from collections import defaultdict
from itertools import combinations
import json

ROOT=Path(__file__).parent
B={(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3)}
a=(0,0); b=(2,-2)

def sub(x,y): return x[0]-y[0],x[1]-y[1]
def cross(x,y): return x[0]*y[1]-x[1]*y[0]
def canon(p,q): return tuple(sorted((p,q)))
def edges(cells):
    out=set()
    for x,y in cells:
        corners=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        for p,q in zip(corners,corners[1:]+corners[:1]):
            if (q,p) in out: out.remove((q,p))
            else: out.add((p,q))
    return out

def boundary(cells):
    ee=edges(cells); outgoing=defaultdict(list); incoming=defaultdict(list)
    for p,q in ee: outgoing[p].append(q); incoming[q].append(p)
    assert set(outgoing)==set(incoming)
    assert all(len(outgoing[p])==len(incoming[p])==1 for p in outgoing),'pinch/branch'
    start=min(outgoing); current=start; path=[]; used=set()
    while True:
        path.append(current); nxt=outgoing[current][0]
        assert (current,nxt) not in used
        used.add((current,nxt)); current=nxt
        if current==start: break
    assert used==ee,'multiple boundaries/hole'
    verts=[p for i,p in enumerate(path) if cross(sub(p,path[i-1]),sub(path[(i+1)%len(path)],p))]
    turns=[cross(sub(p,verts[i-1]),sub(verts[(i+1)%len(verts)],p)) for i,p in enumerate(verts)]
    assert all(turns) and sum(t>0 for t in turns)-sum(t<0 for t in turns)==4
    area2=sum(cross(p,q) for p,q in zip(verts,verts[1:]+verts[:1]))
    assert area2==2*len(cells)
    return {'vertices':verts,'walls':len(verts),'reflex':sum(t<0 for t in turns),
            'area':len(cells),'unit_edges':ee,'unit_vertices':set(outgoing),
            'reflex_set':{p for p,t in zip(verts,turns) if t<0},
            'convex_set':{p for p,t in zip(verts,turns) if t>0}}

def g(point,t):
    sx,sy,tx,ty=t
    return sx*point[0]+tx,sy*point[1]+ty

def inv(point,t):
    sx,sy,tx,ty=t
    return sx*(point[0]-tx),sy*(point[1]-ty)

def transform(cells,t):
    out=set()
    for x,y in cells:
        pp=[g(p,t) for p in [(x,y),(x+1,y),(x+1,y+1),(x,y+1)]]
        out.add((min(p[0] for p in pp),min(p[1] for p in pp)))
    return out

def point_class(p,cells):
    x,y=p
    occ={(dx,dy) for dx,dy in [(-1,-1),(0,-1),(-1,0),(0,0)] if (x+dx,y+dy) in cells}
    if len(occ)==4: return 'interior'
    if len(occ)==3: return 'reflex'
    if len(occ)==1: return 'convex'
    if len(occ)==2:
        p,q=occ
        assert p[0]==q[0] or p[1]==q[1],'point pinch'
        return 'smooth_boundary'
    assert not occ
    return 'outside'

base=boundary(B)
assert (base['walls'],base['reflex'],base['area'])==(10,3,5)
base_walls={canon(p,q) for p,q in zip(base['vertices'],base['vertices'][1:]+base['vertices'][:1])}
all_base_points={(x+dx,y+dy) for x,y in B for dx in (0,1) for dy in (0,1)}
noncorners=all_base_points-set(base['vertices'])
assert noncorners=={a,b} and all(x%2==y%2==0 for x,y in noncorners)
assert all(abs(p[0]-q[0])+abs(p[1]-q[1])<=2 for p,q in base_walls)

fixtures=[('known22',[(1,1,0,0),(1,-1,0,0),(-1,-1,4,0)],22,0,0,2),
          ('shared24',[(1,1,0,0),(1,-1,0,0),(-1,-1,-2,0)],24,1,0,2),
          ('fourfold28',[(1,1,0,0),(1,-1,0,0),(-1,-1,-2,0),(-1,1,-2,0)],28,0,1,4)]
results=[]
for name,transforms,W,t3want,t4want,Ewant in fixtures:
    copies=[transform(B,t) for t in transforms]
    assert all(not(copies[i]&copies[j]) for i,j in combinations(range(len(copies)),2))
    union=set().union(*copies); info=boundary(union); local=[boundary(c) for c in copies]
    assert info['walls']==W
    seams=[]
    for i,j in combinations(range(len(copies)),2):
        shared={canon(p,q) for p,q in local[i]['unit_edges']} & {canon(p,q) for p,q in local[j]['unit_edges']}
        # Exact point-contact fold agreement, plus all unit seam endpoints.
        common_points=local[i]['unit_vertices']&local[j]['unit_vertices']
        assert all(inv(p,transforms[i])==inv(p,transforms[j]) for p in common_points)
        if not shared: continue
        adj=defaultdict(set)
        for p,q in shared: adj[p].add(q); adj[q].add(p)
        remaining=set(adj)
        while remaining:
            start=min(remaining); stack=[start]; component=set()
            while stack:
                p=stack.pop()
                if p in component: continue
                component.add(p); stack.extend(adj[p]-component)
            remaining-=component
            endpoints=[p for p in component if len(adj[p])==1]
            assert len(endpoints)==2
            seg=canon(*endpoints)
            for h in (i,j):
                walls={canon(g(p,transforms[h]),g(q,transforms[h])) for p,q in base_walls}
                assert seg in walls,'partial seam'
            p,q=seg; vertical=p[0]==q[0]
            ti,tj=transforms[i],transforms[j]
            if vertical:
                assert tj==(-ti[0],ti[1],2*p[0]-ti[2],ti[3])
            else:
                assert p[1]==q[1]
                assert tj==(ti[0],-ti[1],ti[2],2*p[1]-ti[3])
            seams.append({'copies':(i,j),'segment':seg})
    assert len(seams)==Ewant
    incidence=defaultdict(list)
    for i,t in enumerate(transforms):
        for p in base['vertices']:
            incidence[g(p,t)].append((i,'reflex' if p in base['reflex_set'] else 'convex',p))
    counts={k:0 for k in (1,2,3,4)}; new_reflex=[]; inherited=[]
    for p,entries in incidence.items():
        if any(e[1]=='reflex' for e in entries):
            assert len(entries)==1 and point_class(p,union)=='reflex'
            inherited.append(p)
        else:
            k=len(entries); assert k in counts
            counts[k]+=1
            assert point_class(p,union)=={1:'convex',2:'smooth_boundary',3:'reflex',4:'interior'}[k]
            if k==3: new_reflex.append(p)
    m=len(copies); t1,t2,t3,t4=[counts[k] for k in (1,2,3,4)]
    assert (t3,t4)==(t3want,t4want)
    assert info['reflex']==m*base['reflex']+t3
    assert W==m*(base['walls']-4)+4+2*t3
    assert t2+2*t3+2*t4==2*m-2
    assert 2*len(seams)==t2+2*t3+4*t4
    assert len(seams)==m-1+t4
    mark_fibers={key:[{'point':p,'class':point_class(p,union)} for p in sorted({g(mark,t) for t in transforms})]
                 for key,mark in [('a',a),('b',b)]}
    if name=='known22':
        assert point_class((0,0),union)==point_class((2,2),union)=='interior'
    elif name=='shared24':
        assert new_reflex==[(-1,0)]
        assert {x['point'] for x in mark_fibers['b']}=={(2,-2),(2,2),(-4,2)}
        assert all(x['class']=='smooth_boundary' for x in mark_fibers['b'])
    results.append({'name':name,'transforms':transforms,'cells':sorted(union),
                    'copy_cells':[sorted(c) for c in copies],
                    'vertices':info['vertices'],'walls':W,'reflex':info['reflex'],'area':info['area'],
                    'seams':seams,'convex_junction_counts':counts,'new_reflex':new_reflex,
                    'inherited_reflex':inherited,'mark_fibers':mark_fibers,
                    'cycle_rank':len(seams)-m+1})
# Marked base walls have disjoint endpoint sets; their isometric images cannot
# supply a shared-endpoint pair of marked full seams in the central copy.
def on_segment(p,v,w):
    return cross(sub(p,v),sub(w,v))==0 and all(min(v[k],w[k])<=p[k]<=max(v[k],w[k]) for k in (0,1))
marked_walls=[]
for mark in (a,b):
    ww=[wall for wall in base_walls if on_segment(mark,*wall)]
    assert len(ww)==1 and mark not in ww[0]
    marked_walls.append(ww[0])
assert set(marked_walls[0]).isdisjoint(marked_walls[1])
# Fixed affine mismatch of the proposed partial-overlap operation. This is
# an algebraic control only, not a generated room or a ray test.
from fractions import Fraction as Q
shift=Q(1,2)
partial_control=[]
for x in (Q(0),Q(1,2)):
    assert Q(-1,2)<x<Q(1)
    lower=(x,Q(0)); upper=(x-shift,Q(0))
    assert lower!=upper and sub(upper,lower)==(-shift,Q(0))
    partial_control.append({'point':str(x),'lower_image':str(x),'upper_image':str(x-shift)})
result={'status':'PASS','scope':'Three analytically prescribed assemblies; no placement/ray/word discovery. General bound is a same-agent hand argument, not independently reviewed.',
        'base':{'walls':10,'reflex':3,'cells':sorted(B),'vertices':base['vertices'],
                'marked_walls':marked_walls},'fixtures':results,'partial_overlap_fold_mismatch':partial_control}
(ROOT/'peer-replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','fixtures':[{k:r[k] for k in ('name','walls','reflex','area','cycle_rank','new_reflex')} for r in results],
                  'receipt':str(ROOT/'peer-replay.json')},indent=2))
