"""Extract sufficient guard subsets for the extension's audited neck lemmas."""
from collections import Counter
import json
from pathlib import Path
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT, digest, solver_for
from extend_illumination_midpoint_covers import PATH, load_base
from search_illumination_midpoint_covers import geometry_parent, fixed_neck
from search_illumination_three_two_star import add_guard
from analyze_illumination_exception_itineraries import independent_events
from audit_illumination_midpoint_covers import signature
from audit_illumination_three_two_star import touched_tiles
from illumination_geometry import owners_of
from search_illumination_one_exception import tile_facts
from search_illumination_midpoint_covers import one_pass


def reconcile(saved,base_guards,peer_guards):
    root=OUT.parent.parent
    manifest=json.loads((OUT/'midpoint-cover-proof-inputs-2-1.json').read_text())
    old_rooms=set();old_guards=set()
    def room_key(room):
        return tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))
    def guard_key(g):
        return tuple(sorted(map(tuple,g['tile_facts'])))
    for name in manifest['paths']:
        if not name.endswith('.json'):continue
        d=json.loads((root/name).read_text())
        if not isinstance(d,dict):continue
        records=d.get('records',[])
        if isinstance(records,list):
            for r in records:
                room=r.get('room',{})
                if room.get('marked')==[[0,0],[4,2]]:
                    old_rooms.add(room_key(room))
                    if '/three-triples/' in name or name.endswith('/case-2-1.json'):
                        old_guards.update(guard_key(g) for g in r.get('derived_guards',[]))
        if name.endswith('/case-2-1.json'):
            old_guards.update(guard_key(g) for g in d.get('seeds',[]))
    old_guards.update(guard_key(g) for g in base_guards)
    assert len(old_guards)==3793
    learned={guard_key(g) for r in saved['records'] for g in r['derived_guards']}
    peer={guard_key(g) for g in peer_guards}
    rooms={room_key(r['room']) for r in saved['records']}
    return dict(prior_matching_geometries=len(old_rooms),prior_unique_guards=len(old_guards),
                processed_geometries=len(rooms),new_geometries=len(rooms-old_rooms),revisited_geometries=len(rooms & old_rooms),
                learned_guards=len(learned),new_learned_guards=len(learned-old_guards),
                peer_seed_guards=len(peer),new_peer_seed_guards=len(peer-old_guards),
                total_new_unique_guards=len((learned|peer)-old_guards))


def run():
    saved=json.loads(PATH.read_text())
    audit_path=OUT/'midpoint-extension-audit-2-1.json'
    audit=json.loads(audit_path.read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(PATH)
    _,ts,_,_,_,_,_,_,_,base_guards,peer_guards,provenance=load_base()
    assert saved['provenance']==provenance
    guards=base_guards+peer_guards+[g for r in saved['records'] for g in r['derived_guards']]
    for g in peer_guards:
        one_pass(g['room'],g['witness'])
        facts=tile_facts(ts,owners_of(ts),g['witness'],g['room'])
        assert facts==g['tile_facts']
        required=touched_tiles(ts,g['witness']);fixed=dict(facts)
        selected={tuple(sorted(map(tuple,t))) for t in g['room']['triangles']}
        assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
    results=[]
    for case in audit['cases']:
        if not case['conditional_lemma'] or case['neck_type']==7:
            continue
        n=case['neck_type']
        model,ts,x,bounded,terms,first,second,patterns=geometry_parent()
        pattern=patterns[n-1]
        fixed_neck(model,terms,bounded,x,first,second,pattern)
        constants={}
        outside=set(map(tuple,pattern[0]))
        for i,t in enumerate(ts):
            center=next(p for p in t if not(p[0]%2 or p[1]%2));cell=(center[0]//2,center[1]//2)
            if cell in bounded['full']:constants[i]=1
            elif cell not in bounded['mandatory'] and cell not in outside:constants[i]=0
        for ids,mask in [(first,pattern[1]),(second,pattern[2])]:
            for j,i in enumerate(ids):constants[i]=(mask>>j)&1
        compatible=[i for i,g in enumerate(guards) if all(j not in constants or constants[j]==v for j,v in g['tile_facts'])]
        control_index=next(i for i,g in enumerate(guards) if signature(g['room'],ts,first,second,bounded)==(tuple(map(tuple,pattern[0])),pattern[1],pattern[2]))
        control=model.clone();selected={tuple(sorted(map(tuple,t))) for t in guards[control_index]['room']['triangles']}
        for t,v in zip(ts,x):control.add(v==int(t in selected))
        solver=solver_for(60,239);solver.parameters.cp_model_presolve=False;solver.parameters.num_search_workers=1
        assert solver.solve(control) in (cp_model.OPTIMAL,cp_model.FEASIBLE)
        candidate=model.clone();assumptions={}
        for i in compatible:
            a=candidate.new_bool_var(f'guard_{i}')
            candidate.add(sum(1-x[j] if v else x[j] for j,v in guards[i]['tile_facts'])>=1).only_enforce_if(a)
            candidate.add_assumption(a);assumptions[a.index]=i
        status=solver.solve(candidate)
        result=dict(neck_type=n,pattern=pattern,compatible_guards=len(compatible),assumption_status=solver.status_name(status),positive_control_guard=control_index,positive_control_status='ACCEPTED',core_is_minimum=False)
        if status==cp_model.INFEASIBLE:
            core=[assumptions[l] for l in solver.sufficient_assumptions_for_infeasibility()]
            replay=model.clone()
            for i in core:add_guard(replay,x,guards[i]['tile_facts'])
            status=solver.solve(replay);assert status==cp_model.INFEASIBLE
            result.update(core_guard_indices=core,core_size=len(core),core_replay=solver.status_name(status),
                          midpoint_gates=dict(Counter(str(independent_events(guards[i]['witness'])[0]) for i in core)))
        results.append(result);print(json.dumps(result),flush=True)
    result=dict(status='PASS',source_sha256=digest(PATH),audit_sha256=digest(audit_path),
                guard_index_order='Frozen base seed guards, frozen base record guards, extension peer guards, extension record guards',
                cases=results,peer_seed_independent_checks=len(peer_guards),dedup=reconcile(saved,base_guards,peer_guards),scope='Sufficient core subsets only; solver timeouts do not affect the full-catalogue audited lemmas.')
    (OUT/'midpoint-extension-core-2-1.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':run()
