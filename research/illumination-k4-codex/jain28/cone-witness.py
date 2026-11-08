"""Find and verify an exact escape from the finite event halfspaces."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,importlib.util
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent/'rigidity-review'))
from event_geometry import EventModel,rref,dot
from ortools.linear_solver import pywraplp
spec=importlib.util.spec_from_file_location('boundary_events',B/'boundary-check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
if __name__=='__main__':
 model=mod.BoundaryEventModel(json.loads((B/'room.json').read_text()));events=json.loads((B/(sys.argv[1] if len(sys.argv)>1 else 'events-R12.json')).read_text());rows=[tuple(map(F,e['row'])) for e in events]+[model.boundary_row()[0]];solver=pywraplp.Solver.CreateSolver('GLOP');vars=[solver.NumVar(-1,1,f'd{j}') for j in range(model.dim)]
 for row in rows:
  c=solver.Constraint(0,solver.infinity())
  for j,g in enumerate(row):c.SetCoefficient(vars[j],float(g))
 equations=[list(map(F,c)) for c in model.closure]
 for j in (0,1,2,3):equations.append(list(model.unit(j)))
 for row in equations:
  c=solver.Constraint(0,0)
  for j,g in enumerate(row):c.SetCoefficient(vars[j],float(g))
 obj=solver.Objective()
 for j in range(model.dim):obj.SetCoefficient(vars[j],sum(float(g[j]) for g in rows))
 obj.SetMaximization();status=solver.Solve();assert status==pywraplp.Solver.OPTIMAL and obj.Value()>1e-5
 approx=[v.solution_value() for v in vars];A=[r+[F(0)] for r in equations]
 for row in rows:
  if abs(sum(float(g)*v for g,v in zip(row,approx)))<1e-6:A.append(list(row)+[F(0)])
 for j,v in enumerate(approx):
  if abs(abs(v)-1)<1e-6:A.append(list(model.unit(j))+[F(1 if v>0 else -1)])
 rr,piv=rref(A);assert all(p<model.dim for p in piv)
 delta=[F(v).limit_denominator(10**7) for v in approx]
 for row,k in reversed(list(zip(rr,piv))):delta[k]=row[-1]-sum(row[j]*delta[j] for j in range(model.dim) if j!=k)
 values=[dot(g,delta) for g in rows];assert all(v>=0 for v in values) and any(v>0 for v in values)
 assert all(dot(c,delta)==0 for c in equations) and all(abs(v)<=1 for v in delta)
 out=dict(status='EXACT_NON_POSITIVE_SPAN_WITNESS',event_count=len(rows),delta=list(map(str,delta)),positive_constraints=sum(v>0 for v in values),tangent_constraints=sum(v==0 for v in values),minimum_event_value=str(min(values)),event_values=list(map(str,values)),gauge='First vertex and first two edge lengths fixed; closure preserved',interpretation='This rational displacement satisfies all finite event survival inequalities and makes some strict. Thus these supplied rows admit no strictly positive zero dependence. It is not a certified dark deformation or a proof that further events cannot establish rigidity.')
 (B/(sys.argv[2] if len(sys.argv)>2 else 'cone-witness.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
