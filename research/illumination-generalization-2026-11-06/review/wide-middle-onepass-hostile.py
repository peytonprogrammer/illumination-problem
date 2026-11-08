"""Second input tranche of the SAME original840-second effort, no clock reset."""
from pathlib import Path
from fractions import Fraction as F
import random,json,time,hashlib
import importlib.util
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('onepass',HERE/'wide-middle-onepass.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
random.seed(60261106)
start=time.time();done=0;skipped=0;first=None;checks=0;timeout=False
try:
 for attempt in range(10000):
  module.guard()
  A=F(random.randrange(2,21));B=F(random.randrange(1,int(A)));a=F(random.randrange(1,int(A)))
  hs,g,ht=[random.choice((F(1,4),F(1,2),F(1),F(3,2),F(2),F(3),F(4))) for _ in range(3)]
  xs=B*random.choice((F(1,6),F(1,3),F(1,2),F(2,3),F(5,6)))
  xt=a+(A-a)*random.choice((F(1,6),F(1,3),F(1,2),F(2,3),F(5,6)))
  L=module.qlcm([2*B/hs,2*A/g,2*(A-a)/ht]);step=module.qgcd([2*B,2*A,2*(A-a)])
  if 8*L*(hs+g+ht)/step>50000:skipped+=1;continue
  data=(A,B,a,hs,g,ht,xs,xt);answer=module.solve(data);done+=1
  checks+=answer.get('checked',answer.get('checked_until_success',0))
  if done%100==0:print(json.dumps({'checked_rooms':done,'skipped_complexity':skipped,'elapsed_seconds':time.time()-start}),flush=True)
  if answer['verdict']=='COMPLETE_EXACT_Y_MONOTONE_FAILURE':
   first={'input_keys':['A','B','a','Hs','g','Ht','xs','xt'],'input':[str(x) for x in data],'answer':answer};break
except TimeoutError:timeout=True
out={'status':'FIRST_EXACT_ONEPASS_FAILURE' if first else 'ORIGINAL_DEADLINE_STOP' if timeout else 'NO_ONEPASS_FAILURE_IN_FINISHED_HOSTILE_SCOPE','rooms':done,'skipped_complexity':skipped,'candidate_checks':checks,'first_failure':first,'elapsed_seconds':time.time()-start,'original_deadline_utc':module.EFF['deadline_utc'],'whole_goal_complete':False,'physical_darkness_claim':False,'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('wide-middle-onepass.py','wide-middle-onepass-hostile.py')}}
(HERE/'wide-middle-onepass-hostile.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
