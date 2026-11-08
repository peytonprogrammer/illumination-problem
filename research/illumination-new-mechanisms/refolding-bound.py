"""Theory-only cone and automorphism audit. No trajectory code is invoked."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json
import hashlib
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from illumination_cover import build,inverse,then
from illumination_midpoint import vertex_data,components,translations,half_turns,inspect_turn

def cycles(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  c=[];j=i
  while j not in seen:seen.add(j);c.append(j);j=p[j]
  out.append(c)
 return out

def admissible_denominators(m,order):
 # Faithful derivative: the local rotation has the same order q as its
 # derivative. Thus gcd(m,q)=1, and the corner angle is pi*m/q.
 from math import gcd
 return [q for q in range(1,order//2+1) if order%(2*q)==0 and gcd(m,q)==1 and 0<F(m,q)<2 and m!=q]
records=[]
for filename in ('illumination-20.json','illumination-22.json','illumination-search-simple-unrestricted.json'):
 data=json.loads((ROOT.parent/filename).read_text());c=build(data);v=vertex_data(c)
 H,V=c['H'],c['V'];cc=cycles(then(then(then(inverse(H),inverse(V)),H),V))
 mult=Counter(len(z) for z in cc)
 dsu_mult=Counter(len(z)//4 for z in v['members'])
 assert all(len(z)%4==0 for z in v['members']) and mult==dsu_mult
 chi=len(v['members'])-len(H);assert (2-chi)%2==0;genus=(2-chi)//2
 assert sum((m-1)*n for m,n in mult.items())==2*genus-2
 colors=Counter(v['colors']);assert colors[1]==colors[2]==8
 ts=[len(translations(H,V,g)) for g in components(H,V)]
 assert len(ts)==1 and ts[0]==1
 blockers=Counter(len(v['members'][i])//4 for i,col in enumerate(v['colors']) if col==3)
 allowed=[d for d in(2,4,6,8) if d<=colors[1]]
 gates={str(d):{str(m):admissible_denominators(m,d) for m in sorted(blockers)} for d in allowed}
 impossible=[d for d in allowed if any(not admissible_denominators(m,d) for m in blockers)]
 turns=half_turns(H,V,components(H,V)[0]);assert len(turns)==1
 turn=inspect_turn(c,v,components(H,V)[0],turns[0])
 assert not turn['fixed_square_centers'] and not turn['fixed_edge_midpoints']
 fixed_indices=Counter(len(v['members'][i])//4 for i in turn['fixed_vertices'])
 fixed_mass=sum(m*n for m,n in fixed_indices.items())
 d4_wall_value=2+F(fixed_mass,4)
 if 8 not in impossible:
  assert fixed_mass%4==0
  assert sum(fixed_indices.values())==sum(blockers.values())
  assert fixed_indices==blockers
 simple=c['geometry']['simple_polygon'];walls=c['geometry']['walls']
 even_corners=None
 if simple:
  # For a genuine D4 simple polygon, angles k*pi/4 have k=1,2,3,5,6,7.
  # N_cone_lifts = W + number_of_90_or_270_corners.
  even_corners=sum(blockers.values())-walls
  assert 2*genus+6==3*walls-even_corners
 records.append(dict(input=filename,input_sha256=hashlib.sha256((ROOT.parent/filename).read_bytes()).hexdigest(),simple=simple,walls=walls,squares=len(H),genus=genus,cone_multiplicities=dict(sorted(mult.items())),absorbing_multiplicities=dict(sorted(blockers.items())),source_lifts=colors[1],target_lifts=colors[2],translation_automorphisms=ts[0],unique_half_turn_fixed_multiplicities=dict(sorted(fixed_indices.items())),fixed_cone_mass=fixed_mass,necessary_D4_simple_quotient_walls=str(d4_wall_value),candidate_group_orders_by_free_orbit_size=allowed,corner_denominator_gates=gates,orders_excluded_by_local_corner_gate=impossible,old_right_angle_corner_count=even_corners))
result=dict(status='PASS_CONE_AND_GROUP_NECESSARY_GATES',dependencies_sha256={name:hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest() for name in ('illumination_cover.py','illumination_midpoint.py','illumination_geometry.py')},records=records,scope='Exact gluings, cone multiplicities, derivative-I automorphisms and necessary local quotient constraints. No ray search; no finite-affine-action enumeration or new room.')
(ROOT/'refolding-bound.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
