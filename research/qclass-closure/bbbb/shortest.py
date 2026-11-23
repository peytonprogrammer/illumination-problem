"""Intrinsic vertex distances on cov4181's marked ordered-pair component."""
from collections import defaultdict
from functools import cache
from heapq import heappop, heappush
from math import gcd, isqrt
from pathlib import Path
import sys

base = next(Path(__file__).resolve().parents[2].glob('illumination-generalization*/fable/directions*'))
sys.path.insert(0, str(base / 'd4-monodromy-blocks'))
from monodromy import Room

cells = {(x,y) for x,ys in enumerate([range(6), (2,3), (2,3), range(6), range(6), (2,3), (2,), range(3)]) for y in ys}
S,T = (2,3),(4,3)
room = Room('cov4181','square',cells,[])
edges = [room.sigma[axis,bit] for axis in ('V','H') for bit in (0,1)]
def vertex(face,x,y):
    tile,copy = room.faces[face]
    a,b = room.tiles[tile]['key']
    return (a+(a%2!=x), b+(b%2!=y))
def status(pt):
    x,y=pt
    return sum((x-i,y-j) in cells for i in (0,1) for j in (0,1))
def copies(pt,face):
    return room.faces[face][1] if status(pt)==4 else None
seed=next((f,g) for f in room.sheets for g in room.sheets
          if vertex(f,0,1)==S and vertex(g,0,1)==T)
faces=[seed]; index={seed:0};adj=[]
for f,g in faces:
    row=[]
    for e in edges:
        pair=e[f],e[g]
        if pair not in index:
            index[pair]=len(faces); faces.append(pair)
        row.append(index[pair])
    adj.append(row)
assert len(faces)==1176
ids={}; stars=[]; points=[]; starts=[]; targets=defaultdict(list); blocked=[]
for x in (0,1):
    for y in (0,1):
        for i in range(len(faces)):
            if (x,y,i) in ids: continue
            j=len(stars); star=[i]; ids[x,y,i]=j
            for h in star:
                for e in (x,2+y):
                    u=adj[h][e]
                    if (x,y,u) not in ids:
                        ids[x,y,u]=j;star.append(u)
            stars.append((x,y,star))
            f,g=faces[i];p,q=vertex(f,x,y),vertex(g,x,y)
            points.append((p,q))
            bad=tuple(v for v in (p,q) if status(v) in (1,3));blocked.append(bad)
            if (p,q)==(S,T):starts.append(j)
            if not bad and (g,f) in index and ids.get((x,y,index[g,f]))==j:
                assert p==q and copies(p,f)==copies(q,g) and len(star)==4
                targets[x,y].append(j)
assert [len(targets[key]) for key in ((0,1),(1,1),(1,0),(0,0))]==[7,14,0,7]

# Exact comparisons of finite sums of square roots. Distinct squarefree roots
# are linearly independent over Q. Refine integer enclosures only on close calls.
@cache
def radical(norm):
    for a in range(isqrt(norm),0,-1):
        if norm%(a*a)==0:return norm//(a*a),a

class Length(tuple):
    def plus(self,root,coef):
        d=dict(self);d[root]=d.get(root,0)+coef
        return Length(sorted(d.items()))
    def __lt__(self,other):
        if self==other:return False
        d=dict(self)
        for r,c in other:d[r]=d.get(r,0)-c
        scale=1024
        while True:
            lo=hi=0
            for r,c in d.items():
                l=isqrt(r*scale*scale);u=l+(l*l!=r*scale*scale)
                lo+=min(c*l,c*u);hi+=max(c*l,c*u)
            if hi<0:return True
            if lo>0:return False
            scale*=scale

R=12
bound=Length(((1,R),))
events=[]
for a in range(R+1):
    for b in range(R+1):
        if gcd(a,b)!=1 or a*a+b*b>R*R:continue
        crosses=sorted([(i*b,0,i%2) for i in range(1,a)]+[(j*a,1,j%2) for j in range(1,b)])
        events.append((a,b,radical(a*a+b*b),crosses))

dist={s:Length() for s in starts}; queue=[(Length(),s) for s in sorted(starts)]
first={s:set([None]) for s in starts}
while queue:
    d,j=heappop(queue)
    if d!=dist[j]:continue
    x,y,star=stars[j]
    for a,b,(root,coef),cross in events:
        cost=d.plus(root,coef)
        if bound<cost:continue
        for face in star:
            h=face
            for _,axis,odd in cross:
                h=adj[h][(2+(y^odd)) if axis else (x^odd)]
            dest=ids[x^(a%2),y^(b%2),h]
            flags={j if z is None and blocked[j] else z for z in first[j]}
            if dest not in dist or cost<dist[dest]:
                dist[dest]=cost;first[dest]=flags;heappush(queue,(cost,dest))
            elif cost==dist[dest]:
                first[dest].update(flags)
for key in [(1,1),(0,0)]:
    known=[j for j in targets[key] if j in dist]
    print('parity',key,'reached',len(known),'of',len(targets[key]),'within',R)
    for j in sorted(known,key=lambda j:(dist[j],j)):
        print(j,points[j][0],tuple(dist[j]),[(v,points[v],blocked[v]) if v is not None else None for v in sorted(first[j],key=lambda v:-1 if v is None else v)])

assert len(starts)==8
assert {j for j in targets[0,0] if None in first[j]} == set()
for parity,point in [((1,1),(7,1)),((0,0),(8,2))]:
    subset=[j for j in targets[parity] if points[j][0]==point]
    assert len(subset)==1
    assert all(v is not None and points[v][1]==(7,2) for v in first[subset[0]])
