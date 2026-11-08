"""Frozen guard projection for nine explicitly hand-reduced single-fan cases."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
archive=ROOT.parent/'claude-illumination-check/k6-run/cases/I3_00_01_10-pair0/guards.jsonl'
raw=archive.read_bytes();records=[json.loads(v) for v in raw.splitlines()]
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
core=set().union(*(check['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,m):
 return {tri((a,(a[0]+dirs[i%8][0],a[1]+dirs[i%8][1]),(a[0]+dirs[(i+1)%8][0],a[1]+dirs[(i+1)%8][1]))) for i in range(start,start+m)}
dw=tri(((2,-2),(1,-2),(1,-1)))
configs={
 'Lupper_Ecenter':((-2,0),7,3,['E-','E+'],['B+','T-','Nb-'],['D-','D+','R-','R+']),
 'Bwest_Lcenter':((0,-2),1,3,['L-','L+'],['E-'],['D-','D+','R-','R+','Nb+','Nr-','Nr+','T-','T+']),
 'Brectangle_Lcenter_Nrminus':((0,-2),0,4,['L-','L+'],['E-','T-','Nr-'],['D-','D+','R-','R+']),
 'BDjoin_Bouter3':((0,-2),7,3,['D-'],['L+','E-'],['R-','R+','Nb+','Nr-','Nr+','T-','T+']),
 'BDjoin_Bouter4':((0,-2),6,4,['D-'],['L+','E-'],['R-','R+','Nb+','Nr-','Nr+','T-','T+']),
 'BDjoin_BHeast4':((0,-2),7,4,['D-'],['L+','E-'],['R-','R+','Nb+','Nr-','Nr+','T-','T+']),
}
transformed=[]
for line,r in enumerate(records,1):
 assert r['q']==[2,-2]
 for frame,base in [('flip_y',lambda p:(p[0],-p[1])),('rotate90',lambda p:(-p[1],p[0]))]:
  for reverse in (False,True):
   cv=(lambda p:(2-base(p)[0],2-base(p)[1])) if reverse else base
   transformed.append((line,frame,reverse,{tri(cv(v) for v in t) for t in r['U']},{tri(cv(v) for v in t) for t in r['Z']},r,cv))
# Store frames by value: closures above are not retained for executing paths.
def convert(frame,reverse,p):
 q=(p[0],-p[1]) if frame=='flip_y' else (-p[1],p[0])
 return (2-q[0],2-q[1]) if reverse else q
out={}
for name,(a,start,m,unit,present,variable_names) in configs.items():
 fixed=core|fan(a,start,m)|{slots[n] for n in present+unit}
 if name.startswith('BDjoin'):fixed.add(dw)
 variables={n:slots[n] for n in variable_names};labels={t:n for n,t in variables.items()};possible=fixed|set(variables.values());terms={}
 for line,frame,reverse,U,Z,r,_ in transformed:
  if not U<=possible or Z&fixed:continue
  need=frozenset(labels[t] for t in U-fixed);absent=frozenset(labels[t] for t in Z&possible)
  if need&absent:continue
  groups=[{'D-','D+'},{'R-','R+'},{'Nb+','Nr-','Nr+'},{'T-','T+'}]
  if any(len(need&g)>1 for g in groups) or {'Nr+','T-'}<=need:continue
  key=(need,absent)
  if key in terms:continue
  path=[convert(frame,reverse,tuple(F(*v) for v in p)) for p in r['path']]
  if reverse:path.reverse()
  assert path[0]==(0,0) and path[-1]==(2,2)
  u,z=check['path_requirements'](path)
  assert u<=fixed|{variables[n] for n in need} and not z&(possible-{variables[n] for n in absent})
  terms[key]={'requires':sorted(need),'forbids':sorted(absent),'source_line':line,'frame':frame,'endpoint_reversal':reverse,'reflections':len(path)-2,'path':[[[v.numerator,v.denominator] for v in p] for p in path],'required_triangles':sorted(u),'forbidden_triangles':sorted(z)}
 minimal=[v for (u,z),v in terms.items() if not any((u2,z2)!=(u,z) and u2<=u and z2<=z for u2,z2 in terms)]
 minimal.sort(key=lambda v:(len(v['requires'])+len(v['forbids']),v['requires'],v['forbids']))
 out[name]={'fan':sorted(fan(a,start,m)),'fixed_triangles':sorted(fixed),'variables':variables,'terms':minimal}
result={'status':'PROJECTION_ONLY','source':str(archive),'sha256':hashlib.sha256(raw).hexdigest(),'records':len(records),'families':out,'scope':'Nine explicitly hand-listed single-fan symbolic cases; no assembled room assignments or new trajectories, directions, words, solver.'}
(HERE/'local-mixed-project.json').write_text(json.dumps(result,indent=2)+'\n')
for name,v in out.items():
 print(name,json.dumps([{k:t[k] for k in ['requires','forbids','source_line','reflections']} for t in v['terms']]))
