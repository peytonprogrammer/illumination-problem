"""Independent fixed C1 controls using reviewer's earlier exact geometry functions.
No author checker imports/execution, no discovery. Pure functions are AST-selected
from the reviewer-owned checker to avoid rerunning or rewriting frozen outputs.
"""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib
R=Path(__file__).resolve().parent;A=R.parent/'construction'
source=R/'geometric-reduction-ear-monotonicity-check.py'
ns={'F':F,'S':(0,0),'T':(2,2)}
mod=ast.parse(source.read_text());pure=ast.Module(body=[node for node in mod.body if isinstance(node,ast.FunctionDef)],type_ignores=[])
exec(compile(pure,str(source),'exec'),ns)
D=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
filled=[(-1,-2)]+D[3:];pruned=D[:11]+[(4,0)]+D[14:]
results={};auth=json.loads((A/'geometric-reduction-check-01.json').read_text())
for name,p in [('known22',D),('C1_corner_filled',filled),('peer_ear_pruned',pruned)]:
 result=ns['analyze'](p);claimed=auth['rows'][name]
 assert list(map(list,p))==claimed['vertices']
 for ownkey,authorfield in [('walls','W'),('reflex','r'),('perimeter','boundary_lattice_count'),('J','J'),('s_N','s_N'),('k','k')]:assert result[ownkey]==claimed[authorfield]
 assert int(result['area'])==claimed['area']
 assert list(map(list,result['interior_points']))==claimed['interior_lattice_points']
 assert list(map(list,result['smooth_boundary_points']))==claimed['smooth_lattice_points']
 results[name]=result
# Full prescribed fill union certificate in rational vertical slabs.
vertical=ns['vertical_intervals']
slabs=[]
levels=sorted({x for x,y in filled+D})
for l,r in zip(levels,levels[1:]):
 x=F(l+r,2);a=vertical(D,x);b=vertical(filled,x)
 if -1<x<0:
  assert a==[(F(-1),F(1))] and b==[(F(-2),F(1))]
 else:assert a==b
 slabs.append(dict(x_interval=[l,r],D=[[str(y),str(z)] for y,z in a],filled=[[str(y),str(z)] for y,z in b]))
# C1 isolation: two new sides have no contact with old D except endpoints A,B.
newK=(-1,-2);oldA=(-1,-1);oldB=(0,-2)
for X,Y in [(oldA,newK),(newK,oldB)]:
 for a,b in ns['edges'](D):
  if ns['intersects'](X,Y,a,b):
   assert any(ns['on'](z,X,Y) and ns['on'](z,a,b) for z in [oldA,oldB])
   # Intersection cannot be a positive-length overlap; axial bounds overlap in at most a point.
   if X[0]==Y[0]==a[0]==b[0]:assert min(max(X[1],Y[1]),max(a[1],b[1]))==max(min(X[1],Y[1]),min(a[1],b[1]))
   if X[1]==Y[1]==a[1]==b[1]:assert min(max(X[0],Y[0]),max(a[0],b[0]))==max(min(X[0],Y[0]),min(a[0],b[0]))
# Author's different r4 availability control, independent all-pairs geometry and mark checks.
avail=auth['availability_control'];p=list(map(tuple,avail['polygon']));n=len(p)
for i,(a,b) in enumerate(ns['edges'](p)):
 assert a!=b and (a[0]==b[0] or a[1]==b[1])
 for j,(c,d) in enumerate(ns['edges'](p)):
  if j<=i or j in ((i-1)%n,(i+1)%n):continue
  assert not ns['intersects'](a,b,c,d)
turns=[ns['cross'](p[i-1],p[i],p[(i+1)%n]) for i in range(n)];assert all(turns)
assert sum(t<0 for t in turns)==avail['r']==4 and n==avail['W']==12
assert all(not(t<0 and turns[i-1]>0 and turns[(i+1)%n]>0) for i,t in enumerate(turns))
assert all(ns['classify'](p,tuple(mark))=='interior' for mark in avail['marks'])
for f,h in auth['source_sha256'].items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h
out={'status':'PASS_INDEPENDENT_PRESCRIBED_C1_REPLAY','rows':results,'fill_union_slabs':slabs,'isolation_new_sides_verified':True,'author_r4_availability_control_verified':True,'author_checker_executed':False,'author_source_sha256_snapshot':{name:hashlib.sha256((A/name).read_bytes()).hexdigest() for name in ['geometric-reduction-candidate-01.md','geometric-reduction-check-01.py','geometric-reduction-check-01.json','geometric-reduction-check-01.log']},'reviewer_pure_functions_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_is_frozen_review_packet':False,'r_le_8_optical_transfer':'OPEN','new_search_or_census':False,'whole_goal_complete':False}
(R/'geometric-reduction-c1-independent-replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','isolation_new_sides_verified','author_r4_availability_control_verified','r_le_8_optical_transfer']},indent=2))
