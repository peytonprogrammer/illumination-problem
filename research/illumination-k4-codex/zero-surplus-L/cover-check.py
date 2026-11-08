"""Replay the six fixed paths used in the hand family proof; no room enumeration."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import runpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
project=json.loads((HERE/'project-guards.json').read_text())
slot_data=json.loads((HERE/'guard-incidence-check.json').read_text())['cap_options']
slots={label:tuple(sorted(map(tuple,t))) for label,t in slot_data.items()}
by_tri={t:label for label,t in slots.items()}
base=json.loads((ROOT/'cap-return-review/lookup.json').read_text())
core=frozenset(tuple(sorted(map(tuple,t))) for t in base['room'])-frozenset(slots[n] for n in ('L+','B+','E-','T-'))
assert len(core)==24
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
def sigma(p):return (2-p[1],2-p[0])
def decode(path):return [tuple(F(*v) for v in p) for p in path]
source=next(s for s in project['sources'] if 'I2_00_11' in s['path'])
data=Path(source['path']).read_bytes()
assert hashlib.sha256(data).hexdigest()==source['sha256']
four_rec=json.loads(data.splitlines()[28526])
assert four_rec['q']==[2,2]
four=decode(four_rec['path'])
assert four==[(0,0),(F(2,5),F(-8,5)),(0,F(-3,2)),(F(2,3),F(-4,3)),(F(7,4),3),(2,2)]
one=[(F(0),F(0)),(F(1,2),F(-1)),(F(2),F(2))]
thirteen=decode(base['path'])
expected={
 'one':(set(),{'B+'}),
 'four':({'B+'},{'B-','T-'}),
 'thirteen':({'B+','T-'},{'B-','L-','Nb-','Nb+','T+'}),
}
out={}
for name,path in (('one',one),('four',four),('thirteen',thirteen)):
 need,absent=checker['path_requirements'](path)
 required=frozenset(by_tri[t] for t in need-core)
 forbidden=frozenset(by_tri[t] for t in absent if t in by_tri)
 assert (set(required),set(forbidden))==expected[name],(name,required,forbidden)
 assert not absent&core
 assert checker['incident']((F(0),F(0))) <= core
 assert checker['incident']((F(2),F(2))) <= core
 for reflected in (False,True):
  p=[sigma(v) for v in path][::-1] if reflected else path
  u,z=checker['path_requirements'](p)
  if reflected:
   su=frozenset(tuple(sorted(sigma(v) for v in t)) for t in need)
   sz=frozenset(tuple(sorted(sigma(v) for v in t)) for t in absent)
   assert u==su and z==sz
  assert p[0]==(0,0) and p[-1]==(2,2)
  out[name+('_sigma' if reflected else '')]=dict(
      reflections=len(p)-2,
      required_caps=sorted(by_tri[t] for t in u-core),
      forbidden_caps=sorted(by_tri[t] for t in z if t in by_tri),
      required_tiles=sorted(u),forbidden_tiles=sorted(z),
      path=[[[v.numerator,v.denominator] if isinstance(v,F) else [v,1] for v in point] for point in p])
# Logical proof is deliberately symbolic: no cap-occupancy assignments are generated.
assert out['one']['forbidden_caps']==['B+']
assert out['one_sigma']['forbidden_caps']==['E-']
assert out['four']['required_caps']==['B+'] and out['four']['forbidden_caps']==['B-','T-']
assert out['four_sigma']['required_caps']==['E-'] and out['four_sigma']['forbidden_caps']==['E+','L+']
assert out['thirteen']['required_caps']==['B+','T-']
assert out['thirteen_sigma']['required_caps']==['E-','L+']
required_four={'B+','E-','L+','T-'}
excluded={'B-','E+','L-','T+','Nb-','Nr+'}
assert set(out['thirteen']['forbidden_caps'])-excluded=={'Nb+'}
assert set(out['thirteen_sigma']['forbidden_caps'])-excluded=={'Nr-'}
assert all(next(v for v in slots[n] if v[0]%2==v[1]%2==0)==(0,2) for n in ('Nb+','Nr-'))
result=dict(status='PASS',paths=out,
            saved_four_path_source=dict(**source,line=28527),
            implication_chain=['dark => B+ and E-',
                               'single-cap B+/E- intact and dark => T- and L+',
                               'four caps and no smooth B imply only Nb+/Nr- can block the two13paths',
                               'both blockers imply direct bridge, contradict darkness'],
            scope='Six fixed path replays and symbolic implication checks; hand classification provides all-room completeness. No room or cap-assignment enumeration.')
(HERE/'cover-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status='PASS',paths={n:v['reflections'] for n,v in out.items()}),indent=2))
