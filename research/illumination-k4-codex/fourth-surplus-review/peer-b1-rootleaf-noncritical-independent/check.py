"""Independent fixed eights, one supplied polygon, whole-support transfers.
No peer execution/import, new room, direction/word discovery or archive scan.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident
from boundary_replay import replay,on,sub,cross,dot
import illumination_geometry as geo
reads=[]
def read(p):reads.append(p);return json.loads(p.read_text())
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(k,ss):
 a=C[k] if isinstance(k,str) else k
 return {tuple(sorted((a,tuple(a[j]+R[i%8][j] for j in (0,1)),tuple(a[j]+R[(i+1)%8][j] for j in (0,1))))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(full(p) for p in ((0,0),(2,0),(2,2))))
allK=H|set().union(*(full(k) for k in C))
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
def fp(xs):return [tuple(F(x) for x in p) for p in xs]
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[sub(v,p) for v in t if v!=p];n+=90 if dot(a,b)==0 else 45
 return n
def provenance(receipt,path):
 for rel,digest in receipt['source_sha256'].items():
  p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,rel
 p=path.parent/'verify.py';reads.append(p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['checker_sha256']
records={}
def optical(name,P,walls,mi,ma,image,parent):
 u,z=path_requirements(P)
 assert u<=mi and not z&ma,(name,u-mi,z&ma)
 assert P[0]==(0,0) and P[-1]==(2,2)
 assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
 for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
  assert on(p,c,e) and p not in (c,e),(name,p)
  v=sub(p,a);w=sub(e,c)
  ref=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
  assert cross(ref,sub(b,p))==0 and dot(ref,sub(b,p))>0
 assert len(walls)==len(P)-2
 a,b=path_requirements(P[::-1]);assert (a,b)==(u,z)
 a,b=path_requirements([sigma(p) for p in P[::-1]]);assert (a,b)==(tr(u),tr(z))
 q=P[-1]
 for a,b in walls[::-1]:
  w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert q==image,(name,q,image)
 if parent is not None:
  assert u==decode(parent['required']) and z==decode(parent['forbidden'])
  assert mi==decode(parent['minimum']) and ma==decode(parent['maximum'])
 records[name]={'path':[[str(x) for x in p] for p in P],'reflections':len(P)-2,'U':len(u),'Z':len(z),'unfold':list(map(str,q)),'required':sorted(u),'forbidden':sorted(z),'minimum':sorted(mi),'maximum':sorted(ma)}
 return u,z
parent_dir=ROOT/'surplus-four-local/e2-e1-b1';parent=read(parent_dir/'check.json')
for rel,pin in parent['input_hashes'].items():
 p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==pin,rel
catalog=read(ROOT/'third-surplus-review/path-support-check.json');data={}
for rel,pin in catalog['sources'].items():
 p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==pin;data[rel]=json.loads(p.read_text())
def pd(P):return [tuple(F(*x) for x in p) for p in P]
zero=data['zero-surplus-L/cover-check.json']['paths'];sq=data['first-surplus-review/square-exchange-check.json']['paths']
paths={n:pd(zero[k]['path']) for n,k in [('one','one'),('four','four'),('13','thirteen'),('sigma13','thirteen_sigma')]}
paths['L3']=pd(data['first-surplus-review/residual-cover-check.json']['path']);paths['B6']=pd(data['first-surplus-review/bottom-residual-check.json']['path']);paths['five']=pd(data['second-surplus-review/five-path-check.json']['five_path'])
paths['T3']=[sigma(p) for p in paths['L3'][::-1]];paths['E6']=[sigma(p) for p in paths['B6'][::-1]]
for k in ('L','B','E','T'):paths[k+'11']=pd(sq[k+'_thirteen']['path'])
ff=data['third-surplus-review/independent-review/guard-extension-check.json']['forcing_paths']
for n,k in [('centerB3','centeredB3'),('outerB2','outerB2')]:paths[n]=pd(ff[k]['path'])
paths['uniform7']=fp(read(ROOT/'surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path'])
ref={'L':0,'B':1,'E':4,'Tc':5};caps={name:fan(k,(i,)) for name,k,i in [('L+','L',0),('E-','E',4),('T-','Tc',5),('T+','Tc',6),('R-','R',4),('R+','R',3),('Nb-','N',5),('Nb+','N',6),('Nr-','N',7),('Nr+','N',0)]}
def cap(names):return set().union(*(caps[n] for n in names)) if names else set()
checks=[]
def guard(name,P,mi,ma,record):
 U,Z=path_requirements(P);assert U<=mi and not Z&ma,name
 assert U==decode(record['required']) and Z==decode(record['forbidden']) and len(P)-2==record['reflections'],name
 Us,Zs=path_requirements([sigma(p) for p in P[::-1]]);assert Us==tr(U) and Zs==tr(Z)
 checks.append({'name':name,'reflections':len(P)-2,'U':len(U),'Z':len(Z)})
Nforms={}
for m in (3,4):
 for start in range(8):
  ss=frozenset((start+j)%8 for j in range(m));sides=int(bool(ss&{5,6}))+int(bool(ss&{7,0}))
  if sides==1 and not {6,7}<=ss:Nforms[ss]='bottom' if ss&{5,6} else 'right'
assert len(Nforms)==8 and set(Nforms)=={frozenset(ss) for ss in parent['eight_N_root_forms'].values()}
forms={'L':{'C':(7,0),'O':(0,1)},'B':{'C':(1,2),'O':(0,1)},'E':{'C':(3,4),'O':(4,5)},'Tc':{'C':(5,6),'O':(4,5)}};DR=full('D')|full('R')
for record in parent['N_whole_family_guards']:
 name=record['name'];tag,suffix=name.rsplit('_',1);ss=parent['eight_N_root_forms'][tag];side=Nforms[frozenset(ss)]
 if suffix=='noncritical':
  mi=H|fan('N',ss)|set().union(*(fan(k,(i,)) for k,i in ref.items()));key='sigma13' if side=='bottom' else '13'
 else:
  site,typ=suffix[:-1],suffix[-1];mi=H|fan('N',ss)|fan(site,forms[site][typ])|set().union(*(fan(k,(i,)) for k,i in ref.items() if k!=site))
  if typ=='C':key={'L':'L3','B':'sigma13' if side=='bottom' else 'B6','E':'E6' if side=='bottom' else '13','Tc':'T3'}[site]
  elif side=='bottom':key={'L':'L11','B':'sigma13' if 6 in ss else 'five','E':'E11','Tc':'sigma13'}[site]
  else:key={'L':'13','B':'five','E':'13','Tc':'T11'}[site]
 assert key==record['selected_path'];guard(name,paths[key],mi,mi|DR,record)
assert len(checks)==72
forcing={r['name']:r for r in parent['reference_forcing']}
for label,key,mi,ma in [('Bplus','one',H,allK-fan('B',(1,))),('Tminus_ordinaryB','four',H|fan('B',(1,)),(allK-full('B')-fan('Tc',(5,)))|fan('B',(1,))),('Tminus_centerB','centerB3',H|fan('B',(1,2)),(allK-full('B')-fan('Tc',(5,)))|fan('B',(1,2))),('Tminus_outerB','outerB2',H|fan('B',(0,1)),(allK-full('B')-fan('Tc',(5,)))|fan('B',(0,1)))]:
 guard(label,paths[key],mi,ma,forcing[label]);guard('sigma_'+label,[sigma(p) for p in paths[key][::-1]],tr(mi),tr(ma),forcing['sigma_'+label])
U,Z=path_requirements(paths['outerB2']);assert U<=H|fan('B',(0,1,2)) and not Z&((allK-full('B')-fan('Tc',(5,)))|fan('B',(0,1,2)))
beast=H|fan('B',(0,1,2))|cap(['L+','E-','T-']);pair={v['name']:v for v in parent['Beast_and_opposite_leaf_guards']}
guard('Beast_without_Nbplus',paths['five'],beast,beast|DR|(full('N')-fan('N',(6,))),pair['Beast_without_Nbplus'])
guard('Beast_with_Nbplus',paths['sigma13'],beast|fan('N',(6,)),beast|DR|fan('N',(4,5,6)),pair['Beast_with_Nbplus'])
guard('B_leaf_missing_Bplus',paths['one'],H,allK-fan('B',(1,)),pair['B_leaf_missing_Bplus'])
parent_rows={v['name']:v for v in parent['six_joined_B_leaf_uniform7_guards']};coeff={};ordinary=['T-','T+','R-','R+','Nb-','Nb+','Nr-','Nr+']
for name,ss in [('O3',(7,0,1)),('O4',(6,7,0,1)),('H4',(7,0,1,2))]:
 for leaf in (3,4):
  label=name+'_D'+str(leaf);fixed=H|fan('B',ss)|fan('D',(leaf,));mi=fixed|cap(['L+','E-']);ma=mi|cap([c for c in ordinary if c!='Nr-']);guard(label,paths['uniform7'],mi,ma,parent_rows[label])
  assert angle(fixed,(1,-2))==270 and angle(fixed,(1,-1))==(315 if leaf==3 else 270)
  points={p for t in mi|cap(ordinary) for p in t if p[0]%2 and p[1]%2};out={}
  for point in points:
   constant=angle(mi,point);variables={c:angle(caps[c],point) for c in ordinary if angle(caps[c],point)};out[str(point)]={'fixed_degrees':constant,'ordinary_cap_degrees':variables}
   if point==(-1,1):assert constant==135 and variables=={'Nb-':45}
   elif point==(1,3):assert constant==90 and variables=={'T-':45,'Nr+':45}
   else:assert constant>=225 or constant+sum(variables.values())<180
  assert out==parent['joined_leaf_B_angle_coefficients'][label];coeff[label]=out
assert len(checks)==89
assert angle(H|fan('B',(0,1))|fan('D',(3,4)),(1,-1))==315 and angle(H|fan('B',(0,1)),(1,-1))==270
assert angle(H|fan('B',(0,1))|fan('D',(3,4)),(1,-2))==270 and angle(H|fan('B',(0,1)),(1,-2))==90
for p in ((1,-2),(-1,-1)):assert angle(H|fan('B',(0,1,2,3))|fan('D',(3,))|fan('L',(0,)),p)==180
priorD=read(ROOT/'surplus-four-local/mixed-allroots-review/check.json');priorLeaf=read(ROOT/'surplus-four-local/mixed-leaf-review/check.json')
assert len(priorD['D_root_local_windows'])==9 and priorLeaf['pinned_catalog_paths']==21 and priorLeaf['supplementary_fixed_compositions']==2
assert all(g['complete_U_Z_avoids_D_R'] for g in priorLeaf['path_checks'].values())
reads += [parent_dir/'argument.txt',parent_dir/'check.py',ROOT/'surplus-four-local/mixed-allroots-review/review.txt',ROOT/'surplus-four-local/mixed-leaf-review/review.txt',ROOT/'second-surplus-L/classification.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_E2_E1_B1_ROOT_LEAF_NONCRITICAL_ACCEPT','bound':13,'eight_N_forms':[(sorted(ss),side) for ss,side in Nforms.items()],'checks':checks,'joined_B_coefficients':coeff,'geometry_dependencies':'Previously independentlyaccepted same9Drootarcs andD34flap; deletionnowleavesONEunitbudgetfreeroom, notTWOunit;21fixedcatalogand2compositionscompleteD/Ravoidance.','limits':'ReviewclearsOLDpending89guard obligation. Criticale2L/B/E/T roots handledelsewhere; no fullDelta4/remoteclaim. No newrooms/discovery/archive/peerexecution.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('ACCEPT oldrootleaf/noncriticale2b1:8Nforms/72Nguards+8forcing+3pair+6joined=89')
