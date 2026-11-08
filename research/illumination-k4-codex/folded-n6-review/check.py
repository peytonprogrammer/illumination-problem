"""Independent replay of the previously reported n6 full-star closure exclusion.
No peer code imported; exact integer ring order; no optical tracing.
"""
from pathlib import Path
from collections import defaultdict, Counter
from functools import cmp_to_key
from itertools import combinations
import hashlib,json
HERE=Path(__file__).resolve().parent
R=4
triangles=set(); roles={}
for i in range(-R,R+1):
    for j in range(-R,R+1):
        p=(6*i,6*j); q=(6*i+6,6*j); r=(6*i,6*j+6); s=(6*i+6,6*j+6)
        for eq in [(p,q,r),(q,r,s)]:
            center=tuple(sum(v[d] for v in eq)//3 for d in (0,1))
            roles[center]='B'
            for v,w in combinations(eq,2):
                midpoint=tuple((v[d]+w[d])//2 for d in (0,1)); roles[midpoint]='C'
                for a in (v,w):
                    roles[a]='A'; triangles.add(tuple(sorted((a,midpoint,center))))
triangles=sorted(triangles)
inc=defaultdict(list)
for i,t in enumerate(triangles):
    for p in t: inc[p].append(i)

def compare(u,v):
    # Physical vector is (u0+u1/2,sqrt(3)*u1/2); determinant sign is unchanged.
    def half(a): return 0 if a[1]>0 or (a[1]==0 and 2*a[0]+a[1]>=0) else 1
    if half(u)!=half(v): return half(u)-half(v)
    cross=u[0]*v[1]-u[1]*v[0]
    return -1 if cross>0 else 1 if cross<0 else 0
ring={}
for p,ts in inc.items():
    vectors={i:tuple(sum(v[d] for v in triangles[i])-3*p[d] for d in (0,1)) for i in ts}
    ring[p]=sorted(ts,key=cmp_to_key(lambda i,j:compare(vectors[i],vectors[j])))
fan_size={'A':12,'B':6,'C':4}
allowed={'A':set(range(1,13)),'B':{1,2,4,5},'C':{1,3}}
patterns={}
for p,ts in ring.items():
    if len(ts)!=fan_size[roles[p]]: continue
    k=len(ts); masks=set()
    for count in allowed[roles[p]]:
        for start in range(k): masks.add(sum(1<<((start+j)%k) for j in range(count)))
    patterns[p]=sorted(masks)

stats=Counter(); walls=Counter(); tile_counts=Counter(); leaf_hashes=[]

def leaf(used):
    stats['leaves']+=1; tile_counts[len(used)]+=1
    counts=Counter(p for i in used for p in triangles[i])
    full=[p for p,n in counts.items() if roles[p]=='A' and n==12]
    smooth=[p for p,n in counts.items() if roles[p]=='A' and n==6]
    stats['extra_full_A']+=len(full)-1; stats['smooth_A']+=len(smooth)
    # Every nonstraight, nonfull fan is one polygon corner.
    W=sum(n not in (fan_size[roles[p]],fan_size[roles[p]]//2) for p,n in counts.items())
    walls[W]+=1
    edges=Counter(tuple(sorted(e)) for i in used for e in combinations(triangles[i],2))
    adj=defaultdict(set)
    for (v,w),n in edges.items():
        if n==1: adj[v].add(w); adj[w].add(v)
    assert all(len(ns)==2 for ns in adj.values())
    todo=[next(iter(adj))]; seen=set()
    while todo:
        v=todo.pop()
        if v not in seen: seen.add(v); todo.extend(adj[v]-seen)
    assert len(seen)==len(adj)
    V=len(counts); E=len(edges); N=len(used)
    assert V-E+N==1
    assert 180*(W-2)==150*N+sum(30*n for p,n in counts.items() if roles[p]=='A' and n not in (6,12))
    leaf_hashes.append(hashlib.sha256(repr(sorted(triangles[i] for i in used)).encode()).hexdigest())

def visit(state):
    stats['nodes']+=1
    used=[i for i,x in state.items() if x]
    vertices=sorted({p for i in used for p in triangles[i]})
    best=None
    for p in vertices:
        ts=ring[p]
        if p not in patterns:
            stats['window_hits']+=1; return
        known=sum(1<<j for j,i in enumerate(ts) if i in state)
        ones=sum(1<<j for j,i in enumerate(ts) if state.get(i)==1)
        options=[mask for mask in patterns[p] if mask&known==ones]
        if not options: return
        if known==(1<<len(ts))-1: continue
        key=(len(options),p[0]*p[0]+p[0]*p[1]+p[1]*p[1],p)
        if best is None or key<best[0]: best=(key,ts,options)
    if best is None: leaf(used); return
    _,ts,options=best
    for mask in options:
        nxt=state.copy()
        for j,i in enumerate(ts): nxt[i]=(mask>>j)&1
        visit(nxt)

visit({i:1 for i in ring[(0,0)]})
print(json.dumps(dict(stats=stats, walls=walls, tiles=tile_counts)),flush=True)
assert stats['leaves']==416 and max(tile_counts)==24
assert stats['extra_full_A']==stats['smooth_A']==stats['window_hits']==0
assert min(walls)==18 and max(walls)==24
# Angle list and orientation parity, independent from closure replay.
raw=[(theta,k,kind) for theta in range(30,360,30) for k in range(2,13) for kind,total in [('smooth',180),('interior',360)] if theta!=180 and theta*k==total]
coherent=[item for item in raw if item[2]!='interior' or item[1]%2==0]
assert sorted({theta for theta,k,kind in coherent})==[30,60,90]
assert (120,3,'interior') in raw and (120,3,'interior') not in coherent
stats['window_hits']=stats['window_hits']
result=dict(status='PASS',method='independent exact replay of existing closure certificate',patch_radius=R,
    stats=dict(stats),wall_histogram=dict(sorted(walls.items())),tile_histogram=dict(sorted(tile_counts.items())),
    distinct_leaves=len(set(leaf_hashes)),leaf_set_digest=hashlib.sha256('\n'.join(sorted(leaf_hashes)).encode()).hexdigest(),
    arithmetic_transparent_cases=raw,coherent_transparent_cases=coherent)
(HERE/'check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
