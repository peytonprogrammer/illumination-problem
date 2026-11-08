"""Independent replay of supplied corner events using exact infinitesimals.
No peer code imports and no additional optical directions. Fraction arithmetic
reconstructs wall words, symbolic endpoint maps, derivative cones and ranks.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
from functools import total_ordering
import json,hashlib,math
B=Path(__file__).resolve().parent;IN=B/'inputs';DIM=28
@total_ordering
class D:
 def __init__(self,a=0,b=0):self.a=F(a);self.b=F(b)
 def __add__(self,o):o=dual(o);return D(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return D(-self.a,-self.b)
 def __sub__(self,o):return self+-dual(o)
 def __rsub__(self,o):return dual(o)+-self
 def __mul__(self,o):o=dual(o);return D(self.a*o.a,self.a*o.b+self.b*o.a)
 __rmul__=__mul__
 def __truediv__(self,o):o=dual(o);assert o.a;return D(self.a/o.a,(self.b*o.a-self.a*o.b)/(o.a*o.a))
 def __eq__(self,o):o=dual(o);return (self.a,self.b)==(o.a,o.b)
 def __lt__(self,o):o=dual(o);return (self.a,self.b)<(o.a,o.b)
def dual(x):return x if isinstance(x,D) else D(x)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def vecadd(a,b):return tuple(x+y for x,y in zip(a,b))
def vecsub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(k,a):return tuple(k*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(i):return tuple(F(j==i) for j in range(DIM))
def evaluate(a):return dot(a,theta)
def ptval(p):return tuple(evaluate(a) for a in p)
def ptgrad(p):return tuple(tuple(a) for a in p)
def canonical_row(r):
 if not any(r):return tuple(r)
 # Positive normalization preserves the one-sided inequality.
 den=math.lcm(*(x.denominator for x in r));ints=[int(x*den) for x in r];g=math.gcd(*ints)
 return tuple(x//g for x in ints)
def rank(rows):
 pivots={}
 for row in rows:
  r=list(map(F,row))
  for i,p in sorted(pivots.items()):
   if r[i]:r=[x-r[i]*y for x,y in zip(r,p)]
  if any(r):
   i=next(i for i,x in enumerate(r) if x);v=r[i];pivots[i]=[x/v for x in r]
 return len(pivots)

room=json.loads((IN/'cand-2_2-1.json').read_text());tris=[tuple(map(tuple,t)) for t in room['triangles']]
edges=Counter(tuple(sorted(e)) for t in tris for e in combinations(t,2));bd={e for e,n in edges.items() if n==1}
adj={}
for a,b in bd:adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
assert all(len(n)==2 for n in adj.values());start=min(adj);cycle=[start];last=None;v=start
while True:
 nxt=min(p for p in adj[v] if p!=last)
 if nxt==start:break
 cycle.append(nxt);last,v=v,nxt
# Atomic boundary can contain smooth subdivision points; retain actual corners.
verts=[p for i,p in enumerate(cycle) if cross(vecsub(p,cycle[i-1]),vecsub(cycle[(i+1)%len(cycle)],p))]
assert len(verts)==22
lengths=[];axes=[]
for a,b in zip(verts,verts[1:]+verts[:1]):
 delta=vecsub(b,a);axis=0 if delta[0] else 1;assert delta[1-axis]==0
 axes.append(axis);lengths.append(delta[axis])
s0,t0=map(tuple,room['marked']);assert (s0,t0)==((0,0),(2,2))
theta=tuple(map(F,verts[0]+tuple(lengths)+s0+t0));assert len(theta)==28
vforms=[];current=(unit(0),unit(1))
for i,axis in enumerate(axes):
 vforms.append(current);n=list(current);n[axis]=vecadd(n[axis],unit(2+i));current=tuple(n)
clos=[tuple(sum((unit(2+i)[j] for i,ax in enumerate(axes) if ax==axis),F(0)) for j in range(DIM)) for axis in (0,1)]
assert all(ptval(v)==p for v,p in zip(vforms,verts)) and all(dot(c,theta)==0 for c in clos)
sforms=(unit(24),unit(25));tforms=(unit(26),unit(27))
# Independently derive global affine directions from physical coordinates.
syms=[]
for axis,mode in ((0,'translation'),(1,'translation'),(0,'scale'),(1,'scale')):
 row=[F(0)]*DIM
 if mode=='translation':row[axis]=row[24+axis]=row[26+axis]=1
 else:
  row[axis]=verts[0][axis];row[24+axis]=s0[axis];row[26+axis]=t0[axis]
  for i,ax in enumerate(axes):
   if ax==axis:row[2+i]=lengths[i]
 syms.append(tuple(row))

def target_on_limit(pos,d,tau):
 delta=tuple(F(t0[j])-pos[j].a for j in (0,1));direction=tuple(x.a for x in d)
 if cross(delta,direction):return False
 j=next(j for j in (0,1) if direction[j]);mu=delta[j]/direction[j]
 return 0<mu<tau.a

def trace(q,side,maxhits=1000):
 # q + eps*side*perp(q) is used only to resolve the prescribed singular event.
 pos=tuple(D(c) for c in s0);direction=(D(q[0],-side*q[1]),D(q[1],side*q[0]))
 word=[];corner=None;corner_unfold=None;corner_order=[];sgn=[1,1];shift=[(F(0),)*DIM,(F(0),)*DIM]
 for hit in range(maxhits):
  candidates=[]
  for i,(a,b) in enumerate(zip(verts,verts[1:]+verts[:1])):
   normal=1-axes[i];parallel=axes[i]
   if not direction[normal].a:continue
   tau=(D(a[normal])-pos[normal])/direction[normal]
   if tau<=0:continue
   at=pos[parallel]+tau*direction[parallel];lo,hi=sorted((a[parallel],b[parallel]))
   if D(lo)<=at<=D(hi):candidates.append((tau,i))
  if not candidates:return dict(status='NO_WALL',hits=hit)
  tau,idx=min(candidates,key=lambda v:v[0])
  # Detect singular vertices on the limiting segment, including the branch
  # that passes a reflex corner without reflecting at either incident wall.
  dv=tuple(d.a for d in direction);pv=tuple(p.a for p in pos);axis=next(j for j in (0,1) if dv[j])
  target_here=target_on_limit(pos,direction,tau)
  end=(F(t0[axis])-pv[axis])/dv[axis] if target_here else tau.a
  crossed=[]
  for vertex in verts:
   delta=vecsub(vertex,pv)
   if cross(delta,dv):continue
   mu=delta[axis]/dv[axis]
   if 0<mu<=end:crossed.append((mu,vertex))
  for mu,vertex in sorted(crossed):
   if corner is None:
    corner=vertex;j=verts.index(corner);corner_unfold=tuple(vecadd(scale(sgn[k],vforms[j][k]),shift[k]) for k in (0,1))
   else:
    j=verts.index(vertex);image=tuple(vecadd(scale(sgn[k],vforms[j][k]),shift[k]) for k in (0,1))
    if ptval(image)!=ptval(corner_unfold):return dict(status='SECOND_CORNER',hits=hit,first=corner,second=vertex)
  if target_here:
   if corner is None:return dict(status='ORDINARY_TARGET',hits=hit)
   tu=tuple(vecadd(scale(sgn[j],tforms[j]),shift[j]) for j in (0,1))
   A=tuple(vecsub(tu[j],sforms[j]) for j in (0,1));C=tuple(vecsub(corner_unfold[j],sforms[j]) for j in (0,1));av=ptval(A);cv=ptval(C)
   assert cross(av,cv)==0 and dot(av,cv)>0 and dot(cv,cv)<dot(av,av)
   grad=tuple(side*(A[0][i]*cv[1]+av[0]*C[1][i]-A[1][i]*cv[0]-av[1]*C[0][i]) for i in range(DIM))
   return dict(status='EVENT',direction=q,perturb_side=side,corner=corner,word=word,gradient=list(map(str,grad)),row=list(canonical_row(grad)),hits=hit,corner_order=corner_order)
  pos=tuple(p+tau*d for p,d in zip(pos,direction));pv=tuple(p.a for p in pos)
  if pv in verts:
   if corner is None:
    corner=pv;j=verts.index(corner);corner_unfold=tuple(vecadd(scale(sgn[k],vforms[j][k]),shift[k]) for k in (0,1))
   elif corner!=pv:return dict(status='SECOND_CORNER',hits=hit,first=corner,second=pv)
   corner_order.append((idx,tuple(str(x.b) for x in pos)))
  word.append(idx);normal=1-axes[idx]
  shift[normal]=vecadd(shift[normal],scale(2*sgn[normal],vforms[idx][normal]));sgn[normal]*=-1
  direction=list(direction);direction[normal]=-direction[normal];direction=tuple(direction)
 return dict(status='CAP',hits=maxhits)

if __name__=='__main__':
 supplied=json.loads((IN/'rigidity-R12.json').read_text());peer=json.loads((IN/'funcs-R12.json').read_text());pfuncs=[tuple(map(F,r)) for r in peer['funcs']]
 assert set(clos)=={tuple(map(F,r)) for r in peer['clos']};assert syms==[tuple(map(F,r)) for r in peer['syms']]
 directions=sorted({tuple(e['dir']) for e in supplied['event_list']});events=[];failures=Counter()
 for q in directions:
  for side in (-1,1):
   r=trace(q,side)
   if r['status']=='EVENT':events.append(r)
   else:failures[r['status']]+=1
 rows={tuple(e['row']) for e in events};prows={canonical_row(r) for r in pfuncs}
 result=dict(status='PRELIMINARY',supplied_directions=len(directions),replayed_sides=2*len(directions),reconstructed_events=len(events),distinct_constraints=len(rows),peer_constraints=len(prows),matches=len(rows&prows),own_only=len(rows-prows),peer_only=len(prows-rows),other_limits=dict(failures),rank_with_closure=rank([*clos,*rows]),rank_on_closure=rank([*clos,*rows])-rank(clos),affine_symmetries_annihilated=all(dot(r,s)==0 for r in rows for s in syms))
 coeff={int(i):F(v) for i,v in json.loads((IN/'posspan-R12.json').read_text())['coefficients'].items()}
 assert set(coeff)==set(range(len(pfuncs))) and all(v>0 for v in coeff.values())
 weighted=[sum(coeff[i]*pfuncs[i][j] for i in coeff) for j in range(DIM)]
 assert rank([*clos,weighted])==rank(clos),'Dependency fails on closure subspace'
 byrow={tuple(e['row']):e for e in events}
 matches=[]
 for i,pf in enumerate(pfuncs):
  event=byrow[canonical_row(pf)];given=supplied['event_list'][i]
  assert list(event['direction'])==given['dir'] and list(event['corner'])==given['corner']
  ours=tuple(map(F,event['gradient']));pivot=next(j for j,x in enumerate(ours) if x)
  ratio=pf[pivot]/ours[pivot];assert ratio>0 and all(p==ratio*x for p,x in zip(pf,ours))
  matches.append(dict(peer_index=i,perturb_side=event['perturb_side'],positive_scale=str(ratio)))
 result.update(status='PASS',positive_coefficients=len(coeff),dependency_zero_on_closure=True,peer_event_metadata_matches=len(matches),kernel_dimension_on_closure=DIM-rank([*clos,*rows]),affine_subspace_dimension=rank(syms),event_reflection_counts=dict(Counter(len(e['corner_order']) for e in events)))
 assert result['rank_on_closure']==22 and result['kernel_dimension_on_closure']==4 and rank(syms)==4
 result['scope']='Fixed supplied-event certificate replay only. Other one-sided limits are not used for coverage or exclusion.'
 (B/'events.json').write_text(json.dumps(events,indent=2,default=lambda x:int(x) if x.denominator==1 else str(x))+'\n');(B/'result.json').write_text(json.dumps(result,indent=2)+'\n');(B/'event-matches.json').write_text(json.dumps(matches,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
