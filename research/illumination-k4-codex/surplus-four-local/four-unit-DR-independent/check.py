"""Independent local attachment checks and exactly 21 selected old path guards.
No peer checker execution, complete room generation, or optical discovery.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
import hashlib, json
HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H']
C=e['C'];sub,dot,on=e['sub'],e['dot'],e['on']
reads=[src,Path(__file__)]
def read(rel):
 p=BASE/rel;reads.append(p);return json.loads(p.read_text())
def edges(ts):
 return {tuple(sorted((a,b))) for t in ts for a,b in zip(t,t[1:]+t[:1])}
def angle(ts,p):
 return sum(90 if dot(*[sub(v,p) for v in t if v!=p])==0 else 45 for t in ts if p in t)
def guard(P):
 walls=[]
 for a,p,b in zip(P,P[1:],P[2:]):
  v=sub(p,a);w=sub(b,p)
  v=tuple(x/max(map(abs,v)) for x in v);w=tuple(x/max(map(abs,w)) for x in w)
  tangent=tuple(v[k]+w[k] for k in (0,1))
  if tangent==(0,0):tangent=(-v[1],v[0])
  walls.append((tuple(p[k]-tangent[k] for k in (0,1)),tuple(p[k]+tangent[k] for k in (0,1))))
 return e['constraints'](P,walls)[:2]
# Side adjacency from actual shared canonical edges, not distances alone.
full={k:fan(k,range(8)) for k in C}
side_pairs=[(a,b) for a in C for b in C if a<b and edges(full[a])&edges(full[b])]
assert set(side_pairs)=={('B','D'),('E','R')}
# Recover all two-sector root windows from shared H edges, one fan at a time.
roots={}
for k in C:
 roots[k]=[tuple((i+j)%8 for j in range(2)) for i in range(8) if edges(fan(k,[i,(i+1)%8]))&edges(H)]
assert roots['D']==[(0,1),(1,2),(2,3)]
# Recover every possible root-to-single-leaf edge, without cap products.
leaf_joins=[]
for a,b in side_pairs:
 for root,leaf in [(a,b),(b,a)]:
  for ss in roots[root]:
   for i in range(8):
    one=fan(leaf,[i])
    if not edges(one)&edges(H) and edges(one)&edges(fan(root,ss)):
     leaf_joins.append((root,ss,leaf,i))
assert set(leaf_joins)=={('B',(0,1),'D',3),('D',(2,3),'B',0),('E',(4,5),'R',2),('R',(2,3),'E',5)}
junctions=[]
for root,ss,leaf,i in leaf_joins:
 p=(1,-2) if root in ('B','D') else (4,1)
 fixed=H|fan(root,ss)|fan(leaf,[i])
 others=set().union(*(full[k] for k in C if k not in (root,leaf)))
 assert angle(fan(root,ss),p)==angle(fan(leaf,[i]),p)==90
 assert angle(fixed,p)==180 and angle(others,p)==0
 junctions.append({'root':root,'sectors':ss,'leaf':leaf,'leaf_sector':i,'C':p,'angle':180,'other_centers_contribution':0})
# Three D arc templates and exclusion of a second attaching edge at B.
arc_checks=[]
for ss in roots['D']:
 f=fan('D',ss);shared=edges(f)&edges(H)
 assert len(shared)==(2 if ss==(1,2) else 1)
 degree=Counter(v for edge in shared for v in edge)
 assert sorted(degree.values())==([1,1,2] if len(shared)==2 else [1,1])
 for p in ((1,-1),(3,-1)):
  if any(p in t for t in f):assert any(on(p,a,b) for a,b in shared)
 assert not any((1,-3) in t for t in f)
 for bss in roots['B']:
  if edges(f)&edges(fan('B',bss)):
   assert ss==(2,3) and bss==(0,1)
   assert angle(H|f|fan('B',bss),(1,-2))==180
 arc_checks.append({'D_window':ss,'H_edges':sorted(shared),'single_proper_arc':True})
# Check the surviving local sectors at each exposed B-type vertex form ONE
# angular interval. Compare shared triangle edges containing p to avoid
# accepting disconnected angular sectors with the right total angle.
continuity=[]
for site,p in [('B',(1,-1)),('R',(3,-1))]:
 options=[()]+[(i,) for i in ([1,2] if site=='B' else [3,4])]+roots[site]
 for ss in options:
  local={t for t in H|fan(site,ss) if p in t}
  seen=set();todo=[next(iter(local))]
  while todo:
   t=todo.pop()
   if t in seen:continue
   seen.add(t)
   todo += [q for q in local-seen if any(p in edge for edge in edges({t})&edges({q}))]
  assert seen==local and 0<angle(local,p)<360
  continuity.append({'vertex':p,'site':site,'sectors':ss,'angle':angle(local,p),'connected':True})
assert angle(H,(2,-1))==180
# Sigma exchanges the complete geometric situation, including absence of
# the E/R outer join retained after deleting D; no auxiliary b0 assumption.
assert e['transform'](H)==H and e['transform'](full['D'])==full['R']
assert e['transform'](full['B'])==full['E']
manifest=read('third-surplus-review/path-support-check.json')
selected={}
for source,pin in manifest['sources'].items():
 p=BASE/source;reads.append(p);raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==pin,source
 data=json.loads(raw)
 if 'forcing_paths' in data:
  for name,rec in data['forcing_paths'].items():selected[source+':'+name]=rec['path']
 elif 'paths' in data:
  for name,rec in data['paths'].items():selected[source+':'+name]=rec['path']
 else:selected[source]=data.get('path',data.get('five_path'))
assert set(selected)==set(manifest['paths']) and len(selected)==21
DR=full['D']|full['R'];catalog=[]
for name,raw in selected.items():
 P=[tuple(F(*v) for v in p) for p in raw]
 u,z=guard(P);assert not (u|z)&DR,name
 # One fresh sigma calculation per path, with reversed endpoint order.
 us,zs=guard([e['sigma'](p) for p in P[::-1]])
 assert (us,zs)==(e['transform'](u),e['transform'](z))
 assert not (us|zs)&DR
 catalog.append({'name':name,'reflections':len(P)-2,'U':len(u),'Z':len(z),'D_R_independent':True,'sigma_recomputed':True})
 print('PASS',len(catalog),name,flush=True)
# The review's hand dependency map is recorded in review.txt; these files
# are pinned so subsequent edits cannot silently change its prerequisites.
for rel in ['fourth-surplus-review/four-unit-DR-erasure/argument.txt','fourth-surplus-review/four-unit-DR-erasure/check.py','fourth-surplus-review/four-unit-DR-erasure/check.json','fourth-surplus-review/four-unit-DR-erasure/coverage.txt','surplus-four-local/two-unit.txt','third-surplus-review/local-two-unit.txt','fourth-surplus-review/two-unit-independent/review.txt','fourth-surplus-review/mixed-e2-e1/noncritical-erasure.txt']:
 reads.append(BASE/rel)
out={'status':'INDEPENDENT_BOTH_DR_FOUR_UNIT_ERASURE_ACCEPT','local_side_pairs':side_pairs,'root_leaf_exclusion':junctions,'D_attaching_arcs':arc_checks,'exposed_vertex_checks':continuity,'catalog':catalog,'reflections_at_most':13,'limits':'Independent geometric review and exact guard recomputation; accepted TWO-root theorem, finite path legality and local square exchanges inherited. No full four-unit/Delta4 result; one-DR extension separately pending. No complete rooms, cap products, optical discovery or peer checker execution.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],flush=True)
