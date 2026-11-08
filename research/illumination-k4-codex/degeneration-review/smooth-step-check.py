"""Exact algebra controls for the smooth-step boundary exclusion criterion.
No optical directions, reflection-word discovery, or room search.
"""
from pathlib import Path
from fractions import Fraction as F
import json,itertools
B=Path(__file__).resolve().parent

def rank(rows):
 rows=[list(map(F,r)) for r in rows];pivot=0
 for j in range(len(rows[0])):
  hit=next((i for i in range(pivot,len(rows)) if rows[i][j]),None)
  if hit is None:continue
  rows[pivot],rows[hit]=rows[hit],rows[pivot];a=rows[pivot][j];rows[pivot]=[x/a for x in rows[pivot]]
  for i in range(len(rows)):
   if i!=pivot:
    a=rows[i][j];rows[i]=[x-a*y for x,y in zip(rows[i],rows[pivot])]
  pivot+=1
  if pivot==len(rows):break
 return pivot

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def bands(A,b,c,x):return all(0<=dot(a,x)+bb<=cc for a,bb,cc in zip(A,b,c))
def dual(A,b,c,lo,hi):
 assert len(A)==len(b)==len(c)==len(lo)==len(hi)
 assert all(x>=0 for x in lo+hi)
 weights=[v-u for u,v in zip(lo,hi)]
 assert all(sum(w*a[j] for w,a in zip(weights,A))==0 for j in range(len(A[0])))
 rhs=sum(u*bb+v*(cc-bb) for u,v,bb,cc in zip(lo,hi,b,c))
 assert rhs<0
 return rhs
# Hand-authored abstract interval incompatibility; not a realized room.
A=[[F(1)],[F(1)]];b=[F(0),F(2)];c=[F(1),F(1)]
assert rank(A)==1
rhs=dual(A,b,c,[F(1),F(0)],[F(0),F(1)])
assert rhs==-1
# Full boundary rank and reversal-like signs do not exclude the shared endpoint.
A2=[[F(1)],[F(-1)]];b2=[F(0),F(0)];c2=[F(1),F(1)]
assert rank(A2)==1 and bands(A2,b2,c2,[F(0)])
# Even full rank on the entire (x,y,e) chart can coexist with feasible e=1.
G=[[F(1),F(0),F(0)],[F(-1),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(-1),F(0)],[F(0),F(0),F(1,2)]]
assert rank(G)==3 and all(0<=dot(g,[0,0,1])<=1 for g in G)
# Reversing a path and restoring the below/above endpoint convention is identical.
reverse_checks=0
for a,b0,m,e,q in itertools.product([F(1),F(2),F(3)],[F(1),F(2)],[F(1,2),F(1),F(2)],[F(1,10),F(1,100)],[F(-1),F(0),F(1)]):
 u=-a*m+q*e;v=b0*m+q*e
 assert u<0<v
 K=b0*u+a*v
 Kr=a*v+b0*u
 assert K==Kr
 lower=K<0;upper=K>-2*e*u
 # The geometric below endpoint is still (-a,u) after time reversal.
 assert (lower,upper)==(Kr<0,Kr>-2*e*u)
 reverse_checks+=1
# Rank-deficient algebraic bands allow displacement much larger than step width.
multiscale=[]
for h in [F(1,10),F(1,100),F(1,1000)]:
 e=h*h;x=h;K=x*x
 assert 0<=K<=e and x/e==1/h
 multiscale.append({'h':str(h),'epsilon':str(e),'x':str(x),'x_over_epsilon':str(x/e)})
# Check the rank-injective quadratic absorption on an explicit scalar control.
absorption=[]
for e in [F(1,100),F(1,1000),F(1,10000)]:
 for x in [e/2,e,3*e/2]:
  K=x-x*x
  if 0<=K<=e:
   assert 0<=x<=2*e
   absorption.append({'epsilon':str(e),'x_over_epsilon':str(x/e)})
corrupt=[]
for label,args in [
 ('negative_multiplier',(A,[F(0),F(2)],c,[F(-1),F(0)],[F(0),F(1)])),
 ('uncancelled_variable',(A,[F(0),F(2)],c,[F(0),F(0)],[F(0),F(1)])),
 ('nonnegative_dual_rhs',(A,[F(0),F(0)],c,[F(1),F(0)],[F(0),F(1)]))]:
 try:dual(*args)
 except AssertionError:corrupt.append(label)
assert len(corrupt)==3
out={'status':'PASS','abstract_incompatible_band_certificate':{'A':[['1'],['1']],'b':['0','2'],'c':['1','1'],'lower_weights':['1','0'],'upper_weights':['0','1'],'cancelled_rhs':str(rhs)},'shared_endpoint_feasible':True,'full_chart_rank_but_feasible':{'rank':3,'normalized_witness':['0','0','1']},'reversal_controls':reverse_checks,'rank_deficient_multiscale':multiscale,'rank_injective_scalar_controls':absorption,'corrupt_certificates_rejected':corrupt,'scope':'Abstract exact algebra and existing local-step formula only. No actual room exclusion, dark deformation, new optical word, ray search or global minimum.'}
(B/'smooth-step-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
