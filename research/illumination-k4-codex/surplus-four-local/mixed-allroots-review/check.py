"""Independent exact local topology identities and fixed N-root dispatch guards."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
from boundary_replay import cross,sub,on
import illumination_geometry as g
tri=lambda t:tuple(sorted(map(tuple,t)))
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan_at(c,ss):
 return {tri((c,(c[0]+dirs[i%8][0],c[1]+dirs[i%8][1]),(c[0]+dirs[(i+1)%8][0],c[1]+dirs[(i+1)%8][1]))) for i in ss}
fan=lambda n,ss:fan_at(centers[n],ss)
full=lambda n:fan(n,range(8))
H=set().union(*(fan_at(c,range(8)) for c in [(0,0),(2,0),(2,2)]))
read=lambda rel:json.loads((ROOT/rel).read_text())
caps={n:tri(t) for n,t in read('triangle-composition/inputs/caps.json')['cap_options'].items()}
C=lambda ns:{caps[n] for n in ns}
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tri(sigma(p) for p in t) for t in ts}
sigpath=lambda P:[sigma(p) for p in P[::-1]]

# Local D-root deletion identities, without generating completed rooms.
def contains(p,t):
 values=[cross(sub(t[(i+1)%3],t[i]),sub(p,t[i])) for i in range(3)]
 return all(v>=0 for v in values) or all(v<=0 for v in values)
def intersect(a,b):
 points={tuple(map(F,p)) for p in a if contains(p,b)}
 points|={tuple(map(F,p)) for p in b if contains(p,a)}
 for x,y in zip(a,a[1:]+a[:1]):
  v=sub(y,x)
  for u,w in zip(b,b[1:]+b[:1]):
   z=sub(w,u);den=cross(v,z)
   if not den:continue
   t=cross(sub(u,x),z)/den;s=cross(sub(u,x),v)/den
   if 0<=t<=1 and 0<=s<=1:points.add(tuple(x[k]+t*v[k] for k in (0,1)))
 return points
Bpossible=fan('B',[0,1,2,3]);Rpossible=fan('R',[2,3,4,5])
far=set().union(*(full(n) for n in ['L','E','Tc','N']))
maximum_rest=H|Bpossible|Rpossible|far
Dchecks=[]
for m in [3,4]:
 for st in range(8):
  ss={(st+i)%8 for i in range(m)}
  if not ss&{1,2}:continue
  tiles=fan('D',ss);arc=[]
  if 1 in ss:arc.append(((2,-1),(3,-1)))
  if 2 in ss:arc.append(((1,-1),(2,-1)))
  if 3 in ss:
   assert 2 in ss;arc.append(((1,-2),(1,-1)))
  if 0 in ss:assert 1 in ss
  # Every declared edge is shared with the max rest along its entire length.
  for a,b in arc:
   assert any(contains(a,t) and contains(b,t) for t in tiles)
   assert any(contains(a,t) and contains(b,t) for t in maximum_rest)
  graph={}
  for a,b in arc:graph.setdefault(a,set()).add(b);graph.setdefault(b,set()).add(a)
  seen={next(iter(graph))};queue=list(seen)
  for p in queue:
   for q in graph[p]:
    if q not in seen:seen.add(q);queue.append(q)
  assert seen==set(graph) and max(map(len,graph.values()))<=2
  assert sum(len(v)==1 for v in graph.values())==2
  for a in tiles:
   for b in maximum_rest:
    points=intersect(a,b)
    assert all(any(on(p,*e) for e in arc) for p in points),(m,st,a,b,points)
    if b in far:assert not points
  assert not any(contains((2,-2),t) for t in maximum_rest)
  Dchecks.append({'m':m,'start':st,'sectors':sorted(ss),'maximum_attach_arc':arc,
   'status':'EXACT_SINGLE_PROPER_ARC_AND_NO_EXTRA_CONTACT'})
assert len(Dchecks)==9

def angle_info(tiles,p):
 owners=g.owners_of(list(tiles));opens={e for e,ii in owners.items() if len(ii)==2}
 angles,inside=g.check_fan_angles(list(tiles),p,owners,opens)
 return [45*a for a in angles],inside
junctions={}
for label,ss in [('empty',[]),('ordinary_plus',[1]),('ordinary_minus',[2]),('eastquarter',[0,1]),('center',[1,2]),('westquarter',[2,3])]:
 aa,inside=angle_info(H|fan('B',ss),(1,-1))
 assert len(aa)==1 and aa[0] in [180,225,270] and not inside
 junctions['B:'+label]=aa[0]
for label,ss in [('empty',[]),('ordinary_plus',[3]),('ordinary_minus',[4]),('upper',[2,3]),('center',[3,4]),('lower',[4,5])]:
 aa,inside=angle_info(H|fan('R',ss),(3,-1))
 assert len(aa)==1 and aa[0] in [90,135,180] and not inside
 junctions['R:'+label]=aa[0]
assert angle_info(H,(2,-1))==([180],False)

# Check pinned existing path coordinates; do not execute discovery or peer checkers.
catalog=read('third-surplus-review/path-support-check.json');records={}
for source,pinned in catalog['sources'].items():
 raw=(ROOT/source).read_bytes();assert hashlib.sha256(raw).hexdigest()==pinned
 data=json.loads(raw)
 if 'forcing_paths' in data:rr={n:r['path'] for n,r in data['forcing_paths'].items()}
 elif 'paths' in data:rr={n:r['path'] for n,r in data['paths'].items()}
 else:rr={None:data.get('path',data.get('five_path'))}
 for key,P in rr.items():records[source+(':'+key if key else '')]=[tuple(F(*v) for v in p) for p in P]
assert set(records)==set(catalog['paths'])
prior_support=read('surplus-four-local/mixed-leaf-review/check.json')
assert prior_support['status']=='INDEPENDENT_HAND_SUPPORT_AND_DELETION_CHECKS_PASS'
assert prior_support['pinned_catalog_paths']==21 and prior_support['supplementary_fixed_compositions']==2
assert prior_support['sources']==catalog['sources']
assert len(prior_support['path_checks'])==23
assert all(r['complete_U_Z_avoids_D_R'] and r['sigma']=='PASS' for r in prior_support['path_checks'].values())

path=lambda f,k=None:records[f+(':'+k if k else '')]
zero='zero-surplus-L/cover-check.json';sq='first-surplus-review/square-exchange-check.json'
paths={'one':path(zero,'one'),'one_sigma':path(zero,'one_sigma'),
 'four':path(zero,'four'),'four_sigma':path(zero,'four_sigma'),
 '13':path(zero,'thirteen'),'sigma13':path(zero,'thirteen_sigma'),
 'L3':path('first-surplus-review/residual-cover-check.json'),
 'B6':path('first-surplus-review/bottom-residual-check.json'),
 'L12':path('first-surplus-review/centered-left-check.json','left'),
 'five':path('second-surplus-review/five-path-check.json')}
paths['T3']=sigpath(paths['L3']);paths['E6']=sigpath(paths['B6'])
for n in ['L','B','E','T']:paths[n+'11']=path(sq,n+'_thirteen')
force='third-surplus-review/independent-review/guard-extension-check.json'
paths['centerB3']=path(force,'centeredB3');paths['outerB2']=path(force,'outerB2')
paths['BT9']=paths['13'][:8]+[(F(6,11),F(-2)),(F(18,11),F(4))]+paths['13'][14:]
paths['LE9']=sigpath(paths['BT9'])
paths['B6T4']=paths['B6'][:4]+[(F(5,3),F(4))]+paths['B6'][7:]
assert len(paths['BT9'])-2==9 and len(paths['B6T4'])-2==4

# Only the two N fans survive the hand local-window exclusions.
Nfans={'bottom':fan('N',[4,5,6]),'right':fan('N',[7,0,1])}
windows=[];survivors=[]
for m in [3,4]:
 for st in range(8):
  ss={(st+i)%8 for i in range(m)}
  bridge={6,7}<=ss
  outside=({1,2}<=ss) or ({3,4}<=ss)
  touches=bool(ss&{5,6}) or bool(ss&{7,0})
  if touches and not bridge and not outside:survivors.append((m,st))
  windows.append({'m':m,'start':st,'bridge':bridge,'outside_smooth_C_pair':outside})
assert survivors==[(3,4),(3,7)] and tr(Nfans['bottom'])==Nfans['right']

BDR=full('D')|full('R');allK=H|set().union(*(full(n) for n in centers))
forcing=[]
def guard(P,minimum,maximum,name):
 assert P[0]==(0,0) and P[-1]==(2,2)
 U,Z=path_requirements(P);assert U<=minimum,(name,'required',U-minimum)
 assert not Z&maximum,(name,'forbidden',Z&maximum)
 Us,Zs=path_requirements(sigpath(P));assert Us==tr(U) and Zs==tr(Z)
 return {'status':'PASS','reflections':len(P)-2,'required':sorted(U),'forbidden':sorted(Z),'sigma':'PASS'}
forcing_specs=[('Bplus','one',H,allK-C(['B+'])),
 ('Tminus_Bordinary','four',H|C(['B+']),(allK-full('B')-C(['T-']))|C(['B+'])),
 ('Tminus_Bcenter','centerB3',H|fan('B',[1,2]),(allK-full('B')-C(['T-']))|fan('B',[1,2])),
 ('Tminus_Bouter','outerB2',H|fan('B',[0,1]),(allK-full('B')-C(['T-']))|fan('B',[0,1]))]
for name,key,minimum,maximum in forcing_specs:
 for sigma_case in [False,True]:
  P=paths[key];mi,ma=minimum,maximum;nn=name
  if sigma_case:P=sigpath(P);mi,ma=tr(mi),tr(ma);nn='sigma_'+name
  forcing.append({'name':nn,**guard(P,mi,ma,nn)})

critical=['L','B','E','Tc'];reference={'L':'L+','B':'B+','E':'E-','Tc':'T-'}
forms={'L':{'C':[7,0],'O':[0,1]},'B':{'C':[1,2],'O':[0,1]},
 'E':{'C':[3,4],'O':[4,5]},'Tc':{'C':[5,6],'O':[4,5]}}
site_sigma={'L':'Tc','Tc':'L','B':'E','E':'B'};flip={'bottom':'right','right':'bottom'}
clauses=[]
def clause(name,typed,side,P):
 minimum=H|Nfans[side]
 for site in critical:
  minimum|=fan(site,forms[site][typed[site]]) if site in typed else C([reference[site]])
 maximum=minimum|BDR
 row=guard(P,minimum,maximum,name)
 clauses.append({'name':name,'critical_units':typed,'N_fan':side,**row})

for side in Nfans:clause('zero_critical_'+side,{},side,paths['sigma13' if side=='bottom' else '13'])
one_table={'L':{'C':['L3','L3'],'O':['L11','13']},
 'Tc':{'C':['T3','T3'],'O':['sigma13','T11']},
 'B':{'C':['sigma13','B6'],'O':['sigma13','B11']},
 'E':{'C':['E6','13'],'O':['E11','13']}}
for site,ff in one_table.items():
 for form,choices in ff.items():
  for side,key in zip(['bottom','right'],choices):clause('one_'+site+form+'_'+side,{site:form},side,paths[key])
for a,b in combinations(critical,2):
 for side in Nfans:
  typed={a:'O',b:'O'}
  if side=='right':
   key='BT9' if 'B' in typed and 'Tc' in typed else ('B11' if 'B' in typed else ('T11' if 'Tc' in typed else '13'))
  else:key='LE9' if 'L' in typed and 'E' in typed else ('L11' if 'L' in typed else ('E11' if 'E' in typed else 'sigma13'))
  clause('OO_'+a+b+'_'+side,typed,side,paths[key])
cc_exclusions=[]
for a,b in combinations(critical,2):
 for side in Nfans:
  typed={a:'C',b:'C'}
  if (a,b) in [('L','B'),('E','Tc')]:
   p=(-1,-1) if a=='L' else (3,3)
   tiles=H|Nfans[side]|fan(a,forms[a]['C'])|fan(b,forms[b]['C'])
   assert angle_info(tiles,p)==([180],False)
   assert not any(p in t for t in BDR)
   cc_exclusions.append({'pair':[a,b],'N_fan':side,'unhealed_angle_degrees':180})
  else:
   key='L3' if a=='L' else ('T3' if b=='Tc' else ('B6' if side=='right' else 'E6'))
   clause('CC_'+a+b+'_'+side,typed,side,paths[key])
representatives=[('L','E',['L3','L3']),('L','Tc',['L3','L3']),
 ('L','B',['L12','five']),('B','L',['L11','B6']),
 ('B','E',['E11','B6']),('B','Tc',['sigma13','B6T4'])]
for center,outer,keys in representatives:
 for side,key in zip(['bottom','right'],keys):
  typed={center:'C',outer:'O'};P=paths[key]
  clause('CO_'+center+outer+'_'+side,typed,side,P)
  other={site_sigma[k]:v for k,v in typed.items()}
  for k,v in typed.items():assert tr(fan(k,forms[k][v]))==fan(site_sigma[k],forms[site_sigma[k]][v])
  clause('CO_sigma_'+center+outer+'_'+side,other,flip[side],sigpath(P))
# Explicitly verify the larger N fan's two outside mates are invisible
# to every named path and its sigma image, including compositions.
N_mates=fan('N',[1,4])
for key,P in paths.items():
 U,Z=path_requirements(P);assert not (U|Z)&N_mates,key
 Us,Zs=path_requirements(sigpath(P));assert not (Us|Zs)&N_mates,key
U13,Z13=path_requirements(paths['13']);Us13,Zs13=path_requirements(paths['sigma13'])
assert Z13&full('N')==C(['Nb-','Nb+'])
assert Zs13&full('N')==C(['Nr-','Nr+'])
assert len(clauses)==62 and len(forcing)==8 and len(cc_exclusions)==4
assert max(r['reflections'] for r in clauses)<=13
out={'status':'INDEPENDENT_D_R_TOPOLOGY_AND_N_ROOT_DISPATCH_CHECKS_PASS',
 'D_root_local_windows':Dchecks,'erased_junction_angles':junctions,
 'N_local_window_checks':windows,'N_surviving_windows':survivors,
 'reference_forcing':forcing,'conditional_path_clauses':clauses,'centered_pair_exclusions':cc_exclusions,
 'D_R_erasure_hand_verdict':'ACCEPT_WITHOUT_CORRECTIONS','N_root_hand_verdict':'ACCEPT_WITHOUT_CORRECTIONS','reflection_bound':13,'N_outside_mates_full_U_Z':'PASS_ALL_NAMED_PATHS_AND_SIGMA','original_sigma13_full_N_blockers':'EXACT_BOTTOM_AND_RIGHT_CAP_PAIRS','hand_argument':'review.txt',
 'input_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in [
  'fourth-surplus-review/mixed-e2-e1/noncritical-erasure.txt','fourth-surplus-review/mixed-e2-e1/N-root.txt',
  'surplus-four-local/two-unit.txt','third-surplus-review/path-support-check.json',
  'surplus-four-local/mixed-leaf-review/check.json']},
 'limits':'Nine local D fan identities and whole-support fixed existing path implications only. No assembled-room/cap assignment enumeration, discovery, orbit run, archive or peer-checker execution. Global topology and dispatch completeness are hand-reviewed.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('D:9localarcs/12junctions; N:2fans/8forcing/62opticalclauses/4CCexclusions; <=13 PASS.')
