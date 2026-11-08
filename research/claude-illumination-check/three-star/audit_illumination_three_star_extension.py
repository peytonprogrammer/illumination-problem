"""Independent fan/SCIP relaxation and exact ray audit of the I=3 extension."""
from collections import defaultdict
import itertools
import json
from pathlib import Path
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
from illumination_geometry import label, owners_of, check_fan_angles
from illumination_family_bound import NEIGHBORS
from illumination_cover import D4, mat
from illumination_two_exception_bound import canonical
from illumination_transparent_bound import counts
from illumination_sector_paths import verify
from search_illumination_one_exception import tile_facts
from audit_illumination_one_exception import untrimmed_facts
from search_illumination_three_star import make_model, checked_builder, solver_for, bounded_support
from illumination_three_exception_bound import shapes as shape_enumeration

BASE=Path(__file__).parent


def independent_shapes():
    # Any connected 3-point distance-two overlap graph has a vertex adjacent
    # to both others. Root at that vertex, enumerate only radius2, not radius4.
    near=[(x,y) for x in range(-2,3) for y in range(-2,3) if 0<abs(x)+abs(y)<=2]
    found=set();checked=0
    for a,b in itertools.combinations(near,2):
        full={(0,0),a,b}
        outside={(x+dx,y+dy) for x,y in full for dx,dy in NEIGHBORS}-full
        checked+=1
        if len(outside)<=8:
            variants=[]
            for g in D4:
                changed=[mat(g,p) for p in full]
                for root in changed:
                    variants.append(tuple(sorted((p[0]-root[0],p[1]-root[1]) for p in changed)))
            found.add(min(variants))
    return found,checked


def fan_model(shape, ray_records, max_walls=23, fixed_room=None):
    _,ts,_,_,_=make_model(shape,max_walls)
    solver=pywraplp.Solver.CreateSolver('SCIP');solver.SetNumThreads(1);solver.SetTimeLimit(20000)
    x=[solver.IntVar(0,1,f't{i}') for i in range(len(ts))]
    incident=defaultdict(list)
    for i,t in enumerate(ts):
        for p in t:incident[p].append(i)
    full={tuple(2*v for v in p) for p in shape['full_A_cells']}
    wall_terms=[];charge_terms=[];bad_terms=[];credit_terms=[]
    used_A={}
    for p,ids in incident.items():
        rows=[]
        for mask in range(1<<len(ids)):
            selected=[ts[i] for bit,i in enumerate(ids) if mask>>bit&1]
            owners=owners_of(selected);opens={e for e,os in owners.items() if len(os)==2}
            angles,interior=check_fan_angles(selected,p,owners,opens)
            if len(angles)>1 or (label(p)=='A' and interior!=(p in full)):
                continue
            bad=int(label(p)!='A' and (interior or angles==[4]))
            credit=(2 if interior else 1) if bad else 0
            wall=int(bool(angles) and angles!=[4])
            charge=0 if label(p)!='A' or interior or not angles else (3 if angles==[4] else angles[0])
            weight=solver.NumVar(0,1,f'f{p}_{mask}');rows.append((mask,weight))
            wall_terms.append(wall*weight);charge_terms.append(charge*weight)
            bad_terms.append(bad*weight);credit_terms.append(credit*weight)
        solver.Add(sum(w for _,w in rows)==1)
        for bit,i in enumerate(ids):solver.Add(sum(w for mask,w in rows if mask>>bit&1)==x[i])
        if label(p)=='A':used_A[p]=sum(w for mask,w in rows if mask)
    walls,Q,E=sum(wall_terms),sum(charge_terms),sum(credit_terms)
    solver.Add(walls<=max_walls);solver.Add(walls-Q+E==20);solver.Add(sum(bad_terms)==3)
    bounded=bounded_support(shape,max_walls)
    missing=sum(1-used_A[2*a,2*b] for a,b in bounded['mandatory']-bounded['full'])
    solver.Add(missing+E<=6);solver.Add(Q+missing<=max_walls-14)
    solver.Add(Q>=2*sum(used_A.values())-14+missing)
    for record in ray_records:
        solver.Add(sum(1-x[i] if v else x[i] for i,v in record['tile_facts'])>=1)
    if fixed_room is not None:
        chosen={tuple(sorted(map(tuple,t))) for t in fixed_room['triangles']}
        assert chosen<=set(ts)
        for t,v in zip(ts,x):solver.Add(v==int(t in chosen))
    status=solver.Solve()
    names={solver.INFEASIBLE:'INFEASIBLE',solver.OPTIMAL:'OPTIMAL',solver.FEASIBLE:'FEASIBLE',solver.NOT_SOLVED:'NOT_SOLVED'}
    return dict(status=names.get(status,str(status)),seconds=solver.WallTime()/1000,
                triangles=len(ts),variables=solver.NumVariables(),constraints=solver.NumConstraints(),
                scope='Independent one-hot fan relaxation; omits explicit Euler and connectivity constraints.')


def main():
    checked_builder()
    shapes=json.loads((BASE/'three-star-shapes.json').read_text())['shapes']
    independent,patterns=independent_shapes()
    assert independent=={tuple(map(tuple,s['full_A_cells'])) for s in shapes}
    assert shape_enumeration()['normalized_three_star_shapes']==5
    results=[];rays=mutations=comparisons=records=0
    for i,shape in enumerate(shapes):
        source=json.loads((BASE/f'three-star-geometry-{i}.json').read_text())
        for j,pair in enumerate(shape['nonadjacent_mark_pairs']):
            saved=json.loads((BASE/f'three-star-case-{i}-{j}.json').read_text())
            model,ts,x,_,_=make_model(shape);owners=owners_of(ts)
            for record in saved['records']:
                c=counts(record['room']);assert c['interior_A']==3 and c['interior_nonA']+c['smooth_boundary_nonA']==3
                assert c['walls']<=23 and c['triangles']<=36
                assert record['room']['marked']==[[2*v for v in p] for p in pair]
                verify(record['room'],record['witness']);rays+=1;records+=1
                facts=tile_facts(ts,owners,record['witness'],record['room'])
                assert facts==list(map(tuple,record['tile_facts']))
                model.add(sum(1-x[k] if v else x[k] for k,v in facts)>=1)
                if comparisons<5:
                    assert facts==untrimmed_facts(ts,record['witness'],record['room']);comparisons+=1
                if mutations<24:
                    selected={tuple(sorted(map(tuple,t))) for t in record['room']['triangles']}
                    for k in [k for k in range(len(ts)) if k not in dict(facts)][:min(4,24-mutations)]:
                        verify(dict(record['room'],triangles=sorted(selected^{ts[k]})),record['witness']);mutations+=1
            solver=solver_for(20);status=solver.solve(model)
            if saved['summary']['exhausted']:assert status==cp_model.INFEASIBLE
            mip=fan_model(shape,saved['records'])
            result=dict(shape=i,pair_index=j,fresh_CP_status=solver.status_name(status),independent_fan_SCIP=mip,
                        rays=len(saved['records']))
            print(json.dumps(result),flush=True);results.append(result)
    control=json.loads((BASE/'three-star-control24.json').read_text())
    assert control['status']=='POSITIVE_CONTROL'
    positives=0
    for trial in control['trials']:
        if 'room' not in trial:continue
        room=trial['room'];c=counts(room)
        assert c['interior_A']==3 and c['interior_nonA']+c['smooth_boundary_nonA']==3 and c['walls']<=24
        model,ts,x,_,_=make_model(shapes[trial['shape']],24)
        selected={tuple(sorted(map(tuple,t))) for t in room['triangles']}
        for t,v in zip(ts,x):model.add(v==int(t in selected))
        solver=solver_for(10);assert solver.solve(model)==cp_model.OPTIMAL
        independent_control=fan_model(shapes[trial['shape']],[],24,room)
        assert independent_control['status']=='OPTIMAL'
        positives+=1
    result=dict(status='PASS',three_star_branch='EXCLUDED' if all(r['fresh_CP_status']=='INFEASIBLE' for r in results) else 'INCOMPLETE',
                independent_grid_patterns=patterns,normalized_shapes=5,mark_pair_cases=len(results),
                exact_rays_checked=rays,room_records=records,full_clipped_guard_comparisons=comparisons,
                guard_preserving_mutations=mutations,fixed_positive_controls=positives,independent_fixed_positive_controls=positives,cases=results,
                independently_excluded_by_fan_SCIP=sum(r['independent_fan_SCIP']['status']=='INFEASIBLE' for r in results),
                scope='I=3 / exactly3 B/C exceptions below24. I=2 is not covered; no full three-exception family exclusion.')
    (BASE/'three-star-extension-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':main()
