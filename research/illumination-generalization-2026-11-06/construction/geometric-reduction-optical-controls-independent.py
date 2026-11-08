"""Independent exact review of the TWO prescribed physical H/V hulls only."""
from pathlib import Path
import datetime, hashlib, importlib.util, json

P=Path(__file__).resolve().parent
REVIEW=P.parent/'review'
spec=importlib.util.spec_from_file_location('own_fixed_geometry',P/'geometric-reduction-check-01.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    request=json.loads((REVIEW/'geometric-reduction-optical-controls-review-request.json').read_text())
    for name,value in request['files_sha256'].items():assert sha(REVIEW/name)==value,name
    supplied=json.loads((REVIEW/'geometric-reduction-optical-controls.json').read_text())
    oldcells=g.cells(g.OLD)
    results=[]
    for row in supplied['rows']:
        poly=[tuple(v) for v in row['physical_output_polygon']]
        got=g.geometry(poly)
        assert (got['W'],got['r'],got['area'],got['J'],got['s_N'],got['k'])==(20,8,17,3,3,6)
        # Independently construct the hull as a set of unit open cells.
        expected=set()
        if row['axis']=='horizontal':
            for y in {y for x,y in oldcells}:
                xs=[x for x,yy in oldcells if yy==y]
                expected.update((x,y) for x in range(min(xs),max(xs)+1))
        else:
            for x in {x for x,y in oldcells}:
                ys=[y for xx,y in oldcells if xx==x]
                expected.update((x,y) for y in range(min(ys),max(ys)+1))
        assert g.cells(poly)==expected
        assert all(not g.hit(g.S,g.T,a,b) for a,b in zip(poly,poly[1:]+poly[:1]))
        assert g.where(poly,(1,1))=='interior'
        results.append({'axis':row['axis'],'geometry':got,'direct_actual_S_T':True,
                        'all_wall_intersections':0,'old_1_1_corner_now_interior':True,
                        'independent_unit_cell_hull_matches_physical_polygon':True})
    for name,value in request['files_sha256'].items():assert sha(REVIEW/name)==value,name
    out={'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'status':'ACCEPT_TWO_SCOPED_OPTICAL_CONTROLS','source_sha256':request['files_sha256'],
         'own_geometry_source_sha256':sha(P/'geometric-reduction-check-01.py'),
         'rows':results,'peer_code_executed_or_imported':False,
         'new_search_or_census':False,'whole_goal_complete':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Both prescribed physical hulls independently match cell hulls, exact counts and direct actual S/T rays.')
