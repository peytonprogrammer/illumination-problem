"""Six fixed-path local substitutions, with exact checks; no discovery search."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
source=ROOT/'zero-surplus-L/cover-check.json'
raw=source.read_bytes()
saved=json.loads(raw)['paths']
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
labels={t:n for n,t in slots.items()}
core=frozenset().union(*(checker['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
actual=lambda row:[tuple(F(*c) for c in v) for v in row['path']]
four=actual(saved['four']);thirteen=actual(saved['thirteen'])
sigma=lambda p:(2-p[1],2-p[0])
reflect=lambda path:[sigma(p) for p in path][::-1]
Bextra=tri(((0,-2),(1,-2),(1,-1)))
Textra=tri(((2,4),(1,4),(1,3)))
Lextra=tri(((-2,0),(-2,1),(-1,1)))
Eextra=tri(((4,2),(4,1),(3,1)))
assert tri(sigma(v) for v in Bextra)==Eextra
assert tri(sigma(v) for v in Textra)==Lextra
# Each changed point is the intersection of the old entering leg with the
# square far wall. The outgoing leg has the exact same line as the old exit.
Bfour=four[:1]+[(F(1,2),F(-2))]+four[4:]
Bthirteen=thirteen[:8]+[(F(6,11),F(-2))]+thirteen[11:]
Tthirteen=thirteen[:11]+[(F(18,11),F(4))]+thirteen[14:]
assert len(Bfour)-2==2 and len(Bthirteen)-2==11 and len(Tthirteen)-2==11
reference={'L+','B+','E-','T-'}
casepaths={
 'B_four':(Bfour,Bextra,'B+',{'B+'}),
 'E_four':(reflect(Bfour),Eextra,'E-',{'E-'}),
 'B_thirteen':(Bthirteen,Bextra,'B+',{'B+','T-'}),
 'E_thirteen':(reflect(Bthirteen),Eextra,'E-',{'E-','L+'}),
 'T_thirteen':(Tthirteen,Textra,'T-',{'B+','T-'}),
 'L_thirteen':(reflect(Tthirteen),Lextra,'L+',{'E-','L+'}),
}
result={}
for name,(path,extra,critical,required) in casepaths.items():
 u,z=checker['path_requirements'](path)
 assert path[0]==(0,0) and path[-1]==(2,2)
 assert u-core==frozenset({slots[x] for x in required}|{extra})
 assert not z&core and extra not in z
 forbidden={labels[t] for t in z if t in labels}
 if name.endswith('four'):
  opposite='T-' if name.startswith('B') else 'L+'
  assert not(forbidden & required) and opposite in forbidden
 else:
  # For any completed reference-cap family, opposite caps at B/E/L/T
  # are unavailable; only the corresponding N side can block the path.
  excluded={'L-','B-','E+','T+'}
  residual=forbidden-excluded
  expect={'Nb-','Nb+'} if name in ('B_thirteen','T_thirteen') else {'Nr-','Nr+'}
  assert residual==expect,(name,residual,expect)
 # Every forbidden non-alphabet triangle is absent in this one-square class:
 # it is neither the unique extra triangle nor part of any ordinary single cap.
 outside=[t for t in z if t not in labels]
 assert extra not in outside
 result[name]={'reflections':len(path)-2,'required_caps':sorted(required),
 'required_extra':extra,'forbidden_caps':sorted(forbidden),
 'forbidden_outside_alphabet':sorted(outside),'path':[[[c.numerator,c.denominator] for c in v] for v in path]}
# Reflection/reversal is checked from actual recomputed universal implications.
for a,b in (('B_four','E_four'),('B_thirteen','E_thirteen'),('T_thirteen','L_thirteen')):
 ua,za=checker['path_requirements'](casepaths[a][0]);ub,zb=checker['path_requirements'](casepaths[b][0])
 assert ub==frozenset(tri(sigma(p) for p in t) for t in ua)
 assert zb==frozenset(tri(sigma(p) for p in t) for t in za)
output={'status':'PASS','source_sha256':hashlib.sha256(raw).hexdigest(),'paths':result,
 'scope':'Fixed analytic triangle-to-square substitutions into six archived paths only. No cap assignments, rooms, directions or words enumerated. Hand argument supplies family completeness.'}
(HERE/'square-exchange-check.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'status':'PASS','paths':{n:{'reflections':v['reflections'],'forbidden_caps':v['forbidden_caps']} for n,v in result.items()}},indent=2))
