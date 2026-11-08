"""R60 prescribed27-elementHeisenberg origami algebra; no direction/orbit discovery."""
from pathlib import Path
import itertools,json,hashlib
R=Path(__file__).resolve().parent
G=list(itertools.product(range(3),repeat=3));e=(0,0,0);r=(1,0,0);u=(0,1,0);z=(0,0,1)
def mul(g,h):
 a,b,c=g;A,B,C=h;return ((a+A)%3,(b+B)%3,(c+C+a*B)%3)
def power(g,n):
 v=e
 for _ in range(n%3):v=mul(v,g)
 return v
def inv(g):
 a,b,c=g;return ((-a)%3,(-b)%3,(-c+a*b)%3)
for a,b,c in itertools.product(G,repeat=3):assert mul(mul(a,b),c)==mul(a,mul(b,c))
for g in G:
 assert mul(g,inv(g))==mul(inv(g),g)==e
 assert mul(mul(g,g),g)==e
 assert mul(z,g)==mul(g,z)
assert mul(mul(mul(r,u),inv(r)),inv(u))==z
reachable={e};todo=[e]
while todo:
 g=todo.pop()
 for h in [r,u]:
  v=mul(g,h)
  if v not in reachable:reachable.add(v);todo.append(v)
assert len(reachable)==27
idx={g:i for i,g in enumerate(G)};rp=[idx[mul(g,r)] for g in G];up=[idx[mul(g,u)] for g in G];tau=[idx[mul(z,g)] for g in G]
assert sorted(rp)==sorted(up)==sorted(tau)==list(range(27))
for i in range(27):assert tau[rp[i]]==rp[tau[i]] and tau[up[i]]==up[tau[i]]
# Vertex cycles are rightmultiplicationcommutator, up to inverse convention.
cp=[idx[mul(g,z)] for g in G];seen=set();cycles=[]
for i in range(27):
 if i in seen:continue
 cyc=[];j=i
 while j not in cyc:cyc.append(j);seen.add(j);j=cp[j]
 assert j==i and len(cyc)==3;cycles.append(cyc)
assert len(cycles)==9
for C in cycles:assert {tau[i] for i in C}==set(C)
center={g for g in G if all(mul(g,h)==mul(h,g) for h in G)};assert center=={e,z,power(z,2)}
allowed=set()
for g in G:
 if g[:2]!=(0,0):
  cyc={power(g,n) for n in range(3)};assert cyc.isdisjoint({z,power(z,2)});allowed|=cyc
assert len(allowed)==25 and set(G)-allowed=={z,power(z,2)}
out={'status':'HEISENBERG_ORIGAMI_AND_ALL_PRIMITIVE_MONODROMY_EXCLUSION_ALGEBRA_PASS','whole_goal_complete':False,'discovery':False,'square_count':27,'connected':True,'r':rp,'u':up,'central_tau':tau,'vertex_cycles':cycles,'true_zero_count':9,'true_zero_orders':[2]*9,'regular_vertex_fiber_over_branch_point':0,'genus':10,'central_tau_order':3,'central_tau_fixes_all_true_zeros':True,'nonzero_abelianization_cyclic_union_size':25,'excluded_central_elements':[z,power(z,2)],'surface_graph_slope':1,'physical_polygon_constructed':False,'physical_full_fiber_darkness_claimed':False,'proof_obligation':'Everyzero-freeconnectingpathprojects to repeatedprimitiveclosedtorusline withnonzero primitivehomology mod3. Handproofrequired, not a bounded direction scan.'}
(R/'global-blocking-check.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['r','u','central_tau','vertex_cycles']})
