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
# Review ONLY the frozen two-reflection witness. Geometry routines above
# are reused from our own helper-free nine/seven independent review.
P=[(F(0),F(0)),(F(-1),F(-3,2)),(F(-2,3),F(-2)),(F(2),F(2))]
walls=[((-1,-2),(-1,-1)),((-1,-2),(0,-2))]
minimum=H|fan('B',[1,2,3])
maximum=H|fan('B',[0,1,2,3,5,6,7])|set().union(*(fan(k,range(8)) for k in C if k!='B'))
U,Z,result=audit(P,walls,minimum,maximum,(-4,-6))
source=PEER/'N7-single-room-search'
raw=json.loads((source/'room.json').read_text())
room={tri(tuple(map(tuple,t))) for t in raw['triangles']}
assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=boundary(room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
physical(P,V);physical(P[::-1],V)
physical([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
assert minimum<=room<=maximum
assert incident((F(0),F(-1)))<=minimum and inside((F(0),F(-1)),V)
assert on((0,-1),P[2],P[3])
# Independently identify exactly two forbidden triangles and their A owner.
expected={tri(((-2,-2),(-1,-2),(-1,-1))),tri(((0,-2),(-1,-2),(-1,-3)))}
assert Z==expected
assert Z&fan('B',[4]) and not Z&fan('B',[0,5,6,7])
# Exact symbolic-family implications, never completed rooms or a census.
applications={}
for label,ss in [('Bwest',[1,2,3]),('Brectangle',[0,1,2,3])]:
 mi=H|fan('B',ss);ma=mi|set().union(*(fan(k,range(8)) for k in C if k!='B'))
 assert U<=mi and not Z&ma
 applications[label]='ALL other six K stars allowed'
# Sigma sends B123 to E234 and B0123 to E2345.
assert transform(fan('B',[1,2,3]))==fan('E',[2,3,4])
assert transform(fan('B',[0,1,2,3]))==fan('E',[2,3,4,5])
assert transform(H)==H
# Two-root b1 e2-at-B windows, exactly the seven in argument.txt.
# These are named local fan implications, NOT completed-room enumeration.
window_status={}
for label,ss in [('701',[7,0,1]),('012',[0,1,2]),('123',[1,2,3]),('6701',[6,7,0,1]),('7012',[7,0,1,2]),('0123',[0,1,2,3]),('1234',[1,2,3,4])]:
 mi=H|fan('B',ss)
 window_status[label]={'required_present':U<=mi,'forbidden_present':bool(Z&mi),'covered':U<=mi and not Z&mi}
assert {k for k,v in window_status.items() if v['covered']}=={'123','0123'}
# Existing eight critical-L inward descriptions have B1, B12 or B01,
# and E4 or E34. Check these five named local support obstructions only.
for ss in [[1],[1,2],[0,1]]:
 assert not U<=H|fan('B',ss)|set().union(*(fan(k,range(8)) for k in C if k!='B'))
for ss in [[4],[3,4]]:
 assert not transform(U)<=H|fan('E',ss)|set().union(*(fan(k,range(8)) for k in C if k!='E'))
rec=json.loads((source/'verification.json').read_text())
def decode(x):return {tri(tuple(map(tuple,t))) for t in x}
assert U==decode(rec['required']) and Z==decode(rec['forbidden'])
assert P==[tuple(F(x) for x in p) for p in rec['path']]
search=json.loads((source/'result.json').read_text())
assert P==[tuple(F(*x) for x in p) for p in search['candidate']['path']]
assert hashlib.sha256((source/'room.json').read_bytes()).hexdigest()==search['room_sha256']
# Frozen room angle ledger. Strict simple boundary is inherited; full local
# angles and a single oriented boundary cycle are independently checked.
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[q for q in t if q!=p];n+=90 if dot(sub(a,p),sub(b,p))==0 else 45
 return n
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
J=sum(angle(room,p)==360 for p in pts-A);sN=sum(angle(room,p)==180 for p in pts-A)
assert (J,sN,J+sN)==(5,1,6)
paths=[source/n for n in ['findings.txt','room.json','result.json','verification.json','verify.py']]+[BASE/'surplus-four-local/e2-e1-b1'/n for n in ['argument.txt','critical-L.txt']]+[BASE/'surplus-four-local/nine-seven-review/check.py']
receipt={'status':'PASS','optical_lemma':result,'frozen_room':{'walls':20,'J':J,'s_N':sN,'interior_A':'S,U,T','physical_first_wall_forward_reverse_sigma':'PASS'},'interior_C_0_minus1':'PASS all incident triangles required/present','whole_families':applications,'b1_named_B_windows':window_status,'b1_critical_L_eight_inward':'No new removal: B1/B12/B01 and E4/E34 lack required support','sigma_correspondence':'B123->E234; B0123->E2345','required':sorted(U),'forbidden':sorted(Z),'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'No classification completeness re-audit, no new room, no discovery, no peer checker execution. Same own geometry engine as preceding review.'}
(OUT/'check.json').write_text(json.dumps(receipt,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['required','forbidden','source_sha256','checker_sha256']},indent=2,default=str))
