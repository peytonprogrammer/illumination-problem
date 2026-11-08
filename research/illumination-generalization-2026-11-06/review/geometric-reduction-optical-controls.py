"""Exact direct-ray controls in already computed H/V known22 hulls. No search."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib
R=Path(__file__).resolve().parent
src=R/'geometric-reduction-ear-monotonicity-check.py';ns={'F':F,'S':(0,0),'T':(2,2)}
mod=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(src),'exec'),ns)
x=json.loads((R/'geometric-reduction-hull-independent-check.json').read_text())
receipt=json.loads((R/'geometric-reduction-hull-independent.json').read_text())
assert hashlib.sha256((R/'geometric-reduction-hull-independent-check.json').read_bytes()).hexdigest()==receipt['review_evidence_sha256']['geometric-reduction-hull-independent-check.json']
rows=[]
for r in x['rows']:
 if r['name']!='known22':continue
 # The vertical band's working coordinates are swapped. Restore actual physical coordinates.
 p=[tuple(z) if r['axis']=='horizontal' else (z[1],z[0]) for z in r['output_polygon']]
 if sum(a[0]*b[1]-a[1]*b[0] for a,b in ns['edges'](p))<0:p=p[::-1]
 counts=ns['analyze'](p)
 assert counts['reflex']==8 and counts['walls']==20
 S=ns['S'];T=ns['T']
 assert all(not ns['intersects'](S,T,a,b) for a,b in ns['edges'](p))
 assert ns['classify'](p,(1,1))=='interior' and (1,1) not in p
 rows.append({'axis':r['axis'],'physical_output_polygon':p,'actual_S':S,'actual_T':T,'counts':counts,'direct_actual_path':[S,T],'all_finite_wall_intersections':0,'old_obstruction_point':[1,1],'old_obstruction_is_now_strict_interior':True,'original_known22_actual_darkness':'Inherited accepted hand proof; originalr9 outside target.','W_independent_existential_hull_transfer':'FALSE','r_le_8_only_transfer':'OPEN'})
out={'status':'PASS_PRESCRIBED_HV_ACTUAL_DIRECT_RAYS','rows':rows,'coordinate_frame_note':'Vertical output_polygon in the earlier band-check JSON is in swapped working axes; this file explicitly swaps back before physical checks.','new_search_or_census':False,'author_checker_executed':False,'whole_goal_complete':False}
(R/'geometric-reduction-optical-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{'axis':r['axis'],'r':r['counts']['reflex'],'k':r['counts']['k'],'direct_actual_ray':True} for r in rows],indent=2))
