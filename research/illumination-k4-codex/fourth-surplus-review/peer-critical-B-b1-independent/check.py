"""Independent reconstruction of the stated 38 implications and local budgets.
No peer checker execution, room/cap-assignment census, or discovery.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
PEER=ROOT/'surplus-four-local/e2-e1-b1'
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
from boundary_replay import on,sub,cross,dot
rays=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
reads=[]
def read(rel):
 p=ROOT/rel;reads.append(p);return json.loads(p.read_text())
def decode(P):return [tuple(F(*x) if isinstance(x,list) else F(x) for x in p) for p in P]
def fan(site,ss):
 a=centers[site] if isinstance(site,str) else site
 return {tuple(sorted((a,(a[0]+rays[i%8][0],a[1]+rays[i%8][1]),(a[0]+rays[(i+1)%8][0],a[1]+rays[(i+1)%8][1])))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
zero=read('zero-surplus-L/cover-check.json')['paths']
P={
 'five':decode(read('second-surplus-review/five-path-check.json')['five_path']),
 'sigma13':decode(zero['thirteen_sigma']['path']),
 'T3':[sigma(p) for p in decode(read('first-surplus-review/residual-cover-check.json')['path'])[::-1]],
 'E6':[sigma(p) for p in decode(read('first-surplus-review/bottom-residual-check.json')['path'])[::-1]],
 'uniform7':decode(read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path']),
 'L12':decode(read('first-surplus-review/centered-left-check.json')['paths']['left']['path']),
 'E11':decode(read('first-surplus-review/square-exchange-check.json')['paths']['E_thirteen']['path']),
 'one_sigma':decode(zero['one_sigma']['path']),
 'four_sigma':decode(zero['four_sigma']['path'])}
P['Lsquare5']=[P['uniform7'][0],(F(-2),F(1,3))]+P['uniform7'][4:]
P['top_square3']=[(F(0),F(0)),(F(1,6),F(1)),(F(2,3),F(-2)),(F(5,3),F(4)),(F(2),F(2))]
force=read('third-surplus-review/independent-review/guard-extension-check.json')['forcing_paths']
for k in ['outerB2','sigma_outerB2','sigma_centeredB3']:P[k]=decode(force[k]['path'])
req={}
for k,path in P.items():
 assert path[0]==(0,0) and path[-1]==(2,2)
 assert all(not on((2,2),a,b) for a,b in zip(path[:-2],path[1:-1]))
 u,z=path_requirements(path)
 ur,zr=path_requirements(path[::-1]);assert (ur,zr)==(u,z)
 us,zs=path_requirements([sigma(p) for p in path[::-1]]);assert (us,zs)==(tr(u),tr(z))
 req[k]=(u,z)
L0=fan('L',[0]);E4=fan('E',[4]);T5=fan('Tc',[5]);DR=full('D')|full('R')
LC=fan('L',[7,0]);LO=fan('L',[0,1]);EC=fan('E',[3,4]);EO=fan('E',[4,5]);TC=fan('Tc',[5,6]);TO=fan('Tc',[4,5])
clauses=[]
def check(name,key,mi,ma):
 u,z=req[key];assert u<=mi,(name,'missing',u-mi)
 assert not z&ma,(name,'forbidden',z&ma)
 clauses.append({'name':name,'path':key,'minimum':sorted(mi),'maximum':sorted(ma),'status':'PASS'})
b=fan('B',[0,1,2])
# Nine proof cases, rebuilt from prose, not the peer receipt.
check('Beast012_awayT_N6abs','five',H|b|T5,H|b|T5|full('L')|full('E')|DR|(full('N')-fan('N',[6])))
for name,k,partner,other in [('LC','L12',LC,E4),('LO','Lsquare5',LO,E4),('EC','E6',EC,L0),('EO','E11',EO,L0)]:
 mi=H|b|partner|other
 check('Beast012_'+name+'_N6',k,mi,mi|T5|DR|fan('N',[6]))
check('Beast012_noncritical_N456','sigma13',H|b|L0|E4,H|b|L0|E4|T5|DR|fan('N',[4,5,6]))
check('Beast012_Tcenter','T3',H|b|E4|TC,H|b|E4|TC|full('L')|DR|full('N'))
check('Beast012_Touter_N6abs','top_square3',H|b|TO,H|b|TO|full('L')|full('E')|DR|(full('N')-fan('N',[6])))
check('Beast012_Touter_N7abs','uniform7',H|b|L0|E4|TO,H|b|L0|E4|TO|DR|(full('N')-fan('N',[7])))
# Four named root families x six conditional implications only.
for label,ss in [('O3_701',[7,0,1]),('O4_6701',[6,7,0,1]),('H4_7012',[7,0,1,2]),('West1234',[1,2,3,4])]:
 b=fan('B',ss)
 check(label+'_ordinaryLE_N7abs','uniform7',H|b|L0|E4,H|b|L0|E4|DR|full('Tc')|(full('N')-fan('N',[7])))
 check(label+'_LO_N7abs','Lsquare5',H|b|LO|E4,H|b|LO|E4|DR|full('Tc')|(full('N')-fan('N',[7])))
 check(label+'_Tcenter','T3',H|b|E4|TC,H|b|E4|TC|DR|full('L')|full('N'))
 check(label+'_EC_N0abs','E6',H|b|L0|EC,H|b|L0|EC|DR|full('Tc')|(full('N')-fan('N',[0])))
 for name,key,partner,other in [('EO','E11',EO,L0),('LC','L12',LC,E4)]:
  check(label+'_'+name+'_T6N0N7abs',key,H|b|partner|other,H|b|partner|other|DR|(full('Tc')-fan('Tc',[6]))|(full('N')-fan('N',[0,7])))
assert len(clauses)==33
allK=H|set().union(*(full(k) for k in centers))
check('force_E4','one_sigma',H,allK-E4)
check('force_L0_Eordinary','four_sigma',H|E4,(allK-full('E')-L0)|E4)
for label,k,e in [('Ecenter','sigma_centeredB3',EC),('Eouter','sigma_outerB2',EO)]:
 check('force_L0_'+label,k,H|e,(allK-full('E')-L0)|e)
check('force_T5_Beast_B2harmless','outerB2',H|fan('B',[0,1,2]),(allK-full('B')-T5)|fan('B',[0,1,2]))
assert len(clauses)==38
receipt=read('surplus-four-local/e2-e1-b1/critical-B-check.json')
other={x['name']:x for x in receipt['whole_envelopes']}
assert len(other)==38
for c in clauses:
 o=other[c['name']]
 assert o['path']==c['path'] and o['minimum']==json.loads(json.dumps(c['minimum'])) and o['maximum']==json.loads(json.dumps(c['maximum']))
# New normal exchange: identical entry/exit states, strict physical mirror hits.
entry=(F(3,2),F(3));exit=(F(11,6),F(3));hit=(F(5,3),F(4))
for a,b,v in [(P['five'][2],entry,(1,6)),(entry,P['five'][3],(1,6)),(P['five'][5],exit,(1,-6)),(exit,P['five'][6],(1,-6)),(entry,hit,(1,6)),(hit,exit,(1,-6))]:
 assert cross(sub(b,a),v)==0 and dot(sub(b,a),v)>0
assert 0<F(1,2)<F(1,2)+2*F(1,6)<1
walls=[((0,1),(1,1)),((0,-2),(1,-2)),((1,4),(2,4))]
for a,p,b,(c,e) in zip(P['top_square3'],P['top_square3'][1:],P['top_square3'][2:],walls):
 assert on(p,c,e) and p not in (c,e)
 v=sub(p,a);w=sub(e,c);rv=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert cross(rv,sub(b,p))==0 and dot(rv,sub(b,p))>0
q=(F(2),F(2))
for a,b in walls[::-1]:
 w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert q==(2,12)
# Local angle/J/b checks: separate slot maxima, never global assignments.
def angle(ts,p):
 total=0
 for t in ts:
  if p in t:
   a,b=[sub(v,p) for v in t if v!=p]
   total+=90 if dot(a,b)==0 else 45
 return total
opts=lambda k,ss:[set()]+[fan(k,[i]) for i in ss]
def bounds(name,fixed,slots,J):
 pts={p for t in fixed for p in t}
 for choices in slots.values():pts.update(p for ts in choices for t in ts for p in t)
 rows={};fullpoints=[]
 for p in sorted(pts):
  if p[0]%2==p[1]%2==0:continue
  base=angle(fixed,p);terms={k:sorted({angle(ts,p) for ts in choices}) for k,choices in slots.items()}
  upper=base+sum(max(xs) for xs in terms.values())
  if base==360:assert upper==360;fullpoints.append(p)
  else:assert upper<360,(name,p,base,terms)
  rows[str(p)]={'fixed':base,'terms':terms,'upper':upper}
 assert len(fullpoints)==J,(name,fullpoints,J)
 return {'J':J,'full':fullpoints,'vertices':rows}
local={}
west=H|fan('B',[1,2,3,4])|LC|E4
slots={'Tc':opts('Tc',[5,6]),'D':opts('D',[1,2]),'R':opts('R',[3,4]),'N':opts('N',[0,5,6,7])}
local['west_LC']=bounds('west_LC',west,slots,4)
assert 4+1==1+len(slots)
# Evaluate coefficients symbolically by vertex, excluding the H-side C/M baseline.
def coefficients(name,fixed,variables,expected_B,expected_C):
 pts={p for t in fixed|set().union(*variables.values()) for p in t if not (p[0]%2==p[1]%2==0)}
 rows={}
 for p in sorted(pts):
  const=angle(fixed,p);cs={k:angle(ts,p) for k,ts in variables.items() if angle(ts,p)}
  rows[str(p)]={'constant':const,'terms':cs}
  if p in expected_B:
   assert (const,cs)==expected_B[p]
  elif p in expected_C:
   assert const==180 and not cs
  elif p[0]%2==p[1]%2==1:
   assert const>=225 or const+sum(cs.values())<180,(name,p,const,cs)
  elif angle(H,p)!=180: # all remaining H-side C at180 belong to M
   assert const>=225 or const+sum(cs.values())<180,(name,'extra C',p,const,cs)
 return rows
variables={'T5':T5,'T6':fan('Tc',[6]),'D1':fan('D',[1]),'D2':fan('D',[2]),'R3':fan('R',[3]),'R4':fan('R',[4]),'N0':fan('N',[0]),'N5':fan('N',[5]),'N6':fan('N',[6]),'N7':fan('N',[7])}
local['west_b']=coefficients('west',west,variables,{(-1,1):(135,{'N5':45}),(1,3):(90,{'T5':45,'N0':45}),(3,-1):(90,{'D1':45,'R4':45})},{(-1,-2)})
for label,ss,h in [('O3',[7,0,1],0),('O4',[6,7,0,1],0),('H4',[7,0,1,2],1)]:
 b=fan('B',ss)
 assert angle(H|b,(1,-2))==180 and angle(H|b|fan('D',[2,3]),(1,-2))==270
 assert angle(H|b|LO,(-1,1))==180
 assert angle(H|b|TO,(1,3))==180
 assert angle(H|b|fan('N',[7,0])|T5,(1,3))==180
 assert not any((1,-2) in t for k in ['L','R','E','Tc','N'] for t in full(k))
 fixedEC=H|b|L0|EC|fan('N',[0])
 assert angle(fixedEC|T5,(1,3))==180 and angle(fixedEC|fan('Tc',[6]),(3,3))==180
 local[label+'_EC']=bounds(label+'_EC',fixedEC,{'D':opts('D',[1,2]),'R':opts('R',[3,4])},3+h)
 assert (3+h)+1==(4 if not h else 5)
 fixedD=H|b|fan('D',[2,3])|L0|E4
 local[label+'_D23']=bounds(label+'_D23',fixedD,{'Tc':opts('Tc',[5,6]),'R':opts('R',[3,4]),'N':opts('N',[0,5,6,7])},3+h)
 local[label+'_b']=coefficients(label,fixedD,{k:v for k,v in variables.items() if not k.startswith('D')},{(-1,1):(135,{'N5':45}),(1,3):(90,{'T5':45,'N0':45})},set())
assert angle(H|fan('B',[7,0,1,2])|LC,(-1,-1))==180
assert angle(H|fan('Tc',[6,7])|E4,(3,3))==180
assert angle(H|fan('B',[1,2,3,4])|L0,(-1,-1))==180
assert angle(west,(-1,-1))==225
assert not any((-1,-2) in t for k in centers if k!='B' for t in full(k))
# Local active e1 windows, not complete room assignments.
root_options={'L':[[7,0],[0,1]],'E':[[3,4],[4,5]],'Tc':[[4,5],[5,6]],'D':[[0,1],[1,2],[2,3]],'R':[[2,3],[3,4],[4,5]],'N':[[4,5],[5,6],[7,0],[0,1]]}
assert [s for s in root_options['N'] if 6 in s]==[[5,6]]
assert [s for s in root_options['D'] if any((1,-2) in t for t in fan('D',s))]==[[2,3]]
# Only L70 among forced-L0 unit options heals the second west smooth point.
assert [s for s in root_options['L'] if angle(H|fan('B',[1,2,3,4])|fan('L',s),(-1,-1))!=180]==[[7,0]]
proof=PEER/'critical-B.txt';selfproof=PEER/'critical-B-self-audit.txt'
reads += [proof,selfproof,PEER/'critical-B-check.py',PEER/'argument.txt',Path(__file__),ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py']
result={'status':'INDEPENDENT_CRITICAL_B_B1_CONSOLIDATION_CHECK_PASS','whole_envelopes':clauses,'local_bounds_and_coefficients':local,'new3_exchange_and_finitewalls_firstT_reverse_sigma':'PASS','new3_unfolded_target':list(map(str,q)),'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)},'limits':'Rebuilt 33 optical and5 forcing envelopes, 7 local J bounds and symbolic b coefficients; inherited earlier two-root/root-leaf geometry, budget identity and accepted existing path proofs. No peer checker execution, newroom/cap assignment census/search/archive/worker. Hand dispatch verdict in review.txt.'}
(HERE/'check.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: all38 rebuilt envelopes; new3 finite/normalexchange/unfold; all7 localJ bounds, joined/west b coefficients, active-window and budget restrictions.')
