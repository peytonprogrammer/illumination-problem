"""Independent local geometry, fixed-boundary replay and terminal-receipt audit.
No boundary/room search, ray search or duplicate long run.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import json,subprocess,re,hashlib,ctypes
B=Path(__file__).resolve().parent
D=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def label(p):return 'A' if not(p[0]%2 or p[1]%2) else 'B' if p[0]%2 and p[1]%2 else 'C'
def ccw_sector(out,back,v):
 z=cross(out,back)
 if z>0:return cross(out,v)>0 and cross(v,back)>0
 if z<0:return cross(out,v)>0 or cross(v,back)>0
 assert out!=back
 return cross(out,v)>0

def cycle(room):
 tris=[tuple(map(tuple,t)) for t in room['triangles']];counts=Counter(tuple(sorted(e)) for t in tris for e in combinations(t,2));adj={}
 for (a,b),n in counts.items():
  if n==1:adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
 assert all(len(a)==2 for a in adj.values())
 v=min(adj);start=v;old=None;out=[v]
 while True:
  nxt=min(p for p in adj[v] if p!=old)
  if nxt==start:break
  assert nxt not in out;out.append(nxt);old,v=v,nxt
 assert len(out)==len(adj)
 return out

def orient_root(vs):
 if sum(cross(a,b) for a,b in zip(vs,vs[1:]+vs[:1]))<0:vs=vs[::-1]
 k=min(range(len(vs)),key=lambda i:(vs[i][1],vs[i][0]));vs=vs[k:]+vs[:k]
 shift=tuple(2*(v//2) for v in vs[0]);return [sub(v,shift) for v in vs]

def main():
 local=[json.loads(s) for s in (B/'cases.jsonl').read_text().splitlines()];assert len(local)==120
 for c in local:
  v=tuple(c['site']);out=D[c['dout']];back=tuple(-x for x in D[c['din']]);inside_points=set()
  assert c['conflict']==0
  for a,b,d,e,f,g,observed in c['tiles']:
   tri=[(a,b),(d,e),(f,g)];centroid=tuple(sum(p[j]-v[j] for p in tri) for j in (0,1));expected=ccw_sector(out,back,centroid)
   assert expected==bool(observed),(c,tri)
   assert Counter(map(label,tri))==Counter('ABC')
   if expected:inside_points.update(tri)
  required={p for p in inside_points if label(p)!='A' and p!=v};assert c['req']==len(required)
 fixed=[];logs=[];frozen=B.parent/'isolation-review/inputs'
 for name,W in [('room-illumination-search-simple-unrestricted',24),('room-tokarsky34',34),('room-jain28',28)]:
  vs=cycle(json.loads((frozen/(name+'.json')).read_text()))
  for swap in (False,True):
   for sx in (-1,1):
    for sy in (-1,1):
     transformed=[(sx*(p[1] if swap else p[0]),sy*(p[0] if swap else p[1])) for p in vs];rooted=orient_root(transformed)
     expected=0 if name=='room-jain28' else 1
     text=f'{W} {len(rooted)} {expected}\n'+''.join(f'{x} {y}\n' for x,y in rooted)
     r=subprocess.run([str(B/'audit')],input=text,text=True,capture_output=True)
     logs.append(f'{name} swap={swap} signs={sx},{sy}\n{r.stdout}{r.stderr}')
     assert r.returncode==0,(name,r.stderr)
     m=re.search(r'FIXED PASS walls=(\d+) atomic_vertices=(\d+) maxreq=(\d+)',r.stderr);assert m and int(m[1])==W
     fixed.append(dict(room=name,swap=swap,signs=[sx,sy],walls=W,atomic_vertices=int(m[2]),max_required=int(m[3]),expected_acceptance=bool(expected)))
 (B/'fixed-controls.log').write_text('\n'.join(logs))
 receipts=[]
 for k in range(4):
  s=(B/'inputs'/f'log-W22-s{k}.txt').read_text();m=re.fullmatch(r'WMAX 22 nodes (\d+) closed (\d+) found 0\n',s);assert m
  assert (B/'inputs'/f'rooms2-W22-s{k}.txt').stat().st_size==0
  receipts.append(dict(start=k,nodes=int(m[1]),closed=int(m[2]),found=0))
 assert ctypes.sizeof(ctypes.c_long)==8
 assert json.loads((B/'binary-compare.json').read_text())['status']=='PASS'
 result=dict(status='PASS',local_wedge_cases=len(local),fixed_boundary_replays=len(fixed),fixed_controls=fixed,receipts=receipts,total_nodes=sum(r['nodes'] for r in receipts),total_closed=sum(r['closed'] for r in receipts),host_long_bits=64,scope='Local wedge geometry, required-point counts, fixed-boundary prune/closure/rollback and completed receipt syntax checked. No duplicate enumeration. Separate binary-compare receipt verifies audited source/core correspondence; launch-start identifiers still rely on stored receipt names.')
 (B/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='fixed_controls'},indent=2))
if __name__=='__main__':main()
