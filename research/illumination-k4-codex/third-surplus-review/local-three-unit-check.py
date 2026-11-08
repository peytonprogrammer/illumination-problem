"""Analytic square substitutions and named three-unit symbolic branches."""
from pathlib import Path
from fractions import Fraction as F
import json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
core=set().union(*(check['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
extras={'B':tri(((0,-2),(1,-2),(1,-1))),'L':tri(((-2,0),(-2,1),(-1,1))),'E':tri(((4,2),(4,1),(3,1))),'T':tri(((2,4),(1,4),(1,3)))}
read=lambda rel:json.loads((ROOT/rel).read_text())
dec=lambda raw:[tuple(F(*v) for v in p) for p in raw]
square=read('first-surplus-review/square-exchange-check.json')['paths']
paths={'B6':dec(read('first-surplus-review/bottom-residual-check.json')['path']), 'five':dec(read('second-surplus-review/five-path-check.json')['five_path']), 'L12':dec(read('first-surplus-review/centered-left-check.json')['paths']['left']['path']), 'B11':dec(square['B_thirteen']['path']), 'T11':dec(square['T_thirteen']['path']), 'E11':dec(square['E_thirteen']['path']), 'L3':dec(read('first-surplus-review/residual-cover-check.json')['path'])}
paths['B4']=paths['B6'][:4]+[(F(5,3),F(4))]+paths['B6'][7:]
paths['fiveTop3']=paths['five'][:3]+[(F(5,3),F(4))]+paths['five'][6:]
paths['L10']=paths['L12'][:3]+[(F(4),F(16,11))]+paths['L12'][6:]
paths['BT9']=paths['B11'][:9]+[(F(18,11),F(4))]+paths['B11'][12:]
sigma=lambda p:(2-p[1],2-p[0])
for name,path in list(paths.items()):paths['sigma_'+name]=[sigma(p) for p in path][::-1]
req={n:check['path_requirements'](p) for n,p in paths.items()}
# Each shape fixes its three critical unit fans; the missing critical cap stays ordinary.
cap={'B':'B+','E':'E-','L':'L+','T':'T-'};opp={'B':'B-','E':'E+','L':'L-','T':'T+'}
shapes={
 'missL_allO':{'B':'O','E':'O','T':'O'},
 'missB_allO':{'L':'O','E':'O','T':'O'},
 'missB_EC':{'L':'O','E':'C','T':'O'},
 'centerL_Bouter_Touter':{'L':'C','B':'O','T':'O'},
 'missL_BC':{'B':'C','E':'O','T':'O'},
 'missL_BC_EC':{'B':'C','E':'C','T':'O'},
 'missL_EC':{'B':'O','E':'C','T':'O'},
 'centerL_Bouter_Eouter':{'L':'C','B':'O','E':'O'},
 'centerL_centerE_Bouter':{'L':'C','E':'C','B':'O'},
}
cases=[
 ('missL_allO_rightN','missL_allO','BT9',['Nb-','Nb+']),
 ('missL_allO_bottomN','missL_allO','E11',['Nr-','Nr+']),
 ('missB_allO_rightN','missB_allO','T11',['Nb-','Nb+']),
 ('missB_allO_bottomN','missB_allO','sigma_BT9',['Nr-','Nr+']),
 ('missB_EC_notNrplus','missB_EC','sigma_B4',['Nr+']),
 ('missB_EC_Nrplus','missB_EC','T11',['Nb-','Nb+','Nr-']),
 ('CL_BO_TO_notNbplus','centerL_Bouter_Touter','fiveTop3',['Nb+']),
 ('CL_BO_TO_Nbplus','centerL_Bouter_Touter','L12',['Nb-','Nr-','Nr+']),
 ('missL_BC_notNbminus','missL_BC','B4',['Nb-']),
 ('missL_BC_Nbminus','missL_BC','E11',['Nb+','Nr-','Nr+']),
 ('missL_BC_EC_notNbminus','missL_BC_EC','B4',['Nb-']),
 ('missL_BC_EC_Nbminus','missL_BC_EC','sigma_B6',['Nb+','Nr-','Nr+']),
 ('missL_EC_notNrplus','missL_EC','sigma_B6',['Nr+']),
 ('missL_EC_Nrplus','missL_EC','BT9',['Nb-','Nb+','Nr-']),
 ('CL_BO_EO_notNbplus','centerL_Bouter_Eouter','five',['Nb+']),
 ('CL_BO_EO_Nbplus','centerL_Bouter_Eouter','L10',['Nb-','Nr-','Nr+']),
 ('CL_CE_BO_notNbplus','centerL_centerE_Bouter','five',['Nb+']),
]
results={}
for name,shape,which,absentN in cases:
 fixed=core|{slots[v] for v in cap.values()};absent={slots[v] for v in absentN};allowed_ex=set()
 for site in cap:
  if shapes[shape].get(site)=='C':fixed.add(slots[opp[site]])
  else:absent.add(slots[opp[site]])
  if shapes[shape].get(site)=='O':fixed.add(extras[site]);allowed_ex.add(extras[site])
 possible=(core|set(slots.values())|allowed_ex)-absent
 u,z=req[which]
 assert u<=fixed,(name,'required',u-fixed)
 assert not z&possible,(name,'forbidden',z&possible)
 results[name]={'status':'PASS','shape':shape,'path':which,'reflections':len(paths[which])-2,'absent_N':absentN}
# Lcentered with missing B needs no E/T restriction; allow their centered/outer unions.
u,z=req['L3'];possible=core|set(slots.values())|{extras['E'],extras['T']};possible-={slots['B-']}
assert not z&possible and u<=core|{slots['B+'],slots['L+'],slots['L-']}
results['Lcentered_missingB_arbitrary_E_T']={'status':'PASS','path':'L3','reflections':3}
(HERE/'local-three-unit-check.json').write_text(json.dumps({'status':'PASS','cases':results,'new_paths':{n:[[[v.numerator,v.denominator] for v in p] for p in paths[n]] for n in ['B4','fiveTop3','L10','BT9']},'scope':'Four exact analytic square substitutions and eighteen named symbolic branch implications, no room assignment enumeration/discovery or archives.'},indent=2)+'\n')
print(json.dumps({'status':'PASS','named_cases':len(results),'new_substitutions':{n:len(paths[n])-2 for n in ['B4','fiveTop3','L10','BT9']}}))
