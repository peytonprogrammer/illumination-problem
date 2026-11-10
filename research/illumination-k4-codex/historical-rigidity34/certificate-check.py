"""Exact checker for the frozen86-event certificate, independent of construction.
No LP or direction scanning. Rebuild each fixed wall word, one-corner premise,
quadratic derivative, rank, symmetries and strictly positive dependence.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json,hashlib
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent/'rigidity-review'))
from event_geometry import EventModel,dot,cross,sub,add,scale,matmul,canon,rank

def geometry_and_gradients(model,events):
 for e in events:
  O=((F(1),F(0)),(F(0),F(1)));shift=(model.zero,model.zero)
  for i in e['word']:
   R,b=model.reflectors[i];shift=model.mapped(O,shift,b);O=matmul(O,R)
  lifted=model.mapped(O,shift,model.tform);A=tuple(sub(lifted[j],model.sform[j]) for j in (0,1));av=model.value(A)
  assert list(map(str,av))==e['unfolded_target_minus_s']
  O=((F(1),F(0)),(F(0),F(1)));shift=(model.zero,model.zero);lower=F(0);images=[]
  for i in [*e['word'],None]:
   if i is None:upper=F(1)
   else:
    n=(-model.dirs[i][1],model.dirs[i][0]);nu=tuple(sum(O[j][k]*n[k] for k in (0,1)) for j in (0,1));wall=model.mapped(O,shift,model.vforms[i]);wv=model.value(wall);assert dot(nu,av)!=0
    upper=dot(nu,sub(wv,model.s))/dot(nu,av)
   assert 0<=lower<=upper<=1
   for j,vertex in enumerate(model.vertices):
    C=tuple(sub(p,s) for p,s in zip(model.mapped(O,shift,model.vforms[j]),model.sform));cv=model.value(C)
    mu=dot(av,cv)/dot(av,av)
    if not cross(av,cv) and 0<mu<1 and lower<=mu<=upper:images.append((vertex,C))
   lower=upper
   if i is not None:
    R,b=model.reflectors[i];shift=model.mapped(O,shift,b);O=matmul(O,R)
  assert images
  assert {model.value(C) for v,C in images}=={model.value(images[0][1])},'More than one unfolded corner'
  assert all(list(v)==e['corner'] for v,C in images)
  C=images[0][1];area=sum(cross(a,b) for a,b in zip(model.vertices,model.vertices[1:]+model.vertices[:1]));j=model.vertices.index(tuple(e['corner']));turn=cross(sub(model.vertices[j],model.vertices[j-1]),sub(model.vertices[(j+1)%model.W],model.vertices[j]));assert area*turn<0
  def polynomial(z):return cross(tuple(dot(a,z) for a in A),tuple(dot(c,z) for c in C))
  assert polynomial(model.theta)==0
  gradient=[]
  for j in range(model.dim):
   plus=tuple(x+int(i==j) for i,x in enumerate(model.theta));minus=tuple(x-int(i==j) for i,x in enumerate(model.theta))
   gradient.append(e['perturb_side']*(polynomial(plus)-polynomial(minus))/2)
  assert gradient==list(map(F,e['gradient'])) and canon(gradient)==tuple(e['row'])
 return True

def algebra(model,events,coeff):
 rows=[tuple(map(F,e['row'])) for e in events]
 assert len(coeff)==len(rows) and all(c>0 for c in coeff)
 total=[sum(c*r[j] for c,r in zip(coeff,rows)) for j in range(model.dim)]
 assert rank([*model.closure,total])==2
 assert rank([*model.closure,*rows])-2==34
 assert rank(model.syms)==4 and all(dot(r,s)==0 for r in rows for s in model.syms)
 return True
if __name__=='__main__':
 model=EventModel(json.loads((B/'room.json').read_text()));events=json.loads((B/'events-targeted.json').read_text());certificate=json.loads((B/'positive-span.json').read_text());coeff=list(map(F,certificate['coefficients']))
 assert certificate['status']=='PASS' and len(events)==86
 assert geometry_and_gradients(model,events) and algebra(model,events,coeff)
 corrupt=[]
 for kind in ('missing_coefficient','negative_coefficient','reversed_row','wrong_gradient'):
  try:
   if kind=='missing_coefficient':algebra(model,events,coeff[:-1])
   elif kind=='negative_coefficient':c=list(coeff);c[0]=-c[0];algebra(model,events,c)
   elif kind=='reversed_row':e=json.loads(json.dumps(events));e[0]['row']=[-x for x in e[0]['row']];algebra(model,e,coeff)
   else:e=json.loads(json.dumps(events));e[0]['gradient'][0]=str(F(e[0]['gradient'][0])+1);geometry_and_gradients(model,e)
  except AssertionError:corrupt.append(kind)
 assert len(corrupt)==4
 out=dict(status='PASS',room_sha256=hashlib.sha256((B/'room.json').read_bytes()).hexdigest(),events=len(events),quadratic_derivative_coordinates_checked=len(events)*model.dim,rank_on_closure=34,closure_dimension=38,common_kernel_dimension=4,strict_positive_coefficients=len(coeff),one_corner_geometry_verified=True,corruptions_rejected=corrupt,scope='Checks a finite local rigidity certificate, not a global minimum. No LP, direction search or peer executable used.')
 (B/'certificate-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
