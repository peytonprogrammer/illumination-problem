"""Nine hand-reduced inputs against one previously used frozen guard archive."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
archive=ROOT.parent/'claude-illumination-check/k6-run/cases/I3_00_01_10-pair0/guards.jsonl'
raw=archive.read_bytes(); records=[json.loads(s) for s in raw.splitlines()];assert len(records)==3896
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
core=set().union(*(checker['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,m):
 return {tri((a,(a[0]+dirs[i%8][0],a[1]+dirs[i%8][1]),(a[0]+dirs[(i+1)%8][0],a[1]+dirs[(i+1)%8][1]))) for i in range(start,start+m)}
Lvars=['D-','D+','R-','R+','Nb-','Nb+','Nr-']
Bvars=['D-','D+','R-','R+','Nb+','Nr-','Nr+','T-','T+']
configs={
 'L_fullH_leftquarter':((-2,0),7,4,(-2,2),4,['B+','E-','T-'],Lvars),
 'L_fullH_rightquarter':((-2,0),7,4,(-2,2),6,['B+','E-','T-'],Lvars),
 'L_fullH_center':((-2,0),7,4,(-2,2),5,['B+','E-','T-'],Lvars),
 'B_fullW_upperquarter':((0,-2),1,4,(-2,-2),0,['E-','L+'],Bvars),
 'B_fullW_center':((0,-2),1,4,(-2,-2),7,['E-','L+'],Bvars),
 'B_west_triple_center':((0,-2),1,3,(-2,-2),7,['E-','L+'],Bvars),
 'B_rectangle_center':((0,-2),0,4,(-2,-2),7,['E-','L+'],Bvars),
 'fixed_L_northquarter_Nrminus':((-2,0),7,3,(-2,2),5,['B+','E-','T-','Nr-'],[]),
 'fixed_L_northtriple_Nbminus':((-2,0),0,3,(-2,2),5,['B+','E-','T-','Nb-'],[]),
}
def convert(frame,reverse,p):
 v=(p[0],-p[1]) if frame=='flip_y' else (-p[1],p[0])
 return (2-v[0],2-v[1]) if reverse else v
transforms=[]
for line,r in enumerate(records,1):
 assert r['q']==[2,-2]
 for frame in ('flip_y','rotate90'):
  for rev in (False,True):
   cv=lambda p:convert(frame,rev,p)
   transforms.append((line,frame,rev,{tri(cv(v) for v in t) for t in r['U']},{tri(cv(v) for v in t) for t in r['Z']},r))
results={}
for name,(a,st,m,la,ls,present,varnames) in configs.items():
 fixed=core|fan(a,st,m)|fan(la,ls,2)|{slots[n] for n in present}
 variables={n:slots[n] for n in varnames};labels={t:n for n,t in variables.items()};possible=fixed|set(variables.values());terms={}
 for line,frame,rev,U,Z,r in transforms:
  if not U<=possible or Z&fixed:continue
  need=frozenset(labels[t] for t in U-fixed);absent=frozenset(labels[t] for t in Z&possible)
  if need&absent:continue
  if any(len(need&g)>1 for g in [{'D-','D+'},{'R-','R+'},{'Nb-','Nb+','Nr-','Nr+'},{'T-','T+'}]):continue
  if {'D+','R-'}<=need or {'Nr+','T-'}<=need:continue
  key=(need,absent)
  if key in terms and terms[key]['reflections']<=len(r['path'])-2:continue
  path=[convert(frame,rev,tuple(F(*v) for v in p)) for p in r['path']]
  if rev:path.reverse()
  assert path[0]==(0,0) and path[-1]==(2,2)
  terms[key]={'requires':sorted(need),'forbids':sorted(absent),'source_line':line,'frame':frame,'endpoint_reversal':rev,'reflections':len(path)-2,'path':[[[x.numerator,x.denominator] for x in p] for p in path]}
 minimal=[v for (u,z),v in terms.items() if not any((uu,zz)!=(u,z) and uu<=u and zz<=z for uu,zz in terms)]
 minimal.sort(key=lambda t:(len(t['requires'])+len(t['forbids']),t['requires'],t['forbids']))
 for t in minimal:
  path=[tuple(F(*v) for v in p) for p in t['path']];U,Z=checker['path_requirements'](path)
  assert U<=fixed|{variables[n] for n in t['requires']}
  assert not Z&(possible-{variables[n] for n in t['forbids']})
  t['required_triangles']=sorted(U);t['forbidden_triangles']=sorted(Z)
 results[name]={'configuration':[a,st,m,la,ls,present,varnames],'fixed_triangles':sorted(fixed),'variables':variables,'terms':minimal}
out={'status':'FIXED_FROZEN_PROJECTION','archive':str(archive),'sha256':hashlib.sha256(raw).hexdigest(),'records':len(records),'scope':'Nine hand-specified symbolic inputs only. One already used archive. Actual S/T fixed; no cap assignments, new trajectories, words, directions, or solver. Terms require a separate exhaustive hand cover.','families':results}
(HERE/'remote22-frozen.json').write_text(json.dumps(out,indent=2)+'\n')
lines=[]
for name,v in results.items():
 lines.append(name)
 for t in v['terms']:lines.append(str({k:t[k] for k in ['requires','forbids','source_line','frame','endpoint_reversal','reflections']}))
(HERE/'remote22-frozen.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
