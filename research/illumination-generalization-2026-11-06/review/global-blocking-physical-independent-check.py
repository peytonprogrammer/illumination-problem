"""Prescribed independent primitive map glue check and nine zero actions."""
from pathlib import Path
from fractions import Fraction as Q
import itertools,json,hashlib
R=Path(__file__).resolve().parent;data=json.loads((R/'global-blocking-check.json').read_text());G=list(itertools.product(range(3),repeat=3))
def F(i,x,y):a,b,_=G[i];return ((a+x)%3,(b+y)%3)
checks=0
for i in range(27):
 for t in [Q(0),Q(1,3),Q(1)]:
  assert F(i,Q(1),t)==F(data['r'][i],Q(0),t)
  assert F(i,t,Q(1))==F(data['u'][i],t,Q(0));checks+=2
branch=[]
for cyc in data['vertex_cycles']:
 images={F(i,0,0) for i in cyc};assert len(images)==1;branch.append(images.pop())
points=list(itertools.product(range(3),repeat=2));assert sorted(branch)==points
fibers={}
for i in range(27):fibers.setdefault(F(i,Q(1,2),Q(1,3)),[]).append(i)
assert len(fibers)==9 and {len(v) for v in fibers.values()}=={3}
rows=[]
for c in points:
 fixed=[w for w in points if tuple((c[i]-w[i])%3 for i in [0,1])==w];assert len(fixed)==1;rows.append({'translation':c,'fixed_zero_image':fixed[0]})
out={'status':'EXACT_PRIMITIVE_PERIOD_MAP_GLUE_AND_ALL_NEGATIONS_FIXED_ZERO_COUNTS_PASS','whole_goal_complete':False,'degree_to_unit_torus':27,'degree_to_primitive_torus':3,'primitive_lattice':'3Z²','edge_glue_controls':checks,'branch_values':branch,'regular_primitive_fiber_sizes':[len(v) for v in fibers.values()],'rows':rows,'new_general_rigidity_claimed':False,'prior_accepted_constraint':'torus-cover-bridge.md section3','source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['global-blocking-heisenberg.md','global-blocking-check.json','half-turn-quotient.md','half-turn-quotient-acceptance.json','torus-cover-bridge.md','torus-cover-bridge-acceptance.json']}}
(R/'global-blocking-physical-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256','branch_values','regular_primitive_fiber_sizes']})
