"""Read-only mathematical controls of the supplied all-n comb formula. No ray search."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util,json
H=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',H/'resumed-exact-check.py')
own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
rows=[]
for n in (0,1,3,10):
    R=Q(20+2*n)
    p=[(0,0),(R,0),(R,4),(4,4),(4,8),(R,8),(R,12),(4,12),(4,16),(R,16),(R,20),(4,20),(4,24),(R,24),(R,28),(4,28),(4,32),(R,32),(R,36),(0,36)]
    p=[tuple(map(Q,z)) for z in p];S=(Q(8+2*n),Q(2));T=(Q(8+2*n),Q(34))
    own.simple(p)
    bottom=[(Q(8+2*n)-k-Q(1,2),Q(4 if k%2==0 else 0)) for k in range(4+2*n)]
    upper=[(Q(9,2)+k,Q(36 if k%2==0 else 32)) for k in range(4+2*n)]
    path=[S]+bottom+[(Q(0),Q(18))]+upper+[T]
    assert all(not own.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]))
    guards=own.path_check(p,path)
    assert guards['reflections']==9+4*n
    rows.append({'n':n,'source':S,'target':T,'path':path,**guards})
out={'status':'ALL_PRESCRIBED_COMB_FORMULA_PATHS_PASS','rows':rows,'total_reflections':sum(x['reflections'] for x in rows),'total_wall_leg_guards':sum(x['wall_leg_guards'] for x in rows),'whole_goal_complete':False,'scope':'Four finite controls corroborate the separate all-n hand proof; no independent search or all-pair claim.'}
(H/'comb-formula-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
