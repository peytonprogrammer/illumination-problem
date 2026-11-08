"""One deadline-limited exact discovery effort; no physical darkness inference."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
from itertools import product
import datetime,time,json,hashlib
HERE=Path(__file__).resolve().parent
EFF=json.loads((HERE/'wide-middle-onepass-effort.json').read_text())
DEADLINE=datetime.datetime.fromisoformat(EFF['deadline_utc']).timestamp()
def guard():
 if time.time()>=DEADLINE:raise TimeoutError('original aggregate deadline')
def qgcd(vals):
 den=lcm(*(x.denominator for x in vals));nums=[int(x*den) for x in vals]
 return F(gcd(*nums),den)
def qlcm(vals):return F(lcm(*(x.numerator for x in vals)),gcd(*(x.denominator for x in vals)))
def fold(u,w):
 z=u%(2*w)
 return (z,1) if z<w else (2*w-z,-1)
def endpoint(A,B,a,hs,g,ht,xs,t):
 p,s1=fold(xs+hs*t,B)
 if p==B:return None,'lower_reflex'
 q,s2=fold(p+s1*g*t,A)
 if q<=a:return None,'upper_gate_or_reflex'
 z,_=fold(q-a+s1*s2*ht*t,A-a)
 return a+z,'valid'
def slopes(A,B,a,hs,g,ht,xs,xt):
 W=A-a;D=hs+g+ht
 L=qlcm([2*B/hs,2*A/g,2*W/ht]);step=qgcd([2*B,2*A,2*W])
 values=set()
 # A conservative necessary grid; all8 sign offsets retained, even redundant ones.
 for e1,e2,e3 in product((-1,1),repeat=3):
  residue=(e1*xs+e2*(xt-a)+e3*a)%step
  n=0
  while residue+n*step<D*L:
   values.add((residue+n*step)/D);n+=1
 return sorted(values),L,step

def solve(data):
 A,B,a,hs,g,ht,xs,xt=data
 vals,L,step=slopes(*data);reasons={};checked=0
 for t in vals:
  guard();q,reason=endpoint(A,B,a,hs,g,ht,xs,t);checked+=1
  reasons[reason]=reasons.get(reason,0)+1
  if q==xt:return {'verdict':'FOUND_EXACT_Y_MONOTONE_PATH','slope':str(t),'period':str(L),'grid_step_numerator':str(step),'checked_until_success':checked,'complete_grid_size':len(vals)}
 return {'verdict':'COMPLETE_EXACT_Y_MONOTONE_FAILURE','period':str(L),'grid_step_numerator':str(step),'checked':checked,'complete_grid_size':len(vals),'candidate_outcomes':reasons}

def main():
 start=time.time();cases=0;candidatechecks=0;first=None;controls=[];timedout=False
 try:
  # Fixed deterministic scope: rational A<=6, integer widths, indicated vertical distances and quarter-position marks.
  for phase in (F(1,2),F(1,4),F(3,4)):
   for A0 in range(2,7):
    for B0 in range(1,A0):
     for a0 in range(1,A0):
      for hs,g,ht in product((F(1,2),F(1),F(3,2)),repeat=3):
       guard();A,B,a=map(F,(A0,B0,a0));xs=phase*B;xt=a+(1-phase)*(A-a)
       data=(A,B,a,hs,g,ht,xs,xt);answer=solve(data);cases+=1
       candidatechecks+=answer.get('checked',answer.get('checked_until_success',0))
       if len(controls)<4:controls.append({'input':[str(x) for x in data],'answer':answer})
       if answer['verdict']=='COMPLETE_EXACT_Y_MONOTONE_FAILURE':
        first={'input_keys':['A','B','a','Hs','g','Ht','xs','xt'],'input':[str(x) for x in data],'answer':answer};break
      if first:break
     if first:break
    if first:break
   if first:break
 except TimeoutError:timedout=True
 out={'status':'FIRST_EXACT_ONEPASS_FAILURE' if first else 'NO_ONEPASS_FAILURE_IN_FINISHED_SCOPE' if not timedout else 'ORIGINAL_DEADLINE_STOP','cases':cases,'candidate_checks':candidatechecks,'first_failure':first,'fixed_controls':controls,'elapsed_seconds':time.time()-start,'original_deadline_utc':EFF['deadline_utc'],'timed_out':timedout,'whole_goal_complete':False,'physical_darkness_claim':False,'limits':'Onepass means y-monotone and vertical-wall reflections only; exact rational data. Completeness depends on hand-derived slope-grid/period proof; arbitrary-real theorem not claimed.','source_sha256':{'wide-middle-onepass.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
 (HERE/'wide-middle-onepass.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='fixed_controls'}),flush=True)
if __name__=='__main__':main()
