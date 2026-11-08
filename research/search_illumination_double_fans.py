"""Bounded complete second-cell refinement; only verified positive-ray cuts."""
import argparse
from collections import Counter
import json
import time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,digest,solver_for
from illumination_geometry import owners_of
from illumination_paths import find_path,trace,room as prepare
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from illumination_residual_fans import TARGET,SECOND_CELL,load_residual,fix_first,fan_masks,fix_fan
from search_illumination_one_exception import orbit,tile_facts
from search_illumination_three_two_star import add_guard,room_from

PATH=OUT/'double-fan-search-2-1.json'

def load_base():
    model,ts,x,bounded,terms,keys,ids,residual,provenance=load_residual()
    probe_path=OUT/'ray-pattern-probe-2-1.json';probe=json.loads(probe_path.read_text())
    assert probe['provenance']==provenance
    for record in probe['records']:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']))
            if key not in keys:keys.add(key);add_guard(model,x,guard['tile_facts'])
    provenance=dict(parent=provenance,probe_sha256=digest(probe_path))
    library=[tuple(row['direction']) for row in probe.get('expanded_greedy_cover',probe['greedy_sample_cover'])][:5]
    return model,ts,x,bounded,terms,keys,ids,residual,provenance,library

def run(seconds,final_seconds):
    begin=time.monotonic();model,ts,x,bounded,terms,keys,ids,residual,provenance,library=load_base()
    second_ids,masks=fan_masks(ts,SECOND_CELL);seed_count=len(keys)
    previous=json.loads(PATH.read_text()) if PATH.exists() else None
    if previous:assert previous['provenance']==provenance
    records=previous['records'] if previous else []
    prior={(tuple(map(tuple,c['outside_cells'])),c['first_mask'],c['second_mask']):c for c in previous['classes']} if previous else {}
    for record in records:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']));assert key not in keys
            keys.add(key);add_guard(model,x,guard['tile_facts'])
    outcomes=[];solver=solver_for(seconds,139);solver.parameters.cp_model_presolve=False;owners=owners_of(ts);global_status=None
    def save():
        visited={(tuple(map(tuple,c['outside_cells'])),c['first_mask'],c['second_mask']) for c in outcomes}
        retained=outcomes+[c for k,c in prior.items() if k not in visited]
        summary=dict(target_A_cell=TARGET,second_cell=SECOND_CELL,second_triangle_ids=second_ids,masks=masks,
                     cp_model_presolve=False,first_residual_branches=len(residual),partition_size=len(residual)*len(masks),visited=len(retained),
                     excluded=sum(c['exhausted'] for c in retained),records=len(records),new_guards=len(keys)-seed_count,
                     witness_sources=dict(Counter(r['witness_source'] for r in records)),library_directions=library,
                     global_status=solver.status_name(global_status) if global_status is not None else 'NOT_SOLVED',seconds=time.monotonic()-begin)
        temp=PATH.with_suffix('.tmp');temp.write_text(json.dumps(dict(summary=summary,provenance=provenance,classes=retained,records=records),indent=2)+'\n');temp.replace(PATH)
        return summary
    for outside,first_mask in residual:
        for second_mask in masks:
            key=(outside,first_mask,second_mask)
            if prior.get(key,{}).get('exhausted'):outcomes.append(prior[key]);continue
            branch=model.clone();fix_first(branch,terms,bounded,x,ids,outside,first_mask);fix_fan(branch,x,second_ids,second_mask)
            start=time.monotonic();status=None;survivor=None;before=len(records)
            while time.monotonic()-start<seconds:
                solver.parameters.max_time_in_seconds=max(.001,seconds-(time.monotonic()-start));status=solver.solve(branch)
                if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
                data=room_from(TARGET,ts,x,solver);witness=None;source='library';prepared=prepare(data)
                for direction in library:
                    ray=trace(data,direction,128,prepared)
                    if ray['status']=='illuminated':witness=ray;break
                if witness is None:source='fallback';witness=find_path(data,16,1000)
                if witness['status']!='illuminated':witness=find_path(data,32,2000)
                if witness['status']!='illuminated':survivor=dict(room=data,bounded_screen=witness);break
                verify(data,witness);guards=[]
                for changed,ray in orbit(data,witness):
                    verify(changed,ray);facts=tile_facts(ts,owners,ray,changed);key=tuple(facts)
                    if key in keys:continue
                    keys.add(key);guards.append(dict(room=changed,witness=ray,tile_facts=facts));add_guard(model,x,facts);add_guard(branch,x,facts)
                assert guards
                records.append(dict(room=data,witness=witness,counts=validate(data,TARGET),outside_cells=outside,first_mask=first_mask,second_mask=second_mask,witness_source=source,derived_guards=guards))
            outcomes.append(dict(outside_cells=outside,first_mask=first_mask,second_mask=second_mask,status=solver.status_name(status) if status is not None else 'NOT_SOLVED',exhausted=status==cp_model.INFEASIBLE,new_records=len(records)-before,seconds=time.monotonic()-start,survivor=survivor))
            summary=save()
            if len(outcomes)%20==0 or survivor:print(json.dumps(dict(event='double_fan_branch',visited=summary['visited'],excluded=summary['excluded'],records=summary['records'],case_index=len(outcomes),partition_size=summary['partition_size'])),flush=True)
    solver.parameters.max_time_in_seconds=final_seconds;global_status=solver.solve(model)
    print(json.dumps(dict(event='double_fan_complete',**save())),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=1);ap.add_argument('--final-seconds',type=float,default=20)
    args=ap.parse_args();run(args.seconds,args.final_seconds)
