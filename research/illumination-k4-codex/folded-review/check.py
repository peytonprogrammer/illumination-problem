"""Fixed local fold algebra and saved artifact census. No fold/ray search."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,ast,hashlib
B=Path(__file__).resolve().parent;I=B/'inputs'
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in (0,1)) for j in (0,1)) for i in (0,1))
def tr(a):return tuple(zip(*a))
ID=((1,0),(0,1));NEG=((-1,0),(0,-1));H=((1,0),(0,-1))
# Reflection matrices at ray angles 0,45,...315 degrees.
R=[H,((0,1),(1,0)),((-1,0),(0,1)),((0,-1),(-1,0)),H,((0,1),(1,0)),((-1,0),(0,1)),((0,-1),(-1,0))]
controls=[]
for theta,k,where in [(1,4,'smooth'),(1,8,'interior'),(2,2,'smooth'),(2,4,'interior')]:
 unfold=[ID]
 for j in range(1,k):unfold.append(mm(R[j*theta%8],unfold[-1]))
 for j in range(k):
  out=k-1-j if where=='smooth' else (j+k//2)%k
  physical=H if where=='smooth' else ID
  assert mm(mm(tr(unfold[out]),physical),unfold[j])==NEG
  controls.append((theta*45,k,where,j,out))

def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def on(a,b,p):return cross(sub(b,a),sub(p,a))==0 and all(min(a[j],b[j])<=p[j]<=max(a[j],b[j]) for j in (0,1))
def inside(V,p):
 if any(on(a,b,p) for a,b in zip(V,V[1:]+V[:1])):return False
 w=0
 for a,b in zip(V,V[1:]+V[:1]):
  if a[1]<=p[1]<b[1] and cross(sub(b,a),sub(p,a))>0:w+=1
  if b[1]<=p[1]<a[1] and cross(sub(b,a),sub(p,a))<0:w-=1
 return bool(w)
def key(V):
 keys=[]
 for swap in (False,True):
  for sx in (-1,1):
   for sy in (-1,1):
    P=[(sx*(y if swap else x),sy*(x if swap else y)) for x,y in V];ox=min(x for x,y in P);oy=min(y for x,y in P);P=[(x-ox,y-oy) for x,y in P]
    for C in [P,P[::-1]]:
     j=C.index(min(C));keys.append(tuple(C[j:]+C[:j]))
 return min(keys)
counts=Counter();marks=[]
for line in (I/'bases-W12.txt').read_text().splitlines():
 cols=line.split();w,n=int(cols[0]),int(cols[1]);V=[tuple(map(int,c.split(','))) for c in cols[2:]];assert len(V)==w
 nc=[]
 for x in range(min(x for x,y in V),max(x for x,y in V)+1):
  for y in range(min(y for x,y in V),max(y for x,y in V)+1):
   if (x,y) in V:continue
   if inside(V,(x,y)) or any(on(a,b,(x,y)) for a,b in zip(V,V[1:]+V[:1])):
    assert x%2==y%2==0;nc.append((x,y))
 assert n==len(nc)>=2;counts[w]+=1;marks.append(n)
assert counts=={9:8,10:52,11:128,12:224};assert not (I/'bases-W8.txt').read_text().strip();assert not (I/'hits.txt').read_text().strip()
# Only canonicalize supplied22-wall positive controls, not generate any fold.
keys=Counter()
for line in (I/'hits22.txt').read_text().splitlines():
 tail=line.split(' Wq ',1)[1];w=int(tail.split()[0]);assert w==22
 V=ast.literal_eval(tail.split(' poly ',1)[1].split(' pairs ',1)[0]);assert len(V)==22;keys[key(V)]+=1
result=dict(status='PASS',local_matrix_identities=len(controls),bases_by_walls=dict(counts),saved_empty_low_threshold_output=True,saved_22_listings=sum(keys.values()),distinct_unmarked_22_shapes=len(keys),shape_multiplicities=sorted(keys.values()),scope='Local algebra and saved-base/positive-control census only. No exhaustion rerun or binary provenance audit.')
(B/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
(B/'manifest.json').write_text(json.dumps({str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(I.iterdir())},indent=2)+'\n')
