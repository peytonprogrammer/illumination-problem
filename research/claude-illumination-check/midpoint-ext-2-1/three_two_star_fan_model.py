"""Separate one-hot fan/SCIP necessary relaxation for the I=2,k=3 branch."""
from collections import defaultdict
import json
from pathlib import Path
from ortools.linear_solver import pywraplp
from illumination_geometry import check_fan_angles,owners_of,label
from illumination_family_bound import triangles_in_cells
from illumination_three_two_star_bound import TARGETS,complete_support
from illumination_cell_path_bound import path_charge_lower_bound,connected_cell_sets

BASE=Path(__file__).parent
OUT=BASE/'three-two-star'


def solve(target,facts_list=(),fixed_room=None,seconds=20):
    bounded=complete_support(target);ts=triangles_in_cells(bounded['allowed'])
    solver=pywraplp.Solver.CreateSolver('SCIP');solver.SetNumThreads(1);solver.SetTimeLimit(int(seconds*1000))
    x=[solver.IntVar(0,1,f't{i}') for i in range(len(ts))]
    incident=defaultdict(list)
    for i,t in enumerate(ts):
        for p in t:incident[p].append(i)
    full={(2*a,2*b) for a,b in bounded['full']}
    walls=[];charges=[];bads=[];credits=[];used={}
    for p,ids in incident.items():
        rows=[]
        for mask in range(1<<len(ids)):
            selected=[ts[i] for bit,i in enumerate(ids) if mask>>bit&1]
            owners=owners_of(selected);opens={e for e,os in owners.items() if len(os)==2}
            angles,interior=check_fan_angles(selected,p,owners,opens)
            if len(angles)>1 or (label(p)=='A' and interior!=(p in full)):continue
            bad=int(label(p)!='A' and (interior or angles==[4]));credit=(2 if interior else 1) if bad else 0
            wall=int(bool(angles) and angles!=[4])
            charge=0 if label(p)!='A' or interior or not angles else (3 if angles==[4] else angles[0])
            w=solver.NumVar(0,1,f'f{p}_{mask}');rows.append((mask,w))
            walls.append(wall*w);charges.append(charge*w);bads.append(bad*w);credits.append(credit*w)
        solver.Add(sum(w for _,w in rows)==1)
        for bit,i in enumerate(ids):solver.Add(sum(w for mask,w in rows if mask>>bit&1)==x[i])
        if label(p)=='A':used[p]=sum(w for mask,w in rows if mask)
    W,Q,E=sum(walls),sum(charges),sum(credits)
    missing=sum(1-used[2*a,2*b] for a,b in bounded['mandatory']-bounded['full'])
    solver.Add(W<=23);solver.Add(W-Q+E==14);solver.Add(sum(bads)==3)
    solver.Add(missing+E<=6);solver.Add(Q+missing<=15);solver.Add(Q>=2*sum(used.values())-10+missing)
    if sum(target)>=3:
        solver.Add(Q+missing>=path_charge_lower_bound(target))
        choices=connected_cell_sets(tuple(target))
        weights=[solver.IntVar(0,1,f'outside{j}') for j in range(len(choices))]
        solver.Add(sum(weights)==1)
        for a,b in sorted(bounded['allowed']-bounded['mandatory']):
            solver.Add(used[2*a,2*b]==sum(w for selected,w in zip(choices,weights) if (a,b) in selected))
    for facts in facts_list:solver.Add(sum(1-x[i] if value else x[i] for i,value in facts)>=1)
    if fixed_room is not None:
        selected={tuple(sorted(map(tuple,t))) for t in fixed_room['triangles']};assert selected<=set(ts)
        for t,v in zip(ts,x):solver.Add(v==int(t in selected))
    status=solver.Solve();names={solver.OPTIMAL:'OPTIMAL',solver.FEASIBLE:'FEASIBLE',solver.INFEASIBLE:'INFEASIBLE',solver.NOT_SOLVED:'NOT_SOLVED'}
    return dict(target_A_cell=target,status=names.get(status,str(status)),seconds=solver.WallTime()/1000,
                variables=solver.NumVariables(),constraints=solver.NumConstraints(),rays=len(facts_list),fixed_control=fixed_room is not None,
                scope='Independent fan necessary relaxation; no explicit connectivity, Euler constraint or triangle-count constraint.')


if __name__=='__main__':
    for t in TARGETS:
        path=OUT/f'geometry-{t[0]}-{t[1]}.json'
        if not path.exists():continue
        geo=json.loads(path.read_text())
        fixed=geo.get('room') if t==(1,1) else None
        if fixed is None and geo['status'] in ('OPTIMAL','FEASIBLE'):continue
        result=solve(t,fixed_room=fixed)
        (OUT/f'fan-geometry-{t[0]}-{t[1]}.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)
