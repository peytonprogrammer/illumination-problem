"""Replay the one prescribed saved six-path; no discovery search."""
from fractions import Fraction as F
from pathlib import Path
import json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
term=json.loads((HERE/'bottom-residual-projection.json').read_text())['undominated_terms'][0]
path=[tuple(F(*c) for c in p) for p in term['path']]
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()};labels={t:n for n,t in slots.items()}
core=frozenset().union(*(checker['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
u,z=checker['path_requirements'](path)
assert path==[(0,0),(-F(1,6),1),(-F(4,7),-F(10,7)),(F(4,5),-F(6,5)),(F(8,5),F(18,5)),(2,F(11,3)),(F(12,7),F(26,7)),(2,2)]
assert not z&core
required={labels[t] for t in u-core};forbidden={labels[t] for t in z if t in labels}
assert required=={'B-','B+','T-'}
assert forbidden=={'Nb-','T+'}
d=F(1,6)
formula=[(F(0),F(0)),(-d,F(1)),(-4*d/(1+d),4*d/(1+d)-2),
 (4*d/(1-d),4*d/(1-d)-2),(8*d/(1-d),8*d/(1-d)+2),
 (F(2),2+10*d),(12*d/(1+d),12*d/(1+d)+2),(12*d,F(2))]
assert formula==path
assert F(1,7)<d<F(2,11)
# Shared two-hit branch is u=-3d, entering tangent=-d; exit=5d.
assert -1 < -3*d < 1 and -1 < -5*d < 1 and -4*d!=0
assert 0<2-9*d<1 and 0<2-11*d<1
sigma=lambda p:(2-p[1],2-p[0])
reflected=[sigma(p) for p in path][::-1]
ur,zr=checker['path_requirements'](reflected)
assert ur==frozenset(tri(sigma(v) for v in t) for t in u)
assert zr==frozenset(tri(sigma(v) for v in t) for t in z)
result={'status':'PASS','reflections':6,'required_caps':sorted(required),'forbidden_caps':sorted(forbidden),
 'forbidden_outside_alphabet':sorted(t for t in z if t not in labels),
 'path':term['path'],'parameter_interval':'1/7<d<2/11','actual_target_equation':'12d=2','d':'1/6',
 'sigma_required_caps':sorted(labels[t] for t in ur-core),'sigma_forbidden_caps':sorted(labels[t] for t in zr if t in labels),
 'provenance':{k:term[k] for k in ('source','source_sha256','line','frame','sigma_reversed')},
 'scope':'One fixed archived six-reflection path plus sigma, exact universal implication and analytic formula checks; no room assignments.'}
(HERE/'bottom-residual-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
