"""Bounded CP-SAT search; certificate checker lives in illumination_geometry.py."""
import argparse,itertools,json,time
from pathlib import Path
from ortools.sat.python import cp_model
from illumination_geometry import patch,owners_of,local_sectors,label,save,check,draw

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bounds',type=int,nargs=4,default=[-2,4,-2,4]);ap.add_argument('--target',type=int,nargs=2,default=[2,0]);ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--slits',type=int,default=1);ap.add_argument('--max-tiles',type=int,default=40);ap.add_argument('--max-walls',type=int);ap.add_argument('--simple',action='store_true');ap.add_argument('--out',default='illumination-search');ap.add_argument('--hint');ap.add_argument('--any-target',action='store_true');ap.add_argument('--transparent-budget',type=int,default=0);ap.add_argument('--require-transparent',action='store_true');ap.add_argument('--screen-candidates',type=int,default=0);ap.add_argument('--direction-bound',type=int,default=8);ap.add_argument('--path-cuts',action='store_true');ap.add_argument('--seed-screen',action='append',default=[]);ap.add_argument('--symmetry-cuts',action='store_true');args=ap.parse_args()
    assert not (args.path_cuts and args.any_target), 'Path cuts require a fixed target'
    started=time.monotonic();base=Path(__file__).parent;ts=patch(*args.bounds);owners=owners_of(ts);shared={e:os for e,os in owners.items() if len(os)==2};vertices=sorted({p for t in ts for p in t});n=len(ts)
    model=cp_model.CpModel();x=[model.new_bool_var(f't{i}') for i in range(n)];op={e:model.new_bool_var(f'o{j}') for j,e in enumerate(shared)};cuts={}
    for j,(e,(a,b)) in enumerate(shared.items()):
        model.add(op[e]<=x[a]);model.add(op[e]<=x[b]);c=model.new_bool_var(f'cut{j}');cuts[e]=c
        model.add(c>=x[a]+x[b]-op[e]-1);model.add(c<=x[a]);model.add(c<=x[b]);model.add(c+op[e]<=1)
    model.add(sum(cuts.values())<=args.slits);model.add(sum(x)<=args.max_tiles)
    marked=[(0,0),tuple(args.target)];assert marked[0]!=marked[1]
    costs=[];fulls={};used_vertices=[];bad_vertices=[]
    for p in vertices:
        ids=[i for i,t in enumerate(ts) if p in t];es=[e for e in shared if p in e];rows=[]
        for mask in range(1<<len(ids)):
            bits=[(mask>>j)&1 for j in range(len(ids))];chosen={i for i,b in zip(ids,bits) if b};eligible=[e for e in es if set(shared[e])<=chosen]
            for omask in range(1<<len(eligible)):
                oe={e for j,e in enumerate(eligible) if (omask>>j)&1};missing=len(eligible)-len(oe)
                if missing>args.slits:continue
                sizes,full=local_sectors([ts[i] for i in chosen],p,oe)
                bad=int(label(p)!='A' and (full or 4 in sizes))
                if bad and args.transparent_budget==0:continue
                if args.simple and len(sizes)>1:continue
                rows.append(bits+[int(e in oe) for e in es]+[sum(s!=4 for s in sizes),int(full),bad])
        used=model.new_bool_var(f'used{p}');model.add_max_equality(used,[x[i] for i in ids]);used_vertices.append(used)
        c=model.new_int_var(0,8,f'cost{p}');full=model.new_bool_var(f'full{p}');fulls[p]=full;costs.append(c);bad=model.new_bool_var(f'bad{p}');bad_vertices.append(bad)
        model.add_allowed_assignments([x[i] for i in ids]+[op[e] for e in es]+[c,full,bad],rows)
    model.add(sum(bad_vertices)<=args.transparent_budget)
    if args.require_transparent:model.add(sum(bad_vertices)>=1)
    model.add(fulls[(0,0)]==1)
    if args.any_target:model.add(sum(v for p,v in fulls.items() if p!=(0,0) and label(p)=='A')>=1)
    else:
        assert marked[1] in fulls;model.add(fulls[marked[1]]==1)
    if args.simple:
        model.add(sum(cuts.values())==0)
        used_edges=[]
        for j,os in enumerate(owners.values()):
            u=model.new_bool_var(f'edgeused{j}');model.add_max_equality(u,[x[i] for i in os]);used_edges.append(u)
        model.add(sum(used_vertices)-sum(used_edges)+sum(x)==1)
    # Parent forest with strictly increasing ranks gives connected open-tile adjacency.
    root=next(i for i,t in enumerate(ts) if marked[0] in t);model.add(x[root]==1)
    rank=[model.new_int_var(0,n-1,f'rank{i}') for i in range(n)];model.add(rank[root]==0);parents=[[] for _ in ts]
    for j,(e,(a,b)) in enumerate(shared.items()):
        for u,v in [(a,b),(b,a)]:
            par=model.new_bool_var(f'p{u}_{v}');parents[v].append(par);model.add(par<=op[e]);model.add(rank[v]>=rank[u]+1).only_enforce_if(par)
    for i in range(n):model.add(sum(parents[i])==(0 if i==root else x[i]))
    walls=sum(costs)
    if args.max_walls is not None:model.add(walls<=args.max_walls)
    model.minimize(walls)
    if args.hint:
        hint=json.loads(Path(args.hint).read_text());ht={tuple(sorted(map(tuple,t))) for t in hint['triangles']};hc={tuple(sorted(map(tuple,e))) for e in hint.get('slits',[])}
        for i,t in enumerate(ts):model.add_hint(x[i],int(t in ht))
        for e,os in shared.items():model.add_hint(op[e],int(all(ts[i] in ht for i in os) and e not in hc))
    print(json.dumps(dict(event='model',triangles=n,vertices=len(vertices),build_seconds=time.monotonic()-started,args=vars(args))),flush=True)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=args.seconds;solver.parameters.num_search_workers=4;solver.parameters.random_seed=7
    class Capture(cp_model.CpSolverSolutionCallback):
        def __init__(self):super().__init__();self.count=0
        def on_solution_callback(self):
            self.count+=1
            actual_marks=[(0,0),next(p for p,v in fulls.items() if p!=(0,0) and label(p)=='A' and self.value(v))] if args.any_target else marked
            data=dict(triangles=[t for i,t in enumerate(ts) if self.value(x[i])],slits=[e for e,c in cuts.items() if self.value(c)],marked=actual_marks,require_simple=args.simple,search=vars(args));r=check(data,strict=args.transparent_budget==0)
            assert r['walls']==round(self.objective_value)
            save(base/(args.out+'.json'),data);draw(data,base/(args.out+'.png'),strict=args.transparent_budget==0);print(json.dumps(dict(event='candidate',walls=r['walls'],tiles=r['tiles'],transparent=r['transparent_vertices'],bound=self.best_objective_bound,seconds=self.wall_time)),flush=True)
    if args.screen_candidates:
        from illumination_paths import find_path
        records=[];variables=x+list(op.values());screen_started=time.monotonic();status=None
        from verify_illumination_paths import verify
        from illumination_path_cuts import path_facts
        model_path_cuts=0
        def add_single_path_cut(data,witness):
            nonlocal model_path_cuts
            verify(data,witness)
            chosen={tuple(sorted(map(tuple,t))) for t in data['triangles']};slits={tuple(sorted(map(tuple,e))) for e in data['slits']}
            assert chosen<=set(ts), 'Symmetry leaves patch'
            selected=[int(t in chosen) for t in ts];opened={e:int(all(ts[i] in chosen for i in os) and e not in slits) for e,os in shared.items()}
            facts=path_facts(ts,owners,shared,witness,selected,opened)
            literals=[]
            for (kind,key),value in facts.items():
                v=x[key] if kind=='tile' else op[key];literals.append(1-v if value else v)
            model.add(sum(literals)>=1);model_path_cuts+=1
            return len(facts)
        if args.symmetry_cuts:
            assert args.path_cuts, 'Symmetry cuts require path cuts'
        def add_path_cut(data,witness):
            if not args.symmetry_cuts:return add_single_path_cut(data,witness)
            from illumination_symmetry import orbit
            return sum(add_single_path_cut(d,w) for d,w in orbit(data,witness))
        assert not args.seed_screen or args.path_cuts, 'Seeding requires path cuts'
        seed_keys=set()
        for filename in args.seed_screen:
            seed=json.loads(Path(filename).read_text())
            for r in seed['records']:
                if r['witness']['status']!='illuminated':continue
                assert r['room']['search']['bounds']==args.bounds and r['room']['marked']==[list(p) for p in marked], 'Seed geometry or marks mismatch'
                k=json.dumps([r['room']['triangles'],r['room']['slits'],r['witness']['path']],sort_keys=True)
                if k in seed_keys:continue
                seed_keys.add(k);r=dict(r);r['path_fact_count']=add_path_cut(r['room'],r['witness']);records.append(r)
        seeded=len(records);print(json.dumps(dict(event='seeded',records=seeded,cuts=model_path_cuts,seconds=time.monotonic()-screen_started)),flush=True)
        def checkpoint(summary):
            path=base/(args.out+'-screen.json');temporary=path.with_suffix('.tmp')
            save(temporary,dict(summary=summary,records=records));temporary.replace(path)
        stop_reason='candidate_limit'
        for attempt in range(args.screen_candidates):
            remaining=args.seconds-(time.monotonic()-screen_started)
            if remaining<=0:stop_reason='time_limit';break
            solver.parameters.max_time_in_seconds=remaining
            status=solver.solve(model)
            if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):stop_reason='exhausted' if status==cp_model.INFEASIBLE else 'solver_unknown';break
            actual_marks=[(0,0),next(p for p,v in fulls.items() if p!=(0,0) and label(p)=='A' and solver.value(v))] if args.any_target else marked
            data=dict(triangles=[t for i,t in enumerate(ts) if solver.value(x[i])],slits=[e for e,c in cuts.items() if solver.value(c)],marked=actual_marks,require_simple=args.simple,search=vars(args))
            r=check(data,strict=False);witness=find_path(data,args.direction_bound,1000)
            record=dict(attempt=attempt+1,walls=r['walls'],transparent=r['transparent_vertices'],witness=witness,room=data);records.append(record)
            if witness['status']!='illuminated':
                save(base/(args.out+'-survivor.json'),data);draw(data,base/(args.out+'-survivor.png'),strict=False)
                print(json.dumps(dict(event='survivor',attempt=attempt+1,walls=r['walls'],transparent=r['transparent_vertices'],screen=witness)),flush=True)
                stop_reason='unresolved_candidate';break
            if args.path_cuts:
                record['path_fact_count']=add_path_cut(data,witness)
            else:model.add_forbidden_assignments(variables,[[solver.value(v) for v in variables]])
            if (attempt+1)%10==0:
                progress=dict(event='screened',count=attempt+1,seeded_records=seeded,model_path_cuts=model_path_cuts,all_illuminated=True,seconds=time.monotonic()-screen_started)
                checkpoint(progress);print(json.dumps(progress),flush=True)
        result=dict(status=solver.status_name(status) if status is not None else 'TIME_LIMIT',stop_reason=stop_reason,seeded_records=seeded,model_path_cuts=model_path_cuts,new_screened=len(records)-seeded,screened=len(records),illuminated=sum(r['witness']['status']=='illuminated' for r in records),exhausted=status==cp_model.INFEASIBLE,seconds=time.monotonic()-screen_started,args=vars(args))
        checkpoint(result);save(base/(args.out+'-result.json'),result);print(json.dumps(result),flush=True)
        return
    cb=Capture();status=solver.solve(model,cb);result=dict(status=solver.status_name(status),best=solver.objective_value if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None,lower_bound=solver.best_objective_bound,solutions=cb.count,solve_seconds=solver.wall_time,total_seconds=time.monotonic()-started,args=vars(args),ortools='9.15.6755')
    save(base/(args.out+'-result.json'),result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
