"""Exact feasibility of a simultaneous miss on strict mask 761. No room enumeration."""
import sys
from itertools import product
import z3 as Z
rank='--rank' in sys.argv
s=Z.SolverFor('QF_NRA' if rank else 'QF_LRA')
s.set(timeout=60000)
xx=Z.Reals('x0 x1 x2 x3'); yy=Z.Reals('y0 y1 y2 y3')
if rank:
    s.add(*(q>0 for q in xx+yy),sum(xx[:3])==1,sum(yy[2:])==1)
    mat=[[a*b for b in yy] for a in xx]
else:
    mat=[[Z.Real('p%d%d'%(i,j)) for j in range(4)] for i in range(4)]
    s.add(*(v>0 for row in mat for v in row),sum(sum(row) for row in mat)==1)
# Transverse and axial distances are sums of positive elementary gaps.
def terms(indices):return tuple(int(i in indices) for i in range(4))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(c,a):return tuple(c*x for x in a)
def area(a,b,swap):
    if swap:a,b=b,a
    return sum(a[i]*b[j]*mat[i][j] for i,j in product(range(4),repeat=2) if a[i]*b[j])
v=tuple(map(terms,[(0,1),(0,1,2),(0,),range(4),(0,),(1,),(2,)]))
h=tuple(map(terms,[(2,3),(1,2,3),(3,),range(4),(3,),(2,),(1,)]))
w,u,x,z,a,d,b=v
s.add(area(w,b,0)>area(u,d,0),area(u,a,0)<area(u,add(b,d),0))
s.add(area(terms((3,)),b,0)<=area(terms((1,2)),b,0),
      area(terms((2,)),b,0)<=3*area(terms((1,)),b,0))
# Add central winding cases first. UNSAT at an early stage proves coverage.
for rad in [0,1,2,3,5,13]:
    for swap,geom,imax in [(False,v,2),(True,h,5)]:
        w,u,x,z,a,d,b=geom
        L=add(d,b);D=add(a,L)
        for i,k,sign in product(range(-min(rad,imax),min(rad,imax)+1),range(-rad,rad+1),[-1,1]):
            if rad and max(abs(i),abs(k))<=prev: continue
            start=add(mul(sign,x),mul(2*k,w))
            E=area(start,L,swap)+area(add(z,mul(2*i,u)),a,swap)
            F=area(z,add(a,d),swap)+area(add(start,mul(-2*i,u)),b,swap)
            top=area(u,D,swap); edge=area(w,D,swap)
            s.add(Z.Or(E<=-edge,E>=edge,F<=(0 if swap else -top),F>=top))
    result=s.check()
    print(rad,result,flush=True)
    if result==Z.unsat: break
    if result==Z.unknown: print(s.reason_unknown(),flush=True)
    if rank and result==Z.sat:print([s.model().eval(q) for q in xx+yy],flush=True)
    prev=rad
if '--cuts' in sys.argv and result==Z.sat:
    import math
    from fractions import Fraction
    def signs(v):
        return (v>0)-(v<0)
    def value(t):
        v=s.model().eval(t)
        return Fraction(v.numerator_as_long(),v.denominator_as_long())
    rays=[v for v in product(range(-2,3),repeat=4) if min(v)<0<max(v) and next(q for q in v if q)>0 and math.gcd(*v)==1]
    for iteration in range(200):
        m=[[value(t) for t in row] for row in mat]
        additions=0
        for trans in (0,1):
            for v in rays:
                # At rank one, v dotted with any two positive columns has identical sign.
                vals=[sum(v[i]*(m[j][i] if trans else m[i][j]) for i in range(4)) for j in range(4)]
                if len(set(map(signs,vals)))==1: continue
                print("sign",trans,v,flush=True)
                proj=[area(v,terms((j,)),trans) for j in range(4)]
                s.add(Z.Or(Z.And(*(q>0 for q in proj)),Z.And(*(q<0 for q in proj)),Z.And(*(q==0 for q in proj))))
                additions+=1
                if additions>=8:break
        result=s.check()
        print('cuts',iteration,additions,result,flush=True)
        if result!=Z.sat or not additions:break
