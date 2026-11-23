"""Exact projected intervals for the fixed RES strip certificate; no ray tracing."""
from fractions import Fraction as F
from math import floor, ceil

def merge(intervals):
    out = []
    for l,r in sorted(intervals):
        if out and l < out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1],r))
        else:
            out.append((l,r))
    return out

def intervals(B, minimum_a=0):
    q=(286*B/200).denominator
    step=F(200,q)
    windows=[]
    L=3+B
    error=10*L/(L+minimum_a)
    A=(11*L-error*(1+B))/2
    H=13*L-error*B
    limit=floor((H+3*A)/L)
    for t in range(-limit,limit+1):
        center=(209*B+1)*t
        l=center+max(-A,(-H-L*t)/3)
        r=center+min(A,(H-L*t)/3)
        if l>=r:
            continue
        for k in range(floor((13-r)/step),ceil((100-l)/step)+1):
            windows.append((l+k*step,r+k*step))
    return windows

def residual():
    # Direct rotations with denominator > 10 already illuminate all abscissas.
    near={F(i,q) for q in range(1,11) for i in range(1,1+143*q//10) if 10*i<143*q}
    return sorted(200*r/286 for r in near if (F(143,5)-r).denominator<=10)

if __name__=='__main__':
    rows=residual()
    failed=[b for b in rows if not any(l<=13 and r>=100 for l,r in merge(intervals(b)+intervals(20-b)))]
    assert len(rows)==142 and failed==[F(100,11)]
    b=failed[0]
    coarse=[(l,r) for l,r in merge(intervals(b)+intervals(20-b)) if r>13 and l<100]
    assert coarse==[(F(-395,22),F(395,22)),(F(485,22),F(1275,22)),(F(1365,22),F(3035,22))]
    minimum_a=coarse[0][1]-13
    sharp=merge(intervals(b,minimum_a)+intervals(20-b,minimum_a))
    cert=next((l,r) for l,r in sharp if l<=13 and r>=100)
    print('exceptional depths',len(rows),'after first pass',failed)
    print('minimum source travel',minimum_a,'final covering interval',cert)
