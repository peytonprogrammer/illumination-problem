"""24 local parent/remote patch reductions, plus21 accepted guard checks.
No completed room, cap assignment product, archive, discovery or peer code.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];C=e['C'];reads=[src,Path(__file__)]
def read(rel):
 p=BASE/rel;reads.append(p);return json.loads(p.read_text())
def edges(ts):return {tuple(sorted((a,b)))for t in ts for a,b in zip(t,t[1:]+t[:1])}
def vertices(ts):return {p for t in ts for p in t}
def angle(ts,p):
 return sum(90 if e['dot'](*[e['sub'](v,p)for v in t if v!=p])==0 else 45 for t in ts if p in t)
def connected_at(ts,p):
 local={t for t in ts if p in t}
 if not local:return True
 seen=set();todo=[next(iter(local))]
 while todo:
  t=todo.pop()
  if t in seen:continue
  seen.add(t)
  todo += [q for q in local-seen if any(p in edge for edge in edges({t})&edges({q}))]
 return seen==local
HE=edges(H);templates=read('surplus-four-remote2110/parent-templates.json')['templates']
# Single-site fan alphabets solely for new boundary-vertex connectivity.
options={}
for k in C:
 caps=[(i,)for i in range(8)if edges(fan(k,[i]))&HE]
 roots=[(i,(i+1)%8)for i in range(8)if edges(fan(k,[i,(i+1)%8]))&HE]
 options[k]=[()]+caps+roots
reductions=[]
for row in templates:
 parent=row['parent']
 if parent not in ('D','R','N'):continue
 root=fan(parent,row['parent_sectors']);leaf=fan(tuple(row['remote_center']),[row['remote_sector']]);whole=root|leaf
 if parent in ('D','R'):
  retained=set();arc=edges(whole)&HE
  assert len(arc)in(1,2)
  degrees=Counter(v for edge in arc for v in edge)
  assert sorted(degrees.values())==([1,1]if len(arc)==1 else[1,1,2])
  for k in C:
   if k==parent:continue
   contacts=vertices(whole)&vertices(fan(k,range(8)))
   assert all(any(e['on'](p,a,b)for a,b in arc)for p in contacts),(row,k,contacts,arc)
 else:
  ss=set(row['parent_sectors'])
  retain=[5,6]if{5,6}<=ss else[4,5]if{4,5}<=ss else[7,0]if{7,0}<=ss else[0,1]
  retained=fan('N',retain);assert retained<=root
  assert root-retained<=fan('N',[1,2,3,4])
  arc=edges(root-retained)&edges(retained)
  assert len(arc)==1
 # At ANY potentially changed vertex, at most ONE other partialKcell
 # contributes. So independent single-site checks cover all actual fans.
 changed=vertices(whole-retained);junctions=[]
 for p in sorted(changed):
  other=[k for k in C if k!=parent and angle(fan(k,range(8)),p)]
  assert len(other)<=1,(row,p,other)
  if other:
   k=other[0]
   for ss in options[k]:
    left=H|retained|fan(k,ss)
    assert connected_at(left,p)and angle(left,p)<=360,(row,p,k,ss)
   junctions.append({'vertex':p,'other_site':k,'single_site_fan_cases':len(options[k])})
  else:
   assert connected_at(H|retained,p)and angle(H|retained,p)<=360
 # Every removed component contains a triangle with a boundary edge of
 # the original patch, independent of otherKpointcontacts. No closed hole.
 removed=whole-retained;unseen=set(removed);components=0
 while unseen:
  start=next(iter(unseen));todo=[start];component=set()
  while todo:
   t=todo.pop()
   if t in component:continue
   component.add(t);todo += [q for q in removed-component if edges({t})&edges({q})]
  unseen-=component;components+=1
  counts=Counter(edge for t in whole for edge in edges({t}))
  otherKedges=set().union(*(edges(fan(k,range(8))) for k in C if k!=parent))
  assert any(counts[edge]==1 and edge not in HE and edge not in otherKedges for t in component for edge in edges({t}))
 reductions.append({'parent':parent,'parent_sectors':row['parent_sectors'],'remote_center':row['remote_center'],'remote_sector':row['remote_sector'],'retained_N_sectors':retain if parent=='N'else[],'changed_vertex_checks':junctions,'removed_patch_components_meet_old_boundary':components,'auxiliary_positive_roots':2 if parent=='N' else 1})
assert len(reductions)==24
# Exactly21 manifest-selected fixed coordinates, prior proof inventory.
manifest=read('third-surplus-review/path-support-check.json');selected={}
for rel,h in manifest['sources'].items():
 p=BASE/rel;reads.append(p);raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==h
 data=json.loads(raw)
 if'forcing_paths'in data:
  for n,r in data['forcing_paths'].items():selected[rel+':'+n]=r['path']
 elif'paths'in data:
  for n,r in data['paths'].items():selected[rel+':'+n]=r['path']
 else:selected[rel]=data.get('path',data.get('five_path'))
assert set(selected)==set(manifest['paths'])and len(selected)==21
allK=H|set().union(*(fan(k,range(8))for k in C))
avoid=fan('D',range(8))|fan('R',range(8))|fan('N',[1,2,3,4])
def guard(P):
 walls=[]
 for a,p,b in zip(P,P[1:],P[2:]):
  v=e['sub'](p,a);w=e['sub'](b,p);v=tuple(x/max(map(abs,v))for x in v);w=tuple(x/max(map(abs,w))for x in w)
  t=tuple(v[k]+w[k]for k in(0,1))
  if t==(0,0):t=(-v[1],v[0])
  walls.append((tuple(p[k]-t[k]for k in(0,1)),tuple(p[k]+t[k]for k in(0,1))))
 return e['constraints'](P,walls)[:2]
catalog=[]
for name,raw in selected.items():
 P=[tuple(F(*x)for x in p)for p in raw];u,z=guard(P)
 assert u|z<=allK and not(u|z)&avoid,name
 us,zs=guard([e['sigma'](p)for p in P[::-1]])
 assert(us,zs)==(e['transform'](u),e['transform'](z))and not(us|zs)&avoid
 catalog.append({'name':name,'U':len(u),'Z':len(z),'full_K_support':True,'DR_and_Noutside1234_avoided':True})
 print('PASS guard',len(catalog),flush=True)
reads += [HERE/'noncritical-erasure.txt',HERE/'parent-templates.txt',BASE/'second-surplus-L/classification.txt',BASE/'surplus-four-local/two-unit.txt',BASE/'surplus-four-local/four-unit-DR-independent/review.txt']
out={'status':'PARENT_24_NONCRITICAL_REMOTE2110_REDUCTIONS_PASS_PENDING_HAND_REVIEW','local_patch_reductions':reductions,'accepted_inventory':catalog,'bound':13,'limits':'Localpatcharc/angularchecks and21fixedguardchecks only. Complete topology/ONEunit/TWOunitinventory applicability argued in companiontext and needspeerreview. No budgets assumedpreserved. No completedroom/capassignment/discovery/archive/peerexecution. RemainingcriticalL/Bsigma20templatesseparate.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'noncritical-erasure.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
