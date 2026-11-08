"""R53 exact necessary residues and prescribed known-lit path; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
left={1,8,10,17};right={4,8,10,14}
beta=sorted((x-2)%18 for x in left);assert beta==[6,8,15,17]
second=[b for b in beta if(2+2*b)%18 in right];assert second==[6,15]
third=[b for b in second if(2+3*b)%18 in left];assert third==[]
assert not any((2+b)%18 in left for b in [2,11])
path=[(1,2),(0,Q(14,3)),(1,Q(22,3)),(Q(3,8),9),(0,8),(Q(9,8),5),(Q(15,8),7),(2,Q(20,3)),(Q(11,8),5),(1,6)]
rows=[]
for a,b in [(Q(1),Q(1)),(Q(1,7),Q(100003)),(Q(100019),Q(2,11))]:
 V=[(0,0),(1,0),(1,1),(2,1),(2,3),(1,3),(1,5),(2,5),(2,7),(1,7),(1,9),(0,9),(0,7),(-b,7),(-b,5),(0,5),(0,4),(-a,4),(-a,2),(0,2)]
 V=[tuple(map(Q,z)) for z in V];g.simple(V)
 z=g.path_check(V,path);assert z['reflections']==8
 assert not any(g.on(A,B,path[-1]) for A,B in zip(path[:-2],path[1:-1]));rows.append({'a':a,'b':b,**z})
out={'status':'R53_ALL_TRAVERSE_NECESSARY_OBSTRUCTION_AND_LIT_CONTROLS_PASS','whole_goal_complete':False,'not_a_darkness_claim':True,'first_beta':beta,'second_beta':second,'third_beta':third,'m1_beta':[2,11],'rows':rows,'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['h2-A1-proof.md','h2-A1-acceptance.json','resumed-exact-check.py']}}
(R/'robust-core-calibration-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256']})
