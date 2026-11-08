"""Exact finite endpoint-cover audit after a hand irrational-circle reduction.
Discovery question only until the hand reduction and output are independently reviewed.
Same original cap effort deadline, not a renewed allowance.
"""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json,time
B=Path(__file__).parent;deadline=json.loads((B/'cap-chart-effort.json').read_text())['deadline']
def guard():
    if time.time()>=deadline:raise TimeoutError('original840s aggregate deadline')
def value(g,s,t):return g[0]*s+g[1]*t+g[2]
def norm(g):
    v=next(x for x in g if x);return tuple(x/v for x in g)
def audit(m,n,r):
    V=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1))];cs=[]
    boxes=[(0,1,(1,2),(1,2)),(0,3,(2,3),(2,3)),(2,1,(1,2),(0,1)),(2,3,(2,3),(3,4))]
    for u,c,i,j in boxes:
     lo=m*i[m<0]+n*j[n<0];hi=m*i[m>=0]+n*j[n>=0]
     assert hi-lo==abs(m)+abs(n)
     for sign in (1,-1):
      C=(F(m+n-r),F(r*sign),F(r*u))
      for k in range(-9,10):
       gs=[(C[0],C[1],C[2]+4*k-lo),(-C[0],-C[1],hi-C[2]-4*k)]
       if any(max(value(g,*P) for P in V)<=0 for g in gs):continue
       cs.append({'u':u,'sign':sign,'c':c,'k':k,'guards':gs})
    lines={norm(g) for c in cs for g in c['guards'] if any(g)}
    lines|={(F(1),F(0),F(0)),(F(1),F(0),F(-1)),(F(0),F(1),F(0)),(F(1),F(-1),F(0))}
    ls=sorted(lines);xs={F(0),F(1)}
    for i,(a,b,c) in enumerate(ls):
      if b==0 and a and 0<=-c/a<=1:xs.add(-c/a)
      for A,Bb,C in ls[i+1:]:
       det=a*Bb-b*A
       if det:
        x=(b*C-c*Bb)/det
        if 0<=x<=1:xs.add(x)
    z=sorted(xs);xx=sorted(xs|{(a+b)/2 for a,b in zip(z,z[1:])});bad=[];cnt=0
    for s in xx:
      guard()
      if not s:continue
      ys={F(0),s}
      for a,b,c in ls:
       if b:
        t=-(a*s+c)/b
        if 0<=t<=s:ys.add(t)
      z=sorted(ys)
      for t in sorted(ys|{(a+b)/2 for a,b in zip(z,z[1:])}):
       if not t:continue
       cnt+=1
       if not any(all(value(g,s,t)>0 for g in c['guards']) for c in cs):bad.append([str(s),str(t)])
    return {'relation':[m,n,r],'clauses':len(cs),'sign_cells':cnt,'uncovered':bad}
def main():
    out=[]
    for m in range(0,5):
      for n in range(-4,5):
       if not 0<abs(m)+abs(n)<=4 or (m==0 and n<=0):continue
       lo,hi=min(0,n,m+n),max(0,n,m+n)
       for r in range(lo+1,hi):
        if gcd(gcd(m,abs(n)),abs(r))!=1:continue
        guard();out.append(audit(m,n,r))
    result={'status':'FINITE_AUDIT_COMPLETE','relations':len(out),'results':out,
            'scope':'Connected-kernel endpoint affine coverage only; HAND density reduction pending review. Rational finite orbits NOT covered.'}
    (B/'phase-lines-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'relations':len(out),'uncovered_relations':[r for r in out if r['uncovered']]}))
if __name__=='__main__':main()
