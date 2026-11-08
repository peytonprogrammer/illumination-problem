"""One bounded, exact-k7 orthogonal SAT/illumination pilot; no other cases."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess
import sys
import time

from model import build,bounded_solve,Solver,base
from controls import validate
from geometry import inspect,replay
from guards import derive

ROOT=Path(__file__).parent

def dump(path,data):path.write_text(json.dumps(data,indent=2)+'\n')

def main():
    assert not (ROOT/'result.json').exists(),'A completed pilot exists; do not silently rerun the search.'
    M=build();validation=validate(M);case=M['record'];budgets=case['budgets']
    marks=case['marked']['marked_original_coordinates'];S,T=map(tuple,marks)
    # Validate whole-cell guard derivation against a prescribed known-lit control.
    control=validation['controls'][0]
    guard_control=derive(control['path'],control['cells'],S,T)
    dump(ROOT/'guard-control.json',guard_control)
    for name in ('models','paths'): (ROOT/name).mkdir(exist_ok=True)
    started=time.monotonic();deadline=started+budgets['search_seconds']
    stats={'valid_rooms':0,'lit_rooms':0,'undecided_rooms':0,'dark_candidates':0,
           'guards_added':0,'sat_calls':0,'sat_interruptions':0,'sat_seconds':0.0,
           'optical_worker_seconds':0.0,'guard_seconds':0.0,'geometry_seconds':0.0,
           'method_counts':{},'short_directions_tested':0,'orbit_states_total':0}
    events=[];clauses=set();reason=None
    def progress(phase):
        dump(ROOT/'progress.json',{'phase':phase,'elapsed_seconds':time.monotonic()-started,
                                  'case':case['marked']['case_id'],'stats':stats})
    with Solver(name='glucose4',bootstrap_with=M['base_cnf'].clauses+M['exact']) as sol:
        while stats['valid_rooms']<budgets['maximum_valid_models']:
            remaining=deadline-time.monotonic()
            if remaining<=0:reason='SEARCH_TIME_LIMIT';break
            progress('solving_geometry')
            t=time.monotonic();status=bounded_solve(sol,min(budgets['sat_call_seconds'],remaining))
            stats['sat_seconds']+=time.monotonic()-t;stats['sat_calls']+=1
            if status is None:
                stats['sat_interruptions']+=1;progress('SAT_interrupted_no_verdict');continue
            if status is False:reason='CASE_EXHAUSTED_WITH_CHECKED_GUARDS';break
            model={v for v in sol.get_model() if v>0}
            cells=[];tiles=[]
            for cell,variables in M['squares'].items():
                assert len({v in model for v in variables})==1
                if variables[0] in model:cells.append(cell)
            tiles=[tri for tri,var in M['triangles'].items() if var in model]
            t=time.monotonic();info=inspect(cells,marks)
            assert info['walls']<=20 and info['k']==7 and info['triangles']<=42
            assert info['interior_A']==[(0,0),(2,2)]
            frozen=base.check({'triangles':tiles,'marked':marks,'require_simple':True},strict=False)
            assert frozen['simple_polygon'] and frozen['walls']==info['walls']
            assert set(map(tuple,frozen['transparent_vertices']))==set(info['exceptions'])
            stats['geometry_seconds']+=time.monotonic()-t
            stats['valid_rooms']+=1;i=stats['valid_rooms'];tag=f'model-{i:03d}'
            room={'case':case['marked']['case_id'],'cells':sorted(cells),'triangles':tiles,
                  'vertices':info['vertices'],'marks':marks,'geometry':info,
                  'frozen_geometry_agrees':True}
            roomfile=ROOT/'models'/f'{tag}.json';pathfile=ROOT/'paths'/f'{tag}.json';dump(roomfile,room)
            remaining=deadline-time.monotonic()
            if remaining<=0:
                optical={'status':'UNDECIDED','reason':'global_time_limit_before_optics'}
            else:
                budget=min(budgets['optical_room_seconds'],remaining)
                progress(f'checking_{tag}')
                t=time.monotonic()
                try:
                    p=subprocess.run([sys.executable,'-B',str(ROOT/'optics.py'),str(roomfile),str(pathfile),str(budget)],
                                     capture_output=True,text=True,timeout=budget+0.4)
                    if p.returncode:
                        dump(ROOT/'worker-error.json',{'model':tag,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
                        raise RuntimeError(f'Optical worker failed for {tag}: {p.stderr}')
                    optical=json.loads(pathfile.read_text())
                except subprocess.TimeoutExpired:
                    optical={'status':'UNDECIDED','reason':'external_optical_wall_time_limit'}
                stats['optical_worker_seconds']+=time.monotonic()-t
            if optical['status']=='LIT':
                reflections=replay(info['vertices'],S,T,optical['path'])
                assert reflections==optical['reflections']
                t=time.monotonic();g=derive(optical['path'],cells,S,T)
                U=list(map(tuple,g['required_unit_cells']));Z=list(map(tuple,g['absent_unit_cells']))
                assert all(p in M['squares'] for p in U)
                clause=tuple(sorted([-M['squares'][p][0] for p in U]+[M['squares'][p][0] for p in Z if p in M['squares']]))
                assert clause not in clauses and all((v not in model if v>0 else -v in model) for v in clause)
                clauses.add(clause);sol.add_clause(list(clause))
                with (ROOT/'guards.jsonl').open('a') as fh:fh.write(json.dumps({'model':tag,'clause':clause,**g})+'\n')
                stats['guard_seconds']+=time.monotonic()-t
                stats['guards_added']+=1;stats['lit_rooms']+=1
                method=optical['method'];stats['method_counts'][method]=stats['method_counts'].get(method,0)+1
                stats['short_directions_tested']+=optical.get('short_directions_tested',0)
                stats['orbit_states_total']+=optical.get('orbit_states',0)
            elif optical['status']=='CANDIDATE_DARK':
                stats['dark_candidates']+=1;reason='DARK_CANDIDATE_REQUIRES_REVIEW'
            else:
                stats['undecided_rooms']+=1;reason='UNDECIDED_ROOM_STOPPED_PILOT'
            dump(pathfile,optical)
            event={'model':tag,'elapsed_seconds':time.monotonic()-started,'walls':info['walls'],'k':info['k'],
                   'triangles':info['triangles'],'optical_status':optical['status'],
                   'method':optical.get('method'),'reflections':optical.get('reflections')}
            events.append(event)
            with (ROOT/'events.jsonl').open('a') as fh:fh.write(json.dumps(event)+'\n')
            print(json.dumps(event),flush=True);progress('model_processed')
            if reason:break
        if reason is None:reason='VALID_ROOM_CAP_REACHED'
    elapsed=time.monotonic()-started
    result={'status':'PILOT_COMPLETE','case':case['marked'],'budgets':budgets,'stop_reason':reason,
            'search_wall_seconds':elapsed,'encoding_seconds':M['seconds'],
            'geometry_variables':len(M['triangles']),'paired_unit_squares':len(M['squares']),
            'geometry_clauses':len(M['base_cnf'].clauses)+len(M['exact']),
            'stats':stats,'events':events,'controls_status':validation['status'],
            'scope':'ONE marked support case, exact k7, orthogonal W<=20. LIT paths directly replayed and all added universal triangle guards audited. Cutoffs stay undecided. No tranche theorem, DRAT proof or runtime extrapolation.'}
    dump(ROOT/'result.json',result);progress('complete')
    print(json.dumps({k:v for k,v in result.items() if k not in ('events','case')},indent=2),flush=True)

if __name__=='__main__':main()
