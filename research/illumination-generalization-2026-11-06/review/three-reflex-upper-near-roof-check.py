"""UDPT01: one fixed existing-room phase audit, with existing reviewer replay.
No room census or new tracing engine. Deadline is loaded before setup.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import floor,lcm
from datetime import datetime,timezone
import ast,json,hashlib,time
HERE=Path(__file__).parent
EFFORT=HERE/'three-reflex-upper-near-roof-effort.json'
effort=json.loads(EFFORT.read_text());deadline=datetime.fromisoformat(effort['deadline_utc'])
def live():assert datetime.now(timezone.utc)<deadline,'UDPT01 aggregate deadline exhausted'
live()
# Reuse reviewer-owned original-wall predicates and earliest-hit replay only.
helpers={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'near_roof_own_predicates'}
exec(compile((HERE/'three-reflex-coprime-wide-check.py').read_text().split('\ndef geometry(')[0],'<own-geometry>','exec'),helpers)
ns=helpers['ns'];fold=ns['fold']
txt=(HERE/'three-reflex-coprime-independent-check.py').read_text();tree=ast.parse(txt);f=next(f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual')
code=ast.get_source_segment(txt,f).replace('def replay_actual(P,S,T,slope,D):','def replay_actual(P,S,T,slope,D,initial_velocity,expected_floor=None):').replace('velocity=(slope,Q(1))','velocity=initial_velocity')
code=code.replace('assert len(roofs)==len(horizontal)==1',"assert len(roofs)==1\n    if expected_floor is None:assert len(horizontal)==1\n    else:\n        floors=[e for e in horizontal if e['point'][1]==expected_floor]\n        assert len(horizontal)==2 and len(floors)==1\n        assert floors[0]['time']==S[1]-expected_floor")
rns={'Q':Q,'ns':ns};exec(compile(code,'<existing-own-first-wall-replay>','exec'),rns);replay=rns['replay_actual']
e=4;a=4;A=28;R=4;B=16;N=7;P=1;L=4;b=2;c=3;h=4;H=12;S=(2,10);T=(20,2);s,u=S;t,v=T;z=A-t
assert effort['allowed_input']['S']==list(S) and effort['allowed_input']['T']==list(T)
dp=u-h;dl=2*(h-b);C=2*(H-h);g1=h-c;d2=c-v;D=dp+dl+C+g1+d2
period=N*P*D*L;shift=Q(2*e*period,D)
assert all((time*shift/width).denominator==1 for time,width in [(dp,2*A),(dl,2*a),(C,2*A),(g1,2*R),(d2,2*B)])
def phases(tau,sigma):
 ip=floor((sigma*s+dp*tau+A)/(2*A));zp=sigma*s+dp*tau-2*A*ip
 il=floor((zp+dl*tau+a)/(2*a));z0=zp+dl*tau-2*a*il
 im=floor((z0+C*tau)/(2*A));z1=z0+C*tau-(2*im+1)*A
 ik=floor((z1+g1*tau+R)/(2*R));z2=z1+g1*tau-2*R*ik
 E=z2+d2*tau
 return (ip,il,im,ik),(zp,z0,z1,z2),E
classes=[];witness=None
for sigma in (1,-1):
 for eta in (1,-1):
  counts=[0]*5;good=[]
  for q in range(period):
   live();tau=Q(A+eta*z-sigma*s+2*e*q,D)
   if tau<=0:continue
   ix,res,E=phases(tau,sigma)
   shifted=phases(tau+shift,sigma)
   assert shifted[1]==res and shifted[2]-E==d2*shift
   tests=[abs(res[0])<a,abs(res[1])<a,abs(res[2])<R,abs(res[3])<R,fold(E,B)==z]
   for j,ok in enumerate(tests):counts[j]+=int(ok)
   if all(tests):
    good.append(q)
    if witness is None:witness=dict(sigma=sigma,eta=eta,q=q,slope=tau,indices=ix,residuals=res,E=E)
  classes.append(dict(sigma=sigma,eta=eta,period=period,individual_guard_counts=counts,good_residue_count=len(good),good_residues=good))
live();assert witness is not None,'No chart witness: inspect the exhaustive residue result, do not infer darkness'
tau=witness['slope'];sigma=witness['sigma'];zp,z0,z1,z2=witness['residuals'];floorx=fold(zp+(h-b)*tau,a);singular=floorx in(0,a)
if singular:
 assert z0==-zp and fold(z0+dp*tau,A)==s
 duration=D-2*(u-b);velocity=(-sigma*tau,Q(1));expected_floor=None
else:
 duration=D;velocity=(sigma*tau,-Q(1));expected_floor=Q(b)
polygon=[(a,b),(a,h),(A-R,h),(A-R,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
ray=replay(polygon,S,T,tau,duration,velocity,expected_floor)
live()
out=dict(status='PASS_UDPT01_FIXED_PAIR_CHART_FEASIBLE_AND_ACTUAL_RAY_VERIFIED',effort_id=effort['id'],deadline_utc=effort['deadline_utc'],period=period,slope_period=shift,scope='ONLY fixed N7 room, S2,10 T20,2; all four signed target-root grids for this chart; no global theorem or darkness.',classes=classes,witness=witness,floor_x=floorx,floor_corner_suffix_used=singular,ray=ray,ended_utc=datetime.now(timezone.utc).isoformat(),author_code_executed=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['classes','ray']},default=str));print('actual reflections',ray['reflections'],'guards',ray['wall_leg_guards'])
