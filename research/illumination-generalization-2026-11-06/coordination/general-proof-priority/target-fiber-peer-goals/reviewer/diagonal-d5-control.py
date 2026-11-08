"""One predeclared d5 affine-ray control; no discovery or replacement loop."""
from pathlib import Path
from fractions import Fraction as Q
from types import SimpleNamespace
import ast, hashlib, json, time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
START=time.monotonic()
def deadline():
    assert time.monotonic()-START < 30, 'prescribed execution guard exceeded'

geo_path=ROOT/'review/resumed-exact-check.py'
trace_path=ROOT/'review/c1-critical-family-check.py'
needed={'vec','det','dot','edges','on','location','intersect','simple','path_check'}
gns={'Q':Q}
gtree=ast.parse(geo_path.read_text())
exec(compile(ast.Module(body=[n for n in gtree.body if isinstance(n,ast.FunctionDef) and n.name in needed],type_ignores=[]),str(geo_path),'exec'),gns)
g=SimpleNamespace(**{name:gns[name] for name in needed})
tns={'Q':Q,'g':g,'deadline':deadline}
tree=ast.parse(trace_path.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='trace'],type_ignores=[]),str(trace_path),'exec'),tns)
P=[tuple(map(Q,z)) for z in [(0,0),(22,0),(22,10),(10,10),(10,22),(0,22)]]
S=(Q(18),Q(2));T=(Q(2),Q(18));velocity=(Q(-84),Q(-85))
g.simple(P)
assert g.location(P,S)==g.location(P,T)==1
path,why=tns['trace'](P,S,T,velocity)
assert path is not None and why=='actual_target', why
assert path[0]==S and path[-1]==T
checked=g.path_check(P,path)
elapsed=sum(abs(b[0]-a[0])/abs(velocity[0]) for a,b in zip(path,path[1:]))
assert elapsed<=4, ('target too late',elapsed)
assert all(not g.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]))
deadline()
out={'status':'PASS_ONE_PRESCRIBED_D5_AFFINE_CONTROL','discovery':False,'replacement_input_or_direction':False,'polygon':P,'source':S,'target':T,'velocity':velocity,'actual_first_T_time':elapsed,'predicted_time_upper_bound':4,**checked,'path':path,'checker_sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [geo_path,trace_path]],'extraction':'Pure functions only; author discovery entry point, old deadline and search loops never executed','general_hand_lemma_verified_by_this_sample':False,'full_gate_resolved':False,'full_goal_complete':False,'execution_seconds':time.monotonic()-START}
(HERE/'diagonal-d5-control.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['path','polygon','checker_sources']},default=str))
