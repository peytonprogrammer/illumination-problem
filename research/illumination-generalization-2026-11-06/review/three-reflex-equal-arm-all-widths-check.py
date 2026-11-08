"""ER03 prescribed symbolic branch transport and 42 actual original-wall controls."""
from pathlib import Path
from fractions import Fraction as Q
from math import floor
import ast,json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-parity-free-floor-check.py').read_text()
prefix=source[:source.index('# Fixed author ordinary-floor calibration')]
prefix=prefix.replace('three-reflex-parity-free-floor-review-request.json','three-reflex-equal-arm-all-widths-review-request.json')
setup={'__file__':__file__};exec(compile(prefix,'<own-actual-wall-setup>','exec'),setup)
ns=setup['ns'];replay=setup['env']['replay_actual']
tree=ast.parse((HERE/'three-reflex-equal-arm-whole-obstruction-check.py').read_text())
choices=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign)
    and any(isinstance(t,ast.Name) and t.id=='choices' for t in n.targets)))
choices += [(2,0,'floor',1,'-1/8'),(4,0,'floor',1,'-1/9'),(6,0,'up',1,'-1/5')]
assert len(choices)==24
branches=[]
def center(x):return x-8*floor((x+4)/8)
for u,y,chart,sgn,ds in choices:
 for mirror in (1,-1):
  sigma=sgn*mirror;delta=Q(ds)*mirror;X=u+4 if chart=='floor' else 6-u;dt=1 if y==2 else 5
  z0=center(sigma*2+X*delta);z1=z0+2*delta;z2=center(z1+3*delta)
  assert max(map(abs,[z0,z1,z2,delta]))<4
  offset=z2+dt*delta;assert abs(offset)==y
  i0=(sigma*2+X*delta-z0)/8;k0=(z1+3*delta-z2)/8
  assert i0.denominator==k0.denominator==1 and 2*X+i0>=0 and 6+k0>=0
  # Coefficients of m in the literal source/cap/right equations vanish exactly.
  assert X*8-8*X==0 and 2*8-16==0 and 3*8-8*3==0
  if chart=='floor':assert (sigma*2+(u-1)*delta)%4!=0
  psi=z2+3*delta
  if dt==5:assert psi%8!=0 and delta!=0 and (4*delta)%32!=0
  assert -8<z0+delta<8
  branches.append(dict(u=u,y=y,chart=chart,sigma=sigma,delta=delta,X=X,dt=dt,
    z0=z0,z1=z1,z2=z2,offset=offset,psi=psi,i0=i0,k0=k0,mirror=mirror))
expected=set(range(0,32,2))-{16}
for u in (2,4,6):assert {b['offset']%32 for b in branches if b['u']==u}==expected
# Finite quotient identity only: this is not a room or direction census.
for q in (0,8,16,24):
 for z in range(2,16,2):assert (z-q)%32 in expected or (-z-q)%32 in expected
rays=[]
for m in (3,5):
 A=16*m;QQ=8*m;poly=setup['polygon'](4,4,A,16,1,3,6,7)
 for u in (2,4,6):
  for z in range(2,16,2):
   eligible=[sgn for sgn in (-1,1) if (sgn*z-QQ)%32 in expected]
   image=eligible[0];w=(image*z-QQ)%32
   # Deterministically choose the last exact prescribed matching branch.
   chosen=[b for b in branches if b['u']==u and b['offset']%32==w][-1]
   tau=QQ+chosen['delta'];S=(2,u);T=(A-z,2);X=chosen['X'];D=X+5+chosen['dt']
   i=X*m+chosen['i0'];k=3*m+chosen['k0']
   assert chosen['sigma']*2+X*tau-8*i==chosen['z0']
   assert chosen['z0']+2*tau-A==chosen['z1']
   assert chosen['z1']+3*tau-8*k==chosen['z2']
   E=chosen['z2']+chosen['dt']*tau
   assert (E-image*z)%32==0 and ns['fold'](E,16)==z
   if chosen['dt']==5:
    assert ns['fold'](chosen['z2']+tau,16)!=z
    assert (chosen['z2']+3*tau)%16!=0
   result=replay(poly,S,T,chosen['sigma']*tau,D,
    initial_vy=Q(-1) if chosen['chart']=='floor' else Q(1),
    horizontal_count=1+(chosen['chart']=='floor')+(chosen['dt']==5))
   assert result['roof']['point']==(QQ+chosen['z0']+chosen['delta'],Q(7))
   rays.append(dict(m=m,Q=QQ,S=S,T=T,chosen=chosen,target_image=image,slope=tau,D=D,**result))
assert any(r['chosen']['y']==0 for r in rays)
assert any(r['chosen']['mirror']==-1 for r in rays)
assert setup['request_hash']==hashlib.sha256(setup['REQ'].read_bytes()).hexdigest()
out=dict(status='PASS_ER03_EXACT_BRANCH_TRANSPORT_CIRCLE_AND_PRESCRIBED_PHYSICAL_REPLAYS',
 source_pins_before=setup['before'],source_pins_after=setup['pins'](),request_sha256=setup['request_hash'],
 branches=branches,rays=rays,branch_rows=24,signed_branches=48,cases=len(rays),
 reflections=sum(r['reflections'] for r in rays),wall_leg_guards=sum(r['wall_leg_guards'] for r in rays),
 unbounded_quantifier_from_hand_proof=True,author_code_executed=False,discovery_search_used=False,
 whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['branches','rays','source_pins_before','source_pins_after']}))
