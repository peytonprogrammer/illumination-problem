"""AP03 two prescribed physical cases: real floor and exact-S suffix only."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm,floor
import ast,json,hashlib
HERE=Path(__file__).parent
REQ=HERE.parent/'construction/three-reflex-parity-free-floor-review-request.json'
def pins():
    rows=json.loads(REQ.read_text())['source_pins']
    for row in rows:assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
    return rows
before=pins();request_hash=hashlib.sha256(REQ.read_bytes()).hexdigest()
ns={'Q':Q,'F':Q}
tree=ast.parse((HERE/'resumed-exact-check.py').read_text())
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)
    and n.name in names],type_ignores=[]),'<own-geometry>','exec'),ns)
source=(HERE/'three-reflex-coprime-independent-check.py').read_text()
node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='replay_actual')
code=ast.get_source_segment(source,node)
code=code.replace('def replay_actual(P,S,T,slope,D):',
    'def replay_actual(P,S,T,slope,D,initial_vy=Q(1),horizontal_count=1):')
code=code.replace('velocity=(slope,Q(1))','velocity=(slope,initial_vy)')
code=code.replace('assert len(roofs)==len(horizontal)==1',
    'assert len(roofs)==1 and len(horizontal)==horizontal_count')
env={'Q':Q,'ns':ns};exec(compile(code,'<own-earliest-original-walls>','exec'),env)
def polygon(a,R,A,B,b,c,h,H):
    return [(a,b),(a,h),(A-R,h),(A-R,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]

# Fixed author ordinary-floor calibration, reconstructed without author code.
e,P,K,N,L,b,c,h,H=2,7,3,13,4,1,3,5,6
a,R,A,B=P*e,K*e,N*e,L*e;S=(2,4);T=(22,2)
poly=polygon(a,R,A,B,b,c,h,H)
ns['simple'](poly);assert ns['location'](poly,S)==ns['location'](poly,T)==1
d0=h+S[1]-2*b;C=2*(H-h);F=h-T[1];D=d0+C+F
Lam=lcm(P,N,K);g=gcd(Lam*(c-T[1]),L)
assert (d0,C,F,D,g)==(7,2,3,12,1)
assert P*F+g*(d0+C)<=K*D
seed=Q(37,3);tau=seed+2*e*Lam
i,m,j,k=276,42,828,184
z0=S[0]+d0*tau-2*a*i
z1=z0+C*tau-(2*m+1)*A
z2=z1+(h-c)*tau-2*R*k;E=z2+(c-T[1])*tau
assert tau==Q(3313,3) and [z0,z1,z2]==[Q(13,3),Q(3),Q(11,3)]
assert g*j-K*k==276 and E==1108 and (E-(A-T[0]))%(2*B)==0
phi=S[0]+(S[1]-b)*tau;assert phi==3315 and ns['fold'](phi,a)==11
ordinary=env['replay_actual'](poly,S,T,tau,D,initial_vy=Q(-1),horizontal_count=2)
assert any(x['point']==(Q(11),Q(1)) and x['time']==3 for x in ordinary['events'])
assert ordinary['roof']['point']==(Q(50,3),Q(6))

# Separate physical suffix-lemma control; not a wider-source family example
# and not claimed to be the half-open selector's output.
a=R=4;A=20;B=12;b=1;c=4;h=6;H=10;S2=(2,4);T2=(14,2);tau2=Q(2)
poly2=polygon(a,R,A,B,b,c,h,H)
ns['simple'](poly2);assert ns['location'](poly2,S2)==ns['location'](poly2,T2)==1
d02=h+S2[1]-2*b;C2=2*(H-h);F2=h-T2[1];D2=d02+C2+F2
phi2=S2[0]+(S2[1]-b)*tau2
assert phi2==8 and phi2/a==2 and ns['fold'](phi2,a)==0
return_time=2*(S2[1]-b)
assert ns['fold'](S2[0]+return_time*tau2,a)==S2[0]
assert d02-return_time==h-S2[1]>=0
z02=S2[0]+d02*tau2-2*a*2
z12=z02+C2*tau2-A;z22=z12+(h-c)*tau2
E2=z22+(c-T2[1])*tau2
assert [z02,z12,z22,E2]==[2,-2,2,6]
assert ns['fold'](E2,B)==A-T2[0]
suffix=env['replay_actual'](poly2,S2,T2,-tau2,D2-return_time)
assert suffix['actual_target_time']==14
assert not any(x['point'][1]==b for x in suffix['events'])
assert request_hash==hashlib.sha256(REQ.read_bytes()).hexdigest()
out=dict(status='PASS_AP03_ORDINARY_REAL_FLOOR_AND_SEPARATE_EXACT_S_SUFFIX',
    source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,
    ordinary=dict(source=S,target=T,slope=tau,D=D,floor_phase=phi,**ordinary),
    suffix=dict(source=S2,target=T2,formal_slope=tau2,formal_floor_phase=phi2,
        discarded_prefix_duration=return_time,emitted_signed_slope=-tau2,
        scope='Physical suffix lemma only; P=K control is not the whole P>K family or a claimed selector output',**suffix),
    cases=2,reflections=ordinary['reflections']+suffix['reflections'],
    wall_leg_guards=ordinary['wall_leg_guards']+suffix['wall_leg_guards'],
    author_code_executed=False,formal_corner_prefix_traced=False,discovery_search_used=False,
    whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['ordinary','suffix','source_pins_before','source_pins_after']}))
