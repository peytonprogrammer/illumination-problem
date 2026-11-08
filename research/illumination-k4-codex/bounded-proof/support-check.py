"""Rebuild all finite supports independently; no room or ray search."""
from pathlib import Path
from itertools import combinations,product
import json
HERE=Path(__file__).resolve().parent;N=((1,0),(-1,0),(0,1),(0,-1))

def neighbors(S):return {(x+a,y+b) for x,y in S for a,b in N}
def canonical(S):
 images=[]
 for flip in (False,True):
  for sx,sy in product((-1,1),repeat=2):
   T={(sx*(p[1] if flip else p[0]),sy*(p[0] if flip else p[1])) for p in S}
   for a,b in T:images.append(tuple(sorted((x-a,y-b) for x,y in T)))
 return min(images)
def support(F,cap):
 R=F|neighbors(F);b=len(R-F);out=set(R)
 for i in range(cap-b):out|=neighbors(out)
 return R,out,b
rows=[]
for d in range(2,7):
 for x in range((d+1)//2,d+1):
  F={(0,0),(x,d-x)};R,S,b=support(F,11)
  rows.append(dict(I=2,full=sorted(F),mandatory=sorted(R),allowed=sorted(S),b=b,mark_pairs=[[(0,0),(x,d-x)]]))
D={(x,y) for x in range(-4,5) for y in range(-4,5) if 0<abs(x)+abs(y)<=4};shapes=set();rooted=0;rooted_after_cap=0
for a,b in combinations(sorted(D),2):
 F={(0,0),a,b};seen={(0,0)}
 while True:
  nxt=seen|{q for p in seen for q in F if abs(p[0]-q[0])+abs(p[1]-q[1])<=2}
  if nxt==seen:break
  seen=nxt
 if seen!=F:continue
 rooted+=1
 if len(neighbors(F)-F)<=9:rooted_after_cap+=1;shapes.add(canonical(F))
for shape in sorted(shapes):
 F=set(shape);R,S,b=support(F,9)
 pairs=[list(p) for p in combinations(shape,2) if sum(abs(a-b) for a,b in zip(*p))>1]
 rows.append(dict(I=3,full=sorted(F),mandatory=sorted(R),allowed=sorted(S),b=b,mark_pairs=pairs))
observed=json.loads((HERE/'inputs/branch-support.json').read_text())['cases']
assert len(rows)==len(observed)==22
for r,o in zip(rows,observed):
 for key in r:assert json.dumps(r[key])==json.dumps(o[key]),(o['tag'],key)
result=dict(status='PASS',support_cases=len(rows),marked_pairs=sum(len(r['mark_pairs']) for r in rows),rooted_triples=rooted,rooted_triples_after_b_cap=rooted_after_cap,
 scope='Necessary supports for W<=23,k<=4, conservatively containing W<=21,k<=4; geometry only.')
(HERE/'support-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
