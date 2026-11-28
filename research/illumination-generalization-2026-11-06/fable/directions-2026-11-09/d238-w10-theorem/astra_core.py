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

import ast
conditions={}
for swap,geom,imax in [(False,v,2),(True,h,5)]:
    w,u,x,z,a,d,b=geom
    L=add(d,b); D=add(a,L)
    for i,k,sign in product(range(-imax,imax+1),range(-13,14),[-1,1]):
        start=add(mul(sign,x),mul(2*k,w))
        E=area(start,L,swap)+area(add(z,mul(2*i,u)),a,swap)
        F=area(z,add(a,d),swap)+area(add(start,mul(-2*i,u)),b,swap)
        top=area(u,D,swap); edge=area(w,D,swap)
        name=f"miss_{int(swap)}_{i}_{k}_{sign}"
        conditions[name]=Z.Or(E<=-edge,E>=edge,F<=(0 if swap else -top),F>=top)
for line in open('astra_vectors.log'):
    if not line.startswith('sign '):continue
    _,axis,coords=line.split(maxsplit=2);vec=ast.literal_eval(coords)
    proj=[area(vec,terms((j,)),int(axis)) for j in range(4)]
    conditions['sign_'+axis+'_'+'_'.join(map(str,vec))]=Z.Or(Z.And(*(p>0 for p in proj)),Z.And(*(p<0 for p in proj)),Z.And(*(p==0 for p in proj)))
base=list(s.assertions())
for name,c in conditions.items():s.assert_and_track(c,name)
assert s.check()==Z.unsat
core=[str(t) for t in s.unsat_core()]
print('initial',len(core),flush=True)
def solver(names):
    q=Z.SolverFor('QF_LRA')
    q.add(*base,*(conditions[key] for key in names))
    return q
for key in core.copy():
    trial=[k for k in core if k!=key]
    if solver(trial).check()==Z.unsat:core=trial
print(core,flush=True)
open('astra_core.txt','w').write('\n'.join(core)+'\n')
q=solver(core); assert q.check()==Z.unsat
open('astra_core.smt2','w').write(q.to_smt2())
