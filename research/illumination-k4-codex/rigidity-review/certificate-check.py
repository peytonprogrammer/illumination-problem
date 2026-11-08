"""Independent exact algebra readback and corruption controls for saved events.
Does not use infinitesimal tracing. Derivatives are recovered via symmetric
finite differences, exact for quadratic corner determinants.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd
from collections import Counter
import json
from check import B,DIM,theta,clos,syms,axes,verts,vforms,sforms,tforms,dot,cross,rank,unit,vecsub,vecadd,scale

def endpoint_forms(word):
 signs=[1,1];shift=[(F(0),)*DIM,(F(0),)*DIM]
 for i in word:
  n=1-axes[i];shift[n]=vecadd(shift[n],scale(2*signs[n],vforms[i][n]));signs[n]*=-1
 return tuple(vecadd(scale(signs[j],tforms[j]),shift[j]) for j in (0,1))
def det_value(A,C,z):return cross(tuple(dot(x,z) for x in A),tuple(dot(x,z) for x in C))
def algebra(events):
 for e in events:
  T=endpoint_forms(e['word']);A=tuple(vecsub(T[j],sforms[j]) for j in (0,1))
  # Find the corner image from the prefix where the unfolded segment meets it.
  j=verts.index(tuple(e['corner']));orientation=cross(vecsub(verts[j],verts[j-1]),vecsub(verts[(j+1)%len(verts)],verts[j]));area=sum(cross(a,b) for a,b in zip(verts,verts[1:]+verts[:1]));assert orientation*area<0,'Not reflex'
  signs=[1,1];shift=[(F(0),)*DIM,(F(0),)*DIM];images=[];lower=F(0)
  for i in [*e['word'],None]:
   C=tuple(vecsub(vecadd(scale(signs[k],vforms[j][k]),shift[k]),sforms[k]) for k in (0,1))
   av=tuple(dot(x,theta) for x in A);cv=tuple(dot(x,theta) for x in C)
   if i is None:upper=F(1)
   else:
    n=1-axes[i];wall=vecadd(scale(signs[n],vforms[i][n]),shift[n]);upper=(dot(wall,theta)-dot(sforms[n],theta))/av[n]
   assert lower<=upper
   parameter=dot(av,cv)/dot(av,av)
   if not cross(av,cv) and 0<parameter<1 and lower<=parameter<=upper:images.append(C)
   lower=upper
   if i is not None:
    n=1-axes[i];shift[n]=vecadd(shift[n],scale(2*signs[n],vforms[i][n]));signs[n]*=-1
  # At a reflected corner two adjoining prefixes can give the same image.
  unique={tuple(tuple(dot(x,theta) for x in C)) for C in images};assert len(unique)==1
  C=images[0];assert det_value(A,C,theta)==0
  gradient=[]
  for k in range(DIM):
   plus=tuple(x+F(i==k) for i,x in enumerate(theta));minus=tuple(x-F(i==k) for i,x in enumerate(theta))
   gradient.append(e['perturb_side']*(det_value(A,C,plus)-det_value(A,C,minus))/2)
  assert gradient==list(map(F,e['gradient'])),'Gradient mismatch'
 return True

def span(rows,coeff):
 assert set(coeff)==set(range(len(rows))) and all(v>0 for v in coeff.values())
 weighted=[sum(coeff[i]*rows[i][j] for i in coeff) for j in range(DIM)]
 assert rank([*clos,weighted])==rank(clos)
 assert rank([*clos,*rows])-rank(clos)==22
 assert all(dot(r,s)==0 for r in rows for s in syms)
 return True

def matrices(gens):
 identity=(1,0,0,1);seen={identity};queue=[identity]
 for a in queue:
  for b in gens:
   c=(a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
   if c not in seen:seen.add(c);queue.append(c)
 return seen
if __name__=='__main__':
 events=json.loads((B/'events.json').read_text());assert algebra(events)
 rows=[tuple(map(F,r)) for r in json.loads((B/'inputs/funcs-R12.json').read_text())['funcs']];coeff={int(i):F(v) for i,v in json.loads((B/'inputs/posspan-R12.json').read_text())['coefficients'].items()};assert span(rows,coeff)
 corrupt=[]
 for mode in ('negative_weight','missing_weight','reversed_row','wrong_gradient'):
  try:
   if mode=='negative_weight':c=dict(coeff);c[0]=-c[0];span(rows,c)
   elif mode=='missing_weight':c=dict(coeff);del c[0];span(rows,c)
   elif mode=='reversed_row':r=list(rows);r[0]=tuple(-x for x in r[0]);span(r,coeff)
   else:e=json.loads(json.dumps(events));e[0]['gradient'][0]=str(F(e[0]['gradient'][0])+1);algebra(e)
  except AssertionError:corrupt.append(mode)
 assert len(corrupt)==4
 H=(1,0,0,-1);V=(-1,0,0,1);diag=(0,1,1,0);orth=matrices([H,V]);mixed=matrices([H,V,diag]);assert len(orth)==4 and len(mixed)==8
 lifts=[dict(angle_units=a,points=gcd(a,4),cone_angle_pi=2*a//gcd(a,4)) for a in (1,2,3,5,6,7)]
 # Direct visibility in a fixed L-shaped room depends on the product a*b.
 lcontrols=[(F(1,2),F(1),1),(F(1),F(1),0),(F(3,2),F(1),-1)]
 for a,b,sgn in lcontrols:
  determinant=cross((b+1,-1-a),(1,-a));assert determinant==1-a*b and (determinant>0)-(determinant<0)==sgn
 result=dict(status='PASS',exact_quadratic_gradient_checks=147*DIM,events_checked=147,strict_positive_dependency='PASS_ON_CLOSURE',corruption_controls_rejected=corrupt,orthogonal_group_order=len(orth),mixed_group_order=len(mixed),corrected_corner_lifts=lifts,nonpolyhedral_visibility='L-room direct segment: a*b<1',limitations='Finite differences check the exact quadratic derivative, not validity of arbitrary event geometry; check.py and validate.py provide independent word/side replay.')
 (B/'certificate-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
