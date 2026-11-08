"""One analytic five-path, three fixed fallback paths, symbolic family guards."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()};labels={t:n for n,t in slots.items()}
core=frozenset().union(*(checker['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
extras={'b':tri(((0,-2),(1,-2),(1,-1))), 'l':tri(((-2,0),(-2,1),(-1,1)))}
d=F(1,6)
five=[(F(0),F(0)),(d,F(1)),(4*d,F(-2)),
 (8*d/(1-d),8*d/(1-d)+2),(F(2),2+10*d),
 (12*d/(1+d),12*d/(1+d)+2),(12*d,F(2))]
assert F(1,7)<d<F(2,11) and five[-1]==(2,2)
u5,z5=checker['path_requirements'](five)
assert u5-core==frozenset({slots['B+'],slots['T-'],extras['b']})
assert {labels[t] for t in z5 if t in labels}=={'Nb+','T+'}
assert not z5&core
old=ROOT/'first-surplus-review'
decode=lambda p:[tuple(F(*v) for v in point) for point in p]
path11=decode(json.loads((old/'square-exchange-check.json').read_text())['paths']['L_thirteen']['path'])
path12=decode(json.loads((old/'centered-left-check.json').read_text())['paths']['left']['path'])
path13=decode(json.loads((ROOT/'zero-surplus-L/cover-check.json').read_text())['paths']['thirteen_sigma']['path'])
paths={'five':five,'L_square_eleven':path11,'L_centered_twelve':path12,'ordinary_thirteen':path13}
req={name:checker['path_requirements'](path) for name,path in paths.items()}
# Conditions are the hand-derived necessary conditions for putative darkness.
# These are six symbolic proof branches, not occupancy assignments or rooms.
cases={
 'L_triple':('L_square_eleven',{'L-','L+','B+','E-','T-','Nb-'},{'B-','E+','T+','Nb+','Nr-','Nr+'},{'l'}),
 'centerB_outerL':('L_square_eleven',{'B-','B+','L+','E-','T-','Nb-'},{'L-','E+','T+','Nb+','Nr-','Nr+'},{'l'}),
 'B_triple_Nbplus_absent':('five',{'B-','B+','L+','E-','T-'},{'L-','E+','T+','Nb+'},{'b'}),
 'B_triple_Nbplus_present':('ordinary_thirteen',{'B-','B+','L+','E-','T-','Nb+'},{'L-','E+','T+','Nb-','Nr-','Nr+'},{'b'}),
 'centerL_outerB_Nbplus_absent':('five',{'L-','L+','B+','E-','T-'},{'B-','E+','T+','Nb+'},{'b'}),
 'centerL_outerB_Nbplus_present':('L_centered_twelve',{'L-','L+','B+','E-','T-','Nb+'},{'B-','E+','T+','Nb-','Nr-','Nr+'},{'b'}),
}
checks={}
for name,(which,present,absent,allowed_extra) in cases.items():
 assert not present&absent
 fixed=core|{slots[n] for n in present}|{extras[n] for n in allowed_extra}
 possible=(core|set(slots.values())|{extras[n] for n in allowed_extra})-{slots[n] for n in absent}
 u,z=req[which]
 assert u<=fixed,(name,'required')
 assert not z&possible,(name,'forbidden',sorted(z&possible))
 checks[name]={'status':'PASS','path':which,'forced_present':sorted(present),'forced_absent':sorted(absent),'only_outer_extras':sorted(allowed_extra)}
sigma=lambda p:(2-p[1],2-p[0])
for name,path in paths.items():
 u,z=req[name]
 reflected=[sigma(p) for p in path][::-1]
 ur,zr=checker['path_requirements'](reflected)
 assert reflected[0]==(0,0) and reflected[-1]==(2,2)
 assert ur==frozenset(tri(sigma(v) for v in t) for t in u)
 assert zr==frozenset(tri(sigma(v) for v in t) for t in z)
result={'status':'PASS','five_path':[[[v.numerator,v.denominator] for v in p] for p in five],
 'five_reflections':5,'five_required_caps':['B+','T-'],'five_required_outer':extras['b'],
 'five_forbidden_caps':sorted(labels[t] for t in z5 if t in labels),
 'five_forbidden_outside_alphabet':sorted(t for t in z5 if t not in labels),
 'analytic_parameter':'d=1/6','whole_interval':'1/7<d<2/11','actual_target_equation':'12d=2',
 'case_implications':checks,'path_reflections':{n:len(p)-2 for n,p in paths.items()},
 'all_sigma_transfers':'PASS',
 'scope':'One local analytic composition plus three previously fixed paths, exact symbolic implications for six hand branches; no room/cap-assignment enumeration or search.'}
(HERE/'five-path-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','five_path':result['five_path'],'five_forbidden_caps':result['five_forbidden_caps'],'branches':{n:v['path'] for n,v in checks.items()}},indent=2))
