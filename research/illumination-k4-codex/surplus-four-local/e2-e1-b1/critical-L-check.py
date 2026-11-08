"""Named inherited guards and symbolic angle tables for critical L at b1."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
helper=ROOT/'surplus-four-local/mixed-allroots-review/check.py';s=helper.read_text()
exec(compile(s[:s.index('# Local D-root deletion identities')],str(helper),'exec'),globals())
funcs=[n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name in ['guard','angle_info']]
exec(compile(ast.Module(body=funcs,type_ignores=[]),str(helper),'exec'),globals())
exec(compile(s[s.index('# Check pinned existing path coordinates'):s.index('# Only the two N fans')],str(helper),'exec'),globals())
from boundary_replay import on
uniform7=[tuple(map(F,p)) for p in read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path']]
paths['Lsquare5']=[uniform7[0],(F(-2),F(1,3))]+uniform7[4:]
paths['double3']=[uniform7[0],(F(-2),F(1,3)),(F(4),F(4,3))]+uniform7[7:]
def retained(family,line,source):
 terms=read(source)['families'][family]['terms'];rr=[v for v in terms if v['source_line']==line];assert len(rr)==1
 r=rr[0];P=[tuple(F(*c) for c in p) for p in r['path']];u,z=path_requirements(P)
 assert u==set(map(tri,r['required_triangles'])) and z==set(map(tri,r['forbidden_triangles']))
 assert P[0]==(0,0) and P[-1]==(2,2)
 for a,b in zip(P[:-2],P[1:-1]):assert not on((2,2),a,b)
 return P
paths['L14']=retained('L_Hupper3_Nrminus',3580,'third-surplus-review/local-e2-project.json')
for line in [2997,2823,2240,2224]:paths[str(line)]=retained('Lupper_Ecenter',line,'third-surplus-review/local-mixed-project.json')
paths['531']=retained('L_outer3_Nbminus',531,'third-surplus-review/local-e2-project.json')
P531=paths['531']
paths['531_Nsquare13']=P531[:2]+[(F(-8,11),F(2))]+P531[5:]
paths['531_Esquare13']=P531[:12]+[(F(4),F(14,11))]+P531[15:]
assert len(paths['531_Nsquare13'])-2==len(paths['531_Esquare13'])-2==13
for key in ['531_Nsquare13','531_Esquare13']:
 for a,b in zip(paths[key][:-2],paths[key][1:-1]):assert not on((2,2),a,b)
# Portal equalities at prescribed entry/exit points, no newly traced itinerary.
compositions={}
for key,indices,entry,velocity,exitpoint,outvelocity,hit,u,d in [
 ('N',(2,3,4),(F(-6,11),F(1)),(-2,11),(F(-10,11),F(1)),(-2,-11),(F(-8,11),F(2)),F(6,11),F(2,11)),
 ('E',(12,13,14),(F(3),F(12,11)),(11,2),(F(3),F(16,11)),(-11,2),(F(4),F(14,11)),F(1,11),F(2,11))]:
 first,last=indices[0],indices[-1]
 assert 0<u<1 and 0<u+2*d<1
 for a,b,v in [(P531[first-1],entry,velocity),(entry,P531[first],velocity),
 (P531[last],exitpoint,outvelocity),(exitpoint,P531[last+1],outvelocity),
 (entry,hit,velocity),(hit,exitpoint,outvelocity)]:
  delta=sub(b,a);assert cross(delta,v)==0 and sum(x*y for x,y in zip(delta,v))>0
 # The substituted far-wall reflection is normal and flips just the normal component.
 assert outvelocity==((velocity[0],-velocity[1]) if key=='N' else (-velocity[0],velocity[1]))
 compositions[key]={'original_contacts':list(indices),'entry':list(map(str,entry)),
 'input_velocity':velocity,'exit':list(map(str,exitpoint)),'output_velocity':outvelocity,
 'one_hit':list(map(str,hit)),'normalized_u':str(u),'normalized_d':str(d),'normalized_exit':str(u+2*d),'status':'STRICT_PORTAL_STATE_IDENTICAL'}
# One analytically forced roof + Dcap composition; no direction/word search.
paths['Ncenter_Dminus6']=[(F(0),F(0)),(F(-1,6),F(-1)),(F(-4,7),F(10,7)),
 (F(4,5),F(6,5)),(F(6,5),F(-6,5)),(F(2),F(-4,3)),(F(10,7),F(-10,7)),(F(2),F(2))]
d=F(1,6);assert F(1,7)<d<F(1,5)
roof_entry=(-3*d,F(1));roof_exit=(5*d,F(1))
assert -4*d/(1+d)==F(-4,7) and 4*d/(1-d)==F(4,5)
assert 0<2-7*d<1 and 0<2-9*d<1 and 12*d==2
# Every declared leg agrees with the independently derived port directions.
for a,b,v in [(paths['Ncenter_Dminus6'][1],roof_entry,(-d,1)),
 (roof_entry,paths['Ncenter_Dminus6'][2],(-d,1)),
 (paths['Ncenter_Dminus6'][3],roof_exit,(d,-1)),
 (roof_exit,(7*d,F(-1)),(d,-1)),
 ((7*d,F(-1)),paths['Ncenter_Dminus6'][4],(d,-1)),
 (paths['Ncenter_Dminus6'][6],(9*d,F(-1)),(d,1)),
 ((9*d,F(-1)),paths['Ncenter_Dminus6'][-1],(d,1))]:
 dv=sub(b,a);assert cross(dv,v)==0 and sum(x*y for x,y in zip(dv,v))>0
for a,b in zip(paths['Ncenter_Dminus6'][:-2],paths['Ncenter_Dminus6'][1:-1]):assert not on((2,2),a,b)
assert len(paths['Ncenter_Dminus6'])-2==6
assert angle_info(H|fan('N',[5,6]),(1,1))==([315],False)
q=(F(2),F(2))
# Reverse actual wall reflections to unfold the actual target T.
for reflect in [lambda p:(-p[1],-p[0]),lambda p:(4-p[0],p[1]),
 lambda p:(-p[1],-p[0]),lambda p:(2-p[1],2-p[0]),
 lambda p:(p[1]-2,p[0]+2),lambda p:(p[0],-2-p[1])]:q=reflect(q)
assert q==(-2,-12) and cross(q,(-1,-6))==0
lo=fan('L',[6,7,0]);up=fan('L',[7,0,1]);rect=fan('L',[6,7,0,1]);lo4=fan('L',[5,6,7,0])
BC=fan('B',[1,2]);BO=fan('B',[0,1]);EC=fan('E',[3,4]);EO=fan('E',[4,5]);TO=fan('Tc',[4,5]);DR=full('D')|full('R')
notNb=full('N')-C(['Nb-']);notNr=full('N')-C(['Nr-']);notNbplus=full('N')-C(['Nb+'])
spec=[
 ('lower3_unit_awayB_L3','L3',H|lo|C(['B+']),H|lo|C(['B+'])|full('E')|full('Tc')|full('N')|DR),
 ('lower3_BC_notNbminus_B6','B6',H|lo|BC|C(['T-']),H|lo|BC|C(['T-'])|full('E')|notNb|DR),
 ('lower3_BO_notNbplus_five','five',H|lo|BO|C(['T-']),H|full('L')|BO|C(['T-'])|full('E')|notNbplus|DR),
 ('lower4_forcedBC_notNbminus_B6','B6',H|lo4|BC|C(['T-']),H|lo4|BC|C(['T-'])|full('E')|notNb|DR),
 ('upper_rectangle_BC_notNbminus_B6','B6',H|BC|C(['T-']),H|full('L')|BC|C(['T-'])|full('E')|notNb|DR),
 ('upper_rectangle_ordinaryE_notNrminus_square5','Lsquare5',H|up|C(['E-']),H|rect|full('B')|C(['E-'])|full('Tc')|notNr|DR),
 ('upper_rectangle_Eouter_notNrminus_double3','double3',H|up|EO,H|rect|full('B')|EO|full('Tc')|notNr|DR),
 ('upper_rectangle_Nrminus_ordinary_or_outer_BE_T_L14','L14',H|up|C(['B+','E-','T-','Nr-']),H|rect|BO|EO|TO|fan('N',[7,0])|DR),
 ('Tcenter_any_L_T3','T3',H|fan('Tc',[5,6])|C(['E-']),H|full('L')|full('B')|C(['E-'])|fan('Tc',[5,6])|full('N')|DR),
 ('upper_EC_Nbminus_DplusRminus_2240','2240',H|up|EC|C(['B+','T-','D+','R-']),H|up|EC|C(['B+','T-','D+','R-','Nb-'])),
 ('upper_rectangle_EC_DplusRplus_bottomN_2997','2997',H|up|EC|C(['B+','T-','D+','R+']),H|rect|EC|C(['B+','T-','D+','R+','Nb-','Nb+'])),
 ('upper_EC_DminusRminus_Nrminus_2224','2224',H|up|EC|C(['B+','T-','D-','R-']),H|up|EC|C(['B+','T-','D-','R-','Nr-'])),
 ('outer3_Nbminus_Bordinary_or_outer_fullDR_531','531',H|fan('L',[0,1,2])|C(['B+','E-','T-','Nb-']),H|fan('L',[0,1,2])|BO|C(['E-','Nb-'])|full('Tc')|DR),
 ('outer3_Nsw_new_normal13','531_Nsquare13',H|fan('L',[0,1,2])|fan('N',[4,5])|C(['B+','E-','T-']),H|fan('L',[0,1,2])|fan('N',[4,5])|C(['B+','E-','T-'])|DR),
 ('outer3_Eouter_new_normal13','531_Esquare13',H|fan('L',[0,1,2])|EO|C(['B+','T-','Nb-']),H|fan('L',[0,1,2])|EO|C(['B+','T-','Nb-'])|DR),
 ('Ncenter_Dminus6_full_L_E_T_R','Ncenter_Dminus6',H|fan('N',[5,6])|C(['D-']),H|fan('N',[5,6])|C(['D-','B+'])|full('L')|full('E')|full('Tc')|full('R')),
]
checks={}
for name,key,mi,ma in spec:checks[name]={'path':key,**guard(paths[key],mi,ma,name)}
# Explicitly retain why the other candidate transfers do not establish closure.
blockers={}
for name,key,added in [('rectangle_EC_Rplus_2823','2823',fan('L',[6])),
 ('rectangle_EC_Rminus_2224','2224',fan('L',[6])),
 ('rectangle_BC_L14','L14',BC),('lower_BC_Nbminus_L12','L12',fan('L',[6])),
 ('outer3_BC_531','531',BC),('outer3_Nsw_531','531',fan('N',[4,5])),
 ('outer3_Ncenter_531','531',fan('N',[5,6])),('fullnorth_531','531',fan('L',[7])),
 ('outer4_531','531',fan('L',[3]))]:
 u,z=path_requirements(paths[key]);bad=z&added;assert bad,name;blockers[name]=sorted(bad)

# Pure angular coefficients. No completed room or cap assignments are generated.
capvars=['D-','D+','R-','R+','Nb-','Nb+','Nr-','Nr+']
base_specs=[('lower_BC',H|lo|BC|C(['E-','T-']),{(-1,1):(135,{'Nb-':45}),(1,3):(135,{'Nr+':45}),(3,-1):(90,{'D+':45,'R-':45})}),
 ('lower_BO',H|lo|BO|C(['E-','T-']),{(-1,-1):(180,{}),(-1,1):(135,{'Nb-':45}),(1,3):(135,{'Nr+':45}),(3,-1):(90,{'D+':45,'R-':45})}),
 ('lower4_BC',H|lo4|BC|C(['E-','T-']),{(-1,1):(135,{'Nb-':45}),(1,3):(135,{'Nr+':45}),(3,-1):(90,{'D+':45,'R-':45})}),
 ('upper_EC',H|up|EC|C(['B+','T-']),{(-1,1):(180,{'Nb-':45}),(1,3):(135,{'Nr+':45}),(3,-1):(90,{'D+':45,'R-':45})}),
 ('rectangle_EC',H|rect|EC|C(['B+','T-']),{(-1,-1):(180,{}),(-1,1):(180,{'Nb-':45}),(1,3):(135,{'Nr+':45}),(3,-1):(90,{'D+':45,'R-':45})})]
coefficients={}
for label,base,expected in base_specs:
 pts={p for t in base|C(capvars) for p in t if p[0]%2==p[1]%2==1};table={}
 for p in sorted(pts):
  fixed=45*sum(p in t for t in base);v={n:45 for n in capvars if p in caps[n]}
  table[str(p)]={'fixed_degrees':fixed,'cap_degrees':v}
  if p in expected:assert (fixed,v)==expected[p],(label,p,fixed,v)
  else:assert fixed>=225 or fixed+sum(v.values())<180,(label,p,fixed,v)
 coefficients[label]=table
assert angle_info(H|lo4|BC,(-2,-1))==([180],False)
# Local L windows and J/n identities are one-cell/count checks only.
Lwindows=[]
for m in [3,4]:
 for st in range(8):
  ss={(st+i)%8 for i in range(m)}
  if 0 not in ss:continue
  Lwindows.append({'m':m,'start':st,'H_centered':{7,0}<=ss,'outside_C_pairs':sum(pair<=ss for pair in [{1,2},{3,4},{5,6}])})
assert len(Lwindows)==7
for h in [0,1]:
 for c in [0,1]:
  J=2+h+c;n=J+1;Q=5+n;sN=12-Q
  assert J+sN==6 and Q+sN-8==4
out={'status':'PARENT_CRITICAL_L_INWARD_FORMS_PARTIAL_COVER_CHECKS_PASS',
 'named_guards':checks,'new_normal_compositions':compositions,'new_roof_Dcap_composition':{'path':[[str(c) for c in p] for p in paths['Ncenter_Dminus6']],'d':'1/6','strict_d_interval':['1/7','1/5'],'roof_entry':list(map(str,roof_entry)),'roof_exit':list(map(str,roof_exit)),'Dcap_entry_x':'7d','Dcap_exit_x':'9d','actual_T_equation':'12d=2','unfolded_actual_target':['-2','-12'],'reflections':6},'failed_transfers_exact_blockers':blockers,'B_angle_coefficients':coefficients,
 'seven_L_root_windows':Lwindows,'proposed_necessary_inward_residue_count_up_to_sigma':13,'closed_subfamily_reflection_bound':max(v['reflections'] for v in checks.values()),
 'residue_split':{'lower3_Bcenter':3,'lower3_Bouter':4,'rectangle_Ecenter':2,'upper_Ecenter':4},
 'limits':'Parent hand reduction only.13 are necessary hand-forced residue descriptions, not geometrically constructed or optically searched rooms. Three remaining outside-C L forms are separate. No wholecriticalL/partition closure. Only named existing paths/retained3580,531 and four LupperEC records, two prescribed normal-return compositions, one analytically forced roof/Dcap six-path and local angle identities; no new room/cap census, raw archive, ray/word/direction discovery, solver or workers.',
 'input_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in [
 'surplus-four-local/mixed-allroots-review/check.py','third-surplus-review/local-e2-project.json',
 'third-surplus-review/local-mixed-project.json','surplus-four-local/single-e2-check.json']}}
(HERE/'critical-L-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status']);print('16namedguards+sigma;2newstrictnormalcompositions+1roofDcap6;5symbolicBtables;7Lwindows PASS.13necessaryinwardresidues+3outsideCformsOPEN.')
