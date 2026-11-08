"""Bounded rational-phase discriminator, same original R33 deadline."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import importlib.util,json,time
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('criterion',R/'comb-spine-end-prefix-check.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
e=json.loads((R/'comb-spine-end-prefix-effort.json').read_text());start=time.monotonic();count=0;bad=None
for u in (Q(1),Q(2)):
 for v in (Q(1),Q(2)):
  for Ds in (Q(1,2),Q(1),Q(2)):
   for Dt in (Q(1,2),Q(1),Q(2)):
    for bs in (u/3,u/2,2*u/3):
     for bt in (v/3,v/2,2*v/3):
      for gap in (Q(1),Q(2),Q(3)):
       c=Q(1);ls=Q(2);lt=ls+u+gap;Hg=lt+v+3;params=(c,u,v,Ds,Dt,bs,bt,ls,lt,Hg)
       m.deadline();count+=1
       if m.criterion(*params) is None:bad={'parameters':params,'actual_source':[c+Ds,ls+bs],'actual_target':[c+Dt,lt+v-bt]};break
      if bad:break
     if bad:break
    if bad:break
   if bad:break
  if bad:break
 if bad:break
out={'status':'FIRST_RESTRICTED_CRITERION_FAILURE' if bad else 'BOUNDED_RATIONAL_CRITERION_CONTROLS_ALL_POSITIVE','tested_patterns':count,'first_failure':bad,'wall_seconds':time.monotonic()-start,'original_effort_deadline':e['deadline_utc'],'whole_goal_complete':False,'discovery':True,'scope':'One finite protected path arithmetic criterion on stated rational data. No positive general theorem or darkness claim from bounded results.'}
(R/'comb-spine-end-rational-discriminator.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,default=str))
