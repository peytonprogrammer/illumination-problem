"""Prescribed local pocket/temporary-seal algebra; no optical search."""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib
b=Path(__file__).resolve().parent

def D(t,z):return(z[1]+t,z[0]-t)
def H(t,z):return(z[0],4-2*t-z[1])
def V(z):return(2-z[0],z[1])
def R(z):return(4-z[0],z[1])
controls=[]
for t in [F(0),F(1,100),F(-1,100)]:
 for z in [(F(0),F(0)),(F(1),F(3,2)),(F(3),F(-2))]:
  actual=D(t,H(t,D(t,z)))
  assert actual==R(z)
  assert tuple(actual[i]-V(z)[i] for i in (0,1))==(2,0)
  controls.append({'t':str(t),'z':list(map(str,z)),'DHD':list(map(str,actual))})
returns=[]
for m in [F(1,8),F(-1,8)]:
 y=F(3,2); yp=y+2*m
 assert 1<yp<2 and m!=2-y
 # The already proved DHD branch: unfolded and refolded exit.
 developed=(F(3),yp)
 assert D(0,H(0,D(0,developed)))==(1,yp)
 assert yp!=y
 returns.append({'entry_y':str(y),'slope':str(m),'exit_y':str(yp),'sealed_y':str(y)})
# A prescribed two-factor affine composition with unequal prefixes.
def plus(x,y):return tuple(x[i]+y[i] for i in (0,1))
def rot(z):return(-z[1],z[0])
z=(F(5),F(7))
old=V(rot(V(z)))
new=R(rot(R(z)))
# Read composition from the source development: outer prefix I, inner prefix V*rot.
first=(2,0)
second=(-rot((2,0))[0],rot((2,0))[1])
assert tuple(new[i]-old[i] for i in (0,1))==plus(first,second)
# Mandatory full-star control for the forbidden diagonal source/target pair.
sfull={(x,y) for x in (-1,0) for y in (-1,0)}
tfull={(x,y) for x in (-1,0) for y in (1,2)}
c_neighborhood={(x,y) for x in (-1,0) for y in (0,1)}
assert c_neighborhood <= sfull | tfull
assert (0%2,1%2)!=(0,0)
# Bind the inherited theorem, without replaying its solvers or rays.
root=b.parents[2]
receipt=root/'.context/three-triples/three-exception-complete.json'
prior=json.loads(receipt.read_text())
assert prior['status']=='EXCLUDED_BELOW_24'
assert prior['attained_minimum_walls']==24
assert prior['at_most_transparent_BC_vertices']==3
assert prior['remaining_placements']==[]
corollary={'wall_change':-3,'transparent_BC_after_sealing':2,'raw_wall_upper_bound':26,'sealed_wall_upper_bound':23,
          'prior_receipt':str(receipt),'prior_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest(),
          'dependency':'Inherited computer-assisted k<=3 exclusion; no new solver or optical replay.',
          'diagonal_full_star_control':{'source':[0,0],'target':[0,2],'forced_interior_C':[0,1],
                                        'four_incident_unit_cells':sorted(c_neighborhood)},
          'inherited_smooth_boundary_scope':prior['scope'],
          'wall_count_definition_source':str(root/'.context/claude-illumination-check/claude_relaxed_replay.py'),
          'wall_count_definition_sha256':hashlib.sha256((root/'.context/claude-illumination-check/claude_relaxed_replay.py').read_bytes()).hexdigest(),
          'wall_count_definition_observed':'vertex_table assigns corner=0 to smooth angle180; replay sums corner indicators.',
          'open_portal_avoidance':'UNPROVED','universal_goal':'OPEN'}
out={'status':'PRESCRIBED_PORTAL_ALGEBRA_PASS','DHD_controls':controls,'local_return_controls':returns,
'composition_control':{'old':list(map(str,old)),'new':list(map(str,new)),'difference':list(map(str,plus(first,second)))},
'bounded_core_corollary':corollary,
'scope':'One mandatory-star cell control and inherited theorem binding, plus nine fixed affine evaluations, two prescribed local return formulas and one fixed composition identity. No room, ray, direction, event-word or orbit discovery.',
'portal_avoiding_existence':'UNRESOLVED','universal_one_corner_goal':'OPEN'}
(b/'pocket-portal.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
