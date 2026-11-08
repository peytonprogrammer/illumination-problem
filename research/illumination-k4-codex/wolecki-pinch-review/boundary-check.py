"""Exact finite-word audit near the contact; no direction discovery."""
from pathlib import Path
from fractions import Fraction as F
import json
from check import PinchModel,load,rationals,rank,dot,sub,cross,matmul,canon
B=Path(__file__).resolve().parent
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
  C=images[0][1];area=sum(cross(a,b) for a,b in zip(model.vertices,model.vertices[1:]+model.vertices[:1]));j=model.vertices.index(tuple(e['corner']));turn=cross(sub(model.vertices[j],model.vertices[j-1]),sub(model.vertices[(j+1)%model.W],model.vertices[j]));assert area*turn!=0
  incoming=sub(model.vertices[j-1],model.vertices[j]);outgoing=sub(model.vertices[(j+1)%model.W],model.vertices[j])
  # Nonregular convex 135-degree corners also generate one-sided events.
  assert not (dot(incoming,outgoing)==0 and area*turn>0)
  assert not (dot(incoming,outgoing)>0 and area*turn>0)
  def polynomial(z):return cross(tuple(dot(a,z) for a in A),tuple(dot(c,z) for c in C))
  assert polynomial(model.theta)==0
  gradient=[]
  for j in range(model.dim):
   plus=tuple(x+int(i==j) for i,x in enumerate(model.theta));minus=tuple(x-int(i==j) for i,x in enumerate(model.theta))
   gradient.append(e['perturb_side']*(polynomial(plus)-polynomial(minus))/2)
  assert gradient==list(map(F,e['gradient'])) and canon(gradient)==tuple(e['row'])
 return True


def pinch_clearance(model,e,labels):
 O=((F(1),F(0)),(F(0),F(1)));shift=(model.zero,model.zero)
 for i in e['word']:
  R,b=model.reflectors[i];shift=model.mapped(O,shift,b);O=matmul(O,R)
 target=model.value(model.mapped(O,shift,model.tform));av=sub(target,model.s);aa=dot(av,av)
 O=((F(1),F(0)),(F(0),F(1)));shift=(model.zero,model.zero);lower=F(0);clearances=[]
 for i in [*e['word'],None]:
  if i is None:upper=F(1)
  else:
   n=(-model.dirs[i][1],model.dirs[i][0]);nu=tuple(sum(O[j][k]*n[k] for k in (0,1)) for j in (0,1));wv=model.value(model.mapped(O,shift,model.vforms[i]));upper=dot(nu,sub(wv,model.s))/dot(nu,av)
  assert 0<=lower<=upper<=1
  for k in labels:
   pv=sub(model.value(model.mapped(O,shift,model.vforms[k])),model.s)
   mu=max(lower,min(upper,dot(av,pv)/aa));difference=tuple(mu*av[j]-pv[j] for j in (0,1));distance2=dot(difference,difference)
   assert distance2>0,(e['index'],i,k)
   clearances.append(distance2)
  lower=upper
  if i is not None:
   R,b=model.reflectors[i];shift=model.mapped(O,shift,b);O=matmul(O,R)
 return min(clearances),len(clearances)

def simple(vs):
 def orientation(a,b,c):return cross(sub(b,a),sub(c,a))
 for i,(a,b) in enumerate(zip(vs,vs[1:]+vs[:1])):
  assert a!=b
  for j,(c,d) in enumerate(zip(vs,vs[1:]+vs[:1])):
   if j<=i or j==i+1 or (i==0 and j==len(vs)-1):continue
   bbox=all(max(min(a[k],b[k]),min(c[k],d[k]))<=min(max(a[k],b[k]),max(c[k],d[k])) for k in (0,1))
   assert not(bbox and orientation(a,b,c)*orientation(a,b,d)<=0 and orientation(c,d,a)*orientation(c,d,b)<=0),(i,j)
 return True

def evalpt(p,z):return tuple(dot(a,z) for a in p)

def room_at(z):
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
   assert cross(sub(b,a),sub(p,a)) or not all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))
   if (a[1]>p[1])!=(b[1]>p[1]):
    if a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])>p[0]:odd=not odd
  return odd
 s,t=evalpt(r.sform,z),evalpt(r.tform,z);assert inside(s) and inside(t);return vs,s,t

def replay(e,z):
 vs,s,t=room_at(z);O=((F(1),F(0)),(F(0),F(1)));shift=(F(0),F(0))
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
   if 0<mu<tau:return step==len(e['word'])
  if step==len(e['word']) or i!=e['word'][step] or corner:return False
  pos=tuple(pos[j]+tau*v[j] for j in (0,1));R,b=ref(i);v=tuple(sum(R[j][k]*v[k] for k in (0,1)) for j in (0,1))
 return False

if __name__=='__main__':
 model=PinchModel(load('room-wolecki22-pinch.json'));r=model;r.matrix_product=matmul;labels=[i for i,v in enumerate(model.vertices) if v==tuple(model.room['pinch'])];replayed=json.loads((B/'replayed-events.json').read_text());cases=[]
 for radius,events in replayed.items():
  geometry_and_gradients(model,events)
  clearances=[pinch_clearance(model,e,labels) for e in events]
  cases.append(dict(radius=int(radius),events=len(events),derivative_coordinates=len(events)*model.dim,pinch_distance_checks=sum(n for d,n in clearances),minimum_squared_pinch_clearance=str(min(d for d,n in clearances))))
 # Tip separation is unrestricted in the closure-only chart.
 tiprows=[sub(model.vforms[labels[0]][j],model.vforms[labels[1]][j]) for j in (0,1)]
 assert rank([*model.closure,*tiprows])-rank(model.closure)==2
 # Explicit simple opening: shorten edge6, lengthen edge8 equally.
 delta=[F(0)]*model.dim;delta[2+6]=-1;delta[2+8]=1
 assert all(dot(c,delta)==0 for c in model.closure)
 epsilon=F(1,100);z=tuple(a+epsilon*d for a,d in zip(model.theta,delta));vs=[tuple(dot(f,z) for f in p) for p in model.vforms]
 assert all(z[2+i]>0 for i in range(model.W)) and simple(vs)
 assert vs[7]!=vs[10]
 values=[dot(tuple(map(F,e['gradient'])),delta) for e in replayed['12']];assert min(values)<0
 predictions=0;lit=0
 for e,value in zip(replayed['12'],values):
  if not value:continue
  actual=replay(e,z);assert actual==(value<0),(e['index'],value,actual)
  predictions+=1;lit+=actual
 assert lit>0
 control=dict(status='SIMPLE_OPENING_WITH_CERTIFICATE_DESCENT',epsilon=str(epsilon),delta=list(map(str,delta)),tip_positions=[list(map(str,vs[i])) for i in labels],negative_event_indices=[i for i,v in enumerate(values) if v<0],exact_word_predictions=predictions,exact_lighting_words=lit,scope='Explicit simple opening and exact replay of frozen words. No new ray search.')
 (B/'opening-control.json').write_text(json.dumps(control,indent=2)+'\n')
 result=dict(status='PASS',cases=cases,free_tip_difference_rank=2,opening_control=control['status'],scope='Frozen word geometry, exact gradients and clearance from both contact labels. Supports persistence of each event under free-tip deformations; global/no-other-shape claims excluded.')
 (B/'boundary-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
