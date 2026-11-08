"""Reconcile historical cuts and independently classify the marked-star hub."""
from collections import Counter
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_midpoint_1_1 import load_base,PATH,TARGET
from search_illumination_three_two_star import make_model,add_guard,room_from
from illumination_geometry import owners_of,local_sectors
from illumination_sector_paths import verify
from illumination_paths import trace
from search_illumination_one_exception import tile_facts
from audit_illumination_three_two_star import touched_tiles
from illumination_triple_cell_sets import refine_connected_cells
from illumination_cover import D4,mat


def run():
    manifest=json.loads((OUT/'mask12-proof-inputs-2-1.json').read_text())
    for name,h in manifest['sha256'].items():assert digest(BASE.parent/name)==h,name
    current=json.loads(PATH.read_text());audit=json.loads((OUT/'midpoint-audit-1-1.json').read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(PATH)
    model,ts,x,bounded,terms,keys,seeds,prov=load_base();assert prov==current['provenance']
    original=set(keys);new_phase=set()
    for g in current['seed_guards']+[g for r in current['records'] for g in r['derived_guards']]:
        key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);new_phase.add(key);add_guard(model,x,key)
    owners=owners_of(ts);earlier=json.loads((OUT/'connected-search-1-1.json').read_text())
    assert earlier['summary']['provenance']==prov['parent']
    old_keys=set();added=[]
    for r in earlier['records']:
        for g in r['derived_guards']:
            key=tuple(map(tuple,g['tile_facts']));old_keys.add(key)
            if key in keys:continue
            room,w=g['room'],g['witness'];verify(room,w);facts=tile_facts(ts,owners,w,room)
            assert facts==list(map(tuple,g['tile_facts']))
            required=touched_tiles(ts,w);fixed=dict(facts);selected={tuple(sorted(map(tuple,t))) for t in room['triangles']}
            assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
            keys.add(key);add_guard(model,x,facts);added.append(g)
    assert len(old_keys)==earlier['summary']['additional_cuts']==626
    print(json.dumps(dict(event='reconciled',phase_guards=len(new_phase),earlier_overlap=len(new_phase&old_keys),restored_guards=len(added),combined_guards=len(keys))),flush=True)
    refine_connected_cells(TARGET,model,terms)
    # Independent cycle connectivity at the shared physical B vertex.
    hub=(1,1);ids=[i for i,t in enumerate(ts) if hub in t];assert len(ids)==8
    forced={j for j,i in enumerate(ids) if (0,0) in ts[i] or (2,2) in ts[i]};assert len(forced)==4
    adjacent={j:set() for j in range(8)}
    for edge,os in owners_of([ts[i] for i in ids]).items():
        if hub in edge and len(os)==2:a,b=os;adjacent[a].add(b);adjacent[b].add(a)
    assert all(len(v)==2 for v in adjacent.values())
    masks=[]
    for mask in range(256):
        chosen={j for j in range(8) if mask>>j&1}
        if not forced<=chosen:continue
        seen={min(chosen)};todo=list(seen)
        for j in todo:
            for k in adjacent[j]&chosen-seen:seen.add(k);todo.append(k)
        if seen==chosen:masks.append(mask)
    geometric=[]
    for mask in range(256):
        if not all(mask>>j&1 for j in forced):continue
        chosen=[ts[i] for j,i in enumerate(ids) if mask>>j&1];os=owners_of(chosen);opened={e for e,own in os.items() if len(own)==2}
        sectors,full=local_sectors(chosen,hub,opened)
        if len(sectors)<=1:geometric.append(mask)
    assert masks==geometric and len(masks)==7
    bare,bts,bx,bb,bt=make_model(TARGET);assert ts==bts
    def fix(m,variables,mask):
        for j,i in enumerate(ids):m.add(variables[i]==(mask>>j&1))
    solver=solver_for(30,317);solver.parameters.cp_model_presolve=False
    control=bare.clone();fix(control,bx,255);status=solver.solve(control)
    assert status in (cp_model.OPTIMAL,cp_model.FEASIBLE),'full hub needs a positive geometry control'
    room=room_from(TARGET,ts,bx,solver);ray=trace(room,(1,1),2);assert ray['status']=='illuminated' and ray['bounces']==0;verify(room,ray)
    facts=tile_facts(ts,owners,ray,room);required=touched_tiles(ts,ray);assert required<=dict(facts).keys()
    forced_tiles={i for i,t in enumerate(ts) if (0,0) in t or (2,2) in t or i in ids}
    assert all(i in forced_tiles and v==1 for i,v in facts)
    direct_key=tuple(facts);direct_new=direct_key not in keys
    if direct_new:keys.add(direct_key);add_guard(model,x,facts)
    direct=dict(room=room,witness=ray,tile_facts=facts,added_new_guard=direct_new)
    # Classify the six non-full masks under the exact mark stabilizer.
    permutations=[];T=(2,2)
    for g in D4:
        for swap in (False,True):
            if mat(g,T)!=tuple(-v if swap else v for v in T):continue
            shift=T if swap else (0,0)
            def transform(p):
                q=mat(g,p);return tuple(q[k]+shift[k] for k in (0,1))
            permutations.append([ids.index(ts.index(tuple(sorted(transform(p) for p in ts[i])))) for i in ids])
    move=lambda mask,p:sum(1<<p[j] for j in range(8) if mask>>j&1)
    orbits={tuple(sorted({move(mask,p) for p in permutations})) for mask in masks if mask!=255}
    assert len(orbits)==2 and set().union(*map(set,orbits))==set(masks)-{255}
    cases=[]
    for mask in masks:
        branch=model.clone();fix(branch,x,mask);solver.parameters.max_time_in_seconds=15;status=solver.solve(branch)
        if mask==255:assert status==cp_model.INFEASIBLE
        cases.append(dict(mask=mask,selected_triangles=mask.bit_count(),status=solver.status_name(status)))
        print(json.dumps(dict(event='hub_replay',**cases[-1])),flush=True)
    solver.parameters.max_time_in_seconds=30;status=solver.solve(model)
    result=dict(status='PASS',current_audit_sha256=digest(OUT/'midpoint-audit-1-1.json'),prior_source_sha256=digest(OUT/'connected-search-1-1.json'),
                original_base_guards=len(original),phase_guards=len(new_phase),overlap_with_earlier_extension=len(new_phase&old_keys),
                globally_new_phase_guards=len(new_phase-old_keys),restored_historical_guards=len(added),restored_guards=added,
                total_guards=len(keys),connectivity_table_sets=2530,hub_point=hub,hub_triangle_ids=ids,forced_bits=sorted(forced),
                complete_hub_masks=masks,nonfull_symmetry_orbits=sorted(orbits),symmetry_permutations=permutations,
                full_hub_control='ACCEPTED',full_hub_direct_ray=direct,cases=cases,composed_parent=solver.status_name(status),
                placement_excluded=status==cp_model.INFEASIBLE or all(c['status']=='INFEASIBLE' for c in cases),
                scope='Exact historical cut reconciliation; complete local hub mask partition with independently checked adjacency and mark symmetry. Connected-cell table is the previously audited necessary refinement. Finite solver caps unresolved; no universal one-pass theorem.')
    (OUT/'hub-analysis-1-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['restored_guards','full_hub_direct_ray','symmetry_permutations']}),flush=True)


if __name__=='__main__':run()
