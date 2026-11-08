"""Finite exact endpoint exceptions on uniformly sampled short relation lines."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import importlib.util,json,time,signal,hashlib
B=Path(__file__).parent;E=json.loads((B/'short-line-finite-effort.json').read_text());margin=json.loads((B/'short-line-margin.json').read_text())
spec=importlib.util.spec_from_file_location('frozen_cover',B/'finite-short-cover.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def timeout(*_):raise TimeoutError('original short-line finite classification deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
progress={'phase_pairs_checked':0,'q_completed':2};exceptions=[]
def save(status):
    out={'status':status,'progress':progress,'exceptional_phase_count':len(exceptions),'exceptions':exceptions,'effort':E,
         'margin_sha256':hashlib.sha256((B/'short-line-margin.json').read_bytes()).hexdigest(),
         'frozen_helper_sha256':hashlib.sha256((B/'finite-short-cover.py').read_bytes()).hexdigest(),
         'scope':'Finite20goodshortlines outside10criticalfamilies; uniform margin/sampling proof and independent review needed. FullgoalOPEN.'}
    (B/'short-line-finite.json').write_text(json.dumps(out,indent=2)+'\n');return out

def main():
    critical=[x for x in margin['rows'] if x['closed_blind_pieces']];good=[x for x in margin['rows'] if not x['closed_blind_pieces']]
    for q in range(3,E['q_max']+1):
      for A in range(1,q-1):
       for C in range(A+1,q):
        if gcd(gcd(A,C),q)!=1:continue
        matches=lambda x:x['relation'][0]*A+x['relation'][1]*C==x['relation'][2]*q
        if any(matches(x) for x in critical):continue
        gs=[x for x in good if matches(x)]
        if not gs or q>min(x['rational_phase_cutoff'] for x in gs):continue
        pieces=[[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]]
        for guards,info in m.guards(A,C,q):
            out={}
            for P in pieces:
                for Q in m.subtract(P,guards):
                    if m.admissible(Q):out[m.key(Q)]=Q
            pieces=list(out.values())
            if not pieces:break
        progress['phase_pairs_checked']+=1
        if pieces:
            reps=[]
            for P in pieces:
                s=sum(v[0] for v in P)/len(P);t=sum(v[1] for v in P)/len(P);m.verify_failure(A,C,q,s,t);reps.append([str(s),str(t)])
            exceptions.append({'phase':[A,C,q],'depths':[str(F(A,C-A)),str(F(q-C,C-A))],
                               'closed_failure_pieces':[[[str(x),str(y)] for x,y in P] for P in pieces],
                               'exact_failure_representatives':reps,'axis_boundaries_excluded':True})
      progress['q_completed']=q;save('PARTIAL_PREFIX_ONLY')
    out=save('COMPLETE_FINITE_GOOD_LINE_EXCEPTION_SUPPORT');print(json.dumps({k:v for k,v in out.items() if k!='exceptions'}));print('exceptional depths',[x['depths'] for x in exceptions])
if __name__=='__main__':
    try:main()
    except TimeoutError:
        out=save('ORIGINAL_DEADLINE_REACHED_PARTIAL_PREFIX_ONLY');print(json.dumps({k:v for k,v in out.items() if k!='exceptions'}))
