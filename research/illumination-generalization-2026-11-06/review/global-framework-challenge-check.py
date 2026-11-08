"""R58 prescribed geometry/tiling/surgery checks. No optical discovery or census."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter,defaultdict
import importlib.util,json,hashlib,time,datetime
R=Path(__file__).resolve().parent
E=json.loads((R/'global-framework-challenge-effort.json').read_text());DEADLINE=datetime.datetime.fromisoformat(E['aggregate_deadline_utc']).timestamp()
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
V=[(-1000,-2),(-2,-2),(-2,-10),(2,-10),(2,-2),(10,-2),(10,0),(8,2),(2,2),(2,10),(0,10),(-2,8),(-2,2),(-1000,2)]
S=(-998,0);T=(0,8);g.simple(V);assert g.location(V,S)==g.location(V,T)==1
assert g.location(V,(-499,4))==-1 # midpoint of selected actual pair
area=abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in g.edges(V)))/2;assert area==4100
lens2=[g.dot(g.vec(a,b),g.vec(a,b)) for a,b in g.edges(V)];assert min(lens2)==4 and max(lens2)==998**2
# Exact certificate excluding EVERY strict Euclidean whole-copy factor atW<=21.
assert max(lens2)>33**2*2*min(lens2)
J=sN=IA=0
for x in range(-1000,11):
 for y in range(-10,11):
  z=(x,y);loc=g.location(V,z);isA=x%2==0 and y%2==0
  IA+=loc==1 and isA
  if not isA:
   J+=loc==1;sN+=loc==0 and z not in V
# Canonical alternating unit-square diagonals: even intercepts, oneA pertriangle.
tris=[]
for x in range(-1000,10):
 if time.time()>DEADLINE:raise TimeoutError('original R58 deadline')
 for y in range(-10,10):
  a,b,c,d=(x,y),(x+1,y),(x+1,y+1),(x,y+1)
  tt=[(a,b,c),(a,c,d)] if (x+y)%2==0 else [(a,b,d),(b,c,d)]
  for tri in tt:
   cen=tuple(Q(sum(z[i] for z in tri),3) for i in [0,1])
   if g.location(V,cen)==1:
    assert sum(z[0]%2==0 and z[1]%2==0 for z in tri)==1
    tris.append(tri)
assert len(tris)==8200
edges=Counter(tuple(sorted((a,b))) for t in tris for a,b in zip(t,t[1:]+t[:1]));verts=set(z for t in tris for z in t)
assert all(v in [1,2] for v in edges.values());assert len(verts)-len(edges)+len(tris)==1
bound=[e for e,n in edges.items() if n==1];adj=defaultdict(list)
for a,b in bound:
 assert any(g.on(c,d,a) and g.on(c,d,b) for c,d in g.edges(V));adj[a].append(b);adj[b].append(a)
assert all(len(a)==2 for a in adj.values());seen=set();todo=[bound[0][0]]
while todo:
 z=todo.pop()
 if z in seen:continue
 seen.add(z);todo+=adj[z]
assert seen==set(adj)
# connected triangle dual, hence one actual finite canonical triangle disk
byedge=defaultdict(list)
for i,t in enumerate(tris):
 for a,b in zip(t,t[1:]+t[:1]):byedge[tuple(sorted((a,b)))].append(i)
dual=defaultdict(list)
for ids in byedge.values():
 if len(ids)==2:a,b=ids;dual[a].append(b);dual[b].append(a)
seen=set();todo=[0]
while todo:
 i=todo.pop()
 if i in seen:continue
 seen.add(i);todo+=dual[i]
assert len(seen)==len(tris)
for z in [S,T]:assert sum(z in t for t in tris)==8
# Prescribed actual witness:996horizontal reflections in left arm, then actualtop target.
path=[tuple(map(Q,S))]
for j in range(1,997):
 x=Q(-998)+Q(4*j-2,4);y=Q(2 if j%2 else -2);path.append((x,y))
path.append(tuple(map(Q,T)));witness=g.path_check(V,path);assert witness['reflections']==996
assert not any(g.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]))
# Separate actualmarked optical control demonstrating failure of bevel-filling wordpreservation.
U=(0,0);Z=(6,0);control=[U,(Q(90,11),Q(20,11)),(Q(22,3),-2),(Q(58,9),2),Z];surgery=g.path_check(V,control);assert surgery['reflections']==3
filled=[(-1000,-2),(-2,-2),(-2,-10),(2,-10),(2,-2),(10,-2),(10,2),(2,2),(2,10),(-2,10),(-2,2),(-1000,2)]
g.simple(filled);assert g.location(filled,(Q(90,11),Q(20,11)))==1
vin=(9,2);e=(-2,2);normal=(-e[1],e[0]);vout=tuple(Q(vin[i])-2*Q(g.dot(vin,normal),g.dot(normal,normal))*normal[i] for i in [0,1]);assert vout==(-2,-9)
# Diagonal wall under anisotropic A=diag(2,1) fails Euclidean opticalconjugacy.
A=lambda z:(2*z[0],z[1]);ed=A(e);nn=(-ed[1],ed[0]);av=A(vin);actual=tuple(Q(av[i])-2*Q(g.dot(av,nn),g.dot(nn,nn))*nn[i] for i in [0,1]);assert g.det(A(vout),actual)!=0
out={'status':'EXACT_QUALIFYING_GEOMETRY_AND_SPECIFIED_OPTICAL_OBSTRUCTIONS_PASS','whole_goal_complete':False,'discovery':False,'polygon':V,'main_actual_pair':[S,T],'maximal_walls':len(V),'area':str(Q(int(2*area),2)),'canonical_triangles':len(tris),'vertices':len(verts),'tiling_edges':len(edges),'triangle_dual_connected':True,'boundary_one_cycle':True,'marks_full_A_stars':True,'interior_A_count':IA,'J':J,'s_N':sN,'k':J+sN,'longest_shortest_wall_ratio':'499','strict_Euclidean_factor_bound_violated':'499>33sqrt(2)','main_pair_is_lit':True,'main_prescribed_witness':witness,'main_launch_velocity':[1,4],'surgery_control_pair':[U,Z],'surgery_control_path':[[str(x),str(y)] for x,y in control],'surgery_control':surgery,'old_diagonal_point_in_filled_room':'interior','bevel_incoming':vin,'bevel_reflected':list(vout),'anisotropic_image_of_reflection':list(A(vout)),'anisotropic_actual_reflection':list(actual),'independent_validator_sha256':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}
(R/'global-framework-challenge-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(out)
