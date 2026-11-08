"""Prescribed independent arithmetic check; no optical author execution."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent/'review'
req=json.loads((R/'unequal-seam-phase-review-request.json').read_text())
pins={name:hashlib.sha256((R/name).read_bytes()).hexdigest()==value for name,value in req['source_sha256'].items()};assert all(pins.values())
rows=0
for c in range(1,21):
 for w in range(1,21):
  q=F(w,c)
  for H in [F(2),F(7,2),F(8),F(13)]:
   n=(q*(H-F(1,2))+F(1,2))//1
   lower=q*H-(1+q)/2;upper=q*H+(1+q)/2
   assert lower<n<upper and n-1<=lower
   assert (q*(H+n)/(1+q)+F(1,2))//1==n
   m=(q*H-n)/(1+q);assert -F(1,2)<m<F(1,2)
   j=0
   while True:
    nj=(q*(H+j)/(1+q)+F(1,2))//1
    assert j<=nj<=n
    if nj==j:break
    j=nj
   assert j==n;rows+=1
out={'status':'INDEPENDENT_ARITHMETIC_AND_PINS_PASS','controls':rows,'source_pins_current':pins,'actual_path_replay':False,'author_optical_code_executed':False}
(P/'unequal-seam-phase-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
