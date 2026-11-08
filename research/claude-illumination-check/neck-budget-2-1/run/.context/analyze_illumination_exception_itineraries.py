"""Classify exact visits to transparent vertices on saved connecting rays."""
from collections import Counter,defaultdict
from fractions import Fraction as F
from math import gcd,lcm
import hashlib
import json
from pathlib import Path
from illumination_geometry import check,label,owners_of,check_fan_angles
from illumination_cover import D4,mat
from illumination_group import reflection,compose
from illumination_sector_paths import verify
from verify_illumination_paths import on_segment
from illumination_family_bound import triangles_in_cells
from illumination_three_two_star_bound import complete_support

OUT=Path(__file__).parent/'three-triples'

def visits(room,witness):
    ts=[tuple(sorted(map(tuple,t))) for t in room['triangles']]
    vertices=sorted({p for t in ts for p in t})
    exceptions=set(map(tuple,check(room,strict=False)['transparent_vertices']))
    points=[tuple(F(*v) for v in p) for p in witness['path']]
    distance=F(0);events=[]
    for a,b in zip(points,points[1:]):
        delta=(b[0]-a[0],b[1]-a[1]);norm=abs(delta[0])+abs(delta[1])
        axis=0 if delta[0] else 1
        for p in vertices:
            if label(p)=='A' or not on_segment(p,a,b):continue
            t=F(p[axis]-a[axis],delta[axis]);along=distance+t*norm
            events.append((along,p))
        distance+=norm
    events=sorted(set(events))
    assert all(p in exceptions for _,p in events)
    midpoint=[p for d,p in events if 2*d==distance]
    return dict(points=[p for _,p in events],event_count=len(events),distinct_vertices=len({p for _,p in events}),
                midpoint_exceptions=midpoint,relative_times=[[d.numerator,d.denominator,distance.numerator,distance.denominator] for d,_ in events])


def independent_events(witness,details=False):
    """Parameterize each segment by primitive integer velocity and hit times."""
    points=[tuple(F(*v) for v in p) for p in witness['path']];events={};elapsed=F(0)
    for a,b in zip(points,points[1:]):
        delta=[b[k]-a[k] for k in (0,1)];den=lcm(*(d.denominator for d in delta));v=[int(d*den) for d in delta];g=gcd(*map(abs,v));v=[d//g for d in v]
        duration=next(delta[k]/v[k] for k in (0,1) if v[k])
        axis=max(range(2),key=lambda k:abs(v[k]))
        low=int(min(a[axis],b[axis]).__ceil__());high=int(max(a[axis],b[axis]).__floor__())
        for coordinate in range(low,high+1):
            t=F(coordinate-a[axis],v[axis]);p=tuple(a[k]+t*v[k] for k in (0,1))
            if 0<=t<=duration and all(z.denominator==1 for z in p):
                p=tuple(map(int,p))
                if label(p)!='A':events[elapsed+t,p]=tuple(v)
        elapsed+=duration
    ordered=sorted(events)
    if details:return dict(events=[dict(time=[t.numerator,t.denominator],point=p,velocity=events[t,p]) for t,p in ordered],total_time=[elapsed.numerator,elapsed.denominator])
    return [p for _,p in ordered]


def unfolding_check(room,witness,event_info):
    triangles=[tuple(sorted(map(tuple,t))) for t in room['triangles']]
    owners=owners_of(triangles);opens={e for e,os in owners.items() if len(os)==2};walls=[e for e in owners if e not in opens]
    points=[tuple(F(*v) for v in p) for p in witness['path']]
    d=tuple(witness['direction']);assert gcd(*map(abs,d))==1
    orbit={mat(g,d) for g in D4};states=[];full=0;smooth=0
    for p in check(room,strict=False)['transparent_vertices']:
        _,is_full=check_fan_angles(triangles,tuple(p),owners,opens)
        full+=is_full;smooth+=not is_full
    for event in event_info['events']:
        point=tuple(event['point']);velocity=tuple(event['velocity']);assert velocity in orbit
        states.append((point,velocity))
    assert len(states)==len(set(states))
    bound=len(orbit)*full+(len(orbit)//2)*smooth
    assert len(states)<=bound
    affine=(1,0,0,1,0,0)
    def apply(g,p):return g[0]*p[0]+g[1]*p[1]+g[4],g[2]*p[0]+g[3]*p[1]+g[5]
    for i,(a,b) in enumerate(zip(points,points[1:])):
        aa,bb=apply(affine,a),apply(affine,b);delta=(bb[0]-aa[0],bb[1]-aa[1])
        assert delta[0]*d[1]==delta[1]*d[0] and sum(delta[k]*d[k] for k in (0,1))>0
        if i<len(points)-2:
            candidates=[e for e in walls if on_segment(b,*e)];assert candidates
            r=reflection(candidates[0]);assert r[:4] in D4 and not (r[4]%2 or r[5]%2)
            affine=compose(affine,r)
    target=apply(affine,points[-1]);axis=0 if d[0] else 1;duration=target[axis]/d[axis]
    assert duration.denominator==1 and duration.numerator%2==0
    assert target==tuple(duration*z for z in d)
    assert duration==F(*event_info['total_time'])==2*len(states)
    return dict(full_exceptions=full,smooth_exceptions=smooth,velocity_orbit=len(orbit),exception_visit_bound=bound,
                unfolded_target=[int(v) for v in target],primitive_duration=int(duration),gate_events=event_info['events'])


def run():
    ts=triangles_in_cells(complete_support((2,1))['allowed']);first=[i for i,t in enumerate(ts) if (2,0) in t];second=[i for i,t in enumerate(ts) if (2,2) in t]
    patterns=json.loads((OUT/'neck-patterns-2-1.json').read_text())['canonical_patterns']
    wanted={(tuple(map(tuple,row[0])),row[1],row[2]):n for n,row in enumerate(patterns,1)}
    permutation=[7,5,6,4,3,1,2,0]
    def move(mask):return sum(1<<permutation[j] for j in range(8) if mask>>j&1)
    rows=[];sources={};by_type=defaultdict(list)
    for name in ['ray-pattern-probe-2-1.json','double-fan-search-2-1.json']:
        path=OUT/name;sources[name]=hashlib.sha256(path.read_bytes()).hexdigest()
        for i,record in enumerate(json.loads(path.read_text())['records']):
            room=record['room'];witness=record['witness'];verify(room,witness)
            selected={tuple(sorted(map(tuple,t))) for t in room['triangles']}
            outside=tuple(sorted({(p[0]//2,p[1]//2) for t in selected for p in t if label(p)=='A'}-complete_support((2,1))['mandatory']))
            a=sum(1<<j for j,k in enumerate(first) if ts[k] in selected);b=sum(1<<j for j,k in enumerate(second) if ts[k] in selected)
            key=(outside,a,b);other=(tuple(sorted((2-x,1-y) for x,y in outside)),move(b),move(a));canonical=min(key,other)
            info=visits(room,witness);assert info['points']==independent_events(witness)
            gate_check=unfolding_check(room,witness,independent_events(witness,details=True))
            assert info['event_count']>=1,('no exceptional passage',name,i)
            # Primitive lattice velocity has invariant L1 norm under reflections.
            # An A-to-A unfolded segment has even integer duration.
            events=info['points']
            if key!=canonical:events=[(4-p[0],2-p[1]) for p in reversed(events)]
            row=dict(source=name,record_index=i,neck_type=wanted.get(canonical),direction=witness['direction'],bounces=witness['bounces'],**info,**gate_check,canonical_exception_word=events)
            rows.append(row)
            if row['neck_type']:by_type[row['neck_type']].append(row)
    summary=dict(paths=len(rows),event_counts=dict(sorted(Counter(r['event_count'] for r in rows).items())),
                 distinct_exception_counts=dict(sorted(Counter(r['distinct_vertices'] for r in rows).items())),
                 paths_with_exception_at_midpoint=sum(bool(r['midpoint_exceptions']) for r in rows),
                 analytic_visit_bounds=dict(sorted(Counter(r['exception_visit_bound'] for r in rows).items())),
                 max_exception_events=max(r['event_count'] for r in rows),
                 all_gate_states_distinct=True,all_unfolded_durations_twice_event_count=True,
                 neck_type_paths={str(k):len(v) for k,v in sorted(by_type.items())},
                 neck_words={str(k):[dict(word=json.loads(word),paths=count) for word,count in Counter(json.dumps(r['canonical_exception_word']) for r in v).most_common()] for k,v in sorted(by_type.items())})
    result=dict(status='PASS',sources=sources,summary=summary,records=rows,
                scope='Exact exceptional-vertex itineraries of saved positive paths; two independent event enumerations plus affine unfolding agree. Finite gate-state bound is a necessary property, not an existence proof or direction cutoff. No new ray search.')
    (OUT/'exception-itineraries-2-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary),flush=True)

if __name__=='__main__':run()
