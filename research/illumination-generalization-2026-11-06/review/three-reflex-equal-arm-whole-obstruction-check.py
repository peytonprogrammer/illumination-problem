"""ER02 independently reconstruct prescribed 21 branches, with original-wall replays.
The unbounded n argument is coefficient algebra; n=1,2 are physical controls only.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import floor
import json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-parity-free-floor-check.py').read_text()
prefix=source[:source.index('# Fixed author ordinary-floor calibration')]
prefix=prefix.replace('three-reflex-parity-free-floor-review-request.json','three-reflex-equal-arm-whole-obstruction-review-request.json')
setup={'__file__':__file__};exec(compile(prefix,'<own-geometry-and-earliest-wall>','exec'),setup)
ns=setup['ns'];replay=setup['env']['replay_actual']
# Only prescribed input choices, independently transcribed. Residuals are recomputed.
choices=[(2,2,'floor',1,'0'),(2,4,'floor',1,'1/8'),(2,6,'floor',1,'-1/2'),
 (2,8,'floor',1,'7/8'),(2,10,'up',-1,'2'),(2,12,'floor',1,'17/8'),(2,14,'floor',-1,'5/2'),
 (4,2,'floor',1,'0'),(4,4,'floor',1,'1/9'),(4,6,'floor',1,'-4/9'),
 (4,8,'floor',1,'5/3'),(4,10,'floor',1,'4/3'),(4,12,'floor',1,'7/3'),(4,14,'floor',1,'22/9'),
 (6,2,'up',1,'0'),(6,4,'up',1,'1/5'),(6,6,'up',-1,'4/5'),(6,8,'up',-1,'1'),
 (6,10,'up',-1,'2'),(6,12,'up',-1,'11/5'),(6,14,'up',-1,'12/5')]
assert {(u,y) for u,y,*_ in choices}=={(u,y) for u in (2,4,6) for y in range(2,16,2)}
assert len(choices)==21
candidate=HERE.parent/'construction/three-reflex-equal-arm-whole-obstruction-candidate.md'
author_table=json.loads(candidate.read_text().split('```json\n')[1].split('```')[0])
proof_cases=[];rays=[]
def centered(x):return x-8*floor((x+4)/8)
for row,auth in zip(choices,author_table):
 u,y,chart,sign,ds=row;delta=Q(ds);A0=u+4 if chart=='floor' else 6-u
 dt=1 if y==2 else 5
 z0=centered(sign*2+A0*delta);z1=z0+2*delta;z2=centered(z1+3*delta)
 assert auth[:4]==list(row[:4]) and Q(auth[4])==delta
 assert list(map(Q,auth[5:]))==[z0,z1,z2]
 assert all(abs(x)<4 for x in (delta,z0,z1,z2))
 i0=(sign*2+A0*delta-z0)/8;k0=(z1+3*delta-z2)/8
 assert i0.denominator==k0.denominator==1 and 2*A0+i0>=0 and 6+k0>=0
 # Exact affine-in-n coefficient identities, not interpolation from sample n.
 assert 16*A0==8*(2*A0)
 assert 2*16==32 and 3*16==8*6
 offset=z2+dt*delta;assert abs(offset)==y
 assert (dt*16)%32==16
 source_floor_phase=sign*2+(u-1)*delta
 if chart=='floor':assert source_floor_phase%4!=0
 bottom_phase=z2+3*delta
 if dt==5:
  assert delta!=0 and (4*delta)%32!=0 and bottom_phase%16!=0
 # 0 < 16n+z0+delta < 32n follows already at n>=1 by |z0+delta|<8.
 assert -8<z0+delta<8
 case=dict(u=u,y=y,source_chart=chart,sign=sign,delta=delta,A0=A0,
   residuals=[z0,z1,z2],i0=i0,k0=k0,target_offset=offset,
   source_floor_phase=source_floor_phase if chart=='floor' else None,
   bottom_phase=bottom_phase if dt==5 else None)
 proof_cases.append(case)
 for n in (1,2):
  A=32*n;tau=16*n+delta;z=y if n%2==0 else 16-y
  S=(2,u);T=(A-z,2);D=A0+2+3+dt
  poly=setup['polygon'](4,4,A,16,1,3,6,7)
  i=2*A0*n+i0;k=6*n+k0
  assert sign*2+A0*tau-8*i==z0
  assert z0+2*tau-A==z1
  assert z1+3*tau-8*k==z2
  E=z2+dt*tau;assert ns['fold'](E,16)==z
  floor_phase=z2+3*tau
  if dt==5:assert ns['fold'](z2+tau,16)!=z and floor_phase%16!=0
  result=replay(poly,S,T,sign*tau,D,initial_vy=Q(-1) if chart=='floor' else Q(1),
     horizontal_count=1+(chart=='floor')+(dt==5))
  assert result['roof']['point']==(16*n+z0+delta,Q(7))
  assert result['roof']['time']==A0+1
  if chart=='floor':
   fx=ns['fold'](sign*2+(u-1)*tau,4)
   assert any(e['time']==u-1 and e['point']==(fx,Q(1)) for e in result['events'])
  if dt==5:
   fx=A-ns['fold'](floor_phase,16)
   assert any(e['time']==A0+8 and e['point']==(fx,Q(0)) for e in result['events'])
  rays.append(dict(n=n,u=u,y=y,S=S,T=T,signed_slope=sign*tau,D=D,**result))
assert setup['request_hash']==hashlib.sha256(setup['REQ'].read_bytes()).hexdigest()
out=dict(status='PASS_ER02_ALL_21_PRESCRIBED_BRANCHES_AND_42_PHYSICAL_PARITY_CONTROLS',
 source_pins_before=setup['before'],source_pins_after=setup['pins'](),request_sha256=setup['request_hash'],
 proof_cases=proof_cases,rays=rays,branch_count=21,cases=len(rays),
 reflections=sum(x['reflections'] for x in rays),wall_leg_guards=sum(x['wall_leg_guards'] for x in rays),
 all_n_from_explicit_coefficient_identities=True,author_code_executed=False,discovery_search_used=False,
 room_census=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['proof_cases','rays','source_pins_before','source_pins_after']}))
