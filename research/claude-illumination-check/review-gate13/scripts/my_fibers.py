# Check MY Section 3.1 origami: vertex classes over the 2x2 torus R^2/2Z^2.
# Squares sq(i,mu,nu), i in Z/q, mu,nu in Z/2. Lower-left corner of sq(i,mu,nu) lies over (mu,nu).
import sys
def run(q):
    S=[(i,m,n) for i in range(q) for m in range(2) for n in range(2)]
    def r(s):
        i,m,n=s
        if m==1: return (i,0,n)
        return ((i+1)%q,1,n) if n==0 else ((i-1)%q,1,n)
    def u(s):
        i,m,n=s
        if n==1: return (i,m,0)
        return ((i+1)%q,m,1) if m==1 else ((i-1)%q,m,1)
    rinv={r(s):s for s in S}; uinv={u(s):s for s in S}
    assert len(rinv)==len(S) and len(uinv)==len(S)
    c=lambda s:u(r(uinv[rinv[s]]))   # counterclockwise around lower-left vertex
    seen=set(); out={}
    for s in S:
        if s in seen: continue
        cyc=[s]; seen.add(s); t=c(s)
        while t!=s: cyc.append(t); seen.add(t); t=c(t)
        labels={(x[1],x[2]) for x in cyc}
        assert len(labels)==1
        out.setdefault(labels.pop(),[]).append(len(cyc))
    zeros=sum(L-1 for v in out.values() for L in v)
    g=(zeros+2)//2
    return out,g
for q in (3,5,7,9,11):
    out,g=run(q)
    print(q,{k:sorted(v) for k,v in sorted(out.items())},'genus',g,'(3q-1)/2=',(3*q-1)//2)
