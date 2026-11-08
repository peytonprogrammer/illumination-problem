"""Complete finite I=3 supports at exactly3 B/C exceptions, below24 walls."""
import argparse
import hashlib
import inspect
import json
from pathlib import Path
import time
from ortools.sat.python import cp_model
from illumination_three_star_model import build_model
from search_illumination_family import build_model as original_builder
from illumination_family_bound import NEIGHBORS
from illumination_geometry import check, owners_of
from illumination_transparent_bound import counts
from illumination_paths import find_path
from illumination_sector_paths import verify
from search_illumination_one_exception import tile_facts

BASE=Path(__file__).parent


def checked_builder():
    original=inspect.getsource(original_builder)
    changed=inspect.getsource(build_model)
    assert changed==original.replace('assert transparent_budget in (0, 1, 2)', 'assert transparent_budget in (0, 1, 2, 3)')
    return hashlib.sha256(original.encode()).hexdigest()


def bounded_support(shape, max_walls=23):
    full=set(map(tuple,shape['full_A_cells']))
    mandatory=full|{(x+dx,y+dy) for x,y in full for dx,dy in NEIGHBORS}
    b=len(mandatory-full)
    allowed=set(mandatory)
    extra=(max_walls-6)//2-b
    assert extra>=0
    for _ in range(extra):
        allowed|={(x+dx,y+dy) for x,y in allowed for dx,dy in NEIGHBORS}
    if max_walls==23:
        assert allowed==set(map(tuple,shape['allowed_A_cells']))
    return dict(full=full,mandatory=mandatory,allowed=allowed,partial_required=b,extra_budget=extra)


def make_model(shape, max_walls=23):
    return build_model((0,0),max_walls,3,bounded_support(shape,max_walls))


def solver_for(seconds):
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=2
    solver.parameters.random_seed=61;solver.parameters.max_time_in_seconds=seconds
    return solver


def make_room(shape,pair,ts,x,solver):
    room=dict(triangles=[t for t,v in zip(ts,x) if solver.value(v)],
              marked=[[2*v for v in p] for p in pair],require_simple=True)
    geometry=check(room,strict=False);c=counts(room)
    assert geometry['simple_polygon'] and c['interior_A']==3
    assert c['interior_nonA']+c['smooth_boundary_nonA']==3
    assert set(map(tuple,geometry['interior_A']))=={tuple(2*v for v in p) for p in shape['full_A_cells']}
    assert c['triangles']<=4*(c['walls']-2+c['defect_credit'])//3
    return room,c


def geometry_case(index,shape,seconds=20):
    model,ts,x,_,terms=make_model(shape)
    solver=solver_for(seconds);status=solver.solve(model)
    result=dict(shape=index,status=solver.status_name(status),seconds=solver.wall_time,
                available_triangles=len(ts),full_A_cells=shape['full_A_cells'])
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        room,c=make_room(shape,shape['nonadjacent_mark_pairs'][0],ts,x,solver)
        assert c['walls']<=23 and c['triangles']<=36
        result.update(room=room,counts=c)
    (BASE/f'three-star-geometry-{index}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(event='geometry',**{k:v for k,v in result.items() if k!='room'})),flush=True)
    return result


def ray_case(index,pair_index,shape,geometry,seconds=40):
    pair=shape['nonadjacent_mark_pairs'][pair_index]
    started=time.monotonic()
    filename=BASE/f'three-star-case-{index}-{pair_index}.json'
    records=[]
    if geometry['status']=='INFEASIBLE':
        result=dict(shape=index,pair_index=pair_index,marked=pair,status='INFEASIBLE',exhausted=True,
                    stop_reason='geometry_excluded',records=0,cuts=0,seconds=0)
        filename.write_text(json.dumps(dict(summary=result,records=[]),indent=2)+'\n')
        return result
    model,ts,x,_,terms=make_model(shape);owners=owners_of(ts)
    solver=solver_for(seconds)
    if filename.exists():
        previous=json.loads(filename.read_text());records=previous['records']
        if previous['summary']['exhausted']:
            return previous['summary']
        for record in records:
            model.add(sum(1-x[i] if value else x[i] for i,value in record['tile_facts'])>=1)
    seeded=len(records);status=None;reason='time_limit';survivor=None
    def save():
        result=dict(shape=index,pair_index=pair_index,marked=pair,status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                    exhausted=status==cp_model.INFEASIBLE,stop_reason=reason,records=len(records),cuts=len(records),
                    new_records=len(records)-seeded,seconds=time.monotonic()-started,survivor=survivor,
                    triangle_index_sha256=hashlib.sha256(json.dumps(ts).encode()).hexdigest())
        temp=filename.with_suffix('.tmp');temp.write_text(json.dumps(dict(summary=result,records=records),indent=2)+'\n');temp.replace(filename)
        return result
    while time.monotonic()-started<seconds:
        solver.parameters.max_time_in_seconds=max(.001,seconds-(time.monotonic()-started))
        status=solver.solve(model)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            reason='exhausted' if status==cp_model.INFEASIBLE else 'solver_unknown';break
        room,c=make_room(shape,pair,ts,x,solver)
        witness=find_path(room,16,1000)
        if witness['status']!='illuminated':witness=find_path(room,32,2000)
        if witness['status']!='illuminated':
            reason='unresolved_candidate';survivor=dict(room=room,bounded_screen=witness);break
        verify(room,witness);facts=tile_facts(ts,owners,witness,room)
        records.append(dict(room=room,counts=c,witness=witness,tile_facts=facts))
        model.add(sum(1-x[i] if value else x[i] for i,value in facts)>=1)
        if (len(records)-seeded)%10==0:
            print(json.dumps(dict(event='screened',**save())),flush=True)
    result=save();print(json.dumps(dict(event='case',**result)),flush=True);return result


def control(shapes):
    trials=[]
    for i,shape in enumerate(shapes):
        model,ts,x,_,terms=make_model(shape,24);solver=solver_for(10);status=solver.solve(model)
        trial=dict(shape=i,status=solver.status_name(status),seconds=solver.wall_time)
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            room,c=make_room(shape,shape['nonadjacent_mark_pairs'][0],ts,x,solver)
            trial.update(room=room,counts=c)
        trials.append(trial)
        if 'room' in trial:break
    result=dict(status='POSITIVE_CONTROL' if any('room' in t for t in trials) else 'NO_CONTROL_FOUND',trials=trials)
    (BASE/'three-star-control24.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(event='control',status=result['status'])),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=40);args=ap.parse_args()
    source_hash=checked_builder()
    shapes=json.loads((BASE/'three-star-shapes.json').read_text())['shapes']
    geometries=[geometry_case(i,shape) for i,shape in enumerate(shapes)]
    results=[ray_case(i,j,shape,geometries[i],args.seconds) for i,shape in enumerate(shapes) for j in range(len(shape['nonadjacent_mark_pairs']))]
    control(shapes)
    summary=dict(status='EXCLUDED' if all(r['exhausted'] for r in results) else 'INCOMPLETE',geometries=geometries,cases=results,
                 original_builder_function_sha256=source_hash,
                 scope='Exactly3 full A stars / exactly3 B/C exceptions, W<=23, all5 complete supports and all10 nonadjacent marked pairs. I=2 not searched; no global three-exception conclusion.')
    (BASE/'three-star-extension-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
