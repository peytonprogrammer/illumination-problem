"""Prescribed R26 joint-growth path and rational sign controls. No ray/word search."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations
import importlib.util,json,signal,time,math
H=Path(__file__).resolve().parent
e=json.loads((H/'joint-growth-limit-effort.json').read_text())
deadline=datetime.fromisoformat(e['deadline_utc']).timestamp()
assert time.time()<deadline,'Original R26 aggregate deadline expired'
signal.alarm(max(1,int(deadline-time.time())))
sp=importlib.util.spec_from_file_location('own',H/'resumed-exact-check.py')
own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
# Each coordinate is (coefficient of lambda, constant).
def pt(ax,bx,ay,by):return ((Q(ax),Q(bx)),(Q(ay),Q(by)))
P=[pt(0,0,0,0),pt(4,0,0,0),pt(4,0,Q(1,2),0),pt(4,-1,Q(1,2),0),pt(4,-1,Q(3,2),0),pt(4,0,Q(3,2),0),pt(4,0,2,-1),pt(2,-1,2,-1),pt(2,-1,4,0),pt(0,0,4,0)]
path=[pt(3,0,1,0),pt(2,0,0,0),pt(0,0,2,0),pt(1,0,3,0)]
def value(z,L):return tuple(a*L+b for a,b in z)
def sub(a,b):return tuple(b[k]-a[k] for k in range(2))
def mul(a,b):return (a[1]*b[1],a[0]*b[1]+a[1]*b[0],a[0]*b[0])
def orient(a,b,c):
 u=[sub(a[k],b[k]) for k in range(2)];v=[sub(a[k],c[k]) for k in range(2)]
 x=mul(u[0],v[1]);y=mul(u[1],v[0]);return tuple(x[k]-y[k] for k in range(3))
mid=[tuple(tuple((a[k][j]+b[k][j])/2 for j in range(2)) for k in range(2)) for a,b in zip(path,path[1:])]
points=P+path+mid
polys=[]
for a,b in combinations(points,2):
 for k in range(2):
  v=sub(a[k],b[k]);polys.append((v[1],v[0]))
for a,b,c in combinations(points,3):polys.append(orient(a,b,c))
nonzero=[p for p in polys if any(p)]
# For lambda>N>=1, the leading term strictly dominates lower terms.
bounds=[]
for p in nonzero:
 d=max(i for i,x in enumerate(p) if x);bounds.append(Q(1)+2*sum(abs(p[i]) for i in range(d))/abs(p[d]))
N=math.ceil(max(bounds))
rows=[]
for L in (Q(4),Q(8),Q(20),Q(4*(N//4+2))):
 assert time.time()<deadline
 polygon=[value(z,L) for z in P];actual=[value(z,L) for z in path]
 own.simple(polygon);assert len(polygon)==10
 assert all(z.denominator==1 for point in polygon for z in point)
 assert all(z.denominator==1 and z%2==0 for point in (actual[0],actual[-1]) for z in point)
 assert not any(own.on(a,b,actual[-1]) for a,b in zip(actual[:-2],actual[1:-1]))
 guards=own.path_check(polygon,actual);assert guards['reflections']==2
 rows.append({'lambda':L,'actual_source':actual[0],'actual_target':actual[-1],**guards})
# A whole half-line sign certificate, not just point evaluation.
for p,bound in zip(nonzero,bounds):
 d=max(i for i,x in enumerate(p) if x)
 assert N>=bound>=1
 assert sum(abs(p[i]) for i in range(d))<abs(p[d])*N
# Trace controls at the normalized limiting path, retaining every index.
K=[(value(a,Q(1)),value(b,Q(1))) for a,b in own.edges([pt(z[0][0],0,z[1][0],0) for z in P])]
limit=[tuple(z[k][0] for k in range(2)) for z in path]
assert limit==[(Q(3),Q(1)),(Q(2),Q(0)),(Q(0),Q(2)),(Q(1),Q(3))]
assert all(z not in [a for a,b in K] for z in limit)
for z in limit[1:-1]:assert sum(a!=b and own.on(a,b,z) for a,b in K)==1
out={'status':'PRESCRIBED_JOINT_GROWTH_PATH_AND_SIGN_CONTROLS_PASS','discovery':False,'rows':rows,'guard_polynomials_total':len(polys),'guard_polynomials_nonzero':len(nonzero),'max_guard_degree':max(max(i for i,x in enumerate(p) if x) for p in nonzero),'safe_sign_cutoff_lambda':N,'all_nonzero_guard_signs_constant_above_cutoff':True,'whole_goal_complete':False,'independent_acceptance':False,'ended_utc':datetime.now(timezone.utc).isoformat(),'within_original_deadline':time.time()<deadline,'scope':'One prescribed10wall affine two-axis family and its finite order-type sign controls; hand theorem provides general limiting-witness transfer, not universal W21 coverage.'}
(H/'joint-growth-limit-controls.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
signal.alarm(0)
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
