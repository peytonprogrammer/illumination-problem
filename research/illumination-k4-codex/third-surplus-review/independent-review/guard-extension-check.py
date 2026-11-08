"""Review-requested fixed forcing paths and full noncritical fan supports; no discovery."""
from pathlib import Path
from fractions import Fraction as F
import json,runpy
HERE=Path(__file__).resolve().parent;P=HERE.parent;ROOT=P.parent
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
core=set().union(*(check['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'T':(2,4),'N':(0,2)}
whole={n:check['incident'](tuple(map(F,c))) for n,c in centers.items()}
Nnoncaps=whole['N']-core-set(slots.values())
# Unit N fans need only the SW/NE mates. The other two noncap sectors
# are NW sectors2/3; bridge sectors6/7 are already Nb+/Nr- caps.
nw=tri(((0,2),(-1,2),(-1,1)));ne=tri(((0,2),(0,3),(1,3)))
assert Nnoncaps-{nw,ne}=={tri(((0,2),(-1,2),(-1,3))),tri(((0,2),(-1,3),(0,3)))}
bridge={tri(((0,2),(0,1),(1,1))),tri(((0,2),(1,1),(1,2)))}
assert bridge=={slots['Nb+'],slots['Nr-']}
Nmates={nw,ne}
extensions={}
for script in ['local-two-unit-check.py','local-three-unit-check.py','local-mixed-check.py']:
 d=runpy.run_path(str(P/script)); records={}
 for name,(u,z) in d['req'].items():
  assert not z&(whole['D']|whole['R']|Nmates),(script,name,'new noncritical mirror',z&(whole['D']|whole['R']|Nmates))
  records[name]={'status':'PASS','full_required':sorted(u),'full_forbidden':sorted(z),'D_R_full_stars_and_N_outer_mates_avoid_forbidden':True}
 extensions[script]=records
# Full N support check for every noncritical e2 N root: the only N forbidden
# triangles of each old13 path are its stated blocking caps, no sector2/3 issue.
zero=json.loads((ROOT/'zero-surplus-L/cover-check.json').read_text())['paths']
N13={}
for name,blocked in [('thirteen',{'Nb-','Nb+'}),('thirteen_sigma',{'Nr-','Nr+'})]:
 path=[tuple(F(*v) for v in p) for p in zero[name]['path']]
 need,forbid=check['path_requirements'](path)
 assert forbid&whole['N']=={slots[n] for n in blocked},(name,'N blocking set',forbid&whole['N'])
 assert not forbid&(whole['D']|whole['R'])
 N13[name]={'status':'PASS','N_forbidden_exactly':sorted(blocked),'required':sorted(need),'forbidden':sorted(forbid)}
# Two paths specified analytically by independent reviewer B, not discovered by a search.
paths={'centeredB3':[(F(0),F(0)),(F(-2,5),F(-8,5)),(F(2,3),F(-4,3)),(F(7,4),F(3)),(F(2),F(2))],
       'outerB2':[(F(0),F(0)),(F(1,2),F(-2)),(F(7,4),F(3)),(F(2),F(2))]}
sigma=lambda p:(2-p[1],2-p[0])
for name,path in list(paths.items()):paths['sigma_'+name]=[sigma(p) for p in path][::-1]
b=tri(((0,-2),(1,-2),(1,-1)));uB=tri(((0,-2),(-1,-2),(-1,-1)))
base_guards={}
for name,path in paths.items():
 need,forbid=check['path_requirements'](path)
 if name=='centeredB3':
  fixed=core|{slots['B-'],slots['B+']};absent={uB,b,slots['T-']}
 elif name=='outerB2':
  fixed=core|{slots['B+'],b};absent={tri(((0,-2),(1,-2),(1,-3))),slots['T-']}
 else:
  source=base_guards[name.removeprefix('sigma_')]
  fixed={tri(sigma(v) for v in t) for t in source['fixed']}
  absent={tri(sigma(v) for v in t) for t in source['absent']}
 possible=core|set().union(*whole.values())
 assert need<=fixed,(name,'needed',need-fixed)
 assert not forbid&(possible-absent),(name,'forbidden',forbid&(possible-absent))
 base_guards[name]={'fixed':sorted(fixed),'absent':sorted(absent)}
 base_guards[name].update({'status':'PASS','path':[[[v.numerator,v.denominator] for v in p] for p in path],'required':sorted(need),'forbidden':sorted(forbid),'reflections':len(path)-2})
# Explicit N unit forms for the pair-cover extension. Outside mates already checked harmless.
nw=tri(((0,2),(-1,2),(-1,1)));ne=tri(((0,2),(0,3),(1,3)))
assert {nw,ne}==Nmates
nforms={'bottom_center':{'Nb-','Nb+'},'bottom_SW':{'Nb-'},'right_center':{'Nr-','Nr+'},'right_NE':{'Nr+'}}
assert all(not (s&{'Nb-','Nb+'} and s&{'Nr-','Nr+'}) for s in nforms.values())
out={'status':'PASS','full_noncritical_support':extensions,'forcing_paths':base_guards,'old13_full_N_support':N13,'N_bridge_is_Nbplus_Nrminus':True,'N_nonbridge_unit_cap_sets':{n:sorted(s) for n,s in nforms.items()},'N_outer_mates':sorted(Nmates),'scope':'Only reviewer-specified rational paths, pre-existing named fallback paths and full noncritical supports. No room/ray/direction/word discovery.'}
(HERE/'guard-extension-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','forcing_paths':len(base_guards),'fallback_guard_sets':sum(map(len,extensions.values()))}))
