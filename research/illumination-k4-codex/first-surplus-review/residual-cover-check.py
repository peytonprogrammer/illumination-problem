"""Verify the one prescribed archived short path; no discovery search."""
from fractions import Fraction as F
from pathlib import Path
import json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
term=json.loads((HERE/'residual-projection.json').read_text())['undominated_terms'][0]
path=[tuple(F(*c) for c in p) for p in term['path']]
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
labels={t:n for n,t in slots.items()}
core=frozenset().union(*(checker['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
u,z=checker['path_requirements'](path)
assert path==[(0,0),(F(6,7),-F(8,7)),(-F(10,7),F(4,7)),(-F(1,4),-1),(2,2)]
assert path[0]==(0,0) and path[-1]==(2,2)
assert not z&core
required={labels[t] for t in u-core}
forbidden={labels[t] for t in z if t in labels}
assert required=={'B+','L+','L-'}
assert forbidden=={'B-'}
# At the center of the left mouth, all four incident90-degree quadrants are
# occupied precisely because both L caps fill the two left quadrants.
base=core|frozenset(slots[n] for n in required)
assert checker['incident']((F(-1),F(0)))<=base
assert not checker['incident']((F(-1),F(0)))<=base-{slots['L-']}
assert not z&base
sigma=lambda p:(2-p[1],2-p[0])
reflected=[sigma(p) for p in path][::-1]
ur,zr=checker['path_requirements'](reflected)
assert ur==frozenset(tri(sigma(v) for v in t) for t in u)
assert zr==frozenset(tri(sigma(v) for v in t) for t in z)
result={'status':'PASS','reflections':3,'required_caps':sorted(required),'forbidden_caps':sorted(forbidden),
 'forbidden_outside_alphabet':sorted(t for t in z if t not in labels),
 'newly_interior_point':[-1,0],'sigma_required_caps':sorted(labels[t] for t in ur-core),
 'sigma_forbidden_caps':sorted(labels[t] for t in zr if t in labels),
 'path':term['path'],'provenance':{k:term[k] for k in ('source','source_sha256','line','frame')},
 'scope':'One fixed archived path and sigma/reversal, exact universal implication and newlyinteriorC check; no room assignments generated.'}
(HERE/'residual-cover-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
