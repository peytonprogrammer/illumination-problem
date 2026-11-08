"""Bounded rational discovery screen of four specified endpoint-cap sheets.
Complete arithmetic periods of those charts, NOT all billiard trajectories.
"""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
import json,time
B=Path(__file__).parent
E=json.loads((B/'cap-chart-effort.json').read_text())
DEADLINE=E['deadline']
def guard():
    if time.time()>=DEADLINE:raise TimeoutError('original aggregate840s deadline')

def solve(s,t,a,b,hm,hp):
    tried=0;sheets=[]
    for lc,uc in ((0,0),(0,1),(1,0),(1,1)):
        A=2*hm-a if lc else a;C=2*hp-b if uc else b;H=A+1+C
        alpha,beta=A/H,(A+1)/H
        capl=(A-hm)/H if lc else None
        capu=(A+1+hp)/H if uc else None
        Q=lcm(*(x.denominator for x in [alpha,beta,capl,capu] if x is not None))
        sheets.append({'lower_cap':lc,'upper_cap':uc,'period':Q})
        for u in (0,2):
            for eps in (1,-1):
                for M in range(Q):
                    guard();tried+=1
                    L=u+eps*t+4*M;D=L-s
                    e1=(s+alpha*D)%4;e2=(s+beta*D)%4
                    c=1 if 1<e1<2 else 3 if 2<e1<3 else None
                    if c is None:continue
                    lo,hi={(0,1):(1,2),(0,3):(2,3),(2,1):(0,1),(2,3):(3,4)}[u,c]
                    if not lo<e2<hi:continue
                    if lc and (s+capl*D)%2==0:continue
                    if uc and (s+capu*D-u)%2==0:continue
                    return {'lc':lc,'uc':uc,'u':u,'epsilon':eps,'M':M,'c':c,'period':Q},tried,sheets
    return None,tried,sheets

def main():
    params=[];attempts=0;failures=[];counts={};passed=0
    depths=list(map(F,['1/4','1/2','1','3/2','2']))
    gaps=list(map(F,['1/4','1/2','1']))
    pairs=[(F(s),F(t)) for s,t in [('1','1'),('1','1/2'),('1/2','1/2'),('1','1/4'),('1/2','1/4'),('1/4','1/4')]]
    for a in depths:
      for b in depths:
       for da in gaps:
        for db in gaps:
         for s,t in pairs:
            guard();hm,hp=a+da,b+db
            hit,n,sheets=solve(s,t,a,b,hm,hp);attempts+=n
            rec=dict(zip(['s','t','a','b','hm','hp'],map(str,[s,t,a,b,hm,hp])))
            if hit:
                passed+=1;k=str((hit['lc'],hit['uc']));counts[k]=counts.get(k,0)+1
            else:
                rec['sheets']=sheets;failures.append(rec)
                out={'status':'COUNTEREXAMPLE_TO_FOUR_SHEET_MECHANISM','effort':E,
                     'tested_parameter_pairs':passed+len(failures),'covered':passed,
                     'arithmetic_chart_tests':attempts,'first_selected_sheet_counts':counts,
                     'failures':failures,'scope':'No darkness inference. Complete chart periods only for four chosen sheet families.'}
                (B/'cap-chart-screen.json').write_text(json.dumps(out,indent=2)+'\n')
                print(json.dumps(out));return
    out={'status':'ALL_PRESCRIBED_RATIONAL_CONTROLS_COVERED','effort':E,
         'tested_parameter_pairs':passed,'arithmetic_chart_tests':attempts,
         'first_selected_sheet_counts':counts,'failures':[],
         'scope':'Discovery controls only, NOT a continuous-parameter proof.'}
    (B/'cap-chart-screen.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
