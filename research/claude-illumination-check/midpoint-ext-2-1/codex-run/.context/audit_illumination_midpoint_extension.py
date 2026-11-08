"""Check the extension's exact paths, sufficient facts, controls and implications."""
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT, digest, solver_for
from extend_illumination_midpoint_covers import PATH, load_base
from audit_illumination_midpoint_covers import signature, positive_controls
from audit_illumination_three_two_star import touched_tiles
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from search_illumination_midpoint_covers import TARGET, fixed_neck, one_pass
from search_illumination_one_exception import tile_facts
from search_illumination_three_two_star import add_guard


def run():
    saved = json.loads(PATH.read_text())
    model, ts, x, bounded, terms, first, second, patterns, keys, base_guards, peer_guards, provenance = load_base()
    assert saved['provenance']==provenance
    assert saved['peer_guards']==json.loads(json.dumps(peer_guards))
    # Positive controls use the original geometry parent before any ray exclusions.
    from search_illumination_midpoint_covers import geometry_parent
    bare, cts, cx, cb, ct, cf, cs, cp = geometry_parent()
    controls = positive_controls(bare,cts,cx,cb,ct,cf,cs,cp)
    owners=owners_of(ts)
    original_count=len(keys)
    mutation_checks=corrupt_guard_checks=0
    max_bounces=0
    rooms=set()
    for record in saved['records']:
        room=record['room'];validate(room,TARGET);one_pass(room,record['witness'])
        p=patterns[record['neck_type']-1]
        assert signature(room,ts,first,second,bounded)==(tuple(map(tuple,p[0])),p[1],p[2])
        room_key=tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))
        assert room_key not in rooms;rooms.add(room_key)
        for g in record['derived_guards']:
            data,witness=g['room'],g['witness'];validate(data,TARGET);one_pass(data,witness)
            facts=tile_facts(ts,owners,witness,data)
            assert facts==list(map(tuple,g['tile_facts']))
            key=tuple(facts);assert key not in keys;keys.add(key)
            required=touched_tiles(ts,witness);fixed=dict(facts)
            selected={tuple(sorted(map(tuple,t))) for t in data['triangles']}
            assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
            if corrupt_guard_checks<8:
                i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
                flipped=dict(fixed);flipped[i]=1-flipped[i];assert flipped[i]!=int(ts[i] in selected);corrupt_guard_checks+=2
            if mutation_checks<8:
                for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutation_checks)]:
                    verify(dict(data,triangles=sorted(selected^{ts[i]})),witness);mutation_checks+=1
            max_bounces=max(max_bounces,witness['bounces'])
            add_guard(model,x,facts)
    assert len(keys)-original_count==saved['summary']['new_guards']
    claims={c['neck_type']:c for c in saved['classes']};assert set(claims)==set(range(1,13))
    solver=solver_for(10,233);solver.parameters.cp_model_presolve=False
    cases=[]
    for n,p in enumerate(patterns,1):
        branch=model.clone();fixed_neck(branch,terms,bounded,x,first,second,p)
        solver.parameters.max_time_in_seconds=60 if claims[n]['exhausted'] else 10
        status=solver.solve(branch)
        if claims[n]['exhausted']:assert status==cp_model.INFEASIBLE
        cases.append(dict(neck_type=n,status=solver.status_name(status),conditional_lemma=status==cp_model.INFEASIBLE))
        print(json.dumps(cases[-1]),flush=True)
    result=dict(status='PASS',source_sha256=digest(PATH),provenance=provenance,fixed_positive_controls=controls,
                new_rooms=len(rooms),new_guards=len(keys)-original_count,peer_seed_guards=len(peer_guards),
                total_guards=len(keys),mutation_checks=mutation_checks,corrupt_guard_checks=corrupt_guard_checks,
                max_reflections=max_bounces,cases=cases,types_proved=sum(c['conditional_lemma'] for c in cases),
                scope='Geometry-only sufficient midpoint cover. Feasible/capped branches unresolved; no whole-placement or darkness conclusion.')
    (OUT/'midpoint-extension-audit-2-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['cases','fixed_positive_controls','provenance']}),flush=True)


if __name__=='__main__':run()
