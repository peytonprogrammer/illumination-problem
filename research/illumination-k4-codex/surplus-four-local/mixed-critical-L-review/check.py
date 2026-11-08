"""Independent fixed guards, original fixtures and local identities: critical L."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import ast,hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
helper=ROOT/'surplus-four-local/mixed-root-leaf-review/check.py'
source=helper.read_text()
# Only own pure setup/functions; no prior check body or receipt writes.
exec(compile(source[:source.index('base7=')],str(helper),'exec'),globals())
functions=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in ['polygon','ledger']]
exec(compile(ast.Module(body=functions,type_ignores=[]),str(helper),'exec'),globals())
from boundary_replay import on
sigpath=lambda P:[sigma(p) for p in P[::-1]]
peerpath=ROOT/'fourth-surplus-review/mixed-e2-e1/critical-L-check.json'
peer=json.loads(peerpath.read_text())
low=fan('L',[6,7,0]);upper=fan('L',[7,0,1]);rect=fan('L',[6,7,0,1])
BC=fan('B',[1,2]);EC=fan('E',[3,4]);EO=fan('E',[4,5]);TO=fan('Tc',[4,5])
BO=fan('B',[0,1]);NSW=fan('N',[4,5]);NC=fan('N',[5,6]);NB=fan('N',[4,5,6]);DR=full('D')|full('R')
B6=decode(read('first-surplus-review/bottom-residual-check.json')['path'])
B4=B6[:4]+[(F(5,3),F(4))]+B6[7:]
L11=decode(read('first-surplus-review/square-exchange-check.json')['paths']['L_thirteen']['path'])
base7=[tuple(map(F,p)) for p in read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path']]
double3=[base7[0],(F(-2),F(1,3)),(F(4),F(4,3))]+base7[7:]
assert len(double3)-2==3
u=d=F(1,6);assert 0<u<1 and 0<u+2*d<1 and 0<u+d<1
paths={'B6':B6,'B4':B4,'L11':L11,'double3':double3}
terms=read('third-surplus-review/local-mixed-project.json')['families']['Lupper_Ecenter']['terms']
retained={}
for line in [2997,2823,2240,2224]:
 matches=[v for v in terms if v['source_line']==line];assert len(matches)==1
 term=matches[0];P=decode(term['path']);U,Z=path_requirements(P)
 assert P[0]==(0,0) and P[-1]==(2,2)
 assert U==set(map(tri,term['required_triangles']))
 assert Z==set(map(tri,term['forbidden_triangles']))
 assert len(P)-2==term['reflections']
 for a,b in zip(P[:-2],P[1:-1]):assert not on((2,2),a,b)
 paths[str(line)]=P
 retained[str(line)]={'source_line':line,'frame':term['frame'],'endpoint_reversal':term['endpoint_reversal'],'reflections':len(P)-2,'full_stored_U_Z':'MATCH','earlier_actual_T':'ABSENT'}

spec=[
 ('Llower_Bcenter_B6','B6',H|low|BC|C(['T-']),H|low|BC|DR|full('E')|(full('N')-C(['Nb-']))|C(['T-'])),
 ('Llower_Bcenter_Touter_B4','B4',H|low|BC|TO,H|low|BC|TO|DR|full('E')|(full('N')-C(['Nb-']))),
 ('Lrectangle_ordinaryE_L11','L11',H|rect|C(['E-']),H|rect|full('B')|DR|NB|TO|C(['E-'])),
 ('Lupper_ordinaryE_L11','L11',H|upper|C(['E-']),H|upper|full('B')|DR|NB|TO|C(['E-'])),
 ('Lrectangle_Eouter_double3','double3',H|rect|EO,H|rect|EO|full('B')|DR|full('Tc')|NB),
 ('Lupper_Eouter_double3','double3',H|upper|EO,H|upper|EO|full('B')|DR|full('Tc')|NB),
]
upperbase=H|upper|EC|C(['B+','T-','Nb-'])
upperB=H|upper|EC|BO|C(['T-','Nb-'])
upperN=H|upper|EC|NSW|C(['B+','T-'])
spec.extend([
 ('rectangle_BC_EC_Dplus_Rplus_2997','2997',H|rect|BC|EC|C(['Nb-','T-','D+','R+']),H|rect|BC|EC|C(['Nb-','T-','D+','R+'])),
 ('upper_EC_Bouter_Dplus_2997','2997',upperB|C(['D+']),upperB|C(['D+','R+'])),
 ('upper_EC_Bouter_noDplus_noRminus_2823','2823',upperB,upperB|C(['D-','R+'])),
 ('upper_EC_Dupperquarter_2240','2240',upperbase|fan('D',[0,1]),upperbase|fan('D',[0,1])),
 ('upper_EC_Dwestquarter_2823','2823',upperbase|fan('D',[2,3]),upperbase|fan('D',[2,3])),
 ('upper_EC_Rupperquarter_2823','2823',upperbase|fan('R',[2,3]),upperbase|fan('R',[2,3])),
 ('upper_EC_Nsw_noDplus_noRminus_2823','2823',upperN,upperN|C(['D-','R+'])),
 ('upper_EC_Nsw_Dplus_2997','2997',upperN|C(['D+']),upperN|C(['D+'])),
 ('upper_EC_Nsw_Rminus_2240','2240',upperN|C(['R-']),upperN|C(['R-'])),
 ('upper_EC_Ncenter_Dplus_Rplus_2997','2997',H|upper|EC|NC|C(['B+','T-','D+','R+']),H|upper|EC|NC|C(['B+','T-','D+','R+'])),
])
checks={}
for name,key,minimum,maximum in spec:
 P=paths[key];U,Z=path_requirements(P)
 assert U<=minimum and not Z&maximum,name
 assert minimum==set(map(tri,peer['named_implications'][name]['fixed']))
 assert maximum==set(map(tri,peer['named_implications'][name]['possible']))
 assert P==[tuple(map(F,p)) for p in peer['named_implications'][name]['path']]
 Us,Zs=path_requirements(sigpath(P));assert Us==tr(U) and Zs==tr(Z)
 assert U==set(map(tri,peer['named_implications'][name]['required']))
 assert Z==set(map(tri,peer['named_implications'][name]['forbidden']))
 checks[name]={'status':'PASS_OWN_FULL_U_Z','reflections':len(P)-2,'required':sorted(U),'forbidden':sorted(Z),'sigma':'PASS'}
assert len(checks)==16 and set(checks)==set(peer['named_implications'])

# Match the fourteen already supplied fixtures, never enumerate new rooms.
fixtures={}
base=H|low|BC|NSW|C(['E-','T-'])
for cap in ['D-','D+','R-','R+']:fixtures['Llower_Bcenter_Nsw_'+cap]=base|C([cap])
base=H|rect|BC|EC|C(['Nb-','T-'])
for dc,rc in [('D-','R-'),('D-','R+'),('D+','R+')]:fixtures['Lrectangle_Bcenter_Ecenter_'+dc+rc]=base|C([dc,rc])
base=H|upper|EC
fixtures['Lupper_Ecenter_Bouter_Rminus']=base|BO|C(['T-','Nb-','R-'])
for rc in ['R-','R+']:fixtures['Lupper_Ecenter_Ncenter_Dminus_'+rc]=base|NC|C(['B+','T-','D-',rc])
for cap in ['D+','R-']:fixtures['Lupper_Ecenter_Nsw_'+cap]=base|NSW|C(['B+','T-',cap])
fixtures['Lupper_Ecenter_Dcenter_Rplus']=base|fan('D',[1,2])|C(['B+','T-','Nb-','R+'])
fixtures['Lupper_Ecenter_Rcenter_Dminus']=base|fan('R',[3,4])|C(['B+','T-','Nb-','D-'])
assert len(fixtures)==14 and set(fixtures)==set(peer['hand_forced_fixtures'])
edges=Counter(tuple(sorted(e)) for t in H for e in [(t[0],t[1]),(t[1],t[2]),(t[2],t[0])])
hbound={e for e,c in edges.items() if c==1}
receipts={}
for name,expected in fixtures.items():
 record=peer['hand_forced_fixtures'][name];ts=set(map(tri,record['triangles']))
 assert ts==expected,name
 V=polygon(ts);assert V==list(map(tuple,record['vertices']))
 ld=ledger(ts);assert ld==record['ledger'] and (ld['W'],ld['k'],ld['Delta'])==(20,6,4)
 charges=[];groups={}
 for t in ts:
  a=next(p for p in t if g.label(p)=='A');groups.setdefault(a,[]).append(t)
 for a,tt in groups.items():
  if len(tt)==8:continue
  touched=set()
  for t in tt:
   edge=tuple(sorted(p for p in t if p!=a))
   if edge in hbound:touched.add(next(p for p in edge if g.label(p)=='C'))
  q=3 if len(tt)==4 else len(tt);degree=len(touched);e=q-degree
  if e:charges.append({'A':list(a),'q':q,'d':degree,'e':e})
 assert sorted(charges,key=lambda r:r['A'])==sorted(record['charges'],key=lambda r:r['A'])
 assert sorted(c['e'] for c in charges)==[1,1,2] and all(c['d']==1 for c in charges)
 assert ld['Delta']-sum(c['e'] for c in charges)==0
 receipts[name]={'geometry':'PASS_ORIGINAL_ROOM','ledger':ld,'charges':charges,'b':0,'optics':'OPEN'}
covered={'Lrectangle_Bcenter_Ecenter_D+R+':'2997','Lupper_Ecenter_Nsw_D+':'2997','Lupper_Ecenter_Nsw_R-':'2240'}
for name,key in covered.items():
 ts=fixtures[name];P=paths[key];V=polygon(ts);U,Z=path_requirements(P)
 assert U<=ts and not Z&ts
 assert replay(V,(0,0),(2,2),P)==len(P)-2
 assert replay(V,(2,2),(0,0),P[::-1])==len(P)-2
 assert replay([sigma(p) for p in V],(0,0),(2,2),sigpath(P))==len(P)-2
 receipts[name]['optics']='CLOSED_FIXED_FIRST_T_FORWARD_REVERSE_SIGMA';receipts[name]['source_line']=key
open_names=sorted(set(fixtures)-set(covered));assert len(open_names)==11
assert open_names==sorted(peer['optically_open_fixture_names'])

# Local fan windows only, not completed budget rooms.
windows=[];survive=[]
for m in [3,4]:
 for start in range(8):
  ss={(start+i)%8 for i in range(m)}
  outside=any(pair<=ss for pair in [{1,2},{3,4},{5,6}])
  good=0 in ss and not outside
  windows.append({'m':m,'start':start,'has_Lplus':0 in ss,'outside_C_pair':outside,'survives':good})
  if good:survive.append((m,start))
assert survive==[(3,6),(3,7),(4,6)]

def angle(ts,p,expected):
 owners=g.owners_of(list(ts));opens={e for e,ii in owners.items() if len(ii)==2}
 aa,inside=g.check_fan_angles(list(ts),p,owners,opens)
 assert aa==[expected//45] and not inside,(p,aa,inside,expected)
 return expected
specangles=[
 ('lower_B_needed',H|low,(-1,-1),180),('lower_BC_repairs',H|low|BC,(-1,-1),225),
 ('lower_Nbminus_forbidden',H|low|BC|C(['Nb-']),(-1,1),180),
 ('lower_Ncenter_forbidden',H|low|BC|NC,(-1,1),180),('lower_Nsw_repairs',H|low|BC|NSW,(-1,1),225),
 ('rectangle_B_needed',H|rect,(-1,-1),180),('rectangle_BC_repairs',H|rect|BC,(-1,-1),225),
 ('rectangle_N_needed',H|rect,(-1,1),180),('rectangle_Nbminus_repairs',H|rect|C(['Nb-']),(-1,1),225),
 ('rectangle_Ncenter_repairs',H|rect|NC,(-1,1),225),('rectangle_Nsw_repairs',H|rect|NSW,(-1,1),270),
 ('upper_N_needed',H|upper,(-1,1),180),('upper_Nbminus_repairs',H|upper|C(['Nb-']),(-1,1),225),
 ('upper_Ncenter_repairs',H|upper|NC,(-1,1),225),('upper_Nsw_repairs',H|upper|NSW,(-1,1),270),
 ('upper_Bcenter_forbidden',H|upper|BC,(-1,-1),180),
 ('Ecenter_Tcenter_forbidden',H|EC|fan('Tc',[5,6]),(3,3),180),
 ('Touter_Nrplus_needed',H|upper|EC|TO,(1,3),180),
 ('Touter_Nrplus_repairs',H|upper|EC|TO|C(['Nr+']),(1,3),225),
 ('Dplus_Rminus_forbidden',H|C(['D+','R-']),(3,-1),180),
 ('Dupperquarter_Rminus_needed',H|fan('D',[0,1]),(3,-1),180),
 ('Dupperquarter_Rminus_repairs',H|fan('D',[0,1])|C(['R-']),(3,-1),225),
 ('Rlowerquarter_Dplus_needed',H|fan('R',[4,5]),(3,-1),180),
 ('Rlowerquarter_Dplus_repairs',H|fan('R',[4,5])|C(['D+']),(3,-1),225),
 ('Dcenter_Rminus_forbidden',H|fan('D',[1,2])|C(['R-']),(3,-1),180),
 ('Rcenter_Dplus_forbidden',H|fan('R',[3,4])|C(['D+']),(3,-1),180),
]
angles={name:{'point':p,'boundary_degrees':angle(ts,p,a)} for name,ts,p,a in specangles}
assert len(angles)==26
# With Q=7+n, Delta4 gives sN=5-n, and k6 gives n=J-1.
counts={}
for J in [4,5]:
 n=J-1;Q=7+n;sN=5-n
 assert Q+sN-8==4 and J+sN==6
 counts[str(J)]={'J':J,'ordinary_caps':n,'Q':Q,'sN':sN,'k':6}
# Only the named remote forbidden triangle ownership is examined.
remote=tri(((-2,1),(-2,2),(-1,1)))
assert next(p for p in remote if g.label(p)=='A')==(-2,2)
assert remote not in H|set().union(*(full(n) for n in centers))
out={'status':'INDEPENDENT_CRITICAL_L_PARTIAL_REDUCTION_CHECKS_PASS','guard_implications':checks,
 'original_fixture_checks':receipts,'optically_open_fixture_names':open_names,'retained_four_sources':retained,
 'L_local_fan_windows':windows,'local_angle_identities':angles,'cap_count_identities':counts,
 'square_exchange_ports':{'u':'1/6','d':'1/6','exit':'1/2'},
 'input_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in [
 'fourth-surplus-review/mixed-e2-e1/critical-L.txt','fourth-surplus-review/mixed-e2-e1/critical-L-check.json',
 'surplus-four-local/mixed-root-leaf-review/check.py','third-surplus-review/local-mixed-project.json',
 'first-surplus-review/bottom-residual-check.json','first-surplus-review/square-exchange-check.json',
 'surplus-four-local/single-e2-check.json','triangle-composition/inputs/guard_checker.py',
 'triangle-composition/inputs/boundary_replay.py','triangle-composition/inputs/illumination_geometry.py']},
 'limits':'Own retained guard/geometry/replay helpers;16 specified implications,14 original rooms,3 prescribed closures,16 local fan windows,26 named local angles. No peer checker execution, new completed room/cap assignments, path/word/direction discovery, raw archive, solver or workers. Hand completeness review is separate in review.txt; eleven room optics stay open.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('16wholeguards/sigma;14originalgeometries;3firstTclosures;16localwindows;26localangles;11OPTICSOPEN.')
