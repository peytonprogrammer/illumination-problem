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
parentdir=ROOT/'surplus-four-remote2110';tp=read(parentdir/'parent-templates.json');nr=read(parentdir/'noncritical-erasure.json')
for doc in (tp,nr):
 for rel,h in doc['source_sha256'].items():
  p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==h,rel
for name in ('parent-templates.txt','parent-templates.py','noncritical-erasure.txt','noncritical-erasure.py'):reads.append(parentdir/name)
def edges(ts):
 return {tuple(sorted((t[i],t[(i+1)%3])))for t in ts for i in range(3)}
def verts(ts):return {p for t in ts for p in t}
def star_connected(ts,p):
 ts={t for t in ts if p in t}
 if not ts:return True
 seen={next(iter(ts))}
 while True:
  nxt={q for q in ts-seen if any(len(set(q)&set(t))==2 for t in seen)}
  if not nxt:break
  seen|=nxt
 return seen==ts
known=set(C.values())|{(0,0),(2,0),(2,2)};HE=edges(H);own=[]
side=[(2,0),(0,2),(0,2),(-2,0),(-2,0),(0,-2),(0,-2),(2,0)];opp=[3,6,5,0,7,2,1,4]
for site,a in C.items():
 for m in (3,4):
  for start in range(8):
   ss={(start+j)%8 for j in range(m)}
   if site in {'L':0,'B':1,'E':4,'Tc':5} and {'L':0,'B':1,'E':4,'Tc':5}[site]not in ss:continue
   if site=='N' and {6,7}<=ss:continue
   root=fan(site,ss);neighbors=[b for b in [(0,0),(2,0),(2,2)]if edges(root)&edges(full(b))]
   if len(neighbors)!=1:continue
   for i in ss:
    remote=tuple(a[j]+side[i][j]for j in(0,1))
    if remote in known:continue
    leaf=fan(remote,[opp[i]]);edge=next(iter(edges(root)&edges(leaf)));cp=next(p for p in edge if p[0]%2!=p[1]%2)
    if angle(root,cp)!=180:continue
    assert angle(leaf,cp)==90
    assert not any(edges(root)&edges(full(k))for k in C if k!=site)
    own.append((site,tuple(sorted(ss)),remote,opp[i]))
expected={(r['parent'],tuple(sorted(r['parent_sectors'])),tuple(r['remote_center']),r['remote_sector'])for r in tp['templates']}
assert len(own)==len(set(own))==44 and set(own)==expected
# Angular topology of each removedpatch; no capchoiceproduct needed.
options={}
for k in C:
 caps=[{i}for i in range(8)if edges(fan(k,[i]))&HE]
 units=[{i,(i+1)%8}for i in range(8)if edges(fan(k,[i,(i+1)%8]))&HE]
 options[k]=[set()]+caps+units
reductions=[]
for site,ss,rc,rs in own:
 if site not in ['D','R','N']:continue
 root=fan(site,ss);leaf=fan(rc,[rs]);patch=root|leaf
 if site in ['D','R']:
  keep=set();arc=edges(patch)&HE
  assert len(arc)in[1,2]
  # Every arcpoint has one or twoincidentedges and singlecomponent.
  points=verts({tuple([*e,e[0]])for e in []}) if False else {p for e in arc for p in e}
  deg={p:sum(p in e for e in arc)for p in points}
  assert sum(v==1 for v in deg.values())==2 and max(deg.values())<=2
  for k in C:
   if k!=site:assert all(any(on(p,*e)for e in arc)for p in verts(patch)&verts(full(k)))
 else:
  choices=[{5,6},{4,5},{0,7},{0,1}];ret=next(q for q in choices if q<=set(ss));keep=fan('N',ret)
  assert root-keep<=fan('N',[1,2,3,4])
  assert len(edges(root-keep)&edges(keep))==1
 removed=patch-keep
 for p in verts(removed):
  others=[k for k in C if k!=site and p in verts(full(k))]
  assert len(others)<=1
  for k in others or [None]:
   for form in options[k]if k else [set()]:
    aux=H|keep|(fan(k,form)if k else set())
    assert star_connected(aux,p)and angle(aux,p)<=360
 # Every removededgecomponent reachesanactualoldouteredge unconditionally.
 pending=set(removed);componentcount=0
 while pending:
  seen={next(iter(pending))}
  while True:
   nxt={q for q in pending-seen if any(len(set(q)&set(t))==2 for t in seen)}
   if not nxt:break
   seen|=nxt
  pending-=seen;componentcount+=1
  exposed=[e for e in edges(seen)if sum(e in edges({t})for t in patch)==1 and e not in HE and not any(e in edges(full(k))for k in C if k!=site)]
  assert exposed
 reductions.append({'parent':site,'sectors':ss,'remote':rc,'leaf':rs,'components':componentcount})
assert len(reductions)==24
# Independentlyrecompute21fixedcoordinates usingownincidenthalfplanes.
manifest=read(ROOT/'third-surplus-review/path-support-check.json');selected={}
for rel,h in manifest['sources'].items():
 p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==h
 doc=json.loads(p.read_text())
 if 'forcing_paths'in doc:
  for n,g in doc['forcing_paths'].items():selected[rel+':'+n]=g['path']
 elif 'paths'in doc:
  for n,g in doc['paths'].items():selected[rel+':'+n]=g['path']
 else:selected[rel]=doc.get('path',doc.get('five_path'))
assert len(selected)==21 and set(selected)==set(manifest['paths'])
avoid=full('D')|full('R')|fan('N',[1,2,3,4]);catalog=[]
for name,raw in selected.items():
 P=[tuple(F(*x)for x in p)for p in raw];u,z=path_requirements(P)
 assert u|z<=allK and not(u|z)&avoid
 us,zs=path_requirements([sigma(p)for p in P[::-1]])
 assert(us,zs)==(tr(u),tr(z))and not(us|zs)&avoid
 catalog.append({'name':name,'U':len(u),'Z':len(z)})
reads += [ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'second-surplus-L/classification.txt',ROOT/'surplus-four-local/two-unit.txt',Path(__file__)]
out={'status':'INDEPENDENT_INTERFACE44_AND_NONCRITICAL24_CHECK_PASS_PENDING_HAND_VERDICT','templates':own,'reductions':reductions,'accepted_inventory':catalog,'limits':'Ownlocaladjacency/angularfan/removedcomponent/exteriorproofchecks;21fixedpaths only, noordinarycapassignment ornewroom. Topology andinventoryscope inreview.txt.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS independent44interfaces/24patchreductions/21fullguards+sigma')
