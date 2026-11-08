#!/usr/bin/env python3
"""Exact local germs/affine reflections; no room, orbit or direction search."""
from fractions import Fraction as F
from pathlib import Path
import json

a,b=F(2),F(4);k0=b/a
rows=[]
for delta in [F(1,10),F(-1,10)]:
 k=(b+delta)/a
 if delta>0:
  point=(F(0),delta);out=(-F(1),k);wall='positive vertical'
  assert -delta/k<0 and point[1]>0
 else:
  point=(-delta/k,F(0));out=(F(1),-k);wall='positive horizontal'
  assert delta<0 and point[0]>0
 assert point[1]==k*point[0]+delta
 assert point[0]==-a+(point[1]+b)/k
 rows.append({'delta':str(delta),'k':str(k),'first_local_wall':wall,'point':[str(x) for x in point],'outgoing':[str(x) for x in out]})
vV=(-F(1),k0);vH=(F(1),-k0)
assert all(x==-y for x,y in zip(vV,vH))
C=(F(3),F(-5));q=(F(7),F(2))
RV=(2*C[0]-q[0],q[1]);RH=(q[0],2*C[1]-q[1])
assert RH==tuple(2*c-x for c,x in zip(C,RV))
controls=[]
v0=(F(1),F(2));tau=F(2)
for lam in [F(1),F(2),F(3)]:
 P=tuple(-lam*v for v in v0);QV=tuple(tau*v for v in v0);QH=tuple(-x for x in QV);d=tuple(q-p for q,p in zip(QH,P))
 assert d==tuple((lam-tau)*v for v in v0)
 if lam>tau:
  assert 0<lam-tau<lam;case='endpoint before declared corner'
 elif lam==tau:
  assert d==(0,0);case='zero flight'
 else:
  assert lam-tau<0;case='opposite launch'
 controls.append({'lambda':str(lam),'tau':str(tau),'displacement':[str(x) for x in d],'case':case})
out={'status':'PASS_PRESCRIBED_LOCAL_GERM_AND_HOLONOMY_CHECKS','one_sided_physical_scattering':rows,'limiting_exit_velocities':[[str(x) for x in vV],[str(x) for x in vH]],'limits_are_antipodal':True,'off_origin_corner_reflections':{'C':[str(x) for x in C],'Q':[str(x) for x in q],'Q_V':[str(x) for x in RV],'Q_H':[str(x) for x in RH],'Q_H_equals_2C_minus_Q_V':True},'two_word_cases':controls,'cone_angle':'6*pi','outgoing_prongs_per_developed_direction':3,'actual_dark_pair_claimed':False,'all_global_rerouting_refuted':False,'local_positive_transfer_proved':False,'nine_distinct_corners_proved':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
