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
# Local junction/template questions only. No completed rooms or cap products.
leaf_cases=[('B',(0,1),'D',(3,),(1,-2)),('D',(2,3),'B',(0,),(1,-2)),('E',(4,5),'R',(2,),(4,1)),('R',(2,3),'E',(5,),(4,1))]
junctions=[]
for root,ss,leaf,tt,p in leaf_cases:
 base=H|fan(root,ss)|fan(leaf,tt)
 possible=base|set().union(*(full(k) for k in C if k not in (root,leaf)))
 assert angle(base,p)==angle(possible,p)==180
 assert len(incident(tuple(map(F,p))))==4
 junctions.append({'root':root,'root_sectors':ss,'leaf':leaf,'leaf_sectors':tt,'shared_C':p,'fixed_angle':180,'other_K_heals':False})
# D01,D12,D23 are EXACTLY the two-sector consecutive windows touching
# D's H-facing north side1/2. Count/sector assertion, not room enumeration.
Dwindows=[(0,1),(1,2),(2,3)]
assert [tuple((i+j)%8 for j in range(2)) for i in range(8) if {i,(i+1)%8}&{1,2}]==Dwindows
arc_checks=[]
for ss in Dwindows:
 Fd=fan('D',ss)
 # Shared canonical edges between the fan and H form a single proper arc.
 tiles=sorted(H|Fd);own=geo.owners_of(tiles);shared=[]
 for edge,owners in own.items():
  if len(owners)==2 and any(tiles[i] in Fd for i in owners) and any(tiles[i] in H for i in owners):shared.append(edge)
 # owners_of returns indexes into the supplied ordered triangle list.
 assert len(shared)==(2 if ss==(1,2) else 1),(ss,shared)
 adj=defaultdict(list)
 for a,b in shared:adj[a].append(b);adj[b].append(a)
 assert sum(len(v)==1 for v in adj.values())==2 and all(len(v)<=2 for v in adj.values())
 # If it meets either diagonal B contact, that point is on the H arc.
 for p in ((1,-1),(3,-1)):
  if any(p in t for t in Fd):assert any(on(p,a,b) for a,b in shared)
 assert not any((1,-3) in t for t in Fd)
 arc_checks.append({'D_sectors':ss,'H_attaching_edges':shared,'proper_arc':True,'possible_B_and_R_point_contacts_on_arc':True})
# Side adjacency of partial centers is exactly the matching B-D and E-R.
adjacent={tuple(sorted((a,b))) for a in C for b in C if a<b and sum(abs(C[a][i]-C[b][i]) for i in (0,1))==2}
assert adjacent=={('B','D'),('E','R')}
# Exactly the21 manifest-selected old fixed paths, no archive search.
manifestfile=ROOT/'third-surplus-review/path-support-check.json';manifest=read(manifestfile)
selected={}
for source,pin in manifest['sources'].items():
 p=ROOT/source;reads.append(p);raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin,source
 data=json.loads(raw)
 if 'forcing_paths' in data:
  for name,record in data['forcing_paths'].items():selected[source+':'+name]=record['path']
 elif 'paths' in data:
  for name,record in data['paths'].items():selected[source+':'+name]=record['path']
 else:selected[source]=data.get('path',data.get('five_path'))
assert set(selected)==set(manifest['paths']) and len(selected)==21
DR=full('D')|full('R');catalog=[]
for name,raw in selected.items():
 P=[tuple(F(*v) for v in p) for p in raw]
 U,Z=path_requirements(P);assert not (U|Z)&DR,name
 us,zs=path_requirements([sigma(p) for p in P[::-1]])
 assert (us,zs)==(tr(U),tr(Z)) and not (us|zs)&DR
 catalog.append({'name':name,'reflections':len(P)-2,'whole_D_R_avoidance':True,'sigma':True})
reads += [ROOT/'surplus-four-local/two-unit.txt',ROOT/'fourth-surplus-review/two-unit-independent/review.txt',ROOT/'fourth-surplus-review/mixed-e2-e1/noncritical-erasure.txt',ROOT/'fourth-surplus-review/mixed-e2-e1/support-check.json']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'PARENT_FOUR_UNIT_BOTH_DR_ERASURE_THIRTEEN','four_root_leaf_junctions':junctions,'D_unit_attaching_arcs':arc_checks,'partial_center_adjacency':sorted(adjacent),'exact21_fixed_inventory_checks':catalog,'parent_claim':'After litNbridgehandled, allfourunits are d1/q2roots atb0; ifDandRunitoccupied, deleteDthenR alongproperHboundaryarcs, preservingtworemainingunitROOTS. AcceptedbudgetfreeTWOunit theorem plus21fixedinventory/fullD-Ravoidance andlocalouter-squareexchanges givesactualST<=13 afterreinsertion. Handgeometry/completeness in argument.txt; independentreviewrequested.','limits':'This closesONLYbothD/Rsubfamily atparentlevel, notallfourunits. No completedroom, capassignmentproduct, discoverypath/ray/direction/word/archive/worker. Only21manifestselectedpaths/sevenpinnedsources read. Sourceopticalbounds andtwo-unitcompleteness are inheritedaccepteddependencies.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS localunitattachment/smoothjunctions and21fixedD/R-avoidingpaths; parentbothD/Rfourunit<=13 requires independenthandreview.')
