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
configs=[
 ('B-full-L70-lower-search',20,30,13,H|fan('L',[7,0])|fan('B',[1,2,3,4])|fan((-2,-2),[7])|fan('E',[4])|fan('R',[3]),fan('L',[6])|fan('B',[5])|fan('D',[1,2])|fan('R',[2,4])|fan('E',[3,5])|fan('Tc',[6])|fan('N',[5,6])|fan((-2,-2),[0,6]),(-32,-40)),
 ('B-full-L70-lower-Tc6-search',6,17,5,H|fan('L',[7,0]),fan('L',[6])|fan('D',[1])|fan('R',[4])|fan('N',[5,7]),(-8,10)),
 ('B-full-L70-lower-N7Tc6-search',8,22,7,H|fan('L',[7,0])|fan('R',[3]),fan('L',[6])|fan('D',[1])|fan('R',[2,4])|fan('Tc',[5])|fan('N',[0,5]),(-8,20)),
 ('B-full-L70-lower-D1-search',10,20,7,H|fan('L',[7,0])|fan('D',[1])|fan('R',[3])|fan('N',[7]),fan('L',[6])|fan('D',[0])|fan('R',[2,4])|fan('N',[0,5,6]),(-12,16)),
 ('B-full-L70-lower-R4-search',5,22,8,H|fan('L',[7,0])|fan('B',[1,2,3,4]),fan('L',[1])|fan('B',[0,5,6,7])|fan('R',[3])|fan('N',[7])|fan((-2,-2),[0]),(-12,6)),
 ('B-full-L70-upper-search',22,30,13,H|fan('L',[7,0])|fan('B',[1,2,3,4])|fan((-2,-2),[0])|fan('E',[4])|fan('R',[3]),fan('L',[6])|fan('B',[5])|fan('D',[1,2])|fan('R',[2,4])|fan('E',[3,5])|fan('Tc',[6])|fan('N',[5,6])|fan((-2,-2),[1,7]),(-32,-40))]
def affine_ev(a,d):return a[0]+a[1]*d
def mul(a,b):return(a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[1]*b[1])
def eqratio(a,b,c,e):return mul(a,e)==mul(c,b)
summaries=[]
for name,n,nu,nz,mi,expectedZ,image in configs:
 q=ROOT/'surplus-four-remote2110'/name;g=read(q/'verification.json');hand=read(q/'hand.json');raw=read(q/'room.json')
 for rel,h in g['source_sha256'].items():
  f=ROOT/rel;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==h,rel
 for file,h in hand['source_sha256'].items():
  f=q/file;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==h
 reads += [q/'argument.txt',q/'coverage.txt',q/'verify.py',q/'hand.py']
 P=fp(g['path']);walls=[[tuple(map(F,a)),tuple(map(F,b))]for a,b in g['walls']]
 ma=(allK|full((-2,-2)))-expectedZ;u,z=optical(name,P,walls,mi,ma,image,g)
 assert(n,len(u),len(z))==(len(P)-2,nu,nz)and z==expectedZ
 assert all(not on((0,0),a,b)for a,b in zip(P[1:],P[2:]))
 room=decode(raw['triangles']);V=list(map(tuple,raw['vertices']));assert len(room)==35 and len(V)==20 and mi<=room<=ma
 assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==n
 assert replay([sigma(p)for p in V],(0,0),(2,2),[sigma(p)for p in P[::-1]])==n
 # Owncanceled-edge reconstruction andnonadjacentintersection checks.
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
 # Independentlytransportreflectedsource+affinevelocity (notpeercovectors).
 root=F(hand['root']);lo,hi=map(F,hand['strict_sufficient_finite_wall_gate']);assert lo<root<hi
 if n in[20,22]:O=(F(0),F(0));Vd=[(F(0),F(-1)),(F(-1),F(0))]
 elif n==5:O=(F(0),F(0));Vd=[(F(-1),F(0)),(F(0),F(1))]
 else:O=(F(0),F(0));Vd=[(F(0),F(-1)),(F(1),F(0))]
 clock=F(0)
 for idx,((a,b),parentrow)in enumerate(zip(walls,hand['contact_mobius_rows']),1):
  tangent=sub(b,a);normal=(-tangent[1],tangent[0]);c=dot(normal,a);norm=dot(normal,normal)
  den=tuple(sum(normal[k]*Vd[k][j]for k in(0,1))for j in(0,1));K=c-dot(normal,O)
  xn=tuple(O[0]*den[j]+K*Vd[0][j]for j in(0,1));yn=tuple(O[1]*den[j]+K*Vd[1][j]for j in(0,1))
  assert affine_ev(den,lo)*affine_ev(den,hi)>0
  assert(affine_ev(xn,root)/affine_ev(den,root),affine_ev(yn,root)/affine_ev(den,root))==P[idx]
  tau=K/affine_ev(den,root);assert tau>clock;clock=tau
  assert eqratio(xn,den,tuple(map(F,parentrow['x_numerator'])),tuple(map(F,parentrow['denominator'])))
  assert eqratio(yn,den,tuple(map(F,parentrow['y_numerator'])),tuple(map(F,parentrow['denominator'])))
  gatevalues=[]
  for d in(lo,hi):
   p=(affine_ev(xn,d)/affine_ev(den,d),affine_ev(yn,d)/affine_ev(den,d));uu=dot(sub(p,a),tangent)/dot(tangent,tangent)
   assert 0<=uu<=1;gatevalues.append(uu)
  # Constantendpointcontactwouldfailstrictgate; varyingMobiuswithclosedendboundsisstrictinside.
  assert gatevalues[0]!=gatevalues[1]or 0<gatevalues[0]<1
  O=tuple(O[k]-2*normal[k]*(dot(normal,O)-c)/norm for k in(0,1))
  nv=tuple(sum(normal[k]*Vd[k][j]for k in(0,1))for j in(0,1))
  Vd=[tuple(Vd[k][j]-2*normal[k]*nv[j]/norm for j in(0,1))for k in(0,1)]
 targeteq=tuple((F(2)-O[0])*Vd[1][j]-(F(2)-O[1])*Vd[0][j]for j in(0,1));assert targeteq[1]and -targeteq[0]/targeteq[1]==root
 # Everyintegercontactisexplicitlysmoothpi; integeropenlegvertices havefullincidentU.
 smooth=[]
 for v in P[1:-1]:
  if all(c.denominator==1 for c in v):assert angle(mi,v)==180 and v not in V;smooth.append(list(map(str,v)))
 summaries.append({'name':name,'reflections':n,'U':nu,'Z':nz,'root':str(root),'gate':[str(lo),str(hi)],'smooth_integer_contacts':smooth,'whole_support_ACCEPT':True})
 print('PASS',name,n,'fullguards/actualphysical/affinebeam',flush=True)
reads += [ROOT/'triangle-composition/inputs'/f for f in('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_SIX_BFULL_OPTICAL_PACKETS_PASS_PENDING_HAND_REVIEW_VERDICT','fixed_paths':records,'reviews':summaries,'limits':'SIXsuppliedpolygons/paths only; independentincidentguards, maximalboundary, reflectedsourceaffinebeam; nopeerexecution/discovery/archive/newroom. Whole2110classificationseparate.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS ALLSIX')
