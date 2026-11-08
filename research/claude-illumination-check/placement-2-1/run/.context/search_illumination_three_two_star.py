"""Ray-cut search of complete I=2 / k=3 supports with fixed-triple branches.

Only exact positive-ray cuts enter the parent model. A capped triple is blocked
in a separate discovery copy and remains unresolved in the parent model.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time
from ortools.sat.python import cp_model
from illumination_three_star_model import build_model
from illumination_three_two_star_bound import TARGETS,complete_support,validate
from illumination_geometry import check,owners_of,check_fan_angles
from illumination_cover import D4,mat
from illumination_paths import find_path
from illumination_sector_paths import verify
from illumination_cell_path_bound import path_charge_lower_bound,connected_cell_sets
from search_illumination_one_exception import orbit,tile_facts

BASE=Path(__file__).parent
OUT=BASE/'three-two-star'


def make_model(target):
    model,ts,x,bounded,terms=build_model(target,23,3,complete_support(target))
    if sum(target)>=3:
        missing=sum(1-terms['used'][2*a,2*b] for a,b in bounded['mandatory']-bounded['full'])
        model.add(sum(terms['charges'])+missing>=path_charge_lower_bound(target))
        outside=sorted(bounded['allowed']-bounded['mandatory'])
        rows=[[int(p in selected) for p in outside] for selected in connected_cell_sets(tuple(target))]
        model.add_allowed_assignments([terms['used'][2*a,2*b] for a,b in outside],rows)
    return model,ts,x,bounded,terms


def new_solver(seconds=15):
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=2
    solver.parameters.random_seed=73;solver.parameters.max_time_in_seconds=seconds
    return solver


def room_from(target,ts,x,solver):
    room=dict(triangles=[t for t,v in zip(ts,x) if solver.value(v)],marked=[[0,0],[2*v for v in target]],require_simple=True)
    validate(room,target)
    return room


def typed_exceptions(room):
    geometry=check(room,strict=False)
    ts=[tuple(map(tuple,t)) for t in room['triangles']];owners=owners_of(ts);opened={e for e,ids in owners.items() if len(ids)==2}
    result=[]
    for p in geometry['transparent_vertices']:
        sizes,full=check_fan_angles(ts,p,owners,opened)
        assert full or sizes==[4]
        result.append((p[0],p[1],2 if full else 1))
    assert len(result)==3
    return tuple(sorted(result))


def triple_orbit(target,triple):
    T=tuple(2*v for v in target);result=set()
    for g in D4:
        for swap in (False,True):
            if mat(g,T)!=tuple(-v if swap else v for v in T):continue
            shift=T if swap else (0,0)
            result.add(tuple(sorted((mat(g,p[:2])[0]+shift[0],mat(g,p[:2])[1]+shift[1],p[2]) for p in triple)))
    return tuple(sorted(result))


def fix_triple(model,terms,triple):
    for px,py,value in triple:model.add(terms['defect_at'][px,py]==value)


def postpone(model,terms,target,triple):
    for other in triple_orbit(target,triple):
        model.add_forbidden_assignments([terms['defect_at'][p[:2]] for p in other],[[p[2] for p in other]])


def add_guard(model,x,facts):
    model.add(sum(1-x[i] if value else x[i] for i,value in facts)>=1)


def geometry(target,seconds=20):
    path=OUT/f'geometry-{target[0]}-{target[1]}.json'
    lower=path_charge_lower_bound(target) if sum(target)>=3 else None
    previous=json.loads(path.read_text()) if path.exists() else None
    version=1 if sum(target)>=3 else 0
    # Claude now owns independent geometry reruns; reuse this phase's cached
    # geometry query and perform further work only in the ray-cut parent.
    if previous:return previous
    model,ts,x,bounded,terms=make_model(target);solver=new_solver(seconds);status=solver.solve(model)
    result=dict(target_A_cell=target,status=solver.status_name(status),seconds=solver.wall_time,available_triangles=len(ts),available_A_cells=len(bounded['allowed']),path_charge_bound=lower,cell_projection_version=version)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        room=room_from(target,ts,x,solver);result.update(room=room,counts=validate(room,target))
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(event='geometry',**{k:v for k,v in result.items() if k!='room'})),flush=True)
    return result


def search(target,seconds=90,class_seconds=2,use_seeds=True,discovery_seconds=15):
    started=time.monotonic();geometric=geometry(target)
    path=OUT/f'case-{target[0]}-{target[1]}.json'
    if path.exists():
        old=json.loads(path.read_text())
        if old['summary']['exhausted']:
            print(json.dumps(dict(event='reuse_exhausted',**old['summary'])),flush=True);return old['summary']
    else:old=None
    independent_file=OUT/f'fan-geometry-{target[0]}-{target[1]}.json'
    independent=json.loads(independent_file.read_text()) if independent_file.exists() else None
    if geometric['status']=='INFEASIBLE' or (independent and independent['status']=='INFEASIBLE'):
        result=dict(target_A_cell=target,status='INFEASIBLE',exhausted=True,stop_reason='geometry_excluded',exclusion_engine='CP-SAT' if geometric['status']=='INFEASIBLE' else 'independent_fan_SCIP',records=0,cuts=0,seed_cuts=0,additional_cuts=0)
        path.write_text(json.dumps(dict(summary=result,seeds=[],records=[],triples=[]),indent=2)+'\n');return result
    model,ts,x,bounded,terms=make_model(target);owners=owners_of(ts)
    index_hash=hashlib.sha256(json.dumps(ts).encode()).hexdigest()
    records=list(old['records']) if old else [];seeds=list(old['seeds']) if old else []
    provenance=dict(old['summary']['seed_sources']) if old else {}
    for name,digest in provenance.items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest
    cut_keys=set()
    for seed in seeds:
        facts=seed['tile_facts'];cut_keys.add(tuple(map(tuple,facts)));add_guard(model,x,facts)
    for record in records:
        for guard in record['derived_guards']:
            facts=guard['tile_facts'];key=tuple(map(tuple,facts));assert key not in cut_keys
            cut_keys.add(key);add_guard(model,x,facts)
    if old:assert old['summary']['triangle_index_sha256']==index_hash
    # Recompile old positive-ray guards against the enlarged support. Never
    # reuse indices from a different triangle table or exception budget.
    if use_seeds and old is None:
        for name in [f'one-global-{target[0]}-{target[1]}.json',f'two-global-{target[0]}-{target[1]}.json',f'two-pair-search-{target[0]}-{target[1]}.json']:
            source=BASE/name
            if not source.exists():continue
            data=json.loads(source.read_text());provenance[name]=hashlib.sha256(source.read_bytes()).hexdigest()
            for ri,record in enumerate(data.get('records',[])):
                for gi,guard in enumerate(record.get('derived_guards',[])):
                    facts=tile_facts(ts,owners,guard['witness'],guard['room']);key=tuple(facts)
                    if key in cut_keys:continue
                    cut_keys.add(key);add_guard(model,x,facts)
                    seeds.append(dict(file=name,record_index=ri,guard_index=gi,tile_facts=facts))
        print(json.dumps(dict(event='seeded',target=target,cuts=len(seeds),seconds=time.monotonic()-started)),flush=True)
    discovery=model.clone();triples=list(old.get('triples',[])) if old else [];pending={};solver=new_solver();global_status=None;reason='time_limit';survivor=None
    latest={}
    for outcome in triples:latest[min(triple_orbit(target,tuple(map(tuple,outcome['triple']))))]=outcome
    for canonical,outcome in latest.items():
        if not outcome['exhausted']:
            triple=tuple(map(tuple,outcome['triple']));pending[canonical]=triple;postpone(discovery,terms,target,triple)
    search_started=time.monotonic();initial_records=len(records)
    def save():
        summary=dict(target_A_cell=target,status=solver.status_name(global_status) if global_status is not None else 'NOT_SOLVED',
                     exhausted=global_status==cp_model.INFEASIBLE,stop_reason=reason,records=len(records),new_records=len(records)-initial_records,
                     cuts=len(cut_keys),seed_cuts=len(seeds),additional_cuts=len(cut_keys)-len(seeds),
                     triples_examined=len(triples),triples_excluded=sum(t['exhausted'] for t in triples),pending_triples=len(pending),
                     seconds=time.monotonic()-started,triangle_index_sha256=index_hash,seed_sources=provenance,survivor=survivor)
        temp=path.with_suffix('.tmp');temp.write_text(json.dumps(dict(summary=summary,seeds=seeds,records=records,triples=triples),indent=2)+'\n');temp.replace(path)
        return summary
    def run_branch(triple,allowance):
        nonlocal survivor
        branch=model.clone();fix_triple(branch,terms,triple);before=len(records);begin=time.monotonic();status=None;stop='time_limit'
        while time.monotonic()-begin<allowance:
            solver.parameters.max_time_in_seconds=max(.001,allowance-(time.monotonic()-begin));status=solver.solve(branch)
            if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
                stop='exhausted' if status==cp_model.INFEASIBLE else 'solver_unknown';break
            room=room_from(target,ts,x,solver);assert typed_exceptions(room)==triple
            witness=find_path(room,16,1000)
            if witness['status']!='illuminated':witness=find_path(room,32,2000)
            if witness['status']!='illuminated':
                survivor=dict(room=room,bounded_screen=witness);stop='unresolved_candidate';break
            verify(room,witness);guards=[]
            for changed,ray in orbit(room,witness):
                verify(changed,ray);facts=tile_facts(ts,owners,ray,changed);key=tuple(facts)
                if key in cut_keys:continue
                cut_keys.add(key);guard=dict(room=changed,witness=ray,tile_facts=facts);guards.append(guard)
                for active in (model,discovery,branch):add_guard(active,x,facts)
            assert guards
            records.append(dict(room=room,witness=witness,counts=validate(room,target),derived_guards=guards))
        outcome=dict(triple=triple,status=solver.status_name(status) if status is not None else 'NOT_SOLVED',exhausted=status==cp_model.INFEASIBLE,
                     stop_reason=stop,new_records=len(records)-before,seconds=time.monotonic()-begin)
        triples.append(outcome)
        return outcome
    while time.monotonic()-search_started<seconds:
        remaining=seconds-(time.monotonic()-search_started)
        solver.parameters.max_time_in_seconds=min(discovery_seconds,remaining);status=solver.solve(discovery)
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            room=room_from(target,ts,x,solver);triple=typed_exceptions(room)
            outcome=run_branch(triple,min(class_seconds,max(.001,seconds-(time.monotonic()-search_started))))
            canonical=min(triple_orbit(target,triple))
            if not outcome['exhausted']:
                pending[canonical]=triple;postpone(discovery,terms,target,triple)
            else:pending.pop(canonical,None)
        elif status in (cp_model.INFEASIBLE,cp_model.UNKNOWN) and pending:
            for canonical,triple in list(pending.items()):
                remaining=seconds-(time.monotonic()-search_started)
                if remaining<=0:break
                outcome=run_branch(triple,min(10,remaining))
                if outcome['exhausted']:pending.pop(canonical,None)
                if survivor:break
            if not pending and status==cp_model.INFEASIBLE:
                reason='all_discovered_triples_excluded';break
        else:
            reason='discovery_exhausted' if status==cp_model.INFEASIBLE else 'discovery_unknown';break
        if survivor:
            reason='unresolved_candidate';break
        if len(triples)%5==0:
            print(json.dumps(dict(event='progress',**save())),flush=True)
    solver.parameters.max_time_in_seconds=20;global_status=solver.solve(model)
    if global_status==cp_model.INFEASIBLE:reason='exhausted'
    result=save();print(json.dumps(dict(event='case_complete',**result)),flush=True);return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--target',type=int,nargs=2);ap.add_argument('--geometry-only',action='store_true');ap.add_argument('--seconds',type=float,default=90);ap.add_argument('--class-seconds',type=float,default=2);ap.add_argument('--discovery-seconds',type=float,default=15);ap.add_argument('--no-seeds',action='store_true');ap.add_argument('--no-summary',action='store_true');args=ap.parse_args()
    targets=[tuple(args.target)] if args.target else list(TARGETS)
    for target in targets:geometry(target)
    if not args.geometry_only:
        results=[search(target,args.seconds,class_seconds=args.class_seconds,use_seeds=not args.no_seeds,discovery_seconds=args.discovery_seconds) for target in reversed(targets)]
        if args.no_summary:raise SystemExit(0)
        all_cases=[json.loads(p.read_text())['summary'] for t in TARGETS if (p:=OUT/f'case-{t[0]}-{t[1]}.json').exists()]
        summary=dict(status='EXCLUDED' if len(all_cases)==len(TARGETS) and all(c['exhausted'] for c in all_cases) else 'INCOMPLETE',cases=all_cases,
                     scope='Two full A stars, exactly3 B/C exceptions, complete W<=23 supports; positive rays only in parent models, capped or missed searches remain unresolved.')
        temp=OUT/'summary.tmp';temp.write_text(json.dumps(summary,indent=2)+'\n');temp.replace(OUT/'summary.json')
