"""Replay fixed mixed-angle event directions, independently of peer executables."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import importlib.util,json,math
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('room24_algebra',B/'check.py');geom=importlib.util.module_from_spec(spec);spec.loader.exec_module(geom)
spec=importlib.util.spec_from_file_location('codex_infinitesimals',B.parent/'check.py');dual=importlib.util.module_from_spec(spec);spec.loader.exec_module(dual)
D=dual.D;cross=geom.cross;dot=geom.dot;vertices=geom.vertices;dirs=geom.directions;rows=geom.rows;DIM=30;theta=tuple(map(F,geom.scale));s0,t0=map(tuple,geom.room['marked'])
def unit(i):return tuple(F(j==i) for j in range(DIM))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def times(k,a):return tuple(k*x for x in a)
def pointvalue(p):return tuple(dot(x,theta) for x in p)
def canon(r):
 den=math.lcm(*(F(x).denominator for x in r));ints=[int(x*den) for x in r];g=math.gcd(*ints)
 return tuple(x//g for x in ints)
vforms=[];p=(unit(0),unit(1))
for i,d in enumerate(dirs):
 vforms.append(p);p=tuple(add(p[j],times(d[j],unit(2+i))) for j in (0,1))
assert all(pointvalue(p)==v for p,v in zip(vforms,vertices))
sform=(unit(26),unit(27));tform=(unit(28),unit(29));ZERO=(F(0),)*DIM

def matrix_product(A,C):return tuple(tuple(sum(A[i][k]*C[k][j] for k in (0,1)) for j in (0,1)) for i in (0,1))
def mapped(O,shift,p):return tuple(add(add(times(O[i][0],p[0]),times(O[i][1],p[1])),shift[i]) for i in (0,1))
def refl(i):
 d=dirs[i];n=(-d[1],d[0]);nn=dot(n,n)
 R=tuple(tuple(F(int(a==b))-F(2*n[a]*n[b],nn) for b in (0,1)) for a in (0,1))
 c=add(times(n[0],vforms[i][0]),times(n[1],vforms[i][1]));b=tuple(times(F(2*n[j],nn),c) for j in (0,1))
 return R,b

def trace(q,side,maxhits=2000):
 pos=tuple(D(c) for c in s0);velocity=(D(q[0],-side*q[1]),D(q[1],side*q[0]));O=((F(1),F(0)),(F(0),F(1)));shift=(ZERO,ZERO);word=[];corner=None;cornerimage=None;reflections=0
 for hit in range(maxhits):
  candidates=[]
  for i,(a,b) in enumerate(zip(vertices,vertices[1:]+vertices[:1])):
   e=dirs[i];n=(-e[1],e[0]);den=n[0]*velocity[0]+n[1]*velocity[1]
   if not den.a:continue
   tau=(dot(n,a)-(n[0]*pos[0]+n[1]*pos[1]))/den
   if tau<=0:continue
   at=tuple(pos[j]+tau*velocity[j] for j in (0,1));along=sum((at[j]-a[j])*e[j] for j in (0,1));length=dot(geom.steps[i],e)
   if 0<=along<=length:candidates.append((tau,i))
  if not candidates:return dict(status='NO_WALL')
  tau,i=min(candidates,key=lambda r:r[0]);pv=tuple(p.a for p in pos);dv=tuple(v.a for v in velocity);axis=next(j for j in (0,1) if dv[j]);delta=sub(t0,pv)
  target=not cross(delta,dv) and 0<delta[axis]/dv[axis]<tau.a
  end=delta[axis]/dv[axis] if target else tau.a
  crossed=[]
  for j,v in enumerate(vertices):
   vd=sub(v,pv)
   if not cross(vd,dv):
    mu=vd[axis]/dv[axis]
    if 0<mu<=end:crossed.append((mu,j))
  for mu,j in sorted(crossed):
   image=mapped(O,shift,vforms[j])
   if corner is None:corner=vertices[j];cornerimage=image
   elif pointvalue(image)!=pointvalue(cornerimage):return dict(status='SECOND_CORNER')
  if target:
   if corner is None:return dict(status='ORDINARY_TARGET')
   lifted=mapped(O,shift,tform);A=tuple(sub(lifted[j],sform[j]) for j in (0,1));C=tuple(sub(cornerimage[j],sform[j]) for j in (0,1));av=pointvalue(A);cv=pointvalue(C)
   assert not cross(av,cv) and 0<dot(av,cv)<dot(av,av)
   g=tuple(side*(A[0][j]*cv[1]+av[0]*C[1][j]-A[1][j]*cv[0]-av[1]*C[0][j]) for j in range(DIM))
   return dict(status='EVENT',direction=q,perturb_side=side,corner=corner,word=word,gradient=list(map(str,g)),row=canon(g),unfolded_target_minus_s=list(map(str,av)),corner_reflections=reflections)
  pos=tuple(pos[j]+tau*velocity[j] for j in (0,1));R,b=refl(i)
  if tuple(x.a for x in pos)==corner:reflections+=1
  velocity=tuple(sum(R[j][k]*velocity[k] for k in (0,1)) for j in (0,1));shift=mapped(O,shift,b);O=matrix_product(O,R);word.append(i)
 return dict(status='CAP')

if __name__=='__main__':
 given=json.loads((B/'inputs/events-room-illumination-search-simple-unrestricted-R12.json').read_text())['rows'];qs=sorted({tuple(e['dir']) for e in given});events=[];other=Counter()
 for q in qs:
  for side in (-1,1):
   r=trace(q,side)
   if r['status']=='EVENT':events.append(r)
   else:other[r['status']]+=1
 found={tuple(e['row']):e for e in events};expected={canon(r) for r in rows};matches=[]
 for i,r in enumerate(rows):
  key=canon(r)
  if key not in found:continue
  e=found[key];g=given[i];assert list(e['direction'])==g['dir'] and list(e['corner'])==g['corner']
  assert e['unfolded_target_minus_s']==g['unfolded_target_minus_s']
  matches.append(i)
 out=dict(status='PASS' if len(matches)==len(rows) else 'INCOMPLETE',supplied_directions=len(qs),sides=2*len(qs),reconstructed_events=len(events),supplied_rows=len(rows),rows_matched=len(matches),own_only=len(set(found)-expected),peer_only=len(expected-set(found)),other_limits=dict(other),rank_on_closure=geom.rank([*geom.closure,*[list(map(F,e['gradient'])) for e in events]])-2,positive_span='Previously independently checked on matched rows; PASS only with complete geometric association.')
 (B/'events.json').write_text(json.dumps(events,indent=2,default=lambda x:int(x) if x.denominator==1 else str(x))+'\n');(B/'replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
