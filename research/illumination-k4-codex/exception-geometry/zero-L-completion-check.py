"""Static six-path illumination cover for the hand-classified equality family.
Two prescribed saved records and four symmetry/manual paths; no room or
cap-assignment enumeration, solver, or path/direction generation.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_path_implication',HERE.parent/'persisted-replay/audit.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
cap=lambda *v:tuple(sorted(v))
B=cap((0,-2),(0,-1),(1,-1));E=cap((4,2),(3,1),(3,2))
L=cap((-2,0),(-1,0),(-1,1));T=cap((2,4),(1,3),(2,3))
Bminus=cap((0,-2),(-1,-1),(0,-1));Eplus=cap((4,2),(3,2),(3,3))
Lminus=cap((-2,0),(-1,-1),(-1,0));Tplus=cap((2,4),(2,3),(3,3))
Nbminus=cap((0,2),(-1,1),(0,1));Nbplus=cap((0,2),(0,1),(1,1))
Nrminus=cap((0,2),(1,1),(1,2));Nrplus=cap((0,2),(1,2),(1,3))
centers=((0,0),(2,0),(2,2))
core=frozenset().union(*(a.incident(tuple(map(F,c))) for c in centers))
options=set()
for x,y in centers:
 for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
  A=(x+2*dx,y+2*dy)
  if A in centers:continue
  C=(x+dx,y+dy)
  for sign in (-1,1):options.add(cap(A,C,(C[0]-sign*dy,C[1]+sign*dx)))
assert len(options)==16
sigma=lambda v:(2-v[1],2-v[0])
reflect_reverse=lambda p:tuple(sigma(v) for v in reversed(p))
maptris=lambda ts:frozenset(cap(*(sigma(v) for v in t)) for t in ts)
manifest=json.loads((HERE.parent/'lower-bound-proof-audit/full-replay/manifest.json').read_text())
source_receipts=[]
def saved(relative,line_number):
 p=HERE.parent.parent/relative
 expected=next(r['sha256'] for r in manifest['guards'] if Path(r['path'])==p.resolve())
 assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
 with p.open() as f:rec=next(json.loads(v) for i,v in enumerate(f,1) if i==line_number)
 checked=a.check_record(rec,tuple(rec['q']),False)
 source_receipts.append({'file':str(p.resolve()),'line':line_number,'sha256':expected,'guard_check':checked})
 return tuple(tuple(F(*c) for c in v) for v in rec['path'])
p4=saved('claude-illumination-check/k6-run/cases/I2_00_11-pair0/guards.jsonl',28527)
p13_raw=saved('claude-illumination-check/k6-run/cases/I3_00_01_10-pair0/guards.jsonl',60)
p13=tuple((-v[1],v[0]) for v in p13_raw)
source,target=(F(0),F(0)),(F(2),F(2))
paths={'bottom_one':(source,(F(1,2),F(-1)),target),
       'east_one':(source,(F(3),F(3,2)),target),
       'bottom_cap_four':p4,'east_cap_four':reflect_reverse(p4),
       'bottom_top_thirteen':p13,'left_east_thirteen':reflect_reverse(p13)}
rows={}
for name,p in paths.items():
 assert p[0]==source and p[-1]==target
 need,z=a.path_requirements(p)
 outside=frozenset(need)-core
 assert outside<=options
 rows[name]={'reflections':len(p)-2,'required_caps':sorted(outside),
  'forbidden_cap_choices':sorted(z&options),'unavailable_forbidden_tiles':sorted(z-options),
  'path':[[[v.numerator,v.denominator] for v in pt] for pt in p]}

tri=lambda ts:frozenset(tuple(map(tuple,t)) for t in ts)
# Direct set assertions representing each step of the HAND decision proof.
assert tri(rows['bottom_one']['required_caps'])==set()
assert tri(rows['bottom_one']['forbidden_cap_choices'])=={B}
assert tri(rows['east_one']['required_caps'])==set()
assert tri(rows['east_one']['forbidden_cap_choices'])=={E}
assert tri(rows['bottom_cap_four']['required_caps'])=={B}
assert tri(rows['bottom_cap_four']['forbidden_cap_choices'])=={Bminus,T}
assert tri(rows['east_cap_four']['required_caps'])=={E}
assert tri(rows['east_cap_four']['forbidden_cap_choices'])=={Eplus,L}
# Four reference caps present, with same-cell and no-smooth-B exclusions.
known_excluded={Bminus,Eplus,Lminus,Tplus,Nbminus,Nrplus}
assert tri(rows['bottom_top_thirteen']['required_caps'])=={B,T}
assert tri(rows['bottom_top_thirteen']['forbidden_cap_choices'])-known_excluded=={Nbplus}
assert tri(rows['left_east_thirteen']['required_caps'])=={E,L}
assert tri(rows['left_east_thirteen']['forbidden_cap_choices'])-known_excluded=={Nrminus}
assert a.incident((F(1),F(1)))<=core|{Nbplus,Nrminus}
need_direct,z_direct=a.path_requirements((source,target))
assert need_direct<=core|{Nbplus,Nrminus} and not z_direct

# Exact hand formula for the new four-reflection route.
def four_family(d):
 return (source,(2*d/(1+d),-2/(1+d)),(F(0),2*d-2),
         (2*d/(1-d),(4*d-2)/(1-d)),(7*d,F(3)),(8*d,F(2)))
d=F(1,4)
assert F(1,5)<d<F(2,7)
assert four_family(d)==p4
assert 3*d<1 and 5*d>1 and 1<7*d<2
# Transform/reversal uses actual S/T, not source/target labels modulo a fold.
for original,other in ((p4,paths['east_cap_four']),(p13,paths['left_east_thirteen'])):
 u,z=a.path_requirements(original);u2,z2=a.path_requirements(other)
 assert maptris(u)==u2 and maptris(z)==z2
result={'status':'PASS','sources':source_receipts,'paths':rows,
 'four_reflection_formula_parameter':'1/4','four_reflection_interval':['1/5','2/7'],
 'direct_bridge':'PASS','maximum_reflections_needed':13,
 'scope':'Static implications of six fixed paths plus the direct midpoint bridge, over the hand-classified exact-zero-surplus I3/L-support family. No cap-assignment census, solving, or discovery. Full-family completeness is the hand decision proof.'}
(HERE/'zero-L-completion-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','sources':source_receipts,'verified_path_reflections':{k:v['reflections'] for k,v in rows.items()},'direct_bridge':'PASS','full_family_reflection_bound':13},indent=2))
