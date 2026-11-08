"""Verify a hand local-fan table and six fixed-path failure modes.
No assembled-room/cap-assignment enumeration, optical discovery or solver.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util
import json
HERE=Path(__file__).resolve().parent
OWN=HERE.parent
spec=importlib.util.spec_from_file_location('exact_paths',OWN/'persisted-replay/audit.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
Fcenters={(0,0),(2,0),(2,2)}
external=sorted({(x+2*dx,y+2*dy) for x,y in Fcenters for dx,dy in ((1,0),(0,1),(-1,0),(0,-1))}-Fcenters)
assert len(external)==7
rays=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
side=((1,0),(0,1),(0,1),(-1,0),(-1,0),(0,-1),(0,-1),(1,0))
make_tri=lambda A,i:tuple(sorted((A,(A[0]+rays[i][0],A[1]+rays[i][1]),(A[0]+rays[(i+1)%8][0],A[1]+rays[(i+1)%8][1]))))
cap=lambda *p:tuple(sorted(p))
bridge={cap((0,2),(0,1),(1,1)),cap((0,2),(1,1),(1,2))}
critical={
 (-2,0):cap((-2,0),(-1,0),(-1,1)),
 (0,-2):cap((0,-2),(0,-1),(1,-1)),
 (4,2):cap((4,2),(3,1),(3,2)),
 (2,4):cap((2,4),(1,3),(2,3)),
}
ordinary=[];defects=[];zero_contact=0;direct=[]
for A in external:
 for m in range(1,8):
  q=3 if m==4 else m
  for start in range(8):
   inds=[(start+j)%8 for j in range(m)]
   touched=set(side[i] for i in inds)
   paid={s for s in touched if (A[0]+2*s[0],A[1]+2*s[1]) in Fcenters}
   d=len(paid);excess=q-d
   tris={make_tri(A,i) for i in inds}
   row={'A':A,'m':m,'start':start,'q':q,'d':d,'triangles':sorted(tris)}
   if excess==0:ordinary.append(row)
   if excess!=1:continue
   if d==0:
    assert m==1
    zero_contact+=1
    continue
   if A==(0,2) and bridge<=tris:
    direct.append(row)
    continue
   assert m==2 and d==1
   # The single full-facing side is fully covered only in the centered fan.
   full_side=next(iter(paid))
   centered=all(side[i]==full_side for i in inds)
   row['type']='centered' if centered else 'quarter'
   row['creates_interior_C']=centered
   defects.append(row)
assert len(ordinary)==17
assert sum(r['m']==1 for r in ordinary)==16
assert sum(r['m']==2 for r in ordinary)==1
assert len(direct)==5 and sorted(r['m'] for r in direct)==[3,3,4,4,4]
assert zero_contact==40
assert len(defects)==22
assert sum(r['A']!=(0,2) for r in defects)==18
assert sum(r['A']==(0,2) for r in defects)==4
active=[r for r in defects if r['A'] in critical and critical[r['A']] in {tuple(map(tuple,t)) for t in r['triangles']}]
assert len(active)==8
for A in critical:
 rows=[r for r in active if r['A']==A]
 assert len(rows)==2 and {r['type'] for r in rows}=={'centered','quarter'}

# Check the known already verified W17/k6 repair fixture. It contains a
# centered left-cell defect and invalidates all SIX zero-layer witnesses.
core=frozenset().union(*(a.incident(tuple(map(F,p))) for p in Fcenters))
reference_caps=frozenset(critical.values())
extra_left=cap((-2,0),(-1,-1),(-1,0))
repair=cap((2,-2),(1,-1),(2,-1))
fixture=core|reference_caps|{extra_left,repair}
old=json.loads((OWN/'exception-geometry/shared-extensions-check.json').read_text())['rooms']['A_left_repair']
assert old['ledger']['W']==17 and old['ledger']['k']==6
assert old['ledger']['Q']+old['ledger']['s_N']==9
paths=json.loads((OWN/'exception-geometry/zero-L-completion-check.json').read_text())['paths']
failures={}
for name,row in paths.items():
 path=tuple(tuple(F(*v) for v in pt) for pt in row['path'])
 need,z=a.path_requirements(path)
 assert need<=fixture and z&fixture
 failures[name]=sorted(z&fixture)
w=old['witness']
known_path=tuple(tuple(F(*v) for v in pt) for pt in w['path'])
need,z=a.path_requirements(known_path)
assert need<=fixture and not z&fixture
sigma=lambda p:(2-p[1],2-p[0])
fan_key=lambda r:tuple(sorted(tuple(map(tuple,t)) for t in r['triangles']))
active_keys={fan_key(r) for r in active}
assert all(tuple(sorted(tuple(sorted(sigma(v) for v in t)) for t in key)) in active_keys for key in active_keys)
orbits={min(key,tuple(sorted(tuple(sorted(sigma(v) for v in t)) for t in key))) for key in active_keys}
assert len(orbits)==4
from_old=lambda name:a.path_requirements(tuple(tuple(F(*v) for v in pt) for pt in paths[name]['path']))
_,z13=from_old('bottom_top_thirteen')
_,z13s=from_old('left_east_thirteen')
noncritical=[]
for r in defects:
 if r['A'] in critical:continue
 tris={tuple(map(tuple,t)) for t in r['triangles']}
 assert not (tris&z13 and tris&z13s)
 noncritical.append({'A':r['A'],'type':r['type'],'blocks_original':bool(tris&z13),'blocks_reflected':bool(tris&z13s)})
assert len(noncritical)==10

result={'status':'PASS','external_A_cells':external,
 'ordinary_zero_excess_fans':ordinary,
 'one_excess_zero_contact_options_excluded_by_connectivity':zero_contact,
 'one_excess_direct_bridge_fans':direct,
 'potentially_dark_one_excess_fans':defects,
 'remaining_active_cap_fans':active,'active_reflection_orbits':len(orbits),'noncritical_defect_static_cover':noncritical,
 'known_one_surplus_fixture':{'W':17,'k':6,'fan_site':[-2,0],'fan_type':'centered',
  'all_six_old_paths_invalidated':True,'old_path_failed_absences':failures,
  'existing_replacement_reflections':w['reflections'],'existing_replacement_source_line':w['source_line'],
  'replacement_exact_implication':'PASS'},
 'scope':'Only contiguous local fans at seven analytically forced external cells and one previously verified fixed fixture. All-room reduction and optical family coverage are hand arguments. No cap-assignment/room census or ray search.'}
(HERE/'local-fans.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','zero_excess_local_fans':len(ordinary),'one_excess_direct_bridge_fans':len(direct),
 'potentially_dark_one_excess_local_fans':len(defects),'remaining_active_cap_fans':len(active),
 'zero_contact_locals_excluded_by_hand_connectivity':zero_contact,
 'old_six_paths_cover_known_first_layer_fixture':False,'existing_replacement_reflections':w['reflections']},indent=2))
