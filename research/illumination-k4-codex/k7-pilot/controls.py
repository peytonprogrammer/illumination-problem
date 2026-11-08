"""Validate the single-case adapter against prescribed whole-room controls."""
from pathlib import Path
import json
from model import build,bounded_solve,base,Solver
from geometry import inspect,replay
from pysat.pb import PBEnc,EncType

ROOT=Path(__file__).parent

def validate(M):
    B={(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3)}
    reflected={(x,-y-1) for x,y in B}
    third={(3-x,-y-1) for x,y in B}
    old=B|reflected|third
    notch=old|{(1,0),(2,0)}
    modified=notch-{(1,-3)}
    marks=M['record']['marked']['marked_original_coordinates']
    old_info=inspect(old,marks);new_info=inspect(modified,marks)
    assert (old_info['walls'],old_info['k'],old_info['triangles'])==(22,4,30)
    assert (new_info['walls'],new_info['k'],new_info['triangles'])==(18,7,32)
    assert new_info['interior_A']==[(0,0),(2,2)]
    assert replay(new_info['vertices'],*marks,marks)==0
    def assignment(cells):
        tiles={t for x,y in cells for t in base.patch(x,x+1,y,y+1)}
        assert tiles<=set(M['triangles'])
        return [v if t in tiles else -v for t,v in M['triangles'].items()],tiles
    new_assumptions,new_tiles=assignment(modified)
    old_assumptions,_=assignment(old)
    results=[]
    with Solver(name='glucose4',bootstrap_with=M['base_cnf'].clauses+M['exact']) as sol:
        status=bounded_solve(sol,15,new_assumptions);assert status is True,('positive control',status)
        model=set(v for v in sol.get_model() if v>0)
        actual={M['pool'].obj(v)[1] for v in M['exceptions'] if v in model}
        assert actual==set(map(tuple,new_info['exceptions']))
        corners={M['pool'].obj(v)[1] for v in model if isinstance(M['pool'].obj(v),tuple) and M['pool'].obj(v)[0]=='corner'}
        assert corners==set(new_info['vertices'])
        results.append({'control':'analytic_notch_fill_and_leaf_truncation_W18_k7','SAT':True,'geometry':new_info,'cells':sorted(modified),
                        'path':marks,'reflections':0,'exception_channels_match':True,'corner_channels_match':True})
        status=bounded_solve(sol,15,old_assumptions);assert status is False,('out-of-scope control',status)
        results.append({'control':'known_W22_k4_room_rejected','SAT':False,'geometry':old_info})
        a,b=next(v for square,v in M['squares'].items() if square not in modified)
        status=bounded_solve(sol,15,[a,-b]);assert status is False,('unit pairing',status)
        results.append({'control':'unpaired_unit_triangles_rejected','SAT':False})
    exact6=PBEnc.equals(lits=M['exceptions'],weights=[1]*len(M['exceptions']),bound=6,
                       vpool=M['pool'],encoding=EncType.adder).clauses
    with Solver(name='glucose4',bootstrap_with=M['base_cnf'].clauses+exact6) as sol:
        status=bounded_solve(sol,15,new_assumptions);assert status is False,('exact exception count',status)
        results.append({'control':'same_k7_room_rejected_when_exact_k6_requested','SAT':False})
    # Frozen triangle/fan geometry checker is independent of the unit-cell check.
    g=base.check({'triangles':sorted(new_tiles),'marked':marks,'require_simple':True},strict=False)
    assert g['simple_polygon'] and g['walls']==18 and len(g['transparent_vertices'])==7
    result={'status':'PASS','case':M['record']['marked']['case_id'],
            'encoding_seconds':M['seconds'],'triangle_variables':len(M['triangles']),
            'unit_square_pairs':len(M['squares']),'exception_channels':len(M['exceptions']),
            'base_clauses':len(M['base_cnf'].clauses),'exact_k_clauses':len(M['exact']),
            'controls':results,'frozen_triangle_checker_agrees':True,
            'scope':'Prescribed controls only, including analytic whole-square modifications of the known room. No second search case.'}
    (ROOT/'controls.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    M=build();result=validate(M)
    print(json.dumps({k:v for k,v in result.items() if k!='controls'},indent=2))
