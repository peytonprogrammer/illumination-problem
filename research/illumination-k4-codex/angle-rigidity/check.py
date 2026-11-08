"""Exact general-vertex derivatives of ONLY 147 previously saved event words."""
from fractions import Fraction as F
from pathlib import Path
import sys,json,hashlib
B=Path(__file__).resolve().parent
OLD=B.parent/'rigidity-review'
sys.path.insert(0,str(OLD))
import check as old
D=48
Z=(F(0),)*D
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(c,a):return tuple(c*x for x in a)
def unit(i):return tuple(F(j==i) for j in range(D))
def sub(a,b):return add(a,mul(-1,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
# U(x) = diag(s)*x+b; its matrix derivative only has off-diagonal entries u,v.
def identity():return ((1,1),(F(0),F(0)),Z,Z,(Z,Z))
def image(U,p,idx):
 s,b,u,v,db=U
 val=(s[0]*p[0]+b[0],s[1]*p[1]+b[1])
 jac=(add(add(mul(s[0],unit(idx)),mul(p[1],u)),db[0]),add(add(mul(s[1],unit(idx+1)),mul(p[0],v)),db[1]))
 return val,jac

def step(U,i):
 s,b,u,v,db=U;a=old.verts[i];j=(i+1)%22;z=old.verts[j];axis=old.axes[i];n=1-axis
 L=z[axis]-a[axis];h=mul(F(2,L),sub(unit(2*j+n),unit(2*i+n)))
 R=[1,1];R[n]=-1;bw=[F(0),F(0)];bw[n]=2*a[n]
 dbw=(sub(mul(2 if n==0 else 0,unit(2*i)),mul(a[1],h)),sub(mul(2 if n==1 else 0,unit(2*i+1)),mul(a[0],h)))
 return ((s[0]*R[0],s[1]*R[1]),(b[0]+s[0]*bw[0],b[1]+s[1]*bw[1]),add(mul(R[1],u),mul(s[0],h)),add(mul(R[0],v),mul(s[1],h)),(add(add(db[0],mul(bw[1],u)),mul(s[0],dbw[0])),add(add(db[1],mul(bw[0],v)),mul(s[1],dbw[1]))))

def event_gradient(e):
 U=identity();prefix=[U]
 for i in e['word']:U=step(U,i);prefix.append(U)
 tv,tj=image(U,old.t0,46);A=old.vecsub(tv,old.s0);dA=(sub(tj[0],unit(44)),sub(tj[1],unit(45)))
 c=tuple(e['corner']);j=old.verts.index(c);lower=F(0);found=[]
 for U,i in zip(prefix,[*e['word'],None]):
  cv,cj=image(U,c,2*j);C=old.vecsub(cv,old.s0);dC=(sub(cj[0],unit(44)),sub(cj[1],unit(45)))
  if i is None:upper=F(1)
  else:
   n=1-old.axes[i];upper=(U[0][n]*old.verts[i][n]+U[1][n]-old.s0[n])/A[n]
  assert lower<=upper
  t=dot(A,C)/dot(A,A)
  if old.cross(A,C)==0 and 0<t<1 and lower<=t<=upper:
   g=mul(e['perturb_side'],add(add(mul(C[1],dA[0]),mul(A[0],dC[1])),add(mul(-C[0],dA[1]),mul(-A[1],dC[0]))))
   found.append((g,t))
  lower=upper
 assert found and all(x==found[0] for x in found)
 return found[0]

def main():
 events=json.loads((OLD/'events.json').read_text());rows=[];params=[]
 pull=[a for p in old.vforms for a in p]+[old.unit(i) for i in range(24,28)]
 for e in events:
  g,t=event_gradient(e);rows.append(g);params.append(str(t))
  back=tuple(sum(g[j]*pull[j][i] for j in range(D)) for i in range(28));diff=old.vecsub(back,tuple(map(F,e['gradient'])))
  assert old.rank([*old.clos,diff])==2,'orthogonal restriction mismatch'
 points=old.verts+[old.s0,old.t0];syms=[]
 for mode in range(5):
  q=[]
  for x,y in points:q.extend(((1,0) if mode==0 else (0,1) if mode==1 else (-y,x) if mode==2 else (x,0) if mode==3 else (0,y)))
  syms.append(q)
 assert old.rank(syms)==5 and all(dot(g,q)==0 for g in rows for q in syms)
 r=old.rank(rows)
 output=dict(status='EXACT_DERIVATIVES',events=len(rows),variables=D,rank=r,kernel_dimension=D-r,known_dark_tangent_dimension=5,orthogonal_restrictions_verified=len(rows),symmetries_annihilated=True,source_sha256=hashlib.sha256((OLD/'events.json').read_bytes()).hexdigest(),rows=[[str(x) for x in row] for row in rows],corner_parameters=params,vertices=old.verts,marks=[old.s0,old.t0],symmetries=syms)
 (B/'result.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('rows','corner_parameters','vertices','marks','symmetries')},indent=2))
if __name__=='__main__':main()
