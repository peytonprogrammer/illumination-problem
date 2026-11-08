"""Produce a coordinate comparison data from the frozen verified room."""
from pathlib import Path
from collections import Counter,defaultdict
from functools import reduce
from math import gcd
import json,hashlib
D=Path(__file__).resolve().parent
src=D/'peer-fast-inputs/cand-2_2-1.json'
r=json.loads(src.read_text());tris=[[tuple(p) for p in t] for t in r['triangles']]
c=Counter(tuple(sorted((t[i],t[(i+1)%3]))) for t in tris for i in range(3))
g=defaultdict(list)
for (a,b),n in c.items():
 if n==1:g[a].append(b);g[b].append(a)
assert all(len(ns)==2 for ns in g.values())
start=min(g);cycle=[start];prev=None;cur=start
while True:
 nxt=next(x for x in sorted(g[cur]) if x!=prev)
 if nxt==start:break
 assert nxt not in cycle
 cycle.append(nxt);prev,cur=cur,nxt
assert len(cycle)==len(g)
def cross(a,b,c):return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
poly=[p for i,p in enumerate(cycle) if cross(cycle[i-1],p,cycle[(i+1)%len(cycle)])]
assert len(poly)==22
lengths=[abs(poly[i][0]-poly[i-1][0])+abs(poly[i][1]-poly[i-1][1]) for i in range(len(poly))]
assert all(poly[i][0]==poly[i-1][0] or poly[i][1]==poly[i-1][1] for i in range(len(poly)))
area2=abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])));assert area2==30
variants=[]
for swap in (False,True):
 for sx in (-1,1):
  for sy in (-1,1):
   def f(p):
    x,y=p[::-1] if swap else p
    return sx*x,sy*y
   ps=[f(p) for p in poly];ms=[f(p) for p in r['marked']]
   x0=min(x for x,y in ps);y0=min(y for x,y in ps);scale=reduce(gcd,lengths)
   ps=[((x-x0)//scale,(y-y0)//scale) for x,y in ps];ms=tuple(sorted(((x-x0)//scale,(y-y0)//scale) for x,y in ms))
   for direction in (ps,ps[::-1]):
    for i in range(len(ps)):variants.append((tuple(direction[i:]+direction[:i]),ms))
canonical=min(variants);fingerprint=hashlib.sha256(json.dumps(canonical,separators=(',',':')).encode()).hexdigest()
out=dict(status='PASS',input=str(src.relative_to(D)),input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),boundary=poly,marks=r['marked'],walls=22,unit_square_area=area2/2,sorted_wall_lengths=sorted(lengths),canonical_under='translations, D4 isometries, common integer wall-length scale, cyclic starting point, orientation and mark interchange',canonical_polygon=canonical[0],canonical_marks=canonical[1],fingerprint_sha256=fingerprint,priority_status='unresolved')
(D/'priority-followup.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
