"""Static local unit-fan exhaustion and H4 proof dispatch, no room census.
No geometry/search import, no peer code execution, no optical discovery.
"""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
A={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(site,sectors):
 a=A[site] if isinstance(site,str) else site
 return {tuple(sorted((a,(a[0]+R[i][0],a[1]+R[i][1]),(a[0]+R[(i+1)%8][0],a[1]+R[(i+1)%8][1])))) for i in sectors}
def decode(x):return {tuple(sorted(tuple(p) for p in t)) for t in x}
def angle(ts,p):
 total=0
 for t in ts:
  if p in t:
   a,b=[(v[0]-p[0],v[1]-p[1]) for v in t if v!=p]
   total+=90 if a[0]*b[0]+a[1]*b[1]==0 else 45
 return total
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]));B=fan('B',[7,0,1,2])
verified=json.loads((HERE/'verification.json').read_text())
assert verified['status']=='FROZEN_ONE_ROOM_THREE_PATH_AND_WHOLE_SUPPORT_PASS'
U=decode(verified['whole_support']['required']);Z=decode(verified['whole_support']['forbidden'])
maximum=decode(verified['whole_support']['maximum']);minimum=H|B
assert U<=minimum and not Z&maximum
# Each listed pair of inward sectors belongs to ONE H-facing side, hence
# touching either or both halves counts d=1. N has TWO different H sides.
# This same side-touch convention is an inherited root-class prerequisite.
faces={'L':[{7,0}],'D':[{1,2}],'R':[{3,4}],'E':[{3,4}],'Tc':[{5,6}],'N':[{5,6},{7,0}]}
expected={'L':[{6,7},{7,0},{0,1}],'D':[{0,1},{1,2},{2,3}],
 'R':[{2,3},{3,4},{4,5}],'E':[{2,3},{3,4},{4,5}],
 'Tc':[{4,5},{5,6},{6,7}],'N':[{4,5},{5,6},{7,0},{0,1}]}
local_windows={};dispatch=[]
for site,inward_faces in faces.items():
 units=[]
 for start in range(8):
  sectors={start,(start+1)%8}
  touched=sum(bool(sectors&face) for face in inward_faces)
  if touched!=1:continue
  # The direct N bridge is handled before the e1-root classification.
  assert not (site=='N' and {6,7}<=sectors)
  units.append(sectors)
 assert {frozenset(s) for s in units}=={frozenset(s) for s in expected[site]}
 local_windows[site]=[sorted(s) for s in units]
 for sectors in units:
  label=site+''.join(map(str,sorted(sectors)));ts=fan(site,sectors)
  rec={'unit_site':site,'sectors':sorted(sectors),'label':label}
  if site=='L' and 0 not in sectors:
   rec.update(dispatch='REFERENCE_FORCING_EXCEPTION',bound=4,reason='ordinary E4 forces L0 by accepted four_sigma')
  elif site=='E' and 4 not in sectors:
   rec.update(dispatch='REFERENCE_FORCING_EXCEPTION',bound=1,reason='absent E4 invokes accepted one_sigma')
  elif site=='L' and 7 in sectors:
   assert sectors=={7,0}
   fixed=H|B|ts
   assert angle(fixed,(1,-2))==angle(fixed,(-1,-1))==180
   ordinary={'D':[1,2],'R':[3,4],'E':[4],'Tc':[5,6],'N':[0,5,6,7]}
   for p in [(1,-2),(-1,-1)]:
    assert all(angle(fan(k,[s]),p)==0 for k,ss in ordinary.items() for s in ss)
   rec.update(dispatch='IMPOSSIBLE_AT_B1',reason='two unhealable extra180 non-A points',points=[[1,-2],[-1,-1]])
  elif site=='D' and 3 in sectors:
   assert sectors=={2,3}
   rec.update(dispatch='ACCEPTED_FOUR_SIX_ORDINARY_TC_SPLIT',bound=6)
  else:
   assert minimum|ts<=maximum and U<=minimum|ts and not Z&(maximum|ts)
   rec.update(dispatch='NEW_THREE_WHOLE_ENVELOPE',bound=3)
  dispatch.append(rec)
assert sum(map(len,local_windows.values()))==19
from collections import Counter
counts=Counter(r['dispatch'] for r in dispatch)
assert counts=={'REFERENCE_FORCING_EXCEPTION':2,'IMPOSSIBLE_AT_B1':1,'ACCEPTED_FOUR_SIX_ORDINARY_TC_SPLIT':1,'NEW_THREE_WHOLE_ENVELOPE':15}
# Accepted forcing clauses are checked by receipt identity, not rerun.
forcing_source=BASE/'surplus-four-local/e2-e1-b1/critical-B-check.json'
forcing=json.loads(forcing_source.read_text())
forces={r['name']:r for r in forcing['whole_envelopes'] if r['name'].startswith('force_')}
assert forces['force_E4']['reflections']==1
assert forces['force_L0_Eordinary']['reflections']==4
assert forces['force_L0_Ecenter']['reflections']==3
assert forces['force_L0_Eouter']['reflections']==2
# Match D23 exception to independently accepted optical triangle guards.
oldsource=BASE/'fourth-surplus-review/mixed-e2-e1/joined-four-check.json'
old=json.loads(oldsource.read_text());accepted_source=BASE/'surplus-four-local/joined-six-review/check.json';accepted=json.loads(accepted_source.read_text())
assert hashlib.sha256(oldsource.read_bytes()).hexdigest()==accepted['source_sha256'][str(oldsource.relative_to(BASE))]
D23=fan('D',[2,3]);T5=fan('Tc',[5]);other=set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
for rec,mi,ma in [(old,H|B|D23,H|B|D23|other|fan('Tc',[0,1,2,3,4,6,7])),(old['six_path_complement'],H|B|D23|T5,H|B|D23|T5|other)]:
 u,z=decode(rec['required']),decode(rec['forbidden'])
 assert u<=mi and not z&ma
assert max(r.get('bound',0) for r in dispatch)==6
sources=[HERE/'findings.txt',HERE/'verification.json',forcing_source,oldsource,accepted_source,BASE/'fourth-surplus-review/peer-critical-B-b1-independent/review.txt']
result={'status':'PARENT_H4_LOCAL_PARTNER_EXHAUSTION_PASS','local_unit_windows':local_windows,'dispatch':dispatch,'counts':dict(counts),'maximum_bound':6,'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Static cyclic local m2 fan exhaustion, not room/cap-assignment enumeration or another discovery search. Inherits root/leaf and H-side-touch definition, b/M interpretation, reference forcing and independently accepted D23 optics. Parent corroboration; independent new3/H4 peer review still pending.'}
(HERE/'H4-partner-coverage.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS:19 local unit-root windows;15 fit new3,2 forcing exceptions<=4,LC impossibleatb1,D23accepted<=6. No room/search/cap census.')
