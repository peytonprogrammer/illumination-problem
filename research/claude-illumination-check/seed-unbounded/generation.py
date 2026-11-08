"""Actual generation of pi1(T2 minus 4 points) by based seed loops (pure group theory, no room data).
F2=<r,u> is pi1 of the unit torus minus 0 at a tangential base point b near 0. K=ker(F2->(Z/2)^2) is
pi1 of T2=R^2/2Z^2 minus its four 2-torsion points. For each primitive w that isn't wall-parallel, the
up push is the straight path b -> b+2w and the down push passes the midpoint lattice point w on the other
side. Stallings folding decides whether the loops generate K: they do iff the folded graph is the
4-vertex covering graph. Run: python3 -B generation.py"""
from fractions import Fraction as Fr
from math import gcd
INV={'r':'R','R':'r','u':'U','U':'u'}
def seg(a,b):
    ev=[]
    for k in range(-60,61):
        for ax,lp,lm in ((0,'r','R'),(1,'u','U')):
            d=b[ax]-a[ax]
            if d:
                t=(k-a[ax])/Fr(d)
                if 0<t<1: ev.append((t,lp if d>0 else lm))
    ev.sort(); return [x for _,x in ev]
def reduce(w):
    out=[]
    for a in w:
        if out and out[-1]==INV[a]: out.pop()
        else: out.append(a)
    return out
def fold(words):
    edges=[]; n=1
    for wd in words:
        v=0
        for i,a in enumerate(wd):
            w=0 if i==len(wd)-1 else n
            if i<len(wd)-1: n+=1
            edges.append((v,a,w)); v=w
    par=list(range(n))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    changed=True
    while changed:
        changed=False; seen={}
        for v,a,w in edges:
            for x,b,y in ((f(v),a,f(w)),(f(w),INV[a],f(v))):
                if (x,b) in seen and f(seen[(x,b)])!=y:
                    p,q=f(seen[(x,b)]),y; par[max(p,q)]=min(p,q); changed=True
                else: seen[(x,b)]=y
    verts={f(x) for x in range(n)}; out={}
    for v,a,w in edges: out[(f(v),a)]=f(w); out[(f(w),INV[a])]=f(v)
    return len(verts),all((v,a) in out for v in verts for a in 'rRuU')
def loops(b,R2):
    ws=[]
    for p in range(-8,9):
        for q in range(-8,9):
            if gcd(p,q)!=1 or p*p+q*q>R2 or p==0 or q==0 or abs(p)==abs(q): continue
            end=(b[0]+2*p,b[1]+2*q); mid=(p-b[0],q-b[1])
            ws+=[reduce(seg(b,end)),reduce(seg(b,mid)+seg(mid,end))]
    return ws
assert fold([list('rr'),list('uu'),list('ruru'),list('ruuR'),list('urrU')])==(4,True)
assert fold([list('rr'),list('uu')])==(3,False)
for b in [(Fr(1,1000),Fr(1,997)),(Fr(1,997),Fr(1,1000)),(Fr(-1,1000),Fr(1,997)),(Fr(-3,1000),Fr(-2,997))]:
    for R2 in (5,10):
        ws=loops(b,R2); print('base',b,'|w|^2<=',R2,'loops',len(ws),'folded (vertices, covering)',fold(ws))
