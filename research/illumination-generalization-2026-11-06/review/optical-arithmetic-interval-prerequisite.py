#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json

def floor(q):return q.numerator//q.denominator
def ceil(q):return -floor(-q)
def labels(A,B):
 assert A<B
 lo,hi=floor(A)+1,ceil(B)-1
 return list(range(lo,hi+1))

fixtures=[(F(0),F(1),[]),(F(-1),F(0),[]),(F(0),F(2),[1]),(F(-2),F(0),[-1]),(F(1,4),F(5,4),[1]),(F(-5,4),F(-1,4),[-1]),(F(1,10),F(9,10),[]),(F(9,10),F(11,10),[1])]
rows=[]
for A,B,expected in fixtures:
 got=labels(A,B);assert got==expected
 assert len(got)==max(0,ceil(B)-floor(A)-1)
 rows.append({'A':str(A),'B':str(B),'labels':got})
branches=[]
for w,K,alpha,beta,eps,J,expected in [(F(8),F(40),F(2),F(6),1,(F(-2,5),F(2,5)),[-1,0]),(F(8),F(40),F(2),F(6),-1,(F(-2,5),F(2,5)),[0,1]),(F(16),F(106),F(4),F(6),1,(F(1,100),F(3,100)),[0]),(F(16),F(706),F(4),F(54),1,(F(7,100),F(9,125)),[0])]:
 A=(K*J[0]+alpha-eps*beta)/(2*w);B=(K*J[1]+alpha-eps*beta)/(2*w)
 ns=labels(A,B);assert ns==expected
 roots=[(2*n*w+eps*beta-alpha)/K for n in ns]
 assert all(J[0]<m<J[1] for m in roots)
 branches.append({'epsilon':eps,'K':str(K),'J':[str(x) for x in J],'A':str(A),'B':str(B),'labels':ns,'roots':[str(x) for x in roots]})
out={'status':'PASS_STRICT_OPEN_PREREQUISITE_CHECKS','endpoint_cases':rows,'signed_prescribed_branches':branches,'global_coverage_proved':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
