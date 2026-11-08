"""Two named inherited guards and one prescribed square-return obstruction; no search."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
helper=HERE/'root-leaf-check.py'
ns={'__file__':str(helper),'__name__':'retained_helpers'}
exec(compile(helper.read_text().split('BDR=')[0],str(helper),'exec'),ns)
H,fan,full,C,tri,g,decode,sigma,tr=[ns[n] for n in ['H','fan','full','C','tri','g','decode','sigma','tr']]
source=ROOT/'third-surplus-review/local-mixed-project.json'
family=json.loads(source.read_text())['families']['Bwest_Lcenter']
rows=[t for t in family['terms'] if t['source_line']==664]
assert len(rows)==1
row=rows[0];P=decode(row['path'])
assert P[0]==(0,0) and P[-1]==(2,2) and len(P)-2==12
U,Z=g['path_requirements'](P)
assert U=={tri(t) for t in row['required_triangles']}
assert Z=={tri(t) for t in row['forbidden_triangles']}
checks={}
for name,ss in [('Bwest',[1,2,3]),('Brectangle',[0,1,2,3])]:
 minimum=H|fan('B',ss)|fan('L',[7,0])|C(['E-'])
 maximum=minimum|full('D')|full('R')|full('Tc')|full('N')
 assert U<=minimum and not Z&maximum
 us,zs=g['path_requirements']([sigma(p) for p in P[::-1]])
 assert us==tr(U) and zs==tr(Z)
 checks[name]={'status':'PASS','reflections':12,'minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z),'sigma':'PASS'}
# Only these two local corner templates, not assembled budget rooms.
dirs=ns['dirs'];index={v:i for i,v in enumerate(dirs)}
def angle(ts,v):
 total=0
 for t in ts:
  if v not in t:continue
  a,b=[p for p in t if p!=v]
  def ray(p):
   x,y=p[0]-v[0],p[1]-v[1];d=gcd(abs(x),abs(y));return index[(x//d,y//d)]
  delta=(ray(a)-ray(b))%8;total+=45*min(delta,8-delta)
 return total
angles={}
for name,ss in [('west',[1,2,3]),('rectangle',[0,1,2,3])]:
 base=H|fan('B',ss)
 values={label:angle(base|fan('L',ls),(-1,-1)) for label,ls in [('empty',[]),('reference',[0]),('outer',[0,1]),('center',[7,0])]}
 assert values=={'empty':180,'reference':180,'outer':180,'center':225}
 assert not any((-1,-1) in t for site in ['D','R','E','Tc','N'] for t in full(site))
 angles[name]=values
# Identical inlet data from the fixed old excursion. All arithmetic is exact.
entry=(F(3),F(16,11));original_exit=(F(3),F(19,12))
v=(F(11),F(12))
assert P[3:6]==[(F(7,2),F(2)),(F(86,23),F(40,23)),(F(38,11),F(2))]
sub=lambda a,b:tuple(x-y for x,y in zip(a,b))
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
assert cross(sub(P[3],entry),v)==0
assert cross(sub(P[6],original_exit),(-12,-11))==0
# Triangle reflection normals: horizontal, slope+1 diagonal, horizontal.
v1=(v[0],-v[1]);v2=(v1[1],v1[0]);oldout=(v2[0],-v2[1])
assert oldout==(-12,-11)
# In the completed square [3,4]x[1,2], same inlet hits top, right, bottom,
# then returns left before any further wall. This is one prescribed itinerary.
q0=entry;q1=(F(7,2),F(2));q2=(F(4),F(16,11));q3=(F(43,12),F(1));q4=(F(3),F(18,11))
velocities=[(11,12),(11,-12),(-11,-12),(-11,12)]
for a,b,w in zip([q0,q1,q2,q3],[q1,q2,q3,q4],velocities):
 d=sub(b,a);assert cross(d,w)==0 and d[0]*w[0]+d[1]*w[1]>0
 for x,y in [a,b]:assert 3<=x<=4 and 1<=y<=2
assert 3<q1[0]<4 and 1<q2[1]<2 and 3<q3[0]<4 and 1<q4[1]<2
assert q4!=original_exit and velocities[-1]!=oldout
# Normalized square-exchange branch requires |tangent/normal|<1/2;
# here tangent/normal=12/11. Thus that lemma is inapplicable.
assert F(12,11)>F(1,2)
blockers={name:sorted(Z&fan('E',ss)) for name,ss in [('center',[3,4]),('outer',[4,5])]}
assert all(blockers.values())
# Named centered-E rescue: evaluate full proposed envelope; a failed guard
# is a proof-strategy result, not a reason to try additional path records.
P6=ns['paths']['Ecenter6'];u6,z6=g['path_requirements'](P6)
mi6=H|fan('L',[7,0])|fan('E',[3,4])
ma6=mi6|full('B')|full('D')|full('R')|full('Tc')|(full('N')-C(['Nr+']))
center_rescue={'required_missing':sorted(u6-mi6),'forbidden_present':sorted(z6&ma6)}
center_rescue['status']='PASS' if not center_rescue['required_missing'] and not center_rescue['forbidden_present'] else 'PROPOSED_GUARD_FAILS'
center_rescue['Lcenter_forbidden']=sorted(z6&fan('L',[7,0]))
# Local fan exhaustion and joined/root-leaf counting correspondence.
windows=[(3,7),(3,0),(3,1),(4,6),(4,7),(4,0),(4,1)]
window_rows=[]
for m,start in windows:
 ss=[(start+i)%8 for i in range(m)];ts=fan('B',ss)
 assert 1 in ss
 category='joined' if {7,0}<=set(ss) else ('excluded_west_outside_C' if {3,4}<=set(ss) else 'no_join')
 if category=='excluded_west_outside_C':
  assert angle(H|ts,(-1,-2))==180
  assert not any((-1,-2) in t for site in ['L','D','R','E','Tc','N'] for t in full(site))
 window_rows.append({'sectors':ss,'category':category})
assert [sum(x['category']==k for x in window_rows) for k in ['no_join','joined','excluded_west_outside_C']]==[3,3,1]
joined=[]
for label,ss,h in [('O3',[7,0,1],0),('O4',[6,7,0,1],0),('H4',[7,0,1,2],1)]:
 base=H|fan('B',ss)
 original=base|fan('D',[3]);extended=base|fan('D',[2,3])
 assert angle(original,(1,-2))==angle(extended,(1,-2))==270
 assert angle(original,(1,-1))==315 and angle(extended,(1,-1))==360
 assert angle(extended,(0,-1))==270+90*h
 assert not any(v in t for site in ['L','R','E','Tc','N'] for t in full(site) for v in [(1,-2),(1,-1),(0,-1)])
 joined.append({'B':label,'D':[2,3],'shared_C':270,'old_B':315,'new_B':360,'H_facing_C':270+90*h,'h':h,'J_formula':'3+h+c','n_formula':'2+h+c'})
# Every already accepted root-leaf optical implication ignores D in both
# its necessary support and forbidden support. No new path is selected.
prior=json.loads((HERE/'root-leaf-check.json').read_text())['named_implications']
transfer={}
for name,term in prior.items():
 path=[tuple(F(x) for x in q) for q in term['path']]
 u,z=g['path_requirements'](path)
 assert not ((u|z)&full('D')),(name,'D-sensitive')
 transfer[name]='D_FULL_U_Z_AVOIDANCE_PASS'
assert len(transfer)==10
# Two fixed Beast envelopes: both remaining units noncritical.
five=decode(json.loads((ROOT/'second-surplus-review/five-path-check.json').read_text())['five_path'])
sig13=decode(json.loads((ROOT/'zero-surplus-L/cover-check.json').read_text())['paths']['thirteen_sigma']['path'])
beast=H|fan('B',[0,1,2])|C(['L+','E-','T-'])
beast_guards={}
for label,path,mi,ma in [
 ('not_Nbplus',five,beast,beast|full('D')|full('R')|(full('N')-C(['Nb+']))),
 ('Nbplus',sig13,beast|C(['Nb+']),beast|full('D')|full('R')|fan('N',[4,5,6]))]:
 u,z=g['path_requirements'](path)
 assert u<=mi and not z&ma,(label,u-mi,z&ma)
 us,zs=g['path_requirements']([sigma(p) for p in path[::-1]])
 assert us==tr(u) and zs==tr(z)
 beast_guards[label]={'status':'PASS','reflections':len(path)-2,'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z),'sigma':'PASS'}
# Twelve explicitly declared Beast/critical-unit whole-support implications.
sq=json.loads((ROOT/'first-surplus-review/square-exchange-check.json').read_text())['paths']
L11=decode(sq['L_thirteen']['path']);E11=decode(sq['E_thirteen']['path'])
B6=decode(json.loads((ROOT/'first-surplus-review/bottom-residual-check.json').read_text())['path'])
B4=B6[:4]+[(F(5,3),F(4))]+B6[7:]
sig=lambda path:[sigma(p) for p in path[::-1]]
E6=sig(B6);sigmaB4=sig(B4)
T3=sig(ns['left3'])
F3=decode(json.loads((ROOT/'third-surplus-review/local-three-unit-check.json').read_text())['new_paths']['fiveTop3'])
double3=[(F(0),F(0)),(F(-2),F(1,3)),(F(4),F(4,3)),(F(1),F(11,6)),(F(2),F(2))]
BCore=H|fan('B',[0,1,2]);LO=fan('L',[0,1]);EC=fan('E',[3,4]);EO=fan('E',[4,5]);TC=fan('Tc',[5,6]);TO=fan('Tc',[4,5]);DR=full('D')|full('R');NB=fan('N',[4,5,6])
critical_specs=[
 ('Louter_Eordinary',L11,BCore|LO|C(['E-','T-']),BCore|LO|C(['E-'])|TO|DR|NB),
 ('Louter_Eouter',double3,BCore|LO|EO|C(['T-']),BCore|LO|EO|DR|NB|full('Tc')),
 ('Louter_Ecenter',sigmaB4,BCore|LO|EC|C(['T-']),BCore|LO|EC|C(['T-'])|DR|NB),
 ('Tcenter_Eordinary',T3,BCore|TC|C(['E-']),H|TC|C(['E-'])|full('B')|full('L')|DR|full('N')),
 ('Ecenter_noncritical_notNbplus',five,BCore|EC|C(['L+','T-']),BCore|EC|C(['L+','T-'])|DR|(full('N')-C(['Nb+']))),
 ('Ecenter_noncritical_Nbplus',E6,BCore|EC|C(['L+','T-','Nb+']),BCore|EC|C(['L+','T-'])|DR|NB),
 ('Eouter_noncritical_notNbplus',five,BCore|EO|C(['L+','T-']),BCore|EO|C(['L+','T-'])|DR|(full('N')-C(['Nb+']))),
 ('Eouter_noncritical_Nbplus',E11,BCore|EO|C(['L+','T-','Nb+']),BCore|EO|C(['L+','T-'])|DR|NB),
 ('Touter_Eordinary',F3,BCore|TO|C(['L+','E-']),BCore|TO|C(['L+','E-'])|DR|(full('N')-C(['Nb+']))),
 ('Ecenter_Touter',F3,BCore|EC|TO|C(['L+']),BCore|EC|TO|C(['L+'])|DR|(full('N')-C(['Nb+']))),
 ('Eouter_Touter',F3,BCore|EO|TO|C(['L+']),BCore|EO|TO|C(['L+'])|DR|(full('N')-C(['Nb+']))),
 ('Eouter_Tcenter_notNrminus',sig(five),BCore|EO|TC|C(['L+']),BCore|EO|TC|C(['L+'])|DR|(full('N')-C(['Nr-'])))
]
critical_guards={};critical_failures={}
for label,path,mi,ma in critical_specs:
 u,z=g['path_requirements'](path)
 missing=u-mi;blocked=z&ma
 row={'status':'PASS' if not missing and not blocked else 'PROPOSED_GUARD_FAILS','reflections':len(path)-2,'required_missing':sorted(missing),'forbidden_present':sorted(blocked),'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z),'path':[[str(x) for x in q] for q in path]}
 us,zs=g['path_requirements'](sig(path));assert us==tr(u) and zs==tr(z);row['sigma']='PASS'
 critical_guards[label]=row
 if missing or blocked:critical_failures[label]={'missing':sorted(missing),'blocked':sorted(blocked)}
# Explicitly named failed rescue at the remaining Eouter/Tcenter/Nr- branch.
T12=decode(json.loads((ROOT/'first-surplus-review/centered-left-check.json').read_text())['paths']['top']['path'])
ut,zt=g['path_requirements'](T12)
rescue_min=BCore|EO|TC|C(['L+','Nr-']);rescue_max=rescue_min|DR
T12_rescue={'required_missing':sorted(ut-rescue_min),'forbidden_present':sorted(zt&rescue_max)}
assert T12_rescue['forbidden_present']
# Declared smooth-point exclusions and forcing identities only.
angle_clauses={
 'Lcenter_impossible':angle(BCore|fan('L',[7,0]),(-1,-1)),
 'Ecenter_Tcenter_impossible':angle(BCore|EC|TC,(3,3)),
 'Louter_unhealed':angle(BCore|LO,(-1,1)),
 'Louter_with_Nbminus':angle(BCore|LO|C(['Nb-']),(-1,1)),
 'Touter_unhealed':angle(BCore|TO,(1,3)),
 'Touter_with_Nrplus':angle(BCore|TO|C(['Nr+']),(1,3)),
 'Tcenter_with_Nrplus':angle(BCore|TC|C(['Nr+']),(1,3)),
}
assert angle_clauses=={'Lcenter_impossible':180,'Ecenter_Tcenter_impossible':180,'Louter_unhealed':180,'Louter_with_Nbminus':225,'Touter_unhealed':180,'Touter_with_Nrplus':225,'Tcenter_with_Nrplus':180}
# Four previously declared, hand-forced residue controls. Geometry only.
geom=ns['runpy'].run_path(str(ROOT/'triangle-composition/inputs/illumination_geometry.py'))
residuals={}
for cap in ['D-','D+','R-','R+']:
 ts=rescue_min|C([cap]);rr=geom['check']({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
 ld=ns['ledger'](ts)
 assert rr['walls']==20 and set(map(tuple,rr['interior_A']))=={(0,0),(2,0),(2,2)}
 assert ld['W']==20 and ld['k']==6 and ld['Delta']==4,(cap,ld)
 residuals[cap]={'status':'VALID_HAND_FORCED_GEOMETRY_OPTICS_OPEN','triangles':sorted(ts),'vertices':ns['polygon'](ts),'ledger':ld}
# NEW proved normal-return composition on the fixed L12, NOT line664.
L12=decode(json.loads((ROOT/'first-surplus-review/centered-left-check.json').read_text())['paths']['left']['path'])
assert L12[3:6]==[(F(10,3),F(4,3)),(F(38,11),F(2)),(F(46,13),F(20,13))]
entry10=(F(3),F(14,11));exit10=(F(3),F(18,11));far10=(F(4),F(16,11))
assert cross(sub(L12[3],entry10),(11,2))==0
assert cross(sub(L12[6],exit10),(-11,2))==0
assert cross(sub(far10,entry10),(11,2))==0 and cross(sub(exit10,far10),(-11,2))==0
u10,d10=F(3,11),F(2,11)
assert 0<u10<1 and 0<u10+2*d10<1 and 0<u10+d10<1
L12E10=L12[:3]+[far10]+L12[6:]
assert len(L12E10)-2==10
E10base=H|fan('L',[7,0])|EO
outer_force=decode(ns['forcing']['outerB2']['path'])
new10_specs=[
 ('Lcenter_Eouter_normal_exchange10',L12E10,E10base,E10base|full('B')|DR|NB|C(['T-'])),
 ('Brectangle_Eouter_notNbplus_five',five,H|fan('B',[0,1,2,3])|fan('L',[7,0])|EO|C(['T-']),H|fan('B',[0,1,2,3])|fan('L',[7,0])|EO|C(['T-'])|DR|(full('N')-C(['Nb+']))),
 ('Brectangle_forces_Tminus',outer_force,H|fan('B',[0,1,2,3]),H|fan('B',[0,1,2,3])|full('L')|full('E')|DR|full('N')|(full('Tc')-C(['T-'])))
]
normal_composition={}
for label,path,mi,ma in new10_specs:
 u,z=g['path_requirements'](path);assert u<=mi and not z&ma,(label,u-mi,z&ma)
 us,zs=g['path_requirements'](sig(path));assert us==tr(u) and zs==tr(z)
 normal_composition[label]={'status':'PASS','reflections':len(path)-2,'path':[[str(x) for x in q] for q in path],'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z),'sigma':'PASS'}
normal_portals={'u':'3/11','d':'2/11','exit_u':'7/11','entry':list(map(str,entry10)),'exit':list(map(str,exit10)),'far_wall_hit':list(map(str,far10)),'input_velocity':['11','2'],'output_velocity':['-11','2'],'status':'SAME_EXIT_POSITION_AND_VELOCITY_STRICT_BRANCH'}
out={'status':'PASS_NAMED_GUARDS_AND_EXCHANGE_OBSTRUCTION','two_whole_family_guards':checks,'local_L_forcing':angles,'path':[[str(x) for x in p] for p in P],'E_obstructions':blockers,'center_E_rescue':center_rescue,'B_local_windows':window_rows,'joined_templates':joined,'ten_root_leaf_transfers':transfer,'Beast_noncritical_guards':beast_guards,'Beast_critical_guards':critical_guards,'Beast_critical_guard_failures':critical_failures,'Beast_angle_clauses':angle_clauses,'Beast_Eouter_Tcenter_Nrminus_T12_rescue':T12_rescue,'Beast_four_declared_residuals':residuals,'NEW_L12_Esquare_normal_composition':normal_composition,'NEW_normal_exchange_portals':normal_portals,'square_attempt':{'status':'EXIT_STATE_MISMATCH','entry':list(map(str,entry)),'input_velocity':['11','12'],'original_exit':list(map(str,original_exit)),'original_velocity':['-12','-11'],'square_contacts':[[str(x) for x in q] for q in [q1,q2,q3]],'square_exit':list(map(str,q4)),'square_velocity':['-11','12'],'normal_branch_ratio':'12/11'},'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,helper]},'limits':'Only retained line664/Bwest_Lcenter; existing named inherited paths; local B windows/angle templates; specified whole-support guards and one prescribed local square-return obstruction. Four hand-forced Beast residues receive geometry/ledger only, optics OPEN. Complete branch reductions are hand proofs, not inferred from control counts. No room/cap/ray/word/direction discovery, raw archive or worker.'}
(HERE/'critical-B-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS:12 Beastcritical guards;4 residual geometries; NEW L12/E-square10 normalreturn +rectangle/five andTforcing wholeguards. No discovery.')
