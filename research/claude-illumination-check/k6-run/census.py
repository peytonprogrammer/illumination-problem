"""Independent k6 support census. Necessary condition only: H = U ∪ R axis-connected with
|H \\ R| <= cap - b, where R = full cells ∪ axis neighbours, b = |R \\ F|. Brute-force Steiner check."""
from itertools import combinations
from collections import deque
import sys
W,K=21,int(sys.argv[1]) if len(sys.argv)>1 else 6
NB=((1,0),(-1,0),(0,1),(0,-1))
D4=[lambda x,y:(x,y),lambda x,y:(-y,x),lambda x,y:(-x,-y),lambda x,y:(y,-x),lambda x,y:(x,-y),lambda x,y:(-x,y),lambda x,y:(y,x),lambda x,y:(-y,-x)]
def norm(S):
    best=None
    for g in D4:
        T=[g(*p) for p in S]; mx=min(a for a,b in T); my=min(b for a,b in T)
        T=tuple(sorted((a-mx,b-my) for a,b in T)); best=T if best is None or T<best else best
    return best
def connected(cells):
    cells=set(cells); start=next(iter(cells)); seen={start}; Q=deque([start])
    while Q:
        a,b=Q.popleft()
        for dx,dy in NB:
            n=(a+dx,b+dy)
            if n in cells and n not in seen: seen.add(n); Q.append(n)
    return len(seen)==len(cells)
def feasible(F):
    I=len(F); cap=(W-4*I+2*K)//2; R=set(F)|{(a+dx,b+dy) for a,b in F for dx,dy in NB}; b=len(R-set(F))
    out=cap-b
    if out<0: return None
    if connected(R): return (b,out)
    cand=set(R)
    for _ in range(out): cand|={(a+dx,b2+dy) for a,b2 in cand for dx,dy in NB}
    cand=sorted(cand-R)
    for n in range(1,out+1):
        for S in combinations(cand,n):
            if connected(R|set(S)): return (b,out)
    return None
def pairs(F):
    P=[(p,q) for p,q in combinations(F,2) if abs(p[0]-q[0])+abs(p[1]-q[1])!=1]
    orb=set()
    for p,q in P:
        best=None
        for g in D4:
            T=[g(*c) for c in F]; mx=min(a for a,b in T); my=min(b for a,b in T)
            sh=lambda c:(g(*c)[0]-mx,g(*c)[1]-my)
            key=(tuple(sorted(sh(c) for c in F)),tuple(sorted((sh(p),sh(q)))))
            best=key if best is None or key<best else best
        orb.add(best)
    return len(P),len(orb)
res={}
for I,rad in ((2,16),(3,14)):
    shapes=set()
    pts=[(x,y) for x in range(-rad,rad+1) for y in range(-rad,rad+1) if abs(x)+abs(y)<=rad]
    if I==2:
        for p in pts:
            if p!=(0,0): shapes.add(norm([(0,0),p]))
    else:
        for p,q in combinations([p for p in pts if p!=(0,0)],2): shapes.add(norm([(0,0),p,q]))
    keep=[]
    for S in sorted(shapes):
        f=feasible(S)
        if f is None: continue
        rp,po=pairs(S)
        if rp==0: continue
        keep.append((S,f,rp,po))
    res[I]=keep
    print(f'I={I}: {len(keep)} supports, {sum(k[2] for k in keep)} raw pairs, {sum(k[3] for k in keep)} pair orbits; max extent',max(max(max(a,b) for a,b in k[0]) for k in keep),flush=True)
    for S,f,rp,po in keep: print('  ',S,'b=%d out=%d'%f,rp,po)
