"""Project a frozen archive onto one hand-specified symbolic family."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
archive=ROOT.parent/'claude-illumination-check/k6-run/cases/I3_00_01_10-pair0/guards.jsonl'
raw=archive.read_bytes()
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
core=set().union(*(check['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
west_up=tri(((0,-2),(-1,-2),(-1,-1)))
west_down=tri(((0,-2),(-1,-2),(-1,-3)))
leaf=tri(((-2,-2),(-1,-2),(-1,-1)))
fixed=core|{slots[n] for n in ['B-','B+','L+','E-']}|{west_up,west_down,leaf}
variables={n:slots[n] for n in ['D-','D+','R-','R+','Nb+','Nr-','Nr+','T-','T+']}
labels={v:n for n,v in variables.items()};possible=fixed|set(variables.values())
terms={}
for line,row in enumerate(raw.splitlines(),1):
 r=json.loads(row);assert r['q']==[2,-2]
 for frame,base in [('flip_y',lambda p:(p[0],-p[1])),('rotate90',lambda p:(-p[1],p[0]))]:
  for reverse in (False,True):
   cv=(lambda p:(2-base(p)[0],2-base(p)[1])) if reverse else base
   U={tri(cv(v) for v in t) for t in r['U']};Z={tri(cv(v) for v in t) for t in r['Z']}
   if not U<=possible or Z&fixed:continue
   required=frozenset(labels[t] for t in U-fixed);forbidden=frozenset(labels[t] for t in Z&possible)
   if required&forbidden:continue
   groups=[{'D-','D+'},{'R-','R+'},{'Nb+','Nr-','Nr+'},{'T-','T+'}]
   if any(len(required&g)>1 for g in groups):continue
   if {'Nr+','T-'}<=required:continue

   key=(required,forbidden)
   if key in terms:continue
   path=[cv(tuple(F(*v) for v in p)) for p in r['path']]
   if reverse:path.reverse()
   assert path[0]==(0,0) and path[-1]==(2,2)
   need,absent=check['path_requirements'](path)
   assert need<=fixed|{variables[n] for n in required}
   assert not absent&(possible-{variables[n] for n in forbidden})
   terms[key]={'requires':sorted(required),'forbids':sorted(forbidden),'source_line':line,'frame':frame,'endpoint_reversal':reverse,'reflections':len(path)-2,'path':[[[v.numerator,v.denominator] for v in p] for p in path],'required_triangles':sorted(need),'forbidden_triangles':sorted(absent)}
# Pure propositional absorption of redundant guard terms, no room assignments.
minimal=[v for (u,z),v in terms.items() if not any((u2,z2)!=(u,z) and u2<=u and z2<=z for u2,z2 in terms)]
minimal.sort(key=lambda v:(len(v['requires'])+len(v['forbids']),v['requires'],v['forbids']))
out={'status':'PROJECTION_ONLY','source':str(archive),'sha256':hashlib.sha256(raw).hexdigest(),'records_read':len(raw.splitlines()),'fixed_triangles':sorted(fixed),'variable_triangles':variables,'terms':minimal,'scope':'One symbolic family, one frozen archive, exact fixed-path guards; no room assignments, new trajectories, directions, words, or solver.'}
(HERE/'remote-B-project.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{k:v[k] for k in ['requires','forbids','source_line','reflections']} for v in minimal],indent=2))
