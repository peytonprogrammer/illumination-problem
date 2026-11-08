"""Complete finite phase-support certificate after the uniform lattice reduction."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import importlib.util,json,time,signal,hashlib
B=Path(__file__).parent;E=json.loads((B/'exceptional-phase-support-effort.json').read_text())
spec=importlib.util.spec_from_file_location('frozen_exact_clip',B/'finite-short-cover.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
# This is a distinct full-support classification after the previous premise was refuted.
# The imported helper has no running job; install THIS effort's persisted aggregate deadline.
def timeout(*_):raise TimeoutError('original exceptional-support aggregate deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
progress={'phase_pairs_checked':0,'q_completed':2,'max_residual_pieces':1,'guard_clauses_applied':0};exceptions=[]

def save(status):
    out={'status':status,'progress':progress,'exceptional_phase_count':len(exceptions),'exceptions':exceptions,'effort':E,
         'frozen_helper_sha256':hashlib.sha256((B/'finite-short-cover.py').read_bytes()).hexdigest(),
         'scope':'Finite q<=100 outside short relation lines. Combine ONLY with independently reviewed lattice-sampling lemma for unbounded conclusion. Full room remainsopen.'}
    (B/'exceptional-phase-support.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

def main():
    m.sanity();normals=[(a,c) for a in range(-4,5) for c in range(-4,5) if 0<abs(a)+abs(c)<=4]
    for q in range(3,E['q_max']+1):
      for A in range(1,q-1):
       for C in range(A+1,q):
        if gcd(gcd(A,C),q)!=1 or any((a*A+c*C)%q==0 for a,c in normals):continue
        pieces=[[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]]
        for gs,info in m.guards(A,C,q):
            result={}
            for P in pieces:
                for R in m.subtract(P,gs):
                    if m.admissible(R):result[m.key(R)]=R
            pieces=list(result.values());progress['guard_clauses_applied']+=1
            progress['max_residual_pieces']=max(progress['max_residual_pieces'],len(pieces))
            if not pieces:break
        progress['phase_pairs_checked']+=1
        if pieces:
            reps=[]
            for P in pieces:
                s=sum(p[0] for p in P)/len(P);t=sum(p[1] for p in P)/len(P)
                assert 0<s<=1 and 0<t<=1;m.verify_failure(A,C,q,s,t);reps.append([str(s),str(t)])
            exceptions.append({'phase':[A,C,q],'depths':[str(F(A,C-A)),str(F(q-C,C-A))],
                               'closed_failure_pieces':[[[str(x),str(y)] for x,y in P] for P in pieces],
                               'exact_failure_representatives':reps,'axis_boundaries_excluded':True})
      progress['q_completed']=q;save('PARTIAL_PREFIX_ONLY')
    out=save('COMPLETE_FINITE_EXCEPTIONAL_PHASE_SUPPORT');print(json.dumps({k:v for k,v in out.items() if k not in ('exceptions',)}))
if __name__=='__main__':
    try:main()
    except TimeoutError:
        out=save('ORIGINAL_DEADLINE_REACHED_PARTIAL_PREFIX_ONLY');print(json.dumps({k:v for k,v in out.items() if k not in ('exceptions',)}))
