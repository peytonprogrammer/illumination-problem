"""Exact prescribed all-A placement/classification controls; not a proof of unseen rooms."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from itertools import combinations
import importlib.util,json
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def polygon(G,left,right):
 p=[(0,0),(1,0)]
 for lo,hi,w in right:
  if p[-1]!=(1,lo):p.append((1,lo))
  p.extend([(1+w,lo),(1+w,hi),(1,hi)])
 if p[-1]!=(1,G):p.append((1,G))
 p.append((0,G))
 for lo,hi,w in reversed(left):p.extend([(0,hi),(-w,hi),(-w,lo),(0,lo)])
 while True:
  if p[-1]==p[0]:p.pop()
  drop=next((i for i in range(len(p)) if p[i]==p[i-1] or g.det(g.vec(p[i-1],p[i]),g.vec(p[i],p[(i+1)%len(p)]))==0),None)
  if drop is None:break
  p.pop(drop)
 g.simple(p);return p
fixtures=[('rectangleG2',2,[(0,2,7)],[(0,2,6)]),('A0',16,[(6,8,7),(10,12,8)],[(1,3,2),(13,15,2)]),('A1',19,[(6,8,8),(11,13,7)],[(1,3,3),(13,15,3)]),('B',8,[(0,2,5),(4,6,7)],[(1,3,2),(5,7,2)]),('C1',12,[(0,2,7),(5,7,6),(10,12,8)],[(2,4,3),(6,8,3)]),('C2',14,[(0,2,6),(7,9,7),(12,14,8)],[(4,6,1),(8,10,1)]),('D',8,[(0,2,7),(3,5,9),(6,8,8)],[(0,2,3),(4,6,3)]),('other',24,[(2,4,7),(9,11,8),(18,20,6)],[(0,2,5),(6,8,7)])]
rows=[];totals=Counter()
for name,G,left,right in fixtures:
 V=polygon(G,left,right);N=sum(lo>0 and hi<G for lo,hi,w in left+right);F=sum((lo==0)^(hi==G) for lo,hi,w in left+right)
 if G>2:assert len(V)==4+4*N+2*F
 for shiftx in [0,1]:
  for shifty in [0,1]:
   points=[];data={}
   for x in range(min(z[0] for z in V),max(z[0] for z in V)+1):
    for y in range(G+1):
     if (x+shiftx)%2 or (y+shifty)%2 or g.location(V,(x,y))!=1:continue
     assert not 0<x<1
     side='L' if x<=0 else 'R';bands=left if side=='L' else right
     matches=[(i,lo,hi,w) for i,(lo,hi,w) in enumerate(bands) if lo<y<hi]
     assert len(matches)==1;i,lo,hi,w=matches[0];D=-x if side=='L' else x-1
     assert y==lo+1 and 0<=D<w
     points.append((x,y));data[x,y]=(side,i,D,w)
   categories=Counter()
   for S,T in combinations(points,2):
    ss,si,ds,ws=data[S];ts,ti,dt,wt=data[T]
    if ss==ts and si==ti:cat='same-tooth visible'
    elif ss!=ts:cat='opposite protected midpoint'
    elif ds!=dt:assert (ds-dt)%2==0;cat='unequal-depth whole theorem'
    elif ds>=3 or max(ws,wt)>=ds+2:cat='R43 generic equal-depth'
    else:
     assert ds in [0,1,2] and ws==wt==ds+1
     s,t=sorted([S[1],T[1]]);h=Q(t-s,2);mu=Q(s+t,2);assert h.denominator==mu.denominator==1 and h>=2
     opposite=right if ss=='L' else left;levels={h,mu,G-mu,G-h};forced=all(any(z==lo or z==hi for lo,hi,w in opposite) for z in levels)
     if not forced:cat='A38 direct chart'
     else:
      q=min(s,G-t)
      if len(V)<=21:
       assert not(h>=3 and q in [1] or h>=3 and q>=3)
       cat='four-band' if h>=3 else 'h2 A1/B/C/D'
      else:cat='outside wall bound'
    categories[cat]+=1;totals[cat]+=1
   rows.append({'fixture':name,'original_A_shift':[shiftx,shifty],'walls':len(V),'interior_A_count':len(points),'pairs':sum(categories.values()),'categories':dict(categories)})
out={'status':'ALL_PRESCRIBED_ORIGINAL_A_PLACEMENT_CONTROLS_PASS','fixtures':len(fixtures),'coordinate_parity_charts':len(rows),'actual_A_pairs':sum(totals.values()),'categories':dict(totals),'rows':rows,'discovery':False,'whole_goal_complete':False,'limits':'Finite controls only. Unbounded all-A placement and entire-room charge proof is c1-arbitrary-width-join-proof.md; pending independent review and listed dependencies.'}
(R/'c1-arbitrary-width-join-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
