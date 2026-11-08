"""Prescribed controls of the analytic single-triangle portal return formula."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'inputs'))
from exact import run
w=F(1);V=[(0,0),(1,0),(0,1)];rows=[]
for x,a,b in [(F(1,3),F(2),F(1)),(F(4,5),F(-3,5),F(1)),(F(1,4),F(-2),F(1)),(F(1,3),F(1,10),F(1)),(F(1,3),F(0),F(1))]:
 ty=2*w/b;tx=(w-x)/a if a>0 else (w+x)/(-a) if a<0 else None
 assert tx!=ty
 if tx is None or ty<tx:
  z=x+a*ty;assert z!=0 and abs(z)<w
  end=(abs(z),F(0));out=((1 if z>0 else -1)*a,-b);tau=ty
 else:
  z=w-b*tx;assert z!=0 and abs(z)<w
  end=(abs(z),F(0));out=(-(1 if z>0 else -1)*b,-abs(a));tau=tx
 dd,P=run(V,(x,0),end,B=8,dirs=[(a,b)])
 assert P is not None and len(P)-2<=5
 actual=(P[-1][0]-P[-2][0],P[-1][1]-P[-2][1])
 assert actual[0]*out[1]==actual[1]*out[0] and sum(actual[k]*out[k] for k in (0,1))>0
 # All contacts strictly avoid the three physical triangle vertices.
 assert not set(P[1:-1])&set(V)
 rows.append({'entry':str(x),'velocity':[str(a),str(b)],'exit':str(end[0]),'exit_velocity':[str(q) for q in out],'reflections':len(P)-2})
result={'status':'PASS','controls':rows,'scope':'Five analytically prescribed controls of the triangle return lemma. No scanned directions or room search. General lemma is proved by square unfolding, not inferred from controls.'}
(HERE/'triangle-return.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
