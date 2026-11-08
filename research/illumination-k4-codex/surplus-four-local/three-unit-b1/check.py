"""Fixed support checks for three local excess-one cells with b=1."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
import ast,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
# Reuse only retained OWN pure helpers and pinned data construction.
# The old check body and all old receipt writes are deliberately not executed.
helper=ROOT/'surplus-four-local/mixed-allroots-review/check.py'
text=helper.read_text()
exec(compile(text[:text.index('# Local D-root deletion identities')],str(helper),'exec'),globals())
functions=[n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name in ['contains','intersect','angle_info','guard']]
exec(compile(ast.Module(body=functions,type_ignores=[]),str(helper),'exec'),globals())
start=text.index('# Check pinned existing path coordinates');end=text.index('# Only the two N fans')
exec(compile(text[start:end],str(helper),'exec'),globals())
paths['T12']=sigpath(paths['L12']);paths['B4']=paths['B6T4']
old=read('third-surplus-review/local-three-unit-check.json')
for n in ['fiveTop3','L10']:
 paths[n]=[tuple(F(*v) for v in p) for p in old['new_paths'][n]]
assert paths['BT9']==[tuple(F(*v) for v in p) for p in old['new_paths']['BT9']]
assert paths['B4']==[tuple(F(*v) for v in p) for p in old['new_paths']['B4']]
for n,P in list(paths.items()):paths['sigma_'+n]=sigpath(P)

# Short D root deletion and active D single-leaf deletion.
Bpossible=fan('B',[0,1,2,3]);Rpossible=fan('R',[2,3,4,5])
far=set().union(*(full(n) for n in ['L','E','Tc','N']))
maximum_rest=H|Bpossible|Rpossible|far
topology=[]
for ss in [[0,1],[1,2],[2,3]]:
 tiles=fan('D',ss);arc=[]
 if 1 in ss:arc.append(((2,-1),(3,-1)))
 if 2 in ss:arc.append(((1,-1),(2,-1)))
 if 3 in ss:assert 2 in ss;arc.append(((1,-2),(1,-1)))
 if 0 in ss:assert 1 in ss
 for a in tiles:
  for b in maximum_rest:
   pts=intersect(a,b);assert all(any(on(p,*e) for e in arc) for p in pts),(ss,a,b,pts)
 for a,b in arc:
  assert any(contains(a,t) and contains(b,t) for t in tiles)
  assert any(contains(a,t) and contains(b,t) for t in maximum_rest)
 topology.append({'D_root_sectors':ss,'maximum_attach_arc':arc,'status':'PASS'})
leaf=fan('D',[3]);attach=((1,-1),(1,-2));rest=H|fan('B',[0,1])|Rpossible|far
for a in leaf:
 for b in rest:assert all(on(p,*attach) for p in intersect(a,b))
assert angle_info(H|fan('B',[0,1])|leaf,(1,-2))==([180],False)
assert angle_info(H|fan('B',[0,1]),(1,-2))==([90],False)
assert angle_info(H|fan('B',[0,1])|leaf,(1,-1))==([315],False)
assert angle_info(H|fan('B',[0,1]),(1,-1))==([270],False)
topology.append({'D_leaf_sectors':[3],'attach_arc':[attach],'status':'PASS'})

# Universal forcing is unchanged by the third unit or b=1.
allK=H|set().union(*(full(n) for n in centers));forcing=[]
spec=[('Bplus','one',H,allK-C(['B+'])),
 ('Tminus_ordinaryB','four',H|C(['B+']),(allK-full('B')-C(['T-']))|C(['B+'])),
 ('Tminus_centerB','centerB3',H|fan('B',[1,2]),(allK-full('B')-C(['T-']))|fan('B',[1,2])),
 ('Tminus_outerB','outerB2',H|fan('B',[0,1]),(allK-full('B')-C(['T-']))|fan('B',[0,1]))]
for name,key,mi,ma in spec:
 for reflected in [False,True]:
  nn=('sigma_' if reflected else '')+name
  forcing.append({'name':nn,**guard(sigpath(paths[key]) if reflected else paths[key],tr(mi) if reflected else mi,tr(ma) if reflected else ma,nn)})

critical=['L','B','E','Tc'];reference={'L':'L+','B':'B+','E':'E-','Tc':'T-'}
forms={'L':{'C':[7,0],'O':[0,1]},'B':{'C':[1,2],'O':[0,1]},
 'E':{'C':[3,4],'O':[4,5]},'Tc':{'C':[5,6],'O':[4,5]}}
site_sigma={'L':'Tc','Tc':'L','B':'E','E':'B'}
BDR=full('D')|full('R')
Nunits={'bottom_center':([5,6],'bottom'),'SW':([4,5],'bottom'),
 'right_center':([7,0],'right'),'NE':([0,1],'right')}
Nrows=[]
def Nclause(name,typed,nname,P):
 ss,side=Nunits[nname];mi=H|fan('N',ss)
 for site in critical:mi|=fan(site,forms[site][typed[site]]) if site in typed else C([reference[site]])
 row=guard(P,mi,mi|BDR,name)
 Nrows.append({'name':name,'critical_units':typed,'N_unit':nname,**row})
for a,b in combinations(critical,2):
 for nname,(ss,side) in Nunits.items():
  # Both centered: the formerly b0-excluded pairs use the budget-free fallback.
  if (a,b)==('L','B'):key='L12' if side=='bottom' else 'B6'
  elif (a,b)==('E','Tc'):key='E6' if side=='bottom' else 'T12'
  elif a=='L':key='L3'
  elif b=='Tc':key='T3'
  else:key='E6' if side=='bottom' else 'B6'
  Nclause('CC_'+a+b+'_'+nname,{a:'C',b:'C'},nname,paths[key])
  typed={a:'O',b:'O'}
  if side=='right':key='BT9' if 'B' in typed and 'Tc' in typed else ('B11' if 'B' in typed else ('T11' if 'Tc' in typed else '13'))
  else:key='LE9' if 'L' in typed and 'E' in typed else ('L11' if 'L' in typed else ('E11' if 'E' in typed else 'sigma13'))
  Nclause('OO_'+a+b+'_'+nname,typed,nname,paths[key])
reps=[('L','E',['L3','L3']),('L','Tc',['L3','L3']),('L','B',['L12','five']),
 ('B','L',['L11','B6']),('B','E',['E11','B6']),('B','Tc',['sigma13','B6T4'])]
for center,outer,keys in reps:
 for nname,(ss,side) in Nunits.items():
  P=paths[keys[0 if side=='bottom' else 1]];typed={center:'C',outer:'O'}
  Nclause('CO_'+center+outer+'_'+nname,typed,nname,P)
  reflected={site_sigma[k]:v for k,v in typed.items()}
  transformed=tr(fan('N',ss))
  partner=next(n for n,(sectors,_) in Nunits.items() if fan('N',sectors)==transformed)
  Nclause('CO_sigma_'+center+outer+'_'+nname,reflected,partner,sigpath(P))
assert len(Nrows)==96 and max(r['reflections'] for r in Nrows)<=13

# Three critical sites: exact inherited clauses, not a cap-assignment scan.
Ncaps=['Nb-','Nb+','Nr-','Nr+'];DRordinary=C(['D-','D+','R-','R+'])
shapes={
 'missL_allO':{'B':'O','E':'O','Tc':'O'},'missB_allO':{'L':'O','E':'O','Tc':'O'},
 'missB_EC':{'L':'O','E':'C','Tc':'O'},'centerL_Bouter_Touter':{'L':'C','B':'O','Tc':'O'},
 'missL_BC':{'B':'C','E':'O','Tc':'O'},'missL_BC_EC':{'B':'C','E':'C','Tc':'O'},
 'missL_EC':{'B':'O','E':'C','Tc':'O'},'centerL_Bouter_Eouter':{'L':'C','B':'O','E':'O'},
 'centerL_centerE_Bouter':{'L':'C','E':'C','B':'O'}}
def critical_support(typed):
 mi=H.copy()
 for site in critical:mi|=fan(site,forms[site][typed[site]]) if site in typed else C([reference[site]])
 return mi
oldrows=[];covered=set()
def pattern(typed):return tuple(sorted(typed.items()))
def oldclause(name,typed,P,mi,ma):
 oldrows.append({'name':name,'critical_units':typed,**guard(P,mi,ma,name)})
 oldrows.append({'name':'sigma_'+name,'critical_units':{site_sigma[k]:v for k,v in typed.items()},**guard(sigpath(P),tr(mi),tr(ma),'sigma_'+name)})
 covered.add(pattern(typed));covered.add(pattern({site_sigma[k]:v for k,v in typed.items()}))
for name,r in old['cases'].items():
 if 'shape' not in r:continue
 typed=shapes[r['shape']];mi=critical_support(typed)
 ma=mi|DRordinary|C([n for n in Ncaps if n not in r['absent_N']])
 oldclause(name,typed,paths[r['path']],mi,ma)
# Missing B with L centered permits arbitrary E/T C/O additions.
mi=H|fan('L',[7,0])|C(['B+'])
ma=mi|full('E')|full('Tc')|full('N')|BDR
oldrows.append({'name':'Lcenter_missingB_generic',**guard(paths['L3'],mi,ma,'Lcenter_generic')})
oldrows.append({'name':'sigma_Lcenter_missingB_generic',**guard(sigpath(paths['L3']),tr(mi),tr(ma),'sigma_Lcenter_generic')})
for e,t in product('CO',repeat=2):
 typed={'L':'C','E':e,'Tc':t};covered.add(pattern(typed));covered.add(pattern({site_sigma[k]:v for k,v in typed.items()}))
# EXACT retained finite9 witness only; no access to its raw archive.
project=read('third-surplus-review/local-three-residue-project.json')
assert len(project['terms'])==1;term=project['terms'][0];assert term['source_line']==800
P9=[tuple(F(*v) for v in p) for p in term['path']]
assert len(P9)-2==9 and P9[0]==(0,0) and P9[-1]==(2,2)
U9,Z9=path_requirements(P9)
assert U9==set(map(tri,term['required_triangles'])) and Z9==set(map(tri,term['forbidden_triangles']))
for a,b in zip(P9[:-2],P9[1:-1]):assert not on((2,2),a,b)
typed=shapes['centerL_centerE_Bouter'];mi=critical_support(typed)|C(['Nb+'])
ma=mi|DRordinary
oldclause('retained_nine_Nbplus',typed,P9,mi,ma)
assert len(oldrows)==38

# New b1 cases: E/T centered already use the ONE permitted smooth B.
# Ordinary Nr+ would create a second unhealed smooth B, hence is absent.
newrows=[];budget_angles=[]
new_patterns=[({'L':'O','E':'C','Tc':'C'},'sigma_B4'),
 ({'B':'O','E':'C','Tc':'C'},'sigma_B6'),({'B':'C','E':'C','Tc':'C'},'sigma_B6')]
for i,(typed,key) in enumerate(new_patterns):
 mi=critical_support(typed);ma=mi|DRordinary|C([n for n in Ncaps if n!='Nr+'])
 with_forbidden=mi|C(['Nr+'])
 assert angle_info(with_forbidden,(3,3))==([180],False)
 assert angle_info(with_forbidden,(1,3))==([180],False)
 assert not any(p in t for t in DRordinary for p in [(3,3),(1,3)])
 for reflect in [False,True]:
  pp=sigpath(paths[key]) if reflect else paths[key];mm=tr(mi) if reflect else mi;xx=tr(ma) if reflect else ma
  nn=('sigma_' if reflect else '')+'new_center_pair_'+str(i)
  newrows.append({'name':nn,**guard(pp,mm,xx,nn)})
  budget_angles.append({'name':nn,'two_distinct_smooth_B_points':[[*sigma(p)] for p in [(3,3),(1,3)]] if reflect else [[3,3],[1,3]],'b_lower_bound_if_blocking_cap_present':2})
 covered.add(pattern(typed));covered.add(pattern({site_sigma[k]:v for k,v in typed.items()}))
assert len(newrows)==6
expected={pattern(dict(zip(sites,forms_tuple))) for sites in combinations(critical,3) for forms_tuple in product('CO',repeat=3)}
assert covered==expected and len(covered)==32

out={'status':'PARENT_THREE_E1_B1_PARTITION_CLOSED_PENDING_PEER_REVIEW','reflection_bound':13,
 'short_D_topology':topology,'N_unit_pair_guard_count':len(Nrows),'N_unit_pair_guards':Nrows,
 'reference_forcing':forcing,'inherited_three_critical_guards':oldrows,
 'new_b1_center_pair_guards':newrows,'new_b1_budget_angles':budget_angles,
 'three_critical_CO_patterns_covered':len(covered),
 'retained_nine_provenance':{'project':'third-surplus-review/local-three-residue-project.json','source_line':800,'raw_archive_read':False},
 'input_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in [
  'surplus-four-local/mixed-allroots-review/check.py','surplus-four-local/mixed-leaf-review/check.json',
  'third-surplus-review/local-three-unit.txt','third-surplus-review/local-three-unit-check.json',
  'third-surplus-review/local-three-residue-project.json','surplus-four-local/two-unit.txt']},
 'limits':'Only named inherited paths and declared local templates; no room/cap assignment discovery, new direction/word scan, orbit run or raw archive access. Geometry completeness and b1 exclusions are hand proof in argument.txt. New theorem needs independent peer challenge.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('4localdeletiontemplates;96Nunitguards;38inherited+6newthreecriticalguards;8forcing;32C/O patterns PASS.')
