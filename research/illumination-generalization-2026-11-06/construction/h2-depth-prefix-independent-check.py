"""Independent prescribed critical-cell check, no discovery or author execution."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent/'review';req=json.loads((R/'h2-depth-prefix-review-request.json').read_text());pins={f:hashlib.sha256((R/f).read_bytes()).hexdigest()==h for f,h in req['source_sha256'].items()};assert all(pins.values())
def contour(d):return [(F(x),F(y)) for x,y in [(0,0),(1,0),(1,1),(F(4,3),1),(F(4,3),3),(1,3),(1,5),(d+2,5),(d+2,7),(1,7),(1,9),(0,9),(0,7),(-1,7),(-1,5),(0,5),(0,4),(-1,4),(-1,2),(0,2)]]
def edge(p):return list(zip(p,p[1:]+p[:1]))
def minus(a,b):return (a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def image(w,p):
 sx=sy=1;tx=ty=F(0)
 for k in w:
  a,b=edge(contour(F(0)))[k]
  if a[0]==b[0]:tx+=2*sx*a[0];sx=-sx
  else:ty+=2*sy*a[1];sy=-sy
 return sx*p[0]+tx,sy*p[1]+ty

def direction(w,d):return minus(image(w,(1+d,F(6))),(F(1),F(2)))
def trace(w,d):
 v=direction(w,d);p=(F(1),F(2));T=(1+d,F(6));es=edge(contour(d));actual=[]
 for _ in range(len(w)+1):
  hits=[]
  for i,(a,b) in enumerate(es):
   e=minus(b,a);den=cross(v,e)
   if den:
    tt=cross(minus(a,p),e)/den;rr=cross(minus(a,p),v)/den
    if tt>0 and 0<=rr<=1:hits.append((tt,i,rr))
  assert hits;time=min(x[0] for x in hits);dt=minus(T,p)
  if cross(v,dt)==0 and sum(v[j]*dt[j] for j in (0,1))>0:
   t=dt[0]/v[0] if v[0] else dt[1]/v[1]
   if t<time:return actual==w
  hs=[(i,r) for t,i,r in hits if t==time]
  if len(hs)!=1 or hs[0][1] in(0,1):return False
  k=hs[0][0]
  if k in {8,12,13,14,16,17,18}:return False
  p=(p[0]+time*v[0],p[1]+time*v[1])
  if p[0]>1+d and 5<=p[1]<=7:return False
  actual.append(k);a,b=es[k];v=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1])
 return False

def roots(fn):
 a=fn(F(0));b=fn(F(1))-a
 assert fn(F(2))==a+2*b
 return [-a/b] if b and 0<=-a/b<=2 else []
words=[[19,0,3,15],[19,0,1,19,5,15],[3,15],[15,9,10,11,6],[0,19,5,11,10,6],[4,3,0,19,5,11,10,6]];rows=[];allints=[];allpts=set()
for w in words:
 assert direction(w,F(0))[1]==direction(w,F(1))[1]!=0
 cuts={F(0),F(2)};cuts.update(roots(lambda d:direction(w,d)[0]))
 for j in range(len(w)+1):
  prefix=w[:j]
  for k in range(20):cuts.update(roots(lambda d,k=k:cross(minus(image(prefix,contour(d)[k]),(F(1),F(2))),direction(w,d))))
  for y in (F(5),F(6),F(7)):cuts.update(roots(lambda d,y=y:cross(minus(image(prefix,(1+d,y)),(F(1),F(2))),direction(w,d))))
 cs=sorted(cuts);pts=[d for d in cs if trace(w,d)];ints=[(a,b) for a,b in zip(cs,cs[1:]) if trace(w,(a+b)/2)];allpts.update(pts);allints+=ints;rows.append({'word':w,'cut_count':len(cs),'intervals':[[str(a),str(b)] for a,b in ints],'points':list(map(str,pts))})
points=sorted({F(0),F(14,15)}|{x for a,b in allints for x in(a,b) if x<=F(14,15)}|{x for x in allpts if x<=F(14,15)})
for x in points:
 if x<F(14,15):assert x in allpts or any(a<x<b for a,b in allints)
for a,b in zip(points,points[1:]):assert any(c<(a+b)/2<d for c,d in allints)
out={'status':'INDEPENDENT_EXACT_SIX_WORD_CELL_COVER_PASS','scope':'0<=D<14/15 ONLY','source_pins_current':pins,'rows':rows,'author_code_executed':False,'whole_goal_complete':False};(P/'h2-depth-prefix-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cut_counts':[r['cut_count'] for r in rows]}))
