"""Focused arithmetic counterexample challenge, both spine orientations."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
from time import monotonic
import random,importlib.util,json
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('both',R/'comb-spine-end-both-branches.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
rng=random.Random(3301);start=monotonic();count=0;bad=None;timeout=False
for index in range(2000):
    m.old.deadline()
    if monotonic()-start>120:timeout=True;break
    c=Q(rng.randrange(1,5));u=Q(rng.randrange(1,6));v=Q(rng.randrange(1,6));Ds=rng.choice([Q(1,2),Q(1),Q(2),Q(3),Q(4)]);Dt=rng.choice([Q(1,2),Q(1),Q(2),Q(3),Q(4)])
    bs=u*Q(rng.randrange(1,5),5);bt=v*Q(rng.randrange(1,5),5);ls=Q(2);lt=ls+u+rng.randrange(1,6);Hg=lt+v+rng.randrange(2,6)
    params=(c,u,v,Ds,Dt,bs,bt,ls,lt,Hg);count+=1
    if m.criterion(*params) is None:
        bad={'parameters':params,'source':[c+Ds,ls+bs],'target':[c+Dt,lt+v-bt]};break
out={'status':'FIRST_BOTH_BRANCH_CRITERION_FAILURE' if bad else 'BOUNDED_BOTH_BRANCH_CHALLENGE_POSITIVE' if not timeout else 'BOUNDED_CHALLENGE_TIMEOUT_INCONCLUSIVE','seed':3301,'tested_patterns':count,'first_failure':bad,'wall_seconds':monotonic()-start,'original_effort_deadline':m.old.effort['deadline_utc'],'discovery':True,'whole_goal_complete':False,'scope':'Restricted finite phase-algebra criterion on prescribed rational comb parameter grid; not darkness or a universal theorem.'}
(R/'comb-spine-end-both-discriminator.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,default=str))
