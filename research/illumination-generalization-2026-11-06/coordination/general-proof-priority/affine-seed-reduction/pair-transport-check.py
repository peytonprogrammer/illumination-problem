"""Four predeclared exact paths and shear congruences; no discovery run."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm
import ast
import hashlib
import json

HERE=Path(__file__).resolve().parent
source=HERE.parents[2]/'review/resumed-exact-check.py'
names={'vec','det','dot','edges','on','location','intersect','simple','path_check'}
ns={'Q':Q}
tree=ast.parse(source.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(source),'exec'),ns)
P=[(0,0),(28,0),(28,4),(16,4),(16,16),(0,16)]
T=(8,8)
A,a,B,H=28,16,4,16
K=lcm(H//gcd(a,H),B//gcd(A-a,B))
assert K==1 and gcd(K*(T[0]+a),2*H)==8
assert (T[1]+(T[0]+a))%(2*H)==0
ns['simple'](P)
controls=[
 ((26,2),False,4,(-9,7),[(Q(164,7),4),(Q(128,7),0)]),
 ((24,2),False,2,(-8,7),[(Q(152,7),4),(Q(120,7),0)]),
 ((22,2),False,0,(-1,1),[(20,4),(16,0)]),
 ((20,2),True,2,(-6,7),[(Q(128,7),4),(Q(104,7),0)]),
]
results=[]
for S,reflect,h,direction,contacts in controls:
 r=(S[1]+S[0]-a)%(2*B)
 assert reflect==(r>B)
 assert h==(2*B-r if reflect else r)
 seed_source=(S[0],h)
 seed_target=(T[0],0)
 assert 0<seed_target[0]<a<seed_source[0]<A and 0<=h<=B
 assert not any(ns['on'](seed_source,seed_target,c) for c in P)
 # Closed lower rectangle is contained in the room. Even the h=0 case
 # is a regular unfolded segment, because its two endpoints and all its
 # intervening points avoid every actual physical corner.
 dx,dy=seed_target[0]-seed_source[0],-h
 inverse=(dx,-dx-dy) if reflect else (dx,dy-dx)
 g=gcd(abs(inverse[0]),abs(inverse[1]))
 assert tuple(v//g for v in inverse)==direction
 path=[S,*contacts,T]
 checked=ns['path_check'](P,path)
 assert checked=={'wall_leg_guards':18,'reflections':2}
 vin=ns['vec'](path[0],path[1])
 assert ns['det'](vin,direction)==0 and ns['dot'](vin,direction)>0
 results.append({'source':S,'map':'R_y V' if reflect else 'V','seed_source':seed_source,'seed_target':seed_target,'wall_aligned_seed':h==0,'launch_direction':direction,'path':[[str(c) for c in z] for z in path],**checked})
# Second target: positive congruence with a larger shear, no new trajectory.
assert gcd(K*(6+a),2*H)==2 and 8%2==0
assert (8+4*(6+a))%(2*H)==0
# Failure of the entire integral vertical shear subfamily is a gcd
# obstruction, not a scan over possible parameters or rays.
assert 6%gcd(K*(8+a),2*H)!=0
out={'status':'PASS_PRESCRIBED_PAIR_TRANSPORT_CONTROLS','uniform_source_target':[8,8],'K':K,'valid_shear':1,'control_count':4,'total_wall_leg_guards':sum(z['wall_leg_guards'] for z in results),'controls':results,'additional_target_arithmetic_only':{'target':[6,8],'valid_shear':4},'restricted_criterion_failure':{'target':[8,6],'gcd':8,'target_y':6},'all_real_source_coverage':'Hand proof in pair-transport.md; four examples are controls, not the proof of the universal quantifier','all_target_coverage':False,'ten_wall_or_universal_progress':False,'search':False,'checker_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
(HERE/'pair-transport-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
