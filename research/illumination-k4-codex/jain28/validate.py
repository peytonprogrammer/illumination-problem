"""Exact fixed-word validation on deformations of the one supplied28-wall boundary-target room."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import importlib.util,json,random,sys
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B.parent/'rigidity-review'))
from event_geometry import EventModel,matmul
r=EventModel(json.loads((B/'room.json').read_text()));r.matrix_product=matmul

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def evalpt(p,z):return tuple(dot(a,z) for a in p)
def rref(rows):
 out=[list(map(F,x)) for x in rows];piv=[];k=0
 for j in range(len(out[0])):
  hit=next((i for i in range(k,len(out)) if out[i][j]),None)
  if hit is None:continue
  out[k],out[hit]=out[hit],out[k];v=out[k][j];out[k]=[a/v for a in out[k]]
  for i in range(len(out)):
   if i!=k:
    v=out[i][j];out[i]=[a-v*b for a,b in zip(out[i],out[k])]
  piv.append(j);k+=1
  if k==len(out):break
 return out,piv
spec=importlib.util.spec_from_file_location('boundary_events',B/'boundary-check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
boundary_model=mod.BoundaryEventModel(r.room)
boundary_row=boundary_model.boundary_row()[0]
C,pivots=rref([*r.closure,boundary_row])
def make_delta(v):
 d=list(map(F,v))
 for c,k in zip(C,pivots):d[k]=-sum(c[j]*d[j] for j in range(r.dim) if j!=k)
 assert all(dot(c,d)==0 for c in C);return d
def move(d):
 eps=F(1,10**7)/(1+max(map(abs,d)))
 return tuple(a+eps*b for a,b in zip(r.theta,d))
def simple(z):
 vs=[evalpt(p,z) for p in r.vforms];edges=list(zip(vs,vs[1:]+vs[:1]));assert all(z[i]>0 for i in range(2,2+r.W))
 for i,(a,b) in enumerate(edges):
  for j,(c,d) in enumerate(edges):
   if j<=i or j==i+1 or (i==0 and j==len(edges)-1):continue
   signs=(cross(sub(b,a),sub(c,a)),cross(sub(b,a),sub(d,a)),cross(sub(d,c),sub(a,c)),cross(sub(d,c),sub(b,c)))
   bbox=all(max(min(a[k],b[k]),min(c[k],d[k]))<=min(max(a[k],b[k]),max(c[k],d[k])) for k in (0,1))
   assert not(bbox and signs[0]*signs[1]<=0 and signs[2]*signs[3]<=0),(i,j)
 def inside(p):
  odd=False
  for a,b in edges:
   if not cross(sub(b,a),sub(p,a)) and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1)):return p==t
   if (a[1]>p[1])!=(b[1]>p[1]):
    if a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])>p[0]:odd=not odd
  return odd
 s,t=evalpt(r.sform,z),evalpt(r.tform,z);assert inside(s) and inside(t);return vs,s,t

def replay(e,z):
 vs,s,t=simple(z);O=((F(1),F(0)),(F(0),F(1)));shift=(F(0),F(0))
 def ref(i):
  normal=(-r.dirs[i][1],r.dirs[i][0]);nn=dot(normal,normal);R=tuple(tuple(F(int(a==b))-F(2*normal[a]*normal[b],nn) for b in (0,1)) for a in (0,1));offset=tuple(F(2*normal[j],nn)*dot(normal,vs[i]) for j in (0,1));return R,offset
 for i in e['word']:
  R,b=ref(i);shift=tuple(sum(O[j][k]*b[k] for k in (0,1))+shift[j] for j in (0,1));O=r.matrix_product(O,R)
 lift=tuple(sum(O[j][k]*t[k] for k in (0,1))+shift[j] for j in (0,1));v=sub(lift,s);pos=s
 for step in range(len(e['word'])+1):
  hits=[]
  for i,a in enumerate(vs):
   d=r.dirs[i];n=(-d[1],d[0]);den=dot(n,v)
   if not den:continue
   tau=(dot(n,a)-dot(n,pos))/den
   if tau<=0:continue
   contact=tuple(pos[j]+tau*v[j] for j in (0,1));along=dot(sub(contact,a),d);length=z[2+i]*dot(d,d)
   if 0<=along<=length:hits.append((tau,i,along==0 or along==length))
  if not hits:return False
  tau,i,corner=min(hits);dt=sub(t,pos)
  if not cross(dt,v):
   k=next(j for j in (0,1) if v[j]);mu=dt[k]/v[k]
   if 0<mu<=tau and not corner:return step==len(e['word'])
  if step==len(e['word']) or i!=e['word'][step] or corner:return False
  pos=tuple(pos[j]+tau*v[j] for j in (0,1));R,b=ref(i);v=tuple(sum(R[j][k]*v[k] for k in (0,1)) for j in (0,1))
 return False
if __name__=='__main__':
 events=json.loads((B/'events.json').read_text());stats=Counter();bad=[]
 for i,e in enumerate(events):
  g=list(map(F,e['gradient']));p=list(g)
  for c,k in zip(C,pivots):
   v=p[k];p=[a-v*b for a,b in zip(p,c)]
  d=make_delta([-x for x in p])
  if not dot(g,d):stats['boundary_normal_only_skipped']+=1;continue
  assert dot(g,d)<0
  if not replay(e,move(d)):bad.append(dict(event=i,control='descent'))
  stats['event_specific_descents']+=1
 rng=random.Random(20261031)
 for trial in range(2):
  d=make_delta([rng.randrange(-9,10) for _ in range(r.dim)])
  if trial==1:
   d=list(d);normal=boundary_model.boundary_row()[2]
   for j in (0,1):d[r.W+4+j]+=normal[j]
   assert dot(boundary_row,d)>0
  z=move(d)
  for i,e in enumerate(events):
   v=dot(map(F,e['gradient']),d)
   if not v:stats['tangent_skipped']+=1;continue
   actual=replay(e,z);expected=v<0;stats['further_predictions']+=1
   stats['predicted_lit' if expected else 'predicted_word_invalid']+=1
   if actual!=expected:bad.append(dict(trial=trial,event=i,expected=expected,actual=actual))
 out=dict(status='PASS' if not bad else 'FAIL',checks=dict(stats),mismatches=bad,scope='Individual prescribed words only. A failed word is not a claim of room darkness.')
 (B/'validate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
