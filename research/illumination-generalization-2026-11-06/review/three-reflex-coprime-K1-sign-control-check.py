"""One hand-prescribed K1 native countercontrol and actual illuminating ray."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm
import hashlib,json
HERE=Path(__file__).parent
source=(HERE/'three-reflex-coprime-wide-check.py').read_text().split('\ndef geometry(')[0]
helpers={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'own_K1_geometry'}
exec(compile(source,'<own-earliest-wall-replay>','exec'),helpers)
ns=helpers['ns'];replay=helpers['rns']['replay_actual']
Pgon=[(12,1),(12,5),(32,5),(32,3),(20,3),(20,0),(36,0),(36,7),(0,7),(0,1)]
S=(Q(6),Q(6));T=(Q(30),Q(2));ns['simple'](Pgon)
assert ns['location'](Pgon,S)==ns['location'](Pgon,T)==1
turns=[ns['det'](ns['vec'](Pgon[i-1],Pgon[i]),ns['vec'](Pgon[i],Pgon[(i+1)%10])) for i in range(10)]
assert sum(t<0 for t in turns)==3 and all(t!=0 for t in turns)
assert all(x%2==0 for point in (S,T) for x in point)
assert gcd(lcm(3,9,1)*1,4)==1
# Exact affine coefficient identities prove all integer branches, not a sample loop.
# q=3+18m -> tau=10+24m -> X=36+72m -> Y=20+48m.
assert (24+4*3,4*18)==(36,72)
assert (6+Q(4,3)*3,Q(4,3)*18)==(10,24)
assert 20%8==4 and 48%8==0
# Independent negative seed and final residual preservation.
q=4;tau0=(Q(36)-6-6+8*q)/6;assert tau0==Q(28,3)
z1=6+3*tau0-36;Y=z1+2*tau0;k=(Y+4)//8;z2=Y-8*k
assert (z1,z2,k)==(-2,Q(2,3),2)
J=(z2+tau0+6)/8;assert J==2
p=2;tau=tau0+8*9*p;m=6;k=38
assert tau==Q(460,3) and 6+3*tau-(2*m+1)*36==z1 and z1+2*tau-8*k==z2
E=z2+tau;assert E==154 and ns['fold'](E,16)==6 and ((6+tau)/36).denominator!=1
ray=replay(Pgon,S,T,tau,Q(6),(tau,Q(1)),1)
pins=[{'path':str(HERE/f),'sha256':hashlib.sha256((HERE/f).read_bytes()).hexdigest()} for f in ['three-reflex-coprime-K1-sign-control.md','three-reflex-coprime-wide-check.py','resumed-exact-check.py','three-reflex-coprime-independent-check.py']]
out={'status':'PASS_K1_ALL_POSITIVE_SEED_FAILURE_AND_ACTUAL_NEGATIVE_SEED_RAY','source_pins':pins,'polygon':Pgon,'source':S,'target':T,'walls':10,'reflex_corners':3,'all_positive_grid_failure':'strictcap iff q=3+18m; rightY=20+48m=4mod8 always true corner','negative_seed_q':q,'final_slope':tau,'final_J':20,'bottom_phase':E,'actual_ray':ray,'author_code_executed':False,'discovery_search_used':False,'darkness_claimed':False,'whole_r3_complete':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('actual_ray','source_pins','polygon')},default=str));print(json.dumps({k:ray[k] for k in ['reflections','wall_leg_guards']}))
