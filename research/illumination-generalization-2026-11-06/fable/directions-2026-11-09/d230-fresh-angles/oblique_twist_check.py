import sys
from math import gcd
from itertools import product
def room(t):
    cols=[(0,1,2),(1,2,4),(2,4,3),(4,6,1),(6,8,4),(8,10,3),(10,11,2),(11,12,4),(12,12+t,1)]
    return {(i,j) for a,b,h in cols for i in range(a,b) for j in range(h)}
def build(cells):
    sq=[(c,ex,ey) for c in sorted(cells) for ex in (1,-1) for ey in (1,-1)]
    idx={s:k for k,s in enumerate(sq)}
    h=[0]*len(sq); v=[0]*len(sq)
    for k,((i,j),ex,ey) in enumerate(sq):
        n=(i+ex,j); h[k]=idx[(n,ex,ey)] if n in cells else idx[((i,j),-ex,ey)]
        n=(i,j+ey); v[k]=idx[(n,ex,ey)] if n in cells else idx[((i,j),ex,-ey)]
    return sq,idx,h,v
def base(s):
    (i,j),ex,ey=s; return (i+(ex<0), j+(ey<0))
def ptype(cells,p):
    x,y=p; n=sum(((x-a,y-b) in cells) for a in (0,1) for b in (0,1))
    return {4:'int',2:'wall',1:'convex',3:'reflex',0:'out'}[n]
def comp(f,g): return [f[g[s]] for s in range(len(g))]
def inv(f):
    r=[0]*len(f)
    for a,b in enumerate(f): r[b]=a
    return r
def shear(h,v,p,q):
    e1,e2=(1,0),(0,1)
    while (e1[0]+e2[0],e1[1]+e2[1])!=(p,q):
        m=(e1[0]+e2[0],e1[1]+e2[1])
        if m[0]*q-m[1]*p<0:   # target between e1 and m
            e2=m; v=comp(v,h)
        else:
            e1=m; h=comp(h,v)
    return h,v
def analyse(cells,S,T,p,q):
    sq,idx,h0,v0=build(cells)
    h,v=shear(h0,v0,p,q)
    N=len(sq); pi=comp(v,h); hi=inv(h)
    bad=[ptype(cells,base(s)) in('convex','reflex') for s in sq]
    cyc=[-1]*N; cycles=[]
    for s in range(N):
        if cyc[s]<0:
            c=[];u=s
            while cyc[u]<0: cyc[u]=len(cycles); c.append(u); u=pi[u]
            cycles.append(c)
    leafbad=[any(bad[u] for u in c) for c in cycles]
    par=list(range(len(cycles)))
    def f(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for ci,c in enumerate(cycles):
        # integer leaf between cycle(s) and cycle(h(s)) = bases of h(s_k)
        if not any(bad[h[u]] for u in c):
            for u in c: par[f(ci)]=f(cyc[h[u]])
    cyl={}
    for ci in range(len(cycles)): cyl.setdefault(f(ci),[]).append(ci)
    tp=1
    for g,m in cyl.items():
        cs={len(cycles[ci]) for ci in m}; assert len(cs)==1,cs
        c=cs.pop(); hh=len(m); k=c//gcd(c,hh); tp=tp*k//gcd(tp,k)
    def twist(s,sign):
        ci=cyc[s]
        # leaf through base(s): bases of h(u), u in cycle(hi[s])
        if any(bad[h[u]] for u in cycles[cyc[hi[s]]]): return None
        a=0;u=s
        while True:
            u=hi[u]; a+=1
            if any(bad[h[w]] for w in cycles[cyc[hi[u]]]) : break
            if a>N: return None
        c=len(cycles[cyc[s]]); k=(sign*tp*a)%c
        for _ in range(k): s=pi[s]
        return s
    lifts=lambda P:[idx[((P[0]-(ex<0),P[1]-(ey<0)),ex,ey)] for ex in(1,-1) for ey in(1,-1)]
    out=[]
    for sign in(1,-1):
        Si=[twist(s,sign) for s in lifts(S)]; Ti=[twist(s,sign) for s in lifts(T)]
        fmt=lambda L:[None if s is None else (base(sq[s]),sq[s][1],sq[s][2]) for s in L]
        out.append((fmt(Si),fmt(Ti)))
    return tp,len(cyl),out
if __name__=='__main__':
    S,T=(2,2),(8,2)
    for t in (3,7,13):
        cells=room(t)
        for d in [(1,1),(1,2),(2,1),(1,3),(3,1),(2,3),(3,2)]:
            tp,nc,out=analyse(cells,S,T,*d)
            Si,Ti=out[0]
            print(f"t={t} d={d} cyl={nc} twist={tp}\n   S-> {Si}\n   T-> {Ti}")
