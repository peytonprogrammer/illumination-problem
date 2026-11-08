from fractions import Fraction as F
from pathlib import Path
from itertools import product
from datetime import datetime
import time,json
p=Path(__file__).parent
stop=datetime.fromisoformat(json.loads((p/'separated-teeth-effort.json').read_text())['deadline']).timestamp()
started=time.time();runs=0

def ladder(base,period,threshold):
    return base+period*max(0,(threshold-base)//period+1)

def match(c,a,b,ds,dt,m,ps,pt):
    tau=F(0);steps=0
    while True:
        if time.time()>=stop:raise TimeoutError('original A29 aggregate deadline')
        ls=ladder(ps,2*a,ds*tau);rt=ladder(pt,2*b,dt*tau)
        nxt=(ls+rt+m)/(2*c+ds+dt);steps+=1
        if nxt==tau:
            es=ls-ds*tau;et=rt-dt*tau
            assert 0<es<2*a and 0<et<2*b
            assert 0<c-es/tau<c and 0<c-et/tau<c
            return {'tau':str(tau),'es':str(es),'et':str(et),'bad_source':es>=a,'bad_target':et>=b,'steps':steps}
        assert nxt>tau
        tau=nxt

result={'hypothesis':'Four fixed-point first-inner-wall phase choices always avoid both genuine outer-mouth corners AND artificial spine-cut reflections at M>=2max(a,b). Requires es<a and et<b, not merely inequality.','status':'no_counterexample_in_bounded_controls','patterns':0,'phase_runs':0,'started':started,'deadline':stop}
try:
    for vals in product(range(1,4),range(1,4),range(1,4),[F(1,2),F(1),F(2),F(3)], [F(1,2),F(1),F(2),F(3)], [F(1,3),F(1,2),F(2,3)], [F(1,3),F(1,2),F(2,3)],[F(0),F(1,2),F(1),F(3)]):
        c,a,b,ds,dt,fs,ft,extra=map(F,vals);bs=a*fs;xt=b*ft;m=2*max(a,b)+extra
        tests=[match(c,a,b,ds,dt,m,ps,pt) for ps,pt in product([a-bs,a+bs],[xt,2*b-xt])]
        result['patterns']+=1;result['phase_runs']+=4
        if all(t['bad_source'] or t['bad_target'] for t in tests):
            result.update(status='exact_mechanism_counterexample',inputs={k:str(v) for k,v in zip(['c','a','b','ds','dt','bs','xt','M'],[c,a,b,ds,dt,bs,xt,m])},four_results=tests);break
        if time.time()-started>35:
            result['status']='bounded_controls_terminal_no_counterexample';break
except TimeoutError as exc:result.update(status='deadline_stop_no_inference',reason=str(exc))
result['elapsed_seconds']=time.time()-started
(p/'separated-teeth-phase-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
