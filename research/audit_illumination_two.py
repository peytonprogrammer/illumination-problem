"""Independent audit of the completed two-transparent-vertex room search."""
import json,sys
from collections import Counter
from pathlib import Path
from illumination_geometry import check,patch,owners_of,edge,save
from illumination_symmetry import orbit
from illumination_path_cuts import path_facts
from verify_illumination_paths import verify

base=Path(__file__).parent
name=sys.argv[1] if len(sys.argv)>1 else 'transparent-simple-two-symmetric'
run=json.loads((base/(name+'-screen.json')).read_text());summary=run['summary'];records=run['records']
assert summary['args']['bounds']==[-2,6,-2,2] and summary['args']['target']==[4,0]
assert summary['args']['transparent_budget']==2 and summary['args']['max_walls']==23 and summary['args']['simple']
ts=patch(-2,6,-2,2);legal=set(ts);owners=owners_of(ts);shared={e:os for e,os in owners.items() if len(os)==2}
paths=0;cuts=0;geometries=set();mutations=0;cut_sizes=[];walls=Counter();bad=Counter()
for index,record in enumerate(records):
    data=record['room'];witness=record['witness'];r=check(data,strict=False)
    assert r['simple_polygon'] and r['walls']<=23 and 1<=len(r['transparent_vertices'])<=2
    assert data['marked']==[[0,0],[4,0]] and not data['slits']
    assert {tuple(sorted(map(tuple,t))) for t in data['triangles']}<=legal
    assert r['walls']==record['walls'] and sorted(map(tuple,r['transparent_vertices']))==sorted(map(tuple,record['transparent']))
    key=tuple(sorted(tuple(sorted(map(tuple,t))) for t in data['triangles']));geometries.add(key);walls[r['walls']]+=1;bad[len(r['transparent_vertices'])]+=1
    for changed,ray in orbit(data,witness):
        check(changed,strict=False);verify(changed,ray);paths+=1
        chosen={tuple(sorted(map(tuple,t))) for t in changed['triangles']};selected=[int(t in chosen) for t in ts];opened={e:int(all(ts[i] in chosen for i in os)) for e,os in shared.items()}
        facts=path_facts(ts,owners,shared,ray,selected,opened);cuts+=1;cut_sizes.append(len(facts))
        # Test all tile flips outside the cut's facts for 20 new two-exception records.
        if len(r['transparent_vertices'])==2 and 165<=index<185:
            for i,t in enumerate(ts):
                if ('tile',i) in facts:continue
                modified=chosen^{t};ns=[int(t in modified) for t in ts];no={e:int(all(ts[j] in modified for j in os)) for e,os in shared.items()}
                if not all((ns[k] if kind=='tile' else no[k])==v for (kind,k),v in facts.items()):continue
                verify(dict(changed,triangles=list(modified)),ray);mutations+=1
    if (index+1)%50==0:print(json.dumps(dict(event='audit_progress',records=index+1,exact_paths=paths,cuts_rebuilt=cuts,mutations=mutations)),flush=True)
control=json.loads((base/'transparent-two-zero-control-result.json').read_text());assert control['status']=='INFEASIBLE' and control['exhausted']
known=json.loads((base/'illumination-search-simple-unrestricted.json').read_text());kr=check(known)
assert kr['simple_polygon'] and kr['walls']==24 and known['marked']==[[0,0],[4,0]] and {tuple(sorted(map(tuple,t))) for t in known['triangles']}<=legal
result=dict(status='PASS',run=name,solver_status=summary['status'],exhausted=summary['exhausted'],stop_reason=summary.get('stop_reason'),records=len(records),distinct_geometries=len(geometries),transparency_counts=dict(bad),wall_counts=dict(walls),independent_exact_paths_verified=paths,path_cuts_rebuilt=cuts,unrelated_tile_mutations_preserving_paths=mutations,smallest_cut_facts=min(cut_sizes),largest_cut_facts=max(cut_sizes),max_reflections=max(r['witness']['bounces'] for r in records),max_direction_coordinate=max(max(map(abs,r['witness']['direction'])) for r in records),zero_exception_control='INFEASIBLE',matching_24_wall_control='PASS',bounded_minimum=24 if summary['exhausted'] else None,scope=dict(bounds=[-2,6,-2,2],source=[0,0],target=[4,0],max_transparent_vertices=2,simple=True))
save(base/'transparent-two-final-audit.json',result);print(json.dumps(result,indent=2))
