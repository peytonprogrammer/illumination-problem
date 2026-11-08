"""Exact checks of the prescribed 3-copy and 4-copy constructions. No ray search."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parent
BASE=frozenset([(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3)])
MAPS=[(1,1,0,0),(1,-1,0,0),(-1,-1,4,0),(-1,1,-2,0)]
S=(0,0);T=(2,2)

def vertices(cells):return {v for x,y in cells for v in ((x,y),(x+1,y),(x+1,y+1),(x,y+1))}
def cells_at(p):
 x,y=p;return {(x-1,y-1),(x,y-1),(x-1,y),(x,y)}
def angle(cells,p):
 occupied=cells_at(p)&cells
 if len(occupied)==4:return 4
 if len(occupied)==2:
  a,b=occupied;assert abs(a[0]-b[0])+abs(a[1]-b[1])==1,('pinch',p)
 return len(occupied)
def geometry(cells):
 edge_count=Counter()
 for x,y in cells:
  v=((x,y),(x+1,y),(x+1,y+1),(x,y+1))
  for i in range(4):edge_count[tuple(sorted((v[i],v[(i+1)%4])))]+=1
 edges=[e for e,n in edge_count.items() if n==1];adj=defaultdict(list)
 for a,b in edges:adj[a].append(b);adj[b].append(a)
 assert all(len(n)==2 for n in adj.values()),'non-Jordan boundary fan'
 start=min(adj);cycle=[start];prev=None;cur=start
 while True:
  nxt=next(p for p in sorted(adj[cur]) if p!=prev)
  if nxt==start:break
  cycle.append(nxt);prev,cur=cur,nxt;assert len(cycle)<=len(adj)
 assert len(cycle)==len(adj),'multiple boundary cycles'
 maximal=[p for i,p in enumerate(cycle) if (p[0]-cycle[i-1][0])*(cycle[(i+1)%len(cycle)][1]-p[1])!=(p[1]-cycle[i-1][1])*(cycle[(i+1)%len(cycle)][0]-p[0])]
 actual={p for p in vertices(cells) if angle(cells,p) in (1,3)}
 assert actual==set(maximal)
 all_edges=set(edge_count);V=vertices(cells);assert len(V)-len(all_edges)+len(cells)==1
 seen={next(iter(cells))};todo=list(seen)
 for x,y in todo:
  for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
   if q in cells and q not in seen:seen.add(q);todo.append(q)
 assert seen==set(cells)
 return dict(cells=sorted(cells),vertices=maximal,walls=len(maximal),corners=sorted(actual),convex=sorted(p for p in actual if angle(cells,p)==1),concave=sorted(p for p in actual if angle(cells,p)==3),smooth=sorted(p for p in V if angle(cells,p)==2),interior=sorted(p for p in V if angle(cells,p)==4),atomic_edges=edges,euler=1)

def point(g,p):sx,sy,dx,dy=g;return (sx*p[0]+dx,sy*p[1]+dy)
def inverse(g,p):sx,sy,dx,dy=g;return (sx*(p[0]-dx),sy*(p[1]-dy))
def image(g,cells):
 out=set()
 for x,y in cells:
  v=[point(g,p) for p in ((x,y),(x+1,y),(x,y+1),(x+1,y+1))]
  out.add((min(p[0] for p in v),min(p[1] for p in v)))
 return frozenset(out)

def check(m):
 copies=[image(g,BASE) for g in MAPS[:m]]
 assert all(not(a&b) for a,b in combinations(copies,2)),'interior overlap'
 room=frozenset().union(*copies);q=geometry(room);base=geometry(BASE)
 assert angle(room,S)==angle(room,T)==4
 seams=[];touches=[]
 for i,j in combinations(range(m),2):
  vi,vj=vertices(copies[i]),vertices(copies[j]);common=vi&vj
  shared=[]
  for edge in qedges(copies[i])&qedges(copies[j]):
   assert all(inverse(MAPS[i],z)==inverse(MAPS[j],z) for z in edge),'discontinuous fold'
   shared.append(edge)
  if shared:seams.append(dict(copies=[i,j],edges=sorted(shared)))
  elif common:touches.append(dict(copies=[i,j],points=sorted(common)))
 incidences=defaultdict(list)
 for i,g in enumerate(MAPS[:m]):
  for c in base['corners']:incidences[point(g,c)].append((i,c))
 reversal=[];true=[]
 for p,inc in sorted(incidences.items()):
  targets={inverse(MAPS[i],p) for i,c in inc};assert len(targets)==1
  base_point=next(iter(targets));n=angle(room,p)
  if n==2:
   assert len(inc)==2 and angle(BASE,base_point)==1
   tangents={('horizontal' if a[1]==b[1] else 'vertical') for a,b in q['atomic_edges'] if p in (a,b)}
   assert len(tangents)==1
   wall=next(iter(tangents));rw=(1,-1) if wall=='horizontal' else (-1,1)
   for (i,_),(j,_) in (inc,inc[::-1]):
    gi,gj=MAPS[i],MAPS[j]
    assert (gj[0]*rw[0]*gi[0],gj[1]*rw[1]*gi[1])==(-1,-1)
   reversal.append(dict(physical=p,base=base_point,copies=[i for i,c in inc],wall=wall,folded_velocity_factor=[-1,-1]))
  else:
   assert n in (1,3),'a base corner became interior'
   true.append(dict(physical=p,base=base_point,copy_incidences=len(inc),angle_units=n))
 assert sum(x['copy_incidences'] for x in true)+2*len(reversal)==10*m
 assert len({tuple(x['physical']) for x in true})==q['walls']
 for i,g in enumerate(MAPS[:m]):
  for c in base['concave']:assert point(g,c) in set(q['corners'])
 fibers={name:sorted({point(g,z) for g in MAPS[:m]}) for name,z in [('a',(0,0)),('b',(2,-2))]}
 for name,ps in fibers.items():
  for p in ps:
   assert len({inverse(g,p) for g,cs in zip(MAPS[:m],copies) if p in vertices(cs)})==1
 packet=dict(copies=m,copy_maps=MAPS[:m],base=base,room=q,marks=[S,T],seams=seams,point_contacts=touches,reversal_points=reversal,corner_incidence_locations=true,mark_fibers=fibers)
 return packet

def qedges(cells):
 counts=Counter()
 for x,y in cells:
  v=((x,y),(x+1,y),(x+1,y+1),(x,y+1))
  for i in range(4):counts[tuple(sorted((v[i],v[(i+1)%4])))]+=1
 return {e for e,n in counts.items() if n==1}

if __name__=='__main__':
 base=geometry(BASE);assert set(base['smooth'])=={(0,0),(2,-2)} and not base['interior'];assert (len(base['convex']),len(base['concave']))==(7,3)
 packets=[check(m) for m in (3,4)]
 assert packets[0]['room']['walls']==22
 (ROOT/'second-example.json').write_text(json.dumps(packets[1],indent=2)+'\n')
 (ROOT/'inputs/room22.json').write_text(json.dumps(packets[0],indent=2)+'\n')
 # Prescribed integer reflection parity controls. These support, not replace,
 # the elementary identity x -> 2c-x preserving x modulo two.
 parity_checks=0
 for c,x in product(range(-6,7),repeat=2):assert (2*c-x-x)%2==0;parity_checks+=1
 # Repeated halving for fixed even-even endpoint arithmetic controls.
 halving_checks=0
 for x,y in product(range(-16,17,2),repeat=2):
  if (x,y)==(0,0):continue
  z=(x,y);power=0
  while z[0]%2==z[1]%2==0:z=(z[0]//2,z[1]//2);power+=1
  assert power>=1 and z!=(0,0) and (z[0]%2 or z[1]%2);halving_checks+=1
 out=dict(status='PASS',base=base,packets=packets,reflection_parity_controls=parity_checks,halving_controls=halving_checks,scope='Prescribed constructions, exact topology, complete corner incidence and reversal matrices. No ray searches or proof by bounded non-finding.')
 (ROOT/'check.json').write_text(json.dumps(out,indent=2)+'\n')
 for q in packets:print(json.dumps(dict(copies=q['copies'],walls=q['room']['walls'],convex=len(q['room']['convex']),concave=len(q['room']['concave']),reversal_points=q['reversal_points'],mark_fibers=q['mark_fibers'])))
 print('PASS',parity_checks,'parity controls',halving_checks,'halving controls')
