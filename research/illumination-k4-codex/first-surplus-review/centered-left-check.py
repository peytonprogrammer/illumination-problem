"""One centered-left prefix substitution and sigma; no discovery search."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
source=ROOT/'zero-surplus-L/cover-check.json';raw=source.read_bytes()
old=[tuple(F(*c) for c in p) for p in json.loads(raw)['paths']['thirteen_sigma']['path']]
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
labels={t:n for n,t in slots.items()}
core=frozenset().union(*(checker['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
d=F(2,11)
first=(-2/(1+d),-2*d/(1+d))
second=(2*(2*d-1)/(1-d),2*d/(1-d))
assert first==(-F(22,13),-F(4,13)) and second==old[3]
new=old[:1]+[first,second]+old[4:]
assert len(new)-2==12
formula=[(F(0),F(0)),first,second,
 ((2+4*d)/(1-d),6*d/(1-d)),(2+8*d,F(2)),
 ((2+12*d)/(1+d),10*d/(1+d)),
 (F(1),11*d),(F(3),13*d),(F(1),15*d),
 (3/d-14,F(3)),(F(3),6-17*d),(F(1),6-19*d),
 (F(3),6-21*d),(F(2),6-22*d)]
assert formula==new
sigma=lambda p:(2-p[1],2-p[0])
results={}
for reflected in (False,True):
 path=[sigma(p) for p in new][::-1] if reflected else new
 u,z=checker['path_requirements'](path)
 assert path[0]==(0,0) and path[-1]==(2,2)
 expected={'L+','L-','E-'} if not reflected else {'T-','T+','B+'}
 assert u-core==frozenset(slots[n] for n in expected)
 assert not z&core and not z&u
 fc={labels[t] for t in z if t in labels}
 if not reflected:assert fc=={'E+','Nr+','Nr-','T+'}
 else:assert fc=={'B-','Nb-','Nb+','L-'}
 results['top' if reflected else 'left']={'reflections':12,'required_caps':sorted(expected),'forbidden_caps':sorted(fc),
 'forbidden_outside_alphabet':sorted(t for t in z if t not in labels),
 'path':[[[v.numerator,v.denominator] for v in p] for p in path]}
# On the whole inherited open interval, the new centered-left prefix remains
# strictly inside the two diagonal sides and returns to the unchanged line.
lo,hi=F(3,17),F(4,21)
assert 0<lo<d<hi<F(1,3)
# Entry(-1,-d) returns(-1,3d),(1,d). Its singularity parameter is -2d,
# and both portal coordinates are strict for 0<d<1/3.
result={'status':'PASS','source_sha256':hashlib.sha256(raw).hexdigest(),'d':'2/11',
 'strict_prefix_interval':'0<d<1/3','hand_derived_tail_interval':'3/17<d<4/21','actual_target_equation':'6-22d=2',
 'paths':results,'scope':'One analytic initial-velocity/prefix replacement in a fixed old path, plus sigma/reversal; no room or ray discovery.'}
(HERE/'centered-left-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','paths':{n:{'reflections':r['reflections'],'required_caps':r['required_caps'],'forbidden_caps':r['forbidden_caps']} for n,r in results.items()}},indent=2))
