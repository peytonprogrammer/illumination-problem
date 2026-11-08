"""Independent fixed eights, one supplied polygon, whole-support transfers.
No peer execution/import, new room, direction/word discovery or archive scan.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident
from boundary_replay import replay,on,sub,cross,dot
import illumination_geometry as geo
reads=[]
def read(p):reads.append(p);return json.loads(p.read_text())
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(k,ss):
 a=C[k] if isinstance(k,str) else k
 return {tuple(sorted((a,tuple(a[j]+R[i%8][j] for j in (0,1)),tuple(a[j]+R[(i+1)%8][j] for j in (0,1))))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(full(p) for p in ((0,0),(2,0),(2,2))))
allK=H|set().union(*(full(k) for k in C))
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
def fp(xs):return [tuple(F(x) for x in p) for p in xs]
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[sub(v,p) for v in t if v!=p];n+=90 if dot(a,b)==0 else 45
 return n
def provenance(receipt,path):
 for rel,digest in receipt['source_sha256'].items():
  p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,rel
 p=path.parent/'verify.py';reads.append(p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['checker_sha256']
records={}
def optical(name,P,walls,mi,ma,image,parent):
 u,z=path_requirements(P)
 assert u<=mi and not z&ma,(name,u-mi,z&ma)
 assert P[0]==(0,0) and P[-1]==(2,2)
 assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
 for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
  assert on(p,c,e) and p not in (c,e),(name,p)
  v=sub(p,a);w=sub(e,c)
  ref=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
  assert cross(ref,sub(b,p))==0 and dot(ref,sub(b,p))>0
 assert len(walls)==len(P)-2
 a,b=path_requirements(P[::-1]);assert (a,b)==(u,z)
 a,b=path_requirements([sigma(p) for p in P[::-1]]);assert (a,b)==(tr(u),tr(z))
 q=P[-1]
 for a,b in walls[::-1]:
  w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert q==image,(name,q,image)
 if parent is not None:
  assert u==decode(parent['required']) and z==decode(parent['forbidden'])
  assert mi==decode(parent['minimum']) and ma==decode(parent['maximum'])
 records[name]={'path':[[str(x) for x in p] for p in P],'reflections':len(P)-2,'U':len(u),'Z':len(z),'unfold':list(map(str,q)),'required':sorted(u),'forbidden':sorted(z),'minimum':sorted(mi),'maximum':sorted(ma)}
 return u,z
# Explicit expected hypotheses and forbidden sectors, independently transcribed
# from the five mathematical statements, not inferred from peer output.
configs=[
 ('R34-centered-search',2,10,2,H|fan('R',[3,4]),fan('D',[1])|fan('R',[2]),(8,2),F(1,4),(F(1,5),F(1,3)),'horizontal'),
 ('R23-square-seven',7,22,5,H|fan('B',[1,2])|fan('R',[2,3])|fan('N',[7]),fan('L',[7])|fan('B',[0])|fan('R',[1])|fan('N',[0,6]),(4,16),F(1,4),(F(3,13),F(4,15)),'vertical'),
 ('E34-centered-search',6,17,6,H|fan('B',[1,2,3,4])|fan('E',[3,4]),fan('B',[0,5,6,7])|fan('E',[2])|fan((-2,-2),[7]),(16,12),F(3,4),(F(749,1000),F(751,1000)),'horizontal'),
 ('N70-center-three',3,11,3,H|fan('N',[7,0]),fan('R',[3])|fan('N',[1,6]),(8,2),F(1,4),(F(1,5),F(2,7)),'horizontal'),
 ('N70-Tc6-search',8,23,6,H|fan('B',[1,2])|fan('R',[3])|fan('N',[7,0]),fan('L',[7])|fan('B',[0])|fan('R',[2,4])|fan('N',[1,6]),(4,16),F(1,4),(F(3,13),F(4,15)),'vertical')]
def ev(a,d):return a[0]+a[1]*d
def mul(a,b):return(a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[1]*b[1])
def eqratio(a,b,c,e):return mul(a,e)==mul(c,b)
summaries=[]
for name,n,nu,nz,mi,expectedZ,image,root,(lo,hi),launch in configs:
 q=ROOT/'surplus-four-remote2110'/name
 g=read(q/('verification.json' if (q/'verification.json').exists() else 'check.json'))
 for rel,h in g['source_sha256'].items():
  p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==h,rel
 reads += [q/'argument.txt',q/'coverage.txt',q/('verify.py' if (q/'verify.py').exists() else 'check.py')]
 P=fp(g['path']);ma=(allK|full((-2,-2)))-expectedZ
 if 'walls' in g:walls=[[tuple(map(F,a)),tuple(map(F,b))]for a,b in g['walls']]
 elif n==7:walls=fp([]) or [((0,1),(1,1)),((0,-2),(1,-1)),((-1,-1),(-1,0)),((4,0),(4,1)),((0,2),(1,1)),((0,2),(1,2)),((0,2),(1,1))]
 else:walls=[((3,0),(3,1)),((0,2),(1,1)),((0,2),(1,3))]
 walls=[[tuple(map(F,a)),tuple(map(F,b))]for a,b in walls]
 u,z=optical(name,P,walls,mi,ma,image,g)
 assert(len(P)-2,len(u),len(z))==(n,nu,nz)and z==expectedZ
 assert all(not on((0,0),a,b)for a,b in zip(P[1:],P[2:]))
 # Minimum is strict for full fan; remove either half and the open-leg
 # lattice crossing is a genuine boundary event. Check connected full stars.
 portal={'R34-centered-search':(3,0),'E34-centered-search':(3,2)}.get(name)
 if portal:
  assert incident(portal)<=mi and angle(mi,portal)==360
  assert any(on(portal,a,b) and portal not in(a,b)for a,b in zip(P,P[1:]))
  half='R' if n==2 else 'E';assert angle(mi-fan(half,[4]),portal)==270
 if (q/'room.json').exists():
  raw=read(q/'room.json');room=decode(raw['triangles']);V=list(map(tuple,raw['vertices']))
  assert len(room)==35 and len(V)==20 and mi<=room<=ma
  assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==n
  assert replay([sigma(p)for p in V],(0,0),(2,2),[sigma(p)for p in P[::-1]])==n
  edges={e for e,owners in geo.owners_of(sorted(room)).items()if len(owners)==1};adj=defaultdict(list)
  for a,b in edges:adj[a].append(b);adj[b].append(a)
  assert all(len(v)==2 for v in adj.values());cycle=[min(adj)];prev=None;v=cycle[0]
  while True:
   w=next(p for p in adj[v]if p!=prev)
   if w==cycle[0]:break
   assert w not in cycle;cycle.append(w);prev,v=v,w
  assert len(cycle)==len(edges)
  verts=[p for i,p in enumerate(cycle)if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))];assert set(verts)==set(V)
  for i,(a,b)in enumerate(zip(V,V[1:]+V[:1])):
   for j,(c,e)in enumerate(zip(V,V[1:]+V[:1])):
    if i<j and j-i not in(1,len(V)-1):
     den=cross(sub(b,a),sub(e,c))
     if den:assert not(0<=F(cross(sub(c,a),sub(e,c)),den)<=1 and 0<=F(cross(sub(c,a),sub(b,a)),den)<=1)
     else:assert not any((on(c,a,b),on(e,a,b),on(a,c,e),on(b,c,e)))
  pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
  assert{p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
  assert sum(angle(room,p)==360 for p in pts-A)==4 and sum(angle(room,p)==180 for p in pts-A)==2
 # Independent reflected SOURCE and VELOCITY transport gives every contact
 # as a rational function of the launch slope, with actual forward times.
 hand=read(q/'hand.json') if (q/'hand.json').exists() else None
 if hand:
  for file,h in hand['source_sha256'].items():
   p=q/file;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==h
  reads.append(q/'hand.py');assert root==F(hand['root'])
  assert [lo,hi]==list(map(F,hand['strict_sufficient_finite_wall_gate']))
 O=(F(0),F(0));Vd=[(F(1),F(0)),(F(0),F(1))] if launch=='horizontal' else [(F(0),F(1)),(F(1),F(0))]
 assert lo<root<hi;clock=F(0);contactrows=[]
 for idx,(a,b)in enumerate(walls,1):
  tangent=sub(b,a);normal=(-tangent[1],tangent[0]);c=dot(normal,a);norm=dot(normal,normal)
  den=tuple(sum(normal[k]*Vd[k][j]for k in(0,1))for j in(0,1));K=c-dot(normal,O)
  xn=tuple(O[0]*den[j]+K*Vd[0][j]for j in(0,1));yn=tuple(O[1]*den[j]+K*Vd[1][j]for j in(0,1))
  assert ev(den,lo)*ev(den,hi)>0
  assert(ev(xn,root)/ev(den,root),ev(yn,root)/ev(den,root))==P[idx]
  tau=K/ev(den,root);assert tau>clock;clock=tau
  gatevalues=[]
  for d in(lo,hi):
   p=(ev(xn,d)/ev(den,d),ev(yn,d)/ev(den,d));uu=dot(sub(p,a),tangent)/norm
   assert 0<=uu<=1,(name,idx,d,uu);gatevalues.append(uu)
  assert gatevalues[0]!=gatevalues[1]or 0<gatevalues[0]<1
  if hand:
   row=hand['contact_mobius_rows'][idx-1]
   assert eqratio(xn,den,tuple(map(F,row['x_numerator'])),tuple(map(F,row['denominator'])))
   assert eqratio(yn,den,tuple(map(F,row['y_numerator'])),tuple(map(F,row['denominator'])))
  contactrows.append({'x_num':list(map(str,xn)),'y_num':list(map(str,yn)),'den':list(map(str,den)),'time':str(tau)})
  O=tuple(O[k]-2*normal[k]*(dot(normal,O)-c)/norm for k in(0,1))
  nv=tuple(sum(normal[k]*Vd[k][j]for k in(0,1))for j in(0,1))
  Vd=[tuple(Vd[k][j]-2*normal[k]*nv[j]/norm for j in(0,1))for k in(0,1)]
 targeteq=tuple((F(2)-O[0])*Vd[1][j]-(F(2)-O[1])*Vd[0][j]for j in(0,1))
 assert targeteq[1] and -targeteq[0]/targeteq[1]==root
 for v in P[1:-1]:
  if all(c.denominator==1 for c in v):assert angle(mi,v)==180
 summaries.append({'name':name,'n':n,'U':nu,'Z':nz,'root':str(root),'gate':[str(lo),str(hi)],'contacts':contactrows,'target_eq':list(map(str,targeteq)),'accepted':True})
 print('PASS',name,n,'fullguard/finitecontacts/target/launch',flush=True)
reads += [ROOT/'triangle-composition/inputs'/f for f in('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
(HERE/'check.json').write_text(json.dumps({'status':'INDEPENDENT_FIVE_CENTERED_OPTICAL_PACKETS_PASS','fixed_paths':records,'reviews':summaries,'limits':'Fixed supplied paths and three supplied rooms. Whole optical conditions, no search, peer execution, archive, or new room; whole classification separate.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}},indent=2)+'\n')
