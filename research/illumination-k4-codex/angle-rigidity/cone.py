"""Solve a finite saved-gradient cone; rationally certify the returned answer."""
import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
B=Path(__file__).resolve().parent
r=json.loads((B/'result.json').read_text());rows=[list(map(F,g)) for g in r['rows']];m=len(rows);n=48
A=np.array([[float(rows[i][j]) for i in range(m)] for j in range(n)])
b=-np.sum(A,axis=1)
sol=linprog(np.ones(m),A_eq=A,b_eq=b,bounds=(0,None),method='highs')
answer=dict(solver_message=sol.message,success=bool(sol.success))
if sol.success:
 support=[i for i,x in enumerate(sol.x) if x>1e-7]
 # Exact Gauss-Jordan solve with the floating support only; no floating verdict.
 M=[[rows[i][j] for i in support]+[-sum(g[j] for g in rows)] for j in range(n)]
 piv=[];row=0
 for col in range(len(support)):
  p=next((p for p in range(row,n) if M[p][col]),None)
  assert p is not None,'dependent support'
  M[row],M[p]=M[p],M[row];v=M[row][col];M[row]=[x/v for x in M[row]]
  for k in range(n):
   if k!=row and M[k][col]:v=M[k][col];M[k]=[x-v*y for x,y in zip(M[k],M[row])]
  piv.append(row);row+=1
 assert all(not any(q[:-1]) and not q[-1] for q in M[row:])
 weights=[F(1)]*m
 for i,p in zip(support,piv):weights[i]+=M[p][-1]
 assert all(w>0 for w in weights)
 assert all(sum(weights[i]*rows[i][j] for i in range(m))==0 for j in range(n))
 answer.update(status='EXACT_STRICT_POSITIVE_DEPENDENCY',weights=list(map(str,weights)),support=len(support),minimum_weight=str(min(weights)),rank=r['rank'])
else:
 answer['status']='NO_STRICT_DEPENDENCY_FROM_FLOATING_LP'
(B/'cone.json').write_text(json.dumps(answer,indent=2)+'\n');print(json.dumps({k:v for k,v in answer.items() if k!='weights'},indent=2))
if not sol.success:
 G=A.T
 escape=linprog(-G.sum(axis=0),A_ub=-G,b_ub=np.zeros(m),bounds=[(-1,1)]*n,method='highs')
 assert escape.success
 active=[]
 for i,g in enumerate(rows):
  if abs(float(G[i]@escape.x))<1e-6:active.append((g,F(0)))
 for j,x in enumerate(escape.x):
  if abs(abs(float(x))-1)<1e-7:active.append(([F(k==j) for k in range(n)],F(1 if x>0 else -1)))
 # Extract an exact independent square active system, then back-substitute.
 piv={}
 for a,rhs in active:
  v=[*a,rhs]
  for k,q in sorted(piv.items()):
   if v[k]:c=v[k];v=[x-c*y for x,y in zip(v,q)]
  k=next((k for k in range(n) if v[k]),None)
  if k is None:
   assert not v[-1],'Inconsistent active equations'
   continue
  c=v[k];piv[k]=[x/c for x in v]
 assert len(piv)==n,('Active system not full rank',len(piv))
 delta=[F(0)]*n
 for k,q in sorted(piv.items(),reverse=True):delta[k]=q[-1]-sum(q[j]*delta[j] for j in range(k+1,n))
 values=[sum(x*y for x,y in zip(g,delta)) for g in rows]
 assert min(values)>=0,'Exact reconstruction failed'
 assert max(values)>0,'No nonsymmetry escape reconstructed'
 answer.update(status='EXACT_NONSYMMETRY_SURVIVAL_TANGENT',delta=list(map(str,delta)),constraint_values=list(map(str,values)),strict_positive=sum(v>0 for v in values),zero=sum(v==0 for v in values),minimum=str(min(values)),maximum=str(max(values)))
 (B/'cone.json').write_text(json.dumps(answer,indent=2)+'\n');print(json.dumps({k:v for k,v in answer.items() if k not in ('weights','delta','constraint_values')},indent=2))
