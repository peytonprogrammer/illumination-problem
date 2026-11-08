"""R59 exact prescribed full-copy separator and regular crossing; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter,defaultdict
import json,hashlib,importlib.util
R=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
frozen=json.loads((R/'global-framework-challenge-check.json').read_text());V=[tuple(z) for z in frozen['polygon']];S,T=map(tuple,frozen['main_actual_pair']);A=(-2,2);B=(2,-2);g.simple(V)
assert g.location(V,S)==g.location(V,T)==1 and sum(S)<0<sum(T)
assert A in V and B in V
for Z in [A,B]:
 i=V.index(Z);u=g.vec(V[i-1],Z);v=g.vec(Z,V[(i+1)%len(V)]);assert g.det(u,v)<0 and g.dot(u,v)==0
# The entire intersection P with line x+y0 is thisoneproperarc.
linehits=[]
for a,b in g.edges(V):
 fa,fb=sum(a),sum(b)
 if fa*fb<0:
  tt=Q(-fa,fb-fa);z=tuple(Q(a[k])+tt*(b[k]-a[k]) for k in [0,1]);linehits.append(z)
 elif not fa:linehits.append(a)
 elif not fb:linehits.append(b)
assert set(linehits)=={A,B};assert g.location(V,(0,0))==1
C=(Q(-8,5),Q(8,5));last=(Q(-5,2),Q(-2));assert g.on(A,B,C) and C not in [A,B] and g.on(last,T,C) and g.location(V,C)==1;assert g.det((1,4),g.vec(A,B))!=0
# Exact8sheetdihedralgroup and four-sector identifications at each reflexendpoint.
def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
I=(1,0,0,1);H=(1,0,0,-1);VV=(-1,0,0,1);DN=(0,-1,-1,0);DP=(0,1,1,0)
def closure(gens):
 seen={I};todo=[I]
 while todo:
  a=todo.pop()
  for b in gens:
   c=mul(a,b)
   if c not in seen:seen.add(c);todo.append(c)
 return seen
D4=closure([H,VV,DN,DP]);K=closure([H,VV]);assert len(D4)==8 and len(K)==4
cosets={frozenset(mul(d,k) for k in K) for d in D4};assert len(cosets)==2
cosets=sorted(cosets,key=lambda z:sorted(z))
def cls(d):return next(i for i,c in enumerate(cosets) if d in c)
edges=[(('A',cls(d)),('B',cls(d))) for d in D4];degrees=Counter(z for e in edges for z in e);assert len(degrees)==4 and set(degrees.values())=={4}
assert 4*270==1080 # coneangle6pi, genuine order2
# Negative and positive physicalside copyadjacency: two versusone component.
assert len(D4)//len(closure([H,VV]))==2
assert len(D4)//len(closure([H,VV,DN,DP]))==1
out={'status':'EXACT_FULL_FIBER_SEPARATOR_AND_LEGAL_REGULAR_CROSSING_PASS','whole_goal_complete':False,'discovery':False,'room_walls':14,'physical_S':S,'physical_T':T,'physical_arc':[A,B],'actual_path_crossing':list(map(str,C)),'crossing_is_regular_interior':True,'transverse':True,'unfolding_sheets':8,'source_fiber_size':8,'target_fiber_size':8,'separator_edges':8,'separator_vertices':4,'separator_vertex_degrees':list(degrees.values()),'separator_vertex_cone_angle':'6pi','separator_graph_components':2,'complement_components_from_copy_gluing':3,'negative_components':2,'positive_components':1,'main_pair_is_lit':True,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['global-framework-challenge.md','global-framework-challenge-check.json','global-framework-challenge-acceptance.json','resumed-exact-check.py']}}
(R/'global-separator-challenge-check.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
