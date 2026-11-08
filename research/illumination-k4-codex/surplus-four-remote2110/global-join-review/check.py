"""Independent finite interface/vertex tests and accepted source-map audit.
No room census, discovery, peer checker execution, or source mutation.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import product
import hashlib,json
HERE=Path(__file__).resolve().parent; BASE=HERE.parents[1]
SRC=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(SRC)}
exec(compile(SRC.read_text().split('\ndef path(d,nine):')[0],str(SRC),'exec'),e)
fan,H,C=e['fan'],e['H'],e['C']; HA={(0,0),(2,0),(2,2)}; K=HA|set(C.values())
def edges(ts):return {tuple(sorted((a,b))) for t in ts for a,b in zip(t,t[1:]+t[:1])}
def verts(ts):return set().union(*(set(t) for t in ts)) if ts else set()
def angle(ts,p):return sum(90 if e['dot'](*[e['sub'](v,p) for v in t if v!=p])==0 else 45 for t in ts if p in t)
def connected(ts,p):
 local={t for t in ts if p in t}
 if not local:return True
 seen=set();todo=[next(iter(local))]
 while todo:
  t=todo.pop()
  if t in seen:continue
  seen.add(t);todo.extend(q for q in local-seen if any(p in ed for ed in edges({t})&edges({q})))
 return seen==local
HE=edges(H); HV=verts(H)
def d(a,ss):
 return len({(2*c[0]-a[0],2*c[1]-a[1]) for t in fan(a,ss) for c in t if (c[0]%2)!=(c[1]%2) and (2*c[0]-a[0],2*c[1]-a[1]) in HA})
def validfan(a,ss):return not fan(a,ss)&H and not(a==(0,2) and {6,7}<=set(ss))
ordinary={a:[()]+[(i,) for i in range(8) if d(a,(i,))==1 and validfan(a,(i,))] for a in C.values()}
units=[(a,ss) for a in C.values() for m in (1,2) for i in range(8) for ss in [tuple((i+j)%8 for j in range(m))] if validfan(a,ss) and m-d(a,ss)==1]
# Every candidate is only a root/remote interface and at most one specified
# unit patch. Necessary local geometry is tested; no whole cap product.
rows=[(1,1,0,2),(1,2,0,1),(1,3,0,0),(1,1,1,1),(1,2,1,0)]
interfaces=[];vertex_trials=0;other_leaf_candidates=0
for row in rows:
 _,l,h,b=row
 for a in C.values():
  for i in range(8):
   ss=(i,(i+1)%8)
   if not validfan(a,ss) or d(a,ss)!=1:continue
   root=fan(a,ss);out=edges(root)-HE
   bc=[ed for ed in out if all(p!=a for p in ed)]
   # Root radial edges are not cell edges. Exactly one outward BC half.
   assert len(bc)<=1
   if not bc:continue
   attach=bc[0];mid=next(p for p in attach if p[0]%2!=p[1]%2)
   remote=(2*mid[0]-a[0],2*mid[1]-a[1])
   if remote in K:continue
   for m in ([1] if l==1 else [2] if l==2 else [3,4]):
    for j in range(8):
     ls=tuple((j+k)%8 for k in range(m));leaf=fan(remote,ls)
     if attach not in edges(leaf):continue
     assert len(edges(root)&edges(leaf))==1
     options=[None] if h==0 else [(ua,us) for ua,us in units if ua!=a]
     for option in options:
      ua,us=option if option else (None,())
      unit=fan(ua,us) if option else set();fixed=H|root|leaf|unit
      if option:
       if not edges(unit)&edges(H|root|leaf):continue
       # Unique parent prohibits a second H-root attached to remote fan.
       if d(ua,us)>0 and edges(unit)&edges(leaf):continue
      # Outside-H smooth C cannot be altered by any ordinary H cap.
      smoothC=[p for p in verts(fixed)-HV if p[0]%2!=p[1]%2 and angle(fixed,p)==180]
      if len(smoothC)>b:continue
      if option and d(ua,us)==0:other_leaf_candidates+=1
      # There cannot be an onward d0 unit attachment in either h1 row.
      assert not option or d(ua,us)==1,(row,a,ss,remote,ls,option)
      assert edges(leaf)&edges(H|root|unit)=={attach}
      # All other occupied cells are ordinary caps. Inspect every local
      # angular completion at EACH changed vertex, not assembled rooms.
      for p in verts(leaf):
       sites=[v for v in C.values() if v!=a and v!=ua and p in verts(fan(v,range(8)))]
       for choices in product(*(ordinary[v] for v in sites)):
        before=fixed|set().union(*(fan(v,cs) for v,cs in zip(sites,choices)))
        if not connected(before,p) or angle(before,p)>360:continue
        # Ordinary caps cannot supply another side attachment.
        assert edges(leaf)&edges(before-leaf)=={attach}
        after=before-leaf
        assert connected(after,p) and angle(after,p)<360,(row,a,ss,remote,ls,option,p,choices)
        if p not in attach:assert not any(p in t for t in after),(row,a,ss,remote,ls,option,p,choices)
        vertex_trials+=1
      interfaces.append({'row':row,'parent':a,'root':ss,'remote':remote,'leaf':ls,'unit':option,'outside_smooth_C':smoothC,'single_edge_and_surviving_stars':'PASS'})
assert other_leaf_candidates==0
# Recompute the entire 21-coordinate named inventory using own Fraction
# half-plane intersection and mirror side incidence, plus sigma/reversal.
reads=[SRC,Path(__file__)]
def read(rel):
 p=BASE/rel;reads.append(p);return json.loads(p.read_text())
support=read('third-surplus-review/path-support-check.json');paths={}
for rel,want in support['sources'].items():
 p=BASE/rel;assert hashlib.sha256(p.read_bytes()).hexdigest()==want
 doc=read(rel)
 if 'forcing_paths' in doc:
  for name,x in doc['forcing_paths'].items():paths[rel+':'+name]=x['path']
 elif 'paths' in doc:
  for name,x in doc['paths'].items():paths[rel+':'+name]=x['path']
 else:paths[rel]=doc.get('path',doc.get('five_path'))
assert set(paths)==set(support['paths']) and len(paths)==21
allK=H|set().union(*(fan(a,range(8)) for a in C.values()))
def guard(P):
 walls=[]
 for a,p,b in zip(P,P[1:],P[2:]):
  v=e['sub'](p,a);w=e['sub'](b,p);v=tuple(x/max(map(abs,v)) for x in v);w=tuple(x/max(map(abs,w)) for x in w)
  t=tuple(v[k]+w[k] for k in (0,1))
  if t==(0,0):t=(-v[1],v[0])
  walls.append((tuple(p[k]-t[k] for k in (0,1)),tuple(p[k]+t[k] for k in (0,1))))
 return e['constraints'](P,walls)[:2]
pathchecks={}
for name,raw in paths.items():
 P=[tuple(F(*x) for x in p) for p in raw]
 assert P[0]==(0,0) and P[-1]==(2,2)
 U,Z=guard(P);ur,zr=guard(P[::-1]);us,zs=guard([e['sigma'](p) for p in P[::-1]])
 assert U|Z<=allK and (ur,zr)==(U,Z) and (us,zs)==(e['transform'](U),e['transform'](Z))
 assert us|zs<=allK
 assert len(P)-2==support['paths'][name]['reflections']<=13
 for a,b in zip(P[:-2],P[1:-1]):assert not e['on']((2,2),a,b)
 pathchecks[name]={'reflections':len(P)-2,'U':len(U),'Z':len(Z),'K_only_forward_reverse_sigma':True}
 print('PASS own guard',len(pathchecks),flush=True)
# Audit independently accepted proof map and every frozen pin.
globalmap=read('fourth-surplus-review/global-four-closure/manifest.json')
supplement=read('fourth-surplus-review/global-four-closure/rowmap-supplement.json')
for doc in (globalmap,supplement):
 for rel,want in doc['source_sha256'].items():
  p=BASE/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==want,rel
local=read('fourth-surplus-review/local-four-closure/manifest.json')
assert len(local['cases'])==10 and max(x['bound'] for x in local['cases'])==32
for rel in ['surplus-four-remote2110/local-join-review/check.json','surplus-four-remote2110/peer-2101-whole-review/check.json','surplus-four-remote2110/check.json']:
 doc=read(rel)
 for src,want in doc.get('source_sha256',{}).items():
  p=(BASE/'surplus-four-remote2110'/src) if rel=='surplus-four-remote2110/check.json' else BASE/src;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==want,src
remote={(r,l,h,b) for r in (1,2) for l in (1,2,3) for h in range(3) for b in range(4) if r+l+h+b==4 and (r!=1 or l!=1 or b>=1)}
assert remote==set(rows)|{(2,2,0,0),(2,1,0,1),(2,1,1,0)}
assert {tuple(x['charge']) for x in globalmap['remote_rows']}==remote
assert all(x['bound']==(23 if tuple(x['charge'])==(2,2,0,0) else 13) for x in globalmap['remote_rows'])
# Review root text and lower theorem sources are frozen separately.
for rel in ['fourth-surplus-review/global-four-closure/theorem.txt','fourth-surplus-review/leaf-erasure.txt','second-surplus-L/classification.txt','surplus-four-local/two-unit.txt','third-surplus-review/local-two-unit.txt','surplus-four-local/four-unit-DR-independent/review.txt','fourth-surplus-review/peer-remote-noncritical-independent/review.txt','remote22-proof-review/review.txt','fourth-surplus-review/structural-reduction.txt']:
 reads.append(BASE/rel)
out={'status':'INDEPENDENT_GLOBAL_DELTA4_JOIN_ACCEPTED','bound':32,'parent1_rows':rows,'necessary_interface_patches':len(interfaces),'patch_counts_by_row':{str(row):sum(tuple(x['row'])==row for x in interfaces) for row in rows},'surviving_angular_vertex_trials':vertex_trials,'additional_d0_unit_leaf_survivors':other_leaf_candidates,'interfaces':interfaces,'fixed_paths':pathchecks,'global_pins_checked':len(globalmap['source_sha256']),'local_types':10,'remote_rows':sorted(remote),'limits':'Interface/fan patches and per-vertex completions are necessary overapproximations, not room counts. New topology and final join hand-reviewed in review.txt; optics inherited from accepted sources plus own 21 full K guards. Derived square compositions have separate hand proof, not claimed among21. No peer checker execution, discovery, whole-room census, formal verification, or external referee.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS independent global32:',len(interfaces),'necessary interface patches;',vertex_trials,'angular trials;',len(globalmap['source_sha256']),'source pins')
