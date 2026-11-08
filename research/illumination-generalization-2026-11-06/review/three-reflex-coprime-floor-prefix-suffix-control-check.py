"""One hand-prescribed singular floor discarded via exact original-S suffix."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-coprime-wide-check.py').read_text().split('\ndef geometry(')[0]
h={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'own_exact_source_return'}
exec(compile(source,'<own-ray-predicates>','exec'),h);ns=h['ns'];replay=h['rns']['replay_actual']
P=[(12,1),(12,4),(32,4),(32,3),(20,3),(20,0),(36,0),(36,5),(0,5),(0,1)]
S=(Q(6),Q(4));T=(Q(26),Q(2));kappa=Q(22);a=Q(12);f=Q(3)
assert 6+f*kappa==72 and (72/a).denominator==1
assert ns['fold'](6+2*f*kappa,a)==6
return_phase=(6+2*f*kappa)%(2*a);assert a<return_phase<2*a
z0=Q(-6);z1=z0+2*kappa-36;Y=z1+kappa;k=(Y+4)//8;z2=Y-8*k;E=z2+kappa
assert (z1,z2,E)==(2,0,22) and ns['fold'](E,16)==10
assert z0+kappa==16
result=replay(P,S,T,kappa,Q(4),(-kappa,Q(1)),1)
out={'status':'PASS_SINGULAR_FLOOR_EXACT_ORIGINAL_SOURCE_SUFFIX','polygon':P,'source':S,'target':T,'formal_floor_time':f,'formal_floor_phase':72,'formal_floor_true_corner':(0,1),'formal_return_time':2*f,'formal_return_phase':138,'actual_return_point':S,'retained_initial_velocity':(-kappa,Q(1)),'retained_duration':4,'actual_ray':result,'residuals':(z0,z1,z2),'final_E':E,'discovery_search_used':False,'author_code_executed':False,'formal_corner_traversed_physically':False,'whole_r3_complete':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['polygon','actual_ray']},default=str));print(json.dumps({k:result[k] for k in ['reflections','wall_leg_guards']}))
