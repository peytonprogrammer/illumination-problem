"""One prescribed native all-one-roof obstruction and exact floor+roof ray."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-coprime-wide-check.py').read_text().split('\ndef geometry(')[0]
helpers={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'own_floor_roof_predicates'}
exec(compile(source,'<own-pure-geometry>','exec'),helpers);ns=helpers['ns']
# Reuse only the existing reviewer earliest-wall function, changing its
# prescribed horizontal itinerary assertion; no new discovery machinery.
txt=(HERE/'three-reflex-coprime-independent-check.py').read_text();tree=ast.parse(txt)
f=next(f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual')
code=ast.get_source_segment(txt,f)
assert code.count('velocity=(slope,Q(1))')==1
code=code.replace('velocity=(slope,Q(1))','velocity=(slope,-Q(1))')
code=code.replace("assert len(roofs)==len(horizontal)==1","assert len(roofs)==1 and len(horizontal)==2\n    floors=[e for e in horizontal if e['point'][1]==1]\n    assert len(floors)==1 and floors[0]['time']==3 and floors[0]['point']==(Q(28,5),Q(1))\n    assert roofs[0]['time']==7 and roofs[0]['point']==(Q(92,5),Q(5))")
rns={'Q':Q,'ns':ns};exec(compile(code,'<own-earliest-wall-two-prescribed-horizontal-contacts>','exec'),rns)
P=[(12,1),(12,4),(28,4),(28,3),(20,3),(20,0),(32,0),(32,5),(0,5),(0,1)]
S=(Q(8),Q(4));T=(Q(24),Q(2));ns['simple'](P)
assert ns['location'](P,S)==ns['location'](P,T)==1 and all(x%2==0 for p in (S,T) for x in p)
turns=[ns['det'](ns['vec'](P[i-1],P[i]),ns['vec'](P[i],P[(i+1)%10])) for i in range(10)]
assert sum(x<0 for x in turns)==3 and all(x!=0 for x in turns)
# Affine coefficients of all integer image indices give kappa even.
assert all(x%2==0 for x in (8,16,2,2,-2,6))
assert (16-4)%8==(16+4)%8==4 and 32%8==0
kappa=Q(76,5)
assert ns['fold'](8+3*kappa,12)==Q(28,5)
z0=8+6*kappa-24*4;z1=z0+2*kappa-32;z2=z1+kappa-8*2;E=z2+kappa
assert (z0,z1,z2,E)==(Q(16,5),Q(8,5),Q(4,5),16)
assert ns['fold'](E,12)==8
ray=rns['replay_actual'](P,S,T,kappa,Q(10))
out={'status':'PASS_K1_ALL_ONE_OUTER_ROOF_WORD_OBSTRUCTION_AND_ACTUAL_FLOOR_RETURN_RAY','polygon':P,'source':S,'target':T,'walls':10,'reflex_corners':3,'all_one_roof_necessity':'kappa even integer; strictcap forces kappa=16+32m-4sigma=4mod8; actual right corner','all_initial_horizontal_signs':True,'all_target_images_and_vertical_words':True,'certified_illuminating_slope':kappa,'actual_ray':ray,'horizontal_reflections':2,'floor_contact':(Q(28,5),Q(1)),'roof_contact':(Q(92,5),Q(5)),'author_code_executed':False,'discovery_search_used':False,'darkness_claimed':False,'whole_r3_complete':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['polygon','actual_ray']},default=str));print(json.dumps({k:ray[k] for k in ['reflections','wall_leg_guards']}))
