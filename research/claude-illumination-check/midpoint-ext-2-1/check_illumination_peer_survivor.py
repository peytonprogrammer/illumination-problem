"""Check the peer's saved geometry against already proved sufficient patterns."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import time
from classify_illumination_three_exception import OUT,digest
from illumination_geometry import owners_of
from illumination_three_two_star_bound import validate
from search_illumination_midpoint_covers import PATH,TARGET,geometry_parent,one_pass,find_one_pass
from audit_illumination_midpoint_covers import signature
from analyze_illumination_exception_itineraries import independent_events
from search_illumination_one_exception import tile_facts


def run():
    source=Path(__file__).parent/'claude-illumination-check/two-star-k3/strong-survivor-2-1.json'
    data=dict(triangles=json.loads(source.read_text()),marked=[[0,0],[4,2]],require_simple=True)
    counts=validate(data,TARGET);saved=json.loads(PATH.read_text());_,ts,_,bounded,_,first,second,patterns=geometry_parent()
    selected={tuple(sorted(map(tuple,t))) for t in data['triangles']};bits=[int(t in selected) for t in ts]
    guards=saved['seed_guards']+[g for r in saved['records'] for g in r['derived_guards']]
    matches=[i for i,g in enumerate(guards) if all(bits[j]==value for j,value in g['tile_facts'])]
    witness=None;mode='existing_sufficient_midpoint_condition'
    if matches:witness=guards[matches[0]]['witness']
    else:
        mode='bounded_new_one_pass_search';frequencies=Counter(tuple(g['witness']['direction']) for g in guards)
        witness,screen=find_one_pass(data,[d for d,_ in frequencies.most_common()],time.monotonic()+20)
    if witness:one_pass(data,witness)
    result=dict(status='VERIFIED_ONE_PASS' if witness else 'UNRESOLVED_FOR_ONE_PASS',peer_source_sha256=digest(source),midpoint_cover_sha256=digest(PATH),
                room=data,counts=counts,neck_signature=signature(data,ts,first,second,bounded),matching_sufficient_conditions=matches,
                mode=mode,witness=witness,midpoint_gate=independent_events(witness)[0] if witness else None,
                guard_tile_facts=tile_facts(ts,owners_of(ts),witness,data) if witness else None,
                scope='Peer geometry checked without modifying it. Positive one-pass witness only; no darkness or whole-placement conclusion.')
    (OUT/'peer-survivor-midpoint-2-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('room','counts','witness','guard_tile_facts','matching_sufficient_conditions')}|dict(matching_conditions=len(matches),bounces=witness['bounces'] if witness else None)),flush=True)

if __name__=='__main__':run()
