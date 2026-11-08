"""Extract one rational direction from an exact labeled-origami orbit proof.
No direction-radius search. Only replay the one certified direction physically.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,math
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('origami_frame',ROOT/'inputs/origami_frame.py')
o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)

def direction(V,S,T,limit=200000):
 r,u,lab,s0,frame=o.build(list(V),S,T)
 start=o.canon(r,u,lab,s0);seen={start};todo=[(start,((1,0),(0,1)),'')];checked=0
 # B maps coordinates of the current sheared surface back to the original.
 # From R_new=R U^-1, new right means old down then right.
 # From U_new=U R^-1, new up means old left then up.
 invT=((1,-1),(0,1));invL=((1,0),(-1,1))
 while todo:
  (R,U,lab),B,word=todo.pop();checked+=1
  s=R[0];distance=1
  while s!=0:
   if lab[s]=='block':break
   if lab[s]=='T':
    developed=(B[0][0],B[1][0])
    physical=o.ap(tuple(zip(*frame)),developed)
    assert math.gcd(abs(physical[0]),abs(physical[1]))==1
    return dict(status='LIT',direction=physical,shear_word=word,inverse_matrix=B,source_frame=frame,horizontal_steps=distance,visited=len(seen),checked=checked)
   s=R[s];distance+=1
  Ri,Ui=o.inv(R),o.inv(U)
  for a,b,inv,name in ((R,tuple(o.comp(U,Ri)),invT,'T'),(tuple(o.comp(R,Ui)),U,invL,'L')):
   nxt=o.canon(a,b,lab,0)
   if nxt not in seen:
    seen.add(nxt);todo.append((nxt,o.mul(B,inv),word+name))
    if len(seen)>limit:return dict(status='UNDECIDED',visited=len(seen),checked=checked)
 return dict(status='DARK',visited=len(seen),checked=checked)

def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def trace_direction(V,S,T,direction):
 """Replay exactly one prescribed direction; never scan directions."""
 V=[tuple(map(F,p)) for p in V];S=tuple(map(F,S));T=tuple(map(F,T))
 edges=list(zip(V,V[1:]+V[:1]));p=S;d=tuple(map(F,direction));path=[p];seen=set()
 while (p,d) not in seen:
  seen.add((p,d));hits=[]
  for a,b in edges:
   e=sub(b,a);den=cross(d,e)
   if not den:continue
   t=cross(sub(a,p),e)/den;s=cross(sub(a,p),d)/den
   if t>0 and 0<=s<=1:hits.append((t,a,b))
  assert hits,('no next wall',p,d)
  t=min(h[0] for h in hits)
  if cross(sub(T,p),d)==0:
   j=0 if d[0] else 1;target=(T[j]-p[j])/d[j]
   if 0<target<t:return path+[T]
  q=tuple(p[k]+t*d[k] for k in (0,1));assert q not in V,('certified direction hits actual corner',q)
  walls=[(a,b) for tt,a,b in hits if tt==t];assert len(walls)==1,(q,walls)
  a,b=walls[0];e=sub(b,a);norm=dot(e,e)
  d=tuple(2*dot(d,e)*e[k]/norm-d[k] for k in (0,1));p=q;path.append(q)
 raise AssertionError('certified direction repeats without reaching target')
