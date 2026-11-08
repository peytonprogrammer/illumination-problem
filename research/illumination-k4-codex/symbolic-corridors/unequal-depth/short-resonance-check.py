"""Falsify a specified short-annihilator premise, with original aggregate deadline."""
from pathlib import Path
from math import gcd
from fractions import Fraction as F
import json,time,signal
B=Path(__file__).parent;E=json.loads((B/'short-resonance-effort.json').read_text())
def alarm(*_):raise TimeoutError('original840second aggregate effort deadline')
signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))

def exact_failure(A,C,q,s,t):
    witnesses=[]
    for u in (0,2):
      for eps in (1,-1):
       for M in range(q):
        x=((q-A)*s+A*(u+eps*t+4*M))/q%4
        y=((q-C)*s+C*(u+eps*t+4*M))/q%4
        c=1 if 1<x<2 else 3 if 2<x<3 else None
        if c is None:continue
        lo,hi={(0,1):(1,2),(0,3):(2,3),(2,1):(0,1),(2,3):(3,4)}[u,c]
        if lo<y<hi:witnesses.append((u,eps,M,c))
    assert not witnesses
    return 4*q

def main():
    D=E['endpoint_grid_denominator'];pairs=[(i,j) for i in range(1,D+1) for j in range(1,D+1)]
    tested=0;skipped=0
    normals=[(m,n) for m in range(-4,5) for n in range(-4,5) if 0<abs(m)+abs(n)<=4]
    for q in range(3,E['phase_denominator_cap']+1):
      for A in range(1,q-1):
       for C in range(A+1,q):
        if gcd(gcd(A,C),q)!=1:continue
        if any((m*A+n*C)%q==0 for m,n in normals):skipped+=1;continue
        tested+=1;alive=list(pairs);scale=D*q
        for M in range(q):
          for u in (0,2):
           for eps in (1,-1):
            remaining=[]
            for i,j in alive:
                x=((q-A)*i+A*(D*u+eps*j+4*D*M))%(4*scale)
                y=((q-C)*i+C*(D*u+eps*j+4*D*M))%(4*scale)
                if u==0:hit=(scale<x<2*scale and scale<y<2*scale) or (2*scale<x<3*scale and 2*scale<y<3*scale)
                else:hit=(scale<x<2*scale and 0<y<scale) or (2*scale<x<3*scale and 3*scale<y<4*scale)
                if not hit:remaining.append((i,j))
            alive=remaining
          if not alive:break
        if alive:
            i,j=alive[0];s,t=F(i,D),F(j,D)
            evaluations=exact_failure(A,C,q,s,t)
            out={'status':'SHORT_NORM4_PREMISE_REFUTED','phase':[A,C,q],'s':str(s),'t':str(t),'a':str(F(A,C-A)),'b':str(F(q-C,C-A)),
                 'exact_all_chart_evaluations':evaluations,'short_normal_count':len(normals),'tested_phase_pairs':tested,'skipped_short_relation_pairs':skipped,
                 'scope':'Vertical-only mechanism failure with no annihilator l1<=4; NOTdarkness or four-cap failure.','effort':E}
            (B/'short-resonance-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));return
    out={'status':'NO_COUNTEREXAMPLE_IN_BOUNDED_CONTROLS','tested_phase_pairs':tested,'skipped_short_relation_pairs':skipped,'endpoint_pairs_per_phase':D*D,'scope':'Not a universal short-resonance proof.','effort':E}
    (B/'short-resonance-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
    try:main()
    except TimeoutError:
        out={'status':'ORIGINAL_DEADLINE_REACHED','effort':E};(B/'short-resonance-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
