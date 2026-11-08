"""Find a numerical LP basis, then reconstruct and check it exactly over Q."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent/'rigidity-review'))
from event_geometry import EventModel,canon,rref,dot,rank
from ortools.linear_solver import pywraplp

def linear_solve(A,b):
 if not A:return []
 n=len(A[0]);rr,piv=rref([list(a)+[v] for a,v in zip(A,b)])
 assert all(p<n for p in piv),'Exact system inconsistent'
 assert len(piv)==n,'LP non-bound variables are not independent'
 solution=[F(0)]*n
 for row,p in zip(rr,piv):solution[p]=row[-1]
 return solution

if __name__=='__main__':
 model=EventModel(json.loads((B/'room.json').read_text()));events=json.loads((B/'events.json').read_text());rows=[tuple(map(F,e['row'])) for e in events];projected=[model.project(r) for r in rows];solver=pywraplp.Solver.CreateSolver('GLOP');solver.SetTimeLimit(10000)
 weights=[solver.NumVar(1,solver.infinity(),f'w{i}') for i in range(len(rows))]
 for j in range(model.dim):
  if not any(g[j] for g in projected):continue
  c=solver.Constraint(0,0)
  for i,g in enumerate(projected):c.SetCoefficient(weights[i],float(g[j]))
 objective=solver.Objective()
 for v in weights:objective.SetCoefficient(v,1)
 objective.SetMinimization();status=solver.Solve()
 out=dict(status='INCONCLUSIVE',solver_status=int(status),solver_version=solver.SolverVersion(),events=len(events),rank_on_closure=rank([*model.closure,*rows])-2,scope='Numerical LP output is accepted only after exact rational reconstruction and positivity/identity checks.')
 if status==pywraplp.Solver.OPTIMAL:
  free=[i for i,v in enumerate(weights) if v.solution_value()>1+1e-6];fixed=[i for i in range(len(rows)) if i not in free]
  coeff=[F(1)]*len(rows)
  if free:
   A=[[g[j] for i,g in enumerate(projected) if i in free] for j in range(model.dim)];rhs=[-sum(projected[i][j] for i in fixed) for j in range(model.dim)];sol=linear_solve(A,rhs)
   for i,value in zip(free,sol):coeff[i]=value
  assert all(c>0 for c in coeff)
  assert all(sum(c*g[j] for c,g in zip(coeff,projected))==0 for j in range(model.dim))
  rawsum=[sum(c*g[j] for c,g in zip(coeff,rows)) for j in range(model.dim)];assert rank([*model.closure,rawsum])==2
  out.update(status='PASS',strict_positive_dependency=True,coefficients=list(map(str,coeff)),non_bound_coefficients=len(free),all_identities_checked_exactly=True,common_kernel_dimension=model.dim-2-out['rank_on_closure'])
 elif status==pywraplp.Solver.INFEASIBLE:
  out['status']='NUMERICAL_INFEASIBLE_NOT_AN_EXACT_EXCLUSION'
 (B/'positive-span.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
