"""Final fixed proof-map/source/optical-support checks. No discovery."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
reads=[]
def read(rel):
 p=ROOT/rel;reads.append(p);return json.loads(p.read_text())
def pinrel(rel):
 p=ROOT/rel;reads.append(p);assert p.is_file(),rel
 return hashlib.sha256(p.read_bytes()).hexdigest()
# Preserve every previously accepted local source rather than replacing it
# by a new list that could quietly lose one of the ten cases.
local=read('fourth-surplus-review/local-four-closure/manifest.json')
localreview=read('surplus-four-remote2110/local-join-review/check.json')
for doc in [local,localreview]:
 for rel,h in doc['source_sha256'].items():assert pinrel(rel)==h,rel
assert len(local['cases'])==10 and max(c['bound']for c in local['cases'])==32
r2101=read('surplus-four-remote2110/peer-2101-whole-review/check.json')
assert r2101['status']=='INDEPENDENT_WHOLE_REMOTE2101_WITHIN13_ACCEPTED'and r2101['bound']==13
r2110=[read('fourth-surplus-review/'+p+'/check.json')for p in ['peer-remote-noncritical-independent','peer-remote-critical-L-independent','peer-B-final-independent']]
for d in [r2101]+r2110:
 for rel,h in d['source_sha256'].items():assert pinrel(rel)==h,rel
assert r2110[1]['necessary_labels']==205 and r2110[2]['necessary_counts']=={'0':151,'7':35}
# The remote2200 proof's frozen original is unchanged. Structural1--5,
# exactly the part reused for remote exhaustion, is unchanged since review;
# the later corrected local list is covered by the separate local review.
for n in ['remote22.txt']:
 assert (ROOT/'remote22-proof-review/inputs/fourth-surplus-review'/n).read_bytes()==(ROOT/'fourth-surplus-review'/n).read_bytes()
cur=(ROOT/'fourth-surplus-review/structural-reduction.txt').read_text();old=(ROOT/'remote22-proof-review/inputs/fourth-surplus-review/structural-reduction.txt').read_text()
assert cur[cur.index('1. Budget'):cur.index('6. Necessary wholly local')]==old[old.index('1. Budget'):old.index('6. Necessary wholly local')]
# Enumerate charge partitions ONLY, not polygon or direction candidates.
remote={(r,l,h,b)for r in (1,2)for l in (1,2,3)for h in range(5)for b in range(5)if r+l+h+b==4 and(not(r==l==1)or b>=1)}
five={(1,1,0,2),(1,2,0,1),(1,3,0,0),(1,1,1,1),(1,2,1,0)}
other={(2,2,0,0),(2,1,0,1),(2,1,1,0)}
assert remote==five|other and len(remote)==8
# Fresh complete guards of precisely the21 already named coordinate records
# in the older K-support receipt. No source archive query or candidate scan.
support=read('third-surplus-review/path-support-check.json');paths={}
for source,h in support['sources'].items():
 assert pinrel(source)==h
 data=read(source)
 if 'forcing_paths'in data:
  for name,g in data['forcing_paths'].items():paths[source+':'+name]=g['path']
 elif 'paths'in data:
  for name,g in data['paths'].items():paths[source+':'+name]=g['path']
 else:paths[source]=data.get('path',data.get('five_path'))
assert set(paths)==set(support['paths'])and len(paths)==21
K={(0,0),(2,0),(2,2),(-2,0),(0,-2),(2,-2),(4,0),(4,2),(2,4),(0,2)}
sigma=lambda p:(2-p[1],2-p[0]);details={}
def centers(ts):
 out=set()
 for t in ts:
  aa=[p for p in t if p[0]%2==p[1]%2==0];assert len(aa)==1;out.add(aa[0])
 return out
for name,raw in paths.items():
 P=[tuple(F(*v)for v in p)for p in raw];assert P[0]==(0,0)and P[-1]==(2,2)
 u,z=path_requirements(P);ur,zr=path_requirements([sigma(p)for p in P[::-1]])
 assert centers(u|z|ur|zr)<=K
 assert len(P)-2==support['paths'][name]['reflections']<=13
 details[name]={'n':len(P)-2,'U':len(u),'Z':len(z),'all_support_in_K':True}
rootfiles=['fourth-surplus-review/structural-reduction.txt','fourth-surplus-review/local-four-closure/theorem.txt','fourth-surplus-review/local-four-closure/manifest.json','surplus-four-remote2110/local-join-review/review.txt','surplus-four-remote2110/local-join-review/coverage.txt','second-surplus-L/classification.txt','surplus-four-local/two-unit.txt','fourth-surplus-review/two-unit-independent/review.txt','fourth-surplus-review/leaf-erasure.txt','remote22-proof-review/review.txt','remote22-proof-review/check.json','fourth-surplus-review/remote22.txt','fourth-surplus-review/remote2101/theorem.txt','fourth-surplus-review/remote2101/manifest.json','surplus-four-remote2110/peer-2101-whole-review/review.txt','surplus-four-remote2110/peer-2101-whole-review/coverage.txt','fourth-surplus-review/peer-remote-noncritical-independent/review.txt','fourth-surplus-review/peer-remote-critical-L-independent/review.txt','fourth-surplus-review/peer-B-final-independent/review.txt','fourth-surplus-review/peer-centered-square-independent/review.txt','fourth-surplus-review/global-four-closure/theorem.txt']
for rel in rootfiles:pinrel(rel)
reads += [Path(__file__),ROOT/'triangle-composition/inputs/guard_checker.py']
manifest={'status':'GLOBAL_DELTA4_PARENT_JOIN_FINAL_INDEPENDENT_REVIEW_REQUESTED','reflection_bound':32,'local_cases':local['cases'],'remote_rows':[{'charge':list(c),'bound':23 if c==(2,2,0,0)else 13,'method':'budget-free local erasure/restoration'if c[0]==1 else 'whole direct remote row proof'}for c in sorted(remote)],'five_parent1_rows':list(map(list,sorted(five))),'remote_structure_review':'remote22-proof-review/review.txt sections1--2, originalstructural1--5 unchanged','local_complete_review':'surplus-four-remote2110/local-join-review/review.txt','remote2101_complete_review':'surplus-four-remote2110/peer-2101-whole-review/review.txt','remote2110_complete_reviews':['fourth-surplus-review/'+p+'/review.txt'for p in ['peer-remote-noncritical-independent','peer-remote-critical-L-independent','peer-B-final-independent']],'pending_review':['single-BC-edge erasure/restoration of five parent1 remote rows with stronger budget-free TWOunit theorem','global18type exhaustion/source join'],'scope':'FixedSUT canonical45 strictsimple room, Delta4,W<=21,k<=6; NOlocalityhypothesis; universalminimumunproved','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(HERE/'join-check.json').write_text(json.dumps({'status':'PARENT_GLOBAL_SOURCE_AND_21_FIXED_GUARD_SUPPORT_CHECK_PASS_PENDING_FINAL_HAND_REVIEW','local_types':10,'remote_rows':list(map(list,sorted(remote))),'bound':32,'fixed_paths':details,'current_source_pins':len(manifest['source_sha256']),'limits':'21fixedpathguards/sigma, weightedchargepartitions, frozenreview/sourceidentity only. Doesnotreplacehandtopologyorfinalindependentreview. No room/ray/direction/worddiscovery.'},indent=2)+'\n')
print('PASS local10/remote8/21fixedpaths+sigmaentireK; currentpins',len(manifest['source_sha256']))
