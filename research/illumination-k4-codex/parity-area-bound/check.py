"""Exact canonical tile/angle census on frozen controls; no room enumeration."""
from pathlib import Path
from collections import Counter,deque
from itertools import combinations
import json,math,hashlib
B=Path(__file__).resolve().parent
IN=B.parent/'isolation-review/inputs'

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def label(v):return 'A' if not(v[0]%2 or v[1]%2) else 'B' if v[0]%2 and v[1]%2 else 'C'
def primitive(v):
 g=math.gcd(*map(abs,v));return (v[0]//g,v[1]//g),g
DIRECTIONS={(1,0):0,(1,1):1,(0,1):2,(-1,1):3,(-1,0):4,(-1,-1):5,(0,-1):6,(1,-1):7}

def census(room):
 original=[tuple(map(tuple,t)) for t in room['triangles']];squares={}
 for t in original:
  box=(min(v[0] for v in t),min(v[1] for v in t));squares.setdefault(box,[]).append(t)
 tris=[];retiled=0
 for (x,y),group in squares.items():
  if len(group)==1:tris.extend(group);continue
  assert len(group)==2
  common=set(group[0])&set(group[1]);assert len(common)==2
  a,b=common;assert abs(a[0]-b[0])==abs(a[1]-b[1])==1
  c=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
  assert set(group[0])|set(group[1])==set(c)
  replacement=[(c[0],c[1],c[2]),(c[0],c[2],c[3])] if (x-y)%2==0 else [(c[1],c[2],c[3]),(c[1],c[3],c[0])]
  retiled+=set(map(frozenset,group))!=set(map(frozenset,replacement));tris.extend(replacement)
 assert len(tris)==len(original)
 assert len({tuple(sorted(t)) for t in tris})==len(tris)
 incidence=Counter();edges=Counter();owners={}
 for i,t in enumerate(tris):
  assert Counter(map(label,t))==Counter('ABC')
  lengths=sorted(sum((a[j]-b[j])**2 for j in (0,1)) for a,b in combinations(t,2));assert lengths==[1,1,2]
  c=next(v for v in t if label(v)=='C');other=[v for v in t if v!=c];assert sum((v[0]-c[0])*(w[0]-c[0])+(v[1]-c[1])*(w[1]-c[1]) for v,w in [(other[0],other[1])])==0
  for v in t:incidence[v]+=2 if label(v)=='C' else 1
  for edge in combinations(t,2):
   e=tuple(sorted(edge));edges[e]+=1;owners.setdefault(e,[]).append(i)
 assert all(n in (1,2) for n in edges.values())
 adj={}
 for (a,b),n in edges.items():
  if n==1:adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
 strict_boundary=all(len(v)==2 for v in adj.values())
 if 'vertices' in room:vs=list(map(tuple,room['vertices']))
 else:
  assert strict_boundary;v=min(adj);start=v;old=None;cycle=[v]
  while True:
   nxt=min(x for x in adj[v] if x!=old)
   if nxt==start:break
   assert nxt not in cycle;cycle.append(nxt);old,v=v,nxt
  assert len(cycle)==len(adj)
  vs=[v for i,v in enumerate(cycle) if cross(sub(v,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],v))]
 if sum(cross(a,b) for a,b in zip(vs,vs[1:]+vs[:1]))<0:vs.reverse()
 corners=[]
 for i,v in enumerate(vs):
  incoming,_=primitive(sub(vs[i-1],v));outgoing,_=primitive(sub(vs[(i+1)%len(vs)],v));angle=(DIRECTIONS[incoming]-DIRECTIONS[outgoing])%8
  assert angle in (1,2,3,5,6,7);corners.append((v,angle))
 W=len(vs);N=len(tris);A_angle=sum(a for v,a in corners if label(v)=='A')
 assert sum(a for v,a in corners)==4*(W-2)
 actual=set(vs);smooth_nonA=[v for v in incidence if label(v)!='A' and v not in actual and v in adj];interior_nonA=[v for v in incidence if label(v)!='A' and v not in adj]
 assert all(incidence[v]==4 for v in smooth_nonA)
 assert all(incidence[v]==8 for v in interior_nonA)
 correction=4*len(smooth_nonA)+8*len(interior_nonA)
 assert 4*(W-2)==3*N+A_angle-correction
 parity=not correction
 if parity:
  assert 3*N+A_angle==4*(W-2)
  for a,b in zip(vs,vs[1:]+vs[:1]):assert primitive(sub(b,a))[1]<=2
 graph=[set() for t in tris]
 for indices in owners.values():
  if len(indices)==2:a,b=indices;graph[a].add(b);graph[b].add(a)
 root=tuple(room['marked'][0]);assert label(root)=='A'
 star=[i for i,t in enumerate(tris) if root in t]
 rooted=None
 if root not in adj:
  assert len(star)==8;dist={i:0 for i in star};q=deque(star)
  while q:
   i=q.popleft()
   for j in graph[i]:
    if j not in dist:dist[j]=dist[i]+1;q.append(j)
  assert len(dist)==N
  assert max(dist.values())<=N-8
  maxcoordinate=max(abs(v[j]-root[j]) for t in tris for v in t for j in (0,1));assert maxcoordinate<=N-7
  rooted=dict(root=root,star_tiles=8,max_dual_distance=max(dist.values()),dual_distance_cap=N-8,max_coordinate=maxcoordinate,coordinate_cap=N-7)
 return dict(walls=W,triangles=N,internal_diagonals_canonicalized=retiled,strict_boundary=strict_boundary,parity=parity,A_corner_angle_units=A_angle,smooth_non_A=len(smooth_nonA),interior_non_A=len(interior_nonA),identity=[4*(W-2),3*N+A_angle-correction],tile_cap=(4*W-8)//3,rooted=rooted)

def main():
 results=[];inputs={}
 for name in ['room-illumination-search-simple-unrestricted','room-tokarsky34','room-jain28','room-wolecki22-pinch','known22']:
  p=IN/(name+'.json');inputs[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();d=census(json.loads(p.read_text()));d['room']=name;results.append(d)
 assert all(d['parity'] for d in results[:-1]) and not results[-1]['parity']
 assert results[-1]['triangles']>results[-1]['tile_cap']
 result=dict(status='PASS',controls=results,caps=[dict(walls=W,max_triangles=(4*W-8)//3,max_square_area_numerator=(4*W-8)//3,max_square_area_denominator=2,root_star_distance_cap=(4*W-8)//3-8,root_coordinate_cap=(4*W-8)//3-7) for W in [21,26]],input_hashes=inputs,scope='Identity and rooted-radius controls on frozen rooms; no shape enumeration, optical tests, global minimality or arbitrary real-grid claim.')
 (B/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
