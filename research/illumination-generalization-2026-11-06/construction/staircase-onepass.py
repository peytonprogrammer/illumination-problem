#!/usr/bin/env python3
"""A11: exact finite test of one-pass mechanism, not physical darkness."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import json,math,signal,time,hashlib
ROOT=Path(__file__).resolve().parent
E=ROOT/'staircase-onepass-effort.json';eff=json.loads(E.read_text());end=datetime.fromisoformat(eff['aggregate_deadline_utc']).timestamp()
if time.time()>=end:raise SystemExit('original deadline expired')
signal.alarm(max(1,int(end-time.time())))
def leg(x,v,w):
    z=x+v;k=z//w;p=z%(2*w)
    y=p if p<=w else 2*w-p
    vv=abs(v) if y==0 else -abs(v) if y==w else v if k%2==0 else -v
    return y,vv
fixtures=[(3,2,1),(4,2,1),(5,3,1),(5,4,2),(7,4,2),(8,5,3),(9,6,2),(10,3,1)]
rows=[];failure=None
for A,b,a in fixtures:
 for s,t in [(F(2*b+1,2),F(1,2)),(F(2*A-1,2),F(2*a-1,2))]:
    P=math.lcm(2*A,2*b,2*a);records=[];success=[]
    for n in range(3*P):
        if time.time()>=end:raise SystemExit('original deadline')
        if not any((F(n)+s-sign*t)%2==0 for sign in (1,-1)):continue
        tau=F(n,3);x,v=leg(s,tau,A)
        rec={'tau':str(tau),'first_portal':str(x)}
        if x>=b:rec['outcome']='first_reflex_or_ledge'
        else:
            x,v=leg(x,v,b);rec['second_portal']=str(x)
            if x>=a:rec['outcome']='second_reflex_or_ledge'
            else:
                x,v=leg(x,v,a);rec['endpoint']=str(x)
                rec['outcome']='connects' if x==t else 'wrong_endpoint'
                if x==t:success.append(str(tau))
        records.append(rec)
    row={'A':A,'b':b,'a':a,'S':[str(s),'1'],'T':[str(t),'4'],'c':2,'d':3,'H':5,'slope_period':P,'necessary_endpoint_congruence':'3*tau = +/-target_x - source_x (mod2)','candidates':len(records),'successful_onepass_slopes':success,'records':records}
    rows.append(row)
    if not success:failure=row;break
 if failure:break
signal.alarm(0)
out={'status':'COMPLETE_ONEPASS_FAILURE' if failure else 'FIXTURES_PASS_NO_UNIVERSAL_PROOF','physical_darkness':False,'whole_goal_complete':False,'fixtures_checked':len(rows),'failure':failure,'rows':rows,'source_sha256':{Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'ended_utc':datetime.now(timezone.utc).isoformat(),'within_original_deadline':time.time()<end}
(ROOT/'staircase-onepass.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','physical_darkness','fixtures_checked','within_original_deadline')}))
if failure:print(json.dumps({k:v for k,v in failure.items() if k!='records'},indent=2))
