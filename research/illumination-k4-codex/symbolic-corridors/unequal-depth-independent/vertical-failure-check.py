"""Exact full-period validation of three explicit peer mechanism failures.
No parameter sweep or replacement-trajectory discovery.
"""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
BOXES=[(0,1,(1,2),(1,2)),(0,3,(2,3),(2,3)),(2,1,(1,2),(0,1)),(2,3,(2,3),(3,4))]

def main():
    rows=[];alltests=0
    for a,b in [(F(1,2),F(1,2)),(F(1,2),F(1)),(F(1),F(1,2))]:
        H=a+1+b;al=a/H;be=(a+1)/H;q=lcm(al.denominator,be.denominator)
        table=[]
        for k in range(2*q):
            x=(1+2*k*al)%4;y=(1+2*k*be)%4
            choices=[]
            for u,c,I,J in BOXES:
                if I[0]<x<I[1] and J[0]<y<J[1]:choices.append((u,c))
            assert not choices,(a,b,k,x,y,choices)
            graph=((1<x<2 and (0<y<1 or 1<y<2)) or (2<x<3 and (2<y<3 or 3<y<4)))
            assert not graph
            table.append({'odd_lift':2*k+1,'first_portal_residue':str(x),'second_portal_residue':str(y),'admissible':False})
        # Directly cross-check ALL four charts and both target signs, periodq.
        for u,c,I,J in BOXES:
            for eps in (1,-1):
                for M in range(q):
                    D=u+eps+4*M-1;x=(1+al*D)%4;y=(1+be*D)%4
                    assert not (I[0]<x<I[1] and J[0]<y<J[1]);alltests+=1
        rows.append({'a':str(a),'b':str(b),'alpha':str(al),'beta':str(be),'period':q,'odd_lift_period':2*q,'whole_period_failure':True,'table':table})
    sources=['unequal-depth/center-failure-graph.py','unequal-depth/center-failure-graph.json','unequal-depth-independent/midpoint-review.md']
    pins={r:hashlib.sha256((BASE/r).read_bytes()).hexdigest() for r in sources}
    pins['unequal-depth-independent/vertical-failure-check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out={'status':'EXPLICIT_VERTICAL_ONLY_FAILURES_VERIFIED','pairs':3,'direct_chart_tests':alltests,'source_sha256':pins,'records':rows,'limits':'Necessity rests on the independent hand unfolding argument. Finite controls do not classify all depth parameters or prove darkness. No peer code executed.'}
    (HERE/'vertical-failure-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k not in ('records','source_sha256')})
if __name__=='__main__':main()
