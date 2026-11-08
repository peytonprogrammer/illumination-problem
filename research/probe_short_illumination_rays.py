"""Compare exact ray guard sizes on four fixed positive configurations."""
import hashlib
import json
from pathlib import Path

from illumination_family_bound import triangles_in_cells
from illumination_three_two_star_bound import complete_support
from illumination_geometry import owners_of
from illumination_paths import directions, trace, room as prepare
from illumination_sector_paths import verify
from search_illumination_one_exception import tile_facts

D=Path(__file__).parent/'three-triples'
source=D/'short-ray-probe-input.json'
data=json.loads(source.read_text())
ts=triangles_in_cells(complete_support((2,1))['allowed'])
owners=owners_of(ts)
chosen=[]
seen=set()
for index,record in enumerate(data['records']):
    key=tuple(map(tuple,record['outside_cells']))
    if key in seen or record['witness']['bounces']<4:continue
    chosen.append((index,record));seen.add(key)
    if len(chosen)==4:break
results=[]
for index,record in chosen:
    room=record['room'];original=record['witness']
    old=tile_facts(ts,owners,original,room)
    prepared=prepare(room)
    candidates=[]
    for direction in directions(8):
        ray=trace(room,direction,64,prepared)
        if ray['status']!='illuminated':continue
        verify(room,ray)
        facts=tile_facts(ts,owners,ray,room)
        candidates.append(dict(direction=direction,bounces=ray['bounces'],guard_size=len(facts),
                               strict_subset_of_original=set(facts)<set(old),witness=ray))
    best=min(candidates,key=lambda r:(r['guard_size'],r['bounces'])) if candidates else None
    row=dict(record_index=index,outside_cells=record['outside_cells'],old_guard_size=len(old),
             old_bounces=original['bounces'],positive_rays=len(candidates),best=best,
             strict_subset_rays=sum(r['strict_subset_of_original'] for r in candidates))
    results.append(row)
    print(json.dumps({k:v for k,v in row.items() if k!='best'}|{'best_guard_size':best['guard_size'] if best else None}),flush=True)
out=dict(status='PASS',direction_bound=8,max_reflections=64,input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),cases=results,
         scope='Exact positive rays only. Fewer guard bits alone do not establish dominance; strict subset checks do. No negative conclusions from finite misses.')
(D/'short-ray-probe.json').write_text(json.dumps(out,indent=2)+'\n')
