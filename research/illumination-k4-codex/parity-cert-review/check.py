"""Census plus prescribed-event replay; never enumerates optical directions."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib
from event_model import EventModel,rank,canon,dot,cross,sub
B=Path(__file__).resolve().parent;I=B/'inputs'
def read(n):return json.loads((I/n).read_text())
def orient(a,b,c):return cross(sub(b,a),sub(c,a))
def on(a,b,p):return orient(a,b,p)==0 and all(min(a[j],b[j])<=p[j]<=max(a[j],b[j]) for j in (0,1))
def meet(a,b,c,d):
 v=[orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)]
 return any((not x) and on(e,f,p) for x,e,f,p in [(v[0],a,b,c),(v[1],a,b,d),(v[2],c,d,a),(v[3],c,d,b)]) or v[0]*v[1]<0 and v[2]*v[3]<0

def inside(V,p):
 if any(on(a,b,p) for a,b in zip(V,V[1:]+V[:1])):return False
 winding=0
 for a,b in zip(V,V[1:]+V[:1]):
  if a[1]<=p[1]<b[1] and orient(a,b,p)>0:winding+=1
  elif b[1]<=p[1]<a[1] and orient(a,b,p)<0:winding-=1
 return winding!=0

def key(room):
 V=room['vertices'];marks=room['marked'];ks=[]
 for swap in (False,True):
  for sx in (-1,1):
   for sy in (-1,1):
    def transform(p):
     x,y=p[::-1] if swap else p
     return sx*x,sy*y
    P=list(map(transform,V));M=list(map(transform,marks));x0=min(x for x,y in P)//2*2;y0=min(y for x,y in P)//2*2
    P=[(x-x0,y-y0) for x,y in P];M=tuple(sorted((x-x0,y-y0) for x,y in M))
    cycles=[]
    for C in (P,P[::-1]):
     j=C.index(min(C));cycles.append(tuple(C[j:]+C[:j]))
    ks.append((min(cycles),M))
 return min(ks)

rows=[json.loads(l) for l in (I/'certs-W26.jsonl').read_text().splitlines()];counts=Counter(r['W'] for r in rows);assert counts=={24:12,25:89,26:226}
keys={};room_checks=0
for r in rows:
 room=read(r['tag']+'.json');V=list(map(tuple,room['vertices']));w=len(V);assert w==r['W'] and len(set(V))==w
 edges=list(zip(V,V[1:]+V[:1]))
 for i,(a,b) in enumerate(edges):
  dx,dy=sub(b,a);assert dx or dy;assert not dx or not dy or abs(dx)==abs(dy)
  if dx and dy:assert (a[0]+a[1])%2==0
  assert orient(V[i-1],a,b)
  for j,(c,d) in enumerate(edges[:i]):
   if j==i-1 or (i==w-1 and j==0):continue
   assert not meet(a,b,c,d)
 interior=[]
 for x in range(min(x for x,y in V),max(x for x,y in V)+1):
  for y in range(min(y for x,y in V),max(y for x,y in V)+1):
   p=(x,y)
   if inside(V,p):assert x%2==0 and y%2==0;interior.append(p)
   elif any(on(a,b,p) for a,b in edges) and (x%2 or y%2):assert p in V
 assert len(interior)==2 and sorted(interior)==sorted(map(tuple,room['marked']))
 assert r['interior_A']==2 and r['R']==12 and r['lit']==0 and r['rigid'] and r['error'] is None
 k=key(room);assert k not in keys;keys[k]=r['tag'];room_checks+=1
old=[json.loads(l) for l in (I/'certs-W24.jsonl').read_text().splitlines()];assert len(old)==12
assert old==[r for r in rows if r['W']==24]  # Saved summary consistency; old geometry not independently archived.
print(json.dumps(dict(census='PASS',counts=dict(counts),rooms_checked=room_checks)),flush=True)
results=[]
for r in read('selected.json'):
 tag=r['tag'];room=read(tag+'.json');m=EventModel(room);peer=read('funcs-'+tag+'-R12.json');events=read('events-'+tag+'-R12.json')['rows'];pos=read('posspan-'+tag+'-R12.json')
 assert len(events)==r['events']==len(peer['funcs']);assert set(map(tuple,m.closure))=={tuple(map(F,c)) for c in peer['clos']}
 funcs=[tuple(map(F,g)) for g in peer['funcs']];replayed=[]
 for e,pf in zip(events,funcs):
  # Only exactly the side and direction in each saved certificate are replayed.
  got=m.event(tuple(e['dir']),e['side']);assert got['status']=='EVENT',(tag,e,got)
  assert tuple(got['corner'])==tuple(e['corner']);assert list(map(F,got['unfolded_target_minus_s']))==list(map(F,e['unfolded_target_minus_s']))
  assert canon(m.project(pf))==canon(m.project(tuple(map(F,got['gradient'])))),(tag,e,got)
  replayed.append(got)
 coefficients={int(i):F(x) for i,x in pos['coefficients'].items()};assert set(coefficients)==set(range(len(funcs))) and all(x>0 for x in coefficients.values())
 weighted=tuple(sum(coefficients[i]*funcs[i][j] for i in coefficients) for j in range(m.dim));assert not any(m.project(weighted))
 rk=rank([*m.closure,*funcs])-2;assert rk==m.dim-2-rank(m.syms)==r['rank']==r['target']
 assert all(dot(g,s)==0 for g in funcs for s in m.syms)
 # Independent corruption controls: exact dependency rejects a flipped weight,
 # and the geometry comparison rejects a deliberately reversed functional.
 bad=dict(coefficients);idx=next(i for i,g in enumerate(funcs) if any(m.project(g)));bad[idx]=-bad[idx]
 assert any(m.project(tuple(sum(bad[i]*funcs[i][j] for i in bad) for j in range(m.dim))))
 assert canon(m.project(tuple(-x for x in funcs[idx])))!=canon(m.project(funcs[idx]))
 out=dict(tag=tag,W=r['W'],events=len(events),rank=rk,kernel_dimension=m.dim-2-rk,symmetry_dimension=rank(m.syms),positive_dependency=True,corruptions_rejected=2)
 results.append(out);print(json.dumps(out),flush=True)
result=dict(status='PASS',census=dict(counts),geometry_and_parity_rooms=room_checks,distinct_D4_even_translation_classes=len(keys),W24_consistency=True,sample=results,event_replays=sum(r['events'] for r in results),scope='Census and fixed supplied-event sample only; no enumeration rerun or new room/ray/direction discovery. Unreplayed certificates remain peer results.')
(B/'check.json').write_text(json.dumps(result,indent=2)+'\n')
files=sorted(p for p in I.rglob('*') if p.is_file())+[B/'check.py',B/'event_model.py']
(B/'manifest.json').write_text(json.dumps({str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
print(json.dumps(dict(status='PASS',event_replays=result['event_replays'])),flush=True)
