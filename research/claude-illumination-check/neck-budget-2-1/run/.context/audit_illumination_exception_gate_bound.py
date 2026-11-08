"""Check the affine gate bound and independently replay directional decisions."""
from collections import Counter
import hashlib
import json
from pathlib import Path
from illumination_geometry import owners_of,label
from illumination_family_bound import triangles_in_cells
from illumination_three_two_star_bound import complete_support
from illumination_group import reflection
from illumination_cover import D4,mul
from illumination_paths import directions
from illumination_sector_paths import trace,verify
from illumination_exception_gate_bound import parameters,decide_direction
from analyze_illumination_exception_itineraries import independent_events,visits,unfolding_check

OUT=Path(__file__).parent/'three-triples'

def audit():
    ts=triangles_in_cells(complete_support((2,1))['allowed']);edges=owners_of(ts)
    for e in edges:
        affine=reflection(e);assert affine[:4] in D4 and affine[4]%2==affine[5]%2==0
        for p in [(0,0),(0,1),(1,0),(1,1)]:
            transformed=(affine[0]*p[0]+affine[1]*p[1]+affine[4],affine[2]*p[0]+affine[3]*p[1]+affine[5])
            assert label(transformed)==label(p)
    for g in D4:
        for h in D4:assert mul(g,h) in D4
    sources={};rooms=[];positive=0;max_reflections=0;max_budget=0
    for name in ['ray-pattern-probe-2-1.json','double-fan-search-2-1.json']:
        path=OUT/name;sources[name]=hashlib.sha256(path.read_bytes()).hexdigest()
        for record in json.loads(path.read_text())['records']:
            room=record['room'];witness=record['witness'];verify(room,witness)
            bounds=parameters(room,witness['direction']);decision=decide_direction(room,witness['direction']);assert decision['status']=='ILLUMINATED'
            assert witness['bounces']<=bounds['reflection_bound']
            independent=trace(room,bounds['direction'],max_events=bounds['reflection_bound']+2)
            assert independent['status']=='illuminated';verify(room,independent)
            rooms.append(room);positive+=1;max_reflections=max(max_reflections,witness['bounces']);max_budget=max(max_budget,bounds['reflection_bound'])
        print(json.dumps(dict(event='gate_bound_positive_replay',source=name,checked=positive)),flush=True)
    direction_checks=0;direction_outcomes=Counter();limit_negatives=0
    for room in [rooms[i] for i in [0,17,42,73,111,146]]:
        for direction in directions(3):
            result=decide_direction(room,direction);bounds=result['bounds'];other=trace(room,bounds['direction'],max_events=bounds['reflection_bound']+2)
            assert (result['status']=='ILLUMINATED')==(other['status']=='illuminated')
            if other['status']=='illuminated':verify(room,other)
            assert other['status'] in ('illuminated','corner','periodic','limit')
            direction_outcomes[result['status']]+=1;direction_checks+=1
            limit_negatives+=other['status']=='limit'
    probe_path=OUT/'single-gate-probe-2-1.json';probe=json.loads(probe_path.read_text());sources[probe_path.name]=hashlib.sha256(probe_path.read_bytes()).hexdigest()
    itinerary_path=OUT/'exception-itineraries-2-1.json';itineraries=json.loads(itinerary_path.read_text())
    assert probe['source_sha256']==hashlib.sha256(itinerary_path.read_bytes()).hexdigest()
    replayed_single=0;catalogue_checks=0;single_keys={(r['source'],r['record_index']) for r in itineraries['records'] if r['event_count']==1}
    cache={name:json.loads((OUT/name).read_text()) for name in ['ray-pattern-probe-2-1.json','double-fan-search-2-1.json']}
    def replay_single_cases(cases,catalogue):
        nonlocal replayed_single,catalogue_checks
        for case in cases:
            room=cache[case['source']]['records'][case['record_index']]['room'];found=None;outcomes=Counter()
            for direction in catalogue:
                bounds=parameters(room,direction);ray=trace(room,bounds['direction'],max_events=bounds['reflection_bound']+2);catalogue_checks+=1
                outcomes['ILLUMINATED' if ray['status']=='illuminated' else 'NOT_ILLUMINATED_IN_DIRECTION']+=1
                if ray['status']!='illuminated':continue
                verify(room,ray);events=independent_events(ray,details=True)
                if len(events['events'])!=1:continue
                assert visits(room,ray)['event_count']==1
                checked=unfolding_check(room,ray,events);assert checked['primitive_duration']==2
                found=ray;break
            assert bool(found)==bool(case['single_gate_witness']) and dict(outcomes)==case['outcomes']
            assert sum(outcomes.values())==case['directions_tested']
            if found:
                verify(room,case['single_gate_witness']['witness']);assert len(independent_events(case['single_gate_witness']['witness']))==1
                replayed_single+=1;single_keys.add((case['source'],case['record_index']))
    replay_single_cases(probe['cases'],probe['catalogue'])
    assert catalogue_checks==probe['summary']['total_direction_tests']
    follow=probe['targeted_follow_up'];before=catalogue_checks
    replay_single_cases(follow['cases'],follow['catalogue'])
    assert catalogue_checks-before==follow['summary']['direction_tests']
    relevant=[r for r in itineraries['records'] if r['neck_type'] is not None]
    relevant_single=sum((r['source'],r['record_index']) in single_keys for r in relevant)
    print(json.dumps(dict(event='single_gate_probe_replay',directions=catalogue_checks,new_single_pass_witnesses=replayed_single)),flush=True)
    control=Path(__file__).parent/'illumination-search-simple-unrestricted.json';data=json.loads(control.read_text());sources[str(control.name)]=hashlib.sha256(control.read_bytes()).hexdigest()
    strict_checks=0
    for direction in directions(3):
        result=decide_direction(data,direction);assert result['status']=='NOT_ILLUMINATED_IN_DIRECTION' and result['bounds']['exception_visit_bound']==0
        strict_checks+=1
    rejected=0
    for altered,direction in [(rooms[0],(0,0)),(dict(rooms[0],slits=[[[0,0],[1,0]]]),(1,2)),(dict(rooms[0],marked=[[0,0],[1,1]]),(1,2))]:
        try:parameters(altered,direction)
        except (ValueError,AssertionError):rejected+=1
        else:raise AssertionError('unsupported input accepted')
    assert rejected==3
    assert sum(direction_outcomes.values())==direction_checks
    result=dict(status='PASS',affine_edges_checked=len(edges),parity_classes_per_edge=4,point_group_products=64,
                positive_paths=positive,independent_single_gate_catalogue_replays=catalogue_checks,new_single_pass_witnesses=replayed_single,saved_rooms_with_single_pass_witness=len(single_keys),current_neck_sample_rooms=len(relevant),current_neck_rooms_with_single_pass_witness=relevant_single,independent_direction_checks=direction_checks,directional_outcomes=dict(direction_outcomes),
                independent_trace_limits=limit_negatives,strict_dark_direction_controls=strict_checks,rejected_inputs=rejected,
                max_saved_reflections=max_reflections,max_directional_reflection_budget=max_budget,sources=sources,
                scope='One-direction decision and elementary affine/parity/state bound only. No finite primitive-direction catalogue covers all directions; no new global minimum, room exclusion or dark construction.')
    (OUT/'gate-bound-audit-2-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':audit()
