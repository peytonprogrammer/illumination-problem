"""Bounded exact arithmetic discriminator of ONE proposed protected-path criterion."""
from pathlib import Path
from datetime import datetime,timezone
from time import monotonic
import importlib.util,json
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('criterion',R/'comb-spine-end-prefix-check.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
e=json.loads((R/'comb-spine-end-prefix-effort.json').read_text());start=monotonic();count=0;failed=None
for c in (1,2,3):
 for Ds in range(1,5):
  if (c+Ds)%2:continue
  for Dt in range(1,5):
   if (c+Dt)%2:continue
   for u in (3,4,5):
    for v in (2,3,4,5):
     for gap in (1,2,3):
      ls=2;lt=ls+u+gap;Hg=lt+v+3
      for bs in range(1,u):
       if (ls+bs)%2:continue
       for bt in range(1,v):
        if (lt+v-bt)%2:continue
        m.deadline();count+=1;params=(c,u,v,Ds,Dt,bs,bt,ls,lt,Hg)
        witness=m.criterion(*params)
        if witness is None:
            failed={'parameters':params,'actual_source':[c+Ds,ls+bs],'actual_target':[c+Dt,lt+v-bt]};break
       if failed:break
      if failed:break
     if failed:break
    if failed:break
   if failed:break
  if failed:break
 if failed:break
out={'status':'FIRST_RESTRICTED_CRITERION_FAILURE' if failed else 'BOUNDED_ARITHMETIC_CONTROLS_ALL_POSITIVE','tested_patterns':count,'first_failure':failed,'wall_seconds':monotonic()-start,'original_effort_deadline':e['deadline_utc'],'scope':'Only the stated bounded16wall integer-parameter phase-criterion discriminator. Failure is not darkness; all-positive bounded checks are not a universal proof.','whole_goal_complete':False,'discovery':True}
(R/'comb-spine-end-prefix-discriminator.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
