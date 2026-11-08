import sys, time
from origami_dark import build, canon, inv, comp
V=[(0,0),(1,1),(2,1),(2,0),(3,1),(4,1),(4,0),(5,1),(5,2),(6,2),(5,3),(4,3),(4,4),(3,3),(3,2),(1,2),(1,3),(0,4),(0,3),(-1,3),(-1,2),(-2,2),(-1,1),(0,1)]
if len(sys.argv)>2 and sys.argv[2]=='R22':
    V=[(-1,-1),(-1,1),(0,1),(0,2),(1,2),(1,3),(3,3),(3,2),(4,2),(4,1),(5,1),(5,0),(3,0),(3,1),(1,1),(1,-1),(2,-1),(2,-3),(1,-3),(1,-2),(0,-2),(0,-1)]
    S,T=(0,0),(2,2)
else: S,T=(0,2),(4,2)
r,u,lab,s0=build(V,S,T); n=len(r); L0=['.']*n
def key(R,U):
    # cheap root filter: roots with minimal cycle-type signature of R at that square
    best=None
    for s in range(n):
        c=canon(R,U,L0,s)[:2]
        if best is None or c<best: best=c
    return best
st=key(tuple(r),tuple(u)); seen={st}; todo=[st]; lim=int(sys.argv[1]); t=time.time()
while todo:
    R,U=todo.pop(); Ri,Ui=inv(R),inv(U)
    for a,b in ((R,tuple(comp(U,Ri))),(tuple(comp(R,Ui)),U)):
        k=key(a,b)
        if k not in seen:
            seen.add(k); todo.append(k)
    if len(seen)>lim: print('>',lim); break
else: print('unrooted orbit',len(seen))
print(round(time.time()-t),'s squares',n)
