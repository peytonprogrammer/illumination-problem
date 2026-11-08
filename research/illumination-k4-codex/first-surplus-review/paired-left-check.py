"""Static replay of three prescribed saved paths; no discovery or room census."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import runpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
source=ROOT/'exception-geometry/shared-extensions-check.json'
data=source.read_bytes()
w=json.loads(data)['rooms']['A_left_repair']['witness']
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={name:tri(t) for name,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
labels={t:name for name,t in slots.items()}
core=frozenset().union(*(checker['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
path=[tuple(F(*v) for v in pt) for pt in w['path']]
u,z=checker['path_requirements'](path)
assert frozenset(map(tri,w['required']))==u
assert frozenset(map(tri,w['forbidden']))==z
assert path[0]==(0,0) and path[-1]==(2,2)
assert {labels[t] for t in u-core}=={'B+','D-'}
assert {labels[t] for t in z if t in labels}=={'B-','D+','Nb+','R-','T+'}
assert not z&core
outside=[t for t in z if t not in labels]
assert len(outside)==2
assert not any(t in outside for t in (slots['L+'],slots['L-']))
# All geometric points are expressions for a fixed already-saved itinerary.
d=F(2,11)
formula=[(F(0),F(0)),(2*d/(1+d),-2/(1+d)),(F(0),2*d-2),
 (2*d/(1-d),2*d/(1-d)-2),(5*d,F(1)),
 (6*d/(1-d),-6*d/(1-d)),(F(2),-8*d),
 (10*d/(1+d),-10*d/(1+d)),(13*d,F(3)),
 (F(3),16-3/d),(6-17*d,F(-1)),(6-21*d,F(3)),(6-22*d,F(2))]
assert formula==path
# The open parameter interval is derived by wall/portal containment, not sampled.
lo,hi=F(3,17),F(3,16)
assert lo<d<hi
# The two ends of this interval respectively keep the bottom bounce left of x3,
# and the right-wall bounce strictly below y0. All further strict bounds below
# hold on the full interval by monotonicity of these affine expressions.
for t in (lo,hi):
 assert F(1,7)<t<F(1,5)
 assert 1<9*t<2 and 1<11*t<3 and 2<13*t<3
 assert 2<15*t<3 and 2<=6-17*t<=3
 assert 2<6-21*t<3
# Sigma maps paired-left to paired-top, with actual endpoints reversed back.
sigma=lambda p:(2-p[1],2-p[0])
reflected=[sigma(p) for p in path][::-1]
ur,zr=checker['path_requirements'](reflected)
assert ur==frozenset(tri(sigma(p) for p in t) for t in u)
assert zr==frozenset(tri(sigma(p) for p in t) for t in z)
# Bounded second attempt: the other two ALREADY SELECTED witnesses cannot
# extend coverage to a paired-left room. This inspects fixed paths, not rooms.
other={}
source_rooms=json.loads(data)['rooms']
for name in ('B_bottom_repair','C_roof'):
 ow=source_rooms[name]['witness']
 op=[tuple(F(*v) for v in pt) for pt in ow['path']]
 ou,oz=checker['path_requirements'](op)
 assert ou==frozenset(map(tri,ow['required']))
 assert oz==frozenset(map(tri,ow['forbidden']))
 for reflected_flag in (False,True):
  pp=[sigma(v) for v in op][::-1] if reflected_flag else op
  uu,zz=checker['path_requirements'](pp)
  rc={labels[t] for t in uu-core}
  fc={labels[t] for t in zz if t in labels}
  if name=='B_bottom_repair':
   # Requires a second defect in B, or after sigma in E.
   assert ({'E-','E+'} if reflected_flag else {'B-','B+'})<=rc
   reason='requires two triangles in an ordinary B/E cell'
  elif reflected_flag:
   assert {'T-','Nr+'}<=rc
   reason='requires T- and Nr+, making forbidden smooth B at (1,3)'
  else:
   assert 'L-' in fc
   reason='requires absence of L-, which is present in the paired-left defect'
  other[name+('_sigma' if reflected_flag else '')]={'required_caps':sorted(rc),'forbidden_caps':sorted(fc),'exclusion_reason':reason}
result={'status':'PASS' ,'source':str(source),'source_sha256':hashlib.sha256(data).hexdigest(),
 'frozen_guard_line':w['source_line'],'reflections':len(path)-2,
 'required_caps':sorted(labels[t] for t in u-core),
 'forbidden_caps':sorted(labels[t] for t in z if t in labels),
 'forbidden_outside_single_cap_alphabet':sorted(outside),
 'sigma_required_caps':sorted(labels[t] for t in ur-core),
 'sigma_forbidden_caps':sorted(labels[t] for t in zr if t in labels),
 'other_prescribed_witnesses':other,'parameter_interval':['3/17','3/16'],'target_equation':'6-22d=2','d':'2/11',
 'scope':'Three previously selected shared-extension paths and isometric reverses; only fixed path implications and symbolic formula checks. No room assignments generated.'}
(HERE/'paired-left-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
