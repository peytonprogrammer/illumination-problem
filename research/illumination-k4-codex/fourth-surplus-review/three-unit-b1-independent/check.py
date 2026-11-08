"""Independent hand-table reconstruction; fixed proofs only, no discovery."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
from collections import defaultdict
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
core=ROOT/'fourth-surplus-review/rplus-exact-one/verify.py'
ns={'__file__':str(core),'__name__':'retained_physical_helpers'}
exec(compile(core.read_text().split("r=json.loads((HERE/'result.json').read_text())")[0],str(core),'exec'),ns)
physical,polygon,sub,cross,dot,tri=[ns[n] for n in ['physical','polygon','sub','cross','dot','tri']]
read=lambda p:json.loads((ROOT/p).read_text());decode=lambda P:[tuple(F(*v) for v in p) for p in P]
D=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def at(a,ss):return {tri((a,(a[0]+D[i%8][0],a[1]+D[i%8][1]),(a[0]+D[(i+1)%8][0],a[1]+D[(i+1)%8][1]))) for i in ss}
def fan(n,ss):return at(centers[n],ss)
def full(n):return fan(n,range(8))
H=set().union(*(at(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in read('zero-surplus-L/guard-incidence-check.json')['cap_options'].items()}
C=lambda names:{caps[n] for n in names}
sigma=lambda p:(2-p[1],2-p[0]);transform=lambda ts:{tri(sigma(p) for p in t) for t in ts};sig=lambda P:[sigma(p) for p in P[::-1]]
siteflip={'L':'Tc','Tc':'L','B':'E','E':'B'}
g=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
zero=read('zero-surplus-L/cover-check.json')['paths'];sq=read('first-surplus-review/square-exchange-check.json')['paths']
P={n:decode(zero[k]['path']) for n,k in [('one','one'),('four','four'),('13','thirteen'),('sigma13','thirteen_sigma')]}
P['L3']=decode(read('first-surplus-review/residual-cover-check.json')['path'])
P['B6']=decode(read('first-surplus-review/bottom-residual-check.json')['path'])
P['L12']=decode(read('first-surplus-review/centered-left-check.json')['paths']['left']['path'])
P['five']=decode(read('second-surplus-review/five-path-check.json')['five_path'])
for n in ['B','E','L','T']:P[n+'11']=decode(sq[n+'_thirteen']['path'])
P['B4']=P['B6'][:4]+[(F(5,3),F(4))]+P['B6'][7:]
P['BT9']=P['13'][:8]+[(F(6,11),F(-2)),(F(18,11),F(4))]+P['13'][14:]
P['LE9']=sig(P['BT9']);P['T3']=sig(P['L3']);P['E6']=sig(P['B6']);P['T12']=sig(P['L12'])
P['fiveTop3']=P['five'][:3]+[(F(5,3),F(4))]+P['five'][6:]
P['L10']=P['L12'][:3]+[(F(4),F(16,11))]+P['L12'][6:]
for key,path in list(P.items()):P['sigma_'+key]=sig(path)
forcing_data=read('third-surplus-review/independent-review/guard-extension-check.json')['forcing_paths']
P['centerB3']=decode(forcing_data['centeredB3']['path']);P['outerB2']=decode(forcing_data['outerB2']['path'])
known=read('third-surplus-review/local-three-unit-check.json')['new_paths']
for n in ['B4','BT9','L10','fiveTop3']:assert P[n]==decode(known[n])
# Own exact local predicates, independent of the peer's topology code.
def on(p,a,b):return cross(sub(b,a),sub(p,a))==0 and 0<=dot(sub(p,a),sub(b,a))<=dot(sub(b,a),sub(b,a))
def inside_closed(p,t):
 z=[cross(sub(t[(i+1)%3],t[i]),sub(p,t[i])) for i in range(3)]
 return all(v>=0 for v in z) or all(v<=0 for v in z)
def meet(a,b):
 points={tuple(map(F,p)) for p in a if inside_closed(p,b)}|{tuple(map(F,p)) for p in b if inside_closed(p,a)}
 for x,y in zip(a,a[1:]+a[:1]):
  for u,v in zip(b,b[1:]+b[:1]):
   d,e,w=sub(y,x),sub(v,u),sub(u,x);den=cross(d,e)
   if den:
    t,s=cross(w,e)/den,cross(w,d)/den
    if 0<=t<=1 and 0<=s<=1:points.add(tuple(x[k]+t*d[k] for k in [0,1]))
 return points
sign=lambda n:(n>0)-(n<0)
def sectors(ts,p):
 out=set()
 for t in ts:
  if p not in t:continue
  rays=[D.index((sign(q[0]-p[0]),sign(q[1]-p[1]))) for q in t if q!=p]
  a,b=rays
  if (b-a)%8>4:a,b=b,a
  length=(b-a)%8;assert length in [1,2]
  for i in range(length):out.add((a+i)%8)
 return out
def single_angle(ts,p):
 ss=sectors(ts,p);assert ss and len(ss)<8
 assert sum(i in ss and (i-1)%8 not in ss for i in range(8))==1
 return 45*len(ss)
maxB=fan('B',[0,1,2,3]);maxR=fan('R',[2,3,4,5]);far=set().union(*(full(n) for n in ['L','E','Tc','N']))
rest=H|maxB|maxR|far;topology=[]
for ss in [[0,1],[1,2],[2,3]]:
 Fd=fan('D',ss);arc=[]
 if 1 in ss:arc.append(((2,-1),(3,-1)))
 if 2 in ss:arc.append(((1,-1),(2,-1)))
 if 3 in ss:assert 2 in ss;arc.append(((1,-2),(1,-1)))
 if 0 in ss:assert 1 in ss
 adjacency=defaultdict(set)
 for a,b in arc:
  adjacency[a].add(b);adjacency[b].add(a)
  assert any(inside_closed(a,t) and inside_closed(b,t) for t in Fd)
  assert any(inside_closed(a,t) and inside_closed(b,t) for t in rest)
 seen={next(iter(adjacency))};todo=list(seen)
 for p in todo:
  for q in adjacency[p]:
   if q not in seen:seen.add(q);todo.append(q)
 assert seen==set(adjacency) and sorted(map(len,adjacency.values())).count(1)==2 and max(map(len,adjacency.values()))<=2
 for a in Fd:
  for b in rest:
   points=meet(a,b)
   assert all(any(on(p,*e) for e in arc) for p in points)
   assert all(any(on(tuple((p[k]+q[k])/2 for k in [0,1]),*e) for e in arc) for p in points for q in points)
 assert not any(inside_closed((2,-2),t) for t in rest)
 topology.append({'D_root':ss,'proper_arc':arc,'status':'PASS'})
leaf=fan('D',[3]);restleaf=H|fan('B',[0,1])|maxR|far;edge=((1,-1),(1,-2))
for a in leaf:
 for b in restleaf:assert all(on(p,*edge) for p in meet(a,b))
for point,before,after in [((1,-1),315,270),((1,-2),180,90)]:
 assert single_angle(H|fan('B',[0,1])|leaf,point)==before
 assert single_angle(H|fan('B',[0,1]),point)==after
topology.append({'D_leaf':[3],'proper_arc':[edge],'status':'PASS'})
junctions=[]
for n,p,forms in [('B',(1,-1),[[],[1],[2],[0,1],[1,2],[2,3]]),('R',(3,-1),[[],[3],[4],[2,3],[3,4],[4,5]])]:
 for ss in forms:junctions.append({'site':n,'sectors':ss,'remaining_angle':single_angle(H|fan(n,ss),p)})
# Every path clause is independently constructed from the hand tables.
checks={}
def verify(name,path,minimum,maximum):
 assert path[0]==(0,0) and path[-1]==(2,2)
 U,Z=g['path_requirements'](path)
 assert U<=minimum,(name,'missing',U-minimum)
 assert not Z&maximum,(name,'blocked',Z&maximum)
 checks[name]={'status':'PASS','reflections':len(path)-2,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(minimum),'maximum':sorted(maximum)}
allK=H|set().union(*(full(n) for n in centers))
for label,key,mi,ma in [
 ('missingB','one',H,allK-C(['B+'])),
 ('missingT_ordinaryB','four',H|C(['B+']),(allK-full('B')-C(['T-']))|C(['B+'])),
 ('missingT_centerB','centerB3',H|fan('B',[1,2]),(allK-full('B')-C(['T-']))|fan('B',[1,2])),
 ('missingT_outerB','outerB2',H|fan('B',[0,1]),(allK-full('B')-C(['T-']))|fan('B',[0,1])),
]:
 verify('forcing_'+label,P[key],mi,ma);verify('forcing_sigma_'+label,sig(P[key]),transform(mi),transform(ma))
crit=['L','B','E','Tc'];reference={'L':'L+','B':'B+','E':'E-','Tc':'T-'}
forms={'L':{'C':[7,0],'O':[0,1]},'B':{'C':[1,2],'O':[0,1]},'E':{'C':[3,4],'O':[4,5]},'Tc':{'C':[5,6],'O':[4,5]}}
def shape(typed):
 ts=H.copy()
 for site in crit:ts|=fan(site,forms[site][typed[site]]) if site in typed else C([reference[site]])
 return ts
Nforms=[('bottom_center',[5,6],'bottom'),('SW',[4,5],'bottom'),('right_center',[7,0],'right'),('NE',[0,1],'right')]
DRfull=full('D')|full('R');DRordinary=C(['D-','D+','R-','R+'])
CC={('L','B'):('L12','B6'),('L','E'):('L3','L3'),('L','Tc'):('L3','L3'),('B','E'):('E6','B6'),('B','Tc'):('T3','T3'),('E','Tc'):('E6','T12')}
OO={('L','B'):('L11','B11'),('L','E'):('LE9','13'),('L','Tc'):('L11','T11'),('B','E'):('E11','B11'),('B','Tc'):('sigma13','BT9'),('E','Tc'):('E11','T11')}
Nkeys=[]
for pair,keys in CC.items():
 for n,ss,side in Nforms:
  typed=dict.fromkeys(pair,'C');mi=shape(typed)|fan('N',ss);name='N_CC_'+'-'.join(pair)+'_'+n
  verify(name,P[keys[side=='right']],mi,mi|DRfull);Nkeys.append(name)
for pair,keys in OO.items():
 for n,ss,side in Nforms:
  typed=dict.fromkeys(pair,'O');mi=shape(typed)|fan('N',ss);name='N_OO_'+'-'.join(pair)+'_'+n
  verify(name,P[keys[side=='right']],mi,mi|DRfull);Nkeys.append(name)
CO={('L','E'):('L3','L3'),('L','Tc'):('L3','L3'),('L','B'):('L12','five'),('B','L'):('L11','B6'),('B','E'):('E11','B6'),('B','Tc'):('sigma13','B4')}
for (a,b),keys in CO.items():
 for n,ss,side in Nforms:
  typed={a:'C',b:'O'};mi=shape(typed)|fan('N',ss);path=P[keys[side=='right']];name='N_CO_'+a+b+'_'+n
  verify(name,path,mi,mi|DRfull);Nkeys.append(name)
  name='sigma_'+name;verify(name,sig(path),transform(mi),transform(mi|DRfull));Nkeys.append(name)
assert len(Nkeys)==96
# The retained nine path is the sole already-scoped term, no other archive data.
project=read('third-surplus-review/local-three-residue-project.json');assert len(project['terms'])==1
term=project['terms'][0];assert term['source_line']==800;P['nine']=decode(term['path'])
U9,Z9=g['path_requirements'](P['nine'])
assert U9=={tri(t) for t in term['required_triangles']} and Z9=={tri(t) for t in term['forbidden_triangles']}
assert fan('D',[3])&Z9
Nall=['Nb-','Nb+','Nr-','Nr+'];covered=set();inherited=[]
def patt(typed):return tuple(sorted(typed.items()))
def clause(name,typed,key,allowedN,fixedN=()):
 mi=shape(typed)|C(fixedN);ma=shape(typed)|C(allowedN)|DRordinary
 verify('three_'+name,P[key],mi,ma);verify('three_sigma_'+name,sig(P[key]),transform(mi),transform(ma))
 inherited.extend(['three_'+name,'three_sigma_'+name]);covered.add(patt(typed));covered.add(patt({siteflip[n]:t for n,t in typed.items()}))
# Each pair is exactly one dichotomy in proof section5.
families=[
 ('missL_allO',{'B':'O','E':'O','Tc':'O'},('BT9',['Nr-','Nr+'],()),('E11',['Nb-','Nb+'],())),
 ('missB_allO',{'L':'O','E':'O','Tc':'O'},('T11',['Nr-','Nr+'],()),('LE9',['Nb-','Nb+'],())),
 ('missB_EC',{'L':'O','E':'C','Tc':'O'},('sigma_B4',['Nb-','Nb+','Nr-'],()),('T11',['Nr+'],('Nr+',))),
 ('CL_BO_TO',{'L':'C','B':'O','Tc':'O'},('fiveTop3',['Nb-','Nr-','Nr+'],()),('L12',['Nb+'],('Nb+',))),
 ('missL_BC',{'B':'C','E':'O','Tc':'O'},('B4',['Nb+','Nr-','Nr+'],()),('E11',['Nb-'],('Nb-',))),
 ('missL_BC_EC',{'B':'C','E':'C','Tc':'O'},('B4',['Nb+','Nr-','Nr+'],()),('sigma_B6',['Nb-'],('Nb-',))),
 ('missL_EC',{'B':'O','E':'C','Tc':'O'},('sigma_B6',['Nb-','Nb+','Nr-'],()),('BT9',['Nr+'],('Nr+',))),
 ('CL_BO_EO',{'L':'C','B':'O','E':'O'},('five',['Nb-','Nr-','Nr+'],()),('L10',['Nb+'],('Nb+',))),
 ('CL_CE_BO',{'L':'C','E':'C','B':'O'},('five',['Nb-','Nr-','Nr+'],()),('nine',['Nb+'],('Nb+',))),
]
for name,typed,left,right in families:
 for side,(key,allowed,fixed) in enumerate([left,right]):clause(name+'_'+str(side),typed,key,allowed,fixed)
mi=H|fan('L',[7,0])|C(['B+']);ma=mi|full('E')|full('Tc')|full('N')|DRfull
verify('generic_L3',P['L3'],mi,ma);verify('generic_T3',sig(P['L3']),transform(mi),transform(ma));inherited+=['generic_L3','generic_T3']
for a,b in product('CO',repeat=2):
 typed={'L':'C','E':a,'Tc':b};covered.add(patt(typed));covered.add(patt({siteflip[n]:t for n,t in typed.items()}))
assert len(inherited)==38
budget=[]
for i,(typed,key) in enumerate([({'L':'O','E':'C','Tc':'C'},'sigma_B4'),({'B':'O','E':'C','Tc':'C'},'sigma_B6'),({'B':'C','E':'C','Tc':'C'},'sigma_B6')]):
 mi=shape(typed);ma=mi|DRordinary|C(['Nb-','Nb+','Nr-']);forbidden=mi|C(['Nr+'])
 assert single_angle(forbidden,(3,3))==180 and single_angle(forbidden,(1,3))==180
 assert all(x%2==y%2==1 for x,y in [(3,3),(1,3)])
 assert not any(point in t for t in DRordinary|C(['Nb-','Nb+','Nr-']) for point in [(3,3),(1,3)])
 for reflected in [False,True]:
  name='budget_'+str(i)+str(reflected)
  verify(name,sig(P[key]) if reflected else P[key],transform(mi) if reflected else mi,transform(ma) if reflected else ma)
  budget.append({'name':name,'distinct_unhealed_B_points':[list(sigma(p) if reflected else p) for p in [(3,3),(1,3)]],'b_if_blocker_present_at_least':2})
 covered.add(patt(typed));covered.add(patt({siteflip[n]:t for n,t in typed.items()}))
expected={patt(dict(zip(sites,types))) for sites in combinations(crit,3) for types in product('CO',repeat=3)}
assert covered==expected and len(covered)==32
# Actual-wall replay on the EXISTING fixed32-triangle minimum in the retained project.
minimum9={tri(t) for t in project['fixed_triangles']};V=polygon(minimum9)
geom=runpy.run_path(str(ROOT/'triangle-composition/inputs/illumination_geometry.py'))
report=geom['check']({'triangles':sorted(minimum9),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
assert set(map(tuple,report['interior_A']))=={(0,0),(2,0),(2,2)}
physical(P['nine'],V);physical(P['nine'][::-1],V);physical(sig(P['nine']),[sigma(p) for p in V])
assert U9<=minimum9 and not Z9&minimum9
negative={}
for name,bad in [('earlier_T',P['nine']+[P['nine'][0],P['nine'][-1]]),('off_wall',P['nine'][:1]+[(P['nine'][1][0]+F(1,100),P['nine'][1][1]+F(1,101))]+P['nine'][2:])]:
 try:physical(bad,V)
 except AssertionError:negative[name]='REJECTED'
 else:raise AssertionError(('corrupted path accepted',name))
# Reconstruct actual target lift from actual walls, rather than the discovery frame.
q=P['nine'][-1]
for p in reversed(P['nine'][1:-1]):
 walls=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on(p,a,b) and p not in [a,b]];assert len(walls)==1
 a,b=walls[0];e=sub(b,a);v=sub(q,a)
 q=tuple(a[k]+2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
assert cross(sub(P['nine'][1],P['nine'][0]),q)==0 and dot(sub(P['nine'][1],P['nine'][0]),q)>0
# Dependency hashes are recorded, not silently treated as fresh independent proofs.
sources=['surplus-four-local/three-unit-b1/argument.txt','surplus-four-local/three-unit-b1/check.json','surplus-four-local/two-unit.txt','third-surplus-review/path-support-check.json','third-surplus-review/local-three-residue-project.json','first-surplus-review/square-exchange-check.json']
out={'status':'EXACT_NAMED_CHECKS_PASS_HAND_VERDICT_SEPARATE','bound':13,'topology':topology,'remaining_boundary_junctions':junctions,'named_guards':checks,'N_unit_guards':len(Nkeys),'inherited_threecritical_guards':len(inherited),'new_b1_angle_exclusions':budget,'threecritical_patterns':len(covered),'retained9_negative_controls':negative,'retained9_actual_first_target_reverse_sigma':'PASS','retained9_unfolded_actual_target':[str(v) for v in q],'source_sha256':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in sources},'limits':'Independent agent reconstruction; retained physical/guard helpers share historical origins. No peer checker executed, discovery, cap assignment search, raw archive or new selected witness.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: independent topology,96 N guards,38 inherited/6 new guards,8 forcing,32 labels,actual-nine firstT/reverse/sigma')
