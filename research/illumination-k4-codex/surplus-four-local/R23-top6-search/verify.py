"""Review two supplied paths only. No search or new room construction.
Independent Fraction geometry; imports no peer or historical geometry code.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
import json, hashlib
BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PEER=BASE/'fourth-surplus-review'
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def tri(t): return tuple(sorted(t))
def ccw(t):
 a,b,c=t
 return (a,b,c) if cross(sub(b,a),sub(c,a))>0 else (a,c,b)
def fan(a,ss):
 if isinstance(a,str): a=C[a]
 return {tri((a,(a[0]+R[i][0],a[1]+R[i][1]),(a[0]+R[(i+1)%8][0],a[1]+R[(i+1)%8][1]))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
# Finite local tiling universe only for incidence tests, not room generation.
TILES=set().union(*(fan((x,y),range(8)) for x in range(-6,9,2) for y in range(-6,9,2)))
def signs(p,t):
 t=ccw(t)
 return [cross(sub(t[(i+1)%3],t[i]),sub(p,t[i])) for i in range(3)]
def incident(p): return {t for t in TILES if min(signs(p,t))>=0}
def on(p,a,b): return cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<=0
def edge_times(a,b,c,d):
 v=sub(b,a);w=sub(d,c);den=cross(v,w)
 if den:
  t=F(cross(sub(c,a),w),den);u=F(cross(sub(c,a),v),den)
  return [t] if 0<=t<=1 and 0<=u<=1 else []
 if cross(sub(c,a),v):return []
 k=0 if v[0] else 1
 return [F(p[k]-a[k],v[k]) for p in (c,d) if on(p,a,b)]
def reflect(v,a,b):
 w=sub(b,a)
 return tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
def constraints(P,walls):
 used=set();absent=set();events=[]
 for a,b in zip(P,P[1:]):
  times={F(0),F(1)}
  for t in TILES:
   for c,d in zip(t,t[1:]+t[:1]):times.update(edge_times(a,b,c,d))
  times=sorted(times);samples=times[1:-1]+[(l+h)/2 for l,h in zip(times,times[1:])]
  for s in samples:
   p=tuple(a[k]+s*(b[k]-a[k]) for k in (0,1));used.update(incident(p))
  events.append(len(times)-2)
 for before,p,after,(a,b) in zip(P,P[1:],P[2:],walls):
  assert on(p,a,b) and p not in (a,b)
  v=reflect(sub(p,before),a,b);w=sub(after,p)
  assert cross(v,w)==0 and dot(v,w)>0
  side=cross(sub(b,a),sub(before,p));assert side
  assert side*cross(sub(b,a),sub(after,p))>0
  for t in incident(p):
   ss=[cross(sub(b,a),sub(q,p)) for q in t]
   assert min(ss)>=0 or max(ss)<=0
   s=sum(ss);assert s
   (used if s*side>0 else absent).add(t)
 assert not used&absent
 return used,absent,events
sigma=lambda p:(2-p[1],2-p[0])
def transform(ts):return {tri(tuple(sigma(p) for p in t)) for t in ts}
def audit(P,walls,minimum,maximum,target):
 assert P[0]==(0,0) and P[-1]==(2,2)
 for a,b in zip(P[:-2],P[1:-1]):assert not on((2,2),a,b)
 U,Z,events=constraints(P,walls)
 assert U<=minimum and not Z&maximum
 ur,zr,_=constraints(P[::-1],walls[::-1]);assert (ur,zr)==(U,Z)
 ps=[sigma(p) for p in P[::-1]];ws=[(sigma(a),sigma(b)) for a,b in walls[::-1]]
 us,zs,_=constraints(ps,ws);assert (us,zs)==(transform(U),transform(Z))
 # Independent specular checks above also cover reverse and sigma paths.
 q=P[-1]
 for a,b in walls[::-1]:
  v=reflect(sub(q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
 assert q==target
 return U,Z,{'reflections':len(walls),'required_count':len(U),'forbidden_count':len(Z),'segment_internal_edge_events':events,'unfolded_target':q,'forward_reverse_sigma':'PASS'}
def boundary(room):
 edges=Counter()
 for t in room:
  t=ccw(t)
  for a,b in zip(t,t[1:]+t[:1]):edges[(a,b)]+=1
 edge={e for e in edges if not edges[(e[1],e[0])]}
 nxt=defaultdict(list)
 for a,b in edge:nxt[a].append(b)
 assert all(len(v)==1 for v in nxt.values())
 p=min(nxt);start=p;cycle=[]
 while True:
  assert p not in cycle;cycle.append(p);p=nxt[p][0]
  if p==start:break
 assert len(cycle)==len(edge)
 return [p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
def inside(p,V):
 if any(on(p,a,b) for a,b in zip(V,V[1:]+V[:1])):return False
 n=0
 for a,b in zip(V,V[1:]+V[:1]):
  if (a[1]>p[1])!=(b[1]>p[1]):
   x=a[0]+F(p[1]-a[1],b[1]-a[1])*(b[0]-a[0]);n+=x>p[0]
 return n%2==1
def physical(P,V):
 for i,(a,b) in enumerate(zip(P,P[1:])):
  assert inside(tuple((a[k]+b[k])/2 for k in (0,1)),V)
  hits=[]
  for c,d in zip(V,V[1:]+V[:1]):
   for s in edge_times(a,b,c,d):
    if s>0:hits.append((s,c,d))
  if i==len(P)-2:assert not hits
  else:
   assert hits and min(h[0] for h in hits)==1
   hit=[h for h in hits if h[0]==1];assert len(hit)==1 and b not in V
   _,c,d=hit[0];v=reflect(sub(b,a),c,d);w=sub(P[i+2],b)
   assert cross(v,w)==0 and dot(v,w)>0

def path(d,nine):
 P=[(F(0),F(0)),(2*d/(1+d),2/(1+d)),(F(0),2-2*d),(2*d/(1-d),2-2*d/(1-d))]
 if nine:P +=[(4*d/(1-d),-4*d/(1-d)),(F(2),-6*d),(8*d/(1+d),-8*d/(1+d))]
 else:P +=[(5*d,F(-1))]
 k=16 if nine else 14
 P +=[((k-5)*d,F(3)),(k*d/(1+d),k*d/(1+d)-2),(F(1),(k-1)*d-2),(F(2),k*d-2)]
 return P
# Search-independent Fraction replay of ONLY the stopped candidate.
HERE=Path(__file__).resolve().parent
raw=json.loads((HERE/'room.json').read_text());result=json.loads((HERE/'result.json').read_text())
assert result['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
assert result['room_sha256']==hashlib.sha256((HERE/'room.json').read_bytes()).hexdigest()
assert result['search_source_sha256']==hashlib.sha256((HERE/'search.py').read_bytes()).hexdigest()
P=[tuple(F(*x) for x in p) for p in result['candidate']['path']]
assert P==[(F(0),F(0)),(F(-1),F(-1,2)),(F(1),F(-3,2)),(F(0),F(-2)),(F(2),F(2))]
assert result['candidate']['initial_direction']==[-2,-1] and result['candidate']['reflections']==3
room={tri(tuple(map(tuple,t))) for t in raw['triangles']}
assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=boundary(room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
physical(P,V);physical(P[::-1],V)
physical([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
# Actual third hit is INSIDE one maximal straight mirror, not a vertex.
assert (0,-2) not in V
containing=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on((0,-2),a,b)]
assert len(containing)==1
assert set(containing[0])=={(-1,-1),(1,-3)}
assert P[3] not in containing[0]
walls=[((-1,-1),(-1,0)),((1,-2),(1,-1)),((-1,-1),(1,-3))]
minimum=H|fan('B',[7,0,1,2])
maximum=minimum|fan('L',[0,1,2,3,4,5,6])|fan('D',[0,1,2,4,5,6,7])|set().union(*(fan(k,range(8)) for k in ['R','E','Tc','N']))
U,Z,proof=audit(P,walls,minimum,maximum,(-8,-4))
assert minimum<=room<=maximum and U<=room and not Z&room
assert Z==fan('L',[7])|fan('D',[3])|fan('B',[3,4,5,6])
assert not (U|Z)&fan('R',range(8))
assert incident((F(0),F(-1)))<=minimum
assert on((0,-1),P[1],P[2])
assert incident((F(1),F(0)))<=H and on((1,0),P[3],P[4])
# Recompute physical frozen-room J, sN, full A and local corner angles.
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[sub(q,p) for q in t if q!=p];n+=90 if dot(a,b)==0 else 45
 return n
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
J=sum(angle(room,p)==360 for p in pts-A);sN=sum(angle(room,p)==180 for p in pts-A)
assert (J,sN)==(3,3) and angle(room,(0,-2))==180
# The actual source and target are fixed, and are reached in the right order.
d=F(1,2);assert F(3,7)<d<F(5,8)
q=((4*d-2)/(1+d),-6*d/(1+d))
assert P==[(F(0),F(0)),(F(-1),-d),(F(1),-3*d),q,(8*d-2,F(2))]
assert 8*d-2==2
assert -1<-d<0 and -2<-3*d<-1 and -1<q[0]<1
assert 1<7*d-2<3
# Whole partner-independent H4 support envelope, no additional room built.
applications=[]
for name,site,sectors in [('Louter01','L',[0,1]),('EC','E',[3,4]),('EO','E',[4,5]),('D01','D',[0,1]),('D12','D',[1,2]),('R23','R',[2,3]),('R34','R',[3,4]),('R45','R',[4,5]),('N70','N',[7,0])]:
 mi=minimum|fan(site,sectors);ma=maximum
 assert U<=mi and not Z&ma and mi<=ma
 applications.append({'unit':name,'whole_family':'fits H4 minimum and L7/D3/B3..6-absent maximum','reflections':3})
# A D4-only leaf also fits the broad envelope; peer owns its mixed dispatch.
assert U<=minimum|fan('D',[4]) and not Z&(maximum|fan('D',[4]))
# H4+LC is excluded at b1 by two unhealable smooth non-A points.
LC=fan('L',[7,0]);assert angle(minimum|LC,(1,-2))==180 and angle(minimum|LC,(-1,-1))==180
# D23's surviving partner class has an independently accepted 4/6 split.
prior=BASE/'surplus-four-local/joined-six-review/check.json';old=json.loads(prior.read_text())
assert old['status']=='PASS'
for r in old['whole_family_applications']:
 if r['B']=='H4' and r['condition'].startswith('D23'):assert r['reflections'] in [4,6]
receipt={'status':'FROZEN_ONE_ROOM_THREE_PATH_AND_WHOLE_SUPPORT_PASS','physical_frozen_room':{'walls':20,'J':J,'s_N':sN,'full_A':'S,U,T','third_hit':'(0,-2),strict inside maximal wall(-1,-1)--(1,-3),angle180','first_wall_firstT_reverse_sigma':'PASS'},'path':[[str(x) for x in p] for p in P],'reflections':3,'initial_direction':[-2,-1],'hand_parameter':'1/2','endpoint_equation':'8d-2=2','sufficient_gate':['3/7','5/8'],'whole_support':{'minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z)},'optical_proof':proof,'applications':applications,'conditional_H4_b1_closure':'New3 covers every remaining partner except LC (two smooth points, impossible at b1) and D23 (accepted four/six ordinaryTc cover). Thus entire H4 two-root b1 <=6, pending independent HAND review.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'room.json',HERE/'result.json',HERE/'search.py',prior,BASE/'surplus-four-local/e2-e1-b1/critical-B.txt',BASE/'fourth-surplus-review/peer-critical-B-b1-independent/review.txt']},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE explicitly authorized fixed-room discovery, stopped after9directions at first candidate. Standalone own Fraction verifier imports no search/peer geometry. No additional room, direction search, archive or worker. Whole support extrema are conditional, not rooms. Parent exact verification and hand proof; independent peer review pending, no full Delta4/universal claim.'}
(HERE/'verification.json').write_text(json.dumps(receipt,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['source_sha256','checker_sha256','whole_support','applications']},indent=2,default=str))
