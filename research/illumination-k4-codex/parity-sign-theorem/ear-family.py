"""Exact cone structure on the34previously frozen axis holdouts. No rays."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,math
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parent;INP=ROOT/'inputs/holdouts'
dot=lambda a,b:sum(x*y for x,y in zip(a,b))

def solve(A,b,unique=False):
 n=len(A[0]);M=[list(map(F,row))+[F(rhs)] for row,rhs in zip(A,b)];piv=[];k=0
 for c in range(n):
  p=next((i for i in range(k,len(M)) if M[i][c]),None)
  if p is None:continue
  M[k],M[p]=M[p],M[k];v=M[k][c];M[k]=[x/v for x in M[k]]
  for i in range(len(M)):
   if i!=k and M[i][c]:v=M[i][c];M[i]=[x-v*y for x,y in zip(M[i],M[k])]
  piv.append(c);k+=1
  if k==len(M):break
 assert all(any(row[:n]) or not row[n] for row in M)
 if unique:assert len(piv)==n
 x=[F(0)]*n
 for i,c in enumerate(piv):x[c]=M[i][-1]
 assert all(dot(row,x)==rhs for row,rhs in zip(A,b))
 return tuple(x),len(piv)

def one(selection):
 tag=selection['tag'];room=json.loads((INP/(tag+'.json')).read_text());old=json.loads((INP/('funcs-'+tag+'-R12.json')).read_text());events=json.loads((INP/('events-'+tag+'-R12.json')).read_text())['rows']
 vertices=list(map(tuple,room['vertices']));W=len(vertices);dim=W+4
 unit=lambda k:tuple(F(i==k) for i in range(dim))
 dirs=[]
 for a,b in zip(vertices,vertices[1:]+vertices[:1]):
  d=(b[0]-a[0],b[1]-a[1]);l=math.gcd(*map(abs,d));dirs.append((d[0]//l,d[1]//l))
 normals=[(-d[1],d[0]) for d in dirs];B=[]
 for i in range(W):
  p=(i-1)%W;a=normals[p];b=normals[i];det=a[0]*b[1]-a[1]*b[0];assert det
  B.append((tuple((F(b[1])*unit(p)[k]-F(a[1])*unit(i)[k])/det for k in range(dim)),
            tuple((-F(b[0])*unit(p)[k]+F(a[0])*unit(i)[k])/det for k in range(dim))))
 ell=[]
 for i,d in enumerate(dirs):
  nn=dot(d,d);ell.append(tuple(sum(F(d[a],nn)*(B[(i+1)%W][a][k]-B[i][a][k]) for a in (0,1)) for k in range(dim)))
 T=list(B[0])+ell+[unit(W+k) for k in range(4)]
 assert all(not sum(F(dirs[i][a])*ell[i][k] for i in range(W)) for a in (0,1) for k in range(dim))
 rows=[tuple(sum(F(row[k])*T[k][c] for k in range(W+6)) for c in range(dim)) for row in old['funcs']]
 theta=tuple(F(dot(n,v)) for n,v in zip(normals,vertices))+tuple(F(x) for p in room['marked'] for x in p)
 assert all(dot(g,theta)==0 for g in rows)
 axis=[i for i,e in enumerate(events) if any(sorted(abs(e['corner'][a]-p[a]) for a in (0,1))==[0,1] for p in room['marked'])]
 length=tuple(sum(row[c] for row in ell) for c in range(dim));gauge=[unit(W),unit(W+1),length]
 norms=[max(map(abs,rows[i])) for i in axis];A=np.array([[float(v/n) for v in rows[i]] for i,n in zip(axis,norms)]);geq=np.array([[float(v) for v in row] for row in gauge])
 def proposal(objective):
  res=linprog(objective,A_ub=-A,b_ub=np.zeros(len(axis)),A_eq=geq,b_eq=np.zeros(3),bounds=[(-1,1)]*dim,method='highs');assert res.success
  eq=list(gauge);rhs=[F(0)]*3
  for i,value in zip(axis,A@res.x):
   if abs(value)<1e-8:eq.append(rows[i]);rhs.append(F(0))
  for c,value in enumerate(res.x):
   if abs(abs(value)-1)<1e-8:eq.append(unit(c));rhs.append(F(1 if value>0 else -1))
  x,_=solve(eq,rhs,unique=True)
  assert all(dot(g,x)==0 for g in gauge) and all(dot(rows[i],x)>=0 for i in axis)
  return x
 delta=proposal(-A.sum(axis=0));assert any(dot(rows[i],delta)>0 for i in axis)
 stress=None;facial_steps=0
 for step in range(len(axis)+1):
  Z=[i for i in axis if dot(rows[i],delta)==0]
  if not Z:stress=[];break
  scales=[max(map(abs,rows[i])) for i in Z];R=[tuple(v/s for v in rows[i]) for i,s in zip(Z,scales)]
  M=np.array([[float(v) for v in row] for row in R])
  lp=linprog(np.ones(len(Z)),A_eq=M.T,b_eq=np.zeros(dim),bounds=[(1,None)]*len(Z),method='highs');assert lp.status in (0,2)
  if lp.status==0:
   active=[i for i,v in enumerate(lp.x) if abs(v-1)<1e-8];free=[i for i in range(len(Z)) if i not in active]
   if free:
    x,_=solve([[R[i][c] for i in free] for c in range(dim)],[-sum(R[i][c] for i in active) for c in range(dim)],unique=True)
   else:x=[]
   mu=[F(1)]*len(Z)
   for i,v in zip(free,x):mu[i]=v
   stress=[v/s for v,s in zip(mu,scales)]
   assert all(v>0 for v in stress)
   assert all(sum(w*rows[i][c] for i,w in zip(Z,stress))==0 for c in range(dim))
   break
  positions=[axis.index(i) for i in Z];other=proposal(-A[positions].sum(axis=0));assert any(dot(rows[i],other)>0 for i in Z)
  delta=tuple(x+y for x,y in zip(delta,other));facial_steps+=1
 else:raise AssertionError('facial reduction did not terminate')
 assert stress is not None
 rankzero=solve(list(zip(*[rows[i] for i in Z])),[F(0)]*dim)[1] if Z else 0
 conedim=dim-rankzero-3
 trans=[tuple(F(n[a]) for n in normals)+tuple(F(k%2==a) for k in range(4)) for a in (0,1)]
 assert all(dot(g,v)==0 for g in rows for v in trans)
 result={'tag':tag,'walls':W,'axis_rows':len(axis),'forced_zero_rows':Z,'forced_zero_rank':rankzero,
         'exact_positive_stress':list(map(str,stress)),'cone_dimension_mod_symmetries':conedim,
         'exact_relative_interior_direction':list(map(str,delta)),'facial_reduction_steps':facial_steps}
 if conedim==1:
  assert solve(list(zip(*trans,theta,delta)),[F(0)]*dim)[1]==4
  s,t=room['marked'];dt=(t[0]-s[0],t[1]-s[1]);axis_t=next(k for k in (0,1) if dt[k]);beta=delta[W+2+axis_t]/dt[axis_t]
  fixed_marks=all(delta[W+2+k]==beta*dt[k] for k in (0,1))
  result['source_and_target_fixed_after_removing_scale']=fixed_marks
  if fixed_marks:
   sym=tuple(theta[c]-sum(F(s[k])*trans[k][c] for k in (0,1)) for c in range(dim))
   local=tuple(delta[c]-beta*sym[c] for c in range(dim));movingwalls=[c for c in range(W) if local[c]]
   movingvertices={str(i):[str(dot(r,local)) for r in b] for i,b in enumerate(B) if any(dot(r,local) for r in b)}
   result['moving_wall_indices']=movingwalls;result['moving_vertices']=movingvertices
   adjacent=len(movingwalls)==2 and ((movingwalls[0]+1)%W==movingwalls[1] or (movingwalls[1]+1)%W==movingwalls[0])
   ear=False
   if adjacent:
    first=next(i for i in movingwalls if (i+1)%W in movingwalls);prev=(first-1)%W;last=(first+2)%W
    a=normals[prev];b=normals[last];k=next(k for k in (0,1) if a[k]);rat=F(b[k],a[k])
    ear=all(F(b[k])==rat*a[k] for k in (0,1)) and theta[last]==rat*theta[prev]
   result['single_triangular_ear_mode']=ear
  repairset={tuple(c) for c in selection['diagonal_repairs']}
  cut=[i for i,e in enumerate(events) if tuple(e['corner']) in repairset and dot(rows[i],delta)<0]
  assert cut
  result['single_repair_event']={'index':cut[0],'corner':events[cut[0]]['corner'],'direction':events[cut[0]]['dir'],'value':str(dot(rows[cut[0]],delta))}
 return result

if __name__ == "__main__":
 out=[]
 for selection in json.loads((INP/'selection.json').read_text()):
  row=one(selection);out.append(row);print(json.dumps({k:row[k] for k in ('tag','cone_dimension_mod_symmetries','single_triangular_ear_mode') if k in row}),flush=True)
 result={'status':'EXACT_PASS','rooms':len(out),'cone_dimension_histogram':dict(Counter(r['cone_dimension_mod_symmetries'] for r in out)),
         'one_dimensional_cones':sum(r['cone_dimension_mod_symmetries']==1 for r in out),
         'single_triangular_ear_modes':sum(r.get('single_triangular_ear_mode',False) for r in out),
         'cases':out,'scope':'Algebra of existing frozen34holdout packets only, exact stresses/ranks. Optical validity for newly transformed rows inherits the prior packets; no new event tracing and no universal theorem.'}
 (ROOT/'ear-family.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2),flush=True)
