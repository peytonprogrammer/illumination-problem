"""Independent general-line dual-number differentiation of frozen event words.
No new ray traces, directions, words, rooms, or point searches.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
B=Path('<SOURCE_WORKSPACE>/.context/illumination-k4-codex/angle-rigidity');OLD=Path('<SOURCE_WORKSPACE>/.context/illumination-k4-codex/rigidity-review');OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(OLD));import check as old
D=old.D

def reflect(p,a,b):
 e=tuple(y-x for x,y in zip(a,b));v=tuple(x-y for x,y in zip(p,a));t=2*sum(x*y for x,y in zip(e,v))/sum(x*x for x in e)
 return tuple(x+t*z-y for x,z,y in zip(a,e,v))

def unfold(p,word,verts):
 for i in reversed(word):p=reflect(p,verts[i],verts[(i+1)%22])
 return p

def corner_prefix(e):
 target=unfold(tuple(map(F,old.t0)),e['word'],old.verts);A=old.vecsub(target,old.s0)
 signs=[1,1];shift=[F(0),F(0)];low=F(0)
 for k,i in enumerate([*e['word'],None]):
  C=tuple(signs[j]*e['corner'][j]+shift[j]-old.s0[j] for j in (0,1))
  if i is None:high=F(1)
  else:
   n=1-old.axes[i];high=(signs[n]*old.verts[i][n]+shift[n]-old.s0[n])/A[n]
  beta=old.dot(A,C)/old.dot(A,A)
  if old.cross(A,C)==0 and 0<beta<1 and low<=beta<=high:return k
  low=high
  if i is not None:n=1-old.axes[i];shift[n]+=2*signs[n]*old.verts[i][n];signs[n]*=-1
 raise AssertionError('No actual corner occurrence')

def main():
 r=json.loads((B/'result.json').read_text());c=json.loads((B/'cone.json').read_text());events=json.loads((OLD/'events.json').read_text());rows=[list(map(F,g)) for g in r['rows']];delta=list(map(F,c['delta']))
 assert len(delta)==48 and len(rows)==147
 strict=json.loads((B/'strict-escape.json').read_text());strict_delta=list(map(F,strict['delta']))
 tangent_controls=[delta,strict_delta,[F((13*j+7)%17-8) for j in range(48)]]
 count=0
 for e,g in zip(events,rows):
  prefix=corner_prefix(e);idx=old.verts.index(tuple(e['corner']))
  for d in tangent_controls:
   v=[tuple(D(x,d[2*i+j]) for j,x in enumerate(p)) for i,p in enumerate(old.verts)];S=tuple(D(x,d[44+j]) for j,x in enumerate(old.s0));T=tuple(D(x,d[46+j]) for j,x in enumerate(old.t0))
   a=tuple(x-y for x,y in zip(unfold(T,e['word'],v),S));b=tuple(x-y for x,y in zip(unfold(v[idx],e['word'][:prefix],v),S));f=e['perturb_side']*old.cross(a,b)
   assert f.a==0 and f.b==old.dot(g,d),'General reflection derivative mismatch'
   count+=1
 values=[old.dot(g,delta) for g in rows]
 assert all(v>=0 for v in values) and any(v>0 for v in values)
 assert list(map(str,values))==c['constraint_values']
 strict_values=[old.dot(g,strict_delta) for g in rows]
 assert min(strict_values)>0 and list(map(str,strict_values))==strict['constraint_values']
 assert all(old.dot(g,q)==0 for q in r['symmetries'] for g in rows)
 assert old.rank(rows)==43 and old.rank(r['symmetries'])==5
 ans=dict(status='PASS',independent_general_reflection_derivatives=count,events=147,exact_rank=43,known_dark_tangent_dimension=5,survival_tangent_inequalities_nonnegative=147,strict_positive=sum(v>0 for v in values),zero=sum(v==0 for v in values),strict_survival_tangent_verified=147,conclusion='The saved147-event first-order cone does not certify angle-changing local rigidity. This does not prove a nearby dark room or disprove local rigidity.',no_new_optical_discovery=True)
 (OUT/'validation.json').write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))
if __name__=='__main__':main()
