"""Synthesize finite disjunctions of sufficient one-exception path patterns.

Parents contain only audited geometry/counting/connectivity constraints and
positive one-pass ray cuts. They contain no historical illumination cuts.
A negative parent therefore proves a universal conditional midpoint lemma for
its fixed neck. Caps and finite direction misses leave it unresolved.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import json
import time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,digest,solver_for
from illumination_geometry import owners_of,label
from illumination_paths import directions,trace,room as prepare
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from analyze_illumination_exception_itineraries import independent_events,unfolding_check
from search_illumination_fan_partitions import fan_masks,fix_fan
from search_illumination_cell_partitions import fix_cells,room_outside
from search_illumination_three_two_star import make_model,add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts

TARGET=(2,1)
PATH=OUT/'midpoint-cover-2-1.json'

def geometry_parent():
    model,ts,x,bounded,terms=make_model(TARGET)
    first,_=fan_masks(ts,(1,0));second,_=fan_masks(ts,(1,1))
    pattern_path=OUT/'neck-patterns-2-1.json';patterns=json.loads(pattern_path.read_text())['canonical_patterns']
    assert len(patterns)==12
    return model,ts,x,bounded,terms,first,second,patterns

def fixed_neck(model,terms,bounded,x,first,second,pattern):
    outside,a,b=pattern;fix_cells(model,terms,bounded,outside);fix_fan(model,x,first,a);fix_fan(model,x,second,b)

def one_pass(room,witness):
    verify(room,witness)
    assert len(independent_events(witness))==1
    assert unfolding_check(room,witness,independent_events(witness,details=True))['primitive_duration']==2


def seed_paths():
    itinerary_path=OUT/'exception-itineraries-2-1.json';itinerary=json.loads(itinerary_path.read_text())
    probe_path=OUT/'single-gate-probe-2-1.json';probe=json.loads(probe_path.read_text())
    assert probe['source_sha256']==digest(itinerary_path)
    sources={name:json.loads((OUT/name).read_text()) for name in itinerary['sources']}
    for name,h in itinerary['sources'].items():assert digest(OUT/name)==h
    alternatives={(c['source'],c['record_index']):c['single_gate_witness']['witness'] for c in probe['cases']+probe['targeted_follow_up']['cases'] if c['single_gate_witness']}
    result=[]
    for row in itinerary['records']:
        record=sources[row['source']]['records'][row['record_index']];witness=record['witness'] if row['event_count']==1 else alternatives[row['source'],row['record_index']]
        one_pass(record['room'],witness)
        result.append(dict(room=record['room'],witness=witness,source=row['source'],record_index=row['record_index']))
    assert len(result)==147
    provenance=dict(itineraries_sha256=digest(itinerary_path),single_pass_probe_sha256=digest(probe_path),neck_patterns_sha256=digest(OUT/'neck-patterns-2-1.json'))
    return result,provenance


def find_one_pass(data,library,deadline):
    prepared=prepare(data);tested=0;seen=set()
    for d in list(library)+directions(16):
        d=tuple(d)
        if d in seen:continue
        seen.add(d)
        if time.monotonic()>=deadline:return None,dict(status='DIRECTION_SCAN_CAPPED',directions_tested=tested)
        # A single-pass ray has primitive duration2; its grid-crossing budget
        # is independent of the total number of allowed exceptional vertices.
        bound=2*(abs(d[0])+abs(d[1])+max(map(abs,d)))
        witness=trace(data,d,bound,prepared);tested+=1
        if witness['status']!='illuminated':continue
        points=[tuple(F(*v) for v in p) for p in witness['path']]
        duration=sum(sum(abs(b[k]-a[k]) for k in (0,1)) for a,b in zip(points,points[1:]))/sum(map(abs,d))
        if duration!=2:continue
        one_pass(data,witness);return witness,dict(status='ONE_PASS_WITNESS',directions_tested=tested)
    return None,dict(status='NO_SINGLE_PASS_IN_CATALOGUE',direction_bound=16,directions_tested=tested)


def run(seconds):
    begin=time.monotonic();model,ts,x,bounded,terms,first,second,patterns=geometry_parent()
    seed,provenance=seed_paths();owners=owners_of(ts);keys=set();seed_guards=[]
    for r in seed:
        for changed,ray in orbit(r['room'],r['witness']):
            one_pass(changed,ray);facts=tile_facts(ts,owners,ray,changed);key=tuple(facts)
            if key in keys:continue
            keys.add(key);add_guard(model,x,facts);seed_guards.append(dict(room=changed,witness=ray,tile_facts=facts))
    initial=len(keys);previous=json.loads(PATH.read_text()) if PATH.exists() else None
    if previous:assert previous['provenance']==provenance
    records=previous['records'] if previous else []
    prior={c['neck_type']:c for c in previous['classes']} if previous else {}
    for record in records:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']));assert key not in keys
            keys.add(key);add_guard(model,x,guard['tile_facts'])
    frequencies=Counter(tuple(r['witness']['direction']) for r in seed)
    library=[d for d,_ in frequencies.most_common()]
    outcomes=[];solver=solver_for(seconds,173);solver.parameters.cp_model_presolve=False
    def save():
        visited={c['neck_type'] for c in outcomes};classes=outcomes+[c for k,c in prior.items() if k not in visited]
        summary=dict(neck_types=12,visited=len(classes),midpoint_cover_proved=sum(c['exhausted'] for c in classes),seed_rooms=len(seed),unique_seed_guards=initial,new_records=len(records),new_guards=len(keys)-initial,total_guards=len(keys),seconds=time.monotonic()-begin,cp_model_presolve=False,scope='Geometry-only fixed-neck parents plus exact sufficient one-pass midpoint paths; no historical ray cuts. Finite disjunction cover proof is conditional on geometry/solver correctness.')
        temp=PATH.with_suffix('.tmp');temp.write_text(json.dumps(dict(summary=summary,provenance=provenance,patterns=patterns,seed_guards=seed_guards,records=records,classes=classes),indent=2)+'\n');temp.replace(PATH);return summary
    print(json.dumps(dict(event='midpoint_seed',rooms=len(seed),guards=initial)),flush=True)
    for number,pattern in enumerate(patterns,1):
        if prior.get(number,{}).get('exhausted'):outcomes.append(prior[number]);continue
        branch=model.clone();fixed_neck(branch,terms,bounded,x,first,second,pattern)
        started=time.monotonic();deadline=started+seconds;status=None;unresolved=None;before=len(records)
        while time.monotonic()<deadline:
            solver.parameters.max_time_in_seconds=max(.001,deadline-time.monotonic());status=solver.solve(branch)
            if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
            data=room_from(TARGET,ts,x,solver);assert room_outside(data,TARGET)==tuple(map(tuple,pattern[0]))
            witness,screen=find_one_pass(data,library,deadline)
            if witness is None:unresolved=dict(room=data,screen=screen);break
            guards=[]
            for changed,ray in orbit(data,witness):
                one_pass(changed,ray);facts=tile_facts(ts,owners,ray,changed);key=tuple(facts)
                if key in keys:continue
                keys.add(key);add_guard(model,x,facts);add_guard(branch,x,facts);guards.append(dict(room=changed,witness=ray,tile_facts=facts))
            assert guards
            records.append(dict(neck_type=number,room=data,witness=witness,counts=validate(data,TARGET),derived_guards=guards,direction_screen=screen))
        outcomes.append(dict(neck_type=number,pattern=pattern,status=solver.status_name(status) if status is not None else 'NOT_SOLVED',exhausted=status==cp_model.INFEASIBLE,new_records=len(records)-before,seconds=time.monotonic()-started,unresolved=unresolved))
        summary=save();print(json.dumps(dict(event='midpoint_neck',neck_type=number,proved=outcomes[-1]['exhausted'],new_records=outcomes[-1]['new_records'],records=len(records),types_proved=summary['midpoint_cover_proved'],unresolved_reason=unresolved['screen']['status'] if unresolved else None)),flush=True)
    print(json.dumps(dict(event='midpoint_complete',**save())),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=10);args=ap.parse_args();run(args.seconds)
