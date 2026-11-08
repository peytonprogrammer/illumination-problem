"""Compare verified saved witnesses, without a new room or direction search."""
from collections import Counter
import json
from pathlib import Path
from analyze_illumination_exception_itineraries import independent_events,unfolding_check
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from classify_illumination_three_exception import OUT,digest


def run():
    results=[]
    for target in [(1,1),(2,0)]:
        source=OUT.parent/'three-two-star'/f'case-{target[0]}-{target[1]}.json'
        saved=json.loads(source.read_text());events=Counter();duration=Counter();directions=Counter();rows=[]
        for i,record in enumerate(saved['records']):
            room=record['room'];w=record['witness'];validate(room,target);verify(room,w)
            ev=independent_events(w);events[len(ev)]+=1;directions[tuple(w['direction'])]+=1
            single=None
            if len(ev)==1:
                single=unfolding_check(room,w,independent_events(w,details=True))['primitive_duration']
                duration[str(single)]+=1
            rows.append(dict(record_index=i,exception_events=len(ev),single_event_duration=single,bounces=w['bounces']))
        results.append(dict(target_A_cell=target,source=str(source.relative_to(OUT.parent.parent)),source_sha256=digest(source),
                            verified_records=len(rows),event_counts=dict(events),single_event_durations=dict(duration),
                            max_bounces=max(r['bounces'] for r in rows),records=rows))
    data=dict(status='PASS',cases=results,scope='Saved witness sample only. Multiple events in a saved witness do not exclude a different single-event path. No new directional scan, geometry enumeration, darkness claim or placement exclusion.')
    (OUT/'remaining-gates.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',cases=[{k:v for k,v in r.items() if k!='records'} for r in results])),flush=True)


if __name__=='__main__':run()
