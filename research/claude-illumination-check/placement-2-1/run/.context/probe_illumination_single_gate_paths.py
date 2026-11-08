"""Test a finite catalogue for one-exception witnesses in saved multi-gate rooms."""
from collections import Counter
import hashlib
import json
from pathlib import Path
from illumination_cover import D4,mat
from illumination_exception_gate_bound import decide_direction
from analyze_illumination_exception_itineraries import independent_events,visits,unfolding_check
from illumination_sector_paths import verify
from illumination_paths import directions

OUT=Path(__file__).parent/'three-triples'

def run():
    source=OUT/'exception-itineraries-2-1.json';saved=json.loads(source.read_text());data={};counts=Counter()
    for name in ['ray-pattern-probe-2-1.json','double-fan-search-2-1.json']:
        data[name]=json.loads((OUT/name).read_text())
        counts.update(tuple(r['witness']['direction']) for r in data[name]['records'])
    directions={mat(g,d) for d in counts for g in D4}
    catalogue=sorted(directions,key=lambda d:(-counts[d],max(map(abs,d)),sum(map(abs,d)),d))[:128]
    cases=[];total_tests=0
    for row in saved['records']:
        if row['event_count']==1:continue
        room=data[row['source']]['records'][row['record_index']]['room'];found=None;outcomes=Counter()
        for direction in catalogue:
            result=decide_direction(room,direction);outcomes[result['status']]+=1;total_tests+=1
            if result['status']!='ILLUMINATED':continue
            witness=result['witness'];info=independent_events(witness,details=True)
            if len(info['events'])!=1:continue
            verify(room,witness);assert visits(room,witness)['event_count']==1
            bounds=unfolding_check(room,witness,info)
            found=dict(witness=witness,gate=info['events'][0]['point'],primitive_duration=bounds['primitive_duration']);break
        case=dict(source=row['source'],record_index=row['record_index'],neck_type=row['neck_type'],original_exception_events=row['event_count'],directions_tested=sum(outcomes.values()),outcomes=dict(outcomes),single_gate_witness=found)
        cases.append(case);print(json.dumps(dict(event='single_gate_probe',checked=len(cases),found=sum(bool(c['single_gate_witness']) for c in cases),directions_tested=total_tests)),flush=True)
    result=dict(status='BOUNDED_PROBE',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),catalogue=catalogue,cases=cases,
                summary=dict(multi_gate_rooms_tested=len(cases),single_gate_alternatives=sum(bool(c['single_gate_witness']) for c in cases),unresolved_for_single_gate=sum(c['single_gate_witness'] is None for c in cases),directions_per_room_limit=len(catalogue),total_direction_tests=total_tests),
                scope='No-new-room finite-direction probe. A failure means only no one-gate witness in the catalogue, never necessity of multiple gates or darkness.')
    (OUT/'single-gate-probe-2-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['summary']),flush=True)

def targeted():
    path=OUT/'single-gate-probe-2-1.json';saved=json.loads(path.read_text())
    cache={name:json.loads((OUT/name).read_text()) for name in ['ray-pattern-probe-2-1.json','double-fan-search-2-1.json']}
    catalogue=[d for d in directions(16) if list(d) not in saved['catalogue']]
    cases=[]
    for previous in saved['cases']:
        if previous['single_gate_witness'] is not None:continue
        room=cache[previous['source']]['records'][previous['record_index']]['room'];found=None;outcomes=Counter()
        for direction in catalogue:
            decision=decide_direction(room,direction);outcomes[decision['status']]+=1
            if decision['status']!='ILLUMINATED':continue
            ray=decision['witness'];events=independent_events(ray,details=True)
            if len(events['events'])!=1:continue
            verify(room,ray);assert visits(room,ray)['event_count']==1
            checked=unfolding_check(room,ray,events);assert checked['primitive_duration']==2
            found=dict(witness=ray,gate=events['events'][0]['point'],primitive_duration=2);break
        case=dict(source=previous['source'],record_index=previous['record_index'],neck_type=previous['neck_type'],directions_tested=sum(outcomes.values()),outcomes=dict(outcomes),single_gate_witness=found)
        cases.append(case);print(json.dumps(dict(event='targeted_single_gate',source=case['source'],record_index=case['record_index'],directions_tested=case['directions_tested'],found=bool(found))),flush=True)
    saved['targeted_follow_up']=dict(direction_bound=16,catalogue=catalogue,cases=cases,
        summary=dict(rooms=len(cases),new_single_pass_witnesses=sum(bool(c['single_gate_witness']) for c in cases),unresolved=sum(c['single_gate_witness'] is None for c in cases),direction_tests=sum(c['directions_tested'] for c in cases)))
    path.write_text(json.dumps(saved,indent=2)+'\n');print(json.dumps(saved['targeted_follow_up']['summary']),flush=True)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--targeted',action='store_true');args=ap.parse_args()
    targeted() if args.targeted else run()
