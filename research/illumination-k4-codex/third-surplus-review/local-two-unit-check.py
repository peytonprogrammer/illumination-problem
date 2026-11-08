"""Specified inherited path implications for two unit defects plus b1."""
from pathlib import Path
from fractions import Fraction as F
import json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
core=set().union(*(check['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
extras={'b':tri(((0,-2),(1,-2),(1,-1))),'l':tri(((-2,0),(-2,1),(-1,1))),'e':tri(((4,2),(4,1),(3,1))),'t':tri(((2,4),(1,4),(1,3))),'dw':tri(((2,-2),(1,-2),(1,-1)))}
decode=lambda raw:[tuple(F(*v) for v in p) for p in raw]
read=lambda rel:json.loads((ROOT/rel).read_text())
paths={
 'B6':decode(read('first-surplus-review/bottom-residual-check.json')['path']),
 'L11':decode(read('first-surplus-review/square-exchange-check.json')['paths']['L_thirteen']['path']),
 'E11':decode(read('first-surplus-review/square-exchange-check.json')['paths']['E_thirteen']['path']),
 'sigma13':decode(read('zero-surplus-L/cover-check.json')['paths']['thirteen_sigma']['path']),
 'five':decode(read('second-surplus-review/five-path-check.json')['five_path']),
}
sigma=lambda p:(2-p[1],2-p[0])
paths['sigma_B6']=[sigma(p) for p in paths['B6']][::-1]
req={n:check['path_requirements'](p) for n,p in paths.items()}
cases={
 'centerL_centerB':('B6',['B-','B+','L-','L+','T-'],['Nb-','T+'],[]),
 'centerB_centerE_Nb_absent':('B6',['B-','B+','E-','E+','T-'],['Nb-','T+'],[]),
 'centerB_centerE_Nb_present':('sigma_B6',['B-','B+','E-','E+','L+','Nb-'],['L-','Nb+','Nr-','Nr+'],[]),
 'centerB_outerL_Nb_absent':('B6',['B-','B+','L+','T-'],['Nb-','T+','L-'],['l']),
 'centerB_outerL_Nb_present':('L11',['B-','B+','L+','E-','T-','Nb-'],['E+','T+','L-','Nb+','Nr-','Nr+'],['l']),
 'centerB_outerE_Nb_absent':('B6',['B-','B+','E-','T-'],['Nb-','T+','E+'],['e']),
 'centerB_outerE_Nb_present':('E11',['B-','B+','E-','L+','T-','Nb-'],['E+','L-','T+','Nb+','Nr-','Nr+'],['e']),
 'centerB_outerT_Nb_present':('sigma13',['B-','B+','E-','L+','T-','Nb-'],['E+','L-','T+','Nb+','Nr-','Nr+'],['t']),
 'BD_join_Nbplus_absent':('five',['B+','D-','E-','L+','T-'],['B-','D+','E+','L-','T+','Nb+'],['b','dw']),
 'BD_join_Nbplus_present':('sigma13',['B+','D-','E-','L+','T-','Nb+'],['B-','D+','E+','L-','T+','Nb-','Nr-','Nr+'],['b','dw']),
}
results={}
for name,(which,present,absent,ex) in cases.items():
 fixed=core|{slots[n] for n in present}|{extras[n] for n in ex}
 possible=(core|set(slots.values())|{extras[n] for n in ex})-{slots[n] for n in absent}
 u,z=req[which]
 assert u<=fixed,(name,'requires',u-fixed)
 assert not z&possible,(name,'forbids',z&possible)
 results[name]={'status':'PASS','path':which,'reflections':len(paths[which])-2,'forced_caps':present,'absent_caps':absent,'only_outer_extras':ex}
(HERE/'local-two-unit-check.json').write_text(json.dumps({'status':'PASS','implications':results,'scope':'Ten specified inherited path implications; no room assignments, trajectories, directions, words, archive retrieval or solver.'},indent=2)+'\n')
print(json.dumps({'status':'PASS','implications':len(results),'paths':list(paths)}))
