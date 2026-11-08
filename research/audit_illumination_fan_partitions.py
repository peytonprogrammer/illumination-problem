"""Replay complete fan branches and independently check new path guards."""
import argparse
import json
from ortools.sat.python import cp_model
from audit_illumination_three_two_star import touched_tiles
from classify_illumination_three_exception import OUT,digest,solver_for
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from search_illumination_cell_partitions import fix_cells,room_outside
from search_illumination_fan_partitions import TARGET,CELL,PATH,load_seed,fan_masks,fix_fan
from search_illumination_one_exception import tile_facts
from search_illumination_three_two_star import add_guard


def audit(seconds):
    saved=json.loads(PATH.read_text())
    model,ts,x,bounded,terms,keys,residual,provenance=load_seed()
    assert saved['provenance']==provenance
    ids,masks=fan_masks(ts)
    # Independent fan coverage: connected proper subsets of the tile adjacency cycle.
    local=[ts[i] for i in ids];adj={j:set() for j in range(8)}
    for e,os in owners_of(local).items():
        if len(os)==2:
            a,b=os;adj[a].add(b);adj[b].add(a)
    assert all(len(v)==2 for v in adj.values())
    expected=[0]
    for mask in range(1,255):
        chosen={j for j in range(8) if mask>>j&1};seen={min(chosen)};todo=list(seen)
        for j in todo:
            for k in adj[j]&chosen-seen:seen.add(k);todo.append(k)
        if seen==chosen:expected.append(mask)
    assert masks==expected and len(masks)==57
    assert saved['summary']['fan_triangle_ids']==ids
    assert saved['summary']['masks']==masks
    owners=owners_of(ts);seen=set(keys);rooms=set();rays=mutations=corruptions=0;max_bounces=0
    for n,record in enumerate(saved['records'],1):
        room=record['room'];validate(room,TARGET);verify(room,record['witness'])
        outside=room_outside(room,TARGET);assert outside in residual
        assert outside==tuple(map(tuple,record['outside_cells']))
        selected={tuple(sorted(map(tuple,t))) for t in room['triangles']}
        assert tuple(sorted(selected)) not in rooms;rooms.add(tuple(sorted(selected)))
        assert sum((1<<j) for j,i in enumerate(ids) if ts[i] in selected)==record['mask']
        max_bounces=max(max_bounces,record['witness']['bounces'])
        for guard in record['derived_guards']:
            verify(guard['room'],guard['witness'])
            facts=tile_facts(ts,owners,guard['witness'],guard['room']);assert facts==list(map(tuple,guard['tile_facts']))
            key=tuple(facts);assert key not in seen;seen.add(key)
            required=touched_tiles(ts,guard['witness']);fixed=dict(facts)
            tiles={tuple(sorted(map(tuple,t))) for t in guard['room']['triangles']}
            assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in tiles) for i in required)
            if corruptions<8:
                i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
                flipped=dict(fixed);flipped[i]=1-flipped[i];assert any(flipped[k]!=int(ts[k] in tiles) for k in required);corruptions+=2
            if mutations<8:
                for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:
                    verify(dict(guard['room'],triangles=sorted(tiles^{ts[i]})),guard['witness']);mutations+=1
            add_guard(model,x,facts);rays+=1
        if n%25==0:print(json.dumps(dict(event='fan_ray_audit',records=n,rays=rays)),flush=True)
    assert len(saved['records'])==saved['summary']['records']
    assert rays==saved['summary']['new_guards']
    claims={(tuple(map(tuple,c['outside_cells'])),c['mask']):c for c in saved['classes']}
    assert len(claims)==len(saved['classes'])
    assert set(claims)=={(outside,mask) for outside in residual for mask in masks}
    solver=solver_for(seconds,113);replays=[]
    # Replay all original cell sets, so prior exclusions remain checked with current guards.
    choices=__import__('illumination_triple_cell_sets').outside_sets(TARGET)[0]
    cell_replays=[]
    for outside in choices:
        branch=model.clone();fix_cells(branch,terms,bounded,outside)
        solver.parameters.max_time_in_seconds=seconds;status=solver.solve(branch)
        cell_replays.append(dict(outside_cells=outside,status=solver.status_name(status)))
    print(json.dumps(dict(event='fan_cell_replay',checked=len(cell_replays),excluded=sum(c['status']=='INFEASIBLE' for c in cell_replays))),flush=True)
    for outside in residual:
        for mask in masks:
            branch=model.clone();fix_cells(branch,terms,bounded,outside);fix_fan(branch,x,ids,mask)
            solver.parameters.max_time_in_seconds=seconds;status=solver.solve(branch)
            claim=claims[outside,mask]
            if claim['exhausted'] and status!=cp_model.INFEASIBLE:
                solver.parameters.max_time_in_seconds=30;status=solver.solve(branch)
                assert status==cp_model.INFEASIBLE,('unreproduced claim',outside,mask,solver.status_name(status))
            replays.append(dict(outside_cells=outside,mask=mask,status=solver.status_name(status)))
            if len(replays)%30==0:print(json.dumps(dict(event='fan_branch_replay',checked=len(replays),excluded=sum(c['status']=='INFEASIBLE' for c in replays))),flush=True)
    solver.parameters.max_time_in_seconds=60;status=solver.solve(model)
    result=dict(status='PASS',source_sha256=digest(PATH),provenance=provenance,fan_cell=CELL,fan_masks=masks,
                independent_adjacency_masks=expected,records=len(saved['records']),exact_new_guards=rays,
                mutations=mutations,corruptions=corruptions,max_bounces=max_bounces,
                partition_size=len(replays),branches_excluded=sum(c['status']=='INFEASIBLE' for c in replays),classes=replays,
                cell_sets_excluded=sum(c['status']=='INFEASIBLE' for c in cell_replays),cell_classes=cell_replays,
                unrestricted_parent=solver.status_name(status),
                placement_excluded=status==cp_model.INFEASIBLE or (all(c['status']=='INFEASIBLE' for c in replays) and all(c['status']=='INFEASIBLE' for c in cell_replays if tuple(map(tuple,c['outside_cells'])) not in residual)),
                scope='Complete 57-mask refinement of all five residual outside sets; positive exact rays only. Caps remain unresolved. Computer-assisted exclusion, not formal UNSAT proof.')
    (OUT/'fan-audit-2-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('classes','cell_classes','fan_masks','independent_adjacency_masks','provenance')}),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=3);args=ap.parse_args();audit(args.seconds)
