"""Named fixed guard and local fan checks: two positives e2/e1 with b1."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
helper=ROOT/'surplus-four-local/mixed-allroots-review/check.py';s=helper.read_text()
exec(compile(s[:s.index('# Local D-root deletion identities')],str(helper),'exec'),globals())
funcs=[n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name in ['guard','angle_info']]
exec(compile(ast.Module(body=funcs,type_ignores=[]),str(helper),'exec'),globals())
exec(compile(s[s.index('# Check pinned existing path coordinates'):s.index('# Only the two N fans')],str(helper),'exec'),globals())
# Only 8 explicit N root windows; m4 has q3, not q4.
Nforms={'right012':[0,1,2],'bottom345':[3,4,5],'bottom456':[4,5,6],
 'right701':[7,0,1],'right0123':[0,1,2,3],'bottom2345':[2,3,4,5],
 'bottom3456':[3,4,5,6],'right7012':[7,0,1,2]}
windows=[];survive=[]
for m in [3,4]:
 for st in range(8):
  ss={(st+i)%8 for i in range(m)};bridge={6,7}<=ss
  touched=int(bool(ss&{5,6}))+int(bool(ss&{7,0}))
  if touched==1 and not bridge:survive.append(frozenset(ss))
  windows.append({'m':m,'start':st,'H_sides_touched':touched,'bridge':bridge})
assert set(survive)=={frozenset(v) for v in Nforms.values()} and len(survive)==8
critical=['L','B','E','Tc'];reference={'L':'L+','B':'B+','E':'E-','Tc':'T-'}
forms={'L':{'C':[7,0],'O':[0,1]},'B':{'C':[1,2],'O':[0,1]},
 'E':{'C':[3,4],'O':[4,5]},'Tc':{'C':[5,6],'O':[4,5]}}
DR=full('D')|full('R');Nchecks=[]
for name,ss in Nforms.items():
 bottom=name.startswith('bottom');nfan=fan('N',ss)
 for site in critical:
  for typ in ['C','O']:
   mi=H|nfan|fan(site,forms[site][typ])|C([reference[k] for k in critical if k!=site])
   if typ=='C':key={'L':'L3','B':'sigma13' if bottom else 'B6','E':'E6' if bottom else '13','Tc':'T3'}[site]
   else:key={'L':'L11' if bottom else '13','B':'sigma13' if 6 in ss else 'five','E':'E11' if bottom else '13','Tc':'sigma13' if bottom else 'T11'}[site]
   label=name+'_'+site+typ;Nchecks.append({'name':label,'selected_path':key,**guard(paths[key],mi,mi|DR,label)})
 mi=H|nfan|C(list(reference.values()));key='sigma13' if bottom else '13'
 Nchecks.append({'name':name+'_noncritical','selected_path':key,**guard(paths[key],mi,mi|DR,name+'_noncritical')})
assert len(Nchecks)==72 and max(c['reflections'] for c in Nchecks)<=13
# Existing forcing implications permit all other K triangles.
allK=H|set().union(*(full(n) for n in centers));forcing=[]
spec=[('Bplus','one',H,allK-C(['B+'])),
 ('Tminus_ordinaryB','four',H|C(['B+']),(allK-full('B')-C(['T-']))|C(['B+'])),
 ('Tminus_centerB','centerB3',H|fan('B',[1,2]),(allK-full('B')-C(['T-']))|fan('B',[1,2])),
 ('Tminus_outerB','outerB2',H|fan('B',[0,1]),(allK-full('B')-C(['T-']))|fan('B',[0,1]))]
for name,key,mi,ma in spec:
 for reflected in [False,True]:
  label=('sigma_' if reflected else '')+name
  forcing.append({'name':label,**guard(sigpath(paths[key]) if reflected else paths[key],tr(mi) if reflected else mi,tr(ma) if reflected else ma,label)})
# Active Beast root +single Dleaf or Droot, ordinary L/E/T slots.
beast=H|fan('B',[0,1,2])|C(['L+','E-','T-']);pairguards=[]
for label,key,mi,ma in [
 ('Beast_without_Nbplus','five',beast,beast|DR|(full('N')-C(['Nb+']))),
 ('Beast_with_Nbplus','sigma13',beast|C(['Nb+']),beast|DR|fan('N',[4,5,6]))]:
 pairguards.append({'name':label,**guard(paths[key],mi,ma,label)})
# Three joined B-root windows, either single D leaf: ONLY named local templates.
uniform7=[tuple(map(F,p)) for p in read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path']]
rows=[];angle_coefficients={}
for label,ss,h in [('O3',[7,0,1],0),('O4',[6,7,0,1],0),('H4',[7,0,1,2],1)]:
 for leaf in [3,4]:
  fixed=H|fan('B',ss)|fan('D',[leaf]);mi=fixed|C(['L+','E-'])
  ordinary=['T-','T+','R-','R+','Nb-','Nb+','Nr-','Nr+']
  ma=mi|C([n for n in ordinary if n!='Nr-'])
  key=label+'_D'+str(leaf);rows.append({'name':key,**guard(uniform7,mi,ma,key)})
  assert angle_info(fixed,(1,-2))==([270],False)
  assert angle_info(fixed,(1,-1))==([315 if leaf==3 else 270],False)
  # Angular coefficient table, not completed-cap choices or room generation.
  base=mi;points=sorted({p for t in base|C(ordinary) for p in t if p[0]%2==p[1]%2==1})
  coeff={}
  for p in points:
   constant=sum(45 for t in base if p in t)
   variables={n:45 for n in ordinary if p in caps[n]}
   coeff[str(p)]={'fixed_degrees':constant,'ordinary_cap_degrees':variables}
  assert coeff[str((-1,1))]=={'fixed_degrees':135,'ordinary_cap_degrees':{'Nb-':45}}
  assert coeff[str((1,3))]=={'fixed_degrees':90,'ordinary_cap_degrees':{'T-':45,'Nr+':45}}
  for point,values in coeff.items():
   if point not in [str((-1,1)),str((1,3))]:
    fixed_angle=values['fixed_degrees'];largest=fixed_angle+sum(values['ordinary_cap_degrees'].values())
    assert fixed_angle>=225 or largest<180,(key,point,values)
  angle_coefficients[key]=coeff
# Beast single leaf has smooth outside C; rectangle plus leaf adds a SECOND B.
assert angle_info(H|fan('B',[0,1,2])|fan('D',[3]),(1,-2))==([180],False)
for p in [(1,-2),(-1,-1)]:
 assert angle_info(H|fan('B',[0,1,2,3])|fan('D',[3])|C(['L+']),p)==([180],False)
# Opposite-root B leaf omits B+; one works even with all other K support.
pairguards.append({'name':'B_leaf_missing_Bplus',**guard(paths['one'],H,allK-C(['B+']),'B_leaf_one')})
# Reuse exact already accepted deletion/support dependencies without rerunning them.
Dprior=read('surplus-four-local/mixed-allroots-review/check.json')
leafprior=read('surplus-four-local/mixed-leaf-review/check.json')
assert Dprior['status']=='INDEPENDENT_D_R_TOPOLOGY_AND_N_ROOT_DISPATCH_CHECKS_PASS'
assert len(Dprior['D_root_local_windows'])==9
assert leafprior['pinned_catalog_paths']==21 and leafprior['supplementary_fixed_compositions']==2
assert all(v['complete_U_Z_avoids_D_R'] for v in leafprior['path_checks'].values())
out={'status':'PARENT_E2_E1_B1_ROOT_LEAF_AND_NONCRITICAL_E2_COVERS_CHECKS_PASS','reflection_bound_for_closed_subfamilies':13,
 'N_e2_local_windows':windows,'eight_N_root_forms':Nforms,'N_whole_family_guards':Nchecks,
 'reference_forcing':forcing,'Beast_and_opposite_leaf_guards':pairguards,'six_joined_B_leaf_uniform7_guards':rows,
 'joined_leaf_B_angle_coefficients':angle_coefficients,'joined_leaf_b_formula':'indicator(Nb-)+indicator(Nr+)*indicator(T-)',
 'dependencies':{'one_unit_budget_free':'second-surplus-L/classification.txt section4',
 'D_R_legal_deletion':'mixed-allroots-review/review.txt; same 9 local windows, one remaining root',
 'e2_leaf_deletion':'mixed-leaf-review/review.txt; same D34 flap, one remaining root',
 'complete_support':'mixed-leaf-review/check.json; 21 catalog plus 2 fixed compositions'},
 'input_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in [
 'surplus-four-local/mixed-allroots-review/check.py','surplus-four-local/mixed-allroots-review/check.json',
 'surplus-four-local/mixed-leaf-review/check.json','second-surplus-L/classification.txt',
 'surplus-four-local/single-e2-check.json']},
 'limits':'Hand root/leaf completeness, b formula and legal deletion applicability in argument.txt; new whole covers need peer challenge. Critical e2 roots L/B/E/T with a second ROOT remain unresolved. No new completed room/cap scan, path discovery, archive, solver, orbit or workers.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status']);print('72Nguards+8forcing+3pairguards+6joinedleafguards PASS; critical e2 roots remain.')
