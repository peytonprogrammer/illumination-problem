"""Exact small necessary-condition probes; no dark polygon is asserted."""
from fractions import Fraction
from itertools import permutations,product
from math import gcd
from pathlib import Path
import json
OUT=Path(__file__).parent
# General strict triangle construction: each tile has exactly one labeled A,
# angle pi/n. Interior A consumes2n tiles; smooth A consumes n. Other vertex
# labels must be corners. Euler gives W=N-2I+2-sA. Hence W>=(1-1/n)N+2
# and N>=2nI, so I>=2 implies W>=4n-2.
# For the right-triangle subclass, each full A creates n smooth right-angle
# vertices. Each needs a third tile to become270 degrees; four would violate
# strictness. Two full stars cannot share such a right vertex. Therefore
# N>=3nI and W>=6n-4. All assumptions are edge-to-edge, simple disk, strict B/C.
angles=[]
for n in (4,6,8,10,12):
 minima={}
 for right in (False,True):
  best=None;best_row=None
  for I in range(2,9):
   for N in range(2*n*I,12*n*I+1):
    if right and N<3*n*I:continue
    for smooth in range((N-2*n*I)//n+1):
     W=N-2*I+2-smooth
     lower=(6*n-4) if right else (4*n-2)
     assert W>=lower
     if best is None or W<best:best,best_row=W,dict(I=I,N=N,smooth_A=smooth)
  assert best==((6*n-4) if right else (4*n-2))
  minima['right_triangle' if right else 'general_triangle']=dict(necessary_wall_lower_bound=best,relaxation_witness=best_row)
 angles.append(dict(n=n,**minima))
# Connected degree3 torus covers, branched only at the three nonzero2-torsion
# points, with every branch preimage ramified. This establishes a genuine
# abstract blocked-fiber template, not an actual billiard realization.
S3=list(permutations(range(3)));identity=tuple(range(3))
def compose(a,b):return tuple(a[b[i]] for i in range(3))
def inverse(a):return tuple(a.index(i) for i in range(3))
def cycles(a):
 seen=set();count=0
 for i in range(3):
  if i in seen:continue
  count+=1;j=i
  while j not in seen:seen.add(j);j=a[j]
 return count
three_cycles=[a for a in S3 if cycles(a)==1]
examples=[]
for h,v in product(S3,repeat=2):
 comm=compose(compose(compose(h,v),inverse(h)),inverse(v))
 for sigmas in product(three_cycles,repeat=3):
  p=comm
  for a in sigmas:p=compose(p,a)
  if p!=identity:continue
  reached={0};todo=[0]
  for i in todo:
   for a in (h,v)+sigmas:
    if a[i] not in reached:reached.add(a[i]);todo.append(a[i])
  assert len(reached)==3
  ramification=sum(3-cycles(a) for a in sigmas);assert ramification==6
  genus=1+Fraction(ramification,2);assert genus==4
  examples.append(dict(h=h,v=v,branch_cycles=sigmas,genus=int(genus)))
assert examples
parities={(a%2,b%2) for a in range(-31,32) for b in range(-31,32) if gcd(abs(a),abs(b))==1}
assert parities=={(0,1),(1,0),(1,1)}
# These three parity classes exhaust primitive torus return midpoints by the
# elementary gcd argument, not by the finite numerical check itself.
# If the origin is fixed by the full base dihedral action and p is equivariant,
# two distinct interior billiard marks require two free group orbits in its fiber.
fiber_gate=[dict(billiard_group=g,group_order=order,minimum_fiber_degree_for_two_interior_marks=2*order,degree3_passes=False) for g,order in [('orthogonal_D2',4),('45_degree_D4',8)]]
# Stronger conditional obstruction for the standard orthogonal quotient:
# corner images must be2-torsion; reflex corners unfold to local degree3,
# convex corners to degree1. Full ramification above the three nonzero classes
# forces d reflex corners there. If r0 more occur above0, c=d+r0+4 by the
# simple orthogonal disk angle sum, but its remaining regular fiber has only
# d-3r0 slots. Their difference4r0+4 is positive for every r0>=0.
for r0 in range(30):assert 4*r0+4>0
# The only non-right even-n strict triangle with n<8, apart from
# relabeling, has angles (1,1,4)*pi/6. A complete A star contributes
# two C sectors at every outer C vertex. Attaching a triangle along ANY
# boundary BC edge adds a third C sector: 3*(2*pi/3)=2*pi, forbidden
# because C must remain a genuine boundary corner. A full A star is thus
# a complete connected tile component. Two distinct interior A stars
# cannot occur in a connected strict label-preserving assembly.
strict_angles=[]
for n in (4,6):
 for m in range(1,n-1):
  a,b,c=Fraction(1,n),Fraction(m,n),Fraction(n-1-m,n)
  right=Fraction(1,2) in (a,b,c)
  sealed=3*max(b,c)>=2
  strict_angles.append(dict(n=n,m=m,angles_pi=[str(a),str(b),str(c)],right=right,
   full_A_star_sealed_under_strict_BC=sealed))
assert all(t['right'] or t['full_A_star_sealed_under_strict_BC'] for t in strict_angles)
# In the stated D2/D4-equivariant rectangular-torus setting, a corner's
# stabilizer contains the half-turn, so its base image is in T[2].
# A universal one-nth-time blocker scheme uses a coset of T[n], size n^2.
# This coset fits in T[2] only if n divides2. This is a no-go ONLY for
# demanding an entire universal blocker fiber, not selective sheet routing.
fraction_gate=[]
for n in range(2,9):
 torsion={(Fraction(i,n),Fraction(j,n)) for i in range(n) for j in range(n)}
 two_torsion={(Fraction(i,2),Fraction(j,2)) for i in range(2) for j in range(2)}
 fits=torsion<=two_torsion
 assert fits==(2%n==0)
 fraction_gate.append(dict(n=n,universal_base_blocker_count=len(torsion),
  in_two_torsion=len(torsion&two_torsion),all_fit_corner_positions=fits))
result=dict(status='PASS_NECESSARY_CONDITION_PROBES',universal_fractional_blocker_gate=fraction_gate,strict_triangle_bounds=angles,strict_low_n_triangle_cases=strict_angles,strict_obtuse_triangle_gate=dict(status='EXCLUDED_BY_LOCAL_FAN_ARGUMENT',angles_degrees=[30,30,120],outer_C_sector_before='4*pi/3',outer_C_sector_after_attachment='2*pi',reason='Every edge of a full A star is BC; any adjacent reflected tile makes C interior, violating strictness. A connected strict assembly cannot contain two full A stars.',scope='Label-preserving edge-to-edge reflected triangle assemblies, no transparent B/C vertices; not a bound for arbitrary triangles or exception-enabled constructions.'),degree3_torus_cover=dict(monodromy_solutions=len(examples),example=examples[0],genus=4,abstract_blocked_fiber=True,planar_room=False),primitive_midpoint_parity_classes=sorted(parities),equivariant_fiber_obstruction=fiber_gate,orthogonal_full_ramification_obstruction=dict(convex_corner_demand_minus_available_regular_origin_fiber='4*r0+4 > 0',scope='Equivariant standard rectangular-torus projection, simple orthogonal polygon, all three nonzero2-torsion fibers genuinely ramified; allowing absorbing removable regular corners escapes this particular no-go.'),scope='Analytic necessary-condition derivations plus exact finite combinatorial checks. No new dark room, polygon-realization proof, exhaustive geometry search.')
(OUT/'mechanism-probe.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('strict_triangle_bounds','degree3_torus_cover')}))
print(json.dumps(dict(angle_bounds=angles,torus_cover_solutions=len(examples))))
