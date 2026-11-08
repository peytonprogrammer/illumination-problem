"""Audit saved pilot outputs only. No SAT, ray or orbit search is rerun."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib
import json
import sys

R=Path(__file__).parent
sys.path.insert(0,str(R/'inputs'))
import illumination_geometry as frozen
from guard_check import check as audit
from geometry import inspect,replay

D=json.loads((R/'result.json').read_text());C=json.loads((R/'case.json').read_text())
controls=json.loads((R/'controls.json').read_text());assert controls['status']=='PASS'
assert D['case']['case_id']==C['marked']['case_id']=='I2_1_1_p00'
assert D['stop_reason']=='VALID_ROOM_CAP_REACHED'
E=[json.loads(line) for line in (R/'events.jsonl').read_text().splitlines()]
G=[json.loads(line) for line in (R/'guards.jsonl').read_text().splitlines()]
assert len(E)==len(G)==len(D['events'])==30
assert E==D['events'] and len({e['model'] for e in E})==30
assert len(list((R/'models').glob('model-*.json')))==30
assert len(list((R/'paths').glob('model-*.json')))==30
seen=set();method=Counter();walls=Counter();triangles=Counter();reflections=[]
seconds=0;direction_tests=0;states=0
for event,guard in zip(E,G):
    tag=event['model'];assert guard['model']==tag
    room=json.loads((R/'models'/f'{tag}.json').read_text())
    path=json.loads((R/'paths'/f'{tag}.json').read_text())
    assert path['status']=='LIT'
    cells=set(map(tuple,room['cells']));key=tuple(sorted(cells));assert key not in seen;seen.add(key)
    geometry=inspect(cells,room['marks']);assert json.loads(json.dumps(geometry))==room['geometry']
    assert geometry['k']==7 and geometry['walls']<=20 and geometry['triangles']<=42
    assert geometry['interior_A']==[(0,0),(2,2)]
    f=frozen.check({'triangles':room['triangles'],'marked':room['marks'],'require_simple':True},strict=False)
    assert f['walls']==geometry['walls'] and f['simple_polygon']
    assert set(map(tuple,f['transparent_vertices']))==set(geometry['exceptions'])
    n=replay(geometry['vertices'],*room['marks'],path['path'])
    assert n==path['reflections']==event['reflections']
    P=[tuple(map(F,p)) for p in path['path']];v=(P[1][0]-P[0][0],P[1][1]-P[0][1]);d=path['direction']
    assert v[0]*d[1]-v[1]*d[0]==0 and v[0]*d[0]+v[1]*d[1]>0
    U=set(map(tuple,guard['required_unit_cells']));Z=set(map(tuple,guard['absent_unit_cells']))
    assert U<=cells and not(Z&cells) and not(U&Z)
    tri={tuple(sorted(map(tuple,t))) for t in room['triangles']}
    required={tuple(sorted(map(tuple,t))) for t in guard['triangle_guard']['U']}
    absent={tuple(sorted(map(tuple,t))) for t in guard['triangle_guard']['Z']}
    assert required<=tri and not(absent&tri)
    assert audit(guard['triangle_guard'])=='ok'
    assert guard['triangle_guard']['q']==[2,2]
    guard_path=[(F(x[0],x[1]),F(y[0],y[1])) for x,y in guard['triangle_guard']['path']]
    assert guard_path==P
    method[path['method']]+=1;walls[geometry['walls']]+=1;triangles[geometry['triangles']]+=1
    reflections.append(n);seconds+=path['seconds'];direction_tests+=path['short_directions_tested'];states+=path['orbit_states']
stats=D['stats']
assert stats['valid_rooms']==stats['lit_rooms']==stats['guards_added']==30
assert stats['undecided_rooms']==stats['dark_candidates']==stats['sat_interruptions']==0
assert dict(method)==stats['method_counts']
assert direction_tests==stats['short_directions_tested']==1055
assert states==stats['orbit_states_total']==895
assert stats['sat_calls']==30
assert sum(stats[k] for k in ('sat_seconds','optical_worker_seconds','guard_seconds','geometry_seconds'))<=D['search_wall_seconds']
assert seconds<=stats['optical_worker_seconds']
assert D['search_wall_seconds']<C['budgets']['search_seconds']
assert not (R/'worker-error.json').exists()
assert all(hashlib.sha256((R/'inputs'/source['file']).read_bytes()).hexdigest()==source['sha256']
           for source in json.loads((R/'inputs/sources.json').read_text()))
verdict={'status':'PASS','saved_rooms_revalidated':30,'distinct_unit_square_sets':30,
         'actual_paths_replayed':30,'universal_guards_rechecked':30,
         'method_counts':dict(method),'walls_histogram':dict(walls),'triangle_histogram':dict(triangles),
         'reflections_min':min(reflections),'reflections_max':max(reflections),
         'short_directions_tested':direction_tests,'orbit_states_total':states,
         'search_wall_seconds':D['search_wall_seconds'],'search_runs':1,
         'timing_scope':'Search loop only: SAT calls,30optical subprocesses,geometry checks,guard derivation/audit and artifact writes. Encoding,controls and this replay excluded.',
         'benchmark_checklist':{'errors_counted':True,'timed_work_consumed':True,
                                'runtime_extrapolation':'Unsupported by one capped case; no speedup/comparative benchmark claimed.'},
         'scope':'Same-agent replay plus frozen separately authored triangle/guard checkers; no new search, formal proof or independent reviewer.',
         'result_sha256':hashlib.sha256((R/'result.json').read_bytes()).hexdigest()}
(R/'verification.json').write_text(json.dumps(verdict,indent=2)+'\n')
print(json.dumps(verdict,indent=2))
