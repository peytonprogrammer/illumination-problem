"""Independent fixed-support and local deletion checks for e2-leaf inheritance."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
from boundary_replay import cross,sub,dot,on
import illumination_geometry as g
tri=lambda t:tuple(sorted(map(tuple,t)))
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(c,ss):
 return {tri((c,(c[0]+dirs[i%8][0],c[1]+dirs[i%8][1]),(c[0]+dirs[(i+1)%8][0],c[1]+dirs[(i+1)%8][1]))) for i in ss}
H=set().union(*(fan(c,range(8)) for c in [(0,0),(2,0),(2,2)]))
B=fan((0,-2),[0,1]);leaf=fan((2,-2),[3,4]);attach=((1,-1),(1,-2))
assert leaf=={tri(((2,-2),(1,-1),(1,-2))),tri(((2,-2),(1,-2),(1,-3)))}
other_centers=[(-2,0),(4,2),(2,4),(4,0),(0,2)]
others=set().union(*(fan(c,range(8)) for c in other_centers))
maximum_rest=H|B|others

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

intersection=set();other_intersections=[]
for a in leaf:
 for b in maximum_rest:
  points=intersect(a,b)
  assert all(on(p,*attach) for p in points),('extra leaf contact',a,b,points)
  intersection|=points
  if b in others and points:other_intersections.append((a,b))
assert not other_intersections and set(attach)<=intersection
# One common edge is fully present on both closed sides, so the union
# intersection is the entire attaching segment, not just sampled points.
assert any(all(contains(p,a) for p in attach) for a in leaf)
assert any(all(contains(p,b) for p in attach) for b in B)
local={}
for name,tiles in [('erased_H_B',H|B),('attached_H_B_D',H|B|leaf)]:
 geo=g.check({'triangles':sorted(tiles),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
 assert geo['simple_polygon'] and set(geo['interior_A'])=={(0,0),(2,0),(2,2)}
 owners=g.owners_of(list(tiles));opens={e for e,ls in owners.items() if len(ls)==2}
 angles={}
 for p in attach:
  aa,full=g.check_fan_angles(list(tiles),p,owners,opens)
  assert len(aa)==1 and not full;angles[str(p)]=45*aa[0]
 local[name]={'simple_fullSUT':'PASS','angles':angles,'triangles':len(tiles)}
assert local['attached_H_B_D']['angles']=={'(1, -1)':315,'(1, -2)':270}
assert local['erased_H_B']['angles']=={'(1, -1)':270,'(1, -2)':90}

catalog_path=ROOT/'third-surplus-review/path-support-check.json'
catalog=json.loads(catalog_path.read_text());paths={};hashes={}
for source,pinned in catalog['sources'].items():
 raw=(ROOT/source).read_bytes();hashes[source]=hashlib.sha256(raw).hexdigest()
 assert hashes[source]==pinned,('catalog drift',source)
 data=json.loads(raw)
 if 'forcing_paths' in data:records={n:r['path'] for n,r in data['forcing_paths'].items()}
 elif 'paths' in data:records={n:r['path'] for n,r in data['paths'].items()}
 else:records={None:data.get('path',data.get('five_path'))}
 for name,rawpath in records.items():
  key=source+(':'+name if name is not None else '')
  paths[key]=[tuple(F(*v) for v in p) for p in rawpath]
assert set(paths)==set(catalog['paths']) and len(paths)==21

def owner(t):
 centers=[p for p in t if p[0]%2==p[1]%2==0]
 assert len(centers)==1;return centers[0]
sigma=lambda p:(2-p[1],2-p[0])
transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}
rows={}

def check_path(name,P):
 assert P[0]==(0,0) and P[-1]==(2,2)
 U,Z=path_requirements(P)
 assert not {owner(t) for t in U|Z}&{(2,-2),(4,0)},name
 Us,Zs=path_requirements([sigma(p) for p in P[::-1]])
 assert Us==transform(U) and Zs==transform(Z)
 assert not {owner(t) for t in Us|Zs}&{(2,-2),(4,0)}
 rows[name]={'status':'PASS','reflections':len(P)-2,'complete_U_Z_avoids_D_R':True,'sigma':'PASS'}
 return U,Z
for name,P in paths.items():check_path(name,P)
old=paths['zero-surplus-L/cover-check.json:thirteen']
double=old[:8]+[(F(6,11),F(-2)),(F(18,11),F(4))]+old[14:]
assert len(double)-2==9
check_path('fixed_double_B_T_square_exchange',double)
b6=paths['first-surplus-review/bottom-residual-check.json']
top=b6[:4]+[(F(5,3),F(4))]+b6[7:]
assert len(top)-2==4
check_path('fixed_Bcenter6_Tsquare_exchange',top)
# Opposite root/leaf orientation: B leaf omits B+, so this one-path
# survives even the maximal possible support of every other K cell.
caps=json.loads((ROOT/'triangle-composition/inputs/caps.json').read_text())['cap_options']
allK=H|set().union(*(fan(c,range(8)) for c in [(-2,0),(0,-2),(2,-2),(4,0),(4,2),(2,4),(0,2)]))
U,Z=path_requirements(paths['zero-surplus-L/cover-check.json:one'])
assert U<=H and not Z&(allK-{tri(caps['B+'])})
# Strict normalized square-exchange controls used by these compositions.
controls=[(F(4,11),F(2,11)),(F(6,11),F(-2,11)),(F(1,2),F(-1,6))]
for u,d in controls:
 assert 0<u<1 and 0<u+2*d<1 and 0<u+d<1
out={'status':'INDEPENDENT_HAND_SUPPORT_AND_DELETION_CHECKS_PASS',
 'subcase':'mixed_e2_d0_leaf_plus_two_e1_roots_b0',
 'local_deletion_templates':local,'flap_intersection_with_maximum_rest':'EXACT_ATTACHING_SEGMENT',
 'flap_contact_with_other_partial_stars':'EMPTY','opposite_root_one_guard':'PASS',
 'pinned_catalog_paths':21,'supplementary_fixed_compositions':2,'sigma_checks_per_path':True,
 'path_checks':rows,'square_exchange_strict_controls':[[str(u),str(d)] for u,d in controls],
 'sources':hashes,'catalog_sha256':hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
 'hand_argument':'review.txt','limits':'No budgetroom enumeration, discovery, orbit run, new direction/word search or peer checker execution. Local templates are geometry identities, not full mixed-budget fixtures. Global erasure and inventory completeness are reviewed by hand.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('Exact flap attachment;315->270 and270->90;21pinnedpaths+2fixedcompositions, allsigma, full D/R support PASS.')
