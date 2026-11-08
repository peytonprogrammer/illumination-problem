"""Exact test: do the event functionals positively span the annihilator of the symmetries on the closure subspace?
Equivalent to: no deformation outside the affine symmetries keeps every event's first-order sign condition."""
import json,sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
R=sys.argv[1];d=json.load(open(R if R.endswith('.json') else f'funcs-R{R}.json'))
F=[[Fr(x) for x in f] for f in d['funcs']];C=[[Fr(x) for x in c] for c in d['clos']]
n=len(F[0])
# basis of closure subspace (null space of C), exact
def nullspace(M,n):
 M=[r[:] for r in M];piv=[];rk=0
 for c in range(n):
  p=next((i for i in range(rk,len(M)) if M[i][c]!=0),None)
  if p is None:continue
  M[rk],M[p]=M[p],M[rk];M[rk]=[x/M[rk][c] for x in M[rk]]
  for i in range(len(M)):
   if i!=rk and M[i][c]!=0:f=M[i][c];M[i]=[x-f*y for x,y in zip(M[i],M[rk])]
  piv.append(c);rk+=1
 free=[c for c in range(n) if c not in piv];basis=[]
 for fc in free:
  v=[Fr(0)]*n;v[fc]=Fr(1)
  for r,pc in enumerate(piv):v[pc]=-M[r][fc]
  basis.append(v)
 return basis
Bz=nullspace(C,n)
G=[[sum(a*b for a,b in zip(f,bv)) for bv in Bz] for f in F]   # functionals restricted to closure subspace
m=len(G);k=len(Bz)
A=np.array([[float(x) for x in row] for row in G]).T
res=linprog(np.zeros(m),A_eq=A,b_eq=np.zeros(k),bounds=[(1,None)]*m,method='highs')
print('LP status',res.status,res.message)
if res.status!=0:sys.exit(1)
c=[Fr(x).limit_denominator(10**6) for x in res.x]
# choose an independent subset B of functionals greedily (largest c first), solve exactly for c_B
order=sorted(range(m),key=lambda i:-res.x[i]);basis=[];rows=[]
def indep(vs):
 M=[v[:] for v in vs];rk=0
 for col in range(k):
  p=next((i for i in range(rk,len(M)) if M[i][col]!=0),None)
  if p is None:continue
  M[rk],M[p]=M[p],M[rk]
  for i in range(len(M)):
   if i!=rk and M[i][col]!=0:f=M[i][col]/M[rk][col];M[i]=[x-f*y for x,y in zip(M[i],M[rk])]
  rk+=1
 return rk==len(vs)
for i in order:
 if indep(rows+[G[i]]):basis.append(i);rows.append(G[i])
rank=len(basis);tgt=d.get('target',k-4);print('rank',rank,'of',k,'(target',tgt,')')
N=[i for i in range(m) if i not in basis]
rhs=[-sum(c[i]*G[i][j] for i in N) for j in range(k)]
# solve sum_{i in basis} x_i G[i] = rhs exactly (overdetermined but consistent)
M=[[G[i][j] for i in basis]+[rhs[j]] for j in range(k)];rk=0;piv=[]
for col in range(rank):
 p=next(r for r in range(rk,k) if M[r][col]!=0);M[rk],M[p]=M[p],M[rk];M[rk]=[x/M[rk][col] for x in M[rk]]
 for r in range(k):
  if r!=rk and M[r][col]!=0:f=M[r][col];M[r]=[x-f*y for x,y in zip(M[r],M[rk])]
 rk+=1
consistent=all(M[r][-1]==0 for r in range(rank,k))
x=[M[r][-1] for r in range(rank)]
coef={i:c[i] for i in N};coef.update({b:x[j] for j,b in enumerate(basis)})
ok=consistent and all(v>0 for v in coef.values()) and all(sum(coef[i]*G[i][j] for i in range(m))==0 for j in range(k))
print('exact positive dependency:',ok,'min coef',float(min(coef.values())))
json.dump(dict(R=R,functionals=m,rank=rank,target=tgt,positive_dependency=ok,coefficients={str(i):str(v) for i,v in coef.items()}),open('posspan-'+R.replace('funcs-','').replace('.json','')+'.json' if R.endswith('.json') else f'posspan-R{R}.json','w'),indent=1)
print('RIGID (first order)' if ok and rank==tgt else 'NOT CERTIFIED')
