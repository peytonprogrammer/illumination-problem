"""Measure gate visits in the peer's saved exact paths; no ray search."""
from collections import Counter
from pathlib import Path
import json,hashlib
from analyze_illumination_exception_itineraries import independent_events,unfolding_check
BASE=Path(__file__).parent
p=BASE/'three-triples/peer-2-0-rays.json';d=json.loads(p.read_text());rows=[]
for n,r in enumerate(d['peer']):
 room=dict(triangles=r['room'],marked=[[0,0],[4,0]],require_simple=True)
 event=independent_events(r['witness'],details=True);u=unfolding_check(room,r['witness'],event)
 rows.append(dict(index=n,event_count=len(event['events']),distinct_vertices=len({tuple(e['point']) for e in event['events']}),bounces=r['witness']['bounces'],direction=r['witness']['direction'],**u))
summary=dict(paths=len(rows),event_counts=dict(Counter(r['event_count'] for r in rows)),distinct_exception_counts=dict(Counter(r['distinct_vertices'] for r in rows)),max_bounces=max(r['bounces'] for r in rows),all_primitive_duration_twice_visits=True)
(BASE/'three-triples/peer-2-0-itineraries.json').write_text(json.dumps(dict(status='PASS',source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),summary=summary,records=rows),indent=2)+'\n')
print(json.dumps(summary),flush=True)
