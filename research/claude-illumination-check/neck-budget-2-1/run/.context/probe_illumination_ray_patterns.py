"""Sample every remaining fan branch and compare exact connecting-ray patterns."""
from collections import Counter
from fractions import Fraction as F
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,solver_for
from illumination_geometry import owners_of
from illumination_paths import find_path,trace,room as prepare
from illumination_sector_paths import verify
from illumination_residual_fans import TARGET,SECOND_CELL,load_residual,fix_first,fan_masks
from search_illumination_one_exception import orbit,tile_facts
from search_illumination_three_two_star import room_from


def sample():
    model,ts,x,bounded,terms,keys,ids,residual,provenance=load_residual()
    second_ids,_=fan_masks(ts,SECOND_CELL);owners=owners_of(ts);solver=solver_for(10,127)
    records=[];branches=[];directions=set()
    for outside,mask in residual:
        branch=model.clone();fix_first(branch,terms,bounded,x,ids,outside,mask)
        status=solver.solve(branch);row=dict(outside_cells=outside,first_mask=mask,status=solver.status_name(status))
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            data=room_from(TARGET,ts,x,solver);witness=find_path(data,16,1000)
            if witness['status']!='illuminated':witness=find_path(data,32,2000)
            row['screen_status']=witness['status']
            if witness['status']=='illuminated':
                verify(data,witness);guards=[]
                for changed,ray in orbit(data,witness):
                    verify(changed,ray);facts=tile_facts(ts,owners,ray,changed)
                    guards.append(dict(room=changed,witness=ray,tile_facts=facts))
                selected={tuple(sorted(map(tuple,t))) for t in data['triangles']}
                second_mask=sum(1<<j for j,i in enumerate(second_ids) if ts[i] in selected)
                points=[tuple(F(*v) for v in p) for p in witness['path']]
                wall_word=[]
                walls,_=prepare(data)
                for p in points[1:-1]:
                    edges=[(a,b) for a,b in walls if (p[0]-a[0])*(b[1]-a[1])==(p[1]-a[1])*(b[0]-a[0]) and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))]
                    assert edges
                    a,b=edges[0];dx=b[0]-a[0];dy=b[1]-a[1]
                    wall_word.append('V' if not dx else 'H' if not dy else '+' if dx*dy>0 else '-')
                record=dict(room=data,witness=witness,derived_guards=guards,outside_cells=outside,first_mask=mask,second_mask=second_mask,reflection_word=''.join(wall_word))
                records.append(record);directions.add(tuple(witness['direction']))
                row.update(record_index=len(records)-1,second_mask=second_mask,direction=witness['direction'],bounces=witness['bounces'])
        branches.append(row);print(json.dumps(dict(event='pattern_sample',**row)),flush=True)
    coverage=[]
    for direction in sorted(directions):
        hits=[]
        for i,record in enumerate(records):
            result=trace(record['room'],direction,256)
            if result['status']=='illuminated':verify(record['room'],result);hits.append(i)
        coverage.append(dict(direction=direction,records=hits))
    missing=set(range(len(records)));greedy=[]
    while missing:
        chosen=max(coverage,key=lambda row:len(set(row['records'])&missing))
        assert set(chosen['records'])&missing
        greedy.append(dict(direction=chosen['direction'],newly_covered=sorted(set(chosen['records'])&missing)))
        missing-=set(chosen['records'])
    result=dict(provenance=provenance,branches=branches,records=records,direction_coverage=coverage,
                greedy_sample_cover=greedy,
                summary=dict(residual_branches=len(residual),sampled_rooms=len(records),distinct_first_directions=len(directions),greedy_directions=len(greedy),reflection_words=dict(Counter(r['reflection_word'] for r in records)),max_bounces=max((r['witness']['bounces'] for r in records),default=0),scope='One sampled room per feasible branch; exact ray cross-checks. Direction coverage of these samples is not a universal illumination lemma.'))
    (OUT/'ray-pattern-probe-2-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['summary']),flush=True)

def expand():
    path=OUT/'ray-pattern-probe-2-1.json'
    result=json.loads(path.read_text());records=result['records']
    frequencies=Counter(tuple(r['witness']['direction']) for name in ['fan-search-2-1.json','cell-search-2-1.json'] for r in json.loads((OUT/name).read_text())['records'])
    catalogue=set(d for d,_ in frequencies.most_common(48))|{tuple(r['witness']['direction']) for r in records}
    coverage=[];statuses=Counter()
    for n,direction in enumerate(sorted(catalogue),1):
        hits=[]
        for i,record in enumerate(records):
            ray=trace(record['room'],direction,64);statuses[ray['status']]+=1
            if ray['status']=='illuminated':verify(record['room'],ray);hits.append(i)
        coverage.append(dict(direction=direction,records=hits))
        if n%10==0:print(json.dumps(dict(event='expanded_directions',checked=n,total=len(catalogue))),flush=True)
    missing=set(range(len(records)));greedy=[]
    while missing:
        chosen=max(coverage,key=lambda row:len(set(row['records'])&missing));covered=set(chosen['records'])&missing
        assert covered;greedy.append(dict(direction=chosen['direction'],newly_covered=sorted(covered)));missing-=covered
    result['expanded_direction_coverage']=coverage;result['expanded_greedy_cover']=greedy
    result['summary']['expanded_catalogue_directions']=len(catalogue)
    result['summary']['expanded_greedy_directions']=len(greedy)
    result['summary']['expanded_trace_statuses']=dict(statuses)
    result['summary']['expanded_reflection_limit']=64
    path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['summary']),flush=True)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--expand',action='store_true');args=ap.parse_args()
    expand() if args.expand else sample()
