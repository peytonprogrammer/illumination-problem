"""Guard audit for the I=2,k=3 scan; geometry-only checking is Claude's scope."""
from collections import Counter
from fractions import Fraction as F
import hashlib
import heapq
import itertools
import json
from pathlib import Path
from ortools.sat.python import cp_model
from illumination_geometry import owners_of,label
from illumination_sector_paths import verify
from illumination_three_two_star_bound import TARGETS,complete_support,validate
from illumination_family_bound import NEIGHBORS
from illumination_cell_path_bound import connected_cell_sets,enumerate_paths,fan_charge_check
from search_illumination_one_exception import tile_facts
from search_illumination_three_two_star import make_model,new_solver

BASE=Path(__file__).parent
OUT=BASE/'three-two-star'


def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def overlap(a,b,c,d):return all(max(min(a[k],b[k]),min(c[k],d[k]))<=min(max(a[k],b[k]),max(c[k],d[k])) for k in (0,1))
def intersects(a,b,c,d):
    return overlap(a,b,c,d) and cross(a,b,c)*cross(a,b,d)<=0 and cross(c,d,a)*cross(c,d,b)<=0

def in_triangle(p,t):
    signs=[cross(t[i],t[(i+1)%3],p) for i in range(3)]
    return all(v>=0 for v in signs) or all(v<=0 for v in signs)


def touched_tiles(ts,witness):
    points=[tuple(F(*v) for v in p) for p in witness['path']]
    segments=[(a,b,tuple(min(a[k],b[k]) for k in (0,1)),tuple(max(a[k],b[k]) for k in (0,1))) for a,b in zip(points,points[1:])]
    required=set()
    for i,t in enumerate(ts):
        lo=tuple(min(p[k] for p in t) for k in (0,1));hi=tuple(max(p[k] for p in t) for k in (0,1))
        for a,b,sl,sh in segments:
            if any(hi[k]<sl[k] or lo[k]>sh[k] for k in (0,1)):continue
            if in_triangle(a,t) or in_triangle(b,t) or any(intersects(a,b,t[j],t[(j+1)%3]) for j in range(3)):
                required.add(i);break
    return required


def independent_connected_sets(target):
    bounded=complete_support(target);required=frozenset(bounded['mandatory']);allowed=bounded['allowed'];states={frozenset()};all_states=set(states)
    for _ in range(2):
        next_states=set()
        for chosen in states:
            full=required|chosen
            frontier={(x+dx,y+dy) for x,y in full for dx,dy in NEIGHBORS}&allowed-full
            for p in frontier:next_states.add(chosen|{p})
        all_states|=next_states;states=next_states
    result=set()
    for chosen in all_states:
        full=required|chosen;seen={(0,0)};todo=[(0,0)]
        for x,y in todo:
            for dx,dy in NEIGHBORS:
                q=(x+dx,y+dy)
                if q in full and q not in seen:seen.add(q);todo.append(q)
        if seen==full:result.add(tuple(sorted(chosen)))
    return result


def independent_path_minimum(target):
    # Directed-edge Dijkstra checks the DFS simple-path lower bounds by a
    # separate relaxation allowing repeated vertices. Equality confirms that
    # repetition cannot reduce any recorded bound in these complete supports.
    bounded=complete_support(target);R=bounded['mandatory'];outside=sorted(bounded['allowed']-R);best=10**6
    for n in range(3):
        for selected in itertools.combinations(outside,n):
            allowed=R|set(selected);queue=[];distance={}
            for dx,dy in NEIGHBORS:
                q=(dx,dy)
                if q in allowed:distance[((0,0),q)]=0;heapq.heappush(queue,(0,(0,0),q))
            while queue:
                cost,previous,p=heapq.heappop(queue)
                if distance.get((previous,p))!=cost:continue
                if p==target:best=min(best,8+cost);break
                for dx,dy in NEIGHBORS:
                    q=(p[0]+dx,p[1]+dy)
                    if q not in allowed or q==previous or q==(0,0):continue
                    straight=(p[0]-previous[0],p[1]-previous[1])==(dx,dy)
                    changed=cost+2+int(straight)-int(p in R)
                    if changed<distance.get((p,q),10**6):
                        distance[(p,q)]=changed;heapq.heappush(queue,(changed,p,q))
    return best


def audit_bounds():
    fan=fan_charge_check();cases=[]
    for target in TARGETS:
        if sum(target)<3:continue
        direct=enumerate_paths(target)
        assert set(connected_cell_sets(target))==independent_connected_sets(target)
        value=independent_path_minimum(target);assert value==direct['minimum_Q_plus_missing']
        cases.append(dict(target_A_cell=target,minimum_Q_plus_missing=value,wall_lower_bound=8+value,
                          connected_outside_sets=len(connected_cell_sets(target))))
    return dict(status='PASS',fan=fan,cases=cases)


def audit_case(target):
    path=OUT/f'case-{target[0]}-{target[1]}.json';data=json.loads(path.read_text());summary=data['summary']
    model,ts,x,_,terms=make_model(target);owners=owners_of(ts)
    seeds=data.get('seeds',[]);records=data['records'];seen=set();sources={};cache={};rays=mutations=corruptions=0
    sources_by_hash=summary.get('seed_sources',{})
    for name,digest in sources_by_hash.items():
        source=BASE/name;assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
        sources[name]=json.loads(source.read_text())
    def audit_guard(room,witness,facts):
        nonlocal rays,mutations,corruptions
        verify(room,witness)
        compiled=tile_facts(ts,owners,witness,room);assert compiled==list(map(tuple,facts))
        key=tuple(compiled);assert key not in seen;seen.add(key)
        selected={tuple(sorted(map(tuple,t))) for t in room['triangles']};assert selected<=set(ts)
        required_key=json.dumps(witness['path'],separators=(',',':'))
        if required_key not in cache:cache[required_key]=touched_tiles(ts,witness)
        required=cache[required_key];fixed=dict(compiled)
        assert required<=fixed.keys(),('unfixed touched tile',target,required-fixed.keys())
        assert all(fixed[i]==int(ts[i] in selected) for i in required)
        model.add(sum(1-x[i] if value else x[i] for i,value in compiled)>=1);rays+=1
        if corruptions<12:
            i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
            flipped=dict(fixed);flipped[i]=1-flipped[i];assert any(flipped[k]!=int(ts[k] in selected) for k in required)
            corruptions+=2
        if mutations<12:
            for i in [i for i in range(len(ts)) if i not in fixed][:min(3,12-mutations)]:
                verify(dict(room,triangles=sorted(selected^{ts[i]})),witness);mutations+=1
    for j,seed in enumerate(seeds,1):
        guard=sources[seed['file']]['records'][seed['record_index']]['derived_guards'][seed['guard_index']]
        audit_guard(guard['room'],guard['witness'],seed['tile_facts'])
        if j%200==0:print(json.dumps(dict(event='seed_guard_audit',target=target,rays=rays)),flush=True)
    room_keys=set();max_bounces=0
    for j,record in enumerate(records,1):
        room=record['room'];validate(room,target);verify(room,record['witness'])
        k=tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']));assert k not in room_keys;room_keys.add(k)
        max_bounces=max(max_bounces,record['witness']['bounces'])
        actual_outside={(p[0]//2,p[1]//2) for t in room['triangles'] for p in t if label(p)=='A'}-complete_support(target)['mandatory']
        if sum(target)>=3:assert tuple(sorted(actual_outside)) in connected_cell_sets(tuple(target))
        for guard in record['derived_guards']:audit_guard(guard['room'],guard['witness'],guard['tile_facts'])
        if j%50==0:print(json.dumps(dict(event='new_guard_audit',target=target,records=j,rays=rays)),flush=True)
    assert len(seen)==summary['cuts']
    # Geometry-only checking belongs to Claude. Replay our parents when they
    # contain ray cuts; preserve caps as caps rather than forcing a conclusion.
    if rays:
        solver=new_solver(30);status=solver.solve(model);status_name=solver.status_name(status)
        if summary['exhausted']:assert status==cp_model.INFEASIBLE
    else:status_name='DEFERRED_TO_PEER_GEOMETRY_CHECK'
    result=dict(target_A_cell=target,status='PASS',source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                records=len(records),seed_cuts=len(seeds),additional_cuts=len(seen)-len(seeds),exact_rays_checked=rays,
                required_touch_sets=len(cache),independent_closed_triangle_guard_checks=rays,
                mutation_checks=mutations,corrupt_guard_checks=corruptions,max_new_path_reflections=max_bounces,
                recorded_exhausted=summary['exhausted'],fresh_parent_replay=status_name,
                scope='Positive-ray guards checked physically and by independent closed segment/triangle intersection; geometry-only negative checking assigned to Claude.')
    print(json.dumps(result),flush=True);return result


if __name__=='__main__':
    bounds=audit_bounds();results=[audit_case(t) for t in TARGETS]
    data=dict(status='PASS',necessary_bounds=bounds,cases=results,
              family_status='INCOMPLETE' if not all(r['recorded_exhausted'] for r in results) else 'AWAIT_PEER_GEOMETRY_COMPOSITION',
              scope='I=2,k=3 guard/bounds audit; this is not a full three-exception exclusion when any case remains open.')
    (OUT/'audit.json').write_text(json.dumps(data,indent=2)+'\n')
