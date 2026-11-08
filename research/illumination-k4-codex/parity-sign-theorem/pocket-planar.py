"""Prescribed frozen-cell quotient checks. No ray, word, direction or orbit search."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict, Counter
from math import gcd
import hashlib, json
if not __debug__:
    raise RuntimeError('Run without -O')
B=Path(__file__).resolve().parent
D4=(((1,0),(0,1)),((0,-1),(1,0)),((-1,0),(0,-1)),((0,1),(-1,0)),
    ((1,0),(0,-1)),((-1,0),(0,1)),((0,1),(1,0)),((0,-1),(-1,0)))
def mul(g,h):
    return tuple(tuple(sum(g[i][k]*h[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def kind(p): return (p[0]&1)+(p[1]&1)
def inside(V,p):
    answer=False
    for a,b in zip(V,V[1:]+V[:1]):
        if (a[1]>p[1])!=(b[1]>p[1]) and p[0]<a[0]+F(p[1]-a[1],b[1]-a[1])*(b[0]-a[0]):
            answer=not answer
    return answer
class DSU:
    def __init__(self,n): self.p=list(range(n))
    def find(self,x):
        while x!=self.p[x]:
            self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def join(self,x,y): self.p[self.find(x)]=self.find(y)
def examine(room):
    V=list(map(tuple,room['vertices'])); tris=[]
    for x in range(min(p[0] for p in V),max(p[0] for p in V)):
        for y in range(min(p[1] for p in V),max(p[1] for p in V)):
            corners=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
            a=next(p for p in corners if kind(p)==0); b=next(p for p in corners if kind(p)==2)
            for c in (p for p in corners if kind(p)==1):
                if inside(V,(F(a[0]+b[0]+c[0],3),F(a[1]+b[1]+c[1],3))): tris.append((a,b,c))
    edges=defaultdict(list); angles=Counter()
    for i,t in enumerate(tris):
        for j,p in enumerate(t):
            angles[p]+=2 if j==2 else 1
            edges[frozenset((t[j],t[(j+1)%3]))].append(i)
    boundary={p for e,ts in edges.items() if len(ts)==1 for p in e}
    interior=set(angles)-boundary
    assert all(kind(p)==0 for p in interior)
    assert all(p in V or kind(p)==0 for p in boundary)
    assert all(angles[p]==8 for p in interior)
    ms=[angles[p] for p in V]
    assert all(1<=m<=7 and m!=4 for m in ms)
    assert sum(ms)==4*len(V)-8
    diagonal=[a[0]!=b[0] and a[1]!=b[1] for a,b in zip(V,V[1:]+V[:1])]
    assert any(diagonal) and not all(diagonal)
    runs=sum(diagonal[i] and not diagonal[i-1] for i in range(len(V)))
    odd=sum(m%2 for m in ms); fixed=sum(gcd(m,4) for m in ms)
    assert odd==2*runs
    quotient={}
    for name,H in [('X',(0,)),('halfturn',(0,2)),('quarterturn',(0,1,2,3))]:
        cosets={g:min(D4.index(mul(D4[h],g)) for h in H) for g in D4}
        labels=sorted(set(cosets.values())); lookup={q:j for j,q in enumerate(labels)}
        nc=len(labels); nt=len(tris); dsu=DSU(3*nt*nc); face_dsu=DSU(nt*nc)
        def vid(t,l,p): return 3*(t*nc+l)+tris[t].index(p)
        for e,ts in edges.items():
            a,b=sorted(e); dx,dy=b[0]-a[0],b[1]-a[1]
            R=((-1,0),(0,1)) if not dx else (((1,0),(0,-1)) if not dy else (((0,1),(1,0)) if dx*dy>0 else ((0,-1),(-1,0))))
            for ti in ts:
                for li,gi in enumerate(labels):
                    tj=ts[1-ts.index(ti)] if len(ts)==2 else ti
                    lj=li if len(ts)==2 else lookup[cosets[mul(D4[gi],R)]]
                    for p in e: dsu.join(vid(ti,li,p),vid(tj,lj,p))
                    face_dsu.join(ti*nc+li,tj*nc+lj)
        vertices=len({dsu.find(x) for x in range(3*nt*nc)})
        faces=nt*nc; assert faces%2==0
        edge_count=3*faces//2; chi=vertices-edge_count+faces
        assert len({face_dsu.find(x) for x in range(nt*nc)})==1
        assert chi%2==0 and chi<=2
        quotient[name]={'faces':faces,'edges':edge_count,'vertices':vertices,'genus':1-chi//2}
        if name=='X':
            roots={dsu.find(x) for x in range(3*nt*nc)}; jmap={}
            for ti,t in enumerate(tris):
                for li,gi in enumerate(labels):
                    lj=lookup[D4.index(mul(D4[2],D4[gi]))]
                    for p in t:
                        root=dsu.find(vid(ti,li,p)); dest=dsu.find(vid(ti,lj,p))
                        assert root not in jmap or jmap[root]==dest
                        jmap[root]=dest
            actual_fixed=sum(jmap[x]==x for x in roots)
            assert actual_fixed==fixed
    gX=1+sum(m-gcd(m,4) for m in ms)//2
    assert quotient['X']['genus']==gX
    assert quotient['halfturn']['genus']==runs-1
    assert quotient['quarterturn']['genus']==0
    assert 2*gX-2==4*(runs-1)-4+fixed
    parts={name:[] for name in ('A','B','C')}
    for p,m in angles.items():
        if p in boundary:
            degree=m//2 if kind(p)==1 else m
            parts[('A','C','B')[kind(p)]].append(degree)
        else: parts['A'].extend([4,4])
    for part in parts.values(): assert sum(part)==len(tris)
    assert sum(d-1 for part in parts.values() for d in part)==2*len(tris)-2
    assert all(d in (1,3) for d in parts['C'])
    angle_counts=Counter(ms)
    K=angle_counts[1]+5*angle_counts[5]+7*angle_counts[7]
    cover_bound={'source_genus':gX,'mark_fiber_degree_lower_bound':16,
        'forced_genus_two_when_source_genus_at_most_32':gX<=32,
        'genus_two_corner_fiber_degree_lower_bound':16+K,
        'genus_two_RH_degree_upper_bound':gX-1,
        'genus_two_unique_zero_fiber_degree_upper_bound':angle_counts[3]+2*angle_counts[6],
        'has_required_225_degree_corner_for_literal_pocket':angle_counts[5]>0,
        'nonperiodic_blocked_fiber_case_excluded_by_counts':gX<=32 and 16+K>angle_counts[3]+2*angle_counts[6],
        'scope':'Necessary cover-degree inequalities only, conditional on the nonperiodic all-to-all blocked-fiber alternative. Does not exclude periodic marked pairs.'}
    return {'tag':room['tag'],'walls':len(V),'triangles':len(tris),'interior_A':len(interior),
        'nonperiodic_cover_degree_bounds':cover_bound,
        'angle_units':ms,'diagonal_runs':runs,'odd_angle_corners':odd,'halfturn_fixed_points':fixed,
        'quotients':quotient,'sphere_branch_partitions':{k:sorted(v) for k,v in parts.items()},
        'nonreal_A_preimages':2*len(interior),'all_B_C_preimages_real':True}
selection=json.loads((B/'inputs/holdouts/selection.json').read_text())
paths=[B/'inputs/holdouts'/f"{e['tag']}.json" for e in selection]
results=[examine(json.loads(p.read_text())) for p in paths]
out={'status':'EXACT_FROZEN_PLANAR_QUOTIENT_CHECKS_PASS','frozen_rooms':len(results),
    'scope':'Independent canonical triangulation and vertex identifications; no optical tracing, orbit enumeration or candidate discovery.',
    'rooms':results,'input_sha256':{str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(B/'pocket-planar.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'frozen_rooms':len(results),'control':results[0],
    'halfturn_genera':dict(Counter(r['quotients']['halfturn']['genus'] for r in results)),
    'nonperiodic_cover_count_exclusions':sum(r['nonperiodic_cover_degree_bounds']['nonperiodic_blocked_fiber_case_excluded_by_counts'] for r in results)},indent=2))
