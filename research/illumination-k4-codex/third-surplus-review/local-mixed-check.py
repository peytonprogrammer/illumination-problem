"""Named inherited guards for mixed e2/e1 fan interactions."""
from pathlib import Path
from fractions import Fraction as F
import json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
core=set().union(*(check['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
extras={'b':tri(((0,-2),(1,-2),(1,-1))),'l':tri(((-2,0),(-2,1),(-1,1))),'e':tri(((4,2),(4,1),(3,1))),'t':tri(((2,4),(1,4),(1,3))),'llow':tri(((-2,0),(-2,-1),(-1,-1)))}
read=lambda rel:json.loads((ROOT/rel).read_text());dec=lambda raw:[tuple(F(*v) for v in p) for p in raw]
sq=read('first-surplus-review/square-exchange-check.json')['paths']
paths={'B6':dec(read('first-surplus-review/bottom-residual-check.json')['path']),'L11':dec(sq['L_thirteen']['path']),'E11':dec(sq['E_thirteen']['path']),'L3':dec(read('first-surplus-review/residual-cover-check.json')['path']),'sigma13':dec(read('zero-surplus-L/cover-check.json')['paths']['thirteen_sigma']['path']),'five':dec(read('second-surplus-review/five-path-check.json')['five_path'])}
new=read('third-surplus-review/local-three-unit-check.json')['new_paths']
paths['BT9']=dec(new['BT9']);paths['F3']=dec(new['fiveTop3'])
sigma=lambda p:(2-p[1],2-p[0])
for name in ['B6','BT9','L3']:paths['sigma_'+name]=[sigma(p) for p in paths[name]][::-1]
req={n:check['path_requirements'](p) for n,p in paths.items()}
cases={
 'Llower_centerB':('B6',['L-','L+','B-','B+','T-'],['Nb-','T+'],['llow']),
 'Lrectangle_centerB':('L11',['L-','L+','B-','B+','E-','T-','Nb-'],['E+','T+','Nb+','Nr-','Nr+'],['l','llow']),
 'Lupper_outerB':('L11',['L-','L+','B+','E-','T-','Nb-'],['B-','E+','T+','Nb+','Nr-','Nr+'],['l','b']),
 'Lupper_outerE':('sigma_BT9',['L-','L+','B+','E-','T-','Nb-'],['B-','E+','T+','Nb+','Nr-','Nr+'],['l','e']),
 'Lupper_centerT':('sigma_L3',['L-','L+','T-','T+','E-'],['E+'],['l']),
 'Lupper_outerT':('L11',['L-','L+','E-','T-','Nb-'],['E+','T+','Nb+','Nr-','Nr+'],['l','t']),
 'BactiveTriple_centerE_Nbplus':('sigma_B6',['B-','B+','E-','E+','L+','T-','Nb+'],['L-','T+','Nb-','Nr-','Nr+'],['b']),
 'BactiveTriple_outerE_Nbplus':('E11',['B-','B+','E-','L+','T-','Nb+'],['E+','L-','T+','Nb-','Nr-','Nr+'],['b','e']),
 'BactiveTriple_centerT':('sigma_L3',['B-','B+','T-','T+','E-'],['E+'],['b']),
 'BactiveTriple_outerT_notNbplus':('F3',['B-','B+','T-','E-','L+'],['T+','Nb+'],['b','t']),
 'BactiveTriple_outerT_Nbplus':('sigma13',['B-','B+','T-','E-','L+','Nb+'],['T+','E+','L-','Nb-','Nr-','Nr+'],['b','t']),
}
results={}
for name,(which,present,absent,ex) in cases.items():
 fixed=core|{slots[n] for n in present}|{extras[n] for n in ex}
 possible=(core|set(slots.values())|{extras[n] for n in ex})-{slots[n] for n in absent}
 u,z=req[which];assert u<=fixed,(name,'required',u-fixed);assert not z&possible,(name,'forbidden',z&possible)
 results[name]={'status':'PASS','path':which,'forced_caps':present,'absent_caps':absent,'only_outer_extras':ex}
# Every possible D-root triangle is harmless to the two inherited B-square paths.
Dwhole=check['incident']((F(2),F(-2)))
for name,which,present,absent in [('Droot_Bunit_notNbplus','five',['B+','T-','L+','E-'],['Nb+','T+']),('Droot_Bunit_Nbplus','sigma13',['B+','T-','L+','E-','Nb+'],['Nb-','Nr-','Nr+','T+','L-','E+'])]:
 fixed=core|{slots[n] for n in present}|{extras['b']}
 possible=(core|set(slots.values())|{extras['b']}|Dwhole)-{slots[n] for n in absent}
 u,z=req[which];assert u<=fixed;assert not z&possible
 results[name]={'status':'PASS','path':which,'whole_D_support_harmless':True}
(HERE/'local-mixed-check.json').write_text(json.dumps({'status':'PASS','cases':results,'scope':'Thirteen specified inherited guard implications, no new trajectories, rooms, words or archive query.'},indent=2)+'\n')
print(json.dumps({'status':'PASS','cases':len(results)}))
